// usage: node render.mjs in.html out.png width height
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
const [,, inp, out, w, h] = process.argv;
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1 });
await p.goto('file://' + inp);
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(150);
await p.screenshot({ path: out, omitBackground: out.endsWith('.png') && process.env.TRANSPARENT === '1' });
await b.close();
