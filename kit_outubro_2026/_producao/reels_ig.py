import sys, json
from vid import *
from anim import *
OUT = S + '/out/instagram'
TMP = S + '/build/tmp'; os.makedirs(TMP, exist_ok=True)

def ig1(T):
    """T: dict of scene boundaries computed from VO"""
    t1, t2 = T['s2'], T['endA']
    body = "<div class='stage'>"
    # S1 photo + headline
    body += scene(0, t1, kb_photo('ana_surpresa', 0, t1+.3, 'center 30%') +
      "<div style='position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.55) 0%,rgba(10,10,10,0) 25%,rgba(10,10,10,0) 45%,rgba(10,10,10,.9) 72%,#0A0A0A 100%)'></div>" + logo_v() +
      f"""<div style='position:absolute;left:80px;right:80px;bottom:420px'>
        <div class='kicker' style='{A('up',.15,.5)}'>Reforma tributária · 01/10/2026</div>
        <div class='h' style='font-size:150px;margin-top:34px;{A('up',.3,.6)}'>A NFS-e</div>
        <div class='h' style='font-size:150px;{A('up',.55,.6)}'><span class='g'>mudou hoje.</span></div></div>""", fade_in=0.01)
    # S2 date card
    body += scene(t1, t2, brand_bg() + logo_v() + f"""
      <div style='position:absolute;left:80px;right:80px;top:500px'>
        <div class='kicker' style='{A('up',t1+.1,.5)}'>A partir de hoje</div>
        <div class='card' style='margin-top:60px;width:420px;border-radius:36px;overflow:hidden;{A('pop',t1+.2,.6)}'>
          <div class='mono' style='background:#10B981;color:#0A0A0A;font-weight:700;font-size:40px;letter-spacing:.3em;text-align:center;padding:18px 0'>OUT · 2026</div>
          <div style='font-size:230px;font-weight:800;letter-spacing:-.06em;text-align:center;line-height:1.05;padding:10px 0 30px'>01</div></div>
        <div class='h' style='font-size:104px;margin-top:80px;{A('up',t1+.6,.6)}'>A NFS-e também traz <span class='g'>IBS e CBS.</span></div>
        <div class='p' style='margin-top:40px;font-size:42px;{A('up',t1+1.0,.6)}'>Os impostos novos da reforma, item a item, no XML e no PDF.</div></div>""")
    body += "</div>"
    anim_clip(body, f'{TMP}/ig1_a.mp4', t2, ANIM_CSS)
    # footage: DANFE com IBS/CBS
    cut(S + '/src/08_reels_encontre_qualquer_nota/reels.mp4', 8.7, T['foot'], f'{TMP}/ig1_b.mp4')
    # C: countdown + endcard
    c0, c1, c2 = T['c0'], T['c_end1'], T['c_end2']
    body = "<div class='stage'>"
    # S3 aliquotas
    def stat(lbl, val, t, w):
        return f"""<div class='card' style='padding:46px 50px;margin-top:34px;{A('up',t,.6)}'>
          <div style='display:flex;justify-content:space-between;align-items:baseline'>
            <span class='mono' style='font-size:40px;letter-spacing:.2em;color:#C9CAD0'>{lbl}</span>
            <span style='font-size:140px;font-weight:800;letter-spacing:-.05em' class='g'>{val}</span></div>
          <div style='height:14px;background:rgba(255,255,255,.07);border-radius:9px;margin-top:20px;overflow:hidden'>
            <div style='--w:{w}%;height:100%;background:#10B981;border-radius:9px;{A('bar',t+.3,1.0)}'></div></div></div>"""
    body += scene(0, T['c0'], brand_bg() + logo_v() + f"""
      <div style='position:absolute;left:80px;right:80px;top:500px'>
        <div class='kicker' style='{A('up',.05,.4)}'>Fase de teste</div>
        <div class='h' style='font-size:110px;margin-top:40px;{A('up',.05,.5)}'>Destacado na nota. <span class='g'>Sem aumento de carga.</span></div>
        {stat('CBS', '0,9%', .1, 90)}{stat('IBS', '0,1%', T['ibs'], 10)}</div>""", fade_out=.01)
    body += scene(c0, c1, brand_bg() + logo_v() + f"""
      <div style='position:absolute;left:80px;right:80px;top:500px'>
        <div class='kicker' style='{A('up',c0+.1,.5)}'>Próxima etapa · 01/01/2027</div>
        <div class='h' style='font-size:116px;margin-top:40px;{A('up',c0+.2,.6)}'>Em janeiro, é a vez do <span class='g'>Simples Nacional.</span></div>
        <div style='display:flex;align-items:baseline;gap:30px;margin-top:90px;{A('pop',T['cd'],.6)}'>
          <span id='cd' class='g' style='font-size:300px;font-weight:800;letter-spacing:-.06em;line-height:.9'>92</span>
          <span class='mono' style='font-size:52px;letter-spacing:.2em;color:#C9CAD0'>DIAS</span></div></div>
      <script>window.__t=function(ms){{var s=ms/1000-{T['cd']},el=document.getElementById('cd');if(!el)return;var p=Math.min(1,Math.max(0,(s)/1.3));el.textContent=Math.round(365-(365-92)*(1-Math.pow(1-p,3)));}}</script>""")
    body += scene(c1, c2, brand_bg() + f"""
      <div style='position:absolute;left:0;right:0;top:470px;text-align:center'>
        <div style='{A('pop',c1+.05,.6)}'><svg width='220' height='220' viewBox='0 0 220 220'><rect x='10' y='20' width='200' height='40' fill='#fff'/><rect x='10' y='90' width='200' height='40' fill='#fff'/><rect x='10' y='160' width='200' height='40' fill='#fff'/></svg></div>
        <img src='file://{B}wordmark_big.png' style='height:62px;margin-top:50px;{A('up',c1+.2,.6)}'>
        <div class='h' style='font-size:86px;margin:90px 80px 0;{A('up',c1+.4,.6)}'>Comente <span class='g'>NFSE</span> e receba o checklist da virada.</div>
        <div class='mono' style='font-size:30px;letter-spacing:.34em;color:#8A8A92;margin-top:50px;{A('fade',c1+.8,.6)}'>📌 SALVE PARA O FECHAMENTO</div></div>""", fade_out=.01)
    body += "</div>"
    anim_clip(body, f'{TMP}/ig1_c.mp4', c2, ANIM_CSS)
    concat([f'{TMP}/ig1_a.mp4', f'{TMP}/ig1_b.mp4', f'{TMP}/ig1_c.mp4'], f'{TMP}/ig1_v.mp4')


