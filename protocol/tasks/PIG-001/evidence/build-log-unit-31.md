# BUILD LOG — PIG-001 unit 31

**Author:** Dürer (`claude-implementation-lead`)
**Branch:** `pig-001-stabilization` (verified; never `main`; not pushed)
**Gate 1:** `protocol/tasks/PIG-001/specification.md:8` → `workflow_state: "approved_for_build"`. Satisfied.

Unit 31 closes **F-8**, the single open major from Van Eyck's quality review
revision 3 (`GATE 2: BLOCKED` · PASS 28 · FAIL 1 · AC19 FAIL), and corrects the
false clearance in unit 29's log that concealed it.

| item | commit |
| --- | --- |
| 31 — `.tl-year` → `--body-ink`; dated correction to unit 29's log; re-measurement of all eight `--faint` declarations | `03ebdde7d3520d35dd32bbb59666a35d02f47488` |

Files touched: `css/styles.css`, `index.html` (`?v=` → `20260729-pig001-u31`),
`protocol/tasks/PIG-001/evidence/build-log-unit-29.md` (dated correction, struck
not deleted), and two new instruments plus their raw data under
`protocol/tasks/PIG-001/evidence/harness/durer-u31/`. `js/app.js` is **not**
touched. No new dependencies. Committed by explicit path; the untracked
`THEORY_001.md`, `protocol/tasks/PIG-001/CHALLENGE_001` and
`protocol/tasks/PIG-001/THEORY_001` were left alone.

## What this unit is NOT

**The seam-closing enumeration required by Van Eyck's adjudication A13 is
Vermeer's work, not mine, and it is not in this log.** A13 rules that a host
census is insufficient for AC19, and that the ink enumeration over the four
`hero()` route families must be re-run **by someone other than its
implementer**. I implemented it; running it here would defeat the point of the
ruling. Nothing below should be read as, or counted towards, that verification.
This unit fixes one measured failure, corrects one false record, measures eight
ink call sites, and stops.

---

# 1 — THE FINDING, AND WHY IT SURVIVED

`.tl-year` (`css/styles.css:871` before this unit) is the era start/end year at
either end of the "Born along the century" rail. It renders on **all 8**
`#/era/*` routes (`js/app.js:2118`; `ERAS` in `js/taxonomy.js` has eight
members, 14th–21st century), at `.7rem` = **11.2 px**, in `--faint`.

Its parent `.timeline` (`css/styles.css:852-855`) declares `position:relative`,
margins, padding and two 1 px borders — **and no background**. The glyphs
therefore composite straight onto `#bg-canvas`, the site-wide generative canvas
unit 29 bounded from source. Against that bound only `--body-ink` and `--ink`
clear the 4.5 small-text floor.

Unit 29 §7.1 (`build-log-unit-29.md:342-345`) nevertheless listed `.tl-year`
among the `--faint` sites surviving **"all inside opaque panels"**, and
Matisse's D-29-6 ruling (`visual-ruling-d29-6.md:267-271`) adopted the claim as
settled. That sentence was a **reading of the stylesheet** — precisely the
method the enumeration was built to replace. It is my error and I am not
softening it. An unmeasured gap invites a later measurement; a false clearance
closes the question and takes a second reviewer with it. F-8 is the more
expensive of the two failure modes, and that is the durable lesson of this unit.

---

# 2 — THE FIX

```css
/* --body-ink, not --faint (unit 31, AC19/F-8). `.timeline` above declares no
   background, so these 11.2 px era years composite straight onto #bg-canvas on
   all 8 #/era/* routes — the ink rule at #bg-canvas applies to them and only
   --body-ink and --ink clear it. … */
.tl-year{position:absolute;bottom:14px;font-size:.7rem;color:var(--body-ink);letter-spacing:.12em}
```

