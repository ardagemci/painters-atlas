"""F-1 — horizontal overflow on `#/` between 821 and 1100 px at 100 % zoom.

The theory pole declined to accept F-1 as out of scope on the ground that real
people use those widths, and they are right, so it is measured here rather than
noted. `body{overflow-x:hidden}` clamps the document scroll width, which is
exactly why the note could survive: the page does not visibly scroll, it CLIPS.
So this measures both — the document's own overflow AND every element whose
border box crosses the right edge of the viewport, which is what a reader
actually loses.

usage: python3 overflow.py <theme> [w1,w2,...]
"""
import json, os, sys

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp                                    # noqa: E402

PROBE = r"""(function(){
 var vw=document.documentElement.clientWidth, out=[];
 /* An element inside a deliberately scrollable box (.strip's marquee track,
    .tl2-wrap, the mobile .main-nav) is not page overflow — its own ancestor
    clips and scrolls it. Only boxes that push the DOCUMENT are counted. */
 function clipped(el){
  for(var n=el.parentElement;n&&n!==document.body;n=n.parentElement){
   var c=getComputedStyle(n).overflowX;
   if(c==='auto'||c==='scroll'||c==='hidden')return true;}
  return false;}
 [].forEach.call(document.querySelectorAll('#app *'),function(el){
  var r=el.getBoundingClientRect();
  if(r.width<2||r.height<2)return;
  var over=Math.round(r.right-vw);
  if(over<=1)return;
  if(clipped(el))return;
  var cs=getComputedStyle(el);
  if(cs.visibility==='hidden'||cs.display==='none')return;
  out.push({sel:el.tagName.toLowerCase()+
            (el.classList.length?'.'+[].slice.call(el.classList).join('.'):''),
            over:over,w:Math.round(r.width),
            minH:cs.minHeight,ar:cs.aspectRatio});});
 out.sort(function(a,b){return b.over-a.over;});
 return JSON.stringify({vw:vw,
   docScrollW:document.documentElement.scrollWidth,
   bodyScrollW:document.body.scrollWidth,
   docOver:document.documentElement.scrollWidth-vw,
   items:out.slice(0,6)});})()"""

WIDTHS = [320, 390, 821, 900, 1024, 1100, 1280, 1440]


def run(theme, widths):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9469")))
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.cmd("Emulation.setEmulatedMedia",
              {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        worst = 0
        for w in widths:
            b.metrics(w, 900)
            b.goto(cdp.BASE + "/index.html#/", settle=2.2)
            d = json.loads(b.ev(PROBE))
            print("%s %4dpx  docScrollW=%-5d over=%-4d  %s"
                  % (theme, w, d["docScrollW"], d["docOver"],
                     "CLEAN" if not d["items"] else ""))
            for it in d["items"]:
                worst = max(worst, it["over"])
                print("      +%-4dpx  %-34s width=%-5d min-height=%-8s aspect-ratio=%s"
                      % (it["over"], it["sel"][:34], it["w"], it["minH"], it["ar"]))
        print("worst overflow on #/ over these widths: %d px" % worst)
    finally:
        b.close()


if __name__ == "__main__":
    ws = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else WIDTHS
    run(sys.argv[1], ws)
