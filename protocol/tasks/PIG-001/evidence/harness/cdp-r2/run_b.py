"""B — re-walk the rendered DOM contrast pairs across 16 routes x 2 themes.

Same semantics as the pre-fix walk that produced contrast-pairs-measured.csv:
every element carrying its own text run, computed colour composited over the
flattened background chain, size classified per WCAG AA, deduped with counts.
Elements painted through background-clip:text emit fg == bg, which the audit
script already treats as 'unresolvable by token maths' (pass 3 territory).
"""
import csv, json
import cdp

OUT = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence"

WALK = r"""(function(){
 function toRGBA(s){var m=/^rgba?\(([^)]+)\)/.exec(s);if(!m)return null;
  var p=m[1].split(',').map(function(x){return parseFloat(x)});
  return [p[0],p[1],p[2],p.length>3?p[3]:1];}
 function comp(f,b){var a=f[3];return [f[0]*a+b[0]*(1-a),f[1]*a+b[1]*(1-a),f[2]*a+b[2]*(1-a),1];}
 function hex(c){return '#'+[0,1,2].map(function(i){var v=Math.max(0,Math.min(255,Math.round(c[i])));
  return (v<16?'0':'')+v.toString(16);}).join('');}
 function backdrop(el){var chain=[],n=el;
  while(n&&n.nodeType===1){chain.push(n);n=n.parentElement;}
  chain.reverse();var base=[255,255,255,1];
  for(var i=0;i<chain.length;i++){var c=toRGBA(getComputedStyle(chain[i]).backgroundColor);
   if(c&&c[3]>0)base=comp(c,base);}
  return base;}
 function sel(el){var s=el.tagName.toLowerCase();
  if(el.classList.length)s+='.'+[].slice.call(el.classList).join('.');
  return s;}
 var out=[],els=document.querySelectorAll('body *');
 for(var i=0;i<els.length;i++){var el=els[i];
  var txt='';for(var j=0;j<el.childNodes.length;j++){var cn=el.childNodes[j];
   if(cn.nodeType===3)txt+=cn.nodeValue;}
  if(!txt.trim())continue;
  var cs=getComputedStyle(el);
  if(cs.display==='none'||cs.visibility==='hidden')continue;
  var r=el.getBoundingClientRect();if(r.width===0&&r.height===0)continue;
  var fgc=toRGBA(cs.color);if(!fgc)continue;
  var bg=backdrop(el);
  var fg=fgc[3]<1?comp(fgc,bg):fgc;
  var fpx=parseFloat(cs.fontSize),wt=parseInt(cs.fontWeight,10)||400;
  var size=(fpx>=24||(fpx>=18.66&&wt>=700))?'large':'body';
  var clip=cs.webkitBackgroundClip||cs.backgroundClip||'';
  var bgh=hex(bg),fgh=(clip==='text')?bgh:hex(fg);
  out.push([fgh,bgh,size,Math.round(fpx),wt,sel(el),txt.trim().replace(/\s+/g,' ').slice(0,26)]);
 }
 return JSON.stringify(out);})()"""


def main():
    b = cdp.Browser()
    agg = {}
    try:
        n = 0
        b.metrics(1440, 900)
        for theme in ["dark", "light"]:
            sid = b.cmd("Page.addScriptToEvaluateOnNewDocument",
                        {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})["identifier"]
            for (slug, route) in cdp.ROUTES16:
                n += 1
                b.goto("%s/index.html?cw=%d%s" % (cdp.BASE, n, route), settle=1.6)
                got = b.ev("document.documentElement.dataset.theme")
                assert got == theme, (slug, theme, got)
                rows = json.loads(b.ev(WALK))
                for (fg, bg, size, fpx, wt, s, ex) in rows:
                    k = (theme, fg, bg, size, fpx, wt, s)
                    if k not in agg:
                        agg[k] = {"count": 0, "route": route, "example": ex}
                    agg[k]["count"] += 1
                print(n, theme, slug, len(rows), flush=True)
            b.cmd("Page.removeScriptToEvaluateOnNewDocument", {"identifier": sid})
    finally:
        b.close()

    path = OUT + "/contrast-pairs-measured.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["theme", "fg", "bg", "size", "fontpx", "weight", "count",
                    "selector", "route", "example"])
        for k in sorted(agg, key=lambda k: (-agg[k]["count"], k)):
            theme, fg, bg, size, fpx, wt, s = k
            d = agg[k]
            w.writerow([theme, fg, bg, size, fpx, wt, d["count"], s, d["route"], d["example"]])
    print("wrote", path, len(agg), "distinct pairs")


main()
