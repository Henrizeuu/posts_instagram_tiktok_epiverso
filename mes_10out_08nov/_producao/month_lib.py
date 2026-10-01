from engine import *
from clips import sc, C
VO = S + '/vo2'
TOP = 230; BOT = 1380
def M(lines):
    """meme: lines = [(clip, dur, top_text, bottom_text_or_None, extra_ov_list)]"""
    scenes = []
    for item in lines:
        name, d, top = item[0], item[1], item[2]
        bot = item[3] if len(item) > 3 else None
        extra = item[4] if len(item) > 4 else []
        ov = []
        if top: ov.append((T(top, top=TOP), 0, None))
        if bot: ov.append((T(bot, top=1250, style='stroke', size=96), 0.6, None))
        ov += extra
        scenes.append(sc(name, d, ov=ov, z=1.05))
    return scenes
def EDU(vo, header, broll, cap_text=None, header_top=TOP):
    from vo_texts import V
    cap_text = cap_text or V[vo]
    """VO + b-roll; broll: list of clip names (cycled) — durations fill the VO."""
    path = f'{VO}/{vo}.wav'
    dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',path])) + 0.8
    CAP = {'robo_sync':3.6,'pasta_xml':3.8,'painel_pronto':4.4,'busca':4.0,'danfe':2.2,'zip':1.7}
    capped = {b: CAP[b] for b in broll if b in CAP}
    free = [b for b in broll if b not in CAP]
    each = (dur - sum(capped.values())) / max(1, len(free))
    scenes = [sc(b, capped.get(b, each), z=(1.0 if b in CAP else 1.06)) for b in broll]
    scenes[0]['ov'] = [(T(header, top=header_top), 0, 3.2)]
    return dict(scenes=scenes, vo=path, vo_at=0.3, caps=cap_text, cap_top=1320)
def TX(lines, broll, first_top=None, extra0=None):
    """text story: each line its own scene over broll clips."""
    scenes = []
    for i, (txt, d) in enumerate(lines):
        b = broll[i % len(broll)]
        prod = b in ('robo_sync','pasta_xml','painel_pronto','busca','danfe','zip')
        ov = [(T(txt, top=1420 if prod else TOP), 0, None)]
        if i == 0 and extra0: ov += extra0
        scenes.append(sc(b, d, ov=ov, z=1.0 if prod else 1.05))
    return scenes
def COMMENT(user, text, top=520):
    return (f"<div style='position:absolute;left:70px;top:{top}px;max-width:820px;background:#fff;border-radius:24px;padding:22px 28px;box-shadow:0 10px 40px rgba(0,0,0,.35);font-family:TT;color:#111'>"
            f"<div style='font-size:30px;color:#777;font-weight:600'>Responder ao comentário de {user}</div><div style='font-size:46px;font-weight:700;margin-top:8px;line-height:1.2'>{text}</div></div>")
def CARD(rows, title, foot='dados de demonstração · empresas fictícias', top=640):
    """card branco estilo app com linhas (rótulo, valor)"""
    r = ''.join(f"<div style='display:flex;justify-content:space-between;padding:18px 0;border-top:1px solid #eee;font-size:40px'><span style='color:#555'>{a}</span><b>{b}</b></div>" for a, b in rows)
    return (f"<div style='position:absolute;left:70px;right:70px;top:{top}px;background:#fff;border-radius:30px;padding:34px 40px;font-family:TT;color:#111;box-shadow:0 18px 50px rgba(0,0,0,.35)'>"
            f"<div style='font-size:44px;font-weight:800;margin-bottom:14px'>{title}</div>{r}"
            f"<div style='font-size:26px;color:#999;margin-top:14px'>{foot}</div></div>")
def BAR(name, val, lim, pct, note, top=640):
    return (f"<div style='position:absolute;left:70px;right:70px;top:{top}px;background:#fff;border-radius:30px;padding:34px 40px;font-family:TT;color:#111;box-shadow:0 18px 50px rgba(0,0,0,.35)'>"
            f"<div style='font-size:30px;color:#777;font-weight:600'>Limite do Simples · 12 meses</div><div style='font-size:46px;font-weight:800;margin:6px 0 22px'>{name}</div>"
            f"<div style='height:34px;background:#eee;border-radius:17px;overflow:hidden'><div style='height:100%;width:{pct}%;background:linear-gradient(90deg,#10B981,#F59E0B)'></div></div>"
            f"<div style='display:flex;justify-content:space-between;font-size:34px;margin-top:14px'><b>{val}</b><span style='color:#777'>limite {lim}</span></div>"
            f"<div style='margin-top:20px;font-size:36px;color:#B45309;font-weight:700'>⚠ {note}</div>"
            f"<div style='font-size:26px;color:#999;margin-top:14px'>dados de demonstração · empresa fictícia</div></div>")
