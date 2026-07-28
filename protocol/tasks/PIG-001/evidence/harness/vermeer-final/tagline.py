"""Vermeer, final pass — focused re-examination of ONE measurement.

`canvastext.py` reported `div.card-tagline` on `#/lists` at 4.10 against a 4.5 floor,
dark 1440x900, stable to two decimals across all five random canvas draws. Before that
is published as a finding it has to be shown NOT to be a single outlying edge pixel:
`worst` is a minimum over ~1300 glyph pixels, and a minimum can be produced by one
antialiased pixel sitting on something the element does not really paint over.

So this dumps the whole distribution instead of the minimum: for every glyph pixel of
every `.card-tagline` on the route, the backdrop it actually sits on and the ratio
there, reported as percentiles and as a histogram of distinct backdrops. If the low
value is one pixel it shows up as a lone tail; if the text genuinely sits on that
backdrop it shows up as mass.

Same two-shot method as the rest of this project (A = as rendered, B = glyphs
transparent, never `visibility:hidden`), `prefers-reduced-motion:reduce` emulated.

usage: python3 tagline.py <theme> <w> <h> <route> <selector>
"""
import collections, json, os, sys

V = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/vermeer-closing"
C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, V)
sys.path.insert(0, C)
import cdp, png, photos

OUT = os.path.dirname(os.path.abspath(__file__))
A_PNG = "/tmp/vf-tag-a-%d.png" % os.getpid()
B_PNG = "/tmp/vf-tag-b-%d.png" % os.getpid()
C_PNG = "/tmp/vf-tag-c-%d.png" % os.getpid()
THRESH = 60

PICK = r"""(function(sel){
 var out=[];
 [].forEach.call(document.querySelectorAll(sel),function(el){
  var txt=el.textContent||''; if(!txt.trim())return;
  var cs=getComputedStyle(el); var r=el.getBoundingClientRect();
  if(r.width<2||r.height<2)return;
  if(r.top<0||r.bottom>window.innerHeight||r.left<0||r.right>window.innerWidth)return;
  var p=cs.color.match(/[\d.]+/g);
  var par=el.parentElement, pcs=par?getComputedStyle(par):null;
  out.push({rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
   ink:[+p[0],+p[1],+p[2]], fpx:parseFloat(cs.fontSize),
   text:txt.trim().replace(/\s+/g,' ').slice(0,44),
   ownBg:cs.backgroundColor, parentBg:pcs?pcs.backgroundColor:null,
   parentSel:par?par.tagName.toLowerCase()+(par.classList.length?'.'+[].slice.call(par.classList).join('.'):''):null});});
 return JSON.stringify(out);})(%s)"""


def main(theme, vw, vh, route, sel):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9421")))
    b.cmd("Page.addScriptToEvaluateOnNewDocument",
          {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
    b.cmd("Emulation.setEmulatedMedia",
          {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
    b.metrics(vw, vh)
    rep = []
    try:
        for scroll in (0, 400, 800, 1200):
            b.goto("%s/index.html?vft=%d%s" % (cdp.BASE, scroll, route), settle=2.0)
            assert b.ev("document.documentElement.dataset.theme") == theme
            assert b.ev("window.innerWidth") == vw
            photos.wait_settled(b)
            if scroll:
                b.ev("window.scrollTo(0,%d)" % scroll)
                b.ev("new Promise(function(r){setTimeout(r,500)})", await_promise=True)
            b.ev("(function(){var o=document.getElementById('vf-nocanvas');"
                 "if(o)o.remove();return 1;})()")
            els = json.loads(b.ev(PICK % json.dumps(sel)))
            if not els:
                print("scroll %-5d no %s in viewport" % (scroll, sel), flush=True)
                continue
            box = (0, 0, vw, vh)
            photos.clip_shot(b, A_PNG, box)
            b.ev(photos.HIDE)
            b.ev("new Promise(function(r){setTimeout(r,260)})", await_promise=True)
            photos.clip_shot(b, B_PNG, box)
            # shot C: glyphs still transparent AND the generative canvas removed, so a
            # failing pixel can be attributed to the canvas or exonerated of it.
            b.ev("(function(){var s=document.createElement('style');s.id='vf-nocanvas';"
                 "s.textContent='#bg-canvas{display:none!important}';"
                 "document.head.appendChild(s);return 1;})()")
            b.ev("new Promise(function(r){setTimeout(r,260)})", await_promise=True)
            photos.clip_shot(b, C_PNG, box)
            A, B, Cm = png.Img(A_PNG), png.Img(B_PNG), png.Img(C_PNG)
            for e in els:
                x, y, w, h = e["rect"]
                ink = tuple(e["ink"])
                vals, bg_hist, worst_at = [], collections.Counter(), None
                canvas_px = 0
                for py in range(max(0, y), min(vh, y + h)):
                    for px_ in range(max(0, x), min(vw, x + w)):
                        a, bb = A.px(px_, py), B.px(px_, py)
                        if abs(a[0]-bb[0]) + abs(a[1]-bb[1]) + abs(a[2]-bb[2]) < THRESH:
                            continue
                        cc = Cm.px(px_, py)
                        r_ = png.ratio(ink, bb)
                        vals.append(r_)
                        bg_hist[bb] += 1
                        if abs(bb[0]-cc[0]) + abs(bb[1]-cc[1]) + abs(bb[2]-cc[2]) > 6:
                            canvas_px += 1
                        if worst_at is None or r_ < worst_at[0]:
                            worst_at = (r_, (px_, py), bb, cc)
                if not vals:
                    continue
                vals.sort()
                n = len(vals)
                pct = {p: round(vals[min(n - 1, int(n * p / 100.0))], 2)
                       for p in (0, 1, 5, 25, 50)}
                below = sum(1 for v in vals if v < 4.5)
                row = {"scroll": scroll, "text": e["text"], "fpx": e["fpx"],
                       "ink": list(ink), "ownBg": e["ownBg"], "parentSel": e["parentSel"],
                       "parentBg": e["parentBg"], "glyphPx": n,
                       "percentiles": pct, "pxBelow4.5": below,
                       "pctBelow4.5": round(100.0 * below / n, 1),
                       "worstPixel": {"ratio": round(worst_at[0], 2),
                                      "at": list(worst_at[1]), "backdrop": list(worst_at[2]),
                                      "backdropNoCanvas": list(worst_at[3]),
                                      "ratioNoCanvas": round(png.ratio(ink, worst_at[3]), 2)},
                       "glyphPxAffectedByCanvas": canvas_px,
                       "topBackdrops": [[list(k), v] for k, v in bg_hist.most_common(4)]}
                rep.append(row)
                print("scroll %-5d %-46s px=%-5d min=%.2f p1=%.2f p5=%.2f median=%.2f "
                      "below4.5=%d (%.1f%%) parent=%s bg=%s"
                      % (scroll, e["text"][:44], n, pct[0], pct[1], pct[5], pct[50],
                         below, row["pctBelow4.5"], e["parentSel"], e["parentBg"]),
                      flush=True)
    finally:
        try:
            b.close()
        except Exception:
            pass
    json.dump(rep, open(os.path.join(OUT, "tagline-%s-%d.json" % (theme, vw)), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5])
