// Teste de ponta a ponta: sobe o sistema com um WhatsApp simulado, um servidor SMTP e um IMAP
// locais, e usa a API HTTP como o painel usa. Rode com: npm test
import net from 'node:net';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { EventEmitter } from 'node:events';
import assert from 'node:assert/strict';

const PASTA = fs.mkdtempSync(path.join(os.tmpdir(), 'epiverso-teste-'));
Object.assign(process.env, { EPIVERSO_DADOS: PASTA, EPIVERSO_PORTA: '3290', EPIVERSO_SEM_NAVEGADOR: '1', EPIVERSO_ESCALA_TEMPO: '0.0005',
  EPIVERSO_IMAP_SEM_TLS: '1', EPIVERSO_TESTE_JANELA_ABERTA: '1' });
const BASE = 'http://127.0.0.1:3290';
let falhas = 0;
async function etapa(nome, fn) {
  try { await fn(); console.log('  ✓', nome); }
  catch (e) { falhas++; console.log('  ✗', nome, '\n    ', e.message); }
}
const api = async (metodo, url, dados, headers = {}) => {
  const r = await fetch(BASE + url, { method: metodo, headers: { 'x-epiverso': '1', ...(dados && !(dados instanceof Buffer) ? { 'Content-Type': 'application/json' } : {}), ...headers },
    body: dados instanceof Buffer ? dados : dados ? JSON.stringify(dados) : undefined });
  const c = (r.headers.get('content-type') || '').includes('json') ? await r.json() : await r.text();
  if (!r.ok) throw new Error(`${metodo} ${url} → ${r.status} ${JSON.stringify(c)}`);
  return c;
};
async function ate(cond, ms = 15000, oQue = 'condição') {
  const fim = Date.now() + ms;
  while (Date.now() < fim) { const v = await cond(); if (v) return v; await new Promise(r => setTimeout(r, 100)); }
  throw new Error('tempo esgotado esperando ' + oQue);
}

// ------------------------------------------------------------------ WhatsApp simulado
const zap = { enviados: [], presencas: [], lids: {} };
function socketFalso() {
  const ev = new EventEmitter();
  const s = {
    ev: { on: (n, f) => ev.on(n, f) }, user: null,
    async onWhatsApp(n) { return String(n).endsWith('0000') ? [] : [{ jid: n + '@s.whatsapp.net', exists: true }]; },
    async sendMessage(jid, c) { zap.enviados.push({ jid, c }); return { key: { id: 'm' + zap.enviados.length }, message: {} }; },
    async sendPresenceUpdate(p) { zap.presencas.push(p); }, async presenceSubscribe() {},
    async requestPairingCode() { return 'ABCD1234'; },
    async logout() { setTimeout(() => ev.emit('connection.update', { connection: 'close', lastDisconnect: { error: { output: { statusCode: 401 } } } }), 10); },
    end() {}, signalRepository: { lidMapping: { getPNForLID: async lid => zap.lids[lid] } }
  };
  setTimeout(() => ev.emit('connection.update', { qr: '2@codigo-de-teste,abc,def' }), 30);
  zap.escanear = () => { s.user = { id: '5548999990099:3@s.whatsapp.net', name: 'Prospecção' }; ev.emit('connection.update', { connection: 'open' }); };
  zap.receber = (jid, texto, chave = {}) => ev.emit('messages.upsert', { type: 'notify', messages: [{ key: { remoteJid: jid, fromMe: false, ...chave }, message: { conversation: texto } }] });
  return s;
}

