#!/bin/bash
# launchd entry point for a scheduled Lane III run. (Phase 4)
#
# A thin wrapper, deliberately. launchd starts jobs with a nearly empty
# environment — PATH is /usr/bin:/bin:/usr/sbin:/sbin, no login shell, none of
# ~/.zshrc — so `claude`, installed in ~/.local/bin, is not on it. A runner that
# works perfectly by hand and fails only at 4am is the least debuggable shape of
# failure, so the environment is set here explicitly rather than inherited.
#
# Everything else stays in lane3-run.sh: this adds no authority and no
# decisions. It sets PATH, timestamps the log, and gets out of the way.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WRIT="${1:-W-001}"
LOG_DIR="${PIGMENT_LANE3_LOG_DIR:-$HOME/Library/Logs/pigment}"
LOG="$LOG_DIR/lane3.log"

export PATH="$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"
mkdir -p "$LOG_DIR"

# Keep the log bounded without needing newsyslog: trim to the last 2000 lines
# when it passes 5000. A scheduled job that quietly fills a disk is its own
# kind of failure.
if [ -f "$LOG" ] && [ "$(wc -l < "$LOG" | tr -d ' ')" -gt 5000 ]; then
  tail -2000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
fi

{
  echo "───────────────────────────────────────────────────────────"
  echo "$(date '+%Y-%m-%d %H:%M:%S %Z') · scheduled run · writ ${WRIT}"
  if ! command -v claude >/dev/null 2>&1; then
    echo "lane3-cron: no 'claude' on PATH — nothing ran. PATH=$PATH"
    exit 1
  fi
  cd "$REPO" || { echo "lane3-cron: cannot cd to ${REPO}"; exit 1; }
  tools/lane3-run.sh "$WRIT"
  echo "$(date '+%Y-%m-%d %H:%M:%S %Z') · exit ${?}"
} >> "$LOG" 2>&1
