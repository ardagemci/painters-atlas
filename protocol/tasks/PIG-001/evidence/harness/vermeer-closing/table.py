"""Render the AC19 museum sweep into the markdown table used in the report."""
import collections, json, os, sys

OUT = os.path.dirname(os.path.abspath(__file__))
HERO = ("nav.breadcrumbs", "mu-hero-body")

LABEL = {
    "span": "breadcrumb, current page (`--muted`)",
    "span.sep": "breadcrumb separators (`--muted`)",
    "a": "breadcrumb links (`--body-ink`)",
    "h1.display": "`h1.display` venue name (`--ink`)",
    "div.mu-sub": "`.mu-sub` city · country · founded (`--muted`)",
    "div.mu-hook": "`.mu-hook` editorial line (`--gold2`)",
    "button.chip": "`Share this page` chip",
    "p.img-credit.mu-credit": "photograph credit line",
    "span.count": "`.sec-title .count`",
    "div.lbl": "stat label", "div.num": "stat number",
    "h2.sec-title": "section title", "p": "essay paragraph",
}


def render(tag, theme):
    d = json.load(open(os.path.join(OUT, "photo-%s.json" % tag)))
    rows = [r for r in d["rows"] if r["glyphWorst"] is not None]
    hero = [r for r in rows if any(h in (r["path"] or "") for h in HERO)]
    by = collections.defaultdict(list)
    for r in hero:
        by[r["sel"]].append(r)
    print("\n**%s theme — %d venue pages, %d measured text elements, %d of them inside the "
          "photograph hero.**\n" % (theme.capitalize(), len(d["pages"]), len(rows), len(hero)))
    print("| element in the hero | px | floor | **worst measured** | venue | fails on |")
    print("| --- | --- | --- | --- | --- | --- |")
    for sel, rs in sorted(by.items(), key=lambda kv: min(x["glyphWorst"] for x in kv[1])):
        need = rs[0]["need"]
        w = min(rs, key=lambda x: x["glyphWorst"])
        f = [x for x in rs if x["glyphWorst"] < need]
        venues = len(set(x["venue"] for x in rs))
        fvenues = len(set(x["venue"] for x in f))
        mark = "**%.2f**" % w["glyphWorst"] if f else "%.2f" % w["glyphWorst"]
        print("| %s | %.1f | %.1f | %s | `%s` | %s |"
              % (LABEL.get(sel, "`%s`" % sel), w["fpx"], need, mark, w["venue"],
                 "**%d of %d venues**" % (fvenues, venues) if f else "— (0 of %d)" % venues))
    # non-hero classes, for completeness
    rest = [r for r in rows if r not in hero]
    by2 = collections.defaultdict(list)
    for r in rest:
        by2[r["sel"]].append(r)
    bad = {k: v for k, v in by2.items() if any(x["glyphWorst"] < x["need"] for x in v)}
    print("\nBelow the hero, on the same pages: %d further text elements measured, "
          "%d classes fail%s"
          % (len(rest), len(bad),
             (" — " + ", ".join("`%s` worst %.2f on %d of %d venues"
                                % (k, min(x["glyphWorst"] for x in v),
                                   len(set(x["venue"] for x in v if x["glyphWorst"] < x["need"])),
                                   len(set(x["venue"] for x in v)))
                                for k, v in sorted(bad.items()))) if bad else "."))


if __name__ == "__main__":
    render("all-dark", "dark")
    render("all-light", "light")