// ------------------------------------------------------------------ SMTP e IMAP locais
const caixaSmtp = [];
net.createServer(c => {
  let buf = '', dados = false, login = 0;
  c.write('220 teste ESMTP\r\n');
  c.on('data', d => {
    buf += d.toString('utf8');
    for (;;) {
      if (dados) { const f = buf.indexOf('\r\n.\r\n'); if (f < 0) return; caixaSmtp.push(buf.slice(0, f)); buf = buf.slice(f + 5); dados = false; c.write('250 ok\r\n'); continue; }
      const i = buf.indexOf('\r\n'); if (i < 0) return;
      const l = buf.slice(0, i); buf = buf.slice(i + 2); const u = l.toUpperCase();
      if (login) { c.write(login++ === 1 ? '334 UGFzc3dvcmQ6\r\n' : '235 ok\r\n'); if (login > 2) login = 0; continue; }
      if (u.startsWith('EHLO')) c.write('250-teste\r\n250-AUTH PLAIN LOGIN\r\n250 8BITMIME\r\n');
      else if (u.startsWith('AUTH PLAIN')) c.write('235 ok\r\n');
      else if (u.startsWith('AUTH LOGIN')) { login = 1; c.write('334 VXNlcm5hbWU6\r\n'); }
      else if (u.startsWith('RCPT')) c.write(/recusa/i.test(l) ? '550 5.1.1 usuario inexistente\r\n' : '250 ok\r\n');
      else if (u.startsWith('DATA')) { dados = true; c.write('354 manda\r\n'); }
      else if (u.startsWith('QUIT')) { c.write('221 tchau\r\n'); c.end(); }
      else c.write('250 ok\r\n');
    }
  });
}).listen(2526, '127.0.0.1');
const imapComandos = [], imapResponderam = new Set();
net.createServer(c => {
  let buf = '';
  c.write('* OK IMAP de teste\r\n');
  c.on('data', d => {
    buf += d.toString('utf8'); let i;
    while ((i = buf.indexOf('\r\n')) >= 0) {
      const l = buf.slice(0, i); buf = buf.slice(i + 2); imapComandos.push(l);
      const [tag, cmd] = l.split(' ');
      if (cmd === 'SEARCH') {
        const de = (l.match(/FROM "([^"]+@[^"]+)"/) || [])[1];
        c.write(`* SEARCH${!l.includes('mailer-daemon') && imapResponderam.has(de) ? ' 7' : ''}\r\n${tag} OK SEARCH completed\r\n`);
      } else if (cmd === 'LOGOUT') { c.write(`* BYE\r\n${tag} OK\r\n`); c.end(); }
      else c.write(`${tag} OK\r\n`);
    }
  });
}).listen(2143, '127.0.0.1');

// ------------------------------------------------------------------ sobe o sistema
const W = await import('../src/whatsapp.mjs');
W._usarSocketDeTeste(socketFalso);
await import('../src/servidor.mjs');
await ate(async () => (await api('GET', '/api/ping').catch(() => null))?.app, 5000, 'servidor');
const D = await import('../src/dados.mjs');
console.log('\nTestes (dados em ' + PASTA + ')');

await etapa('configurações salvas (e a senha nunca volta para o painel)', async () => {
  const c = await api('PUT', '/api/config', { seuNome: 'Ana', empresa: 'Epiverso', pausaAlmoco: false, espalhar: false, waIntervaloMin: 1, waIntervaloMax: 2,
    waMeta: 4, waModo: 'texto', diasEntreCanais: 0, emEmail: 'ana@epiversofiscal.com.br', smtpHost: '127.0.0.1', smtpPorta: 2526, smtpSenha: 'segredo',
    imapAtivo: true, imapHost: '127.0.0.1', imapPorta: 2143, emIntervaloMin: 1, emIntervaloMax: 2, horaFim: 'abc' });
  assert.equal(c.seuNome, 'Ana'); assert.equal(c.temSenha, true); assert.equal(c.smtpSenha, undefined); assert.equal(c.horaFim, 18);
  await api('PUT', '/api/config', { smtpSenha: '' });
  assert.equal(D.db.config.smtpSenha, 'segredo', 'senha vazia deve manter a salva');
});

