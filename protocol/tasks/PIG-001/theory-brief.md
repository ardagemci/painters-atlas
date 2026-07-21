---
task_id: THEORY-001
project: pigment
round: 1
sender: pigment-theory-team
recipient: claude-team
message_type: final_synthesis_and_execution_handoff
workflow_state: claude_analysis
source_reports:
  - IVO_001.md
  - MIRA_001.md
  - SOREN_001.md
  - NIKO_001.md
  - ELARA_001.md
  - ARGUS_001.md
summary: >-
  Pigment is a coherent Atlas-first product with a materially implemented accountless Taste layer.
  The immediate objective is a bounded stabilization and evidence pass, not a broad redesign.
  Claude must verify the complete first-user Taste journey, persistence and recovery, accessibility,
  responsive containment, search and route behavior, documentation consistency, and a minimum
  provenance/rights evidence baseline before returning the build for human review.
assumptions:
  - The target public deployment remains https://ardagemci.github.io/painters-atlas/#/.
  - Atlas 2.0 and the Phase 1.5 accountless Taste Passport remain the accepted product foundation.
  - Admire remains the only v1 positive artwork taste signal; Seen in person and Saved for later remain independent states.
  - Stable routes, IDs, slugs, storage fields, and constitutionally established product terms are preserved unless a frozen specification explicitly changes them.
  - The current multi-door homepage remains the rollback baseline while hierarchy alternatives are unproven.
accepted_points:
  - Pigment's north star is to help people discover, understand, and express their taste in art.
  - Atlas is the durable architectural core; Taste is the personal continuity layer; Daily is a low-choice entrance whose habit value is unproven.
  - The editorial visual identity, relationship-rich detail pages, timeline, search, Lists, and multiple legitimate entrances should be preserved.
  - The current release should prioritize orientation, state clarity, recoverability, first-user continuity, and evidence integrity over feature expansion.
  - Deployment readiness is conditional, not unconditional.
disputed_points:
  - Whether Taste belongs in persistent global navigation now or in a later Atlas Coherence Pass.
  - Whether the top-level navigation should be regrouped immediately or only after first-time and expert retrieval testing.
  - Whether Start with an artist should become the visibly recommended first action in the current release.
  - Whether Eras and Nations need relabeling or only clearer definitions and uncertainty language.
  - Whether the current public build may be described as a historical reference before claim-level provenance and image-rights coverage are established.
proposal: >-
  Advance to Claude analysis under one frozen stabilization objective. Treat first-user Taste integrity,
  accessibility-critical state and orientation, mobile discoverability, responsive containment,
  documentation consistency, runtime regression, and a minimum provenance/rights audit as the active
  evidence package. Keep large navigation restructuring, Taste-first acquisition, Daily-first identity,
  new accounts/social features, and full taxonomy redesign outside the release scope unless Claude proves
  that a specific issue is release-blocking.
confidence: >-
  High for the observed product inventory, route and promise mismatches, mobile-navigation concealment,
  state-communication defects, strong editorial/relational identity, and need for conditional release gates.
  Medium for the preferred opening hierarchy and global Taste placement. Low for behavioral impact,
  retention, screen-reader performance, complete historical accuracy, and recurrence until tested.
next_state: claude_analysis
created_at: 2026-07-21T00:00:00+03:00
---

# THEORY_001 — Pigment Final Theory Synthesis

## 0. Instruction to Claude

Treat this document as the consolidated theory-team handoff. It supersedes no governing constitution, approved implementation specification, or product-owner decision. It does not authorize production edits or deployment by itself.

Claude's first output must be a neutral feasibility and scope classification that:

1. restates the frozen objective;
2. classifies every requested item as **release blocker**, **low-risk inclusion**, **follow-up backlog**, or **product-owner decision**;
3. identifies contradictions between the current build, documentation, and this synthesis;
4. proposes the smallest reversible implementation plan;
5. states the exact evidence required before `human_review_ready`;
6. preserves a rollback path to the current multi-door baseline.

No unrecorded adaptation may silently change product intent, terminology, route structure, stored Taste data, or historical claims.

---

## 1. Consolidated decision

