// WhatsApp pelo QR Code (Baileys: conexão direta, sem navegador escondido, leve).
// Envia com ritmo humano (digitando…, gravando áudio…), uma mensagem diferente para cada lead,
// e para a sequência quando o lead responde.
import fs from 'node:fs';
import path from 'node:path';
import makeWASocket, { useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion, Browsers, jidNormalizedUser } from '@whiskeysockets/baileys';
import pino from 'pino';
import QRCode from 'qrcode';
import { db, salvar, registrar, janela, hojeISO, diasUteisEntre, enviosHoje, proximaEspera, leadAtivo, ultimoToque,
  marcarResposta, esperar, sorteio, horaAgora, daqui, CICLO, ESCALA as ESCALA_REAL, PASTA_SESSAO, PASTA_AUDIOS } from './dados.mjs';
import { contexto, aberturaWhatsApp, olaWhatsApp, followupWhatsApp, hashTexto, ANGULOS, sortear, tipoFone, foneBonito } from '../painel/motor.mjs';

export const wa = { status: 'desconectado', qrSvg: '', codigo: '', numero: '', nome: '', motivo: '', situacao: 'Pausado', proximoEm: 0, ocupado: false, erros: 0 };
let sock = null, querConectado = false, tentativas = 0, vigia = null;
const enviadas = new Map(); // id → mensagem, para o WhatsApp pedir reenvio se precisar

// Permite trocar o socket nos testes automáticos
let criarSocket = makeWASocket;
export function _usarSocketDeTeste(fn) { criarSocket = fn; }

const so = j => String(j || '').split('@')[0].split(':')[0].replace(/\D/g, '');
const semNono = d => (d.length === 13 && d.startsWith('55') && d[4] === '9' ? d.slice(0, 4) + d.slice(5) : d);
const nomeDo = l => l.nome || l.escritorio || foneBonito(l.whatsapp);

// ------------------------------------------------------------------ conexão
export function temSessao() { return fs.existsSync(path.join(PASTA_SESSAO, 'creds.json')); }

export async function conectar() {
  querConectado = true;
  if (sock) return;
  wa.status = 'conectando'; wa.qrSvg = ''; if (!tentativas) wa.motivo = '';
  const { state, saveCreds } = await useMultiFileAuthState(PASTA_SESSAO);
  let version;
  try { ({ version } = await Promise.race([fetchLatestBaileysVersion(), esperar(5000 / ESCALA_REAL).then(() => ({}))])); } catch { /* usa a versão embutida */ }
  const s = sock = criarSocket({
    auth: state, version, logger: pino({ level: 'silent' }), browser: Browsers.windows('Epiverso Prospecção'),
    markOnlineOnConnect: false, syncFullHistory: false, getMessage: async k => enviadas.get(k.id)
  });
  s.ev.on('creds.update', saveCreds);
  // Rede que "engole" a conexão (firewall, Wi-Fi ruim) não gera erro: sem QR nem conexão em 40 s, tenta de novo.
  clearTimeout(vigia);
  vigia = setTimeout(() => {
    if (sock !== s || wa.status !== 'conectando') return;
    console.log('[whatsapp] sem resposta do servidor do WhatsApp em 40s');
    sock = null;
    s.end(undefined).catch(() => {});
    tentarDeNovo(DisconnectReason.timedOut);
  }, 40000);
  s.ev.on('connection.update', async u => {
    if (s !== sock) return;
    if (u.qr) { tentativas = 0; wa.motivo = ''; wa.status = 'qr'; wa.qrSvg = await QRCode.toString(u.qr, { type: 'svg', margin: 1 }); }
    if (u.connection === 'open') {
      tentativas = 0; wa.status = 'conectado'; wa.qrSvg = ''; wa.codigo = ''; wa.motivo = '';
      wa.numero = so(s.user?.id); wa.nome = s.user?.name || '';
      registrar('whatsapp', `✅ WhatsApp conectado: ${foneBonito(wa.numero)}`);
    }
    if (u.connection === 'close') {
      sock = null;
      const codigo = u.lastDisconnect?.error?.output?.statusCode;
      if (codigo === DisconnectReason.loggedOut) {
        apagarSessao(); querConectado = false; wa.status = 'desconectado';
        return registrar('whatsapp', '🔌 O WhatsApp foi desconectado pelo celular. Para voltar, conecte de novo pelo QR Code.');
      }
      if (codigo === DisconnectReason.forbidden) {
        querConectado = false; wa.status = 'erro'; db.config.waLigado = false; salvar.config();
        wa.motivo = 'O WhatsApp recusou este número (pode ser restrição ou bloqueio). Envios pausados.';
        return registrar('erro', '⛔ ' + wa.motivo);
      }
      if (codigo === DisconnectReason.connectionReplaced) {
        querConectado = false; wa.status = 'desconectado';
        return registrar('whatsapp', '🔌 Outra janela do sistema abriu este mesmo WhatsApp. Esta foi desconectada.');
      }
      if (!querConectado) { wa.status = 'desconectado'; return; }
      if (wa.status === 'qr' && codigo === DisconnectReason.timedOut && !state.creds.registered) {
        querConectado = false; wa.status = 'desconectado'; wa.qrSvg = '';
        wa.motivo = 'O QR Code expirou. Clique em "Conectar WhatsApp" para gerar outro.';
        return;
      }
      tentarDeNovo(codigo);
    }
  });
  s.ev.on('messages.upsert', ({ messages, type }) => {
    if (type !== 'notify') return;
    for (const m of messages) tratarRecebida(m).catch(() => {});
  });
}

