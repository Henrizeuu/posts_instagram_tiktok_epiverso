// Mensagens padrão (o botão "Restaurar padrão" do painel volta para estas).
// Edite pelo painel: o que você salva lá fica em dados/mensagens.json.
export default {
  "whatsapp": {
    "saudacoes": [
      "Oi, {nome}, [tudo bem?|tudo certo?|como vai?]",
      "Olá, {nome}! [Tudo bem por aí?|Tudo certo?]",
      "{periodo}, {nome}! [Tudo bem?|Como vai?|Tudo certo por aí?]",
      "{periodo}, {nome}, [tudo bem?|como está a semana?]",
      "{nome}, {periodo_min}! [Tudo bem?|Tudo certo?]",
      "Oi {nome}, [tudo bem?|tudo certo?] [🙂|]",
      "Oi, [tudo bem?|tudo certo?]",
      "{periodo}! [Tudo bem por aí?|Tudo certo?]",
      "Olá, [tudo bem?|como vai?]"
    ],
    "apresentacoes": [
      "Aqui é {seu_nome}, da {empresa}.",
      "Sou {seu_nome}, da {empresa}.",
      "Meu nome é {seu_nome}, [falo|sou] da {empresa}.",
      "{seu_nome} aqui, da {empresa}.",
      "Sou {seu_nome}, da {empresa}. [A gente faz|Nós fazemos] um painel fiscal [só para|para] escritórios contábeis.",
      "Aqui é {seu_nome}. [Trabalho|Eu trabalho] com escritórios contábeis na {empresa}."
    ],
    "contextos": [
      "Encontrei o contato de vocês [pesquisando|procurando] escritórios contábeis [em {cidade}|da região].",
      "Vi o contato de vocês ({escritorio}) e [resolvi te chamar direto|preferi te chamar direto].",
      "Estou conversando com alguns escritórios [de {cidade}|da região] [esta semana|estes dias]."
    ],
    "ganchos": {
      "nfce": [
        "[Uma pergunta rápida|Queria te fazer uma pergunta rápida|Me tira uma dúvida]: como vocês [fazem hoje|fazem] para pegar as NFC-e dos clientes do varejo?",
        "As NFC-e dos clientes de comércio, vocês ainda [dependem do cliente mandar|pedem para o cliente mandar] ou já conseguem pegar direto?",
        "[Curiosidade|Uma curiosidade]: quanto tempo o fiscal de vocês [gasta|perde] por mês correndo atrás de NFC-e de cliente?",
        "NFC-e de cliente do varejo ainda [é dor de cabeça|dá trabalho] aí no fechamento?"
      ],
      "nfse": [
        "Como está [aí|aí no escritório] a rotina com NFS-e? [Cada prefeitura com um portal, cada cliente com uma senha...|Prefeitura por prefeitura, senha por senha...] Vocês já conseguiram centralizar isso?",
        "[Pergunta sincera|Uma pergunta]: as NFS-e dos clientes ainda chegam [por e-mail, planilha ou print|pelo cliente, por e-mail]?",
        "Vocês ainda baixam as NFS-e [prefeitura por prefeitura|portal por portal] ou já têm algo que [puxa sozinho|traz automático]?",
        "Quanto tempo vai por mês aí [só|] para juntar as NFS-e [dos clientes|de todos os clientes]?"
      ],
      "naocontrib": [
        "[Uma dúvida|Me tira uma dúvida]: vocês conseguem pegar as notas dos clientes não contribuintes, [os que não têm IE|os sem inscrição estadual], sem depender deles mandarem?",
        "Os clientes [sem inscrição estadual|não contribuintes] de vocês, [prestadores e afins|prestador de serviço e afins]: as notas deles vocês pegam direto ou ainda pedem para eles?",
        "Nota de cliente não contribuinte ainda é [dor de cabeça|um problema] aí no escritório?",
        "[Pergunta rápida|Uma pergunta]: hoje, quando o cliente não é contribuinte de ICMS, como vocês [conseguem|pegam] as notas de entrada dele?"
      ],
      "sefaz": [
        "Quanto tempo vocês levam [hoje|] para conseguir uma nota na SEFAZ quando o cliente pede [com urgência|para ontem]?",
        "Vocês ainda entram no portal da SEFAZ cliente por cliente para baixar XML? [Pergunto porque é a reclamação que eu mais escuto.|É a reclamação que mais escuto dos escritórios.]",
        "Quando falta uma nota no fechamento, quanto tempo leva [aí|no escritório] para achar ela na SEFAZ?",
        "[Uma curiosidade|Pergunta rápida]: quantas horas por mês o time de vocês passa [esperando a SEFAZ|no portal da SEFAZ] baixando nota?"
      ],
      "geral": [
        "Hoje, o que dá mais trabalho aí: [buscar|] NFC-e, NFS-e, nota de cliente não contribuinte ou a demora da SEFAZ?",
        "Se você pudesse tirar uma dessas da rotina do escritório, qual seria: NFC-e, NFS-e, nota de não contribuinte ou [esperar a SEFAZ|a lentidão da SEFAZ]?",
        "[Uma pergunta rápida|Pergunta rápida]: onde o fiscal de vocês perde mais tempo hoje, NFC-e, NFS-e, cliente não contribuinte ou SEFAZ?"
      ]
    },
    "pontes": {
      "nfce": [
        "[A gente criou|Criamos] um robô que busca as NFC-e [sozinho|automaticamente] na SEFAZ, às 00h e às 12h."
      ],
      "nfse": [
        "[A gente criou|Criamos] um robô que [traz|puxa] as NFS-e [sozinho|automaticamente], sem entrar [prefeitura por prefeitura|em portal]."
      ],
      "naocontrib": [
        "[A gente criou|Criamos] um robô que [busca|traz] essas notas [sozinho|automaticamente], inclusive de cliente sem IE."
      ],
      "sefaz": [
        "[A gente criou|Criamos] um robô que [vai na SEFAZ|busca na SEFAZ] às 00h e às 12h e deixa [tudo|as notas] [separado|organizado] por cliente."
      ],
      "geral": [
        "[A gente criou|Criamos] um robô que [busca|traz] NF-e, NFC-e, CT-e e NFS-e [sozinho|automaticamente], às 00h e às 12h."
      ]
    },
    "fechamentos": [
      "Se não for com você, [me indica|pode me indicar] quem cuida do fiscal?",
      "Se não fizer sentido, é só me avisar que [não te incomodo mais|eu não te chamo mais]. [🙏|]",
      "[Sem compromisso|Sem compromisso nenhum], [é só curiosidade mesmo|só quero entender como vocês fazem].",
      "Se não for o momento, [tudo bem|sem problema], é só me falar."
    ],
    "ola_audio": [
      "Oi, {nome}, [tudo bem?|tudo certo?]",
      "{periodo}, {nome}! [Tudo bem?|Tudo certo?]",
      "Olá, {nome}! [Tudo bem por aí?|Como vai?]",
      "{periodo}, {nome}! [Aqui é|Sou] {seu_nome}, da {empresa}. [Vou te mandar|Te mando] um áudio [rapidinho|curtinho], [menos de 1 minuto|coisa de 40 segundos].",
      "Oi, {nome}! Sou {seu_nome}, da {empresa}. [Gravei|Vou gravar] um áudio [rápido|curto] [para te explicar por que estou te chamando|para explicar o motivo do contato], [tudo bem?|pode ser?]",
      "Oi, [tudo bem?|tudo certo?]",
      "{periodo}! [Tudo bem?|Tudo certo por aí?] Aqui é {seu_nome}, da {empresa}."
    ],
    "followups": [
      "Oi[, {nome}|]! [Só voltando aqui rapidinho.|Passando rapidinho de novo.] [Faz sentido|Vale] eu te mostrar em 15 minutos como o robô [resolve isso|cuida disso] [sozinho|automaticamente]? Se não for o momento, sem problema. [🙂|]",
      "[{nome}, só complementando|Só complementando] minha mensagem: o painel da {empresa} [busca|baixa] NF-e, NFC-e, CT-e e NFS-e dos clientes [sozinho|automaticamente], inclusive dos não contribuintes. Se quiser, te mostro com um cliente seu. [Faz sentido?|Pode ser?]",
      "Oi[ {nome}|], [tudo bem?|tudo certo?] Te chamei [uns dias atrás|semana passada] sobre {dor}. Se não for prioridade agora, [tranquilo|sem problema], é só me avisar que eu paro por aqui. [👍|]",
      "{periodo}[, {nome}|]! [Imagino que a rotina esteja corrida.|Sei que a rotina está puxada.] [Só queria saber|Queria só saber] se isso ({dor}) ainda [toma tempo|dá trabalho] aí. Se sim, te mostro uma solução em 15 min. Se não, [sem problema|tudo bem]!"
    ],
    "roteiros_audio": {
      "nfce": [
        "Oi, tudo bem? Aqui é {seu_nome}, da {empresa}. Vou ser rápido. A gente trabalha só com escritório contábil, e a reclamação que eu mais escuto é NFC-e: cliente do varejo que não manda o XML, cupom que só aparece no fechamento… A gente tem um robô que vai na SEFAZ sozinho, à meia-noite e ao meio-dia, e traz as notas de todos os clientes, NFC-e inclusive, já separadas por cliente e por mês. Queria te perguntar: hoje, como vocês pegam essas NFC-e aí? Se fizer sentido, te mostro em quinze minutinhos. Abraço!",
        "E aí, tudo certo? {seu_nome}, da {empresa}. Te chamei porque quase todo escritório que eu converso perde um tempão correndo atrás de NFC-e de cliente de comércio. O nosso painel faz isso sozinho: duas vezes por dia ele busca na SEFAZ e deixa tudo organizado. Me conta como vocês fazem hoje? Se quiser, te mostro funcionando com um cliente seu. Valeu!"
      ],
      "nfse": [
        "Oi, tudo bem? Aqui é {seu_nome}, da {empresa}. Rapidinho: você sabe como é NFS-e, né? Cada prefeitura com um portal, cada cliente com uma senha, e no fim a nota chega por e-mail ou print. A gente tem um painel que traz as NFS-e dos clientes automaticamente, com as retenções certinhas, sem ninguém entrar em portal. Queria entender como vocês fazem hoje aí. Se fizer sentido, te mostro em quinze minutos. Abraço!",
        "Tudo certo? {seu_nome}, da {empresa}. Te chamei por causa de NFS-e: é onde a maioria dos escritórios mais perde tempo hoje. O nosso robô puxa as NFS-e sozinho e já mostra base, retenções e líquido de cada nota. Como está essa rotina aí no escritório? Se quiser ver, te mostro rapidinho. Valeu!"
      ],
      "naocontrib": [
        "Oi, tudo bem? Aqui é {seu_nome}, da {empresa}. Vou direto ao ponto: nota de cliente não contribuinte, aquele cliente sem inscrição estadual, normalmente só chega quando o cliente lembra de mandar, né? O nosso robô busca essas notas sozinho, junto com as dos outros clientes, e deixa tudo separado por cliente e por mês. Como vocês fazem hoje aí? Se fizer sentido, te mostro em quinze minutos. Abraço!",
        "Tudo certo? {seu_nome}, da {empresa}. Uma coisa que pouca gente consegue resolver é nota de cliente não contribuinte. A gente resolveu: o painel busca automaticamente, inclusive de quem não tem IE. Queria saber se isso é um problema aí também. Se for, te mostro funcionando. Valeu!"
      ],
      "sefaz": [
        "Oi, tudo bem? Aqui é {seu_nome}, da {empresa}. Rapidinho: quanto tempo vocês levam hoje para conseguir uma nota na SEFAZ? Porque o que eu mais escuto é portal lento, cliente por cliente, e nota que falta só no fechamento. O nosso robô vai na SEFAZ sozinho, à meia-noite e ao meio-dia, e de manhã está tudo no painel, organizado. Achar uma nota leva segundos. Se fizer sentido, te mostro em quinze minutinhos. Abraço!",
        "Tudo certo? {seu_nome}, da {empresa}. Te chamei porque a gente tirou o portal da SEFAZ da rotina dos escritórios: o robô baixa as notas de todos os clientes duas vezes por dia, e você acha qualquer nota pelo número, nome ou chave na hora. Como está isso aí hoje? Se quiser, te mostro. Valeu!"
      ],
      "geral": [
        "Oi, tudo bem? Aqui é {seu_nome}, da {empresa}. Vou ser rápido: a gente fez um painel fiscal para escritório contábil que resolve as quatro coisas que mais travam o fechamento: NFC-e, NFS-e, nota de cliente não contribuinte e a demora da SEFAZ. Um robô busca tudo sozinho, à meia-noite e ao meio-dia, e deixa organizado por cliente e por mês. Qual dessas dá mais trabalho aí hoje? Se fizer sentido, te mostro em quinze minutos. Abraço!"
      ]
    }
  },
  "email": {
    "assuntos": {
      "nfce": [
        "NFC-e dos clientes",
        "pergunta sobre NFC-e",
        "{escritorio} e as NFC-e",
        "[{nome}, |]NFC-e no fechamento",
        "cupom de cliente do varejo"
      ],
      "nfse": [
        "NFS-e dos clientes",
        "pergunta sobre NFS-e",
        "{escritorio} e as NFS-e",
        "[{nome}, |]NFS-e prefeitura por prefeitura",
        "notas de serviço no fechamento"
      ],
      "naocontrib": [
        "notas de não contribuintes",
        "cliente sem inscrição estadual",
        "{escritorio}: notas sem IE",
        "[{nome}, |]nota de não contribuinte",
        "pergunta sobre clientes sem IE"
      ],
      "sefaz": [
        "tempo no portal da SEFAZ",
        "pergunta sobre a SEFAZ",
        "{escritorio} e a SEFAZ",
        "[{nome}, |]XML no fechamento",
        "nota faltando no fechamento"
      ],
      "geral": [
        "pergunta rápida[, {nome}|]",
        "{escritorio}: rotina fiscal",
        "XML dos clientes",
        "rotina fiscal do escritório",
        "[{nome}, |]uma dúvida sobre o fechamento"
      ]
    },
    "saudacoes": [
      "Oi, {nome}, tudo bem?",
      "Olá, {nome}, tudo bem?",
      "{periodo}, {nome}!",
      "{nome}, [tudo bem?|tudo certo?]",
      "Olá, tudo bem?",
      "{periodo}!"
    ],
    "aberturas": {
      "nfce": [
        "[Sou {seu_nome}, da {empresa}.|Meu nome é {seu_nome} e falo da {empresa}.] [A gente trabalha só com escritórios contábeis|Nosso foco é o fiscal de escritórios contábeis], e [a reclamação que mais escuto|o que mais escuto nas conversas] é a NFC-e: [cliente do varejo que esquece de mandar o XML|cupom que só aparece quando o cliente lembra de mandar] e fechamento atrasado por causa de [meia dúzia de cupons|algumas notas que faltaram].\n\n[Criamos|Desenvolvemos] um robô que busca as notas na SEFAZ às 00h e às 12h e deixa tudo separado por cliente, modelo e mês, NFC-e inclusive.\n\n[Como vocês fazem isso hoje?|Hoje vocês pegam as NFC-e dos clientes como?|Como vocês resolvem isso hoje?] [Se fizer sentido|Se valer a pena], te mostro em 15 minutos com os clientes de vocês.",
        "[Sou {seu_nome}, da {empresa}.|{seu_nome} aqui, da {empresa}.] [Uma pergunta direta|Vou direto ao ponto]: [quanto tempo o fiscal de vocês gasta por mês|quantas horas por mês vão] correndo atrás de NFC-e de cliente do comércio?\n\nPergunto porque [é o ponto que mais trava o fechamento|é o que mais atrasa o fechamento] nos escritórios com quem converso. [No nosso painel|Na {empresa}], um robô [traz|baixa] as NFC-e [sozinho|automaticamente], duas vezes por dia, junto com NF-e, CT-e e NFS-e.\n\n[Vale uma conversa de 15 minutos?|Faz sentido eu te mostrar em 15 minutos?]"
      ],
      "nfse": [
        "[Sou {seu_nome}, da {empresa}.|Meu nome é {seu_nome} e falo da {empresa}.] [A gente trabalha só com escritórios contábeis|Nosso foco é o fiscal de escritórios contábeis], e NFS-e é [quase sempre|sempre] a parte mais trabalhosa: cada prefeitura com um portal, cada cliente com uma senha, e no fim a nota chega por e-mail ou print.\n\n[Nosso painel|O painel da {empresa}] traz as NFS-e dos clientes [sozinho|automaticamente], com cada retenção no campo certo e o líquido conferido, sem ninguém entrar em portal.\n\n[Como está essa rotina aí no escritório?|Como vocês fazem isso hoje?] [Se fizer sentido|Se valer a pena], te mostro em 15 minutos.",
        "[Sou {seu_nome}, da {empresa}.|{seu_nome} aqui, da {empresa}.] [Uma pergunta rápida|Pergunta sincera]: as NFS-e dos clientes de vocês ainda chegam [pelo cliente, por e-mail ou planilha|por e-mail, planilha ou print]?\n\nSe sim, [vocês não estão sozinhos|é o mesmo cenário da maioria dos escritórios]. [Criamos|Desenvolvemos] um robô que puxa as NFS-e [sozinho|automaticamente] e já organiza por cliente e mês, com base, retenções e líquido.\n\n[Vale uma conversa de 15 minutos?|Faz sentido eu te mostrar?]"
      ],
      "naocontrib": [
        "[Sou {seu_nome}, da {empresa}.|Meu nome é {seu_nome} e falo da {empresa}.] [A gente trabalha só com escritórios contábeis|Nosso foco é o fiscal de escritórios contábeis], e uma dor que [quase ninguém resolveu|pouca gente conseguiu resolver] é a nota de cliente não contribuinte: o prestador sem inscrição estadual cujas notas só chegam quando ele lembra de mandar.\n\n[Nosso robô|O robô da {empresa}] busca essas notas [sozinho|automaticamente], junto com as dos outros clientes, e deixa tudo separado por cliente e mês.\n\n[Como vocês fazem isso hoje?|Como vocês resolvem isso hoje?] [Se fizer sentido|Se valer a pena], te mostro em 15 minutos.",
        "[Sou {seu_nome}, da {empresa}.|{seu_nome} aqui, da {empresa}.] [Uma dúvida|Uma pergunta direta]: quando o cliente não é contribuinte de ICMS, como vocês conseguem as notas de entrada dele?\n\nPergunto porque [na maioria dos escritórios|em quase todo escritório] isso depende do cliente mandar, e [sempre falta alguma|alguma sempre fica para trás]. A gente [resolveu isso|automatizou isso]: o painel [busca|traz] as notas inclusive de quem não tem IE.\n\n[Vale 15 minutos para eu te mostrar?|Faz sentido uma conversa rápida?]"
      ],
      "sefaz": [
        "[Sou {seu_nome}, da {empresa}.|Meu nome é {seu_nome} e falo da {empresa}.] [A gente trabalha só com escritórios contábeis|Nosso foco é o fiscal de escritórios contábeis], e [a reclamação que mais escuto|o que mais escuto] é o tempo perdido no portal da SEFAZ: cliente por cliente, consulta lenta, e a nota que faltava aparece só no fechamento.\n\n[Criamos|Desenvolvemos] um robô que vai na SEFAZ às 00h e às 12h e baixa as notas de todos os clientes. De manhã está tudo no painel, e achar uma nota pelo número, nome ou chave leva segundos.\n\n[Quanto tempo vocês levam hoje para pegar uma nota na SEFAZ?|Como está isso aí no escritório hoje?] [Se fizer sentido|Se valer a pena], te mostro em 15 minutos.",
        "[Sou {seu_nome}, da {empresa}.|{seu_nome} aqui, da {empresa}.] [Uma pergunta rápida|Pergunta direta]: quando o cliente pede uma nota [com urgência|para ontem], quanto tempo leva até vocês acharem ela na SEFAZ?\n\n[Nos escritórios que usam a {empresa}|Com o nosso painel], isso leva segundos: um robô baixa tudo [sozinho|automaticamente] duas vezes por dia e organiza por cliente, modelo e mês.\n\n[Faz sentido eu te mostrar em 15 minutos?|Vale uma conversa rápida?]"
      ],
      "geral": [
        "[Sou {seu_nome}, da {empresa}.|Meu nome é {seu_nome} e falo da {empresa}.] [A gente fez|Desenvolvemos] um painel fiscal para escritórios contábeis que tira da rotina as quatro coisas que mais atrasam o fechamento: NFC-e, NFS-e, nota de cliente não contribuinte e a demora da SEFAZ.\n\nUm robô busca as notas de todos os clientes às 00h e às 12h e deixa tudo separado por cliente, modelo e mês.\n\n[Qual dessas mais pesa aí no escritório hoje?|Qual dessas dá mais trabalho aí hoje?] [Se fizer sentido|Se valer a pena], te mostro em 15 minutos."
      ]
    },
    "followup_1": [
      "[{nome}, só|Só] complementando a mensagem anterior.\n\nE não é só isso: o painel [cobre|resolve] [a rotina inteira|todas as pontas]: NF-e, NFC-e, CT-e e NFS-e, emitidas e destinadas, inclusive de clientes não contribuintes. [Hoje já são|Já organizamos] mais de 110 mil XMLs [no painel|por lá], sem ninguém entrar em portal.\n\n[Vale 15 minutos para eu te mostrar?|Faz sentido uma conversa rápida de 15 minutos?]",
      "[{nome}, voltando|Voltando] rapidinho ao meu e-mail.\n\n[Sei que a rotina de escritório é puxada|Imagino que a semana esteja corrida], então [resumo em uma linha|vou resumir]: o robô da {empresa} busca as notas dos clientes [sozinho|automaticamente] e deixa tudo pronto para conferir de manhã, com PDF, relatório e o ZIP do mês em um clique.\n\n[Te mostro em 15 minutos?|Faz sentido marcarmos 15 minutos?] Se não for prioridade agora, é só me avisar."
    ],
    "followup_2": [
      "{nome}, [imagino que a rotina esteja corrida|sei que a rotina está puxada], então vou ser breve: [este é meu último e-mail sobre o assunto.|não vou mais insistir.]\n\nSe em algum momento fizer sentido automatizar a busca de {dor}, é só responder este e-mail [que eu te mostro o painel|e a gente conversa].\n\n[Bom trabalho por aí!|Boa semana!]",
      "[{nome}, vou|Vou] encerrar por aqui para não lotar sua caixa.\n\nSe fizer sentido no futuro, é só responder [esta mensagem|este e-mail]. E se não for você quem cuida do fiscal aí no escritório, [fico grato se puder me indicar quem é|uma indicação já ajuda muito].\n\n[Abraço!|Obrigado e boa semana!]"
    ],
    "assinatura": "{seu_nome}\n{empresa} · Painel fiscal para escritórios contábeis\nWhatsApp {whatsapp}",
    "rodape_optout": [
      "Se preferir não receber mais e-mails meus, é só responder \"remover\".",
      "Para não receber mais mensagens, responda \"remover\" que eu tiro seu contato da lista.",
      "Não quer receber mais? Responda \"remover\" e eu não envio mais nada."
    ]
  },
  "respostas": [
    {
      "titulo": "Tem interesse / quer ver",
      "texto": "Que ótimo, {nome}! Consigo te mostrar em 15 minutos, por vídeo, com os clientes do seu escritório, para você ver as notas aparecendo no painel. Fica melhor [amanhã às 10h ou às 15h|amanhã de manhã ou à tarde]?"
    },
    {
      "titulo": "Quanto custa?",
      "texto": "Depende do volume de XMLs por mês dos seus clientes, {nome}. Temos plano de 15 mil XMLs/mês, de 25 mil e o ilimitado. Me passa mais ou menos quantos clientes vocês atendem que eu te digo qual encaixa e o valor certinho. 🙂"
    },
    {
      "titulo": "Já temos sistema",
      "texto": "Ótimo, {nome}! Qual vocês usam? Pergunto porque muitos escritórios têm sistema e mesmo assim ainda correm atrás de NFC-e, NFS-e e nota de não contribuinte na mão. Se o seu já resolve tudo isso, perfeito. Se não, o painel funciona junto, sem trocar nada."
    },
    {
      "titulo": "Manda material",
      "texto": "Mando sim, {nome}! [cole aqui o link do vídeo ou da página]. Mas te falo: em 15 minutos ao vivo, com os seus clientes, fica bem mais claro. Se quiser, a gente marca."
    },
    {
      "titulo": "Agora não / sem tempo",
      "texto": "Tranquilo, {nome}! Fechamento é corrido mesmo. Posso te chamar de novo [no começo do mês que vem|daqui a umas semanas]?"
    },
    {
      "titulo": "Não tenho interesse",
      "texto": "Sem problema, {nome}, obrigado pelo retorno! Não te chamo mais. Se um dia precisar, fica o contato. Boa semana! 👍"
    },
    {
      "titulo": "Como pegou meu número?",
      "texto": "Peguei o contato público do escritório [no Google / no site de vocês], {nome}. Trabalho só com escritórios contábeis e achei que podia ser útil. Se preferir que eu não chame mais, é só falar que eu tiro da lista."
    },
    {
      "titulo": "Não sou eu que cuido",
      "texto": "Obrigado, {nome}! Pode me passar o nome ou o contato de quem cuida do fiscal aí? Prometo ser breve com a pessoa. 🙂"
    }
  ]
};
