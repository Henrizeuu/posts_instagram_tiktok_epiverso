import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
const [,, inp, out, ...ts] = process.argv;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto('file://' + inp); await p.evaluate(() => document.fonts.ready);
for (const t of ts) { await p.evaluate(t => window.__t(t * 1000), +t); await p.screenshot({ path: `${out}_${t}.png` }); }
await b.close();
