#!/usr/bin/env python3
"""PreToolUse hook: refuse writes to the sealed set during a Lane III run.
(CLAUDE.md §0, PIGMENT.md §19 D-8)

Scope, deliberately narrow: does nothing unless PIGMENT_LANE3=1, which only
tools/lane3-run.sh sets. Lane II is where verifier edits are *supposed* to
happen, with the user present, so a hook firing in every session would block the
work §0 reserves for a human.

The environment is a sound gate: this script inherits the harness process's
environment, and an agent's Bash calls are sibling children of that process.
Unsetting the variable inside a tool call cannot reach this copy.

Fails CLOSED. The first draft of this hook was a bash wrapper around a
`python3 - <<'PY'` heredoc, which fed the *script* to stdin instead of the
event; every parse threw, an `except: exit(0)` swallowed it, and the hook
allowed all thirteen adversarial cases while appearing installed. That is the
same defect class as backlog C7 -- a gate that reports success unconditionally.
So during a Lane III run, anything this script cannot positively understand is
denied rather than waved through.

WHAT THIS DOES NOT DO. Write and Edit carry a file path and are decided exactly.
Bash does not: a command is a program, and no pattern settles whether an
arbitrary program writes a given file. The Bash arm is a conservative blocklist
of obvious redirections and in-place editors. It raises the cost of a careless
write; it will not stop a determined one. The complete guarantee lives in
tools/lane3-run.sh, which diffs the finished worktree against main and voids the
run if any sealed path moved at all. Git knows exactly which files changed; this
script only guesses earlier and faster.
"""

import json
import os
import re
import sys

SEALED_PREFIXES = (
    "tools/validate", "tools/audit_", "tools/lane3",
    "CLAUDE.md", "PIGMENT.md", ".claude/",
)

WRITE_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")

BASH_WRITE_SHAPES = re.compile(
    r">>?\s*\S*(?:tools/(?:validate|audit_|lane3)|CLAUDE\.md|PIGMENT\.md|\.claude/|protocol/)"
    r"|(?:sed|perl|ruby)\s+[^|;]*-i"
    r"|\b(?:tee|truncate|dd|shred)\b[^|;]*(?:tools/|CLAUDE\.md|PIGMENT\.md|\.claude/|protocol/)"
    r"|\b(?:rm|mv|cp|chmod|chown|ln)\b[^|;]*"
    r"(?:tools/(?:validate|audit_|lane3)|CLAUDE\.md|PIGMENT\.md|\.claude/|protocol/)"
    r"|\bgit\s+(?:checkout|restore|reset|apply|revert|rm)\b"
)


def is_sealed(path):
    """protocol/ is sealed except the run's own report directory."""
    if not path:
        return False
    path = path.replace("\\", "/")
    # Strip a leading "./" as a *prefix*. str.lstrip("./") strips those two
    # characters in any order, which quietly turned ".claude/agents/x.md" into
    # "claude/agents/x.md" and un-sealed the whole agent directory.
    while path.startswith("./"):
        path = path[2:]
    for marker in ("protocol/runs/",):
        if marker in path:
            return False
    if "protocol/" in path:
        return True
    return any(
        path.startswith(prefix) or ("/" + prefix) in path
        for prefix in SEALED_PREFIXES
    )


def deny(reason):
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}, sys.stdout)
    sys.stdout.write("\n")
    sys.exit(0)


def allow():
    sys.exit(0)


def main():
    # Lane II and every ordinary session: this hook is not for you.
    if os.environ.get("PIGMENT_LANE3") != "1":
        allow()

    raw = sys.stdin.read()
    try:
        event = json.loads(raw)
    except Exception:
        deny("The sealed-set hook could not parse its own input, so it cannot "
             "tell whether this call is safe. During a Lane III run an "
             "unreadable guard denies rather than guesses.")

    # `[]` is valid JSON and has no .get, so this once raised AttributeError,
    # crashed, and a crash reads as allow — fail-open through the back door.
    if not isinstance(event, dict):
        deny("The sealed-set hook received %s where an event object was "
             "expected; refusing." % type(event).__name__)

    tool = event.get("tool_name", "")
    data = event.get("tool_input") or {}
    if not isinstance(data, dict):
        deny("Malformed tool_input reached the sealed-set hook; refusing.")

    if tool in WRITE_TOOLS:
        target = data.get("file_path") or data.get("notebook_path") or ""
        if is_sealed(target):
            deny(
                "%s is in the sealed set (CLAUDE.md §0). A Lane III run records "
                "a needed change to a verifier, a constitution or the harness as "
                "a finding in its report; it never makes the change. An agent "
                "that can edit its own grader can make any change pass." % target
            )

    elif tool == "Bash":
        command = data.get("command", "")
        if BASH_WRITE_SHAPES.search(command):
            deny(
                "This command looks like it writes to, moves or reverts "
                "something in the sealed set (CLAUDE.md §0). If it does not, it "
                "was still close enough to refuse on: run a verifier by "
                "executing it, and record any change it needs as a finding. "
                "Refused: %s" % command[:200]
            )

    allow()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException as error:                      # noqa: BLE001
        # A crashing guard must not read as permission. Outside a Lane III run
        # this is unreachable -- main() exits before touching anything.
        deny("The sealed-set hook failed while deciding this call (%s: %s). "
             "A guard that cannot answer denies." % (type(error).__name__, error))
