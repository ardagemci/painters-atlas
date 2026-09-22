"""The artist page's "Major works" panel, tested by what it EMITS.

`js/majorworks.js` renders the panel; `js/renderable.js` decides, per work,
whether a gallery image may stand in for it (`galleryThumbFor`) and whether the
catalog has withheld the work (`isWithheld`). These tests execute both files under
JXA — the same toolchain as every other JS check in this repository — against a
synthetic artist, and assert on the HTML the renderer returns.

Why the renderer and not just the helper
----------------------------------------
The objection that shaped this file: a helper can decide correctly while the
template beside it still uses the old value, or shows "tap a work to enlarge"
unconditionally. So nothing here stops at `galleryThumbFor` returning null; every
case is checked in the emitted markup — image, lightbox attributes, title link,
hint.

The synthetic artist has no Tier-1 arc on purpose. On the live site the panel is
hidden for arc artists, and the only real withheld-with-gallery-art pair (Matisse,
The Snail) belongs to one — so real data alone could never exercise this branch.

What "withheld" means, stated once
----------------------------------
`status:"copyright"` only (docs/ARTWORK_SCHEMA.md §3: the value that suppresses
rendering). A `"pd"` record with no src is missing data, not a decision; `"none"`
is enforced by the validator but used by no record and never defined as
withholding. Both keep their gallery image — see the matrix below.

Proof against the real atlas, run when this was built (2026-09-17): over all 280
artists, the old inline renderer and this one emit the same works, images and hint
for 279. The one difference is Matisse / The Snail, image → title link, invisible
today because Matisse has an arc. No artist's hint changed.
"""
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Gallery_%s.jpg/500px-Gallery_%s.jpg"
SRC = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Catalog_%s.jpg/500px-Catalog_%s.jpg"


def run_panel(artist, catalog, gallery):
    """Execute js/renderable.js + js/majorworks.js under JXA and return the
    renderer's {items, hint, thumbs}. The escaper passed in brackets its input, so
    the tests can also see that every text field went through it."""
    script = r'''
ObjC.import("Foundation");
function read(p){ return ObjC.unwrap($.NSString.stringWithContentsOfFileEncodingError(p, $.NSUTF8StringEncoding, null)); }
var window = {};
[%s, %s].forEach(function(p){ eval(read(p)); });
/* The loader evaluates inside a callback, where declarations stay local; bind the
   published names as globals so the renderer can reach its helper. */
var isRenderable = window.isRenderable, isWithheld = window.isWithheld,
    galleryThumbFor = window.galleryThumbFor, majorWorksPanel = window.majorWorksPanel;
var esc = function(s){ return "[" + s + "]"; };
JSON.stringify(majorWorksPanel(%s, %s, %s, esc));
''' % (json.dumps(str(ROOT / "js" / "renderable.js")), json.dumps(str(ROOT / "js" / "majorworks.js")),
       json.dumps(artist), json.dumps(catalog), "undefined" if gallery is None else json.dumps(gallery))
    with tempfile.NamedTemporaryFile("w", suffix=".jxa.js", delete=False) as f:
        f.write(script)
        path = f.name
    try:
        out = subprocess.run(["osascript", "-l", "JavaScript", path], capture_output=True, text=True, timeout=120)
    finally:
        Path(path).unlink(missing_ok=True)
    if out.returncode != 0:
        raise AssertionError("JXA failed: " + (out.stderr or out.stdout))
    return json.loads(out.stdout.strip())


def works_in(html):
    """Split emitted items into one chunk per work, in order."""
    return [c for c in re.split(r'(?=<div class="work)', html) if c.strip()]


