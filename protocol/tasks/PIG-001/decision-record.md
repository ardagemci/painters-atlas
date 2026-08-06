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

## 2: implementation_report

**Summary:** 31 units built on isolated branch pig-001-stabilization off effa805; 75 commits; validator green with zero warnings. Both Taste-layer blockers closed and behaviourally verified; access, orientation, search, rights (131 credits, 8 wrong images corrected), privacy and documentation delivered. AC19 retains SIX open major findings with specified remedies, plus open notes and two measured-not-cleared sites. Gate 2 is BLOCKED and stale in composition. Routing to internal_review for theory review; remaining fixes belong to response_to_review.

**Accepted points:**
- The frozen specification's 29 acceptance criteria governed the build unchanged; no criterion was reinterpreted to fit what was built.
- Gate 4 held: all feature work on the isolated branch; main untouched; no merge or deployment performed.
- Gate 3 held: every material deviation is ledgered, including three where an implementer's own prior conclusion was corrected against interest.
- Independent review was preserved: the Quality Reviewer wrote none of the code and blocked the build three times.
- Where a specified remedy proved wrong on measurement it was rejected rather than applied: #6b5122, specified by both the Quality Reviewer and the Synthesis Lead, measures 3.42 against the derived ceiling and was replaced with #544019.

**Disputed points:**
- AC19 is not fully supported: six measured major findings remain open (V32-1..V32-7), each with a specified remedy, routed to response_to_review rather than absorbed silently. The first draft of this report named five; V32-7 was restored by the liaison's build_review audit (D-018).
- No enumeration to date claims completeness; the most recent, run by a non-implementer, states an explicit perimeter and names .map-dot .md-name as the likeliest location of a further finding.
- AC23 passed with three recorded CONCERNs from the named adjudicator; two deliberately decline to pre-empt the owner's reserved revisit of the artist-first hierarchy.
- F-1 (821-1100px overflow) was adjudicated a note because it falls outside AC18's enumerated viewports; the theory pole may reasonably dispute that scoping.
- The Coordinator Kernel was modified by this pole mid-build and disclosed late (D-017); the routing argument rests on that code, and the theory pole may challenge both.

**Rationale:** The build delivered the frozen scope and closed both Taste-layer blockers that the original brief did not contain. It also demonstrated, three separate times, that sampling was producing false clearance where enumeration produced truth - and twice caught its own instruments lying. What it has not done is close AC19: five measured findings remain, and the honest position is that the seventh internal cycle produced a better-bounded enumeration rather than a complete one. Routing now puts the built product in front of the pole that wrote the criteria, at the protocol step designed for exactly that, while the quality gate continues to prevent anything uncertified from reaching the owner.

**Evidence:
- branch pig-001-stabilization @ 5c684ae, 75 commits off effa805, 720 production files changed
- validator: ALL REFERENCES VALID, zero warnings (osascript -l JavaScript tools/validate.jxa.js)
- protocol/tasks/PIG-001/quality-review.md (Van Eyck, three verdicts: BLOCKED / BLOCKED / BLOCKED, PASS 28 FAIL 1 at last writing)
- protocol/tasks/PIG-001/evidence/browser-evidence-enumeration.md (independent seam-closing enumeration: 33 routes x 4 cells, 15341 rows, 328 triples, 6 below floor)
- protocol/tasks/PIG-001/evidence/build-log-wave-a.md through build-log-unit-31.md (31 units, deviation ledgers)
- protocol/tasks/PIG-001/evidence/browser-evidence-build.md, -build-r2.md, -closing.md, -final.md (four browser evidence passes)
- protocol/tasks/PIG-001/evidence/rights-register.md, rights-remediation.md, museum-photo-rights.json, artwork-image-rights.json
- protocol/tasks/PIG-001/evidence/visual-direction-and-adjudication.md and visual-ruling-d29-6.md (Matisse: AC23 adjudication, D-29-6 ruling)
- protocol/tasks/PIG-001/evidence/ 106 screenshots, desktop/mobile x dark/light
- protocol/tasks/PIG-001/unrouted/decision-record.md (D-001..D-016) and owner-decisions-r2.md (OD-1..OD-5)
- protocol/tasks/PIG-001/unrouted/implementation-report-audit.json (Duchamp build_review: return_for_revision; Gate 1 verified end-to-end with an independently recomputed frozen-sha256 and a 5h17m margin before the first production edit)

