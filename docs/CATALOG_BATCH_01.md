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
| — | — | — | — | — | — | — |

---

## NEW VENUES REQUIRED

*Filled as records land. `ARTWORK_SCHEMA.md` §5b: registry additions are cheap
and unreviewed; slug renames are forbidden.*

| venue id | name | city | country | type | needed by |
|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

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
