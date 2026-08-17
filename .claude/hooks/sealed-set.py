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


def real(path):
    """Absolute and symlink-resolved. macOS hands out /var/folders temp dirs
    that are symlinks into /private/var, so comparing unresolved paths silently
    fails to match."""
    return os.path.realpath(os.path.abspath(os.path.expanduser(path)))


def under(path, root):
    if not root:
        return False
    root = real(root).rstrip("/") + "/"
    return (real(path) + "/").startswith(root)


def relative_to(path, root):
    return real(path)[len(real(root).rstrip("/")) + 1:].replace("\\", "/")


def is_sealed_within_tree(relative):
    """`relative` is already anchored to the run's worktree root.

    protocol/ is sealed except the run's own report directory.
    """
    if not relative:
        return False
    if relative.startswith("protocol/"):
        return not relative.startswith("protocol/runs/")
    return any(relative.startswith(prefix) for prefix in SEALED_PREFIXES)


def classify(path):
    """Where does this write land, and is it allowed?

    Anchoring matters more than the prefix list. An earlier version asked
    whether "/.claude/" appeared anywhere in the string, which sealed the user's
    global ~/.claude/ config and any unrelated checkout that happened to have a
    protocol/ directory -- it refused the harness's own plan file and broke a
    live run. Substring matching on paths is not scoping.

    Returns (decision, reason).
    """
    worktree = os.environ.get("PIGMENT_LANE3_ROOT")
    origin = os.environ.get("PIGMENT_LANE3_REPO")

    if not worktree or not origin:
        return "deny", (
            "The sealed-set hook is armed but was not told which tree the run "
            "owns (PIGMENT_LANE3_ROOT / PIGMENT_LANE3_REPO are unset), so it "
            "cannot scope this write. A guard that cannot tell inside from "
            "outside denies."
        )

    # The run owns its worktree and nothing else. Writing into the real
    # checkout is not a sealed-set question -- it is the wrong workspace, and
    # Gate 4 exists precisely so an autonomous mistake costs nothing.
    if under(path, origin):
        return "deny", (
            "%s is in the live repository. A Lane III run works only inside its "
            "own worktree (%s); writing to the checkout would put unreviewed "
            "work where the owner did not put it." % (path, worktree)
        )

    if under(path, worktree):
        relative = relative_to(path, worktree)
        if is_sealed_within_tree(relative):
            return "deny", (
                "%s is in the sealed set (CLAUDE.md §0). A Lane III run records "
                "a needed change to a verifier, a constitution or the harness as "
                "a finding in its report; it never makes the change. An agent "
                "that can edit its own grader can make any change pass." % relative
            )
        return "allow", ""

    # Outside both trees: the harness's own scratch, plan files, temp dirs.
    # Not this hook's business. It guards Pigment, not the filesystem.
    return "allow", ""


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
        if target:
            decision, reason = classify(target)
            if decision == "deny":
                deny(reason)

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
