"""AC19 / F-27-2 — text painted over the generative #bg-canvas, measured on real
rendered glyph pixels, across MULTIPLE random cover draws.

Unit 27 found this class by accident: the F-V1 detector (text whose rect
intersects a Wikimedia <img> rect) flagged `span.count` and `p.img-credit`, and
the A/B with `#bg-canvas` removed proved their real surface was the site-wide
generative canvas, not a photograph. Unit 28 looks for that class DELIBERATELY.

Two lessons from unit 27 are built into the instrument:

1. `getBoundingClientRect()` reports boxes that are CLIPPED AWAY and never
   painted (`.mu-collage` row 2 under `.mu-hero{overflow:hidden}`). A rect test
   therefore proves nothing about what is behind a glyph. So membership in this
   class is decided by a DIFFERENTIAL, not by geometry: an element is over the
   canvas iff its own glyph pixels change when `#bg-canvas` is removed.

2. The canvas is `Math.random`-seeded per page load, so a single draw is not a
   verdict. Every route is loaded `--draws` times behind a unique query string;
   the WORST value over all draws is what is reported.

Three shots per (route, draw, scroll position):
  A  page as rendered
  B  glyphs made transparent (never `visibility:hidden` — that would delete an
     element's own background too; Vermeer's correction, inherited)
  C  glyphs transparent AND `#bg-canvas` display:none !important
A pixel is a glyph pixel where A and B differ strongly. Its backdrop is B (the
canvas as actually composited). It belongs to this class iff B != C there.

`prefers-reduced-motion: reduce` is emulated so the canvas paints ONE static
frame at t=0 and stops. Without it the blobs drift between the three shots and
the diff is meaningless. Randomisation is untouched: every blob/ribbon phase,
radius, amplitude and frequency is still `Math.random`, so t=0 draws span the
same distribution the animation passes through.

usage: python3 canvastext.py <theme> <w> <h> <draws> <tag> [route,route,...]
"""
import json, os, sys, time

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp, png

OUT = os.path.dirname(os.path.abspath(__file__))
PID = os.getpid()
A_PNG = "/tmp/u28-a-%d.png" % PID          # run-unique: no two chains can collide
B_PNG = "/tmp/u28-b-%d.png" % PID
C_PNG = "/tmp/u28-c-%d.png" % PID
THRESH = 60

ROUTES = ["#/", "#/artists", "#/artist/leonardo-da-vinci", "#/artwork/david",
          "#/explore", "#/timeline", "#/influences", "#/museums",
          "#/museum/louvre", "#/museum/tate-britain", "#/lists", "#/palette",
          "#/taste", "#/daily", "#/privacy", "#/credits", "#/no-such-page"]

# every visible element with its OWN text, inside the viewport. No image gate.
DETECT = r"""(function(){
 var els=[];
 [].forEach.call(document.querySelectorAll('*'),function(el){
  var txt='';for(var j=0;j<el.childNodes.length;j++){var cn=el.childNodes[j];
   if(cn.nodeType===3)txt+=cn.nodeValue;}
  if(!txt.trim())return;
  var cs=getComputedStyle(el);
  if(cs.display==='none'||cs.visibility==='hidden')return;
  if(parseFloat(cs.opacity)<0.99)return;
  var r=el.getBoundingClientRect();
  if(r.width<2||r.height<2)return;
  if(r.top<0||r.bottom>window.innerHeight||r.left<0||r.right>window.innerWidth)return;
  var fpx=parseFloat(cs.fontSize),wt=parseInt(cs.fontWeight,10)||400;
  var inks=[],clip=cs.webkitBackgroundClip||cs.backgroundClip||'';
  if(clip==='text'){var m=cs.backgroundImage.match(/rgba?\([^)]+\)/g)||[];
   inks=m.map(function(s){var p=s.match(/[\d.]+/g);return [+p[0],+p[1],+p[2]];});}
  if(!inks.length){var p=cs.color.match(/[\d.]+/g);inks=[[+p[0],+p[1],+p[2]]];}
  var path=[],n=el;
  while(n&&n!==document.body){path.unshift(n.tagName.toLowerCase()+
    (n.classList.length?'.'+[].slice.call(n.classList).join('.'):''));n=n.parentElement;}
  els.push({sel:el.tagName.toLowerCase()+(el.classList.length?'.'+[].slice.call(el.classList).join('.'):''),
   path:path.slice(-3).join(' > '),
   text:txt.trim().replace(/\s+/g,' ').slice(0,34),
   rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
   fpx:fpx,weight:wt,large:(fpx>=24||(fpx>=18.66&&wt>=700)),inks:inks});});
 return JSON.stringify({els:els,h:document.body.scrollHeight,y:Math.round(window.scrollY)});})()"""

