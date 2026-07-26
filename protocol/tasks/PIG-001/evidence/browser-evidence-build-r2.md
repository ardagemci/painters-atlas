# BROWSER EVIDENCE — PIG-001 · ROUND 2 (post unit 25)

Reviewer: **Vermeer** (`claude-browser-reviewer`). This is the re-verification of
unit 25 (`b7834b5`…`2296f9d`, log at `evidence/build-log-unit-25.md`). It
supersedes the measurements in **`browser-evidence-build.md`** (round 1, commit
`1214062`), which is retained unchanged as the round-1 record because Matisse's
adjudication cites it. Read the two together: round 1 is the "before" column.

Every statement below is tied to an artifact in this directory or to a command
reproducible from it. Anything I could not exercise is under NOT TESTED and is
never inferred. Where round 1 was wrong, I say so and retract it.

## ENVIRONMENT

| | |
| --- | --- |
| Branch / commit | `pig-001-stabilization` @ `a018fe2` (verified: not `main`) |
| Serve command | `python3 -m http.server 8421 -d .` (repo root) |
| Browser | Chrome 150.0.7871.182, headless, driven over the **DevTools Protocol** |
| Cache | `Network.setCacheDisabled=true` for every session; every route loaded as a **fresh document** via a unique query string, so CSS and data are re-fetched, never reused |
| Build identity verified | `.hero-shade` present (3 rules); `--rose`/`--mauve` present in both themes; `.main-nav{flex-wrap:wrap}`; `.skip-inline` themed on its base rule; **`#route-status` absent from the document (0 live regions)** — i.e. all six unit-25 groups are in the served build |
| Harness | `_shot.html`, `_zoomshot.html`, `_ppshot.html`, `_rmcheck.html` (round 1); round 2 drives the page directly over CDP |

### Method change, and why it was necessary

Round 1 captured screenshots with `chrome --headless --screenshot
--window-size=W,H`. **On this Mac that flag is clamped to a 500 px minimum
window width.** A probe page reporting its own metrics under
`--window-size=390,844` renders `iw=500 cw=500` — Chrome lays the page out at
500 px and then writes a 390 px file. That is the exact evidence defect Matisse
found: a true-390-pixel file containing a 500 px layout, cropped. Round 1's DOM
measurements (`scrollWidth == clientWidth == 390`) were taken in a *different*,
correctly-sized browser session, which is why they disagreed with the images and
why the contradiction was not visible from either side alone.

Round 2 sets the viewport with `Emulation.setDeviceMetricsOverride`, which is not
subject to the window clamp, and captures with `Page.captureScreenshot`.

## A — SCREENSHOTS · mobile capture defect **FIXED**

**Before:** 390 px files containing a 500 px layout — words sheared mid-glyph,
`nav.main-nav` absent. Matisse declined to adjudicate mobile composition on them.
**After:** true 390 px renders. Verdict: **true render, not a tooling limit.**

Every capture carries an assertion evaluated **in the same page, at capture
time**, immediately before the shutter (`capture-assertions.json`, 64 rows):

| assertion | desktop 1440 | mobile 390 |
| --- | --- | --- |
| `window.innerWidth` / `clientWidth` | 1440 / 1440 | **390 / 390** |
| `#app` padding (the ≤820 px rule at `styles.css:1121`) | `34px 28px 90px` | **`22px 16px 70px`** |
| `.main-nav` computed `order` | `0` | **`3`** |
| `.main-nav` computed `overflow-x` | `visible` | **`auto`** |
| `data-theme` matches the requested theme | yes | yes |
| nav present with all 8 links, non-zero box | yes | yes |

**64 / 64 captures passed all six assertions**, so the ≤820 px rules are provably
live in the captured frame, not merely requested. Confirmed by eye on
`home__mobile-390x844__light.png` ("Find your place in / the history of art."
breaks cleanly) and `privacy__mobile-390x844__light.png` (body copy wraps, no
shearing) — the two files Matisse named.

