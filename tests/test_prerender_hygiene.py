"""Backlog D1 — the prerendered stubs must not drift from the app or the data.

Two defects, found together. Both are the same species: `p/` is generated, so
nobody reads it, so what is wrong there stays wrong.

1. A BARE DECORATIVE ARROW. The SPA was fixed for AT-5 — the owner heard
   "or surprise me →" announced as "or surprise me right arrow" — and js/app.js
   gained an `ARR` constant that wraps the glyph in `aria-hidden`. The stub
   template kept a bare arrow, so the defect the fix was for survived in every
   prerendered file: 746 of them by the time this was measured.

2. ORPHANED STUBS. `build_seo.jxa.js` only ever wrote; it never removed. A
   record that is deleted or renamed left its page behind in `p/`, still served
   at its URL, still committed, while the sitemap quietly stopped listing it.
"""
import glob
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAMILIES = ("artist", "artwork", "museum", "list")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def js(pattern):
    return "".join(read(p) for p in sorted(glob.glob(os.path.join(ROOT, "js", pattern))))


class PrerenderHygieneTest(unittest.TestCase):

    def test_no_bare_decorative_arrow_in_any_stub(self):
        """A literal → outside an aria-hidden wrapper is read aloud."""
        offenders = []
        for fam in FAMILIES:
            for path in glob.glob(os.path.join(ROOT, "p", fam, "*.html")):
                html = read(path)
                # strip the wrapped ones, then look for what is left
                stripped = re.sub(r'<span aria-hidden="true">[^<]*</span>', "", html)
                if "→" in stripped or "&#8594;" in stripped:
                    offenders.append(os.path.relpath(path, ROOT))
        self.assertEqual(offenders[:5], [],
                         f"{len(offenders)} stub(s) carry a bare arrow, e.g. {offenders[:5]}")

    def test_the_template_hides_its_arrow(self):
        """Guards the shape, so a later tidy-up cannot unwrap it silently."""
        src = read(os.path.join(ROOT, "tools", "build_seo.jxa.js"))
        m = re.search(r'Open in the atlas[^<]*(<span aria-hidden="true">)', src)
        self.assertTrue(m, "the stub CTA's arrow is no longer wrapped in aria-hidden")

    def test_every_stub_has_a_record_behind_it(self):
        """No orphans: a page in p/ must correspond to something in the data."""
        ids = {
            "artwork": set(re.findall(r'\{ id:"([a-z0-9-]+)", tier:\d', js("catalog-*.js"))),
            "artist": set(re.findall(r'id:"([a-z0-9-]+)", name:"', js("artists-*.js"))),
            "museum": set(re.findall(r'id:"([a-z0-9-]+)"',
                                     read(os.path.join(ROOT, "js", "venues.js")))),
            "list": set(re.findall(r'\{ id:"([a-z0-9-]+)",',
                                   read(os.path.join(ROOT, "js", "lists-1.js")))),
        }
        orphans = []
        for fam in FAMILIES:
            for path in glob.glob(os.path.join(ROOT, "p", fam, "*.html")):
                slug = os.path.basename(path)[:-5]
                if slug not in ids[fam]:
                    orphans.append(f"{fam}/{slug}")
        self.assertEqual(orphans, [], f"stub pages with no record: {orphans}")

    def test_the_builder_prunes(self):
        """Guards the mechanism, not just today's clean state."""
        src = read(os.path.join(ROOT, "tools", "build_seo.jxa.js"))
        self.assertIn("removeItemAtPathError", src,
                      "build_seo.jxa.js no longer removes orphaned stubs")
        self.assertIn("emitted[", src,
                      "the prune has no record of what this run wrote, so it cannot be safe")


if __name__ == "__main__":
    unittest.main()
