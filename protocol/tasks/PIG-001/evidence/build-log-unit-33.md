# BUILD LOG — PIG-001 unit 33 · the correction round

**Author:** Dürer (`claude-implementation-lead`). **Branch:** `pig-001-stabilization`.
**Gate 1:** `protocol/tasks/PIG-001/specification.md` reads
`workflow_state: "approved_for_build"` — verified before any production edit.

**Commits**

| sha | group |
| --- | --- |
| `4f90e96` | **A** — the seven assistive-technology findings |
| `33b97f0` | **B** — the six open AC19 contrast majors, and two of unit 32's residuals |
| `ca72cb8` | **C** — F-1, and the `?v=` bump to `20260805-pig001-u33` |
| `04d3221` | **B follow-up** — every map label after every dot |
| `36bbcb8` | **B follow-up 2** — the graph halo widened to `.46em`, and the label screenshots |

Committed by explicit path. `.gitignore` is modified in the working tree and is
**not mine** — it was already modified when this unit began and is left alone,
as are the untracked `THEORY_001.md`, `passport-test.html`,
`protocol/tasks/PIG-001/CHALLENGE_001` and `protocol/tasks/PIG-001/THEORY_001`.

The three groups touch overlapping files, so the commits were split at hunk
level rather than at file level (`git apply --cached` on filtered patches). The
split is verified lossless: after all four commits the only difference between
the working tree and `HEAD` is the pre-existing `.gitignore` change.

**Validator:** `osascript -l JavaScript tools/validate.jxa.js` → `app.js: syntax
OK`, `ALL REFERENCES VALID`, **zero warnings**, complete count snapshot
unchanged (256 artists · 76 movements · 39 techniques · 8 eras · 37 nations ·
27 painter styles · 238 influence edges · 116 venues · 323 catalog works,
tier 1 = 76 · 75-work daily pool · 104 museum notes · 104 photo credits ·
27 artwork image credits · 15 personas · 12 lists · 36 tier 1 artists/arcs).
No data record was touched by this unit.

---

## 0 — METHOD

### 0.1 What was reused, and from whom

No new measurement technique was invented. The contrast work runs on Vermeer's
unit-32 `sitecensus.py` primitives, imported rather than copied: the four-shot
paint differential (**A** as rendered, **B** the target ink forced transparent,
**C** also `#bg-canvas` `display:none`, **D** also every cover canvas
`visibility:hidden`), the corrected clip origin (`Page.captureScreenshot`'s
`clip` is in page coordinates while `getBoundingClientRect()` is in viewport
coordinates, so `scrollY` is added at capture), the 90 %-in-viewport gate and
the rect-stability guard. Ink is never hidden with `visibility:hidden` or
`display:none`.

`protocol/tasks/PIG-001/evidence/harness/durer-u33/` adds only:

| file | what it is |
| --- | --- |
| `u33.py` | the site table for the findings under repair, `hover=` forced through CDP `CSS.forcePseudoState` (states.py's method inside sitecensus.py's differential), a six-width sweep, and a `LOCATE` variant that can see `::placeholder` |
| `taborder.py` | the real sequential focus order, driven by real `Input.dispatchKeyEvent` Tab presses, not by `focus()` |
| `skiprect.py` | each skip control's rect **at the instant focus lands**, and after its transition settles |
| `overflow.py` | document overflow and the element responsible, ignoring anything inside a deliberately scrollable ancestor |
| `announce.py` | 37 DOM assertions on the announcement work |

### 0.2 Widths, themes, draws

Every contrast figure below is measured over its **actual, differentially
measured backdrop** — never read from the stylesheet — at
**320 / 390 / 900 / 1024 / 1280 / 1440** in **both themes**, with
`prefers-reduced-motion: reduce` emulated so `#bg-canvas` paints one static
`t=0` frame per load. 900 and 1024 are new to the measurement set at the theory
pole's request.

