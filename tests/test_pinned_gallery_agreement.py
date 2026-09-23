"""The pin register and the shipped gallery must name the same Commons file.

Run: python3 -m unittest discover -s tests -p 'test_pinned_gallery_agreement.py'

tools/audit_artworks.py PINNED is the hand-curated instruction a re-resolution
run obeys instead of searching. Nothing checked that it still described the
image js/artworks.js serves, so a pin could drift from the gallery and the only
symptom would appear on the next run, as a silent image swap nobody chose. That
is how "michelangelo::Sistine Chapel Ceiling" came to pin a 2014 interior
photograph while the gallery served a reproduction of the vault; see the note
beside that entry.

The contract: every PINNED key whose work has a gallery entry names the file
that entry's img URL actually serves. A pin whose work has no gallery entry is
not a mismatch — it pins an image for a work the gallery does not yet carry —
so it is skipped rather than failed. This states nothing about rights; it
compares filenames (OD-5).
"""
import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

# Pages the gallery cites on en.wikipedia rather than Commons. Their img still
# resolves to a Commons file and is checked; only the page comparison is moot.
PAGE_EXEMPT = {"hilma-af-klint::Paintings for the Temple",
               "caravaggio::Judith Beheading Holofernes"}


def canonical_commons_filename(url):
    """Decode the ORIGINAL filename, never the resized thumbnail's filename."""
    if not isinstance(url, str):
        return None
    parts = urlsplit(url)
    if parts.netloc != "upload.wikimedia.org":
        return None
    match = re.match(r"^/wikipedia/commons/(?:thumb/)?[0-9a-f]/[0-9a-f]{2}/([^/]+)(?:/|$)", parts.path)
    return unquote(match.group(1)) if match else None


def commons_key(name):
    """Compare the way Commons does: '_' is ' ', and the first letter is capital.

    Nothing else is folded. Two files differing anywhere past the first letter
    are two different files, and this check exists to notice exactly that.
    """
    if not isinstance(name, str):
        return None
    name = unicodedata.normalize("NFC", name).replace("_", " ").strip()
    return name[:1].upper() + name[1:]


def page_filename(url):
    """The file a Commons 'File:' description page names, or None if not one."""
    if not isinstance(url, str) or "/wiki/File:" not in url:
        return None
    return unquote(url.split("/wiki/File:", 1)[1])


def check_pins(pinned, artworks):
    """Every pin whose work has a gallery entry names the file that entry serves."""
    errors = []
    for key, filename in sorted(pinned.items()):
        artist_id, separator, title = key.partition("::")
        if not separator or not artist_id or not title:
            errors.append(f"pin_key: {key!r} is not artist-id::work-title")
            continue
        if not isinstance(filename, str) or not filename.strip():
            errors.append(f"pin_filename: {key} pins no filename")
            continue
        entry = artworks.get(artist_id, {}).get(title)
        if not isinstance(entry, dict):
            continue                    # no gallery entry: nothing to disagree with
        served = canonical_commons_filename(entry.get("img"))
        if served is None:
            errors.append(f"pin_img: {key} has an unrecognised img URL")
        elif commons_key(served) != commons_key(filename):
            errors.append(f"pin_mismatch: {key} pins {filename!r} "
                          f"but the gallery serves {served!r}")
        cited = page_filename(entry.get("page"))
        if cited is not None and key not in PAGE_EXEMPT:
            if commons_key(cited) != commons_key(filename):
                errors.append(f"pin_page_mismatch: {key} pins {filename!r} "
                              f"but the gallery's page cites {cited!r}")
    return errors


def load_pins():
    """The real constant, imported — not a re-parse that could drift from it."""
    import audit_artworks
    return audit_artworks.PINNED


