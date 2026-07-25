"""Unit tests for the rights-register tooling (PIG-001 unit 16).

Offline: every Commons call is stubbed. The only thing these tests are allowed
to hit is the filesystem. Run with:

    python3 -m unittest discover -s tests -v
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import commons_rights as cr          # noqa: E402
import asset_inventory as ai         # noqa: E402
import rights_register as rr         # noqa: E402


class TestCommonsFileTitle(unittest.TestCase):
    def test_thumbnail_url_resolves_to_the_real_file(self):
        u = ("https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/"
             "Caravaggio_%E2%80%94_The_Calling_of_Saint_Matthew.jpg/"
             "500px-Caravaggio_%E2%80%94_The_Calling_of_Saint_Matthew.jpg")
        self.assertEqual(cr.commons_file_title(u),
                         "File:Caravaggio_—_The_Calling_of_Saint_Matthew.jpg")

    def test_direct_url_resolves(self):
        u = "https://upload.wikimedia.org/wikipedia/commons/0/05/Muybridge_race_horse_animated_184px.gif"
        self.assertEqual(cr.commons_file_title(u), "File:Muybridge_race_horse_animated_184px.gif")

    def test_non_commons_host_tree_is_rejected(self):
        # /wikipedia/en/ is a local (often fair-use) upload, never Commons.
        u = "https://upload.wikimedia.org/wikipedia/en/a/ab/Something.jpg"
        self.assertIsNone(cr.commons_file_title(u))

    def test_empty_and_malformed(self):
        self.assertIsNone(cr.commons_file_title(""))
        self.assertIsNone(cr.commons_file_title(None))
        self.assertIsNone(cr.commons_file_title(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5"))


class TestExtmetadataExtraction(unittest.TestCase):
    SAMPLE = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/ab/X.jpg",
        "descriptionurl": "https://commons.wikimedia.org/wiki/File:X.jpg",
        "mime": "image/jpeg",
        "extmetadata": {
            "LicenseShortName": {"value": "Public domain"},
            "License": {"value": "pd"},
            "LicenseUrl": {"value": "http://example.org/pd"},
            "UsageTerms": {"value": "Public domain"},
            "Artist": {"value": '<a href="/wiki/X" title="X">Johannes&nbsp;Vermeer</a>'},
            "Credit": {"value": "<span>Google Art Project</span>"},
            "AttributionRequired": {"value": "false"},
            "DateTimeOriginal": {"value": "1665"},
        },
    }

    def test_fields_are_flattened_and_de_html_ed(self):
        rec = cr.rights_from_imageinfo(self.SAMPLE)
        self.assertEqual(rec["license_short_name"], "Public domain")
        self.assertEqual(rec["artist"], "Johannes Vermeer")
        self.assertEqual(rec["credit"], "Google Art Project")
        self.assertEqual(rec["date_time_original"], "1665")
        self.assertEqual(rec["commons_file_page"], "https://commons.wikimedia.org/wiki/File:X.jpg")

    def test_absent_keys_are_empty_never_guessed(self):
        rec = cr.rights_from_imageinfo({"url": "u", "extmetadata": {}})
        self.assertEqual(rec["license_short_name"], "")
        self.assertEqual(rec["artist"], "")

    def test_no_record_ever_claims_a_legal_conclusion(self):
        self.assertEqual(cr.rights_from_imageinfo(self.SAMPLE)["legal_conclusion"], "none")


class TestFetchRights(unittest.TestCase):
    """The API normalizes underscores to spaces. Records must key on the
    title the caller asked for, or every hit is silently lost."""

    def setUp(self):
        self._real = cr.api_get_json
        self.addCleanup(lambda: setattr(cr, "api_get_json", self._real))

    def test_normalized_titles_are_mapped_back_to_the_requested_title(self):
        cr.api_get_json = lambda url, attempts=4: {
            "query": {
                "normalized": [{"from": "File:A_b.jpg", "to": "File:A b.jpg"}],
                "pages": [{
                    "title": "File:A b.jpg",
                    "imageinfo": [{"descriptionurl": "https://commons.wikimedia.org/wiki/File:A_b.jpg",
                                   "extmetadata": {"LicenseShortName": {"value": "Public domain"}}}],
                }],
            }
        }
        out = list(cr.fetch_rights(["File:A_b.jpg"]))
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["status"], "ok")
        self.assertEqual(out[0]["title"], "File:A_b.jpg")          # what we asked for
        self.assertEqual(out[0]["resolved_title"], "File:A b.jpg")  # what Commons calls it
        self.assertEqual(out[0]["license_short_name"], "Public domain")

    def test_transient_failure_is_unverified_never_a_negative_finding(self):
        def boom(url, attempts=4):
            raise cr.Unverified("HTTP 429")
        cr.api_get_json = boom
        out = list(cr.fetch_rights(["File:A.jpg", "File:B.jpg"]))
        self.assertEqual([r["status"] for r in out], ["unverified", "unverified"])
        for r in out:
            self.assertNotIn("license_short_name", r)   # absence of data, not data
            self.assertEqual(r["legal_conclusion"], "none")

    def test_explicit_missing_is_the_only_definitive_negative(self):
        cr.api_get_json = lambda url, attempts=4: {
            "query": {"pages": [{"title": "File:Gone.jpg", "missing": True}]}}
        out = list(cr.fetch_rights(["File:Gone.jpg"]))
        self.assertEqual(out[0]["status"], "missing")

    def test_page_present_but_no_imageinfo_is_not_a_licence_finding(self):
        cr.api_get_json = lambda url, attempts=4: {
            "query": {"pages": [{"title": "File:A.jpg"}]}}
        self.assertEqual(list(cr.fetch_rights(["File:A.jpg"]))[0]["status"], "no-metadata")

    def test_batch_size_is_capped_at_the_api_limit(self):
        seen = []

        def spy(url, attempts=4):
            import urllib.parse
            titles = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["titles"][0]
            seen.append(len(titles.split("|")))
            return {"query": {"pages": []}}
        cr.api_get_json = spy
        list(cr.fetch_rights(["File:%d.jpg" % i for i in range(120)], batch=500))
        self.assertEqual(seen, [50, 50, 20])


class TestSidecar(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "cache.json")

    def test_a_failed_run_never_erases_a_verified_one(self):
        cr.save_sidecar({"File:A.jpg": {"status": "ok", "license_short_name": "Public domain"}}, self.path)
        cr.save_sidecar({"File:A.jpg": {"status": "unverified"}}, self.path)
        cached = cr.load_sidecar(self.path)
        self.assertEqual(cached["File:A.jpg"]["status"], "ok")
        self.assertEqual(cached["File:A.jpg"]["license_short_name"], "Public domain")

    def test_new_verified_data_does_overwrite(self):
        cr.save_sidecar({"File:A.jpg": {"status": "unverified"}}, self.path)
        cr.save_sidecar({"File:A.jpg": {"status": "ok", "license_short_name": "CC0"}}, self.path)
        self.assertEqual(cr.load_sidecar(self.path)["File:A.jpg"]["license_short_name"], "CC0")

    def test_a_corrupt_cache_is_not_a_finding(self):
        with open(self.path, "w") as f:
            f.write("{not json")
        self.assertEqual(cr.load_sidecar(self.path), {})

    def test_capture_skips_pages_without_extmetadata(self):
        store = {}
        self.assertFalse(cr.capture_from_imageinfo(store, {"title": "File:A.jpg", "imageinfo": [{"url": "u"}]}))
        self.assertFalse(cr.capture_from_imageinfo(store, {"title": "File:A.jpg"}))
        self.assertEqual(store, {})
        self.assertTrue(cr.capture_from_imageinfo(store, {
            "title": "File:A.jpg",
            "imageinfo": [{"url": "u", "extmetadata": {"LicenseShortName": {"value": "CC0"}}}]}))
        self.assertEqual(store["File:A.jpg"]["license_short_name"], "CC0")


class TestAssetInventory(unittest.TestCase):
    FROZEN = ROOT / "protocol" / "tasks" / "PIG-001" / "evidence" / "asset-inventory-effa805.json"

    def test_reproduces_the_frozen_inventory(self):
        """The regenerator must reproduce the effa805 freeze for an unchanged
        data tree — otherwise the frozen copy and the tool are not comparable
        and AC10's inventory cannot be re-verified."""
        frozen = json.loads(self.FROZEN.read_text(encoding="utf-8"))
        now = ai.as_json(ai.build())
        for key in sorted(set(frozen) | set(now)):
            with self.subTest(surface=key):
                self.assertEqual(sorted(frozen.get(key, [])), sorted(now.get(key, [])))

    def test_headline_counts_match_the_frozen_table(self):
        c = ai.build()["counts"]
        self.assertEqual(c["total_unique"], 799)
        self.assertEqual(c["rendered_unique"], 798)
        self.assertEqual(c["metadata_only_unique"], 1)
        self.assertEqual(c["catalog_gallery_overlap"], 91)
        self.assertEqual(c["suppressed_leaking_into_metadata"], 0)
        self.assertEqual(c["copyright_refs"], 60)


