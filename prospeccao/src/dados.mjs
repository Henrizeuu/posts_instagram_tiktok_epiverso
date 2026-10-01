// Armazenamento em arquivos JSON na pasta dados/ (sem banco de dados) e regras de agenda.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import MENSAGENS_PADRAO from './mensagens_padrao.mjs';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
export const RAIZ = path.resolve(AQUI, '..');
export const PASTA_PAINEL = fs.existsSync(path.join(AQUI, 'painel')) ? path.join(AQUI, 'painel') : path.join(RAIZ, 'painel');
export const PASTA_DADOS = process.env.EPIVERSO_DADOS ? path.resolve(process.env.EPIVERSO_DADOS) : path.join(RAIZ, 'dados');
export const PASTA_AUDIOS = path.join(PASTA_DADOS, 'audios');
export const PASTA_SESSAO = path.join(PASTA_DADOS, 'sessao-whatsapp');
fs.mkdirSync(PASTA_AUDIOS, { recursive: true });

export const CONFIG_PADRAO = {
  // meus dados
  seuNome: '', empresa: 'Epiverso', whatsappAssinatura: '(48) 99208-6832',
  // horário (vale para os dois canais)
  horaInicio: 8, horaFim: 18, pausaAlmoco: true, espalhar: true, diasEntreCanais: 2,
  // WhatsApp
  waLigado: false, waMeta: 15, waIntervaloMin: 4, waIntervaloMax: 12,
  waFollowup: true, waDiasFollowup: 3, waModo: 'texto', waPercentAudio: 50,
  // e-mail
  emLigado: false, emNome: '', emEmail: '', smtpHost: 'smtp.gmail.com', smtpPorta: 587, smtpUsuario: '', smtpSenha: '',
  imapAtivo: true, imapHost: 'imap.gmail.com', imapPorta: 993,
  emLimiteMax: 40, emInicioAquecimento: '', emIntervaloMin: 90, emIntervaloMax: 240, emDiasEtapa2: 3, emDiasEtapa3: 4
};

function ler(nome, padrao) {
  try { return JSON.parse(fs.readFileSync(path.join(PASTA_DADOS, nome), 'utf8')); }
  catch { return structuredClone(padrao); }
}
function gravar(nome, dados) {
  const alvo = path.join(PASTA_DADOS, nome), tmp = alvo + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(dados, null, 1));
  fs.renameSync(tmp, alvo);
}

export const db = {
  config: { ...CONFIG_PADRAO, ...ler('config.json', {}) },
  mensagens: mesclarMensagens(ler('mensagens.json', MENSAGENS_PADRAO)),
  leads: ler('leads.json', []),
  audios: ler('audios.json', []),
  hashes: ler('hashes.json', []),
  atividade: ler('atividade.json', [])
};
export const salvar = {
  config: () => gravar('config.json', db.config),
  mensagens: () => gravar('mensagens.json', db.mensagens),
  leads: () => gravar('leads.json', db.leads),
  audios: () => gravar('audios.json', db.audios),
  hashes: () => { db.hashes = db.hashes.slice(-8000); gravar('hashes.json', db.hashes); },
  atividade: () => gravar('atividade.json', db.atividade)
};

/** Garante que toda seção exista (para quem editou e apagou algo, ou de versões antigas). */
export function mesclarMensagens(m) {
  const p = structuredClone(MENSAGENS_PADRAO);
  for (const canal of ['whatsapp', 'email']) {
    m[canal] = { ...p[canal], ...(m[canal] || {}) };
    for (const [k, v] of Object.entries(p[canal])) {
      if (v && typeof v === 'object' && !Array.isArray(v)) m[canal][k] = { ...v, ...(m[canal][k] || {}) };
    }
  }
  if (!Array.isArray(m.respostas)) m.respostas = p.respostas;
  return m;
}

export function restaurarMensagens() {
  db.mensagens = structuredClone(MENSAGENS_PADRAO);
  salvar.mensagens();
}

// ------------------------------------------------------------------ atividade (o "feed" do painel)
export function registrar(tipo, texto, extra = {}) {
  db.atividade.push({ em: new Date().toISOString(), tipo, texto, ...extra });
  if (db.atividade.length > 400) db.atividade = db.atividade.slice(-400);
  salvar.atividade();
  console.log(`[${horaAgora()}] ${texto}`);
}

// ------------------------------------------------------------------ datas e janelas
export const hojeISO = (d = new Date()) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
export const horaAgora = (d = new Date()) => d.toTimeString().slice(0, 5);

export function diasUteisEntre(isoA, isoB) {
  if (!isoA) return Infinity;
  const a = new Date(isoA.slice(0, 10) + 'T12:00:00'), b = new Date(isoB.slice(0, 10) + 'T12:00:00');
  let n = 0;
  while (a < b) { a.setDate(a.getDate() + 1); const d = a.getDay(); if (d !== 0 && d !== 6) n++; }
  return n;
}