**N = 3 draws** for every after-figure. Unit 32 ran 1 draw and said so; F-8 was
partly missed because one cell of eight passed by chance, and `#bg-canvas` is
`Math.random`-seeded. The before-figures reproduced from the shipped build ran
N = 2 and land on unit 32's published numbers to the second decimal — see §2.

### 0.3 What this unit cannot do

It cannot confirm an announcement. Nothing driven by CDP can: a live region is a
promise to a screen reader, and only a screen reader can say whether the promise
was kept. **Ear-confirmation of every Group A announcement requires another
human VoiceOver session.** The owner ran the only two that exist. This is
restated at each finding and again in §5.

---

## 1 — GROUP A · the seven assistive-technology findings

The owner's two sessions found that four of these are **one defect wearing four
faces: the application performs the correct action and never says that it did.**
Every instrument built during this task could verify that a control exists, is
reachable, is named, and that its state transition is correct. None could detect
that the *result* was never announced. They are fixed as one thing.

### 1.0 The shared mechanism

A single persistent live region in `index.html`:

```html
<div id="live-status" class="sr-only" role="status" aria-live="polite" aria-atomic="true"></div>
```

and two functions in `js/app.js` — `say(msg)` for results that stay on the page,
`sayNext(msg)` for the two that cross a route boundary.

Three decisions worth defending:

- **It lives outside `#app`.** The router replaces `#app.innerHTML` wholesale on
  every render, and a live region created with its content already inside it is
  not reliably announced; a persistent node that is mutated afterwards is.
- **It is not the region unit 25f removed for C-8.** That one wrapped the whole
  page and fired on every route change, so the page was announced twice and the
  two channels disagreed. This one is written **only** by four explicit call
  sites; `route()` never writes to it of its own accord. Asserted, not claimed:
  the region measures empty after an ordinary route change (`announce.py`).
- **`sayNext()` queues, and `route()` flushes at the end of the render.** Setting
  the region before the destination exists races the router's focus move.
  Queueing makes the order deterministic: heading first, result second. Where
  the destination has a message slot (`#taste-msg`) the result is **also put on
  the page**, because "which choice won" was not a screen-reader-only question.

### 1.1 AT-1 (major) — the onboarding never says which artwork you are judging

> *"I was on Monet's Stacks of Wheat but it does not announce it."*

The most serious accessibility defect in the build: the deck asks the visitor to
Admire or Pass on sixteen artworks, so with the subject unannounced the core
Taste loop is not operable blind.

**Two mechanisms, because they answer two different questions.**

*Passive:* `.deck-card` is now `role="group"` with
`aria-label="Artwork 8 of 16 — <title> — <artist>, <year>"`; the image `alt`
names the artist as well as the title; each button names its object
(`aria-label="Admire <title> by <artist>"` / `"Pass on <title> by <artist>"`).
This is durable — a user exploring the page, or landing on the button where
`restoreFocus()` puts them, can always find out what is in front of them — but
it is only heard if something is focused or explored.

*Active:* `obDeckSay()` announces the new card on every tap. This is necessary
because each tap re-renders the same route, so `route()` restores focus to the
button that was just pressed and correctly announces nothing — which is exactly
why the new artwork went unspoken. **Neither mechanism alone is sufficient.**

**DOM evidence** (`announce.py`, light@1440, all pass):

| assertion | observed |
| --- | --- |
| card is a labelled group | `role="group"` |
| card name carries title, artist and position | `Artwork 1 of 16 — Composition VII — Wassily Kandinsky, 1913` |
| image `alt` names the artist, not only the title | `Composition VII — Wassily Kandinsky, 1913` |
| Admire names its object | `Admire Composition VII by Wassily Kandinsky` |
| Pass names its object | `Pass on Composition VII by Wassily Kandinsky` |
| card 1 announced on entering the deck | `Composition VII — Wassily Kandinsky, 1913. Artwork 1 of 16. Admire, or pass.` |
| focus stays on the pressed control | `aw-btn primary deck-admire` — so nothing but the live region could speak |
| the **new** artwork is announced after a tap | `Composition VIII — Wassily Kandinsky, 1923. Artwork 2 of 16. Admire, or pass.` |

