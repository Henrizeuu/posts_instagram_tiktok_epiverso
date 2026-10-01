// Motor de mensagens e utilitários de leads. Roda no servidor (envios) e no painel (prévias).
// {campo} vira o dado do lead; [a|b|c] sorteia uma opção. Opção com campo vazio é descartada.

export const ANGULOS = ['nfce', 'nfse', 'naocontrib', 'sefaz', 'geral'];
export const DORES = {
  nfce:       { titulo: 'NFC-e',              whatsapp: 'as NFC-e dos clientes',                  email: 'NFC-e dos clientes' },
  nfse:       { titulo: 'NFS-e',              whatsapp: 'as NFS-e dos clientes',                  email: 'NFS-e dos clientes' },
  naocontrib: { titulo: 'Não contribuintes',  whatsapp: 'as notas dos clientes não contribuintes', email: 'notas de clientes não contribuintes' },
  sefaz:      { titulo: 'Demora na SEFAZ',    whatsapp: 'a demora para pegar nota na SEFAZ',       email: 'notas na SEFAZ' },
  geral:      { titulo: 'Geral (as 4 dores)', whatsapp: 'as notas dos clientes',                  email: 'notas dos clientes' }
};

export const sortear = a => a[Math.floor(Math.random() * a.length)];
export function embaralhar(a) {
  a = a.slice();
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}

// ------------------------------------------------------------------ variações
export const camposOk = (t, ctx) => [...t.matchAll(/\{(\w+)\}/g)].every(m => ctx[m[1]]);

export function spin(t, ctx) {
  const re = /\[([^\[\]]*\|[^\[\]]*)\]/;
  for (let i = 0; i < 500 && re.test(t); i++) {
    t = t.replace(re, (_, dentro) => {
      const ops = dentro.split('|').filter(o => camposOk(o, ctx));
      return ops.length ? sortear(ops) : '';
    });
  }
  return t;
}

export const preencher = (t, ctx) => t.replace(/\{(\w+)\}/g, (_, c) => ctx[c] ?? '');

export function limpar(t) {
  return t.split('\n').map(l => l.replace(/[ \t]+/g, ' ').replace(/ ([,.?!:])/g, '$1').trim()).join('\n')
    .replace(/\n{3,}/g, '\n\n').trim();
}

export function escolher(lista, ctx) {
  for (const t of embaralhar((lista || []).filter(x => String(x).trim()))) {
    const r = spin(t, ctx);
    if (camposOk(r, ctx)) return preencher(r, ctx);
  }
  return '';
}

/** Se o lead tem nome, quase sempre usa uma variação com o nome. */
export function comNome(lista, ctx) {
  const com = (lista || []).filter(t => t.includes('{nome}'));
  return ctx.nome && com.length && Math.random() < 0.85 ? com : lista;
}

export function periodo(d = new Date()) {
  const h = d.getHours();
  return h < 12 ? 'Bom dia' : h < 18 ? 'Boa tarde' : 'Boa noite';
}

export function contexto(lead, cfg, canal, angulo, agora = new Date()) {
  const p = periodo(agora);
  return {
    nome: primeiroNome(lead.nome), escritorio: limparEscritorio(lead.escritorio), cidade: (lead.cidade || '').trim(),
    seu_nome: (cfg.seuNome || '').trim(), empresa: (cfg.empresa || '').trim() || 'Epiverso',
    whatsapp: (cfg.whatsappAssinatura || '').trim(), periodo: p, periodo_min: p.toLowerCase(),
    dor: DORES[angulo || 'geral'][canal === 'email' ? 'email' : 'whatsapp']
  };
}

// ------------------------------------------------------------------ WhatsApp
export function aberturaWhatsApp(m, ctx, angulo) {
  const sau = escolher(comNome(m.saudacoes, ctx), ctx), apr = escolher(m.apresentacoes, ctx);
  const ctxt = Math.random() < 0.45 ? escolher(m.contextos, ctx) : '';
  const gan = escolher(m.ganchos[angulo] || m.ganchos.geral, ctx);
  const pon = !ctxt && Math.random() < 0.35 ? escolher((m.pontes || {})[angulo] || [], ctx) : '';
  const fec = Math.random() < 0.6 ? escolher(m.fechamentos, ctx) : '';
  const corpo = [pon, gan].filter(Boolean).join(' ');
  const layouts = [
    () => `${sau} ${apr} ${ctxt}\n\n${corpo}\n\n${fec}`,
    () => `${sau}\n${apr} ${ctxt}\n\n${corpo} ${fec}`,
    () => `${sau} ${apr}\n\n${ctxt} ${corpo}\n\n${fec}`,
    () => `${sau}\n\n${apr} ${ctxt} ${corpo}`
  ];
  return limpar(sortear(layouts)());
}
export const olaWhatsApp = (m, ctx) => limpar(escolher(comNome(m.ola_audio, ctx), ctx));
export const followupWhatsApp = (m, ctx) => limpar(escolher(m.followups, ctx));
export const roteiroAudio = (m, ctx, angulo) => limpar(escolher((m.roteiros_audio || {})[angulo] || (m.roteiros_audio || {}).geral || [], ctx));

