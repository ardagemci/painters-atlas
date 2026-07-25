# PIG-001 — Deck-Warning Editorial Merit Review (AC3, OD-4, unit 22)

**Author:** Seurat (`claude-data-steward`), Data and Copyright Steward
**Date:** 2026-07-25
**Branch:** `pig-001-stabilization`
**Governing constraint:** **OD-4** — honest editorial re-scores are authorised
*where merit supports them*; **taste coordinates are never tuned merely to
silence a validator.** Absent editorial justification, a dated owner exception
is requested instead.

**Outcome: two coordinate corrections made on the merits, one candidate
refused. Both validator warnings are cleared as a consequence, not as a
goal. No owner exception is required.**

---

## The standard I held myself to

OD-4 makes this a judgement about the *work*, not about the validator. So the
test for each candidate was a single question, asked before looking at whether
the answer would clear anything:

> **Does the current coordinate misdescribe the work?**

A re-score is honest only if the answer is yes for reasons that would stand if
no warning existed. Two tie-breakers were used where the axis reading was close:

1. **Internal consistency** — does the coordinate make sense against comparable
   works already scored in the corpus? (`docs/TASTE_MATH.md` §1.2 makes the
   corpus relational: artworks inherit from artists, artists from movements, and
   per-work overrides exist precisely to record where a work departs from its
   neighbours.)
2. **Agreement with Pigment's own editorial copy** — where a record's
   `description` already characterises the work, a coordinate that contradicts
   it is evidence of a scoring error, not of a bold reading.

A change that lands *exactly* on a validator threshold was treated as a red
flag, not a success.

---

## The two warnings

From `tools/validate.jxa.js:209-214`, over the deck pool (`POOL` =
75 Tier 1 catalog works with a PD image):

```
deck pool: <2 works with E<=-40
deck pool: empty F×D quadrant 1,-1
```

- **Warning 1** — the `E` axis (−100 Classical … +100 Experimental) had exactly
  **one** work at or below −40: `the-trinity` (Rublev) at E = −40.
- **Warning 2** — the F×D quadrant requiring `F ≥ +25` **and** `D ≤ −25`
  (Abstract *and* Calm) was **empty**. Occupancy was F−D+ 35, F−D− 14, F+D+ 1,
  **F+D− 0**.

---

## Candidate 1 — ACCEPTED: `sistine-madonna`, E −30 → −55

**Raphael, *Sistine Madonna* (1512), `js/catalog-3.js:532`.**

Round 1 proposed "a Vermeer/Rembrandt E −35→−40". I examined those first and
**rejected both** (below). Raphael is the correction the axis actually needs.

**Does E = −30 misdescribe the work?** Yes, and the evidence is internal.
At E = −30 the *Sistine Madonna* sat at **exactly the same experimental
distance from the classical pole as Caravaggio's *Calling of Saint Matthew***
(E = −30), with Caravaggio's *Beheading of Saint John* and *David with the Head
of Goliath* scored as *more* classical still (E = −25).

That ordering is indefensible. Caravaggio was the disruptive radical of his
generation — a painter whose naturalism and lighting were contested in his own
lifetime and who redirected European painting. Raphael is the painter whose name
*became* the definition of academic classicism for the four centuries after him;
the European academies taught him as the standard against which deviation was
measured. Having them occupy the same point on a Classical–Experimental axis
says the axis is not measuring what it claims to measure.

The *Sistine Madonna* itself is a supremely canonical devotional composition:
pyramidal, symmetrical, idealised, a Madonna and Child flanked by saints. It is
the type specimen of the High Renaissance solution, not a departure from it.

**Per-axis justification:**

| Axis | Before | After | Reasoning |
| --- | --- | --- | --- |
| `F` Figurative↔Abstract | −85 | **−85** | unchanged; correctly deep-figurative |
| `D` Calm↔Dramatic | −15 | **−15** | unchanged; the parted-curtain device is theatrical but the composition is serene |
| `E` Classical↔Experimental | −30 | **−55** | **corrected.** Raphael is the source of the Western classical standard; −30 placed him level with Caravaggio, the radical of the following generation |
| `C` Sensual↔Conceptual | −25 | **−25** | unchanged |
| `M` Intimate↔Monumental | 50 | **50** | unchanged; 265 × 196 cm altarpiece |

**Honesty check.** −55 is not the minimum value that clears the warning; −40
would have sufficed. −55 was chosen because it is where the work belongs
relative to Rublev's icon (−40) and Caravaggio (−30), not because of the
threshold. Had the threshold been −60, I would still have written −55.

---

## Candidate 2 — ACCEPTED: `composition-viii`, D −20 → −40

**Kandinsky, *Composition VIII* (1923), `js/catalog-1.js:1050`.**

**Does D = −20 misdescribe the work?** Yes — and unusually, Pigment's own
editorial copy is the witness. The record's `description` reads:

> "Ten years after the apocalyptic Composition VII, Kandinsky answered himself:
> where VII boils, **VIII is engineered** — circles, wedges and grids on a **cool
> ground**, painted in his first Bauhaus year."

The corpus scores *Composition VII* at **D = +80**. The editorial text presents
VIII explicitly as the cool, engineered counterweight to VII's boil — and then
the coordinate places it at D = −20, only mildly calm. The description and the
data disagree, which is exactly the "implementation and documentation disagree"
case CLAUDE.md §6 says to surface rather than quietly pick a side.

*Composition VIII* is Kandinsky's Bauhaus-period turn to geometry: floating
circles, precise wedges, straight-edged grids on a pale ground, with none of the
turbulence or apocalyptic massing of the 1913 *Composition VII*. `D = −40` puts
it in the same calm register as `the-arnolfini-portrait` (−40) and `red-fuji`
(−40) — measured, still, non-narrative works — while leaving VII untouched at
+80. The contrast the two paintings actually present is then legible in the data.

