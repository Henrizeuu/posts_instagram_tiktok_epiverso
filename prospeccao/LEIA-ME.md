# Prospecção Epiverso · WhatsApp + E-mail

Sistema para prospectar escritórios contábeis todo dia, falando das 4 dores que o Painel Fiscal resolve:

| Dor | Gancho |
|---|---|
| **NFC-e** | cupom de cliente do varejo que só chega quando o cliente lembra de mandar |
| **NFS-e** | cada prefeitura com um portal, cada cliente com uma senha |
| **Não contribuintes** | notas de cliente sem IE que dependem do cliente mandar |
| **Demora na SEFAZ** | portal lento, cliente por cliente, nota que aparece só no fechamento |

- **WhatsApp:** 15 escritórios por dia, com mensagem diferente para cada um, em modo **texto** ou **olá + áudio**.
- **E-mail:** sequência de 3 e-mails na mesma conversa, com aquecimento automático (10 → 40 por dia por caixa) e parada automática quando o lead responde.

```
prospeccao/
├── LEIA-ME.md                  este guia
├── leads_exemplo.csv           modelo da planilha (serve para os dois canais)
├── whatsapp/
│   ├── painel_whatsapp.html    abra no navegador (duplo clique): fila do dia, mensagens, ritmo e métricas
│   └── mensagens_whatsapp.js   todas as variações de mensagem, roteiros de áudio e respostas prontas
└── email/
    ├── enviar_emails.py        envio com aquecimento, ritmo humano, follow-ups e leitura de respostas
    ├── mensagens_email.json    assuntos, aberturas por dor, follow-ups, assinatura
    └── config_exemplo.ini      copie para config.ini e preencha
```

> **Sem API, de propósito.** Qualquer ferramenta que envia WhatsApp sozinha sem a API oficial (extensão de disparo,
> robô no WhatsApp Web, whatsapp-web.js, Baileys) é o que mais derruba número: o WhatsApp detecta o padrão de robô.
> O painel faz tudo menos apertar "enviar": escolhe o lead, escreve uma mensagem única, controla o ritmo e mede as respostas.
> Você só abre, confere e envia. São uns 10 minutos de trabalho por dia para os 15 contatos.

---

## 1. Antes de começar (uma vez só)

### WhatsApp
- [ ] **Use um número só para prospecção.** Não use o (48) 99208-6832, que é o suporte dos clientes: se o número de prospecção levar um bloqueio, o suporte continua no ar.
- [ ] Instale o **WhatsApp Business** nesse número e complete o perfil: foto (logo Epiverso), nome no formato "Ana · Epiverso", categoria *Software*, descrição ("Painel fiscal para escritórios contábeis"), site e horário. Perfil completo passa confiança e reduz denúncia.
- [ ] **Chip novo? Aqueça por 2 semanas** antes de prospectar: converse com 10 a 20 pessoas conhecidas, receba mensagens, mande áudios, entre em 1 ou 2 grupos. Depois comece com 5 por dia na 1ª semana, 10 na 2ª e 15 a partir da 3ª (ajuste a meta em *Configurações*).
- [ ] Abra o `whatsapp/painel_whatsapp.html` no Chrome ou Edge e coloque **seu nome** em *Configurações*.

### E-mail
- [ ] **Use um domínio separado para prospecção**, parecido com o principal (ex.: `epiversofiscal.com.br` ou `useepiverso.com.br`). Se a reputação dele cair, o e-mail principal da empresa (notas, suporte, cobrança) não é afetado. Redirecione o site desse domínio para o site principal.
- [ ] Crie a caixa (Google Workspace, Zoho ou Microsoft 365) com nome de pessoa: `ana@epiversofiscal.com.br`. Nunca `contato@` ou `comercial@`.
- [ ] **Configure SPF, DKIM e DMARC** no DNS do domínio (no Registro.br ou onde estiver o DNS). Sem isso, Gmail e Outlook mandam para o spam.

  | Registro | Nome | Valor (Google Workspace) |
  |---|---|---|
  | TXT | `@` | `v=spf1 include:_spf.google.com ~all` |
  | TXT | `google._domainkey` | gerado em *Admin > Apps > Google Workspace > Gmail > Autenticar e-mail* |
  | TXT | `_dmarc` | `v=DMARC1; p=none; rua=mailto:ana@epiversofiscal.com.br` |

  Na Zoho, o SPF é `v=spf1 include:zoho.com ~all` e o DKIM sai do painel da Zoho. Depois de 3 a 4 semanas sem problema, troque o DMARC para `p=quarantine`.
