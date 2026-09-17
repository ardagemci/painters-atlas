# PIGMENT reconciliation for owner application

Measured 2026-09-17 in `duo/unsolved-1229`. PIGMENT.md was not edited. This is a repository snapshot during concurrent work, not a deployed-site audit. File references were resolved from the current source while preparing this table; Claude may subsequently move lines. §15 actually has **10** numbered items; all are covered here.

Status describes the cited statement, not permission to close a broader product promise. A partly shipped status can mean that one clause is stale while the remaining gap persists. Lane II owns factual status reconciliation; changes to promises, priorities, or any §19 row belong to Lane I. This report is the Lane II evidence handoff, not an instruction to bypass the owner's PIGMENT seal.

Validator command (run before and after notice edits): `osascript -l JavaScript tools/validate.jxa.js`. Both runs ended `ALL REFERENCES VALID`. Statistics were unchanged:

```text
artists: 280, movements: 85, techniques: 40, eras: 10, nations: 38, painter styles: 27, influence edges: 259 (ungrounded: 107, sourced: 1), venues: 137, catalog: 398 (tier1: 127), daily pool: 120, museum notes: 127, photo credits: 127 (attribution required: 108), artwork image credits: 22, personas: 15, lists: 15 (list works below tier 1: 23/107) (featured: 5), tier1 artists: 36 (arcs: 36)
```

A1 changed from 30 to 3; the independent deck warning remains: `deck quadrant F+D- rests on a single work (1); losing it degrades the deck silently`. The 137 registered venues and 127 museum notes/index pages are different populations.

Read-only measurement, without running the SEO generator:

```python
from pathlib import Path
from collections import Counter
pages = list(Path('p').rglob('*.html'))
print(len(pages))
print(Counter(p.parent.name for p in pages))
print(Counter(p.parent.name for p in pages
              if 'property="og:image"' in p.read_text()))
```

Output: **820 files** (398 artwork, 280 artist, 127 museum, 15 list); **675 with og:image** (337 artwork, 196 artist, 127 museum, 15 list). Thus 61 artwork and 84 artist stubs lack that tag. The premise that all 820 have og:image is not supported. For a present tag, see `p/artist/vincent-van-gogh.html:14`. Passport PNG evidence is the browser canvas painter and its download handler, not a checked-in exported PNG or an executed browser export.

