import numpy as np, scipy.io.wavfile as w, os
SR=48000; D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/sfx/'
rng=np.random.default_rng(7)
def save(n,x):
    x=x/ (np.abs(x).max()+1e-9)*0.9; w.write(D+n+'.wav',SR,(np.stack([x,x],1)*32767).astype(np.int16))
def env(n,a,d): t=np.arange(n)/SR; e=np.minimum(t/a,1)*np.exp(-t/d); return e
# whoosh: noise through moving bandpass approximated by smoothing
n=int(SR*.55); x=rng.standard_normal(n); t=np.arange(n)/n
from scipy.signal import butter, sosfilt
out=np.zeros(n)
for i,(lo,hi) in enumerate([(300,900),(700,2000),(1500,4000),(3000,7000)]):
    sos=butter(2,[lo,hi],btype='band',fs=SR,output='sos'); out+=sosfilt(sos,x)*np.exp(-((t-(.25+i*.12))/.12)**2)
save('whoosh',out*np.sin(np.pi*t)**.5)
# click
n=int(SR*.05); c=rng.standard_normal(n)*env(n,.0005,.006); sos=butter(2,2500,btype='high',fs=SR,output='sos'); save('click',sosfilt(sos,c))
# pop
n=int(SR*.12); tt=np.arange(n)/SR; f=900*np.exp(-tt*30)+300; save('pop',np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.001,.03))
# ding (two partials)
n=int(SR*1.4); tt=np.arange(n)/SR; d=(np.sin(2*np.pi*1318.5*tt)+.5*np.sin(2*np.pi*2637*tt)+.25*np.sin(2*np.pi*1975.5*tt))*env(n,.002,.35); save('ding',d)
# notify (two-tone plim)
n=int(SR*.5); tt=np.arange(n)/SR; a=np.sin(2*np.pi*987.8*tt)*env(n,.002,.08); b=np.zeros(n); k=int(SR*.11); b[k:]=np.sin(2*np.pi*1318.5*tt[:n-k])*env(n-k,.002,.15); save('notify',a+b)
# typing: 14 keystrokes
n=int(SR*1.6); ty=np.zeros(n)
for i in range(14):
    s=max(0,int(SR*(i*.105+rng.uniform(-.02,.02)))+500); m=int(SR*.03)
    if s+m<n: ty[s:s+m]+=sosfilt(butter(2,[1500,6000],btype='band',fs=SR,output='sos'),rng.standard_normal(m))*env(m,.0003,.004)*rng.uniform(.6,1)
save('typing',ty)
# bass hit / impact
n=int(SR*.9); tt=np.arange(n)/SR; f=110*np.exp(-tt*8)+42; save('impact',np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.002,.25)+0.3*rng.standard_normal(n)*env(n,.001,.02))
# tick (clock)
n=int(SR*.04); save('tick',sosfilt(butter(2,[2000,5000],btype='band',fs=SR,output='sos'),rng.standard_normal(n))*env(n,.0002,.003))
# riser
n=int(SR*1.2); tt=np.arange(n)/SR; f=200+800*(tt/tt[-1])**2; r=np.sin(2*np.pi*np.cumsum(f)/SR)*(tt/tt[-1])**2*.6+sosfilt(butter(2,3000,btype='high',fs=SR,output='sos'),rng.standard_normal(n))*(tt/tt[-1])**3*.4; save('riser',r)
print(sorted(os.listdir(D)))
