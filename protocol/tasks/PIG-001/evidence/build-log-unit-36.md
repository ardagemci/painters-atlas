# Build log — PIG-001 unit 36

**Agent:** Dürer (`claude-implementation-lead`)
**Branch:** `pig-001-stabilization` (never `main`; not pushed)
**Parent:** `95e5636` (unit 35)
**Commit:** `4266804` — *PIG-001 unit 36: the OD-5 breach that shipped, and a guard that reaches it*
**Files:** `js/app.js`, `tests/test_rights_tooling.py`, `index.html`
**Gate 1:** `protocol/tasks/PIG-001/specification.md` → `workflow_state: "approved_for_build"`. Verified before any production edit.

## 1. Why this unit exists

OD-5 (`owner-decisions-r2.md`) binds the project to recording **asserted basis,
attribution and residual uncertainty, and never clearance**. Unit 35 corrected
fourteen overclaiming statements across evidence and docs and built
`TestProseLanguage` to keep them corrected. It left one breach standing —
`js/app.js:2393`, the `#/credits` lede — because the Data Steward does not own
that file, and because the guard's `SCANNED` list did not reach `js/`.

The result was an inversion: the evidence documents were disciplined and the
page a visitor actually reads was not. That is the defect this unit closes.

## 2. The lede — old and new, verbatim

**Old** (`js/app.js:2393`, section *Artwork images under a licence*):

> Most reproductions here are public domain. These ${imageIds.length} are photographs somebody licensed for reuse on condition of credit — usually a picture taken in the room, of a fresco, a ceiling or a sculpture, where the photographer's own work is part of what you see. The remaining ${freeImages} carry no attribution condition.

**New:**

> Most reproductions here carry Commons' public-domain assertion, and we checked each file really is the work it names — the source's claim and our own check, not a ruling we are qualified to make. These ${imageIds.length} are photographs somebody licensed for reuse on condition of credit — usually a picture taken in the room, of a fresco, a ceiling or a sculpture, where the photographer's own work is part of what you see. The remaining ${freeImages} carry no attribution condition.

Only the first sentence changed. It now names the two things we actually hold —
what Wikimedia Commons *asserts*, and what the exact-match check *confirmed* —
and closes the gap between them explicitly rather than by omission. It matches
the voice already established one section above (*"none of that is a legal
clearance we claim on your behalf"*), per `docs/STYLE_GUIDE.md` §3.4: state what
the source asserts, never the legal conclusion.

## 3. Other assertion corrected in the same view

`js/app.js:2377`, the Wikimedia Commons section:

- **Old:** "Most of the paintings **are old enough to be in the public domain**, and the photographs of them are offered under public-domain or CC0 terms — …"
- **New:** "Most of the paintings **are old enough that Commons files them as public domain**, and the photographs of them are offered under public-domain or CC0 terms — …"

Same principle: the status is attributed to the source rather than asserted by
us. The sentence's existing disclaimer ("none of that is a legal clearance we
claim on your behalf") is unchanged and still carries the residual-uncertainty
half of OD-5.

**`#/privacy` (`viewPrivacy`, lines 2290–2317): no correction needed.** Swept in
full. Its rights-adjacent sentence — "Artwork and museum images throughout
Pigment are sourced from Wikimedia Commons" — is a statement of provenance, not
of legal status, and the page's remaining claims are about storage, network
requests and fonts. No flat rights or legal assertion found.

**Noted, not changed (out of unit scope):** `js/app.js:1861` renders the artwork
source link with the label "public-domain image source". It is link text
describing the file's Commons basis rather than a sentence asserting a legal
determination, it is not on either swept view, and changing it would invalidate
the artwork-page screenshots as well. It passes the widened guard. Flagged here
so the Quality Reviewer can rule on it deliberately rather than inherit it.

## 4. How the guard was widened

`tests/test_rights_tooling.py`, `TestProseLanguage`:

1. **Scope.** `SCANNED` gained `ROOT / "js" / "app.js"` — "unit 36: the copy
   users actually read". `app.js` only, not all of `js/`: the data registries
   are generated records already governed by `TestRegisterLanguage`. The file is
   scanned whole — string literals *and* code comments — since both are prose
   this pole wrote. The class docstring records the reasoning.
2. **Negative fixture.** `test_the_guard_actually_catches_the_phrases_that_got_through`
   gained the shipped breach as a fixture — the old first sentence quoted in §2
   above, verbatim. It is caught by the existing pattern
   `\b(is|are|was|were)\s+(now\s+)?(in\s+the\s+)?public[- ]domain\b`.
3. **Positive fixture.** `test_bounded_language_is_not_flagged` gained the
   replacement clause verbatim ("Most reproductions here carry Commons'
   public-domain assertion, and we checked each file really is the work it
   names"). It is flagged by nothing — the guard encourages the wording it is
   trying to produce.
4. **Exemption pin.** `EXPECTED_EXEMPTIONS["tests/test_rights_tooling.py"]`
   12 → 13, for the one new exemption marker on the catch fixture, with a
   comment naming the reason. The pin failed first and was raised deliberately —
   the mechanism worked as designed.

### Proof the widened guard reaches the shipped copy

The old lede was written back into `js/app.js` and the scan re-run:

> ```
> FAIL: test_no_artifact_of_ours_asserts_a_legal_conclusion
> AssertionError: Lists differ: ['js/app.js:2393: <p class="page-lede" sty[171 chars]s\''] != []
>   js/app.js:2393: <p class="page-lede" style="font-size:1rem">Most reproductions
>   here are public domain. These ${imageIds.length} are phot
>       -> asserts a legal status; say 'Commons metadata asserts a PD basis'
> Ran 1 test — FAILED (failures=1)
> ```

The new lede was then restored and the scan passes. The guard fails on the
string that shipped and passes on the string that replaced it, at the real file
path and line — not only against in-test fixtures.

## 5. Checks

| Check | Result |
| --- | --- |
| `osascript -l JavaScript tools/validate.jxa.js` | `app.js: syntax OK` · `ALL REFERENCES VALID` · **zero warnings** |
| `python3 -m unittest discover -s tests` | **Ran 46 tests — OK** (46 passing, unchanged) |
| `git diff --stat` scope | `index.html` 4± · `js/app.js` 4± · `tests/test_rights_tooling.py` 25± — no unrelated changes |

`index.html` cache-busting bumped `?v=20260805-pig001-u34` → `?v=20260805-pig001-u36`
on both `css/styles.css` and `js/app.js`.

Untracked/unrelated files left alone as instructed: `THEORY_001.md`,
`passport-test.html`, `.gitignore`, and the two files under
`protocol/tasks/PIG-001/`. Commit used explicit paths only — no `git add -A`.
The owner's server on port 8422 (PID 93806) was not touched; no server was
started or stopped by this unit.

## 6. Deviation ledger

None. No product intent changed: the page reports the same facts about the same
images, bounded to what the evidence supports.

## 7. Action required — re-screenshot

**`#/credits` must be re-captured.** Two paragraphs of rendered text changed on
that view, so any existing `#/credits` screenshot is stale. This was known and
accepted before the edit: the screenshot pass has not yet run, which is why the
fix went now rather than after capture.

- **Layout, colour and geometry are untouched.** No CSS, no class, no inline
  style, no element structure changed — the diff is text inside two existing
  `<p>` elements. The contrast evidence for `#/credits` remains valid; the
  lede paragraph reflows one to two lines longer at narrow viewports.
- No other view's screenshots are affected.