**Van Eyck's specified remedy, verified before shipping it.** He computes
`--body-ink` at 5.01 light / 4.55 dark against unit 29's derived ceiling. I
re-derived it from the committed tokens with my own arithmetic (sRGB relative
luminance, WCAG 2.x) against the ceiling stated at `#bg-canvas` — worst
reachable backdrop `rgb(101,88,76)` dark, `rgb(187,174,162)` light:

| ink | dark | light |
| --- | --- | --- |
| `--faint` `#8b8372` / `#706755` | **1.83** | **2.58** |
| `--muted` `#9b937f` / `#585244` | 2.25 | 3.58 |
| **`--body-ink` `#d8d2c4` / `#433c31`** | **4.56** | **5.02** |
| `--ink` `#ece6d9` / `#2b2620` | 5.53 | 6.92 |

Reproduces his figures to ±0.01. **`--body-ink` clears in both themes and it is
the lowest rung that does** — `--muted` is not a candidate at any nearby value,
so there was no cheaper remedy to prefer. Confirmed, not assumed; §3.2 then
measures it on real pixels. No token was added and no value invented:
`--body-ink` is the ink the `#bg-canvas` rule already names for this case.

---

# 3 — MEASURED

## 3.1 Instrument

`protocol/tasks/PIG-001/evidence/harness/durer-u31/inkprobe.py`, new this unit,
built on `cdp-r2`. It is not another `canvastext.py` sweep, because that sweep
is **structurally blind to three of the six sites unit 29 cleared**:

| site | why unit 28's sweep cannot see it |
| --- | --- |
| `#search::placeholder` | a pseudo-element: it owns no text node, so `DETECT`'s walk never enumerates it |
| `.tn-count`, `.tm-lab` | SVG `<text>`: the ink is `fill:`, and `HIDE` sets `color` / `-webkit-text-fill-color`, so shot A equals shot B, no glyph pixels are found, and the row silently disappears from every table |
| `.sr-group`, `.sr-more` | only exist after a query is typed into the header search, which no sweep does |

So the probe is driven **by selector**, hides the target's ink with an injected
rule (which reaches pseudo-elements and `fill:` alike), and drives each site's
precondition — typing a query, opening the family-tree view, seeding a passport.
**This is what makes `.tn-count` and `.tm-lab` measurable rather than
unverified**, which is the state Van Eyck reported he had to leave them in.

**Four shots** per (site, draw): **A** as rendered; **B** target ink
transparent; **C** = B + `#bg-canvas` `display:none` → `canvasDelta`; **D** = B
+ every cover canvas `visibility:hidden` → `coverDelta`. A pixel is a glyph
pixel where A and B differ by ≥ 60; its backdrop is **B**, the surface as
actually composited. `canvasDelta > 0` means the generative canvas is in that
backdrop; `coverDelta > 0` means a `canvasTag()` cover is; both zero means
opaque paint and a deterministic backdrop.

Inherited corrections, both load-bearing, both from unit 30:

- **clip origin (V-F2)** — `Page.captureScreenshot`'s `clip` is in page
  coordinates while rects are in viewport coordinates; `scrollY` is added at the
  capture so the per-element arithmetic stays in viewport space.
- **`visibility:hidden` for covers, never `display:none`** — several
  `canvasTag` sites emit an in-flow canvas and `display:none` reflows the
  document between shots. `#bg-canvas` is `position:fixed`, so `display:none`
  there moves nothing and unit 28's rule still applies to it.

Added this unit, after a first run produced a nonsense row: a **stability
guard**. The header search panel re-renders on its own input debounce and resets
its own `scrollTop`; if that lands between shots A and B the differential
compares two different documents. The probe now re-locates after the four shots
and **discards** any batch whose measured rects moved. The first (unguarded) run
is kept at `harness/durer-u31/superseded-run1/` rather than deleted; every
number below comes from the guarded re-run, and the guard tripped **zero times**
in it.

`prefers-reduced-motion: reduce` is emulated so the canvas paints one static
t = 0 frame; it is `Math.random`-seeded per load, so every site is loaded
**N = 4 draws** behind a unique query string and the **worst** value over all
draws is reported. Four cells: {light, dark} × {1440×900, 390×844}.

