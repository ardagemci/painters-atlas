"""PIG-001 certification — 200 % text zoom, and F-1, remeasured at HEAD. Vermeer.

Unit 33 changed geometry on `.skip-link`, `.tl2-year`, `.daily-media` and the map
labels. The frozen 200 % matrix (26/26 zero overflow) predates those changes and
is therefore STALE — unit 33 says so itself and did not repeat it. This repeats
it, and measures F-1 in the same instrument.

TWO MEASUREMENTS, because they answer different questions and one hides the other
  * `docOver`  — documentElement.scrollWidth - clientWidth. This is what a
    "does the page scroll sideways" check sees, and it is NOT sufficient:
    `body{overflow-x:hidden}` clamps it, so a page that CLIPS its content reads
    as clean. That is precisely how F-1 survived every earlier responsive pass.
  * `items`    — every element in `#app` whose border box crosses the right edge
    of the viewport, excluding anything inside a deliberately scrollable
    ancestor (the marquee track, `.tl2-wrap`, the mobile nav), because an
    element its own ancestor scrolls is not page overflow. This is what a reader
    actually loses.
  A route is clean only when BOTH are zero.

`mode=zoom` additionally reports the four selectors unit 33 moved, so a
regression in them is attributable rather than merely visible in a total.

usage:
  python3 zoom.py f1   <theme>                 # F-1: #/ at eight widths, 100 %
  python3 zoom.py zoom <theme> <width>         # 200 % text zoom over 26 routes
"""
import json, os, sys

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp                                     # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))

PROBE = r"""(function(){
 var vw=document.documentElement.clientWidth, out=[];
 function scrollClipped(el){
  for(var n=el.parentElement;n&&n!==document.body;n=n.parentElement){
   var c=getComputedStyle(n).overflowX;
   if(c==='auto'||c==='scroll'||c==='hidden')return true;}
  return false;}
 [].forEach.call(document.querySelectorAll('#app *'),function(el){
  var r=el.getBoundingClientRect();
  if(r.width<2||r.height<2)return;
  var over=Math.round(r.right-vw);
  if(over<=1)return;
  if(scrollClipped(el))return;
  var cs=getComputedStyle(el);
  if(cs.visibility==='hidden'||cs.display==='none')return;
  out.push({sel:el.tagName.toLowerCase()+
            (el.classList.length?'.'+[].slice.call(el.classList).join('.'):''),
            over:over,w:Math.round(r.width),
            minH:cs.minHeight,ar:cs.aspectRatio});});
 out.sort(function(a,b){return b.over-a.over;});
 /* the four selectors unit 33 moved — reported so a regression is attributable */
 var moved={};
 ['.skip-link','.tl2-year','.daily-media','.md-name'].forEach(function(s){
  var els=[].slice.call(document.querySelectorAll(s));
  if(!els.length){moved[s]=null;return;}
  var worst=0,wr=null;
  els.forEach(function(el){var r=el.getBoundingClientRect();
   var o=Math.round(r.right-vw); if(o>worst){worst=o;wr=[Math.round(r.left),
    Math.round(r.top),Math.round(r.width),Math.round(r.height)];}});
  moved[s]={n:els.length,worstOver:worst,rect:wr};});
 /* elements whose own box clips their content at this zoom */
 var lost=[];
 [].forEach.call(document.querySelectorAll('#app *'),function(el){
  var cs=getComputedStyle(el);
  if(cs.overflowX!=='hidden'&&cs.overflowX!=='clip'&&
     cs.overflowY!=='hidden'&&cs.overflowY!=='clip')return;
  var lw=el.scrollWidth-el.clientWidth, lh=el.scrollHeight-el.clientHeight;
  if(lw<=1&&lh<=1)return;
  if(el.className&&/strip|marquee|tl2-wrap|main-nav/.test(el.className))return;
  lost.push({sel:el.tagName.toLowerCase()+
    (el.classList.length?'.'+[].slice.call(el.classList).join('.'):''),
    lostW:lw>1?lw:0,lostH:lh>1?lh:0});});
 return JSON.stringify({vw:vw,
   fs:getComputedStyle(document.documentElement).fontSize,
   docScrollW:document.documentElement.scrollWidth,
   docOver:document.documentElement.scrollWidth-vw,
   items:out.slice(0,6), moved:moved, clipped:lost.slice(0,8)});})()"""

F1_WIDTHS = [320, 390, 821, 900, 1024, 1100, 1280, 1440]

STATIC = ["#/", "#/artists", "#/timeline", "#/influences", "#/daily", "#/lists",
          "#/palette", "#/taste", "#/museums", "#/explore", "#/movements",
          "#/techniques", "#/eras", "#/nations", "#/privacy", "#/credits",
          "#/no-such-page"]
DISCOVER = [("#/lists", "list"), ("#/museums", "museum"), ("#/artists", "artist"),
            ("#/movements", "movement"), ("#/techniques", "technique"),
            ("#/eras", "era"), ("#/nations", "nation")]


