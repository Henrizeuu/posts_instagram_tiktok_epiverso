// Epiverso Prospecção: servidor local. Abre o painel em http://localhost:3210 (só neste computador).
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { exec } from 'node:child_process';

const MAIOR = Number(process.versions.node.split('.')[0]);
if (MAIOR < 20) {
  console.error(`\n  Este sistema precisa do Node.js 20 ou mais novo (você tem o ${process.versions.node}).\n  Baixe a versão LTS em https://nodejs.org e rode de novo.\n`);
  process.exit(1);
}

const { db, salvar, registrar, restaurarMensagens, mesclarMensagens, CONFIG_PADRAO, PASTA_PAINEL, PASTA_DADOS, PASTA_AUDIOS,
  enviosHoje, novoLead, hojeISO } = await import('./dados.mjs');
const { lerCSV, normalizarFone, tipoFone, normalizarDor, EMAIL_OK, ANGULOS, foneBonito } = await import('../painel/motor.mjs');
const W = await import('./whatsapp.mjs');
const EM = await import('./email.mjs');
const { webmParaOgg, duracaoOgg, ehOgg, ehWebm } = await import('./audio.mjs');

const PORTA = Number(process.env.EPIVERSO_PORTA || 3210);
const TIPOS = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.ico': 'image/x-icon', '.ogg': 'audio/ogg' };
const STATUS = ['novo', 'em_contato', 'respondeu', 'reuniao', 'cliente', 'sem_interesse', 'pausado'];

process.on('unhandledRejection', e => console.error('[erro]', e?.message || e));
process.on('uncaughtException', e => console.error('[erro]', e?.message || e));

// ------------------------------------------------------------------ utilitários HTTP
function corpo(req, limite = 20 * 1024 * 1024) {
  return new Promise((resolve, reject) => {
    const partes = []; let total = 0;
    req.on('data', d => { total += d.length; if (total > limite) { reject(new Erro(413, 'Arquivo grande demais.')); req.destroy(); } else partes.push(d); });
    req.on('end', () => resolve(Buffer.concat(partes)));
    req.on('error', reject);
  });
}
async function json(req) { const b = await corpo(req, 5 * 1024 * 1024); try { return b.length ? JSON.parse(b.toString('utf8')) : {}; } catch { throw new Erro(400, 'JSON inválido'); } }
class Erro extends Error { constructor(status, msg) { super(msg); this.status = status; } }
function responder(res, status, dados, tipo = 'application/json; charset=utf-8') {
  res.writeHead(status, { 'Content-Type': tipo, 'Cache-Control': 'no-store' });
  res.end(typeof dados === 'string' || Buffer.isBuffer(dados) ? dados : JSON.stringify(dados));
}

// ------------------------------------------------------------------ leads
function leve(l) {
  const { historico, ...resto } = l;
  const ultimo = (historico || []).filter(h => h.envio).at(-1);
  return { ...resto, ultimoEnvio: ultimo ? { em: ultimo.em, canal: ultimo.canal, tipo: ultimo.tipo } : null };
}
function validarLead(o, ignorarId) {
  const whatsapp = o.whatsapp ? normalizarFone(o.whatsapp) : '';
  const email = String(o.email || '').trim().toLowerCase();
  if (whatsapp && tipoFone(whatsapp) === 'invalido') throw new Erro(400, `WhatsApp inválido: ${o.whatsapp}. Use DDD + número.`);
  if (email && !EMAIL_OK.test(email)) throw new Erro(400, `E-mail inválido: ${o.email}`);
  if (!whatsapp && !email) throw new Erro(400, 'Coloque pelo menos o WhatsApp ou o e-mail.');
  const dup = db.leads.find(l => l.id !== ignorarId && ((whatsapp && l.whatsapp === whatsapp) || (email && l.email === email)));
  if (dup) throw new Erro(409, `Já existe: ${dup.nome || dup.escritorio || dup.whatsapp || dup.email}.`);
  return { whatsapp, email };
}
function importar(texto) {
  let novos = 0, repetidos = 0, invalidos = 0;
  for (const o of lerCSV(texto)) {
    try {
      const v = validarLead(o);
      db.leads.push(novoLead({ ...o, ...v, dor: normalizarDor(o.dor) }));
      novos++;
    } catch (e) { e.status === 409 ? repetidos++ : invalidos++; }
  }
  salvar.leads();
  if (novos) registrar('leads', `📋 ${novos} lead(s) importado(s).`);
  return { novos, repetidos, invalidos };
}
function exportarCSV() {
  const cols = ['nome', 'escritorio', 'whatsapp', 'email', 'cidade', 'uf', 'dor', 'status', 'whatsapp_estado', 'email_etapa', 'ultima_resposta', 'origem', 'obs'];
  const c = s => `"${String(s ?? '').replace(/"/g, '""')}"`;
  const linhas = db.leads.map(l => [l.nome, l.escritorio, foneBonito(l.whatsapp), l.email, l.cidade, l.uf, l.dor || l.angulo, l.status,
    l.wa?.estado, l.em?.etapa, l.resposta?.texto, l.origem, l.obs].map(c).join(';'));
  return '﻿' + [cols.join(';'), ...linhas].join('\r\n');
}

