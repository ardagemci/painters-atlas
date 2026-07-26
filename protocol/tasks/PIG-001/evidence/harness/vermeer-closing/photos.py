"""AC19 / F-5 — text painted over upload.wikimedia.org photographs, measured on
real rendered glyph pixels.

Van Eyck's F-5: nobody ever measured this composite class; his worst-case bound
put `.mu-sub` at 2.44:1 against a 4.5 floor across 116 venue photographs.

Cross-origin caveat and the way round it: `canvas.getImageData()` throws on a
canvas tainted by `upload.wikimedia.org`, which is why round 2 recorded this as
NOT TESTED. This harness never touches getImageData. It uses Vermeer's r2 /
Durer u26 two-shot technique instead: CDP captures the composited pixels as a
PNG that *we* then decode locally, so the same-origin policy never applies.

  shot A - page as rendered
  shot B - the candidate text elements set to visibility:hidden
  a pixel counts as a glyph pixel only where A and B differ strongly
  ink     = the element's declared paint (gradient stops if background-clip:text)
  backdrop= that same pixel in B, i.e. the photograph as actually composited
            through every scrim above it

Detection is deliberately an over-approximation: ANY visible text-bearing element
whose rect intersects the rect of an <img> whose src is on upload.wikimedia.org.
Over-selection is harmless (the measured backdrop is then simply the opaque panel
above the photo); under-selection would not be, so the net is cast wide.

usage: python3 photos.py <mode> [args]
  routes  <route,route,...>     - discovery: what composites exist on these routes
  museums <N> [theme] [w] [h]   - measure N museum pages (0 = all), one theme
"""
import json, os, sys, time

H = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, H)
import cdp, png

OUT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("CDP_PORT", "9333"))
A_PNG, B_PNG = "/tmp/vermeer-photo-a.png", "/tmp/vermeer-photo-b.png"
THRESH = 60

DETECT = r"""(function(){
 var imgs=[].slice.call(document.images).filter(function(i){
   return /upload\.wikimedia\.org/.test(i.currentSrc||i.src||'');})
  .map(function(i){var r=i.getBoundingClientRect();
   return {r:[r.left,r.top,r.right,r.bottom],src:(i.currentSrc||i.src),
           nat:[i.naturalWidth,i.naturalHeight],complete:i.complete};})
  .filter(function(o){return o.r[2]>o.r[0]&&o.r[3]>o.r[1];});
 var els=[];
 if(imgs.length){
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
   var hit=null;
   for(var k=0;k<imgs.length;k++){var q=imgs[k].r;
    if(r.left<q[2]&&r.right>q[0]&&r.top<q[3]&&r.bottom>q[1]){hit=imgs[k];break;}}
   if(!hit)return;
   var fpx=parseFloat(cs.fontSize),wt=parseInt(cs.fontWeight,10)||400;
   var inks=[],clip=cs.webkitBackgroundClip||cs.backgroundClip||'';
   if(clip==='text'){var m=cs.backgroundImage.match(/rgba?\([^)]+\)/g)||[];
    inks=m.map(function(s){var p=s.match(/[\d.]+/g);return [+p[0],+p[1],+p[2]];});}
   if(!inks.length){var p=cs.color.match(/[\d.]+/g);inks=[[+p[0],+p[1],+p[2]]];}
   var path=[],n=el;
   while(n&&n!==document.body){path.unshift(n.tagName.toLowerCase()+
     (n.classList.length?'.'+[].slice.call(n.classList).join('.'):''));n=n.parentElement;}
   els.push({sel:el.tagName.toLowerCase()+(el.classList.length?'.'+[].slice.call(el.classList).join('.'):''),
    path:path.slice(-3).join(' > '),
    text:txt.trim().replace(/\s+/g,' ').slice(0,40),
    rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
    fpx:fpx,weight:wt,large:(fpx>=24||(fpx>=18.66&&wt>=700)),inks:inks,clip:clip,
    overSrc:hit.src.split('/').pop().slice(0,60),
    textShadow:cs.textShadow});});}
 return JSON.stringify({url:location.hash,imgs:imgs.length,
   imgSrcs:imgs.map(function(o){return o.src.split('/').pop().slice(0,60);}).slice(0,8),
   els:els});})()"""

