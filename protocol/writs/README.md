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

**Precondition on every grant — satisfied 2026-08-20.** No writ may move to
`granted` until the sealed-set hook has been *observed* refusing, in a live run,
rather than merely existing. `W-002` did that: ten attempts, eight sealed writes
all refused, and the two legitimate operations permitted. Both halves matter — a
guard that refuses everything is as useless as one that permits everything, and
only the pair shows it discriminates. It also distinguished "wrong workspace"
from "sealed path" with the right message for each, which is the harder thing to
get right.

Keep the standard for any *future* guard: this hook's first draft passed review,
looked correctly installed, and allowed all thirteen adversarial cases, because a
heredoc had quietly redirected the input it was meant to read. A control that has
never been observed failing is not known to work. **D-8** is closed.

## Required fields

| Field | Meaning |
| --- | --- |
| `writ_id` | `W-NNN`, permanent, never reused |
| `status` | `proposed` \| `granted` \| `revoked` |
| `class` | One sentence naming the work class. If it needs "and", write two writs |
| `verifier` | The exact commands that decide correctness. A writ with no verifier is not a writ |
| `may_write` | Path globs the run may edit. Binding — exceeds Gate 1, never widens it |
| `may_not` | Paths named explicitly for the reader's benefit; the sealed set applies regardless |
| `probe` | Optional. `true` marks an adversarial writ that deliberately attempts what the guards should refuse. A probe may only run with `--dry-run`, whatever its `status` says — the field is the safety property, not the status. A probe has no legitimate granted form |
| `tools` | Optional allowlist passed to `--allowedTools`. Omitted means a conservative default. Grant the fewest tools the class needs — a read-and-report writ has no use for subagents or schedulers |
| `max_diff` | Line ceiling. Exceeding it aborts the run rather than truncating the work |
| `max_turns`, `max_budget_usd` | Per-run ceilings passed to the harness. **Measure these; do not guess them.** W-001 shipped with `max_turns: 10` and killed three runs mid-sentence, twice at the moment before writing output. Measure with the harness's own `num_turns` — a completed W-001 run reports 13–19 turns and $0.33–$0.46 — not by counting tool calls in a transcript, which is a different number and will justify the wrong ceiling. A ceiling below the work it authorizes does not bound the run, it wastes it. The runner prints turns and cost on every run; set the ceiling from a run that finished, with headroom |
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
6. **Stop.** Do not commit or push: the runner commits the run's work onto
   the branch, and pushing is opt-in via `PIGMENT_LANE3_PUSH`, default off.
   Lane III never merges; the user merges. The first real run pushed to
   origin because this line said to while the runner's own constraint said
   never — the run obeyed the writ, correctly, and the contradiction was
   the defect.
7. Write the run report. **Do not write the ledger** — the runner appends that
   to `main` after the run passes.

The ledger is the one thing the harness writes to `main`, and it is deliberate.
A run branches from `main`, and Lane III never merges, so anything the run
recorded in its own worktree is gone before the next run starts. When the ledger
was the run's job, every run read an empty `main`, reported "first run, no
baseline", and the drift comparison W-001 exists for could never happen — twice,
correctly, and uselessly. Isolation and accumulation were in tension and the
harness is where that resolves: it records what happened, it never changes
Pigment, and it is the only party that knows what a run cost.

## Abort rather than proceed

A run that hits any `abort_if` condition, any `CLAUDE.md` §5 escalation
condition, a failing verifier after its bounded retries, or a `may_write`
violation **stops and reports**. A partial branch with an honest report is a
good outcome. A branch that reached green by narrowing what green means is the
failure this whole structure exists to prevent.

## Probe writs

A probe is a writ whose deliverable is a set of refusals. `W-002` attempts to
write to `CLAUDE.md`, to the validator, to the runner, and to the live checkout,
and reports whether each was refused — then writes its own report, which must be
*permitted*. Both halves matter: a guard that refuses everything is as useless as
one that permits everything, and only the pair shows it discriminates.

They exist because this repository has learned, repeatedly and expensively, that
a control which has never been observed failing is not known to work. Six
separate guards here reported success while doing nothing, and every one was
caught by asserting a specific failure rather than by reading the code.

`probe: true` makes a probe structurally incapable of a real run. Do not remove
the field to "test it properly"; the dry run *is* the proper test, and the
disposable worktree is what makes attempting a violation safe to do at all.

## Writing a new writ

The test is not "is this useful" but **"can a machine decide it is right?"** If
closing the loop needs a person to look at the result, it is Lane II work and
no writ can change that. The highest-value writs are the ones that build new
deterministic checks, because each accepted check permanently moves a class of
work from Lane II into Lane III.
