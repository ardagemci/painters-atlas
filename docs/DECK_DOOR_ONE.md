# §8's first door was open, and nobody walked through it

*2026-08-27. Backlog **E5**. Raised by the Curator during Batch 06 as "the honest
route to a deeper deck is door 1, an editorial list". The route was right. The
door turned out to be open already.*

---

## 1. What was actually wrong

`ARTWORK_SCHEMA` §8 is unambiguous:

> An artwork enters Tier 1 iff it belongs to at least one of:
> **1. an editorial list**, 2. the essential works of a Tier 1 artist,
> 3. the Painting-of-the-Day schedule, 4. the onboarding deck pool.

Measured before anything was written: of the **102 works appearing in the
editorial lists, 64 were still Tier 2.**

The rule was stated, normative, and **enforced by nothing.** The deck pool sat at
75 for months while the works to fill it were already written, already featured
on the site, and already carrying public-domain images. `doorways-into-abstraction`
— a featured list, on exactly the subject `TASTE_AUDIT` says the deck is starved
of — contained **four Tier 2 works with no coordinates at all.**

So E5 was never a missing list. It was a missing check.

## 2. What §8 actually means

A list member below Tier 1 is **a record nobody has finished authoring yet**, not
a corruption. §8 is a *work list* — "these are the works that should be brought up
to Tier 1" — rather than an invariant that data can violate. That reading is
consistent with §4's existing correction, which found the renderer branches on
`description`, not on `tier`.

That distinction decides the shape of the guard: a **ratchet**, not a gate.

## 3. What shipped

**Nine works promoted to Tier 1. Deck pool 75 → 84.**

**Four needed authoring** — they were in a list, public-domain, with dimensions
and a museum, and had no coordinates, no description and no notice bullets:

| work | | |
| --- | --- | --- |
| Turner, *Norham Castle, Sunrise* | c. 1845 | F +10 D −50 |
| Kandinsky, *The Blue Mountain* | 1908–09 | F +20 D +45 |
| Kandinsky, *Untitled (First Abstract Watercolor)* | 1910 dated / c. 1913 | F +90 D +40 |
| Kandinsky, *Improvisation 28 (Second Version)* | 1912 | F +75 D +70 |

Every one was **opened and looked at** before its description was written — the
cow standing in Turner's dissolved river, the yellow and red trees flanking
Kandinsky's blue mountain, the bare white paper under the first abstract sheet.

**Five needed only the flag.** Klee's *Senecio*, Mondrian's *Gray Tree*, Marc's
*The Fate of the Animals*, Carr's *Forest, British Columbia* and Léger's *The
City* were already complete to Tier 1 standard — coordinates, a 60–90 word
description, three notice bullets, tags, a public-domain image — written across
catalog batches 03–05. They were Tier 2 because nothing had ever put them in a
list.

**So a list was written**, and it is not a wrapper for the promotion. **"The Last
Recognisable Thing"** — paintings where you can still name the subject and it is
the last time you can: a tree, a head, a forest, a city, a pond. It is the mid-F
band `TASTE_AUDIT` measured as nearly empty, which is the honest editorial idea
sitting underneath the deck problem.

Turner and Kandinsky's artist records gained the three works they were missing,
so the promoted pages have their back-links and are not orphans — §8's "no
orphans, by construction" is a claim the data has to earn.

## 4. What it did to the deck, and what it could not do

| F×D quadrant | before | after |
| --- | --- | --- |
| F+D+ (abstract, dramatic) | **1** | **6** |
| F+D0 | 3 | 4 |
| **F+D− (abstract, calm)** | **1** | **1** |

**The F+D+ warning clears. The F+D− warning does not, and it cannot.**

Kandinsky's *Composition VIII* is the only work in the atlas at F ≥ 25 and
D ≤ −25, and there is no public-domain candidate to join it — calm abstraction is
Rothko, Newman, Martin and Frankenthaler, and every one of them is in copyright.
`TASTE_AUDIT`'s structural finding, narrowed to a single quadrant: **one door of
the deck rests on one painting, permanently, and no amount of authoring fixes
it.**

Norham Castle was scored **F +10**, not the F +30 that would have closed the
quadrant. The castle, the river and the cow are all nameable; the honest score
puts it outside F+. Scoring a work to satisfy a guard is the failure `TASTE_AUDIT`
opened by refusing.

## 5. The guard

`tools/validate.jxa.js` now counts editorial-list works that are below Tier 1,
prints `list works below tier 1: N/M` on every run, and **fails if N rises above
a ceiling of 60**.

A ratchet, for the same reason as the influence-grounding one: sixty such records
exist, and failing outright would block every unrelated change behind a content
commission — which is how a guard gets deleted. What the ceiling stops is the
thing that costs something: **adding a work to a list and never authoring it.**

Proved non-vacuous by demoting *Black Square* to Tier 2 — `61 editorial-list
works are still Tier 2, above the ceiling of 60`, exit 1.

## 6. What is left

1. **Sixty list works still below Tier 1**, 49 of them carrying public-domain
   images. Each needs coordinates, a 60–90 word description and three notice
   bullets. That is a real content commission and the single largest remaining
   lever on the deck.
2. **Lower `LIST_TIER2_CEILING`** whenever the number falls.
3. **F+D− is unfixable from the public domain** and should be treated as a
   product constraint, not a backlog item — the deck's opening card in that
   quadrant will be the same painting for every user, forever.
