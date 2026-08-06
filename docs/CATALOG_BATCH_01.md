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
| R5 | `three-girls` | Amrita Sher-Gil | india | 2 | `confirmed` | pd |
| R6 | `the-artist-and-his-mother` | Arshile Gorky | armenia | 2 | `confirmed` | pd |
| R7 | `lemminkainens-mother` | Akseli Gallen-Kallela | finland | 2 | `confirmed` | pd |
| R8 | `the-lovers-abbasi` | Reza Abbasi | iran | 2 | `confirmed` | pd |
| R9 | `birds-in-a-lotus-pond` | Bada Shanren | china | 2 | `confirmed` | pd |
| R10 | `ssireum` | Kim Hong-do | korea | 2 | `confirmed` | pd |

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

### R5 — `three-girls`

| field | value | source |
|---|---|---|
| title | Three Girls | Wikidata **Q7797494**. Commons `ObjectName` = *Group of Three Girls* → set `worksKey:"Three Girls"` and keep the `js/artworks.js` key |
| artistId | `amrita-sher-gil` | exists in `js/artists-*.js` |
| year | display `1935`, sort `1935` | Commons `DateTimeOriginal` = 1935; Wikidata **P571** = 1935 (agree) |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Amrita_Sher-Gil_Group_of_Three_Girls.jpg/500px-Amrita_Sher-Gil_Group_of_Three_Girls.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/Three_Girls_(painting)` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False`. Sher-Gil died 1941 |
| techniques | `["oil-painting"]` | Wikidata **P186** = oil paint, canvas; Commons `ImageDescription` says oil on canvas |
| movements | `["post-impressionism"]` | artist record |
| nation | `india` | artist record |
| museum | `{ id:"ngma-new-delhi", … }` — **NEW VENUE** | Wikidata **P195**/**P276** = National Gallery of Modern Art; Commons `ImageDescription` names NGMA, New Delhi |
| dims | `99.5 × 73.5 cm` | Wikidata **P2048** = 99.5, **P2049** = 73.5; Commons `ImageDescription` gives the same pair as "73.5 × 99.5" |
| tags | `["group-scene","quiet","everyday-life"]` | §5 vocabulary |
| coords | `{ F:-85, D:-50, E:+10, C:-20, M:-35 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Amrita
Sher-Gil*. Source file 2184 × 3007 px. The Commons description also records that
the work won a gold medal from the Bombay Art Society; that is what the file
page asserts, and this document does not go beyond it.

**Coordinates, on the merits.** Three seated women, wholly legible → `F −85`.
Nothing happens and nobody looks at anybody → `D −50`. École des Beaux-Arts
training turned on an Indian subject: modern in colour and flattening,
conventional in means → `E +10`. It works by mood and colour rather than by
argument → `C −20`. A metre-high canvas, three figures at close range →
`M −35`.

**A label that survives scrutiny, unlike others in this atlas.**
`post-impressionism` on Sher-Gil is a European movement name on a painter
working in India — the exact shape of the defect `ATLAS_COVERAGE.md` §2.1
records. Here it holds anyway: Sher-Gil trained in Paris and the influence runs
through her own biography rather than being imposed by a cataloguer. That is
the test, and it is why Kim Hong-do under `realism` (R10) fails it.

### R6 — `the-artist-and-his-mother`

| field | value | source |
|---|---|---|
| title | The Artist and His Mother | Commons `ObjectName`; Wikidata **Q64506673** |
| artistId | `arshile-gorky` | exists in `js/artists-*.js` |
| year | display `c. 1926–1936`, sort `1926` | **Sources disagree.** Commons `DateTimeOriginal` = "between 1926 and 1936" and the English Wikipedia article on Gorky reads "*The Artist and His Mother* (ca. 1926–1936)"; Wikidata **P571** = 1931. Two sources give the range and one gives a point date, so the range is recorded and the point date noted, not adopted |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Arshile_Gorky%2C_The_Artist_and_His_Mother.jpg/960px-Arshile_Gorky%2C_The_Artist_and_His_Mother.jpg` | `js/artworks.js` |
| image.page | `https://commons.wikimedia.org/wiki/File:Arshile_Gorky,_The_Artist_and_His_Mother.jpg` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False`. Gorky died 1948 |
| techniques | `["oil-painting"]` | Wikidata **P186** = oil paint, canvas |
| movements | `["modernism"]` | **override.** The artist record carries `surrealism` + `abstract-expressionism`; this work precedes both phases of his development and inheriting them would misdate him |
| nation | `armenia` | artist record — and see below, where the *work* supports it |
| museum | `{ id:"whitney", name:"Whitney Museum of American Art", city:"New York" }` — **venue exists** | Wikidata **P195**/**P276** = Whitney, inv. `50.17` |
| dims | *omitted* | Wikidata carries no **P2048**/**P2049**. Blank beats wrong (§7) |
| tags | `["portrait","mourning","flatness"]` | §5 vocabulary |
| coords | `{ F:-45, D:-25, E:+45, C:+25, M:-5 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Arshile Gorky*,
`ObjectName` = *The Artist and His Mother*, and the Wikidata description names
the Whitney accession. **Source file is only 1024 × 1227 px** — the smallest in
this batch. It is adequate for the 500 px and 960 px renderings the catalog
uses and would not survive a larger hero; flagged in POOL DEFECTS.

**Coordinates, on the merits.** Two figures, frontal, recognisable, but pressed
towards planes and outline → `F −45`. Arrested rather than dramatic; the pair
do not move → `D −25`. The flattening, the scraped and re-laid surfaces, the
refusal to finish over a decade → `E +45`. It is a reconstruction from memory
and from a photograph, and it knows that about itself → `C +25`. Close to
life-scale and frontally formal, which gives presence without scale → `M −5`.

**Why Gorky and not Aivazovsky, for Armenia.** Ivan Aivazovsky is the more
famous Armenian-descended painter in the pool and *The Ninth Wave* has the
tidier record (Wikidata Q1070896, Russian Museum, inv. Ж-2202 — and
`russian-museum` already exists, so it would have cost no new venue). It was
rejected anyway. `ARTWORK_SCHEMA.md` §3 makes an artwork's `nation` a claim
about *work-specific culture*, not about the painter's ancestry, and *The Ninth
Wave* is a Russian-Empire marine painting held in St Petersburg; filing it under
`armenia` would put a national label on a work that does not carry one, purely
to take a counter off zero. Gorky's double portrait is Armenian in its subject:
the English Wikipedia article on Gorky states that the *Artist and His Mother*
paintings "are based on a childhood photograph taken in Van in which he is
depicted standing beside his mother", and that "in the aftermath of the
genocide, his mother died of starvation in Yerevan in 1919." On that record
`nation:"armenia"` is a statement about the painting and not only about the
painter. **Chaïm Soutine was dropped from this batch for the same reason in
reverse** (see NOT PROPOSED).

**Exact-work hazard, handled.** The same Wikipedia article records that *two*
versions of this composition exist — one at the Whitney, "the other … in the
National Gallery of Art in Washington, D.C." Wikidata Q64506673 is described as
the Whitney work and carries inv. `50.17`, which is what ties this file to one
of the two. Any later change to `image.src` for this record must re-establish
which version the new file shows; the title alone cannot.

### R7 — `lemminkainens-mother`

| field | value | source |
|---|---|---|
| title | Lemminkäinen's Mother | Commons `ObjectName`; Wikidata **Q3541051** |
| artistId | `akseli-gallen-kallela` | exists in `js/artists-*.js` |
| year | display `1897`, sort `1897` | Commons `DateTimeOriginal` = 1897; Wikidata **P571** = 1897 (agree) |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Gallen_Kallela_Lemminkainens_Mother.jpg/500px-Gallen_Kallela_Lemminkainens_Mother.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/Lemmink%C3%A4inen's_Mother` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False`. Gallen-Kallela died 1931 |
| techniques | `["tempera"]` | Wikidata **P186** = tempera, canvas — **not** oil, which the artist's default list would have supplied first |
| movements | `["symbolism"]` | artist carries `symbolism` + `art-nouveau`; see TAXONOMY on the missing Nordic node |
| nation | `finland` | artist record |
| museum | `{ id:"ateneum", … }` — **NEW VENUE** | Wikidata **P276** = Ateneum, **P195** = Finnish National Gallery, inv. `A I 640`; Commons `Credit` = kansallisgalleria.fi |
| dims | `85.5 × 108.5 cm` | Wikidata **P2048**/**P2049** |
| tags | `["mythological","mourning","nude","golden"]` | §5 vocabulary |
| coords | `{ F:-80, D:+45, E:+20, C:+10, M:+25 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` =
*Akseli Gallen-Kallela*, `ObjectName` = *Lemminkäinen's Mother*. Source file
2244 × 1770 px, credited to the Finnish National Gallery's own site.

