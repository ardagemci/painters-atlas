#!/usr/bin/env python3
"""Build one Lane III ledger line. Written by the runner, never by the run.

The ledger used to be the agent's job, written inside its own disposable
worktree. Since Lane III never merges, that worktree was thrown away and the
next run branched from a `main` where the ledger still did not exist -- so every
run reported "first run, no baseline", forever, and W-001's entire purpose
(comparing today's counts against the last recorded run) could never happen.
Two runs produced two individually correct and collectively useless reports.

Isolation and accumulation were in direct tension. The resolution is that the
harness records, and only the harness: the runner appends to `main`, the run
never touches the ledger, and the agent is handed the previous entry to diff
against. That also fills in `turns` and `cost_usd`, which an agent cannot know
about itself and used to be recorded as null.

    python3 tools/lane3_ledger.py --writ W-001 --base abc1234 \\
        --branch lane3/... --outcome clean --report 2026-08-22-W-001-abc1234.md \\
        --result /tmp/result.json --verifiers /tmp/verifiers.txt
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone

# `artists: 266, movements: 80, ... catalog: 350 (tier1: 76), ...`
COUNT = re.compile(r"([a-z0-9 ]+?):\s*(\d+)")
PARENTHETICAL = re.compile(r"\(([a-z0-9 ]+?):\s*(\d+)\)")


def parse_counts(text):
    """Pull registry counts out of the validator's summary line.

    Deliberately tolerant: a count that stops being printed simply stops being
    recorded, rather than failing the run. The ledger is evidence, not a gate --
    the verifiers already decided whether the run passed.
    """
    counts = {}
    for line in text.splitlines():
        if "artists:" not in line and "AGENT SYSTEM" not in line:
            continue
        for label, value in PARENTHETICAL.findall(line):
            counts[label.strip().replace(" ", "_")] = int(value)
        stripped = PARENTHETICAL.sub("", line)
        for label, value in COUNT.findall(stripped):
            key = label.strip().replace(" ", "_").lstrip("_")
            if key and key not in counts:
                counts[key] = int(value)
    return counts


def read_findings(path):
    """A writ's own summary, when it produced one.

    The runner cannot compute this: what counts as a finding is the writ's
    business, not the harness's. W-003 writes a JSON with a `summary` block;
    anything shaped like that is recorded verbatim and never interpreted.
    """
    if not path:
        return None
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:
        return None
    summary = data.get("summary")
    return summary if isinstance(summary, dict) else None


def harness_usage(path):
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:
        return None, None, None
    return data.get("num_turns"), data.get("total_cost_usd"), data.get("subtype")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    for flag in ("writ", "base", "branch", "outcome", "report"):
        p.add_argument("--" + flag, required=True)
    p.add_argument("--result")
    p.add_argument("--verifiers")
    p.add_argument("--findings", help="a JSON file the run produced; its "
                                      "`summary` block is recorded verbatim")
    p.add_argument("--abort-reason", default=None)
    args = p.parse_args(argv)

    verifier_text = ""
    verifiers = []
    if args.verifiers:
        try:
            with open(args.verifiers, encoding="utf-8") as handle:
                verifier_text = handle.read()
        except OSError:
            verifier_text = ""
        for block in verifier_text.split("### ")[1:]:
            head, _, body = block.partition("\n")
            cmd, _, code = head.rpartition(" exit=")
            verifiers.append({"cmd": cmd.strip() or head.strip(),
                              "exit": int(code) if code.strip().isdigit() else None})

    turns, cost, subtype = harness_usage(args.result) if args.result else (None, None, None)

    line = {
        "run_id": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "-" + args.writ,
        "writ": args.writ,
        "base": args.base,
        "branch": args.branch,
        "outcome": args.outcome,
        "verifiers": verifiers,
        # Namespaced deliberately. These are scraped from whatever the
        # verifiers printed, which for every writ so far is the validator's
        # registry summary — so `attribution_required` here means "photo
        # credits requiring attribution" (96), while W-003's own report uses
        # that exact phrase for "artwork images under CC-BY" (7). Two
        # unrelated quantities under one name is worse than a missing number:
        # a missing number is visibly missing, and this one is present,
        # plausible, and wrong.
        "registry": parse_counts(verifier_text),
        "findings": read_findings(args.findings),
        "turns": turns,
        "cost_usd": cost,
        "stop_reason": subtype,
        "abort_reason": args.abort_reason,
        "report": args.report,
    }
    print(json.dumps(line, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