function tentarDeNovo(codigo) {
  if (!querConectado) { wa.status = 'desconectado'; return; }
  wa.status = 'conectando'; tentativas++;
  const espera = codigo === DisconnectReason.restartRequired ? 500 : Math.min(60000, 3000 * tentativas);
  if (tentativas >= 2) wa.motivo = `Não consegui falar com o WhatsApp (tentativa ${tentativas}). Confira a internet: o sistema tenta de novo sozinho.`;
  console.log(`[whatsapp] conexão fechada (código ${codigo ?? '?'}), tentando de novo em ${Math.round(espera / 1000)}s`);
  setTimeout(() => { if (querConectado && !sock) conectar().catch(e => registrar('erro', 'WhatsApp: ' + e.message)); }, espera);
}

/** Conectar sem câmera: o WhatsApp do celular pede um código de 8 letras. */
export async function pedirCodigo(numero) {
  const d = so(numero).length <= 11 ? '55' + so(numero) : so(numero);
  if (!/^55\d{10,11}$/.test(d)) throw new Error('Número inválido. Use DDD + número, ex.: 48 99999-0000.');
  if (wa.status === 'conectado') throw new Error('Já está conectado.');
  await conectar();
  for (let i = 0; i < 40 && wa.status !== 'qr'; i++) await esperar(500); // espera o socket ficar pronto
  if (!sock) throw new Error('Não consegui abrir a conexão com o WhatsApp. Confira a internet.');
  const c = await sock.requestPairingCode(d);
  wa.codigo = c.length === 8 ? c.slice(0, 4) + '-' + c.slice(4) : c;
  return wa.codigo;
}

export async function desconectar() {
  querConectado = false; clearTimeout(vigia);
  const s = sock, estavaConectado = wa.status === 'conectado'; sock = null; tentativas = 0;
  if (estavaConectado) { try { await Promise.race([s?.logout(), esperar(4000 / ESCALA_REAL)]); } catch { /* já estava fechado */ } }
  try { s?.end?.(undefined)?.catch?.(() => {}); } catch { /* idem */ }
  apagarSessao();
  Object.assign(wa, { status: 'desconectado', qrSvg: '', codigo: '', numero: '', nome: '', motivo: '' });
  registrar('whatsapp', '🔌 WhatsApp desconectado pelo painel.');
}

function apagarSessao() { fs.rmSync(PASTA_SESSAO, { recursive: true, force: true }); }

// ------------------------------------------------------------------ recebidas
function textoDe(msg) {
  let m = msg || {};
  for (let i = 0; i < 4; i++) {
    const dentro = m.ephemeralMessage || m.viewOnceMessage || m.viewOnceMessageV2 || m.documentWithCaptionMessage || m.editedMessage;
    if (!dentro?.message) break;
    m = dentro.message;
  }
  if (m.protocolMessage || (m.senderKeyDistributionMessage && Object.keys(m).length === 1)) return null;
  return m.conversation || m.extendedTextMessage?.text
    || (m.imageMessage && `[imagem] ${m.imageMessage.caption || ''}`.trim())
    || (m.videoMessage && `[vídeo] ${m.videoMessage.caption || ''}`.trim())
    || (m.audioMessage && '[áudio]') || (m.documentMessage && '[documento]') || (m.stickerMessage && '[figurinha]')
    || (m.reactionMessage && (m.reactionMessage.text ? `[reagiu ${m.reactionMessage.text}]` : null))
    || (m.contactMessage && '[contato]') || (m.locationMessage && '[localização]') || null;
}

