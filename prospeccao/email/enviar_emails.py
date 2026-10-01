#!/usr/bin/env python3
"""
Prospecção por e-mail · Epiverso
================================
Envia a sequência de 3 e-mails (abertura + 2 follow-ups na mesma conversa) com aquecimento
do domínio, ritmo humano entre envios e parada automática quando o lead responde ou pede
para sair. Só usa a biblioteca padrão do Python (3.9 ou mais novo): não precisa instalar nada.

Comandos (rode dentro da pasta email/):
  python enviar_emails.py previa              mostra os e-mails de hoje, sem enviar nada
  python enviar_emails.py teste voce@x.com    manda 1 e-mail de exemplo (use com o mail-tester.com)
  python enviar_emails.py enviar              envia o lote de hoje (pode deixar rodando)
  python enviar_emails.py verificar           confere respostas e e-mails devolvidos (IMAP)
  python enviar_emails.py status              resumo da campanha
  python enviar_emails.py marcar x@y.com respondeu|remover|devolvido|reativar
"""
import argparse
import configparser
import csv
import datetime as dt
import email
import email.policy
import hashlib
import imaplib
import json
import os
import random
import re
import smtplib
import ssl
import sys
import time
from email.message import EmailMessage
from email.utils import formataddr, formatdate, make_msgid
from pathlib import Path

PASTA = Path(__file__).resolve().parent
ARQ_ESTADO = PASTA / 'estado_email.json'
ARQ_LOG = PASTA / 'envios.csv'
ARQ_DESCADASTRO = PASTA / 'descadastrados.txt'
ARQ_MENSAGENS = PASTA / 'mensagens_email.json'

ANGULOS = ['nfce', 'nfse', 'naocontrib', 'sefaz', 'geral']
ESCADA_AQUECIMENTO = [10, 20, 30]  # e-mails/dia na semana 1, 2 e 3; depois, o limite_diario_max
GRATUITOS = {'gmail.com', 'hotmail.com', 'outlook.com', 'live.com', 'yahoo.com', 'yahoo.com.br', 'uol.com.br',
             'bol.com.br', 'terra.com.br', 'icloud.com', 'hotmail.com.br', 'outlook.com.br', 'ig.com.br'}
ALIASES = {
    'nome': ['nome', 'contato', 'responsavel', 'responsável', 'name'],
    'escritorio': ['escritorio', 'escritório', 'empresa', 'razao social', 'razão social', 'nome fantasia', 'fantasia'],
    'email': ['email', 'e-mail', 'mail'],
    'whatsapp': ['whatsapp', 'whats', 'celular', 'telefone', 'fone', 'tel', 'phone'],
    'cidade': ['cidade', 'municipio', 'município'], 'uf': ['uf', 'estado'],
    'dor': ['dor', 'angulo', 'ângulo', 'foco'], 'origem': ['origem', 'fonte'], 'obs': ['obs', 'observacao', 'observação', 'notas'],
}
EMAIL_OK = re.compile(r'^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$')
CAMPO = re.compile(r'\{(\w+)\}')
SPIN = re.compile(r'\[([^\[\]]*\|[^\[\]]*)\]')
PEDIU_PARA_SAIR = re.compile(r'\b(remover|remova|descadastr|n[aã]o quero|n[aã]o tenho interesse|pare de|parem de|sem interesse)', re.I)
CITACAO = re.compile(r'^(>|Em .+escreveu:|On .+wrote:|-{2,}\s*(Mensagem|Original)|De:\s|From:\s)', re.I)


def sair(msg):
    print(f'\n✕ {msg}\n')
    sys.exit(1)


