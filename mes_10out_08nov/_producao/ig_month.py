import sys
from ig_lib import *
TG_RF = '#reformatributaria #ibscbs #contabilidade #contador #escritoriocontabil'
TG_FI = '#notafiscal #fiscal #contabilidade #contador #escritoriocontabil'
TG_DP = '#departamentopessoal #13salario #contabilidade #contador #escritoriocontabil'
TG_SN = '#simplesnacional #contabilidade #contador #escritoriocontabil #mei'
TG_GE = '#contabilidade #contador #escritoriocontabil #gestaocontabil #automacaocontabil'
MUS_C = 'Carrossel: música opcional. Se quiser, instrumental calmo da biblioteca do Instagram (procure "lo-fi" ou "calm piano") a volume baixo.'
MUS_E = 'Estático: sem música (ou a mesma trilha calma dos carrosséis, se postar com áudio).'
P = {}
# ============ 10/10 sáb · Carrossel cClassTrib ============
P['10-10_carrossel_cclasstrib'] = lambda f: carousel(f, [
  (cover('focada', 'Reforma tributária', 'cClassTrib: o código que vai aparecer em <span class="g">toda nota.</span>', 'O que é, onde fica e por que vale começar agora.'), False),
  text('O que é', 'Código de <span class="g">classificação tributária</span> do item.', 'Diz ao fisco como aquele produto ou serviço é tratado no <b>IBS</b> e na <b>CBS</b>. Trabalha junto com o <b>CST</b>.'),
  text('Onde fica', 'Dentro de cada item, no grupo <span class="g">IBSCBS.</span>', '', xml("&lt;det nItem=\"1\"&gt;\n  <span class='g'>&lt;IBSCBS&gt;</span>\n    &lt;CST&gt;000&lt;/CST&gt;\n    &lt;cClassTrib&gt;000001&lt;/cClassTrib&gt;\n    <span style='color:#6E6E76'>…base, alíquota, valor</span>\n  <span class='g'>&lt;/IBSCBS&gt;</span>")),
  text('Calendário', 'Hoje é teste. <span class="g">Janeiro é do Simples.</span>', '', rows([('Regime normal · NF-e/NFC-e', 'EM TESTE EM 2026'), ('NFS-e', 'DESDE 01/10/2026'), ('Simples Nacional', '01/01/2027')], hl=2)),
  text('Por onde começar', 'Classifique primeiro <span class="g">os itens que mais aparecem.</span>', '', checks([('Puxe os 20 itens mais vendidos', 'de cada cliente, pelas notas do último trimestre'), ('Defina CST e cClassTrib', 'e registre num lugar que o time inteiro acesse'), ('Confira no XML', 'uma nota de teste por cliente antes de dezembro')])),
  (cta('Salve e mande para quem cuida do <span class="g">fiscal</span> no seu escritório.'), True),
], LEG('Carrossel · cClassTrib', '10/10/2026 (sáb) às 10h', 'Carrossel 6 lâminas · 1080x1350',
  'cClassTrib vai aparecer em toda nota: é o código de classificação tributária do item no IBS e na CBS. 🧾\n\nEm 2026 é teste. Em 01/01/2027 o Simples Nacional entra. Quem classifica os itens agora não corre em dezembro.\n\nSalve para consultar e mande para quem cuida do fiscal. 📌',
  TG_RF, 'Carrossel escuro com destaques em verde explicando o que é o cClassTrib, onde ele fica no XML e um checklist para começar.', MUS_C))
# ============ 11/10 dom · Estático frase ============
P['11-10_estatico_atendimento'] = lambda f: static(f,
  "<div style='position:absolute;left:86px;right:86px;top:300px'><div class='kicker'>Domingo</div>"
  "<div class='h' style='font-size:108px;margin-top:40px'>O cliente não vê o seu trabalho.<br><span class='g'>Ele vê o seu atendimento.</span></div>"
  "<div class='p' style='margin-top:50px;font-size:40px'>Conferir nota é invisível. Responder no mesmo dia, avisar antes do prazo e mandar o relatório sem ele pedir: isso ele vê.</div></div>",
  LEG('Estático · frase da semana', '11/10/2026 (dom) às 18h', 'Post único 1080x1350',
  'O trabalho mais importante do escritório é invisível pro cliente. O que ele enxerga é o atendimento. 💚\n\nConcorda? Conta nos comentários o que o seu cliente mais valoriza.',
  TG_GE, 'Post escuro com a frase: o cliente não vê o seu trabalho, ele vê o seu atendimento.', MUS_E))
