import json
import tempfile
import unittest
from pathlib import Path

from pigment_coordinator.engine import Coordinator
from pigment_coordinator.analysts import validate_analyst_packet
from pigment_coordinator.errors import ConfigurationError, GateError, MessageValidationError, TransitionError
from pigment_coordinator.gates import check_convergence
from pigment_coordinator.messages import validate_message
from pigment_coordinator.providers import AnthropicProvider, FakeProvider, OpenAIProvider, ProviderRequest


ROOT = Path(__file__).resolve().parents[1]


class TextOnlyFake(FakeProvider):
    capabilities = {"deliberation", "structured_output"}


class CoordinatorTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        (self.repo / "protocol" / "tasks").mkdir(parents=True)
        (self.repo / "protocol" / "message-schema.json").write_text(
            (ROOT / "protocol" / "message-schema.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (self.repo / "protocol" / "analyst-packet-schema.json").write_text(
            (ROOT / "protocol" / "analyst-packet-schema.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (self.repo / "coordinator" / "prompts").mkdir(parents=True)
        for name in ("chatgpt-theory.md", "claude-synthesis.md", "theory-liaison.md", "synthesis-liaison.md"):
            (self.repo / "coordinator" / "prompts" / name).write_text(
                (ROOT / "coordinator" / "prompts" / name).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        fake = FakeProvider()
        self.coordinator = Coordinator(self.repo, fake, fake, fake, validator_command="")

    def tearDown(self):
        self.temporary.cleanup()

    def create(self, task_id="PIG-901"):
        return self.coordinator.create_task(task_id, "Exercise the coordinator safely")

    def advance_to_build_authorized(self, task_id="PIG-901"):
        self.create(task_id)
        for _ in range(5):
            self.coordinator.advance(task_id)
        state = self.coordinator.status(task_id)
        self.assertEqual(state["workflow_state"], "approved_for_build")
        self.assertTrue(state["build_authorized"])
        return state

    def test_complete_offline_cycle_requires_quality_evidence(self):
        task_id = "PIG-901"
        self.advance_to_build_authorized(task_id)

        self.coordinator.advance(task_id)  # build
        self.coordinator.advance(task_id)  # theory review
        self.coordinator.advance(task_id)  # Claude response and revision
        with self.assertRaises(GateError):
            self.coordinator.advance(task_id)

        task_dir = self.repo / "protocol" / "tasks" / task_id
        (task_dir / "quality-review.md").write_text(
            "GATE 2: CERTIFIED\nOPEN CRITICAL: 0\nOPEN MAJOR: 0\n",
            encoding="utf-8",
        )
        for name in (
            "home__desktop__dark.png",
            "home__desktop__light.png",
            "home__mobile__dark.png",
            "home__mobile__light.png",
        ):
            (task_dir / "evidence" / name).write_bytes(b"offline-test")

        state = self.coordinator.advance(task_id)
        self.assertEqual(state["workflow_state"], "human_review_ready")
        package_path = task_dir / "human-review-package.md"
        self.assertTrue(package_path.exists())
        package = package_path.read_text(encoding="utf-8")
        self.assertIn("## Recommended Direction", package)
        self.assertIn("## Test and Accessibility Results", package)
        self.assertIn("## Decisions Requiring the User", package)
        self.assertIn("## Liaison Reports", package)
        self.assertEqual(len(list((task_dir / "analyses").glob("*.json"))), 7)
        self.assertEqual(len(list((task_dir / "analyst-reports").glob("*.md"))), 7)

        state = self.coordinator.decide(task_id, "approved", "Offline state-machine verification")
        self.assertEqual(state["workflow_state"], "approved")
        with self.assertRaises(TransitionError):
            self.coordinator.advance(task_id)

    def test_text_only_claude_cannot_claim_a_build(self):
        task_id = "PIG-902"
        self.advance_to_build_authorized(task_id)
        fake = FakeProvider()
        coordinator = Coordinator(self.repo, fake, fake, TextOnlyFake(), validator_command="")
        with self.assertRaises(ConfigurationError):
            coordinator.advance(task_id)

    def test_convergence_rejects_critical_risk_and_missing_markers(self):
        message = self.valid_message()
        message["accepted_points"] = []
        message["evidence"] = []
        message["risks"] = ["[critical] Unknown legal status"]
        failures = check_convergence(message)
        self.assertGreaterEqual(len(failures), 5)

    def test_message_validation_rejects_coordinator_field_changes(self):
        message = self.valid_message()
        with self.assertRaises(MessageValidationError):
            validate_message(message, {"task_id": "PIG-999"})
        message["unexpected"] = True
        with self.assertRaises(MessageValidationError):
            validate_message(message)

    def test_analyst_packet_validation_and_escalation_visibility(self):
        packet = self.valid_analyst_packet()
        validate_analyst_packet(packet, {"analyst_id": "theory-liaison"})
        packet["owner_report"]["visibility"] = "escalation"
        with self.assertRaises(MessageValidationError):
            validate_analyst_packet(packet)

    def test_openai_adapter_uses_responses_structured_output(self):
        provider = OpenAIProvider("test-key", "test-model")
        captured = {}

        def fake_post(url, headers, body):
            captured.update({"url": url, "headers": headers, "body": body})
            return {
                "output": [
                    {
                        "type": "message",
                        "content": [{"type": "output_text", "text": json.dumps(self.valid_message())}],
                    }
                ]
            }

        provider._post = fake_post
        result = provider.generate(self.provider_request())
        self.assertEqual(result["task_id"], "PIG-901")
        self.assertTrue(captured["url"].endswith("/v1/responses"))
        self.assertEqual(captured["body"]["text"]["format"]["type"], "json_schema")
        self.assertTrue(captured["body"]["text"]["format"]["strict"])
        self.assertFalse(captured["body"]["store"])

    def test_anthropic_adapter_uses_messages_structured_output(self):
        provider = AnthropicProvider("test-key", "test-model")
        captured = {}

        def fake_post(url, headers, body):
            captured.update({"url": url, "headers": headers, "body": body})
            return {"content": [{"type": "text", "text": json.dumps(self.valid_message())}]}

        provider._post = fake_post
        result = provider.generate(self.provider_request())
        self.assertEqual(result["task_id"], "PIG-901")
        self.assertTrue(captured["url"].endswith("/v1/messages"))
        self.assertEqual(captured["headers"]["anthropic-version"], "2023-06-01")
        self.assertEqual(captured["body"]["output_config"]["format"]["type"], "json_schema")
        self.assertEqual(captured["body"]["system"], "system")

    def adopt_fixture(self, task_id):
        task_dir = self.repo / "protocol" / "tasks" / task_id
        (task_dir / "evidence").mkdir(parents=True)
        (task_dir / "evidence" / "home__mobile__dark.png").write_bytes(b"png")
        (task_dir / "round1-report.md").write_text("manual round record", encoding="utf-8")
        (task_dir / "decision-record.md").write_text("## D-001 manual", encoding="utf-8")
        return task_dir

    def write_json(self, name, value):
        path = self.repo / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def deliberation_message(self, task_id, **overrides):
        message = self.valid_message()
        message["task_id"] = task_id
        message.update(overrides)
        return message

    def analyst_fixture(self, task_id, analyst_id, pole, mode="outgoing", round_number=1):
        packet = self.valid_analyst_packet()
        packet.update(
            {"task_id": task_id, "analyst_id": analyst_id, "pole": pole, "analysis_mode": mode, "round": round_number}
        )
        return packet

    def test_adopt_registers_intake_and_preserves_unrouted(self):
        task_id = "PIG-903"
        task_dir = self.adopt_fixture(task_id)
        state = self.coordinator.adopt_task(task_id, "Recover the manual round", "deadbeef")
        self.assertEqual(state["workflow_state"], "intake")
        self.assertEqual(state["adopted"]["baseline"], "deadbeef")
        self.assertEqual(state["adopted"]["preserved_unrouted"], ["decision-record.md", "round1-report.md"])
        self.assertTrue((task_dir / "unrouted" / "round1-report.md").exists())
        self.assertTrue((task_dir / "unrouted" / "decision-record.md").exists())
        self.assertFalse((task_dir / "round1-report.md").exists())
        self.assertTrue((task_dir / "evidence" / "home__mobile__dark.png").exists())
        with self.assertRaises(ConfigurationError):
            self.coordinator.adopt_task(task_id, "again", "deadbeef")
        with self.assertRaises(ConfigurationError):
            self.coordinator.create_task(task_id, "again")

    def test_adopt_requires_existing_artifacts(self):
        with self.assertRaises(ConfigurationError):
            self.coordinator.adopt_task("PIG-904", "Nothing to recover", "deadbeef")

    def test_ingest_routes_deliberation_messages(self):
        task_id = "PIG-905"
        task_dir = self.adopt_fixture(task_id)
        self.coordinator.adopt_task(task_id, "Recover and replay", "deadbeef")

        brief = self.deliberation_message(
            task_id,
            message_type="theory_brief",
            sender="chatgpt-theory",
            workflow_state="theory",
            next_state="challenge",
        )
        state = self.coordinator.ingest(
            task_id,
            self.write_json("brief.json", brief),
            self.write_json("brief-audit.json", self.analyst_fixture(task_id, "theory-liaison", "chatgpt-theory")),
        )
        self.assertEqual(state["workflow_state"], "challenge")
        self.assertTrue((task_dir / "theory-brief.md").exists())
        self.assertTrue((task_dir / "messages" / "001-theory_brief.json").exists())
        self.assertTrue((task_dir / "analyses" / "001-theory-liaison.json").exists())

        challenge = self.deliberation_message(
            task_id,
            message_type="challenge",
            sender="claude-synthesis-lead",
            workflow_state="challenge",
            next_state="theory_revision",
        )
        state = self.coordinator.ingest(
            task_id,
            self.write_json("challenge.json", challenge),
            self.write_json(
                "challenge-audit.json",
                self.analyst_fixture(task_id, "synthesis-liaison", "claude-synthesis-build"),
            ),
        )
        self.assertEqual(state["workflow_state"], "theory_revision")
        self.assertEqual(state["message_count"], 2)
        self.assertEqual(state["analyst_count"], 2)
        self.assertEqual(state["provider_calls"], 0)
        self.assertTrue((task_dir / "challenge-adaptation-report.md").exists())
        record = (task_dir / "decision-record.md").read_text(encoding="utf-8")
        self.assertIn("challenge", record)
        self.assertIn("## D-001 manual", (task_dir / "unrouted" / "decision-record.md").read_text(encoding="utf-8"))

    def test_ingest_rejects_wrong_phase_sender_and_invalid_envelope(self):
        task_id = "PIG-906"
        self.adopt_fixture(task_id)
        self.coordinator.adopt_task(task_id, "Recover", "deadbeef")

        wrong_sender = self.deliberation_message(
            task_id,
            message_type="theory_brief",
            sender="claude-synthesis-lead",
            workflow_state="theory",
            next_state="challenge",
        )
        audit = self.write_json("audit.json", self.analyst_fixture(task_id, "theory-liaison", "chatgpt-theory"))
        with self.assertRaises(MessageValidationError):
            self.coordinator.ingest(task_id, self.write_json("wrong-sender.json", wrong_sender), audit)

        invalid = self.deliberation_message(
            task_id,
            message_type="theory_brief",
            sender="chatgpt-theory",
            workflow_state="theory",
            next_state="challenge",
            evidence=[{"not": "a string"}],
        )
        with self.assertRaises(MessageValidationError):
            self.coordinator.ingest(task_id, self.write_json("invalid.json", invalid), audit)

        state = self.coordinator.status(task_id)
        self.assertEqual(state["workflow_state"], "intake")
        self.assertEqual(state["message_count"], 0)

        state["workflow_state"] = "building"
        self.coordinator.store.save(state)
        valid = self.deliberation_message(
            task_id,
            message_type="theory_brief",
            sender="chatgpt-theory",
            workflow_state="theory",
            next_state="challenge",
        )
        with self.assertRaises(TransitionError):
            self.coordinator.ingest(task_id, self.write_json("valid.json", valid), audit)

    def provider_request(self):
        return ProviderRequest(
            system_prompt="system",
            user_prompt="user",
            schema=json.loads((ROOT / "protocol" / "message-schema.json").read_text(encoding="utf-8")),
            metadata={"task_id": "PIG-901"},
        )

    def valid_message(self):
        return {
            "task_id": "PIG-901",
            "project": "pigment",
            "round": 1,
            "sender": "claude-synthesis-lead",
            "recipient": "coordinator",
            "message_type": "final_synthesis",
            "workflow_state": "final_synthesis",
            "summary": "A concise synthesis.",
            "assumptions": [],
            "accepted_points": [
                "user_outcome: Useful outcome",
                "information_architecture: Clear structure",
                "principal_flow: Coherent flow",
            ],
            "disputed_points": [],
            "proposal": "Buildable proposal",
            "rationale": "Grounded rationale",
            "evidence": ["feasibility-confirmed: reviewer"],
            "requested_actions": [],
            "acceptance_criteria": ["Observable result"],
            "risks": [],
            "confidence": "high: tested",
            "next_state": "awaiting_build_approval",
            "created_at": "2026-07-20T10:00:00Z",
        }

    def valid_analyst_packet(self):
        return {
            "task_id": "PIG-901", "project": "pigment", "round": 1,
            "analyst_id": "theory-liaison", "pole": "chatgpt-theory", "analysis_mode": "outgoing",
            "artifact_reviewed": ["theory_brief"], "summary": "Valid analysis.",
            "semantic_validity": "valid", "intended_user_outcome": "A useful product.",
            "essential_principles": [], "optional_forms": [], "accepted_counterpole_points": [],
            "constraints_or_principles_to_defend": [], "adaptations": [], "resolved_issues": [],
            "critical_issues": [], "noncritical_issues": [], "unsupported_claims": [],
            "evidence_gaps": [], "specialists_recommended": [], "intent_preserved": True,
            "feasibility_supported": False, "quality_evidence_appears_sufficient": False,
            "convergence_recommended": False, "recommended_action": "advance",
            "recommended_next_state": "challenge",
            "human_escalation": {"recommended": False, "reason_category": "", "decision_required": "", "why_the_teams_cannot_resolve_it": ""},
            "confidence": {"level": "high", "basis": "Fixture"}, "rationale": "Fixture rationale.",
            "owner_report": {"visibility": "audit_only", "title": "Theory Liaison Report", "markdown": "No owner attention required."},
            "created_at": "2026-07-20T10:00:00Z",
        }


if __name__ == "__main__":
    unittest.main()
