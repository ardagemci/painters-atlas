"""The one renderability predicate, tested by what it DOES.

`js/renderable.js` defines `isRenderable(img)`: a catalog image is shown only
when it has a non-empty src AND a status of "pd" or "licensed". Since
2026-09-15 it is the sole expression of that rule in `js/app.js` and in
`tools/build_seo.jxa.js`.

Why these tests are behavioural rather than a count of expressions
------------------------------------------------------------------
The debate that produced them turned on one sentence: *all evaluators can agree
on the same bug.* A test that checks the app, the validator and the Python tools
against EACH OTHER passes happily if all of them are wrong together. So:

  1. The production predicate is EXECUTED — `js/renderable.js` is evaluated under
     JXA, exactly as `tools/build_seo.jxa.js` evaluates it — against a fixture
     matrix with the expected answer written down. Nothing here retypes the rule.
  2. The Python tools that decide what the census and the inventory count are
     EXECUTED on a fixture catalog, and checked against the same expected set.
  3. On the real catalog, agreement is checked by RECORD ID, not by URL. URLs are
     not identities here: the af Klint file once existed in two URL forms for one
     record (RIGHTS-001 D-008), so a URL comparison can hide exactly the error it
     is meant to find.
  4. The real validator is RUN, and its printed deck-quadrant warnings are checked
     against counts derived from the executed predicate. The validator is in the
     sealed set and still spells the rule out inline; it is covered here by its
     behaviour, not edited. Moving it onto the shared predicate is a verifier edit
     for the owner (CLAUDE.md §0).

One structural guard remains (TestSinglePredicate): it forbids the rule being
spelled out again in the two files that now share it. It is a supplement to the
behavioural tests above, not a substitute for them.

Known and bounded divergence
----------------------------
For a "pd" record whose src is NOT a Commons URL, the JS predicate answers "render"
(a non-empty string) while the Python tools exclude it (they match src against
upload.wikimedia.org). That input cannot reach a passing build: the validator
errors on any pd/licensed image not Commons-hosted (`tools/validate.jxa.js`,
"image not Commons-hosted"). TestKnownDivergence records it so it is a stated
boundary rather than a surprise.

Scope: catalog records only. `window.ARTWORKS` carries no status and is not gated
by this predicate — see protocol/tasks/IFACE-001/evidence/cross-registry-identity.md.
"""
import contextlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import asset_inventory as ai          # noqa: E402
import rights_register as rr          # noqa: E402
import audit_artwork_rights as aar    # noqa: E402

COMMONS = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Fixture_%s.jpg/500px-Fixture_%s.jpg"


def jxa(script):
    """Run a JXA program and return its final expression, parsed as JSON."""
    with tempfile.NamedTemporaryFile("w", suffix=".jxa.js", delete=False) as f:
        f.write(script)
        path = f.name
    try:
        out = subprocess.run(["osascript", "-l", "JavaScript", path],
                             capture_output=True, text=True, timeout=120)
    finally:
        Path(path).unlink(missing_ok=True)
    if out.returncode != 0:
        raise AssertionError("JXA failed: " + (out.stderr or out.stdout))
    return json.loads(out.stdout.strip())


JXA_PRELUDE = r'''
ObjC.import("Foundation");
function read(p){ return ObjC.unwrap($.NSString.stringWithContentsOfFileEncodingError(p, $.NSUTF8StringEncoding, null)); }
var window = {};
eval(read(%s));
var isRenderable = window.isRenderable;
''' % json.dumps(str(ROOT / "js" / "renderable.js"))


