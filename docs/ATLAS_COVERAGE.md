# Atlas Coverage Review

*Vasari (`claude-curator`), 2026-08-06. Branch `main` at `f4440ca`. A coverage
diagnosis, not a proposal: nothing here was added to the atlas. Every count is a
snapshot taken on the date above from `osascript -l JavaScript
tools/validate.jxa.js` and from a direct read of `js/`, and will go stale the
moment someone adds a painter.*

**Validator at time of review:** `ALL REFERENCES VALID` — artists 256 ·
movements 76 · techniques 39 · eras 8 · nations 37 · painter styles 27 ·
influence edges 238 · venues 116 · catalog 323 (tier 1: 76) · daily pool 75 ·
museum notes 104 · personas 15 · lists 12 · tier 1 artists 36.

---

## INTENT

The owner asked what is missing and which way to expand. The honest answer is
that the atlas's largest gap is not a missing region or a missing century. It is
that **210 of 256 artists have no catalogued artwork at all** — so for 82% of
the people in this atlas, there is nothing to Admire, nothing with coordinates,
nothing that enters a list, the daily painting or the onboarding deck. The atlas
has been built wide at the artist layer and narrow at the artwork layer, and the
artwork layer is where the entire product loop lives.

That reframes the question. "Expand the atlas" most plausibly means "add
painters." The evidence says the highest-return move is to finish the painters
already here — and that this is also, by a wide margin, the cheapest way to fix
the regional shape, because the thin regions are precisely the ones stranded at
the artist layer.

---

## 1. THE DIAGNOSIS — what is systematically missing, and why

Four gaps, each with its cause named. The causes matter because only one of them
is actionable by us.

### Gap 1 — The catalog covers 46 artists. The atlas contains 256.

| | count |
|---|---|
| Artists | 256 |
| Artists with ≥ 1 catalogued artwork | **46** |
| Artists with **zero** catalogued artworks | **210** |
| Of those 210, artists that *already carry* public-domain images in `js/artworks.js` | **141** |
| Image entries sitting in `ARTWORKS` for artists with no catalog record | **413** |

The 323-record catalog is drawn from 17 of 37 nations. **Twenty nations have an
artist and no artwork.** Among them: Türkiye (12 artists, 0 works), Poland (7,
0), China (5, 0), India (3, 0), Korea (2, 0), Iran (1, 0), Nigeria (2, 0),
Armenia (2, 0), South Africa (2, 0), Denmark (3, 0), Australia (2, 0).

**Cause: nobody has looked yet.** This is not collecting history and not
copyright. For Türkiye the atlas *already holds 15 sourced public-domain image
records*; for Poland, 15; for Iran, 3; for India, 6; for Armenia, 6. The images
are in the repository. They have never been promoted into `js/catalog-*.js`, so
they render on an artist page and are invisible to Admire, to the taste engine,
to lists, to the daily painting and to every recommendation surface. This is the
single most actionable finding in the review.

**Visitor-facing consequence:** a visitor who arrives loving Ottoman painting
can read about Matrakçı Nasuh and cannot admire a single Ottoman work. The atlas
knows he exists and gives the visitor no way to say so.

### Gap 2 — Whole traditions are absent, not thin.

Verified by grep across `js/` before asserting absence (see NOT ASSERTED WITHOUT
CHECKING, below). Zero records and zero prose mentions for:

- **Song and Yuan Chinese painting.** No Fan Kuan, Guo Xi, Li Cheng, Ma Yuan,
  Xia Gui, Zhao Mengfu, Ni Zan, Huang Gongwang. The atlas's Chinese coverage
  starts at Shen Zhou (b. 1427). Song landscape — roughly 960–1279, contemporary
  with Duccio and Giotto, both of whom the atlas has — is the foundational
  moment of East Asian painting and is not represented by one work or one name.
- **Mughal painting.** No Basawan, Abu'l Hasan, Bichitr, Manohar. India's three
  artists are all 19th–20th century. The word "Mughal" appears once in `js/`.
- **Safavid Persian painting beyond one artist.** Reza Abbasi is the sole
  entry; Kamāl ud-Dīn Behzād, the tradition's central figure, is absent.
- **Joseon Korea before Kim Hong-do.** No Jeong Seon (the "true-view" landscape
  founder), no Shin Yun-bok, no An Gyeon.
- **Japan's Momoyama and Edo schools beyond ukiyo-e and Rinpa.** No Kanō Eitoku,
  Hasegawa Tōhaku, Tawaraya Sōtatsu, Sharaku, Maruyama Ōkyo.
- **Islamic manuscript painting outside the Ottoman/Persian nodes.** No
  al-Wasiti, no *Maqamat*.
