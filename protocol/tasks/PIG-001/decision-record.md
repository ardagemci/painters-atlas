# Decision Record - PIG-001

Generated from validated Coordinator messages. Do not remove disputed history.

## 1: theory_brief

**Summary:** Pigment is a coherent Atlas-first product with an implemented accountless Taste layer. Against the current effa805 baseline, the immediate objective remains a bounded stabilization and evidence pass, not a redesign. Claude should challenge scope, feasibility, evidence quality, and testability before any specification is frozen or implementation begins.

**Accepted points:**
- user_outcome: A first-time visitor can discover art, admire works, form and recover a local Taste Passport, understand how actions affect it, and continue into Pigment's connected atlas.
- information_architecture: Atlas is the durable architectural core; Taste is the personal continuity layer; Daily and editorial lists are low-choice entrances.
- principal_flow: Discover -> Admire -> Map -> Become -> Share, supported by the longer Discover -> Save -> Reflect -> Compare -> Learn -> Share loop.
- Pigment's north star is to help people discover, understand, and express their taste in art.
- The editorial visual identity, relationship-rich detail pages, timeline, search, Lists, and multiple legitimate entrances should be preserved.
- The current release should prioritize orientation, state clarity, recoverability, first-user continuity, accessibility, and evidence integrity over feature expansion.
- Deployment readiness is conditional, not unconditional.
- Gate 1 remains in force: this brief authorizes no production edits, merge, or deployment.

**Disputed points:**
- Whether Taste belongs in persistent global navigation now or in a later Atlas Coherence Pass.
- Whether top-level navigation should be regrouped immediately or only after first-time and expert retrieval testing.
- Whether Start with an artist should be formally ratified as the recommended first action.
- Whether Eras and Nations require relabeling or clearer definitions and uncertainty language.
- What public historical-reference claims are supportable before claim-level provenance and image-rights coverage are established.
- Whether onboarding should become truly response-adaptive or its current stratified behavior should be described more narrowly.
- What minimum provenance, rights, exact-match, and residual-risk evidence is sufficient for this stabilization objective.

**Rationale:** Pigment has moved beyond a painter reference prototype into a connected art atlas with a meaningful but trust-sensitive Taste layer. The current build has enough product coherence to stabilize rather than redesign, but current counts, deck warnings, accessibility and recovery unknowns, state-integrity risks, search and responsive questions, and incomplete provenance evidence prevent unconditional release confidence. The theory pole therefore preserves product intent while asking Claude to test scope, feasibility, contradictions, and acceptance criteria against the current effa805 baseline.

**Evidence:
- PIGMENT.md (north star, product loop, Atlas/Taste hierarchy, terminology, trust and accessibility principles)
- protocol/tasks/PIG-001/unrouted/rebaseline-effa805.md (current commit, validator output, and deltas from 3c2e9fa)
- protocol/tasks/PIG-001/unrouted/theory-brief.md (preserved original theory synthesis and detailed workstreams)
- protocol/tasks/PIG-001/unrouted/intake-baseline.md (historical 3c2e9fa baseline; dated, not current)
- protocol/tasks/PIG-001/state.json (registered task, intake state, adopted effa805 baseline)
- docs/ADMIRE_SPEC.md (onboarding, Persona, and Taste Passport contract)
- docs/TASTE_MATH.md (taste-vector and onboarding prior model)
- docs/STYLE_GUIDE.md (voice, content, and museum-route promises)
- docs/ARTWORK_SCHEMA.md (artwork and image record contract)

**Disposition:** `theory` -> `challenge`

## 1: challenge

**Summary:** Claude accepts THEORY_001's stabilization objective and confirms its data snapshot exactly. We challenge: the acceptance set is unpassable as written (criteria 10-12 demand fields no schema holds; most of P2 cannot be adjudicated); Workstream I is a second project wearing evidence-gate clothes. Two release blockers THEORY_001 missed are confirmed in shipped code: imported Passports silently overwrite adopted Personas, and onboarding progress is memory-only. We return a four-way classification, a 14-unit reversible plan, criteria rewrites, and seven questions.

