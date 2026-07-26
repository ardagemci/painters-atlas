# PIG-001 — Unit 26 build log (Vermeer round-2 findings V2-1 … V2-4)

**Implementer:** Dürer (`claude-implementation-lead`) · branch `pig-001-stabilization`
(verified: not `main`) · Gate 1 satisfied (`specification.md` at `approved_for_build`).

Unit 26 closes the four findings raised by Vermeer's round-2 re-verification
(`evidence/browser-evidence-build-r2.md`). Every number below was measured by me
in a real browser at this commit, not inherited. Where a number is derived from
the cascade rather than observed under a real render, it says so.

## Commits

| Group | Commit | Finding | Files |
| --- | --- | --- | --- |
| 26a | `09c344b` | V2-1 (P1, AC19) + V2-2 (P2) | `css/styles.css`, `index.html` |
| 26b | `a5cf379` | V2-4 (P2, AC18) | `css/styles.css`, `index.html` |
| 26c | `525af26` | V2-2/V2-3 (P2, AC19) | `css/styles.css`, `index.html` |
| 26d | — | record only, no code | this log |

`?v=` bumped once per commit: `20260726-pig001-u26a` → `u26b` → `u26c`.
`js/app.js` was **not** touched in unit 26; its `?v=` is unchanged.

## Environment

| | |
| --- | --- |
| Serve | `python3 -m http.server 8421 -d .` (repo root) |
| Browser | Google Chrome, headless, driven over the DevTools Protocol |
| Cache | `Network.setCacheDisabled=true`; every route loaded as a fresh document behind a unique query string |
| Viewport | `Emulation.setDeviceMetricsOverride` (not `--window-size`, which this Mac clamps to 500 px) |
| Harness | `evidence/harness/durer-u26/hero.py`, `nav.py`, built on Vermeer's `harness/cdp-r2/cdp.py` + `png.py`; raw results in `harness/durer-u26/*.json` |

---

## 26a — V2-1 · dark home hero over the generative cover · AC19 · P1

### Root cause, re-confirmed before fixing

Vermeer's diagnosis is correct and I reproduced it in the DOM rather than
accepting it. Canvas inventory taken in the live page at 1440×900 and 390×844,
both themes:

| canvas | `getComputedStyle().opacity` | inside `.home-hero` | box |
| --- | --- | --- | --- |
| `#bg-canvas` | **.5 dark / .6 light** | **no** | full viewport (1440×900 / 390×844) |
| *unnamed* | **1** | **yes** | 1182×438 / 356×450 — box-identical to the hero |

The unnamed canvas is emitted by `canvasTag(muse.style, muse.palette, muse.id, …, true, salt)`
at `js/app.js:1630`. It is the layer the hero title paints over. `#bg-canvas` is a
fixed page backdrop *outside* `.home-hero` and never sits behind the hero text.

Two consequences, both confirmed by measurement:

1. Matisse's published bound and unit 25d's arithmetic (`k = .6 × (1 − .72) = .168`,
   worst backdrop `rgb(201,196,186)`, title 3.23) were computed against
   `#bg-canvas`. The real blend factor is `1 − veil`, and light's real
   worst-case bound as shipped by 25d was **2.86, i.e. below its 3.0 floor** —
   not 3.23. Vermeer's observed 3.06 was luck of the draw, not a guarantee.
2. Unit 25d scoped both its scrim and its ink lift to `html[data-theme="light"]`,
   so dark kept `rgba(var(--bg-rgb),.25)` at the ellipse centre over a
   full-opacity cover. Measured worst scrim alpha over the dark title: **.35**.

### Method

Vermeer's glyph-pixel technique, reused unchanged: two screenshots per load, one
with the hero text painted and one with it hidden; a pixel counts only where the
two differ by more than 60 (sum of channel deltas), which confines the sample to
where a glyph actually lands. Ink = the declared paint (the four gradient stops
for the `background-clip:text` title, computed colour otherwise); backdrop = that
same pixel with the text hidden.

Added to it, and the reason the fix can be called a bound rather than a sample:
a second pass **forces the in-hero cover canvas to a fully opaque worst-case
pixel** — white in dark (where the ink is light) and black in light (where the
ink is dark) — and measures the same glyph pixels against that. This is Matisse's
"bound against a worst-case cover pixel, not against one sampled cover", executed
on the real compositor instead of modelled. It is the inverse-case rule he set
for light, applied to dark.