HIDE = r"""(function(){
 /* Shot B must remove the GLYPHS ONLY, never the element's own background:
    visibility:hidden would also delete a pill or panel that is genuinely part
    of the composite, and would then report the raw photograph as the backdrop.
    Making the text transparent leaves every painted layer except the ink. */
 var n=0;
 [].forEach.call(document.querySelectorAll('*'),function(el){
  var txt='';for(var j=0;j<el.childNodes.length;j++){var cn=el.childNodes[j];
   if(cn.nodeType===3)txt+=cn.nodeValue;}
  if(!txt.trim())return;
  var r=el.getBoundingClientRect();
  if(r.width<2||r.height<2)return;
  el.style.setProperty('color','transparent','important');
  el.style.setProperty('-webkit-text-fill-color','transparent','important');
  el.style.setProperty('text-shadow','none','important');
  el.style.setProperty('text-decoration-color','transparent','important');
  n++;});
 return n;})()"""


SETTLE = """(function(){var im=[].slice.call(document.images);
 return JSON.stringify({n:im.length,
  pending:im.filter(function(i){return !i.complete;}).length,
  h:document.body.scrollHeight});})()"""


def wait_settled(b, tries=30):
    """Lazy <img> loads reflow the page AFTER first paint, which silently
    invalidates any rect captured before them - that is how a stats row that
    renders light-on-light came back reading 2.37:1 against a dark backdrop in
    an earlier run of this harness. Wait until no image is pending and the
    document height has stopped moving, then require two identical consecutive
    detections before any rect is trusted."""
    last = None
    for _ in range(tries):
        st = json.loads(b.ev(SETTLE))
        if st["pending"] == 0 and last == st["h"]:
            return st
        last = st["h"]
        b.ev("new Promise(function(r){setTimeout(r,220)})", await_promise=True)
    return json.loads(b.ev(SETTLE))


def detect_stable(b, tries=6):
    """Return a detection whose rects reproduce exactly on a second read."""
    prev = None
    for _ in range(tries):
        d = json.loads(b.ev(DETECT))
        key = [(e["sel"], tuple(e["rect"])) for e in d["els"]]
        if prev is not None and key == prev:
            d["stable"] = True
            return d
        prev = key
        b.ev("new Promise(function(r){setTimeout(r,260)})", await_promise=True)
    d["stable"] = False
    return d


def clip_shot(b, path, box):
    x, y, w, h = box
    r = b.cmd("Page.captureScreenshot",
              {"format": "png", "captureBeyondViewport": False,
               "clip": {"x": x, "y": y, "width": w, "height": h, "scale": 1}})
    import base64
    open(path, "wb").write(base64.b64decode(r["data"]))


