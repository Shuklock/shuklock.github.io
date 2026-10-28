import sys
from PIL import Image
def clean(src,dst,target_h,colors=16,flip=False):
    im=Image.open(src).convert('RGBA');px=im.load();W,H=im.size
    # knock out magenta (and the pinkish haze), by colour distance
    for y in range(H):
        for x in range(W):
            r,g,b,a=px[x,y]
            import colorsys
            h,sat,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
            if 0.78<h<0.92 and sat>0.55 and v>0.5:px[x,y]=(0,0,0,0)
    bb=im.getbbox();im=im.crop(bb)
    if flip:im=im.transpose(Image.FLIP_LEFT_RIGHT)
    sc=target_h/im.height;out=im.resize((max(1,round(im.width*sc)),target_h),Image.BOX)
    # drop semi-transparent fringe, then quantize colours
    a=out.split()[3].point(lambda v:255 if v>128 else 0);out.putalpha(a)
    rgb=out.convert('RGB').quantize(colors=colors,method=Image.MEDIANCUT,dither=Image.NONE).convert('RGB')
    rgb.putalpha(a)
    # dark outline on the silhouette edge
    o=rgb.load();w,h=rgb.size;res=rgb.copy();rp=res.load()
    for y in range(h):
        for x in range(w):
            if o[x,y][3] and any((nx<0 or ny<0 or nx>=w or ny>=h or o[nx,ny][3]==0) for nx,ny in((x-1,y),(x+1,y),(x,y-1),(x,y+1))):rp[x,y]=(10,8,24,255)
    res.save(dst);print(dst,res.size)
    return res
w=clean('/mnt/user-data/uploads/1793108350943.jpg','warlock.png',48)
i=clean('/mnt/user-data/uploads/1793108327751.jpg','pet_imp.png',44,colors=20)
# preview at 6x
for n in ['warlock','pet_imp']:
    im=Image.open(n+'.png');im.resize((im.width*6,im.height*6),Image.NEAREST).save(n+'_big.png')
