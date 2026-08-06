# Catalog Batch 01 — one nation at a time

*Vasari (`claude-curator`), 2026-08-06, branch `main`. Specification only.
No `js/catalog-*.js` file is written by this document; the records below are
proposals for the Data Steward and the Implementation Lead to build.*

**Nothing here is a rights determination or legal advice (OD-5).** Where a
licence is named, this document records what the Commons file page **asserts**
and what remains uncertain. The `pd` token in `ARTWORK_SCHEMA.md` §3 is a
rendering flag, not a finding.

---

## THE BATCH PRINCIPLE

**One artwork per nation, for the eleven nations that have artists in this
atlas and zero catalogued artworks.** Selection inside a nation is by strength
of the surviving record and a `confirmed` exact-work verdict from
`tools/audit_artworks.py:match_verdict` — never by fame, and never by how many
pool images a nation happens to hold.

Why this cut. `ATLAS_COVERAGE.md` §1 names four causes for what the atlas
lacks: collecting history, the copyright constraint, the taxonomy, and *nobody
having looked*. Only the last is actionable by this pole, and it is exactly
what the unused pool is: 413 sourced images sitting on artist pages, invisible
to Admire, the taste engine, lists, the deck and the daily painting. Eleven
nations sit at zero. One record each takes them off zero, and the one-per-nation
ceiling is what keeps the batch from becoming an argument for any nation in
particular.

**On neutrality, stated plainly.** Türkiye (15 pool entries) and Poland (15)
are the two largest zero-nations, and they are also the owner's historically
stated preferences. Both facts are true and only the first is a reason. Giving
either nation more than one record would let the collection's history keep
setting the agenda; *excluding* them because of that history would be the same
error with the sign flipped. They get one record each, on the same test as
Korea and Belarus.

---

## THE POOL AS THIS BATCH FOUND IT

| Zero-work nation | Artists with pool images | Pool entries |
|---|---|---|
| Türkiye | 6 | 15 |
| Poland | 5 | 15 |
| Switzerland | 3 | 9 |
| Denmark | 3 | 8 |
| India | 2 | 6 |
| Armenia | 2 | 6 |
| China | 3 | 6 |
| Finland | 1 | 3 |
| Iran | 1 | 3 |
| Belarus | 1 | 3 |
| Korea | 1 | 1 |

Recomputed here from `js/artworks.js` against the `artistId` set in
`js/catalog-*.js` and the artist dump from `tools/dump-artists.jxa.js`
(post-repair, so `artists-16` and `-17` are included). Pool total reproduces at
**413 across 141 artists**.

Excluded before selection: the 30 entries `IMAGE_RIGHTS_ROUTES.md` §1.6 records
as confirmed mismatches or §14 rendering defects. Six of those fall inside these
eleven nations — `seker-ahmed-pasha :: Forest`, `mihri-musfik :: Self-Portrait`,
`levni :: Portrait of Sultan Ahmed III`, `xu-beihong :: Galloping Horse`,
`reza-abbasi :: Portrait of a Dervish`, and `reza-abbasi :: Youth Reading`
(Group E, unresolvable from metadata).

---

## RECORDS

*Appended two at a time as each pair clears `match_verdict` and its factual
claims are sourced. A row is here only when both are done.*

| # | artwork id | artist | nation | tier | verdict | licence asserted |
|---|---|---|---|---|---|---|
| R1 | `the-tortoise-trainer` | Osman Hamdi Bey | turkey | 2 | `confirmed` | pd |
| R2 | `stanczyk` | Jan Matejko | poland | 2 | `confirmed` | pd |
| R3 | `senecio` | Paul Klee | switzerland | 2 | `confirmed` | pd |
| R4 | `sunlight-in-the-blue-room` | Anna Ancher | denmark | 2 | `confirmed` | pd |

**On the tier column.** Every record in this batch is Tier 2. `ARTWORK_SCHEMA.md`
§8 admits a work to Tier 1 only through an editorial list, a Tier 1 artist's
essential works, the daily-painting schedule or the deck pool. None of these ten
artists is in `js/tier1-artists.js`, no list yet reaches them, and manufacturing
an inbound link so that a record could be called Tier 1 is the "make a count come
out even" failure the curator brief forbids. Tier 2 is what the evidence
supports; §4 makes promotion purely additive and the URL never changes.

### R1 — `the-tortoise-trainer`