- **Historic Africa.** The three African nations in the atlas are represented by
  Ben Enwonwu (b. 1917), Njideka Akunyili Crosby (b. 1983), Gerard Sekoto
  (b. 1913), Marlene Dumas (b. 1953) and Julie Mehretu (b. 1970). There is no
  pre-20th-century African painting of any kind — no Ethiopian church painting,
  which is the obvious candidate and is extensively photographed.
- **Colonial and modern Latin America beyond four countries.** No Cusco School,
  no Torres-García, no Matta, no Reverón, no Tamayo, no Xul Solar.
- **Southeast Asia.** Nothing. No Raden Saleh, no Affandi.

**Cause: mixed, and the mix is the point.** Western collecting history genuinely
explains why these traditions are less famous in an English-language art
education — but it does *not* explain their absence here, because the works are
in public museums with photographed, Commons-hosted collections. Song scrolls
are in the Palace Museum and the National Palace Museum Taipei; Behzād is in the
Golestan and the Bibliothèque nationale; Jeong Seon is in the National Museum of
Korea and the Kansong. **None of those institutions is in the venue registry.**
Copyright does not bind here either: every artist named above died centuries
before 1955. So the cause is the third category — nobody has looked. Collecting
history explains the shape of the *canon we inherited*; it does not excuse the
shape of a 2026 atlas that can reach Commons.

### Gap 3 — The venue registry is where collecting history is doing real work.

116 venues. Twenty-eight are in the United States — more than Italy (15), more
than the United Kingdom, Germany, France and Spain combined at the top of the
list. Türkiye has four, all in Istanbul, all modern institutions; **Topkapı
Palace is not in the registry**, which is to say the atlas has three Ottoman
miniaturists and no record of the building that holds their work.

Poland has exactly **one** venue: the Czartoryski Museum — present because it
holds Leonardo's *Lady with an Ermine*. Poland's only institution in this atlas
exists to serve an Italian painter. The National Museums in Warsaw and Kraków,
which hold essentially the entire Polish canon, are absent.

China: 0. India: 0. Korea: 0. Iran: 0. Egypt: 0. Sub-Saharan Africa: 0. Japan: 1.

**Cause: genuinely collecting history, compounded by nobody having looked.** The
US count is partly honest — American museums really did buy the 20th century,
and the atlas's 20th-century strength follows the collections. But the zeroes
are not collecting history. They are unentered rows in a registry the schema
describes as "cheap and unreviewed" (`ARTWORK_SCHEMA.md` §5b).

### Gap 4 — The atlas names painters it does not contain.

The prose repeatedly reaches for figures that are not nodes. Each of these
appears in an artist record, a Tier 1 arc or a movement description, and has no
record of its own:

| Named in prose | Where | Why the absence bites |
|---|---|---|
| **Andrea del Verrocchio** | Leonardo's `life` and Tier 1 arc | Leonardo's master; the apprenticeship story is told and cannot be clicked |
| **Giovanni Bellini** | Giorgione's and Titian-adjacent records | Taught both Giorgione and Titian, who are both here; the Venetian tree has no root |
| **Jean-Léon Gérôme** | Osman Hamdi Bey's and Şeker Ahmed Paşa's `life` | Taught *both* Ottoman painters in the atlas; the Paris→Istanbul transmission has no European end |
| **Orozco and Siqueiros** | the `muralism` movement description | `muralism` has exactly **one** artist (Rivera); the movement's own copy names the other two |
| **Józef Mehoffer** | Matejko's `career` | Named as one of the three pupils who became Young Poland; the other two are records |
| **Aliye Berger** | Fahrelnissa Zeid's record | `STYLE_GUIDE.md` §6 requires "the Şakir Paşa family treated as the dynasty it is"; one member is a node |
| Cimabue, Ghirlandaio, Pontormo, Filippo Lippi, Simone Martini, the Lorenzetti, Campin, Hobbema, Guardi, Bellotto, Böcklin, Mucha | various | mentioned, not present |

Also absent with no mention at all: Uccello, Antonello da Messina, Carpaccio,
Memling, Hugo van der Goes, Signorelli, Gentile da Fabriano, Pieter de Hooch,
Fabritius, Jordaens, Teniers, Patinir, Avercamp, Cuyp, Bouguereau, Beardsley.

**Cause: nobody has looked yet**, and the atlas itself is telling us where. A
painter named in the prose is a painter the editorial voice already decided
mattered. Every row above is a hole the atlas dug itself.

---

## 2. WHERE THE TAXONOMY MISDESCRIBES ART HISTORY

The two known failures are **symptomatic, not isolated**. They are instances of
three distinct structural defects, and one of them is worse than either example
in the record.

### 2.1 European movement labels applied to non-European painters

Kim Hong-do under `realism` is one of a class. Every case, from the data:

