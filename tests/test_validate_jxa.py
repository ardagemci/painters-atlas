"""`tools/validate.jxa.js` must be able to fail. (backlog C7)

Until 2026-08-17 the script ended by *returning* its report as a string, so
`osascript` exited 0 whichever way the check went. It found errors, printed
them, and told the shell everything was fine — which meant `CLAUDE.md` Gate 2
named as build-blocking a command that could not block, and every automated
green it ever reported was unconditional.

Non-vacuity, per the standard backlog C6 set: a suite that always fails is as
worthless as the gate it replaces. `test_clean_tree_passes` proves this suite is
not failing unconditionally; the broken-tree cases prove it is not passing
unconditionally. Both directions are required.

macOS only — JXA needs `osascript`. Skips elsewhere rather than failing.

    python3 -m unittest tests.test_validate_jxa -v
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HAVE_OSASCRIPT = sys.platform == "darwin" and shutil.which("osascript") is not None


@unittest.skipUnless(HAVE_OSASCRIPT, "JXA validator requires macOS osascript")
class ValidatorFailureSignalTest(unittest.TestCase):
    """Each case runs the real validator against a scratch copy of the tree."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.tree = Path(self.temporary.name)
        # The validator resolves the project root from its own path, so js/ and
        # tools/ must keep their relative positions.
        shutil.copytree(ROOT / "js", self.tree / "js")
        (self.tree / "tools").mkdir()
        shutil.copy(ROOT / "tools" / "validate.jxa.js", self.tree / "tools")
        self.addCleanup(self.temporary.cleanup)

    def run_validator(self):
        completed = subprocess.run(
            ["osascript", "-l", "JavaScript", str(self.tree / "tools" / "validate.jxa.js")],
            capture_output=True,
            text=True,
            timeout=180,
        )
        return completed.returncode, completed.stdout

    def patch(self, filename, old, new):
        path = self.tree / "js" / filename
        source = path.read_text(encoding="utf-8")
        self.assertIn(old, source, f"fixture is stale: {old!r} no longer in {filename}")
        path.write_text(source.replace(old, new, 1), encoding="utf-8")

    # ── the suite is not failing unconditionally ────────────────────────────

    def test_clean_tree_passes(self):
        code, stdout = self.run_validator()
        self.assertEqual(code, 0, f"unmodified tree must exit 0:\n{stdout}")
        self.assertIn("ALL REFERENCES VALID", stdout)

    # ── the suite is not passing unconditionally ────────────────────────────

    def test_broken_reference_exits_nonzero(self):
        """A dangling id. The old script printed this and exited 0."""
        self.patch("artists-1.js", 'nation:"italy"', 'nation:"atlantis"')
        code, stdout = self.run_validator()
        self.assertEqual(code, 1, f"a dangling reference must exit 1:\n{stdout}")
        self.assertIn("bad nation atlantis", stdout)
        self.assertNotIn("ALL REFERENCES VALID", stdout)

    def test_unparseable_data_file_is_inconclusive_not_valid(self):
        """The compounding case, and the reason load failures are tracked apart.

        A file that will not parse contributes no records, so every reference
        check below it then runs on a smaller corpus and can come back clean --
        a parse failure used to make the script *more* likely to report success.
        """
        self.patch("catalog-3.js", "window.CATALOG", "window.CATALOG = (((;")
        code, stdout = self.run_validator()
        self.assertEqual(code, 1, f"an unparseable data file must exit 1:\n{stdout}")
        self.assertIn("LOAD FAILURES", stdout)
        self.assertIn("catalog-3.js ERROR", stdout)
        self.assertNotIn(
            "ALL REFERENCES VALID",
            stdout,
            "a run on incomplete data is inconclusive, never valid",
        )

    def test_a_wikipedia_article_as_image_page_is_refused(self):
        """An en.wikipedia.org article carries no licence statement, so a record
        citing one asserts a public-domain basis it cannot show (PIGMENT.md §14,
        OD-5). 293 records did exactly that until W-004 migrated them, and the
        count had grown from 257 in two days because new records kept arriving
        the same way. This check is why that was the last migration."""
        self.patch("catalog-1.js",
                   'page:"https://commons.wikimedia.org/wiki/File:Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg"',
                   'page:"https://en.wikipedia.org/wiki/The_Starry_Night"')
        code, stdout = self.run_validator()
        self.assertEqual(code, 1, "a Wikipedia article must fail the build:\n" + stdout)
        self.assertIn("image.page is not a Commons file page", stdout)
        self.assertIn("the-starry-night", stdout)

    def test_report_survives_failure(self):
        """Failing must not cost the diagnostics. Exiting early before the
        report is written would swap one broken gate for another."""
        self.patch("artists-1.js", 'nation:"italy"', 'nation:"atlantis"')
        _, stdout = self.run_validator()
        self.assertIn("app.js: syntax OK", stdout)
        self.assertIn("artists:", stdout, "the count summary must still be emitted")