**80 screenshots re-captured**, all overwritten in place so existing citations
stay valid: 64 route shots (16 routes × {desktop-1440x900, mobile-390x844} ×
{dark, light}), 8 passport-import shots, 8 zoom shots.

The passport-import set was outside my brief but its mobile files carried the
same defect, so it was re-captured too; `passport-import-arrival` now exists at
mobile, which it did not before. Each was asserted at `iframe.contentWindow.innerWidth == 390`.

## B — DOM CONTRAST RE-WALK (AC19) · **43 → 5 reported, 3 genuine**

`contrast-pairs-measured.csv` regenerated from the live DOM, same semantics as
round 1 (every element with its own text run; computed colour composited over the
flattened background chain; AA size classification; deduped with counts): 16
routes × 2 themes, **372 distinct pairs over 6 979 occurrences**. `contrast-audit.py`
pass 2 re-run against it (`contrast-audit-output.txt`).

**Pass 2 failures: 43 → 5.** The "43" is retired. Of the 5:

| # | theme | fg | bg | ratio | need | count | selector | route | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | light | `#f6f1e6` | `#faf6ec` | 1.04 | 4.5 | 2 | `span` ("Jasper Johns") | `#/timeline` | **walk artifact** |
| 2 | dark | `#0d0c0a` | `#16140f` | 1.06 | 4.5 | 9 | `span` ("Yayoi Kusama") | `#/timeline` | **walk artifact** |
| 3 | light | `#9e7938` | `#faf6ec` | 3.71 | 4.5 | 120 | `div.lc-kicker` | `#/lists` | **genuine** |
| 4 | light | `#9e7938` | `#f2ecdf` | 3.40 | 4.5 | 1 | `button.tl2-leg.tl2-leg-more` | `#/timeline` | **genuine** |
| 5 | light | `#9e7938` | `#faf6ec` | 3.71 | 4.5 | 1 | `div.tl2-year.t.now` ("today") | `#/timeline` | **genuine** |

Rows 1–2 are **artifacts of the walk, not render failures**. `#/timeline` bars
for *living* painters are filled with an inline `linear-gradient` (`js/app.js:1002`),
and a computed-style walk reads `backgroundColor` only, so it falls through to the
page behind the bar and scores the ink against the wrong surface. Measured from
real glyph pixels instead (section F) those same labels are at **4.61 : 1**. Both
were reproduced and disproved, not waved away; the caveat is now printed by
`contrast-audit.py` itself so the number cannot mislead a later reader.

Rows 3–5 are one defect: **`--gold` (light `#9e7938`) is still used as small
text** in places the 25b re-pointing missed. A supplementary walk over the **10
routes outside the 16-route set** found a fourth instance:

| selector | ratio | need | route |
| --- | --- | --- | --- |
| `span.le-num` (1.2 rem) | **3.40** | 4.5 | `#/list/<id>` |

The Synthesis Lead's pass-1 finding holds in the rendered DOM: **every body-text
*token* clears AA on all three real surfaces**. The residue is not a token
problem — it is four call sites still pointing at `--gold` rather than `--gold2`.

## C — HERO OVER THE GENERATIVE CANVAS (AC19) · light **PASS 3.06**, dark **FAIL 1.10**

Round 1 sampled `#bg-canvas` with `getImageData()` at nine points and modelled the
composite. Round 2 measures **real painted pixels on real glyph pixels**: two
screenshots per load, one with the hero text painted and one with it hidden; a
pixel counts only where the two differ strongly, which confines the sample to
where a glyph actually lands instead of averaging over a mostly-empty text box.
Ink = the declared paint (the four gradient stops for the `background-clip:text`
title, computed colour otherwise); backdrop = that pixel with the text hidden.
**8 fresh covers per theme**, worst observed reported.

### The bound was computed against the wrong layer

A canvas inventory taken in the page (`hero-composite.json`) shows **two** canvases
over the hero:

| canvas | opacity | in `.home-hero` | covers hero box |
| --- | --- | --- | --- |
| `#bg-canvas` | **0.6** | no | yes (full page 1440×900) |
| *unnamed* | **1.0** | **yes** | yes (129,103 · 1182×438) |

Matisse's bound and unit 25d's arithmetic ("canvas opacity .6 … effective paper
alpha .72 … blend factor .168 … worst reachable backdrop `rgb(201,196,186)`")
were derived from `#bg-canvas` at opacity .6. The layer actually behind the hero
title is the **in-hero cover canvas at opacity 1**, scrimmed only by `.hero-shade`.

### Observed vs the published bound

| theme | element | worst observed | predicted bound | floor | verdict |
| --- | --- | --- | --- | --- | --- |
| light | `h1.home-title` | **3.06** | 3.23 (min stop; 6.62 / 3.23 / 4.29) | 3.0 | **PASS by 0.06** |
| light | `div.kicker` | 8.08 | — | 4.5 | PASS |
| light | `p.lede` | 5.69 | — | 4.5 | PASS |
| light | `p.footer-note` (cover credit) | 5.44 | — | 4.5 | PASS |
| light | `a` (painter link in the credit) | 5.72 | — | 4.5 | PASS |
| dark | `h1.home-title` | **1.10** | not modelled | 3.0 | **FAIL** |
| dark | `div.kicker` | 4.05 | — | 4.5 | **FAIL** |
| dark | `p.lede` | **1.97** | — | 4.5 | **FAIL** |
| dark | `p.footer-note` | **1.74** | — | 4.5 | **FAIL** |
| dark | `a` | 4.09 | — | 4.5 | **FAIL** |

**Light: the remediation works** — 2.47 → 3.06, and all four small-text rungs
clear 4.5 comfortably. Two honesty notes: the observed 3.06 is **below the 3.23
the bound predicted**, because the bound used the wrong layer; and the cover
regenerates per visit, so 3.06 is the worst of 8 draws, not a guaranteed floor.
The true margin over 3.0 is 0.06 and is not proven to hold on an unseen cover.

**Dark was never fixed and is far worse than round 1 reported.** Round 1 recorded
dark at 6.20 PASS; that measured `#bg-canvas`, the wrong surface, and so measured
a surface the title does not sit on. Unit 25d's own commit message says
"dark's `.hero-shade` is untouched", and `styles.css:746` leaves dark's scrim at
`rgba(var(--bg-rgb),.25)` at the centre of the ellipse — a 25 % veil over a
full-opacity cover, exactly where the title paints. This is visible without
instruments in `home__desktop-1440x900__dark.png`: the title crosses a saturated
yellow shape and the lede crosses blue and red ones.

This is a **pre-existing defect that round 1 missed**, not a regression introduced
by unit 25.

## D — 200 % TEXT ZOOM (AC18) · **PASS, 0 px overflow on 26/26 routes**

Root font-size forced to 200 % (32 px) after render, re-applied twice to survive
the router's re-paint. Measured at **1270 px** (identical to round 1's effective
`clientWidth`, so the comparison is like-for-like) and again at **1280 px**.

| | round 1 | round 2 @1270 | round 2 @1280 |
| --- | --- | --- | --- |
| routes measured | 26 | **26** | 25 |
| routes overflowing | **26** | **0** | **0** |
| overflow per route | **+115 … +117 px** | **+0** | **+0** |
| `documentElement` sw / cw | 1385 / 1270 | **1270 / 1270** | **1280 / 1280** |
| `nav.main-nav` | 1359 px wide, right edge 1386 | **493 × 258, right edge 868** | 503 × 192, right edge 878 |

`nav.main-nav` now wraps to three rows with **all eight destinations visible and
in the same focus order** (`zoom200-*__desktop-1280x800__*.png`). F-1 is resolved.

The 26 routes are one per `switch` case in `route()` (`js/app.js:2359`), including
the `passport` case and the `default` 404. `#/artwork/david` was measured
separately at 1270 (`over = 0`) after the discovery sweep returned 25.

