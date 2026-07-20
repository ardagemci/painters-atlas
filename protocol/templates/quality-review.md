---
# Envelope: see _envelope.md — message_type: review (internal), workflow_state: internal_review
---

# Quality Review — <task_id>

## 0. Independence declaration
<Reviewer confirms it implemented none of the code under review.>

## 1. Scope reviewed
<Branch, commit, surfaces, and what was NOT reviewed.>

## 2. Checks run
<Validator output; serve environment; tools used.>

## 3. Acceptance criteria
<Table: criterion → PASS/FAIL → reproducible evidence.>

## 4. Accessibility review
<Keyboard, focus visibility/order, contrast (both themes), semantics,
responsive layouts, reduced motion — each with result and evidence.>

## 5. Workflow and failure-state tests
<End-to-end flows exercised, incl. empty/failure/recovery states.>

## 6. Regression sweep
<Existing routes checked; collisions/breakage found or none.>

## 7. Findings
<Numbered: [critical|major|minor|note] — description — reproduction
steps — evidence. Criticals and majors block Gate 2.>

## 8. Gate 2 verdict
**CERTIFIED** (all criteria pass; validator passes; zero open
critical/major findings; browser evidence attached — may advance to
human_review_ready) or **BLOCKED** (list the exact blocking findings).