HIDE = r"""(function(){var n=0;
 [].forEach.call(document.querySelectorAll('*'),function(el){
  var txt='';for(var j=0;j<el.childNodes.length;j++){var cn=el.childNodes[j];
   if(cn.nodeType===3)txt+=cn.nodeValue;}
  if(!txt.trim())return;
  var r=el.getBoundingClientRect();
  if(r.width<2||r.height<2)return;
  /* An element with -webkit-background-clip:text paints its ink as a BACKGROUND
     seen through the glyphs, so transparent text alone does not remove it: shot B
     then still shows the gradient and the element scores against itself (1.00).
     For those, and only those, the background-image IS the ink, so it goes too. */
  var cs2=getComputedStyle(el);
  if((cs2.webkitBackgroundClip||cs2.backgroundClip||'')==='text')
    el.style.setProperty('background-image','none','important');
  el.style.setProperty('color','transparent','important');
  el.style.setProperty('-webkit-text-fill-color','transparent','important');
  el.style.setProperty('text-shadow','none','important');
  el.style.setProperty('text-decoration-color','transparent','important');
  n++;});
 return n;})()"""

UNHIDE = r"""(function(){var n=0;
 [].forEach.call(document.querySelectorAll('[style]'),function(el){
  if(!el.style.getPropertyValue('-webkit-text-fill-color'))return;
  el.style.removeProperty('color');
  el.style.removeProperty('-webkit-text-fill-color');
  el.style.removeProperty('text-shadow');
  el.style.removeProperty('text-decoration-color');
  el.style.removeProperty('background-image');
  n++;});
 return n;})()"""

KILL = ("(function(){var c=document.getElementById('bg-canvas');"
        "if(c)c.style.setProperty('display','none','important');return !!c;})()")

UNKILL = ("(function(){var c=document.getElementById('bg-canvas');"
          "if(c)c.style.removeProperty('display');"
          "return c?getComputedStyle(c).display:null;})()")

SETTLE = """(function(){var im=[].slice.call(document.images);
 return JSON.stringify({pending:im.filter(function(i){return !i.complete;}).length,
  h:document.body.scrollHeight});})()"""


def wait_settled(b, tries=30):
    last = None
    for _ in range(tries):
        st = json.loads(b.ev(SETTLE))
        if st["pending"] == 0 and last == st["h"]:
            return st
        last = st["h"]
        b.ev("new Promise(function(r){setTimeout(r,200)})", await_promise=True)
    return json.loads(b.ev(SETTLE))


def keep(e):
    """Optional ink filter. Measuring every text element on a page costs a
    per-pixel Python loop over every rect, which makes a many-draw sweep
    unaffordable; the at-risk set here is defined by INK, not by selector, so
    U28_INKS='139,131,114;155,147,127' measures exactly the --faint/--muted
    glyphs and skips the rest. Unset = measure everything."""
    want = os.environ.get("U28_INKS", "").strip()
    if not want:
        return True
    sets = {tuple(int(v) for v in s.split(",")) for s in want.split(";") if s}
    return any(tuple(i) in sets for i in e["inks"])


def detect_stable(b, tries=6):
    prev = None
    for _ in range(tries):
        d = json.loads(b.ev(DETECT))
        d["els"] = [e for e in d["els"] if keep(e)]
        key = [(e["sel"], tuple(e["rect"])) for e in d["els"]]
        if prev is not None and key == prev:
            d["stable"] = True
            return d
        prev = key
        b.ev("new Promise(function(r){setTimeout(r,240)})", await_promise=True)
    d["stable"] = False
    return d


def shot(b, path, box, sx=0, sy=0):
    """CLIP ORIGIN — corrected at unit 30 (Vermeer's V-F2).

    `Page.captureScreenshot`'s `clip` is in PAGE (document) coordinates, but
    `box` is assembled from `getBoundingClientRect()`, which is in VIEWPORT
    coordinates. The two agree only at scrollY == 0; at any other scroll
    position the captured pixels were offset by exactly scrollY, so glyphs were
    compared against whatever sat that far up the document. Every row this
    harness produced at scrollY > 0 before unit 30 is invalid for that reason
    (89 rows of the unit-29 pixel run). The scroll offset is added HERE, at the
    capture, so all the per-element pixel arithmetic in measure() stays in the
    viewport space the rects were measured in.
    """
    import base64
    x, y, w, h = box
    r = b.cmd("Page.captureScreenshot",
              {"format": "png", "captureBeyondViewport": False,
               "clip": {"x": x + sx, "y": y + sy, "width": w, "height": h, "scale": 1}})
    open(path, "wb").write(base64.b64decode(r["data"]))