Pigment has crossed the threshold from a painter reference project into a credible **taste atlas**. The product already contains three mutually reinforcing layers:

- **Atlas — durable knowledge and traversal:** artists, artworks, movements, techniques, eras, nations, museums, Lists, search, timeline, influence relationships, and canonical detail pages.
- **Taste — personal continuity:** Palette onboarding, Admire, a local Taste Passport, provisional Pigment Personas, discovery rings, export/import, and independent Seen in person and Saved for later states.
- **Daily and editorial — low-choice entry:** Painting of the Day and curated Lists make the corpus approachable and memorable.

The theory team does **not** recommend a broad redesign before the next release. The active objective is:

> Let a first-time visitor discover art, admire works, form and recover a local Taste Passport, understand how their actions affect it, and recognize Pigment as an atlas of relationships in art.

The release posture is **conditional stabilization**, followed by a separately authorized Atlas Coherence Pass and reversible hierarchy experiments.

---

## 2. Product direction frozen for this round

### 2.1 Core hierarchy

The accepted strategic hierarchy is:

1. **Atlas-first architecture** — retain as the durable core.
2. **Taste as personal continuity** — strengthen clarity, persistence, recovery, and trust without gating knowledge.
3. **Daily as a low-choice entrance** — preserve, but do not promote to the product identity until voluntary recurrence is demonstrated.

Taste-first remains the strongest acquisition-message challenger, not the default architecture. A Daily-first publication identity remains reserved. A pure reference-atlas simplification and forced Taste onboarding are rejected.

### 2.2 Opening experience

Preserve the current multi-door baseline and Pigment's editorial atmosphere. For the current release, Claude may improve hierarchy and clarity but must not silently choose a new product identity.

The preferred design direction is:

> Preserve the atmosphere. Strengthen orientation. Make relationship—not decoration—the signature visual behavior of Pigment.

The opening experience should communicate:

1. what Pigment is;
2. the recommended or clearest first action;
3. evidence of a meaningful relationship in the atlas;
4. secondary routes that remain easy to discover.

SOREN proposes **Start with an artist** as the recommended first-time route. This is not frozen as a production change until MIRA or the product owner confirms it, or Claude supplies evidence for a different hierarchy.

### 2.3 Visual identity to preserve

Preserve:

- the dark, spatial, editorial atmosphere;
- expressive display typography paired with functional readable text;
- muted painterly color and artwork-led chromatic variation;
- a contemplative tempo rather than dashboard urgency;
- authored interpretation and compact editorial wit;
- generous detail-page context and meaningful onward paths;
- the timeline and cross-entity search as major product strengths.

Do not reduce relationship-led design to ornamental lines, generic network imagery, cinematic delay, or visually prominent systems without informational consequence.

---

## 3. Evidence baseline

### 3.1 Dated implementation snapshot

The latest validator snapshot, dated 20 July 2026, reported:

```text
app.js syntax: OK
artists: 246
catalog artworks: 315
Tier 1 artworks: 73
Tier 1 artist arcs: 36
movements: 74
techniques: 39
eras: 8
nations: 37
influence edges: 225
venues: 115
museum notes: 103
personas: 15
lists: 12
all references: valid
```

The validator also reported two onboarding-deck warnings:

```text
deck pool: fewer than 2 works with E <= -40
deck pool: empty F x D quadrant 1,-1
```

These counts are dated observations of current scope, not evidence of completeness, representativeness, accuracy, or market leadership.

### 3.2 Observed strengths

Across the six reports, the strongest observed capabilities are:

- connected traversal between artists, works, movements, techniques, eras, nations, museums, and Lists;
- strong artist, artwork, movement, museum, and editorial detail journeys;
- a functional grand timeline with useful filtering and direct profile transitions;
- cross-entity search with typed results and an explicit no-match state;
- contextual not-found recovery through the existing “Blank canvas” pattern;
- a coherent and distinctive editorial identity;
- meaningful personal verbs: Admire, Seen in person, and Saved for later;
- a materially implemented local Taste Passport with onboarding, discovery, export, import, and reset surfaces.

### 3.3 Observed gaps and bounded unknowns

Directly observed or strongly supported gaps include:

