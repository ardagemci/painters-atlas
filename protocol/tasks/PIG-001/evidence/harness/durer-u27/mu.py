"""Unit 27 / F-V1 — museum-band photograph composites, measured on real glyph
pixels, in both themes, at BOTH viewports.

This is a thin driver over Vermeer's closing harness
(`harness/vermeer-closing/photos.py`): same two-shot glyph diff, same pure-Python
PNG decode (so `getImageData` and the cross-origin taint never enter into it),
same deliberately over-approximate detection. Nothing about the instrument is
re-invented here. What it adds:

  * an explicit venue list, so the venues that produced the worst numbers can be
    re-measured directly rather than the first N off `#/museums`;
  * a viewport argument that is actually threaded through — 390x844 as well as
    1440x900, which is Vermeer's NOT TESTED #4 and this unit's brief;
  * a `band` flag per row, separating the elements that live inside
    `.mu-hero-body` (the class F-V1 is about) from everything else the
    over-approximation caught;
  * a BEFORE mode that restores the shipped rules at runtime, so before and
    after are measured by one instrument on one build;
  * browser recycling, because a single headless Chrome does not survive 104
    clip-captures on this Mac.

usage: python3 mu.py <all|worst|id,id,...> <theme> <w> <h> <tag>
       U27_BEFORE=1 to measure the pre-unit-27 CSS.
"""
import json, os, sys

V = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/vermeer-closing"
C = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, V)
sys.path.insert(0, C)
import cdp, photos
import functools

# photos.measure_page evaluates png.ratio once per pixel per ink over whole
# element rects; at 104 venues x 2 themes x 2 viewports that is the entire
# runtime. png.ratio is a pure function of two RGB tuples and its arguments
# repeat heavily (flat scrim backdrops), so memoising it is exact — identical
# numbers, an order of magnitude less arithmetic. Nothing else is altered.
photos.png.ratio = functools.lru_cache(maxsize=1 << 20)(photos.png.ratio)

# photos.py writes both shots to fixed /tmp paths, so two runs at once silently
# read each other's pixels — that is exactly how a first attempt at this unit
# reported a dark-theme backdrop of [225,211,183], which the veil makes
# arithmetically impossible. Per-process paths; runs are also serialised.
photos.A_PNG = "/tmp/u27-shot-a-%d.png" % os.getpid()
photos.B_PNG = "/tmp/u27-shot-b-%d.png" % os.getpid()

OUT = os.path.dirname(os.path.abspath(__file__))
CHUNK = 20

# The venues that produced the worst glyph contrast in Vermeer's closing sweep,
# per class and per theme, plus the two he checked by eye. This is the
# adversarial sample; `all` is the exhaustive one.
WORST = ["k20-dusseldorf", "prado", "louvre", "moderna-museet", "sistine-chapel",
         "museu-picasso-barcelona", "tate-modern", "stanley-museum-iowa",
         "neue-galerie", "met", "belvedere", "yale-university-art-gallery",
         "frida-kahlo", "accademia-florence", "st-peters-basilica"]

# Unit 27's whole change is CSS, so the BEFORE state can be measured by the same
# instrument on the same build by restoring the shipped rules at runtime. Every
# declaration below is the literal text that stood in styles.css at 73ddc27.
BEFORE_CSS = """
.mu-shade{background:linear-gradient(180deg,rgba(var(--bg-rgb),.18),rgba(var(--bg-rgb),.94) 80%)!important}
.mu-hero-body{background:none!important}
.mu-hero-body .breadcrumbs,.mu-hero-body .breadcrumbs .sep{color:var(--faint)!important}
.mu-hero-body .breadcrumbs a{color:var(--muted)!important}
.mu-hero-body .breadcrumbs a:hover{color:var(--gold2)!important}
html[data-theme="light"] .mu-hook,html[data-theme="light"] .mu-sub a{color:var(--gold2)!important}
"""
BEFORE = bool(os.environ.get("U27_BEFORE"))


def boot(theme, vw, vh):
    b = cdp.Browser(port=int(os.environ.get("CDP_PORT", "9333")))
    b.cmd("Page.addScriptToEvaluateOnNewDocument",
          {"source": "try{localStorage.setItem('pigment-theme','%s')}catch(e){}" % theme})
    if BEFORE:
        b.cmd("Page.addScriptToEvaluateOnNewDocument",
              {"source": "document.addEventListener('DOMContentLoaded',function(){"
                         "var s=document.createElement('style');s.id='u27-before';"
                         "s.textContent=%s;document.head.appendChild(s);});" % json.dumps(BEFORE_CSS)})
    b.metrics(vw, vh)
    return b


