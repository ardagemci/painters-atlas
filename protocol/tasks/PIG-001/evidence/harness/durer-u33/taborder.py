"""AT-2 diagnosis — what does the FIRST Tab actually reach?

Browser evidence recorded `.skip-link` as the first tabbable element with a
visible focus state; the owner's VoiceOver/Safari session reports the first Tab
landing in the navigation with no skip control announced. This walks the real
sequential focus order with real key events (CDP Input.dispatchKeyEvent, not a
simulated `focus()`), and dumps what the accessibility tree says about the
element at each stop.

usage: python3 taborder.py <theme> <w> <h> [n]
"""
import json, os, sys

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp                                    # noqa: E402

DESCRIBE = r"""(function(){
 var a=document.activeElement;
 if(!a||a===document.body)return JSON.stringify({tag:"BODY"});
 var r=a.getBoundingClientRect(), cs=getComputedStyle(a);
 return JSON.stringify({
  tag:a.tagName,
  cls:(a.className&&a.className.baseVal!==undefined?a.className.baseVal:a.className)||"",
  id:a.id||"",
  text:(a.textContent||a.getAttribute("aria-label")||"").trim().replace(/\s+/g," ").slice(0,44),
  rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],
  pos:cs.position, clip:cs.clipPath, vis:cs.visibility,
  inViewport:(r.bottom>0&&r.top<innerHeight&&r.right>0&&r.left<innerWidth)
 });})()"""


def tab(b):
    for t in ("rawKeyDown", "char", "keyUp"):
        p = {"type": t, "key": "Tab", "code": "Tab", "windowsVirtualKeyCode": 9,
             "nativeVirtualKeyCode": 9}
        if t == "char":
            p = {"type": "char", "text": "\t", "key": "Tab"}
        b.cmd("Input.dispatchKeyEvent", p)


def run(theme, vw, vh, n):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9461")))
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.cmd("Emulation.setEmulatedMedia",
              {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        b.metrics(vw, vh)
        b.goto(cdp.BASE + "/index.html#/", settle=2.0)
        b.ev("(function(){document.body.click();"
             "if(document.activeElement&&document.activeElement.blur)"
             "document.activeElement.blur();return true;})()")
        print("start activeElement:", b.ev(DESCRIBE))
        print("--- %s %dx%d — sequential focus order, real Tab key events ---"
              % (theme, vw, vh))
        for i in range(n):
            tab(b)
            b.ev("new Promise(function(r){setTimeout(r,90)})", await_promise=True)
            d = json.loads(b.ev(DESCRIBE))
            print("  Tab %-2d  %-8s %-16s %-30s rect=%s pos=%-8s inVP=%s"
                  % (i + 1, d.get("tag"), (d.get("id") or d.get("cls", ""))[:16],
                     d.get("text", "")[:30], d.get("rect"), d.get("pos"),
                     d.get("inViewport")))
    finally:
        b.close()


if __name__ == "__main__":
    run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
        int(sys.argv[4]) if len(sys.argv) > 4 else 6)
