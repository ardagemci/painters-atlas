"""Unit tests for the rights-register tooling (PIG-001 unit 16).

Offline: every Commons call is stubbed. The only thing these tests are allowed
to hit is the filesystem. Run with:

    python3 -m unittest discover -s tests -v
"""
import json
import os
import re
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


#: Image corrections applied on pig-001-stabilization after the effa805 freeze,
#: from the AC11 rights register (2026-07-25). Recorded here as an explicit
#: delta rather than by rewriting the frozen inventory: the freeze is dated
#: evidence of effa805 and must stay byte-stable, while the tool necessarily
#: reports the corrected tree. Each removal is a confirmed wrong-artwork image
#: OR a swap away from a file whose *photographer* asserted a copyright; each
#: addition passed the exact-work check and carries Commons metadata asserting a
#: public-domain basis. Neither is a clearance and no legal determination was
#: made (OD-5, AC12).
#: Full reasoning: protocol/tasks/PIG-001/evidence/rights-register.md and
#: rights-remediation.md (owner-directed round 2, 2026-07-25).
U = "https://upload.wikimedia.org/wikipedia/commons/thumb/"
CORRECTIONS = {
    "catalog_pd_rendered": {
        "removed": [
            U + "2/25/Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaifuu_kaisei%29_-_Google_Art_Project.jpg/500px-Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaifuu_kaisei%29_-_Google_Art_Project.jpg",
            # Antoine Taveneaux's in-situ ceiling photograph, CC BY-SA 3.0: the
            # photographer asserted a copyright over the photograph itself.
            # Replaced with a PD-Art reproduction plate whose Commons file page
            # carries no photographer claim and asserts a public-domain basis.
            U + "1/1d/Sistine_Chapel_ceiling_02_%28brightened%29.jpg/500px-Sistine_Chapel_ceiling_02_%28brightened%29.jpg",
        ],
        "added": [
            U + "2/25/Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg/500px-Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg",
            U + "2/2a/Sistine_ceiling.jpg/500px-Sistine_ceiling.jpg",
        ],
    },
    "gallery_rendered": {
        "removed": [
            # Added 2026-08-05 (unit 35, D-019). The Sistine swap was ledgered
            # for catalog_pd_rendered and prerender_metadata_refs but NOT for
            # this surface, because at the time of the ledger the swap had only
            # been half-applied: js/artworks.js still carried the CC BY-SA 3.0
            # in-situ photograph. Commit d7675dd completed it (D-016) and the
            # ledger was never extended, so this surface has been failing on a
            # correction we actually made. Same pair as catalog_pd_rendered.
            U + "1/1d/Sistine_Chapel_ceiling_02_%28brightened%29.jpg/500px-Sistine_Chapel_ceiling_02_%28brightened%29.jpg",
            U + "4/46/Joseph_Ducreux_%28French%29_-_Self-Portrait%2C_Yawning_-_Google_Art_Project.jpg/500px-Joseph_Ducreux_%28French%29_-_Self-Portrait%2C_Yawning_-_Google_Art_Project.jpg",
            U + "a/a5/Broken_column_in_Syrakousai.jpg/500px-Broken_column_in_Syrakousai.jpg",
            U + "c/c6/Aleppo_ca1537_by_Matrakci_Nasuh_Istanbul_University_Library_ms5964.png/960px-Aleppo_ca1537_by_Matrakci_Nasuh_Istanbul_University_Library_ms5964.png",
            U + "e/e6/Closeup_of_Frida_Kahlo_and_Diego_Rivera_Sculpture.jpg/960px-Closeup_of_Frida_Kahlo_and_Diego_Rivera_Sculpture.jpg",
            # Livioandronico2013's dome photograph, CC BY-SA 4.0. Replaced with
            # a photograph the photographer himself released under PD-self.
            U + "7/78/Cathedral_%28Parma%29_-_Assumption_by_Correggio.jpg/500px-Cathedral_%28Parma%29_-_Assumption_by_Correggio.jpg",
        ],
        "added": [
            U + "2/2a/Sistine_ceiling.jpg/500px-Sistine_ceiling.jpg",   # unit 35, D-019 — see above
            U + "a/a2/Stanis%C5%82aw_Wyspia%C5%84ski%2C_Autoportret.jpg/500px-Stanis%C5%82aw_Wyspia%C5%84ski%2C_Autoportret.jpg",
            U + "d/db/Karl_Bryullov_%28Bryullo%29_-_%D0%90%D0%B2%D1%82%D0%BE%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82_-_Google_Art_Project.jpg/500px-Karl_Bryullov_%28Bryullo%29_-_%D0%90%D0%B2%D1%82%D0%BE%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82_-_Google_Art_Project.jpg",
            U + "f/f0/Matrak%C3%A7%C4%B1_Nasuh_-_%C4%B0stanbul.jpg/960px-Matrak%C3%A7%C4%B1_Nasuh_-_%C4%B0stanbul.jpg",
            U + "a/a5/Cupola_Duomo_Parma_Correggio.jpg/500px-Cupola_Duomo_Parma_Correggio.jpg",
        ],
    },
    # The stubs were re-emitted so public og:image/twitter:image metadata stops
    # serving the wrong artwork. Kahlo's stub gains no replacement: with no
    # gallery record left, build_seo.jxa.js emits no image at all, which is the
    # honest result — this audit's Commons searches located no candidate that
    # passes the exact-work check, which is a bounded finding about this audit
    # and not a claim that no such file exists anywhere.
    "prerender_metadata_refs": {
        "removed": [
            U + "2/25/Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaifuu_kaisei%29_-_Google_Art_Project.jpg/500px-Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaifuu_kaisei%29_-_Google_Art_Project.jpg",
            U + "c/c6/Aleppo_ca1537_by_Matrakci_Nasuh_Istanbul_University_Library_ms5964.png/960px-Aleppo_ca1537_by_Matrakci_Nasuh_Istanbul_University_Library_ms5964.png",
            U + "e/e6/Closeup_of_Frida_Kahlo_and_Diego_Rivera_Sculpture.jpg/960px-Closeup_of_Frida_Kahlo_and_Diego_Rivera_Sculpture.jpg",
            U + "1/1d/Sistine_Chapel_ceiling_02_%28brightened%29.jpg/500px-Sistine_Chapel_ceiling_02_%28brightened%29.jpg",
            U + "7/78/Cathedral_%28Parma%29_-_Assumption_by_Correggio.jpg/500px-Cathedral_%28Parma%29_-_Assumption_by_Correggio.jpg",
        ],
        "added": [
            U + "2/25/Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg/500px-Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg",
            U + "f/f0/Matrak%C3%A7%C4%B1_Nasuh_-_%C4%B0stanbul.jpg/960px-Matrak%C3%A7%C4%B1_Nasuh_-_%C4%B0stanbul.jpg",
            U + "2/2a/Sistine_ceiling.jpg/500px-Sistine_ceiling.jpg",
            U + "a/a5/Cupola_Duomo_Parma_Correggio.jpg/500px-Cupola_Duomo_Parma_Correggio.jpg",
        ],
    },
}