def ig5(T=None):
    pill = "display:inline-block;background:#fff;color:#0A0A0A;font-weight:800;letter-spacing:-.03em;border-radius:22px;padding:18px 30px;font-size:64px"
    body = "<div class='stage'>"
    body += scene(0, 3.6, kb_photo('ana_pov', 0, 3.9, 'center 15%') +
      "<div style='position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.35) 0%,rgba(10,10,10,0) 30%,rgba(10,10,10,0) 55%,rgba(10,10,10,.8) 100%)'></div>" + f"""
      <div style='position:absolute;left:70px;right:70px;top:250px'><div style='{pill};{A('pop',.05,.45)}'>POV: sexta, 17h58.</div></div>
      <div style='position:absolute;left:70px;right:150px;top:1010px;{A('up',.8,.45)}'>
        <div style='background:rgba(32,32,36,.94);border-radius:34px 34px 34px 8px;padding:28px 34px;box-shadow:0 20px 60px rgba(0,0,0,.5);border:1px solid rgba(255,255,255,.08)'>
          <div class='mono' style='font-size:26px;color:#10B981;letter-spacing:.06em'>Cliente · Padaria Aurora</div>
          <div style='font-size:46px;line-height:1.3;margin-top:10px;color:#fff'>Oi! Consegue me mandar a nota 4.812 de setembro? É pra agora 🙏</div>
          <div class='mono' style='font-size:22px;color:#8A8A92;text-align:right;margin-top:8px'>17:58</div></div></div>
      <div style='position:absolute;left:70px;right:70px;bottom:400px;{A('up',2.1,.45)}'>
        <div class='h' style='font-size:92px'>eu, que ia sair <span class='g'>às 18h:</span></div></div>""", fade_in=.01, fade_out=.01)
    body += "</div>"
    anim_clip(body, f'{TMP}/ig5_a.mp4', 3.6, ANIM_CSS)
    # overlay caption on footage
    render(f"""<div style='position:absolute;left:0;right:0;bottom:330px;text-align:center'>
        <div style='display:inline-block;background:#10B981;color:#0A0A0A;font-weight:800;font-size:66px;letter-spacing:-.03em;border-radius:22px;padding:16px 34px'>achei em 4 segundos.</div></div>""",
        f'{TMP}/ig5_cap.png', 1080, 1920, css='html,body,.stage{background:transparent!important}', transparent=True)
    subprocess.run(['ffmpeg','-v','error','-y','-ss','3.6','-i',S+'/src/08_reels_encontre_qualquer_nota/reels.mp4','-loop','1','-i',f'{TMP}/ig5_cap.png','-t','4.3',
        '-filter_complex',"[1:v]format=rgba,fade=in:st=2.9:d=0.2:alpha=1[c];[0:v][c]overlay=0:0:shortest=1,fps=30",'-an','-c:v','libx264','-pix_fmt','yuv420p','-crf','16',f'{TMP}/ig5_b.mp4'], check=True)
    body = "<div class='stage'>"
    body += scene(0, 4.0, kb_photo('ana_saindo', 0, 4.3, 'center 25%') +
      "<div style='position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.3) 0%,rgba(10,10,10,0) 30%,rgba(10,10,10,0) 45%,rgba(10,10,10,.92) 78%,#0A0A0A 100%)'></div>" + f"""
      <div style='position:absolute;left:70px;right:70px;top:250px'><div style='{pill};{A('pop',.1,.45)}'>17h59.</div></div>
      <div style='position:absolute;left:80px;right:80px;bottom:420px'>
        <div class='h' style='font-size:110px;{A('up',.3,.5)}'>Bom fim de semana. <span class='g'>✌️</span></div>
        <div style='display:flex;align-items:center;gap:26px;margin-top:46px;{A('up',.8,.5)}'>
          <img src='file://{B}logo_wordmark.png' style='height:44px'>
          <span class='mono' style='font-size:28px;letter-spacing:.24em;color:#C9CAD0'>COMENTE <span class='g'>BUSCA</span></span></div></div>""", fade_in=.15, fade_out=.01)
    body += "</div>"
    anim_clip(body, f'{TMP}/ig5_c.mp4', 4.0, ANIM_CSS)
    concat([f'{TMP}/ig5_a.mp4', f'{TMP}/ig5_b.mp4', f'{TMP}/ig5_c.mp4'], f'{TMP}/ig5_v.mp4')
    os.makedirs(OUT+'/05_reels_pov_sexta_17h58', exist_ok=True)
    mix(f'{TMP}/ig5_v.mp4', OUT+'/05_reels_pov_sexta_17h58/reels.mp4',
        sfx=[('pop',0.05,.35),('notify',0.8,.5),('whoosh',2.05,.25),('whoosh',3.55,.3),('typing',4.1,.4),('click',6.45,.4),('ding',6.6,.35),('whoosh',7.85,.3),('pop',8.0,.3)])

if __name__ == '__main__':
    globals()[sys.argv[1]](json.loads(sys.argv[2]))
