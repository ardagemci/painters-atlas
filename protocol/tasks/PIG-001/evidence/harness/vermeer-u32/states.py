"""AC19 — HOVER and FOCUS ink, measured. Vermeer, unit 32.

Every sweep this build owns measures the page AT REST. But an ink that only
exists in a state is still an ink: unit 29 found light `a:hover{color:#fff}`
reading 1.07 against the canvas, and it found it by reading the stylesheet, not
by hovering anything. This instrument hovers and focuses real controls and
measures what is actually painted.

Method:
  1. enumerate every interactive element in the viewport (a, button, input,
     summary, [tabindex], [role=button]);
  2. record every descendant's computed ink AT REST;
  3. put the element into the state — a real CDP mouseMoved for :hover, and
     CDP forcePseudoState for :hover/:focus/:focus-visible/:active, which is how
     the engine itself is asked rather than simulated;
  4. re-read the inks. Only elements whose ink ACTUALLY CHANGED are measured —
     the rest are already covered by the at-rest census and re-measuring them
     would just inflate the row count;
  5. measure the changed ones with the same four-shot paint differential
     (A / ink transparent / no #bg-canvas / no covers).

Not covered here, and stated rather than implied: the focus RING is a non-text
contrast item (WCAG 1.4.11) and a glyph differential cannot see it — the ring is
not a glyph. Ring contrast was measured by unit 30 on `.hero`; elsewhere it is
NOT TESTED by this instrument.

usage: python3 states.py <theme> <w> <h> <tag> [route,route,...]
"""
import base64, json, os, sys, time

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp                                    # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pngfast as png                         # noqa: E402
import triple                                 # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
PID = os.getpid()
SHOT = {k: "/tmp/v32st-%s-%d.png" % (k, PID) for k in "ABCD"}
THRESH = 60

TARGETS = ("a[href], button, input, summary, [tabindex], [role=button], "
           ".chip, .card, .f-btn, .tone")

ENUM = r"""(function(sel){
 var out=[];
 [].forEach.call(document.querySelectorAll(sel),function(el,i){
  var cs=getComputedStyle(el);
  if(cs.display==='none'||cs.visibility==='hidden')return;
  var r=el.getBoundingClientRect();
  if(r.width<6||r.height<6)return;
  if(r.top<0||r.bottom>window.innerHeight||r.left<0||r.right>window.innerWidth)return;
  out.push({i:i,rect:[Math.round(r.left),Math.round(r.top),
                      Math.round(r.width),Math.round(r.height)],
            sel:el.tagName.toLowerCase()+
              (el.classList&&el.classList.length?'.'+[].slice.call(el.classList).join('.'):'')});});
 return JSON.stringify(out);})(%s)"""

# every text-owning node inside one control, with its ink — used twice, at rest
# and in state, and only the DIFFERENCE is measured.
INKS = r"""(function(sel,i){
 var host=document.querySelectorAll(sel)[i]; if(!host)return "[]";
 var out=[];
 function rgb(s){var m=s&&s.match(/[\d.]+/g);
   return m&&m.length>=3?[Math.round(+m[0]),Math.round(+m[1]),Math.round(+m[2])]:null;}
 var all=[host].concat([].slice.call(host.querySelectorAll('*')));
 all.forEach(function(el,k){
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
  var tg=el.tagName.toLowerCase();
  var isSvgText=svg&&(tg==='text'||tg==='tspan');
  if(svg&&!isSvgText)return;
  var ink=(isSvgText&&cs.fill&&cs.fill!=='none')?rgb(cs.fill):rgb(cs.color);
  if(!ink)return;
  var fpx=parseFloat(cs.fontSize),wt=parseInt(cs.fontWeight,10)||400;
  out.push({k:k,ink:ink,fpx:fpx,weight:wt,
            large:(fpx>=24||(fpx>=18.66&&wt>=700)),
            deco:cs.textDecorationLine+'|'+cs.textDecorationColor,
            sel:tg+(el.classList&&el.classList.length?'.'+[].slice.call(el.classList).join('.'):''),
            text:txt.trim().replace(/\s+/g,' ').slice(0,26),
            rect:[Math.round(r.left),Math.round(r.top),
                  Math.round(r.width),Math.round(r.height)]});});
 return JSON.stringify(out);})(%s,%d)"""

