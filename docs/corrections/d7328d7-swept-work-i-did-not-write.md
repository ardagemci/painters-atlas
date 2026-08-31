# Correction to commit d7328d7

**What happened:** `d7328d7` committed and pushed two files authored by another
session, under a commit message that describes neither. I wrote the message. I
did not write the files.

| path | lines | author |
|---|---|---|
| `THEORY_001.md` | 831 | another session / the theory team — **not me** |
| `.gitignore` | +1 (`passport-test.html`) | another session — **not me** |

The commit message says "reconcile state.json with the message log." That
describes `protocol/tasks/RIGHTS-001/state.json`, `tests/test_protocol_ids.py`
and `pigment_coordinator/store.py`, which are mine. It does not mention the
other two, and it carries my `Co-Authored-By` line over all five.

## How

Both files had sat uncommitted in the main checkout all session. I had seen them
in `git status` repeatedly and deliberately left them alone, saying so each time.

The reconciliation work was done in a worktree at
`scratchpad/wt-rec`. The shell's working directory then returned to the main
checkout — `git worktree remove` had run in an earlier compound command — and I
did not re-check it before the commit block. That block ran:

```
git add -A && git commit … && git merge --no-ff rights/001-reconcile-state
```

`git add -A` in the main checkout staged everything uncommitted there, including
the other session's two files. The merge that followed reported "Already up to
date" — the commit had landed directly on `main`, not on the branch — and I read
past it. The push then published all five files.

Two signals said so at the time and I did not act on either: the merge's
"Already up to date", and a push range (`1093230..d7328d7`) that should have been
impossible if the work were sitting on a branch. I noticed the contradiction only
after the push.

## The same failure, twice

`docs/corrections/f445a4d-false-test-claim.md` opens:

> "a parallel agent working on the 20 wrong-artwork records, whose edits landed
> in the main checkout rather than its worktree — which is how the change came
> to be committed by someone who had not written it."

Identical mechanism, opposite seat: there, someone else's stray edits were swept
by this project's own commit; here, I did the sweeping. Gate 4 was extended with
the worktree convention after that incident. A convention did not prevent the
recurrence, because the convention assumes the actor knows which directory they
are in, and that is precisely what fails.

## What was *not* wrong

The reconciliation itself is correct and was verified before the commit:
`workflow_state` `theory_revision`, round 1, `message_count` 2,
`last_message_type` `challenge`, `analyst_count` honestly still 0. Validator exit
0, 183 tests passing. `TestTaskStateMatchesTheMessageLog` was proved
non-vacuous against the pre-reconciliation values. None of that is affected.

## Disposition

The owner chose to leave the content in place and record the error rather than
revert the two paths or rewrite the pushed commit. Rewriting published history in
a tree another session works in is the failure this project most wants to avoid,
and deleting another session's work to tidy my own commit would be worse than the
mistake.

So: **`THEORY_001.md` on `main` is the other session's document, not mine.**
Anyone reading `git log` for its provenance will find the wrong author and an
unrelated message. This file is the correction.

## Note on THEORY_001.md itself

Its front matter carries `task_id: THEORY-001`, which
`^(PIG|RIGHTS|IFACE|CONTENT|PLATFORM)-[0-9]{3,}$` refuses, and which
`tests/test_protocol_ids.py::test_a_rejected_historical_id_is_still_rejected`
deliberately keeps refusing. It also names `message_type:
final_synthesis_and_execution_handoff` and `workflow_state: claude_analysis`,
neither of which is in `protocol/message-schema.json`. The document cannot route
as-is. That is a matter for whoever authored it; it is not repaired here, because
repairing another session's in-flight artifact without being asked is how this
correction came to be needed.

## The lesson, stated so it can be checked

`git add -A` has no place in this repository. Every commit here stages explicit
paths, and `pwd` is confirmed in the same command block as the commit, not
inferred from an earlier `cd`. The rule is not "use a worktree" — that rule
existed and did not hold. The rule is **stage by name, so that being in the wrong
directory cannot silently widen a commit.**
