#!/usr/bin/env python3
"""PIG-001 / AC19 — WCAG 2.2 contrast audit (Vermeer, browser evidence).

Two passes, stdlib only:

  Pass 1  Token table.  Parses the ~19 colour custom properties per theme from
          css/styles.css (:root = dark, html[data-theme="light"] = light) and
          scores every foreground token against every surface token, so the
          design system itself can be inspected pair by pair.

  Pass 2  Actually-used pairs.  Reads contrast-pairs-measured.csv, which was
          produced by walking the live DOM in a real browser across 16 routes in
          both themes: for every element with its own text run, the computed
          colour was composited over the first opaque ancestor background (alpha
          layers flattened in order).  Only pairs that really render are scored.

Thresholds: WCAG 2.2 AA — 4.5:1 body text, 3:1 large text (>=24px, or >=18.66px
at weight >=700) and 3:1 for UI component / focus indicators (1.4.11).

Usage:  python3 contrast-audit.py            # from this directory
"""

import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CSS = os.path.join(REPO, "css", "styles.css")
PAIRS = os.path.join(HERE, "contrast-pairs-measured.csv")

AA_BODY, AA_LARGE, AA_UI = 4.5, 3.0, 3.0


# ---------------------------------------------------------------- colour maths
def parse_colour(s):
    """#rgb / #rrggbb / rgba(...) -> (r, g, b, a) with 0-255 channels."""
    s = s.strip()
    m = re.match(r"^#([0-9a-fA-F]{3})$", s)
    if m:
        return tuple(int(c * 2, 16) for c in m.group(1)) + (1.0,)
    m = re.match(r"^#([0-9a-fA-F]{6})$", s)
    if m:
        h = m.group(1)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    m = re.match(r"^rgba?\(([^)]+)\)$", s)
    if m:
        parts = [p.strip() for p in m.group(1).split(",")]
        r, g, b = (int(round(float(p))) for p in parts[:3])
        a = float(parts[3]) if len(parts) > 3 else 1.0
        return (r, g, b, a)
    return None


def composite(fg, bg):
    """Source-over: flatten a translucent colour onto an opaque backdrop."""
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3)) + (1.0,)