- the mobile primary navigation conceals most destinations behind an unannounced horizontal gesture;
- route changes do not consistently establish concise focus and current-location orientation;
- selected filters, modes, palette tones, and saved actions can communicate state only visually;
- the Start with an artist surface contains competing nested or adjacent actions whose boundaries are unclear;
- search lacks a complete dynamic-results contract and may rank incidental substrings too highly;
- the homepage Explore promise names four instruments while the Explore hub foregrounds two;
- Taste is central on the homepage and in product theory but is not consistently represented in persistent navigation;
- root-level horizontal overflow was directly measured on sampled desktop and mobile routes;
- historical and influence claims on a sampled artist profile lacked traceable sources;
- generic Wikimedia Commons attribution does not establish item-level image provenance, license, or rights status;
- documentation counts appear stale relative to the validator;
- onboarding interruption, correction, persistence across sessions, complete assistive-technology behavior, both-theme contrast, reduced motion, and full-corpus accuracy remain incompletely tested.

A clean sampled console is not evidence of complete runtime stability. Absence of source proof is not proof of historical falsity or copyright infringement. Accessibility risks that were not measured remain hypotheses until tested.

---

## 4. Scope model

### 4.1 Active release scope — stabilization and evidence

The active release scope is the smallest coherent set needed to validate the existing promise:

1. onboarding-deck integrity and warning disposition;
2. complete first-user Taste journey;
3. Taste Passport persistence, update, export, share/import, merge, and reset;
4. independent persistence of Admire, Seen in person, and Saved for later;
5. onboarding interruption, correction, restart, and recovery behavior;
6. route-change orientation, current destination, control-state semantics, keyboard bypass, and interaction boundaries;
7. discoverable mobile navigation and elimination of unintended root overflow;
8. dependable search feedback, ranking, dismissal, grouping, and no-result recovery;
9. Explore promise alignment;
10. contrast, focus, non-color state cues, reduced motion, and visualization alternatives;
11. documentation-count reconciliation;
12. route, link, console, image/canvas, and regression proof;
13. a minimum historical-source and image-rights evidence baseline sufficient to characterize release risk honestly.

### 4.2 Low-risk inclusions Claude may propose

Claude may propose individual low-risk corrections where each is independently testable and does not change product intent, such as:

- correcting malformed labels such as “More by El”;
- replacing a misleading search label with “Search the atlas” plus accessible scope help;
- adding literal explanatory copy around Palette, Persona, local persistence, and state meaning;
- aligning the homepage Explore wording with the actual destination inventory;
- adding visible scroll affordance or replacing concealed mobile navigation with an obvious labeled interaction;
- adding semantic selected/current/expanded states and a skip-to-main path;
- containing unintended overflow;
- preserving query context and providing meaningful empty-state recovery.

Every inclusion must be recorded in the Decision Record with rationale, evidence, UX effect, and rollback consequence.

### 4.3 Deferred Atlas Coherence Pass

The following remain a separately scoped follow-up unless Claude proves a critical release failure:

- adding Taste as a persistent global destination;
- regrouping the global header around product goals rather than taxonomy facets;
- exposing Admirations, Seen in person, and Saved for later as full Passport collections with empty/populated/removal states;
- aligning header and footer into one conceptual model;
- named-artist focus, relationship explanation, canonical transition, and reset inside the influence graph;
- systematic Era and Nation clarification;
- deciding whether Artwork needs a global inventory route;
- restructuring Movements, Techniques, Eras, and Nations beneath Browse or Explore.

The recommended conceptual hierarchy for that later pass is:

```text
Pigment
├── Discover
│   ├── Painting of the Day
│   └── Lists
├── Browse the atlas
│   ├── Artists
│   ├── Museums
│   ├── Movements
│   ├── Techniques
│   ├── Eras
│   └── Nations
├── Explore relationships
│   ├── Timeline
│   ├── Influence graph
│   ├── Movement family tree
│   └── Nation map
├── Taste
│   ├── Taste Passport
│   ├── Admirations
│   ├── Seen in person
│   └── Saved for later
└── Search the atlas
```

This is a conceptual model, not an instruction to create routes or menus.

### 4.4 Explicitly out of scope

