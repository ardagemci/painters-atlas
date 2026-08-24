# Catalog Batch 03 — the atlas's own gravity

*2026-08-24, branch `catalog-batch-03`. Backlog **E1**. Twelve records, built
and shipped as `js/catalog-6.js`; this document is the specification and the
evidence behind them, written alongside rather than after.*

**Nothing here is a rights determination or legal advice (OD-5).** Where a
licence is named, this records what the Commons file page **asserts** and what
remains uncertain. The `pd` token in `ARTWORK_SCHEMA.md` §3 is a rendering flag,
not a finding.

Continues `docs/CATALOG_BATCH_01.md` (breadth: one work per zero-artwork nation)
and `docs/CATALOG_BATCH_02.md` (consequence, without quota). **Cap: 12 records.**

---

## THE BATCH PRINCIPLE

**Inbound gravity — the works the atlas already argues for and cannot show.**

Backlog **E1** says the atlas is mostly inert, and re-measuring it this session
sharpened the number: **194 of 266 painters (73%) have no catalog record at
all**, and **125 of them carry 370 audited gallery images** already rendering on
their artist pages. That pool is the batch's whole universe.

Batch 02's principle was consequence — a demonstrable effect on what was made
afterwards. That is a claim about art history. This batch asks a narrower
question that Pigment can answer about itself: **which painters does this site
lean on hardest in its own prose, while being unable to show a single work?**
It is the same move `B3` made for artist records — *holes the atlas dug for
itself* — applied to works instead of people.

The advantage is that it is measurable rather than felt. For each of the 125
candidates, three counts were taken from the shipped data:

| signal | what it counts | weight |
| --- | --- | --- |
| influence degree | edges in `js/influences.js`, in **and** out | ×3 |
| prose mentions | other painters' `life`/`career`/`outside`/`facts` naming them | ×2 |
| taxonomy mentions | appearances in `js/taxonomy.js` movement and technique copy | ×1 |

The twelve highest-scoring painters with a public-domain gallery image are this
batch. The ranking, and everything below it, is reproducible from the repository
with no judgement in the loop.

### What the ranking said, including the parts it got wrong

The top of the list: Delacroix (28), Rubens (25), Vasari (24), Ingres (23),
Gérôme (23), Van Dyck (19), Sargent (18), Marc (17), Pissarro (16), Mondrian
(16), Poussin (15), Constable (14), Toulouse-Lautrec (14).

**One exclusion, and the reason is the interesting part. Vasari scored third and
is not in this batch.** His ten prose mentions are almost entirely other
painters' records citing *the Lives* — his book, not his brush. The metric
cannot tell bibliographic gravity from painterly gravity, and a Vasari painting
catalogued on the strength of his prose would be the metric using the atlas to
justify itself. Recorded as a limitation of the measure, not patched around.

Constable and Toulouse-Lautrec (14 each) therefore move up into the twelve.

### The distribution, disclosed rather than corrected

Six of twelve are French. That is **inherited from the pool, not endorsed**: the
370-image pool is itself the residue of a collecting history, and Batch 02's
standing rule applies unchanged — *substituting a work into a batch to improve a
distribution is the same error as excluding one*. The number is reported here
so it is visible rather than remembered.

| nation | records |
| --- | --- |
| france | 6 (Delacroix, Ingres, Gérôme, Pissarro, Poussin, Toulouse-Lautrec) |
| belgium | 2 (Rubens, Van Dyck) |
| britain | 1 (Constable) |
| germany | 1 (Marc) |
| netherlands | 1 (Mondrian) |
| usa | 1 (Sargent) |

---

## SELECTION CONSTRAINTS INHERITED FROM BATCHES 01–02

1. Entries recorded as confirmed mismatches in `IMAGE_RIGHTS_ROUTES.md` §1.6 are
   excluded before ranking.
2. **`confirmed` does not mean catalogable** — the working ratio held again, in
   a new way: all twelve resolved to a Wikidata item, but **three of the twelve
   carried a dimension Wikidata got wrong**, and one carried none at all.
3. **Every dimension pair is arbitrated, not copied.** See DIMENSIONS below.
4. **CC BY / CC BY-SA files do not take the `pd` token.** This constrained the
   batch rather than merely filtering it: see Rubens, below.

### The Rubens case, because it shows the constraint doing work

Rubens's most consequential picture in the pool is *The Descent from the Cross*.
Its Commons file asserts **CC BY 3.0**, and the *Marie de' Medici Cycle* file
asserts **CC BY 4.0** — so under constraint 4 neither can carry `pd`, and the
record went to **The Garden of Love** (Prado, public domain). That is the rule
choosing the painting, and it is stated here rather than smoothed over. The
Descent remains his artist-page hero with its credit line intact, which is why
the prerender surface moves for Rubens and not for the other eleven.

