# Turn a Gemini pixel-art still on magenta into a crisp sprite: find its pixel grid, sample one colour per cell, keep every colour, outline the edge.
# usage: python3 grid.py in.jpg out.png
import sys, numpy as np
from PIL import Image
src,dst=sys.argv[1],sys.argv[2]
a=np.array(Image.open(src).convert('RGB')).astype(int)
r,g,b=a[...,0],a[...,1],a[...,2];mag=(r>150)&(b>120)&(g<140)&((r-g)>60)&((b-g)>40)
ys,xs=np.where(~mag)
# ignore stray haze: keep rows/cols with a real amount of content
cols=np.where((~mag).sum(axis=0)>8)[0];rows=np.where((~mag).sum(axis=1)>8)[0]
x0,x1,y0,y1=cols.min(),cols.max()+1,rows.min(),rows.max()+1
crop=a[y0:y1,x0:x1];gx=np.abs(np.diff(crop,axis=1)).sum(axis=2).sum(axis=0);gy=np.abs(np.diff(crop,axis=0)).sum(axis=2).sum(axis=1)
def period(sig):
    sig=sig-sig.mean();best=(0,0)
    for p in range(8,40):
        sc=sum(sig[i::p].sum()**2 for i in range(p))/p
        if sc>best[0]:best=(sc,p)
    return best[1]
p=(period(gx)+period(gy))/2
W=int(round((x1-x0)/p));H=int(round((y1-y0)/p))
out=Image.new('RGBA',(W,H));o=out.load()
for j in range(H):
    for i in range(W):
        sx=min(a.shape[1]-1,max(0,int(x0+(i+.5)*p)));sy=min(a.shape[0]-1,max(0,int(y0+(j+.5)*p)))
        patch=a[max(0,sy-2):sy+3,max(0,sx-2):sx+3].reshape(-1,3).mean(axis=0);m=mag[max(0,sy-2):sy+3,max(0,sx-2):sx+3].mean()
        o[i,j]=tuple(int(v) for v in patch)+(0 if m>.5 else 255,)
out=out.crop(out.getbbox())
px=out.load();w,h=out.size;res=out.copy();rp=res.load()
for y in range(h):
    for x in range(w):
        if px[x,y][3] and any((nx<0 or ny<0 or nx>=w or ny>=h or px[nx,ny][3]==0) for nx,ny in((x-1,y),(x+1,y),(x,y-1),(x,y+1))):rp[x,y]=(14,10,28,255)
# drop isolated specks
for y in range(h):
    for x in range(w):
        if rp[x,y][3] and sum(1 for nx,ny in((x-1,y),(x+1,y),(x,y-1),(x,y+1)) if 0<=nx<w and 0<=ny<h and rp[nx,ny][3])<2:rp[x,y]=(0,0,0,0)
res.save(dst);print(dst,res.size,'grid',p)
