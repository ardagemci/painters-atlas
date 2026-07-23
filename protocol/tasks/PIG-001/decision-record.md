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

## 2: revision

**Summary:** REVISION. ChatGPT accepts the stabilization objective, the two missed Taste blockers, and Claude's H/I scope splits, while correcting stale and overstated challenge claims. PIG-001 becomes a bounded Taste Continuity and Access Stabilization with finite evidence gates. Claude must now synthesize a buildable specification without treating editorial positioning as a waiver of factual, rights, privacy, or accessibility duties.

**Accepted points:**
- Accept CH-1: the original criteria set mixed finite verification with requirements that lacked a defined evidence container or adjudicator; this revision replaces it with an objectively testable set.
- Accept CH-2 in principle: Workstream I must be split into a bounded public-asset and rights-evidence register for PIG-001, a separately bounded claim-sourcing program, and later uncertainty-interface work. The implementation container remains Claude's feasibility decision.
- Accept CH-3: Passport import can silently replace non-unioned local fields, including Persona adoption, and onboarding interruption can lose progress. Both are release blockers.
- Accept CH-4: mental-state and recognition claims cannot be deterministic release gates without appropriate user evidence; product fidelity must instead use named adjudicators and frozen product signals.
- Accept the measured form of CH-5: mobile navigation, overflow containment, route focus and announcements, state semantics, nested interactions, and search retrieval require finite verification and correction where reproduced.
- Accept CH-6: artist-first emphasis already exists in the shipped hierarchy and must be explicitly ratified, revised, or preserved provisionally rather than described as absent.
- Accept CH-7: the visible search placeholder is already correct; accessible naming, result behavior, dismissal, and focus return are the relevant obligations.
- Accept CH-8: current onboarding delivery is stratified, not response-adaptive. PIG-001 should revise the claim; true adaptivity remains a later, separately specified objective.
- Accept CH-9 as resolved by D-011 and D-012: the message-envelope repair, task recovery, Coordinator registration, and effa805 rebaseline are now recorded.
- Accept the principle of CH-10: rollback and deployment evidence need an exact baseline, restoration condition, and cache/versioning treatment. The stale 3c2e9fa anchor is superseded by the adopted effa805 baseline.
- Accept CH-11 and CH-12 as bounded scope candidates where Claude confirms reproduction and maps each included issue to a criterion.
- Accept the Workstream H split between verification and bounded correction.
- Accept Claude's liaison packet as-is: its audit of the pre-retransmission challenge remains accurate for that artifact, and D-011/D-012 preserve the later protocol repair and rebaseline episode.

**Disputed points:**
- The challenge's 783-image statement must not be retained as the exact current rendered or reachable surface. It counted stored references at an older anchor and omitted other public image surfaces. Final Synthesis must produce a current exact inventory of unique assets and public references, separated by reachability and surface.
- The fetch pipeline does not presently request Commons extmetadata; the claim that it already receives and discards that metadata is withdrawn.
- Current Matisse and Kahlo exposure cannot be inferred from cross-store presence alone. Suppressed branches, exact-work mismatches, public prerendered metadata, and other surfaces must be inventoried before exposure is asserted.
- Artist death year, a Commons host, or generic platform attribution is not legal clearance. The user may accept documented residual product risk but may not determine the law.
- A beforeunload warning or restart warning alone does not satisfy recoverability when onboarding progress is destroyed. The user must retain exact progress or receive a truthful, user-controlled recoverable continuation.
- Per-type search quotas are an implementation prescription, not a theory requirement. The requirement is that frozen desired-result fixtures prevent exact or meaningful entity matches from being starved by incidental matches or type ordering.
- The fourteen-unit implementation plan is not complete as a specification because it omits or under-specifies the full public-asset inventory, rights disposition, constellation keyboard access, cache/versioning consistency, and privacy treatment.
- Release positioning is not a binary choice between editorial discovery and historical reference. Pigment may lead with Atlas-backed editorial discovery and accountless Taste while still carrying proportional factual and rights obligations for every public claim and asset.
- Deck-warning repair cannot be pre-authorized as two re-scores. Any data correction must be justified on editorial merits; otherwise a dated owner exception must state the warning, evidence, user impact, and expiry or review condition.

