# PIG-001 — Unit 29 build log (F-7 / AC19: closing the `#bg-canvas` text class)

**Implementer:** Dürer (`claude-implementation-lead`) · branch `pig-001-stabilization`
(verified: **not** `main`; no push, no merge, no deploy) · Gate 1 satisfied
(`specification.md` at `approved_for_build`).

Unit 29 answers **F-7**, the single open major from Van Eyck's Revision 2
(`GATE 2: BLOCKED` · PASS 28 · FAIL 1). F-7 is my own reported finding: unit 28 §7
says plainly *"AC19 is NOT fully supported."*

Every number below was measured or derived by me against the committed CSS. Where a
number is a **bound** it says so and says which bound. Where a cell was **not
measured**, it says that too.

## Commit

| Commit | Finding | Files |
| --- | --- | --- |
| `4362c8a` | F-7 · AC19 | `css/styles.css`, `index.html` |

`?v=` bumped `20260728-pig001-u28` → `20260728-pig001-u29` on the stylesheet.
**`js/app.js` was not touched**; its `?v=` is unchanged. No new dependencies, no
build step. Committed by explicit path; `THEORY_001.md`,
`protocol/tasks/PIG-001/CHALLENGE_001` and `protocol/tasks/PIG-001/THEORY_001` were
left untracked and untouched. **Unit 27's `--mu-veil` band work and unit 28's two
call sites were not touched** — both pass and are certified evidence, and both are
re-measured clean in §4 below.

---

## 1 — The correction that made this unit different: the canvas cannot be sampled

Unit 28 measured this class with a 24-draw model of the canvas. I began unit 29 by
widening that model, as N-5 requires — 30 more draws at 1440 and 30 at 390, per
theme, unioned with unit 28's 24 → **84 draws per theme**. The bound moved:

| ink | unit 28 model (24 draws) | union model (84 draws) |
| --- | --- | --- |
| light `--muted` | 4.47 | **4.07** |
| light `--faint` | 3.22 | **2.92** |
| dark `--faint` | 3.69 | **3.62** |

It moved by 0.40 on the token the whole remedy depended on, and it was **still
moving**. That is the real lesson of F-7, and it generalises the one Van Eyck
recorded: a clean Pass 1 clears nothing because it measures flat paint — and a
sampled bound clears nothing either, because `#bg-canvas` is `Math.random`-seeded
and 84 draws are 84 samples of a continuous space. Had I designed token values to
sit just above 4.5 on my own sample, Van Eyck's next sample would have found worse
and blocked the build a third time.

**So the canvas is bounded from its source instead, and the bound cannot be beaten
by any draw.** From `js/app.js:2749-2812`:

- `light` — `comp: source-over`, `blobA .10`, `ribA .10`, element `opacity .6`
- `dark` — `comp: lighter`, `blobA .16`, `ribA .07`, element `opacity .5`
- halo and core are two strokes of the **same** ribbon path, the core inside the
  halo, so a core pixel takes both: `1-(1-.10)(1-.18) = .262` source-over,
  `.07+.126 = .196` additive.

Each layer's alpha is continuous in `[0, a_max]` (radial-gradient and stroke
falloff) and **both composite formulas are monotone in it**, so the extreme sits at
a corner of the layer cube. There are only 2⁸ = 256 corners, and they are
enumerated exactly rather than sampled. Two ceilings are reported because they
answer different questions:

| ceiling | assumption | worst reachable backdrop |
| --- | --- | --- |
| **ALL** | every blob centre **and** every ribbon core coincident on one pixel | **dark `rgb(101,88,76)`** · **light `rgb(187,174,162)`** |
| **REAL** | 5 blob centres + at most 2 ribbon cores. Ribbon bases are `.18/.46/.74` of `H` (+≤`.08`) with amplitude ≤`.12×1.4`, so ribbons 0 and 2 **cannot** reach each other | dark `rgb(82,76,65)` · light `rgb(186,184,171)` |

The union model is calibrated against unit 28's published table before use: it
reproduces dark `--faint` 3.69, dark `--muted` 4.54, light `--faint` 3.22, light
`--muted` 4.47, light `--gold2` 3.22 at 24 draws — to the second decimal, same
numbers, independently rebuilt. Van Eyck's own single-blob derivation (4.34/4.33)
sits between the sampled and derived bounds, as it should.

