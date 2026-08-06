# Catalog Batch 02 — consequence, without quota

*Vasari (`claude-curator`), 2026-08-07, branch `main`. Specification only.
No `js/catalog-*.js` file is written by this document; the records below are
proposals for the Data Steward and the Implementation Lead to build.*

**Nothing here is a rights determination or legal advice (OD-5).** Where a
licence is named, this document records what the Commons file page **asserts**
and what remains uncertain. The `pd` token in `ARTWORK_SCHEMA.md` §3 is a
rendering flag, not a finding.

Continues `docs/CATALOG_BATCH_01.md`. **Cap: 12 records.**

---

## THE BATCH PRINCIPLE

**Consequence, without quota.** A work is in this batch if *what came after it
is different because of it* — an effect attested in the record rather than
inferred from fame — and if the surviving record is strong enough to catalogue
honestly. **No cap of any kind**: not per nation, not per artist, not per
movement, not per century.

**Why this cut, and why not the alternatives.**

Batch 01's principle was breadth: one artwork per zero-artwork nation, capped at
one. That cap did real work — it stopped the batch becoming an argument for any
nation — but it had a cost that should be named. Under a one-per-nation ceiling,
significance was only ever a *within-nation tiebreak*. Batch 01 never once asked
"what are the strongest works in this pool, full stop," and so it catalogued no
work of the first rank. The pool contains Giotto, Masaccio, Rogier van der
Weyden, Titian, Sesshū and Kōrin, and after ten records it still contained all
of them.

This batch asks that question and removes every ceiling, so that the ranking is
allowed to say what it says.

Two alternatives were considered and rejected:

- **Depth in the eleven nations Batch 01 opened.** Rejected because it is
  region-driven by construction: it would let Batch 01's cut set this batch's
  agenda, and a second Polish record would be chosen *because* the first one was
  Polish. That is the shape of preference the neutrality standard forbids, one
  step removed.
- **The artists the atlas creates the absence of by naming them.** Batch 01
  found Verrocchio inside Leonardo's own arc text and Bellini teaching two
  painters who are both present. Checked this session: **neither is an artist
  record in this atlas** — `Verrocchio` appears once in `js/artists-1.js`,
  `Bellini` three times across `artists-8`, `-9` and `-16`, in prose only, and
  no `id:` matches either name. That route therefore needs **new artist
  records**, which is a different deliverable from a catalog batch and cannot
  draw on the pool at all. Recorded as a finding; not attempted here.

**On "significance", and the canon trap.** The curator brief is explicit that
following the received canon is not neutrality, because the canon is itself an
output of collecting history. So significance here is defined narrowly and
operationally as **consequence**: a demonstrable, sourced effect on what was
made afterwards. Fame is a fact about *reception*; consequence is a fact about
*production*. They overlap heavily in Europe because the same institutions
generated both, and where a work qualifies on both grounds this document says
which one it is here on.

The guard that follows: non-European candidates are tested on the **same
consequence axis** rather than being ranked by how famous they are in English.
Sesshū Tōyō and Ogata Kōrin are in this batch on exactly the test that admits
Giotto — a lineage that exists because of them.

**And the honest disclosure.** The pool is 413 images attached to artists this
atlas already holds, which is itself the residue of a collecting history.
Whatever national distribution this ranking produces is therefore **inherited,
not endorsed**. It is reported in COVERAGE EFFECT as a finding about the pool.
It is not corrected by substitution, because substituting a work into a batch to
improve a distribution is the same error as excluding one, and the brief forbids
both.

---

## SELECTION CONSTRAINTS INHERITED FROM BATCH 01

1. The 30 entries `IMAGE_RIGHTS_ROUTES.md` §1.6 records as confirmed mismatches
   (Groups A–C) or §14 rendering defects (Group D) are excluded before ranking.
2. `tools/audit_artworks.py:match_verdict` must return **`confirmed`**. Anything
   else is not proposable.
3. **`confirmed` does not mean catalogable.** Batch 01's working expectation
   holds: of 20 candidates all 20 confirmed, and only 13 resolved to a Wikidata
   item carrying collection, date and dimensions.
4. **Every dimension pair is sanity-checked** before it is recorded. Batch 01
   found `osman-hamdi-bey :: Two Musician Girls` carrying P2048/P2049 = 580/390,
   which the planned bake would print as "580 × 390 cm" on a live page.
5. Any CC BY / CC BY-SA file is flagged separately and does **not** take the
   `pd` token.

---

## RECORDS