# --------------------------------------------------------------------------- configuração
def carregar_config(caminho):
    if not caminho.exists():
        sair(f'Não achei {caminho.name}. Copie config_exemplo.ini para config.ini e preencha.')
    cfg = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
    cfg.BOOLEAN_STATES = {**cfg.BOOLEAN_STATES, 'sim': True, 's': True, 'não': False, 'nao': False, 'n': False}
    cfg.read(caminho, encoding='utf-8')
    c = {
        'nome': cfg.get('remetente', 'nome', fallback='').strip(),
        'email': cfg.get('remetente', 'email', fallback='').strip(),
        'empresa': cfg.get('remetente', 'empresa', fallback='Epiverso').strip(),
        'whatsapp': cfg.get('remetente', 'whatsapp', fallback='').strip(),
        'smtp_host': cfg.get('smtp', 'host', fallback='').strip(),
        'smtp_porta': cfg.getint('smtp', 'porta', fallback=587),
        'smtp_usuario': cfg.get('smtp', 'usuario', fallback='').strip(),
        'senha': os.environ.get('EPIVERSO_SMTP_SENHA') or cfg.get('smtp', 'senha', fallback='').strip(),
        'imap_ativo': cfg.getboolean('imap', 'ativo', fallback=False),
        'imap_host': cfg.get('imap', 'host', fallback='').strip(),
        'imap_porta': cfg.getint('imap', 'porta', fallback=993),
        'leads': (caminho.parent / cfg.get('envio', 'leads', fallback='../leads.csv').strip()).resolve(),
        'limite_max': cfg.getint('envio', 'limite_diario_max', fallback=40),
        'inicio_aquecimento': cfg.get('envio', 'inicio_aquecimento', fallback='').strip(),
        'intervalo_min': cfg.getint('envio', 'intervalo_min_seg', fallback=90),
        'intervalo_max': cfg.getint('envio', 'intervalo_max_seg', fallback=240),
        'hora_inicio': cfg.getint('envio', 'hora_inicio', fallback=8),
        'hora_fim': cfg.getint('envio', 'hora_fim', fallback=18),
        'dias_etapas': [int(x) for x in cfg.get('envio', 'dias_entre_etapas', fallback='3,4').split(',')],
    }
    c['smtp_usuario'] = c['smtp_usuario'] or c['email']
    faltando = [k for k in ('nome', 'email', 'smtp_host') if not c[k]]
    if faltando:
        sair(f'Preencha no config.ini: {", ".join(faltando)}.')
    return c


def carregar_estado():
    if ARQ_ESTADO.exists():
        return json.loads(ARQ_ESTADO.read_text(encoding='utf-8'))
    return {'inicio': '', 'leads': {}, 'hashes': []}


def salvar_estado(estado):
    tmp = ARQ_ESTADO.with_suffix('.tmp')
    tmp.write_text(json.dumps(estado, ensure_ascii=False, indent=1), encoding='utf-8')
    tmp.replace(ARQ_ESTADO)


def descadastrados():
    if not ARQ_DESCADASTRO.exists():
        return set()
    return {l.strip().lower() for l in ARQ_DESCADASTRO.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')}


def bloqueado(endereco, lista):
    return endereco in lista or '@' + endereco.split('@')[1] in lista


def adicionar_descadastro(endereco):
    novo = not ARQ_DESCADASTRO.exists()
    with ARQ_DESCADASTRO.open('a', encoding='utf-8') as f:
        if novo:
            f.write('# Um e-mail por linha (ou @dominio.com.br para bloquear o domínio inteiro). Nunca recebem nada.\n')
        f.write(endereco + '\n')


# --------------------------------------------------------------------------- leads
def ler_csv(caminho):
    if not caminho.exists():
        sair(f'Não achei a planilha de leads em {caminho}. Ajuste "leads" no config.ini.')
    bruto = caminho.read_bytes()
    try:
        texto = bruto.decode('utf-8-sig')
    except UnicodeDecodeError:
        texto = bruto.decode('cp1252')  # Excel antigo salva em ANSI
    prim = texto.split('\n', 1)[0]
    sep = ';' if prim.count(';') > prim.count(',') else ('\t' if '\t' in prim else ',')
    linhas = list(csv.reader(texto.splitlines(), delimiter=sep))
    if not linhas:
        return []
    cab = [c.strip().lower() for c in linhas[0]]
    idx = {k: next((i for i, c in enumerate(cab) if c in al), -1) for k, al in ALIASES.items()}
    if idx['email'] < 0:
        sair('A planilha de leads precisa de uma coluna "email".')
    leads, vistos = [], set()
    for l in linhas[1:]:
        v = {k: (l[i].strip() if 0 <= i < len(l) else '') for k, i in idx.items()}
        v['email'] = v['email'].lower()
        if not EMAIL_OK.match(v['email']) or v['email'] in vistos:
            continue
        vistos.add(v['email'])
        leads.append(v)
    return leads


def normalizar_dor(d):
    d = (d or '').lower()
    for padrao, ang in (('nfc', 'nfce'), ('nfs', 'nfse'), ('servi', 'nfse'), ('contrib', 'naocontrib'),
                        ('sefaz', 'sefaz'), ('demora', 'sefaz'), ('geral', 'geral')):
        if padrao in d:
            return ang
    return ''


def primeiro_nome(n):
    p = (n or '').split()
    if not p:
        return ''
    cap = lambda s: s[:1].upper() + s[1:].lower()
    if p[0].rstrip('.').lower() in ('dr', 'dra', 'sr', 'sra', 'prof', 'profa') and len(p) > 1:
        return f'{cap(p[0].rstrip("."))}. {cap(p[1])}'
    return cap(p[0])


def limpar_escritorio(n):
    n = re.sub(r'\b(ltda|me|epp|eireli|s/s|ss|s\.s\.|s/c|sociedade simples)\b\.?', '', n or '', flags=re.I)
    return re.sub(r'\s{2,}', ' ', re.sub(r'[\s\-–,.]+$', '', n)).strip()


# --------------------------------------------------------------------------- motor de variações
def campos_ok(t, ctx):
    return all(ctx.get(c) for c in CAMPO.findall(t))


def spin(t, ctx):
    for _ in range(500):
        m = SPIN.search(t)
        if not m:
            break
        ops = [o for o in m.group(1).split('|') if campos_ok(o, ctx)]
        t = t[:m.start()] + (random.choice(ops) if ops else '') + t[m.end():]
    return t


def preencher(t, ctx):
    return CAMPO.sub(lambda m: ctx.get(m.group(1), ''), t)


def limpar(t):
    linhas = [re.sub(r' ([,.?!:])', r'\1', re.sub(r'[ \t]+', ' ', l)).strip() for l in t.split('\n')]
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(linhas)).strip()