class TestSampleBasis(unittest.TestCase):
    def test_sample_matches_the_ac11_basis(self):
        sample = rr.sample_records()
        self.assertGreaterEqual(len(sample), 100)
        tier1 = [r for r in sample if r["surface"] == "catalog"]
        self.assertEqual(len(tier1), 75, "Tier 1 ∪ daily pool is 75 works")
        exposed = [r for r in sample if r["artist_id"] in ("henri-matisse", "frida-kahlo")]
        self.assertTrue(exposed, "every Matisse and Kahlo gallery record is mandatory")

    def test_sample_is_deterministic(self):
        a = [r["id"] for r in rr.sample_records()]
        b = [r["id"] for r in rr.sample_records()]
        self.assertEqual(a, b)

    def test_catalog_surface_matches_the_frozen_pd_count(self):
        self.assertEqual(len(rr.SURFACES["catalog"]()), 257)
        self.assertEqual(len(rr.SURFACES["museum"]()), 103)
        self.assertEqual(len(rr.SURFACES["gallery"]()), 532)


class TestRegisterLanguage(unittest.TestCase):
    """OD-5: the register may say 'asserted'. It may never say 'cleared'."""

    def _fake_rights(self, status, licence=""):
        return {"status": status, "commons_file_page": "https://commons.wikimedia.org/wiki/File:X.jpg",
                "license_short_name": licence}

    def setUp(self):
        self._real = cr.rights_for_urls
        self.addCleanup(lambda: setattr(cr, "rights_for_urls", self._real))

    def test_unverified_entries_stay_unresolved(self):
        cr.rights_for_urls = lambda urls, batch=50, on_batch=None: {
            u: self._fake_rights("unverified") for u in urls}
        reg = rr.build_register([{"id": "x", "artist_id": "", "title": "t", "surface": "catalog",
                                  "src": "https://upload.wikimedia.org/wikipedia/commons/a/ab/X.jpg",
                                  "declared_page": ""}], progress=False)
        self.assertEqual(reg[0]["resolution"], "unresolved")
        self.assertEqual(reg[0]["legal_conclusion"], "none")

    def test_the_word_cleared_appears_nowhere_in_the_output(self):
        cr.rights_for_urls = lambda urls, batch=50, on_batch=None: {
            u: self._fake_rights("ok", "Public domain") for u in urls}
        reg = rr.build_register([{"id": "x", "artist_id": "", "title": "t", "surface": "catalog",
                                  "src": "https://upload.wikimedia.org/wikipedia/commons/a/ab/X.jpg",
                                  "declared_page": ""}], progress=False)
        self.assertEqual(reg[0]["resolution"], "asserted-by-commons")
        md = rr.as_md(reg, rr.summarize(reg), "catalog").lower()
        self.assertNotIn("cleared", md)
        self.assertIn("no legal conclusion", md)

    def test_an_english_wikipedia_page_is_flagged_as_not_the_file_page(self):
        cr.rights_for_urls = lambda urls, batch=50, on_batch=None: {
            u: self._fake_rights("ok", "Public domain") for u in urls}
        reg = rr.build_register([{"id": "x", "artist_id": "", "title": "t", "surface": "catalog",
                                  "src": "https://upload.wikimedia.org/wikipedia/commons/a/ab/X.jpg",
                                  "declared_page": "https://en.wikipedia.org/wiki/X"}], progress=False)
        self.assertFalse(reg[0]["declared_page_is_commons_file_page"])
        self.assertEqual(reg[0]["commons_file_page"], "https://commons.wikimedia.org/wiki/File:X.jpg")


if __name__ == "__main__":
    unittest.main()
