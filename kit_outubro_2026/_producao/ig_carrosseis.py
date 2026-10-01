import os, sys
from kit import *
OUT = S + '/out/instagram'
W, H = 1080, 1350

def photo(name, pos='center', filt='saturate(.92) contrast(1.04) brightness(.92)'):
    return f"<img src='file://{AI}{name}.webp' style='position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos};filter:{filt}'>"

def shade(top=.55, bottom=.96, start=38):
    return (f"<div style='position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,{top}) 0%,rgba(10,10,10,0) 22%,"
            f"rgba(10,10,10,0) {start}%,rgba(10,10,10,.82) {start+22}%,rgba(10,10,10,{bottom}) 100%)'></div>")

def frame(inner, n=None, total=None, foot_left='PAINEL FISCAL', arrow=True, grid=True):
    cnt = f"<div class='count'>{n:02d} / {total:02d}</div>" if n else ''
    g = "<div class='grid'></div><div class='glow'></div>" if grid else ''
    ar = f"<span class='arr'>ARRASTE {ARROW}</span>" if arrow else '<span></span>'
    return f"<div class='stage'>{g}{inner}{logo()}{cnt}<div class='foot'><span>{foot_left}</span>{ar}</div></div>"

def save(folder, i, body):
    os.makedirs(f'{OUT}/{folder}', exist_ok=True)
    render(body, f'{OUT}/{folder}/{i:02d}.png', W, H)