#: Content-lane ADDITIONS after the effa805 freeze — deliberately a separate
#: ledger from CORRECTIONS above, because they are a different kind of event and
#: conflating them would let real corpus growth hide inside a rights-remediation
#: entry (or the reverse). CORRECTIONS records images we changed because they
#: were wrong. This records images that arrived because the atlas grew.
#:
#: Sole cause: commit ef8b2b3, "Add nine Abstract Expressionist painters, the
#: Washington Color School, and Noland's Beginning" — an independent content lane
#: that landed on this branch mid-build and is ledgered as D-016 (Gate 4 partial
#: breach, benign). It moved artists 247->256, movements 75->76, catalog 317->323,
#: venues 115->116, museum notes 103->104, influence edges 225->238.
#:
#: Exactly one new public image asset came with it: the Hirshhorn museum
#: photograph, which appears on two surfaces (the museum registry, and the
#: p/museum/hirshhorn.html stub's og:image/twitter:image). Its credit is
#: registered in js/photo-credits.js as Quadell / CC BY-SA 3.0, required:true.
#: Nine new painters and six new catalog works arrived WITHOUT images: all six
#: works are 20th-century and carry image:{status:"copyright"} with no src, which
#: is why copyright_refs moves 60->66 while the rendered surfaces move by one.
CONTENT_LANE = {
    "museum_photos_rendered": {
        "removed": [],
        "added": [
            U + "d/dd/Hirshhorn_Museum_and_Sculpture_Garden_-_exterior.jpg/960px-Hirshhorn_Museum_and_Sculpture_Garden_-_exterior.jpg",
        ],
    },
    "prerender_metadata_refs": {
        "removed": [],
        "added": [
            U + "d/dd/Hirshhorn_Museum_and_Sculpture_Garden_-_exterior.jpg/960px-Hirshhorn_Museum_and_Sculpture_Garden_-_exterior.jpg",
        ],
    },
}


