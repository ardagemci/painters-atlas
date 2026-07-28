# BROWSER EVIDENCE — PIG-001 (final pass, at shipped HEAD)

**Reviewer:** Vermeer (`claude-browser-reviewer`), Browser Evidence Reviewer
**Date:** 2026-07-28
**Branch:** `pig-001-stabilization` — verified **not** `main`; no push, no merge, no deploy.
**Commit under test:** `c873fe6` (HEAD). I edited no production file. Everything I wrote lives
under `protocol/tasks/PIG-001/evidence/`.

**On the commit that moved under me.** Most of this pass was measured at `a686d98`; Matisse's
D-29-6 ruling (`c873fe6`) landed mid-pass. It changes **no rendered byte**:
`git diff --name-only a686d98..c873fe6 -- css js index.html assets data` returns **nothing** — the
commit adds one document, `evidence/visual-ruling-d29-6.md`. I re-verified after it landed that
the served `/css/styles.css` is byte-identical to the working tree (`curl … | diff -`) and that no
production file is modified. So every measurement and every screenshot below is valid at HEAD, and
I say that from the diff rather than from the assumption.

This pass closes the three items Van Eyck's Gate 2 re-certification (`quality-review.md`) left
against my evidence: **N-4** (my own report shipped with unrendered placeholders), **N-1** (the
screenshot pack is two units behind the code), and **N-5** (units 27–29 have been measured only by
their implementer).

**Everything below is something I observed in a browser at `a686d98`.** Where my number disagrees
with Dürer's, I say so and mine is the one I stand behind. Where I did not observe something, it
is in §6 NOT TESTED and is not inferred.

---

## ENVIRONMENT

| | |
| --- | --- |
| Serve | `python3 -m http.server 8421 -d .` from the repo root |
| Browser | Google Chrome, headless (`--headless=new`), driven over the DevTools Protocol |
| Viewports | `Emulation.setDeviceMetricsOverride` — **never** `--window-size`, which this Mac clamps to a 500 px minimum and which silently produced round 1's defective 390 px captures |
| Cache | `Network.setCacheDisabled=true`; every route loaded as a fresh document behind a unique query string |
| In-page assertions | every capture and measurement asserts `window.innerWidth`, `documentElement.clientWidth`, `#app` padding, `.main-nav` treatment and `documentElement.dataset.theme` **at shutter time**; a run that cannot assert them fails rather than reports |
| Harnesses | new: `harness/vermeer-final/{incidental.py,tagline.py}` · re-run: `harness/cdp-r2/{run_a,run_eg}.py`, `harness/durer-u27/mu.py`, `harness/durer-u28/canvastext.py` |
| Raw data | `harness/vermeer-final/` — `mu-vf-*.json`, `incidental-*.json`, `breadcrumbs.json`, `artist-hero.json`, `tagline-dark-1440.json`, `eg.json`, and the logs `u27-verify.log`, `u29-verify.log`, `incidental.log`, `tagline.log`, `sweep-head.log`, `recapture-head.log` |
| Canvas draws | `prefers-reduced-motion: reduce` emulated so the generative canvas paints one static frame across the shot triple; randomisation untouched, so t=0 draws span the same distribution |

**Verified the served build is the branch under review** before capturing anything: the bytes
served at `/css/styles.css` are byte-identical to the working tree (`curl … | diff -`), the tree
has no modified production file, and the served CSS carries both post-unit-27/29 markers —
`--mu-veil:.88` and light `--gold2:#544019`. This is `a686d98`, not `64d68a0`.

## VIEWPORTS & THEMES COVERED

| Work | Viewports | Themes |
| --- | --- | --- |
| Screenshot pack (N-1) | 1440×900 desktop, 390×844 mobile | dark + light, 16 routes each = 64 |
| Unit 27 museum band (N-5) | 1440×900 **and** 390×844 | dark + light, 15 venues each = 4 cells |
| Unit 29 canvas class (N-5) | 1440×900 **and** 390×844 | dark + light, 7 routes × 5 draws |
| Incidental finds (`.daily-detail b`, light `a:hover`) | 1440×900 **and** 390×844 | dark + light, 9 targets × 3 draws |
| V-F3 artist hero (breadcrumbs + all in-hero text) | 1440×900 **and** 390×844 | light both viewports, dark 1440; 10 artists, rest **and** hover |
| Console / network sweep | 1440×900 | dark, 26 routes |

