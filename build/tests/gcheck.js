const { chromium } = require('playwright');
(async () => {
  const out='/tmp/claude-0/-home-user-enviro-garden-care/5dcb1f51-fa09-5d89-8e44-281d246c0624/scratchpad';
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [name,w] of [['gallery-desktop',1440],['gallery-mobile',390]]) {
    const p = await b.newPage({ viewport:{width:w,height:900} });
    await p.goto('http://127.0.0.1:8123/index.html',{waitUntil:'domcontentloaded'});
    // stand-in tiles so the mosaic geometry is visible without the blocked CDN
    await p.addStyleTag({content:`.shot img{background:repeating-linear-gradient(45deg,#2a8154,#2a8154 14px,#1f6343 14px,#1f6343 28px)!important;min-height:80px}
      .reveal{opacity:1!important;transform:none!important}`});
    await p.evaluate(()=>document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in')));
    await p.waitForTimeout(400);
    const el = await p.$('#work');
    await el.screenshot({path:`${out}/${name}.png`});
    const geo = await p.evaluate(()=>{
      const g=document.querySelector('.shots');
      const rows=[...new Set([...g.children].map(c=>Math.round(c.getBoundingClientRect().top)))];
      const cs=getComputedStyle(g);
      return {items:g.children.length, rows:rows.length,
              cols:cs.gridTemplateColumns.split(' ').length,
              gridRows:cs.gridTemplateRows.split(' ').length};
    });
    console.log(name, JSON.stringify(geo));
    await p.close();
  }
  await b.close();
})();
