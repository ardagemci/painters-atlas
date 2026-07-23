# BUILD LOG — PIG-001 Wave A (units 1–10)

**Author:** Dürer (`claude-implementation-lead`), Implementation Lead
**Date:** 2026-07-24
**Branch:** `pig-001-stabilization` (off `effa805…`; never `main`; not pushed — Synthesis Lead pushes at checkpoints)
**Gate 1:** verified satisfied before any edit — `protocol/tasks/PIG-001/specification.md`
exists, `workflow_state: approved_for_build`, `frozen-sha256:70de6a71…0166` present.
**Validator:** `osascript -l JavaScript tools/validate.jxa.js` run after **every** unit;
stayed green throughout — `ALL REFERENCES VALID`, `app.js: syntax OK`, snapshot unchanged
(247/75/39/8/37/27/225/115/317(75)/75/103/15/12/36). The two pre-existing deck-pool
WARNINGS (`<2 works with E<=-40`, `empty F×D quadrant 1,-1`) are untouched by this wave
(they are unit 22 / owner-decision territory, OD-4).
**Smoke test (end of wave):** `python3 -m http.server 8421 -d .` → homepage 200, `app.js` 200,
`styles.css` 200, `artists-1.js`/`worldmap.js` (newly versioned) 200, index carries 20
`?v=20260724-pig001` tags. No console/load breakage observed via curl.

> Gate 2 is **not** certified here — that is Van Eyck's. Browser/viewport/contrast
> evidence (AC18/19/20 measurement) is Vermeer's and is deliberately not attempted here.

---

## Per-unit record

### U1 — nav active vs. hover (`52465b4`)
- **Files:** `css/styles.css` (~:129-132)
- **Change:** `.active` was visually identical to `:hover` (same `scaleX(1)` gold underline).
  Now the current destination is distinct: `color:var(--gold2)` **+ `font-weight:700`** **+
  persistent `height:2px` `var(--gold2)` underline at full opacity**; hover stays lighter
  (`color:var(--ink)`, thin 1px underline at `.55` opacity). Both themes (all values via tokens).
- **Validator:** green. **Deviations:** none.
- **AC:** AC16 (visible non-color cue for the *active* state — satisfied via weight + underline
  thickness, not color alone). Programmatic `aria-current` is Wave B (unit 14).

### U2 — mobile-nav scroll affordance (`d826fd4`)
- **Files:** `css/styles.css` (≤820px block, ~:837)
- **Change:** `.main-nav{overflow-x:auto}` had no affordance while `.strip` uses a `mask-image`
  edge-fade. Applied the same mask idiom to `.main-nav`.
- **Deviation (recorded):** used a **right-weighted, one-sided** fade
  `linear-gradient(90deg,#000 78%,transparent)` instead of the `.strip`'s symmetric two-sided
  fade. Rationale: a symmetric left fade would dim the **first / current** destination
  ("Artists") at rest; a right-only fade is the honest "more nav →" cue and never obscures the
  leading item. Brief explicitly permits "any small affordance you judge right." Nav not
  restructured.
- **Validator:** green.
- **AC:** AC18 (mobile-nav discoverability / primary destinations have an evident affordance).

### U3 — root overflow containment (`f673a98`)
- **Files:** `css/styles.css` (:96 header; :226-227 `.cards`/`.cards.wide`; :698 `.tree-grid`;
  ≤820px block `.strip`)
- **Change (three measured causes):**
  1. **320px `.strip` gutter:** base `margin:0 -28px` (desktop gutter) overflowed the 16px
     mobile gutter by 12px/side → added `.strip{margin-left:-16px;margin-right:-16px}` in the
     ≤820px block.
  2. **320px oversized card tracks:** `.cards` (232), `.cards.wide` (300) and `.tree-grid`
     (330 — the `.tax-card` tree grid) exceeded the ~288px content box at 320px. Wrapped each
     min track in the `minmax(min(100%,X),1fr)` idiom — identical layout at ≥X, collapses to a
     single full-width column below X, so it can never force root overflow at any width.
  3. **1280px header:** the non-wrapping `brand · nav · search · toggle` row overflowed on all
     routes. Added `flex-wrap:wrap` (with `gap:12px 28px`) to `.site-header`; at ≥~1360px it
     stays one row (1440 unaffected), below that `search`+`toggle` wrap to a second row instead
     of overflowing.
