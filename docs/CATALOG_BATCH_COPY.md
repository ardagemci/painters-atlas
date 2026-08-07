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

---

## FLAGS

<!-- filled as records land -->
