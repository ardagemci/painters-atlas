"""PIG-001 certification pass — INDEPENDENT contrast remeasurement. Vermeer.

Unit 33 (Dürer) reports all six open AC19 majors closed, 0 sites below floor
across twelve cells. Dürer measured his own work. This is the same question
asked by the reviewer's own instrument.

WHAT IS INHERITED, AND FROM WHOM
The four-shot paint differential is MY OWN (`vermeer-u32/sitecensus.py`):
  A  page as rendered
  B  the target selector's ink forced transparent by an INJECTED RULE
     (never visibility:hidden — that would delete the element's own background)
  C  B, plus #bg-canvas display:none              -> canvasDelta
  D  B, plus every cover canvas visibility:hidden -> coverDelta
A glyph pixel is where A and B differ strongly; its BACKDROP is B, the surface
as actually composited, measured rather than read from the stylesheet. Also
inherited from my own harness: the corrected clip origin (captureScreenshot's
`clip` is in page coords, getBoundingClientRect in viewport coords, so scrollY
is added at the shutter), the 90%-in-viewport gate, and the rect-stability
guard.

WHAT IS NOT INHERITED — this is the independence that matters
The SITE TABLE below is derived from the frozen findings and from reading
css/styles.css and js/app.js AT HEAD, not copied from unit 33's table. Where it
agrees with Dürer's, that is convergence on the same defect, not transcription.
Hover is forced through CDP `CSS.forcePseudoState` so the ENGINE is asked for
the state rather than the state being simulated.

RESULT DURABILITY
Every measured row is appended to `rows-<tag>.jsonl` as it is produced, so an
interrupted run leaves usable evidence rather than nothing. This has mattered
repeatedly in this task.

usage:
  python3 cert.py <theme> <w> <h> <draws> <tag> [site,...]
env: PIG_BASE, CDP_PORT
"""
import json, os, sys, time

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
V = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/vermeer-u32"
sys.path.insert(0, C)
sys.path.insert(0, V)
import cdp                                     # noqa: E402
import sitecensus as sc                        # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- preparations
TYPE_QUERY = ("(function(){var i=document.getElementById('search');if(!i)return false;"
              "i.focus();i.value='van';"
              "i.dispatchEvent(new Event('input',{bubbles:true}));return true;})()")
CLICK_NODE = ("(function(){var n=document.querySelector('.ig-node');"
              "if(!n)return false;n.dispatchEvent(new MouseEvent('click',"
              "{bubbles:true}));return true;})()")
ZOOM_EU = ("(function(){var b=document.querySelector('[data-zoom=\"europe\"]');"
           "if(!b)return false;b.click();return true;})()")

# `::placeholder` computes `content:normal`, which sitecensus.LOCATE gates out.
# This is that one gate lifted; rect, ink and differential are otherwise mine
# unchanged.
LOCATE_PH = r"""(function(sel){
 var base=sel.replace(/::placeholder$/,'');
 var out=[];
 function rgb(s){var q=s&&s.match(/[\d.]+/g);
   return q&&q.length>=3?[Math.round(+q[0]),Math.round(+q[1]),Math.round(+q[2])]:null;}
 [].forEach.call(document.querySelectorAll(base),function(el,idx){
  if(el.value)return; if(!el.placeholder)return;
  var cs=getComputedStyle(el,'::placeholder');
  var r=el.getBoundingClientRect();
  if(r.width<2||r.height<2)return;
  var ink=rgb(cs.color); if(!ink)return;
  var fpx=parseFloat(cs.fontSize)||parseFloat(getComputedStyle(el).fontSize);
  var wt=parseInt(cs.fontWeight,10)||400;
  out.push({idx:idx,rect:[Math.round(r.left),Math.round(r.top),
            Math.round(r.width),Math.round(r.height)],
            ink:ink,fpx:fpx,weight:wt,
            large:(fpx>=24||(fpx>=18.66&&wt>=700)),
            path:'input#'+el.id+'::placeholder',
            text:el.placeholder.slice(0,30)});});
 return JSON.stringify(out);})(%s)"""

