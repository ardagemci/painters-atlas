"""AT-2, step 2 — the geometric state of each skip control AT THE INSTANT focus
lands on it, which is what an AT queries.

Two skip controls ship in this build. One (`.skip-inline`, the graph bypass) was
CONFIRMED working under VoiceOver/Safari; the other (`.skip-link`, the header
bypass) was not announced. They differ in exactly two respects, both geometric:

  .skip-link    resting rect is entirely OUTSIDE the viewport (position:fixed,
                top:-120px) and reaches the viewport only through a 180 ms
                `transition:top`.
  .skip-inline  resting rect is a 1x1 clip INSIDE the viewport, and its focus
                state applies with no transition on geometry.

This measures the focused rect at t=0 (same task as the focus event) and after
the transition, for both.

usage: python3 skiprect.py <theme> <w> <h>
"""
import json, os, sys

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp                                    # noqa: E402

PROBE = r"""(function(sel){
 var e=document.querySelector(sel);
 if(!e)return JSON.stringify({missing:true});
 var rest=e.getBoundingClientRect();
 e.focus();
 var t0=e.getBoundingClientRect();          /* same task as the focus event */
 return JSON.stringify({
   restRect:[Math.round(rest.left),Math.round(rest.top),
             Math.round(rest.width),Math.round(rest.height)],
   restInVP:(rest.bottom>0&&rest.top<innerHeight&&rest.right>0&&rest.left<innerWidth),
   t0Rect:[Math.round(t0.left),Math.round(t0.top),
           Math.round(t0.width),Math.round(t0.height)],
   t0InVP:(t0.bottom>0&&t0.top<innerHeight&&t0.right>0&&t0.left<innerWidth),
   transition:getComputedStyle(e).transitionProperty+" "+getComputedStyle(e).transitionDuration
 });})(%s)"""

SETTLED = r"""(function(sel){
 var e=document.querySelector(sel);
 var r=e.getBoundingClientRect();
 return JSON.stringify({rect:[Math.round(r.left),Math.round(r.top),
   Math.round(r.width),Math.round(r.height)],
   inVP:(r.bottom>0&&r.top<innerHeight&&r.right>0&&r.left<innerWidth)});})(%s)"""


def run(theme, vw, vh):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9462")))
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.metrics(vw, vh)
        for route, sel in (("#/", ".skip-link"), ("#/influences", ".skip-inline")):
            b.goto(cdp.BASE + "/index.html" + route, settle=2.2)
            d = json.loads(b.ev(PROBE % json.dumps(sel)))
            if d.get("missing"):
                print("%-14s NOT PRESENT on %s" % (sel, route))
                continue
            b.ev("new Promise(function(r){setTimeout(r,500)})", await_promise=True)
            s = json.loads(b.ev(SETTLED % json.dumps(sel)))
            print("%-14s on %-14s" % (sel, route))
            print("   at rest      rect=%-26s inViewport=%s" % (d["restRect"], d["restInVP"]))
            print("   t=0 (focus)  rect=%-26s inViewport=%s   <-- what an AT queries"
                  % (d["t0Rect"], d["t0InVP"]))
            print("   settled      rect=%-26s inViewport=%s" % (s["rect"], s["inVP"]))
            print("   transition   %s" % d["transition"])
    finally:
        b.close()


if __name__ == "__main__":
    run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
