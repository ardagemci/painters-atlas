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


_REVISION_HEADING = re.compile(r"^#\s+Quality Review\b", re.MULTILINE)
_VERDICT_HEADING = re.compile(r"^#{1,6}\s*\d*\.?\s*Gate\s*2\s*verdict\b", re.MULTILINE | re.IGNORECASE)
# A verdict is a token standing on its own line, optionally wrapped in markdown
# emphasis. It is NOT a word occurring mid-sentence.
_CERTIFIED_LINE = re.compile(r"^\s*[*_`]{0,2}\s*(?:GATE\s*2\s*:\s*)?CERTIFIED\b", re.MULTILINE | re.IGNORECASE)
_BLOCKED_LINE = re.compile(r"^\s*[*_`]{0,2}\s*(?:GATE\s*2\s*:\s*)?BLOCKED\b", re.MULTILINE | re.IGNORECASE)


def check_quality_review_text(text: str) -> List[str]:
    """Read the ONE operative verdict out of an append-only quality review.

    This function exists because the previous implementation did not work, and
    failed in the most dangerous direction: it passed reviews it should have
    blocked. It searched the whole document for the strings "GATE 2: CERTIFIED",
    "OPEN CRITICAL: 0" and "OPEN MAJOR: 0", which meant two things.

    First, `quality-review.md` is append-only. Once revision 1 was certified,
    every later revision inherited that CERTIFIED regardless of its own verdict,
    so a review whose current revision read BLOCKED still satisfied the gate.

    Second, it matched prose. A sentence *describing* the defect — "the gate
    passes a report whose verdict is BLOCKED because a sentence contains GATE 2:
    CERTIFIED" — satisfied the check that the sentence was complaining about.
    That is not a hypothetical; it is how the defect was found.

    The fix is to stop grepping and start locating:

      * the operative revision is the text after the LAST `# Quality Review`
        heading (an appended revision repeats it; a single-revision file has one);
      * inside it, the operative verdict is the LAST `Gate 2 verdict` section;
      * the verdict must stand at the start of a line, so prose about a verdict
        is not a verdict;
      * BLOCKED anywhere in that section fails, even if CERTIFIED is also there —
        a section naming both is ambiguous, and ambiguity is not certification.
    """
    failures: List[str] = []

    heads = list(_REVISION_HEADING.finditer(text))
    operative = text[heads[-1].start():] if heads else text

    verdict_heads = list(_VERDICT_HEADING.finditer(operative))
    if not verdict_heads:
        failures.append("quality review has no 'Gate 2 verdict' section")
        return failures
    verdict_block = operative[verdict_heads[-1].end():]

    blocked = bool(_BLOCKED_LINE.search(verdict_block))
    certified = bool(_CERTIFIED_LINE.search(verdict_block))
    if blocked:
        failures.append("quality review's operative Gate 2 verdict is BLOCKED")
    elif not certified:
        failures.append("quality review's operative Gate 2 verdict is not CERTIFIED")

    # Finding counts are read from the operative revision, not the whole file.
    for pattern, label in ((r"^\s*[*_`]{0,2}\s*OPEN\s+CRITICAL\s*:\s*0\b", "OPEN CRITICAL: 0"),
                           (r"^\s*[*_`]{0,2}\s*OPEN\s+MAJOR\s*:\s*0\b", "OPEN MAJOR: 0")):
        if not re.search(pattern, operative, re.MULTILINE | re.IGNORECASE):
            failures.append(f"operative quality review must state '{label}'")
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
        failures.extend(check_quality_review_text(review.read_text(encoding="utf-8")))

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
