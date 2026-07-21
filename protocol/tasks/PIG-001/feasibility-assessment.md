# FEASIBILITY ASSESSMENT — PIG-001

**Author:** Dürer (`claude-implementation-lead`), Implementation Lead
**Round:** 1 (analysis only — Gate 1 in force)
**Date:** 2026-07-21
**Build:** commit `3c2e9fa45645d787da3754417448bbcebfd4029a` on `main`

**Gate 1 status, reconfirmed this session:** `protocol/tasks/PIG-001/specification.md`
does not exist (`ls protocol/tasks/PIG-001/` shows `browser-evidence.md`,
`challenge-analysis-caravaggio.md`, `evidence/`, `intake-baseline.md`,
`liaison-incoming-analysis.json`, `theory-brief.md`, `ux-requirements.md` — no
`specification.md`). No `approved_for_build` state exists. **This round is
advisory/read-only. No production file was opened for editing; no branch was
created.** This document is a plan, not a diff.

This assessment builds on, and does not re-derive: `intake-baseline.md`
(build identity, validator output), `theory-brief.md` (THEORY_001, Workstreams
A–J, §4.2), `challenge-analysis-caravaggio.md` (confirmed-defect ledger,
findings 1–30), `ux-requirements.md` (route/control/search/journey
inventories, R1–R18), and `browser-evidence.md` (measured overflow + mobile-nav
causes). Where I add a new code citation not already in those documents, I
grepped/read it myself this session and say so.

---

```
F1 — WORKSTREAM CLASSIFICATION
```

| WS | Name | Classification | Why (files named) |
|---|---|---|---|
| A | Freeze scope and release identity | **straightforward-verification** | Build identity is already established (`intake-baseline.md` §2); classification of every finding as blocker/inclusion/backlog/owner-decision is exactly this document plus the other four specialist reports; rollback condition is a commit SHA, not code (`3c2e9fa…`). No production file needs to change to satisfy WS A. |
| B | Data and onboarding integrity | **bounded-correction** | Validator already run, zero reference errors (`intake-baseline.md` §3). The two deck warnings are a **content** fix per Caravaggio finding 26 — add qualifying Tier 1 works to `js/catalog-1.js`…`js/catalog-4.js` so `tools/validate.jxa.js:208-214`'s thresholds clear — not a logic change. Doc-count reconciliation (`PIGMENT.md`, `README.md`) is correction-shaped but sits outside Gate 1's enumerated paths (CLAUDE.md §3 lists `js/`, `css/`, `index.html`, `p/`, `tools/`, `sitemap.xml`, `robots.txt` only) — see F2 unit 14. |
| C | First-user Taste journey | **bounded-correction** (+ verification) | The journey-walk itself is verification (Van Eyck/browser territory). Two confirmed code defects sit on this path and are each small: persona-overwrite guard on `mergePassports` (`js/app.js:2908-2926`, invoked `:3018`) and onboarding persistence-or-warning (`ob` state, `js/app.js:2548-2552`). Neither requires new architecture — see F2 units 12–13. |
| D | Personal-state persistence and recovery | **straightforward-verification** | Admire/Seen/Saved already persist independently via `PP_LABELS` (`js/app.js:84-88`) with label-swap on toggle (`:2084`) — this is testing existing, working behavior. The one gap (no `aria-pressed`, R18) is folded into Workstream H/E's small ARIA additions, not a new build. |
| E | Orientation, state, and interaction semantics | **bounded-correction** | Largest item count, but every item is a small, independently scoped patch inside existing functions: no `.focus()` call in `route()` (`js/app.js:1986-2030`), zero `aria-current`/skip-link (grepped codebase-wide, confirmed 0 by Mondrian §2), `.active`==`:hover` (css:130-132), nested button-in-anchor (`js/app.js:1447-1453`). None requires a new rendering path or data model change. |
| F | Mobile and responsive containment | **bounded-correction** | Root causes are fully identified and CSS-only: `.strip` negative margin (css:626) uncompensated at ≤820px, oversized `.tax-card` at 320px, non-wrapping `.site-header` row at 1280px (css:94-102, wrap only added at css:836/820px), no scroll-affordance on `.main-nav` (css:837) unlike `.strip`'s existing mask idiom (css:627-628). All three fixes are additive CSS rules in existing media-query blocks. |
| G | Search and Explore contract | **bounded-correction** | Ranking fix (exactness tier + per-type quotas ahead of `.slice(0,9)` at `js/app.js:2181`) is a scoped change to one function, testable against Mondrian's 24-query fixture (§3). Explore-promise mismatch (`js/app.js:1463` vs `:1336`) is a copy edit. `aria-label` fix (`index.html:47`) and Enter/Escape focus return (`js/app.js:2209-2210`) are one-line changes. Riskiest item in this workstream is the ranking change (see F2 unit 11), but it is bounded, not a rewrite. |
| H | Accessibility and visualization equivalence | **SPLIT: verification + bounded-correction**, per the brief's own framing | **Verification:** WCAG contrast (see F3), keyboard-operation transcript across the 8 acceptance routes, reduced-motion parity check — these are evidence-gathering, not code. **Bounded-correction:** `.ig-node` has no `tabindex`/`role`/keydown (click-only delegation, `js/app.js:2089`) — add three attributes/one handler; `canvasTag` (`js/app.js:719-720`) emits `<canvas>` with no accessible name — add `role="img" aria-label`; text equivalents for timeline/influence data already exist in the DOM (timeline bars are real `<a>` at `:894`; per-artist "Lineage & circle" panel at `:1699-1704`) so this is exposing, not building. Confirms Caravaggio finding 9/10: no new rendering pipeline needed. |
| I | Provenance, rights, and historical trust | **blocked-on-decision** (owner/Seurat, confirmed) | No `source`/`license`/`confidence` field exists anywhere in the schema (`js/artists-1.js:4-16`, `js/influences.js` 3-tuples, `js/catalog-1.js:14-15`) — adding item 6's "visible differentiation" UI is a feature requiring a schema contract change (`docs/ARTWORK_SCHEMA.md`), correctly out of this round per Caravaggio finding 11. **Narrower exception, startable today, not gated by Gate 1:** an out-of-band rights register at `protocol/tasks/PIG-001/evidence/` (not a production path) scoped to the PD-flagged subset actually rendered (`js/app.js:1357,1360` gate on `image.status==="pd"`) — this is a protocol artifact, not a code change, so it needs no `approved_for_build`. I note it as available but do not build it in this document; it's Seurat's/the owner's call whether to start it now. |
| J | Regression, build identity, deployment proof | **straightforward-verification** | Running the validator, unittest suite, and route-by-route console/link checks and recording unedited output — no code changes. Already partially done in `intake-baseline.md` §3–4. |