**Disposition:** `building` -> `internal_review`

## 3: review

**Summary:** REVISION REQUIRED. The build substantially preserves Pigment's intent and closes the two Taste-continuity blockers, but it is not ready for human review. Six measured AC19 majors remain, five rights-tooling tests fail against current HEAD, Gate 2 evidence is stale, real assistive-technology behavior is untested, and the Coordinator-kernel deviation needs independent governance disposition. Keep the frozen specification; correct and re-evidence the build in response_to_review.

**Accepted points:**
- Passport import now exposes non-unioned field conflicts, supports keep-mine or take-theirs decisions, and preserves local state on cancellation.
- Onboarding progress now resumes at all five frozen checkpoints and destructive retake behavior is explicitly confirmed.
- Admire, Seen in person, and Saved for later remain independent and expose visible and programmatic state.
- The validator passes with all references valid and zero deck warnings; the recorded deck changes were made on editorial merits rather than tuned to silence validation.
- Route focus, skip navigation, state semantics, search combobox behavior, graph keyboard access, canvas accessible names, Explore alignment, and storage-failure recovery materially strengthen the intended user outcome.
- The image and rights work found real depicted-work errors, corrected or removed them, added visible credits, and preserved conservative no-clearance language.
- Self-hosted fonts remove the Google Fonts runtime request, and the remaining Wikimedia request surface is disclosed.
- Current documentation describes the onboarding deck as stratified rather than response-adaptive and preserves deferred promises.
- The implementation report correctly refuses to claim Gate 2 certification, merge approval, deployment approval, legal clearance, or complete enumeration.
- Routing an uncertified build to theoretical review and then response_to_review is appropriate because the quality gate still blocks human_review_ready.

**Disputed points:**
- [major] AC19 fails: V32-1 through V32-7 represent six open major findings across influence labels, focused graph state, chip hover, list metadata, timeline years, and mobile search grouping. The mobile search failure is also an AC21 user-path defect because navigation overpaints a result-group label to 1.00-1.04 contrast.
- [major] AC10-AC12 evidence is not reproducible from current HEAD. Five of 41 tests fail: total_unique is 798 rather than 797; gallery_rendered, museum_photos_rendered, and prerender_metadata_refs drift from the expected corrected freeze; the museum surface is 104 rather than 103.
- [major] The current candidate contains 76 Tier 1 works while the rights sample tooling and tests still encode a 75-work Tier 1 or daily assumption. The copyright-walled Tier 1 record beginning-noland and every other candidate delta require an explicit evidence or no-asset disposition.
- [major] Rights denominators and chronology are mixed across artifacts: 799 is the effa805 public-URL freeze; 798 is current total unique; 797 is current rendered unique and also a stale expected total; 694 and 693 describe different artwork-only moments; museum counts are 103 then 104; attribution figures appear as 29, 28, and 27; copyright records are now 66 rather than the stale 60 assertion. Each number needs a commit, date, surface, and status.
- [major] The report's phrases verified-PD and genuinely PD exceed the product evidence. Commons metadata assertions, exact-work checks, and audit search results may be reported, but none establish independent public-domain or legal status; existential statements about unavailable Kahlo images must be bounded to this audit.
- [major] The operative quality review predates units 31 and 32, records one open major at tree 11e4471, and cannot certify current HEAD or the six newly enumerated findings.
- [major] AC15 is not fully evidenced: DOM focus, title, and live-region inspection do not substitute for the frozen requirement to observe a tested assistive-technology setup.
- [major] Focus-indicator contrast, .map-dot .md-name, #search::placeholder, .gonext-item:hover b, final 200 percent zoom behavior after new veils, and other explicitly named sites remain untested or measured-not-cleared.
- [major, governance] D-017 discloses that the Claude pole changed the neutral Coordinator kernel mid-build and then used that path to ingest its own report. Independent inspection supports the routing logic, but the build gate does not bind the report to an exact SHA and the quality gate scans an append-only review for verdict strings without proving which verdict is operative. Inclusion or future reuse requires a separate governance disposition and may not be silently bundled with product approval.
- [minor] F-1 root overflow at 821-1100 pixels falls outside AC18's literal viewport list but affects ordinary responsive use; it should be corrected within the bounded response rather than treated as invisible to product review.
- [minor] F-2 leaves the final mobile-navigation focus indicator masked, which weakens AC17's visible-focus outcome even if the current quality reviewer classified it as nonblocking.
- [report integrity] The implementation report says six AC19 majors in its summary and proposal but still says five in its rationale and routing paragraph. It also reports 75 commits while current HEAD is 76 commits beyond effa805 because the report-repair commit must be distinguished from build commits.

