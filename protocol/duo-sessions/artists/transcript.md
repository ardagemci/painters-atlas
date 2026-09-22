# Task
Work on artist expansion and build a set of 20 artist package to add to our collection. (Repo: Pigment static art atlas. Read CLAUDE.md §6, docs/ATLAS_COVERAGE.md Gap 4, docs/ROSTER_E3.md, js/artists-20.js as the latest single-artist precedent, commit 26309bb.)

## Claude — round 1
**Package = ** (1) artist record in new js/artists-21.js, STYLE_GUIDE budgets, four works[] with titles/dates checked against Wikidata/holding museum; (2) 2–4 gallery images in js/artworks.js resolved with the existing resolver, MERGED by parse+re-serialise (as E3 did), never by re-running fetch_artworks.py over the whole file; every image opened by eye, because E3 showed match_verdict passes signature crops and wall labels; (3) influence edges only where the new prose names the link, so ungrounded stays at 107; (4) prerendered stubs + sitemap via tools/build_seo.jxa.js. NO catalog records — catalog promotion is its own pipeline (CATALOG_BATCH docs), and ATLAS_COVERAGE warns the atlas is already wide-not-deep.

**Selection: only painters who died ≤1955**, so none needs a generative cover. ATLAS_COVERAGE Gap 4 lists painters the atlas NAMES IN PROSE but lacks; I checked: 39 still absent. Proposed 20:
- Named/absent (10): Cimabue, Simone Martini, Ambrogio Lorenzetti, Filippo Lippi, Domenico Ghirlandaio, Robert Campin, Pontormo, Francesco Guardi, Arnold Böcklin, Alphonse Mucha.
- Unnamed canon (4): Uccello, Antonello da Messina, Memling, Pieter de Hooch.
- Absent traditions (6): al-Wasiti (Maqamat), Pérez de Holguín (Alto Perú), Sōtatsu, Shin Yun-bok, Torres-García, Reverón — needs 4 new nations (iraq, bolivia, uruguay, venezuela) in js/taxonomy.js NATIONS + NATION_COORDS.

**Split:** research needs network: I resolve and eyeball images; Codex drafts 10 records, I draft 10, each fact-checks the other. Guard: tests/test_artist_packages.py asserting each batch id has a record, ≥2 gallery images, a stub page and a sitemap entry.

## Codex — round 1
The roster and separate catalog pipeline make sense. I’d tighten three implementation details before splitting the work:

1. **Include browser registration explicitly.** `index.html:189–190` loads artist shards individually, whereas `tools/build_seo.jxa.js` discovers them automatically. Creating `artists-21.js` and generating stubs could therefore pass your proposed guard while leaving all 20 absent from the app. Commit `26309bb` also changed `index.html`. Register the shard and make the guard verify that registration.

2. **Death year is a selection filter, not sufficient image evidence.** `docs/STYLE_GUIDE.md §3.4` requires language about Commons metadata asserting a public-domain basis; `docs/ROSTER_E3.md` explicitly disclaims a rights determination. Keep the cutoff, but record the Commons file and metadata evidence for each selected image. Also pin every hand-corrected resolution in `tools/audit_artworks.py`, as `CLAUDE.md §6` requires. Visual inspection alone does not preserve corrections against future resolver runs.

3. **Extend the existing verification rather than relying on package counts.** Run `tools/validate.jxa.js` for taxonomy/reference integrity and influence grounding, plus existing prerender and rights tests. `tests/test_rights_tooling.py` already contains an `E3_ABSENT_TRADITIONS` ledger consumed by corpus checks; inspect and extend that mechanism for this batch. A “≥2 images” assertion cannot detect duplicate works or mislabeled images.

I’d retain your 20 provisionally, making four distinct, sourceable works and two usable Commons images the research gate before drafting each biography.
## Claude — round 2
All three accepted, one correction to point 2: tools/audit_artworks.py is in the SEALED set (CLAUDE.md §0) and this run has no owner present to edit a verifier. E3 precedent: five hand-corrections, zero pins (grep confirms no E3 file in PINNED). So this batch touches NO sealed file; any hand-picked file goes into the batch doc as a ready-to-apply PINNED block (Commons file, LicenseShortName/Artist/ObjectName metadata, reason) for the owner — same shape as the pending validator edit. Records get: a new ARTIST_BATCH_21 ledger in tests/test_rights_tooling.py added to the ledger tuple so the asset-inventory freeze accounts for every new URL; index.html registration; and a guard that fails on duplicate image URLs and on any works[] title lacking both a gallery entry and a recorded reason.

Roster fix, my own flaw: my 20 had ZERO women. Drop Guardi, De Hooch, Memling (Canaletto, Vermeer, van Eyck already hold that ground); add Elisabetta Sirani, Helene Schjerfbeck, Gwen John (all d.≤1955, verified absent).
Final 20: Cimabue, Simone Martini, Ambrogio Lorenzetti, Filippo Lippi, Domenico Ghirlandaio, Robert Campin, Pontormo, Arnold Böcklin, Alphonse Mucha, Paolo Uccello, Antonello da Messina, Elisabetta Sirani, Helene Schjerfbeck, Gwen John, al-Wasiti, Melchor Pérez de Holguín, Tawaraya Sōtatsu, Shin Yun-bok, Joaquín Torres-García, Armando Reverón.