## 3.2 `.tl-year` — before → after

Same build, same instrument, same operator; **before** is the shipped
pre-unit-31 declaration restored at runtime
(`U31_BEFORE_CSS='.tl-year{color:var(--faint)!important}'`), so only the one
declaration under test differs. **N = 4 draws** per cell per route; 8 measured
rows per cell per route (2 elements × 4 draws). Worst observed:

| theme | viewport | route | before (`--faint`) | after (`--body-ink`) | backdrop |
| --- | --- | --- | --- | --- | --- |
| light | 1440×900 | `#/era/16th-century` | **4.13 FAIL** | **7.04 pass** | `#bg-canvas` |
| light | 1440×900 | `#/era/19th-century` | **4.16 FAIL** | **7.10 pass** | `#bg-canvas` |
| light | 390×844 | `#/era/16th-century` | **3.69 FAIL** | **7.18 pass** | `#bg-canvas` |
| light | 390×844 | `#/era/19th-century` | **3.68 FAIL** | **7.20 pass** | `#bg-canvas` |
| dark | 1440×900 | `#/era/16th-century` | **4.38 FAIL** | **11.13 pass** | `#bg-canvas` |
| dark | 1440×900 | `#/era/19th-century` | 4.63 pass | **12.37 pass** | `#bg-canvas` |
| dark | 390×844 | `#/era/16th-century` | **4.49 FAIL** | **10.76 pass** | `#bg-canvas` |
| dark | 390×844 | `#/era/19th-century` | **4.41 FAIL** | **11.24 pass** | `#bg-canvas` |

Ink `rgb(112,103,85)` → `rgb(67,60,49)` light; `rgb(139,131,114)` →
`rgb(216,210,196)` dark. Floor 4.5 (11.2 px is small text).

**Worst observed after the fix: 7.04, against a 4.5 floor. 7 of the 8
route×cell pairs failed before; 0 fail after.** `overCanvas` is still `true` on
every row after the fix — the surface did not change, the ink did, which is the
remedy the `#bg-canvas` rule prescribes.

Two notes on the before column, both against my own comfort:

- It is **worse than Van Eyck's** (he measured 4.06–4.47). Four draws found
  darker light-theme corners than his four did. His finding is not merely
  reproduced, it is understated.
- **Dark 1440×900 `#/era/19th-century` passed at 4.63 before the fix.** One cell
  of eight. If that cell had been the only one walked, the site would have read
  as clear — which is a second, quieter illustration of the same lesson: a
  single-cell pass on a `Math.random` surface is not a clearance.

## 3.3 The other seven `--faint` declarations — measured, not asserted

Unit 29 named six sites. `css/styles.css` has **eight** `--faint` declarations:
`.sr-kicker` in that list is two rules (`.sr-group` `:448` and `.sr-more`
`:460`), and `.tl2-year` (`:1183`) appears in no unit-29 list at all. All eight
are below; `.tl-year` is the one fixed above.

Worst observed over 4 draws per cell. "surface" is the **measured** answer from
the C/D shots, not a reading of the CSS: `canvasDelta` and `coverDelta` are both
**0** on every row in this table, i.e. none of these seven touches `#bg-canvas`
or any `canvasTag` cover.

