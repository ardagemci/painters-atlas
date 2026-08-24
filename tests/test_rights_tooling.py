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
            # 2026-08-08, owner-reported and confirmed by opening both files.
            # Ursonate is a forty-minute SOUND POEM and was illustrated with a
            # 1927 photographic portrait of Schwitters — the artist standing in
            # for the work. Commons has no page of the published score; the only
            # Ursonate images there are photographs of a 2024 performance. The
            # slot now holds Das Undbild (1919), a real Merz assemblage. Ursonate
            # keeps its place in his career prose, where a sound poem belongs.
            U + "2/22/Kurt_Schwitters_1927.jpg/500px-Kurt_Schwitters_1927.jpg",
            # Vision of Spain is a FOURTEEN-PANEL cycle at the Hispanic Society
            # and was illustrated with a photograph of the room: ceiling, floor,
            # orange walls, the murals small across the far side. No single frame
            # represents the cycle, so the entry now names the panel it shows.
            U + "a/ac/Joaqu%C3%ACn_sorolla_y_bastida%2C_visione_della_spagna%2C_1911-19%2C_02.JPG/500px-Joaqu%C3%ACn_sorolla_y_bastida%2C_visione_della_spagna%2C_1911-19%2C_02.JPG",
        ],
        "added": [
            U + "2/2a/Sistine_ceiling.jpg/500px-Sistine_ceiling.jpg",   # unit 35, D-019 — see above
            U + "a/a2/Stanis%C5%82aw_Wyspia%C5%84ski%2C_Autoportret.jpg/500px-Stanis%C5%82aw_Wyspia%C5%84ski%2C_Autoportret.jpg",
            U + "d/db/Karl_Bryullov_%28Bryullo%29_-_%D0%90%D0%B2%D1%82%D0%BE%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82_-_Google_Art_Project.jpg/500px-Karl_Bryullov_%28Bryullo%29_-_%D0%90%D0%B2%D1%82%D0%BE%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82_-_Google_Art_Project.jpg",
            U + "f/f0/Matrak%C3%A7%C4%B1_Nasuh_-_%C4%B0stanbul.jpg/960px-Matrak%C3%A7%C4%B1_Nasuh_-_%C4%B0stanbul.jpg",
            U + "a/a5/Cupola_Duomo_Parma_Correggio.jpg/500px-Cupola_Duomo_Parma_Correggio.jpg",
            U + "f/fc/DasUndbild.jpg/500px-DasUndbild.jpg",
            U + "5/5f/Catalu%C3%B1a._El_pescado%2C_por_Joaqu%C3%ADn_Sorolla.jpg/500px-Catalu%C3%B1a._El_pescado%2C_por_Joaqu%C3%ADn_Sorolla.jpg",
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


#: THIRD LEDGER — the catalog batches (docs/CATALOG_BATCH_01.md, _02.md).
#:
#: Kept separate from CORRECTIONS and CONTENT_LANE for the same reason those two
#: are separate from each other: a rights correction, an unrelated content lane
#: and a planned catalog batch must never be mistakable for one another in the
#: diff. This ledger records images that moved SURFACE, not images that arrived.
#:
#: All 22 files were already in the tree — they are pool entries on artist pages,
#: counted in the `gallery` surface at the effa805 freeze. Landing them as catalog
#: records puts the same URLs on the `catalog` surface as well, so:
#:   * catalog_pd_rendered gains 22 entries;
#:   * catalog_gallery_overlap rises by exactly 22, because every one of the 22 is
#:     on both surfaces — which is also the check that no NEW asset came in;
#:   * total_unique, rendered_unique and metadata_only_unique DO NOT MOVE, and if
#:     any of them does, this batch introduced an image it did not declare.
#: The list is emitted from js/catalog-5.js rather than typed, so it cannot drift
#: from what actually shipped.
CATALOG_BATCHES = {
    "catalog_pd_rendered": {
        "removed": [],
        "added": [
            # BEGIN catalog-5 pd images
            # 2026-08-08, appended to catalog-5.js: Caillebotte, Young Man at
            # His Window. Same behaviour as the 22 above - the file was already a
            # gallery pool entry, so it moves surface rather than arriving:
            # catalog_gallery_overlap 114 -> 115 while total_unique and
            # rendered_unique do not move.
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Gustave_Caillebotte_-_Jeune_homme_%C3%A0_sa_fen%C3%AAtre_%28B_32%29.jpg/960px-Gustave_Caillebotte_-_Jeune_homme_%C3%A0_sa_fen%C3%AAtre_%28B_32%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg/500px-Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Jan_Matejko%2C_Sta%C5%84czyk.jpg/500px-Jan_Matejko%2C_Sta%C5%84czyk.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg/500px-Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg/500px-Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Amrita_Sher-Gil_Group_of_Three_Girls.jpg/500px-Amrita_Sher-Gil_Group_of_Three_Girls.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Arshile_Gorky%2C_The_Artist_and_His_Mother.jpg/960px-Arshile_Gorky%2C_The_Artist_and_His_Mother.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Gallen_Kallela_Lemminkainens_Mother.jpg/500px-Gallen_Kallela_Lemminkainens_Mother.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Reza_Abbasi_-_Two_Lovers_%281630%29.jpg/500px-Reza_Abbasi_-_Two_Lovers_%281630%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Bada_Shanren_%28Zhu_Da%29_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg/960px-Bada_Shanren_%28Zhu_Da%29_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Danwon_Ssireum.jpg/960px-Danwon_Ssireum.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Giotto%2C_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg/500px-Giotto%2C_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Masaccio%2C_trinit%C3%A0.jpg/500px-Masaccio%2C_trinit%C3%A0.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/El_Descendimiento%2C_by_Rogier_van_der_Weyden%2C_from_Prado_in_Google_Earth.jpg/960px-El_Descendimiento%2C_by_Rogier_van_der_Weyden%2C_from_Prado_in_Google_Earth.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Giorgione_-_Das_Gewitter.jpg/500px-Giorgione_-_Das_Gewitter.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg/500px-Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_dead_Christ_and_three_mourners%2C_by_Andrea_Mantegna.jpg/500px-The_dead_Christ_and_three_mourners%2C_by_Andrea_Mantegna.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Sesshu_-_Haboku-Sansui_-_complete.jpg/960px-Sesshu_-_Haboku-Sansui_-_complete.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_%28National_Treasure%29_-_Google_Art_Project.jpg/500px-Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_%28National_Treasure%29_-_Google_Art_Project.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Le_Serment_des_Horaces_-_Jacques-Louis_David_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3692_%3B_MR_1432.jpg/500px-Le_Serment_des_Horaces_-_Jacques-Louis_David_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3692_%3B_MR_1432.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/JEAN_LOUIS_TH%C3%89ODORE_G%C3%89RICAULT_-_La_Balsa_de_la_Medusa_%28Museo_del_Louvre%2C_1818-19%29.jpg/500px-JEAN_LOUIS_TH%C3%89ODORE_G%C3%89RICAULT_-_La_Balsa_de_la_Medusa_%28Museo_del_Louvre%2C_1818-19%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Gustave_Courbet_-_A_Burial_at_Ornans_-_Google_Art_Project_2.jpg/500px-Gustave_Courbet_-_A_Burial_at_Ornans_-_Google_Art_Project_2.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/A_Sunday_on_La_Grande_Jatte%2C_Georges_Seurat%2C_1884.jpg/500px-A_Sunday_on_La_Grande_Jatte%2C_Georges_Seurat%2C_1884.jpg",            # END catalog-5 pd images
        ],
    },
    #: The prerender surface moves differently from the data surface, and the
    #: difference is the point. build_seo.jxa.js:74 artistImage() prefers a
    #: CATALOG pd work over a js/artworks.js pool entry, so an artist who gains a
    #: catalog record has their stub's og:image switch from a pool work to the
    #: catalog work. Eight artists did. Thirteen of the 22 catalog images were
    #: already on this surface for that same reason, which is why the net is
    #: +9/-8 and not +22. Nothing left the tree: all eight removed files are
    #: still rendered on the artist-page gallery surface, they are simply no
    #: longer what a scraper is handed for that artist.
    "prerender_metadata_refs": {
        "removed": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Riza-yi-Abbasi_008.jpg/960px-Riza-yi-Abbasi_008.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Young_Girls.jpg/500px-Young_Girls.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jan_Matejko%2C_Bitwa_pod_Grunwaldem.jpg/960px-Jan_Matejko%2C_Bitwa_pod_Grunwaldem.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Die_Zwitscher-Maschine_%28Twittering_Machine%29%2C_1922_-_Paul_Klee.jpg/500px-Die_Zwitscher-Maschine_%28Twittering_Machine%29%2C_1922_-_Paul_Klee.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Bada_Shanren_-_Fish_and_Rocks_-_1953.247_-_Cleveland_Museum_of_Art.tiff/lossy-page1-960px-Bada_Shanren_-_Fish_and_Rocks_-_1953.247_-_Cleveland_Museum_of_Art.tiff.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Tizian_041.jpg/500px-Tizian_041.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Gallen-Kallela_The_defence_of_the_Sampo.png/500px-Gallen-Kallela_The_defence_of_the_Sampo.png",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Giotto_di_Bondone_-_Scenes_with_decorative_bands_-_WGA09284.jpg/500px-Giotto_di_Bondone_-_Scenes_with_decorative_bands_-_WGA09284.jpg",
            # 2026-08-08 side-effect of the Caillebotte record: build_seo.jxa.js
            # prefers a catalogued work for an artist stub's og:image, so
            # p/artist/gustave-caillebotte.html switched from Paris Street;
            # Rainy Day to Young Man at His Window. Recorded because it is a
            # real change to what a scraper is handed, not a rights event.
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Gustave_Caillebotte_-_Paris_Street%3B_Rainy_Day_-_Google_Art_Project.jpg/500px-Gustave_Caillebotte_-_Paris_Street%3B_Rainy_Day_-_Google_Art_Project.jpg",
        ],
        "added": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg/500px-Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Giotto%2C_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg/500px-Giotto%2C_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Amrita_Sher-Gil_Group_of_Three_Girls.jpg/500px-Amrita_Sher-Gil_Group_of_Three_Girls.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Bada_Shanren_%28Zhu_Da%29_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg/960px-Bada_Shanren_%28Zhu_Da%29_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_%28National_Treasure%29_-_Google_Art_Project.jpg/500px-Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_%28National_Treasure%29_-_Google_Art_Project.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Jan_Matejko%2C_Sta%C5%84czyk.jpg/500px-Jan_Matejko%2C_Sta%C5%84czyk.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Reza_Abbasi_-_Two_Lovers_%281630%29.jpg/500px-Reza_Abbasi_-_Two_Lovers_%281630%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Gallen_Kallela_Lemminkainens_Mother.jpg/500px-Gallen_Kallela_Lemminkainens_Mother.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg/500px-Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg",
            # 2026-08-08: the new p/artwork/young-man-at-his-window.html stub
            # carries this file as og:image/twitter:image. It was already a
            # rendered gallery asset, so this is a second surface for it and
            # total_unique still does not move.
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Gustave_Caillebotte_-_Jeune_homme_%C3%A0_sa_fen%C3%AAtre_%28B_32%29.jpg/960px-Gustave_Caillebotte_-_Jeune_homme_%C3%A0_sa_fen%C3%AAtre_%28B_32%29.jpg",
        ],
    },
}


