# Shared path handling for the sprite tools.
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
ART_DIR=ROOT/'drain-soul'/'art'
PREVIEW_DIR=ROOT/'tools'/'preview'
def out_path(arg):
    """'pet_felh' -> drain-soul/art/pet_felh.png; anything with a slash or an extension is used as given."""
    p=Path(arg)
    if p.suffix or len(p.parts)>1:return p
    return ART_DIR/(arg+'.png')
def preview(im,name,scale=6):
    from PIL import Image
    PREVIEW_DIR.mkdir(exist_ok=True);p=PREVIEW_DIR/(name+'_big.png')
    bg=Image.new('RGBA',(im.width*scale,im.height*scale),(60,60,70,255))
    bg.alpha_composite(im.resize(bg.size,Image.NEAREST));bg.save(p);print('preview',p)
