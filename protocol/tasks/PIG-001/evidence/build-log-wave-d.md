# PIG-001 — Build Evidence Report, Wave D (units 16, 20, 21)

**Author:** Dürer (`claude-implementation-lead`), Implementation Lead
**Date:** 2026-07-25
**Branch:** `pig-001-stabilization` (verified; never `main`; not pushed by this wave)
**Gate 1:** VERIFIED — `protocol/tasks/PIG-001/specification.md` line 8 reads
`workflow_state: "approved_for_build"`.
**Binding inputs honored:** `owner-decisions-r2.md` OD-1, OD-3, OD-5.
**Gate 2:** NOT certified here. That is Van Eyck's call, not mine.

| Unit | Commit | Summary |
| --- | --- | --- |
| 20 | `83e95e82fe01f21385ca0da45a7873534f1141c1` | Self-host the fonts; remove the last third-party runtime host |
| 16 | `33400a77adc111d9bd0d7388a80c3920016d6cec` | Rights-register tooling: `extmetadata`, register, inventory regenerator, 24 tests |
| 21 | `62fac35ca5b8ec3c4a4c232cc1ec95e9de75f586` | Documentation corrections + deferred-promise register |

Diffstat across the wave: 22 files, +1651 / −32 (6 of the additions are font
binaries, 228,780 bytes total).

Validator run after **every** unit, unedited each time:

```
app.js: syntax OK
artists: 247, movements: 75, techniques: 39, eras: 8, nations: 37, painter styles: 27, influence edges: 225, venues: 115, catalog: 317 (tier1: 75), daily pool: 75, museum notes: 103, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
WARNINGS:
  deck pool: <2 works with E<=-40
  deck pool: empty F×D quadrant 1,-1
ALL REFERENCES VALID
```

The two warnings are the pre-existing deck-pool coverage warnings that unit 22
(AC3, Seurat + Van Gogh editorial review) exists to resolve. Wave D neither
introduced nor silenced them. No coordinate was touched.

Python test suite: `python3 -m unittest discover -s tests` → **35 tests, OK**
(24 new in `tests/test_rights_tooling.py`, 11 pre-existing coordinator tests
unchanged and still passing).

---

## Unit 20 — Google Fonts self-hosting (OD-3, AC25)

**Commit** `83e95e8` · **Files:** `index.html`, `css/styles.css`,
`assets/fonts/` (9 new files: 6 woff2 + `LICENSE.md` + 2 OFL texts)

### What changed

`index.html:19-21` held two `preconnect` hints and a remote stylesheet from
`fonts.googleapis.com`. On a product whose entire premise is accountless,
local and untracked, that was the one place a visitor's browser talked to
someone else. OD-3 decided self-host; this executes it.

1. **Determined actual usage.** The remote request was
   `Playfair Display:ital,wght@0,400;0,600;0,800;1,400` and
   `Inter:wght@300;400;500;600`. Grep confirms both are load-bearing:
   `--serif` (`css/styles.css:26`) and `--sans` (`:27`) are referenced at 40+
   sites. Weights used in CSS: 300, 400, 500, 600, 700, 800.
2. **Character audit before downloading anything.** A scan of `index.html`,
   `css/` and every `js/*.js` found latin-ext (1069 occurrences: `ğ İ ı ł ń Ō
   ō Ş ş š ū ǐ ç é ö ü ß …`) and general punctuation, and **zero** Cyrillic,
   Greek or Vietnamese codepoints. Only the `latin` and `latin-ext` subsets
   were fetched — 12 of Google's 44 `@font-face` blocks discarded as weight
   nobody would ever download.
3. **Both families turned out to be variable fonts.** The 16 kept blocks
   resolve to only **6 unique binaries** (one per family × style × subset).
4. **Licences verified before committing** (see record below).
5. **`css/styles.css`** gained 16 `@font-face` rules whose
   `font-family`/`font-style`/`font-weight`/`unicode-range` descriptors are
   copied **verbatim** from the Google `css2` response, plus
   `font-display:swap`, with `src:url('../assets/fonts/…') format('woff2')`.
6. **`index.html`** dropped both preconnects and the stylesheet link, and
   preloads the two `latin` binaries first paint needs. `css/styles.css?v=`
   bumped `20260724-pig001` → `20260725-pig001d`.

