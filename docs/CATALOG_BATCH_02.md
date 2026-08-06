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
| R3 | `the-descent-from-the-cross-van-der-weyden` | Rogier van der Weyden | belgium | 2 | `confirmed` | pd |
| R4 | `the-tempest` | Giorgione | italy | 2 | `confirmed` | pd |
| R5 | `venus-of-urbino` | Titian | italy | 2 | `confirmed` | pd |
| R6 | `lamentation-of-christ-mantegna` | Andrea Mantegna | italy | 2 | `confirmed` | pd |
| R7 | `haboku-sansui` | Sesshū Tōyō | japan | 2 | `confirmed` | pd |
| R8 | `red-and-white-plum-blossoms` | Ogata Kōrin | japan | 2 | `confirmed` | pd |
| R9 | `oath-of-the-horatii` | Jacques-Louis David | france | 2 | `confirmed` | pd |
| R10 | `the-raft-of-the-medusa` | Théodore Géricault | france | 2 | `confirmed` | pd |
| R11 | `a-burial-at-ornans` | Gustave Courbet | france | 2 | `confirmed` | pd |
| R12 | `a-sunday-afternoon-on-the-island-of-la-grande-jatte` | Georges Seurat | france | 2 | `confirmed` | pd |

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

### R3 — `the-descent-from-the-cross-van-der-weyden`

