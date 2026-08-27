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
        # Not pinned to a value: `status` is the one field designed to change,
        # and a test asserting it stays "proposed" fails the moment the writ is
        # granted -- which is the mechanism working, not a regression.
        self.assertIn(fields["status"], lane3_writ.STATUSES)
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


class ProbeWritTest(unittest.TestCase):
    """W-002 attempts sealed writes on purpose, to close PIGMENT.md §19 D-8.

    That is only safe in a worktree that is thrown away, so a probe must be
    incapable of a real run — and incapable structurally, not by convention.
    """

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name) / "repo"
        (self.repo / "tools").mkdir(parents=True)
        (self.repo / "protocol" / "writs").mkdir(parents=True)
        for tool in ("lane3-run.sh", "lane3_writ.py"):
            target = self.repo / "tools" / tool
            target.write_bytes((ROOT / "tools" / tool).read_bytes())
            target.chmod(0o755)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.repo, check=True,
                       capture_output=True)
        self.addCleanup(self.temporary.cleanup)

    def commit_writ(self, name, text):
        (self.repo / "protocol" / "writs" / (name + ".md")).write_text(text, encoding="utf-8")
        for args in (["add", "-A"],
                     ["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", "w"]):
            subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True)

    def run_lane3(self, *args):
        return subprocess.run(
            ["bash", str(self.repo / "tools" / "lane3-run.sh"), *args],
            cwd=self.repo, capture_output=True, text=True, timeout=60,
        )

    def test_a_granted_probe_still_refuses_a_real_run(self):
        """The field is the safety property, not the status. A probe with
        `granted` typed into it by accident must still be inert."""
        self.commit_writ("W-900", writ(
            writ_id="W-900", probe="true", status="granted",
            granted_by="ardagemci", granted_at="2026-08-18"))
        result = self.run_lane3("W-900")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("probe: true", result.stderr)
        self.assertIn("no legitimate granted form", result.stderr)

    def test_a_non_probe_writ_is_unaffected(self):
        """Non-vacuity: the guard must not simply refuse everything."""
        self.commit_writ("W-901", writ(writ_id="W-901", status="proposed"))
        result = self.run_lane3("W-901")
        self.assertIn("not 'granted'", result.stderr)
        self.assertNotIn("probe", result.stderr)


class ShippedProbeTest(unittest.TestCase):
    """The state of W-002 as committed."""

    def setUp(self):
        self.fields = lane3_writ.parse(
            (ROOT / "protocol/writs/W-002.md").read_text(encoding="utf-8"))

    def test_it_is_marked_a_probe_and_stays_ungranted(self):
        self.assertEqual(self.fields.get("probe"), "true")
        self.assertEqual(self.fields["status"], "proposed")
        self.assertFalse(self.fields.get("granted_by"),
                         "a probe writ has no legitimate granted form")

    def test_it_may_still_only_write_the_report(self):
        """Attempting sealed writes does not widen what it is allowed to keep."""
        self.assertEqual(self.fields["may_write"], ["protocol/runs/**"])

    def test_it_probes_both_directions(self):
        """A guard that refuses everything is as useless as one that permits
        everything; the probe has to show it discriminates."""
        body = (ROOT / "protocol/writs/W-002.md").read_text(encoding="utf-8")
        self.assertIn("permitted", body)
        self.assertIn("wrong workspace", body)

    def test_the_runner_swaps_the_first_constraint_for_a_probe(self):
        script = (ROOT / "tools" / "lane3-run.sh").read_text(encoding="utf-8")
        self.assertIn("CONSTRAINT_ONE", script)
        self.assertIn("ADVERSARIAL PROBE", script)
        self.assertIn("Never to the sealed set.", script)


