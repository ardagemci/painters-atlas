"""Batch 21's integration contract, with independent synthetic negative controls.

Run: python3 -m unittest discover -s tests -p 'test_artist_batch_21.py'
The integration checks intentionally fail with actionable errors before Claude's
artists-21/artworks/stub integration. Missing records do not short-circuit the
image, identity, or claim checks. JXA executes the real global registries.
"""
import copy
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {"life", "career", "outside", "facts", "tagline"}
LICENSES = {"Public domain", "CC0", "PDM-owner"}


def canonical_commons_filename(url):
    """Decode the ORIGINAL filename, never the resized thumbnail's filename."""
    if not isinstance(url, str):
        return None
    parts = urlsplit(url)
    if parts.netloc != "upload.wikimedia.org":
        return None
    match = re.match(r"^/wikipedia/commons/(?:thumb/)?[0-9a-f]/[0-9a-f]{2}/([^/]+)(?:/|$)", parts.path)
    return unquote(match.group(1)) if match else None


def check_wiring(evidence, records, definitions, index_html, stubs, sitemap):
    """Check executed records and their per-file provenance plus published routes."""
    errors = []
    by_id = {r.get("id"): r for r in records}
    script = re.search(r'<script\b[^>]*\bsrc\s*=\s*[\"\']js/artists-21\.js(?:\?[^\"\']*)?[\"\'][^>]*>',
                       index_html, re.I)
    if not script:
        errors.append("script: index.html does not register js/artists-21.js")
    for aid in evidence:
        if aid not in by_id:
            errors.append(f"record: {aid} is missing from ARTISTS")
        if "js/artists-21.js" not in definitions.get(aid, []):
            errors.append(f"definition: {aid} is not defined in js/artists-21.js")
        if aid not in stubs:
            errors.append(f"stub: p/artist/{aid}.html is missing")
        if not re.search(r"artist/" + re.escape(aid) + r"(?:\.html)?(?:[<#?\s]|$)", sitemap):
            errors.append(f"sitemap: artist/{aid} is missing")
    return errors


def check_works(evidence, records, artworks):
    """The evidence is the ordered title/date and exact image/page contract."""
    errors = []
    by_id = {r.get("id"): r for r in records}
    for aid, sheet in evidence.items():
        works = sheet.get("works", [])
        expected = [(w.get("t"), w.get("y")) for w in works]
        record = by_id.get(aid)
        if record is not None:
            actual = [(w.get("t"), w.get("y")) for w in record.get("works", [])]
            if actual != expected:
                errors.append(f"works: {aid} titles/dates/order differ from evidence")
        gallery = artworks.get(aid, {})
        for work in works:
            title = work.get("t")
            image = work.get("image")
            label = f"{aid} / {title}"
            if image is None:
                reason = work.get("no_image_reason")
                if not isinstance(reason, str) or not reason.strip():
                    errors.append(f"no_image_reason: {label} needs a reason")
                if title in gallery:
                    errors.append(f"unexpected_image: {label} has no image in evidence")
            else:
                if image.get("license_short_name") not in LICENSES:
                    errors.append(f"license: {label} has an unaccepted source label")
                entry = gallery.get(title)
                if not isinstance(entry, dict):
                    errors.append(f"image_entry: {label} is missing from ARTWORKS")
                    continue
                for key in ("img", "page"):
                    if entry.get(key) != image.get(key):
                        errors.append(f"{key}_mismatch: {label} differs from evidence")
        for title in gallery:
            if title not in {w.get("t") for w in works}:
                errors.append(f"extra_artwork: {aid} / {title} is absent from evidence")
    return errors


def check_work_ids(evidence):
    errors = []
    for aid, sheet in evidence.items():
        seen, illustrated = set(), set()
        for work in sheet.get("works", []):
            wid = work.get("work_id")
            if not isinstance(wid, str) or not wid.strip():
                errors.append(f"work_id: {aid} / {work.get('t')} needs an identity")
                continue
            if wid in seen:
                errors.append(f"duplicate_work_id: {aid} repeats {wid}")
            seen.add(wid)
            if work.get("image") is not None:
                illustrated.add(wid)
        if len(illustrated) < 2:
            errors.append(f"distinct_works: {aid} has fewer than 2 distinct illustrated work_ids")
    return errors


