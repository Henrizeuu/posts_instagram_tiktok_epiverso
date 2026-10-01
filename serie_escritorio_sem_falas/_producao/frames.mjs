// usage: node frames.mjs in.html outdir durationSec fps width height
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import fs from 'fs';
const [,, inp, out, dur, fps, w, h] = process.argv;
fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: +w, height: +h } });
await p.goto('file://' + inp);
await p.evaluate(() => document.fonts.ready);
await p.evaluate(() => Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => i.onload = i.onerror = r))));
const n = Math.round(+dur * +fps);
for (let i = 0; i < n; i++) {
  const t = i * 1000 / +fps;
  await p.evaluate(t => { document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; }); window.__t && window.__t(t); }, t);
  await p.evaluate(() => Promise.all([...document.images].filter(i => !i.complete).map(i => new Promise(r => { i.onload = i.onerror = r; }))));
  await p.screenshot({ path: `${out}/f${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92 });
}
await b.close();
