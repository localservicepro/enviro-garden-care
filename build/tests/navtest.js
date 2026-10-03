/* Services dropdown / submenu regression test.
   The dropdown once broke silently because main.js bound it with a URL
   selector that a routing change invalidated. These checks fail loudly if
   the binding, the hover behaviour or the mobile submenu ever go missing. */
const { chromium } = require('playwright');
(async () => {
  const BASE = 'http://127.0.0.1:8123';
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = [];
  const T = (label, ok, extra='') => out.push(`${ok?'PASS':'FAIL'}  ${label}${extra?' — '+extra:''}`);
  const only = r => /127\.0\.0\.1/.test(r.request().url());

  const EXPECTED = ['/services/lawn-mowing/','/services/acreage-mowing/','/services/garden-maintenance/',
    '/services/green-waste-removal/','/services/commercial-property-maintenance/','/services/odd-jobs-handyman/'];

  // ---------- desktop: hover opens the megamenu --------------------------
  for (const url of ['/', '/about/', '/services/lawn-mowing/']) {
    const p = await b.newPage({ viewport:{width:1440,height:900} });
    await p.route('**', r => only(r) ? r.continue() : r.abort());
    await p.goto(BASE+url, {waitUntil:'domcontentloaded'});
    await p.waitForFunction(() => document.documentElement.classList.contains('js-ready'));

    const item = await p.$('[data-nav="services"]');
    T(`${url} has the data-nav hook`, !!item);
    if (!item) { await p.close(); continue; }

    T(`${url} megamenu starts hidden`, await p.$eval('#megamenu', e => e.hasAttribute('hidden')));
    await item.hover();
    await p.waitForTimeout(250);
    const open = await p.$eval('#megamenu', e => !e.hasAttribute('hidden') && e.getBoundingClientRect().height > 0);
    T(`${url} hovering Services opens the dropdown`, open);

    const hrefs = await p.$$eval('#megamenu .megamenu__grid a', as => as.map(a=>a.getAttribute('href')));
    T(`${url} dropdown lists all 6 services`, hrefs.length === 6, `${hrefs.length} links`);
    T(`${url} dropdown links are correct`, EXPECTED.every(h => hrefs.includes(h)), hrefs.join(' '));

    // links must be clickable, not just painted
    const box = await p.$eval('#megamenu .megamenu__grid a', a => { const r=a.getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2}; });
    const top = await p.evaluate(({x,y}) => { const el=document.elementFromPoint(x,y); return el && !!el.closest('#megamenu'); }, box);
    T(`${url} dropdown links are on top / clickable`, top);

    // moving away closes it
    await p.mouse.move(10, 600);
    await p.waitForTimeout(350);
    T(`${url} dropdown closes on mouse-out`, await p.$eval('#megamenu', e => e.hasAttribute('hidden')));

    // keyboard: focus opens, Escape closes
    await p.focus('[data-nav="services"] > a');
    await p.waitForTimeout(200);
    T(`${url} keyboard focus opens the dropdown`, await p.$eval('#megamenu', e => !e.hasAttribute('hidden')));
    await p.keyboard.press('Escape');
    await p.waitForTimeout(150);
    T(`${url} Escape closes the dropdown`, await p.$eval('#megamenu', e => e.hasAttribute('hidden')));
    await p.close();
  }

  // ---------- desktop: nested list must NOT show ------------------------
  let p = await b.newPage({ viewport:{width:1440,height:900} });
  await p.route('**', r => only(r) ? r.continue() : r.abort());
  await p.goto(BASE+'/', {waitUntil:'domcontentloaded'});
  T('desktop hides the nested submenu (megamenu covers it)',
    await p.$eval('.nav__sub', e => getComputedStyle(e).display === 'none'));
  await p.close();

  // ---------- mobile: service links reachable in the drawer -------------
  p = await b.newPage({ viewport:{width:390,height:844}, hasTouch:true });
  await p.route('**', r => only(r) ? r.continue() : r.abort());
  await p.goto(BASE+'/', {waitUntil:'domcontentloaded'});
  await p.waitForFunction(() => document.documentElement.classList.contains('js-ready'));
  T('mobile drawer starts closed', await p.$eval('#nav', e => getComputedStyle(e).visibility === 'hidden'));
  await p.click('#burger');
  await p.waitForTimeout(450);
  T('burger opens the drawer', await p.$eval('#nav', e => getComputedStyle(e).visibility === 'visible'));
  // The drawer is position:fixed. If any ancestor gains transform/filter/
  // backdrop-filter it becomes the containing block and the drawer gets
  // clipped to that ancestor's height — which is exactly what happened once.
  const geo = await p.evaluate(() => {
    const n = document.querySelector('#nav'); const r = n.getBoundingClientRect();
    return {h: Math.round(r.height), vh: window.innerHeight, scrollH: n.scrollHeight};
  });
  T('drawer spans the viewport, not a clipped ancestor',
    geo.h >= geo.vh - 2, `drawer ${geo.h}px vs viewport ${geo.vh}px`);

  const subShown = await p.$eval('.nav__sub', e => getComputedStyle(e).display !== 'none');
  T('mobile drawer shows the service submenu', subShown);

  // Every nav entry must sit inside the drawer's visible box, not below its fold.
  const offscreen = await p.evaluate(() => {
    const n = document.querySelector('#nav');
    const nb = n.getBoundingClientRect();
    return [...n.querySelectorAll('a')]
      .filter(a => { const r = a.getBoundingClientRect();
                     return r.bottom > nb.bottom + 1 || r.top < nb.top - 1; })
      .map(a => a.textContent.trim().slice(0, 24));
  });
  T('no nav link falls outside the drawer', offscreen.length === 0, offscreen.join(' | '));
  const mHrefs = await p.$$eval('.nav__sub a', as => as.map(a=>a.getAttribute('href')));
  T('mobile submenu lists all 6 services', mHrefs.length === 6, `${mHrefs.length} links`);
  T('mobile submenu links are correct', EXPECTED.every(h => mHrefs.includes(h)), mHrefs.join(' '));
  const visible = await p.$$eval('.nav__sub a', as => as.every(a => a.getBoundingClientRect().width > 0));
  T('mobile submenu links are actually visible', visible);
  // tapping one navigates
  await p.click('.nav__sub a[href="/services/acreage-mowing/"]');
  await p.waitForURL('**/services/acreage-mowing/', {timeout:8000}).catch(()=>{});
  T('tapping a mobile submenu link navigates', /acreage-mowing/.test(p.url()), p.url());
  await p.close();

  await b.close();
  console.log(out.join('\n'));
  console.log(`\n${out.filter(r=>r.startsWith('FAIL')).length} failure(s)`);
})();