def measure(b, els, vw, vh):
    """Three-shot glyph diff. Returns rows; `overCanvas` is a PAINT test."""
    # read the scroll offset once, here, and use it for all three shots: the
    # page must not move between A, B and C or the diff is meaningless.
    sx = int(b.ev("Math.round(window.scrollX)") or 0)
    sy = int(b.ev("Math.round(window.scrollY)") or 0)
    xs0 = max(0, min(e["rect"][0] for e in els))
    ys0 = max(0, min(e["rect"][1] for e in els))
    xs1 = min(vw, max(e["rect"][0] + e["rect"][2] for e in els))
    ys1 = min(vh, max(e["rect"][1] + e["rect"][3] for e in els))
    box = (xs0, ys0, max(1, xs1 - xs0), max(1, ys1 - ys0))
    shot(b, A_PNG, box, sx, sy)
    b.ev(HIDE)
    b.ev("new Promise(function(r){setTimeout(r,200)})", await_promise=True)
    shot(b, B_PNG, box, sx, sy)
    b.ev(KILL)
    b.ev("new Promise(function(r){setTimeout(r,200)})", await_promise=True)
    shot(b, C_PNG, box, sx, sy)
    # the three shots must be the same pixels of the same document
    assert int(b.ev("Math.round(window.scrollY)") or 0) == sy, "page scrolled mid-capture"
    # Both mutations are inline-style only and are undone here, so ONE page load
    # -- i.e. one canvas draw -- serves every scroll band of that route. Reloading
    # between bands would have re-seeded the canvas mid-route and made "a draw"
    # meaningless. The caller re-detects afterwards and asserts the inks came back.
    b.ev(UNKILL)
    b.ev(UNHIDE)
    b.ev("new Promise(function(r){setTimeout(r,160)})", await_promise=True)
    A, B, Cc = png.Img(A_PNG), png.Img(B_PNG), png.Img(C_PNG)
    res = []
    for e in els:
        x, y, w, h = e["rect"]
        x0, y0 = max(0, max(0, x) - box[0]), max(0, max(0, y) - box[1])
        x1 = min(A.w, B.w, Cc.w, min(vw, x + w) - box[0])
        y1 = min(A.h, B.h, Cc.h, min(vh, y + h) - box[1])
        lo, lopx, ng, dmax, nodelta = None, None, 0, 0, None
        bmin = bmax = None                       # canvas-free BASE under the glyphs
        for py in range(y0, y1):
            for px_ in range(x0, x1):
                a, bb = A.px(px_, py), B.px(px_, py)
                if abs(a[0]-bb[0]) + abs(a[1]-bb[1]) + abs(a[2]-bb[2]) < THRESH:
                    continue
                ng += 1
                cc = Cc.px(px_, py)
                d = max(abs(bb[0]-cc[0]), abs(bb[1]-cc[1]), abs(bb[2]-cc[2]))
                if d > dmax:
                    dmax = d
                # The base is what is under the glyph with the canvas GONE. It is
                # deterministic (no Math.random in it), so one draw fixes it — and
                # it is what the canvas model must be composited over. Keep both
                # luminance extremes: the blend is monotone in the base, so these
                # two bracket every base pixel this element actually sits on.
                lc = png.lum(cc)
                if bmin is None or lc < bmin[0]:
                    bmin = (lc, cc)
                if bmax is None or lc > bmax[0]:
                    bmax = (lc, cc)
                for ink in e["inks"]:
                    r_ = png.ratio(tuple(ink), bb)
                    if lo is None or r_ < lo:
                        lo, lopx, nodelta = r_, (tuple(ink), bb), cc
        if lo is None:
            continue
        res.append({"sel": e["sel"], "path": e["path"], "text": e["text"],
                    "fpx": e["fpx"], "large": e["large"],
                    "need": 3.0 if e["large"] else 4.5,
                    "glyphPx": ng, "worst": round(lo, 2),
                    "ink": list(lopx[0]), "backdrop": list(lopx[1]),
                    "backdropNoCanvas": list(nodelta),
                    "baseDarkest": list(bmin[1]), "baseBrightest": list(bmax[1]),
                    "canvasDelta": dmax, "overCanvas": dmax > 0})
    return res


