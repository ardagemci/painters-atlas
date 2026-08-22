#!/usr/bin/env python3
"""Resolve every *shipped* artwork image against Wikimedia Commons.

Why this exists
---------------
`protocol/tasks/PIG-001/evidence/rights-register.md` examined a 122-record
*sample* of artwork images and reported two attribution-required files still
shipped. A sample cannot answer "does anything we ship still need credit?" —
only a census can. This tool is the census: it reads every image URL that the
shipped data files actually contain, resolves each one to its Commons file,
and records the licence Commons asserts.

Scope, stated precisely:
  * `js/catalog-{1..5}.js`  — `image:{ src, page, status }`; only `status:"pd"`
    records are read, because `js/app.js` renders an artwork image only when
    `w.image.status === "pd"`. A `status:"copyright"` record ships no image.
  * `js/artworks.js`        — `window.ARTWORKS[artistId][title].img`, the
    artist-page gallery registry.

Output: `protocol/tasks/PIG-001/evidence/artwork-image-rights.json`, the
machine-readable input to `tools/build_photo_credits.py`.

This is not a legal clearance and does not claim to be one (OD-5). It records
what Commons asserts, and where each file is used. A network failure is
recorded as `unverified` — never silently as a clean result.

Usage:
    python3 tools/audit_artwork_rights.py [--out PATH]

Stdlib only, plus tools/commons_rights.py (also stdlib).
"""

import argparse
import collections
import json
import glob
import os
import re
import sys
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import commons_rights as cr  # noqa: E402  (path set above)

# C2. Discovered, not listed. This file named the catalogs explicitly, so a new
# catalog-6.js would have been audited by some tools and silently skipped by the
# rights audit — the place a miss is least visible.
CATALOG_FILES = [os.path.basename(p) for p in sorted(
    glob.glob(os.path.join(ROOT, "js", "catalog-*.js")),
    key=lambda p: int(re.search(r"catalog-(\d+)", p).group(1)))]
GALLERY_FILE = "artworks.js"
DEFAULT_OUT = os.path.join(
    ROOT, "protocol", "tasks", "PIG-001", "evidence", "artwork-image-rights.json"
)

# image:{ src:"…", …, status:"pd" } — the status is what gates rendering in app.js
CATALOG_RE = re.compile(r'image:\{\s*src:"([^"]+)"[^}]*?status:"([a-z]+)"', re.S)
GALLERY_RE = re.compile(r'"img":\s*"([^"]+)"')


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def shipped_image_urls():
    """{url: [where, …]} for every image the app can actually render."""
    urls = collections.OrderedDict()

    def add(url, where):
        urls.setdefault(url, [])
        if where not in urls[url]:
            urls[url].append(where)

    for name in CATALOG_FILES:
        path = os.path.join(ROOT, "js", name)
        if not os.path.exists(path):
            continue
        for src, status in CATALOG_RE.findall(read(path)):
            if status == "pd":                     # the only status app.js renders
                add(src, "js/" + name)

    gallery = os.path.join(ROOT, "js", GALLERY_FILE)
    if os.path.exists(gallery):
        for src in GALLERY_RE.findall(read(gallery)):
            add(src, "js/" + GALLERY_FILE)

    return urls


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    urls = shipped_image_urls()
    sys.stderr.write("resolving %d shipped image URLs against Commons…\n" % len(urls))

    resolved = cr.rights_for_urls(list(urls.keys()))

    entries, by_licence = [], collections.Counter()
    unverified = 0
    for url, where in urls.items():
        rec = resolved.get(url) or {"status": "unverified"}
        status = rec.get("status", "unverified")
        if status != "ok":
            unverified += 1
        licence = rec.get("license_short_name", "")
        by_licence[licence or ("[" + status + "]")] += 1
        entries.append({
            "src": url,
            "used_in": where,
            "commons_title": rec.get("requested_title", ""),
            "commons_file_page": rec.get("commons_file_page", ""),
            "fetch_status": status,
            "license_short": licence,
            "license_tpl": rec.get("license", ""),
            "license_url": rec.get("license_url", ""),
            "author": cr.strip_html(rec.get("artist", "")),
            "credit": cr.strip_html(rec.get("credit", "")),
            "attribution": cr.strip_html(rec.get("attribution", "")),
            "attribution_required": rec.get("attribution_required", ""),
            "usage_terms": rec.get("usage_terms", ""),
            "legal_conclusion": "none",
        })

    # A file needs credit when Commons says so, or when its licence template is
    # anything other than a public-domain / CC0 dedication. Both tests, because
    # extmetadata's own flag has been observed to be absent on some files.
    def needs_credit(e):
        tpl = (e["license_tpl"] or "").lower()
        return e["attribution_required"] == "true" or (
            e["fetch_status"] == "ok" and tpl not in ("pd", "cc0", "")
        )

    required = [e for e in entries if needs_credit(e)]
    for e in entries:
        e["credit_required"] = needs_credit(e)

    doc = {
        "generated": datetime.date.today().isoformat(),
        "author": "Durer (claude-implementation-lead), PIG-001 build unit 24",
        "source": "js/catalog-{1..5}.js image{src,status:pd} + js/artworks.js img",
        "method": (
            "Commons API extmetadata via tools/commons_rights.py; deduplicated by "
            "underlying Commons file; a transient failure is recorded as "
            "unverified and never as a clean result"
        ),
        "scope_note": (
            "Census of every renderable shipped artwork image, not a sample. "
            "Supersedes the coverage (not the conclusions) of the 122-record "
            "sample in rights-register.json for the question 'what still needs "
            "credit?'"
        ),
        "legal_conclusion": "none",
        "totals": {
            "images": len(entries),
            "resolved_ok": len(entries) - unverified,
            "unverified": unverified,
            "credit_required": len(required),
            "no_obligation": len(entries) - len(required),
            "by_licence": dict(sorted(by_licence.items())),
        },
        "entries": entries,
    }

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    sys.stderr.write("wrote %s\n" % args.out)
    sys.stderr.write("  %d images, %d need credit, %d unverified\n"
                     % (len(entries), len(required), unverified))
    for lic, n in sorted(by_licence.items(), key=lambda kv: -kv[1]):
        sys.stderr.write("  %-18s %d\n" % (lic, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
