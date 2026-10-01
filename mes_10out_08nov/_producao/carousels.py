"""Carrosséis de fotos do TikTok (photo mode 1080x1920): frame real do clipe + texto nativo."""
import os, sys, subprocess, json
from engine import page, T, render_pngs, LIB, TMP, clip_info, NOTIF
from clips import C
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
import render_month as RM
FR = TMP + '/frames'; os.makedirs(FR, exist_ok=True)
def still(name, dt=0.6):
    clip, ss, x = C[name]
    out = f'{FR}/{name}_{dt}.jpg'
    if os.path.exists(out): return out
    f, w, h, D = clip_info(clip)
    vf = f"crop={int(h*9/16)//2*2}:{h}:{int((w-int(h*9/16))*x)}:0,scale=1080:1920" if w > h else "scale=1080:1920"
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(min(ss+dt, D-0.1)),'-i',f,'-frames:v','1','-vf',vf,'-q:v','2',out], check=True)
    return out
def slide(name, text, sub=None, extra='', dim=0.0, top=300, dt=0.6, big=None):
    img = still(name, dt)
    st = f'font-size:{big}px;' if big else ''
    h = (f"<img src='file://{img}' style='position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover'>"
         f"<div style='position:absolute;inset:0;background:rgba(0,0,0,{dim})'></div>"
         f"<div class='tt' style='top:{top}px'><span class='box' style='{st}'>{text}</span></div>")
    if sub: h += f"<div class='tt' style='top:1180px'><span class='stroke' style='font-size:62px'>{sub}</span></div>"
    return h + extra