### What the ceiling says, and it is not "twelve selectors"

| theme | `--faint` | `--muted` | `--gold2` | `--teal` | `--body-ink` | `--ink` |
| --- | --- | --- | --- | --- | --- | --- |
| dark ALL | **1.82** | **2.24** | **4.30** | **2.84** | 4.55 | 5.51 |
| light ALL | **2.57** | **3.57** | **2.58** | **2.57** | 5.01 | 6.90 |

**Only `--body-ink` and `--ink` clear the 4.5 small-text floor over this canvas, in
either theme.** `--muted` is not marginal — it is 2.24 dark. No nudge rescues it,
and the one obvious lever does not either: I recomputed the opacity Dürer-28 and
Van Eyck both rejected, and confirmed it exactly — `--faint` would need the canvas
at **.106 dark / .057 light** against a shipped `.5`/`.6`.

---

## 2 — What changed

**The rule, now written into the stylesheet at `#bg-canvas`:** small text on the
**page background** takes `--body-ink`; `--faint` and `--muted` remain **panel
inks**, where Pass 1 of `evidence/contrast-audit.py` measures them clear. That
distinction is exactly what the flat-paint pass could not see, and why this class
survived 28 units.

### 26 selectors re-pointed

| # | selector | before | after |
| --- | --- | --- | --- |
| 1 | `.breadcrumbs` | `--faint` | `--body-ink` |
| 2 | `.breadcrumbs .sep` | `--faint` | `--body-ink` |
| 3 | `.chip-label` | `--faint` | `--body-ink` |
| 4 | `.aw-provenance` | `--faint` | `--body-ink` |
| 5 | `.daily-return` | `--faint` | `--body-ink` |
| 6 | `.filter-bar .f-label` | `--faint` | `--body-ink` |
| 7 | `.map-hint` | `--faint` | `--body-ink` |
| 8 | `.footer-nav a` | `--faint` | `--body-ink` |
| 9 | `.footer-note` | `--faint` | `--body-ink` |
| 10 | `.brand-sub` | `--muted` | `--body-ink` |
| 11 | `.breadcrumbs a` | `--muted` | `--body-ink` |
| 12 | `.hero-content .breadcrumbs` | `--muted` | `--body-ink` |
| 13 | `.page-lede` | `--muted` | `--body-ink` |
| 14 | `.sec-title .count` | `--muted` (unit 28) | `--body-ink` |
| 15 | `.mini-card .mc-meta` | `--muted` | `--body-ink` |
| 16 | `.daily-kicker span` | `--muted` | `--body-ink` |
| 17 | `.f-btn` | `--muted` | `--body-ink` |
| 18 | `.tl2-leg` | `--muted` | `--body-ink` |
| 19 | `.footer-brand` | `--muted` | `--body-ink` |
| 20 | `.main-nav a` | `--muted` | `--body-ink` |
| 21 | `.era-tile .et-label span` | `--muted` | `--body-ink` |
| 22 | `.daily-sequence` | `--muted` | `--body-ink` |
| 23 | `.lost p` | `--muted` | `--body-ink` |
| 24 | `.daily-detail b` | `--teal` | `#b0dad3` dark / `#1b4a43` light |
| 25 | light `--gold2` **token** | `#81632b` | **`#544019`** |
| 26 | light `a:hover` | `#fff` (inherited from dark) | `var(--ink)` |

Rows 1–23 are the `--faint`/`--muted` class. Rows 20–23 were **not** in F-7's
selector list and **not** in my own unit-28 census; they were found by re-running
the enumerator after the first pass of edits and re-auditing — see §4.

### Three corrections to the specified fix, each measured rather than assumed

**a. `#6b5122` does not clear, so light `--gold2` went to `#544019`.**
The routed remedy was `--gold2` → `#6b5122`, "already in the palette from unit 27".
It is in the palette — as a **large-text** stop in the light home-title gradient, at
a 3.0 floor. It was never validated as small text over the canvas, and it does not
hold there:

| candidate | flat | union84 | REAL | ALL | |
| --- | --- | --- | --- | --- | --- |
| `#81632b` (shipped) | 4.75 | 2.93 | 2.81 | 2.58 | fails |
| **`#6b5122`** (routed) | 6.31 | **3.89** | **3.73** | **3.42** | **fails** |
| `#624a1f` | 7.08 | 4.37 | 4.18 | 3.84 | fails |
| **`#544019`** (shipped u29) | 8.40 | **5.18** | **4.96** | **4.55** | **clears all three** |

