"""AC19 — the SELECTOR-driven half of the unit-32 census. Vermeer.

`triple.py` walks routes and scores every element that owns a text node. Three
classes are structurally invisible to any such walk, and this is the instrument
for them:

  * ::before / ::after with textual `content` — they own no text node and no rect
    of their own, so a page walk cannot even enumerate them, and if it could it
    could not separate their glyph pixels from their host's.
  * ::placeholder — same, and it only paints while the field is empty.
  * SVG <text> whose ink is `fill:` — triple.py DOES reach these (it injects a
    `fill:transparent` rule), but they are re-measured here one selector at a
    time as a cross-check on that rule.
  * anything that exists only in a STATE: search open, tree view, populated
    passport, hover, focus.

Method is the same four-shot paint differential as triple.py — A as rendered,
B target ink transparent, C also `#bg-canvas` gone, D also every cover hidden —
except that the ink is hidden by an INJECTED RULE for one selector, which reaches
pseudo-elements and `fill:` alike, and only that one selector's glyphs move
between A and B, so the pixels are unambiguously its own. That isolation is why
this is a separate pass and not an option on the walk.

`--suppress <selector>` additionally hides a named LAYER (visibility:hidden) for
a second measurement, which is how a failing site is ATTRIBUTED to the thing
behind it rather than to its own ink. Used to test N-31-1 and N-31-2.

usage:
  python3 sitecensus.py scan  <theme> <w> <h>              # enumerate pseudo inks
  python3 sitecensus.py probe <theme> <w> <h> <draws> <tag> [site,...]
env: V32_SUPPRESS='.tl2-grid'  hides that selector for the whole probe run
"""
import base64, json, os, sys, time

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp                                    # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pngfast as png                         # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
PID = os.getpid()
SHOT = {k: "/tmp/v32s-%s-%d.png" % (k, PID) for k in "ABCD"}
THRESH = 60

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

# ---------------------------------------------------------------- preparations
TYPE_QUERY = ("(function(){var i=document.getElementById('search');if(!i)return false;"
              "i.focus();i.value='van';"
              "i.dispatchEvent(new Event('input',{bubbles:true}));return true;})()")
TYPE_QUERY_END = ("(function(){var i=document.getElementById('search');if(!i)return false;"
                  "i.focus();i.value='van';"
                  "i.dispatchEvent(new Event('input',{bubbles:true}));"
                  "var p=document.querySelector('.search-results');"
                  "if(p)p.scrollTop=p.scrollHeight;return true;})()")
SHOW_TREE = ("(function(){var b=document.querySelector('.f-btn[data-view=\"tree\"]');"
             "if(!b)return false;b.click();return true;})()")
CLICK_FIRST = ("(function(){var b=document.querySelector('%s');"
               "if(!b)return false;b.click();return true;})()")