class TestPredicateOutcomes(unittest.TestCase):
    """The production predicate, executed, against written-down answers."""

    #: (label, image value as JS source, expected)
    MATRIX = [
        ("pd, Commons src",            '{src:%s, status:"pd"}' % json.dumps(COMMONS % ("a", "a")),        True),
        ("licensed, Commons src",      '{src:%s, status:"licensed"}' % json.dumps(COMMONS % ("b", "b")),  True),
        ("copyright WITH a src",       '{src:%s, status:"copyright"}' % json.dumps(COMMONS % ("c", "c")), False),
        ("none WITH a src",            '{src:%s, status:"none"}' % json.dumps(COMMONS % ("d", "d")),      False),
        ("unknown status WITH a src",  '{src:%s, status:"generative"}' % json.dumps(COMMONS % ("e", "e")),False),
        ("missing status WITH a src",  '{src:%s}' % json.dumps(COMMONS % ("f", "f")),                     False),
        ("pd, empty src",              '{src:"", status:"pd"}',                                           False),
        ("pd, missing src",            '{status:"pd"}',                                                   False),
        ("licensed, missing src",      '{status:"licensed"}',                                             False),
        ("pd, src not a string",       '{src:42, status:"pd"}',                                           False),
        ("image null",                 'null',                                                            False),
        ("image undefined",            'undefined',                                                       False),
    ]

    def test_fixture_matrix(self):
        body = "JSON.stringify([" + ",".join("isRenderable(%s)" % src for _, src, _ in self.MATRIX) + "]);"
        got = jxa(JXA_PRELUDE + body)
        self.assertEqual(len(got), len(self.MATRIX), "JXA must return one result per fixture")
        for (label, _, want), actual in zip(self.MATRIX, got):
            with self.subTest(case=label):
                self.assertIs(actual, want)

    def test_the_cases_that_used_to_leak(self):
        """Before 2026-09-15 three surfaces tested `image && image.src` with no
        status: a withheld record that kept its src would have rendered there.
        These are the inputs that distinguish the old rule from the new one."""
        got = jxa(JXA_PRELUDE + 'JSON.stringify(['
                  'isRenderable({src:%s, status:"copyright"}),'
                  'isRenderable({src:%s, status:"none"})]);'
                  % (json.dumps(COMMONS % ("x", "x")), json.dumps(COMMONS % ("y", "y"))))
        self.assertEqual(got, [False, False])


@contextlib.contextmanager
def fixture_catalog(records_js):
    """A throwaway repo root holding one catalog file and an empty gallery,
    with the three Python tools pointed at it."""
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "js").mkdir()
        (root / "js" / "catalog-1.js").write_text(
            "window.CATALOG = (window.CATALOG || []).concat([\n" + records_js + "\n]);\n", encoding="utf-8")
        (root / "js" / "artworks.js").write_text("window.ARTWORKS = {};\n", encoding="utf-8")
        saved = (ai.ROOT, rr.ROOT, aar.ROOT, aar.CATALOG_FILES)
        ai.ROOT = rr.ROOT = aar.ROOT = str(root)
        aar.CATALOG_FILES = ["catalog-1.js"]
        try:
            yield root
        finally:
            ai.ROOT, rr.ROOT, aar.ROOT, aar.CATALOG_FILES = saved


class TestPythonToolsOnFixtures(unittest.TestCase):
    """The census and inventory tools, executed on fixtures, against the same
    expected answer as the predicate. Every fixture src is unique, so mapping a
    returned URL back to its record is exact."""

    FIXTURES = [
        # id,              image block (or None),                                           renders
        ("fx-pd",          'image:{ src:"%s", page:"p", status:"pd" }' % (COMMONS % ("pd", "pd")),        True),
        ("fx-licensed",    'image:{ src:"%s", page:"p", status:"licensed" }' % (COMMONS % ("li", "li")),  True),
        ("fx-copy-src",    'image:{ src:"%s", page:"p", status:"copyright" }' % (COMMONS % ("cs", "cs")), False),
        ("fx-copy",        'image:{ status:"copyright" }',                                                False),
        ("fx-none-src",    'image:{ src:"%s", page:"p", status:"none" }' % (COMMONS % ("ns", "ns")),      False),
        ("fx-nostatus",    'image:{ src:"%s", page:"p" }' % (COMMONS % ("nt", "nt")),                     False),
        ("fx-empty-src",   'image:{ src:"", page:"p", status:"pd" }',                                    False),
        ("fx-missing-src", 'image:{ page:"p", status:"pd" }',                                            False),
        ("fx-no-image",    None,                                                                         False),
    ]

    def _records_js(self):
        rows = []
        for rid, block, _ in self.FIXTURES:
            fields = '{ id:"%s", tier:1, title:"%s", artistId:"fixture-artist"' % (rid, rid)
            rows.append(fields + (", " + block if block else "") + " },")
        return "\n".join(rows)

    def _expected(self):
        return {rid for rid, _, renders in self.FIXTURES if renders}

    def _url_to_id(self):
        out = {}
        for rid, block, _ in self.FIXTURES:
            m = block and re.search(r'src:"([^"]+)"', block)
            if m:
                out[m.group(1)] = rid
        return out

    def test_rights_register_selects_by_record_id(self):
        with fixture_catalog(self._records_js()):
            got = {r["id"] for r in rr._catalog_records()}
        self.assertEqual(got, self._expected())

    def test_asset_inventory_selects_the_same_records(self):
        with fixture_catalog(self._records_js()):
            urls, _, _ = ai.catalog_images()
        self.assertEqual({self._url_to_id()[u] for u in urls}, self._expected())

    def test_census_audit_selects_the_same_records(self):
        with fixture_catalog(self._records_js()):
            shipped = aar.shipped_image_urls()
        got = {self._url_to_id()[u] for u, where in shipped.items() if "js/catalog-1.js" in where}
        self.assertEqual(got, self._expected())

    def test_the_js_predicate_agrees_on_the_same_fixtures(self):
        """Same fixtures, executed through js/renderable.js, same expected set."""
        parts = []
        for rid, block, _ in self.FIXTURES:
            img = block[len("image:"):] if block else "undefined"
            parts.append('[%s, isRenderable(%s)]' % (json.dumps(rid), img))
        got = jxa(JXA_PRELUDE + "JSON.stringify([" + ",".join(parts) + "]);")
        self.assertEqual(len(got), len(self.FIXTURES), "JXA must return one result per fixture")
        self.assertEqual({rid for rid, ok in got if ok}, self._expected())


