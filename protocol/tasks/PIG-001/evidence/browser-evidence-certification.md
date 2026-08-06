# BROWSER EVIDENCE — PIG-001 · certification pass

**Agent:** Vermeer (`claude-browser-reviewer`).
**Branch:** `pig-001-stabilization` · **HEAD:** `09f61a8` (verified before capture;
never `main`, nothing pushed).
**Production code under review:** complete at `4266804` (unit 36). `09f61a8` is
that unit's build log and touches no production file.

**Environment:** headless Google Chrome driven over the Chrome DevTools Protocol
by a pure-stdlib client (`harness/cdp-r2/cdp.py`). Served from my own
`python3 -m http.server 8433 -d .` (PID 10589). **The owner's server on port 8422
(PID 93806) was never contacted and is still running.**

**Served build asserted to be HEAD before any measurement**, by four independent
markers rather than by trusting the checkout:

| marker | unit | observed over HTTP |
| --- | --- | --- |
| `?v=20260805-pig001-u36` on both `css/styles.css` and `js/app.js` | 36 | present |
| `<div id="live-status" …>` at `index.html:80` | 33 | present |
| `stroke-width:.46em` on the graph-label halo | 33 (follow-up 2) | present |
| `.daily-media` carries no `min-height` | 33 (F-1) | confirmed absent |
| `"…carry Commons' public-domain assertion…"` | 36 | present |
| `const pos = (n === 1 \|\| n % 4 === 0)` | 34 | present at line 3256 |

---

## 0 — WHAT THIS PASS IS, AND WHAT IT IS NOT

This is the final evidence pass. Its job is to give the independent Quality
Reviewer something to certify **against**, which means the one thing it must not
do is re-report the implementer's own numbers back to him.

Unit 33 measured unit 33. That is not an accusation — his instrument is sound and
imports my own primitives — but "all six majors closed, 0 sites below floor in
twelve cells" is a self-assessment until somebody else's instrument says it too.
So every contrast figure below was produced by my harness, from my own site
table, against the shipped build. **Where my number differs from Dürer's, mine is
stated and his is named, and I say which is lower.**

Three things in this document are **carried forward, not re-observed**, and are
labelled at each use:

1. **The owner's VoiceOver session-3 ear-confirmations** (six of seven AT
   findings). I cannot reproduce them and I do not contradict them. No instrument
   here can hear anything; where I report on the live region I report presence
   and mutation behaviour only.
2. **Behavioural / journey results unaffected by units 33, 34 and 36** — routing,
   passport merge semantics, storage, interaction flows. Unit 34 is speech-only
   and unit 36 changed text inside two existing `<p>` elements; neither can move
   those results. Unit 33 did move geometry, which is why the zoom matrix *is*
   re-run below rather than carried.
3. **Unit 32's and unit 33's own NOT TESTED lists**, restated in §7 where they
   remain open. I did not close them and do not claim to.

---

## 1 — FINDING 1 · the six contrast majors, independently remeasured