`#544019` is a new hex and it is the smallest step that clears the derived ceiling,
not merely my sample. It holds the gold hue; the accents that also read `--gold2`
(`.brand-dot`, `.chip.a::before`, `.main-nav a.active::after`, `.hero-accent`) are
fills and rules at a 3:1 floor and only get **darker** against warm paper, so none
of them regresses. The `#81632b` literal in the home-title gradient is untouched.

**b. `.daily-detail b` — a `--teal` small-text site F-7 never enumerated.**
`--teal` is a 3:1 fill token (chip dots, the `.trait` bullet, this block's
`border-left`), but `.daily-detail b` paints it as **9.92 px uppercase label text**
on `#/` and `#/daily`, directly on the page background. It measures **2.57 light /
2.84 dark** against the ceiling. It is not in F-7's table, not in unit 28's §4 list,
and not in any reviewer's brief — I found it by scoring *every* ink the enumerator
reported, not just the two the routing note named. The block keeps its teal identity
on the `border-left`; the label takes a stop of the same hue that clears
(`#1b4a43` light: 5.22/5.00/4.59 · `#b0dad3` dark: 8.94/5.59/4.51).

**c. `a:hover{color:#fff}` paints white on warm paper — 1.07 in light.**
`a:hover` is dark's hover rule and is global (`styles.css:266`). In light it puts
`#fff` on `--bg` at **1.07:1**. Unit 27 patched this **inside the museum band only**
(`html[data-theme="light"] .mu-hero-body .breadcrumbs a:hover`, `.mu-sub a:hover`,
lines 1272–1273 with a comment naming the problem); every other link on the site
kept it. AC19 covers state pairs, so unit 29 closes it site-wide at the rung the
band already uses: `html[data-theme="light"] a:hover{color:var(--ink)}` (light
`--ink` = 7.85 union / 6.90 ALL). This was not in F-7 either.

---

## 3 — Instruments

All under `evidence/harness/durer-u28/` (unit 28's harness, reused unchanged — no
new instrument was needed, only wider coverage and a derived ceiling alongside).

| | instrument | what it settles | new in u29 |
| --- | --- | --- | --- |
| 1 | `canvastext.py` — three-shot glyph diff | measurement of record: real rendered glyph pixels | run in **all four** theme × viewport cells |
| 2 | `enumerate_overcanvas.py` — cascade enumerator | *which* elements are in the class, exhaustively | run in **all four** cells, before **and** after |
| 3 | `canvasextremes.py` — exact canvas model | the sampled bound | widened to **84 draws/theme**, both viewports |
| 4 | **derived ceiling** (§1) | the bound no draw can beat | **new** — 2⁸ corner enumeration from source |

**Membership is decided by paint differential, never by rect overlap** — the
`.mu-collage` phantom-box lesson is built into instrument 1 rather than remembered
alongside it. Each band takes three shots (A as rendered, B with glyphs
transparent, C with glyphs transparent *and* `#bg-canvas` `display:none`) and an
element counts only if its own glyph pixels change between B and C. The AFTER
tables in §4 carry the differential explicitly: e.g. light `a` at `#/credits` reads
`no-canvas [242,236,223] → [195,201,190]`, a 47-point excursion, so those glyphs are
demonstrably over painted canvas and not over flat paper.

`prefers-reduced-motion: reduce` is emulated so the canvas paints one static frame
at `t=0` and stops. Randomisation is untouched: at `t=0` blob positions are
`(sin(px)·0.5+0.5)·W` with `px` random in `[0,1000]`, so the seed space *is* the
position space and `t=0` draws span the distribution the animation traverses.

### Draws sampled — stated honestly

| run | N |
| --- | --- |
| canvas model (instrument 3), per theme, unioned across 1440 **and** 390 | **84** (24 from u28 @1440 + 30 @1440 + 30 @390) |
| **pixel AFTER, each of the four theme × viewport cells** | **5 draws** × 6 routes × ≤5 scroll bands |
| enumerator BEFORE / AFTER, each of the four cells | 1 pass × 19 routes (static cascade read; scroll- and draw-independent) |
| derived ceiling (instrument 4) | not sampled — 256 corners enumerated exactly |

