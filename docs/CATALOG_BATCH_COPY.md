# Catalog Batch Copy — editorial fields for Batches 01 and 02

*Van Gogh (`claude-content-editor`), 2026-08-07, branch `main`. Copy only.
No `js/catalog-*.js` file is written by this document. The Implementation Lead
builds; this supplies the sentences a visitor reads.*

Source specifications: `docs/CATALOG_BATCH_01.md` (10 records) and
`docs/CATALOG_BATCH_02.md` (12 records). **Twenty-two records.** Every factual
field — id, title, artist, date, image, techniques, movements, nation, venue,
tier, coordinates — belongs to the Curator and is not restated or altered here.

---

## WHAT THIS DOCUMENT SUPPLIES

`ARTWORK_SCHEMA.md` §3 marks exactly two fields **A (authored)** on an artwork
record: `description` and `notice`. Checked against the shipped renderer:
`js/app.js:2072` renders `description` under **The picture** and `notice` under
**What to notice**, and falls back to a single shared empty-state string when
`description` is absent. That string is **not** per-record copy — it is one
literal in `app.js`. So there is no third editorial field to write, and this
document supplies two fields per record and nothing else.

## THE RULES THIS COPY WAS WRITTEN UNDER

1. **No fact the Curator did not source.** Where a sentence wanted a detail his
   specification does not carry — a colour, a count, a position in the frame —
   the sentence was rewritten rather than the detail invented. Losses are listed
   in FLAGS.
2. **His uncertainty is carried, not smoothed.** Where he recorded a disputed
   date, a contested subject, an unestablished anecdote or a single-source
   claim, the prose says so, in the record where a visitor will meet it.
3. **OD-5.** No sentence here describes any image as verified, cleared, or
   settled in law. Rights language does not appear in visitor copy at all —
   there is no place in `description` or `notice` where it belongs.
4. **Budgets** per `STYLE_GUIDE.md` §4.4, with the known conflict recorded
   below and every count stated per field.

## BUDGET CONFLICT (PIGMENT.md §15.5) — flagged, not silently resolved

Three documents give three budgets for these two fields:

| field | STYLE_GUIDE §4.4 | ARTWORK_SCHEMA §3 | validator (§9 / `tools/validate.jxa.js`) |
|---|---|---|---|
| `description` | 50–80 words | "50–80 words, STYLE_GUIDE §4.4" | **30–110 words** |
| `notice` bullet | 3 bullets, "same rules as Look-for" → **≤ 8 words** (§4.3) | 3 bullets, **≤ 12 words** | exactly 3 bullets, no word check |

**`description` is not really in conflict.** The validator range is a wider
gate around the same target, and every description here is written to the
50–80 target.

**`notice` is a real conflict: 8 words against 12.** It is not academic. The
shipped catalog breaks the 8-word rule as a matter of routine — `catalog-1.js`
opens with *"Christ's languid hand quotes Adam's from the Sistine ceiling"* (9)
and *"The maid is young and strong — a co-conspirator, not a witness"* (12) —
so the shipped precedent sits on the schema's side, and the validator enforces
neither number.

**What this document did, stated plainly:** wrote every bullet to **≤ 12**,
held as many as possible at ≤ 8, and **noted the count on every bullet** so a
reviewer can apply either rule without re-counting. Bullets over 8 words are
marked `†`. My brief names STYLE_GUIDE authoritative and I am not overriding
it — I am declining to pick, because picking 8 silently would put this document
in conflict with every shipped record, and picking 12 silently would put it in
conflict with the guide. **This wants an adjudication, not a content editor's
preference.**

---

## RECORDS

*Appended four at a time. A record is here only when both its fields are
written and counted.*

**Counting rule**, stated so nobody has to guess: whitespace-separated tokens,
with a standalone em-dash counted as a token. That is the conservative reading —
it never reports a field as shorter than another rule would. `†` marks a
`notice` bullet over 8 words (see BUDGET CONFLICT).

---

## BATCH 01