**Method.** The four-shot paint differential from my own `vermeer-u32/sitecensus.py`:
**A** the page as rendered · **B** the target selector's ink forced transparent by
an injected rule · **C** B plus `#bg-canvas` removed · **D** B plus every cover
canvas hidden. A glyph pixel is where A and B differ strongly; its **backdrop is
B — the surface as actually composited, measured, never read from the
stylesheet.** Ink is never hidden with `visibility:hidden` (that would delete the
element's own background). `prefers-reduced-motion: reduce` is emulated so
`#bg-canvas` paints one static frame per load, and the theme, `innerWidth` and
reduced-motion state are asserted **on every page load**, not once per run.

Hover is forced through CDP `CSS.forcePseudoState`, so the **engine** is asked for
the state rather than the state being simulated with a synthetic mouse event.

**Scale.** 12 cells — 320 / 390 / 900 / 1024 / 1280 / 1440 × light and dark.
**2 626 measured glyph rows.** N = 3 draws at the two frozen viewports, N = 2 at
the four intermediate widths.

### 1.1 The matrix — worst observed contrast per site, per cell

`-` means *not measured in that cell*, not *passed*. Floor is 4.5 (no measured
site qualified as large text).

| site | theme | 320 | 390 | 900 | 1024 | 1280 | 1440 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `.ig-node text` | light | 7.14 | 7.14 | 7.14 | 7.14 | 7.13 | 7.14 |
| `.ig-node text` | dark | 6.02 | 6.02 | 6.02 | 6.02 | **6.02** | **6.02** |
| `#ig-svg.focused .ig-node.lit text` | light | – | 13.86 | – | – | – | 13.86 |
| `#ig-svg.focused .ig-node.lit text` | dark | – | 14.80 | – | – | – | 14.80 |
| `button.chip:hover` | light | – | 10.30 | – | – | – | 10.95 |
| `button.chip:hover` | dark | – | 16.42 | – | – | – | 14.99 |
| `.le-meta` | light | 6.92 | **6.26** | 7.27 | 6.90 | 6.88 | 6.99 |
| `.le-meta` | dark | 10.55 | 10.16 | 11.19 | 11.71 | 10.48 | 10.88 |
| `.tl2-year` | light | 5.17 | 5.17 | 5.17 | 5.17 | 5.13 | 5.13 |
| `.tl2-year` | dark | 4.90 | 4.90 | 4.90 | 4.90 | 4.90 | 4.90 |
| `.tl2-year.now` | light | 9.16 | 9.16 | 9.16 | 9.16 | 9.16 | 9.16 |
| `.tl2-year.now` | dark | 11.53 | 11.53 | 11.53 | 11.53 | 11.53 | 11.53 |
| `.sr-group` | light | 4.62 | **4.62** | 4.62 | 4.62 | 4.62 | 4.62 |
| `.sr-group` | dark | 4.62 | **4.62** | 4.62 | 4.62 | 4.62 | 4.62 |
| `.gonext-item:hover b` | light | – | 13.89 | – | – | – | – |
| `.gonext-item:hover b` | dark | – | 18.40 | – | – | – | – |
| `#search::placeholder` | light | – | 5.17 | – | – | – | 5.17 |
| `#search::placeholder` | dark | – | 4.90 | – | – | – | 4.90 |
| `.sr-meta` *(control)* | light | 6.42 | 6.42 | 6.42 | 6.42 | 6.42 | 6.42 |
| `.sr-meta` *(control)* | dark | 5.68 | 5.68 | 5.68 | 5.68 | 5.68 | 5.68 |
| `.md-name` | light | 5.56 | 5.81 | 6.38 | 6.38 | 6.38 | 6.38 |
| `.md-name` | dark | 4.99 | 5.24 | 5.68 | 5.68 | 5.68 | 5.68 |

**0 of 2 626 measured rows fall below floor, in every one of the twelve cells.**
Worst value anywhere in my matrix is **4.62** (`.sr-group`, both themes, all six
widths) — the same worst value unit 33 reports.

### 1.2 My numbers against Dürer's — including where we differ

| site | Dürer (unit 33) | **Vermeer (this pass)** | verdict |
| --- | --- | --- | --- |
| `.ig-node text` | 6.02 dark · 6.58–7.14 light | 6.02 dark (all 6 widths) · **7.13–7.14** light | agree; my light **floor is higher** than his (7.13 vs 6.58) |
| `#ig-svg.focused .ig-node.lit text` | 13.86 light · 14.80 dark | **13.86 · 14.80** | **exact** |
| `button.chip:hover` | 9.43 light · 14.38 dark | **10.30–10.95** light · **14.99–16.42** dark | agree; mine **higher** in both themes |
| `.le-meta` | 6.50 light · 9.86 dark | **6.26** light@390 · **10.16–11.71** dark | agree on verdict; **my light figure is LOWER than his** — see below |
| `.tl2-year` | 5.13 light · 4.90 dark | **5.13–5.17** light · **4.90** dark | **exact** |
| `.tl2-year.now` | (folded into V32-5/6) | 9.16 light · 11.53 dark | measured separately here |
| `.sr-group` | 4.62 both themes, every width | **4.62** both themes, every width | **exact** |
| `.gonext-item:hover b` | 13.89 light · 18.40 dark | **13.89 · 18.40** | **exact** |
| `#search::placeholder` | 5.17 light · 4.90 dark | **5.17 · 4.90** | **exact** |
| `.sr-meta` (control) | 6.42 light · 5.68 dark | **6.42 · 5.68** | **exact** |
| `.md-name` | 5.56–6.38 light · 4.99–5.68 dark | **5.56–6.38 · 4.99–5.68** | **exact** |

**Where we disagree, and saying it plainly:** on `.le-meta` in light my worst is
**6.26**, against his published **6.50**. **Mine is the lower number and mine
wins.** It does not change the verdict — 6.26 clears the 4.5 floor comfortably —
but the published figure is 0.24 optimistic and the record should carry mine. The
difference is a sampling one: my worst light `.le-meta` pixel occurs at **390 px**,
and `.le-meta` sits directly on `#bg-canvas` (`canvasDelta` 21–37 across cells),
which is `Math.random`-seeded, so the narrow-viewport draw finds a slightly
darker corner of the generative backdrop than his did.

On `button.chip:hover` and on the light floor of `.ig-node text` my numbers are
**higher** than his. I flag these as disagreements too, in the same breath, so
the direction of the drift is not mistaken for a pattern: two of my three
deviations favour the build and one does not.

**The dark 1280/1440 cell specifically.** Unit 33's most interesting finding was
that `.ig-node text` passed everywhere *except* dark at 1280 and 1440, at 4.42
against the floor, and that widening the halo `.34em → .46em` took it to 6.02.
Those are exactly the two cells most worth an independent look. **I measure 6.02
in both, with the measured backdrop resolving to `--panel`** — his attribution
reproduces.

### 1.3 Coverage honesty inside this finding

Not every site was measured in every cell, and the table's `-` cells are real:

- `button.chip:hover`, `#ig-svg.focused .ig-node.lit text` and
  `#search::placeholder` were measured at **390 and 1440 only** (both themes,
  N = 3). The four intermediate widths ran the width-sensitive selectors only.
- `.gonext-item:hover b` was measured at **390 only, both themes**. At 1440 it
  never sat 90 % inside the viewport, so my visibility gate discarded it rather
  than measuring a partly-offscreen glyph. **At 1440 this selector is NOT
  TESTED by me** — Dürer's 13.89 is his figure there, not mine.
- `.ig-node text` recorded an isolated "selector matched nothing" on single draws
  in two cells (the force-directed graph had not laid out at the moment of the
  query). It was measured successfully on other draws in **every** cell, so no
  cell rests on a missing measurement.

---

## 2 — FINDING 2 · the 200 % text-zoom matrix, and F-1

### 2.1 F-1 — closed, confirmed independently

`min-height:390px` on a box carrying `aspect-ratio:4/3` transfers through the
ratio into a 520 px minimum **width**, and `body{overflow-x:hidden}` then hid the
symptom by clipping rather than scrolling. Because of that clipping, document
scroll width alone is **not** a sufficient probe — so I measure both it and every
`#app` element whose border box crosses the viewport's right edge, excluding
anything inside a deliberately scrollable ancestor. A width is clean only when
both are zero.

`#/`, both themes, eight widths:

| width | 320 | 390 | **821** | **900** | **1024** | **1100** | 1280 | 1440 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| before (unit 33's record, light) | 0 | 0 | **150** | **113** | **54** | **18** | 0 | 0 |
| **after — light (measured here)** | 0 | 0 | **0** | **0** | **0** | **0** | 0 | 0 |
| **after — dark (measured here)** | 0 | 0 | **0** | **0** | **0** | **0** | 0 | 0 |

Zero crossing elements and zero document overflow at every width in both themes.
**F-1 is closed, and confirmed by an instrument that is not the one that fixed
it.**

### 2.2 200 % text zoom — re-run, and the route count corrected

Unit 33 changed geometry on `.skip-link`, `.tl2-year`, `.daily-media` and the map
labels, so the earlier matrix was stale. Re-run at `documentElement.fontSize =
200%` (asserted to compute to `32px` on every route before the probe is read),
viewport 1280×800, **both themes**.

**Result: 26 router cases × 2 themes — 0 routes with document overflow, 0 with a
crossing element, 0 with a clipped box.** The four selectors unit 33 moved were
reported per route for attribution; none contributed overflow in any cell.

**A correction to the inherited figure, which is a finding in its own right.**
The frozen "26/26 zero overflow" result came from `cdp-r2/run_d.py`, whose route
discovery walks list, museum, artist, movement, technique, era and nation — **but
not artwork**. That harness therefore covered **25** routes, and
`#/artwork/<id>` — one of the image-heaviest views in the build — **was never
zoom-tested at all**. I measured it separately (`gapfill.py`): `#/artwork/david`
and `#/artwork/the-starry-night`, both themes, at 200 % — **0 overflow, 0
crossing, 0 clipped**. With that case included the sweep genuinely covers 26
router cases. The old number was right by luck, not by coverage.

---

## 3 — FINDING 3 · the screenshot pack, recaptured at HEAD

**64 PNGs** — 16 routes × {1440×900 desktop, 390×844 mobile} × {dark, light} —
all captured against `09f61a8`. Filenames keep `desktop`/`mobile` and
`dark`/`light` literal for the kernel's quality gate:
`<route>__desktop-1440x900__<theme>.png` / `<route>__mobile-390x844__<theme>.png`.

Routes: `home`, `artists`, `artist-leonardo`, `artwork-david`, `explore`,
`timeline`, `influences`, `museums`, `museum-louvre`, `lists`, `palette`,
`taste`, `daily`, `privacy`, `credits`, `invalid-route`.

**Mobile is a real 390 px render, not a cropped 500 px one.** Headless Chrome on
this Mac clamps window width to a 500 px minimum — my own earlier finding — so
every viewport is set through `Emulation.setDeviceMetricsOverride`, which is not
subject to the clamp, and **`window.innerWidth` is asserted in the page at
shutter time** together with the theme. Per-capture assertions (innerWidth,
innerHeight, theme, hash, image count, broken-image count, byte size) are
recorded in `harness/vermeer-cert/capture-assertions-{light,dark}-{390,1440}.json`.
**0 broken images across all 64 captures.**

**`#/credits` is included and its new copy is asserted, not assumed.** A
screenshot is only evidence of unit 36's rewrite if the rewrite was on the page
when the shutter fired, so the rendered `#app` text was checked in both themes:
the new lede (*"…carry Commons' public-domain assertion…"*) **present**, the old
lede **absent**, the new attributed phrasing (*"old enough that Commons files
them as public domain"*) **present**, the old flat assertion **absent**. Both
themes, 13 064 characters each.

### 3.1 An instrument failure I caught, and what it means for the pack

Recording this because it nearly put sixteen worthless files into the evidence
directory under correct-looking names.

The first dark-desktop run returned **sixteen byte-identical 43 124-byte PNGs**
with `document.images.length === 0` on every route — blank frames. The theme and
`innerWidth` assertions *passed*, because the inline theme script runs before
`app.js`; the app simply never rendered in that one browser instance, which was
one of four competing for a single-threaded local server. **The same routes
rendered correctly in dark at 390 and in light at 1440 in the same batch, so this
was my harness under contention and not a product defect.** Re-run alone, the
dark-desktop set produced 16 correctly varied captures and the blank files were
overwritten. Verified afterwards: zero 43 124-byte files remain, and all 64 pack
files carry fresh timestamps.

The general lesson, which applies to the rest of this document: **an assertion
that the viewport and theme are right is not an assertion that the page
rendered.** Byte-size variance across routes is what caught it.

---

## 4 — FINDING 4a · the `.md-name` residual, measured and characterised

Unit 33 records "roughly 3 px at 320 px width" as an unfixed **legibility**
residual, distinct from the contrast question it did close. Measured properly:
`getComputedStyle` reports **2.07 px**, but that is in **SVG user units** and is
not what a reader sees — the viewBox transform scales it. So rendered size is
computed as `userUnits × getScreenCTM().a` and cross-checked against the measured
client rect.

| viewport width | CTM scale | **rendered font-size** | glyph box height |
| --- | --- | --- | --- |
| **320** | 1.129 | **2.34 px** | **3 px** |
| **390** | 1.435 | **2.97 px** | **4 px** |
| 900 | 3.561 | 7.37 px | 9 px |
| 1024 | 4.104 | 8.49 px | 10 px |
| 1280 | 5.049 | 10.45 px | 13 px |
| 1440 | 5.049 | 10.45 px | 13 px |

Identical in both themes. 22 labels in every cell.

**Characterisation — three things that bound how bad this is:**

1. **Unit 33's estimate is confirmed and slightly refined.** 2.34 px rendered /
   3 px glyph box at 320. At the **frozen mobile viewport of 390 it is 2.97 px /
   4 px** — still far below any practical reading size, and 390 is a viewport
   this project actually certifies against, which 320 is not.
2. **The label only exists in the europe-zoom state.** With the map at its
   default world view, `.md-name` matches **zero elements** at every width I
   tested. The residual is reachable only after the reader opts into that zoom,
   which materially narrows its blast radius.
3. **It is not an information loss for assistive technology.** Each dot keeps its
   own `<title>` as its accessible name (unit 33 moved the labels into a trailing
   `<g class="md-labels">` with `pointer-events:none` precisely so that no
   semantics or hit target were lost). The text is illegible to a sighted reader
   at narrow widths; it is not missing from the accessibility tree.
4. **Scale caps at 1280.** 1280 and 1440 are identical (5.049), so the label
   never gets larger than 10.45 px however wide the viewport.

**Severity: MINOR.** Contrast passes at every width (§1, 4.99–6.38). WCAG has no
minimum-font-size success criterion, so this is not a conformance failure — it is
a legibility defect, and at 2.34–2.97 px it is a real one for anyone using the
europe zoom on a phone. Unit 33's proposed remedy (make the europe-zoom label
size a floor rather than a pure function of `mag`) is sound and is **not applied
in this build**. Recorded as open, not closed.

---

## 5 — FINDING 4b · the live region

**What I can see, and what I cannot.** A live region is a promise to a screen
reader. I can verify the promise is well-formed and that it is not being broken
in the DOM; I **cannot** verify anything is spoken. Nothing in this section
speaks to audibility, and nothing here contradicts the owner's ear.

**Identity and placement** — `#/`, light, 1440:

| property | observed |
| --- | --- |
| present | **yes** |
| **outside `#app`** | **yes** — its parent is `body` |
| `role` | `status` |
| `aria-live` | `polite` |
| `aria-atomic` | `true` |
| class | `sr-only` (`display:block`, `visibility:visible` — visually hidden, **not** removed from the tree) |
| text at rest | empty |
| **other live regions in the document** | **none — `#live-status` is the only one** |

That last row is the load-bearing one for the C-8 regression question. The defect
unit 25f removed was a live region *wrapping the whole page* that fired on every
route change, so the page was announced twice and the two channels disagreed.
**There is exactly one live region in this document and it is the new one.** The
old one has not come back.

**Mutation behaviour on ordinary route changes.** A `MutationObserver`
(`childList` + `characterData` + `attributes`, `subtree:true`) was installed on
the region, then twelve ordinary route changes were driven through `location.hash`:

`#/artists`, `#/timeline`, `#/influences`, `#/museums`, `#/lists`, `#/palette`,
`#/explore`, `#/credits`, `#/privacy`, `#/artist/leonardo-da-vinci`,
`#/no-such-page`, `#/`

**Result: 0 mutations on every one of the twelve; the region's text was empty
after each.** `route()` does not write to it of its own accord.

**The positive control, which is why the negative result counts.** "The observer
recorded nothing" is worthless if the observer was never working — that failure
mode is indistinguishable from a pass. So the run ends on a path that *should*
write to the region: open the search panel, then Escape. **Observed: panel
confirmed open, then 1 mutation, region text
`"Search results closed. You are back in the search field."`** The observer was
live throughout, so the twelve silences are real silences.

**Verdict: the live region is present, correctly placed outside `#app`, correctly
attributed, is the only one in the document, is silent on ordinary route changes,
and demonstrably does fire when it should.** The double-announcement defect has
**not** returned.

**Carried forward, not re-observed:** the owner confirmed by ear in VoiceOver
session 3 that AT-1, AT-2, AT-3, AT-4, AT-6 and AT-7 are fixed, and that AT-5
(arrows) was **still not fixed** at that time. Unit 34 subsequently fixed the
`.branch-chip::before` glyph that unit 33's JS-side fix structurally could not
reach. **AT-5 remains unconfirmed by ear** — unit 34 says so itself, and I cannot
close it. My instrument can only report that the glyph is out of the
accessibility tree, which unit 34 already established.

---

## 6 — FINDING 5 · the 26-route console / network sweep

Re-run so the regression evidence matches shipped code. Events are taken from the
protocol (`Runtime.consoleAPICalled`, `Runtime.exceptionThrown`, `Log.entryAdded`,
`Network.loadingFailed`, `Network.responseReceived`), not scraped from the page,
and every route is a fresh full navigation with the cache disabled so one route's
failures cannot be blamed on another.

**26 router cases, light theme, 1440×900:**

| measure | result |
| --- | --- |
| routes with console errors | **0** |
| routes with warnings | **0** |
| routes with failed requests | **0** |
| routes with HTTP ≥ 400 | **0** |
| routes with broken images | **0** |
| **hosts contacted** | `localhost` (954 requests) · **`upload.wikimedia.org` (69)** |
| **font / CDN providers contacted** | **0** |

The external-origin expectation on record is met exactly: `upload.wikimedia.org`
only, and **zero** font or CDN providers. This matters beyond tidiness —
`#/privacy` tells the reader there are no font providers, so a hit here would
make a shipped page untruthful, not merely untidy.

**A first run that I am reporting and discarding, with the reason.** My initial
sweep ran concurrently with two other browser instances against my single local
server and reported, on `#/` only, three network errors
(`ERR_SOCKET_NOT_CONNECTED`, `ERR_CONNECTION_RESET`) and two
"preloaded but not used" warnings for the self-hosted `inter` and
`playfair-display` woff2 files. Re-run with nothing else contending, **`#/` is
clean on all five measures** and the warnings do not reappear. The first result
was my own load, not the product's. I record it because a reader of the JSON will
otherwise find `sweep-light.json` disagreeing with `log-sweep-light-clean.txt`
and deserve to know which is which — **the clean run is the evidence.**

---

## 7 — PERIMETER

Stated as a first-class output. This is what I covered, and it is not everything.

### 7.1 Covered — measured in this pass, at HEAD

| dimension | covered |
| --- | --- |
| **Contrast — cells** | 12: light and dark × 320 / 390 / 900 / 1024 / 1280 / 1440 |
| **Contrast — draws** | N = 3 at 390 and 1440; N = 2 at 320 / 900 / 1024 / 1280 |
| **Contrast — rows** | 2 626 measured glyph rows, 0 below floor |
| **Contrast — selectors** | `.ig-node text`, `#ig-svg.focused .ig-node.lit text`, `button.chip:hover`, `.le-meta`, `.tl2-year`, `.tl2-year.now`, `.sr-group`, `.sr-meta`, `.gonext-item:hover b`, `#search::placeholder`, `.md-name` |
| **States exercised** | search panel open (typed query), influence graph focused (node clicked), map europe-zoom, `:hover` forced via `CSS.forcePseudoState`, seeded populated passport |
| **F-1** | `#/`, 8 widths (320–1440 incl. 821/900/1024/1100), both themes |
| **200 % zoom** | 26 router cases × both themes at 1280, incl. the artwork case the old harness missed |
| **Screenshots** | 16 routes × 2 viewports × 2 themes = 64, all asserted in-page |
| **Console / network** | 26 router cases, light, fresh navigation each |
| **Live region** | identity, placement, sole-region check, 12 route changes, 1 positive control |
| **`.md-name` legibility** | 6 widths light, 3 widths dark, zoomed and unzoomed |

### 7.2 Not covered — explicitly

- **Engines other than Chrome.** No Safari, Firefox or WebKit measurement of any
  kind. This matters more than usual here: **every ear-confirmation in this
  project was obtained in Safari + VoiceOver, and my instrument cannot reach that
  combination at all.**
- **`deviceScaleFactor ≠ 1`.** All measurement at 1×. Retina/HiDPI antialiasing
  is a different pixel population and halo-based fixes (`.ig-node text`,
  `.md-name`) are exactly the kind that could behave differently there.
- **The deployed origin.** Everything here is `localhost:8433`.
- **Dark-theme console/network sweep.** Light only (§6). Canvas painting differs
  by theme; console and network behaviour is not expected to, but I did not
  measure it and do not claim it.
- **200 % zoom at viewports other than 1280**, and zoom in combination with the
  390 mobile viewport.
- **`button.chip:hover`, the focused-graph state and `#search::placeholder` at
  320 / 900 / 1024 / 1280** — measured at 390 and 1440 only.
- **`.gonext-item:hover b` at 1440** — discarded by my 90 %-in-viewport gate;
  measured at 390 only.
- **Second and later ids for parameterised routes.** One id per family
  (`leonardo-da-vinci`, `david`, `louvre`, `impressionism`, `oil-painting`,
  `16th-century`, `italy`, `paintings-that-still-scare-us`), plus a second
  artwork id at 200 % zoom only.
- **Onboarding deck interaction, passport import/merge/cancel journeys, and the
  taste loop.** Not re-exercised in this pass. Unit 33 changed their announcement
  behaviour and unit 34 changed the deck's spoken cadence; **the DOM assertions
  for both are Dürer's, not mine, and the confirmations are the owner's ear.**
- **Focus-ring contrast (WCAG 1.4.11).** A glyph differential cannot see a ring —
  the ring is not a glyph. Unmeasured here, as in unit 32.
- **`.branch-chip::before` and `.tone.on::after`.** Neither unit 32, unit 33 nor
  this pass rendered and measured them. Unit 34 changed the accessible-name
  handling of the first; its *painted contrast* remains unmeasured.
- **Colour-emoji glyphs**, and the pseudo-element perimeter derived from reading
  the stylesheet rather than from the DOM.
- **The pre-rendered SEO pages under `p/artwork/*.html`.** Outside the SPA, not
  linked from it, not swept, and carrying a known bare `→` that unit 34
  deliberately did not fix.
- **Anything spoken.** No audibility claim appears anywhere in this document.

### 7.3 Carried forward — labelled, with the reason

| carried | from | why not re-observed |
| --- | --- | --- |
| Six of seven AT findings confirmed fixed **by ear** (AT-1, 2, 3, 4, 6, 7) | owner, VoiceOver session 3 | I have no screen reader and no Safari. Not reproducible by any instrument I have; not contradicted. |
| AT-5 still open by ear as of session 3; unit 34's `.branch-chip` fix unheard | owner + unit 34 | Same reason. Unit 34 does not claim it closed either. |
| Deck cadence 1/4/8/12/16 | unit 34 | Speech-only change; verified by Dürer against the served file. No rendered pixel moves, so my pack and contrast evidence are unaffected by it. |
| Routing, storage, passport-merge semantics, journey results | units ≤ 32 evidence | Unit 34 is speech-only; unit 36 changes text inside two existing `<p>` elements; neither can move them. Unit 33 *did* move geometry — which is why the zoom matrix was re-run rather than carried. |
| Unit 32's 553 fully-occluded rows; unit 27's 784-row museum-band sweep | units 32 / 27 | Not re-walked. Nothing in units 33/34/36 touches those selectors or surfaces. |

---

## 8 — FINDINGS SUMMARY, SEVERITY-TAGGED

| # | finding | severity | evidence |
| --- | --- | --- | --- |
| **V-C1** | All six previously-open AC19 contrast majors measure **above floor in all twelve cells**, independently confirmed. 0 of 2 626 rows below 4.5. | **closed** | §1, `cert-*.json`, `rows-*.jsonl`, `log-{l,d}{320,390,900,1024,1280,1440}.txt` |
| **V-C2** | `.le-meta` light worst is **6.26**, not the published **6.50**. Verdict unchanged; the record should carry the lower figure. | **note** (correction to the build log) | §1.2, `rows-l390.jsonl` |
| **V-C3** | `.gonext-item:hover b` at 1440 could not be measured by me (visibility gate). Dürer's figure stands unreviewed there. | **note** (perimeter, not a defect) | §1.3 |
| **V-Z1** | **F-1 closed** — 0 px overflow on `#/` at all eight widths in both themes, including the four that previously overflowed by 150/113/54/18 px. | **closed** | §2.1, `f1-light.json`, `f1-dark.json` |
| **V-Z2** | 200 % text zoom: **26 router cases × both themes, 0 overflow, 0 clipping** after unit 33's geometry changes. | **closed** | §2.2, `zoom200-{light,dark}-1280.json` |
| **V-Z3** | The inherited "26/26" zoom figure actually covered **25** routes — `#/artwork/<id>` was never zoom-tested. Now measured: clean. | **note** (coverage gap in prior evidence, now closed) | §2.2, `gapfill.json` |
| **V-S1** | Screenshot pack recaptured at HEAD: **64 files**, 0 broken images, in-page assertions recorded. `#/credits` copy asserted to be unit 36's. | **closed** | §3, `capture-assertions-*.json` |
| **V-S2** | A concurrent-run harness fault produced 16 blank dark-desktop frames that passed theme and viewport assertions. Caught by byte-size variance, re-run, corrected. | **note** (instrument, not product) | §3.1 |
| **V-M1** | `.md-name` renders at **2.34 px (320) / 2.97 px (390)**; illegible at narrow widths. Contrast passes; europe-zoom state only; accessible name preserved via `<title>`. **Not fixed in this build.** | **minor, open** | §4, `mdname-{light,dark}.json` |
| **V-L1** | Live region present, outside `#app`, sole live region in the document, **0 mutations across 12 route changes**, positive control fires correctly. No C-8 regression. | **closed** (DOM only — not audibility) | §5, `live-light.json` |
| **V-N1** | 26-route sweep: 0 errors, 0 warnings, 0 failed requests, 0 broken images; **`upload.wikimedia.org` only, 0 font/CDN providers**. | **closed** | §6, `sweep-light.json`, `log-sweep-light-clean.txt` |

**No new major or critical finding.** The one open defect I raise is **V-M1**, a
minor legibility residual that unit 33 named, did not fix, and did not
misrepresent.

---

## 9 — NOT TESTED (explicit)

1. Any browser engine other than Chrome — **including the Safari/VoiceOver
   combination in which every ear-confirmation in this project was obtained**.
2. Any screen reader. **Nothing in this document is evidence about speech.**
3. `deviceScaleFactor ≠ 1` (Retina/HiDPI).
4. The deployed origin; HTTPS; any host other than `localhost:8433`.
5. Dark-theme console/network sweep.
6. 200 % zoom at any viewport other than 1280×800, and zoom × mobile.
7. `button.chip:hover`, `#ig-svg.focused .ig-node.lit text` and
   `#search::placeholder` at 320 / 900 / 1024 / 1280.
8. `.gonext-item:hover b` at 1440.
9. Focus-ring contrast (WCAG 1.4.11).
10. `.branch-chip::before` and `.tone.on::after` painted contrast.
11. Onboarding deck, passport import / merge / cancel journeys, taste loop —
    behaviour and announcements alike.
12. Second and later ids for parameterised routes.
13. Colour-emoji glyph rendering.
14. `p/artwork/*.html` pre-rendered SEO pages.
15. Unit 32's 553 fully-occluded rows; unit 27's museum-band surfaces.
16. Print stylesheet, reduced-transparency, forced-colors / high-contrast mode.

---

## 10 — NOT CLAIMED

Gate 2 certification, merge approval, deployment approval, or a complete
enumeration of the build. I am the browser-evidence pole; the independent Quality
Reviewer certifies. No production file was touched by this pass, nothing was
pushed, and no `main` merge has occurred or been prepared.

---

## 11 — EVIDENCE INDEX

**Harness** (`protocol/tasks/PIG-001/evidence/harness/vermeer-cert/`)

| file | what it does |
| --- | --- |
| `cert.py` | independent contrast remeasurement; own site table, own hover forcing, rows flushed to JSONL as produced |
| `zoom.py` | F-1 at eight widths, and the 200 % matrix over the router cases; measures document overflow **and** crossing elements |
| `pack.py` | the 64-capture screenshot pack, `setDeviceMetricsOverride` + in-page shutter-time assertions |
| `probe4.py` | `.md-name` rendered-size characterisation; live-region identity, mutation log and positive control |
| `sweep.py` | 26-route console / network sweep from protocol events |
| `gapfill.py` | the artwork zoom case the old harness missed; `#/credits` copy assertion |

**Data**

| file | contents |
| --- | --- |
| `rows-{l,d}{320,390,900,1024,1280,1440}.jsonl` | 2 626 measured glyph rows, one JSON object each |
| `cert-*.json` / `log-*.txt` | per-cell summaries and full run logs |
| `f1-{light,dark}.json` | F-1, eight widths per theme |
| `zoom200-{light,dark}-1280.json` | 200 % matrix, per route |
| `mdname-{light,dark}.json` | rendered font size, CTM scale, glyph box per width |
| `live-light.json` | live-region identity, 12 route changes, positive control |
| `sweep-light.json` (contended) · `log-sweep-light-clean.txt` (**the evidence**) | console / network |
| `gapfill.json` | artwork zoom + credits copy assertions |
| `capture-assertions-{light,dark}-{390,1440}.json` | per-capture in-page assertions for all 64 PNGs |

**Screenshots** — 64 files in `protocol/tasks/PIG-001/evidence/`, named
`<route>__desktop-1440x900__<theme>.png` and `<route>__mobile-390x844__<theme>.png`.

---

## 12 — CLEANUP

My server (`python3 -m http.server 8433`, **PID 10589**) and every Chrome
instance I started were stopped by **exact PID**. No wildcard `rm` and no
pattern-matched `pkill` were used at any point — that has bitten this task twice.
**The owner's server on port 8422 (PID 93806) was never contacted and is still
running.** The untracked `THEORY_001.md`, `passport-test.html`, the modified
`.gitignore` and the two files under `protocol/tasks/PIG-001/` were left
untouched; the commit uses explicit paths only.

---

# N-1 CLOSED — MOBILE PACK RECAPTURED AT HEAD

**2026-08-06 · Vermeer · HEAD `4553b8e` (production tip `fb8ba6e`, unit 37)**

The owner chose recapture over a stated limitation. Every mobile frame is retaken
at HEAD and overwritten in place. Harness: `harness/vermeer-cert/n1recap.py`
(21 routes × 2 themes + the dark-only `v32-` frame) and `harness/vermeer-cert/n1pp.py`
(the two passport-import states); served from my own `python3 -m http.server 8447`.

**Count — 47 of 47.** `git status` reports exactly 47 modified
`*mobile-390x844*.png` and nothing else under `evidence/` but my four new
assertion JSONs and the two scripts. The pack is 24 dark + 23 light (the
`v32-influences-svg-labels` frame has only ever existed in dark; I did not invent
a light twin).

**Assertions — 47/47 passed, at shutter time, in the page.** Viewport set through
`Emulation.setDeviceMetricsOverride`, never `--window-size` (headless Chrome
clamps windows to a 500 px minimum on this Mac, which once produced 500 px
*layouts* cropped into 390 px *files*). Every capture asserted
`window.innerWidth === 390` and `documentElement.dataset.theme === <theme>` before
the shutter, and each frame decodes to exactly 390×844. `0` broken images across
729 image elements. Records: `n1-recap-{dark,light}-390.json`,
`n1-recap-pp-{dark,light}.json`.

**Blank-frame check — clean.** The fault I caught in myself last time was 16
frames that passed their own theme and viewport assertions while being blank, so
the same test was run again and then strengthened. Byte-size variance: smallest
92 675 B (`taste__…__dark`), largest 322 636 B (`daily__…__light`) — no cluster at
the bottom, no frame anywhere near the size a blank render compresses to. Beyond
byte size I decoded all 47 PNGs in pure Python and counted distinct sampled
colours: the *least* varied frame carries **444** distinct colours, the most 1 841.
A blank frame yields one to three. **Zero blank frames.**

Three pairs are byte-identical, and all three are expected aliases rather than a
stuck renderer: `influences` ≡ `v32-influences-svg-labels` and
`museum-louvre` ≡ `u27-museum-louvre` (dark and light) are two legacy names for
the same route, captured in the same run.

**One capture was wrong and was redone.** `passport-import-conflicts` first came
out a duplicate of `passport-import-arrival`: the harness's seed passport leaves
`quiz`, `palette` and `persona.adopted` empty, `ppFieldKey()` correctly treats an
empty shell as "no decision", so `passportConflicts()` returned `[]` and the
arrival screen offered "Merge into my passport" instead of "Choose what to keep".
Step 2 never rendered. `n1pp.py` gives the local passport a decision in all four
single-value fields and sends a payload differing in all four; the frame now shows
kicker `Taste Passport · import · 4 choices`, h1 *"Which of these should Pigment
keep?"*. Reported here because the first version passed every viewport and theme
assertion while depicting the wrong screen — the same class of fault as the blank
frames, caught by a content check rather than a geometry one.

**Desktop — verified current, not assumed.** Unit 37 touched `css/styles.css`,
`index.html` and `js/app.js`. Every changed CSS rule sits inside the ≤ 820 px
block (`.main-nav` box widening, `scroll-padding-inline-end`, the `::after`
strip); the `index.html` change is the two cache-busting query strings. The JS
`focusin` handler early-returns when the nav carries no mask. Measured at
1440×900 at HEAD: `maskImage: none`, and focusing each of the 8 nav links moves
`scrollLeft` by **0 px for all 8** — the handler is inert at desktop, by its own
guard, observed. **No desktop frame is stale; none was rewritten.**

One correction to how that was tested. I first tried byte-comparing fresh 1440×900
captures against the shipped ones; all 11 differed, which proves nothing — the
home hero rotates its artwork and lazily-loaded imagery settles differently between
runs, so desktop frames are not byte-reproducible across runs and byte identity is
not a valid staleness test. The geometry measurement above is the evidence; the
byte comparison is withdrawn.

**What actually changed, and what did not.** Decoding predecessor against
successor pixel by pixel: on `home__…__dark` 59.3 % of pixels differ (max channel
Δ 201) and on `artists__…__dark` 33.9 % — the recapture is emphatically not a
no-op, though most of that is the rotating hero and lazily-loaded imagery in the
content area, not unit 37. In the header band (y 0–129) the picture is the
opposite and is the honest finding: rows 0–38 are **pixel-identical**, and every
differing header pixel is a glyph-edge antialiasing difference of max channel
Δ 3–5 over a few dozen pixels. Van Eyck's measurement holds: the visible header
delta between `a71e2c5` and `fb8ba6e` is sub-perceptual.

That is expected, and it is worth stating plainly rather than dressing up.
**No screenshot in this pack depicts a focused nav link**, so no screenshot can
depict what unit 37 changed. The recapture fixes the *provenance* defect — the
pack now demonstrably corresponds to the code that ships — it does not turn the
pack into evidence for F-2. The evidence for F-2 is the measurement, taken at
HEAD at 390×844: the nav carries `linear-gradient(90deg, rgb(0,0,0) 78% …)`,
**5 of 8 links scroll the row on focus** (Explore 47 px, Movements 247, Techniques
360, Eras 424, Nations 424), and afterwards **0 links are clipped and 0 focus
rings remain inside the fade**. Unit 37 is live in the build these frames were
taken from.

**The pack now corresponds to `4553b8e`**, whose production files are those of
`fb8ba6e` — unit 37, the certified SHA. It no longer predates any production
commit.

**Cleanup.** My server (`python3 -m http.server 8447`, **PID 21483**) was stopped
by exact PID; every Chrome I started exited with its harness process. No wildcard
`rm`, no pattern `pkill`. **The owner's server on port 8422 (PID 93806) was never
contacted and is still listening.** `THEORY_001.md`, `passport-test.html`, the
modified `.gitignore` and the two files under `protocol/tasks/PIG-001/` are
untouched; the commit names every path explicitly.