Each draw is one page load behind a unique query string.

---

## 4 — Measured, before → after

Floor **4.5** (small text). The BEFORE column is the **union-84 model bound**; the
ALL column is the derived ceiling. AFTER is the **pixel instrument** — real
rendered glyphs — with the model figure for the destination ink in brackets.

### Per token × theme (site-wide, whole-surface)

| theme | token | BEFORE union84 | BEFORE ALL | → destination | AFTER union84 | AFTER ALL |
| --- | --- | --- | --- | --- | --- | --- |
| dark | `--faint` | **3.62 FAIL** | **1.82 FAIL** | `--body-ink` | 9.02 | 4.55 |
| light | `--faint` | **2.92 FAIL** | **2.57 FAIL** | `--body-ink` | 5.70 | 5.01 |
| dark | `--muted` | **4.45 FAIL** | **2.24 FAIL** | `--body-ink` | 9.02 | 4.55 |
| light | `--muted` | **4.07 FAIL** | **3.57 FAIL** | `--body-ink` | 5.70 | 5.01 |
| light | `--gold2` | **2.93 FAIL** | **2.58 FAIL** | `#544019` | 5.18 | 4.55 |
| light | `--teal` (`.daily-detail b`) | **2.93 FAIL** | **2.57 FAIL** | `#1b4a43` | 5.22 | 4.59 |
| dark | `--teal` (`.daily-detail b`) | 5.63 pass | **2.84 FAIL** | `#b0dad3` | 8.94 | 4.51 |
| dark | `--gold2` | 8.52 pass | 4.30 — see §7 | unchanged | 8.52 | 4.30 |

### Per theme × viewport — pixel instrument, worst class observed, N = 5 draws each

| viewport | theme | BEFORE (u28 §4, pixel) | AFTER worst class | AFTER | below floor |
| --- | --- | --- | --- | --- | --- |
| 1440×900 | dark | `div.chip-label` **4.39 FAIL** | `p.aw-provenance` | **9.12** | **0 of 28** |
| 1440×900 | light | `div.page-kicker` **3.53 FAIL**, `a` **3.64 FAIL**, `div.chip-label` **3.72 FAIL** | `p.aw-provenance` | **5.65** | **0 of 28** |
| 390×844 | dark | `p.page-lede` **4.47 FAIL** | `a` | **9.37** | **0 of 17** |
| 390×844 | light | `div.chip-label` **3.45 FAIL**, `a` **3.49 FAIL**, `div.page-kicker` **3.77 FAIL**, `a.active` **4.47 FAIL** | `div.page-kicker` | **5.95** | **0 of 17** |

Named selectors from F-7's table, after, pixel-measured:
`div.page-kicker` 6.93 light 1440 / 5.95 light 390 · `a` (global link) 5.85 light
1440 / 6.00 light 390 · `a.active` 7.89 light 390 · `div.chip-label` and
`span.f-label` 7.19 light 390 · `p.page-lede` 6.60 light 1440 / 9.70 dark 390 ·
`.daily-detail b` 6.11 light 1440.

**Unit 27 and unit 28 surfaces re-measured, untouched and still passing:**
`p.img-credit.mu-credit` 6.41 light 1440 / 6.56 light 390 / 11.02 dark 390 ·
`span.img-credit` 6.63 light 1440 / 11.30 dark 1440 · `span.count` 6.46 light 1440
/ 11.52 dark 1440.

### The exhaustive AFTER audit — this is the completeness claim

Every ink painting small text over `#bg-canvas` in **all four** cells, scored
against all three bounds. `PASS` = clears union84, REAL **and** the absolute ALL
ceiling; `pass*` = clears union84 and REAL only.

| theme | ink | token | n | min px | union84 | REAL | ALL | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| light | `[84,64,25]` | `--gold2` new | 142 | 10.4 | 5.18 | 4.96 | 4.55 | PASS |
| light | `[27,74,67]` | teal, `.daily-detail b` | 4 | 9.9 | 5.22 | 5.00 | 4.59 | PASS |
| dark | `[232,201,138]` | `--gold2` | 146 | 10.4 | 8.52 | 5.33 | 4.30 | pass\* |
| light | `[67,60,49]` | `--body-ink` | 2088 | 9.3 | 5.70 | 5.46 | 5.01 | PASS |
| dark | `[176,218,211]` | teal, `.daily-detail b` | 4 | 9.9 | 8.94 | 5.59 | 4.51 | PASS |
| dark | `[216,210,196]` | `--body-ink` | 2086 | 9.3 | 9.02 | 5.64 | 4.55 | PASS |
| dark | `[236,230,217]` | `--ink` | 380 | 12.5 | 10.93 | 6.84 | 5.51 | PASS |
| light | `[43,38,32]` | `--ink` | 382 | 11.5 | 7.85 | 7.52 | 6.90 | PASS |

