#!/usr/bin/env python3
"""Read and validate a Lane III writ. (CLAUDE.md §0, protocol/writs/README.md)

A writ is the owner's standing approval for one class of autonomous work, so
every field this reads is a permission boundary. It is parsed here rather than
in the shell because a mis-parsed `may_write` is indistinguishable from a wider
one, and a run that silently widens its own authorization is the failure the
whole lane is built to prevent.

Deliberately not a YAML library: this repository has no dependencies and Python
3.9's stdlib has no yaml. The accepted subset is exactly what a writ uses --
scalars, `>-` folded blocks, and `- ` lists -- and anything outside it is a
parse error rather than a guess.

    python3 tools/lane3_writ.py protocol/writs/W-001.md --get status
    python3 tools/lane3_writ.py protocol/writs/W-001.md --validate
"""

import argparse
import sys

REQUIRED = [
    "writ_id", "status", "class", "verifier", "may_write",
    "max_diff", "max_turns", "max_budget_usd", "abort_if",
]
STATUSES = ["proposed", "granted", "revoked"]
INTEGER_FIELDS = ["max_diff", "max_turns"]


class WritError(Exception):
    pass


def _strip_comment(value):
    """Drop a trailing ` # comment`. A '#' with no leading space is data."""
    cut = value.find(" #")
    return value[:cut] if cut != -1 else value


def parse(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise WritError("writ must open with a '---' frontmatter fence")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise WritError("frontmatter is never closed by a second '---'")

    fields = {}
    key = None
    folding = False
    index = 1
    while index < end:
        raw = lines[index]
        line = raw.rstrip()
        index += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indented = line[:1] in (" ", "\t")

        if indented and folding and not line.lstrip().startswith("- "):
            fields[key] = (fields[key] + " " + line.strip()).strip()
            continue
        if indented and line.lstrip().startswith("- "):
            if key is None:
                raise WritError("list item before any key: " + line.strip())
            if not isinstance(fields[key], list):
                fields[key] = []
            fields[key].append(_strip_comment(line.lstrip()[2:]).strip())
            continue

        if ":" not in line:
            raise WritError("unparseable line: " + line.strip())
        key, _, value = line.partition(":")
        key = key.strip()
        value = _strip_comment(value).strip()
        folding = value in (">-", ">", "|", "|-")
        fields[key] = "" if folding else value
    return fields


def validate(fields):
    problems = []
    for name in REQUIRED:
        if name not in fields:
            problems.append("missing required field: " + name)
        elif fields[name] == "" or fields[name] == []:
            problems.append("required field is empty: " + name)

    status = fields.get("status")
    if status is not None and status not in STATUSES:
        problems.append("status must be one of %s, got %r" % ("/".join(STATUSES), status))

    for name in INTEGER_FIELDS:
        value = fields.get(name)
        if value not in (None, "") and not str(value).isdigit():
            problems.append("%s must be a positive integer, got %r" % (name, value))

    for name in ("verifier", "may_write", "abort_if"):
        if name in fields and not isinstance(fields[name], list):
            problems.append("%s must be a list of '- ' items" % name)

    # A granted writ without a signature is an unsigned cheque.
    if status == "granted":
        for name in ("granted_by", "granted_at"):
            if not fields.get(name):
                problems.append("a granted writ must record %s" % name)

    # The sealed set is not negotiable by writ. (CLAUDE.md §0)
    sealed = ("tools/validate", "tools/audit_", "tools/lane3",
              "CLAUDE.md", "PIGMENT.md", ".claude/")
    for path in fields.get("may_write", []) or []:
        if path.startswith("protocol/") and not path.startswith("protocol/runs"):
            problems.append("may_write may not reach into protocol/ except protocol/runs: " + path)
        for seal in sealed:
            if path.startswith(seal):
                problems.append("may_write names a sealed path: " + path)
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("writ")
    parser.add_argument("--get", metavar="FIELD")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args(argv)

    try:
        with open(args.writ, encoding="utf-8") as handle:
            fields = parse(handle.read())
    except OSError as error:
        print("cannot read writ: %s" % error, file=sys.stderr)
        return 2
    except WritError as error:
        print("malformed writ: %s" % error, file=sys.stderr)
        return 2

    if args.validate:
        problems = validate(fields)
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1 if problems else 0

    if args.get:
        value = fields.get(args.get)
        if value is None:
            print("no such field: %s" % args.get, file=sys.stderr)
            return 2
        print("\n".join(value) if isinstance(value, list) else value)
        return 0

    parser.error("one of --get or --validate is required")


if __name__ == "__main__":
    sys.exit(main())
