import * as M from './motor.mjs';

// ================================================================== base
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const hora = iso => iso ? new Date(iso).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) : '';
const dataHora = iso => iso ? new Date(iso).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }) : '';
const STATUS = { novo: 'Novo', em_contato: 'Em contato', respondeu: 'Respondeu', reuniao: 'Demo agendada', cliente: 'Virou cliente', sem_interesse: 'Sem interesse / não chamar', pausado: 'Pausado' };
const COR_STATUS = { respondeu: 'verde', reuniao: 'azul', cliente: 'azul', sem_interesse: 'vermelha', pausado: 'laranja', em_contato: '', novo: '' };
const MODOS = { '': 'Padrão', texto: 'Texto', ola_audio: 'Olá + áudio' };

async function api(metodo, url, dados, extra = {}) {
  const r = await fetch(url, { method: metodo, headers: { 'x-epiverso': '1', ...(dados !== undefined && !(dados instanceof Blob) ? { 'Content-Type': 'application/json' } : {}), ...extra },
    body: dados === undefined ? undefined : dados instanceof Blob ? dados : JSON.stringify(dados) });
  const tipo = r.headers.get('content-type') || '';
  const corpo = tipo.includes('json') ? await r.json() : await r.text();
  if (!r.ok) throw new Error(corpo?.erro || 'Erro ' + r.status);
  return corpo;
}
function toast(msg, erro) {
  const t = $('#toast'); t.textContent = msg; t.classList.toggle('erro', !!erro); t.classList.add('on');
  clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove('on'), erro ? 5000 : 2600);
}
async function acao(fn, ok) { try { const r = await fn(); if (ok) toast(typeof ok === 'function' ? ok(r) : ok); return r; } catch (e) { toast(e.message, true); } }
async function copiar(txt) { try { await navigator.clipboard.writeText(txt); toast('Copiado!'); } catch { toast('Não consegui copiar.', true); } }
function abrirModal(html) { $('#modal-caixa').innerHTML = html; $('#modal').hidden = false; }
function fecharModal() { $('#modal').hidden = true; $('#modal-caixa').innerHTML = ''; }
$('#modal').addEventListener('click', e => { if (e.target.id === 'modal' || e.target.closest('[data-fechar]')) fecharModal(); });
function bip() { try { const a = new AudioContext(), o = a.createOscillator(), g = a.createGain(); o.frequency.value = 880; g.gain.value = .08; o.connect(g); g.connect(a.destination); o.start(); o.stop(a.currentTime + .18); } catch { /* sem som */ } }

let E = null, CFG = null, MSG = null, LEADS = [], AUDIOS = [];
let aba = 'inicio', naoLidasAntes = null;

// ================================================================== navegação
$('#nav').addEventListener('click', e => {
  const b = e.target.closest('button[data-aba]'); if (!b) return;
  if (aba === 'mensagens' && mensagensAlteradas && !confirm('Há mudanças nas mensagens que não foram salvas. Sair mesmo assim?')) return;
  if (aba === 'mensagens') mensagensAlteradas = false;
  aba = b.dataset.aba;
  $$('#nav button').forEach(x => x.classList.toggle('ativo', x === b));
  $$('.aba').forEach(x => x.classList.toggle('ativo', x.id === 'aba-' + aba));
  ({ inicio: renderInicio, leads: renderLeads, mensagens: renderMensagens, audios: renderAudios, config: renderConfig, guia: renderGuia })[aba]();
});
const irPara = a => $(`#nav button[data-aba=${a}]`).click();

// ================================================================== cabeçalho + atualização
function renderChips() {
  const w = E.whatsapp, m = E.email;
  const ponto = w.status === 'conectado' ? 'on' : w.status === 'erro' ? 'erro' : ['qr', 'conectando'].includes(w.status) ? 'meio' : '';
  $('#chips').innerHTML = `
    ${E.naoLidas ? `<span class="chip alerta" data-ir="inicio">💬 <b>${E.naoLidas}</b> nova(s) resposta(s)</span>` : ''}
    <span class="chip"><span class="ponto ${ponto}"></span>WhatsApp ${{ conectado: 'conectado', qr: 'aguardando QR Code', conectando: 'conectando…', erro: 'com problema' }[w.status] || 'desconectado'}</span>
    <span class="chip">WhatsApp hoje <b>${w.hoje}/${w.meta}</b>${w.ligado ? '' : ' ⏸'}</span>
    <span class="chip">E-mail hoje <b>${m.hoje}/${m.limite}</b>${m.ligado ? '' : ' ⏸'}</span>`;
  document.title = (E.naoLidas ? `(${E.naoLidas}) ` : '') + 'Epiverso · Prospecção';
  if (naoLidasAntes !== null && E.naoLidas > naoLidasAntes) { bip(); toast('💬 Nova resposta de um lead!'); }
  naoLidasAntes = E.naoLidas;
}
$('#chips').addEventListener('click', e => { if (e.target.closest('[data-ir]')) irPara('inicio'); });

async function atualizar() {
  try { E = await api('GET', '/api/estado'); }
  catch { $('#chips').innerHTML = '<span class="chip" style="background:#8f1515;color:#fff">Sistema fechado: abra o INICIAR de novo</span>'; return; }
  renderChips();
  if (aba === 'inicio') atualizarInicio();
}

// ================================================================== INÍCIO
function renderInicio() {
  $('#aba-inicio').innerHTML = `
    <div id="avisos-inicio"></div>
    <div class="grade2">
      <div class="card"><h2>📱 WhatsApp</h2><div id="wa-conexao"></div><div id="wa-envios"></div></div>
      <div class="card"><h2>✉️ E-mail</h2><div id="em-envios"></div></div>
    </div>
    <div class="grade2" style="margin-top:14px">
      <div class="card"><h2>💬 Respostas</h2><p class="suave peq" style="margin:0 0 6px">Quem respondeu sai das sequências na hora. Clique para ver a conversa e responder.</p><div id="conversas"></div></div>
      <div class="card"><h2>📋 Atividade</h2><div class="feed" id="feed"></div></div>
    </div>
    <div class="card" style="margin-top:14px"><h2>📊 Números</h2><div id="numeros"></div></div>`;
  memo = {};
  if (E) atualizarInicio();
}
let memo = {};
function mudou(chave, valor) { const v = JSON.stringify(valor); if (memo[chave] === v) return false; memo[chave] = v; return true; }