### Fix

- `.home-hero .hero-shade` rebuilt **once**, one geometry for both themes, alphas
  supplied per theme by two new tokens `--hero-veil` / `--hero-veil-edge`:
  `radial-gradient(ellipse 100% 100% at 50% 50%, veil 0%, veil 62%, edge 100%)`.
  Radii of 100 % of the box put the whole of `.home-hero-content` inside the
  plateau at every viewport measured (worst normalised radius **.58 at 390 px**,
  **.49 at 1440 px**); the corners reach r = .707 and take ~23 % of the way to
  the edge alpha, so the cover still reads at the rounded frame.
  25d's light-only `.hero-shade` override is deleted — its `.38` stop at 84 %
  cut across the lower text at 390 px, where the credit sat at an effective alpha
  of roughly .47.
- `--hero-veil` **.80 dark** (was .25 at the ellipse centre), **.86 light**
  (was .84 falling to .74 at 62 %).
- `.home-hero-content .footer-note{color:var(--body-ink)}` is now **unscoped**,
  i.e. the cover credit takes the body rung in both themes. `--faint` needs an
  effective alpha of ≈ .93 to reach 4.5:1 against a worst-case cover, which would
  erase the cover entirely — the same argument Matisse made for light.
- Nothing else re-pointed. Dark's kicker keeps `--gold2` and dark's credit link
  keeps `a{}`'s `--gold2`; both clear 4.5 under the new veil. The light-only
  `.kicker → --ink` and `.footer-note a → --body-ink` rules from 25d are kept
  unchanged, so the light fix is not weakened.

### Measured — worst observed on real glyph pixels

10 fresh covers per theme (4 + 3 at 1440×900, 3 at 390×844). "before" is my own
baseline run at `a4898d3`, and it reproduces Vermeer's numbers.

| theme | element | floor | before | **after (worst of 10)** | verdict |
| --- | --- | --- | --- | --- | --- |
| dark | `h1.home-title` | 3.0 | **1.08** | **4.84** | PASS |
| dark | `div.kicker` | 4.5 | 4.35 | **7.11** | PASS |
| dark | `p.lede` | 4.5 | **1.88** | **7.53** | PASS |
| dark | `p.footer-note` (cover credit) | 4.5 | **1.58** | **8.38** | PASS |
| dark | `a` (painter link in the credit) | 4.5 | 4.02 | **7.91** | PASS |
| light | `h1.home-title` | 3.0 | 3.13 | **3.67** | PASS |
| light | `div.kicker` | 4.5 | 8.15 | **9.87** | PASS |
| light | `p.lede` | 4.5 | 5.76 | **6.66** | PASS |
| light | `p.footer-note` | 4.5 | 5.52 | **7.17** | PASS |
| light | `a` | 4.5 | 5.60 | **7.17** | PASS |

### Measured — the bound, forced worst-case opaque cover pixel

Identical at 1440×900 and 390×844, which is the plateau doing its job.

| theme | element | floor | before (bound) | **after (bound)** | verdict |
| --- | --- | --- | --- | --- | --- |
| dark | `h1.home-title` | 3.0 | **1.00** | **4.62** | PASS |
| dark | `div.kicker` | 4.5 | **3.06** | **6.80** | PASS |
| dark | `p.lede` | 4.5 | **1.47** | **7.20** | PASS |
| dark | `p.footer-note` | 4.5 | **1.31** | **7.20** | PASS |
| dark | `a` | 4.5 | **3.10** | **6.80** | PASS |
| light | `h1.home-title` | 3.0 | **2.86 (FAIL)** | **3.42** | PASS |
| light | `div.kicker` | 4.5 | 7.42 | **9.18** | PASS |
| light | `p.lede` | 4.5 | 5.33 | **6.66** | PASS |
| light | `p.footer-note` | 4.5 | 5.03 | **6.66** | PASS |
| light | `a` | 4.5 | 5.03 | **6.66** | PASS |

**V2-2 is closed in the same change.** Light's title margin over 3.0 moves from
**−0.14 to +0.42 on the bound** and from 0.06 to **0.67 on observed covers**. The
criterion is now met for covers nobody has drawn yet, which is what V2-2 asked
for — the honest statement Vermeer could not make about 3.06 can now be made
about 3.42, because the number comes from a forced worst case rather than a draw.