# ---------------------------------------------------------------- IG 02: Faltam 92 dias
F = '02_carrossel_faltam_92_dias'; T = 8
def ig2():
    # 1 capa (foto Marcos)
    save(F, 1, frame(photo('marcos_calendario', 'center 30%') + shade(.6, .97, 30) + f"""
      <div style='position:absolute;left:86px;right:86px;bottom:150px'>
        <div class='kicker'>Reforma tributária</div>
        <div class='h' style='font-size:104px;margin-top:30px'>Faltam <span class='g'>92 dias</span> para o Simples entrar no IBS/CBS.</div>
        <div class='p' style='margin-top:30px;color:#C9CAD0'>O checklist que o seu escritório precisa fechar até 01/01/2027.</div>
      </div>""", 1, T, grid=False))
    # 2 linha do tempo
    rows = [('03/08/2026', 'NF-e e NFC-e do regime normal', 'Campos IBS/CBS obrigatórios', False),
            ('01/10/2026', 'NFS-e', 'Passa a trazer IBS e CBS', False),
            ('01/01/2027', 'Empresas do Simples Nacional', 'Entram na fase de teste', True)]
    tl = ''.join(f"""<div style='display:flex;gap:34px;align-items:flex-start;padding:30px 0;border-top:1px solid rgba(255,255,255,.08)'>
        <div class='mono' style='font-size:26px;letter-spacing:.06em;color:{"#10B981" if hi else "#8A8A92"};width:220px;padding-top:6px'>{d}</div>
        <div><div style='font-size:40px;font-weight:700;letter-spacing:-.03em;color:{"#10B981" if hi else "#fff"}'>{a}</div>
        <div style='font-size:30px;color:#A6A6AE;margin-top:6px'>{b}</div></div></div>""" for d, a, b, hi in rows)
    save(F, 2, frame(f"""<div style='position:absolute;left:86px;right:86px;top:190px'>
        <div class='kicker'>O que muda</div>
        <div class='h' style='font-size:84px;margin-top:34px'>A reforma chega por etapas. <span class='g'>A próxima é a do Simples.</span></div>
        <div style='margin-top:56px'>{tl}</div>
        <div class='mono' style='font-size:24px;color:#7A7A82;margin-top:30px;letter-spacing:.04em;line-height:1.6'>2026–2027: fase de teste. CBS 0,9% e IBS 0,1%, sem aumento de carga.<br>Confira sempre a Nota Técnica vigente.</div>
      </div>""", 2, T))
    # 3-7 checklist
    items = [
      ('Mapeie a carteira.', 'Liste os clientes do Simples, o que cada um emite e qual emissor usa.',
       """<div class='card' style='padding:30px 34px'>""" + ''.join(f"""<div style='display:flex;justify-content:space-between;align-items:center;padding:16px 0;{"border-top:1px solid rgba(255,255,255,.07);" if k else ""}font-size:28px'>
          <span style='font-weight:600'>{c}</span><span class='chip'>{m}</span><span class='mono' style='color:{col};font-size:24px'>{s}</span></div>"""
          for k, (c, m, s, col) in enumerate([('Padaria Aurora', 'NFC-e', 'pronto', '#10B981'), ('Ferragem Exemplo', 'NF-e', 'pendente', '#F59E0B'), ('Clínica Exemplo', 'NFS-e', 'pendente', '#F59E0B'), ('Café Exemplo', 'NFC-e', 'sem resposta', '#EF4444')])) + "</div>"),
      ('Cobre o emissor.', 'Peça ao fornecedor do sistema de cada cliente a versão com o grupo IBSCBS. Por escrito, com data.',
       """<div class='card mono' style='padding:34px 38px;font-size:28px;line-height:1.7;color:#C9CAD0'>
          <span style='color:#6E6E76'>&lt;det nItem="1"&gt;</span><br>&nbsp;&nbsp;<span class='g'>&lt;IBSCBS&gt;</span><br>&nbsp;&nbsp;&nbsp;&nbsp;&lt;CST&gt;000&lt;/CST&gt;<br>&nbsp;&nbsp;&nbsp;&nbsp;&lt;cClassTrib&gt;000001&lt;/cClassTrib&gt;<br>&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#6E6E76'>...</span><br>&nbsp;&nbsp;<span class='g'>&lt;/IBSCBS&gt;</span></div>"""),
      ('Classifique os itens.', 'CST e cClassTrib por produto e serviço. Comece pelos itens que mais aparecem nas notas.',
       """<div class='card' style='padding:30px 34px'>""" + ''.join(f"""<div style='display:grid;grid-template-columns:1fr 120px 190px;align-items:center;padding:15px 0;{"border-top:1px solid rgba(255,255,255,.07);" if k else ""}font-size:27px'>
          <span>{p}</span><span class='mono' style='color:#C9CAD0'>{c}</span><span class='mono' style='color:{"#10B981" if t!="?" else "#F59E0B"}'>{t}</span></div>"""
          for k, (p, c, t) in enumerate([('Pão de forma 500 g', '000', '000001'), ('Bolo de laranja', '000', '000001'), ('Serviço de entrega', '000', '?'), ('Kit café da manhã', '?', '?')])) + "</div>"),
      ('Teste em dezembro.', 'Uma nota-teste por cliente, com o XML conferido. Não descubra em janeiro que o emissor não estava pronto.',
       """<div style='zoom:.8'><div style='display:grid;grid-template-columns:repeat(7,1fr);gap:12px'>""" + ''.join(
          f"<div class='card mono' style='height:70px;display:flex;align-items:center;justify-content:center;font-size:30px;border-radius:18px;{'background:#10B981;color:#0A0A0A;font-weight:700;border-color:#10B981' if d in (15,16,17) else ('color:#8A8A92' if d<=31 else 'opacity:0')}'>{d if d<=31 else ''}</div>" for d in range(1, 32)) + "</div><div class='mono' style='font-size:22px;color:#8A8A92;margin-top:20px;letter-spacing:.2em'>DEZEMBRO · 15 A 17: SEMANA DE TESTE</div></div>"),
      ('Defina quem confere.', 'Todo mês alguém precisa olhar se os campos vieram certos. Quem? Com qual ferramenta? Em quanto tempo?',
       """<div class='card' style='padding:34px 38px;display:flex;flex-direction:column;gap:22px;font-size:30px'>
          <div style='display:flex;justify-content:space-between'><span style='color:#A6A6AE'>Responsável</span><span style='font-weight:600'>Ana · fiscal</span></div>
          <div style='display:flex;justify-content:space-between'><span style='color:#A6A6AE'>Ferramenta</span><span style='font-weight:600'>Painel Fiscal</span></div>
          <div style='display:flex;justify-content:space-between'><span style='color:#A6A6AE'>Quando</span><span style='font-weight:600'>dia 1º de cada mês</span></div>
          <div style='display:flex;justify-content:space-between'><span style='color:#A6A6AE'>Tempo</span><span class='g' style='font-weight:700'>minutos, não dias</span></div></div>"""),
    ]
    for k, (t, d, vis) in enumerate(items):
        save(F, 3 + k, frame(f"""<div style='position:absolute;left:86px;right:86px;top:190px'>
          <div class='kicker'>Checklist · {k+1} de 5</div>
          <div style='display:flex;align-items:baseline;gap:30px;margin-top:40px'>
            <div class='mono g' style='font-size:120px;font-weight:700;letter-spacing:-.04em;line-height:1'>0{k+1}</div>
            <div class='h' style='font-size:86px'>{t}</div></div>
          <div class='p' style='margin-top:34px'>{d}</div>
          <div style='margin-top:70px;zoom:1.3'>{vis}</div></div>""", 3 + k, T))
    # 8 CTA (foto Ana + Marcos)
    save(F, 8, frame(f"""<div style='position:absolute;left:86px;right:86px;top:170px'>
        <div class='card' style='height:430px;overflow:hidden;position:relative;border-radius:30px'>{photo('ana_marcos', 'center 40%')}</div>
        <div class='h' style='font-size:74px;margin-top:52px'>No Epiverso, o IBS/CBS <span class='g'>já aparece em cada nota.</span></div>
        <div style='margin-top:38px;display:flex;flex-direction:column;gap:18px;font-size:31px;color:#C9CAD0'>
          <div><span class='g'>→</span>&nbsp; DANFE, DACTE e DANFSe com o quadro IBS/CBS</div>
          <div><span class='g'>→</span>&nbsp; Relatórios com uma coluna por imposto</div>
          <div><span class='g'>→</span>&nbsp; Excel com CST, cClassTrib, base e alíquota por item</div></div>
        <div class='mono' style='margin-top:46px;font-size:24px;letter-spacing:.3em;color:#E5E5E8'>📌 SALVE · ENVIE PARA O FISCAL</div>
      </div>""", 8, T, arrow=False))

