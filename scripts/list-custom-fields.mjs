#!/usr/bin/env node
// Lists the sub-account's contact custom fields and resolves the Job Photos
// field ID for GHL_JOB_PHOTOS_FIELD_ID.
//
//   GHL_PIT_TOKEN=... GHL_LOCATION_ID=T4thSQ8YoNDiusrGSEhY node scripts/list-custom-fields.mjs
//
// Also prints which twin each of the duplicated keys (service_needed,
// property_size, property_address) resolves to, so api/quote.js can be bound
// to an { id } instead of a { key } where the key is ambiguous.

const BASE = 'https://services.leadconnectorhq.com';
const VERSION = '2021-07-28';

const token = process.env.GHL_PIT_TOKEN;
const locationId = process.env.GHL_LOCATION_ID;
if (!token || !locationId) {
  console.error('Set GHL_PIT_TOKEN and GHL_LOCATION_ID.');
  process.exit(2);
}

const WANT = ['full_name', 'email', 'phone', 'property_address', 'property_size',
  'service_needed', 'job_type', 'job_notes', 'job_photos'];

const res = await fetch(`${BASE}/locations/${locationId}/customFields`, {
  headers: { Authorization: `Bearer ${token}`, Version: VERSION, Accept: 'application/json' },
});
const text = await res.text();
if (!res.ok) {
  console.error(`GET /locations/${locationId}/customFields -> ${res.status}\n${text}`);
  process.exit(1);
}

let json;
try { json = JSON.parse(text); } catch { console.error('Non-JSON response:\n' + text); process.exit(1); }

// The response shape is not part of the verified contract, so find the first
// array of field-shaped objects rather than assume a property name.
function findFields(node, depth = 0) {
  if (depth > 4 || !node || typeof node !== 'object') return null;
  if (Array.isArray(node)) {
    return node.length && node.every(x => x && typeof x === 'object' && 'id' in x && ('fieldKey' in x || 'key' in x))
      ? node : null;
  }
  for (const v of Object.values(node)) { const f = findFields(v, depth + 1); if (f) return f; }
  return null;
}
const fields = findFields(json);
if (!fields) {
  console.error('Could not locate a custom-field array in the response. Raw JSON follows so the shape can be read off:\n');
  console.log(JSON.stringify(json, null, 2));
  process.exit(1);
}

const keyOf = f => String(f.fieldKey ?? f.key ?? '').replace(/^contact\./, '');
const typeOf = f => f.dataType ?? f.type ?? '';
const rows = fields.map(f => ({ id: f.id, name: f.name ?? '', key: keyOf(f), type: typeOf(f) }));

const pad = (s, n) => String(s).padEnd(n);
const w = { id: Math.max(2, ...rows.map(r => r.id.length)), name: Math.max(4, ...rows.map(r => r.name.length)), key: Math.max(3, ...rows.map(r => r.key.length)) };
console.log(`${pad('ID', w.id)}  ${pad('NAME', w.name)}  ${pad('KEY', w.key)}  TYPE`);
for (const r of rows) console.log(`${pad(r.id, w.id)}  ${pad(r.name, w.name)}  ${pad(r.key, w.key)}  ${r.type}`);

// Duplicate names — the sub-account is known to have twins.
const byName = new Map();
for (const r of rows) byName.set(r.name, [...(byName.get(r.name) ?? []), r]);
const dupes = [...byName.entries()].filter(([, v]) => v.length > 1);
if (dupes.length) {
  console.log('\nDUPLICATE NAMES:');
  for (const [name, list] of dupes) {
    console.log(`  "${name}"`);
    for (const r of list) console.log(`    id=${r.id}  key=${r.key}  type=${r.type}`);
  }
}

// Which twin does each key actually resolve to (what a { key } binding in the
// upsert will hit), and is any key duplicated outright?
console.log('\nKEY RESOLUTION:');
for (const k of WANT) {
  const hits = rows.filter(r => r.key === k);
  if (!hits.length) console.log(`  ${pad(k, 17)} NOT FOUND — tell the developer, do not guess a variant`);
  else if (hits.length > 1) console.log(`  ${pad(k, 17)} AMBIGUOUS x${hits.length}: ${hits.map(h => h.id).join(', ')} — bind by { id } in api/quote.js`);
  else console.log(`  ${pad(k, 17)} -> id=${hits[0].id}  name="${hits[0].name}"  type=${hits[0].type}`);
}

const photos = rows.filter(r => r.key === 'job_photos');
console.log('');
if (photos.length === 1) {
  console.log(`GHL_JOB_PHOTOS_FIELD_ID=${photos[0].id}`);
  if (!/file/i.test(photos[0].type)) console.log(`  WARNING: type is "${photos[0].type}", expected a file-upload type`);
} else {
  console.log(photos.length ? `job_photos is ambiguous (${photos.length} fields) — pick by id above.` : 'job_photos key not found.');
  process.exit(1);
}
