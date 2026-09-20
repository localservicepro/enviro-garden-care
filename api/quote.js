'use strict';
// Vercel serverless function: quote form -> GoHighLevel.
//
//   1. Upsert the contact  (POST /contacts/upsert, custom fields by key or id)
//   2. Upload photos       (POST /forms/upload-custom-files, multipart, parts
//                           keyed "<fieldId>_<uuid>")
//
// The contact is always written first. A photo failure never loses the lead:
// the response is still ok:true with a photoError flag.
//
// Env (Vercel project settings, server-side only):
//   GHL_LOCATION_ID, GHL_PIT_TOKEN, GHL_JOB_PHOTOS_FIELD_ID
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
  // photos: uploaded to the file field whose ID is GHL_JOB_PHOTOS_FIELD_ID
  //         (key contact.job_photos — the upload endpoint needs the ID).
};

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
    customFields: buildCustomFields(body),
  };

  let contactId;
  try {
    const r = await ghlJson('POST', '/contacts/upsert', env.token, contact);
    contactId = r && r.contact && r.contact.id;
    if (!contactId) throw new Error('upsert returned no contact id');
  } catch (e) {
    console.error('[quote] upsert failed:', e.message);
    return send(res, 502, { ok: false, error: 'upsert_failed' });
  }

  // --- 2. upload photos (never fatal) -------------------------------------
  const out = { ok: true, contactId, photos: { received: photos.length, uploaded: 0 } };
  if (photos.length) {
    try {
      await uploadPhotos(env, contactId, photos);
      out.photos.uploaded = photos.length;
    } catch (e) {
      console.error('[quote] photo upload failed for', contactId, ':', e.message);
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
  if (!r.ok) throw new Error(`${method} ${path} -> ${r.status} ${text.slice(0, 300)}`);
  try { return JSON.parse(text); } catch { throw new Error(`${path} returned non-JSON`); }
}

async function uploadPhotos(env, contactId, photos) {
  const fd = new FormData();
  for (const p of photos) {
    // One part per file. Key = "<customFieldId>_<uuid>"; all parts sharing the
    // field id land in the same custom field.
    const part = env.photoFieldId + '_' + crypto.randomUUID();
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
}

// ---------------------------------------------------------------------------
// Mapping + validation
// ---------------------------------------------------------------------------
function buildCustomFields(body) {
  const out = [];
  for (const [name, map] of Object.entries(FIELDS)) {
    if (!map.key && !map.id) continue;
    const value = str(body[name]);
    if (!value) continue;
    out.push(map.id ? { id: map.id, value } : { key: map.key, value });
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
  const photoFieldId = process.env.GHL_JOB_PHOTOS_FIELD_ID;
  if (!locationId || !token || !photoFieldId) {
    console.error('[quote] missing env: ' + ['GHL_LOCATION_ID', 'GHL_PIT_TOKEN', 'GHL_JOB_PHOTOS_FIELD_ID']
      .filter(k => !process.env[k]).join(', '));
    return { error: 'server_misconfigured' };
  }
  return { locationId, token, photoFieldId };
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