#: FOURTH LEDGER — museum building photographs, 2026-08-08.
#:
#: Separate from the three above for the same reason they are separate from each
#: other. This is neither a rights correction (nothing here was a licence or
#: wrong-artwork problem) nor corpus growth (no artist, work or venue arrived)
#: nor a catalog batch (nothing moved surface). It is a *quality* remediation of
#: the building photographs themselves, following the measured audit in
#: docs/MUSEUM_PHOTO_AUDIT.md.
#:
#: THREE REPLACED. Each old file was an architectural detail that did not read as
#: the building: the Kunsthistorisches file, despite being named "Exterior…", is
#: a close-up of a marble inscription tablet; the Vatican and St Bavo files were
#: likewise fragments. Replacements are landscape exterior views, verified by
#: looking at each one rendered in a 16:10 card, not by filename.
#:
#: NINE ADDED. Venues that held catalogued works but had no photograph at all and
#: fell back to a generative canvas. Note which ones they were — Finland, Korea,
#: Poland, India, Turkey, Japan, Denmark, Switzerland, Italy: the venues holding
#: the atlas's non-Western and smaller-nation works were the ones missing
#: photographs.
#:
#: Every URL here had a `?utm_source=commons.wikimedia.org` tracking query string
#: when it came back from the Commons API. It is stripped. A campaign tag on a
#: shipped image URL is a third-party beacon, and this project self-hosts its
#: fonts specifically to avoid those. The inventory is what caught it: the tagged
#: URLs did not match their untagged rendered twins, so metadata_only_unique rose
#: from 1 to 13 and the discrepancy surfaced as a count.
#:
#: Effect: museum_photos_rendered 104 -> 113, total_unique 798 -> 807,
#: rendered_unique 797 -> 806. metadata_only_unique, catalog_gallery_overlap and
#: suppressed_leaking_into_metadata do not move; if any of them does, this change
#: introduced an asset it did not declare.
MUSEUM_PHOTOGRAPHS = {
    "museum_photos_rendered": {
        "removed": [
            U + "7/78/Gent-Sint-Baafskathedraal_vom_Belfried_aus_gesehen.jpg/960px-Gent-Sint-Baafskathedraal_vom_Belfried_aus_gesehen.jpg",
            U + "8/85/Museos_Vaticanos_-_Entrada_-_001.jpg/960px-Museos_Vaticanos_-_Entrada_-_001.jpg",
            U + "d/d4/AT_13763_Exterior_of_the_Kunsthistorisches_Museum%2C_Vienna-4.jpg/960px-AT_13763_Exterior_of_the_Kunsthistorisches_Museum%2C_Vienna-4.jpg",
        ],
        "added": [
            U + "0/0e/Istanbul_Beyoglu_Pera_museum.jpg/960px-Istanbul_Beyoglu_Pera_museum.jpg",
            U + "3/32/Front_view_of_national_museum_of_korea.jpg/960px-Front_view_of_national_museum_of_korea.jpg",
            U + "4/43/Ateneum_main_facade.jpg/960px-Ateneum_main_facade.jpg",
            U + "6/65/Gent_-_Sint-Baafskathedraal_%2848186851401%29.jpg/960px-Gent_-_Sint-Baafskathedraal_%2848186851401%29.jpg",
            U + "6/6e/WarsawNationalMuseumDSC_2528.JPG/960px-WarsawNationalMuseumDSC_2528.JPG",
            U + "9/91/Kunsthistorisches_Museum_Exterior.JPG/960px-Kunsthistorisches_Museum_Exterior.JPG",
            U + "a/a5/Tokyo_National_Museum%2C_Honkan_2010.jpg/960px-Tokyo_National_Museum%2C_Honkan_2010.jpg",
            U + "a/a7/Skagens_museum.jpg/960px-Skagens_museum.jpg",
            U + "a/ae/Basel_-_2017_-_Kunstmuseum_Basel_-_Neubau.jpg/960px-Basel_-_2017_-_Kunstmuseum_Basel_-_Neubau.jpg",
            U + "c/c8/Santa_Maria_Novella_%28Florence%29_-_Facade_%283%29.jpg/960px-Santa_Maria_Novella_%28Florence%29_-_Facade_%283%29.jpg",
            U + "d/df/Jaipur_House_2019_%282%29.jpg/960px-Jaipur_House_2019_%282%29.jpg",
            U + "f/f8/Vatican_Museums_entrance_2016.jpg/960px-Vatican_Museums_entrance_2016.jpg",
            # 2026-08-08, second pass: moa-museum-of-art. The first sweep left it
            # on a generative cover because every Commons file found was the
            # escalator tunnel. A second series (231007) turned out to hold real
            # exteriors, and this one is what both the English and Japanese
            # Wikipedia articles use as their lead. Every indexed venue now has a
            # building photograph; the generative fallback is unused.
            U + "2/2a/231007_MOA_Museum_of_Art_Atami_Japan09s3.jpg/960px-231007_MOA_Museum_of_Art_Atami_Japan09s3.jpg",
        ],
    },
    "prerender_metadata_refs": {
        "removed": [
            U + "7/78/Gent-Sint-Baafskathedraal_vom_Belfried_aus_gesehen.jpg/960px-Gent-Sint-Baafskathedraal_vom_Belfried_aus_gesehen.jpg",
            U + "8/85/Museos_Vaticanos_-_Entrada_-_001.jpg/960px-Museos_Vaticanos_-_Entrada_-_001.jpg",
            U + "d/d4/AT_13763_Exterior_of_the_Kunsthistorisches_Museum%2C_Vienna-4.jpg/960px-AT_13763_Exterior_of_the_Kunsthistorisches_Museum%2C_Vienna-4.jpg",
        ],
        "added": [
            U + "0/0e/Istanbul_Beyoglu_Pera_museum.jpg/960px-Istanbul_Beyoglu_Pera_museum.jpg",
            U + "3/32/Front_view_of_national_museum_of_korea.jpg/960px-Front_view_of_national_museum_of_korea.jpg",
            U + "4/43/Ateneum_main_facade.jpg/960px-Ateneum_main_facade.jpg",
            U + "6/65/Gent_-_Sint-Baafskathedraal_%2848186851401%29.jpg/960px-Gent_-_Sint-Baafskathedraal_%2848186851401%29.jpg",
            U + "6/6e/WarsawNationalMuseumDSC_2528.JPG/960px-WarsawNationalMuseumDSC_2528.JPG",
            U + "9/91/Kunsthistorisches_Museum_Exterior.JPG/960px-Kunsthistorisches_Museum_Exterior.JPG",
            U + "a/a5/Tokyo_National_Museum%2C_Honkan_2010.jpg/960px-Tokyo_National_Museum%2C_Honkan_2010.jpg",
            U + "a/a7/Skagens_museum.jpg/960px-Skagens_museum.jpg",
            U + "a/ae/Basel_-_2017_-_Kunstmuseum_Basel_-_Neubau.jpg/960px-Basel_-_2017_-_Kunstmuseum_Basel_-_Neubau.jpg",
            U + "c/c8/Santa_Maria_Novella_%28Florence%29_-_Facade_%283%29.jpg/960px-Santa_Maria_Novella_%28Florence%29_-_Facade_%283%29.jpg",
            U + "d/df/Jaipur_House_2019_%282%29.jpg/960px-Jaipur_House_2019_%282%29.jpg",
            U + "f/f8/Vatican_Museums_entrance_2016.jpg/960px-Vatican_Museums_entrance_2016.jpg",
            # 2026-08-08, second pass: moa-museum-of-art. The first sweep left it
            # on a generative cover because every Commons file found was the
            # escalator tunnel. A second series (231007) turned out to hold real
            # exteriors, and this one is what both the English and Japanese
            # Wikipedia articles use as their lead. Every indexed venue now has a
            # building photograph; the generative fallback is unused.
            U + "2/2a/231007_MOA_Museum_of_Art_Atami_Japan09s3.jpg/960px-231007_MOA_Museum_of_Art_Atami_Japan09s3.jpg",
        ],
    },
}


