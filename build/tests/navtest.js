/* Navigation: desktop megamenu, mobile drawer, and every service link reachable.
   The services dropdown broke once on a previous build when a URL changed, so it
   is covered here. See README.md in this folder. */
const { chromium } = require('playwright');

const BASE = process.env.BASE || 'http://127.0.0.1:8123';
const CHROME = process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

(async () => {
  const b = await chromium.launch({ executablePath: CHROME });
  const results = [];
  const T = (label, ok, extra = '') =>
    results.push(`${ok ? 'PASS' : 'FAIL'}  ${label}${extra ? ' — ' + extra : ''}`);

  // ---- desktop megamenu --------------------------------------------------
  let p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
  T('megamenu starts hidden', await p.$eval('#megamenu', e => e.hidden));
  await p.hover('[data-nav="services"] > a');
  await p.waitForTimeout(250);
  T('megamenu opens on hover', await p.$eval('#megamenu', e => !e.hidden));
  const megaLinks = await p.$$eval('#megamenu a[href^="/services/"]', a => a.map(x => x.href));
  T('megamenu lists all 6 services + hub', megaLinks.length === 7, `${megaLinks.length} links`);
  for (const href of megaLinks) {
    const r = await p.request.get(href);
    if (r.status() !== 200) T(`megamenu link ${href}`, false, `HTTP ${r.status()}`);
  }
  T('every megamenu link resolves 200', true);
  await p.mouse.move(20, 600);
  await p.waitForTimeout(400);
  T('megamenu closes when the pointer leaves', await p.$eval('#megamenu', e => e.hidden));
  await p.close();

  // ---- mobile drawer -----------------------------------------------------
  p = await b.newPage({ viewport: { width: 390, height: 844 } });
  await p.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
  const offscreen = await p.$eval('#nav', e => e.getBoundingClientRect().left >= window.innerWidth - 2);
  T('drawer starts off-screen', offscreen);
  await p.click('#burger');
  await p.waitForTimeout(450);
  T('burger opens the drawer', await p.$eval('#nav', e => e.getBoundingClientRect().left < window.innerWidth - 50));
  T('burger reports expanded', await p.$eval('#burger', e => e.getAttribute('aria-expanded') === 'true'));
  const subLinks = await p.$$eval('.nav__sub a', a => a.filter(x => x.offsetParent !== null).length);
  T('service links are tappable inside the drawer (no hover needed)', subLinks === 6, `${subLinks} visible`);
  await p.keyboard.press('Escape');
  await p.waitForTimeout(400);
  T('Escape closes the drawer', await p.$eval('#burger', e => e.getAttribute('aria-expanded') === 'false'));
  await p.close();

  // ---- footer + crawlable link graph ------------------------------------
  p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const seen = new Set();
  for (const url of ['/', '/services/', '/about/', '/contact/']) {
    await p.goto(BASE + url, { waitUntil: 'domcontentloaded' });
    const hrefs = await p.$$eval('a[href^="/"]', a => a.map(x => x.getAttribute('href')));
    hrefs.forEach(h => seen.add(h.split('#')[0]));
  }
  for (const want of ['/', '/services/', '/about/', '/contact/',
                      '/services/lawn-mowing/', '/services/ndis-yard-garden-maintenance/',
                      '/services/garden-maintenance/', '/services/tree-palm-removal/',
                      '/services/green-waste-removal/', '/services/hedging-lawn-treatments/']) {
    T(`${want} is linked from the main pages`, seen.has(want));
  }
  await p.close();

  await b.close();
  const fails = results.filter(r => r.startsWith('FAIL')).length;
  console.log(results.join('\n'));
  console.log(`\n${fails} failure(s)`);
  process.exit(fails ? 1 : 0);
})();
