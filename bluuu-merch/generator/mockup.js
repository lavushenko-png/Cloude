// Render each design onto the photo with multiply blend. Usage: node mockup.js [ids...]
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const OUT = path.join(__dirname, 'out', 'designs');
const manifest = JSON.parse(fs.readFileSync(path.join(OUT, 'manifest.json'), 'utf8'));
const PX_MM = 2.85, NECK = { x: 757, y: 548 }, TILT = 2.4, SQUASH = 0.95;
const want = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1512, height: 2016 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const photo = 'data:image/jpeg;base64,' + fs.readFileSync(path.join(__dirname, 'photo.jpg')).toString('base64');
  for (const m of manifest) {
    if (want.length && !want.includes(m.id)) continue;
    const folder = path.join(OUT, `${m.id}-${m.slug}`);
    let svg = fs.readFileSync(path.join(folder, 'artwork.svg'), 'utf8');
    const W = m.w * PX_MM, H = m.h * PX_MM;
    const top = NECK.y + m.top * PX_MM;
    const axisX = NECK.x + (top - NECK.y) * Math.tan(TILT * Math.PI / 180);
    const left = axisX - W / 2;
    const tonal = m.method === 'puff';
    const style = tonal
      ? `mix-blend-mode:normal; opacity:0.92; filter: drop-shadow(1.5px 2.5px 2px rgba(20,30,50,0.28)) drop-shadow(-0.5px -0.5px 0.5px rgba(255,255,255,0.9));`
      : `mix-blend-mode:multiply; opacity:0.96;`;
    svg = svg.replace(/width="[^"]+mm" height="[^"]+mm"/, `width="${W}" height="${H}"`);
    const html = `<html><body style="margin:0;background:#fff">
      <div style="position:relative;width:1512px;height:2016px;overflow:hidden">
        <img src="${photo}" style="position:absolute;left:0;top:0;width:1512px;height:2016px">
        <div style="position:absolute;left:${left}px;top:${top}px;width:${W}px;height:${H}px;transform-origin:50% 0;transform:rotate(${TILT}deg) scaleY(${SQUASH});${style}">${svg}</div>
      </div></body></html>`;
    await page.setContent(html, { waitUntil: 'load' });
    await page.waitForTimeout(150);
    const buf = await page.screenshot({ type: 'jpeg', quality: 90, clip: { x: 0, y: 0, width: 1512, height: 2016 } });
    fs.writeFileSync(path.join(folder, 'mockup.jpg'), buf);
    console.log('mockup', m.id);
  }
  await browser.close();
})();
