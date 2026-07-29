"""AC19 / F-8 — unit 31. Targeted backdrop attribution for the surviving
`--faint` call sites, measured on real rendered glyph pixels.

Why a new instrument and not another canvastext.py sweep. Unit 28's sweep
answers "which of the elements it can SEE are over #bg-canvas". Three of the
six sites unit 29 cleared are invisible to it:

  * `#search::placeholder` is a pseudo-element. It owns no text node, so the
    DETECT walk never enumerates it and its ink is never scored.
  * `.tn-count` and `.tm-lab` are SVG `<text>`. Their ink is `fill:`, not
    `color:`, so unit 28's HIDE (which sets `color`/`-webkit-text-fill-color`)
    does not remove the glyphs: shot A equals shot B, no glyph pixels are
    found, and the element silently drops out of every table. This is exactly
    what Van Eyck reported he could not verify.
  * `.sr-group`/`.sr-more` only exist after a query is typed into the header
    search, which no sweep does.

So this probe is driven by SELECTOR rather than by a page walk, hides the
target's ink with an injected rule (which reaches pseudo-elements and `fill`
alike), and drives each site's precondition explicitly.

FOUR shots per (site, draw):
  A  page as rendered
  B  the target selector's ink forced transparent (colour, -webkit-text-fill,
     fill, text-shadow, text-decoration-colour)
  C  B, plus `#bg-canvas` display:none            -> canvasDelta
  D  B, plus every cover canvas visibility:hidden -> coverDelta

A pixel is a glyph pixel where A and B differ strongly; its backdrop is B, the
surface as actually composited. `canvasDelta > 0` means the generative
site-wide canvas is part of that backdrop (unit 28's paint test, inherited).
`coverDelta > 0` means a canvasTag() cover is. Both zero means the glyph sits
on opaque paint, and the measured backdrop is deterministic.

Inherited corrections, both load-bearing:
  * unit 30 / V-F2 — `Page.captureScreenshot`'s clip is in PAGE coordinates
    while rects are in VIEWPORT coordinates; scrollY is added at the capture.
  * unit 30 — covers are hidden with `visibility:hidden`, never `display:none`:
    several canvasTag sites emit an IN-FLOW canvas and display:none reflows the
    document between shots. `#bg-canvas` is `position:fixed`, so display:none
    there moves nothing and unit 28's rule still holds for it.

`prefers-reduced-motion: reduce` is emulated, so the canvas paints one static
t=0 frame; it is Math.random-seeded per load, so every site is loaded --draws
times behind a unique query string and the WORST value is reported.

usage: python3 inkprobe.py <theme> <w> <h> <draws> <tag> [site,site,...]
"""
import base64, json, os, sys, time

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp, png

OUT = os.path.dirname(os.path.abspath(__file__))
PID = os.getpid()
SHOT = {k: "/tmp/u31-%s-%d.png" % (k, PID) for k in "ABCD"}
THRESH = 60

# A passport with admirations is the precondition for #/taste; without it the
# route renders the empty state and neither .tm-lab nor .pp-card-loading exists.
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

TYPE_QUERY = ("(function(){var i=document.getElementById('search');if(!i)return false;"
              "i.focus();i.value='van';"
              "i.dispatchEvent(new Event('input',{bubbles:true}));return true;})()")

# `.search-results` is max-height:380px / overflow-y:auto, so `.sr-more` sits in
# the CLIPPED-AWAY part of the panel and is never painted at rest. Unit 27's
# lesson (a rect proves nothing about paint) applies: scroll the panel to the
# bottom so the element under test is genuinely on screen before measuring.
TYPE_QUERY_END = ("(function(){var i=document.getElementById('search');if(!i)return false;"
                  "i.focus();i.value='van';"
                  "i.dispatchEvent(new Event('input',{bubbles:true}));"
                  "var p=document.querySelector('.search-results');"
                  "if(p)p.scrollTop=p.scrollHeight;return true;})()")

