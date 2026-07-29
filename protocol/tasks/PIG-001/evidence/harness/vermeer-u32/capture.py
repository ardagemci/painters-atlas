"""Screenshot helper for unit-32 findings. Vermeer.

Loads a route in a named theme/viewport, optionally runs a prep script and
scrolls a selector into view, and writes a PNG under the task evidence dir with
the Coordinator's naming (`<name>__<viewport>__<theme>.png`).

usage: python3 capture.py <theme> <w> <h> <route> <name> [selector] [prepJS]
"""
import os, sys

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp                                   # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triple                                # noqa: E402
import json                                  # noqa: E402

EV = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence"


def main():
    th, w, h, route, name = (sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
                             sys.argv[4], sys.argv[5])
    sel = sys.argv[6] if len(sys.argv) > 6 else ""
    prep = sys.argv[7] if len(sys.argv) > 7 else ""
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9455")))
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s');"
                         "localStorage.setItem('pigment.taste.v1',%s)}catch(e){}"
                         % (th, json.dumps(triple.SEED_PASSPORT))})
        b.cmd("Emulation.setEmulatedMedia",
              {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        b.metrics(w, h)
        b.goto("%s/index.html?v32cap=%d%s" % (cdp.BASE, os.getpid(), route), settle=2.0)
        assert b.ev("document.documentElement.dataset.theme") == th
        triple.wait_settled(b)
        if prep:
            print("prep ->", b.ev(prep))
            b.ev("new Promise(function(r){setTimeout(r,500)})", await_promise=True)
        if sel:
            b.ev("(function(){var e=document.querySelector(%s);"
                 "if(e)e.scrollIntoView({block:'center',inline:'center'});return !!e;})()"
                 % json.dumps(sel))
            b.ev("new Promise(function(r){setTimeout(r,420)})", await_promise=True)
        vp = "desktop-%dx%d" % (w, h) if w >= 1000 else "mobile-%dx%d" % (w, h)
        out = os.path.join(EV, "%s__%s__%s.png" % (name, vp, th))
        n = b.shot(out)
        print("wrote %s (%d bytes)" % (out, n))
    finally:
        b.close()


if __name__ == "__main__":
    main()