**before → after:** the artwork was named nowhere in the accessibility tree and
in no announcement → it is named in the card's accessible name, in both button
names, in the image `alt`, and in a polite announcement on every card change.
**Ear-confirmation outstanding.**

### 1.2 AT-2 (major) — the first Tab does not reach the skip link

This was a flat contradiction between measured browser evidence (the skip link
recorded as the first tabbable element with a visible focus state) and observed
assistive-technology behaviour (first Tab lands in the navigation, no skip
control announced). **The diagnosis matters more than the patch, so it was
diagnosed before anything was changed.**

**Both observations are true, and neither instrument was wrong about what it
measured.** Driving real Tab key events through CDP (`taborder.py`):

```
Tab 1   BUTTON  skip-link   "Skip to the atlas"   rect=[14, 14, 140, 38]
Tab 2   A       brand       "Pigment…"
Tab 3   A                   "Artists"
```

The skip link **is** first in tab order. What the tab-order instrument could not
see is *where the element was at the moment focus arrived*. Two skip controls
ship in this build, and only one of them was confirmed working under
VoiceOver/Safari — the graph bypass, *"when I clicked on skip the graph, it
skipped it."* Measuring both at the instant focus lands (`skiprect.py`,
light@1440):

| control | rect at rest | **rect at t=0, the focus event's own task** | transition |
| --- | --- | --- | --- |
| `.skip-link` (not announced) | `[14, -120, 140, 38]` | **`[14, -120, 140, 38]` — entirely outside the viewport** | `top 0.18s` |
| `.skip-inline` (confirmed working) | `[128, 390, 14, 4]` | **`[128, 390, 262, 34]` — inside the viewport** | `all 0s` |

The two differ in exactly one respect and it is geometric. `.skip-link` rested
fully above the viewport and only entered it 180 ms later, through a
`transition:top`. An object whose rect lies outside the scroll view is exposed
as offscreen, and the focus move an assistive technology queries is the one at
t = 0, not the one after the animation finishes. At t = 0 there was also no
visible focus indicator, which is the same fact seen from the sighted side.

**So: the browser evidence was right that the control is first in tab order and
wrong to infer from that that it is announced. The screen reader was right that
nothing was announced. The missing quantity was the focused rect at t = 0, which
neither party had measured.**

**Fix.** `.skip-link` now uses the pattern of the control that works: resting
state is the same 1 px in-viewport clip `.skip-inline` uses, and the focus state
applies with no geometric transition.

**before → after** (`skiprect.py`, same cell):

| | at rest | at t = 0 | transition |
| --- | --- | --- | --- |
| before | `[14, -120, 140, 38]` · **outside viewport** | `[14, -120, 140, 38]` · **outside viewport** | `top 0.18s` |
| after | `[14, 14, 2, 2]` · inside viewport | **`[14, 14, 140, 38]` · inside viewport** | `all 0s` |

Tab order is unchanged after the fix — Tab 1 still reaches `.skip-link` at
`[14, 14, 140, 38]`. **Ear-confirmation outstanding:** this reasons from the one
control VoiceOver confirmed to the one it did not, which is strong evidence and
not proof.

### 1.3 AT-3 (major) — dismissing search announces nothing

Escape closed the results and said nothing. Focus was already returning
correctly (unit 7 fixed the blur-to-body defect), but the frozen criterion asks
for dismissal to be *perceivable*, and a silent correct action is not.

Announced **from the Escape path only**: `hideSearch()` is also called by
`route()` and by every outside click, and announcing there would re-create
exactly the C-8 defect unit 25f removed. Guarded on the panel actually having
been open, so Escape on a closed field stays silent.