**Headline:** N-4, N-1 and N-5 are all closed, and my measurements **support** Dürer on units 27
and 29. But this pass found a criterion-failing surface that none of units 26–29 covered —
**V-F3**, the artist hero, §5.3. **AC19 does not hold at HEAD.**

---

# 1 — N-4 · THE PLACEHOLDERS IN MY OWN REPORT · **RESOLVED, 4 of 4**

`browser-evidence-closing.md` shipped in the committed object at `73ddc27` carrying four literal
markers. All four are now rendered **from the raw data that was already on disk**, each under a
dated repair note that says so. No measurement was re-run for this section and no number was
reconstructed from memory.

| marker | section | source it was rendered from | resolved |
| --- | --- | --- | --- |
| `<!--PLACEHOLDER-DARK-->` | §1.2 AC19 dark table | `harness/vermeer-closing/photo-all-dark.json` via that pass's own renderer `table.py` | **yes** |
| `<!--PLACEHOLDER-LIGHT-->` | §1.2 AC19 light table | `harness/vermeer-closing/photo-all-light.json`, same renderer | **yes, with a defect disclosed** |
| `<!--PLACEHOLDER-FINDINGS-->` | §6 findings | that pass's own body + raw data | **yes** |
| `<!--PLACEHOLDER-VERDICT-->` | §9 verdict | that pass's own body + the commit that carried it (`73ddc27`) | **yes** |

`grep -cE '^<!--PLACEHOLDER-[A-Z]+-->$'` on the repaired file returns **0**. The four remaining
textual occurrences are the marker names quoted inside the repair notes.

**§1's AC19 FAIL verdict is cross-referenced, not rewritten.** The repair notes state plainly that
the failure was real on 2026-07-26 and that units 27–29 have since closed it, and point here for
the current measurements. Nothing in §1–§5 of that document was altered.

### FINDING V-F1 · MAJOR · evidence integrity · *found while rendering the light table*

Rendering `photo-all-light.json` surfaced a defect in **that run's instrument** which the
interrupted session never inspected. The light run carries a contamination signature the dark run
does not:

| signature | dark run | light run |
| --- | --- | --- |
| rows reporting a contrast ratio of exactly **1.00** (ink pixel identical to backdrop pixel — impossible for a real glyph on a scrim) | **0** of 1 467 | **33** of 1 461 |
| rows whose glyph-pixel count exceeds 50 000 (larger than any element's glyph area; one `p` reaches **214 760**, roughly the whole viewport) | **0** | **11** |
| venues showing either signature | **0** | **16** of 104 |

Both are what shot-A/shot-B divergence looks like when the two loads do not render the *same*
collage. Excluding the 16 affected venues leaves 88 clean venues and a light picture coherent with
the dark one — worst cells `1.24 / 1.29 / 1.57 / 2.88 / 3.60 / 3.84` rather than a wall of `1.00`.

**Severity is about the record, not about the build.** F-V1 was a failure in both themes on either
reading, and the *class* that failed is identical; the contaminated cells only exaggerated the
magnitude. It is recorded because a certification package must not carry numbers that its own
instrument cannot support, and because the light figures in that table must never be quoted as
measurements of the shipped build. Full statement: `browser-evidence-closing.md` §1.2a.

Two things reduce this to a historical defect. Dürer's unit-27 BEFORE run reproduced the **dark**
figures (`a` 1.33, `span.sep` 1.31, `div.mu-sub` 3.23) to two decimals — the dark run has
cross-operator agreement and is the one F-V1 rests on. And **my four re-runs at HEAD (§3) show
zero rows with either signature**, so the defect is not in the instrument as it stands.

---

# 2 — N-1 · SCREENSHOT PACK RE-CAPTURED AT FINAL HEAD · **DONE, 64 shots**

All 64 shots — 16 routes × {1440×900 desktop, 390×844 mobile} × {dark, light} — re-captured at
`a686d98` and **overwritten in place**. `git status` shows 64 files modified, 0 added: the
`desktop`/`mobile` and `dark`/`light` filename literals are unchanged.

`harness/cdp-r2/run_a.py` asserts at shutter time, per shot: `innerWidth == clientWidth == the
nominal width` (the CDP override, not `--window-size`); `#app` padding `16px`/`22px` at 390 and
`28px`/`34px` at 1440; `.main-nav` `order:3` + `overflow-x:auto` at 390 and `order:0` +
`overflow-x:visible` at 1440; all 8 nav links present and the nav box visible; the theme actually
applied.

**TOTAL 64 · FAILED ASSERTIONS 0** (`capture-assertions.json` regenerated;
`harness/vermeer-final/recapture-head.log`).

**The shot Van Eyck opened is now correct — I checked by eye, not by timestamp.**

| shot | what he found at `64d68a0` | what it shows now at `a686d98` |
| --- | --- | --- |
| `museum-louvre__desktop-1440x900__dark.png` | the **pre-veil** band; breadcrumb washed out over the collage (the F-5/F-V1 failure state) | the veiled band: "Atlas / Museums / Musée du Louvre" fully legible, "Paris · France · founded 1793" legible, the hook and the Share chip clearly separated from the photograph |
| `museum-louvre__mobile-390x844__light.png` | not in his complaint; checked because unit 27 is viewport-dependent | veil present at 390 too; breadcrumb, `h1`, `.mu-sub` and hook all legible over the collage, which is still visible behind them |

Units 28 and 29 are now depicted as well: every route in the pack carries the re-pointed
breadcrumbs, `.page-lede`, `.main-nav a`, `.sec-title .count` and light link colour, because the
pack was captured after `4362c8a`.

### Observation V-O1 · minor · visual direction, not a criterion

On dark desktop the `--mu-veil:.88` band leaves very little of the Louvre collage visible — a
narrow strip at the top of the hero and near-black beneath it. Nothing fails: this is the veil
doing exactly what unit 27 designed it to do, and the criterion is contrast, not photograph
presence. But the hero exists to show the photograph, and how much of it should survive is
Matisse's call, not mine. This is the surface his AC23 record pre-dates (Van Eyck's N-2). Recorded
as an observation with the picture attached, not as a finding.

---

# 3 — N-5 · UNIT 27 (MUSEUM PHOTOGRAPH BAND) INDEPENDENTLY VERIFIED · **SUPPORTS DÜRER**

Re-measured in my own run at HEAD, on **real rendered glyph pixels**, over the adversarial venue
sample (the 15 venues that produced the worst numbers in my closing sweep, including the two I
checked by eye), in **both themes at both viewports** — 4 cells, 15 venues each, **504 in-band
measurements**. Raw: `harness/vermeer-final/mu-vf-{dark,light}-{1440,390}.json`,
log `u27-verify.log`.

## 3.1 His two headline claims

| cell | class | floor | **Dürer** | **mine** | agreement |
| --- | --- | --- | --- | --- | --- |
| dark 1440×900 | `div.mu-sub` | 4.5 | 5.08 | **5.08** | exact |
| light 1440×900 | `div.mu-sub` | 4.5 | 5.30 | **5.31** | +0.01 |
| dark 390×844 | `div.mu-sub` | 4.5 | 5.08 | **5.10** | +0.02 |
| light 390×844 | `div.mu-sub` | 4.5 | 5.25 | **5.25** | exact |
| dark 1440×900 | `h1.display` | 3.0 | 12.29 | **12.29** | exact |
| light 1440×900 | `h1.display` | 3.0 | 10.04 | **10.04** | exact |
| dark 390×844 | `h1.display` | 3.0 | 12.15 | **12.15** | exact |
| light 390×844 | `h1.display` | 3.0 | 9.97 | **9.99** | +0.02 |

**My measurement supports his.** Every cell agrees to within 0.02, and where we differ mine is the
higher — i.e. he reported the more conservative number, which is the honest direction to err.

## 3.2 The whole band, per class, worst of 15 venues

