"""The task-id rule, and the four places that must agree about it.

Why this file exists
--------------------
`protocol/oriented/README.md` declared four Oriented Protocols with four task-id
prefixes — RIGHTS-, IFACE-, CONTENT-, PLATFORM- — while the message schema, the
analyst-packet schema and the Coordinator all still enforced `^PIG-[0-9]{3,}$`.
`RIGHTS-001` was therefore unroutable: a Theory Brief that was valid in every
other respect (all required fields present, one violation) could not be
ingested, and the work sat uncommitted in a worktree.

That was the SECOND time. `protocol/tasks/PIG-001/unrouted/liaison-incoming-analysis.json`
already recorded `THEORY-001` being rejected for the same reason. A rule
enforced in three places and documented in a fourth will drift unless something
compares them, so this compares them.

The prefix list is enumerated rather than open-ended (`^[A-Z]+-`) on purpose. An
open pattern would have accepted `THEORY-001` and `RIGHTS-001` silently, and a
typo would mint a namespace nobody meant to create. Enumeration makes adding an
Oriented Protocol a deliberate act in four files at once — which is exactly what
these tests require.
"""
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: The one true list. Every site below must agree with it, and with the OP index.
PREFIXES = ("PIG", "RIGHTS", "IFACE", "CONTENT", "PLATFORM")
PATTERN = "^(" + "|".join(PREFIXES) + ")-[0-9]{3,}$"


def _prefixes_from_pattern(pat):
    """Pull the alternation out of a task-id pattern, order preserved."""
    m = re.search(r"\^\(([A-Z|]+)\)-", pat)
    return tuple(m.group(1).split("|")) if m else ()


class TestTaskIdPatternAgreement(unittest.TestCase):
    """The three enforcement points must carry the same list, in the same order."""

    def test_message_schema(self):
        d = json.loads((ROOT / "protocol" / "message-schema.json").read_text(encoding="utf-8"))
        self.assertEqual(_prefixes_from_pattern(d["properties"]["task_id"]["pattern"]), PREFIXES)

    def test_analyst_packet_schema(self):
        d = json.loads((ROOT / "protocol" / "analyst-packet-schema.json").read_text(encoding="utf-8"))
        self.assertEqual(_prefixes_from_pattern(d["properties"]["task_id"]["pattern"]), PREFIXES)

    def test_coordinator(self):
        src = (ROOT / "pigment_coordinator" / "util.py").read_text(encoding="utf-8")
        m = re.search(r'TASK_ID_RE = re\.compile\(r"([^"]+)"\)', src)
        self.assertIsNotNone(m, "TASK_ID_RE not found in pigment_coordinator/util.py")
        self.assertEqual(_prefixes_from_pattern(m.group(1)), PREFIXES)


class TestOrientedProtocols(unittest.TestCase):
    """The OP index and the task-id rule describe the same set of protocols.

    This is the join that was missing. Declaring an OP in prose while the
    schemas do not know its prefix is precisely the defect that blocked
    RIGHTS-001, and it is invisible until someone tries to route a message."""

    INDEX = ROOT / "protocol" / "oriented" / "README.md"

    def _table_prefixes(self):
        rows = re.findall(r"\|\s*OP-([A-Z]+)\s*\|\s*`([A-Z]+)-`\s*\|", self.INDEX.read_text(encoding="utf-8"))
        return rows

    def test_every_declared_op_has_a_routable_prefix(self):
        for op, prefix in self._table_prefixes():
            with self.subTest(op=op):
                self.assertIn(prefix, PREFIXES,
                              "OP-%s declares prefix %s- which no schema accepts. A message "
                              "carrying it cannot be ingested." % (op, prefix))

    def test_every_op_has_a_definition_file(self):
        for op, _ in self._table_prefixes():
            with self.subTest(op=op):
                self.assertTrue((ROOT / "protocol" / "oriented" / ("OP-%s.md" % op)).is_file(),
                                "OP-%s is indexed but has no definition file" % op)

    def test_no_orphan_prefix(self):
        """A prefix the schemas accept but no OP declares is a namespace nobody
        owns. PIG- is exempt: it is the cross-cutting root, not an OP."""
        declared = {p for _, p in self._table_prefixes()} | {"PIG"}
        self.assertEqual(set(PREFIXES) - declared, set())


