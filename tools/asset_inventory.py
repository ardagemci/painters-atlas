#!/usr/bin/env python3
"""Regenerate Pigment's public asset inventory.

Enumerates every upload.wikimedia.org reference the repository exposes, by
surface, and reports references vs unique assets plus reachability. Pure
static analysis: **no network requests**, so reachability is derived from code
gating, not from fetches — the same method and the same definitions as the
frozen copy at ``protocol/tasks/PIG-001/evidence/asset-inventory-effa805.{md,json}``,
which this tool must reproduce for an unchanged tree.

"Unique asset" means a unique URL string. Distinct thumbnail widths of the
same Commons file count separately, so the number of unique underlying files
is slightly lower — ``tools/rights_register.py`` deduplicates to real files.

Usage:
    python3 tools/asset_inventory.py                        # print summary
    python3 tools/asset_inventory.py --out-json a.json --out-md a.md
    python3 tools/asset_inventory.py --compare protocol/tasks/PIG-001/evidence/asset-inventory-effa805.json

Standard library only.
"""
import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

URL = r"https://upload\.wikimedia\.org/[^\"'\s]+"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def catalog_images():
    """(pd_urls, copyright_records_with_url) from js/catalog-*.js.

    Each catalog work carries image:{ src, page, status }. status "pd" renders
    in the app (js/app.js gates on status === "pd"); status "copyright" is
    suppressed. Copyright records are counted so leakage can be measured.
    """
    pd, cw, copyright_refs = [], [], 0
    for path in sorted(glob.glob(os.path.join(ROOT, "js", "catalog-*.js"))):
        src = read(path)
        for block in re.findall(r"image:\s*\{(.*?)\}", src, re.S):
            m_src = re.search(r'src:\s*"(%s)"' % URL, block)
            m_status = re.search(r'status:\s*"([a-z]+)"', block)
            status = m_status.group(1) if m_status else ""
            if status == "pd" and m_src:
                pd.append(m_src.group(1))
            elif status == "copyright":
                copyright_refs += 1
                if m_src:
                    cw.append(m_src.group(1))
    return pd, cw, copyright_refs


def gallery_images():
    """Artist-page gallery images from js/artworks.js (window.ARTWORKS)."""
    src = read(os.path.join(ROOT, "js", "artworks.js"))
    data = json.loads(src.split("window.ARTWORKS = ", 1)[1].rstrip().rstrip(";\n").rstrip(";"))
    out = []
    for works in data.values():
        for entry in works.values():
            if entry.get("img", "").startswith("https://upload.wikimedia.org/"):
                out.append(entry["img"])
    return out


def museum_photos():
    src = read(os.path.join(ROOT, "js", "museums-1.js"))
    return re.findall(r'photo:\s*\{\s*src:\s*"(%s)"' % URL, src)


def prerender_refs():
    """og:image / twitter:image in the p/** prerendered stubs."""
    refs, files = [], sorted(glob.glob(os.path.join(ROOT, "p", "**", "*.html"), recursive=True))
    for path in files:
        refs += re.findall(r'content="(%s)"' % URL, read(path))
    return refs, len(files)


def homepage_refs():
    return re.findall(r'content="(%s)"' % URL, read(os.path.join(ROOT, "index.html")))


def build():
    pd, cw_urls, copyright_refs = catalog_images()
    gallery = gallery_images()
    museum = museum_photos()
    stubs, stub_files = prerender_refs()
    home = homepage_refs()

    surfaces = [
        ("Catalog artwork images (js/catalog-1..4.js, status:\"pd\")", "catalog_pd_rendered",
         pd, "rendered in app (gate: app.js status===\"pd\")"),
        ("Catalog copyright records (status:\"copyright\")", "catalog_copyright_suppressed",
         cw_urls, "no src field exists; nothing stored or rendered"),
        ("Artist-page galleries (js/artworks.js)", "gallery_rendered",
         gallery, "rendered in app"),
        ("Museum photos (js/museums-1.js photo.src)", "museum_photos_rendered",
         museum, "rendered in app"),
        ("Prerendered stub metadata (p/**, %d files, og:/twitter:image)" % stub_files,
         "prerender_metadata_refs", stubs, "public metadata references (crawlable regardless of app gating)"),
        ("Homepage metadata (index.html)", "homepage_metadata_refs",
         home, "public metadata reference"),
    ]

    rendered = set(pd) | set(gallery) | set(museum)
    metadata = set(stubs) | set(home)
    all_unique = rendered | metadata

    return {
        "surfaces": surfaces,
        "counts": {
            "copyright_refs": copyright_refs,
            "stub_files": stub_files,
            "total_unique": len(all_unique),
            "rendered_unique": len(rendered),
            "metadata_only_unique": len(metadata - rendered),
            "catalog_gallery_overlap": len(set(pd) & set(gallery)),
            "suppressed_leaking_into_metadata": len(set(cw_urls) & metadata),
        },
    }