# site id -> (route, selector, prep JS or None, note)
SITES = {
    # --- pseudo-element ink, invisible to every page walk ---
    "trait-before":    ("#/artist/leonardo-da-vinci", ".trait::before", None,
                        "::before ✦ glyph, --teal"),
    "facts-before":    ("#/artist/leonardo-da-vinci", ".facts li::before", None,
                        "::before ✦ glyph, --gold2"),
    "branch-before":   ("#/movement/impressionism", ".branch-chip::before", None,
                        "::before ↳ glyph, --gold2"),
    "tone-after":      ("#/palette", ".tone.on::after", None,
                        "::after ✓ glyph, --gold2 (needs a selected tone)"),
    "search-ph":       ("#/", "#search::placeholder", None,
                        "header search placeholder, --faint"),
    # --- SVG fill: ink, cross-check on triple.py's injected fill rule ---
    "tn-count-mv":     ("#/movements", ".tree-svg .tn-count", SHOW_TREE,
                        "SVG fill: branch painter count"),
    "tn-count-tq":     ("#/techniques", ".tree-svg .tn-count", SHOW_TREE,
                        "SVG fill: branch painter count"),
    "tn-name-mv":      ("#/movements", ".tree-svg .tn-name", SHOW_TREE,
                        "SVG fill: branch name"),
    "tm-lab":          ("#/taste", ".tm-lab", None,
                        "SVG fill: taste map axis labels (populated passport)"),
    "tm-dot-lab":      ("#/taste", ".taste-map text", None,
                        "SVG fill: every <text> on the taste map"),
    # SVG fill: inks that appear in NO prior enumeration — not unit 29's list of
    # six, not unit 31's list of eight. Found by reading every `fill:var(--…)`
    # declaration in the stylesheet and then MEASURING each one.
    "ig-node-text":    ("#/influences", ".ig-node text", None,
                        "SVG fill: influence-graph painter labels, --muted 10.5px"),
    "ig-node-lit":     ("#/influences", "#ig-svg.focused .ig-node.lit text",
                        "(function(){var n=document.querySelector('.ig-node');"
                        "if(!n)return false;n.dispatchEvent(new MouseEvent('click',"
                        "{bubbles:true}));return true;})()",
                        "SVG fill: the FOCUSED graph's lit labels, --ink (state-only)"),
    "map-dot-name":    ("#/nations", ".map-dot .md-name", None,
                        "SVG fill: world-map dot labels, --muted"),
    # --- state-only surfaces ---
    "sr-group":        ("#/", ".search-results .sr-group", TYPE_QUERY,
                        "search results group label, --faint"),
    "sr-more":         ("#/", ".search-results .sr-more", TYPE_QUERY_END,
                        "search results overflow line, --faint"),
    "sr-meta":         ("#/", ".search-results .sr-meta", TYPE_QUERY,
                        "search results meta, --muted"),
    "sr-name":         ("#/", ".search-results .sr-name", TYPE_QUERY,
                        "search result name"),
    # --- N-31-1 / N-31-2 subjects ---
    "tl2-year":        ("#/timeline", ".tl2-year", None,
                        "grand timeline century labels on the .tl2-grid rule"),
    "tl2-year-now":    ("#/timeline", ".tl2-year.now", None,
                        "the 'today' label in --gold2 on the gold now rule"),
    "tl-year":         ("#/era/16th-century", ".tl-year", None,
                        "era start/end years — unit 31's fix"),
    "tl-year-19":      ("#/era/19th-century", ".tl-year", None,
                        "era start/end years — the cell that passed by chance"),
    # --- populated passport surfaces Van Eyck named unverifiable ---
    "pp-card-label":   ("#/palette", ".pp-card-prev *", None,
                        "passport card preview text, populated"),
    "taste-body":      ("#/taste", ".taste-wrap *", None,
                        "populated taste route text"),
    "palette-body":    ("#/palette", ".palette-wrap *", None,
                        "populated palette route text"),
}

ORDER = list(SITES.keys())