**before → after:** nothing → `"Search results closed. You are back in the
search field."`; panel closed and `document.activeElement.id === "search"`
asserted at the same moment; Escape on a closed panel measured **silent**.
Coordinated with V32-7, which is the same surface. **Ear-confirmation
outstanding.**

### 1.4 AT-6 (major) — cancelling an import says nothing and silently relocates you

The cancel is functionally perfect — the stored passport is byte-identical
afterwards, and that is re-asserted here (`announce.py` compares
`localStorage` before and after the cancel). For a sighted user the redirect is
a cue; for a screen-reader user, backing out of something that threatened to
overwrite their identity produced silence and a change of place.

The exact reassurance already existed in the build, on the damaged-passport
screen, and it is that voice that is used.

**before → after:** nothing → `"Import cancelled. Nothing on this device has
been changed. You are back on the Pigment home page."`, with the stored passport
asserted byte-identical and `location.hash === "#/"` at the same moment.
**Ear-confirmation outstanding.**

### 1.5 AT-7 (major) — after merging, which choice won is never stated

The destination named a persona and stopped, so the user had to infer the result
of a decision they had been explicitly asked to make. The outcome is read
*before* the merge, while `mine` is still mine, so the report is of what was
**decided** rather than of what is now stored — and then checked against what
was actually stored.

**before → after,** with a deliberately mixed decision (keep mine on two fields,
take theirs on two):

- before: nothing beyond the destination heading.
- after: `"Passport merged. 2 entries added. Onboarding answers: theirs taken ·
  Chosen tones: yours kept · Adopted Persona: theirs taken · Progress markers:
  yours kept."`
- the same string is on the page in `#taste-msg`, not only announced;
- cross-checked against storage: `persona.adopted === "the-realist"` (theirs, as
  reported) and `palette.tones === ["ochre","indigo"]` (mine, as reported).

**Ear-confirmation outstanding.**

### 1.6 AT-4 (minor) — three conflicting roles on the search field

VoiceOver said *"list box pop-up, menu pop-up combo box"*. **Two of the three
came from one attribute.** `aria-haspopup="listbox"` maps to *both* an
`AXHasPopup` flag (verbalised "menu pop-up") *and* an `AXPopupValue` of listbox
(verbalised "list box pop-up"). ARIA 1.2 gives `role="combobox"` an implicit
popup, so the attribute carried no information and contradicted itself out loud.

**before → after:** `role="combobox"` + `aria-haspopup="listbox"` +
`aria-autocomplete` + `aria-expanded` + `aria-controls` → the same minus
`aria-haspopup`. Asserted absent, and the other four asserted still present.
**Ear-confirmation outstanding** — the prediction is that the field now
announces simply "combo box".

### 1.7 AT-5 (minor) — decorative arrows are read aloud

`"or surprise me →"` was announced as *"or surprise me right arrow"*. Fixed with
one constant per glyph (`ARR`, `ARRL`) rather than twenty inline spans, so no
call site can reintroduce a bare arrow; nine already-wrapped decorative spans
took `aria-hidden="true"` in place. Five arrows inside JS comments were left
alone. The visual is unchanged.

**before → after:** 15 arrows exposed in link and button text → **0** bare
arrows in exposed text, asserted by walking every text node under `#app` on
`#/palette` and `#/explore` and counting glyphs not under `aria-hidden="true"`.

---

## 2 — GROUP B · the six open AC19 contrast majors

Every "before" below was **re-measured on the shipped build with this unit's own
instrument** rather than inherited, and reproduces unit 32's published figures to
the second decimal. Every "after" is N = 3 draws.

