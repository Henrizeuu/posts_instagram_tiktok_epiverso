"""Escritório sem falas · ep. 01 · "é rapidinho" (2D, SVG + timeline JS, renderizado quadro a quadro)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/build')
from kit import FONTS
DUR = 11.6
HTML = r"""<!doctype html><html><head><meta charset='utf-8'><style>""" + FONTS + r"""
*{margin:0;padding:0} html,body{width:1080px;height:1920px;overflow:hidden;background:#000}
.hook{position:absolute;left:70px;right:150px;top:230px;text-align:center;font-family:TT;font-weight:700;line-height:1.45}
.hook span{background:#fff;color:#111;padding:8px 20px;border-radius:14px;font-size:58px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
</style></head><body>
<svg id="s" width="1080" height="1920" viewBox="40 60 1000 1778" xmlns="http://www.w3.org/2000/svg">
<defs>
 <radialGradient id="gW" cx="35%" cy="28%" r="80%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#EEF1F3"/><stop offset="1" stop-color="#C5CCD2"/></radialGradient>
 <radialGradient id="gW2" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".6" stop-color="#E9EDF0"/><stop offset="1" stop-color="#BFC7CE"/></radialGradient>
 <linearGradient id="gWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B7C2BC"/><stop offset="1" stop-color="#A6B2AB"/></linearGradient>
 <linearGradient id="gFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9C9286"/><stop offset="1" stop-color="#857B70"/></linearGradient>
 <linearGradient id="gDesk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2C9A4"/><stop offset="1" stop-color="#C8A97F"/></linearGradient>
 <radialGradient id="gGlow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#BFD8FF" stop-opacity=".9"/><stop offset="1" stop-color="#BFD8FF" stop-opacity="0"/></radialGradient>
 <radialGradient id="gPh" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".95"/><stop offset="1" stop-color="#DDF7EC" stop-opacity="0"/></radialGradient>
 <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="10"/></filter>
</defs>
<!-- parede, rodapé, chão -->
<rect width="1080" height="1500" fill="url(#gWall)"/>
<rect y="1480" width="1080" height="440" fill="url(#gFloor)"/>
<rect y="1468" width="1080" height="18" fill="#8E9A93"/>
<!-- janela -->
<g transform="translate(640 520)">
 <rect x="-14" y="-14" width="368" height="468" rx="10" fill="#2B3036"/>
 <rect id="sky" width="340" height="440" fill="#CFE6F7"/>
 <g id="sun"><circle cx="250" cy="110" r="42" fill="#FFF6D8"/></g>
 <g id="stars" opacity="0"><circle cx="70" cy="80" r="3" fill="#fff"/><circle cx="210" cy="60" r="2.5" fill="#fff"/><circle cx="290" cy="170" r="3" fill="#fff"/><circle cx="120" cy="210" r="2" fill="#fff"/><circle cx="40" cy="300" r="2.5" fill="#fff"/></g>
 <g id="city" fill="#7E93A6"><rect x="0" y="330" width="70" height="110"/><rect x="80" y="290" width="60" height="150"/><rect x="150" y="350" width="80" height="90"/><rect x="240" y="300" width="100" height="140"/></g>
 <g id="lights" opacity="0" fill="#FFD77A"><rect x="18" y="350" width="10" height="12"/><rect x="40" y="380" width="10" height="12"/><rect x="95" y="310" width="10" height="12"/><rect x="115" y="350" width="10" height="12"/><rect x="170" y="370" width="10" height="12"/><rect x="260" y="320" width="10" height="12"/><rect x="300" y="360" width="10" height="12"/><rect x="280" y="400" width="10" height="12"/></g>
 <rect x="163" width="14" height="440" fill="#2B3036"/><rect y="213" width="340" height="14" fill="#2B3036"/>
 <rect x="-30" y="452" width="400" height="20" rx="4" fill="#2B3036"/>
</g>
<!-- relógio -->
<g transform="translate(330 470)">
 <circle r="118" fill="#2B3036"/><circle r="104" fill="#F7F7F4"/>
 <g id="ticks"></g>
 <g id="hh"><rect x="-7" y="-58" width="14" height="66" rx="7" fill="#2B3036"/></g>
 <g id="mm"><rect x="-5" y="-86" width="10" height="94" rx="5" fill="#2B3036"/></g>
 <circle r="9" fill="#10B981"/>
</g>
<!-- prateleira -->
<g transform="translate(60 830)">
 <rect x="22" y="-118" width="34" height="118" rx="5" fill="#10B981"/><rect x="60" y="-110" width="34" height="110" rx="5" fill="#2B3036"/>
 <rect x="98" y="-118" width="34" height="118" rx="5" fill="#3A4047"/><rect x="136" y="-112" width="34" height="112" rx="5" fill="#10B981"/>
 <path d="M200 -10 h60 l-8 -56 h-44z" fill="#C98A64"/><circle cx="230" cy="-86" r="34" fill="#2F7A4E"/><circle cx="210" cy="-100" r="22" fill="#3B8F5D"/>
 <rect y="0" width="300" height="18" rx="4" fill="#C8A97F"/>
</g>
<!-- cadeira (atrás do boneco) -->
<g>
 <rect x="120" y="980" width="44" height="330" rx="20" fill="#2B3036"/>
 <rect x="130" y="1300" width="300" height="40" rx="18" fill="#2B3036"/>
 <rect x="268" y="1340" width="22" height="120" fill="#3A4047"/>
 <rect x="190" y="1452" width="180" height="16" rx="8" fill="#3A4047"/>
</g>
<!-- personagem A (base no assento) -->
<g id="A">
 <ellipse cx="0" cy="8" rx="150" ry="16" fill="#000" opacity=".18" filter="url(#soft)"/>
 <g id="Abody">
  <g id="Aarm2"><ellipse cx="0" cy="105" rx="40" ry="112" fill="#C8CFD5"/></g>
  <ellipse cx="0" cy="-190" rx="150" ry="192" fill="url(#gW)" stroke="#AEB7BF" stroke-width="2"/>
  <g id="Ahead">
   <circle cx="0" cy="-118" r="118" fill="url(#gW2)" stroke="#AEB7BF" stroke-width="2"/>
   <path d="M -100 -150 A 112 112 0 0 1 98 -160" fill="none" stroke="#10B981" stroke-width="16" stroke-linecap="round"/>
   <path d="M 6 -96 C 50 -40, 92 -40, 118 -58" fill="none" stroke="#10B981" stroke-width="9" stroke-linecap="round"/>
   <circle cx="121" cy="-60" r="13" fill="#2B3036"/>
   <ellipse cx="0" cy="-104" rx="34" ry="40" fill="#10B981"/><ellipse cx="-8" cy="-114" rx="12" ry="14" fill="#5FD3A9" opacity=".7"/>
  </g>
  <g id="Aarm1">
   <ellipse cx="0" cy="105" rx="42" ry="114" fill="url(#gW)" stroke="#AEB7BF" stroke-width="2"/>
   <g id="flag" opacity="0"><rect x="-5" y="150" width="10" height="230" rx="5" fill="#2B3036" transform="rotate(180 0 150)"/>
     <path id="cloth" d="M 5 -60 C 60 -80, 100 -40, 150 -62 L 150 40 C 100 62, 60 22, 5 42 Z" fill="#FFFFFF" stroke="#2B3036" stroke-width="4" transform="translate(0 -12)"/></g>
  </g>
 </g>
</g>
<!-- mesa e objetos (na frente) -->
<g>
 <rect x="440" y="1250" width="660" height="34" rx="8" fill="url(#gDesk)"/>
 <rect x="470" y="1284" width="22" height="200" fill="#2B3036"/><rect x="1020" y="1284" width="22" height="200" fill="#2B3036"/>
 <!-- monitor (de lado, tela virada pro boneco) -->
 <ellipse id="mglow" cx="860" cy="1050" rx="230" ry="230" fill="url(#gGlow)" opacity=".15"/>
 <rect x="900" y="1130" width="18" height="120" fill="#2B3036"/><rect x="852" y="1236" width="110" height="16" rx="6" fill="#2B3036"/>
 <path d="M 870 960 L 920 940 L 920 1160 L 870 1140 Z" fill="#2B3036"/>
 <path id="scr" d="M 874 966 L 902 956 L 902 1144 L 874 1134 Z" fill="#DDEBFF"/>
 <!-- teclado, caneca -->
 <rect x="640" y="1236" width="150" height="16" rx="6" fill="#2B3036"/>
 <g transform="translate(990 1182)"><rect width="56" height="68" rx="10" fill="#F2F2EE"/><path d="M56 16 q30 4 0 36" fill="none" stroke="#F2F2EE" stroke-width="10"/><rect x="8" y="12" width="40" height="8" rx="4" fill="#10B981"/></g>
 <!-- celular -->
 <g id="phone" transform="translate(540 1238)">
  <ellipse id="pglow" cx="40" cy="0" rx="80" ry="60" fill="url(#gPh)" opacity="0"/>
  <rect x="0" y="-4" width="84" height="14" rx="6" fill="#1E2227"/>
  <rect id="pscr" x="6" y="-6" width="72" height="4" rx="2" fill="#3A4047"/>
  <g id="vib" opacity="0" stroke="#2B3036" stroke-width="5" fill="none" stroke-linecap="round">
   <path d="M -14 -26 q -12 14 0 28"/><path d="M -32 -36 q -18 24 0 48"/><path d="M 98 -26 q 12 14 0 28"/><path d="M 116 -36 q 18 24 0 48"/></g>
 </g>
 <g id="speed" opacity="0" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"><path d="M 600 1150 l 40 -30"/><path d="M 640 1170 l 50 -36"/><path d="M 700 1160 l 40 -30"/></g>
</g>
<!-- noite -->
<rect id="night" width="1080" height="1920" fill="#0B1838" opacity="0" style="mix-blend-mode:multiply"/>
<ellipse id="mglow2" cx="820" cy="1060" rx="330" ry="300" fill="url(#gGlow)" opacity="0" style="mix-blend-mode:screen"/>
<!-- balões -->
<g id="balloons"></g>
</svg>
<div class="hook" id="hook"><span>quando o cliente diz que "é rapidinho"</span></div>
<script>
// ------- glifos da "língua do escritório" (aleatórios, mas fixos por semente)
function rng(seed){ return () => (seed = (seed * 16807) % 2147483647) / 2147483647; }
function glyph(seed){
  const r = rng(seed * 97 + 13), w = 34, h = 46; let d = '';
  const base = Math.floor(r() * 3);
  if (base == 0) d += `M${8 + r() * 6} 6 L${8 + r() * 6} ${h - 6} `;
  else if (base == 1) d += `M6 ${h - 8} Q ${w / 2} ${4 + r() * 10} ${w - 6} ${h - 8} `;
  else d += `M${w / 2 - 11} ${h / 2} a11 11 0 1 0 22 0 a11 11 0 1 0 -22 0 `;
  const n = 1 + Math.floor(r() * 2);
  for (let i = 0; i < n; i++) {
    const t = Math.floor(r() * 4), y = 8 + r() * (h - 16);
    if (t == 0) d += `M6 ${y} L${w - 6} ${y - 6} `;
    else if (t == 1) d += `M${w - 9} ${y} a3 3 0 1 0 0.1 0 `;
    else if (t == 2) d += `M${w / 2} ${y} l 10 10 `;
    else d += `M6 ${y} c 7 -9, 13 9, 22 0 `;
  }
  return d;
}
function word(seed, n, x0, y0, col){
  let s = ''; for (let i = 0; i < n; i++) s += `<path d="${glyph(seed + i)}" transform="translate(${x0 + i * 40} ${y0})" fill="none" stroke="${col}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>`;
  return s;
}
// balão: id, centro (x,y), largura, altura, ponta (tx,ty), conteúdo
const BAL = [];
function balloon(id, x, y, w, h, tx, ty, inner, dark){
  const fill = dark ? '#1E2227' : '#FFFFFF', st = dark ? '#1E2227' : '#2B3036';
  const g = `<g id="${id}" opacity="0"><g class="in">
    <path d="M ${x - 30} ${y + h / 2 - 6} L ${tx} ${ty} L ${x + 20} ${y + h / 2 - 6} Z" fill="${fill}" stroke="${st}" stroke-width="5" stroke-linejoin="round"/>
    <rect x="${x - w / 2}" y="${y - h / 2}" width="${w}" height="${h}" rx="${h / 2.4}" fill="${fill}" stroke="${st}" stroke-width="5"/>
    <rect x="${x - 40}" y="${y + h / 2 - 12}" width="70" height="16" fill="${fill}"/>
    ${inner}</g></g>`;
  BAL.push(g); return id;
}
const E = (x, y, s, e) => `<text x="${x}" y="${y}" font-size="${s}" text-anchor="middle" dominant-baseline="central">${e}</text>`;
// A quer ir pra casa
balloon('b1', 330, 650, 300, 130, 300, 770, word(11, 3, 205, 618, '#2B3036') + E(375, 650, 64, '🏠') + E(440, 620, 34, '✨'));
// celular: "1 min? 🙏"
balloon('b2', 600, 1010, 420, 150, 585, 1215, word(41, 2, 420, 975, '#FFFFFF') + E(560, 1010, 64, '⏱️') + `<text x="640" y="1012" font-size="58" font-family="TT" font-weight="800" fill="#fff" text-anchor="middle" dominant-baseline="central">1'</text>` + E(730, 1010, 60, '🙏'), true);
// A: "…"
balloon('b3', 300, 690, 190, 110, 300, 790, `<circle cx="255" cy="690" r="11" fill="#2B3036"/><circle cx="300" cy="690" r="11" fill="#2B3036"/><circle cx="345" cy="690" r="11" fill="#2B3036"/>`);
// celular de novo: "1 min? 🙏🙏"
balloon('b4', 700, 790, 460, 150, 600, 1210, word(77, 3, 500, 755, '#FFFFFF') + E(680, 790, 64, '⏱️') + `<text x="760" y="792" font-size="58" font-family="TT" font-weight="800" fill="#fff" text-anchor="middle" dominant-baseline="central">1'</text>` + E(850, 790, 56, '🙏🙏'), true);
document.getElementById('balloons').innerHTML = BAL.join('');
// marcadores do relógio
let tk = ''; for (let i = 0; i < 12; i++) tk += `<rect x="-4" y="-98" width="8" height="${i % 3 ? 14 : 22}" rx="3" fill="#2B3036" transform="rotate(${i * 30})"/>`;
document.getElementById('ticks').innerHTML = tk;
// ------- motor de keyframes
const ease = { io: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2, l: t => t, o: t => 1 + 2.70158 * Math.pow(t - 1, 3) + 1.70158 * Math.pow(t - 1, 2), i: t => t * t * t };
const TR = {};
function k(id, prop, arr){ (TR[id] = TR[id] || {})[prop] = arr; }
function val(arr, t){
  if (t <= arr[0][0]) return arr[0][1];
  for (let i = 1; i < arr.length; i++) if (t <= arr[i][0]) {
    const [t0, v0] = arr[i - 1], [t1, v1, e] = arr[i]; const p = (ease[e || 'io'])((t - t0) / (t1 - t0));
    return typeof v0 === 'number' ? v0 + (v1 - v0) * p : lerpc(v0, v1, p);
  }
  return arr[arr.length - 1][1];
}
function lerpc(a, b, p){ const A = parseInt(a.slice(1), 16), B = parseInt(b.slice(1), 16);
  const c = [16, 8, 0].map(s => Math.round(((A >> s) & 255) + (((B >> s) & 255) - ((A >> s) & 255)) * p));
  return '#' + c.map(x => x.toString(16).padStart(2, '0')).join(''); }
const BASE = { A: [300, 1300], Abody: [0, 0], Ahead: [0, -330], Aarm1: [26, -300], Aarm2: [-20, -300], phone: [540, 1238], hh: [0, 0], mm: [0, 0] };
for (const id of ['b1', 'b2', 'b3', 'b4']) BASE[id] = [0, 0];
function apply(t){
  for (const id in BASE) if (!TR[id]) { const el = document.getElementById(id); if (el && el.tagName == 'g' && !id.startsWith('b')) el.setAttribute('transform', `translate(${BASE[id][0]} ${BASE[id][1]})`); }
  for (const id in TR) {
    const el = document.getElementById(id), P = TR[id], b = BASE[id] || [0, 0];
    const g = p => P[p] ? val(P[p], t) : null;
    if (P.fill) el.setAttribute('fill', g('fill'));
    if (P.op != null) el.setAttribute('opacity', g('op'));
    if (P.x || P.y || P.r || P.sx || P.sy) {
      const x = b[0] + (g('x') || 0), y = b[1] + (g('y') || 0), r = g('r') || 0, sx = P.sx ? g('sx') : 1, sy = P.sy ? g('sy') : 1;
      el.setAttribute('transform', `translate(${x} ${y}) rotate(${r}) scale(${sx} ${sy})`);
    }
  }
  // balões: pop de escala ao redor do próprio centro
  for (const [id, cx, cy, t0, t1] of POPS) {
    const el = document.getElementById(id), inn = el.querySelector('.in');
    let s = 0, o = 0;
    if (t >= t0 && t <= t1) { const a = Math.min(1, (t - t0) / .22), z = Math.min(1, (t1 - t) / .15); s = .55 + .45 * ease.o(a); o = Math.min(a * 2, 1) * z; s *= (.85 + .15 * z); }
    el.setAttribute('opacity', o); inn.setAttribute('transform', `translate(${cx} ${cy}) scale(${s}) translate(${-cx} ${-cy})`);
  }
  document.getElementById('hook').style.opacity = t < 2.9 ? 1 : 0;
}
const POPS = [['b1', 330, 700, 1.35, 2.75], ['b2', 590, 1080, 3.75, 5.55], ['b3', 300, 740, 5.0, 5.95], ['b4', 680, 860, 9.35, 10.9]];
// ------- timeline (segundos)
const ARM_TYPE = -72, ARM_UP = -172;
const a1 = [[0, ARM_TYPE]], a2 = [[0, ARM_TYPE + 6]];
function typing(t0, t1, step, amp){ for (let t = t0, i = 0; t <= t1; t += step, i++) { a1.push([t, ARM_TYPE + (i % 2 ? amp : -amp), 'io']); a2.push([t, ARM_TYPE + 6 + (i % 2 ? -amp : amp), 'io']); } }
typing(0.1, 1.2, .16, 6);
a1.push([1.45, ARM_TYPE]); a2.push([1.45, ARM_TYPE + 6]);
a1.push([2.8, ARM_TYPE]); a2.push([2.8, ARM_TYPE + 6]);
a1.push([3.25, ARM_UP, 'o']); a2.push([3.25, ARM_UP + 8, 'o']);
a1.push([4.55, ARM_UP]); a2.push([4.55, ARM_UP + 8]);           // congelado
a1.push([5.3, -130]); a2.push([5.3, -124]);
a1.push([5.8, ARM_TYPE]); a2.push([5.8, ARM_TYPE + 6]);
typing(5.9, 8.3, .066, 11);                                      // digitando desesperado
a1.push([8.55, -60]); a2.push([8.55, -54]);
a1.push([9.0, -30]); a2.push([9.0, -24]);                        // braços caem
a1.push([9.9, -30]); a1.push([10.25, -175, 'o']);                 // bandeira
for (let t = 10.45, i = 0; t < 11.6; t += .22, i++) a1.push([t, -175 + (i % 2 ? 12 : -12)]);
a2.push([11.6, -24]);
k('Aarm1', 'r', a1); k('Aarm2', 'r', a2);
k('Ahead', 'r', [[0, 4], [1.2, 4], [1.5, -22], [2.6, -22], [2.85, 0], [3.25, -10, 'o'], [4.55, -10], [5.1, 22], [5.8, 10], [8.3, 12], [8.55, 14], [9.0, 48, 'o'], [11.6, 48]]);
k('Ahead', 'x', [[0, 0], [8.55, 0], [9.0, 30], [11.6, 30]]);
k('Abody', 'sx', [[0, 1], [2.8, 1], [3.25, .93, 'o'], [4.55, .93], [5.4, 1], [8.55, 1], [9.0, 1.1, 'o'], [11.6, 1.1]]);
k('Abody', 'sy', [[0, 1], [1.2, 1], [1.5, 1.02], [2.8, 1.02], [3.25, 1.09, 'o'], [4.55, 1.09], [5.4, 1], [8.55, 1], [9.0, .86, 'o'], [11.6, .86]]);
k('Abody', 'r', [[0, 0], [8.55, 0], [9.0, 16], [11.6, 16]]);
// respiração / balanço digitando
const by = [[0, 0]]; for (let t = .2, i = 0; t < 1.2; t += .32, i++) by.push([t, i % 2 ? -4 : 0]);
by.push([5.9, 0]); for (let t = 5.95, i = 0; t < 8.3; t += .066, i++) by.push([t, i % 2 ? -7 : 0]); by.push([8.4, 0]);
k('Abody', 'y', by);
// celular vibra
const px = [[0, 0]], vib = [[0, 0]], pg = [[0, 0]], ps = [[0, '#3A4047']];
function buzz(t0, t1){ px.push([t0 - .01, 0]); vib.push([t0 - .01, 0]); pg.push([t0 - .01, 0]); ps.push([t0 - .01, '#3A4047']);
  for (let t = t0, i = 0; t <= t1; t += .045, i++) px.push([t, i % 2 ? 7 : -7, 'l']);
  px.push([t1 + .05, 0]); vib.push([t0, 1, 'l'], [t1, 1], [t1 + .1, 0]); pg.push([t0, 1, 'l'], [t1 + .6, .5], [t1 + 1.2, 0]); ps.push([t0, '#7CF0C3', 'l'], [t1 + 1.2, '#7CF0C3'], [t1 + 1.4, '#3A4047']); }
buzz(3.5, 4.4); buzz(9.15, 9.9);
k('phone', 'x', px); k('vib', 'op', vib); k('pglow', 'op', pg); k('pscr', 'fill', ps);
// relógio: 17h55 -> 21h40 durante o timelapse
const m0 = 17 * 60 + 55, m1 = 21 * 60 + 40;
k('mm', 'r', [[0, m0 * 6], [5.9, m0 * 6], [8.3, m1 * 6, 'io']]);
k('hh', 'r', [[0, m0 * .5], [5.9, m0 * .5], [8.3, m1 * .5, 'io']]);
// anoitecer
k('sky', 'fill', [[0, '#CFE6F7'], [5.9, '#CFE6F7'], [7.2, '#F2B58A'], [8.3, '#162447']]);
k('sun', 'op', [[0, 1], [5.9, 1], [7.4, 0]]); k('stars', 'op', [[0, 0], [7.6, 0], [8.3, 1]]); k('lights', 'op', [[0, 0], [7.4, 0], [8.2, 1]]);
k('city', 'fill', [[0, '#7E93A6'], [5.9, '#7E93A6'], [8.3, '#0D1428']]);
k('night', 'op', [[0, 0], [5.9, 0], [8.3, .36]]);
k('mglow2', 'op', [[0, 0], [6.2, 0], [8.3, .9]]); k('mglow', 'op', [[0, .15], [5.9, .15], [8.3, .5]]);
k('speed', 'op', [[0, 0], [5.95, 0], [6.05, 1], [8.25, 1], [8.35, 0]]);
k('flag', 'op', [[0, 0], [9.95, 0], [10.05, 1], [11.6, 1]]);
const cl = [[0, 0]]; for (let t = 10.1, i = 0; t < 11.6; t += .18, i++) cl.push([t, i % 2 ? 1.08 : .94]);
k('cloth', 'sy', cl);
window.__t = ms => apply(ms / 1000);
apply(0);
</script></body></html>"""
out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/ep01.html'
open(out, 'w').write(HTML); print(out, DUR)