---

```
F2 — SMALLEST REVERSIBLE PLAN
```

Ordered safest/most-independent → riskiest/most cross-cutting. Every unit
assumes authorization arrives later; none of this was built. "?v= bump"
answers whether `index.html:70-97`'s hand-maintained cache-busting query
strings must change (verified pattern below, F4-ii).

| # | Unit | Files touched | Est. LOC | Revert cost | Ship independently? | `?v=` bump needed |
|---|---|---|---|---|---|---|
| 1 | Nav `.active` vs `:hover` non-color fix | `css/styles.css` (:130-132) | ~5 | trivial | yes | css only |
| 2 | Mobile nav scroll affordance (apply `.strip` mask idiom, css:627-628, to `.main-nav`, css:837) | `css/styles.css` | ~10 | trivial | yes | css only |
| 3 | Overflow containment: `.strip` margin override ≤820px + oversized `.tax-card` at 320px + header `flex-wrap` at 1280px | `css/styles.css` (css:626 media override, css:94-102 / css:836 breakpoint) | ~15-20 | trivial | yes (independent of #2, though both touch header region — test together) | css only |
| 4 | Tone `.on` non-color cue (css:923) | `css/styles.css`, `js/app.js` (:2571-2574 markup, add glyph or `aria-pressed`) | ~8 | trivial | yes | css + app.js |
| 5 | Nested-button extraction (U8/R7) | `js/app.js` (:1447-1453) | ~10 | trivial | yes | app.js |
| 6 | Strip de-dup for reduced-motion/AT hazard | `js/app.js` (:1480) | ~10-15 | trivial | yes | app.js |
| 7 | Search `aria-label` fix + Enter/Escape focus return | `index.html` (:47), `js/app.js` (:2209-2210) | ~5 | trivial | yes | app.js (index.html itself carries no `?v=`) |
| 8 | Name-splitting fix (displayName helper) | `js/app.js` (new helper + call sites :922, :1119, :1646, :1795, :1800) | ~15-20 | trivial | yes, but layout/copy impact of full names in tight labels should get a quick visual check | app.js |
| 9 | Explore-promise alignment (narrow home copy to match the 2 exposed instruments) | `js/app.js` (:1460-1465, copy only) | ~5-8 | trivial | yes | app.js |
| 10 | Persona-overwrite guard + honest import copy | `js/app.js` (`mergePassports` :2921-2923, import copy :2941) | ~15 | trivial (isolated function) | yes | app.js |
| 11 | Onboarding honest-warning (recommended option, see below) | `js/app.js` (`obStart`/`obFinish` region :2548-2552, `retake` :2982) | ~15 | trivial | yes | app.js |
| 12 | Route-focus / skip-link / `aria-live` de-noise | `js/app.js` (`route()` :1986-2030), `index.html` (:53, add skip-link), `css/styles.css` (visually-hidden-until-focus skip-link style) | ~30-40 | moderate — touches the one shared `route()` fn called from every navigation site | yes, but needs the widest regression pass (all 24 routes) | app.js + index.html + css |
| 13 | Search ranking fix (exactness tier + per-type quota before `.slice(0,9)`) | `js/app.js` (:2160-2194) | ~20-30 | moderate — core, shared search path | yes, but re-run Mondrian's F1–F24 fixture (`ux-requirements.md` §3) as the acceptance test before/after | app.js |
| 14 | Doc-count reconciliation | `PIGMENT.md`, `README.md` | ~4 | trivial | yes | N/A — not versioned assets, and outside Gate 1's enumerated paths (CLAUDE.md §3) so not blocked by it, but still a content decision I'd flag rather than do unilaterally |

**Persona-overwrite guard (unit 10) — detail.** `js/app.js:2921-2923` currently
does last-writer-wins on `["quiz","palette","persona","milestones"]` by
`updatedAt` comparison. Fix: split `persona` out of that loop; if
`theirs.persona?.adopted` differs from `out.persona?.adopted`, do not assign
until `confirm()`-gated (mirroring the existing `reset` action's
`confirm()` at `:3010`, which this file already uses for a comparable
destructive choice). Also correct the import-screen string at `:2941`
("nothing is dropped") to state accurately that persona/quiz/palette/
milestones update to the most-recently-changed copy rather than merging.
Never rename `pigment.taste.v1` or any of its field names (see F4-i).

**Onboarding persistence-or-warning (unit 11) — recommendation.** Two options
were specified; I recommend the **warning**, not persistence, as the smaller
correction:
- *Option A — persist `ob` to sessionStorage.* Requires serializing the full
  in-progress deck, `admired`/`skipped` arrays, and answer state on every
  step transition, **and** fixing that `obStart()` (`js/app.js:2549-2552`)
  reseeds via `Math.random()` on every call — true resume needs the seed (or
  the built deck) persisted too, not just progress counters. More surface
  area, more places to introduce a subtle bug.
- *Option B — `beforeunload` warning + explicit restart copy.* A single
  listener scoped to "onboarding in progress" (i.e., `ob !== null` and not
  yet at reveal) plus making `retake` (`:2982`) call `confirm()` the way
  `reset` already does at `:3010` (today `retake` sets `ob = null` with no
  confirmation and no `route()` call — a second, smaller bug worth folding
  into the same commit since it's the same code path).
Recommend **Option B**. It ships in ~15 LOC, touches no persistence format,
and directly satisfies criterion 6 ("explicit and recoverable" — recoverable
via warning-before-loss, not silent resume).

**`?v=` pattern — verified, not uniform.** Read `index.html:70-97` directly
this session. Cache-busted: `css/styles.css?v=20260717-card1`,
`js/artworks.js`, `js/influences.js`, `js/catalog-1.js`…`catalog-4.js`,
`js/tier1-artists.js`, `js/lists-1.js`, `js/personas.js`, `js/museums-1.js`,
`js/app.js?v=20260717-seo1` (all `?v=YYYYMMDD-slug`). **Not** cache-busted:
`js/taxonomy.js`, `js/worldmap.js`, `js/venues.js`, and all sixteen
`js/artists-1.js`…`artists-16.js` — these carry no query string at all. None
of the F2 units touch the unversioned files, so this plan is unaffected in
practice, but it is a pre-existing gap worth flagging once (see F4-ii) since
a future data-only fix to `artists-*.js` would need a version string added
for the first time, not just bumped.

---

```
F3 — CONTRAST WITHOUT NODE
```

**Token count — verified by direct read, not re-derived from the citations
in Caravaggio's document (which named the lines but not the full lists).**
The dark `:root{}` block (css:6-28) and the light `html[data-theme="light"]{}`
block (css:32-51) each define exactly the same **19 color-relevant custom
properties**, 1:1 paired across themes: `--bg`, `--bg-rgb`, `--bg2`, `--panel`,
`--panel2`, `--ink`, `--body-ink`, `--muted`, `--faint`, `--gold`, `--gold2`,
`--wine`, `--teal`, `--blue`, `--line`, `--line2`, `--shadow`, `--scroll1`,
`--scroll2`. Three more tokens in the dark block (`--serif`, `--sans`,
`--ease`) are typography/timing, not color, and are correctly **not**
redefined in the light block. `--line`/`--line2` are low-alpha rgba border
tokens, not solid fill/text pairs; `--shadow` is a box-shadow value; `--scroll1/2`
are scrollbar thumb/track (WCAG 1.4.11 non-text, 3:1 bar, not 1.4.3).

**Verdict: FEASIBLE, with a scoped method.** A `python3` script computing
WCAG 2.2 relative-luminance contrast ratios over **actually-used token
pairs** is straightforward — no Node, no DOM, and no network needed, since
every value is a static hex or rgba literal already extracted above for both
themes. It is not feasible to brute-force all 19×19 combinations meaningfully;
the script must first establish which token pairs are real
foreground/background combinations by parsing `css/styles.css` rule-by-rule
(map selector → declared `color`/`background`/`background-color`, resolving
`var()` indirection via the two token tables above), then compute ratios for
those pairs only. One necessary judgment call: rules that set only `color`
inherit their background from an ancestor selector (e.g. `.muted` text inside
`.card` inside `.panel`) — resolving that chain is a parsing/heuristic step,
not a browser dependency, but it is not pure lookup either; flag any
ambiguous inheritance chain in the script's output rather than guessing
silently.

**What genuinely needs a browser afterward:**
1. **Text over gradients** — light-theme `.home-hero-content h1` uses a
   `background-clip:text` linear-gradient (css:53-56, confirmed by direct
   read this session), so contrast varies continuously across the glyph;
   no single token pair captures it.
2. **Text/labels over generative covers** — `canvasTag` (`js/app.js:719-720`)
   paints a runtime-generated painterly background per view; any overlaid
   text's contrast against it is unknowable statically.
3. **Focus indicators** — outline color/width against whichever of several
   adjacent backgrounds (`--bg`, `--panel`, `--panel2`, card colors) a given
   focused control happens to sit on; a script can approximate per declared
   context but real rendering (or Vermeer's visual sampling, as already done
   for the 320px "Nations" focus-ring case in `browser-evidence.md`) is the
   only way to be certain across all contexts a ring can appear in.
4. **Alpha-composited tokens over non-`--bg` surfaces** — `--line`/`--line2`
   composited against `--panel`/`--panel2` rather than the flat page
   background; computable in principle (pre-composite the rgba against each
   candidate backdrop) but requires enumerating every backdrop a bordered
   element can sit on, which is closer to a rendering question than a
   lookup.

**Method sketch:** parse `css/styles.css` into declaration blocks → resolve
`var()` references against the two 19-entry token tables (dark, light) →
pair declared `color` with declared/inherited `background`/`background-color`
per selector → convert hex/rgba to sRGB → linear-light relative luminance
(`L = 0.2126R + 0.7152G + 0.0722B` after the standard gamma-linearization) →
`(L1+0.05)/(L2+0.05)` with L1 the lighter → threshold 4.5:1 normal text / 3:1
large text and non-text UI components → emit a pass/fail table per theme,
flagging any pair whose background could not be statically resolved.

---

```
F4 — ARCHITECTURAL RISK REGISTER
```

**(i) `pigment.taste.v1` compatibility rules.** `PASSPORT_KEY =
"pigment.taste.v1"` at `js/app.js:59`. The persona-overwrite guard (F2 unit
10) must be **additive only**: never rename `quiz`/`palette`/`persona`/
`milestones`/`admirations`/`seen`/`wantToSee`/`saved`/`probes`/`skipped`/
`deckSeen`/`notForMe`/`updatedAt`. The fix changes *when* a write happens
(gate behind confirmation for `persona.adopted` specifically), not the
stored shape — so a passport written before this ship still parses correctly
after it, and vice versa. If a new field is ever wanted (e.g., a
`persona.adoptedAt` timestamp or a confirmation flag), adding one is
compatible with §4.4's anti-drift rule; renaming or repurposing an existing
one is not (this is the same distinction Caravaggio's finding 12(b) already
established for Workstream I — it applies identically here).

**(ii) `?v=` bump procedure — verified this session (see F2).** Every commit
that changes `css/styles.css` or `js/app.js` must bump that file's own
`?v=YYYYMMDD-slug` string at `index.html:70-97`; every F2 unit's table row
states which. `index.html` itself carries no version string and needs none
(entry document). Files with **no** existing `?v=` at all (`taxonomy.js`,
`worldmap.js`, `venues.js`, `artists-1..16.js`) are outside this plan's scope
but represent a latent gap: the first future edit to any of them would need
a version string *added*, not bumped, or it silently relies on GitHub Pages'
default cache lifetime alone.

**(iii) `app.js` strict-mode IIFE — confirmed by direct read.**
`js/app.js` opens `(function(){\n"use strict";` and closes `route();\n})();`
at end of file — the entire module is one closure; there is exactly one
bootstrap call to `route()`, at the very last line, plus `hashchange`-driven
and in-app calls to the same function throughout (`:2110`, `:2126`, `:2145`,
`:2152` listener registration, `:2952` etc., `:3039` final bootstrap call).
Any new helper this plan introduces (a `displayName()` helper for unit 8, a
focus-management helper for unit 12) is invisible outside this file by
design and must be declared **inside** the IIFE, following the existing
convention of declaring shared helpers (`byId`, `Mx`/`Tx`/`Ex`/`Nx`/`Ax`,
`CatX`) near the top alongside related lookups — and, if it must run during
initial page load, before the final `route();` call. No unit in this plan
needs to run before that line except unit 12, which modifies `route()`
itself in place.

**(iv) GitHub Pages cache reality.** GitHub Pages serves static assets with
a default `Cache-Control: max-age=600` (10 minutes) — standard platform
behavior; not independently re-verified against this specific deployment's
live HTTP headers in this session (no network fetch performed). Combined
with (ii)'s non-uniform `?v=` coverage: a client that fetched an unversioned
file during a bad deploy window could hold it past the 10-minute cache
window even after a clean revert of the versioned files. Practical
consequence for the rollback procedure (Caravaggio finding 23): state
"redeploy the reverted commit, then allow ≥10 minutes or instruct a hard
refresh" rather than assuming instantaneous rollback.

**(v) Route/ID stability.** Cross-checked every F2 unit against
`ux-requirements.md` §1's 24-route table: none adds, removes, or renames a
route `case` value, an artist/artwork/museum `id`, or a `slug`. Unit 9
(Explore promise) changes only copy text at `js/app.js:1460-1465`, not the
`#/explore` route itself. Unit 8 (name-splitting) changes only *displayed*
string content, never the `id`/`slug` used in `href`s. No unit touches
`route()`'s `switch` statement's case values.

---

```
F5 — VALIDATOR & TEST DELTA
```

**Confirmed feasible, using a pattern the file already uses.**
`tools/validate.jxa.js` runs via `osascript -l JavaScript` (no Node), reads
files as raw strings via its own `read()` (`ObjC.NSString`-based, no DOM),
and **already** treats `js/app.js` two ways: (a) `new Function(read(...))`
for a syntax-only check (line ~16), and (b) as a raw string it regexes over
— `const appSrc = read(base + "js/app.js");` followed by
`let m, re = /^(\w+)\(ctx,w,h,P,R\)/gm; while((m = re.exec(appSrc)))
styleNames[m[1]] = 1;` to harvest generative-cover style function names.
This proves the harness can already do exactly the kind of static
source-text scanning new checks would need — no new capability required.

Proposed additions, each following the file's existing `errs`/`warns`-push
convention:
- **Nested-interactive scan** — a lightweight regex/bracket-matching pass
  over `appSrc` flagging a `<button` opened before the nearest preceding
  unclosed `<a`. This is a heuristic (JXA has no HTML parser/DOM), sufficient
  to catch a regression of the one known instance (F2 unit 5) but not a
  general nested-interactive guarantee — worth stating as a limitation in
  the check's own output.
- **Name-splitting pattern grep** — `/\.name\.split\(/g` count against
  `appSrc`; assert it drops to 0 (or a documented allow-list) once F2 unit 8
  ships.
- **`?v=` consistency check** — `read()` `index.html`, regex every
  `<script src="js/…">`/`<link …href="css/…">`, extract `?v=` suffixes, and
  assert every referenced file carries one. This would **currently fail**
  for the four unversioned files noted in F4-ii, so it should ship as a
  `warns` push (not `errs`) unless/until those files are backfilled with a
  version string — flagging that ordering dependency here so it isn't
  silently treated as a new hard failure.

All three are additions to the existing `errs`/`warns` arrays and the final
`out.push(errs.length ? …)` reporting block — no new tooling, no Node.

---

```
F6 — BRANCH STRATEGY
```

`git status` re-run this session: branch `main`, working tree has only the
already-known untracked files (`IVO_001.md`, `MIRA_001.md`, `SOREN_001.md`,
`THEORY_001.md`, `protocol/tasks/PIG-001/`) — no production file modified,
matching `intake-baseline.md` §2 exactly. **Nothing is built.** No branch was
created and no production file was opened in write mode during this
assessment.

**Branch to cut once `approved_for_build` is reached:** `pig-001-stabilization`.

**Rollback anchor:** commit `3c2e9fa45645d787da3754417448bbcebfd4029a` on
`main` (per `intake-baseline.md` §2; independently cross-confirmed by
`browser-evidence.md`'s own `git log -1` / `git diff HEAD -- css/ js/
index.html` check, which found the tracked production tree unmodified at
that SHA). Rollback procedure per F4-iv: redeploy the reverted commit, then
allow the GitHub Pages ~10-minute cache window to clear (or instruct a hard
refresh) before treating rollback as complete — not stated anywhere in
THEORY_001 (Caravaggio finding 23), and this document is the first place a
concrete procedure, not just a preference, is recorded for it.

---

```
SUMMARY VERDICTS
```

- **F1:** A, D, J = straightforward-verification. B, C, E, F, G = bounded-
  correction. H splits (verification + bounded-correction, per brief). I =
  blocked-on-decision, with a narrower rights-register exception that is
  startable today as a protocol artifact, not production code.
- **F2:** 14 commit-sized, independently-revertible units identified,
  ordered CSS-only/safest (1-3) → small isolated JS (4-9) → guard/warning
  fixes (10-11) → cross-cutting shared-code changes (12-13, route() and
  search ranking — highest care) → doc-only (14, outside Gate 1). Onboarding
  fix: recommend the `beforeunload`-warning option over sessionStorage
  persistence (smaller, no persistence-format risk). `?v=` bump pattern
  confirmed but **not uniformly applied** across all script includes —
  flagged, not a blocker for this plan.
- **F3:** 19 color tokens per theme, paired 1:1. A static `python3` WCAG
  contrast script over actually-used token pairs is feasible with no Node;
  genuinely browser-only for gradient text, generative-cover overlays,
  focus-indicator visibility across varying backdrops, and multi-surface
  alpha composites.
- **F4:** Merge fix must be additive-only against `pigment.taste.v1`; `?v=`
  bump is per-file and confirmed non-uniform; new helpers must live inside
  `app.js`'s single strict-mode IIFE, before the final `route();` call if
  needed at load time; GitHub Pages' ~10-minute cache means rollback isn't
  instantaneous; no F2 unit touches route/ID stability.
- **F5:** Validator additions (nested-interactive heuristic, name-split
  grep, `?v=` consistency) are feasible using the file's own existing
  read-as-string + regex pattern — no new capability needed, though the
  `?v=` check should land as a warning first given the four already-
  unversioned files.
- **F6:** Nothing built; `git status` confirms untracked-only working tree.
  Branch: `pig-001-stabilization`. Rollback anchor: `3c2e9fa4…` on `main`,
  with an explicit cache-clearing wait added to the procedure.
