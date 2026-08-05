# VISUAL DIRECTION — PIG-001 · ruling on deviation D-29-6

**From:** Matisse (`claude-visual-director`)
**On:** D-29-6, `evidence/build-log-unit-29.md` §7 and Decision Record row D-29-6;
quality review finding F-7 (`quality-review.md` A9)
**Question referred:** should light prose links be underlined, now that every ink
which clears the `#bg-canvas` ceiling lands next to `--body-ink`?
**Ruling:** **Yes — underline prose links, in both themes. Not blocking.**

---

## INTENT

Pigment's chrome recedes so the artwork can be the hero. A link is chrome. For
twenty-nine units this project has spent its accessibility budget on *contrast* —
making glyphs legible against a moving generative ground — and it has succeeded:
AC19's floors are met everywhere. D-29-6 is a different failure mode and it is the
one the contrast work created. Having pushed every usable ink into a single narrow
band of dark warm brown, we can no longer ask hue to do a job it is now too weak
to do. The correct answer is not to walk the ink back — the ceiling is derived, not
negotiable — but to stop asking colour to carry the affordance and give it to the
underline, which is the older and more editorial device anyway. A ruled line under
a word is book typography. It suits this atlas better than a coloured word does.

---

## MEASUREMENTS I TOOK MYSELF

Recomputed from the shipped token values in `css/styles.css` (sRGB → WCAG relative
luminance; CIELAB/LCh for perceptual separation). I did not carry figures from the
build log.

**Link ↔ body-text separation (the subject of D-29-6):**

| pair | contrast | ΔL\* | ΔC\* | ΔE76 |
| --- | --- | --- | --- | --- |
| light, before unit 29 — `#81632b` vs `--body-ink` `#433c31` | **1.95** | 18.2 | 28.1 | 33.5 |
| light, after unit 29 — `--gold2` `#544019` vs `#433c31` | **1.10** | 2.7 | 18.9 | 19.1 |
| dark — `--gold2` `#e8c98a` vs `--body-ink` `#d8d2c4` | **1.06** | 2.1 | 27.9 | 28.1 |

Dürer's 1.95 → 1.10 figure is confirmed exactly.

**Text legibility is not in question** (both themes, worst reachable canvas
backdrop from the unit-29 derivation, light ceiling `rgb(187,174,162)`, dark
ceiling `rgb(101,88,76)`):

| ink | on `--bg` | on `--panel` | on canvas ceiling |
| --- | --- | --- | --- |
| light `--gold2` `#544019` | 8.40 | 9.16 | **4.56** |
| light `--body-ink` `#433c31` | 9.25 | 10.09 | **5.02** |
| dark `--gold2` `#e8c98a` | 11.90 | — | **4.31** |
| dark `--body-ink` `#d8d2c4` | — | — | **4.56** |

**Underline colour candidates**, composited and measured, because this decides
which colour the underline takes:

| candidate | rendered on light `--bg` | vs `--bg` | vs canvas ceiling |
| --- | --- | --- | --- |
| `--line` `rgba(168,129,60,.3)` | `rgb(220,204,174)` | 1.34 | **1.16** |
| `--gold` `#9e7938` | — | 3.40 | **1.85** |
| `currentColor` (= the glyph) | `#544019` | 8.40 | **4.56** |

That table is the whole reason this ruling deviates from the precedent's colour.

---

## 1. RULING — light prose links are underlined (and so are dark)

### 1a. Yes, underline. Scope: prose only.

Blanket underlining of every anchor would be wrong and I reject it. Pigment's
anchors fall into two populations and only one of them has the problem:

**Underline (colour is the only distinguisher):** inline links inside running body
copy — `.page-lede`, `.aw-provenance` provenance lines, the `.lost` 404 copy,
`.hpw-step p` step copy, and the unclassed `<p>` prose on `#/credits`, `#/privacy`
and `#/about`. Every one of these is a bare `<a href>` with no class of its own,
sitting mid-sentence in `--body-ink` copy.

