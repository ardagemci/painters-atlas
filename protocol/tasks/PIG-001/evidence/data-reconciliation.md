# PIG-001 — Data reconciliation, language sweep, and test resolution

**Unit 35 · Seurat (Data and Copyright Steward) · 2026-08-05**
**Measured at:** `a1b822b` (`PIG-001 unit 34: record the build commit sha in the log`), branch `pig-001-stabilization`, 91 commits from `effa805`.
**Ledger reference:** D-019.

This document answers requested actions 4, 5, 6 and 7 of the round-3 theoretical
review (`messages/007-review.json`). It is one authoritative reconciliation: every
figure below carries a value, the commit and date it was measured at, the surface
it counts, and its exact meaning.

Two standing rules govern everything here:

1. **The `effa805` freeze is immutable.** `evidence/asset-inventory-effa805.json`
   is dated evidence of a commit and is never edited. Current state is published
   beside it as `evidence/asset-inventory-a1b822b.{json,md}`.
2. **No clearance is claimed anywhere.** Per OD-5 (decided 2026-07-23) and AC12,
   this project records what Wikimedia Commons *asserts*, what the exact-work
   check *confirmed*, and what an audit *could not* establish. It does not make,
   and is not qualified to make, a legal determination in any jurisdiction.

---

## 1. Denominator glossary

The review asked for 799/798/797, 694/693, 104/103, 29/28/27, 695/679 and 66/60
to be bound to commit, date, surface and meaning. Most of these pairs are not
inconsistencies — they are *different quantities*, or the same quantity at
different dates. Two are genuine errors and are marked **ERROR** below.

### 1.1 Whole-repository asset totals

| Value | Commit | Date | Surface | Exact meaning |
| ---: | --- | --- | --- | --- |
| **799** | `effa805` | 2026-07-23 | all public surfaces | `total_unique` — unique `upload.wikimedia.org` URL strings across catalog ∪ gallery ∪ museum ∪ stub metadata ∪ homepage metadata. The frozen baseline. |
| **798** | `effa805` | 2026-07-23 | rendered surfaces | `rendered_unique` — the subset the app actually renders (catalog ∪ gallery ∪ museum). One asset is metadata-only. |
| **798** | `a1b822b` | 2026-08-05 | all public surfaces | `total_unique` **now**. Collides in value with the row above and means something different. 799 → 797 by the rights corrections, then 797 → 798 by one content-lane addition. |
| **797** | `a1b822b` | 2026-08-05 | rendered surfaces | `rendered_unique` **now**. |
| **797** | — | 2026-07-25 → 2026-08-05 | test expectation | The *stale* expected `total_unique` in `tests/test_rights_tooling.py`. Correct for the corrected tree before `ef8b2b3`; superseded. **Re-frozen to 798** — see §3. |
| **1** | both | — | metadata only | `metadata_only_unique` — the homepage `og:image`, referenced in `index.html` but never rendered in-app. Unchanged throughout. |

**Reading the collision:** 798 is simultaneously the *old rendered* total and the
*new overall* total. That is a coincidence of arithmetic, not a mistake, and it is
the single likeliest number in this project to be misread. Always pair 798 with
its surface.

### 1.2 Artwork-only counts (the 694 family)

Artwork-only = catalog ∪ gallery, i.e. renderable images of *artworks*, excluding
museum building photographs.

| Value | Commit | Date | Derivation | Meaning |
| ---: | --- | --- | --- | --- |
| **695** | `effa805` | 2026-07-23 | 257 ∪ 529, overlap **91** | Artwork-only unique assets at the freeze. |
| **694** | census tree | 2026-07-24 | 257 ∪ 529, overlap **92** | Artwork-only at the rights census. The overlap moved 91 → 92 when a corrected catalog image became identical to a gallery image already present. |
| **693** | `a1b822b` | 2026-08-05 | 257 ∪ 528, overlap **92** | Artwork-only **now**, after one duplicate gallery record (Bada Shanren, "Two Birds") was removed. |

**ERROR corrected.** `build-evidence-report.md` said "a census of **all 694**
renderable images" in the present tense. 694 was true on 2026-07-24 and is not
true now. This was an error of tense, not of census; the finding the sentence
carries (29 attribution-required images, not 2) stands as a dated result. The
report now reads "the 694 renderable images *as counted on 2026-07-24* (693 at
`a1b822b`)". The liaison's arithmetic check (`257 ∪ 529 − 92 = 694`) is confirmed;
this reconciliation adds the `effa805` point (695, overlap 91) that neither pole
had measured.