- **Validator:** green. **Deviations:** none (all three are the brief's named causes; the
  `min()` idiom is a superset of "reduce the min-width").
- **AC:** AC18 (`documentElement.scrollWidth <= clientWidth` at 320/390/768/1280/1440) — **code
  complete; final measurement is Vermeer's**. Reasoning: each named overflow source is now
  bounded; two-column split layouts (:558 etc.) were not listed among the measured causes and
  already collapse via their own media queries.

### U4 — tone non-color state cue (`3e53962`)
- **Files:** `css/styles.css` (:923)
- **Change:** `.tone.on` was color-only. Added non-color cues: a **`::after` `"✓"` glyph**
  (pushed right via `margin-left:auto`), **`font-weight:600`**, and an **`inset 0 0 0 1px`
  box-shadow** (border/shape change). Both themes (glyph uses `--gold2`, visible on light paper).
- **Deviation (recorded, minor):** achieved **CSS-only**; the unit table anticipated an
  `app.js:2571-2574` markup edit. A `::after` glyph delivers the visual cue with no markup
  change and no JS risk. No product-intent change. ARIA (`aria-pressed`) is Wave B as instructed
  — visual cue only here.
- **Validator:** green.
- **AC:** AC16 (selected state has a non-color visible cue).

### U5 — nested-button extraction (`ef109b3`)
- **Files:** `js/app.js` (:1447-1453), `css/styles.css` (`.ec-cover`, `.ec-surprise`)
- **Change:** `<button class="ec-surprise">` was a descendant of `<a class="entry-card">`
  (illegal nested interactive content). Restructured the first home entry card to a
  `<div class="entry-card">` with a **stretched cover-link** (`<a class="ec-cover"
  aria-label="Start with an artist">`, `position:absolute;inset:0;z-index:1`) and the surprise
  button as a **sibling** (`position:relative;z-index:2`). Card → `#/artists`, surprise →
  random artist (handler `[data-random-artist]` at :2074 unchanged, `preventDefault` intact).
  No interactive element nests inside another; visual design unchanged (other two cards remain
  `<a>`).
- **Validator:** green. **Deviations:** none.
- **AC:** AC17 (no interactive control contains a competing interactive control — the named
  violation is resolved; both actions keyboard-focusable as two separate tab stops).

### U6 — strip de-dup for AT/keyboard (`38b2eaa`)
- **Files:** `js/app.js` (:1431-1432 generation, :1480 render)
- **Change:** the marquee doubled `${stripItems}${stripItems}`, so every artwork link existed
  twice for keyboard/AT. Introduced a `stripAnchor(w, dup)` helper; the **second copy** now
  renders each link with `tabindex="-1" aria-hidden="true"` and empty `alt`. Flex layout
  identical (still N+N children), so the animation and the reduced-motion `overflow-x:auto`
  path both keep a **single logical sequence** for keyboard/AT.
- **Validator:** green. **Deviations:** none.
- **AC:** AC17/AC20 (keyboard sequence + reduced-motion single sequence).

### U7 — search a11y (`f684831`)
- **Files:** `index.html` (:47), `js/app.js` (:2209-2210)
- **Change:** (a) search `aria-label` named only 5 of 8 indexed types → now
  "artists, artworks, lists, museums, movements, techniques, eras and nations" (matches `INDEX`).
  (b) Enter and Escape both `blur()`-ed focus to `<body>`. Removed both blurs: **Escape** now
  `hideSearch()` + `searchInput.focus()` (focus returns to the input on dismiss); **Enter**
  navigates and keeps focus in the (cleared) input — no focus-to-body.
- **Validator:** green. **Deviations:** none.
- **AC:** AC21 partial (dismissal + focus-return half). Search **ranking/starvation** is unit 17
  (Wave C) — not in scope here.

### U8 — name-splitting helper (`224417c`)
- **Files:** `js/app.js` (helper after :42; sites :1119, :1646, :1795, :1800)
- **Change:** added one IIFE helper `artistShortName(a)` — returns the surname while keeping
  leading particles (`van/von/da/de/del/della/di/du/la/le/el/…`). Replaced the five split hacks
  at the **four artist sites**. Verified outputs: El Greco→"El Greco", Leonardo da Vinci→
  "da Vinci", Vincent van Gogh→"van Gogh", Artemisia Gentileschi→"Gentileschi", Fitz Henry
  Lane→"Lane" (single-name artists e.g. Rembrandt→"Rembrandt"; O'Keeffe, Toulouse-Lautrec also
  correct). Prior output had produced "More by El", "Why Vinci matters", "All of Gogh".