// ------------------------------------------------------------------ painel: resumo
function metricas() {
  const r = { leads: db.leads.length, novos: 0, whatsapp: { contatados: 0, respostas: 0 }, email: { contatados: 0, respostas: 0 }, sairam: 0, reunioes: 0 };
  for (const l of db.leads) {
    if (l.status === 'novo') r.novos++;
    if (l.status === 'sem_interesse') r.sairam++;
    if (['reuniao', 'cliente'].includes(l.status)) r.reunioes++;
    for (const canal of ['whatsapp', 'email']) {
      if ((l.historico || []).some(h => h.canal === canal && h.envio)) r[canal].contatados++;
      if ((l.historico || []).some(h => h.canal === canal && h.tipo === 'recebida')) r[canal].respostas++;
    }
  }
  for (const canal of ['whatsapp', 'email']) r[canal].taxa = r[canal].contatados ? Math.round(100 * r[canal].respostas / r[canal].contatados) : 0;
  return r;
}
function estado() {
  const cfg = db.config;
  const conversas = db.leads.filter(l => l.resposta).sort((a, b) => b.resposta.em.localeCompare(a.resposta.em)).slice(0, 30)
    .map(l => ({ id: l.id, nome: l.nome, escritorio: l.escritorio, status: l.status, naoLida: !!l.naoLida, resposta: l.resposta, temWhatsapp: !!l.whatsapp }));
  return {
    whatsapp: { status: W.wa.status, qrSvg: W.wa.qrSvg, codigo: W.wa.codigo, numero: W.wa.numero, nome: W.wa.nome, motivo: W.wa.motivo,
      situacao: W.wa.situacao, ligado: cfg.waLigado, hoje: enviosHoje('whatsapp'), meta: cfg.waMeta, fila: W.filaWhatsApp(cfg).length },
    email: { situacao: EM.estadoEmail.situacao, ligado: cfg.emLigado, hoje: enviosHoje('email'), limite: EM.limiteHoje(cfg), limiteMax: cfg.emLimiteMax,
      fila: EM.filaEmail(cfg).length, falta: EM.faltaConfigurar(cfg) },
    metricas: metricas(), atividade: db.atividade.slice(-60).reverse(), conversas,
    naoLidas: db.leads.filter(l => l.naoLida).length, audios: db.audios.length, seuNome: cfg.seuNome, hoje: hojeISO()
  };
}
function configPublica() {
  const { smtpSenha, ...resto } = db.config;
  return { ...resto, temSenha: !!smtpSenha };
}
function salvarConfig(novo) {
  for (const [k, padrao] of Object.entries(CONFIG_PADRAO)) {
    if (!(k in novo)) continue;
    let v = novo[k];
    if (k === 'smtpSenha' && !v) continue; // vazio = manter a senha salva
    if (typeof padrao === 'number') { v = Number(v); if (!Number.isFinite(v)) continue; }
    else if (typeof padrao === 'boolean') v = v === true || v === 'true' || v === 1;
    else v = String(v ?? '').trim();
    db.config[k] = v;
  }
  if (db.config.waIntervaloMax < db.config.waIntervaloMin) db.config.waIntervaloMax = db.config.waIntervaloMin;
  if (db.config.emIntervaloMax < db.config.emIntervaloMin) db.config.emIntervaloMax = db.config.emIntervaloMin;
  if (db.config.horaFim <= db.config.horaInicio) db.config.horaFim = db.config.horaInicio + 1;
  salvar.config();
}
function validarMensagens(m) {
  const ok = v => typeof v === 'string' || (Array.isArray(v) && v.every(x => typeof x === 'string')) ||
    (v && typeof v === 'object' && Object.values(v).every(ok));
  if (!m || typeof m !== 'object' || !ok(m.whatsapp) || !ok(m.email)) throw new Erro(400, 'Formato de mensagens inválido.');
  if (!Array.isArray(m.respostas) || !m.respostas.every(r => typeof r?.titulo === 'string' && typeof r?.texto === 'string')) throw new Erro(400, 'Respostas prontas inválidas.');
  const limparLista = v => Array.isArray(v) ? v.map(s => s.trim()).filter(Boolean) : typeof v === 'string' ? v : Object.fromEntries(Object.entries(v).map(([k, x]) => [k, limparLista(x)]));
  return mesclarMensagens({ whatsapp: limparLista(m.whatsapp), email: limparLista(m.email), respostas: m.respostas.filter(r => r.titulo.trim() || r.texto.trim()) });
}

