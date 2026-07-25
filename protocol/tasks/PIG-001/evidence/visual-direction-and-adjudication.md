# VISUAL DIRECTION — PIG-001

**Author:** Matisse (`claude-visual-director`), Visual Design Director
**Date:** 2026-07-26 · branch `pig-001-stabilization`
**Two jobs:** (1) AC23 product adjudication; (2) AC19 contrast remediation direction.

This document directs; it does not build. Every value below is verified
arithmetic against `css/styles.css` at this commit, not estimated. Dürer
implements; Vermeer re-measures; Van Eyck certifies.

---

## INTENT

Pigment's light theme currently reads as *faded* where it means to read as
*quiet*. Those are not the same thing, and the difference is exactly the
43 failing pairs. A muted, contemplative, editorial identity is carried by
**hue, weight, spacing, and restraint** — not by low contrast. Nothing in
PIGMENT.md §5 asks for text that is hard to read; "poetic but usable" has
the word *usable* in it.

So the remediation below moves lightness only. Every proposed value keeps
its token's hue and saturation. The warm paper stays warm, the gold stays
gold, the tonal ladder (`--ink` → `--body-ink` → `--muted` → `--faint`)
stays four rungs deep and correctly ordered in both themes. What is lost is
named, per token, in the table's *Character cost* column. The dark gallery
theme — which already passes almost everywhere — is touched in exactly one
token and nowhere else.

Accessibility-driven constraints override styling preference (my role
definition, §Disagreement). AA is the frozen bar. I have flagged one item
below as **accept-as-is with rationale**, and it is the only one.

---

## SYSTEM

### Colour — token remediation (AC19)

**Verification method.** `evidence/contrast-audit.py` pass 1 scores every ink
against every surface; I re-ran it, then wrote a solver that preserves each
token's HSL hue and saturation and moves lightness only until the target
ratio is met on the **worst surface the token actually renders on**. Note a
correction to the audit's surface set: `--bg2` is declared in both theme
blocks but is **never used as a background anywhere** in `css/styles.css`
(`grep -n "var(--bg2)"` returns nothing). The real surfaces are `--bg`,
`--panel`, `--panel2`. Light's darkest real surface is `--panel2 #f0e9da`;
dark's lightest real surface is `--panel2 #1d1a13`. All ratios below are
against those three surfaces.

#### Table 1 — token replacements (implement directly)

| Token | Theme | Current | **Specified** | Verified ratio (bg / panel / panel2) | Floor | Surfaces & selectors affected | Character cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `--muted` | light | `#7a715e` | **`#585244`** | **6.59 / 7.19 / 6.42** | 4.5 | `p` in `.entry-card`/`.hpw-step`/`.lost` (768), `.brand-sub` (620), `.page-lede`, `.main-nav a`, `.footer-brand`, `.sr-meta`, `.sr-empty`, `.breadcrumbs a` | Secondary copy moves from washed to printed. Long-form prose already uses `--body-ink` and is unchanged, so the page's reading texture is not affected — only card taglines, the nav row and the wordmark sub-line get more ink. |
| `--faint` | light | `#a39a86` | **`#706755`** | **4.74 / 5.17 / 4.62** | 4.5 | all 18 `var(--faint)` uses — every one is text: `.footer-note` (207), `.chip-label` (21), `.breadcrumbs`, `.sec-title .count`, `.aw-provenance`, `.tl-year`, `.daily-return`, `.f-label`, `.map-hint`, `.tm-lab`, `.sr-group`, `.sr-hint`, `#search::placeholder`, `.tn-count`, `.pp-card-loading` | The largest single loss. The "barely there" tier disappears; `--faint` becomes a genuine tertiary ink sitting one visible step under `--muted` (4.74 vs 6.59 on `--bg`). This is the same gap the dark theme will now have (5.20 vs 6.40), so the two themes become symmetric rather than one being softer than the other. Accepted: there is **no** non-text use of `--faint` to preserve, so no decorative purpose is served by keeping it illegible. |
| `--gold` | light | `#a8813c` | **`#9e7938`** | **3.40 / 3.71 / 3.31** | **3.0** (UI/non-text only — see re-pointing below) | `.sec-title::before`, `.main-nav a::after`, `--line`, `#search:focus` border, `#theme-toggle:hover` border, `.skip-link`/`.skip-inline` border, `.chip.m:hover`, `.arc-work:hover`, `.btn`/`.aw-btn` borders, `::selection` background | Almost imperceptible (one lightness step). Fixes the `--panel2` 2.96 → 3.31, which was a genuine focus-indicator failure under 1.4.11. |
| `--gold2` | light | `#8a6a2e` | **`#81632b`** | **4.75 / 5.18 / 4.63** | 4.5 | `a{}` link colour (site-wide), `.ec-arrow`, `.aw-btn.primary`, `.footer-nav a:hover`, `.breadcrumbs a:hover`, `.img-credit a:hover`, `.btn`, plus all kicker text re-pointed here | Negligible. Fixes links, which were failing at 4.27. |
| `--wine` | light | `#a85544` | **`#a05141`** | **4.76 / 5.19 / 4.64** | 4.5 | `.entry-card --ec` (WANDER / Explore card, "Family trees"), `b` relationship text, chip hover borders | Negligible — a 4 % lightness move. |
| `--teal` | light | `#2e7a6e` | **`#2b7368`** | **4.75 / 5.18 / 4.63** | 4.5 | `.entry-card --ec` (BECOME / "The influence constellation"), `.one-detail` kicker on `#/daily`, `b` relationship text | Negligible. |
| `--blue` | light | `#4a6e9e` | **`#476a98`** | **4.72 / 5.14 / 4.59** | 4.5 | `.entry-card --ec` (GEOGRAPHY card), nation chips | Negligible. |
| `--rose` | light | *(new — hoisted from `js/app.js:995` `#c4536a`)* | **`#b43e56`** | **4.74 / 5.17 / 4.62** | 4.5 | relationship type `rivaled`: graph stroke, legend swatch, and the inline `<b>` at `js/app.js:1182,1837` | New token, but not a new colour: it formalises a hex already hardcoded in JS. |
| `--mauve` | light | *(new — hoisted from `js/app.js:996` `#d98ab0`)* | **`#b23a74`** | **4.76 / 5.19 / 4.63** | 4.5 | relationship type `partners`, same three sites | As above. |
| `--faint` | dark | `#6e675a` | **`#8b8372`** | **5.20 / 4.90 / 4.62** | 4.5 | same 18 selectors, dark theme | The **only** dark-theme token that changes. Dark `.footer-note` was 3.49 and `.chip-label` 3.29. The dark ladder becomes 15.72 / 12.97 / 6.40 / 5.20 — still four distinct rungs. |
| `--rose` | dark | *(new)* | **`#ca6478`** | **5.22 / 4.91 / 4.63** | 4.5 | as light `--rose` | Dark `#c4536a` measured 4.01 on `--panel2`; this is a minimal lift of the same hue. |
| `--mauve` | dark | *(new)* | **`#d98ab0`** | **7.65 / 7.20 / 6.79** | 4.5 | as light `--mauve` | **Unchanged value** — the existing hex already passes in dark. Hoisted to a token only so the light theme can flip it. |

