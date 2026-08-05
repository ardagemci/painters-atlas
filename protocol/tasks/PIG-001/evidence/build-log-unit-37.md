# Build log — unit 37 (Dürer)

Branch `pig-001-stabilization`, parent `7592136`. Scope: the two findings Van
Eyck held certification on — **F-9** (red suite at HEAD) and **F-2** (masked
focus ring on the narrow nav). Nothing else was touched. F-10, F-11, the
`.md-name` legibility item and AT-5 were explicitly out of scope and were not
opened.

Gate 1: `protocol/tasks/PIG-001/specification.md` line 8 reads
`workflow_state: "approved_for_build"`. Verified before any production edit.

---

## F-9 — the suite was red at HEAD

**Before:** `python3 -m unittest discover -s tests` → **46 tests, 1 failure**
(`TestProseLanguage.test_no_artifact_of_ours_asserts_a_legal_conclusion`).
**After:** **46 tests, 0 failures.**

### Diagnosis

One offence, in `protocol/tasks/PIG-001/evidence/harness/vermeer-cert/gapfill.py:28`:

> `OLD_LEDE = "Most reproductions here are public domain."`

(quoted as a blockquote, per the unit-35 mechanism — this log is scanned too,
and the guard caught this very line when it was first written as a code block)
matching the BANNED pattern `\b(is|are|was|were)\s+(now\s+)?(in\s+the\s+)?public[- ]domain\b`.

The question the brief asks — genuine overclaim, or legitimate quotation of a
previously corrected breach — resolves cleanly to the second, and the file says
so itself. `gapfill.py`'s own docstring (gap 2) states that `#/credits` changed
its visible text in unit 36 and that the recaptured screenshot is only evidence
of the new copy if the new copy was on the page at shutter time. The script
therefore asserts the rendered DOM **contains** `NEW_LEDE` and **does not
contain** `OLD_LEDE`. `OLD_LEDE` is a negative control. It is the string this
pole *removed*; holding it is how the harness proves it is gone.

Three things confirm it is not an overclaim:

1. The identical string is already sanctioned elsewhere. `tests/test_rights_tooling.py:594`
   carries it verbatim, under the same marker, as the unit-36 catch fixture in
   `test_the_guard_actually_catches_the_phrases_that_got_through`. The guard
   already accepts this exact sentence as a thing that must be quotable in
   order to be caught.
2. Every other surviving copy in the tree is already a preserved-and-corrected
   quotation: `build-log-unit-36.md:26` and `data-reconciliation.md:348` both
   hold it inside blockquotes, which is precisely the unit-35 mechanism, and
   both pass.
3. The shipped copy itself was corrected in unit 36. Nothing in the product
   asserts this any more. The only occurrences left are records of the
   correction.

`TestProseLanguage`'s docstring is explicit that the third exemption route
exists "for the few places that must contain a forbidden phrase in order to
forbid or test it." A `.py` file cannot use the blockquote route, so the marker
route is the one the design provides.

### Remedy

`gapfill.py:28` carries `# OD5-EXEMPT` with a four-line comment recording that
the string is the superseded lede, is quoted as a negative control, and is not
a claim this pole makes. The exemption is **pinned**, not loosened:
`EXPECTED_EXEMPTIONS` in `tests/test_rights_tooling.py` gains
`protocol/tasks/PIG-001/evidence/harness/vermeer-cert/gapfill.py: 1` with its
justification, so `test_exemption_markers_are_pinned` continues to fail if
anyone adds another.

**What was deliberately not done:** the BANNED list was not weakened, no
pattern was narrowed, no path was removed from `SCANNED`, and the guard's reach
is byte-for-byte what it was at `7592136`. The exemption count went from 16 to
18 — one for `gapfill.py`, one for this log, which names the marker while
recording the change exactly as `data-reconciliation.md` already does and
exempts no phrase of its own — and all 18 are named in the pin. Re-running the
guard against the unit-36 breach string still catches it (that test passes
unchanged).

The guard also caught **this log** while it was being written: the diagnosis
above first quoted the offending line as an indented code block, which is not
an exempt form, and the suite went red. That is the mechanism working, and the
line was moved into a blockquote rather than given an exemption.

---

## F-2 — the focus ring masked at the right edge of the narrow nav

### What was actually wrong (two mechanisms, not one)

A mask paints over an element's **own box**, not over its content. At ≤820 px
`.main-nav` is a single scrolling row with
`mask-image:linear-gradient(90deg,#000 78%,transparent)`, so whichever link
comes to rest in the last 22 % of the box has its focus ring faded out —
*regardless of scroll position*. On top of that, `overflow-x:auto` clips at the
padding box while an outline is painted **outside** the border box, so the ring
was also being cut off outright.

I tried the CSS-only route first and measured it failing. `scroll-padding-inline-end`
and `scroll-margin-inline-end` both only bite when the browser runs
scroll-into-view, and Chrome declines to run it for a link that is already
visible — which is exactly this case: the link is visible, it is merely faded.
Measured at 320 px with `scroll-padding-inline-end` alone, "Museums" still sat
at 88 % and "Movements" at 67 %. That approach is recorded here because it
looks correct and is not.

### The fix (mask untouched, content moved instead)

- `css/styles.css`, ≤820 block — `.main-nav::after` reserves a strip of
  scrollable space the width of the fade past the last link. At maximum scroll
  the strip, not a link, is what sits under the gradient, and the ring is no
  longer clipped by the scrollport. `scroll-padding-inline-end` matches it and
  handles the genuinely-off-view case.