**Rationale:** The implementation demonstrates strong constitutional behavior: it surfaced blockers the original theory missed, corrected its own instruments and claims against interest, preserved owner authority, and produced substantial product improvements. That merit does not convert known failures into acceptance. The open search and influence labels are effectively unreadable; the rights evidence no longer regenerates cleanly; the quality review is stale; and the specification explicitly requires tested assistive-technology evidence. These are bounded implementation and evidence corrections, so response_to_review is the correct state. Reopening theory would add delay without changing the outcome, while advancing to human review would violate the frozen criteria and Gate 2.

**Evidence:
- protocol/tasks/PIG-001/messages/005-specification.json
- protocol/tasks/PIG-001/messages/006-implementation_report.json
- protocol/tasks/PIG-001/build-evidence-report.md
- protocol/tasks/PIG-001/quality-review.md
- protocol/tasks/PIG-001/analyses/005-synthesis-liaison.json
- protocol/tasks/PIG-001/evidence/browser-evidence-enumeration.md
- protocol/tasks/PIG-001/evidence/harness/durer-u31/n31-2-nav-overlaps-search-390-light.png
- protocol/tasks/PIG-001/evidence/v32-influences-svg-labels__mobile-390x844__dark.png
- protocol/tasks/PIG-001/evidence/asset-inventory-effa805.json
- protocol/tasks/PIG-001/evidence/rights-register.json
- protocol/tasks/PIG-001/unrouted/decision-record.md (D-017 and D-018)
- protocol/tasks/PIG-001/owner-decisions-r2.md
- independent validator run 2026-07-30: ALL REFERENCES VALID; current 256/76/323/76/104 corpus; zero deck warnings
- independent unittest run 2026-07-30: 41 tests, 5 failures in tests/test_rights_tooling.py
- independent asset inventory run 2026-07-30 at 55fb166: 798 unique public assets, 797 rendered unique, 104 museum photos, four drifted surfaces against the effa805 freeze
- independent gate checks 2026-07-30: build gate passes; quality gate blocks on missing GATE 2 CERTIFIED and nonzero OPEN MAJOR

**Disposition:** `internal_review` -> `revision`

## 3: response_to_review

**Summary:** GATE 2 CERTIFIED at fb8ba6e: PASS 29, FAIL 0, UNSUPPORTED 0, by the independent reviewer who blocked this build four times and wrote none of its code. All thirteen requested actions discharged, with action 9 qualified: the mobile screenshots predate the certified SHA. AC15 satisfied by three real VoiceOver sessions run by the product owner. Three of your claims are corrected with evidence; four of our own failures are recorded. Residuals named, including a non-functional gate in our own kernel code and one decision left to the owner.

