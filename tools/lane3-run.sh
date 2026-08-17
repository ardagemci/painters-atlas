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
HOOK=".claude/hooks/sealed-set.sh"
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
TREE="$SCRATCH/tree"
git worktree add -q -b "$BRANCH" "$TREE" main \
  || die "could not create an isolated worktree; refusing to run in place."
cleanup_tree() { git worktree remove --force "$TREE" 2>/dev/null || true; }
trap 'cleanup_tree; rm -rf "$SCRATCH"; rm -f "$LOCK"' EXIT

note "writ ${WRIT_ID} (${STATUS}) · base ${BASE} · branch ${BRANCH}"
[ "$DRY_RUN" -eq 1 ] && note "DRY RUN — proposes a diff, writes nothing, pushes nothing"

# ── The run ─────────────────────────────────────────────────────────────────
PERMISSION_MODE="dontAsk"
[ "$DRY_RUN" -eq 1 ] && PERMISSION_MODE="plan"

PROMPT="$(cat <<PROMPT_END
You are executing Lane III writ ${WRIT_ID} under CLAUDE.md §0.

$(cat "$SCRATCH/writ.md")

Binding constraints, in order of precedence:
  1. Write only to paths in may_write. Never to the sealed set.
  2. Run every verifier command. All must pass. Do not edit a verifier.
  3. Stop at ${BRANCH}. Never merge, never push, never touch main.
  4. Abort and report on any abort_if condition or CLAUDE.md §5 condition.
  5. A partial result with an honest report beats a green you had to widen.
PROMPT_END
)"

set +e
perl -e 'alarm shift; exec @ARGV' "$WALL_CLOCK" \
  "$CLAUDE_BIN" -p "$PROMPT" \
    --output-format json \
    --max-turns "$(field max_turns)" \
    --max-budget-usd "$(field max_budget_usd)" \
    --permission-mode "$PERMISSION_MODE" \
    --session-id "lane3-${WRIT_ID}-${STAMP}" \
    > "$SCRATCH/result.json" 2> "$SCRATCH/harness.err"
RUN_EXIT=$?
set -e

if [ "$RUN_EXIT" -eq 142 ]; then
  note "ABORTED: exceeded the ${WALL_CLOCK}s wall clock"
elif [ "$RUN_EXIT" -ne 0 ]; then
  note "ABORTED: harness exited ${RUN_EXIT}"
  head -20 "$SCRATCH/harness.err" >&2 || true
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

# Lane III never merges. Pushing is outward-facing and stays opt-in.
if [ "${PIGMENT_LANE3_PUSH:-0}" = "1" ]; then
  ( cd "$TREE" && git push -q origin "$BRANCH" ) && note "pushed ${BRANCH}"
else
  note "branch ${BRANCH} is local. Set PIGMENT_LANE3_PUSH=1 to push it."
fi
note "complete. The owner merges, or does not."
