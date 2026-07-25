# BUILD LOG — PIG-001 Wave C (units 17–19)

**Author:** Dürer (`claude-implementation-lead`), Implementation Lead
**Date:** 2026-07-25
**Branch:** `pig-001-stabilization` (verified; never `main`; **not pushed** — pushing is the
Synthesis Lead's).
**Gate 1:** re-verified before any edit — `protocol/tasks/PIG-001/specification.md` exists with
`workflow_state: approved_for_build`.
**Builds on:** Wave A (`evidence/build-log-wave-a.md`) and Wave B (`evidence/build-log-wave-b.md`),
both read in full first. Wave B's U14 (combobox/listbox/option semantics on search) and U12
(~194 focusable graph nodes) directly shaped units 17 and 19 below. No Wave A or B unit was
re-done or reverted.
**Validator:** `osascript -l JavaScript tools/validate.jxa.js` after **every** unit — green
throughout: `app.js: syntax OK`, `ALL REFERENCES VALID`, snapshot unchanged
(247/75/39/8/37/27/225/115/317(75)/75/103/15/12/36). The two pre-existing deck-pool WARNINGS
(`<2 works with E<=-40`, `empty F×D quadrant 1,-1`) are untouched (unit 22 / AC3).
**Commits (one per unit, in the briefed order):**

| Unit | SHA | Files |
|---|---|---|
| U17 search ranking | `f54c33d` | `js/app.js`, `css/styles.css` |
| U18 onboarding checkpoints | `191fe44` | `js/app.js` |
| U19 route orientation / focus / skip | `c0847c4` | `js/app.js`, `css/styles.css`, `index.html` |

Each commit's `--stat` was checked: 2, 1 and 3 files respectively, nothing else. Staging was by
explicit path every time (Wave B lesson B-12); `git add -A` was never used. `THEORY_001.md` at the
repo root remains **untracked**, as found.

**`?v=` treatment:** this wave edits only `js/app.js`, `css/styles.css` (both already at the
uniform `?v=20260724-pig001` from Wave A U10) and `index.html` (which carries no `?v=` of its own).
The existing wave string covers every edited file — **verified on the served page**, no bump needed.

**Smoke test (served, end of wave):** `python3 -m http.server 8421 -d .` → `/` 200 (6331 B),
`css/styles.css?v=20260724-pig001` 200 (49068 B), `js/app.js?v=20260724-pig001` 200 (180158 B).
Served index carries **20** `?v=20260724-pig001` tags and **0** unversioned script/css tags; the
skip control and `#route-status` are present; `aria-live` is **gone from `#app`**, which now carries
`tabindex="-1"`.

**Working-tree note (not mine):** `git status` at the end of the wave shows `CHALLENGE_001` and
`THEORY_001` deleted from the repo root and appearing untracked under
`protocol/tasks/PIG-001/`. That relocation was **not made by this session** and is not in any Wave C
commit; I left it exactly as found rather than staging or reverting someone else's working tree.

> Gate 2 is **not** certified here — that is Van Eyck's. Browser/viewport/contrast/AT measurement
> (screenshots, real screen-reader transcripts) is Vermeer's and is deliberately not attempted.

---

## Evidence harnesses (reproducible, committed with this log)

Three executable harnesses under `protocol/tasks/PIG-001/evidence/harness/`. All three load the
**real** data files and extract the **real** source text out of `js/app.js` — none of them
re-implements the logic under test. No Node on this Mac; all run under `osascript -l JavaScript`.

| Harness | What it proves |
|---|---|
| `wave-c-fixture.jxa.js` | Runs the frozen 24-query fixture against the real 838-entry INDEX using the real `srKeys`/`srRank`/`srSelect` text. Also measures ordering, header uniqueness, starvation and the documented no-match baselines. |
| `wave-c-checkpoints.jxa.js` | Round-trips the five frozen onboarding checkpoints through the real `obWrite`/`obRestore`/`obClear` text with a faithful Storage stand-in, plus the tamper/corruption/isolation cases. |
| `wave-c-routes.jxa.js` | Loads **all of `js/app.js`** under a minimal DOM shim and drives all 24 router branches plus a full onboarding run through the real click handler. |

---

## U17 — search ranking (`f54c33d`)

**Files:** `js/app.js` (`INDEX` builder, new `SR_*` constants, `srKeys`, `srWordStart`, `srRank`,
`srSelect`, rewritten `runSearch`, `hideSearch`), `css/styles.css` (`.search-results .sr-more`).

### The five confirmed defects and what replaced them

| # | Defect (briefed, re-verified in source) | Fix |
|---|---|---|
| a | Exactness not modelled at all — an exact full-name match ranked identically to any other prefix match | `SR_EXACT` is its own tier and returns immediately; an exact name is always the first option rendered |
| b | Within a bucket, order was INDEX insertion order, i.e. **ranking by entity type** | Six relevance tiers now order results; entity type survives only as the deterministic tie-break *inside* one tier |
| c | `.slice(0, 9)` applied **after** `[...starts, ...contains]`, so 247 artists could starve every matching artwork/museum/movement | `srSelect` fills the cap tier by tier, and **inside a tier the matching types take turns**. Tiers are never crossed for fairness, so a prefix match still always outranks a substring match |
| d | Group headers emitted on type **change**, so one type rendered two headers once the bucket boundary was crossed | Grouping now happens **after** ranking: one `role="group"` + heading per type, ordered by that type's best-ranked member. Measured: **0 duplicate headers** across all 33 probed queries |
| e | Only `name` was searched — no artwork was findable by its painter's name | `meta` is matched, and a meta match on a word boundary is its own tier **above** incidental name substrings, so it cannot be starved by them |

### The tiers

`0 exact name` · `1 name prefix` · `2 word-start inside the name` · `3 meaningful metadata (exact /
prefix / word-start)` · `4 incidental substring` · `5 metadata substring`.

Two supporting mechanisms, both required by the fixture's own rows:

- **Alternate names.** A nation is indexed as `🇹🇷 Türkiye`; the bare country name is carried as an
  explicit `alt` so `türkiye` is an *exact* match (F18), not a substring. Leading articles are
  stripped into an extra key, so `starry night` exactly matches *The Starry Night* (F5) and
  `art` prefix-matches *The Art of Painting*.
- **A list's `meta` is a count** (`"12 works"`), not identity. It is still displayed and is
  explicitly excluded from matching (`nometa`) so `works` does not summon every list.

### Frozen 24-query fixture — actual vs expected (AC21's required evidence)

Produced by `wave-c-fixture.jxa.js` against the real data (INDEX = 838 entries). "tier" is the
relevance tier of the top result; "shown/total" is the visible count against the number of
matching entries.

| # | Query | Expected #1 | Actual #1 | Route | Tier | shown/total | Pass |
|---|---|---|---|---|---|---|---|
| F1 | `vermeer` | Johannes Vermeer | Johannes Vermeer [Artists] | `#/artist/johannes-vermeer` | 2 | 9/11 | **PASS** |
| F2 | `rembrandt` | Rembrandt van Rijn | Rembrandt van Rijn [Artists] | `#/artist/rembrandt` | 1 | 9/11 | **PASS** |
| F3 | `frida kahlo` | Frida Kahlo | Frida Kahlo [Artists] | `#/artist/frida-kahlo` | 0 | 9/11 | **PASS** |
| F4 | `basquiat` | Jean-Michel Basquiat | Jean-Michel Basquiat [Artists] | `#/artist/jean-michel-basquiat` | 2 | 1/1 | **PASS** |
| F5 | `starry night` | The Starry Night | The Starry Night [Artworks] | `#/artwork/the-starry-night` | 0 | 1/1 | **PASS** |
| F6 | `guernica` | Guernica | Guernica [Artworks] | `#/artwork/guernica` | 0 | 1/1 | **PASS** |
| F7 | `mona lisa` | Mona Lisa | Mona Lisa [Artworks] | `#/artwork/mona-lisa` | 0 | 1/1 | **PASS** |
| F8 | `las meninas` | Las Meninas | Las Meninas [Artworks] | `#/artwork/las-meninas` | 0 | 2/2 | **PASS** |
| F9 | `louvre` | Musée du Louvre | Musée du Louvre [Museums] | `#/museum/louvre` | 2 | 1/1 | **PASS** |
| F10 | `rijksmuseum` | Rijksmuseum | Rijksmuseum [Museums] | `#/museum/rijksmuseum` | 0 | 1/1 | **PASS** |
| F11 | `impressionism` | Impressionism | Impressionism [Movements] | `#/movement/impressionism` | 0 | 3/3 | **PASS** |
| F12 | `cubism` | Cubism | Cubism [Movements] | `#/movement/cubism` | 0 | 1/1 | **PASS** |
| F13 | `fresco` | Fresco | Fresco [Techniques] | `#/technique/fresco` | 0 | 1/1 | **PASS** |
| F14 | `woodcut` | Woodcut (id `woodblock`) | Woodcut [Techniques] | `#/technique/woodblock` | 0 | 1/1 | **PASS** |
| F15 | `17th century` | 17th Century | 17th Century [Eras] | `#/era/17th-century` | 0 | 1/1 | **PASS** |
| F16 | `19th` | 19th Century | 19th Century [Eras] | `#/era/19th-century` | 1 | 1/1 | **PASS** |
| F17 | `japan` | 🇯🇵 Japan | 🇯🇵 Japan [Nations] | `#/nation/japan` | 0 | 1/1 | **PASS** |
| F18 | `türkiye` | 🇹🇷 Türkiye (id `turkey`) | 🇹🇷 Türkiye [Nations] | `#/nation/turkey` | 0 | 1/1 | **PASS** |
| F19 | `tate` | Tate Modern | Tate Modern [Museums] | `#/museum/tate-modern` | 1 | 6/6 | **PASS** |
| F20 | `art` | Artemisia Gentileschi | Artemisia Gentileschi [Artists] | `#/artist/artemisia-gentileschi` | 1 | 9/51 | **PASS** |
| F21 | `son` | Sonia Delaunay | Sonia Delaunay [Artists] | `#/artist/sonia-delaunay` | 1 | 9/18 | **PASS** |
| F22 | `min` | Minneapolis Institute of Art | Minneapolis Institute of Art [Museums] | `#/museum/minneapolis-institute-of-art` | 1 | 8/8 | **PASS** |
| F23 | `zzzqx` | *(no match)* | *(no match → `.sr-empty`)* | — | — | 0/0 | **PASS** |
| F24 | `qwertyuiopasdf` | *(no match)* | *(no match → `.sr-empty`)* | — | — | 0/0 | **PASS** |

**FIXTURE: 24 / 24 PASS, 0 FAIL.** Every frozen query class is covered and resolves: exact
(F3, F5–F8, F10–F15, F17, F18), prefix (F2, F16, F19–F22), alternate name (F5, F14, F17, F18),
word-start/mid-name (F1, F4, F9), ambiguous/incidental-substring probes (F19–F22), no-match
(F23, F24).

### Ordering, starvation and header measurements

Over the 24 fixture queries plus 24 extra probes (48 queries):

- **Ranking order (what the cap selects): 48/48 clean** — in the selected set, every exact/prefix
  hit is ordered above every non-prefix hit. This is R11's assertion at the ranking layer, and it
  holds by construction: `srSelect` never crosses a tier for fairness.
- **Display order after type grouping: 43/48 clean.** Five queries (`art`, `min`, `night`, `water`,
  `mo`) show a *cross-group interleave* — see deviation **C-1**, which proves this is unavoidable and
  explains the choice.
- **Duplicate group headers: 0** across all probed queries (defect d closed).
- **Starvation:** `art` matches 51 entries across 4 types; the visible nine now carry all four types
  (1 artist, 1 artwork, 3 museums, 4 movements). `o` matches 595 entries across 8 types and the
  visible nine carry 4 types rather than nine artists. `picasso` shows the artist, 6 of his works
  (via metadata) and 2 museums.
- **Metadata reachability (defect e):** `vermeer` now surfaces 8 Vermeer paintings under the artist;
  `artemisia` surfaces 8 of hers. Neither was findable at all before.
- **Truncation is no longer silent:** when more matches exist than fit, the panel renders
  *"Showing 9 of 51 matches — keep typing to narrow it."* (`aria-hidden`, because the same count is
  carried in the listbox's own `aria-label`, so it is announced once, not twice).

### Documented no-match baselines (ux-requirements §3) — re-checked

`durer`, `velazquez`, `cezanne` (no diacritic folding), `rose`, `seventeenth`, `moma` (ids are not
indexed), `woodblock` — **all unchanged, still no match.** One change: `1600` now matches 8 entries
(movement/era `period` and `range` metadata). See deviation **C-2**.

### Wave B semantics preserved

`role="combobox"`/`aria-autocomplete`/`aria-haspopup`/`aria-controls` on the input, `aria-expanded`
toggled by `runSearch`/`hideSearch`, `role="listbox"` on the panel, `role="group"` type wrappers
with `role="presentation"` headings, `role="option" aria-selected tabindex="-1"` with `sr-opt-N`
ids — all intact. `aria-activedescendant` is **removed on every result-set change** and `selIdx` is
reset, so a stale option id can never be pointed at; the arrow-key handler reads DOM order, and ids
are numbered in DOM order after grouping, so selection tracks what is on screen. The listbox
`aria-label` is now dynamic (match count / nothing-matches) and is reset by `hideSearch`.

---

## U18 — onboarding checkpoint persistence (`191fe44`)

**Files:** `js/app.js` (`OB_KEY`, `obWrite`, `obClear`, `obRestore`, `obStart`, the module-init
`ob = obRestore()`, the `tone` / `tones-done` / `deck-admire` / `deck-pass` / `answer` / `adopt`
handlers, a rewritten `retake`, and the `reset` / `storage-reset` branches).

**The defect:** `let ob = null` was module memory only. A reload, a back/forward, or a tab restore
at any point before `obFinish()` destroyed the tones, the deck, the admirations, the passes and the
answers, with no warning and no recovery. Warning-only handling was explicitly rejected by the
frozen spec.

**The mechanism (materialized, not seeded).** `obStart()` seeds `buildDeck()` with
`Math.random()`, so **no seed can rebuild the same sixteen works**. What is persisted is the
resolved state: `{ v, step, tones, deck: [ids], di, admired, skipped, answers, adopted }`, written
after **every** step transition. Store: **`sessionStorage`, new key `pigment.onboarding.v1`** — a
half-finished quiz is not yet taste data, and the tab-lifetime scope matches "in progress". It is a
separate key in a separate store: **`pigment.taste.v1` and its schema are untouched**, no field
added, renamed or repurposed, so a Passport written before this ships parses identically after.

**Restore refuses to half-resume.** Absent, unreadable, wrong-version, a deck id the catalog no
longer has, or an impossible progress index all fall back to a clean intro rather than a corrupt
run; `step 2` with a finished deck is normalised to `step 3`, and a full answer sheet at `step 3` is
normalised to the reveal, so no view is ever asked to render question six or card seventeen. Every
storage call is wrapped: a browser that refuses the write loses resumability, never the run itself,
and nothing in the UI claims otherwise.

**`retake` (briefed as broken).** It was `ob = null;` — no confirmation, no re-render, and it is an
`<a href="#/palette">`, unlike `reset` which confirms. It now states the consequence in full
("finishing replaces the tones and answers behind your current map… your admirations are kept"),
treats **cancel as cancel** (`e.preventDefault()` on the anchor), clears the stored run, and
re-renders when already on `#/palette`. `reset` and `storage-reset` now clear the stored run too, so
an erased Passport cannot leave a ghost half-quiz behind.

### The five frozen checkpoints — resume verification (`wave-c-checkpoints.jxa.js`)

Each checkpoint is saved, **all memory is dropped**, and the state is restored from storage, exactly
as a reload does it.

| # | Frozen checkpoint | Simulated state | Result |
|---|---|---|---|
| 1 | **Tone selection** | step 1, 2 of 4 tones chosen | **RESUMES EXACTLY** — step 1, both tones (`ultramarine`, `venetian-red`) intact, same 16 works still the deck |
| 2 | **Artwork 8 of 16** | step 2, `di=7`, 3 admired + 4 passed | **RESUMES EXACTLY** — still on card 8, card 8 is the *same* artwork (*The Kiss*), all 3 admirations and 4 passes preserved, whole deck order preserved, tones preserved |
| 3 | **Question 3 of 5** | step 3, 2 answers recorded | **RESUMES EXACTLY** — step 3, both prior answers intact with the same chosen options, next question is question 3, the 9 deck admirations survived into the question step |
| 4 | **Reveal** | step 4, all 5 answers | **RESUMES EXACTLY** — the reveal, not the intro; five answers and four tones intact |
| 5 | **Adopt / defer** | step 4, persona adopted | **RESUMES EXACTLY** — the reveal with the adoption recorded, answers intact behind it |

**5 / 5 checkpoints resume exactly. 29 / 29 harness assertions pass, 0 fail** — including: no stored
run → clean intro; unreadable bytes → no resume, no throw; unknown schema version → no resume; a
work missing from the catalog → refuse to half-resume; impossible progress index clamped;
`clear()` removes both the stored run and the in-memory run; **`pigment.taste.v1` byte-identical
after a full write/restore/clear cycle**; onboarding writes land **only** under
`pigment.onboarding.v1`.

**End-to-end, through the real click handler** (`wave-c-routes.jxa.js`, real `js/app.js` under a DOM
shim): Begin → 4 tones → 16 deck taps (advances to the questions at exactly 16; 16 admirations+passes
recorded) → question 3 of 5 is the stored checkpoint → the fifth answer reaches the reveal →
`obFinish` wrote the Passport (`milestones.onboarded`, 5 quiz answers, 4 palette tones, admirations
present) → the reveal checkpoint still recoverable. Storage keys written across the whole run:
`pigment.taste.v1` (localStorage) and `pigment.onboarding.v1` (sessionStorage) — nothing else.

---

## U19 — route orientation, focus, skip navigation, live region (`c0847c4`)

**Files:** `js/app.js` (`routeStatus`, `lastRouteKey`, `focusSilently`, `viewEntry`, `fpOf`,
`restoreFocus`, `route()`, the `[data-skipto]` handler, `viewInfluences`), `index.html` (skip
control, `#route-status`, `#app`), `css/styles.css` (`.sr-only`, `.skip-link`, `.skip-inline`,
focus-visible rules).

**The worst of it, confirmed:** `index.html:53` declared `aria-live="polite"` on
`<main id="app">` — the exact element whose entire `innerHTML` `route()` replaces. Assistive tech
therefore re-read the **whole page** on every navigation, and onboarding calls `route()` on every
single deck tap: sixteen whole-page re-announcements in one flow. Alongside it: `focus()` 0
occurrences, no skip link, and `route()` never moved focus anywhere.

**1 — the live region.** `aria-live` is removed from `#app` entirely. A dedicated visually hidden
`<p id="route-status" role="status" aria-live="polite">` now carries the **page name alone**, taken
from the leading segment of `document.title`, set once per navigation.

**2 — focus.** `route()` moves focus to the view's entry point — its `<h1>`, given `tabindex="-1"`
on demand, falling back to the `#app` landmark for a view without one. Two deliberate exceptions:

- **The first load never moves focus and never announces.** Arriving at a page should not steal
  focus from the user's starting position.
- **A re-render of the page already on screen announces nothing and does not jump to the heading.**
  `route()` compares the routed key against the last one; on a same-page re-render it captures the
  focused element's signature (`id | tagName | sorted data-*`) beforehand and restores focus to the
  matching control afterwards. This is what stops the fix fighting the onboarding deck: a deck tap
  destroys and re-creates the Admire button, and focus lands back on it instead of collapsing to
  `<body>`. When the control genuinely no longer exists (answering a question replaces it with the
  next one) focus goes to the new heading **silently**.

**3 — skip to main.** A `.skip-link` control is the first tabbable element in `<body>`, off-screen
until focused, then pinned top-left with a gold border and outline drawn from theme tokens, so it
renders in **both** themes.

**4 — the bypass Wave B flagged and handed over.** `#/influences` gained ~194 focusable nodes in
U12 with no way past them. A `.skip-inline` control now sits **before** the graph
("Skip the graph — 194 painters follow"), invisible until tabbed to, and moves focus to a
`tabindex="-1"` target **after** the graph. Measured in the rendered page: skip control before,
target after, 194 node stops bypassed. AC17's "repeated navigation can be bypassed" half, left open
by Wave B, is now closed on both the header and the graph.

**Focus indicators** use `:focus-visible` (the same guard Wave B U12 used), so the mouse never sees
a ring on a heading that route() focused, while keyboard users always do — `outline:2px solid
var(--gold)` in both themes.

**`document.title` is untouched** — all 22 assignments remain exactly as they were; this unit adds
focus and announcement, nothing else.

### All 24 router branches — regression pass (`wave-c-routes.jxa.js`)

The real `js/app.js` was loaded under a minimal DOM shim and every router branch driven through the
real `hashchange` listener.

| # | Route | Renders | `<h1>` | `document.title` | Focus moved | Announced |
|---|---|---|---|---|---|---|
| 1 | `#/` | 196 kB | yes | `Pigment — Find your place in the history of art` | n/a — first load, deliberately not stolen | n/a — first load |
| 2 | `#/artists` | 178 kB | yes | `Artists — Pigment` | yes | `Artists` |
| 3 | `#/timeline` | 71 kB | yes | `Timeline — Pigment` | yes | `Timeline` |
| 4 | `#/influences` | 130 kB | yes | `Influences — Pigment` | yes | `Influences` |
| 5 | `#/daily` | 3.4 kB | yes | `Portrait of Innocent X — Painting of the Day — Pigment` | yes | `Portrait of Innocent X` |
| 6 | `#/lists` | 10 kB | yes | `Lists — Pigment` | yes | `Lists` |
| 7 | `#/list/{id}` | 12 kB | yes | `Paintings That Still Scare Us — Pigment` | yes | `Paintings That Still Scare Us` |
| 8 | `#/palette` | 511 B | yes | `Find your palette — Pigment` | yes | `Find your palette` |
| 9 | `#/taste` | 442 B | yes | `Your taste — Pigment` | yes | `Your taste` |
| 10 | `#/passport/{payload}` | 395 B | yes | `Import passport — Pigment` | yes | `Import passport` |
| 11 | `#/museums` | 59 kB | yes | `Museums — Pigment` | yes | `Museums` |
| 12 | `#/museum/{id}` | 12 kB | yes | `Musée du Louvre — Pigment` | yes | `Musée du Louvre` |
| 13 | `#/explore` | 1.9 kB | yes | `Explore — Pigment` | yes | `Explore` |
| 14 | `#/artist/{id}` | 20 kB | yes | `Leonardo da Vinci — Pigment` | yes | `Leonardo da Vinci` |
| 15 | `#/artwork/{id}` | 7.5 kB | yes | `The Calling of Saint Matthew — Caravaggio — Pigment` | yes | `The Calling of Saint Matthew` |
| 16 | `#/movements` | 25 kB | yes | `Movements — Pigment` | yes | `Movements` |
| 17 | `#/movement/{id}` | 23 kB | yes | `Renaissance — Pigment` | yes | `Renaissance` |
| 18 | `#/techniques` | 14 kB | yes | `Techniques — Pigment` | yes | `Techniques` |
| 19 | `#/technique/{id}` | 146 kB | yes | `Oil Painting — Pigment` | yes | `Oil Painting` |
| 20 | `#/eras` | 5.3 kB | yes | `Eras — Pigment` | yes | `Eras` |
| 21 | `#/era/{id}` | 5.1 kB | yes | `14th Century — Pigment` | yes | `14th Century` |
| 22 | `#/nations` | 84 kB | yes | `Nations — Pigment` | yes | `Nations` |
| 23 | `#/nation/{id}` | 22 kB | yes | `Italy — Pigment` | yes | `Italy` |
| 24 | `default` → 404 | 180 B | yes | `Lost — Pigment` | yes | `Lost` |

**ROUTES: 24 / 24 render, title, focus and announce correctly. 0 fail.**
Plus: a same-hash re-render **announces nothing (PASS)** and **does not jump focus to the heading
(PASS)** — the onboarding-deck guarantee, measured rather than asserted.

---

## Deviation ledger (Gate 3)

| # | Unit | Deviation | Rationale |
|---|---|---|---|
| **C-1** | U17 | **Grouped display is kept, and strict global rank order is therefore not achievable.** In the visible set, a lower-ranked item of an earlier type group can appear above a higher-ranked item of a later group (measured: 5 of 48 probed queries — `art`, `min`, `night`, `water`, `mo`). | The two requirements are **provably incompatible**: if type X matches at ranks {1,3} and type Y at rank {2}, any one-header-per-type layout yields 1,3,2 or 2,1,3 — neither is rank-monotone. The brief requires "group headers never duplicate for one type" (defect d) and states the starvation requirement in terms of *exclusion* ("never **starved** by … ordering … or by the result cap"), which is fully satisfied. So I closed defect (d) as briefed and kept the Wave-B `role="group"` presentation, ordering the groups by their best-ranked member so an exact match is always the first option and each group's own items are in rank order. `ux-requirements.md` R11's literal cross-type reading holds at the **ranking** layer (48/48) but not in the grouped **display** (43/48). Flagged here for Van Eyck/the Synthesis Lead rather than silently chosen — if R11's display reading is the binding one, the fix is to drop the type headings for a flat labelled list, which is a visible design change (Matisse's territory) and outside my authority. |
| **C-2** | U17 | `1600` now returns 8 results (period/range metadata) where the frozen fixture documented it as no-match. | Direct, unavoidable consequence of the briefed defect (e) — enabling `meta` matching. It is a literal metadata match, not the "fuzzy/semantic layer" the fixture was testing for; the intent of that baseline note (no fuzzy matching) is intact. `paris` likewise now finds Paris museums by city. All the other documented baselines (`durer`, `velazquez`, `cezanne`, `rose`, `seventeenth`, `moma`, `woodblock`) are unchanged. |
| **C-3** | U17 | Diacritic folding and id matching were **not** added. | Both would flip documented baselines Van Eyck treats as the current baseline (`durer`/`velazquez`/`cezanne`, `moma`/`woodblock`), neither is required by AC21 or any fixture row, and both are scope beyond the briefed defect list. Recorded as deliberately not done. |
| **C-4** | U17 | A list's `meta` (`"12 works"`) is displayed but excluded from matching. | It is a count, not identity; indexing it would make `works` return all twelve lists as "meaningful metadata matches" and push real matches down. |
| **C-5** | U18 | The stored run is **not** cleared at `obFinish()`, contrary to the r2 mechanism note. | `obFinish()` runs the instant the fifth answer lands — *before* checkpoints 4 (reveal) and 5 (adopt/defer). Clearing there would have made two of the five frozen checkpoints unrecoverable, i.e. it would have failed the very criterion the unit exists for. The run is cleared on a confirmed `retake`, on `reset` and on `storage-reset`; sessionStorage disposes of the rest at tab close. |
| **C-6** | U18 | `retake`'s confirmation text is new user-facing copy. | The brief required making the data-loss consequence explicit. The wording is literal state/consequence copy per the spec's language rule — it states what is discarded, what is kept (admirations), and when the replacement actually happens. |
| **C-7** | U19 | The skip controls are `<button>`s, not the conventional `<a href="#main">`. | The URL fragment belongs to the hash router: `href="#app"` would set `location.hash = "#app"`, fire `hashchange`, and route the user to the 404 page. A button is the only correct control here. |
| **C-8** | U19 | Focus **and** the live region both fire on a navigation, which can announce the page name twice. | Programmatic-focus announcement behaviour varies across screen reader / browser pairs; relying on either alone risks silent navigations. Both together guarantee one short announcement in every combination, at the cost of a possible duplicate of one short string — against the whole-page re-read being replaced, that is a large net reduction. Named here so Vermeer can measure it and Van Eyck can rule on it. |
| **C-9** | U19 | `route()` grew a same-page re-render path with focus restoration, beyond "add `.focus()`". | Without it the fix would have fought the onboarding deck exactly as the brief warned: sixteen route() calls, each dumping focus at the top of the page. The restoration is signature-matched and touches nothing else. |
| **C-10** | U19 | `viewInfluences`'s trailing `.map-hint` gained `id="ig-end" tabindex="-1"`. | It is the only element after the graph, so it is the correct landing point for the bypass; no copy or layout changed. |

---

## Self-assessment against the named criteria

- **AC7 — PASS (code-complete, evidence attached).** All five frozen checkpoints (tone selection,
  artwork 8 of 16, question 3 of 5, reveal, adopt/defer) resume **at the exact checkpoint with prior
  answers intact** — 5/5, proved by 29/29 round-trip assertions that drop all memory between save and
  restore, plus a full end-to-end run through the real click handler. Warning-only handling was not
  used. `pigment.taste.v1` is byte-identical across the cycle and its schema is untouched.
- **AC15 — PASS for the code half.** Every route transition now sets a distinct `document.title`
  (unchanged, 24/24), announces the new page identity **once** through a dedicated live region
  instead of re-reading the whole view, and moves focus to a meaningful entry point — 24/24 measured.
  The whole-page live region is gone. **The real screen-reader transcript is Vermeer's/Van Eyck's**
  and is not claimed here; deviation C-8 is the specific thing to measure.
- **AC17 — PASS for the bypass half; the wave's own additions are keyboard-operable.** The header
  skip control and the `#/influences` graph bypass both exist, are the first/earliest tabbable
  controls in their scope, are visible on focus in both themes, and move focus to a real target —
  closing the half Wave B explicitly left open. Keyboard operability of C1–C18 and the nested-control
  clearance stand from Waves A/B. Contrast measurement of the new focus styles is Vermeer's.
- **AC21 — PASS on the frozen instrument.** The frozen 24-query fixture is **24/24**, with all six
  query classes resolving. Exact matches rank first; prefix, alternate-name and metadata matches are
  no longer starved by incidental substrings, by entity-type ordering, or by the result cap
  (measured: 48/48 clean at the ranking layer, four types represented in a 51-match query that
  previously could have shown only artists). Group headers never duplicate (0 across 33 queries).
  Truncation is disclosed rather than silent. The one open question is deviation **C-1** — the
  grouped display's cross-group interleave — which is a stated, proved trade-off, not an oversight.
- **AC9 (contributed, not claimed whole):** the silent `slice(0,9)` truncation now names its own
  limit, which was the one decidable "limit state preserves context" gap in `ux-requirements.md` §6.

**Not claimed, deliberately:** AC18/AC19 measurements, AT transcripts, screenshots, contrast of the
new focus ring and skip controls, the AC4 journey-matrix transcript, and **Gate 2** — all of which
belong to Vermeer and Van Eyck.

---

## Wave C summary

- **Units complete:** 3/3 (U17, U18, U19), one commit each, in the briefed order, never sharing a
  commit — the blast radius of any regression is attributable to exactly one change.
- **Commits:** `f54c33d` (U17) · `191fe44` (U18) · `c0847c4` (U19).
- **Files touched:** `js/app.js`, `css/styles.css`, `index.html` only. No route `case`, id, slug,
  frozen term, or `pigment.taste.v1` field was added, renamed or dropped. One new storage key,
  additive, in a different store. No new dependency, no build step.
- **Validator:** green after every unit; snapshot unchanged.
- **Fixture:** 24/24. **Checkpoints:** 5/5 (29/29 assertions). **Routes:** 24/24.
- **Gate 2 NOT certified here** (Van Eyck's). **Not pushed** (Synthesis Lead's).
