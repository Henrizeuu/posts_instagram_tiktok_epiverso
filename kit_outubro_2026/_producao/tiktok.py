import sys, json
from vid import *
from anim import *
OUT = S + '/out/tiktok'
TMP = S + '/build/tmp'; os.makedirs(TMP, exist_ok=True)
# TikTok-native text: TikTok Sans, classic white box / outlined text. Safe zone: x 70..930, y 180..1440
TT_CSS = ANIM_CSS + """
.tt{font-family:TT;font-weight:700;letter-spacing:-.01em;line-height:1.18}
.box{display:inline;background:#fff;color:#111;padding:8px 18px;border-radius:14px;box-decoration-break:clone;-webkit-box-decoration-break:clone;font-size:60px}
.stroke{color:#fff;font-size:66px;text-shadow:0 0 2px #000,0 0 2px #000,3px 3px 0 #000,-3px 3px 0 #000,3px -3px 0 #000,-3px -3px 0 #000,0 4px 14px rgba(0,0,0,.6)}
.yel{color:#FFE14D}
@keyframes punch{0%{transform:scale(1.18)}100%{transform:scale(1.0)}}
@keyframes flash{0%{opacity:.9}100%{opacity:0}}
"""
def ph(name, t0, dur, pos='center', anim='kb', filt='saturate(1.02) contrast(1.03)'):
    return kb_photo(name, t0, dur, pos, anim, filt)
def txt(html_, t, top=230, cls='box', anim='pop', size=None, align='center'):
    st = f"font-size:{size}px;" if size else ''
    return (f"<div class='tt' style='position:absolute;left:70px;right:150px;top:{top}px;text-align:{align};{A(anim,t,.35)}'>"
            f"<span class='{cls}' style='{st}'>{html_}</span></div>")

def stage(scenes): return "<div class='stage' style='background:#000'>" + ''.join(scenes) + "</div>"

# ---------------------------------------------------------------- TT01: POV dia 19
def tt1():
    cuts = [0, 2.3, 4.5, 6.7, 9.6]
    sc = []
    sc.append(scene(0, cuts[1], ph('julia_sobrecarregada', 0, 2.6, 'center 40%', 'punch') + txt('POV: dia 19 no escritório contábil 🫠', .05) , fade_in=.01, fade_out=.01))
    sc.append(scene(cuts[1], cuts[2], ph('julia_telefones', cuts[1], 2.5, 'center 35%', 'punch') + txt('cliente 1, cliente 2, cliente 3, cliente 4…', cuts[1]+.05), fade_in=.01, fade_out=.01))
    sc.append(scene(cuts[2], cuts[3], ph('julia_monitor', cuts[2], 2.5, 'center 35%', 'punch') + txt('o portal fora do ar às 17h59', cuts[2]+.05), fade_in=.01, fade_out=.01))
    sc.append(scene(cuts[3], cuts[4], ph('escritorio_meianoite', cuts[3], 3.2, 'center', 'kb', 'brightness(.75) saturate(1.1)') +
        f"<div style='position:absolute;inset:0;background:#fff;{A('flash',cuts[3],.35)}'></div>" +
        txt('enquanto isso, no escritório que tem robô:', cuts[3]+.1) +
        txt('00:00 · baixando 1.284 XMLs sozinho 🤖', cuts[3]+1.0, top=1180, cls='stroke', size=58), fade_in=.01, fade_out=.01))
    anim_clip(stage(sc), f'{TMP}/tt1_v.mp4', cuts[-1], TT_CSS)
    os.makedirs(OUT+'/01_video_pov_dia_19', exist_ok=True)
    mix(f'{TMP}/tt1_v.mp4', OUT+'/01_video_pov_dia_19/video.mp4',
        sfx=[('impact',0,.4),('notify',0.6,.25),('impact',2.3,.35),('notify',2.5,.3),('notify',3.0,.3),('notify',3.5,.3),('impact',4.5,.35),('click',4.9,.3),('click',5.2,.3),('whoosh',6.6,.35),('ding',7.8,.3)])

