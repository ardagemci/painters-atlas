import json
import os
import shlex
import subprocess
import time
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Set

from .errors import ConfigurationError, ProviderError


def _provider_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Remove application-only constraints unsupported by some model grammars."""
    unsupported = {"$schema", "$id", "description", "pattern", "format", "maxLength", "minimum"}
    if isinstance(schema, dict):
        return {
            key: _provider_schema(value)
            for key, value in schema.items()
            if key not in unsupported
        }
    if isinstance(schema, list):
        return [_provider_schema(value) for value in schema]
    return schema


def _extract_json(text: str) -> Dict[str, Any]:
    candidate = text.strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        candidate = "\n".join(lines[1:-1]).strip()
    try:
        value = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise ProviderError(f"Provider did not return valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ProviderError("Provider JSON must be an object")
    return value


@dataclass
class ProviderRequest:
    system_prompt: str
    user_prompt: str
    schema: Dict[str, Any]
    metadata: Dict[str, str]


class Provider(ABC):
    name = "provider"
    capabilities: Set[str] = set()

    @abstractmethod
    def generate(self, request: ProviderRequest) -> Dict[str, Any]:
        raise NotImplementedError


class HttpProvider(Provider):
    def __init__(self, retries: int = 2, timeout: int = 300):
        self.retries = retries
        self.timeout = timeout

    def _post(self, url: str, headers: Dict[str, str], body: Dict[str, Any]) -> Dict[str, Any]:
        payload = json.dumps(body).encode("utf-8")
        last_error: Optional[Exception] = None
        for attempt in range(self.retries + 1):
            request = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")
                last_error = ProviderError(f"HTTP {exc.code} from {self.name}: {detail[:1200]}")
                if exc.code < 500 and exc.code != 429:
                    break
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                last_error = exc
            if attempt < self.retries:
                time.sleep(min(2 ** attempt, 4))
        raise ProviderError(f"{self.name} request failed: {last_error}")


class OpenAIProvider(HttpProvider):
    name = "openai-responses"
    capabilities = {"deliberation", "structured_output"}

    def __init__(self, api_key: str, model: str, base_url: str = "https://api.openai.com/v1", **kwargs: Any):
        super().__init__(**kwargs)
        if not api_key:
            raise ConfigurationError("OPENAI_API_KEY is required for the OpenAI provider")
        if not model:
            raise ConfigurationError("OPENAI_MODEL is required for the OpenAI provider")
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")

    def generate(self, request: ProviderRequest) -> Dict[str, Any]:
        body = {
            "model": self.model,
            "instructions": request.system_prompt,
            "input": request.user_prompt,
            "max_output_tokens": 12000,
            "store": False,
            "metadata": request.metadata,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "pigment_message",
                    "strict": True,
                    "schema": _provider_schema(request.schema),
                }
            },
        }
        response = self._post(
            f"{self.base_url}/responses",
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            body,
        )
        for output in response.get("output", []):
            if output.get("type") != "message":
                continue
            for content in output.get("content", []):
                if content.get("type") == "refusal":
                    raise ProviderError(f"OpenAI refused the request: {content.get('refusal', '')}")
                if content.get("type") == "output_text":
                    return _extract_json(content.get("text", ""))
        raise ProviderError("OpenAI response contained no output_text message")


class AnthropicProvider(HttpProvider):
    name = "anthropic-messages"
    capabilities = {"deliberation", "structured_output"}

    def __init__(self, api_key: str, model: str, base_url: str = "https://api.anthropic.com", **kwargs: Any):
        super().__init__(**kwargs)
        if not api_key:
            raise ConfigurationError("ANTHROPIC_API_KEY is required for the Anthropic provider")
        if not model:
            raise ConfigurationError("ANTHROPIC_MODEL is required for the Anthropic provider")
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")

    def generate(self, request: ProviderRequest) -> Dict[str, Any]:
        body = {
            "model": self.model,
            "max_tokens": 12000,
            "system": request.system_prompt,
            "messages": [{"role": "user", "content": request.user_prompt}],
            "output_config": {
                "format": {
                    "type": "json_schema",
                    "schema": _provider_schema(request.schema),
                }
            },
        }
        response = self._post(
            f"{self.base_url}/v1/messages",
            {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            body,
        )
        for content in response.get("content", []):
            if content.get("type") == "text":
                return _extract_json(content.get("text", ""))
        raise ProviderError("Anthropic response contained no text block")


class CommandProvider(Provider):
    def __init__(
        self,
        name: str,
        command: str,
        cwd: Path,
        workspace_write: bool = False,
        timeout: int = 3600,
    ):
        if not command.strip():
            raise ConfigurationError("A Claude workspace command is required")
        self.argv = shlex.split(command)
        if not self.argv:
            raise ConfigurationError("Claude workspace command is empty")
        self.cwd = cwd
        self.timeout = timeout
        self.name = name
        self.capabilities = {"deliberation", "structured_output"}
        if workspace_write:
            self.capabilities.add("workspace_write")

    def generate(self, request: ProviderRequest) -> Dict[str, Any]:
        prompt = request.system_prompt + "\n\n" + request.user_prompt
        environment = os.environ.copy()
        environment.update({f"PIGMENT_{key.upper()}": value for key, value in request.metadata.items()})
        try:
            result = subprocess.run(
                self.argv,
                cwd=str(self.cwd),
                input=prompt,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout,
                env=environment,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ProviderError(f"{self.name} could not complete: {exc}") from exc
        if result.returncode != 0:
            raise ProviderError(
                f"Claude workspace command failed ({result.returncode}): {result.stderr[-2000:]}"
            )
        parsed = _extract_json(result.stdout)
        if "result" in parsed and isinstance(parsed["result"], str):
            return _extract_json(parsed["result"])
        return parsed


class FakeProvider(Provider):
    """Deterministic provider used for tests and no-cost workflow rehearsals."""

    name = "fake"
    capabilities = {"deliberation", "structured_output", "workspace_write"}

    def generate(self, request: ProviderRequest) -> Dict[str, Any]:
        if "expected_analyst" in request.metadata:
            expected = json.loads(request.metadata["expected_analyst"])
            reviewed = json.loads(request.metadata["reviewed_message"])
            is_theory = expected["analyst_id"] == "theory-liaison"
            return {
                **expected,
                "summary": "Deterministic liaison analysis for workflow verification.",
                "semantic_validity": "valid",
                "intended_user_outcome": reviewed.get("summary", ""),
                "essential_principles": reviewed.get("accepted_points", []),
                "optional_forms": [],
                "accepted_counterpole_points": [],
                "constraints_or_principles_to_defend": [],
                "adaptations": [],
                "resolved_issues": [], "critical_issues": [], "noncritical_issues": [],
                "unsupported_claims": [], "evidence_gaps": [], "specialists_recommended": [],
                "intent_preserved": True,
                "feasibility_supported": bool(reviewed.get("evidence")),
                "quality_evidence_appears_sufficient": expected["analysis_mode"] == "build_review",
                "convergence_recommended": expected["analysis_mode"] == "convergence_review",
                "recommended_action": "advance",
                "recommended_next_state": reviewed.get("next_state", ""),
                "human_escalation": {"recommended": False, "reason_category": "", "decision_required": "", "why_the_teams_cannot_resolve_it": ""},
                "confidence": {"level": "high", "basis": "Deterministic fixture"},
                "rationale": "Exercises analyst validation, persistence, and report routing.",
                "owner_report": {
                    "visibility": "human_review" if expected["analysis_mode"] == "build_review" else "audit_only",
                    "title": "Theory Liaison Report" if is_theory else "Synthesis Liaison Report",
                    "markdown": "No owner attention required. This is an offline workflow rehearsal.",
                },
            }
        expected = json.loads(request.metadata["expected_message"])
        message_type = expected["message_type"]
        accepted = ["A coherent direction is ready for the next phase."]
        evidence = ["offline deterministic rehearsal"]
        criteria = ["The review package identifies the intended user outcome."]
        if message_type == "final_synthesis":
            accepted = [
                "user_outcome: Help a visitor understand and explore the proposed Pigment experience.",
                "information_architecture: Preserve the existing connected atlas structure.",
                "principal_flow: Enter, inspect, navigate related material, and return without losing context.",
            ]
            evidence.append("feasibility-confirmed: offline provider fixture")
        return {
            **expected,
            "summary": f"Deterministic {message_type.replace('_', ' ')} for workflow verification.",
            "assumptions": ["This is an offline rehearsal, not a product decision."],
            "accepted_points": accepted,
            "disputed_points": [],
            "proposal": f"Offline fixture for {message_type}; replace with a configured provider in live operation.",
            "rationale": "Exercises routing, validation, persistence, and gates without network calls or token cost.",
            "evidence": evidence,
            "requested_actions": ["Advance only if deterministic validation passes."],
            "acceptance_criteria": criteria,
            "risks": [],
            "confidence": "high: deterministic fixture",
        }


def providers_from_environment(repo_root: Path, fake: bool = False):
    if fake:
        provider = FakeProvider()
        return provider, provider, provider

    theory_command = os.environ.get("PIGMENT_CHATGPT_TEAM_COMMAND", "")
    if theory_command:
        theory = CommandProvider("chatgpt-team-command", theory_command, repo_root)
    else:
        theory = OpenAIProvider(
            api_key=os.environ.get("OPENAI_API_KEY", ""),
            model=os.environ.get("OPENAI_MODEL", "gpt-5.6"),
            base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        )

    team_command = os.environ.get("PIGMENT_CLAUDE_TEAM_COMMAND", "")
    build_command = os.environ.get("PIGMENT_CLAUDE_BUILD_COMMAND", "")
    if team_command:
        synthesis = CommandProvider(
            "claude-team-command",
            team_command,
            repo_root,
            workspace_write=False,
        )
    else:
        synthesis = AnthropicProvider(
            api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
            model=os.environ.get("ANTHROPIC_MODEL", "claude-fable-5"),
            base_url=os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com"),
        )

    if build_command:
        build = CommandProvider(
            "claude-build-command",
            build_command,
            repo_root,
            workspace_write=True,
        )
    else:
        build = synthesis
    return theory, synthesis, build
