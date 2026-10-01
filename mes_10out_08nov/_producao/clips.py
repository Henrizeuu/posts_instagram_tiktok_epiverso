# Catálogo: nome -> (clip, ss, x)   x = centro do recorte vertical (só p/ horizontais)
C = {
 'tel_calma':('h10',2,.62), 'tel_explica':('h10',12,.62), 'tel_ocupada':('h11',2,.45), 'tel_fixo':('v12',2,.5),
 'tel_gesticula':('h01',11,.45), 'tel_serio':('h01',20,.45), 'tel_anota':('h01',29,.45), 'texta_mesa':('h01',37,.45), 'anota_mesa':('h01',2,.45),
 'cel_sorri':('h02',3,.42), 'cel_olha_longe':('h02',11,.42), 'cel_le_sorri':('v02',1,.5), 'cel_cafe':('v03',0.5,.5), 'cel_maos':('v04',1,.5),
 'dor_cabeca':('h03',0.5,.42), 'cansada_noite':('h04',0.5,.36), 'anota_noite':('h04',13,.5), 'maos_cabeca':('h17',5,.45), 'preocupada':('h17',13,.45),
 'tedio':('h05',2,1.0), 'tedio2':('v09',2,.5), 'sem_expressao':('v13',2.5,.5), 'focada':('v14',1,.5), 'focada2':('v13',8,.5),
 'papel_mesa':('v05',0.5,.5), 'sorri_laptop':('v08',2,.5), 'mulher_wide':('v21',1,.5), 'homeoffice':('v01',1,.5),
 'teclado':('v06',1,.5), 'teclado2':('v18',5,.5), 'laptop_maos':('v07',1,.5), 'notebook_mao':('v07',5,.5),
 'socios_conversa':('h06',3,.5), 'cafe_grupo':('h07',0.5,.5), 'rindo_tablet':('h09',1.5,.45), 'rindo_colegas':('v11',0,.5),
 'postit_tel':('h13',3,.5), 'highfive':('h08',9.3,.58), 'colegas_viram':('h08',3,.5),
 'madura_tel':('h12',1,.45), 'madura_olha_cel':('h12',8.3,.45), 'chefe_explica':('h14',0.3,.5), 'equipe_laptop':('h15',2,.5), 'equipe_monitor':('h16',1,.45),
 'cafe_duas':('h22',1.5,.36), 'pausa_cafe':('v17',1,.5), 'almoco':('v16',1,.5),
 'alivio':('h18',1,.4), 'sofa_tv':('h20',1,.4), 'sofa_pipoca':('h21',0.3,.62), 'sofa_laptop':('v15',1,.5),
 'socio_camera':('h24',5,.5), 'socio_tela':('h23',1,.42), 'madrugada':('h25',2,.4), 'homem_laptop':('v19',1,.5), 'estagiario':('v20',1,.5),
}
def sc(name, d, **kw):
    clip, ss, x = C[name]
    s = dict(clip=clip, ss=kw.pop('ss', ss), x=kw.pop('x', x), d=d)
    if name in MAXEND: s['maxend'] = MAXEND[name]
    s.update(kw); return s
C.update({'robo_sync':('r04',4.0,.5),'pasta_xml':('r04',8.0,.5),'painel_pronto':('r04',11.8,.5),
          'busca':('r08',3.6,.5),'danfe':('r08',8.7,.5),'zip':('r08',12.0,.5)})
MAXEND = {'robo_sync':7.8, 'pasta_xml':11.6, 'painel_pronto':14.3, 'busca':7.8, 'danfe':10.9, 'zip':13.7}
C.update({'madura_escreve':('h26',1,.5), 'madura_digita':('h26',12,.5), 'quadro':('h27',2,.72), 'postits':('h28',0.3,.5),
          'notif_mesa':('h29',4,.58), 'pega_cel':('h29',10.5,.62), 'comemora':('h31',6.5,.5), 'comemora_inicio':('h31',1,.5),
          'tchau':('h32',0.8,.6), 'fecha_laptop':('h32',3.6,.6), 'satisfeito':('h32',9,.62), 'sala_noite':('h33',1,.3),
          'headset':('h34',1,.55), 'headset_ri':('h34',11,.55), 'chega':('h35',0.3,.62), 'chega_le':('h35',5,.6),
          'digita_anota':('h37',1,.6), 'anota_papel':('h37',8.5,.65), 'ma_noticia':('h38',1,.52), 'ma_noticia2':('h38',7.5,.52)})
