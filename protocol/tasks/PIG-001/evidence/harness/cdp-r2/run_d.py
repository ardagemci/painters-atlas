"""D — 200% text zoom containment across all 26 router cases, 1280 viewport.
Also re-measures the .main-nav mobile treatment (before/after flex-wrap).
"""
import json
import cdp

# one route per switch case in route() (26 cases incl. the 404 default)
STATIC = ["#/", "#/artists", "#/timeline", "#/influences", "#/daily", "#/lists",
          "#/palette", "#/taste", "#/museums", "#/explore", "#/movements",
          "#/techniques", "#/eras", "#/nations", "#/privacy", "#/credits",
          "#/no-such-page"]
# discovered detail routes: list, museum, artist, artwork, movement, technique, era, nation
DISCOVER = [("#/lists", "list"), ("#/museums", "museum"), ("#/artists", "artist"),
            ("#/movements", "movement"), ("#/techniques", "technique"),
            ("#/eras", "era"), ("#/nations", "nation")]

ZOOM_PROBE = r"""(function(){
 var de=document.documentElement;
 var lost=[];
 var sels=['div.mu-hero','div.card-tagline','button.skip-inline'];
 sels.forEach(function(s){
  [].forEach.call(document.querySelectorAll(s),function(el){
   var cs=getComputedStyle(el);
   var ox=cs.overflowX, oy=cs.overflowY;
   var lw=el.scrollWidth-el.clientWidth, lh=el.scrollHeight-el.clientHeight;
   var clipped=(ox==='hidden'||ox==='clip')&&lw>1 ? lw : 0;
   var clippedH=(oy==='hidden'||oy==='clip')&&lh>1 ? lh : 0;
   if(clipped||clippedH) lost.push({sel:s,lostW:clipped,lostH:clippedH,ov:ox+'/'+oy});
  });
 });
 var offend=null,maxR=0;
 [].forEach.call(document.querySelectorAll('body *'),function(el){
  var r=el.getBoundingClientRect();
  if(r.width>0&&r.right>maxR){maxR=r.right;offend=el.tagName.toLowerCase()+
   (el.classList.length?'.'+[].slice.call(el.classList).join('.'):'');}
 });
 var nav=document.querySelector('.main-nav');
 return JSON.stringify({fs:getComputedStyle(de).fontSize,
  cw:de.clientWidth, sw:de.scrollWidth, over:de.scrollWidth-de.clientWidth,
  maxRight:Math.round(maxR), offender:offend,
  navW:nav?Math.round(nav.getBoundingClientRect().width):null,
  navH:nav?Math.round(nav.getBoundingClientRect().height):null,
  navRight:nav?Math.round(nav.getBoundingClientRect().right):null,
  navWrap:nav?getComputedStyle(nav).flexWrap:null,
  clipped:lost, sel3:sels.map(function(s){return s+':'+document.querySelectorAll(s).length;})});})()"""


def main():
    b = cdp.Browser()
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','dark')}catch(e){}"})
        b.metrics(1280, 800)

        # ---- discover detail routes
        routes = list(STATIC)
        for idx, kind in DISCOVER:
            b.goto(cdp.BASE + "/index.html" + idx, settle=1.2)
            href = b.ev("(function(){var a=document.querySelector('#app a[href^=\"#/%s/\"]');"
                        "return a?a.getAttribute('href'):null;})()" % kind)
            if href:
                routes.append(href)
        # passport case
        b.goto(cdp.BASE + "/index.html#/", settle=0.8)
        pp = b.ev("(function(){var p={version:1,createdAt:'2026-01-01T00:00:00.000Z',"
                  "updatedAt:'2026-01-01T00:00:00.000Z',admirations:[],notForMe:[],seen:[],"
                  "wantToSee:[],saved:[],probes:[],quiz:{answers:{},at:null},"
                  "palette:{tones:[]},persona:{},tasteVector:{},milestones:{},"
                  "skipped:[],deckSeen:[],clusters:[]};"
                  "return btoa(unescape(encodeURIComponent(JSON.stringify(p))))"
                  ".replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,'');})()")
        routes.append("#/passport/" + pp)
        print("ROUTES", len(routes), flush=True)

        results = {}
        for width in (1270, 1280):
            b.metrics(width, 800)
            rs = []
            for i, r in enumerate(routes):
                b.goto("%s/index.html?z=%d_%d%s" % (cdp.BASE, width, i, r), settle=1.3)
                b.ev("document.documentElement.style.fontSize='200%'")
                b.ev("new Promise(function(r){setTimeout(r,450)})", await_promise=True)
                b.ev("document.documentElement.style.fontSize='200%'")
                p = json.loads(b.ev(ZOOM_PROBE))
                p["route"] = r[:44]
                rs.append(p)
                print(width, r[:34], "fs=%s cw=%s sw=%s over=%+d nav=%sx%s(r%s) clipped=%d" %
                      (p["fs"], p["cw"], p["sw"], p["over"], p["navW"], p["navH"],
                       p["navRight"], len(p["clipped"])), flush=True)
            results[width] = rs

        # ---- nav mobile treatment: current vs flex-wrap:nowrap (pre-unit-25 behaviour)
        b.metrics(390, 844)
        b.goto(cdp.BASE + "/index.html?navchk=1#/", settle=1.4)
        navm = {}
        for mode in ("wrap", "nowrap"):
            b.ev("document.querySelector('.main-nav').style.flexWrap=%r" % mode)
            navm[mode] = json.loads(b.ev(r"""(function(){var n=document.querySelector('.main-nav');
             var r=n.getBoundingClientRect(); var links=[].slice.call(n.querySelectorAll('a'));
             var vis=links.filter(function(a){var b=a.getBoundingClientRect();
               return b.right<=r.right+0.5 && b.left>=r.left-0.5;}).length;
             return JSON.stringify({w:Math.round(r.width),h:Math.round(r.height),
              scrollW:n.scrollWidth,clientW:n.clientWidth,
              linksFullyInsideBox:vis, links:links.length,
              headerH:Math.round(document.querySelector('.site-header').getBoundingClientRect().height)});})()"""))
        print("NAV390", json.dumps(navm), flush=True)
        with open("zoom200.json", "w") as f:
            json.dump({"routes": routes, "results": {str(k): v for k, v in results.items()},
                       "nav390": navm}, f, indent=1)
    finally:
        b.close()

    for width, rs in results.items():
        bad = [r for r in rs if r["over"] > 0]
        clip = [r for r in rs if r["clipped"]]
        print("\n@%d: %d routes, %d overflowing, max over=%d, %d routes with clipped elements"
              % (width, len(rs), len(bad), max([r["over"] for r in rs]), len(clip)))
        for r in clip:
            print("   clip", r["route"], r["clipped"])


main()
