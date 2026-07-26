# PIG-001 — Unit 27 build log (F-V1 / AC19: text over Wikimedia photographs)

**Implementer:** Dürer (`claude-implementation-lead`) · branch `pig-001-stabilization`
(verified: **not** `main`; no push, no merge, no deploy) · Gate 1 satisfied
(`specification.md` at `approved_for_build`).

Unit 27 closes **F-V1**, the last criterion-failing finding from Vermeer's closing pass
(`evidence/browser-evidence-closing.md` §1, §6) and Van Eyck's **F-5**
(`quality-review.md`). Every number below was measured by me in a real browser at the
committed CSS. Where a number is a bound derived from the cascade rather than an
observation, it says so.

## Commit

| Commit | Finding | Files |
| --- | --- | --- |
| `563f0af` | F-V1 (major, criterion-failing) · AC19 | `css/styles.css`, `index.html` |

`?v=` bumped `20260726-pig001-u26c` → `20260726-pig001-u27` on the stylesheet.
**`js/app.js` was not touched**; its `?v=` is unchanged. No new dependencies, no build
step. Committed by explicit path; `THEORY_001.md`,
`protocol/tasks/PIG-001/CHALLENGE_001` and `protocol/tasks/PIG-001/THEORY_001` were left
untracked and untouched.

## Environment

| | |
| --- | --- |
| Serve | `python3 -m http.server 8421 -d .` (repo root) |
| Browser | Google Chrome, headless, driven over the DevTools Protocol |
| Viewports | `Emulation.setDeviceMetricsOverride` — never `--window-size`, which this Mac clamps to 500 px |
| Cache | `Network.setCacheDisabled=true`; every route a fresh document behind a unique query string |
| Harness | `evidence/harness/durer-u27/{mu,table,ring2,bgcanvas,probe_outband}.py`, thin drivers over Vermeer's `harness/vermeer-closing/photos.py` + `harness/cdp-r2/{cdp,png}.py`. Raw results: `harness/durer-u27/mu-*.json`, `ring2-*.json`, `log2-*.txt` |

**Cross-origin caveat.** `canvas.getImageData()` throws on a canvas tainted by
`upload.wikimedia.org`. This harness never calls it — it reuses Vermeer's corrected
two-shot glyph diff: CDP captures composited pixels as a PNG decoded locally in pure
Python, so same-origin policy never applies. Shot B makes glyphs transparent
(`color:transparent` + `-webkit-text-fill-color:transparent`) rather than hiding the
element, which is the fix Vermeer made mid-pass after `visibility:hidden` deleted an
element's own background and produced a false 2.38:1. I inherited the corrected
instrument and did not rebuild it.

**Instrument corroborated against its author.** My BEFORE run reproduces Vermeer's
independent closing sweep on the shipped CSS to the second decimal — `a` 1.33,
`span.sep` 1.31, `div.mu-sub` 3.23. Same instrument, same numbers, different operator.

---

## 1 — The mechanism

### Root cause, re-confirmed before fixing

Vermeer's diagnosis is correct and I reproduced it rather than accepting it.
`.mu-shade` ramped its alpha as a percentage of **`.mu-hero`'s** height, but the text
block `.mu-hero-body` is bottom-anchored and its own height varies with the venue name
(one line or two), the presence of a hook and the presence of a founding year. So the
*same element* landed at a different scrim alpha on every venue — `.37–.51` where it
needed `.864`.

### What changed

Reuses the mechanism established for the home hero in units 25d/26a — **one geometry, a
per-theme token** (`.hero-shade` + `--hero-veil`) — rather than inventing a third
pattern, per Matisse's direction.

| | before | after |
| --- | --- | --- |
| `.mu-shade` | `linear-gradient(180deg, rgba(bg,.18), rgba(bg,.94) 80%)` | `linear-gradient(180deg, rgba(bg,.06), rgba(bg,.30))` — a light tie only; it carries **no** contrast duty |
| `.mu-hero-body` | no background | `linear-gradient(180deg, rgba(bg,0) 0, rgba(bg,--mu-veil) 18px, rgba(bg,--mu-veil) 100%)` |
| `--mu-veil` | — | **`.88`** in both themes |