function atualizarInicio() {
  if (!$('#wa-conexao')) return;
  const w = E.whatsapp, m = E.email;
  if (mudou('avisos', [E.seuNome, E.audios, CFG?.waModo])) {
    $('#avisos-inicio').innerHTML = !E.seuNome ? `<div class="aviso ruim">Comece por <a href="#" data-ir-config>Configurações</a>: coloque o seu nome (ele entra nas mensagens).</div>` : '';
  }
  // --- conexão
  if (mudou('conexao', [w.status, w.codigo, w.numero, w.motivo])) {
    memo.qr = null;
    let h = '';
    if (w.status === 'conectado') {
      h = `<div class="aviso ok">Conectado: <b>${esc(M.foneBonito(w.numero))}</b> ${w.nome ? '· ' + esc(w.nome) : ''}</div>
        <div class="linha"><button class="b mini" data-wa="teste-texto">Enviar teste para mim</button><button class="b mini" data-wa="teste-audio">Teste com áudio</button>
        <button class="b mini perigo" data-wa="desconectar">Desconectar</button></div>`;
    } else if (w.status === 'qr' || w.codigo) {
      h = `${w.codigo ? `<p>No celular: <b>WhatsApp › Aparelhos conectados › Conectar um aparelho › Conectar com número de telefone</b> e digite:</p><div class="codigo">${esc(w.codigo)}</div>`
        : `<ol class="passos"><li>Abra o WhatsApp no celular do número de <b>prospecção</b></li><li>Toque em <b>⋮</b> (ou Configurações) › <b>Aparelhos conectados</b> › <b>Conectar um aparelho</b></li><li>Aponte a câmera para o QR Code:</li></ol>
        <div class="qr"></div><p class="suave peq">O código se renova sozinho a cada 20 segundos.</p>`}
        <details style="margin-top:8px"><summary class="peq">Sem câmera? Conectar com código pelo número</summary>
        <div class="linha" style="margin-top:6px"><input id="num-par" placeholder="DDD + número, ex.: 48 99999-0000" style="max-width:240px"><button class="b mini" data-wa="codigo">Gerar código</button></div></details>
        <div class="linha" style="margin-top:8px"><button class="b mini" data-wa="cancelar">Cancelar</button></div>`;
    } else if (w.status === 'conectando') {
      h = `<div class="aviso info">Conectando ao WhatsApp…</div>${w.motivo ? `<div class="aviso">${esc(w.motivo)}</div>` : ''}
        <div class="linha"><button class="b mini" data-wa="cancelar">Cancelar</button></div>`;
    } else {
      h = `${w.motivo ? `<div class="aviso ${w.status === 'erro' ? 'ruim' : ''}">${esc(w.motivo)}</div>` : ''}
        <p class="suave peq" style="margin-top:0">Conecte o número que vai fazer a prospecção (de preferência um número só para isso, não o do suporte).</p>
        <button class="b prim grande" data-wa="conectar">Conectar WhatsApp (QR Code)</button>`;
    }
    $('#wa-conexao').innerHTML = h;
  }
  if ($('#wa-conexao .qr') && mudou('qr', w.qrSvg)) $('#wa-conexao .qr').innerHTML = w.qrSvg; // renova sem apagar o que foi digitado
  // --- envios WhatsApp
  if (mudou('waenv', [w.ligado, w.hoje, w.meta, w.situacao, w.fila])) {
    const pct = Math.min(100, Math.round(100 * w.hoje / Math.max(1, w.meta)));
    $('#wa-envios').innerHTML = `<h3>Envios de hoje</h3>
      <div class="linha entre"><span class="grande-num">${w.hoje}<span class="suave" style="font-size:18px">/${w.meta}</span></span>
      <button class="b ${w.ligado ? '' : 'prim'} grande" data-wa="${w.ligado ? 'pausar' : 'ligar'}">${w.ligado ? '⏸ Pausar envios' : '▶ Ligar envios'}</button></div>
      <div class="barra"><i style="width:${pct}%"></i></div>
      <div class="situacao">${w.ligado ? '🟢' : '⏸'} ${esc(w.situacao)}</div>
      <p class="suave peq" style="margin:0">${w.fila} na fila (aberturas + follow-ups). Ligado, ele envia sozinho todo dia útil no horário configurado, com intervalos de pessoa.</p>`;
  }
  // --- e-mail
  if (mudou('email', [m])) {
    const pct = Math.min(100, Math.round(100 * m.hoje / Math.max(1, m.limite)));
    $('#em-envios').innerHTML = `${m.falta.length ? `<div class="aviso">Falta configurar: <b>${esc(m.falta.join(', '))}</b>. <a href="#" data-ir-config>Abrir Configurações</a></div>` : ''}
      <h3>Envios de hoje</h3>
      <div class="linha entre"><span class="grande-num">${m.hoje}<span class="suave" style="font-size:18px">/${m.limite}</span></span>
      <button class="b ${m.ligado ? '' : 'prim'} grande" data-em="${m.ligado ? 'pausar' : 'ligar'}" ${m.falta.length && !m.ligado ? 'disabled' : ''}>${m.ligado ? '⏸ Pausar envios' : '▶ Ligar envios'}</button></div>
      <div class="barra"><i style="width:${pct}%"></i></div>
      <div class="situacao">${m.ligado ? '🟢' : '⏸'} ${esc(m.situacao)}</div>
      <p class="suave peq" style="margin:0">${m.fila} na fila. Limite de hoje: ${m.limite} (aquecimento: 10 → 20 → 30 → ${m.limiteMax} por dia, semana a semana).</p>
      <div class="linha" style="margin-top:10px"><button class="b mini" data-em="verificar">Ver respostas na caixa agora</button></div>`;
  }
  // --- conversas
  if (mudou('conversas', E.conversas)) {
    $('#conversas').innerHTML = E.conversas.length ? E.conversas.map(c => `<div class="conversa-item" data-lead="${c.id}">
        <div style="min-width:0"><div>${c.naoLida ? '<span class="nova"></span>' : ''}<b>${esc(c.nome || c.escritorio || 'Sem nome')}</b> <span class="suave peq">${c.nome && c.escritorio ? esc(c.escritorio) + ' · ' : ''}${c.resposta.canal === 'email' ? 'e-mail' : 'WhatsApp'} · ${dataHora(c.resposta.em)}</span></div>
        <div class="txt">${esc(c.resposta.texto)}</div></div><span class="tag ${COR_STATUS[c.status]}">${STATUS[c.status]}</span></div>`).join('')
      : '<p class="suave">Ninguém respondeu ainda. Quando responderem, aparece aqui (e toca um aviso).</p>';
  }
  // --- feed
  if (mudou('feed', E.atividade[0])) {
    $('#feed').innerHTML = E.atividade.length ? E.atividade.map(a => `<div><time>${dataHora(a.em)}</time><span class="t-${a.tipo}">${esc(a.texto)}</span></div>`).join('')
      : '<p class="suave">Nada ainda. O que o sistema fizer aparece aqui.</p>';
  }
  if (mudou('numeros', E.metricas)) {
    const n = E.metricas;
    $('#numeros').innerHTML = `<div class="form">
      <div><div class="suave peq">Leads cadastrados</div><div class="grande-num">${n.leads}</div><div class="suave peq">${n.novos} ainda não contatados</div></div>
      <div><div class="suave peq">Resposta no WhatsApp</div><div class="grande-num">${n.whatsapp.taxa}%</div><div class="suave peq">${n.whatsapp.respostas} de ${n.whatsapp.contatados} · meta 20% a 35%</div></div>
      <div><div class="suave peq">Resposta no e-mail</div><div class="grande-num">${n.email.taxa}%</div><div class="suave peq">${n.email.respostas} de ${n.email.contatados} · meta 3% a 8%</div></div>
      <div><div class="suave peq">Demos / clientes</div><div class="grande-num">${n.reunioes}</div><div class="suave peq">${n.sairam} pediram para não chamar</div></div></div>
      ${n.whatsapp.contatados >= 20 && n.whatsapp.taxa < 10 ? '<div class="aviso ruim">Resposta no WhatsApp abaixo de 10%: lista fria ou mensagem fraca. Reduza a meta diária por uns dias e revise as mensagens. Pouca resposta é o que leva a bloqueio.</div>' : ''}
      ${n.whatsapp.contatados >= 20 && n.sairam / n.whatsapp.contatados > 0.05 ? '<div class="aviso ruim">Mais de 5% pediram para parar. Diminua o volume e use mais o modo olá + áudio.</div>' : ''}`;
  }
}