def real_catalog_renderable_ids():
    """Record ids the production predicate renders, over the real catalog,
    loaded the way the app loads it (window.CATALOG built by concatenation)."""
    files = sorted((ROOT / "js").glob("catalog-*.js"), key=lambda p: int(re.search(r"(\d+)", p.name).group(1)))
    loads = "".join("eval(read(%s));\n" % json.dumps(str(p)) for p in files)
    return jxa(JXA_PRELUDE + loads + r'''
JSON.stringify((window.CATALOG || []).map(function(w){
  return {id: w.id, render: isRenderable(w.image), tier: w.tier, src: w.image && w.image.src || null,
          F: w.coords ? w.coords.F : null, D: w.coords ? w.coords.D : null};
}));''')


class TestRealCatalogAgreement(unittest.TestCase):
    """On the shipped data, by record id."""

    @classmethod
    def setUpClass(cls):
        cls.rows = real_catalog_renderable_ids()

    def test_the_catalog_actually_loaded(self):
        """A vacuity check: an empty load would make every agreement below pass."""
        self.assertGreater(len(self.rows), 300)
        self.assertGreater(sum(1 for r in self.rows if r["render"]), 300)

    def test_rights_register_agrees_by_record_id(self):
        js = {r["id"] for r in self.rows if r["render"]}
        py = {r["id"] for r in rr._catalog_records()}
        self.assertEqual(js - py, set(), "the app renders records the rights register does not audit")
        self.assertEqual(py - js, set(), "the rights register audits records the app does not render")

    def test_asset_inventory_agrees_on_the_rendered_files(self):
        js_srcs = {r["src"] for r in self.rows if r["render"]}
        urls, _, _ = ai.catalog_images()
        self.assertEqual(set(urls), js_srcs)

    def test_every_rendered_src_is_commons_hosted(self):
        """The condition under which TestKnownDivergence can never fire."""
        bad = [r["id"] for r in self.rows if r["render"] and "/wikipedia/commons/" not in (r["src"] or "")]
        self.assertEqual(bad, [])


class TestValidatorAgreement(unittest.TestCase):
    """The sealed validator, RUN, against counts from the executed predicate.

    The validator's E4 block reports the onboarding deck's F×D quadrant depth. Its
    eligibility rule is spelled out inline (sealed set, not edited here). The deck
    pool below is built with the executed js/renderable.js; the quadrant thresholds
    are the validator's own (|F|, |D| >= 25 on the named signs).

    LIMIT, MEASURED — do not over-read a pass. The validator prints a quadrant only
    when it holds fewer than two works, so this test can only see a disagreement
    that moves a quadrant across that line. Negative control, 2026-09-15: making
    the predicate stop rendering "licensed" removed black-fuji from F-D+ (47 -> 46
    works) and this test stayed GREEN, while four other tests in this file failed.
    Full coverage needs the validator to consume js/renderable.js or report counts;
    both are edits to a sealed verifier and belong to the owner (CLAUDE.md §0)."""

    QUADRANTS = [("F+D+", 1, 1), ("F+D-", 1, -1), ("F-D+", -1, 1), ("F-D-", -1, -1)]

    def test_quadrant_warnings_match_the_predicate(self):
        out = subprocess.run(["osascript", "-l", "JavaScript", str(ROOT / "tools" / "validate.jxa.js")],
                             capture_output=True, text=True, timeout=300, cwd=str(ROOT))
        self.assertEqual(out.returncode, 0, "validator must pass before its output is interpreted")
        text = out.stdout + out.stderr
        deck = [r for r in real_catalog_renderable_ids()
                if r["render"] and r["tier"] == 1 and r["F"] is not None and r["D"] is not None]
        for name, sf, sd in self.QUADRANTS:
            n = sum(1 for r in deck if sf * r["F"] >= 25 and sd * r["D"] >= 25)
            with self.subTest(quadrant=name, count=n):
                mentioned = ("deck quadrant " + name) in text
                if n >= 2:
                    self.assertFalse(mentioned, "validator warns on %s but the predicate finds %d works" % (name, n))
                elif n == 1:
                    self.assertIn("deck quadrant %s rests on a single work (1)" % name, text)
                else:
                    self.assertIn("deck quadrant %s has NO qualifying work" % name, text)


