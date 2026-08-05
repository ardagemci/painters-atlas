"""PIG-001 certification — the `.md-name` residual, and the live region. Vermeer.

TWO QUESTIONS, both bounded by what a DOM/pixel instrument can actually answer.

1. `.md-name` LEGIBILITY (not contrast — unit 33 closed the contrast at 4.5+).
   Unit 33 records "roughly 3 px at 320 px width" as an unfixed legibility
   residual. `getComputedStyle` reports the font-size in SVG USER UNITS, which
   is not what a reader sees: the viewBox transform scales it. So the RENDERED
   size is computed here as `userUnits x screenCTM.a`, and cross-checked against
   the measured client rect height of the glyph box. Both are reported, because
   a single number here is exactly how the 2.07 px confusion arose.

2. The LIVE REGION added for announcements. What this instrument can see:
   that the node exists, that it is OUTSIDE `#app` (the router replaces
   `#app.innerHTML` wholesale, and a region rebuilt with its content already
   inside it is not reliably announced), and whether it MUTATES on an ordinary
   route change — the C-8 double-announcement defect unit 25f removed.
   What it CANNOT see: whether anything is spoken. That is the owner's ear and
   nothing here contradicts it.

   METHOD NOTE — the negative result needs a positive control. "The observer
   recorded no mutation" is worthless if the observer was never working. So the
   run ends by firing a path that SHOULD write to the region (Escape from an
   open search panel). If that mutation is not caught, the silence on route
   changes proves nothing and is reported as inconclusive rather than as a pass.

usage: python3 probe4.py mdname <theme> <w1,w2,...>
       python3 probe4.py live   <theme>
"""
import json, os, sys

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp                                     # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))

ZOOM_EU = ("(function(){var b=document.querySelector('[data-zoom=\"europe\"]');"
           "if(!b)return false;b.click();return true;})()")

MDNAME = r"""(function(){
 var els=[].slice.call(document.querySelectorAll('.md-name'));
 if(!els.length)return JSON.stringify({n:0});
 var rows=els.map(function(el){
  var cs=getComputedStyle(el);
  var userFs=parseFloat(cs.fontSize);           /* SVG user units */
  var m=el.getScreenCTM?el.getScreenCTM():null; /* viewBox transform */
  var scale=m?m.a:null;
  var r=el.getBoundingClientRect();             /* real painted box, CSS px */
  var bb=null; try{bb=el.getBBox();}catch(e){}
  return {text:(el.textContent||'').trim().slice(0,28),
          userFs:userFs, ctmScale:scale?Math.round(scale*1000)/1000:null,
          renderedFs:scale?Math.round(userFs*scale*100)/100:null,
          rectH:Math.round(r.height*100)/100, rectW:Math.round(r.width*100)/100,
          bboxH:bb?Math.round(bb.height*100)/100:null};});
 var rf=rows.filter(function(r){return r.renderedFs;}).map(function(r){return r.renderedFs;});
 var rh=rows.map(function(r){return r.rectH;});
 return JSON.stringify({n:rows.length,
   minRenderedFs:rf.length?Math.min.apply(null,rf):null,
   maxRenderedFs:rf.length?Math.max.apply(null,rf):null,
   minRectH:Math.min.apply(null,rh), maxRectH:Math.max.apply(null,rh),
   sample:rows.slice(0,4)});})()"""

# ---- live region: identity and placement
LIVE_ID = r"""(function(){
 var el=document.getElementById('live-status');
 var app=document.getElementById('app');
 if(!el)return JSON.stringify({present:false});
 return JSON.stringify({present:true,
  outsideApp: !!(app && !app.contains(el)),
  parent: el.parentElement?el.parentElement.tagName.toLowerCase():null,
  role: el.getAttribute('role'),
  ariaLive: el.getAttribute('aria-live'),
  ariaAtomic: el.getAttribute('aria-atomic'),
  cls: el.className,
  textAtRest: el.textContent,
  /* is it visually hidden but still exposed? sr-only, not display:none */
  display: getComputedStyle(el).display,
  visibility: getComputedStyle(el).visibility,
  otherLiveRegions: [].slice.call(document.querySelectorAll(
    '[aria-live],[role=status],[role=alert]')).map(function(n){
     return (n.id||n.tagName.toLowerCase())+'['+(n.getAttribute('aria-live')||
      n.getAttribute('role'))+']';})});})()"""

# ---- install a recorder on the region
WATCH = r"""(function(){
 var el=document.getElementById('live-status');
 if(!el)return false;
 window.__vlog=[];
 window.__vobs=new MutationObserver(function(ms){
   ms.forEach(function(m){
     window.__vlog.push({t:Date.now(),type:m.type,
       text:el.textContent, at:location.hash});});});
 window.__vobs.observe(el,{childList:true,characterData:true,subtree:true,
                           attributes:true});
 return true;})()"""
DUMP = "JSON.stringify(window.__vlog||[])"
CLEARLOG = "(function(){window.__vlog=[];return true;})()"

