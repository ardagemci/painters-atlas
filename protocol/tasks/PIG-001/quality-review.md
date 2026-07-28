# PIG-001 — QUALITY REVIEW (Gate 2)

**Reviewer:** Van Eyck (`claude-quality-reviewer`), Quality and Accessibility Reviewer
**Branch:** `pig-001-stabilization` (verified: **not** `main`; no push, no merge)
**Standard:** the 29 acceptance criteria of `protocol/tasks/PIG-001/specification.md`,
frozen at `approved_for_build`. Nothing else. A criterion passes or fails; there is no
partial credit, and an untested criterion is not a passing criterion.

| Revision | Date | Tree | Verdict | Counts |
| --- | --- | --- | --- | --- |
| 1 | 2026-07-26 | `4fc8239` / `5fdf1aa` | GATE 2: BLOCKED | PASS 26 · FAIL 0 · UNSUPPORTED 3 (AC4, AC8, AC19) |
| **2 — operative** | **2026-07-28** | **`1a41cff` (HEAD)** | **GATE 2: BLOCKED** | **PASS 28 · FAIL 1 · UNSUPPORTED 0 (AC19 FAIL)** |

Revision 1 is preserved verbatim in the **ARCHIVE** below. Nothing in it has been deleted:
the record of what was blocked, and why, stands as written. Revision 2 supersedes only its
verdict and its criterion statuses.

---

# REVISION 2 (2026-07-28) — OPERATIVE

**Product tree reviewed at:** `1a41cff` (HEAD). Production code last moved at `3e24e4a`
(unit 28); `1a41cff` and `1e9a1ad` are evidence-only.

**Independence:** I wrote none of this code. I did not fix anything I found. This round I
re-derived the two contested bounds arithmetically myself from the committed CSS and the
committed canvas source rather than accept either implementer's or reviewer's numbers.

## R2.1 — What this revision is

Revision 1 blocked on three criteria for which no evidence existed. Since then:

| Was | Work | Now |
| --- | --- | --- |
| AC4 UNSUPPORTED (F-3) | Vermeer ran the frozen journey matrix — 33 steps, 0 FAIL (`evidence/browser-evidence-closing.md` §2) | **PASS** — F-3 closed |
| AC8 UNSUPPORTED (F-4) | Vermeer exercised storage failure with a passport present (`…closing.md` §3) | **PASS** — F-4 **retracted as my own false negative** |
| AC19 UNSUPPORTED (F-5) | Unit 27 (`563f0af`) museum photograph band; unit 28 (`3e24e4a`) two canvas call sites | **FAIL** — F-5 closed, **new F-7 opened** |

**The 26 passes of Revision 1 stand.** I re-tested only what the delta could disturb.
Units 27 and 28 are CSS-only (plus a `?v=` bump); they touch no data, no `js/app.js`, and
no layout geometry, so AC1–AC18 and AC20–AC29 cannot have moved except through the token
and scrim changes I trace below. I re-ran the validator and re-checked F-1 and F-2 directly.

## R2.2 — Checks I ran myself, with output

### R2.2.1 Validator — `osascript -l JavaScript tools/validate.jxa.js`

```
app.js: syntax OK
artists: 256, movements: 76, techniques: 39, eras: 8, nations: 37, painter styles: 27,
influence edges: 238, venues: 116, catalog: 323 (tier1: 76), daily pool: 75,
museum notes: 104, photo credits: 104 (attribution required: 88),
artwork image credits: 27, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```

Zero errors, **zero warnings**, all references valid — byte-identical to my Revision 1 run
and to units 27 and 28's own logs. AC2 continues to hold. N-3 (corpus counts differ from the
spec's frozen assumption, cause D-016) is unchanged.

### R2.2.2 Source spot-checks — units 27 and 28 verified in the file, not in the log

| Claim | Verified | Where |
| --- | --- | --- |
| `--mu-veil` exists, `.88` in **both** themes | **yes** | `styles.css:176` (dark), `:219` (light) |
| Veil is on the **text block**, not the hero box | **yes** | `styles.css:1244-1249` — `.mu-hero-body` gradient, 18 px feather |
| `.mu-shade` *reduced* to `.06→.30` (carries no contrast duty) | **yes** | `styles.css:1234` |
| Band breadcrumbs off `--faint` → `--muted` / `--body-ink` | **yes** | `styles.css:1257-1259`, scoped to `.mu-hero-body` |
| Light band gold `#6b5122`, hover `#4a3616` | **yes** | `styles.css:1272` and neighbours |
| Band focus ring re-pointed in light only | **yes** | `styles.css:1283`, `#app` specificity carried |
| `.sec-title .count` `--faint` → `--muted` (unit 28) | **yes** | `styles.css:431` |
| `.img-credit` / `.img-credit a` → `--body-ink` (unit 28) | **yes** | `styles.css:676-681` |
| Stylesheet `?v=` bumped for the shipped code | **yes** | `index.html:27` → `20260728-pig001-u28` |
| `js/app.js` untouched by both units | **yes** | `git show --stat 563f0af 3e24e4a` — `css/styles.css` + `index.html` only |

Both units are in the tree exactly as their logs describe. The one place a log corrected
itself against the routing note (`.img-credit` was already `--muted`, not `--faint`, so the
one-rung lift landed on `--body-ink`) is confirmed by the comment preserved at
`styles.css:671-675`.

### R2.2.3 I re-derived unit 27's `.88` bound myself

Unit 27 is the evidence that moves AC19's photograph sub-claim from FAIL to PASS, and Dürer
measured his own work. So I did not take his table. The veil is anchored to `.mu-hero-body`,
which makes the bound pure arithmetic on the committed tokens — `.88·bg + .12·worst-opaque-pixel`,
worst = white in dark, black in light, the rule Matisse set:

| theme | element | ink | floor | **my bound** | Dürer's | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| dark | `--ink` `h1.display` | `#ece6d9` | 3.0 | **11.66** | 11.66 | PASS |
| dark | `--body-ink` crumb link | `#d8d2c4` | 4.5 | **9.63** | 9.63 | PASS |
| dark | `--muted` `.mu-sub` + crumbs | `#9b937f` | 4.5 | **4.75** | 4.75 | PASS |
| dark | `--gold2` `.mu-hook` | `#e8c98a` | 4.5 | **9.08** | 9.08 | PASS |
| light | `--ink` `h1.display` | `#2b2620` | 3.0 | **9.72** | 9.72 | PASS |
| light | `--body-ink` crumb link | `#433c31` | 4.5 | **7.06** | 7.06 | PASS |
| light | `--muted` `.mu-sub` + crumbs | `#585244` | 4.5 | **5.03** | 5.03 | PASS |
| light | band gold `#6b5122` | — | 4.5 | **4.82** | 4.82 | PASS |

Every figure reproduces to the second decimal. **This is a bound, not a sample**, and because
the veil is anchored to the text block it is independent of hero height — which is the
structural reason one value serves 104 venues at both viewports, and why Dürer's 3,744
measurements found zero below floor rather than getting lucky. The binding constraints are
`--muted` at 4.75 dark and 4.82 light band gold; both clear, and both are thin margins that
should not be eroded by a later token change without re-measuring.

I also confirmed the fix by eye, comparing the committed pack shot against unit 27's:
`museum-louvre__desktop-1440x900__dark.png` shows the breadcrumb "Atlas / Museums / Musée du
Louvre" washed out over the collage; `u27-museum-louvre__desktop-1440x900__dark.png` shows it
legible on a veiled block with the photographs *more* present above it, not less. D-27-4's
claim that the photograph gained presence is true.

**F-5 is genuinely closed**, on a bound I derived myself.

### R2.2.4 I derived the canvas bound myself, from the committed CSS and canvas source

This is the contested question, so I did not rely on unit 28's model either. From the tree:

- `#bg-canvas` — `position:fixed; inset:0; width:100vw; height:100vh; z-index:-1; opacity:.5`
  (`styles.css:277-280`), `opacity:.6` in light (`:221`). It is behind the entire viewport on
  every route.
- `a{color:var(--gold2)}` (`styles.css:265`) — **`--gold2` is the global link colour**, and in
  light it is `#81632b` (`:199`).
- The canvas paints, in light, blobs `#a8813c #a85544 #4a6e9e #3e7a5e #6e3a5e` at α .10 and
  ribbons at α .10 (halo) and .18 (core), `source-over` (`js/app.js:2754-2758`).

Computed by me on flat paper first, to locate the headroom:

| light ink | on flat `--bg` | backdrop luminance it needs for 4.5 | flat paper L | headroom |
| --- | --- | --- | --- | --- |
| `--gold2` `#81632b` (= `a{}`) | **4.75** | 0.7944 | 0.8420 | **+0.0475** |
| `--faint` `#706755` | **4.74** | 0.7961 | 0.8420 | **+0.0459** |
| `--muted` `#585244` | 6.59 | 0.5587 | 0.8420 | +0.2833 |

Then my own composite of the canvas over the page:

| light backdrop | resulting L | `--gold2` | `--faint` | `--muted` |
| --- | --- | --- | --- | --- |
| **one** darkest blob at its centre (α .10 × .6) | 0.7645 | **4.34** | **4.33** | 6.02 |
| all five blobs overlapping | 0.5823 | **3.37** | **3.36** | 4.67 |
| five blobs + three ribbons (halo + core) | 0.3734 | **2.26** | **2.25** | 3.13 |

**A single blob is enough.** The most conservative assumption available — one blob, at its
own centre, no overlap, no ribbon — already puts the global link colour and `--faint` below
4.5 in the light theme. My figures bracket Dürer's model bound (3.22) and his measured range
(3.49–3.64) from both sides. This is not an instrument artefact and not a worst-corner
contrivance: `--gold2` and `--faint` sit on **4.7-ish on flat paper**, roughly 0.046–0.048 of
luminance from the floor, and the canvas that sits behind everything spends that margin
several times over.

### R2.2.5 Contrast audit re-run — and the blind spot that explains 28 units

`python3 evidence/contrast-audit.py`, run in full, read with the caution Revision 1 established:

- **Pass 1 (parses `css/styles.css` live) — current, and clean.** 19 tokens per theme over
  four surfaces, all PASS.
- **Pass 2 (`contrast-pairs-measured.csv`) — still stale.** Regenerated at `a018fe2`, before
  unit 26. It still prints the three `#9e7938` gold-as-small-text rows unit 26c fixed.
- **Pass 3 (browser-sampled pixels) — still stale.** It still prints the dark hero at
  **1.10:1 FAIL**, a state unit 26a fixed and that Vermeer independently re-measured at 4.62
  bound / 5.14 observed. Its five "composite FAIL" summary lines describe a build two units old.

Treating the script's summary as current would be wrong, and I do not.