| # | selector | line | px | host | light 1440 | dark 1440 | light 390 | dark 390 | surface (measured) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `#search::placeholder` | 439 | 14.1 | `#search` `--panel` | 5.17 pass | 4.90 pass | 5.17 pass | 4.90 pass | opaque paint |
| 2 | `.search-results .sr-group` | 448 | 9.9 | `.search-results` `--panel2` | 4.62 pass | 4.62 pass | **1.00 †** | **1.04 †** | opaque paint |
| 3 | `.search-results .sr-more` | 460 | 11.5 | `.search-results` `--panel2` | 4.62 pass | 4.62 pass | 4.62 pass | 4.62 pass | opaque paint |
| 4 | `.tree-svg .tn-count` (movements) | 1158 | 11.0 | `.tree-wrap` `--panel` | 4.62 pass | 4.62 pass | 4.62 pass | 4.62 pass | opaque paint |
| 5 | `.tree-svg .tn-count` (techniques) | 1158 | 11.0 | `.tree-wrap` `--panel` | 4.62 pass | 4.62 pass | 4.62 pass | 4.62 pass | opaque paint |
| 6 | `.tm-lab` | 1473 | 10.0 | `.taste-map` `--panel` | 5.17 pass | 4.90 pass | 5.17 pass | 4.90 pass | opaque paint |
| 7 | `.pp-card-loading` | 1493 | 13.6 | `.pp-card-prev` `--panel` | 5.17 pass | 4.90 pass | 5.17 pass | 4.90 pass | opaque paint |
| 8 | `.tl2-year` | 1183 | 11.2 | `.tl2-wrap` `--panel` | **3.78 FAIL** | **3.63 FAIL** | **3.78 FAIL** | **3.63 FAIL** | opaque paint — **N-31-1** |

Rows measured per cell: `sr-group` 12, `sr-more` 4, `tn-count` 92–192,
`tn-count-tech` 96–156, `tm-lab` 16, `pp-card-loading` 4, `tl2-year` 16–32,
`search-ph` 4. Raw data: `harness/durer-u31/ink-after-*.json`.

**Nothing here is marked unverified.** Van Eyck flagged `.tm-lab` and
`.tn-count` as SVG `fill:` inks he could not reach; the injected-rule HIDE does
reach `fill:`, so both are measured on real glyph pixels in all four cells, and
I am clearing them **on measurement**, not for a second time on assertion. Every
one of the seven is confirmed to be on opaque paint — which is what unit 29
claimed for six of them, and it happened to be true for those six. It was not
true for `.tl-year`, and the method could not have told the difference.

### † `.sr-group` at 390 px is **not** a `.sr-group` contrast defect — N-31-2

The 1.00 / 1.04 figures are real pixels and I am not discarding them, but they
do not measure this ink against its own backdrop. At 390 px the header's
`.main-nav` row is painted **over** the open search-results panel and its links
collide with the first group label. The worst "glyph pixel" is where `--faint`
`MUSEUMS` sits underneath a dark nav link.

Attributed by measurement, not by argument
(`harness/durer-u31/attribute.py`, 3 draws, one layer suppressed):

```
as shipped  light 390x844  .search-results .sr-group  worst 1.00  ink [112,103,85] on [110,103,92]  'Museums'
suppressed  light 390x844  .search-results .sr-group  worst 4.62  ink [112,103,85] on [240,233,218] 'Museums'
as shipped  dark  390x844  .search-results .sr-group  worst 1.04  ink [139,131,114] on [139,134,123] 'Museums'
suppressed  dark  390x844  .search-results .sr-group  worst 4.62  ink [139,131,114] on [29,26,19]    'Museums'
```

With `.main-nav{visibility:hidden}` the site reads **4.62 pass** in both themes
— identical to its 1440 px value. So `.sr-group`'s own backdrop is `--panel2`
and it clears; the failure is an **overlap defect in the mobile header**, not an
ink defect. Screenshot evidence:
`harness/durer-u31/n31-2-nav-overlaps-search-390-light.png`. Recorded as
**N-31-2 (new, unfixed, out of this brief)** — `.main-nav` and `.search-results`
both compute `z-index:auto` inside a wrapping `.site-header`, and the panel is
`position:absolute; top:calc(100% + 8px)` on a 220 px wrapper. Deciding the
remedy is a UX/visual call, not an ink call.

### N-31-1 — `.tl2-year` fails on the 1 px gridline behind it

