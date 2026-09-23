'use strict';
// Local test for api/quote.js. Mocks global fetch; no network, no deps.
//   node --test build/tests/quote.test.js

const test = require('node:test');
const assert = require('node:assert/strict');
const { Readable } = require('node:stream');
const path = require('node:path');

const LOCATION = 'T4thSQ8YoNDiusrGSEhY';
const FIELD_ID = 'aBc123FieldId';
process.env.GHL_LOCATION_ID = LOCATION;
process.env.GHL_PIT_TOKEN = 'pit-test-token';
process.env.GHL_JOB_PHOTOS_FIELD_ID = FIELD_ID;

const handler = require(path.join(__dirname, '..', '..', 'api', 'quote.js'));

// 1x1 valid images (magic bytes are checked server-side).
const JPEG = Buffer.from('/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wAALCAABAAEBAREA/8QAFAABAAAAAAAAAAAAAAAAAAAACf/EABQQAQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEAAD8AN//Z', 'base64');
const PNG = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==', 'base64');

function req(body, { method = 'POST', headers = {} } = {}) {
  const raw = typeof body === 'string' ? body : JSON.stringify(body);
  const r = Readable.from([Buffer.from(raw)]);
  r.method = method;
  r.headers = Object.assign({ 'content-type': 'application/json' }, headers);
  return r;
}

function res() {
  const r = { statusCode: 200, headers: {}, body: '' };
  r.setHeader = (k, v) => { r.headers[k.toLowerCase()] = v; };
  r.end = (s) => { r.body = s || ''; r.ended = true; };
  r.json = () => JSON.parse(r.body);
  return r;
}

// Captures every fetch call. Defaults to a healthy GHL.
function mockFetch(overrides = {}) {
  const calls = [];
  global.fetch = async (url, init = {}) => {
    calls.push({ url: String(url), init });
    const u = String(url);
    if (u.endsWith('/contacts/upsert')) {
      if (overrides.upsert) return overrides.upsert(url, init);
      return new Response(JSON.stringify({ contact: { id: 'contact_123' } }), { status: 200 });
    }
    if (u.includes('/forms/upload-custom-files')) {
      if (overrides.upload) return overrides.upload(url, init);
      return new Response(JSON.stringify({ ok: true }), { status: 200 });
    }
    throw new Error('unexpected fetch ' + u);
  };
  return calls;
}

const good = () => ({
  full_name: 'Jane Citizen',
  email: 'Jane.Citizen@Example.COM',
  phone: '0412 345 678',
  property_address: '12 Example St, Ormeau',
  property_size: 'Half to 1 acre',
  service_needed: 'Acreage / ride-on mowing',
  job_type: 'Regular maintenance (fortnightly / three-weekly)',
  job_notes: 'Hedges too.',
  _t: Date.now() - 10000,
  photos: [
    { name: 'front yard.jpg', type: 'image/jpeg', data: 'data:image/jpeg;base64,' + JPEG.toString('base64') },
    { name: '../../etc/passwd.png', type: 'image/png', data: PNG.toString('base64') },
  ],
});

test('phone normalised to E.164, email lowercased, every custom field mapped', async () => {
  const calls = mockFetch();
  const r = res();
  await handler(req(good()), r);
  assert.equal(r.statusCode, 200, r.body);
  assert.equal(r.json().ok, true);

  const upsert = calls.find(c => c.url.endsWith('/contacts/upsert'));
  assert.ok(upsert, 'upsert called');
  const body = JSON.parse(upsert.init.body);
  assert.equal(body.phone, '+61412345678');
  assert.equal(body.email, 'jane.citizen@example.com');
  assert.equal(body.firstName, 'Jane');
  assert.equal(body.lastName, 'Citizen');
  assert.equal(body.locationId, LOCATION);
  assert.equal(body.address1, '12 Example St, Ormeau');
  assert.equal(upsert.init.headers.Version, '2021-07-28');
  assert.equal(upsert.init.headers.Authorization, 'Bearer pit-test-token');

  const cf = Object.fromEntries(body.customFields.map(f => [f.key || f.id, f.value]));
  assert.deepEqual(cf, {
    property_address: '12 Example St, Ormeau',
    property_size: 'Half to 1 acre',
    service_needed: 'Acreage / ride-on mowing',
    job_type: 'Regular maintenance (fortnightly / three-weekly)',
    job_notes: 'Hedges too.',
  });
});

test('photos: every part prefixed with the field ID, unique uuids, locationId in query, contact first', async () => {
  const calls = mockFetch();
  const r = res();
  await handler(req(good()), r);
  assert.equal(r.json().photos.uploaded, 2);

  assert.ok(calls[0].url.endsWith('/contacts/upsert'), 'upsert happens before upload');
  const up = calls[1];
  const u = new URL(up.url);
  assert.equal(u.pathname, '/forms/upload-custom-files');
  assert.equal(u.searchParams.get('locationId'), LOCATION);
  assert.equal(u.searchParams.get('contactId'), 'contact_123');
  assert.equal(up.init.headers.Version, '2021-07-28');
  assert.equal(up.init.headers['Content-Type'], undefined, 'multipart boundary must be set by fetch, not by hand');

  const fd = up.init.body;
  assert.ok(fd instanceof FormData);
  const keys = [...fd.keys()];
  assert.equal(keys.length, 2);
  const uuidRe = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  for (const k of keys) {
    assert.ok(k.startsWith(FIELD_ID + '_'), 'part keyed by field ID: ' + k);
    assert.match(k.slice(FIELD_ID.length + 1), uuidRe);
  }
  assert.equal(new Set(keys).size, keys.length, 'uuids unique');

  const files = [...fd.values()];
  assert.equal(files[0].type, 'image/jpeg');
  assert.equal(files[0].name, 'front-yard.jpg');
  assert.equal(files[1].name, 'passwd.png', 'path components stripped from filename');
  assert.equal(files[0].size, JPEG.length);
});