**New and material, though:** Pass 1's surface set is `--bg`, `--bg2`, `--panel`, `--panel2`
— **flat paint only**. `#bg-canvas` is not among them and never has been. Pass 1 reports
`--faint` over `--bg` at 5.20 dark, and light `--faint`/`--gold2` at ~4.74/4.75, all PASS —
which is exactly the clearance unit 26c and Vermeer's §5.4 gold sweep relied on. **That
clearance was against a surface that is not what these tokens actually paint on for about a
third of the site's text.** This is the structural reason the canvas class survived 28 units
undetected, and it means the audit's clean Pass 1 must never again be read as clearing tokens
site-wide. It clears them over panels.

### R2.2.6 AC8 — I checked Vermeer's reasoning rather than accepting it, and it is half right

Vermeer says my F-4 was a false negative because "my probe had no passport to fail against".
**I traced the write-failure path in source, and that explanation does not hold for the case
I actually probed** — but the conclusion is still correct, for a different reason:

- `passportToggle` (`app.js:110-118`) does `getPassport() || newPassport()`. **With no passport
  present it builds one**, mutates it, and calls `ppWrite`.
- `ppWrite` (`:90-97`) then hits the throwing `setItem`, catches, sets `ppState.write="failed"`,
  returns false.
- The click handler at **`app.js:2481-2482`** is unconditional: `if(on === null){ ppNotice(PP_WRITE_MSG); return; }`.
  There is no passport-presence gate anywhere on this path.

So the notice **was** raised during my probe. I missed it because `ppNotice` (`:126-140`)
creates `#pp-notice` lazily and appends it to `document.body` — outside `#app` — styled
`position:fixed; bottom:16px; z-index:60` (`styles.css:1108-1114`). I inspected the route
view and the button's `aria-pressed`; a body-level fixed toast was outside where I looked.
**F-4 was my probe's error, and I retract it.**

Vermeer's stated reason *is* correct for the **corrupt-read** half (his S2): my corrupt probe
was genuinely inconclusive because there was nothing stored to corrupt.