`.tl2-year` (`:1183`) is the grand timeline's century labels, 11.2 px `--faint`,
with a `.now` variant in `--gold2` (`:1185`). It is panel-hosted — and it still
fails, because `.tl2-grid` draws a 1 px vertical rule at exactly the century
position and `.tl2-year` is centred on it (`transform:translateX(-50%)`), so the
line passes through the glyphs. Attributed the same way:

```
as shipped  light 1440x900  .tl2-year  worst 3.78  ink [112,103,85]  on [225,211,183]  '1300'
suppressed  light 1440x900  .tl2-year  worst 5.13  ink [112,103,85]  on [249,245,235]  '1600'
as shipped  light  390x844  .tl2-year  worst 3.78  ink [112,103,85]  on [225,211,183]  '1300'
suppressed  light  390x844  .tl2-year  worst 5.17  ink [112,103,85]  on [250,246,236]  '1300'
as shipped  dark  1440x900  .tl2-year  worst 3.63  ink [232,201,138]  on [119,99,57]   'today'
suppressed  dark  1440x900  .tl2-year  worst 4.90  ink [139,131,114]  on [22,20,15]    '1300'
as shipped  dark   390x844  .tl2-year  worst 3.63  ink [232,201,138]  on [119,99,57]   'today'
suppressed  dark   390x844  .tl2-year  worst 4.90  ink [139,131,114]  on [22,20,15]    '1300'
```

With `.tl2-grid{visibility:hidden}` it clears in both themes (5.13–5.17 light,
4.90 dark). In dark the binding element is the `.now` label in `--gold2` over
the gold `now` rule, not `--faint`. So this is a **flat-paint** contrast defect,
not an AC19 `#bg-canvas` one, and its remedy is geometric (offset the label off
the rule, or give it a chip) rather than an ink swap.

**Recorded, not fixed.** My brief is explicit — fix `.tl-year`, correct the log,
measure the siblings, stop — and unlike D-30-6 this is a *different* surface
class from the finding under repair, so folding it in would reopen certified
flat-paint evidence at the last criterion. It is stated here so that it is a
known open item and not a second false clearance. **Two of eight `--faint`
declarations therefore end this unit failing their floor: `.tl2-year` in all
four cells (N-31-1), and `.sr-group` at 390 px only, by occlusion (N-31-2).**

---

# 4 — THE CORRECTION TO UNIT 29's LOG

`build-log-unit-29.md` §7.1 is **amended in place, not rewritten**: the false
sentence is struck through (`~~…~~`) and left legible, and a dated correction
block follows it in the style the Decision Record uses. Nothing was deleted. The
text added is:

> **CORRECTION — 2026-07-29, unit 31, re F-8 (Van Eyck, quality review rev 3
> §R3.3).** The struck sentence above is **false as written, and it was accepted
> as settled** — Matisse's D-29-6 ruling (`visual-ruling-d29-6.md:267-271`)
> repeats it. Two errors, and the second is the worse one:
>
> **(a) `.tl-year` is not inside an opaque panel.** `.timeline`
> (`css/styles.css:852-855`) declares `position`, margins, padding and two
> borders and **no background**, so the era start/end years composite directly
> onto `#bg-canvas` on all 8 `#/era/*` routes. Van Eyck measured 4.06–4.47
> against a 4.5 floor on real pixels; unit 31 reproduced it worse still — worst
> of 4 draws per cell: **3.68** light 390×844, **4.13** light 1440×900, **4.38**
> dark 1440×900, **4.41** dark 390×844. Fixed in unit 31 by re-pointing
> `.tl-year` to `--body-ink` (7.04–12.37 after).
>
> **(b) The clearance was asserted, not measured.** No instrument in unit 29
> could see three of the six sites — `#search::placeholder` is a pseudo-element
> with no text node, and `.tn-count`/`.tm-lab` are SVG `fill:` inks that unit
> 28's `color`-based glyph differential cannot hide. "All inside opaque panels"
> was a reading of the stylesheet, which is precisely the method the enumeration
> was built to replace. A false clearance propagates further than an unmeasured
> gap: an unmeasured gap invites a later measurement, a clearance closes the
> question.
>
> **(c) The list was also incomplete.** `--faint` has **eight** declarations in
> `css/styles.css`, not six: `.sr-kicker` names two (`.sr-group` at `:448` and
> `.sr-more` at `:460`), and `.tl2-year` (`:1183`, the grand timeline's gridline
> years) appears in no unit-29 list at all. Unit 31 measures it at **3.78** light
> / **3.63** dark, below the 4.5 floor — on opaque panel paint, so it is a
> flat-paint contrast defect rather than an AC19 `#bg-canvas` one. Recorded by
> unit 31 as **N-31-1**, not fixed there, and not covered by this correction.
>
> Unit 31 re-measured all eight sites on real rendered pixels in both themes at
> 1440×900 and 390×844; the table is in
> `protocol/tasks/PIG-001/evidence/build-log-unit-31.md` §3. The sentence above
> is struck rather than deleted because the record of the error is the useful
> part. — Dürer

