'use strict';
// Vercel serverless function: quote form -> GoHighLevel.
//
//   1. Upsert the contact  (POST /contacts/upsert; custom fields sent as
//                           { id, key, field_value } — id is required by
//                           GHL's spec, so IDs come from the field listing)
//   2. Upload photos       (POST /forms/upload-custom-files, multipart, parts
//                           keyed "<fieldId>_<uuid>")
//
// The contact is always written first. A photo failure never loses the lead:
// the response is still ok:true with a photoError flag.
//
// Env (Vercel project settings, server-side only):
//   GHL_LOCATION_ID, GHL_PIT_TOKEN          required
//   GHL_JOB_PHOTOS_FIELD_ID                 optional: the Job Photos field's
//     ID, or its key ("property_photo", "contact.property_photo" or
//     "{{contact.property_photo}}"). Unset or a key -> the ID is looked up once
//     via GET /locations/{id}/customFields and cached.
//
// Node 18+ runtime. No dependencies: global fetch, FormData, Blob, crypto.

const crypto = require('node:crypto');

// ---------------------------------------------------------------------------
// Field mapping. Form field name -> how it lands in GHL.
//   { key: 'x' }  binds by merge-field key  ("contact.x")
//   { id: '...' } binds by custom-field id   (use when a key is ambiguous —
//                 see scripts/list-custom-fields.mjs KEY RESOLUTION output)
// Standard contact properties are set alongside where noted.
// ---------------------------------------------------------------------------
const FIELDS = {
  full_name:        { standard: 'name' },                                  // -> firstName / lastName
  phone:            { standard: 'phone' },                                 // -> phone (E.164)
  email:            { standard: 'email' },                                 // -> email (lowercased)
  property_address: { key: 'property_address', standard: 'address1' },
  property_size:    { key: 'property_size' },
  service_needed:   { key: 'service_needed' },
  job_type:         { key: 'job_type' },
  job_notes:        { key: 'job_notes' },
  // photos: see PHOTO_FIELD_KEY below.
};

// File-upload field that receives the photos ({{contact.property_photo}}, type
// "File upload", Contact folder). The upload endpoint needs the field's ID;
// it is resolved from this key unless GHL_JOB_PHOTOS_FIELD_ID holds an ID.
const PHOTO_FIELD_KEY = 'property_photo';

const GHL = {
  base: 'https://services.leadconnectorhq.com',
  version: '2021-07-28',
  timeoutMs: 20000,
};

const LIMITS = {
  maxFiles: 6,
  maxFileBytes: 1.5 * 1024 * 1024,   // per decoded image
  maxTotalBytes: 3.2 * 1024 * 1024,  // all decoded images
  maxBodyBytes: 4.4 * 1024 * 1024,   // Vercel caps requests at 4.5 MB
  minFillMs: 2500,                   // faster than this is a bot
};

const ALLOWED_TYPES = { 'image/jpeg': 'jpg', 'image/png': 'png', 'image/gif': 'gif' };

const SOURCE = 'Website quote form';
const TAGS = ['website-quote-form'];
const THANK_YOU = '/thank-you/';

// ---------------------------------------------------------------------------