**Do not underline (a non-colour affordance already exists):** card and heading
links (`.card-body h3 a`, `.lc-kicker`, `.le-body h3 a`) — heading-sized, block
position, whole-card hit area; `.chip`, `.branch-chip`, `.chip.a` — bordered pills;
`.entry-card`, `.mini-card`, `.gonext-item`, `.stat`, `.era-tile`, `.arc-work`,
`.daily-enter`, `.daily-media`, `.map-dot`, `.btn`, `.aw-btn` — block objects with
their own boxes; `.main-nav a` — navigation, positional, with the `::after` rule and
`.active` state; `.breadcrumbs a` — positional with `/` separators; `.tree-svg a`,
`.tl2-bar` — diagram geometry; `.credit-list .cr-what a` — already carries
`border-bottom:1px solid var(--line)` (`styles.css:726`), a non-colour affordance by
a different mechanism, which I leave alone; `#lightbox` links — over photography,
its own contrast regime.

### 1b. Precedent found, and where I depart from it

The repo carries the treatment three times, two of them by `text-decoration`:

- `css/styles.css:709-711` — `.img-credit a`: `underline`, `text-underline-offset:2px`,
  `text-decoration-color:var(--line)`; hover/focus → `color:var(--gold2)`,
  `text-decoration-color:var(--gold)`. Theme-neutral.
- `css/styles.css:245-252` — `html[data-theme="light"] .home-hero-content .footer-note a`:
  identical geometry, identical colours, with the comment naming `.img-credit a`
  as its source.
- `css/styles.css:726-727` — `.credit-list .cr-what a`: the border-bottom variant.

**I adopt the precedent's geometry unchanged** — `text-decoration:underline` with
`text-underline-offset:2px`. **I depart on one value: the resting decoration colour.**
`--line` renders at **1.16:1 against the worst reachable canvas backdrop** (measured
above). In the two precedent sites that was acceptable because the underline was a
supporting cue on a small credit line already set apart by size and by its own ink.
Here the underline is the *sole* non-colour distinguisher on a third of the site's
text, over a ground that moves. A cue that can drop to 1.16:1 over its own backdrop
is not a remedy; it is the appearance of one. The resting underline therefore takes
`currentColor`, which by construction can never be less visible than the word it
underlines (4.56:1 worst case in light, 4.31 in dark). No new custom property is
introduced and no parallel system is created — this is the same treatment at a
value that survives the surface it now has to work on.

### 1c. Implementable specification

Add to `css/styles.css`, in the link/anchor region near `a{}` (`styles.css:274`).
**Theme-neutral — no `html[data-theme]` prefix** (see §2).

```css
/* D-29-6 · Prose links carry an underline, not just a colour.
   Unit 29 pushed every ink that clears the #bg-canvas ceiling into one narrow
   band: link-vs-body separation is 1.10:1 in light and 1.06:1 in dark, so the
   3:1 luminance technique for WCAG 1.4.1 (G183) is unreachable in either theme
   without deleting the ink work. Colour therefore stops being the affordance and
   the underline becomes it. Scoped to inline prose links only — classed anchors
   (chips, cards, nav, entry-cards, diagram links) are distinguished by shape,
   box or position and are excluded by :not([class]). The two credit surfaces
   certified in units 26a and 28 keep their own rule and are excluded by class.
   Resting colour is currentColor, not --line: --line renders at 1.16:1 against
   the worst reachable canvas backdrop and cannot be the sole non-colour cue on
   this surface. Geometry (underline + 2px offset) is unit 28's, unchanged.
   (WCAG 1.4.1 / D-29-6 / Matisse ruling visual-ruling-d29-6.md) */
#app p:not(.img-credit):not(.footer-note) a:not([class]){
  text-decoration:underline;
  text-decoration-thickness:1px;
  text-decoration-color:currentColor;
  text-underline-offset:2px;
  text-decoration-skip-ink:auto;
  transition:color .2s var(--ease),text-decoration-thickness .2s var(--ease);
}
#app p:not(.img-credit):not(.footer-note) a:not([class]):hover,
#app p:not(.img-credit):not(.footer-note) a:not([class]):focus-visible{
  text-decoration-thickness:2px;
}
```