# The family tree is behind a view toggle; the cards view is the default, so no
# sweep that only loads the route ever renders `.tn-count`.
SHOW_TREE = ("(function(){var b=document.querySelector('.f-btn[data-view=\"tree\"]');"
             "if(!b)return false;b.click();return true;})()")

# `.pp-card-loading` is a TRANSIENT state: viewTaste() schedules
# drawCardPreview() on the next animation frame, which replaces the holder's
# contents with the painted canvas, so by the time any instrument can look the
# element is gone. The markup below is `js/app.js:3457` verbatim, put back into
# its own real host on the real route: the HOST, its paint and the page around
# it are the shipped ones and are what the measurement is about — only the
# moment is forced. Recorded as a deviation in the unit 31 log.
REINSTATE_LOADING = ("(function(){var h=document.getElementById('pp-card-prev');"
                     "if(!h)return false;"
                     "h.innerHTML='<div class=\"pp-card-loading\">mixing pigment\u2026</div>';"
                     "return true;})()")

# site id -> (route, selector, prep JS or None, note)
SITES = {
    "tl-year":         ("#/era/16th-century", ".tl-year", None,
                        "era start/end years"),
    "tl-year-19":      ("#/era/19th-century", ".tl-year", None,
                        "era start/end years"),
    "search-ph":       ("#/", "#search::placeholder", None,
                        "header search placeholder"),
    "sr-group":        ("#/", ".search-results .sr-group", TYPE_QUERY,
                        "search results group label"),
    "sr-more":         ("#/", ".search-results .sr-more", TYPE_QUERY_END,
                        "search results overflow line"),
    "tn-count":        ("#/movements", ".tree-svg .tn-count", SHOW_TREE,
                        "SVG fill: branch painter count"),
    "tn-count-tech":   ("#/techniques", ".tree-svg .tn-count", SHOW_TREE,
                        "SVG fill: branch painter count"),
    "tm-lab":          ("#/taste", ".tm-lab", None,
                        "SVG fill: taste map axis labels"),
    "pp-card-loading": ("#/taste", ".pp-card-loading", REINSTATE_LOADING,
                        "passport card loading state (transient — re-instated)"),
    "tl2-year":        ("#/timeline", ".tl2-year", None,
                        "grand timeline gridline years (not in unit 29's list)"),
}

ORDER = ["tl-year", "tl-year-19", "search-ph", "sr-group", "sr-more",
         "tn-count", "tn-count-tech", "tm-lab", "pp-card-loading", "tl2-year"]

# The target's own ink, wherever it lives: `color` for HTML, `fill` for SVG
# <text>, and the pseudo-element's computed colour for `::placeholder`.
LOCATE = r"""(function(sel){
 var pseudo=null,base=sel;
 var m=sel.match(/^(.*?)(::[a-z-]+)$/);
 if(m){base=m[1];pseudo=m[2];}
 var out=[];
 [].forEach.call(document.querySelectorAll(base),function(el,idx){
  var cs=getComputedStyle(el,pseudo||undefined);
  if(cs.display==='none'||cs.visibility==='hidden')return;
  if(parseFloat(cs.opacity)<0.99)return;
  var r=el.getBoundingClientRect();
  if(r.width<2||r.height<2)return;
  var paint=cs.fill&&cs.fill!=='none'&&el.ownerSVGElement?cs.fill:cs.color;
  var p=paint.match(/[\d.]+/g);if(!p)return;
  var fpx=parseFloat(cs.fontSize),wt=parseInt(cs.fontWeight,10)||400;
  var path=[],n=el;
  while(n&&n!==document.body){path.unshift(n.tagName.toLowerCase()+
    (n.classList&&n.classList.length?'.'+[].slice.call(n.classList).join('.'):''));
   n=n.parentElement;}
  out.push({idx:idx,
            rect:[Math.round(r.left),Math.round(r.top),
                  Math.round(r.width),Math.round(r.height)],
            docTop:Math.round(r.top+window.scrollY),
            ink:[+p[0],+p[1],+p[2]],fpx:fpx,weight:wt,
            large:(fpx>=24||(fpx>=18.66&&wt>=700)),
            path:path.slice(-3).join(' > '),
            text:(el.textContent||'').trim().replace(/\s+/g,' ').slice(0,30)});});
 return JSON.stringify(out);})(%s)"""

