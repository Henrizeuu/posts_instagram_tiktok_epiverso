from synth import *
DUR = 16.6; N = int(DUR * SR); mix = np.zeros(N)
def put(y, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(y)); mix[i:j] += y[:j - i] * g
def step(heavy=False):
    n = int(.09 * SR); t = np.arange(n) / SR; f = 90 if heavy else 130
    return np.sin(2 * np.pi * f * t) * np.exp(-t / .03) * .8
def thud():
    n = int(.25 * SR); t = np.arange(n) / SR; rnd = np.random.default_rng(5)
    return (np.sin(2 * np.pi * 70 * t) * np.exp(-t / .07) + rnd.normal(0, .3, n) * np.exp(-t / .02)) * .9
def chime():
    n = int(.9 * SR); t = np.arange(n) / SR; y = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / .35) / (k + 1) for k, f in enumerate([1568, 2093, 2637]))
    return y * .4
def growl(dur=.9):
    n = int(dur * SR); t = np.arange(n) / SR; rnd = np.random.default_rng(2)
    y = np.sign(np.sin(2 * np.pi * (95 + 10 * np.sin(2 * np.pi * 9 * t)) * t)) * .4 + rnd.normal(0, .25, n)
    return y * env(n, .05, .2) * .5
def kettle(dur=1.6):
    n = int(dur * SR); t = np.arange(n) / SR; f = 1500 + 300 * (t / dur) + 30 * np.sin(2 * np.pi * 7 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .3, .2) * .18
t = .1; i = 0
while t <= 1.6: put(click(i), t, 1.2); t += .16; i += 1
for k_ in range(13): put(step(), 1.0 + k_ * .11, .5)
put(glide(500, 900, .12, .3), 2.0); put(thud(), 2.65, .7)
put(pop(), 2.75, .5); put(talk(300, 8, 31, rise=.15), 2.85, .5)
put(glide(420, 260, .18, .3), 3.3)
put(pop(), 4.85, .5); put(pop(), 4.95, .35); put(talk(310, 10, 33, rise=.2), 4.95, .5)
put(syll(220, .3, 'e', .4), 5.15, .4)
put(growl(.9), 5.95, .55)
put(pop(), 7.1, .5); put(pop(), 7.2, .35); put(talk(320, 9, 35, rise=.1), 7.2, .5)
put(kettle(1.7), 7.75, 1.0); put(talk(170, 10, 37, speed=1.5), 7.85, .45)
for k_ in range(12): put(step(True), 9.0 + k_ * .11, .55)
put(chime(), 9.9, .6)
put(pop(), 10.4, .5); put(talk(140, 7, 41, rise=.05), 10.5, .55)
put(syll(420, .35, 'i', .5), 10.9, .35); put(glide(500, 900, .12, .3), 10.8)
put(pop(), 12.6, .5); put(talk(140, 6, 43, rise=.35), 12.7, .55)
put(glide(300, 140, 1.2, .45, .05), 13.3)
put(chime(), 13.5, .5); put(syll(230, .7, 'a', -.35), 13.8, .4)
for k_ in range(11): put(step(), 14.9 + k_ * .14, .4)
mix = mix / np.abs(mix).max() * .9
st = np.stack([mix, mix], 1); pcm = (st * 32767).astype(np.int16)
with wave.open('ep02.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok')
