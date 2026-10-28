# Turn a Gemini pixel-art still on magenta into a game sprite: find its pixel grid, sample one
# colour per cell, keep every colour, outline the edge, drop specks. This is how the warlock and
# the imp, voidwalker and succubus sprites were made.
#
#   python3 tools/grid.py render.jpg pet_felh            # -> drain-soul/art/pet_felh.png
#   python3 tools/grid.py render.jpg pet_felh --flip     # mirror it (sprites face right)
#   python3 tools/grid.py render.jpg some/where.png --preview
import argparse, numpy as np
from PIL import Image
from artpath import out_path, preview
OUTLINE=(14,10,28,255)
def magenta(a):
    r,g,b=a[...,0],a[...,1],a[...,2]
    return (r>150)&(b>120)&(g<140)&((r-g)>60)&((b-g)>40)
def period(sig,lo=8,hi=40):
    sig=sig-sig.mean();best=(0,lo)
    for p in range(lo,hi):
        sc=sum(sig[i::p].sum()**2 for i in range(p))/p
        if sc>best[0]:best=(sc,p)
    return best[1]
def grid(src,flip=False,cell=None):
    a=np.array(Image.open(src).convert('RGB')).astype(int);mag=magenta(a)
    # ignore stray haze: keep rows/cols with a real amount of content
    cols=np.where((~mag).sum(axis=0)>8)[0];rows=np.where((~mag).sum(axis=1)>8)[0]
    x0,x1,y0,y1=cols.min(),cols.max()+1,rows.min(),rows.max()+1
    crop=a[y0:y1,x0:x1]
    if cell:p=cell
    else:
        gx=np.abs(np.diff(crop,axis=1)).sum(axis=2).sum(axis=0);gy=np.abs(np.diff(crop,axis=0)).sum(axis=2).sum(axis=1)
        p=(period(gx)+period(gy))/2
    W=int(round((x1-x0)/p));H=int(round((y1-y0)/p))
    out=Image.new('RGBA',(W,H));o=out.load()
    for j in range(H):
        for i in range(W):
            sx=min(a.shape[1]-1,max(0,int(x0+(i+.5)*p)));sy=min(a.shape[0]-1,max(0,int(y0+(j+.5)*p)))
            win=(slice(max(0,sy-2),sy+3),slice(max(0,sx-2),sx+3))
            o[i,j]=tuple(int(v) for v in a[win].reshape(-1,3).mean(axis=0))+(0 if mag[win].mean()>.5 else 255,)
    out=out.crop(out.getbbox())
    if flip:out=out.transpose(Image.FLIP_LEFT_RIGHT)
    px=out.load();w,h=out.size;res=out.copy();rp=res.load()
    for y in range(h):
        for x in range(w):
            if px[x,y][3] and any((nx<0 or ny<0 or nx>=w or ny>=h or px[nx,ny][3]==0) for nx,ny in((x-1,y),(x+1,y),(x,y-1),(x,y+1))):rp[x,y]=OUTLINE
    for y in range(h):  # drop isolated specks
        for x in range(w):
            if rp[x,y][3] and sum(1 for nx,ny in((x-1,y),(x+1,y),(x,y-1),(x,y+1)) if 0<=nx<w and 0<=ny<h and rp[nx,ny][3])<2:rp[x,y]=(0,0,0,0)
    return res,p
if __name__=='__main__':
    ap=argparse.ArgumentParser(description='Gemini still on magenta -> crisp sprite PNG.')
    ap.add_argument('src');ap.add_argument('out',help='sprite name (written to drain-soul/art/) or a path')
    ap.add_argument('--flip',action='store_true',help='mirror horizontally')
    ap.add_argument('--cell',type=float,help='grid cell size in source pixels (default: detect)')
    ap.add_argument('--preview',action='store_true',help='also write a 6x copy to tools/preview/')
    a=ap.parse_args()
    res,p=grid(a.src,a.flip,a.cell);dst=out_path(a.out);res.save(dst)
    print(dst,res.size,'grid %.1f'%p)
    print('ART entry: {frames:1,fps:1,scale:S} where S*%d is the height you want in game pixels (warlock: .36*151=54)'%res.height)
    if a.preview:preview(res,dst.stem)
