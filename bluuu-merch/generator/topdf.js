const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const jobs = [
    { html: 'out/techpack/techpack.html', pdf: 'out/techpack/bluuu-bodysuit-techpack.pdf', opts: { format: 'A4', landscape: true, printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } } },
    { html: 'out/lookbook/lookbook-standalone.html', pdf: 'out/lookbook/bluuu-merch-lookbook.pdf', opts: { format: 'A4', printBackground: true, margin: { top: '12mm', right: '10mm', bottom: '12mm', left: '10mm' } } },
  ];
  for (const j of jobs) {
    await page.goto('file://' + path.resolve(j.html), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(500);
    await page.pdf({ path: j.pdf, ...j.opts });
    console.log('pdf', j.pdf);
  }
  // page previews of the techpack for checking
  await page.goto('file://' + path.resolve('out/techpack/techpack.html'), { waitUntil: 'networkidle' });
  await page.setViewportSize({ width: 1123, height: 794 });
  const secs = await page.$$('section.page');
  for (const i of [0, 1, 2, 3, 4, 10, 14]) { if (secs[i]) await secs[i].screenshot({ path: `out/techpack/page-${i+1}.png` }); }
  await page.goto('file://' + path.resolve('out/lookbook/lookbook-standalone.html'), { waitUntil: 'networkidle' });
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.screenshot({ path: 'out/lookbook/shot-top.png' });
  await page.setViewportSize({ width: 400, height: 800 });
  await page.screenshot({ path: 'out/lookbook/shot-phone.png' });
  await page.setViewportSize({ width: 1280, height: 900 });
  const card = await page.$('#d07'); if (card) await card.screenshot({ path: 'out/lookbook/shot-card.png' });
  const tbl = await page.$('#summary'); if (tbl) await tbl.screenshot({ path: 'out/lookbook/shot-summary.png' });
  await browser.close();
})();
