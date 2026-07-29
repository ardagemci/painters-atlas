"""AC19 / F-8 / A13 — the (ink, size, backdrop) TRIPLE census over the full route
table. Vermeer, unit 32. Independent of the implementer of every fix it checks.

WHY THIS INSTRUMENT EXISTS
Van Eyck's A13: AC19's unit is the (ink, size, backdrop) triple, not the host.
Unit 29 scored every ink but over 19 routes containing none of the four hero()
families; unit 30 walked those families but excluded #bg-canvas by design.
`span.tl-year` fell in the seam. So this walks the ROUTE TABLE — every `case` in
`route()` (js/app.js:2359-2384) — and on every route scores every ink site it can
see against its MEASURED backdrop.

METHOD — four shots per (route, draw, scroll band):
  A  page as rendered
  B  every glyph's ink forced transparent (never visibility:hidden — that would
     delete an element's own background; Vermeer's own correction, inherited)
  C  B, plus #bg-canvas display:none            -> canvasDelta
  D  B, plus every canvasTag() cover visibility:hidden -> coverDelta
A pixel is a glyph pixel where A and B differ strongly. Its BACKDROP is B — the
surface as actually composited, measured, never read from the stylesheet. That
method distinction is the whole lesson of F-8. canvasDelta>0 means #bg-canvas is
part of that backdrop; coverDelta>0 means a canvasTag cover is; both 0 means the
glyph sits on deterministic opaque paint.

INHERITED CORRECTIONS, both load-bearing:
  * unit 30 / V-F2 — Page.captureScreenshot's `clip` is in PAGE coordinates while
    getBoundingClientRect is in VIEWPORT coordinates; scrollY is added at the
    capture, so all per-pixel arithmetic stays in viewport space.
  * unit 30 — covers are hidden with visibility:hidden, never display:none:
    several canvasTag sites emit an IN-FLOW canvas and display:none reflows the
    document between shots. #bg-canvas is position:fixed so display:none there
    moves nothing, and unit 28's rule still holds for it.

WHAT THIS SWEEP ADDS OVER UNIT 28's
  * SVG <text>/<tspan> inks are read from `fill`, not `color`, and hidden with an
    injected `fill:transparent` rule, so they are scored instead of silently
    dropping out (Van Eyck A16 named this class unverifiable).
  * the D shot, so a cover backdrop is distinguished from the site canvas.
  * the full route table, both themes, both viewports.

WHAT IT STILL CANNOT SEE — and is NOT cleared by it:
  * ::before/::after and ::placeholder pseudo-element ink. They own no text node
    and no rect of their own, so a page walk cannot isolate their glyph pixels
    from their host's. They are measured by SELECTOR in sitecensus.py instead.
  * anything not painted at the sampled scroll bands / draws.

usage: python3 triple.py <theme> <w> <h> <draws> <tag> [route,route,...]
"""
import base64, json, os, sys, time

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp                                    # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pngfast as png                         # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
PID = os.getpid()
SHOT = {k: "/tmp/v32-%s-%d.png" % (k, PID) for k in "ABCD"}
THRESH = 60

# ---------------------------------------------------------------- route table
# Every `case` in route() (js/app.js). Parameterised routes carry a real id; the
# ones marked * are the four hero() families unit 29 never loaded.
ROUTES = [
    "#/",                       # viewHome
    "#/artists",                # viewArtists
    "#/artist/leonardo-da-vinci",
    "#/artwork/david",
    "#/explore",
    "#/timeline",
    "#/influences",
    "#/daily",
    "#/lists",
    "#/list/paintings-that-still-scare-us",
    "#/palette",
    "#/taste",
    "#/museums",
    "#/museum/louvre",
    "#/movements",
    "#/movement/impressionism",         # *
    "#/techniques",
    "#/technique/oil-painting",         # *
    "#/eras",
    "#/era/16th-century",               # *
    "#/nations",
    "#/nation/italy",                   # *
    "#/privacy",
    "#/credits",
    "#/passport/import",
    "#/no-such-page",                   # view404
]

# every #/era/* route: F-8 lived on this family and the family has 8 members.
ERA_ROUTES = ["#/era/%s" % e for e in
              ["14th-century", "15th-century", "16th-century", "17th-century",
               "18th-century", "19th-century", "20th-century", "21st-century"]]

