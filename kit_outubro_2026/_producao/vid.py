import os, subprocess, tempfile, shutil
from kit import *
FPS = 30
def anim_clip(body, out, dur, css='', w=1080, h=1920):
    """Render an animated HTML scene to an mp4 (no audio)."""
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, dir=S+'/build') as f:
        f.write(html(body, css)); p = f.name
    d = tempfile.mkdtemp(dir=S+'/build')
    subprocess.run(['node', S+'/build/frames.mjs', p, d, str(dur), str(FPS), str(w), str(h)], check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-framerate',str(FPS),'-i',d+'/f%05d.jpg','-c:v','libx264','-pix_fmt','yuv420p','-crf','16','-preset','medium',out], check=True)
    shutil.rmtree(d); os.unlink(p); return out

def cut(src, start, dur, out, vf=None):
    args=['ffmpeg','-v','error','-y','-ss',str(start),'-i',src,'-t',str(dur),'-an','-r',str(FPS)]
    if vf: args+=['-vf',vf]
    subprocess.run(args+['-c:v','libx264','-pix_fmt','yuv420p','-crf','16',out], check=True); return out

def concat(clips, out):
    lst = out + '.txt'
    open(lst,'w').write(''.join(f"file '{c}'\n" for c in clips))
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',lst,'-c','copy',out], check=True); os.unlink(lst); return out

def mix(video, out, sfx=(), voice=None, voice_at=0.0, voice_vol=1.0, bed=None, bed_vol=0.2):
    """sfx: list of (name, time, vol). Mix to AAC 48k stereo, -14 LUFS-ish."""
    dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',video]).strip())
    ins=['-i',video]; flt=[]; labels=[]
    k=1
    for name,t,vol in sfx:
        ins+=['-i',f'{S}/sfx/{name}.wav']; flt.append(f'[{k}:a]adelay={int(t*1000)}|{int(t*1000)},volume={vol}[a{k}]'); labels.append(f'[a{k}]'); k+=1
    if voice:
        ins+=['-i',voice]; flt.append(f'[{k}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(voice_at*1000)}|{int(voice_at*1000)},volume={voice_vol}[a{k}]'); labels.append(f'[a{k}]'); k+=1
    if bed:
        ins+=['-i',bed]; flt.append(f'[{k}:a]aresample=48000,volume={bed_vol}[a{k}]'); labels.append(f'[a{k}]'); k+=1
    flt.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{dur}[sil]")
    flt.append(f"[sil]{''.join(labels)}amix=inputs={len(labels)+1}:normalize=0,atrim=0:{dur},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]")
    subprocess.run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',';'.join(flt),'-map','0:v','-map','[aout]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-shortest','-movflags','+faststart',out], check=True)
    return out