module.exports = async function handler(req, res) {
  if (req.method === 'GET' && new URL(req.url || '/', 'http://x').searchParams.has('check')) {
    return send(res, 200, await diagnose());
  }
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return send(res, 405, { ok: false, error: 'method_not_allowed' });
  }

  const env = readEnv();
  if (env.error) return send(res, 500, { ok: false, error: env.error });

  let body;
  try {
    body = await readBody(req);
  } catch (e) {
    return send(res, e.status || 400, { ok: false, error: e.code || 'bad_request' });
  }
  const isForm = body.__urlencoded === true;

  // --- spam: honeypot + minimum fill time. Both look like success. ---------
  if (str(body.company_website)) return finish(res, isForm, { ok: true, skipped: 'honeypot' });
  const started = Number(body._t);
  if (started && Date.now() - started < LIMITS.minFillMs) {
    return finish(res, isForm, { ok: true, skipped: 'too_fast' });
  }

  // --- validate + normalise ------------------------------------------------
  const phone = normaliseAuPhone(str(body.phone));
  if (!phone) return send(res, 400, { ok: false, error: 'phone_required' });
  const email = str(body.email).toLowerCase();
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
    return send(res, 400, { ok: false, error: 'email_invalid' });
  }
  const { firstName, lastName } = splitName(str(body.full_name));
  if (!firstName) return send(res, 400, { ok: false, error: 'name_required' });

  let photos;
  try {
    photos = validatePhotos(body.photos);
  } catch (e) {
    return send(res, 400, { ok: false, error: e.code || 'photos_invalid', detail: e.message });
  }

  // --- 1. upsert contact ---------------------------------------------------
  // Custom fields need their IDs (GHL spec: id required, value in
  // field_value). Fetched once per warm instance; if the listing fails the
  // contact is still saved, just without the custom fields.
  let fieldMap = null;
  try { fieldMap = await loadContactFields(env); }
  catch (e) { console.error('[quote] custom-field listing failed:', e.message); }

  const contact = {
    locationId: env.locationId,
    firstName,
    lastName,
    email: email || undefined,
    phone,
    address1: str(body.property_address) || undefined,
    country: 'AU',
    source: SOURCE,
    tags: TAGS,
    customFields: buildCustomFields(body, fieldMap),
  };

  let contactId;
  let fieldsError = false;
  try {
    contactId = await upsert(env, contact);
  } catch (e) {
    // A rejected custom field must never cost the lead: retry once without them.
    if (contact.customFields.length && (e.status === 400 || e.status === 422)) {
      console.error('[quote] upsert rejected custom fields, retrying without them:', e.message);
      lastUpsertError = { at: new Date().toISOString(), reason: e.message.slice(0, 400) };
      fieldsError = true;
      try { contactId = await upsert(env, Object.assign({}, contact, { customFields: [] })); }
      catch (e2) { e = e2; }
    }
    if (!contactId) {
      console.error('[quote] upsert failed:', e.message);
      lastUpsertError = { at: new Date().toISOString(), reason: e.message.slice(0, 400) };
      return send(res, 502, { ok: false, error: 'upsert_failed' });
    }
  }

  // --- 2. upload photos (never fatal) -------------------------------------
  const out = { ok: true, contactId, photos: { received: photos.length, uploaded: 0 } };
  if (fieldsError) out.fieldsError = true;
  if (photos.length) {
    try {
      out.photos.uploaded = await uploadPhotos(env, contactId, photos);
    } catch (e) {
      console.error('[quote] photo upload failed for', contactId, ':', e.message);
      lastPhotoError = { at: new Date().toISOString(), photos: photos.length, reason: e.message.slice(0, 400) };
      out.photoError = true;
    }
  }
  return finish(res, isForm, out);
};