**Tokens deliberately NOT changed:** dark `--muted`, `--gold`, `--gold2`,
`--wine`, `--teal`, `--blue`, and both `--ink` / `--body-ink`. All pass with
margin (worst: dark `--wine` 5.40). Do not "improve" them.

#### Table 2 — required re-pointings (selector changes, not token changes)

`--gold` in light is the only token asked to be two things at once: a 3:1
rule/border colour and a 4.5:1 text colour. Splitting the role is cheaper
than collapsing `--gold` into `--gold2`, which would flatten the two-step
gold. **Every text use of `var(--gold)` moves to `var(--gold2)`:**

| File:line | Selector | From | To | Resulting light ratio |
| --- | --- | --- | --- | --- |
| `css/styles.css:354` | `.page-kicker` | `var(--gold)` | `var(--gold2)` | 4.75 on `--bg` (was 3.04) |
| `css/styles.css:465` | `.why-kicker` | `var(--gold)` | `var(--gold2)` | 5.18 on `--panel` |
| `css/styles.css:546` | `.facts li::before` (✦) | `var(--gold)` | `var(--gold2)` | 5.18 on `--panel` |
| `css/styles.css:559` | `.work .w-year` | `var(--gold)` | `var(--gold2)` | 4.75 on `--bg` |
| `css/styles.css:737` | `.entry-card .ec-kicker` fallback | `var(--ec,var(--gold))` | `var(--ec,var(--gold2))` | 4.75 |
| `js/app.js:1459,1581` | `.entry-card` inline `--ec` | `var(--gold)` | `var(--gold2)` | 4.75 — this is the `div.ec-kicker` 127-occurrence failure |

`--ec` drives both the 3 px `.entry-card::before` rule **and** the kicker
text, so `--ec` must be text-safe; over-contrast on a 3 px rule is not a
defect. `.entry-card` inline `--ec` for teal / wine / blue stays as-is —
those tokens are fixed in Table 1.

Gold-as-fill check (`::selection`, `.btn:hover`, `.aw-btn.on`, `.f-btn.on`,
all `#171307` text on a `--gold` fill): **light 4.63**, **dark 7.90** with the
specified `--gold`. Both pass; no change needed. Verified.

#### Table 3 — theme-invariant hardcoded colours in JS

Two systems paint hexes that ignore the theme. Both must become
theme-aware. These are the remaining 30-odd failures.

**(a) Relationship colours — `js/app.js:991-997` `EDGE_STYLE`.**
`st.color` is used three ways: SVG `stroke`/marker `fill` (graphic,
1.4.11 → 3:1), the legend swatch `<i style="background:…">` (redundant with
its own text label → decorative), and **inline `<b style="color:…">` text at
`js/app.js:1182` and `js/app.js:1837`** (body text → 4.5:1). The text use is
what fails: light `#6fb3a8` on `#faf6ec` = 2.24, `#c4536a` = 4.06; dark
`#c4536a` = 4.01.

