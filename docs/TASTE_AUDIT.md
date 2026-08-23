# The taste coordinates — a measurement pass

*2026-08-22. Backlog **E4**, whose instruction was explicit: "the first job is
measurement, not revolution — audit the coordinates, test discrimination by
simulation, and only then consider new frameworks." This is that audit. It
proposes no new framework and changes no score.*

Axes are `ADMIRE_SPEC` §3: **F** figurative↔abstract, **D** calm↔dramatic,
**E** classical↔experimental, **C** sensual↔conceptual, **M** intimate↔monumental.

---

## 1. Coverage

| | count |
| --- | --- |
| catalog records | 350 |
| carrying explicit coordinates | **168** (48%) |
| Tier 1 | 75 |
| **deck pool** — Tier 1 **and** coords **and** a public-domain image | **75** |

The backlog recorded "141 of 323". The comparable figure today is 168 of 350;
the proportion has barely moved.

## 2. The headline finding: F is one-sided, and curation cannot fix it

Of the 75 works the onboarding deck can draw on, **70 are on the figurative side
of F. Five are not.** The deck's own §6.2 quota asks for three works at `F ≥ 30`
and the pool contains exactly five.

The cause is not that nobody scored abstraction. **35 works are scored `F ≥ 0`.
Twenty-nine of them are in copyright and cannot be shown.**

| | abstract half (F≥0) | figurative half (F<0) |
| --- | --- | --- |
| works scored | 35 | 133 |
| public domain | **6** | 94 |
| Tier 1 *and* PD → usable by the deck | **5** | 70 |
| median year | **1950** | 1882 |

**The public-domain cutoff and the abstract turn in painting are the same
historical event.** Pigment can only show work whose maker died by about 1955;
abstraction is overwhelmingly later. So the deck can ask "how figurative?" and
can barely ask "how abstract?", and no amount of cataloguing changes that. Every
past instance of "the deck pool is thin at F+" was a symptom of this, which is
why filling it never worked.

## 3. F is bimodal — it behaves like a flag, not a dimension

Distribution of F across all 168 scored works:

```
-100..-75  ############################# 59
 -75..-50  ###################           39
 -50..-25  ############                  25
 -25..  0  #####                         10
   0.. 25  ##                             4
  25.. 50  #                              3
  50.. 75  #                              3
  75..100  ############                   25
```

**Thirty-eight works sit in the whole middle third of the axis; 84 sit at one
extreme.** A user placed at F −40 is being positioned in a region the atlas
barely occupies. This is a property of painting as much as of the atlas — pictures
tend to be representational or not — but it means F is closer to a **binary
signal** than to the continuous dimension the taste maths treats it as.

## 4. F and E are not independent, and the overlap is a scoring habit

| pair | r |
| --- | --- |
| **F–E** | **+0.64** (deck pool) · **+0.60** (all 168) |
| E–C | +0.38 |
| F–C | +0.32 |
| D–M | +0.32 |
| everything else | < 0.3 |

The obvious explanation — that the abstract cluster drags both together — is
**wrong**, and testing it is what makes this worth recording:

- within the **figurative half alone** (n=133): **r = +0.68**, *higher*
- within the **abstract half alone** (n=35): **r = −0.08**

So the correlation lives entirely among figurative pictures: the more a
figurative work leans away from straight representation, the more experimental
it gets scored. That is a habit of the scorer, not a fact about the corpus, and
it is the one thing here that **rescoring could actually fix**.

## 5. E is scored relative to its moment, not absolutely

| period | n | mean E | negative |
| --- | --- | --- | --- |
| before 1500 | 13 | **+18.5** | 4/13 |
| 1500–1699 | 31 | −4.0 | 19/31 |
| 1700–1799 | 4 | +1.2 | 2/4 |
| 1800–1899 | 39 | +36.5 | 5/39 |
| 1900+ | 81 | **+63.4** | **1/81** |

E rises almost monotonically with date. The overall positive mean (+39.8) is
therefore mostly **corpus composition** — 81 of 168 scored works are post-1900 —
rather than a broken axis, which is a softer verdict than the backlog's.

But look at the first row. Pre-1500 works average **+18.5**, and 20 of 44
pre-1700 works are scored experimental. Van Eyck's oil technique genuinely *was*
rupture in 1430 — so the axis is being read as **"innovative for its time"**,
while `ADMIRE_SPEC` §3's wording ("tradition, craft, order ↔ rupture, risk,
rule-breaking") equally permits an absolute reading. **A user who says they like
"classical" cannot know which question they answered.** That ambiguity is in the
specification, not in the scores.

## 6. The healthy axes

Over the deck pool, **D, C and M are close to balanced** — the only three that
discriminate in both directions:

| axis | mean | sd | negative |
| --- | --- | --- | --- |
| D | +19.3 | 45.7 | 27/75 |
| C | −2.3 | 35.1 | 35/75 |
| M | +2.6 | 50.5 | 38/75 |
| E | +24.9 | 38.0 | 23/75 |
| **F** | **−60.6** | 44.1 | **70/75** |

## 7. The deck's opening rests on single works

Stage 1 of `buildDeck` picks one anchor per F×D quadrant, preferring |F|,|D| ≥ 50:

| quadrant | candidates |
| --- | --- |
| F−D+ | 19 |
| F−D− | 2 |
| **F+D+** | **1** |
| **F+D−** | **1** (and only at the relaxed ≥25 threshold; nothing at 50) |

**Two of the four quadrants that define the taste map are held up by one picture
each.** Remove, retitle or lose the image on either and that quadrant silently
degrades to a weaker threshold with no warning. Nothing in the validator watches
this.

## 8. What this says about next steps

Not proposals — findings, in the order they should be argued about.

1. **F cannot be balanced.** Accept it and say so, or reduce F's weight in the
   engine, or narrow what F claims to measure. Filling the catalog will not help.
2. **The F–E overlap is fixable** and is the only genuine scoring defect here.
   Rescoring E on figurative works, independent of how abstract they are, is a
   bounded job over 133 records.
3. **`ADMIRE_SPEC` §3 should say whether E is absolute or relative to period.**
   Until it does, the axis means two things.
4. **Guard the quadrant anchors.** A validator rule that fails when any F×D
   quadrant drops below two qualifying works would have caught this before it
   became load-bearing.
5. Coordinate coverage is **48%**. Every uncoordinated Tier 1 record is invisible
   to the deck.
