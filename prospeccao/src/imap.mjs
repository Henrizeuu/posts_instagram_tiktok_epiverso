// Cliente IMAP mínimo: só faz login e buscas (SEARCH) na caixa de entrada, para saber
// quem respondeu e quais e-mails voltaram. Não baixa nem altera mensagens.
import tls from 'node:tls';
import net from 'node:net';

const MESES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
export const dataImap = iso => { const d = new Date(iso.slice(0, 10) + 'T12:00:00'); return `${d.getDate()}-${MESES[d.getMonth()]}-${d.getFullYear()}`; };
export const q = s => '"' + String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"';

/**
 * Executa várias buscas e devolve, para cada uma, a lista de ids encontrados.
 * @param {{host:string, porta:number, usuario:string, senha:string}} c
 * @param {string[]} buscas  critérios IMAP, ex.: `SINCE 1-Oct-2026 FROM "fulano@x.com"`
 */
export function imapBuscar(c, buscas) {
  return new Promise((resolve, reject) => {
    const opcoes = { host: c.host, port: c.porta, servername: c.host };
    const sock = process.env.EPIVERSO_IMAP_SEM_TLS ? net.connect(opcoes) : tls.connect(opcoes);
    sock.setTimeout(30000, () => { sock.destroy(); reject(new Error('IMAP: tempo esgotado')); });
    sock.on('error', reject);
    let buffer = '', n = 0, pendente = null, achados = [];
    const resultados = [];
    const comandos = [`LOGIN ${q(c.usuario)} ${q(c.senha)}`, 'EXAMINE INBOX', ...buscas.map(b => `SEARCH ${b}`), 'LOGOUT'];
    let idx = -1;
    const proximo = () => {
      idx++;
      if (idx >= comandos.length) return;
      pendente = `E${++n}`;
      achados = [];
      sock.write(`${pendente} ${comandos[idx]}\r\n`);
    };
    sock.on('data', d => {
      buffer += d.toString('utf8');
      let i;
      while ((i = buffer.indexOf('\r\n')) >= 0) {
        const linha = buffer.slice(0, i); buffer = buffer.slice(i + 2);
        if (pendente === null) { if (/^\* (OK|PREAUTH)/i.test(linha)) proximo(); else return reject(new Error('IMAP: ' + linha)); continue; }
        if (/^\* SEARCH/i.test(linha)) { achados.push(...linha.replace(/^\* SEARCH\s*/i, '').split(/\s+/).filter(Boolean)); continue; }
        if (linha.startsWith(pendente + ' ')) {
          const ok = /^\S+ OK/i.test(linha), cmd = comandos[idx];
          if (!ok && !cmd.startsWith('LOGOUT')) {
            sock.destroy();
            return reject(new Error(cmd.startsWith('LOGIN') ? 'IMAP: usuário ou senha recusados' : 'IMAP: ' + linha));
          }
          if (cmd.startsWith('SEARCH')) resultados.push(achados);
          if (cmd.startsWith('LOGOUT')) { sock.end(); return resolve(resultados); }
          proximo();
        }
      }
    });
    sock.on('close', () => { if (idx < comandos.length - 1) reject(new Error('IMAP: conexão fechada')); else resolve(resultados); });
  });
}
