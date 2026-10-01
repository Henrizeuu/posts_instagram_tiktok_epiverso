"""Monta vídeos verticais a partir de clipes reais + overlays HTML + áudio."""
import os, json, subprocess, tempfile, re, hashlib
from kit import S, FONTS, BASE_CSS, B, AI
LIB = S + '/stock/lib'
TMP = S + '/build/eng'; os.makedirs(TMP, exist_ok=True)
FPS = 30
TT_CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box} html,body{width:1080px;height:1920px;background:transparent;overflow:hidden}
.tt{font-family:TT;font-weight:700;letter-spacing:-.01em;line-height:1.45;position:absolute;left:70px;right:150px;text-align:center}
.box{display:inline;background:#fff;color:#111;padding:8px 20px;border-radius:14px;box-decoration-break:clone;-webkit-box-decoration-break:clone;font-size:58px}
.stroke{color:#fff;font-size:64px;font-weight:800;text-shadow:0 0 3px #000,3px 3px 0 #000,-3px 3px 0 #000,3px -3px 0 #000,-3px -3px 0 #000,0 5px 16px rgba(0,0,0,.6)}
.yel{color:#FFE14D}
.notif{position:absolute;left:60px;right:60px;background:rgba(245,245,247,.97);border-radius:34px;padding:26px 30px;display:flex;gap:22px;align-items:center;box-shadow:0 18px 50px rgba(0,0,0,.35);font-family:TT;color:#111}
.notif .ic{width:84px;height:84px;border-radius:20px;background:#25A35A;display:flex;align-items:center;justify-content:center;flex:none}
.notif .ttl{font-weight:700;font-size:36px}.notif .msg{font-size:36px;color:#333;margin-top:4px}.notif .tm{font-size:26px;color:#888;margin-left:auto;align-self:flex-start}
.clock{position:absolute;font-family:TT;font-weight:800;color:#fff;font-size:120px;letter-spacing:-.02em;text-shadow:0 4px 20px rgba(0,0,0,.6)}
"""
CHAT_ICON = "<svg width='48' height='48' viewBox='0 0 24 24'><path fill='#fff' d='M4 4h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H9l-5 4v-4H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z'/></svg>"

def page(inner, css=''):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{TT_CSS}{css}</style></head><body>{inner}</body></html>"

# ---------- overlay builders (return inner html) ----------
def T(text, top=230, style='box', size=None):
    st = f" style='font-size:{size}px'" if size else ''
    return f"<div class='tt' style='top:{top}px'><span class='{style}'{st}>{text}</span></div>"
def NOTIF(title, msg, tm='agora', top=180):
    return f"<div class='notif' style='top:{top}px'><div class='ic'>{CHAT_ICON}</div><div><div class='ttl'>{title}</div><div class='msg'>{msg}</div></div><div class='tm'>{tm}</div></div>"
def CLOCK(txt, top=300, left=80):
    return f"<div class='clock' style='top:{top}px;left:{left}px'>{txt}</div>"

def render_pngs(items):
    """items: list of (inner_html, out_path). Renders only missing files, one browser."""
    jobs = [dict(html=page(h), out=o, transparent=not o.split("/")[-1].startswith("car_")) for h, o in items if not os.path.exists(o)]
    if not jobs: return
    jf = tempfile.mktemp(suffix='.json', dir=TMP); json.dump(jobs, open(jf, 'w'))
    subprocess.run(['node', S + '/build/render_batch.mjs', jf], check=True); os.unlink(jf)

def key(s): return hashlib.md5(s.encode()).hexdigest()[:12]

def clip_info(c):
    f = f'{LIB}/{c}.mp4'
    w, h = map(int, subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','csv=p=0', f]).decode().strip().split(','))
    d = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0', f]))
    return f, w, h, d

def seg(scene, out):
    """scene: clip, ss, d, x (0..1 crop center for landscape), z (end zoom, 1=none), speed"""
    f, w, h, D = clip_info(scene['clip'])
    ss = scene.get('ss', 0); d = scene['d']; sp = scene.get('speed', 1.0)
    me = scene.get('maxend')
    if me and ss + d * sp > me:  # telas do produto: desacelera em vez de passar para a próxima tela
        sp = max(0.45, (me - ss) / d)
    ss = max(0, min(ss, D - d * sp - 0.05))
    if w > h:  # landscape 4K -> crop 9:16
        cw = int(h * 9 / 16) // 2 * 2; cx = int((w - cw) * scene.get('x', 0.5))
        base = f"crop={cw}:{h}:{cx}:0,scale=1080:1920"
    else:
        base = "scale=1080:1920"
    z = scene.get('z', 1.04)
    zoom = f",scale=w='trunc(1080*(1+({z}-1)*t/{d})/2)*2':h='trunc(1920*(1+({z}-1)*t/{d})/2)*2':eval=frame,crop=1080:1920" if z != 1 else ''
    vf = f"setpts=PTS/{sp},{base}{zoom},fps={FPS},format=yuv420p" + scene.get('vf', '')
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(ss),'-i',f,'-t',str(d*sp),'-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','18',out], check=True)
    return out

def build(spec, out_mp4):
    """spec: scenes[ {clip,ss,d,x,z,ov:[(html,t0,t1)] } ], global_ov [(html,t0,t1)], sfx [(name,t,vol)], vo path, captions bool"""
    os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
    segs = []; t = 0; overlays = []
    for i, sc in enumerate(spec['scenes']):
        p = f"{TMP}/{spec['id']}_s{i}.mp4"; seg(sc, p); segs.append(p)
        for h, a, b in sc.get('ov', []):
            overlays.append((h, t + a, t + (b if b is not None else sc['d']) - 0.02))  # sem quadro duplicado na troca
        t += sc['d']
    total = t
    for h, a, b in spec.get('ov', []): overlays.append((h, a, b if b is not None else total))
    # captions from VO
    if spec.get('vo') and spec.get('caps'):
        for txt, a, b in caption_chunks(spec['vo'], spec['caps'], spec.get('vo_at', 0)):
            overlays.append((T(txt, top=spec.get('cap_top', 1300), style='stroke', size=66), a, b))
    pngs = []
    for h, a, b in overlays:
        o = f"{TMP}/ov_{key(h)}.png"; pngs.append((h, o, a, b))
    render_pngs([(h, o) for h, o, _, _ in pngs])
    lst = f"{TMP}/{spec['id']}_l.txt"; open(lst, 'w').write(''.join(f"file '{p}'\n" for p in segs))
    cat = f"{TMP}/{spec['id']}_cat.mp4"
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',lst,'-c','copy',cat], check=True)
    # overlay chain
    ins = ['-i', cat]; fc = []; last = '0:v'
    for k, (h, o, a, b) in enumerate(pngs):
        ins += ['-i', o]; nl = f'v{k}'
        fc.append(f"[{last}][{k+1}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[{nl}]"); last = nl
    vid = f"{TMP}/{spec['id']}_v.mp4"
    if fc:
        subprocess.run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',';'.join(fc),'-map',f'[{last}]','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',vid], check=True)
    else: os.replace(cat, vid)
    mix(vid, out_mp4, spec.get('sfx', []), spec.get('vo'), spec.get('vo_at', 0), total)
    return out_mp4

def mix(video, out, sfx, vo, vo_at, dur):
    ins = ['-i', video]; flt = []; lab = []; k = 1
    for name, t, vol in sfx:
        ins += ['-i', f'{S}/sfx/{name}.wav']; flt.append(f'[{k}:a]adelay={int(t*1000)}|{int(t*1000)},volume={vol}[a{k}]'); lab.append(f'[a{k}]'); k += 1
    if vo:
        ins += ['-i', vo]; flt.append(f'[{k}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(vo_at*1000)}|{int(vo_at*1000)}[a{k}]'); lab.append(f'[a{k}]'); k += 1
    flt.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{dur}[sil]")
    flt.append(f"[sil]{''.join(lab)}amix=inputs={len(lab)+1}:normalize=0,atrim=0:{dur},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[ao]")
    subprocess.run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',';'.join(flt),'-map','0:v','-map','[ao]','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',out], check=True)

def speech_segments(audio):
    out = subprocess.run(['ffmpeg','-i',audio,'-af','silencedetect=noise=-35dB:d=0.2','-f','null','-'],capture_output=True,text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', out)]; en = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', out)]
    dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',audio]))
    segs = []; cur = 0.0
    for a, b in zip(st, en):
        if a - cur > 0.05: segs.append((cur, a))
        cur = b
    if dur - cur > 0.05: segs.append((cur, dur))
    return segs, dur

def caption_chunks(audio, text, offset=0):
    """Splits text into sentence-aligned speech segments, then 3-word chunks."""
    segs, _ = speech_segments(audio)
    sents = [s.strip() for s in re.split(r'(?<=[.:?!,])\s+', text) if s.strip()]
    # merge sentences/segments proportionally by length
    words = text.split(); tot = sum(len(w) + 1 for w in words); D = sum(b - a for a, b in segs)
    def realt(x):
        for a, b in segs:
            if x <= b - a: return a + x
            x -= b - a
        return segs[-1][1]
    acc = 0; timed = []
    for w in words:
        s0 = acc / tot * D; acc += len(w) + 1; s1 = acc / tot * D
        timed.append((w, realt(s0), realt(s1)))
    chunks = []; cur = []
    for w in timed:
        cur.append(w)
        if len(cur) == 3 or w[0][-1] in '.:?!,':
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    out = [(' '.join(w for w, _, _ in c), c[0][1] + offset, c[-1][2] + offset + 0.08) for c in chunks]
    for i in range(len(out) - 1):  # nunca duas legendas ao mesmo tempo
        if out[i][2] > out[i + 1][1] - 0.001:
            out[i] = (out[i][0], out[i][1], out[i + 1][1] - 0.001)
    return out
