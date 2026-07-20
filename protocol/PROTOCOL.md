# Pigment Dipolar Protocol

Operating protocol for the ChatGPT Theory Team ↔ Claude Synthesis and Build
Team dialogue, carried by the neutral Pigment Coordinator. Companion to the
constitutional rules in `/CLAUDE.md`. Templates live in
`protocol/templates/`; the message envelope schema is
`protocol/message-schema.json`.

The executable Coordinator lives in `pigment_coordinator/`, with its operator
guide at `coordinator/README.md` and CLI at `tools/pigment_coordinator.py`.
It is deterministic workflow software, not a third product-decision agent.

## 1. Deliberation cycle

For each Pigment objective (one `task_id`):

1. ChatGPT → Theory Brief (`theory_brief`)
2. Claude → Challenge and Adaptation Report (`challenge` / `adaptation`)
3. ChatGPT → Revision or Defense (`revision` / `defense`)
4. Claude → Final Synthesis (`final_synthesis`)
5. Coordinator freezes the Implementation Specification (`specification`,
   state → `approved_for_build` after deterministic convergence approval)
6. Claude builds and tests on an isolated branch (`implementation_report`)
7. ChatGPT reviews the built product theoretically (`review`)
8. Claude evaluates and performs justified revisions
   (`response_to_review`)
9. Coordinator prepares the Human Review Package
   (`human_review_package`)
10. The user reviews and decides (`approved` / `rejected`)

Ordinary deliberation ≤ 3 rounds. Each extra round must resolve a
disagreement, add evidence, reduce uncertainty, or materially improve the
proposal — state which, in the message's `rationale`.

After every team artifact, that pole's liaison analyst audits it before the
Kernel routes it. The Theory Liaison checks conceptual integrity and treatment
of Claude's evidence; the Synthesis Liaison checks feasibility, adaptation
accountability, and evidentiary honesty. Their packets validate against
`protocol/analyst-packet-schema.json`. Analysts recommend only: the Kernel
alone controls state and neither analyst sends directly to the other or user.

## 2. Workflow states

`intake` → `theory` → `challenge` → `theory_revision` → `final_synthesis`
→ `awaiting_build_approval` → `approved_for_build` → `building` →
`internal_review` → `revision` (loops to `internal_review`) →
`human_review_ready` → `approved` | `rejected`. Any state may move to
`blocked`.

Only the Coordinator advances `awaiting_build_approval` →
`approved_for_build` and `internal_review`/`revision` →
`human_review_ready`. Only the user sets `approved` / `rejected`.

The Coordinator automatically authorizes isolated implementation when the
Convergence Standard passes. This is not merge or deployment approval. A
workspace-capable Claude command is required to perform a build; the text-only
Messages API cannot satisfy that step.

## 3. Message envelope

Every cross-team message begins with a YAML envelope containing ALL of:

```yaml
task_id:            # e.g. PIG-001
project: pigment
round:              # integer, 1-based
sender:             # chatgpt-theory | claude-synthesis-lead | coordinator
recipient:
message_type:       # see §4
workflow_state:     # see §2
summary:            # ≤ 3 sentences
assumptions: []
accepted_points: []
disputed_points: []
proposal:           # or reference to body section
rationale:
evidence: []        # file paths, screenshots, validator output, citations
requested_actions: []
acceptance_criteria: []
risks: []
confidence:         # low | medium | high, with one-line basis
next_state:         # requested next workflow_state
created_at:         # ISO 8601
```

A message missing any field is returned by the Coordinator without
processing. The schema is machine-checkable via
`protocol/message-schema.json`.

## 4. Message types

`theory_brief`, `challenge`, `adaptation`, `revision`, `defense`,
`final_synthesis`, `specification`, `implementation_report`, `review`,
`response_to_review`, `escalation`, `human_review_package`.

## 5. Convergence standard

The Synthesis Lead may recommend freezing a specification only when ALL
hold:

1. The intended user outcome is explicit.
2. Material assumptions are documented.
3. Critical objections are resolved or recorded.
4. Information architecture and main user flows are coherent.
5. The direction is technically feasible (Implementation Lead confirmed).
6. Acceptance criteria are testable.
7. Material deviations from ChatGPT's proposal are visible in the Decision
   Record.
8. No unresolved critical risk is hidden.
9. Remaining disagreements are noncritical or genuinely require the user.

## 6. Quality gates (enforced, not advisory)

- **Gate 1 — build authorization.** No production file edits for a feature
  until `protocol/tasks/<task_id>/specification.md` exists with
  `workflow_state: approved_for_build`. The Implementation Lead checks this
  before every build session; risky work additionally requires plan
  approval before edits.
- **Gate 2 — review certification.** `human_review_ready` requires: all
  acceptance criteria pass; the data validator passes; zero open critical
  or major Quality Review findings; browser evidence (desktop + mobile,
  both themes) attached. Certified only by the Quality Reviewer, who must
  be independent of the implementation.
- **Gate 3 — deviation ledger.** Every material adaptation records: what
  changed, why, which assumption/constraint required it, supporting
  evidence, UX effect, and accept/reconsider/escalate status. Unrecorded
  deviations are defects.
- **Gate 4 — isolation.** Feature work happens on an isolated branch or
  worktree; `main` merges and production deployment require the user.

## 7. Task artifact layout

When a real objective starts, create `protocol/tasks/<task_id>/` at
runtime (do not pre-create; do not hand-edit Claude's runtime team-state or
mailbox directories — reusable roles live only in `.claude/agents/`):

```
protocol/tasks/PIG-001/
  analyses/                       (canonical liaison JSON packets)
  analyst-reports/                (rendered reports; Kernel-routed only)
  messages/                       (immutable cross-team JSON envelopes)
  theory-brief.md                 (from Coordinator)
  challenge-adaptation-report.md
  revision-or-defense.md          (from Coordinator)
  final-synthesis.md
  specification.md                (frozen by Coordinator; carries state)
  decision-record.md              (living document, Gate 3)
  build-evidence-report.md
  evidence/                       (screenshots, outputs)
  quality-review.md
  theoretical-review.md           (from Coordinator)
  response-to-theoretical-review.md
  human-review-package.md
```

## 8. Escalation to the user

Escalate early only for: material identity/audience/purpose change; two
equally coherent directions separated mainly by taste; legal, privacy,
security, or financial risk; paid services or significant infrastructure;
substantial scope/timeline change; essential information that cannot be
responsibly inferred. Use message_type `escalation`. Everything else is
resolved internally with evidence.

## 9. Presentation discipline

Raw internal debate is preserved in the task directory and Decision Record
but is not shown to the user by default. The Human Review Package
summarizes only disagreements that materially affected the product.
Analyst reports marked `audit_only` remain internal; `human_review` reports
are included in the Human Review Package; `escalation` reports are surfaced
only when their packet also recommends a valid constitutional escalation.