### Character cost, and the deviation it forces

The generative cover is now veiled behind the hero text in the **dark** theme
too. Matisse accepted the light veil partly on the grounds that "dark is the
default theme and is untouched"; that is no longer true. This is a **material
deviation from directed visual direction (Gate 3)**, forced by V2-1 at P1: the
dark title's darkest gradient stop is `--gold` `#c9a45c`, and no veil below ≈ .69
holds it at 3.0:1 against an opaque bright cover pixel. The alternative —
lightening the dark hero gradient the way Matisse darkened the light one — would
have let the veil drop to ≈ .58, but it rewrites the shipped look of the default
theme's hero on my own authority rather than his, so I did not take it.
**Recommend Matisse re-adjudicate the dark hero veil**; the value is a single
token (`--hero-veil`) and re-tuning it is a one-line change, provided the bound
in the block comment is re-verified with the same forced-cover run.

---

## 26b — V2-4 · the 390 px nav · AC18 · P2 · regression from unit 25e

### Root cause, re-confirmed

Reproduced at `a4898d3` before touching anything, 390×844, both themes:
`.site-header` **362 px** (43 % of the viewport), `.main-nav` box **97 × 291**,
**8 rows**, computed `flex-basis: 0%`, `flex-wrap: wrap`, 6 of 8 links inside the
box, `nav.scrollWidth/clientWidth` 109/97. Vermeer's mechanism is exactly right:
`.main-nav{flex:1}` resolves to `flex-basis:0%`, flex-basis beats the `width:100%`
the ≤ 820 px rule sets, so the box computes 97 px — and 25e's `flex-wrap:wrap`
then had 97 px to wrap eight destinations into.

### Fix

Scoped to the `@media (max-width:820px)` block only, so the desktop wrap AC18
needs at 200 % zoom is untouched:

```
.main-nav{order:3;flex:0 0 100%;width:100%;flex-wrap:nowrap; overflow-x:auto; …mask…}
```

`flex-basis:100%` makes the authored `width:100%` effective; `flex-wrap:nowrap`
restores the single row behind the unit-2 `-webkit-mask-image` affordance.

### Measured (390×844, dark and light identical)

| measure | before | **after** |
| --- | --- | --- |
| `.site-header` height | **362 px** (43 % of 844) | **154 px** (18 %) |
| `.main-nav` box | 97 × 291 | **358 × 35** |
| rows of links | 8 | **1** |
| computed `flex-basis` | `0%` | **`100%`** |
| computed `flex-wrap` | `wrap` | **`nowrap`** |
| computed `overflow-x` | `auto` | `auto` |
| nav `scrollWidth` / `clientWidth` | 109 / 97 | **689 / 358** (scrollable) |
| mask-image | present, fading a vertical stack | present, **fading a horizontal scroll** |
| links visible in the box | 6 of 8, stacked | **4 of 8, in one row** |
| `documentElement` sw / cw | 390 / 390 | 390 / 390 |

### No regression at ≥ 821 px — re-measured, not assumed

