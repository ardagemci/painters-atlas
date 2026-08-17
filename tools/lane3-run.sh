#!/bin/bash
# Execute one Lane III writ. (CLAUDE.md §0)
#
#   tools/lane3-run.sh W-001              # a real run; requires status: granted
#   tools/lane3-run.sh W-001 --dry-run    # proposes a diff, changes nothing
#
# The guards below run before anything is spawned, in a deliberate order: the
# cheapest and most consequential first, so a misconfigured run dies before it
# costs a token. Every one of them refuses rather than degrades. A run that
# cannot establish its own authority does not proceed with less of it.
#
# macOS notes, learned the hard way: this host has neither `flock` nor
# `timeout`. `shlock` (BSD, /usr/bin) and a perl `alarm` are the substitutes,
# and both are present on a stock system.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

WRIT_ID="${1:-}"
MODE="${2:-}"
DRY_RUN=0
[ "$MODE" = "--dry-run" ] && DRY_RUN=1

LOCK="/tmp/pigment-lane3.lock"
HOOK=".claude/hooks/sealed-set.py"
SETTINGS=".claude/settings.json"
CLAUDE_BIN="${PIGMENT_CLAUDE_BIN:-claude}"
WALL_CLOCK="${PIGMENT_LANE3_TIMEOUT:-900}"

die()  { echo "lane3: $*" >&2; exit 1; }
note() { echo "lane3: $*"; }

# ── Guard 1 · a writ was named ──────────────────────────────────────────────
[ -n "$WRIT_ID" ] || die "usage: tools/lane3-run.sh <WRIT_ID> [--dry-run]"
[ -z "$MODE" ] || [ "$MODE" = "--dry-run" ] || die "unknown option: $MODE"

# ── Guard 2 · the writ is read from main, never from the current branch ─────
# A branch that could supply its own writ could widen its own authorization.
WRIT_PATH="protocol/writs/${WRIT_ID}.md"
WRIT_TEXT="$(git show "main:${WRIT_PATH}" 2>/dev/null)" \
  || die "no writ at ${WRIT_PATH} on main (a writ on a branch is not a writ)"

SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"; [ -e "$LOCK" ] && rm -f "$LOCK" || true' EXIT
printf '%s\n' "$WRIT_TEXT" > "$SCRATCH/writ.md"

# ── Guard 3 · the writ is well-formed ───────────────────────────────────────
python3 tools/lane3_writ.py "$SCRATCH/writ.md" --validate \
  || die "writ ${WRIT_ID} is malformed; refusing to infer intent"

field() { python3 tools/lane3_writ.py "$SCRATCH/writ.md" --get "$1"; }
STATUS="$(field status)"

# ── Guard 4 · authorization ─────────────────────────────────────────────────
if [ "$DRY_RUN" -eq 0 ]; then
  [ "$STATUS" = "granted" ] \
    || die "writ ${WRIT_ID} is '${STATUS}', not 'granted'. Only the owner grants, by commit."
else
  [ "$STATUS" != "revoked" ] || die "writ ${WRIT_ID} is revoked; not even a dry run."
fi

# ── Guard 5 · D-8, the sealed-set hook must be real before any granted run ──
# CLAUDE.md §0 says the sealed set is enforced by hook rather than instruction.
# Until that hook exists the claim is prose, and prose does not stop an agent
# from editing its own grader. Dry runs are exempt: they mutate nothing.
if [ "$DRY_RUN" -eq 0 ]; then
  [ -x "$HOOK" ] \
    || die "sealed-set hook missing at ${HOOK} (PIGMENT.md §19 D-8). No granted run before Phase 3."
  grep -q "sealed-set" "$SETTINGS" 2>/dev/null \
    || die "${HOOK} exists but is not registered in ${SETTINGS}; an unregistered hook enforces nothing."
fi

# ── Guard 6 · the harness exists ────────────────────────────────────────────
command -v "$CLAUDE_BIN" >/dev/null 2>&1 \
  || die "no '${CLAUDE_BIN}' on PATH. The desktop app's copy is a Linux binary in a VM and cannot run here; install the native CLI or set PIGMENT_CLAUDE_BIN."

# ── Guard 7 · one run at a time ─────────────────────────────────────────────
# Overlapping runs on the same writ would race on the branch and the ledger.
shlock -f "$LOCK" -p $$ || die "another run holds ${LOCK}; not starting a second."

