---
# Message envelope — required on every cross-team artifact.
# Validate against protocol/message-schema.json. All fields required.
task_id: PIG-000
project: pigment
round: 1
sender: claude-synthesis-lead
recipient: coordinator
message_type: # theory_brief | challenge | adaptation | revision | defense | final_synthesis | specification | implementation_report | review | response_to_review | escalation | human_review_package
workflow_state: # intake | theory | challenge | theory_revision | final_synthesis | awaiting_build_approval | approved_for_build | building | internal_review | revision | human_review_ready | approved | rejected | blocked
summary: ""
assumptions: []
accepted_points: []
disputed_points: []
proposal: ""
rationale: ""
evidence: []
requested_actions: []
acceptance_criteria: []
risks: []
confidence: "" # low|medium|high — basis
next_state: ""
created_at: "" # ISO 8601
---