### The two round-1 clipping claims, re-examined

**`button.skip-inline` — RESOLVED, and round 1's number was measured in the wrong state.**

| state | position | box | lostW / lostH | in viewport | colour |
| --- | --- | --- | --- | --- | --- |
| unfocused | `absolute` | 14 × 4 | 100 / 217 | — | — |
| **focused** | `static` | **492 × 49** | **0 / 0** | **yes** | `rgb(232,201,138)` on `rgb(29,26,19)` |

Unfocused, `.skip-inline` is a deliberate 1 px clipped visually-hidden control
(`styles.css:328`), so a clip reading taken there is meaningless — that is what
round 1's "109 px" was. Focused, it is unclipped and fully in the viewport.
**F-6 (unthemed control) is also resolved**: the tokens are on the base rule now.

**`div.mu-hero` 942 px — RETRACTED. Round 1 was wrong; unit 25e was right to decline it.**

The overflow is real but it is **six decorative collage `<img>` tiles and zero
text** (`textsOutside = 0` of 6 text-bearing elements on both museum routes), and
it is **larger unzoomed than zoomed**:

| route | 100 % zoom | 200 % zoom |
| --- | --- | --- |
| `#/museum/louvre` | **982 px** | 942 px |
| `#/museum/met` | — | 707 px |

A quantity that shrinks when you zoom is not a zoom defect. This is the
border-radius mask over the bleeding collage, exactly as Dürer argued. His
specific claim "measured lostW/lostH = 0" is not reproducible — the number is
942/982 — but his conclusion was correct and no content is lost. **Round 1's F-1
sub-finding is withdrawn.**

## E — ROUTE ANNOUNCEMENT (AC15 / C-8) · **RESOLVED**

Same five routes as round 1, so the comparison is like-for-like. A
`MutationObserver` over `documentElement` (childList + characterData + attribute
changes to `aria-live`/`role`) plus a capture-phase `focusin` log, installed once
and carried across real hash navigations.

| route | round 1 focus target | round 1 live text | round 1 live mutations | round 2 live mutations | round 2 focus target |
| --- | --- | --- | --- | --- | --- |
| `#/museums` | "Museums" | "Museums" | 1 | **0** | `h1.display[tabindex=-1]` "Museums" |
| `#/timeline` | "The grand timeline" | "Timeline" | 1 | **0** | `h1.display[tabindex=-1]` "The grand timeline" |
| `#/palette` | "Find your palette." | "Find your palette" | 1 | **0** | `h1.display[tabindex=-1]` "Find your palette." |
| `#/credits` | "Credits" | "Credits" | 1 | **0** | `h1.display[tabindex=-1]` "Credits" |
| `#/no-such-page` | "Blank canvas" | "Lost" | 1 | **0** | `h1[tabindex=-1]` "Blank canvas" |

- **`[aria-live], [role=status], [role=alert], [role=log]` in the whole document: 0**, on every one of the five routes. No live region remains to fire.
- Page identity is conveyed **exactly once**, by the focus move.
- Focus still lands on a meaningful labelled entry point: the view's `h1`, carrying `tabindex="-1"`, whose text is the page name. The divergent-wording problem disappears with the second channel.

**C-8 resolved: yes.** (Mechanism verified — focus movement and mutation counts.
Actual spoken output is under NOT TESTED; no screen reader was run.)

## F — TIMELINE BAR INK (AC19) · **PASS, worst 4.61**

Measured with the same glyph-pixel diff technique as section C, which is the only
way to reach the `linear-gradient` fill used for living painters. `.tl2-wrap`
scrolled through **7 positions** across its 4 740 px width, both themes.