def run(theme, vw, vh, draws, tag, routes):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9421")))
    rows = []
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.cmd("Emulation.setEmulatedMedia",
              {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        b.metrics(vw, vh)
        for d in range(draws):
            for r in routes:
                b.goto("%s/index.html?u28=%d-%d-%d%s"
                       % (cdp.BASE, d, int(time.time() * 1000) % 999983, os.getpid(), r),
                       settle=1.9)
                assert b.ev("document.documentElement.dataset.theme") == theme
                assert b.ev("window.innerWidth") == vw
                assert b.ev("matchMedia('(prefers-reduced-motion: reduce)').matches") is True
                if os.environ.get("U28_BEFORE"):
                    # restore the SHIPPED rule at runtime, so before and after are
                    # the same build, the same instrument and the same operator —
                    # only the one declaration under test differs
                    assert b.ev(
                        "(function(){var s=document.createElement('style');"
                        "s.textContent='.sec-title .count{color:var(--faint)!important}"
                        ".img-credit,.img-credit a{color:var(--muted)!important}';"
                        "document.head.appendChild(s);"
                        "return true;})()") is True
                wait_settled(b)
                worst_route, nb, nel, noc = 99.0, 0, 0, 0
                y, step = 0, int(vh * 0.85)
                maxb = int(os.environ.get("U28_MAXBANDS", "12"))
                seen, dry = set(), 0
                while nb < maxb:
                    b.ev("window.scrollTo(0,%d)" % y)
                    b.ev("new Promise(function(r){setTimeout(r,280)})", await_promise=True)
                    at = b.ev("Math.round(window.scrollY)")
                    det = detect_stable(b)
                    nb += 1
                    if det["els"]:
                        nel += len(det["els"])
                        for x in measure(b, det["els"], vw, vh):
                            x.update({"route": r, "draw": d, "theme": theme,
                                      "vw": vw, "vh": vh, "scrollY": at})
                            rows.append(x)
                            if x["overCanvas"]:
                                noc += 1
                                if x["worst"] < worst_route:
                                    worst_route = x["worst"]
                        # the mutations restore, so the ink of the next band's
                        # detection must equal what was there before the shots
                        assert json.loads(b.ev(DETECT))["els"], "restore lost the text"
                    # A long index page repeats one card grid for thousands of
                    # pixels; once three consecutive bands add no NEW (sel,path)
                    # the route has nothing further to say about class coverage.
                    fresh = {(e["sel"], e["path"]) for e in det["els"]} - seen
                    seen |= fresh
                    dry = 0 if fresh else dry + 1
                    if dry >= 3:
                        break
                    # scrollHeight can grow as lazy images land, so re-read it here
                    page_h = json.loads(b.ev(SETTLE))["h"]
                    ymax = max(0, page_h - vh)
                    if at >= ymax - 2 or y > ymax:
                        break
                    y = min(ymax, y + step)
                print("draw %-2d %-30s bands=%-3d els=%-4d overCanvas=%-4d worst %.2f"
                      % (d, r, nb, nel, noc, worst_route), flush=True)
    finally:
        b.close()
    json.dump({"theme": theme, "viewport": [vw, vh], "draws": draws, "rows": rows},
              open(os.path.join(OUT, "canvas-%s.json" % tag), "w"))
    summarise(rows)
    return rows


def summarise(rows):
    by = {}
    for r in rows:
        if not r["overCanvas"]:
            continue
        k = r["sel"]
        if k not in by or r["worst"] < by[k]["worst"]:
            by[k] = r
    print("\nWORST OBSERVED OVER #bg-canvas, PER ELEMENT CLASS (all draws)")
    fails = 0
    for k, r in sorted(by.items(), key=lambda kv: kv[1]["worst"]):
        bad = r["worst"] < r["need"]
        fails += bad
        print("  %-34s %6.2f need %.1f %-4s  %-26s d=%-3d %s -> %s (no-canvas %s) draw %d"
              % (k, r["worst"], r["need"], "FAIL" if bad else "pass", r["route"],
                 r["canvasDelta"], str(r["ink"]), str(r["backdrop"]),
                 str(r["backdropNoCanvas"]), r["draw"]))
    print("classes below floor: %d of %d" % (fails, len(by)))


if __name__ == "__main__":
    th, w, h, n, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rt = sys.argv[6].split(",") if len(sys.argv) > 6 else ROUTES
    run(th, w, h, n, tag, rt)