class LedgerTest(unittest.TestCase):
    """The ledger is the harness's record, not the run's. (see tools/lane3_ledger.py)

    When the run wrote it, it wrote it inside a worktree that Lane III never
    merges -- so the next run branched from a `main` where it did not exist, and
    every run reported "first run, no baseline". Two real runs produced two
    individually correct and collectively useless reports before this surfaced.
    """

    def setUp(self):
        sys.path.insert(0, str(ROOT / "tools"))
        import lane3_ledger
        self.mod = lane3_ledger
        self.script = (ROOT / "tools" / "lane3-run.sh").read_text(encoding="utf-8")

    VALIDATOR = ("app.js: syntax OK\n"
                 "artists: 266, movements: 80, techniques: 39, eras: 8, nations: 37, "
                 "painter styles: 27, influence edges: 246, venues: 125, "
                 "catalog: 350 (tier1: 76), daily pool: 75, museum notes: 114, "
                 "photo credits: 114 (attribution required: 96), artwork image credits: 28, "
                 "personas: 15, lists: 14 (featured: 4), tier1 artists: 36 (arcs: 36)\n"
                 "ALL REFERENCES VALID\n")

    def test_counts_come_out_of_the_validator_summary(self):
        counts = self.mod.parse_counts(self.VALIDATOR)
        self.assertEqual(counts["artists"], 266)
        self.assertEqual(counts["catalog"], 350)
        self.assertEqual(counts["influence_edges"], 246)
        self.assertEqual(counts["venues"], 125)

    def test_parenthetical_counts_are_not_lost(self):
        """`catalog: 350 (tier1: 76)` carries two numbers, not one."""
        counts = self.mod.parse_counts(self.VALIDATOR)
        self.assertEqual(counts["tier1"], 76)
        self.assertEqual(counts["featured"], 4)
        self.assertEqual(counts["attribution_required"], 96)

    def test_a_missing_count_is_dropped_not_fatal(self):
        """The ledger is evidence, not a gate; the verifiers already decided."""
        self.assertEqual(self.mod.parse_counts("nothing useful here"), {})

    def test_scraped_counts_are_namespaced_away_from_findings(self):
        """`attribution_required` meant 96 in the ledger (photo credits, from
        the validator) and 7 in W-003's report (artwork images under CC-BY).
        Two unrelated quantities under one name is worse than a missing
        number: a missing number is visibly missing."""
        import lane3_ledger
        line = json.loads(subprocess.run(
            [sys.executable, str(ROOT / "tools" / "lane3_ledger.py"),
             "--writ", "W-T", "--base", "abc", "--branch", "b",
             "--outcome", "clean", "--report", "r.md"],
            capture_output=True, text=True).stdout)
        self.assertIn("registry", line)
        self.assertIn("findings", line)
        self.assertNotIn("counts", line, "the ambiguous key must be gone")

    def test_a_writ_can_publish_its_own_findings(self):
        """What counts as a finding is the writ's business, not the harness's."""
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp, "w.json")
            f.write_text(json.dumps({"summary": {"entries": 282,
                                                 "declared_page_wrong": 258}}))
            line = json.loads(subprocess.run(
                [sys.executable, str(ROOT / "tools" / "lane3_ledger.py"),
                 "--writ", "W-003", "--base", "abc", "--branch", "b",
                 "--outcome", "clean", "--report", "r.md", "--findings", str(f)],
                capture_output=True, text=True).stdout)
            self.assertEqual(line["findings"]["declared_page_wrong"], 258)
            self.assertEqual(line["findings"]["entries"], 282)

    def test_a_malformed_findings_file_is_dropped_not_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp, "bad.json"); f.write_text("not json")
            line = json.loads(subprocess.run(
                [sys.executable, str(ROOT / "tools" / "lane3_ledger.py"),
                 "--writ", "W-T", "--base", "a", "--branch", "b",
                 "--outcome", "clean", "--report", "r.md", "--findings", str(f)],
                capture_output=True, text=True).stdout)
            self.assertIsNone(line["findings"])

    def test_the_runner_hands_over_a_published_findings_file(self):
        self.assertIn("--findings", self.script)
        self.assertIn("FINDINGS_REL", self.script)
        self.assertIn("grep -v ledger", self.script,
                      "the ledger itself is not a findings file")

    def test_the_shipped_ledger_uses_the_new_shape(self):
        """Migrated in the same commit; a half-renamed ledger is unreadable."""
        for line in (ROOT / "protocol/runs/ledger.jsonl").read_text().strip().splitlines():
            d = json.loads(line)
            self.assertIn("registry", d, d["run_id"])
            self.assertNotIn("counts", d, d["run_id"])

    def test_the_runner_reads_the_previous_entry_from_main(self):
        self.assertIn('git show "main:${LEDGER_REL}"', self.script)
        self.assertIn("PREV_NOTE", self.script)
        self.assertIn("${PREV_NOTE}", self.script)

    def test_the_runner_appends_the_ledger_to_main(self):
        self.assertIn("lane3_ledger.py", self.script)
        ledger_at = self.script.index("LEDGER_LINE=")
        for earlier in ("VERIFY_FAILED", "SEALED_TOUCHED"):
            self.assertLess(self.script.index(earlier), ledger_at,
                            "%s must be decided before anything is recorded" % earlier)

    def test_the_first_ledger_line_can_actually_be_committed(self):
        """`git commit -- <path>` matches only tracked paths, and the first
        ledger line is what creates the file. The pathspec matched nothing, the
        commit failed, and the line sat untracked on main -- caught only because
        the runner warns rather than assuming its own commit worked."""
        block = self.script[self.script.index("LEDGER_LINE="):]
        self.assertIn('git add -- "$LEDGER_REL"', block)
        self.assertLess(block.index("git add --"), block.index('commit -q -m "ledger'),
                        "the ledger must be staged before it is committed")

    def test_a_failed_ledger_commit_is_reported(self):
        """The run passed and the report is committed; only the record failed.
        Saying so is the difference between a known gap and a silent one."""
        self.assertIn("WARNING: ledger line built but not committed", self.script)

    def test_comparisons_anchor_to_the_base_commit_not_the_branch(self):
        """`main` advances under a running job. A W-003 dry run was voided for
        "modifying protocol/writs/W-003.md" when main simply moved mid-run: the
        worktree held the old file, main held the new one, and the diff blamed
        the run for someone else's commit. $BASE is captured once and cannot
        move; the branch ref can."""
        code = "\n".join(ln for ln in self.script.splitlines()
                         if not ln.lstrip().startswith("#"))
        offenders = [ln.strip() for ln in code.splitlines()
                     if ("git diff" in ln or "rev-list" in ln)
                     and re.search(r'(?<![\w$"])main(?![\w"])', ln)]
        self.assertEqual(offenders, [],
                         "these compare against a ref that moves:\n  " +
                         "\n  ".join(offenders))

    def test_the_base_is_captured_once(self):
        self.assertIn('BASE="$(git rev-parse --short main)"', self.script)
        base_at = self.script.index('BASE="$(git rev-parse')
        self.assertLess(base_at, self.script.index("git worktree add"),
                        "the base must be pinned before the worktree exists")

    def test_verifier_output_is_captured_not_discarded(self):
        """The counts the ledger records are printed by the validator."""
        self.assertIn("VERIFIER_LOG", self.script)
        self.assertNotIn('( cd "$TREE" && eval "$command" ) >/dev/null', self.script)

    def test_the_writ_no_longer_tells_the_run_to_write_a_ledger(self):
        body = (ROOT / "protocol/writs/W-001.md").read_text(encoding="utf-8")
        self.assertIn("do not write the ledger", body.lower())
        self.assertNotIn("Append one line to `protocol/runs/ledger.jsonl`", body)


