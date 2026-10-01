"""Reels do Instagram na identidade Epiverso: clipes reais + Inter/verde + tela final."""
import os, sys, subprocess
from month_lib import *
from engine import build, caption_chunks
from vo_texts import V
import ig_lib
REPO = ig_lib.REPO
GRAD = ("<div style='position:absolute;left:0;right:0;top:0;height:560px;background:linear-gradient(180deg,rgba(10,10,10,.85),rgba(10,10,10,0))'></div>"
        "<div style='position:absolute;left:0;right:0;bottom:0;height:820px;background:linear-gradient(0deg,rgba(10,10,10,.92) 10%,rgba(10,10,10,0))'></div>")
LOGO = f"<img src='file://{B}logo_wordmark.png' style='position:absolute;left:80px;top:150px;height:40px'>"
def HEAD(kicker, title, top=930):
    return (f"<div style='position:absolute;left:80px;right:150px;top:{top}px;font-family:Inter'>"
            f"<div style='font-family:JBM;color:#10B981;font-size:26px;letter-spacing:.38em;text-transform:uppercase;display:flex;gap:16px;align-items:center'><span style='width:34px;height:3px;background:#10B981;display:block'></span>{kicker}</div>"
            f"<div style='font-weight:800;font-size:84px;letter-spacing:-.05em;line-height:1;color:#fff;margin-top:22px;text-shadow:0 4px 30px rgba(0,0,0,.5)'>{title}</div></div>")
def CAP(txt, top=1290):
    return (f"<div style='position:absolute;left:80px;right:150px;top:{top}px;font-family:Inter;font-weight:800;font-size:64px;letter-spacing:-.035em;line-height:1.08;color:#fff;"
            f"text-shadow:0 3px 18px rgba(0,0,0,.75)'>{txt}</div>")
def LINE(txt, top=1180, size=72):
    return (f"<div style='position:absolute;left:80px;right:150px;top:{top}px;font-family:Inter;font-weight:800;font-size:{size}px;letter-spacing:-.045em;line-height:1.02;color:#fff;"
            f"text-shadow:0 3px 18px rgba(0,0,0,.7)'>{txt}</div>")
def END(line, sub):
    return ("<div style='position:absolute;inset:0;background:#0A0A0A'></div>"
            "<div style='position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:54px 54px;-webkit-mask-image:radial-gradient(ellipse 90% 60% at 80% 10%,#000,transparent 80%)'></div>"
            "<div style='position:absolute;width:1200px;height:1200px;right:-500px;top:-500px;background:radial-gradient(circle,rgba(16,185,129,.25),transparent 65%)'></div>"
            f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 110px;font-family:Inter'>"
            f"<img src='file://{B}logo_stack.png' style='height:300px'>"
            f"<div style='font-weight:800;font-size:76px;letter-spacing:-.05em;line-height:1.04;color:#fff;margin-top:90px'>{line}</div>"
            f"<div style='font-family:JBM;font-size:26px;letter-spacing:.32em;color:#8A8A92;margin-top:44px'>{sub}</div></div>")
PROD = ('robo_sync', 'pasta_xml', 'painel_pronto', 'busca', 'danfe', 'zip')
def chrome(scenes):
    """logo + degradê só nas cenas de pessoas (as telas do produto já têm o próprio logo)"""
    ov = []; t = 0
    for s_ in scenes:
        if s_['clip'] not in ('r04', 'r08'): ov += [(GRAD, t, t + s_['d']), (LOGO, t, t + s_['d'])]
        t += s_['d']
    return ov
def reel_vo(vo, kicker, title, broll, end_line, end_sub='SALVE PARA O FECHAMENTO'):
    e = EDU(vo, title, broll)
    scenes = e['scenes']; scenes[0]['ov'] = []
    total = sum(s['d'] for s in scenes)
    scenes.append(sc('sala_noite', 2.8, z=1.0))
    ov = chrome(scenes[:-1]) + [(HEAD(kicker, title), 0, 3.6)]
    words = {}
    for txt, a, b in caption_chunks(e['vo'], V[vo], e['vo_at']):
        ov.append((CAP(txt), a, min(b, total)))
    ov.append((END(end_line, end_sub), total, total + 2.8))
    return dict(scenes=scenes, ov=ov, vo=e['vo'], vo_at=e['vo_at'], sfx=[('whoosh', total - 0.15, .3)])