### 1.3 The 695 / 679 pair — a true value collision

| Value | Commit | Date | Surface | Meaning |
| ---: | --- | --- | --- | --- |
| **679** | `effa805` | 2026-07-23 | `p/**` | Prerendered stub **files** on disk. |
| **695** | `a1b822b` | 2026-08-05 | `p/**` | Prerendered stub **files** now — +16 from `ef8b2b3` (9 artist stubs, 6 artwork stubs, 1 museum stub). |
| **695** | `effa805` | 2026-07-23 | catalog ∪ gallery | Artwork-only unique **assets** (§1.2). |

695 is therefore two entirely unrelated quantities — a *file* count today and an
*asset* count at the freeze. They are not a discrepancy and neither is wrong.
This row exists because an unexplained "695 vs 679" reads as sloppiness.

### 1.4 Per-surface counts

| Value | Commit | Date | Surface | Meaning |
| ---: | --- | --- | --- | --- |
| **257** | both | — | `catalog_pd_rendered` | Catalog works with `image.status:"pd"` and a Commons URL. Count unchanged from `effa805`; **membership changed** (two rights corrections), fully ledgered. |
| **529** | `effa805` | 2026-07-23 | `gallery_rendered` | Artist-page gallery images at the freeze. |
| **528** | `a1b822b` | 2026-08-05 | `gallery_rendered` | Now: −6 / +5 against the freeze, all ledgered (§3). |
| **532** | pre-`effa805` | — | `gallery_rendered` | Historical: before three Kahlo records and one duplicate were removed. Appears only in an older test comment. |
| **103** | `effa805` | 2026-07-23 | `museum_photos_rendered` | Museum building photographs. |
| **104** | `a1b822b` | 2026-08-05 | `museum_photos_rendered` | Now: +1, the Hirshhorn Museum and Sculpture Garden photograph, from `ef8b2b3`. Also the count of `museum notes` and of `PHOTO_CREDITS` entries — all three are 1:1 by construction. |
| **502** | `effa805` | 2026-07-23 | `prerender_metadata_refs` | Unique assets referenced by `og:image`/`twitter:image` in `p/**`. |
| **502** | `a1b822b` | 2026-08-05 | `prerender_metadata_refs` | Same **count**, different **membership**: +5 / −5 (four rights corrections plus Hirshhorn; five superseded URLs retired). Count stability here hid real drift, which is why the test compares members, not totals. |
| **92** | `a1b822b` | 2026-08-05 | catalog ∩ gallery | URLs on both surfaces. Was 91 at `effa805`. |
| **0** | both | — | leakage | `suppressed_leaking_into_metadata` — copyright-suppressed URLs reaching public stub metadata. Must stay 0; asserted by test. |

### 1.5 Tier 1 and the daily pool — three numbers, all correct

| Value | Commit | Date | Surface | Meaning |
| ---: | --- | --- | --- | --- |
| **76** | `a1b822b` | 2026-08-05 | `js/catalog-*.js` | Catalog records with `tier:1`, regardless of image status. What the JXA validator reports as `tier1`. |
| **75** | `a1b822b` | 2026-08-05 | rights sample, `surface == "catalog"` | Tier 1 records **that have an image asset**. `tools/rights_register.py::_catalog_records()` admits only records carrying a Commons URL, so this counts works there is something to register rights *for*. |
| **75** | `a1b822b` | 2026-08-05 | daily pool | The rotating daily-work pool. A third quantity that happens to equal the second. |

