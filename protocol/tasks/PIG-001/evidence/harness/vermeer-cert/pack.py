"""PIG-001 certification — the screenshot pack, recaptured at HEAD. Vermeer.

The shipped pack predates units 33 (contrast + geometry), 34 (speech) and 36
(the `#/credits` lede). `#/credits` in particular changed its VISIBLE TEXT, so
the existing capture of it is not merely old, it is wrong.

WHY Emulation.setDeviceMetricsOverride AND NOT --window-size
Headless Chrome on this Mac clamps window width to a 500 px minimum. A 390 px
capture requested through `--window-size` silently produced a 500 px-wide
LAYOUT cropped into a 390 px FILE — a mobile screenshot that was never a mobile
render. That was my own finding and it is the reason every viewport here is set
through `Emulation.setDeviceMetricsOverride`, which is not subject to the clamp,
and the reason `window.innerWidth` is asserted IN THE PAGE at shutter time
rather than assumed from the request.

FILENAMES keep `desktop`/`mobile` and `dark`/`light` literal, because the
kernel's quality gate greps them.

usage: python3 pack.py <theme> <w> <h> [routekey,...]
"""
import base64, json, os, sys, time

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
V = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/vermeer-u32"
sys.path.insert(0, C)
sys.path.insert(0, V)
import cdp                                     # noqa: E402
import sitecensus as sc                        # noqa: E402

EV = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence"
OUT = os.path.dirname(os.path.abspath(__file__))

# the shipped pack's own route set and names, so the recapture REPLACES it
ROUTES = [
    ("home", "#/"),
    ("artists", "#/artists"),
    ("artist-leonardo", "#/artist/leonardo-da-vinci"),
    ("artwork-david", "#/artwork/david"),
    ("explore", "#/explore"),
    ("timeline", "#/timeline"),
    ("influences", "#/influences"),
    ("museums", "#/museums"),
    ("museum-louvre", "#/museum/louvre"),
    ("lists", "#/lists"),
    ("palette", "#/palette"),
    ("taste", "#/taste"),
    ("daily", "#/daily"),
    ("privacy", "#/privacy"),
    ("credits", "#/credits"),          # unit 36 changed this view's visible text
    ("invalid-route", "#/no-such-page"),
]


def main():
    theme, w, h = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    keys = sys.argv[4].split(",") if len(sys.argv) > 4 else None
    routes = [r for r in ROUTES if not keys or r[0] in keys]
    vp = "desktop-%dx%d" % (w, h) if w >= 1000 else "mobile-%dx%d" % (w, h)
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9490")))
    asserts = []
    try:
        sc.boot(b, theme)                       # theme + seeded passport + reduced motion
        b.metrics(w, h)                         # NOT --window-size: see module docstring
        for name, route in routes:
            b.goto("%s/index.html?cap=%d%s" % (cdp.BASE, os.getpid(), route), settle=2.4)
            sc.wait_settled(b)
            # asserted IN THE PAGE, at shutter time, not assumed from the request
            iw = b.ev("window.innerWidth")
            th = b.ev("document.documentElement.dataset.theme")
            hsh = b.ev("location.hash")
            imgs = b.ev("(function(){var i=[].slice.call(document.images);"
                        "return JSON.stringify({total:i.length,"
                        "broken:i.filter(function(x){return x.complete&&"
                        "x.naturalWidth===0;}).length});})()")
            assert iw == w, "innerWidth %s != %s for %s" % (iw, w, name)
            assert th == theme, "theme %s != %s for %s" % (th, theme, name)
            out = os.path.join(EV, "%s__%s__%s.png" % (name, vp, theme))
            r = b.cmd("Page.captureScreenshot",
                      {"format": "png", "captureBeyondViewport": False})
            open(out, "wb").write(base64.b64decode(r["data"]))
            rec = {"file": os.path.basename(out), "route": route, "theme": th,
                   "innerWidth": iw, "innerHeight": b.ev("window.innerHeight"),
                   "hash": hsh, "images": json.loads(imgs),
                   "bytes": os.path.getsize(out)}
            asserts.append(rec)
            print("%-16s %-30s iw=%-5d theme=%-5s imgs=%s broken=%d %d bytes"
                  % (name, route[:30], iw, th, rec["images"]["total"],
                     rec["images"]["broken"], rec["bytes"]), flush=True)
    finally:
        b.close()
    p = os.path.join(OUT, "capture-assertions-%s-%d.json" % (theme, w))
    json.dump(asserts, open(p, "w"), indent=1)
    print("wrote %d captures; assertions -> %s" % (len(asserts), p))


if __name__ == "__main__":
    main()
