# Catalog Batch 04 — the same ranking, run again

*2026-08-24, branch `catalog-batch-04`. Backlog **E1**. Twelve records, shipped
as `js/catalog-7.js`. Continues `docs/CATALOG_BATCH_03.md` with the same
principle and no new argument: the whole point of a measured cut is that it can
be re-run.*

**Nothing here is a rights determination or legal advice (OD-5).**

---

## THE RANKING, RE-RUN

Batch 03's rule, unchanged: **inbound gravity** over the painters who hold
audited gallery images and no catalog record — influence-graph degree ×3,
mentions by name in other painters' prose ×2, taxonomy-copy mentions ×1. The
pool going in was **113 painters**; it is **101** now.

| # | painter | score | edges | prose | taxonomy |
|---|---|---|---|---|---|
| 1 | Renoir | 14 | 2 | 4 | 0 |
| 2 | Fragonard | 14 | 2 | 3 | 2 |
| 3 | Gainsborough | 13 | 3 | 2 | 0 |
| 4 | Millet | 13 | 3 | 2 | 0 |
| 5 | Frederic Edwin Church | 13 | 2 | 3 | 1 |
| 6 | Theophanes the Greek | 13 | 1 | 4 | 2 |
| 7 | Bellini | 12 | 2 | 3 | 0 |
| 8 | Boucher | 12 | 2 | 3 | 0 |
| 9 | Watteau | 12 | 2 | 2 | 2 |
| 10 | Emily Carr | 12 | 0 | 5 | 2 |

## THE TIE, AND WHAT WAS DONE ABOUT IT

The ranking then stops working. **Seven painters tie at 11 points with
identical values on all three signals** — Signac, Reynolds, Daumier, Rossetti,
Corot, Carracci and Modigliani each score edges 3, prose 1, taxonomy 0. There is
no sort order that is not arbitrary, and two of the seven were needed.

Three ways out were considered:

1. **Take all seven and ship seventeen.** Batch 02 removed every cap for a good
   reason, and cutting a tie arbitrarily is worse than a larger batch. Rejected
   only because a cap of twelve was the instruction.
2. **Pick two by taste.** Rejected: that is the metric being overruled without
   saying so, which is precisely the failure the Vasari exclusion exists to name.
3. **Ask a second-order version of the same question** — adopted.

**The tie-break: how many of a painter's influence edges land on a painter who
already has a catalog record.** It asks not only whether the atlas argues for
them but whether it argues from ground it has already covered, which is the
batch principle one level down rather than a different principle.

| painter | edges to catalogued painters |
|---|---|
| **Paul Signac** | **3 of 3** — Delacroix, Matisse, Seurat |
| **Annibale Carracci** | **2 of 3** — Poussin, Caravaggio |
| Reynolds | 1 (Van Dyck) |
| Daumier | 1 (Goya) |
| Corot | 1 (Pissarro) |
| Rossetti | 0 |
| Modigliani | 0 |

It separates cleanly, and there is a detail worth keeping: **Signac's promotion
was caused by Batch 03.** One of his three edges runs to Delacroix, who was
inert a week ago. The graph tightens as the atlas fills, and the ranking
notices.

## STANDING EXCLUSIONS

**Vasari — permanently, not per batch.** He tops this ranking too, at 24 points,
and will keep topping it. Ten of his prose mentions are other painters' records
citing *the Lives*. That is bibliographic gravity, not painterly, and the
measure cannot tell them apart. Recording it once here retires the decision so
no future batch re-argues it.

*Six Tuscan Poets* — Vasari's invented group portrait of six writers who could
not have sat for it, painted by the man who invented art history — is a strong
record and the honest route to it is an editorial list, which would give it real
Tier 1 inbound gravity under `ARTWORK_SCHEMA` §8. Filed as a list idea, not as a
catalog exception.

---

## RECORDS

All twelve Tier 2; none named in `js/tier1-artists.js` or `js/lists-1.js`.