# ============ 12/10 seg · Estático feriado ============
P['12-10_estatico_feriado_robo'] = lambda f: static(f,
  ph('sofa_pipoca', 0.6, 0.62, 'saturate(.9) brightness(.8)') + shade(.5, .97, 20) +
  "<div style='position:absolute;left:86px;right:86px;bottom:160px'><div class='kicker'>12 de outubro · feriado</div>"
  "<div class='h' style='font-size:104px;margin-top:30px'>Hoje o escritório descansa.<br><span class='g'>O robô, não.</span></div>"
  "<div class='p' style='margin-top:28px;color:#C9CAD0'>Ao meio-dia e à meia-noite ele baixa os XMLs de cada cliente. Amanhã cedo, tudo está na pasta certa.</div></div>",
  LEG('Estático · feriado', '12/10/2026 (seg, feriado) às 10h', 'Post único 1080x1350',
  'Feriado é pra descansar. 🛋️ Enquanto isso, o Painel Fiscal segue baixando as notas dos clientes ao meio-dia e à meia-noite.\n\nBom feriado! Amanhã a gente volta.',
  TG_GE, 'Pessoa relaxando no sofá com pipoca, à noite, com o texto: hoje o escritório descansa, o robô não.', MUS_E), grid=False)
# ============ 14/10 qua · Carrossel dia 20 ============
P['14-10_carrossel_semana_do_dia_20'] = lambda f: carousel(f, [
  (cover('anota_mesa', 'Prazos da semana', 'Terça é <span class="g">dia 20.</span> Comece hoje.', 'O que vence e o que dá para adiantar até segunda.'), False),
  big('Terça · 20/10', '20', 'DE OUTUBRO', 'DAS do Simples Nacional e FGTS Digital vencem no mesmo dia.'),
  text('Quarta e quinta', 'Gere e envie <span class="g">os DAS primeiro.</span>', '', checks([('DAS gerado para todos do Simples', 'e enviado por mensagem, não só por e-mail'), ('Guia do FGTS Digital conferida', 'com a folha fechada'), ('Lista de quem ainda não pagou', 'para cobrar na segunda')])),
  text('Segunda', 'Dia de <span class="g">confirmar, não de gerar.</span>', 'Segunda é para ligar para quem não confirmou o pagamento. Gerar guia na véspera é pedir para dar errado.'),
  (cta('Confira sempre a <span class="g">agenda oficial</span> e salve este checklist.', 'SALVE PARA A PRÓXIMA SEMANA'), True),
], LEG('Carrossel · semana do dia 20', '14/10/2026 (qua) às 8h', 'Carrossel 5 lâminas · 1080x1350',
  'Terça (20/10) vence o DAS do Simples e o FGTS Digital. 📌\n\nO checklist para chegar na segunda só conferindo, sem correria.\n\nConfira sempre a agenda tributária oficial. Salve e marque quem gera as guias aí.',
  TG_SN, 'Carrossel com o número 20 em destaque e um checklist para a semana de vencimento do DAS e do FGTS Digital.', MUS_C))
# ============ 15/10 qui · Carrossel cancelada x substituída ============
P['15-10_carrossel_cancelada_vs_substituida'] = lambda f: carousel(f, [
  (cover('focada2', 'Glossário', 'Nota cancelada × <span class="g">nota substituída.</span>', 'A diferença que evita dobrar o faturamento do cliente.'), False),
  text('Lado a lado', 'As duas <span class="g">saem da soma.</span>', '', vs('CANCELADA', 'A nota deixa de valer. Não entra no faturamento.', 'SUBSTITUÍDA', 'Uma nova NFS-e substitui a anterior. A antiga também sai do faturamento.')),
  text('O erro', 'Somar a original <span class="g">e a substituta.</span>', 'No papel, o faturamento do cliente dobra. E o erro só aparece depois, no <b>limite do Simples</b>.'),
  text('Como evitar', 'Confira o status <span class="g">antes de fechar o mês.</span>', '', rows([('NFS-e 1.204', 'SUBSTITUÍDA'), ('NFS-e 1.205', 'VÁLIDA'), ('NFS-e 1.198', 'CANCELADA'), ('Total válido', 'R$ 18.400,00')], hl=3)),
  (cta('Salve e mostre para o <span class="g">estagiário.</span>'), True),
], LEG('Carrossel · cancelada x substituída', '15/10/2026 (qui) às 12h', 'Carrossel 5 lâminas · 1080x1350',
  'Cancelada e substituída: as duas saem da soma. Somar a original e a substituta dobra o faturamento do cliente no papel. 🧾\n\nSalve para o fechamento e mostre para quem está começando no fiscal.\n\n(valores e números de nota ilustrativos)',
  TG_FI, 'Carrossel comparando nota cancelada e nota substituída, com tabela de exemplo.', MUS_C))
