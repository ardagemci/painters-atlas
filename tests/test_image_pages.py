"""tools/check_image_pages.py — the gate W-004 has to satisfy.

W-004 proposes rewriting `image.page` on 257 production records. A writ that
changes production data at that scale needs something that can say whether it
did so correctly, and this is it. These tests exist because the first draft of
that checker produced exactly the right counts while attaching the wrong id to
every one of them.

    python3 -m unittest tests.test_image_pages -v
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check_image_pages as checker  # noqa: E402

REGISTER = ROOT / "protocol/runs/2026-08-22-W-003-9eca5d5.json"


class CensusTest(unittest.TestCase):
    def setUp(self):
        self.pd = [r for r in checker.records() if r["status"] == "pd"]

    def test_it_finds_every_public_domain_record(self):
        """Cross-checked against a register built by a completely different
        method — rights_register.py evaluates the JS, this parses text. A
        parser that silently reads fewer records reports a falsely clean
        census, and agreeing with an independent count is what rules that out."""
        expected = json.loads(REGISTER.read_text())["summary"]["entries"]
        self.assertEqual(len(self.pd), expected)

    def test_ids_are_artworks_not_museums(self):
        """`museum:{ id:"san-luigi-dei-francesi" }` sits between a record's id
        and its image block. An unanchored regex returns the museum's id for
        every record — and the counts come out identical either way, which is
        why the bug survived until a sample was printed."""
        ids = {r["id"] for r in self.pd}
        self.assertIn("the-calling-of-saint-matthew", ids)
        self.assertIn("girl-with-a-pearl-earring", ids)
        for museum in ("san-luigi-dei-francesi", "uffizi", "louvre", "rijksmuseum"):
            self.assertNotIn(museum, ids, "%s is a venue, not an artwork" % museum)

    def test_catalog_files_are_discovered_not_listed(self):
        """The C2 lesson: a catalog-6.js added later must not need this file
        edited, or it is silently skipped by whichever tool someone forgets."""
        names = [p.name for p in checker.catalog_files()]
        self.assertTrue(names)
        self.assertEqual(names, sorted(names, key=lambda n: int(
            "".join(c for c in n if c.isdigit()))))


class GateTest(unittest.TestCase):
    def run_checker(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "tools" / "check_image_pages.py"), *args],
                              capture_output=True, text=True, cwd=ROOT)

    def test_census_alone_never_fails(self):
        """Report-only by default: knowing the number is not a build break."""
        self.assertEqual(self.run_checker().returncode, 0)

    def test_the_gate_fails_while_the_work_is_undone(self):
        """Non-vacuity, and it is the point of the tool: 257 records still cite
        a Wikipedia article, so --require-commons must refuse today. If this
        ever passes without W-004 having run, the check has stopped checking."""
        result = self.run_checker("--require-commons")
        self.assertEqual(result.returncode, 1)
        self.assertIn("still cite a page that is not a Commons file page", result.stderr)

    def test_the_gate_passes_when_every_page_is_a_commons_file_page(self):
        """The other direction, on synthetic data — a gate that only ever
        fails is as useless as one that only ever passes."""
        good = [{"id": "x", "file": "f", "status": "pd",
                 "page": "https://commons.wikimedia.org/wiki/File:A.jpg"}]
        original, checker.records = checker.records, lambda: iter(good)
        try:
            self.assertEqual(checker.main(["--require-commons"]), 0)
        finally:
            checker.records = original

    def test_a_register_mismatch_is_an_error_not_a_shrug(self):
        with tempfile.TemporaryDirectory() as tmp:
            bogus = Path(tmp, "r.json")
            bogus.write_text(json.dumps({"summary": {"entries": 999}}))
            result = self.run_checker("--against", str(bogus))
            self.assertEqual(result.returncode, 2)
            self.assertIn("MISMATCH", result.stderr)


if __name__ == "__main__":
    unittest.main()