// ---------------------------------------------------------------------------
// GHL calls
// ---------------------------------------------------------------------------
async function ghlJson(method, path, token, payload) {
  const r = await fetch(GHL.base + path, {
    method,
    headers: {
      Authorization: 'Bearer ' + token,
      Version: GHL.version,
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(GHL.timeoutMs),
  });
  const text = await r.text();
  if (!r.ok) { const e = new Error(`${method} ${path} -> ${r.status} ${text.slice(0, 300)}`); e.status = r.status; throw e; }
  try { return JSON.parse(text); } catch { throw new Error(`${path} returned non-JSON`); }
}

// GHL custom-field IDs are ~20 mixed-case alphanumerics; keys contain "_",
// "." or braces. Anything that is not clearly an ID is treated as a key.
function looksLikeFieldId(v) { return /^[A-Za-z0-9]{16,40}$/.test(v); }
function normaliseFieldKey(v) {
  return String(v || '').trim().replace(/^\{\{\s*/, '').replace(/\s*\}\}$/, '').replace(/^contact\./, '');
}

// Response shape of the custom-field listing is not part of the verified
// contract, so find the first array of field-shaped objects (same approach as
// scripts/list-custom-fields.mjs) rather than assume a property name.
function findFieldArray(node, depth = 0) {
  if (depth > 4 || !node || typeof node !== 'object') return null;
  if (Array.isArray(node)) {
    return node.length && node.every(x => x && typeof x === 'object' && 'id' in x && ('fieldKey' in x || 'key' in x))
      ? node : null;
  }
  for (const v of Object.values(node)) { const f = findFieldArray(v, depth + 1); if (f) return f; }
  return null;
}

// Contact custom fields by key ("property_photo" -> { id, type, multi, max }).
// Cached per warm function instance for FIELD_CACHE_MS.
const FIELD_CACHE_MS = 10 * 60 * 1000;
let fieldCache = null;   // { at, map }

async function fetchContactFields(env) {
  const url = `${GHL.base}/locations/${encodeURIComponent(env.locationId)}/customFields?model=contact`;
  const r = await fetch(url, {
    headers: { Authorization: 'Bearer ' + env.token, Version: GHL.version, Accept: 'application/json' },
    signal: AbortSignal.timeout(GHL.timeoutMs),
  });
  const text = await r.text();
  if (!r.ok) { const e = new Error(`customFields -> ${r.status} ${text.slice(0, 300)}`); e.status = r.status; throw e; }
  let fields;
  try { fields = findFieldArray(JSON.parse(text)); } catch { fields = null; }
  if (!fields) throw new Error('customFields: could not find a field list in the response');
  const map = new Map();
  for (const f of fields) {
    const fk = String(f.fieldKey ?? f.key ?? '');
    if (fk && !fk.startsWith('contact.') && fk.includes('.')) continue;   // opportunity twins etc.
    const key = fk.replace(/^contact\./, '');
    if (!key || map.has(key)) continue;
    map.set(key, {
      id: f.id, name: f.name, fieldKey: fk, type: String(f.dataType ?? f.type ?? ''),
      multi: f.isMultiFileAllowed, max: f.maxFileLimit,
    });
  }
  return map;
}

async function loadContactFields(env, { fresh = false } = {}) {
  if (!fresh && fieldCache && Date.now() - fieldCache.at < FIELD_CACHE_MS) return fieldCache.map;
  const map = await fetchContactFields(env);
  fieldCache = { at: Date.now(), map };
  return map;
}

async function resolvePhotoField(env) {
  const configured = String(env.photoField || '').trim();
  const map = await loadContactFields(env).catch(e => {
    if (configured && looksLikeFieldId(configured)) return null;   // can still upload by ID
    throw e;
  });
  if (configured && looksLikeFieldId(configured)) {
    const meta = map && [...map.values()].find(f => f.id === configured);
    return meta || { id: configured };
  }
  const key = normaliseFieldKey(configured) || PHOTO_FIELD_KEY;
  const meta = map.get(key);
  if (!meta) throw new Error(`customFields: no contact field with key "contact.${key}"`);
  if (meta.type && !/file/i.test(meta.type)) console.warn(`[quote] "${key}" field type is "${meta.type}", expected a file upload`);
  return meta;
}

async function upsert(env, contact) {
  const r = await ghlJson('POST', '/contacts/upsert', env.token, contact);
  const id = r && r.contact && r.contact.id;
  if (!id) throw new Error('upsert returned no contact id');
  return id;
}

// ---------------------------------------------------------------------------
// GET /api/quote?check  — read-only setup check, for when photos go missing
// and the Vercel logs are not to hand. Never returns the token. Makes one
// read call to GHL (the custom-field listing); writes nothing.
// ---------------------------------------------------------------------------
let lastPhotoError = null;   // best effort: only this warm instance remembers it
let lastUpsertError = null;

async function diagnose() {
  const ghlVars = Object.keys(process.env).filter(k => /^GHL_|LEADCONNECTOR|HIGHLEVEL/i.test(k)).sort();
  const photoSetting = String(process.env.GHL_JOB_PHOTOS_FIELD_ID || '').trim();
  const out = {
    env: {
      GHL_LOCATION_ID: process.env.GHL_LOCATION_ID ? 'set (' + process.env.GHL_LOCATION_ID + ')' : 'MISSING',
      GHL_PIT_TOKEN: process.env.GHL_PIT_TOKEN ? 'set (' + process.env.GHL_PIT_TOKEN.length + ' chars, starts "' + process.env.GHL_PIT_TOKEN.slice(0, 4) + '…")' : 'MISSING',
      GHL_JOB_PHOTOS_FIELD_ID: !photoSetting ? 'not set (fine: looked up by key)'
        : looksLikeFieldId(photoSetting) ? 'set to an ID: ' + photoSetting : 'set to a key: ' + photoSetting,
      ghl_variable_names_seen: ghlVars,
    },
    customFieldLookup: null,
    fields: null,
    jobPhotosField: null,
    lastUpsertErrorOnThisInstance: lastUpsertError,
    lastPhotoErrorOnThisInstance: lastPhotoError,
  };
  const env = readEnv();
  if (env.error) { out.verdict = 'Missing GHL_LOCATION_ID or GHL_PIT_TOKEN (check the exact names) and redeploy.'; return out; }
  let map;
  try {
    map = await loadContactFields(env, { fresh: true });
    out.customFieldLookup = { status: 200, ok: true, contactFields: map.size };
  } catch (e) {
    out.customFieldLookup = { status: e.status || null, ok: false, error: e.message.slice(0, 300) };
    out.verdict = e.status === 401 || e.status === 403
      ? 'GHL rejected the token. It needs these Private Integration scopes: contacts.write, locations/customFields.readonly, forms.write.'
      : 'Could not list custom fields; see customFieldLookup.';
    return out;
  }
  out.fields = {};
  const missing = [];
  for (const [name, m] of Object.entries(FIELDS)) {
    if (!m.key) continue;
    const f = map.get(m.key);
    out.fields[name] = f ? `${f.fieldKey} -> ${f.id} (${f.type})` : 'NOT FOUND';
    if (!f) missing.push('contact.' + m.key);
  }
  const photoKey = normaliseFieldKey(photoSetting && !looksLikeFieldId(photoSetting) ? photoSetting : '') || PHOTO_FIELD_KEY;
  const pf = photoSetting && looksLikeFieldId(photoSetting)
    ? [...map.values()].find(f => f.id === photoSetting) : map.get(photoKey);
  out.jobPhotosField = pf ? { id: pf.id, name: pf.name, fieldKey: pf.fieldKey, type: pf.type,
    allowsMultipleFiles: pf.multi ?? 'not reported', maxFiles: pf.max ?? 'not reported' } : 'NOT FOUND';
  const problems = [];
  if (photoSetting && !looksLikeFieldId(photoSetting) && photoKey !== PHOTO_FIELD_KEY) {
    problems.push(`GHL_JOB_PHOTOS_FIELD_ID points photos at contact.${photoKey}, not contact.${PHOTO_FIELD_KEY}: delete that variable (or set it to {{contact.${PHOTO_FIELD_KEY}}}) and redeploy`);
  }
  if (!pf) problems.push('no contact field contact.' + photoKey);
  else if (pf.type && !/file/i.test(pf.type)) problems.push('Job Photos is type ' + pf.type + ', not a file upload');
  else if (pf.multi === false) problems.push('Job Photos allows only ONE file: turn on multiple files in the field settings');
  if (missing.length) problems.push('missing contact fields: ' + missing.join(', '));
  if (lastUpsertError) problems.push('a recent contact save was rejected: see lastUpsertErrorOnThisInstance');
  if (lastPhotoError) problems.push('a recent photo upload failed: see lastPhotoErrorOnThisInstance');
  out.verdict = problems.length ? 'Problems: ' + problems.join('; ') + '.'
    : 'Setup looks right. If photos still go missing, submit once and reload this page straight after.';
  return out;
}

async function uploadPhotos(env, contactId, photos) {
  const field = await resolvePhotoField(env);
  const fieldId = field.id;
  // Respect the field's own settings: a single-file field keeps one photo.
  let limit = photos.length;
  if (field.multi === false) limit = 1;
  if (Number(field.max) > 0) limit = Math.min(limit, Number(field.max));
  if (limit < photos.length) {
    console.warn(`[quote] Job Photos field accepts ${limit} file(s); sending ${limit} of ${photos.length}`);
  }
  const fd = new FormData();
  for (const p of photos.slice(0, limit)) {
    // One part per file. Key = "<customFieldId>_<uuid>"; all parts sharing the
    // field id land in the same custom field.
    const part = fieldId + '_' + crypto.randomUUID();
    fd.append(part, new Blob([p.bytes], { type: p.type }), p.filename);
  }
  const qs = new URLSearchParams({ contactId, locationId: env.locationId });
  const r = await fetch(`${GHL.base}/forms/upload-custom-files?${qs}`, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + env.token, Version: GHL.version },
    body: fd,
    signal: AbortSignal.timeout(GHL.timeoutMs),
  });
  if (!r.ok) throw new Error(`upload-custom-files -> ${r.status} ${(await r.text()).slice(0, 300)}`);
  return limit;
}

