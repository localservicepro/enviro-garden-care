/* Quote form: GHL field mapping, validation, capture and the thank-you redirect.
   See README.md in this folder. */
const { chromium } = require('playwright');

const BASE = process.env.BASE || 'http://127.0.0.1:8123';
const CHROME = process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const FORM = '#quote-contact';

(async () => {
  const b = await chromium.launch({ executablePath: CHROME });
  const results = [];
  const T = (label, ok, extra = '') =>
    results.push(`${ok ? 'PASS' : 'FAIL'}  ${label}${extra ? ' — ' + extra : ''}`);

  const expected = ['full_name', 'email', 'phone', 'property_address',
                    'property_size', 'service_needed', 'job_notes'];
  const merge = {
    full_name: '{{contact.full_name}}', email: '{{contact.email}}',
    phone: '{{contact.phone}}', property_address: '{{contact.property_address}}',
    property_size: '{{contact.property_size}}', service_needed: '{{contact.service_needed}}',
    job_notes: '{{contact.job_notes}}',
  };

  // ---- 1. Field mapping on every page that carries a form ----------------
  for (const url of ['/', '/contact/', '/services/lawn-mowing/']) {
    const p = await b.newPage();
    await p.goto(BASE + url, { waitUntil: 'domcontentloaded' });
    const forms = await p.$$eval('.quote__form', fs => fs.map(f => ({
      id: f.id,
      action: f.getAttribute('action'),
      fields: [...f.querySelectorAll('[name]')].filter(c => c.name !== 'company_website')
        .map(c => ({ name: c.name, ghl: c.dataset.ghl })),
    })));
    T(`${url} has a quote form`, forms.length > 0);
    for (const f of forms) {
      const names = f.fields.map(x => x.name);
      T(`${url} #${f.id} has all 7 GHL fields`, expected.every(e => names.includes(e)), names.join(','));
      T(`${url} #${f.id} merge tags correct`, f.fields.every(x => merge[x.name] === x.ghl));
      T(`${url} #${f.id} action -> /thank-you/`, f.action === '/thank-you/', f.action);
    }
    // the tracking script must be installed once, globally
    const trackers = await p.$$eval('script[src*="external-tracking.js"]',
      s => s.map(x => x.dataset.trackingId));
    T(`${url} tracking script installed exactly once`, trackers.length === 1, trackers.join(','));
    T(`${url} tracking id set`, trackers[0] === 'tk_6582cb70c3d84289821c555a3d8691f9', trackers[0]);
    await p.close();
  }

  // ---- 2. Validation blocks an empty submit ------------------------------
  let p = await b.newPage();
  await p.goto(BASE + '/contact/', { waitUntil: 'domcontentloaded' });
  const before = p.url();
  await p.click(`${FORM} button[type=submit]`);
  await p.waitForTimeout(400);
  T('empty submit is blocked', p.url() === before, p.url());
  const invalid = await p.$$eval('[aria-invalid="true"]', e => e.length);
  T('all 5 required fields flagged invalid', invalid === 5, `${invalid} flagged`);

  // ---- 3. Bad email is rejected -----------------------------------------
  await p.fill('#quote-contact-full_name', 'Test User');
  await p.fill('#quote-contact-email', 'not-an-email');
  await p.fill('#quote-contact-phone', '0456198080');
  await p.fill('#quote-contact-property_address', '12 Example St, Sunnybank');
  await p.selectOption('#quote-contact-service_needed', { index: 1 });
  await p.click(`${FORM} button[type=submit]`);
  await p.waitForTimeout(300);
  T('invalid email rejected', p.url() === before);

  // ---- 4. Valid submit redirects to the thank-you page -------------------
  await p.fill('#quote-contact-email', 'test@example.com');
  await p.fill('#quote-contact-job_notes', 'Big dog, side gate unlocked.');
  await p.click(`${FORM} button[type=submit]`);
  await p.waitForURL('**/thank-you/', { timeout: 8000 }).catch(() => {});
  T('valid submit redirects to /thank-you/', /thank-you\/$/.test(p.url()), p.url());
  const h1 = await p.$eval('h1', e => e.textContent.trim()).catch(() => '');
  T('thank-you page renders', /Thanks/i.test(h1), h1);
  const robots = await p.$eval('meta[name=robots]', e => e.content).catch(() => '');
  T('thank-you is noindex', /noindex/.test(robots), robots);
  T('no field values leaked into the URL', !/full_name|email=/.test(p.url()), p.url());
  await p.close();

  // ---- 5. The tracker sees the submit, and the redirect waits for it -----
  p = await b.newPage();
  // Stand in for link.msgsndr.com: a document-level submit listener, which is
  // how the GHL external-tracking script captures a form.
  await p.addInitScript(() => {
    window.__captured = null;
    document.addEventListener('submit', (ev) => {
      const d = {};
      [...ev.target.querySelectorAll('[name]')].forEach(c => { d[c.name] = c.value; });
      window.__captured = d;
    });
  });
  await p.goto(BASE + '/contact/', { waitUntil: 'domcontentloaded' });
  await p.fill('#quote-contact-full_name', 'Sam Tester');
  await p.fill('#quote-contact-email', 'sam@example.com');
  await p.fill('#quote-contact-phone', '0456 198 080');
  await p.fill('#quote-contact-property_address', '9 Logan Rd, Mount Gravatt');
  await p.selectOption('#quote-contact-property_size', { index: 2 });
  await p.selectOption('#quote-contact-service_needed', { index: 1 });
  await p.click(`${FORM} button[type=submit]`);
  const cap = await p.evaluate(() => window.__captured);
  T('tracking-style listener received the submit', !!cap,
    cap ? Object.keys(cap).filter(k => k !== 'company_website').join(',') : 'nothing captured');
  T('captured values are the real field values',
    !!cap && cap.full_name === 'Sam Tester' && cap.email === 'sam@example.com');
  T('redirect is deferred, not immediate', !/thank-you/.test(p.url()),
    'still on /contact/ right after submit');
  if (cap) console.log('\nExample GHL payload:\n' + JSON.stringify(
    Object.fromEntries(Object.entries(cap).filter(([k]) => k !== 'company_website')), null, 2));
  await p.waitForURL('**/thank-you/', { timeout: 8000 }).catch(() => {});
  T('redirect still happens', /thank-you\/$/.test(p.url()), p.url());
  await p.close();

  // ---- 6. Honeypot -------------------------------------------------------
  p = await b.newPage();
  await p.addInitScript(() => {
    window.__captured = null;
    document.addEventListener('submit', () => { window.__captured = 'yes'; });
  });
  await p.goto(BASE + '/contact/', { waitUntil: 'domcontentloaded' });
  const hp = await p.$eval(`${FORM} [name=company_website]`, e => ({
    off: e.getBoundingClientRect().left < 0, tab: e.tabIndex }));
  T('honeypot is off-screen and untabbable', hp.off && hp.tab === -1, JSON.stringify(hp));
  await p.evaluate(() => {
    const f = document.getElementById('quote-contact');
    f.full_name.value = 'Bot'; f.email.value = 'bot@spam.example'; f.phone.value = '0400000000';
    f.property_address.value = 'x'; f.service_needed.selectedIndex = 1;
    f.querySelector('[name=company_website]').value = 'http://spam.example';
  });
  await p.click(`${FORM} button[type=submit]`);
  await p.waitForTimeout(300);
  const botCap = await p.evaluate(() => window.__captured);
  T('honeypot submission is NOT passed to the tracker', botCap === null, String(botCap));
  await p.close();

  await b.close();
  const fails = results.filter(r => r.startsWith('FAIL')).length;
  console.log('\n' + results.join('\n'));
  console.log(`\n${fails} failure(s)`);
  process.exit(fails ? 1 : 0);
})();