- `css/styles.css` — `margin-inline-start:-6px; padding-inline-start:6px;
  flex-basis:calc(100% + 6px)`. The scrollport was also clipping the **first**
  link's ring on the left at `scrollLeft:0` (measured 94.3 %, 5 px cut). The
  box is widened 6 px to the left and the same 6 px handed back as padding, so
  the ring has room to paint and **every link stays exactly where it was** —
  first link measured at x=16 both before and after, row still ending flush
  with the header content box at x=304.
- `js/app.js` — a `focusin` handler on `#main-nav`, sibling to the existing
  `.ig-node` handler at the same place in the file and modelled on it. It
  early-returns when the computed mask is `none` (i.e. above 820 px), and
  otherwise scrolls the row by `Math.ceil` of the overlap needed to lift the
  focused link's ring clear of where the gradient starts. It never scrolls
  left and never scrolls the page.

**The mask is unchanged.** It still fades at every scroll position and the
scroll affordance unit 2 added is intact — confirmed visually at 320 px dark
(row reads `ARTISTS LISTS MUSEUMS EXPL…` with the right edge fading out).

### Measured ring extent

Visible extent = the share of the focus ring's outer box that is both inside
the scrollport and in the gradient's fully opaque region. A 5 px ring allowance
is assumed, which is conservative for Chrome's default focus ring. Each link
was focused in turn from `scrollLeft:0`, letting native scroll-into-view run
first, then the shipped handler.

| Viewport | Theme | Before — worst link | Before — last link (`Nations`) | After — every link |
| --- | --- | --- | --- | --- |
| 320×760 | dark  | `Explore` **0 %** (36.9 px clipped) | **25 %**, 4.9 px clipped | **100 %**, 0 clipped |
| 320×760 | light | `Explore` **0 %** (36.9 px clipped) | **25 %**, 4.9 px clipped | **100 %**, 0 clipped |
| 390×844 | dark  | `Movements` **0 %** (79 px clipped) | **0 %**, 24.9 px clipped | **100 %**, 0 clipped |
| 390×844 | light | `Movements` **0 %** (79 px clipped) | **0 %**, 24.9 px clipped | **100 %**, 0 clipped |

Geometry: at 320 px the nav box is 294 px and the gradient starts fading at
229.3 px; at 390 px the box is 364 px and the fade starts at 283.9 px. All 8
links reach 100 % in both themes at both widths. The two themes measure
identically because the defect is geometric; the ring's colour differs, its
extent does not.

Desktop unaffected, verified at 1280×800: computed mask `none`,
`margin-inline-start:0px`, `flex-wrap:wrap` still in force (AC18 needs it at
200 % zoom), no `::after` box, and the handler scrolled by 0 when the last link
was focused.

### Limitation on this measurement — read before relying on it

The Browser pane is not the system-focused window, so Chrome suppresses `focus`
/`focusin` dispatch (it still runs scroll-into-view). Direct keyboard input was
also unavailable — `computer{left_click}` timed out with the pane hidden. The
numbers above were therefore produced by focusing each link (native
scroll-into-view runs for real) and then dispatching a bubbling `focusin` on
it, which drives the **shipped** listener through its real registration,
guards, arithmetic and scroll write. What is *not* exercised is Chrome's own
emission of the event on a real Tab press, and `:focus-visible` never matched,
so the ring geometry is the assumed 5 px rather than a measured live ring.
**A real keyboard pass at 320 and 390 is worth having from Vermeer**, who has a
genuine browser session. I flag this rather than present the figures as a
keyboard-driven result.

---

## Stale screenshots

This changes rendered pixels in the header at ≤820 px only. The nav box now
starts 6 px further left (its links do not move) and the row has a trailing
scroll strip, so its scroll range and thumb width differ. Desktop captures at
1440×900 and 1280×800 are unaffected and remain valid.

**47 files matching `*mobile-390x844*.png` under
`protocol/tasks/PIG-001/evidence/` now show a pre-unit-37 header.** The page
content below the header is unchanged in all of them. Either re-capture them,
or state the limitation — the header strip is the only stale region, and no
acceptance criterion is evidenced by the header's scroll affordance.

No screenshot in the set showed a focused nav link, so none of them was
evidence for F-2 in the first place.

---

## Checks

- `osascript -l JavaScript tools/validate.jxa.js` → `app.js: syntax OK`,
  `ALL REFERENCES VALID`, **zero warnings**.
- `python3 -m unittest discover -s tests` → **46 tests, OK** (was 46 tests,
  1 failure at `7592136`).
- Versioned files bumped: `styles.css?v=20260805` → `?v=20260806`,
  `app.js?v=20260805-pig001-u36` → `?v=20260806-pig001-u37`. No prerendered
  file references either asset, so no `p/` regeneration is implied.

## Deviations

- **D-37-1.** F-2 was fixed partly in JS rather than wholly in CSS. The
  CSS-only route was attempted and measured insufficient (see above): Chrome
  will not scroll an already-visible link, so no scroll property reaches a link
  that is visible but faded. The alternative — dropping the mask on
  `:focus-within` — was rejected because the brief requires the affordance to
  survive, and it would remove it exactly while a keyboard user is in the nav.
- **D-37-2.** The first link's left-edge ring clip (94.3 %, 5 px) was not part
  of F-2, which reports the *last* link. It was found while measuring and
  fixed, because the brief's standard is "fully visible on every nav link" and
  the fix is two declarations with no positional change. Flagging it as a
  deliberate, in-scope-adjacent inclusion rather than burying it.
- **D-37-3.** No product intent changed. No acceptance criterion is affected.