The stylesheet carries the same correction where the next author will meet it:
the comment now above `.tl-year` states that unit 29's list was wrong for this
selector, and the `--faint` note at `#bg-canvas` points at N-31-1.

The block's figures are the guarded run's, i.e. §3.2's. (An earlier draft quoted
the first, unguarded run — 3.54 / 4.34; those numbers are superseded and appear
nowhere in the committed text. Both runs fail the same floor in the same cells.)

**Not corrected by me:** Matisse's `visual-ruling-d29-6.md` repeats the false
claim at `:267-271`. It is his artifact, not mine, and my role does not permit
editing another agent's protocol record. Flagged here for the Synthesis Lead.

---

# 5 — DEVIATION LEDGER

| id | deviation | why | effect | disposition |
| --- | --- | --- | --- | --- |
| **D-31-1** | New instrument (`inkprobe.py`) rather than another `canvastext.py` sweep | Three of the six sites under review are structurally invisible to the unit-28 sweep (pseudo-element; SVG `fill:`; requires typed input). Re-running it would have returned "not present" and re-cleared them by silence | `.tn-count` and `.tm-lab` move from **unverified** to measured in all four cells | **Accepted** |
| **D-31-2** | Stability guard added mid-unit; first run superseded | The search panel's own input debounce can re-render between shots A and B; one `.sr-group` row scored 1.00 against a backdrop equal to its own ink | Guard discards moved batches. Zero trips in the final run. Superseded run retained under `superseded-run1/`, not deleted | **Accepted** |
| **D-31-3** | `visible_frac >= 0.9` instead of full viewport containment | `.search-results` is `right:0` on a 220 px wrapper and 335 px wide, so at 390 px every `.sr-group` reports `left = -2` — a 2 px sliver off-screen with all glyphs painted. Strict containment reported the site unverified, i.e. a coverage gap dressed as a limitation | `.sr-group`/`.sr-more` measured at 390 px in both themes | **Accepted** |
| **D-31-4** | `.pp-card-loading` measured after re-instating its own markup | The state is transient: `viewTaste()` schedules `drawCardPreview()` on the next animation frame, which replaces the holder. The markup injected is `js/app.js:3457` verbatim into its own real host on the real route — the host, its paint and the page are the shipped ones; only the moment is forced | Site measured rather than declared untestable. Stated, not hidden | **Accepted** |
| **D-31-5** | A passport is seeded in `localStorage` for `#/taste` | Without admirations the route renders its empty state and neither `.tm-lab` nor `.pp-card-loading` exists | Two sites measurable. Seed is in the instrument, visible and reproducible | **Accepted** |
| **D-31-6** | Family-tree view clicked open for `.tn-count` | `taxIndexView` defaults to cards; the tree is behind a `data-view="tree"` toggle, so no route-loading sweep ever renders that ink | `.tn-count` measured on two taxonomies | **Accepted** |
| **D-31-7** | Four cells measured, not the two Van Eyck used | He measured light 1440 and dark 390. The extra two cells found dark 1440 `#/era/19th-century` **passing** before the fix at 4.63 | Prevents a single-cell pass being read as a clearance — the same error class as F-8 | **Accepted** |
| — | **N-31-1** (`.tl2-year` on its gridline) **not fixed** | Different surface class from the finding under repair (flat paint, not `#bg-canvas`), and the remedy is geometric rather than an ink swap; fixing it would reopen certified flat-paint evidence at the last criterion | Measured, attributed, recorded open | **Deferred**, referred to Matisse/Mondrian |
| — | **N-31-2** (`.main-nav` over `.search-results` at 390 px) **not fixed** | A layout/stacking defect found by an ink probe; out of this brief, and the remedy is a UX call | Measured, attributed, screenshot attached, recorded open | **Deferred**, referred to Mondrian |
| — | The A13 seam-closing enumeration **not run** | A13 requires it to be run by someone other than its implementer. I am its implementer | Left to Vermeer, explicitly | **Correct by design** |