Notes for Dürer, so nothing here is left to interpretation:

1. **Hover colour is already correct and must not be touched.**
   `html[data-theme="light"] a:hover{color:var(--ink)}` (`styles.css:256`) and dark's
   `a:hover{color:#fff}` (`styles.css:275`) both stand. Because the underline is
   `currentColor`, it follows the hover colour automatically — the state change is
   carried by *thickness plus colour together*, and the thickness half survives
   greyscale and every colour-vision deficiency.
2. **Focus is unchanged.** The global focus-visible ring is the focus indicator of
   record and I am not modifying it. The `:focus-visible` thickness bump above is
   additive only, so a keyboard user gets the same emphasis as a mouse user.
3. **The two `:not()` class exclusions are deliberate**, not defensive noise.
   `#app p a:not([class])` has specificity (1,1,2) and would otherwise override
   `.img-credit a` (0,1,1) and the light hero `.footer-note a` (0,3,2), silently
   restyling two surfaces Van Eyck has already certified in units 26a and 28.
   Excluding them costs nothing and keeps the certified evidence valid.
4. **`:not([class])` is the load-bearing scope mechanism.** Every prose link in
   `js/app.js` is a bare `<a href>`; every non-prose link carries a class. I verified
   this against all 86 anchor call sites in `js/app.js`. The `<p style="margin-top:26px">
   <a class="chip" href="#/">Back to the atlas</a></p>` pattern on the static pages is
   correctly excluded.
5. **No token, no value, no measurement changes.** This rule sets decoration
   properties only. No text colour moves, so **no AC19 figure in unit 29's log or in
   Vermeer's evidence is disturbed** and nothing needs re-measuring for contrast.
   A `?v=` bump on `index.html:27` is required as usual.

### 1d. Optional follow-on (my recommendation, not a requirement)

For one treatment site-wide, `.img-credit a` (`:709`) and the light hero
`.footer-note a` (`:247`) could take `text-decoration-color:currentColor` in place of
`var(--line)`. It is a two-value change with no contrast implication. I mark it
**optional and out of Gate 2 scope** precisely because those two surfaces are
certified and I would rather leave a small inconsistency than reopen certified
evidence at the last criterion. If it is not taken now, it belongs on the
post-PIG-001 list.

---

## 2. DARK THEME — it needs the same treatment, and the referral's premise is wrong

Dark's separation is **1.06:1** — measurably *worse* than light's 1.10:1. Its ΔL\* is
2.1 against light's 2.7. What dark has is chroma: ΔC\* 27.9 against light's 18.9,
giving ΔE76 28.1 against 19.1. Dark's gold reads as a link because it is *saturated*
next to a near-neutral body ink, not because it is lighter.

That makes dark **more separable but not differently qualified**. Chroma is colour.
A user in greyscale, or with any of the common colour-vision deficiencies on the
warm axis, gets 1.06:1 in dark and 1.10:1 in light — both are, for that user, no
distinction at all. WCAG 1.4.1 asks whether colour is the *only* visual means; in
dark today it is. The 3:1 luminance technique fails in dark by a wider margin than
in light.

I therefore reject the light-only framing. Ruling for light alone would ship an
atlas where the same user gets an affordance in one theme and loses it by toggling
to the other, and it would put a `html[data-theme="light"]` prefix on a rule that
has nothing to do with theme. The theme-neutral rule in §1c is both the more
accessible answer and the *smaller* one. Visually the cost is real but slight: dark
prose links keep their gold and gain a 1px gold rule at 2px offset — in a dark
gallery theme that reads as gilding, not as browser chrome.

---

## 3. BLOCKING OR NOTE — a note, with the remedy specified

**My view for Van Eyck: this does not block Gate 2.**