// ---------------------------------------------------------------------------
// Mapping + validation
// ---------------------------------------------------------------------------
// GHL spec for upsert customFields: { id (required), key, field_value }.
// Without the field listing (fieldMap null) send key + field_value as a best
// effort; the handler retries without custom fields if GHL rejects them.
function buildCustomFields(body, fieldMap) {
  const out = [];
  for (const [name, map] of Object.entries(FIELDS)) {
    if (!map.key && !map.id) continue;
    const value = str(body[name]);
    if (!value) continue;
    const id = map.id || (fieldMap && fieldMap.get(map.key) && fieldMap.get(map.key).id);
    if (id) out.push({ id, key: map.key, field_value: value });
    else if (!fieldMap) out.push({ key: map.key, field_value: value });
    else console.warn(`[quote] no contact field with key "contact.${map.key}"; "${name}" not saved`);
  }
  return out;
}

function validatePhotos(list) {
  if (list == null) return [];
  if (!Array.isArray(list)) throw err('photos_invalid', 'photos must be an array');
  if (list.length > LIMITS.maxFiles) throw err('too_many_photos', `max ${LIMITS.maxFiles} photos`);
  const out = [];
  let total = 0;
  list.forEach((p, i) => {
    if (!p || typeof p !== 'object') throw err('photos_invalid', `photo ${i} malformed`);
    const type = String(p.type || '').toLowerCase();
    const ext = ALLOWED_TYPES[type];
    if (!ext) throw err('photo_type', `photo ${i}: type ${type || '(none)'} not allowed`);
    const b64 = String(p.data || '').replace(/^data:[^,]*,/, '');
    if (!/^[A-Za-z0-9+/=\s]+$/.test(b64)) throw err('photos_invalid', `photo ${i}: not base64`);
    const bytes = Buffer.from(b64, 'base64');
    if (!bytes.length) throw err('photos_invalid', `photo ${i}: empty`);
    if (!sniffMatches(bytes, type)) throw err('photo_type', `photo ${i}: content is not ${type}`);
    if (bytes.length > LIMITS.maxFileBytes) throw err('photo_too_large', `photo ${i} exceeds ${LIMITS.maxFileBytes} bytes`);
    total += bytes.length;
    if (total > LIMITS.maxTotalBytes) throw err('photos_too_large', `photos exceed ${LIMITS.maxTotalBytes} bytes total`);
    out.push({ type, bytes, filename: sanitiseFilename(p.name, ext, i) });
  });
  return out;
}

