# RIGHTS-001 — Decision Record

Living document (Gate 3). Every material adaptation records: what changed, why,
which assumption or constraint required it, supporting evidence, effect, and
accept / reconsider / escalate status. Unrecorded deviations are defects.

Owner decisions are recorded here as **decisions**; agent analysis is recorded
as **evidence**. OD-5 binds: nothing in this file states a clearance.

## D-000 — Task opened

- **What:** RIGHTS-001 opened under OP-RIGHTS at baseline `dd87ad2`, state `intake`.
- **Why:** Four open questions had accumulated with evidence assembled but no
  route to an owner decision — see `intake-baseline.md` §§3–6.
- **Constraint:** `protocol/oriented/OP-RIGHTS.md`; OD-5 throughout.
- **Status:** accept.

## Open items carried in at intake

| id | Item | State |
|---|---|---|
| A | Six records on a `pd` token over CC-asserted files | open — schema value undecided |
| B | `the-ten-largest-no-9`: bare CC tag, no licensor; alternative carries © | open — no clean basis located |
| C | Procedural covers on 61 walled records, drawn from Pigment's own palette assignment for the artist | open — see E-001; no artwork pixels involved |
| D | Jurisdiction | open — blocks precise answers to A, B and C |

## Decisions

## D-001 — Round-one challenge routed without a liaison packet

- **What:** `messages/002-challenge.json` and
  `challenge-adaptation-report.md` were sent to the Theory Team directly. The
  Synthesis Liaison (Duchamp) packet required by `PROTOCOL.md` §1 was not
  produced, and the Coordinator did not ingest the message or advance
  `state.json`, which remains at `intake`.
- **Why:** Owner instruction, given explicitly after being told the packet and
  ingest were the alternative. Round one is a challenge to a theory artifact,
  not a build authorisation; nothing downstream of it can reach production
  without Gate 1, which is untouched.
- **Constraint waived:** `PROTOCOL.md` §1, "after every team artifact, that
  pole's liaison analyst audits it before the Kernel routes it."
- **Effect:** The round-two revision arrives unaudited by the liaison, so any
  defect in the challenge reaches the Theory Team unfiltered. `state.json` and
  the message log now disagree about the round: two messages exist at
  `workflow_state` `theory` and `challenge` while state reads `intake`. That
  divergence must be reconciled before the Coordinator is used on this task
  again, or its first ingest will act on a stale state.
- **Evidence:** owner instruction this session; `messages/001-theory_brief.json`,
  `messages/002-challenge.json`, both schema-valid.
- **Status:** accept (owner). Reconsider if the Coordinator is brought back into
  this task.

## E-001 — The procedural covers use no artwork pixels (evidence, not a decision)

- **What:** The round-one brief assumed "the repository evidence does not show
  that artwork pixels are used to generate those covers." Measured at `fa102fc`:
  279 artists carry hand-authored hex palettes in `js/artists-*.js`, and the
  paint path at `js/app.js:815–850` performs no pixel sampling — no
  `getImageData`, no `drawImage` of a source image.
- **Effect on the question:** Derivation from the underlying work is not a live
  possibility. What remains is narrower — whether attaching a Pigment-generated
  image to a named artist on that artist's page raises an issue independent of
  the artwork. It also enlarges option C2: replacing the artist palette removes
  an authored curatorial judgement, not a derivation.
- **Evidence:** `challenge-adaptation-report.md` CH-4.
- **Status:** accept as finding. Decides nothing; C remains open.
