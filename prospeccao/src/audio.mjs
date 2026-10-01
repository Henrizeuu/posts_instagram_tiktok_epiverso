// Converte a gravação do navegador (WebM/Opus) para Ogg/Opus, o formato da mensagem de voz do WhatsApp.
// É só uma troca de "embalagem" (o áudio Opus não é recodificado), por isso não precisa de ffmpeg.

const ID = { EBML: 0x1a45dfa3, SEGMENT: 0x18538067, TRACKS: 0x1654ae6b, TRACK_ENTRY: 0xae, CODEC_ID: 0x86,
  CODEC_PRIVATE: 0x63a2, CLUSTER: 0x1f43b675, SIMPLE_BLOCK: 0xa3, BLOCK_GROUP: 0xa0, BLOCK: 0xa1 };
const CONTAINERS = new Set([ID.SEGMENT, ID.TRACKS, ID.TRACK_ENTRY, ID.CLUSTER, ID.BLOCK_GROUP]);

function lerVint(buf, pos, manterMarcador) {
  const b = buf[pos];
  if (b === undefined) return null;
  let tam = 1, mascara = 0x80;
  while (tam <= 8 && !(b & mascara)) { tam++; mascara >>= 1; }
  if (tam > 8 || pos + tam > buf.length) return null;
  let valor = manterMarcador ? b : b & (mascara - 1), todosUm = (b & (mascara - 1)) === mascara - 1;
  for (let i = 1; i < tam; i++) { valor = valor * 256 + buf[pos + i]; if (buf[pos + i] !== 0xff) todosUm = false; }
  return { valor, tam, desconhecido: !manterMarcador && todosUm };
}

/** Amostras (a 48 kHz) de um pacote Opus, pelo byte TOC (RFC 6716, seção 3.1). */
export function amostrasOpus(pacote) {
  if (!pacote.length) return 0;
  const toc = pacote[0], config = toc >> 3;
  const ms = config < 12 ? [10, 20, 40, 60][config % 4] : config < 16 ? [10, 20][config % 2] : [2.5, 5, 10, 20][config % 4];
  const codigo = toc & 3;
  const quadros = codigo === 0 ? 1 : codigo < 3 ? 2 : (pacote[1] || 0) & 0x3f;
  return Math.round(ms * 48) * quadros;
}

function extrairWebm(buf) {
  let pos = 0, codecPrivate = null, codec = '';
  const pacotes = [];
  while (pos < buf.length) {
    const id = lerVint(buf, pos, true); if (!id) break;
    const tam = lerVint(buf, pos + id.tam, false); if (!tam) break;
    const ini = pos + id.tam + tam.tam;
    if (CONTAINERS.has(id.valor)) { pos = ini; continue; } // desce no elemento (tamanho conhecido ou não)
    const fim = tam.desconhecido ? buf.length : Math.min(buf.length, ini + tam.valor);
    if (id.valor === ID.CODEC_ID) codec = buf.subarray(ini, fim).toString('latin1');
    else if (id.valor === ID.CODEC_PRIVATE) codecPrivate = Buffer.from(buf.subarray(ini, fim));
    else if (id.valor === ID.SIMPLE_BLOCK || id.valor === ID.BLOCK) {
      const trilha = lerVint(buf, ini, false);
      const flags = buf[ini + trilha.tam + 2];
      if (flags & 0x06) throw new Error('Gravação com "lacing" não suportada.');
      pacotes.push(Buffer.from(buf.subarray(ini + trilha.tam + 3, fim)));
    }
    pos = fim;
  }
  if (codec && codec !== 'A_OPUS') throw new Error(`O áudio não é Opus (${codec}).`);
  if (!pacotes.length) throw new Error('Não encontrei áudio na gravação.');
  return { codecPrivate, pacotes };
}