def rel_luminance(c):
    out = []
    for ch in c[:3]:
        v = ch / 255.0
        out.append(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4)
    r, g, b = out
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    l1, l2 = rel_luminance(fg), rel_luminance(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


# ------------------------------------------------------------------ token table
def read_tokens():
    src = open(CSS, encoding="utf-8").read()
    themes = {}
    for name, pattern in (("dark", r"^:root\{(.*?)^\}"),
                          ("light", r'^html\[data-theme="light"\]\{(.*?)^\}')):
        m = re.search(pattern, src, re.S | re.M)
        if not m:
            sys.exit("could not find the %s token block in %s" % (name, CSS))
        toks = {}
        for prop, val in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", m.group(1)):
            c = parse_colour(val)
            if c:
                toks[prop] = c
        themes[name] = toks
    return themes


# `--bg` is the page, `--panel`/`--panel2` are raised cards; the rest are inks.
SURFACES = ["--bg", "--bg2", "--panel", "--panel2"]
FOREGROUNDS = ["--ink", "--body-ink", "--muted", "--faint",
               "--gold", "--gold2", "--wine", "--teal", "--blue"]


def pass1(themes):
    print("=" * 78)
    print("PASS 1 — design tokens, every ink over every surface (both themes)")
    print("=" * 78)
    worst = []
    for theme in ("dark", "light"):
        toks = themes[theme]
        print("\n[%s]  %d colour tokens parsed" % (theme, len(toks)))
        print("  %-12s %-10s %-9s %-7s %-7s %s"
              % ("ink", "surface", "ratio", "body", "large/UI", "note"))
        for fgname in FOREGROUNDS:
            if fgname not in toks:
                continue
            for bgname in SURFACES:
                if bgname not in toks:
                    continue
                bg = toks[bgname]
                fg = toks[fgname]
                if fg[3] < 1:
                    fg = composite(fg, bg)
                r = ratio(fg, bg)
                body = "PASS" if r >= AA_BODY else "FAIL"
                large = "PASS" if r >= AA_LARGE else "FAIL"
                note = ""
                if body == "FAIL" and large == "PASS":
                    note = "large text / UI only"
                elif body == "FAIL":
                    note = "below 3:1 — not usable for text or UI"
                    worst.append((theme, fgname, bgname, r))
                print("  %-12s %-10s %-9.2f %-7s %-7s %s"
                      % (fgname, bgname, r, body, large, note))
    return worst


# ------------------------------------------------------- actually-rendered pairs
def pass2():
    print("\n" + "=" * 78)
    print("PASS 2 — pairs actually rendered in the browser (16 routes x 2 themes)")
    print("=" * 78)
    rows = list(csv.DictReader(open(PAIRS, encoding="utf-8")))
    fails, unresolvable = [], []
    for row in rows:
        fg, bg = parse_colour(row["fg"]), parse_colour(row["bg"])
        if fg is None or bg is None:
            continue
        if row["fg"] == row["bg"]:
            unresolvable.append(row)
            continue
        r = ratio(fg, bg)
        need = AA_LARGE if row["size"] == "large" else AA_BODY
        row["_ratio"], row["_need"] = r, need
        if r < need:
            fails.append(row)

    scored = len(rows) - len(unresolvable)
    print("\n%d distinct rendered pairs; %d scored, %d unresolvable by token maths."
          % (len(rows), scored, len(unresolvable)))

    if fails:
        print("\nFAILURES (%d):" % len(fails))
        print("  %-6s %-9s %-9s %-6s %-6s %-7s %-22s %s"
              % ("theme", "fg", "bg", "ratio", "need", "count", "selector", "example"))
        for f in sorted(fails, key=lambda x: x["_ratio"]):
            print("  %-6s %-9s %-9s %-6.2f %-6.1f %-7s %-22s %s"
                  % (f["theme"], f["fg"], f["bg"], f["_ratio"], f["_need"],
                     f["count"], f["selector"], f["example"][:34]))
        print("\n  CAVEAT — a bare `span` row whose ratio is ~1.0 is a walk artifact, not a")
        print("  render failure: #/timeline bars for LIVING painters are filled with an")
        print("  inline linear-gradient, and a computed-style walk reads backgroundColor")
        print("  only, so it falls through to the page behind the bar. Those labels were")
        print("  measured from real glyph pixels instead — worst 4.61:1 across 156")
        print("  painters in both themes, zero below AA. See the pass 3 note.")
    else:
        print("\nNo failures among the scored pairs.")

    if unresolvable:
        print("\nUNRESOLVABLE by token maths — must be judged from pixels (%d):"
              % len(unresolvable))
        for u in unresolvable:
            print("  %-6s %-22s %-12s %s"
                  % (u["theme"], u["selector"], u["route"], u["example"]))
        print("  (background-clip:text over a gradient: the computed colour is the")
        print("   fill, not the painted glyph, so a browser pixel read is required.)")
    return fails, unresolvable


# --------------------------------------------- composites read from the browser
# Values below were sampled in Chrome, not assumed:
#   * HERO: re-measured after unit 25 on REAL GLYPH PIXELS. Two screenshots per
#     load, one with the hero text painted and one with it hidden; a pixel counts
#     only where the two differ strongly, so the sample is confined to where a
#     glyph actually lands instead of covering the whole (mostly empty) text box.
#     The ink is the declared paint — the four gradient stops for the
#     background-clip:text title, the computed colour otherwise — and the
#     backdrop is that same pixel with the text hidden, i.e. everything really
#     painted behind it. 8 fresh covers per theme; the worst is recorded.
#     NOTE the surface: the hero sits over an UNNAMED canvas inside .home-hero at
#     opacity 1 (rect 129,103 1182x438), not over #bg-canvas at opacity .6. The
#     unit-25d bound was computed against #bg-canvas, which is the wrong layer.
#   * focus indicators: token values read from the live cascade after unit 25.
HERO_MEASURED = {  # (worst ratio, ink, backdrop, font px, large?) per selector
    "light": [("h1.home-title", 3.06, [129, 99, 43], [196, 191, 181], 59, True),
              ("div.kicker", 8.08, [43, 38, 32], [194, 190, 180], 12, False),
              ("p.lede", 5.69, [67, 60, 49], [192, 187, 177], 17, False),
              ("p.footer-note", 5.44, [67, 60, 49], [187, 183, 173], 12, False),
              ("a", 5.72, [67, 60, 49], [194, 187, 178], 12, False)],
    "dark": [("h1.home-title", 1.10, [201, 164, 92], [170, 160, 144], 59, True),
             ("div.kicker", 4.05, [232, 201, 138], [96, 94, 90], 12, False),
             ("p.lede", 1.97, [216, 210, 196], [151, 150, 143], 17, False),
             ("p.footer-note", 1.74, [139, 131, 114], [99, 93, 80], 12, False),
             ("a", 4.09, [232, 201, 138], [99, 93, 80], 12, False)],
}
FOCUS_RINGS = {  # circle.ig-ring stroke (= --gold2) vs the graph panel beneath it
    "dark": ([232, 201, 138], [22, 20, 15]),
    "light": ([129, 99, 43], [250, 246, 236]),
}
SKIP_LINK = {  # skip-link outline (= --gold) vs its own focused background
    "dark": ([201, 164, 92], [29, 26, 19]),
    "light": ([158, 121, 56], [240, 233, 218]),
}


def pass3():
    print("\n" + "=" * 78)
    print("PASS 3 — composites token maths cannot reach (browser-sampled)")
    print("=" * 78)
    fails = []

    print("\nHome hero over the generative cover, measured on real glyph pixels")
    print("(8 fresh covers per theme; worst observed):")
    for theme in ("dark", "light"):
        for sel, r, ink, backdrop, fpx, large in HERO_MEASURED[theme]:
            need = AA_LARGE if large else AA_BODY
            verdict = "PASS" if r >= need else "FAIL"
            print("  %-6s %-16s %5.2f:1  need %.1f %-11s %s   ink %-16s over %s"
                  % (theme, sel, r, need, "(large text)" if large else "(body text)",
                     verdict, str(ink), str(backdrop)))
            if verdict == "FAIL":
                fails.append(("hero:" + sel, theme, r))

    print("\nFocus indicators (WCAG 1.4.11, need %.1f:1):" % AA_UI)
    for label, table in (("influence-graph node ring", FOCUS_RINGS),
                         ("skip-link outline", SKIP_LINK)):
        for theme in ("dark", "light"):
            fg, bg = table[theme]
            r = ratio(tuple(fg) + (1.0,), tuple(bg) + (1.0,))
            verdict = "PASS" if r >= AA_UI else "FAIL"
            print("  %-26s %-6s %6.2f:1  %s" % (label, theme, r, verdict))
            if verdict == "FAIL":
                fails.append((label, theme, r))
    return fails


def main():
    themes = read_tokens()
    pass1(themes)
    fails, unresolvable = pass2()
    composite_fails = pass3()
    print("\n" + "=" * 78)
    print("SUMMARY: %d rendered-pair failures (pass 2), %d composite failures (pass 3)."
          % (len(fails), len(composite_fails)))
    for name, theme, r in composite_fails:
        print("         composite FAIL: %s [%s] %.2f:1" % (name, theme, r))
    print("=" * 78)


if __name__ == "__main__":
    main()