### Licence record (AC25 / OD-3)

| | Playfair Display | Inter |
| --- | --- | --- |
| Licence | **SIL Open Font License, Version 1.1** | **SIL Open Font License, Version 1.1** |
| Copyright | Copyright 2017 The Playfair Display Project Authors (https://github.com/clauseggers/Playfair-Display), with Reserved Font Name "Playfair Display" | Copyright 2020 The Inter Project Authors (https://github.com/rsms/inter) |
| Designer | Claus Eggers Sørensen | Rasmus Andersson |
| Binary version | `v40` | `v20` |
| Licence source | `https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/OFL.txt` | `https://raw.githubusercontent.com/google/fonts/main/ofl/inter/OFL.txt` |
| Metadata confirmation | `https://fonts.google.com/metadata/fonts/Playfair%20Display` → `license: ofl`, last modified 2025-09-11 | `https://fonts.google.com/metadata/fonts/Inter` → `license: ofl`, last modified 2025-09-10 |
| Binary source | `fonts.gstatic.com/s/playfairdisplay/v40/…` | `fonts.gstatic.com/s/inter/v20/…` |

Both licences are OFL 1.1, confirmed two ways: the Google Fonts metadata API
reports `license: ofl` for each family, and the upstream `google/fonts` OFL
headers (committed verbatim as `assets/fonts/OFL-Playfair-Display.txt` and
`assets/fonts/OFL-Inter.txt`) state "This Font Software is licensed under the
SIL Open Font License, Version 1.1." Redistribution is therefore permitted.
Playfair Display carries a **Reserved Font Name**; the RFN clause restricts
*modified* versions from using the name, and these files are unmodified and
keep the original name, so the clause is satisfied. Neither family is
non-OFL, so the STOP-and-report branch of the brief was not triggered.

Files committed, with integrity hashes (full table in `assets/fonts/LICENSE.md`):

| File | Bytes | SHA-256 (first 16) |
| --- | --- | --- |
| `inter-normal-latin.woff2` | 48,432 | `c940764593d0fe5d` |
| `inter-normal-latin-ext.woff2` | 85,272 | `a28eb6d3ccb534ae` |
| `playfair-display-normal-latin.woff2` | 38,460 | `5d91eb5d522a0308` |
| `playfair-display-normal-latin-ext.woff2` | 20,980 | `5628567856d60d71` |
| `playfair-display-italic-latin.woff2` | 21,952 | `ce3932af6f6a6c73` |
| `playfair-display-italic-latin-ext.woff2` | 13,684 | `ac9c3bcc1848b07c` |

All six verified to carry the `wOF2` magic and a `0x00010000` TrueType flavor
before being committed. Nothing downloaded was executed.

### Third-party host verification (AC25)

Grep for `googleapis` and `gstatic` across `index.html`, `css/`, `js/`, `p/`
and `tools/` returns exactly one hit — the explanatory comment at
`css/styles.css:9` recording where the binaries came from. No link, no
`@import`, no `src`, no `preconnect`.

Full external-host inventory of `index.html` + `css/` + `js/app.js` after the
change:

| Host | Kind | Runtime request? |
| --- | --- | --- |
| `www.w3.org` | SVG XML namespace string | No — never fetched |
| `ardagemci.github.io` | own canonical / `og:url` | First-party |
| `upload.wikimedia.org` | `og:image` / `twitter:image` metadata | Crawl-time only, from `index.html` |

Served locally (`python3 -m http.server 8421 -d .`): homepage 200; all six
font files 200 with `Content-Type: font/woff2`; the served homepage HTML
references no Google host.

### Deviation / finding — AC25's frozen inventory is incomplete (Gate 3)

**Recorded, not fixed.** The frozen spec states the runtime third-party
request inventory is "exactly two hosts, fonts.googleapis.com and
fonts.gstatic.com", and treats `upload.wikimedia.org` as metadata-only. That
is true of `index.html`. It is **not** true of the application: the catalog,
gallery and museum data carry **892 `upload.wikimedia.org` URLs** across
`js/catalog-1.js`, `js/catalog-3.js`, `js/catalog-4.js`, `js/artworks.js` and
`js/museums-1.js`, and `js/app.js` renders them as `<img src>` at 12+ sites
(`:804`, `:1318`, `:1368`, `:1445`, `:1475`, `:1494`, `:1517`, `:1628`, …).
Every visitor who opens an artist or artwork page makes third-party requests
to Wikimedia.

So after unit 20 the honest claim is: **zero third-party requests remain for
fonts, and Wikimedia remains a third-party runtime image host by design.** I
have not "verified zero third-party requests" in the absolute sense the brief
asks for, because that statement would be false, and this is exactly the kind
of overclaim AC14 exists to prevent.

Not fixed here, deliberately: hosting 892 images locally would mean
re-committing the entire image corpus, breaking the Commons attribution and
sourcing model that PIGMENT.md §14 depends on, and is far outside a
stabilization unit. **Escalated** for the AC25 disposition — the owner and the
privacy reviewer should decide about Wikimedia knowingly, as they did about
Google Fonts, rather than inherit an inventory that omitted it.

### Rendering-regression check

`font-weight:700` appears twice (`.main-nav a.active` `css/styles.css:131`,
`.tone.on::after` `:983`), both in `--sans` context. 700 was never requested
from Google either, so CSS font matching resolved it to Inter 600 before this
change. Because the self-hosted declarations pin the same discrete weights,
it still resolves to 600 — no synthetic bolding introduced, no substitution.
Italic behaviour is likewise unchanged: Playfair italic 400 ships; the
sans-italic sites (`.card-tagline` etc.) were synthesised obliques before and
remain so. Glyphs outside latin/latin-ext (arrows, `✓`, flag emoji) fell back
to system fonts before and still do — those subsets were never downloaded.

**Not verified by me:** pixel-level visual confirmation in a real browser at
both themes. That is Vermeer's evidence pass. What I can attest is that the
descriptors are byte-identical in every rendering-relevant field.

### Self-assessment

- **AC25** — *disclosure half:* PASS. Full runtime-request inventory produced,
  including the correction above. *Disposition half:* the Google Fonts
  decision (OD-3) is executed and the hosts are gone. The Wikimedia
  disposition is newly surfaced and **open**, pending owner + privacy
  reviewer. AC25 should not be marked satisfied until that is decided.

---

## Unit 16 — Rights-register tooling (AC10–AC12, supports OD-5)

**Commit** `33400a7` · **Files:** `tools/commons_rights.py` (new),
`tools/rights_register.py` (new), `tools/asset_inventory.py` (new),
`tools/fetch_artworks.py`, `tools/audit_artworks.py`,
`tests/test_rights_tooling.py` (new)

Scope held as briefed: **tooling only.** No full-corpus harvest was run.
Seurat runs the register.

### `extmetadata` extension

Verified premise before editing: `tools/fetch_artworks.py:49` and
`tools/audit_artworks.py:99` requested `iiprop=url|mime`. Both now request
`iiprop=url|mime|extmetadata`, as does `audit_artworks.py`'s PINNED-file
resolver (which previously asked for bare `iiprop=url`). This costs **zero
extra requests** — the parameter rides on queries both tools already make.

Captured per image: `LicenseShortName`, `License`, `LicenseUrl`, `UsageTerms`,
`Artist`, `Credit`, `Attribution`, `AttributionRequired`, `DateTimeOriginal`,
`Copyrighted`, `Restrictions`, `mime`, the direct file URL, and the Commons
**file page** (`descriptionurl`).

The file page is the point of the exercise. The shipped catalog's
`image.page` points at an *English Wikipedia article*
(`https://en.wikipedia.org/wiki/The_Calling_of_Saint_Matthew`), which carries
no licence statement at all. `tools/rights_register.py` records the real
`commons.wikimedia.org/wiki/File:…` page and flags every entry where the two
disagree.

### Rate-limit discipline (enforced in code, not just documented)

`tools/commons_rights.py`:

- process-wide throttle, `MIN_INTERVAL = 0.25`s minimum between any two
  outbound requests;
- 4 attempts with backoff `1 / 3 / 9`s, honouring `Retry-After` when present;
- **a transient failure is never a negative finding.** Timeout, 429, 5xx,
  reset and malformed JSON all produce status `unverified`. Only an explicit
  `missing` page from the API is a definitive negative, and even that is
  reported as `missing`, not as a rights conclusion;
- batching capped at the API's 50-title limit, deduplicated by underlying
  Commons file, so N thumbnail widths of one file cost one lookup;
- the sidecar merge rule: an `unverified` record **never** overwrites an `ok`
  one, so a throttled run cannot erase what an earlier run verified.

`OVERRIDES` and `PINNED` behaviour in `audit_artworks.py` is byte-for-byte
preserved; the only changes inside those branches are the `iiprop` string and
one `capture_from_imageinfo()` call.

### Where captured rights go — deviation (Gate 3)

The brief says "capture, per image". I capture to a **sidecar**
(`tools/rights-cache.json`, overridable via `PIGMENT_RIGHTS_CACHE`) rather
than adding fields to `js/artworks.js`.

Rationale: `js/artworks.js` is a **shipped runtime bundle**. Adding licence
templates, author strings and credit lines for ~530 gallery records would
make every visitor download rights paperwork to look at a painting, for data
that is build-time provenance and never rendered. The evidence obligation is
fully met by the register; the runtime cost is avoided. Reversible — it is a
file path, not a schema decision. Flagged for review rather than assumed.

### Asset-inventory regenerator (AC10)

`tools/asset_inventory.py` regenerates the inventory in the frozen shape and
can diff itself against the freeze (`--compare`). Result against
`evidence/asset-inventory-effa805.json`:

```
  catalog_copyright_suppressed     identical (0)
  catalog_pd_rendered              identical (257)
  gallery_rendered                 identical (529)
  homepage_metadata_refs           identical (1)
  museum_photos_rendered           identical (103)
  prerender_metadata_refs          identical (502)

NO DRIFT — inventory reproduces the frozen copy
```

Headline figures also reproduce: 799 total unique, 798 rendered-in-app, 1
metadata-only, 91 catalog∩gallery overlap, 0 suppressed-asset leakage, 60
copyright records.

**One discrepancy, in the frozen document's favour of brevity:** the frozen
`.md` reports the homepage surface as 1 reference / 1 unique. There are
actually 2 references (`og:image` and `twitter:image`) to 1 unique URL. The
unique count — the figure every downstream total depends on — is correct;
only the reference count was understated by one. The regenerator reports 2.

### Smoke run — proof `extmetadata` actually returns (required evidence)

Two runs, both against the live API, both throttled, 16 records total.

**Run 1 — `python3 tools/rights_register.py --surface catalog --limit 8`**

```
Resolving 8 references / 8 unique Commons files (≥0.25s between requests)
  ... resolved 8 files (ok)

| Measure | Count |
| Entries | 8 |
| Licence asserted by Commons | 8 |
| Unresolved | 0 |
| — of which transient lookup failure (proves nothing) | 0 |
| — of which file reported missing by the API | 0 |
| Entries whose shipped `page` is NOT the Commons file page | 7 |

| Licence (Commons LicenseShortName) | Entries |
| Public domain | 7 |
| CC0 | 1 |

the-calling-of-saint-matthew   CC0            Gleb Simonov         commons.wikimedia.org/wiki/File:Caravaggio_%E2%80%94_The_Calling_of_Saint_Matthew.jpg
judith-slaying-holofernes      Public domain  Artemisia Gentileschi
the-starry-night               Public domain  Vincent van Gogh
sunflowers                     Public domain  Vincent van Gogh
girl-with-a-pearl-earring      Public domain  Johannes Vermeer
the-milkmaid                   Public domain  Johannes Vermeer
las-meninas                    Public domain  Diego Velázquez
the-garden-of-earthly-delights Public domain  Hieronymus Bosch
```

**Run 2 — 8 records from the AC11 sample, weighted to the Matisse/Kahlo
gallery entries OD-5 sends into the register**

```
| Entries | 8 |
| Licence asserted by Commons | 8 |
| Unresolved | 0 |
| Attribution required per Commons | 2 |
| Entries whose shipped `page` is NOT the Commons file page | 5 |

| Public domain | 6 |
| CC BY 2.0    | 1 |
| CC BY-SA 4.0 | 1 |

frida-kahlo::Self-Portrait with Thorn Necklace…  Public domain  Joseph Ducreux    attribution:false
frida-kahlo::The Broken Column                   CC BY 2.0      Andrew Malone     attribution:TRUE
frida-kahlo::The Two Fridas                      CC BY-SA 4.0   Ines Suarez R.    attribution:TRUE
henri-matisse::The Dance                         Public domain  Henri Matisse     attribution:false
henri-matisse::The Red Studio                    Public domain  Henri Matisse     attribution:false
a-bar-at-the-folies-bergere                      Public domain  Édouard Manet
adele-bloch-bauer-i                              Public domain  Gustav Klimt
barge-haulers-on-the-volga                       Public domain  Ilya Repin
```

`extmetadata` returns end to end on both the catalog and gallery paths:
16/16 asserted, 0 unverified, licences and authors and real Commons file
pages captured.

### Material finding for Seurat and OD-5 (not fixed here)

The first eight sample records the tooling touched exposed three shipped
gallery images that are **the wrong artwork entirely**, confirmed against
`js/artworks.js`:

| Shipped as | Actually is | Licence | Attribution required |
| --- | --- | --- | --- |
| Kahlo, *Self-Portrait with Thorn Necklace and Hummingbird* | `File:Joseph_Ducreux_(French)_-_Self-Portrait,_Yawning_-_Google_Art_Project.jpg` | Public domain | no |
| Kahlo, *The Broken Column* | `File:Broken_column_in_Syrakousai.jpg` — a photograph of a broken column in Syracuse | **CC BY 2.0** | **yes** |
| Kahlo, *The Two Fridas* | `File:Closeup_of_Frida_Kahlo_and_Diego_Rivera_Sculpture.jpg` — a photo of a sculpture | **CC BY-SA 4.0** | **yes** |

Two of the three carry attribution-required Creative Commons licences that
Pigment does not honour anywhere in the UI, so this is a rights exposure and
not only an accuracy defect. All three are exactly the failure mode
`audit_artworks.py`'s BLACKLIST/`fname_valid` heuristics are meant to catch
and did not.

Not corrected in this unit: data records are the Data Steward's to change
(CLAUDE.md §2 — Seurat writes data records, Dürer does not), and the fix is
editorial re-resolution, not tooling. **Handed to Seurat as a priority input
to the AC11 register.** Note also that these are Kahlo (d. 1954) and Matisse
(d. 1954) — both inside the ≤1955 filter but among the most contested PD
claims in the corpus, which is precisely why OD-5 routed them into the sample.

### Unit tests

`tests/test_rights_tooling.py`, 24 tests, fully offline (every API call
stubbed). Coverage includes: thumbnail→file-title derivation, rejection of
the non-Commons `/wikipedia/en/` tree, HTML-stripped extmetadata extraction,
absent keys staying empty rather than guessed, the underscore/space title
normalization bug (which this suite caught during development — the first
smoke run silently reported 8/8 unresolved because records were keyed on the
API's normalized title instead of the requested one), transient failure →
`unverified`, `missing` as the only definitive negative, batch capping at 50,
sidecar merge protecting verified data, the frozen-inventory reproduction, the
AC11 sample basis (exactly 100 = 75 Tier 1 + all 7 Matisse/Kahlo gallery
records + 18 stratified), determinism, and an assertion that **the word
"cleared" never appears in generated output**.

### Self-assessment

- **AC10** — PASS. Inventory is now regenerable and provably reproduces the
  freeze on all six surfaces; the frozen document is no longer a one-off.
- **AC11** — tooling PASS, population NOT DONE by design. The sample basis is
  encoded, deterministic and exactly 100. Seurat runs it.
- **AC12** — PASS at the tooling level. `unresolved` is the default; the
  strongest word the code can emit is `asserted-by-commons`; every record
  carries `legal_conclusion: "none"`; a test enforces that "cleared" cannot
  appear. Editorial discipline over the produced register is still a human
  check once the register exists.

---

## Unit 21 — Documentation corrections (AC14, AC26)

**Commit** `62fac35` · **Files:** `PIGMENT.md`, `README.md`,
`docs/ADMIRE_SPEC.md`, `docs/TASTE_MATH.md`, `docs/STYLE_GUIDE.md`,
`index.html`

### (a) The adaptivity claim

`docs/ADMIRE_SPEC.md:100` asserted "deck delivery is **adaptive**". Per the
frozen spec the claim is corrected, not the code. It now describes what ships
— stratified, chosen up front, `buildDeck()` once per session, nothing
re-reads `admired`/`skipped` mid-deck — and points at the new register.
`docs/TASTE_MATH.md` §6's stages 2–4 are relabelled **DESIGNED, NOT SHIPPED**
so the design document stops reading as a description of the engine.

### (b) Stale counts

All figures re-derived from this session's validator run, not copied from the
briefing.

| Claim | Was | Now |
| --- | --- | --- |
| `PIGMENT.md` §12 artists | 235 | 247 |
| `PIGMENT.md` §12 canonical artworks | 314 | 317 |
| `PIGMENT.md` §12 Tier 1 artworks | 73 | 75 |
| `PIGMENT.md` §12 movements | 74 | 75 |
| `PIGMENT.md` §12 influence relationships | 215 | 225 |
| `PIGMENT.md` §12 daily-pool works | 73 | 75 |
| `README.md` painters (×2) | 231 | 247 |
| `README.md` movements | 74 | 75 |
| `README.md` influence relationships | 210 | 225 |
| `README.md` artist file range | `artists-1.js … artists-7.js` | `… artists-16.js` |
| `index.html` meta description | 246 artists / 315 masterpieces | 247 / 317 |

`27 generative painter styles` added to §12 (previously absent). Snapshot
dated **2026-07-25** with the branch named, and both files now state that the
validator is the only current source — so the numbers degrade honestly rather
than silently.

### (c) Deferred-promise register

Created as **`PIGMENT.md` §19** (my call, as the brief permits — it lives next
to §15's "known gaps" and §16's priorities, which are the two things a reader
would otherwise mistake it for; a separate `docs/` file would have been the
fourth place to look for the same subject). Seven entries, each with promise /
where promised / real status / where deferred:

D-1 response-adaptive onboarding · D-2 museum "If you only have one hour"
route · D-3 Taste absent from the global nav · D-4 full Passport collections ·
D-5 uncertainty interfaces · D-6 instrumentation · D-7 the fifth taste axis.

Nothing was built. The register carries an enforceable contributor rule:
write a promise into a doc, add a row in the same commit; ship it, delete the
row; a promise in neither the build nor the table is a defect.

Two source documents were also annotated so they stop reading as descriptions
of shipped behaviour: `docs/STYLE_GUIDE.md:103` (the one-hour route, the
strongest museum-page promise in the style guide, marked **Not yet built**)
and `PIGMENT.md` §15's preamble (points at §19).

### (d) Release-language check (AC14, OD-1)

Scanned `README.md`, `PIGMENT.md`, `docs/*.md`, `index.html` and `js/app.js`
for "comprehensive", "definitive", "complete history", "exhaustive",
"authoritative", "encyclopedi", and completeness-implying quantifiers.

Findings and dispositions:

1. **Rights overclaim — corrected.** `README.md:15` described artworks as being
   "for painters in the public domain (died ≤ 1955)", stating a legal
   conclusion as fact from a death year. Per OD-5 and AC28 this is exactly
   what may not be asserted. Reworded: Commons *asserts* PD, the build filters
   on died ≤ 1955, "a death year and a Commons licence template are an
   asserted basis, not a rights clearance; no clearance determination has been
   made."
2. **Completeness implication — corrected.** Neither README nor the site said
   "comprehensive", but neither said what Pigment *is not*, and a 247-painter
   atlas invites the inference. OD-1's positioning is now explicit in README's
   opening ("an editorial, path-discovering tool, not a comprehensive history
   of art… what it leaves out is as deliberate as what it includes") and in
   `index.html`'s meta description ("An editorial selection, not a complete
   history").
3. **`PIGMENT.md:124` "authoritative"** — scopes `STYLE_GUIDE.md` as
   authoritative *for tone and content budgets*, an internal precedence
   statement about documents. Not a claim about art history. **Left alone.**
4. **`PIGMENT.md:44` "a dry encyclopedia or museum wiki"** — appears under
   "What Pigment Is Not". Already correct. **Left alone.**
5. No adaptivity, accessibility-conformance, privacy-certification or
   legal-readiness claim survives in user-facing copy after (a) and (1).

A standing release-language rule is recorded at the end of §19 so the check is
repeatable rather than a one-off scan.

### Scope note

`PIGMENT.md`, `README.md` and `docs/` sit outside Gate 1's enumerated
production paths. `index.html` does **not** — its one-line meta-description
edit is a production-path change, made under the frozen specification's AC14
authority on an approved branch. Edits kept to correctness; no rewrites.

### Self-assessment

- **AC14** — PASS for the surfaces scanned. The one true overclaim (rights)
  is corrected, positioning is now explicit, and the check is written down so
  it can be re-run. Note the **honest residual**: AC25's own frozen inventory
  turned out to overclaim (unit 20 finding above), which is itself an AC14
  data point — the release-language problem was not confined to marketing copy.
- **AC26** — contributes the defect/deferred-promise register the criterion
  requires. The criterion-to-unit matrix and rollback procedure remain the
  Synthesis Lead's document; this supplies its register input.

---

## Deviation ledger (Gate 3)

| # | Deviation | Rationale | Status |
| --- | --- | --- | --- |
| D-W-1 | "Verify zero third-party requests remain" (U20 step 6) **not** asserted as written | `upload.wikimedia.org` is a genuine third-party runtime image host: 892 URLs in data, rendered as `<img src>` at 12+ sites in `app.js`. Claiming zero would be false and would itself violate AC14. Fonts-zero is verified; Wikimedia is disclosed. | **Escalated** — AC25 disposition for owner + privacy reviewer |
| D-W-2 | AC25's frozen "exactly two hosts" inventory is incomplete | Same evidence as D-W-1. Reported rather than silently conformed to. | **Escalated** to the Coordinator |
| D-W-3 | Captured rights written to a sidecar, not into `js/artworks.js` | `js/artworks.js` is a shipped bundle; ~530 records of licence paperwork would be downloaded by every visitor for data never rendered. Build-time provenance belongs out of the runtime payload. Reversible (a path, not a schema). | **Accepted**, flagged for review |
| D-W-4 | Only `latin` + `latin-ext` font subsets committed | Character audit found zero Cyrillic/Greek/Vietnamese codepoints in the entire corpus. `unicode-range` descriptors are verbatim, so selection behaviour is identical. | **Accepted** |
| D-W-5 | Frozen inventory `.md` understates homepage references (1 vs 2) | `og:image` and `twitter:image` are two references to one URL. Unique counts — which every total depends on — are unaffected. Regenerator reports the true 2. | **Accepted**, recorded |
| D-W-6 | 3 wrong Kahlo gallery images found; **not fixed** in this unit | Data records are the Data Steward's (CLAUDE.md §2), and 2 of 3 carry attribution-required CC licences — a rights question, not a tooling one. | **Handed to Seurat**, priority |
| D-W-7 | `docs/TASTE_MATH.md` and `docs/STYLE_GUIDE.md` edited beyond the brief's enumerated files | Both make the same unshipped claims unit 21 was told to correct in `ADMIRE_SPEC.md`/`PIGMENT.md`. Correcting one copy and leaving two would have left the defect in place. One annotation line each; no rewrites. | **Accepted** |

## Preview

```sh
git checkout pig-001-stabilization
python3 -m http.server 8421 -d .
open http://localhost:8421/
```

Fonts should load with no network access at all after first byte. To confirm
the privacy claim in a browser: DevTools → Network → filter by domain; no
request should leave `localhost` except `upload.wikimedia.org` image loads on
artist/artwork pages (see D-W-1).

## Known limitations of this wave

- No browser-rendered visual confirmation that typography is unchanged
  (Vermeer's pass). Descriptor-level equivalence is attested; pixels are not.
- The rights register is **tooling only**. No corpus-wide harvest was run, and
  no rights conclusion of any kind has been reached.
- The AC25 disposition is now larger than the owner was told when OD-3 was
  decided. That needs to go back to them before Gate 2.
- Gate 2 is **not** certified here.