def escolher(lista, ctx):
    for t in random.sample(lista, len(lista)):
        r = spin(t, ctx)
        if campos_ok(r, ctx):
            return preencher(r, ctx)
    return ''


def com_nome(lista, ctx):
    """Se o lead tem nome, quase sempre usa uma saudação com o nome."""
    com = [t for t in lista if '{nome}' in t]
    return com if ctx.get('nome') and com and random.random() < 0.85 else lista


def contexto(cfg, lead, angulo, msgs):
    h = dt.datetime.now().hour
    periodo = 'Bom dia' if h < 12 else 'Boa tarde' if h < 18 else 'Boa noite'
    return {
        'nome': primeiro_nome(lead.get('nome')), 'escritorio': limpar_escritorio(lead.get('escritorio')),
        'cidade': lead.get('cidade', ''), 'seu_nome': cfg['nome'], 'empresa': cfg['empresa'],
        'whatsapp': cfg['whatsapp'], 'periodo': periodo, 'dor': msgs['dores'][angulo],
    }


def montar_email(cfg, msgs, lead, etapa, angulo):
    """Devolve (assunto, corpo). etapa 0 = abertura, 1 e 2 = follow-ups."""
    ctx = contexto(cfg, lead, angulo, msgs)
    if etapa == 0:
        assunto = limpar(escolher(msgs['assuntos'][angulo], ctx))
        corpo = escolher(com_nome(msgs['saudacoes'], ctx), ctx) + '\n\n' + escolher(msgs['aberturas'][angulo], ctx)
    else:
        assunto = ''
        corpo = escolher(msgs['followup_1' if etapa == 1 else 'followup_2'], ctx)
    assinatura = preencher(msgs['assinatura'], ctx)
    rodape = escolher(msgs['rodape_optout'], ctx)
    return assunto, limpar(f'{corpo}\n\n{assinatura}\n\n{rodape}')


def impressao(texto):
    return hashlib.sha1(re.sub(r'\s+', ' ', texto.lower()).encode()).hexdigest()[:16]


def montar_unico(cfg, msgs, lead, etapa, angulo, estado):
    for _ in range(40):
        assunto, corpo = montar_email(cfg, msgs, lead, etapa, angulo)
        if impressao(corpo) not in estado['hashes']:
            break
    return assunto, corpo


# --------------------------------------------------------------------------- agenda
def dias_uteis_entre(a, b):
    n, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return n


def limite_hoje(cfg, estado, hoje):
    inicio = cfg['inicio_aquecimento'] or estado.get('inicio') or hoje.isoformat()
    semanas = max(0, (hoje - dt.date.fromisoformat(inicio)).days) // 7
    degrau = ESCADA_AQUECIMENTO[semanas] if semanas < len(ESCADA_AQUECIMENTO) else cfg['limite_max']
    return min(degrau, cfg['limite_max'])