class TestPanelMatrix(unittest.TestCase):
    """One synthetic non-arc artist whose works cover every case at once — which
    is also the mixed panel: the hint must appear, and image/lightbox must appear
    only on the eligible works."""

    # title, catalog record image (None = no catalog match), gallery? , shows thumb?, linked?
    CASES = [
        ("Allowed",              {"src": SRC % ("a", "a"), "status": "pd"},        True,  True,  True),
        ("Licensed",             {"src": SRC % ("l", "l"), "status": "licensed"},  True,  True,  True),
        ("Withheld with src",    {"src": SRC % ("w", "w"), "status": "copyright"}, True,  False, True),
        ("Withheld without src", {"status": "copyright"},                           True,  False, True),
        ("Missing src",          {"status": "pd"},                                  True,  True,  True),
        ("Status none",          {"src": SRC % ("n", "n"), "status": "none"},      True,  True,  True),
        ("Unmatched",            None,                                              True,  True,  False),
        ("No gallery entry",     {"src": SRC % ("g", "g"), "status": "pd"},        False, False, True),
    ]

    @classmethod
    def setUpClass(cls):
        artist = {"id": "fixture-painter", "name": "Fixture Painter",
                  "works": [{"t": t, "y": "19%02d" % i} for i, (t, *_rest) in enumerate(cls.CASES)]}
        catalog, gallery = [], {}
        for i, (t, image, has_gallery, _, _) in enumerate(cls.CASES):
            if image is not None:
                catalog.append({"id": "fx-%d" % i, "title": t, "artistId": "fixture-painter", "image": image})
            if has_gallery:
                gallery[t] = {"img": IMG % (i, i), "page": "https://commons.wikimedia.org/wiki/File:Gallery_%d.jpg" % i}
        cls.out = run_panel(artist, catalog, gallery)
        cls.chunks = works_in(cls.out["items"])

    def test_one_item_per_work(self):
        """A vacuity check: every case below indexes into this list."""
        self.assertEqual(len(self.chunks), len(self.CASES))

    def test_each_case(self):
        for i, (title, _, _, thumb, linked) in enumerate(self.CASES):
            html = self.chunks[i]
            with self.subTest(case=title):
                self.assertIn("[%s]" % title, html, "title missing or not escaped")
                self.assertEqual('<img class="w-thumb"' in html, thumb, "thumbnail")
                self.assertEqual("data-lb-img=" in html, thumb, "lightbox image attribute")
                self.assertEqual("data-lb-link=" in html, thumb, "lightbox link attribute")
                self.assertEqual('href="#/artwork/fx-%d"' % i in html, linked, "catalog link")

    def test_withheld_image_url_never_appears(self):
        """Not merely no <img>: the withheld work's gallery URL is absent from the
        whole panel, so no attribute anywhere can carry it."""
        for i, (title, image, *_rest) in enumerate(self.CASES):
            if image and image.get("status") == "copyright":
                with self.subTest(case=title):
                    self.assertNotIn(IMG % (i, i), self.out["items"])

    def test_mixed_panel_shows_the_hint(self):
        expected = sum(1 for c in self.CASES if c[3])
        self.assertEqual(self.out["thumbs"], expected)
        self.assertIn("tap a work to enlarge", self.out["hint"])


class TestHintOnlyWhenSomethingCanBeTapped(unittest.TestCase):
    def test_withheld_work_alone(self):
        """Codex's case: an artist whose only listed work is withheld, with gallery
        art present. No image, no lightbox, no promise to enlarge — but the title
        and its catalog link survive."""
        artist = {"id": "solo", "name": "Solo", "works": [{"t": "Only Work", "y": "1950"}]}
        catalog = [{"id": "only-work", "title": "Only Work", "artistId": "solo",
                    "image": {"src": SRC % ("o", "o"), "status": "copyright"}}]
        gallery = {"Only Work": {"img": IMG % ("o", "o"), "page": "p"}}
        out = run_panel(artist, catalog, gallery)
        self.assertEqual(out["thumbs"], 0)
        self.assertEqual(out["hint"], "")
        self.assertNotIn("<img", out["items"])
        self.assertNotIn("data-lb-", out["items"])
        self.assertIn('href="#/artwork/only-work"', out["items"])

    def test_gallery_registry_with_no_matching_work(self):
        """The inline version showed the hint whenever the artist had ANY gallery
        registry, even when no listed work matched an entry in it."""
        artist = {"id": "nomatch", "name": "No Match", "works": [{"t": "Listed", "y": "1900"}]}
        gallery = {"Something Else": {"img": IMG % ("x", "x"), "page": "p"}}
        out = run_panel(artist, [], gallery)
        self.assertEqual(out["hint"], "")

    def test_no_gallery_at_all(self):
        artist = {"id": "bare", "name": "Bare", "works": [{"t": "Listed", "y": "1900"}]}
        out = run_panel(artist, [], None)
        self.assertEqual((out["thumbs"], out["hint"]), (0, ""))

    def test_empty_gallery_img_is_not_a_thumbnail(self):
        artist = {"id": "e", "name": "E", "works": [{"t": "W", "y": "1900"}]}
        out = run_panel(artist, [], {"W": {"img": "", "page": "p"}})
        self.assertEqual(out["thumbs"], 0)
        self.assertNotIn("<img", out["items"])


class TestWiring(unittest.TestCase):
    """Supplementary structural guard: the page actually uses the renderer."""

    def test_app_delegates_the_panel(self):
        app = (ROOT / "js" / "app.js").read_text(encoding="utf-8")
        self.assertIn("majorWorksPanel(a,", app)
        self.assertNotRegex(app, r"window\.ARTWORKS\[a\.id\]\[wk\.t\]",
                            "the panel reads gallery entries directly again, bypassing galleryThumbFor")
        self.assertNotIn("tap a work to enlarge", app,
                         "the hint text is emitted from app.js again instead of the renderer")

    def test_load_order(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        r, m, a = (html.find('src="js/%s' % f) for f in ("renderable.js", "majorworks.js", "app.js"))
        self.assertTrue(-1 < r < m < a, "must load renderable.js, then majorworks.js, then app.js")

    def test_each_function_defined_once(self):
        files = list((ROOT / "js").glob("*.js")) + list((ROOT / "tools").glob("*.js"))
        for name, home in (("isWithheld", "renderable.js"), ("galleryThumbFor", "renderable.js"),
                           ("majorWorksPanel", "majorworks.js")):
            with self.subTest(function=name):
                defs = [p.name for p in files
                        if re.search(r"function\s+%s\s*\(" % name, p.read_text(encoding="utf-8"))]
                self.assertEqual(defs, [home])


if __name__ == "__main__":
    unittest.main()