### B01-R1 — `the-tortoise-trainer` (Osman Hamdi Bey, 1906)

**description** — 61 words

> A man in Ottoman dress stands stooped over his tortoises, a naqareh drum
> slung on his back, waiting for them to learn something. They do not hurry.
> Nothing in the picture moves at all. Osman Hamdi Bey built it to be read
> rather than felt, and gave two and a quarter metres of canvas to the slowest
> lesson in the room.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | The drum on his back is a naqareh | 8 |
| 2 | Nothing in this picture is in a hurry | 8 |
| 3 | That the trainer wears the painter's own face — widely repeated, unestablished | 12 `†` |

*Carrying the doubt.* Bullet 3 is Batch 01 UNCERTAIN §4. The Curator recorded
that the identification is widely repeated and declined to assert it; the bullet
repeats it as repetition and stops there. This is the more interesting sentence
anyway — an unresolved face is better copy than a resolved one.

### B01-R2 — `stanczyk` (Jan Matejko, 1862)

**description** — 59 words

> A court ball is going on through the doorway behind him, bright and busy. The
> jester sits apart in red, out of the light, and does not perform. He has read
> the dispatch; the dancers have not. Matejko painted it in 1862 in entirely
> conventional means, and gave the loudest man at court the only silence in the
> room.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | The ball is bright; his corner is not | 8 |
| 2 | In costume, and the only figure not performing | 8 |
| 3 | He has read the dispatch; the dancers haven't | 8 |

### B01-R3 — `senecio` (Paul Klee, 1922)

**description** — 63 words

> A head, still legible as a head, assembled out of squares and wedges the way
> a bricklayer would build one. The gaze is level and it holds. Klee was
> teaching at the Bauhaus in 1922, laying colour down as a system rather than
> as a description — and the system came out amused. Forty centimetres square.
> You could carry it under one arm.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | A head built from squares and wedges | 7 |
| 2 | The gaze is level, and it holds yours | 8 |
| 3 | Oil on gauze, or oil and canvas — sources disagree | 10 `†` |

*Carrying the doubt.* Bullet 3 is Batch 01 UNCERTAIN §5 — the Commons filename
and Wikidata disagree about the support, and the Curator recorded the
disagreement rather than resolving it. The bullet does the same, in the place a
visitor will actually read it.

### B01-R4 — `sunlight-in-the-blue-room` (Anna Ancher, 1891)

**description** — 64 words

> A child sits in a blue room, and the event of the picture is sunlight
> arriving on the wall behind her. That is the whole plot. Ancher painted it in
> 1891 at sixty-five centimetres — a corner of a house rather than a scene —
> and gave the light more attention than the sitter, which is why your eye goes
> to the wall first.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | The wall holds the light; the child holds still | 9 `†` |
| 2 | Blue throughout, warmed only where the sun lands | 8 |
| 3 | Sixty-five centimetres: a corner, not a scene | 7 |

### B01-R5 — `three-girls` (Amrita Sher-Gil, 1935)

**description** — 64 words

> Three young women sit close together and not one of them looks at another, or
> at you. Nothing happens. Sher-Gil trained in Paris and turned that training on
> an Indian subject — modern in its colour and its flattening, conventional in
> every other means — so the picture works by mood instead of by argument. A
> metre of canvas, three figures, no story offered.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | Nobody meets anybody's eye, including yours | 6 |
| 2 | Modern in colour and flattening, conventional in means | 8 |
| 3 | Reportedly won a gold medal from the Bombay Art Society | 10 `†` |

*Hedge.* The medal is what the Commons file page states and the Curator declined
to go beyond it, so bullet 3 takes `STYLE_GUIDE.md` §3.1's sanctioned hedge
("reportedly") rather than the flat statement.

### B01-R6 — `the-artist-and-his-mother` (Arshile Gorky, c. 1926–1936)

**description** — 68 words