$('#aba-inicio').addEventListener('click', async e => {
  if (e.target.closest('[data-ir-config]')) { e.preventDefault(); return irPara('config'); }
  const c = e.target.closest('[data-lead]'); if (c) return abrirConversa(c.dataset.lead);
  const b = e.target.closest('[data-wa],[data-em]'); if (!b) return;
  b.disabled = true;
  const w = b.dataset.wa, m = b.dataset.em;
  if (w === 'conectar') await acao(() => api('POST', '/api/whatsapp/conectar'));
  if (w === 'cancelar' || w === 'desconectar') {
    if (w === 'desconectar' && !confirm('Desconectar este WhatsApp do sistema? Para voltar, precisa escanear o QR de novo.')) { b.disabled = false; return; }
    await acao(() => api('POST', '/api/whatsapp/desconectar'));
  }
  if (w === 'codigo') await acao(() => api('POST', '/api/whatsapp/codigo', { numero: $('#num-par').value }), r => 'Código: ' + r.codigo);
  if (w === 'ligar' || w === 'pausar') {
    if (w === 'ligar' && E.whatsapp.status !== 'conectado') toast('Ligado. Os envios começam quando o WhatsApp estiver conectado.');
    await acao(() => api('POST', '/api/whatsapp/ligar', { ligado: w === 'ligar' }));
  }
  if (w === 'teste-texto') await acao(() => api('POST', '/api/whatsapp/teste', { modo: 'texto' }), 'Enviado! Veja a conversa "Você" no WhatsApp.');
  if (w === 'teste-audio') await acao(() => api('POST', '/api/whatsapp/teste', { modo: 'ola_audio' }), 'Enviando olá + áudio para você…');
  if (m === 'ligar' || m === 'pausar') await acao(() => api('POST', '/api/email/ligar', { ligado: m === 'ligar' }));
  if (m === 'verificar') await acao(() => api('POST', '/api/email/verificar'), r => r.msg);
  b.disabled = false;
  memo = {}; atualizar();
});

// ------------------------------------------------------------------ conversa (modal)
async function abrirConversa(id) {
  const l = await acao(() => api('GET', '/api/leads/' + id)); if (!l) return;
  const ctx = M.contexto(l, CFG || {}, 'whatsapp', l.angulo || 'geral');
  const respostas = (MSG?.respostas || []).map(r => ({ titulo: r.titulo, texto: M.limpar(M.preencher(M.spin(r.texto, ctx), ctx)) }));
  const temZap = l.whatsapp && l.wa?.estado !== 'sem_whatsapp', podeResponder = temZap && E.whatsapp.status === 'conectado';
  abrirModal(`<div class="linha entre"><h2 style="margin:0">${esc(l.nome || l.escritorio || 'Lead')}</h2><button class="b mini" data-fechar>✕ Fechar</button></div>
    <p class="suave peq">${[l.escritorio, l.cidade && l.cidade + (l.uf ? '/' + l.uf : ''), M.foneBonito(l.whatsapp), l.email].filter(Boolean).map(esc).join(' · ')}</p>
    <div class="bolhas" id="bolhas">${(l.historico || []).map(h => `<div class="bolha ${h.tipo === 'recebida' ? '' : 'nossa'}">${esc(h.texto)}<small>${h.canal === 'email' ? '✉️' : '📱'} ${dataHora(h.em)} · ${{ abertura: 'abertura', followup: 'follow-up', followup1: 'follow-up 1', followup2: 'follow-up 2', recebida: 'recebida', enviada: 'você respondeu' }[h.tipo] || h.tipo}</small></div>`).join('') || '<p class="suave">Sem mensagens ainda.</p>'}</div>
    <label>Situação do lead</label>
    <select id="conv-status" style="max-width:320px">${Object.entries(STATUS).map(([k, v]) => `<option value="${k}" ${k === l.status ? 'selected' : ''}>${v}</option>`).join('')}</select>
    ${l.resposta?.canal === 'email' ? '<div class="aviso info">Respondeu por e-mail: responda pela sua caixa de entrada normal.</div>' : ''}
    ${temZap ? `<label>Responder pelo WhatsApp</label>
      <select id="conv-pronta"><option value="">Respostas prontas…</option>${respostas.map((r, i) => `<option value="${i}">${esc(r.titulo)}</option>`).join('')}</select>
      <textarea id="conv-texto" rows="4" style="margin-top:6px" placeholder="Escreva aqui (ou escolha uma resposta pronta acima e ajuste)"></textarea>
      <div class="linha" style="margin-top:8px"><button class="b prim" id="conv-enviar" ${podeResponder ? '' : 'disabled'}>Enviar no WhatsApp</button>
      ${podeResponder ? '' : '<span class="suave peq">Conecte o WhatsApp para responder daqui (ou responda pelo celular).</span>'}</div>` : ''}`);
  const bol = $('#bolhas'); bol.scrollTop = bol.scrollHeight;
  $('#conv-status').onchange = e => acao(() => api('PUT', '/api/leads/' + id, { status: e.target.value }), 'Situação atualizada');
  if ($('#conv-pronta')) $('#conv-pronta').onchange = e => { if (e.target.value !== '') $('#conv-texto').value = respostas[e.target.value].texto; };
  if ($('#conv-enviar')) $('#conv-enviar').onclick = async () => {
    const texto = $('#conv-texto').value.trim(); if (!texto) return;
    $('#conv-enviar').disabled = true;
    if (await acao(() => api('POST', `/api/leads/${id}/responder`, { texto }), 'Enviado ✓')) abrirConversa(id);
    else $('#conv-enviar').disabled = false;
  };
  atualizar();
}

// ================================================================== LEADS
let filtro = { busca: '', status: '' };
const CAMPOS_LEAD = [['nome', 'Nome do contato', 'Ex.: Marcos Silva'], ['escritorio', 'Escritório', 'Ex.: Contabilidade Silva'], ['whatsapp', 'WhatsApp', '(48) 99999-0000'],
  ['email', 'E-mail', 'marcos@escritorio.com.br'], ['cidade', 'Cidade', ''], ['uf', 'UF', 'SC']];
function formLead(l = {}) {
  return `<div class="form">${CAMPOS_LEAD.map(([k, rot, ph]) => `<div><label>${rot}</label><input data-campo="${k}" value="${esc(k === 'whatsapp' ? M.foneBonito(l[k]) : l[k])}" placeholder="${ph}"></div>`).join('')}
    <div><label>Dor principal</label><select data-campo="dor"><option value="">Sortear</option>${M.ANGULOS.map(a => `<option value="${a}" ${l.dor === a ? 'selected' : ''}>${M.DORES[a].titulo}</option>`).join('')}</select></div>
    <div><label>Abertura no WhatsApp</label><select data-campo="modo">${Object.entries(MODOS).map(([k, v]) => `<option value="${k}" ${(l.modo || '') === k ? 'selected' : ''}>${v}</option>`).join('')}</select></div></div>
    <label>Observação</label><input data-campo="obs" value="${esc(l.obs)}" placeholder="Ex.: muitos clientes de varejo">`;
}
const lerForm = el => Object.fromEntries($$('[data-campo]', el).map(i => [i.dataset.campo, i.value.trim()]));

