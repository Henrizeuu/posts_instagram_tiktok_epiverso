import sys
from PIL import Image
out=sys.argv[1]; files=sys.argv[2:]; H=int(__import__('os').environ.get('CH','540'))
ims=[Image.open(f).convert('RGB') for f in files]; ims=[i.resize((int(i.width*H/i.height),H)) for i in ims]
cols=int(__import__('os').environ.get('COLS','4')); rows=(len(ims)+cols-1)//cols; w=max(i.width for i in ims)
c=Image.new('RGB',(cols*w+(cols-1)*8,rows*H+(rows-1)*8),(40,40,40))
for k,i in enumerate(ims): c.paste(i,((k%cols)*(w+8),(k//cols)*(H+8)))
c.save(out,quality=88)