def enviados_hoje(hoje):
    if not ARQ_LOG.exists():
        return 0
    with ARQ_LOG.open(encoding='utf-8') as f:
        return sum(1 for r in csv.DictReader(f, delimiter=';') if r['data'] == hoje.isoformat())


def fila_de_hoje(cfg, estado, leads, hoje, limite):
    bloq = descadastrados()
    por_email = {l['email']: l for l in leads}
    fila = []
    # 1) follow-ups vencidos (quem não respondeu)
    for end, s in estado['leads'].items():
        if s['status'] != 'ativo' or not 1 <= s['etapa'] <= 2 or bloqueado(end, bloq):
            continue
        espera = cfg['dias_etapas'][min(s['etapa'], len(cfg['dias_etapas'])) - 1]
        if dias_uteis_entre(dt.date.fromisoformat(s['ultimo_envio']), hoje) >= espera:
            fila.append((por_email.get(end) or s.get('lead') or {'email': end}, s['etapa']))
    # 2) leads novos, no máximo 1 por domínio de empresa por dia (vários e-mails no mesmo domínio parece disparo)
    dominios = {l['email'].split('@')[1] for l, _ in fila}
    for l in leads:
        dom = l['email'].split('@')[1]
        s = estado['leads'].get(l['email'])
        if (s and (s['status'] != 'ativo' or s['etapa'] > 0)) or bloqueado(l['email'], bloq):
            continue
        if dom not in GRATUITOS and dom in dominios:
            continue
        dominios.add(dom)
        fila.append((l, 0))
    return fila[:max(0, limite)]


# --------------------------------------------------------------------------- SMTP e IMAP
def conectar_smtp(cfg):
    ctx = ssl.create_default_context()
    if cfg['smtp_porta'] == 465:
        s = smtplib.SMTP_SSL(cfg['smtp_host'], 465, context=ctx, timeout=60)
    else:
        s = smtplib.SMTP(cfg['smtp_host'], cfg['smtp_porta'], timeout=60)
        s.starttls(context=ctx)
    if not cfg['senha']:
        sair('Sem senha do SMTP. Defina a variável EPIVERSO_SMTP_SENHA ou preencha "senha" no config.ini.')
    s.login(cfg['smtp_usuario'], cfg['senha'])
    return s


def criar_mensagem(cfg, lead, assunto, corpo, anteriores=()):
    m = EmailMessage()
    m['From'] = formataddr((cfg['nome'], cfg['email']))
    m['To'] = formataddr((lead.get('nome') or '', lead['email']))
    m['Subject'] = assunto
    m['Date'] = formatdate(localtime=True)
    m['Message-ID'] = make_msgid(domain=cfg['email'].split('@')[1])
    m['List-Unsubscribe'] = f'<mailto:{cfg["email"]}?subject=remover>'
    if anteriores:
        m['In-Reply-To'] = anteriores[-1]
        m['References'] = ' '.join(anteriores)
    m.set_content(corpo)
    return m


def texto_novo(msg):
    """Só o que a pessoa escreveu, sem a parte citada do nosso e-mail."""
    try:
        parte = msg.get_body(preferencelist=('plain', 'html'))
        texto = parte.get_content() if parte else ''
    except Exception:
        return ''
    if parte is not None and parte.get_content_type() == 'text/html':
        texto = re.sub(r'<[^>]+>', ' ', texto)
    novo = []
    for linha in texto.splitlines():
        if CITACAO.match(linha.strip()):
            break
        novo.append(linha)
    return '\n'.join(novo)


def data_imap(iso):
    d = dt.date.fromisoformat(iso)
    return f'{d.day:02d}-{["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][d.month-1]}-{d.year}'


