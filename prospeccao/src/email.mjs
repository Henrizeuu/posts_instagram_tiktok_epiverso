// Envio de e-mail: sequência de 3 (abertura + 2 follow-ups na mesma conversa), aquecimento,
// ritmo humano e parada automática por IMAP quando o lead responde ou o e-mail volta.
import nodemailer from 'nodemailer';
import { db, salvar, registrar, janela, hojeISO, diasUteisEntre, enviosHoje, proximaEspera, leadAtivo, ultimoToque,
  marcarResposta, sorteio, horaAgora, daqui, CICLO } from './dados.mjs';
import { contexto, emailEtapa, hashTexto, ANGULOS, sortear, EMAIL_OK } from '../painel/motor.mjs';
import { imapBuscar, dataImap, q } from './imap.mjs';

const GRATUITOS = new Set(['gmail.com', 'hotmail.com', 'outlook.com', 'live.com', 'yahoo.com', 'yahoo.com.br', 'uol.com.br',
  'bol.com.br', 'terra.com.br', 'icloud.com', 'hotmail.com.br', 'outlook.com.br', 'ig.com.br']);
const ESCADA = [10, 20, 30]; // e-mails/dia nas semanas 1, 2 e 3; depois, o limite máximo
const dominio = e => (e || '').split('@')[1] || '';

export const estadoEmail = { situacao: 'Pausado', proximoEm: 0, ocupado: false, erros: 0, ultimaVerificacao: 0 };

export function faltaConfigurar(cfg) {
  const f = [];
  if (!cfg.seuNome) f.push('seu nome');
  if (!EMAIL_OK.test(cfg.emEmail || '')) f.push('e-mail remetente');
  if (!cfg.smtpHost) f.push('servidor SMTP');
  if (!cfg.smtpSenha) f.push('senha do e-mail');
  return f;
}

export function limiteHoje(cfg) {
  const inicio = cfg.emInicioAquecimento || cfg._emInicio || hojeISO();
  const dias = Math.max(0, (new Date(hojeISO()) - new Date(inicio.slice(0, 10))) / 86400000);
  const semana = Math.floor(dias / 7);
  return Math.min(semana < ESCADA.length ? ESCADA[semana] : cfg.emLimiteMax, cfg.emLimiteMax);
}

export function filaEmail(cfg = db.config) {
  const hoje = hojeISO(), fila = [];
  for (const l of db.leads) {
    if (!leadAtivo(l) || !l.email || l.em.estado === 'devolvido') continue;
    if (l.em.etapa === 1 && diasUteisEntre(l.em.ultimoEnvio, hoje) >= cfg.emDiasEtapa2) fila.push({ lead: l, etapa: 1 });
    else if (l.em.etapa === 2 && diasUteisEntre(l.em.ultimoEnvio, hoje) >= cfg.emDiasEtapa3) fila.push({ lead: l, etapa: 2 });
  }
  const dominios = new Set(fila.map(f => dominio(f.lead.email)));
  for (const l of db.leads) {
    if (!leadAtivo(l) || !EMAIL_OK.test(l.email || '') || l.em.etapa !== 0 || l.em.estado === 'devolvido') continue;
    const wa = ultimoToque(l, 'whatsapp');
    if (wa && diasUteisEntre(wa, hoje) < cfg.diasEntreCanais) continue; // não chega pelos dois canais no mesmo dia
    const d = dominio(l.email);
    if (!GRATUITOS.has(d) && dominios.has(d)) continue; // 1 contato novo por empresa por dia
    dominios.add(d);
    fila.push({ lead: l, etapa: 0 });
  }
  return fila;
}

const ehGoogle = cfg => /gmail|google/i.test(cfg.smtpHost || '');
/** O Google mostra a senha de app como "abcd efgh ijkl mnop": os espaços (às vezes invisíveis) fazem o login falhar. */
export const senhaDe = cfg => ehGoogle(cfg) ? String(cfg.smtpSenha || '').replace(/[\s\u00a0\u200b]/g, '') : String(cfg.smtpSenha || '').replace(/[\u00a0\u200b]/g, '').trim();

const transporte = cfg => nodemailer.createTransport({
  host: cfg.smtpHost, port: Number(cfg.smtpPorta), secure: Number(cfg.smtpPorta) === 465,
  auth: { user: (cfg.smtpUsuario || cfg.emEmail).trim(), pass: senhaDe(cfg) }, connectionTimeout: 30000, greetingTimeout: 30000
});

