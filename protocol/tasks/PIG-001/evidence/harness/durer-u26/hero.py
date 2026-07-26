"""Unit-26 hero contrast: real glyph pixels, real fresh covers PLUS a forced
worst-case cover (opaque white in dark, opaque black in light).

Method is Vermeer's run_c2.py: two shots per load, one with hero text painted and
one with it hidden; a pixel counts only where the two differ strongly. Ink is the
declared paint (the four gradient stops for the background-clip:text title,
computed colour otherwise); backdrop is that pixel with the text hidden.

usage: python3 hero.py <N-fresh-covers> [tag] [width height]
"""
import json, sys, os
H = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, H)
import cdp, png

N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
TAG = sys.argv[2] if len(sys.argv) > 2 else "run"
VW = int(sys.argv[3]) if len(sys.argv) > 3 else 1440
VH = int(sys.argv[4]) if len(sys.argv) > 4 else 900
A_PNG, B_PNG = "/tmp/durer-hero-a.png", "/tmp/durer-hero-b.png"
THRESH = 60

COLLECT = r"""(function(){
 var out=[], hero=document.querySelector('.home-hero');
 [].forEach.call(hero.querySelectorAll('*'),function(el){
  var txt='';for(var j=0;j<el.childNodes.length;j++){var cn=el.childNodes[j];
   if(cn.nodeType===3)txt+=cn.nodeValue;}
  if(!txt.trim())return;
  var cs=getComputedStyle(el); if(cs.display==='none'||cs.visibility==='hidden')return;
  var r=el.getBoundingClientRect(); if(r.width<2||r.height<2)return;
  var fpx=parseFloat(cs.fontSize), wt=parseInt(cs.fontWeight,10)||400;
  var inks=[], clip=cs.webkitBackgroundClip||cs.backgroundClip||'';
  if(clip==='text'){var m=cs.backgroundImage.match(/rgba?\([^)]+\)/g)||[];
   inks=m.map(function(s){var p=s.match(/[\d.]+/g);return [+p[0],+p[1],+p[2]];});}
  else {var p=cs.color.match(/[\d.]+/g); inks=[[+p[0],+p[1],+p[2]]];}
  out.push({sel:el.tagName.toLowerCase()+(el.classList.length?'.'+[].slice.call(el.classList).join('.'):''),
   text:txt.trim().replace(/\s+/g,' ').slice(0,30),
   rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
   fpx:fpx, large:(fpx>=24||(fpx>=18.66&&wt>=700)), inks:inks, clip:clip});});
 return JSON.stringify(out);})()"""

HIDE = ("[].forEach.call(document.querySelector('.home-hero').querySelectorAll('*'),"
        "function(el){var t='';for(var j=0;j<el.childNodes.length;j++){var c=el.childNodes[j];"
        "if(c.nodeType===3)t+=c.nodeValue;} if(t.trim())el.style.visibility='hidden';});1")

# Force the operative layer (the in-hero cover canvas, opacity 1) to a fully
# opaque worst-case pixel everywhere.  Dark ink is light, so its worst backdrop
# is white; light ink is dark, so its worst backdrop is black.
FORCE = """(function(col){var c=document.querySelector('.home-hero canvas');
 var x=c.getContext('2d'); x.globalCompositeOperation='source-over';
 x.fillStyle=col; x.fillRect(0,0,c.width,c.height);
 return c.width+'x'+c.height+' filled '+col;})(%r)"""

WORST_COVER = {"dark": "#ffffff", "light": "#000000"}


def measure(b, els, tagname, store):
    b.shot(A_PNG)
    b.ev(HIDE)
    b.ev("new Promise(function(r){setTimeout(r,260)})", await_promise=True)
    b.shot(B_PNG)
    A, B = png.Img(A_PNG), png.Img(B_PNG)
    for e in els:
        x, y, w, h = e["rect"]
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(A.w, x + w), min(A.h, y + h)
        lo, lopx, ng = None, None, 0
        for py in range(y0, y1):
            for px_ in range(x0, x1):
                a, bb = A.px(px_, py), B.px(px_, py)
                if abs(a[0]-bb[0]) + abs(a[1]-bb[1]) + abs(a[2]-bb[2]) < THRESH:
                    continue
                ng += 1
                for ink in e["inks"]:
                    r = png.ratio(tuple(ink), bb)
                    if lo is None or r < lo:
                        lo, lopx = r, (tuple(ink), bb)
        if lo is None:
            continue
        need = 3.0 if e["large"] else 4.5
        k = (tagname, e["sel"])
        if k not in store or lo < store[k]["ratio"]:
            store[k] = {"ratio": lo, "need": need, "px": lopx, "glyphPx": ng,
                        "text": e["text"], "fpx": e["fpx"]}


def main():
    b = cdp.Browser()
    obs, forced = {}, {}
    try:
        b.metrics(VW, VH)
        for theme in ("dark", "light"):
            b.cmd("Page.addScriptToEvaluateOnNewDocument",
                  {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
            for it in range(N):
                b.goto("%s/index.html?u26=%s%d#/" % (cdp.BASE, theme, it), settle=2.3)
                assert b.ev("document.documentElement.dataset.theme") == theme
                els = json.loads(b.ev(COLLECT))
                measure(b, els, theme, obs)
                print(theme, "fresh cover", it, "ok", flush=True)
            b.goto("%s/index.html?u26=%sW#/" % (cdp.BASE, theme), settle=2.3)
            els = json.loads(b.ev(COLLECT))
            print("  forced:", b.ev(FORCE % WORST_COVER[theme]))
            b.ev("new Promise(function(r){setTimeout(r,300)})", await_promise=True)
            measure(b, els, theme, forced)
            print(theme, "worst-case cover ok", flush=True)
    finally:
        b.close()

    def dump(title, store):
        print("\n%s" % title)
        rows = []
        for (theme, sel), v in sorted(store.items()):
            verdict = "PASS" if v["ratio"] >= v["need"] else "FAIL"
            rows.append({"theme": theme, "selector": sel, "worst": round(v["ratio"], 2),
                         "need": v["need"], "verdict": verdict, "ink": list(v["px"][0]),
                         "backdrop": list(v["px"][1]), "fontpx": v["fpx"],
                         "glyphPixels": v["glyphPx"], "text": v["text"]})
            print("  %-6s %-18s %6.2f  need %.1f  %-4s  ink %-18s backdrop %-18s %.0fpx  %d glyph-px"
                  % (theme, sel, v["ratio"], v["need"], verdict,
                     str(v["px"][0]), str(v["px"][1]), v["fpx"], v["glyphPx"]))
        return rows

    r1 = dump("OBSERVED — worst of %d fresh covers per theme (%dx%d):" % (N, VW, VH), obs)
    r2 = dump("BOUND — forced worst-case opaque cover pixel (%dx%d):" % (VW, VH), forced)
    json.dump({"viewport": [VW, VH], "freshCovers": N, "observed": r1, "worstCaseBound": r2},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "hero-%s.json" % TAG), "w"), indent=1)


main()