- **Deviation (recorded):** the fifth listed site, `js/app.js:922`, is the **timeline
  era-jump**, operating on **era** names, not artist names. Eras are "14th Century"…"21st
  Century"; `split(" ")[0]` yields "14th"…"21st" — clean, distinct compact labels, **not** the
  name-mangling defect. Applying a surname helper there would collapse all eight eras to
  "Century" (last-word) — a regression. Left `:922` unchanged with rationale. (Confirmed:
  `js/artists-*.js` records carry no short-name field, as the brief anticipated.)
- **Validator:** green.
- **AC:** editorial-correctness defect from the register (name-splitting) — resolved at all
  genuine sites.

### U9 — Explore alignment (`b0763d6`)
- **Files:** `js/app.js` (`viewExplore`, :1330-1352)
- **Change:** hub lede said "Two instruments" and exposed two cards, while the homepage promises
  four. Corrected the lede to "Four instruments" and added two entry cards matching the existing
  hub pattern: **Family trees of movements** → `#/movements` (its Family-tree view toggle,
  :1821) and **A world map of painters** → `#/nations` (the world map, :1197). Accents
  `--wine`/`--blue` from the existing token set; voice consistent with the existing cards
  (world-map copy reuses the `viewNations` "refused to stay put" line). All four instruments now
  have a reachable path.
- **Validator:** green. **Deviations:** none. (Family-tree instrument is a stateful view toggle,
  not its own hash route, so the card routes to `#/movements` where the toggle lives — the
  instrument is reachable, per AC22.)
- **AC:** AC22 — homepage Explore promise and the Explore destination now name the same four
  available instruments, each reachable.

### U10 — ?v= uniformity (`de9d7f3`)
- **Files:** `index.html` (:26 css; :69,72,78-93 scripts; :97 app.js)
- **Change:** added `?v=20260724-pig001` to the exactly-18 previously-unversioned tags
  (`worldmap.js`, `venues.js`, `artists-1..16.js`) and **bumped** the two files this wave edited
  (`css/styles.css` `20260717-card1`→`20260724-pig001`, `js/app.js` `20260717-seo1`→
  `20260724-pig001`) to the same uniform string. Already-versioned files not edited this wave
  (taxonomy, artworks, influences, catalog-*, tier1, lists, personas, museums) were left at
  their existing versions per the r2 plan (uniformity = every tag carries a version; no
  gratuitous cache-bust of unchanged files). Verified: **0** unversioned script/css tags remain;
  20 tags carry the new string.
- **Validator:** green. **Deviations:** none.
- **AC:** AC26 (cache/versioning treatment) + AC1 (deployed-identity `?v=` proof). Rollback note
  for AC26: the 18 files now carry a version string, closing the last cache gap the r2 plan flagged.

---

## Wave A summary

- **Units complete:** 10/10 (U1–U10), one commit each, order preserved.
- **Commits:** `52465b4 d826fd4 f673a98 3e53962 ef109b3 38b2eaa f684831 224417c b0763d6 de9d7f3`.
- **Files touched:** `css/styles.css`, `js/app.js`, `index.html` only. No route/id/slug/frozen-
  term/`pigment.taste.v1` changes; no new deps, no build step.
- **Validator:** green after every unit (syntax + references), snapshot unchanged.
- **Deviations logged:** U2 (one-sided mask, rationale), U4 (CSS-only, no markup edit), U8
  (site :922 excluded — era labels, not a name defect). All are recorded above for Gate 3.
- **AC self-assessment (partial, per wave scope):** AC16 visible-cue half (U1,U4); AC17 nested-
  control + strip sequence (U5,U6); AC18 overflow + mobile-nav affordance code-complete, pending
  Vermeer measurement (U2,U3); AC21 dismissal/focus-return half (U7); AC22 satisfied (U9); AC26
  versioning (U10). ARIA/programmatic state (AC16 second half), search ranking (AC21 first half),
  and browser-measured AC18/19/20 evidence remain for later waves / reviewers.
- **Gate 2 NOT certified here** (Van Eyck). **Not pushed** (Synthesis Lead).
