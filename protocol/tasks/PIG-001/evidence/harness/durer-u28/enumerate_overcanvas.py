"""The DELIBERATE sweep: every text element on the site that paints over the
generative `#bg-canvas`, enumerated exhaustively rather than sampled.

Unit 27 found this class by accident, so unit 28 must not find it by accident
again. The pixel instrument (`canvastext.py`) is the measurement of record, but
it can only see one viewport-band of one draw at a time, which makes it a poor
*enumerator* — a class that never happens to be on screen is a class nobody
knows about.

This is the enumerator. `#bg-canvas` is `position:fixed; inset:0; z-index:-1`,
so it paints ABOVE the propagated body background and BELOW all in-flow content.
An element's glyphs therefore composite over the canvas unless some ancestor
between it and `<body>` paints an OPAQUE background. That is a static property
of the cascade, so it can be read for every text element on a route at once, at
any scroll position, in milliseconds.

It is a static analysis and is treated as one: `canvastext.py` re-tests the same
elements by the three-shot paint differential, and §"corroboration" in the build
log compares the two. Over-selection here is safe (a shielded element simply
measures the same with and without the canvas); under-selection would not be, so
anything ambiguous — a translucent ancestor, a background-image of unknown
coverage, a backdrop-filter — is reported as OVER the canvas.

usage: python3 enumerate_overcanvas.py <theme> <w> <h> <tag>
"""
import json, os, sys

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp, png

OUT = os.path.dirname(os.path.abspath(__file__))

ROUTES = ["#/", "#/artists", "#/artist/leonardo-da-vinci", "#/artist/frida-kahlo",
          "#/artwork/david", "#/explore", "#/timeline", "#/influences", "#/museums",
          "#/museum/louvre", "#/museum/tate-britain", "#/museum/k20-dusseldorf",
          "#/lists", "#/palette", "#/taste", "#/daily", "#/privacy", "#/credits",
          "#/no-such-page"]

SCAN = r"""(function(){
 function alpha(c){var m=(c||'').match(/rgba?\(([^)]+)\)/);
  if(!m)return 0; var p=m[1].split(',');
  return p.length>3?parseFloat(p[3]):1;}
 var out=[];
 [].forEach.call(document.querySelectorAll('*'),function(el){
  var txt='';for(var j=0;j<el.childNodes.length;j++){var cn=el.childNodes[j];
   if(cn.nodeType===3)txt+=cn.nodeValue;}
  if(!txt.trim())return;
  var cs=getComputedStyle(el);
  if(cs.display==='none'||cs.visibility==='hidden')return;
  var r=el.getBoundingClientRect();
  if(r.width<2||r.height<2)return;                 /* never rendered at all */
  /* Walk to <body>. body/html are NOT shields: the body background propagates
     to the canvas root and is painted UNDER a z-index:-1 fixed element. */
  var shield=null, why=null, n=el;
  while(n && n!==document.body){
   var s=getComputedStyle(n);
   if(alpha(s.backgroundColor)>=0.999){shield=n;why='opaque background-color '+s.backgroundColor;break;}
   n=n.parentElement;
  }
  var soft=[];                                     /* ambiguous, reported as OVER */
  n=el;
  while(n && n!==document.body){
   var s2=getComputedStyle(n);
   if(s2.backgroundImage&&s2.backgroundImage!=='none')soft.push('bg-image');
   if(s2.backdropFilter&&s2.backdropFilter!=='none')soft.push('backdrop-filter');
   var a2=alpha(s2.backgroundColor);
   if(a2>0&&a2<0.999)soft.push('bg-alpha '+a2.toFixed(2));
   n=n.parentElement;
  }
  var fpx=parseFloat(cs.fontSize),wt=parseInt(cs.fontWeight,10)||400;
  var inks=[],clip=cs.webkitBackgroundClip||cs.backgroundClip||'';
  if(clip==='text'){var m=cs.backgroundImage.match(/rgba?\([^)]+\)/g)||[];
   inks=m.map(function(s3){var p=s3.match(/[\d.]+/g);return [+p[0],+p[1],+p[2]];});}
  if(!inks.length){var p=cs.color.match(/[\d.]+/g);inks=[[+p[0],+p[1],+p[2]]];}
  var path=[],q=el;
  while(q&&q!==document.body){path.unshift(q.tagName.toLowerCase()+
    (q.classList.length?'.'+[].slice.call(q.classList).join('.'):''));q=q.parentElement;}
  out.push({sel:el.tagName.toLowerCase()+(el.classList.length?'.'+[].slice.call(el.classList).join('.'):''),
   path:path.slice(-3).join(' > '),
   text:txt.trim().replace(/\s+/g,' ').slice(0,30),
   fpx:fpx,weight:wt,large:(fpx>=24||(fpx>=18.66&&wt>=700)),inks:inks,clip:clip,
   overCanvas:(shield===null),
   shieldedBy:shield?(shield.tagName.toLowerCase()+
     (shield.classList.length?'.'+[].slice.call(shield.classList).join('.'):'')+' — '+why):null,
   soft:soft.slice(0,4)});});
 return JSON.stringify({route:location.hash,n:out.length,els:out});})()"""


def main():
    theme, vw, vh, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9451")))
    allels = []
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.cmd("Emulation.setEmulatedMedia",
              {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        b.metrics(vw, vh)
        for k, r in enumerate(ROUTES):
            b.goto("%s/index.html?u28e=%d%s" % (cdp.BASE, k, r), settle=2.4)
            assert b.ev("document.documentElement.dataset.theme") == theme
            d = json.loads(b.ev(SCAN))
            for e in d["els"]:
                e["route"] = r
            allels += d["els"]
            oc = [e for e in d["els"] if e["overCanvas"]]
            print("%-30s text-els=%-4d overCanvas=%-4d" % (r, d["n"], len(oc)), flush=True)
    finally:
        b.close()
    json.dump({"theme": theme, "viewport": [vw, vh], "els": allels},
              open(os.path.join(OUT, "enum-%s.json" % tag), "w"))
    report(allels, theme)


def report(els, theme):
    """Group by (ink, font size, weight): that pair, not the selector, is what
    decides whether a glyph can clear its floor over a given backdrop."""
    groups = {}
    for e in els:
        if not e["overCanvas"]:
            continue
        for ink in e["inks"]:
            k = (tuple(ink), round(e["fpx"], 1), e["weight"], e["large"])
            g = groups.setdefault(k, {"sels": set(), "routes": set(), "n": 0, "soft": set()})
            g["sels"].add(e["sel"]); g["routes"].add(e["route"]); g["n"] += 1
            for s in e["soft"]:
                g["soft"].add(s)
    print("\nDISTINCT (ink x size x weight) PAINTING OVER #bg-canvas — %s" % theme)
    print("%-18s %6s %4s %-6s %5s  %-42s %s" %
          ("ink", "px", "wt", "floor", "count", "selectors", "routes"))
    for k in sorted(groups, key=lambda x: (-groups[x]["n"])):
        ink, fpx, wt, large = k
        g = groups[k]
        print("%-18s %6.1f %4d %-6s %5d  %-42s %d routes  %s" %
              (str(list(ink)), fpx, wt, "3.0" if large else "4.5", g["n"],
               ",".join(sorted(g["sels"]))[:42], len(g["routes"]),
               ",".join(sorted(g["soft"])) or "-"))
    print("\ntotal text elements scanned: %d, over canvas: %d, distinct ink groups: %d"
          % (len(els), sum(1 for e in els if e["overCanvas"]), len(groups)))


main()