def boot(b, theme):
    b.cmd("Page.addScriptToEvaluateOnNewDocument",
          {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
    b.cmd("Emulation.setEmulatedMedia",
          {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})


def discover_routes(b):
    routes = list(STATIC)
    for idx, kind in DISCOVER:
        b.goto(cdp.BASE + "/index.html" + idx, settle=1.3)
        href = b.ev("(function(){var a=document.querySelector('#app a[href^=\"#/%s/\"]');"
                    "return a?a.getAttribute('href'):null;})()" % kind)
        if href:
            routes.append(href)
    b.goto(cdp.BASE + "/index.html#/", settle=0.8)
    pp = b.ev("(function(){var p={version:1,createdAt:'2026-01-01T00:00:00.000Z',"
              "updatedAt:'2026-01-01T00:00:00.000Z',admirations:[],notForMe:[],seen:[],"
              "wantToSee:[],saved:[],probes:[],quiz:{answers:{},at:null},"
              "palette:{tones:[]},persona:{},tasteVector:{},milestones:{},"
              "skipped:[],deckSeen:[],clusters:[]};"
              "return btoa(unescape(encodeURIComponent(JSON.stringify(p))))"
              ".replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,'');})()")
    routes.append("#/passport/" + pp)
    return routes


def f1(theme):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9480")))
    rows = []
    try:
        boot(b, theme)
        worst = 0
        for w in F1_WIDTHS:
            b.metrics(w, 900)
            b.goto("%s/index.html?f1=%d#/" % (cdp.BASE, w), settle=2.2)
            assert b.ev("window.innerWidth") == w
            d = json.loads(b.ev(PROBE))
            d["width"] = w
            d["theme"] = theme
            rows.append(d)
            crossing = sum(i["over"] for i in d["items"])
            worst = max(worst, d["docOver"], max([i["over"] for i in d["items"]] or [0]))
            print("%-5s %4dpx  docScrollW=%-5d docOver=%-4d crossing=%-2d  %s"
                  % (theme, w, d["docScrollW"], d["docOver"], len(d["items"]),
                     "CLEAN" if not d["items"] and d["docOver"] <= 0 else "OVERFLOW"),
                  flush=True)
            for it in d["items"]:
                print("        +%-4dpx  %-32s width=%-5d min-height=%-8s aspect-ratio=%s"
                      % (it["over"], it["sel"][:32], it["w"], it["minH"], it["ar"]),
                      flush=True)
        print("WORST overflow on #/ across these widths (%s): %d px" % (theme, worst))
    finally:
        b.close()
    json.dump(rows, open(os.path.join(OUT, "f1-%s.json" % theme), "w"), indent=1)
    return rows


def zoom(theme, width):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9480")))
    rows = []
    try:
        boot(b, theme)
        b.metrics(width, 800)
        routes = discover_routes(b)
        print("ROUTES %d  theme=%s width=%d" % (len(routes), theme, width), flush=True)
        b.metrics(width, 800)
        for i, r in enumerate(routes):
            b.goto("%s/index.html?z=%d_%d%s" % (cdp.BASE, width, i, r), settle=1.5)
            # applied twice: the router re-renders and can reset inline style
            b.ev("document.documentElement.style.fontSize='200%'")
            b.ev("new Promise(function(r){setTimeout(r,500)})", await_promise=True)
            b.ev("document.documentElement.style.fontSize='200%'")
            b.ev("new Promise(function(r){setTimeout(r,250)})", await_promise=True)
            d = json.loads(b.ev(PROBE))
            assert d["fs"] == "32px", "200%% zoom not applied: %s" % d["fs"]
            d["route"] = r
            d["theme"] = theme
            rows.append(d)
            print("%-5s %-40s fs=%s docOver=%-4d crossing=%-2d clipped=%-2d %s"
                  % (theme, r[:40], d["fs"], d["docOver"], len(d["items"]),
                     len(d["clipped"]),
                     "" if not d["items"] and d["docOver"] <= 0 else "*** OVERFLOW"),
                  flush=True)
            for it in d["items"]:
                print("        +%-4dpx  %-32s width=%d"
                      % (it["over"], it["sel"][:32], it["w"]), flush=True)
    finally:
        b.close()
    json.dump(rows, open(os.path.join(OUT, "zoom200-%s-%d.json" % (theme, width)), "w"),
              indent=1)
    bad = [r for r in rows if r["items"] or r["docOver"] > 0]
    print("\n%s @%d: %d routes, %d with overflow at 200%%"
          % (theme, width, len(rows), len(bad)))
    for r in bad:
        print("   ", r["route"], r["docOver"], [i["sel"] for i in r["items"]])
    return rows


if __name__ == "__main__":
    if sys.argv[1] == "f1":
        f1(sys.argv[2])
    else:
        zoom(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1280)