| section/item | what PIGMENT.md says (quote) | what the repository shows now (with file:line or command output) | status | which lane an update belongs to |
| --- | --- | --- | --- | --- |
| Header / §12 date | Last updated: 2026-07-16; Snapshot taken 2026-08-27 | `PIGMENT.md:3` and `PIGMENT.md:367`: header predates its own snapshot. Historical dates should remain historical; a new reconciliation date should describe an actual owner-applied update. | stale — partly shipped | Lane II — factual status |
| §12 artist / influence totals | 279 artists; 258 influence relationships (107 ungrounded, against a ratchet of 107) | Validator now reports 280 artists and 259 influence edges (ungrounded: 107, sourced: 1). Historical snapshot is not disproved; it no longer supplies current totals. | stale — partly shipped | Lane II — factual status |
| §12 unchanged quantitative snapshot | 398 canonical artworks; 127 Tier 1 artworks; 36 Tier 1 exhibition artist profiles, all with career arcs; 85 movements; 40 techniques; 10 eras, from before 1200 to today; 38 nations; 137 registered venues; 127 museum notes/pages represented in the current museum index; 15 editorial lists (5 featured); 15 provisional Personas; 27 generative painter styles; 120 eligible Painting-of-the-Day works | Validator agrees with all numeric values (full output below). Museum index filters non-sentinel venues with catalog works at `js/app.js:1592`. This row confirms counts, not an editorial reassessment of chronology or profile quality. | still accurate | Lane II — factual status |
| §12 route inventory | Implemented routes include: | `js/app.js:2600` through `js/app.js:2626` contains all listed routes. Also ships actuality, echoes, privacy and credits; “include” is not an exhaustive claim. | still accurate | Lane II — factual status |
| §12 deployed site | https://ardagemci.github.io/painters-atlas/ | The same origin appears in `index.html:8`. No network request was made; deployment availability or parity with this worktree cannot be determined. | cannot determine | Lane II — factual status |
| §15.1 | 1. **Persona names are placeholders.** The prototypes may survive; labels and copy may change. | `js/personas.js:2` explicitly retains placeholder status. | still accurate | Lane II — factual status |
| §15.2 | 2. **The onboarding deck is not fully adaptive yet.** The current implementation chooses the full deck upfront, while `docs/TASTE_MATH.md` describes later choices reacting to earlier responses. | `js/app.js:3353`; `js/app.js:3501` constructs the whole deck up front. The response handler at `js/app.js:4052` records responses and advances without rebuilding it. | still accurate | Lane II — factual status |
| §15.3 | 3. **The onboarding pool has coverage warnings.** It currently lacks a calm-abstract quadrant anchor and has too few strongly classical works. Fix content coverage before drawing conclusions from Persona quality. | Validator reports one F+D- anchor, not zero, and no E<=-40 shortage warning. `tools/validate.jxa.js:444` tests the classical shortage threshold (<2). Coverage remains fragile, but the specific absence/shortage wording is stale. | stale — partly shipped | Lane II — factual status |
| §15.4 | 4. **Museum pages need curated one-hour routes.** The current collection grid does not yet fulfill the Style Guide's strongest museum-page promise. | `js/app.js:1604`; `js/app.js:1640` renders a chronological collection grid, with no curated one-hour sequence. | still accurate | Lane II — factual status |
| §15.5 | 5. **Editorial list word budgets conflict.** Reconcile `STYLE_GUIDE.md` and `ARTWORK_SCHEMA.md` before enforcing a final contract. | `docs/STYLE_GUIDE.md:90` still says 40–70; `docs/ARTWORK_SCHEMA.md:221` says 15–60; `tools/validate.jxa.js:273` enforces 15–60. | still accurate | Lane II — factual status |
| §15.6 | 6. **Static metadata is behind the product.** The HTML description still understates the chronology and taste/museum/list direction. | `index.html:7` now names 280 artists, 398 catalogued works, 127 museums and churches, movements and taste mapping. `index.html:12` names eight centuries. Lists remain absent from this description; any broader desired repositioning remains an editorial decision. | stale — partly shipped | Lane II — factual status |
| §15.7 | 7. **Instrumentation is undecided.** The product cannot yet answer how many people finish onboarding or share a result. | `js/app.js:2437`; `js/app.js:2440` states no analytics; a source search found no fetch/XMLHttpRequest/sendBeacon/gtag/plausible implementation in js/*.js or index.html. No repository evidence here establishes whether an owner decision has since occurred outside the repository. | cannot determine | Lane II — factual status |
| §15.8 | 8. **Share graphics and real SEO pages are incomplete.** Hash routes alone are weak for search and link previews. | Read-only Python inventory: 820 p/**/*.html files; 675 with og:image, 145 without. `js/app.js:3683`; `js/app.js:4093` implements a painted Passport card and PNG download. Local assets and implementation exist; deployment, indexing and export execution were not tested. | stale — partly shipped | Lane II — factual status |
| §15.9 | 9. **Movement, technique, era, and nation upgrades remain uneven.** The taxonomy is broad; emotional and educational depth is not yet uniform. | `js/app.js:2265` renders description, taxonomy branches and painter cards; `js/app.js:2329` and `js/app.js:2389` provide separate era/nation surfaces. No measurable acceptance threshold defines uniform emotional or educational depth, so that qualitative assertion cannot be adjudicated here. | cannot determine | Lane II — factual status |
| §15.10 | 10. **The visible role of the fifth axis is unresolved.** `M` is stored, while the public map currently emphasizes `F x D`. | `js/app.js:3426`; `js/app.js:3857` surfaces M as intimate/monumental secondary text when abs(M)>=15; `js/app.js:3429` remains F×D. The degree to which the axis should be explained is still an owner choice. | stale — partly shipped | Lane II — factual status |
| §16.1 | 1. Repair onboarding coordinate coverage and either implement true adaptivity or revise the claim. | The specific missing-quadrant/classical warnings have improved (validator), but F+D- still has only one anchor. `js/app.js:3353`; `js/app.js:3501` remains prebuilt. | stale — partly shipped | Lane I — priority / promise decision; Lane II may refresh supporting facts |
| §16.2 | 2. Test the complete onboarding flow with real users before expanding the Persona set. | No real-user completion study was run in this lane; the repository implementation and validator cannot establish user-study completion or outcome. | cannot determine | Lane I — priority / promise decision; Lane II may refresh supporting facts |
| §16.3 | 3. Resolve Persona names and descriptions after observing result quality. | `js/personas.js:2` retains provisional names. Whether sufficient result-quality observation has occurred cannot be determined from the measured code. | cannot determine | Lane I — priority / promise decision; Lane II may refresh supporting facts |
| §16.4 | 4. Add museum one-hour routes for the strongest museums. | `js/app.js:1604`; `js/app.js:1640` still supplies a grid rather than a curated route. | still accurate | Lane I — priority / promise decision; Lane II may refresh supporting facts |
| §16.5 | 5. Upgrade the top movement and technique pages into beginner-friendly explainers. | `js/app.js:2265` provides shared descriptive pages and related taxonomy/painters. “Top” and “beginner-friendly” have no measured acceptance set in this audit. | cannot determine | Lane I — priority / promise decision; Lane II may refresh supporting facts |
| §16.6 | 6. Reconcile docs, metadata, navigation, and product copy with the current taste-atlas direction. | `index.html:48` and `index.html:59` ships Taste in the header; `index.html:7` reflects current scale and taste/museums. PIGMENT itself still has the factual mismatches recorded here. | stale — partly shipped | Lane I — priority / promise decision; Lane II may refresh supporting facts |
| §16.7 | 7. Add share cards and a realistic SEO/prerender plan. | 820 prerendered stubs exist; 675 have og:image. `js/app.js:3683`; `js/app.js:4093` implements Passport PNG export; `tools/build_seo.jxa.js:1` exists but was not run. Completion of all desired share cards is not established. | stale — partly shipped | Lane I — priority / promise decision; Lane II may refresh supporting facts |
| §16.8 | 8. Add privacy-friendly onboarding/share instrumentation only after an explicit product decision. | `js/app.js:2437`; `js/app.js:2440` supports no current analytics, but cannot establish an off-repository owner decision. The conditional promise is left intact. | cannot determine | Lane I — priority / promise decision; Lane II may refresh supporting facts |
| §16.9 | 9. Continue Tier 1 depth selectively where it creates meaningful discovery paths. | Validator measures 127 Tier 1 works, 36 artist profiles with 36 arcs, and 23/107 distinct list works below Tier 1. It cannot measure whether every chosen promotion creates a meaningful discovery path or decide future priority. | cannot determine | Lane I — priority / promise decision; Lane II may refresh supporting facts |
| §19 D-1 | Not implemented. `buildDeck()` runs once per session and builds a **stratified** deck up front; no code re-reads `admired`/`skipped` mid-deck. The composition rules are honored; the adaptivity is not. | `js/app.js:3353`; `js/app.js:3501` and `js/app.js:4052` confirm an upfront stratified deck without response-based reselection. | still accurate | Lane I — all §19 edits / promise changes |
| §19 D-2 | Not implemented. Museum pages ship a collection grid. The Style Guide's strongest museum promise is the one thing museum pages do not do. | `js/app.js:1604`; `js/app.js:1640` shows the collection grid, no one-hour route. | still accurate | Lane I — all §19 edits / promise changes |
| §19 D-3 | Partially shipped. The `#/taste` route exists and is reachable from the homepage and the footer nav, but **not** from the primary header nav (`index.html`, `.main-nav`), so the product's central promise is absent from its most persistent surface. | `index.html:48` and `index.html:59` places the Taste link inside the primary header nav. The stated navigation omission is closed. | stale — closed | Lane I — all §19 edits / promise changes |
| §19 D-4 | Not implemented, and correctly so. The Passport currently holds admirations, seen, want-to-see, saved, quiz answers, coordinates, Persona and milestones in `localStorage` under `pigment.taste.v1`. Phase 2 explicitly depends on accounts, which is a deliberate not-yet. | `js/app.js:134` contains artwork actions, quiz, palette, persona, vector and milestones; `js/app.js:2435` describes the accountless build. Full Phase 2 collections are absent from this schema and route switch. | still accurate | Lane I — all §19 edits / promise changes |
| §19 D-5 | Not implemented as an interface. Confidence is computed internally; the UI presents a Persona and coordinates with no visible error bar, and nothing distinguishes a reading from 8 admirations from one from 40. | `js/app.js:3304`; `js/app.js:3606` computes provisional/forming/solid/strong/deep tiers and displays the tier plus admiration count. Eight and forty therefore differ visibly. Error bars and a general attribution-uncertainty interface are not established by these controls. | stale — partly shipped | Lane I — all §19 edits / promise changes |
| §19 D-6 | Not implemented, and undecided rather than merely unbuilt. There is no analytics of any kind, which is also currently a feature: after PIG-001 unit 20 the product makes **zero** third-party runtime requests, and any instrumentation would be the first thing to break that. | `js/app.js:2437`; `js/app.js:2440` explicitly distinguishes no analytics from Wikimedia image requests. `js/app.js:1621` renders external museum artwork images. The zero-third-party-request assertion is false at source level; no live traffic measurement or owner instrumentation decision was obtained. | stale — partly shipped | Lane I — all §19 edits / promise changes |
| §19 D-7 | Partially shipped. `M` is computed and persisted; the public map emphasizes `F × D`. So the model is five-dimensional and the interface is two-dimensional, and the gap is unexplained to the user. | `js/app.js:3426`; `js/app.js:3857` conditionally includes intimate/monumental in the visible secondary signals; `js/app.js:3429` keeps the map F×D. “Stored but not surfaced” is too broad, while the full axis-interface question remains open. | stale — partly shipped | Lane I — all §19 edits / promise changes |