*Appended two at a time as each pair clears `match_verdict` and its factual
claims are sourced. A row is here only when both are done.*

| # | artwork id | artist | nation | tier | verdict | licence asserted |
|---|---|---|---|---|---|---|
| R1 | `ognissanti-madonna` | Giotto di Bondone | italy | 2 | `confirmed` | pd |
| R2 | `the-holy-trinity-masaccio` | Masaccio | italy | 2 | `confirmed` | pd |

**On the tier column, and why it is not a dodge.** `ARTWORK_SCHEMA.md` §8 admits
a work to Tier 1 only through an editorial list, a Tier 1 artist's essential
works, the daily-painting schedule or the deck pool. This batch checked whether
the pool could reach any of those and it cannot: the **312 work ids named across
the Tier 1 arcs all resolve in the catalog already** (computed this session — zero
dangling references), so there is no arc waiting on a pool record, and none of
these artists is in `js/tier1-artists.js`. Every record here is Tier 2 on the
same reasoning as Batch 01. **Unlike Batch 01, this batch does propose a tier
change** — see T-TIER below, which uses §8 in the demotion direction.

### R1 — `ognissanti-madonna`

| field | value | source |
|---|---|---|
| title | Ognissanti Madonna | `js/artworks.js` key. Commons `ObjectName` = *Madonna Enthroned (Ognissanti Madonna)*; Wikidata **Q2016193** label = *Madonna Enthroned*. Keep `worksKey:"Ognissanti Madonna"` |
| artistId | `giotto` | exists in `js/artists-*.js` |
| year | display `c. 1300–1305`, sort `1300` | Commons `DateTimeOriginal` = "between circa 1300 and circa 1305"; Wikidata **P571** = 1300. The point date is the low end of the range, so the two agree rather than conflict |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Giotto%2C_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg/500px-Giotto%2C_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/Ognissanti_Madonna` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons `LicenseShortName` asserts a public-domain basis; `Copyrighted: False`; `Restrictions` empty |
| techniques | `["tempera","gold-leaf"]` | Wikidata **P186** = tempera, panel, gold. `panel` is a support and has no technique id; the artist record's `fresco` is **not** inherited — this is a panel |
| movements | `["proto-renaissance"]` | artist record. Commons' own date qualifier carries `P1480 → Q5727902 Proto-Renaissance`, so the label is not only ours |
| nation | `italy` | artist record |
| museum | `{ id:"uffizi", name:"Gallerie degli Uffizi", city:"Florence" }` — **venue exists** | Wikidata **P195** = Uffizi Gallery; **P217** inv. `00284545` |
| dims | `325 × 204 cm` | Wikidata **P2048** = 325, **P2049** = 204. **Sanity-checked:** a 3.25 m altarpiece is the right order of magnitude for a high altar panel; this is not the 580 × 390 failure |
| tags | `["sacred","group-scene","golden","monumental-scale"]` | `ARTWORK_SCHEMA.md` §5 vocabulary |
| coords | `{ F:-75, D:-55, E:+35, C:-25, M:+75 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**A three-way title split, resolved without renaming anything.** The Commons
*filename* calls the work **Maestà**, `ImageDescription` reads "Maestà Madonna
and Child", `ObjectName` reads *Madonna Enthroned (Ognissanti Madonna)*, and
Wikidata Q2016193's English label is *Madonna Enthroned*. `js/artworks.js` keys
it *Ognissanti Madonna*, which is also the English Wikipedia article title, and
that is the string the record should carry — it is the only one of the four that
identifies *this* Maestà rather than the genre. `worksKey` preserves the link
back to the artist page. Note for the Data Steward: **do not derive this title
from the filename.**

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Giotto*,
`ObjectName` names the work in several languages, `Credit` = Google Arts &
Culture. Source file 2056 × 3272 px.

**Consequence — why this work and not another.** The atlas's own influence graph
carries exactly one Giotto edge, `["giotto","masaccio","influenced"]`, and
`js/influences.js` states in its header that its edges are "grounded in the
artist bios elsewhere in the atlas" — which is a statement about internal
consistency and **not a source**, a defect this curator has already recorded
against all 238 edges. So the consequence claim is not resting on that edge. It
rests on what the object is: a panel in which a body has weight under cloth, a
throne is built in depth, and the hierarchy of a Byzantine Maestà is retained
while its flatness is not. R2 is the next move in the same argument, made by the
painter that edge points at, a hundred and twenty years later, on a wall.

**Coordinates, on the merits.** Fully figurative, but a gold ground and
hierarchical scaling that no illusionist would accept → `F −75`. Ceremonial and
motionless; the angels kneel and hold still → `D −55`. Conventional materials —
tempera, panel, gold, exactly the inherited kit — used to describe solids the
convention had no way to describe. The novelty is in the seeing, not the means,
which is why this is `E +35` and not higher. Presence before argument: the point
is a knee under drapery → `C −25`. Three and a quarter metres, made to be met
across a church → `M +75`.

### R2 — `the-holy-trinity-masaccio`

| field | value | source |
|---|---|---|
| id | `the-holy-trinity-masaccio` | §2: a generic devotional title takes artist disambiguation. Bare `the-holy-trinity` would collide with any later El Greco or Rublev record |
| title | The Holy Trinity | Commons `ObjectName`; Wikidata **Q977200** label = *Holy Trinity* |
| artistId | `masaccio` | exists in `js/artists-*.js` |
| year | display `1425–1426`, sort `1425` | **Sources disagree.** Commons `DateTimeOriginal` = "between 1425 and 1426"; Wikidata **P571** = 1420 (recorded twice on the item). The Commons range is adopted because it is the narrower statement and the qualifier structure shows it was entered as a range rather than rounded; **Wikidata's 1420 is noted, not adopted** |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Masaccio%2C_trinit%C3%A0.jpg/500px-Masaccio%2C_trinit%C3%A0.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/Holy_Trinity_(Masaccio)` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | `["fresco"]` | Wikidata **P186** = fresco; **P31** = fresco. The artist record's `tempera` is **not** inherited |
| movements | `["early-renaissance"]` | artist record |
| nation | `italy` | artist record |
| museum | `{ id:"santa-maria-novella", name:"Santa Maria Novella", city:"Florence" }` — **NEW VENUE**, type `church` | Wikidata **P195** = Basilica of Santa Maria Novella. The work is a wall, not a movable object; §5b exists for exactly this |
| dims | `667 × 317 cm` | Wikidata **P2048** = 667, **P2049** = 317. **Sanity-checked:** 6.67 m is large but is a wall fresco's correct order of magnitude, and the aspect matches the image (1028 × 2073 px, taller than wide) |
| tags | `["sacred","group-scene","geometry","monumental-scale"]` | §5 vocabulary |
| coords | `{ F:-80, D:-40, E:+55, C:+30, M:+80 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Masaccio*,
`ObjectName` = *The Holy Trinity* in several languages. Source file
**1028 × 2073 px — the smallest in this batch**, and its `Credit` is a book
reproduction (John T. Spike, *Masaccio*, Rizzoli, Milano 2002) rather than a
holding institution or an open-access programme. Flagged in POOL DEFECTS: it is
adequate for the 500 px rendering the catalog uses and it is the weakest file
provenance among these records.

**Consequence.** This is the batch's clearest case and the reason the principle
is *consequence* rather than significance: the work's effect is a technique that
every subsequent painter in the tradition had to either use or refuse. The
architecture is constructed in one-point perspective with the vanishing point at
a standing viewer's eye level, which is a fact about the picture rather than a
claim about its reception. The atlas's graph runs
`masaccio → michelangelo` and `masaccio → piero-della-francesca`; again those
edges carry no source and are not what the claim rests on.

**Coordinates, on the merits.** Every figure legible and solid → `F −80`.
Nothing moves; this is a vertical hierarchy held still → `D −40`. The means
*are* the invention here, which is what separates R2 from R1 → `E +55`. It is
built to be read — the eye-level vanishing point places the viewer inside the
argument, and a painted tomb with an inscription sits beneath it → `C +30`. Life
scale and above, on a church wall → `M +80`.

---

## NEW VENUES REQUIRED

*Filled as records land. `ARTWORK_SCHEMA.md` §5b: registry additions are cheap
and unreviewed; slug renames are forbidden.*

| venue id | name | city | country | type | needed by |
|---|---|---|---|---|---|

---

## CC-LICENSED IMAGES FLAGGED

*Filled as records land.*

---

## TAXONOMY, TIER AND TECHNIQUE PROPOSALS

*Filled as records land.*

---

## POOL DEFECTS THIS BATCH FOUND

*Filled as records land.*

---

## NOT PROPOSED — considered and rejected

*Filled as records land.*

---

## COVERAGE EFFECT

*Filled as records land.*

---

## UNCERTAIN — left standing rather than smoothed

*Filled as records land.*