def check_filenames(artworks):
    """Every registry entry participates, including artists outside the batch."""
    errors, owners = [], {}
    for aid, gallery in artworks.items():
        for title, entry in gallery.items():
            url = entry.get("img")
            if not url:
                continue
            filename = canonical_commons_filename(url)
            if filename is None:
                errors.append(f"commons_filename: {aid} / {title} has an unrecognised img URL")
                continue
            owner = f"{aid} / {title}"
            if filename in owners:
                errors.append(f"duplicate_filename: {filename}: {owners[filename]} and {owner}")
            else:
                owners[filename] = owner
    return errors


def check_claims(evidence):
    errors = []
    for aid, sheet in evidence.items():
        claims = sheet.get("claims", [])
        if not isinstance(claims, list):
            errors.append(f"claims: {aid} must have a claims array")
            continue
        if len(claims) < 8:
            errors.append(f"claim_count: {aid} has fewer than 8 claims")
        for i, claim in enumerate(claims):
            if not isinstance(claim, dict):
                errors.append(f"claim_shape: {aid} claim {i} is not an object")
                continue
            if claim.get("field") not in FIELDS:
                errors.append(f"claim_field: {aid} claim {i} has an invalid field")
            url = claim.get("source_url")
            if not isinstance(url, str) or not url.startswith("https://"):
                errors.append(f"claim_url: {aid} claim {i} needs an https:// source")
            for key in ("claim", "note"):
                value = claim.get(key)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"claim_{key}: {aid} claim {i} needs non-empty {key}")
    return errors


def load_registries():
    paths = [ROOT / "js/taxonomy.js"]
    paths += sorted((ROOT / "js").glob("artists-*.js"), key=lambda p: int(p.stem.split("-")[-1]))
    paths += [ROOT / "js/artworks.js"]
    script = r'''
ObjC.import("Foundation");
function read(p) { return ObjC.unwrap($.NSString.stringWithContentsOfFileEncodingError(p, $.NSUTF8StringEncoding, null)); }
var window = {}, definitions = {};
%s.forEach(function(p) {
    var before = (window.ARTISTS || []).length;
    eval(read(p));
    if (/\/artists-\d+\.js$/.test(p)) {
        (window.ARTISTS || []).slice(before).forEach(function(a) {
            (definitions[a.id] || (definitions[a.id] = [])).push("js/" + p.split("/").pop());
        });
    }
});
JSON.stringify({records: window.ARTISTS || [], artworks: window.ARTWORKS || {}, definitions: definitions,
    taxonomy: {nations: window.NATIONS, eras: window.ERAS, movements: window.MOVEMENTS, techniques: window.TECHNIQUES}});
''' % json.dumps([str(p) for p in paths])
    with tempfile.NamedTemporaryFile("w", suffix=".jxa.js", delete=False) as f:
        f.write(script)
        path = Path(f.name)
    try:
        out = subprocess.run(["osascript", "-l", "JavaScript", str(path)],
                             capture_output=True, text=True, timeout=120)
    finally:
        path.unlink(missing_ok=True)
    if out.returncode:
        raise AssertionError("JXA registry loader failed: " + (out.stderr or out.stdout))
    return json.loads(out.stdout.strip())