def measure_page(b, els, vw, vh):
    """Two-shot glyph diff over the union box of the candidate elements."""
    xs0 = max(0, min(e["rect"][0] for e in els))
    ys0 = max(0, min(e["rect"][1] for e in els))
    xs1 = min(vw, max(e["rect"][0] + e["rect"][2] for e in els))
    ys1 = min(vh, max(e["rect"][1] + e["rect"][3] for e in els))
    box = (xs0, ys0, max(1, xs1 - xs0), max(1, ys1 - ys0))
    clip_shot(b, A_PNG, box)
    b.ev(HIDE)
    b.ev("new Promise(function(r){setTimeout(r,220)})", await_promise=True)
    clip_shot(b, B_PNG, box)
    A, B = png.Img(A_PNG), png.Img(B_PNG)
    res = []
    for e in els:
        x, y, w, h = e["rect"]
        x0, y0 = max(0, x) - box[0], max(0, y) - box[1]
        x1, y1 = min(vw, x + w) - box[0], min(vh, y + h) - box[1]
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(A.w, B.w, x1), min(A.h, B.h, y1)
        lo, lopx, ng = None, None, 0
        bandlo, bandpx = None, None
        for py in range(y0, y1):
            for px_ in range(x0, x1):
                bb = B.px(px_, py)
                for ink in e["inks"]:                    # band bound: whole rect
                    r_ = png.ratio(tuple(ink), bb)
                    if bandlo is None or r_ < bandlo:
                        bandlo, bandpx = r_, (tuple(ink), bb)
                a = A.px(px_, py)
                if abs(a[0]-bb[0]) + abs(a[1]-bb[1]) + abs(a[2]-bb[2]) < THRESH:
                    continue
                ng += 1
                for ink in e["inks"]:                    # real measurement: glyphs
                    r_ = png.ratio(tuple(ink), bb)
                    if lo is None or r_ < lo:
                        lo, lopx = r_, (tuple(ink), bb)
        res.append({"sel": e["sel"], "path": e["path"], "text": e["text"],
                    "fpx": e["fpx"], "large": e["large"], "need": 3.0 if e["large"] else 4.5,
                    "glyphPx": ng,
                    "glyphWorst": None if lo is None else round(lo, 2),
                    "glyphInk": None if lo is None else list(lopx[0]),
                    "glyphBackdrop": None if lo is None else list(lopx[1]),
                    "bandWorst": None if bandlo is None else round(bandlo, 2),
                    "bandBackdrop": None if bandlo is None else list(bandpx[1]),
                    "overSrc": e["overSrc"], "textShadow": e["textShadow"]})
    return res


def venue_ids(b):
    b.goto(cdp.BASE + "/index.html#/museums", settle=2.0)
    ids = json.loads(b.ev(
        "JSON.stringify([].slice.call(document.querySelectorAll('a[href^=\"#/museum/\"]'))"
        ".map(function(a){return a.getAttribute('href').split('/').pop();}))"))
    seen, out = set(), []
    for i in ids:
        if i not in seen:
            seen.add(i); out.append(i)
    return out


def run_routes(routes, theme="dark", vw=1440, vh=900):
    b = cdp.Browser(port=PORT)
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.metrics(vw, vh)
        for r in routes:
            b.goto("%s/index.html?vc=%d%s" % (cdp.BASE, int(time.time() * 1000) % 99999, r), settle=2.2)
            d = json.loads(b.ev(DETECT))
            print("\n%-28s imgs=%d  candidates=%d" % (r, d["imgs"], len(d["els"])))
            for e in d["els"]:
                print("   %-34s %5.1fpx %-5s  %s" % (e["sel"], e["fpx"],
                      "LARGE" if e["large"] else "body", e["text"][:34]))
    finally:
        b.close()


