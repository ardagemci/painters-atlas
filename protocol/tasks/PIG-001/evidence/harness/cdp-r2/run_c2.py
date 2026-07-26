"""C2 — hero contrast measured on real glyph pixels only.

Two screenshots per load: text visible (A) and text hidden (B). A pixel counts
as a glyph pixel where |A-B| is large, which excludes the large parts of a text
box that no glyph ever touches. The ink is the declared paint (gradient stops
for the background-clip:text title, computed colour otherwise); the backdrop is
that same pixel in B, i.e. everything actually painted behind the glyph.
Also inventories the canvases behind the hero, since the published bound was
computed against #bg-canvas at opacity .6.
"""
import json, sys
import cdp, png

N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
A_PNG, B_PNG = "/tmp/vermeer-hero-a.png", "/tmp/vermeer-hero-b.png"
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

CANVASES = r"""(function(){
 var hero=document.querySelector('.home-hero'), hr=hero.getBoundingClientRect();
 return JSON.stringify([].map.call(document.querySelectorAll('canvas'),function(c){
  var cs=getComputedStyle(c), r=c.getBoundingClientRect();
  return {id:c.id||null, cls:c.className||null, opacity:cs.opacity,
   inHero:hero.contains(c),
   coversHero:(r.left<=hr.left+2&&r.right>=hr.right-2&&r.top<=hr.top+2&&r.bottom>=hr.bottom-2),
   rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]};}));})()"""

HIDE = ("[].forEach.call(document.querySelector('.home-hero').querySelectorAll('*'),"
        "function(el){var t='';for(var j=0;j<el.childNodes.length;j++){var c=el.childNodes[j];"
        "if(c.nodeType===3)t+=c.nodeValue;} if(t.trim())el.style.visibility='hidden';});1")


def main():
    b = cdp.Browser()
    worst, inv = {}, None
    try:
        b.metrics(1440, 900)
        for theme in ("light", "dark"):
            b.cmd("Page.addScriptToEvaluateOnNewDocument",
                  {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
            for it in range(N):
                b.goto("%s/index.html?h2=%s%d#/" % (cdp.BASE, theme, it), settle=2.3)
                assert b.ev("document.documentElement.dataset.theme") == theme
                els = json.loads(b.ev(COLLECT))
                if inv is None:
                    inv = json.loads(b.ev(CANVASES))
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
                    k = (theme, e["sel"])
                    if k not in worst or lo < worst[k]["ratio"]:
                        worst[k] = {"ratio": lo, "need": need, "px": lopx, "glyphPx": ng,
                                    "text": e["text"], "fpx": e["fpx"], "iter": it}
                print(theme, it, "ok", flush=True)
    finally:
        b.close()

    print("\nCANVASES behind the hero:", json.dumps(inv))
    print("\nWORST OBSERVED on real glyph pixels, %d fresh covers per theme:" % N)
    rows = []
    for (theme, sel), v in sorted(worst.items()):
        verdict = "PASS" if v["ratio"] >= v["need"] else "FAIL"
        rows.append({"theme": theme, "selector": sel, "worst": round(v["ratio"], 2),
                     "need": v["need"], "verdict": verdict, "ink": list(v["px"][0]),
                     "backdrop": list(v["px"][1]), "fontpx": v["fpx"],
                     "glyphPixels": v["glyphPx"], "text": v["text"]})
        print("  %-6s %-22s %6.2f  need %.1f  %-4s  ink %-16s backdrop %-16s %.0fpx"
              % (theme, sel, v["ratio"], v["need"], verdict,
                 str(v["px"][0]), str(v["px"][1]), v["fpx"]))
    json.dump({"canvases": inv, "rows": rows}, open("hero-composite.json", "w"), indent=1)


main()