// ------------------------------------------------------------------ rotas
const rotas = {
  'GET /api/ping': () => ({ app: 'epiverso-prospeccao' }),
  'GET /api/estado': () => estado(),
  'GET /api/config': () => configPublica(),
  'PUT /api/config': async req => { salvarConfig(await json(req)); return configPublica(); },

  'GET /api/mensagens': () => db.mensagens,
  'PUT /api/mensagens': async req => { db.mensagens = validarMensagens(await json(req)); salvar.mensagens(); registrar('config', '✏️ Mensagens salvas.'); return db.mensagens; },
  'POST /api/mensagens/restaurar': () => { restaurarMensagens(); registrar('config', '↺ Mensagens restauradas para o padrão.'); return db.mensagens; },

  'GET /api/leads': () => db.leads.map(leve),
  'POST /api/leads': async req => {
    const o = await json(req), v = validarLead(o);
    const l = novoLead({ ...o, ...v, dor: normalizarDor(o.dor), modo: ['texto', 'ola_audio'].includes(o.modo) ? o.modo : '' });
    db.leads.push(l); salvar.leads();
    return leve(l);
  },
  'POST /api/leads/importar': async req => importar((await json(req)).texto),
  'GET /api/leads/exportar': (req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/csv; charset=utf-8', 'Content-Disposition': `attachment; filename="leads_${hojeISO()}.csv"` });
    res.end(exportarCSV());
  },

  'POST /api/whatsapp/conectar': async () => { await W.conectar(); return { ok: true }; },
  'POST /api/whatsapp/desconectar': async () => { await W.desconectar(); return { ok: true }; },
  'POST /api/whatsapp/codigo': async req => ({ codigo: await W.pedirCodigo((await json(req)).numero) }),
  'POST /api/whatsapp/ligar': async req => {
    const { ligado } = await json(req);
    db.config.waLigado = !!ligado; salvar.config(); W.wa.proximoEm = 0;
    registrar('whatsapp', ligado ? '▶️ Envios de WhatsApp ligados.' : '⏸️ Envios de WhatsApp pausados.');
    return { ok: true };
  },
  'POST /api/whatsapp/teste': async req => { await W.enviarTeste((await json(req)).modo); return { ok: true }; },

  'POST /api/email/ligar': async req => {
    const { ligado } = await json(req);
    db.config.emLigado = !!ligado; salvar.config(); EM.estadoEmail.proximoEm = 0;
    registrar('email', ligado ? '▶️ Envios de e-mail ligados.' : '⏸️ Envios de e-mail pausados.');
    return { ok: true };
  },
  'POST /api/email/teste': async req => ({ assunto: await EM.enviarTeste((await json(req)).para) }),
  'POST /api/email/verificar': async () => EM.verificarRespostas(),

  'GET /api/audios': () => db.audios,
  'POST /api/audios': async req => {
    let buf = await corpo(req), segundos = Number(req.headers['x-segundos']) || 0;
    if (ehWebm(buf)) ({ ogg: buf, segundos } = webmParaOgg(buf));
    else if (ehOgg(buf) && buf.includes(Buffer.from('OpusHead'))) segundos = duracaoOgg(buf) || segundos;
    else throw new Erro(415, 'Formato não aceito. Grave pelo painel ou envie um arquivo .ogg / .opus (mensagem de voz).');
    const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
    const a = { id, arquivo: `${id}.ogg`, nome: decodeURIComponent(req.headers['x-nome'] || 'Áudio').slice(0, 80),
      dor: ANGULOS.includes(req.headers['x-dor']) ? req.headers['x-dor'] : 'geral', segundos: Math.round(segundos),
      waveform: String(req.headers['x-waveform'] || '').slice(0, 200), usos: 0, criadoEm: new Date().toISOString() };
    fs.writeFileSync(path.join(PASTA_AUDIOS, a.arquivo), buf);
    db.audios.push(a); salvar.audios();
    registrar('audio', `🎤 Áudio "${a.nome}" salvo (${a.segundos}s).`);
    return a;
  }
};