# ── Isolation · Gate 4, never on main ───────────────────────────────────────
BASE="$(git rev-parse --short main)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BRANCH="lane3/${WRIT_ID}-${STAMP}"
# --session-id must be a UUID; the harness rejects anything else. The
# human-readable writ/timestamp label stays on the branch name and in the
# notes below — it just can't double as the session id.
SESSION_ID="$(uuidgen | tr 'A-Z' 'a-z')"
TREE="$SCRATCH/tree"
git worktree add -q -b "$BRANCH" "$TREE" main \
  || die "could not create an isolated worktree; refusing to run in place."
cleanup_tree() { git worktree remove --force "$TREE" 2>/dev/null || true; }
trap 'cleanup_tree; rm -rf "$SCRATCH"; rm -f "$LOCK"' EXIT

note "writ ${WRIT_ID} (${STATUS}) · base ${BASE} · branch ${BRANCH} · session ${SESSION_ID}"
[ "$DRY_RUN" -eq 1 ] && note "DRY RUN — proposes a diff, writes nothing, pushes nothing"

# ── The run ─────────────────────────────────────────────────────────────────
# Same permission mode for both: the worktree (Gate 4) is what makes this
# safe, not the mode. "plan" would stop the agent from writing anything at
# all, even into the disposable worktree, so a dry run could never show a
# real proposed diff — it would just prove the guards and verifiers ran.
PERMISSION_MODE="dontAsk"

# The mode has to be stated. A run once saw PIGMENT_LANE3 armed and the hook
# firing while the writ read `proposed`, could not reconcile the two, and
# aborted — correctly, on the information it had. It had no way to know it was
# a rehearsal because the prompt never said so.
if [ "$DRY_RUN" -eq 1 ]; then
  MODE_NOTE="This is a DRY RUN — a rehearsal of an ungranted writ (status: ${STATUS}).
  Do the work as specified so the owner can read a real proposed diff. Your
  worktree is disposable and nothing you write here will be committed, pushed
  or merged. The sealed set still applies and the hook is armed, deliberately:
  a rehearsal that skipped the guards would rehearse the wrong thing.
  Do NOT abort merely because the writ is not granted — that is expected here."
else
  MODE_NOTE="This is a REAL RUN of a granted writ. Your work will be committed
  to ${BRANCH} and left for the owner to review. It will not be merged."
fi

PROMPT="$(cat <<PROMPT_END
You are executing Lane III writ ${WRIT_ID} under CLAUDE.md §0.

${MODE_NOTE}

$(cat "$SCRATCH/writ.md")

Binding constraints, in order of precedence:
  1. Write only to paths in may_write. Never to the sealed set.
  2. Run every verifier command. All must pass. Do not edit a verifier.
  3. Stop at ${BRANCH}. Never merge, never push, never touch main.
  4. Abort and report on any abort_if condition or CLAUDE.md §5 condition.
  5. A partial result with an honest report beats a green you had to widen.
  6. Do the writ and only the writ. No subagents, no scheduling, no side quests.
PROMPT_END
)"

# PIGMENT_LANE3 arms the sealed-set hook; the two roots tell it what the run
# owns. Without them the hook cannot tell inside from outside and denies
# everything — which is the correct failure, but a useless run.
export PIGMENT_LANE3=1
export PIGMENT_LANE3_ROOT="$TREE"
export PIGMENT_LANE3_REPO="$REPO"

# An allowlist, not a blocklist. A read-and-report writ has no business
# spawning subagents or scheduling wakeups, and one run did both.
TOOLS="$(field tools 2>/dev/null | paste -sd, - 2>/dev/null || true)"
[ -n "$TOOLS" ] || TOOLS="Read,Grep,Glob,Bash,Write,Edit"
note "tools: ${TOOLS}"

set +e
perl -e 'alarm shift; exec @ARGV' "$WALL_CLOCK" \
  "$CLAUDE_BIN" -p "$PROMPT" \
    --output-format json \
    --max-turns "$(field max_turns)" \
    --max-budget-usd "$(field max_budget_usd)" \
    --permission-mode "$PERMISSION_MODE" \
    --allowedTools "$TOOLS" \
    --session-id "$SESSION_ID" \
    > "$SCRATCH/result.json" 2> "$SCRATCH/harness.err"
RUN_EXIT=$?
set -e