#: FIFTH LEDGER — artist share images, 2026-08-08 (owner decision).
#:
#: build_seo.jxa.js used to pick an artist's og:image by preferring any
#: catalogued work. That meant the share image silently moved the moment an
#: artist gained their first catalog record, and it had already moved for 49
#: artists: Leonardo's preview was not the Mona Lisa, Van Gogh's was not The
#: Starry Night, Munch's was not The Scream.
#:
#: The owner's ruling is that an artist keeps a designated hero. The artist
#: record's `works:[]` array is already an ordered, hand-made statement of which
#: pictures matter most, so the first listed work is treated as the designation,
#: with an optional `hero:` override. artistImage() now reads
#: hero -> works[] order -> any gallery image -> catalogued work.
#:
#: Nine of the twelve URLs below are ones CATALOG_BATCHES recorded as REMOVED
#: from the metadata surface. They were removed only because of the rule this
#: change reverses, so they return. That ledger is left exactly as written —
#: it is the true record of what the catalog batches did — and this one composes
#: on top of it. The order matters: batches took them out, the hero decision
#: puts them back.
#:
#: The other three (af Klint, Whistler, Cezanne) are works whose artists' own
#: `works[]` ordering now names them where the freeze had picked something else.
#:
#: No count moves. total_unique stays 807 and rendered_unique 806, because every
#: URL here is already a rendered gallery asset — this change alters WHICH
#: existing picture represents an artist, never how many pictures exist.
ARTIST_HEROES = {
    "prerender_metadata_refs": {
        "removed": [],
        "added": [
            "https://upload.wikimedia.org/wikipedia/commons/d/d7/4_hilma_af_klint%2C_the_ten_largest%2C_no_9.jpg",
            U + "1/17/Gustave_Caillebotte_-_Paris_Street%3B_Rainy_Day_-_Google_Art_Project.jpg/500px-Gustave_Caillebotte_-_Paris_Street%3B_Rainy_Day_-_Google_Art_Project.jpg",
            U + "1/1b/Whistlers_Mother_high_res.jpg/500px-Whistlers_Mother_high_res.jpg",
            U + "2/24/Riza-yi-Abbasi_008.jpg/960px-Riza-yi-Abbasi_008.jpg",
            U + "2/2f/Young_Girls.jpg/500px-Young_Girls.jpg",
            U + "3/38/Jan_Matejko%2C_Bitwa_pod_Grunwaldem.jpg/960px-Jan_Matejko%2C_Bitwa_pod_Grunwaldem.jpg",
            U + "7/7e/Die_Zwitscher-Maschine_%28Twittering_Machine%29%2C_1922_-_Paul_Klee.jpg/500px-Die_Zwitscher-Maschine_%28Twittering_Machine%29%2C_1922_-_Paul_Klee.jpg",
            U + "9/9c/Bada_Shanren_-_Fish_and_Rocks_-_1953.247_-_Cleveland_Museum_of_Art.tiff/lossy-page1-960px-Bada_Shanren_-_Fish_and_Rocks_-_1953.247_-_Cleveland_Museum_of_Art.tiff.jpg",
            U + "9/9e/Tizian_041.jpg/500px-Tizian_041.jpg",
            U + "a/af/La_Montagne_Sainte-Victoire_vue_de_la_carri%C3%A8re_Bib%C3%A9mus%2C_par_Paul_C%C3%A9zanne.jpg/960px-La_Montagne_Sainte-Victoire_vue_de_la_carri%C3%A8re_Bib%C3%A9mus%2C_par_Paul_C%C3%A9zanne.jpg",
            U + "d/d8/Gallen-Kallela_The_defence_of_the_Sampo.png/500px-Gallen-Kallela_The_defence_of_the_Sampo.png",
            U + "e/e9/Giotto_di_Bondone_-_Scenes_with_decorative_bands_-_WGA09284.jpg/500px-Giotto_di_Bondone_-_Scenes_with_decorative_bands_-_WGA09284.jpg",
        ],
    },
}