LOCATE = r"""(function(sel){
 var pseudo=null,base=sel;
 var m=sel.match(/^(.*?)(::[a-z-]+)$/);
 if(m){base=m[1];pseudo=m[2];}
 var out=[];
 function rgb(s){var q=s&&s.match(/[\d.]+/g);
   return q&&q.length>=3?[Math.round(+q[0]),Math.round(+q[1]),Math.round(+q[2])]:null;}
 var list;
 try{ list=document.querySelectorAll(base); }catch(e){ return "[]"; }
 [].forEach.call(list,function(el,idx){
  var cs=getComputedStyle(el,pseudo||undefined);
  if(cs.display==='none'||cs.visibility==='hidden')return;
  if(parseFloat(cs.opacity)<0.99)return;
  if(pseudo){var ct=cs.content;
   if(!ct||ct==='none'||ct==='normal')return;}
  var r=el.getBoundingClientRect();
  if(r.width<2||r.height<2)return;
  var svg=(el.namespaceURI==='http://www.w3.org/2000/svg');
  var paint=(svg&&cs.fill&&cs.fill!=='none')?cs.fill:cs.color;
  var ink=rgb(paint); if(!ink)return;
  var fpx=parseFloat(cs.fontSize),wt=parseInt(cs.fontWeight,10)||400;
  var path=[],n=el;
  while(n&&n!==document.body){path.unshift(n.tagName.toLowerCase()+
    (n.classList&&n.classList.length?'.'+[].slice.call(n.classList).join('.'):''));
   n=n.parentElement;}
  out.push({idx:idx,
            rect:[Math.round(r.left),Math.round(r.top),
                  Math.round(r.width),Math.round(r.height)],
            ink:ink,fpx:fpx,weight:wt,
            large:(fpx>=24||(fpx>=18.66&&wt>=700)),
            path:path.slice(-3).join(' > '),
            text:(pseudo?cs.content:(el.textContent||'')).trim()
                  .replace(/\s+/g,' ').slice(0,30)});});
 return JSON.stringify(out);})(%s)"""

HIDE = r"""(function(sel){
 var s=document.createElement('style');s.id='v32-hide';
 s.textContent=sel+'{color:transparent!important;'+
   '-webkit-text-fill-color:transparent!important;fill:transparent!important;'+
   'text-shadow:none!important;text-decoration-color:transparent!important}';
 document.head.appendChild(s);return true;})(%s)"""
UNHIDE = ("(function(){var s=document.getElementById('v32-hide');"
          "if(s)s.parentNode.removeChild(s);return true;})()")

SUPPRESS = r"""(function(sel){
 var s=document.createElement('style');s.id='v32-suppress';
 s.textContent=sel+'{visibility:hidden!important}';
 document.head.appendChild(s);return true;})(%s)"""

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

# ---- the pseudo-element PERIMETER scan: which ::before/::after actually carry
# glyphs on this route. No measurement — this is what defines the site list, so
# that the list is derived from the DOM rather than from my reading of the CSS.
SCAN = r"""(function(){
 var out={};
 [].forEach.call(document.querySelectorAll('*'),function(el){
  ['::before','::after','::placeholder','::marker','::first-letter'].forEach(function(pe){
   var cs;try{cs=getComputedStyle(el,pe);}catch(e){return;}
   if(!cs)return;
   var ct=cs.content;
   if(pe==='::placeholder'){
     if(el.tagName!=='INPUT'&&el.tagName!=='TEXTAREA')return;
     if(el.value)return;
     if(!el.placeholder)return;
   } else {
     if(!ct||ct==='none'||ct==='normal')return;
     if(!/[^\s'"]/.test(ct.replace(/^["']|["']$/g,'')))return;
     if(/^url\(/.test(ct))return;
   }
   if(cs.display==='none'||cs.visibility==='hidden')return;
   var sel=el.tagName.toLowerCase()+
     (el.classList&&el.classList.length?'.'+[].slice.call(el.classList).join('.'):'')+pe;
   var k=sel+'|'+cs.color+'|'+cs.fontSize;
   out[k]=(out[k]||0)+1;});});
 return JSON.stringify(out);})()"""


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
    x, y, w, h = box
    r = b.cmd("Page.captureScreenshot",
              {"format": "png", "captureBeyondViewport": False,
               "clip": {"x": x + sx, "y": y + sy, "width": w, "height": h, "scale": 1}})
    open(path, "wb").write(base64.b64decode(r["data"]))


def js(s):
    return json.dumps(s)