class TestExistingTasksAreRoutable(unittest.TestCase):
    def test_every_task_directory_matches_the_rule(self):
        """A task directory the Coordinator would refuse to open is a task that
        cannot be worked. This catches the RIGHTS-001 state directly."""
        rx = re.compile(PATTERN)
        bad = [p.name for p in sorted((ROOT / "protocol" / "tasks").iterdir())
               if p.is_dir() and not rx.match(p.name)]
        self.assertEqual(bad, [], "task directories the Coordinator cannot route: %s" % bad)

    def test_state_files_agree_with_their_directory(self):
        for p in sorted((ROOT / "protocol" / "tasks").iterdir()):
            state = p / "state.json"
            if not state.is_file():
                continue
            with self.subTest(task=p.name):
                self.assertEqual(json.loads(state.read_text(encoding="utf-8"))["task_id"], p.name)


class TestTheGuardActuallyFails(unittest.TestCase):
    """A guard that cannot fail is not a guard."""

    def test_the_old_pattern_would_be_caught(self):
        self.assertNotEqual(_prefixes_from_pattern("^PIG-[0-9]{3,}$"), PREFIXES)

    def test_a_rejected_historical_id_is_still_rejected(self):
        """THEORY-001 was refused once and must stay refused — widening the rule
        for Oriented Protocols must not quietly admit every invented prefix."""
        self.assertIsNone(re.match(PATTERN, "THEORY-001"))
        self.assertIsNone(re.match(PATTERN, "RIGHTS-01"))      # too few digits
        self.assertIsNone(re.match(PATTERN, "rights-001"))     # case
        self.assertIsNone(re.match(PATTERN, "XPIG-001"))       # anchored

    def test_the_ids_we_use_are_accepted(self):
        for good in ("PIG-001", "RIGHTS-001", "IFACE-001", "CONTENT-001", "PLATFORM-999"):
            self.assertIsNotNone(re.match(PATTERN, good), good)


if __name__ == "__main__":
    unittest.main()


class TestTaskStateMatchesTheMessageLog(unittest.TestCase):
    """`state.json` and `messages/` must describe the same task.

    RIGHTS-001 drifted: two messages were authored and merged while the
    Coordinator was out of the loop (the liaison packet was skipped by owner
    instruction, decision record D-001), so state.json still read `intake` /
    round 0 / message_count 0 while messages/ held a theory_brief and a
    challenge. Nothing detected it — the Coordinator's next ingest would have
    acted on a stale state and re-run a round that had already happened.

    These invariants are derived from what `engine.ingest` actually writes, and
    they hold for PIG-001, which was driven entirely through the Coordinator.
    `analyst_count` is checked against `analyses/` rather than against
    `message_count`: PIG-001 legitimately carries 5 messages and 4 packets.
    """

    TASKS = sorted(p for p in (ROOT / "protocol" / "tasks").iterdir()
                   if p.is_dir() and (p / "state.json").is_file())

    def _load(self, task):
        state = json.loads((task / "state.json").read_text(encoding="utf-8"))
        msgs = sorted((task / "messages").glob("*.json")) if (task / "messages").is_dir() else []
        return state, msgs

    def test_message_count_matches_the_files(self):
        for task in self.TASKS:
            state, msgs = self._load(task)
            with self.subTest(task=task.name):
                self.assertEqual(state["message_count"], len(msgs))

    def test_analyst_count_matches_the_packets(self):
        for task in self.TASKS:
            state, _ = self._load(task)
            n = len(sorted((task / "analyses").glob("*.json"))) if (task / "analyses").is_dir() else 0
            with self.subTest(task=task.name):
                self.assertEqual(state.get("analyst_count", 0), n)

    def test_a_task_with_messages_is_not_still_at_intake(self):
        """The exact RIGHTS-001 defect."""
        for task in self.TASKS:
            state, msgs = self._load(task)
            if not msgs:
                continue
            with self.subTest(task=task.name):
                self.assertNotEqual(state["workflow_state"], "intake",
                                    "%s holds %d message(s) but state reads intake"
                                    % (task.name, len(msgs)))

    def test_last_message_type_and_round_agree(self):
        for task in self.TASKS:
            state, msgs = self._load(task)
            if not msgs:
                continue
            last = json.loads(msgs[-1].read_text(encoding="utf-8"))
            with self.subTest(task=task.name):
                self.assertEqual(state["last_message_type"], last["message_type"])
                self.assertGreaterEqual(state["round"], last["round"])

    def test_events_are_sequenced(self):
        """record_event stamps a contiguous sequence; a hand-written event that
        omits it leaves a log that cannot be ordered."""
        for task in self.TASKS:
            state, _ = self._load(task)
            with self.subTest(task=task.name):
                self.assertEqual([e.get("sequence") for e in state["events"]],
                                 list(range(1, len(state["events"]) + 1)))
