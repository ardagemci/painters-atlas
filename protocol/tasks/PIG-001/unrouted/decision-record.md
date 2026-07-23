# Decision Record — PIG-001

Living Gate 3 ledger. Every material deviation from ChatGPT's proposal, and
every significant internal decision, gets an entry. An unrecorded deviation
is a defect. Raw debate is preserved here and summarized elsewhere.

---

## D-001

- **Date / round / state:** 2026-07-21 / round 1 / challenge
- **What changed:** Incoming task identifier `THEORY-001` is carried as `PIG-001` for all repository and Kernel purposes.
- **Why it changed:** The frozen schema constrains `task_id` to `^PIG-[0-9]{3,}$`; `THEORY-001` cannot be represented.
- **Assumption or constraint that required it:** `protocol/message-schema.json` (task_id pattern); PROTOCOL.md §7 task layout.
- **Supporting evidence:** intake-baseline.md §1.
- **Effect on user experience:** None; internal identifier only.
- **Status:** accepted
- **Raised by / decided by:** Synthesis Lead / Synthesis Lead (endorsed by Duchamp, adaptation 1)

## D-002

- **Date / round / state:** 2026-07-21 / round 1 / challenge
- **What changed:** Requested workflow state `claude_analysis` (not a legal state) normalized to `challenge`.
- **Why it changed:** The canonical state set has no `claude_analysis`; the work requested by THEORY_001 §0 is what `challenge` contains (PROTOCOL.md §1 step 2).
- **Assumption or constraint that required it:** PROTOCOL.md §2; message-schema.json state enums.
- **Supporting evidence:** intake-baseline.md §5 C2; liaison-incoming-analysis.json adaptation 2.
- **Effect on user experience:** None; keeps Gate 1 unambiguously in force.
- **Status:** accepted
- **Raised by / decided by:** Synthesis Lead / Synthesis Lead (endorsed by Duchamp)

## D-003

- **Date / round / state:** 2026-07-21 / round 1 / challenge
- **What changed:** THEORY_001's envelope defect (8 schema violations; arrived by direct commit, bypassing the Kernel) is dispositioned as: process exception recorded; conforming re-envelope requested from the theory pole; Claude proceeds on the content in parallel and does NOT rewrite the counterparty's envelope.
- **Why it changed:** Content soundness and envelope validity are separate questions. Waiving teaches that direct commits bypass the protocol; discarding sound content is process fetishism; Claude rewriting another pole's message would erase the process fact.
- **Assumption or constraint that required it:** PROTOCOL.md §3 ("a message missing any field is returned without processing").
- **Supporting evidence:** intake-baseline.md §5 C1; liaison-incoming-analysis.json CRITICAL 6 and noncritical issue 1.
- **Effect on user experience:** None directly; preserves the Kernel's enforcement power.
- **Status:** accepted
- **Raised by / decided by:** Duchamp / Synthesis Lead

## D-004

- **Date / round / state:** 2026-07-21 / round 1 / challenge
- **What changed:** Vermeer (Browser Evidence Reviewer, normally a review-time role) was invoked during the analysis round, scoped to exactly two measurements (root overflow; mobile nav discoverability).
- **Why it changed:** THEORY_001 §0 demands a blocker classification that could not be made honestly while its two most safety-relevant inputs (U1, U2) were unmeasured; both concern the currently deployed build, not Claude's work, so independence is not compromised.
- **Assumption or constraint that required it:** Duchamp presented the tradeoff neutrally and declined to decide; the Synthesis Lead decided.
- **Supporting evidence:** liaison-incoming-analysis.json specialists_recommended (Vermeer CONDITIONAL); browser-evidence.md (both measurements delivered).
- **Effect on user experience:** None; evidence-gathering only.
- **Status:** accepted
- **Raised by / decided by:** Synthesis Lead / Synthesis Lead

## D-005

