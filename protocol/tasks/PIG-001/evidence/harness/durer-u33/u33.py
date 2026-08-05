"""AC19 unit 33 — before/after measurement for V32-1 … V32-7.

This is NOT a new instrument. Every primitive is imported from Vermeer's unit-32
`sitecensus.py`: the four-shot paint differential (A as rendered, B target ink
transparent, C also `#bg-canvas` gone, D also every cover hidden), the corrected
clip origin (page coordinates = viewport rect + scrollY), `visibility:hidden`
cover-hiding, the 90 %-in-viewport gate and the rect-stability guard. What is
added here is only:

  * a site table for the seven findings under repair, including the two that
    unit 32 measured with `states.py` rather than `sitecensus.py`;
  * `hover=` on a site, forced through CDP `CSS.forcePseudoState` so the engine
    is asked for the state rather than the state being simulated (states.py's
    method, applied inside sitecensus.py's differential);
  * a six-width sweep — 320 / 390 / 900 / 1024 / 1280 / 1440 — where unit 32 ran
    two, because the theory pole's requested action 3 adds 900 and 1024;
  * multi-draw where a generative canvas is involved. `#bg-canvas` is
    Math.random-seeded, so a single draw can miss the corner (that is how F-8 was
    partly missed). N is reported per row.

usage:
  python3 u33.py <theme> <w> <h> <draws> <tag> [site,...]
env:
  V33_SUPPRESS='.ig-edge'   hides a named layer, for attribution
  PIG_BASE, CDP_PORT
"""
import json, os, sys, time

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
V = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/vermeer-u32"
sys.path.insert(0, C)
sys.path.insert(0, V)
import cdp                                    # noqa: E402
import sitecensus as sc                       # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))

TYPE_QUERY = sc.TYPE_QUERY
CLICK_NODE = ("(function(){var n=document.querySelector('.ig-node');"
              "if(!n)return false;n.dispatchEvent(new MouseEvent('click',"
              "{bubbles:true}));return true;})()")
ZOOM_EU = ("(function(){var b=document.querySelector('[data-zoom=\"europe\"]');"
           "if(!b)return false;b.click();return true;})()")

# unit 32 could not measure `#search::placeholder`: its LOCATE gates every
# pseudo-element on a non-empty `content`, and `::placeholder` computes
# `content:normal`. This is that gate lifted for `::placeholder` only — the rect
# and the differential are otherwise sitecensus.py's, unchanged.
LOCATE_PH = r"""(function(sel){
 var base=sel.replace(/::placeholder$/,'');
 var out=[];
 function rgb(s){var q=s&&s.match(/[\d.]+/g);
   return q&&q.length>=3?[Math.round(+q[0]),Math.round(+q[1]),Math.round(+q[2])]:null;}
 [].forEach.call(document.querySelectorAll(base),function(el,idx){
  if(el.value)return;
  if(!el.placeholder)return;
  var cs=getComputedStyle(el,'::placeholder');
  var r=el.getBoundingClientRect();
  if(r.width<2||r.height<2)return;
  var ink=rgb(cs.color); if(!ink)return;
  var fpx=parseFloat(cs.fontSize)||parseFloat(getComputedStyle(el).fontSize);
  var wt=parseInt(cs.fontWeight,10)||400;
  out.push({idx:idx,
            rect:[Math.round(r.left),Math.round(r.top),
                  Math.round(r.width),Math.round(r.height)],
            ink:ink,fpx:fpx,weight:wt,
            large:(fpx>=24||(fpx>=18.66&&wt>=700)),
            path:'input#'+el.id+'::placeholder',
            text:el.placeholder.slice(0,30)});});
 return JSON.stringify(out);})(%s)"""

