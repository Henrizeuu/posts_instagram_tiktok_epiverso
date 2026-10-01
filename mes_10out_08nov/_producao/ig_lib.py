"""Instagram do mês: templates na identidade Epiverso (1080x1350)."""
import os, subprocess
from kit import *
from clips import C
from engine import clip_info, LIB
REPO = '/home/user/posts_instagram_tiktok_epiverso/mes_10out_08nov/instagram'
FR = S + '/build/eng/igframes'; os.makedirs(FR, exist_ok=True)
W, H = 1080, 1350
def still45(name, dt=0.6, x=None):
    clip, ss, cx = C[name]; cx = cx if x is None else x
    out = f'{FR}/{name}_{dt}_{cx}.jpg'
    if not os.path.exists(out):
        f, w, h, D = clip_info(clip)
        if w > h:
            cw = int(h * 4 / 5) // 2 * 2; vf = f"crop={cw}:{h}:{int((w-cw)*cx)}:0,scale=1080:1350"
        else:
            ch = int(w * 5 / 4) // 2 * 2; vf = f"crop={w}:{ch}:0:{int((h-ch)*0.35)},scale=1080:1350"
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(min(ss+dt, D-0.1)),'-i',f,'-frames:v','1','-vf',vf,'-q:v','2',out], check=True)
    return out
def ph(name, dt=0.6, x=None, filt='saturate(.9) contrast(1.04) brightness(.9)'):
    return f"<img src='file://{still45(name, dt, x)}' style='position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:{filt}'>"
def shade(top=.55, bottom=.97, start=34):
    return (f"<div style='position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,{top}) 0%,rgba(10,10,10,0) 20%,"
            f"rgba(10,10,10,0) {start}%,rgba(10,10,10,.85) {start+24}%,rgba(10,10,10,{bottom}) 100%)'></div>")
def frame(inner, n=None, total=None, foot='PAINEL FISCAL', arrow=True, grid=True):
    cnt = f"<div class='count'>{n:02d} / {total:02d}</div>" if n else ''
    g = "<div class='grid'></div><div class='glow'></div>" if grid else ''
    ar = f"<span class='arr'>ARRASTE {ARROW}</span>" if arrow else '<span></span>'
    return f"<div class='stage'>{g}{inner}{logo()}{cnt}<div class='foot'><span>{foot}</span>{ar}</div></div>"
# ---------- lâminas ----------
def cover(photo, kicker, title, sub='', size=100, x=None, dt=0.6):
    return (ph(photo, dt, x) + shade(.6, .97, 30) +
        f"<div style='position:absolute;left:86px;right:86px;bottom:150px'><div class='kicker'>{kicker}</div>"
        f"<div class='h' style='font-size:{size}px;margin-top:28px'>{title}</div>"
        + (f"<div class='p' style='margin-top:28px;color:#C9CAD0'>{sub}</div>" if sub else '') + "</div>")
def text(kicker, title, body='', vis='', size=92, top=None):
    return (f"<div style='position:absolute;left:86px;right:86px;top:150px;bottom:150px;display:flex;flex-direction:column;justify-content:center'><div class='kicker'>{kicker}</div>"
            f"<div class='h' style='font-size:{size}px;margin-top:32px'>{title}</div>"
            + (f"<div class='p' style='margin-top:34px;font-size:42px'>{body}</div>" if body else '')
            + (f"<div style='margin-top:48px'>{vis}</div>" if vis else '') + "</div>")
def rows(items, hl=None):
    """items: [(left, right)] → tabela em card"""
    r = ''.join(f"<div style='display:flex;justify-content:space-between;align-items:center;gap:30px;padding:22px 0;{'border-top:1px solid rgba(255,255,255,.07);' if k else ''}font-size:36px'>"
                f"<span style='font-weight:600;color:{'#10B981' if hl==k else '#fff'}'>{a}</span><span class='mono' style='color:#C9CAD0;font-size:27px;text-align:right'>{b}</span></div>"
                for k, (a, b) in enumerate(items))
    return f"<div class='card' style='padding:20px 38px'>{r}</div>"
