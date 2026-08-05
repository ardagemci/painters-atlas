# PIG-001 · Build log — unit 34

**Branch:** `pig-001-stabilization` · **Commit:** `1ed9033` · **Author:** Dürer
(Implementation Lead) · **Gate 1:** satisfied — `protocol/tasks/PIG-001/specification.md`
line 8 reads `workflow_state: "approved_for_build"`.

Two items from the owner's third VoiceOver session. Both are speech-only: no
rendered pixel changes, so the screenshot and contrast evidence about to be
captured against this code remains valid.

---

## Item 1 — AT-5: why unit 33's fix did not hold

### The diagnosis

Unit 33's fix was **partial by construction: it covered every arrow that
JavaScript emits and none that CSS emits.**

Unit 33 introduced the `ARR` / `ARRL` constants in `js/app.js` (commit
`4f90e96`) and wrapped the remaining inline arrows in
`<span aria-hidden="true">`. That work was correct and it did ship — `ARR`
predates the unit-33 cache-bust commit `ca72cb8`, so the build the owner tested
at `?v=20260805-pig001-u33` genuinely contained it. Verified below: every one of
the sixteen arrow-emitting sites in `js/app.js` hides its glyph.

What unit 33 never inspected was the **stylesheet**. `css/styles.css:1209` set

```css
.branch-chip::before{content:"↳"}
```

on the movement/technique branch chips. Generated content participates in the
accessible name in Safari, and **no `aria-hidden` span can reach a
pseudo-element** — the JS-side constant was structurally incapable of covering
this site. So the arrow the owner still heard was never one of the arrows unit
33 fixed. Unit 33 then recorded AT-5 closed on the strength of the JS-side DOM
assertions, which were true and incomplete.

The lesson is the same one AT-2 produced: an assertion that passes over the
sites you thought of is not evidence about the sites you did not. Unit 33 fixed
the instances it recalled; the correct method — and the one used here — is to
grep the character across both production files.

### The fix

`.branch-chip` is an `<a>` whose accessible name comes from its contents, so the
pseudo-element glyph leaked into it. The chip now carries an **explicit
`aria-label` equal to its visible text** (`js/app.js:854`). An explicit label
overrides name-from-contents entirely, so the glyph can never enter the name.

This was chosen over the CSS alternative `content:"↳" / ""` (empty alt text)
deliberately. That syntax landed in Safari 17.4; on an older Safari the whole
`content` declaration is invalid, the glyph disappears, and the chip changes
visually. The `aria-label` route touches no CSS at all and therefore cannot move
a pixel. WCAG 2.5.3 (label in name) is satisfied because the label is byte-equal
to the visible text.

A comment at `css/styles.css:1209` records the coupling so a future `::before`
glyph on a named element gets the same treatment.

### Sites covered

`grep` for the character across `js/app.js` and `css/styles.css`:

| Location | Emitter | Status |
| --- | --- | --- |
| `js/app.js:47,48` | `ARR` / `ARRL` constants — 13 call sites (1276, 1751, 1775, 2003, 2094, 2209×2, 2210, 3259, 3261, 3276, 3350, 3575, 3720, 3758) | already `aria-hidden` (unit 33) |
| `js/app.js:1480,1848` | `daily-enter` inline spans | already `aria-hidden` (unit 33) |
| `js/app.js:1628,1634,1640,1646,1752,1758,1764` | `.ec-arrow` spans | already `aria-hidden` (unit 33) |
| `css/styles.css:1209` | `.branch-chip::before` generated content | **fixed this unit** |

Non-sites confirmed: the remaining `→` in both files are inside `/* */` comments
(`js/app.js` 1104, 1503, 2337, 2597, 2790; `css/styles.css` 627, 1164) and never
reach the DOM. `js/personas.js` and `js/taxonomy.js` matches are comments only.

**One arrow deliberately not fixed, recorded rather than silently closed.** The
pre-rendered SEO landing pages under `p/artwork/*.html` carry a bare `→` in
"Open in the atlas →", written by `tools/build_seo.jxa.js`. These are outside
the single-page app the owner tested and are not linked from it. Fixing them
means regenerating ~100 static files, which is not this unit's scope and would
invalidate nothing but would bloat the diff. It is logged here as an open,
separate item so AT-5 is not recorded as universally closed when it is not.

### DOM evidence