---

## RECORDS

All twelve are **Tier 2**. `ARTWORK_SCHEMA.md` §8 admits a work to Tier 1 only
through an inbound link, and none of these twelve is named in
`js/tier1-artists.js` or `js/lists-1.js` — checked by string search, not assumed.
Each nevertheless carries hand-scored coords, a 60–90 word description and
exactly three notice bullets, so promotion is a one-line tier edit and the URL
never changes.

| # | artwork id | artist | museum | year | verdict |
|---|---|---|---|---|---|
| R1 | `liberty-leading-the-people` | Delacroix | Louvre | 1830 | pd |
| R2 | `the-garden-of-love` | Rubens | Prado | c. 1630–1635 | pd |
| R3 | `grande-odalisque` | Ingres | Louvre | 1814 | pd |
| R4 | `pollice-verso` | Gérôme | **Phoenix Art Museum** | 1872 | pd |
| R5 | `charles-i-at-the-hunt` | Van Dyck | Louvre | c. 1635 | pd |
| R6 | `madame-x` | Sargent | Met | 1883–1884 | pd |
| R7 | `the-fate-of-the-animals` | Marc | Kunstmuseum Basel | 1913 | pd |
| R8 | `the-boulevard-montmartre-at-night` | Pissarro | National Gallery | 1897 | pd |
| R9 | `gray-tree` | Mondrian | **Kunstmuseum Den Haag** | 1911 | pd |
| R10 | `et-in-arcadia-ego` | Poussin | Louvre | 1637–1638 | pd |
| R11 | `the-hay-wain` | Constable | National Gallery | 1821 | pd |
| R12 | `at-the-moulin-rouge` | Toulouse-Lautrec | Art Institute of Chicago | 1892–1895 | pd |

### Two venues the batch had to open

`Pollice Verso` and `Gray Tree` are held by museums the registry did not
contain. **E3** names exactly this — *the holding institutions are simply not in
the venue registry* — so the batch opened them rather than picking easier
paintings, which would have let the infrastructure choose the art.

`phoenix-art-museum` and `kunstmuseum-den-haag` are now in `js/venues.js` with
full notes in `js/museums-1.js` (hook, founded, essay, building photograph) and
credit records in `js/photo-credits.js`. Both photographs are CC BY-SA and both
require attribution.

**The Den Haag photograph was chosen by looking at it.** The obvious candidate,
`File:Den Haag - Gemeentemuseum (39788683042).jpg`, is **a painting hanging
inside the museum**, not the museum. This is the same failure the Schwitters,
Sorolla, Kunsthistorisches and Groeningemuseum images were: a filename that
names the thing, attached to a file that is not it.

---

## DIMENSIONS — what arbitration actually found

Rule 1 of `ARTWORK_SCHEMA` §7.1 exists because a bake once nearly printed metres
as centimetres. It is still live, and this batch found two more shapes of the
same problem. The standing rule applied throughout: **where the holding
institution publishes a measurement, the institution wins.**

| record | Wikidata says | shipped | why |
| --- | --- | --- | --- |
| `madame-x` | 2432 × 1438 mm | **208.6 × 109.9 cm** | Wikidata carries the **frame**. The Met gives the canvas as 208.6 × 109.9 and lists *Framed: 243.2 × 143.8 × 12.7* separately. New rule: §7.1 rule 3. |
| `at-the-moulin-rouge` | 1230 × 1410 **mm** | **123 × 141 cm** | Rule 1, unpatched and still firing. Confirmed against the Art Institute's own API. |
| `gray-tree` | 79.7 × 109.1 cm | **79.7 × 109.1 cm** | Kept — English Wikipedia's competing 78.5 × 107.5 measures the **cropped derivative file**, not the painting. The Gemeentemuseum's own record, via the Commons `Artwork` template, agrees with Wikidata. |
| `the-fate-of-the-animals` | 196 × 266 **and** 195 × 263.5 | **195 × 263.5 cm** | Three published widths existed (268 / 266 / 263.5). Taken from the pair attached to Basel's own inventory number 1739, corroborated by the German article the museum's file is used in. |
| `pollice-verso` | height only (96.5) | **96.5 × 149.2 cm** | Wikidata has no `P2049`. Width from the Phoenix Art Museum record. |

`grande-odalisque` carries a **date** disagreement of the same kind: Wikidata's
`P571` says 1810, the Louvre and every catalogue say **1814**, and 1814 ships.