#: SIXTH LEDGER — the four painters the atlas already named, 2026-08-08.
#:
#: Backlog B3, and corpus growth rather than a correction: Giovanni Bellini,
#: Andrea del Verrocchio, Giorgio Vasari and Jean-Léon Gérôme. Each was cited in
#: Pigment's own prose — in another painter's life text, in a movement blurb, or
#: in the name of the curator role itself — with no record of their own.
#:
#: Kept separate from CONTENT_LANE, which records one specific commit (ef8b2b3)
#: and says so; folding a second growth event into it would make that entry a lie
#: about its own cause.
#:
#: 15 gallery images arrive, all public domain, all verified by rendering them
#: and looking. 4 artist stubs follow, each carrying its artist's first listed
#: work as og:image under the hero rule in ARTIST_HEROES above. Nothing moves on
#: the catalog surface: none of the four has a catalog record yet, so
#: catalog_gallery_overlap must stay at 115 — if it moves, a record was added
#: that this ledger did not declare.
B3_NAMED_PAINTERS = {
    "gallery_rendered": {
        "removed": [],
        "added": [
            U + "0/08/Giovanni_Bellini_St_Francis_in_Ecstasy.jpg/500px-Giovanni_Bellini_St_Francis_in_Ecstasy.jpg",
            U + "1/15/Workshop_of_Andrea_del_Verrocchio._Tobias_and_the_Angel._33x26cm._1470-75._NG_London.jpg/500px-Workshop_of_Andrea_del_Verrocchio._Tobias_and_the_Angel._33x26cm._1470-75._NG_London.jpg",
            U + "1/17/Madonna-with-Child-by-Verrocchio.jpg/500px-Madonna-with-Child-by-Verrocchio.jpg",
            U + "4/48/Vasari-Lorenzo.jpg/500px-Vasari-Lorenzo.jpg",
            U + "5/52/Jean-L%C3%A9on_G%C3%A9r%C3%B4me_-_Bonaparte_Before_the_Sphinx.jpg/500px-Jean-L%C3%A9on_G%C3%A9r%C3%B4me_-_Bonaparte_Before_the_Sphinx.jpg",
            U + "6/60/Pala_di_san_zaccaria_01.jpg/500px-Pala_di_san_zaccaria_01.jpg",
            U + "6/6b/Giovanni_Bellini%2C_portrait_of_Doge_Leonardo_Loredan.jpg/500px-Giovanni_Bellini%2C_portrait_of_Doge_Leonardo_Loredan.jpg",
            U + "9/98/Vasari%2C_perseo_e_andromeda%2C_studiolo.jpg/500px-Vasari%2C_perseo_e_andromeda%2C_studiolo.jpg",
            U + "a/a9/Jean-L%C3%A9on_G%C3%A9r%C3%B4me_-_Le_charmeur_de_serpents.jpg/500px-Jean-L%C3%A9on_G%C3%A9r%C3%B4me_-_Le_charmeur_de_serpents.jpg",
            U + "b/bc/Andrea_del_Verrocchio%2C_Leonardo_da_Vinci_-_Baptism_of_Christ_-_Uffizi.jpg/500px-Andrea_del_Verrocchio%2C_Leonardo_da_Vinci_-_Baptism_of_Christ_-_Uffizi.jpg",
            U + "c/c3/Cleopatra_and_Caesar_by_Jean-Leon-Gerome.jpg/500px-Cleopatra_and_Caesar_by_Jean-Leon-Gerome.jpg",
            U + "c/c5/Jean-Leon_Gerome_Pollice_Verso.jpg/500px-Jean-Leon_Gerome_Pollice_Verso.jpg",
            U + "d/d7/Feast_of_the_Gods_Giovanni_Bellini_1514.jpg/500px-Feast_of_the_Gods_Giovanni_Bellini_1514.jpg",
            U + "d/d9/Italien_humanists_by_Giorgio_Vasari.jpg/500px-Italien_humanists_by_Giorgio_Vasari.jpg",
            U + "e/ea/Giorgio_Vasari_-_Self-Portrait_-_WGA24284.jpg/500px-Giorgio_Vasari_-_Self-Portrait_-_WGA24284.jpg",
            # second pass, same B3 event: Orozco, Siqueiros, Mehoffer and
            # Aliye Berger. Only 7 images arrive for 4 painters, because
            # Siqueiros (d. 1974) and Berger (d. 1974) are still in copyright
            # and carry generative covers with no reproduction — which is why
            # only 2 of the 4 new stubs contribute an og:image.
            U + "3/38/Jos%C3%A9_Clemente_Orozco%2C_Zapatistas%2C_1931%2C_MoMA.jpg/500px-Jos%C3%A9_Clemente_Orozco%2C_Zapatistas%2C_1931%2C_MoMA.jpg",
            U + "4/43/J%C3%B3zef_Mehoffer_-_Self-portrait_-_MP_403_MNW_-_National_Museum_in_Warsaw.jpg/500px-J%C3%B3zef_Mehoffer_-_Self-portrait_-_MP_403_MNW_-_National_Museum_in_Warsaw.jpg",
            U + "9/90/J%C3%B3zef_Mehoffer_-_Zinnias_-_MP_4274_MNW_-_National_Museum_in_Warsaw.jpg/500px-J%C3%B3zef_Mehoffer_-_Zinnias_-_MP_4274_MNW_-_National_Museum_in_Warsaw.jpg",
            U + "9/96/Jos%C3%A9_Clemente_Orozco%2C_The_Subway.jpg/500px-Jos%C3%A9_Clemente_Orozco%2C_The_Subway.jpg",
            U + "b/b7/Jos%C3%A9_Clemente_Orozco%2C_Barricade.jpg/500px-Jos%C3%A9_Clemente_Orozco%2C_Barricade.jpg",
            U + "e/e2/Prometheus_%281930%29_de_Jos%C3%A9_Clemente_Orozco_en_Pomona_College.jpg/500px-Prometheus_%281930%29_de_Jos%C3%A9_Clemente_Orozco_en_Pomona_College.jpg",
            U + "e/e9/J%C3%B3zef_Mehoffer_-_Dziwny_ogr%C3%B3d.jpg/500px-J%C3%B3zef_Mehoffer_-_Dziwny_ogr%C3%B3d.jpg",
        ],
    },
    "prerender_metadata_refs": {
        "removed": [],
        "added": [
            U + "6/6b/Giovanni_Bellini%2C_portrait_of_Doge_Leonardo_Loredan.jpg/500px-Giovanni_Bellini%2C_portrait_of_Doge_Leonardo_Loredan.jpg",
            U + "a/a9/Jean-L%C3%A9on_G%C3%A9r%C3%B4me_-_Le_charmeur_de_serpents.jpg/500px-Jean-L%C3%A9on_G%C3%A9r%C3%B4me_-_Le_charmeur_de_serpents.jpg",
            U + "b/bc/Andrea_del_Verrocchio%2C_Leonardo_da_Vinci_-_Baptism_of_Christ_-_Uffizi.jpg/500px-Andrea_del_Verrocchio%2C_Leonardo_da_Vinci_-_Baptism_of_Christ_-_Uffizi.jpg",
            U + "d/d9/Italien_humanists_by_Giorgio_Vasari.jpg/500px-Italien_humanists_by_Giorgio_Vasari.jpg",
            # second pass, same B3 event: Orozco, Siqueiros, Mehoffer and
            # Aliye Berger. Only 7 images arrive for 4 painters, because
            # Siqueiros (d. 1974) and Berger (d. 1974) are still in copyright
            # and carry generative covers with no reproduction — which is why
            # only 2 of the 4 new stubs contribute an og:image.
            U + "3/38/Jos%C3%A9_Clemente_Orozco%2C_Zapatistas%2C_1931%2C_MoMA.jpg/500px-Jos%C3%A9_Clemente_Orozco%2C_Zapatistas%2C_1931%2C_MoMA.jpg",
            U + "e/e9/J%C3%B3zef_Mehoffer_-_Dziwny_ogr%C3%B3d.jpg/500px-J%C3%B3zef_Mehoffer_-_Dziwny_ogr%C3%B3d.jpg",
        ],
    },
}


