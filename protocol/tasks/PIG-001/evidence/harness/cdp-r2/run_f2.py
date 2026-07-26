"""F2 — timeline bar-label ink on real glyph pixels.

Same glyph-diff technique as the hero measurement: screenshot with the labels
painted (A) and with them hidden (B); a pixel counts only where |A-B| is large,
which confines the sample to where a glyph actually lands and so cannot stray
onto the page behind the bar. Score the bar's inherited ink against B at those
pixels. This resolves both the flat fills and the linear-gradient fade that
living painters' bars use, which no computed-style walk can reach.
"""
import json, sys
import cdp, png

A_PNG, B_PNG = "/tmp/vermeer-tl-a.png", "/tmp/vermeer-tl-b.png"
STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 7
THRESH = 45

COLLECT = r"""(function(){
 var out=[];
 [].forEach.call(document.querySelectorAll('a.tl2-bar'),function(a){
  var sp=a.querySelector('span'); if(!sp) return;
  var r=sp.getBoundingClientRect(), cr=a.getBoundingClientRect();
  if(r.width<3||r.height<3) return;
  if(cr.right<0||cr.left>innerWidth||cr.bottom<0||cr.top>innerHeight) return;
  var p=getComputedStyle(a).color.match(/[\d.]+/g);
  out.push({name:(sp.textContent||'').trim().slice(0,34), ink:[+p[0],+p[1],+p[2]],
   living:/linear-gradient/.test(a.style.background||''),
   fill:(a.style.background||'').slice(0,60),
   rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
   bar:[Math.round(cr.left),Math.round(cr.top),Math.round(cr.width),Math.round(cr.height)]});});
 return JSON.stringify(out);})()"""

HIDE = "[].forEach.call(document.querySelectorAll('a.tl2-bar span'),function(s){s.style.visibility='hidden'});1"
SHOW = "[].forEach.call(document.querySelectorAll('a.tl2-bar span'),function(s){s.style.visibility=''});1"
SCROLL = ("(function(){var t=document.querySelector('.tl2-wrap');if(t)t.scrollLeft=%d;})()")


def main():
    b = cdp.Browser()
    res = {}
    try:
        b.metrics(1600, 1200)
        for theme in ("dark", "light"):
            b.cmd("Page.addScriptToEvaluateOnNewDocument",
                  {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
            b.goto("%s/index.html?tl2=%s#/timeline" % (cdp.BASE, theme), settle=2.6)
            assert b.ev("document.documentElement.dataset.theme") == theme
            sw = b.ev("document.querySelector('.tl2-wrap').scrollWidth")
            cw = b.ev("document.querySelector('.tl2-wrap').clientWidth")
            maxs = sw - cw
            allrows, skipped = [], 0
            for st in range(STEPS):
                b.ev(SCROLL % int(maxs * st / max(1, STEPS - 1)))
                b.ev("new Promise(function(r){setTimeout(r,340)})", await_promise=True)
                bars = json.loads(b.ev(COLLECT))
                b.shot(A_PNG)
                b.ev(HIDE)
                b.ev("new Promise(function(r){setTimeout(r,240)})", await_promise=True)
                b.shot(B_PNG)
                b.ev(SHOW)
                A, B = png.Img(A_PNG), png.Img(B_PNG)
                for bar in bars:
                    x, y, w, h = bar["rect"]
                    x0, y0 = max(0, x), max(0, y)
                    x1, y1 = min(A.w, x + w), min(A.h, y + h)
                    lo, lopx, ng = None, None, 0
                    for py in range(y0, y1):
                        for px_ in range(x0, x1):
                            a_, bb = A.px(px_, py), B.px(px_, py)
                            if abs(a_[0]-bb[0]) + abs(a_[1]-bb[1]) + abs(a_[2]-bb[2]) < THRESH:
                                continue
                            ng += 1
                            r = png.ratio(tuple(bar["ink"]), bb)
                            if lo is None or r < lo:
                                lo, lopx = r, bb
                    if lo is None:
                        skipped += 1
                        continue
                    allrows.append({"ratio": round(lo, 2), "name": bar["name"],
                                    "living": bar["living"], "ink": bar["ink"],
                                    "backdrop": list(lopx), "glyphPx": ng})
                print(" ", theme, "step", st, "bars", len(bars), flush=True)
            # dedupe by painter, keep worst
            best = {}
            for r in allrows:
                if r["name"] not in best or r["ratio"] < best[r["name"]]["ratio"]:
                    best[r["name"]] = r
            rows = sorted(best.values(), key=lambda z: z["ratio"])
            res[theme] = {"painters": len(rows), "samples": len(allrows), "skipped": skipped,
                          "worst": rows[0], "below45": [r for r in rows if r["ratio"] < 4.5],
                          "below30": [r for r in rows if r["ratio"] < 3.0]}
            print(theme, "painters", len(rows), "worst", rows[0], flush=True)
    finally:
        b.close()
    for t in ("dark", "light"):
        d = res[t]
        print("\n%s: %d distinct painters sampled, worst %.2f (%s), %d below 4.5, %d below 3.0"
              % (t, d["painters"], d["worst"]["ratio"], d["worst"]["name"],
                 len(d["below45"]), len(d["below30"])))
        for r in d["below45"][:14]:
            print("   %5.2f %-32s living=%-5s ink=%s backdrop=%s"
                  % (r["ratio"], r["name"], r["living"], r["ink"], r["backdrop"]))
    json.dump(res, open("timeline-ink.json", "w"), indent=1)


main()