- [ ] Confira tudo em [mxtoolbox.com](https://mxtoolbox.com) (SPF, DKIM e DMARC verdes).
- [ ] **Senha de app:** no Gmail/Workspace, ative a verificação em 2 etapas e crie uma senha de app em *Conta Google > Segurança > Senhas de app*. É ela que vai no envio, não a sua senha normal.
- [ ] Instale o Python 3.9 ou mais novo ([python.org](https://www.python.org/downloads/); no Windows, marque "Add Python to PATH"). Não precisa instalar mais nada.
- [ ] Na pasta `email/`, copie `config_exemplo.ini` para `config.ini` e preencha.
- [ ] Guarde a senha numa variável de ambiente (mais seguro que no arquivo):
  - Windows: `setx EPIVERSO_SMTP_SENHA "sua-senha-de-app"` (feche e abra o terminal depois)
  - Mac/Linux: `export EPIVERSO_SMTP_SENHA="sua-senha-de-app"` (coloque no `~/.zshrc` ou `~/.bashrc`)
- [ ] **Teste de spam:** abra [mail-tester.com](https://www.mail-tester.com), copie o endereço que ele mostra e rode
  `python enviar_emails.py teste endereco@srv1.mail-tester.com`. Só comece com nota **9/10 ou mais**.
- [ ] Mande também um teste para um Gmail e um Outlook seus e veja se chegou na **caixa de entrada** (não em Promoções nem Spam).

### Leads
- [ ] Monte a planilha `leads.csv` na pasta `prospeccao/` (modelo: `leads_exemplo.csv`). No Excel: *Salvar como > CSV (separado por ponto e vírgula)*.
  Colunas: `nome; escritorio; whatsapp; email; cidade; uf; dor; origem; obs`. A coluna `dor` aceita *NFC-e, NFS-e, não contribuinte, SEFAZ* ou *geral* (vazio = sorteia).
- [ ] Importe a mesma planilha no painel do WhatsApp (aba *Leads*). O `leads.csv`, o `config.ini` e o histórico de envios **não vão para o GitHub** (estão no `.gitignore`).

---

## 2. Rotina diária (segunda a sexta)

| Quando | O quê | Tempo |
|---|---|---|
| 8h30 | Rodar `python enviar_emails.py enviar` (ou deixar agendado, veja a seção 4) | 0 min |
| 9h às 11h | WhatsApp: **bloco 1**, 5 aberturas/follow-ups | 4 min |
| 13h30 às 15h | WhatsApp: **bloco 2**, 5 envios | 4 min |
| 16h às 17h30 | WhatsApp: **bloco 3**, 5 envios | 4 min |
| O dia todo | **Responder quem respondeu**, rápido (aba *Respostas prontas*) | o que precisar |
| Fim do dia | Marcar no painel quem respondeu; `python enviar_emails.py status` | 2 min |

Evite os dias perto do dia 20 (vencimento do DAS) e os primeiros dias úteis do mês (fechamento): o contador está sem tempo e a taxa de resposta despenca.

---

## 3. Painel do WhatsApp

1. **Fila de hoje** mostra um lead por vez: nome, escritório, cidade, a dor escolhida e a mensagem já escrita.
   - **🔄 Outra variação** sorteia outra combinação. Pode editar o texto à vontade antes de abrir.
   - **Abrir no WhatsApp** abre a conversa com o texto pronto (WhatsApp Web, app do computador ou celular, você escolhe em *Configurações*).
   - Confira, aperte enviar no WhatsApp, volte e clique **✓ Enviei**.
   - O painel trava o próximo envio por **4 a 9 minutos (sorteado)**. É o ritmo de uma pessoa, e é o que mais protege o número. Use esse tempo para responder conversas.
2. **Follow-up:** quem não respondeu em 3 dias úteis volta para a fila **uma única vez**, com uma mensagem curta. Depois disso o lead sai da fila: insistir é o que gera denúncia.
3. **Aguardando resposta:** marque *Respondeu*, *Demo* ou *Parar*. A taxa de resposta aparece no topo e o painel avisa se ela cair abaixo de 10%.
4. **Leads:** importar CSV (vírgula ou ponto e vírgula; números repetidos são ignorados), mudar status, exportar e **fazer backup**. Os dados ficam só no navegador desse computador: faça backup toda semana.
5. **Respostas prontas:** textos para "quanto custa?", "já temos sistema", "manda material", "não tenho interesse" e outras. Digite o nome do contato e copie.

### Modo "olá + áudio"
No card, troque **Texto** por **Olá + áudio**:
1. **Passo 1:** o painel escreve só o olá ("Oi, Marcos, tudo bem?"). Abra e envie.
2. **Passo 2:** espere de 20 segundos a 1 minuto e **grave o áudio na hora, no mesmo chat**, usando o roteiro da tela como guia (30 a 45 s, falando o nome da pessoa).

Dicas para o áudio:
- Grave em lugar silencioso, em pé e sorrindo (muda o tom de voz). Fale como numa ligação, não leia palavra por palavra.
- **Nunca encaminhe um áudio pronto:** aparece "Encaminhada" e fica com cara de disparo. Também não mande arquivo de áudio pelo computador: chega como arquivo, não como mensagem de voz.
- Áudio tem mais resposta, mas pesa mais para quem não te conhece. Funciona melhor com escritórios pequenos e médios. Se quiser ser mais cuidadoso, mande o olá e grave o áudio **só quando a pessoa responder**.
- Quer deixar o áudio como padrão? *Configurações > Modo padrão da abertura > Olá + áudio*.

---

## 4. Envio de e-mail

Na pasta `email/`:

```bash
python enviar_emails.py previa          # mostra os e-mails de hoje, sem enviar (use sempre antes)
python enviar_emails.py enviar          # envia o lote de hoje, com 1,5 a 4 min entre um e outro
python enviar_emails.py status          # resumo: enviados, respostas, devolvidos
python enviar_emails.py verificar       # lê a caixa de entrada e para a sequência de quem respondeu
python enviar_emails.py marcar fulano@escritorio.com.br respondeu   # ou: remover | devolvido | reativar
```

**Como a sequência funciona**

| Etapa | Quando | Conteúdo |
|---|---|---|
| 1 | dia 0 | Abertura focada em uma das 4 dores, terminando em pergunta |
| 2 | +3 dias úteis | Mesma conversa ("Re:"), complementa com as outras dores e a prova (110 mil+ XMLs) |
| 3 | +4 dias úteis | E-mail de despedida curto, deixando a porta aberta |

- **Aquecimento automático:** 10 e-mails/dia na 1ª semana, 20 na 2ª, 30 na 3ª e depois o `limite_diario_max` (40). Os follow-ups contam no limite.
- **Para sozinho** quando o lead responde (lê a caixa por IMAP antes de cada follow-up). Se a resposta tiver "remover", "não tenho interesse" e afins, o e-mail vai para o `descadastrados.txt` e nunca mais recebe nada.
- **E-mail devolvido** (endereço que não existe) sai da lista sozinho.
- No máximo **1 contato novo por domínio de empresa por dia** (3 e-mails no mesmo escritório no mesmo dia parece disparo).
- Só envia de segunda a sexta, das 8h às 18h. Se chegar às 18h no meio do lote, o resto fica para amanhã.
- Pode parar com Ctrl+C a qualquer hora: o que já foi enviado fica registrado em `envios.csv`.

**Agendar para rodar sozinho**
- **Windows** (Agendador de Tarefas > Criar tarefa básica): disparo *Diariamente*, 8h40; ação *Iniciar um programa*: `python`, argumentos `enviar_emails.py enviar`, *Iniciar em*: a pasta `email`. Fim de semana o próprio script não envia.
- **Mac/Linux** (`crontab -e`):
  `40 8 * * 1-5 cd /caminho/prospeccao/email && EPIVERSO_SMTP_SENHA='sua-senha-de-app' python3 enviar_emails.py enviar >> envio.log 2>&1`
  (o cron não lê o `~/.zshrc`, por isso a senha vai na linha ou no `config.ini`).

**Quer mandar mais de 40 por dia?** Não aumente o limite de uma caixa: crie **outra caixa** (ex.: `joao@epiversofiscal.com.br`), copie a pasta `email/` inteira para `email_joao/`, ajuste o `config.ini` e **divida os leads em duas planilhas** (cada pasta guarda o próprio histórico; com a mesma planilha, o mesmo escritório receberia dois e-mails). 2 caixas × 40 = 80 por dia, cada uma aquecida separadamente.

---

## 5. Por que não toma bloqueio no WhatsApp

O WhatsApp não lê sua mensagem para decidir. Ele **mede comportamento**. Os sinais que derrubam um número são:

| Sinal de risco | O que o sistema faz |
|---|---|
| Muitas conversas novas por dia | Meta de 15, com aquecimento para chip novo |
| Ritmo de robô (uma mensagem atrás da outra) | Trava de 4 a 9 min sorteados entre envios, em 3 blocos no dia |
| Texto idêntico para todo mundo | Milhares de combinações por dor (num teste de 6.000 aberturas, praticamente nenhuma se repetiu); o painel não reenvia um texto já usado |
| Conversas sem resposta | Mensagem curta que termina em pergunta fácil ("como vocês fazem hoje?"); resposta é o sinal mais forte de que você não é spam |
| Denúncias e bloqueios | Saída fácil ("se não fizer sentido, me avisa"), 1 follow-up só, nunca no fim de semana ou de noite |
| Link ou arquivo na 1ª mensagem | Nenhuma mensagem de abertura tem link, PDF ou imagem; material só depois da resposta |
| Automação no WhatsApp Web | Nenhuma: quem envia é você, pelo WhatsApp normal |

Outras práticas:
- **Responda rápido.** Conversa com ida e volta aumenta a confiança no número.
- **Peça para salvarem seu contato** quando a conversa engatar ("salva meu número que te mando o acesso").
- **Não crie grupos** nem adicione leads em grupos. Lista de transmissão só chega para quem salvou seu número: não use para prospecção.
- **Se aparecer aviso de atividade incomum ou bloqueio temporário:** pare de 3 a 7 dias e volte com metade do volume.

**Nenhum método zera o risco** (a decisão é sempre do WhatsApp), mas 15 por dia, com mensagens únicas, ritmo humano e boa taxa de resposta, é um padrão que não se parece com disparo.

---

## 6. Por que o e-mail não cai no spam

| Regra | Por quê |
|---|---|
| Domínio separado + SPF, DKIM e DMARC | Gmail e Outlook exigem autenticação; sem ela, spam ou rejeição. O domínio separado protege o principal |
| Aquecimento (10 → 40/dia) | Domínio novo mandando muito de repente é o padrão de spammer |
| Texto puro, sem imagem, sem anexo, sem link | Parece e-mail de pessoa para pessoa (e é). Link e imagem são os maiores gatilhos de filtro |
| Sem rastreio de abertura | O pixel de rastreio é uma imagem escondida, e os filtros detectam |
| Cada e-mail diferente (assunto e corpo sorteados) | Filtros agrupam mensagens idênticas e as tratam como campanha em massa |
| Assunto curto, minúsculo, sem "grátis", "oferta", "R$", "!!!" | São as palavras e formatos que os filtros mais pesam |
| 1,5 a 4 min entre envios, só em horário comercial | Ritmo de pessoa, não de robô |
| Follow-ups na mesma conversa ("Re:") | Mais contexto para quem lê e menos e-mails "novos" saindo |
| Saída fácil ("responda remover") + cabeçalho List-Unsubscribe | Quem pode sair com um clique não aperta "denunciar spam" |
| Para de enviar para quem respondeu e tira os devolvidos | Mandar para endereço inexistente e insistir com quem já respondeu derrubam a reputação |

Acompanhe a reputação no [Google Postmaster Tools](https://postmaster.google.com) (cadastre o domínio de prospecção).
**Nunca compre lista de e-mails:** elas têm endereços-armadilha (spam traps) que queimam o domínio em dias.

---

## 7. Números para acompanhar

| Métrica | Bom | Sinal de alerta | O que fazer |
|---|---|---|---|
| Resposta no WhatsApp | 20% a 35% | abaixo de 10% | revisar lista e mensagens; reduzir volume |
| Pediram para parar (WhatsApp) | abaixo de 3% | acima de 5% | menos volume, mais "olá + áudio", lista mais qualificada |
| Resposta no e-mail | 3% a 8% | abaixo de 1% | provavelmente caindo no spam: rodar o mail-tester de novo |
| E-mails devolvidos | abaixo de 2% | acima de 3% | limpar a lista antes de continuar |
| Denúncia de spam (Postmaster) | abaixo de 0,1% | acima de 0,3% | parar e revisar (0,3% é o limite do Gmail) |

Teste as dores: depois de 2 ou 3 semanas, exporte o CSV do painel e veja qual dor (`dor`) teve mais resposta. Use mais essa.

---

## 8. LGPD
- Prospecção B2B para o contato profissional do escritório se apoia no **legítimo interesse** (art. 7º, IX). Use só dados públicos (site, Google, redes do escritório) e anote de onde veio na coluna `origem`.
- Sempre se identifique (nome + Epiverso), ofereça a saída e **atenda o pedido de saída na hora** (no painel: *Não chamar*; no e-mail: automático, ou `marcar ... remover`).
- Não use lista comprada nem dado pessoal que não seja do contexto profissional.

---

## 9. Onde achar escritórios
- **Google Maps:** "escritório de contabilidade" + cidade. Tem telefone, site e, no site, o e-mail. Comece pela sua região: dá para citar a cidade.
- **Site do escritório:** e-mail do sócio ou do fiscal costuma estar em "Equipe" ou "Contato".
- **Instagram e LinkedIn:** escritórios que postam sobre fiscal, reforma tributária e XML são os mais propensos.
- **CRC do estado** (consulta cadastral) e listas de associados do **Sescon** e de associações comerciais.
- Preencha a coluna `dor` quando souber o perfil: escritório com muitos clientes de **comércio → NFC-e**; de **serviços → NFS-e**; com muito **prestador sem IE → não contribuinte**.

---

## 10. Editar as mensagens
- WhatsApp: `whatsapp/mensagens_whatsapp.js`. E-mail: `email/mensagens_email.json`.
- `{nome}`, `{escritorio}`, `{cidade}`, `{seu_nome}`... viram os dados do lead. `[opção 1|opção 2|opção 3]` sorteia uma a cada mensagem.
- Se uma frase usa um campo que o lead não tem, ela é descartada e outra é sorteada. Por isso, mantenha sempre opções sem campos.
- Não escreva "o {escritorio}" ou "no {escritorio}": não dá para saber se o nome é masculino ou feminino.
- Depois de editar: no painel, *Configurações > Gerar exemplos*; no e-mail, `python enviar_emails.py previa`.
- Os números do follow-up de e-mail (**110 mil+ XMLs**) vêm do kit do Instagram. Confirme que quer divulgar antes de usar, ou edite em `followup_1`.