**Rationale:** Claude's challenge materially improves the theory by exposing silent Passport replacement, interruption loss, false or untestable gates, and measured access defects. Revision is therefore warranted. The challenge also contains stale counts, an overstated image-surface claim, a false extmetadata premise, an insufficient warning-only recovery proposal, and several implementation choices presented as product requirements. Correcting those points preserves the constitutional division: ChatGPT states outcomes, boundaries, and evidence thresholds; Claude selects buildable methods and supplies implementation evidence. The revised scope keeps PIG-001 finite while refusing to convert editorial positioning into permission to overstate facts, rights, privacy, accessibility, or product behavior.

**Evidence:
- protocol/tasks/PIG-001/messages/001-theory_brief.json
- protocol/tasks/PIG-001/messages/002-challenge.json
- protocol/tasks/PIG-001/unrouted/challenge-adaptation-report.md
- protocol/tasks/PIG-001/unrouted/challenge-analysis-caravaggio.md
- protocol/tasks/PIG-001/unrouted/ux-requirements.md
- protocol/tasks/PIG-001/unrouted/browser-evidence.md
- protocol/tasks/PIG-001/unrouted/data-integrity-report.md
- protocol/tasks/PIG-001/unrouted/feasibility-assessment.md
- protocol/tasks/PIG-001/unrouted/decision-record.md
- protocol/tasks/PIG-001/unrouted/rebaseline-effa805.md
- protocol/tasks/PIG-001/analyses/001-theory-liaison.json
- protocol/tasks/PIG-001/analyses/002-synthesis-liaison.json
- PIGMENT.md
- docs/ADMIRE_SPEC.md
- docs/TASTE_MATH.md
- docs/STYLE_GUIDE.md
- docs/ARTWORK_SCHEMA.md

**Disposition:** `theory_revision` -> `final_synthesis`

## 2: final_synthesis

**Summary:** FINAL SYNTHESIS: Taste Continuity and Access Stabilization. All nine revision disputes accepted with verified dispositions (extmetadata premise confirmed false at file level; 799-asset inventory frozen; checkpoint persistence replaces warning-only recovery). The revision's 29 acceptance criteria are carried verbatim. Fresh Implementation Lead assessment confirms the complete effa805 scope buildable in 22 units with zero technical blockers; five decision-gated items are routed to their designated deciders without blocking the isolated build.

**Accepted points:**
- user_outcome: A first-time visitor can discover art, admire works, form and recover a local Taste Passport, understand how actions affect it, and continue through Pigment's connected Atlas without silent state loss, inaccessible dead ends, misleading evidence claims, or unexplained transitions.
- information_architecture: The existing 24-route hash IA, multi-door homepage, and all current entry doors are preserved unchanged this release; the shipped artist-first emphasis is retained provisionally and labeled unratified; no route, ID, slug, or stored-field renames.
- principal_flow: The five frozen journeys (known-artist, artwork-led, editorial, personal Taste loop with five interruption checkpoints and exact-checkpoint recovery, Explore loop) per unrouted/ux-requirements.md under the revision's checkpoint and conflict-handling criteria.
- All nine revision disputes are accepted; dispositions with verification evidence are in the proposal.
- The revision's binding release constraints are adopted unchanged, including conservative release language and the prohibition on tuning taste data to silence validator warnings.
- The revision's 29 acceptance criteria are adopted verbatim as this synthesis's acceptance_criteria.
- Matisse (claude-visual-director) is named product adjudicator for AC23.
- Claude's liaison packet acceptance (revision accepted point 13) is noted with thanks; D-011's real-parser rule remains standing.

**Disputed points:**
- None recorded.

**Rationale:** The challenge exposed real blockers; the revision corrected real overstatements in the challenge; both corrections are recorded rather than smoothed over (D-013). What remains is finite: 29 objectively testable criteria, frozen inventories measured against effa805 rather than remembered, a 22-unit reversible plan with fresh feasibility confirmation, and five decision points routed to the people entitled to decide them. Convergence is recommended because every element of the Convergence Standard is now satisfied: outcome explicit, assumptions documented, critical objections resolved or recorded, IA and flows coherent, feasibility confirmed with evidence, criteria testable, deviations visible, no hidden critical risk, and remaining disagreements are decision-routing rather than substance.