The veil sits on the **text block**, not the hero box. That is the whole point: anchored
there, every glyph in the band sits at exactly `--mu-veil` on all 104 venues at every
viewport, and the photograph keeps its full presence everywhere the text is not — more of
it than the old `.94`-at-80 % ramp left. The 18 px feather is shorter than the smallest
top padding in the band (22 px at ≤700 px), so no glyph can fall inside the ramp.

### Why .88, verified independently

`.88` is a **bound**, not a sample: it is computed against a worst-case *fully opaque*
photograph pixel (white where the ink is light, black where the ink is dark), the standard
Matisse set and unit 26 met for the home hero. I re-derived every figure rather than
inheriting Vermeer's:

| theme | element | ink | floor | min alpha required | at `.88` |
| --- | --- | --- | --- | --- | --- |
| dark | `--ink` `h1.display` | `#ece6d9` | 3.0 | .506 | 11.66 |
| dark | `--body-ink` crumb link | `#d8d2c4` | 4.5 | .675 | 9.63 |
| dark | **`--muted`** `.mu-sub` + crumbs | `#9b937f` | 4.5 | **.864** | **4.75** |
| dark | `--gold2` `.mu-hook` | `#e8c98a` | 4.5 | .690 | 9.08 |
| light | `--ink` `h1.display` | `#2b2620` | 3.0 | .471 | 9.72 |
| light | `--body-ink` crumb link | `#433c31` | 4.5 | .705 | 7.06 |
| light | **`--muted`** `.mu-sub` + crumbs | `#585244` | 4.5 | **.834** | **5.03** |
| light | `--gold2` **as shipped** | `#81632b` | 4.5 | **.975** | 3.63 ✗ |
| light | band gold `#6b5122` | `#6b5122` | 4.5 | .851 | **4.82** |

`.864` dark and `.834` light are the binding constraints; `.88` clears both. One value
serves both themes, so the band's geometry is identical in each — only the token is
per-theme.

### Two colours no usable veil can carry

Both go up one rung **inside the band only**, which is exactly the remedy unit 26a used
for the light home hero:

- **Breadcrumbs off `--faint`.** `--faint` needs `.932` dark / `.975` light — an opaque
  band. In the band they take the rung the artist hero already takes over its cover:
  `--muted` for the current crumb and separators, `--body-ink` for links. Outside the
  band `.breadcrumbs` keeps `--faint` on opaque page paint, unchanged.
- **Light `--gold2` → `#6b5122`.** `#81632b` needs `.975`. `#6b5122` is the light
  home-hero title's darker stop — not a new colour — and clears at 4.82; its hover takes
  `#4a3616` (7.44), that gradient's darkest stop, because the global `a:hover{color:#fff}`
  would otherwise paint white on warm paper here. **Dark's `--gold2` needs only `.690`
  and is left alone.**

### Photograph presence

Brief constraint: hit the bound, do not over-darken decoratively. `.mu-shade` was
*reduced* from a ramp reaching `.94` to a flat `.06→.30`; the veil is confined to the
text block's own height. Confirmed by eye at
`evidence/u27-museum-{louvre,k20-dusseldorf,moderna-museet}__{desktop-1440x900,mobile-390x844}__{dark,light}.png`
— the Kandinsky behind K20 and the Louvre collage read clearly above the text block in
both themes, and Van Eyck's named failure ("K20 runs straight across a saturated
Kandinsky", "the Met breadcrumb is invisible") is gone.

---

## 2 — Measured before → after, per class × theme × viewport

Real rendered glyph pixels. **BEFORE** = the shipped rules restored at runtime by the same
instrument on the same build (`U27_BEFORE=1`), over the 15 adversarial venues that
produced the worst numbers in Vermeer's closing sweep. **AFTER** = the full 104-venue
sweep, reported both restricted to those same 15 and over all 104 (which can only be worse,
never better).

