import os, re, glob, json, base64, io, subprocess, datetime, html
from PIL import Image
M = '/home/user/posts_instagram_tiktok_epiverso/mes_10out_08nov'
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/page2'
os.makedirs(OUT + '/v', exist_ok=True)
DN = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']
def b64(path, w):
    im = Image.open(path).convert('RGB'); im.thumbnail((w, 4000))
    bio = io.BytesIO(); im.save(bio, 'JPEG', quality=72, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(bio.getvalue()).decode()
def parse(txt):
    L = txt.splitlines(); d = {'title': L[0]}
    m = re.search(r'POSTAR: (\d\d)/(\d\d)/2026 \((.*?)\) às (\S+)', txt); d['dd'], d['mm'], d['hora'] = m.group(1), m.group(2), m.group(4)
    m = re.search(r'FORMATO: (.*)', txt); d['fmt'] = m.group(1)
    m = re.search(r'LEGENDA \(copiar e colar\):\n(.*?)\n\n(#[^\n]*)', txt, re.S); d['leg'] = m.group(1).strip(); d['tags'] = m.group(2).strip()
    m = re.search(r'\n(SOM|MÚSICA): (.*)', txt); d['som'] = m.group(2) if m else ''
    m = re.search(r'VERSÃO GRAVADA PELA EQUIPE.*?:\n(.*?)\n', txt); d['rot'] = m.group(1) if m else ''
    return d
def preview(src, key):
    dst = f'{OUT}/v/{key}.mp4'
    if not os.path.exists(dst):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', 'scale=432:-2', '-c:v', 'libx264', '-preset', 'medium', '-crf', '31',
                        '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', dst], check=True)
    return f'v/{key}.mp4'
posts = []
for net in ['instagram', 'tiktok']:
    for d in sorted(glob.glob(f'{M}/{net}/*/')):
        name = os.path.basename(d.rstrip('/'))
        p = parse(open(d + 'legenda.txt').read()); p['net'] = net; p['folder'] = f'{net}/{name}'
        imgs = sorted(glob.glob(d + '[0-9][0-9].jpg'))
        if os.path.exists(d + 'video.mp4'):
            p['kind'] = 'video'; p['thumb'] = b64(d + 'capa.jpg', 220); p['video'] = preview(d + 'video.mp4', f'{net[:2]}_{name}')
        elif imgs:
            p['kind'] = 'carrossel'; p['thumb'] = b64(imgs[0], 220); p['slides'] = [b64(i, 360) for i in imgs]
        else:
            p['kind'] = 'estatico'; p['thumb'] = b64(d + 'post.jpg', 220); p['slides'] = [b64(d + 'post.jpg', 540)]
        dt = datetime.date(2026, int(p['mm']), int(p['dd'])); p['date'] = dt.isoformat(); p['dow'] = DN[dt.weekday()]
        posts.append(p)
posts.sort(key=lambda p: (p['date'], 0 if p['net'] == 'instagram' else 1, p['hora'].replace('h', ':').zfill(5)))
json.dump(posts, open(OUT + '/posts.json', 'w'), ensure_ascii=False)
print(len(posts), sum(len(p.get('slides', [])) for p in posts), os.path.getsize(OUT + '/posts.json') // 1024, 'KB')
