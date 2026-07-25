# BROWSER EVIDENCE — PIG-001

Reviewer: **Vermeer** (`claude-browser-reviewer`). Every statement below is tied
to an artifact in this directory or to a command reproducible from it. Anything
I could not exercise is listed under NOT TESTED and is never inferred.

## ENVIRONMENT

| | |
| --- | --- |
| Branch / commit | `pig-001-stabilization` @ `d7675dd` |
| Serve command | `python3 -m http.server 8421 -d .` (repo root) |
| Interactive browser | Chrome via the Claude Browser pane (`navigate` / `read_page` / `computer` / `javascript_tool` / `resize_window`) — real key presses and clicks |
| Capture browser | headless Chrome 1440×900 / 390×844 / 1280×800, `--screenshot`, one fresh profile per shot |
| Build identity verified | `#/credits` renders (previously absent); `css/styles.css` contains **16 `@font-face`** rules pointing at `assets/fonts/*.woff2`; `index.html` contains no `fonts.googleapis.com` reference |
| Corpus verified live | `ARTISTS.length = 256`, `CATALOG.length = 323`, `VENUES.length = 116`, `PHOTO_CREDITS = 104` keys, `IMAGE_CREDITS = 27` keys |
| Data freshness | all data files re-fetched with `{cache:"reload"}` before judging; every screenshot taken in a fresh Chrome profile |

All screenshots on disk were **re-captured for this run**; the stale files from
the two interrupted runs were overwritten.

## VIEWPORTS & THEMES COVERED

| Surface set | 1440×900 desktop | 390×844 mobile | dark | light |
| --- | --- | --- | --- | --- |
| 16 routes (`#/`, `#/artists`, artist, artwork, `#/explore`, `#/timeline`, `#/influences`, `#/museums`, museum, `#/lists`, `#/palette`, `#/taste`, `#/daily`, `#/privacy`, `#/credits`, invalid) | yes | yes | yes | yes |
| Passport import — arrival screen | yes | — | yes | yes |
| Passport import — per-field conflicts | yes | yes | yes | yes |
| 200 % text zoom @ 1280×800 (`#/`, `#/artists`) | yes | — | yes | yes |

**74 screenshots** total: 64 route shots + 6 passport-import shots + 4 zoom shots.
Measurement sweeps additionally covered **26 routes × 5 widths** (320 / 390 / 768
/ 1280 / 1440) in the interactive browser.

## EVIDENCE INDEX

| File | What it shows |
| --- | --- |
| `<route>__desktop-1440x900__{dark,light}.png` (32) | every changed surface at desktop, both themes |
| `<route>__mobile-390x844__{dark,light}.png` (32) | the same 16 routes at mobile, both themes |
| `museum-louvre__*__*.png` | museum page **with the photo credit line rendered** (AC11/AC12) |
| `credits__*__*.png` | the new `#/credits` attribution page (unit 24) |
| `privacy__*__*.png` | the new `#/privacy` page |
| `invalid-route__*__*.png` | 404 view for an unrouted hash |
| `passport-import-arrival__desktop-1440x900__{dark,light}.png` | import screen 1: what merges vs what needs a choice |
| `passport-import-conflicts__{desktop-1440x900,mobile-390x844}__{dark,light}.png` | the per-field keep-mine / take-theirs UI, 4 conflicts (AC5/AC6) |
| `zoom200-{home,artists}__desktop-1280x800__{dark,light}.png` | 200 % text zoom at 1280 — shows the nav overflow in F-1 |
| `contrast-audit.py` | stdlib-only WCAG 2.2 auditor: token table, measured pairs, browser composites |
| `contrast-pairs-measured.csv` | the 139 fg/bg pairs that actually render, harvested from the live DOM across 16 routes × 2 themes |
| `contrast-audit-output.txt` | full audit output (pass 1 / 2 / 3) |
| `_shot.html`, `_zoomshot.html`, `_ppshot.html`, `_rmcheck.html` | capture harnesses (evidence only, not production files) |

