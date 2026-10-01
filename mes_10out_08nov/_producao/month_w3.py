from month_lib import *
SPECS = {}
P = lambda n: [('pop', t, .2) for t in n]
# ---------- 24/10 (sáb) ----------
SPECS['2410_10h'] = dict(scenes=M([
  ('notif_mesa', 3.4, 'coisas que só quem trabalha em escritório contábil entende (parte 6)', None,
   [(NOTIF('E-mail · Cliente', 'URGENTE · "oi tudo bem?" (sem anexo)', '08:03', top=900), 0.6, None)]),
  ('focada2', 3.2, 'achar 3 tokens A3 iguais na gaveta, sem etiqueta'),
  ('estagiario', 3.2, 'estagiário: "é pra lançar ou pra conferir?"', 'todo mundo: "CONFERIR."'),
]), sfx=[('notify', 0.6, .45), ('pop', 3.4, .2), ('pop', 6.6, .2)])
SPECS['2410_20h'] = dict(scenes=[
  sc('sem_expressao', 6.4, z=1.08, ov=[(T('a cara que eu faço quando o cliente diz que "o contador anterior fazia de graça"', top=TOP), 0, None),
     (T('…', top=1250, style='stroke', size=110), 3.6, None)]),
], sfx=[('pop', 3.6, .2)])
# ---------- 25/10 (dom) ----------
SPECS['2510_10h'] = EDU('DP1', '13º: 1ª parcela até 30/11 (avisa o cliente agora)', ['estagiario', 'anota_mesa', 'tel_calma', 'teclado2'])
SPECS['2510_15h'] = dict(scenes=M([
  ('chega_le', 3.4, 'tipos de cliente: o que manda a nota certa, no dia certo, com tudo organizado'),
  ('equipe_monitor', 3.2, 'chamando a equipe pra ver'),
  ('cafe_duas', 3.0, 'a colega:', '"emoldura." 🖼️'),
]), sfx=P([3.4, 6.6]))
SPECS['2510_20h'] = dict(scenes=[
  sc('sala_noite', 3.0, z=1.06, ov=[(T('domingo, 00h: o escritório dorme', top=TOP), 0, None), (CLOCK('00:00', top=820, left=340), 0.3, None)]),
  sc('robo_sync', 3.4, z=1.0, ov=[(T('o robô não 🤖 · baixando cliente por cliente', top=1420), 0, None)]),
  sc('pasta_xml', 3.0, z=1.0, ov=[(T('segunda 8h: tudo na pasta certa', top=1420), 0, None)]),
], sfx=[('tick', 0.3, .3), ('click', 3.4, .25), ('ding', 8.8, .3)])
# ---------- 26/10 (seg) ----------
SPECS['2610_0730'] = EDU('R6', 'o XML mudou: onde ficam IBS e CBS', ['teclado', 'pasta_xml', 'focada', 'danfe', 'sorri_laptop'])
SPECS['2610_1215'] = dict(scenes=M([
  ('cel_olha_longe', 2.6, 'cliente diz vs contador entende (edição abertura de empresa)'),
  ('tel_calma', 3.2, '"já abri a empresa"', 'abriu o MEI com a atividade errada'),
  ('madura_tel', 3.2, '"é só comércio"', 'tem serviço também'),
  ('tel_serio', 3.2, '"não tenho funcionário"', 'tem o primo que ajuda'),
]), sfx=P([2.6, 5.8, 9.0]))
SPECS['2610_1930'] = dict(scenes=TX([
  ('o que faz uma assistente fiscal (de verdade)', 3.2),
  ('confere notas de entrada e saída', 3.0),
  ('olha as canceladas antes de fechar o mês', 3.0),
  ('gera o relatório do mês', 2.8),
  ('responde cliente (muito)', 3.0),
  ('ajusta cadastro que veio errado', 3.0),
  ('não é só lançar nota: é achar o erro antes de virar problema', 3.8),
], ['digita_anota', 'focada', 'busca', 'painel_pronto', 'texta_mesa', 'teclado2', 'sorri_laptop']),
  sfx=P([3.2, 6.2, 9.2, 12.0, 15.0, 18.0]))