1. **AC19's frozen text is "contrast checks."** (`specification.md:64`.) 1.4.1 is not
   a contrast check — it has no ratio requirement at all. I searched the frozen
   specification for any use-of-colour criterion and found none. Unlike F-7, where
   Van Eyck's reasoning turned on AC19 having no enumerated pair inventory to
   exclude the canvas class, here there is no criterion for D-29-6 to fail against.
2. **This is a worsened margin inside a condition that already failed, not a new
   failure.** At 1.95:1 with `text-decoration:none`, light prose links did not meet
   the luminance technique before PIG-001 either, and dark at 1.06:1 never has.
   PIG-001 did not create the 1.4.1 exposure; it made an already-failing margin
   smaller while closing a real 1.4.3 failure on a third of the site's text. That is
   a straight improvement in accessible outcome.
3. **I am not invoking "pre-existing" as an excuse, and Van Eyck is right that it has
   never been accepted in this task.** The distinction is that in units 25–29 the
   pre-existing conditions were failures *of a frozen criterion*. This one is not, and
   it comes with a specified, implementable, one-rule remedy attached — §1c is not a
   promise to fix it later, it is the fix.
4. **My own role's rule — accessibility overrides styling preference — is what
   produced §1c, not what should escalate this.** I have ruled *for* the remedy on
   accessibility grounds and against my own preference for undecorated links. Having
   done that, holding the gate as well would be belt-and-braces on a criterion that
   does not exist.

**Recommended disposition:** apply §1c as unit 30 (CSS + `?v=`, no token changes, no
re-measurement of AC19 figures), record D-29-6 as **accepted with remedy applied**,
and note in the Decision Record that the 1.4.1 exposure was pre-existing in both
themes and is closed by this unit rather than by AC19. If unit 30 cannot be run
before certification, D-29-6 downgrades to a **note carried into the release record**
with this document as its specification — but it should be run; it is one rule.

---

## 4. THE PANEL-ONLY INK LADDER — accepted as a standing design rule for Pigment

**I accept it, and I want it stated more strongly than Dürer stated it.**

Dürer wrote the rule as a fact about the palette: only `--body-ink` and `--ink`
clear the small-text floor over `#bg-canvas`, so the four-rung ladder is panel-only.
That is correct and it is now in the stylesheet at `#bg-canvas` where the next
author meets it before choosing a colour. As Visual Director I adopt it, with one
reframing and four consequences.

**The reframing: a ladder is a property of a surface, not of a palette.** Pigment
does not have a four-rung ink ladder. Pigment has *two ladders* — a four-rung ladder
on opaque panels and a two-rung ladder on the page background — and which one is in
force is decided by what is behind the glyph, not by the token's name. Writing it
that way stops the next author reading "panel-only" as a demotion of `--faint` and
`--muted`. They are not demoted. They are surface-scoped, and they always were; unit
29 is the first time anyone measured the surface.

**What this means going forward:**

1. **`--faint` and `--muted` are panel inks.** They are legitimate and I want them
   used — inside `--panel` / `--panel2`, where the ladder is real. Their surviving
   sites (`#search::placeholder`, `.sr-kicker`, `.tl-year`, `.tn-count`, `.tm-lab`,
   `.pp-card-loading`) are correct and stay. They may not paint small text on the
   page background, in either theme, without a fresh measurement against the
   derived ceiling.
2. **Chromatic inks — `--gold`, `--teal`, `--wine`, `--blue`, `--rose`, `--mauve` —
   are 3:1 tokens.** Fills, rules, borders, focus indicators, large text. They are
   not small-text inks anywhere on the page background, and in light they do not
   clear 4.5 on *any* of our surfaces at small sizes. This is a colour-relationship
   rule I am glad to have: these hues do their best work as chips, keylines and
   accents, and they have always been weakest as body glyphs.
3. **Hierarchy on the page background is carried by size, weight, letter-spacing and
   space — not by ink.** This is the design consequence and it is the one worth
   internalising. With two rungs available, a designer who reaches for a third tone
   to signal "less important" has no third tone; they must reach for scale, for the
   uppercase letterspaced kicker, for a rule, for whitespace. That is a *better*
   editorial instinct than tonal grading, and it is more consistent with Pigment's
   character. I would have argued for it on aesthetic grounds; the measurement has
   made it mandatory, which saves the argument.