HIDE_ONE = r"""(function(sel,i,ks){
 var host=document.querySelectorAll(sel)[i]; if(!host)return false;
 var all=[host].concat([].slice.call(host.querySelectorAll('*')));
 ks.forEach(function(k){var el=all[k]; if(!el)return;
  el.style.setProperty('color','transparent','important');
  el.style.setProperty('-webkit-text-fill-color','transparent','important');
  el.style.setProperty('fill','transparent','important');
  el.style.setProperty('text-shadow','none','important');
  el.style.setProperty('text-decoration-color','transparent','important');});
 return true;})(%s,%d,%s)"""

UNHIDE = r"""(function(){[].forEach.call(document.querySelectorAll('[style]'),function(el){
  if(!el.style.getPropertyValue('-webkit-text-fill-color'))return;
  ['color','-webkit-text-fill-color','fill','text-shadow','text-decoration-color']
   .forEach(function(p){el.style.removeProperty(p);});});return true;})()"""


def shot(b, path, box, sx, sy):
    x, y, w, h = box
    r = b.cmd("Page.captureScreenshot",
              {"format": "png", "captureBeyondViewport": False,
               "clip": {"x": x + sx, "y": y + sy, "width": w, "height": h, "scale": 1}})
    open(path, "wb").write(base64.b64decode(r["data"]))


def js(s):
    return json.dumps(s)


def measure_one(b, sel, i, els, vw, vh):
    sx = int(b.ev("Math.round(window.scrollX)") or 0)
    sy = int(b.ev("Math.round(window.scrollY)") or 0)
    xs0 = max(0, min(e["rect"][0] for e in els))
    ys0 = max(0, min(e["rect"][1] for e in els))
    xs1 = min(vw, max(e["rect"][0] + e["rect"][2] for e in els))
    ys1 = min(vh, max(e["rect"][1] + e["rect"][3] for e in els))
    box = (xs0, ys0, max(1, xs1 - xs0), max(1, ys1 - ys0))
    ks = [e["k"] for e in els]
    shot(b, SHOT["A"], box, sx, sy)
    assert b.ev(HIDE_ONE % (js(sel), i, json.dumps(ks))) is True
    b.ev("new Promise(function(r){setTimeout(r,180)})", await_promise=True)
    shot(b, SHOT["B"], box, sx, sy)
    b.ev(triple.KILL_CANVAS)
    b.ev("new Promise(function(r){setTimeout(r,180)})", await_promise=True)
    shot(b, SHOT["C"], box, sx, sy)
    b.ev(triple.UNKILL_CANVAS)
    b.ev(triple.KILL_COVERS)
    b.ev("new Promise(function(r){setTimeout(r,180)})", await_promise=True)
    shot(b, SHOT["D"], box, sx, sy)
    assert int(b.ev("Math.round(window.scrollY)") or 0) == sy, "page scrolled mid-capture"
    b.ev(triple.UNKILL_COVERS)
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
                cd = max(cd, max(abs(bb[j]-cc[j]) for j in range(3)))
                vd = max(vd, max(abs(bb[j]-dd[j]) for j in range(3)))
                r_ = png.ratio(ink, bb)
                if lo is None or r_ < lo:
                    lo, lopx, nod = r_, bb, cc
        if lo is None:
            continue
        res.append({"sel": e["sel"], "host": sel, "text": e["text"],
                    "fpx": e["fpx"], "weight": e["weight"], "large": e["large"],
                    "need": 3.0 if e["large"] else 4.5, "glyphPx": ng,
                    "worst": round(lo, 2), "ink": list(ink),
                    "backdrop": list(lopx), "backdropNoCanvas": list(nod),
                    "canvasDelta": cd, "coverDelta": vd,
                    "overCanvas": cd > 0, "overCover": vd > 0})
    return res