def as_json(inv):
    return {key: sorted(set(urls)) for _, key, urls, _ in inv["surfaces"]}


def git_head():
    try:
        return subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=10).stdout.strip()[:7] or "unknown"
    except Exception:
        return "unknown"


def as_md(inv, head, json_name):
    c = inv["counts"]
    lines = [
        "# Pigment — Public Asset Inventory at %s" % head,
        "",
        "Enumerated %s by static analysis of the repository at %s" % (
            datetime.date.today().isoformat(), head),
        "(regenerate: `python3 tools/asset_inventory.py`; JSON detail in %s)." % json_name,
        '"Unique asset" means a unique upload.wikimedia.org URL string; distinct',
        "thumbnail widths of the same Commons file count separately, so unique",
        "underlying files may be slightly fewer. No network requests were made;",
        "reachability is derived from code gating, not fetches.",
        "",
        "## Exact counts by surface",
        "",
        "| Surface | References | Unique assets | Reachability |",
        "| --- | --- | --- | --- |",
    ]
    for label, key, urls, reach in inv["surfaces"]:
        refs = c["copyright_refs"] if key == "catalog_copyright_suppressed" else len(urls)
        lines.append("| %s | %d | %d | %s |" % (label, refs, len(set(urls)), reach))
    lines += [
        "",
        "## Cross-surface reconciliation",
        "",
        "- Total unique assets across all public surfaces: **%d**" % c["total_unique"],
        "- Rendered-in-app unique: **%d**; metadata-only (referenced but never rendered in app): **%d**"
        % (c["rendered_unique"], c["metadata_only_unique"]),
        "- Catalog∩gallery overlap: %d unique URLs appear on both surfaces" % c["catalog_gallery_overlap"],
        "- Copyright-suppressed URLs leaking into public stub metadata: **%d**"
        % c["suppressed_leaking_into_metadata"],
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-json")
    ap.add_argument("--out-md")
    ap.add_argument("--compare", help="frozen inventory JSON to diff against")
    args = ap.parse_args()

    inv = build()
    head = git_head()
    payload = as_json(inv)
    md = as_md(inv, head, os.path.basename(args.out_json or "asset-inventory.json"))
    print(md)

    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)
        print("wrote %s" % args.out_json)
    if args.out_md:
        with open(args.out_md, "w", encoding="utf-8") as f:
            f.write(md)
        print("wrote %s" % args.out_md)

    if args.compare:
        with open(args.compare, encoding="utf-8") as f:
            frozen = json.load(f)
        drift = 0
        print("\n## Comparison against %s\n" % args.compare)
        for key in sorted(set(frozen) | set(payload)):
            a, b = set(frozen.get(key, [])), set(payload.get(key, []))
            if a == b:
                print("  %-32s identical (%d)" % (key, len(a)))
            else:
                drift += 1
                print("  %-32s DRIFT  frozen=%d now=%d  +%d -%d"
                      % (key, len(a), len(b), len(b - a), len(a - b)))
                for u in sorted(b - a)[:5]:
                    print("      + %s" % u)
                for u in sorted(a - b)[:5]:
                    print("      - %s" % u)
        print("\n%s" % ("NO DRIFT — inventory reproduces the frozen copy" if not drift
                        else "%d surface(s) drifted" % drift))
        return 1 if drift else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
