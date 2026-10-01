# Série "Escritório sem falas"

Animações curtas (8–15 s) num escritório contábil, com bonecos sem rosto e sem fala.
Quem conta a piada é o corpo (espreguiçar, murchar, congelar) e os **balões, com texto curto que dá para ler**.
O som é o **contabilês**: sílabas inventadas, como nos jogos tipo The Sims. Ninguém fala de verdade, então não
depende de voz gravada nem de sotaque.

## Visual (o mesmo dos posts)
- Fundo preto #0A0A0A com a grade e o brilho verde no canto, logo no topo.
- Kicker em JetBrains Mono ("ESCRITÓRIO SEM FALAS · EP. 01") e título em Inter 800 com a palavra-chave em verde.
- Relógio digital "HORA" em verde à direita do título.
- A cena fica dentro de um card escuro (#121214) com borda fina, como os cards dos carrosséis.
- Rodapé "PAINEL FISCAL · EPIVERSO". A faixa de baixo fica livre para a legenda do app.

## Personagens (sempre os mesmos, para o público reconhecer)
- **O Fiscal**: branco, macio, com headset verde Epiverso. Não tem rosto; o microfone mostra para onde ele olha.
- Próximos: **o Sócio** (gravata cinza), **a Estagiária** (crachá verde) e **o Cliente**, que só aparece
  pelo celular (balão escuro). Mais adiante, o **robô do Painel**: um mini-robô verde que aparece à meia-noite.

## Regras dos balões
- Balão claro = alguém do escritório. Balão escuro com borda verde e etiqueta "CLIENTE · HORA" = cliente.
- No máximo 2 linhas e uns 6 palavras. Cada balão fica pelo menos 2 s na tela, para dar tempo de ler.
- No som, cada personagem tem um tom: o Fiscal é médio e fofo, o cliente é agudo e com som de telefone.

## Próximos episódios (ideias)
1. **Dia 19, 17h**: as notificações não param e o Fiscal vira um polvo com 8 braços digitando.
2. **Certificado vencido**: aparece um cadeado no monitor; ele procura o token na gaveta e acha 3 iguais.
3. **Portal da prefeitura fora do ar**: barra de carregamento infinita; ele faz origami e cria teia de aranha.
4. **Boleto em foto torta**: ele inclina o corpo inteiro para conseguir ler.
5. **Meia-noite**: o robô verde do Painel entra e as notas voam sozinhas para as pastas enquanto o Fiscal dorme.
6. **Sexta 17h59**: o Sócio chega com um balão de 📋 "só uma coisinha".
7. **Reforma tributária**: balão do cliente "IBS? CBS? 😱"; o Fiscal responde em contabilês com "0,9%".

## Como é feito
Desenho em SVG e animação por linha do tempo em JavaScript, renderizados quadro a quadro (30 fps). O som é todo
sintetizado em Python (sem direitos de terceiros). Arquivos em `_producao/`: `ep01.py` (cena e animação),
`synth.py` (vozes e efeitos), `ep01_audio.py` (trilha do episódio).