| Artist | Filed under | The problem |
|---|---|---|
| `kim-hong-do` (b. 1745, Joseon) | `realism` | European Realism is a French movement of the 1840s. His own record calls the work "genre albums" and names "the 'Danwon style'" — the taxonomy has no node for either |
| `qi-baishi` | `literati-painting`, `realism` | the second label adds nothing a Chinese term would not say better |
| `park-soo-keun` | `realism`, `naive-art` | `naive-art` on a deliberate, trained modernist |
| `raja-ravi-varma` | `realism`, **`orientalism`** | see 2.2 |
| `osman-hamdi-bey` | **`orientalism`**, `realism` | see 2.2 |
| `seker-ahmed-pasha` | `realism`, **`orientalism`** | see 2.2 |
| `gerard-sekoto` | `expressionism`, `realism` | |
| `tsuguharu-foujita` | `expressionism` | the real label is School of Paris; no such node exists |

`xu-beihong` under `realism` is the one defensible case — he trained in Paris
and consciously imported academic realism. That is a documented transmission,
not a misfit, and it shows the labels are not wrong *by rule*. They are wrong
when no non-European node exists to be right.

### 2.2 `orientalism` applied to the painters it was coined about

**This is a sharper failure than Kim Hong-do and it is not in the record yet.**
Orientalism as a movement term denotes European painters depicting an imagined
East. The atlas has three artists tagged `orientalism`. Two are Ottoman and one
is Indian. The term's definition requires the painter to be an outsider; filing
Osman Hamdi Bey under it inverts its meaning.

The atlas already knows this. Osman Hamdi Bey's tagline reads *"The Tortoise
Trainer — Orientalism, corrected from the inside"* and his `career` field says
he *"used Orientalism's own polished technique to overturn its clichés."* **The
editorial voice argues he subverted Orientalism while the `movements` array
files him as one of them.** Wikipedia's article records the same debate as
live — that his work is read both as continuing his teachers' style and as
"subversive and critical of European orientalism" — which is exactly the kind of
scholarly dispute OD-5 requires us to carry rather than flatten into a chip.

Recommended change: introduce a distinct movement node for late-Ottoman /
non-European academic painting (working name **Ottoman Westernist painting**,
covering Şeker Ahmed Paşa, Osman Hamdi Bey, Hoca Ali Rıza and the 1914
Generation), and reserve `orientalism` for European painters — of whom the
atlas currently has **none**, another finding in itself.

### 2.3 The movement hierarchy encodes internal differentiation only for Europe

Every non-Western tradition in the tree is a **root with no children**:
`literati-painting`, `ukiyo-e`, `rinpa`, `nihonga`, `zen-painting`,
`ottoman-miniature`, `persian-miniature`, `icon-painting`, `muralism`.

Meanwhile `renaissance` has seven children, `abstract-art` six, `realism` four
plus a grandchild, `expressionism` four, `post-impressionism` three,
`romanticism` a child and a grandchild.

The consequence is not cosmetic. `literati-painting` is a single flat node
covering roughly nine centuries and several named schools. Shen Zhou (b. 1427,
founder of the Wu School) and Bada Shanren (b. 1626, a Ming-loyalist
Individualist) receive the identical label, while the atlas cheerfully
distinguishes `washington-color-school` from `color-field`. That asymmetry is a
curatorial statement about which traditions have internal history, and it is not
one we mean to make.

Also: `renaissance` has **zero** artists — it is a pure container — while
`muralism`, `superflat`, `persian-miniature`, `zen-painting`, `constructivism`,
`suprematism`, `de-stijl` and eleven others have exactly one.

### 2.4 `nation` is a single string, and it cannot carry the truth

**This is a schema constraint and I am reporting it as a finding, not routing
around it.** `docs/STYLE_GUIDE.md` §3.3 and §7 already state the correct policy —
*"primary filing + acknowledgment"*, "contested identities are stated as
contested." The prose honors it. The data model has no field in which to put the
acknowledgment, so `js/app.js` renders a single flag-and-name chip on the artist
page, the artwork page and the world map. **The policy is honored in prose and
violated on every derived surface.**

Cases where the single string is demonstrably false or misleading, all from the
shipped data:

| Artist | `nation` | What the record itself says |
|---|---|---|
| `matrakci-nasuh` | `turkey` 🇹🇷 | born in Visoko, Bosnia, to Bosnian Muslim parentage, of Ottoman service; his own record says "Nasuh of Visoko". Türkiye is a 1923 republic; he died c. 1564 |
| `osman-hamdi-bey` | `turkey` 🇹🇷 | Wikipedia describes him as an **Ottoman Greek** who "was extremely proud of his Greek descent" — the filing is wrong on polity *and* arguably on ethnicity |
| `nakkas-osman`, `levni` | `turkey` 🇹🇷 | 16th and 18th century Ottoman court painters |
| `kazimir-malevich` | `ukraine` 🇺🇦 | his own `facts` field: *"Both Ukraine and Russia claim him"*; his `life` says "born near Kyiv to a Polish family" |
| `arshile-gorky` | `armenia` 🇦🇲 | born near Lake Van in the Ottoman Empire, entire career in New York, central to Abstract Expressionism |
| `ivan-aivazovsky` | `armenia` 🇦🇲 | born in Crimean Feodosia, official painter of the Russian Navy; never lived in Armenia |
| `jan-matejko` and six others | `poland` 🇵🇱 | his own `life` field: *"Born in Kraków when Poland existed only in memory — partitioned off every map."* The `young-poland` movement blurb says *"With Poland erased from the map."* The atlas's prose knows the state did not exist; the nation field asserts it |
| `el-greco` | `greece` 🇬🇷 | the Greece nation blurb concedes it: *"Two Greeks who transformed other nations' art"* |
| `leonora-carrington` | `mexico` 🇲🇽 | born in Lancashire, England |
| `tsuguharu-foujita` | `japan` 🇯🇵 | became a French citizen, died in France |
| `fahrelnissa-zeid` | `turkey` 🇹🇷 | Ottoman-born, married into the Iraqi royal house, lived Baghdad/London/Paris/Amman, died in Jordan |
| `amrita-sher-gil` | `india` 🇮🇳 | born in Budapest, Hungarian mother, trained in Paris |

**What I would change.** Not the primary filing — `nation` should stay a single
string, because it is shipped infrastructure, it drives the map and the routes,
and renaming or re-typing it is a migration with no product payoff. The defect
is the *absence of the second field*, and the fix is additive and cheap:

- add an optional `nationNote` (short string, ≤ 100 chars, authored) rendered
  beside the nation chip — *"Ottoman Empire; born in Bosnia"*, *"claimed by
  Ukraine, Russia and Poland"*, *"Ottoman-born; French citizen from 1955"*;
- add an optional `alsoNations: []` for map and index membership only, never for
  the primary chip;
- treat the flag emoji as the sharpest offender: a 🇹🇷 flag on a man who died
  in 1564 is a claim the prose would never make, and suppressing the flag where
  `nationNote` exists is a one-line rendering rule.

That is a UX/implementation decision, not mine to make — I am recording that the
schema cannot currently express what the Style Guide requires, and that roughly
**twelve shipped records are visibly wrong on a surface a visitor sees.**

### 2.5 Eras and techniques — the parts that work

Worth saying plainly, because two of four axes are sound. The eight eras are
centuries, and a century is a century everywhere; they carry non-Western art
without distortion. The 39 techniques are the most honest axis in the taxonomy —
`ink-wash`, `splashed-ink`, `silk-painting`, `woodblock`, `miniature-painting`,
`gold-leaf` are genuinely non-European and properly parented. The failure is
concentrated in `movements` and `nation`. The eras' only real limit is that they
cannot say "Edo", "Joseon", "Ming" or "Safavid" — a real loss of texture, but a
low priority next to the two defects above.

---

## 3. THE SHAPE

### Where the atlas is deepest — and whether that is where a visitor needs it

The deepest single cluster is the **New York School**: fourteen painters born
1899–1930 working in Abstract Expressionism, Color Field and Pop, plus Hans
Hofmann filed under Germany. The United States has 34 artists, second only to
France's 40, and 28 of the 116 venues.

That depth is real and defensible — it is where 20th-century collecting
happened. But it is also where copyright bites hardest: **66 of 323 catalogued
works are `status:"copyright"` and cannot render an image**, and 28 of those 66
are American, 18 Spanish, 9 Mexican. So the atlas's deepest region is also its
most image-suppressed. **Cause: the public-domain constraint, correctly
applied.** That one is not fixable by looking harder.

### Centuries

| Born | Artists | | Catalogued works dated | |
|---|---|---|---|---|
| 13th | 2 | | 15th c. | 29 |
| 14th | 5 | | 16th c. | 47 |
| 15th | 18 | | 17th c. | 45 |
| 16th | 24 | | **18th c.** | **5** |
| 17th | 17 | | 19th c. | 104 |
| 18th | 25 | | 20th c. | 93 |
| 19th | 109 | | | |
| 20th | 56 | | | |

**The 18th century is the atlas's hole.** Twenty-five painters born, and five
catalogued artworks — one of which carries coordinates. Watteau, Chardin,
Boucher, Fragonard, Tiepolo, Canaletto, Piranesi, Hogarth, Reynolds, Stubbs,
Gainsborough, Wright of Derby, Vigée Le Brun, Kauffman, Rosalba Carriera and
Goya are all present as artists and effectively absent as art. **Cause: nobody
has looked yet** — the century is comprehensively public domain and
comprehensively photographed. This is the cheapest correction in the review
after Gap 1, and it is the same correction.