# ---------------------------------------------------------------- IG 03: Um dia no escritório
F3 = '03_carrossel_um_dia_no_escritorio'; T3 = 7
def tag(t):
    return f"<div class='mono' style='display:inline-flex;align-items:center;gap:14px;font-size:30px;font-weight:700;color:#0A0A0A;background:#10B981;padding:10px 20px;border-radius:12px;letter-spacing:.06em'>{t}</div>"
def ig3():
    save(F3, 1, frame(photo('ana_saindo', 'center 25%') + shade(.55, .97, 34) + f"""
      <div style='position:absolute;left:86px;right:86px;bottom:150px'>
        {tag('18:02 · DIA 19')}
        <div class='h' style='font-size:100px;margin-top:30px'>Véspera do DAS. <span class='g'>E ela já está indo embora.</span></div>
        <div class='p' style='margin-top:26px;color:#C9CAD0'>Arraste e veja o dia de um escritório que parou de baixar XML.</div>
      </div>""", 1, T3, grid=False))
    scenes = [
      ('escritorio_meianoite', 'center', '00:00', 'Ninguém no escritório.', 'O robô busca as notas de todos os clientes na SEFAZ. NF-e, NFC-e, CT-e e NFS-e.',
       "<div class='card mono' style='position:absolute;right:86px;top:190px;padding:22px 26px;font-size:22px;line-height:1.9;color:#C9CAD0;background:rgba(18,18,20,.88);backdrop-filter:blur(8px)'><span class='g'>● robô · sincronizando</span><br>Padaria Aurora · NFC-e &nbsp;<span class='g'>+1.284</span><br>Ferragem Exemplo · NF-e &nbsp;<span class='g'>+312</span><br>Canceladas conferidas &nbsp;<span class='g'>✓</span></div>"),
      ('ana_cafe', 'center 30%', '07:40', 'O painel já está pronto.', 'Cada XML na pasta certa: cliente, mês e modelo. Canceladas marcadas e fora da soma.', ''),
      ('ana_telefone2', 'center 30%', '10:15', 'A nota 4.812 de março? Achou em 5 segundos.', 'Número, nome, CNPJ ou chave. O PDF abre na hora, ainda na ligação.', ''),
      ('ana_marcos', 'center 35%', '14:30', 'Um cliente chega no sublimite em novembro.', 'O alerta veio antes. Dá tempo de conversar e planejar.', ''),
      ('ana_sofa', 'center 30%', '22:00', 'Em casa. Sem notebook.', 'À meia-noite o robô começa de novo. Amanhã o painel estará pronto.', ''),
    ]
    for k, (img, pos, hh, t, d, extra) in enumerate(scenes):
        save(F3, 2 + k, frame(photo(img, pos) + shade(.55, .97, 36) + extra + f"""
          <div style='position:absolute;left:86px;right:86px;bottom:150px'>
            {tag(hh)}
            <div class='h' style='font-size:76px;margin-top:28px'>{t}</div>
            <div class='p' style='margin-top:22px;color:#C9CAD0;font-size:34px'>{d}</div>
          </div>""", 2 + k, T3, grid=False))
    save(F3, 7, frame(f"""<div style='position:absolute;left:86px;right:86px;top:250px'>
        <div class='kicker'>Painel Fiscal Epiverso</div>
        <div class='h' style='font-size:104px;margin-top:36px'>Esse dia pode ser <span class='g'>o do seu escritório.</span></div>
        <div class='p' style='margin-top:40px'>Robô às 00h e às 12h. Notas organizadas, canceladas marcadas, alerta do Simples e PDF na hora.</div>
        <div class='card' style='margin-top:70px;padding:40px 44px;display:flex;align-items:center;gap:30px'>
          <div style='font-size:64px'>💬</div>
          <div style='font-size:36px;line-height:1.35'>Comente <b class='g'>DIA</b> e a gente te mostra o painel com os clientes do seu escritório.</div></div>
      </div>""", 7, T3, arrow=False))

