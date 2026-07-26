"""Unit-26b: mobile header composition at 390, and the 200% text-zoom
containment sweep that must not regress.

usage: python3 nav.py <tag>
"""
import json, sys, os
H = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, H)
import cdp

TAG = sys.argv[1] if len(sys.argv) > 1 else "run"

NAV = r"""(function(){
 var hd=document.querySelector('.site-header'), nv=document.querySelector('.main-nav');
 var hr=hd.getBoundingClientRect(), nr=nv.getBoundingClientRect();
 var cs=getComputedStyle(nv);
 var links=[].map.call(nv.querySelectorAll('a'),function(a){var r=a.getBoundingClientRect();
  return {t:a.textContent.trim(), top:Math.round(r.top), left:Math.round(r.left),
   w:Math.round(r.width), h:Math.round(r.height),
   inside:(r.left>=nr.left-1&&r.right<=nr.right+1)};});
 var rows={}; links.forEach(function(l){rows[l.top]=1;});
 return JSON.stringify({
  headerH:Math.round(hr.height), viewportH:innerHeight, viewportW:innerWidth,
  navBox:[Math.round(nr.width),Math.round(nr.height)],
  navScrollW:nv.scrollWidth, navClientW:nv.clientWidth,
  wrap:cs.flexWrap, basis:cs.flexBasis, grow:cs.flexGrow, order:cs.order,
  overflowX:cs.overflowX, mask:(cs.webkitMaskImage||cs.maskImage||'none').slice(0,60),
  navRows:Object.keys(rows).length, linkCount:links.length,
  linksInside:links.filter(function(l){return l.inside;}).length,
  docSW:document.documentElement.scrollWidth, docCW:document.documentElement.clientWidth,
  links:links});})()"""

ZOOM = ("document.documentElement.style.setProperty('font-size','32px','important');1")
OVER = ("JSON.stringify({sw:document.documentElement.scrollWidth,"
        "cw:document.documentElement.clientWidth,"
        "bsw:document.body.scrollWidth,"
        "nav:(function(){var r=document.querySelector('.main-nav').getBoundingClientRect();"
        "return [Math.round(r.width),Math.round(r.height),Math.round(r.right)];})(),"
        "fs:getComputedStyle(document.documentElement).fontSize})")

ROUTES = ["#/", "#/artists", "#/artist/leonardo-da-vinci", "#/artwork/david", "#/explore",
          "#/timeline", "#/influences", "#/museums", "#/museum/louvre", "#/lists",
          "#/list/" , "#/palette", "#/taste", "#/daily", "#/privacy", "#/credits",
          "#/movements", "#/techniques", "#/eras", "#/nations", "#/no-such-page",
          "#/passport", "#/movement/impressionism", "#/technique/oil-on-canvas",
          "#/era/renaissance", "#/nation/france"]

out = {}
b = cdp.Browser()
try:
    # --- A: 390 mobile header composition, both themes
    b.metrics(390, 844)
    for theme in ("dark", "light"):
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.goto("%s/index.html?n26=%s#/" % (cdp.BASE, theme), settle=1.8)
        d = json.loads(b.ev(NAV))
        out["mobile390-" + theme] = d
        print("== 390", theme, "headerH=%d/%d navBox=%s rows=%d wrap=%s basis=%s sw/cw=%d/%d ovX=%s"
              % (d["headerH"], d["viewportH"], d["navBox"], d["navRows"], d["wrap"],
                 d["basis"], d["docSW"], d["docCW"], d["overflowX"]), flush=True)
        print("   navScrollW=%d navClientW=%d linksInside=%d/%d mask=%s"
              % (d["navScrollW"], d["navClientW"], d["linksInside"], d["linkCount"], d["mask"]))

    # --- B: 200% text zoom at 1280 and 1270, every route
    for W in (1280, 1270):
        b.metrics(W, 800)
        bad, rows = [], []
        for r in ROUTES:
            rr = r if r != "#/list/" else "#/lists"
            b.goto("%s/index.html?z26=%d%s%s" % (cdp.BASE, W, rr.replace("#", "&h="), rr),
                   settle=1.0)
            b.ev(ZOOM); b.ev("new Promise(function(x){setTimeout(x,320)})", await_promise=True)
            b.ev(ZOOM); b.ev("new Promise(function(x){setTimeout(x,320)})", await_promise=True)
            d = json.loads(b.ev(OVER))
            over = d["sw"] - d["cw"]
            rows.append({"route": rr, "over": over, "sw": d["sw"], "cw": d["cw"],
                         "nav": d["nav"], "fs": d["fs"]})
            if over > 0:
                bad.append((rr, over))
        out["zoom200-%d" % W] = rows
        print("== 200%% zoom @%d : %d routes, %d overflowing %s  nav=%s fs=%s"
              % (W, len(rows), len(bad), bad, rows[0]["nav"], rows[0]["fs"]), flush=True)
finally:
    b.close()

json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "nav-%s.json" % TAG), "w"), indent=1)
