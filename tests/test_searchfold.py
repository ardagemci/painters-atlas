"""Search must not depend on typing accents.

`js/searchfold.js` defines searchFold(), the one function search uses to compare
text; js/app.js passes both the index keys and the visitor's query through it.
These tests execute that file under JXA — the repository's JS toolchain — and
hold it to three things:

1. It folds what visitors actually type: accents, Turkish İ and ı, ł, ø, æ, ß,
   hyphens and dashes.
2. EVERY name the atlas can be searched by folds to plain ASCII. This is the
   guard that matters over time: a future painter whose name carries a letter the
   fold table lacks would otherwise become unfindable without anyone noticing,
   which is exactly how 51 of 300 painters went unfindable until 2026-09-27.
   A negative control proves the check can fail.
3. js/app.js is wired to it on both sides, and loads it first.
"""
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def page_scripts():
    """The data and helper scripts index.html loads, in its order, minus app.js
    (which needs a DOM)."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    return [s for s in re.findall(r'<script src="js/([^"?]+)', html) if s != "app.js"]


def run_jxa(expression, files=None):
    files = page_scripts() if files is None else files
    script = r'''
ObjC.import("Foundation");
function read(p){ return ObjC.unwrap($.NSString.stringWithContentsOfFileEncodingError(p, $.NSUTF8StringEncoding, null)); }
var window = {};
%s.forEach(function(f){ eval(read(%s + f)); });
var searchFold = window.searchFold;
JSON.stringify(%s);
''' % (json.dumps(files), json.dumps(str(ROOT / "js") + "/"), expression)
    with tempfile.NamedTemporaryFile("w", suffix=".jxa.js", delete=False, encoding="utf-8") as f:
        f.write(script)
        path = Path(f.name)
    try:
        out = subprocess.run(["osascript", "-l", "JavaScript", str(path)],
                             capture_output=True, text=True, timeout=120)
    finally:
        path.unlink(missing_ok=True)
    if out.returncode:
        raise AssertionError("JXA failed: " + (out.stderr or out.stdout))
    return json.loads(out.stdout.strip())


def fold_all(strings):
    return run_jxa("%s.map(searchFold)" % json.dumps(strings, ensure_ascii=False),
                   files=["searchfold.js"])


class TestFoldMatrix(unittest.TestCase):
    CASES = [
        ("Paul Cézanne", "paul cezanne"),
        ("Joan Miró", "joan miro"),
        ("Diego Velázquez", "diego velazquez"),
        ("Albrecht Dürer", "albrecht durer"),
        ("Arnold Böcklin", "arnold bocklin"),
        ("Tawaraya Sōtatsu", "tawaraya sotatsu"),
        ("İbrahim Çallı", "ibrahim calli"),          # capital İ, dotless ı
        ("Matrakçı Nasuh", "matrakci nasuh"),
        ("Burhan Doğançay", "burhan dogancay"),
        ("Şeker Ahmed Paşa", "seker ahmed pasa"),
        ("Vilhelm Hammershøi", "vilhelm hammershoi"),
        ("Stanisław Wyspiański", "stanislaw wyspianski"),
        ("P.S. Krøyer", "p.s. kroyer"),
        ("Joaquín Torres-García", "joaquin torres garcia"),
        ("Nocturne in Black and Gold — The Falling Rocket", "nocturne in black and gold the falling rocket"),
        ("Ærø Œuvre Straße", "aero oeuvre strasse"),
        ("Mona Lisa", "mona lisa"),                  # ASCII: only lower-cased
        ("", ""),
    ]

    def test_cases(self):
        got = fold_all([c[0] for c in self.CASES])
        self.assertEqual(len(got), len(self.CASES))
        for (src, want), have in zip(self.CASES, got):
            with self.subTest(source=src):
                self.assertEqual(have, want)

    def test_idempotent(self):
        once = fold_all([c[0] for c in self.CASES])
        self.assertEqual(fold_all(once), once)


COVERAGE = r'''(function(){
  var bad = [];
  function chk(kind, s){ var f = searchFold(s); if(/[^\x00-\x7f]/.test(f)) bad.push(kind + ": " + s + " -> " + f); }
  (window.ARTISTS || []).forEach(function(a){ chk("artist", a.name); });
  (window.CATALOG || []).forEach(function(w){ chk("artwork", w.title); });
  (window.VENUES || []).forEach(function(v){ chk("museum", v.name); chk("museum city", v.city || ""); });
  (window.MOVEMENTS || []).forEach(function(m){ chk("movement", m.name); });
  (window.TECHNIQUES || []).forEach(function(t){ chk("technique", t.name); });
  (window.ERAS || []).forEach(function(e){ chk("era", e.name); });
  (window.NATIONS || []).forEach(function(n){ chk("nation", n.name); });
  (window.EDITORIAL_LISTS || []).forEach(function(l){ chk("list", l.title); });
  return { artists: (window.ARTISTS || []).length, catalog: (window.CATALOG || []).length, bad: bad };
})()'''


class TestAtlasCoverage(unittest.TestCase):
    def test_every_searchable_name_folds_to_ascii(self):
        r = run_jxa(COVERAGE)
        # vacuity: the registries actually loaded
        self.assertGreaterEqual(r["artists"], 300)
        self.assertGreaterEqual(r["catalog"], 398)
        self.assertEqual(r["bad"], [], "names search cannot match by typing — extend "
                         "SEARCH_FOLD_LETTERS in js/searchfold.js:\n" + "\n".join(r["bad"]))

    def test_negative_control_an_unmapped_letter_is_caught(self):
        """Maltese ħ has no decomposition and is not in the table. Injected as a
        painter, the coverage check must report it — otherwise the guard above
        could pass by never looking."""
        expr = '(window.ARTISTS.push({name:"Ħal Saflieni Painter"}), ' + COVERAGE + ')'
        r = run_jxa(expr)
        self.assertTrue(any("Ħal Saflieni" in b for b in r["bad"]), r["bad"])


class TestWiring(unittest.TestCase):
    APP = (ROOT / "js" / "app.js").read_text(encoding="utf-8")

    def body(self, name):
        m = re.search(r"function %s\(.*?\n}\n" % name, self.APP, re.S)
        self.assertIsNotNone(m, name + " not found in js/app.js")
        return m.group(0)

    def test_index_keys_are_folded(self):
        keys = self.body("srKeys")
        self.assertIn("searchFold(it.name)", keys)
        self.assertIn("searchFold(it.alt)", keys)
        self.assertNotIn("toLowerCase", keys, "srKeys lower-cases without folding again")
        self.assertRegex(self.APP, r"it\.metaKey = .*searchFold\(it\.meta")

    def test_query_is_folded(self):
        run = self.body("runSearch")
        self.assertIn("searchFold(raw)", run)
        self.assertNotIn("toLowerCase", run, "runSearch lower-cases without folding again")

    def test_load_order_and_single_definition(self):
        scripts = page_scripts() + ["app.js"]
        self.assertLess(scripts.index("searchfold.js"), scripts.index("app.js"))
        defs = [p.name for p in list((ROOT / "js").glob("*.js")) + list((ROOT / "tools").glob("*.js"))
                if re.search(r"function\s+searchFold\s*\(", p.read_text(encoding="utf-8"))]
        self.assertEqual(defs, ["searchfold.js"])


if __name__ == "__main__":
    unittest.main()