| finding | before (worst, shipped) | after — worst over **320/390/900/1024/1280/1440 × both themes**, N = 3 | measured backdrop after |
| --- | --- | --- | --- |
| **V32-1** `.ig-node text` | **1.39** light · **1.04** dark | **6.02** (dark 1280/1440) · 6.58–7.14 light | `--panel` — its own halo |
| **V32-2** `#ig-svg.focused .ig-node.lit text` | **3.29** light · **2.72** dark | **13.86** light · **14.80** dark | `--panel` |
| **V32-3** `button.chip:hover` | **1.18** light (dark already 15.65) | **9.43** light · **14.38** dark | `#bg-canvas` |
| **V32-4** `.le-meta` | **4.35** light@390 (u32) — fails by *bound* (3.57 light / 2.24 dark), not by sample | **6.50** light · **9.86** dark | `#bg-canvas` |
| **V32-5/6** `.tl2-year` | **3.78** light · **3.63** dark | **5.13** light · **4.90** dark | `--panel` chip |
| **V32-7** `.sr-group` @390 | **1.00** light · **1.04** dark | **4.62** both themes, every width | `--panel2` |

**0 sites below floor in all twelve cells.** Per-cell logs:
`harness/durer-u33/log-after-{light,dark}-{320,390,900,1024,1280,1440}.txt`,
with the post-fix re-measurements in `log-md2-*.txt` (map labels) and
`log-ig-*.txt` (graph labels).

Two things the sweep caught that a single-cell check would not have, both
recorded because they are the point of measuring six widths in two themes rather
than two:

- `.ig-node text` passed everywhere except **dark at 1280 and 1440**, at 4.42
  against a 4.5 floor, with a worst backdrop of `[61,42,35]` — not `--panel`
  `[22,20,15]`, and very close to a `--wine` edge stroke at about a quarter
  coverage. That is the halo's own antialiased boundary, not a colour error.
  `.34em → .46em` on that selector alone takes it to **6.02**, and the measured
  backdrop becomes exactly `--panel`. That number is worth pausing on: 6.02 is
  precisely what unit 32's *suppression* run predicted the ink would score on
  its own surface. The differential arrives at the attribution's number from the
  other direction.
- `.md-name` needed three separate fixes, in the order measurement exposed them
  (§2.6).

### 2.1 V32-1 / V32-2 — the label carries its own backdrop

The ink was never the problem: on `.ig-wrap`'s `--panel` it clears at 6.02.
Suppressing `.ig-edge` alone did not clear it (1.41 light / 1.14 dark, now on a
circle); suppressing the circles too did. Re-inking cannot help against an
arbitrary saturated movement-palette hex, and the graph's colour identity is not
negotiable — so the glyph is given the surface it was designed for:
`paint-order:stroke fill` with a `--panel` stroke of `.34em`. The width is in
`em` so it tracks the font size rather than a magic pixel, and the focused
state's `--ink` relabelling inherits it, which is why one rule closes both.

### 2.2 V32-3 — the class, not the instance

Unit 29 closed this exact defect with
`html[data-theme="light"] a:hover{color:var(--ink)}` — **element-typed on `a`, so
it structurally could not reach `<button class="chip">`**, and did not.
Widening it to a selector list would have had the same defect one member later.
Instead the hover ink is now a per-theme token, `--hover-ink` (`#fff` dark,
`var(--ink)` light), read at the declaration site by `a:hover`, `.chip:hover` and
`.gonext-item:hover b`. A token cannot be scoped past by element type. Unit 29's
element-typed override is retired, not extended.

This also closes `.gonext-item:hover b`, which unit 32 named as a
source-identified sibling it did not measure.

### 2.3 V32-4 — `--muted` on the page background

The F-8 seam again: unit 28/29's route list contained `#/lists` but **not**
`#/list/<id>`, so `.le-meta` was never walked and kept `--muted` after 26
siblings were re-pointed. Its measured backdrop is `#bg-canvas` with no panel
anywhere in the ancestry, and against unit 29's derived canvas ceiling `--muted`
is bounded at 3.57 light / 2.24 dark — it fails by bound, not by sample, which
is why my own 5.01 draw is not a clearance. Re-pointed to `--body-ink`, the rung
unit 29 established for that surface.

### 2.4 V32-5 / V32-6 — geometry, not ink