| | round 1 | round 2 dark | round 2 light |
| --- | --- | --- | --- |
| distinct painters sampled | ~30 failing pairs | **156** | **156** |
| worst observed | **2.42** (`#f6f1e6` on `#d9886e`) | **4.61** ("Giorgione") | **4.61** ("Giorgione") |
| below 4.5 | ~30 | **0** | **0** |
| below 3.0 | several | **0** | **0** |

Worst pair: ink `rgb(246,241,230)` over backdrop `rgb(181,77,29)`. Matisse's worst
*computed* result was 4.58; **observed 4.61**, consistent with the implementation's
own `BAR_AA = 4.6` target and its ≤0.039 HSL-L nudge. Identical in both themes,
as expected — the ink is derived from the fixed swatch palette, not from the theme.

## G — REGRESSION SPOT-CHECK · **CLEAN**

26 routes visited in one document with `console.error`/`console.warn`/`onerror`/
`unhandledrejection` instrumented in-page **and** CDP `Log.entryAdded` /
`Runtime.consoleAPICalled` / `Runtime.exceptionThrown` collected out-of-page.

| measure | result |
| --- | --- |
| console errors (in-page) | **0** |
| console warnings (in-page) | **0** |
| CDP error/warning log entries | **0** |
| HTTP responses ≥ 400 | **0** |
| broken images | **0** of **680** checked across the 26 routes |
| total resource entries | 117 |

**External hosts contacted automatically — complete list:**

| host | requests |
| --- | --- |
| `localhost:8421` | 38 |
| `upload.wikimedia.org` | 79 |

- **`fonts.googleapis.com` — 0 requests. `fonts.gstatic.com` — 0 requests.** Still confirmed at runtime after the token work.
- No host other than `upload.wikimedia.org` is contacted automatically.

Photo credits still render, all four parts present, no raw-HTML leakage:

| page | credit |
| --- | --- |
| `#/museum/louvre` | `Photograph: Benh LIEU SONG (Flickr) · CC BY-SA 3.0 · file on Commons` |
| `#/artwork/david` | `Image credit: Jörg Bittner Unna · CC BY 3.0 · file on Commons` |

Note on coverage: this sweep produced 117 resource entries against round 1's 373,
because it navigated by hash inside one document with shorter dwell times. The
host list and the zero-failure counts are sound; it is a *lighter* sweep than
round 1, not a broader one.

## FINDINGS

Severity: **P1** = blocks the criterion · **P2** = criterion met but with a real
defect · **P3** = observation.

### V2-1 — dark home hero fails AA over the generative cover · AC19 · **P1**

Worst of 8 covers: `h1.home-title` **1.10** (floor 3.0), `p.lede` **1.97**,
`p.footer-note` **1.74**, `a` **4.09**, `div.kicker` **4.05** (floor 4.5).
`.hero-shade` in dark is still `rgba(var(--bg-rgb),.25)` at the ellipse centre
(`styles.css:746`) over a **full-opacity** in-hero cover canvas. Unit 25d scoped
its scrim and its ink lift to light only. Not a unit-25 regression — a
pre-existing defect that round 1 measured on the wrong layer and cleared at 6.20.
Evidence: `contrast-audit.py` pass 3, `hero-composite.json`,
`home__desktop-1440x900__dark.png`.

### V2-2 — light hero title clears its floor by 0.06, on a surface that changes every visit · AC19 · **P2**

3.06 observed vs a 3.0 floor and a 3.23 predicted bound. The bound was computed
against `#bg-canvas` at opacity .6; the operative layer is the in-hero cover
canvas at opacity 1. The criterion is met on every cover I drew, but the margin
is not established for covers I did not draw.

### V2-3 — `--gold` still used as small text in four light-theme places · AC19 · **P2**

| selector | ratio | need | route |
| --- | --- | --- | --- |
| `div.lc-kicker` (×120) | 3.71 | 4.5 | `#/lists`, `#/list/<id>` |
| `span.le-num` (×10) | 3.40 | 4.5 | `#/list/<id>` |
| `button.tl2-leg-more` | 3.40 | 4.5 | `#/timeline` |
| `div.tl2-year.t.now` | 3.71 | 4.5 | `#/timeline` |

