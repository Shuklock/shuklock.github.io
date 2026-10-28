# Glowing gem on black -> transparent PNG that keeps its glow. Used for the enemy stand-in crystals.
# The black around the gem (and its halo) is "unscreened": alpha from brightness, colour divided back
# out, so the glow composites over any backdrop. Pixels inside the gem's silhouette stay opaque, so its
# dark core doesn't turn see-through.
#
#   python3 tools/crystal.py gem.jpg mob_crystal_2 [--height 192]
import argparse, numpy as np
from PIL import Image
from scipy import ndimage
from artpath import out_path
def crystal(src,height):
    a=np.asarray(Image.open(src).convert('RGB')).astype(float)
    mx=a.max(axis=2)
    bg=ndimage.binary_fill_holes(mx>40)       # the gem and its bright rim, holes (dark core) filled
    bg=ndimage.binary_erosion(bg,iterations=6) # pull in past the soft edge so the halo stays translucent
    alpha=np.clip(mx/255*1.15,0,1);alpha[bg]=1
    rgb=np.where(bg[...,None],a,np.clip(a/np.maximum(alpha[...,None],1e-3),0,255))
    out=Image.fromarray(np.dstack([rgb,alpha*255]).astype(np.uint8),'RGBA')
    out=out.crop(Image.fromarray((alpha*255>40).astype(np.uint8)*255).getbbox())
    w=round(out.width*height/out.height);return out.resize((w,height),Image.LANCZOS)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('src');ap.add_argument('out');ap.add_argument('--height',type=int,default=192)
    a=ap.parse_args();im=crystal(a.src,a.height);p=out_path(a.out);im.save(p,optimize=True);print(p,im.size)