### Women

44 of 256 artists (17%) — strong for an art-historical atlas, and clearly the
product of deliberate work. But:

- **4 of 36 Tier 1 artists (11%)** are women: Artemisia Gentileschi, Frida
  Kahlo, Hilma af Klint, Mary Cassatt. Depth lags breadth.
- By birth century the weakest band is the **18th (2 of 25, 8%)** — Vigée Le Brun
  and Kauffman. Labille-Guiard, Therbusch, Marguerite Gérard, Ulrika Pasch and
  Constance Mayer are all absent, all public domain.
- Zero women born before 1532.

**Cause: mostly collecting history, partly nobody having looked.** The 18th
century band is the actionable part.

### Non-court, non-academy makers

Thin by construction. The atlas is overwhelmingly a record of court painters,
academicians and gallery modernists. Emily Kame Kngwarreye is the only
Indigenous artist and, notably, the atlas's only entry from a tradition without
a Western institutional pipeline. Folk, votive, guild, workshop-anonymous and
devotional painting is essentially unrepresented, which is a defensible editorial
choice for a taste product built on named identification — but it should be
named as a choice rather than left as an accident.

### The influence graph: a Eurocentric spine with appendages

238 edges — `influenced` 133, `befriended` 57, `taught` 30, `rivaled` 14,
`partners` 4. 204 of 256 artists are touched by at least one edge; **52 are
isolated**.

Only **39 of 238 edges touch a non-Western nation at all**, and the internal
structure of those 39 is the finding:

- Most are **intra-national closed loops** — Turkey→Turkey (6), China→China (4),
  India→India (2), Japan→Japan (1). Real, but they connect a tradition to itself.
- Most of the rest are **spokes off a European hub.** Picasso alone accounts
  for four of them (Gorky, Lam, Zhang Daqian, Abidin Dino). Picasso has degree
  18, the highest in the graph.
- **There is not one edge between two different non-Western traditions.** No
  China→Korea, no China→Japan, no Persia→Ottoman, no Persia→Mughal. Those are
  among the best-documented transmissions in world art — Chinese literati
  painting is the direct parent of Korean and Japanese ink painting; Persian
  manuscript painting is the direct parent of both the Ottoman and Mughal
  workshops. The atlas records Japan→Europe (Hokusai and Hiroshige to Van Gogh
  and Monet, Utamaro to Cassatt) but never Asia→Asia.

So the answer to the question as posed: **it is a Eurocentric spine with
appendages**, and the appendages attach only at European joints. The single
cheapest structural repair in this entire review is a dozen well-sourced
Asia→Asia edges.

One caution the role requires me to repeat: **all 238 edges carry a type and no
source.** I did not audit them individually in this pass. The `zurbaran`/
`caravaggio` case already in the record — where Wikipedia says it is unknown
whether Zurbarán had the opportunity to see Caravaggio's paintings, and the edge
asserts influence anyway — should be assumed to have siblings. Any expansion that
adds edges should add a `basis` field at the same time; retrofitting 238 later
costs more than adding it to 250 now.

### What an expansion does to the taste engine

Recorded, not solved — the mathematics belongs to a future role.

141 of 323 works carry coordinates. Confirmed independently: **F×E = +0.60**,
E mean **+44.4** with only **2 of 141 works at E ≤ −40**. The F×D quadrants run
76 figurative-dramatic / 31 figurative-calm / 22 abstract-dramatic / **12
abstract-calm** — the calm-abstract shortfall `PIGMENT.md` §15.3 already flags.

The art-historical cause of the F×E correlation is worth naming, because it
bears directly on the recommendation. The coordinate-carrying corpus is 74/141
twentieth-century and drawn almost entirely from Europe and America. In that
corpus, *abstract* and *experimental* are the same historical event — European
modernism, 1900–1970. There is no body of work in the atlas that is formally
abstract and art-historically classical.

Such a body exists, and it is exactly what the owner has asked for. Ottoman and
Persian miniature, Islamic geometric ornament, Chinese calligraphic ink and
Joseon court painting are non-illusionistic, flat, patterned — and simultaneously
the most rule-bound, canonical, tradition-governed painting on earth. They are
the natural inhabitants of the empty region: high F, low E. **The content that
would most decorrelate F and E, and populate the E ≤ −40 anchor the deck lacks,
is the content the owner already wants.** That is a genuine convergence and not a
rationalization; I flag it as an implication for whoever owns the taste math, not
as a licence to score works to fill a gap. Coordinates get scored on the merits
of the work, per the role's constraint and `ARTWORK_SCHEMA.md`.

