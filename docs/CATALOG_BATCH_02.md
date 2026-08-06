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