async function renderLeads() {
  LEADS = await api('GET', '/api/leads');
  $('#aba-leads').innerHTML = `<div class="grade2">
    <div class="card"><h2>➕ Cadastrar lead</h2><div id="novo-lead">${formLead()}</div>
      <div class="linha" style="margin-top:12px"><button class="b prim" id="btn-novo">Salvar lead</button><span class="suave peq">Precisa de WhatsApp ou e-mail (ou os dois).</span></div></div>
    <div class="card"><h2>📥 Importar planilha</h2>
      <p class="suave peq" style="margin-top:0">CSV do Excel (vírgula ou ponto e vírgula). Colunas: <span class="mono">nome, escritorio, whatsapp, email, cidade, uf, dor, origem, obs</span>. Repetidos são ignorados.</p>
      <input type="file" id="arq" accept=".csv,.txt">
      <label>Ou cole aqui</label><textarea id="colar" rows="4" placeholder="nome;escritorio;whatsapp;email&#10;Marcos;Contabilidade Silva;48999990000;marcos@silva.com.br"></textarea>
      <div class="linha" style="margin-top:8px"><button class="b prim" id="btn-importar">Importar</button><button class="b mini" id="btn-modelo">Baixar planilha modelo</button></div></div></div>
    <div class="card" style="margin-top:14px"><div class="linha entre"><h2>${LEADS.length} leads</h2><a class="b mini" href="/api/leads/exportar">Exportar CSV</a></div>
      <div class="linha" style="margin:8px 0"><input id="busca" placeholder="Buscar nome, escritório, cidade, número ou e-mail" style="flex:1;min-width:220px" value="${esc(filtro.busca)}">
      <select id="fstatus" style="width:auto"><option value="">Todas as situações</option>${Object.entries(STATUS).map(([k, v]) => `<option value="${k}" ${filtro.status === k ? 'selected' : ''}>${v}</option>`).join('')}</select></div>
      <div class="rolagem"><table class="tabela"><thead><tr><th>Contato</th><th>WhatsApp</th><th>E-mail</th><th>Dor</th><th>Situação</th><th>Canais</th><th></th></tr></thead><tbody id="tb"></tbody></table></div></div>`;
  pintarLeads();
}
function canais(l) {
  const wa = { novo: '', abertura: '<span class="tag">📱 abertura</span>', followup: '<span class="tag">📱 follow-up</span>', sem_whatsapp: '<span class="tag laranja">📵 sem WhatsApp</span>' }[l.wa?.estado] || '';
  const em = l.em?.estado === 'devolvido' ? '<span class="tag laranja">✉️ devolvido</span>' : l.em?.etapa ? `<span class="tag">✉️ ${l.em.etapa}/3</span>` : '';
  return wa + ' ' + em;
}
function pintarLeads() {
  const b = filtro.busca.toLowerCase();
  const lista = LEADS.filter(l => (!filtro.status || l.status === filtro.status) && (!b || [l.nome, l.escritorio, l.cidade, l.whatsapp, l.email].join(' ').toLowerCase().includes(b)));
  $('#tb').innerHTML = lista.slice(0, 400).map(l => `<tr data-id="${l.id}">
    <td>${l.naoLida ? '<span class="nova"></span>' : ''}<b>${esc(l.nome || '—')}</b><div class="suave peq">${esc(l.escritorio)}${l.cidade ? ' · ' + esc(l.cidade) : ''}</div></td>
    <td class="mono">${esc(M.foneBonito(l.whatsapp))}</td><td class="peq">${esc(l.email)}</td>
    <td class="peq">${l.dor ? esc(M.DORES[l.dor].titulo) : '<span class="suave">sorteio</span>'}</td>
    <td><select data-status>${Object.entries(STATUS).map(([k, v]) => `<option value="${k}" ${k === l.status ? 'selected' : ''}>${v}</option>`).join('')}</select></td>
    <td>${canais(l)}</td>
    <td class="linha" style="flex-wrap:nowrap"><button class="b mini" data-ver>Conversa</button><button class="b mini" data-editar>✎</button><button class="b mini perigo" data-apagar>✕</button></td></tr>`).join('')
    + (lista.length > 400 ? `<tr><td colspan="7" class="suave">Mostrando 400 de ${lista.length}. Use a busca.</td></tr>` : '')
    + (!lista.length ? '<tr><td colspan="7" class="suave">Nenhum lead aqui.</td></tr>' : '');
}
$('#aba-leads').addEventListener('input', e => { if (e.target.id === 'busca') { filtro.busca = e.target.value; pintarLeads(); } });
$('#aba-leads').addEventListener('change', async e => {
  if (e.target.id === 'fstatus') { filtro.status = e.target.value; return pintarLeads(); }
  if (e.target.id === 'arq') {
    const f = e.target.files[0]; if (!f) return;
    const buf = await f.arrayBuffer(); let txt = new TextDecoder('utf-8').decode(buf);
    if (txt.includes('�')) txt = new TextDecoder('windows-1252').decode(buf); // Excel antigo salva em ANSI
    return importarTexto(txt);
  }
  if (e.target.matches('[data-status]')) {
    const id = e.target.closest('tr').dataset.id;
    await acao(() => api('PUT', '/api/leads/' + id, { status: e.target.value }), 'Situação atualizada');
    LEADS.find(l => l.id === id).status = e.target.value;
  }
});
async function importarTexto(txt) {
  const r = await acao(() => api('POST', '/api/leads/importar', { texto: txt }), r => `${r.novos} importados · ${r.repetidos} repetidos · ${r.invalidos} sem WhatsApp/e-mail válido`);
  if (r) renderLeads();
}
$('#aba-leads').addEventListener('click', async e => {
  const t = e.target;
  if (t.id === 'btn-novo') {
    if (await acao(() => api('POST', '/api/leads', lerForm($('#novo-lead'))), 'Lead salvo ✓')) renderLeads();
    return;
  }
  if (t.id === 'btn-importar') { const txt = $('#colar').value.trim(); if (txt) importarTexto(txt); return; }
  if (t.id === 'btn-modelo') {
    const csv = '﻿nome;escritorio;whatsapp;email;cidade;uf;dor;origem;obs\r\nMarcos Silva;Contabilidade Exemplo;(48) 99999-0001;marcos@exemplo.com.br;Florianópolis;SC;NFC-e;Google Maps;Muitos clientes de varejo\r\n';
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' })); a.download = 'planilha_modelo_leads.csv'; a.click();
    return;
  }
  const tr = t.closest('tr[data-id]'); if (!tr) return;
  const id = tr.dataset.id, l = LEADS.find(x => x.id === id);
  if (t.matches('[data-ver]')) return abrirConversa(id);
  if (t.matches('[data-apagar]') && confirm(`Apagar ${l.nome || l.escritorio || 'este lead'}? O histórico dele some.`)) {
    if (await acao(() => api('DELETE', '/api/leads/' + id), 'Apagado')) renderLeads();
  }
  if (t.matches('[data-editar]')) {
    abrirModal(`<div class="linha entre"><h2 style="margin:0">Editar lead</h2><button class="b mini" data-fechar>✕</button></div><div id="edita">${formLead(l)}</div>
      <div class="linha" style="margin-top:12px"><button class="b prim" id="btn-salva-edicao">Salvar</button></div>`);
    $('#btn-salva-edicao').onclick = async () => { if (await acao(() => api('PUT', '/api/leads/' + id, lerForm($('#edita'))), 'Salvo ✓')) { fecharModal(); renderLeads(); } };
  }
});

