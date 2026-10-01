"""Personagens da série (SVG). Cada um é montado com ids prefixados para o rig: P, Pbody, Phead, Parm1, Parm2, Pfx."""
GRAD = """
 <radialGradient id="gW" cx="35%" cy="28%" r="80%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#ECEEF0"/><stop offset="1" stop-color="#B4BCC3"/></radialGradient>
 <radialGradient id="gW2" cx="38%" cy="30%" r="75%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".6" stop-color="#E7EAED"/><stop offset="1" stop-color="#AEB7BF"/></radialGradient>
 <radialGradient id="gC" cx="35%" cy="28%" r="80%"><stop offset="0" stop-color="#FFF4E0"/><stop offset=".6" stop-color="#F6DDB4"/><stop offset="1" stop-color="#D7B07A"/></radialGradient>
 <linearGradient id="gRim" x1="0" y1="0" x2="1" y2="0"><stop offset=".7" stop-color="#10B981" stop-opacity="0"/><stop offset="1" stop-color="#10B981" stop-opacity=".22"/></linearGradient>
"""
def fx(p, facing=1):
    """símbolos de emoção estilo mangá, acima-direita da cabeça (cada um com id próprio p+'_xxx')"""
    return f"""
  <g id="{p}fx">
   <g id="{p}_vein" opacity="0" transform="translate(95 -560)"><g stroke="#EF4444" stroke-width="11" stroke-linecap="round" fill="none">
     <path d="M -30 -8 q 22 -4 26 -26"/><path d="M 8 -34 q 4 22 26 26"/><path d="M 34 8 q -22 4 -26 26"/><path d="M -8 34 q -4 -22 -26 -26"/></g></g>
   <g id="{p}_sweat" opacity="0" transform="translate(120 -470)"><path d="M 0 -40 C 18 -10, 26 6, 26 18 A 26 26 0 0 1 -26 18 C -26 6, -18 -10, 0 -40 Z" fill="#7DD3FC"/><ellipse cx="-8" cy="12" rx="6" ry="10" fill="#fff" opacity=".8"/></g>
   <g id="{p}_spark" opacity="0" fill="#10B981"><path d="M 110 -560 l 9 26 26 9 -26 9 -9 26 -9 -26 -26 -9 26 -9z"/><path d="M 160 -500 l 6 16 16 6 -16 6 -6 16 -6 -16 -16 -6 16 -6z"/><path d="M 70 -610 l 5 13 13 5 -13 5 -5 13 -5 -13 -13 -5 13 -5z"/></g>
   <g id="{p}_gloom" opacity="0" stroke="#8A8AA0" stroke-width="8" stroke-linecap="round" fill="none"><path d="M -60 -600 q 10 20 0 40 q -10 20 0 40"/><path d="M 0 -620 q 10 20 0 40 q -10 20 0 40"/><path d="M 60 -600 q 10 20 0 40 q -10 20 0 40"/></g>
   <g id="{p}_excl" opacity="0" transform="translate(120 -560)"><rect x="-11" y="-60" width="22" height="70" rx="11" fill="#10B981"/><circle cy="34" r="13" fill="#10B981"/></g>
   <g id="{p}_q" opacity="0" transform="translate(120 -560) scale({facing} 1)"><text font-family="Inter" font-weight="800" font-size="120" fill="#10B981" text-anchor="middle" dominant-baseline="central">?</text></g>
   <g id="{p}_steam" opacity="0" fill="#E5E5E8"><circle cx="-40" cy="-600" r="26"/><circle cx="0" cy="-630" r="32"/><circle cx="44" cy="-600" r="24"/></g>
  </g>"""
