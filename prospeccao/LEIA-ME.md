# Epiverso · Prospecção (WhatsApp + E-mail)

Sistema local para prospectar escritórios contábeis: WhatsApp conectado por **QR Code** e e-mail,
com painel no navegador para mudar mensagens, cadastrar leads, gravar áudios e configurar tudo.

## Para usar

Baixe **[`epiverso_prospeccao.zip`](../epiverso_prospeccao.zip)** (1,4 MB), descompacte e siga o `LEIA-ME.txt` que vem dentro.
Resumo: instale o [Node.js LTS](https://nodejs.org/pt-br/download), dê dois cliques em `INICIAR (Windows).bat`
(ou `INICIAR (Mac).command`) e o painel abre em `http://localhost:3210`.

Não precisa de `npm install` nem de navegador escondido: o sistema inteiro é um arquivo de ~5 MB.

## O que ele faz

| | WhatsApp | E-mail |
|---|---|---|
| Conexão | QR Code ou código pelo número (Baileys, sem Chromium) | SMTP + IMAP do seu provedor |
| Volume | até 15/dia (configurável), só dias úteis e horário comercial | aquecimento 10 → 20 → 30 → 40/dia |
| Ritmo | espalhado pelo dia, "digitando…" e "gravando áudio…" antes de enviar | intervalo aleatório, espalhado pelo dia |
| Mensagem | sorteada de milhares de combinações, focada na dor do lead (NFC-e, NFS-e, não contribuintes, SEFAZ) | assunto e corpo sorteados, texto puro, sem link |
| Abertura | texto ou **olá + áudio** (o áudio vai como mensagem de voz, gravado no painel) | sequência de 3 na mesma conversa ("Re:") |
| Respostas | detecta na hora, para a sequência, avisa no painel, responde pelo painel | lê a caixa de entrada e para quem respondeu |
| Saída | "remover", "não tenho interesse"… tira o lead de todas as listas | descadastro em todo e-mail + cabeçalho List-Unsubscribe |

## Desenvolvimento

```bash
cd prospeccao
npm install
npm run dev     # sobe o servidor em http://localhost:3210 usando src/
npm test        # ponta a ponta: WhatsApp simulado, SMTP e IMAP locais (15 cenários)
npm run build   # gera ../epiverso_prospeccao.zip (esbuild: um arquivo só)
```

```
prospeccao/
├── src/
│   ├── servidor.mjs          servidor HTTP local + API do painel
│   ├── whatsapp.mjs          conexão (QR/código), envio com ritmo humano, respostas recebidas
│   ├── email.mjs             sequência de e-mails, aquecimento, verificação por IMAP
│   ├── imap.mjs              cliente IMAP mínimo (só busca)
│   ├── audio.mjs             WebM/Opus do navegador → Ogg/Opus (mensagem de voz), sem ffmpeg
│   ├── dados.mjs             arquivos JSON em dados/, horários e regras de lead
│   └── mensagens_padrao.mjs  todas as variações de mensagem padrão
├── painel/                   index.html, app.js, estilo.css e motor.mjs (motor de variações, usado também no servidor)
├── testes/rodar.mjs          teste de ponta a ponta
├── build.mjs                 empacotamento do zip
└── LEIA-ME.txt               guia que vai dentro do zip
```