def force(b, i, sel, classes):
    """Ask the ENGINE for the state rather than simulating it."""
    doc = b.cmd("DOM.getDocument", {"depth": 0})["root"]["nodeId"]
    ids = b.cmd("DOM.querySelectorAll", {"nodeId": doc, "selector": sel})["nodeIds"]
    if i >= len(ids):
        return None
    b.cmd("CSS.forcePseudoState", {"nodeId": ids[i], "forcedPseudoClasses": classes})
    return ids[i]


def run(theme, vw, vh, tag, routes):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9448")))
    rows, notes = [], []
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s');"
                         "localStorage.setItem('pigment.taste.v1',%s)}catch(e){}"
                         % (theme, json.dumps(triple.SEED_PASSPORT))})
        b.cmd("Emulation.setEmulatedMedia",
              {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        b.cmd("DOM.enable")
        b.cmd("CSS.enable")
        b.metrics(vw, vh)
        cap = int(os.environ.get("V32_STATE_CAP", "26"))
        for rt in routes:
            b.goto("%s/index.html?v32st=%d%s" % (cdp.BASE, PID, rt), settle=1.8)
            assert b.ev("document.documentElement.dataset.theme") == theme
            triple.wait_settled(b)
            ctrls = json.loads(b.ev(ENUM % js(TARGETS)))
            changed = 0
            for c in ctrls[:cap]:
                i = c["i"]
                rest = json.loads(b.ev(INKS % (js(TARGETS), i)))
                if not rest:
                    continue
                nid = force(b, i, TARGETS, ["hover", "focus", "focus-visible"])
                if nid is None:
                    continue
                b.ev("new Promise(function(r){setTimeout(r,260)})", await_promise=True)
                now = json.loads(b.ev(INKS % (js(TARGETS), i)))
                byk = {e["k"]: e for e in rest}
                diff = [e for e in now
                        if e["k"] not in byk
                        or byk[e["k"]]["ink"] != e["ink"]
                        or byk[e["k"]]["deco"] != e["deco"]]
                if diff:
                    changed += 1
                    for x in measure_one(b, TARGETS, i, diff, vw, vh):
                        x.update({"route": rt, "theme": theme, "vw": vw, "vh": vh,
                                  "state": "hover+focus-visible",
                                  "control": c["sel"],
                                  "restInk": [byk[e["k"]]["ink"] for e in diff
                                              if e["k"] in byk][:1]})
                        rows.append(x)
                b.cmd("CSS.forcePseudoState", {"nodeId": nid, "forcedPseudoClasses": []})
            bad = [r for r in rows if r["route"] == rt and r["worst"] < r["need"]]
            print("%-30s controls=%-3d ink-changing=%-3d measured=%-3d FAIL=%d"
                  % (rt, len(ctrls), changed,
                     len([r for r in rows if r["route"] == rt]), len(bad)), flush=True)
    finally:
        b.close()
    json.dump({"theme": theme, "viewport": [vw, vh], "rows": rows, "notes": notes},
              open(os.path.join(OUT, "state-%s.json" % tag), "w"))
    fails = [r for r in rows if r["worst"] < r["need"]]
    print("\nHOVER/FOCUS INK — %s %dx%d: %d measured, %d below floor"
          % (theme, vw, vh, len(rows), len(fails)))
    for r in sorted(fails, key=lambda r: r["worst"]):
        print("  FAIL %5.2f need %.1f  %-24s in %-22s %-18s ink %s -> %s"
              % (r["worst"], r["need"], r["sel"][:24], r["route"][:22],
                 r["text"][:18], str(r["ink"]), str(r["backdrop"])))


if __name__ == "__main__":
    th, w, h, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rt = sys.argv[5].split(",") if len(sys.argv) > 5 else triple.ROUTES
    run(th, w, h, tag, rt)