| class | floor | dark 1440 | dark 390 | light 1440 | light 390 |
| --- | --- | --- | --- | --- | --- |
| `span` — breadcrumb, current page | 4.5 | **4.98** | **4.88** | 5.15 | 5.11 |
| `span.sep` — breadcrumb separators | 4.5 | 5.09 | 4.93 | 5.29 | 5.15 |
| `div.mu-sub` — city · country · founded | 4.5 | 5.08 | 5.10 | 5.31 | 5.25 |
| `div.mu-hook` — editorial line | 4.5 | 9.83 | 9.71 | **5.13** | **5.08** |
| `a` — breadcrumb links | 4.5 | 10.03 | 9.90 | 7.29 | 7.17 |
| `h1.display` — venue name | 3.0 | 12.29 | 12.15 | 10.04 | 9.99 |
| `button.chip` — Share this page | 4.5 | 12.17 | 12.36 | 10.54 | 10.54 |

**504 in-band measurements · 0 below floor · 0 below floor anywhere else on those pages either**
(a further 177 elements caught by the same deliberately over-approximate detector). The pre-unit-27
state this replaces bottomed out at **1.01**.

### One refinement of his claim, in my numbers, not a contradiction

He headlines `.mu-sub` as the band's worst class. **In my run it is not.** The worst in-band class
is the breadcrumb's current-page `span`, at **4.88** dark at 390×844 — below his `.mu-sub` figure
in three of four cells. It passes, but the band's true margin over the 4.5 floor is **0.38**, not
the 0.58 his headline implies. In light the tightest class is `div.mu-hook` at **5.08**, which he
does not quote at all.

This changes no verdict — 0 of 504 below floor either way — and it is not a disagreement about the
build. It is a disagreement about which number is the headline, and mine is the smaller one.

### Instrument health

**0 rows with a 1.00 ratio and 0 rows with an implausible glyph-pixel count, in all four cells.**
The contamination signature of V-F1 does not appear anywhere in this pass.


---

# 4 — N-5 · UNIT 29 (CANVAS INK CLASS) INDEPENDENTLY VERIFIED · **SUPPORTS DÜRER, ON THE VALID ROWS**

I did not re-derive his 2⁸-corner bound; my brief was to measure the rendered result. Re-measured
at HEAD on **real glyph pixels** over **7 routes × 5 random canvas draws**, both themes, both
viewports — a route set deliberately overlapping his only in part (`#/`, `#/artists`,
`#/artist/leonardo-da-vinci`, `#/artwork/david`, `#/museum/tate-britain`, `#/lists`, `#/privacy`),
so the sample is independent rather than a repeat. Raw:
`harness/durer-u28/canvas-vf-{dark,light}-{1440,390}.json`, log `harness/vermeer-final/u29-verify.log`.

Membership in the class is decided by a **paint differential** (a glyph is over the canvas iff its
own pixels change when `#bg-canvas` is removed), not by geometry.

| cell | elements over the canvas | classes | **below floor** |
| --- | --- | --- | --- |
| dark 1440×900 | 328 | 23 | **0** |
| dark 390×844 | 412 | 22 | **0** |
| light 1440×900 | 453 | 23 | **0** |
| light 390×844 | 438 | 22 | **0** |

**1 631 measurements over the canvas, 0 below floor.** The re-pointed classes he names all clear
comfortably in my run — worst per cell: `p.page-lede` 10.13 dark 1440, `div.chip-label` 9.16 dark
390, `p.img-credit` 6.54 light 1440, `div.page-kicker` 6.29 light 390. Breadcrumbs (`span.sep`,
`a`), `.footer-note`, `.main-nav a` (`a.active`), `.sec-title .count` (`span.count`) and plain
links are all in the measured set and all pass. **My measurement supports his claim of 0 below
floor.**

### FINDING V-F2 · MAJOR · instrument · *the scrolled rows of this sweep are invalid — in his run and in mine*

The table above is restricted to rows measured at `scrollY == 0`, and it has to be.

`Page.captureScreenshot`'s `clip` is in **page (document) coordinates**, but both
`vermeer-closing/photos.py` and `durer-u28/canvastext.py` pass it rectangles from
`getBoundingClientRect()`, which are **viewport** coordinates. At `scrollY == 0` the two agree.
At any other scroll position the captured pixels are offset by `scrollY`, so glyphs are compared
against whatever happens to sit that far up the document.