class TestAssetInventory(unittest.TestCase):
    FROZEN = ROOT / "protocol" / "tasks" / "PIG-001" / "evidence" / "asset-inventory-effa805.json"

    def test_reproduces_the_frozen_inventory_plus_recorded_corrections(self):
        """The regenerator must reproduce the effa805 freeze once the recorded
        image corrections are applied — otherwise the frozen copy and the tool
        are not comparable and AC10's inventory cannot be re-verified.

        Any drift NOT listed in CORRECTIONS or CONTENT_LANE fails, which is the
        point: an undocumented image change cannot slip through as 'expected
        drift'. The two ledgers stay separate so that a rights correction and a
        corpus addition can never be mistaken for one another."""
        frozen = json.loads(self.FROZEN.read_text(encoding="utf-8"))
        now = ai.as_json(ai.build())
        for key in sorted(set(frozen) | set(now)):
            with self.subTest(surface=key):
                expected = set(frozen.get(key, []))
                for ledger in (CORRECTIONS, CONTENT_LANE):
                    delta = ledger.get(key)
                    if delta:
                        expected -= set(delta["removed"])
                        expected |= set(delta["added"])
                self.assertEqual(sorted(expected), sorted(now.get(key, [])))

    def test_prerender_refs_track_the_corrections(self):
        """The stub pages carry og:image/twitter:image. A corrected image that
        was not re-emitted into p/ would keep serving the wrong artwork in
        public metadata, so the stub surface must never lag the data."""
        now = set(ai.as_json(ai.build()).get("prerender_metadata_refs", []))
        for delta in CORRECTIONS.values():
            for url in delta["removed"]:
                self.assertNotIn(url, now, "corrected image still referenced by a stub page")

    def test_headline_counts_match_the_corrected_tree(self):
        """Re-frozen at a1b822b, 2026-08-05 (unit 35, D-019). Every figure that
        moved carries its reason here; nothing was renumbered to match drift.
        Full derivation: protocol/tasks/PIG-001/evidence/data-reconciliation.md."""
        c = ai.build()["counts"]
        # 799 (effa805) -> 797 (rights corrections) -> 798 (content lane).
        # Three Kahlo records and one duplicate gallery record were removed as
        # confirmed wrong-artwork images and two corrected files added, giving
        # 797; ef8b2b3 then added the single Hirshhorn museum photograph, giving
        # 798. The +1 is the ONLY new public image asset in the content lane.
        self.assertEqual(c["total_unique"], 798)
        self.assertEqual(c["rendered_unique"], 797)      # 796 + the same Hirshhorn photo
        self.assertEqual(c["metadata_only_unique"], 1)   # unchanged: the homepage og:image
        self.assertEqual(c["catalog_gallery_overlap"], 92)   # unchanged
        self.assertEqual(c["suppressed_leaking_into_metadata"], 0)  # unchanged, and must stay 0
        # 60 -> 66: ef8b2b3's six 20th-century works, all image:{status:"copyright"}
        # with no src — beginning-noland, chief-kline, city-limits-guston,
        # elegy-to-the-spanish-republic-108, mars-dust, the-gate-hofmann. A rise
        # here is correct behaviour: it means works that may not be rendered were
        # recorded as such rather than silently given an image.
        self.assertEqual(c["copyright_refs"], 66)