def one(b, k, vid, theme, vw, vh):
    """Measure one venue. Raises on any broken assertion or dead browser."""
    b.goto("%s/index.html?u27=%d#/museum/%s" % (cdp.BASE, k, vid), settle=1.9)
    assert b.ev("document.documentElement.dataset.theme") == theme
    assert b.ev("window.innerWidth") == vw
    # a BEFORE run that lost its override would silently report the fixed build
    assert bool(b.ev("!!document.getElementById('u27-before')")) == BEFORE
    photos.wait_settled(b)
    d = photos.detect_stable(b)
    if not d["els"]:
        return [], {"venue": vid, "imgs": d["imgs"], "els": 0}
    res = photos.measure_page(b, d["els"], vw, vh)
    for r in res:
        r["venue"], r["theme"], r["viewport"] = vid, theme, [vw, vh]
        r["band"] = "mu-hero-body" in (r["path"] or "")
        r["layoutStable"] = d.get("stable")
    return res, {"venue": vid, "imgs": d["imgs"], "els": len(res),
                 "layoutStable": d.get("stable"),
                 "heroKind": "collage" if any("collage" in (e["path"] or "")
                                              for e in d["els"]) else "photo"}


def run(ids, theme, vw, vh, tag):
    b = boot(theme, vw, vh)
    rows, pages, done, fails = [], [], set(), {}
    try:
        if ids == "all":
            ids = photos.venue_ids(b)
        assert len(ids) >= 100 or ids is not None
        print("venues=%d theme=%s %dx%d before=%s" % (len(ids), theme, vw, vh, BEFORE), flush=True)
        queue = list(ids)
        while queue:
            vid = queue.pop(0)
            k = len(done)
            try:
                res, page = one(b, k, vid, theme, vw, vh)
            except Exception as e:
                fails[vid] = fails.get(vid, 0) + 1
                print("   !! %s: %s — recycling browser (attempt %d)"
                      % (vid, type(e).__name__, fails[vid]), flush=True)
                try:
                    b.close()
                except Exception:
                    pass
                b = boot(theme, vw, vh)
                if fails[vid] < 3:
                    queue.append(vid)          # retry at the end of the queue
                continue
            rows.extend(res)
            pages.append(page)
            done.add(vid)
            if res:
                w = min([r["glyphWorst"] for r in res if r["glyphWorst"] is not None] or [99])
                bw = min([r["glyphWorst"] for r in res
                          if r["band"] and r["glyphWorst"] is not None] or [99])
                print("%3d %-28s imgs=%-2d els=%-2d worst=%.2f band=%.2f"
                      % (k, vid, page["imgs"], len(res), w, bw), flush=True)
            else:
                print("%3d %-28s imgs=%d  no composite" % (k, vid, page["imgs"]), flush=True)
            if len(done) % CHUNK == 0 and queue:
                b.close()
                b = boot(theme, vw, vh)
    finally:
        try:
            b.close()
        except Exception:
            pass
    print("measured %d venues; unrecoverable: %s"
          % (len(done), [v for v, n in fails.items() if n >= 3] or "none"), flush=True)
    json.dump({"theme": theme, "viewport": [vw, vh], "before": BEFORE,
               "measured": len(done), "unrecoverable": [v for v, n in fails.items() if n >= 3],
               "pages": pages, "rows": rows},
              open(os.path.join(OUT, "mu-%s.json" % tag), "w"), indent=1)
    report(rows, tag)
    return rows


def report(rows, tag):
    for scope, keep in (("IN THE MUSEUM BAND (.mu-hero-body)", True),
                        ("ELSEWHERE ON THE PAGE (over-approximation)", False)):
        by = {}
        for r in rows:
            if r["glyphWorst"] is None or r["band"] != keep:
                continue
            k = r["sel"]
            if k not in by or r["glyphWorst"] < by[k]["glyphWorst"]:
                by[k] = r
        print("\n%s  [%s]" % (scope, tag))
        if not by:
            print("  (none)")
        for k, r in sorted(by.items(), key=lambda kv: kv[1]["glyphWorst"]):
            print("  %-30s %6.2f  need %.1f  %-4s  %-26s ink %-16s backdrop %-16s (%d px)"
                  % (k, r["glyphWorst"], r["need"],
                     "PASS" if r["glyphWorst"] >= r["need"] else "FAIL",
                     r["venue"], str(r["glyphInk"]), str(r["glyphBackdrop"]), r["glyphPx"]))


if __name__ == "__main__":
    what = sys.argv[1]
    v = "all" if what == "all" else (WORST if what == "worst" else what.split(","))
    run(v, sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
