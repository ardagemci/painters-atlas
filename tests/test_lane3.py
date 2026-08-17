"""Lane III authorization: the writ parser and the runner's guards.

Every field a writ declares is a permission boundary, so these tests care less
about happy paths than about refusals. A run that cannot establish its own
authority must stop, not proceed with less of it -- and a `may_write` that
parses one character wide is indistinguishable from a writ that was granted
wider than the owner intended.

    python3 -m unittest tests.test_lane3 -v
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import lane3_writ  # noqa: E402


def writ(**overrides):
    fields = {
        "writ_id": "W-TEST",
        "status": "proposed",
        "class": "A test writ.",
        "verifier": ["true"],
        "may_write": ["protocol/runs/**"],
        "max_diff": "50",
        "max_turns": "5",
        "max_budget_usd": "1",
        "abort_if": ["anything at all"],
    }
    fields.update(overrides)
    lines = ["---"]
    for key, value in fields.items():
        if value is None:
            lines.append("%s:" % key)
        elif isinstance(value, list):
            lines.append("%s:" % key)
            lines.extend("  - %s" % item for item in value)
        else:
            lines.append("%s: %s" % (key, value))
    lines += ["---", "", "# body"]
    return "\n".join(lines)


class ParserTest(unittest.TestCase):
    def test_parses_the_shipped_writ(self):
        fields = lane3_writ.parse((ROOT / "protocol/writs/W-001.md").read_text(encoding="utf-8"))
        self.assertEqual(fields["writ_id"], "W-001")
        self.assertEqual(fields["status"], "proposed")
        self.assertEqual(fields["may_write"], ["protocol/runs/**"])
        self.assertEqual(len(fields["verifier"]), 2)

    def test_strips_trailing_comments_from_values(self):
        """`status: proposed  # only the owner...` must not parse as the comment."""
        fields = lane3_writ.parse(writ(status="granted          # not by an agent"))
        self.assertEqual(fields["status"], "granted")

    def test_folded_block_becomes_one_string(self):
        source = writ().replace("class: A test writ.", "class: >-\n  first line\n  second line")
        self.assertEqual(lane3_writ.parse(source)["class"], "first line second line")

    def test_missing_fence_is_an_error_not_a_guess(self):
        with self.assertRaises(lane3_writ.WritError):
            lane3_writ.parse("writ_id: W-001\nstatus: granted\n")

    def test_unclosed_frontmatter_is_an_error(self):
        with self.assertRaises(lane3_writ.WritError):
            lane3_writ.parse("---\nwrit_id: W-001\n")


class ValidationTest(unittest.TestCase):
    def check(self, **overrides):
        return lane3_writ.validate(lane3_writ.parse(writ(**overrides)))

    def test_a_well_formed_writ_has_no_problems(self):
        self.assertEqual(self.check(), [])

    def test_every_required_field_is_required(self):
        for name in lane3_writ.REQUIRED:
            source = writ()
            kept = [ln for ln in source.splitlines() if not ln.startswith(name + ":")]
            problems = lane3_writ.validate(lane3_writ.parse("\n".join(kept)))
            self.assertTrue(problems, "dropping %s should be a problem" % name)

    def test_status_must_be_a_known_value(self):
        self.assertTrue(any("status must be" in p for p in self.check(status="approved")))

    def test_granted_writ_without_a_signature_is_rejected(self):
        """The commit is the signature; a granted writ must say who and when."""
        problems = self.check(status="granted")
        self.assertTrue(any("granted_by" in p for p in problems))
        self.assertTrue(any("granted_at" in p for p in problems))
        self.assertEqual(
            self.check(status="granted", granted_by="ardagemci", granted_at="2026-08-17"), []
        )

    def test_may_write_cannot_name_the_sealed_set(self):
        for path in ["tools/validate.jxa.js", "tools/audit_artworks.py", "CLAUDE.md",
                     "PIGMENT.md", ".claude/agents/x.md"]:
            problems = self.check(may_write=[path])
            self.assertTrue(
                any("sealed" in p for p in problems), "%s must be refused" % path
            )

    def test_may_write_cannot_reach_into_protocol_except_runs(self):
        self.assertTrue(any("protocol/" in p for p in self.check(may_write=["protocol/writs/**"])))
        self.assertEqual(self.check(may_write=["protocol/runs/**"]), [])

    def test_numeric_ceilings_must_be_numbers(self):
        self.assertTrue(any("max_turns" in p for p in self.check(max_turns="lots")))


class RunnerGuardTest(unittest.TestCase):
    """The runner's refusals, exercised end to end in a throwaway repository."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name) / "repo"
        (self.repo / "tools").mkdir(parents=True)
        (self.repo / "protocol" / "writs").mkdir(parents=True)
        for tool in ("lane3-run.sh", "lane3_writ.py"):
            target = self.repo / "tools" / tool
            target.write_bytes((ROOT / "tools" / tool).read_bytes())
            target.chmod(0o755)
        self.addCleanup(self.temporary.cleanup)

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.repo, check=True,
                       capture_output=True, text=True)

    def commit_writ(self, name, text):
        (self.repo / "protocol" / "writs" / (name + ".md")).write_text(text, encoding="utf-8")
        self.git("add", "-A")
        self.git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", "writ")

    def run_lane3(self, *args):
        self.git("init", "-q", "-b", "main")
        return subprocess.run(
            ["bash", str(self.repo / "tools" / "lane3-run.sh"), *args],
            cwd=self.repo, capture_output=True, text=True, timeout=60,
        )

    def test_refuses_a_writ_that_is_not_on_main(self):
        self.git("init", "-q", "-b", "main")
        self.commit_writ("W-002", writ(writ_id="W-002"))
        result = subprocess.run(
            ["bash", str(self.repo / "tools" / "lane3-run.sh"), "W-404"],
            cwd=self.repo, capture_output=True, text=True, timeout=60,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no writ at", result.stderr)

    def test_refuses_a_proposed_writ_for_a_real_run(self):
        self.git("init", "-q", "-b", "main")
        self.commit_writ("W-002", writ(writ_id="W-002", status="proposed"))
        result = subprocess.run(
            ["bash", str(self.repo / "tools" / "lane3-run.sh"), "W-002"],
            cwd=self.repo, capture_output=True, text=True, timeout=60,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not 'granted'", result.stderr)

    def test_refuses_a_revoked_writ_even_as_a_dry_run(self):
        self.git("init", "-q", "-b", "main")
        self.commit_writ("W-003", writ(writ_id="W-003", status="revoked"))
        result = subprocess.run(
            ["bash", str(self.repo / "tools" / "lane3-run.sh"), "W-003", "--dry-run"],
            cwd=self.repo, capture_output=True, text=True, timeout=60,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("revoked", result.stderr)

    def test_granted_writ_stops_on_the_missing_sealed_set_hook(self):
        """D-8. The hook is Phase 3; until it exists no granted run may proceed,
        however well-formed and however loudly granted the writ is."""
        self.git("init", "-q", "-b", "main")
        self.commit_writ("W-004", writ(writ_id="W-004", status="granted",
                                       granted_by="ardagemci", granted_at="2026-08-17"))
        result = subprocess.run(
            ["bash", str(self.repo / "tools" / "lane3-run.sh"), "W-004"],
            cwd=self.repo, capture_output=True, text=True, timeout=60,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sealed-set hook missing", result.stderr)
        self.assertIn("D-8", result.stderr)

    def test_refuses_a_malformed_writ_rather_than_inferring(self):
        self.git("init", "-q", "-b", "main")
        self.commit_writ("W-005", "no frontmatter here at all\n")
        result = subprocess.run(
            ["bash", str(self.repo / "tools" / "lane3-run.sh"), "W-005", "--dry-run"],
            cwd=self.repo, capture_output=True, text=True, timeout=60,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("malformed", result.stderr)


class SealedHookTest(unittest.TestCase):
    """The PreToolUse hook. (PIGMENT.md §19 D-8)

    The first draft was a bash wrapper around a `python3 - <<'PY'` heredoc,
    which fed the *script* to stdin instead of the event. Every parse threw, an
    `except: exit(0)` swallowed it, and the hook allowed all thirteen
    adversarial cases while looking correctly installed -- backlog C7's defect
    class, reproduced inside the control built to prevent it. These cases exist
    because nothing short of them caught it.
    """

    HOOK = ROOT / ".claude" / "hooks" / "sealed-set.py"

    def decide(self, event, lane3=True):
        result = subprocess.run(
            [sys.executable, str(self.HOOK)],
            input=json.dumps(event) if isinstance(event, dict) else event,
            capture_output=True, text=True, timeout=30,
            env={**os.environ, "PIGMENT_LANE3": "1" if lane3 else "0"},
        )
        return "deny" if '"permissionDecision": "deny"' in result.stdout else "allow"

    def write(self, path):
        return {"tool_name": "Edit", "tool_input": {"file_path": path}}

    def bash(self, command):
        return {"tool_name": "Bash", "tool_input": {"command": command}}

    # ── Lane II must never be touched ───────────────────────────────────────
    def test_lane_two_is_never_blocked(self):
        """§0 reserves verifier edits for Lane II, with the user present. A hook
        that fired in every session would block the work it exists to protect."""
        for path in ["CLAUDE.md", "tools/validate.jxa.js", "tools/lane3-run.sh"]:
            self.assertEqual(self.decide(self.write(path), lane3=False), "allow", path)
        self.assertEqual(self.decide("not json at all", lane3=False), "allow")

    # ── The suite is not passing unconditionally ────────────────────────────
    def test_sealed_writes_are_refused(self):
        for path in [
            "CLAUDE.md", "PIGMENT.md",
            "tools/validate.jxa.js", "tools/audit_artworks.py",
            "tools/lane3-run.sh", "tools/lane3_writ.py",
            ".claude/agents/claude-curator.md",
            ".claude/settings.json",
            ".claude/hooks/sealed-set.py",
            "protocol/writs/W-001.md",
            "/Users/someone/painters-atlas/CLAUDE.md",
        ]:
            self.assertEqual(self.decide(self.write(path)), "deny", path)

    def test_leading_dot_slash_does_not_unseal(self):
        """str.lstrip('./') strips those characters in any order, which turned
        '.claude/agents/x.md' into 'claude/agents/x.md' and un-sealed the whole
        agent directory. It must be a prefix strip."""
        self.assertEqual(self.decide(self.write("./.claude/agents/x.md")), "deny")
        self.assertEqual(self.decide(self.write(".claude/agents/x.md")), "deny")

    def test_unparseable_input_fails_closed(self):
        """A guard that cannot read its own input does not get to wave things
        through -- that is precisely how the first draft failed silently."""
        for junk in ["not json at all", "", "[]", '{"tool_input": "a string"}']:
            self.assertEqual(self.decide(junk), "deny", repr(junk))

    def test_bash_write_shapes_are_refused(self):
        for command in [
            "echo pass > tools/validate.jxa.js",
            "echo x >> CLAUDE.md",
            'sed -i "" s/a/b/ tools/lane3-run.sh',
            "rm tools/validate.jxa.js",
            "git checkout main -- CLAUDE.md",
            "cp /tmp/fake.py tools/audit_artworks.py",
        ]:
            self.assertEqual(self.decide(self.bash(command)), "deny", command)

    # ── The suite is not failing unconditionally ────────────────────────────
    def test_permitted_work_still_passes(self):
        self.assertEqual(self.decide(self.write("protocol/runs/2026-08-17-W-001.md")), "allow")
        self.assertEqual(self.decide(self.write("js/artists-1.js")), "allow")
        self.assertEqual(self.decide({"tool_name": "Read",
                                      "tool_input": {"file_path": "CLAUDE.md"}}), "allow")

    def test_verifiers_can_still_be_executed(self):
        """Running a sealed file is the whole point; only writing it is refused."""
        for command in [
            "osascript -l JavaScript tools/validate.jxa.js",
            "python3 tools/validate_agent_system.py",
            "python3 tools/audit_artwork_rights.py --help",
        ]:
            self.assertEqual(self.decide(self.bash(command)), "allow", command)


class SealedBackstopTest(unittest.TestCase):
    """tools/lane3-run.sh asks git which files actually moved.

    The hook decides Write and Edit exactly, but a Bash command is a program and
    no pattern settles what an arbitrary program writes. This is the complete
    check: it runs before any outcome is declared, and voids the run.
    """

    def setUp(self):
        self.script = (ROOT / "tools" / "lane3-run.sh").read_text(encoding="utf-8")

    def test_the_backstop_exists_and_voids_the_run(self):
        self.assertIn("SEALED_TOUCHED", self.script)
        self.assertIn("git diff --name-only main", self.script)
        self.assertIn("VOID", self.script)

    def test_the_backstop_classifies_paths_correctly(self):
        """Extracts the pattern from the script itself, so drift is caught."""
        match = re.search(r"\|\s*grep -E '(\^\([^']+)'", self.script)
        self.assertIsNotNone(match, "could not find the backstop's grep pattern")
        pattern = match.group(1)
        paths = "\n".join([
            "js/artists-1.js", "css/styles.css", "protocol/runs/report.md",
            "CLAUDE.md", "PIGMENT.md", "tools/validate.jxa.js",
            "tools/lane3-run.sh", "tools/audit_artworks.py",
            ".claude/settings.json", "protocol/writs/W-001.md",
        ])
        flagged = subprocess.run(
            ["bash", "-c", "grep -E %s | grep -v '^protocol/runs/' || true"
             % json.dumps(pattern)],
            input=paths, capture_output=True, text=True,
        ).stdout.split()
        self.assertEqual(sorted(flagged), sorted([
            "CLAUDE.md", "PIGMENT.md", "tools/validate.jxa.js",
            "tools/lane3-run.sh", "tools/audit_artworks.py",
            ".claude/settings.json", "protocol/writs/W-001.md",
        ]))

    def test_the_runner_arms_the_hook(self):
        self.assertIn("export PIGMENT_LANE3=1", self.script)
        self.assertIn(".claude/hooks/sealed-set.py", self.script)


class SettingsRegistrationTest(unittest.TestCase):
    """An unregistered hook enforces nothing."""

    def test_hook_is_registered_on_the_write_tools(self):
        settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        entries = settings["hooks"]["PreToolUse"]
        matcher = entries[0]["matcher"]
        for tool in ("Write", "Edit", "Bash"):
            self.assertIn(tool, matcher, "%s must be matched" % tool)
        self.assertIn("sealed-set", entries[0]["hooks"][0]["command"])


class SealedSetCoverageTest(unittest.TestCase):
    """The harness must seal itself, not only the grader."""

    def test_constitution_seals_the_runner(self):
        section = (ROOT / "CLAUDE.md").read_text(encoding="utf-8").split("## 1.")[0]
        self.assertIn(
            "tools/lane3",
            section,
            "an agent that can rewrite its own runner can bypass every guard in it",
        )


if __name__ == "__main__":
    unittest.main()