class TestSampleBasis(unittest.TestCase):
    def test_sample_matches_the_ac11_basis(self):
        sample = rr.sample_records()
        self.assertGreaterEqual(len(sample), 100)
        tier1 = [r for r in sample if r["surface"] == "catalog"]
        self.assertEqual(len(tier1), 75, "Tier 1 ∪ daily pool is 75 works")
        # Every Matisse and Kahlo gallery record is mandatory in the sample.
        # Kahlo's three were removed as confirmed wrong-artwork images, so the
        # mandatory set is now exactly Matisse's — and "all of them" must still
        # hold rather than "some of them".
        gallery = rr.SURFACES["gallery"]()
        mandatory = {r["id"] for r in gallery
                     if r["artist_id"] in ("henri-matisse", "frida-kahlo")}
        in_sample = {r["id"] for r in sample if r["surface"] == "gallery"}
        self.assertTrue(mandatory <= in_sample,
                        "every Matisse and Kahlo gallery record is mandatory")
        self.assertFalse([r for r in gallery if r["artist_id"] == "frida-kahlo"],
                         "Kahlo gallery records are suppressed; none may return")

    def test_the_tier1_record_with_no_asset_is_dispositioned_not_counted_away(self):
        """AC11 no-asset disposition for the 76th Tier 1 work (unit 35, D-019).

        The validator reports `tier1: 76`; the rights sample reports 75 catalog
        records. Both are right, and the gap is not an error to be closed by
        changing a number. `_catalog_records()` deliberately admits only records
        carrying a Commons URL, so it counts *Tier 1 works that have an asset*.
        Exactly one Tier 1 work has none.

        That record is `beginning-noland` — Kenneth Noland's "Beginning" (1958),
        which arrived with ef8b2b3. Noland died in 2010, so no public-domain
        basis is assertable on the ordinary term arithmetic; the record carries
        `image:{status:"copyright"}` with no `src`, and the app renders it as a
        title row with no image. Its AC11 disposition is therefore *no asset to
        register*: there is nothing to check rights on, because nothing is
        served. This test exists so that fact stays asserted rather than
        inferred, and so a future silent addition of an image would fail here."""
        catalog = rr.SURFACES["catalog"]()
        tier1_with_asset = [r for r in catalog if r["tier"] == 1]
        self.assertEqual(len(tier1_with_asset), 75)

        src = (ROOT / "js" / "catalog-4.js").read_text(encoding="utf-8")
        rec = re.search(r'^\{\s*id:"beginning-noland".*?(?=^\{\s*id:"|\Z)',
                        src, re.S | re.M)
        self.assertIsNotNone(rec, "the 76th Tier 1 record must still exist")
        img = re.search(r"image:\s*\{(.*?)\}", rec.group(0), re.S).group(1)
        self.assertIn('status:"copyright"', img.replace(" ", ""))
        self.assertNotIn("upload.wikimedia.org", img,
                         "a copyright-status record must carry no image URL")

        # And it must not have leaked onto any rendered or metadata surface.
        inv = ai.as_json(ai.build())
        for surface, urls in inv.items():
            self.assertFalse([u for u in urls if "beginning-noland" in u],
                             "beginning-noland must not appear on %s" % surface)

    def test_sample_is_deterministic(self):
        a = [r["id"] for r in rr.sample_records()]
        b = [r["id"] for r in rr.sample_records()]
        self.assertEqual(a, b)

    def test_catalog_surface_matches_the_corrected_pd_count(self):
        self.assertEqual(len(rr.SURFACES["catalog"]()), 257)
        # 103 -> 104 at ef8b2b3: the Hirshhorn Museum and Sculpture Garden note,
        # which arrived with Noland's "Beginning". Credited in js/photo-credits.js
        # (Quadell, CC BY-SA 3.0, attribution required). Unit 35, D-019.
        self.assertEqual(len(rr.SURFACES["museum"]()), 104)
        # 532 -> 528: the three Kahlo records and the duplicate Bada Shanren
        # "Two Birds" record were removed as confirmed wrong-artwork images.
        self.assertEqual(len(rr.SURFACES["gallery"]()), 528)