await etapa('importa planilha: válidos, repetidos e inválidos', async () => {
  const csv = 'nome;escritorio;whatsapp;email;cidade;dor\n' +
    'Marcos Silva;Contabilidade Exemplo Ltda;(48) 99999-0001;marcos@exemplo.com.br;Joinville;NFC-e\n' +
    'Dra. Ana Souza;Souza Contábil;47 98888-0002;;;NFS-e\n' +
    'Sem Zap;Zap Contabilidade;(51) 97777-0000;semzap@zapcontab.com.br;;\n' +
    'Recusa;Recusa Ltda;;recusa@recusado.com.br;;sefaz\n' +
    'Carla;Carla Contábil;(11) 96666-0005;carla@carla.com.br;;geral\n' +
    'Marcos de novo;;48999990001;;;\n' +
    'Ninguém;;;email-invalido;;\n';
  const r = await api('POST', '/api/leads/importar', { texto: csv });
  assert.deepEqual(r, { novos: 5, repetidos: 1, invalidos: 1 });
  const leads = await api('GET', '/api/leads');
  assert.equal(leads.find(l => l.nome === 'Marcos Silva').whatsapp, '5548999990001');
  assert.equal(leads.find(l => l.nome === 'Recusa').dor, 'sefaz');
});

await etapa('cadastro manual valida número e e-mail', async () => {
  await assert.rejects(api('POST', '/api/leads', { nome: 'X', whatsapp: '123' }), /inválido/);
  await assert.rejects(api('POST', '/api/leads', { nome: 'X' }), /pelo menos/);
  await assert.rejects(api('POST', '/api/leads', { nome: 'X', email: 'marcos@exemplo.com.br' }), /Já existe/);
});

const ID = async nome => (await api('GET', '/api/leads')).find(l => l.nome === nome).id;
await etapa('áudio gravado no navegador (WebM) vira mensagem de voz (Ogg/Opus)', async () => {
  const webm = path.join(path.dirname(new URL(import.meta.url).pathname), 'amostra.webm');
  const a = await api('POST', '/api/audios', fs.readFileSync(webm), { 'x-nome': encodeURIComponent('Geral 1'), 'x-dor': 'geral', 'x-waveform': Buffer.from([0, 50, 100]).toString('base64') });
  assert.ok(a.segundos >= 3 && a.segundos <= 5, 'duração ' + a.segundos);
  const ogg = fs.readFileSync(path.join(PASTA, 'audios', a.arquivo));
  assert.equal(ogg.subarray(0, 4).toString(), 'OggS'); assert.ok(ogg.includes(Buffer.from('OpusHead')));
  await assert.rejects(api('POST', '/api/audios', Buffer.from('ID3 isto é um mp3')), /Formato não aceito/);
});

await etapa('conectar: mostra o QR Code e gera código por número', async () => {
  await api('POST', '/api/whatsapp/conectar');
  const e = await ate(async () => { const s = await api('GET', '/api/estado'); return s.whatsapp.status === 'qr' && s; }, 15000, 'QR');
  assert.match(e.whatsapp.qrSvg, /^<svg/);
  const { codigo } = await api('POST', '/api/whatsapp/codigo', { numero: '48 99999-0099' });
  assert.equal(codigo, 'ABCD-1234');
  zap.escanear();
  const c = await ate(async () => { const s = await api('GET', '/api/estado'); return s.whatsapp.status === 'conectado' && s; }, 5000, 'conectado');
  assert.equal(c.whatsapp.numero, '5548999990099');
});