#: SEVENTH LEDGER — A3, the Orientalism correction, 2026-08-08.
#:
#: The atlas applied `orientalism` to two Ottoman painters and one Indian one
#: and contained no actual European Orientalists — so the movement described
#: nobody in it and mislabelled everybody in it. Osman Hamdi Bey's tagline read
#: "Orientalism, corrected from the inside" while his movements array filed him
#: AS an Orientalist.
#:
#: Owner decision: add the real ones, then re-file the three. John Frederick
#: Lewis and Ludwig Deutsch join Gérôme, and Şeker Ahmed Paşa, Osman Hamdi Bey
#: and Raja Ravi Varma move to `academicism` — which is where they belong on the
#: evidence, since two of the three were taught by Gérôme inside that system.
#:
#: Only the two new painters bring images; the re-filing moves no asset at all.
#: 6 gallery images, 2 stubs. catalog_gallery_overlap stays 115.
A3_ORIENTALISM = {
    "gallery_rendered": {
        "removed": [],
        "added": [
            U + "0/02/John_Frederick_Lewis_-_Sheik_Hussein_of_Gebel_Tor_and_His_Son_-_Google_Art_Project.jpg/500px-John_Frederick_Lewis_-_Sheik_Hussein_of_Gebel_Tor_and_His_Son_-_Google_Art_Project.jpg",
            U + "0/0c/John_frederick_lewis-reception1873.jpg/500px-John_frederick_lewis-reception1873.jpg",
            U + "4/40/John_Frederick_Lewis_-_Hhareem_Life%2C_Constantinople.jpg/500px-John_Frederick_Lewis_-_Hhareem_Life%2C_Constantinople.jpg",
            U + "8/86/Ludwig_Deutsch_-_The_Girl_with_the_Buffalo.jpg/500px-Ludwig_Deutsch_-_The_Girl_with_the_Buffalo.jpg",
            U + "a/ac/John_Frederick_Lewis_%281804-1876%29_-_Indoor_Gossip%2C_Cairo_-_O.1961.1_-_Whitworth_Art_Gallery.jpg/500px-John_Frederick_Lewis_%281804-1876%29_-_Indoor_Gossip%2C_Cairo_-_O.1961.1_-_Whitworth_Art_Gallery.jpg",
            U + "f/f0/Ludwig_Deutsch-_The_Palace_Guard.jpg/500px-Ludwig_Deutsch-_The_Palace_Guard.jpg",
        ],
    },
    "prerender_metadata_refs": {
        "removed": [],
        "added": [
            U + "0/0c/John_frederick_lewis-reception1873.jpg/500px-John_frederick_lewis-reception1873.jpg",
            U + "f/f0/Ludwig_Deutsch-_The_Palace_Guard.jpg/500px-Ludwig_Deutsch-_The_Palace_Guard.jpg",
        ],
    },
}


#: EIGHTH LEDGER — Actuality expansion, 2026-08-12.
#:
#: The owner's direction: an Actuality list may add whatever the atlas needs to
#: answer the story properly, rather than being limited to what is already here.
#: News as an acquisition driver.
#:
#: Two lists. The LeBron entry grew from 6 works to 10 with side-plots — the
#: helicopter commute (Bruegel's Icarus), the arena's five names (Bruegel's Tower
#: of Babel), the Hinkie Process (Bruegel's Hunters in the Snow) and Embiid
#: (Enwonwu's Tutu). A second list answers INPE's Amazon deforestation figures
#: with Rousseau, Tarsila do Amaral, Bosch, af Klint and Klimt.
#:
#: Only TWO images arrive, both Rousseau, and only ONE is new to the atlas —
#: Surprised! was already in his gallery pool, so catalog_gallery_overlap moves
#: 115 -> 116 while total_unique moves 836 -> 837. Everything else was either
#: already catalogued or is in copyright: Tutu (d. 1994) and Abaporu (d. 1973)
#: carry no reproduction, which is why copyright_refs moves 66 -> 68 and the
#: rendered surfaces do not move for them at all.
ACTUALITY_EXPANSION = {
    "catalog_pd_rendered": {
        "removed": [],
        "added": [
            U + "1/16/Henri_Rousseau_005.jpg/500px-Henri_Rousseau_005.jpg",
            U + "f/fa/Surprised-Rousseau.jpg/500px-Surprised-Rousseau.jpg",
        ],
    },
    "prerender_metadata_refs": {
        "removed": [],
        "added": [
            U + "1/16/Henri_Rousseau_005.jpg/500px-Henri_Rousseau_005.jpg",
            U + "f/fa/Surprised-Rousseau.jpg/500px-Surprised-Rousseau.jpg",
        ],
    },
}


