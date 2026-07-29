"""Aggregate every unit-32 run into the (ink, size, backdrop) TRIPLE table.

The reporting unit is Van Eyck's, not the host: a row is one
(ink RGB, font size + weight class, measured backdrop class) and it carries the
worst value observed anywhere for that triple, with the route/selector/cell that
produced it. A host appears only as an example of a triple, never as the key.

usage: python3 report.py [glob ...]
"""
import glob, json, os, sys

OUT = os.path.dirname(os.path.abspath(__file__))


def hexs(c):
    return "#%02x%02x%02x" % tuple(int(v) for v in c)


def surface(r):
    if r.get("overCanvas") and r.get("overCover"):
        return "canvas+cover"
    if r.get("overCanvas"):
        return "#bg-canvas"
    if r.get("overCover"):
        return "cover"
    return "opaque " + hexs(r["backdropNoCanvas"])


def size_class(r):
    return "%.1fpx/%d%s" % (r["fpx"], r["weight"], " L" if r["large"] else "")


def load(pats):
    rows = []
    for p in pats:
        for f in sorted(glob.glob(os.path.join(OUT, p))):
            d = json.load(open(f))
            for r in d["rows"]:
                r.setdefault("route", r.get("route", "?"))
                r["_file"] = os.path.basename(f)
                rows.append(r)
    return rows


def main():
    pats = sys.argv[1:] or ["triple-*.json", "site-*.json"]
    rows = [r for r in load(pats) if not r.get("suppress")]
    # fullyOccluded rows have no unoccluded backdrop; they are carried into
    # NOT TESTED, never into the triple table.
    rows = [r for r in rows if r.get("worst") is not None]
    print("rows loaded: %d" % len(rows))
    cells = sorted({(r["theme"], r["vw"]) for r in rows})
    routes = sorted({r["route"] for r in rows})
    print("cells: %s" % ", ".join("%s@%d" % c for c in cells))
    print("routes: %d" % len(routes))

    by = {}
    for r in rows:
        k = (r["theme"], hexs(r["ink"]), size_class(r), surface(r))
        e = by.setdefault(k, {"worst": 99.0, "n": 0, "need": r["need"],
                              "routes": set(), "sels": set(), "cells": set()})
        e["n"] += 1
        e["routes"].add(r["route"])
        e["sels"].add(r["sel"])
        e["cells"].add("%s@%d" % (r["theme"], r["vw"]))
        if r["worst"] < e["worst"]:
            e.update({"worst": r["worst"], "ex": r})

    fails = {k: v for k, v in by.items() if v["worst"] < v["need"]}
    print("\ndistinct triples: %d   below floor: %d\n" % (len(by), len(fails)))
    print("| theme | ink | size | measured backdrop | worst | floor | n | routes | example selector |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for k, v in sorted(by.items(), key=lambda kv: kv[1]["worst"]):
        th, ink, sz, sf = k
        bad = v["worst"] < v["need"]
        print("| %s | `%s` | %s | %s | %s%.2f%s | %.1f | %d | %d | `%s` |"
              % (th, ink, sz, sf,
                 "**" if bad else "", v["worst"], "**" if bad else "",
                 v["need"], v["n"], len(v["routes"]),
                 sorted(v["sels"], key=len)[0][:44]))
    if fails:
        print("\nFAILING TRIPLES — detail")
        for k, v in sorted(fails.items(), key=lambda kv: kv[1]["worst"]):
            e = v["ex"]
            print("  %s %s %s on %s -> %.2f (need %.1f)"
                  % (k[0], k[1], k[2], k[3], v["worst"], v["need"]))
            print("      worst at %s  sel %s  text %r  backdrop %s  glyphPx %d"
                  % (e["route"], e["sel"], e.get("text", ""),
                     hexs(e["backdrop"]), e.get("glyphPx", 0)))
            print("      seen on %d route(s), cells %s"
                  % (len(v["routes"]), ",".join(sorted(v["cells"]))))
            print("      routes: %s" % ", ".join(sorted(v["routes"])[:12]))
    # OCCLUSION — reported as its own class, never mixed into the AC19 verdict.
    occ = {}
    for r in rows:
        if r.get("worstOccluded") is None or r["worstOccluded"] >= r["need"]:
            continue
        k = (r["theme"], r["vw"], tuple(sorted(r.get("occluders") or [])), r["route"])
        e = occ.setdefault(k, {"worst": 99.0, "n": 0, "sels": set()})
        e["n"] += 1
        e["sels"].add(r["sel"])
        if r["worstOccluded"] < e["worst"]:
            e["worst"] = r["worstOccluded"]
            e["ex"] = r
    print("\nOCCLUDED-PIXEL LOWS (NOT AC19 verdicts — text in transit under an overlay)")
    print("| theme | vp | route | occluder(s) | worst occluded | clean worst | n |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for k, v in sorted(occ.items(), key=lambda kv: kv[1]["worst"]):
        e = v["ex"]
        print("| %s | %d | `%s` | %s | %.2f | %s | %d |"
              % (k[0], k[1], k[3], ", ".join("`%s`" % s for s in k[2]),
                 v["worst"], e["worst"] if e["worst"] is not None else "n/a", v["n"]))
    fo = [r for r in rows if r.get("fullyOccluded")]
    print("rows with NO unoccluded glyph pixel at their sampled band (not cleared): %d" % len(fo))

    # per-route coverage, so the perimeter is stated from the data
    print("\nROUTE x CELL COVERAGE (rows measured)")
    cov = {}
    for r in rows:
        cov.setdefault(r["route"], {}).setdefault("%s@%d" % (r["theme"], r["vw"]), 0)
        cov[r["route"]]["%s@%d" % (r["theme"], r["vw"])] += 1
    hdr = ["%s@%d" % c for c in cells]
    print("| route | " + " | ".join(hdr) + " |")
    print("| --- |" + " --- |" * len(hdr))
    for rt in routes:
        print("| `%s` | %s |" % (rt, " | ".join(str(cov[rt].get(h, 0)) for h in hdr)))


if __name__ == "__main__":
    main()