/** Traduz os erros do servidor de e-mail para o que fazer. */
export function explicarErroEmail(e, cfg = db.config) {
  const txt = `${e.response || ''} ${e.message || ''}`;
  if (e.code === 'EAUTH' || /\b535\b|BadCredentials|authentication failed|Username and Password not accepted/i.test(txt)) {
    if (ehGoogle(cfg)) {
      return 'O Gmail recusou a senha. Ele não aceita a senha normal da conta aqui: precisa de uma SENHA DE APP. ' +
        '1) Ative a verificação em 2 etapas em myaccount.google.com/security. ' +
        '2) Crie a senha de app em myaccount.google.com/apppasswords (nome: Epiverso). ' +
        '3) Cole as 16 letras no campo Senha, salve e teste de novo. ' +
        (senhaDe(cfg).length !== 16 ? `(A senha salva tem ${senhaDe(cfg).length} caracteres; a senha de app tem 16.)` : 'Se já é senha de app, confira se o e-mail remetente é a mesma conta onde ela foi criada.');
    }
    return 'O servidor recusou usuário ou senha. Confira o e-mail, a senha (alguns provedores exigem "senha de app") e se o SMTP está liberado na sua conta.';
  }
  if (/ETIMEDOUT|ECONNECTION|ECONNREFUSED|ENOTFOUND|ESOCKET/.test(e.code || '') || /timeout|getaddrinfo/i.test(txt)) {
    return `Não consegui conectar em ${cfg.smtpHost}:${cfg.smtpPorta}. Confira o servidor, a porta (587 ou 465) e a internet; antivírus/firewall às vezes bloqueiam.`;
  }
  if (/\b5\.4\.5\b|daily|limit exceeded|quota/i.test(txt)) return 'O provedor bloqueou por limite de envio diário. Espere até amanhã e diminua o limite em Configurações.';
  return 'Erro do servidor de e-mail: ' + (e.message || String(e));
}

function montar(lead, etapa, cfg) {
  const angulo = lead.angulo || (lead.angulo = lead.dor || sortear(ANGULOS));
  const ctx = contexto(lead, cfg, 'email', angulo);
  let r;
  for (let i = 0; i < 40; i++) { r = emailEtapa(db.mensagens.email, ctx, etapa, angulo); if (!db.hashes.includes(hashTexto(r.corpo))) break; }
  return r;
}

async function enviar(cfg, para, assunto, texto, anteriores = []) {
  const messageId = `<${Date.now().toString(36)}.${Math.random().toString(36).slice(2, 10)}@${dominio(cfg.emEmail)}>`;
  await transporte(cfg).sendMail({
    from: { name: cfg.emNome || cfg.seuNome, address: cfg.emEmail }, to: para, subject: assunto, text: texto, messageId,
    inReplyTo: anteriores.at(-1), references: anteriores.length ? anteriores : undefined,
    list: { unsubscribe: { url: `mailto:${cfg.emEmail}?subject=remover`, comment: 'Remover' } }
  });
  return messageId;
}

async function enviarUm({ lead, etapa }, cfg) {
  if (etapa > 0 && cfg.imapAtivo) { // respondeu nos últimos minutos?
    await verificarRespostas([lead]).catch(() => {});
    if (!leadAtivo(lead)) return;
  }
  const r = montar(lead, etapa, cfg);
  const assunto = etapa === 0 ? r.assunto : 'Re: ' + lead.em.assunto;
  let id;
  try {
    id = await enviar(cfg, { name: lead.nome, address: lead.email }, assunto, r.corpo, lead.em.ids || []);
  } catch (e) {
    if (e.code === 'EAUTH') {
      cfg.emLigado = false; salvar.config();
      return registrar('erro', '✉️ Envios de e-mail pausados. ' + explicarErroEmail(e, cfg));
    }
    if (e.code === 'EENVELOPE' && e.rejected?.length) {
      lead.em.estado = 'devolvido'; salvar.leads();
      return registrar('devolvido', `↩️ ${lead.email} foi recusado pelo servidor (endereço inválido). Saiu da sequência.`, { leadId: lead.id });
    }
    estadoEmail.erros++;
    registrar('erro', `✉️ Erro ao enviar para ${lead.email}: ${e.message}`);
    if (estadoEmail.erros >= 3) {
      cfg.emLigado = false; salvar.config(); estadoEmail.erros = 0;
      registrar('erro', '✉️ 3 erros seguidos: envios de e-mail pausados para proteger o domínio. Veja a conexão e o limite do provedor.');
    }
    return;
  }
  estadoEmail.erros = 0;
  const agora = new Date().toISOString();
  Object.assign(lead.em, {
    etapa: etapa + 1, estado: `etapa${etapa + 1}`, ids: [...(lead.em.ids || []), id], ultimoEnvio: agora,
    ...(etapa === 0 ? { assunto, primeiroEnvio: agora } : {})
  });
  lead.status = 'em_contato';
  lead.historico.push({ em: agora, canal: 'email', tipo: etapa === 0 ? 'abertura' : `followup${etapa}`, envio: true, texto: `Assunto: ${assunto}\n\n${r.corpo}` });
  db.hashes.push(hashTexto(r.corpo)); salvar.hashes(); salvar.leads();
  if (!cfg.emInicioAquecimento && !cfg._emInicio) { cfg._emInicio = hojeISO(); salvar.config(); }
  registrar('email', `✉️ E-mail ${etapa + 1}/3 para ${lead.nome || lead.email}${lead.escritorio ? ' · ' + lead.escritorio : ''}: "${assunto}"`, { leadId: lead.id });
}