Do not add or redesign the following in this round:

- accounts, public profiles, following, reviews, social feeds, or community mechanics;
- new taste mathematics or unapproved recommendation logic;
- a forced onboarding gate;
- a wholesale Daily publication identity;
- a pure reference-atlas simplification;
- a full visual-language redesign;
- new analytics providers or privacy-policy changes without product-owner approval;
- silent renaming of stable IDs, slugs, localStorage fields, or frozen product terms;
- claims of historical completeness or collection comprehensiveness.

---

## 5. Canonical journeys Claude must protect

### 5.1 Known-artist discovery

```text
Home or Search
→ Artist
→ career arc, artwork, movement, relationship, or museum
→ related entity
→ explicit onward path
```

Preserve the visible anchor. Explain why the relationship matters. Do not replace strong detail-page traversal with generic cards.

### 5.2 Artwork-led discovery

```text
Search, List, Daily, Artist, Museum, or recommendation
→ Artwork
→ Artist / Movement / Technique / Era / Nation / Museum
→ related work or wider classification
→ optional personal action
```

Artwork is the principal junction between knowledge discovery and personal state.

### 5.3 Editorial discovery

```text
Home or Lists
→ ordered editorial List
→ Artwork
→ related entity
→ another List or onward route
```

Preserve Lists as authored walks rather than reducing them to taxonomy results.

### 5.4 Personal Taste loop

```text
Home
→ Find your palette
→ four tones
→ sixteen artwork cards
→ five philosophy questions
→ reveal
→ adopt or defer Persona
→ matched discovery
→ Taste Passport
→ further Admire actions
→ updated Passport
```

The return path must be clear, state must persist, and local/device scope must be explicit.

### 5.5 Explore loop

```text
Home
→ Explore
→ choose temporal, relational, movement, or geographic projection
→ focus an entity
→ understand the relationship
→ open canonical page
→ continue through the atlas
```

The homepage promise and destination inventory must agree. Visual instruments require readable, keyboard-accessible alternatives for essential information.

### 5.6 Journey design rhythm

Every representative journey should express:

> Anchor → relationship → consequence → onward path

- **Anchor:** where the visitor is.
- **Relationship:** how the current object connects to another.
- **Consequence:** why the connection matters.
- **Onward path:** how to continue without losing orientation.

---

## 6. Claude work package

### Workstream A — Freeze scope and release identity

Claude must:

1. identify the current branch/build and target deployment;
2. preserve the current multi-door homepage as rollback;
3. classify each finding as blocker, low-risk inclusion, deferred backlog, or owner decision;
4. record whether the release is being positioned as an editorial discovery/taste product, a historical reference, or both;
5. state the consequences of that positioning for provenance requirements;
6. avoid choosing Taste-first, Daily-first, or a new global navigation without approval.

**Required output:** feasibility brief, frozen-scope proposal, rollback condition, and contradiction register.

### Workstream B — Data and onboarding integrity

Claude must:

1. run the existing validator and attach the unedited summary;
2. confirm zero reference errors;
3. analyze the two deck-coverage warnings against the accepted onboarding specification;
4. correct the pool or record a dated, explicit exception with user-impact rationale;
5. verify that documentation counts match the validator or are clearly dated as historical.

**Blocking condition:** no unexamined onboarding warning or unexplained validator/documentation contradiction.

### Workstream C — First-user Taste journey

Exercise the complete path:

1. open Home;
2. start Find your palette;
3. select four tones;
4. complete sixteen artwork cards with Admire/Pass;
5. answer five philosophy questions;
6. reach reveal;
7. adopt or defer a Persona;
8. enter matched discovery;
9. open the Taste Passport;
10. verify discovery rings and Admirations;
11. export the Passport;
12. generate a share/import URL;
13. import or merge into a clean state;
14. reset and verify the stated consequence.

Also test interruption and correction at:

- tone selection;
- artwork 8 of 16;
- question 3 of 5.

The interface must either resume safely or explain restart/data-loss consequences before they occur.

### Workstream D — Personal-state persistence and recovery

For distinct artworks, test:

- Admire;
- Seen in person;
- Saved for later.

Verify after navigation and reload that:

- each visible state remains accurate;
- states remain independent;
- only Admire affects the v1 taste model;
- removing a state is reflected consistently;
- the Taste page includes admired works;
- local persistence scope is communicated where trust requires it.

If expanded Passport collections are not in the frozen release scope, document their current retrieval limitations rather than implying they are complete.

### Workstream E — Orientation, state, and interaction semantics

Resolve or explicitly disposition:

- route-change focus and concise page identity;
- current global destination;
- selected/active/expanded/current/unavailable/loading/success/error semantics;
- skip-to-main or equivalent keyboard bypass;
- visible focus and logical focus order;
- competing nested actions in the artist/surprise surface;
- non-color state differentiation;
- feedback that answers: what happened, what is the current state, and what can happen next.

No link, button, or control may contain a competing interactive action whose accessible name predicts a different outcome.

### Workstream F — Mobile and responsive containment

At minimum, test:

- 320 px;
- 360 px;
- 390 × 844;
- 400 px;
- 768 × 1024;
- 1280 × 720;
- 1440 × 900;
- up to 200% text enlargement.

Acceptance requires:

- every primary destination is discoverable without accidental gesture knowledge;
- no unintended root-level horizontal scroll;
- intentionally horizontal instruments are contained, keyboard-operable, and visibly signaled;
- header, search, hero copy, controls, labels, provenance, and profile metadata do not clip or overlap;
- narrow layouts preserve hierarchy rather than stacking every region at equal weight.

### Workstream G — Search and Explore contract

Search must communicate:

- when results open;
- result groups and types;
- result count where useful;
- active choice;
- keyboard movement and selection;
- dismissal and focus return;
- no-result state and recovery.

Exact names and meaningful semantic matches must rank above incidental character sequences. Test representative queries for Artist, Artwork, Museum, Movement, Technique, Era, and Nation where data exists, plus a nonsense query.

The homepage Explore invitation and Explore destination must describe the same available instruments. Either expose onward paths to movement family and nation map views or narrow the promise to the two primary instruments. Do not claim instruments that users cannot locate.

### Workstream H — Accessibility and visualization equivalence

Provide evidence for:

- WCAG 2.2 AA contrast for required text and controls in both themes;
- keyboard operation across Home, search, Artists, Palette, Taste, Timeline, influence, and representative details;
- visible focus and logical order;
- route orientation and selected-state semantics;
- reduced-motion parity;
- readable alternatives for essential timeline and relationship information;
- no meaning dependent solely on color, motion, position, or canvas rendering.

A screenshot-only pass is insufficient.

### Workstream I — Provenance, rights, and historical trust

Before `human_review_ready`, Claude must return a minimum evidence baseline:

1. a ten-profile audit spanning at least five eras, five movements, and five nations;
2. a representative source model for biography, dates, classifications, major works, and relationships;
3. source, relationship type, and confidence/dispute state for sampled influence edges;
4. item-level provenance and rights/license status for sampled artworks/images;
5. aggregate coverage counts for sourced, uncertain, generic-attribution-only, and unresolved records;
6. visible differentiation between fact, editorial interpretation, legend, disputed claim, and unknown where applicable.

This is an evidence gate, not a demand to complete full-corpus sourcing in the stabilization patch. Claude must explicitly state whether unresolved coverage prevents the intended release claim. Generic platform attribution alone does not pass as item-level rights evidence.

Legal uncertainty must be escalated rather than inferred away.

### Workstream J — Regression, build identity, and deployment proof

Return:

- commit SHA and build identifier;
- UTC deployment time and environment;
- exact public URL;
- automated test commands and unedited summaries;
- internal-link result;
- route-by-route console evidence;
- visual evidence at acceptance viewports;
- known warnings and dispositions;
- change rationale and residual-risk register;
- rollback instructions.

Smoke-test at least:

```text
#/
#/artists
#/palette
#/taste
#/daily
#/lists
#/museums
#/explore
#/timeline
one Tier 1 artwork
one artist profile
one museum
one editorial List
one invalid entity route
```

---

## 7. Unified acceptance criteria

### P0 — Product and state integrity