I caught this because my run reported one apparent failure — `div.card-tagline` on `#/lists` at
**4.10** against a 4.5 floor, stable to two decimals across all five draws, which is exactly what
a real defect looks like. It is not one. Measured directly, one variable at a time
(`harness/vermeer-final/tagline.py`, `tagline.log`, `tagline-dark-1440.json`):

| clip origin | glyph px | worst | median | top backdrop |
| --- | --- | --- | --- | --- |
| viewport `y` — what both harnesses pass | 1 199 | **4.38** | 5.13 | `[23,39,50]` |
| viewport `y` + `scrollY` — the correct page origin | 5 328 | **6.02** | 6.02 | `[22,20,15]` = `--panel` |

`[22,20,15]` is exactly dark `--panel` `#16140f`, and 6.02 is exactly `--muted` on `--panel`.
At every unscrolled position the same class measures a flat 6.02 dark / 7.19 light.
**The failure was my instrument, not the build. I withdraw it.** The card was independently
confirmed opaque (`background rgb(22,20,15)`, `opacity 1`, no overlap with its art) and not
mid-animation (effective opacity 1.000 held at 0.5 s, 1.5 s, 3 s and 6 s after scrolling).

**Impact on the record.** Re-analysed by scroll position, the affected share is:

| run | rows over the canvas | at `scrollY == 0` | **scrolled (invalid)** |
| --- | --- | --- | --- |
| mine, 4 cells | 1 782 | 1 631 (85–97 %) | **151** |
| Dürer's unit-29 pixel run, 4 cells | 1 679 | 1 590 (93–97 %) | **89** |

Restricted to valid rows, **his four cells also show 0 below floor** — so his conclusion survives;
what does not survive is the claim that the sweep covered the scrolled bands. Those rows are
neither a pass nor a fail: they are **NOT TESTED**, in both runs, and they are listed as such in
§6. Nothing in §3 is affected — the museum-band runs measure at scroll 0 only.

---

# 5 — N-5 · DÜRER'S TWO INCIDENTAL FINDS, AND WHAT THEY LED TO

Neither is reachable through `canvastext.py`, which never hovers anything, so I built a separate
instrument: `harness/vermeer-final/incidental.py`. It hovers with a real
`Input.dispatchMouseEvent` and **asserts that the computed colour actually changed** before it
measures — a hover that did not take is reported as such rather than silently measured at rest.
Raw: `incidental-*.json`, log `incidental.log`. 4 cells, 9 targets, 3 draws.

## 5.1 `.daily-detail b` — **fixed, confirmed**

| theme | Dürer, before | **my measurement at HEAD** | floor | verdict |
| --- | --- | --- | --- | --- |
| light | 2.57 | **6.40** | 4.5 | **PASS** |
| dark | — | **11.50** | 4.5 | **PASS** |

## 5.2 Light `a:hover` — **fixed, confirmed; no white ink survives anywhere I looked**

Dürer's 1.07 was `a:hover{color:#fff}` painting white on warm paper. Under a real pointer at HEAD I
measured **no `#fff` ink on any light-theme link on any route tested**. The hover ink resolves to
`--ink` `[43,38,32]` or to a `--gold2` variant, and every cell passes:

| route | hovered ink | worst | floor | verdict |
| --- | --- | --- | --- | --- |
| `#/artists` `.main-nav a` | `--ink` `[43,38,32]` | 12.42 | 4.5 | **PASS** |
| `#/credits` `main a` (390) | `--ink` `[43,38,32]` | 11.05 | 4.5 | **PASS** |
| `#/lists` `.card-body h3 a` | `--gold2` `[84,64,25]` | 9.16 | 4.5 | **PASS** |
| `#/museum/louvre` `.breadcrumbs a` | in-band gold `[107,81,34]` | 5.28 | 4.5 | **PASS** |

**Both of his incidental finds are closed, and my measurement supports him on both.**

## 5.3 What the hover probe found instead — **FINDING V-F3**

