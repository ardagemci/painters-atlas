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

<!-- records follow -->

---

## FLAGS

<!-- filled as records land -->
