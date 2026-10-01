# Shared animated-scene helpers (CSS keyframes; frames.mjs seeks every animation per frame)
from kit import *
ANIM_CSS = """
@keyframes punch{0%{transform:scale(1.18)}100%{transform:scale(1.03)}}
@keyframes kb{from{transform:scale(1.0)}to{transform:scale(1.12)}}
@keyframes kbl{from{transform:scale(1.12) translateX(2%)}to{transform:scale(1.02) translateX(-1%)}}
@keyframes up{from{opacity:0;transform:translateY(60px)}to{opacity:1;transform:none}}
@keyframes pop{0%{opacity:0;transform:scale(.6)}70%{opacity:1;transform:scale(1.06)}100%{opacity:1;transform:scale(1)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes out{from{opacity:1}to{opacity:0}}
@keyframes wipe{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes bar{from{width:0}to{width:var(--w)}}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-10px)}40%{transform:translateX(10px)}60%{transform:translateX(-6px)}80%{transform:translateX(6px)}}
.sc{position:absolute;inset:0;opacity:0;overflow:hidden}
.a{animation-fill-mode:both;animation-timing-function:cubic-bezier(.2,.8,.2,1)}
"""
def scene(t0, t1, inner, fade_in=.25, fade_out=.25, bg='#0A0A0A'):
    """visible from t0..t1 (seconds)"""
    d = t1 - t0
    return (f"<div class='sc' style='background:{bg};animation:fade {fade_in}s linear {t0}s both, out {fade_out}s linear {t1-fade_out}s forwards'>"
            f"{inner}</div>")
def A(name, t, dur=.6, extra=''):
    return f"animation:{name} {dur}s cubic-bezier(.2,.8,.2,1) {t}s both;{extra}"
def kb_photo(name, t0, dur, pos='center', anim='kb', filt='saturate(.95) contrast(1.05) brightness(.9)'):
    return (f"<img src='file://{AI}{name}.webp' style='position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos};"
            f"filter:{filt};animation:{anim} {dur}s linear {t0}s both'>")
def brand_bg():
    return "<div class='grid'></div><div class='glow'></div>"
def logo_v():  # logo for 1080x1920 (safe zone top ~ 130px)
    return f"<img src='file://{B}logo_wordmark.png' style='position:absolute;left:80px;top:150px;height:44px'>"
