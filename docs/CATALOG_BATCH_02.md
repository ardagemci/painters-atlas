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
