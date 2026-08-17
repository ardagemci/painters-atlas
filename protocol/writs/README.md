# protocol/writs/

A **writ** is the user's standing approval for one *class* of autonomous work.
It is the Lane III authorization named in `CLAUDE.md` §0 and Gate 1.

Lane I approves work one task at a time, which is exactly what makes autonomy
impossible — the approval is the bottleneck. A writ moves the signature up one
level: the user approves a class once, with its verifier named and its blast
radius fixed, and the loop then runs that class without asking. Revocation is
deleting a line.

## Lifecycle

```
proposed  →  granted  →  revoked
```

- **`proposed`** — drafted by anyone, including an agent. Inert. A run must
  refuse to execute it.
- **`granted`** — the user changed the field and committed the file. **The
  commit is the signature**; there is no other grant mechanism, and no agent
  may set this field.
- **`revoked`** — the class stops immediately. Deleting the file has the same
  effect. Prefer revoking to deleting when the reasoning is worth keeping.

A run reads writs from `main`, never from its own branch, so a branch cannot
widen its own authorization.

**Precondition on every grant.** No writ may move to `granted` until the
sealed-set hook has been **observed refusing** a write to `tools/validate*`
inside a live run — not merely until the file exists. The runner checks the
weaker condition, because a script can only check what it can see; the stronger
one is yours.

The distinction is the point. `.claude/hooks/sealed-set.py` currently passes 29
tests and has never been exercised by a real harness. Its first draft passed
review, looked installed, and allowed all thirteen adversarial cases, because a
heredoc had quietly redirected the input it was meant to read. Only an
adversarial test caught it. **D-8** in `PIGMENT.md` §19 stays open until a live
refusal is seen.

## Required fields

| Field | Meaning |
| --- | --- |
| `writ_id` | `W-NNN`, permanent, never reused |
| `status` | `proposed` \| `granted` \| `revoked` |
| `class` | One sentence naming the work class. If it needs "and", write two writs |
| `verifier` | The exact commands that decide correctness. A writ with no verifier is not a writ |
| `may_write` | Path globs the run may edit. Binding — exceeds Gate 1, never widens it |
| `may_not` | Paths named explicitly for the reader's benefit; the sealed set applies regardless |
| `tools` | Optional allowlist passed to `--allowedTools`. Omitted means a conservative default. Grant the fewest tools the class needs — a read-and-report writ has no use for subagents or schedulers |
| `max_diff` | Line ceiling. Exceeding it aborts the run rather than truncating the work |
| `max_turns`, `max_budget_usd` | Per-run ceilings passed to the harness. **Measure these; do not guess them.** W-001 shipped with `max_turns: 10` against work that needs 25–30, and three runs were killed mid-sentence — twice at the moment before writing their output. A ceiling below the work it authorizes does not bound the run, it wastes it. The runner prints turns and cost on every run; set the ceiling from a run that finished, with headroom |
| `abort_if` | Conditions that stop the run and file a report |
| `granted_by`, `granted_at` | Filled by the user in the granting commit |

## What every run must do

1. Read this writ from `main` and confirm `status: granted`.
2. Work in an isolated branch or worktree (Gate 4). Never on `main`.
3. Stay inside `may_write`. The sealed set — `tools/validate*`,
   `tools/audit_*.py`, `tools/lane3*`, `CLAUDE.md`, `PIGMENT.md`, `protocol/`,
   `.claude/` — is unwritable in every writ, enforced by hook. The single
   carve-out is `protocol/runs/`, where the run writes its own report.
   `tools/lane3*` is in the set because it holds the authorization checks: a run
   that can rewrite its own runner needs no other exploit.
4. Run every command in `verifier`. All must pass.
5. Have the diff reviewed by an agent that did not write it (Van Eyck).
6. Push the branch. **Stop.** Lane III never merges; the user merges.
7. Append one line to `protocol/runs/ledger.jsonl` and write the run report.

## Abort rather than proceed

A run that hits any `abort_if` condition, any `CLAUDE.md` §5 escalation
condition, a failing verifier after its bounded retries, or a `may_write`
violation **stops and reports**. A partial branch with an honest report is a
good outcome. A branch that reached green by narrowing what green means is the
failure this whole structure exists to prevent.

## Writing a new writ

The test is not "is this useful" but **"can a machine decide it is right?"** If
closing the loop needs a person to look at the result, it is Lane II work and
no writ can change that. The highest-value writs are the ones that build new
deterministic checks, because each accepted check permanently moves a class of
work from Lane II into Lane III.
