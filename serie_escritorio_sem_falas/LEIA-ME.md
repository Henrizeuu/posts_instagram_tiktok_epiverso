# Série "Escritório sem falas"

Animações curtas (8–15 s) num escritório contábil, com bonecos sem rosto e sem fala.
Quem conta a piada é o corpo (espreguiçar, murchar, congelar), os balões e o **contabilês**,
a língua inventada dos bonecos: glifos no balão + sons de sílabas que não querem dizer nada.
Como não tem idioma, funciona para qualquer pessoa, sem legenda, e não depende de voz gravada.

## Personagens (sempre os mesmos, para o público reconhecer)
- **O Fiscal**: branco, macio, com headset verde Epiverso. Não tem rosto; o microfone mostra para onde ele olha.
- Próximos: **o Sócio** (gravata cinza), **a Estagiária** (crachá verde) e **o Cliente**, que só aparece
  pelo celular (balão escuro). Mais adiante, o **robô do Painel**: um mini-robô verde que aparece à meia-noite.

## Regras do contabilês
- Balão claro = pessoa do escritório. Balão escuro = cliente (no celular).
- Dentro do balão: 2 a 3 "palavras" em glifos + 1 ou 2 símbolos que todo contador entende (⏱️ 1', 🏠, 📎, 🧾, 🙏, DAS).
- Cada personagem tem um tom de voz: o Fiscal é médio e fofo; o cliente é agudo, com som de telefone.

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
