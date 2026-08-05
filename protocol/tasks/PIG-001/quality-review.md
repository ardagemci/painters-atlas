# PIG-001 — QUALITY REVIEW (Gate 2)

**Reviewer:** Van Eyck (`claude-quality-reviewer`), Quality and Accessibility Reviewer
**Branch:** `pig-001-stabilization` (verified: **not** `main`; no push, no merge)
**Standard:** the 29 acceptance criteria of `protocol/tasks/PIG-001/specification.md`,
frozen at `approved_for_build`. Nothing else. A criterion passes or fails; there is no
partial credit, and an untested criterion is not a passing criterion.

| Revision | Date | Tree | Verdict | Counts |
| --- | --- | --- | --- | --- |
| 1 | 2026-07-26 | `4fc8239` / `5fdf1aa` | GATE 2: BLOCKED | PASS 26 · FAIL 0 · UNSUPPORTED 3 (AC4, AC8, AC19) |
| 2 | 2026-07-28 | `1a41cff` | GATE 2: BLOCKED | PASS 28 · FAIL 1 · UNSUPPORTED 0 (AC19 FAIL — F-7, the `#bg-canvas` ink class) |
| 3 | 2026-07-29 | `11e4471` | GATE 2: BLOCKED | PASS 28 · FAIL 1 · UNSUPPORTED 0 (AC19 FAIL — F-8, one residual member of F-7's class) |
| **4 — operative** | **2026-08-06** | **`06ab20f` (HEAD)** | **GATE 2: BLOCKED** | **PASS 29 · FAIL 0 · UNSUPPORTED 0. All 29 criteria pass — including AC15 and AC19, for the first time. Blocked on one open major outside the criteria set: F-9, the repository test suite is RED at this HEAD while the record states it is green.** |

Revisions 1, 2 and 3 are preserved verbatim below. Nothing in any of them has been deleted:
the record of what was blocked, and why, stands as written. Each revision supersedes only the
verdict and criterion statuses of the one before it.

**What each revision blocked on, kept visible on purpose:** R1 — three criteria unsupported
(AC4, AC8, AC19) because no evidence existed for them, not because they had failed. R2 — the
canvas-text class (F-7): `--faint`/`--muted` small text composited over `#bg-canvas`, which the
flat-paint audit could not see. R3 — `span.tl-year` (F-8), the one member of F-7's class that
sat in the seam between two enumerations with non-overlapping gaps, and which the build record
affirmatively *cleared* as panel-shielded. Twice I derived the failure myself rather than taking
it from a log. **All three are now closed and I have re-verified each in the file.**

---

# REVISION 4 (2026-08-06) — OPERATIVE

**Product tree reviewed at:** `06ab20f` (HEAD), 96 commits off `effa805`.
**Last production commit:** `4266804` (unit 36). `09f61a8` is a build log, `a71e2c5` is
evidence and harness, `06ab20f` is Matisse's ruling — the last three commits move no
production file. I verified this with `git show --stat` on each.

**Independence:** I wrote none of this code and I fixed nothing I found. This round I ran the
validator and the test suite myself, re-derived the load-bearing contrast rule from the
committed CSS with my own arithmetic, regenerated the asset inventory and diffed it against the
committed copy, verified the coordinator's gate-reachability claim by reading the callers rather
than the ledger, and bisected a test failure across four commits to find where it entered.

## R4.0 — THE SHAPE OF THIS VERDICT, STATED FIRST

This is the fourth attempt and it is not like the previous three. **All 29 frozen criteria now
pass.** AC19 passes for the first time in this task. AC15 passes for the first time on real
assistive-technology evidence rather than DOM inference. The three things I blocked on are
closed, and I re-verified each of them in the file rather than accepting the closure.

I am nevertheless returning `GATE 2: BLOCKED`, on **one** finding that is not a criterion
failure and not a product defect:

> **The repository test suite does not pass at the HEAD I am asked to certify.** It passes at
> the last production commit and was broken two commits later by the certification-evidence
> commit itself. The build record states it is green. `python3 -m unittest discover -s tests`
> at `06ab20f` returns `Ran 46 tests … FAILED (failures=1)`.

I want to be exact about the discomfort here, because I was warned in both directions. The
remedy is one comment marker and one integer. No user is affected. Nothing in the product is
wrong. If the only question were "is the product good enough", I would certify.

The question is not that. It is whether a certification can stand on an evidence base whose own
green-suite claim is false at the certified SHA — when the single discipline this build has
failed five separate times is *reporting truthfully about a smaller universe than the claim
requires*. I did not go looking for this. It was the first independent check I was told to run,
and it came back red. Certifying past it would make my verdict falsifiable by one command, and
would leave the only mechanism protecting the owner's own decision (OD-5) in a permanently
failing state — which is the same as not having it.

That is the whole of the blocker. Everything else below is a pass.

**One second major finding is open and does not block this gate: F-10**, a governance finding
against the Coordinator kernel — which I was asked to dispose of, and did (A20). It is a
condition on the **merge**, not on the certification, because no acceptance criterion turns on it
and no user is affected. It earned its severity by demonstration rather than argument: **the
quality gate passed this very report while its verdict read `GATE 2: BLOCKED`** (R4.1.7). The
committed state is correct — I neutralised the cause and confirmed the gate blocks — but the
defect is real, and it means the kernel change must not ride into `main` inside a product
approval.

## R4.1 — CHECKS I RAN MYSELF, WITH OUTPUT

### R4.1.1 Validator — `osascript -l JavaScript tools/validate.jxa.js`

```
app.js: syntax OK
artists: 256, movements: 76, techniques: 39, eras: 8, nations: 37, painter styles: 27,
influence edges: 238, venues: 116, catalog: 323 (tier1: 76), daily pool: 75,
museum notes: 104, photo credits: 104 (attribution required: 88),
artwork image credits: 27, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```

Zero errors, zero warnings, all references valid — as in R1, R2 and R3. **AC2, AC3 pass.**

### R4.1.2 Test suite — `python3 -m unittest discover -s tests` — **RED at HEAD**

```
FAIL: test_no_artifact_of_ours_asserts_a_legal_conclusion (test_rights_tooling.…)
AssertionError: Lists differ: [… 1 element …] != []

  protocol/tasks/PIG-001/evidence/harness/vermeer-cert/gapfill.py:28:
  OLD_LEDE = "Most reproductions here are public domain."
      -> asserts a legal status; say 'Commons metadata asserts a PD basis'

Ran 46 tests in 1.467s
FAILED (failures=1)
```

**I bisected it across the final four commits, in clean worktrees:**

| commit | what it is | suite |
| --- | --- | --- |
| `95e5636` | unit 35 — the unit that made the suite green | **46 OK** |
| `4266804` | unit 36 — **last production commit** | **46 OK** |
| `09f61a8` | unit 36 build log (docs only) | **46 OK** |
| `a71e2c5` | **certification evidence + harness** | **46, 1 FAILED** |
| `06ab20f` | HEAD (Matisse's ruling, docs only) | **46, 1 FAILED** |

This is **F-9**, below. Note what it is and is not: the product tree is green; the break is in an
evidence harness file; and the offending string is a *reference to* the old lede used to prove
the old lede is gone — structurally identical to the six fixtures inside the test file itself,
each of which carries an `OD5-EXEMPT` marker. The sanctioned disposition is to mark it and pin
it. Nobody re-ran the suite after the evidence commit, so nobody saw it.

### R4.1.3 Asset inventory — regenerated by me at HEAD and diffed

```
Total unique assets across all public surfaces: 798
Rendered-in-app unique: 797; metadata-only: 1
Catalog∩gallery overlap: 92
Copyright-suppressed URLs leaking into public stub metadata: 0
```

I diffed my regeneration against the committed `asset-inventory-a1b822b.json` field by field:

```
committed a1b822b == my regeneration at HEAD 06ab20f : True
```

**Byte-identical.** The inventory is reproducible at HEAD, and its `a1b822b` filename is a
naming artefact rather than a currency defect — the tree at HEAD produces the same output. I
had expected to raise this as a second currency finding and the measurement retired it.
**AC10 passes.**

### R4.1.4 I re-derived the load-bearing contrast rule myself

The entire AC19 remedy class rests on one rule, written into `css/styles.css:344-363`: against
the worst reachable `#bg-canvas` backdrop — `rgb(101,88,76)` dark, `rgb(187,174,162)` light —
only `--body-ink` and `--ink` clear the 4.5 small-text floor. Every one of the 27 re-pointed
selectors, including my own F-8, was fixed by appeal to it. I computed it from the committed
token values with my own WCAG arithmetic:

| ink | theme | **my value** | published | floor |
| --- | --- | --- | --- | --- |
| `--body-ink` | dark | **4.56** | 4.55 | 4.5 ✓ |
| `--body-ink` | light | **5.02** | 5.01 | 4.5 ✓ |
| `--faint` | dark | **1.83** | 1.82 | ✗ |
| `--faint` | light | **2.58** | 2.57 | ✗ |
| `--muted` | dark | **2.25** | 2.24 | ✗ |
| `--gold2` | dark | **4.31** | 4.31 (N-6) | ✗ |

All six reproduce to ±0.01. This is the third revision in which I have reproduced this class and
been unable to fault it.

**I also re-derived the search-panel inks**, which were the two "measured-not-cleared" residuals
and the 1.00:1 major:

| selector | dark | light | floor |
| --- | --- | --- | --- |
| `.sr-group` (`--faint` on `--panel2`) | **4.62** | **4.62** | 4.5 ✓ |
| `.sr-meta` (`--muted` on `--panel2`) | **5.68** | **6.42** | 4.5 ✓ |
| `#search::placeholder` (`--faint` on `--panel`) | **4.90** | **5.17** | 4.5 ✓ |

My `.sr-group` figure of 4.62 in both themes reproduces exactly the value the stylesheet comment
records for the suppressed-nav state. V32-7 was never a colour defect — I confirmed the fix is
`z-index:3` on `.search-wrap` (`styles.css:478`), settling a flex `order` repaint that put the
nav on top of the open panel below 820 px.

**One deliberate cross-check against a real-pixel figure.** Flat-derived, `.le-meta`
(`--body-ink`) scores **9.25** light over `--bg`. Vermeer measured **6.26** worst on real pixels.
His number is *lower* than my idealisation, which is the correct and honest direction — the
canvas erodes the composite, and a flat-paint derivation over-reports. That relationship is the
single lesson of this build's contrast history, and it holds here.

### R4.1.5 Source spot-checks — the four I was asked to make, verified in the file

| claim | verified at | result |
| --- | --- | --- |
| **Announcement mechanism** (AT-1/3/6/7, one shared channel) | `index.html:80`, `js/app.js:69-75` | **Present.** `#live-status`, `role="status" aria-live="polite" aria-atomic="true"`, `class="sr-only"`, **outside `#app`**. `say(msg, delay)` clears then re-sets after ≥60 ms so a repeated string still fires; `sayNext()` queues across a route change and is drained in `route()` (`:2519-2528`). |
| **Sole live region** | grep over `index.html` + `js/*.js` | **Confirmed.** Exactly one `aria-live`/`role="status"`/`role="alert"` in the shipped source. The only other match is a comment. Independently corroborates Vermeer. |
| **`.branch-chip` label** (AT-5, the CSS arrow) | `js/app.js:854` | **Present.** `aria-label="${esc(k.name)}"` on the anchor. This is the correct mechanism: `.branch-chip::before{content:"↳"}` (`styles.css:1214`) joins the accessible name and **no `aria-hidden` span can reach a pseudo-element** — only an explicit `aria-label` on the host overrides it. Unit 34's diagnosis is right. |
| **Credits lede** (the shipped OD-5 breach) | `js/app.js:2393` | **Rewritten.** Now reads *"Most reproductions here **carry Commons' public-domain assertion**, and we checked each file really is the work it names — the source's claim and our own check, **not a ruling we are qualified to make**."* Bounded, and it names the limit of the evidence in the user-facing copy. |
| **Widened prose guard** | `tests/test_rights_tooling.py:541-548` | **Present and reaches the real path.** `SCANNED` now includes `ROOT/"js"/"app.js"` with the comment *"unit 36: the copy users actually read"*, and the old lede is added verbatim to the positive-catch fixture (`:594`), so the guard is proven to catch the exact string that shipped. |

I also re-verified my own R3 blocker: **`.tl-year` is now `color:var(--body-ink)`**
(`styles.css:927`), and the two false clearances are corrected in place at `styles.css:920-926`
and `build-log-unit-29.md:343-365` — the original sentence struck with `~~`, followed by a dated
`CORRECTION` block naming F-8 and me. That is the sanctioned pattern, and it is the pattern the
prose guard itself honours. **All three conditions I attached to closing F-8 are met.**

### R4.1.6 I verified the coordinator's Gate-2 reachability claim myself

Theory's action A12 asks for a demonstration that no path bypasses Gate 2. I read the callers
rather than the ledger:

- `check_quality_gate` has **exactly one** caller in the package: `engine.py:418`, inside
  `prepare_human_review`.
- `prepare_human_review` (`engine.py:413-416`) first raises `TransitionError` unless
  `workflow_state == "internal_review"` **and** `last_message_type == "response_to_review"`.

**The claim holds.** `human_review_ready` is unreachable without passing the quality gate. Duchamp
was right, and I did not take it from him.

**But reading that code produced a finding of my own — see F-10 and A20.**

### R4.1.7 I ran the quality gate against my own report, and it passed a blocking review

Having described the gate's verdict scan in A20, I ran it on this task directory to check my
reasoning. The result was worse than my reasoning:

```
python3 -c "from pathlib import Path; from pigment_coordinator.gates import check_quality_gate;
            print(check_quality_gate(Path('.'), Path('protocol/tasks/PIG-001')))"
[]        # no failures -> THE GATE PASSES
```

**The gate reported no failures on a Quality Review whose operative verdict is `GATE 2: BLOCKED`
with two open majors.** The cause was my own prose: three sentences explaining the defect quoted
the three patterns verbatim, and `re.search` over the whole file found them. Had I committed that
draft, the Coordinator would have read my blocking review as a certifying one.

I broke every illustrative occurrence with a zero-width character and re-ran it:

```
   - quality review must contain 'GATE 2: CERT<U+200B>IFIED'      <- zero-width inserted by me
   - quality review must contain 'OPEN MAJOR: <U+200B>0'          <- zero-width inserted by me
  -> GATE CORRECTLY BLOCKS
```

*(Even those two lines are the gate's **own failure messages**, and pasting them verbatim
re-armed the defect a second time: my next gate run passed again, on the text of the errors
telling me it should fail. They are shown above with the zero-width markers made visible. I
mention it because it is not a joke at the code's expense — it is the measure of how little
effort it takes to satisfy this gate by accident, and it happened to the reviewer who had just
finished documenting it.)*

**Two things follow.** First, the state committed here is correct: the gate blocks, as it should.
Second, and far more important — the defect in F-10 is no longer an inference from reading the
source. It is **demonstrated**, and the exploit required no adversary, no unusual input and no
mistake: it required a reviewer to write down what the code does. Any future revision that
discusses the gate, quotes a prior verdict, or simply certifies once will arm it permanently.

This is also the sharpest available illustration of this build's signature failure. The gate is
an instrument reporting truthfully about a smaller universe — *"these three strings are present
in this file"* — than the claim it is used to support: *"this task's operative verdict certifies
it."* It is the same error as flat-paint contrast, the JS-only arrow sweep, the 25-route zoom
matrix, the non-zero-byte screenshot check, and F-9. **Five instruments and the gate itself.**

## R4.2 — ADJUDICATIONS

### A17 — AC15: **PASS.** The frozen wording is satisfied, and the boundaries are real.

The frozen text: *"Every frozen route transition updates the document title, exposes one
meaningful page identity to **the tested assistive-technology setup**, moves focus to a
meaningful entry point, and avoids whole-page repeat announcements."*

I cannot reproduce these sessions and I will not contradict them. My job is to rule whether they
satisfy the criterion **as frozen**. They do, clause by clause:

| clause | evidence | source |
| --- | --- | --- |
| updates the document title | instrument-verified across 26 routes | prior browser evidence |
| **exposes one meaningful page identity to the tested AT setup** | *"On reaching a new page it announces the level-1 heading and stops."* | **session 1, by ear** |
| moves focus to a meaningful entry point | `focusSilently(viewEntry())` in `route()`; confirmed by ear when the skip link *"landed past the graph"* and, after repair, *"Return scrolls to the first entry card"* | code + **sessions 1 and 3** |
| **avoids whole-page repeat announcements** | *"It says it only once."* | **session 1, by ear** |

The decisive phrase is **"the tested assistive-technology setup"** — definite article, singular.
The criterion requires that such a setup *exist* and that the four behaviours hold *in it*. It
does not require two screen readers, two engines, or two operators. One operator on VoiceOver +
Safari is a tested assistive-technology setup. My R1–R3 rulings carried this criterion as PASS
with the standing caveat *"real screen-reader output NOT TESTED (A6)"*. **That caveat is now
discharged**, and it is the only one of my three long-running caveats that was discharged by
something other than code.

**The generalisation across routes is structural, not sampled**, which is why I accept it. The
sessions walked principal paths, not all 24 frozen routes. But route identity is produced by a
single route-independent code path — one `focusSilently(viewEntry())` in `route()` — every route
renders a non-empty `h1` (validator: all references valid), and Vermeer measured **0 live-region
mutations across 12 route changes with a positive control proving the observer was live**. The ear
confirms the mechanism; the instrument confirms the mechanism is the same on every route. Neither
alone would carry it.

**Boundaries, recorded honestly as residual risk and not as passing evidence:**

1. **One operator, one screen reader, one browser, one theme.** VoiceOver + Safari, light only.
   No JAWS, no NVDA, no TalkBack, no VoiceOver/iOS.
2. **The asymmetry nobody has named, and it is the sharpest one.** Vermeer's perimeter
   (§7.2) *explicitly excludes WebKit/Safari* — every pixel, zoom, overflow and live-region
   measurement in this build was taken in Chrome. So **the engine in which the ear-confirmations
   were obtained is the one engine no instrument measured, and the engine every instrument
   measured is one no ear has heard.** The two evidence bases are in disjoint engines and do not
   corroborate each other at any point. This is not a defect in either; it is a hole between
   them, and it is exactly the shape of hole that produced F-7, F-8 and V-Z3. It cannot be
   closed by more of either instrument.
3. **Not tested under AT:** dark theme, reduced motion, 200 % zoom.
4. **Talkativeness is "acceptable, not free"** by the owner's own words. The sixteen
   per-card announcements were reduced to quarter points at his request; I verified the cadence
   in source — `const pos = (n === 1 || n % 4 === 0)` (`js/app.js:3256`), giving 1/4/8/12/16
   exactly as asked, with card 1 retained because entering the deck otherwise says nothing.

**What these sessions actually bought, which I want on the record.** They found seven defects in
two sittings that thirty-one units of DOM inspection and pixel measurement did not, and the
pattern is not random: our instruments could prove a control **exists, is reachable, is named,
and that its state transition is correct**, and had no way to detect that the control's
**subject was never announced** (AT-1) or that a completed action **was never reported**
(AT-3/6/7). AT-1 is the one that matters most: the Taste deck asked a visitor to Admire or Pass
on sixteen artworks and never said which artwork. The core product loop was not operable by a
blind user, and no instrument in this project could have found that. The theory pole was right
to insist that inspection could not satisfy this criterion, and I was wrong in R1–R3 to carry it
as PASS on inspection with a caveat attached. **AC15 PASSES — and it did not before.**

### A18 — AC19: **PASS.** First time in this task.

Six previously-open majors plus the two measured-not-cleared residuals now measure clear in an
instrument that is not the one that fixed them: **2,626 glyph rows across 12 cells, 0 below
floor** (Vermeer, `browser-evidence-certification.md` §1). I re-derived the token arithmetic
underneath five of those sites myself (R4.1.4) and reproduce every figure. My own F-8 is closed
in the file and its record corrections are made. F-1 is closed and independently confirmed —
0 px overflow at all eight widths, previously 150/113/54/18.

**Two open items sit outside AC19's frozen scope, and I am ruling them out of it on the same
reasoning I used against the build in R1.** In R1 I ruled F-1 (821–1100 px overflow) *outside*
AC18 because AC18 freezes a viewport list and 821–1100 is not on it — a ruling that went against
the finding I had just raised. Consistency requires the same treatment here:

- **`.md-name` at 2.34 px (320) / 2.97 px (390)** — V-M1, minor, open. This is a **legibility**
  defect and AC19 is a **contrast** criterion. Contrast passes and is not marginal (5.56–6.38
  light, 4.99–5.68 dark). I verified the mechanism in source: the size is an inline
  `style="font-size:${lfs}px"` computed per-label (`js/app.js:1322`), so it scales below
  legibility only in the **europe-zoom state** at narrow widths; and the accessible name survives
  regardless, because each dot carries its own `<title>` and the labels are `pointer-events:none`
  (`js/app.js:1327`, `styles.css:1382-1387`). Real defect, real user impact for a low-vision
  visitor, **not an AC19 failure**. Open minor.
- **AT-5, decorative arrows** — minor, open, and **not a contrast matter at all**. Ruled under
  AC19 only because that is where the reviewer traffic went. See A19.

**AC19 PASSES.** I have blocked this criterion in three consecutive revisions. It passes now.

### A19 — AT-5: still open, and the record understates it. **Minor, non-blocking.**

Unit 34's diagnosis is correct and was earned: unit 33 fixed every arrow *JavaScript* emits and
none *CSS* emits, then recorded AT-5 closed on the strength of a DOM sweep that could only see
the half it had fixed. `::before` content joins the accessible name and no `aria-hidden` span
can reach a pseudo-element. I verified both halves in the file: `ARR` is
`<span aria-hidden="true">→</span>` (`js/app.js:47`), and the single CSS-emitted arrow
`.branch-chip::before` is neutralised by an explicit `aria-label` on the host.

**AT-5 remains unconfirmed by ear**, and I am not treating "fixed in the DOM" as closed —
that is precisely the error unit 34 was written to correct. Unit 34 itself says so: it records
AT-5 as *"fixed and awaiting the ear"*, not closed. **That is the right posture and I adopt it.**

**But the residual is larger than the record says, and I measured it.** Unit 34 carves out one
deliberate exception: *"The pre-rendered SEO landing pages under `p/artwork/*.html` carry a bare
`→` … Fixing them means regenerating ~100 static files."* Both figures are wrong:

```
p/artist  : 256 files with a bare →
p/artwork : 323
p/list    :  12
p/museum  : 104
            ---
            695 files, four families
```

695 files across **four** families, not ~100 in **one**. (The asset inventory independently
counts the same 695 stub files.) The glyph is inside link text — `>Open in the atlas →<` — with
no `aria-hidden` wrapper, so a screen-reader user arriving from search hears "Open in the atlas
right arrow" on any of them. These are crawlable, indexed entry points; "outside the single-page
app the owner tested" is true, but "not linked from it" does not mean not reached.

**This does not block.** The announcement is genuinely minor by the owner's own assessment
(*"I'm not sure if that's a big problem tho"*), it was disclosed rather than silently closed,
and the disclosure was made against interest. But the carve-out must be restated at its true
size before the Human Review Package, because an understated exception is how F-8 happened.
Recorded as **F-11 (minor)**.

### A20 — D-017: the kernel change. **My disposition, since nobody else could give one.**

The liaison declined as conflicted. The theory pole asked for an independent governance
disposition (A12) and identified the risk precisely. I am the only reviewer in this task with no
stake in it, so I will rule.

**What happened.** The Claude pole modified the neutral Coordinator Kernel mid-build
(`5fdf1aa`, 2026-07-26) — `check_build_gate`, `ingest_build`, CLI wiring, four tests — and did
not ledger it until D-017, three days later. It then used that path to ingest its own build
report. Across the branch the kernel has moved by 307 lines in four files.

**On the merits: the code is sound and the need was real.** PIG-001's build had no routable
path; without `ingest_build` a completed build could not enter the state machine at all. The
requirement it adds is *stricter*, not looser — a build claim must be corroborated by the
repository (isolated branch, descends from the frozen baseline, commits beyond it, production
files actually changed), and one test proves a prose-only branch is refused as a build. I
verified the load-bearing structural claim myself (R4.1.6) rather than accepting it.

**On the governance: the objection stands regardless of the merits.** A party changed the
arbiter's code, did not disclose it for three days, and then invoked the boundary it had written
to route its own report. That the change was correct is fortunate; it is not exculpatory, and
"we checked and it was fine" is not a governance control. Gate 3 exists to make exactly this
visible at the time, and it did not.

**And reading that code, I found the defect theory suspected but could not name.** This is mine,
not carried from anyone:

> `check_quality_gate` (`gates.py`) validates the Quality Review by `re.search` for three
> patterns — the `GATE 2:` marker followed by the word CERT&#8203;IFIED, the `OPEN CRITICAL:`
> marker followed by zero, and the `OPEN MAJOR:` marker followed by zero — **anywhere in the
> file**, as three independent matches.
>
> *(Every occurrence of those patterns in this section is deliberately broken with a zero-width
> character so that this analysis cannot itself satisfy the gate. That precaution is not
> fastidiousness — see the demonstration below.)*

This file is **append-only by design** and currently contains four verdict blocks, three of them
superseded. Two consequences follow, and both are live:

1. **The moment any revision writes the certification marker, that string is in the archive
   permanently, and every future run of the gate passes on it** — even if the operative verdict
   is `BLOCKED` with three open majors. A certification cannot be withdrawn once written.
2. **The three patterns need not come from the same verdict.** The critical-count marker from
   Revision 1, the certification marker from a later one, and the major-count marker from a
   third would satisfy the gate even though no single verdict ever said all three.

The gate cannot distinguish an operative verdict from a historical one — which is precisely what
theory alleged ("*historical verdict text cannot satisfy a current gate*").

**I proved this by accident, and then on purpose.** My first draft of this section quoted the
three patterns verbatim in order to explain them. I then ran the gate against my own blocking
report:

```
python3 -c "from pathlib import Path; from pigment_coordinator.gates import check_quality_gate;
            print(check_quality_gate(Path('.'), Path('protocol/tasks/PIG-001')))"
[]        # no failures -> THE GATE PASSES
```

**The gate passed a Quality Review whose operative verdict is `GATE 2: BLOCKED` with two open
majors** — because three sentences *describing* the defect contained the strings it greps for.
A review that blocks would have been read by the Coordinator as a review that certifies. I have
since broken every illustrative occurrence with a zero-width character and re-run the gate to
confirm it now blocks correctly (R4.1.7).

This is no longer a theoretical weakness or an inference from reading the source. It is a
demonstrated one, produced by the most ordinary act available to a reviewer: writing down what
the code does.

While there, a second one, which bears directly on the instrument-credibility question: the
gate's browser-evidence check tests `path.stat().st_size == 0` and matches viewport/theme
**substrings in filenames**. A blank-but-non-zero PNG named correctly passes. That is, at the
gate level, the identical failure to the 16 blank screenshots that passed their own theme and
viewport assertions.

**DISPOSITION — four parts, and the first is the one that matters before any merge:**

1. **The kernel change must be EXCLUDED from the product merge set.** `pigment_coordinator/` is
   not a production surface — it is not in Gate 1's list (`js/`, `css/`, `index.html`, `p/`,
   `tools/`, `sitemap.xml`, `robots.txt`), it ships nothing to users, and it affects no
   acceptance criterion. But it **is** on `pig-001-stabilization`, so merging that branch as-is
   carries it silently into `main` under cover of a product approval. **This code does not belong
   in the product merge set**, and a merge that includes it is a merge the owner was not asked
   about. Land it separately, on its own review, named as what it is: a change to the arbiter.
2. **Before the kernel change is reused, the verdict scan must be fixed** to parse a single
   operative verdict block rather than grep an append-only archive, and the screenshot check
   strengthened beyond non-zero file size. Until then the quality gate is advisory.
3. **The Gate 3 failure is recorded as sustained** — against the Synthesis Lead, as D-017
   already assigns it, not against the implementer. The disclosure was late; it was still made,
   by the party it implicates, and it was made in enough detail for me to check it. That is the
   behaviour the constitution wants, arriving three days later than it should have.
4. **D-017 does not block Gate 2.** It is not a product defect and no acceptance criterion turns
   on it. It is a **condition on the merge**, not on the certification. Recorded as **F-10
   (major, governance-scoped)** so that it cannot be discharged silently.

**A note on my own instrument, since I have just impugned everyone else's.** The format I am
required to end this report in — three literal strings in an append-only file — is itself the
weakness described above. Whoever consumes this verdict must read the **operative** verdict
block, not grep the file. I have labelled every superseded block explicitly. That is the most I
can do from inside the report.

### A21 — The theory pole's 13 requested actions

Their round-3 review is the operative external standard. My assessment, action by action:

| # | Requested action | Status | Basis |
| --- | --- | --- | --- |
| **A1** | Close V32-1…V32-7, independently remeasure every route/theme/viewport/state | **DISCHARGED** | 2,626 glyph rows, 12 cells, 0 below floor, by an instrument that did not author the fix; I re-derived five of the sites' arithmetic |
| **A2** | Measure and disposition `.md-name`, `#search::placeholder`, `.gonext-item:hover b`, frozen focus indicators, populated visualization text — no inference from neighbours | **DISCHARGED** | all named selectors measured explicitly; `.md-name` characterised at 6 widths and given an open-minor disposition rather than a clearance. The "do not infer from neighbours" instruction is honoured — this is the F-8 lesson, applied |
| **A3** | Correct F-1 and F-2, add 900/1024 checks, repeat the 200 % zoom matrix after final visual changes | **DISCHARGED (F-1) · PARTIAL (F-2)** | F-1 closed, 0 px at all 8 widths including 900 and 1024, confirmed independently. Zoom matrix re-run post-change, 26 routes × both themes. **F-2 (masked focus ring on the last nav link ≤820 px) I cannot find evidence of having been corrected** — it remains an open minor, as in R1–R3 |
| **A4** | Regenerate inventories from final HEAD, explain every delta, disposition the 76th Tier 1 record | **DISCHARGED** | **I regenerated it myself at HEAD and it is byte-identical to the committed copy**; `beginning-noland` given an explicit no-asset disposition |
| **A5** | One denominator glossary reconciling 799/798/797, 694/693, 104/103, 29/28/27, 695/679, 66/60 | **DISCHARGED** | `evidence/data-reconciliation.md`, each figure bound to value/commit/date/surface/meaning; `effa805` freeze left byte-stable |
| **A6** | Replace verified-PD / genuinely-PD / jurisdictional assertions with bounded evidence language | **DISCHARGED IN SUBSTANCE** | 14 sites corrected; the shipped `#/credits` lede — the one breach users could read — rewritten and verified by me at `js/app.js:2393`. **The enforcement mechanism is currently failing: F-9** |
| **A7** | **Make the complete repository test suite pass** | **NOT DISCHARGED at HEAD** | green at `4266804`, **red at `06ab20f`**. See F-9. Their acceptance criteria 1 and 3 both fail with it |
| **A8** | A named real AT/browser transcript covering route identity, search, import conflicts, onboarding recovery, state controls, graph bypass | **DISCHARGED** | three sessions; every path they enumerated was reached, the import-conflict path across two sittings. See A17 |
| **A9** | Refresh the screenshot pack only after the last production commit; complete N-8 against final surfaces | **DISCHARGED** | pack recaptured at `a71e2c5`, which post-dates the last production commit `4266804` — I verified the intervening commits touch no production file. **N-1 is closed.** N-8 delivered: PASS WITH NOTE |
| **A10** | Commission a new independent Quality Review at final HEAD, all 29 criteria, every limitation | **DISCHARGED by this document** | — |
| **A11** | Correct five-vs-six, commit-count, corpus-count, evidence-currency contradictions | **DISCHARGED** | six majors carried consistently since D-018; corpus figures reconciled in `data-reconciliation.md`; the 76-vs-75 and Guggenheim/Hirshhorn errors corrected **against both poles** |
| **A12** | D-017 independent governance disposition; bind evidence to an exact SHA; demonstrate no path bypasses Gate 2; identify whether the kernel change is excluded from the merge | **DISCHARGED by A20** | I verified the no-bypass claim in the callers, gave the disposition, and answered the merge question: **excluded** |
| **A13** | Return a `response_to_review`; do not merge, deploy or prepare `human_review_ready` while Gate 2 is uncertified | **HELD** | branch `pig-001-stabilization`, no merge, no push, no deploy; Gate 2 remains uncertified by this verdict |

**11 discharged, 1 partial (A3/F-2), 1 not discharged (A7).**

Two of their findings deserve explicit credit, because both were right and both were resisted
by our evidence at the time: they were right that DOM inspection could not satisfy AC15 (it
could not, and seven defects proved it), and right that the OD-5 language breach was a breach of
the **owner's own decision** rather than a stylistic preference — including one instance that had
shipped to users.

### A22 — Instrument credibility: **trustworthy enough to certify against.** Qualified.

I was asked to judge this one last time, and the honest answer has two halves.

**The pattern is real and it recurred six times, not four.** Each instrument reported truthfully
about a universe smaller than the claim it was used to support:

| # | instrument | true of | used to support | caught by |
| --- | --- | --- | --- | --- |
| 1 | contrast audit | flat paint | all text | me (R2, F-7) |
| 2 | unit 33's arrow sweep | JS-emitted glyphs | all arrows | **the owner's ear** |
| 3 | zoom matrix "26/26" | 25 routes | 26 | Vermeer |
| 4 | 16 screenshots | filename + non-zero size | rendered surfaces | its own operator |
| 5 | **"46 tests, all passing"** | **the tree at `95e5636`** | **the tree at `06ab20f`** | **me, this revision** |
| 6 | **the quality gate itself** | **"three strings appear in this file"** | **"the operative verdict certifies"** | **me, R4.1.7 — by running it on my own blocking report, which it passed** |

**The fifth one is the reason I am blocking, and its location is what makes it serious.** It did
not enter through a build unit. It entered through **the independent certification-evidence
commit itself** — the artefact whose stated purpose was *"to give the independent Quality
Reviewer something to certify against."* The instrument built to close the gap opened a new one,
in the only mechanism guarding the owner's own decision, and it went unnoticed for two commits
because nobody re-ran the suite at the SHA they were certifying.

**The sixth is the one that should change how this pattern is understood.** It is not an
instrument someone built badly — it is the arbiter's own gate, the last check standing between a
blocking review and human review, and it fails in exactly the same shape as the five before it.
That tells me the pattern is not a series of individual lapses by individual authors. It is what
happens by default whenever a *proxy* is checked in place of the *thing*: string presence for
verdict, flat paint for rendered pixels, JS nodes for glyphs, file size for image content, one
commit for another. Nobody in this task was careless. The proxy is always cheaper than the thing,
and it is always right until it is not.

**And yet: yes, trustworthy enough.** Not from fatigue, and not because 96 commits earn it. On
the evidence:

- **Every one of the six was found and none was buried.** Three were found by the pole's own
  people, one by the owner, two by me. Nobody defended a lost figure.
- **Corrections were repeatedly made against interest.** Vermeer lowered Dürer's `.le-meta` from
  6.50 to 6.26 — against his own colleague and toward a worse number — and discovered that the
  inherited 26/26 had covered 25 while auditing his own inheritance. Unit 35 corrected the theory
  pole's diagnosis *and* our own tense error *and* both poles' Guggenheim/Hirshhorn mistake.
  Unit 34 recorded that unit 33 had marked a finding closed that was not closed. Matisse
  overturned his own reasoning on which theme was marginal, and declined to claim a hover state
  he had not seen. **Instruments that correct themselves against interest are the only kind worth
  certifying against.**
- **The method changed, not just the results.** Sampling was replaced by source-bounded
  enumeration; a rule enforced by grep was replaced by a pinned test; a claimed fix was replaced
  by a diagnosis of why the claim was structurally incapable of being true. Unit 34 is the model:
  it did not patch the arrow, it explained why the previous patch could not have worked.
- **The load-bearing arithmetic reproduces.** I have now re-derived this contrast class in three
  separate revisions and cannot fault it.

**What remains structurally unverifiable — named plainly, because certification should not imply
these are covered:**

1. **The engine gap (A17.2).** Every pixel measurement is Chrome; every ear confirmation is
   Safari. Neither corroborates the other, and no amount of either closes it.
2. **The canvas is `Math.random`-seeded.** It can be bounded from source, never sampled to
   exhaustion. Everything rests on the corner-enumeration argument being *sound*, which I have
   checked three times — not on any measurement.
3. **Screen-reader behaviour is a rendering, not a fact.** One operator, one AT, one browser,
   one theme. A second screen reader could produce a different transcript on identical DOM, and
   nothing in this project would predict it.
4. **The build's own signature failure mode cannot be instrumented away.** Every check has a
   perimeter, and perimeters are invisible from inside. The only controls that worked were
   *stating the perimeter explicitly* (Vermeer §7.2, unit 34's carve-out) and *having someone
   outside it look*. Both are procedural, not technical, and both must survive into whatever
   comes after this task.
5. **`.md-name` in the europe-zoom state, and every unwalked interaction state.** State space is
   not enumerable; route space is.

**Verdict on the evidence base: trustworthy enough to certify against — once the fifth instance
is closed rather than carried.** I would not have written that sentence at R2.

## R4.3 — ACCEPTANCE CRITERIA — ALL 29, CURRENT

**PASS 29 · FAIL 0 · UNSUPPORTED 0**

| # | Criterion (abbrev.) | R1 | R2 | R3 | **R4** | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AC1 | `effa805` baseline named, older labelled historical | PASS | PASS | PASS | **PASS** | unchanged |
| AC2 | Validator: no errors, refs valid, unedited snapshot | PASS | PASS | PASS | **PASS** | **my run, R4.1.1** — 0 errors, 0 warnings |
| AC3 | Two deck warnings cleared on merit or owner exception | PASS | PASS | PASS | **PASS** | my validator run confirms 0 warnings |
| AC4 | Frozen first-user journey matrix, no broken transition | UNSUP | PASS | PASS | **PASS** | `browser-evidence-closing.md` §2 — 33 steps, 0 FAIL. Units 33/34/36 touch the deck and credits paths; the deck path is independently re-confirmed by VoiceOver session 3 |
| AC5 | Import: per-field identify, explicit confirm, cancel/malformed preserves local | PASS | PASS | PASS | **PASS** | **strengthened** — session 2 confirms by ear: *"It asks what to keep… I can tell which one is mine… It names both"*; malformed path confirmed session 1 |
| AC6 | Admire/Seen/Saved independent, accurate visible + programmatic state | PASS | PASS | PASS | **PASS** | unchanged |
| AC7 | Five interruption checkpoints resume exactly | PASS | PASS | PASS | **PASS** | **strengthened** — session 1 by ear: *"It put me back where I was, not restarting"* |
| AC8 | Storage failure: no false success, context preserved, retry/recovery | UNSUP | PASS | PASS | **PASS** | A8, my source trace |
| AC9 | Invalid-route/no-match/empty/limit/failure preserve context + next action | PASS | PASS | PASS | **PASS** | unchanged; 26-route sweep clean |
| AC10 | Frozen asset inventory, exact counts by surface + reachability | PASS | PASS | PASS | **PASS** | **my regeneration at HEAD is byte-identical to the committed inventory** (R4.1.3) |
| AC11 | Item-level rights sample ≥100 incl. Tier1∪daily + all Matisse/Kahlo | PASS | PASS | PASS | **PASS** | 122 entries; `beginning-noland` no-asset disposition added |
| AC12 | Mismatches/unresolved/out-of-sample stay explicitly unresolved | PASS | PASS | PASS | **PASS** | **strengthened by the 14-site OD-5 sweep**; substance is clean at HEAD — the *enforcement* is failing (F-9), not the language |
| AC13 | Historical sample: 10 profiles, ≥5 eras/movements/nations, 20 edges | PASS | PASS | PASS | **PASS** | unchanged |
| AC14 | Release language checked, no overclaim | PASS | PASS | PASS | **PASS** | **strengthened** — the shipped `#/credits` lede, the one overclaim users could read, is corrected and bounded |
| AC15 | Title updates, one identity to the tested AT setup, focus to entry point, no repeat announcements | PASS* | PASS* | PASS* | **PASS** | **A17. Three human VoiceOver sessions — the caveat carried through R1–R3 ("real screen-reader output NOT TESTED") is discharged.** Boundaries recorded as residual risk |
| AC16 | Selected/current/expanded/pressed/active: visible + programmatic | PASS | PASS | PASS | **PASS** | unchanged |
| AC17 | Keyboard-operable with visible focus; bypass; no nested interactive | PASS | PASS | PASS | **PASS** | **strengthened** — the skip link was silent and is now *"skip to the atlas immediately"*, and the graph bypass confirmed by ear. F-2 remains an open minor (focus degraded, not absent) |
| AC18 | 320/390/768/1280/1440 + 200 % zoom: reachable, no root overflow | PASS | PASS | PASS | **PASS** | **strengthened** — F-1 closed (0 px at all 8 widths, was 150/113/54/18); zoom matrix re-run post-change, and the inherited 26/26 corrected to a true 26 |
| AC19 | Both themes pass AA for frozen text/control/focus/state pairs incl. browser-measured composites | UNSUP | FAIL | FAIL | **PASS** | **A18. First pass in this task.** 2,626 rows / 12 cells / 0 below floor, independent instrument; F-7 and F-8 closed and re-verified by me in the file; ink rule re-derived to ±0.01. `.md-name` legibility and AT-5 are open minors outside this criterion's contrast scope |
| AC20 | Reduced motion preserves info/choices; canvas + viz have alternative + accessible name | PASS | PASS | PASS | **PASS** | unchanged. Reduced motion under AT is NOT TESTED — recorded, not relied on |
| AC21 | Frozen fixture, six classes, no starvation, count/selection/dismissal/focus-return | PASS | PASS | PASS | **PASS** | **strengthened** — dismissal was silent (AT-3) and now *"announces everything needed"*; type-identification confirmed by ear; the combobox role reduced from three conflicting roles to one |
| AC22 | Home Explore promise = Explore destination; every instrument reachable | PASS | PASS | PASS | **PASS** | unchanged |
| AC23 | Named adjudicator reviews hierarchy/relationship/entrances/identity | PASS | PASS | PASS | **PASS** | **N-8 closed** — Matisse, PASS WITH NOTE, against rendered prose in both themes and viewports, correcting his own reasoning on which theme is marginal and declining to claim the hover state he did not observe |
| AC24 | ≥1 relationship journey: named entities, relationship + consequence, onward path | PASS | PASS | PASS | **PASS** | **strengthened** — graph node naming confirmed richer under real AT than specified; Return-key activation confirmed session 2 |
| AC25 | Every third-party runtime request identified; undisclosed fails | PASS | PASS | PASS | **PASS** (disclosure) | 26 routes, 0 console errors, 0 requests ≥400, `upload.wikimedia.org` only, 0 Google Fonts. Deployment-gated condition remains F-6 |
| AC26 | Criterion-to-unit matrix, defect register, rollback, cache/versioning | PASS | PASS | PASS | **PASS** | `?v=20260805-pig001-u36` bumped for the last production commit; D-019 ledgered |
| AC27 | Fresh IL assessment confirms buildability | PASS | PASS | PASS | **PASS** | unchanged |
| AC28 | No legal conclusion from death year/host/attribution alone | PASS | PASS | PASS | **PASS** | substance clean at HEAD, including the shipped lede. The guard enforcing it is red (F-9) — a mechanism failure, not a substance failure |
| AC29 | No production edit before `approved_for_build`; merge/deploy need approval | PASS | PASS | PASS | **PASS** | branch verified `pig-001-stabilization`; no merge, push or deploy; untracked files left alone |

\* AC15 was carried PASS in R1–R3 on DOM inference with an explicit NOT-TESTED caveat (A6). R4 is
the first revision in which it passes on the evidence the criterion actually names.

## R4.4 — FINDINGS LEDGER

### CRITICAL — 0

### MAJOR — 2 open

#### F-9 (major, **open**, **blocking**) · the repository test suite is RED at HEAD while the record says green

**What.** `python3 -m unittest discover -s tests` at `06ab20f` returns
`Ran 46 tests … FAILED (failures=1)`. The failing test is
`TestProseLanguage.test_no_artifact_of_ours_asserts_a_legal_conclusion` — the OD-5 guard built
in unit 35 and widened in unit 36. It fires on:

```
protocol/tasks/PIG-001/evidence/harness/vermeer-cert/gapfill.py:28:
OLD_LEDE = "Most reproductions here are public domain."
```

**Where it entered** (my bisection, clean worktrees — R4.1.2): green at `95e5636` (unit 35),
green at `4266804` (**last production commit**), green at `09f61a8`, **red at `a71e2c5`** — the
certification-evidence commit — and red at HEAD.

**What it is not, stated first and plainly.** Not a product defect. Not a user-facing OD-5
breach. Not a failure of any of the 29 frozen criteria — I checked, and the frozen specification
contains no test-suite requirement. The product tree is green. The string is a *reference to* the
old lede, used by the harness to prove the old lede is gone — structurally identical to the six
fixtures inside the test file itself, each carrying an `OD5-EXEMPT` marker.

**Why it blocks anyway.**

1. **The record states the opposite.** D-019 and the build evidence report record *"41 tests
   with 5 failures becomes 46 with 0"*. That was true when written and is false at the SHA being
   certified. A false clearance in the record is what made F-8 major, and the reasoning has to
   apply to us as readily as to a stylesheet.
2. **Theory's operative acceptance criteria fail with it** — #3 ("the complete repository test
   suite passes with its executed test count reported") and #1 ("the validator, **tests**,
   inventories, screenshots, implementation evidence, and Quality Review all correspond to that
   SHA"). Requested action A7 is not discharged.
3. **A red guard stops guarding.** This is the mechanism protecting the owner's own decision
   (OD-5), and unit 35 built it on the explicit principle that *"a rule enforced only where a
   test looks is not enforced."* A rule whose test is permanently red is equally unenforced —
   people learn to skip a suite that is always failing. Leaving it red disables it for every
   future change, which is a larger loss than the string.
4. **It would make this certification falsifiable in one command.**

**Reproduction.** `python3 -m unittest discover -s tests` at `06ab20f`.

**Remedy — not applied by me, and small.** The sanctioned disposition already exists in the
guard's design: append `# OD5-EXEMPT` to `gapfill.py:28` and add
`"protocol/tasks/PIG-001/evidence/harness/vermeer-cert/gapfill.py": 1` to `EXPECTED_EXEMPTIONS`,
so that widening the hole stays a deliberate, reviewable act. Alternatively reword the constant
so it is not a bare assertion. **One line either way.**

**The condition that matters more than the fix:** the suite must be **re-run at the final SHA,
after the last evidence commit**, and its output bound to that SHA. This failure exists because
the suite was run at the commit that fixed it and never again. That ordering requirement is the
same one N-1 imposed on the screenshot pack — which was honoured this round, and should have
been generalised.

#### F-10 (major, **open**, governance-scoped — **does not block Gate 2**; blocks the merge) · the quality gate cannot tell an operative verdict from an archived one, and the kernel change is inside the product merge set

Full reasoning at **A20**. In summary:

- `check_quality_gate` greps an **append-only** review file for the certification marker and the
  two zero-count markers as three independent matches. **Demonstrated, not inferred: the gate
  passed this very report while its operative verdict was `GATE 2: BLOCKED`**, because three
  sentences describing the defect contained the strings it greps for (A20, R4.1.7). Once any
  revision writes a certification, it can never be withdrawn, and the three strings need not come from the same
  verdict. **Inert only because I am blocking.**
- The gate's browser-evidence check accepts any non-zero PNG whose filename contains the right
  substrings — the same failure as the 16 blank screenshots.
- `pigment_coordinator/` (307 lines changed across this branch) is **not a production surface**
  and affects no criterion, but it sits on the branch and would ride into `main` under a product
  approval. **It must be excluded from the product merge set and proposed separately.**

**Disposition:** does **not** block Gate 2 — no criterion turns on it and no user is affected.
It is a **condition on the merge**. Recorded as major so it cannot be discharged silently.

### MAJOR — closed this revision

#### F-8 (major) · `.tl-year` painting `--faint` over `#bg-canvas` on all 8 `#/era/*` routes — **CLOSED, re-verified by me**
`css/styles.css:927` now reads `color:var(--body-ink)`. All three conditions I attached are met:
(1) both false clearances corrected in place — `styles.css:920-926` and
`build-log-unit-29.md:343-365`, the original sentence struck with `~~` and followed by a dated
`CORRECTION` block naming the finding and me, not silently rewritten; (2) the five sibling sites
re-checked by measurement rather than by reading — I re-derived three of them myself
(`#search::placeholder` 4.90/5.17, `.sr-group` 4.62/4.62, `.sr-meta` 5.68/6.42); (3) the ink
enumeration re-run over the `hero()` route families by someone other than its implementer.
**Closed.**

#### V32-1…V32-7, and the two measured-not-cleared residuals (major) · AC19 — **CLOSED, independently remeasured**
2,626 glyph rows across 12 cells, 0 below floor, by an instrument that did not author the fixes.
V32-7 was a stacking defect, not a colour one — `z-index:3` on `.search-wrap` (`styles.css:478`)
settles a flex `order` repaint; I verified the fix and re-derived the ink at 4.62 in both themes.

#### F-1 (was minor) · horizontal overflow at 821–1100 px — **CLOSED, confirmed independently**
0 px at all eight widths including 900 and 1024, previously 150/113/54/18. Confirmed by an
instrument that is not the one that fixed it, and probed on both document scroll width **and**
per-element border boxes, because `body{overflow-x:hidden}` was clipping the symptom.

#### AT-1, AT-2, AT-3, AT-4, AT-6, AT-7 (six of seven AT findings) — **CLOSED BY EAR**
Confirmed by the operator in session 3, not by DOM assertion. AT-1 is the significant one: the
core Taste loop is now operable by a blind user. I verified the mechanism in source — two
deliberate halves (a labelled `role="group"` and per-button `aria-label`s for exploration; the
live `obDeckSay()` for the card change that moves under a stationary focus), plus the owner's
requested quarter-point cadence at `js/app.js:3256`.

### MINOR — 4 open, none blocking

#### F-2 (minor, open) · AC17 · the last nav destination's focus indicator is faded by the mask, ≤820 px
Unchanged through four revisions. Theory asked for it (A3); I can find no evidence it was
corrected. Focus is degraded, not absent. **Schedule it.**

#### F-11 (minor, **new**) · AT-5 · the SEO-page arrow residual is 695 files in four families, not "~100" in one
`build-log-unit-34.md:78-84` carves out *"`p/artwork/*.html` … ~100 static files"*. Measured by
me: `p/artist` 256, `p/artwork` 323, `p/list` 12, `p/museum` 104 = **695**, corroborated by the
asset inventory's own stub-file count. Each carries a bare `→` inside link text
(`>Open in the atlas →<`) with no `aria-hidden`. These are crawlable entry points. The
carve-out is honest in kind and wrong in size; restate it before the Human Review Package. See
**A19**.

#### V-M1 (minor, open) · `.md-name` renders at 2.34 px (320) / 2.97 px (390)
Legibility, not contrast; europe-zoom state only; accessible name preserved via each dot's
`<title>`. Outside AC19's frozen scope (**A18**), real for a low-vision user. Not fixed in this
build, and correctly disclosed as not fixed.

#### AT-5 (minor, open) · decorative arrows, **unconfirmed by ear**
Fixed in the DOM for every JS- and CSS-emitted arrow in the app; **not re-heard**. Unit 34
records it as *"fixed and awaiting the ear"* rather than closed, which is the correct posture
after unit 33 recorded it closed when it was not. Do not close it on a DOM sweep.

### NOTES

- **N-1 — CLOSED.** The screenshot pack was recaptured at `a71e2c5`, which post-dates the last
  production commit `4266804`; I verified the intervening commits move no production file. The
  ordering condition I imposed in R3 was honoured. 64 screenshots recaptured, all four
  viewport×theme cells present and non-empty.
- **N-8 — CLOSED.** Matisse, PASS WITH NOTE. He corrected his own reasoning (light is the
  marginal theme, not dark) and stated that the hover thickening is held *"on defence, not
  observation"* because his browser hung before he could capture the frame. **I accept the note
  as written**: the rule exists as specified at `styles.css:333-336`, the missing artefact is one
  hover frame, and I agree it does not block. Recording an unobserved thing as unobserved is the
  behaviour I want from an adjudicator.
- **N-6 (open)** — dark `--gold2` at 4.31 against the absolute canvas ceiling. Reproduced by me
  again this revision at 4.31. Disclosed and argued (D-29-7); the corner is geometrically
  unreachable. Not a blocker; recorded so the margin stays visible.
- **F-6 (open)** — deployment-gated third-party request condition (AC25). Unchanged.
- **N-3 (open)** — unchanged.
- **New note · the engine gap.** Every pixel measurement in this build is Chrome; every ear
  confirmation is Safari. No single engine has both. See **A17.2** — this is the most consequential
  uncovered area in the task and it cannot be closed with more of either instrument.

## R4.5 — REGRESSION SWEEP AT HEAD

- **Validator:** clean, zero warnings, all references valid — identical to R1, R2, R3.
- **Test suite:** 46 tests, **1 failure** (F-9). 45 of 46 green, including all rights-tooling,
  register-language, denominator and coordinator tests.
- **Asset inventory:** regenerated by me at HEAD, **byte-identical** to the committed copy. 798
  unique / 797 rendered / 0 copyright-suppressed URLs leaking into public metadata.
- **26 routes:** 0 console errors, 0 warnings, 0 requests ≥400 of 107, 680 images 0 broken,
  `upload.wikimedia.org` the only third-party host, 0 Google Fonts.
- **Live region:** exactly one in the shipped source, outside `#app` — I grepped for all of
  `aria-live`, `role="status"`, `role="alert"`. 0 mutations across 12 route changes with a
  positive control proving the observer was live.
- **Cache/versioning:** `?v=20260805-pig001-u36`, bumped at the last production commit.
- **Branch discipline:** `pig-001-stabilization`, never `main`. No merge, no push, no deploy.
  Untracked `THEORY_001.md`, `passport-test.html`, `.gitignore` left untouched.
- **No regression found** in any previously certified surface. Units 33–36 close findings and
  introduce none that I can measure — the single new defect this revision (F-9) is in evidence
  code and was introduced by the evidence commit, not by a build unit.

## R4.6 — PRESSURE, AND HOW I MADE THIS CALL

I was told plainly that this is the fourth attempt, that ninety-six commits and three human
sessions stand behind it, and — correctly — that manufacturing a blocker to avoid the discomfort
of certifying is the same failure as certifying too readily. I have tried to hold both.

**What I did not do.** I did not block on any of the 29 criteria. All 29 pass, and I moved AC19
from FAIL to PASS and AC15 from a caveated PASS to a real one. I did not block on `.md-name`,
which is a real defect I could have stretched into AC19 and did not, because AC19 is a contrast
criterion and stretching it would have been exactly the manufacture I was warned about. I did not
block on AT-5, F-2, F-11, N-6 or D-017's governance defect — each is real, each is recorded, none
of them blocks. I did not block on the inventory's SHA label, which I expected to raise as a
finding until I regenerated it and found it byte-identical.

**What I did.** I ran the first check I was told to run and it came back red at the SHA I was
asked to certify, against a record that says it is green. I bisected it to be sure it was real
and to find where it entered, and it entered through the certification evidence itself. I then
had to decide whether a one-line annotation in a harness file should stop this.

The argument for certifying is strong: no user is affected, the product tree is green, the fix is
trivial. The argument that decided it is that this build's one persistent failure — five times
now — is a true report about a smaller universe than the claim it supports, and the fifth
instance is a claim that the tests pass, made about a different commit than the one being
certified, discovered inside the artefact built to be the independent check. If I certify past
that, I am ruling that nobody needs to run the suite at the SHA they certify. That is the
discipline theory asked for, the discipline the owner's OD-5 guard depends on, and the discipline
whose absence produced every other finding in this ledger.

**Blocking here costs one short round. Certifying here costs the meaning of the gate.** I have
kept the blocker as narrow as I can make it: one finding, one line, one re-run, and an explicit
statement that everything else is ready.

I want the last word to be the other half of the truth, because it would be unjust to end on the
blocker. **This is the strongest state PIG-001 has been in.** AC19 passes after three revisions
of my refusing it. AC15 passes on the evidence it actually named, and the sessions that got it
there found seven defects no instrument could have found — including one that made the core
product loop unusable by a blind user. Six of seven were repaired and confirmed by ear. Every
pole in this task corrected itself against interest at least once, some against their own
colleagues. The one finding I am holding is a comment marker away from closed, and when it is
closed I expect to certify.

---

# REVISION 3 (2026-07-29) — SUPERSEDED BY REVISION 4

*Preserved verbatim. Its verdict is superseded; its findings and adjudications A13–A16 remain
the record of what was blocked and why. Its blocking finding, F-8, is **closed** — see R4.4.
Where Revision 4 changes a criterion status, R4.3 and R4.4 say so explicitly.*

**Product tree reviewed at:** `11e4471` (HEAD at the time). Production code last moved at
`094a631` (unit 30c); `11e4471` was evidence-only.

**Independence:** I wrote none of this code and I fixed nothing I found. This round I ran
two of the build's own instruments myself, on routes their authors did not walk, and I
re-derived ten published contrast figures from the committed CSS with my own arithmetic
before accepting any of them.

## R3.1 — What this revision is

Revision 2 blocked on F-7: `--faint`/`--muted` small text and the light global link colour
failing over `#bg-canvas`. Since then five commits landed:

| Was | Work | Now |
| --- | --- | --- |
| F-7 (AC19 FAIL) | Unit 29 (`4362c8a`) bounded `#bg-canvas` **from source** — 2⁸ corner enumeration — and re-pointed 26 selectors | **Closed for 26 of 27 call sites.** One residual site survives and fails → **F-8** |
| D-29-6 (light link/body separation) | Matisse's ruling (`c873fe6`); applied as unit 30b (`a2ca161`) | Note, discharged |
| N-4, N-1, N-5 | Vermeer's final pass (`821fe60`) | N-4 **closed**; N-5 substantially discharged; N-1 **stale a third time** |
| — (new) | Vermeer reopened AC19 on the `.hero` cover (V-F3); unit 30a/30c (`8d3a3ee`, `094a631`) closed it on four route families plus `.era-tile` | V-F3 **closed**, verified by me |

**AC19 fails again, on a new finding, for the reason this review was asked to test.**

## R3.2 — Checks I ran myself, with output

### R3.2.1 Validator — `osascript -l JavaScript tools/validate.jxa.js`

```
app.js: syntax OK
artists: 256, movements: 76, techniques: 39, eras: 8, nations: 37, painter styles: 27,
influence edges: 238, venues: 116, catalog: 323 (tier1: 76), daily pool: 75,
museum notes: 104, photo credits: 104 (attribution required: 88),
artwork image credits: 27, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```

Zero errors, **zero warnings**, all references valid — byte-identical to my Revision 1 and
Revision 2 runs. AC2 continues to hold. N-3 (corpus counts vs the spec's frozen assumption,
cause D-016) unchanged.

### R3.2.2 Source spot-checks — units 29 and 30 verified in the file, not in the log

| Claim | Verified | Where |
| --- | --- | --- |
| `--hero-text-veil:.80` declared in **both** theme blocks | **yes** | `styles.css:185` (dark), `:241` (light) |
| Veil on the **text block**, 18 px feather | **yes** | `styles.css:604-610` — `.hero-content` gradient |
| `.hero .hero-shade` reduced to `.06 → .30` | **yes** | `styles.css:588-591` |
| Hero focus ring re-pointed, light only | **yes** | `styles.css:626` — `html[data-theme="light"] #app .hero-content h1:focus-visible{outline-color:#6b5122}` |
| `.era-tile .et-label` veil, **10 px** feather, `.et-shade` at `.06 → .30` | **yes** | `styles.css:1106-1112`; `padding:12px 14px` confirms 10 < 12 |
| Underline selector and **both** `:not()` exclusions | **yes** | `styles.css:307` — `#app p:not(.img-credit):not(.footer-note) a:not([class])`, `text-decoration-color:currentColor` at `:310` |
| Unit 29's light `--gold2` = **`#544019`** (not the `#6b5122` I specified) | **yes** | `styles.css:212` |
| 20 `canvasTag` call sites, at the lines Dürer's table names | **yes** | my own `grep -n canvasTag js/app.js` returns the definition at `:775` and exactly 20 call sites: 789, 805, 816, 833, 1434, 1500, 1553, 1583, 1602, 1630, 1698, 1793, 1883, 1951, 1993, 1995, 2078, 2139, 3216, 1948 |
| `?v=` bumped | **yes** | `index.html:27` → `20260729-pig001-u30` |
| `js/app.js` untouched by units 29–30 | **yes** | `git show --stat`; `?v=` still `u25f` |

**I also checked for cover surfaces the enumeration could not see.** `grep url( css/styles.css`
returns **only** `@font-face` sources — there is no CSS background image anywhere. The only
overlay-scrim elements in the build are `.hero-shade` (twice: `hero()` and `.home-hero`),
`.mu-shade` and `.et-shade` — exactly the four instances now fixed. `.card-art`, `.mini-card`,
`.le-art`, `.arc-work-gen` set their text in **sibling** blocks on opaque `--panel` paint, so
their `<img>` variants (which the canvas-differential enumerator is blind to) carry no overlaid
text either. `.daily-media > span` **is** text over a photograph and is in no enumeration; I
derived it myself — `#f2eee5` on its own `rgba(10,9,8,.76)` pill over a worst-case white
photograph pixel gives **8.40**, PASS. `.taste-map` carries `background:var(--panel)`
(`styles.css:1471`), so its `fill:`-inked labels are shielded.

### R3.2.3 I re-derived ten published figures myself, from the committed CSS

Not one taken on report. sRGB relative luminance, WCAG 2.x:

| source | claim | Dürer's | **mine** |
| --- | --- | --- | --- |
| u30 §2.3 | light `--gold2` `#544019` on the veil at `.74` | 4.50 | **4.50** |
| u30 §2.3 | same at the shipped `.80` | 5.27 | **5.27** |
| u30 §2.3 | light `--body-ink` at `.80` | 5.80 | **5.80** |
| u30 §2.3 | light `--ink` `h1` at `.80` | 7.99 | **7.99** |
| u30 §2.3 | dark `--gold2` / `--body-ink` / `--ink` at `.80` | 6.84 / 7.25 / 8.78 | **6.84 / 7.25 / 8.78** |
| u30 §2.7 | light `--gold` ring on the veil | 2.13 | **2.13** |
| u30 §2.7 | `#6b5122` ring on the veil | 3.96 | **3.96** |
| u29 §1 | `--faint` vs the ALL ceiling, dark / light | 1.82 / 2.57 | **1.83 / 2.58** |
| u29 §1 | `--muted` vs the ALL ceiling, dark | 2.24 | **2.25** |
| u29 §3a | `#6b5122` vs the light ceiling — **why my own specified value was rejected** | 3.42 | **3.43** |
| u29 §3a | `#544019` vs the light ceiling | 4.55 | **4.56** |

Every figure reproduces to ±0.01. **Dürer was right to overrule the `#6b5122` that Matisse and
I both specified**: it is a large-text gradient stop and it does not clear as small text. I
record that as a correction to my own Revision 2 remedy.

The veil bounds are **bounds, not samples** — the veil is anchored to the text block, so the
composited backdrop is `cover·(1−v) + page·v` for *any* cover pixel, independent of hero height
or subject. That is the same structural property that made unit 27 certifiable, and it is why
V-F3's closure does not depend on which 12 painters were sampled.

### R3.2.4 I ran the build's own enumerator on the routes nobody walked

This is the check the brief asked for, and it is the one that decides this review.
`harness/durer-u28/enumerate_overcanvas.py`, unmodified, driven against a local server on a
private port, at **light 1440×900** and **dark 390×844**, over **18 route strings** (14 render
distinct content) that appear in **no** sweep's `ROUTES` list — the four `hero()` route families
among them. Every element over `#bg-canvas` scored against unit 29's own derived ALL ceiling:

```
#/era/16th-century         els=207  over=49   BELOW-CEILING=2   (light 1440)
       ('span.tl-year.end',   (112,103,85), 11.2px, 2.58, floor 4.5)
       ('span.tl-year.start', (112,103,85), 11.2px, 2.58, floor 4.5)
#/era/19th-century         els=516  over=49   BELOW-CEILING=2
#/movements  #/techniques  #/nations  #/movement/impressionism
#/technique/oil-painting   #/nation/italy   #/eras   #/influences
#/timeline   #/daily       #/explore  #/museums      BELOW-CEILING=0
```

```
#/era/16th-century   (dark 390)   span.tl-year.start / .end  (139,131,114) 11.2px  1.83  floor 4.5
```

### R3.2.5 …then measured it on real pixels with Dürer's pixel instrument

`harness/durer-u28/canvastext.py` at HEAD — the corrected-origin version — 4 random draws per
route, `prefers-reduced-motion:reduce`, three-shot glyph differential:

```
light 1440×900, #/era/16th-century + #/era/19th-century
  span.tl-year.end     4.06  need 4.5  FAIL   [112,103,85] -> [229,218,206]  (no-canvas [242,236,223])
  span.tl-year.start   4.28  need 4.5  FAIL   [112,103,85] -> [229,225,215]
  (10 other classes 6.40 – 12.09, all pass)          classes below floor: 2 of 12

dark 390×844, same two routes
  span.tl-year.start   4.19  need 4.5  FAIL   [139,131,114] -> [33,36,29]   (no-canvas [13,12,10])
  span.tl-year.end     4.47  need 4.5  FAIL   [139,131,114] -> [27,30,29]
  (8 other classes 10.52 – 15.24, all pass)          classes below floor: 2 of 10
```

**It fails on all three instruments** — the derived ceiling (1.83 / 2.58), the 84-draw sampled
model (`--faint` 3.69 dark / 3.22 light, unit 29 §1), and real rendered pixels (4.06–4.47).
This is not a worst-corner contrivance.

### R3.2.6 F-1, F-2, N-4 re-checked at HEAD

- **F-1** — `.daily-media` is still 520 px fixed with `min-height:390px` (`styles.css:995-999`),
  untouched by every commit since `4fc8239`. Stands, minor, adjudication **A1** unaffected.
- **F-2** — the nav mask `linear-gradient(90deg,#000 78%,transparent)` is still present.
  Stands, minor.
- **N-4** — `grep -cE '^<!--PLACEHOLDER-[A-Z]+-->$' browser-evidence-closing.md` returns **0**.
  The four surviving string matches are quoted references inside prose describing the repair.
  **Closed, verified by me, not on assertion.**

## R3.3 — THE DECISIVE RESULT, AND WHETHER IT WAS ALREADY KNOWN

**It was named, and it was affirmatively cleared — wrongly, by two people.**

Unit 29 §7.1 (`build-log-unit-29.md:342-345`):

> `--faint` is effectively retired as a page-background ink. It survives at
> `#search::placeholder`, `.sr-kicker`, **`.tl-year`**, `.tn-count`, `.tm-lab` and
> `.pp-card-loading` — **all inside opaque panels**, all still clear on Pass 1.

Matisse's ruling repeats it as settled (`visual-ruling-d29-6.md:267-271`): *"Their surviving
sites … are correct and stay."*

**`.tl-year` is not inside an opaque panel.** `.timeline` (`styles.css:852-855`) declares
`position:relative`, margins, padding and two 1 px borders — **no background**. `.tl-year`
(`styles.css:871`) is `position:absolute; bottom:14px; color:var(--faint)` at 11.2 px, and it
renders on `#/era/*` (`js/app.js:2112-2118`) — all **8** eras, reachable from the "Begin with an
era" strip on `#/`. Dürer's own enumerator, run by me, reports it `overCanvas: true` with
`shieldedBy: null`.

So this is **worse than an unmeasured surface**: it is a false clearance in the build record.
It is not in unit 30's enumeration table (that table covers `canvasTag` cover hosts and
excludes `#bg-canvas` by design), not in Vermeer's NOT TESTED list, and not in the qualified
closing statement — which claims support "for every surface that has been enumerated and
measured", and this one was neither.

**Why it survived, precisely.** AC19's composite surface has two layers, and they were closed
by two enumerations with **non-overlapping coverage gaps**:

| layer | closed by | enumerated over | gap |
| --- | --- | --- | --- |
| `#bg-canvas` (site-wide) | unit 29, bound at source + **ink call-site** enumeration | **19 routes** — containing **none** of `#/era/*`, `#/movement/*`, `#/technique/*`, `#/nation/*` | those four route families |
| `canvasTag` covers (20 sites) | unit 30, paint differential | 12 routes, **but** `#bg-canvas` deliberately excluded | the `#bg-canvas` layer on any route |

Unit 30 walked `#/era/16th-century` — but only through `covertext.py`/`herotext.py`, which scope
to cover hosts and to `.hero`. Unit 29 scored every ink — but never loaded an era route.
`.tl-year` sits exactly in the seam. **The host census is what put it there.**

## R3.4 — ADJUDICATIONS

### A13 — Is a host census sufficient for AC19? **No.** (the central question)

Dürer's bound is honest and precisely worded, and I want to be exact about what I am rejecting.
His **call-site enumeration is genuinely complete** — I verified the count of 20 independently
against `js/app.js`, and his classification by measured paint differential rather than by
reading the CSS is the right method, arrived at for the right reason. That part I certify.

What does not carry is the extrapolation: *"every unwalked route renders only hosts already in
the table, so the class is covered even where the route was not walked."*

**First, on its own terms it re-imports the error it was built to eliminate.** The census's
whole virtue is that membership is decided by measurement, not by reading the code — because
reading the code is how four instances were missed. At the route boundary that discipline is
dropped: the claim that the 12 unwalked routes render only known hosts is a *reading of the
view builders*, unmeasured. A census whose perimeter is defended by the method it replaced is
sound inside the perimeter and inferential outside it, and AC19 is a criterion about composites
"that require browser measurement".

**Second, and decisively, it is false in a way that matters.** The premise is true about
`canvasTag` hosts and false about the criterion. AC19's unit is not the host — it is the
**(ink, size, backdrop) triple**. An unwalked route can introduce a new *ink over an old
backdrop*, and that is precisely what `#/era/*` does: no new host, no new cover, one old ink
(`--faint`) on the oldest backdrop in the build (`#bg-canvas`). The host table cannot see it
because the host table excludes that layer, and the layer's own enumeration never walked the
route. I did walk it, and it fails on three instruments.

**Ruling: for AC19, a host census is not sufficient.** The criterion is closed only when every
*ink call site* has been scored against every *backdrop it can reach*, and that requires either
a route census or a source-level argument that covers the unwalked routes — the kind unit 29
made for the backdrop and did not make for the inks. The unwalked half of the route table left
the criterion unsupported, and concealed a live failure. Recorded as **F-8 (major)**.

I record what this ruling does **not** say: it does not say the enumeration was wasted or
wrong-headed. It is the best instrument this build has produced, it converted 14 assumed passes
into measured ones, and it found `.era-tile` before a reviewer did. The defect is in the
perimeter argument, not in the census.

### A14 — The two out-of-brief fixes: **both correct. Not scope creep.**

**D-30-6 (`.era-tile`) — correct, and required.** Dürer's reasoning is the right reasoning:
writing "AC19 is fully supported" while leaving a measured, criterion-failing surface open
would have been a false statement in a certification package. The fix is inside the same
criterion, the same defect class and the same remedy geometry as the brief's own item; it adds
no token and no new value (it reuses `--hero-text-veil`, with a 10 px feather because the tile's
`padding-top` is 12 px — a value the geometry forces, and stated rather than hidden). Measured
1.44–1.79 → 8.71–10.36. Finding it and *not* fixing it would have been the scope-creep-avoidant
choice and the wrong one.

**D-30-4 (hero focus ring) — correct, and the stronger case of the two.** This was **not** a
pre-existing defect he wandered into: his own veil created the deterministic backdrop against
which light `--gold` reads 2.13 under WCAG 1.4.11's 3.0 floor. A fix that introduces a new
failure and ships it unfixed is a regression, and an implementer who found it and left it for
the reviewer would be gaming the gate. I re-derived both figures myself (2.13 → 3.96) and the
remedy reuses unit 27's colour on a scoped selector.

**The boundary he drew is the right one**, and I note it because it is what distinguishes these
two from creep: he *declined* Matisse's §1d follow-on as out of Gate 2 scope, on the ground that
it is a cosmetic consistency item that would reopen certified evidence. Criterion-failing →
fixed; cosmetic → deferred. That is the correct line, applied consistently, and both deviations
are in the ledger where a reviewer can find them. **Accepted, both.**

### A15 — Prior findings

- **F-1 (821–1100 px overflow) — stands, minor.** Re-verified in the tree (R3.2.6). Outside
  AC18's frozen viewport set; adjudication **A1** unchanged. Schedule it.
- **F-2 (masked nav focus ring ≤820 px) — stands, minor.** Re-verified. Focus is degraded, not
  absent; predates the build.
- **N-4 (placeholders) — CLOSED.** Verified by anchored grep, 0 unrendered markers.
- **N-5 (unit 28's sweep run light@1440 only) — substantially discharged.** Dark and 390 cells
  now exist for the canvas class (unit 30 §1.3: 1,501 previously-untested scrolled rows measured,
  0 below floor) and for the hero class (1,956 in-hero measurements across four cells). The
  condition I attached — that verification be done by someone other than the implementer — is met
  for units 27 and 29 by Vermeer, and for unit 30 by me. **What N-5 has become is A13**: the gap
  moved from *cells* to *routes*.
- **N-1 (screenshot pack) — stale a third time. Still a note, not a blocker.** The 64-shot
  re-capture carries mtimes of 2026-07-28 17:10–17:12; units 30a/30b landed 22:56, 30a-follow-on
  23:08, and 30c at 04:15 the next morning. Unit 30 shipped 8 `u30-*` shots of two hero subjects,
  which are current for 30a but predate 30c; **`.era-tile` (30c) and the underline (30b) appear
  on no shot in the pack.** Ruling unchanged from **A10**: no criterion turns on a picture, and
  the stale shots understate the build. It does not block. But it is now the third consecutive
  round in which the pack has been re-captured mid-flight and immediately overtaken, and F-8's
  fix will overtake it a fourth time — so **the pack must be captured once, after the last
  production commit, and that ordering should be a condition on the Human Review Package rather
  than a task anyone repeats per unit.**

### A16 — Instrument credibility: **trustworthy enough to certify against.**

Two systematic defects were found mid-build: the tainted/`visibility:hidden` canvas read, and
the clip-origin page-vs-viewport error that invalidated 89 of Dürer's rows and 151 of Vermeer's.
Both are the kind of defect that should worry a certifier. I judge the corrected instruments
sound, on four grounds I checked rather than assumed:

1. **Both were found by their own operators and published against their own interest.** Vermeer
   withdrew a `card-tagline` 4.10 failure of his own; Dürer withdrew three rows of his and
   re-analysed his whole archive by scroll position rather than asserting the conclusion
   survived. I confirmed the re-analysis is real: the corrected run reports 0 below floor on
   1,069 / 763 over-canvas rows, and I reproduced the pattern on my own two runs.
2. **The corrections are structural, not patches.** The clip fix adds the scroll offset at
   capture *and* asserts `scrollY` is unchanged mid-capture — an assertion that then earned its
   keep by catching the `display:none` reflow in `covertext.py`.
3. **Cross-operator agreement on the numbers.** Vermeer's independent museum-band figures agree
   with Dürer's to ≤0.08; unit 30's `U30_BEFORE=1` mode reproduces Vermeer's published hero
   failures (`h1` 2.40 light / 2.35 dark) exactly.
4. **I reproduced ten of their published figures from the committed CSS by my own arithmetic,
   to ±0.01** (R3.2.3), and the instruments then produced my new finding when I aimed them at
   new routes. **The instruments are sound; the aiming was not.** That is the correct diagnosis
   and it is what A13 turns on.

**What remains unverifiable, and must not be read as passing:**

- **SVG text inks.** `enumerate_overcanvas.py` reads `getComputedStyle().color`; `.tn-count` and
  `.tm-lab` are inked with `fill:`, so their ink is mis-read wherever they are enumerated. I
  established by source that both sit on opaque paint (`.tree-svg .tree-node rect{fill:var(--panel2)}`,
  `.taste-map{background:var(--panel)}`), so no defect is implied — but the class is invisible to
  the instrument and any future SVG text will be too.
- **`#/taste` and `#/palette` have only ever been enumerated in their no-passport state** (29
  text elements — the onboarding CTA). Their real content, including the taste map, is unmeasured
  by every sweep including mine.
- Real assistive technology; browsers other than Chrome; `deviceScaleFactor ≠ 1`; 200 % text zoom
  over the three new veils; deployed identity at the GitHub Pages origin (F-6); artists beyond
  the 12 sampled — though for the veiled surfaces that is a bound, not a sample, and I verified
  the bound.

## R3.5 — ACCEPTANCE CRITERIA — ALL 29, CURRENT

**PASS 28 · FAIL 1 · UNSUPPORTED 0**

| # | Criterion (abbrev.) | R1 | R2 | **R3** | Evidence |
| --- | --- | --- | --- | --- | --- |
| AC1 | `effa805` baseline named, older labelled historical, deployed-identity proof defined | PASS | PASS | **PASS** | unchanged |
| AC2 | Validator: no errors, refs valid, unedited snapshot | PASS | PASS | **PASS** | **my run, R3.2.1** — zero errors, zero warnings |
| AC3 | Two deck warnings cleared on merit or owner exception | PASS | PASS | **PASS** | `deck-merit-review.md`; my validator run confirms 0 warnings |
| AC4 | Frozen first-user journey matrix, no broken/unexplained transition | UNSUP | PASS | **PASS** | `browser-evidence-closing.md` §2 — 33 steps, 0 FAIL (**A7**). Not re-exercised at this HEAD; units 29–30 are CSS-only and `js/app.js` is byte-unchanged |
| AC5 | Import: per-field identify, explicit confirm, cancel/malformed preserves local | PASS | PASS | **PASS** | unchanged |
| AC6 | Admire/Seen/Saved independent, accurate visible + programmatic state | PASS | PASS | **PASS** | unchanged |
| AC7 | Five interruption checkpoints resume exactly | PASS | PASS | **PASS** | unchanged (**A5** carry-forward) |
| AC8 | Storage failure: no false success, context preserved, retry/recovery/export | UNSUP | PASS | **PASS** | **A8**, my source trace; F-4 retracted |
| AC9 | Invalid-route/no-match/empty/limit/failure preserve context + next action | PASS | PASS | **PASS** | unchanged |
| AC10 | Frozen asset inventory, exact counts by surface + reachability | PASS | PASS | **PASS** | unchanged |
| AC11 | Item-level rights sample ≥100 incl. Tier1∪daily + all Matisse/Kahlo | PASS | PASS | **PASS** | unchanged — 122 entries |
| AC12 | Mismatches/unresolved/out-of-sample stay explicitly unresolved | PASS | PASS | **PASS** | unchanged |
| AC13 | Historical sample: 10 profiles, ≥5 eras/movements/nations, 5 claim classes, 20 edges | PASS | PASS | **PASS** | unchanged |
| AC14 | Release language checked, no overclaim | PASS | PASS | **PASS** | unchanged. Unit 30's closing statement is scoped rather than absolute, which is the behaviour this criterion wants |
| AC15 | Title updates, one identity to AT, focus to entry point, no repeat announcements | PASS | PASS | **PASS** | my R1 §2.6; re-confirmed at HEAD by `browser-evidence-final.md` §6 — 0 live regions, 0 live mutations across 5 route changes, `activeElement` = route `h1[tabindex="-1"]`. Real screen-reader output NOT TESTED (**A6**) |
| AC16 | Selected/current/expanded/pressed/active: visible + programmatic, not colour/position/hover alone | PASS | PASS | **PASS** | unchanged. R2's `a.active` caveat is resolved — I measure it 7.97 over the canvas on `#/era/*` at HEAD |
| AC17 | Keyboard-operable with visible focus; bypass; no nested interactive | PASS | PASS | **PASS** | unchanged; **strengthened** by D-30-4 — the hero focus ring 2.13 → 3.96, re-derived by me. F-2 minor, re-checked |
| AC18 | 320/390/768/1280/1440 + 200 % zoom: destinations reachable, no root overflow | PASS | PASS | **PASS** as frozen | unchanged; 821–1100 band outside the frozen set → **A1**, F-1. 200 % zoom over the three new veils NOT re-measured (unit 30 §6.6) — the veil is text-block-anchored with an 18 px feather under a 22 px minimum padding, so reflow cannot put a glyph in the ramp; recorded, not relied on |
| AC19 | Both themes pass AA for frozen text/control/focus/state pairs **incl. browser-measured composites** | UNSUP | FAIL | **FAIL** | Very large closure this round — V-F3 closed on **four** route families (831 in-hero failures → 0, bound re-derived by me), `.era-tile` closed, the hero ring closed, 1,501 scrolled canvas rows measured, F-7 closed at 26 of 27 call sites. **But `span.tl-year` (`--faint`, 11.2 px) paints over `#bg-canvas` on all 8 `#/era/*` routes and measures 4.06/4.28 light and 4.19/4.47 dark on real pixels** — and the build record affirmatively clears it as panel-shielded, which it is not. **Adjudication A13 · F-8** |
| AC20 | Reduced motion preserves info/choices; canvas + relationship viz have alternative + accessible name | PASS | PASS | **PASS** | unchanged; units 29–30 add no transition beyond a decoration-thickness transition on prose links |
| AC21 | Frozen fixture, six classes, no starvation, count/selection/dismissal/focus-return | PASS | PASS | **PASS** | unchanged |
| AC22 | Home Explore promise = Explore destination; every instrument reachable | PASS | PASS | **PASS** | unchanged |
| AC23 | Named adjudicator reviews hierarchy/relationship/entrances/identity without claiming comprehension | PASS | PASS | **PASS** | **A4** unchanged. **N-2 substantially closed**: Matisse ruled on D-29-6 at `c873fe6`, overturning the premise he was given (dark separation 1.06:1 is *worse* than light's 1.10:1) and declining the pre-existing defence himself. His §Review of the underline against real prose is still outstanding → N-8 |
| AC24 | ≥1 relationship journey: named entities, relationship + consequence, anchor, onward path | PASS | PASS | **PASS** | unchanged |
| AC25 | Every third-party runtime request identified; undisclosed fails | PASS | PASS | **PASS** (disclosure) | re-confirmed at HEAD — `browser-evidence-final.md` §6: 26/26 routes, 0 console errors, 0 warnings, 0 requests ≥400 of 107, 680 images 0 broken, `upload.wikimedia.org` only, 0 Google Fonts. Deployment-gated condition remains **F-6** |
| AC26 | Criterion-to-unit matrix, defect/deferred register, rollback, cache/versioning | PASS | PASS | **PASS** | unchanged; `?v=` bumped to `20260729-pig001-u30`; D-30-1…D-30-8 ledgered |
| AC27 | Fresh IL assessment confirms buildability, doesn't lean on the 14-unit plan | PASS | PASS | **PASS** | unchanged |
| AC28 | No legal conclusion from death year/host/attribution alone | PASS | PASS | **PASS** | unchanged |
| AC29 | No production edit before `approved_for_build`; merge/deploy need explicit approval | PASS | PASS | **PASS** | branch verified `pig-001-stabilization` at HEAD; units 29–30 committed by explicit path; three untracked files left alone; no merge, no push, no deploy |

## R3.6 — FINDINGS LEDGER

### CRITICAL — 0

### MAJOR — 1 open

#### F-8 (major, **open**) · AC19 · `.tl-year` paints `--faint` over `#bg-canvas` on every `#/era/*` route, and the record wrongly clears it

**What.** `.tl-year` (`css/styles.css:871`) — `position:absolute; bottom:14px;
font-size:.7rem; color:var(--faint)` — renders the era's start and end years inside
`<div class="timeline">` (`js/app.js:2112-2118`) on all **8** `#/era/*` routes, reachable from
the "Begin with an era" strip on `#/`. `.timeline` (`styles.css:852-855`) declares **no
background**, so the glyphs composite directly over `#bg-canvas`.

**Measured, by me, with the build's own instruments at HEAD:**

| instrument | theme / viewport | value | floor |
| --- | --- | --- | --- |
| `canvastext.py` real pixels, 4 draws | light 1440×900 | **4.06** (`.end`), **4.28** (`.start`) | 4.5 |
| `canvastext.py` real pixels, 4 draws | dark 390×844 | **4.19** (`.start`), **4.47** (`.end`) | 4.5 |
| unit 29's derived ALL ceiling | light / dark | **2.58 / 1.83** | 4.5 |
| unit 28's 84-draw sampled model (`--faint`) | light / dark | 3.22 / 3.69 | 4.5 |

It fails on every instrument the project owns. It is the **only** residual member of F-7's class:
my enumerator run over 18 unwalked route strings in both themes found no other ink below the
ceiling except dark `--gold2`, which is separately disclosed (N-6).

**Why nobody saw it.** Unit 29's ink enumeration ran over 19 routes that include **none** of
`#/era/*`, `#/movement/*`, `#/technique/*` or `#/nation/*`; unit 30 walked era routes but only
through cover-host and `.hero`-scoped instruments, with `#bg-canvas` excluded by design. The
element sits in the seam between the two enumerations. See **A13**.

**It is worse than unmeasured — it is mis-cleared.** `build-log-unit-29.md:342-345` lists
`.tl-year` among the surviving `--faint` sites and states they are *"all inside opaque panels"*;
`visual-ruling-d29-6.md:267-271` adopts that and rules them *"correct and stay"*. Dürer's own
enumerator, run by me, returns `overCanvas: true, shieldedBy: null` for this element in both
themes. A future author reading the build record would conclude the opposite of the truth.

**Reproduction.** `python3 -m http.server 8431 -d .`, then
`PIG_BASE=http://localhost:8431 python3 harness/durer-u28/canvastext.py light 1440 900 4 tag "#/era/16th-century,#/era/19th-century"`.
Or read it: `#8b8372`/`#706755` at 11.2 px, no opaque ancestor between `span.tl-year` and
`<body>`.

**Remedy — not applied by me, and small.** The rule unit 29 wrote into the stylesheet already
decides it: *small text on the page background takes `--body-ink` or `--ink`.* Re-point
`.tl-year` to `--body-ink`, which measures 5.01 light / 4.55 dark against the derived ceiling.
One declaration. No token, no new value, no visual-direction decision — this is the 27th member
of a class where 26 have already been re-pointed the same way.

**Conditions on closing it, and they are the point of this finding:**

1. **The two false clearances in the record must be corrected**, in `build-log-unit-29.md` §7.1
   and in Matisse's ruling — not silently, but as a correction, since both are now cited as
   settled.
2. **The other five sites in that same sentence must be re-checked by measurement, not by
   reading** — `#search::placeholder`, `.sr-kicker`, `.tn-count`, `.tm-lab`, `.pp-card-loading`.
   I checked them from source and believe all five are genuinely shielded (`--panel`/`--panel2`
   ancestors, and `.taste-map{background:var(--panel)}`), but two of them are SVG `fill:` inks the
   enumerator cannot score (A16), and `.tm-lab`/`.pp-card-loading` live on routes no sweep has
   ever rendered in a populated state. The claim that failed here is *exactly* the claim that
   still covers them.
3. **The ink enumeration must be re-run over the four `hero()` route families** at both themes
   and both viewports — the routes that produced this finding — and by someone other than its
   implementer.

### MAJOR — closed this revision

#### F-7 (major) · AC19 · `--faint`/`--muted` small text and the light link colour over `#bg-canvas` — **CLOSED at 26 of 27 call sites; the residual is re-issued as F-8**

Unit 29 replaced my Revision-2 sampling argument with a source bound: both composite formulas are
monotone in each layer's alpha, so the extreme sits at a corner of the layer cube, and all 2⁸
corners were enumerated exactly. **I re-derived the ceiling myself** (`--faint` 1.83/2.58,
`--muted` 2.25 dark, `#544019` 4.56 light) and reproduce his figures to ±0.01. He also
**correctly overruled the `#6b5122` that Matisse and I both specified** — it measures 3.43 as
small text and was only ever a large-text gradient stop. He found two sites no reviewer named
(`.daily-detail b`, light `a:hover{color:#fff}` at 1.07:1). Twenty-six selectors re-pointed and
verified by me in the file. **The class is closed; one call site was never in any route the
enumeration walked, and that is F-8.**

#### V-F3 (major, Vermeer) · AC19 · the `.hero` cover fails at rest — **CLOSED, verified by me**

Reported as an artist-hero defect; it was a `.hero` defect on **four** route families
(`hero()` at `js/app.js:833`, called from `:1826, :2042, :2099, :2158`) — I confirmed the four
call sites in source. Unit 30a moved the veil onto the text block, the third instance of one
geometry: 831 of 1,956 in-hero measurements below floor → **0**, four cells, 16 subjects. **I
re-derived the bound rather than accepting the sweep** (R3.2.3) — and because the veil is
anchored to the text block it is a bound over *any* cover pixel, not a sample of 12 painters, so
the "artists beyond the 12" limit does not weaken it. The painter's own name goes 2.40/2.35 →
8.80/10.21. `#/artwork/*` was shown by measurement not to share the defect (it does not call
`hero()`; I confirmed at `js/app.js:1948`). **Closed.**

### MINOR — 2 open

#### F-1 (minor, open) · pre-existing horizontal overflow at 821–1100 px on `#/`
Unchanged, re-verified at HEAD. Outside AC18's frozen viewport set (**A1**). Schedule it.

#### F-2 (minor, open) · AC17 · the last nav destination's focus indicator is faded by the mask, ≤820 px
Unchanged, re-verified at HEAD. Focus degraded, not absent. Suggested one-line remedy stands.

### NOTES

#### N-6 (note, **new**) · dark `--gold2` sits at 4.31 against the absolute ALL ceiling
My enumerator run scores dark `--gold2` `#e8c98a` at **4.31** against a 4.5 floor on every route,
reproducing Dürer's 4.30. This is **disclosed and argued** (D-29-7): it clears the 84-draw model
at 8.52, the REAL ceiling at 5.33, and pixel measurement at 5.85/6.00, and the ALL corner
requires all five blob centres *and* all three ribbon cores coincident on one pixel — which the
ribbon geometry makes unreachable (bases `.18/.46/.74` of `H`, amplitude ≤`.168`). Lifting it
means moving toward white, which deletes the gold. **Not a blocker**; recorded so the margin is
visible to whoever next changes the canvas, and so the ALL/REAL distinction is not quietly lost.

#### N-1 (note, open) · the screenshot pack is behind the code a third time
See **A15**. Not a blocker. Capture once, after the last production commit; make the ordering a
condition on the Human Review Package.

#### N-8 (note, **new**) · Matisse's visual review of the underline has not happened
Unit 30b applied his ruling verbatim, including `currentColor` at rest (he measured `var(--line)`
at 1.16:1 against the derived ceiling — a real measurement, not a preference). He asked for
captures of `#/credits`, `#/privacy` and `#/404` at both viewports in both themes before the rule
is considered settled. That review is outstanding. It is a visual-direction item, not a contrast
one, and it does not block: I verified in the browser that the rule's two `:not()` exclusions hold
(254 `.img-credit a` and the light hero `.footer-note a` keep their existing treatment), so no
previously certified surface is disturbed.

#### N-3, N-4, N-5, F-6, N-2 — see A15 and the criteria table
N-4 **closed** (verified). N-5 substantially discharged, its residue is **A13**. N-2 substantially
closed by Matisse's D-29-6 ruling. N-3 and F-6 unchanged.

## R3.7 — REGRESSION SWEEP AT HEAD

- **Validator:** clean, zero warnings, all references valid — identical to R1 and R2.
- **26 routes at HEAD** (`browser-evidence-final.md` §6): 26/26 reached, **0** console errors,
  **0** warnings, **0** requests ≥400 of 107, **680** images with **0** broken,
  `upload.wikimedia.org` the only third-party host, **0** Google Fonts. That sweep predates units
  30a–30c, which are CSS-only (`git show --stat`: `css/styles.css` + `index.html` only, `js/app.js`
  untouched, its `?v=` unchanged). Carried forward on that reasoning, stated so it is auditable.
- **My own runs add coverage the sweep did not have:** 18 route strings never previously
  enumerated, both themes, plus 8 pixel-measured route-loads on `#/era/*`. Zero console-visible
  failures; zero below-floor classes other than `.tl-year`.
- **No token regression.** `--hero-text-veil` is shared by the four `hero()` families and
  `.era-tile`; `--hero-veil` (26a) and `--mu-veil` (27) are unmodified — I verified the token
  values and the consuming selectors in the file. Unit 30's post-30c re-measurement shows all
  three veil families undisturbed, and Vermeer's independent museum-band figures agree with
  Dürer's to ≤0.08.
- **Contrast moved in one direction only.** Every change in units 29 and 30 lifts ink a rung or
  adds opacity. F-8 is a pre-existing condition newly measured, not a new defect: no element
  measures worse at HEAD than at `4fc8239`.

No regression found.

## R3.8 — PRESSURE, AND HOW I MADE THIS CALL

None was applied. I was told plainly that manufacturing a blocker to avoid the discomfort of
certifying would itself be a failure, and I agree with that. So I record the shape of the
decision.

I did not go looking for a way to block. I went looking for whether the host-census argument
holds, because that is what I was asked to test and because it was the one load-bearing claim
in unit 30 that rested on inference rather than measurement. The test was to run the
implementer's own enumerator on the routes his sweep did not walk. If it had come back clean —
and 17 of the 18 route strings did — I would have certified, and I had drafted no alternative.

It came back with one element, and then the pixel instrument confirmed it in both themes at
both viewports over eight route-loads. I then found that the build record does not merely omit
it: it affirmatively declares it shielded. That is the single most consequential thing in this
review, because a mis-cleared selector is more durable than an unmeasured one — the next author
reads "all inside opaque panels" and stops.

**What I certify without reservation:** unit 29 is the best piece of work in this task and it
corrected my own specified remedy on measured grounds; unit 30's V-F3 closure is a bound I
reproduced myself and it is wider and better-founded than the finding that prompted it; both
out-of-brief fixes were correct; the instruments, having been broken twice and repaired at
source both times, now reproduce my independent arithmetic to ±0.01 and found this finding the
moment they were aimed at new ground.

**What blocks is one CSS declaration.** `.tl-year` → `--body-ink`. What must accompany it is not
optional: the two false clearances corrected in the record, the five sibling sites re-checked by
measurement rather than by the same reading that failed here, and the ink enumeration re-run over
the four `hero()` route families by someone other than its implementer.

Thirty units earn no presumption, and they receive none. But it would be dishonest not to say
that twenty-eight of twenty-nine criteria pass, that two of my three original blocking findings
were closed by work I verified from first principles, that I retracted one finding of my own and
had another of my own remedies correctly overruled — and that the twenty-ninth is one declaration
away.

---

# REVISION 2 (2026-07-28) — SUPERSEDED BY REVISION 3

*Preserved verbatim. Its verdict is superseded; its findings and adjudications A7–A12 remain the
record of what was blocked and why. Where Revision 3 changes a status, R3.5 and R3.6 say so
explicitly.*

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

# VERDICT — REVISION 2 (2026-07-28, tree `1a41cff`) — SUPERSEDED BY REVISION 3

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

*(Revision 2's verdict line read `GATE 2: BLOCKED`, `OPEN CRITICAL: 0`, `OPEN MAJOR: 1`.
Superseded — see the operative verdict below. F-7 is now closed at 26 of its 27 call sites;
the residual is re-issued as F-8, and the `#6b5122` remedy specified above was correctly
overruled by unit 29 on measured grounds.)*

---

# VERDICT — REVISION 3 (2026-07-29, tree `11e4471`) — SUPERSEDED BY REVISION 4

Twenty-eight of twenty-nine criteria pass. The work since Revision 2 is the strongest in this
task: unit 29 replaced my sampling argument with a source bound I re-derived myself and could
not fault — and overruled the `#6b5122` remedy that Matisse and I both specified, correctly, on
measurement. Unit 30 closed Vermeer's hero finding on **four** route families rather than the
one reported, bounded against a worst-case opaque cover pixel rather than sampled, fixed a
WCAG 1.4.11 failure its own fix had created, and replaced accident-driven discovery with a
complete enumeration of all twenty `canvasTag` call sites. Two harness defects were found by
their own operators, corrected at source, and their effect on prior conclusions re-analysed
rather than asserted. I reproduced ten of the published figures to ±0.01.

AC19 still fails, on one element, for the reason I was asked to test.

Dürer bounded his claim honestly — *"a host census, not a route census"* — and reasoned that
every unwalked route renders only hosts already in his table. **That reasoning does not hold,
and I tested it rather than argued it.** AC19's unit is not the host but the (ink, size,
backdrop) triple, and an unwalked route can introduce an old ink over an old backdrop with no
new host at all. I ran his own enumerator over 18 route strings that appear in no sweep's route
list, and his own pixel instrument over `#/era/*`. `span.tl-year` — `--faint` at 11.2 px, the
era's start and end years, on all 8 `#/era/*` routes — composites over `#bg-canvas` inside a
`.timeline` that declares no background, and measures **4.06 / 4.28** light and **4.19 / 4.47**
dark against a 4.5 floor on real pixels, and **2.58 / 1.83** against unit 29's own derived
ceiling. It fails on all three of the project's instruments.

It sits in the seam between two enumerations with non-overlapping gaps: unit 29 scored every ink
but over 19 routes containing none of the four `hero()` families; unit 30 walked those families
but scoped to cover hosts with `#bg-canvas` excluded by design. And the record does not merely
omit it — `build-log-unit-29.md:342-345` and Matisse's ruling both state that the surviving
`--faint` sites, `.tl-year` named among them, are *"all inside opaque panels."* They are not. A
mis-cleared selector is more durable than an unmeasured one, because the next author reads the
clearance and stops.

**PASS 28 · FAIL 1 · UNSUPPORTED 0**

Blocking finding, tied to its criterion:

- **F-8 · AC19** — `.tl-year` (`css/styles.css:871`, `color:var(--faint)`, 11.2 px) paints over
  `#bg-canvas` on all 8 `#/era/*` routes (`js/app.js:2112-2118`; `.timeline`, `styles.css:852-855`,
  has no background). Measured by me at HEAD with `canvastext.py`: **4.06/4.28** light 1440×900
  and **4.19/4.47** dark 390×844 over 4 draws each, floor 4.5; **2.58/1.83** against the unit-29
  ALL ceiling; 3.22/3.69 against the 84-draw model. The only residual member of F-7's class.
  Remedy is one declaration — `--body-ink`, which clears at 5.01 light / 4.55 dark — and needs no
  visual-direction decision, since 26 selectors have already been re-pointed the same way. **It
  must be accompanied by:** correcting the two false clearances in the build record; re-checking
  the five sibling sites in that same sentence (`#search::placeholder`, `.sr-kicker`, `.tn-count`,
  `.tm-lab`, `.pp-card-loading`) by measurement rather than by the reading that failed here; and
  re-running the ink enumeration over the four `hero()` route families in both themes at both
  viewports, by someone other than its implementer.

Not blocking, but required before the Human Review Package: **N-1** — capture the screenshot pack
**once, after the last production commit**, and make that ordering a condition rather than a task
repeated per unit; it has now been overtaken three times, and `.era-tile` and the prose underline
appear on no shot. **N-8** — Matisse's visual review of the underline against real prose.

Open minor findings, neither blocking: **F-1** (821–1100 px overflow, outside AC18's frozen set),
**F-2** (masked focus ring on the last nav link at ≤820 px). Open notes: **N-6** (dark `--gold2`
at 4.31 against the absolute ceiling — disclosed and argued, D-29-7), **N-3**, **F-6**.

GATE 2: BLOCKED

OPEN CRITICAL: 0
OPEN MAJOR: 1

*(Revision 3's verdict line read `GATE 2: BLOCKED`, `OPEN CRITICAL: 0`, `OPEN MAJOR: 1`.
Superseded — see the operative verdict below. **F-8 is now closed**, re-verified by me in the
file, with all three of the conditions I attached to it met: the two false clearances corrected
in place rather than silently rewritten, the five sibling sites re-checked by measurement, and
the ink enumeration re-run over the `hero()` route families by someone other than its
implementer.)*

---

# OPERATIVE VERDICT — REVISION 4 (2026-08-06, tree `06ab20f`)

**All twenty-nine criteria pass.** AC19 passes for the first time in this task, after I blocked
it in three consecutive revisions. AC15 passes for the first time on the evidence it actually
names — a tested assistive-technology setup — rather than on DOM inference with a caveat
attached. Every finding I have ever blocked on is closed, and I re-verified each in the file
rather than accepting its closure: F-7's class at all 27 call sites, F-8's declaration and both
of the false clearances that had wrongly cleared it, and F-1's overflow at all eight widths.

The three owner-operated VoiceOver sessions did what no instrument in this project could. They
found that the Taste deck asked a blind visitor to Admire or Pass on sixteen artworks and never
said which artwork — the core product loop, unusable by ear, invisible to thirty-one units of
DOM and pixel work. Six of the seven defects they found are confirmed repaired by ear. I cannot
reproduce that evidence and I have not tried to; I have ruled on whether it satisfies AC15 as
frozen, and it does, with its boundaries recorded as residual risk rather than smoothed away —
one operator, one screen reader, one browser, one theme, and an engine gap that no further
measurement can close.

I re-derived the load-bearing contrast rule from the committed CSS and reproduce all six of its
figures to ±0.01. I regenerated the asset inventory at HEAD and it is byte-identical to the
committed copy. I verified in the coordinator's own callers that no path reaches
`human_review_ready` without passing this gate. The evidence base is trustworthy enough to
certify against — a sentence I would not have written at Revision 2.

**And the first check I was asked to run came back red at the SHA I am asked to certify.**

`python3 -m unittest discover -s tests` at `06ab20f`: `Ran 46 tests … FAILED (failures=1)`. The
record states the suite is green. It is green at the last production commit `4266804` and was
broken two commits later — by the independent certification-evidence commit itself, in the OD-5
guard, the one mechanism protecting the owner's own decision. Nobody re-ran the suite after it.

That is the fifth time in this build an instrument has reported truthfully about a smaller
universe than the claim it was used to support: contrast measured only flat paint; the arrow fix
covered only JS-emitted glyphs; a zoom matrix that said 26 covered 25; sixteen blank screenshots
passed their own theme and viewport assertions; and now "46 tests, all passing" is a true
statement about a different commit than the one being certified. The first four were caught. This
one entered through the artefact built to be the independent check.

No user is affected. The product tree is green. The remedy is one comment marker and one pinned
integer. I have weighed at length whether that should stop ninety-six commits and three human
sessions, and it should — not because the string matters, but because certifying past it would
rule that nobody needs to run the suite at the SHA they certify, and would leave a guard
permanently red, which is the same as not having it. Blocking costs one short round. Certifying
costs the meaning of the gate.

**PASS 29 · FAIL 0 · UNSUPPORTED 0**

Blocking finding, tied to its criterion:

- **F-9 · no frozen criterion; theory's requested action A7 and acceptance criteria 1 and 3** —
  the repository test suite fails at HEAD.
  `TestProseLanguage.test_no_artifact_of_ours_asserts_a_legal_conclusion` fires on
  `protocol/tasks/PIG-001/evidence/harness/vermeer-cert/gapfill.py:28`
  (`OLD_LEDE = "Most reproductions here are public domain."`). Bisected by me in clean
  worktrees: green at `95e5636`, green at `4266804` (last production commit), green at
  `09f61a8`, **red at `a71e2c5`**, red at HEAD. **Remedy:** append `# OD5-EXEMPT` to that line
  and pin it in `EXPECTED_EXEMPTIONS`, or reword the constant. **The condition that matters more
  than the fix:** re-run the suite at the final SHA, *after* the last evidence commit, and bind
  its output to that SHA — this failure exists only because the suite was run at the commit that
  fixed it and never again.

Open major, **not blocking Gate 2 — a condition on the merge**: **F-10** (A20, R4.1.7) — the
quality gate greps an append-only review for verdict strings and cannot distinguish an operative
verdict from an archived one. **This is demonstrated, not inferred: the gate passed this very
report while its verdict was `GATE 2: BLOCKED` with two open majors**, because three sentences
describing the defect contained the strings it greps for. I broke them with zero-width characters
and confirmed the gate now blocks; the state committed here is correct. Its screenshot check also
accepts any non-zero PNG with the right filename — the same failure as the 16 blank screenshots.
And `pigment_coordinator/` is a change to the neutral arbiter, made by the pole it governs and
disclosed late, that **must be excluded from the product merge set and proposed separately**.
**Whoever consumes this verdict must read the operative block, not grep the file** — and until
the scan is fixed, the quality gate should be treated as advisory rather than binding.

Open minors, none blocking: **F-2** (masked focus ring, ≤820 px — requested by theory, still not
corrected), **F-11** (the AT-5 SEO carve-out is 695 files in four families, not "~100" in one),
**V-M1** (`.md-name` at 2.34 px, legibility not contrast), **AT-5** (fixed in the DOM, still
unconfirmed by ear — do not close it on a DOM sweep). Open notes: **N-6**, **N-3**, **F-6**, and
the engine gap — every pixel measurement is Chrome, every ear confirmation is Safari, and no
single engine has both.

**N-1 and N-8 are closed.** The screenshot pack post-dates the last production commit, and
Matisse ruled PASS WITH NOTE while stating plainly that the hover thickening is held on defence
rather than observation.

When F-9 is closed and the suite is re-run and bound to the final SHA, I expect to certify.

GATE 2: BLOCKED

OPEN CRITICAL: 0
OPEN MAJOR: 2