| viewport | theme | class | floor | BEFORE (15) | AFTER (same 15) | **AFTER (all 104)** | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1440×900 | dark | `span` (crumb current) | 4.5 | 1.18 FAIL | 4.98 | **4.95** | **PASS** |
| 1440×900 | dark | `span.sep` | 4.5 | 1.31 FAIL | 5.09 | **5.06** | **PASS** |
| 1440×900 | dark | `div.mu-sub` | 4.5 | 3.23 FAIL | 5.08 | **5.08** | **PASS** |
| 1440×900 | dark | `a` (crumb link) | 4.5 | 1.33 FAIL | 10.03 | **10.03** | **PASS** |
| 1440×900 | dark | `div.mu-hook` | 4.5 | 8.98 pass | 9.83 | **9.83** | **PASS** |
| 1440×900 | dark | `button.chip` | 4.5 | 13.24 pass | 12.17 | **12.17** | **PASS** |
| 1440×900 | dark | `h1.display` | 3.0 | 3.97 pass | 12.29 | **12.29** | **PASS** |
| 1440×900 | light | `span` (crumb current) | 4.5 | 1.28 FAIL | 5.15 | **5.15** | **PASS** |
| 1440×900 | light | `span.sep` | 4.5 | 1.40 FAIL | 5.29 | **5.20** | **PASS** |
| 1440×900 | light | `div.mu-sub` | 4.5 | 3.84 FAIL | 5.31 | **5.30** | **PASS** |
| 1440×900 | light | `a` (crumb link) | 4.5 | 1.57 FAIL | 7.29 | **7.29** | **PASS** |
| 1440×900 | light | `div.mu-hook` | 4.5 | 3.60 FAIL | 5.13 | **5.13** | **PASS** |
| 1440×900 | light | `button.chip` | 4.5 | 11.28 pass | 10.54 | **10.47** | **PASS** |
| 1440×900 | light | `h1.display` | 3.0 | 2.88 FAIL | 10.04 | **10.04** | **PASS** |
| **390×844** | dark | `span` (crumb current) | 4.5 | **1.00 FAIL** | 4.88 | **4.82** | **PASS** |
| **390×844** | dark | `span.sep` | 4.5 | **1.00 FAIL** | 4.93 | **4.82** | **PASS** |
| **390×844** | dark | `div.mu-sub` | 4.5 | **1.82 FAIL** | 5.10 | **5.08** | **PASS** |
| **390×844** | dark | `a` (crumb link) | 4.5 | **1.06 FAIL** | 9.90 | **9.77** | **PASS** |
| **390×844** | dark | `div.mu-hook` | 4.5 | 5.20 pass | 9.71 | **9.71** | **PASS** |
| **390×844** | dark | `button.chip` | 4.5 | 13.40 pass | 12.36 | **12.16** | **PASS** |
| **390×844** | dark | `h1.display` | 3.0 | **2.40 FAIL** | 12.15 | **12.15** | **PASS** |
| **390×844** | light | `span` (crumb current) | 4.5 | **1.04 FAIL** | 5.11 | **5.11** | **PASS** |
| **390×844** | light | `span.sep` | 4.5 | **1.25 FAIL** | 5.15 | **5.11** | **PASS** |
| **390×844** | light | `div.mu-sub` | 4.5 | **2.28 FAIL** | 5.25 | **5.25** | **PASS** |
| **390×844** | light | `a` (crumb link) | 4.5 | **1.36 FAIL** | 7.17 | **7.17** | **PASS** |
| **390×844** | light | `div.mu-hook` | 4.5 | **2.54 FAIL** | 5.08 | **5.08** | **PASS** |
| **390×844** | light | `button.chip` | 4.5 | 11.28 pass | 10.54 | **10.47** | **PASS** |
| **390×844** | light | `h1.display` | 3.0 | **2.52 FAIL** | 9.99 | **9.97** | **PASS** |

### Exhaustive count, not just worst-per-class

| sweep | band measurements | venues | **below floor** |
| --- | --- | --- | --- |
| 1440×900 dark | 936 | 104 | **0** |
| 1440×900 light | 936 | 104 | **0** |
| 390×844 dark | 936 | 104 | **0** |
| 390×844 light | 936 | 104 | **0** |

**3 744 band measurements across 416 venue-loads. Zero below floor.** No venue was
unrecoverable in any sweep.

### 390 px did not inherit — Vermeer was right to demand it

His NOT TESTED #4 said the mobile numbers "are neither inherited nor assumed" because the
failing mechanism was height-dependent. That was correct, and 390 px was **worse** than
1440: the crumbs bottomed out at **1.00** in both themes, and `h1.display` **failed its
3.0 floor** at 390 (2.40 dark / 2.52 light) while passing at 1440 dark (3.97). Had this
unit measured only 1440 it would have shipped a mobile large-text failure.

The reason one value fixes both viewports is structural, not lucky: the veil is anchored
to the text block, so it is independent of hero height, and hero height is the only thing
that differed between the two viewports.