Direction: the `<b>` gets a class, not an inline colour, and the class
resolves to a theme token. Presentation attributes do not accept `var()`,
so if the SVG strokes are to follow the tokens they must be driven by CSS
classes (`.ig-edge.e-taught { stroke: var(--gold2) }`) rather than the
`stroke=` attribute — Dürer's call on mechanism; the mapping is mine:

| Relationship | Current hex | Token | Light ratio (worst surface) | Dark ratio (worst surface) |
| --- | --- | --- | --- | --- |
| `taught` | `#c9a45c` | `var(--gold2)` | 4.63 | 10.88 |
| `influenced` | `#6fb3a8` | `var(--teal)` | 4.63 | 7.18 |
| `befriended` | `#c97b6a` | `var(--wine)` | 4.64 | 5.40 |
| `rivaled` | `#c4536a` | `var(--rose)` **(new)** | 4.62 | 4.63 |
| `partners` | `#d98ab0` | `var(--mauve)` **(new)** | 4.63 | 6.79 |

The five types stay five distinguishable hues in both themes, and the dash
patterns (`""`, `5 4`, `""`, `2 4`, `""`) still carry type redundantly, so
none of this depends on colour alone.

**(b) Timeline bar labels — `js/app.js:952`.**
The current rule is `luma(c) > 0.62 ? "#1d1a14" : "#f6f1e6"`. The threshold
is a guess and the dark ink is not dark enough; it produces ~30 failures
from 2.42 (`#f6f1e6` on `#d9886e`, "Paul Signac") upward. Replace the
luma heuristic with a real contrast computation:

```
ink = contrast(#0d0c0a, fill) >= 4.6  ?  #0d0c0a
    : contrast(#f6f1e6, fill) >= 4.6  ?  #f6f1e6
    : (darken fill in HSL-L, hue and saturation fixed,
       until contrast(#f6f1e6, fill') >= 4.6)  and use #f6f1e6
```

`#0d0c0a` is the existing dark `--bg`; `#f6f1e6` is the existing bar paper —
no new colours. Verified against all 14 failing swatches:

| Swatch | Ink chosen | Fill after nudge | Ratio |
| --- | --- | --- | --- |
| `#d9886e` `#8a9bb0` `#e87a2e` `#d97a8a` `#c4763e` `#5e8ab0` `#8a8276` `#e0427a` `#b06a32` | `#0d0c0a` | unchanged | 4.61 – 7.17 |
| `#c4542e` | `#f6f1e6` | `#b44d2a` | 4.62 |
| `#c4541f` | `#f6f1e6` | `#b54d1d` | 4.61 |
| `#8a6e46` | `#f6f1e6` | `#836842` | 4.63 |
| `#c4423e` | `#f6f1e6` | `#c13f3b` | 4.61 |
| `#c43e4e` | `#f6f1e6` | `#c33c4c` | 4.58 |

Worst result **4.58**, all 14 pass. Only five swatches fall in the dead zone
where neither ink reaches 4.5; the largest lightness correction any of them
needs is **ΔL = 0.039** in HSL — four lightness points, hue and saturation
untouched. **This is a render-time display transform on the bar fill; the
palette data in `js/taxonomy.js` is not edited.** That distinction matters:
OD-4's "coordinates are never tuned to silence a validator" is about the
taste corpus, and this does not touch it.

### Colour — the hero over the generative canvas (AC19 / F-2)

A token change cannot fix this alone, because the glyphs are gradient stops
painted through `-webkit-background-clip:text` over a canvas whose pixels are
regenerated every visit. Anything that passes only against *the cover
Vermeer happened to sample* is not a fix. The mechanism must hold for **any**
cover.

**The bound.** With canvas opacity `o` and a paper scrim of alpha `s` over
the text block, the backdrop under a glyph is
`B = c·(α·o·(1−s)) + page·(1 − α·o·(1−s))`. The worst reachable backdrop is
the one produced by a fully-opaque **black** cover pixel, i.e. blend factor
`k = o·(1−s)`. Guarantee every hero text token against that backdrop and the
composite is safe for every cover forever.

**Specified mechanism — light theme only, three parts:**

1. **Darken the light hero gradient.** `css/styles.css:191-195`,
   `html[data-theme="light"] .home-hero-content h1`:
   - from `linear-gradient(92deg,#5e451c,#a8813c 38%,#5e451c 62%,#8a6a2e)`
   - to **`linear-gradient(92deg,#4a3616,#81632b 38%,#4a3616 62%,#6b5122)`**
   - The lightest stop `#81632b` is the new light `--gold2`, so the hero and
     the link colour agree. On plain paper the stops score 9.75 / 4.75 /
     9.75 / 6.31 — the old `#a8813c` scored 3.04, i.e. it cleared the
     large-text floor by 0.04 even with **no** canvas behind it.