## FINDINGS

Severity: **P1** = blocks the criterion · **P2** = criterion met but with a real
defect · **P3** = observation, no criterion breached.

### F-1 — 200 % text zoom overflows every route horizontally · AC18 · **P1**

At 1280 CSS px with root font-size at 200 % (32 px), **all 26 routes** push
`document.documentElement.scrollWidth` past `clientWidth` by **115–117 px**.

Measured cause, isolated: `nav.main-nav` computes `flex-wrap: nowrap`; at 200 %
it measures **1359 px wide inside a 1270 px viewport**, and the element sitting
past the right edge is the last nav link, "Nations". The header's *outer* row
does wrap correctly at 200 % (the nav drops to its own line, `left` moves from
229 px to 28 px) — the Wave A wrap fix works; it is the nav row itself that
cannot wrap.

| Route (sample) | overflow px | widest offender |
| --- | --- | --- |
| `#/artists`, `#/movements`, `#/nations` | +117 | `nav.main-nav` |
| `#/`, `#/palette`, `#/credits`, `#/no-such-page` | +115 | `nav.main-nav` |
| `#/museums`, `#/timeline`, `#/influences` | +116 | `nav.main-nav` |

Clipping at the same setting (`overflow:hidden` containers losing content):

| Route | element | content lost |
| --- | --- | --- |
| `#/museum/louvre` | `div.mu-hero` | 942 px |
| `#/`, `#/lists`, `#/list/…` | `div.card-tagline` | 266 px |
| `#/influences` | `button.skip-inline` | 109 px — **the skip-the-graph bypass control itself is clipped** |

Evidence: `zoom200-*__desktop-1280x800__*.png`.

### F-2 — light-mode hero title falls below AA over the generative canvas · AC19 · **P1**

`h1.home-title` is painted with `-webkit-background-clip:text`, so the glyphs are
the gradient stops, not the computed colour. Sampling `#bg-canvas` with
`getImageData()` at nine points across the title's box and compositing (light
theme applies `#bg-canvas{opacity:.6}`):

| theme | worst measured | threshold (large text) | verdict |
| --- | --- | --- | --- |
| dark | **6.20 : 1** | 3.0 | PASS |
| light | **2.47 : 1** | 3.0 | **FAIL** |

Worst pair: stop `rgb(168,129,60)` over backdrop `rgb(223,213,201)`. Reproduce:
`python3 contrast-audit.py`, pass 3.

### F-3 — 43 rendered text pairs below AA, both themes · AC19 · **P2**

From the 139 pairs actually rendered across 16 routes × 2 themes (pass 2). The
high-volume ones:

| theme | fg | bg | ratio | need | occurrences | element |
| --- | --- | --- | --- | --- | --- | --- |
| light | `#7a715e` | `#faf6ec` | **4.47** | 4.5 | 768 | `p` — the main body paragraph colour, short by 0.03 |
| light | `#7a715e` | `#f2ecdf` | 4.10 | 4.5 | 620 | `span.brand-sub` (9 px) |
| light | `#a8813c` | `#faf6ec` | 3.31 | 4.5 | 127 | `div.ec-kicker` |
| dark | `#6e675a` | `#0d0c0a` | 3.49 | 4.5 | 207 | `p.footer-note` |
| light | `#a39a86` | `#f2ecdf` | **2.37** | 4.5 | 207 | `p.footer-note` |
| light | `#a39a86` | `#faf6ec` | 2.59 | 4.5 | 21 | `a.chip-label` |
| light | `#8a6a2e` | `#f2ecdf` | 4.27 | 4.5 | 48 | `div.kicker` |

Root cause in the token table (pass 1): `--faint` fails body AA in both themes
and fails even the 3:1 UI floor in light (2.21–2.59 : 1); `--muted` fails body AA
in light on every surface (3.81–4.47); `--gold` fails body AA in light on every
surface (2.83–3.31).

