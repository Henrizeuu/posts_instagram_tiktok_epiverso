import sys, os, re, glob, datetime, csv
sys.path.insert(0, '/home/user/posts_instagram_tiktok_epiverso/mes_10out_08nov/_dados')
import tiktok_1, tiktok_2, tiktok_3
TT = tiktok_1.TT + tiktok_2.TT + tiktok_3.TT
M = '/home/user/posts_instagram_tiktok_epiverso/mes_10out_08nov'
DN = ['seg','ter','qua','qui','sex','sáb','dom']
def dow(d):
    dd, mm = map(int, d.split('/')); return DN[datetime.date(2026, mm, dd).weekday()]
ig = {}
for f in sorted(glob.glob(M + '/instagram/*/legenda.txt')):
    L = open(f).read().splitlines()
    m = re.match(r'POSTAR: (\d\d/\d\d)/2026 \(.*?\) às (\S+)', L[1])
    ig[m.group(1)] = (m.group(2), L[0], os.path.basename(os.path.dirname(f)))
tt = {}
for t in TT:
    folder = [p for p in glob.glob(M + f"/tiktok/{t[0][:2]}-{t[0][3:]}_{t[1]}_*")]
    tt.setdefault(t[0], []).append((t[1], t[2], t[3], os.path.basename(folder[0]) if folder else '??'))
days = sorted(tt, key=lambda d: (int(d[3:]), int(d[:2])))
rows = []
md = ['| Data | Instagram (1/dia) | TikTok 1 | TikTok 2 | TikTok 3 |', '|---|---|---|---|---|']
for d in days:
    i = ig.get(d, ('', '—', ''))
    t = tt[d]
    fmt = lambda x: f"{x[0]} · {x[1]}" + (' 📸' if x[2] != 'Vídeo' else '')
    md.append(f"| {dow(d)} {d} | {i[0]} · {i[1]} | " + ' | '.join(fmt(x) for x in t) + ' |')
    rows.append([f'{d}/2026', dow(d), 'Instagram', i[0], i[1], 'instagram/' + i[2]])
    for x in t: rows.append([f'{d}/2026', dow(d), 'TikTok', x[0], x[1] + (' (carrossel de fotos)' if x[2] != 'Vídeo' else ''), 'tiktok/' + x[3]])
with open(M + '/CALENDARIO.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['data', 'dia', 'rede', 'hora', 'post', 'pasta']); w.writerows(rows)
open(S_ := M + '/_dados/calendario_tabela.md', 'w').write('\n'.join(md) + '\n')
print(len(rows), 'linhas'); print('\n'.join(md[:6]))
