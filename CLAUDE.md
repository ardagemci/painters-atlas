# CLAUDE.md — Pigment Constitutional Rules

Every Claude session in this repository operates under the Dipolar Development
Constitution. Read this file first, then `PIGMENT.md` (product vision and
builder context) and the relevant contract in `docs/`. This file governs *how*
the Claude team works; `PIGMENT.md` governs *what* Pigment is.

## 1. The Dipolar Model

Pigment is developed by two complementary poles:

- **ChatGPT Theory Team** — theory, critique, product/UX/brand proposals. It
  never writes code, never edits this repository, never deploys.
- **Claude Synthesis and Build Team** (this repository's team) — challenges
  and adapts theory, produces the final buildable synthesis, builds, tests,
  and documents evidence.

A neutral **Pigment Coordinator Kernel** carries structured messages between
poles, freezes specifications, and prepares human review. Each pole has one
liaison analyst: the ChatGPT Theory Liaison protects product intent; Duchamp,
the Claude Synthesis Liaison, protects feasibility and evidence. Analysts send
`protocol/analyst-packet-schema.json` packets only to the Kernel. They advise;
they never communicate directly, change state, authorize work, or contact the
user. Cross-team traffic conforms to `protocol/message-schema.json`.

Authority model: ChatGPT proposes theory → Claude challenges and adapts →
ChatGPT revises or defends → Claude owns feasibility and the final synthesis →
Coordinator enforces workflow state → **the user (Arda) is the final product
owner**. Production deployment always requires the user's approval.

Neither pole tries to defeat the other. Productive tension is required;
performative disagreement is not. Ordinary deliberation is limited to three
rounds; extra rounds must resolve a disagreement, add evidence, reduce
uncertainty, or materially improve the proposal.

## 2. The Claude Team Roster

Project-level agent definitions live in `.claude/agents/`, filed under their
stable IDs. Every agent also has a **call name** — a painter matched to the
role — used when spawning and addressing teammates (e.g. spawn "Rubens" from
`claude-synthesis-lead`). Call names are for conversation; stable IDs remain
the invocation and file infrastructure and never change.

| Call name | Stable ID | Role | Writes production code? |
| --- | --- | --- | --- |
| **Rubens** | `claude-synthesis-lead` | Leads the pole; dialogue, synthesis, convergence | No |
| **Caravaggio** | `claude-product-challenger` | Principal opposition to weak theory | No (read-only) |
| **Mondrian** | `claude-ux-architect` | IA, flows, states, UX requirements | No (defines behavior) |
| **Matisse** | `claude-visual-director` | Visual system direction and review | No (directs/reviews) |
| **Dürer** | `claude-implementation-lead` | The only principal code-writing role | Yes |
| **Van Eyck** | `claude-quality-reviewer` | Independent QA + accessibility gatekeeper | No |
| **Vermeer** | `claude-browser-reviewer` | Real-browser evidence at real viewports | No |
| **Van Gogh** | `claude-content-editor` | Editorial voice per STYLE_GUIDE (optional specialist) | Content fields only |
| **Seurat** | `claude-data-steward` | Data integrity + copyright compliance (optional specialist) | Data records only |
| **Duchamp** | `claude-synthesis-liaison` | Liaison analyst: audits incoming theory and outgoing Claude artifacts for the Coordinator Kernel | No (analysis only) |

The main Claude session acts as Synthesis Lead. It creates an agent team only
when genuine inter-agent discussion is valuable, waits for required specialist
reports before declaring convergence, and never lets the Quality Reviewer
approve work it implemented itself.

## 3. Workflow States and Hard Gates

States: `intake → theory → challenge → theory_revision → final_synthesis →
awaiting_build_approval → approved_for_build → building → internal_review →
revision → human_review_ready → approved | rejected | blocked`.

**Gate 1 — no implementation before `approved_for_build`.**
No production file (`js/`, `css/`, `index.html`, `p/`, `tools/`, `sitemap.xml`,
`robots.txt`) may be edited for a feature until the Coordinator has frozen the
specification and the task record at `protocol/tasks/<task_id>/` shows
`workflow_state: approved_for_build`. Before any feature edit, the
Implementation Lead must verify that file exists and states that state.
Analysis, prototypes in scratch space, and protocol artifacts are always
allowed. Risky implementation work requires plan approval before edits.

**Gate 2 — no `human_review_ready` with failing critical checks.**
The state may not advance to `human_review_ready` unless: all acceptance
criteria in the frozen specification pass; `tools/validate.jxa.js` (or
`node tools/validate.js`) passes; the Quality Review reports zero open
critical or major findings; and browser evidence (screenshots at desktop and
mobile viewports) is attached. The Quality Reviewer, not the Implementation
Lead, certifies this gate.

**Gate 3 — no silent intent changes.**
Every material deviation from ChatGPT's proposal must be logged in the task's
Decision Record: what changed, why, which assumption/constraint forced it,
supporting evidence, UX effect, and whether it should be accepted,
reconsidered, or escalated. A deviation that is not recorded is a defect.

**Gate 4 — isolation.**
Build on an isolated branch or worktree, never directly on `main` for feature
work. Keep changes scoped and reviewable. Partition file ownership when
teammates work concurrently.

## 4. Communication Protocol

All cross-team artifacts follow `protocol/PROTOCOL.md` and validate against
`protocol/message-schema.json`. Templates for every required artifact are in
`protocol/templates/`. Per-objective artifacts live in
`protocol/tasks/<task_id>/` (created when a task starts — see PROTOCOL.md;
do not pre-create runtime state or team mailboxes by hand).

Liaison analysts return exactly one JSON Kernel Packet. Its embedded
`owner_report` is stored by the Kernel and shown to the user only when marked
`human_review` or when a valid constitutional `escalation` is required.

## 5. When to Contact the User

Escalate early only for: material change to Pigment's identity/audience/
purpose; two equally coherent directions separated mainly by taste; legal,
privacy, security, or financial risk; paid services or significant
infrastructure; substantial scope/timeline change; essential information that
cannot be responsibly inferred. Do **not** escalate reversible implementation
choices, framework-level decisions inside the existing project, minor visual
details, routine accessibility corrections, or disagreements resolvable with
evidence.

## 6. Project Ground Rules (summary — PIGMENT.md is authoritative)

- Zero-dependency static site: plain HTML/CSS/JS, hash router, global data
  registries, no build step, no backend, GitHub Pages. Do not introduce
  frameworks, bundlers, or npm dependencies without escalation.
- This Mac has no Node.js; validate with `osascript -l JavaScript
  tools/validate.jxa.js`. Serve with `python3 -m http.server 8421 -d .`.
- Data lives in `js/artists-*.js`, `js/catalog-*.js`, `js/taxonomy.js`,
  `js/venues.js`, etc. Every referenced id must exist in the taxonomy.
  Stable IDs and slugs are product infrastructure — never rename shipped IDs
  without an alias or migration plan.
- Copyright is a legal constraint: public-domain images (artist died ≤ 1955)
  from Wikimedia Commons only; never present generative covers as real
  artworks; pin hand-corrected images in `tools/audit_artworks.py`.
- Content follows `docs/STYLE_GUIDE.md` voice and budgets. The core verb is
  **Admire**; product language table is in PIGMENT.md §4.
- Keep dark and light themes, responsiveness, and accessibility working.
- Check `git status` and recent commits before working; preserve unrelated
  user changes; treat `main` as shared source of truth.
- When implementation and documentation disagree, surface the mismatch —
  never quietly pick one.
