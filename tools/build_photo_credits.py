#!/usr/bin/env python3
"""Generate `js/photo-credits.js` — the shipped attribution registry.

The rights evidence lives under `protocol/`, which is never served to users, so
none of it can satisfy a licence term on its own. This tool turns that evidence
into a normal Pigment data file: a global registry, loaded by `index.html`,
read by `js/app.js` to render credit next to the image it belongs to.

Inputs (both under protocol/tasks/PIG-001/evidence/):
    museum-photo-rights.json   — museum building photographs, keyed by venue
                                 (topped up by museum-photo-rights-supplement.json,
                                 written by tools/audit_museum_photo_rights.py)
    artwork-image-rights.json  — census of every shipped artwork image
                                 (produced by tools/audit_artwork_rights.py)

Output (js/photo-credits.js), two registries:
    window.PHOTO_CREDITS  { venueId: credit }      — every museum photograph
    window.IMAGE_CREDITS  { "File:…": credit }     — artwork images that require
                                                     credit, keyed by Commons title

Shipped payload is deliberately narrow: author, licence short name, licence
deed URL, Commons file page, and whether attribution is actually required.
Audit-only fields (usage terms, fetch status, verification dates) stay in the
evidence file.

Every text field is reduced to plain text here, at build time, so no Commons
HTML can ever reach a page: `Artist`/`Credit` arrive from the API as HTML
fragments full of anchors and `<span class="int-own-work">` wrappers.
`js/app.js` escapes on output as well — this is the first of the two passes,
not a substitute for the second.

Re-run whenever a photograph changes, then bump the `?v=` string in index.html:
    python3 tools/build_photo_credits.py

Stdlib only; no network. Regenerating from a fixed input is deterministic.
"""

import argparse
import datetime
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE = os.path.join(ROOT, "protocol", "tasks", "PIG-001", "evidence")
MUSEUM_IN = os.path.join(EVIDENCE, "museum-photo-rights.json")
# optional top-up for photographs added after the base census — written by
# tools/audit_museum_photo_rights.py, merged on top of the base by venue id
MUSEUM_SUPPLEMENT = os.path.join(EVIDENCE, "museum-photo-rights-supplement.json")
ARTWORK_IN = os.path.join(EVIDENCE, "artwork-image-rights.json")
DEFAULT_OUT = os.path.join(ROOT, "js", "photo-credits.js")

# Commons' placeholder for a file whose author was inferred from the upload:
#   "No machine-readable author provided. Foo assumed (based on copyright claims)."
ASSUMED_RE = re.compile(
    r"^No machine-readable author provided\.\s*(.+?)\s+assumed\s*\(based on copyright claims\)\.?$",
    re.I,
)
# Commons authors are written freehand, so many arrive already labelled:
# "Photo: Andreas Praefcke", "Photograph by Mike Peel (www.mikepeel.net)." The
# renderer supplies its own label, so strip theirs rather than print both.
LABEL_RE = re.compile(r"^(photo|photograph|picture|image)\s*(?::|\bby\b)\s*", re.I)


def plain(value):
    """Commons text → plain text: no markup, no entities, no runs of whitespace."""
    if not value:
        return ""
    s = str(value)
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = s.replace("‎", "").replace("‏", "")     # bidi marks from <bdi>
    return re.sub(r"\s+", " ", s).strip()


def author_of(record, *fields):
    """Best plain-text author name available, in the order the fields are given."""
    for f in fields:
        name = plain(record.get(f, ""))
        if not name:
            continue
        m = ASSUMED_RE.match(name)
        if m:
            name = m.group(1).strip()
        name = LABEL_RE.sub("", name).strip()
        name = re.sub(r"\.$", "", name).strip()      # trailing full stop, not part of a name
        if not name or name.lower() in ("unknown", "unknown author", "anonymous"):
            continue
        return name
    return ""


def js_string(s):
    """A JS double-quoted string literal — escaped for JS, not for HTML."""
    out = json.dumps(s, ensure_ascii=False)
    # keep the generated file safe inside a <script> element
    return out.replace("</", '<\\/')


def credit_literal(entry):
    """One registry value, emitted as a compact JS object literal."""
    parts = []
    if entry["author"]:
        parts.append("author:" + js_string(entry["author"]))
    parts.append("license:" + js_string(entry["license"]))
    if entry["licenseUrl"]:
        parts.append("licenseUrl:" + js_string(entry["licenseUrl"]))
    if entry["page"]:
        parts.append("page:" + js_string(entry["page"]))
    if entry["required"]:
        parts.append("required:true")
    return "{ " + ", ".join(parts) + " }"