await etapa('envios de WhatsApp: texto, olá + áudio e número sem WhatsApp', async () => {
  await api('PUT', '/api/leads/' + await ID('Marcos Silva'), { modo: 'texto' });
  await api('PUT', '/api/leads/' + await ID('Dra. Ana Souza'), { modo: 'ola_audio' });
  await api('POST', '/api/whatsapp/ligar', { ligado: true });
  await ate(async () => (await api('GET', '/api/estado')).whatsapp.hoje >= 3, 30000, '3 envios de WhatsApp');
  const paraMarcos = zap.enviados.filter(x => x.jid === '5548999990001@s.whatsapp.net');
  assert.equal(paraMarcos.length, 1); assert.match(paraMarcos[0].c.text, /Ana/);
  const paraAna = zap.enviados.filter(x => x.jid === '5547988880002@s.whatsapp.net');
  assert.equal(paraAna.length, 2, 'olá + áudio');
  assert.ok(paraAna[0].c.text.length < 200, 'olá curto');
  assert.equal(paraAna[1].c.ptt, true); assert.equal(paraAna[1].c.mimetype, 'audio/ogg; codecs=opus'); assert.ok(paraAna[1].c.waveform instanceof Uint8Array);
  assert.ok(zap.presencas.includes('composing') && zap.presencas.includes('recording'));
  const semZap = (await api('GET', '/api/leads')).find(l => l.nome === 'Sem Zap');
  assert.equal(semZap.wa.estado, 'sem_whatsapp');
  assert.ok(!zap.enviados.some(x => x.jid.startsWith('5551977770000')));
});

