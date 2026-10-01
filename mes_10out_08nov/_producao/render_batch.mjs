// usage: node render_batch.mjs jobs.json   (jobs: [{html, out, w, h, transparent}])
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import fs from 'fs';
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
for (const j of jobs) {
  await p.setViewportSize({ width: j.w || 1080, height: j.h || 1920 });
  const hf = j.out + '.html'; fs.writeFileSync(hf, j.html);
  await p.goto('file://' + hf, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => i.onload = i.onerror = r))));
  await p.screenshot({ path: j.out, omitBackground: !!j.transparent });
  fs.unlinkSync(hf);
}
await b.close();
