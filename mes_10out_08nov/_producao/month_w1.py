from month_lib import *
SPECS = {}
# ---------- 10/10 ----------
SPECS['1010_10h'] = dict(scenes=M([
  ('cel_cafe', 3.0, 'coisas que só quem trabalha em escritório contábil entende (parte 2)', None, [(NOTIF('Cliente · Padaria Aurora','🎤 Mensagem de voz (3:47)','agora',top=640),0.7,None)]),
  ('sem_expressao', 3.2, 'o áudio de 3 minutos pra perguntar se o DAS já foi pago'),
  ('tel_ocupada', 3.0, 'atender ligação com 3 conversas piscando no WhatsApp'),
  ('cafe_duas', 3.4, 'a colega: "é aquele cliente?"', 'é.'),
]), sfx=[('notify',0.7,.5),('pop',3.0,.2),('pop',6.2,.2),('pop',9.2,.2)])
SPECS['1010_15h'] = EDU('R1', 'cClassTrib: o que é (sem enrolação)', ['focada','teclado','danfe','sorri_laptop'],
  "Você já viu esse tal de cClassTrib na nota? É o código de classificação tributária do item. Ele diz pro fisco como aquele produto ou serviço é tratado no IBS e na CBS. Em 2026 ainda é teste. Em janeiro, o Simples Nacional entra. Então quem já classifica os itens hoje não vai correr em dezembro.")
SPECS['1010_20h'] = dict(scenes=M([
  ('sofa_tv', 3.5, 'sábado 20h, de boa no sofá'),
  ('sofa_laptop', 4.0, 'e o cérebro: "será que eu conferi as notas de entrada da Padaria?"'),
]), sfx=[('pop',3.5,.25)])
# ---------- 11/10 ----------
SPECS['1110_15h'] = dict(scenes=M([
  ('cel_le_sorri', 3.0, 'tipos de cliente: o que manda "oi" e some', None, [(NOTIF('Cliente · Ferragem Exemplo','Oi','09:12',top=640),0.4,None)]),
  ('focada', 3.0, 'eu respondendo em 2 minutos: "Oi! Tudo bem? Como posso ajudar?"'),
  ('tedio', 3.2, '2 horas depois...'),
  ('sem_expressao', 3.2, '18h: "tá aí?"', None, [(NOTIF('Cliente · Ferragem Exemplo','tá aí?','18:01',top=640),0.3,None)]),
]), sfx=[('notify',0.4,.45),('click',3.6,.3),('notify',9.5,.45)])
SPECS['1110_20h'] = dict(scenes=M([
  ('sofa_laptop', 3.5, 'domingo 20h: abrindo a agenda da semana'),
  ('preocupada', 3.5, 'quando lembra que a semana tem dia 20'),
]), sfx=[('pop',3.5,.25)])
# ---------- 12/10 (feriado) ----------
SPECS['1210_10h'] = dict(scenes=M([
  ('sofa_tv', 3.2, 'feriado 🎉 escritório fechado, celular no silencioso'),
  ('madura_olha_cel', 3.4, 'cliente: "amanhã você consegue ver aquilo cedinho?"', None, [(NOTIF('Cliente · Clínica Exemplo','amanhã vc consegue ver aquilo cedinho? 🙏','10:02',top=640),0.2,None)]),
  ('sofa_pipoca', 3.0, 'amanhã eu vejo. hoje é feriado.'),
]), sfx=[('notify',3.4,.45),('pop',6.6,.2)])
SPECS['1210_20h'] = dict(scenes=[
  sc('robo_sync', 3.4, z=1.0, ov=[(T('o que o robô fez enquanto você estava no feriado 🤖', top=1420),0,None)]),
  sc('pasta_xml', 2.8, z=1.0, ov=[(T('a SEFAZ não tira feriado, então ele também não', top=1420),0,None)]),
  sc('painel_pronto', 3.0, z=1.0, ov=[(T('terça cedo: tudo baixado e na pasta certa', top=1420),0,None)]),
], sfx=[('click',0.5,.25),('ding',6.4,.3)])
# ---------- 13/10 ----------
SPECS['1310_0730'] = EDU('R2', 'o cliente vai pagar mais imposto em 2026?', ['madura_tel','danfe','tel_calma','focada2'],
  "IBS e CBS na nota: o cliente vai pagar mais imposto em 2026? Não. Esse ano é teste. A CBS aparece com 0,9% e o IBS com 0,1%, e esses valores podem ser compensados com PIS e Cofins. O que muda é o XML e o PDF da nota. O cliente vai ver um número novo e vai te ligar. Já deixa essa resposta pronta.")
SPECS['1310_1215'] = dict(scenes=M([
  ('cel_olha_longe', 2.6, 'o que o cliente diz vs o que o contador entende'),
  ('tel_calma', 3.0, '"é rapidinho"', 'vai levar a tarde'),
  ('tel_serio', 3.0, '"te mando amanhã"', 'te mando dia 19'),
  ('madura_tel', 3.2, '"não mudou nada na empresa"', 'abriu filial'),
]), sfx=[('pop',2.6,.2),('pop',5.6,.2),('pop',8.6,.2)])
SPECS['1310_1930'] = dict(scenes=TX([
  ('um dia normal num escritório contábil (sem filtro)', 3.0),
  ('08h · liga os 2 monitores, abre o sistema e o WhatsApp', 3.2),
  ('09h · confere as notas que chegaram no painel', 3.0),
  ('10h30 · café rápido com a equipe', 3.0),
  ('15h · ligação de cliente sobre o boleto do DAS', 3.2),
  ('17h · fila de tarefas conferida', 3.0),
  ('18h · desliga tudo e vai pra casa', 3.2),
], ['chega','focada','painel_pronto','cafe_grupo','tel_calma','alivio','tchau']),
 sfx=[('pop',3.0,.2),('pop',6.2,.2),('pop',9.2,.2),('pop',12.2,.2),('pop',15.4,.2),('pop',18.4,.2)])
