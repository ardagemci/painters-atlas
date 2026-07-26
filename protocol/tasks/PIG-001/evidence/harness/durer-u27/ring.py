"""Unit 27 — the museum band's focus ring, measured rather than assumed.

`#app h1:focus-visible{outline:2px solid var(--gold)}` is the one control
indicator that paints INSIDE the new veil, so the veil sets its backdrop. Light's
--gold #9e7938 reads 2.60 against the veiled bound, under WCAG 1.4.11's 3.0
non-text floor; this unit re-points it in the band only.

Both operands are measured here, not asserted:
  * the ring colour is read from the live cascade (getComputedStyle outlineColor
    with :focus-visible actually applied — a real Tab press puts the browser in
    keyboard modality first, because Chrome will not match :focus-visible on a
    programmatic focus otherwise);
  * the backdrop is the veiled block, taken from the same glyph-pixel sweep that
    measured h1.display (`mu-after-<theme>-<w>.json`), i.e. real composited
    pixels, not a computed colour.

usage: python3 ring.py <theme> <w> <h> [venue,venue,...]
"""
import json, os, sys

V = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/vermeer-closing"
C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, V)
sys.path.insert(0, C)
import cdp, photos

OUT = os.path.dirname(os.path.abspath(__file__))
DEFAULT = ["k20-dusseldorf", "louvre", "moderna-museet", "tate-modern", "prado", "met"]

READ = r"""(function(){
 var h=document.querySelector('.mu-hero-body h1');
 if(!h) return JSON.stringify({error:'no h1'});
 h.focus();
 var cs=getComputedStyle(h);
 var r=h.getBoundingClientRect();
 return JSON.stringify({
   matchesFocusVisible: h.matches(':focus-visible'),
   isActive: document.activeElement===h,
   outlineColor: cs.outlineColor, outlineWidth: cs.outlineWidth,
   outlineStyle: cs.outlineStyle, outlineOffset: cs.outlineOffset,
   rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]});})()"""


def lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def ratio(a, b):
    la = .2126 * lin(a[0]) + .7152 * lin(a[1]) + .0722 * lin(a[2])
    lb = .2126 * lin(b[0]) + .7152 * lin(b[1]) + .0722 * lin(b[2])
    if la < lb:
        la, lb = lb, la
    return (la + .05) / (lb + .05)


def main():
    theme, vw, vh = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    ids = sys.argv[4].split(",") if len(sys.argv) > 4 else DEFAULT

    # worst measured backdrop under h1.display in the band, from the glyph sweep
    sweep = os.path.join(OUT, "mu-after-%s-%d.json" % (theme, vw))
    worst_bd, worst_ven = None, None
    if os.path.exists(sweep):
        for r in json.load(open(sweep))["rows"]:
            if r.get("band") and r["sel"] == "h1.display" and r["glyphWorst"] is not None:
                if worst_bd is None or r["glyphWorst"] < worst_bd[0]:
                    worst_bd, worst_ven = (r["glyphWorst"], r["glyphBackdrop"]), r["venue"]

    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9371")))
    b.cmd("Page.addScriptToEvaluateOnNewDocument",
          {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
    b.metrics(vw, vh)
    rows = []
    try:
        for i, vid in enumerate(ids):
            b.goto("%s/index.html?ring=%d#/museum/%s" % (cdp.BASE, i, vid), settle=1.8)
            assert b.ev("document.documentElement.dataset.theme") == theme
            # keyboard modality: Chrome will not match :focus-visible without it
            b.cmd("Input.dispatchKeyEvent", {"type": "rawKeyDown", "key": "Tab",
                                             "code": "Tab", "windowsVirtualKeyCode": 9})
            b.cmd("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Tab",
                                             "code": "Tab", "windowsVirtualKeyCode": 9})
            photos.wait_settled(b)
            d = json.loads(b.ev(READ))
            d["venue"] = vid
            rows.append(d)
            print("%-24s focus-visible=%-5s outline=%s %s %s offset=%s"
                  % (vid, d.get("matchesFocusVisible"), d.get("outlineStyle"),
                     d.get("outlineWidth"), d.get("outlineColor"), d.get("outlineOffset")),
                  flush=True)
    finally:
        b.close()

    print("\nworst measured veiled backdrop under h1.display (%s, %dpx): %s at %s"
          % (theme, vw, worst_bd[1] if worst_bd else "?", worst_ven))
    if worst_bd:
        for d in rows:
            m = (d.get("outlineColor") or "").replace("rgb(", "").replace(")", "").split(",")
            if len(m) < 3:
                continue
            ring = [int(x) for x in m[:3]]
            print("  %-24s ring %s vs %s -> %.2f  need 3.0  %s"
                  % (d["venue"], ring, worst_bd[1], ratio(ring, worst_bd[1]),
                     "PASS" if ratio(ring, worst_bd[1]) >= 3.0 else "FAIL"))
    json.dump(rows, open(os.path.join(OUT, "ring-%s-%d.json" % (theme, vw)), "w"), indent=1)


main()
