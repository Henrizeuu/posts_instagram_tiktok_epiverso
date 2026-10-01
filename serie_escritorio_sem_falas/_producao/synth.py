"""Sons do episódio, todos sintetizados (sem direitos de terceiros)."""
import numpy as np, wave, sys
SR = 48000
def env(n, a=.008, r=.04):
    e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
VOW = {'a': (800, 1200), 'e': (450, 2000), 'i': (300, 2300), 'o': (500, 900), 'u': (350, 750)}
def syll(f0, dur, vowel, glide=0.0, rnd=None):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (1 + glide * t / dur) * (1 + .03 * np.sin(2 * np.pi * 6 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    F1, F2 = VOW[vowel]; y = np.zeros(n)
    for h in range(1, 14):
        fh = f0 * h; g = np.exp(-((fh - F1) / 260) ** 2) + .6 * np.exp(-((fh - F2) / 380) ** 2) + .08 / h
        y += g * np.sin(h * ph)
    if rnd is not None and rnd.random() < .6:  # consoante (ruído curto)
        k = int(.012 * SR); y[:k] += rnd.normal(0, .6, k) * np.linspace(1, 0, k)
    return y * env(n, .006, .035)
def talk(f0, n, seed, rise=0.0, speed=1.0, tel=False):
    rnd = np.random.default_rng(seed); out = []
    for i in range(n):
        d = rnd.uniform(.07, .12) / speed; v = rnd.choice(list(VOW))
        p = f0 * rnd.uniform(.88, 1.18) * (1 + rise * i / max(1, n - 1))
        out.append(syll(p, d, v, rnd.uniform(-.15, .15), rnd)); out.append(np.zeros(int(rnd.uniform(.012, .03) * SR)))
    y = np.concatenate(out)
    if tel:  # "voz de telefone": banda estreita + leve saturação
        Y = np.fft.rfft(y); fr = np.fft.rfftfreq(len(y), 1 / SR); Y[(fr < 380) | (fr > 3200)] *= .05; y = np.fft.irfft(Y, len(y))
        y = np.tanh(y * 2.2)
    return y / (np.abs(y).max() + 1e-9)
def buzz(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.sign(np.sin(2 * np.pi * 170 * t)) * .5 + np.sin(2 * np.pi * 85 * t)
    gate = (np.sin(2 * np.pi * 2.2 * t) > -.2).astype(float)
    return y * gate * env(n, .01, .05) * .5
def click(seed, amp=1.0):
    rnd = np.random.default_rng(seed); n = int(.025 * SR)
    y = rnd.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * .004)); y += .5 * np.sin(2 * np.pi * rnd.uniform(1800, 2600) * np.arange(n) / SR) * np.exp(-np.arange(n) / (SR * .006))
    return y * .35 * amp
def tick(f=2600):
    n = int(.03 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * f * t) * np.exp(-t / .004) * .5
def glide(f0, f1, dur, amp=.5, wob=0):
    n = int(dur * SR); t = np.arange(n) / SR; f = f0 + (f1 - f0) * (t / dur); ph = 2 * np.pi * np.cumsum(f * (1 + wob * np.sin(2 * np.pi * 7 * t))) / SR
    return (np.sin(ph) + .3 * np.sin(2 * ph)) * env(n, .01, .08) * amp
def deflate(dur=.9):
    n = int(dur * SR); t = np.arange(n) / SR; rnd = np.random.default_rng(3)
    noise = rnd.normal(0, 1, n); Y = np.fft.rfft(noise); fr = np.fft.rfftfreq(n, 1 / SR); Y[(fr < 600) | (fr > 5000)] = 0; noise = np.fft.irfft(Y, n)
    return (glide(420, 110, dur, .5, .04) + noise / np.abs(noise).max() * .25 * (1 - t / dur)) * env(n, .01, .2)
def pop():
    n = int(.08 * SR); t = np.arange(n) / SR; f = 500 + 900 * (t / .08); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .03) * .5
def fwip():
    n = int(.25 * SR); rnd = np.random.default_rng(9); y = rnd.normal(0, 1, n); Y = np.fft.rfft(y); fr = np.fft.rfftfreq(n, 1 / SR)
    Y[(fr < 1200) | (fr > 7000)] = 0; y = np.fft.irfft(Y, n); return y / np.abs(y).max() * env(n, .05, .15) * .35
