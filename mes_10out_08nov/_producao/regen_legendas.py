import render_month as RM, carousels as CA, importlib
n = 0
for m in ['month_w1', 'month_w2', 'month_w3', 'month_w4']:
    M = importlib.import_module(m)
    for k in M.SPECS:
        open(RM.folder(k) + '/legenda.txt', 'w').write(RM.legenda(k)); n += 1
for k in CA.CAR:
    t = RM.legenda(k).replace('FORMATO: Carrossel de fotos', 'FORMATO: Carrossel de fotos (modo foto do TikTok, 9:16)')
    t = t.replace('(a versão desta pasta já está pronta com vídeo real de banco de imagens)', '(a versão desta pasta já está pronta com fotos reais de banco de imagens)')
    t += "\nCOMO POSTAR: no TikTok, + > Foto > selecione 01.jpg…%02d.jpg na ordem > adicione o som > cole a legenda.\n" % len(CA.CAR[k])
    open(RM.folder(k) + '/legenda.txt', 'w').write(t); n += 1
print(n)