**Note on the collection field.** Wikidata separates the owner (Finnish
National Gallery) from the location (Ateneum). The venue registry is a *venue*
registry (§5b), so `ateneum` is the correct reference and the owning body is not
represented — a small loss the schema accepts by design.

**Coordinates, on the merits.** A woman and a body, both wholly legible →
`F −80`. The subject is a mother assembling her dismembered son beside the
river of the dead: still, but not calm → `D +45`. Tempera revival, flattened
and decoratively bounded, in deliberate opposition to salon oil → `E +20`. It
carries an emblem, but it works on the body first → `C +10`. A metre wide,
pitched at a national-epic register → `M +25`.

### R8 — `the-lovers-abbasi`

| field | value | source |
|---|---|---|
| title | The Lovers | Commons `ObjectName` = *The Lovers*; Wikidata **Q29385121**. `js/artworks.js` keys it *Two Lovers* → set `worksKey:"Two Lovers"` |
| id | `the-lovers-abbasi` | §2: a generic title takes artist disambiguation. Bare `the-lovers` would collide with any later Magritte or Picasso record |
| artistId | `reza-abbasi` | exists in `js/artists-*.js` |
| year | display `1630`, sort `1630` | Commons `DateTimeOriginal`: "dated 8 Shawwal 1039 A.H. / May 21, 1630 A.D." — an inscribed date, the firmest in this batch. Wikidata **P571** = 1630 (agree) |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Reza_Abbasi_-_Two_Lovers_%281630%29.jpg/500px-Reza_Abbasi_-_Two_Lovers_%281630%29.jpg` | `js/artworks.js` |
| image.page | `https://en.wikipedia.org/wiki/The_Lovers_(Abbasi)` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | `["miniature-painting"]` | **narrowed deliberately.** The artist record adds `gouache` and `gold-leaf`; Wikidata carries no **P186** for this sheet and nothing read here states its medium, so the two specific claims are not inherited |
| movements | `["persian-miniature"]` | artist record — an existing non-European node that does describe the work |
| nation | `iran` | artist record |
| museum | `{ id:"met", name:"The Metropolitan Museum of Art", city:"New York" }` — **venue exists** | Wikidata **P195**/**P276** = Metropolitan Museum of Art, inv. `50.164`; Commons `Credit` = "Metropolitan Museum of Art: entry 451023" |
| dims | *omitted* | no **P2048**/**P2049**. Blank beats wrong |
| tags | `["tender","pattern","miniature-scale","golden"]` | §5 vocabulary |
| coords | `{ F:-70, D:-55, E:-55, C:-65, M:-80 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Reza Abbasi*,
`ObjectName` = *The Lovers* with labels in five languages. Source file
4012 × 6088 px. Note that Reza Abbasi's *other* two pool entries are both
excluded: *Portrait of a Dervish* is `IMAGE_RIGHTS_ROUTES.md` A8 (a portrait
*of* him by his pupil Mu'in Musavvir) and *Youth Reading* is Group E, an opaque
serial filename.

**Coordinates, on the merits.** Two figures entwined, entirely legible inside a
flattened idiom that never pretended to depth → `F −70`. Nothing happens but
the touching → `D −55`. Safavid album convention handled at the height of its
tradition; the mastery is not novelty → `E −55`. It is a picture about how a
sleeve feels against a shoulder → `C −65`. An album page, hand-held →
`M −80`.

**Iran stays at zero venues, and that is the finding.** This record takes Iran
off zero *artworks* while leaving the venue registry's Iranian count at nought,
because the only Reza Abbasi in this pool that survives the exact-work check is
in New York. That is `ATLAS_COVERAGE.md` §Gap 3 arriving as data rather than as
an argument: the Golestan Palace and the Reza Abbasi Museum in Tehran hold this
tradition and are absent from the registry; the batch cannot fix that from the
pool it was given.

### R9 — `birds-in-a-lotus-pond`

| field | value | source |
|---|---|---|
| title | Birds in a Lotus Pond | Commons `ObjectName` = *Birds in a lotus pond*. `js/artworks.js` keys it *Lotus and Birds* → set `worksKey:"Lotus and Birds"` |
| artistId | `bada-shanren` | exists in `js/artists-*.js` |
| year | display `1690`, sort `1690` | Commons `DateTimeOriginal` = 1690. No Wikidata item resolves; this is a single-source date and is recorded as such |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Bada_Shanren_%28Zhu_Da%29_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg/500px-…` (full URL in `js/artworks.js`) | `js/artworks.js` |
| image.page | `https://commons.wikimedia.org/wiki/File:Bada_Shanren_(Zhu_Da)_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False` |
| techniques | `["ink-wash"]` | artist record; no **P186** available |
| movements | `["literati-painting"]` | artist record — an existing non-European node that does describe the work |
| nation | `china` | artist record |
| museum | `{ id:"met", name:"The Metropolitan Museum of Art", city:"New York" }` — **venue exists** | Commons `Credit` = Metropolitan Museum of Art; accession `1989.363.135` carried in the filename |
| dims | *omitted* | no source read here states them |
| tags | `["animal","quiet","monochrome","gesture"]` | §5 vocabulary |
| coords | `{ F:-35, D:-30, E:+30, C:+5, M:-45 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Bada Shanren*,
`ObjectName` = *Birds in a lotus pond*, `Credit` = the holding museum, and the
accession number sits in the filename — the strongest identifier chain in the
batch after R8's inscribed date. Source file 3891 × 1840 px.

**Why not *Fish and Rocks*.** Bada's other pool entry (Cleveland Museum of Art
`1953.247`) also returns `confirmed`, and it was rejected on rendering grounds:
the source is a **36789 × 4833 px handscroll**, so the pool's own 960 px
derivative is 960 × 126 — a strip, not a picture. See POOL DEFECTS; this is not
in `IMAGE_RIGHTS_ROUTES.md` §1.6.

**Coordinates, on the merits.** A bird is still a bird, but it is two strokes
and a dot of an eye; the reduction is as far as figuration goes without leaving
→ `F −35`. Empty paper, one perched bird, a sour stillness → `D −30`. Inside
the literati tradition Bada is its individualist extreme, and the reduction was
not the convention he inherited → `E +30`. It works on the eye before the mind
→ `C +5`. Read at arm's length, unrolled → `M −45`.

### R10 — `ssireum`

| field | value | source |
|---|---|---|
| title | Ssireum | Commons `ObjectName` = *Danwon Ssireum*, `ImageDescription` = *Ssireum*. `js/artworks.js` keys it *Ssireum (Wrestling)* → set `worksKey:"Ssireum (Wrestling)"` |
| artistId | `kim-hong-do` | exists in `js/artists-*.js` |
| year | display `18th century`, sort `1780` | Commons `DateTimeOriginal` = **"Unknown date"**. The English Wikipedia article on the album places it in the late Joseon period, 18th century. **`sort:1780` is an ordering key inside Kim Hong-do's working life (1745–1806), not a date claim** |
| image.src | `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Danwon_Ssireum.jpg/960px-Danwon_Ssireum.jpg` | `js/artworks.js` |
| image.page | `https://commons.wikimedia.org/wiki/File:Danwon_Ssireum.jpg` | `js/artworks.js` |
| image.status | `pd` — a rendering token only | Commons asserts a public-domain basis; `Copyrighted: False`. `Credit` points at Korea's `gongu.copyright.or.kr` open-content portal |
| techniques | `["ink-wash","watercolor"]` | the album article states the leaves are "painted with light watercolor on Korean paper". **The artist record's `silk-painting` is not inherited** — this leaf is on paper |
| movements | `["pungsokhwa"]` — **NEW MOVEMENT, see TAXONOMY** | replaces the artist record's `realism`, which is a European label on a Korean painter |
| nation | `korea` | artist record |
| museum | `{ id:"national-museum-korea", … }` — **NEW VENUE** | the English Wikipedia article on *Danwon pungsokdo cheop* states the album is held by the "National Museum of Korea located in Yongsan District, Seoul" |
| dims | *omitted* | no source read here states them |
| tags | `["group-scene","everyday-life","playful"]` | §5 vocabulary |
| coords | `{ F:-85, D:+20, E:-30, C:-40, M:-70 }`, `coordsSource:"override"` | scored below |
| tier | 2 | §8 |