class TestBatch21Integration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = {p.stem: json.loads(p.read_text(encoding="utf-8"))
                        for p in sorted((ROOT / "docs/roster-batch-21").glob("*.json"))
                        if not p.name.startswith("_")}
        cls.data = load_registries()

    def assert_clean(self, errors):
        self.assertFalse(errors, "\n" + "\n".join(errors))

    def test_evidence_inventory(self):
        self.assertEqual(len(self.evidence), 20, "batch 21 must contain twenty evidence sheets")
        for aid, sheet in self.evidence.items():
            self.assertEqual(sheet.get("id"), aid)

    def test_published_records_and_routes(self):
        stubs = {p.stem for p in (ROOT / "p/artist").glob("*.html")}
        self.assert_clean(check_wiring(self.evidence, self.data["records"], self.data["definitions"],
                                      (ROOT / "index.html").read_text(), stubs,
                                      (ROOT / "sitemap.xml").read_text()))

    def test_ordered_works_and_exact_images(self):
        self.assert_clean(check_works(self.evidence, self.data["records"], self.data["artworks"]))

    def test_distinct_work_identities(self):
        self.assert_clean(check_work_ids(self.evidence))

    def test_canonical_filenames_across_whole_registry(self):
        self.assert_clean(check_filenames(self.data["artworks"]))

    def test_claim_evidence(self):
        self.assert_clean(check_claims(self.evidence))


def valid_fixture():
    """A complete small batch that passes every pure checker before mutation."""
    def image(filename):
        return {"img": f"https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/{filename}/500px-{filename}",
                "page": f"https://commons.wikimedia.org/wiki/File:{filename}", "license_short_name": "Public domain"}
    works = [{"t": "First", "y": "1900", "work_id": "object:1", "image": image("First_work.jpg")},
             {"t": "Second", "y": "1901", "work_id": "object:2", "image": image("Second.jpg")},
             {"t": "Unpictured", "y": "1902", "work_id": "object:3", "image": None,
              "no_image_reason": "No matching Commons image found."}]
    evidence = {"fixture": {"id": "fixture", "works": works, "claims": [
        {"field": "life", "claim": f"Documented fact {i}", "source_url": "https://example.org/source",
         "note": 'Source records “supporting words”.'} for i in range(8)]}}
    records = [{"id": "fixture", "works": [{"t": w["t"], "y": w["y"]} for w in works]}]
    artworks = {"fixture": {w["t"]: {k: w["image"][k] for k in ("img", "page")}
                            for w in works if w["image"]}}
    return evidence, records, artworks