const rotasComId = [
  ['GET', /^\/api\/leads\/(\w+)$/, (l) => { l.naoLida = false; salvar.leads(); return l; }, 'lead'],
  ['PUT', /^\/api\/leads\/(\w+)$/, async (l, req) => {
    const o = await json(req);
    if ('whatsapp' in o || 'email' in o) {
      const v = validarLead({ whatsapp: o.whatsapp ?? l.whatsapp, email: o.email ?? l.email }, l.id);
      if (v.whatsapp !== l.whatsapp) l.wa = { estado: 'novo' };
      Object.assign(l, v);
    }
    for (const k of ['nome', 'escritorio', 'cidade', 'uf', 'obs', 'origem']) if (k in o) l[k] = String(o[k] || '').trim();
    if ('dor' in o) l.dor = normalizarDor(o.dor);
    if ('modo' in o) l.modo = ['texto', 'ola_audio'].includes(o.modo) ? o.modo : '';
    if ('status' in o && STATUS.includes(o.status)) l.status = o.status;
    if ('naoLida' in o) l.naoLida = !!o.naoLida;
    salvar.leads();
    return leve(l);
  }, 'lead'],
  ['DELETE', /^\/api\/leads\/(\w+)$/, (l) => { db.leads = db.leads.filter(x => x !== l); salvar.leads(); return { ok: true }; }, 'lead'],
  ['POST', /^\/api\/leads\/(\w+)\/responder$/, async (l, req) => { await W.responder(l, String((await json(req)).texto || '').trim() || (() => { throw new Erro(400, 'Mensagem vazia.'); })()); return { ok: true }; }, 'lead'],
  ['PUT', /^\/api\/audios\/(\w+)$/, async (a, req) => {
    const o = await json(req);
    if (o.nome) a.nome = String(o.nome).slice(0, 80);
    if (ANGULOS.includes(o.dor)) a.dor = o.dor;
    salvar.audios(); return a;
  }, 'audio'],
  ['DELETE', /^\/api\/audios\/(\w+)$/, (a) => {
    fs.rmSync(path.join(PASTA_AUDIOS, a.arquivo), { force: true });
    db.audios = db.audios.filter(x => x !== a); salvar.audios(); return { ok: true };
  }, 'audio'],
  ['GET', /^\/api\/audios\/(\w+)\/arquivo$/, (a, req, res) => {
    res.writeHead(200, { 'Content-Type': 'audio/ogg', 'Cache-Control': 'no-store' });
    res.end(fs.readFileSync(path.join(PASTA_AUDIOS, a.arquivo)));
  }, 'audio']
];