# ---------------------------------------------------------------- TT02: carrossel photo mode
def tt2():
    os.makedirs(OUT+'/02_carrossel_coisas_que_so_contador_entende', exist_ok=True)
    slides = [
      ('julia_selfie', 'center 30%', 'coisas que só quem trabalha em escritório contábil entende 🫠', 'parte 1'),
      ('nota_amassada', 'center', 'o cliente mandando a nota fiscal assim:', ''),
      ('julia_sorriso_forcado', 'center 30%', 'o cliente: “é rapidinho”', 'eu:'),
      ('julia_monitor', 'center 35%', 'o portal fora do ar às 17h59 do último dia', ''),
      ('julia_choque', 'center 30%', 'quando a nota cancelada entrou na apuração', ''),
      ('julia_telefones', 'center 35%', 'dia 19. todo mês. sem exceção.', ''),
      ('ana_saindo', 'center 25%', 'e a colega que automatizou o download de XML indo embora às 18h', '🙂'),
    ]
    for i, (img, pos, t, t2) in enumerate(slides, 1):
        extra = f"<div class='tt' style='position:absolute;left:70px;right:150px;top:1250px;text-align:center'><span class='stroke' style='font-size:72px'>{t2}</span></div>" if t2 else ''
        body = f"<div class='stage' style='background:#000'><img src='file://{AI}{img}.webp' style='position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos}'>" \
               f"<div class='tt' style='position:absolute;left:70px;right:150px;top:260px;text-align:center'><span class='box' style='font-size:62px'>{t}</span></div>{extra}</div>"
        render(body, f'{OUT}/02_carrossel_coisas_que_so_contador_entende/{i:02d}.jpg', 1080, 1920, css=TT_CSS)

# ---------------------------------------------------------------- TT04: eu em 2025 vs 2026
def tt4():
    sc = []
    sc.append(scene(0, 4.4, ph('ana_2025', 0, 4.6, 'center 35%', 'kb', 'saturate(.8) contrast(1.05) brightness(.95)') +
        txt('eu em 2025, 23h, baixando XML cliente por cliente', .1) +
        txt('(sim, de novo)', 2.0, top=1230, cls='box', size=56), fade_in=.01, fade_out=.01))
    sc.append(scene(4.4, 9.4, ph('ana_sofa', 4.4, 5.2, 'center 30%', 'kbl') +
        f"<div style='position:absolute;inset:0;background:#fff;{A('flash',4.4,.4)}'></div>" +
        txt('eu em 2026:', 4.5) +
        txt('o robô baixa tudo à meia-noite e eu nem lembro que XML existe', 5.6, top=1180, cls='box', size=56), fade_in=.01, fade_out=.01))
    anim_clip(stage(sc), f'{TMP}/tt4_v.mp4', 9.4, TT_CSS)
    os.makedirs(OUT+'/04_video_eu_2025_vs_2026', exist_ok=True)
    mix(f'{TMP}/tt4_v.mp4', OUT+'/04_video_eu_2025_vs_2026/video.mp4',
        sfx=[('typing',0.3,.35),('click',1.9,.3),('riser',3.2,.3),('impact',4.4,.45),('pop',5.6,.3)])

# ---------------------------------------------------------------- TT05: respondendo comentário
def tt5():
    reel = S + '/src/08_reels_encontre_qualquer_nota/reels.mp4'
    comment = f"""<div class='tt' style='position:absolute;left:70px;top:300px;max-width:760px;{A('pop',.1,.4)}'>
      <div style='background:#fff;color:#111;border-radius:22px;padding:22px 28px;box-shadow:0 10px 40px rgba(0,0,0,.35)'>
        <div style='font-size:30px;font-weight:600;color:#666'>Responder ao comentário de contabil.rs</div>
        <div style='font-size:46px;margin-top:8px'>mas quanto tempo vc leva pra achar UMA nota? 🤔</div></div></div>"""
    a = stage([scene(0, 2.8, ph('julia_selfie', 0, 3.0, 'center 30%', 'kb') + comment +
        txt('deixa eu te mostrar 👇', 1.2, top=1250, cls='stroke', size=66), fade_in=.01, fade_out=.01)])
    anim_clip(a, f'{TMP}/tt5_a.mp4', 2.8, TT_CSS)
    # footage segments with TikTok captions on the empty lower half
    segs = [(3.6, 4.2, 'digita o número…'), (8.7, 2.2, 'o PDF abre na hora'), (12.0, 1.7, 'o mês inteiro? um clique')]
    parts = [f'{TMP}/tt5_a.mp4']
    for k, (st, du, cap) in enumerate(segs):
        render(f"<div class='tt' style='position:absolute;left:70px;right:150px;top:1480px;text-align:center'><span class='box' style='font-size:62px'>{cap}</span></div>",
               f'{TMP}/tt5_cap{k}.png', 1080, 1920, css=TT_CSS + 'html,body,.stage{background:transparent!important}', transparent=True)
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(st),'-i',reel,'-loop','1','-i',f'{TMP}/tt5_cap{k}.png','-t',str(du),
            '-filter_complex','[0:v][1:v]overlay=0:0:shortest=1,fps=30','-an','-c:v','libx264','-pix_fmt','yuv420p','-crf','16',f'{TMP}/tt5_s{k}.mp4'], check=True)
        parts.append(f'{TMP}/tt5_s{k}.mp4')
    e = stage([scene(0, 2.4, ph('julia_selfie', 0, 2.6, 'center 30%', 'kbl') +
        txt('4 segundos. <span style="color:#10B981">sem portal, sem pasta.</span>', .05) +
        txt('o sistema tá no perfil 🫶', .8, top=1250, cls='stroke', size=60), fade_in=.01, fade_out=.01)])
    anim_clip(e, f'{TMP}/tt5_e.mp4', 2.4, TT_CSS); parts.append(f'{TMP}/tt5_e.mp4')
    concat(parts, f'{TMP}/tt5_v.mp4')
    os.makedirs(OUT+'/05_video_respondendo_comentario', exist_ok=True)
    mix(f'{TMP}/tt5_v.mp4', OUT+'/05_video_respondendo_comentario/video.mp4',
        sfx=[('pop',0.1,.35),('whoosh',2.75,.3),('typing',3.0,.45),('click',6.1,.35),('whoosh',6.95,.3),('ding',7.1,.3),('whoosh',9.15,.3),('click',10.0,.35),('ding',10.4,.3),('whoosh',10.85,.3)])


