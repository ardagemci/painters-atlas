# PIG-001 — Intake Baseline (verified facts)

**Prepared by:** Synthesis Lead (Rubens), main session
**Date:** 2026-07-21
**Purpose:** A single verified fact base for every PIG-001 specialist. Cite this
file rather than re-deriving. Everything below was observed on this machine at
the commit named; nothing here is inferred.

---

## 1. Task identity

| Field | Value | Note |
| --- | --- | --- |
| Task id (this repo) | `PIG-001` | Schema-compliant (`^PIG-[0-9]{3,}$`) |
| Incoming artifact id | `THEORY-001` | **Alias.** See contradiction C1 |
| Incoming artifact | `THEORY_001` (repo root), filed as `theory-brief.md` | |
| Requested state | `claude_analysis` | **Not a legal state.** See C2 |

`THEORY-001` and `PIG-001` denote the same objective. This alias is recorded,
not silent — the schema forbids the incoming id, and `protocol/tasks/README.md`
plus PROTOCOL.md §7 mandate `PIG-NNN` directories.

## 2. Build identity

| Field | Value |
| --- | --- |
| Commit SHA | `3c2e9fa45645d787da3754417448bbcebfd4029a` |
| Branch | `main` (no feature branch cut yet — Gate 4 applies before any build) |
| Upstream | `origin/main` at same SHA (fast-forwarded 24a807d → 3c2e9fa) |
| Target deployment | https://ardagemci.github.io/painters-atlas/#/ |
| Working tree | Untracked only: `IVO_001.md`, `MIRA_001.md`, `SOREN_001.md`, `THEORY_001.md` |

`THEORY_001` (tracked, committed in 3c2e9fa) and `THEORY_001.md` (untracked) are
byte-identical — SHA1 `d3a37c422a3cff7d384667cdfc645b6c7c946663` for both. A
duplicate, not a conflict.

## 3. Validator output — unedited

Command: `osascript -l JavaScript tools/validate.jxa.js`

```text
app.js: syntax OK
artists: 246, movements: 74, techniques: 39, eras: 8, nations: 37, painter styles: 27, influence edges: 225, venues: 115, catalog: 315 (tier1: 73), daily pool: 73, museum notes: 103, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
WARNINGS:
  deck pool: <2 works with E<=-40
  deck pool: empty F×D quadrant 1,-1
ALL REFERENCES VALID
```

**THEORY_001 §3.1 is accurate.** All fourteen counts match today's build exactly,
and both deck warnings reproduce verbatim. The theory team's data snapshot is
confirmed, not stale.

## 4. Coordinator unit tests

`python3 -m unittest discover -s tests` → **6 tests, OK** (run 2026-07-21).

## 5. Confirmed contradictions (for the register)

**C1 — Envelope violates the frozen schema; the Kernel would reject it.**
Checked against `protocol/message-schema.json`. THEORY_001's envelope fails on
eight counts:

| # | Field | Value supplied | Schema requires |
| --- | --- | --- | --- |
| 1 | `task_id` | `THEORY-001` | pattern `^PIG-[0-9]{3,}$` |
| 2 | `sender` | `pigment-theory-team` | enum: chatgpt-theory / claude-synthesis-lead / coordinator |
| 3 | `recipient` | `claude-team` | enum: chatgpt-theory / claude-synthesis-lead / coordinator / user |
| 4 | `message_type` | `final_synthesis_and_execution_handoff` | one of 12 enumerated types |
| 5 | `workflow_state` | `claude_analysis` | one of 14 enumerated states |
| 6 | `next_state` | `claude_analysis` | one of 14 enumerated states |
| 7 | `source_reports` | present | `additionalProperties: false` — unknown key |
| 8 | missing | — | `rationale`, `evidence`, `requested_actions`, `acceptance_criteria`, `risks` all absent (all required) |

PROTOCOL.md §3: "A message missing any field is returned by the Coordinator
without processing." This document could not have entered the system through the
Kernel; it arrived by direct commit. That is a process fact the team must
disposition — it does not by itself make the content wrong, and the content is
substantially sound (see §3 above).

**C2 — `claude_analysis` is not a legal workflow state.** The canonical set
(PROTOCOL.md §2, schema) has no such state. The nearest legal state for "theory
received, Claude analyzing" is `challenge`.

**C3 — Three of six cited source reports do not exist in the repo.**

| Report | Status |
| --- | --- |
| `IVO_001.md` | present (616 lines) |
| `MIRA_001.md` | present (285 lines) |
| `SOREN_001.md` | present (251 lines) |
| `NIKO_001.md` | **missing** |
| `ELARA_001.md` | **missing** |
| `ARGUS_001.md` | **missing** |

THEORY_001 §12 assigns live responsibilities to NIKO, ELARA, and ARGUS, and §7
criteria 9–13 rest on ARGUS-style evidence reasoning. Claude cannot verify that
the synthesis faithfully represents three of its six inputs. Treated as an
evidence gap, not as an accusation.

**C4 — Documentation counts are stale (theory claim confirmed).**

| Source | Claim | Validator | Status |
| --- | --- | --- | --- |
| `PIGMENT.md` | 235 artists | 246 | stale |
| `README.md` | 231 painters | 246 | stale |
| `PIGMENT.md` | 103 museum notes | 103 | current |

## 6. Standing constraints for every specialist

- **Gate 1 is in force.** No production file (`js/`, `css/`, `index.html`, `p/`,
  `tools/`, `sitemap.xml`, `robots.txt`) may be edited. No
  `specification.md` exists, so no build authorization exists. This round is
  analysis only — THEORY_001 §0 asks for exactly that.
- **Gate 4.** Any later build happens on an isolated branch, never `main`.
- Zero-dependency static site; no Node on this Mac (JXA validator);
  serve with `python3 -m http.server 8421 -d .`.
- Frozen terms (THEORY_001 §9.1) and stable IDs/slugs/localStorage fields must
  not be renamed.
