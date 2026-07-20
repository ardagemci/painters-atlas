PROJECT = "pigment"

WORKFLOW_STATES = (
    "intake",
    "theory",
    "challenge",
    "theory_revision",
    "final_synthesis",
    "awaiting_build_approval",
    "approved_for_build",
    "building",
    "internal_review",
    "revision",
    "human_review_ready",
    "approved",
    "rejected",
    "blocked",
)

MESSAGE_TYPES = (
    "theory_brief",
    "challenge",
    "adaptation",
    "revision",
    "defense",
    "final_synthesis",
    "specification",
    "implementation_report",
    "review",
    "response_to_review",
    "escalation",
    "human_review_package",
)

SENDERS = ("chatgpt-theory", "claude-synthesis-lead", "coordinator")
RECIPIENTS = SENDERS + ("user",)

REQUIRED_MESSAGE_FIELDS = (
    "task_id",
    "project",
    "round",
    "sender",
    "recipient",
    "message_type",
    "workflow_state",
    "summary",
    "assumptions",
    "accepted_points",
    "disputed_points",
    "proposal",
    "rationale",
    "evidence",
    "requested_actions",
    "acceptance_criteria",
    "risks",
    "confidence",
    "next_state",
    "created_at",
)

ARTIFACT_FILENAMES = {
    "theory_brief": "theory-brief.md",
    "challenge": "challenge-adaptation-report.md",
    "adaptation": "challenge-adaptation-report.md",
    "revision": "revision-or-defense.md",
    "defense": "revision-or-defense.md",
    "final_synthesis": "final-synthesis.md",
    "specification": "specification.md",
    "implementation_report": "build-evidence-report.md",
    "review": "theoretical-review.md",
    "response_to_review": "response-to-theoretical-review.md",
    "human_review_package": "human-review-package.md",
    "escalation": "escalation.md",
}
