import json
from pathlib import Path
from typing import Any, Dict, Tuple

from .analysts import persist_analyst_packet, validate_analyst_packet
from .errors import ConfigurationError, GateError, TransitionError
from .gates import check_convergence, check_quality_gate, require_gate
from .messages import persist_message, validate_message
from .prompts import PHASE_INSTRUCTIONS, analyst_prompt, load_analyst_prompt, load_system_prompt, provider_prompt
from .providers import Provider, ProviderRequest
from .store import TaskStore
from .util import atomic_write_text, digest, read_json, utc_now


class Coordinator:
    def __init__(
        self,
        repo_root: Path,
        theory_provider: Provider,
        synthesis_provider: Provider,
        build_provider: Provider,
        validator_command: str = "",
    ):
        self.repo_root = repo_root.resolve()
        self.store = TaskStore(self.repo_root)
        self.theory_provider = theory_provider
        self.synthesis_provider = synthesis_provider
        self.build_provider = build_provider
        self.validator_command = validator_command
        self.schema = read_json(self.repo_root / "protocol" / "message-schema.json")
        self.analyst_schema = read_json(self.repo_root / "protocol" / "analyst-packet-schema.json")

    def create_task(self, task_id: str, objective: str, max_rounds: int = 3, max_provider_calls: int = 20):
        return self.store.create(task_id, objective, max_rounds, max_provider_calls)

    def status(self, task_id: str) -> Dict[str, Any]:
        return self.store.load(task_id)

    def _expected(self, state: Dict[str, Any], message_type: str, sender: str, recipient: str, current: str, next_state: str, round_number: int) -> Dict[str, Any]:
        return {
            "task_id": state["task_id"],
            "project": "pigment",
            "round": round_number,
            "sender": sender,
            "recipient": recipient,
            "message_type": message_type,
            "workflow_state": current,
            "next_state": next_state,
            "created_at": utc_now(),
        }

    def _call(
        self,
        state: Dict[str, Any],
        provider: Provider,
        pole: str,
        expected: Dict[str, Any],
        instruction_key: str,
        allowed_types: Tuple[str, ...] = (),
    ) -> Dict[str, Any]:
        if state["provider_calls"] >= state["max_provider_calls"]:
            raise GateError("Provider-call budget exhausted")
        if expected["round"] > state["max_rounds"]:
            raise GateError("Deliberation round budget exhausted")

        prompt = provider_prompt(
            self.repo_root,
            state,
            expected,
            PHASE_INSTRUCTIONS[instruction_key],
        )
        request = ProviderRequest(
            system_prompt=load_system_prompt(self.repo_root, pole),
            user_prompt=prompt,
            schema=self.schema,
            metadata={
                "task_id": state["task_id"],
                "phase": instruction_key,
                "expected_message": json.dumps(expected),
            },
        )
        state["provider_calls"] += 1
        self.store.record_event(
            state,
            "provider_call_started",
            {"provider": provider.name, "phase": instruction_key},
        )
        self.store.save(state)
        message = provider.generate(request)
        if allowed_types and message.get("message_type") in allowed_types:
            expected = {**expected, "message_type": message["message_type"]}
        validate_message(message, expected)
        self._call_analyst(state, provider, pole, message)

        state["message_count"] += 1
        state["last_message_type"] = message["message_type"]
        state["round"] = message["round"]
        state["workflow_state"] = message["next_state"]
        artifact = persist_message(self.store.task_dir(state["task_id"]), state["message_count"], message)
        self._refresh_decision_record(state["task_id"])
        self.store.record_event(
            state,
            "message_routed",
            {
                "provider": provider.name,
                "message_type": message["message_type"],
                "artifact": str(artifact.relative_to(self.repo_root)),
            },
        )
        self.store.save(state)
        return state

    def _call_analyst(self, state: Dict[str, Any], provider: Provider, pole: str, message: Dict[str, Any]) -> None:
        if state["provider_calls"] >= state["max_provider_calls"]:
            raise GateError("Provider-call budget exhausted before liaison analysis")
        analyst_id = "theory-liaison" if pole == "chatgpt" else "synthesis-liaison"
        analyst_pole = "chatgpt-theory" if pole == "chatgpt" else "claude-synthesis-build"
        mode = "build_review" if message["message_type"] in ("implementation_report", "review", "response_to_review") else "outgoing"
        if message["message_type"] == "final_synthesis":
            mode = "convergence_review"
        expected = {
            "task_id": state["task_id"], "project": "pigment", "round": message["round"],
            "analyst_id": analyst_id, "pole": analyst_pole, "analysis_mode": mode,
            "artifact_reviewed": [message["message_type"]], "created_at": utc_now(),
        }
        request = ProviderRequest(
            system_prompt=load_analyst_prompt(self.repo_root, analyst_id),
            user_prompt=analyst_prompt(self.repo_root, state, expected, message),
            schema=self.analyst_schema,
            metadata={
                "task_id": state["task_id"], "phase": f"{analyst_id}:{mode}",
                "expected_analyst": json.dumps(expected),
                "reviewed_message": json.dumps(message),
            },
        )
        state["provider_calls"] += 1
        packet = provider.generate(request)
        validate_analyst_packet(packet, expected)
        state["analyst_count"] = state.get("analyst_count", 0) + 1
        artifact = persist_analyst_packet(self.store.task_dir(state["task_id"]), state["analyst_count"], packet)
        self.store.record_event(state, "analyst_packet_routed", {
            "analyst_id": analyst_id, "visibility": packet["owner_report"]["visibility"],
            "artifact": str(artifact.relative_to(self.repo_root)),
        })
        self.store.save(state)

    def _refresh_decision_record(self, task_id: str) -> None:
        task_dir = self.store.task_dir(task_id)
        messages = [read_json(path) for path in sorted((task_dir / "messages").glob("*.json"))]
        lines = [f"# Decision Record - {task_id}", "", "Generated from validated Coordinator messages. Do not remove disputed history.", ""]
        for message in messages:
            lines.extend(
                [
                    f"## {message['round']}: {message['message_type']}",
                    "",
                    f"**Summary:** {message['summary']}",
                    "",
                    "**Accepted points:**",
                ]
            )
            lines.extend(f"- {item}" for item in message["accepted_points"] or ["None recorded."])
            lines.extend(["", "**Disputed points:**"])
            lines.extend(f"- {item}" for item in message["disputed_points"] or ["None recorded."])
            lines.extend(["", f"**Rationale:** {message['rationale']}", "", "**Evidence:"])
            lines.extend(f"- {item}" for item in message["evidence"] or ["None recorded."])
            lines.extend(["", f"**Disposition:** `{message['workflow_state']}` -> `{message['next_state']}`", ""])
        atomic_write_text(task_dir / "decision-record.md", "\n".join(lines))

    def advance(self, task_id: str) -> Dict[str, Any]:
        state = self.store.load(task_id)
        current = state["workflow_state"]

        if current == "intake":
            expected = self._expected(state, "theory_brief", "chatgpt-theory", "coordinator", "theory", "challenge", 1)
            return self._call(state, self.theory_provider, "chatgpt", expected, "theory_brief")

        if current == "challenge":
            expected = self._expected(state, "challenge", "claude-synthesis-lead", "coordinator", "challenge", "theory_revision", state["round"])
            return self._call(state, self.synthesis_provider, "claude", expected, "challenge")

        if current == "theory_revision":
            expected = self._expected(state, "revision", "chatgpt-theory", "coordinator", "theory_revision", "final_synthesis", state["round"] + 1)
            return self._call(
                state,
                self.theory_provider,
                "chatgpt",
                expected,
                "revision_or_defense",
                allowed_types=("revision", "defense"),
            )

        if current == "final_synthesis":
            expected = self._expected(state, "final_synthesis", "claude-synthesis-lead", "coordinator", "final_synthesis", "awaiting_build_approval", state["round"])
            return self._call(state, self.synthesis_provider, "claude", expected, "final_synthesis")

        if current == "awaiting_build_approval":
            return self.freeze_specification(task_id)

        if current == "approved_for_build":
            if "workspace_write" not in self.build_provider.capabilities:
                raise ConfigurationError(
                    "Build is authorized, but the configured Claude provider is text-only. "
                    "Set PIGMENT_CLAUDE_BUILD_COMMAND to a workspace-capable Claude Code command."
                )
            state["workflow_state"] = "building"
            self.store.record_event(state, "build_started", {"provider": self.build_provider.name})
            self.store.save(state)
            expected = self._expected(state, "implementation_report", "claude-synthesis-lead", "coordinator", "building", "internal_review", state["round"])
            return self._call(state, self.build_provider, "claude", expected, "implementation_report")

        if current == "internal_review" and state["last_message_type"] == "implementation_report":
            expected = self._expected(state, "review", "chatgpt-theory", "coordinator", "internal_review", "revision", state["round"] + 1)
            return self._call(state, self.theory_provider, "chatgpt", expected, "review")

        if current == "revision":
            if "workspace_write" not in self.build_provider.capabilities:
                raise ConfigurationError("Claude review response requires a workspace-capable build provider")
            expected = self._expected(state, "response_to_review", "claude-synthesis-lead", "coordinator", "revision", "internal_review", state["round"])
            return self._call(state, self.build_provider, "claude", expected, "response_to_review")

        if current == "internal_review" and state["last_message_type"] == "response_to_review":
            return self.prepare_human_review(task_id)

        if current in ("human_review_ready", "approved", "rejected", "blocked"):
            raise TransitionError(f"Task is paused in terminal or human-controlled state: {current}")
        raise TransitionError(f"No deterministic transition is defined from {current}")

    def freeze_specification(self, task_id: str) -> Dict[str, Any]:
        state = self.store.load(task_id)
        if state["workflow_state"] != "awaiting_build_approval":
            raise TransitionError("Specification can only freeze from awaiting_build_approval")
        message_path = self.store.task_dir(task_id) / "messages" / f"{state['message_count']:03d}-final_synthesis.json"
        final = read_json(message_path)
        require_gate("Convergence", check_convergence(final))

        expected = self._expected(
            state,
            "specification",
            "coordinator",
            "claude-synthesis-lead",
            "approved_for_build",
            "approved_for_build",
            state["round"],
        )
        specification = {
            **expected,
            "summary": "The converged synthesis is frozen and authorized for isolated implementation.",
            "assumptions": final["assumptions"],
            "accepted_points": final["accepted_points"],
            "disputed_points": final["disputed_points"],
            "proposal": final["proposal"],
            "rationale": final["rationale"],
            "evidence": final["evidence"] + [f"frozen-sha256:{digest(final)}"],
            "requested_actions": ["Build on an isolated branch or worktree; do not merge or deploy."],
            "acceptance_criteria": final["acceptance_criteria"],
            "risks": final["risks"],
            "confidence": final["confidence"],
        }
        validate_message(specification, expected)
        state["message_count"] += 1
        state["last_message_type"] = "specification"
        state["workflow_state"] = "approved_for_build"
        state["build_authorized"] = True
        artifact = persist_message(self.store.task_dir(task_id), state["message_count"], specification)
        self._refresh_decision_record(task_id)
        self.store.record_event(state, "specification_frozen", {"artifact": str(artifact.relative_to(self.repo_root))})
        self.store.save(state)
        return state

    def prepare_human_review(self, task_id: str) -> Dict[str, Any]:
        state = self.store.load(task_id)
        if state["workflow_state"] != "internal_review" or state["last_message_type"] != "response_to_review":
            raise TransitionError("Human review can only be prepared after Claude's response to theoretical review")
        task_dir = self.store.task_dir(task_id)
        require_gate("Quality", check_quality_gate(self.repo_root, task_dir, self.validator_command))

        messages = [read_json(path) for path in sorted((task_dir / "messages").glob("*.json"))]
        by_type = {message["message_type"]: message for message in messages}
        final = by_type["final_synthesis"]
        build = by_type["implementation_report"]
        review = by_type["review"]
        response = by_type["response_to_review"]

        visible_reports = []
        for path in sorted((task_dir / "analyses").glob("*.json")):
            packet = read_json(path)
            if packet["owner_report"]["visibility"] in ("human_review", "escalation"):
                visible_reports.append(f"### {packet['owner_report']['title']}\n{packet['owner_report']['markdown']}")
        analyst_section = "\n\n".join(visible_reports) if visible_reports else "No liaison report requires owner attention."

        def prefixed(prefix: str, fallback: str) -> str:
            for item in final["accepted_points"]:
                if item.lower().startswith(prefix.lower()):
                    return item.split(":", 1)[1].strip()
            return fallback

        def bullets(items, fallback: str) -> str:
            return "\n".join(f"- {item}" for item in items) if items else fallback

        expected = self._expected(
            state,
            "human_review_package",
            "coordinator",
            "user",
            "human_review_ready",
            "human_review_ready",
            state["round"],
        )
        proposal = (
            f"## Recommended Direction\n{final['proposal']}\n\n"
            f"## Intended User Outcome\n{prefixed('user_outcome:', 'See the frozen specification.')}\n\n"
            f"## Final Product Rationale\n{final['rationale']}\n\n"
            f"## What Claude Changed and Why\n{build['rationale']}\n\n"
            f"## Important Alternatives Rejected\n{bullets(final['disputed_points'], 'None recorded.')}\n\n"
            f"## Website Structure and User Flow\n"
            f"{prefixed('information_architecture:', 'See the frozen specification.')} "
            f"{prefixed('principal_flow:', '')}\n\n"
            f"## Visual and Interaction Direction\n"
            f"{prefixed('visual_direction:', 'See the frozen specification and implementation evidence.')}\n\n"
            f"## Working Preview and Product Evidence\n{build['summary']}\n"
            "See build-evidence-report.md and evidence/.\n\n"
            "## Test and Accessibility Results\n"
            "Gate 2 is certified. See quality-review.md and evidence/coordinator-validator.txt.\n\n"
            f"## Theoretical Review\n{review['summary']}\n\n"
            f"## Claude Response\n{response['summary']} {response['rationale']}\n\n"
            f"## Liaison Reports\n{analyst_section}\n\n"
            f"## Remaining Risks\n{bullets(response['risks'], 'None recorded.')}\n\n"
            f"## Decisions Requiring the User\n"
            f"{bullets(response['disputed_points'], 'Approve or reject the reviewed product.')}"
        )
        package = {
            **expected,
            "summary": "Pigment's internally reviewed implementation is ready for the product owner's decision.",
            "assumptions": final["assumptions"],
            "accepted_points": final["accepted_points"],
            "disputed_points": response["disputed_points"],
            "proposal": proposal,
            "rationale": response["rationale"],
            "evidence": sorted(set(build["evidence"] + response["evidence"] + ["quality-review.md", "evidence/"])),
            "requested_actions": ["Review the preview and approve or reject the product. Production deployment remains locked."],
            "acceptance_criteria": final["acceptance_criteria"],
            "risks": response["risks"],
            "confidence": response["confidence"],
        }
        validate_message(package, expected)
        state["message_count"] += 1
        state["last_message_type"] = "human_review_package"
        state["workflow_state"] = "human_review_ready"
        artifact = persist_message(task_dir, state["message_count"], package)
        self._refresh_decision_record(task_id)
        self.store.record_event(state, "human_review_prepared", {"artifact": str(artifact.relative_to(self.repo_root))})
        self.store.save(state)
        return state

    def decide(self, task_id: str, decision: str, note: str = "") -> Dict[str, Any]:
        state = self.store.load(task_id)
        if state["workflow_state"] != "human_review_ready":
            raise TransitionError("The user may decide only from human_review_ready")
        if decision not in ("approved", "rejected"):
            raise ConfigurationError("decision must be approved or rejected")
        state["workflow_state"] = decision
        state["human_decision"] = {"decision": decision, "note": note.strip(), "at": utc_now()}
        self.store.record_event(state, "human_decision", state["human_decision"])
        self.store.save(state)
        return state

    def run_until_pause(self, task_id: str, max_steps: int = 20) -> Dict[str, Any]:
        for _ in range(max_steps):
            state = self.store.load(task_id)
            if state["workflow_state"] in ("human_review_ready", "approved", "rejected", "blocked"):
                return state
            if state["workflow_state"] == "approved_for_build" and "workspace_write" not in self.build_provider.capabilities:
                return state
            self.advance(task_id)
        raise GateError(f"Run exceeded {max_steps} coordinator steps")