HIDE = r"""(function(sel){
 var s=document.createElement('style');s.id='u31-hide';
 s.textContent=sel+'{color:transparent!important;'+
   '-webkit-text-fill-color:transparent!important;fill:transparent!important;'+
   'text-shadow:none!important;text-decoration-color:transparent!important}';
 document.head.appendChild(s);return true;})(%s)"""

UNHIDE = ("(function(){var s=document.getElementById('u31-hide');"
          "if(s)s.parentNode.removeChild(s);return true;})()")

KILL_CANVAS = ("(function(){var c=document.getElementById('bg-canvas');"
               "if(c)c.style.setProperty('display','none','important');return !!c;})()")
UNKILL_CANVAS = ("(function(){var c=document.getElementById('bg-canvas');"
                 "if(c)c.style.removeProperty('display');return true;})()")

# visibility, not display: unit 30's correction. Several canvasTag sites are
# in flow and display:none would reflow the page between shots.
KILL_COVERS = ("(function(){var n=0;[].forEach.call("
               "document.querySelectorAll('canvas:not(#bg-canvas)'),function(c){"
               "c.style.setProperty('visibility','hidden','important');n++;});return n;})()")
UNKILL_COVERS = ("(function(){[].forEach.call("
                 "document.querySelectorAll('canvas:not(#bg-canvas)'),function(c){"
                 "c.style.removeProperty('visibility');});return true;})()")

SETTLE = """(function(){var im=[].slice.call(document.images);
 return JSON.stringify({pending:im.filter(function(i){return !i.complete;}).length,
  h:document.body.scrollHeight});})()"""


def wait_settled(b, tries=24):
    last = None
    for _ in range(tries):
        st = json.loads(b.ev(SETTLE))
        if st["pending"] == 0 and last == st["h"]:
            return st
        last = st["h"]
        b.ev("new Promise(function(r){setTimeout(r,180)})", await_promise=True)
    return json.loads(b.ev(SETTLE))


def shot(b, path, box, sx, sy):
    """Clip is in PAGE coordinates, box is in VIEWPORT coordinates — unit 30."""
    x, y, w, h = box
    r = b.cmd("Page.captureScreenshot",
              {"format": "png", "captureBeyondViewport": False,
               "clip": {"x": x + sx, "y": y + sy, "width": w, "height": h, "scale": 1}})
    open(path, "wb").write(base64.b64decode(r["data"]))


def js(sel):
    return json.dumps(sel)


def visible_frac(rect, vw, vh):
    """Fraction of an element's box inside the viewport.

    Not a containment test. `.search-results` is `right:0` on a 220 px wrapper
    and 335 px wide, so at 390 px its left edge is at -9 and every `.sr-group`
    row reports left = -2 — a 2 px sliver off-screen, with every glyph fully
    painted. Requiring total containment discarded those rows and reported the
    site unverified, which would have been a coverage gap dressed up as a
    limitation. The screenshot clip and the per-pixel loop already clamp to the
    viewport, so a box that is >=90% on screen is measured on the part that is
    actually painted; anything less is dropped and recorded as not measured.
    """
    x, y, w, h = rect
    ix = max(0, min(vw, x + w) - max(0, x))
    iy = max(0, min(vh, y + h) - max(0, y))
    area = float(max(1, w * h))
    return (ix * iy) / area