class ValidatorStructureTest(unittest.TestCase):
    """Guards the shape of the fix, so a later tidy-up cannot silently undo it."""

    def test_script_exits_explicitly(self):
        source = (ROOT / "tools" / "validate.jxa.js").read_text(encoding="utf-8")
        self.assertIn("$.exit(", source, "the validator must exit explicitly")
        self.assertIn("emit(", source, "the report must be written to stdout, not returned")
        self.assertFalse(
            source.rstrip().endswith('out.join("\\n");'),
            "ending on a bare expression is the C7 defect: osascript would exit 0",
        )

    def test_load_failures_are_counted(self):
        """Every eval-load catch must route to loadFail, not to the report."""
        source = (ROOT / "tools" / "validate.jxa.js").read_text(encoding="utf-8")
        stragglers = [
            line.strip()
            for line in source.splitlines()
            if "out.push(" in line and "ERROR: " in line
        ]
        self.assertEqual(
            stragglers,
            [],
            "these load failures are reported but not counted:\n  " + "\n  ".join(stragglers),
        )


class SingleValidatorTest(unittest.TestCase):
    """There is exactly one grader. (backlog C7, Phase 0b)

    `tools/validate.js` was deleted 2026-08-17. It had been stale since
    2026-07-02, loading neither `artists-16/17/18` (35 artists) nor any of the
    fourteen other registries -- no catalog, no venues, no influences. The
    Coordinator preferred it whenever Node was on PATH, so installing Node would
    have silently downgraded Gate 2 rather than failing loudly.
    """

    INSTRUCTIONAL = [
        Path("CLAUDE.md"),
        Path("README.md"),
        Path("pigment_coordinator/cli.py"),
        *sorted(Path(".claude/agents").glob("*.md")),
    ]

    def test_node_validator_stays_deleted(self):
        self.assertFalse(
            (ROOT / "tools" / "validate.js").exists(),
            "a second validator checking less data is worse than no fallback",
        )

    def test_default_validator_never_prefers_node(self):
        sys.path.insert(0, str(ROOT))
        from pigment_coordinator.cli import default_validator

        with unittest.mock.patch.dict("os.environ", {}, clear=False) as environ:
            environ.pop("PIGMENT_VALIDATOR_COMMAND", None)
            self.assertNotIn("node", default_validator())

    def test_nothing_instructs_a_reader_to_run_it(self):
        """Docs and agent briefs must not name a command that no longer exists."""
        offenders = []
        for relative in self.INSTRUCTIONAL:
            path = ROOT / relative
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8").replace("validate.jxa.js", "")
            if "validate.js" in text:
                offenders.append(str(relative))
        self.assertEqual(
            offenders,
            [],
            "these still point a reader at the deleted validator: " + ", ".join(offenders),
        )


if __name__ == "__main__":
    unittest.main()