# ---------------------------------------------------------------- site table
# id -> dict(route, sel, prep, hover, note). Derived from the frozen findings
# and from HEAD's stylesheet, not from unit 33's table.
SITES = {
    # --- the six previously-open majors ---
    "ig-node-text": dict(route="#/influences", sel=".ig-node text", prep=None, hover=None,
                         note="V32-1 graph labels — reported 1.01-1.39 -> 6.02-7.14"),
    "ig-node-lit":  dict(route="#/influences", sel="#ig-svg.focused .ig-node.lit text",
                         prep=CLICK_NODE, hover=None,
                         note="V32-2 FOCUSED graph lit labels — reported 2.72 -> 13.86/14.80"),
    "chip-hover":   dict(route="#/artist/leonardo-da-vinci", sel="button.chip", prep=None,
                         hover="button.chip",
                         note="V32-3 button.chip:hover — reported 1.18 light -> 9.43"),
    "le-meta":      dict(route="#/list/paintings-that-still-scare-us", sel=".le-meta",
                         prep=None, hover=None,
                         note="V32-4 list entry meta on #bg-canvas — reported -> 6.50/9.86"),
    "tl2-year":     dict(route="#/timeline", sel=".tl2-year", prep=None, hover=None,
                         note="V32-5/6 century labels — LIGHT binding element"),
    "tl2-year-now": dict(route="#/timeline", sel=".tl2-year.now", prep=None, hover=None,
                         note="V32-5/6 'today' label in --gold2 — DARK binding element"),
    "sr-group":     dict(route="#/", sel=".search-results .sr-group", prep=TYPE_QUERY,
                         hover=None,
                         note="V32-7 result group label — reported 1.00 -> 4.62 (worst in matrix)"),
    # --- the two residuals unit 33 additionally claims cleared ---
    "gonext-hover": dict(route="#/artist/leonardo-da-vinci", sel=".gonext-item b", prep=None,
                         hover=".gonext-item",
                         note="u32 measured-not-cleared — reported 13.89 light"),
    "search-ph":    dict(route="#/", sel="#search::placeholder", prep=None, hover=None,
                         locate=LOCATE_PH,
                         note="u32 measured-not-cleared — reported 5.17 light / 4.90 dark"),
    # --- non-regression controls ---
    "sr-meta":      dict(route="#/", sel=".search-results .sr-meta", prep=TYPE_QUERY,
                         hover=None, note="control — must not regress (u33: 6.42/5.68)"),
    # --- the residual unit 33 names but does not fix ---
    "map-dot-name": dict(route="#/nations", sel=".md-name", prep=ZOOM_EU, hover=None,
                         note="u33 §2.6 — contrast fixed, ~3px legibility residual at 320"),
}
ORDER = list(SITES.keys())


def force_hover(b, sel):
    """Ask the ENGINE for :hover rather than simulating it."""
    doc = b.cmd("DOM.getDocument", {"depth": 0})["root"]["nodeId"]
    ids = [i for i in b.cmd("DOM.querySelectorAll",
                            {"nodeId": doc, "selector": sel})["nodeIds"] if i]
    for nid in ids:
        b.cmd("CSS.forcePseudoState", {"nodeId": nid, "forcedPseudoClasses": ["hover"]})
    return len(ids)