The remaining ~30 failures are `#/timeline` painter-bar labels (fixed palette ink
on fixed swatch colours, identical in both themes), ranging 2.42–4.50 : 1 —
worst `#f6f1e6` on `#d9886e` (2.42, "Paul Signac").

### F-4 — route change announces twice · AC15 · **P2** (confirms Wave C deviation C-8)

Measured with a `MutationObserver` on `#route-status` across five navigations.
On **every** route change both channels fire:

1. focus moves to `h1[tabindex="-1"]` — a screen reader announces the heading;
2. `#route-status` (`role="status"`, `aria-live="polite"`) mutates **once** with
   the page name — announced again.

| route | focus target text | live-region text | live mutations |
| --- | --- | --- | --- |
| `#/museums` | "Museums" | "Museums" | 1 |
| `#/timeline` | "The grand timeline" | "Timeline" | 1 |
| `#/palette` | "Find your palette." | "Find your palette" | 1 |
| `#/credits` | "Credits" | "Credits" | 1 |
| `#/no-such-page` | "Blank canvas" | "Lost" | 1 |

C-8 is real and reproducible. Note that in 3 of 5 cases the two announcements
carry **different wording** for the same event, so the user hears two different
names for one page rather than a duplicate.

### F-5 — one Escape both closes the listbox and clears the query · AC16 · **P3**

APG's combobox pattern separates the two: the first Escape dismisses the popup,
a second clears the value. Measured here, a single Escape sets
`aria-expanded="false"`, hides the listbox, clears `aria-activedescendant` **and**
empties the input. Focus correctly returns to the input (not `body`). Minor
divergence, no criterion breached.

### F-6 — the skip-the-graph button is unthemed · AC17/AC19 · **P3**

`button.skip-inline` on `#/influences` computes `#000000` on `#efefef` in **both**
themes — the user-agent default button styling, not a Pigment token. Contrast is
fine (18.1 : 1); it simply does not follow the theme. Combined with F-1's 109 px
clipping of the same control at 200 % zoom, this control deserves attention.

## VERIFIED PASSES

### AC18 — overflow at the five widths: **PASS, both Wave A causes gone**

`documentElement.scrollWidth` vs `clientWidth`, all **26 routes** at each width:

| width | routes measured | routes overflowing | max scrollWidth | verdict |
| --- | --- | --- | --- | --- |
| 320 | 26 | **0** | 320 | PASS |
| 390 | 26 | **0** | 390 | PASS |
| 768 | 26 | **0** | 768 | PASS |
| 1280 | 26 | **0** | 1270 (= clientWidth) | PASS |
| 1440 | 26 | **0** | 1430 (= clientWidth) | PASS |

**130 / 130 route×width combinations show zero horizontal overflow.**

- Cause 1 — 320 px `.strip` negative-margin bleed + oversized cards: **fixed**.
  At 320 every route reports `scrollWidth == clientWidth == 320`; the offender
  scan returns no element extending past the viewport on any route.
- Cause 2 — 1280 px header search + toggle non-wrapping row, previously
  +127…137 px on **all** routes: **fixed**. At 1280, `header.scrollWidth`,
  `header.clientWidth` and the header's right edge all equal 1270; zero routes
  overflow.

(200 % text zoom at 1280 is the separate failure F-1.)

### AC26 / AC25 — route sweep: clean, and no Google Fonts

26 routes visited in one session with `console.error` / `console.warn` /
`window.onerror` / `unhandledrejection` instrumented and the full Resource Timing
buffer read afterwards:

| measure | result |
| --- | --- |
| console errors | **0** |
| console warnings | **0** |
| HTTP responses ≥ 400 | **0** (`responseStatus` confirmed supported) |
| broken images | **0** of **690** images checked across the 26 routes |
| total requests | 373 |

**External hosts contacted automatically — complete list:**