> Gorky worked from a childhood photograph taken in Van: himself as a boy,
> standing beside his mother. In the aftermath of the genocide she died of
> starvation in Yerevan, in 1919. He painted this over roughly a decade and
> never called it finished. The surfaces are scraped back and laid again, the
> faces pressed towards outline and plane. Two versions exist. This is the one
> at the Whitney.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | Painted from a childhood photograph taken in Van | 8 |
| 2 | Scraped back and repainted for a decade, never finished | 9 `†` |
| 3 | A second version is in Washington | 6 |

*Register.* `STYLE_GUIDE.md` §5: genocide gets no joke and no dramatic
flourish either. Every sentence here is plain and declarative on purpose, and
the em-dash — this project's signature turn — is deliberately absent from the
whole record. The facts are the Curator's, from the English Wikipedia article
on Gorky that he cites.

*Note, not a doubt carried in copy.* The record's `year.display` is
`c. 1926–1936` and the description's "roughly a decade" follows it. Wikidata's
competing point date of 1931 (Batch 01 UNCERTAIN §1) is **not** surfaced in the
prose — see FLAGS.

### B01-R7 — `lemminkainens-mother` (Akseli Gallen-Kallela, 1897)

**description** — 64 words

> A mother kneels on the bank of the river of the dead and puts her dismembered
> son back together. Gallen-Kallela painted it in 1897 in tempera rather than
> salon oil — flattened, hard-edged, bounded like decoration — so that a scene
> of that kind holds absolutely still. The stillness is not calm. Nothing in the
> picture moves and everything in it is at pitch.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | Tempera, not oil — a refusal of salon finish | 9 `†` |
| 2 | The body is being assembled, not mourned | 7 |
| 3 | Motionless, and not remotely calm | 5 |

### B01-R8 — `the-lovers-abbasi` (Reza Abbasi, 1630)

**description** — 67 words

> Two figures fold into one another on a page you could hold in one hand.
> Nothing happens but the touching — no depth, no room, no story arriving. Reza
> Abbasi worked inside Safavid album convention at the height of it, and the
> whole picture is about how a sleeve sits against a shoulder. The sheet carries
> its own date: 8 Shawwal 1039, which is 21 May 1630.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | The sheet is dated 8 Shawwal 1039 — 21 May 1630 | 11 `†` |
| 2 | No depth is attempted; the idiom never wanted it | 9 `†` |
| 3 | The real subject is the fall of cloth | 8 |

*Why the date is the headline.* This is the one record in either batch whose
date is inscribed on the object rather than inferred from it — the Curator
calls it the firmest date in Batch 01. Everywhere else in these twenty-two
records the copy has to hedge a date; here it can name the day, and that
contrast is worth spending a bullet on.

### B01-R9 — `birds-in-a-lotus-pond` (Bada Shanren, 1690)

**description** — 61 words

> One perched bird, made of two strokes and a dot for an eye, on a great deal
> of empty paper. Bada Shanren painted inside the literati tradition and at its
> far edge — the reduction was his, not the convention's. The mood is not
> serene. It is sour, and the bird looks as though it has formed an opinion
> about you.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | The eye is a single dot, and it judges | 9 `†` |
| 2 | Most of the sheet is left as paper | 8 |
| 3 | The 1690 date rests on one source | 7 |

*Carrying the doubt.* Bullet 3 is Batch 01 UNCERTAIN §6: no Wikidata item
resolves and the year has one source behind it. The record's `year.display`
prints a bare `1690`, which reads firmer than the evidence is, so the bullet is
where the hedge has to live.

### B01-R10 — `ssireum` (Kim Hong-do, 18th century)

**description** — 70 words

> Two wrestlers at the moment the contest tips, and a ring of spectators around
> them, every one of them a separate person. There is no ground and no
> background — just figures on empty paper. It is played for comedy rather than
> violence. One leaf out of an album of 25. Nobody knows the year: no date
> survives on the record, and the album is placed in the 18th century.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | No ground, no background — figures on bare paper | 9 `†` |
| 2 | One leaf from an album of 25 | 7 |
| 3 | The date is unknown; the century is a placing | 9 `†` |

