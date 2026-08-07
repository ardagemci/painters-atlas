# Batch build — catalog batches 01 and 02

*Dürer (`claude-implementation-lead`), 2026-08-07, branch `main`.*

Assembly of the twenty-two records specified in `docs/CATALOG_BATCH_01.md`
(Vasari) and `docs/CATALOG_BATCH_02.md` (Vasari), with the `description` and
`notice` copy from `docs/CATALOG_BATCH_COPY.md` (Van Gogh). This build decided no
factual field and wrote no visitor prose. Where it had to author something the
specifications did not supply, or diverge from them, it is listed under
DEVIATIONS below rather than absorbed silently.

PIG-001 is closed and shipped, so Gate 1 does not apply. Four commits, in
dependency order, each one validator-green and suite-green before the next
started.

---

## GROUP 1 — the bake path, fixed before any record landed

Commit `325d5d5` — `docs/ARTWORK_SCHEMA.md` only.

Both batches found that the bake §7 planned would corrupt records that are
individually correct. §7 gained a normative sub-section, **§7.1 Bake rules**, and
§3's `dims` example lost its bare `cm`.

| rule | defect | regression case |
|---|---|---|
| 1 | `P2048`/`P2049` carry a **unit qualifier**. Read it and convert (`Q11573` metre ×100, `Q174728` centimetre as-is); any other unit or a missing qualifier is a miss | Courbet, *A Burial at Ornans* — `3.15 × 6.68` in **metres**, which §3's example would have published as "3.15 × 6.68 cm" |
| 2 | **Then** range-check the converted values (reject > ~1000 cm or < ~1 cm) | `osman-hamdi-bey :: Two Musician Girls`, `580 × 390`. Ceiling set wide enough to admit *The Raft of the Medusa* at 491 × 716 cm |
| 3 | The amounts do not say **what** they measure | Kōrin, `156 × 172.2` — the figure measures one screen of a pair |
| 4 | Multi-valued `P195`/`P276` are **provenance chains, not alternatives**; the bake must not choose | *The Tempest* (Vendramin, Manfrin); Rogier's *Descent* (five locations, incl. El Escorial) |
| 5 | A single value can be the wrong **granularity**; slug matching must fail closed | "Department of Paintings of the Louvre" (David, Géricault) |
| 6 | Never derive `title` from the Commons filename | *Maestà*; *The dead Christ and three mourners*; *A Sunday on La Grande Jatte … 1884* |

**Order is normative, and rules 1 and 2 do not substitute for each other.** The
Curator's warning is the load-bearing part and is written into the document: a
plausibility range does not catch a unit error, it *launders* one, because
3.15 × 6.68 cm is a perfectly plausible miniature.

**No tooling changed, because none implements the bake.** `tools/build_catalog.py`
is named in §7 and does not exist; `grep` for `P2048`/`P195`/`build_catalog`
across `tools/` and `js/` returns nothing outside the documents themselves. So
this fixes the contract before an implementation inherits it, and the six
regression cases are named in the document so an implementation can be tested
against them.

> Validator: `ALL REFERENCES VALID` · Tests: `OK` (44)

---

## GROUP 2 — venues and taxonomy

Commit `03a2964`.

**Nine venues, 116 → 125.** All as specified. First entries for **India, Korea
and Switzerland**; Poland's first venue that exists for Polish painting rather
than for a Leonardo; **Japan's first two venues that hold Japanese art** — the
registry's only prior Japanese entry, `nmwa-tokyo`, is the National Museum of
*Western* Art.

**Three movements, 76 → 79**, all at top level with no parent, as specified.

- **`pungsokhwa`** — Korean genre painting of the late Joseon period, following
  the `ukiyo-e` / `rinpa` / `literati-painting` / `ottoman-miniature` /
  `persian-miniature` precedent the Curator names. `kim-hong-do` moves from
  `["realism"]` to `["pungsokhwa"]`. `realism` stays in the taxonomy: the defect
  was the application, not the node.
- **`bauhaus`** — his reasoning holds. Sixteen prose mentions across `js/`, three
  Bauhaus painters held, no node. Added **as an institution**, not as a style
  sibling of `expressionism`, and the node's own `desc` says so.
- **`skagen-painters`** — his reasoning holds. Twenty-two prose mentions, two
  painters held, no node. Added as a **colony**, labelled as a grouping rather
  than a doctrine.

> Validator: `ALL REFERENCES VALID`, 9 warnings · Tests: `OK` (44)

---

## GROUP 3 — the twenty-two records

Commits `dcc433d` (batch 01 R1–R6), `a633197` (batch 01 R7–R10), `84e4760`
(batch 02 R1–R6), `bb29c03` (batch 02 R7–R12 + prerender).

All 22 land in **`js/catalog-5.js`** (new file, ~40 records/file per §7). Catalog
**323 → 345**. All Tier 2; the Tier 1 count does not move.

