"""Capture a clipped screenshot of one route for visual confirmation.
usage: python3 shot.py <route> <theme> <out.png> [w h] [clipX clipY clipW clipH]
"""
import base64, sys, os
H = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, H)
import cdp

route, theme, out = sys.argv[1], sys.argv[2], sys.argv[3]
w = int(sys.argv[4]) if len(sys.argv) > 4 else 1440
h = int(sys.argv[5]) if len(sys.argv) > 5 else 900
clip = [int(x) for x in sys.argv[6:10]] if len(sys.argv) > 9 else None

b = cdp.Browser()
try:
    b.cmd("Page.addScriptToEvaluateOnNewDocument",
          {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
    b.metrics(w, h)
    b.goto("%s/index.html?s=1%s" % (cdp.BASE, route), settle=2.4)
    assert b.ev("document.documentElement.dataset.theme") == theme
    assert b.ev("window.innerWidth") == w
    p = {"format": "png", "captureBeyondViewport": False}
    if clip:
        p["clip"] = {"x": clip[0], "y": clip[1], "width": clip[2], "height": clip[3], "scale": 1}
    r = b.cmd("Page.captureScreenshot", p)
    open(out, "wb").write(base64.b64decode(r["data"]))
    print("wrote", out, os.path.getsize(out), "bytes; innerWidth", b.ev("window.innerWidth"),
          "theme", b.ev("document.documentElement.dataset.theme"))
finally:
    b.close()
