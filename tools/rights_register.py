#!/usr/bin/env python3
"""Build Pigment's artwork rights register from Wikimedia Commons.

For every image URL on a chosen surface, this resolves the underlying Commons
file and records what Commons asserts about it: licence short name, licence
template, usage terms, author, credit, attribution requirement, origination
date, and — critically — the **Commons file page** (``descriptionurl``).

Why the file page matters: the shipped catalog's ``image.page`` field points at
an English Wikipedia *article*, which carries no licence statement whatsoever.
An article URL cannot support a rights claim. The register stores the real
``commons.wikimedia.org/wiki/File:...`` page alongside it, and reports when the
two disagree.

**This tool reaches no legal conclusion.** Per owner decision OD-5 it records
asserted basis, attribution obligation and residual uncertainty; a clearance
claim requires qualified review. Entries that could not be verified are
labelled ``unverified`` and stay that way — a timeout or a 429 is never
evidence that an asset lacks a licence.

Rate-limit discipline lives in tools/commons_rights.py: ≥0.25s between
requests, retry with backoff, transient failure is never a negative finding.

Usage:
    # smoke test — 8 catalog images, proves extmetadata comes back
    python3 tools/rights_register.py --surface catalog --limit 8

    # the real register (Seurat): the AC11 sample, written to the task record
    python3 tools/rights_register.py --surface sample \\
        --out-json protocol/tasks/PIG-001/evidence/rights-register.json \\
        --out-md   protocol/tasks/PIG-001/evidence/rights-register.md

Standard library only.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import commons_rights as cr                                   # noqa: E402
import asset_inventory as ai                                  # noqa: E402

ROOT = ai.ROOT


# ---------------------------------------------------------------- surfaces

def _catalog_records():
    """[{id, artist_id, title, src, page, status}] for status:"pd" catalog works."""
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "js", "catalog-*.js"))):
        src = ai.read(path)
        # Records are top-level object literals that begin at column 0 with
        # `{ id:"…"`. Slice between consecutive starts rather than trying to
        # brace-match a JS literal with a regex.
        starts = [m for m in re.finditer(r'^\{\s*id:\s*"([^"]+)"', src, re.M)]
        for i, m in enumerate(starts):
            end = starts[i + 1].start() if i + 1 < len(starts) else len(src)
            wid, body = m.group(1), src[m.start():end]
            img_block = re.search(r"image:\s*\{(.*?)\}", body, re.S)
            if not img_block:
                continue
            block = img_block.group(1)
            status = re.search(r'status:\s*"([a-z]+)"', block)
            m_src = re.search(r'src:\s*"(%s)"' % ai.URL, block)
            if not m_src or not status or status.group(1) != "pd":
                continue
            page = re.search(r'page:\s*"([^"]*)"', block)
            aid = re.search(r'artistId:\s*"([^"]+)"', body)
            title = re.search(r'title:\s*"([^"]*)"', body)
            tier = re.search(r'tier:\s*(\d+)', body)
            out.append({
                "id": wid,
                "tier": int(tier.group(1)) if tier else 0,
                "artist_id": aid.group(1) if aid else "",
                "title": title.group(1) if title else "",
                "surface": "catalog",
                "src": m_src.group(1),
                "declared_page": page.group(1) if page else "",
            })
    return out


def _gallery_records():
    src = ai.read(os.path.join(ROOT, "js", "artworks.js"))
    data = json.loads(src.split("window.ARTWORKS = ", 1)[1].rstrip().rstrip(";\n").rstrip(";"))
    out = []
    for aid, works in data.items():
        for title, entry in works.items():
            if entry.get("img", "").startswith("https://upload.wikimedia.org/"):
                out.append({"id": "%s::%s" % (aid, title), "artist_id": aid, "title": title,
                            "surface": "gallery", "src": entry["img"],
                            "declared_page": entry.get("page", "")})
    return out


def _museum_records():
    src = ai.read(os.path.join(ROOT, "js", "museums-1.js"))
    out = []
    for m in re.finditer(r'"([a-z0-9-]+)":\s*\{.*?photo:\s*\{\s*src:\s*"(%s)"\s*,\s*page:\s*"([^"]*)"'
                         % ai.URL, src, re.S):
        out.append({"id": m.group(1), "artist_id": "", "title": m.group(1),
                    "surface": "museum", "src": m.group(2), "declared_page": m.group(3)})
    return out


def sample_records():
    """The AC11 sample basis, per asset-inventory-effa805.md.

    Tier 1 ∪ daily pool (the 75 works with full pages, which is also the
    onboarding deck pool), plus every Matisse and Kahlo gallery record — the
    two cross-store inconsistencies OD-5 sends into the register — plus a
    stratified fill of gallery records to reach ≥100 total. Deterministic
    (sorted, strided), so two runs produce the same sample and the register
    is reproducible.
    """
    catalog = _catalog_records()
    gallery = _gallery_records()

    chosen, seen = [], set()

    def add(rec):
        key = (rec["surface"], rec["id"])
        if key not in seen:
            seen.add(key)
            chosen.append(rec)

    for r in sorted(catalog, key=lambda r: r["id"]):          # Tier 1 ∪ daily pool
        if r.get("tier") == 1:
            add(r)
    for r in sorted(gallery, key=lambda r: r["id"]):          # mandatory exposure cases
        if r["artist_id"] in ("henri-matisse", "frida-kahlo"):
            add(r)

    rest = sorted([r for r in gallery if ("gallery", r["id"]) not in seen], key=lambda r: r["id"])
    if len(chosen) < 100 and rest:
        stride = max(1, len(rest) // (100 - len(chosen)))
        for r in rest[::stride]:
            if len(chosen) >= 100:
                break
            add(r)
    return chosen


SURFACES = {
    "catalog": _catalog_records,
    "gallery": _gallery_records,
    "museum": _museum_records,
    "sample": sample_records,
    "all": lambda: _catalog_records() + _gallery_records() + _museum_records(),
}


# ---------------------------------------------------------------- register

UNRESOLVED = {"unverified", "missing", "no-metadata", "not-commons"}


def build_register(records, batch=50, progress=True):
    urls = [r["src"] for r in records]
    seen_files = len({cr.commons_file_title(u) for u in urls} - {None})

    def on_batch(start, n, status):
        if progress:
            print("  ... resolved %d files (%s)" % (start + n, status), flush=True)

    if progress:
        print("Resolving %d references / %d unique Commons files (≥%.2fs between requests)"
              % (len(urls), seen_files, cr.MIN_INTERVAL), flush=True)
    rights = cr.rights_for_urls(urls, batch=batch, on_batch=on_batch)

    out = []
    for r in records:
        got = rights.get(r["src"], {})
        status = got.get("status", "unverified")
        file_page = got.get("commons_file_page", "")
        entry = dict(r)
        entry.update({
            "commons_file_title": got.get("requested_title", cr.commons_file_title(r["src"]) or ""),
            "commons_file_page": file_page,
            "declared_page_is_commons_file_page": bool(file_page) and r["declared_page"] == file_page,
            "license_short_name": got.get("license_short_name", ""),
            "license": got.get("license", ""),
            "license_url": got.get("license_url", ""),
            "usage_terms": got.get("usage_terms", ""),
            "artist": got.get("artist", ""),
            "credit": got.get("credit", ""),
            "attribution": got.get("attribution", ""),
            "attribution_required": got.get("attribution_required", ""),
            "date_time_original": got.get("date_time_original", ""),
            "mime": got.get("mime", ""),
            "lookup_status": status,
            "lookup_reason": got.get("reason", ""),
            "verified_on": datetime.date.today().isoformat(),
            # Resolution language is deliberately blunt. "asserted" is the
            # strongest thing this tool may ever say; "cleared" is not in the
            # vocabulary, because no code can earn that word (OD-5).
            "resolution": ("asserted-by-commons" if status == "ok" and got.get("license_short_name")
                           else "unresolved"),
            "legal_conclusion": "none",
        })
        out.append(entry)
    return out


def summarize(reg):
    s = {
        "entries": len(reg),
        "asserted": sum(1 for e in reg if e["resolution"] == "asserted-by-commons"),
        "unresolved": sum(1 for e in reg if e["resolution"] == "unresolved"),
        "unverified_transient": sum(1 for e in reg if e["lookup_status"] == "unverified"),
        "missing": sum(1 for e in reg if e["lookup_status"] == "missing"),
        "attribution_required": sum(1 for e in reg if e["attribution_required"].lower() == "true"),
        "declared_page_wrong": sum(1 for e in reg if not e["declared_page_is_commons_file_page"]),
    }
    licences = {}
    for e in reg:
        if e["license_short_name"]:
            licences[e["license_short_name"]] = licences.get(e["license_short_name"], 0) + 1
    s["licences"] = dict(sorted(licences.items(), key=lambda kv: -kv[1]))
    return s


def as_md(reg, summary, surface):
    L = [
        "# Pigment — Artwork Rights Register (%s surface)" % surface,
        "",
        "Generated %s by `python3 tools/rights_register.py --surface %s`."
        % (datetime.date.today().isoformat(), surface),
        "",
        "**This register reaches no legal conclusion.** It records what Wikimedia",
        "Commons asserts about each file, and the Commons file page it asserts it",
        "on. Per owner decision OD-5 a clearance claim requires qualified review;",
        "nothing here is a clearance. Entries marked `unresolved` stay unresolved.",
        "An `unverified` lookup means the request failed — a timeout or a 429 is",
        "never evidence that an asset lacks a licence.",
        "",
        "## Summary",
        "",
        "| Measure | Count |",
        "| --- | --- |",
        "| Entries | %d |" % summary["entries"],
        "| Licence asserted by Commons | %d |" % summary["asserted"],
        "| Unresolved | %d |" % summary["unresolved"],
        "| — of which transient lookup failure (proves nothing) | %d |" % summary["unverified_transient"],
        "| — of which file reported missing by the API | %d |" % summary["missing"],
        "| Attribution required per Commons | %d |" % summary["attribution_required"],
        "| Entries whose shipped `page` is NOT the Commons file page | %d |" % summary["declared_page_wrong"],
        "",
        "### Asserted licences",
        "",
    ]
    if summary["licences"]:
        L += ["| Licence (Commons `LicenseShortName`) | Entries |", "| --- | --- |"]
        L += ["| %s | %d |" % (k, v) for k, v in summary["licences"].items()]
    else:
        L.append("_None asserted — every entry unresolved._")
    L += ["", "## Entries", "",
          "| Id | Surface | Commons file page | Licence | Author | Attribution required | Status |",
          "| --- | --- | --- | --- | --- | --- | --- |"]
    for e in reg:
        page = e["commons_file_page"] or "—"
        L.append("| `%s` | %s | %s | %s | %s | %s | %s |" % (
            e["id"], e["surface"], page,
            e["license_short_name"] or "—",
            (e["artist"] or "—")[:60],
            e["attribution_required"] or "—",
            e["resolution"] if e["lookup_status"] == "ok" else "%s (%s)" % (e["resolution"], e["lookup_status"]),
        ))
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--surface", default="sample", choices=sorted(SURFACES))
    ap.add_argument("--limit", type=int, default=0, help="cap entries (smoke runs)")
    ap.add_argument("--batch", type=int, default=50, help="titles per API request (max 50)")
    ap.add_argument("--out-json")
    ap.add_argument("--out-md")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    records = SURFACES[args.surface]()
    if args.limit:
        records = records[:args.limit]
    if not records:
        print("no records on surface %r" % args.surface, file=sys.stderr)
        return 2

    reg = build_register(records, batch=args.batch, progress=not args.quiet)
    summary = summarize(reg)
    md = as_md(reg, summary, args.surface)
    print("\n" + md)

    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump({"generated": datetime.date.today().isoformat(),
                       "surface": args.surface, "summary": summary, "entries": reg},
                      f, ensure_ascii=False, indent=1)
        print("wrote %s" % args.out_json)
    if args.out_md:
        with open(args.out_md, "w", encoding="utf-8") as f:
            f.write(md)
        print("wrote %s" % args.out_md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