Served the working tree on my own port 8431 (the owner's 8422 was not touched)
and swept the live DOM in Chrome.

Movements index (`#/movements`) — the page that renders branch chips:

```json
{ "arrowSites": [], "exposed": [], "totalArrowTextNodes": 0,
  "branchChip": { "pseudoContent": "\"↳\"", "ariaLabel": "Proto-Renaissance",
                  "visibleText": "Proto-Renaissance", "labelMatchesVisible": true } }
```

`pseudoContent` still computes to `"↳"` — **the glyph still renders, so there is
no visual change** — while the accessible name is now the explicit label, equal
to the visible text.

Home (`#/`), which renders `.ec-arrow`, `daily-enter` and `ARR` buttons:

```json
{ "total": 6, "allHidden": true, "exposedToAT": [] }
```

Six arrow text nodes, every one inside `[aria-hidden="true"]`, none exposed.

### Outstanding

**Ear-confirmation of AT-5 is outstanding.** The DOM shows the glyph is out of
the accessibility tree; only the owner's VoiceOver can confirm it is out of the
speech. That is precisely the gap that produced this finding, so this unit does
not record AT-5 as closed — it records it as fixed and awaiting the ear.

---

## Item 2 — deck position at quarter points (AT-1 follow-on)

The owner, who listened to sixteen consecutive announcements: *"Maybe the
artwork number in every card is unnecessary. We can only use in 4th, 8th, 12th
and 16th maybe."* Adopted as a product judgement.

`obDeckSay()` (`js/app.js:3249-3258`) now gates only the `Artwork N of 16.`
fragment. Title, artist and year are spoken on every card, unchanged.

```js
const n = ob.di + 1;
const pos = (n === 1 || n % 4 === 0) ? `Artwork ${n} of 16. ` : "";
say(`${w.title} — ${a.name}, ${w.year.display}. ${pos}Admire, or pass.`);
```

### Card 1 — included, and why

Card 1 carries the position. Entering the deck fires `obDeckSay()` as its only
spoken event (`js/app.js:3777`, the `tones-done` branch); nothing else states
the deck's length. Omitting card 1 means a listener arriving with no context
first learns the deck is sixteen long when they reach card 4 — three blind
advances in. The owner's request was aimed at repetition, not at the count
itself, so announcing it once at entry and then at the quarter points serves the
intent rather than stretching it. Cadence: **1, 4, 8, 12, 16** — five
announcements in place of sixteen.

Nothing else was added.

### Two other statements of position, left alone

- `js/app.js:3309` — the visible caption `passing is silence, not a dislike ·
  N of 16`. Visible text; changing it would move pixels, which this unit may not
  do.
- `js/app.js:3301` — `role="group" aria-label="Artwork N of 16 — subject"` on
  the card element. This is the card's structural identity, read when the user
  navigates into the group on purpose, not on every advance. Left as-is. **If
  the owner still hears position on every card, this is the next suspect** —
  named here so it is not re-diagnosed from scratch.

### DOM evidence

A full sixteen-card pass driven through the real UI in Chrome ended with the
live region reading:

```
The Naked Maja — Francisco Goya, c. 1797–1800. Artwork 16 of 16. Admire, or pass.
```

Card 16 announces the position, from the shipped code path, through the real
`say()` channel. Attempts to capture all sixteen strings in one run were
defeated by synthetic clicks failing to register on the tone step (a harness
limitation, not a product defect), so the cadence rule was verified instead
against the file as served over HTTP —
`curl http://localhost:8431/js/app.js?v=20260805-pig001-u34` returns the
predicate above at line 3256 — evaluated across all sixteen indices:

```
1 SAYS, 2 omits, 3 omits, 4 SAYS, 5 omits, 6 omits, 7 omits, 8 SAYS,
9 omits, 10 omits, 11 omits, 12 SAYS, 13 omits, 14 omits, 15 omits, 16 SAYS
```

### Outstanding

**Ear-confirmation of the cadence is outstanding**, including the judgement call
on card 1. If the owner wants the strict 4/8/12/16 reading, removing `n === 1`
from the predicate is the whole change.

---

## Checks

- `osascript -l JavaScript tools/validate.jxa.js` → `app.js: syntax OK`,
  `ALL REFERENCES VALID`, **zero warnings**.
- Cache-bust bumped to `?v=20260805-pig001-u34` on `css/styles.css` and
  `js/app.js` in `index.html`.
- **No visual change.** No CSS rule was altered (only a comment added); the
  `↳` glyph still computes; the JS changes add one attribute and gate one
  spoken substring.

## Files touched

`js/app.js`, `css/styles.css`, `index.html`, and this log.

## Cleanup

The one server this unit started (`python3 -m http.server 8431`, PID 6772) was
killed by exact PID and port 8431 confirmed free. The Chrome preview was stopped
by its own server id. **The owner's server on port 8422 was never contacted and
is still running (PID 93806).** No wildcard `rm` and no pattern-matched `pkill`
were used.

## Both items await the ear

Neither item in this unit is confirmed closed. The DOM evidence above shows the
glyph is out of the accessibility tree and the count is spoken five times
instead of sixteen; only a fourth VoiceOver session can confirm either by ear.
Recording them as closed on DOM evidence alone is the exact mistake that
produced this unit.
