"""Before -> after table for F-V1, per element class x theme x viewport.

BEFORE is the 15-venue adversarial subset (`mu.WORST`) measured with the shipped
rules restored at runtime; AFTER is the full 104-venue sweep. To keep the two
comparable the AFTER column is reported twice: once restricted to the same 15
venues, once over all 104 (which can only be worse, never better).
"""
import json, os, sys

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, OUT)
import mu


def load(tag):
    p = os.path.join(OUT, "mu-%s.json" % tag)
    return json.load(open(p))["rows"] if os.path.exists(p) else None


def worst(rows, band=True, venues=None):
    by = {}
    for r in rows or []:
        if r["glyphWorst"] is None or r.get("band") != band:
            continue
        if venues and r["venue"] not in venues:
            continue
        k = r["sel"]
        if k not in by or r["glyphWorst"] < by[k]["glyphWorst"]:
            by[k] = r
    return by


def main():
    subset = set(mu.WORST)
    print("| viewport | theme | class | floor | BEFORE (15 venues) | AFTER (same 15) "
          "| AFTER (all 104) | verdict |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for vw, vh, vlabel in ((1440, 900, "1440x900"), (390, 844, "390x844")):
        for theme in ("dark", "light"):
            bef = worst(load("before-%s-%d" % (theme, vw)))
            aft_s = worst(load("after-%s-%d" % (theme, vw)), venues=subset)
            aft_a = worst(load("after-%s-%d" % (theme, vw)))
            for k in sorted(set(bef) | set(aft_a),
                            key=lambda k: aft_a.get(k, {}).get("glyphWorst", 99)):
                need = (aft_a.get(k) or bef.get(k))["need"]
                b_ = bef.get(k, {}).get("glyphWorst")
                s_ = aft_s.get(k, {}).get("glyphWorst")
                a_ = aft_a.get(k, {}).get("glyphWorst")
                ok = a_ is not None and a_ >= need
                print("| %s | %s | `%s` | %.1f | %s | %s | %s | %s |"
                      % (vlabel, theme, k, need,
                         "%.2f %s" % (b_, "FAIL" if b_ < need else "pass") if b_ else "—",
                         "%.2f" % s_ if s_ else "—",
                         "**%.2f**" % a_ if a_ else "—",
                         "**PASS**" if ok else "**FAIL**"))
    print()
    for vw, vh, vlabel in ((1440, 900, "1440x900"), (390, 844, "390x844")):
        for theme in ("dark", "light"):
            rows = load("after-%s-%d" % (theme, vw)) or []
            band = [r for r in rows if r.get("band") and r["glyphWorst"] is not None]
            bad = [r for r in band if r["glyphWorst"] < r["need"]]
            ven = len(set(r["venue"] for r in band))
            print("%s %-5s  band measurements %4d over %3d venues · below floor: %d %s"
                  % (vlabel, theme, len(band), ven, len(bad),
                     [(r["venue"], r["sel"], r["glyphWorst"]) for r in bad[:6]]))
    print("\nOUTSIDE THE BAND (over-approximation; not a photograph composite unless noted)")
    for vw, vh, vlabel in ((1440, 900, "1440x900"), (390, 844, "390x844")):
        for theme in ("dark", "light"):
            w = worst(load("after-%s-%d" % (theme, vw)), band=False)
            for k, r in sorted(w.items(), key=lambda kv: kv[1]["glyphWorst"])[:3]:
                print("  %-9s %-5s %-26s %6.2f need %.1f %-4s  %s"
                      % (vlabel, theme, k, r["glyphWorst"], r["need"],
                         "PASS" if r["glyphWorst"] >= r["need"] else "FAIL", r["venue"]))


main()