async function tratar(req, res) {
  const url = new URL(req.url, 'http://x');
  try {
    // Só o próprio painel conversa com o sistema: bloqueia sites abertos no navegador (CSRF / DNS rebinding).
    if (!['localhost', '127.0.0.1'].includes((req.headers.host || '').replace(/:\d+$/, ''))) throw new Erro(403, 'Acesso negado.');
    if (url.pathname.startsWith('/api/') && req.method !== 'GET') {
      const origem = req.headers.origin;
      if ((origem && !/^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origem)) || req.headers['x-epiverso'] !== '1') throw new Erro(403, 'Acesso negado.');
    }
    const direta = rotas[`${req.method} ${url.pathname}`];
    if (direta) { const r = await direta(req, res); if (r !== undefined) responder(res, 200, r); return; }
    for (const [metodo, re, fn, tipo] of rotasComId) {
      const m = url.pathname.match(re);
      if (!m || metodo !== req.method) continue;
      const alvo = (tipo === 'lead' ? db.leads : db.audios).find(x => x.id === m[1]);
      if (!alvo) throw new Erro(404, 'Não encontrado.');
      const r = await fn(alvo, req, res);
      if (r !== undefined) responder(res, 200, r);
      return;
    }
    if (url.pathname.startsWith('/api/')) throw new Erro(404, 'Rota não encontrada.');
    // arquivos do painel
    const arquivo = path.normalize(path.join(PASTA_PAINEL, url.pathname === '/' ? 'index.html' : decodeURIComponent(url.pathname)));
    if (!arquivo.startsWith(PASTA_PAINEL) || !fs.existsSync(arquivo) || fs.statSync(arquivo).isDirectory()) throw new Erro(404, 'Não encontrado.');
    responder(res, 200, fs.readFileSync(arquivo), TIPOS[path.extname(arquivo)] || 'application/octet-stream');
  } catch (e) {
    if (!res.headersSent) responder(res, e.status || 500, { erro: e.message || String(e) });
  }
}

// ------------------------------------------------------------------ início
function abrirNavegador(url) {
  if (process.env.EPIVERSO_SEM_NAVEGADOR) return;
  const cmd = process.platform === 'win32' ? `start "" "${url}"` : process.platform === 'darwin' ? `open "${url}"` : `xdg-open "${url}"`;
  exec(cmd, () => {});
}

async function jaRodando(porta) {
  try {
    const r = await fetch(`http://127.0.0.1:${porta}/api/ping`, { signal: AbortSignal.timeout(1500) });
    return (await r.json()).app === 'epiverso-prospeccao';
  } catch { return false; }
}

if (await jaRodando(PORTA)) {
  console.log(`O sistema já está aberto. Abrindo o painel: http://localhost:${PORTA}`);
  abrirNavegador(`http://localhost:${PORTA}`);
  setTimeout(() => process.exit(0), 1500);
} else {
  const servidor = http.createServer(tratar);
  let porta = PORTA;
  servidor.on('error', e => {
    if (e.code === 'EADDRINUSE' && porta < PORTA + 10) { porta++; servidor.listen(porta, '127.0.0.1'); }
    else { console.error('Não consegui abrir o servidor:', e.message); process.exit(1); }
  });
  servidor.on('listening', () => {
    const url = `http://localhost:${porta}`;
    console.log('\n  ┌──────────────────────────────────────────────┐');
    console.log('  │  EPIVERSO · PROSPECÇÃO                        │');
    console.log(`  │  Painel: ${url.padEnd(37)}│`);
    console.log('  │  Deixe esta janela aberta enquanto usa.       │');
    console.log('  │  Para fechar: feche a janela ou Ctrl+C.       │');
    console.log('  └──────────────────────────────────────────────┘\n');
    console.log(`  Dados em: ${PASTA_DADOS}\n`);
    abrirNavegador(url);
  });
  servidor.listen(porta, '127.0.0.1');
  W.iniciarWhatsApp();
  EM.iniciarEmail();
}