# ============ 17/10 sáb · Carrossel fontes oficiais (indicação) ============
P['17-10_carrossel_fontes_oficiais'] = lambda f: carousel(f, [
  (cover('cel_le_sorri', 'Indicação', 'Onde conferir mudança <span class="g">antes de virar boato.</span>', '4 fontes oficiais que todo escritório deveria acompanhar.'), False),
  text('01', 'Portal Nacional <span class="g">da NF-e</span>', 'Notas Técnicas, cronogramas e leiautes. Quando o XML muda, é aqui que aparece primeiro.'),
  text('02', 'Portal da <span class="g">NFS-e Nacional</span>', 'Emissor, consulta e documentação do padrão nacional da nota de serviço.'),
  text('03', 'Agenda tributária <span class="g">da Receita Federal</span>', 'Vencimentos do mês. Vale colocar no calendário do escritório com alerta.'),
  text('04', 'Portal do <span class="g">Simples Nacional</span>', 'PGDAS-D, limites, comunicados. Para quem tem carteira grande de Simples, é parada diária.'),
  (cta('Qual fonte você acompanha e <span class="g">não está aqui?</span>', 'SALVE A LISTA'), True),
], LEG('Carrossel · fontes oficiais (indicação)', '17/10/2026 (sáb) às 10h', 'Carrossel 6 lâminas · 1080x1350',
  'Print de grupo não é fonte. 😅 4 lugares oficiais para conferir mudança antes de repassar pro cliente.\n\nQual você acompanha e não está na lista? Comenta aqui.',
  TG_GE, 'Carrossel listando quatro fontes oficiais: Portal Nacional da NF-e, NFS-e Nacional, agenda tributária da Receita e Portal do Simples Nacional.', MUS_C))
# ============ 18/10 dom · Estático humor ============
P['18-10_estatico_domingo_antes_do_dia_20'] = lambda f: static(f,
  "<div style='position:absolute;left:86px;right:86px;top:260px'><div class='kicker'>Domingo, 20h</div>"
  "<div class='h' style='font-size:112px;margin-top:40px'>Amanhã é segunda.<br>Terça é dia 20.<br><span class='g'>Respira.</span></div>"
  "<div class='p' style='margin-top:56px;font-size:40px'>Se os DAS já foram gerados e enviados, segunda é só conferência. E se não foram… pelo menos agora você lembrou. 💚</div></div>",
  LEG('Estático · domingo antes do dia 20', '18/10/2026 (dom) às 18h', 'Post único 1080x1350',
  'Domingo à noite de quem trabalha em escritório contábil. 😮‍💨\n\nMarca aquele colega que já está pensando na terça.',
  TG_SN, 'Post escuro com o texto: amanhã é segunda, terça é dia 20, respira.', MUS_E))
# ============ 20/10 ter · Estático lembrete dia 20 ============
P['20-10_estatico_hoje_e_dia_20'] = lambda f: static(f,
  big('Hoje · terça, 20 de outubro', '20', 'VENCE HOJE', '') +
  "<div style='position:absolute;left:86px;right:86px;top:640px'>" + checks([('DAS do Simples Nacional', 'competência setembro'), ('FGTS Digital', 'competência setembro'), ('Cliente avisado?', 'mensagem curta agora evita ligação às 17h')]) + "</div>",
  LEG('Estático · hoje é dia 20', '20/10/2026 (ter) às 7h30', 'Post único 1080x1350',
  'Hoje vence o DAS do Simples e o FGTS Digital. ✅\n\nUma mensagem curta para os clientes agora vale mais que dez ligações às 17h. Bom dia 20 pra todo mundo!\n\n(confira sempre a agenda oficial)',
  TG_SN, 'Post com o número 20 em verde e checklist do dia: DAS, FGTS Digital e aviso ao cliente.', MUS_E))