async function tratarRecebida(m) {
  const jid = m.key?.remoteJid || '';
  if (m.key?.fromMe || !jid || /@(g\.us|broadcast|newsletter)$/.test(jid)) return;
  const texto = textoDe(m.message);
  if (texto === null) return;
  const candidatos = [jid, m.key.remoteJidAlt, m.key.senderPn].filter(Boolean);
  if (jid.endsWith('@lid') && sock?.signalRepository?.lidMapping) {
    try { const pn = await sock.signalRepository.lidMapping.getPNForLID(jid); if (pn) candidatos.push(pn); } catch { /* sem mapeamento */ }
  }
  const lead = acharLead(candidatos);
  if (!lead) return;
  if (jid.endsWith('@lid')) lead.wa.lid = jid;
  marcarResposta(lead, 'whatsapp', texto);
}

export function acharLead(jids) {
  const numeros = new Set(jids.filter(j => !String(j).endsWith('@lid')).map(j => semNono(so(j))));
  return db.leads.find(l => l.whatsapp && (jids.includes(l.wa?.jid) || jids.includes(l.wa?.lid) || numeros.has(semNono(l.whatsapp))));
}

// ------------------------------------------------------------------ envio
export function filaWhatsApp(cfg = db.config) {
  const hoje = hojeISO(), fups = [], novos = [];
  for (const l of db.leads) {
    if (!leadAtivo(l) || tipoFone(l.whatsapp) === 'invalido' || ['sem_whatsapp', 'followup'].includes(l.wa.estado)) continue;
    if (l.wa.estado === 'abertura') {
      if (cfg.waFollowup && diasUteisEntre(l.wa.aberturaEm, hoje) >= cfg.waDiasFollowup) fups.push({ lead: l, tipo: 'followup' });
    } else {
      const em = ultimoToque(l, 'email');
      if (em && diasUteisEntre(em, hoje) < cfg.diasEntreCanais) continue; // não chega pelos dois canais no mesmo dia
      novos.push({ lead: l, tipo: 'abertura' });
    }
  }
  return [...fups, ...novos];
}

function escolherModo(lead, cfg) {
  if (lead.modo === 'texto' || lead.modo === 'ola_audio') return lead.modo;
  if (cfg.waModo === 'misto') return Math.random() * 100 < cfg.waPercentAudio ? 'ola_audio' : 'texto';
  return cfg.waModo === 'ola_audio' ? 'ola_audio' : 'texto';
}

export function escolherAudio(angulo) {
  const existentes = db.audios.filter(a => fs.existsSync(path.join(PASTA_AUDIOS, a.arquivo)));
  const daDor = existentes.filter(a => a.dor === angulo);
  const gerais = existentes.filter(a => !a.dor || a.dor === 'geral');
  const opcoes = daDor.length ? daDor : gerais.length ? gerais : existentes;
  if (!opcoes.length) return null;
  const menor = Math.min(...opcoes.map(a => a.usos || 0));
  return sortear(opcoes.filter(a => (a.usos || 0) === menor));
}

function unico(gerar) {
  let t = '';
  for (let i = 0; i < 40; i++) { t = gerar(); if (!db.hashes.includes(hashTexto(t))) break; }
  return t;
}

async function digitar(jid, texto) {
  try {
    await sock.presenceSubscribe(jid);
    await sock.sendPresenceUpdate('composing', jid);
    await esperar(Math.min(9000, Math.max(2500, texto.length * 45)) * sorteio(0.8, 1.2));
    await sock.sendPresenceUpdate('paused', jid);
  } catch { /* presença é só um detalhe */ }
}

async function mandar(jid, conteudo) {
  const r = await sock.sendMessage(jid, conteudo);
  if (r?.key?.id) { enviadas.set(r.key.id, r.message); if (enviadas.size > 500) enviadas.delete(enviadas.keys().next().value); }
  return r;
}