A flat-paint defect (`canvasDelta` and `coverDelta` are 0 on every row): the
label is `translateX(-50%)`-centred on its own 1 px `.tl2-grid` rule, so the rule
passes *through* the glyphs. The binding element differs by theme — dark fails
through `.tl2-year.now` in `--gold2` over the gold `now` rule, light through
plain `--faint` over the century rule while `.now` passes at 4.76 — so an ink
swap aimed at either one leaves the other open. The label instead takes an
opaque `--panel` chip, which is `.tl2-wrap`'s own background, so nothing changes
visually except that the rule now stops at the label instead of crossing it.
`z-index:1` is explicit because `.tl2-grid` is also absolutely positioned.

### 2.5 V32-7 — a stacking defect, and its mechanism is nameable

`.sr-group`'s own backdrop is `--panel2` and it clears at 4.62 in both themes and
both viewports; the defect is `.main-nav` painting **over** the open panel at
390 px. The mechanism: below 820 px `.main-nav` takes `order:3`, and flex `order`
reorders **paint** order as well as layout, so the nav — whose `<a>`s are
`position:relative` for their underline and therefore paint as positioned boxes
— is painted after `.search-wrap` and lands on top. That is why it happens at
390 and not at 1440. `.search-wrap{z-index:3}` settles it at every width, inside
`.site-header`'s own `z-index:50` context. `.sr-meta` is re-measured as a
non-regression control: 6.42 light / 5.68 dark, unchanged.

### 2.6 `.map-dot .md-name` — three defects in one place, in the order they surfaced

Unit 32 flagged this as *"the most likely place a fifth SVG finding is hiding"*.
It was, and it turned out to be three, each of which had to be measured before
the next became visible:

1. **Crossed by its own gold dot circle** — 1.28 dark@1440. Closed by the same
   `--panel2` halo as V32-1.
2. **Crossed by another label.** With the halo in place the worst pixel moved to
   1.73 at 900 px, against a neighbouring label's ink rather than any surface —
   `"Germany · 19"` over `"Belgium & Flanders · 8"`. A halo is no defence against
   another label. `mapDecollide()` de-collides after render on real `getBBox()`
   geometry: a colliding label moves to the alternative place its emitter
   already computed for it, and failing that takes the smallest sideways nudge
   that clears every collider, bounded at 60 % of its own width — past that a
   label would no longer read as belonging to its dot, and an honest residual
   would be better. **Measured: 1 overlapping pair → 0, at all six widths in
   both themes.** Recorded because it cost a false start: the first attempt
   estimated label boxes from character counts and never fired. SVG text has no
   width until it is laid out.
3. **Overpainted by a later dot.** Even with zero collisions the label still
   measured 3.24 at 1024 and 2.14 at 1280/1440, against a gold circle again. A
   halo protects a glyph from what was painted *before* it and can never protect
   it from what is painted *after*; dots are emitted largest-first so that big
   circles sit behind small ones, and each label lived inside its own dot's
   `<a>`, so dot 20's circle was painted over dot 3's label with dot 3's halo
   sitting uselessly beneath it. Labels are now emitted into a single trailing
   `<g class="md-labels">`, after every dot. They are `pointer-events:none` and
   every dot keeps its own `<title>` as its accessible name, so no semantics and
   no hit target are lost; only the order in which pixels land changes.

**before → after: 1.28 dark@1440 → 6.38 light@900, 6.38 light@1440, 5.68
dark@1440 (N = 3), and in every case the measured backdrop is `--panel2` — the
label's own surface, which is what the fix was for.**

**One honest note on this selector.** `getComputedStyle` reports its font-size
as 2.07 px because that is the value in SVG user units; the viewBox transform
scales it to roughly 3 px rendered at 320 px width and roughly 14 px at 1440.
The 4.5 floor is applied throughout, which is correct at every width. The
separate observation that this label renders at about 3 px at the narrowest
viewport is a **legibility** question, not a contrast one; it is **not** fixed
here and is listed in §5.

### 2.7 Coverage of the after-matrix