def reel_lines(kicker, title, lines, end_line, end_sub, sfx=None):
    """lines: [(clip, dur, text)]"""
    scenes = []; ov = []; t = 0
    for i, (clip, d, txt) in enumerate(lines):
        prod = clip in ('robo_sync', 'pasta_xml', 'painel_pronto', 'busca', 'danfe', 'zip')
        scenes.append(sc(clip, d, z=1.0 if prod else 1.05))
        if txt: ov.append((LINE(txt, top=1490 if prod else 1250), t + .15, t + d - .02))
        t += d
    total = t
    scenes.append(sc('sala_noite', 2.8, z=1.0))
    ov = chrome(scenes[:-1]) + [(HEAD(kicker, title), 0, lines[0][1])] + ov
    ov.append((END(end_line, end_sub), total, total + 2.8))
    s = sfx or []
    return dict(scenes=scenes, ov=ov, sfx=s + [('whoosh', total - 0.15, .3)])
TG = ig_lib
R = {}
R['13-10_reels_ache_qualquer_nota'] = (reel_lines('Painel Fiscal', 'Ache qualquer nota <span style="color:#10B981">em 3 segundos.</span>', [
    ('focada2', 2.8, None),
    ('busca', 4.0, 'Digite o número, o CNPJ ou o nome.'),
    ('danfe', 2.2, 'O DANFE abre na hora.'),
    ('zip', 1.7, 'O mês inteiro? Um ZIP.'),
    ('comemora', 2.8, 'Sem portal. Sem pedir pro cliente.'),
  ], 'Comente <span style="color:#10B981">BUSCA</span> e veja numa demonstração.', 'PAINEL FISCAL · EPIVERSO',
  sfx=[('typing', 3.2, .35), ('ding', 6.8, .3), ('click', 9.0, .3), ('ding', 10.7, .3)]),
  ('Reels · ache qualquer nota em 3 segundos', '13/10/2026 (ter) às 18h30',
   'Cliente jurando que a nota não existe? 🔎 No Painel Fiscal você digita o número, o CNPJ ou o nome e a nota aparece, com o DANFE na hora.\n\nComente BUSCA que a gente te mostra numa demonstração.\n\n(telas de demonstração, empresas fictícias)',
   '#notafiscal #xml #contabilidade #escritoriocontabil #automacaocontabil',
   'Instrumental leve e moderno da biblioteca do Instagram (ex.: procure "tech minimal" ou "corporate upbeat") a 20–30%.'))
R['16-10_reels_cliente_vai_pagar_mais'] = (reel_vo('R2', 'Reforma tributária', 'O cliente vai pagar <span style="color:#10B981">mais imposto?</span>',
    ['madura_tel', 'danfe', 'tel_calma', 'focada2'], 'Salve a resposta <span style="color:#10B981">antes do cliente ligar.</span>'),
  ('Reels · IBS e CBS: o cliente vai pagar mais?', '16/10/2026 (sex) às 12h',
   'A pergunta que mais vai chegar no seu WhatsApp: "vou pagar mais imposto?" Em 2026, não. 📌\n\nCBS 0,9% e IBS 0,1% em fase de teste, compensáveis com PIS e Cofins. O que muda é o XML e o PDF da nota.\n\nSalve e mande para o cliente.',
   '#reformatributaria #ibscbs #contabilidade #contador #escritoriocontabil', 'Voz já no vídeo. Música opcional bem baixa (5–10%), instrumental calmo.'))
R['19-10_reels_um_dia_no_escritorio'] = (reel_lines('Bastidores', 'Um dia num escritório contábil, <span style="color:#10B981">sem filtro.</span>', [
    ('chega', 3.2, None),
    ('focada', 3.0, '8h · liga os monitores e abre o painel'),
    ('painel_pronto', 3.4, '9h · as notas da noite já estão lá'),
    ('cafe_grupo', 3.0, '10h30 · café rápido'),
    ('tel_calma', 3.0, '15h · cliente com dúvida do DAS'),
    ('quadro', 3.0, '17h · prazos da semana no quadro'),
    ('tchau', 3.0, '18h · até amanhã'),
  ], 'Rotina organizada <span style="color:#10B981">não é rotina corrida.</span>', 'PAINEL FISCAL · EPIVERSO',
  sfx=[('pop', 3.2, .2), ('pop', 6.2, .2), ('pop', 9.6, .2), ('pop', 12.6, .2), ('pop', 15.6, .2), ('pop', 18.6, .2)]),
  ('Reels · um dia no escritório', '19/10/2026 (seg) às 18h30',
   'Um dia normal num escritório contábil, sem filtro e sem pilha infinita de papel. ☕\n\nComo é a rotina aí? Conta nos comentários.',
   '#contabilidade #contador #escritoriocontabil #rotina #vidadecontador', 'Áudio em alta do Instagram, leve (estilo "day in my life"), escolhido no app no dia.'))
