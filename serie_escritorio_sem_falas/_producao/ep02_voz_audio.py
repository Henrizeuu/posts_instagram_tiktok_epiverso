from synth import *
import subprocess
DUR = 25.8; N = int(DUR * SR); mix = np.zeros(N); vox = np.zeros(N)
def load(name):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', f'vox/{name}.wav', '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'])
    return np.frombuffer(raw, np.int16).astype(float) / 32768
def put(y, t, g=1.0, buf=None):
    b = mix if buf is None else buf; i = int(t * SR); j = min(N, i + len(y)); b[i:j] += y[:j - i] * g
def step(heavy=False):
    n = int(.09 * SR); t = np.arange(n) / SR; f = 90 if heavy else 130
    return np.sin(2 * np.pi * f * t) * np.exp(-t / .03) * .8
def thud():
    n = int(.25 * SR); t = np.arange(n) / SR; rnd = np.random.default_rng(5)
    return (np.sin(2 * np.pi * 70 * t) * np.exp(-t / .07) + rnd.normal(0, .3, n) * np.exp(-t / .02)) * .9
def chime():
    n = int(.9 * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-t / .35) / (k + 1) for k, f in enumerate([1568, 2093, 2637])) * .4
def kettle(dur=1.6):
    n = int(dur * SR); t = np.arange(n) / SR; f = 1500 + 300 * (t / dur) + 30 * np.sin(2 * np.pi * 7 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .3, .2) * .18
# efeitos
t = .1; i = 0
while t <= 1.6: put(click(i), t, .9); t += .16; i += 1
for k_ in range(13): put(step(), 1.0 + k_ * .11, .4)
put(thud(), 2.65, .6)
for tt in (2.75, 5.3, 8.55, 10.35, 15.0, 17.4, 19.8, 22.0, 23.35): put(pop(), tt, .25)
put(pop(), 5.35, .2); put(pop(), 10.4, .2)
put(kettle(2.6), 11.2, .7)
for k_ in range(12): put(step(True), 13.6 + k_ * .11, .45)
put(chime(), 14.4, .35); put(chime(), 17.45, .25)
put(glide(300, 140, 1.0, .25, .05), 22.3)
put(chime(), 23.5, .3)
for k_ in range(14): put(step(), 23.3 + k_ * .14, .3)
# vozes
for name, tt in [('C1', 2.85), ('C2', 5.4), ('F1', 8.6), ('C3', 10.4), ('S1', 15.1), ('C4', 17.45), ('S2', 19.9), ('C5', 22.05), ('F2', 23.4)]:
    put(load(name), tt, 1.0, vox)
vox = vox / (np.abs(vox).max() + 1e-9) * .9
fx = mix / (np.abs(mix).max() + 1e-9) * .35
out = vox + fx; out = out / np.abs(out).max() * .95
pcm = (np.stack([out, out], 1) * 32767).astype(np.int16)
with wave.open('ep02v.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok')