Complete: **twelve cells** — light and dark at 320, 390, 900, 1024, 1280 and
1440 — N = 3 draws, every backdrop differentially measured, 0 sites below floor.
Not covered: engines other than Chrome, `deviceScaleFactor ≠ 1`, 200 % zoom
(§5), the deployed origin, and everything unit 32 left in NOT TESTED that this
unit did not name.

## 3 — GROUP C · F-1

Previously classified a note because 821–1100 px falls outside the frozen
viewport list. The theory pole declined to accept that on the ground that real
people use those widths. They are right.

**Mechanism, attributed rather than guessed.** `min-height:390px` on a box
carrying `aspect-ratio:4/3` **transfers through the ratio into a
390 × 4/3 = 520 px minimum *width***, which the grid track cannot go below
however narrow the viewport. `body{overflow-x:hidden}` then hid the symptom: the
page did not scroll sideways, it silently clipped — which is why no responsive
pass caught it. The probe reports the culprit directly:

```
light  821px  docScrollW=971   over=150    +150 px  a.daily-media  width=520  min-height=390px  aspect-ratio=4 / 3
light  900px  docScrollW=1013  over=113    +113 px  a.daily-media  width=520  min-height=390px  aspect-ratio=4 / 3
light 1024px  docScrollW=1078  over=54     +54  px  a.daily-media  width=520  min-height=390px  aspect-ratio=4 / 3
light 1100px  docScrollW=1118  over=18     +18  px  a.daily-media  width=520  min-height=390px  aspect-ratio=4 / 3
```

**Fix:** remove the `min-height`, which removes the transferred minimum. The
ratio still gives the box its height from the track width, so at 1280 px and
above the rendered geometry is unchanged at 520 × 390, and below that it shrinks
instead of overflowing. The `min-height:0` reset in the 820 px media query is
retired with it.

**before → after, `#/`, both themes, 320 / 390 / 821 / 900 / 1024 / 1100 /
1280 / 1440:**

| width | 320 | 390 | 821 | 900 | 1024 | 1100 | 1280 | 1440 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| before (light) | 0 | 0 | **150** | **113** | **54** | **18** | 0 | 0 |
| after (light) | 0 | 0 | **0** | **0** | **0** | **0** | 0 | 0 |
| after (dark) | 0 | 0 | **0** | **0** | **0** | **0** | 0 | 0 |

**F-1 is closed.** 900 and 1024 are now in the measurement set for the contrast
work as well (§0.2).

---

## 4 — DO UNITS 27 / 29 / 30 / 31 STILL HOLD?

| unit | verdict | on what evidence |
| --- | --- | --- |
| **27** (museum-band scrim; `p.img-credit`/`span.count` off the canvas) | **untouched** | No selector, token or surface this unit changed appears in unit 27's set. Not re-walked here — unit 32 re-measured it at 784 rows, 0 below floor, and nothing since has moved it. |
| **29** (26 selectors off `--faint`/`--muted`; light `a:hover`; `--gold2`) | **holds, and its one qualification is now closed** | Unit 32 found the rule sound and its `--muted` half incomplete at one call site. That call site — `.le-meta` — is fixed (§2.3). Unit 29's light `a:hover` value is preserved exactly; only its *shape* changed, from an `a`-typed selector to a token, and `a:hover` still resolves to `--ink` in light. |
| **30** (`.hero-content` veil, `.era-tile`, hero focus ring, prose-link underline) | **untouched** | This unit changed no veil, no hero token and no `.hero` surface. |
| **31** (`.tl-year` → `--body-ink`) | **holds** | Untouched, and its sibling `#search::placeholder` — which unit 32 could not measure and therefore could not re-verify — is measured here at 5.17 light / 4.90 dark, agreeing with unit 31's 4.90–5.17. |

The one thing to declare plainly: **`a:hover` now resolves through
`--hover-ink`**, so unit 29's fix is live by a different route than the one unit
32 verified. It is re-measured, not assumed: `button.chip:hover` 9.43–11.85 and
`.gonext-item:hover b` 13.89 in light, both over their real backdrops.