# ============ 21/10 qua · Carrossel NFS-e nacional ============
P['21-10_carrossel_nfse_padrao_nacional'] = lambda f: carousel(f, [
  (cover('teclado2', 'NFS-e', 'NFS-e padrão nacional: <span class="g">o que muda pro escritório.</span>'), False),
  text('A ideia', 'Um layout <span class="g">em vez de centenas.</span>', 'Cada prefeitura tinha o seu jeito. O padrão nacional junta tudo num formato só.'),
  text('Na prática', 'XML parecido <span class="g">em todo município.</span>', '', checks([('Retenções sempre no mesmo lugar', 'ISS, PIS, COFINS, IR, CSLL e INSS'), ('Menos portal diferente', 'para baixar e consultar'), ('IBS e CBS na nota', 'desde 01/10/2026, em fase de teste')])),
  text('O que conferir', 'O sistema do escritório <span class="g">lê o novo XML?</span>', 'Se o relatório do mês não mostra as retenções e o grupo IBSCBS das notas de serviço, ele está incompleto.'),
  (cta('Comente <span class="g">NFSE</span> que a gente te mostra como o Painel organiza as notas de serviço.', 'SALVE PARA O FECHAMENTO'), True),
], LEG('Carrossel · NFS-e padrão nacional', '21/10/2026 (qua) às 12h', 'Carrossel 5 lâminas · 1080x1350',
  'NFS-e padrão nacional: um XML parecido para todo município e retenções sempre no mesmo lugar. 🧾\n\nO que muda para quem baixa e confere nota de serviço todo mês.\n\nComente NFSE que a gente te chama no direct.',
  TG_FI, 'Carrossel explicando a NFS-e no padrão nacional e o que o escritório deve conferir.', MUS_C))
# ============ 23/10 sex · Carrossel série coisas que só... ============
def meme(photo, txt, x=None):
    return (ph(photo, 0.6, x) + shade(.2, .95, 48) +
            f"<div style='position:absolute;left:86px;right:86px;bottom:150px'><div class='h' style='font-size:74px'>{txt}</div></div>", False)
P['23-10_carrossel_coisas_que_so_quem_trabalha'] = lambda f: carousel(f, [
  (cover('cafe_grupo', 'Série', 'Coisas que só quem trabalha em escritório contábil <span class="g">entende.</span>', size=92), False),
  meme('tel_ocupada', 'Atender o telefone já sabendo <span class="g">qual cliente é</span> pelo toque.'),
  meme('focada2', 'Ler “é rapidinho” e <span class="g">cancelar a tarde.</span>'),
  meme('equipe_monitor', 'Três pessoas no mesmo monitor <span class="g">olhando um erro estranho.</span>'),
  meme('highfive', '“Achei!” e a sala inteira <span class="g">solta o ar.</span>'),
  (cta('Qual faltou? <span class="g">Comenta a sua.</span>', 'MANDE PARA A EQUIPE'), True),
], LEG('Carrossel · série "coisas que só quem trabalha em escritório contábil entende"', '23/10/2026 (sex) às 12h', 'Carrossel 6 lâminas · 1080x1350',
  'Coisas que só quem trabalha em escritório contábil entende. 😅 Qual delas é a mais real aí?\n\nComenta a sua que ela pode entrar na próxima.',
  TG_GE, 'Carrossel com fotos de pessoas em escritório e frases bem-humoradas sobre a rotina contábil.', 'Áudio em alta do Instagram, leve e bem-humorado (escolha no app no dia).'))