Application notes / changed status:

- The 2026-07-16 header predates the 2026-08-27 §12 snapshot. Keep historical provenance distinct from any new update date.
- §12 current artist/influence totals are 280/259, previously 279/258; the other listed counts still match.
- §15.3 / §16.1 coverage wording needs narrowing: calm-abstract has one anchor; the classical shortage warning no longer appears. Adaptivity remains absent.
- §15.6 / §16.6 metadata and header navigation have shipped substantial updates; remaining copy reconciliation is not thereby complete.
- §15.8 / §16.7 prerendering and Passport PNG implementation exist, with incomplete og:image coverage and no deployment/export execution checked here.
- §15.10 / D-7: M has conditional secondary text; the map remains F×D.
- D-3's header-navigation omission is closed; D-5's absence-of-visible-confidence claim is partly superseded; D-6's zero-third-party-request rationale conflicts with image rendering. All §19 edits route to Lane I.
- Cannot determine: live deployment/indexing, browser PNG output, real-user study completion, off-repository owner instrumentation decisions, final qualitative taxonomy/depth adequacy, or whether strategic priorities should be retired. No network access, browser run, SEO regeneration, or PIGMENT edit was performed.

---

## Independent verification (Claude, 2026-09-17)

Codex produced this table. Before commit, six of its verdicts were re-checked
against the repository directly, including every item Claude had described
differently during the debate:

| Claim | Check | Result |
| --- | --- | --- |
| §19 D-3: Taste is absent from the header nav | `index.html:59` `<a href="#/taste" data-nav="taste">Taste</a>` sits inside `.main-nav` | **stale — closed**, confirmed |
| §15.8: share/SEO pages incomplete | `find p -name '*.html'` → 820 stubs; 675 carry `og:image` (337 of 398 artwork stubs) | confirmed. **Correction to the debate record:** Claude said "820 stubs with og:image"; 675 do |
| §19 D-6 rests on "zero third-party runtime requests" | every catalog image loads from `upload.wikimedia.org` | confirmed. The rationale as written is untrue |
| §19 D-5: no visible confidence | `js/app.js:3304` computes provisional/forming/solid/strong/deep; `:3312` flags `provisional` | **partly superseded**, confirmed |
| §15.10 / D-7: M not surfaced | `js/app.js:3426` puts E/C/M poles into the Persona's secondary text when \|value\| ≥ 15 | confirmed. The map stays F×D |
| §15.3: too few strongly classical works | validator output mentions "classical" 0 times; F+D− still rests on one work | confirmed |

**The one thing this table cannot do is apply itself.** PIGMENT.md is sealed
against Lane III, and every §19 change is a Lane I promise change. Owner action is
needed.
