from month_lib import *
SPECS = {}
P = lambda n: [('pop', t, .2) for t in n]
# ---------- 17/10 (sáb) ----------
SPECS['1710_10h'] = dict(scenes=M([
  ('teclado', 3.2, 'coisas que só quem trabalha em escritório contábil entende (parte 4)'),
  ('teclado2', 3.0, 'errar a senha do e-CAC 2x e parar antes da 3ª 🫣'),
  ('tedio', 3.2, 'esperando a impressora que só trava quando é procuração'),
  ('equipe_monitor', 3.4, 'duas pessoas perguntando ao mesmo tempo:', '"qual é o CNPJ mesmo?"'),
]), sfx=P([3.2, 6.2, 9.4]))
SPECS['1710_15h'] = dict(scenes=[
  sc('sofa_laptop', 3.4, ss=1, ov=[(T('sim, às vezes contador trabalha no sábado (mas só às vezes)', top=TOP), 0, None)]),
  sc('sofa_laptop', 3.0, ss=5, ov=[(T('9h · 2 alertas no painel', top=TOP), 0, None)]),
  sc('sofa_laptop', 3.2, ss=9.5, ov=[(T('resolvido em 10 minutos ✅', top=TOP), 0, None)]),
  sc('sofa_laptop', 3.4, ss=13.5, ov=[(T('sábado de 10 minutos > sábado inteiro', top=TOP), 0, None)]),
], sfx=[('notify', 3.6, .4), ('pop', 6.4, .2), ('ding', 9.6, .3)])
SPECS['1710_20h'] = dict(scenes=[
  sc('cel_olha_longe', 2.4, z=1.05, ov=[(T('me explica em 1 palavra o seu mês de outubro', top=TOP), 0, None)]),
  sc('focada', 1.7, z=1.1, ov=[(T('reforma.', top=820, style='stroke', size=130), 0, None)]),
  sc('dor_cabeca', 1.7, z=1.1, ov=[(T('NFS-e.', top=820, style='stroke', size=130), 0, None)]),
  sc('pausa_cafe', 2.2, z=1.1, ov=[(T('café. ☕', top=820, style='stroke', size=130), 0, None)]),
], sfx=[('impact', 2.4, .35), ('impact', 4.1, .35), ('impact', 5.8, .35)])
# ---------- 18/10 (dom) ----------
SPECS['1810_10h'] = dict(scenes=TX([
  ('como eu organizo os prazos de 50 clientes sem planilha gigante', 3.6),
  ('1 · agenda com alerta 3 dias antes de cada vencimento', 3.6),
  ('2 · etiquetas no WhatsApp Business: aguardando doc · conferindo · ok', 4.0),
  ('3 · alerta de certificado vencendo, antes de vencer', 3.6),
  ('o resto é rotina, não memória 💚', 3.0),
], ['cel_maos', 'cel_le_sorri', 'texta_mesa', 'focada', 'sorri_laptop'],
), ov=[(NOTIF('Painel Fiscal', 'Certificado A1 · Clínica Exemplo vence em 15 dias', '09:00', top=1180), 11.2, 14.8)],
  sfx=[('pop', 3.6, .2), ('pop', 7.2, .2), ('notify', 11.2, .4), ('pop', 14.8, .2)])
SPECS['1810_15h'] = dict(scenes=M([
  ('cansada_noite', 3.6, 'tipos de cliente: o que pergunta "quanto eu pago de imposto" por áudio às 22h', None,
   [(NOTIF('Cliente · Studio Exemplo', '🎤 Mensagem de voz (2:04)', '22:14', top=900), 1.0, None)]),
  ('sofa_tv', 3.2, 'amanhã às 8h eu respondo, juro 🙏'),
]), sfx=[('notify', 1.0, .45), ('pop', 3.6, .2)])
SPECS['1810_20h'] = dict(scenes=[
  sc('anota_noite', 3.2, ss=10.5, ov=[(T('domingo à noite, lista da semana', top=TOP), 0, None)]),
  sc('anota_noite', 3.8, ss=14, ov=[(T('risca "conferir DAS"…', top=TOP), 0, None), (T('e escreve: "segunda: conferir DAS DE NOVO"', top=1250, style='stroke', size=88), 0.6, None)]),
], sfx=[('pop', 3.2, .2)])
# ---------- 19/10 (seg) ----------
SPECS['1910_0730'] = dict(scenes=TX([
  ('amanhã é dia 20: checklist de 3 itens ✅', 3.0),
  ('1 · DAS gerado e enviado pra todos do Simples', 3.4),
  ('2 · guia do FGTS Digital conferida', 3.2),
  ('3 · cliente avisado por mensagem, não só por e-mail', 3.4),
  ('salva pra amanhã 📌', 2.6),
], ['focada', 'teclado2', 'digita_anota', 'texta_mesa', 'sorri_laptop']), sfx=P([3.0, 6.4, 9.6, 13.0]))
SPECS['1910_1215'] = dict(scenes=M([
  ('madura_olha_cel', 3.2, 'POV: dia 19 e o cliente pergunta', None,
   [(NOTIF('Cliente · Ferragem Exemplo', 'o que é DAS? 🤔', '11:47', top=640), 0.5, None)]),
  ('teclado', 3.0, 'eu começando uma explicação de 4 parágrafos'),
  ('sem_expressao', 2.4, 'apaga tudo.'),
  ('tel_calma', 3.2, '"te liguei, atende 😊"'),
]), sfx=[('notify', 0.5, .45), ('typing', 3.3, .35), ('pop', 6.2, .2), ('pop', 8.6, .2)])
SPECS['1910_1930'] = dict(scenes=TX([
  ('o alerta que salvou o mês do cliente', 3.6),
  ('ligação na hora, antes de virar problema', 3.4),
  ('alerta em outubro > susto em janeiro', 3.4),
], ['focada2', 'tel_explica', 'sorri_laptop'], extra0=[(NOTIF('Painel Fiscal', 'Ferragem Exemplo · atenção: projeção passa do sublimite em novembro', '16:20', top=700), 0.6, None)]),
  sfx=[('notify', 0.6, .45), ('pop', 3.6, .2), ('ding', 7.0, .3)])
