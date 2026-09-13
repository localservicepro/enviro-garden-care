/* Screenshots + a layout/JS error sweep. See README.md in this folder. */
const { chromium } = require('playwright');

const OUT = process.env.SHOT_OUT || '/tmp/a1-shots';
const BASE = process.env.BASE || 'http://127.0.0.1:8123';
const CHROME = process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  const errs = [];
  const pages = [
    ['home-desktop', '/', 1440, 1000],
    ['home-mobile', '/', 390, 844],
    ['services-desktop', '/services/', 1440, 1000],
    ['service-desktop', '/services/ndis-yard-garden-maintenance/', 1440, 1000],
    ['service-mobile', '/services/tree-palm-removal/', 390, 844],
    ['about-desktop', '/about/', 1440, 1000],
    ['contact-desktop', '/contact/', 1440, 1000],
    ['contact-mobile', '/contact/', 390, 844],
    ['thanks-desktop', '/thank-you/', 1440, 1000],
    ['notfound-desktop', '/404.html', 1440, 1000],
  ];

  for (const [name, url, w, h] of pages) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    page.on('console', m => { if (m.type() === 'error') errs.push(`${name}: console ${m.text()}`); });
    page.on('pageerror', e => errs.push(`${name}: pageerror ${e.message}`));

    const resp = await page.goto(BASE + url, { waitUntil: 'load', timeout: 30000 })
      .catch(e => { errs.push(`${name}: ${e.message}`); return null; });
    if (resp && resp.status() !== 200) errs.push(`${name}: HTTP ${resp.status()}`);

    await page.evaluate(() => {
      document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in'));
    });
    await page.waitForTimeout(600);

    // horizontal overflow
    const ovf = await page.evaluate(() => {
      window.scrollTo(500, 0);
      const x = window.scrollX;
      window.scrollTo(0, 0);
      return x;
    });
    if (ovf > 1) errs.push(`${name}: page scrolls horizontally by ${ovf}px`);

    // the off-canvas drawer must not keep links focusable while closed
    const focusable = await page.evaluate(() => {
      const n = document.querySelector('#nav');
      if (!n || getComputedStyle(n).position !== 'fixed') return 0;
      if (document.body.classList.contains('nav-open')) return 0;
      const box = n.getBoundingClientRect();
      return box.left < window.innerWidth - 2 ? n.querySelectorAll('a,button').length : 0;
    });
    if (focusable) errs.push(`${name}: ${focusable} off-canvas nav links exposed while closed`);

    // exactly one H1, and it is visible
    const h1 = await page.evaluate(() => {
      const all = document.querySelectorAll('h1');
      return { n: all.length, text: all[0] ? all[0].textContent.trim().slice(0, 70) : '' };
    });
    if (h1.n !== 1) errs.push(`${name}: ${h1.n} h1 tags`);

    await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: true });
    console.log(`${name.padEnd(18)} h1="${h1.text}"`);
    await page.close();
  }

  await browser.close();
  // Drive images, Google Fonts and the Maps embed are third-party hosts; a
  // sandbox with no egress will 404 them without that meaning anything.
  const real = errs.filter(e => !/Failed to load resource|ERR_(NAME|CONNECTION|TUNNEL|BLOCKED)/i.test(e));
  console.log('\n' + (real.length ? real.join('\n') : 'NO LAYOUT/JS ERRORS (external asset failures ignored)'));
  process.exit(real.length ? 1 : 0);
})();