def run_museums(n, theme="dark", vw=1440, vh=900, tag=None):
    b = cdp.Browser(port=PORT)
    rows, pages = [], []
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.metrics(vw, vh)
        ids = venue_ids(b)
        if n:
            ids = ids[:n]
        print("venues to measure: %d (theme=%s %dx%d)" % (len(ids), theme, vw, vh), flush=True)
        for k, vid in enumerate(ids):
            b.goto("%s/index.html?vc=%d#/museum/%s" % (cdp.BASE, k, vid), settle=1.9)
            assert b.ev("document.documentElement.dataset.theme") == theme
            assert b.ev("window.innerWidth") == vw, b.ev("window.innerWidth")
            wait_settled(b)
            d = detect_stable(b)
            if not d["els"]:
                pages.append({"venue": vid, "imgs": d["imgs"], "els": 0,
                              "note": "no text over a wikimedia image"})
                print("%3d %-26s imgs=%d  no composite" % (k, vid, d["imgs"]), flush=True)
                continue
            res = measure_page(b, d["els"], vw, vh)
            for r in res:
                r["venue"] = vid; r["theme"] = theme; r["layoutStable"] = d.get("stable")
                rows.append(r)
            pages.append({"venue": vid, "imgs": d["imgs"], "els": len(res),
                          "layoutStable": d.get("stable"),
                          "heroKind": "collage" if any("collage" in (e["path"] or "") for e in d["els"])
                                      else "photo"})
            w = min([r["glyphWorst"] for r in res if r["glyphWorst"] is not None] or [99])
            print("%3d %-26s imgs=%-2d els=%-2d worst=%.2f" % (k, vid, d["imgs"], len(res), w),
                  flush=True)
    finally:
        b.close()
    name = tag or ("museums-%s-%dx%d" % (theme, vw, vh))
    json.dump({"theme": theme, "viewport": [vw, vh], "pages": pages, "rows": rows},
              open(os.path.join(OUT, "photo-%s.json" % name), "w"), indent=1)
    summarise(rows)
    return rows


def summarise(rows):
    by = {}
    for r in rows:
        if r["glyphWorst"] is None:
            continue
        k = r["sel"]
        if k not in by or r["glyphWorst"] < by[k]["glyphWorst"]:
            by[k] = r
    print("\nWORST OBSERVED GLYPH CONTRAST PER ELEMENT CLASS")
    for k, r in sorted(by.items(), key=lambda kv: kv[1]["glyphWorst"]):
        print("  %-30s %6.2f  need %.1f  %-4s  %-22s ink %-16s backdrop %-16s (%d glyph px)"
              % (k, r["glyphWorst"], r["need"],
                 "PASS" if r["glyphWorst"] >= r["need"] else "FAIL",
                 r["venue"], str(r["glyphInk"]), str(r["glyphBackdrop"]), r["glyphPx"]))


def run_pages(routes, theme="dark", vw=1440, vh=900, tag=None):
    """Measure the composites on an arbitrary list of routes (non-museum surfaces)."""
    b = cdp.Browser(port=PORT)
    rows = []
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.metrics(vw, vh)
        for k, r in enumerate(routes):
            b.goto("%s/index.html?vp=%d%s" % (cdp.BASE, k, r), settle=2.4)
            assert b.ev("document.documentElement.dataset.theme") == theme
            assert b.ev("window.innerWidth") == vw
            wait_settled(b)
            d = detect_stable(b)
            if not d["els"]:
                print("%-26s imgs=%d  no composite" % (r, d["imgs"]), flush=True)
                continue
            res = measure_page(b, d["els"], vw, vh)
            for x in res:
                x["venue"] = r; x["theme"] = theme
                rows.append(x)
            w = min([x["glyphWorst"] for x in res if x["glyphWorst"] is not None] or [99])
            print("%-26s imgs=%-3d els=%-2d worst=%.2f" % (r, d["imgs"], len(res), w), flush=True)
    finally:
        b.close()
    json.dump({"theme": theme, "viewport": [vw, vh], "rows": rows},
              open(os.path.join(OUT, "photo-%s.json" % (tag or "pages")), "w"), indent=1)
    summarise(rows)
    return rows


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "routes":
        run_routes(sys.argv[2].split(","), *(sys.argv[3:4] or ["dark"]))
    elif mode == "pages":
        run_pages(sys.argv[2].split(","),
                  sys.argv[3] if len(sys.argv) > 3 else "dark",
                  1440, 900, sys.argv[4] if len(sys.argv) > 4 else None)
    elif mode == "museums":
        run_museums(int(sys.argv[2]),
                    sys.argv[3] if len(sys.argv) > 3 else "dark",
                    int(sys.argv[4]) if len(sys.argv) > 4 else 1440,
                    int(sys.argv[5]) if len(sys.argv) > 5 else 900,
                    sys.argv[6] if len(sys.argv) > 6 else None)
