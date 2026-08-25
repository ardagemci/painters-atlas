# The influence graph, measured

*2026-08-24. Backlog **E2**. A measurement pass and one guard, in the shape of
`docs/TASTE_AUDIT.md`: the point is to find out what is true, not to propose a
programme. Nothing here is a rights determination or a legal claim (OD-5); a
source records where a relationship is **attested**, never that this project has
verified it.*

---

## 1. The claim the file was making

`js/influences.js` opened with one sentence of self-description:

> Every relationship is grounded in the artist bios elsewhere in the atlas.

That is a **checkable** claim, and nobody had checked it. This pass did.

**It was false for 107 of 246 edges — 43%.**

| | edges |
| --- | --- |
| attested — one endpoint's prose names the other painter | 139 |
| **not attested anywhere in the atlas's prose** | **107** |

By type, the unattested edges are `influenced` 71, `befriended` 29, `rivaled` 5,
`taught` 2. Teaching survives almost intact, which makes sense: a teacher is a
biographical fact and the bios say so. Influence is the soft one.

**The edges are not wrong.** Caravaggio did shape Velázquez and Rembrandt; Giotto
did shape Masaccio. What was wrong was the sentence claiming the atlas said so.
Three spot-checks, read in full rather than grepped:

- **Velázquez's** record names Manet, Whistler, Bacon and Picasso. It does not
  name Caravaggio or Titian. The graph carries both.
- **Rembrandt's** record names neither Caravaggio nor Titian. The graph carries
  both.
- **Masaccio's** record names Michelangelo, Leonardo, Raphael, Vasari,
  Brunelleschi, Donatello and Torrigiano. It does not name Giotto. The graph
  carries `giotto → masaccio`.

## 2. How the measure was built, and the two times it was wrong first

The measure is: **does either endpoint's own prose name the other painter?** —
over `tagline`, `life`, `career`, `outside` and `facts`, accent-folded.

It took three attempts, and the failures are worth keeping because they are the
same failure in two directions.

1. **Surname-only matching gave 117 unattested.** It extracted the *last* long
   token of a name, so Leonardo da Vinci reduced to "vinci" and every bio that
   says "Leonardo" was scored as silent. **False negatives.**
2. **All-tokens matching gave 103.** Now "David" matched Jacques-Louis David,
   Caspar David Friedrich and David Hockney; "Still" matched the ordinary
   English word. **False positives**, which *understate* the problem — the
   dangerous direction.
3. **Word-boundary matching with given names and common words removed gives
   107**, and it reports the one painter left with no distinctive token at all
   rather than silently failing on him.

The final matcher is deliberately biased: a false negative asks for a source
string, which is a safe way to be wrong. A false positive would let an
ungrounded edge pass as grounded, which is not.

**A fourth measure was attempted and thrown away.** The inverse question — which
relationships does the prose attest that the graph does *not* carry? — returned
517 pairs across 215 artists, and inspection showed it was mostly the
false-positive problem again at scale. It is not reported as a finding, because
reporting it would be the exact error this repository keeps catching: a proxy
standing in for the thing. Three instances of the inverse gap were found by hand
instead, and fixed (§3).

## 3. What shipped

**The schema gained an optional fourth element.** An edge is now
`[from, to, type]` or `[from, to, type, source]`. Every consumer in `js/app.js`
destructures `[f, t, ty]` positionally, so the addition is invisible to all four
of them and to the prerenderer.

**An edge is GROUNDED if either endpoint's prose names the other, or it carries
a source string of at least 20 characters.** `tools/validate.jxa.js` computes
this on every run, prints `(ungrounded: N, sourced: M)` in its summary line, and
**fails if N rises above a recorded ceiling of 107.**

A ratchet rather than a pass/fail, deliberately. 107 ungrounded edges exist;
failing the build on them would block every unrelated change until a research
project finishes, which is how a guard gets deleted. What the ceiling stops is
the thing that costs something — **a new edge asserted with nothing behind it.**
The number can only fall.

Two further rules are hard errors, because a bad source is worse than none: a
source that is not a string, and a source under 20 characters.