class TestSuppression(unittest.TestCase):
    """A wrong image that a regeneration can restore is not fixed."""

    def test_resolver_and_auditor_share_one_suppression_list(self):
        import fetch_artworks as fa
        import audit_artworks as aa
        self.assertIs(aa.SUPPRESS, fa.SUPPRESS)

    def test_suppressed_works_carry_a_reason(self):
        import fetch_artworks as fa
        self.assertTrue(fa.SUPPRESS)
        for key, reason in fa.SUPPRESS.items():
            self.assertIn("::", key)
            self.assertGreater(len(reason), 20, "a suppression needs a stated reason")

    def test_suppressed_works_are_absent_from_shipped_gallery_data(self):
        shipped = {r["id"] for r in rr.SURFACES["gallery"]()}
        import fetch_artworks as fa
        for key in fa.SUPPRESS:
            self.assertNotIn(key, shipped)


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


class TestProseLanguage(unittest.TestCase):
    """OD-5, extended to the prose (unit 35, D-019).

    TestRegisterLanguage above enforces the no-clearance rule on the register the
    tooling *generates*, and it has always passed. The rule broke anyway, in the
    human-written build report, because nothing read the prose. A rule enforced
    only where a test looks is not enforced — so this class looks at the prose.

    Scope is deliberately limited to artifacts THIS pole authors and may edit.
    Incoming theory messages, liaison analyses and the frozen specification are
    excluded: they quote the offending phrases in order to object to them or to
    forbid them, and they are history that must not be rewritten.

    A line is exempt if it is a blockquote (`>`), contains strikethrough (`~~`),
    or carries the literal marker `OD5-EXEMPT`. The first two are how this
    project preserves a superseded claim beside its dated correction; the third
    is for the few places that must contain a forbidden phrase in order to
    forbid or test it. Exemptions are counted and pinned below, so widening the
    hole is itself a test failure rather than a quiet edit.
    """

    #: Every sanctioned OD5-EXEMPT marker in the tree, by file. Pinned so that
    #: adding one is a deliberate, reviewable act and never a silent bypass.
    EXPECTED_EXEMPTIONS = {
        "docs/STYLE_GUIDE.md": 1,           # quotes the phrases in order to ban them
        "tools/fetch_artworks.py": 1,       # dated note quoting what it replaced
        # names the marker while documenting the mechanism (D-019, §2.2)
        "protocol/tasks/PIG-001/evidence/data-reconciliation.md": 1,
        # 6 fixture phrases in test_the_guard_actually_catches..., plus this
        # class's own docstring, this map's comment, and the two lines that
        # implement and count the marker. All self-referential; none is prose.
        "tests/test_rights_tooling.py": 12,
    }

    #: Assertions of legal status. Each is a claim no evidence in this project
    #: supports. Bounded alternatives: "Commons metadata asserts a public-domain
    #: basis", "the exact-work check confirmed", "this audit did not locate".
    BANNED = [
        (r"verified[- ]?PD", "asserts a legal status; say what Commons asserts"),
        (r"verifiably[- ]?PD", "asserts a legal status"),
        (r"genuinely[- ]?(PD|public[- ]domain)", "asserts a legal status"),
        (r"confirmed[- ]?(PD|public[- ]domain)", "asserts a legal status"),
        (r"\b(is|are|was|were)\s+(now\s+)?(in\s+the\s+)?public[- ]domain\b",
         "asserts a legal status; say 'Commons metadata asserts a PD basis'"),
        (r"\b(is|are)\s+PD\b", "asserts a legal status"),
        (r"(rights|legally|copyright)[- ]cleared", "OD-5 forbids 'cleared'"),
        (r"cleared\s+for\s+(use|publication)", "OD-5 forbids 'cleared'"),
        (r"no\s+(suitable\s+)?(PD|public[- ]domain)\s+image\s+[^.]{0,40}\bexists?\b",
         "exhaustive-absence claim; bound it to this audit's searches"),
        (r"public[- ]domain\s+status\s+(is|was|has been)\s+(verified|confirmed|established)",
         "asserts a legal determination"),
    ]

    #: Our own prose. Everything here is a file this pole wrote and may correct.
    SCANNED = [
        ROOT / "protocol" / "tasks" / "PIG-001" / "build-evidence-report.md",
        ROOT / "protocol" / "tasks" / "PIG-001" / "evidence",
        ROOT / "docs",
        ROOT / "tools",
        ROOT / "tests",
        ROOT / "README.md",
    ]
    SUFFIXES = (".md", ".py", ".js")

    def _files(self):
        for target in self.SCANNED:
            if target.is_file():
                yield target
            elif target.is_dir():
                for p in sorted(target.rglob("*")):
                    if p.is_file() and p.suffix in self.SUFFIXES:
                        yield p

    def test_no_artifact_of_ours_asserts_a_legal_conclusion(self):
        offences = []
        for path in self._files():
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for n, line in enumerate(text.split("\n"), 1):
                stripped = line.lstrip()
                if (stripped.startswith(">") or "~~" in line
                        or "OD5-EXEMPT" in line):
                    continue          # a preserved claim beside its correction
                for pattern, why in self.BANNED:
                    if re.search(pattern, line, re.I):
                        offences.append("%s:%d: %s\n      -> %s"
                                        % (path.relative_to(ROOT), n,
                                           stripped[:120], why))
        self.assertEqual(offences, [], "\n\nOD-5 language breach in prose:\n  "
                                       + "\n  ".join(offences)
                                       + "\n\nRecord what Commons asserts and what "
                                         "the exact-work check confirmed. Never a "
                                         "legal conclusion.\n")

    def test_the_guard_actually_catches_the_phrases_that_got_through(self):
        """A guard that cannot fail is not a guard. These are the exact strings
        that reached the routed implementation report."""
        for phrase in ("three replaced with verified-PD files",            # OD5-EXEMPT
                       "replaced with genuinely PD images",                # OD5-EXEMPT
                       "the fresco is PD",                                 # OD5-EXEMPT
                       "No PD image exists on Commons.",                   # OD5-EXEMPT
                       "this work is public domain",                       # OD5-EXEMPT
                       "the image is rights-cleared"):                     # OD5-EXEMPT
            self.assertTrue(
                any(re.search(p, phrase, re.I) for p, _ in self.BANNED),
                "guard does not catch: %r" % phrase)

    def test_bounded_language_is_not_flagged(self):
        """The guard must not punish the wording it is trying to encourage, or
        authors will route around it."""
        for phrase in ("Commons metadata asserts a public-domain basis",
                       "the exact-work check confirmed the depicted work",
                       "this audit's searches located no candidate",
                       "carries a Commons public-domain assertion",
                       "resolution: asserted-by-commons; no legal conclusion"):
            self.assertFalse(
                [p for p, _ in self.BANNED if re.search(p, phrase, re.I)],
                "bounded language wrongly flagged: %r" % phrase)

    def test_exemption_markers_are_pinned(self):
        """Widening the exemption must be visible, not silent."""
        found = {}
        for path in self._files():
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            n = text.count("OD5-EXEMPT")                        # OD5-EXEMPT
            if n:
                found[str(path.relative_to(ROOT))] = n
        self.assertEqual(found, self.EXPECTED_EXEMPTIONS,
                         "OD5-EXEMPT markers changed. Every exemption must be "
                         "justified in the pin above, not added quietly.")


if __name__ == "__main__":
    unittest.main()
