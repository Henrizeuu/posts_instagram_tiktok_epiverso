// Gera o zip para baixar e rodar: tudo em um arquivo só (app/servidor.mjs), sem npm install.
// Uso: npm run build   →   ../epiverso_prospeccao.zip
import { build } from 'esbuild';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const RAIZ = path.dirname(new URL(import.meta.url).pathname);
const NOME = 'epiverso-prospeccao';
const DIST = path.join(RAIZ, 'dist', NOME);
const ZIP = path.resolve(RAIZ, '..', 'epiverso_prospeccao.zip');

fs.rmSync(path.join(RAIZ, 'dist'), { recursive: true, force: true });
fs.mkdirSync(path.join(DIST, 'app'), { recursive: true });

await build({
  entryPoints: [path.join(RAIZ, 'src/servidor.mjs')], outfile: path.join(DIST, 'app/servidor.mjs'),
  bundle: true, platform: 'node', format: 'esm', target: 'node20', minify: true, legalComments: 'external',
  // opcionais do Baileys que não usamos (imagens, prévia de link, decodificar áudio): ficam de fora
  external: ['sharp', 'jimp', 'audio-decode', 'link-preview-js'],
  banner: { js: "import{createRequire as __cr}from'module';const require=__cr(import.meta.url);" },
  logLevel: 'warning'
});
fs.cpSync(path.join(RAIZ, 'painel'), path.join(DIST, 'app/painel'), { recursive: true });
fs.copyFileSync(path.join(RAIZ, 'leads_exemplo.csv'), path.join(DIST, 'leads_exemplo.csv'));
fs.copyFileSync(path.join(RAIZ, 'LEIA-ME.txt'), path.join(DIST, 'LEIA-ME.txt'));

const crlf = s => s.replace(/\r?\n/g, '\r\n');
fs.writeFileSync(path.join(DIST, 'INICIAR (Windows).bat'), crlf(`@echo off
chcp 65001 >nul
title Epiverso Prospeccao - deixe esta janela aberta
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo.
  echo   O Node.js nao esta instalado neste computador.
  echo   Vou abrir o site: baixe a versao LTS, instale ^(Avancar, Avancar, Concluir^)
  echo   e depois abra este arquivo de novo.
  echo.
  start "" "https://nodejs.org/pt-br/download"
  pause
  exit /b
)
node "app\\servidor.mjs"
echo.
echo   O sistema foi fechado. Os envios param ate voce abrir de novo.
pause
`));
const unix = abrir => `#!/bin/bash
cd "$(dirname "$0")"
if ! command -v node >/dev/null 2>&1; then
  echo "O Node.js não está instalado. Baixe a versão LTS em https://nodejs.org e abra este arquivo de novo."
  ${abrir} "https://nodejs.org/pt-br/download" >/dev/null 2>&1
  read -p "Aperte Enter para sair"
  exit 1
fi
node app/servidor.mjs
`;
fs.writeFileSync(path.join(DIST, 'INICIAR (Mac).command'), unix('open'), { mode: 0o755 });
fs.writeFileSync(path.join(DIST, 'iniciar-linux.sh'), unix('xdg-open'), { mode: 0o755 });

fs.rmSync(ZIP, { force: true });
execFileSync('zip', ['-r', '-9', '-X', '-q', ZIP, NOME], { cwd: path.join(RAIZ, 'dist') });
const mb = b => (b / 1024 / 1024).toFixed(1) + ' MB';
console.log(`servidor.mjs: ${mb(fs.statSync(path.join(DIST, 'app/servidor.mjs')).size)} · zip: ${mb(fs.statSync(ZIP).size)} → ${ZIP}`);