Source lines: `styles.css:1139`, `:1150`, `:985`, `:1000`. The 25b re-pointing
missed them. Tokens themselves are correct — these are call sites.

### V2-4 — unit 25e's `flex-wrap:wrap` regresses the 390 px header · AC18 / AC23 · **P2** · **NEW**

`.main-nav` gets `flex:1`, i.e. `flex-basis: 0%`, which **overrides the
`width:100%` the ≤820 px rule sets** (`styles.css:1116`). The nav box is therefore
only **97 px wide** at 390 px. Adding `flex-wrap:wrap` for the desktop zoom fix
turned that narrow box from one scrolling row into eight stacked ones:

| | pre-25 behaviour (`flex-wrap:nowrap`) | shipped (`flex-wrap:wrap`) |
| --- | --- | --- |
| nav box | 97 × **35** | 97 × **291** |
| `.site-header` height | **109 px** | **362 px** — 43 % of an 844 px viewport |
| links fully inside the box | 1 of 8 | 6 of 8 |
| links overflowing the box | 7 (scrollable, mask-faded) | **2** |

Both states were measured in the same live page by toggling only `flex-wrap`, so
the comparison isolates the unit-25 change. The `-webkit-mask-image` fade at 78 %
(`styles.css:1117`) was designed as a horizontal-scroll affordance and now fades
the right edge of a vertical stack. Visible in every `*__mobile-390x844__*.png`.
No horizontal overflow results, so AC18's letter holds — but this is a real
composition regression at the primary mobile viewport, and it is the one thing
unit 25 made worse. The underlying `flex:1` vs `width:100%` conflict predates
unit 25; the wrap made it consequential.

### V2-5 — one Escape both closes the listbox and clears the query · AC16 · **P3**

Unchanged from round 1's F-5. Carried forward, not re-measured.

## RESOLVED SINCE ROUND 1

| round 1 finding | round 2 status |
| --- | --- |
| **F-1** 26 routes overflow 115–117 px at 200 % zoom · AC18 | **RESOLVED** — 0 px on 26/26 |
| **F-1** `button.skip-inline` clipped 109 px | **RESOLVED** — focused 492 × 49, lost 0 |
| **F-1** `div.mu-hero` loses 942 px | **WITHDRAWN** — decorative collage, 982 px at 100 % zoom, zero text |
| **F-1** `div.card-tagline` clipped 266 px | **RESOLVED** — absent from the clipped set on all 26 routes |
| **F-2** light hero 2.47 : 1 · AC19 | **RESOLVED** — 3.06, but see V2-2 |
| **F-3** 43 rendered pairs below AA · AC19 | **43 → 5 reported, 2 artifacts, 3 genuine** (+1 off-set) → V2-3 |
| **F-3** ~30 timeline pairs, worst 2.42 | **RESOLVED** — worst 4.61 across 156 painters, both themes |
| **F-4 / C-8** route announced twice · AC15 | **RESOLVED** — 0 live regions, focus only |
| **F-6** `button.skip-inline` unthemed · AC17/AC19 | **RESOLVED** — `--gold2` on `--panel2`, gold border |
| **Evidence defect** 390 px shots are a cropped 500 px layout | **FIXED** — true 390 px, asserted at capture time |

## CARRIED FORWARD FROM ROUND 1 (commit `1214062`) — NOT RE-OBSERVED

The following were **not re-tested in round 2**. Unit 25 changed only CSS colour
tokens, `.main-nav`'s `flex-wrap`, `.skip-inline`'s base rule, the light hero
scrim, and the removal of `#route-status` — none of which touches the storage,
merge, animation or keyboard machinery these results exercise. They are reported
here as **carried forward from round 1, on that reasoning**, and are *not* claims
of fresh observation:

- **AC7 onboarding checkpoint resume — 5 / 5 PASS** (`browser-evidence-build.md`).
- **AC5 / AC6 import conflict UI, and byte-identical cancel** (2578 → 2578 bytes, first differing index −1).
- **AC20 reduced motion** — animations removed, 621 → 0 transitions, no content or control lost.
- **AC17 skip link, influence-graph bypass (204 stops skipped), focus ring, Enter activation.**
- **AC16 search combobox semantics** — every checked APG point, and F-5's single-Escape divergence (now V2-5).

One caveat on carrying the two focus-ring numbers forward: `--gold2` **changed
value in light** (`#8a6a2e` → `#81632b`), so round 1's light ring figure of 4.65
is stale. I recomputed it from the live cascade rather than re-measuring under a
real Tab: `circle.ig-ring` takes `--gold2` (`styles.css:1045`), giving **5.18 : 1**
against the graph panel — still above the 3.0 UI floor. The skip-link outline
takes `--gold`: **7.40** dark, **3.31** light. Both are cascade-derived, not
observed under `:focus-visible` this round.

## NOT TESTED

1. **Real assistive-technology output.** Section E measures focus movement and live-region mutations — the mechanism. VoiceOver / NVDA were not run, so the spoken result is unverified.
2. **Space-key activation of custom controls.** Carried forward from round 1: the browser tooling could not emit a space key. Enter passes. Space remains untested — not assumed to pass, not reported as failing.
3. **`:focus-visible` focus indicators under a real Tab, this round.** Round 1 observed them; round 2 only recomputed the colours from the cascade after the token change (see above).
4. **AC19 for text over artwork photographs.** The generative covers were pixel-sampled. Text over `upload.wikimedia.org` photographs was not: those canvases are cross-origin-tainted and `getImageData()` throws. The screenshot-diff method used here could reach them; it was not run against them.
5. **768 px and 1280 px screenshots.** 1280 was captured at 200 % zoom only. 768 was neither measured nor captured this round.
6. **The five widths (320/390/768/1280/1440) overflow sweep.** Round 1 measured 130/130 clean. Round 2 re-measured 390 and 1440 (as part of A, 0 overflow on all 64 captures) and 1270/1280 at 200 % zoom. **320 and 768 were not re-measured.**
7. **Hero contrast on covers I did not draw.** 8 covers per theme; the generator is not exhaustively characterised.
8. **Storage-failure UX (AC8), the full 18 ARIA control types (AC16), the 24-query search fixture (AC21), Explore alignment (AC22), the relationship journey (AC24).** Outside my brief; no evidence collected, no opinion offered.
9. **Real touch input on a physical device.** Mobile viewports are CSS-pixel emulation with `mobile:false`; no touch, no device pixel ratio other than 1.

## SUMMARY

| Criterion | Round 1 | Round 2 |
| --- | --- | --- |
| AC15 route orientation (C-8) | PASS with defect F-4 | **PASS** — single channel |
| AC18 responsive overflow @200 % zoom | **FAIL** 26/26 routes | **PASS** 0/26 routes |
| AC18 mobile header composition @390 | not adjudicable (bad evidence) | **PASS with defect V2-4** |
| AC19 token contrast | FAIL | **PASS** — all body tokens clear AA |
| AC19 rendered pairs | FAIL (43) | **3 genuine failures** → V2-3 |
| AC19 timeline bar ink | FAIL (worst 2.42) | **PASS** (worst 4.61) |
| AC19 hero, light | **FAIL** 2.47 | **PASS** 3.06 (margin 0.06) |
| AC19 hero, dark | reported PASS 6.20 (wrong layer) | **FAIL** 1.10 → V2-1 |
| AC25 third-party requests | PASS | **PASS** — zero Google Fonts |
| AC26 route sweep | PASS | **PASS** — 0 errors, 0 warnings, 0 failures |
| Mobile screenshot evidence | **defective** | **sound** — asserted at capture time |

**Open against Gate 2: V2-1 (P1), V2-3 (P2), V2-4 (P2), V2-2 (P2).**