/** Lê a caixa de entrada: quem respondeu para a sequência; e-mail devolvido sai da lista. */
export async function verificarRespostas(somente) {
  const cfg = db.config;
  estadoEmail.ultimaVerificacao = Date.now();
  if (!cfg.imapAtivo) return { ok: false, msg: 'Leitura da caixa (IMAP) desligada em Configurações.' };
  const limite = new Date(Date.now() - 45 * 86400000).toISOString();
  const alvos = somente || db.leads.filter(l => leadAtivo(l) && l.em.etapa > 0 && l.em.estado !== 'devolvido' && (l.em.ultimoEnvio || '') > limite);
  if (!alvos.length) return { ok: true, msg: 'Nenhum e-mail aguardando resposta.' };
  const semAuto = 'NOT SUBJECT "autom" NOT SUBJECT "out of office" NOT SUBJECT "ausente"'; // IMAP: só ASCII aqui
  const buscas = [
    ...alvos.map(l => `SINCE ${dataImap(l.em.primeiroEnvio)} FROM ${q(l.email)} ${semAuto}`),
    ...alvos.map(l => `SINCE ${dataImap(l.em.primeiroEnvio)} OR FROM "mailer-daemon" FROM "postmaster" BODY ${q(l.email)}`)
  ];
  const res = await imapBuscar({ host: cfg.imapHost, porta: Number(cfg.imapPorta), usuario: (cfg.smtpUsuario || cfg.emEmail).trim(), senha: senhaDe(cfg) }, buscas);
  let respostas = 0, devolvidos = 0;
  alvos.forEach((l, i) => {
    if (res[i]?.length) { respostas++; marcarResposta(l, 'email', '(respondeu por e-mail: leia na sua caixa de entrada)'); }
    else if (res[alvos.length + i]?.length) {
      devolvidos++; l.em.estado = 'devolvido'; salvar.leads();
      registrar('devolvido', `↩️ ${l.email} voltou (endereço não existe). Saiu da sequência.`, { leadId: l.id });
    }
  });
  return { ok: true, msg: `Caixa verificada: ${respostas} resposta(s), ${devolvidos} devolvido(s).` };
}

export async function enviarTeste(para) {
  const cfg = db.config, falta = faltaConfigurar(cfg);
  if (falta.length) throw new Error('Falta configurar: ' + falta.join(', '));
  const lead = { nome: 'Marcos Silva', escritorio: 'Contabilidade Exemplo', cidade: 'Joinville', email: para, em: {} };
  const r = montar(lead, 0, cfg);
  try { await enviar(cfg, para, r.assunto, r.corpo); }
  catch (e) { throw new Error(explicarErroEmail(e, cfg)); }
  registrar('email', `✉️ E-mail de teste enviado para ${para}`);
  return r.assunto;
}

// ------------------------------------------------------------------ laço de envio (roda a cada 5 s)
async function passo() {
  const cfg = db.config;
  if (estadoEmail.ocupado) return;
  if (!cfg.emLigado) { estadoEmail.situacao = 'Pausado'; estadoEmail.proximoEm = 0; return; }
  const falta = faltaConfigurar(cfg);
  if (falta.length) { estadoEmail.situacao = 'Falta configurar: ' + falta.join(', '); return; }
  const j = janela(cfg);
  if (!j.aberta) { estadoEmail.situacao = j.motivo; estadoEmail.proximoEm = 0; return; }
  const lim = limiteHoje(cfg), feitos = enviosHoje('email');
  if (feitos >= lim) { estadoEmail.situacao = `Meta de hoje batida (${feitos}/${lim}). Volta amanhã.`; return; }
  estadoEmail.ocupado = true;
  try {
    if (cfg.imapAtivo && Date.now() - estadoEmail.ultimaVerificacao > 15 * 60000) {
      await verificarRespostas().catch(e => registrar('erro', '✉️ Não consegui ler a caixa de entrada: ' + e.message));
    }
    const fila = filaEmail(cfg);
    if (!fila.length) { estadoEmail.situacao = 'Nenhum e-mail para enviar agora (cadastre mais leads com e-mail).'; return; }
    if (!estadoEmail.proximoEm) estadoEmail.proximoEm = daqui(sorteio(30, 90));
    if (Date.now() < estadoEmail.proximoEm) {
      estadoEmail.situacao = `Próximo e-mail às ${horaAgora(new Date(estadoEmail.proximoEm))} · ${feitos}/${lim} hoje`;
      return;
    }
    estadoEmail.situacao = 'Enviando…';
    await enviarUm(fila[0], cfg);
    const restantes = Math.min(lim - enviosHoje('email'), filaEmail(cfg).length);
    estadoEmail.proximoEm = daqui(proximaEspera({ espalhar: cfg.espalhar, minSeg: cfg.emIntervaloMin, maxSeg: cfg.emIntervaloMax, restantes, cfg }));
  } catch (e) {
    registrar('erro', '✉️ ' + e.message);
  } finally {
    estadoEmail.ocupado = false;
  }
}

export function iniciarEmail() { setInterval(passo, CICLO); }