# ---------- 27/10 (ter) ----------
SPECS['2710_0730'] = EDU('G4', 'emitidas vs destinadas', ['focada', 'busca', 'tel_explica', 'sorri_laptop'])
SPECS['2710_1215'] = dict(scenes=M([
  ('dor_cabeca', 3.0, 'POV: 3 horas esperando o portal da prefeitura voltar'),
  ('teclado', 2.4, 'clica em "entrar"…'),
  ('comemora', 3.6, 'ELE CARREGOU 🙌'),
]), sfx=[('click', 4.2, .4), ('ding', 5.4, .3)])
SPECS['2710_1930'] = dict(scenes=TX([
  ('escritório contábil precisa estar no TikTok?', 3.2),
  ('meu cliente de 25 anos me achou aqui', 3.0),
  ('o de 55 me achou por indicação', 3.0),
  ('os dois existem.', 2.6),
  ('não é sobre dancinha. é sobre ser encontrado.', 3.6),
], ['socio_camera', 'cel_le_sorri', 'madura_tel', 'socio_camera', 'sorri_laptop']), sfx=P([3.2, 6.2, 9.2, 11.8]))
# ---------- 28/10 (qua) ----------
SPECS['2810_0730'] = EDU('DP2', 'o erro de eSocial que mais aparece', ['estagiario', 'teclado', 'tel_anota', 'focada2'])
SPECS['2810_1215'] = dict(scenes=M([
  ('equipe_laptop', 3.2, 'coisas que só quem trabalha em escritório contábil entende (parte 7)'),
  ('sem_expressao', 3.0, 'o silêncio quando alguém fala "mudou o layout"'),
  ('equipe_monitor', 3.0, 'todo mundo no mesmo monitor olhando um erro estranho'),
  ('highfive', 3.4, '"ACHEI!" e a sala inteira solta o ar'),
]), sfx=P([3.2, 6.2, 9.2]))
SPECS['2810_1930'] = dict(scenes=TX([
  ('"quanto tempo leva pra começar a usar um sistema assim?"', 3.6),
  ('o que leva tempo é cadastrar os certificados dos clientes', 3.6),
  ('depois disso, o robô começa a baixar sozinho', 3.2),
  ('o resto é o time se acostumar a abrir o painel em vez do portal', 3.8),
], ['socio_camera', 'socio_tela', 'robo_sync', 'equipe_laptop'],
 extra0=[(COMMENT('contadora.rafa', 'quanto tempo leva pra começar a usar um sistema assim?', top=560), 0, None)]),
 sfx=P([0.2, 3.6, 7.2, 10.4]))
# ---------- 29/10 (qui) ----------
SPECS['2910_0730'] = EDU('R7', 'Split payment: o que é', ['tel_explica', 'focada', 'cel_maos', 'sorri_laptop'])
SPECS['2910_1215'] = dict(scenes=M([
  ('madura_olha_cel', 3.4, 'tipos de cliente: o que corrige o contador com vídeo do YouTube', None,
   [(NOTIF('Cliente · Studio Exemplo', 'vi num vídeo que não preciso pagar isso 👀', '14:22', top=900), 0.6, None)]),
  ('cafe_duas', 3.0, 'eu e a colega:'),
  ('texta_mesa', 3.2, '"vamos marcar 15 minutinhos?" 😊'),
]), sfx=[('notify', 0.6, .45), ('pop', 3.4, .2), ('typing', 6.6, .35)])
SPECS['2910_1930'] = dict(scenes=TX([
  ('fechamento do mês: de 3 dias para 1 tarde', 3.0),
  ('antes: portal por portal + planilha', 3.0),
  ('depois: as notas já estão no painel', 3.0),
  ('relatório do mês em PDF e Excel', 2.6),
  ('ZIP do mês baixado. sem drama.', 2.6),
], ['focada2', 'dor_cabeca', 'painel_pronto', 'danfe', 'zip']), sfx=[('pop', 3.0, .2), ('ding', 6.0, .3), ('click', 9.0, .25), ('ding', 11.6, .3)])
# ---------- 30/10 (sex) ----------
SPECS['3010_0730'] = dict(scenes=TX([
  ('último dia útil do mês: o que conferir hoje', 3.0),
  ('✔ notas canceladas do mês', 2.8),
  ('✔ destinadas baixadas', 2.8),
  ('✔ certificados que vencem em novembro', 3.0),
], ['quadro', 'quadro', 'anota_papel', 'focada']), sfx=P([3.0, 5.8, 8.6]))
SPECS['3010_1215'] = dict(scenes=M([
  ('fecha_laptop', 2.8, 'sexta, último dia útil do mês, 17h58'),
  ('tel_fixo', 3.6, 'o telefone toca', '"oi! pode falar 😊"'),
  ('socio_camera', 2.4, 'a gente sempre atende 🥲'),
]), sfx=[('notify', 2.8, .4), ('pop', 6.4, .2)])
SPECS['3010_1930'] = dict(scenes=TX([
  ('fechamento de mês num escritório contábil, sem drama', 3.2),
  ('9h · conferência das canceladas', 3.0),
  ('14h · relatório do mês gerado', 3.0),
  ('16h · enviado pros clientes', 3.0),
  ('fechamento é conferência, não correria', 3.4),
], ['chega', 'focada', 'painel_pronto', 'texta_mesa', 'tchau']), sfx=P([3.2, 6.2, 9.2, 12.2]))