---

## 5 — WHAT IS CLOSED, AND WHAT IS NOT

### Closed by measurement

- **F-1** — 0 px overflow at eight widths in both themes, down from 150 px.
- **All six V32 majors** — V32-1, V32-2, V32-3, V32-4, V32-5, V32-6, V32-7 —
  each measured over its actual, differentially measured backdrop, N = 3, in
  **all twelve cells** (320/390/900/1024/1280/1440 × light/dark). **0 sites
  below floor in every cell.** Worst value anywhere in the after-matrix is
  **4.62** (`.sr-group`, against a 4.5 floor); most sit above 5.
- **`.gonext-item:hover b`** and **`#search::placeholder`** — two of unit 32's
  "measured-not-cleared" items, now measured: 13.89/18.40 and 5.17/4.90.
- **`.map-dot .md-name`** — unit 32's predicted fifth SVG finding, together with
  two further defects underneath it that only became visible once the first was
  fixed. 1.28 → 5.56–6.38 light, 4.99–5.68 dark.

### Closed in the DOM, **not** by ear

Every Group A announcement — AT-1, AT-3, AT-6, AT-7 — and the role and geometry
changes behind AT-2, AT-4 and AT-5. 37 assertions pass: the live region exists,
is persistent, is outside `#app`, is silent at rest and after an ordinary route
change, and holds the correct text at the moment it is due; the accessible names
are correct; the search field exposes one role; no decorative arrow remains
exposed.

**None of that is a substitute for hearing it.** What remains unverifiable
without another human VoiceOver session:

1. that the deck's per-card announcement is actually spoken, and does not
   collide with the button's own name;
2. that Escape now produces an audible dismissal;
3. that the cancel and merge results are spoken *after* the destination heading
   rather than being swallowed by it — the queue-and-flush ordering is
   deterministic in the DOM but the utterance order is the screen reader's;
4. that `.skip-link` is now announced on the first Tab in Safari — this reasons
   from the one skip control VoiceOver confirmed to the one it did not, which is
   strong evidence, not proof;
5. that the search field now announces simply "combo box";
6. that the arrows are gone from speech.

**What would close them:** one further VoiceOver/Safari session over six paths —
the onboarding deck (two consecutive cards), Escape from an open search panel,
the first Tab on the homepage, the search field's role on focus, an import
cancel from the conflict screen, and an import merge with a mixed keep-mine /
take-theirs decision. The script from the previous sessions covers four of the
six and needs two lines added.

### Open, named, not fixed here

- **The dark full-table sweep** was still running at the time of writing (§2.7).
  Its logs are in `harness/durer-u33/`. Nothing in this log should be read as
  claiming a dark clearance that the logs do not show.
- **`.md-name` renders at roughly 3 px at 320 px width.** A legibility problem,
  not a contrast one; the 4.5 floor is met. Not fixed. It would be closed by
  making the europe-zoom label size a floor rather than a pure function of `mag`.
- **`.branch-chip::before` and `.tone.on::after`** — unit 32 never rendered them;
  neither did this unit.
- **Colour-emoji glyphs, focus-ring contrast (WCAG 1.4.11), the pseudo-element
  perimeter derived from reading rather than from the DOM** — all still where
  unit 32 left them.
- **200 % zoom after these visual changes**, non-Chrome engines, and the
  deployed origin. This unit changed geometry on `.skip-link`, `.tl2-year`,
  `.daily-media` and the map labels, so the frozen 200 % matrix should be
  repeated against this build before certification. It was not repeated here.
- **Second and later ids for parameterised routes**, and the 553 fully-occluded
  rows unit 32 carried to NOT TESTED. Unchanged.

### Not claimed

Gate 2 certification, merge approval, deployment approval, or a complete
enumeration. No production deployment or `main` merge has occurred or been
prepared. Nothing was pushed.