def person(p, kind='fiscal', facing=1, pose='sit'):
    """kind: fiscal (headset verde), socio (colete escuro + gravata verde), cliente (cor creme + boné)"""
    body = 'url(#gC)' if kind == 'cliente' else 'url(#gW)'
    head = 'url(#gC)' if kind == 'cliente' else 'url(#gW2)'
    far = '#B89A6E' if kind == 'cliente' else '#8E98A1'
    big = 1.12 if kind == 'socio' else 1.0
    acc_head = ''
    if kind == 'fiscal':
        acc_head = """<path d="M -112 -420 A 124 124 0 0 1 110 -432" fill="none" stroke="#10B981" stroke-width="17" stroke-linecap="round"/>
   <path d="M 6 -378 C 52 -318, 98 -320, 126 -340" fill="none" stroke="#10B981" stroke-width="9" stroke-linecap="round"/><circle cx="129" cy="-342" r="14" fill="#0A0A0A"/>
   <ellipse cx="0" cy="-384" rx="36" ry="42" fill="#10B981"/><ellipse cx="-9" cy="-395" rx="12" ry="15" fill="#6EE7B7" opacity=".6"/>"""
    elif kind == 'cliente':
        acc_head = """<path d="M -118 -440 A 126 126 0 0 1 118 -440 Z" fill="#F59E0B"/><path d="M 60 -446 q 90 -6 120 18 q -40 10 -120 2z" fill="#D97706"/>"""
    acc_body = ''
    if kind == 'socio':
        acc_body = """<path d="M -128 -250 C -120 -120, -100 -40, -40 -6 L 40 -6 C 100 -40, 120 -120, 128 -250 C 90 -300, 40 -318, 0 -320 C -40 -318, -90 -300, -128 -250 Z" fill="#26262B"/>
   <path d="M 0 -318 L 22 -280 L 8 -150 L 0 -130 L -8 -150 L -22 -280 Z" fill="#10B981"/><path d="M -46 -320 L 0 -300 L 46 -320" fill="none" stroke="#F2F2F3" stroke-width="10" stroke-linecap="round"/>"""
    elif kind == 'cliente':
        acc_body = """<path d="M -60 -300 L -40 -60" stroke="#B45309" stroke-width="12" stroke-linecap="round"/>"""
    if pose == 'sit':
        leg2 = f'<g id="{p}leg2"><rect x="-10" y="-70" width="150" height="70" rx="35" fill="{far}"/><rect x="104" y="-40" width="56" height="110" rx="28" fill="{far}"/><ellipse cx="150" cy="78" rx="44" ry="24" fill="#2A2A2F"/></g>'
        leg1 = f'<g id="{p}leg1"><rect x="0" y="-74" width="160" height="74" rx="37" fill="{body}"/><rect x="118" y="-40" width="60" height="112" rx="30" fill="{body}"/><ellipse cx="168" cy="80" rx="48" ry="26" fill="#1E1E22"/></g>'
    else:
        leg2 = f'<g id="{p}leg2" transform="translate(-40 -30)"><rect x="-30" y="0" width="60" height="140" rx="30" fill="{far}"/><ellipse cx="14" cy="138" rx="46" ry="24" fill="#2A2A2F"/></g>'
        leg1 = f'<g id="{p}leg1" transform="translate(40 -30)"><rect x="-30" y="0" width="60" height="140" rx="30" fill="{body}"/><ellipse cx="14" cy="140" rx="48" ry="26" fill="#1E1E22"/></g>'
    rim1 = '' if kind == 'cliente' else '<path d="M 0 -330 C 105 -330, 150 -230, 150 -140 C 150 -40, 90 0, 0 0 C -90 0, -150 -40, -150 -140 C -150 -230, -105 -330, 0 -330 Z" fill="url(#gRim)"/>'
    rim2 = '' if kind == 'cliente' else '<circle cx="0" cy="-430" r="132" fill="url(#gRim)"/>'
    return f"""
<g id="{p}"><g transform="scale({facing * big} {big})">
 <ellipse cx="20" cy="12" rx="160" ry="16" fill="#000" opacity=".5" filter="url(#soft)"/>
 <g id="{p}body">
  {leg2}
  <g id="{p}arm2" transform="translate(-24 -290)"><ellipse cx="0" cy="96" rx="38" ry="100" fill="{far}"/><circle cx="0" cy="196" r="36" fill="{far}"/></g>
  <path d="M 0 -330 C 105 -330, 150 -230, 150 -140 C 150 -40, 90 0, 0 0 C -90 0, -150 -40, -150 -140 C -150 -230, -105 -330, 0 -330 Z" fill="{body}"/>
  {rim1}
  {acc_body}
  {leg1}
  <g id="{p}head" transform="translate(0 -300)"><g transform="translate(0 300)">
   <circle cx="0" cy="-430" r="132" fill="{head}"/>
   {rim2}
   {acc_head}
  </g></g>
  <g id="{p}arm1" transform="translate(28 -290)"><ellipse cx="0" cy="96" rx="40" ry="102" fill="{body}"/><circle cx="0" cy="198" r="38" fill="{body}"/><g id="{p}hand"></g></g>
 </g>
 {fx(p, facing)}
</g></g>"""
