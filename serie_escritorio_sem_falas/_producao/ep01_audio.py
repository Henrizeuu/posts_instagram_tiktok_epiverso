from synth import *
DUR = 14.0; N = int(DUR * SR); mix = np.zeros(N)
def put(y, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(y)); mix[i:j] += y[:j - i] * g
# digitação calma e depois desesperada (mesmos tempos dos braços)
t = .1; i = 0
while t <= 1.3: put(click(i), t, 1.3); t += .16; i += 1
t = 7.7
while t <= 10.1: put(click(i), t, 1.3); t += .066; i += 1
# A: "bora pra casa"
put(pop(), 1.45, .6); put(talk(250, 6, 1, rise=.25), 1.55, .55)
# espreguiçada
put(glide(300, 720, .35, .35), 3.55); put(syll(230, .6, 'a', -.3), 3.75, .4)
# celular 1
put(buzz(.95), 4.1, .22); put(pop(), 4.35, .6); put(talk(330, 9, 7, rise=.3, tel=True), 4.45, .5)
# A: "hmmm…"
put(pop(), 6.7, .5); put(syll(165, .28, 'u', -.1), 6.8, .45); put(syll(150, .38, 'u', -.25), 7.12, .45)
# timelapse: tique-taque acelerando
t = 7.7; dt = .14
while t < 10.1: put(tick(2400 + (t - 7.7) * 300), t, 1.1); t += dt; dt = max(.035, dt * .93)
# murchando
put(deflate(.9), 10.3, .7)
# celular 2
put(buzz(.8), 10.9, .22); put(pop(), 11.1, .6); put(talk(350, 11, 21, rise=.4, speed=1.25, tel=True), 11.2, .5)
# bandeira branca + gemidinho
put(fwip(), 11.95, .8); put(syll(380, .22, 'i', -.3), 12.3, .35); put(syll(330, .4, 'i', -.45), 12.55, .35)
mix = mix / np.abs(mix).max() * .9
st = np.stack([mix, mix], 1); pcm = (st * 32767).astype(np.int16)
with wave.open('ep01b.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok')