2. **Strengthen the light-theme hero scrim over the text block.**
   `css/styles.css:701`, scoped to `html[data-theme="light"] .home-hero .hero-shade`
   — dark's `radial-gradient(ellipse at center,rgba(var(--bg-rgb),.25),rgba(var(--bg-rgb),.88) 88%)`
   is untouched. Requirement: **effective paper alpha ≥ 0.72 everywhere
   `.home-hero-content` paints text**; free to thin outside that box so the
   cover still reads at the frame. A gradient that satisfies it:
   `radial-gradient(ellipse 96% 74% at 50% 42%, rgba(var(--bg-rgb),.84) 0%, rgba(var(--bg-rgb),.74) 62%, rgba(var(--bg-rgb),.38) 84%, rgba(var(--bg-rgb),.66) 100%)`.
   `#bg-canvas{opacity:.6}` at `css/styles.css:190` is **unchanged** — the
   cover keeps its strength; only the title block gets a paper haze.
3. **Raise the hero's small text one rung in light theme.** A scrim cannot
   carry 4.5:1 small text in the worst case without effectively hiding the
   cover (α ≈ 0.96 required for gold at that size — I checked; that is not
   an acceptable trade). So inside `.home-hero-content`, light theme only:
   - `.kicker` ("PIGMENT · A TASTE ATLAS OF PAINTING") → `var(--ink)`
   - hero lede and `.footer-note` cover credit ("Tonight's cover: mixed
     after …") → `var(--body-ink)`

**Verified at `o = .60`, `s = .72` (k = 0.168, worst backdrop `rgb(201,196,186)`):**

| Hero element | Colour | Worst-case ratio (black cover) | Floor | Verdict |
| --- | --- | --- | --- | --- |
| `h1` stop `#4a3616` | gradient | **6.62** | 3.0 | PASS |
| `h1` stop `#81632b` (lightest, governs) | gradient | **3.23** | 3.0 | PASS |
| `h1` stop `#6b5122` | gradient | **4.29** | 3.0 | PASS |
| `.kicker` | `--ink` `#2b2620` | **8.66** | 4.5 | PASS |
| hero lede | `--body-ink` `#433c31` | **6.28** | 4.5 | PASS |
| cover credit | `--body-ink` `#433c31` | **6.28** | 4.5 | PASS |

Over Vermeer's nine actually-sampled canvas pixels the title scores **4.49**
(vs 2.47 today). **Minimum the mechanism must achieve: 3.0:1 for the title
(large text) and 4.5:1 for the kicker, lede and cover credit — under a
worst-case fully-opaque black cover pixel, not under a sampled average.**
Dark theme untouched; it measures 6.20 and stays there.

**Character cost, stated plainly:** in the light theme the generative cover
is veiled behind the title block. The cover is Pigment's hero image and this
takes something from it. Three things make the trade acceptable: dark is the
default theme and is untouched; the veil is shaped to the text box, so the
cover reads at full strength around the frame; and a title nobody can read
is not a hero either.

### Typography, spacing, imagery, motion

No changes directed. The type scale (`clamp(2.6rem,6.5vw,4.8rem)` hero,
Playfair display / Inter sans pairing), the 3 px `--ec` card rule, the
`.sec-title::before` 30 px rule, the generative-cover language and the
`--ease` motion curve are all coherent and are working. `prefers-reduced-motion`
is out of my scope here (AC20, Van Eyck). Do not touch them in this pass.

### Responsive composition — the two open findings

**F-1, nav at 200 % text zoom.** `nav.main-nav` is `display:flex; gap:4px; flex:1`
with implicit `flex-wrap:nowrap` (`css/styles.css:256-258`); at 200 % it measures
1359 px in a 1270 px viewport and pushes every one of 26 routes 115–117 px wide.
Visible in `zoom200-home__desktop-1280x800__light.png`: "NATIONS" is sheared at
the right edge while the search field and theme toggle have already wrapped
below.

**Direction: wrap. Not scroll, not collapse.**

- *Wrap* — `flex-wrap:wrap` on `.main-nav`, with `row-gap` matching the
  existing 4 px `gap`. Eight uppercase destinations become two or three rows
  at 200 %. Every destination stays visible and keyboard-reachable with no
  new affordance to learn, no new control to name for AT, and no new focus
  trap. It is one declaration.
- *Scroll with an affordance* is rejected: it would introduce a named
  horizontal region that AC18 then requires to be independently operable and
  labelled, i.e. new controls, new accessible names, new focus order — a
  larger surface than the defect, inside a stabilization task.
- *Collapse to a menu* is rejected outright: `mobile-nav discoverability` is
  already on the known-defect register. Adding a second disclosure pattern at
  200 % zoom would multiply an unsolved problem.

The header's outer row already wraps correctly (Wave A's fix works — the nav
drops to its own line, `left` 229 px → 28 px). Wrapping the nav row is the
same fix one level down, and it composes with what is there.