CAR = {}
CAR['1110_10h'] = [
  slide('cel_le_sorri', '5 coisas grátis que todo escritório contábil deveria usar 📌', 'arrasta →'),
  slide('cel_maos', '1 · app da Receita Federal no celular', 'consulta rápida sem abrir o computador', dim=.15),
  slide('focada', '2 · Portal Nacional da NFS-e', 'emissão e consulta no padrão nacional', dim=.15),
  slide('anota_mesa', '3 · agenda tributária no Google Agenda', 'com alerta 3 dias antes', dim=.15),
  slide('texta_mesa', '4 · WhatsApp Business com etiquetas', 'aguardando doc · conferindo · ok', dim=.15),
  slide('sorri_laptop', '5 · e um robô que baixa XML à meia-noite 🤖', 'esse não é grátis, mas paga o café', dim=.15),
]
CAR['1210_15h'] = [
  slide('estagiario', 'NF-e, NFC-e, NFS-e, CT-e: qual é qual?', '(pra explicar pro estagiário)'),
  slide('focada', 'NF-e', 'venda de mercadoria (principalmente entre empresas)', dim=.25, big=110),
  slide('cel_cafe', 'NFC-e', 'venda no varejo, pro consumidor final', dim=.25, big=110),
  slide('teclado', 'NFS-e', 'prestação de serviço (agora com padrão nacional)', dim=.25, big=110),
  slide('rindo_colegas', 'CT-e', 'transporte de carga · e agora manda pro estagiário 🫶', dim=.25, big=110),
]
CAR['1510_1215'] = [
  slide('cafe_grupo', 'coisas que só quem trabalha em escritório contábil entende (parte 3)'),
  slide('cel_maos', 'o boleto do DAS mandado em foto torta 📸'),
  slide('madura_tel', 'cliente: "já paguei?"', '(não pagou)'),
  slide('dor_cabeca', 'o portal da prefeitura que só funciona num navegador de 2009'),
  slide('preocupada', 'senha gov.br do cliente: ninguém sabe'),
  slide('alivio', 'a satisfação de zerar a fila de tarefas ✅'),
  slide('teclado2', 'e o café que esfriou do lado do teclado ☕'),
]
CAR['2110_1215'] = [
  slide('cel_olha_longe', 'coisas que só quem trabalha em escritório contábil entende (parte 5)'),
  slide('focada2', 'quando o cliente manda o XML em PDF'),
  slide('dor_cabeca', 'quando manda o PDF em foto'),
  slide('tedio', 'quando manda a foto do PDF impresso'),
  slide('cel_cafe', 'o grupo do escritório às 7h:', '"alguém tem a senha do portal?"'),
  slide('cafe_grupo', 'e a gente ama mesmo assim 💚'),
]
CAR['2410_15h'] = [
  slide('equipe_laptop', 'o que eu colocaria num escritório contábil novo (com orçamento pequeno)'),
  slide('focada', '1 · dois monitores por pessoa', 'o upgrade barato que mais rende', dim=.15),
  slide('headset', '2 · um headset decente', 'cliente ouve melhor, você cansa menos', dim=.15),
  slide('anota_mesa', '3 · certificados A1 com controle de vencimento', dim=.15),
  slide('teclado2', '4 · uma rotina de backup', 'que alguém realmente confere', dim=.15),
  slide('sorri_laptop', '5 · automação no que é repetitivo', 'tipo baixar XML 🤖', dim=.15),
]
CAR['3110_10h'] = [
  slide('highfive', 'coisas que só quem trabalha em escritório contábil entende (edição fim de mês)'),
  slide('satisfeito', 'zerar a caixa de entrada às 18h'),
  slide('cel_le_sorri', 'o cliente que agradece', '(raridade)'),
  slide('comemora', 'o relatório batendo com o extrato de primeira'),
  slide('cafe_grupo', 'a colega que traz pão de queijo no fechamento'),
  slide('sofa_tv', 'a sensação de mês fechado…', 'e amanhã começa tudo de novo 🙃'),
]
CAR['0111_10h'] = [
  slide('estagiario', 'checklist do 13º pra mandar pro cliente 📌', 'salva'),
  slide('anota_mesa', '1ª parcela: até 30/11', dim=.25, big=84),
  slide('teclado2', '2ª parcela: até 20/12', dim=.25, big=84),
  slide('focada2', 'mês com 15 dias ou mais trabalhados conta como mês inteiro', '1/12 por mês', dim=.25),
  slide('digita_anota', 'tem FGTS sobre o 13º', 'não esquece de avisar', dim=.25),
  slide('cel_cafe', 'manda isso pro cliente hoje 💚', dim=.15),
]
CAR['0211_15h'] = [
  slide('madura_escreve', 'MEI, ME, EPP: os limites de faturamento em 1 minuto'),
  slide('cel_maos', 'MEI', 'até R$ 81 mil por ano', dim=.3, big=120),
  slide('focada', 'Simples Nacional', 'até R$ 4,8 milhões por ano', dim=.3, big=100),
  slide('anota_papel', 'sublimite: R$ 3,6 milhões', 'acima disso, ICMS e ISS saem do Simples', dim=.3),
  slide('sorri_laptop', 'acompanhar mês a mês evita susto em dezembro 📈', dim=.15),
]
CAR['0711_10h'] = [
  slide('chefe_explica', 'coisas que só quem trabalha em escritório contábil entende (parte 10)'),
  slide('tel_explica', 'explicar pela 5ª vez o que é pró-labore'),
  slide('sem_expressao', 'o cliente que chama a gente de despachante'),
  slide('socio_tela', 'o orgulho de achar um erro antes da fiscalização'),
  slide('cel_sorri', 'ser a primeira a saber da reforma na família…', 'e a última a saber da fofoca do escritório'),
  slide('rindo_tablet', 'parte 11? comenta a sua 👇'),
]
def build(key):
    out = RM.folder(key); os.makedirs(out, exist_ok=True)
    items = [(h, f'{TMP}/car_{key}_{i+1:02d}.png') for i, h in enumerate(CAR[key])]
    for _, p in items:
        if os.path.exists(p): os.unlink(p)
    render_pngs(items)
    for i, (_, p) in enumerate(items):
        Image.open(p).convert('RGB').save(f'{out}/{i+1:02d}.jpg', quality=90)
    t = RM.entry(key)
    open(out + '/legenda.txt', 'w').write(RM.legenda(key).replace('FORMATO: Carrossel de fotos', 'FORMATO: Carrossel de fotos (modo foto do TikTok, 9:16)') +
        "\nCOMO POSTAR: no TikTok, + > Foto > selecione 01.jpg…%02d.jpg na ordem > adicione o som > cole a legenda.\n" % len(items))
    return out
if __name__ == '__main__':
    for k in (sys.argv[1:] or CAR): print(build(k))