4. **If we ever want more rungs on the page background, the correct lever is the
   canvas, not the inks.** The ceiling is derived from `#bg-canvas`'s reachable tone
   range in `js/app.js`. Narrowing that range — tightening the blob/ribbon alpha
   envelope, or the light-theme `opacity:.6` — would raise the floor and give the
   background back a third rung. That is a real future option and it belongs in the
   record so nobody concludes the palette is permanently capped. It is a
   deliberate, measurable, whole-system change and must be re-derived, not
   eyeballed. Nobody re-points an ink to buy a rung.

**Where this is written down.** The derivation lives at `#bg-canvas` in
`css/styles.css` and should stay there. The *design* rule — consequences 1–4 above —
belongs in `docs/STYLE_GUIDE.md` as a short colour section, because that is where
the next author looks before they open the stylesheet. I am not editing that file;
it is a post-PIG-001 documentation item and I am recording it here so it is not lost.

---

## CONTINUITY

Reused unchanged: `text-decoration:underline` + `text-underline-offset:2px` from
`.img-credit a` (`:709`) and the light hero `.footer-note a` (`:245`); `var(--ease)`
for transitions; the existing `a:hover` colours in both themes (`:256`, `:275`); the
global focus-visible ring. New: one decoration value (`currentColor` in place of
`var(--line)`), justified by measurement in §1b, and `text-decoration-thickness` as
the greyscale-safe half of the hover/focus state change. **No new custom property,
no new token, no colour value changed anywhere.**

## CHALLENGES RAISED

1. **To the referral's framing.** "Should *light* prose links be underlined" assumes
   dark is adequate. Measured, dark is 1.06:1 — worse. The rule is theme-neutral.
2. **To the precedent's underline colour.** `var(--line)` at 1.16:1 against the
   canvas ceiling cannot be the sole non-colour affordance for a third of the site's
   text. Geometry kept, colour changed, reason measured.
3. **To any proposal to walk `--gold2` back toward `#81632b` to recover separation.**
   It clears the ceiling at 2.58 and fails 4.5. Restoring hue separation by
   reintroducing a contrast failure is a trade this project has refused four times
   and must refuse again.
4. **To reading "panel-only ladder" as a loss.** It is a correct statement about
   surfaces and it forces a better hierarchy discipline than tonal grading. Adopted
   as standing direction, not as a regrettable constraint.

## REVIEW

Not applicable — no screenshots exist for the proposed rule. If §1c is built,
Vermeer should capture `#/credits`, `#/privacy` and `#/404` at 1440×900 and 390×844
in both themes, and I will review the underline weight and offset against the
prose at those sizes before the rule is considered settled.

---

# N-8 — the underline, seen

**Date:** 2026-08-06 · **Reviewer:** Matisse (`claude-visual-director`) · **HEAD:** `a71e2c5`
**Scope:** the D-29-6 prose-link underline as built in unit 30b (`css/styles.css:310-336`),
judged against rendered prose for the first time. Plus a short coherence sweep over
units 33/34/36. Not in scope: contrast (measured and closed), artist-first hierarchy
(owner-reserved), AC23.

## VERDICT — **PASS WITH NOTE**

The specification survives contact with real prose. Both themes, both viewports.
One note, recorded below, and one thing I could not see.

### Evidence

