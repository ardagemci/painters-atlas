# PIG-001 — Unit 28 build log (F-27-2 / AC19: text over the generative `#bg-canvas`)

**Implementer:** Dürer (`claude-implementation-lead`) · branch `pig-001-stabilization`
(verified: **not** `main`; no push, no merge, no deploy) · Gate 1 satisfied
(`specification.md` at `approved_for_build`).

Unit 28 takes the finding unit 27 raised against itself and routed rather than absorbed
(`build-log-unit-27.md` §4 F-27-2): text that paints over the site-wide generative
`#bg-canvas` and measures below the 4.5 body floor. Every number below was measured by me
against the committed CSS. Where a number is a **bound** derived from the canvas rather
than an observation, it says so. Where a cell was **not measured**, it says that too.

## Commit

| Commit | Finding | Files |
| --- | --- | --- |
| `3e24e4a` | F-27-2 · AC19 | `css/styles.css`, `index.html` |

`?v=` bumped `20260726-pig001-u27` → `20260728-pig001-u28` on the stylesheet.
**`js/app.js` was not touched**; its `?v=` is unchanged. No new dependencies, no build
step. Committed by explicit path; `THEORY_001.md`,
`protocol/tasks/PIG-001/CHALLENGE_001` and `protocol/tasks/PIG-001/THEORY_001` were left
untracked and untouched. **Unit 27's museum-band work was not touched** — it passes and is
certified evidence.

---

## 1 — What changed, and one correction to the routing note

| selector | before | after |
| --- | --- | --- |
| `.sec-title .count` | `--faint` | **`--muted`** |
| `.img-credit` | `--muted` | **`--body-ink`** |
| `.img-credit a` | `--muted` | **`--body-ink`** |

