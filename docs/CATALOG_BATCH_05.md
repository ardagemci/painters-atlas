# Catalog Batch 05 — the ranking, and a loop closing

*2026-08-24. Backlog **E1**. Twelve records, `js/catalog-8.js`. Same principle
as Batches 03 and 04; this document records only what was different.*

---

## The cut needed no tie-break

Batch 04 had to invent one: seven painters tied at 11 points with identical
values on all three signals. This time the arithmetic is kinder — the whole
11-point band (seven) and the whole 10-point band (five) come to **exactly
twelve**, so the boundary falls on a score change rather than inside one. The
second-order tie-break stands unused, for next time.

| band | painters |
| --- | --- |
| 11 | Reynolds, Daumier, Rossetti, Corot, Modigliani, **Nakkaş Osman**, **Guo Xi** |
| 10 | Aivazovsky, Holbein, Léger, Morisot, Georges de La Tour |

Vasari remains the standing exclusion.

## The E3 roster entered the ranking on its own merit

**Guo Xi arrives at 11 points**, level with Corot and Daumier — three taxonomy
mentions and edges to Fan Kuan and An Gyeon, all created by the E3 batch three
hours earlier. Shen Zhou, Hasegawa Tōhaku, Abd al-Samad and Fan Kuan are all in
the ranking now too.

Nothing was pushed. **Widening the roster fed the measure that selects what to
catalogue**, which is the first time these two threads have closed a loop — and
`early-spring` is the atlas's first Song dynasty catalog record.

Nations: france 4, britain 2, italy 1, germany 1, china 1, turkey 1, armenia 1,
france-again — the most varied batch so far, and the first with a Chinese and an
Ottoman record in it.

## Eleven of twelve image URLs were wrong when first written

They were **composed from memory** of Commons naming conventions, and **every
one of the eleven returned 404**. This is Batch 04's Signac failure, at scale.

What caught it was a HEAD check on every `src` before anything shipped —
a check that exists *because* of the Signac. What fixed it was giving up on
writing URLs at all: **all twelve are now read straight out of `js/artworks.js`**,
which is where a catalog batch should take them anyway, since the economics of
the format depend on re-using the audited pool. Each was then re-checked on two
conditions — a 200, **and** membership of the gallery pool — and all twelve pass
both.

**The rule that generalises:** a catalog batch should never author an image URL.
If the work is in the pool the URL exists already; if it is not in the pool, the
batch is adding an asset and should say so.

## Two pairings came back `unconfirmed`, and were resolved by looking

- **The Cradle** — the file's `ObjectName` is *"Le berceau"*. That is the exact
  example `match_verdict`'s own docstring gives for a foreign-language file page,
  and the docstring says a caller holding independent evidence may accept it.
  Accepted, and the image was opened: Edma with her chin propped, the gauze, the
  sleeping child.
- **Surname-i Hümayun** — Commons describes the folio as *the carrying-in of a
  model of the Süleymaniye Mosque*. The record's description originally described
  a different folio (the glassblowers at their furnace), so **the description was
  rewritten to describe the page the reader will actually see**. The record now
  says what is on the screen.

## Dimensions and dates

The aggregator was wrong twice more. `the-third-class-carriage` carries **two**
Wikidata inceptions, 1862 and 1868, neither preferred — the Met says **1864**.
`beata-beatrix` reads 1872 on Wikidata; Tate, which holds it (N01279), gives
**c. 1864–70**, and the 1872 belongs to one of the later versions.

`surname-i-humayun` carries **no `dims`**: Wikidata's lone 335 cm height with no
width is a figure about a manuscript, and a height × width pair for an
illustrated book would be a claim about one folio. Same reasoning as the Novgorod
frescoes in E3.

## Three venues

`national-palace-museum-taipei`, `topkapi-palace-museum` and
`national-portrait-gallery-london` — the first two because Guo Xi and Nakkaş
Osman are held there and the E3 roster brought them, the third because
*Portrait of Omai* was **bought jointly in 2023** by the National Portrait
Gallery and the Getty and alternates between London and Los Angeles. Filing it
under one owner would be half-true, so the record names the NPG and the notice
bullet states the joint acquisition.

Batch 04 predicted five new venues for this batch. It was three.

## Coverage effect

- Artists with a catalog record: **96 → 108** of 279.
- Catalog records **374 → 386**; venues **131 → 134**; museum notes **120 → 123**.
- `catalog_gallery_overlap` **140 → 152**; `total_unique` **868 → 871**, and the
  +3 is the three museum photographs. **No new artwork asset, for the third
  batch running.**
- Pool remaining: **~101 painters**, plus the thirteen E3 added.