if [ "$RUN_EXIT" -eq 142 ]; then
  note "ABORTED: exceeded the ${WALL_CLOCK}s wall clock"
elif [ "$RUN_EXIT" -ne 0 ]; then
  note "ABORTED: harness exited ${RUN_EXIT}"
  head -20 "$SCRATCH/harness.err" >&2 || true
fi

# ── Sealed-set backstop · the guarantee the hook only approximates ──────────
# The hook decides Write and Edit exactly, but a Bash command is a program and
# no pattern settles what an arbitrary program writes. Git does: this asks the
# finished worktree which files actually moved. Complete, unbypassable from
# inside the run, and it runs before any outcome is declared — a run that
# touched the sealed set is void no matter how green its verifiers came back.
SEALED_TOUCHED="$(cd "$TREE" && git diff --name-only main \
  | grep -E '^(tools/validate|tools/audit_|tools/lane3|CLAUDE\.md|PIGMENT\.md|\.claude/|protocol/)' \
  | grep -v '^protocol/runs/' || true)"
if [ -n "$SEALED_TOUCHED" ]; then
  note "VOID: the run modified the sealed set —"
  printf '  %s\n' $SEALED_TOUCHED >&2
  note "discarding the branch. This is a finding about the run, not about Pigment."
  cleanup_tree
  git branch -D "$BRANCH" >/dev/null 2>&1 || true
  exit 1
fi

# ── Verification · the writ's own commands decide, not the agent ────────────
VERIFY_FAILED=0
while IFS= read -r command; do
  [ -n "$command" ] || continue
  note "verifier: ${command}"
  ( cd "$TREE" && eval "$command" ) >/dev/null 2>&1 || { VERIFY_FAILED=1; note "  FAILED"; }
done <<< "$(field verifier)"

# ── Diff ceiling ────────────────────────────────────────────────────────────
CHANGED=$(cd "$TREE" && git diff --shortstat main | grep -oE '[0-9]+ insertion|[0-9]+ deletion' | grep -oE '[0-9]+' | paste -sd+ - | bc 2>/dev/null || echo 0)
MAX_DIFF="$(field max_diff)"
if [ "${CHANGED:-0}" -gt "$MAX_DIFF" ]; then
  note "ABORTED: diff is ${CHANGED} lines against a ${MAX_DIFF} ceiling"
  VERIFY_FAILED=1
fi

# ── Outcome ─────────────────────────────────────────────────────────────────
if [ "$DRY_RUN" -eq 1 ]; then
  note "dry run complete — proposed diff follows, nothing was kept"
  ( cd "$TREE" && git diff main ) || true
  exit 0
fi

if [ "$RUN_EXIT" -ne 0 ] || [ "$VERIFY_FAILED" -ne 0 ]; then
  note "run did not pass. Branch ${BRANCH} kept for inspection; nothing merged."
  trap 'rm -rf "$SCRATCH"; rm -f "$LOCK"' EXIT   # keep the worktree
  exit 1
fi

# ── Commit · without this the whole run evaporates ──────────────────────────
# The worktree is deleted by the EXIT trap, so work that is not committed is
# work that never happened. This step was missing: a passing run used to push a
# branch with zero commits and report success — the same shape of defect as the
# validator that could not fail, arriving at the other end of the pipeline.
if [ -n "$(cd "$TREE" && git status --porcelain)" ]; then
  ( cd "$TREE" \
    && git add -A \
    && git -c user.name="pigment-lane3" -c user.email="lane3@pigment.local" \
         commit -q -m "lane3(${WRIT_ID}): ${STAMP}" \
         -m "Autonomous run under writ ${WRIT_ID}, base ${BASE}, session ${SESSION_ID}.
Verifiers passed. Sealed set untouched. Not reviewed by a person." )
  note "committed $(cd "$TREE" && git rev-parse --short HEAD) on ${BRANCH}"
else
  note "the run produced no changes — nothing to commit. Branch ${BRANCH} is empty."
fi

# Lane III never merges. Pushing is outward-facing and stays opt-in.
if [ "${PIGMENT_LANE3_PUSH:-0}" = "1" ]; then
  ( cd "$TREE" && git push -q origin "$BRANCH" ) && note "pushed ${BRANCH}"
else
  note "branch ${BRANCH} is local. Set PIGMENT_LANE3_PUSH=1 to push it."
fi
note "complete. The owner merges, or does not."
