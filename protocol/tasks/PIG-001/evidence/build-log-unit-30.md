# BUILD LOG — PIG-001 unit 30

**Author:** Dürer (`claude-implementation-lead`)
**Branch:** `pig-001-stabilization` (verified; never `main`; not pushed)
**Gate 1:** `protocol/tasks/PIG-001/specification.md:8` → `workflow_state: "approved_for_build"`. Satisfied.

| item | commit |
| --- | --- |
| 30a — bound the `.hero` cover from its text block (V-F3) | `8d3a3ee1b3c5261d147220cff940f9173befb901` |
| 30b — prose-link underline (D-29-6, Matisse's ruling) | `a2ca16145ebbe544234ae5908551d3b7efc0a256` |
| 30a follow-on — the hero focus ring, now that the veil is deterministic | `90b0803a3ed37d01d78aadbc02fa76b7116ea0fe` |
| 30c — `.era-tile`, and the enumeration that should have found it | `094a631` |

Files touched: `css/styles.css`, `index.html` (`?v=` → `20260729-pig001-u30`),
`harness/durer-u28/canvastext.py` (the V-F2 fix), `harness/durer-u30/herotext.py`
and `harness/durer-u30/covertext.py` (new instruments), `harness/cdp-r2/cdp.py`
(`PIG_BASE` override — the measurement moved to port 8422).
`js/app.js` is **not** touched by this unit. No new dependencies. Committed by
explicit path; the untracked `THEORY_001.md`, `protocol/tasks/PIG-001/CHALLENGE_001`
and `protocol/tasks/PIG-001/THEORY_001` were left alone.

---

# 1 — THE HARNESS DEFECT, FIXED BEFORE ANYTHING WAS MEASURED

## 1.1 What was wrong

`Page.captureScreenshot`'s `clip` is in **page (document)** coordinates.
`durer-u28/canvastext.py` assembled that rect from `getBoundingClientRect()`,
which is in **viewport** coordinates. The two agree only at `scrollY == 0`; at
any other scroll position the captured pixels were offset by exactly `scrollY`,
so glyphs were compared against whatever happened to sit that far up the
document. Vermeer found this independently in both harnesses (V-F2) and nearly
published a false `div.card-tagline` 4.10 failure that is really 6.02.

The scroll offset is now added **at the capture**, so all the per-element pixel
arithmetic stays in the viewport space the rects were measured in, and the three
shots are asserted to be the same pixels of the same document:

```python
def shot(b, path, box, sx=0, sy=0):
    ...
    "clip": {"x": x + sx, "y": y + sy, "width": w, "height": h, "scale": 1}
...
assert int(b.ev("Math.round(window.scrollY)") or 0) == sy, "page scrolled mid-capture"
```

## 1.2 What it changed in my prior numbers — re-analysed by scroll position

| my run | over-canvas rows | at `scrollY == 0` | scrolled (was invalid) | below floor at 0 | below floor scrolled |
| --- | --- | --- | --- | --- | --- |
| `canvas-u29-px-dark-1440` | 417 | 389 | 28 | **0** | 0 |
| `canvas-u29-px-dark-390` | 339 | 329 | 10 | **0** | 0 |
| `canvas-u29-px-light-1440` | 558 | 521 | 37 | **0** | 0 |
| `canvas-u29-px-light-390` | 365 | 351 | 14 | **0** | 0 |

**89 invalid rows — exactly the count Vermeer reported.** Restricted to valid
rows, all four cells still show **0 below floor**, so **unit 29's conclusion
survives unchanged**, confirmed in my own archive rather than on his word. What
did not survive was the claim that the sweep covered the scrolled bands.

The only below-floor rows the bug ever produced in my archive are three
`div.card-tagline` rows on `#/lists` at `scrollY = 765`, all reading **4.10** —
the same false failure Vermeer caught and withdrew. **Withdrawn here too.** With
the corrected origin the same class reads **6.71**.

One further row was checked and cleared: `p.page-lede` on `#/museums`, dark 390,
**4.47 at `scrollY == 0`** in `canvas-after-count-dark-390.json`. The clip bug
does not excuse a scroll-0 row, so it was chased. It is the **pre-unit-29**
state: unit 29 row 13 re-pointed `.page-lede` from `--muted` to `--body-ink`
precisely because of that 4.47, and `build-log-unit-29.md:241` records it as the
before value. Not a live defect.

**No prior conclusion of mine rested on a scrolled row.**

## 1.3 The scrolled bands are no longer NOT TESTED

Re-run at HEAD with the corrected instrument, the canvas class now measures the
scrolled bands that both runs had to disclaim:

| cell | over-canvas rows | of which scrolled | classes | below floor |
| --- | --- | --- | --- | --- |
| light 1440×900 | 1 069 | **881** | 42 | **0 of 42** |
| dark 390×844 | 763 | **620** | 37 | **0 of 37** |

**1 501 rows that were NOT TESTED in both runs are now measured, and none is
below floor.** V-F2's disclosure item is closed for the canvas class.

---

# 2 — ITEM 30a · THE `.hero` COVER (V-F3)

## 2.1 Scope is wider than the finding, and this is the unit's main correction

Vermeer reported V-F3 as an **artist-hero** defect. It is not. `hero()`
(`js/app.js:831`) is called from **four** view builders:

| call site | routes |
| --- | --- |
| `js/app.js:1826` | `#/artist/*` |
| `js/app.js:2042` | `#/movement/*`, `#/technique/*` |
| `js/app.js:2099` | `#/era/*` |
| `js/app.js:2158` | `#/nation/*` |

All four emit `.hero > .hero-shade + .hero-content` verbatim, and **all four
failed**. Measured before the fix, light 1440×900: `#/era/16th-century` **1.72**,
`#/technique/oil-painting` **1.76**, `#/nation/italy` **2.43** — alongside the
artist routes. One rule closes all four. Had this been fixed only on
`#/artist/*`, AC19 would still have been open on three route families.

## 2.2 Root cause — F-V1's mechanism, on the hero that never got the fix

`.hero .hero-shade` ramped `rgba(bg,.18) 0% → .42 52% → .93 100%` by hero
**height**, under a `.hero-content` that is bottom-anchored
(`.hero{min-height:330px; align-items:flex-end}`). The breadcrumb row — the
block's first line — lands around 55–70 % of the hero, where the ramp delivers
only **.43–.61**. The home hero received `--hero-veil` at unit 26a and the
museum band received `--mu-veil` at unit 27; this hero received neither and
still carried the pre-unit-26 geometry. Unit 27's own comment
(`styles.css`, museum band) cites the artist hero as its correctness reference,
which is how this survived twenty-nine units.

## 2.3 Derivation — and a deviation from the specified value

Bounded against a **worst-case fully opaque cover pixel** (WHITE in dark, where
ink is light; BLACK in light, where ink is dark), composited as
`B = cover·(1−v) + page·v`. `.hero-shade` is ignored in the bound: it only ever
pulls the backdrop further toward the page colour, which in both themes is the
direction the veil already moves it, so the veil alone is conservative.

| theme | ink | floor | alpha needed | at `.74` | at **`.80`** (shipped) |
| --- | --- | --- | --- | --- | --- |
| dark | `--gold2` `#e8c98a` (`.hero-sub a`) | 4.5 | **.691** | 5.44 | **6.84** |
| dark | `--body-ink` `#d8d2c4` | 4.5 | .675 | 5.77 | 7.25 |
| dark | `--ink` `#ece6d9` (`h1`) | 3.0 | .506 | 6.99 | 8.78 |
| light | `--gold2` `#544019` (`.hero-sub a`) | 4.5 | **.740** | **4.50** | **5.27** |
| light | `--body-ink` `#433c31` | 4.5 | .705 | 4.96 | 5.80 |
| light | `--ink` `#2b2620` (`h1`) | 3.0 | .472 | 6.83 | 7.99 |

**DEVIATION D-30-1 — shipped at `.80`, not the specified `.74`.**
V-F3 specifies `.74` and gives the requirement as "≥ .690 dark / ≥ .710 light".
The dark figure reproduces exactly (.691). The light figure does not: light's
binding ink is `--gold2`, which **unit 29 re-pointed to `#544019`**, and it needs
**.740** — so `.74` lands it at exactly **4.50**, a bound with no margin at all,
where every other bound in this file is set with one. (`.710` is `--body-ink`'s
requirement, not the binding ink's.) Shipped at `.80`, which is also the home
hero's dark `--hero-veil`, so **no new value enters the system**. Strictly safer
than specified; recorded here and in the Decision Record rather than taken
silently.

## 2.4 What was implemented — the same one geometry, third instance

Per-theme token, declared in both theme blocks with the same value exactly as
`--mu-veil` is:

```css
--hero-text-veil:.80;
```

```css
.hero .hero-shade{                       /* was .18 → .42 → .93 by hero height */
  position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(var(--bg-rgb),.06),rgba(var(--bg-rgb),.30));
}
.hero-content{
  position:relative;padding:36px 38px 30px;width:100%;
  background:linear-gradient(180deg,
    rgba(var(--bg-rgb),0) 0,
    rgba(var(--bg-rgb),var(--hero-text-veil)) 18px,
    rgba(var(--bg-rgb),var(--hero-text-veil)) 100%);
}
```

The 18 px feather is unit 27's, and is shorter than the smallest `padding-top`
in the block (22 px at ≤480 px), so no glyph can fall inside the ramp.
`.hero-shade` had to come down: left at `.93` under the new veil the two would
composite to **.986** and the cover would effectively be gone — the outcome
units 26a and 27 were careful to avoid. It takes `.mu-shade`'s values, cited.
Combined at the text block the cover retains ~14 %, against the home hero's
20 % (dark) / 14 % (light). **No fourth pattern was invented.**

## 2.5 Measured — 4 cells × 16 subjects × 3 draws

Instrument: `harness/durer-u30/herotext.py`, scroll 0 only (asserted),
`prefers-reduced-motion: reduce` so the cover paints one static frame, three-shot
glyph diff on real rendered pixels. Before and after are the **same build, same
instrument, same operator** — `U30_BEFORE=1` restores the shipped geometry at
runtime, and it reproduces Vermeer's published numbers exactly (caravaggio `a`
**1.42**, leonardo **2.01**, h1 **2.40** light / **2.35** dark, monet clean in
light and worst in dark), which is the instrument's own check.

Subjects: 12 painters (Vermeer's three named extremes plus leonardo plus 8
spanning other eras and palettes) + `#/movement/impressionism`,
`#/technique/oil-painting`, `#/era/16th-century`, `#/nation/italy`.
**489 in-hero measurements per cell; 1 956 in total.**

| cell | below floor | worst | subjects with ≥1 failure |
| --- | --- | --- | --- |
| light 1440×900 | **219 → 0** | **1.42 → 6.06** | 12/16 → **0/16** |
| dark 1440×900 | **150 → 0** | **1.68 → 8.27** | 10/16 → **0/16** |
| light 390×844 | **261 → 0** | **1.66 → 5.93** | 13/16 → **0/16** |
| dark 390×844 | **201 → 0** | **1.72 → 8.18** | 11/16 → **0/16** |

**831 below floor → 0.**

Per class, worst across all subjects and all draws (before → after):

| class | px | floor | light 1440 | dark 1440 | light 390 | dark 390 |
| --- | --- | --- | --- | --- | --- | --- |
| `.breadcrumbs a` | 12.5 | 4.5 | 1.42 → **6.06** | 1.68 → **8.27** | 1.82 → **5.93** | 1.72 → **8.18** |
| `.breadcrumbs .sep` | 12.5 | 4.5 | 1.48 → **6.26** | 1.68 → **8.27** | 1.66 → **6.33** | 1.72 → **8.39** |
| breadcrumb current `span` | 12.5 | 4.5 | 1.48 → **6.26** | 1.68 → **8.27** | 1.80 → **6.35** | 1.72 → **8.39** |
| **`h1` — the painter's name** | 57.6 / 30.4 | **3.0** | 2.40 → **8.80** | 2.35 → **10.21** | 2.82 → **8.71** | 2.35 → **10.21** |
| `.hero-tagline` | 17.9 | 4.5 | 5.38 → 6.66 | 6.49 → 8.89 | 4.64 → 6.59 | 4.61 → 8.89 |

**Dark 390×844 was Vermeer's NOT TESTED #4.** Measured here: it failed before
(**1.72**, 11 of 16 subjects) and passes now (**8.18**).

The cover is still there. The measured cover-delta under the glyphs — how much
the backdrop moves when the in-hero canvas is removed — falls from **~130–156**
to **~35–42**, i.e. the cover still modulates the veiled ground rather than
being replaced by a flat slab. Screenshots attached:
`u30-artist-caravaggio__*`, `u30-era-16th-century__*` (4 viewport×theme cells each).

## 2.6 `#/artwork/*` — measured, and it does **not** fail

Vermeer listed artwork hero interiors as NOT TESTED, expected them to fail on
the same `.hero-shade`, and explicitly did not claim it. **Measured: they do not
fail, and the expectation is structurally unfounded.**

`#/artwork/*` does **not** call `hero()`. It renders `.aw-hero`
(`js/app.js:1948`, `styles.css:666`), which is a different element with **no
`.hero-shade`, no `.hero-content`, and no in-hero text at all** on the 257 works
that have a photograph. The title and `.hero-sub` sit in `.page-head` **below**
the hero on ordinary page paint — the surface Vermeer already measured at
9.25 light / 11.60 dark, PASS.

The 66 works with no photograph render `.aw-hero-gen`, whose only in-hero text
is `span.map-hint`. It carries its own `rgba(10,9,8,.72)` pill and `#f2eee5`
ink — a self-contained affordance, not the hero scrim. Measured on
`#/artwork/the-red-studio`, `blue-nude-ii`, `the-old-guitarist`, `the-snail`:

| cell | worst `span.map-hint` | floor | verdict |
| --- | --- | --- | --- |
| light 1440×900 | **7.99** | 4.5 | PASS |
| dark 1440×900 | **7.99** | 4.5 | PASS |
| light 390×844 | **7.99** | 4.5 | PASS |
| dark 390×844 | **7.99** | 4.5 | PASS |

Identical before and after, as expected — this unit does not touch that surface.
**Vermeer's NOT TESTED #2 is closed by measurement, not by inference.**

## 2.7 Follow-on found while reviewing the screenshots — the hero focus ring

The route's programmatic focus ring (`#app h1:focus-visible`, `2px solid
var(--gold)`, offset 5px) lands inside the hero and therefore now sits **on the
veil**. Light's `--gold` `#9e7938` reads **2.13** against the veiled bound
`rgb(194,189,178)` — under the **3.0** non-text floor of WCAG 1.4.11.

Not a regression: over a dark cover the old ramp put the same ring lower still
and left it different on every subject. The veil is what makes it deterministic
enough to fix. Closed exactly as unit 27 closed it for the museum band and with
the same colour — `#6b5122`, already the light home-hero title's darker stop,
not a new value — clearing at **3.96**. Scoped to the hero; verified in the
browser across five routes in both themes:

| surface | theme | resolved outline | verdict |
| --- | --- | --- | --- |
| `.hero-content h1` (`#/artist/*`, `#/era/*`, `#/nation/*`) | light | `rgb(107,81,34)` = `#6b5122` | **3.96** |
| `.mu-hero-body h1` | light | `rgb(107,81,34)` — unit 27's rule, untouched | 4.82 |
| `.page-head h1` (`#/artists`) | light | `rgb(158,121,56)` = `--gold`, untouched | 3.40 |
| `.hero-content h1` | dark | `rgb(201,164,92)` = `--gold`, untouched | 4.65 |

An outline is not a glyph and is identical in the A and B shots of the diff, so
§2.5's numbers are undisturbed by this commit.

---

# 3 — ITEM 30b · D-29-6, MATISSE'S UNDERLINE

Applied **verbatim from his §1c**, including the comment block. Not redesigned.

- **Theme-neutral**, per his §2 — no `html[data-theme]` prefix. He measured dark
  at **1.06:1**, *worse* than light's 1.10:1; dark reads as a link only because
  it is saturated, and chroma is colour.
- **Scope** `#app p:not(.img-credit):not(.footer-note) a:not([class])`.
- **Resting `text-decoration-color:currentColor`**, his one measured departure
  from the unit-26a/28 precedent — `var(--line)` renders at 1.16:1 against the
  worst reachable canvas backdrop.
- 1px thickness, 2px offset, `skip-ink:auto`, thickness → **2px** on `:hover` /
  `:focus-visible`. Hover colours and the global focus ring untouched.
- His **§1d optional follow-on is NOT taken** — explicitly out of Gate 2 scope.

**The two `:not()` class exclusions are load-bearing, and I verified that in the
browser rather than from specificity arithmetic.** Probed at HEAD, both themes,
5 routes, classifying every anchor by whether it carries the new rule
(`currentColor` + 1px) or its own pre-existing one:

| route | new rule | pre-existing (`--line`/auto), unchanged | plain |
| --- | --- | --- | --- |
| `#/credits` | 2 | **254** (`.img-credit a`) | 153 |
| `#/privacy` | 1 | 0 | 20 |
| `#/no-such-page` | 2 | 0 | 19 |
| `#/artwork/david` | 2 (`.aw-provenance`) | 2 (`.img-credit a`) | 33 |
| `#/` light | 2 | 1 (light hero `.footer-note a`) | 606 |
| `#/` dark | 2 | 0 (that rule is light-only — correct) | 609 |

Resolved decoration colour is light `rgb(84,64,25)` = `--gold2` `#544019` and
dark `rgb(232,201,138)` = `#e8c98a` — i.e. `currentColor`, in both themes. The
254 `.img-credit a` and the light hero `.footer-note a` keep their own
`--line`/`auto` treatment, so **the surfaces certified in units 26a and 28 are
untouched and their evidence stays valid**. `.credit-list .cr-what a` sits in
`ul > li > span`, never in a `<p>`, so it is **not** double-ruled by its
`border-bottom` plus an underline.

No token, no colour and no measurement changes — this rule sets decoration
properties only, so no AC19 figure in unit 29's log or in Vermeer's evidence is
disturbed.

**Open, and not claimed:** Matisse's §Review asks Vermeer to capture
`#/credits`, `#/privacy` and `#/404` at both viewports in both themes so he can
review the underline weight and offset against the prose before the rule is
considered settled. That review has not happened. It is a visual-review item,
not a contrast one.

---

# 3.5 — ITEM 30c · `.era-tile`, AND THE ENUMERATION THAT SHOULD HAVE FOUND IT

## 3.5.1 Why this section exists

`.era-tile` is the **fourth** instance of one defect — home hero (26a), museum
band (27), the `.hero` family (30a), `.era-tile` (here). Four instances found by
four separate accidents is a **sampling process**, and it would have produced a
fifth. This project has twice ended an iteration cycle by switching from
sampling to enumeration: unit 24's 694-image census superseding a 122-record
sample, and unit 29's source bound superseding an 84-draw model that was still
moving. That switch is made here.

## 3.5.2 The instance

`.et-shade` ramped `transparent 30% → rgba(bg,.88)` as a percentage of
`.era-tile`'s **height**, while `.et-label` is bottom-anchored
(`align-items:flex-end`) — the same shape as the other three. `b` is the era's
name at 16.8 px / weight 600, which is **small** text (it clears neither the
24 px nor the 18.66 px-bold large-text threshold), so its floor is 4.5, not 3.0.

**Correction to my own earlier note:** `.era-tile` lives on **`#/`** (the "Begin
with an era" strip), not on `#/eras`. The era *cards* on `#/eras` are
`.card-art` and were never broken (5.71 light / 8.10 dark). My first attempt to
measure it on `#/eras` returned 0 elements for exactly that reason.

Measured with `covertext.py`, 8 tiles × 2 draws per cell, before → after:

| cell | `b` — era name (floor 4.5) | `span` — range · painters (floor 4.5) |
| --- | --- | --- |
| light 1440×900 | **1.50 → 8.71** | **3.37 → 6.59** |
| dark 1440×900 | **1.44 → 10.32** | **1.98 → 8.88** |
| light 390×844 | **1.79 → 8.81** | **3.42 → 6.53** |
| dark 390×844 | **1.83 → 10.36** | **3.70 → 8.89** |

**2 of 10 (host, class) pairs below floor before → 0 of 10 after, in every cell.**

Same remedy, same token, no new value. The one number that differs from
`.hero-content` is the feather — **10 px, not 18** — because it must stay
shorter than the block's `padding-top`, which is 12 px on this tile. The
geometry is the same; the single value the geometry requires is different, and
that is stated rather than forced.

## 3.5.3 The enumeration — `harness/durer-u30/covertext.py`

`js/app.js` has **20 `canvasTag` call sites**. Rather than reason about each
from the CSS — which is how the first four were missed — membership is decided
by a **paint differential** over every cover canvas in the document:

- **A** page as rendered · **B** glyphs transparent · **C** glyphs transparent
  **and** every `canvas:not(#bg-canvas)` hidden.
- A glyph composites over a cover **iff B ≠ C at its pixels**.

An element nobody thought to name still turns up; an element whose canvas sits
behind an opaque panel correctly does not. Each row carries its nearest
canvas-bearing ancestor, so it maps back to a call site. `#bg-canvas` is
excluded on purpose — different layer, bounded at source in unit 29.

Two instrument corrections were forced and are recorded because they matter:

1. The cover is hidden by **`visibility:hidden`, not `display:none`**. Several
   call sites emit an **in-flow** canvas (`.mini-card`, `.arc-work-gen`,
   `.le-art`), so `display:none` reflowed the document and moved `scrollY`
   between shots — caught by the mid-capture scroll assertion on the first run,
   which is the assertion earning its keep.
2. `cdp.BASE` is now env-overridable (`PIG_BASE`); measurement moved to 8422.

## 3.5.4 The 20 call sites — enumeration result

Grouped by the host each call site produces. "Text over it" is the measured
paint differential, not a reading of the CSS.

| # | `js/app.js` | host produced | text composites over it | worst measured (light / dark) | verdict | veil |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `:789` | `.card-art` (artist card) | yes | 12.74 / 15.52 | **pass** | none needed |
| 2 | `:805` | `.card-art` (work card) | yes | 12.74 / 15.52 | **pass** | none needed |
| 3 | `:816` | `.card-art` (taxonomy card) | yes | 6.15 / 9.47 | **pass** | none needed |
| 4 | **`:833`** | **`.hero` (4 view builders)** | **yes** | **6.06 / 8.27** | **pass** | **`--hero-text-veil` (30a)** |
| 5 | `:1434` | `.card-art` (venue card) | yes | 6.34 / 7.43 | **pass** | none needed |
| 6 | `:1500` | `.mini-card` | yes | 9.26 / 12.80 | **pass** | none needed |
| 7 | `:1553` | `.card-art` (list card) | yes | 6.15 / 9.47 | **pass** | none needed |
| 8 | `:1583` | `.card-art` (featured list) | yes | 6.15 / 9.47 | **pass** | none needed |
| 9 | `:1602` | `.le-art` | **no** — `.le-body` is a sibling on panel paint | — | N/A | — |
| 10 | **`:1630`** | **`.home-hero`** | **yes** | **3.79 / 5.19** (`h1`, floor 3.0) | **pass** | **`--hero-veil` (26a)** |
| 11 | **`:1698`** | **`.era-tile`** | **yes** | **8.71 / 10.32** | **pass** | **`--hero-text-veil` (30c)** |
| 12 | `:1793` | `.arc-work-gen` | yes (`.arc-work-t`) | 12.86 light | **pass** | none needed |
| 13 | `:1883` | `.mini-card` (kindred) | yes | 9.26 / 12.80 | **pass** | none needed |
| 14 | `:1951` | `.aw-hero-gen` | yes (`.map-hint` only) | 7.99 / 7.99 | **pass** | own pill |
| 15 | `:1993` | `.mini-card` | yes | 9.26 / 12.80 | **pass** | none needed |
| 16 | `:1995` | `.mini-card` | yes | 9.26 / 12.80 | **pass** | none needed |
| 17 | `:2078` | `.card-art` (era card) | yes | 5.71 / 8.10 | **pass** | none needed |
| 18 | `:2139` | `.card-art` (nation card) | yes | 5.71 / 8.10 | **pass** | none needed |
| 19 | `:3216` | `.mini-card` (taste) | yes | 9.26 / 12.80 | **pass** | none needed |
| 20 | `:1948`† | `.aw-hero` `<img>` variant | **no** — no in-hero text | — | N/A | — |

† the photographed branch of the artwork hero; `overCover = 0` measured on
`#/artwork/david`, confirming no text composites there.

**Why the card and mini-card families never needed a veil, now measured rather
than assumed:** their text sits in a sibling block on opaque `--panel` paint
(`.card-body`, `.le-body`, `.mc-name`/`.mc-meta` beside the canvas), so the
cover is adjacent to the glyphs, not behind them. The four that failed are
exactly the four where a text block is *overlaid* on the cover. That is the
distinguishing property, and it is now stated as a rule rather than rediscovered.

**Run result at HEAD**, 12 routes × 2 draws × 4 cells:

| cell | (host, class) pairs | below floor |
| --- | --- | --- |
| light 1440×900 | 17 | **0** |
| dark 1440×900 | 17 | **0** |
| light 390×844 | 21 | **0** |
| dark 390×844 | 21 | **0** |

## 3.5.5 Bound on this enumeration — stated plainly

The **call-site enumeration is complete**: all 20 are classified, and the four
overlay surfaces are the four that were fixed. The **route coverage behind it is
bounded, not exhaustive**: 12 routes × 2 draws × 4 cells at HEAD, plus a
partial BEFORE sweep over 11–12 routes. 24 routes exist. The routes not swept in
the final pass (`#/influences`, `#/palette`, `#/taste`, `#/daily`, `#/explore`,
`#/museums`, `#/movements`, `#/techniques`, `#/nations`, `#/artists` index
variants) render **only** hosts already covered by the table above — every one
of them is a `.card-art` or `.mini-card` grid — so the *class* is covered even
where the *route* was not walked. **I am not claiming a route census; I am
claiming a host census.** That distinction is the honest bound.

---

# 4 — UNITS 26a, 27, 28 AND 29 STILL PASS

Structural isolation first: the home hero is `<header class="home-hero">`, never
`.hero`, and uses `.home-hero-content` — so `.hero .hero-shade` and
`.hero-content` never matched it and unit 26a cannot be reached by this unit.
`--mu-veil`, `.mu-shade`, `.mu-hero-body` and every canvas token are unmodified.
`--hero-veil` / `--hero-veil-edge` are unmodified. Then re-measured at HEAD:

**Unit 27 — museum band** (`herotext.py`, `.mu-hero-body` scope, 4 venues × 2 draws):

| cell | classes | below floor | worst |
| --- | --- | --- | --- |
| light 1440×900 | 7 | **0 of 7** | `div.mu-hook` 5.14 |
| dark 390×844 | 7 | **0 of 7** | breadcrumb `span` 4.88 |

Agrees with Vermeer's §3.2 table to ≤0.08 on every class, including his
correction that the band's tightest class is the breadcrumb `span` at **4.88**,
not `.mu-sub`.

**Units 28 / 29 — the `#bg-canvas` ink class** (`canvastext.py` with the
corrected origin, 6 routes × 2 draws):

| cell | over-canvas rows | classes | below floor |
| --- | --- | --- | --- |
| light 1440×900 | 1 069 | 42 | **0 of 42** |
| dark 390×844 | 763 | 37 | **0 of 37** |

`.page-lede`, `.chip-label`, `.img-credit`, `.page-kicker`, `.sec-title .count`,
breadcrumbs, `.footer-note`, `.main-nav a` and plain links are all in the
measured set and all pass.

**Re-verified again at the final HEAD (after 30c)**, because `.era-tile` shares
`--hero-text-veil` with the four `hero()` families and a token change would have
reached them:

| veil token | consumers | worst at final HEAD (light / dark) | verdict |
| --- | --- | --- | --- |
| `--hero-text-veil` | 4 × `hero()` + `.era-tile` | `header.hero` 6.06 / 8.27 (1440), 5.93 / 8.27 (390); `a.era-tile` 6.59 / 8.88 | **undisturbed** |
| `--hero-veil` (26a) | `.home-hero .hero-shade` | `h1.home-title` 3.79 / 5.19 (floor 3.0); `p.lede` 7.37 / 8.24; `div.kicker` 10.33 / 7.69 | **undisturbed** |
| `--mu-veil` (27) | `.mu-hero-body` | 0 of 7 classes below floor both cells; worst `span` 4.90 dark 390 | **undisturbed** |

`--mu-veil`'s figures are unchanged from unit 27's certified evidence and from
Vermeer's §3.2 table. 30c added no token and changed no token value — it reuses
`--hero-text-veil` — so the only way it could have reached these surfaces was
through the shared token, and it did not.

**Validator:** `osascript -l JavaScript tools/validate.jxa.js` → `app.js: syntax
OK` … `ALL REFERENCES VALID`. **Zero warnings**, run after each commit,
including after 30c.

---

# 5 — DEVIATION LEDGER

| id | deviation | why | effect | disposition |
| --- | --- | --- | --- | --- |
| **D-30-1** | Veil shipped at **`.80`**, not V-F3's specified **`.74`** | Re-derived against a worst-case opaque cover pixel, light's binding ink `--gold2` `#544019` (unit 29's re-point) needs **.740**; `.74` lands it at exactly **4.50**, a bound with zero margin. `.710` in V-F3 is `--body-ink`'s requirement, not the binding ink's | Strictly safer. Light `--gold2` 4.50 → **5.27**. `.80` is the home hero's dark `--hero-veil`, so no new value enters the system | **Accepted** |
| **D-30-2** | Fix applied to **all four** `hero()` families, not only `#/artist/*` | `hero()` is called from four view builders; `#/era/16th-century` 1.72, `#/technique/oil-painting` 1.76, `#/nation/italy` 2.43 all failed before | Fixing only the artist route would have left AC19 open on three route families | **Accepted** |
| **D-30-3** | `.hero .hero-shade` reduced to `.06 → .30` | Left at `.93` under the new veil the two composite to `.986` and the cover is effectively deleted | Cover retains ~14 % at the text block, matching the home hero. Values and rationale are unit 27's `.mu-shade`, cited | **Accepted** |
| **D-30-4** | Added `html[data-theme="light"] #app .hero-content h1:focus-visible{outline-color:#6b5122}` — not in either referral | The veil makes the ring's backdrop deterministic and light `--gold` reads **2.13** against it, under WCAG 1.4.11's 3.0 | 2.13 → **3.96**. Same remedy, same colour as unit 27's museum-band ring | **Accepted** |
| **D-30-5** | `canvastext.py` clip origin corrected (V-F2) | `clip` is page coords, rects are viewport coords | 89 previously-invalid rows re-analysed (unit 29's conclusion survives); 3 false `card-tagline` 4.10 rows withdrawn; 1 501 scrolled rows moved from NOT TESTED to measured and passing | **Accepted** |
| **D-30-6** | `.era-tile` fixed in this unit, outside the original brief | It is the same AC19 defect class and it was measured failing at 1.44–1.79 against a 4.5 floor. Writing "AC19 is fully supported" while leaving a measured, criterion-failing surface open would be false | 2 of 10 (host,class) pairs below floor → 0, all four cells | **Accepted** |
| **D-30-7** | `.era-tile`'s feather is **10 px**, not `.hero-content`'s 18 px | The feather must stay shorter than the block's `padding-top`, which is 12 px on this tile rather than 22 px | Same geometry; the one value the geometry requires differs, and is stated rather than forced | **Accepted** |
| **D-30-8** | Enumeration by paint differential (`covertext.py`) added beyond the brief | Four instances found by four accidents is a sampling process; the coordinator directed the switch to enumeration | All 20 `canvasTag` call sites classified; host census complete, route coverage bounded and declared | **Accepted** |
| — | Matisse's **§1d** optional follow-on not taken | He marked it optional and out of Gate 2 scope; it would reopen certified evidence at the last criterion | Small inconsistency between the two credit surfaces and prose links | **Deferred**, post-PIG-001 |

---

# 6 — NOT TESTED / NOT CLAIMED

Explicit, and not inferred from anything.

1. **Artists beyond the 12 sampled.** 256 exist. 12 painters × 4 hero families ×
   4 cells × 3 draws is a sample, not a census. The cover is per-subject
   generated, so the *pass* is a bound argument (the veil is derived against a
   worst-case fully opaque cover pixel and holds for any cover), not a claim
   that every one of the 256 was rendered.
2. **`#/movement/*` and `#/technique/*` beyond one subject each**, and
   `#/era/*` / `#/nation/*` beyond one each.
3. **Matisse's review of the underline** (his §Review) — not performed; needs
   Vermeer's captures of `#/credits`, `#/privacy`, `#/404`.
4. **Real assistive technology.** No VoiceOver/NVDA/JAWS session.
5. **Browsers other than Chrome.** Chrome headless only, `deviceScaleFactor: 1`.
6. **200 % text zoom over the new veil.** Not re-measured this unit; the veil is
   anchored to the text block and the feather is 18 px against a 22 px minimum
   padding, so reflow should not put a glyph in the ramp — but I did not measure it.
7. **Van Eyck's F-1 (821–1100 px overflow) and F-2 (masked focus indicator).**
   Outside this brief; both stand as recorded.
8. **Deployed identity.** Everything measured against a local `http.server`.

---

# 7 — PREVIEW

```
git checkout pig-001-stabilization
python3 -m http.server 8421 -d .
open http://localhost:8421/index.html#/artist/caravaggio
```
Compare `#/artist/caravaggio`, `#/era/16th-century`, `#/technique/oil-painting`,
`#/nation/italy` in both themes at 1440×900 and 390×844; then `#/credits` and
`#/privacy` for the underline.

Raw data: `harness/durer-u30/hero-{before,after}-{light,dark}-{1440,390}.json`
and `log-*.txt`; `harness/durer-u28/canvas-u30-regress-*.json`;
`harness/durer-u30/hero-u27-mu-*.json`.

---

# 8 — CLOSING STATEMENT ON AC19

Van Eyck certifies against this sentence, so it is written precisely.

**On the evidence in this log, AC19 is fully supported for every surface that
has been enumerated and measured, and I am not claiming more than that.**

Specifically:

- **V-F3 is closed, and closed wider than it was reported.** The `.hero` cover
  surface fails on four route families, not one; all four are bounded by one
  veil derived against a worst-case opaque cover pixel; 831 of 1 956 in-hero
  measurements were below floor before and **0** are now, in both themes at both
  viewports across 16 subjects and 3 draws — including dark 390×844, which was
  previously unmeasured. The painter's own name goes from 2.40/2.35 to
  8.80/10.21 against its 3.0 floor.
- **The three NOT TESTED items that bore on AC19 are closed by measurement.**
  `#/artwork/*` hero interiors (they do not fail, and structurally cannot fail
  the way V-F3 predicted); dark 390×844 for the hero class; and the 1 501
  scrolled canvas rows invalidated by V-F2, now measured with a corrected
  instrument and all passing.
- **`.era-tile` is closed** — the fourth instance of the same defect, found by
  enumerating rather than by waiting for it to fail in a screenshot: 1.44–1.79
  → 8.71–10.36 across all four cells.
- **Units 26a, 27, 28 and 29 are undisturbed**, verified structurally, then
  re-measured at HEAD, and re-measured a second time after 30c because
  `.era-tile` shares `--hero-text-veil` with the four `hero()` families.
- **One new WCAG failure that this unit's own fix created was found and closed
  in the same unit** (D-30-4, the hero focus ring at 2.13 against 1.4.11's 3.0).

- **`.era-tile` — the scrim my own first draft of this section flagged as
  unmeasured — was measured, and it failed, and it is fixed.** `b`, the era's
  name, read **1.44–1.79** against a 4.5 floor in all four cells; it now reads
  **8.71–10.36**. Flagging it was right; leaving it flagged would not have been.

**On the enumeration, precisely.** Vermeer's closing paragraph asks for the
scrims to be *enumerated* rather than the failures found one at a time. That is
done, and §3.5 is the deliverable:

- **The call-site enumeration is COMPLETE.** All **20** `canvasTag` call sites in
  `js/app.js` are classified by measured paint differential — not by my reading
  of the CSS, which is exactly how the first four instances were missed.
  Eighteen composite text over a cover and two do not. Four of the eighteen
  needed a veil; all four now have one; the other fourteen were never broken and
  are now **measured rather than assumed**.
- **The distinguishing property is now stated as a rule**, so the next author
  does not have to rediscover it: a cover needs a veil **iff a text block is
  overlaid on it**. The card and mini-card families set their text in a sibling
  block on opaque `--panel` paint — adjacent to the cover, not over it — which
  is why they never failed and why nothing in this unit touches them.
- **The route coverage behind that enumeration is BOUNDED, not exhaustive**:
  12 routes × 2 draws × 4 cells at HEAD, against 24 routes in the frozen
  inventory. Every unwalked route renders only hosts the table already covers.
  **I am claiming a host census, not a route census**, and that is the honest
  limit of this unit's claim.

The remaining NOT TESTED items in §6 — artists beyond the 12 sampled, Matisse's
visual review of the underline, real assistive technology, non-Chrome browsers,
200 % zoom over the new veil — are listed there and none of them is a measured
failure being reported as a pass.

Everything that has been enumerated and measured passes.
