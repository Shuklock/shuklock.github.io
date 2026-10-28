# Alternative to grid.py for a Gemini render that is NOT on a clean pixel grid (painterly or
# smoothly scaled): knock out magenta, crop, box-resize to a fixed height, quantize, outline.
# Gives a smaller, flatter sprite than grid.py. grid.py is the default.
#
#   python3 tools/clean.py render.jpg pet_felh --height 48 --colors 20 [--flip] [--preview]
import argparse, colorsys
from PIL import Image
from artpath import out_path, preview
OUTLINE=(10,8,24,255)
def clean(src,target_h,colors=16,flip=False):
    im=Image.open(src).convert('RGBA');px=im.load();W,H=im.size
    for y in range(H):  # knock out magenta (and the pinkish haze)
        for x in range(W):
            r,g,b,_=px[x,y];h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
            if 0.78<h<0.92 and s>0.55 and v>0.5:px[x,y]=(0,0,0,0)
    im=im.crop(im.getbbox())
    if flip:im=im.transpose(Image.FLIP_LEFT_RIGHT)
    sc=target_h/im.height;out=im.resize((max(1,round(im.width*sc)),target_h),Image.BOX)
    a=out.split()[3].point(lambda v:255 if v>128 else 0)  # drop the semi-transparent fringe
    rgb=out.convert('RGB').quantize(colors=colors,method=Image.MEDIANCUT,dither=Image.NONE).convert('RGBA');rgb.putalpha(a)
    o=rgb.load();w,h=rgb.size;res=rgb.copy();rp=res.load()
    for y in range(h):
        for x in range(w):
            if o[x,y][3] and any((nx<0 or ny<0 or nx>=w or ny>=h or o[nx,ny][3]==0) for nx,ny in((x-1,y),(x+1,y),(x,y-1),(x,y+1))):rp[x,y]=OUTLINE
    return res
if __name__=='__main__':
    ap=argparse.ArgumentParser(description='Gemini render on magenta -> quantized sprite at a fixed height.')
    ap.add_argument('src');ap.add_argument('out',help='sprite name (written to drain-soul/art/) or a path')
    ap.add_argument('--height',type=int,required=True);ap.add_argument('--colors',type=int,default=16)
    ap.add_argument('--flip',action='store_true');ap.add_argument('--preview',action='store_true')
    a=ap.parse_args()
    res=clean(a.src,a.height,a.colors,a.flip);dst=out_path(a.out);res.save(dst);print(dst,res.size)
    if a.preview:preview(res,dst.stem)