**Proved non-vacuous four ways**, each by breaking it: a new ungrounded edge
(`hokusai → kahlo`) produced *"108 edges … above the ceiling of 107"* and **exit
1**; an 8-character source produced *"a stub source is worse than none"*; a
numeric source produced *"source must be a string"*; and the Python measure and
the JXA implementation, written separately, agree exactly at 250 / 107 / 1.

**Prose is preferred to a source string, and the preference has a reason.** If
the relationship is in the bio, a reader learns it; if it is only in a citation,
the graph asserts something the site never tells anyone. A source string is the
honest fallback, not the goal — which is why three of the four edges added below
carry no source and did not need one.

**Three relationships the atlas already tells its readers, that the graph did not
carry.** Masaccio's own record says Michelangelo, Leonardo and Raphael "all
sketched there as students" in the Brancacci Chapel; only the Michelangelo edge
existed. Bellini's record calls Mantegna his brother-in-law and "a lifelong
argument to paint against", and Mantegna's record names Bellini back. Added:
`masaccio → leonardo-da-vinci`, `masaccio → raphael`,
`andrea-mantegna → giovanni-bellini`. All three are grounded by prose already
written — they cost nothing but noticing.

## 4. The cross-tradition gap — measured, and mostly not this file's problem

The backlog says **"not one edge connects two different non-Western
traditions"**. Confirmed, on a clean definition: over the 246 edges, taking the
13 non-Western nations in the atlas, the count of edges whose two endpoints sit
in two *different* non-Western nations was **zero**. (An earlier, cruder scan had
suggested two; those were Ukraine→Belarus and Armenia→Ukraine, which the
national split now files as European.)

**One edge closes, and it is a real one.**
`tsuguharu-foujita ↔ diego-rivera` (**befriended**, japan ↔ mexico): Foujita
visited Rivera's studio soon after reaching Paris in 1913; Rivera painted him in
*Portrait of Mr Kawashima and Foujita* (1914); and Foujita's seven-month Mexican
stay from November 1932 was drawn by the mural movement *"led by Diego Rivera,
whom he had befriended in Paris"*. Sourced on the edge.

**The rest of the gap is downstream of E3, not of this file**, and that is the
finding worth carrying forward. The named cases cannot be drawn because the
endpoints do not exist:

| the backlog asks for | the atlas holds |
| --- | --- |
| China → Korea | 5 Chinese painters, 2 Korean, and no documented painter-to-painter link between any pair of them |
| Persia → Ottoman | **one** Iranian painter (Reza Abbasi, 1565–1635) — later than Nakkaş Osman, so the obvious edge runs the wrong way |
| Persia → Mughal | **no Mughal painter at all** |

Two candidates were researched and **rejected on evidence**, which is recorded
because a rejected candidate is a result:

- **Wifredo Lam ↔ Kahlo / Rivera** (cuba ↔ mexico). The claim appears in the
  *lead* of Lam's Wikipedia article and is not carried in the body, and the
  sources disagree on the year of the Mexico visit — 1938 in one, 1942 in
  another. Lead-only, date-unstable: below the bar.
- **Botero ↔ the Mexican muralists** (colombia ↔ mexico). Nothing found to
  support it.

**Sesshū Tōyō travelled to Ming China in 1468–69 and Zhang Daqian studied in
Kyoto** — both real, both un-drawable, because the graph joins *painters* and
neither man's Chinese or Japanese counterpart is in the roster. Drawing
`shen-zhou → sesshu-toyo` because they were contemporaries would be inventing an
acquaintance. The gap is a roster gap wearing a graph's clothes.

## 5. What is left

1. **107 ungrounded edges.** The ceiling holds them; lowering it is the work.
   The preferred route for each is **a sentence in a bio**, not a citation —
   better content and better grounding at the same time. That is Content Editor
   work, and it is a large, genuinely useful commission rather than a chore.
2. **Lower `INF_UNGROUNDED_CEILING`** in `tools/validate.jxa.js` every time the
   number falls. A ratchet that is never tightened is a ceiling, not a ratchet.
3. **The cross-tradition gap waits on E3.** No amount of graph work opens it.