// ================================================================== MENSAGENS
let mensagensAlteradas = false, subMsg = 'whatsapp', rascunho = null;
const D = a => M.DORES[a].titulo;
function secoes() {
  const porDor = (canal, chave, titulo, ajuda) => M.ANGULOS.map(a => ({ canal, caminho: [chave, a], titulo: `${titulo} · ${D(a)}`, ajuda }));
  return {
    whatsapp: [
      { canal: 'whatsapp', caminho: ['saudacoes'], titulo: 'Saudação', ajuda: 'Primeira linha. Tenha variações com e sem {nome}.' },
      { canal: 'whatsapp', caminho: ['apresentacoes'], titulo: 'Apresentação', ajuda: 'Quem é você. Use {seu_nome} e {empresa}.' },
      { canal: 'whatsapp', caminho: ['contextos'], titulo: 'Contexto (entra em ~45% das mensagens)', ajuda: 'Como achou o escritório. Não escreva "o {escritorio}": o nome pode ser masculino ou feminino.' },
      ...porDor('whatsapp', 'ganchos', 'Pergunta-gancho', 'O coração da mensagem: termine com uma pergunta fácil de responder.'),
      ...porDor('whatsapp', 'pontes', 'Frase de valor (entra em ~35%)', 'Uma frase curta sobre o que o sistema faz.'),
      { canal: 'whatsapp', caminho: ['fechamentos'], titulo: 'Fechamento / saída fácil (entra em ~60%)', ajuda: 'Dar a opção de dizer "não" reduz denúncia.' },
      { canal: 'whatsapp', caminho: ['ola_audio'], titulo: 'Olá (modo olá + áudio)', ajuda: 'Mensagem curta que vai antes do áudio.' },
      { canal: 'whatsapp', caminho: ['followups'], titulo: 'Follow-up (1 só, para quem não respondeu)', ajuda: '{dor} vira "as NFC-e dos clientes", "a demora para pegar nota na SEFAZ"…' },
      ...porDor('whatsapp', 'roteiros_audio', 'Roteiro para gravar', 'Aparece na aba Áudios. Não use {nome}: o mesmo áudio vai para várias pessoas.')
    ],
    email: [
      ...porDor('email', 'assuntos', 'Assunto', 'Curto (2 a 6 palavras), sem "grátis", "oferta", "R$" ou "!!!".'),
      { canal: 'email', caminho: ['saudacoes'], titulo: 'Saudação', ajuda: 'Primeira linha do e-mail.' },
      ...porDor('email', 'aberturas', 'Corpo do 1º e-mail', 'Texto puro, 60 a 130 palavras, sem link. Termine com pergunta.'),
      { canal: 'email', caminho: ['followup_1'], titulo: '2º e-mail (mesma conversa, "Re:")', ajuda: 'Complementa o primeiro.' },
      { canal: 'email', caminho: ['followup_2'], titulo: '3º e-mail (despedida)', ajuda: '{dor} vira "NFC-e dos clientes", "notas na SEFAZ"… (sem artigo).' },
      { canal: 'email', caminho: ['assinatura'], titulo: 'Assinatura', ajuda: 'Use {seu_nome}, {empresa} e {whatsapp}.', unico: true },
      { canal: 'email', caminho: ['rodape_optout'], titulo: 'Rodapé de descadastro', ajuda: 'Obrigatório: a saída fácil evita denúncia de spam.' }
    ]
  };
}
const pegar = (canal, caminho) => caminho.reduce((o, k) => o?.[k], rascunho[canal]);
function definir(canal, caminho, valor) { let o = rascunho[canal]; caminho.slice(0, -1).forEach(k => { o = o[k] ||= {}; }); o[caminho.at(-1)] = valor; }
const linhasTxt = t => Math.min(10, Math.max(1, Math.ceil(t.length / 95) + (t.match(/\n/g) || []).length));

async function renderMensagens() {
  [MSG, CFG] = await Promise.all([api('GET', '/api/mensagens'), api('GET', '/api/config')]);
  rascunho = structuredClone(MSG); mensagensAlteradas = false;
  pintarMensagens();
}
function pintarMensagens() {
  const el = $('#aba-mensagens');
  let corpo = '';
  if (subMsg === 'respostas') {
    corpo = `<div class="card"><p class="suave peq" style="margin-top:0">Aparecem na conversa de cada lead (botão "Respostas prontas"). Aqui pode usar link: a pessoa já respondeu.</p>
      <div id="lista-resp">${rascunho.respostas.map((r, i) => `<div class="card" style="margin:8px 0;padding:12px" data-resp="${i}">
        <div class="linha" style="flex-wrap:nowrap"><input data-r="titulo" value="${esc(r.titulo)}" placeholder="Título"><button class="b mini perigo" data-del-resp="${i}">✕</button></div>
        <textarea data-r="texto" rows="${linhasTxt(r.texto)}" style="margin-top:6px">${esc(r.texto)}</textarea></div>`).join('')}</div>
      <button class="b mini" id="add-resp">+ Adicionar resposta</button></div>`;
  } else {
    corpo = `<div class="aviso info peq"><b>Como funciona:</b> cada envio sorteia uma variação de cada parte. <span class="mono">{nome}</span>, <span class="mono">{escritorio}</span>, <span class="mono">{cidade}</span>, <span class="mono">{seu_nome}</span>, <span class="mono">{empresa}</span>, <span class="mono">{periodo}</span> (Bom dia/Boa tarde) viram os dados.
      <span class="mono">[opção 1|opção 2]</span> sorteia uma das opções dentro da frase. Se o lead não tem um dado (ex.: sem cidade), a frase que usa esse dado é trocada por outra. Mais variações = menos chance de bloqueio.</div>
      <div class="card"><div class="linha entre"><b>Ver como as mensagens saem</b><button class="b mini" id="exemplos">Gerar exemplos (um por dor)</button></div><div id="saida-exemplos"></div></div>
      ${secoes()[subMsg].map((s, si) => {
        const v = pegar(s.canal, s.caminho);
        return `<details class="secao" ${si < 2 ? 'open' : ''}><summary>${esc(s.titulo)} <span class="suave peq">${s.unico ? '' : (v || []).length + ' variações'}</span></summary><div class="corpo">
          <p class="suave peq" style="margin:0 0 6px">${esc(s.ajuda)}</p>
          ${s.unico ? `<textarea data-sec="${si}" data-unico rows="4">${esc(v)}</textarea>`
            : `<div data-lista="${si}">${(v || []).map((t, i) => `<div class="variacao"><textarea data-sec="${si}" data-i="${i}" rows="${linhasTxt(t)}">${esc(t)}</textarea><button class="b mini perigo" data-del="${si}:${i}" title="Apagar">✕</button></div>`).join('')}</div>
               <button class="b mini" data-add="${si}">+ Adicionar variação</button>`}
        </div></details>`;
      }).join('')}`;
  }
  el.innerHTML = `<div class="subnav">${[['whatsapp', '📱 WhatsApp'], ['email', '✉️ E-mail'], ['respostas', '💬 Respostas prontas']].map(([k, v]) => `<button data-sub="${k}" class="${subMsg === k ? 'ativo' : ''}">${v}</button>`).join('')}</div>
    ${corpo}
    <div class="barra-salvar"><button class="b prim" id="salvar-msg">Salvar mensagens</button><span id="status-msg" class="suave peq">${mensagensAlteradas ? 'Alterações não salvas' : 'Tudo salvo'}</span>
    <span style="flex:1"></span><button class="b mini" id="restaurar-msg">Restaurar padrão</button></div>`;
}
function marcarAlterado() { mensagensAlteradas = true; const s = $('#status-msg'); if (s) { s.textContent = 'Alterações não salvas'; s.style.color = 'var(--alerta)'; } }
$('#aba-mensagens').addEventListener('input', e => {
  const t = e.target, S = secoes()[subMsg];
  if (t.dataset.sec !== undefined) {
    const s = S[t.dataset.sec];
    if (t.hasAttribute('data-unico')) definir(s.canal, s.caminho, t.value);
    else pegar(s.canal, s.caminho)[t.dataset.i] = t.value;
    marcarAlterado();
  }
  if (t.dataset.r) { rascunho.respostas[t.closest('[data-resp]').dataset.resp][t.dataset.r] = t.value; marcarAlterado(); }
});
$('#aba-mensagens').addEventListener('click', async e => {
  const t = e.target, S = subMsg === 'respostas' ? [] : secoes()[subMsg];
  if (t.dataset.sub) { subMsg = t.dataset.sub; return pintarMensagens(); }
  if (t.dataset.add !== undefined) {
    const s = S[t.dataset.add]; const lista = pegar(s.canal, s.caminho) || []; lista.push(''); definir(s.canal, s.caminho, lista);
    marcarAlterado(); pintarMensagens();
    const caixas = $$(`[data-lista="${t.dataset.add}"] textarea`); caixas.at(-1)?.closest('details')?.setAttribute('open', ''); caixas.at(-1)?.focus();
    return;
  }
  if (t.dataset.del) {
    const [si, i] = t.dataset.del.split(':').map(Number), s = S[si], lista = pegar(s.canal, s.caminho);
    if (lista.length <= 1) return toast('Deixe pelo menos uma variação.', true);
    lista.splice(i, 1); marcarAlterado(); pintarMensagens(); $$('details.secao')[si]?.setAttribute('open', ''); return;
  }
  if (t.id === 'add-resp') { rascunho.respostas.push({ titulo: '', texto: '' }); marcarAlterado(); return pintarMensagens(); }
  if (t.dataset.delResp !== undefined) { rascunho.respostas.splice(Number(t.dataset.delResp), 1); marcarAlterado(); return pintarMensagens(); }
  if (t.id === 'exemplos') {
    const lead = { nome: 'Marcos Silva', escritorio: 'Contabilidade Exemplo', cidade: 'Joinville' };
    $('#saida-exemplos').innerHTML = M.ANGULOS.map(a => {
      const ctx = M.contexto(lead, CFG, subMsg, a);
      if (subMsg === 'whatsapp') {
        return `<h3>${D(a)}</h3><div class="exemplo">${esc(M.aberturaWhatsApp(rascunho.whatsapp, ctx, a))}</div>`;
      }
      const r = M.emailEtapa(rascunho.email, ctx, 0, a);
      return `<h3>${D(a)}</h3><div class="exemplo"><b>Assunto: ${esc(r.assunto)}</b>\n\n${esc(r.corpo)}</div>`;
    }).join('') + (subMsg === 'whatsapp' ? `<h3>Follow-up</h3><div class="exemplo">${esc(M.followupWhatsApp(rascunho.whatsapp, M.contexto(lead, CFG, 'whatsapp', 'nfce')))}</div>` : '')
      + (CFG.seuNome ? '' : '<div class="aviso">Coloque seu nome em Configurações para ele aparecer nas mensagens.</div>');
    return;
  }
  if (t.id === 'salvar-msg') {
    const r = await acao(() => api('PUT', '/api/mensagens', rascunho), 'Mensagens salvas ✓');
    if (r) { MSG = r; rascunho = structuredClone(r); mensagensAlteradas = false; pintarMensagens(); }
    return;
  }
  if (t.id === 'restaurar-msg' && confirm('Voltar todas as mensagens para o padrão? O que você editou será perdido.')) {
    const r = await acao(() => api('POST', '/api/mensagens/restaurar'), 'Mensagens restauradas');
    if (r) { MSG = r; rascunho = structuredClone(r); mensagensAlteradas = false; pintarMensagens(); }
  }
});
window.addEventListener('beforeunload', e => { if (mensagensAlteradas) { e.preventDefault(); e.returnValue = ''; } });