// Magic bytes — the declared type is user-controlled.
function sniffMatches(b, type) {
  if (type === 'image/jpeg') return b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff;
  if (type === 'image/png') return b[0] === 0x89 && b[1] === 0x50 && b[2] === 0x4e && b[3] === 0x47;
  if (type === 'image/gif') return b[0] === 0x47 && b[1] === 0x49 && b[2] === 0x46 && b[3] === 0x38;
  return false;
}

function sanitiseFilename(name, ext, i) {
  let base = String(name || '').split(/[\\/]/).pop().replace(/\.[^.]*$/, '');
  base = base.replace(/[^A-Za-z0-9._-]+/g, '-').replace(/^[-.]+|[-.]+$/g, '').slice(0, 60);
  if (!base) base = 'photo-' + (i + 1);
  return `${base}.${ext}`;
}

// 0412 345 678 / (04) 1234 5678 / 61412345678 / +61 412 345 678 -> +61412345678
function normaliseAuPhone(raw) {
  const digits = String(raw).replace(/\D/g, '');
  if (!digits) return null;
  let n;
  if (digits.startsWith('61') && digits.length >= 11) n = digits.slice(2);
  else if (digits.startsWith('0') && digits.length === 10) n = digits.slice(1);
  else if (digits.length === 9) n = digits;
  else if (digits.length === 10 && /^1[38]00/.test(digits)) n = digits;      // 1300 / 1800
  else return null;
  if (n.length < 9 || n.length > 10) return null;
  return '+61' + n;
}

