import os, subprocess, tempfile, base64
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = S + '/fonts/ttf/'
B = S + '/brand/'
AI = S + '/ai/'
def uri(p):
    ext = p.rsplit('.',1)[1].lower()
    mt = {'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg','webp':'image/webp'}[ext]
    return 'file://' + p

FONTS = ''.join(
    f"@font-face{{font-family:'{fam}';src:url('file://{F}{fn}-latin-{w}-normal.ttf');font-weight:{w};}}"
    for fam, fn, ws in [('Inter','inter',[400,500,600,700,800,900]),('JBM','jetbrains-mono',[400,500,700]),('TT','tiktok-sans',[400,500,600,700,800,900])]
    for w in ws)

BASE_CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:100%;height:100%;background:#0A0A0A;color:#fff;font-family:Inter;-webkit-font-smoothing:antialiased}
.stage{position:relative;width:100%;height:100%;overflow:hidden;background:#0A0A0A}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:54px 54px;
 -webkit-mask-image:radial-gradient(ellipse 90% 70% at 85% 0%,#000 0%,rgba(0,0,0,.35) 55%,transparent 85%)}
.glow{position:absolute;width:1100px;height:1100px;right:-420px;top:-520px;background:radial-gradient(circle,rgba(16,185,129,.22) 0%,rgba(16,185,129,.07) 35%,transparent 65%)}
.logo{position:absolute;left:80px;top:72px;height:44px}
.count{position:absolute;right:86px;top:80px;font-family:JBM;font-size:24px;letter-spacing:.32em;color:#8A8A92}
.kicker{font-family:JBM;font-weight:500;color:#10B981;font-size:24px;letter-spacing:.42em;display:flex;align-items:center;gap:18px;text-transform:uppercase}
.kicker:before{content:'';width:34px;height:3px;background:#10B981;display:block}
.h{font-weight:800;letter-spacing:-.055em;line-height:.98;background:linear-gradient(180deg,#fff 25%,#BFC0C7 85%);-webkit-background-clip:text;color:transparent}
.h .g{background:none;-webkit-text-fill-color:#10B981;color:#10B981}
.g{color:#10B981}
.p{font-weight:400;color:#A6A6AE;font-size:36px;line-height:1.38;letter-spacing:-.01em}
.p b{color:#fff;font-weight:600}
.foot{position:absolute;left:86px;right:86px;bottom:66px;display:flex;justify-content:space-between;align-items:center;font-family:JBM;font-size:22px;letter-spacing:.34em;color:#8A8A92}
.foot .arr{color:#E5E5E8;display:flex;align-items:center;gap:18px}
.card{background:#121214;border:1px solid rgba(255,255,255,.08);border-radius:28px}
.mono{font-family:JBM}
.chip{display:inline-block;font-family:JBM;font-size:20px;letter-spacing:.12em;padding:8px 16px;border-radius:999px;border:1px solid rgba(255,255,255,.14);color:#C9CAD0}
"""
ARROW = '<svg width="68" height="18" viewBox="0 0 68 18"><path d="M0 9h64M56 1l8 8-8 8" stroke="#E5E5E8" stroke-width="2" fill="none"/></svg>'

def html(body, css=''):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}{css}</style></head><body>{body}</body></html>"

def render(body, out, w, h, css='', transparent=False):
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, dir=S+'/build') as f:
        f.write(html(body, css)); p = f.name
    env = dict(os.environ, TRANSPARENT='1' if transparent else '0')
    subprocess.run(['node', S+'/build/render.mjs', p, out, str(w), str(h)], check=True, env=env)
    os.unlink(p)
    return out

def logo(): return f"<img class='logo' src='file://{B}logo_wordmark.png'>"