# ---------------------------------------------------------------- TT03: explicativo NFS-e (voz + legenda palavra a palavra)
def tt3():
    d = json.load(open(TMP + '/tt3_words.json')); W = d['words']; END = round(d['dur'] + 0.9, 2)
    # caption chunks of up to 3 words (break after punctuation)
    chunks, cur = [], []
    for w in W:
        cur.append(w)
        if len(cur) == 3 or w[0][-1] in '.:,?':
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    js_chunks = json.dumps([[[w, a, b] for w, a, b in c] for c in chunks], ensure_ascii=False)
    FA = sorted(os.listdir(TMP + '/foot')); fa = [f for f in FA if f.startswith('a')]; fb = [f for f in FA if f.startswith('b')]
    foot_js = json.dumps([f'file://{TMP}/foot/{f}' for f in fa + fb])
    T0, T1 = 42.4, 42.4 + (len(fa) + len(fb)) / 30  # real footage window
    def stat(lbl, val, t):
        return f"<div class='tt' style='display:flex;justify-content:space-between;align-items:center;background:#fff;color:#111;border-radius:26px;padding:22px 36px;margin-top:24px;{A('pop',t,.35)}'><span style='font-size:50px'>{lbl}</span><span style='font-size:96px;font-weight:900'>{val}</span></div>"
    sc = [
      scene(0, 5.0, ph('julia_selfie', 0, 5.2, 'center 30%', 'kb') + txt('mudou a NFS-e e quase ninguém tá falando disso ⚠️', .05, top=220), fade_in=.01, fade_out=.01),
      scene(5.0, 12.7, f"<div style='position:absolute;inset:0;background:#0A0A0A'></div><div style='position:absolute;left:0;right:0;top:170px;height:900px;overflow:hidden;animation:kb 16s linear 5s both;transform-origin:50% 60%'><img src='file://{AI}danfe_still.jpg' style='position:absolute;left:0;top:-480px;width:1080px;height:1920px'></div>" + txt('é assim que o quadro IBS/CBS aparece no PDF', 5.1, top=1130), fade_in=.01, fade_out=.01),
      scene(12.7, 23.0, ph('broll_maos', 12.7, 10.5, 'center', 'kb', 'blur(6px) brightness(.55)') + txt('calma: é só teste 🧘‍♀️', 12.8, top=220) +
         f"<div style='position:absolute;left:90px;right:170px;top:520px'>{stat('CBS', '0,9%', 15.2)}{stat('IBS', '0,1%', 18.4)}{stat('aumento de imposto', '0 ✅', 20.6)}</div>", fade_in=.01, fade_out=.01),
      scene(23.0, 25.1, ph('julia_selfie', 23.0, 2.4, 'center 30%', 'punch') + txt('3 coisas pra fazer agora 👇', 23.05, top=220), fade_in=.01, fade_out=.01),
      scene(25.1, 30.1, ph('broll_maos', 25.1, 5.3, 'center', 'kb', 'blur(6px) brightness(.5)') + txt('1. confere o XML das notas de serviço', 25.15, top=220) +
         f"""<div class='mono' style='position:absolute;left:90px;right:170px;top:560px;background:#0E0E10;border:2px solid #10B981;border-radius:26px;padding:36px 40px;font-size:40px;line-height:1.6;color:#E5E5E8;{A('pop',25.6,.4)}'>
           <span style='color:#10B981'>&lt;IBSCBS&gt;</span><br>&nbsp;&nbsp;&lt;CST&gt;000&lt;/CST&gt;<br>&nbsp;&nbsp;&lt;cClassTrib&gt;…&lt;/cClassTrib&gt;<br>&nbsp;&nbsp;&lt;vBC&gt;…&lt;/vBC&gt;<br><span style='color:#10B981'>&lt;/IBSCBS&gt;</span></div>
           <div class='tt' style='position:absolute;left:90px;right:170px;top:1000px;text-align:center;{A('pop',27.6,.35)}'><span class='box' style='font-size:50px'>tá vindo? ✅ não tá? cobra o emissor</span></div>""", fade_in=.01, fade_out=.01),
      scene(30.1, 36.5, ph('julia_telefones', 30.1, 6.6, 'center 35%', 'kb') + txt('2. avisa os clientes: o PDF da nota vai mudar', 30.15, top=220), fade_in=.01, fade_out=.01),
      scene(36.5, T0, ph('marcos_calendario', 36.5, 6.2, 'center 30%', 'kb') + txt('3. janeiro: vez do Simples Nacional', 36.55, top=220) +
         f"<div class='tt' style='position:absolute;left:90px;right:170px;top:1030px;text-align:center;{A('pop',40.9,.4)}'><span class='box' style='font-size:100px;font-weight:900'>faltam 92 dias</span></div>", fade_in=.01, fade_out=.01),
      scene(T0, T1, f"<img id='foot' src='file://{TMP}/foot/{fa[0]}' style='position:absolute;inset:0;width:100%;height:100%;object-fit:cover'>" + txt('aqui no escritório:', T0 + .05, top=150), fade_in=.01, fade_out=.01),
      scene(T1, END, ph('julia_selfie', T1, END - T1 + .3, 'center 30%', 'kbl') + txt('salva 📌 e manda pro colega do fiscal', T1 + .05, top=220), fade_in=.01, fade_out=.01),
    ]
    cap = "<div id='cap' class='tt' style='position:absolute;left:80px;right:160px;top:1270px;text-align:center;font-size:76px;font-weight:900;line-height:1.12;color:#fff;text-shadow:0 0 3px #000,4px 4px 0 #000,-4px 4px 0 #000,4px -4px 0 #000,-4px -4px 0 #000,0 6px 18px rgba(0,0,0,.7)'></div>"
    js = f"""<script>
    const C={js_chunks}; const F={foot_js}; const T0={T0};
    window.__t=function(ms){{const t=ms/1000; const el=document.getElementById('cap'); let h='';
      for(const c of C){{ if(t>=c[0][1]-0.05 && t<c[c.length-1][2]+0.12){{ h=c.map(w=>(t>=w[1]&&t<w[2]+0.02)?'<span style="color:#FFE14D">'+w[0]+'</span>':w[0]).join(' '); break; }} }}
      el.innerHTML=h;
      const f=document.getElementById('foot'); if(f){{ const i=Math.floor((t-T0)*30); if(i>=0&&i<F.length&&f.getAttribute('src')!==F[i]) f.setAttribute('src',F[i]); }} }};
    </script>"""
    anim_clip(stage(sc) + cap + js, f'{TMP}/tt3_v.mp4', END, TT_CSS)
    os.makedirs(OUT+'/03_video_explicativo_nfse', exist_ok=True)
    mix(f'{TMP}/tt3_v.mp4', OUT+'/03_video_explicativo_nfse/video.mp4', voice=S+'/vo/tt3_vo_fast.wav', voice_at=0.0,
        sfx=[('pop',0.05,.25),('whoosh',4.95,.25),('whoosh',12.65,.25),('pop',15.2,.25),('pop',18.4,.25),('ding',20.6,.25),('whoosh',22.95,.25),('whoosh',25.05,.25),('pop',25.6,.25),('whoosh',30.05,.25),('whoosh',36.45,.25),('impact',40.9,.3),('whoosh',T0-.05,.25),('typing',T0+.3,.3),('whoosh',T1-.05,.25)])

if __name__ == '__main__':
    for f in sys.argv[1:]: globals()[f]()