- **Date / round / state:** 2026-07-21 / round 1 / challenge
- **What changed:** Duchamp's CRITICAL 4 — "The timeline and influence constellation are canvas-rendered generative instruments, so an accessible alternative is a new parallel rendering path, not a correction" (recorded verbatim per CLAUDE.md §2, as an overruled critical finding) — is overruled on evidence.
- **Why it changed:** The timeline is DOM anchors (`js/app.js:894`), the constellation is inline SVG (`:1095`, nodes `:1077`); PIGMENT.md §13 says canvas *covers*, not instruments. Workstream H's "readable alternatives" is bounded markup work, not a parallel renderer.
- **Assumption or constraint that required it:** Evidence beats assertion (CLAUDE.md §5).
- **Supporting evidence:** challenge-analysis-caravaggio.md finding 9; ux-requirements.md item 4 (independent confirmation); feasibility-assessment.md F1-H.
- **Effect on user experience:** Positive — the accessibility corrections stay in the stabilization release instead of being deferred as a "substantial build."
- **Status:** accepted
- **Raised by / decided by:** Caravaggio + Mondrian / Synthesis Lead

## D-006

- **Date / round / state:** 2026-07-21 / round 1 / challenge
- **What changed:** Workstream I (provenance/rights) is proposed split three ways: (a) rights-only register, in scope, out-of-band now, hybrid target (minimal `image.license` + `image.commons` schema fields folded in during the authorized build phase); (b) claim-level historical sourcing, separate task gated on the release-positioning decision; (c) uncertainty UI, deferred to the Atlas Coherence Pass.
- **Why it changed:** Workstream I as written is a second product capability (schema design + corpus migration + new UI) presented as an evidence gate; the legal duty is discharged by the rights register over the actually rendered surface.
- **Assumption or constraint that required it:** No source/license/confidence field exists in any schema; rendering gates display to `status:"pd"` images; PIGMENT.md §14 requires attribution close to the record (hence hybrid, not register-forever).
- **Supporting evidence:** liaison-incoming-analysis.json CRITICAL 2–3; challenge-analysis-caravaggio.md findings 11–13; data-integrity-report.md Q1–Q2.
- **Effect on user experience:** Stabilization release remains shippable; rights documentation improves; no user-facing change until the build phase.
- **Status:** reconsider — proposed to the theory pole in the Challenge Report; not unilaterally applied
- **Raised by / decided by:** Duchamp + Caravaggio + Seurat / Synthesis Lead (pending theory revision + owner positioning decision)

## D-007

- **Date / round / state:** 2026-07-21 / round 1 / challenge
- **What changed:** Acceptance-criteria triage proposed: criteria 10–12 rescoped to the rights register and a disposition register; P2 criteria 28/30/31/33/34 demoted to design review with named adjudicators (Matisse for 33–34, Mondrian for 31–32); 29 reworded as a regression check plus an owner ratification item; 19 reworded to `scrollWidth ≤ clientWidth`; 2 bound to the validator's existing rule; 4 reworded "import (which merges)" plus a new persona-guard criterion; 15/16/22/24/25/27 bound to Mondrian's frozen inventories.
- **Why it changed:** As written, the Release rule plus unpassable P0 criteria closes the gate permanently; roughly ten criteria cannot be objectively judged.
- **Assumption or constraint that required it:** Gate 2 requires criteria the Quality Reviewer can pass/fail without judgment calls.
- **Supporting evidence:** liaison-incoming-analysis.json CRITICAL 1–2, 5; challenge-analysis-caravaggio.md findings 14–19; ux-requirements.md R1–R18.
- **Effect on user experience:** None directly; makes an achievable, honest release gate.
- **Status:** reconsider — proposed to the theory pole; ChatGPT may revise or defend
- **Raised by / decided by:** Duchamp + Caravaggio + Mondrian / Synthesis Lead

## D-008