NAV = "(function(h){location.hash=h;return true;})(%s)"

OPEN_SEARCH = ("(function(){var i=document.getElementById('search');if(!i)return false;"
               "i.focus();i.value='van';"
               "i.dispatchEvent(new Event('input',{bubbles:true}));return true;})()")
ESC = r"""(function(){var i=document.getElementById('search');if(!i)return false;
 i.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',code:'Escape',
  keyCode:27,which:27,bubbles:true,cancelable:true}));return true;})()"""
PANEL_OPEN = ("(function(){var p=document.querySelector('.search-results');"
              "return !!(p&&getComputedStyle(p).display!=='none'&&p.offsetHeight>0);})()")


def boot(b, theme):
    b.cmd("Page.addScriptToEvaluateOnNewDocument",
          {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
    b.cmd("Emulation.setEmulatedMedia",
          {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})


def wait(b, ms):
    b.ev("new Promise(function(r){setTimeout(r,%d)})" % ms, await_promise=True)


def mdname(theme, widths):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9495")))
    rows = []
    try:
        boot(b, theme)
        for w in widths:
            b.metrics(w, 900)
            b.goto("%s/index.html?md=%d#/nations" % (cdp.BASE, w), settle=2.2)
            assert b.ev("window.innerWidth") == w
            for zoomed in (False, True):
                if zoomed:
                    if b.ev(ZOOM_EU) is not True:
                        print("%-5s %4dpx  europe-zoom control absent" % (theme, w))
                        continue
                    wait(b, 700)
                d = json.loads(b.ev(MDNAME))
                d.update({"theme": theme, "width": w, "europeZoom": zoomed})
                rows.append(d)
                print("%-5s %4dpx zoom=%-5s n=%-3d renderedFontSize %s..%s px  "
                      "clientRectH %s..%s px"
                      % (theme, w, zoomed, d.get("n", 0),
                         d.get("minRenderedFs"), d.get("maxRenderedFs"),
                         d.get("minRectH"), d.get("maxRectH")), flush=True)
                if d.get("sample"):
                    s = d["sample"][0]
                    print("        e.g. %-28s userFs=%s ctm=%s -> %s px"
                          % (s["text"], s["userFs"], s["ctmScale"], s["renderedFs"]),
                          flush=True)
    finally:
        b.close()
    json.dump(rows, open(os.path.join(OUT, "mdname-%s.json" % theme), "w"), indent=1)
    return rows


def live(theme):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9495")))
    res = {}
    try:
        boot(b, theme)
        b.metrics(1440, 900)
        b.goto("%s/index.html?live=%d#/" % (cdp.BASE, os.getpid()), settle=2.2)
        ident = json.loads(b.ev(LIVE_ID))
        res["identity"] = ident
        print("LIVE REGION IDENTITY")
        for k, v in ident.items():
            print("   %-18s %s" % (k, v))
        if not ident.get("present"):
            return res
        assert b.ev(WATCH) is True
        # ---- ordinary route changes: the C-8 regression test
        routes = ["#/artists", "#/timeline", "#/influences", "#/museums",
                  "#/lists", "#/palette", "#/explore", "#/credits", "#/privacy",
                  "#/artist/leonardo-da-vinci", "#/no-such-page", "#/"]
        b.ev(CLEARLOG)
        per = []
        for r in routes:
            b.ev(CLEARLOG)
            b.ev(NAV % json.dumps(r))
            wait(b, 900)
            log = json.loads(b.ev(DUMP))
            txt = b.ev("document.getElementById('live-status').textContent")
            per.append({"route": r, "mutations": len(log),
                        "regionText": txt, "log": log[:3]})
            print("route %-30s mutations=%-2d regionText=%r"
                  % (r, len(log), txt), flush=True)
        res["routeChanges"] = per
        # ---- POSITIVE CONTROL: a path that SHOULD write to the region.
        # Without this, "no mutations" could just mean a dead observer.
        b.ev(NAV % json.dumps("#/"))
        wait(b, 900)
        b.ev(CLEARLOG)
        opened = b.ev(OPEN_SEARCH)
        wait(b, 700)
        panel = b.ev(PANEL_OPEN)
        b.ev(ESC)
        wait(b, 900)
        ctl_log = json.loads(b.ev(DUMP))
        ctl_txt = b.ev("document.getElementById('live-status').textContent")
        res["positiveControl"] = {"searchOpened": opened, "panelWasOpen": panel,
                                  "mutations": len(ctl_log), "regionText": ctl_txt}
        print("\nPOSITIVE CONTROL (Escape from open search): opened=%s panelOpen=%s "
              "mutations=%d text=%r" % (opened, panel, len(ctl_log), ctl_txt))
    finally:
        b.close()
    json.dump(res, open(os.path.join(OUT, "live-%s.json" % theme), "w"), indent=1)
    return res


if __name__ == "__main__":
    if sys.argv[1] == "mdname":
        ws = [int(x) for x in sys.argv[3].split(",")]
        mdname(sys.argv[2], ws)
    else:
        live(sys.argv[2])
