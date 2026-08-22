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

## Scheduling (Phase 4)

`tools/com.pigment.lane3.plist` runs `W-001` daily at 09:17 through
`tools/lane3-cron.sh`. Install it:

```sh
cp tools/com.pigment.lane3.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.pigment.lane3.plist
```

`launchctl list | grep pigment` shows whether it is loaded;
`launchctl start com.pigment.lane3` fires one immediately, which is the honest
way to check it works rather than waiting until tomorrow.

**Three independent off switches**, and none of them requires understanding the
others: `launchctl unload` the plist, delete the plist, or set `W-001` to
`revoked` in `protocol/writs/`. The last one stops the class everywhere, whether
or not anything is scheduled — a run reads its writ from `main` before it does
anything else.

**What the schedule costs.** A clean W-001 run is 13–19 turns and $0.29–$0.59.
Daily is roughly $9–15 a month for a report that mostly says "nothing drifted".
That is the correct output when nothing drifted, but if the atlas goes quiet for
a stretch, weekly (`<key>Weekday</key><integer>1</integer>`) buys the same signal
for a seventh of the money.

**Why the wrapper exists.** launchd starts a job with `PATH=/usr/bin:/bin` and
no login shell, so the CLI in `~/.local/bin` is not on it. A runner that works
perfectly by hand and fails only at 09:17 is the least debuggable failure this
project could ship, so the wrapper sets the environment explicitly, logs the
`PATH` it actually had when the CLI is missing, and exits without spending.

**Logs** are at `~/Library/Logs/pigment/lane3.log`, timestamped per run and
trimmed to the last 2000 lines once past 5000 — a scheduled job that quietly
fills a disk is its own kind of failure.

## Retention

Nothing here is pruned automatically. The ledger is the only durable evidence
that the lane behaved, and it is small — a line per run. Reports may be thinned
by hand once a writ has a long clean record, but never the ledger.
