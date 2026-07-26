"""Is the OUT-OF-BAND shortfall a photograph composite, or the generative canvas?

The over-approximate detector flags any text element whose rect intersects a
Wikimedia <img> rect. On museum pages `.mu-collage.c4` is a 2x2 grid taller than
`.mu-hero`, which has `overflow:hidden` — so the bottom row is CLIPPED AWAY and
never painted, while `getBoundingClientRect()` still reports its full box far
down the page. Elements in normal flow below the hero (`span.count`,
`p.img-credit.mu-credit`) intersect that phantom box and get flagged.

That is a detection artefact, but their measured backdrops are still not flat
page paint, so something IS behind them. This settles which: measure the same
glyph pixels twice, once as shipped and once with `#bg-canvas` removed. If the
backdrop collapses to the flat page colour, the surface is the site-wide
generative canvas — NOT a Wikimedia photograph, and therefore not F-V1's class.

usage: python3 bgcanvas.py <venue> <theme> <w> <h>
"""
import json, os, sys

V = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/vermeer-closing"
C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, V)
sys.path.insert(0, C)
import cdp, photos

photos.A_PNG = "/tmp/u27-bgc-a-%d.png" % os.getpid()
photos.B_PNG = "/tmp/u27-bgc-b-%d.png" % os.getpid()

CLIP = r"""(function(){
 /* is the bottom collage row actually painted where its rect claims to be? */
 var out=[];
 [].forEach.call(document.querySelectorAll('.mu-collage img'),function(im){
   var q=im.getBoundingClientRect();
   var cx=Math.round(q.left+q.width/2), cy=Math.round(q.top+q.height/2);
   var hero=document.querySelector('.mu-hero').getBoundingClientRect();
   var top=document.elementFromPoint(cx,cy);
   out.push({rect:[Math.round(q.left),Math.round(q.top),Math.round(q.width),Math.round(q.height)],
             centreInsideHero:(cy>=hero.top&&cy<=hero.bottom),
             elementAtItsOwnCentre: top?top.tagName.toLowerCase()+(top.classList.length?'.'+[].slice.call(top.classList).join('.'):''):null});});
 var h=document.querySelector('.mu-hero').getBoundingClientRect();
 return JSON.stringify({heroRect:[Math.round(h.left),Math.round(h.top),Math.round(h.width),Math.round(h.height)],
   heroOverflow:getComputedStyle(document.querySelector('.mu-hero')).overflow, imgs:out});})()"""


def run(b, venue, theme, vw, vh, kill_canvas, tag):
    b.goto("%s/index.html?bgc=%s#/museum/%s" % (cdp.BASE, tag, venue), settle=2.0)
    assert b.ev("document.documentElement.dataset.theme") == theme
    if kill_canvas:
        b.ev("(function(){var c=document.getElementById('bg-canvas');"
             "if(c)c.style.setProperty('display','none','important');return !!c;})()")
    photos.wait_settled(b)
    d = photos.detect_stable(b)
    res = photos.measure_page(b, d["els"], vw, vh) if d["els"] else []
    return {r["sel"] + "|" + (r["path"] or ""): r for r in res}, d


def main():
    venue, theme, vw, vh = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9381")))
    b.cmd("Page.addScriptToEvaluateOnNewDocument",
          {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
    b.metrics(vw, vh)
    try:
        shipped, d = run(b, venue, theme, vw, vh, False, "as-shipped")
        print("--- collage clipping, %s @ %dx%d ---" % (venue, vw, vh))
        print(b.ev(CLIP))
        killed, _ = run(b, venue, theme, vw, vh, True, "no-canvas")
    finally:
        b.close()
    print("\n%-46s %-22s %-22s" % ("element", "backdrop AS SHIPPED", "backdrop NO #bg-canvas"))
    for k in sorted(set(shipped) | set(killed)):
        a, c = shipped.get(k), killed.get(k)
        if not a or not c or a.get("glyphBackdrop") is None:
            continue
        print("%-46s %-22s %-22s  %s"
              % (k.split("|")[0] + ("  [band]" if a.get("band") else ""),
                 str(a["glyphBackdrop"]), str(c.get("glyphBackdrop")),
                 "worst %.2f -> %.2f" % (a["glyphWorst"], c["glyphWorst"])
                 if a["glyphWorst"] and c.get("glyphWorst") else ""))


main()