// ------------------------------------------------------------------ E-mail (etapa 0 = abertura, 1 e 2 = follow-ups)
export function emailEtapa(m, ctx, etapa, angulo) {
  let assunto = '', corpo;
  if (etapa === 0) {
    assunto = limpar(escolher(m.assuntos[angulo] || m.assuntos.geral, ctx));
    corpo = escolher(comNome(m.saudacoes, ctx), ctx) + '\n\n' + escolher(m.aberturas[angulo] || m.aberturas.geral, ctx);
  } else {
    corpo = escolher(etapa === 1 ? m.followup_1 : m.followup_2, ctx);
  }
  const rodape = escolher(m.rodape_optout, ctx);
  return { assunto, corpo: limpar(`${corpo}\n\n${preencher(m.assinatura || '', ctx)}\n\n${rodape}`) };
}

export function hashTexto(s) {
  let h = 5381;
  for (const c of String(s).replace(/\s+/g, ' ').trim().toLowerCase()) h = ((h << 5) + h + c.charCodeAt(0)) | 0;
  return (h >>> 0).toString(36);
}

// ------------------------------------------------------------------ leads
export const EMAIL_OK = /^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/;

export function normalizarFone(f) {
  let d = String(f || '').replace(/\D/g, '').replace(/^0+/, '');
  if (d.length === 10 || d.length === 11) d = '55' + d;
  return d;
}
export function tipoFone(d) {
  if (!/^55\d{10,11}$/.test(d || '')) return 'invalido';
  return d.length === 13 && d[4] === '9' ? 'celular' : 'fixo';
}
export function foneBonito(d) {
  const m = String(d || '').match(/^55(\d{2})(\d{4,5})(\d{4})$/);
  return m ? `(${m[1]}) ${m[2]}-${m[3]}` : (d || '');
}
const TITULOS = ['dr', 'dra', 'sr', 'sra', 'prof', 'profa'];
export function primeiroNome(n) {
  const p = String(n || '').trim().split(/\s+/).filter(Boolean);
  if (!p.length) return '';
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
  const t = p[0].replace('.', '').toLowerCase();
  return TITULOS.includes(t) && p[1] ? `${cap(t)}. ${cap(p[1])}` : cap(p[0]);
}
export function limparEscritorio(n) {
  return String(n || '').replace(/\b(ltda|me|epp|eireli|s\/s|ss|s\.s\.|s\/c|sociedade simples)\b\.?/gi, '')
    .replace(/[\s\-–,.]+$/, '').replace(/\s{2,}/g, ' ').trim();
}
export function normalizarDor(d) {
  d = String(d || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  if (ANGULOS.includes(d)) return d;
  if (/nfc/.test(d)) return 'nfce';
  if (/nfs|servico/.test(d)) return 'nfse';
  if (/contrib|\bie\b/.test(d)) return 'naocontrib';
  if (/sefaz|demora/.test(d)) return 'sefaz';
  if (/geral|todas/.test(d)) return 'geral';
  return '';
}

const ALIASES = {
  nome: ['nome', 'contato', 'responsavel', 'responsável', 'name'],
  escritorio: ['escritorio', 'escritório', 'empresa', 'razao social', 'razão social', 'nome fantasia', 'fantasia'],
  whatsapp: ['whatsapp', 'whats', 'celular', 'telefone', 'fone', 'tel', 'phone'],
  email: ['email', 'e-mail', 'mail'],
  cidade: ['cidade', 'municipio', 'município'], uf: ['uf', 'estado'],
  dor: ['dor', 'angulo', 'ângulo', 'foco'], origem: ['origem', 'fonte'], obs: ['obs', 'observacao', 'observação', 'notas']
};

/** Lê CSV (vírgula, ponto e vírgula ou tab) e devolve objetos com os campos conhecidos. */
export function lerCSV(texto) {
  texto = String(texto || '').replace(/^﻿/, '');
  const prim = texto.split('\n')[0] || '';
  const sep = (prim.match(/;/g) || []).length > (prim.match(/,/g) || []).length ? ';' : (prim.includes('\t') ? '\t' : ',');
  const linhas = []; let campo = '', linha = [], aspas = false;
  for (let i = 0; i < texto.length; i++) {
    const ch = texto[i];
    if (aspas) { if (ch === '"') { if (texto[i + 1] === '"') { campo += '"'; i++; } else aspas = false; } else campo += ch; }
    else if (ch === '"') aspas = true;
    else if (ch === sep) { linha.push(campo); campo = ''; }
    else if (ch === '\n' || ch === '\r') { if (ch === '\r' && texto[i + 1] === '\n') i++; linha.push(campo); linhas.push(linha); linha = []; campo = ''; }
    else campo += ch;
  }
  if (campo || linha.length) { linha.push(campo); linhas.push(linha); }
  const uteis = linhas.filter(l => l.some(c => c.trim()));
  if (uteis.length < 2) return [];
  const cab = uteis[0].map(c => c.trim().toLowerCase());
  const idx = {};
  for (const [k, al] of Object.entries(ALIASES)) idx[k] = cab.findIndex(c => al.includes(c));
  return uteis.slice(1).map(l => {
    const o = {};
    for (const k of Object.keys(ALIASES)) o[k] = idx[k] >= 0 ? (l[idx[k]] || '').trim() : '';
    return o;
  });
}