class TestBatch21NegativeControls(unittest.TestCase):
    def setUp(self):
        self.evidence, self.records, self.artworks = valid_fixture()
        self.definitions = {"fixture": ["js/artists-21.js"]}
        self.index = '<script src="js/artists-21.js?v=21"></script>'
        self.stubs = {"fixture"}
        self.sitemap = '<loc>https://example.org/p/artist/fixture.html</loc>'

    def assert_caught(self, code, errors):
        self.assertTrue(any(e.startswith(code + ":") for e in errors), (code, errors))

    def test_valid_fixture_passes_every_guard(self):
        self.assertEqual(check_wiring(self.evidence, self.records, self.definitions, self.index,
                                      self.stubs, self.sitemap), [])
        self.assertEqual(check_works(self.evidence, self.records, self.artworks), [])
        self.assertEqual(check_work_ids(self.evidence), [])
        self.assertEqual(check_filenames(self.artworks), [])
        self.assertEqual(check_claims(self.evidence), [])

    def test_each_wiring_guard(self):
        args = [self.evidence, self.records, self.definitions, self.index, self.stubs, self.sitemap]
        for code, position, broken in [("record", 1, []), ("definition", 2, {"fixture": ["js/artists-20.js"]}),
                                       ("script", 3, '<script src="js/artists-210.js"></script>'),
                                       ("stub", 4, set()), ("sitemap", 5, "artist/fixture-extra.html")]:
            with self.subTest(guard=code):
                changed = copy.deepcopy(args)
                changed[position] = broken
                self.assert_caught(code, check_wiring(*changed))

    def test_each_ordered_work_guard(self):
        for mutation in ("title", "date", "order", "missing", "extra"):
            records = copy.deepcopy(self.records)
            works = records[0]["works"]
            if mutation == "title": works[0]["t"] = "Wrong"
            if mutation == "date": works[0]["y"] = "1909"
            if mutation == "order": works.reverse()
            if mutation == "missing": works.pop()
            if mutation == "extra": works.append({"t": "Extra", "y": "1903"})
            with self.subTest(mutation=mutation):
                self.assert_caught("works", check_works(self.evidence, records, self.artworks))

    def test_mismatched_img_and_page(self):
        for key in ("img", "page"):
            artworks = copy.deepcopy(self.artworks)
            artworks["fixture"]["First"][key] += "-wrong"
            with self.subTest(key=key):
                self.assert_caught(key + "_mismatch", check_works(self.evidence, self.records, artworks))

    def test_missing_gallery_entry(self):
        del self.artworks["fixture"]["First"]
        self.assert_caught("image_entry", check_works(self.evidence, self.records, self.artworks))

    def test_missing_no_image_reason(self):
        for value in (None, "", "  "):
            evidence = copy.deepcopy(self.evidence)
            evidence["fixture"]["works"][2]["no_image_reason"] = value
            self.assert_caught("no_image_reason", check_works(evidence, self.records, self.artworks))

    def test_image_for_unpictured_work(self):
        self.artworks["fixture"]["Unpictured"] = self.artworks["fixture"]["First"].copy()
        self.assert_caught("unexpected_image", check_works(self.evidence, self.records, self.artworks))

    def test_extra_artwork(self):
        self.artworks["fixture"]["Unknown"] = self.artworks["fixture"]["First"].copy()
        self.assert_caught("extra_artwork", check_works(self.evidence, self.records, self.artworks))

    def test_license_label(self):
        self.evidence["fixture"]["works"][0]["image"]["license_short_name"] = "CC BY"
        self.assert_caught("license", check_works(self.evidence, self.records, self.artworks))

    def test_duplicate_filename_existing_artist_different_size_and_encoding(self):
        self.artworks["existing"] = {"Other title": {
            "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/%46irst_work.jpg/900px-First_work.jpg"}}
        self.assert_caught("duplicate_filename", check_filenames(self.artworks))

    def test_duplicate_filename_within_batch(self):
        self.artworks["fixture"]["Second"]["img"] = self.artworks["fixture"]["First"]["img"]
        self.assert_caught("duplicate_filename", check_filenames(self.artworks))

    def test_original_filename_not_thumbnail_suffix(self):
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/A%20painting.svg/500px-A_painting.svg.png"
        self.assertEqual(canonical_commons_filename(url), "A painting.svg")
        self.assertEqual(canonical_commons_filename(url.replace("thumb/", "").rsplit("/", 1)[0]), "A painting.svg")
        self.artworks["fixture"]["First"]["img"] = "https://example.org/image.jpg"
        self.assert_caught("commons_filename", check_filenames(self.artworks))

    def test_one_distinct_work_despite_two_images(self):
        self.evidence["fixture"]["works"][1]["work_id"] = "object:1"
        errors = check_work_ids(self.evidence)
        self.assert_caught("duplicate_work_id", errors)
        self.assert_caught("distinct_works", errors)

    def test_only_one_illustrated_work(self):
        self.evidence["fixture"]["works"][1]["image"] = None
        self.assert_caught("distinct_works", check_work_ids(self.evidence))

    def test_missing_work_id(self):
        del self.evidence["fixture"]["works"][0]["work_id"]
        self.assert_caught("work_id", check_work_ids(self.evidence))

    def test_claim_count_and_each_claim_guard(self):
        for code, key, value in [("claim_field", "field", "works"), ("claim_url", "source_url", "http://example.org"),
                                 ("claim_claim", "claim", "  "), ("claim_note", "note", "")]:
            evidence = copy.deepcopy(self.evidence)
            evidence["fixture"]["claims"][0][key] = value
            with self.subTest(guard=code):
                self.assert_caught(code, check_claims(evidence))
        self.evidence["fixture"]["claims"].pop()
        self.assert_caught("claim_count", check_claims(self.evidence))
        self.evidence["fixture"]["claims"][0] = None
        self.assert_caught("claim_shape", check_claims(self.evidence))
        self.evidence["fixture"]["claims"] = None
        self.assert_caught("claims", check_claims(self.evidence))


if __name__ == "__main__":
    unittest.main()
