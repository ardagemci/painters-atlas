"""Vermeer, final pass — Dürer's two incidental unit-29 finds, measured directly.

He reports `.daily-detail b` was 2.57 in light and light `a:hover` was 1.07 (dark's
`a:hover{color:#fff}` painting white on warm paper). Both are claimed fixed at HEAD.
Neither is reachable through `canvastext.py`, which never hovers anything, so this is
a separate instrument.

Method is the two-shot glyph diff this project already uses (`vermeer-closing/photos.py`):
  A  the page as rendered, WITH a real CDP mouse hovering the link under test
  B  the same page, same hover, glyphs made transparent (never `visibility:hidden`)
A pixel counts only where A and B differ; its backdrop is that pixel in B, i.e. the
generative `#bg-canvas` as actually composited. `prefers-reduced-motion:reduce` is
emulated so the canvas paints one static frame and holds it across both shots.

The hover is a real `Input.dispatchMouseEvent`, and the run ASSERTS that
`getComputedStyle(el).color` actually changed under the pointer before it measures —
a hover that did not take would otherwise be silently measured as the resting colour.

The canvas is Math.random-seeded, so every route is loaded `--draws` times behind a
unique query string and the WORST value over all draws is reported.

usage: python3 incidental.py <theme> <w> <h> <draws> <tag>
"""
import json, os, sys, time

V = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/vermeer-closing"
C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, V)
sys.path.insert(0, C)
import cdp, png, photos

OUT = os.path.dirname(os.path.abspath(__file__))
photos.A_PNG = "/tmp/vf-inc-a-%d.png" % os.getpid()
photos.B_PNG = "/tmp/vf-inc-b-%d.png" % os.getpid()

# (route, css selector, what it is). Links are hovered; non-links are measured at rest.
TARGETS = [
    ("#/daily", ".daily-detail b", "hover:no"),
    ("#/daily", ".daily-copy p a", "hover:yes"),
    ("#/credits", "main a", "hover:yes"),
    ("#/museum/louvre", ".breadcrumbs a", "hover:yes"),
    ("#/artist/leonardo-da-vinci", ".breadcrumbs a", "hover:yes"),
    ("#/lists", ".card-body h3 a", "hover:yes"),
    ("#/artists", ".main-nav a", "hover:yes"),
    ("#/privacy", "main a", "hover:yes"),
    ("#/", ".footer-nav a", "hover:yes"),
]

PICK = r"""(function(sel){
 var out=[];
 [].forEach.call(document.querySelectorAll(sel),function(el){
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
  var p=cs.color.match(/[\d.]+/g);
  var path=[],n=el;
  while(n&&n!==document.body){path.unshift(n.tagName.toLowerCase()+
    (n.classList.length?'.'+[].slice.call(n.classList).join('.'):''));n=n.parentElement;}
  out.push({sel:el.tagName.toLowerCase()+(el.classList.length?'.'+[].slice.call(el.classList).join('.'):''),
   path:path.slice(-3).join(' > '),
   text:txt.trim().replace(/\s+/g,' ').slice(0,40),
   rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
   fpx:fpx,weight:wt,large:(fpx>=24||(fpx>=18.66&&wt>=700)),
   inks:[[+p[0],+p[1],+p[2]]],clip:'',overSrc:null,textShadow:cs.textShadow,
   cx:Math.round(r.left+r.width/2),cy:Math.round(r.top+r.height/2)});});
 return JSON.stringify(out.slice(0,6));})(%s)"""

COLOR_AT = r"""(function(sel,i){
 var els=[].slice.call(document.querySelectorAll(sel));
 var el=els.filter(function(e){var r=e.getBoundingClientRect();
   return r.width>2&&r.height>2&&r.top>=0&&r.bottom<=window.innerHeight;})[i];
 return el?getComputedStyle(el).color:null;})(%s,%d)"""


def boot(theme, vw, vh):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9411")))
    b.cmd("Page.addScriptToEvaluateOnNewDocument",
          {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
    b.cmd("Emulation.setEmulatedMedia",
          {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
    b.metrics(vw, vh)
    return b


def hover(b, x, y):
    for t in ("mouseMoved",):
        b.cmd("Input.dispatchMouseEvent",
              {"type": t, "x": x, "y": y, "button": "none", "clickCount": 0})
    b.ev("new Promise(function(r){setTimeout(r,300)})", await_promise=True)


def run(theme, vw, vh, draws, tag):
    b = boot(theme, vw, vh)
    rows, k = [], 0
    try:
        for d in range(draws):
            for (route, sel, mode) in TARGETS:
                k += 1
                b.goto("%s/index.html?vfi=%d%s" % (cdp.BASE, k, route), settle=1.9)
                assert b.ev("document.documentElement.dataset.theme") == theme, "theme"
                assert b.ev("window.innerWidth") == vw, "innerWidth"
                assert b.ev("!!document.getElementById('bg-canvas')") in (True, "true"), "no canvas"
                photos.wait_settled(b)
                els = json.loads(b.ev(PICK % json.dumps(sel)))
                if not els:
                    print("   -- %-28s %-22s no element in viewport" % (route, sel), flush=True)
                    continue
                e = els[0]
                rest = e["inks"][0]
                if mode == "hover:yes":
                    hover(b, e["cx"], e["cy"])
                    now = b.ev(COLOR_AT % (json.dumps(sel), 0))
                    p = [int(float(v)) for v in
                         __import__("re").findall(r"[\d.]+", now or "0,0,0")][:3]
                    if p == rest:
                        print("   !! %-26s %-22s hover did NOT change colour (%s) — "
                              "NOT a measurement of :hover" % (route, sel, now), flush=True)
                        hovered = False
                    else:
                        hovered = True
                    e["inks"] = [p]
                    e["hoverColor"] = now
                else:
                    hovered = None
                e["restColor"] = rest
                res = photos.measure_page(b, [e], vw, vh)
                for r in res:
                    r.update({"route": route, "cssSel": sel, "draw": d, "theme": theme,
                              "viewport": [vw, vh], "hovered": hovered,
                              "restInk": rest, "usedInk": e["inks"][0]})
                    rows.append(r)
                    print("  d%d %-28s %-22s %-6s worst=%s ink=%s bg=%s (%s px)"
                          % (d, route, sel, "HOVER" if hovered else "rest",
                             r["glyphWorst"], r["glyphInk"], r["glyphBackdrop"],
                             r["glyphPx"]), flush=True)
    finally:
        try:
            b.close()
        except Exception:
            pass
    json.dump({"theme": theme, "viewport": [vw, vh], "draws": draws, "rows": rows},
              open(os.path.join(OUT, "incidental-%s.json" % tag), "w"), indent=1)
    print("\nWORST PER (route, selector)  [%s]" % tag)
    by = {}
    for r in rows:
        if r["glyphWorst"] is None:
            continue
        key = (r["route"], r["cssSel"])
        if key not in by or r["glyphWorst"] < by[key]["glyphWorst"]:
            by[key] = r
    bad = 0
    for key, r in sorted(by.items(), key=lambda kv: kv[1]["glyphWorst"]):
        ok = r["glyphWorst"] >= r["need"]
        bad += 0 if ok else 1
        print("  %-30s %-22s %6.2f need %.1f %-4s ink %-16s bg %-16s hovered=%s"
              % (key[0], key[1], r["glyphWorst"], r["need"], "PASS" if ok else "FAIL",
                 str(r["glyphInk"]), str(r["glyphBackdrop"]), r["hovered"]))
    print("cells below floor: %d of %d" % (bad, len(by)))


if __name__ == "__main__":
    run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