// ================================================================== ÁUDIOS
let gravador = null, gravacao = null, roteiroDor = 'geral';
async function renderAudios() {
  [AUDIOS, MSG, CFG] = await Promise.all([api('GET', '/api/audios'), api('GET', '/api/mensagens'), api('GET', '/api/config')]);
  $('#aba-audios').innerHTML = `<div class="grade2">
    <div class="card"><h2>🎤 Gravar áudio</h2>
      <p class="suave peq" style="margin-top:0">No modo <b>olá + áudio</b>, o sistema manda o olá com o nome da pessoa e, de 20 s a 1 min depois, o seu áudio <b>como mensagem de voz</b> (não aparece "encaminhada"). Grave de 2 a 3 versões por dor: o sistema reveza.</p>
      <label>Roteiro (leia em voz natural, 30 a 45 s)</label>
      <div class="linha"><select id="rot-dor" style="width:auto">${M.ANGULOS.map(a => `<option value="${a}" ${a === roteiroDor ? 'selected' : ''}>${D(a)}</option>`).join('')}</select><button class="b mini" id="outro-rot">🔄 Outro roteiro</button></div>
      <div class="roteiro" id="roteiro" style="margin-top:8px"></div>
      <div class="linha" style="margin-top:14px"><button class="b prim grande" id="gravar">● Gravar</button><span class="timer" id="timer"></span></div>
      <div id="pos-gravacao"></div>
      <h3>Ou envie um arquivo</h3>
      <p class="suave peq" style="margin:0 0 6px">.ogg ou .opus (mensagem de voz). Dica: grave no WhatsApp para você mesmo, baixe pelo WhatsApp Web e envie aqui.</p>
      <input type="file" id="arq-audio" accept=".ogg,.opus,.oga,.webm,audio/ogg,audio/webm"></div>
    <div class="card"><h2>Seus áudios (${AUDIOS.length})</h2><div id="lista-audios"></div>
      <h3>Dicas para gravar</h3><ul class="regras peq">
        <li>Lugar silencioso, celular/microfone a um palmo da boca. Em pé e sorrindo: muda o tom de voz.</li>
        <li>Fale como numa ligação. O roteiro é um guia, não precisa ser palavra por palavra.</li>
        <li>Não diga o nome da pessoa no áudio (o mesmo áudio vai para várias): o nome já vai no olá.</li>
        <li>Termine com uma pergunta ("como vocês fazem hoje?"). É o que faz a pessoa responder.</li></ul></div></div>`;
  mostrarRoteiro(); pintarAudios();
}
function mostrarRoteiro() {
  const ctx = M.contexto({}, CFG, 'whatsapp', roteiroDor);
  $('#roteiro').textContent = M.roteiroAudio(MSG.whatsapp, ctx, roteiroDor) || 'Sem roteiro para esta dor (adicione em Mensagens › WhatsApp).';
}
function pintarAudios() {
  $('#lista-audios').innerHTML = AUDIOS.length ? AUDIOS.map(a => `<div class="audio-item" data-audio="${a.id}">
      <div style="min-width:0"><input value="${esc(a.nome)}" data-nome-audio style="margin-bottom:6px"><audio controls preload="none" src="/api/audios/${a.id}/arquivo"></audio>
      <div class="suave peq">${a.segundos}s · enviado ${a.usos || 0}x</div></div>
      <div style="display:grid;gap:6px"><select data-dor-audio>${M.ANGULOS.map(d => `<option value="${d}" ${a.dor === d ? 'selected' : ''}>${D(d)}</option>`).join('')}</select>
      <button class="b mini perigo" data-del-audio>Apagar</button></div></div>`).join('')
    : '<p class="suave">Nenhum áudio ainda. Sem áudio, o modo olá + áudio envia em texto.</p>';
}
async function ondaEDuracao(blob) {
  const ac = new AudioContext(), buf = await ac.decodeAudioData(await blob.arrayBuffer());
  const dados = buf.getChannelData(0), n = 64, passo = Math.floor(dados.length / n), picos = [];
  for (let i = 0; i < n; i++) { let m = 0; for (let j = i * passo; j < (i + 1) * passo; j++) m = Math.max(m, Math.abs(dados[j])); picos.push(m); }
  const max = Math.max(...picos, 0.01);
  ac.close();
  return { segundos: Math.max(1, Math.round(buf.duration)), waveform: btoa(String.fromCharCode(...picos.map(p => Math.round(100 * p / max)))) };
}
async function salvarAudio(blob, nome, dor) {
  let info = { segundos: 0, waveform: '' };
  try { info = await ondaEDuracao(blob); } catch { /* o servidor calcula a duração */ }
  const r = await acao(() => api('POST', '/api/audios', blob, { 'x-nome': encodeURIComponent(nome || 'Áudio'), 'x-dor': dor, 'x-segundos': String(info.segundos), 'x-waveform': info.waveform }), 'Áudio salvo ✓');
  if (r) renderAudios();
}
$('#aba-audios').addEventListener('click', async e => {
  const t = e.target;
  if (t.id === 'outro-rot') return mostrarRoteiro();
  if (t.id === 'gravar') {
    if (gravador) { gravador.stop(); return; }
    let stream;
    try { stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } }); }
    catch { return toast('Não consegui usar o microfone. Permita o acesso no navegador (ícone de cadeado na barra de endereço).', true); }
    const tipo = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') ? 'audio/webm;codecs=opus' : MediaRecorder.isTypeSupported('audio/ogg;codecs=opus') ? 'audio/ogg;codecs=opus' : '';
    if (!tipo) return toast('Este navegador não grava em Opus. Use Chrome, Edge ou Firefox.', true);
    const partes = []; gravador = new MediaRecorder(stream, { mimeType: tipo, audioBitsPerSecond: 32000 });
    gravador.ondataavailable = ev => partes.push(ev.data);
    const inicio = Date.now(), tick = setInterval(() => { const s = Math.floor((Date.now() - inicio) / 1000); $('#timer').textContent = `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`; if (s >= 120) gravador?.stop(); }, 250);
    gravador.onstop = () => {
      clearInterval(tick); stream.getTracks().forEach(x => x.stop()); gravador = null;
      t.textContent = '● Gravar de novo'; t.classList.remove('gravando');
      gravacao = new Blob(partes, { type: tipo.split(';')[0] });
      $('#pos-gravacao').innerHTML = `<div class="card" style="margin:12px 0 0;padding:12px"><audio controls src="${URL.createObjectURL(gravacao)}" style="width:100%"></audio>
        <div class="form"><div><label>Nome do áudio</label><input id="nome-grav" value="${esc(D(roteiroDor))} ${AUDIOS.filter(a => a.dor === roteiroDor).length + 1}"></div>
        <div><label>Usar para a dor</label><select id="dor-grav">${M.ANGULOS.map(a => `<option value="${a}" ${a === roteiroDor ? 'selected' : ''}>${D(a)}</option>`).join('')}</select></div></div>
        <div class="linha" style="margin-top:10px"><button class="b prim" id="salvar-grav">Salvar áudio</button><button class="b" id="descartar-grav">Descartar</button></div></div>`;
    };
    gravador.start(); t.textContent = '■ Parar'; t.classList.add('gravando'); $('#pos-gravacao').innerHTML = '';
    return;
  }
  if (t.id === 'salvar-grav' && gravacao) { t.disabled = true; await salvarAudio(gravacao, $('#nome-grav').value, $('#dor-grav').value); gravacao = null; return; }
  if (t.id === 'descartar-grav') { gravacao = null; $('#pos-gravacao').innerHTML = ''; $('#timer').textContent = ''; return; }
  if (t.matches('[data-del-audio]')) {
    const id = t.closest('[data-audio]').dataset.audio;
    if (confirm('Apagar este áudio?') && await acao(() => api('DELETE', '/api/audios/' + id), 'Apagado')) renderAudios();
  }
});
$('#aba-audios').addEventListener('change', async e => {
  const t = e.target;
  if (t.id === 'rot-dor') { roteiroDor = t.value; return mostrarRoteiro(); }
  if (t.id === 'arq-audio' && t.files[0]) return salvarAudio(t.files[0], t.files[0].name.replace(/\.\w+$/, ''), roteiroDor);
  const item = t.closest('[data-audio]'); if (!item) return;
  if (t.matches('[data-dor-audio]')) await acao(() => api('PUT', '/api/audios/' + item.dataset.audio, { dor: t.value }), 'Atualizado');
  if (t.matches('[data-nome-audio]')) await acao(() => api('PUT', '/api/audios/' + item.dataset.audio, { nome: t.value }), 'Atualizado');
});

