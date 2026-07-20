import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .constants import (
    ARTIFACT_FILENAMES,
    MESSAGE_TYPES,
    PROJECT,
    RECIPIENTS,
    REQUIRED_MESSAGE_FIELDS,
    SENDERS,
    WORKFLOW_STATES,
)
from .errors import MessageValidationError
from .util import TASK_ID_RE, atomic_write_json, atomic_write_text


def _is_string_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def validate_message(message: Dict[str, Any], expected: Dict[str, Any] = None) -> None:
    if not isinstance(message, dict):
        raise MessageValidationError("Provider output must be a JSON object")

    missing = [field for field in REQUIRED_MESSAGE_FIELDS if field not in message]
    extra = [field for field in message if field not in REQUIRED_MESSAGE_FIELDS]
    if missing or extra:
        raise MessageValidationError(f"Message fields invalid; missing={missing}, extra={extra}")

    if not isinstance(message["task_id"], str) or not TASK_ID_RE.match(message["task_id"]):
        raise MessageValidationError("task_id must match PIG- followed by at least three digits")
    if message["project"] != PROJECT:
        raise MessageValidationError("project must be pigment")
    if not isinstance(message["round"], int) or isinstance(message["round"], bool) or message["round"] < 1:
        raise MessageValidationError("round must be a positive integer")
    if message["sender"] not in SENDERS:
        raise MessageValidationError(f"Invalid sender: {message['sender']}")
    if message["recipient"] not in RECIPIENTS:
        raise MessageValidationError(f"Invalid recipient: {message['recipient']}")
    if message["message_type"] not in MESSAGE_TYPES:
        raise MessageValidationError(f"Invalid message_type: {message['message_type']}")
    if message["workflow_state"] not in WORKFLOW_STATES or message["next_state"] not in WORKFLOW_STATES:
        raise MessageValidationError("workflow_state and next_state must use the protocol enum")

    for field in ("summary", "proposal", "rationale", "confidence", "created_at"):
        if not isinstance(message[field], str) or not message[field].strip():
            raise MessageValidationError(f"{field} must be a non-empty string")
    if len(message["summary"]) > 600:
        raise MessageValidationError("summary exceeds 600 characters")
    if not re.match(r"^(low|medium|high)( *[\u2014:-].*)?$", message["confidence"]):
        raise MessageValidationError("confidence must begin with low, medium, or high")
    try:
        datetime.fromisoformat(message["created_at"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise MessageValidationError("created_at must be ISO 8601") from exc

    for field in (
        "assumptions",
        "accepted_points",
        "disputed_points",
        "evidence",
        "requested_actions",
        "acceptance_criteria",
        "risks",
    ):
        if not _is_string_list(message[field]):
            raise MessageValidationError(f"{field} must be an array of strings")

    if expected:
        mismatches = {
            field: (expected[field], message.get(field))
            for field in expected
            if message.get(field) != expected[field]
        }
        if mismatches:
            raise MessageValidationError(f"Provider changed coordinator-owned fields: {mismatches}")


def _yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def render_artifact(message: Dict[str, Any]) -> str:
    lines: List[str] = ["---"]
    for field in REQUIRED_MESSAGE_FIELDS:
        value = message[field]
        if isinstance(value, list):
            if not value:
                lines.append(f"{field}: []")
            else:
                lines.append(f"{field}:")
                lines.extend(f"  - {_yaml_scalar(item)}" for item in value)
        elif isinstance(value, str):
            lines.append(f"{field}: {_yaml_scalar(value)}")
        else:
            lines.append(f"{field}: {value}")
    lines.extend(
        [
            "---",
            "",
            f"# {message['message_type'].replace('_', ' ').title()}",
            "",
            message["proposal"].strip(),
            "",
            "## Rationale",
            "",
            message["rationale"].strip(),
            "",
        ]
    )
    return "\n".join(lines)


def persist_message(task_dir: Path, sequence: int, message: Dict[str, Any]) -> Path:
    messages_dir = task_dir / "messages"
    messages_dir.mkdir(parents=True, exist_ok=True)
    message_path = messages_dir / f"{sequence:03d}-{message['message_type']}.json"
    atomic_write_json(message_path, message)

    artifact_name = ARTIFACT_FILENAMES[message["message_type"]]
    artifact_path = task_dir / artifact_name
    atomic_write_text(artifact_path, render_artifact(message))
    return artifact_path


def contains_severity(items: Iterable[str], severity: str) -> bool:
    pattern = re.compile(rf"^\s*(\[{severity}\]|{severity}\s*:)", re.IGNORECASE)
    return any(pattern.search(item) for item in items)