def visible_frac(rect, vw, vh):
    x, y, w, h = rect
    ix = max(0, min(vw, x + w) - max(0, x))
    iy = max(0, min(vh, y + h) - max(0, y))
    return (ix * iy) / float(max(1, w * h))


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
        lo, lopx, ng, cd, vd, nod = None, None, 0, 0, 0, None
        ink = tuple(e["ink"])
        for py in range(y0, y1):
            for px_ in range(x0, x1):
                a, bb = A.px(px_, py), B.px(px_, py)
                if abs(a[0]-bb[0]) + abs(a[1]-bb[1]) + abs(a[2]-bb[2]) < THRESH:
                    continue
                ng += 1
                cc, dd = Cc.px(px_, py), D.px(px_, py)
                cd = max(cd, max(abs(bb[i]-cc[i]) for i in range(3)))
                vd = max(vd, max(abs(bb[i]-dd[i]) for i in range(3)))
                r_ = png.ratio(ink, bb)
                if lo is None or r_ < lo:
                    lo, lopx, nod = r_, bb, cc
        if lo is None:
            continue
        res.append({"sel": sel, "path": e["path"], "text": e["text"],
                    "fpx": e["fpx"], "weight": e["weight"], "large": e["large"],
                    "need": 3.0 if e["large"] else 4.5,
                    "glyphPx": ng, "worst": round(lo, 2),
                    "ink": list(ink), "backdrop": list(lopx),
                    "backdropNoCanvas": list(nod),
                    "canvasDelta": cd, "coverDelta": vd,
                    "overCanvas": cd > 0, "overCover": vd > 0})
    return res


def boot(b, theme):
    b.cmd("Page.addScriptToEvaluateOnNewDocument",
          {"source": "try{localStorage.setItem('pigment-theme','%s');"
                     "localStorage.setItem('pigment.taste.v1',%s)}catch(e){}"
                     % (theme, json.dumps(SEED_PASSPORT))})
    b.cmd("Emulation.setEmulatedMedia",
          {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})


def scan(theme, vw, vh):
    """Enumerate every pseudo-element that carries glyphs, over the route table."""
    import triple
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9445")))
    agg = {}
    try:
        boot(b, theme)
        b.metrics(vw, vh)
        routes = triple.ROUTES + [r for r in triple.ERA_ROUTES if r not in triple.ROUTES]
        for r in routes:
            b.goto("%s/index.html?v32s=%d%s" % (cdp.BASE, PID, r), settle=1.5)
            wait_settled(b)
            for prep in (None, TYPE_QUERY, SHOW_TREE):
                if prep:
                    b.ev(prep)
                    b.ev("new Promise(function(r){setTimeout(r,350)})", await_promise=True)
                for k, n in json.loads(b.ev(SCAN)).items():
                    agg.setdefault(k, set()).add(r)
    finally:
        b.close()
    print("PSEUDO-ELEMENT INK SITES — %s %dx%d, over the full route table" % (theme, vw, vh))
    for k in sorted(agg):
        sel, colr, fs = k.split("|")
        print("  %-46s %-22s %-8s  on %d route(s): %s"
              % (sel, colr, fs, len(agg[k]), ", ".join(sorted(agg[k])[:4])))
    json.dump({k: sorted(v) for k, v in agg.items()},
              open(os.path.join(OUT, "pseudo-scan-%s-%d.json" % (theme, vw)), "w"))
    return agg


