from pathlib import Path
from typing import Any, Dict

from .errors import ConfigurationError
from .util import TASK_ID_RE, atomic_write_json, read_json, utc_now


class TaskStore:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()
        self.tasks_root = self.repo_root / "protocol" / "tasks"

    def task_dir(self, task_id: str) -> Path:
        if not TASK_ID_RE.match(task_id):
            raise ConfigurationError("task_id must match PIG- followed by at least three digits")
        return self.tasks_root / task_id

    def create(self, task_id: str, objective: str, max_rounds: int, max_provider_calls: int) -> Dict[str, Any]:
        task_dir = self.task_dir(task_id)
        state_path = task_dir / "state.json"
        if state_path.exists():
            raise ConfigurationError(f"Task already exists: {task_id}")
        if not objective.strip():
            raise ConfigurationError("objective cannot be empty")
        if max_rounds < 1 or max_provider_calls < 1:
            raise ConfigurationError("round and provider-call budgets must be positive")

        now = utc_now()
        state = {
            "version": 1,
            "task_id": task_id,
            "project": "pigment",
            "objective": objective.strip(),
            "workflow_state": "intake",
            "round": 1,
            "max_rounds": max_rounds,
            "provider_calls": 0,
            "max_provider_calls": max_provider_calls,
            "message_count": 0,
            "analyst_count": 0,
            "last_message_type": None,
            "build_authorized": False,
            "human_decision": None,
            "created_at": now,
            "updated_at": now,
            "events": [],
        }
        self.record_event(state, "task_created", {"objective": objective.strip()})
        task_dir.mkdir(parents=True, exist_ok=False)
        (task_dir / "evidence").mkdir()
        (task_dir / "messages").mkdir()
        (task_dir / "analyses").mkdir()
        (task_dir / "analyst-reports").mkdir()
        self.save(state)
        return state

    def load(self, task_id: str) -> Dict[str, Any]:
        path = self.task_dir(task_id) / "state.json"
        if not path.exists():
            raise ConfigurationError(f"Unknown task: {task_id}")
        return read_json(path)

    def save(self, state: Dict[str, Any]) -> None:
        state["updated_at"] = utc_now()
        atomic_write_json(self.task_dir(state["task_id"]) / "state.json", state)

    def record_event(self, state: Dict[str, Any], event_type: str, detail: Dict[str, Any]) -> None:
        state["events"].append(
            {
                "sequence": len(state["events"]) + 1,
                "type": event_type,
                "at": utc_now(),
                "detail": detail,
            }
        )