### The focus indicator inside the veil

`#app h1:focus-visible{outline:2px solid var(--gold); outline-offset:5px}` is the one
control indicator that paints **inside** the new veil. Measured with `:focus-visible`
forced on via `CSS.forcePseudoState` (see §4 for why the first attempt was discarded),
against the worst veiled backdrop measured under `h1.display` by the glyph sweep:

| viewport | theme | ring resolves to | backdrop (measured) | ratio | floor (1.4.11) | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| 1440×900 | dark | `--gold` `rgb(201,164,92)` | `[39,37,34]` | **6.51** | 3.0 | PASS |
| 1440×900 | light | `#6b5122` `rgb(107,81,34)` | `[216,211,199]` | **4.98** | 3.0 | PASS |
| 390×844 | dark | `--gold` `rgb(201,164,92)` | `[39,38,37]` | **6.44** | 3.0 | PASS |
| 390×844 | light | `#6b5122` `rgb(107,81,34)` | `[216,210,199]` | **4.94** | 3.0 | PASS |

---

## 3 — Validator

```
app.js: syntax OK
artists: 256, movements: 76, techniques: 39, eras: 8, nations: 37, painter styles: 27,
influence edges: 238, venues: 116, catalog: 323 (tier1: 76), daily pool: 75,
museum notes: 104, photo credits: 104 (attribution required: 88),
artwork image credits: 27, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```

`osascript -l JavaScript tools/validate.jxa.js` — **zero warnings**, re-run after the last
edit. Unit 27 is CSS-only and touches no data, so no validator movement was expected and
none occurred.

---

## 4 — Findings

### F-27-1 (method, important) · An orphaned duplicate chain created provenance ambiguity

A measurement chain from the **previous** unit-27 pass (`sh /tmp/u27-all.sh`, started
19:28, orphaned to PID 1 when that session ended) was **still running six hours later**,
and it wrote the *same* `mu-<tag>.json` filenames this pass writes. For roughly six
minutes two chains measured the same venues concurrently.

Pixel cross-talk was never possible — `mu.py` gives each process its own shot paths
(itself a fix from the earlier pass, after a shared `/tmp` path produced a dark-theme
backdrop the veil makes arithmetically impossible) and each browser its own CDP port.
What *was* compromised is knowing **which CSS state produced which file**: two late edits
to `styles.css` landed while those runs were in flight.

**I did not trust the mixed files.** Both chains were stopped and everything ambiguous was
re-measured serially, one process at a time, against the final committed CSS
(`harness/durer-u27/runall2.sh`, logs `log2-*.txt`). The two 104-venue 1440 sweeps were
retained rather than repeated, but **not on assertion** — the 15 adversarial venues were
re-measured at 1440 against the final CSS and reproduce the retained sweep to the second
decimal in both themes and all seven classes (dark: 4.98 / 5.09 / 5.08 / 10.03 / 9.83 /
12.17 / 12.29; light: 5.15 / 5.29 / 5.31 / 7.29 / 5.13 / 10.54 / 10.04).

**For future passes:** a long harness chain must be launched so it dies with its session,
or must write to a run-unique output path. This one nearly put numbers of unknown
provenance into a certification package.

### F-27-2 (method, correction) · `.mu-collage.c4` phantom boxes — a detection artefact, not an AC19 failure

The over-approximate detector flags any text element whose rect intersects the rect of an
`<img>` from `upload.wikimedia.org`. On museum pages it flagged `span.count`,
`p.img-credit.mu-credit` and `h2.sec-title`, which are in **normal flow below the hero**
and read backdrops that are not flat page paint. That looked like an out-of-band
photograph composite. **It is not.**

`.mu-collage` is a grid whose intrinsic height exceeds `.mu-hero`, and `.mu-hero` has
`overflow:hidden`. The lower row is **clipped away and never painted** — but
`getBoundingClientRect()` still reports its full box far down the page. Measured at
`#/museum/tate-britain`, 1440×900, dark:

| | value |
| --- | --- |
| `.mu-hero` rect | `[128, 102, 1184, 340]` → bottom edge **442** |
| `.mu-hero` `overflow` | `hidden` |
| collage imgs 1–2 | `[129,103,590,439]`, `[721,103,590,439]` — `centreInsideHero: true`, element at centre `div.mu-sub` |
| collage imgs 3–4 | `[129,**544**,590,441]`, `[721,544,590,441]` — `centreInsideHero: **false**`, element at centre **`div.cards`** |