# ============ 24/10 sáb · Estático mito x verdade ============
P['24-10_estatico_mito_automacao'] = lambda f: static(f,
  "<div style='position:absolute;left:86px;right:86px;top:230px'><div class='kicker'>Mito × verdade</div>"
  "<div class='h' style='font-size:84px;margin-top:40px;color:#8A8A92;-webkit-text-fill-color:#9A9AA2;text-decoration:line-through;text-decoration-color:#EF4444'>“Automação é coisa de escritório grande.”</div>"
  "<div class='h' style='font-size:96px;margin-top:60px'>É o que deixa o pequeno <span class='g'>crescer sem contratar alguém só pra baixar XML.</span></div></div>",
  LEG('Estático · mito x verdade', '24/10/2026 (sáb) às 10h', 'Post único 1080x1350',
  'Mito: automação é coisa de escritório grande.\nVerdade: num escritório de 4 pessoas, cada hora de portal faz falta. 🤖\n\nO que você automatizaria primeiro?',
  TG_GE, 'Post com a frase riscada "automação é coisa de escritório grande" e a resposta em verde.', MUS_E))
# ============ 25/10 dom · Carrossel 13º ============
P['25-10_carrossel_13_salario_datas'] = lambda f: carousel(f, [
  (cover('estagiario', 'Departamento pessoal', '13º salário: <span class="g">avise o cliente em outubro.</span>'), False),
  big('1ª parcela', '30/11', 'SEGUNDA-FEIRA', 'Metade do 13º, sem descontos de INSS e IR.'),
  big('2ª parcela', '18/12', 'SEXTA-FEIRA', 'O prazo é 20/12, que em 2026 cai num domingo. Antecipe.'),
  text('Proporcional', '1/12 por mês com <span class="g">15 dias ou mais.</span>', 'Quem foi contratado no meio do ano recebe proporcional. Mês com menos de 15 dias trabalhados não conta.'),
  text('Mensagem pronta', 'Copie e mande <span class="g">hoje.</span>', '', "<div class='card' style='padding:34px 38px;font-size:32px;line-height:1.5;color:#E5E5E8'>Oi! Lembrete do escritório: a 1ª parcela do 13º vence em 30/11 e a 2ª em 18/12. Já dá pra separar o caixa. Qualquer dúvida, chama aqui 💚</div>"),
  (cta('Salve e mande para quem cuida do <span class="g">DP.</span>'), True),
], LEG('Carrossel · 13º salário', '25/10/2026 (dom) às 18h', 'Carrossel 6 lâminas · 1080x1350',
  '13º salário: 1ª parcela até 30/11 e 2ª até 18/12 (o dia 20 cai num domingo em 2026). 📌\n\nTem mensagem pronta no carrossel para mandar pro cliente hoje.\n\nConfira sempre a convenção coletiva e a orientação oficial.',
  TG_DP, 'Carrossel com as datas do 13º salário em 2026 e uma mensagem pronta para o cliente.', MUS_C))
# ============ 27/10 ter · Carrossel emitidas x destinadas ============
P['27-10_carrossel_emitidas_vs_destinadas'] = lambda f: carousel(f, [
  (cover('madura_digita', 'Glossário', 'Notas emitidas × <span class="g">notas destinadas.</span>'), False),
  text('Lado a lado', 'Uma é venda. <span class="g">A outra é compra.</span>', '', vs('EMITIDAS', 'Notas que o seu cliente fez. Saídas.', 'DESTINADAS', 'Notas feitas contra o CNPJ dele. As compras.')),
  text('O problema', 'Pedir só as emitidas <span class="g">deixa o crédito de fora.</span>', 'As compras não entram na conferência, o estoque não fecha e o crédito some do mês.'),
  text('A solução', 'Baixar as duas, <span class="g">sem pedir para o cliente.</span>', 'Com o certificado do cliente, as destinadas podem ser consultadas direto na SEFAZ. O Painel faz isso sozinho, duas vezes por dia.'),
  (cta('As destinadas existem. <span class="g">A gente jura.</span>'), True),
], LEG('Carrossel · emitidas x destinadas', '27/10/2026 (ter) às 12h', 'Carrossel 5 lâminas · 1080x1350',
  'Emitidas são as vendas. Destinadas são as compras. Pedir só as emitidas deixa o crédito de fora. 🧾\n\nSalve e mande para o cliente que jura que "não tem nota de compra".',
  TG_FI, 'Carrossel comparando notas emitidas e destinadas.', MUS_C))
