"""AC19 — ENUMERATION of every generative COVER canvas that has text over it.

Why this exists. Four instances of one defect — a scrim that ramps by container
height under a bottom-anchored text block — were found by four separate
accidents: the home hero (unit 26a), the museum band (unit 27), the `.hero`
family (unit 30a) and `.era-tile` (unit 30, found while writing the log). Four
finds by four accidents is a sampling process and it will keep producing a
fifth. This instrument replaces the sampling with an enumeration, the way unit
24's 694-image census replaced a 122-record sample and unit 29's source bound
replaced an 84-draw model.

The enumeration is NOT a list of selectors I thought of. It is a PAINT
DIFFERENTIAL over every cover canvas in the document:

  A  page as rendered
  B  glyphs made transparent            -> the real composited backdrop
  C  glyphs transparent AND every COVER canvas display:none

A pixel is a glyph pixel where A and B differ strongly. The glyph composites
over a cover canvas iff B != C there. So membership is decided by what actually
paints, not by my reading of the CSS — an element I never thought to name still
turns up if its glyphs sit on a cover, and an element whose canvas is hidden
behind an opaque panel correctly does not.

"COVER canvas" means every <canvas> EXCEPT #bg-canvas. #bg-canvas is the
site-wide background, bounded at its source in unit 29 and re-verified with the
corrected instrument at unit 30; it is excluded here so this run measures the
per-subject covers that canvasTag() emits and nothing else. There are 20
canvasTag call sites in js/app.js; each element found here is reported with its
nearest canvas-bearing ancestor so the row maps back to a call site.

The clip-origin defect V-F2 is fixed here as it is in canvastext.py: capture
clips are in PAGE coordinates and getBoundingClientRect() is in VIEWPORT
coordinates. That fix is what makes the scrolled bands — where most of these
covers live — measurable at all.

usage: python3 covertext.py <theme> <w> <h> <draws> <tag> [route,route,...]
"""
import json, os, sys, time

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp, png

OUT = os.path.dirname(os.path.abspath(__file__))
PID = os.getpid()
A_PNG = "/tmp/u30c-a-%d.png" % PID
B_PNG = "/tmp/u30c-b-%d.png" % PID
C_PNG = "/tmp/u30c-c-%d.png" % PID
THRESH = 60