# site id -> dict(route, sel, prep, hover, note)
#   hover: CSS selector whose elements get :hover forced before the differential
SITES = {
    # V32-1 / V32-2 — SVG fill: labels crossed by graph edges and node circles
    "ig-node-text": dict(route="#/influences", sel=".ig-node text", prep=None,
                         hover=None, note="V32-1 influence-graph labels"),
    "ig-node-lit":  dict(route="#/influences", sel="#ig-svg.focused .ig-node.lit text",
                         prep=CLICK_NODE, hover=None,
                         note="V32-2 focused graph's lit labels (state-only)"),
    # V32-3 — white hover ink on warm paper
    "chip-hover":   dict(route="#/artist/leonardo-da-vinci", sel="button.chip",
                         prep=None, hover="button.chip", note="V32-3 button.chip:hover"),
    "chip-hover-t": dict(route="#/taste", sel="button.chip", prep=None,
                         hover="button.chip", note="V32-3 button.chip:hover on #/taste"),
    "gonext-hover": dict(route="#/artist/leonardo-da-vinci", sel=".gonext-item b",
                         prep=None, hover=".gonext-item",
                         note="u32 NOT TESTED 9 — .gonext-item:hover b"),
    # V32-4 — --muted directly on #bg-canvas on an unwalked route
    "le-meta":      dict(route="#/list/paintings-that-still-scare-us", sel=".le-meta",
                         prep=None, hover=None, note="V32-4 list entry metadata"),
    # V32-5 / V32-6 — .tl2-year on its own gridline, binding element differs by theme
    "tl2-year":     dict(route="#/timeline", sel=".tl2-year", prep=None, hover=None,
                         note="V32-5/6 century labels on the .tl2-grid rule"),
    "tl2-year-now": dict(route="#/timeline", sel=".tl2-year.now", prep=None, hover=None,
                         note="V32-5/6 the 'today' label on the gold now rule"),
    # V32-7 — the open search panel overpainted by .main-nav at 390
    "sr-group":     dict(route="#/", sel=".search-results .sr-group", prep=TYPE_QUERY,
                         hover=None, note="V32-7 result group label under .main-nav"),
    "sr-meta":      dict(route="#/", sel=".search-results .sr-meta", prep=TYPE_QUERY,
                         hover=None, note="V32-7 sibling — must not regress"),
    # u32 NOT TESTED 7 — same SVG fill: class as V32-1, in no prior enumeration
    "map-dot-name": dict(route="#/nations", sel=".md-name", prep=ZOOM_EU,
                         hover=None,
                         note="u32 NOT TESTED 7 — world-map dot labels (europe zoom only)"),
    # u32 NOT TESTED 1 — the placeholder its LOCATE gate could not see
    "search-ph":    dict(route="#/", sel="#search::placeholder", prep=None, hover=None,
                         locate=LOCATE_PH, note="u32 NOT TESTED 1 — #search::placeholder"),
}
ORDER = list(SITES.keys())


def force_hover(b, sel):
    doc = b.cmd("DOM.getDocument", {"depth": 0})["root"]["nodeId"]
    ids = b.cmd("DOM.querySelectorAll", {"nodeId": doc, "selector": sel})["nodeIds"]
    ids = [i for i in ids if i]
    for nid in ids:
        b.cmd("CSS.forcePseudoState", {"nodeId": nid, "forcedPseudoClasses": ["hover"]})
    return len(ids)