def load_artworks():
    paths = [ROOT / "js/artworks.js"]
    script = r'''
ObjC.import("Foundation");
function read(p) { return ObjC.unwrap($.NSString.stringWithContentsOfFileEncodingError(p, $.NSUTF8StringEncoding, null)); }
var window = {};
%s.forEach(function(p) { eval(read(p)); });
JSON.stringify(window.ARTWORKS || {});
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


class TestPinnedGalleryAgreement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pinned = load_pins()
        cls.artworks = load_artworks()

    def test_every_pin_names_the_file_the_gallery_serves(self):
        errors = check_pins(self.pinned, self.artworks)
        self.assertFalse(errors, "\n" + "\n".join(errors))

    def test_the_register_is_not_silently_empty(self):
        """A check over zero pins would pass for the wrong reason."""
        self.assertGreaterEqual(len(self.pinned), 80)

    def test_page_exemptions_are_still_earned(self):
        """An exemption that stopped being needed should be deleted, not kept."""
        for key in PAGE_EXEMPT:
            artist_id, _, title = key.partition("::")
            entry = self.artworks.get(artist_id, {}).get(title, {})
            self.assertIsNone(page_filename(entry.get("page")),
                              f"{key} now cites a Commons file page; drop its exemption")


def valid_fixture():
    """A register and gallery that agree, before mutation."""
    def entry(filename):
        return {"img": f"https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/{filename}/500px-{filename}",
                "page": f"https://commons.wikimedia.org/wiki/File:{filename}"}
    pinned = {"fixture::First": "First work.jpg",
              "fixture::Second": "Second.jpg",
              "fixture::Uncarried": "Not in the gallery.jpg"}
    artworks = {"fixture": {"First": entry("First_work.jpg"), "Second": entry("Second.jpg")}}
    return pinned, artworks


class TestPinnedGalleryNegativeControls(unittest.TestCase):
    def setUp(self):
        self.pinned, self.artworks = valid_fixture()

    def assert_caught(self, code, errors):
        self.assertTrue(any(e.startswith(code + ":") for e in errors), (code, errors))

    def test_valid_fixture_passes(self):
        self.assertEqual(check_pins(self.pinned, self.artworks), [])

    def test_the_real_mismatch_this_test_was_written_for(self):
        """The Sistine pin as it stood: a pin naming a file the gallery never served."""
        pinned = {"michelangelo::Sistine Chapel Ceiling": "Sistine Chapel ceiling 02 (brightened).jpg"}
        artworks = {"michelangelo": {"Sistine Chapel Ceiling": {
            "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Sistine_ceiling.jpg/500px-Sistine_ceiling.jpg",
            "page": "https://commons.wikimedia.org/wiki/File:Sistine_ceiling.jpg"}}}
        self.assert_caught("pin_mismatch", check_pins(pinned, artworks))
        pinned["michelangelo::Sistine Chapel Ceiling"] = "Sistine ceiling.jpg"
        self.assertEqual(check_pins(pinned, artworks), [])

    def test_a_different_file_is_caught(self):
        self.pinned["fixture::First"] = "Another work.jpg"
        self.assert_caught("pin_mismatch", check_pins(self.pinned, self.artworks))

    def test_a_near_miss_past_the_first_letter_is_caught(self):
        """Only '_'/' ' and the leading capital are folded; nothing else is."""
        for filename in ("First Work.jpg", "First work.png", "First work 2.jpg", "Firstwork.jpg"):
            with self.subTest(filename=filename):
                pinned = dict(self.pinned, **{"fixture::First": filename})
                self.assert_caught("pin_mismatch", check_pins(pinned, self.artworks))

    def test_underscore_space_and_leading_case_are_not_mismatches(self):
        for filename in ("First_work.jpg", "First work.jpg", "first work.jpg",
                         "first_work.jpg", " first_work.jpg "):
            with self.subTest(filename=filename):
                pinned = dict(self.pinned, **{"fixture::First": filename})
                self.assertEqual(check_pins(pinned, self.artworks), [])

    def test_a_pin_without_a_gallery_entry_is_skipped_not_failed(self):
        self.assertIn("fixture::Uncarried", self.pinned)
        self.assertEqual(check_pins(self.pinned, self.artworks), [])
        del self.artworks["fixture"]["First"]
        self.assertEqual(check_pins(self.pinned, self.artworks), [])

    def test_the_thumbnail_name_is_never_read_as_the_file(self):
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/A%20painting.svg/500px-A_painting.svg.png"
        self.assertEqual(canonical_commons_filename(url), "A painting.svg")
        self.assertEqual(canonical_commons_filename(url.replace("thumb/", "").rsplit("/", 1)[0]),
                         "A painting.svg")
        self.artworks["fixture"]["First"]["img"] = (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Other.jpg/500px-First_work.jpg")
        self.assert_caught("pin_mismatch", check_pins(self.pinned, self.artworks))

    def test_an_unreadable_img_url_is_caught(self):
        for url in ("https://example.org/First_work.jpg", "", None):
            with self.subTest(url=url):
                artworks = copy.deepcopy(self.artworks)
                artworks["fixture"]["First"]["img"] = url
                self.assert_caught("pin_img", check_pins(self.pinned, artworks))

    def test_a_page_citing_a_different_file_is_caught(self):
        self.artworks["fixture"]["First"]["page"] = "https://commons.wikimedia.org/wiki/File:Other.jpg"
        self.assert_caught("pin_page_mismatch", check_pins(self.pinned, self.artworks))

    def test_a_non_commons_page_is_not_compared(self):
        self.artworks["fixture"]["First"]["page"] = "https://en.wikipedia.org/wiki/First_work"
        self.assertEqual(check_pins(self.pinned, self.artworks), [])

    def test_a_malformed_key_or_filename_is_caught(self):
        for key in ("fixture", "::First", "fixture::"):
            with self.subTest(key=key):
                self.assert_caught("pin_key", check_pins({key: "First work.jpg"}, self.artworks))
        for filename in (None, "", "   ", 7):
            with self.subTest(filename=filename):
                self.assert_caught("pin_filename",
                                   check_pins({"fixture::First": filename}, self.artworks))


if __name__ == "__main__":
    unittest.main()
