"""AC19 / V-F3 — text painted INSIDE a `.hero` over its own cover canvas.

Vermeer's V-F3 isolated the failing layer one variable at a time on
`#/artist/caravaggio`: as shipped 1.42, in-hero cover canvas removed 8.51,
`#bg-canvas` alone removed 1.42 (unchanged). The failing backdrop is therefore
the **in-hero cover canvas at opacity:1**, a different layer from the
site-wide `#bg-canvas` that units 28 and 29 bounded. This instrument measures
that layer directly.

Differences from `durer-u28/canvastext.py`, and why:

1. **Scroll 0 only.** Every `.hero` is the first block of its route, so the
   whole class is in the first viewport. Nothing here needs a scrolled
   capture, so nothing here can be touched by the clip-origin defect V-F2
   (which is fixed in `canvastext.py` at this unit regardless).

2. **Membership is structural, not differential.** "Inside `.hero-content`"
   is a containment test, not a paint test — the question is not *which*
   layer is behind the glyph but whether the glyph clears its floor over
   whatever is actually composited there. Shot C still removes the in-hero
   canvas, but only to keep Vermeer's layer attribution reproducible
   (`coverDelta`), never to decide membership.

3. **The sample is the point.** The cover is generated per subject, so which
   subjects fail is a lottery: Vermeer measured 8 of 10 painters failing in
   light and 4 of 10 in dark, with `claude-monet` clean in light and *worst*
   in dark. A single subject is not a verdict, so every cell runs a subject
   list x `--draws` fresh draws and reports the WORST over all of them.

4. **All four hero families, not just the artist hero.** `hero()` in
   `js/app.js:831` is called from four view builders — artist (:1826),
   movement/technique (:2042), era (:2099) and nation (:2158). They share
   `.hero .hero-shade` and `.hero-content` exactly, so V-F3 is not an
   artist-route defect; it is a `.hero` defect and the sample says so.

`prefers-reduced-motion: reduce` is emulated, so the cover paints one static
frame at t=0 (same rationale as unit 28 — without it the cover drifts between
the three shots and the diff is meaningless). Randomisation is untouched.

usage: python3 herotext.py <theme> <w> <h> <draws> <tag> [route,route,...]
"""
import json, os, sys, time

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp, png

OUT = os.path.dirname(os.path.abspath(__file__))
PID = os.getpid()
A_PNG = "/tmp/u30-a-%d.png" % PID
B_PNG = "/tmp/u30-b-%d.png" % PID
C_PNG = "/tmp/u30-c-%d.png" % PID
THRESH = 60

# 12 painters: Vermeer's three named extremes (caravaggio worst light,
# frida-kahlo worst light-390, claude-monet worst dark / clean light) plus
# leonardo-da-vinci from his run, plus 8 spanning other eras and palettes.
ARTISTS = ["caravaggio", "frida-kahlo", "claude-monet", "leonardo-da-vinci",
           "vincent-van-gogh", "rembrandt", "katsushika-hokusai", "jmw-turner",
           "artemisia-gentileschi", "el-greco", "gustav-klimt", "paul-cezanne"]

# the other three hero families, which share .hero/.hero-content verbatim
OTHER_HEROES = ["#/movement/impressionism", "#/technique/oil-painting",
                "#/era/16th-century", "#/nation/italy"]

# artwork routes: Vermeer listed #/artwork/* hero interiors as NOT TESTED and
# expected them to fail on the same .hero-shade. Both variants are measured:
# one with a real photograph, one with a generative cover.
# 66 of the 323 catalogue works have no photograph and render .aw-hero-gen (a
# generative cover + the .map-hint caption); the rest render a real <img>.
# Both variants are measured, since only the generative one has in-hero text.
ARTWORKS = ["#/artwork/david", "#/artwork/mona-lisa",
            "#/artwork/the-red-studio", "#/artwork/blue-nude-ii",
            "#/artwork/the-old-guitarist", "#/artwork/the-snail"]

ROUTES = ["#/artist/" + a for a in ARTISTS] + OTHER_HEROES + ARTWORKS