def probe(b, sel, els, vw, vh):
    sx = int(b.ev("Math.round(window.scrollX)") or 0)
    sy = int(b.ev("Math.round(window.scrollY)") or 0)
    xs0 = max(0, min(e["rect"][0] for e in els))
    ys0 = max(0, min(e["rect"][1] for e in els))
    xs1 = min(vw, max(e["rect"][0] + e["rect"][2] for e in els))
    ys1 = min(vh, max(e["rect"][1] + e["rect"][3] for e in els))
    box = (xs0, ys0, max(1, xs1 - xs0), max(1, ys1 - ys0))
    shot(b, SHOT["A"], box, sx, sy)
    b.ev(HIDE % js(sel))
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
    A, B, Cc, D = (png.Img(SHOT[k]) for k in "ABCD")
    res = []
    for e in els:
        x, y, w, h = e["rect"]
        x0, y0 = max(0, max(0, x) - box[0]), max(0, max(0, y) - box[1])
        x1 = min(A.w, B.w, Cc.w, D.w, min(vw, x + w) - box[0])
        y1 = min(A.h, B.h, Cc.h, D.h, min(vh, y + h) - box[1])
        lo, lopx, ng, cdmax, vdmax, nodelta = None, None, 0, 0, 0, None
        for py in range(y0, y1):
            for px_ in range(x0, x1):
                a, bb = A.px(px_, py), B.px(px_, py)
                if abs(a[0]-bb[0]) + abs(a[1]-bb[1]) + abs(a[2]-bb[2]) < THRESH:
                    continue
                ng += 1
                cc, dd = Cc.px(px_, py), D.px(px_, py)
                cdmax = max(cdmax, max(abs(bb[i]-cc[i]) for i in range(3)))
                vdmax = max(vdmax, max(abs(bb[i]-dd[i]) for i in range(3)))
                r_ = png.ratio(tuple(e["ink"]), bb)
                if lo is None or r_ < lo:
                    lo, lopx, nodelta = r_, bb, cc
        if lo is None:
            continue
        res.append({"sel": sel, "path": e["path"], "text": e["text"],
                    "fpx": e["fpx"], "large": e["large"],
                    "need": 3.0 if e["large"] else 4.5,
                    "glyphPx": ng, "worst": round(lo, 2),
                    "ink": e["ink"], "backdrop": list(lopx),
                    "backdropNoCanvas": list(nodelta),
                    "canvasDelta": cdmax, "coverDelta": vdmax,
                    "overCanvas": cdmax > 0, "overCover": vdmax > 0})
    return res