def verificar_caixa(cfg, estado, so=None, silencioso=False):
    """Marca quem respondeu (para de enviar), quem pediu para sair e quem foi devolvido."""
    if not cfg['imap_ativo']:
        if not silencioso:
            print('IMAP desligado no config.ini: marque as respostas com "marcar". Os follow-ups NÃO param sozinhos.')
        return
    ativos = {e: s for e, s in estado['leads'].items() if s['status'] == 'ativo' and (so is None or e == so)}
    if not ativos:
        return
    try:
        imap = imaplib.IMAP4_SSL(cfg['imap_host'], cfg['imap_porta'])
        imap.login(cfg['smtp_usuario'], cfg['senha'])
        imap.select('INBOX', readonly=True)
    except Exception as e:
        print(f'! Não consegui abrir a caixa de entrada por IMAP ({e}). Sigo sem verificar respostas.')
        return
    mudou = 0
    try:
        for end, s in ativos.items():
            _, dados = imap.search(None, f'(FROM "{end}" SINCE {data_imap(s["primeiro_envio"])})')
            ids = dados[0].split() if dados and dados[0] else []
            if not ids:
                continue
            _, bruto = imap.fetch(ids[-1], '(BODY.PEEK[])')
            msg = email.message_from_bytes(bruto[0][1], policy=email.policy.default)
            if PEDIU_PARA_SAIR.search(texto_novo(msg)):
                s['status'] = 'removido'
                adicionar_descadastro(end)
                print(f'  ⊘ {end} pediu para sair: removido da lista.')
            else:
                s['status'] = 'respondeu'
                print(f'  ★ {end} RESPONDEU. Sequência parada: responda pessoalmente!')
            mudou += 1
        if so is None:
            desde = data_imap(min(s['primeiro_envio'] for s in ativos.values()))
            _, dados = imap.search(None, f'(OR FROM "mailer-daemon" FROM "postmaster" SINCE {desde})')
            for num in (dados[0].split() if dados and dados[0] else []):
                _, bruto = imap.fetch(num, '(BODY.PEEK[])')
                conteudo = bruto[0][1].decode('latin-1', 'ignore').lower()
                for end, s in ativos.items():
                    if s['status'] == 'ativo' and end in conteudo:
                        s['status'] = 'devolvido'
                        mudou += 1
                        print(f'  ↩ {end} devolvido (endereço não existe). Removido da sequência.')
    finally:
        try:
            imap.logout()
        except Exception:
            pass
    if mudou:
        salvar_estado(estado)
    elif not silencioso and so is None:
        print('Nenhuma resposta nova.')


def registrar_envio(hoje, lead, etapa, assunto, mid):
    novo = not ARQ_LOG.exists()
    with ARQ_LOG.open('a', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=';')
        if novo:
            w.writerow(['data', 'hora', 'email', 'nome', 'escritorio', 'etapa', 'assunto', 'message_id'])
        w.writerow([hoje.isoformat(), dt.datetime.now().strftime('%H:%M'), lead['email'], lead.get('nome', ''),
                    lead.get('escritorio', ''), etapa + 1, assunto, mid])


# --------------------------------------------------------------------------- comandos
def angulo_do_lead(lead, s=None):
    return (s or {}).get('angulo') or normalizar_dor(lead.get('dor')) or random.choice(ANGULOS)


def cmd_previa(cfg, msgs, estado, args):
    hoje = dt.date.today()
    leads = ler_csv(cfg['leads'])
    lim = limite_hoje(cfg, estado, hoje)
    fila = fila_de_hoje(cfg, estado, leads, hoje, lim - enviados_hoje(hoje))
    print(f'Hoje: limite {lim} (aquecimento) · já enviados {enviados_hoje(hoje)} · na fila {len(fila)}\n')
    for lead, etapa in fila[:args.n]:
        s = estado['leads'].get(lead['email'], {})
        assunto, corpo = montar_email(cfg, msgs, lead, etapa, angulo_do_lead(lead, s))
        assunto = assunto or 'Re: ' + s.get('assunto', '')
        print('═' * 70)
        print(f'Para: {lead["email"]}   ·   Etapa {etapa + 1}/3   ·   {len(corpo.split())} palavras')
        print(f'Assunto: {assunto}\n')
        print(corpo)
    print('═' * 70)
    if len(fila) > args.n:
        print(f'… e mais {len(fila) - args.n}. Use -n para ver mais.')


def cmd_teste(cfg, msgs, estado, args):
    leads = ler_csv(cfg['leads']) if cfg['leads'].exists() else []
    lead = dict(leads[0]) if leads else {'nome': 'Marcos Silva', 'escritorio': 'Contabilidade Exemplo', 'cidade': 'Joinville'}
    lead['email'] = args.para
    assunto, corpo = montar_email(cfg, msgs, lead, 0, angulo_do_lead(lead))
    s = conectar_smtp(cfg)
    s.send_message(criar_mensagem(cfg, lead, assunto, corpo))
    s.quit()
    print(f'✓ Teste enviado para {args.para}. Assunto: "{assunto}"')
    print('  Dica: mande para o endereço do mail-tester.com e busque nota 9/10 ou mais antes de começar.')