| # | artwork id | artist | museum | year |
|---|---|---|---|---|
| R1 | `bal-du-moulin-de-la-galette` | Renoir | Musée d'Orsay | 1876 |
| R2 | `the-bolt` | Fragonard | Louvre | 1777 |
| R3 | `mr-and-mrs-andrews` | Gainsborough | National Gallery | c. 1750 |
| R4 | `the-gleaners` | Millet | Musée d'Orsay | 1857 |
| R5 | `the-heart-of-the-andes` | Church | Met | 1859 |
| R6 | `frescoes-of-the-transfiguration-novgorod` | Theophanes | **Novgorod** | 1378 |
| R7 | `portrait-of-doge-leonardo-loredan` | Bellini | National Gallery | c. 1501–1502 |
| R8 | `madame-de-pompadour` | Boucher | **Wallace Collection** | 1759 |
| R9 | `the-embarkation-for-cythera` | Watteau | Louvre | 1717 |
| R10 | `forest-british-columbia` | Emily Carr | **Vancouver Art Gallery** | 1931–1932 |
| R11 | `the-papal-palace-avignon` | Signac | Musée d'Orsay | 1909 |
| R12 | `the-beaneater` | Carracci | **Palazzo Colonna** | c. 1580–1590 |

### Four venues, as predicted

Batch 03 closed with: *"Budget for venues. Expect that ratio to rise as the batch
moves down the ranking and away from the Louvre."* It went from two in twelve to
**four in twelve**. All four are in `js/venues.js` with notes, photographs and
credit records; the Wallace Collection and Vancouver Art Gallery carry full
essays, Palazzo Colonna and the Novgorod church carry hook and photograph.

**The Novgorod church is E3 arriving inside an E1 batch** — a 1378 fresco cycle
whose holding building simply had no registry row, which is exactly the shape of
absence E3 describes.

**And a third filename trap, caught by looking.**
`File:The Wallace collection London 01.jpg` is **a black-and-white photograph of
a bronze sculpture indoors**. That is the same failure as
`File:Den Haag - Gemeentemuseum (39788683042).jpg` in Batch 03 (a painting
hanging inside the museum) and the Groeningemuseum and Kunsthistorisches files
before them. Every venue photograph in this batch was opened and looked at.

---

## THE IMAGE THAT WAS WRONG, AND WHAT CAUGHT IT

`the-papal-palace-avignon` originally shipped a Commons URL for a file named
`Paul_Signac_-_Avignon._Soir_(le_château_des_Papes)_-_Google_Art_Project.jpg`.
**No such file exists.** The real gallery file is `..._-_1909.jpg`.

The mistake was made in a recognisable way: a Commons wikitext fetch for that
title returned **empty**, and that empty result was read as "this file has no
Artwork template" rather than as "this file is not there." An absent answer was
treated as a null finding instead of as a negative one.

What caught it was `tools/audit_artwork_rights.py`: the census reported one
entry `missing`, and reported its `used_in` as `['js/catalog-7.js']` **alone**.
A catalog image that the artist's own gallery does not also carry is the
signature of an invented URL, because a catalog batch built from the pool can
only ever re-use one. That is a reusable check and it is written down here.

---

## DIMENSIONS — five of twelve needed arbitration

The standing rule holds: **where the holding institution publishes a
measurement, the institution wins.**

| record | aggregators say | shipped | why |
| --- | --- | --- | --- |
| `the-gleaners` | 830 × 1100 mm (WD); 83.8 × 111.8 (enwiki) | **83.5 × 110 cm** | The Musée d'Orsay's own figure. Wikidata and Wikipedia disagree with the holder in two different directions. |
| `bal-du-moulin-de-la-galette` | 131 × 175 (WD **and** enwiki) | **131.5 × 176.5 cm** | The Orsay again. **Two sources agreeing is not two checks** — this is the clearest case of it the batches have produced. |
| `the-embarkation-for-cythera` | 1.29 × 1.94 **metres** | **129 × 194 cm** | §7.1 rule 1, the Courbet regression case, live again. |
| `the-papal-palace-avignon` | 73.5 × 92.3; inception 1900 *or* 1909 | **73.3 × 91.9 cm, 1909** | Two competing inceptions, neither preferred. The Orsay gives 1909 — and so does the Commons filename, once the right file is found. |
| `the-heart-of-the-andes` | 168 × 302.9 | **168 × 302.9 cm** | Kept: confirmed identical against the Met's own API. A check that passes is still a check. |

