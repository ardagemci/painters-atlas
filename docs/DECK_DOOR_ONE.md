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

## 6. The first tranche of the backlog — 60 → 47

*Same day.* Thirteen more works brought up to Tier 1. **Deck pool 84 → 96.**

**Ten were authored** — coordinates, a 60–90 word description and three notice
bullets each, and each verified against Commons before a word was written:

- **Four Vermeers**: *The Milkmaid*, *The Lacemaker*, *Woman in Blue Reading a
  Letter*, *The Concert*. Vermeer was the atlas's most underserved major painter;
  he now has five full pages.
- **Four Rembrandts**: *Danaë*, *Self-Portrait at the Age of 63*, *Self-Portrait
  with Two Circles*, *The Storm on the Sea of Galilee*.
- **Two Hokusai prints**: *The Amida Falls*, *Thunderstorm Beneath the Summit*.

**Three needed only the flag** — Rousseau's *The Dream* and *Tiger in a Tropical
Storm*, and Tarsila do Amaral's *Abaporu*, all already complete to standard.

**`match_verdict` produced a FALSE REJECTION**, the mirror of the false confirms
E3 found. *The Amida Falls* was `rejected` because its Commons file carries the
Rijksmuseum's Dutch title and an inventory number — *"De Amida waterval langs de
Kisokaido, AK-MAK-904"* — which ties to neither the English title nor the
artist's name. The file is a genuine impression of the print. Opening it settled
it in seconds. Recorded beside E3's two false confirms: the check is a filter,
not a verdict, in both directions.

**Nine back-link warnings fired and all nine were real.** Promoting a work to
Tier 1 turns on §8's back-link check, and it found that Vermeer's record listed
four works and not *The Lacemaker*, *The Concert* or *Woman in Blue*; Rembrandt's
omitted *Danaë*, *Self-Portrait at 63* and *The Storm*; Hokusai's omitted both
prints. Those artist records now list them, so the pages are reachable from the
artist page as §8 promises. **The promotions did not create the gap — they
revealed it.**

`LIST_TIER2_CEILING` lowered **60 → 47**.

## 6b. Second tranche — 47 → 35, and six lists finished

*Same day.* Twelve more, and the organising principle changed: instead of
grouping by artist, **the tranche was chosen to finish whole lists.** Twelve
works completed five of them outright.

| list | what it needed |
| --- | --- |
| `judith-one-story-many-knives` | Caravaggio, Artemisia and Klimt's three Judiths |
| `ways-of-water` | Monet's *La Grenouillère* and *Bridge over a Pond*, Turner's *Fishermen at Sea* |
| `doorways-into-abstraction` | Pollock's *Autumn Rhythm*, Rothko's *No. 14* |
| `paint-you-can-touch` | Turner's *Snow Storm*, Pollock's *Full Fathom Five* |
| `the-forest-that-stopped-shrinking` | af Klint's *Tree of Knowledge*, Klimt's *Tree of Life* |

**Six of the fifteen lists are now entirely Tier 1, up from one.** Deck pool
**96 → 105**.

**Four of the twelve are in copyright** — the two Pollocks, the Rothko, and
`abaporu` from the first tranche — and they are Tier 1 all the same, carrying
`image:{status:"copyright"}` with no `src`. **A record may be written about
without being displayable**, and the rights sample counts 105 against the
validator's 109 for exactly that reason.

**Three of the three Pollock/Rothko records already carried hand-scored
coordinates**, in `js/catalog-2.js`'s compact record shape. Those were left
alone and only `description` and `notice` were added — rescoring existing
coordinates to fit a new author's taste is not a promotion, it is a silent edit.

**`match_verdict` false-rejected twice more**, both on filename words rather than
content: Klimt's *Judith I* on `(cropped)` — the file is the complete painting
including its inscribed frame — and the Stoclet *Tree of Life* on `Part of`,
where the file is an honestly-labelled section of the full-size cartoon and the
record already says so. With *The Amida Falls*, that is **three false rejections
against E3's two false confirms.** The pattern is now clear enough to state: the
check reads filenames and titles, so it fails on foreign-language pages,
inventory numbers, and the words *cropped* and *part of* — in both directions.

`LIST_TIER2_CEILING` lowered **47 → 35**.

## 6c. Third tranche — 35 → 24, and both Actuality lists finished

Eleven more, again chosen to finish lists. **Eight of fifteen are now entirely
Tier 1.**

- **`the-king-goes-to-philadelphia`** (eight works: Cassatt ×2, Cézanne, Turner,
  Degas, Goya, Bruegel, Enwonwu) — and with `the-forest-that-stopped-shrinking`
  already done, **both Actuality lists are now complete**. The monthly ritual's
  own pages are Tier 1 the whole way down.
- **`the-same-thing-obsessively`** (Monet's *Rouen Cathedral*, Warhol's *Marilyn
  Diptych* and *Campbell's Soup Cans*).

### A defect the tranche surfaced: the `pd` token on credit-required files

Promoting `little-dancer-aged-fourteen` showed that its image is a **CC BY 2.0
photograph of the sculpture** while the record carries `image.status:"pd"`.
**Seven records do.** Six of them are photographs of three-dimensional or
physically-sited works — Michelangelo's *David* and *Pietà*, the Degas — where
the Commons file page asserts a licence for the *photograph* though the work
beneath it is centuries old.

**It is not a licence breach, and the finding says so rather than implying one.**
All seven are registered in `js/photo-credits.js` and render their credit, so the
attribution obligation is met. The defect is that `pd` is doing two jobs:
`ARTWORK_SCHEMA` §3 defines `status` as a *rendering* flag, and `pd` also reads
as a claim about legal status — which `CATALOG_BATCH_02` constraint 5 explicitly
forbids for CC BY files.

Recorded and ratcheted at seven in `tests/test_rights_tooling.py`, **not silently
edited**: changing `status` could suppress rendering, and the schema has no value
meaning "licensed photograph of an old work", so choosing one is a schema
decision rather than a test's to make. A second test asserts the obligation that
*does* bind — every attribution-required image has a credit record.

**The repository's own OD-5 language guard then caught the docstring I wrote for
that test**, because I had stated a file's legal status directly instead of
saying what Commons asserts. Reworded. The guard works on its authors.

`LIST_TIER2_CEILING` lowered **35 → 24**.

## 7. What is left

1. **Twenty-four list works still below Tier 1**, across seven lists. Roughly
   two more tranches clears the backlog entirely.
2. **Seven records carry `pd` on a credit-required file.** Deciding what token a
   licensed photograph of an out-of-copyright work should carry is a schema
   question for the owner, not a silent edit.
3. **Lower `LIST_TIER2_CEILING`** whenever the number falls.
4. **F+D− is unfixable from the public domain** and should be treated as a
   product constraint, not a backlog item — the deck's opening card in that
   quadrant will be the same painting for every user, forever.