**How the copy got in.** The `description` and `notice` fields are **parsed out
of `docs/CATALOG_BATCH_COPY.md`**, not retyped. The generator asserts, before it
writes: that each description's word count equals the count the Content Editor
declared; that each bullet's word count equals its declared count; that every `†`
marks a bullet over 8 words and no other; and that the slug in the copy document
matches the slug in the specification. A transcription error cannot reach the
catalog without failing one of those four.

**Nothing was promoted.** All 22 carry `coordsSource:"override"` with hand-scored
coordinates, a description and exactly three notice bullets, so all 22 meet §4's
*field* requirements for Tier 1 and are held at Tier 2 by §8's inbound-link rule
alone. That is the Curator's call and it stands.

### §4's wording, corrected — the code was right

The Content Editor flagged it and it checks out. `js/app.js:2072` branches on
`w.description` and renders **The picture** and **What to notice** whenever it is
present; it never consults `tier`. §4 claimed Tier 2 shows "a single styled
empty-state line" *instead*, which described a tier gate the renderer does not
implement. **The wording was corrected, not the code** — a Tier 2 record that has
been written about should show what was written. Verified twice: by reading the
branch, and by confirming the copy is present in the generated stub
(`p/artwork/the-tortoise-trainer.html` carries "the slowest lesson in the room").

### The `notice` budget conflict — still open, and deliberately so

`STYLE_GUIDE` §4.3 implies ≤ 8 words, `ARTWORK_SCHEMA` §3 says ≤ 12, the
validator checks neither, and 21 of 66 bullets land at 9–12.

**Shipped at 12**, because the shipped corpus already does — `catalog-1.js` opens
with a 9-word bullet. **This is not a resolution and must not be read as one.**
The Content Editor's `†` markers and his FLAGS §F1 stand untouched in
`docs/CATALOG_BATCH_COPY.md`, and the conflict is still an open adjudication for
the owner. His observation §3 is worth the owner's attention when it is taken up:
§4.3's 8-word rule was written for artist and movement traits, and may be a rule
inherited into a context it was not written for rather than a competing budget.

---

## WHAT COULD NOT BE BUILT

1. **`tarashikomi` (Batch 02 T-TECHNIQUE).** Not built. It is proposed with a
   source and a scope argument, but it is a *technique-registry* proposal in a
   document whose taxonomy brief to this build was the three movement nodes, and
   `red-and-white-plum-blossoms` ships with **no `techniques` field at all**
   rather than a wrong one — which is the specification's own instruction and
   which the node would not change. Landing it is a one-line follow-up.
2. **The `abstract` tag and the §5 vocabulary enforcement (T-TAGS).** Not built.
   130 of the shipped records carry off-vocabulary tags; adding the validator
   check would fail the suite on all 130, and the Curator is explicit that the
   check must be sequenced **after** the normalisation, not before it. All 22 new
   records are fully inside the §5 vocabulary — checked — so this batch adds
   nothing to the backlog.
3. **The `beginning-noland` demotion (T-TIER).** Not built. It is a tier change
   proposed by the Curator against an existing record, not part of assembling
   these 22, and it deserves its own commit and its own review.
4. **§9's "Tier 1 record with zero inbound links" warn.** Still unimplemented in
   `tools/validate.jxa.js`; three records qualify and remain invisible to the
   suite. Recorded by Batch 02, not fixed here.
5. **Building photographs for the ten museum notes** (see DEVIATIONS 2).

---

## DEVIATIONS

**D-1 — Ten museum-note hooks were authored by this build.** *Necessary.*
`tools/validate.jxa.js:200` **errors** on any venue that holds catalog works and
carries no museum note, so the records could not land without them. Neither batch
specification nor `CATALOG_BATCH_COPY.md` supplies museum copy. Each hook is held
to facts already sourced in those documents. **These are the only visitor-facing
sentences in this build that the Content Editor did not write, and they should be
reviewed as his.** Nine are for the new venues; the tenth is `pera-museum`, which
is not new — it has been in the registry since day one and simply held no catalog
work until batch 01 R1.

**D-2 — Those ten notes carry no building photograph.** *Accepted, and it is the
whole of the validator's warning output.* Adding a photograph requires a
`js/photo-credits.js` record or the validator errors, which means a Commons
rights lookup and, on this evidence, live attribution obligations for some of
them. That is a rights exercise with its own governance
(`docs/IMAGE_RIGHTS_ROUTES.md`) and not part of assembling a catalog batch. The
pages fall back to a generative cover, which is the designed path.

**D-3 — `national-museum-warsaw` displays one name, not two.** Batch 01's venue
table gives `Muzeum Narodowe w Warszawie / National Museum in Warsaw`. **No venue
among the other 116 carries a dual name**, and the registry's practice for
institutions whose native name is opaque to an English reader is the English form
(`National Museum of Western Art`, `State Russian Museum`, `Royal Museums of Fine
Arts of Belgium`). The English form was taken. Both strings are the Curator's;
this build chose which of the two to display and changed nothing else.