async function enviarAudio(jid, audio) {
  const buf = fs.readFileSync(path.join(PASTA_AUDIOS, audio.arquivo));
  try { await sock.sendPresenceUpdate('recording', jid); } catch { /* idem */ }
  await esperar(Math.min(12, audio.segundos || 10) * 1000 * sorteio(0.6, 1));
  await mandar(jid, {
    audio: buf, mimetype: 'audio/ogg; codecs=opus', ptt: true, seconds: audio.segundos || 1,
    ...(audio.waveform ? { waveform: new Uint8Array(Buffer.from(audio.waveform, 'base64')) } : {})
  });
  try { await sock.sendPresenceUpdate('paused', jid); } catch { /* idem */ }
  audio.usos = (audio.usos || 0) + 1; salvar.audios();
}

async function resolverJid(lead) {
  if (lead.wa.jid) return lead.wa.jid;
  const [r] = (await sock.onWhatsApp(lead.whatsapp)) || [];
  if (!r?.exists) return null;
  lead.wa.jid = r.jid; salvar.leads();
  return r.jid;
}

async function enviarUm({ lead, tipo }, cfg) {
  const jid = await resolverJid(lead);
  if (!jid) {
    lead.wa.estado = 'sem_whatsapp'; salvar.leads();
    registrar('aviso', `📵 ${nomeDo(lead)} (${foneBonito(lead.whatsapp)}) não tem WhatsApp. Pulado.`, { leadId: lead.id });
    return false;
  }
  const angulo = lead.angulo || (lead.angulo = lead.dor || sortear(ANGULOS));
  const ctx = contexto(lead, cfg, 'whatsapp', angulo), m = db.mensagens.whatsapp;
  let modo = tipo === 'followup' ? 'texto' : escolherModo(lead, cfg), audio = null;
  if (modo === 'ola_audio' && !(audio = escolherAudio(angulo))) {
    modo = 'texto';
    if (!wa.avisouSemAudio) { wa.avisouSemAudio = true; registrar('aviso', '🎤 Modo "olá + áudio" ligado, mas nenhum áudio gravado. Enviando em texto: grave um áudio na aba Áudios.'); }
  }
  const texto = unico(() => tipo === 'followup' ? followupWhatsApp(m, ctx) : modo === 'ola_audio' ? olaWhatsApp(m, ctx) : aberturaWhatsApp(m, ctx, angulo));
  await digitar(jid, texto);
  await mandar(jid, { text: texto });
  const agora = new Date().toISOString(), h = { em: agora, canal: 'whatsapp', tipo, envio: true, modo, texto };
  lead.historico.push(h);
  if (tipo === 'abertura') { lead.wa.estado = 'abertura'; lead.wa.aberturaEm = agora; } else { lead.wa.estado = 'followup'; lead.wa.followupEm = agora; }
  if (lead.status === 'novo') lead.status = 'em_contato';
  db.hashes.push(hashTexto(texto)); salvar.hashes(); salvar.leads();
  if (audio) {
    await esperar(sorteio(20, 60) * 1000); // o tempo de "pegar o celular e gravar"
    if (!sock || wa.status !== 'conectado') registrar('aviso', `🎤 A conexão caiu antes do áudio para ${nomeDo(lead)}: só o olá foi enviado.`, { leadId: lead.id });
    else if (!leadAtivo(lead)) registrar('aviso', `🎤 ${nomeDo(lead)} respondeu ao olá antes do áudio: o áudio não foi enviado, a conversa é sua.`, { leadId: lead.id });
    else { await enviarAudio(jid, audio); h.texto += `\n[🎤 áudio: ${audio.nome}]`; salvar.leads(); }
  }
  registrar('whatsapp', `📤 ${tipo === 'abertura' ? 'Abertura' : 'Follow-up'}${audio ? ' (olá + áudio)' : ''} para ${nomeDo(lead)}${lead.escritorio && lead.nome ? ' · ' + lead.escritorio : ''}`, { leadId: lead.id });
  return true;
}