# ---------- 20/10 (ter) · dia 20 ----------
SPECS['2010_0730'] = dict(scenes=M([
  ('headset', 3.6, 'hoje é dia 20, então hoje a gente só fala com cliente se for sobre DAS'),
  ('tel_ocupada', 3.2, 'qualquer outro assunto:', '"só um minutinho" ☝️'),
]), sfx=P([3.6]))
SPECS['2010_1215'] = dict(scenes=M([
  ('cel_olha_longe', 2.6, 'cliente diz vs contador entende (edição dia 20)'),
  ('tel_calma', 3.2, '"paguei ontem"', 'agendou pra hoje às 23h'),
  ('madura_tel', 3.2, '"meu sobrinho faz as notas"', 'CFOP aleatório'),
  ('tel_serio', 3.2, '"pode deixar que eu vejo"', 'você vai ver'),
]), sfx=P([2.6, 5.8, 9.0]))
SPECS['2010_1930'] = dict(scenes=M([
  ('highfive', 4.2, '18h do dia 20: todos os DAS pagos ✅'),
  ('fecha_laptop', 3.4, 'desliga, fecha e vai embora 💚'),
]), sfx=[('ding', 1.2, .3), ('click', 5.0, .3)])
# ---------- 21/10 (qua) ----------
SPECS['2110_0730'] = EDU('R4', 'NFS-e padrão nacional: o que muda pro escritório', ['focada', 'pasta_xml', 'teclado2', 'sorri_laptop'])
SPECS['2110_1930'] = dict(scenes=TX([
  ('como funciona a reunião de segunda num escritório contábil', 3.4),
  ('9h · prazos da semana na tela', 3.2),
  ('cada um fala 1 travamento (só 1)', 3.4),
  ('alguém anota no quadro (sempre a mesma pessoa)', 3.4),
  ('15 minutos. todo mundo sabe o que fazer.', 3.4),
], ['equipe_laptop', 'chefe_explica', 'equipe_monitor', 'quadro', 'cafe_grupo']), sfx=P([3.4, 6.6, 10.0, 13.4]))
# ---------- 22/10 (qui) ----------
SPECS['2210_0730'] = EDU('G3', 'CFOP em 20 segundos', ['postits', 'focada', 'teclado', 'preocupada'])
SPECS['2210_1215'] = dict(scenes=[
  sc('busca', 4.0, z=1.0, ov=[(T('POV: você acha a nota que o cliente jurava que não existia', top=1420), 0, None)]),
  sc('danfe', 2.2, z=1.0, ov=[(T('emitida dia 03. por ele mesmo. 🧾', top=1420), 0, None)]),
  sc('comemora', 3.4, z=1.05, ov=[(T('eu mandando o print', top=TOP), 0, None)]),
], sfx=[('typing', 0.6, .35), ('ding', 4.0, .3), ('pop', 6.2, .25)])
SPECS['2210_1930'] = dict(scenes=TX([
  ('"e quando a SEFAZ cai, o robô faz o quê?"', 3.4),
  ('tenta de novo na próxima janela: meio-dia ou meia-noite', 3.6),
  ('e mostra a última sincronização de cada cliente', 3.4),
  ('ninguém precisa ficar dando F5 🙃', 3.2),
], ['robo_sync', 'pasta_xml', 'painel_pronto', 'alivio'],
 extra0=[(COMMENT('escritorio.mendes', 'e quando a SEFAZ cai, o robô faz o quê?', top=560), 0, None)]),
 sfx=P([0.2, 3.4, 7.0, 10.4]))
# ---------- 23/10 (sex) ----------
SPECS['2310_0730'] = EDU('R5', '3 perguntas que o cliente vai fazer sobre IBS/CBS', ['madura_tel', 'tel_calma', 'focada', 'tel_explica', 'sorri_laptop'])
SPECS['2310_1215'] = dict(scenes=M([
  ('cel_maos', 3.4, 'tipos de cliente: o que some o ano todo e aparece em dezembro', None,
   [(NOTIF('Cliente · Loja Exemplo', 'oi, sumida! preciso de tudo do ano 🥲', '02/12', top=900), 0.8, None)]),
  ('sem_expressao', 3.0, 'eu, que mandei 11 lembretes no ano'),
  ('rindo_colegas', 3.0, 'rir pra não chorar'),
]), sfx=[('notify', 0.8, .45), ('pop', 3.4, .2), ('pop', 6.4, .2)])
SPECS['2310_1930'] = dict(scenes=M([
  ('chefe_explica', 3.2, 'sexta 17h59: "pessoal, só uma coisinha…"'),
  ('colegas_viram', 3.0, 'todo mundo já de bolsa no ombro'),
  ('socio_camera', 3.0, '"…segunda eu falo." 😅'),
]), sfx=P([3.2, 6.2]))