# ------------------------------------------------------------------ detection
# Every visible element with its OWN text, plus SVG <text>/<tspan>, inside the
# viewport. No image gate, no ink filter: the point is a census.
DETECT = r"""(function(){
 var els=[];
 function rgb(s){var m=s&&s.match(/[\d.]+/g);
   return m&&m.length>=3?[Math.round(+m[0]),Math.round(+m[1]),Math.round(+m[2])]:null;}
 /* ---- OVERLAYS: the occlusion guard, and it decides what a low number MEANS.
    `.site-header` is position:sticky, z-index:50, background rgba(--bg-rgb,.78)
    with a 14px backdrop-blur. Page content scrolling underneath it composites
    through a translucent bar, so a glyph caught there measures against a
    backdrop that is partly the header. That is ordinary scrolling, not an AC19
    presentation defect. Measuring it as a failure manufactures findings;
    measuring it silently puts a false number in the table. So it is measured
    SEPARATELY: the AC19 verdict comes from the unoccluded pixels, and the
    occluded pixels are reported as their own class with the occluder named.
    An overlay counts against an element only when it is NOT that element's own
    ancestor — which keeps `.search-results` (position:absolute INSIDE the sticky
    header) measurable while still catching `.main-nav` painting over it. That
    distinction is the whole of the N-31-2 question. */
 var ovEls=[].filter.call(document.querySelectorAll('*'),function(el){
  var cs=getComputedStyle(el);
  if(cs.position!=='fixed'&&cs.position!=='sticky')return false;
  if(cs.display==='none'||cs.visibility==='hidden')return false;
  if(parseFloat(cs.opacity)<0.01)return false;
  var bg=cs.backgroundColor||'',m=bg.match(/rgba?\(([^)]+)\)/);
  var parts=m?m[1].split(','):[];
  var alpha=parts.length>3?parseFloat(parts[3]):(m?1:0);
  var bf=(cs.backdropFilter||cs.webkitBackdropFilter||'none');
  if(!(alpha>0.01||bf!=='none'))return false;
  var r=el.getBoundingClientRect();
  return r.width>=2&&r.height>=2;});
 var overlays=ovEls.map(function(el){var r=el.getBoundingClientRect();
  return {sel:el.tagName.toLowerCase()+
    (el.classList&&el.classList.length?'.'+[].slice.call(el.classList).join('.'):''),
   rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]};});
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
  var svg=(el.namespaceURI==='http://www.w3.org/2000/svg');
  var tag=el.tagName.toLowerCase();
  var isSvgText=svg&&(tag==='text'||tag==='tspan');
  if(svg&&!isSvgText)return;
  var fpx=parseFloat(cs.fontSize),wt=parseInt(cs.fontWeight,10)||400;
  var inks=[],clip=cs.webkitBackgroundClip||cs.backgroundClip||'';
  if(clip==='text'){var m=cs.backgroundImage.match(/rgba?\([^)]+\)/g)||[];
   inks=m.map(rgb).filter(Boolean);}
  if(!inks.length){
   var v=(isSvgText&&cs.fill&&cs.fill!=='none')?rgb(cs.fill):rgb(cs.color);
   if(!v)return; inks=[v];}
  var path=[],n=el;
  while(n&&n!==document.body){path.unshift(n.tagName.toLowerCase()+
    (n.classList&&n.classList.length?'.'+[].slice.call(n.classList).join('.'):''));
   n=n.parentElement;}
  var ov=[];
  ovEls.forEach(function(o,oi){ if(!o.contains(el)) ov.push(oi); });
  els.push({sel:tag+(el.classList&&el.classList.length?'.'+[].slice.call(el.classList).join('.'):''),
   kind:isSvgText?'svgtext':'text',
   path:path.slice(-3).join(' > '),
   text:txt.trim().replace(/\s+/g,' ').slice(0,34),
   rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
   fpx:fpx,weight:wt,large:(fpx>=24||(fpx>=18.66&&wt>=700)),inks:inks,ov:ov});});
 return JSON.stringify({els:els,overlays:overlays,
   h:document.body.scrollHeight,y:Math.round(window.scrollY)});})()"""