# FINDING V-F3 · MAJOR · criterion-failing · AC19 · the artist hero fails in both themes, at rest

The hover probe returned one cell far below floor: `#/artist/leonardo-da-vinci` `.breadcrumbs a`,
**2.77** light. I chased it rather than reporting the hover number, and it is much larger than a
hover defect.

### It fails at rest, and at rest it is worse

`harness/vermeer-final/breadcrumbs.json` — 72 measurements, 5 routes, rest **and** hover:

| theme · viewport | state | worst | floor | verdict |
| --- | --- | --- | --- | --- |
| light 1440×900 | **rest** | **2.01** | 4.5 | **FAIL** |
| light 1440×900 | hover | 2.77 | 4.5 | **FAIL** |
| light 390×844 | **rest** | **2.16** | 4.5 | **FAIL** |
| light 390×844 | hover | 2.98 | 4.5 | **FAIL** |

**This is not a hover-only defect.** Hover is the *better* of the two states, because unit 29's
`html[data-theme="light"] a:hover{color:var(--ink)}` darkens the ink. Van Eyck is ruling on an
at-rest failure.

### Which selector actually wins (`CSS.getMatchedStylesForNode`, observed, not reasoned from the cascade)

| state | winning declaration | computed |
| --- | --- | --- |
| rest | `.hero-content .breadcrumbs a{color:var(--body-ink)}` — `styles.css:542` | `rgb(67,60,49)` = light `--body-ink` `#433c31` |
| hover | `html[data-theme="light"] a:hover{color:var(--ink)}` — `styles.css:256` (unit 29) | `rgb(43,38,32)` = light `--ink` `#2b2620` |

Unit 29's light hover rule **beats** `.breadcrumbs a:hover{color:var(--gold2)}` (`:438`) here — I
report that as measured, from the matched-rule list and the computed value, and did not try to
talk myself into it from specificity arithmetic.

### Which backdrop layer (one variable at a time, `#/artist/caravaggio`, light)

| layers present | worst | backdrop |
| --- | --- | --- |
| as shipped | **1.42** | `[86,83,79]` |
| **in-hero cover canvas removed** | **8.51** | `[233,227,214]` |
| in-hero cover **and** `#bg-canvas` removed | 9.23 | `[241,236,223]` |
| only `#bg-canvas` removed, cover restored | **1.42** | `[86,83,79]` |

**The failing layer is the in-hero cover canvas at `opacity:1` — a different layer from
`#bg-canvas`.** Removing `#bg-canvas` changes nothing; removing the cover fixes it outright. So
**unit 29's derived `#bg-canvas` ceiling does not bound this surface**, and F-7's closure does not
reach it.

### Scope: it is the artist hero, it is most artists, and it is both themes

10 artists × all in-hero text, at scroll 0 (`harness/vermeer-final/artist-hero.json`):

| cell | measurements | **below floor** | artists affected | worst |
| --- | --- | --- | --- | --- |
| light 1440×900 | 104 | **59 (57 %)** | **8 of 10** | `a` **1.42** (caravaggio) |
| light 390×844 | 104 | **68 (65 %)** | **9 of 10** | `span.sep` **1.66** (frida-kahlo) |
| dark 1440×900 | 104 | **20 (19 %)** | **4 of 10** | `a` **1.68** (claude-monet) |

Per class, worst across the sample:

| element | px | floor | light 1440 | light 390 | dark 1440 |
| --- | --- | --- | --- | --- | --- |
| `.breadcrumbs a` | 12.5 | 4.5 | **1.42** | **1.78** | **1.68** |
| `.breadcrumbs .sep` | 12.5 | 4.5 | **1.48** | **1.66** | **1.68** |
| breadcrumb current `span` | 12.5 | 4.5 | **1.48** | **1.80** | **1.68** |
| **`h1` — the painter's name** | 57.6 / 30.4 | **3.0** | **2.40** | **2.82** | **2.35** |
| `.hero-tagline` | 17.9 | 4.5 | 5.38 | 4.66 | 6.49 |

**The painter's name itself misses its large-text floor** — 2.40 light, 2.35 dark. Only
`claude-monet` is clean in light (a pale cover), and it is the *worst* artist in dark, which is the
signature of an unbounded surface rather than a bad palette choice: the cover is generated per
painter, so which artists fail is a lottery.