test('non-image file rejected with 400 and GHL never called', async () => {
  const calls = mockFetch();
  const body = good();
  body.photos = [{ name: 'notes.txt', type: 'text/plain', data: Buffer.from('hello').toString('base64') }];
  const r = res();
  await handler(req(body), r);
  assert.equal(r.statusCode, 400);
  assert.equal(r.json().error, 'photo_type');
  assert.equal(calls.length, 0);
});

test('declared image type with non-image bytes rejected', async () => {
  const calls = mockFetch();
  const body = good();
  body.photos = [{ name: 'x.jpg', type: 'image/jpeg', data: Buffer.from('not a jpeg at all').toString('base64') }];
  const r = res();
  await handler(req(body), r);
  assert.equal(r.statusCode, 400);
  assert.equal(calls.length, 0);
});

test('honeypot short-circuits: ok:true, no GHL call', async () => {
  const calls = mockFetch();
  const body = good();
  body.company_website = 'http://spam.example';
  const r = res();
  await handler(req(body), r);
  assert.equal(r.statusCode, 200);
  assert.equal(r.json().ok, true);
  assert.equal(calls.length, 0);
});

test('submitted faster than the minimum fill time short-circuits', async () => {
  const calls = mockFetch();
  const body = good();
  body._t = Date.now() - 300;
  const r = res();
  await handler(req(body), r);
  assert.equal(r.json().ok, true);
  assert.equal(r.json().skipped, 'too_fast');
  assert.equal(calls.length, 0);
});

test('missing phone returns 400', async () => {
  const calls = mockFetch();
  const body = good();
  body.phone = '';
  const r = res();
  await handler(req(body), r);
  assert.equal(r.statusCode, 400);
  assert.equal(r.json().error, 'phone_required');
  assert.equal(calls.length, 0);
});

test('photo upload failure still returns ok:true with photoError', async () => {
  mockFetch({ upload: () => new Response('boom', { status: 500 }) });
  const r = res();
  await handler(req(good()), r);
  assert.equal(r.statusCode, 200);
  const j = r.json();
  assert.equal(j.ok, true);
  assert.equal(j.photoError, true);
  assert.equal(j.contactId, 'contact_123');
});

test('upsert failure returns 502 and does not attempt upload', async () => {
  const calls = mockFetch({ upsert: () => new Response('nope', { status: 401 }) });
  const r = res();
  await handler(req(good()), r);
  assert.equal(r.statusCode, 502);
  assert.equal(calls.length, 1);
});

test('too many photos rejected', async () => {
  mockFetch();
  const body = good();
  body.photos = Array.from({ length: 7 }, (_, i) => ({ name: `p${i}.png`, type: 'image/png', data: PNG.toString('base64') }));
  const r = res();
  await handler(req(body), r);
  assert.equal(r.statusCode, 400);
  assert.equal(r.json().error, 'too_many_photos');
});

test('no-JS urlencoded fallback upserts and redirects 303 to /thank-you/', async () => {
  const calls = mockFetch();
  const form = new URLSearchParams({ full_name: 'Sam Test', phone: '(04) 1234 5678', email: 'SAM@EXAMPLE.COM', service_needed: 'Lawn mowing', job_type: 'One-off job' });
  const r = res();
  await handler(req(form.toString(), { headers: { 'content-type': 'application/x-www-form-urlencoded' } }), r);
  assert.equal(r.statusCode, 303);
  assert.equal(r.headers.location, '/thank-you/');
  const body = JSON.parse(calls[0].init.body);
  assert.equal(body.phone, '+61412345678');
  assert.equal(body.email, 'sam@example.com');
  assert.equal(calls.length, 1, 'no photo upload for the fallback');
});

test('GET is 405; missing env is 500 without calling GHL', async () => {
  const calls = mockFetch();
  let r = res();
  await handler(req({}, { method: 'GET' }), r);
  assert.equal(r.statusCode, 405);

  const saved = process.env.GHL_PIT_TOKEN;
  delete process.env.GHL_PIT_TOKEN;
  r = res();
  await handler(req(good()), r);
  assert.equal(r.statusCode, 500);
  assert.equal(r.json().error, 'server_misconfigured');
  process.env.GHL_PIT_TOKEN = saved;
  assert.equal(calls.length, 0);
});

test('phone normalisation table', () => {
  const n = handler.normaliseAuPhone;
  assert.equal(n('0412 345 678'), '+61412345678');
  assert.equal(n('+61 412 345 678'), '+61412345678');
  assert.equal(n('61412345678'), '+61412345678');
  assert.equal(n('412345678'), '+61412345678');
  assert.equal(n('(07) 5555 1234'), '+61755551234');
  assert.equal(n('1300 123 456'), '+611300123456');
  assert.equal(n('12345'), null);
  assert.equal(n(''), null);
});