/** Fim da janela de envio de hoje (Date) ou null se agora não é hora de enviar, com o motivo. */
export function janela(cfg, agora = new Date()) {
  if (process.env.EPIVERSO_TESTE_JANELA_ABERTA) return { aberta: true, fim: new Date(Date.now() + 8 * 3600e3) };
  const dia = agora.getDay(), h = agora.getHours() + agora.getMinutes() / 60;
  if (dia === 0 || dia === 6) return { aberta: false, motivo: 'Fim de semana: volta na segunda às ' + cfg.horaInicio + 'h' };
  if (h < cfg.horaInicio) return { aberta: false, motivo: `Aguardando o horário (${cfg.horaInicio}h)` };
  if (h >= cfg.horaFim) return { aberta: false, motivo: `Encerrado por hoje (depois das ${cfg.horaFim}h)` };
  if (cfg.pausaAlmoco && h >= 12 && h < 13.5) return { aberta: false, motivo: 'Pausa de almoço (12h às 13h30)' };
  const fim = new Date(agora); fim.setHours(cfg.horaFim, 0, 0, 0);
  if (cfg.pausaAlmoco && h < 12) fim.setHours(12, 0, 0, 0);
  return { aberta: true, fim };
}

/** Minutos de janela que ainda restam hoje (considerando a pausa de almoço). */
export function minutosRestantes(cfg, agora = new Date()) {
  const h = agora.getHours() + agora.getMinutes() / 60;
  let fim = cfg.horaFim - Math.max(h, cfg.horaInicio);
  if (cfg.pausaAlmoco) fim -= Math.max(0, Math.min(13.5, cfg.horaFim) - Math.max(12, h, cfg.horaInicio));
  return Math.max(0, fim * 60);
}

/** Espera até o próximo envio: espalhada pelo resto do dia ou sorteada entre mínimo e máximo. */
export function proximaEspera({ espalhar, minSeg, maxSeg, restantes, cfg }) {
  const sorteio = minSeg + Math.random() * Math.max(0, maxSeg - minSeg);
  if (!espalhar || restantes <= 0) return sorteio;
  const base = (minutosRestantes(cfg) * 60) / restantes;
  return Math.max(minSeg, base * (0.55 + Math.random() * 0.7));
}

// ------------------------------------------------------------------ regras de lead
export const PAROU = ['respondeu', 'reuniao', 'cliente', 'sem_interesse', 'pausado'];
export const leadAtivo = l => !PAROU.includes(l.status);

export function ultimoToque(l, canal) {
  const h = (l.historico || []).filter(x => x.canal === canal && x.envio);
  return h.length ? h[h.length - 1].em : '';
}

export function enviosHoje(canal) {
  const hoje = hojeISO();
  let n = 0;
  for (const l of db.leads) for (const h of l.historico || []) if (h.canal === canal && h.envio && h.em.slice(0, 10) === hoje) n++;
  return n;
}

export function novoLead(o) {
  return {
    id: Date.now().toString(36) + Math.random().toString(36).slice(2, 7), nome: o.nome || '', escritorio: o.escritorio || '',
    whatsapp: o.whatsapp || '', email: (o.email || '').toLowerCase(), cidade: o.cidade || '', uf: o.uf || '', dor: o.dor || '',
    modo: o.modo || '', origem: o.origem || '', obs: o.obs || '', status: 'novo', criadoEm: new Date().toISOString(),
    wa: { estado: 'novo' }, em: { estado: 'novo', etapa: 0, ids: [] }, historico: []
  };
}

const QUER_SAIR = /\b(remover|remova|me tira|descadastr|n[aã]o (quero|tenho interesse|me (chame|mande|ligue))|pare de|parem de|sem interesse|sair da lista|stop)\b/i;

/** Registra uma mensagem recebida de um lead: para as sequências e avisa no painel. */
export function marcarResposta(l, canal, texto) {
  const em = new Date().toISOString(), quem = l.nome || l.escritorio || l.whatsapp || l.email;
  const sair = QUER_SAIR.test(texto || '');
  const jaConversando = ['respondeu', 'reuniao', 'cliente'].includes(l.status);
  if (sair) l.status = 'sem_interesse';
  else if (!jaConversando && l.status !== 'sem_interesse') l.status = 'respondeu';
  l.resposta = { canal, texto, em };
  l.naoLida = true;
  (l.historico ||= []).push({ em, canal, tipo: 'recebida', texto });
  salvar.leads();
  const trecho = (texto || '').replace(/\s+/g, ' ').slice(0, 90);
  if (sair) registrar('saiu', `🚫 ${quem} pediu para não receber mais (${canal}). Saiu das listas.`, { leadId: l.id });
  else registrar('resposta', `💬 ${quem} ${jaConversando ? 'mandou mensagem' : 'RESPONDEU'} no ${canal === 'email' ? 'e-mail' : 'WhatsApp'}: "${trecho}"`, { leadId: l.id });
}

// Escala de tempo: 1 = real. Os testes automáticos usam um valor pequeno para não esperar minutos.
export const ESCALA = Number(process.env.EPIVERSO_ESCALA_TEMPO || 1);
export const esperar = ms => new Promise(r => setTimeout(r, ms * ESCALA));
export const daqui = seg => Date.now() + seg * 1000 * ESCALA;
export const CICLO = Math.max(200, 5000 * ESCALA);
export const sorteio = (min, max) => min + Math.random() * Math.max(0, max - min);