#: NINTH LEDGER — A2, the wrong-artwork replacements, 2026-08-12.
#:
#: IMAGE_RIGHTS_ROUTES.md §1.6 records 20 confirmed mismatches. C1 was fixed
#: earlier; twelve more are fixed here, and SEVEN remain — they are listed in
#: BACKLOG A2 and are still wrong on the live site.
#:
#: Every replacement was chosen by rendering it and looking at it, and every one
#: passed a guard that a proposed file must differ from the file it replaces.
#: That guard exists because an earlier automated pass proposed two records'
#: own defects back at them: Commons ranks the existing wrong file first
#: PRECISELY because it is titled after the artist and work being searched, the
#: same property that hid these from the suspect detector to begin with.
#:
#: One half-fix was caught by the inventory rather than by me. Ogata Korin's
#: Irises exists twice — a gallery entry and a catalog record — and fixing only
#: the gallery left the catalog still showing Van Gogh's Irises.
#: catalog_gallery_overlap fell 116 -> 115 and named the problem. Both are fixed,
#: and the overlap is back at 116.
#:
#: A pure swap: 12 out and 12 in on the gallery surface, 1 for 1 on catalog,
#: 3 for 3 on the stubs. No count moves.
A2_WRONG_ARTWORKS = {
    "gallery_rendered": { "removed": [
            U + "3/36/Gustave_Moreau_-_%C3%89tude_t%C3%AAte_d%27%C5%92dipe.JPG/500px-Gustave_Moreau_-_%C3%89tude_t%C3%AAte_d%27%C5%92dipe.JPG",
            U + "3/38/Young_Woman_Powdering_Herself_Georges_Seurat.jpg/500px-Young_Woman_Powdering_Herself_Georges_Seurat.jpg",
            U + "3/3e/Irises-Vincent_van_Gogh.jpg/500px-Irises-Vincent_van_Gogh.jpg",
            U + "4/42/Portrait_Anne_of_Cleves_by_Hans_Holbein_the_Younger_%28Louvre%29.jpg/500px-Portrait_Anne_of_Cleves_by_Hans_Holbein_the_Younger_%28Louvre%29.jpg",
            U + "6/6d/Cha%C3%AFm_Soutine_-_Vue_de_C%C3%A9ret.jpg/500px-Cha%C3%AFm_Soutine_-_Vue_de_C%C3%A9ret.jpg",
            U + "7/72/Lucas_Cranach_d.%C3%84._-_Bildnis_der_Prinzessin_Sibylle_von_Cleve_%281526%2C_Klassik_Stiftung_Weimar%29.jpg/960px-Lucas_Cranach_d.%C3%84._-_Bildnis_der_Prinzessin_Sibylle_von_Cleve_%281526%2C_Klassik_Stiftung_Weimar%29.jpg",
            U + "8/86/Paula_Modersohn-Becker_001.jpg/500px-Paula_Modersohn-Becker_001.jpg",
            U + "a/a3/Forest%2C_a_painting_by_Paul_C%C3%A9zanne%2C_circa_1902-1904.png/500px-Forest%2C_a_painting_by_Paul_C%C3%A9zanne%2C_circa_1902-1904.png",
            U + "a/a8/George_Stubbs_-_self_portrait.jpg/500px-George_Stubbs_-_self_portrait.jpg",
            U + "b/b5/Composition_%281917%29_-_Liubova_Popova_%281889-1924%29_%2845056449312%29.jpg/960px-Composition_%281917%29_-_Liubova_Popova_%281889-1924%29_%2845056449312%29.jpg",
            U + "b/b8/Hiroshige_Van_Gogh_2.JPG/500px-Hiroshige_Van_Gogh_2.JPG",
            U + "d/dc/Amalie_Kaercher_-_A_Flower_Still_Life_with_Grapes%2C_1857.jpg/500px-Amalie_Kaercher_-_A_Flower_Still_Life_with_Grapes%2C_1857.jpg",
        ], "added": [
            U + "0/04/Adam_and_Eve_%28UK_CIA_P-1947-LF-77%29.jpg/500px-Adam_and_Eve_%28UK_CIA_P-1947-LF-77%29.jpg",
            U + "0/04/Henry_VIII_of_England%2C_by_Hans_Holbein.jpg/500px-Henry_VIII_of_England%2C_by_Hans_Holbein.jpg",
            U + "1/13/Fabric_Designs_by_Popova_04.jpg/500px-Fabric_Designs_by_Popova_04.jpg",
            U + "2/2a/Amedeo_Modigliani_-_Chaim_Soutine_%281917%29.jpg/500px-Amedeo_Modigliani_-_Chaim_Soutine_%281917%29.jpg",
            U + "2/2f/Gustave_Moreau_-_Oedipus_and_the_Sphinx_-_WGA16201.jpg/500px-Gustave_Moreau_-_Oedipus_and_the_Sphinx_-_WGA16201.jpg",
            U + "4/45/George_Stubbs_-_Horse_Devoured_by_a_Lion_-_Google_Art_Project.jpg/500px-George_Stubbs_-_Horse_Devoured_by_a_Lion_-_Google_Art_Project.jpg",
            U + "4/46/Irises_screen_2.jpg/500px-Irises_screen_2.jpg",
            U + "4/48/Paula_Moderson-Becker_-_Selbstbildnis_am_6_Hochzeitstag_-_1906.jpeg/500px-Paula_Moderson-Becker_-_Selbstbildnis_am_6_Hochzeitstag_-_1906.jpeg",
            U + "9/90/Morisot_jeune_femme_se_poudrant.jpg/500px-Morisot_jeune_femme_se_poudrant.jpg",
            U + "c/cc/Hiroshige_Atake_sous_une_averse_soudaine.jpg/500px-Hiroshige_Atake_sous_une_averse_soudaine.jpg",
            U + "d/d7/Rachel_Ruysch_-_Still-Life_with_Flowers_-_WGA20555.jpg/500px-Rachel_Ruysch_-_Still-Life_with_Flowers_-_WGA20555.jpg",
            U + "d/db/Ahmed-Forest.jpg/500px-Ahmed-Forest.jpg",
        ] },
    "catalog_pd_rendered": { "removed": [
            U + "3/3e/Irises-Vincent_van_Gogh.jpg/500px-Irises-Vincent_van_Gogh.jpg",
        ], "added": [
            U + "4/46/Irises_screen_2.jpg/500px-Irises_screen_2.jpg",
        ] },
    "prerender_metadata_refs": { "removed": [
            U + "3/3e/Irises-Vincent_van_Gogh.jpg/500px-Irises-Vincent_van_Gogh.jpg",
            U + "8/86/Paula_Modersohn-Becker_001.jpg/500px-Paula_Modersohn-Becker_001.jpg",
            U + "d/dc/Amalie_Kaercher_-_A_Flower_Still_Life_with_Grapes%2C_1857.jpg/500px-Amalie_Kaercher_-_A_Flower_Still_Life_with_Grapes%2C_1857.jpg",
        ], "added": [
            U + "4/46/Irises_screen_2.jpg/500px-Irises_screen_2.jpg",
            U + "4/48/Paula_Moderson-Becker_-_Selbstbildnis_am_6_Hochzeitstag_-_1906.jpeg/500px-Paula_Moderson-Becker_-_Selbstbildnis_am_6_Hochzeitstag_-_1906.jpeg",
            U + "d/d7/Rachel_Ruysch_-_Still-Life_with_Flowers_-_WGA20555.jpg/500px-Rachel_Ruysch_-_Still-Life_with_Flowers_-_WGA20555.jpg",
        ] },
}


#: TENTH LEDGER — A2 completed, 2026-08-12. All twenty are now resolved.
#:
#: The last seven could not be fixed by swapping an image, because for five of
#: them the work the record NAMED has no public-domain photograph on Commons at
#: all. So the record was retitled to a work that does — the same remedy Sorolla's
#: Vision of Spain needed:
#:
#:   claude-lorrain   The Enchanted Castle    -> Landscape with Narcissus and Echo
#:   reza-abbasi      Portrait of a Dervish   -> Young Man with a Sword (Detroit)
#:   nicolas-poussin  The Four Seasons        -> The Adoration of the Golden Calf
#:   emily-carr       Big Raven               -> Forest, British Columbia
#:   mihri-musfik     Self-Portrait           -> Portrait of a Woman
#:
#: And two have NO usable image in any form, so the gallery entry is removed and
#: the work keeps its place in the artist's works[] with no picture — which is
#: the honest state, not a gap:
#:
#:   sesshu-toyo      Winter Landscape   (no PD Sesshu on Commons at all)
#:   xu-beihong       Galloping Horse    (his paintings are not on Commons as PD)
#:
#: 5 in, 7 out. total_unique 837 -> 835, rendered 836 -> 834, overlap unmoved.
A2_RETITLES = {
    "gallery_rendered": { "removed": [
            "https://upload.wikimedia.org/wikipedia/commons/0/05/Muybridge_race_horse_animated_184px.gif",
            "https://upload.wikimedia.org/wikipedia/commons/b/ba/Emily_Carr_Canada_stamp_1971.jpg",
            U + "6/6a/Francis_Danby_%281793-1861%29_-_The_Enchanted_Castle_-_FA.66%28O%29_-_Victoria_and_Albert_Museum.jpg/500px-Francis_Danby_%281793-1861%29_-_The_Enchanted_Castle_-_FA.66%28O%29_-_Victoria_and_Albert_Museum.jpg",
            U + "7/74/Mihri_Han%C4%B1m_-_Leyla_Turgut_Portresi.jpg/500px-Mihri_Han%C4%B1m_-_Leyla_Turgut_Portresi.jpg",
            U + "7/75/Winter_Landscape_with_Brabrand_Church.jpg/500px-Winter_Landscape_with_Brabrand_Church.jpg",
            U + "d/d9/Nicolas_Poussin_078.jpg/500px-Nicolas_Poussin_078.jpg",
            U + "e/e9/Portrait_of_the_artist_Reza_%27Abbasi_by_Mu%27in_Musavvir%2C_Isfahan%2C_Iran%2C_signed_and_dated_19_April_1676.jpg/960px-Portrait_of_the_artist_Reza_%27Abbasi_by_Mu%27in_Musavvir%2C_Isfahan%2C_Iran%2C_signed_and_dated_19_April_1676.jpg",
        ], "added": [
            "https://upload.wikimedia.org/wikipedia/commons/5/5f/Painting_by_Mihri_M%C3%BC%C5%9Ffik.jpg",
            U + "5/51/Riza-i_Abbasi_Young_Man_with_a_Sword_-_Detroit_Institute_of_Arts.jpg/500px-Riza-i_Abbasi_Young_Man_with_a_Sword_-_Detroit_Institute_of_Arts.jpg",
            U + "6/65/Landscape_with_Narcissus_and_Echo.jpg/500px-Landscape_with_Narcissus_and_Echo.jpg",
            U + "9/95/Emily_Carr_%281931%E2%80%9332%29_Forest%2C_British_Columbia.jpg/500px-Emily_Carr_%281931%E2%80%9332%29_Forest%2C_British_Columbia.jpg",
            U + "b/b2/The_Adoration_of_the_Golden_Calf_%E2%80%93_Nicolas_Poussin.jpg/500px-The_Adoration_of_the_Golden_Calf_%E2%80%93_Nicolas_Poussin.jpg",
        ] },
    "prerender_metadata_refs": { "removed": [
            "https://upload.wikimedia.org/wikipedia/commons/0/05/Muybridge_race_horse_animated_184px.gif",
            "https://upload.wikimedia.org/wikipedia/commons/b/ba/Emily_Carr_Canada_stamp_1971.jpg",
            U + "7/74/Mihri_Han%C4%B1m_-_Leyla_Turgut_Portresi.jpg/500px-Mihri_Han%C4%B1m_-_Leyla_Turgut_Portresi.jpg",
        ], "added": [
            "https://upload.wikimedia.org/wikipedia/commons/5/5f/Painting_by_Mihri_M%C3%BC%C5%9Ffik.jpg",
            U + "9/95/Emily_Carr_%281931%E2%80%9332%29_Forest%2C_British_Columbia.jpg/500px-Emily_Carr_%281931%E2%80%9332%29_Forest%2C_British_Columbia.jpg",
            U + "b/b1/Xu_Beihong_yugongyishan.jpg/960px-Xu_Beihong_yugongyishan.jpg",
        ] },
}