# Every route that renders a canvasTag surface, plus the index pages that repeat
# the card grids. `#/` carries the home hero, the era strip, the daily card and
# the mini-card rails, so it exercises several call sites at once.
ROUTES = ["#/", "#/artists", "#/artist/caravaggio", "#/artist/leonardo-da-vinci",
          "#/artwork/the-red-studio", "#/artwork/david",
          "#/movements", "#/movement/impressionism", "#/techniques",
          "#/technique/oil-painting", "#/eras", "#/era/16th-century",
          "#/nations", "#/nation/italy", "#/museums", "#/museum/louvre",
          "#/lists", "#/list/paintings-that-still-scare-us", "#/explore", "#/timeline",
          "#/influences", "#/palette", "#/taste", "#/daily"]

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
  /* nearest ancestor that CONTAINS a cover canvas -- this is what maps the row
     back to one of the 20 canvasTag call sites. */
  var host='',h=el;
  while(h&&h!==document.body){
   var cv=h.querySelector?h.querySelector('canvas:not(#bg-canvas)'):null;
   if(cv){host=h.tagName.toLowerCase()+(h.classList.length?'.'+[].slice.call(h.classList).join('.'):'');break;}
   h=h.parentElement;}
  els.push({sel:el.tagName.toLowerCase()+(el.classList.length?'.'+[].slice.call(el.classList).join('.'):''),
   path:path.slice(-3).join(' > '),host:host,
   text:txt.trim().replace(/\s+/g,' ').slice(0,30),
   rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
   fpx:fpx,weight:wt,large:(fpx>=24||(fpx>=18.66&&wt>=700)),inks:inks});});
 return JSON.stringify({els:els,y:Math.round(window.scrollY),h:document.body.scrollHeight});})()"""

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

# every COVER canvas -- i.e. every canvasTag() output. #bg-canvas is excluded on
# purpose: it is a different layer, bounded at its source in unit 29.
#
# visibility:hidden, NOT display:none. Several canvasTag call sites emit an
# IN-FLOW canvas (.mini-card, .arc-work-gen, .le-art), so display:none reflows
# the document, changes scrollHeight and moves scrollY between shots B and C --
# which the mid-capture scroll assertion below caught on the first run. Hiding
# by visibility removes the canvas's PAINT while keeping its box, so the layout
# under the glyphs is identical in all three shots. (This is the opposite of
# unit 28's rule for TEXT elements, where visibility:hidden would wrongly delete
# an element's own background too; a canvas has no such background to lose.)
KILL = ("(function(){var n=0;[].forEach.call("
        "document.querySelectorAll('canvas:not(#bg-canvas)'),function(c){"
        "c.style.setProperty('visibility','hidden','important');n++;});return n;})()")
UNKILL = ("(function(){var n=0;[].forEach.call("
          "document.querySelectorAll('canvas:not(#bg-canvas)'),function(c){"
          "c.style.removeProperty('visibility');n++;});return n;})()")

# restores the pre-unit-30 geometry of all three veiled cover surfaces, so
# before/after are the same build, instrument and operator.
BEFORE_CSS = (".hero .hero-shade{background:linear-gradient(180deg,"
              "rgba(var(--bg-rgb),.18) 0%,rgba(var(--bg-rgb),.42) 52%,"
              "rgba(var(--bg-rgb),.93) 100%)!important}"
              ".hero-content{background:none!important}"
              ".era-tile .et-shade{background:linear-gradient(180deg,transparent 30%,"
              "rgba(var(--bg-rgb),.88))!important}"
              ".era-tile .et-label{background:none!important}")

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
    """clip is in PAGE coordinates, box is in VIEWPORT coordinates (V-F2)."""
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
    b.ev("window.scrollTo(%d,%d)" % (sx, sy))
    b.ev("new Promise(function(r){setTimeout(r,200)})", await_promise=True)
    shot(b, C_PNG, box, sx, sy)
    # the three shots must be the same pixels of the same document
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
        res.append({"sel": e["sel"], "path": e["path"], "host": e["host"],
                    "text": e["text"], "fpx": e["fpx"], "large": e["large"],
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
                b.goto("%s/index.html?u30c=%d-%d-%d%s"
                       % (cdp.BASE, d, int(time.time() * 1000) % 999983, os.getpid(), r),
                       settle=1.9)
                assert b.ev("document.documentElement.dataset.theme") == theme
                if before:
                    b.ev("(function(){var s=document.createElement('style');"
                         "s.textContent=%s;document.head.appendChild(s);return true;})()"
                         % json.dumps(BEFORE_CSS))
                wait_settled(b)
                worst_route, nb, noc = 99.0, 0, 0
                y, step = 0, int(vh * 0.85)
                maxb = int(os.environ.get("U30_MAXBANDS", "10"))
                seen, dry = set(), 0
                while nb < maxb:
                    b.ev("window.scrollTo(0,%d)" % y)
                    b.ev("new Promise(function(r){setTimeout(r,300)})", await_promise=True)
                    det = detect_stable(b)
                    nb += 1
                    if det["els"]:
                        for x in measure(b, det["els"], vw, vh):
                            x.update({"route": r, "draw": d, "theme": theme,
                                      "vw": vw, "vh": vh, "scrollY": det["y"],
                                      "before": before})
                            rows.append(x)
                            if x["overCover"]:
                                noc += 1
                                if x["worst"] < worst_route:
                                    worst_route = x["worst"]
                        assert json.loads(b.ev(DETECT))["els"], "restore lost the text"
                    fresh = {(e["sel"], e["host"]) for e in det["els"]} - seen
                    seen |= fresh
                    dry = 0 if fresh else dry + 1
                    if dry >= 3:
                        break
                    page_h = json.loads(b.ev(SETTLE))["h"]
                    ymax = max(0, page_h - vh)
                    if det["y"] >= ymax - 2 or y > ymax:
                        break
                    y = min(ymax, y + step)
                print("draw %-2d %-28s bands=%-2d overCover=%-4d worst %.2f"
                      % (d, r, nb, noc, worst_route), flush=True)
    finally:
        b.close()
    json.dump({"theme": theme, "viewport": [vw, vh], "draws": draws,
               "before": before, "rows": rows},
              open(os.path.join(OUT, "cover-%s.json" % tag), "w"))
    summarise(rows)
    return rows


def summarise(rows):
    """Grouped by HOST -- i.e. by canvasTag call site, not by ink class."""
    by = {}
    for r in rows:
        if not r["overCover"]:
            continue
        k = (r["host"], r["sel"])
        if k not in by or r["worst"] < by[k]["worst"]:
            by[k] = r
    print("\nTEXT COMPOSITING OVER A COVER CANVAS, WORST PER (host, class)")
    fails = 0
    for k, r in sorted(by.items(), key=lambda kv: kv[1]["worst"]):
        bad = r["worst"] < r["need"]
        fails += bad
        print("  %-26s %-20s %6.2f need %.1f %-4s  %-26s d=%-3d %s"
              % (k[0][:26], k[1][:20], r["worst"], r["need"],
                 "FAIL" if bad else "pass", r["route"], r["coverDelta"], str(r["ink"])))
    print("(host,class) pairs below floor: %d of %d" % (fails, len(by)))
    hosts = {}
    for r in rows:
        if not r["overCover"]:
            continue
        h = hosts.setdefault(r["host"], {"n": 0, "bad": 0, "worst": 99.0})
        h["n"] += 1
        h["bad"] += 1 if r["worst"] < r["need"] else 0
        h["worst"] = min(h["worst"], r["worst"])
    print("\nPER HOST (canvasTag call site)")
    for k in sorted(hosts, key=lambda k: hosts[k]["worst"]):
        v = hosts[k]
        print("  %-30s n=%-5d below=%-4d worst %.2f %s"
              % (k[:30], v["n"], v["bad"], v["worst"], "FAIL" if v["bad"] else "pass"))


if __name__ == "__main__":
    th, w, h, n, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rt = sys.argv[6].split(",") if len(sys.argv) > 6 else ROUTES
    run(th, w, h, n, tag, rt)
