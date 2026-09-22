# Duo transcript — task: "Work on open cases and find possible future steps to elevate this platform (Pigment) into something closer to its original goal."

## Facts established before round 1 (measured, not asserted)
- Repo: Pigment, zero-dependency static art atlas (plain HTML/CSS/JS, hash router, GitHub Pages). No Node in the toolchain by project rule; validate with `osascript -l JavaScript tools/validate.jxa.js`; tests `python3 -m unittest discover -s tests`.
- North star (PIGMENT.md §1): "a social atlas where people discover, understand, and express their taste in art." Phased: 1 Atlas 2.0 → 1.5 Accountless Taste Prototype → 2 Profiles → 3 Learning → 4 Community. §16: "Do not jump to accounts or community merely because Phase 1.5 exists. First prove that Discover -> Admire -> Map -> Become is enjoyable."
- This duo branch `duo/elevate-1629` is based on origin/main 352b276.
- Three UNMERGED open branches, each green alone (tests OK, validator 0), and all three merge cleanly together (199 tests OK, validator 0):
  1. `duo/rights-pd-token-0350` (+3): executes owner decisions D-010 (residence Türkiye) and D-011 (Decision A → new image.status value "licensed"); adds `isRenderable(img)` at js/app.js:93.
  2. `duo/lane-iv-and-fixes-0236` (+4): adds "Lane IV — Dual-Build" to CLAUDE.md (the constitution), sealed-set hook fixes, AGENTS.md, tools/lane4-run.sh. Constitutional + sealed set.
  3. `codex/moderna` (+1): "homepage/artwork-page redesign preview, imported for review" — js/studio.js, css/studio.css, index.html, js/app.js +40.
- On the rights branch, `isRenderable(img)` checks STATUS only. 13 sites call `x.image && x.image.src && isRenderable(x.image)`; the two mini-card rails at js/app.js:2252 and :2254 test `o.image && o.image.src` with NO status check (correct today only because all 61 status:"copyright" records lack src). IFACE-001's UX requirements (protocol/tasks/IFACE-001/ux-requirements.md) REQ-P1 asks for ONE renderability expression, ceiling 0, test-guarded.
- Separately: js/artworks.js (581 gallery entries) has no status field at all (RIGHTS-001 E-007).
- Validator's only warning on main: "deck quadrant F+D- rests on a single work (1); losing it degrades the deck silently".
- A painted shareable Passport PNG card already exists (js/app.js ~3693) and shareChip exists.
- Open protocol tasks: RIGHTS-001 (awaiting_build_approval, convergence not recommended), IFACE-001 (intake, Gate 1 unmet, theory brief requested), PLATFORM (unstaffed).

## Claude — round 1
Two tracks, split by authority.

Track 1 — close open cases that are ours to close. (a) Integrate `duo/rights-pd-token-0350`: owner-directed decisions D-010/D-011, green, merges clean. (b) Finish what it half-did. `isRenderable(img)` (app.js:93) checks status only; all 13 call sites still repeat `w.image && w.image.src &&` beside it, and the two mini-card rails (app.js:2252/2254) test `o.image && o.image.src` with no status check at all — correct only because every copyright record lacks a src. With a fourth status now live the trap is wider. One `renderableImage(w)` covering src + status, every site routed through it, a test allowing zero raw expressions. That is Mondrian's REQ-P1: zero reader-visible change, verifier-decidable.

Lane IV (rewrites CLAUDE.md and the sealed set) and codex/moderna (a design study) stay as separate branches with written assessments — adopting either is the owner's call.

Track 2 — elevate toward the goal. PIGMENT §16 says prove Discover→Admire→Map→Become before accounts. The validator's only warning is that deck quadrant F+D− rests on one work: the loop's weakest structural point. I'd build a loop-health report — per-quadrant deck depth, taste-map reachability — so future content work aims at the loop, not at raw record count. No social layer yet.

## Codex — round 1
The predicate refactor is useful, but does not close IFACE-001. REQ-P3 explicitly includes window.ARTWORKS; its records use img, with no status. A canonical-record helper alone leaves artist galleries outside the gate. Ship the mechanical consolidation as a scoped prerequisite, with behavioral tests for copyright-with-src, missing-src, and licensed-with-src — not merely a regex counting expressions. Then write the requested theory brief resolving cross-registry identity and withholding, including prerender output. Keep RIGHTS-001 open: executing D-010/D-011 does not establish convergence on its remaining questions.

A coverage report cannot establish that the loop is enjoyable. tools/validate.jxa.js:323–343 already counts qualifying quadrant anchors and warns below two. Calling that warning the loop's weakest structural point overstates what we know; it identifies a content fragility, not the largest user obstacle.

My next slice: 1. Curate a second qualifying calm-abstract work, with defensible coordinates and image provenance. 2. Extend existing validation only where necessary; define "taste-map reachability" before creating another report. 3. Run a small observed usability study through onboarding → Passport → recommended artwork → Admire → Passport return. Record completion time, whether people recognize themselves in the result, and whether they can find a compelling next work. PIGMENT §16 explicitly prioritizes real-user testing.

## Facts checked between rounds (by Claude)
- Codex's validator citation is exact (E4 block). On the rights branch the validator WAS updated to (pd || licensed) at lines 168, 185, 221, 343, 435 — validator and app agree; no divergence. But the rule `(status pd||licensed) && src` is now duplicated across js/app.js (13 sites + 2 rails that skip status), tools/validate.jxa.js (6 sites), and Python tools (build_seo, asset_inventory, rights_register, audit_artwork_rights).
- F+D− is recorded as a PRODUCT CONSTRAINT: docs/BACKLOG.md:758 "F+D− stays at 1 and cannot move", :760 "no public-domain candidate exists to join it — calm abstraction is Rothko", :836 "F+D− is a product constraint, not a backlog item". The validator comment says 29 of 35 abstract works are in copyright. The licensed records entering the deck (black-fuji F−55/D+75, little-dancer F−85/D+5) are not F+D−. PIG-001 spec: coordinates are never tuned to silence a validator.