# ---------------------------------------------------------------- IG 04: Estático manifesto
def ig4():
    os.makedirs(f'{OUT}/04_estatico_manifesto', exist_ok=True)
    body = frame(photo('marcos_retrato', '70% 20%', 'grayscale(.35) contrast(1.08) brightness(.82)') +
      "<div style='position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,10,10,.92) 0%,rgba(10,10,10,.55) 48%,rgba(10,10,10,0) 75%),linear-gradient(180deg,rgba(10,10,10,0) 55%,rgba(10,10,10,.95) 100%)'></div>"
      "<div class='glow' style='opacity:.7'></div>" + f"""
      <div style='position:absolute;left:86px;width:700px;top:250px'>
        <div class='kicker'>Manifesto</div>
        <div class='h' style='font-size:104px;margin-top:36px'>Contador não é <span class='g'>baixador de XML.</span></div>
        <div class='p' style='margin-top:40px;color:#C9CAD0;font-size:35px'>É quem enxerga o risco antes do cliente. Deixe o robô buscar as notas. Fique com a parte que <b>só você sabe fazer.</b></div>
      </div>""", arrow=False, grid=False)
    render(body, f'{OUT}/04_estatico_manifesto/post.png', W, H)

if __name__ == '__main__':
    for f in sys.argv[1:]: globals()[f]()