def run(theme, vw, vh, draws, tag, sites):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9421")))
    rows, misses = [], []
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s');"
                         "localStorage.setItem('pigment.taste.v1',%s)}catch(e){}"
                         % (theme, json.dumps(SEED_PASSPORT))})
        b.cmd("Emulation.setEmulatedMedia",
              {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        b.metrics(vw, vh)
        for d in range(draws):
            for sid in sites:
                route, sel, prep, note = SITES[sid]
                b.goto("%s/index.html?u31=%d-%d-%d%s"
                       % (cdp.BASE, d, int(time.time() * 1000) % 999983, PID, route),
                       settle=1.9)
                assert b.ev("document.documentElement.dataset.theme") == theme
                assert b.ev("window.innerWidth") == vw
                assert b.ev("matchMedia('(prefers-reduced-motion: reduce)').matches") is True
                if os.environ.get("U31_BEFORE_CSS"):
                    assert b.ev("(function(){var s=document.createElement('style');"
                                "s.textContent=%s;document.head.appendChild(s);return true;})()"
                                % json.dumps(os.environ["U31_BEFORE_CSS"])) is True
                wait_settled(b)
                if prep:
                    assert b.ev(prep) is True
                    b.ev("new Promise(function(r){setTimeout(r,420)})", await_promise=True)
                found = json.loads(b.ev(LOCATE % js(sel)))
                if not found:
                    misses.append((sid, sel, route, "selector matched nothing"))
                    print("draw %-2d %-16s %-30s NOT PRESENT" % (d, sid, sel), flush=True)
                    continue
                # A selector's matches can be spread across a strip wider or
                # taller than one viewport — `.tl2-year` lives in `.tl2-inner`,
                # which is `width:<W>px` inside an `overflow-x:auto` wrapper, so
                # at 390 px most of them are scrolled off horizontally. Anchor on
                # three matches (first, middle, last) and use scrollIntoView,
                # which scrolls EVERY scrollable ancestor, not just the window.
                # Only fully-visible rects are measured: a clipped rect proves
                # nothing about paint (unit 27).
                anchors, got, seen_idx = sorted({0, len(found) // 2, len(found) - 1}), [], set()
                unstable = 0
                for ai in anchors:
                    b.ev("(function(){var e=document.querySelectorAll(%s)[%d];"
                         "if(e)e.scrollIntoView({block:'center',inline:'center'});"
                         "return true;})()" % (js(sel.split("::")[0]), ai))
                    b.ev("new Promise(function(r){setTimeout(r,320)})", await_promise=True)
                    els = [e for e in json.loads(b.ev(LOCATE % js(sel)))
                           if visible_frac(e["rect"], vw, vh) >= 0.9]
                    els = [e for e in els if e["idx"] not in seen_idx]
                    if not els:
                        continue
                    seen_idx |= {e["idx"] for e in els}
                    pre = {e["idx"]: tuple(e["rect"]) for e in els}
                    res = probe(b, sel, els, vw, vh)
                    # STABILITY GUARD. The header search panel re-renders on its
                    # own input debounce and resets its own scrollTop, which can
                    # land between shots A and B; the differential then compares
                    # two different documents and returns nonsense (a `.sr-group`
                    # row scored 1.00 against a backdrop equal to its own ink).
                    # Nothing may move between the four shots, so re-locate after
                    # them and discard the batch if any measured rect has moved.
                    post = {e["idx"]: tuple(e["rect"])
                            for e in json.loads(b.ev(LOCATE % js(sel)))}
                    if any(post.get(i) != r for i, r in pre.items()):
                        unstable += len(res)
                        continue
                    got += res
                if unstable:
                    print("draw %-2d %-16s %-30s DISCARDED %d unstable row(s)"
                          % (d, sid, sel, unstable), flush=True)
                if not got:
                    why = ("every batch discarded by the stability guard" if unstable
                           else "present but never 90% in viewport")
                    misses.append((sid, sel, route, why))
                    print("draw %-2d %-16s %-30s NOT MEASURED (%s)" % (d, sid, sel, why),
                          flush=True)
                    continue
                for x in got:
                    x.update({"site": sid, "route": route, "draw": d, "theme": theme,
                              "vw": vw, "vh": vh, "note": note})
                    rows.append(x)
                w = min(x["worst"] for x in got)
                print("draw %-2d %-16s %-30s n=%-2d/%-3d worst %5.2f canvas=%-3d cover=%-3d"
                      % (d, sid, sel, len(got), len(found), w,
                         max(x["canvasDelta"] for x in got),
                         max(x["coverDelta"] for x in got)), flush=True)
    finally:
        b.close()
    json.dump({"theme": theme, "viewport": [vw, vh], "draws": draws,
               "rows": rows, "misses": misses},
              open(os.path.join(OUT, "ink-%s.json" % tag), "w"))
    summarise(rows, misses)
    return rows


def summarise(rows, misses):
    by = {}
    for r in rows:
        k = r["site"]
        if k not in by or r["worst"] < by[k]["worst"]:
            by[k] = r
    print("\nWORST OBSERVED PER SITE (all draws)")
    fails = 0
    for k, r in sorted(by.items(), key=lambda kv: kv[1]["worst"]):
        bad = r["worst"] < r["need"]
        fails += bad
        surf = "#bg-canvas" if r["overCanvas"] else ("cover" if r["overCover"] else "opaque paint")
        print("  %-16s %-26s %6.2f need %.1f %-4s %5.1fpx  on %-11s  ink %s -> %s (no-canvas %s)"
              % (k, r["sel"], r["worst"], r["need"], "FAIL" if bad else "pass",
                 r["fpx"], surf, str(r["ink"]), str(r["backdrop"]),
                 str(r["backdropNoCanvas"])))
    print("sites below floor: %d of %d measured" % (fails, len(by)))
    if misses:
        print("\nNOT MEASURED (unverified by this instrument)")
        for m in sorted(set(misses)):
            print("  %-16s %-30s %-22s %s" % m)


if __name__ == "__main__":
    th, w, h, n, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    st = sys.argv[6].split(",") if len(sys.argv) > 6 else ORDER
    run(th, w, h, n, tag, st)