`document.elementsFromPoint()` at those glyph coordinates returns **no image at all**.
The same holds at `#/museum/uffizi` light, where imgs 4–6 sit at `y=424` with their
centres resolving to `p` and `main.view-enter`.

What *is* behind them was settled by A/B: measure the same glyph pixels twice, once as
shipped and once with `#bg-canvas` removed (`bgcanvas.py`).

| element | backdrop as shipped | backdrop with `#bg-canvas` removed |
| --- | --- | --- |
| `span.count` (dark) | `[36,25,21]` | **`[13,12,10]`** = `--bg` `#0d0c0a` |
| `h2.sec-title` (dark) | `[36,25,21]` | **`[13,12,10]`** |
| `p.img-credit.mu-credit` (dark) | `[19,23,22]` | **`[12,11,10]`** |
| `p.img-credit.mu-credit` (light) | `[200,203,192]` | **`[234,227,213]`** |
| `p` `.mu-essay` (light) | `[220,200,188]` | **`[242,236,223]`** = `--bg` `#f2ecdf` |
| **every band element** (`h1.display`, `div.mu-sub`, `div.mu-hook`, `button.chip`, `span`, `span.sep`) | *unchanged* | *unchanged* — the veil is opaque enough that the canvas behind contributes nothing |

**Conclusion:** those elements paint over the site-wide **generative `#bg-canvas`**, not
over a Wikimedia photograph. They are outside F-V1's class. This is a correction to the
**measurement method**, not to the build — and it matters, because a future pass reading
the raw sweep would otherwise report a photograph composite that does not exist.

**Recorded but not fixed, deliberately out of scope** (`span.count` is `--faint` over the
generative canvas, a different composite class from F-V1, and it is a random-draw surface —
the cover is `Math.random`-seeded, so the worst observed value moves between runs):

| viewport | theme | class | worst observed | floor |
| --- | --- | --- | --- | --- |
| 1440×900 | dark | `span.count` | 4.13 | 4.5 |
| 1440×900 | light | `span.count` | 3.52 | 4.5 |
| 1440×900 | light | `p.img-credit.mu-credit` / its `a` | 4.43 / 4.48 | 4.5 |
| 390×844 | light | `span.count` | 3.39 | 4.5 |
| 390×844 | light | `p.img-credit.mu-credit` / its `a` | 4.18 | 4.5 |

It is **pre-existing**: Vermeer's own closing sweep on the shipped CSS records
`span.count` at 4.44 FAIL. Unit 27 does not touch `.sec-title`, `.img-credit` or
`#bg-canvas`. **This is a live AC19 gap outside the museum band and should be routed as
its own finding** — text over the generative canvas is a distinct class from text over a
photograph, and fixing it is a token/veil decision for the whole site, not a museum-band
edit.

### F-27-3 (fixed here) · The band's focus ring, pre-existing and made uniform by the veil

`#app h1:focus-visible{outline:2px solid var(--gold)}` paints **inside** the new veil, so
the veil sets its backdrop. Light's `--gold` `#9e7938` reads **2.60** against the veiled
bound — under the **3.0** non-text floor of WCAG 1.4.11.

**This is not a regression I introduced, and should not be read as one.** Before unit 27
the same ring sat on the raw photograph under a `.37–.51` scrim, where it ranged from
about **1.15** over a dark photograph to a pass over a bright one. The veil did not break
it; the veil made it **deterministic** — the worst case improved from ~1.15 to 2.60, but
2.60 is uniform and still short. Because the veil is what fixed its backdrop, correcting
it belongs to this unit.

Fixed with the band gold this unit already introduced, **scoped to the band**:

```css
html[data-theme="light"] #app .mu-hero-body h1:focus-visible{outline-color:#6b5122}
```

→ **4.98** at 1440, **4.94** at 390. On ordinary light page paint the shipped ring reads
**3.40** and is deliberately left alone; dark needs nothing (**6.51 / 6.44**). The `#app`
id is carried to outrank `#app h1:focus-visible`.

---

## 5 — Deviation ledger (Gate 3)

