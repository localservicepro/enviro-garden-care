const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const results = [];
  const T = (label, ok, extra='') => results.push(`${ok?'PASS':'FAIL'}  ${label}${extra?' — '+extra:''}`);

  // ---- 1. GHL field mapping present on every form ------------------------
  const expected = ['full_name','email','phone','property_address','property_size','service_needed','job_notes'];
  const merge = {full_name:'{{contact.full_name}}',email:'{{contact.email}}',phone:'{{contact.phone}}',
    property_address:'{{contact.property_address}}',property_size:'{{contact.property_size}}',
    service_needed:'{{contact.service_needed}}',job_notes:'{{contact.job_notes}}'};
  for (const url of ['/index.html','/contact.html','/services/lawn-mowing.html']) {
    const p = await b.newPage();
    await p.goto('http://127.0.0.1:8123'+url,{waitUntil:'domcontentloaded'});
    const forms = await p.$$eval('.quote__form', fs => fs.map(f => ({
      id: f.id, action: f.getAttribute('action'),
      fields: [...f.querySelectorAll('[name]')].filter(c=>c.name!=='company_website')
        .map(c=>({name:c.name, ghl:c.dataset.ghl, req:c.hasAttribute('required'), tag:c.tagName.toLowerCase()}))
    })));
    for (const f of forms) {
      const names = f.fields.map(x=>x.name);
      T(`${url} #${f.id} has all 7 GHL fields`, expected.every(e=>names.includes(e)), names.join(','));
      T(`${url} #${f.id} merge tags correct`, f.fields.every(x=>merge[x.name]===x.ghl));
      T(`${url} #${f.id} action -> thank-you`, /thank-you\.html$/.test(f.action||''), f.action);
    }
    await p.close();
  }

  // ---- 2. Validation blocks an empty submit ------------------------------
  let p = await b.newPage();
  await p.goto('http://127.0.0.1:8123/contact.html',{waitUntil:'networkidle'});
  const before = p.url();
  await p.click('#contact-quote button[type=submit]');
  await p.waitForTimeout(500);
  T('empty submit is blocked', p.url() === before, p.url());
  const invalid = await p.$$eval('[aria-invalid="true"]', e=>e.length);
  T('all 5 required fields flagged invalid', invalid === 5, `${invalid} flagged`);
  const msgs = await p.$$eval('.field__msg', e=>e.length);
  T('inline error messages shown', msgs === 5, `${msgs} messages`);

  // ---- 3. Bad email is rejected -----------------------------------------
  await p.fill('#contact-quote-full_name','Test User');
  await p.fill('#contact-quote-email','not-an-email');
  await p.fill('#contact-quote-phone','0400000000');
  await p.fill('#contact-quote-property_address','1 Test St, Coomera');
  await p.selectOption('#contact-quote-service_needed',{index:1});
  await p.click('#contact-quote button[type=submit]');
  await p.waitForTimeout(400);
  T('invalid email rejected', p.url() === before);
  const emailBad = await p.$eval('#contact-quote-email', e=>e.getAttribute('aria-invalid'));
  T('email field flagged', emailBad === 'true');

  // ---- 4. Valid submit redirects to thank-you ----------------------------
  await p.fill('#contact-quote-email','test@example.com');
  await p.fill('#contact-quote-job_notes','Big dog, side gate unlocked.');
  await p.click('#contact-quote button[type=submit]');
  await p.waitForURL('**/thank-you.html',{timeout:8000}).catch(()=>{});
  T('valid submit redirects to thank-you.html', /thank-you\.html$/.test(p.url()), p.url());
  const h1 = await p.$eval('h1', e=>e.textContent.trim()).catch(()=>'');
  T('thank-you page renders', /Thanks/i.test(h1), h1);
  const noindex = await p.$eval('meta[name=robots]', e=>e.content).catch(()=>'');
  T('thank-you is noindex', /noindex/.test(noindex), noindex);
  await p.close();

  // ---- 5. Payload shape that would be POSTed to GHL ----------------------
  p = await b.newPage();
  await p.goto('http://127.0.0.1:8123/contact.html',{waitUntil:'networkidle'});
  const payload = await p.evaluate(() => {
    const f = document.getElementById('contact-quote');
    f.full_name.value='Jane Citizen'; f.email.value='jane@example.com'; f.phone.value='0407 276 574';
    f.property_address.value='12 Example St, Ormeau'; f.property_size.selectedIndex=3;
    f.service_needed.selectedIndex=2; f.job_notes.value='Hedges too.';
    const d={}; [...f.querySelectorAll('[name]')].forEach(c=>{ if(c.name!=='company_website') d[c.name]=c.value.trim(); });
    return d;
  });
  console.log('\nExample GHL payload:\n' + JSON.stringify(payload,null,2));
  T('payload keys match GHL contact fields', expected.every(k=>k in payload));

  // ---- 6. Honeypot ------------------------------------------------------
  const hp = await p.$eval('#contact-quote [name=company_website]', e=>({
    off: e.getBoundingClientRect().left < 0, tab: e.tabIndex }));
  T('honeypot is off-screen and untabbable', hp.off && hp.tab === -1, JSON.stringify(hp));
  await p.close();

  // ---- 7. Tracking script still sees the submit, and redirect waits for it ----
  p = await b.newPage();
  // Stand in for link.msgsndr.com (blocked here / third-party): register a
  // document-level submit listener exactly like the GHL tracker does.
  await p.addInitScript(() => {
    window.__captured = null; window.__capturedAt = null; window.__navAt = null;
    document.addEventListener('submit', (ev) => {
      const f = ev.target; const d = {};
      [...f.querySelectorAll('[name]')].forEach(c => { d[c.name] = c.value; });
      window.__captured = d; window.__capturedAt = Date.now();
    });
    window.addEventListener('beforeunload', () => { window.__navAt = Date.now(); });
  });
  await p.goto('http://127.0.0.1:8123/contact.html',{waitUntil:'networkidle'});
  await p.fill('#contact-quote-full_name','Sam Tester');
  await p.fill('#contact-quote-email','sam@example.com');
  await p.fill('#contact-quote-phone','0407 276 574');
  await p.fill('#contact-quote-property_address','9 Cullen St, Pimpama');
  await p.selectOption('#contact-quote-service_needed',{index:1});
  await p.click('#contact-quote button[type=submit]');
  const cap = await p.evaluate(() => ({ d: window.__captured, at: window.__capturedAt }));
  T('tracking-style listener received the submit', !!cap.d, cap.d ? Object.keys(cap.d).filter(k=>k!=='company_website').join(',') : 'nothing captured');
  T('captured values are the real field values', cap.d && cap.d.full_name === 'Sam Tester' && cap.d.email === 'sam@example.com');
  const stillHere = !/thank-you/.test(p.url());
  T('redirect is deferred, not immediate', stillHere, stillHere ? 'still on contact.html right after submit' : 'navigated instantly — capture at risk');
  await p.waitForURL('**/thank-you.html',{timeout:8000}).catch(()=>{});
  T('redirect still happens', /thank-you\.html$/.test(p.url()), p.url());
  await p.close();

  // ---- 8. No PII in the URL on the JS path ------------------------------
  T('no field values leaked into the thank-you URL', !/full_name|email=/.test(p.url()), p.url());

  // ---- 9. Honeypot submissions are not captured -------------------------
  p = await b.newPage();
  await p.addInitScript(() => {
    window.__captured = null;
    document.addEventListener('submit', (ev) => { window.__captured = 'yes'; });
  });
  await p.goto('http://127.0.0.1:8123/contact.html',{waitUntil:'networkidle'});
  await p.evaluate(() => {
    const f = document.getElementById('contact-quote');
    f.full_name.value='Bot'; f.email.value='bot@spam.com'; f.phone.value='0400000000';
    f.property_address.value='x'; f.service_needed.selectedIndex=1;
    f.querySelector('[name=company_website]').value='http://spam.example';
  });
  await p.click('#contact-quote button[type=submit]');
  await p.waitForTimeout(300);
  const botCap = await p.evaluate(() => window.__captured);
  T('honeypot submission is NOT passed to the tracker', botCap === null, String(botCap));
  await p.close();

  await b.close();
  console.log('\n' + results.join('\n'));
  console.log(`\n${results.filter(r=>r.startsWith('FAIL')).length} failure(s)`);
})();
