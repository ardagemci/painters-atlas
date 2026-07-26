"""Why do the OUT-OF-BAND elements read a non-flat backdrop?

Unit 27's veil covers `.mu-hero-body`. The over-approximate detector also caught
`span.count` and `p.img-credit.mu-credit`, which are in normal flow BELOW the
hero and should therefore sit on flat page paint. They do not — they read
[42,35,26] dark / [195,198,188] light. Before any of that is called an AC19
photograph composite, find out what is actually painted underneath: this walks
the real stacking at the element's own glyph coordinates.

usage: python3 probe_outband.py <venue> <theme> <sel> <w> <h>
"""
import json, os, sys

V = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/vermeer-closing"
C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, V)
sys.path.insert(0, C)
import cdp, photos

PROBE = r"""(function(){
 var el=document.querySelector(%s);
 if(!el) return JSON.stringify({error:'not found'});
 var r=el.getBoundingClientRect();
 var x=Math.round(r.left+r.width/2), y=Math.round(r.top+r.height/2);
 var stack=document.elementsFromPoint(x,y).map(function(n){
   var cs=getComputedStyle(n);
   return {tag:n.tagName.toLowerCase()+(n.classList.length?'.'+[].slice.call(n.classList).join('.'):''),
           bg:cs.backgroundColor, bgImg:cs.backgroundImage.slice(0,70),
           pos:cs.position, z:cs.zIndex,
           rect:[Math.round(n.getBoundingClientRect().left),Math.round(n.getBoundingClientRect().top),
                 Math.round(n.getBoundingClientRect().width),Math.round(n.getBoundingClientRect().height)]};});
 /* every wikimedia img on the page, and whether its rect contains (x,y) */
 var imgs=[].slice.call(document.images).filter(function(i){
   return /upload\.wikimedia\.org/.test(i.currentSrc||i.src||'');}).map(function(i){
   var q=i.getBoundingClientRect();
   return {src:(i.currentSrc||i.src).split('/').pop().slice(0,44),
           rect:[Math.round(q.left),Math.round(q.top),Math.round(q.width),Math.round(q.height)],
           containsGlyphPoint:(x>=q.left&&x<=q.right&&y>=q.top&&y<=q.bottom),
           intersectsElRect:(r.left<q.right&&r.right>q.left&&r.top<q.bottom&&r.bottom>q.top)};})
   .filter(function(o){return o.intersectsElRect||o.containsGlyphPoint;});
 var can=document.getElementById('bg-canvas');
 var ccs=can?getComputedStyle(can):null;
 return JSON.stringify({sel:%s, rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
   glyphPoint:[x,y], color:getComputedStyle(el).color,
   stack:stack, wikimediaImgs:imgs,
   bgCanvas: can?{opacity:ccs.opacity,pos:ccs.position,z:ccs.zIndex,
                  rect:[can.getBoundingClientRect().left,can.getBoundingClientRect().top,
                        can.getBoundingClientRect().width,can.getBoundingClientRect().height],
                  display:ccs.display}:null,
   bodyBg:getComputedStyle(document.body).backgroundColor,
   htmlBg:getComputedStyle(document.documentElement).backgroundColor});})()"""


def main():
    venue, theme, sel, vw, vh = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9341")))
    b.cmd("Page.addScriptToEvaluateOnNewDocument",
          {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
    b.metrics(vw, vh)
    try:
        b.goto("%s/index.html?probe=1#/museum/%s" % (cdp.BASE, venue), settle=2.0)
        assert b.ev("document.documentElement.dataset.theme") == theme
        photos.wait_settled(b)
        out = json.loads(b.ev(PROBE % (json.dumps(sel), json.dumps(sel))))
        print(json.dumps(out, indent=1))
    finally:
        b.close()


main()