// CRC do Ogg (polinômio 0x04c11db7, sem reflexão)
const TABELA_CRC = new Uint32Array(256).map((_, i) => {
  let r = i << 24;
  for (let j = 0; j < 8; j++) r = r & 0x80000000 ? ((r << 1) ^ 0x04c11db7) >>> 0 : (r << 1) >>> 0;
  return r >>> 0;
});
function crcOgg(buf) {
  let crc = 0;
  for (const b of buf) crc = ((crc << 8) ^ TABELA_CRC[((crc >>> 24) ^ b) & 0xff]) >>> 0;
  return crc >>> 0;
}

function paginaOgg(pacotes, { granulo, serial, seq, tipo }) {
  const lacing = [];
  for (const p of pacotes) {
    let n = p.length;
    while (n >= 255) { lacing.push(255); n -= 255; }
    lacing.push(n);
  }
  const cab = Buffer.alloc(27 + lacing.length);
  cab.write('OggS', 0, 'latin1');
  cab[4] = 0; cab[5] = tipo;
  cab.writeBigInt64LE(BigInt(granulo), 6);
  cab.writeUInt32LE(serial, 14); cab.writeUInt32LE(seq, 18); cab.writeUInt32LE(0, 22);
  cab[26] = lacing.length; Buffer.from(lacing).copy(cab, 27);
  const pagina = Buffer.concat([cab, ...pacotes]);
  pagina.writeUInt32LE(crcOgg(pagina), 22);
  return pagina;
}

export function webmParaOgg(webm) {
  const { codecPrivate, pacotes } = extrairWebm(webm);
  let head = codecPrivate && codecPrivate.subarray(0, 8).toString('latin1') === 'OpusHead' ? codecPrivate : null;
  if (!head) { // cabeçalho padrão: mono, 48 kHz
    head = Buffer.alloc(19); head.write('OpusHead', 0, 'latin1'); head[8] = 1; head[9] = 1;
    head.writeUInt16LE(312, 10); head.writeUInt32LE(48000, 12);
  }
  const vendor = Buffer.from('Epiverso');
  const tags = Buffer.alloc(8 + 4 + vendor.length + 4);
  tags.write('OpusTags', 0, 'latin1'); tags.writeUInt32LE(vendor.length, 8); vendor.copy(tags, 12);
  const serial = (Math.random() * 0xffffffff) >>> 0;
  const paginas = [paginaOgg([head], { granulo: 0, serial, seq: 0, tipo: 0x02 }), paginaOgg([tags], { granulo: 0, serial, seq: 1, tipo: 0 })];
  let seq = 2, granulo = 0, grupo = [], segs = 0;
  for (let i = 0; i < pacotes.length; i++) {
    const p = pacotes[i], s = Math.floor(p.length / 255) + 1;
    if (grupo.length && segs + s > 255) {
      paginas.push(paginaOgg(grupo, { granulo, serial, seq: seq++, tipo: 0 }));
      grupo = []; segs = 0;
    }
    grupo.push(p); segs += s; granulo += amostrasOpus(p);
  }
  paginas.push(paginaOgg(grupo, { granulo, serial, seq: seq++, tipo: 0x04 }));
  const preSkip = head.readUInt16LE(10);
  return { ogg: Buffer.concat(paginas), segundos: Math.max(1, Math.round((granulo - preSkip) / 48000)) };
}

/** Duração de um Ogg/Opus pelo granulo da última página. */
export function duracaoOgg(buf) {
  const i = buf.lastIndexOf(Buffer.from('OggS'));
  if (i < 0 || buf.subarray(28, 36).toString('latin1') !== 'OpusHead') return 0;
  const granulo = Number(buf.readBigInt64LE(i + 6)), preSkip = buf.readUInt16LE(28 + 10);
  return Math.max(1, Math.round((granulo - preSkip) / 48000));
}

export const ehOgg = buf => buf.subarray(0, 4).toString('latin1') === 'OggS';
export const ehWebm = buf => buf.length > 4 && buf.readUInt32BE(0) === ID.EBML;
