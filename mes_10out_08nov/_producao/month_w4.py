from month_lib import *
SPECS = {}
P = lambda n: [('pop', t, .2) for t in n]
EXPL = ("<div style='position:absolute;left:70px;right:70px;top:880px;background:#fff;border-radius:26px;padding:30px 36px;font-family:TT;color:#111;box-shadow:0 18px 50px rgba(0,0,0,.35);font-size:40px;line-height:1.6'>"
        "<div style='font-size:28px;color:#888'>PEN DRIVE (E:)</div>📁 NOTAS 2024-2026 ORGANIZADO<br>&nbsp;&nbsp;&nbsp;└ 📁 Nova pasta (3)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└ 🖼️ foto_nota_final2.jpeg</div>")
# ---------- 31/10 (sáb) ----------
SPECS['3110_15h'] = dict(scenes=M([
  ('sala_noite', 2.6, 'Halloween de contador: o que mais dá medo 🎃'),
  ('preocupada', 2.2, 'certificado vencido.'),
  ('maos_cabeca', 2.2, 'XML faltando.'),
  ('ma_noticia2', 2.6, 'cliente sumido no dia do DAS.'),
]), sfx=[('riser', 0.4, .3), ('impact', 2.6, .5), ('impact', 4.8, .5), ('impact', 7.0, .55)])
SPECS['3110_20h'] = dict(scenes=[
  sc('painel_pronto', 4.4, z=1.0, ov=[(T('outubro em números 📊', top=TOP), 0, None),
     (CARD([('XMLs baixados', '12.480'), ('canceladas conferidas', '214'), ('clientes sincronizados', '50 de 50'), ('certificados renovados a tempo', '6')], 'Outubro no painel'), 0.5, None)]),
  sc('alivio', 3.0, ov=[(T('outubro: fechado ✅', top=TOP), 0, None)]),
], sfx=[('pop', 0.5, .25), ('ding', 4.4, .3)])
# ---------- 01/11 (dom) ----------
SPECS['0111_15h'] = dict(scenes=M([
  ('chega', 3.0, 'tipos de cliente: o que já chega com tudo "organizado" num pen drive'),
  ('focada2', 3.6, 'abrindo…', None, [(EXPL, 0.5, None)]),
  ('sorri_laptop', 2.8, 'sorrindo por fora 🙂'),
]), sfx=[('click', 3.5, .35), ('pop', 6.6, .2)])
SPECS['0111_20h'] = dict(scenes=[
  sc('sofa_laptop', 3.6, ss=1, ov=[(T('novembro: 13º, Black Friday dos clientes e o ano acabando', top=TOP), 0, None)]),
  sc('sofa_laptop', 3.4, ss=12, ov=[(T('respira fundo. amanhã é feriado 🍿', top=TOP), 0, None)]),
], sfx=[('pop', 3.6, .2)])
# ---------- 02/11 (seg · feriado) ----------
SPECS['0211_10h'] = dict(scenes=M([
  ('cel_maos', 3.2, 'feriado: o celular do contador também merece descanso', None,
   [(NOTIF('Foco', '🌙 Não perturbe ativado até amanhã, 08:00', 'agora', top=900), 0.8, None)]),
  ('sofa_tv', 3.0, 'volto amanhã, clientes 💚'),
]), sfx=[('click', 0.8, .35), ('pop', 3.2, .2)])
SPECS['0211_20h'] = dict(scenes=[
  sc('robo_sync', 3.6, z=1.0, ov=[(T('feriado de novo, robô trabalhando de novo 🤖', top=1420), 0, None)]),
  sc('painel_pronto', 3.4, z=1.0, ov=[(T('sincronização das 12:00 ✓', top=1420), 0, None)]),
  sc('sofa_pipoca', 2.6, ov=[(T('ele não pediu folga. a gente pediu.', top=TOP), 0, None)]),
], sfx=[('click', 0.6, .25), ('ding', 4.0, .3), ('pop', 7.0, .2)])
# ---------- 03/11 (ter) ----------
SPECS['0311_0730'] = EDU('R8', 'a reforma tributária em 3 frases (pro cliente)', ['tel_explica', 'madura_tel', 'focada', 'sorri_laptop'])
SPECS['0311_1215'] = dict(scenes=M([
  ('focada', 3.0, 'coisas que só quem trabalha em escritório contábil entende (parte 9)'),
  ('socio_tela', 3.0, '"deixa eu só ver uma coisinha"', 'some 40 minutos'),
  ('tel_fixo', 3.0, 'cliente liga perguntando pelo "contador" e qualquer um atende'),
  ('cafe_grupo', 3.2, 'o café da tarde que vira reunião ☕'),
]), sfx=P([3.0, 6.0, 9.0]))
SPECS['0311_1930'] = dict(scenes=TX([
  ('"vocês mostram dado de cliente nos vídeos?"', 3.4),
  ('não. toda tela aqui é de demonstração', 3.2),
  ('empresas e CNPJs inventados', 2.8),
  ('dado de cliente é sigilo (e LGPD)', 3.0),
  ('cliente real, só com autorização por escrito', 3.4),
], ['socio_camera', 'painel_pronto', 'pasta_xml', 'madura_digita', 'chefe_explica'],
 extra0=[(COMMENT('dp.camila', 'vocês mostram dado de cliente nos vídeos?', top=560), 0, None)]),
 sfx=P([0.2, 3.4, 6.6, 9.4, 12.4]))