/** Resposta digitada no painel para um lead. */
export async function responder(lead, texto) {
  if (!sock || wa.status !== 'conectado') throw new Error('Conecte o WhatsApp primeiro.');
  const jid = lead.wa.lid || await resolverJid(lead);
  if (!jid) throw new Error('Este número não tem WhatsApp.');
  await digitar(jid, texto);
  await mandar(jid, { text: texto });
  lead.historico.push({ em: new Date().toISOString(), canal: 'whatsapp', tipo: 'enviada', texto });
  lead.naoLida = false; salvar.leads();
}

/** Manda um exemplo para o seu próprio número (chat "Você"). */
export async function enviarTeste(modo) {
  if (!sock || wa.status !== 'conectado') throw new Error('Conecte o WhatsApp primeiro.');
  const jid = jidNormalizedUser(sock.user.id), cfg = db.config, angulo = sortear(ANGULOS);
  const ctx = contexto({ nome: 'Marcos Silva', escritorio: 'Contabilidade Exemplo', cidade: 'Joinville' }, cfg, 'whatsapp', angulo);
  if (modo === 'ola_audio') {
    const audio = escolherAudio(angulo);
    if (!audio) throw new Error('Grave um áudio na aba Áudios primeiro.');
    await mandar(jid, { text: olaWhatsApp(db.mensagens.whatsapp, ctx) });
    await esperar(3000);
    await enviarAudio(jid, audio);
  } else {
    await mandar(jid, { text: aberturaWhatsApp(db.mensagens.whatsapp, ctx, angulo) });
  }
  registrar('whatsapp', '🧪 Mensagem de teste enviada para o seu próprio número (abra a conversa "Você" no WhatsApp).');
}

// ------------------------------------------------------------------ laço de envio (roda a cada 5 s)
async function passo() {
  const cfg = db.config;
  if (wa.ocupado) return;
  if (!cfg.waLigado) { wa.situacao = 'Pausado'; wa.proximoEm = 0; return; }
  if (wa.status !== 'conectado') { wa.situacao = 'Aguardando o WhatsApp conectar'; return; }
  if (!cfg.seuNome) { wa.situacao = 'Falta configurar: seu nome'; return; }
  const j = janela(cfg);
  if (!j.aberta) { wa.situacao = j.motivo; wa.proximoEm = 0; return; }
  const feitos = enviosHoje('whatsapp');
  if (feitos >= cfg.waMeta) { wa.situacao = `Meta de hoje batida (${feitos}/${cfg.waMeta}). Volta amanhã.`; return; }
  const fila = filaWhatsApp(cfg);
  if (!fila.length) { wa.situacao = 'Ninguém na fila agora (cadastre mais leads com WhatsApp).'; return; }
  if (!wa.proximoEm) wa.proximoEm = daqui(sorteio(60, 180)); // começa com um respiro
  const prox = fila[0].lead;
  if (Date.now() < wa.proximoEm) {
    wa.situacao = `Próximo envio às ${horaAgora(new Date(wa.proximoEm))} para ${nomeDo(prox)} · ${feitos}/${cfg.waMeta} hoje`;
    return;
  }
  wa.ocupado = true;
  wa.situacao = `Enviando para ${nomeDo(prox)}…`;
  try {
    const enviou = await enviarUm(fila[0], cfg);
    wa.erros = 0;
    if (enviou) {
      const restantes = Math.min(cfg.waMeta - enviosHoje('whatsapp'), filaWhatsApp(cfg).length);
      wa.proximoEm = daqui(proximaEspera({ espalhar: cfg.espalhar, minSeg: cfg.waIntervaloMin * 60, maxSeg: cfg.waIntervaloMax * 60, restantes, cfg }));
    } else {
      wa.proximoEm = daqui(sorteio(15, 45)); // número sem WhatsApp: segue logo para o próximo
    }
  } catch (e) {
    wa.erros++;
    registrar('erro', `WhatsApp: erro ao enviar para ${nomeDo(prox)}: ${e.message}`);
    wa.proximoEm = daqui(5 * 60);
    if (wa.erros >= 3) {
      cfg.waLigado = false; salvar.config(); wa.erros = 0;
      registrar('erro', '⛔ 3 erros seguidos no WhatsApp: envios pausados por segurança. Confira a conexão e ligue de novo.');
    }
  } finally {
    wa.ocupado = false;
  }
}

export function iniciarWhatsApp() {
  if (temSessao()) conectar().catch(e => registrar('erro', 'WhatsApp: ' + e.message));
  setInterval(passo, CICLO);
}