1. The validator reports no errors and all references are valid.
2. Both onboarding-deck warnings are resolved or intentionally accepted with a dated rationale.
3. The complete first-user Taste journey finishes without a broken or unexplained transition.
4. Passport creation, update, export, share/import, merge, and reset do not silently discard signals.
5. Admire, Seen in person, and Saved for later persist across navigation and reload, remain independent, and display accurate state.
6. Onboarding interruption and correction consequences are explicit and recoverable.
7. Existing invalid-route and no-match recovery remain functional.
8. Reviewer-facing documentation no longer contradicts current validator counts without a historical-date label.

### P0 — Evidence integrity

9. The minimum ten-profile provenance sample and aggregate coverage baseline are complete.
10. Sampled influence edges carry source, type, and confidence/dispute information.
11. Sampled images carry item-level provenance and rights/license status.
12. No indispensable provenance or legal unknown is hidden or mislabeled.
13. Release language does not imply historical-reference readiness beyond the evidence produced.

### P1 — Accessibility, orientation, and responsive behavior

14. Every route change identifies the new page once and moves focus to a meaningful entry point.
15. The current destination and every active control state are perceivable without color or position alone.
16. Repeated navigation can be bypassed; all primary actions remain keyboard-operable with visible focus.
17. No interactive surface contains a competing interactive action.
18. At 320–400 px widths, all primary destinations are discoverable without unexplained horizontal swiping.
19. There is no unintended root-level horizontal scroll at the acceptance viewports.
20. Both themes meet WCAG 2.2 AA for required text and controls.
21. Reduced motion preserves the same information and choices.
22. Essential visualization content has a meaningful readable and keyboard-accessible alternative.

### P1 — Search, promise, and recovery

23. Search results, groups, selection, dismissal, count, and empty states are perceivable and operable.
24. Exact and meaningful matches outrank incidental substrings.
25. Representative entity queries resolve to correctly typed destinations where matching data exists.
26. The homepage Explore promise and Explore destination describe the same available instruments.
27. Empty, unavailable, invalid, limit, and failure states preserve context and offer a meaningful next action.

### P2 — Product hierarchy and visual fidelity

28. A first-time visitor can describe Pigment as a way to discover and express relationships and taste in art, not as three unrelated products.
29. The recommended first action, if one is frozen, is identifiable without reading every route description.
30. At least one meaningful relationship is demonstrated rather than merely asserted in the opening experience.
31. Global access and guided first-time entry are distinguishable.
32. Representative journeys preserve an anchor, explain the relationship and consequence, and offer an onward path.
33. The product remains recognizably Pigment without depending only on the wordmark, dark background, or display typeface.
34. No decorative relationship system is more prominent than the information it communicates.
35. No secondary path becomes materially less discoverable without an approved tradeoff and rollback condition.

### Release rule

Do not advance to `human_review_ready` while:

- any applicable P0 criterion is unsupported;
- a P1 failure blocks a primary journey;
- licensing evidence required for the intended release remains missing;
- test evidence materially contradicts the claimed result;
- the frozen scope or rollback path is undocumented.

---

## 8. Evidence packet format

Claude's final evidence package should contain the following artifacts.

| Artifact | Required content | Pass condition |
|---|---|---|
| Scope and decision record | frozen objective, blocker/inclusion/backlog classification, approved adaptations, product-owner decisions | no silent scope or intent change |
| Build identity | commit SHA, build ID, UTC deployment time, environment, exact URL | identifiers agree |
| Validator and tests | commands, unedited summaries, pass/fail counts, warning dispositions | all required checks pass |
| Journey transcript | complete onboarding, interruptions, Persona adopt/defer, Passport export/import/merge/reset | no unexplained break or signal loss |
| Persistence matrix | Admire, Seen, Saved across navigation, reload, removal, and source-page return | states remain accurate and independent |
| Accessibility proof | contrast report, keyboard transcript, focus evidence, semantics audit, reduced-motion result, visualization alternative | every applicable P1 criterion supported |
| Responsive proof | screenshots and measurements at acceptance widths and 200% text | no clipping, overlap, or root overflow |
| Search and recovery proof | query set, ranking, typed groups, keyboard behavior, no-result and invalid-route recovery | contract is predictable and recoverable |
| Provenance proof | ten-profile register, relationship sample, image-rights sample, aggregate coverage | every P0 evidence criterion supported |
| Runtime and links | route console logs and automated internal-link result | zero unresolved console errors and broken internal links |
| Visual review | opening experience and representative Atlas/Taste journeys at wide, intermediate, and narrow conditions | hierarchy, relationship grammar, and identity preserved |
| Residual risks | open unknowns, severity, owner, mitigation, release consequence | no indispensable unknown hidden |
| Rollback | exact restoration condition and procedure | current baseline recoverable |