- **Date / round / state:** 2026-07-21 / round 1 / challenge
- **What changed:** The rights-surface size is corrected to a measured **783 rendered images** (255 catalog `pd` + 528 artworks.js gallery works). This supersedes both Duchamp's "~786 records" framing AND Caravaggio's "not the ~786 records" rebuttal.
- **Why it changed:** Caravaggio was right that the *composition* differs (rendered images, not prose bios + influence edges) and that the work is ~80–90% automatable; but his implication that the rendered surface was materially smaller was wrong — artworks.js (528 rendered images, no status field) is the larger two-thirds of the surface and was missing from his scoping. Stated plainly here so neither error is buried.
- **Assumption or constraint that required it:** Counts must be measured, not argued (Steward's verification duty).
- **Supporting evidence:** data-integrity-report.md Q2.
- **Effect on user experience:** None; scopes the register honestly.
- **Status:** accepted
- **Raised by / decided by:** Seurat / Synthesis Lead

## D-009

- **Date / round / state:** 2026-07-21 / round 1 / challenge
- **What changed:** Matisse and Kahlo (both d. 1954) are flagged `copyright` in the catalog yet their works render ungated in artworks.js galleries — the two stores assert opposite rights postures for the same painters. Queued as an owner escalation item (licensing policy), not resolved internally.
- **Why it changed:** Steward's rule: licensing ambiguity escalates rather than being resolved by assumption. Both satisfy the died≤1955 rule, so this is a policy inconsistency, not a rule breach.
- **Assumption or constraint that required it:** CLAUDE.md §5 (legal risk escalates); PIGMENT.md §14.
- **Supporting evidence:** data-integrity-report.md Q3.
- **Effect on user experience:** None until decided; galleries currently display these works.
- **Status:** escalated (queued for the owner via the Challenge Report §7)
- **Raised by / decided by:** Seurat / Synthesis Lead

## D-010

- **Date / round / state:** 2026-07-21 / round 1 / challenge
- **What changed:** Deck-pool repair path recorded: both validator warnings clear with ~2 re-scores of works already in the pool (Seurat's candidates: Malevich Black Square D −20→−25; a Vermeer/Rembrandt E −35→−40), with the explicit constraint that any re-score must be honest on the merits — coordinates are taste data and must never be tuned merely to silence the validator. Re-scoring is a Gate-1-blocked data edit; recorded as a costed recommendation requiring owner sign-off in the specification.
- **Why it changed:** Every onboarding deck currently ships 3 of 4 quadrant anchors (real calibration impact, not cosmetic).
- **Assumption or constraint that required it:** ADMIRE_SPEC.md:99 coverage rule; validate.jxa.js:209-214.
- **Supporting evidence:** challenge-analysis-caravaggio.md finding 26; data-integrity-report.md Q5.
- **Effect on user experience:** Calm-abstract and strongly classical users stop being pulled toward the middle of the taste map.
- **Status:** reconsider — requires build authorization + owner acceptance
- **Raised by / decided by:** Caravaggio + Seurat / Synthesis Lead

## D-011

- **Date / round / state:** 2026-07-21 / round 1 / challenge (retransmission)
- **What changed:** CHALLENGE_001 retransmitted with its four defective evidence entries quoted. Unquoted colon+space sequences ("Mondrian: ", "Vermeer: ", "Seurat: ", "Durer: ") made YAML parse those entries as mappings, violating the schema's requirement that `evidence` be an array of strings.
- **Why it changed:** The theory pole's liaison reported the defect and — correctly, mirroring our own D-003 posture — declined to rewrite Claude's message. Verified on our side with a real parser before fixing: Ruby/Psych confirmed entries 3–6 parsed as Hash, all other envelope fields clean.
- **Assumption or constraint that required it:** protocol/message-schema.json (`evidence: array of strings`); YAML plain-scalar rules.
- **Supporting evidence:** ruby -ryaml parse before (4 of 8 entries Hash) and after (8 of 8 String), run 2026-07-21.
- **Effect on user experience:** None; envelope mechanics only.
- **Status:** accepted
- **Raised by / decided by:** ChatGPT Theory Liaison / Synthesis Lead. Recorded honestly: Duchamp's outgoing audit passed this envelope after catching the summary-length defect — it validated by inspection, not by an actual YAML parse, and missed this. Standing correction for all future outgoing audits: parse the envelope with a real YAML parser (ruby -ryaml is available on this Mac; PyYAML is not guaranteed).

<!-- Copy the block above for each new decision. Never delete entries;
strike through and supersede instead. -->

## D-012

- **Date / round / state:** 2026-07-21 / round 1 / intake (kernel recovery)
- **What changed:** PIG-001 was recovered into the executable Coordinator per the theory pole's seven-step direction: `adopt` and `ingest` operations implemented in pigment_coordinator/ (store/engine/cli) with 4 new unit tests (suite 11/11); PIG-001 registered at `intake` with all eleven round-1 manual artifacts preserved under `unrouted/`; rebaselined at effa805 (see rebaseline-effa805.md — counts changed under 2b0e18d); challenge-message.json extracted from CHALLENGE_001 and kernel-validated together with liaison-outgoing-audit.json against the exact ingest expectations.
- **Why it changed:** The kernel reported "Unknown task: PIG-001" — the manual round ran outside the state machine, so declaring `theory_revision` would fabricate authoritative state, the mirror of our own C1 finding against THEORY_001.
- **Assumption or constraint that required it:** Kernel authority over workflow state (CLAUDE.md §1, PROTOCOL.md §2); ingest is restricted to deliberation phases so a text file can never claim a build.
- **Supporting evidence:** tests/test_coordinator.py (11 passing); state.json event `task_adopted`; rebaseline-effa805.md; kernel validation run of both transmission pieces.
- **Effect on user experience:** None; workflow infrastructure only.
- **Status:** accepted
- **Raised by / decided by:** ChatGPT team (via owner relay) / Synthesis Lead. Note: liaison-outgoing-audit.json validates against the kernel analyst schema but audited the pre-retransmission CHALLENGE_001; its findings (including the summary repair it demanded) remain accurate and D-011 records the subsequent YAML episode. Routing it as-is with this note, or refreshing it, is the theory pole's call at step 6.

## D-013

- **Date / round / state:** 2026-07-23 / round 2 / final_synthesis
- **What changed:** Three challenge-side claims are corrected per the Round 2 revision's disputes, each verified before acceptance. (1) The 783-image rights-surface figure is superseded by the frozen effa805 inventory: **799 unique public assets** across five surfaces (evidence/asset-inventory-effa805.md) — the old figure counted stored references at 3c2e9fa and omitted museum photos, prerender metadata references, and the homepage reference. (2) The claim that the fetch pipeline "already receives and discards" Commons extmetadata was **false**: tools/fetch_artworks.py:49 and tools/audit_artworks.py:99 request `iiprop=url|mime` only; register automation remains feasible as a one-parameter extension, not a recovery of discarded data. (3) The round-1 warning-only interruption remedy is withdrawn: the revision's criterion requires exact-checkpoint recovery, adopted as materialized-state persistence (deck ids + answers, not the Math.random seed). Additionally corrected during the r2 feasibility pass: the revision carries **29** acceptance criteria (not 31 as first briefed); taxonomy.js IS versioned — the unversioned set is exactly worldmap.js, venues.js, and artists-1..16.js (18 files); canvasTag has 19 call sites.
- **Why it changed:** The counterpole's disputes were verified against the repository and confirmed correct. Recording our own errors plainly is the same standard this team applied to THEORY_001's envelope and claims.
- **Assumption or constraint that required it:** Gate 3 — an unrecorded deviation is a defect; counts must be measured, not argued.
- **Supporting evidence:** evidence/asset-inventory-effa805.{md,json}; tools/fetch_artworks.py:49; tools/audit_artworks.py:99; evidence/feasibility-assessment-r2.md; messages/003-revision.json disputed_points 1, 2, 5.
- **Effect on user experience:** Positive at build time — onboarding interruption recovery is now specified as genuine recovery rather than a warning.
- **Status:** accepted
- **Raised by / decided by:** ChatGPT theory pole (disputes 1–2, 5) and Dürer r2 assessment / Synthesis Lead.
