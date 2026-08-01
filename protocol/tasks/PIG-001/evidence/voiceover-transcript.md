# VoiceOver session — observed results (acceptance criterion 15)

**Operator:** Arda (human), VoiceOver on macOS, Safari, `http://localhost:8422`
serving `pig-001-stabilization` @ `56241d8`, light theme.
**Recorded by:** Synthesis Lead, from the operator's own report. Nothing here is
inferred, embellished, or produced by an agent. Where the operator did not
observe something, it is marked NOT TESTED rather than assumed.

This is the first and only assistive-technology evidence in PIG-001. Every prior
accessibility claim rested on DOM inspection and pixel measurement.

---

## What passed

| # | Behaviour | Observed |
| --- | --- | --- |
| 1 | **Route change announces the page once** | On reaching a new page it announces the level-1 heading and stops. **"It says it only once."** This independently confirms the C-8 fix (unit 25f removed the whole-page live region); the doubled/divergent announcement is gone. |
| 2 | Page structure is conveyed | Announces "link" before each navigation item, and reads headings with their level ("heading 1", "text"). |
| 3 | Search field label | Reads "Search artists, artworks, lists, museums, movements, techniques…" — the corrected label from unit 7 is reaching the screen reader. |
| 4 | **Search results are type-identified** | Typing `leonardo` announces artists, then their artworks, saying "not selected" between items. Operator: *"As it announced the type of item before starting to list them, I knew what was what."* |
| 5 | **The influence-graph bypass works** | "When I clicked on skip the graph, it skipped it. It landed past the graph." Confirms the unit-19 bypass past ~204 node stops. |
| 6 | **Graph node names are rich and correct** | Tabbing to a node announced "Leonardo da Vinci", his birth and death dates, how many connections he has and of what types, and that it is a button. Unit 12's accessible naming works better under real AT than its specification required. |
| 7 | **Onboarding interruption recovery works** | After reload mid-deck: *"It put me back where I was, not restarting the test with previous questions."* Confirms unit 18 under real AT. |
| 8 | **Malformed passport import is handled truthfully** | A deliberately corrupted share link produced: heading *"That passport didn't scan"*, body *"The link seems damaged. Nothing on this device has been changed. Ask for a fresh one, or start your own map."*, with a "Find your palette" button and "NO THANKS — TAKE ME HOME". Correct, and the truthfulness clause is satisfied: it states nothing was changed. |

---

## Findings — all new, none previously detected

### AT-1 (major) · The onboarding never says which artwork you are judging

> *"I was on Monet's Stacks of Wheat but it does not announce it."*

The taste deck asks the visitor to Admire or Pass on sixteen artworks. If the
artwork is not announced, a screen-reader user is asked to express a preference
about something they were never told. **The core product loop — the one the whole
Taste layer is built on — is not operable by a blind user.**

This is the most serious accessibility defect found in PIG-001, and no
DOM-or-pixel instrument found it in thirty-one units. Every prior check confirmed
the *controls* were reachable and named; none checked that the *subject* was
announced.

### AT-2 (major) · The skip link is not what the first Tab reaches

The build added a skip-to-main link, and browser evidence recorded it as the
first tabbable element with a visible focus state. Under VoiceOver the operator
reports the homepage announces its level-1 heading and stops, and **"When I Tab
once, it starts to list the nav sections"** — i.e. the first Tab lands in the
navigation, not on a skip control, and no skip control was announced.

Either the skip link is not first in tab order in Safari, or it is not being
announced when focused. **Direct contradiction between measured browser evidence
and observed assistive-technology behaviour** — precisely the class of error this
criterion exists to catch.

### AT-3 (major) · Dismissing search announces nothing

> *"It didn't say anything after I pressed esc."*

The frozen criterion requires dismissal and focus return to be *perceivable*.
Focus may well be returning correctly (unit 7 fixed the blur-to-body defect), but
a screen-reader user gets no confirmation that the results closed or where they
now are.

### AT-4 (minor) · The search field announces three conflicting roles

VoiceOver called it **"list box pop-up, menu pop-up combo box"**. Unit 14 applied
a full combobox/listbox/option pattern; the resulting announcement is
over-decorated and self-contradictory rather than simply "combo box". Suggests
redundant or conflicting ARIA attributes on the same element.

### AT-5 (minor) · Decorative arrows are read aloud

> *"It also mentions right arrows."*

The "→" characters in link text ("or surprise me →", "Go next →") are announced
as "right arrow". Decorative punctuation should be hidden from assistive
technology.

---

## NOT TESTED — stated, not assumed

- **Return-key activation on a graph node.** The operator pressed the browser's
  Back control rather than the Return key ("VO gets out of Pigment and focuses on
  the prompt I'm typing"), so node activation by keyboard was not exercised. The
  script's wording was ambiguous; this is a defect in my instructions, not in the
  operator's execution.
- **The passport import *conflict* path — the single most important fix in the
  build.** The deliberately altered share link was correctly rejected as damaged,
  which exercised the *malformed-input* path instead. The per-field
  keep-mine/take-theirs confirmation was therefore never reached. Requires a
  second valid passport to test; must be re-run before this criterion can be
  called satisfied.
- Reduced motion, dark theme, and 200% zoom under VoiceOver.
- Any screen reader other than VoiceOver; any browser other than Safari.

---

## Assessment

The session confirms five build fixes under real assistive technology and finds
**five defects, two of them major**, that thirty-one units of code inspection and
pixel measurement did not.

The pattern is consistent and worth stating plainly: our instruments verified
that **controls exist, are reachable, and are named**. They had no way to detect
that a control's **subject was never announced** (AT-1), that a measured tab
order does not survive contact with a real screen reader (AT-2), or that a state
change is silent (AT-3).

The theory pole was right to insist the frozen wording — *a tested
assistive-technology setup* — could not be satisfied by inspection.