**Small-text ink groups over `#bg-canvas` below the 4.5 floor: 0 of 8.**
`--faint` and `--muted` no longer appear over this surface in either theme at
either viewport. Enumerator census is stable across the change: 3,753–3,758 text
elements scanned, **1,345 over the canvas**, 19 routes, in each of the four cells —
so the class did not shrink because elements stopped being measured.

**How rows 20–23 were caught.** The first pass of edits left 304 `--muted`
instances per theme still over the canvas on selectors reported only as `a`, `p`,
`span`. Re-running the enumerator and grouping by *ancestor path* named them:
`header.site-header > nav.main-nav > a` (560), `a.era-tile > div.et-label > span`
(32), `div.hero-content > nav.breadcrumbs > span` (8), `div.daily-page-head >
div.daily-sequence > span` (4), `main.view-enter > div.lost > p` (4). They are in
the table above because the audit was re-run to zero, not because the first pass
was complete.

---

## 5 — Validator

```
app.js: syntax OK
artists: 256, movements: 76, techniques: 39, eras: 8, nations: 37, painter styles: 27,
influence edges: 238, venues: 116, catalog: 323 (tier1: 76), daily pool: 75,
museum notes: 104, photo credits: 104 (attribution required: 88),
artwork image credits: 27, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```

`osascript -l JavaScript tools/validate.jxa.js` — **zero warnings**, re-run after
the last edit. Unit 29 is CSS-only and touches no data, so no validator movement was
expected and none occurred.

**Measurement chains:** every chain this pass started was stopped before the pass
ended — `ps` confirms no `canvastext.py`, `canvasextremes.py`,
`enumerate_overcanvas.py`, `theory29b.py` or `--remote-debugging-port` Chrome
remains. Each run took its own CDP port (9471–9504) and its own output tag, and
instrument 1 writes run-unique shot paths, so the unit-27 provenance failure cannot
recur.

---

## 6 — Deviation ledger (Gate 3)

| # | Deviation | Why | Product intent |
| --- | --- | --- | --- |
| D-29-1 | Light `--gold2` went to **`#544019`**, not the routed `#6b5122` | `#6b5122` measures **3.42** against the derived ceiling and 3.89 against the 84-draw model. It is a *large-text* stop from the home-title gradient and was never valid as small text here | Preserved — gold hue held, accents only gain contrast |
| D-29-2 | **26** selectors changed, not the ~12 F-7 described | F-7's list was the subset two instruments had happened to see. The exhaustive audit adds `.main-nav a`, `.era-tile .et-label span`, `.daily-sequence`, `.lost p`, `.daily-detail b`, `a:hover` | Not changed; the class is what it is |
| D-29-3 | `--faint` and `--muted` were **not** re-valued as tokens; their over-canvas call sites were re-pointed instead | Re-valuing them to clear would make them `--body-ink`, deleting two rungs everywhere including inside panels where they measure clear. Scoping the change to the page background keeps the ladder where it is sound | Preserved inside panels; the rule is documented at `#bg-canvas` |
| D-29-4 | `.daily-detail b` took a literal per-theme hex, not a token | One call site; adding a `--teal2` token for it would imply a rung that does not otherwise exist. Mirrors the existing `html[data-theme="light"]` override block | Preserved — the block's teal identity lives on its `border-left` |
| D-29-5 | Light `a:hover` fixed although it is **not** in F-7 | It is a live AA failure at 1.07 in a state AC19 names, and unit 27 had already fixed it band-only with a comment naming the cause. Leaving it would have made §8's closing sentence false | Preserved; uses the rung the band already uses |
| D-29-6 | **Link/body colour separation in light is reduced.** `--gold2` `#81632b` vs `--body-ink` was ~1.95:1; `#544019` vs `--body-ink` is ~1.10:1 | Any ink that clears the canvas floor lands near `--body-ink` — that is forced by §1, not chosen | **Not preserved.** See §7; needs Matisse |
| D-29-7 | Dark `--gold2` left unchanged at ALL-ceiling 4.30 | It clears the 84-draw model at 8.52 and REAL at 5.33; lifting it in dark means moving *toward white*, which deletes the gold | Preserved; disclosed in §7 |