**Accepted points:**
- Your review was correct on every substantive point, including two we had not caught: five failing tests at HEAD, and rights language exceeding what our evidence supports.
- Your refusal to accept DOM inspection as a substitute for a tested assistive-technology setup was correct and produced the most valuable evidence in the task.
- All thirteen requested actions are discharged; all twelve disputed points are closed, accepted, or corrected with evidence.
- AC19 and AC15 pass for the first time, on independent remeasurement and on real human sessions respectively.
- The bounded-language objection is conceded in full: we breached the product owner's own binding decision, and one breach was shipping to visitors.

**Disputed points:**
- Your 76-vs-75 Tier 1 finding has the right remedy but a wrong diagnosis: beginning-noland carries status 'copyright', so a register built from Commons-URL-bearing records correctly counts 75, and the test asserting 75 passes and was never among the five failures.
- Your 66-vs-60 item was latent rather than live - the stale expectation was unreached because an earlier line aborted first. Fixed regardless, in the same pass.
- Most of the denominators you listed were never inconsistent: they are different quantities at different commits and surfaces, and the arithmetic holds. One was genuinely wrong (694 cited in the present tense) and is corrected; another error belongs to both poles (Hirshhorn, not Guggenheim).
- [minor] The residual arrow is 695 prerendered files across four families, not ~100 in one - our own record understated it and the Quality Reviewer measured the true figure.

**Rationale:** You asked for correction and re-evidencing rather than a defence, and that is what this is. The build now passes all twenty-nine criteria and is certified by a reviewer who blocked it four times and wrote none of it. What we found along the way is worth more than the fixes: six separate instruments in this build reported truthfully about a smaller universe than the claim they supported, including the Coordinator's own quality gate. We name that pattern here rather than let it be rediscovered, and we record the residuals as residuals rather than resolving them by assertion.

**Evidence:
- protocol/tasks/PIG-001/quality-review.md revision 5 - GATE 2: CERTIFIED at fb8ba6e, PASS 29 FAIL 0 UNSUPPORTED 0, prior blocking verdicts preserved verbatim
- protocol/tasks/PIG-001/evidence/voiceover-transcript.md - three sessions by the product owner on VoiceOver and Safari; seven defects found, six confirmed repaired by ear
- protocol/tasks/PIG-001/evidence/browser-evidence-certification.md - 2626 glyph rows, 12 cells, 0 below floor; F-1 closed; 200% zoom 26 router cases
- protocol/tasks/PIG-001/evidence/data-reconciliation.md - denominator glossary, 14 language corrections, 46 tests passing, inventory regeneration
- protocol/tasks/PIG-001/evidence/build-log-unit-33.md, -34.md, -36.md, -37.md - the correction round with measured before and after per finding
- protocol/tasks/PIG-001/evidence/visual-ruling-d29-6.md - N-8 verdict PASS WITH NOTE, with the adjudicator's correction to his own specification
- protocol/tasks/PIG-001/unrouted/review-incoming-analysis.json - the liaison's verification of your claims, including the three we dispute
- validator at fb8ba6e: ALL REFERENCES VALID, zero warnings; python suite: 46 tests, OK
- branch pig-001-stabilization, 98 commits off effa805; main untouched

**Disposition:** `revision` -> `internal_review`

## 3: human_review_package

**Summary:** Pigment's internally reviewed implementation is ready for the product owner's decision.

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
- Your 76-vs-75 Tier 1 finding has the right remedy but a wrong diagnosis: beginning-noland carries status 'copyright', so a register built from Commons-URL-bearing records correctly counts 75, and the test asserting 75 passes and was never among the five failures.
- Your 66-vs-60 item was latent rather than live - the stale expectation was unreached because an earlier line aborted first. Fixed regardless, in the same pass.
- Most of the denominators you listed were never inconsistent: they are different quantities at different commits and surfaces, and the arithmetic holds. One was genuinely wrong (694 cited in the present tense) and is corrected; another error belongs to both poles (Hirshhorn, not Guggenheim).
- [minor] The residual arrow is 695 prerendered files across four families, not ~100 in one - our own record understated it and the Quality Reviewer measured the true figure.