**Evidence:
- feasibility-confirmed: Implementation Lead r2 assessment, protocol/tasks/PIG-001/evidence/feasibility-assessment-r2.md (FEASIBILITY CONFIRMED, 29/29 criteria classified, 0 infeasible)
- protocol/tasks/PIG-001/evidence/asset-inventory-effa805.md (frozen: 799 unique assets by surface and reachability)
- protocol/tasks/PIG-001/evidence/asset-inventory-effa805.json (per-URL detail)
- tools/fetch_artworks.py:49 and tools/audit_artworks.py:99 (iiprop=url|mime only - extmetadata dispute verified)
- protocol/tasks/PIG-001/unrouted/rebaseline-effa805.md (validator snapshot: 247/75/317/75, two deck warnings, all references valid)
- protocol/tasks/PIG-001/unrouted/ux-requirements.md (frozen route/control/journey/query inventories)
- protocol/tasks/PIG-001/unrouted/browser-evidence.md (measured U1/U2)
- protocol/tasks/PIG-001/messages/003-revision.json (the revision this synthesis dispositions)
- protocol/tasks/PIG-001/unrouted/decision-record.md (D-001..D-013 manual ledger)

**Disposition:** `final_synthesis` -> `awaiting_build_approval`

## 2: specification

**Summary:** The converged synthesis is frozen and authorized for isolated implementation.

**Accepted points:**
- user_outcome: A first-time visitor can discover art, admire works, form and recover a local Taste Passport, understand how actions affect it, and continue through Pigment's connected Atlas without silent state loss, inaccessible dead ends, misleading evidence claims, or unexplained transitions.
- information_architecture: The existing 24-route hash IA, multi-door homepage, and all current entry doors are preserved unchanged this release; the shipped artist-first emphasis is retained provisionally and labeled unratified; no route, ID, slug, or stored-field renames.
- principal_flow: The five frozen journeys (known-artist, artwork-led, editorial, personal Taste loop with five interruption checkpoints and exact-checkpoint recovery, Explore loop) per unrouted/ux-requirements.md under the revision's checkpoint and conflict-handling criteria.
- All nine revision disputes are accepted; dispositions with verification evidence are in the proposal.
- The revision's binding release constraints are adopted unchanged, including conservative release language and the prohibition on tuning taste data to silence validator warnings.
- The revision's 29 acceptance criteria are adopted verbatim as this synthesis's acceptance_criteria.
- Matisse (claude-visual-director) is named product adjudicator for AC23.
- Claude's liaison packet acceptance (revision accepted point 13) is noted with thanks; D-011's real-parser rule remains standing.

**Disputed points:**
- None recorded.

**Rationale:** The challenge exposed real blockers; the revision corrected real overstatements in the challenge; both corrections are recorded rather than smoothed over (D-013). What remains is finite: 29 objectively testable criteria, frozen inventories measured against effa805 rather than remembered, a 22-unit reversible plan with fresh feasibility confirmation, and five decision points routed to the people entitled to decide them. Convergence is recommended because every element of the Convergence Standard is now satisfied: outcome explicit, assumptions documented, critical objections resolved or recorded, IA and flows coherent, feasibility confirmed with evidence, criteria testable, deviations visible, no hidden critical risk, and remaining disagreements are decision-routing rather than substance.

**Evidence:
- feasibility-confirmed: Implementation Lead r2 assessment, protocol/tasks/PIG-001/evidence/feasibility-assessment-r2.md (FEASIBILITY CONFIRMED, 29/29 criteria classified, 0 infeasible)
- protocol/tasks/PIG-001/evidence/asset-inventory-effa805.md (frozen: 799 unique assets by surface and reachability)
- protocol/tasks/PIG-001/evidence/asset-inventory-effa805.json (per-URL detail)
- tools/fetch_artworks.py:49 and tools/audit_artworks.py:99 (iiprop=url|mime only - extmetadata dispute verified)
- protocol/tasks/PIG-001/unrouted/rebaseline-effa805.md (validator snapshot: 247/75/317/75, two deck warnings, all references valid)
- protocol/tasks/PIG-001/unrouted/ux-requirements.md (frozen route/control/journey/query inventories)
- protocol/tasks/PIG-001/unrouted/browser-evidence.md (measured U1/U2)
- protocol/tasks/PIG-001/messages/003-revision.json (the revision this synthesis dispositions)
- protocol/tasks/PIG-001/unrouted/decision-record.md (D-001..D-013 manual ledger)
- frozen-sha256:70de6a712bff204b1d9f12e6bfcc8a1087a86cfdd288edc741826acb9f9b0166

**Disposition:** `approved_for_build` -> `approved_for_build`
