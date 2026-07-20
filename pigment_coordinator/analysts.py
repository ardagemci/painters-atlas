import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from .errors import MessageValidationError
from .util import TASK_ID_RE, atomic_write_json, atomic_write_text


REQUIRED_FIELDS = (
    "task_id", "project", "round", "analyst_id", "pole", "analysis_mode",
    "artifact_reviewed", "summary", "semantic_validity", "intended_user_outcome",
    "essential_principles", "optional_forms", "accepted_counterpole_points",
    "constraints_or_principles_to_defend", "adaptations", "resolved_issues",
    "critical_issues", "noncritical_issues", "unsupported_claims", "evidence_gaps",
    "specialists_recommended", "intent_preserved", "feasibility_supported",
    "quality_evidence_appears_sufficient", "convergence_recommended",
    "recommended_action", "recommended_next_state", "human_escalation",
    "confidence", "rationale", "owner_report", "created_at",
)


def validate_analyst_packet(packet: Dict[str, Any], expected: Dict[str, Any] = None) -> None:
    if not isinstance(packet, dict):
        raise MessageValidationError("Analyst output must be a JSON object")
    missing = [field for field in REQUIRED_FIELDS if field not in packet]
    extra = [field for field in packet if field not in REQUIRED_FIELDS]
    if missing or extra:
        raise MessageValidationError(f"Analyst fields invalid; missing={missing}, extra={extra}")
    if not isinstance(packet["task_id"], str) or not TASK_ID_RE.match(packet["task_id"]):
        raise MessageValidationError("Invalid analyst task_id")
    if packet["project"] != "pigment":
        raise MessageValidationError("Analyst project must be pigment")
    if packet["analyst_id"] not in ("theory-liaison", "synthesis-liaison"):
        raise MessageValidationError("Invalid analyst_id")
    if packet["pole"] not in ("chatgpt-theory", "claude-synthesis-build"):
        raise MessageValidationError("Invalid analyst pole")
    if packet["analysis_mode"] not in ("incoming", "outgoing", "build_review", "convergence_review"):
        raise MessageValidationError("Invalid analysis_mode")
    if packet["semantic_validity"] not in ("valid", "repairable", "invalid"):
        raise MessageValidationError("Invalid semantic_validity")
    for field in ("artifact_reviewed", "essential_principles", "optional_forms", "accepted_counterpole_points", "constraints_or_principles_to_defend", "resolved_issues", "critical_issues", "noncritical_issues", "unsupported_claims", "evidence_gaps", "specialists_recommended"):
        if not isinstance(packet[field], list) or not all(isinstance(item, str) for item in packet[field]):
            raise MessageValidationError(f"{field} must be an array of strings")
    for field in ("intent_preserved", "feasibility_supported", "quality_evidence_appears_sufficient", "convergence_recommended"):
        if not isinstance(packet[field], bool):
            raise MessageValidationError(f"{field} must be boolean")
    report = packet["owner_report"]
    if not isinstance(report, dict) or set(report) != {"visibility", "title", "markdown"}:
        raise MessageValidationError("Invalid owner_report")
    if report["visibility"] not in ("audit_only", "human_review", "escalation"):
        raise MessageValidationError("Invalid owner_report visibility")
    if report["visibility"] == "escalation" and not packet["human_escalation"].get("recommended"):
        raise MessageValidationError("Escalation report requires a recommended human escalation")
    try:
        datetime.fromisoformat(packet["created_at"].replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise MessageValidationError("Analyst created_at must be ISO 8601") from exc
    if expected:
        mismatches = {key: (value, packet.get(key)) for key, value in expected.items() if packet.get(key) != value}
        if mismatches:
            raise MessageValidationError(f"Analyst changed coordinator-owned fields: {mismatches}")


def persist_analyst_packet(task_dir: Path, sequence: int, packet: Dict[str, Any]) -> Path:
    analyses = task_dir / "analyses"
    reports = task_dir / "analyst-reports"
    analyses.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)
    stem = f"{sequence:03d}-{packet['analyst_id']}"
    path = analyses / f"{stem}.json"
    atomic_write_json(path, packet)
    atomic_write_text(reports / f"{stem}.md", f"# {packet['owner_report']['title']}\n\n{packet['owner_report']['markdown'].strip()}\n")
    return path
