"""PIG-001 certification — the 26-route console / network sweep, at HEAD. Vermeer.

Re-run so the regression evidence matches SHIPPED code: units 33/34/36 landed
after the last sweep, and unit 33 in particular added a live region, changed
`route()`'s tail (the sayNext flush) and moved SVG emission order on the map.
Any of those could have introduced a console error the old sweep could not have
seen.

WHAT IS COLLECTED, per route, from the protocol rather than from the page:
  * `Runtime.consoleAPICalled`   — console.error / warn / assert
  * `Runtime.exceptionThrown`    — uncaught exceptions
  * `Log.entryAdded`             — the browser's own log (CSP, deprecations,
                                   mixed content, 404s the page never sees)
  * `Network.loadingFailed`      — requests that did not complete
  * `Network.responseReceived`   — every response, kept for status >= 400
  * every request URL's HOST     — the external-origin question. Expectation on
                                   record: `upload.wikimedia.org` only, and ZERO
                                   font providers. A font provider appearing
                                   here is a privacy regression, not a nicety —
                                   `#/privacy` tells the reader there are none.

Each route is loaded FRESH (full navigation, cache disabled) so one route's
failures cannot be attributed to another.

usage: python3 sweep.py <theme>
"""
import json, os, sys
from urllib.parse import urlparse

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp                                     # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))

# the 26 router cases: every `case` in route(), with real ids for the
# parameterised families, plus the 404 default and the passport path.
ROUTES = [
    "#/", "#/artists", "#/artist/leonardo-da-vinci", "#/artwork/david",
    "#/explore", "#/timeline", "#/influences", "#/daily", "#/lists",
    "#/list/paintings-that-still-scare-us", "#/palette", "#/taste",
    "#/museums", "#/museum/louvre", "#/movements", "#/movement/impressionism",
    "#/techniques", "#/technique/oil-painting", "#/eras", "#/era/16th-century",
    "#/nations", "#/nation/italy", "#/privacy", "#/credits",
    "#/passport/import", "#/no-such-page",
]

FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "use.typekit.net",
              "p.typekit.net", "fast.fonts.net", "cloud.typography.com",
              "use.fontawesome.com", "cdn.jsdelivr.net", "unpkg.com",
              "cdnjs.cloudflare.com")


def classify(b, route):
    """Drain the event queue and bucket everything that arrived for this route."""
    b.drain(1.2)
    errs, warns, failed, http4xx, hosts, logs = [], [], [], [], {}, []
    for m in b.events:
        meth, p = m.get("method"), m.get("params", {})
        if meth == "Runtime.consoleAPICalled":
            lvl = p.get("type")
            txt = " ".join(str(a.get("value", a.get("description", "")))
                           for a in p.get("args", []))[:300]
            if lvl in ("error", "assert"):
                errs.append(txt)
            elif lvl == "warning":
                warns.append(txt)
        elif meth == "Runtime.exceptionThrown":
            d = p.get("exceptionDetails", {})
            errs.append("EXCEPTION: %s %s" % (
                d.get("text", ""),
                (d.get("exception") or {}).get("description", ""))[:300])
        elif meth == "Log.entryAdded":
            e = p.get("entry", {})
            rec = "%s/%s: %s" % (e.get("source"), e.get("level"),
                                 (e.get("text") or "")[:200])
            logs.append(rec)
            if e.get("level") == "error":
                errs.append(rec)
            elif e.get("level") == "warning":
                warns.append(rec)
        elif meth == "Network.requestWillBeSent":
            u = p.get("request", {}).get("url", "")
            h = urlparse(u).hostname
            if h:
                hosts[h] = hosts.get(h, 0) + 1
        elif meth == "Network.loadingFailed":
            if not p.get("canceled"):
                failed.append("%s %s" % (p.get("type"), p.get("errorText")))
        elif meth == "Network.responseReceived":
            r = p.get("response", {})
            if r.get("status", 0) >= 400:
                http4xx.append("%s %s" % (r.get("status"), r.get("url", "")[:160]))
    b.events = []
    return {"route": route, "errors": errs, "warnings": warns,
            "failedRequests": failed, "http4xx": http4xx,
            "hosts": hosts, "browserLog": logs}


def main():
    theme = sys.argv[1]
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9498")))
    rows = []
    try:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.metrics(1440, 900)
        for i, r in enumerate(ROUTES):
            b.events = []
            # full navigation per route, cache disabled by the driver
            b.goto("%s/index.html?sw=%d_%d%s" % (cdp.BASE, os.getpid(), i, r), settle=2.6)
            # let late XHR / image loads and any deferred render settle
            b.ev("new Promise(function(x){setTimeout(x,900)})", await_promise=True)
            d = classify(b, r)
            # broken images, asked of the DOM as well as of the network
            d["brokenImages"] = b.ev(
                "(function(){var i=[].slice.call(document.images);"
                "return i.filter(function(x){return x.complete&&x.naturalWidth===0;})"
                ".length;})()")
            d["imageCount"] = b.ev("document.images.length")
            rows.append(d)
            print("%-40s err=%-2d warn=%-2d failed=%-2d 4xx=%-2d brokenImg=%-2d hosts=%s"
                  % (r[:40], len(d["errors"]), len(d["warnings"]),
                     len(d["failedRequests"]), len(d["http4xx"]),
                     d["brokenImages"], ",".join(sorted(d["hosts"]))), flush=True)
            for e in d["errors"][:3]:
                print("      ERROR  %s" % e[:150], flush=True)
            for wq in d["warnings"][:3]:
                print("      WARN   %s" % wq[:150], flush=True)
    finally:
        b.close()
    json.dump(rows, open(os.path.join(OUT, "sweep-%s.json" % theme), "w"), indent=1)

    allhosts = {}
    for d in rows:
        for h, n in d["hosts"].items():
            allhosts[h] = allhosts.get(h, 0) + n
    print("\n==== SWEEP SUMMARY (%s, %d routes) ====" % (theme, len(rows)))
    print("routes with console errors : %d" % sum(1 for d in rows if d["errors"]))
    print("routes with warnings       : %d" % sum(1 for d in rows if d["warnings"]))
    print("routes with failed requests: %d" % sum(1 for d in rows if d["failedRequests"]))
    print("routes with >=400 responses: %d" % sum(1 for d in rows if d["http4xx"]))
    print("routes with broken images  : %d" % sum(1 for d in rows if d["brokenImages"]))
    print("\nHOSTS CONTACTED:")
    for h, n in sorted(allhosts.items(), key=lambda kv: -kv[1]):
        tag = ""
        if h in FONT_HOSTS:
            tag = "   <-- FONT/CDN PROVIDER: privacy regression"
        elif h not in ("localhost", "127.0.0.1"):
            tag = "   <-- external"
        print("   %-34s %4d%s" % (h, n, tag))
    fonts = [h for h in allhosts if h in FONT_HOSTS]
    print("\nfont/CDN providers contacted: %d %s" % (len(fonts), fonts or ""))


if __name__ == "__main__":
    main()