## Claude — round 2
Accepted, all three corrections. The refactor is a prerequisite, not IFACE-001's closure — ARTWORKS has no status (REQ-P3). RIGHTS-001 stays open. And a coverage report measures fragility, not enjoyment; E4 already counts anchors, so a new report duplicates it.

Two pushbacks, both on grounds I checked. (1) "Curate a second calm-abstract work" was already investigated and closed: BACKLOG.md:758 records F+D− "stays at 1 and cannot move" — calm abstraction is Rothko, in copyright. "licensed" doesn't help: it covers CC photographs, and here the painting itself is protected. Re-scoring to fill the quadrant is explicitly banned. (2) Neither of us can run a usability study, and §16 #8 forbids instrumentation without an explicit product decision. What we can build is the study kit: a 5-person protocol the owner runs — tasks, timing, recognition questions, a results template keyed to the loop.

That leaves one engineering slice, and Codex's "behavioral, not regex" point is where it matters most: the renderability rule now lives in three languages. One test that loads every record and asserts app, validator and Python tools return the SAME renderable set — fixtures for copyright-with-src, missing-src, licensed-with-src — plus routing the two rails through the helper. Proposed slice on this branch: (A) merge duo/rights-pd-token-0350; (B) renderableImage(w) in app.js covering src+status, all sites incl. rails 2252/2254; (C) cross-evaluator agreement test with those fixtures; (D) docs/LOOP_STUDY_PROTOCOL.md; (E) written assessments of lane-iv and moderna branches for the owner. Not doing: IFACE-001's no-image state (Gate 1, needs theory brief), ARTWORKS gating (REQ-P3, needs cross-registry design), any merge to main.

## Codex — round 2
I accept withdrawing the second-quadrant candidate. I'd change C in two ways: Test against expected outcomes, not just agreement — all evaluators can agree on the same bug. Use a fixture matrix covering pd, licensed, copyright, unknown/missing status, missing image, and empty/missing src. Execute production predicates or consumers; don't recreate their expressions inside the test. Compare equivalent scopes — audit_artwork_rights.py includes ARTWORKS galleries; asset_inventory.py also reports museum photos and prerender metadata. Compare catalog eligibility by record ID, then separately verify downstream inclusion and exclusion; URL-only comparisons can hide mistakes when records share a URL. build_seo is JXA, so two languages not three; include its artwork-image selection. The study kit is sensible, but §16.8's instrumentation restriction does not prohibit manually observed sessions; describe the kit as ready for owner-led sessions. Finally, add the requested IFACE-001 theory brief as a bounded deliverable proposing cross-registry identity, rights precedence, and consistent withholding across runtime and prerender.

## Claude — round 3
Adopted, four of them: "all evaluators can agree on the same bug" is the decisive flaw in my test — expected-outcome matrix, executing production code, not retyped expressions. Record-ID scope, not URL scope: this very session proved it, when one af Klint record existed under two URL forms. Two languages, not three. And §16.8 governs instrumentation, not observed sessions — I overstated.

One line I'm holding: the theory brief is the other pole's artifact. PROTOCOL.md §1 gives it to ChatGPT, and IFACE-001/theory-brief-request.md has already been sent to them. Claude writing it collapses the dipole: the pole that challenges theory would be authoring it. What the Claude pole owns is evidence — so I'd produce the cross-registry identity measurement the brief needs: for each of the 581 ARTWORKS entries, which catalog record it corresponds to (by Commons title, not URL), where the two disagree about renderability, and what prerender emits for each. That unblocks the brief without writing it.

Final slice: (A) merge rights branch; (B) renderableImage(w) covering src+status, every app.js site incl. rails 2252/2254; (C) expected-outcome fixture matrix executing app (via JXA) and Python predicates, plus record-ID agreement on the real catalog; (D) cross-registry identity evidence for IFACE-001; (E) study kit framed as ready for owner-led sessions; (F) written assessments of lane-iv and moderna.

## Codex — round 3
I accept preserving the theory/synthesis separation and delivering evidence for the pending brief. Three concrete refinements:

1. **C must explicitly retain validator and prerender coverage.** “App (via JXA) and Python predicates” drops two previously agreed consumers. Execute production eligibility logic in `tools/validate.jxa.js` and image selection in `tools/build_seo.jxa.js`, including artist and cover selection. Use expected outcomes for fixtures and record-ID comparisons only where eligibility scopes match.

2. **Commons titles establish shared assets, not necessarily artwork identity.** D should classify matches as exact asset, independently confirmed same artwork, ambiguous, or unmatched. Different photographs can depict the same work; forcing every gallery entry into a catalog match would manufacture certainty. Preserve source identifiers and matching evidence. Report observed gallery rendering separately from catalog eligibility, since missing gallery status is an unresolved policy question.

3. **Distinguish generated output from checked-in output.** For prerender evidence, identify the route and whether the result comes from executing the generator or inspecting existing stubs. Otherwise stale HTML can masquerade as current behavior. Flag unmatched gallery entries without corresponding artwork routes explicitly.

The study kit should include an actionable results template: observed obstacle, affected loop step, supporting observation, and proposed next experiment. Five sessions can expose usability problems; they do not establish general enjoyment.

With these incorporated, the slice is bounded and useful. RIGHTS-001 and IFACE-001 remain open, and the quadrant constraint stays documented.

AGREE