200 % text zoom (root font-size forced to 32 px, re-applied twice to survive the
router's re-paint), all 26 routes, at both widths round 2 used:

| | round 2 @1270 | **unit 26 @1270** | round 2 @1280 | **unit 26 @1280** |
| --- | --- | --- | --- | --- |
| routes measured | 26 | **26** | 25 | **26** |
| routes overflowing | 0 | **0** | 0 | **0** |
| `documentElement` sw / cw | 1270 / 1270 | **1270 / 1270** | 1280 / 1280 | **1280 / 1280** |
| `nav.main-nav` box | 493 × 258 | **493 × 258** | 503 × 192 | **503 × 192** |

Breakpoint sweep at 100 % zoom (`#/`, both sides of the 820 px boundary):

| width | header | nav box | rows | wrap | basis | doc sw / cw |
| --- | --- | --- | --- | --- | --- | --- |
| 320 | 154 | 288 × 35 | 1 | nowrap | 100% | 320 / 320 |
| 390 | 154 | 358 × 35 | 1 | nowrap | 100% | 390 / 390 |
| 768 | 108 | 736 × 35 | 1 | nowrap | 100% | 768 / 768 |
| 820 | 108 | 788 × 35 | 1 | nowrap | 100% | 820 / 820 |
| 821 | 239 | 224 × 210 | 5 | wrap | 0% | 971 / 821 † |
| 1280 | 110 | 649 × 81 | 2 | wrap | 0% | 1280 / 1280 |
| 1440 | 68 | 809 × 39 | 1 | wrap | 0% | 1440 / 1440 |

† see the pre-existing finding recorded at the end of this log — it is not the nav.

### Recorded deviation

Vermeer's pre-25 baseline was a **109 px** header and unit 26's brief asked for
"~109 px". It is **154 px**, and that is deliberate. The 109 px figure came from
the nav being crammed into the 97 px left over beside the search field *on the
same row*, with **1 of 8 links visible**. Restoring `flex-basis` gives the nav
its own full-width row — which is what `width:100%` in that rule was written to
do, and what the mask affordance was designed for — at a cost of 45 px of sticky
header. Both states were measured in the same page by toggling only the two
declarations, so the comparison isolates the choice:

| | literal pre-25 restore (`flex:1 1 0%`, `nowrap`) | **shipped (`flex:0 0 100%`, `nowrap`)** |
| --- | --- | --- |
| `.site-header` | **109 px** | 154 px |
| `.main-nav` box | 97 × 35, sharing row 2 with the search field | **358 × 35, its own row** |
| links visible | 1 of 8 | **4 of 8** |

Reverting to the literal 109 px is a one-line change (drop `flex:0 0 100%`, keep
`flex-wrap:nowrap`). Flagged for the reviewer rather than decided silently.
Relevant context: "mobile-nav discoverability" is already on the known-defect
register, and a 97 px scroll window is its proximate cause.

---

## 26c — V2-2/V2-3 · gold-as-small-text · AC19 · P2

### The sweep

Every `var(--gold)` reference in `css/styles.css` and `js/app.js` was read and
classified. **51 references** (49 in `css/styles.css`, 2 in `js/app.js`):

| class | count | what it means |
| --- | --- | --- |
| **fill** | **22** | area / shape / graphic stroke, or a gold ground carrying `#171307` ink (`::selection`, `.btn:hover`, `.aw-btn.on`, `.f-btn.on`, `.sec-title::before`, `.entry-card::before`, `.tl-dot`, `.tm-you`, `.tree-link`, the two `js/app.js` legend `<i>` swatches, …) |
| **UI** | **21** | border, outline, focus indicator, hairline rule, underline colour — 1.4.11, 3:1 floor (`.skip-link`, `.skip-inline`, `#search:focus`, `#theme-toggle:hover`, `.btn`, `.chip.m:hover`, `.tl2-leg.on`, `.tone.on`, …) |
| **large text** | **2** | ≥ 24 px, or ≥ 18.66 px bold — 3.0 floor, `--gold` clears it: the dark home-hero `h1` gradient stop (59.2 px / 800) and `.mu-essay ::first-letter` (≈ 55 px / 600) |
| **small text** | **6** | 4.5 floor — `--gold` does **not** clear it. All six re-pointed to `--gold2`. |

`js/app.js` needed no edit: its only two `--gold` uses are the timeline and
influence-graph legend `<i>` swatches, 10 px fills redundant with their own
adjacent text labels. Its other two hits are `--ec:var(--gold2)`, already correct.

### The six re-pointings, measured in the live DOM, both themes

| selector | size / weight | route measured | light before | **light after** | **dark after** |
| --- | --- | --- | --- | --- | --- |
| `.list-card .lc-kicker` | 10.2 px / 300 | `#/lists`, `#/list/…` | 3.71 | **5.18** | **11.53** |
| `.le-num` | 19.2 px / 300 | `#/list/…` | 3.40 | **4.75** | **12.25** |
| `.tl2-leg-more` | 12.2 px / 300 | `#/timeline` | 3.40 | **4.75** | **12.25** |
| `.tl2-year.now` ("today") | 11.2 px / 300 | `#/timeline` | 3.71 | **5.18** | **11.53** |
| `.pc-kind` | 9.9 px / 300 | `#/taste` (see caveat) | 3.71 | **5.18** | **11.53** |
| `.branch-chip::before` "↳" | 11.2 px | `#/movements` (38 instances) | 3.71 | **5.18** | **11.53** |

Ink after: light `#81632b` = `rgb(129,99,43)`, dark `#e8c98a` = `rgb(232,201,138)`,
measured against the real composited surface behind each element.

**Two of the six are new** and were not in Vermeer's round-2 walk:

- `.pc-kind` only renders once a persona has been proposed or adopted, which the
  route walk never reached.
- `.branch-chip::before` is a pseudo-element, and a computed-style walk over
  *elements* cannot see it. The "↳" is an ornament redundant with the chip's own
  label, so it could be argued as non-text at a 3:1 floor; re-pointed anyway
  rather than left as a judgement call.

**Caveat, stated rather than hidden:** `.pc-kind` was read from the cascade with
the element injected into `#/taste` in the live document, because the route
cannot reach a persona card without completing the palette flow. It is
cascade-derived, not observed in the real flow. Everything else in the table was
read off a real render.

### The invariant is now written down

A comment at the light `--gold` declaration states the rule — `--gold` is a 3:1
token: fills, rules, borders, focus indicators and large text only; every
glyph-painting use below 24 px (or below 18.66 px bold) takes `--gold2` — and
records the audit counts, so a seventh site is a visible rule violation rather
than an oversight.

---

## 26d — the two withdrawn round-1 findings, examined and closed

No code change. Recorded so the register shows these were disposed of, not
forgotten.

| round-1 finding | round-2 disposition | status |
| --- | --- | --- |
| `div.mu-hero` "loses 942 px at 200 % zoom" on `#/museum/louvre` | **WITHDRAWN by Vermeer.** The overflow is six decorative collage `<img>` tiles and **zero text** (`textsOutside = 0` of 6 text-bearing elements on both museum routes), and it is **larger unzoomed than zoomed** — 982 px at 100 % vs 942 px at 200 %. A quantity that shrinks when you zoom is not a zoom defect; it is the border-radius mask over the bleeding collage. Vermeer states the earlier decision to decline this was correct, while noting the specific claim "measured lostW/lostH = 0" was not reproducible (the number is 942/982). | **CLOSED — no action** |
| `button.skip-inline` "109 px clipped" on `#/influences` | **WITHDRAWN by Vermeer.** The reading was taken **unfocused**, where `.skip-inline` is a deliberate 1 px visually-hidden control (`styles.css:328`) — a clip measurement there is meaningless. **Focused** it is `492 × 49`, `lostW/lostH = 0`, fully inside the viewport, `rgb(232,201,138)` on `rgb(29,26,19)`. F-6 (unthemed control) is separately resolved: the tokens are on its base rule. | **CLOSED — no action** |

---

## Validator

`osascript -l JavaScript tools/validate.jxa.js` run after **each** of the three
commits, and at HEAD:

```
app.js: syntax OK
artists: 256, movements: 76, techniques: 39, eras: 8, nations: 37, painter styles: 27,
influence edges: 238, venues: 116, catalog: 323 (tier1: 76), daily pool: 75,
museum notes: 104, photo credits: 104 (attribution required: 88),
artwork image credits: 27, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```

**Zero warnings, as before unit 26.**

## Regression sweep at HEAD

26 routes visited in one document with `console.error` / `console.warn` /
`onerror` / `unhandledrejection` instrumented in-page:

| measure | result |
| --- | --- |
| console errors | **0** |
| console warnings | **0** |
| broken images | **0** of **690** checked across the 26 routes |
| routes reached | 26 / 26 |

## Deviation ledger (Gate 3)

| # | Deviation | Why forced | Effect | Disposition |
| --- | --- | --- | --- | --- |
| D-1 | The **dark** hero cover is now veiled (`--hero-veil` .25 → .80). Matisse's direction said dark was untouched and would stay at 6.20. | V2-1 (P1): dark measured 1.10 / 1.97 / 1.74. The bound Matisse's "dark untouched" rested on was computed against `#bg-canvas`, a layer that is not behind the hero. No veil below ≈ .69 holds the darkest title stop at 3.0:1 against an opaque bright cover pixel. | The default theme's hero cover is dimmed behind the text block; it still reads at the rounded frame. | **Escalate to Matisse** to re-adjudicate. One token, re-tunable in one line if the bound is re-verified. |
| D-2 | The **light** veil moved .84/.74 → a flat .86, and 25d's shaped light-only `.hero-shade` was deleted in favour of one shared geometry. | The 25d gradient's `.38` stop at 84 % cut across the lower hero text at 390 px, and light's real bound was 2.86, below its floor. | Light's cover is slightly more veiled at the lower text; title bound −0.14 → +0.42 over floor. | Accept — this is the "cheap way to widen the light margin" the brief invited, and it closes V2-2. |
| D-3 | The 390 px header lands at **154 px**, not the ~109 px the brief named. | The 109 px baseline was produced by a 97 px nav sharing a row with the search field, showing 1 of 8 links. Honouring `flex-basis` is what makes the rule's own `width:100%` effective. | +45 px of sticky header; 4 of 8 links visible instead of 1. | **Flag for reviewer.** One-line revert available; both states measured above. |
| D-4 | `.pc-kind` and `.branch-chip::before` re-pointed although neither is in V2-3. | Same defect class; the brief asked for a sweep so it "does not come back a third time". | Two more small-text sites clear AA. | Accept. |
| D-5 | `.branch-chip::before` "↳" is classified as small text although it is an ornament redundant with its label. | Ambiguous under 1.4.3 vs 1.4.11; re-pointing costs one lightness step. | None visible. | Accept, recorded as a judgement call. |

## New observation — NOT a unit-26 regression, and NOT fixed here

While sweeping breakpoints for 26b I found a **pre-existing horizontal overflow
on `#/` at intermediate desktop widths**, at 100 % zoom, which no previous round
measured (round 1 swept 320 / 390 / 768 / 1280 / 1440; round 2 swept 390 / 1440
and 1270 / 1280 at zoom — the 821–1100 band was never in the set):

| width | `documentElement` sw / cw | overflow | first overflowing element |
| --- | --- | --- | --- |
| 821 | 971 / 821 | **+150 px** | `a.daily-media`, 520 px wide, right edge 971 |
| 900 | 1013 / 900 | **+113 px** | `a.daily-media`, right edge 1013 |
| 980 | 1055 / 980 | **+75 px** | `a.daily-media`, right edge 1055 |
| 1000 | 1066 / 1000 | **+66 px** | `a.daily-media`, right edge 1066 |

`#/artists` is clean (0 overflowing elements) at all four widths, so this is the
"Painting of the Day" media block on the home route, not the nav and not the
header. `git diff a4898d3..HEAD -- css/styles.css` does not touch `.daily-media`
or its grid, so it predates unit 26.

I have **not** fixed it: it is outside the four findings this unit was scoped to,
and a fifth unreviewed layout change inside a stabilization task is the wrong
trade. **It is an open AC18 item and should be triaged before Gate 2.**

## Self-assessment against the acceptance criteria

**AC18 — responsive layout, no horizontal overflow, containment at 200 % zoom**

- 200 % text zoom: **PASS**, 0 px overflow on 26/26 routes at 1270 and at 1280.
  Unit 25e's result is intact; 26b did not regress it.
- 390 px mobile header composition: **PASS**, and V2-4 is closed — 362 px → 154 px,
  one scrolling row, mask affordance restored, `flex-basis` honoured.
- 100 % zoom overflow at 320 / 390 / 768 / 820 / 1280 / 1440: **PASS**, sw == cw.
- **Not clean:** the 821–1100 band on `#/` overflows by 66–150 px through
  `a.daily-media`. Pre-existing, newly observed, unfixed, recorded above. I do
  **not** claim AC18 fully passes while that is open.

**AC19 — contrast**

- Hero over the generative cover, **both themes**: **PASS**, on 10 fresh covers
  per theme *and* against a forced worst-case opaque cover pixel. Worst bound:
  title 4.62 dark / 3.42 light (floor 3.0); every small-text element ≥ 6.66
  (floor 4.5). V2-1 and V2-2 closed.
- `--gold` as small text: **PASS**, all six sites re-pointed, worst measured 4.75
  in light and 11.53 in dark, both above the 4.5 floor. V2-3 closed, plus two
  sites nobody had found.
- **Not claimed:** text over `upload.wikimedia.org` artwork photographs is still
  unmeasured (Vermeer's NOT TESTED #4 — those canvases are cross-origin-tainted).
  The forced-cover technique in `harness/durer-u26/hero.py` would reach them via
  the screenshot diff; it was not run against them in unit 26.

**Not certified by me.** Gate 2 is Van Eyck's, and the browser re-verification of
this unit is Vermeer's. This log is the implementer's evidence, not a pass mark.