# ---------- 04/11 (qua) ----------
SPECS['0411_0730'] = EDU('DP4', 'férias coletivas: pergunta pro cliente hoje', ['estagiario', 'tel_calma', 'anota_mesa', 'focada2'])
SPECS['0411_1215'] = dict(scenes=M([
  ('cel_olha_longe', 2.6, 'cliente diz vs contador entende (edição fim de ano)'),
  ('headset', 3.2, '"vou fazer promoção na Black Friday"', 'e o limite do Simples?'),
  ('tel_gesticula', 3.2, '"quero dar um bônus de Natal"', 'precisa ver como lançar'),
  ('ma_noticia', 3.4, '"vou comprar um carro pela empresa"', 'vamos conversar.'),
]), sfx=P([2.6, 5.8, 9.0]))
SPECS['0411_1930'] = dict(scenes=TX([
  ('um dia com o estagiário de DP', 3.0),
  ('8h · confere o ponto', 2.8),
  ('10h · lança horas extras', 2.8),
  ('12h · almoço com o pessoal', 2.8),
  ('14h · tira dúvida com a contadora', 3.0),
  ('16h · envia os eventos do eSocial', 3.0),
  ('aprendendo um dia de cada vez 💚', 3.0),
], ['estagiario', 'anota_mesa', 'teclado2', 'almoco', 'chefe_explica', 'homem_laptop', 'rindo_colegas']),
 sfx=P([3.0, 5.8, 8.6, 11.4, 14.4, 17.4]))
# ---------- 05/11 (qui) ----------
SPECS['0511_0730'] = EDU('G6', 'CST do IBS/CBS em 20 segundos', ['focada', 'danfe', 'teclado', 'sorri_laptop'])
SPECS['0511_1215'] = dict(scenes=M([
  ('notif_mesa', 3.4, 'POV: o cliente manda o XML certo, no formato certo, sem você pedir', None,
   [(NOTIF('E-mail · Padaria Aurora', '📎 XMLs_outubro.zip · "segue, qualquer coisa me avisa"', '08:41', top=900), 0.6, None)]),
  ('alivio', 3.0, '*encosta na cadeira*'),
  ('comemora', 3.0, 'eu vivi pra ver isso 🥹'),
]), sfx=[('notify', 0.6, .45), ('pop', 3.4, .2), ('ding', 6.4, .3)])
SPECS['0511_1930'] = dict(scenes=TX([
  ('como fica o limite do Simples de um cliente em novembro', 3.6),
  ('faturou acima da média em outubro? a projeção já mostra', 3.8),
  ('dá tempo de conversar com o cliente antes de dezembro', 3.6),
], ['focada2', 'socio_tela', 'tel_explica']),
 ov=[(BAR('Comércio Exemplo Ltda', 'R$ 4,31 mi', 'R$ 4,8 mi', 90, 'projeção do ano passa do limite em dezembro', top=700), 0.6, 7.4)],
 sfx=[('notify', 0.6, .4), ('pop', 3.6, .2), ('pop', 7.4, .2)])
