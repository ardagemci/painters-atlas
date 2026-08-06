#!/usr/bin/env python3
"""Resolve museum building photographs that have no rights record yet.

`protocol/tasks/PIG-001/evidence/museum-photo-rights.json` (the Data Steward's
census) covers the 103 photographs that existed when it was run. Museum notes
keep being added, and a photograph with no credit record is exactly the licence
breach this work exists to close — `tools/validate.jxa.js` now fails the build
when one appears.

This tool is the top-up: it reads every `photo:{src,page}` in `js/museums-1.js`,
subtracts the venues already covered by the base census, resolves the remainder
against Commons, and writes them to a supplement file that
`tools/build_photo_credits.py` merges on top of the base. The base census is
never modified — it belongs to the audit that produced it.

Usage:
    python3 tools/audit_museum_photo_rights.py          # top up what is missing
    python3 tools/audit_museum_photo_rights.py --all    # re-resolve everything

Then regenerate the shipped registry:
    python3 tools/build_photo_credits.py

Stdlib only, plus tools/commons_rights.py. Records what Commons asserts; claims
no legal clearance (OD-5). A failed lookup is recorded as unverified, never as
a clean result.
"""

import argparse
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import commons_rights as cr  # noqa: E402

MUSEUMS_JS = os.path.join(ROOT, "js", "museums-1.js")
EVIDENCE = os.path.join(ROOT, "protocol", "tasks", "PIG-001", "evidence")
BASE = os.path.join(EVIDENCE, "museum-photo-rights.json")
SUPPLEMENT = os.path.join(EVIDENCE, "museum-photo-rights-supplement.json")

NOTE_RE = re.compile(r'^"([a-z0-9-]+)":\s*\{', re.M)
SRC_RE = re.compile(r'photo:\s*\{\s*src:"([^"]+)"')
PAGE_RE = re.compile(r'photo:\s*\{[^}]*?page:"([^"]+)"', re.S)


def note_photos():
    """{venue_id: {src, page}} for every museum note that carries a photograph."""
    text = open(MUSEUMS_JS, "r", encoding="utf-8").read()
    marks = list(NOTE_RE.finditer(text))
    out = {}
    for i, m in enumerate(marks):
        block = text[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(text)]
        src = SRC_RE.search(block)
        if not src:
            continue
        page = PAGE_RE.search(block)
        out[m.group(1)] = {"src": src.group(1), "page": page.group(1) if page else ""}
    return out


def covered(path):
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as fh:
        return {e.get("venue_id") for e in json.load(fh).get("entries", [])}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true",
                    help="re-resolve every museum photograph, not just uncovered ones")
    ap.add_argument("--out", default=SUPPLEMENT)
    args = ap.parse_args()

    photos = note_photos()
    known = set() if args.all else covered(BASE)
    todo = {vid: p for vid, p in photos.items() if vid not in known}
    if not todo:
        sys.stderr.write("every museum photograph already has a rights record (%d covered)\n"
                         % len(photos))
        return 0

    sys.stderr.write("resolving %d uncovered museum photograph(s): %s\n"
                     % (len(todo), ", ".join(sorted(todo))))
    resolved = cr.rights_for_urls([p["src"] for p in todo.values()])

    entries, unverified = [], 0
    for vid in sorted(todo):
        p = todo[vid]
        rec = resolved.get(p["src"]) or {"status": "unverified"}
        if rec.get("status") != "ok":
            unverified += 1
        required = rec.get("attribution_required", "")
        if not required:
            tpl = (rec.get("license") or "").lower()
            required = "false" if tpl in ("pd", "cc0", "") else "true"
        entries.append({
            "venue_id": vid,
            "src": p["src"],
            "page": p["page"],
            "commons_title": rec.get("requested_title", ""),
            "fetch_status": rec.get("status", "unverified"),
            "license_short": rec.get("license_short_name", ""),
            "license_tpl": rec.get("license", ""),
            "license_url": rec.get("license_url", ""),
            "author": cr.strip_html(rec.get("artist", "")),
            "credit": cr.strip_html(rec.get("credit", "")),
            "attribution": cr.strip_html(rec.get("attribution", "")),
            "attribution_required": required,
            "commons_file_page": rec.get("commons_file_page", ""),
            "usage_terms": rec.get("usage_terms", ""),
            "legal_conclusion": "none",
            "attribution_gap": required == "true",
        })

    doc = {
        "generated": datetime.date.today().isoformat(),
        "author": "Durer (claude-implementation-lead), PIG-001 build unit 24",
        "source": "js/museums-1.js photo{src,page}",
        "method": ("Commons API extmetadata via tools/commons_rights.py; a transient "
                   "failure is recorded as unverified, never as a negative finding"),
        "scope_note": ("Supplement only — museum photographs added after the base census "
                       "in museum-photo-rights.json, which this file never modifies. "
                       "tools/build_photo_credits.py merges this on top of the base."),
        "legal_conclusion": "none",
        "totals": {
            "photos": len(entries),
            "resolved_ok": len(entries) - unverified,
            "unverified": unverified,
            "attribution_required": sum(1 for e in entries if e["attribution_gap"]),
        },
        "entries": entries,
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    sys.stderr.write("wrote %s (%d entries, %d requiring attribution, %d unverified)\n"
                     % (args.out, len(entries), doc["totals"]["attribution_required"], unverified))
    for e in entries:
        sys.stderr.write("  %-32s %-16s %s\n" % (e["venue_id"], e["license_short"], e["author"][:40]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