def run(theme, vw, vh, draws, tag, sites):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9463")))
    supp = os.environ.get("V33_SUPPRESS", "").strip()
    rows, misses = [], []
    try:
        sc.boot(b, theme)
        b.metrics(vw, vh)
        b.cmd("DOM.enable")
        b.cmd("CSS.enable")
        for d in range(draws):
            for sid in sites:
                S = SITES[sid]
                sel, route = S["sel"], S["route"]
                b.goto("%s/index.html?u33=%d-%d-%d%s"
                       % (cdp.BASE, d, int(time.time() * 1000) % 999983, os.getpid(), route),
                       settle=1.9)
                assert b.ev("document.documentElement.dataset.theme") == theme
                assert b.ev("window.innerWidth") == vw
                sc.wait_settled(b)
                if supp:
                    assert b.ev(sc.SUPPRESS % sc.js(supp)) is True
                if S["prep"]:
                    if b.ev(S["prep"]) is not True:
                        misses.append((sid, sel, route, "prep did not apply"))
                        print("d%-2d %-14s %-34s PREP FAILED" % (d, sid, sel), flush=True)
                        continue
                    b.ev("new Promise(function(r){setTimeout(r,420)})", await_promise=True)
                if S["hover"]:
                    n = force_hover(b, S["hover"])
                    if not n:
                        misses.append((sid, sel, route, "hover host matched nothing"))
                        print("d%-2d %-14s %-34s NO HOVER HOST" % (d, sid, sel), flush=True)
                        continue
                    b.ev("new Promise(function(r){setTimeout(r,420)})", await_promise=True)
                LOC = S.get("locate") or sc.LOCATE
                found = json.loads(b.ev(LOC % sc.js(sel)))
                if not found:
                    misses.append((sid, sel, route, "selector matched nothing"))
                    print("d%-2d %-14s %-34s NOT PRESENT" % (d, sid, sel), flush=True)
                    continue
                anchors = sorted({0, len(found) // 2, len(found) - 1})
                got, seen_idx, unstable = [], set(), 0
                for ai in anchors:
                    b.ev("(function(){var e=document.querySelectorAll(%s)[%d];"
                         "if(e&&e.scrollIntoView)e.scrollIntoView({block:'center',inline:'center'});"
                         "return true;})()" % (sc.js(sel.split("::")[0]), ai))
                    b.ev("new Promise(function(r){setTimeout(r,320)})", await_promise=True)
                    els = [e for e in json.loads(b.ev(LOC % sc.js(sel)))
                           if sc.visible_frac(e["rect"], vw, vh) >= 0.9
                           and e["idx"] not in seen_idx]
                    if not els:
                        continue
                    seen_idx |= {e["idx"] for e in els}
                    els = els[:40]
                    pre = {e["idx"]: tuple(e["rect"]) for e in els}
                    res = sc.probe(b, sel, els, vw, vh)
                    post = {e["idx"]: tuple(e["rect"])
                            for e in json.loads(b.ev(LOC % sc.js(sel)))}
                    if any(post.get(i) != r for i, r in pre.items()):
                        unstable += len(res)
                        continue
                    got += res
                if not got:
                    why = ("every batch discarded by the stability guard" if unstable
                           else "present but never 90% in viewport")
                    misses.append((sid, sel, route, why))
                    print("d%-2d %-14s %-34s NOT MEASURED (%s)" % (d, sid, sel, why), flush=True)
                    continue
                for x in got:
                    x.update({"site": sid, "route": route, "draw": d, "theme": theme,
                              "vw": vw, "vh": vh, "note": S["note"], "suppress": supp})
                    rows.append(x)
                w = min(x["worst"] for x in got)
                print("d%-2d %-14s %-34s n=%-3d worst %5.2f canvas=%-3d cover=%-3d %s"
                      % (d, sid, sel, len(got), w,
                         max(x["canvasDelta"] for x in got),
                         max(x["coverDelta"] for x in got),
                         "DISCARDED %d" % unstable if unstable else ""), flush=True)
    finally:
        b.close()
    json.dump({"theme": theme, "viewport": [vw, vh], "draws": draws,
               "suppress": supp, "rows": rows, "misses": misses},
              open(os.path.join(OUT, "u33-%s.json" % tag), "w"))
    sc.summarise(rows, misses)
    return rows


if __name__ == "__main__":
    th, w, h, n, tag = (sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
                        int(sys.argv[4]), sys.argv[5])
    st = sys.argv[6].split(",") if len(sys.argv) > 6 else ORDER
    run(th, w, h, n, tag, st)