# ---------- 06/11 (sex) ----------
SPECS['0611_0730'] = EDU('R9', '1 mês de NFS-e com IBS/CBS: o que a gente viu', ['madura_tel', 'danfe', 'focada', 'busca', 'sorri_laptop'])
SPECS['0611_1215'] = dict(scenes=M([
  ('chega', 3.0, 'tipos de cliente: o que manda presente no fim do ano'),
  ('cafe_grupo', 3.2, 'cartão: "obrigado pelo ano, equipe! 💚"'),
  ('highfive', 3.4, 'esse pode mandar áudio de 5 minutos 🥹'),
]), sfx=P([3.0, 6.2]))
SPECS['0611_1930'] = dict(scenes=M([
  ('tchau', 3.0, 'sexta no escritório: a última hora'),
  ('satisfeito', 3.0, 'semana fechada.'),
  ('sala_noite', 3.0, 'até segunda 💚'),
]), sfx=P([3.0, 6.0]))
# ---------- 07/11 (sáb) ----------
SPECS['0711_15h'] = dict(scenes=TX([
  ('3 hábitos que deixam um escritório pequeno parecer grande', 3.4),
  ('1 · responder no mesmo dia (nem que seja pra dizer quando)', 3.8),
  ('2 · mandar o relatório do mês sem o cliente pedir', 3.6),
  ('3 · avisar antes: limite, certificado, prazo', 3.6),
  ('atendimento é o que o cliente vê 💚', 3.0),
], ['socio_camera', 'headset', 'texta_mesa', 'tel_explica', 'sorri_laptop']), sfx=P([3.4, 7.2, 10.8, 14.4]))
SPECS['0711_20h'] = dict(scenes=M([
  ('tel_gesticula', 3.2, 'eu explicando pra minha mãe o que eu faço no trabalho'),
  ('tel_explica', 3.4, '"então, mãe: confiro nota, XML, Simples, reforma…"'),
  ('madura_tel', 3.4, 'mãe:', '"ah, então você é do imposto de renda?"'),
]), sfx=P([3.2, 6.6]))
# ---------- 08/11 (dom) ----------
SPECS['0811_10h'] = EDU('DP5', '13º de quem entrou no meio do ano', ['estagiario', 'anota_mesa', 'teclado2', 'focada2'])
SPECS['0811_15h'] = dict(scenes=[
  sc('cel_le_sorri', 2.8, z=1.05, ov=[(T('qual tipo de cliente é o seu favorito? comenta o número 👇', top=TOP), 0, None)]),
  sc('cel_sorri', 2.2, z=1.05, ov=[(T('1 · o do "oi" que some', top=TOP), 0, None)]),
  sc('focada2', 2.2, z=1.05, ov=[(T('2 · o do dia 19 às 17h', top=TOP), 0, None)]),
  sc('sorri_laptop', 2.2, z=1.05, ov=[(T('3 · o do pen drive "organizado"', top=TOP), 0, None)]),
  sc('highfive', 2.6, z=1.05, ov=[(T('4 · o do presente 💚', top=TOP), 0, None)]),
], sfx=P([2.8, 5.0, 7.2, 9.4]))
SPECS['0811_20h'] = dict(scenes=TX([
  ('1 mês postando a rotina de um escritório contábil: o que eu aprendi', 3.6),
  ('contador se identifica com verdade, não com perfeição', 3.4),
  ('os vídeos mais simples foram os que mais deram certo', 3.4),
  ('e vocês salvam tudo que é checklist 📌', 3.0),
  ('valeu por estarem aqui 💚 o que vocês querem ver em dezembro?', 3.6),
], ['cel_le_sorri', 'madura_escreve', 'rindo_tablet', 'cel_sorri', 'cafe_grupo']), sfx=P([3.6, 7.0, 10.4, 13.4]))
