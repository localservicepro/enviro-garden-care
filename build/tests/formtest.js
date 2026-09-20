// Browser-level form suite (Playwright + bundled Chromium). Serves the built
// site from 127.0.0.1:8123 and mocks /api/quote so nothing reaches GHL.
//   python3 -m http.server 8123 &  node build/tests/formtest.js
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const results = [];
  const T = (label, ok, extra='') => results.push(`${ok?'PASS':'FAIL'}  ${label}${extra?' — '+extra:''}`);
  const PNG = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==','base64');

  // Mock the serverless function. Records every JSON body it receives.
  const posted = [];
  async function mockApi(page, { status = 200, body = { ok: true, contactId: 'c_1', photos: { received: 0, uploaded: 0 } } } = {}) {
    await page.route('**/api/quote', async r => {
      const req = r.request();
      posted.push({ method: req.method(), headers: req.headers(), json: (() => { try { return req.postDataJSON(); } catch { return null; } })() });
      r.fulfill({ status, contentType: 'application/json', body: JSON.stringify(body) });
    });
  }
  const fillContact = async (p) => {
    await p.fill('#contact-quote-full_name','Sam Tester');
    await p.fill('#contact-quote-email','Sam@Example.com');
    await p.fill('#contact-quote-phone','0407 276 574');
    await p.fill('#contact-quote-property_address','9 Cullen St, Pimpama');
    await p.selectOption('#contact-quote-service_needed',{index:1});
    await p.selectOption('#contact-quote-job_type',{index:1});
  };

  // ---- 1. Field mapping + action on every form ----------------------------
  const expected = ['full_name','email','phone','property_address','property_size','service_needed','job_type','job_notes'];
  const merge = {full_name:'{{contact.full_name}}',email:'{{contact.email}}',phone:'{{contact.phone}}',
    property_address:'{{contact.property_address}}',property_size:'{{contact.property_size}}',
    service_needed:'{{contact.service_needed}}',job_type:'{{contact.job_type}}',job_notes:'{{contact.job_notes}}',
    property_photos:'{{contact.job_photos}}'};
  for (const url of ['/','/contact/','/services/lawn-mowing/']) {
    const p = await b.newPage();
    await p.goto('http://127.0.0.1:8123'+url,{waitUntil:'domcontentloaded'});
    const forms = await p.$$eval('.quote__form', fs => fs.map(f => ({
      id: f.id, action: f.getAttribute('action'), method: (f.getAttribute('method')||'').toLowerCase(),
      fields: [...f.querySelectorAll('[name]')].filter(c=>!['company_website','_t'].includes(c.name))
        .map(c=>({name:c.name, ghl:c.dataset.ghl, tag:c.tagName.toLowerCase()}))
    })));
    for (const f of forms) {
      const names = f.fields.map(x=>x.name);
      T(`${url} #${f.id} has all 8 GHL text fields`, expected.every(e=>names.includes(e)), names.join(','));
      T(`${url} #${f.id} merge tags correct`, f.fields.every(x=>merge[x.name]===x.ghl));
      T(`${url} #${f.id} posts to /api/quote`, f.action === '/api/quote' && f.method === 'post', `${f.method} ${f.action}`);
      T(`${url} #${f.id} photo field present and visible`, names.includes('property_photos'));
    }
    const fileDisplay = await p.$eval('.quote__form .field--file', e => getComputedStyle(e).display).catch(()=>'missing');
    T(`${url} photo field is rendered (computed display)`, fileDisplay !== 'none' && fileDisplay !== 'missing', fileDisplay);
    await p.close();
  }

  // ---- 2. Validation blocks an empty submit ------------------------------
  let p = await b.newPage();
  await mockApi(p);
  await p.goto('http://127.0.0.1:8123/contact/',{waitUntil:'networkidle'});
  const before = p.url();
  await p.click('#contact-quote button[type=submit]');
  await p.waitForTimeout(500);
  T('empty submit is blocked', p.url() === before, p.url());
  const invalid = await p.$$eval('[aria-invalid="true"]', e=>e.length);
  T('all 6 required fields flagged invalid', invalid === 6, `${invalid} flagged`);
  T('nothing was POSTed for an invalid form', posted.length === 0);

  // ---- 3. Bad email is rejected -----------------------------------------
  await fillContact(p);
  await p.fill('#contact-quote-email','not-an-email');
  await p.click('#contact-quote button[type=submit]');
  await p.waitForTimeout(400);
  T('invalid email rejected client-side', p.url() === before && posted.length === 0);

  // ---- 4. Valid submit → JSON POST → redirect ----------------------------
  await p.fill('#contact-quote-email','Sam@Example.com');
  await p.fill('#contact-quote-job_notes','Big dog, side gate unlocked.');
  await p.click('#contact-quote button[type=submit]');
  await p.waitForURL('**/thank-you/',{timeout:8000}).catch(()=>{});
  T('valid submit redirects to /thank-you/', /\/thank-you\/$/.test(p.url()), p.url());
  T('exactly one POST to /api/quote', posted.length === 1 && posted[0].method === 'POST', `${posted.length} requests`);
  const j = posted[0] && posted[0].json;
  T('body is JSON', !!j && /application\/json/.test(posted[0].headers['content-type']||''));
  T('body carries every text field', j && expected.every(k => k in j), j ? Object.keys(j).join(',') : '');
  T('phone sent raw for server-side E.164 normalisation', j && j.phone === '0407 276 574', j && j.phone);
  T('email sent as typed (server lowercases)', j && j.email === 'Sam@Example.com');
  T('job_type carries the once-off / regular choice (CD r83)', j && /One-off/.test(j.job_type), j && j.job_type);
  T('minimum-fill timestamp _t is sent', j && typeof j._t === 'number' && Date.now() - j._t < 60000);
  T('honeypot field is not in the JSON', j && !('company_website' in j));
  T('no photos → empty photos array', j && Array.isArray(j.photos) && j.photos.length === 0);
  const h1 = await p.$eval('h1', e=>e.textContent.trim()).catch(()=>'');
  T('thank-you page renders', /Thanks/i.test(h1), h1);
  T('no field values leaked into the URL', !/full_name|email=/.test(p.url()), p.url());
  await p.close();

  // ---- 5. Tracking script still sees the submit; redirect waits ----------
  posted.length = 0;
  p = await b.newPage();
  await mockApi(p);
  // Stand in for link.msgsndr.com (blocked here): document-level submit listener like the GHL tracker.
  await p.addInitScript(() => {
    window.__captured = null;
    document.addEventListener('submit', (ev) => {
      const d = {}; [...ev.target.querySelectorAll('[name]')].forEach(c => { d[c.name] = c.value; });
      window.__captured = d;
    });
  });
  await p.goto('http://127.0.0.1:8123/contact/',{waitUntil:'networkidle'});
  const tracker = await p.$$eval('script[src*="external-tracking.js"]', s => s.map(x => x.dataset.trackingId));
  T('GHL tracking script tag present once', tracker.length === 1 && tracker[0] === 'tk_5bee5316dafc4ac09c8e0e20ec24e0e4', JSON.stringify(tracker));
  await fillContact(p);
  await p.click('#contact-quote button[type=submit]');
  const cap = await p.evaluate(() => window.__captured);
  T('tracking-style listener received the submit', !!cap, cap ? Object.keys(cap).filter(k=>!['company_website','_t'].includes(k)).join(',') : 'nothing captured');
  T('captured values are the real field values', cap && cap.full_name === 'Sam Tester' && cap.phone === '0407 276 574');
  const stillHere = !/thank-you/.test(p.url());
  T('redirect is deferred, not immediate', stillHere);
  await p.waitForURL('**/thank-you/',{timeout:8000}).catch(()=>{});
  T('redirect still happens after API + grace', /\/thank-you\/$/.test(p.url()), p.url());
  await p.close();

  // ---- 6. Honeypot: no tracker, no API, still thank-you ------------------
  posted.length = 0;
  p = await b.newPage();
  await mockApi(p);
  await p.addInitScript(() => { window.__captured = null; document.addEventListener('submit', () => { window.__captured = 'yes'; }); });
  await p.goto('http://127.0.0.1:8123/contact/',{waitUntil:'networkidle'});
  const hp = await p.$eval('#contact-quote [name=company_website]', e=>({
    off: e.getBoundingClientRect().left < 0, tab: e.tabIndex, display: getComputedStyle(e).display }));
  T('honeypot is off-screen, untabbable, not display:none', hp.off && hp.tab === -1 && hp.display !== 'none', JSON.stringify(hp));
  await fillContact(p);
  await p.evaluate(() => { document.querySelector('#contact-quote [name=company_website]').value = 'http://spam.example'; });
  await p.click('#contact-quote button[type=submit]');
  await p.waitForURL('**/thank-you/',{timeout:5000}).catch(()=>{});
  T('honeypot submission is NOT passed to the tracker', (await p.evaluate(() => window.__captured)) === null);
  T('honeypot submission never calls /api/quote', posted.length === 0, `${posted.length} requests`);
  T('honeypot submission still lands on thank-you (fails silently)', /\/thank-you\/$/.test(p.url()), p.url());
  await p.close();

  // ---- 7. Photos: thumbnails, rejection, resize to JPEG, base64 in JSON --
  posted.length = 0;
  p = await b.newPage();
  await mockApi(p, { body: { ok: true, contactId: 'c_1', photos: { received: 2, uploaded: 2 } } });
  await p.goto('http://127.0.0.1:8123/contact/',{waitUntil:'networkidle'});
  await p.setInputFiles('#contact-quote-property_photos', [{name:'front.png', mimeType:'image/png', buffer:PNG},{name:'back yard.png', mimeType:'image/png', buffer:PNG}]);
  await p.waitForFunction(() => document.querySelectorAll('#contact-quote .field__thumbs img').length === 2, null, { timeout: 5000 }).catch(()=>{});
  T('thumbnails render for attached photos', (await p.$$eval('#contact-quote .field__thumbs img', e=>e.length)) === 2);
  await p.setInputFiles('#contact-quote-property_photos', [{name:'notes.txt', mimeType:'text/plain', buffer:Buffer.from('x')}]);
  await p.waitForTimeout(300);
  const rejected = await p.$eval('#contact-quote .field--file', e => (e.querySelector('.field__msg')||{}).textContent || '');
  T('non-image attachment is rejected client-side', /Photos only/.test(rejected), rejected);
  const seven = Array.from({length:7}, (_,i)=>({name:`p${i}.png`, mimeType:'image/png', buffer:PNG}));
  await p.setInputFiles('#contact-quote-property_photos', seven);
  await p.waitForTimeout(300);
  const tooMany = await p.$eval('#contact-quote .field--file', e => (e.querySelector('.field__msg')||{}).textContent || '');
  T('more than 6 photos rejected client-side', /up to 6/.test(tooMany), tooMany);
  await p.setInputFiles('#contact-quote-property_photos', [{name:'front.png', mimeType:'image/png', buffer:PNG},{name:'back yard.png', mimeType:'image/png', buffer:PNG}]);
  await p.waitForFunction(() => document.querySelectorAll('#contact-quote .field__thumbs img').length === 2, null, { timeout: 5000 }).catch(()=>{});
  await fillContact(p);
  await p.click('#contact-quote button[type=submit]');
  await p.waitForURL('**/thank-you/',{timeout:8000}).catch(()=>{});
  const pj = posted[0] && posted[0].json;
  T('photos submit POSTed once and redirected', posted.length === 1 && /\/thank-you\/$/.test(p.url()), p.url());
  T('2 photos in JSON body', pj && Array.isArray(pj.photos) && pj.photos.length === 2, pj && pj.photos && pj.photos.length);
  const ph = pj && pj.photos && pj.photos[0];
  T('photo re-encoded to JPEG data URL (HEIC/PNG → JPEG)', ph && ph.type === 'image/jpeg' && /^data:image\/jpeg;base64,[A-Za-z0-9+/=]+$/.test(ph.data), ph && (ph.data||'').slice(0,40));
  T('photo filename carried (server sanitises)', ph && ph.name === 'front.png', ph && ph.name);
  const bytes = ph ? Buffer.from(ph.data.split(',')[1], 'base64') : Buffer.alloc(0);
  T('JPEG magic bytes present', bytes[0] === 0xFF && bytes[1] === 0xD8, bytes.slice(0,2).toString('hex'));
  await p.close();

  // ---- 8. Server errors surface, no redirect -----------------------------
  posted.length = 0;
  p = await b.newPage();
  await mockApi(p, { status: 400, body: { ok: false, error: 'phone_required' } });
  await p.goto('http://127.0.0.1:8123/contact/',{waitUntil:'networkidle'});
  await fillContact(p);
  await p.click('#contact-quote button[type=submit]');
  await p.waitForTimeout(1500);
  const err400 = await p.$eval('#contact-quote .quote__error', e => ({ hidden: e.hidden, text: e.textContent }));
  T('400 keeps the visitor on the page with a phone hint', !/thank-you/.test(p.url()) && !err400.hidden && /phone/i.test(err400.text), err400.text);
  const reenabled = await p.$eval('#contact-quote', f => !f.classList.contains('is-sending'));
  T('form re-enabled after an error', reenabled);
  await p.close();

  p = await b.newPage();
  await mockApi(p, { status: 500, body: { ok: false, error: 'server_misconfigured' } });
  await p.goto('http://127.0.0.1:8123/contact/',{waitUntil:'networkidle'});
  await fillContact(p);
  await p.click('#contact-quote button[type=submit]');
  await p.waitForTimeout(1500);
  const err500 = await p.$eval('#contact-quote .quote__error', e => ({ hidden: e.hidden, text: e.textContent }));
  T('500 shows a generic message with the phone number', !/thank-you/.test(p.url()) && !err500.hidden && /0407 276 574/.test(err500.text), err500.text);
  await p.close();

  // ---- 9. photoError is still a success -----------------------------------
  p = await b.newPage();
  await mockApi(p, { body: { ok: true, contactId: 'c_1', photoError: true, photos: { received: 1, uploaded: 0 } } });
  await p.goto('http://127.0.0.1:8123/contact/',{waitUntil:'networkidle'});
  await fillContact(p);
  await p.click('#contact-quote button[type=submit]');
  await p.waitForURL('**/thank-you/',{timeout:8000}).catch(()=>{});
  T('ok:true with photoError still redirects (lead never lost)', /\/thank-you\/$/.test(p.url()), p.url());
  await p.close();

  await b.close();
  console.log(results.join('\n'));
  const fails = results.filter(r=>r.startsWith('FAIL')).length;
  console.log(`\n${fails} failure(s)`);
  process.exit(fails ? 1 : 0);
})();
