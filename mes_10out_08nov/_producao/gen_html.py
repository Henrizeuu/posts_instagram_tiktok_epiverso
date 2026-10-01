import json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/page2'
posts = json.load(open(D + '/posts.json'))
def mins(h):
    h = h.replace('h', ':'); a, b = (h.split(':') + ['0'])[:2]; return int(a) * 60 + int(b or 0)
posts.sort(key=lambda p: (p['date'], 0 if p['net'] == 'instagram' else 1, mins(p['hora'])))
data = json.dumps(posts, ensure_ascii=False).replace('</', '<\\/')
HTML = r"""<title>Epiverso · Mês de Conteúdo</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
/* Layout: agenda por semana; cada dia é uma linha com 1 post do Instagram + 3 do TikTok. Identidade Epiverso (escura, deliberadamente tema único). */
:root{--bg:#0A0A0A;--card:#121214;--line:rgba(255,255,255,.08);--fg:#F2F2F3;--mute:#8A8A92;--acc:#10B981;--tt:#FE2C55;--ig:#C13584;
 --display:'Inter',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font-family:var(--display);margin:0}
.wrap{max-width:1180px;margin:0 auto;padding-inline:20px;padding-block:40px 80px}
.k{font-family:var(--mono);font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:var(--acc)}
h1{font-size:clamp(34px,6vw,64px);letter-spacing:-.05em;line-height:.98;margin:14px 0 0;font-weight:800;text-wrap:balance}
h1 em{font-style:normal;color:var(--acc)}
.lead{color:#B4B4BC;font-size:17px;line-height:1.55;max-width:62ch;margin-top:16px}
.stats{display:flex;flex-wrap:wrap;gap:10px 28px;margin-top:26px;font-family:var(--mono);font-size:13px;color:var(--mute)}
.stats b{color:var(--fg);font-family:var(--display);font-size:22px;letter-spacing:-.03em;margin-right:6px}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:rgba(10,10,10,.92);backdrop-filter:blur(8px);margin:30px -20px 0;padding:12px 20px;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.chip{font:500 13px var(--display);color:var(--fg);background:transparent;border:1px solid var(--line);border-radius:999px;padding:7px 14px;cursor:pointer}
.chip[aria-pressed=true]{background:var(--acc);border-color:var(--acc);color:#04130D}
.chip:focus-visible,.card:focus-visible,.btn:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
.legend{margin-left:auto;display:flex;gap:14px;font-family:var(--mono);font-size:11px;color:var(--mute);letter-spacing:.08em}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;vertical-align:middle}
.week{margin-top:38px}
.week h2{font-family:var(--mono);font-weight:500;font-size:12px;letter-spacing:.3em;color:var(--mute);text-transform:uppercase;margin:0 0 6px;border-bottom:1px solid var(--line);padding-bottom:10px}
.day{display:grid;grid-template-columns:92px minmax(0,1.25fr) repeat(3,minmax(0,1fr));gap:14px;padding:16px 0;border-bottom:1px solid var(--line);align-items:start}
.date{font-variant-numeric:tabular-nums}
.date .d{font-size:30px;font-weight:800;letter-spacing:-.04em}
.date .w{font-family:var(--mono);font-size:12px;color:var(--mute);letter-spacing:.14em;text-transform:uppercase}
.date .hol{display:inline-block;margin-top:6px;font-family:var(--mono);font-size:10px;letter-spacing:.12em;color:#F59E0B;border:1px solid rgba(245,158,11,.4);border-radius:4px;padding:2px 5px}
.card{all:unset;cursor:pointer;display:flex;gap:10px;align-items:flex-start;min-width:0;border-radius:10px;padding:6px;margin:-6px}
.card:hover{background:var(--card)}
.card img{width:64px;flex:none;border-radius:6px;border:1px solid var(--line);object-fit:cover}
.card.ig img{width:84px;aspect-ratio:4/5}
.card.tt img{aspect-ratio:9/16}
.meta{min-width:0}
.meta .t{font-size:13.5px;font-weight:600;line-height:1.3;letter-spacing:-.01em;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.meta .h{font-family:var(--mono);font-size:11px;color:var(--mute);margin-top:6px;letter-spacing:.04em}
.tag{display:inline-block;font-family:var(--mono);font-size:10px;letter-spacing:.08em;padding:2px 6px;border-radius:4px;margin-right:4px;text-transform:uppercase}
.tag.ig{background:rgba(193,53,132,.16);color:#F08BC8}.tag.tt{background:rgba(254,44,85,.14);color:#FF8FA6}
.tag.f{background:rgba(255,255,255,.06);color:#C9CAD0}
.hide{display:none!important}
dialog{background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:16px;padding:0;width:min(980px,calc(100vw - 32px));max-height:calc(100vh - 40px)}
dialog::backdrop{background:rgba(0,0,0,.7)}
.dl{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:0}
.media{background:#000;display:flex;align-items:center;justify-content:center;padding:18px;min-height:320px}
.media video{max-height:72vh;max-width:100%;border-radius:8px}
.slides{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;max-width:100%}
.slides img{max-height:64vh;scroll-snap-align:center;border-radius:6px;flex:none;max-width:88%}
.info{padding:24px 26px;overflow:auto;max-height:calc(100vh - 42px)}
.info h3{margin:8px 0 4px;font-size:22px;letter-spacing:-.03em;line-height:1.15;text-wrap:balance}
.info .when{font-family:var(--mono);font-size:12px;color:var(--mute)}
.lab{font-family:var(--mono);font-size:11px;letter-spacing:.24em;color:var(--acc);text-transform:uppercase;margin-top:20px}
.box{white-space:pre-wrap;font-size:14.5px;line-height:1.55;background:#0D0D0F;border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-top:8px}
.small{font-size:13.5px;line-height:1.5;color:#C9CAD0;margin-top:6px}
.btn{font:600 13px var(--display);border:1px solid var(--acc);background:transparent;color:var(--acc);border-radius:8px;padding:8px 12px;cursor:pointer;margin-top:10px}
.x{position:absolute;right:12px;top:10px;background:rgba(0,0,0,.6);color:#fff;border:0;border-radius:999px;width:34px;height:34px;font-size:18px;cursor:pointer}
.path{font-family:var(--mono);font-size:12px;color:var(--mute);word-break:break-all;margin-top:6px}
@media (max-width:820px){
 .day{grid-template-columns:repeat(3,minmax(0,1fr));}
 .date{grid-column:1/-1;display:flex;gap:12px;align-items:baseline}
 .card.ig{grid-column:1/-1}
 .card{flex-direction:column}.card img,.card.ig img{width:100%}
 .card.ig{flex-direction:row}.card.ig img{width:96px}
 .legend{display:none}
 .dl{grid-template-columns:1fr}.info{max-height:none}
}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
</style>
<div class="wrap">
 <div class="k">Epiverso · Painel Fiscal</div>
 <h1>10 de outubro a 8 de novembro: <em>120 posts</em> prontos.</h1>
 <p class="lead">Um post por dia no Instagram, na identidade da marca, e três por dia no TikTok, no estilo nativo do app. Pessoas reais filmadas em escritório, telas do Painel com empresas fictícias. Toque em qualquer post para ver o vídeo ou as lâminas e copiar a legenda.</p>
 <div class="stats"><span><b>30</b>Instagram</span><span><b>90</b>TikTok</span><span><b>90</b>vídeos</span><span><b>23</b>carrosséis</span><span><b>7</b>estáticos</span></div>
 <div class="bar" role="toolbar" aria-label="Filtros">
  <button class="chip" data-f="all" aria-pressed="true">Tudo</button>
  <button class="chip" data-f="instagram" aria-pressed="false">Instagram</button>
  <button class="chip" data-f="tiktok" aria-pressed="false">TikTok</button>
  <button class="chip" data-f="serie" aria-pressed="false">Série “coisas que só…”</button>
  <button class="chip" data-f="reforma" aria-pressed="false">Reforma tributária</button>
  <button class="chip" data-f="dp" aria-pressed="false">Departamento pessoal</button>
  <span class="legend"><span><i class="dot" style="background:var(--ig)"></i>Instagram</span><span><i class="dot" style="background:var(--tt)"></i>TikTok</span></span>
 </div>
 <div id="cal"></div>
</div>
<dialog id="dlg" aria-label="Detalhes do post"><div style="position:relative"><button class="x" id="x" aria-label="Fechar">×</button><div class="dl"><div class="media" id="media"></div><div class="info" id="info"></div></div></div></dialog>
<script id="data" type="application/json">__DATA__</script>
<script>
const P = JSON.parse(document.getElementById('data').textContent);
const HOL = {'2026-10-12':'feriado','2026-11-02':'feriado'};
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const kindLabel = p => p.kind==='video' ? (p.net==='instagram'?'reels':'vídeo') : p.kind==='carrossel' ? 'carrossel' : 'estático';
const topics = p => { const t=(p.title+' '+p.tags+' '+p.leg).toLowerCase(); const a=[];
  if (/coisas que s[oó]/.test(t)) a.push('serie'); if (/reforma|ibs|cbs|cclasstrib|split|nfs-e|xml|cst/.test(t)) a.push('reforma');
  if (/13º|13o|esocial|férias|departamento pessoal|#departamentopessoal/.test(t)) a.push('dp'); return a; };
const byDay = {}; P.forEach((p,i)=>{p.i=i;p.top=topics(p);(byDay[p.date]=byDay[p.date]||[]).push(p)});
const days = Object.keys(byDay).sort();
const cal = document.getElementById('cal'); let html=''; let wk=-1;
days.forEach((d,n)=>{ const w=Math.floor(n/7); if(w!==wk){ if(wk>=0) html+='</section>'; wk=w;
   const a=days[w*7], b=days[Math.min(w*7+6,days.length-1)]; const f=x=>x.slice(8)+'/'+x.slice(5,7);
   html+=`<section class="week"><h2>Semana ${w+1} · ${f(a)} a ${f(b)}</h2>`; }
  const ps=byDay[d]; const dow=ps[0].dow;
  html+=`<div class="day" data-day="${d}"><div class="date"><div class="d">${d.slice(8)}/${d.slice(5,7)}</div><div class="w">${dow}</div>${HOL[d]?'<span class="hol">FERIADO</span>':''}</div>`;
  ps.forEach(p=>{ const c=p.net==='instagram'?'ig':'tt';
    html+=`<button class="card ${c}" data-i="${p.i}" data-net="${p.net}" data-top="${p.top.join(' ')}"><img src="${p.thumb}" alt="" loading="lazy"><span class="meta"><span class="tag ${c}">${c==='ig'?'IG':'TT'}</span><span class="tag f">${kindLabel(p)}</span><span class="t">${esc(p.title)}</span><span class="h">${esc(p.hora)}</span></span></button>`; });
  html+='</div>'; });
cal.innerHTML = html + '</section>';
document.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{ document.querySelectorAll('.chip').forEach(x=>x.setAttribute('aria-pressed', x===b)); const f=b.dataset.f;
  document.querySelectorAll('.card').forEach(c=>{ const ok = f==='all' || c.dataset.net===f || c.dataset.top.split(' ').includes(f); c.classList.toggle('hide', !ok); });
  document.querySelectorAll('.day').forEach(d=>d.classList.toggle('hide', !d.querySelector('.card:not(.hide)')));
  document.querySelectorAll('.week').forEach(w=>w.classList.toggle('hide', !w.querySelector('.day:not(.hide)')));
  try{localStorage.setItem('f',f)}catch(e){} });
const dlg=document.getElementById('dlg');
function copy(txt, btn){ const done=()=>{btn.textContent='Copiado'; setTimeout(()=>btn.textContent='Copiar legenda',1500)};
  if(navigator.clipboard) navigator.clipboard.writeText(txt).then(done, ()=>sel(btn)); else sel(btn); }
function sel(btn){ const r=document.createRange(); r.selectNodeContents(btn.previousElementSibling); const s=getSelection(); s.removeAllRanges(); s.addRange(r); btn.textContent='Selecionado: copie com Ctrl+C'; }
document.addEventListener('click', e=>{ const c=e.target.closest('.card'); if(!c) return; const p=P[+c.dataset.i];
  const m=document.getElementById('media');
  m.innerHTML = p.kind==='video' ? `<video src="${p.video}" controls playsinline preload="metadata" poster="${p.thumb}"></video>` : `<div class="slides">${p.slides.map(s=>`<img src="${s}" alt="">`).join('')}</div>`;
  const leg = p.leg+'\n\n'+p.tags;
  document.getElementById('info').innerHTML = `<span class="tag ${p.net==='instagram'?'ig':'tt'}">${p.net}</span><span class="tag f">${kindLabel(p)}</span>
   <h3>${esc(p.title)}</h3><div class="when">${p.dow} ${p.date.slice(8)}/${p.date.slice(5,7)} às ${esc(p.hora)} · ${esc(p.fmt)}</div>
   <div class="lab">Legenda</div><div class="box">${esc(leg)}</div><button class="btn" type="button">Copiar legenda</button>
   ${p.som?`<div class="lab">Som / música</div><div class="small">${esc(p.som)}</div>`:''}
   ${p.rot?`<div class="lab">Para a equipe regravar</div><div class="small">${esc(p.rot)}</div>`:''}
   ${p.kind==='video'&&p.net==='tiktok'?'<div class="small" style="color:var(--mute)">A prévia aqui é comprimida. O arquivo final em alta está na pasta abaixo.</div>':''}
   <div class="lab">Pasta no repositório</div><div class="path">mes_10out_08nov/${esc(p.folder)}/</div>`;
  document.querySelector('#info .btn').onclick=ev=>copy(leg, ev.target);
  dlg.showModal(); });
document.getElementById('x').onclick=()=>dlg.close();
dlg.addEventListener('close',()=>{ const v=dlg.querySelector('video'); if(v) v.pause(); });
dlg.addEventListener('click',e=>{ if(e.target===dlg) dlg.close(); });
try{ const f=localStorage.getItem('f'); if(f) document.querySelector(`.chip[data-f="${f}"]`)?.click(); }catch(e){}
</script>
"""
open(D + '/index.html', 'w').write(HTML.replace('__DATA__', data))
print(os.path.getsize(D + '/index.html') // 1024, 'KB')
