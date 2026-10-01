import sys, os, re, subprocess, importlib, unicodedata, time
from multiprocessing import Pool
sys.path.insert(0, '/home/user/posts_instagram_tiktok_epiverso/mes_10out_08nov/_dados')
import tiktok_1, tiktok_2, tiktok_3
TT = tiktok_1.TT + tiktok_2.TT + tiktok_3.TT
REPO = '/home/user/posts_instagram_tiktok_epiverso/mes_10out_08nov/tiktok'
DOW = {'10/10':'sáb','11/10':'dom','12/10':'seg (feriado)','13/10':'ter','14/10':'qua','15/10':'qui','16/10':'sex'}
def wd(date):
    import datetime
    d, m = map(int, date.split('/')); y = 2026
    n = ['seg','ter','qua','qui','sex','sáb','dom'][datetime.date(y, m, d).weekday()]
    return n + (' (feriado)' if date in ('12/10', '02/11') else '')
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'[^a-z0-9]+', '_', s).strip('_'); return s[:40].rstrip('_')
def entry(key):
    dm, h = key.split('_'); date = dm[:2] + '/' + dm[2:]
    for t in TT:
        if t[0] == date and t[1].replace('h', '') == h.replace('h', ''): return t
    raise KeyError(key)
def folder(key):
    t = entry(key); hh = t[1] if 'h' in t[1] else t[1]
    return f"{REPO}/{t[0][:2]}-{t[0][3:]}_{hh}_{slug(t[2].split('·')[-1] if '·' in t[2] else t[2])}"
CODES = {'G': 'gravar com a equipe no celular', 'S': 'vídeo de banco de imagens + texto', 'T': 'gravação de tela do Painel',
         'D': 'fotos/design', 'I': 'vídeo com IA'}
def prod_txt(p):
    out = re.sub(r"\b([GSTDI])\b", lambda m: CODES[m.group(1)], p.strip())
    return out + ' (a versão desta pasta já está pronta com vídeo real de banco de imagens)'
def has_vo(key):
    for m in ('month_w1', 'month_w2', 'month_w3', 'month_w4'):
        M = importlib.import_module(m)
        if key in M.SPECS: return bool(M.SPECS[key].get('vo'))
    return False
def som_txt(key, som):
    if has_vo(key):
        return som + ' (a narração já está no vídeo; música, se usar, bem baixa)'
    if 'sem m' in som.lower() or '5%' in som:
        return 'Som leve da CML a 20–30% (esta versão é só texto na tela). Se a equipe regravar falando: ' + som.lower()
    return som
def legenda(key, fmt_note=''):
    t = entry(key)
    date, hour, title, fmt, dur, hook, rot, leg, tags, som, prod = t
    return f"""{title}
POSTAR: {date}/2026 ({wd(date)}) às {hour}
FORMATO: {fmt} · {dur}{fmt_note}

LEGENDA (copiar e colar):
{leg}

{tags}

SOM: {som_txt(key, som)}
(adicione o som pelo próprio app do TikTok na hora de postar; sons da Biblioteca Comercial (CML) são os liberados para perfil de empresa)

GANCHO NA TELA: {hook}

VERSÃO GRAVADA PELA EQUIPE (se quiserem refazer com o pessoal do escritório):
{rot}
Produção sugerida: {prod_txt(prod)}
"""
def do(args):
    mod, key = args
    from engine import build
    M = importlib.import_module(mod); spec = dict(M.SPECS[key]); spec['id'] = key
    out = folder(key); os.makedirs(out, exist_ok=True)
    t0 = time.time()
    build(spec, out + '/video.mp4')
    dur = sum(s['d'] for s in spec['scenes'])
    subprocess.run(['ffmpeg','-v','error','-y','-ss', str(min(1.2, dur/3)), '-i', out+'/video.mp4','-frames:v','1','-q:v','3', out+'/capa.jpg'], check=True)
    open(out + '/legenda.txt', 'w').write(legenda(key))
    return f'{key} {dur:.1f}s em {time.time()-t0:.0f}s'
if __name__ == '__main__':
    mod = sys.argv[1]; keys = sys.argv[2:]
    M = importlib.import_module(mod)
    keys = keys or list(M.SPECS)
    with Pool(int(os.environ.get('J', 3))) as p:
        for r in p.imap_unordered(do, [(mod, k) for k in keys]): print(r, flush=True)