# HIDE: inline for HTML text (unit 28's, including the -webkit-background-clip
# case), plus ONE injected rule for SVG <text>/<tspan>, whose ink is `fill:` and
# is therefore untouched by `color`. Without that rule shot B still shows the SVG
# glyphs, A==B there, no glyph pixels are found, and the element drops silently
# out of the table — exactly the blind spot Van Eyck (A16) said he could not
# close.
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
 var s=document.createElement('style');s.id='v32-hide';
 s.textContent='text,tspan{fill:transparent!important;'+
   '-webkit-text-fill-color:transparent!important;stroke:none!important}';
 document.head.appendChild(s);
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
 var s=document.getElementById('v32-hide');if(s)s.parentNode.removeChild(s);
 return n;})()"""

KILL_CANVAS = ("(function(){var c=document.getElementById('bg-canvas');"
               "if(c)c.style.setProperty('display','none','important');return !!c;})()")
UNKILL_CANVAS = ("(function(){var c=document.getElementById('bg-canvas');"
                 "if(c)c.style.removeProperty('display');return true;})()")
KILL_COVERS = ("(function(){var n=0;[].forEach.call("
               "document.querySelectorAll('canvas:not(#bg-canvas)'),function(c){"
               "c.style.setProperty('visibility','hidden','important');n++;});return n;})()")
UNKILL_COVERS = ("(function(){[].forEach.call("
                 "document.querySelectorAll('canvas:not(#bg-canvas)'),function(c){"
                 "c.style.removeProperty('visibility');});return true;})()")

SETTLE = """(function(){var im=[].slice.call(document.images);
 return JSON.stringify({pending:im.filter(function(i){return !i.complete;}).length,
  h:document.body.scrollHeight});})()"""

SEED_PASSPORT = json.dumps({
    "version": 1, "createdAt": "2026-07-29T00:00:00.000Z",
    "updatedAt": "2026-07-29T00:00:00.000Z",
    "admirations": [{"id": i, "at": "2026-07-29T00:00:00.000Z"} for i in
                    ["david", "the-night-watch", "the-starry-night",
                     "impression-sunrise", "the-kiss", "guernica"]],
    "notForMe": [], "seen": [], "wantToSee": [], "saved": [], "probes": [],
    "quiz": None, "palette": None,
    "persona": {"adopted": None, "candidates": [], "adoptedAt": None, "hidden": False},
    "tasteVector": None, "milestones": {"onboarded": True, "confidence": "sketch"},
})


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
    """Optional ink filter for the SECOND, many-draw pass.

    Pass 1 is unfiltered — it is the census, and it is what enumerates the triple
    set. But `#bg-canvas` is Math.random-seeded, so a triple whose measured
    backdrop is the canvas has been sampled, not bounded, and one draw is not a
    verdict (unit 28's lesson; and F-8 was partly missed because one cell of eight
    passed by chance). Pass 2 re-runs the same instrument at many draws over only
    the inks pass 1 actually observed on the canvas, which is what makes the
    draw-count affordable. V32_INKS='67,60,49;43,38,32'. Unset = measure all.
    """
    want = os.environ.get("V32_INKS", "").strip()
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


def shot(b, path, box, sx, sy):
    """Clip is in PAGE coordinates; box is in VIEWPORT coordinates — unit 30."""
    x, y, w, h = box
    r = b.cmd("Page.captureScreenshot",
              {"format": "png", "captureBeyondViewport": False,
               "clip": {"x": x + sx, "y": y + sy, "width": w, "height": h, "scale": 1}})
    open(path, "wb").write(base64.b64decode(r["data"]))


def in_any(px_, py, boxes):
    for (ox, oy, ow, oh) in boxes:
        if ox <= px_ < ox + ow and oy <= py < oy + oh:
            return True
    return False


def measure(b, els, overlays, vw, vh):
    sx = int(b.ev("Math.round(window.scrollX)") or 0)
    sy = int(b.ev("Math.round(window.scrollY)") or 0)
    xs0 = max(0, min(e["rect"][0] for e in els))
    ys0 = max(0, min(e["rect"][1] for e in els))
    xs1 = min(vw, max(e["rect"][0] + e["rect"][2] for e in els))
    ys1 = min(vh, max(e["rect"][1] + e["rect"][3] for e in els))
    box = (xs0, ys0, max(1, xs1 - xs0), max(1, ys1 - ys0))
    shot(b, SHOT["A"], box, sx, sy)
    b.ev(HIDE)
    b.ev("new Promise(function(r){setTimeout(r,200)})", await_promise=True)
    shot(b, SHOT["B"], box, sx, sy)
    b.ev(KILL_CANVAS)
    b.ev("new Promise(function(r){setTimeout(r,200)})", await_promise=True)
    shot(b, SHOT["C"], box, sx, sy)
    b.ev(UNKILL_CANVAS)
    b.ev(KILL_COVERS)
    b.ev("new Promise(function(r){setTimeout(r,200)})", await_promise=True)
    shot(b, SHOT["D"], box, sx, sy)
    assert int(b.ev("Math.round(window.scrollY)") or 0) == sy, "page scrolled mid-capture"
    b.ev(UNKILL_COVERS)
    b.ev(UNHIDE)
    b.ev("new Promise(function(r){setTimeout(r,160)})", await_promise=True)
    A, B, Cc, D = (png.Img(SHOT[k]) for k in "ABCD")
    ratio, pxA, pxB, pxC, pxD = png.ratio, A.px, B.px, Cc.px, D.px
    res = []
    for e in els:
        x, y, w, h = e["rect"]
        x0, y0 = max(0, max(0, x) - box[0]), max(0, max(0, y) - box[1])
        x1 = min(A.w, B.w, Cc.w, D.w, min(vw, x + w) - box[0])
        y1 = min(A.h, B.h, Cc.h, D.h, min(vh, y + h) - box[1])
        lo, lopx, ng, cd, vd, nodelta = None, None, 0, 0, 0, None
        olo, olopx, ong = None, None, 0          # the OCCLUDED pixels, kept apart
        inks = [tuple(i) for i in e["inks"]]
        # boxes are in viewport coords, the loop in box-local coords
        obox = [(overlays[i]["rect"][0] - box[0], overlays[i]["rect"][1] - box[1],
                 overlays[i]["rect"][2], overlays[i]["rect"][3])
                for i in e.get("ov", [])]
        for py in range(y0, y1):
            for px_ in range(x0, x1):
                a, bb = pxA(px_, py), pxB(px_, py)
                if abs(a[0]-bb[0]) + abs(a[1]-bb[1]) + abs(a[2]-bb[2]) < THRESH:
                    continue
                occ = obox and in_any(px_, py, obox)
                if occ:
                    ong += 1
                    for ink in inks:
                        r_ = ratio(ink, bb)
                        if olo is None or r_ < olo:
                            olo, olopx = r_, (ink, bb)
                    continue
                ng += 1
                cc, dd = pxC(px_, py), pxD(px_, py)
                d1 = max(abs(bb[0]-cc[0]), abs(bb[1]-cc[1]), abs(bb[2]-cc[2]))
                if d1 > cd:
                    cd = d1
                d2 = max(abs(bb[0]-dd[0]), abs(bb[1]-dd[1]), abs(bb[2]-dd[2]))
                if d2 > vd:
                    vd = d2
                for ink in inks:
                    r_ = ratio(ink, bb)
                    if lo is None or r_ < lo:
                        lo, lopx, nodelta = r_, (ink, bb), cc
        row = {"sel": e["sel"], "kind": e["kind"], "path": e["path"],
               "text": e["text"], "fpx": e["fpx"], "weight": e["weight"],
               "large": e["large"], "need": 3.0 if e["large"] else 4.5,
               "occludedPx": ong,
               "occluders": [overlays[i]["sel"] for i in e.get("ov", [])],
               "worstOccluded": round(olo, 2) if olo is not None else None}
        if lo is None:
            # every glyph pixel of this element was under an overlay: it has no
            # unoccluded value at this scroll position, and it is NOT cleared.
            if olo is None:
                continue
            row.update({"glyphPx": 0, "worst": None, "ink": list(olopx[0]),
                        "backdrop": list(olopx[1]), "backdropNoCanvas": None,
                        "canvasDelta": None, "coverDelta": None,
                        "overCanvas": None, "overCover": None,
                        "fullyOccluded": True})
        else:
            row.update({"glyphPx": ng, "worst": round(lo, 2),
                        "ink": list(lopx[0]), "backdrop": list(lopx[1]),
                        "backdropNoCanvas": list(nodelta),
                        "canvasDelta": cd, "coverDelta": vd,
                        "overCanvas": cd > 0, "overCover": vd > 0,
                        "fullyOccluded": False})
        res.append(row)
    return res


def run(theme, vw, vh, draws, tag, routes):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9437")))
    rows = []
    seed = os.environ.get("V32_PASSPORT", "")
    t_start = time.time()
    try:
        boot = "try{localStorage.setItem('pigment-theme','%s');" % theme
        if seed:
            boot += "localStorage.setItem('pigment.taste.v1',%s);" % json.dumps(SEED_PASSPORT)
        boot += "}catch(e){}"
        b.cmd("Page.addScriptToEvaluateOnNewDocument", {"source": boot})
        b.cmd("Emulation.setEmulatedMedia",
              {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        b.metrics(vw, vh)
        for d in range(draws):
            for r in routes:
                b.goto("%s/index.html?v32=%d-%d-%d%s"
                       % (cdp.BASE, d, int(time.time() * 1000) % 999983, PID, r),
                       settle=1.9)
                assert b.ev("document.documentElement.dataset.theme") == theme
                assert b.ev("window.innerWidth") == vw
                assert b.ev("matchMedia('(prefers-reduced-motion: reduce)').matches") is True
                wait_settled(b)
                worst_route, nb, nel, noc, nov, nocc = 99.0, 0, 0, 0, 0, 0
                y, step = 0, int(vh * 0.85)
                maxb = int(os.environ.get("V32_MAXBANDS", "8"))
                seen, dry = set(), 0
                while nb < maxb:
                    b.ev("window.scrollTo(0,%d)" % y)
                    b.ev("new Promise(function(r){setTimeout(r,280)})", await_promise=True)
                    at = b.ev("Math.round(window.scrollY)")
                    det = detect_stable(b)
                    nb += 1
                    if det["els"]:
                        nel += len(det["els"])
                        for x in measure(b, det["els"], det.get("overlays", []), vw, vh):
                            x.update({"route": r, "draw": d, "theme": theme,
                                      "vw": vw, "vh": vh, "scrollY": at})
                            rows.append(x)
                            if x["overCanvas"]:
                                noc += 1
                            if x["overCover"]:
                                nov += 1
                            if x["occludedPx"]:
                                nocc += 1
                            if x["worst"] is not None and x["worst"] < x["need"] \
                                    and x["worst"] < worst_route:
                                worst_route = x["worst"]
                        assert json.loads(b.ev(DETECT))["els"], "restore lost the text"
                    fresh = {(e["sel"], e["path"]) for e in det["els"]} - seen
                    seen |= fresh
                    dry = 0 if fresh else dry + 1
                    if dry >= 3:
                        break
                    page_h = json.loads(b.ev(SETTLE))["h"]
                    ymax = max(0, page_h - vh)
                    if at >= ymax - 2 or y > ymax:
                        break
                    y = min(ymax, y + step)
                print("d%-2d %-32s bands=%-2d els=%-4d canvas=%-4d cover=%-3d occl=%-4d worstFail %s  [%ds]"
                      % (d, r, nb, nel, noc, nov, nocc,
                         "-" if worst_route > 90 else "%.2f" % worst_route,
                         int(time.time() - t_start)), flush=True)
    finally:
        b.close()
    json.dump({"theme": theme, "viewport": [vw, vh], "draws": draws,
               "routes": routes, "rows": rows},
              open(os.path.join(OUT, "triple-%s.json" % tag), "w"))
    summarise(rows)
    return rows


def surface(r):
    if r["overCanvas"] and r["overCover"]:
        return "canvas+cover"
    if r["overCanvas"]:
        return "#bg-canvas"
    if r["overCover"]:
        return "cover"
    return "opaque"


def summarise(rows):
    """Report by TRIPLE — (ink, size, backdrop class) — not by host. A13."""
    by = {}
    for r in rows:
        if r["worst"] is None:
            continue
        k = (tuple(r["ink"]), round(r["fpx"], 1), r["weight"], surface(r))
        if k not in by or r["worst"] < by[k]["worst"]:
            by[k] = r
    fails = [r for r in by.values() if r["worst"] < r["need"]]
    print("\nTRIPLES (ink, size, measured backdrop class): %d distinct, %d below floor"
          % (len(by), len(fails)))
    for k, r in sorted(by.items(), key=lambda kv: kv[1]["worst"]):
        bad = r["worst"] < r["need"]
        print("  %-6s %6.2f need %.1f  %-16s %5.1fpx w%-3d  %-34s %-26s %s -> %s"
              % ("FAIL" if bad else "pass", r["worst"], r["need"], k[3], k[1], k[2],
                 r["sel"][:34], r["route"][:26], str(r["ink"]), str(r["backdrop"])))


if __name__ == "__main__":
    th, w, h, n, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rt = sys.argv[6].split(",") if len(sys.argv) > 6 else ROUTES
    if rt == ["ERAS"]:
        rt = ERA_ROUTES
    elif rt == ["FULL"]:
        # the 26 route cases + the other seven members of the #/era/* family,
        # because that family is the one that produced F-8 and one of its eight
        # cells passed by chance in the sampling that missed it.
        rt = ROUTES + [r for r in ERA_ROUTES if r not in ROUTES]
    run(th, w, h, n, tag, rt)