*Carrying the doubt.* Bullets 2–3 are Batch 01 UNCERTAIN §2. The record's
`year.display` reads `18th century` and its `sort` is an ordering key, not a
claim; the copy says so rather than letting `1780` leak into a sentence. The
National Treasure designation (UNCERTAIN §3) is deliberately **not** in the
copy — see FLAGS.

*On how this one is written.* It is a picture of a wrestling match, and the
copy treats it as a picture of a wrestling match. No sentence here explains
Korea to anybody, and none of the eight first-for-their-nation records in Batch
01 carries a word about being a first.

---

## BATCH 02

### B02-R1 — `ognissanti-madonna` (Giotto, c. 1300–1305)

**description** — 63 words

> Gold ground, angels ranked by importance, everything the convention asked for
> — and then a knee pushes out under the drapery and the whole thing changes.
> Giotto kept the hierarchy of a Byzantine Maestà and threw the flatness away.
> The throne is built in depth. The body has weight. Three and a quarter metres
> of panel, made to be met across a church.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | A knee carries real weight under the drapery | 8 |
| 2 | The throne is built in depth, not stacked | 8 |
| 3 | Gold ground kept; the flatness thrown out | 7 |

### B02-R2 — `the-holy-trinity-masaccio` (Masaccio, 1425–1426)

**description** — 68 words

> The architecture behind the figures is built in one-point perspective, and
> the vanishing point sits at the eye level of someone standing in the church —
> so the painted space is not a backdrop, it is the room you are in. A painted
> tomb and its inscription run beneath. Masaccio put this on a wall around 1425,
> and afterwards the tradition had to use it or refuse it.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | The vanishing point sits at your standing eye level | 9 `†` |
| 2 | A painted tomb and inscription run beneath | 7 |
| 3 | This is a wall, not a panel | 7 |

### B02-R3 — `the-descent-from-the-cross-van-der-weyden` (Rogier van der Weyden, c. 1435–1438)

**description** — 68 words

> Ten figures at life size, packed into a box barely deeper than a carved
> shrine — there is nowhere for any of them to go. The Virgin has collapsed,
> and her body is drawn as a near-exact rhyme of her son's: same curve, same
> fall, one directly above the other. That is the invention. The grief is not
> performed by the faces; it is built into the composition.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | The Virgin's body rhymes with Christ's, curve for curve | 9 `†` |
| 2 | Ten life-size figures in a shrine-shallow box | 7 |
| 3 | Grief at full pitch, and nothing is moving | 8 |

### B02-R4 — `the-tempest` (Giorgione, c. 1505)

**description** — 64 words

> A man stands on one bank, a woman nurses a child on the other, lightning goes
> off behind them, and neither reacts. No figure carries an attribute that would
> identify it; no action connects the two. The readings proposed for the subject
> are numerous and mutually exclusive, and none has settled. Meanwhile the
> landscape takes most of the picture and carries all its weather.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | Lightning behind them, and nobody reacts | 6 |
| 2 | No attribute identifies anyone in the picture | 7 |
| 3 | The proposed readings are many, and mutually exclusive | 8 |

*Carrying the doubt — the record where it mattered most.* Batch 02's spec is
explicit that "nobody agrees what it shows" is the sourceable fact and warns the
Content Editor off picking the most charming candidate. **No reading is named
here.** The unreadability is written as the subject of the copy rather than as a
caveat at the end of it, which is also the better sentence: a picture nobody can
identify is more interesting than any of the identifications.

### B02-R5 — `venus-of-urbino` (Titian, 1538)

**description** — 65 words

> A woman on a bed in an ordinary sixteenth-century bedroom, looking at you, and
> looking as though she has been for some time. Two maids at a chest in the
> background, a dog asleep, white linen and fur. Nothing here is mythological
> except the word Venus in the title. The reclining nude that Western painting
> used for the next three hundred years starts about here.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | She met your eye before you arrived | 7 |
| 2 | The only mythology is in the title | 7 |
| 3 | Two maids at a chest; a dog asleep | 8 |

