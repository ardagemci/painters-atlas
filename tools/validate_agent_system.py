#!/usr/bin/env python3
"""Check that Pigment's team roster, agent definitions, and liaison contracts agree."""

import re
import sys
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors = []
    agents = {}
    for path in sorted((ROOT / ".claude" / "agents").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        match = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
        if not match:
            errors.append(f"{path}: missing YAML frontmatter")
            continue
        fields = dict(re.findall(r"^([a-z_]+):\s*(.+)$", match.group(1), re.MULTILINE))
        for required in ("name", "description", "tools", "model"):
            if required not in fields:
                errors.append(f"{path}: missing frontmatter field {required}")
        stable_id = fields.get("name", "")
        if stable_id != path.stem:
            errors.append(f"{path}: name {stable_id!r} does not match filename")
        if stable_id in agents:
            errors.append(f"{path}: duplicate stable ID {stable_id}")
        agents[stable_id] = path

    constitution = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    roster_ids = set(re.findall(r"\| \*\*[^|]+\*\* \| `([^`]+)` \|", constitution))
    file_ids = set(agents)
    for stable_id in sorted(roster_ids - file_ids):
        errors.append(f"CLAUDE.md roster has no agent file: {stable_id}")
    for stable_id in sorted(file_ids - roster_ids):
        errors.append(f"Agent file missing from CLAUDE.md roster: {stable_id}")

    required_files = (
        "protocol/message-schema.json", "protocol/analyst-packet-schema.json",
        "coordinator/prompts/chatgpt-theory.md", "coordinator/prompts/claude-synthesis.md",
        "coordinator/prompts/theory-liaison.md", "coordinator/prompts/synthesis-liaison.md",
        ".claude/agents/claude-synthesis-liaison.md",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            errors.append(f"Missing team contract: {relative}")

    schema = json.loads((ROOT / "protocol" / "analyst-packet-schema.json").read_text(encoding="utf-8"))
    liaison_text = (ROOT / ".claude" / "agents" / "claude-synthesis-liaison.md").read_text(encoding="utf-8")
    examples = re.findall(r"```json\n(.*?)\n```", liaison_text, re.DOTALL)
    if len(examples) != 1:
        errors.append("Claude synthesis liaison must contain exactly one JSON packet example")
    else:
        try:
            example = json.loads(examples[0])
            required = set(schema["required"])
            if set(example) != required:
                errors.append(f"Claude liaison example differs from analyst schema; missing={sorted(required - set(example))}, extra={sorted(set(example) - required)}")
        except json.JSONDecodeError as exc:
            errors.append(f"Claude liaison JSON example is invalid: {exc}")

    protocol = (ROOT / "protocol" / "PROTOCOL.md").read_text(encoding="utf-8")
    for phrase in ("Theory Liaison", "Synthesis Liaison", "analyst-packet-schema.json", "Coordinator Kernel"):
        if phrase not in protocol and phrase not in constitution:
            errors.append(f"Team documentation does not define {phrase}")

    if errors:
        print("AGENT SYSTEM: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"AGENT SYSTEM: PASS ({len(agents)} Claude agents, 2 liaison prompts, 2 schemas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
