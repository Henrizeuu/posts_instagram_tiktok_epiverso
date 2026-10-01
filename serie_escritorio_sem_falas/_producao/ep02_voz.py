"""Escritório sem falas · ep. 02 · "É despesa, né?" (3 personagens)"""
import sys, os
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); sys.path.insert(0, os.path.dirname(H) + '/build')
from kit import FONTS, B
from chars import GRAD, person
DUR = 25.8
CSS = FONTS + r"""
*{margin:0;padding:0;box-sizing:border-box} html,body{width:1080px;height:1920px;overflow:hidden;background:#0A0A0A;font-family:Inter;-webkit-font-smoothing:antialiased}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:54px 54px;-webkit-mask-image:radial-gradient(ellipse 95% 60% at 85% 0%,#000 0%,rgba(0,0,0,.35) 55%,transparent 85%)}
.glow{position:absolute;width:1200px;height:1200px;right:-480px;top:-560px;background:radial-gradient(circle,rgba(16,185,129,.24) 0%,rgba(16,185,129,.07) 35%,transparent 65%)}
.logo{position:absolute;left:80px;top:150px;height:42px}
.kicker{position:absolute;left:80px;top:268px;font-family:JBM;font-weight:500;color:#10B981;font-size:24px;letter-spacing:.42em;display:flex;align-items:center;gap:18px;text-transform:uppercase}
.kicker:before{content:'';width:34px;height:3px;background:#10B981;display:block}
.title{position:absolute;left:78px;right:80px;top:316px;font-weight:800;font-size:104px;letter-spacing:-.055em;line-height:.98;background:linear-gradient(180deg,#fff 25%,#BFC0C7 85%);-webkit-background-clip:text;color:transparent}
.title .g{-webkit-text-fill-color:#10B981}
.card{position:absolute;left:40px;top:560px;width:1000px;height:960px;border-radius:36px;background:#121214;border:1px solid rgba(255,255,255,.08);overflow:hidden}
.foot{position:absolute;left:80px;right:80px;top:1550px;display:flex;justify-content:space-between;font-family:JBM;font-size:22px;letter-spacing:.34em;color:#6E6E76}
.bal{position:absolute;opacity:0;transform-origin:var(--ox) var(--oy)}
.bal .box{border-radius:30px;padding:20px 30px 22px;font-weight:700;font-size:46px;letter-spacing:-.025em;line-height:1.12}
.bal .lab{font-family:JBM;font-weight:500;font-size:19px;letter-spacing:.3em;margin-bottom:10px}
.bal.me .box{background:#F2F2F3;color:#0A0A0A;box-shadow:0 16px 40px rgba(0,0,0,.45)} .bal.me .lab{color:#6E6E76}
.bal.cli .box{background:#121214;color:#fff;border:2px solid #10B981;box-shadow:0 16px 40px rgba(0,0,0,.55)} .bal.cli .lab{color:#10B981}
.bal .tail{position:absolute;width:34px;height:34px;transform:rotate(45deg)}
.bal.me .tail{background:#F2F2F3}.bal.cli .tail{background:#121214;border-right:2px solid #10B981;border-bottom:2px solid #10B981}
"""
SCENE = f"""
<svg width="1000" height="960" viewBox="-220 272 1300 1248" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" style="overflow:visible">
<defs>{GRAD}
 <pattern id="pg" width="54" height="54" patternUnits="userSpaceOnUse"><path d="M54 0H0V54" fill="none" stroke="rgba(255,255,255,.035)" stroke-width="1"/></pattern>
 <radialGradient id="gScr" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#10B981" stop-opacity=".5"/><stop offset="1" stop-color="#10B981" stop-opacity="0"/></radialGradient>
 <filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>
</defs>
<rect x="-400" y="200" width="1700" height="1400" fill="#141417"/><rect x="-400" y="200" width="1700" height="1400" fill="url(#pg)"/>
<rect x="-400" y="1440" width="1700" height="200" fill="#0E0E10"/><rect x="-400" y="1438" width="1700" height="3" fill="rgba(255,255,255,.07)"/>
<g transform="translate(640 500)">
 <rect x="-12" y="-12" width="344" height="404" rx="18" fill="#1E1E22" stroke="rgba(255,255,255,.08)"/>
 <rect width="320" height="380" rx="10" fill="#5E7F9C"/><circle cx="232" cy="96" r="36" fill="#F3E3B0"/>
 <g fill="#3E556B"><rect x="0" y="270" width="66" height="110"/><rect x="74" y="232" width="56" height="148"/><rect x="138" y="290" width="76" height="90"/><rect x="222" y="244" width="98" height="136"/></g>
 <rect x="153" width="14" height="380" fill="#1E1E22"/><rect y="183" width="320" height="14" fill="#1E1E22"/>
</g>
<g transform="translate(330 560)"><circle r="96" fill="#1E1E22" stroke="rgba(255,255,255,.1)" stroke-width="2"/><circle r="84" fill="#EDEDEF"/>
 <rect x="-6" y="-48" width="12" height="54" rx="6" fill="#0A0A0A" transform="rotate(130)"/><rect x="-4" y="-70" width="8" height="76" rx="4" fill="#0A0A0A" transform="rotate(240)"/><circle r="8" fill="#10B981"/></g>
<g transform="translate(-170 880)"><rect x="18" y="-110" width="32" height="110" rx="5" fill="#10B981"/><rect x="54" y="-102" width="32" height="102" rx="5" fill="#2A2A2F"/><rect x="90" y="-110" width="32" height="110" rx="5" fill="#3A3A40"/><rect y="0" width="150" height="14" rx="4" fill="#2A2A2F"/></g>
<!-- sócio (atrás, à esquerda) -->
{person('S', 'socio', 1, 'stand')}
<!-- cliente (atrás da mesa, à direita) -->
{person('C', 'cliente', -1, 'stand')}
<!-- cadeira + fiscal -->
<g fill="#26262B"><rect x="140" y="990" width="44" height="320" rx="20"/><rect x="150" y="1300" width="300" height="40" rx="18"/><rect x="288" y="1340" width="22" height="100"/><rect x="210" y="1432" width="180" height="14" rx="7"/></g>
{person('F', 'fiscal', 1, 'sit')}
<!-- mesa -->
<rect x="470" y="1250" width="610" height="30" rx="8" fill="#2A2A2F"/><rect x="470" y="1250" width="610" height="4" rx="2" fill="#10B981" opacity=".55"/>
<rect x="500" y="1280" width="20" height="160" fill="#1E1E22"/><rect x="1030" y="1280" width="20" height="160" fill="#1E1E22"/>
<ellipse cx="610" cy="1080" rx="160" ry="160" fill="url(#gScr)" opacity=".35"/>
<rect x="628" y="1130" width="16" height="120" fill="#1E1E22"/><rect x="590" y="1236" width="96" height="14" rx="6" fill="#1E1E22"/>
<path d="M 600 980 L 650 962 L 650 1160 L 600 1142 Z" fill="#1E1E22"/><path d="M 606 988 L 642 975 L 642 1146 L 606 1134 Z" fill="#0F2A22"/>
<g fill="#10B981"><path d="M 612 1100 l 6 -2 v 20 l -6 2z"/><path d="M 622 1092 l 6 -2 v 30 l -6 2z" opacity=".8"/><path d="M 632 1080 l 6 -2 v 44 l -6 2z"/></g>
<rect x="476" y="1236" width="110" height="14" rx="6" fill="#1E1E22"/>
<g transform="translate(700 1186)"><rect width="50" height="62" rx="9" fill="#EDEDEF"/><path d="M50 14 q28 4 0 32" fill="none" stroke="#EDEDEF" stroke-width="9"/><rect x="7" y="11" width="36" height="7" rx="3" fill="#10B981"/></g>
<!-- caixa de notas -->
<g id="box"><g transform="translate(-75 -110)">
 <rect width="150" height="110" rx="8" fill="#C08A57"/><path d="M0 0 L -18 -34 L 70 -34 L 75 0 Z" fill="#D39C66"/><path d="M150 0 L 168 -34 L 80 -34 L 75 0 Z" fill="#A9763F"/>
 <rect x="30" y="38" width="90" height="34" rx="6" fill="#F7F1E6"/><text x="75" y="56" font-family="JBM" font-size="16" font-weight="700" fill="#0A0A0A" text-anchor="middle" dominant-baseline="central">NOTAS</text>
</g></g>
<g id="it1" opacity="0"><text font-size="96" text-anchor="middle" dominant-baseline="central">🍖</text></g>
<g id="it2" opacity="0"><text font-size="96" text-anchor="middle" dominant-baseline="central">🏖️</text></g>
</svg>"""
BALLOONS = """
<div class="bal cli" id="c1" style="left:330px;top:720px;--ox:560px;--oy:190px"><div class="box"><div class="lab">CLIENTE</div>Trouxe as notas<br>do ano! 📦</div><div class="tail" style="right:70px;bottom:-15px"></div></div>
<div class="bal cli" id="c2" style="left:300px;top:700px;--ox:590px;--oy:210px"><div class="box"><div class="lab">CLIENTE</div>A churrasqueira entra<br>como despesa, né? 🍖</div><div class="tail" style="right:70px;bottom:-15px"></div></div>
<div class="bal me" id="f1" style="left:250px;top:730px;--ox:200px;--oy:150px"><div class="box"><div class="lab">FISCAL</div>Churrasqueira?!</div><div class="tail" style="left:180px;bottom:-14px"></div></div>
<div class="bal cli" id="c3" style="left:330px;top:700px;--ox:560px;--oy:210px"><div class="box"><div class="lab">CLIENTE</div>E a viagem pra praia…<br>foi reunião! 🏖️</div><div class="tail" style="right:70px;bottom:-15px"></div></div>
<div class="bal me" id="s1" style="left:90px;top:640px;--ox:80px;--oy:200px"><div class="box"><div class="lab">SÓCIO</div>Claro! A gente<br>lança tudo…</div><div class="tail" style="left:60px;bottom:-14px"></div></div>
<div class="bal cli" id="c4" style="left:560px;top:720px;--ox:330px;--oy:150px"><div class="box"><div class="lab">CLIENTE</div>Opa! Isso! 🤩</div><div class="tail" style="right:70px;bottom:-15px"></div></div>
<div class="bal me" id="s2" style="left:90px;top:640px;--ox:80px;--oy:200px"><div class="box"><div class="lab">SÓCIO</div>…na sua pessoa<br>física. 🙂</div><div class="tail" style="left:60px;bottom:-14px"></div></div>
<div class="bal cli" id="c5" style="left:620px;top:740px;--ox:280px;--oy:150px"><div class="box"><div class="lab">CLIENTE</div>Ah… tá.</div><div class="tail" style="right:70px;bottom:-15px"></div></div>
<div class="bal me" id="f2" style="left:250px;top:740px;--ox:200px;--oy:150px"><div class="box"><div class="lab">FISCAL</div>Obrigado, chefe. 😮‍💨</div><div class="tail" style="left:180px;bottom:-14px"></div></div>
"""
JS = r"""
const ease = { io: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2, l: t => t, o: t => 1 + 2.70158 * Math.pow(t - 1, 3) + 1.70158 * Math.pow(t - 1, 2) };
const TR = {}; function k(id, prop, arr){ (TR[id] = TR[id] || {})[prop] = arr; }
function val(arr, t){ if (t <= arr[0][0]) return arr[0][1];
  for (let i = 1; i < arr.length; i++) if (t <= arr[i][0]) { const [t0, v0] = arr[i - 1], [t1, v1, e] = arr[i]; return v0 + (v1 - v0) * (ease[e || 'io'])((t - t0) / (t1 - t0)); }
  return arr[arr.length - 1][1]; }
const BASE = { F: [330, 1300], S: [-560, 1300], C: [1260, 1300], box: [1150, 1110], it1: [800, 1060], it2: [800, 1060] };
for (const p of 'FSC') Object.assign(BASE, { [p + 'body']: [0, 0], [p + 'head']: [0, -300], [p + 'arm1']: [28, -290], [p + 'arm2']: [-24, -290],
  [p + '_vein']: [95, -560], [p + '_sweat']: [120, -470], [p + '_excl']: [120, -560], [p + '_q']: [120, -560] });
for (const p of 'SC') Object.assign(BASE, { [p + 'leg1']: [40, -30], [p + 'leg2']: [-40, -30] });
const FLIP = { C_q: true };
const POPS = [['c1', 2.75, 5.2], ['c2', 5.3, 8.55], ['f1', 8.55, 10.3], ['c3', 10.35, 14.2], ['s1', 15.0, 17.35], ['c4', 17.4, 19.7], ['s2', 19.8, 21.9], ['c5', 22.0, 23.3], ['f2', 23.35, 25.7]];
function apply(t){
  for (const id in BASE) { if (TR[id]) continue; const el = document.getElementById(id); if (!el) continue;
    if (!['S_spark','F_spark','C_spark'].includes(id)) el.setAttribute('transform', `translate(${BASE[id][0]} ${BASE[id][1]})` + (FLIP[id] ? ' scale(-1 1)' : '')); }
  for (const id in TR) { const el = document.getElementById(id), P = TR[id], b = BASE[id] || [0, 0], g = p => P[p] ? val(P[p], t) : null;
    if (P.op) el.setAttribute('opacity', g('op'));
    if (P.x || P.y || P.r || P.sx || P.sy) el.setAttribute('transform', `translate(${b[0] + (g('x') || 0)} ${b[1] + (g('y') || 0)}) rotate(${g('r') || 0}) scale(${(P.sx ? g('sx') : 1) * (FLIP[id] ? -1 : 1)} ${P.sy ? g('sy') : 1})`); }
  for (const [id, t0, t1] of POPS) { const el = document.getElementById(id); let s = .6, o = 0;
    if (t >= t0 && t <= t1) { const a = Math.min(1, (t - t0) / .25), z = Math.min(1, (t1 - t) / .18); s = (.6 + .4 * ease.o(a)) * (.9 + .1 * z); o = Math.min(1, a * 2) * z; }
    el.style.opacity = o; el.style.transform = `scale(${s})`; }
}
// helpers
function show(id, t0, t1, pulse){ const a = [[0, 0], [t0 - .01, 0], [t0 + .12, 1], [t1 - .12, 1], [t1, 0]]; k(id, 'op', a);
  if (pulse) { const s = [[0, 1]]; for (let t = t0, i = 0; t < t1; t += .2, i++) s.push([t, i % 2 ? 1.18 : .92]); k(id, 'sx', s); k(id, 'sy', s); } }
function walk(p, t0, t1, x0, x1, step = .22){ const x = [[0, x0], [t0, x0], [t1, x1, 'l']], y = [[0, 0], [t0, 0]], l1 = [[0, 0], [t0, 0]], l2 = [[0, 0], [t0, 0]];
  for (let t = t0, i = 0; t <= t1; t += step / 2, i++) { y.push([t, i % 2 ? -14 : 0]); l1.push([t, i % 2 ? 0 : (i % 4 ? 16 : -16)]); l2.push([t, i % 2 ? 0 : (i % 4 ? -16 : 16)]); }
  y.push([t1 + .1, 0]); l1.push([t1 + .1, 0]); l2.push([t1 + .1, 0]); return { x, y, l1, l2 }; }
function merge(id, prop, arr){ const cur = (TR[id] && TR[id][prop]) || []; k(id, prop, cur.concat(arr).sort((a, b) => a[0] - b[0])); }
// ---------- fiscal digitando
const TY = -72, a1 = [[0, TY]], a2 = [[0, TY + 6]];
for (let t = .1, i = 0; t <= 1.6; t += .16, i++) { a1.push([t, TY + (i % 2 ? 6 : -6)]); a2.push([t, TY + 6 + (i % 2 ? -6 : 6)]); }
a1.push([1.9, TY]); a2.push([1.9, TY + 6]);
// "Churrasqueira?!": braço aponta pro cliente
a1.push([8.5, TY], [8.75, -100, 'o'], [10.2, -100], [10.6, TY]); a2.push([8.5, TY + 6], [10.6, TY + 6]);
// raiva (11.0–13.9): punhos tremendo
a1.push([10.9, TY], [11.15, -150, 'o']); a2.push([10.9, TY + 6], [11.15, -140, 'o']);
for (let t = 11.25, i = 0; t < 13.9; t += .06, i++) { a1.push([t, -150 + (i % 2 ? 6 : -6)]); a2.push([t, -140 + (i % 2 ? -6 : 6)]); }
a1.push([14.2, TY]); a2.push([14.2, TY + 6]);
a1.push([23.3, TY], [23.7, -15]); a2.push([23.3, TY + 6], [23.7, -10]); a1.push([25.8, -15]); a2.push([25.8, -10]);
k('Farm1', 'r', a1); k('Farm2', 'r', a2);
k('Fhead', 'r', [[0, 4], [1.8, 4], [2.1, -4], [8.5, -4], [8.7, -12], [10.2, -12], [10.9, -4], [11.1, 8], [13.9, 8], [14.4, -14], [15.2, -14], [15.6, -4], [23.3, -4], [23.8, -18], [25.8, -18]]);
const fbx = [[0, 0], [11.0, 0]]; for (let t = 11.05, i = 0; t < 13.9; t += .05, i++) fbx.push([t, i % 2 ? 5 : -5]); fbx.push([13.95, 0]); k('Fbody', 'x', fbx);
k('Fbody', 'r', [[0, 0], [23.3, 0], [23.8, -10], [25.8, -10]]);
k('Fbody', 'sy', [[0, 1], [8.5, 1], [8.7, 1.06, 'o'], [10.2, 1.06], [10.4, 1], [10.9, 1], [11.1, 1.05, 'o'], [13.9, 1.05], [14.2, 1], [25.8, 1]]);
show('F_sweat', 3.6, 5.2); show('F_q', 8.5, 9.4); show('F_vein', 9.2, 14.0, true); show('F_steam', 11.1, 14.0);
k('F_excl', 'op', [[0, 0], [1.99, 0], [2.12, 1], [2.58, 1], [2.7, 0], [17.39, 0], [17.52, 1], [18.3, 1], [18.45, 0]]);
show('F_spark', 23.4, 25.7);
// ---------- cliente
let w = walk('C', 1.0, 2.4, 0, -300);
k('C', 'x', w.x.concat([[23.3, -300], [25.2, 60, 'l']]));
const cy = w.y.concat([[17.4, 0], [17.6, -18], [17.75, 0], [17.9, -18], [18.05, 0], [18.2, -14], [18.35, 0], [18.5, -14], [18.65, 0]]);
for (let t = 23.3, i = 0; t < 25.2; t += .14, i++) cy.push([t, i % 2 ? -8 : 0]); k('C', 'y', cy.sort((a, b) => a[0] - b[0]));
const cl1 = w.l1.slice(), cl2 = w.l2.slice(); for (let t = 23.3, i = 0; t < 25.2; t += .14, i++) { cl1.push([t, i % 2 ? 0 : (i % 4 ? 12 : -12)]); cl2.push([t, i % 2 ? 0 : (i % 4 ? -12 : 12)]); }
k('Cleg1', 'r', cl1); k('Cleg2', 'r', cl2);
k('Carm1', 'r', [[0, -40], [2.4, -40], [2.7, -60], [2.9, -10], [5.2, -10], [5.4, -130, 'o'], [8.4, -130], [8.6, -10], [10.3, -10], [10.5, -150, 'o'], [14.0, -150], [14.3, -10], [17.4, -10], [17.6, -160, 'o'], [19.6, -160], [19.9, -10], [23.2, -10], [23.5, -50], [25.8, -50]]);
k('Carm2', 'r', [[0, -40], [2.4, -40], [2.9, -10], [17.4, -10], [17.6, -150, 'o'], [19.6, -150], [19.9, -10], [25.8, -10]]);
k('Chead', 'r', [[0, 0], [21.6, 0], [22.0, 26], [25.8, 26]]);
k('Cbody', 'sy', [[0, 1], [21.6, 1], [22.0, .9], [25.8, .9]]); k('Cbody', 'sx', [[0, 1], [21.6, 1], [22.0, 1.05], [25.8, 1.05]]);
show('C_spark', 17.4, 19.7); show('C_q', 21.4, 22.1);
k('C_gloom', 'op', [[0, 0], [22.0, 0], [22.2, 1], [25.8, 1]]);
const bx = [[0, 0], [1.0, 0], [2.4, -300, 'l'], [2.7, -350], [23.2, -350], [23.4, -300], [25.2, 60, 'l']];
const byy = [[0, 0], [1.0, 0]]; for (let t = 1.0, i = 0; t <= 2.4; t += .11, i++) byy.push([t, i % 2 ? -14 : 0]);
byy.push([2.7, 26, 'o'], [23.2, 26], [23.4, 0]); k('box', 'x', bx); k('box', 'y', byy);
show('it1', 5.3, 8.55); k('it1', 'y', [[0, 30], [5.3, 30], [5.6, -30, 'o'], [8.55, -30]]);
show('it2', 10.35, 14.2); k('it2', 'y', [[0, 30], [10.35, 30], [10.65, -30, 'o'], [14.2, -30]]);
// ---------- sócio
w = walk('S', 13.6, 14.9, 0, 490);
k('S', 'x', w.x); k('S', 'y', w.y); k('Sleg1', 'r', w.l1); k('Sleg2', 'r', w.l2);
k('Sarm1', 'r', [[0, -10], [14.9, -10], [15.2, -125, 'o'], [17.3, -125], [17.6, -95], [21.9, -95], [22.3, -62], [25.8, -62]]);
k('Sarm2', 'r', [[0, 0], [25.8, 0]]);
show('S_spark', 14.4, 16.8);
window.__t = ms => apply(ms / 1000); apply(0);
"""
HTML = f"""<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>
<div class="grid"></div><div class="glow"></div>
<img class="logo" src="file://{B}logo_wordmark.png">
<div class="kicker">Cenas de escritório · ep. 02</div>
<div class="title">É despesa, <span class="g">né?</span></div>
<div class="card">{SCENE}</div>
{BALLOONS}
<div class="foot"><span>PAINEL FISCAL</span><span>EPIVERSO</span></div>
<script>{JS}</script></body></html>"""
out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/ep02.html'
open(out, 'w').write(HTML); print(out, DUR)