**The routing note was wrong about `.img-credit`, and I checked rather than assumed.**
F-27-2 recorded both call sites as `--faint`. `grep` says otherwise: `.img-credit` has been
`--muted` since it was written, with a comment saying so explicitly ("`--muted`, not
`--faint`"). So the instructed one-rung lift was already spent on it, and the measured
shortfall is a shortfall **of `--muted` itself**, not of `--faint`.

`--muted` reaches only **4.18** against 4.5 on the base `.mu-credit` actually sits on, so
`.img-credit` takes the next rung, `--body-ink` (**5.85** on that same base). That is not a
new token and not a scrim: it is the remedy unit 26a applied to
`.home-hero-content .footer-note a`, and it is the rung `.bio-block p` (specificity `0,1,1`
over `.img-credit`'s `0,1,0`) **already gives this exact line in artist bios today**. Its
links move with it and keep their underline, which is where their affordance already lived.

---

## 2 — Instruments, and why three of them

The `Math.random` seed means a single draw is not a verdict — my own words in unit 27, and
the first thing this pass had to design around. It is also not enough to sample the draw:
an element's score depends on **where the element happens to sit** relative to a blob, so a
per-element sample is a lottery twice over. Three instruments, each covering the others'
blind spot. All under `evidence/harness/durer-u28/`.

| | instrument | what it settles |
| --- | --- | --- |
| 1 | `canvastext.py` — **three-shot glyph diff** | the measurement of record: real rendered glyph pixels |
| 2 | `enumerate_overcanvas.py` — **cascade enumerator** | *which* elements are in this class, exhaustively |
| 3 | `canvasextremes.py` — **exact canvas model** | the worst backdrop the canvas can present, at any position |

### The phantom-box lesson is built into instrument 1, not remembered alongside it

Unit 27's F-27-2 correction was that `getBoundingClientRect()` reports boxes that are
clipped away and never painted (`.mu-collage` row 2 under `.mu-hero{overflow:hidden}`), so
**a rect test proves nothing about what is behind a glyph.** Accordingly, membership in this
class is never decided by geometry here. Each band takes three shots — A as rendered, B with
glyphs transparent, C with glyphs transparent *and* `#bg-canvas` `display:none` — and an
element counts as over the canvas **only if its own glyph pixels change between B and C**
(`canvasDelta > 0`). That is the A/B unit 27 used to settle the question, promoted from a
one-off diagnostic into the detector itself. Shot B makes glyphs transparent rather than
hidden (Vermeer's correction, inherited).

Two instrument defects found and fixed during this pass, both of which would have produced
false numbers:

- **`background-clip:text` elements score against themselves.** Transparent text does not
  remove ink that is painted as a *background* seen through the glyphs, so shot B still
  showed the gradient and `h1.home-title` came back at **1.00**. Those elements, and only
  those, now have `background-image:none` in shot B as well.
- **A drifting canvas invalidates the diff.** The three shots are seconds apart and the
  blobs animate. `prefers-reduced-motion: reduce` is emulated so the canvas paints one
  static frame at `t=0` and stops. Randomisation is untouched — every blob and ribbon
  phase, radius, amplitude and frequency is still `Math.random`, so `t=0` draws span the
  same distribution the animation passes through.

### Why a model at all

`#bg-canvas` paints gradients and strokes only, so — unlike the museum photographs —
it is **not cross-origin tainted and `getImageData()` works on it**. Instrument 3 therefore
reads the canvas exactly, at its backing resolution, and returns its own (colour, alpha)
pairs so they can be composited over whatever base a given element really sits on. Bucket
quantisation is expanded to its worst corner (alpha rounded **up**), so it can only
overstate the canvas, never understate it.

**The model is corroborated against an independent observation from another session.**
Composited over the base `canvastext.py` measures under `.mu-credit` (`[234,227,213]`, not
`--bg`), it puts `--muted` at **4.18** — reproducing unit 27's separately-instrumented
`p.img-credit.mu-credit` figure of 4.18 to the second decimal. Different instrument,
different session, same number.

### Draws sampled — stated honestly

| run | draws |
| --- | --- |
| canvas model (instrument 3), each theme @1440 | **24** |
| pixel AFTER, each of the four theme × viewport cells | **4** |
| pixel BEFORE, dark 1440 / light 1440 / light 390 | **6** each |
| pixel BEFORE, **dark 390** | **0 — not measured** (see §6) |

Each draw is one page load behind a unique query string. Instrument 1's mutations are
inline-style only and are reverted, so one load — one draw — serves every scroll band of a
route; reloading between bands would have re-seeded the canvas mid-route and made "a draw"
meaningless.

---

## 3 — Measured before → after, per class × theme × viewport

Real rendered glyph pixels, floor **4.5** (both classes are body text). BEFORE for
dark 1440 / light 390 was taken with the shipped declarations restored at runtime
(`U28_BEFORE=1`) so before and after are the same build, same instrument, same operator;
light 1440 BEFORE was taken against the shipped CSS before any edit.

### `.sec-title .count` — `--faint` → `--muted`

| viewport | theme | BEFORE | AFTER | verdict |
| --- | --- | --- | --- | --- |
| 1440×900 | dark | **4.34 FAIL** (6 draws) | **5.67** (4 draws) | **PASS** |
| 1440×900 | light | **3.59 FAIL** (6 draws) | **5.09** (4 draws) | **PASS** |
| 390×844 | dark | not measured by me; unit 27 prior 4.13, model bound 3.69 | **not observed over a canvas pixel** — see note | — |
| 390×844 | light | unit 27 prior 3.39 FAIL, model bound 3.22 | **not observed over a canvas pixel** — see note | — |

**Note on the two 390 cells, stated rather than glossed.** `.sec-title .count` *does*
render at 390 on `#/` and `#/credits` and *does* carry the new token (probed directly:
`rgb(155,147,127)`). But across 4 draws × 9 scroll bands it never landed on a pixel where
the canvas had non-zero alpha, so the detector — correctly — refused to score it, and
**I have no AFTER observation for this class at 390.** What covers those cells is the
token-level number: the same `--muted` ink at the same floor measures **4.47 dark /
4.86 light** at 390 on `p.page-lede` (§4). That is a weaker claim than a direct
observation and I am not dressing it up as one.

### `p.img-credit.mu-credit` — `--muted` → `--body-ink`

| viewport | theme | BEFORE | AFTER | verdict |
| --- | --- | --- | --- | --- |
| 1440×900 | dark | 5.64 pass (6 draws) | **11.43** (4 draws) | **PASS** |
| 1440×900 | light | 4.70 observed (6 draws); **4.18 FAIL** by model + unit 27 | **6.64** (4 draws) | **PASS** |
| 390×844 | dark | not measured by me | **10.73** (4 draws) | **PASS** |
| 390×844 | light | 4.62 observed (6 draws); **4.18 FAIL** by model + unit 27 | **6.04** (4 draws) | **PASS** |

The light BEFORE cells are the honest awkward case: my own 6-draw sample never caught this
element below 4.5 (4.62 / 4.70), while the exact canvas model and unit 27's independent
instrument both put it at **4.18**. I treat it as failing, because a sample that fails to
find the worst case is not evidence that the worst case does not exist — which is the whole
reason this class was routed as its own unit.

`span.img-credit` (the `#/credits` list) moved 5.40 → **11.36** dark 1440 and
4.86 → **6.38** light 1440 on the same change.

---

## 4 — The deliberate sweep

Unit 27 found this class by accident. This is the deliberate look, and it did not come back
clean.

### Coverage — what was and was not swept

- **Enumerator (instrument 2):** 19 routes, **light theme @1440 only**. 3 755 text elements
  scanned; **1 346 paint over `#bg-canvas`**; **67 distinct (ink × size × weight) groups**.
  Not run for dark, not run at 390.
- **Pixel sweep (instrument 1):** 6 routes, ≤5 scroll bands each, 4–6 draws, both themes,
  both viewports, filtered to the `--faint` / `--muted` / `--body-ink` / `--gold2` inks.
- **Canvas model (instrument 3):** both themes @1440, 24 draws, whole-surface — this one is
  position-complete and is what the site-wide claims below rest on.

### Found below floor, and **not fixed** in this unit

| theme | viewport | class | ink | measured | floor |
| --- | --- | --- | --- | --- | --- |
| light | 390 | `div.chip-label` | `--faint` | **3.45** | 4.5 |
| light | 390 | `a` (global link) | `--gold2` | **3.49** | 4.5 |
| light | 1440 | `div.page-kicker` | `--gold2` | **3.53** | 4.5 |
| light | 1440 | `a` (global link) | `--gold2` | **3.64** | 4.5 |
| light | 1440 | `div.chip-label` | `--faint` | **3.72** | 4.5 |
| light | 390 | `div.page-kicker` | `--gold2` | **3.77** | 4.5 |
| light | 390 | `a.active` | `--gold2` | **4.47** | 4.5 |
| dark | 1440 | `div.chip-label` | `--faint` | **4.39** | 4.5 |
| dark | 390 | **`p.page-lede`** | **`--muted`** | **4.47** | 4.5 |

And the model's whole-surface bound over 24 draws, on the plain `--bg` base:

| theme | `--faint` | `--muted` | `--gold2` | `--teal` | `--body-ink` | `--ink` |
| --- | --- | --- | --- | --- | --- | --- |
| dark | **3.69** | **4.54** | 8.68 | — | 9.20 | 11.15 |
| light | **3.22** | **4.47** | **3.22** | **3.22** | 6.27 | 8.63 |

**Three things follow, and none of them is "two call sites".**

1. **`--faint` cannot carry small text over this canvas in either theme** (3.69 dark /
   3.22 light). It is not confined to `span.count`: the same token paints `.chip-label`,
   `.f-label`, `.map-hint`, `.daily-return`, `.aw-provenance`, `.footer-note`, `.tl-year`,
   `.tn-count`, `.tm-lab`, `.footer-nav a` and the search placeholder, all over the canvas.
2. **`--gold2` — the global link colour `a{}` — fails in light** (3.22 bound, 3.49–3.64
   measured). Every link on page background is affected. Unit 26c's gold audit and
   Vermeer's §5.4 both cleared these against *flat paint*; nobody had measured them over
   the canvas, because until this unit there was no instrument for it.
3. **`--muted` is itself marginal** (4.54 dark / 4.47 light by bound; 4.47 measured on
   `p.page-lede` at dark 390). So the rung `.sec-title .count` was lifted onto is only just
   adequate, and on the darker bases some elements sit on it is not.

### Why I did not fix them here

- **Scope.** This unit was scoped to two call sites. Items 1–3 are a site-wide token and
  link-colour question — `--faint` would effectively cease to exist as a distinct rung —
  which is visual direction (Matisse), not an implementation choice I may make silently.
- **The obvious single lever does not work.** Lowering `#bg-canvas` opacity looks like the
  one-line fix. It is not: `--faint` needs the light backdrop held above L≈0.796 and
  `--gold2` above L≈0.794, against a flat-paper L of 0.842 — i.e. the canvas would have to
  become very nearly invisible, which deletes the generative identity PIGMENT.md exists to
  carry. I checked this before proposing anything, so that the next unit does not spend
  itself discovering it.
- **A one-off patch would be incoherent.** Lifting `.img-credit`'s hover off `--gold2`
  while every other link on the site stays at 3.49 would buy nothing for the criterion and
  obscure the real shape of the problem.

### What would fix it

Two candidates, both token-level and both reversible, for whoever routes this:
**(a)** retire `--faint` as a small-text colour over the canvas (fold it into `--muted`)
and re-point the light link colour `--gold2` to a darker stop — `#6b5122` is already in the
palette from unit 27 and clears comfortably; or **(b)** give the canvas a per-theme
opacity low enough that `--muted` clears, and lift `--faint` and light `--gold2` anyway,
since no achievable opacity rescues those two. **(a)** is the smaller change and matches
the rung-lifting remedy used in units 26a, 27 and here.

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

`osascript -l JavaScript tools/validate.jxa.js` — **zero warnings**, re-run after the last
edit. Unit 28 is CSS-only and touches no data, so no validator movement was expected and
none occurred.

**Measurement chains:** every chain this pass started was stopped before the pass ended;
`ps` confirms no `canvastext.py`, `canvasextremes.py`, `enumerate_overcanvas.py` or
`--remote-debugging-port` Chrome remains. Instrument 1 writes run-unique shot paths
(`/tmp/u28-{a,b,c}-<pid>.png`) and each run takes its own CDP port and its own output tag,
so the unit-27 provenance failure (two chains writing the same filenames) cannot recur.

---

## 6 — Deviation ledger (Gate 3)

| # | Deviation | Why | Product intent |
| --- | --- | --- | --- |
| D-28-1 | `.img-credit` went to `--body-ink`, **two** rungs from the routed `--faint`, not one | The routing note's premise was wrong: it was already `--muted`, and `--muted` measures 4.18 on this element's base. One rung from where it actually was **is** `--body-ink` | Preserved. Size and weight still separate the credit from prose, and `.bio-block p` already renders this line at `--body-ink` today |
| D-28-2 | `.img-credit a` moved with its parent | A `--muted` link inside a `--body-ink` line would have been the failing element instead | Preserved; the underline already carried the affordance |
| D-28-3 | `.sec-title .count` shipped on `--muted` although `--muted`'s own bound is 4.47 | Instructed rung, and a strict improvement (3.59 → 5.09 light). Going further would pre-empt the token decision D-28-4 routes | Preserved, and flagged rather than presented as clearance |
| D-28-4 | The site-wide `--faint` / `--gold2` / `--muted` failures were **reported, not fixed** | Visual-direction decision outside this unit's scope; see §4 | Not changed. Escalated to the Synthesis Lead as a finding |
| D-28-5 | Two 390 AFTER cells for `.sec-title .count` rest on a token-level number, not a direct observation | The class never landed on a canvas-painted pixel across 4 draws × 9 bands at 390 | Recorded as a gap in §3, not as a pass |

Nothing was escalated for a paid service, new infrastructure, or a legal judgement.

---

## 7 — Self-assessment against AC19

**AC19** — *"Both themes pass AA for frozen text/control/focus/state pairs including
composites that require browser measurement."*

| sub-claim | verdict | evidence |
| --- | --- | --- |
| Text over Wikimedia photographs (F-V1 / F-5) | PASS, carried | unit 27 §2 — untouched here |
| Focus indicator inside that composite | PASS, carried | unit 27 F-27-3 |
| Home hero over the generative cover (unit 26a) | PASS, carried | Vermeer §5.1 |
| **`.sec-title .count` over `#bg-canvas`** | **PASS at 1440 both themes**; 390 not directly observed | §3 — 4.34→5.67 dark, 3.59→5.09 light |
| **`.img-credit` / `.mu-credit` over `#bg-canvas`** | **PASS, both themes, both viewports** | §3 — worst AFTER 6.04 (light 390) against 4.5 |
| **`--faint` small text over `#bg-canvas`, site-wide** | **FAIL — open** | §4 — 3.45–4.39 measured; 3.69/3.22 bound |
| **`--gold2` links over `#bg-canvas` in light** | **FAIL — open** | §4 — 3.49–3.64 measured; 3.22 bound |
| **`--muted` small text over `#bg-canvas`** | **MARGINAL FAIL** | §4 — 4.47 measured (`p.page-lede`, dark 390); 4.54/4.47 bound |

### The sentence Van Eyck certifies against

**AC19 is NOT fully supported.** The two call sites F-27-2 named are closed and measured,
and the museum-band composite from unit 27 is untouched and still passes — but the
deliberate sweep this unit was asked to run found the same defect in a much wider class
than the routing note described: `--faint` small text and, in the light theme, the global
`--gold2` link colour both fall below 4.5 wherever they paint over `#bg-canvas`, and
`--muted` itself measures 4.47. These are **pre-existing** (they predate units 25–28 and
were never measured because no instrument for this composite existed until now) and they
are **not regressions introduced here**, but they are live AC19 failures and I am not
reporting this unit as closing the criterion. §4 states what would close it.

## 8 — Not tested

1. **Browsers other than Chrome.** Chrome headless only.
2. **Real assistive technology.** Pixels and cascade, not spoken output.
3. **Device pixel ratio ≠ 1, real touch input.** All synthetic at `deviceScaleFactor: 1`.
4. **The enumerator in dark, or at 390.** Run in light @1440 only; the site-wide claims
   rest on the canvas model, which *is* run for both themes.
5. **Viewports other than 1440×900 and 390×844**; the frozen set also names 320 / 768 /
   1280 and 200 % zoom.
6. **`.sec-title .count` AFTER at 390 over a canvas-painted pixel** — see §3.
7. **Hover and focus states of the changed links** were not re-measured; `.img-credit
   a:hover` remains `--gold2` and is inside the open §4 failure.

## 9 — Preview

```
git checkout pig-001-stabilization      # at 3e24e4a
python3 -m http.server 8421 -d .
open http://localhost:8421/#/credits        # span.count + span.img-credit
open http://localhost:8421/#/museum/louvre  # p.img-credit.mu-credit
```
Toggle the theme with the header control; both changes are per-token and identical in each.