#: Catalog Batch 03 (docs/CATALOG_BATCH_03.md), 2026-08-24 — js/catalog-6.js.
#: Twelve works by twelve painters the atlas already leaned on and could not
#: show a picture by, selected on measured inbound gravity. Backlog E1.
#:
#: NO NEW ARTWORK IMAGE ENTERS THE TREE. All twelve were already js/artworks.js
#: gallery entries, audited and rendering on artist pages; a catalog record
#: moves an image onto a second surface rather than adding an asset. So
#: catalog_pd_rendered gains 12 and catalog_gallery_overlap moves with it, while
#: total_unique and rendered_unique do not move for any of them. Same behaviour
#: as the 22 records of Batch 01/02 above, and the reason a catalog batch is the
#: cheapest honest way to grow the atlas.
#:
#: The two MUSEUM photographs below are a different matter and are the batch's
#: only new assets: total_unique 835 -> 837, rendered_unique 834 -> 836.
#:
#: The prerender surface moves by FOUR, not twelve, and the arithmetic is worth
#: keeping. Each artwork stub carries its own og:image, but build_seo.jxa.js
#: also uses a pd catalog work as its artist's stub hero — so for eight of these
#: twelve the URL was already on the metadata surface before the record existed.
#: The four that were not are Rubens, Gérôme, Marc and Mondrian, whose artist
#: heroes are other paintings (Rubens's is the CC BY Descent from the Cross,
#: which is why it was never a catalog candidate). Plus the two museum
#: photographs below: 4 + 2 = 6.
CATALOG_BATCH_03 = {
    "catalog_pd_rendered": { "removed": [], "added": [
            U + "0/02/La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg/500px-La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg",
            U + "3/32/Franz_Marc-The_fate_of_the_animals-1913.jpg/500px-Franz_Marc-The_fate_of_the_animals-1913.jpg",
            U + "5/5e/John_Constable_-_The_Hay_Wain_%281821%29.jpg/500px-John_Constable_-_The_Hay_Wain_%281821%29.jpg",
            U + "8/80/Piet_Mondrian%2C_1911%2C_Gray_Tree_%28De_grijze_boom%29%2C_oil_on_canvas%2C_79.7_x_109.1_cm%2C_Gemeentemuseum_Den_Haag%2C_Netherlands.jpg/500px-Piet_Mondrian%2C_1911%2C_Gray_Tree_%28De_grijze_boom%29%2C_oil_on_canvas%2C_79.7_x_109.1_cm%2C_Gemeentemuseum_Den_Haag%2C_Netherlands.jpg",
            U + "8/82/Camille_Pissarro%2C_The_Boulevard_Montmartre_at_Night%2C_1897.jpg/960px-Camille_Pissarro%2C_The_Boulevard_Montmartre_at_Night%2C_1897.jpg",
            U + "a/a4/Madame_X_%28Madame_Pierre_Gautreau%29%2C_John_Singer_Sargent%2C_1884_%28unfree_frame_crop%29.jpg/960px-Madame_X_%28Madame_Pierre_Gautreau%29%2C_John_Singer_Sargent%2C_1884_%28unfree_frame_crop%29.jpg",
            U + "a/ae/Portrait_de_Charles_1er%2C_roi_d%27Angleterre%2C_%C3%A0_la_chasse_-_Antoon_van_Dyck_-_Mus%C3%A9e_du_Louvre_Peintures_INV_1236_%3B_MR_666.jpg/500px-Portrait_de_Charles_1er%2C_roi_d%27Angleterre%2C_%C3%A0_la_chasse_-_Antoon_van_Dyck_-_Mus%C3%A9e_du_Louvre_Peintures_INV_1236_%3B_MR_666.jpg",
            U + "c/c5/Jean-Leon_Gerome_Pollice_Verso.jpg/500px-Jean-Leon_Gerome_Pollice_Verso.jpg",
            U + "d/d9/El_Jard%C3%ADn_del_Amor_%28Rubens%29.jpg/500px-El_Jard%C3%ADn_del_Amor_%28Rubens%29.jpg",
            U + "d/df/La_grande_odalisque_-_Jean-Auguste_Dominique_Ingres_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1158.jpg/500px-La_grande_odalisque_-_Jean-Auguste_Dominique_Ingres_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1158.jpg",
            U + "d/df/Nicolas_Poussin_-_Et_in_Arcadia_ego_%28deuxi%C3%A8me_version%29.jpg/960px-Nicolas_Poussin_-_Et_in_Arcadia_ego_%28deuxi%C3%A8me_version%29.jpg",
            U + "e/e4/Henri_de_Toulouse-Lautrec%2C_At_the_Moulin_Rouge.jpg/500px-Henri_de_Toulouse-Lautrec%2C_At_the_Moulin_Rouge.jpg",
        ] },
    #: Two venues the batch had to open, because Pollice Verso and Gray Tree are
    #: held by museums the registry did not contain — the E3 gap, met head on
    #: rather than dodged by picking easier paintings. Both notes carry a
    #: building photograph and both photographs require attribution (CC BY-SA
    #: 2.0 Chanel Wheeler; CC BY-SA 4.0 Choinowski), credited in
    #: js/photo-credits.js. The Den Haag file was picked by LOOKING at it: the
    #: obvious candidate, "Den Haag - Gemeentemuseum (39788683042).jpg", is a
    #: painting hanging inside the building, not the building.
    "museum_photos_rendered": { "removed": [], "added": [
            U + "2/27/Main_entrance_to_Phoenix_Art_Museum_-_19_June_2008.jpg/960px-Main_entrance_to_Phoenix_Art_Museum_-_19_June_2008.jpg",
            U + "3/3e/Kunstmuseum_Den_Haag.jpg/960px-Kunstmuseum_Den_Haag.jpg",
        ] },
    "prerender_metadata_refs": { "removed": [], "added": [
            U + "2/27/Main_entrance_to_Phoenix_Art_Museum_-_19_June_2008.jpg/960px-Main_entrance_to_Phoenix_Art_Museum_-_19_June_2008.jpg",
            U + "3/32/Franz_Marc-The_fate_of_the_animals-1913.jpg/500px-Franz_Marc-The_fate_of_the_animals-1913.jpg",
            U + "3/3e/Kunstmuseum_Den_Haag.jpg/960px-Kunstmuseum_Den_Haag.jpg",
            U + "8/80/Piet_Mondrian%2C_1911%2C_Gray_Tree_%28De_grijze_boom%29%2C_oil_on_canvas%2C_79.7_x_109.1_cm%2C_Gemeentemuseum_Den_Haag%2C_Netherlands.jpg/500px-Piet_Mondrian%2C_1911%2C_Gray_Tree_%28De_grijze_boom%29%2C_oil_on_canvas%2C_79.7_x_109.1_cm%2C_Gemeentemuseum_Den_Haag%2C_Netherlands.jpg",
            U + "c/c5/Jean-Leon_Gerome_Pollice_Verso.jpg/500px-Jean-Leon_Gerome_Pollice_Verso.jpg",
            U + "d/d9/El_Jard%C3%ADn_del_Amor_%28Rubens%29.jpg/500px-El_Jard%C3%ADn_del_Amor_%28Rubens%29.jpg",
        ] },
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
                for ledger in (CORRECTIONS, CONTENT_LANE, CATALOG_BATCHES, CATALOG_BATCH_03, MUSEUM_PHOTOGRAPHS, ARTIST_HEROES, B3_NAMED_PAINTERS, A3_ORIENTALISM, ACTUALITY_EXPANSION, A2_WRONG_ARTWORKS, A2_RETITLES):
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
        # 798 -> 807: the museum-photograph remediation of 2026-08-08 (fourth
        # ledger above) replaced three detail shots and added nine photographs to
        # venues that had none. +12 -3 = +9 on both total and rendered; nothing
        # else moves. Full measurement: docs/MUSEUM_PHOTO_AUDIT.md.
        # 835 -> 837 and 834 -> 836: Catalog Batch 03 opened two venues the
        # registry did not hold — Phoenix Art Museum and Kunstmuseum Den Haag —
        # and their building photographs are the ONLY genuinely new assets in
        # that batch. Its twelve artworks moved no total at all: every one was
        # already a js/artworks.js gallery image, so they land on
        # catalog_gallery_overlap instead.
        self.assertEqual(c["total_unique"], 837)   # +2: the two new museum photographs
        self.assertEqual(c["rendered_unique"], 836)   # +2: the same, both rendered
        self.assertEqual(c["metadata_only_unique"], 1)   # unchanged: the homepage og:image
        # 116 -> 128: Batch 03's twelve records, each drawn from the gallery
        # pool. This number moving while total_unique holds is the signature of
        # a catalog batch done from the audited pool rather than from new images.
        self.assertEqual(c["catalog_gallery_overlap"], 128)   # +12: Catalog Batch 03
        self.assertEqual(c["suppressed_leaking_into_metadata"], 0)  # unchanged, and must stay 0
        # 60 -> 66: ef8b2b3's six 20th-century works, all image:{status:"copyright"}
        # with no src — beginning-noland, chief-kline, city-limits-guston,
        # elegy-to-the-spanish-republic-108, mars-dust, the-gate-hofmann. A rise
        # here is correct behaviour: it means works that may not be rendered were
        # recorded as such rather than silently given an image.
        # 66 -> 67: the Actuality expansion of 2026-08-12 added Enwonwu's Tutu,
        # the catalog's first African record. He died in 1994, so it carries
        # image:{status:"copyright"} with no src — which is why this number moves
        # and total_unique/rendered_unique do not. A record that added a picture
        # would have moved those too.
        self.assertEqual(c["copyright_refs"], 68)


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
        self.assertEqual(len(rr.SURFACES["catalog"]()), 294)   # +12: Catalog Batch 03
        # 103 -> 104 at ef8b2b3: the Hirshhorn Museum and Sculpture Garden note,
        # which arrived with Noland's "Beginning". Credited in js/photo-credits.js
        # (Quadell, CC BY-SA 3.0, attribution required). Unit 35, D-019.
        self.assertEqual(len(rr.SURFACES["museum"]()), 116)   # +2: Phoenix, Kunstmuseum Den Haag
        # 532 -> 528: the three Kahlo records and the duplicate Bada Shanren
        # "Two Birds" record were removed as confirmed wrong-artwork images.
        self.assertEqual(len(rr.SURFACES["gallery"]()), 554)


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

    Unit 36 widened the scope to `js/app.js`. Unit 35 corrected fourteen
    statements in evidence and docs and left the one breach that a visitor
    actually reads — the `#/credits` lede — standing, because no scanned path
    reached the shipped copy. Evidence disciplined, shipped prose not, is the
    inversion this class exists to prevent, so the file that renders the pages
    is now scanned whole: string literals and code comments alike, since both
    are prose this pole wrote. Only `app.js` is scanned, not all of `js/`; the
    data registries are generated records, governed by TestRegisterLanguage.

    Scope is otherwise limited to artifacts THIS pole authors and may edit.
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
        # NOT on main. Three evidence artifacts carried one sanctioned marker
        # each and were pinned here, but they live only on the unmerged branch
        # `pig-001-stabilization` (95e5636, a71e2c5, fb8ba6e) — this test file
        # reached main without them, so the pin has asserted three markers that
        # no scanned file could supply, and this test has failed on main ever
        # since. Their justifications are kept below so a future merge restores
        # them deliberately rather than rediscovering them; until then they are
        # not entries, because a pin must describe the tree it runs against:
        #   evidence/data-reconciliation.md      1  names the marker while
        #       documenting the mechanism (D-019, §2.2)
        #   evidence/harness/vermeer-cert/gapfill.py  1  unit 37 (F-9): quotes
        #       unit 36's superseded #/credits lede as a negative control — the
        #       harness asserts the DOM does NOT contain it
        #   evidence/build-log-unit-37.md        1  names the marker while
        #       recording what unit 37 added and why; exempts no phrase of its own
        # 6 fixture phrases in test_the_guard_actually_catches..., plus this
        # class's own docstring, this map's comment, and the two lines that
        # implement and count the marker. All self-referential; none is prose.
        # +1 in unit 36: the shipped #/credits lede added as a catch fixture
        "tests/test_rights_tooling.py": 13,
        # 2 lines that quote a banned phrase in order to argue against it: the
        # §0 note explaining why the CLEARED label was rejected (it must show
        # the ambiguity to make the case), and the jurisdiction paragraph
        # stating the flat assertion in order to show it has no single truth
        # value. Both carry the marker as an HTML comment, invisible when the
        # Markdown renders. Neither asserts anything about a Pigment image.
        "docs/IMAGE_RIGHTS_ROUTES.md": 2,
        # names the marker once while recording the two entries above and why,
        # exactly as the evidence artifacts did. Exempts no phrase of its own.
        "docs/corrections/tooling-repairs.md": 1,
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
        ROOT / "js" / "app.js",          # unit 36: the copy users actually read
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
                       "the image is rights-cleared",                      # OD5-EXEMPT
                       # unit 36: the shipped #/credits lede, verbatim
                       "Most reproductions here are public domain."):      # OD5-EXEMPT
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
                       "resolution: asserted-by-commons; no legal conclusion",
                       # unit 36: the replacement lede, verbatim
                       "Most reproductions here carry Commons' public-domain "
                       "assertion, and we checked each file really is the work "
                       "it names"):
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