---

## 4. DIRECTIONS, RANKED

Three coherent directions. Tier costs follow `PIGMENT.md` §7: Tier 1 artist =
exhibition profile with arc; Tier 2/3 = correct taxonomy and clean content;
Tier 1 artwork = description, three notice bullets, explicit coordinates,
provenance, related; Tier 2 artwork = thin canonical page.

---

### ▶ DIRECTION A — *Finish the painters you already have.* **(recommended)**

**What it adds.** No new artists. Promote existing, already-sourced images into
`js/catalog-*.js`, prioritised by what is most broken.

- **~120 new catalogue records** drawn from the 413 image entries already in
  `js/artworks.js` belonging to artists with no catalog record.
- Priority order, by damage repaired: Türkiye (12 artists → ~15 works) ·
  Poland (7 → ~15) · the 18th century (~16 artists → ~30 works) · China, India,
  Korea, Iran, Armenia (13 → ~22) · Denmark, Finland, Czechia, Hungary,
  Australia, Canada (~12 → ~20).
- **Tier split: roughly 30 Tier 1, 90 Tier 2.** Tier 2 is the point — thin
  canonical pages give every work a URL and an Admire button, which is all that
  is needed to end the "no way to admire this tradition" problem.
- ~15 venue registry additions (Topkapı, National Museum Warsaw, National
  Museum Kraków, National Museum of Korea, National Palace Museum Taipei,
  Palace Museum Beijing, Golestan, and the holders of specific works).
- Taxonomy repair shipped in the same pass: the `orientalism` correction (2.2),
  1–2 non-European movement nodes, and the `nationNote` proposal handed to UX.

**What it costs.** The smallest of the three by a wide margin. The images are
sourced and in the repository; the work is per-record authoring (50–80 word
description, three notice bullets, coordinates for Tier 1) plus verification that
each Commons URL depicts the exact work. Roughly 30 authored Tier 1 records is
the real expense; the 90 Tier 2 promotions are close to mechanical.

**How much can carry a real photograph.** Nearly all of it. Every artist in the
priority list died well before 1955 except the modern Turkish and Polish
generations, where it is a per-artist judgement (Fikret Mualla d. 1967, Abidin
Dino d. 1993, Burhan Doğançay d. 2013, Beksiński d. 2005, Lempicka d. 1980 are
generative-cover or suppressed-image cases; Matrakçı, Nakkaş Osman, Levni, Şeker
Ahmed, Osman Hamdi, Çallı, Matejko, Malczewski, Boznańska, Wyspiański are not).

**What it fixes.** Gap 1 outright. The Türkiye and Poland zeroes — the owner's
two named priorities — become real, admirable coverage rather than reading
matter. The 18th-century hole. Most of Gap 3. It puts the first non-European
coordinates into the taste space, which is the only content intervention that
addresses the F×E correlation.

**What it does not fix.** Gap 2 — Song, Yuan, Mughal, Joseon-before-Kim,
historic Africa and Southeast Asia stay absent, because you cannot catalogue a
painter you do not have. It does not fix the influence graph's Asia→Asia
vacuum. It does not add a single new name to the atlas, which means it will not
*feel* like expansion on the artist index even though it roughly triples what a
visitor can actually do.

---

### ▶ DIRECTION B — *Fill the structural absences.*