Nothing was escalated for a paid service, new infrastructure, or a legal judgement.

---

## 7 — For the record: what the ceiling means for the palette

This is the durable finding, and it outlives F-7.

**Over `#bg-canvas` — which is roughly a third of all site text, 1,345 of 3,756
elements across 19 routes — only `--body-ink` and `--ink` clear the 4.5 small-text
floor, in either theme.** Every other ink rung fails, most of them badly (`--faint`
1.82 dark, `--muted` 2.24 dark). The atlas therefore has **two** usable small-text
rungs on the page background, not four. The four-rung ladder is real, but it is a
**panel-only** ladder.

Three consequences the project should carry forward:

1. **`--faint` is effectively retired as a page-background ink.** ~~It survives at
   `#search::placeholder`, `.sr-kicker`, `.tl-year`, `.tn-count`, `.tm-lab` and
   `.pp-card-loading` — all inside opaque panels, all still clear on Pass 1.~~ There
   is no room below `--muted` on the page background, and there is no room at
   `--muted` either.

   > **CORRECTION — 2026-07-29, unit 31, re F-8 (Van Eyck, quality review rev 3
   > §R3.3).** The struck sentence above is **false as written, and it was accepted
   > as settled** — Matisse's D-29-6 ruling (`visual-ruling-d29-6.md:267-271`) repeats
   > it. Two errors, and the second is the worse one:
   >
   > **(a) `.tl-year` is not inside an opaque panel.** `.timeline`
   > (`css/styles.css:852-855`) declares `position`, margins, padding and two
   > borders and **no background**, so the era start/end years composite directly
   > onto `#bg-canvas` on all 8 `#/era/*` routes. Van Eyck measured 4.06–4.47
   > against a 4.5 floor on real pixels; unit 31 reproduced it worse still —
   > worst of 4 draws per cell: **3.68** light 390×844, **4.13** light 1440×900,
   > **4.38** dark 1440×900, **4.41** dark 390×844. Fixed in unit 31 by
   > re-pointing `.tl-year` to `--body-ink` (7.04–12.37 after).
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
2. **Any new small text on the page background must take `--body-ink` or `--ink`,
   or be measured against the ceiling first.** The rule and the derivation are now
   in the stylesheet at `#bg-canvas` so the next author meets them before choosing a
   colour, not after review.
3. **Chromatic inks cannot be small text on this surface at all in light.**
   `--gold` 2.30, `--teal` 2.57, `--wine` 3.23, `--blue` 3.20, `--rose` 3.21,
   `--mauve` 3.22 (union-84 figures). They are 3:1 fill tokens here. The two that
   *were* painting glyphs (`--gold2` via `a{}`, `--teal` via `.daily-detail b`) are
   fixed; the rest are fills today and must stay fills.

**And one thing this unit could not settle, which is a design question, not a
measurement one (D-29-6).** Because every clearing ink lands near `--body-ink`,
light links (`#544019`) are now close to body text in lightness — the colour
separation falls from ~1.95:1 to ~1.10:1, and `a{}` sets
`text-decoration:none`. Links remain distinguishable by hue and by hover/focus, but
**not** by the 3:1 luminance technique for WCAG 1.4.1. That technique was already
not met before this unit (1.95 < 3.0), so this is a **worsening of a pre-existing
condition, not a new failure, and it is not an AC19 contrast failure** — AC19's
floors are met. The precedented remedy exists in this repo twice already
(`.img-credit a` and the light hero credit both carry `text-decoration:underline`
with `text-underline-offset:2px`). I did not apply it site-wide because deciding
that every prose link in the light theme gains an underline is visual direction, and
scoping it by selector without Matisse would have been me choosing quietly.
**Recommend: Matisse rules on underlining light prose links.**

---

## 8 — Self-assessment against AC19

**AC19** — *"Both themes pass applicable WCAG 2.2 AA contrast checks for the frozen
text, control, focus-indicator, and state pairs, including composites that require
browser measurement."*