| field | value | source |
|---|---|---|
| id | `the-descent-from-the-cross-van-der-weyden` | §2, and the collision is not hypothetical: a Wikidata title search for "The Descent from the Cross" returns **four** paintings — this one, Rembrandt's (Alte Pinakothek), Rubens's Antwerp triptych, and a Chassériau — plus the subject-matter item. Bare `the-descent-from-the-cross` would be indefensible |
| title | The Descent from the Cross | Commons `ObjectName` = *El Descendimiento* / *The Descent from the Cross*; Wikidata **Q568847** |
| artistId | `rogier-van-der-weyden` | exists in `js/artists-*.js` |
| year | display `c. 1435–1438`, sort `1435` | **Sources disagree.** Commons `DateTimeOriginal` = "between 1435 and 1438" with `P1319`/`P1326` earliest/latest qualifiers; Wikidata **P571** = 1440. The Commons range is recorded; **1440 is noted, not adopted** |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/El_Descendimiento%2C_by_Rogier_van_der_Weyden%2C_from_Prado_in_Google_Earth.jpg/960px-El_Descendimiento%2C_by_Rogier_van_der_Weyden%2C_from_Prado_in_Google_Earth.jpg` | `js/artworks.js` |
| image.page | `https://commons.wikimedia.org/wiki/File:El_Descendimiento,_by_Rogier_van_der_Weyden,_from_Prado_in_Google_Earth.jpg` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False`; `Restrictions` empty |
| techniques | `["oil-painting"]` | Wikidata **P186** = oil paint, panel. The artist record's `glazing` is **not** inherited — no source read here asserts it of this work |
| movements | `["early-netherlandish"]` | artist record |
| nation | `belgium` | artist record — **anachronistic, flagged in T-NATION below, not silently corrected** |
| museum | `{ id:"prado", name:"Museo Nacional del Prado", city:"Madrid" }` — **venue exists** | Wikidata **P195** = Museo del Prado; **P217** inv. `P002825`. Commons `Credit` = "The Prado in Google Earth", which ties the *file* to the same institution |
| dims | `204.5 × 261.5 cm` | Wikidata **P2048** = 204.5, **P2049** = 261.5. **Sanity-checked** |
| tags | `["sacred","group-scene","mourning","theatrical"]` | §5 vocabulary |
| coords | `{ F:-85, D:+55, E:-10, C:-30, M:+45 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Rogier van der
Weyden*, `ObjectName` names the work in six languages. Source file
**30000 × 23277 px**, the largest in this batch.

**How the Wikidata item was resolved, stated because it is weaker than R1's.**
This record's `image.page` is a **Commons file page, not a Wikipedia article**,
so the `pageprops → wikibase_item` route that resolved R1, R2 and R4 returns
nothing. Q568847 was reached by `wbsearchentities`, whose own description string
reads "painting by Rogier van der Weyden in the Museo del Prado", and the tie is
corroborated by the file's `Credit` naming the Prado. That is a two-step
identification rather than a link, and it is exactly the resolution method Batch
01 warned was "not exhaustive". It is recorded so a later reviewer can re-test it
rather than inherit it.

**Consequence.** Rogier's effect is not a technique but a register: grief given
the compositional weight of doctrine. Ten life-size figures are pressed into a
shallow gilded box the depth of a carved shrine, and the Virgin's collapsed body
is drawn as a near-exact rhyme of her son's — the invention is that the picture's
*structure* is the emotion. The atlas's graph carries one inbound edge,
`["jan-van-eyck","rogier-van-der-weyden","influenced"]`, and **no outbound edge
at all**, which understates him considerably; see COVERAGE EFFECT.

**Coordinates, on the merits.** Wholly figurative, life scale → `F −85`. Grief
at full pitch, but arrested rather than moving — a tableau, not an action →
`D +55`. Netherlandish panel practice at its height; superb, and not novel in
its means → `E −10`. It works on the body first: you feel the swoon before you
read the theology → `C −30`. Two and a half metres of altarpiece with figures at
life size, but the emotional register is intimate → `M +45`.

### R4 — `the-tempest`

| field | value | source |
|---|---|---|
| title | The Tempest | Commons `ObjectName` = *La Tempesta* / *Tempest*; Wikidata **Q930137** |
| artistId | `giorgione` | exists in `js/artists-*.js` |
| year | display `c. 1505`, sort `1505` | Commons `DateTimeOriginal` = "circa 1505"; Wikidata **P571** = 1506. A one-year gap between a circa and a point date; the circa is recorded as the weaker and therefore truer claim |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Giorgione_-_Das_Gewitter.jpg/500px-Giorgione_-_Das_Gewitter.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/The_Tempest_(Giorgione)` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | `["oil-painting"]` | Wikidata **P186** = oil paint, canvas. The artist record's `glazing` and `sfumato` are **not** inherited |
| movements | `["venetian-school"]` | artist record carries `venetian-school` + `high-renaissance`. **`high-renaissance` is deliberately dropped** — it is a Roman-and-Florentine periodisation, and the whole interest of this picture is that it is not doing what Rome was doing. See T-TAXONOMY |
| nation | `italy` | artist record |
| museum | `{ id:"accademia-venice", name:"Gallerie dell'Accademia", city:"Venice" }` — **venue exists** | Wikidata **P195**, first value; **P217** inv. `Cat.915` |
| dims | `82 × 73 cm` | Wikidata **P2048** = 82, **P2049** = 73 (unit Q174728, centimetre). **Sanity-checked** |
| tags | `["landscape","storm","unsettling","nude"]` | §5 vocabulary |
| coords | `{ F:-70, D:+30, E:+25, C:+10, M:-30 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Giorgione*,
`ObjectName` = *La Tempesta*. Source file 3329 × 3696 px. Note the file's
`Credit` field reads simply **"Internet"** — the weakest provenance string of
any file in this batch, and a defect flagged below.

**A bake hazard this record exposes, and it would have shipped silently.**
Wikidata Q930137 carries **three** values for `P195` (collection) — Gallerie
dell'Accademia, **Vendramin Collection**, **Manfrin Collection** — and **two**
for `P276` (location): "Hall VIII" and **"Palazzo Priuli Manfrin"**. Those are a
*provenance chain*, not alternatives: the Vendramin and Manfrin entries are
sixteenth- and nineteenth-century owners. `ARTWORK_SCHEMA.md` §7 plans to bake
`museum` from "P276/P195" with no rule for multiplicity, so a bake taking the
last value, or the first non-empty of P276, would file this painting in a
Venetian palazzo it left in 1856. R3 shows the same shape — five `P276` values
including El Escorial and El Pardo. **See POOL DEFECTS.**

**Consequence, and the limit of what is asserted here.** What is visible in the
object is that the landscape occupies most of the picture and carries its
weather, while the two figures are given no attribute that identifies them and
no action that connects them — a soldier or shepherd standing, a woman nursing,
across a stream, under lightning. A picture with figures and no nameable subject
was not a category Venetian painting had, and the line that runs from here to
every later painting that is a *mood* rather than a story is the reason this work
is in a batch about consequence.

**The reception history is deliberately not summarised.** *The Tempest*'s
identification is one of the most contested in the literature — the readings
proposed for it are numerous and mutually exclusive — and **nothing read this
session establishes any of them**, so none is repeated. The Content Editor
should treat "nobody agrees what it shows" as the sourceable fact and resist the
temptation to pick the most charming candidate. Both of the atlas's own Giorgione
facts are thin: the graph carries one edge,
`["giorgione","titian","befriended"]`, and nothing else.

**Coordinates, on the merits.** Figures are present and legible but subordinate,
and what they are doing is not → `F −70`. A storm is arriving and nobody is
reacting to it; charge without event → `D +30`. Oil on canvas in the ordinary
Venetian way, turned to a purpose the tradition had no category for — the
departure is in the conception, not the handling → `E +25`. Famously
unreadable, which pulls it towards the conceptual, but it does its work on the
eye before the mind gets a turn → `C +10`. Eighty-two centimetres, a private
cabinet picture for one person at a time → `M −30`.

### R5 — `venus-of-urbino`

| field | value | source |
|---|---|---|
| title | Venus of Urbino | Commons `ObjectName` = *Venere di Urbino* / *Venus of Urbino*; Wikidata **Q727875** |
| artistId | `titian` | exists in `js/artists-*.js` |
| year | display `1538`, sort `1538` | Commons `DateTimeOriginal` = 1538; Wikidata **P571** = 1538 (agree) |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg/500px-Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/Venus_of_Urbino` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False`; `Restrictions` empty |
| techniques | `["oil-painting"]` | Wikidata **P186** = oil paint, canvas. The artist record's `glazing` and `impasto` are **not** inherited |
| movements | `["venetian-school"]` | as R4, and for the same reason: the artist record's `high-renaissance` is a Roman-Florentine periodisation |
| nation | `italy` | artist record |
| museum | `{ id:"uffizi", name:"Gallerie degli Uffizi", city:"Florence" }` — **venue exists** | Wikidata **P195**/**P276** = Uffizi Gallery; **P217** inv. `1437` |
| dims | `119 × 165.5 cm` | Wikidata **P2048** = 119, **P2049** = 165.5 (unit Q174728, centimetre). **Sanity-checked** |
| tags | `["nude","interior","tender","everyday-life"]` | §5 vocabulary |
| coords | `{ F:-85, D:-25, E:-20, C:-35, M:-5 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Titian*,
`ObjectName` names the work in six languages, `Credit` = Google Arts & Culture.
Source file 3000 × 2110 px.

**A metadata trap this file walked into and the tool did not.** The Commons
`ImageDescription` for this file reads **"Toilet of Venus"** — a different
Titian composition entirely, and one that exists in several versions. Nothing
else on the page says so; `ObjectName`, `Artist` and the filename all say *Venere
di Urbino*. `match_verdict` returned `confirmed` and was not misled, because it
**deliberately does not consult `ImageDescription`** — the docstring gives the
Emily Carr postage stamp as the reason. This is the first case in either batch
where that design decision was load-bearing in the *helpful* direction, and it
is worth recording as evidence for keeping the rule.

**Consequence, with the descent labelled.** What is in the object: a nude on a
bed in a contemporary domestic interior, meeting the viewer's eye, with two maids
at a chest in the background — the mythological title carried by nothing except
the title. The reclining-nude type this fixes is the one Western painting used
for the next three hundred years. **The specific descent — Velázquez's Rokeby
Venus, Goya's *Maja*, Manet's *Olympia* — is *conventional*** in the sense the
curator brief requires: long-repeated in the literature, and **not sourced in
this session**. It is recorded here as conventional rather than documented, and
the Content Editor should carry that hedge through. The atlas's own graph gives
Titian five outbound edges (`el-greco` taught; `rubens`, `velazquez`,
`rembrandt`, `tintoretto` influenced) — the densest of any artist in this batch,
and, like all 238, unsourced.

**Coordinates, on the merits.** Wholly figurative, near life scale → `F −85`.
Nothing happens; she has been looking at you for a while → `D −25`. Venetian oil
handled with total command and no departure — the radicalism is in the address,
not the means → `E −20`. It works on the body: skin against white linen, fur,
the dog asleep → `C −35`. A metre and a half wide, a private picture for a
bedchamber, however life-size the figure → `M −5`.

### R6 — `lamentation-of-christ-mantegna`

| field | value | source |
|---|---|---|
| id | `lamentation-of-christ-mantegna` | §2 disambiguation: the Lamentation is one of the most-painted subjects in the tradition and the atlas already holds Giotto's, named in his arc |
| title | Lamentation of Christ | Wikidata **Q546297**; the English Wikipedia article title. Commons filename reads *The dead Christ and three mourners* → set `worksKey:"Lamentation of Christ"` and keep the `js/artworks.js` key |
| artistId | `andrea-mantegna` | exists in `js/artists-*.js` |
| year | display `c. 1470–1474`, sort `1470` | **Sources disagree, by thirteen years.** Commons `DateTimeOriginal` = "from 1470 until 1474" with `P580`/`P582` start/end qualifiers; Wikidata **P571** = 1483. The Commons range is recorded; **1483 is noted, not adopted**, and neither is preferred here on any ground except that the range is the weaker claim |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_dead_Christ_and_three_mourners%2C_by_Andrea_Mantegna.jpg/500px-The_dead_Christ_and_three_mourners%2C_by_Andrea_Mantegna.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/Lamentation_of_Christ_(Mantegna)` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | `["tempera"]` | Wikidata **P186** = tempera, canvas. The artist record's `fresco` is **not** inherited |
| movements | `["early-renaissance"]` | artist record |
| nation | `italy` | artist record |
| museum | `{ id:"brera", name:"Pinacoteca di Brera", city:"Milan" }` — **venue exists** | Wikidata **P195**/**P276** = Pinacoteca di Brera; **P217** inv. `352` |
| dims | `68 × 81 cm` | Wikidata **P2048** = 68, **P2049** = 81. **Sanity-checked** — and worth noticing that a picture this famous is smaller than a briefcase is wide |
| tags | `["sacred","mourning","geometry","group-scene"]` | §5 vocabulary |
| coords | `{ F:-80, D:+25, E:+60, C:+25, M:-10 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Andrea
Mantegna*; the artist tie carries the match, since the filename gives a
descriptive title rather than the catalogue one. Source file 2500 × 2076 px.

**Consequence.** The body is laid feet-first towards the viewer and drawn in
extreme foreshortening — the single hardest thing perspective can be asked to
do, and done here on a figure whose proportions are visibly adjusted so that the
feet do not swallow the head. That is a technical demonstration presented as a
devotional image, and the atlas's own graph runs
`["andrea-mantegna","albrecht-durer","influenced"]` to a painter it holds.

**Coordinates, on the merits.** Wholly figurative, and the distortion is
perspectival rather than expressive → `F −80`. A dead body and three weeping
heads: charged, and completely without motion → `D +25`. The foreshortening is
the experiment, and it is the reason the picture exists → `E +60`. It is a
demonstration as much as a devotion, and it knows it → `C +25`. Sixty-eight
centimetres, but staged to confront you at close range → `M −10`.

### R7 — `haboku-sansui`

| field | value | source |
|---|---|---|
| id | `haboku-sansui` | **§2 applied to a work with no settled English title.** Commons `ObjectName` = *Haboku-Sansui, splashed-ink style landscape*; Wikidata **Q28418167**'s English label is *Haboku sansui*; the English Wikipedia article is at *Haboku sansui*; `js/artworks.js` keys it *Haboku (Splashed Ink) Landscape*. Three of the four use the romanised Japanese title, so that is the stable identifier and the slug follows it. Set `worksKey:"Haboku (Splashed Ink) Landscape"` |
| title | Haboku Sansui (Splashed-Ink Landscape) | as above |
| artistId | `sesshu-toyo` | exists in `js/artists-*.js` |
| year | display `1495`, sort `1495` | **Three independent sources agree** — Commons `DateTimeOriginal` = 1495, Wikidata **P571** = 1495, and the English Wikipedia article states it "was made by the Japanese artist Sesshū Tōyō in 1495, in the Muromachi period". The firmest date in this batch |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Sesshu_-_Haboku-Sansui_-_complete.jpg/960px-Sesshu_-_Haboku-Sansui_-_complete.jpg` | `js/artworks.js` |
| image.page | `https://commons.wikimedia.org/wiki/File:Sesshu_-_Haboku-Sansui_-_complete.jpg` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | `["ink-wash","splashed-ink"]` | Wikidata **P186** = ink, paper. The English Wikipedia article calls it "a splashed-ink landscape painting" and "the ink wash painting" — **both technique ids are asserted by a source rather than inherited**, and `splashed-ink` is the work's own name |
| movements | `["zen-painting"]` | artist record; the Wikipedia article on the artist describes work "infused with Zen Buddhist beliefs" |
| nation | `japan` | artist record |
| museum | `{ id:"tokyo-national-museum", name:"Tokyo National Museum", city:"Tokyo" }` — **NEW VENUE** | Wikidata **P195**/**P276** = Tokyo National Museum, **P217** inv. `A-282`; the English Wikipedia article states it is "currently held by the Tokyo National Museum" (two sources agree) |
| dims | `148.6 × 32.7 cm` | Wikidata **P2048** = 148.6, **P2049** = 32.7. **Sanity-checked, and the check is informative:** 148.6 ÷ 32.7 = 4.54, and the source file is 7183 × 31957 px = 1 : 4.45. The stated dimensions and the image proportions agree, which is independent evidence that the file shows the whole scroll and not a crop |
| tags | `["landscape","monochrome","gesture","quiet"]` | §5 vocabulary |
| coords | `{ F:-20, D:+10, E:+50, C:0, M:-35 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Sesshū Tōyō*,
`ObjectName` = *Haboku-Sansui, splashed-ink style landscape*, `Credit` =
**e-Museum**, the Japanese national-institutions portal for designated cultural
properties — the strongest `Credit` in this batch after R3's.

**Heritage designation, recorded as an assertion.** Wikidata **P1435** carries
*National Treasure of Japan* and *Important Cultural Property of Japan*; the
English Wikipedia article states it "is classified as a National Treasure of
Japan". Two sources agree. No primary designation record was read here, and this
document does not go beyond what those two assert. (Batch 01 made the same
qualification for the Korean National Treasure designation at R10; it was right
to.)

**A rendering hazard, not a match failure.** The pool's own derivative at 960 px
wide is **960 × 4271** — a column four and a half times taller than it is wide.
This is the same class of defect Batch 01 recorded for `bada-shanren :: Fish and
Rocks` (a 36789 × 4833 handscroll rendering as a 960 × 126 strip), rotated
ninety degrees. **The difference matters and should be recorded as such:** Bada's
file is unusable because the derivative is unreadable at any layout width, while
this one is the correct proportion of a real hanging scroll and simply needs a
hero that does not assume landscape orientation. It is a layout requirement, not
a reason to reject the file.

**Consequence.** The English Wikipedia article on the artist states that Sesshū
"is considered a great master of Japanese ink painting" and that his work, though
"initially inspired by Chinese landscapes", "holds a distinctively Japanese
style". That is the consequence claim in its sourced form: a Chinese idiom
becoming a Japanese one in a single body of work. *Haboku sansui* is that
argument at its limit — the reduction taken as far as the tradition ever took it.
**The atlas holds Sesshū with zero influence edges**, in either direction; see
COVERAGE EFFECT, where this turns out not to be an accident.

**Coordinates, on the merits.** A cliff, a hut, a boat and two figures survive
inside blots of wet ink that stop describing anything at the top of the sheet;
this is as close to non-figuration as the fifteenth century gets anywhere →
`F −20`. The brush moved fast, the scene is empty and nothing is happening; the
energy is in the making, not the subject → `D +10`. Haboku is the deliberately
most extreme manner available in the tradition, and this is its exemplar →
`E +50`. Neither a thesis nor purely sensory — it is a demonstration of a manner,
which sits at the middle → `C 0`. A metre and a half tall and a third of a metre
wide, hung to be read close → `M −35`.

### R8 — `red-and-white-plum-blossoms`

| field | value | source |
|---|---|---|
| title | Red and White Plum Blossoms | Commons `ObjectName`; Wikidata **Q28154824**; English Wikipedia article title |
| artistId | `ogata-korin` | exists in `js/artists-*.js` |
| year | display `c. 1714–1715`, sort `1714` | **The work is undated, and the sources say so.** Commons `DateTimeOriginal` = "1700/1800" — a century, not a date. Wikidata **P571** = 1715. The English Wikipedia article states the work "is undated" and that "art historian Yūzō Yamane dates the work to 1714 or 1715, just before the artist's death", on the evidence of signature, technique and composition. The display value records the attributed range and the attribution is named; **`sort:1714` is an ordering key, not a date claim** |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_%28National_Treasure%29_-_Google_Art_Project.jpg/500px-Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_%28National_Treasure%29_-_Google_Art_Project.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/Red_and_White_Plum_Blossoms` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | ***omitted*** | **Deliberately.** Wikidata carries **no P186** for this item. The artist record offers `silk-painting`, `gold-leaf` and `ink-wash`: the first is **wrong** — the Wikipedia article states the work is "in coloured pigments on paper" — and the other two are unsourced by anything read here. Blank beats wrong (§7). See T-TECHNIQUE, which proposes the node this record actually needs |
| movements | `["rinpa"]` | artist record, and independently supported: the English Wikipedia article on Rinpa states the style "was consolidated by brothers Ogata Kōrin (1658–1716) and Ogata Kenzan" |
| nation | `japan` | artist record |
| museum | `{ id:"moa-museum-of-art", name:"MOA Museum of Art", city:"Atami" }` — **NEW VENUE** | Wikidata **P195**/**P276** = MOA Museum of Art; the Wikipedia article states it "resides in the MOA Museum of Art in the city of Atami in Shizuoka Prefecture" (two sources agree). **No inventory number** is carried by either |
| dims | `156 × 172.2 cm` **per screen** — see the disagreement below | Wikidata **P2048** = 156, **P2049** = 172.2 |
| tags | `["pattern","flatness","golden","gesture"]` | §5 vocabulary |
| coords | `{ F:-25, D:-20, E:+45, C:-25, M:+30 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Ogata Kōrin*,
`ObjectName` = *RED AND WHITE PLUM BLOSSOMS (National Treasure)*. Source file
4001 × 1757 px.

**Two disagreements, both recorded rather than resolved.**

1. **Dimensions.** Wikidata gives 156 × 172.2 cm with no note of what it
   measures. The English Wikipedia article gives **156.5 × 172.5 cm** and states
   explicitly that this is the measurement of **each screen** of a pair. The
   half-centimetre gap is trivial; **the missing word "each" is not.** A bake
   that prints "156 × 172.2 cm" beside a single image of a two-screen pair states
   something false about the object. Recommend the `dims` string for this record
   read `156.5 × 172.5 cm (each of two screens)` and take the Wikipedia figure,
   because it is the only one of the two that says what it is measuring.
2. **What Kōrin's relation to Rinpa is.** The article on the work says the piece
   is "exemplary of the Rinpa school that Kōrin cofounded"; the article on Rinpa
   says the school "was created in 17th century Kyoto by Hon'ami Kōetsu and
   Tawaraya Sōtatsu" and that "roughly fifty years later, the style was
   consolidated by" Kōrin and his brother. **Those are different claims** —
   founder versus consolidator — made by the same encyclopaedia about the same
   painter. The second is the more specific and the more careful, and it is what
   this document repeats; the first is noted, not adopted.

**Consequence.** The object is a river drawn as flat repeating pattern between
two trees whose bark is mottled by letting wet pigment bleed into wet — a
decorative surface and a described natural fact refusing to be separated. The
sourced consequence claim is the one above: the school this atlas already carries
as a movement id, `rinpa`, was consolidated by this painter. **The atlas holds
Kōrin with zero influence edges**, exactly as it holds Sesshū.

**A technique the atlas cannot name.** The Wikipedia article states Kōrin
"achieved the mottling texture on the trees using **tarashikomi**, a technique in
which the painter applies a second layer of pigment or ink before the first layer
has dried." The registry has no id for it. See T-TECHNIQUE.

**Coordinates, on the merits.** Two trees and a stream, recognisable and
radically stylised — the water is pure pattern with no attempt at water →
`F −25`. Nothing happens; it is spring and it stays spring → `D −20`. The
flattening, the pattern-as-water and the wet-into-wet mottling are all departures
inside a decorative tradition that did not require them → `E +45`. It works
entirely on the eye → `C −25`. A pair of screens over a metre and a half tall —
room-scale, and domestic rather than civic → `M +30`.

### R9 — `oath-of-the-horatii`

| field | value | source |
|---|---|---|
| title | Oath of the Horatii | Commons `ObjectName` (*Le Serment des Horaces*); Wikidata **Q476458** label = *The Oath of the Horatii*; English Wikipedia article at *Oath of the Horatii*, which is also the `js/artworks.js` key |
| artistId | `jacques-louis-david` | exists in `js/artists-*.js` |
| year | display `1784–1785`, sort `1784` | Commons `DateTimeOriginal` = "between 1784 and 1785" with earliest/latest qualifiers; Wikidata **P571** = 1784-01-01. The point date is the low end of the range — the two agree |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Le_Serment_des_Horaces_-_Jacques-Louis_David_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3692_%3B_MR_1432.jpg/500px-Le_Serment_des_Horaces_-_Jacques-Louis_David_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3692_%3B_MR_1432.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/Oath_of_the_Horatii` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | `["oil-painting"]` | Wikidata **P186** = oil paint, canvas. The artist record's `glazing` is **not** inherited |
| movements | `["neoclassicism"]` | artist record |
| nation | `france` | artist record |
| museum | `{ id:"louvre", name:"Musée du Louvre", city:"Paris" }` — **venue exists** | Wikidata **P195** = **Department of Paintings of the Louvre** — see the bake note. **P217** carries *three* values: `INV. 3692`, `MR 1432`, `INV 3692`. The Commons filename independently carries `INV 3692 ; MR 1432`, which is the strongest identifier chain in this batch |
| dims | `330 × 425 cm` | Wikidata **P2048** = 330, **P2049** = 425. **Sanity-checked** |
| tags | `["historical","group-scene","theatrical","monumental-scale"]` | §5 vocabulary |
| coords | `{ F:-85, D:+65, E:-35, C:+55, M:+70 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` =
*Jacques-Louis David*, `ObjectName` = *Le Serment des Horaces*. Source file
10051 × 7794 px.

**A second bake hazard, distinct from R4's.** Wikidata's `P195` here is not
"Louvre" but **"Department of Paintings of the Louvre"** — a sub-organisation.
R10 carries the same value. A bake matching venue-registry slugs against the
`P195` label string will not match `louvre`, and will either drop the museum
field or invent a venue row for a curatorial department. R4's hazard was
*too many* values; this one is *the wrong granularity of one value*. Both are
listed in POOL DEFECTS.

**Consequence.** The object argues by geometry: three sons, three arms, three
swords converging on a single point held by the father, and the women collapsed
in a separate curve to the right so that duty and grief do not share a shape.
Every element that a history painting had been free to arrange for beauty is
here arranged to make a proposition. The atlas's graph carries
`["jacques-louis-david","jean-auguste-dominique-ingres","taught"]` — a
**documented pupillage**, the strongest of the three edge classes and one of the
few in the graph that would survive its own audit — and
`["nicolas-poussin","jacques-louis-david","influenced"]` inbound.

**Coordinates, on the merits.** Wholly figurative, life scale, nothing withheld
→ `F −85`. Maximum tension held perfectly still: an oath at the instant before
it is spoken → `D +65`. The means are academic on purpose — the picture's
argument *is* a return to conventional means, which puts it firmly negative
→ `E −35`. It is a diagram of a moral proposition and makes no secret of it →
`C +55`. Three and a third metres by four and a quarter, pitched at a nation
→ `M +70`.

### R10 — `the-raft-of-the-medusa`

| field | value | source |
|---|---|---|
| title | The Raft of the Medusa | Commons `ObjectName` (*La Balsa de la Medusa*); Wikidata **Q212616**; English Wikipedia article title |
| artistId | `theodore-gericault` | exists in `js/artists-*.js` |
| year | display `1818–1819`, sort `1818` | **Careful.** Commons `DateTimeOriginal` = 1819 and Wikidata **P571** = 1819 — two sources agreeing on a point date. The Commons **filename** carries "1818-19", which is a third statement and *not* a source in the sense the other two are. The display range is taken because two-year execution is what the filename and the general record both indicate; **if a reviewer prefers the strictly-sourced value, use `1819` for both fields** — this is the one date in the batch where this document has taken the looser reading, and it is flagged rather than buried |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/JEAN_LOUIS_TH%C3%89ODORE_G%C3%89RICAULT_-_La_Balsa_de_la_Medusa_%28Museo_del_Louvre%2C_1818-19%29.jpg/500px-JEAN_LOUIS_TH%C3%89ODORE_G%C3%89RICAULT_-_La_Balsa_de_la_Medusa_%28Museo_del_Louvre%2C_1818-19%29.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/The_Raft_of_the_Medusa` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | `["oil-painting"]` | Wikidata **P186** = oil paint, canvas. The artist record's `lithography` and `chiaroscuro` are **not** inherited — the first is a different medium entirely |
| movements | `["romanticism"]` | artist record |
| nation | `france` | artist record |
| museum | `{ id:"louvre", name:"Musée du Louvre", city:"Paris" }` — **venue exists** | Wikidata **P195** = Department of Paintings of the Louvre (same granularity problem as R9); **P217** inv. `INV 4884` |
| dims | `491 × 716 cm` | Wikidata **P2048** = 491, **P2049** = 716. **Sanity-checked** — 4.9 × 7.2 m is extreme but is the correct order for a Salon machine, and it is *the point of the picture*, so a bake rejecting it as implausible would be wrong. The sanity rule proposed in POOL DEFECTS is set wide enough to admit this |
| tags | `["seascape","group-scene","storm","monumental-scale"]` | §5 vocabulary |
| coords | `{ F:-85, D:+85, E:+10, C:+20, M:+90 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Jean Louis
Théodore Géricault*, `ObjectName` = *La Balsa de la Medusa*, and the filename
carries the holding museum. Source file 5872 × 4008 px.

**Consequence.** A contemporary political scandal painted at the scale, and with
the compositional machinery, that the Salon reserved for scripture and antiquity
— a pyramid of the living and the dead straining toward a speck on the horizon,
with no hero, no state, and no moral resolution at the apex. That transfer of
*apparatus* from myth to news is the consequential act, and it is visible in the
object rather than inferred. **The atlas's influence graph carries no Géricault
edge in either direction** — see COVERAGE EFFECT.

**Not asserted.** It is widely repeated that Delacroix posed for one of the
figures. Nothing read here establishes it and the record above does not depend on
it; it is left out, per the same rule that kept Osman Hamdi Bey's features out of
Batch 01's R1.

**Coordinates, on the merits.** Wholly figurative and anatomically insistent →
`F −85`. Among the highest-drama objects the atlas could hold: bodies, a wave, a
sail against the wind, and a sighting → `D +85`. The means are academic history
painting; the departure is what they are pointed at, not how they are handled →
`E +10`. It is an indictment, but it lands in the stomach long before the mind →
`C +20`. Seven metres of canvas; there is no larger register → `M +90`.

### R11 — `a-burial-at-ornans`

| field | value | source |
|---|---|---|
| title | A Burial at Ornans | Commons `ObjectName`; Wikidata **Q540488**; English Wikipedia article title |
| artistId | `gustave-courbet` | exists in `js/artists-*.js` |
| year | display `1849–1850`, sort `1849` | **Commons is used and Wikidata is rejected, which is the reverse of this batch's usual direction and needs saying.** Commons `DateTimeOriginal` = "1849-50.". Wikidata **P571** carries **two values, 1846 and 1841**, which are mutually inconsistent and neither of which matches Commons. An item carrying two contradictory inceptions is not a source that can be preferred over one carrying a single consistent statement |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Gustave_Courbet_-_A_Burial_at_Ornans_-_Google_Art_Project_2.jpg/500px-Gustave_Courbet_-_A_Burial_at_Ornans_-_Google_Art_Project_2.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/A_Burial_at_Ornans` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | `["oil-painting"]` | Wikidata **P186** = oil paint, canvas. The artist record's `palette-knife` and `impasto` are **not** inherited — no source read here asserts either of this canvas |
| movements | `["realism"]` | artist record |
| nation | `france` | artist record |
| museum | `{ id:"musee-dorsay", name:"Musée d'Orsay", city:"Paris" }` — **venue exists** | Wikidata **P195**/**P276** = Musée d'Orsay; **P217** inv. `RF 325` |
| dims | `315 × 668 cm` — **converted, see below** | Wikidata **P2048** = 3.15, **P2049** = 6.68, **unit `Q11573` (metre), not `Q174728` (centimetre)** |
| tags | `["group-scene","mourning","everyday-life","monumental-scale"]` | §5 vocabulary |
| coords | `{ F:-85, D:-15, E:+15, C:+30, M:+85 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Gustave
Courbet*, `ObjectName` = *A Burial at Ornans*, `Credit` = Google Arts & Culture.
Source file 6042 × 2777 px.

**THE UNIT BUG — the most consequential finding in this batch, and it is not
about a painting.** `ARTWORK_SCHEMA.md` §7 specifies baking `dims` from
"P2048×P2049" and §3's example prints a bare `cm` string. **P2048 and P2049
carry a unit qualifier and it is not always centimetres.** This item's values are
`3.15` and `6.68` in **metres** (`Q11573`). A bake that reads the amounts and
appends "cm" — which is precisely what the schema describes — would publish
**"3.15 × 6.68 cm"** for a canvas six and a half metres wide: a Salon machine
rendered as a postage stamp, on a live page, with no error anywhere.

This is a *different and worse* failure than the one Batch 01 found. Batch 01's
`osman-hamdi-bey :: Two Musician Girls` hazard (580 × 390) is a **magnitude**
error, and a plausibility range catches it. This is a **unit** error, and a
plausibility range makes it worse: 3.15 × 6.68 "cm" is a perfectly plausible
size for a miniature, so a magnitude filter would wave it through. The two
findings together give the rule: **read `Q174728` vs `Q11573` from the unit
qualifier and convert, then range-check.** Neither check substitutes for the
other.

**Consequence.** Twenty-odd feet of canvas at the scale the Salon reserved for
coronations, given to a village funeral in which nobody is ennobled, nothing is
composed into a hierarchy, and the open grave is at the viewer's feet in the
foreground. The consequential act is the transfer of scale and seriousness to a
subject that had no claim on either — and unlike R10, which borrowed the
apparatus for a national scandal, this one borrows it for nothing in particular,
which is the more radical move. The atlas's graph runs
`["gustave-courbet","edouard-manet","influenced"]` to a painter it holds.

**Coordinates, on the merits.** Wholly figurative, portrait-accurate, life scale
→ `F −85`. A funeral in which the drama is deliberately withheld — a row of
people waiting → `D −15`. Coarser handling and a darker ground than the Salon
liked, but the scandal was the subject and the size, not the brush → `E +15`.
It is a polemic about who deserves a large painting → `C +30`. Six and a half
metres → `M +85`.

### R12 — `a-sunday-afternoon-on-the-island-of-la-grande-jatte`

| field | value | source |
|---|---|---|
| id | `a-sunday-afternoon-on-the-island-of-la-grande-jatte` | §2 slug of the common English title. Long, and permanent once shipped — flagged for the Implementation Lead to confirm nothing in routing or OG assumes a slug length |
| title | A Sunday Afternoon on the Island of La Grande Jatte | Wikidata **Q1044742**; English Wikipedia article title; the `js/artworks.js` key. The Commons filename reads *A Sunday on La Grande Jatte* — **do not derive the title from the filename** |
| artistId | `georges-seurat` | exists in `js/artists-*.js` |
| year | display `1884–1886`, sort `1884` | Commons `DateTimeOriginal` = "between 1884 and 1886" with earliest/latest qualifiers; Wikidata **P571** = 1884. The point date is the low end of the range — the two agree. Note the Commons **filename** says only "1884" |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/A_Sunday_on_La_Grande_Jatte%2C_Georges_Seurat%2C_1884.jpg/500px-A_Sunday_on_La_Grande_Jatte%2C_Georges_Seurat%2C_1884.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/A_Sunday_Afternoon_on_the_Island_of_La_Grande_Jatte` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | `["oil-painting","pointillism"]` — **the second is inherited, not asserted** | Wikidata **P186** = oil paint, canvas, and supports `oil-painting` only. `pointillism` comes from the artist record. This document has narrowed inherited techniques everywhere else and is **widening** here, deliberately: it is the one field where the atlas would be less truthful for being more cautious. Marked so a reviewer can reverse it. `broken-color` is **not** inherited — it is a different claim |
| movements | `["neo-impressionism"]` | artist record carries `post-impressionism` + `neo-impressionism`. The narrower node is the accurate one for this work, and `post-impressionism` is a retrospective umbrella coined after the fact |
| nation | `france` | artist record |
| museum | `{ id:"art-institute-chicago", name:"Art Institute of Chicago", city:"Chicago" }` — **venue exists** | Wikidata **P195**/**P276** = Art Institute of Chicago; **P217** inv. `1926.224` |
| dims | `207.5 × 308.1 cm` | Wikidata **P2048** = 207.5, **P2049** = 308.1 (unit Q174728, centimetre). **Sanity-checked** |
| tags | `["landscape","group-scene","everyday-life","quiet"]` | §5 vocabulary |
| coords | `{ F:-75, D:-55, E:+60, C:+35, M:+35 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Georges Seurat*,
`ObjectName` names the work, `Credit` = Google Arts & Culture. Source file
**20000 × 13313 px** — the second largest here.

**Consequence.** A colour theory executed as a manufacturing method: separated
dots of unmixed pigment left to combine in the eye rather than on the palette,
applied over two years to a two-by-three-metre canvas of people standing
perfectly still. The consequence is not a mood or a subject but a *procedure*
that other painters could adopt wholesale, and did. The atlas can represent that
lineage without adding anybody: `["georges-seurat","paul-signac","befriended"]`
and `["georges-seurat","camille-pissarro","influenced"]` both point at painters
already in the atlas, and the second is the more interesting edge because it runs
from the younger man to the elder — a Neo-Impressionist conversion rather than a
transmission down a generation. Neither edge carries a source, like all 238.

**Coordinates, on the merits.** Every figure legible, and every figure flattened
into profile or full-face and held rigid — figuration under visible strain →
`F −75`. A frieze in which nothing moves, including the dog → `D −55`. The means
are the invention, and the invention is systematic → `E +60`. It is a theory
being demonstrated at scale, and the archaism of the poses is part of the
argument → `C +35`. Two by three metres — public, but a park rather than a
nation → `M +35`.

---

## NEW VENUES REQUIRED

*Filled as records land. `ARTWORK_SCHEMA.md` §5b: registry additions are cheap
and unreviewed; slug renames are forbidden.*

| venue id | name | city | country | type | needed by |
|---|---|---|---|---|---|
| `santa-maria-novella` | Basilica di Santa Maria Novella | Florence | Italy | **church** | R2 |
| `tokyo-national-museum` | Tokyo National Museum | Tokyo | Japan | museum | R7 |
| `moa-museum-of-art` | MOA Museum of Art | Atami | Japan | museum | R8 |

**Only three, and that is the point of the principle.** Batch 01's
one-per-nation cut needed six new venues for ten records, because spreading
across nations means spreading across collections. Ranking by consequence
concentrates: nine of these twelve records land in venues the registry already
carries (Uffizi ×2, Prado, Accademia Venice, Brera, Louvre ×2, Musée d'Orsay,
Art Institute of Chicago).

**Japan gets its first two venues that hold Japanese painting.** The registry's
only existing Japanese entry is `nmwa-tokyo` — the National Museum of Western
Art. That is the collecting-history point arriving as data for the second batch
running: Batch 01 found Iran and China taking their first catalogued artworks
while staying at zero venues because both works are in New York; this batch finds
that the atlas's one Japanese venue existed for European pictures.

---

## CC-LICENSED IMAGES FLAGGED

**None of the twelve records is CC-licensed.** All twelve return `pd` from
`commons_rights.rights_for_urls`, with `Copyrighted: False` and an empty
`Restrictions` field.

Rather than trust that, **the entire 413-entry pool was swept** — the first
full enumeration of these files by name anywhere in the repository.
`IMAGE_RIGHTS_ROUTES.md` §1.3 gives the counts and names only three of the
twenty; the table below is the whole list, and **the count reproduces exactly**:
385 `pd`, 8 `cc0`, and **20 carrying a live attribution or share-alike
obligation**.

| # | record | licence asserted | obligation |
|---|---|---|---|
| 1 | `andrea-mantegna` :: Camera degli Sposi | CC BY-SA 4.0 | attribution + share-alike |
| 2 | `chaim-soutine` :: Le Petit Pâtissier | CC BY-SA 3.0 | attribution + share-alike |
| 3 | `george-stubbs` :: The Anatomy of the Horse | CC BY-SA 4.0 | attribution + share-alike |
| 4 | `henri-rousseau` :: The Sleeping Gypsy | CC BY 2.0 | attribution |
| 5 | `jacob-van-ruisdael` :: The Windmill at Wijk bij Duurstede | CC BY-SA 4.0 | attribution + share-alike |
| 6 | `jean-honore-fragonard` :: The Swing | CC BY-SA 4.0 | attribution + share-alike |
| 7 | `joaquin-sorolla` :: Vision of Spain | CC BY-SA 3.0 | attribution + share-alike |
| 8 | `joshua-reynolds` :: Mrs Siddons as the Tragic Muse | CC BY 2.0 | attribution |
| 9 | `kathe-kollwitz` :: The Grieving Parents | CC BY 2.0 | attribution |
| 10 | `kitagawa-utamaro` :: Woman Playing a Poppin | CC BY 2.0 | attribution |
| 11 | `lyubov-popova` :: Textile designs, First State Factory | CC BY 2.0 | attribution |
| 12 | `matthias-grunewald` :: The Isenheim Altarpiece | CC BY-SA 3.0 | attribution + share-alike |
| 13 | `max-beckmann` :: Departure | CC BY 2.0 | attribution |
| 14 | `mihri-musfik` :: Self-Portrait | CC BY-SA 4.0 | attribution + share-alike |
| 15 | `nakkas-osman` :: Hünername | CC BY-SA 4.0 | attribution + share-alike |
| 16 | `peter-paul-rubens` :: The Descent from the Cross | CC BY 3.0 | attribution |
| 17 | `peter-paul-rubens` :: The Marie de' Medici Cycle | CC BY 4.0 | attribution |
| 18 | `piero-della-francesca` :: The Legend of the True Cross | CC BY-SA 4.0 | attribution + share-alike |
| 19 | `piero-della-francesca` :: The Resurrection | CC BY-SA 4.0 | attribution + share-alike |
| 20 | `valentin-serov` :: Portrait of Ida Rubinstein | CC BY-SA 4.0 | attribution + share-alike |

All twenty carry `Copyrighted: True`. **None may take the `pd` token.**

**What the full list shows that the counts did not, and it bears directly on
this batch's principle.** Five of the twenty are works that would have ranked
high on a consequence test and are blocked by licence rather than by merit:
**Grünewald's Isenheim Altarpiece**, **both** Piero della Francesca entries,
**Mantegna's Camera degli Sposi**, and **Rubens's Descent from the Cross**. Six
of the twelve painters affected are exactly the kind whose one great work is a
wall or a chapel — and a wall has to be photographed by somebody standing in a
room, which is where a photographer's copyright claim is most defensible and
least like a flat scan. **The licence obligation and the fresco are correlated,
and the correlation systematically biases any pool-drawn batch against
monumental painting in situ.** That is a finding about the pool, not about art
history, and it should be stated wherever the pool's coverage is discussed.

Two entries also intersect other lists: `mihri-musfik :: Self-Portrait` is
simultaneously `IMAGE_RIGHTS_ROUTES.md` B6 (a confirmed mismatch), and
`piero-della-francesca :: The Resurrection`, `henri-rousseau :: The Sleeping
Gypsy`, `jacob-van-ruisdael :: The Windmill` and `kathe-kollwitz :: The Grieving
Parents` are all Group D rendering defects. Batch 01 noted that the §1.3 and
§1.6 lists intersect and neither cross-references the other; **the overlap is
five entries, not one.**

---

## TAXONOMY, TIER AND TECHNIQUE PROPOSALS

### T-TIER — a demotion, proposed plainly, and the structural finding behind it

Batch 01 recorded "no tier change proposed" as a gap rather than a finding,
because a demotion claim would need the existing Tier 1 records read against
each other. **That is now done, and it did not require reading seventy-six
records as prose.** `ARTWORK_SCHEMA.md` §8 states the test itself — a work is
Tier 1 *iff* it belongs to an editorial list, a Tier 1 artist's essential works,
the daily schedule, or the deck pool — so the test can be computed.

**First, two of §8's four routes turn out to be circular.** In the shipped code,
`DAILY_POOL` (`js/app.js:1443`) and `deckPool()` (`js/app.js:3107`) both begin
`CAT.filter(w => w.tier === 1 …)`. They are *derived from* tier and therefore
cannot justify it. §8's operative test reduces to two routes: **an editorial
list, or a Tier 1 artist's arc `works[]`.**

Computed against those two:

| | count |
|---|---|
| Tier 1 records | 76 |
| justified by an arc only | 37 |
| justified by a list only | 2 |
| justified by both | 34 |
| **justified by neither — §8 orphans** | **3** |
| **Tier 2 records that a list or an arc *does* name** | **242** |

**PROPOSED DEMOTION — `beginning-noland`, Tier 1 → Tier 2.**

- It is a §8 orphan: no list, no arc.
- **It has no image.** `image:{ status:"copyright" }` — no `src`, no `page`.
  Kenneth Noland died in 2010, so this is the copyright constraint working
  correctly, not a sourcing failure.
- Consequently it is excluded from `DAILY_POOL` and `deckPool()`, both of which
  require `image.status === "pd"`, so the two derived routes cannot rescue it
  either. It is Tier 1 and reachable by nothing.
- Its `tags` are `["abstract","geometric","quiet","experimental"]`, of which
  **three are not in the §5 vocabulary at all** (see T-TAGS).
- **This is not a judgement on Noland.** Demotion here costs almost nothing:
  §4 makes Tier 2 a real canonical page, promotion is purely additive, and the
  URL never changes. What it buys is that the atlas stops spending a full
  exhibition page on a record with no picture and no way in.

**NOT proposed for demotion, and the reasoning matters more than the verdict.**
The other two orphans are `nocturne-in-black-and-gold` (Whistler) and
`lumber-schooners-penobscot-bay` (Fitz Henry Lane). Both are §8 orphans by the
same computation. **Both should be given an inbound link instead**, because the
defect is in the link graph rather than in the record: the Whistler is the
picture Ruskin was sued over, it carries a `pd` image, an authored description
and hand-scored coords, and it sits at `E +80` — the most experimental coordinate
in the catalog and one the deck needs. Demoting it to make a rule come out even
would be the mirror image of the error the brief forbids. **A rule that would
demote the Whistler is a rule being applied without judgement, and saying so is
the point of having a curator rather than a script.**

**The larger finding, which is not a proposal but should not be buried.**
**242 Tier 2 records are named by a list or a Tier 1 artist's arc** — that is,
§8's "iff" is contradicted by the data seventy-nine times more often in the
promotion direction than in the demotion direction. Tier is not being allocated
by §8. It is being allocated by which records have had a description and three
notice bullets written for them, which is exactly the "allocated by the order
things were built rather than by judgement" the curator brief names. **The honest
repair is to §8's wording, not to 242 records**: either the rule is a *ceiling*
on what may become Tier 1 (in which case say so), or it is a *promise* that
242 records currently break.

**Also a spec/implementation mismatch, per CLAUDE.md §6.**
`ARTWORK_SCHEMA.md` §9 requires "warn: Tier 1 record with zero inbound links".
**`tools/validate.jxa.js` implements no such check** — the three orphans above
are invisible to the suite, which reports `ALL REFERENCES VALID`.

### T-TAGS — the §5 controlled vocabulary is not being enforced, and 130 records are outside it

This is the largest taxonomic defect this batch found and it is squarely a
curatorial one.

`ARTWORK_SCHEMA.md` §5 defines the tag vocabulary as "one flat list … additions
require a PR to this file — **no free-typing**." Checked against the shipped
catalog: **130 of 323 records carry at least one tag outside the vocabulary.**
The validator checks only that a Tier 1 record has ≥ 3 tags
(`tools/validate.jxa.js:106`); **it never checks that a tag is in the list.**

The most frequent off-vocabulary tags, and what they collide with:

| off-vocabulary tag | uses | the vocabulary already has |
|---|---|---|
| `religious` | 41 | **`sacred`** — a straight synonym, splitting one concept in two |
| `night` | 33 | **`nocturne`** — same |
| `abstract` | 21 | **nothing** — a genuine gap, see below |
| `experimental` | 6 | nothing (and it duplicates the `E` coordinate) |
| `geometric` | 6 | **`geometry`** — an inflection, not a new idea |
| `drip`, `dream`, `grief`, `figures`, `body`, `political`, `repetition`, `death`, … | 1–6 each | various |

Three different failure shapes, needing three different fixes:

1. **Synonym splits (`religious`/`sacred`, `night`/`nocturne`,
   `geometric`/`geometry`).** These are pure damage: tag-driven list assembly,
   mood search and "similar artworks" tie-breaking all silently see two
   concepts where there is one, and `sacred` looks 41 records rarer than it is.
   **Fix: normalise to the vocabulary term. No new node.** This is 80 of the
   uses.
2. **`abstract` (21 uses) is a real gap in the vocabulary, not a typo.** §5's
   Form group runs `pattern · geometry · gesture · miniature-scale ·
   monumental-scale · flatness · texture` and has no word for
   non-representational. An atlas holding Kandinsky, Mondrian, Rothko, Pollock,
   af Klint and Noland cannot describe half of what it holds. **Proposed: add
   `abstract` to the §5 Form group by PR**, which is what §5's own governance
   rule requires and what 21 records have already done without it.
3. **The rest are one-off free-typing** and should be normalised or dropped.

**Proposed enforcement:** add a validator check that every catalog tag resolves
in the §5 list. It should ship as an **error, not a warn** — §5 is a governance
rule about a namespace, and a governance rule nobody can breach noisily is not
being enforced at all. Note this will fail the suite on 130 records the moment
it lands, which is the correct behaviour and should be sequenced with the
normalisation, not before it.

### T-TECHNIQUE — `tarashikomi` proposed; and the registry's Western skew

**Proposed: `tarashikomi` (NEW TECHNIQUE).** Applying a second layer of pigment
or ink before the first has dried, so the two bleed into a mottled surface. R8
needs it and the registry has no id for it.

- **Source:** the English Wikipedia article on *Red and White Plum Blossoms*
  states Kōrin "achieved the mottling texture on the trees using tarashikomi, a
  technique in which the painter applies a second layer of pigment or ink before
  the first layer has dried."
- **Kind of category:** a named studio procedure, the same kind of node as
  `sfumato`, `impasto` or `soak-stain` — not a style claim.
- **Scope beyond one record:** it is a defining Rinpa procedure, so it reaches
  Kōrin and the school the atlas already carries as `rinpa`. Batch 01 declined
  `marouflage` on the grounds that one record does not justify a node; that test
  is met here and it was not met there.

**The finding underneath the proposal.** The 39-technique registry carries
`squeegee`, `benday-dots`, `soak-stain`, `dripping`, `frottage`, `spray-paint`
and `photomontage` — seven ids for twentieth-century Western studio procedures,
several of which describe one artist each. Against `ink-wash`, `splashed-ink`,
`silk-painting`, `miniature-painting` and `gold-leaf` for the whole of Asian and
Islamic practice. **The registry is not neutral about which traditions deserve
fine-grained vocabulary**, and R8 is what that costs: a National Treasure whose
`techniques` field had to be left blank because the atlas has no word for what
was done to it. This is the `ATLAS_COVERAGE.md` §2.1 defect appearing in the
technique registry rather than the movement registry, where it has not
previously been recorded.

### T-TAXONOMY — `high-renaissance` dropped from two records, with reasoning

R4 (Giorgione) and R5 (Titian) both use `["venetian-school"]` alone, dropping
the `high-renaissance` their artist records carry.

- `high-renaissance` is a **periodisation of Roman and Florentine practice**
  around Leonardo, Raphael and Michelangelo. Applied to Venice it does not
  describe a shared programme; it borrows a Central-Italian clock.
- Both records are of works whose interest is precisely that they are *not*
  doing what Rome was doing — a picture with no nameable subject, and a nude
  addressed to the viewer in a domestic room.
- **No hierarchy change is proposed.** `venetian-school` exists at top level and
  `high-renaissance` stays in the taxonomy; the defect is application, not the
  node — the same distinction Batch 01 drew for `realism` on Kim Hong-do.
- **This is deliberately a smaller claim than Batch 01's T1.** `pungsokhwa` was
  a European label on a non-European painter. This is a Central-Italian label on
  an Italian painter, which is a much milder error, and it is proposed at the
  artwork level only. **Whether the two artist records should also drop it is
  not adjudicated here.**

### T-NATION — two more anachronistic nation fields, flagged, not fixed

Batch 01's T6 recorded three. Two more, both from this batch:

- **`rogier-van-der-weyden` → `belgium`** (R3). Belgium was founded in 1830;
  Rogier died in 1464 in a Brabantine city under Burgundian rule. The label is
  four centuries early.
- **`hans-holbein` → `germany`** (used by no record here, but the artist record
  drives inheritance). Born in Augsburg, made his career in Basel and London,
  and died in England — in an empire, not a Germany.

Both are the same defect as `matrakci-nasuh → turkey`, which the curator brief
names and which Batch 01 found could not be fixed by editing one field because
`js/taxonomy.js` has no `bosnia`. **These two are worse in one respect and
better in another:** worse because nobody has flagged them (they read as
correct to a modern eye), better because there is no missing node — the honest
answer is that `nation` is a single string being asked to carry a birthplace, a
citizenship and a work's cultural home at once, which `ATLAS_COVERAGE.md` §2.4
already establishes it cannot. **No record in this batch is proposed as a fix.**
R3 uses `belgium` because the artist record says so and overriding it silently
would hide the problem rather than record it.

### T-GRAPH — the influence graph's coverage measured, since two records exposed it

R7 and R8 are both by painters the atlas holds with **zero influence edges in
either direction**, and R10 (Géricault) is a third. That prompted a measurement
rather than an impression:

| | artists | edge endpoints | per artist |
|---|---|---|---|
| European nations | 171 | 354 | **2.07** |
| USA | 34 | 66 | 1.94 |
| **Everywhere else** | **51** | **56** | **1.10** |

**52 of 256 artists have no edge at all.** Japan has 10 artists and 10 edge
endpoints; `iran`, `nigeria`, `south-africa`, `ethiopia`, `colombia`,
`australia` and `czechia` have **zero edges between them**.

Two honest qualifications, because this number is easy to over-read:

1. **A ratio of 2.07 to 1.10 is a real skew but not a chasm**, and part of it is
   a fact about the world rather than about this atlas: transmission inside the
   European tradition is unusually well documented because that tradition wrote
   a great deal about itself, starting with the book this agent is named after.
2. **The edges that do cross traditions almost all run outward to Europe.**
   `["utagawa-hiroshige","vincent-van-gogh","influenced"]` is the pattern — the
   Japanese painter appears in the graph because a European copied him. That
   shape means the graph records Japanese art's *effect on Europe* and not its
   internal lineage, which is why Sesshū, who is the pivot of that internal
   lineage, has no edge.

**No edge is proposed here.** Adding `sesshu-toyo → ogata-korin` would be
inventing a relationship to fix a statistic, and nothing read this session
attests it. The finding is that the graph's silence is patterned, and the repair
is research, not edges.

---

## POOL DEFECTS THIS BATCH FOUND

Six. **All six are in the build path rather than in the images** — which is the
headline: Batch 01 found bad pictures, this batch found that the planned bake
would corrupt good ones.

1. **THE UNIT BUG (R11) — the most serious.** `P2048`/`P2049` carry a unit
   qualifier. Courbet's *A Burial at Ornans* records `3.15` and `6.68` in
   **metres** (`Q11573`), not centimetres (`Q174728`). `ARTWORK_SCHEMA.md` §7
   bakes "P2048×P2049" and §3's example appends `cm`, which would publish
   **"3.15 × 6.68 cm"** for a canvas six and a half metres wide. **A plausibility
   range does not catch this and makes it worse** — 3.15 × 6.68 cm is a perfectly
   plausible miniature. Required fix: read the unit qualifier and convert,
   *then* range-check. Batch 01's `580 × 390` finding and this one are different
   bugs needing different checks; neither substitutes for the other.

2. **Multi-valued `P195`/`P276` are provenance chains, not alternatives (R4,
   R3).** Q930137 (*The Tempest*) lists **Gallerie dell'Accademia, Vendramin
   Collection, Manfrin Collection** for collection and **Hall VIII, Palazzo
   Priuli Manfrin** for location. Q568847 (Rogier) lists five locations
   including **El Escorial** and **El Pardo**. A bake taking the last value, or
   the first non-empty of P276, files these paintings with sixteenth- and
   nineteenth-century owners. §7 has no multiplicity rule.

3. **`P195` granularity: "Department of Paintings of the Louvre" (R9, R10).**
   Both Louvre records give a curatorial sub-organisation, not the museum. A
   slug match against the label string will not find `louvre` and will either
   drop the field or mint a venue row for a department.

4. **`P2048`/`P2049` do not say what they measure (R8).** Q28154824 gives
   `156 × 172.2` for *Red and White Plum Blossoms*; English Wikipedia gives
   `156.5 × 172.5 cm` **for each of two screens**. The number is nearly right and
   the statement is wrong. Any work that is a pair, a set or a polyptych has this
   problem and nothing in the schema records it.

5. **A tall-scroll rendering requirement (R7).** *Haboku sansui* is
   7183 × 31957 px; the pool's 960 px derivative is **960 × 4271**. This is the
   mirror of Batch 01's `bada-shanren :: Fish and Rocks` (960 × 126). **They need
   opposite responses and should not be filed together:** Bada's derivative is
   unreadable at any layout width and the file is unusable; this one is the true
   proportion of a hanging scroll and needs a hero that does not assume landscape
   orientation. Nothing in the pipeline records an aspect-ratio expectation in
   either direction.

6. **Titles must not be derived from filenames (R1, R6, R12).** Three of twelve
   records have a Commons filename that disagrees with the catalogue title:
   *Maestà* for the Ognissanti Madonna, *The dead Christ and three mourners* for
   the Lamentation, and *A Sunday on La Grande Jatte, Georges Seurat, 1884* —
   which also embeds a date narrower than either Commons or Wikidata asserts.
   A quarter of this batch would be mistitled by a filename-derived bake.

**And one non-defect worth recording as evidence.** R5's Commons
`ImageDescription` reads "Toilet of Venus" — a different Titian composition —
while `ObjectName`, `Artist` and the filename all say *Venere di Urbino*.
`match_verdict` returned `confirmed` and was not misled, because it deliberately
does not consult `ImageDescription`. That design decision was justified in the
docstring by a case where reading the field would have caused a **false accept**
(the Emily Carr stamp); this is the first recorded case where it prevented a
**false reject**. It should not be relaxed.

---

## NOT PROPOSED — considered and rejected

| candidate | why rejected |
|---|---|
| `hans-holbein` :: The Ambassadors (germany) | **Screened, `confirmed`, and fully resolved** — Q1212937, National Gallery London, oil on oak panel, 207 × 209 cm, inv. NG1314, Commons and Wikidata both giving 1533. It is the best record in this batch that is not in it. Rejected on the principle: its consequence claim is the English portrait tradition (`["hans-holbein","nicholas-hilliard","influenced"]`), which is a *national school* rather than a change in what painting could do, and the batch had twelve slots. **This is the rejection this document is least confident about**, and it is recorded in full so the next batch can take it in one step |
| `utagawa-hiroshige` :: Sudden Shower over Shin-Ōhashi | **`confirmed`, and rejected on record strength alone — which is uncomfortable, because its consequence is the best-documented in the whole pool.** Van Gogh copied this print in oil, both painters are in the atlas, and the edge `["utagawa-hiroshige","vincent-van-gogh","influenced"]` already exists. But the `image.page` is a Commons file page with no Wikidata link, and a **woodblock print exists in many impressions across many museums**: `wbsearchentities` returns three separate items for this design, two of them keyed to different accession numbers (1921.318, 1985.318). `museum` and `dims` could not be stated for *this* impression without inventing which one it is. Recommended for a later batch **once the print-impression problem has a schema answer** — it is a class problem, not a one-record problem, and every ukiyo-e record will hit it |
| `matthias-grunewald` :: The Isenheim Altarpiece | **CC BY-SA 3.0.** A top-rank consequence candidate blocked by licence, not merit |
| `piero-della-francesca` :: The Resurrection, The Legend of the True Cross | **Both CC BY-SA 4.0**, and *The Resurrection* is also a Group D detail crop. The same block |
| `andrea-mantegna` :: Camera degli Sposi | **CC BY-SA 4.0.** Would have been the stronger Mantegna on consequence — the first fully illusionistic painted room — and R6 is in the batch partly because this one could not be |
| `peter-paul-rubens` :: The Descent from the Cross | **CC BY 3.0**, and it would have collided with R3 on the slug |
| `duccio` :: Maestà | Not screened. Rejected before screening on a records ground that is visible without a lookup: the Maestà was **dismembered** and its panels are dispersed across at least three countries, so `museum` and `dims` describe a fiction for any single file. The Rucellai Madonna would be the tractable Duccio |
| `giotto` :: The Scrovegni (Arena) Chapel frescoes | A cycle, not a work. `dims` and `museum` are meaningless for it; the venue `scrovegni-chapel` already exists and should get a *museum* page rather than an artwork record |
| a second work by any artist in this batch | Not by rule — **the principle imposes no per-artist cap** — but because no artist's second-strongest pool entry outranked another artist's strongest. If one had, it would be here |
| `ito-jakuchu`, `kitagawa-utamaro`, `shen-zhou`, `uemura-shoen`, `theophanes-the-greek` | Considered on the consequence axis and **not screened** — an honest statement of what was and was not done. Theophanes is the most interesting of the five (a documented teaching relationship to Andrei Rublev, which the atlas's graph does not carry) and his single pool entry is a fresco *cycle*, the same problem as Giotto's Scrovegni |
| any work chosen to alter the batch's national distribution | The principle forbids it in both directions. See COVERAGE EFFECT, where the distribution is reported instead |

---

## COVERAGE EFFECT

**The distribution, reported and not corrected.** The twelve records are:

| nation | records |
|---|---|
| italy | 5 (R1, R2, R4, R5, R6) |
| france | 4 (R9, R10, R11, R12) |
| japan | 2 (R7, R8) |
| belgium | 1 (R3) |

**Nine of twelve are European and that is the honest output of the test.**
Three things are true about it at once and none of them cancels the others:

1. **It is inherited.** The pool is 413 images attached to artists this atlas
   already holds, and the atlas's artist list is the residue of the same
   collecting history `ATLAS_COVERAGE.md` §1 describes. A ranking cannot reach
   Song China or Mughal India because no such painter is in the pool to rank.
2. **It was not steered.** Sesshū and Kōrin are here on the same consequence
   test that admits Giotto, not as a correction; Hiroshige was dropped on record
   strength while a fully-resolved Holbein was also dropped, so the marginal
   calls did not run one way.
3. **The licence sweep shows a second, non-obvious filter.** Five of the twenty
   CC-blocked pool entries are exactly the monumental works — Isenheim, both
   Pieros, the Camera degli Sposi, Rubens's *Descent* — whose photographs are
   hardest to argue are flat reproductions. **The pool is biased against
   painting that lives on a wall**, in every tradition, and that is invisible in
   the counts.

**What this batch fixes:**

- Twelve works of the first rank enter the catalog, which Batch 01's
  one-per-nation ceiling structurally could not deliver.
- **Japan gets its first two venues holding Japanese art** — the registry's only
  prior Japanese entry is the National Museum of *Western* Art.
- The catalog gains its **earliest records by a wide margin**: R1 at c. 1300 and
  R2 at 1425–1426.
- Italy's venue coverage deepens with `santa-maria-novella`, the registry's
  first Florentine church.

**What it does not fix, stated as plainly as Batch 01 stated its own:**

- **Not one tradition comes off zero.** Same conclusion as Batch 01, same
  reason: a batch drawn from the pool cannot reach a painter who is not in the
  atlas. Song and Yuan China, Mughal India, Behzād, Jeong Seon, Momoyama Japan,
  historic Africa and Southeast Asia remain absent from the *artist* registry,
  and no catalog batch can touch that.
- **Belarus, and the eleventh zero-nation Batch 01 left open.** Batch 01 left
  Belarus at zero by decision, having declined to file Soutine's Paris pictures
  under it. **This batch does not close that, and should not be read as having
  tried:** it went looking for consequential works, not for the missing nation,
  and Soutine's position has not changed — his other pool entry is CC BY-SA 3.0
  (#2 in the licence table). Belarus is still at zero, still honestly.
- **The Tier 1 record count does not move.** All twelve are Tier 2, and one
  existing Tier 1 record is proposed for demotion, so depth in the atlas goes
  *down* by one page. That is the correct direction: depth was being spent on a
  record with no image and no way in.
- **The influence graph's non-European silence is measured but not repaired.**
  See T-GRAPH.

---

## UNCERTAIN — left standing rather than smoothed

1. **R6's date** — Commons says 1470–1474, Wikidata says 1483, thirteen years
   apart. The range is recorded because it is the weaker claim. Nothing read
   here explains the disagreement, and this document does not claim the range is
   right.
2. **R11's date** — Wikidata carries **two** inceptions, 1846 and 1841, which
   contradict each other and both contradict Commons' 1849–50. Commons is used.
   Why the item carries two is not established.
3. **R10's date range** is the one place this batch preferred a looser reading
   than its sources strictly support: both Commons and Wikidata say 1819, and
   only the filename says 1818-19. The alternative is given in the record.
4. **R8's date is an attribution, not a date.** The work is undated; Yamane's
   1714-or-1715 is named as his, and `sort:1714` is an ordering key.
5. **R8's dimensions and what they measure**, and **R8's relation to Rinpa**
   (cofounder or consolidator) — two claims on which English Wikipedia
   contradicts either Wikidata or itself. Recorded in the record.
6. **R3's Wikidata identification** was reached by search, not by a link. It is
   corroborated by the file's Prado `Credit` and by the item's own description
   string, and it is weaker than the other eleven.
7. **R7 and R8's heritage designations** are what Wikidata and English Wikipedia
   assert. No primary Japanese designation record was read.
8. **R5's descent to Velázquez, Goya and Manet** is recorded as *conventional*
   — long-repeated in the literature, not sourced here.
9. **R4's subject.** *The Tempest*'s identification is contested and no reading
   is repeated here.
10. **R10's Delacroix anecdote** is not asserted.
11. **The consequence judgements themselves.** Each record's consequence
    paragraph rests on what is visible in the object plus, where available, the
    atlas's own influence graph. **Those 238 edges carry no source**, which is
    this curator's own standing finding, so no consequence claim in this document
    rests on an edge alone, and every one says which part is observation and
    which is citation.
12. **Every `pd` token here** records that a Commons file page asserts a
    public-domain basis. It is not a determination by this project, and
    `IMAGE_RIGHTS_ROUTES.md` §0 gives two reasons not to over-trust Commons
    hosting in either direction.
13. **The pool was screened, not looked at.** 393 of 413 entries have never been
    seen by a human, and `IMAGE_RIGHTS_ROUTES.md` §STATE OF VERIFICATION records
    that its 4.8% wrong-image rate is a **floor**, not a measurement. Twelve
    records surviving `match_verdict` is evidence, not proof.

---

## VALIDATOR

`osascript -l JavaScript tools/validate.jxa.js` at commit `cd9ed55`:

```
app.js: syntax OK
artists: 256, movements: 76, techniques: 39, eras: 8, nations: 37,
painter styles: 27, influence edges: 238, venues: 116, catalog: 323
(tier1: 76), daily pool: 75, museum notes: 104, photo credits: 104
(attribution required: 88), artwork image credits: 27, personas: 15,
lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```

This document changes no registry, so the validator's role here is only to
confirm that every id these records reference resolves in the tree as it stands:
the nine existing venues (`uffizi`, `prado`, `accademia-venice`, `brera`,
`louvre`, `musee-dorsay`, `art-institute-chicago`), the twelve `artistId`s, and
the movements and techniques named above. The three new venue ids and
`tarashikomi` do **not** resolve yet, by design — they are proposals, and each
record that uses one cannot be built until its row lands in `js/venues.js` or
`js/taxonomy.js`.

**Read `ALL REFERENCES VALID` with the two gaps this batch found.** The suite
does not implement §9's "Tier 1 record with zero inbound links" warn (three
records qualify), and it does not check tags against the §5 vocabulary (130
records fail). A clean validator run is evidence about references, and it is
being read as evidence about correctness.
