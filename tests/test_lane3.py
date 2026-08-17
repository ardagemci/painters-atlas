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

    Two live defects shaped this class. The first draft was a bash wrapper
    around a `python3 - <<'PY'` heredoc, which fed the *script* to stdin instead
    of the event; every parse threw, an `except: exit(0)` swallowed it, and the
    hook allowed all thirteen adversarial cases while looking installed. The
    second asked whether "/.claude/" appeared anywhere in the path string, which
    sealed the user's global ~/.claude/ config and any unrelated checkout with a
    protocol/ directory -- it refused the harness's own plan file and aborted a
    real run. Substring matching on paths is not scoping.
    """

    HOOK = ROOT / ".claude" / "hooks" / "sealed-set.py"

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        base = Path(self.temporary.name)
        self.worktree = base / "tree"       # what the run owns
        self.origin = base / "checkout"     # the live repository
        self.elsewhere = base / "elsewhere"  # neither
        for d in (self.worktree, self.origin, self.elsewhere):
            d.mkdir(parents=True)
        self.addCleanup(self.temporary.cleanup)

    def decide(self, event, lane3=True, scoped=True):
        env = {**os.environ, "PIGMENT_LANE3": "1" if lane3 else "0"}
        if scoped:
            env["PIGMENT_LANE3_ROOT"] = str(self.worktree)
            env["PIGMENT_LANE3_REPO"] = str(self.origin)
        else:
            env.pop("PIGMENT_LANE3_ROOT", None)
            env.pop("PIGMENT_LANE3_REPO", None)
        result = subprocess.run(
            [sys.executable, str(self.HOOK)],
            input=json.dumps(event) if isinstance(event, dict) else event,
            capture_output=True, text=True, timeout=30, env=env,
        )
        return "deny" if '"permissionDecision": "deny"' in result.stdout else "allow"

    def write(self, path):
        return {"tool_name": "Edit", "tool_input": {"file_path": str(path)}}

    def bash(self, command):
        return {"tool_name": "Bash", "tool_input": {"command": command}}

    # ── Lane II is never touched ────────────────────────────────────────────
    def test_lane_two_is_never_blocked(self):
        """§0 reserves verifier edits for Lane II, with the user present."""
        for name in ("CLAUDE.md", "tools/validate.jxa.js", "tools/lane3-run.sh"):
            self.assertEqual(self.decide(self.write(self.worktree / name),
                                         lane3=False), "allow", name)
        self.assertEqual(self.decide("not json at all", lane3=False), "allow")

    # ── Inside the worktree: the sealed set applies ─────────────────────────
    def test_sealed_paths_in_the_worktree_are_refused(self):
        for name in [
            "CLAUDE.md", "PIGMENT.md",
            "tools/validate.jxa.js", "tools/audit_artworks.py",
            "tools/lane3-run.sh", "tools/lane3_writ.py",
            ".claude/agents/claude-curator.md",
            ".claude/settings.json",
            ".claude/hooks/sealed-set.py",
            "protocol/writs/W-001.md",
        ]:
            self.assertEqual(self.decide(self.write(self.worktree / name)),
                             "deny", name)

    def test_permitted_work_in_the_worktree_passes(self):
        for name in ("protocol/runs/2026-08-17-W-001.md", "js/artists-1.js",
                     "css/styles.css", "docs/BACKLOG.md"):
            self.assertEqual(self.decide(self.write(self.worktree / name)),
                             "allow", name)

    # ── Outside the worktree ────────────────────────────────────────────────
    def test_the_live_checkout_is_the_wrong_workspace(self):
        """Gate 4: a run works in its worktree and nowhere else."""
        for name in ("js/artists-1.js", "CLAUDE.md"):
            self.assertEqual(self.decide(self.write(self.origin / name)),
                             "deny", name)

    def test_paths_outside_both_trees_are_out_of_scope(self):
        """The bug that aborted a live run: the harness's own plan file lives in
        the user's global ~/.claude/, which is nothing to do with this repo."""
        for name in (".claude/plans/foo.md", "protocol/notes.md", "scratch.txt"):
            self.assertEqual(self.decide(self.write(self.elsewhere / name)),
                             "allow", name)

    # ── Failing closed ──────────────────────────────────────────────────────
    def test_unscoped_run_denies_everything(self):
        """Armed but not told which tree it owns: it cannot tell inside from
        outside, so it refuses rather than guessing."""
        self.assertEqual(
            self.decide(self.write(self.worktree / "js/artists-1.js"), scoped=False),
            "deny",
        )

    def test_unparseable_input_fails_closed(self):
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

    def test_verifiers_can_still_be_executed(self):
        """Running a sealed file is the point; only writing it is refused."""
        for command in [
            "osascript -l JavaScript tools/validate.jxa.js",
            "python3 tools/validate_agent_system.py",
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


class RunnerCompletenessTest(unittest.TestCase):
    """Three defects a live run exposed, each now with a test that would catch it."""

    def setUp(self):
        self.script = (ROOT / "tools" / "lane3-run.sh").read_text(encoding="utf-8")

    def test_the_runner_commits_its_work(self):
        """The worktree is deleted on exit, so uncommitted work never happened.
        Without this the runner pushed a branch with zero commits and reported
        success -- the validator-that-could-not-fail, at the other end."""
        # Matched loosely on purpose: the invocation is
        # `git -c user.name=... \` newline `commit -q -m ...`, so the literal
        # "git commit" never appears in the source.
        self.assertIn("commit -q -m", self.script)
        self.assertIn("git add -A", self.script)
        commit_at = self.script.index("commit -q -m")
        for check in ("SEALED_TOUCHED", "VERIFY_FAILED"):
            self.assertLess(
                self.script.index(check), commit_at,
                "%s must be decided before anything is committed" % check,
            )

    def test_the_runner_scopes_the_hook(self):
        """Armed without roots, the hook denies everything and the run is useless."""
        for name in ("PIGMENT_LANE3=1", "PIGMENT_LANE3_ROOT", "PIGMENT_LANE3_REPO"):
            self.assertIn("export %s" % name, self.script)

    def test_the_prompt_states_which_mode_it_is(self):
        """A run saw the hook armed against a writ reading 'proposed', could not
        reconcile the two, and aborted. It had no way to know it was a rehearsal."""
        self.assertIn("MODE_NOTE", self.script)
        self.assertIn("DRY RUN", self.script)
        self.assertIn("REAL RUN", self.script)
        self.assertIn("${MODE_NOTE}", self.script)

    def test_tool_use_is_an_allowlist(self):
        """One run spawned two subagents and scheduled two wakeups under a
        read-two-verifiers-and-report writ."""
        self.assertIn("--allowedTools", self.script)
        self.assertNotIn("Agent", self.script.split("TOOLS=")[1].split("\n")[0])

    def test_the_runner_reports_what_the_run_consumed(self):
        """Three runs died against a ceiling and nothing said which one."""
        self.assertIn("num_turns", self.script)
        self.assertIn("total_cost_usd", self.script)
        self.assertIn("ceilings:", self.script)

    def test_a_failed_dry_run_does_not_report_success(self):
        """The success message used to print before RUN_EXIT was consulted, so
        an aborted rehearsal announced 'dry run complete' and exited 0. Fifth
        instance of this shape in one afternoon."""
        outcome = self.script[self.script.index("Outcome"):]
        dry_block = outcome[outcome.index('if [ "$DRY_RUN" -eq 1 ]'):]
        complete_at = dry_block.index("dry run complete")
        guard_at = dry_block.index("RUN_EXIT")
        self.assertLess(
            guard_at, complete_at,
            "the abort check must precede the success message",
        )

    def test_shipped_writ_ceilings_clear_observed_usage(self):
        """25-26 turns were observed; a ceiling under that truncates the work."""
        fields = lane3_writ.parse((ROOT / "protocol/writs/W-001.md").read_text(encoding="utf-8"))
        self.assertGreaterEqual(int(fields["max_turns"]), 30)

    def test_shipped_writ_grants_the_fewest_tools_it_needs(self):
        fields = lane3_writ.parse((ROOT / "protocol/writs/W-001.md").read_text(encoding="utf-8"))
        tools = fields.get("tools", [])
        self.assertTrue(tools, "W-001 should name its tools explicitly")
        for forbidden in ("Agent", "ScheduleWakeup", "WebFetch", "WebSearch", "Edit"):
            self.assertNotIn(forbidden, tools,
                             "an observation-only writ has no use for %s" % forbidden)


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
