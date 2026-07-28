"""What is the WORST backdrop `#bg-canvas` can present, over many random draws?

`span.count` was 4.13 in one unit-27 run and 5.01 in another: the cover is
`Math.random`-seeded, so a single draw is not a verdict and a per-element sample
is a lottery over BOTH the draw and where that element happens to sit. This
instrument removes both lotteries.

`#bg-canvas` paints gradients and strokes only — no images — so unlike the museum
photographs it is NOT cross-origin tainted and `getImageData()` works on it. So
the canvas is read EXACTLY, at its own backing resolution, and composited over
`--bg` in the same way the browser does (`out = bg*(1-op*a) + rgb*op*a`, where
`op` is the element opacity: .5 dark, .6 light). No screenshot, no glyph diff,
no sampling error, and every pixel of the surface is considered — including the
places no text happened to sit on the draw that was screenshotted.

What it returns is the canvas's own (colour, alpha) pairs, so the caller can
composite them over whatever base a given element actually sits on — measured
for real by `canvastext.py`'s third shot — instead of over an assumed `--bg`.
That distinction is not academic: unit 27 recorded `p.img-credit.mu-credit`
sitting on `[234,227,213]`, not on `--bg` `[242,236,223]`.

Two conservative properties, stated rather than assumed:
  - the canvas backing store is `innerWidth*.55 x innerHeight*.55` stretched to
    the viewport, so on-screen pixels are INTERPOLATIONS of these; interpolation
    cannot exceed the source range, so source extremes bound screen extremes.
  - each quantisation bucket is expanded to its worst corner (alpha rounded UP),
    so quantisation can only overstate the canvas's effect, never understate it.

For a given ink the worst pixel is the one whose composite luminance is CLOSEST
to the ink's, so the whole pair set is scanned rather than just the extremes —
the extremes alone would understate a mid-tone ink.

usage: python3 canvasextremes.py <theme> <w> <h> <draws> <tag>
"""
import json, os, sys

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp, png

OUT = os.path.dirname(os.path.abspath(__file__))

Q = 4                                          # colour/alpha quantisation step

READ = r"""(function(){
 var cv=document.getElementById('bg-canvas');
 if(!cv) return JSON.stringify({error:'no canvas'});
 var op=parseFloat(getComputedStyle(cv).opacity);
 var bgs=getComputedStyle(document.body).backgroundColor.match(/[\d.]+/g);
 var ctx=cv.getContext('2d');
 var d;
 try{ d=ctx.getImageData(0,0,cv.width,cv.height).data; }
 catch(e){ return JSON.stringify({error:'tainted: '+e.message}); }
 /* Return the canvas's own (colour, alpha) pairs, NOT a composite over one
    background: the same canvas sits over different base layers in different
    places, and a histogram baked against --bg would silently understate an
    element whose base is darker than --bg. Quantised to %d/255 per channel so
    the set stays small; the consumer expands each bucket by +/- half a step. */
 var Q=%d, seen=Object.create(null), n=d.length/4, amax=0;
 for(var i=0;i<n;i++){
  var A=d[i*4+3];
  if(A>amax)amax=A;
  if(A===0)continue;                            /* fully transparent: no effect */
  var k=((d[i*4]/Q|0)<<24)|((d[i*4+1]/Q|0)<<16)|((d[i*4+2]/Q|0)<<8)|(A/Q|0);
  seen[k]=(seen[k]||0)+1;
 }
 var out=[];
 for(var kk in seen){var v=+kk;
  out.push([(v>>>24)&255,(v>>>16)&255,(v>>>8)&255,v&255,seen[kk]]);}
 return JSON.stringify({op:op,bg:[+bgs[0],+bgs[1],+bgs[2]],cw:cv.width,chh:cv.height,
   px:n,maxAlpha:amax,q:Q,pairs:out});})()""" % (Q, Q)


def main():
    theme, vw, vh, draws, tag = (sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
                                 int(sys.argv[4]), sys.argv[5])
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9461")))
    pairs = set()
    meta = None
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.cmd("Emulation.setEmulatedMedia",
              {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        b.metrics(vw, vh)
        for d in range(draws):
            b.goto("%s/index.html?u28x=%d-%d#/privacy" % (cdp.BASE, d, os.getpid()), settle=1.5)
            assert b.ev("document.documentElement.dataset.theme") == theme
            assert b.ev("window.innerWidth") == vw
            r = json.loads(b.ev(READ))
            assert "error" not in r, r
            meta = {"op": r["op"], "bg": r["bg"], "backing": [r["cw"], r["chh"]],
                    "px": r["px"], "q": r["q"]}
            before = len(pairs)
            for p in r["pairs"]:
                pairs.add(tuple(p[:4]))
            print("draw %-3d canvas maxAlpha=%-3d pairs=%-6d new=%-6d union=%d"
                  % (d, r["maxAlpha"], len(r["pairs"]), len(pairs) - before, len(pairs)),
                  flush=True)
    finally:
        b.close()
    res = {"theme": theme, "viewport": [vw, vh], "draws": draws, "meta": meta,
           "pairs": sorted(pairs)}
    json.dump(res, open(os.path.join(OUT, "extremes-%s.json" % tag), "w"))
    print("\n%s %dx%d over %d draws: canvas opacity %.2f on bg %s, backing %s, "
          "%d distinct (colour,alpha) buckets"
          % (theme, vw, vh, draws, meta["op"], meta["bg"], meta["backing"], len(pairs)))
    return res


def composite(base, pair, op, q):
    """Dequantise to the bucket's WORST corner and composite over `base`."""
    a = min(255.0, (pair[3] + 1) * q) / 255.0 * op        # alpha rounded up
    return tuple(base[i] * (1 - a) + min(255.0, (pair[i] + 0.5) * q) * a for i in range(3))


def worst_for(ink, base, model):
    """Lowest contrast `ink` can reach on `base` under any observed canvas pixel."""
    op, q = model["meta"]["op"], model["meta"]["q"]
    w, at = png.ratio(tuple(ink), tuple(base)), tuple(base)   # alpha 0 is reachable
    for p in model["pairs"]:
        c = composite(base, p, op, q)
        r = png.ratio(tuple(ink), c)
        if r < w:
            w, at = r, tuple(round(v) for v in c)
    return w, at


if __name__ == "__main__":
    main()