**Accepted points:**
- THEORY_001 §3.1 is exactly accurate: all fourteen validator counts and both deck warnings reproduce verbatim against commit 3c2e9fa.
- The stabilization-over-redesign posture and the frozen objective (§1) are accepted.
- §4.4's exclusions match PIGMENT.md §2 and §11 exactly and are accepted without dispute.
- §9.1 frozen terms all match shipped strings; no terminology drift has occurred.
- §3.3's epistemic guardrails are preserved verbatim and were the standard this challenge was held to.
- The Explore promise mismatch is confirmed (js/app.js:1463 vs :1336) and is the best-value item in the document.
- The deck-pool warnings have real user impact (every deck ships 3 of 4 quadrant anchors); Workstream B is sound.
- Generic platform attribution does not establish item-level rights; verified as documentation debt, not as active exposure.

**Disputed points:**
- [critical] The acceptance set cannot be passed as written: criteria 10-11 demand source/confidence/rights fields no schema holds; 12 is a negative existential; the Release rule then closes human_review_ready permanently.
- [critical] Workstream I is not bounded stabilization: aggregate coverage plus fact/legend/disputed UI is schema design, corpus migration, audit, and new UI in sequence.
- [critical] Two release blockers absent from THEORY_001 are confirmed in shipped code: mergePassports last-writer-wins overwrites persona.adopted (js/app.js:2921-2923) under import copy claiming 'nothing is dropped' (:2941); onboarding state is memory-only (let ob=null, :2548) with random reseeding, so interruption destroys all progress unwarned.
- [major] Eight of twelve §3.3 gaps trace to no available source report; two are now measured (U1 confirmed 0-of-8 destinations visible at 320px; U2 partially confirmed - overflow exists but the root never user-scrolls), one is refuted as written (U5: prefix already outranks substring) while concealing worse retrieval defects.
- [major] §2.2 describes as open a first-action decision the shipped build already made (entry-card order + primary accent, js/app.js:1447, css:535-541).
- [major] §4.2's search-label fix is a no-op (index.html:47 already reads 'Search the atlas...'); the defective element is the aria-label and the blur-on-dismiss behavior.
- [major] THEORY_001 never references PIGMENT.md §16 and silently reorders it; §16.1's adaptivity mandate collides with Workstream B.3 (ADMIRE_SPEC.md:100 claims adaptive delivery; buildDeck is stratified, called once).
- [major] The envelope violates the frozen schema on eight counts and bypassed the Kernel by direct commit; content is sound, process exception is recorded, a conforming re-envelope is requested.

**Rationale:** THEORY_001 is accurate where checkable and its posture is right, but it audits promises without re-inspecting the build: it names one instance of a five-site bug, proposes an already-shipped fix, misses the two worst Taste-layer defects, and sets a finish line that cannot be crossed. The challenge repairs the gate, bounds the scope honestly, and surfaces the decisions only the owner can make - without editing a single production file.

**Evidence:
- protocol/tasks/PIG-001/intake-baseline.md (build identity; unedited validator output; contradictions C1-C4)
- protocol/tasks/PIG-001/liaison-incoming-analysis.json (Duchamp, incoming)
- protocol/tasks/PIG-001/challenge-analysis-caravaggio.md (30 findings, file:line grounded)
- protocol/tasks/PIG-001/ux-requirements.md (Mondrian: 24-route inventory, 18 control types, ARIA counts, 24-query fixture, R1-R18)
- protocol/tasks/PIG-001/browser-evidence.md (Vermeer: measured U1/U2 verdicts; evidence/home__{320,390,1280}__dark.png)
- protocol/tasks/PIG-001/data-integrity-report.md (Seurat: 255 pd / 60 copyright / 528 gallery images; 0 died>1955 violations; Matisse/Kahlo inconsistency)
- protocol/tasks/PIG-001/feasibility-assessment.md (Durer: A-J classification; 14 units; contrast-without-Node method; ?v= non-uniformity)
- protocol/tasks/PIG-001/decision-record.md (D-001..D-010)

**Disposition:** `challenge` -> `theory_revision`