---

## 9. Terminology and content rules

### 9.1 Frozen terms

Preserve unless the product owner explicitly changes them:

- Admire
- Admirations
- Taste Passport
- Palette
- Pigment Persona
- Seen in person
- Saved for later
- Find your palette
- Go next

The issue is not the existence of these terms; it is insufficient explanation of their relationship, consequence, and retrieval.

Recommended conceptual explanation:

> Find your palette begins the journey. Your Palette, Admirations, Seen works, Saved works, taste map, and Pigment Persona live in your Taste Passport.

ELARA owns final sentence-level voice.

### 9.2 Language rules

- Invitation may be lyrical; instruction, consent, state, privacy, persistence, and recovery must be literal.
- Define Persona before repeated capitalization; present it as provisional interpretation, not diagnosis or authority.
- Explain that tone choices influence the starting profile and how their weight compares with artwork choices and questions.
- State whether saved actions live on this device/browser or another explicit persistence scope.
- Choose and document an artists/painters usage rule.
- Distinguish historical fact, disputed evidence, editorial interpretation, and legend.
- Do not use humor where warning, consent, error recovery, or factual qualification is required.

### 9.3 Taxonomy cautions

- Era currently behaves as century-oriented grouping; do not silently rename it.
- Nation must not imply that a modern nationality exhausts birthplace, identity, migration, principal career geography, artistic tradition, Indigenous affiliation, diasporic context, or contested history.
- Movement family structures should state whether they are strict hierarchy, pedagogical approximation, or mixed interpretation.
- Preserve multiple affiliations where the data model supports them.

---

## 10. Risks and guardrails

| Risk | Guardrail |
|---|---|
| Premature convergence | preserve the current baseline and compare challengers against it |
| Scope expansion | no new mode or broad navigation change without a named uncertainty, frozen scope, and rollback |
| Copy-only repair | do not correct promises while leaving retrieval or state failures unresolved |
| Passport overload | maintain hierarchy between identity, taste signal, encounter log, and utility state |
| Pseudo-scientific Taste | keep results provisional, explain sparse signals, preserve reset/export, and never gate knowledge |
| Daily novelty bias | require voluntary recurrence and atlas continuation before identity-level promotion |
| Atlas commoditization | protect editorial voice, relationship depth, atmosphere, and personal continuity |
| Decorative relationships | every connection must communicate consequence and an onward path |
| Accessibility exclusion | require keyboard, assistive, contrast, motion, zoom, and mobile evidence—not screenshots alone |
| Hidden navigation | test discoverability independently from reachability |
| Historical overclaim | require provenance coverage, uncertainty states, and release language proportional to evidence |
| Image-rights exposure | item-level provenance/license sample; escalate unresolved legal questions |
| Taxonomic overconfidence | document Era, Nation, and Movement semantics and uncertainty |
| Frozen-term drift | preserve stable language and storage schema unless explicitly approved |
| Behavioral overclaim | do not infer comprehension, retention, or habit from surface presence or one-session tests |

---

## 11. Product-owner decisions

The following require Arda/MIRA approval rather than silent Claude selection.

### Required before any related implementation

- whether Start with an artist becomes the visually recommended first route;
- whether Taste is a persistent global destination in this release or deferred;
- whether an onboarding-deck imbalance may be accepted temporarily;
- whether instrumentation is approved and under what privacy constraints;
- whether the fifth taste axis is visible at launch.

### May remain provisional for stabilization

- final Pigment Persona names;
- whether Era becomes “Centuries” or “Eras by century” publicly;
- the precise public definition and possible future label of Nations/Places;
- whether Artwork needs a global inventory route;
- whether the header later reduces to Artists, Lists, Museums, Explore, and Taste.

