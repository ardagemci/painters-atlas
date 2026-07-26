"""Unit 27 — the museum band's focus ring, measured a way that actually works.

ring.py tried to reach :focus-visible by dispatching Tab and then calling
focus(). Chrome did not enter keyboard modality, so `h.matches(':focus-visible')`
came back FALSE, `outline-style` computed to `none`, and the outlineColor it
reported was just currentColor — i.e. it was measuring the TEXT, not the ring.
Those numbers were discarded rather than reported. This is the replacement.

Two independent instruments, because the question has two halves:

  1. DOES MY RULE WIN? — `CSS.getMatchedStylesForNode` lists every rule that
     matches the element INCLUDING pseudo-class rules that are not currently
     active, in cascade order. That answers the specificity question
     (`html[data-theme=light] #app .mu-hero-body h1:focus-visible` vs the shipped
     `#app h1:focus-visible`) without needing the state to be live.
  2. WHAT DOES IT ACTUALLY PAINT? — `CSS.forcePseudoState` forces :focus-visible
     on for real, so getComputedStyle returns the ring as it would render.

The backdrop is not computed here: it is the worst veiled backdrop measured
under h1.display by the glyph sweep (`mu-after-<theme>-<w>.json`), i.e. real
composited pixels over a real photograph.

usage: python3 ring2.py <theme> <w> <h> [venue,...]
"""
import json, os, sys

V = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/vermeer-closing"
C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, V)
sys.path.insert(0, C)
import cdp, photos

OUT = os.path.dirname(os.path.abspath(__file__))
DEFAULT = ["k20-dusseldorf", "louvre", "moderna-museet", "tate-modern", "prado", "met"]


def lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def ratio(a, b):
    la = .2126 * lin(a[0]) + .7152 * lin(a[1]) + .0722 * lin(a[2])
    lb = .2126 * lin(b[0]) + .7152 * lin(b[1]) + .0722 * lin(b[2])
    if la < lb:
        la, lb = lb, la
    return (la + .05) / (lb + .05)


def rgb(s):
    n = [int(float(x)) for x in (s or "").replace("rgba(", "").replace("rgb(", "")
         .replace(")", "").split(",")[:3] if x.strip()]
    return n if len(n) == 3 else None


def main():
    theme, vw, vh = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    ids = sys.argv[4].split(",") if len(sys.argv) > 4 else DEFAULT

    sweep = os.path.join(OUT, "mu-after-%s-%d.json" % (theme, vw))
    bd, bd_ven = None, None
    for r in json.load(open(sweep))["rows"]:
        if r.get("band") and r["sel"] == "h1.display" and r["glyphWorst"] is not None:
            if bd is None or r["glyphWorst"] < bd[0]:
                bd, bd_ven = (r["glyphWorst"], r["glyphBackdrop"]), r["venue"]
    worst_bd = bd[1]

    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9421")))
    b.cmd("Page.addScriptToEvaluateOnNewDocument",
          {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
    b.metrics(vw, vh)
    rows = []
    try:
        b.cmd("DOM.enable", {})
        b.cmd("CSS.enable", {})
        for i, vid in enumerate(ids):
            b.goto("%s/index.html?ring2=%d#/museum/%s" % (cdp.BASE, i, vid), settle=1.8)
            assert b.ev("document.documentElement.dataset.theme") == theme
            photos.wait_settled(b)
            # cdp.Browser.cmd already unwraps the "result" envelope
            root = b.cmd("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
            nid = b.cmd("DOM.querySelector",
                        {"nodeId": root, "selector": ".mu-hero-body h1"})["nodeId"]

            # (1) cascade: which :focus-visible rules match, in order?
            ms = b.cmd("CSS.getMatchedStylesForNode", {"nodeId": nid})
            fv = []
            for m in ms.get("matchedCSSRules", []):
                sel = m["rule"]["selectorList"]["text"]
                if "focus-visible" not in sel:
                    continue
                props = {p["name"]: p["value"] for p in m["rule"]["style"]["cssProperties"]
                         if p.get("name") in ("outline", "outline-color")}
                if props:
                    fv.append({"selector": sel, "props": props})

            # (2) rendering: force the state on and read what it paints
            b.cmd("CSS.forcePseudoState", {"nodeId": nid, "forcedPseudoClasses": ["focus-visible"]})
            b.ev("document.querySelector('.mu-hero-body h1').focus()")
            got = json.loads(b.ev(
                "(function(){var h=document.querySelector('.mu-hero-body h1');var c=getComputedStyle(h);"
                "return JSON.stringify({color:c.outlineColor,style:c.outlineStyle,"
                "width:c.outlineWidth,offset:c.outlineOffset});})()"))
            b.cmd("CSS.forcePseudoState", {"nodeId": nid, "forcedPseudoClasses": []})
            got["venue"], got["matchedFocusVisibleRules"] = vid, fv
            rows.append(got)
            print("%-24s outline=%s %s %s offset=%s" % (vid, got["style"], got["width"],
                                                        got["color"], got["offset"]), flush=True)
            for f in fv:
                print("      matched: %-58s %s" % (f["selector"], f["props"]), flush=True)
    finally:
        b.close()

    print("\nworst veiled backdrop under h1.display (%s, %d px): %s at %s  [measured pixels]"
          % (theme, vw, worst_bd, bd_ven))
    ok = True
    for d in rows:
        c = rgb(d["color"])
        if not c or d["style"] == "none":
            print("  %-24s NO RING RESOLVED — inconclusive" % d["venue"])
            ok = False
            continue
        r = ratio(c, worst_bd)
        if r < 3.0:
            ok = False
        print("  %-24s ring %s vs %s -> %.2f  need 3.0  %s"
              % (d["venue"], c, worst_bd, r, "PASS" if r >= 3.0 else "FAIL"))
    print("VERDICT:", "PASS" if ok else "FAIL")
    json.dump(rows, open(os.path.join(OUT, "ring2-%s-%d.json" % (theme, vw)), "w"), indent=1)


main()