def checks(items):
    r = ''.join(f"<div style='display:flex;gap:26px;align-items:flex-start;padding:22px 0;{'border-top:1px solid rgba(255,255,255,.07);' if k else ''}'>"
                f"<div style='flex:none;width:46px;height:46px;border-radius:12px;background:rgba(16,185,129,.14);border:1px solid #10B981;display:flex;align-items:center;justify-content:center;color:#10B981;font-size:28px;font-weight:800'>✓</div>"
                f"<div><div style='font-size:40px;font-weight:700;letter-spacing:-.02em'>{a}</div>"
                + (f"<div style='font-size:31px;color:#A6A6AE;margin-top:8px;line-height:1.35'>{b}</div>" if b else '') + "</div></div>"
                for k, (a, b) in enumerate(items))
    return f"<div>{r}</div>"
def big(kicker, num, label, body='', top=230):
    return (f"<div style='position:absolute;left:86px;right:86px;top:{top}px'><div class='kicker'>{kicker}</div>"
            f"<div style='display:flex;align-items:flex-end;gap:26px;margin-top:40px'><div class='g' style='font-size:230px;font-weight:800;letter-spacing:-.06em;line-height:.85'>{num}</div>"
            f"<div class='mono' style='font-size:30px;letter-spacing:.2em;color:#C9CAD0;padding-bottom:18px'>{label}</div></div>"
            + (f"<div class='p' style='margin-top:50px;font-size:40px;color:#C9CAD0'>{body}</div>" if body else '') + "</div>")
def vs(lt, lb, rt, rb):
    box = lambda t, b, c: (f"<div class='card' style='flex:1;padding:36px 34px;border-color:{c}'><div class='mono' style='font-size:24px;letter-spacing:.3em;color:{c}'>{t}</div>"
                          f"<div style='font-size:37px;line-height:1.35;margin-top:22px;color:#E5E5E8'>{b}</div></div>")
    return f"<div style='display:flex;gap:26px'>{box(lt, lb, '#8A8A92')}{box(rt, rb, '#10B981')}</div>"
def xml(lines):
    return f"<div class='card mono' style='padding:34px 38px;font-size:31px;line-height:1.75;color:#C9CAD0;white-space:pre'>{lines}</div>"
def cta(line, sub='SALVE PARA O FECHAMENTO'):
    return (f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 110px'>"
            f"<img src='file://{B}logo_stack.png' style='height:250px'>"
            f"<div class='h' style='font-size:64px;margin-top:80px;line-height:1.05'>{line}</div>"
            f"<div class='mono' style='font-size:22px;letter-spacing:.34em;color:#8A8A92;margin-top:40px'>📌 {sub}</div></div>")
def carousel(folder, slides, legenda):
    out = f'{REPO}/{folder}'; os.makedirs(out, exist_ok=True)
    n = len(slides)
    for i, s in enumerate(slides, 1):
        last = i == n
        if isinstance(s, tuple):  # (inner, grid)
            inner, grid = s
        else: inner, grid = s, True
        body = frame(inner, i, n, arrow=not last, grid=grid)
        render(body, f'{out}/{i:02d}.png', W, H)
        subprocess.run(['convert', f'{out}/{i:02d}.png', '-quality', '92', f'{out}/{i:02d}.jpg'], check=False)
        if os.path.exists(f'{out}/{i:02d}.jpg'): os.unlink(f'{out}/{i:02d}.png')
    open(f'{out}/legenda.txt', 'w').write(legenda)
    return out
def static(folder, inner, legenda, grid=True):
    out = f'{REPO}/{folder}'; os.makedirs(out, exist_ok=True)
    render(frame(inner, arrow=False, grid=grid), f'{out}/post.png', W, H)
    subprocess.run(['convert', f'{out}/post.png', '-quality', '92', f'{out}/post.jpg'], check=False)
    if os.path.exists(f'{out}/post.jpg'): os.unlink(f'{out}/post.png')
    open(f'{out}/legenda.txt', 'w').write(legenda)
    return out
def LEG(title, when, fmt, text, tags, alt, music, extra=''):
    return f"""{title}
POSTAR: {when}
FORMATO: {fmt}

LEGENDA (copiar e colar):
{text}

{tags}

TEXTO ALTERNATIVO (acessibilidade): {alt}

MÚSICA: {music}
{extra}"""
