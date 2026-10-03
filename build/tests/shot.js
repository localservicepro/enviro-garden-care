const { chromium } = require('playwright');
(async () => {
  const out = '/tmp/claude-0/-home-user-enviro-garden-care/5dcb1f51-fa09-5d89-8e44-281d246c0624/scratchpad';
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const errs = [];
  for (const [name, url, w, h, full] of [
    ['home-desktop', '/', 1440, 1000, true],
    ['home-mobile', '/', 390, 844, true],
    ['service', '/services/acreage-mowing/', 1440, 1000, true],
    ['contact', '/contact/', 1440, 1000, true],
    ['thanks', '/thank-you/', 1440, 1000, true],
    ['about', '/about/', 1440, 1000, true],
  ]) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    page.on('console', m => { if (m.type() === 'error') errs.push(`${name}: console ${m.text()}`); });
    page.on('pageerror', e => errs.push(`${name}: pageerror ${e.message}`));
    const resp = await page.goto('http://127.0.0.1:8123' + url, { waitUntil: 'networkidle', timeout: 30000 }).catch(e => { errs.push(name + ': ' + e.message); return null; });
    if (resp && resp.status() !== 200) errs.push(`${name}: HTTP ${resp.status()}`);
    await page.evaluate(() => { document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in')); });
    await page.waitForTimeout(700);
    // measure horizontal overflow
    const ovf = await page.evaluate(() => { window.scrollTo(500, 0); const x = window.scrollX; window.scrollTo(0, 0); return x; });
    if (ovf > 1) errs.push(`${name}: page scrolls horizontally by ${ovf}px`);
    const focusable = await page.evaluate(() => { const n = document.querySelector('#nav'); if (!n || getComputedStyle(n).position !== 'fixed') return 0; return getComputedStyle(n).visibility === 'hidden' ? 0 : n.querySelectorAll('a,button').length; });
    if (focusable) errs.push(`${name}: ${focusable} off-canvas nav links still focusable`);
    await page.screenshot({ path: `${out}/${name}.png`, fullPage: full });
    await page.close();
  }
  await browser.close();
  const real = errs.filter(e => !/Failed to load resource/.test(e));
  console.log(real.length ? real.join('\n') : 'NO LAYOUT/JS ERRORS (external asset 404s ignored — sandbox blocks Drive/Fonts/Maps)');
})();