`frescoes-of-the-transfiguration-novgorod` carries **no `dims` at all**, and that
is correct rather than missing: the work is a fresco cycle in a building, and a
height × width pair would be a statement about one wall.

**Collections bit twice more.** `bal-du-moulin-de-la-galette` lists the Louvre
(1929–1986, ended) before the Orsay, and `the-embarkation-for-cythera` lists the
Académie royale (1717–1793, ended) before the Louvre. Both were read with rank
and end-date qualifiers intact.

---

## TONE — one record written straight

**`the-bolt`.** Fragonard's *Le Verrou* has a genuinely contested subject: an
embrace, or an assault. `STYLE_GUIDE` forbids a light register where factual
qualification is required, and the atlas keeps the record on hard subjects
rather than smoothing them. The description names the disagreement and does not
resolve it, and there is no wink in it anywhere.

The alternative — swapping to *The Progress of Love* — was rejected on Batch
02's rule: removing a work from a batch to make the batch more comfortable is
the same error as adding one for the same reason. (Fragonard's *The Swing* was
never a candidate: its Commons file asserts **CC BY-SA 4.0**, so it cannot take
the `pd` token, the same constraint that chose Rubens's picture in Batch 03.)

---

## WORK-LEVEL OVERRIDES

- **`the-papal-palace-avignon` → `neo-impressionism` only** (his record adds
  `post-impressionism`), and **`forest-british-columbia` → `expressionism` only**
  (hers adds `post-impressionism`) — in both cases the work sits squarely in one.
- **`portrait-of-doge-leonardo-loredan` → `early-renaissance`,
  `venetian-school`**, dropping the generic `renaissance`; techniques are
  `oil-painting` alone, because Wikidata's material is oil on **panel** and the
  artist record's `tempera` is not what this is.
- **`the-beaneater` keeps `baroque`** although the picture predates the movement
  by twenty years. Carracci is the painter through whom the Baroque arrives and
  this canvas is part of how; filing it under `mannerism` would name its
  opposite. Flagged as the batch's one knowingly loose label.
- **`frescoes-of-the-transfiguration-novgorod` keeps `nation: "greece"`** for a
  monument standing in Russia, on the same reasoning that kept Van Dyck's
  *Charles I at the Hunt* Flemish in Batch 03: the field records the painter's
  tradition, consistently across the catalog.

---

## COVERAGE EFFECT

- Artists with at least one catalog record: **84 → 96** of 266.
- Artists with none: **182 → 170**. Pool remaining: **101 painters**.
- Catalog records: **362 → 374**. Tier 1 unchanged at **75**.
- Venues **127 → 131**; museum notes **116 → 120**, all with photographs.
- `catalog_gallery_overlap` **128 → 140**; `total_unique` **837 → 841**, and the
  +4 is entirely the four museum photographs. **The twelve artworks add no new
  asset to the tree**, for the second batch running.

### The distribution, again inherited

France 5 (Renoir, Fragonard, Millet, Boucher, Watteau — Signac makes 6), Italy 2,
Britain 1, USA 1, Canada 1, Greece 1. Still Europe-weighted, still a fact about
the pool rather than a preference, still not corrected by substitution.

## WHAT THE NEXT BATCH SHOULD KNOW

1. **101 painters left.** Re-run `rank.py`'s logic; it is four lines of counting.
2. **Venue cost is rising fast**: two in twelve, then four in twelve. Assume five.
3. **The tie will recur** — five painters still sit at 11 with identical signals.
   The second-order tie-break is now precedent and should be applied, not
   reinvented.
4. **An empty lookup is a negative finding, not a null one.** The Signac.
5. **Two aggregators agreeing is one source.** The Renoir.