| # | Deviation | Why | Product intent |
| --- | --- | --- | --- |
| D-27-1 | Breadcrumbs in the band go off `--faint` to `--muted` / `--body-ink` | `--faint` needs `.932` dark / `.975` light — an opaque band, which would erase the photograph the hero exists to show | Preserved. Same remedy unit 26a applied to the light home hero; outside the band `.breadcrumbs` is unchanged |
| D-27-2 | Light `--gold2` in the band → `#6b5122`, hover `#4a3616` | `#81632b` needs `.975`. `#6b5122` is the light home-hero title's darker stop — not a new colour | Preserved. Dark `--gold2` untouched |
| D-27-3 | Band focus ring re-pointed in light only | See F-27-3 | Preserved; band-scoped, global ring untouched |
| D-27-4 | `.mu-shade` reduced from a `.94` ramp to `.06→.30` | The veil now carries all contrast duty; leaving both would darken the photograph past what the floor requires | **Improved** — PIGMENT.md wants the building photo visible, and it now keeps more of itself than before |

No deviation changes product intent. Nothing was escalated to the Synthesis Lead because
nothing required a paid service, new infrastructure, or a legal judgement.

---

## 6 — Self-assessment against AC19

**AC19** — *"Both themes pass AA for frozen text/control/focus/state pairs including
composites that require browser measurement."*

| sub-claim | verdict | evidence |
| --- | --- | --- |
| **Text over Wikimedia photographs (F-V1 / F-5)** | **PASS, both themes, both viewports** | §2 — 3 744 band measurements over 416 venue-loads, 0 below floor; worst `div.mu-sub` 5.08 dark / 5.30 light (1440) and 5.08 / 5.25 (390) against 4.5; worst `h1.display` 12.29 / 10.04 and 12.15 / 9.97 against 3.0 |
| Focus indicator inside that composite | **PASS, both themes, both viewports** | §2, F-27-3 — 6.51 / 4.98 (1440), 6.44 / 4.94 (390) against 3.0 |
| Home hero over the generative cover (unit 26a) | PASS, carried | Vermeer's §5.1 independent re-measurement |
| Six gold-as-small-text sites (unit 26c) | PASS, carried | Vermeer's §5.4 — 12 measurements, 0 failures |
| **Text over the generative `#bg-canvas` outside the band** | **FAIL — open, out of scope, routed** | F-27-2 — `span.count` 3.39–4.13 against 4.5; pre-existing (Vermeer measured 4.44 FAIL on the shipped CSS); a distinct composite class from F-V1 |

**F-V1 is closed. AC19 as a whole is not yet fully supported**, because F-27-2 identifies a
*different* composite class — text over the generative canvas — that is below floor and
that this unit deliberately did not touch. I am stating that plainly rather than reporting
a partial success as a pass: the museum-band photograph composite AC19 named, and that
Van Eyck and Vermeer both flagged, now passes everywhere it is measurable; a
neighbouring class does not.

**What would fix F-27-2**, if it is routed as a unit: `.sec-title .count` and
`.img-credit` are `--faint` over a `#bg-canvas` at `.5` dark / `.6` light. Either lift
those two call sites one rung to `--muted` (which passes on flat page paint in both
themes), or lower the canvas opacity — the first is the smaller, more reversible change
and matches the rung-lifting remedy used in units 26a and 27. It should be measured with
this harness over a spread of random cover draws, since the canvas is `Math.random`-seeded
and the worst draw moves between runs.

## 7 — Not tested

1. **Browsers other than Chrome.** Chrome headless only.
2. **Real assistive technology.** The focus ring was measured as pixels and cascade, not
   spoken output.
3. **Device pixel ratio ≠ 1 and real touch input.** All input synthetic at
   `deviceScaleFactor: 1`.
4. **The 12 unreachable venues.** 116 venues exist; 104 render a page. The other 12 are
   sentinels or carry no catalogued work.
5. **Viewports other than 1440×900 and 390×844** for the band. The frozen set also names
   320 / 768 / 1280 and 200 % zoom; the veil is anchored to the text block and so is
   height-independent, but that is an argument, not a measurement.

## 8 — Preview

```
git checkout pig-001-stabilization      # at 563f0af
python3 -m http.server 8421 -d .
open http://localhost:8421/#/museum/k20-dusseldorf   # and /louvre, /moderna-museet
```
Toggle the theme with the header control; the band's treatment is identical in both.