| # | Screenshot | What it shows |
| --- | --- | --- |
| E1 | `evidence/credits__desktop-1440x900__dark.png` | Wikimedia Commons + Privacy links in body prose, dark |
| E2 | `evidence/credits__desktop-1440x900__light.png` | same paragraph, light paper over the ambient wave |
| E3 | 2× crops of E1/E2 at the same paragraph (sips, `--cropOffset 385 120`, 780×110 → 2340×330) | underline weight, offset, skip-ink, wrap behaviour |
| E4 | `evidence/credits__mobile-390x844__dark.png` | 390px column: link on its own line, and a link mid-sentence |
| E5 | `evidence/privacy__desktop-1440x900__light.png` | prose with mono `code` spans and no links — the control case |
| E6 | `evidence/museum-louvre__desktop-1440x900__light.png` | `.img-credit` underlines on light paper, directly above unlinked prose |
| E7 | live at `127.0.0.1:8433` (own port, killed; owner's 8422 untouched) | computed style on `#/credits`: `text-decoration-thickness:1px`, `text-decoration-color:rgb(232,201,138)` = `currentColor`, `text-underline-offset:2px` |

### 1. Affordance without noise — **holds**

E1/E3: "Wikimedia Commons" and "Privacy" read as links at a glance, before colour is
consciously processed. Nothing else in that column is underlined, so the mark is
unambiguous. Density is the reason it works: the D-29-6 scope
(`p:not(.img-credit):not(.footer-note) a:not([class])`) yields **two** underlines in
the whole Credits lede and **zero** on the Privacy page (E5) — where the mono `code`
spans, correctly, carry no underline and so cannot be mistaken for links. On the
artist and museum pages (E6, `u30-artist-caravaggio__desktop-1440x900__dark.png`) the
editorial prose carries no inline links at all, so the dense-prose smear I was most
worried about does not exist on this site. The rule is doing work exactly where prose
links exist and nowhere else.

### 2. Both themes — **holds; dark is the stronger of the two, not the weaker**

I ruled theme-neutral because dark measured worse (1.06:1 vs light's 1.10:1) and I
expected dark to be the case I had got wrong. Seen (E3), it is the opposite. In dark
the underline is `#e8c98a` on near-black: high-luminance hairline on a dark field,
and it reads as crisply as the glyphs above it. In light it is the muted gold-brown
on paper — present, correct, and quieter, because a dark hairline on a light ground
at 1px simply carries less optical weight than a light hairline on a dark ground at
the same measure. Light is the marginal case. It still passes: at 2× (E3, light) the
rule under "Wikimedia / Commons" and under "Privacy" is continuous and unmistakable.
But if anyone ever proposes trimming this treatment, light is where it would break
first — the opposite of what my own measurement predicted. Recorded as a correction
to my §1b reasoning: the contrast ratio predicted which theme needed the underline
*most*, not which theme would render it *best*. Those are different questions and I
conflated them.

### 3. Collisions — **none found**

- **Descenders:** "Privacy" is the test case in both themes. `text-decoration-skip-ink:auto`
  cuts the rule cleanly around the `y` tail at 2px offset (E3, both). No pierce, no
  visible nick in the glyph.
- **Adjacent punctuation:** "Wikimedia Commons**,**" — the comma sits outside the
  underline in both themes (E3). Correct: the anchor ends where the link ends.
- **Wrapped links:** the same link breaks across two lines in E1/E2/E3 and again,
  differently, at 390px (E4). Both fragments carry the rule; the second-line fragment
  starts flush at the measure's left edge with no orphaned stub. Line-height is wide
  enough (E3) that the first line's underline never crowds the second line's
  ascenders.
- **Links inside list entries:** none exist under this selector — list, card and chip
  anchors are classed and excluded, and E6/`lists__desktop-1440x900__light.png`
  confirm the exclusions hold at HEAD. Nothing in a list picked up the rule by accident.

### 4. Hover / focus thickening — **not seen; specification confirmed in the cascade**

I state this plainly rather than claim a judgement I did not make. The evidence pack
contains **no hover or focus-visible capture** — 108 stills, all resting state — and
my live session on `#/credits` confirmed the resting computed values (E7) but the
pane became unresponsive before I could capture the hovered frame. What is confirmed:
the rule exists as specified at `css/styles.css:333-336`, `1px → 2px` on both `:hover`
and `:focus-visible`, transitioned on thickness rather than colour so it survives
greyscale.

On the value itself I hold my specification: a doubling is the smallest step that is
reliably perceptible on a 16px body at 2px offset, and the step below it (1px → 1.5px)
would land on sub-pixel rendering and read as nothing on a non-retina display. 2px is
not crude — at 2px offset the thickened rule still clears the descenders that
skip-ink carves around it. **This is a defended specification, not an observation.**
If Van Eyck wants N-8 closed on observed evidence rather than on the cascade, the
missing artifact is one frame: `#/credits`, dark and light, mouse over "Privacy".
I do not consider that frame blocking.

### 5. NOTE (non-blocking) — two underline colours on one page

E1 shows it: in the Credits lede the prose underlines are gold (`currentColor`), and
250px below, in the attribution table, the `.img-credit` underlines are grey
(`var(--line)`). Same geometry, same page, two colours for one affordance. I looked
at this deliberately and I am not calling it a defect: the table is metadata, it is
set smaller and dimmer on purpose, and its links being visibly quieter than the
lede's is correct hierarchy rather than an inconsistency. E6 shows the same pairing
on light paper and it reads as deliberate there too. The unification already noted in
this document (`.img-credit`/`.footer-note` taking `currentColor`) remains available
and remains **out of scope for PIG-001** — it would touch two certified surfaces to
buy tidiness, not accessibility. Recorded so the next reviewer does not rediscover it
as a finding.

## COHERENCE SWEEP — units 33 / 34 / 36

Screenshot-grounded, no contrast re-audit.

- **Influence-graph label halo (u33) — passes, and it is the best change in the set.**
  `evidence/u33-ig-labels__desktop-1440x900__dark.png` and
  `evidence/influences__desktop-1440x900__dark.png`. The fear was a smear; the result
  is the opposite. At full density (204 painters, 238 edges) the halo is invisible as
  an object — you see no glow, no plate, no box — and its only perceptible effect is
  that "Dante Gabriel Rossetti" and "Lucas Cranach the Elder" stay readable where they
  cross an edge line. Re-emitting labels after the dots is right: a label clipped by a
  node is a bug, a label over a node is a legend. **Pass.**
- **Graph label crowding — observation, not a finding.** In the dense right-hand
  cluster (Renoir / Hokusai / Dalí / Bacon) labels sit close enough to touch. That is
  the graph's data density at 1440px, not a regression from unit 33, and the halo is
  what keeps it legible rather than what causes it. No action.
- **`.tl2-year` (unit 34) — passes.** `evidence/timeline__desktop-1440x900__light.png`.
  The 1300/1400 markers read as quiet letterspaced gold on the gridline, in the same
  voice as the "EIGHT CENTURIES AT A GLANCE" eyebrow and the "— " section rules. It
  belongs to the system; nothing bolted on.
- **`.le-meta` (unit 34) — passes.** `evidence/lists__desktop-1440x900__light.png`.
  "LIST · 10 WORKS" sits in the same caps-tracked register as every other eyebrow on
  the site. The card stack still leads with the artwork; the meta recedes. Identity
  holds.
- **Chips (unit 36) — resting state passes.**
  `evidence/u30-artist-caravaggio__desktop-1440x900__dark.png`. The movement/technique/
  era/nation row and the "why this painter matters" tag row are one family, dot-marked
  and pill-shaped, and they do not compete with the hero. Hover is a state and is not
  in the pack; not judged.
- **Mobile search-panel layering (unit 36) — passes.**
  `evidence/credits__mobile-390x844__dark.png`. Search field above, horizontally
  scrolling nav row below, both on the sticky header, no bleed-through of page content
  and no z-order artifact at the seam.
- **`#/credits` lede copy (unit 36) — passes, and it is in voice.** "Pigment is built
  on pictures other people took and shared" is plain, unembarrassed, and does the
  Style Guide's job of crediting without lawyering. Set in body prose directly under
  the framed title, it also gives the two prose underlines the uncrowded field that
  makes §1 pass.

**Identity holds across all seven.** Nothing in units 33/34/36 reads as bolted on;
the additions are all in the existing letterspaced-caps / hairline-rule / dot-chip
vocabulary rather than beside it.