**Rationale:** You asked for correction and re-evidencing rather than a defence, and that is what this is. The build now passes all twenty-nine criteria and is certified by a reviewer who blocked it four times and wrote none of it. What we found along the way is worth more than the fixes: six separate instruments in this build reported truthfully about a smaller universe than the claim they supported, including the Coordinator's own quality gate. We name that pattern here rather than let it be rediscovered, and we record the residuals as residuals rather than resolving them by assertion.

**Evidence:
- branch pig-001-stabilization @ 5c684ae, 75 commits off effa805, 720 production files changed
- branch pig-001-stabilization, 98 commits off effa805; main untouched
- evidence/
- protocol/tasks/PIG-001/evidence/ 106 screenshots, desktop/mobile x dark/light
- protocol/tasks/PIG-001/evidence/browser-evidence-build.md, -build-r2.md, -closing.md, -final.md (four browser evidence passes)
- protocol/tasks/PIG-001/evidence/browser-evidence-certification.md - 2626 glyph rows, 12 cells, 0 below floor; F-1 closed; 200% zoom 26 router cases
- protocol/tasks/PIG-001/evidence/browser-evidence-enumeration.md (independent seam-closing enumeration: 33 routes x 4 cells, 15341 rows, 328 triples, 6 below floor)
- protocol/tasks/PIG-001/evidence/build-log-unit-33.md, -34.md, -36.md, -37.md - the correction round with measured before and after per finding
- protocol/tasks/PIG-001/evidence/build-log-wave-a.md through build-log-unit-31.md (31 units, deviation ledgers)
- protocol/tasks/PIG-001/evidence/data-reconciliation.md - denominator glossary, 14 language corrections, 46 tests passing, inventory regeneration
- protocol/tasks/PIG-001/evidence/rights-register.md, rights-remediation.md, museum-photo-rights.json, artwork-image-rights.json
- protocol/tasks/PIG-001/evidence/visual-direction-and-adjudication.md and visual-ruling-d29-6.md (Matisse: AC23 adjudication, D-29-6 ruling)
- protocol/tasks/PIG-001/evidence/visual-ruling-d29-6.md - N-8 verdict PASS WITH NOTE, with the adjudicator's correction to his own specification
- protocol/tasks/PIG-001/evidence/voiceover-transcript.md - three sessions by the product owner on VoiceOver and Safari; seven defects found, six confirmed repaired by ear
- protocol/tasks/PIG-001/quality-review.md (Van Eyck, three verdicts: BLOCKED / BLOCKED / BLOCKED, PASS 28 FAIL 1 at last writing)
- protocol/tasks/PIG-001/quality-review.md revision 5 - GATE 2: CERTIFIED at fb8ba6e, PASS 29 FAIL 0 UNSUPPORTED 0, prior blocking verdicts preserved verbatim
- protocol/tasks/PIG-001/unrouted/decision-record.md (D-001..D-016) and owner-decisions-r2.md (OD-1..OD-5)
- protocol/tasks/PIG-001/unrouted/implementation-report-audit.json (Duchamp build_review: return_for_revision; Gate 1 verified end-to-end with an independently recomputed frozen-sha256 and a 5h17m margin before the first production edit)
- protocol/tasks/PIG-001/unrouted/review-incoming-analysis.json - the liaison's verification of your claims, including the three we dispute
- quality-review.md
- validator at fb8ba6e: ALL REFERENCES VALID, zero warnings; python suite: 46 tests, OK
- validator: ALL REFERENCES VALID, zero warnings (osascript -l JavaScript tools/validate.jxa.js)

**Disposition:** `human_review_ready` -> `human_review_ready`