def cmd_enviar(cfg, msgs, estado, args):
    hoje, agora = dt.date.today(), dt.datetime.now()
    if not args.forcar:
        if hoje.weekday() >= 5:
            sair('Hoje é fim de semana. E-mail de prospecção no fim de semana tem menos resposta e mais denúncia. (Use --forcar se quiser mesmo.)')
        if not cfg['hora_inicio'] <= agora.hour < cfg['hora_fim']:
            sair(f'Fora do horário ({cfg["hora_inicio"]}h às {cfg["hora_fim"]}h). (Use --forcar se quiser mesmo.)')
    verificar_caixa(cfg, estado, silencioso=True)
    leads = ler_csv(cfg['leads'])
    lim = limite_hoje(cfg, estado, hoje)
    if args.max is not None:
        lim = min(lim, args.max)
    fila = fila_de_hoje(cfg, estado, leads, hoje, lim - enviados_hoje(hoje))
    if not fila:
        print(f'Nada para enviar hoje (limite {lim}, já enviados {enviados_hoje(hoje)}).')
        return
    print(f'Enviando {len(fila)} e-mails hoje (limite de aquecimento: {lim}). Ctrl+C para parar a qualquer momento.\n')
    estado['inicio'] = estado.get('inicio') or hoje.isoformat()
    erros_seguidos = 0
    for i, (lead, etapa) in enumerate(fila, 1):
        end = lead['email']
        s = estado['leads'].get(end)
        if etapa > 0:
            verificar_caixa(cfg, estado, so=end, silencioso=True)  # respondeu nos últimos minutos?
            if s['status'] != 'ativo':
                continue
        if not args.forcar and dt.datetime.now().hour >= cfg['hora_fim']:
            print('Chegou o fim do horário comercial. O resto fica para amanhã.')
            break
        angulo = angulo_do_lead(lead, s)
        assunto, corpo = montar_unico(cfg, msgs, lead, etapa, angulo, estado)
        if etapa > 0:
            assunto = 'Re: ' + s['assunto']
        msg = criar_mensagem(cfg, lead, assunto, corpo, (s or {}).get('message_ids', []))
        try:
            smtp = conectar_smtp(cfg)
            smtp.send_message(msg)
            smtp.quit()
            erros_seguidos = 0
        except smtplib.SMTPAuthenticationError:
            sair('O servidor recusou usuário/senha. No Gmail/Workspace, use uma "senha de app" (veja o LEIA-ME).')
        except smtplib.SMTPRecipientsRefused:
            print(f'  ↩ {end} recusado pelo servidor: marcado como devolvido.')
            estado['leads'][end] = {**(s or {}), 'status': 'devolvido', 'etapa': (s or {}).get('etapa', 0),
                                    'angulo': angulo, 'primeiro_envio': (s or {}).get('primeiro_envio', hoje.isoformat()),
                                    'ultimo_envio': hoje.isoformat(), 'message_ids': (s or {}).get('message_ids', []),
                                    'assunto': (s or {}).get('assunto', assunto)}
            salvar_estado(estado)
            continue
        except Exception as e:
            erros_seguidos += 1
            print(f'  ! Erro ao enviar para {end}: {e}')
            if erros_seguidos >= 3:
                sair('3 erros seguidos: parei para proteger o domínio. Confira a conexão/limite do provedor e rode de novo depois.')
            continue
        if s is None:
            s = estado['leads'][end] = {'angulo': angulo, 'etapa': 0, 'assunto': assunto, 'message_ids': [],
                                        'primeiro_envio': hoje.isoformat(), 'status': 'ativo',
                                        'lead': {k: lead.get(k, '') for k in ('nome', 'escritorio', 'cidade', 'email')}}
        if etapa == 0:
            s['assunto'] = assunto
        s['etapa'] = etapa + 1
        s['ultimo_envio'] = hoje.isoformat()
        s['message_ids'].append(msg['Message-ID'])
        if s['etapa'] >= 3:
            s['status'] = 'concluido'
        estado['hashes'] = (estado['hashes'] + [impressao(corpo)])[-5000:]
        salvar_estado(estado)
        registrar_envio(hoje, lead, etapa, assunto, msg['Message-ID'])
        print(f'  ✓ {i}/{len(fila)}  {end}  ·  etapa {etapa + 1}/3  ·  "{assunto}"')
        if i < len(fila):
            espera = random.randint(cfg['intervalo_min'], max(cfg['intervalo_min'], cfg['intervalo_max']))
            print(f'    aguardando {espera // 60}min{espera % 60:02d}s (ritmo humano)…')
            time.sleep(espera)
    print('\nPronto por hoje.')