**What it adds.** ~25–30 new artists chosen to close whole traditions rather
than lengthen existing lists: Song and Yuan China (Fan Kuan, Guo Xi, Ni Zan,
Huang Gongwang) · Behzād · Mughal (Basawan, Abu'l Hasan, Bichitr) · Joseon
(Jeong Seon, Shin Yun-bok) · Momoyama/Edo Japan (Sōtatsu, Tōhaku, Kanō Eitoku,
Sharaku) · Ethiopian church painting · Raden Saleh · Torres-García, Matta,
Tamayo, Orozco · plus the 15–20 Asia→Asia and Persia→Ottoman/Mughal influence
edges that finally make the graph a network.

**What it costs.** The largest. New artist records need the full required field
set (`life`, `career`, `outside`, ≥ 3 `facts`, ≥ 3 `works`, palette, a `style`
matching an existing painter function in `js/app.js`) plus taxonomy nodes that
do not yet exist — Song landscape, Mughal, Joseon genre and true-view painting
have no movement to be filed under, and inventing them properly is the hardest
curatorial work in this document. Realistically **4–6 Tier 1 at most, the rest
Tier 2/3**, and it needs new generative painter styles or it will look wrong.

**How much can carry a real photograph.** Almost all of it — every name above
except the Latin American moderns died centuries before 1955, and the holdings
are photographed. Siqueiros (d. 1974) is a generative-cover case; Orozco
(d. 1949) is not.

**What it fixes.** Gap 2, which is the gap most visible to anyone who tries to
read this as a world atlas. It makes the influence graph a genuine network. It
is the only direction that changes what the atlas *is* rather than how much of
it works.

**What it does not fix.** Anything in Gap 1 — it adds 25–30 more artists to the
210 who have nothing to admire, and if done alone it makes the ratio worse. It
does not touch Poland or the 18th century. It is also the direction most likely
to produce records the atlas cannot honestly support: for several of these
figures the biographical record is thin, disputed, or legendary, and a "figure a
visitor can identify with" is exactly what a 12th-century Chinese landscapist
does not readily supply.

---

### ▶ DIRECTION C — *Repair the European spine.*

**What it adds.** ~20 artists the atlas already names in its own prose or
obviously implies: Verrocchio, Giovanni Bellini, Cimabue, Ghirlandaio, Uccello,
Antonello da Messina, Carpaccio, Memling, Pontormo, Guardi, Bellotto, Gérôme,
Bouguereau, de Hooch, Fabritius, Jordaens, Mehoffer, plus the
Polish 19th century (Chełmoński d. 1914, the Gierymski brothers, Podkowiński,
Wyczółkowski) and the late-Ottoman generation (Hoca Ali Rıza d. 1930, Halil
Paşa, Lifij, Nazmi Ziya, Namık İsmail).

**What it costs.** Moderate. These are the best-documented painters on earth;
sourcing is fast, images are abundant, and every one fits an existing movement
node and an existing painter style. Mostly **Tier 2, with 3–4 Tier 1**.

**What it fixes.** Gap 4 and the broken-hinge problem — Leonardo's master,
Titian's master, and the teacher shared by both Ottoman painters all become
clickable, which is the strongest thing that can be done for the influence graph
per unit of effort. It substantially strengthens Poland and Türkiye, both named
priorities.

**What it does not fix.** It makes the Eurocentric shape *more* pronounced in
raw count, and it does nothing at all for Gap 2 or the F×E correlation. It is
the safest direction and the least interesting one.

---

### WHICH I WOULD CHOOSE

**Direction A, with Direction C's Polish and Turkish artists folded in as a
second wave, and Direction B deferred to a distinct later objective.**

The reasoning:

1. **The binding constraint is not breadth, it is that 82% of the atlas is
   inert.** Adding painters to a product where four in five painters have
   nothing to admire optimises the number a visitor can count and not the thing
   a visitor can do. `PIGMENT.md` §18 is explicit that a change is not good
   merely because it adds more entities, and §16 says the most useful next work
   is not simply "more data." Direction A is the only one of the three that
   obeys both.

2. **It serves the owner's stated priorities faster than the direction that
   looks like it serves them.** He asked for strong Turkish/Ottoman and Polish
   coverage. Both already exist at the artist layer — twelve Turkish painters,
   seven Polish — and both are completely absent from the artwork layer. The
   fastest route to "strong Turkish coverage" is not more Turkish painters; it
   is making the twelve already here admirable, which the atlas can do with
   images it already holds.

3. **It is the cheapest per unit of repair by a factor of several.** 413
   sourced image records are sitting unused. No other direction has its raw
   material already in the repository.

4. **It is the only direction that touches the taste engine's known defect.**
   Ottoman miniature, Persian miniature and Chinese ink are flat and
   non-illusionistic while being deeply classical — the empty high-F/low-E
   region. Direction C adds more European figurative-classical work, which
   deepens the existing correlation. Direction B would help, but only after the
   much larger cost of creating the artists first.

5. **Direction B is right and should not be done now.** Song and Yuan painting
   is the largest genuine absence in this atlas and I do not want that
   sentence softened. But it needs new movement nodes, new painter styles, new
   venue records and a serious answer to "who is the figure a visitor identifies
   with here" — and doing it on top of an atlas where nothing is catalogued
   would produce another twenty-five artists with nothing to admire. It is a
   flagship objective, not a wave. Do A, then C's two national blocks, then B
   with the taxonomy work it deserves.

**Suggested sequencing:** A1 Türkiye + Poland catalogue (~30 works, ~15 venue
rows, the `orientalism` correction, the `nationNote` proposal to UX) → A2 the
18th century (~30 works) → A3 the remaining stranded nations (~40 works) →
C-Poland + C-Türkiye (~10 artists, Tier 2) → C-hinges (Verrocchio, Bellini,
Gérôme, Mehoffer, Orozco — five artists that repair five named holes) → B as its
own objective.

---

## SOURCES

Read directly, this session: `js/taxonomy.js`, `js/artists-1..17.js`,
`js/catalog-1..4.js`, `js/artworks.js`, `js/influences.js`, `js/venues.js`,
`js/museums-1.js`, `js/lists-1.js`, `js/tier1-artists.js`, `js/app.js` (nation
chip rendering, `DAILY_POOL`), `tools/validate.jxa.js`, `PIGMENT.md`,
`CLAUDE.md`, `docs/STYLE_GUIDE.md`, `docs/ARTWORK_SCHEMA.md`. All counts,
correlations and distributions above were computed from those files, not quoted
from any prior summary; where they differ from `PIGMENT.md` §12's 2026-07-25
snapshot, the figures here are current.

Web, per claim class:

- **Osman Hamdi Bey** — `en.wikipedia.org/wiki/Osman_Hamdi_Bey`. Basis for:
  Ottoman Greek identity and his stated pride in Greek descent; training under
  Gérôme and Boulanger; museum and academy roles. The article presents the
  Orientalism question as **contested**, giving both the "continued in his
  teachers' style" reading and the "subversive and critical of European
  orientalism" reading. I have carried the dispute rather than resolving it; the
  atlas should too.
- **Matrakçı Nasuh** — `en.wikipedia.org/wiki/Matrakçı_Nasuh`. Born in Visoko,
  Bosnia, to Bosnian Muslim parentage; *el-Bosnavî* in his own name; recruited
  via devşirme, exceptionally extended to Bosnian Muslim families. The article
  records **no dispute** about the Bosnian origin. The atlas's current `turkey`
  filing is not a contested call; it is simply wrong.
- **Józef Chełmoński** — `en.wikipedia.org/wiki/Józef_Chełmoński`. 1849–1914
  (death year ≤ 1955, so a public-domain basis is available to assert); works in
  the National Museums in Warsaw and Kraków, neither of which is in the venue
  registry.
- **Hoca Ali Rıza** — `en.wikipedia.org/wiki/Hoca_Ali_Rıza`. 1858–1930 (≤ 1955);
  teacher at the School of Fine Arts, formative for the generation the atlas
  already holds via Çallı.

**Not asserted without checking.** Every absence claimed in §1 and §4 was
grepped across `js/` before being written down. That check changed the document:
**Aliye Berger, Verrocchio, Bellini, Gérôme, Orozco, Siqueiros, Mehoffer,
Cimabue, Ghirlandaio, Pontormo, Guardi, Bellotto, Böcklin, Mucha and Filippo
Lippi all return hits** — as prose mentions, not records — which is how §1 Gap 4
came to exist at all. "Brandt" and "Weiss" return hits that are substring false
positives (Rembrandt, and unrelated German text); they are not artists in this
atlas.

## UNCERTAIN — left standing rather than smoothed

- **The influence graph's 238 edges were not individually audited.** I report
  their shape, not their truth. The proportion that is documented, conventional
  or unfounded is unknown, and the one edge with a known problem
  (Zurbarán ← Caravaggio) suggests the answer is not "all documented."
- **The 44-women count is a heuristic**, derived from pronoun frequency in each
  record's prose, not from a `gender` field — the schema has none. I spot-checked
  the list and believe it is correct, but treat 17% as approximately right rather
  than exact.
- **"Ottoman Westernist painting" is a working name**, not an established
  art-historical term I can cite. The category is real and the current
  `orientalism` filing is wrong; the label needs a decision and possibly a better
  word than mine.
- **Whether Osman Hamdi Bey subverted Orientalism or practised it is genuinely
  disputed in the literature.** I have not picked a side and the atlas should not
  either. What is *not* disputed is that he was an Ottoman insider, which is what
  makes the movement chip wrong regardless of how the debate resolves.
- **Şeker Ahmed Paşa's `orientalism` tag** I judge simply mistaken rather than
  contested — he is normally described as an early Ottoman painter working in the
  Western manner — but I did not find a source addressing the tag directly, so I
  am recording that as a judgement rather than a citation.
- **I did not verify that the 413 `ARTWORKS` image URLs still resolve or still
  depict the exact works.** Direction A's cost estimate assumes they largely do;
  that assumption should be tested by the Data Steward before the work is scoped,
  and per `PIGMENT.md` §14 a timeout or a 429 is not evidence of a dead URL.
- **Nothing in this document is a rights determination.** Death years are an
  asserted basis for a public-domain claim, per OD-5, and nothing here is
  cleared or verified.

## VALIDATOR

No data was modified in this pass. Run at the start and end of the review,
unchanged:

```
app.js: syntax OK
artists: 256, movements: 76, techniques: 39, eras: 8, nations: 37,
painter styles: 27, influence edges: 238, venues: 116, catalog: 323 (tier1: 76),
daily pool: 75, museum notes: 104, photo credits: 104 (attribution required: 88),
artwork image credits: 27, personas: 15, lists: 12 (featured: 4),
tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```