Gate order as you proposed: research first for all 20 (4 works + ≥2 usable Commons files); failures swapped BEFORE prose. Codex's sandbox has no network, so I produce evidence/<id>.json per artist (Wikidata QIDs, dates, holdings, Commons metadata); Codex drafts 10 records ONLY from those sheets, I draft 10; each fact-checks the other's against the sheets.

## Codex — round 2
The revised roster works. Three concrete changes remain:

1. **The sealed-file restriction is lane-specific.** `CLAUDE.md:31–37` prohibits those edits in Lane III; §0 routes curatorial judgement and visual review to Lane II. E3’s missing pins do not override §6’s explicit pinning requirement. If this run truly lacks the user presence required for verifier edits, document the pending pins as unfinished work; don’t describe the packages as fully complete.

2. **The evidence sheets need to support prose, not just object identification.** QIDs, dates, holdings and Commons metadata cannot substantiate the `life`, `career`, `outside` and `facts` fields illustrated in `js/artists-20.js`. Add claim-level source URLs and supporting excerpts or notes for biography, historical context and each proposed influence. Reviewing each other against identical sheets checks consistency; someone must also verify those sheets against their sources.

3. **Duplicate URLs are too narrow a guard.** `tests/test_rights_tooling.py:E3_ABSENT_TRADITIONS` contains both original and thumbnail URLs. Different thumbnail sizes—or separate Commons scans—can depict the same work. Store a canonical Commons filename plus a work identifier (museum accession, Wikidata ID, or documented fallback), and count distinct works toward the two-image gate. `docs/ROSTER_E3.md §4` already records a rejected duplicate alongside the signature crop and wall label.

I’d retain the revised twenty and research-first gate, but make evidence completeness and any pending pin application explicit acceptance criteria.
## Claude — round 3 (final round)
Accept all three.
1. Pins: I will not edit tools/audit_artworks.py in this autonomous run. The report and batch doc will state plainly that the packages are complete EXCEPT the pin application, which is an open owner item with a ready-to-paste PINNED block. "Complete" will not be claimed without that qualifier.
2. Evidence: each sheet gets claims[] — {field, claim, source_url, note} — for every sentence-level fact in life/career/outside/facts and each influence edge; sources = Wikipedia/Wikidata/museum pages fetched live. Short notes, not copied passages. I verify the sheets against sources while building them (network is mine); Codex's cross-check then verifies the PROSE against the sheets AND flags any claim whose note does not plainly support it.
3. Guard keys: each gallery image recorded in the sheet as {work_title, commons_file (canonical, un-thumbed), work_id (QID | accession | "fallback:<reason>")}. The test normalises thumb URLs to the canonical filename, fails on a repeated filename or a repeated work_id within an artist, and requires ≥2 distinct work_ids per artist.
Build split: Claude — evidence sheets (all 20), taxonomy nations, image merge, ledger, index.html, stubs/sitemap, batch doc; records for artists 1–10. Codex (workspace-write) — records 11–20 in js/artists-21.js from sheets, plus tests/test_artist_batch_21.py per point 3. Then swap for review.

## Codex — round 3
The substantive research and acceptance criteria now align. I’d make three final implementation adjustments:

- **Give `js/artists-21.js` one integrator.** Both halves currently target the same file. `js/artists-20.js` uses one `window.ARTISTS = …concat([...])` wrapper; draft separate fragments, then have one person assemble the twenty records. This avoids concurrent edits to the wrapper and array boundaries.

- **Test shipped data against the sheets.** `js/artworks.js` stores images under artist ID and work title as `{img, page}`. The guard must read that actual registry and reconcile its URLs and titles with the evidence. Testing only the sheets could pass while the merged gallery contains a wrong image. Namespace accession identifiers by museum, and use a stable fallback identity with a separate explanation; `"fallback:<reason>"` alone does not establish work identity.

- **Assign influence integration explicitly.** Your final ownership list omits `js/influences.js`. Commit `26309bb` changed it, and `docs/ROSTER_E3.md §3` describes the batch’s eight grounded edges. Claude should own adding whichever edges survive research, followed by the grounding check; no edge quota is needed.

One operational correction: this session is **read-only**, not workspace-write. I can review evidence and provide draft records/tests, but cannot save them here under the current permissions.

With those adjustments, I have no further substantive disagreement.

AGREE
## Synthesis (Claude, as tiebreaker)
- Roster: the 20 in round 2, research-gated before prose (Reverón later failed and was replaced by Michelena).
- Claude: evidence sheets for all 20, taxonomy, artworks merge (parse + re-serialise), influences, index.html, stubs/sitemap, ARTIST_BATCH_21 ledger, batch doc with a ready-to-paste PINNED block; records 1–10; single integrator of js/artists-21.js.
- Codex (workspace-write): records 11–20 as a fragment, only from fetched sources; claims for those sheets; tests/test_artist_batch_21.py reading the shipped registries.
- Tiebreak on pins: no sealed file is edited in this autonomous run; the packages are reported complete EXCEPT the pins (open owner item).

## Build notes
- Codex completed its build turn and then hit its usage limit (resets 5:25 PM) before writing a summary; its files were verified from git status and by re-running every check, not from a self-report.
- Codex's final cross-review pass could not run for the same reason (see the session report).