---

# 6 — NOT TESTED / NOT CLAIMED

Explicit, and not inferred from anything.

1. **The A13 ink enumeration over the four `hero()` route families.** Not run
   here, by design. It is Vermeer's.
2. **`#/era/*` beyond two of the eight eras.** `#/era/16th-century` and
   `#/era/19th-century` were measured. The other six render the identical
   `.timeline` markup from the same builder with the same ink and the same
   (absent) parent background, so the *fix* is structural — but I did not load
   them, and I am not claiming I did.
3. **Browsers other than Chrome**, `deviceScaleFactor: 1`, headless.
4. **Real assistive technology.** No VoiceOver/NVDA/JAWS session.
5. **200 % text zoom.** `.tl-year` is absolutely positioned at `bottom:14px`
   inside a 56 px bottom padding; not re-measured under zoom.
6. **`--muted` call sites.** Out of this brief; unit 29's treatment stands.
7. **N-31-1 and N-31-2 remedies.** Measured and attributed, not designed, not
   implemented, not verified.
8. **Van Eyck's F-1 and F-2.** Outside this brief; both stand as recorded.
9. **Deployed identity.** Everything measured against a local `http.server` on
   port **8437** (a long-lived server holds 8421; it was not disturbed).

---

# 7 — VALIDATOR

`osascript -l JavaScript tools/validate.jxa.js`, run at the committed tree:

```
app.js: syntax OK
artists: 256, movements: 76, techniques: 39, eras: 8, nations: 37, painter styles: 27,
influence edges: 238, venues: 116, catalog: 323 (tier1: 76), daily pool: 75,
museum notes: 104, photo credits: 104 (attribution required: 88),
artwork image credits: 27, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```

Zero errors, **zero warnings**, all references valid — byte-identical to the run
in Van Eyck's revision 3 §R3.2.1. This unit touches no data file, so this is a
regression check, not evidence of new work.

---

# 8 — PREVIEW

```
git checkout pig-001-stabilization
python3 -m http.server 8437 -d .
open http://localhost:8437/index.html#/era/16th-century
```

Toggle the theme with the header control. The two years at either end of the
"Born along the century" rail are the subject; they are now `--body-ink`, the
same weight as body copy, on all eight eras.

---

# 9 — SELF-ASSESSMENT

**AC19 / F-8: closed.** `.tl-year` measured at 3.68–4.63 before and 7.04–12.37
after, across four cells × two era routes × four draws, on the same instrument
with only that declaration changed. All eight `--faint` declarations are now
measured rather than asserted, and their backdrops are attributed by paint
differential rather than by reading the stylesheet.

**Two new findings are left open and named** (N-31-1, N-31-2), both measured,
both attributed, neither fixed. **I do not certify Gate 2** — that is Van Eyck's
call, and the A13 enumeration it depends on is Vermeer's.