Also clipped at 200 % and in scope with it: `div.mu-hero` (942 px lost on
`#/museum/louvre`), `div.card-tagline` (266 px on `#/`, `#/lists`, `#/list/…`),
and `button.skip-inline` (109 px on `#/influences`). Direction: these are
`overflow:hidden` containers sized for a fixed line count. Replace the fixed
heights with `min-height` + `overflow:visible` so the box grows with the
text. **`button.skip-inline` is the priority of the three** — a bypass
control that is itself clipped is a worse defect than a truncated tagline.
While it is being touched, give it Pigment's button styling: it currently
computes `#000000` on `#efefef` in **both** themes (F-6), which is
user-agent default, not a Pigment token. `.btn`'s existing
`border:1px solid var(--gold); color:var(--gold2); background:var(--panel2)`
is the right treatment — contrast verified above.

---

## CONTINUITY

**Reused from `css/styles.css`:** every remediation in Table 1 adjusts an
existing custom property in place, in its own theme block, preserving hue and
saturation. No parallel palette. `--ink`, `--body-ink`, both `--panel`s, the
`--line`/`--line2` rgba pairs, `--serif`/`--sans`, `--ease`, the `--ec`
mechanism, `.hero-shade`, `.entry-card`, `.sec-title` and the generative
covers are all reused unchanged.

**New, and why:** exactly two tokens, `--rose` and `--mauve`, in both theme
blocks. They are not new colours — they are `#c4536a` and `#d98ab0`, already
hardcoded in `js/app.js:995-996`, hoisted into the system so the light theme
can flip them. Dark `--mauve` is byte-identical to the current hex. This
makes the palette smaller in spirit, not larger: five relationship types now
resolve through the same token layer as everything else.

**What is explicitly not touched:** the dark theme (one token, `--faint`),
`#bg-canvas{opacity:.6}`, the type scale, spacing rhythm, motion, and every
token that already passes.

---

## CHALLENGES RAISED

1. **`--faint` was never a decorative token.** All 18 uses are text. There is
   no "faint rule" or "faint hairline" to protect, so the argument for
   keeping it below 3:1 in light was never an aesthetic argument — it was an
   unexamined default. Raised and resolved by darkening.
2. **`--bg2` is dead.** Declared in both theme blocks, referenced nowhere.
   The audit scored it as a surface, which made three tokens look worse than
   they render. I have scored against the three real surfaces instead. Not a
   defect; flagged so nobody "fixes" contrast against a phantom surface.
   Removing it is out of scope for this task.
3. **A hero fix validated against one sampled cover is not a fix.** The
   covers are regenerated per visit. I have specified the mechanism against a
   worst-case black cover pixel and given Dürer the bound, not a sample.
4. **The light theme was quieter than the dark theme, and called it style.**
   After remediation the two ladders are symmetric (light 12.73/9.25/6.59/4.74;
   dark 15.72/12.97/6.40/5.20). Pigment should not have a "good" theme and a
   "pretty" theme.
5. **Decorative prominence on thin routes** — see REVIEW item 5. I am
   recording this as a CONCERN, not directing a change inside PIG-001, because
   the fix is compositional rather than a token value and would exceed a
   stabilization scope.
6. **The mobile evidence is not sound for composition judgements** — see the
   note under REVIEW item 6. This is an evidence defect, not a product defect,
   and I have adjudicated only what the shots can actually support.

### Accepted as-is, with rationale — one item

**The five dead-zone timeline swatches receive a ≤ 0.039 HSL-lightness
darkening at render time.** I considered accepting them at 4.20–4.50 and
refused: AA is the frozen bar and 4.50 is not 4.5 by luck. I also considered
moving the label out of the bar (guaranteed pass, no colour change) and
rejected it as a layout rewrite inside a stabilization task. The display
transform is the smallest change that clears the bar. What is accepted as-is
is the **hue**: no swatch changes hue or saturation, and no palette record
is edited.

Nothing else is accepted below AA. "It looks nicer" did not carry any item.

---

## REVIEW — AC23 PRODUCT ADJUDICATION

> **Scope statement, per the criterion.** AC23 asks a named adjudicator to
> review the built product against frozen product signals and to record
> observations and tradeoffs **without claiming unmeasured user comprehension
> or preference**. No user research was authorised or performed. Nothing below
> asserts what a visitor would think, understand, notice, feel, or prefer.
> Every finding is a statement about what is present in the interface and how
> it is weighted, verifiable from the cited screenshot. Where the honest
> answer requires knowing what a person perceived, I say so and stop.

**Evidence:** 74 screenshots in `protocol/tasks/PIG-001/evidence/`
(16 routes × {1440×900, 390×844} × {dark, light}, plus 6 passport-import and
4 200 %-zoom shots). I viewed a representative set spanning home, explore,
artists, artist detail, daily, taste, timeline, influences, credits, privacy,
invalid-route, passport-import-conflicts, in both themes and both viewports.
Frozen signals: PIGMENT.md §5, `docs/STYLE_GUIDE.md`, OD-1, OD-2.

### Item 1 — Opening hierarchy · **CONCERN**

*Is the recommended first action identifiable without reading every route
description? Is the multi-door baseline preserved?*