R['22-10_reels_simples_2027'] = (reel_vo('R3', 'Simples Nacional', 'Simples em 2027: <span style="color:#10B981">o que muda na nota.</span>',
    ['tel_explica', 'focada', 'anota_mesa', 'sorri_laptop'], 'Pergunte ao emissor <span style="color:#10B981">hoje. Por escrito.</span>'),
  ('Reels · Simples Nacional em 2027', '22/10/2026 (qui) às 12h',
   'Em janeiro de 2027 o Simples Nacional passa a preencher IBS e CBS na nota (fase de teste). 🗓️\n\nQuem emite por sistema próprio ou emissor antigo precisa perguntar ao fornecedor se a versão nova já está pronta.\n\nSalve e marque quem cuida do Simples aí.',
   '#simplesnacional #reformatributaria #ibscbs #contabilidade #contador', 'Voz já no vídeo. Música opcional bem baixa (5–10%).'))
R['26-10_reels_cfop_em_20_segundos'] = (reel_vo('G3', 'Glossário', 'CFOP em <span style="color:#10B981">20 segundos.</span>',
    ['postits', 'focada', 'teclado', 'preocupada'], 'Mande para o cliente que <span style="color:#10B981">chuta o CFOP.</span>', 'MANDE PARA O CLIENTE'),
  ('Reels · CFOP em 20 segundos', '26/10/2026 (seg) às 18h30',
   'CFOP é o código da natureza da operação: 5 ou 6 na saída, 1 ou 2 na entrada. Errou o CFOP, errou o faturamento (e o limite do Simples). 🧾\n\nMande para aquele cliente.',
   '#cfop #notafiscal #fiscal #contabilidade #contador', 'Voz já no vídeo. Música opcional bem baixa (5–10%).'))
R['28-10_reels_o_xml_mudou'] = (reel_vo('R6', 'Reforma tributária', 'O XML mudou: <span style="color:#10B981">onde ficam IBS e CBS.</span>',
    ['teclado', 'pasta_xml', 'focada', 'danfe', 'sorri_laptop'], 'Comente <span style="color:#10B981">XML</span> e veja o relatório com coluna por imposto.'),
  ('Reels · o XML mudou', '28/10/2026 (qua) às 12h',
   'Dentro de cada item agora tem o grupo IBSCBS: CST, cClassTrib, base, alíquota e valor. Se o sistema que confere não lê esse grupo, o relatório do mês fica incompleto. 🔍\n\nComente XML que a gente te mostra o relatório do Painel com coluna por imposto.',
   '#xml #ibscbs #reformatributaria #contabilidade #escritoriocontabil', 'Voz já no vídeo. Música opcional bem baixa (5–10%).'))
R['31-10_reels_erro_do_esocial'] = (reel_vo('DP2', 'Departamento pessoal', 'O erro de eSocial <span style="color:#10B981">que mais aparece.</span>',
    ['estagiario', 'teclado', 'tel_anota', 'focada2'], 'Combine com o cliente: admissão <span style="color:#10B981">antes do 1º dia.</span>', 'SALVE PARA O DP'),
  ('Reels · erro de eSocial', '31/10/2026 (sáb) às 10h',
   'Admissão enviada depois que a pessoa já começou a trabalhar: o erro de eSocial que mais aparece no fim do mês. 📋\n\nCombine com o cliente, por escrito, que a admissão chega antes do primeiro dia.',
   '#esocial #departamentopessoal #contabilidade #contador #escritoriocontabil', 'Voz já no vídeo. Música opcional bem baixa (5–10%).'))
R['03-11_reels_3_perguntas_do_cliente'] = (reel_vo('R5', 'Reforma tributária', '3 perguntas que o cliente <span style="color:#10B981">vai te fazer.</span>',
    ['madura_tel', 'tel_calma', 'focada', 'tel_explica', 'sorri_laptop'], 'Salve as respostas e <span style="color:#10B981">ganhe tempo no telefone.</span>'),
  ('Reels · 3 perguntas sobre IBS/CBS', '03/11/2026 (ter) às 12h',
   'Vou pagar mais? Por que minha nota mudou? Preciso fazer alguma coisa? As 3 perguntas sobre IBS e CBS (com as respostas). 📞\n\nSalve e use no atendimento.',
   '#reformatributaria #ibscbs #contabilidade #contador #escritoriocontabil', 'Voz já no vídeo. Música opcional bem baixa (5–10%).'))
