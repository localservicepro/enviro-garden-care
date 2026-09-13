/* Gallery mosaic geometry: the featured tile must not leave a hole in the grid.
   See README.md in this folder. */
const { chromium } = require('playwright');

const OUT = process.env.SHOT_OUT || '/tmp/a1-shots';
const BASE = process.env.BASE || 'http://127.0.0.1:8123';
const CHROME = process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

(async () => {
  const b = await chromium.launch({ executablePath: CHROME });
  let bad = 0;
  for (const [name, w] of [['gallery-desktop', 1440], ['gallery-mobile', 390]]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
    // Stand-in tiles: the Drive CDN is a third party and may be blocked here.
    await p.addStyleTag({ content:
      `.shot img{background:repeating-linear-gradient(45deg,#2f7d1e,#2f7d1e 14px,#14472a 14px,#14472a 28px)!important;min-height:80px}
       .reveal{opacity:1!important;transform:none!important}` });
    await p.evaluate(() => document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in')));
    await p.waitForTimeout(400);
    const el = await p.$('#work');
    await el.screenshot({ path: `${OUT}/${name}.png` });

    const geo = await p.evaluate(() => {
      const g = document.querySelector('.shots');
      const cells = [...g.children];
      const cols = getComputedStyle(g).gridTemplateColumns.split(' ').length;
      const rows = [...new Set(cells.map(c => Math.round(c.getBoundingClientRect().top)))];
      // a hole shows up as a row whose tiles do not span the full width
      const right = Math.round(g.getBoundingClientRect().right);
      const lastRowTop = Math.max(...cells.map(c => Math.round(c.getBoundingClientRect().top)));
      const lastRow = cells.filter(c => Math.round(c.getBoundingClientRect().top) === lastRowTop);
      const fills = Math.abs(Math.round(lastRow[lastRow.length - 1].getBoundingClientRect().right) - right) < 2;
      return { items: cells.length, cols, rows: rows.length, lastRowFull: fills };
    });
    console.log(name, JSON.stringify(geo));
    if (!geo.lastRowFull) { console.log(`  FAIL ${name}: the last gallery row leaves a hole`); bad++; }
    await p.close();
  }
  await b.close();
  console.log(bad ? `\n${bad} failure(s)` : '\n0 failure(s)');
  process.exit(bad ? 1 : 0);
})();