def load(path, label):
    if not os.path.exists(path):
        sys.exit("missing %s input: %s" % (label, path))
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def museum_credits(doc, supplement=None):
    merged = {}
    for src in (doc, supplement or {}):
        for e in src.get("entries", []):
            if e.get("venue_id"):
                merged[e["venue_id"]] = e          # supplement wins on collision
    out = []
    for vid in merged:
        e = merged[vid]
        out.append((vid, {
            "author": author_of(e, "author", "attribution"),
            "license": plain(e.get("license_short", "")) or "Unstated",
            "licenseUrl": plain(e.get("license_url", "")),
            "page": plain(e.get("commons_file_page", "")) or plain(e.get("page", "")),
            "required": str(e.get("attribution_required", "")).lower() == "true",
        }))
    out.sort(key=lambda kv: kv[0])
    return out


def image_credits(doc):
    """Only images that actually carry an obligation — the lean-payload rule."""
    seen, out = set(), []
    for e in doc.get("entries", []):
        if not e.get("credit_required"):
            continue
        title = e.get("commons_title") or ""
        if not title or title in seen:
            continue
        seen.add(title)
        out.append((title, {
            "author": author_of(e, "author", "attribution", "credit"),
            "license": plain(e.get("license_short", "")) or "Unstated",
            "licenseUrl": plain(e.get("license_url", "")),
            "page": plain(e.get("commons_file_page", "")),
            "required": True,
        }))
    out.sort(key=lambda kv: kv[0])
    return out


HEADER = '''/* Pigment photo credits — GENERATED FILE, do not edit by hand.
   Regenerate with:  python3 tools/build_photo_credits.py
   Sources: protocol/tasks/PIG-001/evidence/museum-photo-rights.json
            protocol/tasks/PIG-001/evidence/artwork-image-rights.json
   Generated: %(date)s

   Two registries, both read by js/app.js:

   window.PHOTO_CREDITS — museum building photographs, keyed by venue id
     (js/venues.js). One entry per photograph in js/museums-1.js. %(mus_total)d
     entries, %(mus_req)d of which carry a licence requiring attribution; the
     other %(mus_free)d are public-domain or CC0 and are credited as a courtesy.

   window.IMAGE_CREDITS — artwork images that require attribution, keyed by
     Commons file title as derived from the image URL (see commonsTitle() in
     js/app.js). %(img_req)d entries. Public-domain and CC0 images are
     deliberately absent: they carry no obligation, and the existing
     "image via Wikimedia Commons" source link already names their origin.

   Credit shape: { author, license, licenseUrl, page, required }
     author      photographer / uploader, plain text (may be absent)
     license     licence short name, e.g. "CC BY-SA 4.0"
     licenseUrl  licence deed (absent for public-domain files, which have none)
     page        Commons file page — the "source" half of TASL
     required    true when the licence requires attribution

   All text is plain — Commons markup is stripped at build time — and js/app.js
   escapes it again on output. This file asserts no legal clearance (OD-5); it
   records what Commons asserts. */
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    supplement = None
    if os.path.exists(MUSEUM_SUPPLEMENT):
        with open(MUSEUM_SUPPLEMENT, "r", encoding="utf-8") as fh:
            supplement = json.load(fh)
    museums = museum_credits(load(MUSEUM_IN, "museum"), supplement)
    images = image_credits(load(ARTWORK_IN, "artwork"))

    mus_req = sum(1 for _, c in museums if c["required"])
    body = [HEADER % {
        "date": datetime.date.today().isoformat(),
        "mus_total": len(museums),
        "mus_req": mus_req,
        "mus_free": len(museums) - mus_req,
        "img_req": len(images),
    }]

    body.append("window.PHOTO_CREDITS = {")
    body.append(",\n".join('%s: %s' % (js_string(k), credit_literal(v)) for k, v in museums))
    body.append("};\n")

    body.append("window.IMAGE_CREDITS = {")
    body.append(",\n".join('%s: %s' % (js_string(k), credit_literal(v)) for k, v in images))
    body.append("};")

    text = "\n".join(body) + "\n"
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(text)

    missing_author = [k for k, v in museums if not v["author"]]
    sys.stderr.write("wrote %s (%d bytes)\n" % (args.out, len(text.encode("utf-8"))))
    sys.stderr.write("  PHOTO_CREDITS: %d venues (%d require attribution, %d free)\n"
                     % (len(museums), mus_req, len(museums) - mus_req))
    sys.stderr.write("  IMAGE_CREDITS: %d artwork images requiring attribution\n" % len(images))
    if missing_author:
        sys.stderr.write("  note: no author recorded for %d venue photo(s): %s\n"
                         % (len(missing_author), ", ".join(missing_author)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
