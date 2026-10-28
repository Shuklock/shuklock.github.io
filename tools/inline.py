# index.html carries base64 copies of a few art files (ART_INLINE, BG_INLINE) so the scene draws
# before the art/ folder loads, and when the page is opened from disk. Run this after replacing
# one of those files so the copy matches.
#
#   python3 tools/inline.py          # rewrite any stale copies
#   python3 tools/inline.py --check  # exit 1 if any copy differs from its file
# To inline a backdrop again, put it in BG_INLINE as key:'data:...' and add it to FILES below.
import argparse, base64, re, sys
from artpath import ROOT, ART_DIR
HTML=ROOT/'drain-soul'/'index.html'
# key inside ART_INLINE / BG_INLINE -> file in art/
FILES={'warlock':'warlock.png'}
MIME={'.png':'image/png','.jpg':'image/jpeg'}
ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
s=HTML.read_text();stale=[]
for key,fn in FILES.items():
    f=ART_DIR/fn;want='data:%s;base64,%s'%(MIME[f.suffix],base64.b64encode(f.read_bytes()).decode())
    m=re.search(r"\b%s:'(data:image/[^']+)'"%key,s)
    if not m:sys.exit('no inline copy for '+key)
    if m.group(1)!=want:stale.append(key);s=s[:m.start(1)]+want+s[m.end(1):]
    print(key,'stale' if key in stale else 'ok')
if stale and not a.check:HTML.write_text(s);print('updated',HTML.relative_to(ROOT))
sys.exit(1 if stale and a.check else 0)
