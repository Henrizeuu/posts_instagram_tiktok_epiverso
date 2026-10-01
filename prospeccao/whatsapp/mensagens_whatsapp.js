/*
  BANCO DE MENSAGENS · WHATSAPP · EPIVERSO
  =========================================
  Pode editar à vontade. Como funciona:

  {nome}        primeiro nome do contato           {escritorio}  nome do escritório
  {cidade}      cidade do escritório               {seu_nome}    seu nome (Configurações)
  {empresa}     Epiverso                           {periodo}     Bom dia / Boa tarde / Boa noite
  {periodo_min} bom dia / boa tarde / boa noite    {dor}         "as NFC-e", "as NFS-e"... (pela dor do lead)

  [a|b|c]  sorteia uma das opções a cada mensagem. [😊|] = às vezes com emoji, às vezes sem.
  Se uma frase usa um campo que o lead não tem (ex.: {cidade} vazio), ela é descartada
  automaticamente e o sorteio escolhe outra. Por isso, mantenha sempre variações sem campos.

  As dores: nfce · nfse · naocontrib · sefaz · geral
*/
window.MENSAGENS_WHATSAPP = {

  // Nome curto de cada dor (aparece no painel e no {dor})
  dores: {
    nfce:       { titulo: 'NFC-e',                 dor: 'as NFC-e dos clientes' },
    nfse:       { titulo: 'NFS-e',                 dor: 'as NFS-e dos clientes' },
    naocontrib: { titulo: 'Não contribuintes',     dor: 'as notas dos clientes não contribuintes' },
    sefaz:      { titulo: 'Demora na SEFAZ',       dor: 'a demora para pegar nota na SEFAZ' },
    geral:      { titulo: 'Geral (as 4 dores)',    dor: 'as notas dos clientes' }
  },

  // ---------------------------------------------------------------- ABERTURA (modo texto)
  saudacoes: [
    'Oi, {nome}, [tudo bem?|tudo certo?|como vai?]',
    'Olá, {nome}! [Tudo bem por aí?|Tudo certo?]',
    '{periodo}, {nome}! [Tudo bem?|Como vai?|Tudo certo por aí?]',
    '{periodo}, {nome}, [tudo bem?|como está a semana?]',
    '{nome}, {periodo_min}! [Tudo bem?|Tudo certo?]',
    'Oi {nome}, [tudo bem?|tudo certo?] [🙂|]',
    // sem nome
    'Oi, [tudo bem?|tudo certo?]',
    '{periodo}! [Tudo bem por aí?|Tudo certo?]',
    'Olá, [tudo bem?|como vai?]'
  ],

  apresentacoes: [
    'Aqui é {seu_nome}, da {empresa}.',
    'Sou {seu_nome}, da {empresa}.',
    'Meu nome é {seu_nome}, [falo|sou] da {empresa}.',
    '{seu_nome} aqui, da {empresa}.',
    'Sou {seu_nome}, da {empresa}. [A gente faz|Nós fazemos] um painel fiscal [só para|para] escritórios contábeis.',
    'Aqui é {seu_nome}. [Trabalho|Eu trabalho] com escritórios contábeis na {empresa}.'
  ],

  // Usado às vezes. Não use "o {escritorio}" / "no {escritorio}": não dá para saber se o nome é masculino ou feminino.
  contextos: [
    'Encontrei o contato de vocês [pesquisando|procurando] escritórios contábeis [em {cidade}|da região].',
    'Vi o contato de vocês ({escritorio}) e [resolvi te chamar direto|preferi te chamar direto].',
    'Estou conversando com alguns escritórios [de {cidade}|da região] [esta semana|estes dias].'
  ],

  // A pergunta-gancho: o coração da mensagem. Sempre termina em pergunta fácil de responder.
  ganchos: {
    nfce: [
      '[Uma pergunta rápida|Queria te fazer uma pergunta rápida|Me tira uma dúvida]: como vocês [fazem hoje|fazem] para pegar as NFC-e dos clientes do varejo?',
      'As NFC-e dos clientes de comércio, vocês ainda [dependem do cliente mandar|pedem para o cliente mandar] ou já conseguem pegar direto?',
      '[Curiosidade|Uma curiosidade]: quanto tempo o fiscal de vocês [gasta|perde] por mês correndo atrás de NFC-e de cliente?',
      'NFC-e de cliente do varejo ainda [é dor de cabeça|dá trabalho] aí no fechamento?'
    ],
    nfse: [
      'Como está [aí|aí no escritório] a rotina com NFS-e? [Cada prefeitura com um portal, cada cliente com uma senha...|Prefeitura por prefeitura, senha por senha...] Vocês já conseguiram centralizar isso?',
      '[Pergunta sincera|Uma pergunta]: as NFS-e dos clientes ainda chegam [por e-mail, planilha ou print|pelo cliente, por e-mail]?',
      'Vocês ainda baixam as NFS-e [prefeitura por prefeitura|portal por portal] ou já têm algo que [puxa sozinho|traz automático]?',
      'Quanto tempo vai por mês aí [só|] para juntar as NFS-e [dos clientes|de todos os clientes]?'
    ],
    naocontrib: [
      '[Uma dúvida|Me tira uma dúvida]: vocês conseguem pegar as notas dos clientes não contribuintes, [os que não têm IE|os sem inscrição estadual], sem depender deles mandarem?',
      'Os clientes [sem inscrição estadual|não contribuintes] de vocês, [prestadores e afins|prestador de serviço e afins]: as notas deles vocês pegam direto ou ainda pedem para eles?',
      'Nota de cliente não contribuinte ainda é [dor de cabeça|um problema] aí no escritório?',
      '[Pergunta rápida|Uma pergunta]: hoje, quando o cliente não é contribuinte de ICMS, como vocês [conseguem|pegam] as notas de entrada dele?'
    ],
    sefaz: [
      'Quanto tempo vocês levam [hoje|] para conseguir uma nota na SEFAZ quando o cliente pede [com urgência|para ontem]?',
      'Vocês ainda entram no portal da SEFAZ cliente por cliente para baixar XML? [Pergunto porque é a reclamação que eu mais escuto.|É a reclamação que mais escuto dos escritórios.]',
      'Quando falta uma nota no fechamento, quanto tempo leva [aí|no escritório] para achar ela na SEFAZ?',
      '[Uma curiosidade|Pergunta rápida]: quantas horas por mês o time de vocês passa [esperando a SEFAZ|no portal da SEFAZ] baixando nota?'
    ],
    geral: [
      'Hoje, o que dá mais trabalho aí: [buscar|] NFC-e, NFS-e, nota de cliente não contribuinte ou a demora da SEFAZ?',
      'Se você pudesse tirar uma dessas da rotina do escritório, qual seria: NFC-e, NFS-e, nota de não contribuinte ou [esperar a SEFAZ|a lentidão da SEFAZ]?',
      '[Uma pergunta rápida|Pergunta rápida]: onde o fiscal de vocês perde mais tempo hoje, NFC-e, NFS-e, cliente não contribuinte ou SEFAZ?'
    ]
  },

  // Uma frase de valor (entra só às vezes, para a mensagem não virar propaganda)
  pontes: {
    nfce:       ['[A gente criou|Criamos] um robô que busca as NFC-e [sozinho|automaticamente] na SEFAZ, às 00h e às 12h.'],
    nfse:       ['[A gente criou|Criamos] um robô que [traz|puxa] as NFS-e [sozinho|automaticamente], sem entrar [prefeitura por prefeitura|em portal].'],
    naocontrib: ['[A gente criou|Criamos] um robô que [busca|traz] essas notas [sozinho|automaticamente], inclusive de cliente sem IE.'],
    sefaz:      ['[A gente criou|Criamos] um robô que [vai na SEFAZ|busca na SEFAZ] às 00h e às 12h e deixa [tudo|as notas] [separado|organizado] por cliente.'],
    geral:      ['[A gente criou|Criamos] um robô que [busca|traz] NF-e, NFC-e, CT-e e NFS-e [sozinho|automaticamente], às 00h e às 12h.']
  },

  // Saída fácil: reduz denúncia (é o que mais derruba número)
  fechamentos: [
    'Se não for com você, [me indica|pode me indicar] quem cuida do fiscal?',
    'Se não fizer sentido, é só me avisar que [não te incomodo mais|eu não te chamo mais]. [🙏|]',
    '[Sem compromisso|Sem compromisso nenhum], [é só curiosidade mesmo|só quero entender como vocês fazem].',
    'Se não for o momento, [tudo bem|sem problema], é só me falar.',
    ''
  ],

  // --------------------------------------------------------- ABERTURA (modo olá + áudio)
  // Só o "olá". O áudio vem logo depois (roteiros abaixo).
  ola_audio: [
    'Oi, {nome}, [tudo bem?|tudo certo?]',
    '{periodo}, {nome}! [Tudo bem?|Tudo certo?]',
    'Olá, {nome}! [Tudo bem por aí?|Como vai?]',
    '{periodo}, {nome}! [Aqui é|Sou] {seu_nome}, da {empresa}. [Vou te mandar|Te mando] um áudio [rapidinho|curtinho], [menos de 1 minuto|coisa de 40 segundos].',
    'Oi, {nome}! Sou {seu_nome}, da {empresa}. [Gravei|Vou gravar] um áudio [rápido|curto] [para te explicar por que estou te chamando|para explicar o motivo do contato], [tudo bem?|pode ser?]',
    // sem nome
    'Oi, [tudo bem?|tudo certo?]',
    '{periodo}! [Tudo bem?|Tudo certo por aí?] Aqui é {seu_nome}, da {empresa}.'
  ],

  // Roteiros para você gravar (30 a 45 s). Fale com as suas palavras: o roteiro é um guia.
  roteiros_audio: {
    nfce: [
      'Oi[, {nome}|], tudo bem? Aqui é {seu_nome}, da {empresa}. Vou ser rápido. A gente trabalha só com escritório contábil, e a reclamação que eu mais escuto é NFC-e: cliente do varejo que não manda o XML, cupom que só aparece no fechamento… A gente tem um robô que vai na SEFAZ sozinho, à meia-noite e ao meio-dia, e traz as notas de todos os clientes, NFC-e inclusive, já separadas por cliente e por mês. Queria te perguntar: hoje, como vocês pegam essas NFC-e aí? Se fizer sentido, te mostro em quinze minutinhos. Abraço!',
      'E aí[, {nome}|], tudo certo? {seu_nome}, da {empresa}. Te chamei porque quase todo escritório que eu converso perde um tempão correndo atrás de NFC-e de cliente de comércio. O nosso painel faz isso sozinho: duas vezes por dia ele busca na SEFAZ e deixa tudo organizado. Me conta como vocês fazem hoje? Se quiser, te mostro funcionando com um cliente seu. Valeu!'
    ],
    nfse: [
      'Oi[, {nome}|], tudo bem? Aqui é {seu_nome}, da {empresa}. Rapidinho: você sabe como é NFS-e, né? Cada prefeitura com um portal, cada cliente com uma senha, e no fim a nota chega por e-mail ou print. A gente tem um painel que traz as NFS-e dos clientes automaticamente, com as retenções certinhas, sem ninguém entrar em portal. Queria entender como vocês fazem hoje aí. Se fizer sentido, te mostro em quinze minutos. Abraço!',
      '[{nome}, tudo certo?|Tudo certo?] {seu_nome}, da {empresa}. Te chamei por causa de NFS-e: é onde a maioria dos escritórios mais perde tempo hoje. O nosso robô puxa as NFS-e sozinho e já mostra base, retenções e líquido de cada nota. Como está essa rotina aí no escritório? Se quiser ver, te mostro rapidinho. Valeu!'
    ],
    naocontrib: [
      'Oi[, {nome}|], tudo bem? Aqui é {seu_nome}, da {empresa}. Vou direto ao ponto: nota de cliente não contribuinte, aquele cliente sem inscrição estadual, normalmente só chega quando o cliente lembra de mandar, né? O nosso robô busca essas notas sozinho, junto com as dos outros clientes, e deixa tudo separado por cliente e por mês. Como vocês fazem hoje aí? Se fizer sentido, te mostro em quinze minutos. Abraço!',
      '[{nome}, tudo certo?|Tudo certo?] {seu_nome}, da {empresa}. Uma coisa que pouca gente consegue resolver é nota de cliente não contribuinte. A gente resolveu: o painel busca automaticamente, inclusive de quem não tem IE. Queria saber se isso é um problema aí também. Se for, te mostro funcionando. Valeu!'
    ],
    sefaz: [
      'Oi[, {nome}|], tudo bem? Aqui é {seu_nome}, da {empresa}. Rapidinho: quanto tempo vocês levam hoje para conseguir uma nota na SEFAZ? Porque o que eu mais escuto é portal lento, cliente por cliente, e nota que falta só no fechamento. O nosso robô vai na SEFAZ sozinho, à meia-noite e ao meio-dia, e de manhã está tudo no painel, organizado. Achar uma nota leva segundos. Se fizer sentido, te mostro em quinze minutinhos. Abraço!',
      '[{nome}, tudo certo?|Tudo certo?] {seu_nome}, da {empresa}. Te chamei porque a gente tirou o portal da SEFAZ da rotina dos escritórios: o robô baixa as notas de todos os clientes duas vezes por dia, e você acha qualquer nota pelo número, nome ou chave na hora. Como está isso aí hoje? Se quiser, te mostro. Valeu!'
    ],
    geral: [
      'Oi[, {nome}|], tudo bem? Aqui é {seu_nome}, da {empresa}. Vou ser rápido: a gente fez um painel fiscal para escritório contábil que resolve as quatro coisas que mais travam o fechamento: NFC-e, NFS-e, nota de cliente não contribuinte e a demora da SEFAZ. Um robô busca tudo sozinho, à meia-noite e ao meio-dia, e deixa organizado por cliente e por mês. Qual dessas dá mais trabalho aí hoje? Se fizer sentido, te mostro em quinze minutos. Abraço!'
    ]
  },

  // ----------------------------------------------------------------- FOLLOW-UP (1 só)
  // Vai X dias depois da abertura (Configurações), só para quem não respondeu.
  followups: [
    'Oi[, {nome}|]! [Só voltando aqui rapidinho.|Passando rapidinho de novo.] [Faz sentido|Vale] eu te mostrar em 15 minutos como o robô [resolve isso|cuida disso] [sozinho|automaticamente]? Se não for o momento, sem problema. [🙂|]',
    '[{nome}, só complementando|Só complementando] minha mensagem: o painel da {empresa} [busca|baixa] NF-e, NFC-e, CT-e e NFS-e dos clientes [sozinho|automaticamente], inclusive dos não contribuintes. Se quiser, te mostro com um cliente seu. [Faz sentido?|Pode ser?]',
    'Oi[ {nome}|], [tudo bem?|tudo certo?] Te chamei [uns dias atrás|semana passada] sobre {dor}. Se não for prioridade agora, [tranquilo|sem problema], é só me avisar que eu paro por aqui. [👍|]',
    '{periodo}[, {nome}|]! [Imagino que a rotina esteja corrida.|Sei que a rotina está puxada.] [Só queria saber|Queria só saber] se isso ({dor}) ainda [toma tempo|dá trabalho] aí. Se sim, te mostro uma solução em 15 min. Se não, [sem problema|tudo bem]!'
  ],

  // ------------------------------------------------------------- RESPOSTAS PRONTAS
  // Para quando a pessoa responde. Aqui link pode (ela já conversou com você).
  respostas: [
    { titulo: 'Tem interesse / quer ver',
      texto: 'Que ótimo, {nome}! Consigo te mostrar em 15 minutos, por vídeo, com os clientes do seu escritório, para você ver as notas aparecendo no painel. Fica melhor [amanhã às 10h ou às 15h|amanhã de manhã ou à tarde]?' },
    { titulo: 'Quanto custa?',
      texto: 'Depende do volume de XMLs por mês dos seus clientes, {nome}. Temos plano de 15 mil XMLs/mês, de 25 mil e o ilimitado. Me passa mais ou menos quantos clientes vocês atendem que eu te digo qual encaixa e o valor certinho. 🙂' },
    { titulo: 'Já temos sistema',
      texto: 'Ótimo, {nome}! Qual vocês usam? Pergunto porque muitos escritórios têm sistema e mesmo assim ainda correm atrás de NFC-e, NFS-e e nota de não contribuinte na mão. Se o seu já resolve tudo isso, perfeito. Se não, o painel funciona junto, sem trocar nada.' },
    { titulo: 'Manda material',
      texto: 'Mando sim, {nome}! [cole aqui o link do vídeo ou da página]. Mas te falo: em 15 minutos ao vivo, com os seus clientes, fica bem mais claro. Se quiser, a gente marca.' },
    { titulo: 'Agora não / sem tempo',
      texto: 'Tranquilo, {nome}! Fechamento é corrido mesmo. Posso te chamar de novo [no começo do mês que vem|daqui a umas semanas]?' },
    { titulo: 'Não tenho interesse',
      texto: 'Sem problema, {nome}, obrigado pelo retorno! Não te chamo mais. Se um dia precisar, fica o contato. Boa semana! 👍' },
    { titulo: 'Como pegou meu número?',
      texto: 'Peguei o contato público do escritório [no Google / no site de vocês], {nome}. Trabalho só com escritórios contábeis e achei que podia ser útil. Se preferir que eu não chame mais, é só falar que eu tiro da lista.' },
    { titulo: 'Não sou eu que cuido',
      texto: 'Obrigado, {nome}! Pode me passar o nome ou o contato de quem cuida do fiscal aí? Prometo ser breve com a pessoa. 🙂' }
  ]
};