### Root cause — the same mechanism as F-V1, on the one hero that was never fixed

`.hero .hero-shade` (`styles.css:536`) carries a **hardcoded** ramp keyed to hero height:
`rgba(bg,.18) 0% → rgba(bg,.42) 52% → rgba(bg,.93) 100%`. `.hero` is
`min-height:330px; align-items:flex-end`, so `.hero-content` is **bottom-anchored** and the
breadcrumb row — its first line — lands around 55–70 % of the hero, where the ramp delivers only
**.43–.61**. Derived from the shipped tokens, the alpha a text block actually needs against a
worst-case opaque cover pixel is **≥ .690 dark and ≥ .710 light** (`--gold2` in `.hero-sub a` is
the binding ink; `--body-ink` needs .676/.677, `h1` .505/.454).

This is precisely the defect I reported as F-V1 for the museum band: *a scrim that ramps by
container height under a text block whose position varies*. Unit 26a fixed the home hero with
`--hero-veil` (.80/.86). Unit 27 fixed the museum band with `--mu-veil:.88` on the text block.
**`.hero .hero-shade` — artist and artwork heroes — received neither and still uses the pre-unit-26
geometry.** Its `--hero-veil` tokens exist and are applied only at `.home-hero .hero-shade:817`.

There is an irony worth recording because it explains how this survived 29 units: unit 27's own
comment at `styles.css:1286` justifies the museum band's ink by saying the crumbs "take the rung
**the artist hero already takes over its cover** (`.hero-content .breadcrumbs`)". The artist hero
was used as the reference for correctness. It had never been measured, and it fails.

### The fix (specified, not implemented — Dürer's call)

Put a fixed-alpha veil on the **text block**, as units 26a and 27 already established, instead of
ramping by hero height:

```css
.hero-content{
  background:linear-gradient(180deg, rgba(var(--bg-rgb),.74), rgba(var(--bg-rgb),.80));
}
```

`.74` clears the derived requirement in both themes (`.690` dark / `.710` light) with margin, and
is a **bound** against a worst-case opaque cover pixel rather than a sample — the standard Matisse
set at unit 26 and Dürer met at unit 27. `.hero .hero-shade` can then be *reduced*, so the cover
keeps more of itself than the present `.93`-at-the-bottom ramp already leaves it.

Two things the fix must not do. It must not be validated on one painter: the cover is generated
per artist and the failing set is a lottery — `claude-monet` passes in light and is the worst case
in dark. And it must not be assumed to carry `#/artwork/*`: those breadcrumbs are **outside** the
hero (`inHero=false`, measured 9.25 light / 11.60 dark) and are not part of this finding, but the
artwork *hero* uses the same `.hero .hero-shade` and was not separately measured here (§6).

Whatever is chosen, re-measure with `harness/vermeer-final/` across the artist sample, both
themes, both viewports.

---

# 6 — REGRESSION SWEEP AT HEAD (console / network / images)

Re-run at HEAD so the regression evidence matches the shipped code
(`harness/cdp-r2/run_eg.py`, output `harness/vermeer-final/{eg.json,sweep-head.log}`; all 26 frozen
routes walked inside one document, as a real user moves through the SPA, so observers and the
Resource Timing buffer survive).

| measure | result |
| --- | --- |
| routes walked | **26 / 26** reached |
| console **errors** (`console.error`, `onerror`, `unhandledrejection`) | **0** |
| console **warnings** | **0** |
| CDP `Log.entryAdded` / `Runtime.exceptionThrown` at error or warning severity | **0** |
| network requests with status ≥ 400 | **0** of 107 |
| third-party hosts | **`upload.wikimedia.org` only** (69 requests), plus `localhost:8421` (38). **0** to `fonts.googleapis.com` / `fonts.gstatic.com` |
| images checked | **680** · **broken: 0** |
| route orientation (AC15 spot-check) | live regions: **0**; live mutations across 5 route changes: **0**; `document.activeElement` after each = the route's `h1[tabindex="-1"]` |
| image credit lines | `#/museum/louvre` → *"Photograph: Benh LIEU SONG (Flickr) · CC BY-SA 3.0 · file on Commons"*; `#/artwork/david` → *"Image credit: Jörg Bittner Unna · CC BY 3.0 · file on Commons"*; no raw-markup leakage |