| sub-claim | verdict | evidence |
| --- | --- | --- |
| Text over Wikimedia photographs (F-V1 / F-5) | PASS, carried + re-measured | unit 27 §2; `p.img-credit.mu-credit` 6.41/6.56/11.02 here |
| Focus indicator inside that composite | PASS, carried | unit 27 F-27-3 — untouched |
| Home hero over the generative cover | PASS, carried | unit 26a / Vermeer §5.1 — untouched |
| `.sec-title .count`, `.img-credit` over `#bg-canvas` | PASS, re-measured at all four cells | §4 |
| **`--faint` small text over `#bg-canvas`, site-wide** | **PASS** | §4 — token no longer paints over this surface; 0 of 8 groups below floor |
| **`--gold2` links over `#bg-canvas` in light** | **PASS** | §4 — 5.18 union / 4.55 ceiling; pixel 5.85 / 6.00 |
| **`--muted` small text over `#bg-canvas`** | **PASS** | §4 — token no longer paints over this surface |
| **`--teal` small text over `#bg-canvas`** (new, F-7 did not name it) | **PASS** | §2b, §4 |
| **`a:hover` in light** (new, F-7 did not name it) | **PASS** | §2c — 1.07 → 7.85 |

### The sentence Van Eyck certifies against

**AC19 is now fully supported.** Every text, control and state pair that paints over
`#bg-canvas` clears the 4.5 small-text floor (3.0 large) in **both themes at both
1440×900 and 390×844**, verified two independent ways: the cascade enumerator
reports **0 of 8** small-text ink groups below floor across all four cells, and the
three-shot glyph-diff instrument reports **0 of 28** element classes below floor at
1440 and **0 of 17** at 390, in each theme, over **5 draws per cell**. The claim
does not rest on those draws: the destinations were chosen against a bound
**derived from `js/app.js` by enumerating all 2⁸ corners of the layer cube**, which
no draw can beat, and all of them clear it — the single exception is dark `--gold2`,
which clears the 84-draw model at 8.52 and the REAL ceiling at 5.33 but sits at
**4.30 against the absolute ALL ceiling** (every blob centre *and* all three ribbon
cores coincident on one pixel — a configuration the ribbon geometry makes
unreachable, since bases `.18/.46/.74` with amplitude ≤`.168` keep ribbons 0 and 2
apart). I record that rather than round it up. Units 27's band work and 28's two
call sites are untouched and were re-measured passing here.

One thing is **not** closed and is not an AC19 contrast failure: **D-29-6**, the
light link/body-text colour separation, which falls to ~1.10:1 and needs Matisse's
ruling on underlining prose links (§7).

## 9 — Not tested

1. **Browsers other than Chrome.** Chrome headless only.
2. **Real assistive technology.** Pixels and cascade, not spoken output.
3. **Device pixel ratio ≠ 1, real touch input.** All synthetic at `deviceScaleFactor: 1`.
4. **Viewports other than 1440×900 and 390×844**; the frozen set also names 320 /
   768 / 1280 and 200 % zoom. The derived ceiling is viewport-independent (the
   canvas backing store scales with the viewport and the 84-draw union spans both
   1440 and 390), so the site-wide claim carries; the *pixel* observations do not.
5. **Hover and focus states other than `a:hover`.** `.breadcrumbs a:hover`,
   `.footer-nav a:hover`, `.card-body h3 a:hover` and `.img-credit a:hover` all read
   `--gold2`, which now clears in light (5.18) and already cleared in dark (8.52),
   but they were not separately pixel-measured.
6. **The screenshot pack.** Still at `64d68a0`, now three units behind (Van Eyck's
   N-1 / A10). Unit 29 does not re-capture it; per A10 it should be re-captured
   **once, at final HEAD**, which is now `4362c8a`.

## 10 — Preview

```
git checkout pig-001-stabilization      # at 4362c8a
python3 -m http.server 8421 -d .
open http://localhost:8421/#/credits        # span.count, page-kicker, footer
open http://localhost:8421/#/daily          # .daily-detail b, .daily-kicker
open http://localhost:8421/#/museum/louvre  # unit 27's band, untouched
```
Toggle the theme with the header control. The light theme is where the change reads
most: links, kickers, breadcrumbs and the footer all sit a rung darker.