// ================================================================== CONFIGURAÇÕES
const PRESETS = {
  'Gmail / Google Workspace': { smtpHost: 'smtp.gmail.com', smtpPorta: 587, imapHost: 'imap.gmail.com', imapPorta: 993 },
  'Outlook / Microsoft 365': { smtpHost: 'smtp.office365.com', smtpPorta: 587, imapHost: 'outlook.office365.com', imapPorta: 993 },
  'Zoho': { smtpHost: 'smtp.zoho.com', smtpPorta: 587, imapHost: 'imap.zoho.com', imapPorta: 993 },
  'Hostinger': { smtpHost: 'smtp.hostinger.com', smtpPorta: 465, imapHost: 'imap.hostinger.com', imapPorta: 993 },
  'Locaweb': { smtpHost: 'email-ssl.com.br', smtpPorta: 465, imapHost: 'email-ssl.com.br', imapPorta: 993 }
};
const GRUPOS = [
  ['👤 Meus dados', [['seuNome', 'Seu nome', 'texto', 'Entra nas mensagens: "Aqui é Ana, da Epiverso".'], ['empresa', 'Empresa', 'texto'],
    ['whatsappAssinatura', 'WhatsApp na assinatura do e-mail', 'texto']]],
  ['🕘 Horário de envio (WhatsApp e e-mail)', [['horaInicio', 'Começa às (hora)', 'numero'], ['horaFim', 'Termina às (hora)', 'numero'],
    ['pausaAlmoco', 'Pausa de almoço (12h às 13h30)', 'check'], ['espalhar', 'Espalhar os envios ao longo do dia', 'check', 'Mais natural do que mandar tudo de manhã.'],
    ['diasEntreCanais', 'Dias úteis entre WhatsApp e e-mail para o mesmo lead', 'numero', 'Evita chegar pelos dois canais no mesmo dia.']]],
  ['📱 WhatsApp', [['waMeta', 'Meta diária (aberturas + follow-ups)', 'numero', 'Recomendado: 15. Chip novo: comece com 5.'],
    ['waIntervaloMin', 'Intervalo mínimo entre envios (minutos)', 'numero'], ['waIntervaloMax', 'Intervalo máximo (minutos)', 'numero', 'Usado quando "espalhar" está desligado.'],
    ['waModo', 'Abertura', 'select', '', { texto: 'Texto', ola_audio: 'Olá + áudio', misto: 'Misturar os dois' }],
    ['waPercentAudio', '% com áudio (no modo misturar)', 'numero'],
    ['waFollowup', 'Fazer 1 follow-up para quem não respondeu', 'check'], ['waDiasFollowup', 'Follow-up depois de (dias úteis)', 'numero']]],
  ['✉️ E-mail', [['emNome', 'Nome do remetente', 'texto', 'Vazio = seu nome.'], ['emEmail', 'E-mail remetente', 'texto', 'Use um domínio separado para prospecção (veja Como usar).'],
    ['smtpHost', 'Servidor SMTP', 'texto'], ['smtpPorta', 'Porta SMTP', 'numero', '587 ou 465.'], ['smtpUsuario', 'Usuário SMTP', 'texto', 'Vazio = o e-mail remetente.'],
    ['smtpSenha', 'Senha (no Gmail: senha de app)', 'senha'], ['imapAtivo', 'Ler a caixa de entrada para parar quem respondeu (IMAP)', 'check'],
    ['imapHost', 'Servidor IMAP', 'texto'], ['imapPorta', 'Porta IMAP', 'numero'], ['emLimiteMax', 'Limite diário depois do aquecimento', 'numero', 'Recomendado: 40 por caixa.'],
    ['emInicioAquecimento', 'Início do aquecimento', 'data', 'Vazio = começa no primeiro envio.'], ['emIntervaloMin', 'Intervalo mínimo (segundos)', 'numero'],
    ['emIntervaloMax', 'Intervalo máximo (segundos)', 'numero'], ['emDiasEtapa2', '2º e-mail depois de (dias úteis)', 'numero'], ['emDiasEtapa3', '3º e-mail depois de (dias úteis)', 'numero']]]
];
async function renderConfig() {
  CFG = await api('GET', '/api/config');
  const campo = ([k, rot, tipo, ajuda, opcoes]) => {
    const v = CFG[k];
    if (tipo === 'check') return `<div><label class="check"><input type="checkbox" data-cfg="${k}" ${v ? 'checked' : ''}>${rot}</label>${ajuda ? `<div class="ajuda">${ajuda}</div>` : ''}</div>`;
    const input = tipo === 'select' ? `<select data-cfg="${k}">${Object.entries(opcoes).map(([o, t]) => `<option value="${o}" ${o === v ? 'selected' : ''}>${t}</option>`).join('')}</select>`
      : `<input data-cfg="${k}" type="${{ numero: 'number', senha: 'password', data: 'date' }[tipo] || 'text'}" value="${tipo === 'senha' ? '' : esc(v)}" ${tipo === 'senha' && CFG.temSenha ? 'placeholder="•••••••• (salva; deixe vazio para manter)"' : ''} autocomplete="off">`;
    return `<div><label>${rot}</label>${input}${ajuda ? `<div class="ajuda">${ajuda}</div>` : ''}</div>`;
  };
  $('#aba-config').innerHTML = GRUPOS.map(([titulo, campos]) => `<div class="card"><h2>${titulo}</h2>
      ${titulo.includes('E-mail') ? `<div class="linha" style="margin:4px 0 2px"><span class="suave peq">Provedor:</span>${Object.keys(PRESETS).map(p => `<button class="b mini" data-preset="${p}">${p}</button>`).join('')}</div>` : ''}
      <div class="form">${campos.map(campo).join('')}</div>
      ${titulo.includes('E-mail') ? `<h3>Testar</h3><div class="linha"><input id="para-teste" placeholder="seu-email@gmail.com ou o endereço do mail-tester.com" style="max-width:360px"><button class="b mini" id="teste-email">Enviar e-mail de teste</button></div>
        <p class="ajuda">Salve antes de testar. Use o <a href="https://www.mail-tester.com" target="_blank" rel="noopener">mail-tester.com</a> e só comece com nota 9/10 ou mais.</p>` : ''}</div>`).join('')
    + '<div class="barra-salvar"><button class="b prim grande" id="salvar-cfg">Salvar configurações</button></div>';
}
$('#aba-config').addEventListener('click', async e => {
  const t = e.target;
  if (t.dataset.preset) { for (const [k, v] of Object.entries(PRESETS[t.dataset.preset])) $(`[data-cfg=${k}]`).value = v; return toast('Preenchido. Agora salve.'); }
  if (t.id === 'salvar-cfg') {
    const novo = Object.fromEntries($$('[data-cfg]').map(i => [i.dataset.cfg, i.type === 'checkbox' ? i.checked : i.value]));
    const r = await acao(() => api('PUT', '/api/config', novo), 'Configurações salvas ✓');
    if (r) { CFG = r; renderConfig(); atualizar(); }
  }
  if (t.id === 'teste-email') {
    const para = $('#para-teste').value.trim(); if (!para) return toast('Digite para onde mandar o teste.', true);
    t.disabled = true; await acao(() => api('POST', '/api/email/teste', { para }), r => `Enviado! Assunto: "${r.assunto}"`); t.disabled = false;
  }
});