class TestKnownDivergence(unittest.TestCase):
    def test_non_commons_src_is_the_one_stated_boundary(self):
        """JS says render, the Python tools say no — for input the validator refuses.
        If this ever stops being true, the boundary moved and the module docstring
        is wrong."""
        js = jxa(JXA_PRELUDE + 'JSON.stringify(isRenderable({src:"https://example.org/x.jpg", status:"pd"}));')
        self.assertIs(js, True)
        with fixture_catalog('{ id:"fx-offsite", tier:1, title:"x", artistId:"a", '
                             'image:{ src:"https://example.org/x.jpg", page:"p", status:"pd" } },'):
            self.assertEqual(rr._catalog_records(), [])
        validator = (ROOT / "tools" / "validate.jxa.js").read_text(encoding="utf-8")
        self.assertIn("image not Commons-hosted", validator)


class TestSinglePredicate(unittest.TestCase):
    """Supplementary structural guard: the rule is not spelled out again in the
    files that now share it. Behaviour is tested above; this stops drift."""

    SHARED = [ROOT / "js" / "app.js", ROOT / "tools" / "build_seo.jxa.js"]

    #: The shapes the rule was written in before 2026-09-15. The copyright LABEL
    #: (`w.image.status === "copyright"`, which captions a walled record) is a
    #: different predicate and is deliberately not matched.
    FORBIDDEN = [
        r"\.image\s*&&\s*\w+\.image\.src",
        r"\.image\.status\s*===\s*\"(?:pd|licensed)\"",
        r"status\s*===\s*\"pd\"\s*\|\|",
        r"\bimg\.status\s*===\s*\"(?:pd|licensed)\"",
    ]

    def test_no_raw_renderability_expression(self):
        hits = []
        for path in self.SHARED:
            for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if any(re.search(p, line) for p in self.FORBIDDEN):
                    hits.append("%s:%d  %s" % (path.name, i, line.strip()[:90]))
        print("raw renderability expressions outside js/renderable.js: %d (ceiling 0)" % len(hits))
        self.assertEqual(hits, [])

    def test_the_guard_can_fail(self):
        """Each forbidden pattern matches a line of the kind it exists to refuse."""
        samples = ['const img = w.image && w.image.src && isRenderable(w.image);',
                   'if(w.image.status === "pd") return;',
                   '(w.image.status === "pd" || w.image.status === "licensed")',
                   'return img.status === "licensed";']
        self.assertEqual(len(samples), len(self.FORBIDDEN),
                         "every forbidden pattern needs a sample, or zip() skips it untested")
        for pattern, sample in zip(self.FORBIDDEN, samples):
            with self.subTest(pattern=pattern):
                self.assertRegex(sample, pattern)

    def test_defined_exactly_once(self):
        defs = [p for p in list((ROOT / "js").glob("*.js")) + list((ROOT / "tools").glob("*.js"))
                if re.search(r"function\s+isRenderable\s*\(", p.read_text(encoding="utf-8"))]
        self.assertEqual([p.name for p in defs], ["renderable.js"])

    def test_loaded_before_the_app(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        r = html.find('src="js/renderable.js')
        a = html.find('src="js/app.js')
        self.assertGreater(r, -1, "index.html does not load js/renderable.js")
        self.assertLess(r, a, "js/renderable.js must load before js/app.js, which calls it")


if __name__ == "__main__":
    unittest.main()