# ============ 29/10 qui · Carrossel split payment ============
P['29-10_carrossel_split_payment'] = lambda f: carousel(f, [
  (cover('tel_explica', 'Reforma tributária', 'Split payment: <span class="g">o que é e o que ainda não é.</span>'), False),
  text('O que é', 'O imposto separado <span class="g">no momento do pagamento.</span>', 'A parte do imposto vai direto para o governo, antes de o dinheiro chegar na empresa.'),
  text('O que ainda não é', 'Não está valendo <span class="g">hoje.</span>', 'Está previsto na reforma, com implantação gradual. Hoje nada muda no pagamento dos seus clientes.'),
  text('Onde focar agora', 'No que <span class="g">já mudou.</span>', '', checks([('A nota', 'IBS e CBS destacados em fase de teste'), ('O XML', 'grupo IBSCBS em cada item'), ('A conferência', 'relatório do mês com coluna por imposto')])),
  (cta('Notícia boa: <span class="g">dá tempo de aprender.</span>'), True),
], LEG('Carrossel · split payment', '29/10/2026 (qui) às 12h', 'Carrossel 5 lâminas · 1080x1350',
  'Split payment: o imposto separado no momento do pagamento. Está previsto na reforma, mas ainda não vale. 💡\n\nPor enquanto, o foco é a nota e o XML. Salve para quando o cliente perguntar.',
  TG_RF, 'Carrossel explicando o split payment e o que já mudou na nota.', MUS_C))
# ============ 30/10 sex · Estático último dia útil ============
P['30-10_estatico_ultimo_dia_util'] = lambda f: static(f,
  "<div style='position:absolute;left:86px;right:86px;top:220px'><div class='kicker'>Sexta · último dia útil de outubro</div>"
  "<div class='h' style='font-size:96px;margin-top:36px'>3 coisas para <span class='g'>conferir hoje.</span></div><div style='margin-top:60px'>" +
  checks([('Notas canceladas do mês', 'fora da soma do faturamento'), ('Destinadas baixadas', 'compras de todos os clientes'), ('Certificados que vencem em novembro', 'avise o cliente antes')]) + "</div></div>",
  LEG('Estático · último dia útil', '30/10/2026 (sex) às 8h', 'Post único 1080x1350',
  'Último dia útil de outubro. ✅ 3 conferências rápidas antes de fechar o mês.\n\nSalve para todo fim de mês.',
  TG_GE, 'Checklist de último dia útil: canceladas, destinadas e certificados.', MUS_E))
# ============ 01/11 dom · Carrossel novembro ============
P['01-11_carrossel_novembro_no_escritorio'] = lambda f: carousel(f, [
  (cover('sofa_laptop', 'Novembro', 'O mês do escritório contábil <span class="g">em 4 datas.</span>'), False),
  text('Calendário', 'Marque no <span class="g">calendário do escritório.</span>', '', rows([('20/11 · Consciência Negra', 'FERIADO NACIONAL'), ('DAS e FGTS Digital', 'CONFIRA A DATA OFICIAL'), ('27/11 · Black Friday', 'LIMITE DO SIMPLES'), ('30/11 · 13º 1ª parcela', 'SEGUNDA-FEIRA')], hl=3)),
  text('Feriado no dia 20', 'Vencimento em feriado <span class="g">muda de data.</span>', 'Cada guia tem a sua regra: umas vão para o próximo dia útil, outras são antecipadas. Confira na agenda oficial e avise o cliente da data certa.'),
  text('Black Friday', 'Faturou o dobro? <span class="g">Olhe o limite.</span>', 'Cliente do Simples que vende muito em novembro pode chegar perto do sublimite. Projeção do ano agora, não em dezembro.'),
  (cta('Novembro organizado começa <span class="g">hoje.</span>', 'SALVE O CALENDÁRIO'), True),
], LEG('Carrossel · novembro no escritório', '01/11/2026 (dom) às 18h', 'Carrossel 5 lâminas · 1080x1350',
  'Novembro em 4 datas: feriado no dia 20, guias do mês, Black Friday dos clientes e 1ª parcela do 13º. 🗓️\n\n20/11 é feriado nacional: confira na agenda oficial a data certa de cada guia antes de avisar o cliente.',
  TG_SN, 'Carrossel com o calendário de novembro para escritórios contábeis.', MUS_C))