# ---------- 14/10 ----------
SPECS['1410_0730'] = dict(scenes=TX([
  ('prazo da semana 📌', 2.6),
  ('dia 20 (terça): DAS do Simples', 3.2),
  ('dia 20 também: FGTS Digital', 3.2),
  ('não deixa pra segunda à noite 🙏 (confere sempre a agenda oficial)', 3.6),
], ['anota_mesa','focada','teclado','tel_anota']), sfx=[('pop',2.6,.2),('pop',5.8,.2),('pop',9.0,.2)])
SPECS['1410_1215'] = dict(scenes=M([
  ('focada2', 3.0, 'POV: o certificado digital do cliente vence hoje', None, [(NOTIF('Painel Fiscal','Certificado A1 · Ferragem Exemplo vence hoje','08:30',top=640),0.4,None)]),
  ('tel_ocupada', 3.0, 'e ele tá viajando'),
  ('maos_cabeca', 3.2, 'caixa postal.'),
]), sfx=[('notify',0.4,.45),('pop',3.0,.2),('pop',6.0,.2)])
SPECS['1410_1930'] = dict(scenes=TX([
  ('vale a pena automatizar um escritório pequeno?', 3.4),
  ('pensa num escritório de 4 pessoas com 50 clientes', 3.2),
  ('o que mais come tempo: baixar e organizar nota, portal por portal', 3.6),
  ('automatizar isso não é coisa de escritório grande', 3.2),
  ('é o que deixa o pequeno crescer sem contratar alguém só pra baixar XML', 4.0),
], ['socio_camera','equipe_monitor','teclado','socios_conversa','socio_camera'],
 extra0=[(COMMENT('contab.lima','vale a pena automatizar escritório pequeno?'),0,None)]),
 sfx=[('pop',0.2,.25),('pop',3.4,.2),('pop',6.6,.2),('pop',10.2,.2),('pop',13.4,.2)])
# ---------- 15/10 ----------
SPECS['1510_0730'] = EDU('G2', 'nota cancelada x substituída', ['focada','pasta_xml','preocupada','focada2'],
  "Nota cancelada e nota substituída, a diferença em 20 segundos. Cancelada: a nota deixa de valer e sai da soma. Substituída: no caso da NFS-e, uma nova nota substitui a anterior, e a antiga também sai do faturamento. Se você soma as duas, o faturamento do cliente dobra no papel. E esse erro aparece depois, no limite do Simples.")
SPECS['1510_1930'] = dict(scenes=[
  sc('robo_sync', 3.4, z=1.0, ov=[(T('ASMR de nota fiscal se organizando sozinha 🎧', top=1420),0,None)]),
  sc('pasta_xml', 2.8, z=1.0, ov=[(T('cliente > mês > modelo', top=1420),0,None)]),
  sc('busca', 4.2, z=1.0, ov=[(T('e quando precisa: digita e pronto', top=1480),0,None)]),
], sfx=[('click',0.6,.3),('click',1.4,.3),('click',2.2,.3),('pop',3.6,.25),('ding',5.8,.3),('typing',6.6,.4),('ding',9.6,.3)])
# ---------- 16/10 ----------
SPECS['1610_0730'] = EDU('R3', 'Simples Nacional em 2027: o que muda na nota', ['tel_explica','focada','anota_mesa','sorri_laptop'],
  "Seu cliente é do Simples? Então presta atenção: em janeiro de 2027, empresa do Simples Nacional passa a preencher IBS e CBS na nota, ainda em fase de teste. Quem precisa se mexer agora é quem emite por sistema próprio ou por um emissor antigo. Pergunta pro fornecedor do emissor se a versão com o grupo IBS CBS já está pronta. De preferência, por escrito.")
SPECS['1610_1215'] = dict(scenes=M([
  ('focada2', 3.2, 'tipos de cliente: o que manda tudo no dia 19 às 17h', None, [(NOTIF('Cliente · Café Exemplo','segue as notas do mês 😊 📎 notas_setembro.zip','17:02',top=640),0.4,None)]),
  ('sem_expressao', 3.0, 'eu, que ia conferir com calma'),
  ('cafe_duas', 3.2, 'a colega: "de novo?"'),
]), sfx=[('notify',0.4,.45),('pop',3.2,.2),('pop',6.2,.2)])
SPECS['1610_1930'] = dict(scenes=TX([
  ('contador deveria cobrar à parte pelo trabalho da reforma?', 3.4),
  ('classificar item, conferir XML novo, orientar cliente: é trabalho extra', 3.8),
  ('minha opinião: melhor combinar um valor claro do que absorver calado', 3.8),
  ('concorda? 👇', 2.6),
], ['socio_camera','chefe_explica','socios_conversa','socio_camera']), sfx=[('pop',3.4,.2),('pop',7.2,.2),('pop',11.0,.2)])