**And the collection field bit once.** `Liberty Leading the People` lists
Luxembourg Museum (1863–1874, ended) *before* the Louvre. A resolver taking
`claims[0]` files the most famous painting in France in a museum it left in
1874. `P195` was read with rank and start/end qualifiers intact throughout —
`ARTWORK_SCHEMA` §7.1 rule 5, confirmed as load-bearing rather than theoretical.

---

## COORDS — and one deliberate correction to the house habit

`docs/TASTE_AUDIT.md` (E4, 2026-08-22) measured a scoring habit in the existing
168 scored records: within the **figurative half alone**, F and E correlate at
**+0.68** — the less straightforwardly representational a picture, the more
experimental it gets scored, independently of whether it was. That was named as
the one defect rescoring could fix.

These twelve were scored with that finding in hand. Ten of the twelve sit at
F −60 to −90, and their E values run from **−55** (Gérôme, an arch-conservative
technician painting a lost gesture) to **+45** (Toulouse-Lautrec). F and E are
decoupled across the figurative records here by construction. The two works that
are genuinely moving away from description — Marc at F +25 and Mondrian at
F +15 — carry high E because that is what they are doing, not because of where
they sit on F.

**E is read as "experimental for its moment", not absolutely.** The audit found
that ambiguity is in `ADMIRE_SPEC` §3's own wording and remains unresolved. This
batch does not resolve it; it follows the reading the existing 168 records
already use, so that a new batch does not deepen an inconsistency it cannot
settle. Recorded here so the choice is visible.

`gray-tree` is the batch's one deliberate contribution to the axis the audit
found bimodal: **F is a flag, not a dimension** — 84 works at the extremes, 38
across the entire middle third. *Gray Tree* is a tree that has stopped being a
tree, and it is scored where it belongs, at **F +15**. One record does not fix a
distribution, and it is not offered as fixing one.

---

## WORK-LEVEL OVERRIDES, AND WHY

`movements`, `techniques` and `nation` inherit from the artist unless the work
argues otherwise (§3). Five records argue otherwise:

- **`gray-tree` → `cubism`.** Mondrian's record carries `de-stijl` and
  `abstract-art`; in **1911** he is a member of neither. The work is Mondrian
  beginning to work through Cubism, which is the honest label and exactly the
  case the override exists for.
- **`et-in-arcadia-ego` → `baroque` only.** Poussin's record adds
  `neoclassicism`, which is an eighteenth-century movement and anachronistic on
  a painting of 1637.
- **`pollice-verso` → `academicism` only.** Gérôme's record carries
  `orientalism` as well, and **A3** settled that he belongs there — but this is
  a Roman arena, and tagging it Orientalist because its painter is one would
  undo the point A3 made.
- **`madame-x` → `realism` only** (his record adds `impressionism`), and
  **`the-boulevard-montmartre-at-night` → `impressionism` only** (his adds
  `neo-impressionism`, which by 1897 he had left behind).

`nation` on the two Flemish records stays `belgium` although *Charles I at the
Hunt* was painted in London for an English king: it records the painter's
tradition, consistently with how every other record in the catalog is filed.

---

## COVERAGE EFFECT

- Artists with at least one catalog record: **72 → 84** of 266.
- Artists with none: **194 → 182**. Still 68% of the atlas.
- Catalog records: **350 → 362**. Tier 1 unchanged at **75** — a Tier 2 batch
  cannot move the deck pool, and this one does not pretend to.
- Venues: **125 → 127**. Museum notes: **114 → 116**, all with photographs.
- Asset inventory: `catalog_pd_rendered` **+12**, `catalog_gallery_overlap`
  116 → **128**, `total_unique` 835 → **837**. The +2 is the two museum
  photographs — **the twelve artworks add no new asset to the tree at all**,
  because every one was already an audited gallery image. That is the economics
  of a catalog batch, and the reason there should be several more.

## WHAT THE NEXT BATCH SHOULD KNOW

1. **The pool is still 113 painters deep.** The ranking is reproducible; run it
   again and take the next twelve.
2. **Budget for venues.** Two of twelve needed a new venue *and* a museum note
   *and* a verified building photograph. Expect that ratio to rise as the batch
   moves down the ranking and away from the Louvre.
3. **The measure cannot tell why a painter is cited.** Vasari is the recorded
   case. Read the mentions before trusting the score.
4. **Check the institution, not the aggregator.** Three of twelve dimensions and
   one date were wrong on Wikidata, in three different ways, and every one of
   them passed the existing §7.1 checks.