# ============ 02/11 seg · Estático feriado ============
P['02-11_estatico_feriado_desconecta'] = lambda f: static(f,
  ph('cel_maos', 0.6, None, 'saturate(.85) brightness(.75)') + shade(.5, .97, 20) +
  "<div style='position:absolute;left:86px;right:86px;bottom:160px'><div class='kicker'>2 de novembro · feriado</div>"
  "<div class='h' style='font-size:108px;margin-top:30px'>Não perturbe: <span class='g'>ativado.</span></div>"
  "<div class='p' style='margin-top:28px;color:#C9CAD0'>O celular do contador também merece descanso. Amanhã a gente volta. 💚</div></div>",
  LEG('Estático · feriado de Finados', '02/11/2026 (seg, feriado) às 10h', 'Post único 1080x1350',
  'Hoje o celular fica no "não perturbe". 📵 Bom descanso para todos os escritórios.',
  TG_GE, 'Mãos segurando o celular com o texto: não perturbe ativado.', MUS_E), grid=False)
# ============ 04/11 qua · Carrossel férias coletivas ============
P['04-11_carrossel_ferias_coletivas'] = lambda f: carousel(f, [
  (cover('tel_calma', 'Departamento pessoal', 'Férias coletivas em dezembro? <span class="g">Pergunte hoje.</span>'), False),
  big('Comunicação', '15', 'DIAS ANTES', 'Aviso ao órgão do Ministério do Trabalho, ao sindicato e aos empregados com antecedência mínima de 15 dias.'),
  big('Pagamento', '2', 'DIAS ANTES', 'As férias (com o terço) são pagas até 2 dias antes do início.'),
  text('As perguntas', 'O que perguntar <span class="g">ao cliente agora.</span>', '', checks([('Vai ter férias coletivas?', 'para todos ou só alguns setores'), ('Quais datas?', 'início e retorno'), ('Tem quem não completou o período?', 'férias proporcionais')])),
  (cta('Descobrir no dia 20 de dezembro <span class="g">não dá tempo.</span>', 'SALVE PARA O DP'), True),
], LEG('Carrossel · férias coletivas', '04/11/2026 (qua) às 18h', 'Carrossel 5 lâminas · 1080x1350',
  'Férias coletivas no fim do ano: comunicação com 15 dias de antecedência e pagamento até 2 dias antes. 🏖️\n\nPergunte ao cliente hoje. Confira sempre a convenção coletiva da categoria.',
  TG_DP, 'Carrossel com prazos de férias coletivas e perguntas para o cliente.', MUS_C))
# ============ 05/11 qui · Carrossel limite do Simples (indicação produto) ============
BARH = ("<div class='card' style='padding:36px 38px'><div class='mono' style='font-size:22px;letter-spacing:.3em;color:#8A8A92'>COMÉRCIO EXEMPLO LTDA · 12 MESES</div>"
        "<div style='height:30px;background:#1E1E22;border-radius:15px;overflow:hidden;margin-top:28px'><div style='height:100%;width:90%;background:linear-gradient(90deg,#10B981,#F59E0B)'></div></div>"
        "<div style='display:flex;justify-content:space-between;font-size:32px;margin-top:18px'><b>R$ 4,31 mi</b><span style='color:#8A8A92'>limite R$ 4,8 mi</span></div>"
        "<div style='margin-top:24px;font-size:30px;color:#F59E0B;font-weight:700'>⚠ projeção do ano passa do limite em dezembro</div>"
        "<div class='mono' style='font-size:20px;color:#6E6E76;margin-top:18px;letter-spacing:.1em'>DADOS DE DEMONSTRAÇÃO · EMPRESA FICTÍCIA</div></div>")