| host | requests | note |
| --- | --- | --- |
| `localhost:8421` | 39 | the site itself (html, css, js, self-hosted woff2) |
| `upload.wikimedia.org` | 334 | artwork and museum images |

- `fonts.googleapis.com` — **0 requests**. `fonts.gstatic.com` — **0 requests**.
  Unit 20's self-hosting is confirmed at runtime, not just in source.
- Unit 23's disclosure that `upload.wikimedia.org` is the only automatic external
  host is **independently confirmed**.
- Unit 24's credit links introduce **no automatic request**:
  `commons.wikimedia.org` and `creativecommons.org` appear only as `href`
  attributes (`target="_blank" rel="noopener"`), and neither host appears in the
  Resource Timing buffer after the full sweep. They are click-through only.

### AC17 — skip link: PASS, both themes

| | dark | light |
| --- | --- | --- |
| first tabbable element in the document | yes | yes |
| off-screen when unfocused | `top: -120px` (fixed) | `top: -120px` |
| moves into view on focus | `top: 14px`, 140×39, in viewport | `top: 14px`, 140×39, in viewport |
| visible indicator | 2 px solid `rgb(201,164,92)`, z-index 140 | 2 px solid `rgb(168,129,60)` |
| activation works | focus → `h1[tabindex="-1"]` "All 256 painters" inside `#app` | same |

### AC17 — influence graph: PASS (Enter path), bypass verified

- 204 graph nodes, each `<g role="button" tabindex="0">` with a real accessible
  name (`"Leonardo da Vinci, 1452–1519, 2 connections"`).
- **Bypass works under a real key press.** `button.skip-inline`
  ("Skip the graph — 204 painters follow", count accurate) sits at tab position
  18, immediately before the first node at 19; the last node is at 222. A real
  Enter moved focus to `p#ig-end` — **204 tab stops skipped**, confirmed by index
  arithmetic, not by assumption.
- **Visible focus ring in both themes**, verified under a real Tab (so
  `:focus-visible` genuinely matched): `circle.ig-ring` r=13.8 around an r=8.8
  node, stroke 2.5 px, `#e8c98a` dark / `#8a6a2e` light. Contrast against the
  graph panel: **11.53 : 1** dark, **4.65 : 1** light — both above the 3 : 1 UI
  floor. (Programmatic `.focus()` does *not* trigger `:focus-visible`; measuring
  it that way would have produced a false failure.)