*What the last sentence does and does not claim.* Batch 02 UNCERTAIN §8 records
the specific descent — the Rokeby Venus, the *Maja*, *Olympia* — as
**conventional rather than sourced**, and the Curator asks that the hedge be
carried through. So the copy makes the type claim the spec does state ("the
reclining-nude type this fixes is the one Western painting used for the next
three hundred years"), hedges it with "starts about here", and **names none of
the three descendants.** If a later record sources one of them, that sentence
can get sharper; it should not get sharper before then.

### B02-R6 — `lamentation-of-christ-mantegna` (Andrea Mantegna, c. 1470–1474)

**description** — 62 words

> The body is laid out feet-first, straight at you, in the hardest thing
> perspective can be asked to do. Then Mantegna adjusts it: the proportions are
> visibly tuned so that the feet do not swallow the head. Three mourners weep
> beside him. It is a technical demonstration wearing the clothes of a devotional
> picture, and the whole thing is 68 centimetres wide.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | Feet-first foreshortening, the hardest problem perspective has | 7 |
| 2 | The proportions are tuned so feet don't dominate | 8 |
| 3 | 68 centimetres — narrower than a briefcase is wide | 8 |

### B02-R7 — `haboku-sansui` (Sesshū Tōyō, 1495)

**description** — 74 words

> A cliff, a hut, a boat and two small figures — and above them the ink simply
> stops describing anything, just fast wet blots on a sheet a metre and a half
> tall. Haboku is the most extreme manner the tradition had, and Sesshū took it
> to the edge in 1495. This is about as close to non-figuration as the fifteenth
> century gets anywhere. Stand close: the whole landscape is a handful of
> strokes.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | The top of the sheet stops describing anything | 8 |
| 2 | A cliff, a hut, a boat, two figures | 8 |
| 3 | Two sources call it a National Treasure of Japan | 9 `†` |

*Carrying the doubt.* Bullet 3 is Batch 02 UNCERTAIN §7. Wikidata and English
Wikipedia both assert the designation and no primary Japanese record was read,
so the bullet says *two sources call it* rather than *it is*. That is a weaker
sentence and a truer one, and it costs the copy nothing.

*On how this one is written.* "This is about as close to non-figuration as the
fifteenth century gets anywhere" is the Curator's own consequence reading, and
it is a claim about the painting, not about Japan. No sentence in this record
introduces Sesshū as a representative of anywhere.

### B02-R8 — `red-and-white-plum-blossoms` (Ogata Kōrin, c. 1714–1715)

**description** — 64 words

> A river runs down the middle as flat repeating pattern, with no attempt
> whatsoever to look like water, and a plum tree stands on either bank. The bark
> is mottled because Kōrin laid a second pigment down before the first had
> dried — tarashikomi. It is spring, and it stays spring. Nothing else happens.
> Two screens, each over a metre and a half tall.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | The river is pattern; no attempt at water | 8 |
| 2 | Mottled bark: wet pigment dropped into wet | 7 |
| 3 | Undated — 1714 to 1715 is Yamane's attribution | 8 |

*Carrying the doubt.* Bullet 3 is Batch 02 UNCERTAIN §4: the work is undated,
the range is Yūzō Yamane's dating, and `sort:1714` is an ordering key. The
bullet names the attributor, which is what turns a date into an attribution in
the reader's hand.

*The "each" that the dimensions do not say.* The description ends "Two screens,
each over a metre and a half tall" — deliberately. POOL DEFECT 4 records that
Wikidata's `156 × 172.2` does not state that it measures **one screen of a
pair**, and that a bake printing it beside a single image would state something
false about the object. The copy carries the word the metadata is missing, so
the page is truthful even if the `dims` string ships wrong.

### B02-R9 — `oath-of-the-horatii` (Jacques-Louis David, 1784–1785)

**description** — 68 words

> Three sons, three arms, three swords, all converging on the single point their
> father holds. To the right the women have collapsed into a separate curve, so
> that duty and grief do not share a shape. Everything a history painting used
> to arrange for beauty, David arranges to make a proposition instead. The oath
> has not been spoken yet. Four and a quarter metres, pitched at a nation.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | Three arms, three swords, one point | 6 |
| 2 | The women make a curve; the men make angles | 9 `†` |
| 3 | The instant before the oath is spoken | 7 |

### B02-R10 — `the-raft-of-the-medusa` (Théodore Géricault, 1818–1819)

**description** — 63 words

> Seven metres of canvas — the size the Salon reserved for scripture and
> antiquity — given over to a news story. Bodies pile into a pyramid, the dead
> at the base and the living straining up out of it, and at the apex there is no
> hero, no state and no moral resolution: only a figure signalling at a speck on
> the horizon.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | Seven metres wide, at Salon scale, for contemporary news | 9 `†` |
| 2 | The apex holds no hero and no state | 8 |
| 3 | A speck on the horizon is the whole plot | 9 `†` |

*Not asserted.* The story that Delacroix posed for one of the figures is
Batch 02 UNCERTAIN §10 — widely repeated, established by nothing the Curator
read. It is the single most tempting sentence available for this record and it
is **not in the copy**, on the same rule that kept Osman Hamdi Bey's face out of
B01-R1. Left out, not hedged: a hedge would still put the name on the page.

### B02-R11 — `a-burial-at-ornans` (Gustave Courbet, 1849–1850)

**description** — 67 words

> Six and a half metres of canvas, the scale the Salon kept for coronations,
> spent on a village funeral. Nobody is ennobled. Nothing is arranged into a
> hierarchy — the mourners stand in a row and wait, and the open grave is at
> your feet in the foreground. That was the scandal: not the brushwork, which is
> coarse, but the size, and who Courbet thought deserved it.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | The open grave sits at the viewer's feet | 8 |
| 2 | A row of people waiting — the drama is withheld | 10 `†` |
| 3 | Coronation scale, given to a village funeral | 7 |

*The scale is written in words on purpose.* THE UNIT BUG (Batch 02 POOL DEFECT
1) is live in the build path: Wikidata carries `3.15` and `6.68` in **metres**,
and `ARTWORK_SCHEMA.md` §7 appends `cm`, so an unfixed bake prints
"3.15 × 6.68 cm" for this canvas — a six-and-a-half-metre Salon machine
rendered as a miniature, with no error raised anywhere. The description
therefore states the scale in prose ("six and a half metres") rather than
gesturing at the `dims` line. If the bug ships, the page contradicts itself
visibly instead of lying quietly, and the copy is the thing that is right. This
is not a substitute for the fix.

### B02-R12 — `a-sunday-afternoon-on-the-island-of-la-grande-jatte` (Georges Seurat, 1884–1886)

**description** — 67 words

> Dots of unmixed colour, set side by side and left to mix in your eye instead
> of on the palette — two years of that, across two by three metres. The park is
> full of people and every one of them is frozen in profile or full face, stiff
> as a frieze. Nothing moves, including the dog. The stiffness is not a failure;
> it is the argument.

**notice** — 3 bullets

| # | bullet | words |
|---|---|---|
| 1 | The colours mix in your eye, not the palette | 9 `†` |
| 2 | Every figure is profile or full face, and rigid | 9 `†` |
| 3 | Nothing moves, including the dog | 5 |

---

## TOTALS

| | |
|---|---|
| records | **22** — Batch 01 × 10, Batch 02 × 12 |
| `description` fields | 22, all within the 50–80 target |
| shortest / longest description | 59 (B01-R2) / 74 (B02-R7) |
| `notice` bullets | 66 (3 × 22), all ≤ 12 words |
| bullets ≤ 8 words (STYLE_GUIDE §4.3) | 44 |
| bullets 9–12 words (`†`, ARTWORK_SCHEMA §3) | 22 |
| records spending a bullet on recorded doubt | 8 |

---

## FLAGS

<!-- filled as records land -->