P['05-11_carrossel_limite_do_simples'] = lambda f: carousel(f, [
  (cover('socio_tela', 'Simples Nacional', 'O limite do Simples <span class="g">não avisa.</span> Você precisa olhar.'), False),
  text('Os números', 'Os limites <span class="g">de 2026.</span>', '', rows([('MEI', 'R$ 81 MIL / ANO'), ('Simples Nacional', 'R$ 4,8 MI / ANO'), ('Sublimite ICMS/ISS', 'R$ 3,6 MI / ANO')], hl=1)),
  text('O risco', 'Novembro e dezembro <span class="g">vendem mais.</span>', 'Black Friday e Natal podem empurrar o faturamento acumulado para perto do limite justamente no fim do ano.'),
  text('Como acompanhar', 'Projeção mês a mês, <span class="g">com alerta.</span>', '', BARH),
  (cta('Comente <span class="g">LIMITE</span> e veja o alerta do Painel numa demonstração.', 'SALVE PARA NOVEMBRO'), True),
], LEG('Carrossel · limite do Simples', '05/11/2026 (qui) às 12h', 'Carrossel 5 lâminas · 1080x1350',
  'MEI até R$ 81 mil, Simples até R$ 4,8 milhões, sublimite de R$ 3,6 milhões para ICMS e ISS. 📈\n\nNovembro e dezembro vendem mais: acompanhe a projeção agora. No Painel Fiscal, o alerta aparece antes do problema.\n\nComente LIMITE que a gente te mostra.',
  TG_SN, 'Carrossel com os limites do Simples e uma barra de projeção de faturamento de uma empresa fictícia.', MUS_C))
# ============ 07/11 sáb · Carrossel 3 hábitos ============
P['07-11_carrossel_3_habitos'] = lambda f: carousel(f, [
  (cover('headset', 'Gestão', '3 hábitos que deixam um escritório pequeno <span class="g">parecer grande.</span>', size=92), False),
  text('01', 'Responder <span class="g">no mesmo dia.</span>', 'Mesmo que seja para dizer quando vai resolver. Silêncio é o que mais irrita cliente.', size=96),
  text('02', 'Mandar o relatório <span class="g">sem ele pedir.</span>', 'Um PDF por mês com o que entrou, o que saiu e o que vem pela frente. O cliente começa a enxergar o seu trabalho.', size=96),
  text('03', 'Avisar <span class="g">antes.</span>', 'Limite chegando, certificado vencendo, prazo na semana. Quem avisa antes nunca é o culpado.', size=96),
  (cta('Atendimento é o que o <span class="g">cliente vê.</span>', 'MANDE PARA O SÓCIO'), True),
], LEG('Carrossel · 3 hábitos', '07/11/2026 (sáb) às 10h', 'Carrossel 5 lâminas · 1080x1350',
  '3 hábitos que fazem um escritório pequeno parecer grande. 💚 Qual deles vocês já fazem?\n\nMande para o sócio. 😉',
  TG_GE, 'Carrossel com três hábitos de atendimento para escritórios contábeis.', MUS_C))
# ============ 08/11 dom · Carrossel 13º proporcional ============
P['08-11_carrossel_13_proporcional'] = lambda f: carousel(f, [
  (cover('anota_papel', 'Departamento pessoal', '13º de quem entrou no meio do ano: <span class="g">o erro mais comum.</span>', size=90), False),
  text('A regra', '1/12 por mês <span class="g">com 15 dias ou mais.</span>', 'Mês com menos de 15 dias trabalhados não entra na conta.'),
  text('Exemplo', 'Contratada em <span class="g">20 de março.</span>', '', rows([('Março (12 dias)', 'NÃO CONTA'), ('Abril a dezembro', '9 MESES'), ('13º proporcional', '9/12 DO SALÁRIO')], hl=2)),
  text('Na prática', 'Salário de R$ 2.400 <span class="g">→ 13º de R$ 1.800.</span>', 'R$ 2.400 ÷ 12 × 9 = R$ 1.800 (antes de INSS e IR, que entram na 2ª parcela). Valores ilustrativos.'),
  (cta('Salve para o <span class="g">cálculo de novembro.</span>', 'SALVE PARA O DP'), True),
], LEG('Carrossel · 13º proporcional', '08/11/2026 (dom) às 18h', 'Carrossel 5 lâminas · 1080x1350',
  '13º de quem foi contratado no meio do ano: 1/12 por mês com 15 dias ou mais trabalhados. Contratou dia 20? Aquele mês não entra. 🧮\n\nTem exemplo com conta no carrossel. Salve para novembro.',
  TG_DP, 'Carrossel com a regra e um exemplo de cálculo do 13º proporcional.', MUS_C))
if __name__ == '__main__':
    keys = sys.argv[1:] or list(P)
    for k in keys: print(P[k](k))
