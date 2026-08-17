# protocol/runs/

Where Lane III runs write what they did. This is the one carve-out in the sealed
set: everything else under `protocol/` is unwritable to an autonomous run, and
this directory is not.

It is Gate 3's Decision Record in a form a machine can append to and a person can
grep — *"a deviation that is not recorded is a defect"*, applied to work nobody
watched happen.

## Two artefacts

**`ledger.jsonl`** — append-only, one line per run, never edited or rewritten.
The line is written even when the run aborts; an abort with a reason is a
result, and a gap in the ledger is the one thing that should never appear.

```json
{"run_id":"2026-08-17T03:14:22Z-W-001","writ":"W-001","base":"4fdb1d8",
 "branch":"lane3/W-001-20260817","outcome":"clean|drift|broken|aborted",
 "verifiers":[{"cmd":"…","exit":0}],"counts":{"artists":266,"catalog":350},
 "reviewer":"claude-quality-reviewer","turns":6,"cost_usd":0.41,
 "abort_reason":null,"report":"2026-08-17-W-001-4fdb1d8.md"}
```

`counts` is what makes drift detection possible: each run compares against the
last line carrying the same writ id.

**`YYYY-MM-DD-<writ>-<short-sha>.md`** — the human-readable report. Verifier
output verbatim, what changed, what the run concluded, and what it deliberately
did not do. Written in the same plain register as the rest of this repository:
state what happened, name what is uncertain, do not pad a clean result into
something that sounds like work.

## Reading the ledger

```sh
# every run that was not clean
grep -v '"outcome":"clean"' protocol/runs/ledger.jsonl

# what a writ has cost so far
grep '"writ":"W-001"' protocol/runs/ledger.jsonl \
  | python3 -c 'import sys,json; print(sum(json.loads(l)["cost_usd"] for l in sys.stdin))'
```

## Retention

Nothing here is pruned automatically. The ledger is the only durable evidence
that the lane behaved, and it is small — a line per run. Reports may be thinned
by hand once a writ has a long clean record, but never the ledger.