**Per-axis justification:**

| Axis | Before | After | Reasoning |
| --- | --- | --- | --- |
| `F` Figurative↔Abstract | 90 | **90** | unchanged; fully non-objective |
| `D` Calm↔Dramatic | −20 | **−40** | **corrected.** Geometric, weightless, non-narrative; the record's own copy calls it "engineered" on a "cool ground" against VII's "boil" |
| `E` Classical↔Experimental | 75 | **75** | unchanged |
| `C` Sensual↔Conceptual | 35 | **35** | unchanged; Bauhaus theory-driven but still colour-led |
| `M` Intimate↔Monumental | 10 | **10** | unchanged; 140 × 201 cm |

**Honesty check.** The quadrant needs `D ≤ −25`. −40 overshoots it by 15 points
because −40 is the honest reading against the corpus's other calm works, not
because −25 would have been too obviously minimal. This is the change I would
defend if the quadrant rule were deleted tomorrow.

---

## Candidate 3 — REFUSED: `black-square`, D −20 → −25

**Malevich, *Black Square* (1915).** This was round 1's headline suggestion. I
am declining it, and the reason matters more than the decision.

**It is a five-point move that lands exactly on the threshold.** The quadrant
test is `D ≤ −25`. The proposal is `−20 → −25`. That is not a re-reading of the
painting; it is the smallest possible edit that changes a validator's output,
which is the precise behaviour OD-4 forbids and the specification's disposition 9
names ("coordinates are taste data and are never tuned to silence a validator").
Had I made it, the resulting register would have been a record of gaming, and
the fact that it *would* have worked is what makes it dangerous rather than
harmless.

**On the merits, the coordinate is contestable rather than wrong.** There is a
real case that *Black Square* is radically calm — no gesture, no narrative, no
modelling, absolute stillness. There is an equally real case that it is
confrontational: it was hung in the icon corner of the 0,10 exhibition and
declared the "zero of form", and many viewers experience it as an act of
negation rather than repose. When a coordinate is genuinely arguable in both
directions, "the current value misdescribes the work" is not established, and
OD-4's bar is not met.

*Composition VIII* cleared that bar and *Black Square* did not, which is why one
was changed and the other was not. If the owner later wants *Black Square*
re-read as deeply calm — a defensible editorial position — that should be a
deliberate taste decision on its own terms, recorded as such, and not smuggled in
as a warning fix.

---

## Also examined and rejected

| Candidate | Proposed | Verdict |
| --- | --- | --- |
| `the-return-of-the-prodigal-son` (Rembrandt), E −35 → −40 | round 1 | **Rejected.** Moving late Rembrandt *toward* the classical pole is backwards. The late works are famously rough, loose and unfinished-looking, and were criticised as such in his own time. If anything E = −35 is already too classical. |
| `girl-with-a-pearl-earring` (Vermeer), E −35 → −40 | round 1 | **Rejected.** A *tronie*, not a portrait, by a painter whose optical technique (pointillé highlights, camera-obscura effects) was materially innovative. −35 is defensible; −40 is less true, not more. |
| `view-of-delft` (Vermeer), E −30 | considered | **Rejected**, same reasoning. |
| `the-trinity` (Rublev), E −40 → −65 | mine | **Not made.** I think −40 understates how canon-bound icon painting is, and −65 is arguably truer. But it changes no warning, I hold it with lower confidence than the two above, and PIG-001 is a bounded stabilisation. **Recorded as a recommendation** for the taste-math objective OD-4 flags as future work. |
| `the-ten-largest-no-7` (af Klint), D −15 | considered | **Rejected.** The *Ten Largest* are large, soft and floating, but also swirling and energetic; −15 is within a defensible range. |

---

## Result

Validator, unedited, after both edits:

```
app.js: syntax OK
artists: 247, movements: 75, techniques: 39, eras: 8, nations: 37, painter styles: 27, influence edges: 225, venues: 115, catalog: 317 (tier1: 75), daily pool: 75, museum notes: 103, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```

**No warnings.** Both deck-pool warnings are gone:

- `E <= -40` now has **2** works — `the-trinity` (−40) and `sistine-madonna` (−55).
- F×D quadrant `1,-1` now has **1** work — `composition-viii` (F 90, D −40).

Counts are unchanged (247/75/317/75), all references valid, and no id, slug or
schema was touched. Two integers changed in two files.

**AC3 disposition:** satisfied by editorially justified correction, not by owner
exception. **No dated owner exception is requested.** If a reviewer disagrees
with either re-score on the merits, the correct remedy is to revert that integer
and request the exception — the warning returning is the intended, honest
consequence, and both edits are independently reversible.

---

## Files changed

| File | Line | Change |
| --- | --- | --- |
| `js/catalog-3.js` | 532 | `sistine-madonna` `coords.E` −30 → −55 |
| `js/catalog-1.js` | 1050 | `composition-viii` `coords.D` −20 → −40 |

`coordsSource:"override"` was already set on both records, so both remain
correctly marked as hand-scored per `docs/TASTE_MATH.md` §1.2.

---

## Recommendation beyond this task

Two of the 75 deck-pool works carried coordinates that misdescribed them, and
one of those contradicted its own record's editorial copy. That rate suggests
the coordinate corpus has never been reviewed against the descriptions written
alongside it. OD-4 already elevates taste mathematics to a candidate flagship
and calls for a dedicated future objective; **a systematic description-versus-
coordinate consistency pass belongs in that objective's scope.** It is out of
scope here and I have not started it.