**Verdict.** `match_verdict` → `confirmed`. Commons `Artist` = *Kim Hong-do*,
`ObjectName` = *Danwon Ssireum* (Danwon being his art name, already in the
artist record's display name). Source file 3690 × 4442 px.

**What the sources assert, and what they do not.** The English Wikipedia article
on the album states it is "designated as the 527th National Treasure of South
Korea", that it "contains 25 paintings", and that it is held by the National
Museum of Korea. This document repeats those as **assertions of that article**;
Korea operates more than one heritage register and no primary designation
record was read here. The Commons file page carries no date, no dimensions and
no accession number.

**Coordinates, on the merits.** A ring of spectators and two wrestlers, every
figure legible → `F −85`. A contest at its turning point, played for comedy
rather than violence → `D +20`. Brush convention handled with complete
assurance, on empty paper with no ground and no background — traditional means,
brilliantly used → `E −30`. Observation and warmth carry it; there is no thesis
→ `C −40`. An album leaf → `M −70`.

**A note on the empty region.** Four of this batch's ten records fall below zero
on `E` (R2 −60, R4 −10, R8 −55, R10 −30), which the coordinator flags as
territory the existing 141 scored works barely occupy. None of the four was
moved to get there. Three of them are works whose whole quality is mastery
inside an inherited convention — which is a real and common way for a painting
to be good, and the reason the region is empty is that the atlas has so far
catalogued the European nineteenth and twentieth centuries, where novelty was
the value being chased.

---

## NEW VENUES REQUIRED

*Filled as records land. `ARTWORK_SCHEMA.md` §5b: registry additions are cheap
and unreviewed; slug renames are forbidden.*

| venue id | name | city | country | type | needed by |
|---|---|---|---|---|---|
| `national-museum-warsaw` | Muzeum Narodowe w Warszawie / National Museum in Warsaw | Warsaw | Poland | museum | R2 |
| `kunstmuseum-basel` | Kunstmuseum Basel | Basel | Switzerland | museum | R3 |
| `skagens-museum` | Skagens Museum | Skagen | Denmark | museum | R4 |
| `ngma-new-delhi` | National Gallery of Modern Art | New Delhi | India | museum | R5 |
| `ateneum` | Ateneum Art Museum | Helsinki | Finland | museum | R7 |
| `national-museum-korea` | National Museum of Korea | Seoul | South Korea | museum | R10 |

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