await etapa('e-mails: sequência, assinatura, descadastro e endereço recusado', async () => {
  await api('POST', '/api/email/ligar', { ligado: true });
  await ate(async () => (await api('GET', '/api/estado')).email.hoje >= 3, 30000, '3 e-mails');
  const m = caixaSmtp.find(x => /To: .*marcos@exemplo\.com\.br/i.test(x));
  assert.ok(m, 'e-mail para Marcos'); assert.match(m, /List-Unsubscribe: <mailto:ana@epiversofiscal\.com\.br\?subject=remover>/);
  assert.match(m, /From: Ana <ana@epiversofiscal\.com\.br>/); assert.doesNotMatch(m, /<img|https?:\/\//i);
  const recusa = (await api('GET', '/api/leads')).find(l => l.nome === 'Recusa');
  await ate(async () => (await api('GET', '/api/leads')).find(l => l.nome === 'Recusa').em.estado === 'devolvido', 10000, 'devolvido');
  assert.ok(recusa);
});

await etapa('resposta no WhatsApp (contato com privacidade @lid) para a sequência', async () => {
  zap.receber('99887766@lid', 'Oi! Quanto custa?', { remoteJidAlt: '5547988880002@s.whatsapp.net' });
  const l = await ate(async () => (await api('GET', '/api/leads')).find(x => x.nome === 'Dra. Ana Souza' && x.status === 'respondeu'), 3000, 'respondeu');
  assert.equal(l.naoLida, true); assert.equal(l.wa.lid, '99887766@lid');
  const e = await api('GET', '/api/estado');
  assert.equal(e.naoLidas, 1); assert.match(e.conversas[0].resposta.texto, /Quanto custa/);
});

await etapa('pedido para sair tira o lead de todas as listas', async () => {
  zap.receber('5548999990001@s.whatsapp.net', 'Por favor, me remova da lista');
  await ate(async () => (await api('GET', '/api/leads')).find(x => x.nome === 'Marcos Silva').status === 'sem_interesse', 3000, 'sem_interesse');
});

await etapa('responder pelo painel vai para o contato certo', async () => {
  await api('POST', `/api/leads/${await ID('Dra. Ana Souza')}/responder`, { texto: 'Depende do volume, Ana!' });
  assert.equal(zap.enviados.at(-1).jid, '99887766@lid'); assert.equal(zap.enviados.at(-1).c.text, 'Depende do volume, Ana!');
});

await etapa('resposta por e-mail detectada pela caixa de entrada (IMAP)', async () => {
  imapResponderam.add('semzap@zapcontab.com.br');
  const r = await api('POST', '/api/email/verificar');
  assert.match(r.msg, /1 resposta/);
  assert.equal((await api('GET', '/api/leads')).find(x => x.nome === 'Sem Zap').status, 'respondeu');
  assert.ok(imapComandos.some(c => /SEARCH SINCE \d+-\w{3}-\d{4} FROM "semzap@zapcontab\.com\.br"/.test(c)));
});

await etapa('follow-ups: 1 no WhatsApp e o 2º e-mail na mesma conversa ("Re:")', async () => {
  const carla = D.db.leads.find(l => l.nome === 'Carla');
  const antes = new Date(Date.now() - 9 * 86400e3).toISOString();
  for (const l of D.db.leads) for (const h of l.historico) h.em = antes; // "envios de semanas atrás"
  carla.wa.aberturaEm = antes; carla.em.ultimoEnvio = antes;
  const n = zap.enviados.length;
  await ate(() => carla.wa.estado === 'followup' && carla.em.etapa === 2, 30000, 'follow-ups da Carla');
  assert.equal(zap.enviados.length, n + 1);
  const re = caixaSmtp.filter(x => /To: .*carla@carla\.com\.br/i.test(x));
  assert.equal(re.length, 2); assert.match(re[1], /Subject: (Re: |=\?UTF-8\?Q\?Re=3A_)/); assert.match(re[1], /In-Reply-To: </);
  assert.ok(!zap.enviados.slice(n).some(x => x.jid.includes('5548999990001')), 'quem saiu não recebe follow-up');
});

await etapa('mensagens: salvar, validar e restaurar padrão', async () => {
  const m = await api('GET', '/api/mensagens');
  m.whatsapp.saudacoes = ['Olá, {nome}!', '  '];
  const s = await api('PUT', '/api/mensagens', m);
  assert.deepEqual(s.whatsapp.saudacoes, ['Olá, {nome}!']);
  await assert.rejects(api('PUT', '/api/mensagens', { whatsapp: 3 }), /inválido/);
  const p = await api('POST', '/api/mensagens/restaurar');
  assert.ok(p.whatsapp.saudacoes.length > 3);
});

await etapa('exportar CSV e painel servindo os arquivos', async () => {
  const csv = await api('GET', '/api/leads/exportar');
  assert.match(csv, /nome;escritorio;whatsapp/); assert.match(csv, /Carla/);
  assert.match(await api('GET', '/'), /Epiverso · Prospecção/);
  assert.match(await api('GET', '/motor.mjs'), /export function spin/);
  await assert.rejects(api('GET', '/../src/servidor.mjs'), /404/);
});

await etapa('bloqueia pedidos de outros sites (CSRF) e de outros hosts', async () => {
  const semCabecalho = await fetch(BASE + '/api/email/ligar', { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: '{"ligado":false}' });
  assert.equal(semCabecalho.status, 403);
  const outraOrigem = await fetch(BASE + '/api/email/ligar', { method: 'POST', headers: { 'x-epiverso': '1', Origin: 'https://site-malicioso.com' }, body: '{}' });
  assert.equal(outraOrigem.status, 403);
  const http = await import('node:http'); // fetch não deixa trocar o Host
  const outroHost = await new Promise(r => http.get({ host: '127.0.0.1', port: 3290, path: '/api/leads', headers: { Host: 'malicioso.com:3290' } }, res => { res.resume(); r(res.statusCode); }));
  assert.equal(outroHost, 403);
  assert.equal(D.db.config.emLigado, true, 'nada mudou');
});

await etapa('desconectar remove a sessão do WhatsApp', async () => {
  assert.ok(fs.existsSync(path.join(PASTA, 'sessao-whatsapp')));
  await api('POST', '/api/whatsapp/desconectar');
  await ate(async () => (await api('GET', '/api/estado')).whatsapp.status === 'desconectado', 3000, 'desconectado');
  assert.ok(!fs.existsSync(path.join(PASTA, 'sessao-whatsapp', 'creds.json')));
});

console.log(falhas ? `\n${falhas} teste(s) falharam.` : '\nTudo certo.');
if (process.env.EPIVERSO_TESTE_MANTER) { console.log('Servidor de teste mantido em', BASE); }
else { fs.rmSync(PASTA, { recursive: true, force: true }); process.exit(falhas ? 1 : 0); }