# Every visible element with its own text inside a hero container. SCOPE is the
# containment test; it also reports which container matched so the artwork
# routes can be told apart from the .hero routes in the output.
DETECT = r"""(function(){
 var els=[],scopes=[['.hero-content','hero'],['.aw-hero','aw-hero'],
                    ['.mu-hero-body','mu-hero-body']];
 scopes.forEach(function(sc){
  [].forEach.call(document.querySelectorAll(sc[0]),function(root){
   var all=[root].concat([].slice.call(root.querySelectorAll('*')));
   all.forEach(function(el){
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
     path:path.slice(-3).join(' > '),scope:sc[1],
     text:txt.trim().replace(/\s+/g,' ').slice(0,34),
     rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
     fpx:fpx,weight:wt,large:(fpx>=24||(fpx>=18.66&&wt>=700)),inks:inks});});});});
 return JSON.stringify({els:els,y:Math.round(window.scrollY)});})()"""

HIDE = r"""(function(){var n=0;
 [].forEach.call(document.querySelectorAll('*'),function(el){
  var txt='';for(var j=0;j<el.childNodes.length;j++){var cn=el.childNodes[j];
   if(cn.nodeType===3)txt+=cn.nodeValue;}
  if(!txt.trim())return;
  var r=el.getBoundingClientRect();
  if(r.width<2||r.height<2)return;
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

# the IN-HERO cover canvas -- NOT #bg-canvas. This is Vermeer's isolated layer.
KILL = ("(function(){var n=0;"
        "[].forEach.call(document.querySelectorAll("
        "'.hero canvas,.aw-hero canvas,.mu-hero canvas'),function(c){"
        "c.style.setProperty('display','none','important');n++;});return n;})()")

UNKILL = ("(function(){var n=0;"
          "[].forEach.call(document.querySelectorAll("
          "'.hero canvas,.aw-hero canvas,.mu-hero canvas'),function(c){"
          "c.style.removeProperty('display');n++;});return n;})()")

# Restores the SHIPPED pre-unit-30 geometry at runtime, so before and after are
# the same build, the same instrument and the same operator, and only the one
# declaration under test differs. Mirrors unit 28's U28_BEFORE.
BEFORE_CSS = (".hero .hero-shade{background:linear-gradient(180deg,"
              "rgba(var(--bg-rgb),.18) 0%,rgba(var(--bg-rgb),.42) 52%,"
              "rgba(var(--bg-rgb),.93) 100%)!important}"
              ".hero-content{background:none!important}")

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


def detect_stable(b, tries=6):
    prev = None
    for _ in range(tries):
        d = json.loads(b.ev(DETECT))
        key = [(e["sel"], tuple(e["rect"])) for e in d["els"]]
        if prev is not None and key == prev:
            d["stable"] = True
            return d
        prev = key
        b.ev("new Promise(function(r){setTimeout(r,240)})", await_promise=True)
    d["stable"] = False
    return d


def shot(b, path, box, sx=0, sy=0):
    """clip is in PAGE coordinates; box comes from getBoundingClientRect(),
    which is in VIEWPORT coordinates. See canvastext.py::shot — V-F2."""
    import base64
    x, y, w, h = box
    r = b.cmd("Page.captureScreenshot",
              {"format": "png", "captureBeyondViewport": False,
               "clip": {"x": x + sx, "y": y + sy, "width": w, "height": h, "scale": 1}})
    open(path, "wb").write(base64.b64decode(r["data"]))


def measure(b, els, vw, vh):
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
    assert int(b.ev("Math.round(window.scrollY)") or 0) == sy, "page scrolled mid-capture"
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
                for ink in e["inks"]:
                    r_ = png.ratio(tuple(ink), bb)
                    if lo is None or r_ < lo:
                        lo, lopx, nodelta = r_, (tuple(ink), bb), cc
        if lo is None:
            continue
        res.append({"sel": e["sel"], "path": e["path"], "text": e["text"],
                    "scope": e["scope"], "fpx": e["fpx"], "large": e["large"],
                    "need": 3.0 if e["large"] else 4.5,
                    "glyphPx": ng, "worst": round(lo, 2),
                    "ink": list(lopx[0]), "backdrop": list(lopx[1]),
                    "backdropNoCover": list(nodelta),
                    "coverDelta": dmax, "overCover": dmax > 0})
    return res


def run(theme, vw, vh, draws, tag, routes):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9421")))
    rows = []
    before = bool(os.environ.get("U30_BEFORE"))
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.cmd("Emulation.setEmulatedMedia",
              {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        b.metrics(vw, vh)
        for d in range(draws):
            for r in routes:
                b.goto("%s/index.html?u30=%d-%d-%d%s"
                       % (cdp.BASE, d, int(time.time() * 1000) % 999983, os.getpid(), r),
                       settle=1.9)
                assert b.ev("document.documentElement.dataset.theme") == theme
                assert b.ev("window.innerWidth") == vw
                assert b.ev("matchMedia('(prefers-reduced-motion: reduce)').matches") is True
                if before:
                    assert b.ev(
                        "(function(){var s=document.createElement('style');"
                        "s.textContent=%s;document.head.appendChild(s);return true;})()"
                        % json.dumps(BEFORE_CSS)) is True
                wait_settled(b)
                b.ev("window.scrollTo(0,0)")
                b.ev("new Promise(function(r){setTimeout(r,260)})", await_promise=True)
                det = detect_stable(b)
                assert det["y"] == 0, "hero must be measured at scroll 0"
                worst_route, nel = 99.0, 0
                if det["els"]:
                    nel = len(det["els"])
                    for x in measure(b, det["els"], vw, vh):
                        x.update({"route": r, "draw": d, "theme": theme,
                                  "vw": vw, "vh": vh, "scrollY": 0, "before": before})
                        rows.append(x)
                        if x["worst"] < worst_route:
                            worst_route = x["worst"]
                    assert json.loads(b.ev(DETECT))["els"], "restore lost the text"
                print("draw %-2d %-34s els=%-3d worst %.2f"
                      % (d, r, nel, worst_route), flush=True)
    finally:
        b.close()
    json.dump({"theme": theme, "viewport": [vw, vh], "draws": draws,
               "before": before, "rows": rows},
              open(os.path.join(OUT, "hero-%s.json" % tag), "w"))
    summarise(rows)
    return rows


def summarise(rows):
    by = {}
    for r in rows:
        k = (r["scope"], r["sel"])
        if k not in by or r["worst"] < by[k]["worst"]:
            by[k] = r
    print("\nWORST OBSERVED PER ELEMENT CLASS (all draws, all subjects)")
    fails = 0
    for k, r in sorted(by.items(), key=lambda kv: kv[1]["worst"]):
        bad = r["worst"] < r["need"]
        fails += bad
        print("  %-12s %-24s %6.2f need %.1f %-4s  %-32s cover-d=%-3d %s -> %s draw %d"
              % (k[0], k[1], r["worst"], r["need"], "FAIL" if bad else "pass",
                 r["route"], r["coverDelta"], str(r["ink"]), str(r["backdrop"]), r["draw"]))
    print("classes below floor: %d of %d" % (fails, len(by)))
    # per-subject roll-up: which subjects fail at all, the lottery Vermeer named
    subj = {}
    for r in rows:
        s = subj.setdefault(r["route"], {"n": 0, "bad": 0, "worst": 99.0})
        s["n"] += 1
        s["bad"] += 1 if r["worst"] < r["need"] else 0
        s["worst"] = min(s["worst"], r["worst"])
    nbad = sum(1 for v in subj.values() if v["bad"])
    print("subjects with >=1 element below floor: %d of %d" % (nbad, len(subj)))
    for k in sorted(subj, key=lambda k: subj[k]["worst"]):
        v = subj[k]
        print("    %-34s %d/%d below floor, worst %.2f" % (k, v["bad"], v["n"], v["worst"]))


if __name__ == "__main__":
    th, w, h, n, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rt = sys.argv[6].split(",") if len(sys.argv) > 6 else ROUTES
    run(th, w, h, n, tag, rt)