class ScheduleTest(unittest.TestCase):
    """The launchd job. (Phase 4)

    A scheduled run fails differently from a hand-run one: nobody is watching,
    the environment is not a login shell, and the machine may have been asleep.
    Each of those is a way for the job to look installed and do nothing, which
    is this repository's established failure mode.
    """

    PLIST = ROOT / "tools" / "com.pigment.lane3.plist"
    WRAPPER = ROOT / "tools" / "lane3-cron.sh"

    def plist_value(self, key):
        out = subprocess.run(["plutil", "-extract", key, "json", "-o", "-", str(self.PLIST)],
                             capture_output=True, text=True)
        return json.loads(out.stdout) if out.returncode == 0 else None

    def test_the_plist_is_valid(self):
        checked = subprocess.run(["plutil", "-lint", str(self.PLIST)],
                                 capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_a_sleeping_mac_does_not_queue_a_week_of_runs(self):
        """StartInterval fires every missed tick on wake; StartCalendarInterval
        fires once. On a laptop that difference is seven runs and seven bills."""
        self.assertIsNotNone(self.plist_value("StartCalendarInterval"))
        self.assertIsNone(self.plist_value("StartInterval"))

    def test_a_failing_run_is_not_retried_on_a_timer(self):
        """KeepAlive would turn one broken night into a bill."""
        self.assertFalse(self.plist_value("KeepAlive"))
        self.assertFalse(self.plist_value("RunAtLoad"))

    def test_it_schedules_off_the_hour(self):
        minute = self.plist_value("StartCalendarInterval").get("Minute")
        self.assertNotIn(minute, (0, 30), "every job in the world fires on the hour")

    def test_it_invokes_the_wrapper_with_a_writ(self):
        args = self.plist_value("ProgramArguments")
        self.assertIn("lane3-cron.sh", args[1])
        self.assertTrue(args[2].startswith("W-"), "a writ must be named explicitly")

    def test_the_wrapper_repairs_path_before_looking_for_claude(self):
        """launchd gives a job /usr/bin:/bin and no ~/.zshrc, so the CLI in
        ~/.local/bin is not on PATH. A runner that works by hand and fails only
        at 09:17 is the least debuggable shape of failure."""
        text = self.WRAPPER.read_text(encoding="utf-8")
        self.assertLess(text.index("export PATH="), text.index("command -v claude"))
        self.assertIn(".local/bin", text)

    def test_the_wrapper_stops_cleanly_when_the_cli_is_missing(self):
        """Exercised, not asserted: run it with an empty environment."""
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                ["/bin/bash", str(self.WRAPPER), "W-001"],
                env={"HOME": tmp + "/nohome", "PATH": "/usr/bin:/bin",
                     "PIGMENT_LANE3_LOG_DIR": tmp},
                capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(result.returncode, 1)
            log = Path(tmp, "lane3.log").read_text(encoding="utf-8")
            self.assertIn("no 'claude' on PATH", log)
            self.assertIn("PATH=", log, "log the PATH it actually had, or the "
                                        "failure is unfixable from the log alone")

    def test_the_wrapper_is_in_the_sealed_set(self):
        """It matches tools/lane3*, so a run cannot rewrite its own scheduler."""
        hook = (ROOT / ".claude" / "hooks" / "sealed-set.py").read_text(encoding="utf-8")
        self.assertIn("tools/lane3", hook)


class ShippedWritsTest(unittest.TestCase):
    """Standing checks over every writ in the registry, W-003 included."""

    def writs(self):
        for path in sorted((ROOT / "protocol" / "writs").glob("W-*.md")):
            yield path.name, lane3_writ.parse(path.read_text(encoding="utf-8"))

    def test_every_shipped_writ_is_well_formed(self):
        for name, fields in self.writs():
            self.assertEqual(lane3_writ.validate(fields), [], name)

    def test_no_writ_grants_itself_a_dangerous_tool(self):
        """A writ that could rewrite production data by invoking a tool is a
        writ whose may_write list is decorative."""
        for name, fields in self.writs():
            self.assertNotIn("Agent", fields.get("tools", []), name)
            self.assertNotIn("ScheduleWakeup", fields.get("tools", []), name)

    def test_w003_forbids_the_tool_that_rewrites_artworks(self):
        """tools/audit_artworks.py has no read-only mode: it rewrites
        js/artworks.js in place. A rights audit that invoked it would repair
        the thing it was sent to observe."""
        body = (ROOT / "protocol/writs/W-003.md").read_text(encoding="utf-8")
        fields = lane3_writ.parse(body)
        self.assertTrue(any("audit_artworks" in c for c in fields["abort_if"]),
                        "invoking it must be an abort condition, not advice")
        self.assertIn("forbidden", body)

    def test_w003_honours_the_transient_failure_rule(self):
        """PIGMENT.md §14: a timeout or 429 is not a dead URL. A run that
        reports 200 dead images because Commons throttled it has produced a lie
        that costs a person a day to disprove."""
        body = (ROOT / "protocol/writs/W-003.md").read_text(encoding="utf-8")
        self.assertIn("transient", body.lower())
        self.assertIn("429", body)

    def test_w003_reports_and_does_not_repair(self):
        fields = dict(self.writs())["W-003.md"]
        self.assertEqual(fields["may_write"], ["protocol/runs/**"])
        for guarded in ("js/**", "docs/**", "tools/**"):
            self.assertIn(guarded, fields["may_not"])


class WritFourTest(unittest.TestCase):
    """W-004 is the first writ allowed to change a production file.

    It gets that permission because an external authority decides the right
    answer: the correct `image.page` is the Commons file page the record's own
    `image.src` resolves to. Nothing about it is a judgement. These tests guard
    the boundary that makes that true.
    """

    def setUp(self):
        self.body = (ROOT / "protocol/writs/W-004.md").read_text(encoding="utf-8")
        self.fields = lane3_writ.parse(self.body)
        # Prose wraps. Asserting on a literal substring of a hand-wrapped
        # paragraph tests the line breaks, not the meaning -- this failed on
        # "leave the\nrecord exactly as it is", which is present and correct.
        self.prose = " ".join(self.body.replace("*", "").split())

    def test_it_may_touch_only_the_catalog_and_its_own_report(self):
        allowed = set(self.fields["may_write"])
        self.assertEqual(allowed - {"protocol/runs/**"}, {"js/catalog-*.js"})

    def test_it_names_the_catalog_by_glob_not_by_number(self):
        """C2, the rule the validator already learned and this writ broke:
        numbered data families are discovered, never listed. Written as
        catalog-1..5 and wrong four files later — catalog-6 through 9 exist,
        and a run confined to the named five would leave their records unfixed
        while its own verifier still failed."""
        for name in self.fields["may_write"]:
            self.assertNotRegex(name, r"catalog-\d+\.js",
                                "a numbered catalog file is named explicitly")
        on_disk = sorted((ROOT / "js").glob("catalog-*.js"))
        self.assertGreater(len(on_disk), 5,
                           "if this ever drops to 5 the regression is invisible")
        for guarded in ("js/artworks.js", "js/taxonomy.js", "js/app.js",
                        "tools/**", "docs/**"):
            self.assertIn(guarded, self.fields["may_not"])

    def test_its_success_is_decided_by_a_gate_that_fails_today(self):
        """A writ whose verifier already passes cannot tell you it worked."""
        self.assertTrue(any("check_image_pages" in v and "--require-commons" in v
                            for v in self.fields["verifier"]),
                        "the gate must be one of its verifiers")
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "check_image_pages.py"),
             "--require-commons"], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(result.returncode, 1,
                         "if this passes before W-004 runs, the gate is vacuous")

    def test_changing_anything_but_the_page_field_aborts(self):
        aborts = " ".join(self.fields["abort_if"]).lower()
        self.assertIn("image.page", aborts)
        self.assertIn("record count changes", aborts)
        self.assertIn("audit_artworks", aborts)

    def test_it_forbids_guessing_a_replacement(self):
        """Five records in A2 carry permanent caveats because a gap was filled
        with something that looked right."""
        self.assertIn("never guessed", self.prose)
        self.assertIn("leave the record exactly as it is", self.prose)

    def test_it_carries_the_a2_formatting_warning(self):
        """A diff where every line moved is a diff nobody can review, and
        review is the only thing between this and A2 happening again."""
        self.assertIn("do not reformat", self.prose.lower())
        self.assertIn("A2", self.prose)

    def test_it_stays_ungranted_until_a_person_signs(self):
        self.assertEqual(self.fields["status"], "proposed")
        self.assertFalse(self.fields.get("granted_by"))


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
        self.assertIn('git diff --name-only "$BASE"', self.script)
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

    def test_the_proposed_diff_includes_new_files(self):
        """`git diff` is silent on untracked files, and a W-001 report is
        precisely that: a brand-new file under protocol/runs/. Without an
        intent-to-add the runner printed "proposed diff follows" over nothing,
        every time, whatever the run had actually written."""
        outcome = self.script[self.script.index("Outcome"):]
        dry = outcome[outcome.index('if [ "$DRY_RUN" -eq 1 ]'):]
        self.assertIn("git add -N", dry)
        self.assertLess(
            dry.index("git add -N"), dry.index("diff \"$BASE\""),
            "the intent-to-add must precede the diff it exists to populate",
        )

    def test_the_human_facing_diff_does_not_page(self):
        """git pipes terminal output through less, which waits for a keypress
        the caller does not know to give. The run then holds its lock and its
        worktree while looking finished, and the next invocation is refused
        with "another run holds the lock" -- a failure two steps from its
        cause. Only the diff printed for a human is affected; the two piped
        into grep already suppress the pager."""
        outcome = self.script[self.script.index("Outcome"):]
        dry = outcome[outcome.index('if [ "$DRY_RUN" -eq 1 ]'):]
        printed = [ln for ln in dry.splitlines()
                   if 'diff "$BASE"' in ln and "|" not in ln.replace("||", "")]
        self.assertTrue(printed, "expected a diff printed straight to the terminal")
        for line in printed:
            self.assertIn("--no-pager", line, line.strip())

    def test_branch_emptiness_is_decided_by_commits_not_a_dirty_tree(self):
        """The first real run wrote a report, committed it, and was announced as
        having produced nothing -- because the runner asked `git status
        --porcelain`, which is clean precisely when a run has committed its own
        work. Whether a branch has anything on it is a question about the
        branch."""
        self.assertIn("rev-list --count", self.script)
        self.assertIn("has no commits", self.script)
        empty_msg = self.script.index("has no commits")
        counted = self.script.index("rev-list --count")
        self.assertLess(counted, empty_msg,
                        "the count must be taken before the verdict is printed")

    def test_only_the_runner_may_push(self):
        """Three sources disagreed and the run obeyed the writ, correctly: W-001
        and the writs README both said 'push the branch' while the runner's own
        constraint said never push and its PIGMENT_LANE3_PUSH gate defaulted
        off. The first real run pushed to origin. One push path now."""
        self.assertIn("PIGMENT_LANE3_PUSH", self.script)
        self.assertIn("Do NOT commit, push or merge", self.script)
        for doc in ("protocol/writs/W-001.md", "protocol/writs/README.md"):
            text = (ROOT / doc).read_text(encoding="utf-8")
            self.assertNotIn("Push the branch", text,
                             "%s still instructs the run to push" % doc)

    def test_the_prompt_survives_an_apostrophe(self):
        """A heredoc nested inside $( ) is parsed for quotes by macOS bash, so
        one apostrophe in the prompt made the entire script unparseable. Prompt
        text is prose; it will contain apostrophes. Written via a plain
        redirect now, and this asserts the structure rather than the absence."""
        self.assertIn('cat > "$SCRATCH/prompt.txt"', self.script)
        # Comments are allowed to name the broken form; code is not.
        code = "\n".join(ln for ln in self.script.splitlines()
                         if not ln.lstrip().startswith("#"))
        self.assertNotIn('PROMPT="$(cat <<', code)
        block = self.script[self.script.index('cat > "$SCRATCH/prompt.txt"'):
                            self.script.index('PROMPT="$(cat "$SCRATCH/prompt.txt")"')]
        self.assertIn("'", block, "keep an apostrophe here: it is the regression")
        checked = subprocess.run(["bash", "-n", str(ROOT / "tools" / "lane3-run.sh")],
                                 capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)

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
