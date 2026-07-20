import re
import shlex
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from .errors import GateError
from .messages import contains_severity


def check_convergence(final_synthesis: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    accepted = [item.lower() for item in final_synthesis["accepted_points"]]
    evidence = [item.lower() for item in final_synthesis["evidence"]]

    required_prefixes = ("user_outcome:", "information_architecture:", "principal_flow:")
    for prefix in required_prefixes:
        if not any(item.startswith(prefix) and item[len(prefix):].strip() for item in accepted):
            failures.append(f"accepted_points requires a non-empty '{prefix}' entry")
    if not final_synthesis["acceptance_criteria"]:
        failures.append("at least one testable acceptance criterion is required")
    if not any("feasibility-confirmed" in item for item in evidence):
        failures.append("evidence must include a feasibility-confirmed marker")
    if contains_severity(final_synthesis["disputed_points"], "critical"):
        failures.append("critical disputed points remain")
    if contains_severity(final_synthesis["risks"], "critical"):
        failures.append("critical risks remain")
    return failures


def check_quality_gate(repo_root: Path, task_dir: Path, validator_command: str = "") -> List[str]:
    failures: List[str] = []
    for required in ("specification.md", "decision-record.md", "build-evidence-report.md"):
        if not (task_dir / required).exists():
            failures.append(f"{required} is missing")
    review = task_dir / "quality-review.md"
    if not review.exists():
        failures.append("quality-review.md is missing")
    else:
        text = review.read_text(encoding="utf-8")
        requirements = (
            (r"GATE\s*2\s*:\s*CERTIFIED", "quality review must contain 'GATE 2: CERTIFIED'"),
            (r"OPEN\s+CRITICAL\s*:\s*0", "quality review must contain 'OPEN CRITICAL: 0'"),
            (r"OPEN\s+MAJOR\s*:\s*0", "quality review must contain 'OPEN MAJOR: 0'"),
        )
        for pattern, failure in requirements:
            if not re.search(pattern, text, re.IGNORECASE):
                failures.append(failure)

    evidence_dir = task_dir / "evidence"
    screenshots = list(evidence_dir.glob("*.png")) if evidence_dir.exists() else []
    for path in screenshots:
        if path.stat().st_size == 0:
            failures.append(f"browser evidence is empty: {path.name}")
    names = [path.name.lower() for path in screenshots]
    for viewport, theme in (("desktop", "dark"), ("desktop", "light"), ("mobile", "dark"), ("mobile", "light")):
        if not any(viewport in name and theme in name for name in names):
            failures.append(f"browser evidence is missing a {viewport}/{theme} screenshot")

    if validator_command:
        output_path = task_dir / "evidence" / "coordinator-validator.txt"
        try:
            result = subprocess.run(
                shlex.split(validator_command),
                cwd=str(repo_root),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=180,
            )
            output_path.write_text(result.stdout, encoding="utf-8")
            if result.returncode != 0:
                failures.append(f"repository validator failed with exit code {result.returncode}")
        except (OSError, subprocess.TimeoutExpired) as exc:
            output_path.write_text(str(exc) + "\n", encoding="utf-8")
            failures.append(f"repository validator could not complete: {exc}")
    return failures


def require_gate(name: str, failures: List[str]) -> None:
    if failures:
        raise GateError(f"{name} blocked: " + "; ".join(failures))
