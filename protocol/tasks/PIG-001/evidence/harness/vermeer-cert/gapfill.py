"""PIG-001 certification — two gaps closed explicitly. Vermeer.

1. `#/artwork/<id>` is a router case that the inherited 200 % zoom harness
   (`cdp-r2/run_d.py`) never reached: its DISCOVER table walks list, museum,
   artist, movement, technique, era and nation, but NOT artwork. So the frozen
   "26/26" zoom result was in fact 25 routes, and the artwork detail view — one
   of the image-heaviest in the build — was never zoom-tested. Measured here.

2. `#/credits` changed its VISIBLE TEXT in unit 36. The recaptured screenshot is
   only evidence of the new copy if the new copy was actually on the page at
   shutter time, so the rendered DOM is asserted to contain the new lede and NOT
   to contain the old one. A screenshot nobody checked the text of is a picture,
   not evidence.

usage: python3 gapfill.py
"""
import json, os, sys

C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, C)
import cdp                                     # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zoom as Z                               # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))

NEW_LEDE = "carry Commons' public-domain assertion"
# OLD_LEDE is the superseded #/credits lede, corrected in unit 36. It is quoted
# verbatim because gap 2 asserts the rendered DOM does NOT contain it: this is a
# negative control, not a claim this pole makes. Marked so the OD-5 prose guard
# records the quotation instead of reading it as an assertion (unit 37, F-9).
OLD_LEDE = "Most reproductions here are public domain."  # OD5-EXEMPT
OLD_PD = "are old enough to be in the public domain"
NEW_PD = "are old enough that Commons files them as public domain"

res = {}
b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9499")))
try:
    # ---------- gap 1: #/artwork/david at 200 % zoom, both themes
    rows = []
    for theme in ("light", "dark"):
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.cmd("Emulation.setEmulatedMedia",
              {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        b.metrics(1280, 800)
        for route in ("#/artwork/david", "#/artwork/the-starry-night"):
            b.goto("%s/index.html?gz=%s%s" % (cdp.BASE, theme, route), settle=2.2)
            if b.ev("location.hash") != route:
                continue
            b.ev("document.documentElement.style.fontSize='200%'")
            b.ev("new Promise(function(r){setTimeout(r,500)})", await_promise=True)
            b.ev("document.documentElement.style.fontSize='200%'")
            b.ev("new Promise(function(r){setTimeout(r,250)})", await_promise=True)
            d = json.loads(b.ev(Z.PROBE))
            d.update({"route": route, "theme": theme})
            rows.append(d)
            print("%-5s %-28s fs=%s docOver=%-4d crossing=%-2d clipped=%-2d %s"
                  % (theme, route, d["fs"], d["docOver"], len(d["items"]),
                     len(d["clipped"]),
                     "" if not d["items"] and d["docOver"] <= 0 else "*** OVERFLOW"),
                  flush=True)
            for it in d["items"]:
                print("      +%-4dpx %-32s width=%d" % (it["over"], it["sel"][:32],
                                                        it["w"]), flush=True)
    res["artworkZoom200"] = rows

    # ---------- gap 2: the #/credits copy that the screenshot claims to show
    cred = {}
    for theme in ("light", "dark"):
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
        b.metrics(1440, 900)
        b.goto("%s/index.html?gc=%s#/credits" % (cdp.BASE, theme), settle=2.6)
        txt = b.ev("document.getElementById('app').innerText")
        cred[theme] = {
            "newLedePresent": NEW_LEDE in txt,
            "oldLedeAbsent": OLD_LEDE not in txt,
            "newPdPhrasePresent": NEW_PD in txt,
            "oldPdPhraseAbsent": OLD_PD not in txt,
            "theme": b.ev("document.documentElement.dataset.theme"),
            "chars": len(txt),
        }
        print("credits/%-5s newLede=%s oldLedeGone=%s newPD=%s oldPDGone=%s (%d chars)"
              % (theme, cred[theme]["newLedePresent"], cred[theme]["oldLedeAbsent"],
                 cred[theme]["newPdPhrasePresent"], cred[theme]["oldPdPhraseAbsent"],
                 cred[theme]["chars"]), flush=True)
    res["creditsCopy"] = cred
finally:
    b.close()

json.dump(res, open(os.path.join(OUT, "gapfill.json"), "w"), indent=1)
bad = [r for r in res["artworkZoom200"] if r["items"] or r["docOver"] > 0]
print("\nartwork routes at 200%%: %d measured, %d overflowing"
      % (len(res["artworkZoom200"]), len(bad)))