Claude must identify where a blocked technical decision depends on one of these choices and present the smallest reversible alternatives.

---

## 12. Ownership and review sequence

| Owner | Responsibility in this round | Required output |
|---|---|---|
| MIRA | product direction, scope selection, final tradeoffs | frozen direction and product-owner decisions |
| IVO | journey structure, retrieval, taxonomy coherence | blocker/backlog classification and IA review |
| SOREN | visual hierarchy and relationship grammar | visual review against orientation and identity criteria |
| NIKO | alternatives, experiments, guardrails, fallback | experiment logic only if hierarchy work is authorized |
| ELARA | language, state, feedback, recovery, accessibility | AC review and experiential sign-off |
| ARGUS | evidence integrity, provenance, confidence, contradictions | evidence audit and readiness determination |
| VERA | critical challenge, failure paths, novelty-bias control | independent challenge and failure record |
| Claude/Rubens | neutral synthesis of the frozen implementation scope | implementation specification proposal |
| Claude/Caravaggio | challenge blocker claims and unproven hierarchy changes | challenge record |
| Claude/Mondrian | UX states and journey specification | state matrix and journey plan |
| Claude/Dürer | feasibility and implementation | isolated implementation with recorded adaptations |
| Claude/Van Eyck | independent quality review | acceptance-criteria verdict |
| Claude/Vermeer | browser and responsive evidence | reproducible route evidence |
| Claude/Van Gogh | content correction within frozen terminology | approved copy changes |
| Claude/Seurat | data semantics and taxonomy flags | Era/Nation/source integrity report |
| Claude/Duchamp | audit for silent intent change and overclaim | synthesis integrity review |

Recommended sequence:

```text
claude_analysis
→ challenge
→ MIRA/product-owner scope decision
→ approved_for_build
→ isolated implementation
→ independent quality + browser review
→ ARGUS + VERA evidence challenge
→ ELARA + SOREN fidelity review
→ human_review_ready
→ explicit user authorization
→ merge/deploy
```

---

## 13. Post-release experiment backlog

Do not run these experiments until the stabilization evidence is complete and instrumentation/privacy are approved.

### Experiment 0 — Mobile discoverability

**Question:** Can users find every major mode without being told to swipe?

Advance only when major destinations are reliably discovered at tested widths.

### Experiment 1 — Acquisition hierarchy

Compare:

- current multi-door baseline;
- Atlas-primary message;
- Taste-primary message.

Advance a challenger only if it improves comprehension and first action without materially harming known-item lookup, open exploration, or secondary-path discoverability.

### Experiment 2 — Taste accumulating value

Measure onboarding completion, post-onboarding exploration, repeated admiration, return behavior, and perceived validity.

Advance Taste-first only if continued atlas use improves; quiz starts alone do not count.

### Experiment 3 — Daily voluntary ritual

Measure spontaneous next-day or within-week return, engagement with the daily detail, demand for archive/reminders, and continuation into the atlas.

Advance Daily-first only if users return voluntarily and move beyond the single work.

No local metric may be optimized in isolation.

---

## 14. Final synthesis determination

The six reports converge on the following:

1. Pigment's product theory is coherent and worth preserving.
2. The Atlas is the architectural core, Taste is the accumulating personal layer, and Daily is a promising but unproven entrance.
3. The next release should stabilize the existing promise rather than invent a new product.
4. The highest immediate product risks are first-user continuity, state persistence, orientation, mobile discoverability, accessibility, search/recovery behavior, and onboarding balance.
5. The highest trust risks are unsourced historical authority and unverified image rights.
6. The largest strategic risk is treating visual polish or feature presence as proof of comprehension, habit, accessibility, or reference readiness.
7. Broad navigation restructuring and identity experiments should remain reversible follow-up work.

**Theory-team recommendation:** advance to `claude_analysis`. Claude should return a frozen implementation proposal and evidence plan, not begin unapproved production deployment. The build may advance to `human_review_ready` only when the applicable P0/P1 gates are supported by reproducible evidence and all remaining unknowns are explicitly dispositioned.