- **Enter activates**: first Enter selects the node — 3 nodes light up, a detail
  panel appears ("influenced Raphael / rival of Michelangelo Buonarroti / Open da
  Vinci's page →"), and the node's accessible name *updates* to
  `"… — circle shown; choose again to open their page"`, which is exemplary state
  communication.

### AC16 — search combobox: PASS on every checked point

Attributes before typing: `role="combobox"`, `aria-expanded="false"`,
`aria-controls="search-results"` (target exists), `aria-haspopup="listbox"`,
`aria-autocomplete="list"`, `aria-label` present, `autocomplete="off"`.

| step (real keystrokes) | observed |
| --- | --- |
| type `monet` | `aria-expanded="true"`; listbox visible with 9 `role="option"`; **exact artist "Claude Monet" ranked first**, works below — not starved |
| `aria-activedescendant` before arrowing | `null` (correct per APG) |
| ArrowDown | `aria-activedescendant="sr-opt-0"`, exactly **one** `aria-selected="true"`, DOM focus stays in the input |
| Escape | `aria-expanded="false"`, listbox hidden, activedescendant cleared, **focus returns to the input, not body** |
| type `vermeer`, ArrowDown, Enter | navigates to `#/artist/johannes-vermeer`, listbox dismissed, focus lands on the `h1` |

### AC7 — onboarding checkpoint resume: **5 / 5 PASS**

Method: drive the flow to the checkpoint, snapshot `sessionStorage`
`pigment.onboarding.v1` **and** the rendered view, then perform a **genuine
`location.reload()`**, then compare. (The Browser pane's own `navigate` restores
a sessionStorage snapshot, which would have masked a failure — an in-page reload
was used instead so the test is real.)

| # | checkpoint | resumed at | prior answers intact | same deck | verdict |
| --- | --- | --- | --- | --- | --- |
| 1 | tone selection | step 1, "Pick four tones." | tones `["ultramarine"]`, and the button still renders `aria-pressed="true"` | 16/16 ids identical | **PASS** |
| 2 | artwork 8 of 16 | step 2, counter reads **"8 of 16"**, same work (*Girl with a Pearl Earring*) | 4 admired + 3 skipped, exact ids | 16/16 identical | **PASS** |
| 3 | question 3 of 5 | step 3, same question text, options `q3:a…q3:d` | `{q1:"a", q2:"b"}` | 16/16 identical | **PASS** |
| 4 | reveal | step 4, identical reveal copy | all 5 answers, 10 admired, 6 skipped | 16/16 identical; **same 3 persona candidates in the same order** | **PASS** |
| 5 | adopt / defer | `adopted:true` persisted; adopt and "Decide later" buttons correctly gone | persona `gilded-sentimentalist` persisted to `pigment.taste.v1` | 16/16 identical | **PASS** |

Observation (not a defect): after checkpoint 5 the reload lands on the Taste view
rather than replaying the reveal — onboarding is complete, and all state survived.

### AC5 / AC6 — import conflict UI: **PASS, cancel is byte-identical**

Built a local Passport (18 admirations, persona *Gilded Sentimentalist*, 4 tones,
5 quiz answers, milestones), then imported a passport differing in **all four**
single-value fields plus 2 extra admirations and 1 "seen".

1. **Asked per conflicting field — yes, all four.** Separate panels for
   *Onboarding answers*, *Chosen tones*, *Adopted Persona*, *Progress markers*,
   each with `Keep mine` / `Take theirs` as `aria-pressed` buttons, both sides
   summarised in plain language and dated. `Keep mine` is pre-selected.
2. **Cancel changes nothing — byte-identical.** `pigment.taste.v1` read before
   and after: **2578 bytes → 2578 bytes, first differing index = −1 (no
   difference at any index)**. Storage was also unchanged after *each* choice
   toggle and after opening the conflict screen — no write happens on any path
   until Merge.
3. **The copy is truthful.** Screen 1 states lists are combined and "none of
   yours is removed"; screen 2 states "Nothing is written until you press Merge
   below, and nothing at all is written if you cancel." Both verified by
   executing the merge: choosing only `persona: theirs` replaced **only** the
   persona; palette, quiz and milestones kept mine; admirations unioned 18 → 20
   with every original entry retained. The original passport was then restored
   byte-identically.

### AC20 — reduced motion: PASS

Two headless runs of `_rmcheck.html`, identical except for
`--force-prefers-reduced-motion`, probing from inside the page:

| probe | normal | reduced (`matchMedia` = true) |
| --- | --- | --- |
| `div.strip-track` `stripScroll` | **running, 90 s, infinite** | **animation removed entirely** |
| `main.view-enter` `viewIn` | 0.55 s | 0.001 s |
| `h1.home-title` `shimmer` | 7 s infinite | 0.001 s |
| elements with a non-zero transition | **621** | **0** |
| running Web Animations | 2 / 3 | 1 / 2 |
| `.strip` `overflow-x` | `hidden` | **`auto`** |
| `.strip` keyboard-reachable items | 514 | **514** |
| counters (`[data-count]`) | 256, 76, 39, 8, 37 | **256, 76, 39, 8, 37** |

No information and no control is lost: when the marquee stops, `overflow-x`
becomes `auto` so the same content is reachable by scrolling, all 514 items stay
keyboard-reachable, and the counters still show their real values rather than
sitting at zero. Minor note: `shimmer` remains `iteration-count: infinite` at
0.001 s — imperceptible, but a duration of 0 or `animation: none` would be
cleaner.

### AC11 / AC12 — photo credits: PASS, no raw Commons HTML leaks

Museum page `#/museum/louvre`:

```html
<p class="img-credit mu-credit">Photograph: Benh LIEU SONG (Flickr) ·
<a href="https://creativecommons.org/licenses/by-sa/3.0" target="_blank" rel="noopener license">CC BY-SA 3.0</a> ·
<a href="https://commons.wikimedia.org/wiki/File:Louvre_Museum_Wikimedia_Commons.jpg" target="_blank" rel="noopener">file on Commons</a></p>
```

Artwork page `#/artwork/david` — credit renders inline *and* again inside the
lightbox where the thumbnail becomes the image:
`Image credit: Jörg Bittner Unna · CC BY 3.0 · file on Commons`, with
`rel="noopener license"` on the licence link and the correct percent-encoded
Commons file page.

All four required parts present in both cases: **author · licence name · licence
link · Commons file-page link**. No escaped-tag or raw-HTML leakage: a scan for
`&lt;`/`&gt;` and for literal tags in `textContent` returned false across the
artwork page, the museum page and the open lightbox.

## NOT TESTED

1. **Space-key activation of influence-graph nodes and other custom controls.**
   The Browser pane cannot emit a space key: it delivers `KeyboardEvent.key === ""`
   for `"space"`, `"Space"` and `" "` alike, verified with a capture-phase
   listener. Enter was tested and passes. Space is untested — **not assumed to
   pass and not reported as failing.**
2. **Real assistive-technology output.** I measured focus movement and live-region
   mutations (F-4), which is the mechanism; I did not run VoiceOver or NVDA, so
   the actual spoken result is unverified.
3. **AC19 for text over artwork photographs.** The generative `#bg-canvas` was
   pixel-sampled (F-2). Text sitting over `upload.wikimedia.org` photographs was
   not sampled — those canvases are cross-origin-tainted, so `getImageData()`
   would throw. The `.ec-cover` / `.card-art` elements checked on `#/` contained
   no text nodes, so no cover-text pair entered the audit.
4. **200 % zoom beyond `#/` and `#/artists` as screenshots.** The overflow
   *measurement* covers all 26 routes; only those two routes were captured as
   zoom images.
5. **768 px and 1280 px screenshots.** Those widths were measured, not captured;
   the screenshot matrix is 1440 and 390 as specified.
6. **Storage-failure UX (AC8), the full 18 ARIA control types (AC16), the full
   24-query search fixture (AC21), Explore alignment (AC22), and the relationship
   journey (AC24).** Outside the scope I was given; no evidence collected, no
   opinion offered.
7. **Real touch input on a physical mobile device.** Mobile viewports were
   emulated by CSS-pixel resizing only.

## SUMMARY

| Criterion | Verdict |
| --- | --- |
| AC5 / AC6 import conflicts + cancel | **PASS** (byte-identical cancel) |
| AC7 checkpoint resume | **PASS 5 / 5** |
| AC11 / AC12 photo credits | **PASS** |
| AC15 route orientation | **PASS with defect F-4** (double announcement, C-8 confirmed) |
| AC16 search / combobox semantics | **PASS** (F-5 minor) |
| AC17 skip link + graph keyboard | **PASS** for skip link, bypass, focus ring, Enter; Space NOT TESTED |
| AC18 responsive overflow | **PASS 130/130** at the five widths; **FAIL F-1** at 200 % text zoom |
| AC19 contrast | **FAIL** — F-2 (light hero, 2.47 : 1) and F-3 (43 pairs) |
| AC20 reduced motion | **PASS** |
| AC25 third-party requests | **PASS** — only `upload.wikimedia.org`; zero Google Fonts |
| AC26 route sweep | **PASS** — 0 errors, 0 warnings, 0 failed requests, 0 broken images |