def run(theme, vw, vh, draws, tag, sites):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9445")))
    supp = os.environ.get("V32_SUPPRESS", "").strip()
    rows, misses = [], []
    try:
        boot(b, theme)
        b.metrics(vw, vh)
        for d in range(draws):
            for sid in sites:
                route, sel, prep, note = SITES[sid]
                b.goto("%s/index.html?v32=%d-%d-%d%s"
                       % (cdp.BASE, d, int(time.time() * 1000) % 999983, PID, route),
                       settle=1.9)
                assert b.ev("document.documentElement.dataset.theme") == theme
                assert b.ev("window.innerWidth") == vw
                assert b.ev("matchMedia('(prefers-reduced-motion: reduce)').matches") is True
                wait_settled(b)
                if supp:
                    assert b.ev(SUPPRESS % js(supp)) is True
                if prep:
                    if b.ev(prep) is not True:
                        misses.append((sid, sel, route, "prep did not apply"))
                        print("d%-2d %-16s %-30s PREP FAILED" % (d, sid, sel), flush=True)
                        continue
                    b.ev("new Promise(function(r){setTimeout(r,420)})", await_promise=True)
                found = json.loads(b.ev(LOCATE % js(sel)))
                if not found:
                    misses.append((sid, sel, route, "selector matched nothing"))
                    print("d%-2d %-16s %-30s NOT PRESENT" % (d, sid, sel), flush=True)
                    continue
                anchors = sorted({0, len(found) // 2, len(found) - 1})
                got, seen_idx, unstable = [], set(), 0
                for ai in anchors:
                    b.ev("(function(){var e=document.querySelectorAll(%s)[%d];"
                         "if(e&&e.scrollIntoView)e.scrollIntoView({block:'center',inline:'center'});"
                         "return true;})()" % (js(sel.split("::")[0]), ai))
                    b.ev("new Promise(function(r){setTimeout(r,320)})", await_promise=True)
                    els = [e for e in json.loads(b.ev(LOCATE % js(sel)))
                           if visible_frac(e["rect"], vw, vh) >= 0.9
                           and e["idx"] not in seen_idx]
                    if not els:
                        continue
                    seen_idx |= {e["idx"] for e in els}
                    els = els[:40]
                    pre = {e["idx"]: tuple(e["rect"]) for e in els}
                    res = probe(b, sel, els, vw, vh)
                    post = {e["idx"]: tuple(e["rect"])
                            for e in json.loads(b.ev(LOCATE % js(sel)))}
                    if any(post.get(i) != r for i, r in pre.items()):
                        unstable += len(res)
                        continue
                    got += res
                if not got:
                    why = ("every batch discarded by the stability guard" if unstable
                           else "present but never 90% in viewport")
                    misses.append((sid, sel, route, why))
                    print("d%-2d %-16s %-30s NOT MEASURED (%s)" % (d, sid, sel, why), flush=True)
                    continue
                for x in got:
                    x.update({"site": sid, "route": route, "draw": d, "theme": theme,
                              "vw": vw, "vh": vh, "note": note, "suppress": supp})
                    rows.append(x)
                w = min(x["worst"] for x in got)
                print("d%-2d %-16s %-30s n=%-3d worst %5.2f canvas=%-3d cover=%-3d %s"
                      % (d, sid, sel, len(got), w,
                         max(x["canvasDelta"] for x in got),
                         max(x["coverDelta"] for x in got),
                         "DISCARDED %d" % unstable if unstable else ""), flush=True)
    finally:
        b.close()
    json.dump({"theme": theme, "viewport": [vw, vh], "draws": draws,
               "suppress": supp, "rows": rows, "misses": misses},
              open(os.path.join(OUT, "site-%s.json" % tag), "w"))
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
        surf = ("#bg-canvas" if r["overCanvas"] else
                ("cover" if r["overCover"] else "opaque paint"))
        print("  %-16s %-30s %6.2f need %.1f %-4s %5.1fpx on %-12s ink %s -> %s"
              % (k, r["sel"][:30], r["worst"], r["need"], "FAIL" if bad else "pass",
                 r["fpx"], surf, str(r["ink"]), str(r["backdrop"])))
    print("sites below floor: %d of %d measured" % (fails, len(by)))
    if misses:
        print("\nNOT MEASURED (unverified by this instrument)")
        for m in sorted(set(misses)):
            print("  %-16s %-30s %-24s %s" % m)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "scan":
        scan(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    else:
        th, w, h, n, tag = (sys.argv[2], int(sys.argv[3]), int(sys.argv[4]),
                            int(sys.argv[5]), sys.argv[6])
        st = sys.argv[7].split(",") if len(sys.argv) > 7 else ORDER
        run(th, w, h, n, tag, st)
