# BROWSER EVIDENCE — PIG-001 · the seam-closing (ink, size, backdrop) enumeration

**Author:** Vermeer (`claude-browser-reviewer`). **Not** the author of any fix
under test. This document exists because of Van Eyck's **A13** and **F-8**
condition 3: *"the ink enumeration must be re-run … by someone other than its
implementer."*

**ENVIRONMENT**

| | |
| --- | --- |
| commit under test | `a716397` (branch `pig-001-stabilization`), working tree clean but for the three pre-existing untracked files and this unit's own harness |
| browser | Google Chrome, headless (`--headless=new`), `--force-device-scale-factor=1`, `deviceScaleFactor` 1 |
| driver | `harness/cdp-r2/cdp.py` (stdlib CDP client, inherited) |
| serve | `python3 -m http.server 8437 -d .` — my own port; nothing else was touched |
| media | `prefers-reduced-motion: reduce` emulated, so `#bg-canvas` paints one static `t=0` frame per load and the four shots compare the same pixels |
| build verified | `.tl-year` reads `color:var(--body-ink)` at `css/styles.css:881` (unit 31's fix) before any capture |

---

## 1 — METHOD, AND WHY THIS METHOD

### 1.1 The reporting unit is the triple, not the host

Van Eyck's ruling in **A13** is that AC19's unit is the **(ink, size, backdrop)
triple**, and that a host census cannot close it because *"an unwalked route can
introduce a new ink over an old backdrop."* So this enumeration is keyed on
`(ink RGB, font-size + weight, measured backdrop class)` and a selector appears
only as an *example* of a triple, never as the key.

### 1.2 The backdrop is measured, never read

Every backdrop in this document is a **paint differential** on real rendered
pixels. Four screenshots per (route, draw, scroll band):

| shot | what it is | what it yields |
| --- | --- | --- |
| **A** | the page as rendered | — |
| **B** | every glyph's ink forced transparent | a pixel is a **glyph pixel** where \|A−B\| ≥ 60; its **backdrop is B** |
| **C** | B, plus `#bg-canvas` `display:none` | `canvasDelta` = max\|B−C\| over the glyph pixels |
| **D** | B, plus every `canvasTag()` cover `visibility:hidden` | `coverDelta` = max\|B−D\| |

`canvasDelta > 0` ⇒ the generative site canvas is part of that backdrop.
`coverDelta > 0` ⇒ a cover canvas is. Both `0` ⇒ deterministic opaque paint, and
the exact RGB is recorded. **No verdict in this document is derived from reading
`css/styles.css`.** That distinction is the entire lesson of F-8: unit 29 read
the stylesheet, concluded `.tl-year` was "inside an opaque panel", and was wrong.

Ink is never hidden with `visibility:hidden` (that would delete the element's own
background too) and never with `display:none` (unit 30: in-flow cover canvases
reflow the document between shots). Both corrections are inherited, as is unit
30 / V-F2's clip-origin fix — `Page.captureScreenshot`'s `clip` is in **page**
coordinates while `getBoundingClientRect()` is in **viewport** coordinates, so
`scrollY` is added at the capture and all per-pixel arithmetic stays in viewport
space.

### 1.3 The occlusion guard — the one thing I added, and it changed the answer

`.site-header` is `position:sticky; z-index:50; background:rgba(var(--bg-rgb),.78)`
with a 14 px `backdrop-filter`. Body content scrolling underneath it composites
**through a translucent bar**, so a glyph caught mid-scroll measures against a
backdrop that is partly the header.

My first run of this instrument, without the guard, reported failures of **1.07
on `#/daily`** and **1.09 on `#/timeline`** at 390 px. Both were text in transit
under the sticky header. Reporting them as AC19 failures would have manufactured
findings; averaging them into the table silently would have put false numbers
into a certification package. So:

- every `position:fixed`/`sticky` element that actually paints (non-zero
  background alpha **or** a backdrop-filter) is enumerated per band as an
  **overlay**;
- an overlay counts against an element only when it is **not that element's own
  ancestor** — which keeps `.search-results` (absolutely positioned *inside* the
  sticky header) fully measurable while still catching `.main-nav` painting over
  it. That distinction is the whole of the N-31-2 question;
- glyph pixels under a counting overlay are scored **separately** (`worstOccluded`)
  and are **not** part of any AC19 verdict; the verdict comes from the
  unoccluded pixels;
- an element with **no** unoccluded glyph pixel at its band is recorded as
  `fullyOccluded` and is **not cleared** — it is carried into NOT TESTED.

### 1.4 Instruments

All four are new for this unit and live in
`protocol/tasks/PIG-001/evidence/harness/vermeer-u32/`.

| file | what it does |
| --- | --- |
| `triple.py` | the route walk: every element that owns a text node, plus SVG `<text>`/`<tspan>`, over the full route table, four shots per band, occlusion-aware |
| `sitecensus.py` | the selector-driven pass for what no walk can reach — `::before`/`::after`, `::placeholder`, state-only surfaces — plus `scan` mode, which enumerates the pseudo-element perimeter **from the DOM** rather than from my reading of the CSS, and `V32_SUPPRESS`, which hides one named layer so a failure can be **attributed** rather than argued |
| `states.py` | hover and focus ink, via CDP `CSS.forcePseudoState` — the engine is asked for the state rather than the state being simulated. Only elements whose ink **actually changes** are measured |
| `capture.py` | screenshots, Coordinator naming |
| `pngfast.py` | PNG reader. Verified **byte-identical** to the certified `cdp-r2/png.py` on 6 real shots of this run, and its `ratio()` agrees to 0.00e+00 over 4 000 random colour pairs |

### 1.5 What each instrument can and cannot see

Stated here rather than discovered later, because A13's finding was a perimeter
failure, not a counting failure.

**`triple.py` can see:** HTML elements owning a text node (ink = `color`, or the
gradient stops when `-webkit-background-clip:text`); SVG `<text>`/`<tspan>` (ink
= `fill`, hidden with an injected `fill:transparent` rule — this is the class
Van Eyck recorded in **A16** as invisible to `enumerate_overcanvas.py`, which
reads `getComputedStyle().color` and therefore mis-reads every `fill:` ink).

**`triple.py` cannot see:** `::before`/`::after` and `::placeholder`. They own no
text node and no rect of their own, so a walk cannot enumerate them and could not
separate their glyph pixels from their host's if it did. They are covered by
`sitecensus.py` instead, and the site list is derived from `scan` mode's DOM
enumeration, not from grepping the stylesheet.

**Neither can see:** the focus **ring**. A ring is not a glyph, so a glyph
differential cannot measure it. WCAG 1.4.11 ring contrast is **NOT TESTED** here
except where unit 30 already measured it on `.hero`.

---


## 2 — WHAT WAS RUN

| pass | instrument | cells | scope | result file |
| --- | --- | --- | --- | --- |
| 1 — route census | `triple.py` | light/dark × 1440×900/390×844 (**4/4**) | **33 routes** (26 `route()` cases + the other 7 `#/era/*`), 1 draw, ≤8 scroll bands, dry-band exit | `triple-p1-{light,dark}-{1440,390}.json` — **15 894 rows** |
| 2b — selector census | `sitecensus.py probe` | 4/4, **draw 0 complete in all four** | 24 sites: pseudo ink, SVG `fill:` ink, state-only surfaces | logs only — see §2.1 |
| 2c — N-31-1 | `sitecensus.py` ± `V32_SUPPRESS='.tl2-grid'` | 4/4 | `.tl2-year`, `.tl2-year.now` | `site-n311*-*.json` |
| 2d — N-31-2 | `sitecensus.py` ± `V32_SUPPRESS='.main-nav'` | light/dark @390 | `.sr-group/.sr-more/.sr-meta/.sr-name` | `site-n312*-*.json` |
| 2e — populated passport | `triple.py` `V32_PASSPORT=1` | 4/4 | `#/taste`, `#/palette`, `#/daily`, `#/lists` | `triple-pop-*.json` — 1 202 rows |
| 2f — hover/focus | `states.py` | 4/4 | 26 routes, ≤26 controls/route, CDP `forcePseudoState` | `state-*.json` — **1 181 rows** |
| 2g — graph attribution | `sitecensus.py` ± `.ig-edge`, ± `.ig-edge,.ig-node circle` | 4/4 | `.ig-node text` | `site-ig*-*.json` |

### 2.1 — One pass degraded, disclosed rather than smoothed over

The four **2b** runs were launched concurrently and Chrome died on each of them
partway through draw 1 (`ConnectionResetError` / `socket closed` — four headless
Chromes plus four pixel loops on an 8-core machine). Because `sitecensus.py`
prints each site's result with `flush=True` and only dumps JSON at the end, **draw
0 is complete and legible in all four logs and no JSON was written.** So:

- the 2b numbers quoted below are cited to `log-site-<cell>.txt`, at **1 draw**,
  not the 3 intended;
- for the sites that matter this is not the binding evidence anyway — `.tl2-year`,
  `.sr-group` and `.ig-node text` all have complete 2-draw JSON from 2c/2d/2g;
- the pseudo-element **perimeter scan** (`sitecensus.py scan`) died the same way
  and produced **no output at all**. The pseudo-element site list in this document
  is therefore derived from **my reading of the stylesheet**, not from a DOM
  enumeration. **That is the exact weakness A13 rejected**, so the pseudo class is
  reported as bounded-by-reading and is listed in NOT TESTED, not cleared.

**Route census totals:** 15 894 rows → **15 341** with at least one unoccluded
glyph pixel, **553** fully occluded (carried to NOT TESTED, not cleared).
**328 distinct (ink, size, backdrop-class) triples. 6 below floor.**

---

## 3 — THE FAILING TRIPLES

Six of 328 triples measured below floor in the route census. Two more were found
only by the selector pass, and one only by the hover/focus pass. All nine are
below, severity-tagged, each tied to AC19 (*"both themes pass AA for frozen
text/control/focus/state pairs incl. browser-measured composites"*).

`not measured` in a cell means exactly that — it is never a pass.

### V32-1 (major) · `.ig-node text` — SVG `fill:` labels crossed by graph edges and node circles

| | |
| --- | --- |
| selector | `.ig-node text` (`css/styles.css:1229-1232`, `fill:var(--muted)`, `font-size:10.5px`), emitted at `js/app.js:1197` as `<text y="r+12">` |
| route | `#/influences` |
| size / floor | 10.5 px, weight 300 → **4.5** |
| backdrop (measured) | flat SVG paint inside `.ig-wrap{background:var(--panel)}` — `.ig-edge` strokes and neighbouring `.ig-node circle` fills, which are **hard-coded movement palette hexes** (`vivid(mov.palette)`, `js/app.js:1190`), not theme tokens |

| cell | light@1440 | light@390 | dark@1440 | dark@390 |
| --- | --- | --- | --- | --- |
| route census (174 rows) | **1.27** | **1.27** | **1.04** | **1.26** |
| selector probe, 2 draws | **1.39** | **1.39** | **1.04** | **1.01** |

**Attributed by suppression, not by argument** (`site-ig*-*.json`):

| layer state | light@1440 | dark@390 |
| --- | --- | --- |
| as shipped | 1.39 FAIL | 1.01 FAIL |
| `.ig-edge{visibility:hidden}` | 1.41 **still FAIL** (now on a circle, `#c4302a`) | 1.14 **still FAIL** (`#c19845`) |
| `.ig-edge` **and** `.ig-node circle` hidden | — | **6.02 pass** (`#161…` = `--panel`) |

So the ink is fine on its host panel; **both** overlapping layers contribute, and
suppressing only one does not clear it. Not occluded (`occludedPx` 0), not
`#bg-canvas` (`canvasDelta` 0 on the binding rows), at rest, no scrolling, in
**all four cells**.

**Why no prior pass saw it.** `#/influences` **is** in unit 28/29's route list —
it was walked. But `enumerate_overcanvas.py` reads `getComputedStyle().color`,
and this ink is `fill:`, so its ink was **mis-read**, and unit 28's HIDE sets
`color`, so shot A equalled shot B and the element **dropped silently out of every
table**. This is the failure mode Van Eyck recorded in **A16** as unverifiable.
Unit 31 reached the SVG class correctly with an injected rule, but enumerated only
the two members Van Eyck had named (`.tn-count`, `.tm-lab`) — `.ig-node text` and
`.map-dot .md-name` are in **no** prior list. **This is F-8's pattern repeating on
a different axis: not an unwalked route, but an unreadable ink on a walked one.**

Evidence: `v32-influences-svg-labels__desktop-1440x900__light.png`,
`v32-influences-svg-labels__mobile-390x844__dark.png` — the teal and gold
relationship strokes are visibly drawn through the painter names.

### V32-2 (major) · `#ig-svg.focused .ig-node.lit text` — the focused graph's own labels

`css/styles.css:1237` re-inks the lit labels to `--ink` when a node is chosen.
Measured with the state driven for real (a click on `.ig-node`):

| | light@1440 | light@390 | dark@1440 | dark@390 |
| --- | --- | --- | --- | --- |
| worst, 10.5 px, floor 4.5 | **3.29** | **3.29** | **2.72** | **2.72** |

Same geometry as V32-1 and the same remedy space. A **state-only** ink: it exists
on no route at rest, so no at-rest sweep in this build could have scored it.
Source: `log-site-*.txt` (1 draw — see §2.1).

### V32-3 (major) · `button.chip:hover` paints `#fff` on warm paper in light theme

| | |
| --- | --- |
| rule | `.chip:hover{transform:translateY(-2px);color:#fff}` — `css/styles.css:515` |
| why it survives | unit 29 closed this exact defect with `html[data-theme="light"] a:hover{color:var(--ink)}` (`css/styles.css:274`). That selector is **element-typed on `a`** and cannot reach `<button class="chip">` (`js/app.js:137, 139, 3401`, …). `a.chip` is fixed; `button.chip` is not. |
| measured | ink `#ffffff` on `[239,233,221]` (≈`--bg`), **1.21–1.32**, floor 4.5 |

| cell | worst | rows | routes affected |
| --- | --- | --- | --- |
| light@1440 | **1.21** | 11 light rows total | `#/artist/leonardo-da-vinci`, `#/museum/louvre`, `#/list/<id>`, `#/taste` |
| light@390 | **1.21** | ″ | ″ |
| dark@1440 / dark@390 | 15.47 pass | 7 | white-on-panel is correct in dark |

Dark is fine — this is a light-theme-only defect, which is why it reads as the
same defect class unit 29 named. Source: `state-*.json`.

### V32-4 (major) · `.le-meta` — `--muted` directly on `#bg-canvas` on `#/list/<id>`

| | |
| --- | --- |
| selector | `.le-meta` (`css/styles.css:1359`, `color:var(--muted)`, `.82rem` = 13.1 px) |
| route | `#/list/<id>` — measured on `#/list/paintings-that-still-scare-us` |
| backdrop (measured) | `#bg-canvas`, `canvasDelta` up to **44**; `backdropNoCanvas` = `[242,236,223]` = `--bg` exactly, i.e. **no panel anywhere in the ancestry** |

| cell | worst measured | canvasΔ | unit 29's certified ALL ceiling for this ink |
| --- | --- | --- | --- |
| light@390 | **4.35 FAIL** | 44 | **3.57** |
| light@1440 | 5.38 | 30 | **3.57** |
| dark@390 | 5.50 | 20 | **2.24** |
| dark@1440 | 5.51 | 19 | **2.24** |

**This is a second residual member of F-7's class, and it is the F-8 seam
exactly.** Unit 28/29's route list contains `#/lists` but **not** `#/list/<id>`,
so the route was never walked; unit 30's instruments were cover- and
`.hero`-scoped. `.le-meta` therefore kept `--muted` on the page background after
26 siblings were re-pointed.

Severity note, and I want to be precise: only **one of four cells** measured below
floor on a single draw. But `#bg-canvas` is `Math.random`-seeded, and against unit
29's **derived ALL ceiling — which Van Eyck re-derived himself to ±0.01** — this
ink fails in **both themes by bound, not by sample** (3.57 light / 2.24 dark
against 4.5). My three passing cells are draws that missed the corner; they are
not clearances. I did not re-run at more draws (out of budget), so the *bound* is
inherited and the *membership* is mine and measured.

### V32-5 / V32-6 (major) · `.tl2-year` on its own gridline — **this is N-31-1**

Full verdict in §4.1. Two triples (one per theme), `#/timeline`, 11.2 px:

| cell | as shipped | with `.tl2-grid` hidden |
| --- | --- | --- |
| light@1440 | **3.78** | 5.13 |
| light@390 | **3.78** | 5.17 |
| dark@1440 | **3.63** (`.now`, `--gold2`) / 3.77 (`--faint`) | 4.90 / 11.53 |
| dark@390 | **3.63** | 4.90 |

### V32-7 (major) · `.sr-group` under `.main-nav` at 390 px — **this is N-31-2**

Full verdict in §4.2. `1.00` light / `1.04` dark @390; `4.62` both themes with
`.main-nav` suppressed; `4.62` at 1440 where the collision does not occur.

### V32-8 (NOT A FINDING — instrument false positive, disclosed) · `text.md-flag`

The census flagged `text.md-flag` on `#/nations` at **1.21 dark@1440 / 2.59
dark@390**, ink `#000000`, 13 px. **I do not report this as a defect.** These are
**colour flag emoji** (`js/app.js:1287`, `${n.flag}`). Their painted colour comes
from the colour-emoji font, not from `fill`; the `#000000` my instrument recorded
is the *computed default* `fill` and is painted nowhere on screen. The measured
ratio is therefore between a fictitious ink and a real backdrop and means nothing.

**I am not clearing it either.** My instrument structurally cannot score
colour-emoji glyphs, so this class is **unmeasured**, and it is in NOT TESTED. I
lean strongly to "not a text-contrast defect" — the glyph is a national flag
identifying a link that also carries an SVG `<title>` accessible name, and at the
europe zoom a `.md-name` text label — but that lean is reasoning, not measurement,
and it should not be recorded as a pass.

### V32-9 (NOT A FINDING — instrument artefact, disclosed) · 19 hover rows on a blue backdrop

Of 30 failing hover/focus rows, **19** have a saturated blue worst-pixel
(`[68,133,203]`, `[83,144,215]`) — `a` at 3.90–4.23 and `button.ec-surprise` at
2.98. That blue is **Chrome's default `:focus-visible` ring**: the site sets
`outline:2px solid var(--gold)` only on `.skip-link`, `.skip-inline` and
`#app h1/#app/#ig-end` (`css/styles.css:410, 424, 429`), so plain links and
buttons take the UA ring.

I classify these as artefacts of measuring within `getBoundingClientRect()`: the
ring is drawn at the element's edge and its antialiased pixels fall inside the box,
where a glyph's own antialiased tail can coincide. The discriminator is in the
data — for the same selector and same ink, **516 rows measured and only 18 fail,
every failing one on a blue pixel** while non-blue worst values sit far higher. A
focus ring beside text is not that text's background under 1.4.3.

Two honest riders: the observation that plain controls take the **UA** ring rather
than the site's gold one is real and adjacent to **F-2**; and ring-vs-adjacent
contrast (**WCAG 1.4.11**) is a separate criterion I did **not** measure.

---

## 4 — EXPLICIT VERDICTS ON DÜRER'S TWO UNFIXED FINDINGS

### 4.1 — N-31-1 (`.tl2-year` on the 1 px `.tl2-grid` rule): **CONFIRMED, and refined**

Independently reproduced with my own instrument, and my numbers land on his to the
second decimal.

| | Dürer (unit 31) | **me (unit 32)** |
| --- | --- | --- |
| as shipped, light | 3.78 | **3.78** (1440 and 390) |
| as shipped, dark | 3.63 | **3.63** (1440 and 390) |
| `.tl2-grid` suppressed, light | 5.13–5.17 | **5.13** @1440, **5.17** @390 |
| `.tl2-grid` suppressed, dark | 4.90 | **4.90** (both) |

**Confirmed:** the failure is caused by the layer behind the glyphs, not by the
ink. `.tl2-year` is `transform:translateX(-50%)`-centred on a 1 px
`.tl2-grid` rule, so the rule passes *through* the glyphs; hiding only that rule
recovers 4.90–5.17 in every cell. `canvasDelta` and `coverDelta` are **0** on
every row, so his classification — a **flat-paint** defect, not an AC19
`#bg-canvas` one — is right, and so is his remedy space (geometric: offset the
label off the rule, or give it a chip) rather than an ink swap.

**Refinement 1 — the binding element differs by theme, as he said, and I can name
it exactly.** In **dark** the binding row is `.tl2-year.now` in `--gold2`
`[232,201,138]` on the gold `now` rule `[119,99,57]` → 3.63. In **light** the
binding row is plain `--faint` `[112,103,85]` on the century rule `[225,211,183]`
→ 3.78, while `.tl2-year.now` in light measures **4.76 and passes**. So light and
dark fail through *different elements against different rules*, and a fix aimed at
only one of them would leave the other open.

**Refinement 2 — a coverage note on my own bulk walk, not on his finding.** My
route census caught `.tl2-year` at **1440 only**; at 390 the labels live inside
`.tl2-inner` in an `overflow-x:auto` wrapper and are horizontally scrolled out, so
`triple.py`'s viewport-containment filter dropped them. The selector probe, which
uses `scrollIntoView` on every scrollable ancestor, caught all four cells. Had I
run only the walk I would have under-reported this finding by half — recorded
because it is the same class of perimeter error A13 is about.

### 4.2 — N-31-2 (`.main-nav` over the open `.search-results` at 390 px): **CONFIRMED; his attribution is right**

| site | as shipped @390 | `.main-nav{visibility:hidden}` @390 | @1440 as shipped |
| --- | --- | --- | --- |
| `.sr-group` light | **1.00** | **4.62 pass** | 4.62 pass |
| `.sr-group` dark | **1.04** | **4.62 pass** | 4.62 pass |
| `.sr-more` light/dark | 4.62 pass | 4.62 pass | 4.62 pass |
| `.sr-meta` light/dark | 6.42 / 5.68 pass | unchanged | pass |

Identical to his published 1.00 / 1.04 → 4.62. **The ink is not the defect**:
`.sr-group`'s own backdrop is `--panel2` and it clears at 4.62 in both themes and
both viewports. The defect is `.main-nav` painting **over** the open panel at
390 px, both computing `z-index:auto` inside `.site-header`. A layout/stacking
defect, remedy is a UX call — exactly as he recorded it.

**Now the part my §1.3 promised, because it decides whether this is a finding at
all.** My occlusion guard treats an overlay as counting against an element only
when the overlay is **not that element's own ancestor**. That single rule
separates two things that look identical to a pixel differential:

- **Benign transit.** `.site-header` is sticky and 78 % opaque with a
  backdrop-blur, so body text scrolling under it composites through the bar. My
  first, guard-less run reported **1.07 on `#/daily`** and **1.09 on `#/timeline`**
  from exactly this. Those are *not* AC19 defects — the text is mid-scroll, not
  presented — and in the final census they appear only in the occluded-pixel
  table, attributed to `header.site-header` + `button.skip-link`, worst 1.07 over
  4 rows on 2 routes.
- **A real defect.** `.search-results` is a **descendant** of `.site-header`, so the
  header does not count against it and the panel is measured on its own backdrop —
  which is how it clears at 4.62. `.main-nav` is a **sibling subtree inside** that
  header, therefore *not* an ancestor of `.sr-group`, and it is precisely the layer
  whose suppression recovers the value. Nothing is scrolling; the panel is open at
  rest; the collision is in the presented state.

So the guard that *demoted* two 1.0x readings to non-findings **kept** this one,
on a structural criterion rather than a judgement call — and that is the
independent corroboration of Dürer's attribution. Had the guard been naive
("anything under a sticky header is benign"), N-31-2 would have been wrongly
dismissed; had there been no guard, two false majors would have been filed.

---

## 5 — DO UNITS 27 / 29 / 30 / 31 STILL HOLD AT HEAD (`a716397`)?

| unit | what it fixed | verdict | my measurement |
| --- | --- | --- | --- |
| **27** | museum-band scrim; `p.img-credit`/`span.count` off the canvas | **HOLDS** | `#/museums` + `#/museum/louvre`, all 4 cells: **784 rows, 0 below floor**, worst **4.90** (`span`, dark@390) |
| **29** | 26 selectors off `--faint`/`--muted` onto `--body-ink`; light `a:hover` → `--ink`; `--gold2` → `#544019` | **RULE HOLDS · CLASS NOT FULLY CLOSED** | `--faint` over `#bg-canvas`: **0 rows in 33 routes × 4 cells** — the retirement is complete and measured. Light `a:hover` measured as `#2b2620` = `--ink`, so that fix is live. **But `--muted` over `#bg-canvas` still has 53 rows on 2 sites, one of which fails → V32-4 (`.le-meta`).** |
| **30** | `.hero-content` veil on four `hero()` families; `.era-tile`; hero focus ring; prose-link underline | **HOLDS** | all four hero families walked (`#/artist/*`, `#/museum/*`, `#/era/*` ×8, `#/movement/*`, `#/technique/*`, `#/nation/*`): **0 hero-surface failures**; worst on any hero surface **3.58** against its 3.0 floor (`h1.home-title`, light@390, on a cover) |
| **31** | `.tl-year` → `--body-ink` | **HOLDS** | `.tl-year` over `#bg-canvas` (canvasΔ 5–39), all 4 cells: **7.14 / 7.19** light@390, **11.45–12.73** dark, **8.60** light@1440 census — against 4.06–4.47 before the fix. Its siblings re-confirmed independently: `.tn-count` 4.62, `.tm-lab` 4.90/5.17, `.tn-name` 12.40+, `.sr-more` 4.62, `#search::placeholder` **not measured** (see NOT TESTED) |

Unit 29 is the one qualified verdict, and the qualification is narrow: the *rule*
it wrote into the stylesheet is correct and its `--faint` half is now verified
exhaustively over the full route table. Its `--muted` half has one call site on a
route no enumeration had walked.

---

## 6 — PERIMETER

**What this enumeration is:** a route-and-state census of the (ink, size, backdrop)
triple in which every backdrop is a measured paint differential. **What it is not:**
complete. The gaps are named here and in §7 rather than argued away.

### 6.1 Routes walked — 33, all in 4/4 cells

All 26 `case` labels in `route()` (`js/app.js:2359-2384`), plus the other seven
`#/era/*` members:

`#/` · `#/artists` · `#/artist/leonardo-da-vinci` · `#/artwork/david` · `#/explore`
· `#/timeline` · `#/influences` · `#/daily` · `#/lists` ·
`#/list/paintings-that-still-scare-us` · `#/palette` · `#/taste` · `#/museums` ·
`#/museum/louvre` · `#/movements` · `#/movement/impressionism` · `#/techniques` ·
`#/technique/oil-painting` · `#/eras` · `#/era/{14th…21st}-century` (**all 8**) ·
`#/nations` · `#/nation/italy` · `#/privacy` · `#/credits` · `#/passport/import` ·
`#/no-such-page`

Each in **light and dark × 1440×900 and 390×844** — 4/4 cells, no cell inferred
from another. Per-route × per-cell row counts: `report-p1-tables.txt`.

**One `id` per parameterised route.** Only one artist, one artwork, one museum, one
movement, one technique, one nation and one list were rendered. Other ids are
**NOT TESTED** — for the veiled hero surfaces unit 30 established a bound rather
than a sample, but for anything outside that bound a second id is unmeasured.

### 6.2 States exercised

| state | how | cells |
| --- | --- | --- |
| at rest, ≤8 scroll bands per route | `triple.py` | 4/4 |
| **search open** (`van` typed, input event dispatched) | `sitecensus.py` | 4/4 (1 draw) |
| **search panel scrolled to its overflow** (`.sr-more` is clipped away at rest) | `sitecensus.py` | 4/4 (1 draw) |
| **taxonomy tree view** (behind a toggle; the default is cards, so no sweep ever rendered it) | `sitecensus.py` | 4/4 (1 draw) |
| **populated passport** — 6 admirations seeded, `#/taste` `#/palette` `#/daily` `#/lists` | `triple.py V32_PASSPORT=1` | 4/4 |
| **influence graph focused** (real click on a node) | `sitecensus.py` | 4/4 (1 draw) |
| **hover + focus + focus-visible** on ≤26 controls × 26 routes, engine-forced | `states.py` | 4/4 |
| single layers suppressed for attribution (`.tl2-grid`, `.main-nav`, `.ig-edge`, `.ig-node circle`) | `sitecensus.py` | as tabulated |

**Populated `#/taste` and `#/palette` — Van Eyck's named unverifiable — are now
measured:** 1 202 rows, **0 below floor**, and **14 selector/route pairs were
reached that the no-passport state never renders**, including `text.tm-lab`. That
gap is closed.

### 6.3 Element classes — what each instrument can and cannot see

Carried forward from §1.5, with the outcome of each:

| class | instrument | status |
| --- | --- | --- |
| HTML element owning a text node (ink = `color`) | `triple.py` | **covered**, 33 routes × 4 cells |
| `-webkit-background-clip:text` gradient ink | `triple.py` (gradient stops enumerated) | **covered** |
| SVG `<text>`/`<tspan>` (ink = `fill`) | `triple.py` injected `fill:transparent` rule + `sitecensus.py` | **covered — and it is where V32-1/V32-2 came from.** This is the class **A16** recorded as unverifiable |
| `::before` / `::after` textual ink | `sitecensus.py` **only** — `triple.py` is structurally blind (no text node, no rect of its own) | **partially covered**: `.trait::before` 4.73–6.59 pass, `.facts li::before` 6.58–11.79 pass (over canvas). **`.branch-chip::before` and `.tone.on::after` never rendered** → NOT TESTED. **And the perimeter scan that was to enumerate this class from the DOM crashed, so the site list is from my reading of the CSS** — bounded by reading, which is the method A13 rejected |
| `::placeholder` | `sitecensus.py` | **NOT MEASURED** — my `LOCATE` gates pseudo-elements on a non-empty `content`, and `::placeholder` has `content:normal`, so `#search::placeholder` returned "NOT PRESENT" in all 4 cells. Instrument bug, mine, disclosed |
| colour-emoji glyphs | none | **structurally unmeasurable** (painted colour ≠ computed `fill`) — V32-8 |
| focus **ring** (WCAG 1.4.11) | none | **structurally unmeasurable by a glyph differential** — a ring is not a glyph. NOT TESTED beyond unit 30's `.hero` |
| overlapping text rects | `triple.py` conflates them | **known limitation**: the bulk walk hides all ink at once, so a glyph inside element X's rect belonging to element Y is attributed to X. Material only where text rects densely overlap — i.e. `#/influences`. For V32-1 it does not change the verdict, because every conflated neighbour is another `.ig-node text` with the **same ink and same size**, so the triple is right whichever label owns the pixel. The selector-isolated probe and the suppression runs are the binding evidence there |

### 6.4 The honest summary of this perimeter

Complete: the **route** axis for the at-rest HTML and SVG text classes, in all four
cells, by measurement. Bounded: pseudo-element ink (list from reading, two members
unrendered), one `id` per parameterised route, one draw per canvas-exposed triple.
Not covered at all: `::placeholder`, emoji, focus rings, non-Chrome engines, real
AT, 200 % zoom, `deviceScaleFactor ≠ 1`.

**I am not claiming a complete enumeration.** I am claiming that the route axis
that produced F-8 is now closed by measurement, that a second unwalked-route
residual (V32-4) and an unreadable-ink class (V32-1/V32-2) were found inside it,
and that three named gaps remain open where a previous pass would have argued them
shut.

---

## 7 — NOT TESTED

Nothing in this list is a pass.

**Instrument-blind classes**
1. `#search::placeholder` — my `LOCATE` bug (§6.3); "NOT PRESENT" in all 4 cells. Unit 31 measured it at 4.90–5.17; **not re-verified by me.**
2. Colour-emoji glyphs (`text.md-flag`, `a.chip.n` flags) — painted colour is not the computed `fill` (V32-8).
3. Focus **ring** contrast, WCAG 1.4.11, everywhere except unit 30's `.hero`.
4. The pseudo-element **perimeter itself** — the DOM scan crashed; the list is from reading the stylesheet.

**Never rendered, so never measured**
5. `.branch-chip::before` — absent on `#/movement/impressionism` in all 4 cells.
6. `.tone.on::after` — needs a selected tone on `#/palette`; my prep did not select one.
7. `.map-dot .md-name` — only emitted at the **europe** map zoom; I never zoomed. Its ink is `fill:var(--muted)` (`css:1280`) — **same class as V32-1 and in no prior enumeration**. Unmeasured, and I flag it as the most likely place a fifth SVG finding is hiding.
8. `.search-results .sr-name`, `.pp-card-prev *`, `.taste-wrap *`, `.palette-wrap *` — my selectors matched nothing (wrong class names on my part, not absent surfaces). The populated-passport census (§6.2) covers those routes' text by a different route, at 0 failures.
9. `.gonext-item:hover b{color:#fff}` (`css:662`) — **source-identified sibling of V32-3 that I did not measure.** `.gonext-item` is an `<a>` (`js/app.js:1923`), so unit 29's light `a:hover` override colours the anchor, but this rule re-inks the `<b>` descendant to white. My hover pass capped at 26 controls per route and did not reach it. **Explicitly not cleared.**
10. `.pp-card-loading` — transient, replaced on the next animation frame. Unit 31 measured it by re-instating the markup; I did not.

**Coverage gaps**
11. **553 fully-occluded rows** — every glyph pixel under an overlay at their sampled band. No unoccluded value exists for them at that scroll position; they are not cleared.
12. Second and later `id`s for every parameterised route (§6.1).
13. Multi-draw confirmation of canvas-exposed triples. The census ran **1 draw**; the intended many-draw pass was not run. For V32-4 the *bound* is inherited from unit 29 (Van Eyck-verified) and only *membership* is mine. **Any canvas-exposed triple in my table that passes, passes on one draw** — and F-8 was partly missed because one cell of eight passed by chance.
14. The 2b selector census ran **1 draw**, not 3 (§2.1).
15. `#/passport/import` was rendered with the literal payload `import`, i.e. its invalid-payload state; the real import-conflict states were not exercised.
16. Browsers other than Chrome; real assistive technology; `deviceScaleFactor ≠ 1`; 200 % text zoom over any of these surfaces; the deployed GitHub Pages origin (**F-6**); 768×1024 and the 320 px width.
17. Whether V32-1/V32-2/V32-3/V32-4 have remedies that hold — I measured, I did not design or apply anything. **No production file was touched by this unit.**

---

## 8 — SUMMARY

- **33 routes × 2 themes × 2 viewports = 132 route-cells**, all measured; 15 341
  scored rows; **328 distinct (ink, size, backdrop) triples; 6 below floor** in the
  route census, **9 findings** in total once the selector and state passes are
  added, of which **2 are disclosed non-findings** (V32-8, V32-9).
- **4 new open findings**: V32-1 and V32-2 (SVG `fill:` inks crossed by graph
  layers — the **A16** class), V32-3 (`button.chip:hover` white on paper in light —
  unit 29's fix was element-typed on `a`), V32-4 (`.le-meta` `--muted` on
  `#bg-canvas` on an unwalked route — **the F-8 seam again**).
- **N-31-1 CONFIRMED** (3.78 / 3.63 → 5.13–5.17 / 4.90), refined: the binding
  element differs by theme. **N-31-2 CONFIRMED** (1.00 / 1.04 → 4.62), and the
  occlusion guard corroborates his attribution structurally.
- **Units 27, 30, 31 hold. Unit 29's rule holds; its `--muted` class has one
  residual call site.**
- The recurring shape of every one of these is the same, and it is A13's: **the
  instruments were sound and the perimeter was not.** F-8 was an unwalked route.
  V32-4 is another unwalked route. V32-1 is a walked route with an ink the reader
  could not read. V32-3 is a fixed defect whose fix was scoped by element type.
  None of them needed a new measurement technique — they needed the perimeter to be
  stated and then tested instead of argued.