function splitName(full) {
  const parts = full.trim().split(/\s+/).filter(Boolean);
  return { firstName: parts.shift() || '', lastName: parts.join(' ') };
}

// ---------------------------------------------------------------------------
// Plumbing
// ---------------------------------------------------------------------------
function readEnv() {
  const locationId = process.env.GHL_LOCATION_ID;
  const token = process.env.GHL_PIT_TOKEN;
  // Optional: a missing or key-shaped value is resolved at upload time, so a
  // photo-field problem can never block the contact itself.
  const photoField = process.env.GHL_JOB_PHOTOS_FIELD_ID || '';
  if (!locationId || !token) {
    console.error('[quote] missing env: ' + ['GHL_LOCATION_ID', 'GHL_PIT_TOKEN']
      .filter(k => !process.env[k]).join(', '));
    return { error: 'server_misconfigured' };
  }
  return { locationId, token, photoField };
}

// JSON from the site script (with base64 photos), or urlencoded from the
// no-JS fallback. Vercel pre-parses req.body for both; a raw stream is also
// handled so the handler runs unchanged under the local test.
async function readBody(req) {
  const ct = String(req.headers['content-type'] || '').toLowerCase();
  let raw = req.body;
  if (raw === undefined) {
    const chunks = [];
    let size = 0;
    for await (const c of req) {
      size += c.length;
      if (size > LIMITS.maxBodyBytes) throw err('payload_too_large', 'body too large', 413);
      chunks.push(c);
    }
    raw = Buffer.concat(chunks).toString('utf8');
  }
  if (ct.startsWith('application/x-www-form-urlencoded')) {
    const params = typeof raw === 'string' ? new URLSearchParams(raw) : null;
    const obj = params ? Object.fromEntries(params) : (raw || {});
    return Object.assign({ __urlencoded: true }, obj);
  }
  if (typeof raw === 'string') {
    if (raw.length > LIMITS.maxBodyBytes) throw err('payload_too_large', 'body too large', 413);
    try { return JSON.parse(raw); } catch { throw err('bad_json', 'invalid JSON'); }
  }
  return raw && typeof raw === 'object' ? raw : {};
}

function finish(res, isForm, payload) {
  if (isForm) {
    res.statusCode = 303;
    res.setHeader('Location', THANK_YOU);
    return res.end();
  }
  return send(res, 200, payload);
}

function send(res, status, payload) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  return res.end(JSON.stringify(payload));
}

function str(v) { return v == null ? '' : String(v).trim(); }
function err(code, message, status) { const e = new Error(message); e.code = code; e.status = status; return e; }

// Exposed for tests.
module.exports.normaliseAuPhone = normaliseAuPhone;
module.exports.FIELDS = FIELDS;
module.exports.LIMITS = LIMITS;
module.exports._resetFieldCache = () => { fieldCache = null; lastPhotoError = null; lastUpsertError = null; };