def cmd_verificar(cfg, msgs, estado, args):
    verificar_caixa(cfg, estado)


def cmd_status(cfg, msgs, estado, args):
    hoje = dt.date.today()
    cont = {}
    for s in estado['leads'].values():
        cont[s['status']] = cont.get(s['status'], 0) + 1
    total = len(estado['leads'])
    resp = cont.get('respondeu', 0) + cont.get('removido', 0)
    leads = ler_csv(cfg['leads']) if cfg['leads'].exists() else []
    bloq = descadastrados()
    novos = sum(1 for l in leads if l['email'] not in estado['leads'] and not bloqueado(l['email'], bloq))
    print(f'Hoje: {enviados_hoje(hoje)} de {limite_hoje(cfg, estado, hoje)} (limite de aquecimento, máx. {cfg["limite_max"]})')
    print(f'Leads contatados: {total} · ainda não contatados: {novos}')
    for chave, nome in (('ativo', 'Na sequência'), ('respondeu', 'Responderam'), ('removido', 'Pediram para sair'),
                        ('devolvido', 'Devolvidos'), ('concluido', 'Sequência concluída sem resposta')):
        print(f'  {nome:<34}{cont.get(chave, 0)}')
    if total:
        print(f'Taxa de resposta: {100 * resp / total:.1f}%   ·   Devolução: {100 * cont.get("devolvido", 0) / total:.1f}%')
        if cont.get('devolvido', 0) / total > 0.03:
            print('! Devolução acima de 3%: limpe a lista (valide os e-mails) antes de continuar. Isso derruba a reputação do domínio.')


def cmd_marcar(cfg, msgs, estado, args):
    end, acao = args.email.lower(), args.acao
    s = estado['leads'].setdefault(end, {'angulo': 'geral', 'etapa': 0, 'assunto': '', 'message_ids': [],
                                         'primeiro_envio': dt.date.today().isoformat(),
                                         'ultimo_envio': dt.date.today().isoformat(), 'status': 'ativo'})
    s['status'] = {'respondeu': 'respondeu', 'remover': 'removido', 'devolvido': 'devolvido', 'reativar': 'ativo'}[acao]
    if acao == 'remover':
        adicionar_descadastro(end)
    salvar_estado(estado)
    print(f'✓ {end}: {s["status"]}')


def main():
    p = argparse.ArgumentParser(description='Prospecção por e-mail · Epiverso', formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    p.add_argument('--config', default=str(PASTA / 'config.ini'), help='arquivo de configuração (padrão: config.ini)')
    sub = p.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('previa', help='mostra os e-mails de hoje sem enviar')
    a.add_argument('-n', type=int, default=5, help='quantos mostrar (padrão 5)')
    a = sub.add_parser('teste', help='manda 1 e-mail de exemplo para você')
    a.add_argument('para')
    a = sub.add_parser('enviar', help='envia o lote de hoje')
    a.add_argument('--forcar', action='store_true', help='ignora fim de semana e horário comercial')
    a.add_argument('--max', type=int, help='envia no máximo N hoje (abaixo do limite de aquecimento)')
    sub.add_parser('verificar', help='confere respostas e devoluções (IMAP)')
    sub.add_parser('status', help='resumo da campanha')
    a = sub.add_parser('marcar', help='muda o status de um lead')
    a.add_argument('email')
    a.add_argument('acao', choices=['respondeu', 'remover', 'devolvido', 'reativar'])
    args = p.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(errors='replace')  # console/arquivo de log do Windows sem UTF-8

    cfg = carregar_config(Path(args.config).resolve())
    msgs = json.loads(ARQ_MENSAGENS.read_text(encoding='utf-8'))
    estado = carregar_estado()
    try:
        globals()['cmd_' + args.cmd](cfg, msgs, estado, args)
    except KeyboardInterrupt:
        salvar_estado(estado)
        print('\nParado. O que já foi enviado está registrado; rode "enviar" de novo para continuar.')


if __name__ == '__main__':
    main()
