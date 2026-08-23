#!/usr/bin/env python3
"""Census: does every public-domain catalog image cite a Commons file page?

Pigment's rights basis for an image is what Commons asserts on that file's
page. 257 of 282 records instead cite an `en.wikipedia.org` article, and a
Wikipedia article carries no licence statement at all — so for those records
the basis is unverifiable from what the site ships. `PIGMENT.md` §14 and owner
decision OD-5 both turn on this.

This exists because W-004 proposes to rewrite those 257 values, and a writ that
changes production data needs something that can say whether it did so
correctly. Report-only by default; `--require-commons` turns it into a gate.

    python3 tools/check_image_pages.py                    # census, exits 0
    python3 tools/check_image_pages.py --require-commons  # exits 1 if any remain
    python3 tools/check_image_pages.py --against <register.json>
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMONS_FILE_PAGE = re.compile(
    r"^https://commons\.wikimedia\.org/wiki/File:", re.I)

# A catalog record opens a line: `{ id:"the-calling-of-saint-matthew", tier:1,`
# Anchored to that, NOT to any `id:` — because `museum:{ id:"..." }` sits
# between the artwork id and its image block, so an unanchored match returns
# the museum's id for every record. The counts were identical either way, which
# is exactly why that bug survived until a sample was printed: 282 and 257 were
# right while every id attached to them was wrong.
RECORD = re.compile(
    r'^\{\s*id:\s*"([a-z0-9-]+)"(?P<body>.*?)(?=^\{\s*id:\s*"|\Z)', re.S | re.M)
IMAGE = re.compile(
    r'image:\s*\{(?P<img>[^{}]*)\}', re.S)
FIELD = re.compile(r'(\w+)\s*:\s*"([^"]*)"')


def catalog_files():
    """Discovered, never listed — the C2 lesson. A catalog-6.js added later is
    picked up here without anyone remembering to edit this file."""
    files = [p for p in (ROOT / "js").glob("catalog-*.js")]
    return sorted(files, key=lambda p: int(re.search(r"\d+", p.name).group()))


def records():
    for path in catalog_files():
        text = path.read_text(encoding="utf-8")
        for match in RECORD.finditer(text):
            body = match.group("body")
            image = IMAGE.search(body)
            if not image:
                continue
            fields = dict(FIELD.findall(image.group("img")))
            if not fields.get("src"):
                continue
            yield {"id": match.group(1), "file": path.name,
                   "page": fields.get("page", ""),
                   "status": fields.get("status", "")}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--require-commons", action="store_true",
                   help="exit 1 if any pd record cites a non-Commons page")
    p.add_argument("--against", help="a W-003 register JSON to cross-check "
                                     "the record count against")
    p.add_argument("--list", action="store_true", help="print every offender")
    args = p.parse_args(argv)

    pd = [r for r in records() if r["status"] == "pd"]
    good = [r for r in pd if COMMONS_FILE_PAGE.match(r["page"])]
    bad = [r for r in pd if not COMMONS_FILE_PAGE.match(r["page"])]

    print("public-domain catalog images: %d" % len(pd))
    print("  cite a Commons file page:   %d" % len(good))
    print("  cite something else:        %d" % len(bad))

    if args.list:
        for r in bad:
            print("    %-38s %s  %s" % (r["id"], r["file"], r["page"][:70]))

    # A parser that silently reads fewer records than exist would report a
    # falsely clean census. Cross-check against a register that counted them
    # independently, rather than trusting this file's own regex.
    if args.against:
        try:
            expected = json.load(open(args.against))["summary"]["entries"]
        except Exception as error:
            print("cannot read register: %s" % error, file=sys.stderr)
            return 2
        if expected != len(pd):
            print("MISMATCH: register counted %d pd entries, this parser found %d"
                  % (expected, len(pd)), file=sys.stderr)
            return 2
        print("  cross-checked against register: %d, agrees" % expected)

    if args.require_commons and bad:
        print("\n%d record(s) still cite a page that is not a Commons file page."
              % len(bad), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