// ================================================================== GUIA
function renderGuia() {
  $('#aba-guia').innerHTML = `<div class="grade2">
  <div class="card"><h2>🚀 Começando (uma vez só)</h2><ol class="passos">
    <li><b>Configurações › Meus dados:</b> seu nome e empresa.</li>
    <li><b>Início › Conectar WhatsApp:</b> escaneie o QR Code com o celular do número de prospecção.</li>
    <li><b>Leads:</b> cadastre um por um ou importe a planilha (WhatsApp e/ou e-mail).</li>
    <li><b>Áudios</b> (opcional): grave 2 ou 3 áudios por dor para o modo olá + áudio.</li>
    <li><b>Mensagens:</b> ajuste o texto do seu jeito e clique em "Gerar exemplos" para conferir.</li>
    <li><b>Configurações › E-mail:</b> preencha o servidor e a senha de app e mande um teste.</li>
    <li><b>Início › Ligar envios</b> (WhatsApp e e-mail). Deixe a janela preta do sistema aberta: ele envia sozinho nos dias úteis.</li></ol>
    <div class="aviso">O computador precisa estar ligado e com o sistema aberto no horário de envio. Fechou a janela, os envios param (e voltam quando abrir de novo).</div></div>
  <div class="card"><h2>📱 Para não tomar bloqueio no WhatsApp</h2><ul class="regras">
    <li><b>Use um número só para prospecção</b>, nunca o do suporte. Chip novo: use normalmente por 2 semanas antes e comece com meta 5.</li>
    <li>Perfil completo no WhatsApp Business: foto, nome "Ana · Epiverso", descrição e site.</li>
    <li>Até 15 conversas novas por dia, espalhadas, só em dias úteis e horário comercial (o sistema já faz isso).</li>
    <li>Primeira mensagem sem link, sem PDF, terminando com pergunta. Cada uma sai diferente.</li>
    <li>Um follow-up só. Quem responde sai da sequência na hora. Quem pede para sair nunca mais recebe.</li>
    <li>Responda rápido quem respondeu: conversa com ida e volta protege o número.</li>
    <li>Se a resposta cair abaixo de 10% ou o WhatsApp mostrar aviso de restrição: pause de 3 a 7 dias e volte com metade do volume.</li></ul>
    <div class="aviso">Conectar pelo QR usa o WhatsApp Web por baixo, sem a API oficial (paga). Funciona bem nesse volume, mas o WhatsApp pode restringir qualquer número que pareça disparo em massa. Por isso as regras acima importam.</div></div>
  <div class="card"><h2>✉️ Para o e-mail não cair no spam</h2><ul class="regras">
    <li><b>Domínio separado</b> para prospecção (ex.: epiversofiscal.com.br), com caixa de pessoa (ana@…).</li>
    <li>Configure <b>SPF, DKIM e DMARC</b> no DNS (no Google Workspace: Admin › Gmail › Autenticar e-mail). Confira em mxtoolbox.com.</li>
    <li>No Gmail, crie uma <b>senha de app</b> (Conta Google › Segurança › Senhas de app) e use ela aqui.</li>
    <li>Teste no mail-tester.com: só comece com 9/10 ou mais.</li>
    <li>O sistema aquece sozinho: 10 → 20 → 30 → 40 por dia, semana a semana. Texto puro, sem link, sem imagem, cada e-mail diferente.</li>
    <li>Quer mais de 40/dia? Use outra caixa de e-mail em outra pasta do sistema, com outra lista de leads.</li></ul></div>
  <div class="card"><h2>💾 Seus dados</h2><ul class="regras">
    <li>Tudo fica na pasta <span class="mono">dados</span> ao lado do INICIAR: leads, mensagens, áudios, configurações e a conexão do WhatsApp.</li>
    <li>Para fazer backup, copie a pasta <span class="mono">dados</span>. Para trocar de computador, leve ela junto.</li>
    <li>A conexão do WhatsApp fica nessa pasta: não compartilhe com ninguém.</li>
    <li>Atualizar o sistema: baixe o zip novo e copie a sua pasta <span class="mono">dados</span> para dentro dele.</li></ul></div></div>`;
}

// ================================================================== início
(async () => {
  [CFG, MSG] = await Promise.all([api('GET', '/api/config'), api('GET', '/api/mensagens')]).catch(() => [null, null]);
  renderInicio();
  await atualizar();
  setInterval(atualizar, 2000);
})();