def run(theme, vw, vh, draws, tag, sites):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9470")))
    jsonl = open(os.path.join(OUT, "rows-%s.jsonl" % tag), "a", buffering=1)
    rows, misses = [], []
    try:
        sc.boot(b, theme)
        b.cmd("DOM.enable"); b.cmd("CSS.enable")
        b.metrics(vw, vh)
        for d in range(draws):
            for sid in sites:
                s = SITES[sid]
                sel, prep, hov = s["sel"], s["prep"], s["hover"]
                locate = s.get("locate", sc.LOCATE)
                b.goto("%s/index.html?vcert=%d-%d-%d%s"
                       % (cdp.BASE, d, int(time.time() * 1000) % 999983, os.getpid(),
                          s["route"]), settle=1.9)
                # assert the cell is the cell claimed, every load
                assert b.ev("document.documentElement.dataset.theme") == theme
                assert b.ev("window.innerWidth") == vw, "viewport not honoured"
                assert b.ev("matchMedia('(prefers-reduced-motion: reduce)').matches") is True
                sc.wait_settled(b)
                if prep:
                    if b.ev(prep) is not True:
                        misses.append((sid, sel, s["route"], "prep did not apply"))
                        print("d%-2d %-14s %-34s PREP FAILED" % (d, sid, sel), flush=True)
                        continue
                    b.ev("new Promise(function(r){setTimeout(r,450)})", await_promise=True)
                if hov:
                    n = force_hover(b, hov)
                    if not n:
                        misses.append((sid, sel, s["route"], "hover target absent"))
                        print("d%-2d %-14s %-34s NO HOVER TARGET" % (d, sid, sel), flush=True)
                        continue
                    b.ev("new Promise(function(r){setTimeout(r,320)})", await_promise=True)
                found = json.loads(b.ev(locate % sc.js(sel)))
                if not found:
                    misses.append((sid, sel, s["route"], "selector matched nothing"))
                    print("d%-2d %-14s %-34s NOT PRESENT" % (d, sid, sel), flush=True)
                    continue
                anchors = sorted({0, len(found) // 2, len(found) - 1})
                got, seen_idx, unstable = [], set(), 0
                for ai in anchors:
                    b.ev("(function(){var e=document.querySelectorAll(%s)[%d];"
                         "if(e&&e.scrollIntoView)e.scrollIntoView({block:'center',inline:'center'});"
                         "return true;})()" % (sc.js(sel.split("::")[0]), ai))
                    b.ev("new Promise(function(r){setTimeout(r,320)})", await_promise=True)
                    if hov:
                        force_hover(b, hov)
                        b.ev("new Promise(function(r){setTimeout(r,220)})", await_promise=True)
                    els = [e for e in json.loads(b.ev(locate % sc.js(sel)))
                           if sc.visible_frac(e["rect"], vw, vh) >= 0.9
                           and e["idx"] not in seen_idx]
                    if not els:
                        continue
                    seen_idx |= {e["idx"] for e in els}
                    els = els[:40]
                    pre = {e["idx"]: tuple(e["rect"]) for e in els}
                    res = sc.probe(b, sel, els, vw, vh)
                    post = {e["idx"]: tuple(e["rect"])
                            for e in json.loads(b.ev(locate % sc.js(sel)))}
                    if any(post.get(i) != r for i, r in pre.items()):
                        unstable += len(res)
                        continue
                    got += res
                if not got:
                    why = ("every batch discarded by the stability guard" if unstable
                           else "present but never 90% in viewport")
                    misses.append((sid, sel, s["route"], why))
                    print("d%-2d %-14s %-34s NOT MEASURED (%s)" % (d, sid, sel, why), flush=True)
                    continue
                for x in got:
                    x.update({"site": sid, "route": s["route"], "draw": d, "theme": theme,
                              "vw": vw, "vh": vh, "note": s["note"]})
                    rows.append(x)
                    jsonl.write(json.dumps(x) + "\n")     # durable as produced
                w = min(x["worst"] for x in got)
                need = max(x["need"] for x in got)
                print("d%-2d %-14s %-34s n=%-3d worst %5.2f need %.1f %s canvas=%-3d cover=%-3d %s"
                      % (d, sid, sel, len(got), w, need,
                         "FAIL" if w < need else "pass",
                         max(x["canvasDelta"] for x in got),
                         max(x["coverDelta"] for x in got),
                         "DISCARDED %d" % unstable if unstable else ""), flush=True)
    finally:
        jsonl.close()
        b.close()
    json.dump({"theme": theme, "viewport": [vw, vh], "draws": draws,
               "rows": rows, "misses": misses},
              open(os.path.join(OUT, "cert-%s.json" % tag), "w"))
    sc.summarise(rows, misses)
    return rows


if __name__ == "__main__":
    th, w, h, n, tag = (sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
                        int(sys.argv[4]), sys.argv[5])
    st = sys.argv[6].split(",") if len(sys.argv) > 6 else ORDER
    run(th, w, h, n, tag, st)