| field | value | source |
|---|---|---|
| title | The Tortoise Trainer | Commons `ObjectName`; Wikidata **Q7769644** label |
| artistId | `osman-hamdi-bey` | exists in `js/artists-*.js` |
| year | display `1906`, sort `1906` | Commons `DateTimeOriginal` = 1906; Wikidata Q7769644 **P571** = 1906 (agree) |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg/500px-Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/The_Tortoise_Trainer` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons `LicenseShortName` / `UsageTerms` assert a public-domain basis; `Copyrighted: False` |
| techniques | `["oil-painting"]` | Wikidata **P186** = oil paint, canvas |
| movements | `["realism"]` | see TAXONOMY below — the artist record's `orientalism` is *not* inherited here |
| nation | `turkey` | artist record |
| museum | `{ id:"pera-museum", name:"Pera Museum", city:"Istanbul" }` — **venue exists** | Wikidata **P195**/**P276** = Pera Museum; inv. `PM_GAP_PC.045` |
| dims | `221.5 × 120 cm` | Wikidata **P2048**/**P2049**; Commons `ImageDescription` states the same |
| tags | `["interior","quiet","monumental-scale"]` | `ARTWORK_SCHEMA.md` §5 vocabulary |
| coords | `{ F:-85, D:-40, E:-25, C:+45, M:+10 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Osman Hamdi Bey*;
`ObjectName` = *The Tortoise Trainer* in eleven languages. Source file
9492 × 17758 px, `image/jpeg`, from Google Arts & Culture.

**Coordinates, on the merits.** A single standing figure, fully legible →
`F −85`. Nothing happens: the man waits, the tortoises do not hurry →
`D −40`. Paris-academy means, conventionally handled → `E −25`. The picture is
built to be *read* rather than felt — a man in Ottoman dress with a naqareh
drum on his back, training animals that will not be trained — so it sits well
onto the conceptual side, `C +45`. Near life-size on a tall canvas, but the
register is a room rather than a hall → `M +10`.

**Uncertain.** It is widely repeated that the trainer carries Osman Hamdi Bey's
own features. This document does not assert it: no source read here establishes
it, and the record above does not depend on it.

### R2 — `stanczyk`

| field | value | source |
|---|---|---|
| title | Stańczyk | Commons `ObjectName`; Wikidata **Q6609268** |
| artistId | `jan-matejko` | exists in `js/artists-*.js` |
| year | display `1862`, sort `1862` | Commons `DateTimeOriginal` = 1862; Wikidata **P571** = 1862 (agree) |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Jan_Matejko%2C_Sta%C5%84czyk.jpg/500px-Jan_Matejko%2C_Sta%C5%84czyk.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/Sta%C5%84czyk_(painting)` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | `["oil-painting"]` | Wikidata **P186** = oil paint, canvas |
| movements | `["romanticism"]` | artist carries `romanticism` + `realism`; the work is Polish Romantic history painting |
| nation | `poland` | artist record |
| museum | `{ id:"national-museum-warsaw", … }` — **NEW VENUE** | Wikidata **P195**/**P276** = National Museum in Warsaw; inv. `MP 433 MNW` |
| dims | `88 × 120 cm` | Wikidata **P2048**/**P2049** |
| tags | `["historical","interior","lonely","red"]` | §5 vocabulary |
| coords | `{ F:-85, D:+35, E:-60, C:+40, M:-15 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Jan Matejko*,
`ObjectName` = *Stańczyk* with a Polish label naming the full title (the jester
during a ball at the royal court). Source file 5766 × 4289 px. The Commons
`Credit` field records the file as arriving through a GLAM-WIKI partnership
between the National Museum in Warsaw and Wikimedia Polska — which is also the
best evidence for the collection field.

**Coordinates, on the merits.** Fully figurative, one seated man → `F −85`.
The ball behind him is bright and busy while he is not; the drama is withheld
rather than absent → `D +35`. Academic history painting in entirely
nineteenth-century means → `E −60`. It is an argument in paint — the one man in
the room who has read the dispatch — so `C +40`. A single figure, a private
moment, a canvas about a metre wide → `M −15`.

**Placement note (not a reason to change the number).** `E −60` sits in the
region the coordinator flags as nearly empty. It is where the work honestly
falls: nothing about *Stańczyk*'s means is experimental, and its subject being
modern does not make its handling so.

### R3 — `senecio`

| field | value | source |
|---|---|---|
| title | Senecio | Commons `ObjectName` (*Senecio (Baldgreis)*); Wikidata **Q60497141** |
| artistId | `paul-klee` | exists in `js/artists-*.js` |
| year | display `1922`, sort `1922` | Commons `DateTimeOriginal` = 1922; Wikidata **P571** = 1922 (agree) |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg/500px-Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/Senecio_(Klee)` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False`. Klee died 1940 |
| techniques | `["oil-painting"]` | Wikidata **P186** = oil paint, canvas, marouflage — see the medium disagreement below |
| movements | `["expressionism","abstract-art"]` | inherited from the artist minus `der-blaue-reiter`, which the 1922 Bauhaus work postdates; see TAXONOMY |
| nation | `switzerland` | artist record — **contested, see TAXONOMY** |
| museum | `{ id:"kunstmuseum-basel", … }` — **NEW VENUE** | Wikidata **P195**/**P276** = Kunstmuseum Basel, inv. `1569`; Commons `Credit` = Kunstmuseum Basel |
| dims | `40.3 × 37.4 cm` | Wikidata **P2048**/**P2049**; the Commons filename states the same |
| tags | `["portrait","geometry","flatness","playful"]` | §5 vocabulary |
| coords | `{ F:+35, D:-20, E:+65, C:+15, M:-70 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Paul Klee*,
`ObjectName` names the work in German and English. Source file 3712 × 4046 px,
credited to the holding institution.

**Coordinates, on the merits.** A head, still legible as a head, assembled out
of squares and wedges — the abstraction is in the construction, not the subject
→ `F +35`. Nothing moves; the gaze is level → `D −20`. Bauhaus-period
constructive method, colour laid down as a system → `E +65`. It is about
facture and colour relation more than about a person, but it is not a thesis →
`C +15`. Forty centimetres square, a hand-sized panel → `M −70`.

**Medium disagreement, recorded rather than resolved.** The Commons filename
asserts *oil on gauze*; Wikidata **P186** lists oil paint, canvas and
marouflage. These are compatible readings of a gauze support laid down on
board, but they are not the same statement, and the atlas has no `marouflage`
technique id. `["oil-painting"]` is the narrowest claim both support.

### R4 — `sunlight-in-the-blue-room`

| field | value | source |
|---|---|---|
| title | Sunlight in the Blue Room | Commons `ObjectName`; Wikidata **Q18386367** |
| artistId | `anna-ancher` | exists in `js/artists-*.js` |
| year | display `1891`, sort `1891` | Commons `DateTimeOriginal` = 1891; Wikidata **P571** = 1891 (agree) |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg/500px-Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/Sunlight_in_the_Blue_Room` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | `["oil-painting"]` | Wikidata **P186** = oil paint, canvas |
| movements | `["impressionism"]` | artist carries `impressionism` + `realism`; see TAXONOMY on the missing Skagen node |
| nation | `denmark` | artist record |
| museum | `{ id:"skagens-museum", … }` — **NEW VENUE** | Wikidata **P195**/**P276** = Skagens Museum, inv. `222` |
| dims | `65.2 × 58.8 cm` | Wikidata **P2048**/**P2049** |
| tags | `["interior","quiet","everyday-life","blue"]` | §5 vocabulary |
| coords | `{ F:-80, D:-70, E:-10, C:-45, M:-60 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Anna Ancher*,
`ObjectName` = *Sunlight in the blue room*. Source file 7088 × 7958 px from the
Google Cultural Institute at maximum zoom.

**Coordinates, on the merits.** A seated child in a room, wholly legible →
`F −80`. The event of the picture is sunlight reaching a wall → `D −70`. Danish
naturalist means with an impressionist attention to light; the *subject* is
modern, the handling is not → `E −10`. It asks to be felt rather than read →
`C −45`. Sixty-five centimetres, a corner of a house → `M −60`.

**Why Ancher and not Hammershøi.** Vilhelm Hammershøi carries three pool images
and the larger present-day reputation. His two candidate files
(*Dust Motes Dancing in the Sunbeams*, *Interior, Strandgade 30*) returned
`confirmed` but **no Wikidata item resolves from either**, so collection,
inventory number and dimensions would all have had to be asserted without a
source. Ancher's file resolves to a Wikidata item with collection, inventory
number and both dimensions. The choice is record strength, not merit ranking
between the two painters, and not a gender correction — those would each be a
different kind of thumb on the scale.

---

## NEW VENUES REQUIRED

*Filled as records land. `ARTWORK_SCHEMA.md` §5b: registry additions are cheap
and unreviewed; slug renames are forbidden.*

| venue id | name | city | country | type | needed by |
|---|---|---|---|---|---|
| `national-museum-warsaw` | Muzeum Narodowe w Warszawie / National Museum in Warsaw | Warsaw | Poland | museum | R2 |
| `kunstmuseum-basel` | Kunstmuseum Basel | Basel | Switzerland | museum | R3 |
| `skagens-museum` | Skagens Museum | Skagen | Denmark | museum | R4 |

Poland's registry entry is currently the Czartoryski Museum alone, present
because it holds a Leonardo. `national-museum-warsaw` is the first Polish venue
in this atlas that exists for Polish painting. Switzerland has **zero** venues
today; `kunstmuseum-basel` is its first.

---

## CC-LICENSED IMAGES FLAGGED

*Twenty pool entries carry CC BY / CC BY-SA licences with live attribution or
share-alike obligations (`IMAGE_RIGHTS_ROUTES.md` §1.3). Any that surface in
this batch are listed here and are **not** given the `pd` token.*

| record | licence asserted | obligation |
|---|---|---|
| — | — | — |

---

## TAXONOMY, TIER AND TECHNIQUE PROPOSALS

*Filled as records land.*

---

## POOL DEFECTS THIS BATCH FOUND

*Anything wrong that §1.6 did not already record.*

---

## UNCERTAIN

*What could not be established, left standing rather than smoothed.*