R['06-11_reels_reforma_em_3_frases'] = (reel_vo('R8', 'Reforma tributária', 'A reforma em <span style="color:#10B981">3 frases.</span>',
    ['tel_explica', 'madura_tel', 'focada', 'sorri_laptop'], 'Sem palestra. <span style="color:#10B981">Salve e use.</span>'),
  ('Reels · a reforma em 3 frases', '06/11/2026 (sex) às 18h30',
   'Como explicar a reforma tributária para o cliente em 3 frases (sem palestra). 💬\n\n1. Vários impostos sobre consumo viram dois: IBS e CBS.\n2. A transição é longa, vai até 2033.\n3. Por enquanto muda a nota e a conferência, e o escritório cuida disso.',
   '#reformatributaria #ibscbs #contabilidade #contador #escritoriocontabil', 'Voz já no vídeo. Música opcional bem baixa (5–10%).'))
def cover_img(folder, photo, kicker, title):
    """capa 1080x1920 com o título no centro (área que aparece no grid 4:5)"""
    from kit import render
    img = ig_lib.still45(photo)
    body = (f"<div class='stage'><img src='file://{img}' style='position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.7) saturate(.9)'>"
            "<div style='position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.2),rgba(10,10,10,.85) 70%)'></div>"
            f"<img src='file://{B}logo_wordmark.png' style='position:absolute;left:86px;top:330px;height:44px'>"
            f"<div style='position:absolute;left:86px;right:86px;top:1050px'><div class='kicker'>{kicker}</div>"
            f"<div class='h' style='font-size:104px;margin-top:28px'>{title}</div></div></div>")
    render(body, f'{folder}/capa.png', 1080, 1920)
    subprocess.run(['convert', f'{folder}/capa.png', '-quality', '92', f'{folder}/capa.jpg']); os.unlink(f'{folder}/capa.png')
COV = {'13-10_reels_ache_qualquer_nota': ('focada2', 'Painel Fiscal', 'Ache qualquer nota <span class="g">em 3 segundos.</span>'),
       '16-10_reels_cliente_vai_pagar_mais': ('madura_tel', 'Reforma tributária', 'O cliente vai pagar <span class="g">mais imposto?</span>'),
       '19-10_reels_um_dia_no_escritorio': ('chega', 'Bastidores', 'Um dia num escritório contábil, <span class="g">sem filtro.</span>'),
       '22-10_reels_simples_2027': ('tel_explica', 'Simples Nacional', 'Simples em 2027: <span class="g">o que muda.</span>'),
       '26-10_reels_cfop_em_20_segundos': ('focada', 'Glossário', 'CFOP em <span class="g">20 segundos.</span>'),
       '28-10_reels_o_xml_mudou': ('teclado', 'Reforma tributária', 'O XML mudou: <span class="g">onde ficam IBS e CBS.</span>'),
       '31-10_reels_erro_do_esocial': ('estagiario', 'Departamento pessoal', 'O erro de eSocial <span class="g">que mais aparece.</span>'),
       '03-11_reels_3_perguntas_do_cliente': ('madura_tel', 'Reforma tributária', '3 perguntas que o cliente <span class="g">vai te fazer.</span>'),
       '06-11_reels_reforma_em_3_frases': ('tel_explica', 'Reforma tributária', 'A reforma em <span class="g">3 frases.</span>')}
def do(key):
    spec, (title, when, text, tags, music) = R[key]
    spec = dict(spec); spec['id'] = 'ig_' + key
    out = f'{REPO}/{key}'; os.makedirs(out, exist_ok=True)
    build(spec, out + '/video.mp4')
    cover_img(out, *COV[key])
    dur = sum(s['d'] for s in spec['scenes'])
    open(out + '/legenda.txt', 'w').write(ig_lib.LEG(title, when, f'Reels 9:16 · {dur:.0f} s (capa: capa.jpg, título centralizado para o grid 4:5)', text, tags,
        'Vídeo com pessoas reais em escritório e textos na tela; transcrição na legenda automática do Instagram.', music,
        '\nAO POSTAR: ative "legendas automáticas", use capa.jpg como capa e compartilhe no feed. Responda os comentários na primeira hora.\n'))
    return key + f' {dur:.1f}s'
if __name__ == '__main__':
    from multiprocessing import Pool
    keys = sys.argv[1:] or list(R)
    with Pool(int(os.environ.get('J', 2))) as p:
        for r in p.imap_unordered(do, keys): print(r, flush=True)