Observed (`home__desktop-1440x900__dark.png`, `…__light.png`,
`home__mobile-390x844__light.png`): three `.entry-card`s below the hero —
BEGIN / "Start with an artist", BECOME / "Find your palette", WANDER /
"Explore the atlas". They are rendered at **identical** width, padding,
border, corner radius, background, kicker size, `h3` size (1.4rem) and body
size (0.9rem). `.entry-cards` is `repeat(auto-fit,minmax(250px,1fr))`, so the
three columns are equal by construction.

OD-2 ratifies "Start with an artist" as *the recommended first action*.
The only signals that distinguish it from the other two in the rendered
composition are: (a) leftmost position in reading order; (b) its gold `--ec`
rule versus teal and wine; (c) a secondary "or surprise me →" link that the
other two cards lack. (b) is a categorical hue difference, not a rank
difference — the same three-hue vocabulary is used on `#/explore` for four
peer instruments (`explore__desktop-1440x900__dark.png`), where no ranking is
intended. So the recommendation is carried by **position alone**, plus the
card's own prose.

**Multi-door baseline: PASS.** Three doors are present, all visible above
the fold at 1440×900, all reachable, none subordinated into a menu.

**Recommendation identifiable without reading descriptions: CONCERN.** The
interface encodes "recommended" nowhere in weight, size, or a ranking label —
only in order. I record this as a compositional fact. Whether any visitor
resolves the recommendation from position is precisely the unmeasured
question AC23 forbids me to answer, and I do not answer it.

Contrast with `taste__desktop-1440x900__dark.png`, where a single primary
control ("Find your palette →", the only button on the route) makes the
recommended action unambiguous in the composition itself. The vocabulary for
ranking exists in the system; it is not applied on `#/`.