This matters beyond bookkeeping: because the affordance is raised unconditionally in code, AC8's
recovery clause does not depend on a seeded passport, which is a stronger result than his
transcript alone shows. I further confirmed in source the three affordances he clicked
(`data-tsx="export"`, `href="#/taste"`, `data-tsx="notice-close"`, `:133-138`), the
corrupt/denied branch split (`:3392-3402`, `:3415`), and the no-silent-overwrite guard
(`ppWrite`'s first line: `if(ppState.corrupt || ppState.read === "denied") return false;`) —
the build refuses to write over data it could not read. **AC8 passes.**

### R2.2.7 F-1 and F-2 re-checked at HEAD

- **F-1 (821–1100 px overflow).** `git diff 4fc8239..HEAD -- css/styles.css` contains **zero**
  hits for `daily-media`; the rule is unchanged at `styles.css:879-884`. The finding stands
  exactly as recorded, and adjudication **A1** is unaffected.
- **F-2 (masked focus ring on the last nav link, ≤820 px).** The mask is still present and
  unchanged — `linear-gradient(90deg,#000 78%,transparent)`, now at `styles.css:1176-1177`
  (moved from `:1156` only because units 27/28 inserted rules above it). The finding stands
  as recorded, minor.

## R2.3 — Adjudications added this revision

### A7 — AC4: **PASS**

The transcript F-3 said did not exist now exists and I read it in full
(`browser-evidence-closing.md` §2, raw at `harness/vermeer-closing/ac4-journeys.json`).
It covers all five frozen journeys of `ux-requirements.md` §5 **and** AC4's own eleven-link
chain — 33 steps, 0 FAIL, driven with real CDP mouse and key events rather than JavaScript
shortcuts. The three links Revision 1 named as never exercised end to end are all there and
all substantive: **consequence explanation** (`#/taste` stating "9 admirations inform it"),
**export/share** (a 4,747-char `.json` and a share URL produced through the build's *own*
clipboard fallback), and **reset** (confirm copy, then `localStorage.getItem` returning `null`).
Conflict handling shows per-field keep/take **plus** an explicit "Cancel — change nothing",
and the merge is a union that removes nothing. No broken or unexplained transition.

This is the one criterion I certify **entirely on another reviewer's observation.** I did not
re-walk the 33 steps. What I checked is that the transcript is specific enough to be falsifiable
— it names counts, labels, `aria-pressed` transitions and stored-key states at each step, and
it records a method correction against itself (an anchor-click override that had disabled the
very link it was measuring, re-run cleanly). Evidence that reports its own instrument's failures
is evidence I extend credit to. **AC4 passes.**

I adopt his note N-V1: `ux-requirements.md` §5 still describes `#/explore` as offering two
instruments where the build offers four. The frozen table is stale in the *build's favour* and
this is what AC22 required; it is a documentation correction, not a defect.

### A8 — AC8: **PASS**, F-4 retracted

See R2.2.6. All five AC8 clauses are satisfied and I verified the mechanism in source rather
than on report: no false success (`aria-pressed` stays `false`, label unchanged), context
preserved (bytes byte-identical, 436→436), truthful notice (`role="status"`, "Nothing already
saved has changed."), and a retry / recovery / **export** path. The corrupt branch preserves
the stored bytes rather than wiping them and offers a verbatim download — which is better than
the criterion asks for. **AC8 passes.**

### A9 — The canvas class: **a live AC19 failure. It blocks.** (F-7)

This is the decision I was asked to make and not defer, so here is the reasoning in full.

**The frozen text.** AC19 reads: *"Both themes pass applicable WCAG 2.2 AA contrast checks for
the frozen text, control, focus-indicator, and state pairs, including composites that require
browser measurement."* (`specification.md:64`.)

**Why the F-1 analogy does not transfer.** I ruled the 821–1100 px overflow a note because
**AC18 enumerates its own test conditions** — "320, 390, 768, 1280, and 1440 CSS pixels and at
200 percent text zoom" — and the specification's Frozen Inventories repeat those five widths.
900 px is outside a set the criterion itself names, and widening it at certification time would
be me rewriting a frozen standard. That escape hatch is textual, and it is the whole basis of A1.

**AC19 has no such enumeration.** I checked: the Frozen Inventories freeze routes, control
types, journeys, checkpoints, viewports, the search fixture, asset surfaces, the rights sample,
the historical sample and third-party hosts. **They do not freeze a contrast-pair inventory.**
There is no list from which the canvas class is absent. And the criterion's trailing clause —
"including composites that require browser measurement" — reaches *toward* this class rather
than away from it: text over a `position:fixed` generative canvas is the paradigm case of a
composite that token maths cannot reach, which is precisely why Pass 1 of the audit never saw it.

**The failure is real and I reproduced it independently.** R2.2.4: a single blob at its centre,
the most conservative assumption available, puts light `--gold2` at **4.34** and `--faint` at
**4.33** against a 4.5 floor; realistic overlap gives 3.37/3.36. `--gold2` is `a{}`, the global
link colour. `#bg-canvas` is fixed to the viewport at `z-index:-1` behind every route, and unit
28's enumerator — deciding membership by paint differential, not rect overlap, which is the
sound method — found **1,346 of 3,755 text elements** painting over it across 19 routes. This is
not an edge case reachable only by a contrived draw. It is roughly a third of the site's text,
and in one of two shipped themes the global link colour is among it.

**Why "pre-existing" does not excuse it here.** It is true and I record it: these failures
pre-date PIG-001, and this build measurably improved contrast rather than degrading it. But
that argument proves far too much in this task specifically. The dark home hero at 1.10:1 was
pre-existing. The six gold-as-small-text sites were pre-existing. The museum photograph band —
the F-5 I blocked on in Revision 1, and which units 27 and 28 exist to answer — was pre-existing.
**Pre-existence has not once been accepted as an excuse across units 25, 26, 27 or 28.** Adopting
it now, at the last criterion, only because the remaining work is inconvenient, would be lowering
the bar at exactly the moment it is load-bearing. My own Revision 1 standard governs: *"a
criterion-named composite class is unmeasured and its worst case fails."* The class is now
measured, and it fails.

**The implementer does not claim it.** Unit 28's self-assessment says plainly: *"AC19 is NOT
fully supported."* Dürer checked and rejected the obvious lever (the canvas would have to become
near-invisible — I confirmed the arithmetic: `--faint` needs the light backdrop held above
L≈0.796 against flat paper's 0.842, so almost the entire canvas contribution would have to go),
and specified a fix he correctly declined to implement on his own authority because retiring
`--faint` and re-pointing the global light link colour is visual direction, not an implementation
choice. Certifying a criterion the implementer refuses to claim, over his own written FAIL, on
reasoning he already tested and rejected, is not something an independent gate can do.

**Ruling: AC19 FAILS.** Not "unsupported" — Revision 1's word, when nobody had measured it —
but **FAIL**, because it has now been measured, by three instruments and independently by me.
Recorded as **F-7 (major)**.

I record what is *not* in dispute, so the fix is not over-scoped: the museum band (unit 27),
the home hero (unit 26a), the six re-pointed gold sites (unit 26c), the two call sites unit 28
closed, and the band focus ring all pass and are independently corroborated. **The open failure
is a token question, not a re-design**: `--faint` as a small-text colour over the canvas, and
the light `--gold2` link colour. Dürer's option (a) — fold `--faint` into `--muted` over the
canvas and re-point light `--gold2` to `#6b5122`, already in the palette from unit 27 — is the
smaller and more reversible of the two he costed, and matches the rung-lifting remedy used in
26a, 27 and 28. It needs Matisse's sign-off as visual direction, and it must be re-measured
with unit 28's instruments in **both** themes and at **both** viewports, not inferred.

**One thing the fix must not do:** `--muted` is the rung `.sec-title .count` was just lifted
onto, and its own bound is 4.54 dark / 4.47 light, with 4.47 measured on `p.page-lede` at dark
390. Folding `--faint` into `--muted` moves failing text onto a rung that is itself marginal.
Whoever routes this should treat `--muted` over the canvas as in scope, not as the destination.

### A10 — N-1 (screenshot pack): **re-opened. Still a note, not a blocker.**

The pack was re-captured at `64d68a0` and the two surfaces I named are now correct — I verified
by eye, not by timestamp, and Revision 1's complaint is answered.

**But it is behind the code again, by two units.** The pack's files carry mtimes of
2026-07-26 13:19–13:21; unit 27 committed 2026-07-27 02:23 and unit 28 2026-07-28 12:07. I
opened `museum-louvre__desktop-1440x900__dark.png` and it shows the **pre-veil** band, with the
breadcrumb washed out over the collage — the F-5 failure state. Unit 28's `.sec-title .count`
and `.img-credit` changes appear on no shot in the pack at all. Unit 27 shipped its own four
`u27-museum-*` captures, which *are* current for the band but pre-date unit 28.

**Ruling: note, not a blocker**, on the same reasoning as Revision 1 — the stale shots understate
the build, I verified the affected surfaces myself by derivation and by comparing the unit-27
captures, and no criterion turns on a picture. But the spec's evidence package requires
"desktop/mobile × dark/light screenshots" with Gate-2 certification, and a reader of the current
pack would conclude the opposite of the truth on the museum surfaces. Because AC19 work must
continue anyway, **the pack should be re-captured exactly once, at the final HEAD**, rather than
chased per unit. If it is not re-captured before the Human Review Package, that becomes a
certification defect in its own right.

### A11 — Units 27/28 independence: **one real gap, and it is not load-bearing**

Vermeer independently verified units 25–26. Nobody but Dürer has verified 27–28. That is the
same arrangement that let round 1's 500 px capture defect survive two rounds, and I flagged it
in N-1 for unit 26. It recurs here. What settles whether it leaves anything unsupported:

- **Unit 27 — covered, by me.** Its result is a *bound*, not a sample, and I re-derived every
  figure in it myself (R2.2.3), matching to the second decimal. Because the veil is anchored to
  the text block, the bound is height-independent, so the 3,744-measurement sweep is
  corroboration on top of arithmetic I verified rather than the load-bearing claim. He also
  inherited Vermeer's corrected instrument rather than building his own and reproduced Vermeer's
  BEFORE figures (`a` 1.33, `span.sep` 1.31, `div.mu-sub` 3.23) to two decimals — cross-operator
  agreement on the instrument. I additionally confirmed the visible result by eye. **Not unsupported.**
- **Unit 28's *fixes* — covered, by construction.** Both call sites moved to rungs whose
  clearance I can check directly, and the direction of change is unambiguous. Its model
  reproduced unit 27's independently-instrumented 4.18 figure exactly. **Not unsupported.**
- **Unit 28's *sweep* — this is the real gap, and it points the safe way.** The 3,755-element
  census ran in **light @1440 only**; the dark enumeration and the 390 enumeration were not run,
  and two 390 AFTER cells for `.sec-title .count` rest on a token-level number rather than a
  direct observation (D-28-5, stated honestly in the log). But every gap here is a gap in
  *finding more failures*, not in confirming a pass. An under-run sweep cannot manufacture F-7;
  it can only have missed additional members of it. Since F-7 blocks regardless, the gap changes
  no verdict — but it means **the eventual fix cannot be verified by re-running this sweep alone**.
  Whoever closes F-7 must run the enumerator in dark and at 390 as well, and that verification
  should be done by someone other than its implementer.

**Ruling:** unit 27 and unit 28's fixes are adequately supported, by my own derivation rather
than by their author's assertion. The unrun halves of unit 28's sweep leave no criterion
unsupported *today*, but they are a condition on the AC19 re-certification, recorded as N-5.

### A12 — F-1 and F-2 stand as I left them

Both re-checked in the tree at HEAD (R2.2.7) and unchanged by units 27–28. F-1 remains a minor
finding outside AC18's frozen viewport set (adjudication A1 unchanged); F-2 remains a minor
degradation of focus *visibility*, not its absence, on a control that predates the build.
Neither blocks. Both belong in the Human Review Package as scheduled follow-ups.

## R2.4 — ACCEPTANCE CRITERIA — ALL 29, CURRENT

**PASS 28 · FAIL 1 · UNSUPPORTED 0**

| # | Criterion (abbrev.) | R1 | **R2** | Evidence |
| --- | --- | --- | --- | --- |
| AC1 | effa805 baseline named, older labelled historical, deployed-identity proof defined | PASS | **PASS** | unchanged |
| AC2 | Validator: no errors, refs valid, unedited snapshot | PASS | **PASS** | **my run, R2.2.1** — zero errors, zero warnings |
| AC3 | Two deck warnings cleared on merit or owner exception | PASS | **PASS** | `deck-merit-review.md`; my validator run confirms 0 warnings |
| AC4 | Frozen first-user journey matrix, no broken/unexplained transition | UNSUP | **PASS** | `browser-evidence-closing.md` §2 — 33 steps, 0 FAIL, five journeys + the eleven-link chain. **Adjudication A7**; F-3 closed |
| AC5 | Import: per-field identify, explicit confirm, cancel/malformed preserves local | PASS | **PASS** | round 1 + AC4 chain links 9–10b (per-field keep/take **plus** cancel; union merge) |
| AC6 | Admire/Seen/Saved independent, accurate visible + programmatic state | PASS | **PASS** | round 1; AC4 J2 — `admirations` flips, `seen`/`saved` stay `false` |
| AC7 | Five interruption checkpoints resume exactly | PASS | **PASS** | Vermeer round 1, 5/5; wave-c U18. Not re-run in the closing pass (his NOT TESTED #10); carry-forward legitimate (A5) |
| AC8 | Storage failure: no false success, context preserved, retry/recovery/export offered | UNSUP | **PASS** | `…closing.md` §3 + **my source trace, R2.2.6**. **Adjudication A8**; F-4 retracted |
| AC9 | Invalid-route/no-match/empty/limit/failure preserve context + next action | PASS | **PASS** | unchanged; AC8's trouble views strengthen it |
| AC10 | Frozen asset inventory, exact counts by surface + reachability | PASS | **PASS** | unchanged |
| AC11 | Item-level rights sample ≥100 incl. Tier1∪daily + all Matisse/Kahlo | PASS | **PASS** | unchanged — 122 entries, nine fields each |
| AC12 | Mismatches/unresolved/out-of-sample stay explicitly unresolved | PASS | **PASS** | unchanged |
| AC13 | Historical sample: 10 profiles, ≥5 eras/movements/nations, 5 claim classes, 20 edges | PASS | **PASS** | unchanged |
| AC14 | Release language checked, no overclaim | PASS | **PASS** | unchanged |
| AC15 | Title updates, one identity to AT, focus to entry point, no repeat announcements | PASS | **PASS** | my R1 §2.6 (5/5, 0 live regions); re-confirmed at HEAD by `…closing.md` §7. Real screen-reader output NOT TESTED (A6) |
| AC16 | Selected/current/expanded/pressed/active: visible + programmatic, not colour/position/hover alone | PASS | **PASS** | unchanged. **See F-7 caveat:** `a.active` measures 4.47 over the canvas in light 390 — a contrast defect, not a semantics defect; scored under AC19 |
| AC17 | Keyboard-operable with visible focus; bypass; no nested interactive | PASS | **PASS** | unchanged; unit 27's band focus ring re-derived by me as an improvement (light 4.98/4.94 vs 2.60). F-2 minor, re-checked |
| AC18 | 320/390/768/1280/1440 + 200 % zoom: destinations reachable, no root overflow | PASS | **PASS** as frozen | unchanged; 200 % zoom 0/26 at 1280 and 1270 (`…closing.md` §5.3). 821–1100 band outside the frozen set → **A1**, F-1 |
| AC19 | Both themes pass AA for frozen text/control/focus/state pairs **incl. browser-measured composites** | UNSUP | **FAIL** | Photograph band **now PASSES** (unit 27; **bound re-derived by me, R2.2.3**) — F-5 closed. **But `--faint` small text and the light global link colour `--gold2` fail over `#bg-canvas`** — 3.45–4.39 measured, 3.22/3.69 bound, **reproduced independently by me at 4.33/4.34 from a single blob** (R2.2.4). **Adjudication A9 · F-7** |
| AC20 | Reduced motion preserves info/choices; canvas + relationship viz have alternative + accessible name | PASS | **PASS** | unchanged; units 27–28 add no transition or animation |
| AC21 | Frozen fixture, six classes, no starvation, count/selection/dismissal/focus-return | PASS | **PASS** | unchanged — wave-c 24/24 + my own six-class re-run |
| AC22 | Home Explore promise = Explore destination; every instrument reachable | PASS | **PASS** | my R1 §2.7; re-confirmed by AC4 J5 (four cards, four routes) |
| AC23 | Named adjudicator reviews hierarchy/relationship/entrances/identity without claiming comprehension | PASS | **PASS** | **A4** unchanged. N-2 stands, and now widens: Matisse has not seen units 26–28 either |
| AC24 | ≥1 relationship journey: named entities, relationship + consequence, anchor, onward path | PASS | **PASS** | strengthened by AC4 J1/J5 — chip → movement → back with the anchor intact; `#ig-info` lineage with an onward link |
| AC25 | Every third-party runtime request identified; undisclosed fails | PASS | **PASS** (disclosure) | `…closing.md` §7 at HEAD — `upload.wikimedia.org` only, 0 Google Fonts. Deployment-gated condition remains open as **F-6** |
| AC26 | Criterion-to-unit matrix, defect/deferred register, rollback, cache/versioning | PASS | **PASS** | unchanged; `?v=` uniformity maintained through u27/u28 |
| AC27 | Fresh IL assessment confirms buildability, doesn't lean on the 14-unit plan | PASS | **PASS** | unchanged |
| AC28 | No legal conclusion from death year/host/attribution alone | PASS | **PASS** | unchanged |
| AC29 | No production edit before `approved_for_build`; merge/deploy need explicit approval | PASS | **PASS** | branch verified `pig-001-stabilization` at HEAD; units 27–28 committed by explicit path; no merge, no push, no deploy |

## R2.5 — FINDINGS LEDGER (full history)

### CRITICAL — 0

### MAJOR — 1 open

#### F-7 (major, **open**) · AC19 · `--faint` small text and the light global link colour fail over `#bg-canvas`

`#bg-canvas` (`styles.css:277-280`, `position:fixed; inset:0; z-index:-1; opacity:.5` dark /
`.6` light) sits behind every route. Unit 28's census found **1,346 of 3,755 text elements**
painting over it across 19 routes, membership decided by paint differential rather than rect
overlap. Measured below floor, with a 4.5 body-text floor:

| theme | viewport | class | ink | measured |
| --- | --- | --- | --- | --- |
| light | 390 | `div.chip-label` | `--faint` | 3.45 |
| light | 390 | **`a` (global link)** | `--gold2` | 3.49 |
| light | 1440 | `div.page-kicker` | `--gold2` | 3.53 |
| light | 1440 | **`a` (global link)** | `--gold2` | 3.64 |
| light | 1440 | `div.chip-label` | `--faint` | 3.72 |
| light | 390 | `div.page-kicker` | `--gold2` | 3.77 |
| light | 390 | `a.active` | `--gold2` | 4.47 |
| dark | 1440 | `div.chip-label` | `--faint` | 4.39 |
| dark | 390 | `p.page-lede` | `--muted` | 4.47 |

Whole-surface model bound over 24 draws on plain `--bg`: `--faint` **3.69** dark / **3.22**
light; `--gold2` **3.22** light; `--muted` 4.54 dark / 4.47 light.

**Reproduced independently by me** (R2.2.4) from the committed CSS and `js/app.js:2754-2758`:
a *single* darkest blob at its own centre, α .10 through element opacity .6, puts light
`--gold2` at **4.34** and `--faint` at **4.33**. Both inks sit ~4.75 on flat paper, about
0.046 of luminance above the floor; the canvas spends that several times over.

`--faint` is not two call sites: it also paints `.chip-label`, `.f-label`, `.map-hint`,
`.daily-return`, `.aw-provenance`, `.footer-note`, `.tl-year`, `.tn-count`, `.tm-lab`,
`.footer-nav a` and the search placeholder over the canvas. `--gold2` is `a{}`
(`styles.css:265`) — the global link colour.

**Reproduction:** serve the repo; load any route in light theme; read the composited backdrop
under a link or a `.chip-label` with the three-shot glyph diff (`evidence/harness/durer-u28/canvastext.py`),
or compute it: `#81632b` over `.6·blob(#6e3a5e, α.10)` on `#f2ecdf`.

**Why it is FAIL and not a scoped-out note:** adjudication **A9**. In short — AC18 enumerated
its viewports and 900 px was outside them; AC19 enumerates no pair inventory and its
"composites that require browser measurement" clause reaches this class directly. Pre-existence
was not accepted as an excuse for the dark hero, the six gold sites, or the museum band, and
cannot be accepted for the last one.

**Remedy (not applied by me, and requiring Matisse's sign-off as visual direction):** Dürer's
option (a) — retire `--faint` as a small-text colour over the canvas and re-point light
`--gold2` to `#6b5122`. Lowering canvas opacity does not work; he checked and I confirmed the
arithmetic. **`--muted` must be treated as in scope, not as the destination** — its own bound
is 4.47 light / 4.54 dark.

### MAJOR — closed this revision

#### F-5 (major) · AC19 · text over Wikimedia photographs — **CLOSED by unit 27, verified by me**

Raised in Revision 1: a criterion-named composite unmeasured across 116 venues, whose worst
case I bounded at `.mu-sub` 2.44:1. Unit 27 moved the scrim from the hero box onto the text
block (`--mu-veil:.88`, `styles.css:1244-1249`), lifted the band's breadcrumbs off `--faint`,
and re-pointed the light band gold. **I re-derived the bound myself** (R2.2.3) and reproduce
Dürer's table to the second decimal; his sweep adds 3,744 measurements over 416 venue-loads
with zero below floor, at both viewports, and 390 px proved *worse* than 1440 rather than
inheriting from it. The photograph is more present than before, not less. **Closed.**

#### F-3 (major) · AC4 · the journey-matrix transcript did not exist — **CLOSED**

It now exists and I read it in full: `browser-evidence-closing.md` §2, raw at
`harness/vermeer-closing/ac4-journeys.json`. 33 steps, 0 FAIL. **Closed** (adjudication A7).

### MINOR — 2 open, 1 retracted

#### F-1 (minor, open) · pre-existing horizontal overflow at 821–1100 px on `#/`

Unchanged and re-verified at HEAD: `.daily-media` (520 px fixed) is untouched by every commit
since `4fc8239`. Root `scrollWidth` 1008 vs `clientWidth` 890 at 900 px. Outside AC18's frozen
viewport set (**A1**), pre-dates PIG-001, and the band includes 1024 px. Schedule it.

#### F-2 (minor, open) · AC17 · the last nav destination's focus indicator is faded by the mask, at ≤820 px

Unchanged and re-verified at HEAD: `styles.css:1176-1177`, `linear-gradient(90deg,#000 78%,transparent)`
on a `overflow-x:auto` box, so whatever link sits at the right edge is faded even when scrolled
fully. Measured in Revision 1 at α≈0.52 (390 px) and ≈0.16 (673 px). Focus is degraded, not
absent; the control predates the build. Minor. **Suggested remedy, one line, not applied:** drop
the mask when the container is scrolled to its end, or apply it to the scrolling content.

#### F-4 (minor) · AC8 · **RETRACTED — my own false negative**

I reported no user-visible recovery affordance on write failure. There is one, and it is raised
unconditionally at `app.js:2481-2482`. I missed it because `#pp-notice` is appended to
`document.body` outside `#app` as a fixed bottom toast, and I inspected the route view. See
R2.2.6 — including my correction to Vermeer's stated explanation, which holds only for the
corrupt-read half. **Withdrawn with the reason recorded.**

### NOTE

#### F-6 (note) · AC25 · deployment-gated disclosure condition

Recorded for completeness: Revision 1's AC25 row referenced "F-6" without defining it — my
drafting slip, corrected here. The condition is that AC25 passes **on disclosure** against a
locally served build; nothing in this review proves what a deployed GitHub Pages build serves
(Vermeer's NOT TESTED #11). Confirming third-party request identity at the deployed origin is a
pre-deployment step, not a Gate 2 condition.

#### N-1 (note, **re-opened**) · the screenshot pack is behind the code again, by two units

Re-captured at `64d68a0` and the two surfaces I originally named are now correct. But units 27
and 28 shipped afterwards: `museum-louvre__*` in the pack still shows the **pre-veil** band
(I opened it and compared against `u27-museum-louvre__*`), and no shot depicts unit 28 at all.
Not a blocker (**A10**) — the stale shots understate the build and no criterion turns on a
picture — but the pack must be re-captured **once, at final HEAD**, before the Human Review
Package, or a reader will conclude the opposite of the truth on the museum surfaces.

#### N-2 (note) · Matisse adjudicated on round-1 evidence, and the gap has widened

AC23 stands (**A4**), but his record now pre-dates units 25 through 28, including two changes in
his own domain: the museum band's treatment and the token rungs. He has never seen the corrected
mobile captures he asked for. F-7's remedy requires his sign-off in any case, which is the
natural occasion to refresh the record.

#### N-3 (note) · corpus counts differ from the frozen specification assumption

Unchanged: spec assumed 247/75/317/225; HEAD reports 256/76/323/238, cause D-016 (Sol's
`ef8b2b3` landing mid-build), recorded and accepted. Flagged only so the Human Review Package
does not present the spec's assumption line as current.

#### N-4 (note, **new**) · `browser-evidence-closing.md` ships with four unresolved placeholders

The committed file — the evidence of record for AC4 and AC8 — contains literal
`<!--PLACEHOLDER-DARK-->` (line 86), `<!--PLACEHOLDER-LIGHT-->` (88),
`<!--PLACEHOLDER-FINDINGS-->` (393) and `<!--PLACEHOLDER-VERDICT-->` (463), present in the
committed object at `73ddc27` as well as on disk. So §1.2's AC19 dark and light measurement
tables, the entire §6 findings section, and §9's verdict **are missing from the document**.

This does not disturb AC4 or AC8: §2 and §3 are complete, specific and self-consistent, and
they are what those criteria rest on. The missing §1.2 tables describe F-V1, which unit 27 has
since closed and which I re-derived myself. But an evidence artifact in a certification package
must not ship with unrendered template markers — a reader cannot tell a placeholder from a
deletion. **Repair before the Human Review Package.**

#### N-5 (note, new) · unit 28's census was run in light @1440 only

19 routes, 3,755 elements, 67 ink groups — **light theme at 1440 only**. Not run in dark, not
run at 390; two 390 AFTER cells rest on a token-level number rather than an observation (D-28-5,
disclosed in the log). This cannot have manufactured F-7 — an under-run sweep only misses
failures — so it leaves no criterion unsupported today. But **the fix for F-7 cannot be verified
by re-running this sweep alone**: the enumerator must be run in dark and at 390, and by someone
other than the implementer (**A11**).

## R2.6 — REGRESSION SWEEP AT HEAD

- **Validator:** clean, zero warnings, all references valid (R2.2.1). Identical to Revision 1.
- **26 routes at `64d68a0`** (`…closing.md` §7): 26/26 reached, **0** console errors, **0**
  warnings, **0** requests ≥400 of 112, **680** images checked with **0** broken,
  `upload.wikimedia.org` the only third-party host, **0** Google Fonts. Units 27 and 28 landed
  after that sweep, but both are CSS-only and neither adds a request, a script or an element —
  `git show --stat` confirms `css/styles.css` + `index.html` only, with `js/app.js` untouched
  and its `?v=` unchanged. I accept the sweep as carried forward on that reasoning, stated so it
  is auditable.
- **Changed surfaces did not break neighbours.** Unit 27's rules are confined to `.mu-hero-body`,
  `.mu-shade` and band-scoped breadcrumb/focus overrides; `.breadcrumbs` outside the band keeps
  `--faint` on opaque paint (`styles.css:1256` comment, verified). Unit 28 changed two
  declarations. The separate `.hero .hero-shade` used by artist/artwork heroes and the
  `.home-hero` rebuild from unit 26a are both untouched.
- **Contrast did not regress anywhere.** Every unit-27/28 change moves ink *up* a rung or adds
  opacity. F-7 is a pre-existing condition newly measured, not a new defect: no element measures
  worse at HEAD than it did at `4fc8239`.
- **F-1 and F-2 re-checked in the tree** (R2.2.7); neither moved.

No regression found.

## R2.7 — PRESSURE

None was applied. I record that this revision was the harder call of the two, and how I made it.

Revision 1 blocked on three criteria with no evidence — that is nearly mechanical. This time two
of the three came back genuinely answered, with work of high quality: unit 27's bound reproduces
under my own arithmetic, unit 28 found a defect *against its own unit's success story* and
declined to paper over it, and every author in this chain corrected their own instrument in
public (Vermeer's `visibility:hidden` false positive, Dürer's orphaned-chain provenance failure,
his `background-clip:text` self-scoring). I retracted one of my own findings as a false negative
for the same reason. Twenty-eight units of that culture make it tempting to call the last item
residual risk and be done.

I was explicitly told that ruling the canvas class a properly recorded pre-existing note would
be legitimate and not a lowered bar. I considered it seriously, and I decline it — on a textual
distinction rather than a temperamental one. AC18 froze the viewports that let me note the
821–1100 px overflow; AC19 freezes no pair inventory and names browser-measured composites
directly. The global link colour, in a shipped theme, over a layer behind every route, below
floor on a single blob. The implementer says AC19 is not supported. I will not certify over that.

Equally, I have not inflated it. F-7 is **one** finding, token-level, with a costed and
reversible remedy that already exists in the palette. Twenty-eight of twenty-nine criteria pass,
two of them newly, and I closed two of my own three blocking findings — one by verifying someone
else's fix from first principles, one by admitting my probe was wrong.

**What blocks is narrow and specific:** F-7 needs a token decision from Matisse and one
re-measurement pass in both themes at both viewports, verified by someone who did not implement
it. Plus the evidence hygiene in N-1 and N-4, neither of which is a criterion.

---

# ARCHIVE — REVISION 1 (2026-07-26) — SUPERSEDED BY REVISION 2

*Preserved verbatim. Its verdict is superseded; its findings and adjudications A1–A6 remain the
record of what was blocked and why. Where Revision 2 changes a status, the ledger in R2.5 says
so explicitly. Section numbering below is Revision 1's own.*

**Reviewer:** Van Eyck (`claude-quality-reviewer`), Quality and Accessibility Reviewer
**Date:** 2026-07-26
**Branch:** `pig-001-stabilization` (verified: **not** `main`; no push, no merge)
**Product tree reviewed at:** `4fc8239` (unit 26 log). Re-confirmed unchanged at `5fdf1aa`,
which touches only `pigment_coordinator/` and `tests/` — no production file.
**Standard:** the 29 acceptance criteria of `protocol/tasks/PIG-001/specification.md`,
frozen at `approved_for_build`. Nothing else. A criterion passes or fails; there is no
partial credit, and an untested criterion is not a passing criterion.

**Independence:** I wrote none of this code and reviewed none of it before now. I did not
fix anything I found. Everything below is either a command I ran, a file I read, or a
measurement I took in a browser myself — except where I explicitly name someone else's
artifact as the source.

---

## 1. SCOPE REVIEWED

- The frozen specification and its 29 criteria; `owner-decisions-r2.md` (OD-1…OD-5);
  `unrouted/decision-record.md` (D-001…D-016).
- Build records: `build-log-wave-{a,b,c,d}.md`, `build-log-unit-{23,24,25,26}.md`.
- Browser evidence: `browser-evidence-build.md` (round 1) and
  `browser-evidence-build-r2.md` (round 2, authoritative), plus the ~80 screenshots.
- `visual-direction-and-adjudication.md` (Matisse: AC23 + contrast direction).
- Rights and history: `rights-register.{md,json}`, `rights-remediation.md`,
  `historical-sample.md`, `museum-photo-rights.json`, `artwork-image-rights.json`,
  `asset-inventory-effa805.md`, `deck-merit-review.md`.
- Contrast harness: `contrast-audit.py`, `contrast-pairs-measured.csv`.
- Source: `css/styles.css`, `index.html`, `js/app.js` (read directly, not via the logs).
- The running product, served locally and driven in a real browser at 390, 673, 900 and
  1440 CSS px, both themes.

---

## 2. CHECKS I RAN MYSELF, WITH OUTPUT

### 2.1 Validator — `osascript -l JavaScript tools/validate.jxa.js`

```
app.js: syntax OK
artists: 256, movements: 76, techniques: 39, eras: 8, nations: 37, painter styles: 27,
influence edges: 238, venues: 116, catalog: 323 (tier1: 76), daily pool: 75,
museum notes: 104, photo credits: 104 (attribution required: 88),
artwork image credits: 27, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```

Zero errors, **zero warnings**, all references valid. This is the unedited snapshot AC2
requires. It matches unit 26's log exactly.

Counts differ from the specification's frozen assumption (247/75/317/225/115/103) because
Sol's independent content commit `ef8b2b3` landed mid-build. That is recorded as D-016 and
is not a defect; see the regression sweep (§5).

### 2.2 Contrast audit — `python3 evidence/contrast-audit.py`

Run in full. **Its output must be read with care and I did not take it at face value.**

- **Pass 1 parses `css/styles.css` live** → current. All body-text tokens clear AA on the
  three real surfaces in both themes. The `--bg2` rows it prints as FAIL are **vacuous**: I
  verified independently that `--bg2` is declared (`styles.css:146,180`) and referenced
  **nowhere** — `grep -rn "var(--bg2)" css/ js/ index.html` returns no hits. Matisse's
  correction is confirmed.
- **Pass 2 reads `contrast-pairs-measured.csv`** — regenerated by Vermeer in round 2, i.e.
  **at `a018fe2`, before unit 26**. It still prints 5 failures including the three
  `#9e7938` gold-as-small-text rows that **unit 26c fixed**. Stale by construction.
- **Pass 3 has browser-sampled pixels baked in from before unit 26.** It still prints the
  dark hero at 1.10:1 FAIL — a state that **unit 26a fixed**. Stale by construction.

Both build logs (unit 25 §"Honest limits", unit 26) warn about exactly this. **Treating the
script's summary line as the current state of the build would be wrong**, and I do not.
I re-derived the affected numbers myself instead (§2.4, §2.5).

### 2.3 Source spot-checks — the implementers' claims, verified in the code

Every one of these I checked in the file, not in the log:

| Claim | Verified | Where |
| --- | --- | --- |
| `--hero-veil` tokens exist, .80 dark / .86 light | **yes** | `styles.css:169,207` |
| One shared `.home-hero .hero-shade` geometry, both themes | **yes** | `styles.css:768-774` |
| 25d's light-only `.hero-shade` override deleted | **yes** | only one `.home-hero` rule remains |
| Cover credit unscoped to `--body-ink` | **yes** | `styles.css:777` |
| Nav rule: `flex:0 0 100%; width:100%; flex-wrap:nowrap` in the ≤820 block | **yes** | `styles.css:1154` |
| Desktop wrap retained above 820 px | **yes** | `styles.css:300` |
| All six gold→gold2 re-pointings landed | **yes** | `:984, :1016, :1031, :1178, :1189, :1277` |
| `#route-status` gone; zero live regions in source | **yes** | only historical comments at `app.js:2314,2317` |
| `--gold` invariant written down at the token | **yes** | `styles.css:187-191` |

**I ran my own independent gold-as-text sweep** rather than trusting the audit's counts.
The only remaining `color:var(--gold)` glyph-painting uses are
`.mu-essay p:first-child::first-letter` (a ≈55 px drop cap — large text, floor 3.0) and the
hero `h1` gradient stops (59.2 px — large text). Both are correctly classified. **No seventh
small-text site exists.** The sweep is accurate.

### 2.4 Hero contrast — re-derived by me, both themes, against a forced worst-case cover

I did not repeat Dürer's glyph-pixel diff. I computed the bound from the live cascade in
the running page: backdrop = `worstCoverPixel·(1−veil) + page·veil`, worst cover = opaque
white in dark, opaque black in light — the rule Matisse set.

| theme | element | floor | **my measured bound** | verdict |
| --- | --- | --- | --- | --- |
| dark | `h1` worst gradient stop `rgb(201,164,92)` | 3.0 | **4.65** | PASS |
| dark | `.kicker` | 4.5 | **6.84** | PASS |
| dark | `.lede` | 4.5 | **7.25** | PASS |
| dark | `.footer-note` (cover credit) | 4.5 | **7.25** | PASS |
| light | `h1` worst stop `rgb(129,99,43)` | 3.0 | **3.46** | PASS |
| light | `.kicker` | 4.5 | **9.27** | PASS |
| light | `.lede` / `.footer-note` / credit link | 4.5 | **6.73** | PASS |

These agree with Dürer's forced-cover run (4.62 / 6.80 / 7.20 dark; 3.42 light) to within
rounding, and with the bound recorded in the `styles.css` block comment. **V2-1 and V2-2 are
genuinely closed.** I confirmed the shade element is `radial-gradient(100% 100%, rgba(13,12,10,0.8) 0%,
… 62%, rgba(13,12,10,0.3) 100%)` — one geometry, per-theme alpha.

### 2.5 Responsive — measured by me in a real browser

| width | root `sw / cw` | overflow | header | nav box | wrap / basis |
| --- | --- | --- | --- | --- | --- |
| **390** | 390 / 390 | **0** | 164 px | 358 × 45, **1 row** | `nowrap` / `100%` |
| **900** | **1008 / 890** | **+118 px** | — | — | — |
| **1440** | 1430 / 1430 | **0** | 110 px | 799 × 81 | `wrap` / `0%` |

At 390 the unit-26b fix is confirmed live: `flex-basis:100%`, `flex-wrap:nowrap`, one
scrolling row, all 8 links tabbable, zero root overflow. (I measure the header at 164 px
where Dürer measured 154 px — an environment difference, immaterial.)

At 900 px I **independently reproduced Dürer's unfixed finding**: `a.daily-media`, 520 px
fixed, right edge 1008, pushing the root 118 px wide on `#/`. See adjudication A1.

### 2.6 Route orientation (AC15) — measured by me at HEAD

Navigated `#/museums → #/timeline → #/palette → #/credits → #/no-such-page` with a
`MutationObserver` on `documentElement` and a capture-phase `focusin` log:

- `document.title` updates on every route: `Museums — Pigment`, `Timeline — Pigment`,
  `Find your palette — Pigment`, `Credits — Pigment`, `Lost — Pigment`. **5/5.**
- **Live regions in the document: 0.** `#route-status`: absent. **Live mutations: 0.**
- `document.activeElement` after each navigation is the route's `h1[tabindex="-1"]`
  carrying the page name ("Museums", "Blank canvas"). Focus moves to a meaningful entry
  point, and page identity is conveyed exactly once.

C-8 is resolved in the build I am certifying, not merely in the one Vermeer measured.

### 2.7 Search (AC21) and Explore (AC22) — measured by me; no browser reviewer covered these

**AC22.** Home's WANDER card promises "one timeline, an influence constellation, family
trees of movements, and a world map of painters". `#/explore` renders exactly four
`.entry-card`s → `#/timeline`, `#/influences`, `#/movements`, `#/nations`. Same four
instruments, all reachable. **Aligned.**

**AC21.** Driven through the real combobox, one query class each:

| class | query | result | verdict |
| --- | --- | --- | --- |
| exact | `Leonardo` | Leonardo da Vinci #1 | PASS |
| prefix | `Leo` | Leonardo #1, then Leonora / Leopold / Tolstoy | PASS, not starved |
| metadata | `oil painting` | Oil Painting (technique) | PASS |
| ambiguous | `david` | *David* (Michelangelo), *David with the Head of Goliath*, David Hockney, Jacques-Louis David | PASS — both senses surfaced |
| no-match | `zzzqqqxyz` | "Nothing…" empty state | PASS |
| multi-entity | `van gogh` | Museum, painter, *Starry Night*, *Sunflowers* | PASS |

`aria-expanded` flips correctly; options carry `role="option"`. Consistent with wave C's
frozen 24-query fixture (24/24), which I read in full and accept as the criterion's
instrument.

### 2.8 Storage failure (AC8) — partially settled, see F-4

Under a `Storage.prototype.setItem` that throws `QuotaExceededError`, I clicked Admire on
`#/daily`: the button stayed **"Admire"** with **`aria-pressed="false"`**. **The interface
does not claim a success that did not happen** — the most important half of AC8 holds, and
I verified the state machine exists in source (`getPassport` sets `ppState.read="denied"`
on a throwing read and distinguishes `corrupt` from "no passport yet", `app.js:76-84`).

My corrupt-read probe was inconclusive (no passport existed to corrupt, so the route
correctly showed its empty state), and I observed **no user-visible retry / recovery /
export affordance** in the write-failure case. See F-4.

### 2.9 Space-key activation — resolved in source

Vermeer could not emit a space key from automation. I read the handler instead:
`js/app.js:2556` — `if(e.key === "Enter" || e.key === " " || e.key === "Spacebar")`, on the
`.ig-node` delegate. The graph nodes are `role="button" tabindex="0"` (`app.js:1194`).
**Space is implemented**, on the same code path whose Enter branch Vermeer observed
working. This does not leave AC17 unsupported.

---

## 3. ACCEPTANCE CRITERIA — ALL 29

**PASS 26 · FAIL 0 · UNSUPPORTED 3**

| # | Criterion (abbrev.) | Verdict | Evidence |
| --- | --- | --- | --- |
| AC1 | effa805 baseline named, older labelled historical, deployed-identity proof defined | **PASS** | `final-synthesis.md`; `unrouted/rebaseline-effa805.md`; `?v=` uniformity, wave-a U10 |
| AC2 | Validator: no errors, refs valid, unedited snapshot | **PASS** | **My run, §2.1** — zero errors, zero warnings |
| AC3 | Two deck warnings cleared on merit or owner exception | **PASS** | `deck-merit-review.md` — 2 corrections on merit, 1 refused; warnings cleared as consequence; my validator run confirms 0 warnings |
| AC4 | Frozen first-user journey matrix, no broken/unexplained transition | **UNSUPPORTED** | **No transcript exists.** `build-log-wave-c.md:362` lists "the AC4 journey-matrix transcript" under *"Not claimed, deliberately."* See F-3 |
| AC5 | Import: per-field identify, explicit confirm, cancel/malformed preserves local | **PASS** | Vermeer round 1 (`browser-evidence-build.md:292`), byte-identical cancel 2578→2578; wave-b U15. Carry-forward legitimate (§6, A5) |
| AC6 | Admire/Seen/Saved independent, accurate visible + programmatic state | **PASS** | Round 1 + wave-b `aria-pressed` on C17; my §2.8 confirms `aria-pressed` is live |
| AC7 | Five interruption checkpoints resume exactly | **PASS** | Vermeer round 1, **5/5**; wave-c U18. Carry-forward legitimate (§6, A5) |
| AC8 | Storage failure: no false success, context preserved, retry/recovery/export offered | **UNSUPPORTED** | Half verified by me (§2.8, no false success); recovery-path half never demonstrated by anyone. See F-4 |
| AC9 | Invalid-route/no-match/empty/limit/failure preserve context + next action | **PASS** | My §2.6 (`#/no-such-page` → "Blank canvas", focus moves) and §2.7 (empty state); wave-c truncation affordance "Showing 9 of 51"; `invalid-route__*` shots |
| AC10 | Frozen asset inventory, exact counts by surface + reachability | **PASS** | `asset-inventory-effa805.{md,json}` — 799 assets; regenerable (wave-d U16) |
| AC11 | Item-level rights sample ≥100 incl. Tier1∪daily + all Matisse/Kahlo | **PASS** | `rights-register.json` — **122 entries**, all nine required fields present per entry (verified by me: `id, surface, declared_page, exact_match_verdict, pd_basis, attribution_required, verified_on, status, disposition`) |
| AC12 | Mismatches/unresolved/out-of-sample stay explicitly unresolved | **PASS** | Same file — 8 `mismatch` + 2 `attribution-required` recorded as such; `rights-remediation.md` |
| AC13 | Historical sample: 10 profiles, ≥5 eras/movements/nations, 5 claim classes, 20 edges | **PASS** | `historical-sample.md` — 10 profiles × 5 slots + 20 edges, spread table, one contradicted edge recorded |
| AC14 | Release language checked, no overclaim | **PASS** | wave-d U21 §(d); unit 23/24 corrections; the AC25 self-correction (D-W-2) is itself the criterion working |
| AC15 | Title updates, one identity to AT, focus to entry point, no repeat announcements | **PASS** | **My §2.6** — 5/5 titles, 0 live regions, 0 live mutations, focus on `h1[tabindex=-1]`. Real screen-reader output NOT TESTED; recorded as a limitation (§6, A6) |
| AC16 | Selected/current/expanded/pressed/active: visible + programmatic, not colour/position/hover alone | **PASS** | wave-a U1/U4 (weight + 2 px underline, not colour alone); wave-b C1–C18 programmatic pass; combobox verified by me §2.7 |
| AC17 | Keyboard-operable with visible focus; bypass; no nested interactive | **PASS** | Round 1 skip link + graph bypass (204 stops) + Enter + focus ring; **Space verified in source by me** §2.9; all 8 nav links tabbable §2.5. Degraded-focus finding F-2 recorded as minor |
| AC18 | 320/390/768/1280/1440 + 200 % zoom: destinations reachable, no root overflow | **PASS** as frozen | 200 % zoom **0/26 routes** (Vermeer r2, re-confirmed unit 26 at 1270 and 1280); 100 % sw==cw at 320/390/768/820/1280/1440 (unit 26 sweep; **390 and 1440 re-measured by me**). 821–1100 band is outside the frozen set → adjudication A1, finding F-1 |
| AC19 | Both themes pass AA for frozen text/control/focus/state pairs **incl. composites needing browser measurement** | **UNSUPPORTED** | Tokens PASS (pass 1, live); hero **both themes** PASS (**my bound, §2.4**); six gold re-pointings PASS (**my source sweep, §2.3**); timeline ink PASS 4.61 (Vermeer r2). **But text over Wikimedia photographs — a named composite class — was never measured by anyone, and my own worst-case bound fails it.** See F-5 |
| AC20 | Reduced motion preserves info/choices; canvas + relationship viz have alternative + accessible name | **PASS** | Round 1: animations removed, 621→0 transitions, nothing lost; wave-b: 19 `canvasTag` call sites named, `#ig-svg` `role="group"`+label. Carry-forward legitimate (§6, A5) |
| AC21 | Frozen fixture, six classes, no starvation, count/selection/dismissal/focus-return | **PASS** | wave-c frozen 24-query fixture **24/24**, starvation and truncation measured; **six classes re-verified by me in a real browser** §2.7 |
| AC22 | Home Explore promise = Explore destination; every instrument reachable | **PASS** | **My §2.7** — same four instruments, four reachable routes |
| AC23 | Named adjudicator reviews hierarchy/relationship/entrances/identity without claiming comprehension | **PASS** | `visual-direction-and-adjudication.md` §REVIEW — Matisse (named in the spec) reviewed all four named subjects, recorded observations + tradeoffs, explicitly refused comprehension claims. Adjudication A4 |
| AC24 | ≥1 relationship journey: named entities, relationship + consequence, anchor, onward path | **PASS** | `#/influences` — 238 typed edges, legend with counts, named chains (Theophanes→Rublev, Warhol↔Kusama); "Rublev's teacher" as consequence in a list cell; keyboard-traversable (wave-b U12). Matisse item 2 |
| AC25 | Every third-party runtime request identified; undisclosed fails | **PASS** (disclosure) | Fonts self-hosted per OD-3; **0** requests to `fonts.googleapis.com`/`fonts.gstatic.com` (Vermeer r2 §G); `upload.wikimedia.org` disclosed on `#/privacy` (unit 23). Deployment-gated condition open — see F-6 |
| AC26 | Criterion-to-unit matrix, defect/deferred register, rollback, cache/versioning | **PASS** | `feasibility-assessment-r2.md` R1/R2; spec's known-defect + deferred-promise register; rollback amended by D-016 to revert **by commit** |
| AC27 | Fresh IL assessment confirms buildability, doesn't lean on the 14-unit plan | **PASS** | `feasibility-assessment-r2.md` — FEASIBILITY CONFIRMED, 29/29 classified, 0 infeasible |
| AC28 | No legal conclusion from death year/host/attribution alone | **PASS** | `rights-register.md:55,520` explicitly refuses the death-year inference; `legal_conclusion` field per entry; OD-5 |
| AC29 | No production edit before `approved_for_build`; merge/deploy need explicit approval | **PASS** | Spec at `approved_for_build` precedes all units; branch verified `pig-001-stabilization`; no merge, no push, no deploy. D-016 records the Gate-4 partial breach honestly |

---

## 4. FINDINGS BY SEVERITY

### CRITICAL — 0

### MAJOR — 2

#### F-5 (major) · AC19 · Text over Wikimedia photographs was never measured, and the bound fails

**AC19 names this class explicitly:** "including composites that require browser
measurement." Text over `upload.wikimedia.org` photographs is exactly such a composite. It
is Vermeer's NOT TESTED #4 (cross-origin taint makes `getImageData()` throw) and unit 26
states plainly: *"Not claimed: text over `upload.wikimedia.org` artwork photographs is still
unmeasured."* **No one has measured it.**

I computed the bound myself instead, using the project's own adopted rule (worst-case
opaque pixel, not a sampled one). On `#/museum/louvre`, dark theme, 6 photographic tiles
behind `.mu-hero`, scrim `linear-gradient(rgba(13,12,10,.18), rgba(13,12,10,.94) 80%)`:

| element | size | scrim alpha at its band | vs worst **dark** photo px | vs worst **bright** photo px | floor | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `.mu-hero-body h1` | 32 px | .564 | 16.22 | **3.65** | 3.0 | pass, thin |
| **`.mu-sub`** | **15.2 px** | **.700** | 6.54 | **2.44** | **4.5** | **FAIL** |
| `.mu-hook` | 18.9 px | .845 | 12.39 | 8.06 | 4.5 | pass |

`.mu-sub` ("Paris · France · founded 1793") sits where the scrim is only 70 % opaque. Over a
bright region of a building photograph it reaches **2.44:1 against a 4.5 floor**. There are
**116 venues**, each with its own photograph; architectural photography routinely has bright
sky or wall at that height. On the Louvre draw I screenshotted the text is legible, so I am
**not** claiming an observed failure — I am reporting that a criterion-named composite class
is **unmeasured across 116 surfaces and its worst case fails**.

**Reproduction:** serve the repo, open `#/museum/louvre`, read the computed colour of
`.mu-sub` and the `.mu-shade` alpha at its vertical band, composite against an opaque white
pixel. Script in §2 of this review.

**Why this is unsupported rather than passing:** every other AC19 sub-claim was driven to a
worst-case bound (hero) or a 156-sample measurement (timeline). This class alone rests on
nothing. Matisse's own standard governs: *"Anything that passes only against the cover
Vermeer happened to sample is not a fix. The mechanism must hold for any cover."* The same
must hold for any photograph.

**Remedy (not applied by me):** either raise the `.mu-shade` alpha where `.mu-sub` paints,
or measure the class across the venue set with the screenshot-diff technique already built
in `harness/durer-u26/hero.py` — unit 26 notes that harness would reach it.

#### F-3 (major) · AC4 · The journey-matrix transcript does not exist

The specification's evidence package requires *"the frozen journey matrix transcript
(AC4)"*. `build-log-wave-c.md:362` lists it under **"Not claimed, deliberately."** I searched
`evidence/` and the task tree; there is no such artifact.

AC4 requires one matrix demonstrating a chain: *entry, onboarding, Passport creation, an
Admire action, consequence explanation, persistence, return, export or share, import,
conflict handling, and reset* — with no broken or unexplained transition. Several links are
individually evidenced (AC5 import/cancel, AC6 states, AC7 checkpoints, all from round 1),
but **consequence explanation, export/share, and reset are nowhere exercised end to end**,
and the point of a matrix criterion is the joined chain, not the parts.

**Reproduction:** `grep -rn "AC4" protocol/tasks/PIG-001/evidence/` returns only feasibility
and self-assessment references — no transcript.

**Remedy:** run the eleven-step journey once, in a browser, and transcribe it. This is
evidence work, not code work; on the current build I expect it to pass.

### MINOR — 3

#### F-1 (minor) · Pre-existing horizontal overflow at 821–1100 px on `#/`

Reproduced independently at 900 px: root `scrollWidth` **1008** vs `clientWidth` **890** =
**+118 px**, first overflowing element `a.daily-media` (520 px fixed, right edge 1008).
`#/artists` is clean at the same width, so this is the "Painting of the Day" media block.
`git diff a4898d3..HEAD -- css/styles.css` does not touch `.daily-media`; it predates unit 26
and predates PIG-001.

Outside AC18's frozen viewport set (320/390/768/1280/1440) — see adjudication **A1**. Minor
rather than major because it is pre-existing, outside every frozen criterion, and a
narrowing of the "overflow" entry already on the specification's known-defect register.
Note the band includes 1024 px (tablet landscape), so it is worth scheduling.

**Reproduction:** serve, open `#/` at 900 px, read `document.documentElement.scrollWidth`.

#### F-2 (minor) · AC17 · The last nav destination's focus indicator is faded by the mask, at ≤820 px

`.main-nav` below 820 px is `overflow-x:auto` behind
`-webkit-mask-image:linear-gradient(90deg,#000 78%,transparent)` (`styles.css:1156`). The
mask fades the right 22 % of the **box**, not of the content — so **whatever link is at the
right edge is faded, including when the user has scrolled as far as it goes.**

Measured by me at the frozen 390 px width, nav scrolled fully to the end (`scrollLeft` 332
of 331 max): "Nations" is the active element, its centre sits at **89 %** of the box, where
mask alpha is **≈0.52**, falling toward 0 at its right edge. So the eighth destination — and
its focus ring — never renders at full opacity at 390 px. At 673 px I measured the same link
at alpha **≈0.16**.

This is restored pre-25 behaviour (unit 25e's accidental `wrap` had hidden it; 26b correctly
restored the scrolling row), not a new regression, and AC18's "or has an evident
keyboard-operable navigation affordance" clause is satisfied — the nav scrolls and every
link is tabbable. But *visible focus* on that link is degraded below what 2.4.7 / 1.4.11
contemplate. Minor, not blocking: focus is degraded, not absent; the control predates the
build; and "mobile-nav discoverability" is already on the known-defect register.

**Reproduction:** 390 px, `nav.scrollLeft = nav.scrollWidth`, focus the last link, compare
its centre offset against the 78 % mask stop.
**Suggested remedy (one line, not applied):** drop the mask when the container is scrolled
to its end, or apply it to the scrolling content rather than the viewport box.

#### F-4 (minor) · AC8 · No user-visible recovery affordance observed on write failure

With `setItem` throwing `QuotaExceededError`, Admire correctly refused to flip
(`aria-pressed="false"`, label unchanged) — no false success. But no message, retry, or
export path appeared. AC8 asks the interface to preserve context *"while offering a
meaningful retry, recovery, or export path."* The state machine exists in source
(`app.js:76-84` distinguishes `denied` / `corrupt` / genuinely-absent), so this may be a
gap in my probe rather than in the build — my corrupt-read test was inconclusive because no
passport existed to corrupt. Recorded as the reason AC8 is unsupported rather than passing.

### NOTE — 3

#### N-1 · The screenshot evidence pack depicts a superseded build

All ~80 screenshots were committed at **`a4898d3`**, before the four unit-26 commits. I
confirmed this by eye, not by timestamp alone:

- `home__desktop-1440x900__dark.png` shows the hero title crossing **saturated, unveiled**
  yellow/blue/red cover shapes — the V2-1 failure state at 1.10:1. The current build (my
  screenshot at 1440, dark) shows a heavily veiled cover with the title clearly separated.
- `home__mobile-390x844__dark.png` shows the nav as **eight stacked rows** filling the top
  of the viewport — the V2-4 failure state, 362 px header. The current build shows one
  horizontally scrolling row.

So **all 32 mobile shots and the dark-theme home shots no longer depict the build under
review**, on exactly the two surfaces unit 26 changed. I did not treat this as a blocker,
because I re-measured both surfaces myself in a live browser (§2.4, §2.5) and they pass — my
own observation replaces the stale artifact rather than depending on it. But the evidence
pack should be re-captured at HEAD before the Human Review Package goes out, or a reader
will conclude the opposite of the truth from the pictures.

Related and worth stating: **unit 26 has had no independent browser verification at all.**
Dürer measured his own work. That is exactly the arrangement that produced round 1's
undetected 500-px capture defect. My §2.4–2.7 measurements are the only third-party
observation of unit 26 that exists, and they are narrower than a Vermeer pass.

#### N-2 · Matisse adjudicated on round-1 evidence and never saw the corrected shots

AC23's record cites the 390 px captures he himself declared defective, and his item 5(a)
rests on light `.footer-note` at 2.37:1 — a value unit 25 fixed. He asked for a re-capture
"before Gate 2"; it happened, but the sound shots were never put back in front of him. His
four *named* subjects were all adjudicated on desktop evidence that was sound, so AC23
stands (A4), but the mobile-composition half of his record is stale.

#### N-3 · Corpus counts differ from the frozen specification assumption

The spec assumed 247 artists / 75 movements / 317 catalog / 225 edges; HEAD reports
256 / 76 / 323 / 238. Cause is D-016 (Sol's `ef8b2b3` landing mid-build), recorded and
accepted. AC2 asks for a valid unedited snapshot, which this is. Flagged only so the
Human Review Package does not present the spec's assumption line as current.

---

## 5. REGRESSION SWEEP

- **Validator at HEAD:** clean, zero warnings, all references valid (§2.1). The corpus that
  moved under D-016 validates.
- **26 routes:** Vermeer r2 §G and unit 26's own sweep both report 0 console errors,
  0 warnings, 0 HTTP ≥400, 0 broken images (680 and 690 images checked respectively),
  26/26 routes reached. I did not repeat the full sweep; I visited `#/`, `#/artists`,
  `#/explore`, `#/museums`, `#/museum/louvre`, `#/timeline`, `#/palette`, `#/credits`,
  `#/daily`, `#/taste`, `#/artist/*` and `#/no-such-page` across both themes and 390/900/1440
  and saw no error, no broken layout and no missing content.
- **Both themes:** exercised throughout §2.4–2.7. Theme toggle flips `data-theme` and the
  token cascade resolves correctly in both directions.
- **Changed surfaces did not break neighbours:** unit 26b's nav change is scoped inside
  `@media (max-width:820px)`; I confirmed the desktop wrap that AC18 needs at 200 % zoom is
  untouched (`styles.css:300`, and 1440 measures `wrap`/`flex-basis:0%` with 0 overflow).
  Unit 26a's `.hero-shade` rebuild is confined to `.home-hero`; the separate `.hero .hero-shade`
  rule (`styles.css:492`) used by artist/artwork heroes is unchanged.
- **Concurrent teammate content (D-016):** Sol's nine Abstract Expressionists, the
  Washington Color School and Noland's *Beginning* validate, render, and were absorbed by the
  photo-credit pipeline with no code change. `#/artists` reports "All 256 painters". No
  conflict with PIG-001's surfaces. The Sistine PD swap (`d7675dd`) is complete in both
  `js/catalog-1.js` and `js/artworks.js`.
- **Third-party runtime hosts:** `upload.wikimedia.org` only; zero Google Fonts (Vermeer r2
  §G, post-token-work). Consistent with OD-3.

No regression found.

---

## 6. THE SIX ADJUDICATIONS

### A1 — The 821–1100 px overflow: **AC18 PASSES as frozen; recorded as F-1 (minor), outside scope**

AC18 enumerates its own test conditions: *"At 320, 390, 768, 1280, and 1440 CSS pixels and at
200 percent text zoom…"* The specification's Frozen Inventories repeat the same five widths.
A frozen criterion is tested at the conditions it names; widening the test set at
certification time would be me rewriting the standard I was given, which is precisely what
"frozen" forbids.

At every named condition the build passes, and I re-measured two of them myself: 390 → 0,
1440 → 0, 200 % zoom → 0 on 26/26 routes. **AC18 passes.**

The 821–1100 px overflow is nonetheless real, reproducible (I reproduced it at +118 px), and
user-facing at common laptop and tablet-landscape widths. It is *pre-existing* — it predates
unit 26 and predates PIG-001 — and "overflow" already sits on the specification's own
known-defect register, which this build narrowed rather than introduced. So it is a **note
against scope, not a criterion failure**, recorded as F-1 with reproduction, and it should be
scheduled. Dürer was right not to fix it as a fifth unreviewed layout change inside a
stabilization task, and right to flag it.

### A2 — Deviation D-1 (dark hero veiled): **correctly taken; accepted; does not block**

Matisse's "dark is untouched and stays at 6.20" rested on arithmetic against `#bg-canvas` at
opacity .6. That layer is **not behind the hero title**. Vermeer found this, Dürer reproduced
it in the DOM, and **I verified it independently**: the veil is on `.home-hero .hero-shade`,
which sits over an in-hero cover canvas at opacity 1, and the pre-fix dark title measured
1.08–1.10:1 against a 3.0 floor. The direction's premise was factually wrong; a direction
premised on a mis-measured layer cannot bind a measured accessibility failure.

Matisse's own document settles the conflict in advance: *"Accessibility-driven constraints
override styling preference (my role definition, §Disagreement). AA is the frozen bar."*
AC19 is frozen; the visual preference is not. Dürer also took the **conservative** branch —
veiling (one token) rather than re-tinting the shipped dark gradient on his own authority —
and escalated rather than deciding silently, which is Gate 3 working as designed.

I verified the result myself: worst dark title stop **4.65** against a forced opaque-white
cover, all dark small text ≥ 6.84. **D-1 is accepted.** Matisse's re-adjudication of the veil
*value* is a worthwhile follow-up (it is one token, re-tunable in one line) but is **not** a
Gate 2 condition — the criterion is met at the shipped value.

### A3 — Deviation D-3 (154 px mobile header, not ~109 px): **accepted as built**

The 109 px "baseline" was never a good state: it was produced by the nav being crushed into
the 97 px left beside the search field, showing **1 of 8 destinations** — which is the
proximate cause of "mobile-nav discoverability", already on the known-defect register.
Restoring `flex-basis` gives the nav the full-width row that the rule's own `width:100%` was
written to produce, showing 4 of 8 with a scroll affordance.

No acceptance criterion caps header height. AC18 asks that destinations be "visible **or**
[have] an evident keyboard-operable navigation affordance" — 4 of 8 in a scrolling row with a
fade affordance satisfies that strictly better than 1 of 8. I measure 164 px at 390×844,
about 19 % of the viewport, for a sticky header carrying wordmark, search, theme toggle and
eight destinations. That is proportionate.

**D-3 accepted**, properly recorded, one-line reversible, both states measured. The related
mask-fade defect is separately recorded as F-2.

### A4 — AC23 with three CONCERNs: **PASSES**

AC23 requires that *a named adjudicator review* four named subjects *and record observations
and tradeoffs without claiming unmeasured user comprehension or preference.* It does **not**
require the review to come back empty. A criterion that demanded zero concerns would make the
adjudicator's independence worthless.

Matisse was the adjudicator named in the frozen specification. He reviewed all four named
subjects (opening hierarchy, Atlas relationship signal, Daily and Taste entrances, Pigment
identity), recorded observations tied to specific screenshots, stated the tradeoff for each,
and was scrupulous — repeatedly and explicitly — about not asserting what any visitor would
perceive. That is the criterion, fully performed. **AC23 passes.**

The three CONCERNs are the record the criterion asked for, and two of them properly decline
to act: elevating one of three equal doors would pre-empt **OD-2**, which the owner ratified
*with an explicit reservation to revisit*; constraining the light-mode backdrop is
compositional work beyond a stabilization scope. The third (light ribbons out-contrasting
body text) was materially *reduced* by unit 25, since every ink it was measured against has
since been raised. All three belong in the Human Review Package as follow-ups. N-2 records
that his mobile evidence went stale.

### A5 — Vermeer's carry-forward: **legitimate for all five, with one narrowed caveat**

He carried AC7, AC5/AC6, AC20, AC17 and AC16 forward from `1214062` on the reasoning that
unit 25 touched only colour tokens, `.main-nav`'s `flex-wrap`, `.skip-inline`'s base rule, the
light hero scrim and the live region. I tested that reasoning against the two changes most
likely to reach further — 25f (live-region removal) and 26b (the nav rule):

- **AC7, AC5/AC6** — storage, merge and onboarding-state machinery. Neither 25f nor 26b is
  anywhere near it; both are CSS-plus-one-element changes. **Legitimate.** I additionally
  confirmed `aria-pressed` is live on the Admire control (§2.8).
- **AC20** — 25a–c changed token *values*; 26a added a non-animated gradient; 26b changed flex
  properties. None introduces a transition or animation, so the 621→0 result cannot have
  moved in the direction that matters. **Legitimate**, with the transition *count* now stale
  by an unknown small delta that cannot flip the verdict.
- **AC16** — 25f removed a live region, which does not touch combobox semantics. I did not
  rely on the carry-forward here: **I re-verified the combobox at HEAD myself** (§2.7) —
  `role=combobox`, `aria-expanded`, `aria-controls`, `aria-autocomplete=list`, labelled.
  **Legitimate and now independently re-observed.**
- **AC17 — the one place the carry-forward genuinely reaches.** 26b restored
  `flex-wrap:nowrap` + `overflow-x:auto` under a right-edge mask below 820 px. Round 1's
  AC17 evidence was taken before that rule existed in its current form and did not exercise
  focus visibility inside a masked scroll container. I therefore **did not carry this half
  forward** — I measured it, and found F-2. The rest of AC17 (skip link, 204-stop bypass,
  Enter, focus ring) is untouched by 25f/26b and carries forward legitimately; Space I
  resolved in source (§2.9).

So: the carry-forward is **legitimate as reasoned**, and the one gap it left is now closed by
measurement rather than by inference. Vermeer stating his reasoning explicitly is what made
it auditable — the right practice.

### A6 — Which NOT TESTED items leave a criterion unsupported

| NOT TESTED item | Leaves a criterion unsupported? | Why |
| --- | --- | --- |
| Real screen-reader output | **No** — AC15 **passes**, limitation recorded | The failure mode AC15 targets (whole-page repeat announcement) is *measured absent*: 0 live regions, 0 live mutations, one identity channel, focus on a labelled `h1`. The accessibility tree is the interface AT reads and it is correct. I will not fail a criterion whose every objective clause I verified because no VoiceOver session was run — but a real AT pass belongs in the follow-up list |
| Space-key activation | **No** | Resolved in source: `app.js:2556` handles `" "` and `"Spacebar"` on the same delegate whose Enter branch was observed working (§2.9) |
| 320 px / 768 px not re-measured in round 2 | **No** | Unit 26's breakpoint sweep measured both at 100 % zoom (320→320/320, 768→768/768), and round 1 measured 130/130 across all five widths. AC18's named conditions are covered |
| **Text over Wikimedia photographs** | **YES — AC19 unsupported** | A composite class AC19 names explicitly, unmeasured by anyone across 116 venue photographs, and my own worst-case bound puts `.mu-sub` at **2.44:1** against a 4.5 floor. **F-5** |
| **AC8 storage-failure UX** | **YES — AC8 unsupported** | No reviewer exercised it; my probe verified the no-false-success half only. **F-4** |
| AC21 24-query fixture | **No** | wave-c's fixture is a real, documented instrument (24/24, starvation and truncation measured), and I re-verified all six query classes in a live browser (§2.7) |
| AC22 Explore alignment | **No** | Measured by me (§2.7) |
| AC24 relationship journey | **No** | Structurally satisfied and evidenced: named entities, typed relationship, consequence copy, preserved anchor, onward path, keyboard-traversable |
| Full 18 ARIA control set not re-observed | **No** | wave-b walked C1–C18 at implementation; the visible half landed in wave-a; spot-checks at HEAD clean. Recorded as a coverage limitation, not a failure |
| **AC4 journey matrix** (never in anyone's brief) | **YES — AC4 unsupported** | The required transcript was never produced. **F-3** |
| Real touch input / device pixel ratio ≠ 1 | **No** | No criterion requires it |

---

## 7. PRESSURE

None was applied to me. I record, as my role requires, that I weighed it deliberately: this
build ran 26 units across four waves and the work is of high quality — the implementers
repeatedly reported defects against themselves (unit 26's own "I do **not** claim AC18 fully
passes while that is open"; wave-d's refusal to assert "zero third-party requests"; Vermeer
retracting his own round-1 findings). That culture is why so few criteria fail. It is not a
reason to certify three criteria that no one has evidence for. **A build that took 26 units
does not thereby earn a certification.**

Equally, I have not manufactured blockers. The 821–1100 px overflow is outside the frozen
viewport set and is a note (A1). The dark-veil deviation is a correct engineering call and is
accepted (A2). The 154 px header is accepted (A3). AC23's concerns are the criterion working,
not failing (A4). Twenty-six of twenty-nine criteria pass, several of them re-measured by me
rather than taken on report.

**What blocks is narrow and specific, and none of it requires re-opening a design decision:**

- **AC19** needs one measurement class run (the harness to do it already exists in
  `harness/durer-u26/hero.py`), and possibly one scrim-alpha adjustment on `.mu-sub`.
- **AC4** needs one journey transcribed in a browser. I expect it to pass on this build.
- **AC8** needs the storage-failure path exercised once with a passport present.

Plus the evidence-package hygiene in N-1: re-capture the screenshots at HEAD, because the
current pack shows a reader the *opposite* of what the build now does on two surfaces.

---

## 8. VERDICT *(Revision 1 — SUPERSEDED by Revision 2; retained as the record)*

Three acceptance criteria cannot be certified as passing because no evidence exists for
them — two of those were never in any reviewer's brief, and one (AC19's photograph
composites) fails the only bound anyone has computed for it. Under my role's rule that Gate 2
may not be certified while any acceptance criterion fails or lacks evidence, and my own rule
that an untested criterion is not a passing criterion:

**PASS 26 · FAIL 0 · UNSUPPORTED 3 (AC4, AC8, AC19)**

Blocking findings, each tied to its criterion:

- **F-5 · AC19** — text over Wikimedia photographs is an unmeasured composite class that
  AC19 names explicitly; my worst-case bound puts `.mu-sub` at 2.44:1 against a 4.5 floor
  across 116 venue photographs.
- **F-3 · AC4** — the required frozen journey-matrix transcript does not exist; it is
  recorded in `build-log-wave-c.md:362` as deliberately not claimed.
- **F-4 · AC8** — the storage-failure recovery path was never exercised by any reviewer;
  I verified only the no-false-success half.

*(Revision 1's verdict line read `GATE 2: BLOCKED`, `OPEN CRITICAL: 0`, `OPEN MAJOR: 2`.
Superseded — see the operative verdict below.)*

---

# OPERATIVE VERDICT — REVISION 2 (2026-07-28, tree `1a41cff`)

Twenty-eight of twenty-nine criteria pass. Two of the three criteria that blocked Revision 1
came back genuinely evidenced and I have closed them — AC4 on a transcript I read in full, AC8
on a source trace that also retracts one of my own findings. The third did not.

AC19's photograph composite is closed and I verified its bound myself. But the deliberate sweep
that unit 28 was asked to run found the same defect in a far wider class: `--faint` small text
in both themes, and the **global link colour `a{}` in the light theme**, fall below the 4.5
floor wherever they paint over `#bg-canvas` — a layer fixed behind every route, under roughly a
third of the site's text. I reproduced this independently from the committed CSS and canvas
source: a *single* blob at its own centre is enough, at 4.34 and 4.33 against 4.5.

These failures pre-date PIG-001 and this build improved contrast rather than degrading it. I
weighed ruling them a scoped-out note, as I ruled the 821–1100 px overflow, and I decline: AC18
enumerates the viewports that put 900 px outside it, whereas AC19 freezes no pair inventory and
its "composites that require browser measurement" clause reaches this class directly. Pre-existence
was not accepted as an excuse for the dark hero, the six gold sites, or the museum band. It cannot
be accepted for the last one — least of all over the implementer's own written *"AC19 is NOT
fully supported."*

**PASS 28 · FAIL 1 · UNSUPPORTED 0**

Blocking finding, tied to its criterion:

- **F-7 · AC19** — `--faint` small text (3.45–4.39 measured; 3.69 dark / 3.22 light bound) and
  the light global link colour `--gold2` (3.49–3.64 measured; 3.22 bound) fail WCAG AA over
  `#bg-canvas`, across 1,346 of 3,755 text elements on 19 routes. Independently reproduced by me
  at 4.34 / 4.33 from a single canvas blob. Remedy is token-level and reversible (retire `--faint`
  over the canvas; re-point light `--gold2` to `#6b5122`), requires Matisse's sign-off as visual
  direction, and must be re-measured in **both** themes at **both** viewports by someone other
  than its implementer. `--muted` (4.47 light / 4.54 dark bound) is in scope, not the destination.

Not blocking, but required before the Human Review Package: **N-1** (re-capture the screenshot
pack once at final HEAD — it is two units stale and shows the pre-veil museum band) and **N-4**
(`browser-evidence-closing.md` ships with four unresolved `<!--PLACEHOLDER-*-->` markers where its
AC19 tables, findings and verdict should be).

Open minor findings, neither blocking: **F-1** (821–1100 px overflow, outside AC18's frozen set),
**F-2** (masked focus ring on the last nav link at ≤820 px).

GATE 2: BLOCKED

OPEN CRITICAL: 0
OPEN MAJOR: 1