**The theory pole's 76-vs-75 finding had the right remedy and the wrong
diagnosis, and the record should say so.** Their claim was that "the rights
sample tooling and tests still encode a 75-work Tier 1 or daily assumption",
framed as a defect. It is not: the tooling's 75 is a different and correct
quantity, and the assertion encoding it (`tests/test_rights_tooling.py`, "Tier 1
∪ daily pool is 75 works") **passes and was never among the five failures**.

What was genuinely owed is the AC11 disposition of the 76th record, now given:

> **AC11 no-asset disposition — `beginning-noland`.** Kenneth Noland,
> *Beginning* (1958), Hirshhorn Museum and Sculpture Garden; added by `ef8b2b3`.
> Noland died in 2010, so on the ordinary term arithmetic no public-domain basis
> is assertable. The record carries `image:{status:"copyright"}` and **no `src`
> field**; `js/app.js` renders it as a plain title row with no image and no
> generative cover posing as one. **There is no asset, therefore nothing to
> register rights for** — this is a no-asset disposition, not an unresolved one.
> It is asserted rather than inferred by
> `test_the_tier1_record_with_no_asset_is_dispositioned_not_counted_away`, which
> also checks that the record leaks onto no rendered or metadata surface.

### 1.6 Attribution figures (the 29/28/27 family)

| Value | Commit | Date | Surface | Meaning |
| ---: | --- | --- | --- | --- |
| **2** | pre-census | — | 122-record sample | Attribution-required artwork images believed to exist, from the superseded sample. |
| **29** | census tree | 2026-07-24 | artwork census | Attribution-required **artwork images** found by the full census. A dated finding. |
| **28** | unit 24 tree | 2026-07-25 | `IMAGE_CREDITS` | After the census, recorded in `evidence/build-log-unit-24.md`. |
| **27** | `a1b822b` | 2026-08-05 | `IMAGE_CREDITS` | Now, after the half-applied Sistine swap was completed (D-016) and the replacement carried no photographer claim. What the validator reports as `artwork image credits`. |
| **88** | `a1b822b` | 2026-08-05 | `PHOTO_CREDITS` | **Museum photographs** requiring attribution — a fourth number in the same family, omitted from the review's list. Not comparable to 27: different surface. |
| **104** | `a1b822b` | 2026-08-05 | `PHOTO_CREDITS` | All museum photograph credits (88 required + 16 courtesy). |
| **131** | `a1b822b` | 2026-08-05 | both registries | Total rendered credits: 104 museum + 27 artwork. |

### 1.7 Copyright-suppressed records (66 / 60)

| Value | Commit | Date | Surface | Meaning |
| ---: | --- | --- | --- | --- |
| **60** | `effa805` | 2026-07-23 | `js/catalog-*.js` | Catalog records with `image.status:"copyright"` — works that may not be rendered. |
| **66** | `a1b822b` | 2026-08-05 | `js/catalog-*.js` | Now: +6 from `ef8b2b3` — `beginning-noland`, `chief-kline`, `city-limits-guston`, `elegy-to-the-spanish-republic-108`, `mars-dust`, `the-gate-hofmann`. All six are 20th-century works carrying no `src`. |
| **60** | — | — | test expectation | The *stale* expectation at `tests/test_rights_tooling.py`. **Re-frozen to 66** — see §3. |

A rise in this figure is correct behaviour, not a regression: it means six works
that may not be rendered were *recorded as such* rather than quietly given an
image.

**The theory pole listed 66-vs-60 among the five reproduced failures; the liaison
was right that it was latent, not live** — the assertion sits after an earlier
assertion in the same test method that aborted first. It is now fixed together
with that earlier line, so no sixth failure surfaces.

### 1.8 Commit counts

| Value | Meaning |
| ---: | --- |
| **75** | `effa805..5c684ae` — the last *build* commit at the time the implementation report was written. What the report claimed. |
| **76** | `effa805..55fb166` — the SHA actually routed. |
| **91** | `effa805..a1b822b` — **current**, this measurement. |

The report's "75 commits" was true of a commit other than the one transmitted. It
is stale again now, which is the structural point: a commit count is only
meaningful beside the SHA it was computed against. Every figure in this document
names its commit for that reason.

---

## 2. Language sweep (OD-5 / AC12)

### 2.1 What the breach was

OD-5 binds this project to record *asserted basis, attribution and residual
uncertainty, never clearance*. The implementation report described images with
two phrases — struck and preserved as rows 1 and 2 of §2.3 below — that assert a
legal status this project has never established. **The theory pole is right and
the finding is conceded without qualification.**

The instructive detail is *where* it broke. `TestRegisterLanguage` enforces
exactly this restraint on the machine-generated register — "the register may say
asserted; it may never say cleared" — and it has always passed. The rule broke
only in human-written prose, which no test read. **A rule enforced only where a
test looks is not enforced.**

### 2.2 The structural fix

`tests/test_rights_tooling.py` gains **`TestProseLanguage`**, which reads the
prose this pole authors — `build-evidence-report.md`, `evidence/**`, `docs/**`,
`tools/**`, `tests/**`, `README.md` — and fails on ten patterns of legal
assertion. It ships with:

- a **negative fixture**: the six exact strings that reached the routed report
  must all be caught, so a guard that cannot fail is rejected;
- a **positive fixture**: bounded phrasing ("Commons metadata asserts…", "the
  exact-work check confirmed…", "this audit's searches located no candidate")
  must *not* be flagged, so the guard cannot push authors away from the wording
  it exists to encourage;
- a **pinned exemption map**: a line may carry a banned phrase only if it is a
  blockquote, contains strikethrough, or carries the literal marker
  `OD5-EXEMPT`; the count of markers per file is pinned, so widening the hole is
  itself a test failure rather than a quiet edit.

Incoming theory messages, liaison analyses and the frozen specification are
**out of scope by design**: they quote the banned phrases in order to object to
them or forbid them, and they are history that must not be rewritten.

### 2.3 Corrections made — 14 sites

History is not rewritten. Where a superseded claim sits in a committed artifact,
the original wording is preserved beside a dated correction; only live code
comments and generator templates are edited in place.

| # | File | Was | Now | Form |
| --- | --- | --- | --- | --- |
| 1 | `build-evidence-report.md` body | ~~"three replaced with verified-PD files"~~ | struck; "three replaced" | strikethrough + `CORRECTION` block |
| 2 | `build-evidence-report.md` body | ~~"replaced with genuinely PD images"~~ | struck; "files whose Commons metadata asserts a public-domain basis" | strikethrough + `CORRECTION` block |
| 3 | `build-evidence-report.md` body | ~~"a census of all 694 renderable images"~~ | "the 694 renderable images *as counted on 2026-07-24*" | strikethrough + `CORRECTION` block |
| 4 | `build-evidence-report.md` front-matter `proposal:` | ~~carried both phrases uncorrected~~ | bounded text + pointer to the preserved wording | in-place; the field duplicated the body and contradicted it |
| 5 | `evidence/rights-register.md` §Dispositions | ~~"her *works* remain in copyright"; "No public-domain image of a Kahlo painting exists on Commons"~~ | term arithmetic; "this audit's Commons searches located no candidate that passes the exact-work check" | in-place + `CORRECTION` block |
| 6 | `evidence/rights-register.md` §Systemic 1 | ~~"*The Snail* is PD in France only from 2025 and remains under US copyright until 2049"~~ | published term arithmetic, explicitly not a determination | in-place + `CORRECTION` block |
| 7 | `evidence/rights-register.md` §Systemic 3 | ~~"a verified PD scan"~~ | "a file whose Commons metadata asserts a public-domain basis" | in-place |
| 8 | `evidence/rights-remediation.md` | ~~"genuinely public-domain images"~~ | "images carrying a Commons public-domain assertion" | in-place |
| 9 | `evidence/build-log-unit-24.md` | ~~"most images are public domain"~~ | "most images carry a Commons public-domain assertion" | in-place + `CORRECTION` block |
| 10 | `tools/fetch_artworks.py` docstring | ~~"Commons enforces public-domain status in the US and the source country"~~ | Commons policy requires a basis to be *asserted*; not a determination by Commons or by this project | in-place |
| 11 | `tools/fetch_artworks.py` `SUPPRESS` | ~~"works still in copyright"; "No PD image exists on Commons"~~ | term arithmetic; bounded to this audit's logged searches | in-place + dated note |
| 12 | `tools/audit_artworks.py` pin comment | ~~"Verified exact-match + PD before pinning"~~ | exact-work check passed; file page asserts a PD basis; no legal determination | in-place |
| 13 | `tools/build_photo_credits.py` `HEADER` | ~~"are public-domain or CC0"; "Public-domain and CC0 images…"~~ | "carry a Commons public-domain or CC0 assertion"; plus an explicit no-clearance line in the generated file | in-place; **`js/photo-credits.js` regenerated** |
| 14 | `docs/STYLE_GUIDE.md` §4.4 rule 4 | ~~"We show public-domain works and say so"~~ | show works whose Commons metadata *asserts* a PD basis; never write "is public domain", "is cleared", "is verified PD" | in-place |

Additionally `docs/ARTWORK_SCHEMA.md` now states that `status:"pd"` is a
*rendering* token, not a legal finding — closing the path by which a machine
token was read back into prose as a claim.

`js/photo-credits.js` was regenerated from the corrected template. **The credit
data is byte-identical** (104 venues / 88 requiring attribution / 16 courtesy; 27
artwork credits); only the header language and generation date changed.

---

## 3. Test resolution — 41 tests with 5 failures → 46 tests, all passing

No expectation was loosened and no assertion was deleted. Every changed
expectation carries its reason in the test file itself, and the membership
comparison that catches undocumented drift is unchanged and still strict.

### 3.1 The two ledgers

The pre-existing `CORRECTIONS` ledger records images changed **because they were
wrong**. Corpus growth is a different kind of event, so it gets its own ledger,
`CONTENT_LANE`, rather than being folded in. Conflating them would let real
growth hide inside a rights-remediation entry, or the reverse.

Both ledgers trace to causes already recorded: D-016 (`ef8b2b3`, the independent
content lane) and the AC11 rights register.

### 3.2 Every changed expectation and its reason

| Failure | Was | Now | Reason |
| --- | ---: | ---: | --- |
| `gallery_rendered` membership | Sistine pair unledgered | pair added to `CORRECTIONS` | **A ledger omission, not drift.** The Sistine swap was ledgered for `catalog_pd_rendered` and `prerender_metadata_refs` but not for this surface, because when the ledger was written the swap was only half-applied — `js/artworks.js` still carried the CC BY-SA 3.0 in-situ photograph. Commit `d7675dd` completed it (D-016) and the ledger was never extended. The test was failing on a correction we had actually made. |
| `museum_photos_rendered` membership | 103 expected | +1 via `CONTENT_LANE` | The Hirshhorn photograph, from `ef8b2b3`. Rights covered in `museum-photo-rights.json` (Quadell, CC BY-SA 3.0, attribution required); credited in `js/photo-credits.js` with `required:true`. |
| `prerender_metadata_refs` membership | 501 expected | +1 via `CONTENT_LANE` | The same Hirshhorn photograph, reached through `p/museum/hirshhorn.html`'s `og:image`. One asset, two surfaces. |
| `total_unique` | 797 | **798** | The same one Hirshhorn asset. It is the *only* new public image asset in the entire content lane. |
| `rendered_unique` | 796 | **797** | Same asset. |
| `museum` surface (`TestSampleBasis`) | 103 | **104** | Same asset, counted through `rights_register.SURFACES`. |
| `copyright_refs` (**latent**) | 60 | **66** | The six new 20th-century works from `ef8b2b3`, all `status:"copyright"` with no `src`. This assertion was never reached because `total_unique` aborted the method first; fixed in the same pass so no sixth failure surfaces. |

Unchanged and still asserted: `metadata_only_unique` 1, `catalog_gallery_overlap`
92, `suppressed_leaking_into_metadata` 0, catalog surface 257, gallery surface
528, Tier-1-with-asset 75.

### 3.3 Correcting a mis-identification in the record

Both the theory pole's failure output and the liaison's analysis identify the
added museum photograph as **Guggenheim**. It is **Hirshhorn**. The Guggenheim
photograph is present in the `effa805` freeze and did not change. The error comes
from reading `unittest`'s "first extra element" — a positional artefact of
comparing two *sorted lists* — as though it were the set difference. The set
difference, which is authoritative, is the Hirshhorn exterior photograph. The
remedy is unaffected; the identification is corrected here so the record is right.

### 3.4 New tests (41 → 46)

| Test | Purpose |
| --- | --- |
| `TestProseLanguage.test_no_artifact_of_ours_asserts_a_legal_conclusion` | Enforces OD-5 on prose, where the rule actually broke. |
| `TestProseLanguage.test_the_guard_actually_catches_the_phrases_that_got_through` | Negative fixture — the six real strings. |
| `TestProseLanguage.test_bounded_language_is_not_flagged` | Positive fixture — bounded wording must pass. |
| `TestProseLanguage.test_exemption_markers_are_pinned` | Makes widening the exemption a visible failure. |
| `TestSampleBasis.test_the_tier1_record_with_no_asset_is_dispositioned_not_counted_away` | Asserts the `beginning-noland` AC11 disposition and its non-leakage. |

The guard caught **five breaches that a hand-written grep had missed**, including
one in a file this unit had already corrected once, and one in this unit's own
first draft of a correction. That is the argument for the test, made by the test.

---

## 4. Inventory regeneration

- **Regenerated:** `evidence/asset-inventory-a1b822b.{json,md}` from the current
  tree. Reproducible with
  `python3 tools/asset_inventory.py --out-json … --out-md …` (stdlib only, no
  network, static analysis).
- **Preserved:** `evidence/asset-inventory-effa805.{json,md}` untouched, byte-stable.
- **Comparison:** `python3 tools/asset_inventory.py --compare
  protocol/tasks/PIG-001/evidence/asset-inventory-effa805.json` reports **4
  drifted surfaces**, and every single `+`/`−` line is accounted for by
  `CORRECTIONS` or `CONTENT_LANE`. The reproduction test proves this
  exhaustively rather than by inspection.

### 4.1 Every delta from the `effa805` freeze

| Surface | Freeze | Now | Δ | Cause |
| --- | ---: | ---: | --- | --- |
| `catalog_pd_rendered` | 257 | 257 | +2 / −2 | Rights corrections: Hokusai filename normalisation; Sistine photographer-copyright swap. |
| `catalog_copyright_suppressed` | 0 | 0 | — | No copyright record has ever carried a URL. |
| `gallery_rendered` | 529 | 528 | +5 / −6 | Four wrong-artwork removals (Ducreux, Kahlo column, Aleppo folio, Kahlo sculpture), the Correggio and Sistine photographer-copyright swaps, and one duplicate removal. |
| `museum_photos_rendered` | 103 | 104 | +1 | `ef8b2b3` — Hirshhorn. |
| `prerender_metadata_refs` | 502 | 502 | +5 / −5 | The four rights corrections re-emitted into `p/**`, plus Hirshhorn; five superseded URLs retired. Equal totals, changed membership. |
| `homepage_metadata_refs` | 1 | 1 | — | Unchanged. |
| `copyright_refs` | 60 | 66 | +6 | `ef8b2b3` — six 20th-century works, no assets. |
| `stub_files` | 679 | 695 | +16 | `ef8b2b3` — 9 artist, 6 artwork, 1 museum stub. |

**One commit, `ef8b2b3`, explains every non-corrective delta.** It is already
ledgered as D-016 (Gate 4 partial breach, benign): an independent content lane
that landed on this branch mid-build, moving artists 247→256, movements 75→76,
catalog 317→323, venues 115→116, museum notes 103→104, influence edges 225→238.

### 4.2 Rights coverage after the growth

Checked rather than assumed: **every record in the current 100-record AC11 sample
is already present in the 122-record register** (`evidence/rights-register.json`).
The content lane opened no gap in artwork rights coverage, because it added no
artwork *images* — its six catalog works are all copyright-suppressed with no
`src`. The single new asset is a museum photograph, and it is covered in
`museum-photo-rights.json` and credited in `js/photo-credits.js`.

- **Validator:** `ALL REFERENCES VALID`, **zero warnings**, at `a1b822b` and
  after regeneration. This is load-bearing: the validator now treats an
  uncredited attribution-required photograph as an **error**, so a green run is
  positive evidence that the 88 attribution-required museum photographs and 27
  artwork images all carry credits.

---

## 5. Still open — named precisely

1. **`js/app.js:2393` ships an OD-5 breach on a production surface.** The credits
   page lede reads, verbatim:

   > Most reproductions here are public domain.

   That is a bare legal assertion with no hedge, rendered to users. `js/app.js:2377`
   is weaker but related — it says the paintings are "old enough to be in the
   public domain" — though it does at least end with an explicit no-clearance
   disclaimer. **This unit does not own
   `js/app.js`** — it is frozen behind another unit's contrast and screenshot
   evidence — so the lines were left untouched and are reported instead.
   Suggested wording: "Most reproductions here carry a public-domain assertion
   from Wikimedia Commons." Until it is changed, `TestProseLanguage` deliberately
   does **not** scan `js/`, so this breach is recorded here rather than enforced.
   **Whoever next owns `js/app.js` should fix this line and add `js/app.js` to
   `TestProseLanguage.SCANNED`.**
2. **The prose guard's scope is bounded to this pole's own artifacts.** It does
   not read `PIGMENT.md`, `CLAUDE.md`, the coordinator, or `js/`. Extending it is
   cheap; it was left narrow so that it passes honestly today rather than
   requiring exemptions to go green.
3. **`minneapolis-institute-of-art` has no recorded photograph author.** Flagged
   by `build_photo_credits.py` on every run. It is not an attribution-required
   photograph, so the validator does not error, but the credit is thinner than
   its neighbours.
4. **The 122-record register is a superset of, not a re-run at, `a1b822b`.** No
   Commons re-fetch was performed in this unit; coverage was verified by record
   identity, not by re-reading Commons metadata. Licence assertions therefore
   date from 2026-07-25. Re-running `tools/rights_register.py` requires network
   access and would be the stronger evidence.
5. **Not in this unit's scope and still open:** AC15 (no assistive-technology
   observation exists; not producible by an agent), the AC19 perimeter, the stale
   Gate 2 Quality Review, and the D-017 governance disposition.