**No regression at HEAD.** Consistent with AC25's disclosure position: fonts are self-hosted and
`upload.wikimedia.org` is the only third-party host, disclosed on `#/privacy`.

---

# 7 — NOT TESTED

Explicit, and not inferred from anything.

1. **The scrolled bands of the canvas sweep — in my run and in Dürer's.** 151 of my rows and 89 of
   his were captured at `scrollY > 0` and are invalid for the reason in **V-F2**. They are not a
   pass and not a fail. Whoever re-runs the canvas class must fix the clip origin first, or
   measure only at scroll 0 and say so.
2. **`#/artwork/*` heroes.** The artwork *breadcrumbs* sit outside the hero and were measured
   (9.25 light / 11.60 dark, PASS). The artwork **hero interior** uses the same `.hero .hero-shade`
   as the artist hero and was **not** measured. V-F3's mechanism is not viewport- or
   route-specific, so I expect it there too — but I did not observe it and I am not claiming it.
3. **Artists beyond the 10 sampled for V-F3.** 256 exist; I measured 10 at three cells. The rate
   (8 of 10 light, 4 of 10 dark) is a sample, not a census.
4. **Dark 390×844 for V-F3.** The artist-hero sweep ran light at both viewports and dark at 1440
   only. Dark already fails at 1440, so this changes no verdict, but the dark mobile rate is
   unmeasured.
5. **Real assistive-technology output.** No VoiceOver, NVDA or JAWS session. I measured the
   accessibility tree, not what a screen reader speaks.
6. **Real touch input and device-pixel-ratio ≠ 1.** All input was synthetic mouse and key events at
   `deviceScaleFactor: 1`.
7. **Browsers other than Chrome.** Chrome headless only — `-webkit-mask-image` on `.main-nav` and
   `backdrop-filter` are where that gap could matter.
8. **The 821–1100 px overflow band (Van Eyck F-1)** and **the masked focus indicator (F-2).** Not
   re-measured by me; outside this brief. Both stand as recorded.
9. **Deployed identity.** Everything was measured against a local `http.server`. No GitHub Pages
   URL was fetched; nothing here proves what a deployed build serves.
10. **AC4 and AC8 were not re-exercised at this HEAD.** They were established at `64d68a0`
    (`browser-evidence-closing.md` §2–§3); units 27–29 are CSS-only and touch neither, but I did
    not re-walk them.

---

# 8 — VERDICT

| item I was sent to close | answer |
| --- | --- |
| **N-4** — the four placeholders | **CLOSED.** 4 of 4 rendered from raw data; 0 live markers remain. One instrument defect disclosed in the process (**V-F1**) |
| **N-1** — screenshot pack at final HEAD | **CLOSED.** 64 shots, 0 failed assertions; the shot Van Eyck opened now shows the veiled band |
| **N-5** — units 27–29 verified by someone other than the implementer | **CLOSED for 27 and 29.** My measurements **support** both. Unit 28's fixes are inside the classes I re-measured and also pass |

**But AC19 does not hold at HEAD.** Not because unit 27 or unit 29 failed — both do what their
authors claim, and I confirmed it in my own instrument — but because **V-F3** is a surface none of
them covered: the artist hero's own cover canvas, failing in both themes, at rest, on 8 of 10
sampled painters in light and 4 of 10 in dark, with the painter's name below its large-text floor.

The pattern is now three for three. The home hero (unit 26a), the museum band (unit 27) and the
artist hero (open) are the same defect: **a scrim that ramps by container height under a
bottom-anchored text block.** Two were fixed one at a time, by finding them. I would not certify
AC19 on a fourth surface being absent until someone enumerates the scrims rather than the failures
— `.hero .hero-shade` is the one I found; `grep -n 'hero-shade\|shade\|scrim' css/styles.css` is
where I would start, and the artwork hero (§7 #2) is the first place I would look.