**D-4 — `prado` displays "Museo del Prado" on the Rogier record.** Batch 02 R3
gives `name:"Museo Nacional del Prado"`. Every existing catalog record for that
venue, and the registry row itself, reads `Museo del Prado`. One venue displaying
two names across the catalog is a data-quality defect, so the existing string was
used. Both name the same institution and both are correct; nothing factual moved.

**D-5 — A third ledger in `tests/test_rights_tooling.py`.** *Necessary, and the
mechanism was already there for it.* The suite freezes the rights inventory and
fails on undeclared image drift — correctly, and it did. `CATALOG_BATCHES` is
kept separate from `CORRECTIONS` and `CONTENT_LANE` on exactly the principle
those two are separate from each other. **These 22 files are not new assets**:
they are pool entries already counted on the `gallery` surface, now also on
`catalog`. So `catalog_gallery_overlap` 92 → 114 and the catalog surface 257 →
279, both by exactly 22, while `total_unique` and `rendered_unique` **do not
move** — and if they ever do, the batch introduced an image it did not declare.
The URL list is emitted from `js/catalog-5.js` rather than typed, so declaration
and data cannot drift apart.

**D-6 — The prerender surface moved +9/−8, not +22.** *Explained, not adjusted.*
`tools/build_seo.jxa.js:74` `artistImage()` prefers a catalog `pd` work over a
`js/artworks.js` pool entry, so eight artists' stubs switched `og:image` from a
pool work to their new catalog record, and thirteen of the 22 were already on
that surface for the same reason. **No file left the tree** — all eight are still
rendered on the artist-page gallery surface. The mechanism is recorded in the
ledger comment so the next reader does not have to rediscover it.

**D-7 — `js/catalog-5.js` is enumerated by name in four places.** `index.html`,
`tools/validate.jxa.js`, `tools/build_seo.jxa.js` and
`tools/audit_artwork_rights.py` each list catalog files literally; all four were
updated. Worth noting as a fragility: a fifth consumer added later, or a
`catalog-6.js`, will silently be missed by whichever list is forgotten — the
rights audit being the one where a miss would be least visible and most serious.

**D-8 — `?v=` bumped** to `20260807-batch12` for every versioned asset touched
(`taxonomy.js`, `venues.js`, `museums-1.js`, `artists-5/15/16/17.js`), and
`catalog-5.js` ships at that version.

---

## VERDICTS

Read as verdict lines, not run counts — per
`docs/corrections/f445a4d-false-test-claim.md`.

| group | validator | suite |
|---|---|---|
| 1 — bake path | `ALL REFERENCES VALID` | `OK` · Ran 44 tests |
| 2 — venues + taxonomy | `ALL REFERENCES VALID` (9 warnings) | `OK` · Ran 44 tests |
| 3a — batch 01 R1–R6 | `ALL REFERENCES VALID` (10 warnings) | `OK` · Ran 44 tests |
| 3b — batch 01 R7–R10 | `ALL REFERENCES VALID` (10 warnings) | `OK` · Ran 44 tests |
| 3c — batch 02 R1–R6 | `ALL REFERENCES VALID` (10 warnings) | `OK` · Ran 44 tests |
| 3d — batch 02 R7–R12 + prerender | `ALL REFERENCES VALID` (10 warnings) | `OK` · Ran 44 tests |

Final validator line, in full:

```
app.js: syntax OK
artists: 256, movements: 79, techniques: 39, eras: 8, nations: 37,
painter styles: 27, influence edges: 238, venues: 125, catalog: 345
(tier1: 76), daily pool: 75, museum notes: 114, photo credits: 104
(attribution required: 88), artwork image credits: 27, personas: 15,
lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```

**All ten warnings are the same warning**, and D-2 is why: ten museum notes with
no building photograph. There is no other warning in the tree.

**And the caveat Batch 02 attached to its own clean run still stands.** A clean
validator run is evidence about *references*. It is not evidence about
correctness, and two gaps behind it are known and unfixed: the suite does not
implement §9's inbound-link warn, and it does not check tags against the §5
vocabulary. Neither would have caught a wrong fact in any of these 22 records,
because nothing in this pipeline checks a fact — the 22 rest on the Curator's
sourcing, and `IMAGE_RIGHTS_ROUTES.md`'s STATE OF VERIFICATION records that the
pool's wrong-image rate is a floor rather than a measurement.

## Preview

```
python3 -m http.server 8421 -d .    # a server is already running on 8422
```
`#/artwork/ssireum` · `#/artwork/a-burial-at-ornans` ·
`#/movement/pungsokhwa` · `#/museum/skagens-museum`
