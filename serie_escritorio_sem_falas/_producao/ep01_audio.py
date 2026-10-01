from synth import *
DUR = 11.6; N = int(DUR * SR); mix = np.zeros(N)
def put(y, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(y)); mix[i:j] += y[:j - i] * g
# digitação calma e depois desesperada (mesmos tempos dos braços)
t = .1; i = 0
while t <= 1.2: put(click(i), t, 1.3); t += .16; i += 1
t = 5.9
while t <= 8.3: put(click(i), t, 1.3); t += .066; i += 1
# A: "bora pra casa"
put(pop(), 1.35, .6); put(talk(250, 6, 1, rise=.25), 1.45, .55)
# espreguiçada
put(glide(300, 720, .35, .35), 2.85); put(syll(230, .6, 'a', -.3), 3.05, .4)
# celular 1
put(buzz(.95), 3.5, .22); put(pop(), 3.75, .6); put(talk(330, 9, 7, rise=.3, tel=True), 3.85, .5)
# A: "hmmm…"
put(pop(), 5.0, .5); put(syll(165, .28, 'u', -.1), 5.1, .45); put(syll(150, .38, 'u', -.25), 5.42, .45)
# timelapse: tique-taque acelerando
t = 5.9; dt = .14
while t < 8.3: put(tick(2400 + (t - 5.9) * 300), t, 1.1); t += dt; dt = max(.035, dt * .93)
# murchando
put(deflate(.9), 8.5, .7)
# celular 2
put(buzz(.8), 9.15, .22); put(pop(), 9.35, .6); put(talk(350, 11, 21, rise=.4, speed=1.25, tel=True), 9.45, .5)
# bandeira branca + gemidinho
put(fwip(), 10.02, .8); put(syll(380, .22, 'i', -.3), 10.35, .35); put(syll(330, .4, 'i', -.45), 10.6, .35)
mix = mix / np.abs(mix).max() * .9
st = np.stack([mix, mix], 1); pcm = (st * 32767).astype(np.int16)
with wave.open('ep01.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok')
