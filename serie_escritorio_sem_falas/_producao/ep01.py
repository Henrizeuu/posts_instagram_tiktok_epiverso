"""Escritório sem falas · ep. 01 · identidade dos posts (preto, grade, verde, Inter/JBM) + balões legíveis"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/build')
from kit import FONTS, B
DUR = 14.0
HTML = r"""<!doctype html><html><head><meta charset='utf-8'><style>""" + FONTS + r"""
*{margin:0;padding:0;box-sizing:border-box} html,body{width:1080px;height:1920px;overflow:hidden;background:#0A0A0A;font-family:Inter;-webkit-font-smoothing:antialiased}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:54px 54px;-webkit-mask-image:radial-gradient(ellipse 95% 60% at 85% 0%,#000 0%,rgba(0,0,0,.35) 55%,transparent 85%)}
.glow{position:absolute;width:1200px;height:1200px;right:-480px;top:-560px;background:radial-gradient(circle,rgba(16,185,129,.24) 0%,rgba(16,185,129,.07) 35%,transparent 65%)}
.logo{position:absolute;left:80px;top:150px;height:42px}
.kicker{position:absolute;left:80px;top:268px;font-family:JBM;font-weight:500;color:#10B981;font-size:24px;letter-spacing:.42em;display:flex;align-items:center;gap:18px;text-transform:uppercase}
.kicker:before{content:'';width:34px;height:3px;background:#10B981;display:block}
.title{position:absolute;left:78px;right:80px;top:316px;font-weight:800;font-size:104px;letter-spacing:-.055em;line-height:.98;background:linear-gradient(180deg,#fff 25%,#BFC0C7 85%);-webkit-background-clip:text;color:transparent}
.title .g{-webkit-text-fill-color:#10B981}
.card{position:absolute;left:40px;top:560px;width:1000px;height:960px;border-radius:36px;background:#121214;border:1px solid rgba(255,255,255,.08);overflow:hidden}
.chip{position:absolute;right:80px;top:330px;font-family:JBM;color:#8A8A92;font-size:20px;letter-spacing:.3em;text-align:right}
.chip b{display:block;font-weight:500;color:#10B981;font-size:46px;letter-spacing:.04em;margin-top:6px}
.foot{position:absolute;left:80px;right:80px;top:1550px;display:flex;justify-content:space-between;font-family:JBM;font-size:22px;letter-spacing:.34em;color:#6E6E76}
.bal{position:absolute;opacity:0;transform-origin:var(--ox) var(--oy)}
.bal .box{border-radius:30px;padding:22px 30px;font-weight:700;font-size:46px;letter-spacing:-.025em;line-height:1.12}
.bal.me .box{background:#F2F2F3;color:#0A0A0A;box-shadow:0 16px 40px rgba(0,0,0,.45)}
.bal.cli .box{background:#121214;color:#fff;border:2px solid #10B981;box-shadow:0 16px 40px rgba(0,0,0,.55)}
.bal.cli .lab{font-family:JBM;font-weight:500;font-size:19px;letter-spacing:.3em;color:#10B981;margin-bottom:10px}
.bal .tail{position:absolute;width:34px;height:34px;transform:rotate(45deg)}
.bal.me .tail{background:#F2F2F3}.bal.cli .tail{background:#121214;border-right:2px solid #10B981;border-bottom:2px solid #10B981}
.g{color:#10B981}
</style></head><body>
<div class="grid"></div><div class="glow"></div>
<img class="logo" src="file://""" + B + r"""logo_wordmark.png">
<div class="kicker">Escritório sem falas · ep. 01</div>
<div class="title">É <span class="g">rapidinho.</span></div>
<div class="card">
<svg width="1000" height="960" viewBox="0 420 1080 1037" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
<defs>
 <radialGradient id="gW" cx="35%" cy="28%" r="80%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#ECEEF0"/><stop offset="1" stop-color="#B9C0C6"/></radialGradient>
 <radialGradient id="gW2" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".6" stop-color="#E7EAED"/><stop offset="1" stop-color="#B4BCC3"/></radialGradient>
 <radialGradient id="gScr" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#10B981" stop-opacity=".55"/><stop offset="1" stop-color="#10B981" stop-opacity="0"/></radialGradient>
 <radialGradient id="gPh" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#34D399" stop-opacity=".9"/><stop offset="1" stop-color="#34D399" stop-opacity="0"/></radialGradient>
 <pattern id="pg" width="54" height="54" patternUnits="userSpaceOnUse"><path d="M54 0H0V54" fill="none" stroke="rgba(255,255,255,.035)" stroke-width="1"/></pattern>
 <filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>
</defs>
<rect x="0" y="400" width="1080" height="1100" fill="#141417"/><rect x="0" y="400" width="1080" height="1100" fill="url(#pg)"/>
<rect y="1440" width="1080" height="80" fill="#0E0E10"/><rect y="1438" width="1080" height="3" fill="rgba(255,255,255,.07)"/>
<!-- janela -->
<g transform="translate(650 500)">
 <rect x="-12" y="-12" width="344" height="444" rx="18" fill="#1E1E22" stroke="rgba(255,255,255,.08)"/>
 <rect id="sky" width="320" height="420" rx="10" fill="#5E7F9C"/>
 <g id="sun"><circle cx="232" cy="96" r="36" fill="#F3E3B0"/></g>
 <g id="stars" opacity="0" fill="#fff"><circle cx="60" cy="70" r="3"/><circle cx="200" cy="54" r="2.5"/><circle cx="280" cy="150" r="3"/><circle cx="110" cy="190" r="2"/><circle cx="36" cy="270" r="2.5"/></g>
 <g id="city" fill="#3E556B"><rect x="0" y="310" width="66" height="110"/><rect x="74" y="272" width="56" height="148"/><rect x="138" y="330" width="76" height="90"/><rect x="222" y="284" width="98" height="136"/></g>
 <g id="lights" opacity="0" fill="#10B981"><rect x="16" y="330" width="10" height="12"/><rect x="38" y="360" width="10" height="12"/><rect x="88" y="292" width="10" height="12"/><rect x="108" y="330" width="10" height="12"/><rect x="160" y="350" width="10" height="12"/><rect x="244" y="302" width="10" height="12"/><rect x="284" y="340" width="10" height="12"/><rect x="262" y="380" width="10" height="12"/></g>
 <rect x="153" width="14" height="420" fill="#1E1E22"/><rect y="203" width="320" height="14" fill="#1E1E22"/>
</g>
<!-- relógio -->
<g transform="translate(300 560)">
 <circle r="112" fill="#1E1E22" stroke="rgba(255,255,255,.1)" stroke-width="2"/><circle r="98" fill="#EDEDEF"/>
 <g id="ticks"></g>
 <g id="hh"><rect x="-7" y="-54" width="14" height="62" rx="7" fill="#0A0A0A"/></g>
 <g id="mm"><rect x="-5" y="-80" width="10" height="88" rx="5" fill="#0A0A0A"/></g>
 <circle r="9" fill="#10B981"/>
</g>
<!-- prateleira -->
<g transform="translate(50 860)">
 <rect x="18" y="-110" width="32" height="110" rx="5" fill="#10B981"/><rect x="54" y="-102" width="32" height="102" rx="5" fill="#2A2A2F"/>
 <rect x="90" y="-110" width="32" height="110" rx="5" fill="#3A3A40"/><rect x="126" y="-104" width="32" height="104" rx="5" fill="#0E9F6E"/>
 <rect y="0" width="200" height="14" rx="4" fill="#2A2A2F"/>
</g>
<!-- cadeira -->
<g fill="#26262B"><rect x="120" y="980" width="44" height="330" rx="20"/><rect x="130" y="1300" width="300" height="40" rx="18"/><rect x="268" y="1340" width="22" height="100"/><rect x="190" y="1432" width="180" height="14" rx="7"/></g>
<!-- personagem -->
<g id="A">
 <ellipse cx="0" cy="10" rx="150" ry="16" fill="#000" opacity=".5" filter="url(#soft)"/>
 <g id="Abody">
  <g id="Aarm2"><ellipse cx="0" cy="105" rx="40" ry="112" fill="#9AA3AB"/></g>
  <ellipse cx="0" cy="-190" rx="150" ry="192" fill="url(#gW)"/>
  <g id="Ahead">
   <circle cx="0" cy="-118" r="118" fill="url(#gW2)"/>
   <path d="M -100 -150 A 112 112 0 0 1 98 -160" fill="none" stroke="#10B981" stroke-width="16" stroke-linecap="round"/>
   <path d="M 6 -96 C 50 -40, 92 -40, 118 -58" fill="none" stroke="#10B981" stroke-width="9" stroke-linecap="round"/>
   <circle cx="121" cy="-60" r="13" fill="#0A0A0A"/>
   <ellipse cx="0" cy="-104" rx="34" ry="40" fill="#10B981"/><ellipse cx="-8" cy="-114" rx="12" ry="14" fill="#6EE7B7" opacity=".6"/>
  </g>
  <g id="Aarm1">
   <ellipse cx="0" cy="105" rx="42" ry="114" fill="url(#gW)"/>
   <g id="flag" opacity="0"><rect x="-5" y="-80" width="10" height="230" rx="5" fill="#EDEDEF"/>
     <path id="cloth" d="M 5 -60 C 60 -80, 100 -40, 150 -62 L 150 40 C 100 62, 60 22, 5 42 Z" fill="#FFFFFF" transform="translate(0 -12)"/></g>
  </g>
 </g>
</g>
<!-- mesa -->
<rect x="440" y="1250" width="660" height="30" rx="8" fill="#2A2A2F"/><rect x="440" y="1250" width="660" height="4" rx="2" fill="#10B981" opacity=".55"/>
<rect x="470" y="1280" width="20" height="160" fill="#1E1E22"/><rect x="1020" y="1280" width="20" height="160" fill="#1E1E22"/>
<ellipse id="mglow" cx="840" cy="1050" rx="240" ry="240" fill="url(#gScr)" opacity=".25"/>
<rect x="900" y="1130" width="18" height="120" fill="#1E1E22"/><rect x="852" y="1236" width="110" height="16" rx="6" fill="#1E1E22"/>
<path d="M 868 960 L 922 938 L 922 1162 L 868 1140 Z" fill="#1E1E22"/>
<path d="M 874 968 L 912 953 L 912 1146 L 874 1132 Z" fill="#0F2A22"/>
<g fill="#10B981"><path d="M 880 1100 l 6 -2 v 20 l -6 2z"/><path d="M 890 1092 l 6 -2 v 30 l -6 2z" opacity=".8"/><path d="M 900 1080 l 6 -2 v 44 l -6 2z"/></g>
<rect x="640" y="1236" width="150" height="16" rx="6" fill="#1E1E22"/>
<g transform="translate(990 1182)"><rect width="56" height="68" rx="10" fill="#EDEDEF"/><path d="M56 16 q30 4 0 36" fill="none" stroke="#EDEDEF" stroke-width="10"/><rect x="8" y="12" width="40" height="8" rx="4" fill="#10B981"/></g>
<g id="phone">
 <ellipse id="pglow" cx="40" cy="-6" rx="90" ry="64" fill="url(#gPh)" opacity="0"/>
 <rect x="0" y="-4" width="84" height="14" rx="6" fill="#0A0A0A" stroke="rgba(255,255,255,.15)"/>
 <rect id="pscr" x="6" y="-6" width="72" height="4" rx="2" fill="#2A2A2F"/>
 <g id="vib" opacity="0" stroke="#10B981" stroke-width="5" fill="none" stroke-linecap="round"><path d="M -14 -26 q -12 14 0 28"/><path d="M -32 -36 q -18 24 0 48"/><path d="M 98 -26 q 12 14 0 28"/><path d="M 116 -36 q 18 24 0 48"/></g>
</g>
<g id="speed" opacity="0" stroke="#10B981" stroke-width="6" stroke-linecap="round"><path d="M 600 1150 l 40 -30"/><path d="M 640 1170 l 50 -36"/><path d="M 700 1160 l 40 -30"/></g>
<rect id="night" x="0" y="400" width="1080" height="1100" fill="#000" opacity="0"/>
<ellipse id="mglow2" cx="800" cy="1080" rx="360" ry="320" fill="url(#gScr)" opacity="0" style="mix-blend-mode:screen"/>
</svg>
</div>
<div class="chip">HORA<b id="clk">17:55</b></div>
<div class="bal me" id="b1" style="left:400px;top:790px;--ox:30px;--oy:150px"><div class="box">17h55. Hoje eu saio<br>no horário ✨</div><div class="tail" style="left:44px;bottom:-14px"></div></div>
<div class="bal cli" id="b2" style="left:480px;top:880px;--ox:110px;--oy:200px"><div class="box"><div class="lab">CLIENTE · AGORA</div>É rapidinho!<br>1 minutinho 🙏</div><div class="tail" style="left:70px;bottom:-15px"></div></div>
<div class="bal me" id="b3" style="left:230px;top:820px;--ox:70px;--oy:120px"><div class="box" style="font-size:60px;padding:6px 34px 18px">…</div><div class="tail" style="left:50px;bottom:-14px"></div></div>
<div class="bal cli" id="b4" style="left:480px;top:860px;--ox:110px;--oy:220px"><div class="box"><div class="lab">CLIENTE · 21:41</div>E aquele outro<br>rapidinho? 🙏🙏</div><div class="tail" style="left:70px;bottom:-15px"></div></div>
<div class="foot"><span>PAINEL FISCAL</span><span>EPIVERSO</span></div>
<script>
const ease = { io: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2, l: t => t, o: t => 1 + 2.70158 * Math.pow(t - 1, 3) + 1.70158 * Math.pow(t - 1, 2) };
const TR = {}; function k(id, prop, arr){ (TR[id] = TR[id] || {})[prop] = arr; }
function val(arr, t){ if (t <= arr[0][0]) return arr[0][1];
  for (let i = 1; i < arr.length; i++) if (t <= arr[i][0]) { const [t0, v0] = arr[i - 1], [t1, v1, e] = arr[i]; const p = (ease[e || 'io'])((t - t0) / (t1 - t0));
    return typeof v0 === 'number' ? v0 + (v1 - v0) * p : lerpc(v0, v1, p); } return arr[arr.length - 1][1]; }
function lerpc(a, b, p){ const A = parseInt(a.slice(1), 16), B = parseInt(b.slice(1), 16);
  return '#' + [16, 8, 0].map(s => Math.round(((A >> s) & 255) + (((B >> s) & 255) - ((A >> s) & 255)) * p).toString(16).padStart(2, '0')).join(''); }
let tk = ''; for (let i = 0; i < 12; i++) tk += `<rect x="-4" y="-92" width="8" height="${i % 3 ? 12 : 20}" rx="3" fill="#0A0A0A" transform="rotate(${i * 30})"/>`;
document.getElementById('ticks').innerHTML = tk;
const BASE = { A: [300, 1300], Abody: [0, 0], Ahead: [0, -330], Aarm1: [26, -300], Aarm2: [-20, -300], phone: [540, 1238], hh: [0, 0], mm: [0, 0] };
const POPS = [['b1', 1.45, 3.45], ['b2', 4.35, 6.6], ['b3', 6.7, 7.6], ['b4', 11.1, 13.4]];
function apply(t){
  for (const id in BASE) if (!TR[id]) document.getElementById(id).setAttribute('transform', `translate(${BASE[id][0]} ${BASE[id][1]})`);
  for (const id in TR) { const el = document.getElementById(id), P = TR[id], b = BASE[id] || [0, 0], g = p => P[p] ? val(P[p], t) : null;
    if (P.fill) el.setAttribute('fill', g('fill')); if (P.op) el.setAttribute('opacity', g('op'));
    if (P.x || P.y || P.r || P.sx || P.sy) el.setAttribute('transform', `translate(${b[0] + (g('x') || 0)} ${b[1] + (g('y') || 0)}) rotate(${g('r') || 0}) scale(${P.sx ? g('sx') : 1} ${P.sy ? g('sy') : 1})`); }
  for (const [id, t0, t1] of POPS) { const el = document.getElementById(id); let s = .6, o = 0;
    if (t >= t0 && t <= t1) { const a = Math.min(1, (t - t0) / .25), z = Math.min(1, (t1 - t) / .18); s = (.6 + .4 * ease.o(a)) * (.9 + .1 * z); o = Math.min(1, a * 2) * z; }
    el.style.opacity = o; el.style.transform = `scale(${s})`; }
  const m = Math.round(val(TR.mm.r, t) / 6), hh = Math.floor(m / 60) % 24, mm = m % 60;
  document.getElementById('clk').textContent = String(hh).padStart(2, '0') + ':' + String(mm).padStart(2, '0');
}
// ---------- linha do tempo (s)
const TY = -72, UP = -172, a1 = [[0, TY]], a2 = [[0, TY + 6]];
function typing(t0, t1, st, amp){ for (let t = t0, i = 0; t <= t1; t += st, i++) { a1.push([t, TY + (i % 2 ? amp : -amp)]); a2.push([t, TY + 6 + (i % 2 ? -amp : amp)]); } }
typing(.1, 1.3, .16, 6); a1.push([1.5, TY]); a2.push([1.5, TY + 6]);
a1.push([3.5, TY]); a2.push([3.5, TY + 6]); a1.push([3.95, UP, 'o']); a2.push([3.95, UP + 8, 'o']);
a1.push([5.6, UP]); a2.push([5.6, UP + 8]); a1.push([6.4, -130]); a2.push([6.4, -124]); a1.push([6.9, TY]); a2.push([6.9, TY + 6]);
typing(7.7, 10.1, .066, 11); a1.push([10.35, -60]); a2.push([10.35, -54]); a1.push([10.8, -30]); a2.push([10.8, -24]);
a1.push([11.9, -30]); a1.push([12.25, -175, 'o']); for (let t = 12.45, i = 0; t < 14; t += .22, i++) a1.push([t, -175 + (i % 2 ? 12 : -12)]); a2.push([14, -24]);
k('Aarm1', 'r', a1); k('Aarm2', 'r', a2);
k('Ahead', 'r', [[0, 4], [1.3, 4], [1.6, -22], [3.3, -22], [3.55, 0], [3.95, -10, 'o'], [5.6, -10], [6.3, 22], [6.9, 10], [10.1, 12], [10.35, 14], [10.8, 48, 'o'], [14, 48]]);
k('Ahead', 'x', [[0, 0], [10.35, 0], [10.8, 30], [14, 30]]);
k('Abody', 'sx', [[0, 1], [3.5, 1], [3.95, .93, 'o'], [5.6, .93], [6.5, 1], [10.35, 1], [10.8, 1.1, 'o'], [14, 1.1]]);
k('Abody', 'sy', [[0, 1], [1.3, 1], [1.6, 1.02], [3.5, 1.02], [3.95, 1.09, 'o'], [5.6, 1.09], [6.5, 1], [10.35, 1], [10.8, .86, 'o'], [14, .86]]);
k('Abody', 'r', [[0, 0], [10.35, 0], [10.8, 16], [14, 16]]);
const by = [[0, 0]]; for (let t = .2, i = 0; t < 1.3; t += .32, i++) by.push([t, i % 2 ? -4 : 0]); by.push([7.7, 0]);
for (let t = 7.75, i = 0; t < 10.1; t += .066, i++) by.push([t, i % 2 ? -7 : 0]); by.push([10.2, 0]); k('Abody', 'y', by);
const px = [[0, 0]], vib = [[0, 0]], pg = [[0, 0]], ps = [[0, '#2A2A2F']];
function buzz(t0, t1){ px.push([t0 - .01, 0]); vib.push([t0 - .01, 0]); pg.push([t0 - .01, 0]); ps.push([t0 - .01, '#2A2A2F']);
  for (let t = t0, i = 0; t <= t1; t += .045, i++) px.push([t, i % 2 ? 7 : -7, 'l']);
  px.push([t1 + .05, 0]); vib.push([t0, 1, 'l'], [t1, 1], [t1 + .1, 0]); pg.push([t0, 1, 'l'], [t1 + .6, .5], [t1 + 1.2, 0]); ps.push([t0, '#34D399', 'l'], [t1 + 1.2, '#34D399'], [t1 + 1.4, '#2A2A2F']); }
buzz(4.1, 5.0); buzz(10.9, 11.6);
k('phone', 'x', px); k('vib', 'op', vib); k('pglow', 'op', pg); k('pscr', 'fill', ps);
const m0 = 17 * 60 + 55, m1 = 21 * 60 + 40;
k('mm', 'r', [[0, m0 * 6], [7.7, m0 * 6], [10.1, m1 * 6]]); k('hh', 'r', [[0, m0 * .5], [7.7, m0 * .5], [10.1, m1 * .5]]);
k('sky', 'fill', [[0, '#5E7F9C'], [7.7, '#5E7F9C'], [9.0, '#B07A5A'], [10.1, '#0E1830']]);
k('sun', 'op', [[0, 1], [7.7, 1], [9.2, 0]]); k('stars', 'op', [[0, 0], [9.4, 0], [10.1, 1]]); k('lights', 'op', [[0, 0], [9.2, 0], [10.0, 1]]);
k('city', 'fill', [[0, '#3E556B'], [7.7, '#3E556B'], [10.1, '#0A0F1C']]);
k('night', 'op', [[0, 0], [7.7, 0], [10.1, .22]]); k('mglow2', 'op', [[0, 0], [8.0, 0], [10.1, .8]]); k('mglow', 'op', [[0, .25], [7.7, .25], [10.1, .6]]);
k('speed', 'op', [[0, 0], [7.75, 0], [7.85, 1], [10.05, 1], [10.15, 0]]);
k('flag', 'op', [[0, 0], [11.85, 0], [11.95, 1], [14, 1]]);
const cl = [[0, 1]]; for (let t = 12.0, i = 0; t < 14; t += .18, i++) cl.push([t, i % 2 ? 1.08 : .94]); k('cloth', 'sy', cl);
window.__t = ms => apply(ms / 1000); apply(0);
</script></body></html>"""
out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/ep01b.html'
open(out, 'w').write(HTML); print(out, DUR)