*Tradeoff, recorded not resolved:* elevating one of three equal doors is a
product decision touching a ratified-but-reserved owner decision (OD-2 says
Arda "is not certain about its long-term future and reserves the right to
revisit"). Directing a visual promotion of card 1 inside PIG-001 would
pre-empt that. Recommend it be routed as a follow-up alongside the OD-2
"artists as figures users identify with" direction, not built here.

### Item 2 — Relationship signal in the opening experience · **CONCERN**

*Is at least one meaningful relationship demonstrated rather than asserted?
Does relationship read as consequence, not decoration?*

Observed on `#/` above the fold: the hero lede reads "…and every connection
that made them"; card 1's tagline reads "…follow the threads — teachers,
rivals, movements, and the works that made them matter"; card 3 promises "an
influence constellation, family trees of movements". Every one of these is a
**claim about** relationships. In the opening viewport at 1440×900 no named
entity is joined to another named entity by a stated relationship — no edge,
no pair, no "X taught Y".

Where relationship **is** demonstrated, it is demonstrated well, and as
consequence rather than decoration:

- `explore__desktop-1440x900__dark.png` — "238 relationships — taught,
  influenced, befriended, rivaled, partnered — drawn as one force-directed
  web."
- `influences__desktop-1440x900__dark.png` — 204 painters, 238 typed and
  colour-coded edges, a per-type legend with counts (taught·30,
  influenced·133, friends·57, rivals·14, partners·4), and a lede that names
  two concrete chains: Theophanes → Rublev, Warhol ↔ Kusama. That is a
  demonstration with named entities and stated relationship types.
- `artist-leonardo__desktop-1440x900__light.png` — "Kindred spirits" panel;
  and card copy elsewhere states consequence directly ("Byzantium's lightning,
  loosed on Russian walls — **Rublev's teacher**",
  `artists__desktop-1440x900__light.png`). That is a relationship carrying a
  consequence inside a list cell, which is the strongest form of it I saw.

So the capability is real and it is not decorative. The finding is narrow and
specific: **the opening viewport of `#/` asserts the atlas's relationship
promise; it does not instantiate it.** The nearest demonstration is one
navigation away.

*Tradeoff:* the home hero's job is also to carry the generative cover and the
three doors; adding a demonstrated relationship above the fold competes for
the same space. Not directed here.

### Item 3 — Entrances: global taxonomic access vs guided first-time entry · **PASS**, with a recorded gap

*Are they distinguishable?*

Two systems are present and their visual vocabularies do not overlap:

- **Global taxonomic access** — `nav.main-nav`: eight uppercase, letterspaced,
  0.86 rem sans labels in a single row (ARTISTS · LISTS · MUSEUMS · EXPLORE ·
  MOVEMENTS · TECHNIQUES · ERAS · NATIONS), plus persistent search. Uniform
  weight, no ranking, present on every route. Active state is `--gold2` +
  `font-weight:700` + a 2 px underline — not colour alone
  (`artists__desktop-1440x900__light.png`, `explore__…__dark.png`).
- **Guided entry** — the `.entry-card` system: serif `h3`, coloured kicker,
  3 px `--ec` rule, prose tagline, arrow affordance. Used on `#/` for the
  three doors and on `#/explore` for the four instruments.

The two are unambiguously different objects in the composition. **PASS.**

Recorded gap, not a failure of this item: the two entrances AC23 names —
**Daily and Taste** — have no presence in `nav.main-nav`. `#/taste` appears
only in the footer (`taste__desktop-1440x900__dark.png`, footer row) and
"Painting of the Day" only on `#/` below the fold. "Taste in global
navigation" is already on the frozen deferred-promise register, so this is a
known deferral, not a regression. I note it because it means the guided path
is absent from persistent chrome once a visitor leaves `#/`.

`#/explore` and `nav.main-nav` name the same four instruments (timeline,
influence constellation, family trees, world map) — consistent with AC22,
which is Van Eyck's to certify, not mine.

### Item 4 — Identity without wordmark, dark ground, or display face · **PASS**

*Is the product still recognisably Pigment? Does the new material sit inside
the visual system or read as bolted on?*

Testing the harder case — the **light** theme, which removes the dark ground,
and looking past the wordmark and Playfair:

`daily__desktop-1440x900__light.png` is the strongest single piece of
evidence. Identity survives on: the kicker-over-title rule
("PAINTING OF THE DAY · SUNDAY, JULY 26, 2026"); the serif marginal statistic
("**75** WORKS IN THIS DAILY ROTATION"); the teal rule-and-kicker aside
("ONE DETAIL YOU CANNOT UNSEE — Find the three muskets: loading, firing,
clearing — a manual in one frame"); the three-verb action row (Admire · Seen
in person · Save for later) with Admire as the only outlined primary; the
"GO DEEPER INTO THE ARTWORK →" onward step; the warm-paper generative ribbons.
Cover the wordmark and change the typeface and the composition is still a
specific product with a specific voice. **PASS.**

New material:

- **Credits** (`credits__desktop-1440x900__light.png`) — ATTRIBUTION kicker,
  display title, `.sec-title` em-rule sections ("— Wikimedia Commons",
  "— Museum photographs" with an inline `104 buildings · 88 under a licence
  requiring credit" count in the same `.sec-title .count` slot used by the
  atlas routes), two-column credit rows. **Inside the system.**
- **Privacy** (`privacy__mobile-390x844__light.png`) — same kicker/title/lede
  spine, `.sec-title` sections, inline `<code>` for the three storage keys.
  **Inside the system.**
- **Photo credits** — rendered next to the picture and repeated on Credits;
  uses the existing `.img-credit` treatment. **Inside the system.**
- **Four-instrument Explore hub** (`explore__desktop-1440x900__dark.png`) —
  reuses `.entry-card` verbatim, extending the three-door vocabulary to four
  with the same kicker/rule/serif/arrow grammar. It is the same object as the
  home doors, not a new one. **Inside the system.**

Nothing in the new material reads as bolted on. Note that the *reason* it
holds is the kicker + display-serif + em-rule + coloured-rule grammar — which
is exactly what the contrast remediation must not destroy, and does not: the
grammar is structural, and only lightness moves.

### Item 5 — Does any decorative system outrank its information? · **CONCERN (light theme)** / PASS (dark)

Two observations, both from pixels.

**(a) The generative ribbon backdrop on thin routes — light theme.**
`invalid-route__desktop-1440x900__light.png`: the route carries one display
title ("Blank canvas") and one sentence with two links. Behind them, four
full-width wine/teal/gold ribbon sweeps occupy the entire viewport. By area
the decorative system is the dominant element on the route by a wide margin.
This becomes a defensible *inversion* rather than a matter of taste when set
against the AC19 numbers: today the `.footer-note` ink in light measures
**2.37:1** while those ribbons are painted at higher local contrast against
the same paper. A decorative layer is rendered more strongly than compliant
text on the same page. Same pattern, less extreme, on
`credits__desktop-1440x900__light.png` (ribbons crossing the credit column)
and `taste__desktop-1440x900__dark.png` (≈ 500 px of backdrop below a 3-line
empty state — dark, so far less visible).

The Table 1 remediation *reduces* this inversion by raising every ink above
the ribbons; it does not remove it. **CONCERN**, recorded not directed:
the fix is compositional (constrain backdrop amplitude on text-only routes,
or bound the empty-state canvas height) and exceeds a stabilization scope.

**(b) The influence graph at full density.**
`influences__desktop-1440x900__dark.png`: at 204 nodes the labels collide in
the dense right-hand cluster — "Käthe Kollwitz" / "Kitagawa Hokusai" /
"Pierre-Auguste Renoir" / "Salvador Dalí" overlap each other and their edges;
"Andrei Rublev" is crossed by an edge. Readability degrades exactly where
edge density — the information — is highest. The visualization is not
decorative (it is the route's content, it is typed, counted and legended, and
a keyboard bypass exists), so it does not fail the criterion's letter. But
the ornamental cost is concentrated where the informational payload is
greatest, which is the same inversion in a different form. Recorded.

**Dark theme, all other routes: PASS.** Chrome recedes; the artwork and the
generative covers are the strongest elements, which is the intended order.

### Item 6 — Mobile hierarchy at 390 px · **PASS on what the evidence supports**, with an evidence defect recorded

**Evidence defect, stated first.** The 390×844 captures are genuinely
390 px wide files, but their content is laid out at a wider measure and
cropped: on `privacy__mobile-390x844__light.png` body lines are sheared
mid-word at the right edge ("what it sen…", "(localS…"), on
`home__mobile-390x844__light.png` the hero title is cut ("…in the histor"),
and `nav.main-nav` is absent from every mobile shot. Vermeer's independent
DOM measurement reports `scrollWidth == clientWidth == 390` on all 26 routes,
and that measurement is taken in JS and does not depend on the capture. The
two are only reconcilable if the harness rasterised a wider layout into a
390 px frame. **I therefore cannot adjudicate final line-breaking, wrapping,
or edge composition at 390 from this evidence, and I do not.** Recommend
Vermeer re-capture at a correct 390 device metric before Gate 2; this is an
evidence-package defect for Van Eyck, not a product finding.

**What the shots do support** — vertical order and relative weight, which
survive the crop:

- `home__mobile-390x844__light.png`: kicker → hero title → lede → cover
  credit → cards stacked in the desktop order, "Start with an artist" first.
  The hero title remains far the largest element; card `h3`s are secondary;
  taglines tertiary. Importance is preserved down the stack.
- `artists__mobile-390x844__dark.png`: kicker → display title ("All 256
  painters") → lede → filter chips → one full-width card per row with the
  generative cover dominant, name, dates, tagline, movement chip. A clear
  four-level hierarchy, not a flat stack.
- `explore__mobile-390x844__dark.png`: the four instruments stack in order,
  each retaining its coloured rule, kicker, serif title and prose — the
  desktop card grammar survives the single-column reflow intact.

**Nothing stacks at equal weight.** The one composition that is flat at
390 is flat at 1440 too — the three home doors — and that is item 1's
finding, not a mobile-specific one. **PASS**, scoped to what the evidence can
carry.

### AC23 verdict summary

| # | Item | Verdict |
| --- | --- | --- |
| 1 | Opening hierarchy — recommended first action / multi-door baseline | **CONCERN** (baseline PASS; recommendation carried by position alone) |
| 2 | Relationship demonstrated vs asserted in the opening experience | **CONCERN** (asserted on `#/`; demonstrated well one step away, as consequence not decoration) |
| 3 | Global taxonomic access vs guided first-time entry distinguishable | **PASS** (Daily/Taste absent from persistent nav — known deferral, recorded) |
| 4 | Identity without wordmark / dark ground / display face; new material inside the system | **PASS** |
| 5 | No decorative system outranks its information | **CONCERN in light theme** (backdrop outweighs sub-AA text on thin routes); PASS in dark |
| 6 | Mobile hierarchy at 390 px preserves importance | **PASS on supported evidence**; mobile capture defect recorded for Van Eyck |

**No item FAILS.** Two PASS, three CONCERN, one PASS-with-evidence-caveat.
The three CONCERNs are recorded observations with tradeoffs, per the
criterion; none is directed as a PIG-001 build item, and none of them claims
anything about what a visitor perceived.

---

## ADVICE — C-8, double route announcement (AC15 / F-4)

Not a colour problem, so this is advice rather than direction.

Vermeer measured both channels firing on every route change: focus moves to
`h1[tabindex="-1"]` (announced) **and** `#route-status` mutates once
(announced). In 3 of 5 sampled routes the two carry different wording —
"The grand timeline" / "Timeline", "Blank canvas" / "Lost", "Find your
palette." / "Find your palette".

**Reconcile to one channel: keep the focus move, drop the live region.**
Focus movement is the stronger signal — it announces the page identity *and*
places the caret at the content, which is what AC15 asks for ("moves focus to
a meaningful entry point"). A `role="status"` region that merely restates the
heading adds a second announcement with no additional information. Removing
it eliminates the duplicate and the divergence in one change, and cannot
produce a mismatch because there is then nothing to mismatch.

**If both channels are retained,** the wording must be identical, and the
`h1` is the authority — it is the visible, persistent, editorial string, and
"The grand timeline" and "Blank canvas" are Pigment's voice while "Timeline"
and "Lost" are labels. Do not fix the divergence by flattening the `h1` to
match the live region; that would trade a duplicate announcement for a loss
of voice.

**Van Gogh (`claude-content-editor`) owns sentence-level voice.** If any
string is rewritten rather than deleted, route it to him. My recommendation
(drop the live region) requires no rewrite at all, which is one more reason to
prefer it.

---

## HANDOFF

- **Dürer** — implement Tables 1, 2, 3, the hero mechanism (3 parts), the
  `.main-nav` wrap, and the three clipped containers. Every value is verified;
  do not re-derive them, and do not substitute "close enough" hexes — several
  clear the bar by under 0.15.
- **Vermeer** — re-run `contrast-audit.py` (pass 1 will need `--rose`/`--mauve`
  added to `FOREGROUNDS`; the `SURFACES` list should drop the unused `--bg2`),
  re-walk the 139 rendered pairs, re-sample the light hero composite, and
  re-capture the 390 shots at a correct device metric.
- **Van Eyck** — AC19 remains FAIL until Vermeer's re-measurement returns
  zero failures. This document is the AC23 adjudication record; the mobile
  capture defect in item 6 is yours to disposition before Gate 2.
