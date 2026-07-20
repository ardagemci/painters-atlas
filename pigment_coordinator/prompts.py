import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .constants import REQUIRED_MESSAGE_FIELDS


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_system_prompt(repo_root: Path, pole: str) -> str:
    if pole == "chatgpt":
        return _read(repo_root / "coordinator" / "prompts" / "chatgpt-theory.md")
    return _read(repo_root / "coordinator" / "prompts" / "claude-synthesis.md")


def load_analyst_prompt(repo_root: Path, analyst_id: str) -> str:
    filename = "theory-liaison.md" if analyst_id == "theory-liaison" else "synthesis-liaison.md"
    return _read(repo_root / "coordinator" / "prompts" / filename)


def analyst_prompt(repo_root: Path, state: Dict[str, Any], expected: Dict[str, Any], message: Dict[str, Any]) -> str:
    schema = _read(repo_root / "protocol" / "analyst-packet-schema.json")
    return f"""Audit the proposed team artifact below before the Kernel routes it.

Return exactly one JSON object and no prose outside it. Copy these Kernel-owned fields exactly:
{json.dumps(expected, indent=2)}

ANALYST PACKET SCHEMA:
{schema}

PROPOSED TEAM ARTIFACT:
{json.dumps(message, indent=2)}

TASK CONTEXT:
{task_context(repo_root, state)}
"""


def task_context(repo_root: Path, state: Dict[str, Any], limit: int = 120000) -> str:
    task_dir = repo_root / "protocol" / "tasks" / state["task_id"]
    parts: List[str] = [
        f"TASK ID: {state['task_id']}",
        f"OBJECTIVE: {state['objective']}",
        f"CURRENT STATE: {state['workflow_state']}",
        f"ROUND: {state['round']} of {state['max_rounds']}",
    ]
    for path in sorted(task_dir.glob("*.md")):
        parts.append(f"\n--- {path.name} ---\n{_read(path)}")
    joined = "\n".join(parts)
    if len(joined) > limit:
        joined = joined[-limit:]
        joined = "[Earlier context truncated by Coordinator]\n" + joined
    return joined


def provider_prompt(
    repo_root: Path,
    state: Dict[str, Any],
    expected: Dict[str, Any],
    phase_instruction: str,
) -> str:
    schema = _read(repo_root / "protocol" / "message-schema.json")
    return f"""{phase_instruction}

Return exactly one JSON object and no prose outside it. It must validate against the schema below.
The Coordinator owns these fields; copy them exactly:
{json.dumps(expected, indent=2)}

All remaining required fields must be substantive. Do not expose hidden chain-of-thought; provide concise rationale and evidence.

MESSAGE SCHEMA:
{schema}

TASK CONTEXT:
{task_context(repo_root, state)}
"""


PHASE_INSTRUCTIONS = {
    "theory_brief": (
        "Produce the ChatGPT Theory Team's Theory Brief. Define the intended user outcome, scope, principles, "
        "information architecture, principal flow, meaningful alternatives, assumptions, risks, and testable product criteria. "
        "Remain theory-only and do not prescribe code."
    ),
    "challenge": (
        "Act as the Claude Synthesis Lead. Convene the relevant Claude specialists conceptually and produce a Challenge and "
        "Adaptation Report. Preserve sound intent, oppose weak assumptions, identify feasibility and accessibility consequences, "
        "and state requested revisions. Do not edit production files in this phase."
    ),
    "revision_or_defense": (
        "Produce the ChatGPT Theory Team's Revision or Defense. Answer every material Claude objection, concede unsupported "
        "details, defend only essential outcomes, and return either message_type revision or defense. Remain theory-only."
    ),
    "final_synthesis": (
        "Produce Claude's Final Synthesis. It must be buildable and testable. In accepted_points include non-empty entries beginning "
        "exactly 'user_outcome:', 'information_architecture:', and 'principal_flow:'. In evidence include a "
        "'feasibility-confirmed:' entry. Prefix any unresolved critical dispute or risk with '[critical]'. Do not edit production files yet."
    ),
    "implementation_report": (
        "The specification is frozen and build authorization is explicit. Operate as the Claude Synthesis and Build Team: use the "
        "project agents, build on an isolated branch or worktree, run repository checks, perform independent quality and browser "
        "review, save quality-review.md and desktop/mobile dark/light PNG evidence under the task directory, and return the Build "
        "Evidence Report envelope. Do not deploy, merge, or mark human_review_ready. Your final stdout must be only the JSON envelope."
    ),
    "review": (
        "Review Claude's built product as the theory-only ChatGPT team. Judge implementation evidence against the frozen intent. "
        "Identify only material product, experience, structural, visual, or evidence issues. Do not write code or prescribe technical fixes."
    ),
    "response_to_review": (
        "Evaluate the ChatGPT theoretical review as the Claude team. Accept, adapt, or reject each material point with evidence; "
        "make justified code revisions where accepted; rerun independent quality and browser checks; update task evidence; and return "
        "a Response to Theoretical Review. Do not deploy or merge. Final stdout must be only the JSON envelope."
    ),
}
