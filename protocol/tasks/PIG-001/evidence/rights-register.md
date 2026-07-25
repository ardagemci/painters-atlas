# PIG-001 — Artwork Rights Register (AC11, AC12, AC28)

**Author:** Seurat (`claude-data-steward`), Data and Copyright Steward
**Date:** 2026-07-25
**Branch:** `pig-001-stabilization` (verified; never `main`; not pushed)
**Gate 1:** VERIFIED — `protocol/tasks/PIG-001/specification.md` line 8 reads `workflow_state: "approved_for_build"`
**Binding input:** `owner-decisions-r2.md` **OD-5** — ship on documented residual risk; a clearance claim requires qualified review; unresolved is labelled unresolved, never "cleared"
**Machine-readable sibling:** `rights-register.json`

---

## Headline: actual rights exposure **and** documentation insufficiency — both

My round-1 conclusion ("zero actual rights exposure") was **wrong**, and it was
wrong for a specific, correctable reason: it tested whether the *artist* died by
1955 and never tested whether the *image depicted the artwork claimed*. Those
are different questions, and the second one is where the exposure lives.

Stated plainly, in the two categories the role's standard requires:

**1. Actual rights exposure — real, small, and now mostly closed.**
Four records in the reviewed set carry Creative Commons licences with live
attribution obligations that Pigment honours nowhere in its interface. Two of
them were also the wrong artwork and have been removed. **Two remain shipped**
and are the real residual:

| Record | Licence | Obligation | State |
| --- | --- | --- | --- |
| `sistine-chapel-ceiling` (**Tier 1 catalog**, in the daily deck pool) | **CC BY-SA 3.0** | attribution **and** share-alike | **open** |
| `correggio::Assumption of the Virgin (Parma Cathedral)` | **CC BY-SA 4.0** | attribution | **open** |

Both are photographs of frescoes *in situ*. A photograph of a three-dimensional
interior is the photographer's own copyrighted work — the PD-Art reasoning that
covers a flat scan of a painting does not reach it. The underlying frescoes are
long out of copyright; the photographs are not. `sistine-chapel-ceiling`
additionally ships with `image.status:"pd"` in `js/catalog-1.js`, which is a
false statement about a CC BY-SA 3.0 file sitting in shipped data.

**2. Documentation insufficiency — large, systemic, and not the same thing as exposure.**
Ninety-two of 122 records (75%) declare an `image.page` that is **not** the
Commons file page — mostly English Wikipedia *articles*, which carry no licence
statement of any kind. Every one of those records was resolvable to a real
Commons file page with an asserted licence, so this is a provenance-recording
defect rather than a rights defect. It is nonetheless the reason the round-1
review could not have caught the mismatches: the field Pigment stores does not
point at the evidence.

**3. A third finding the brief did not anticipate: accuracy.**
Eight records were the wrong artwork. Five had no rights consequence at all —
they were simply, factually wrong pictures, which PIGMENT.md §14 treats as a
product defect in its own right ("Artwork accuracy is a product requirement, not
a cosmetic detail").

**No clearance is claimed here, for any record, including the 116 that Commons
labels "Public domain."** Per OD-5 and AC28, a death year plus a Commons licence
template is an *asserted basis*, not a rights determination. Nothing in this
document may be cited as clearance.

---

## Coverage

| Measure | Count |
| --- | --- |
| **Distinct artwork records examined** | **122** (AC11 minimum: 100) |
| Tier 1 ∪ daily pool (catalog, mandatory) | 75 |
| Every Matisse gallery record (mandatory) | 4 |
| Every Kahlo gallery record (mandatory) | 3 — all three were mismatches, all three removed |
| Stratified gallery records | 37 |
| Records examined beyond the sample, found during the sweep | 3 |

### By status

| Status | Count |
| --- | --- |
| `documented` | 112 |
| `mismatch` | 8 |
| `attribution-required` | 2 |
| `unresolved` | **0** |

### By exact-match verdict

| Verdict | Count |
| --- | --- |
| `confirmed` | 114 |
| `mismatch` | 8 |
| `unverified` | 0 |

### By asserted licence

| Licence (Commons `LicenseShortName`) | Count |
| --- | --- |
| Public domain | 116 |
| CC0 | 2 |
| CC BY-SA 4.0 | 2 |
| CC BY-SA 3.0 | 1 |
| CC BY 2.0 | 1 |

### Verification integrity

| Measure | Count |
| --- | --- |
| Transient lookup failures recorded as negative findings | **0** |
| Entries whose declared `page` is not the Commons file page | 92 |
| Legal conclusions reached | **0** |

Every record resolved. There is no entry in this register whose status rests on
a request that failed.

---

## Method

Built with `tools/rights_register.py` and `tools/commons_rights.py` (Wave D,
unit 16), extended for this pass with a depiction check the tooling did not have.

**Rate-limit discipline** (enforced in code, `tools/commons_rights.py`):
minimum 0.25 s between any two outbound requests, process-wide; four attempts
with 1/3/9 s backoff; `Retry-After` honoured; batching capped at the API's
50-title limit and deduplicated by underlying file. **A timeout, 429, 5xx,
connection reset or malformed JSON produces `unverified` and never a negative
finding.** Only an explicit `missing` from the API is a definitive negative, and
even that is reported as `missing`, not as a rights conclusion. A previous run
of a similar tool falsely killed 216 entries by ignoring this; nothing in this
register was classified from a failed request.

**Exact-artwork verification** (new this pass — the round-1 gap). For every
record, Commons `extmetadata` `ObjectName`, `ImageDescription` and file
categories were compared against the claimed title *and* the claimed artist:

- **`confirmed`** requires corroboration on both axes, or on one axis with a
  stated reason for the other (a non-English `ObjectName` — *Det syke barn*,
  *Les Joueurs de cartes*, *Die Tanzklasse*, *Svanen No. 17*, *L'Atelier rouge*
  — or an `Artist` field naming the photographer rather than the painter). Eight
  such single-axis cases occurred; each was inspected individually rather than
  waved through.
- **`mismatch`** means the file was positively identified as a different work.
- **`unverified`** means neither axis corroborated. Zero records ended here.

Two ambiguous files were resolved by downloading and **viewing the image**
(`henri-matisse::The Snail`, `giambattista-tiepolo::Apollo and the Continents`).

### A note on why the existing audit tool missed all of this

`tools/audit_artworks.py:75`:

```python
return any(t in f for t in name_toks) or any(t in f for t in title_toks)
```

A file is accepted if its name contains **any** artist token **or** **any**
title token. `Closeup_of_Frida_Kahlo_and_Diego_Rivera_Sculpture.jpg` contains
"kahlo"; `Broken_column_in_Syrakousai.jpg` contains "broken" and "column";
`Joseph_Ducreux_-_Self-Portrait,_Yawning.jpg` contains "self" and "portrait".
All three passed a validator that was working exactly as written. The rule is
too weak by construction, and it is the single root cause of the entire mismatch
class. I have not rewritten it — that is a tooling change and belongs to the
Implementation Lead — but it should not survive to the next audit run.

---

## The eight mismatches

Every one was found in `js/artworks.js`, the gallery store, which has no
`status` field and had never been audited for depiction accuracy.

| # | Record | Pigment claimed | The file actually is | Licence | Attribution | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `frida-kahlo::The Broken Column` | Kahlo's 1944 self-portrait | **A photograph of an actual broken column in Syracuse, Sicily** (`File:Broken_column_in_Syrakousai.jpg`) | **CC BY 2.0** | **YES** (Andrew Malone) | **removed** |
| 2 | `frida-kahlo::The Two Fridas` | Kahlo's 1939 double portrait | **A photograph of a public sculpture** in the Frida Kahlo Park, Coyoacán | **CC BY-SA 4.0** | **YES** (Ines Suarez R.) | **removed** |
| 3 | `frida-kahlo::Self-Portrait with Thorn Necklace and Hummingbird` | Kahlo's 1940 self-portrait | **Joseph Ducreux, *Self-Portrait, Yawning*** — different artist, different century, different painting | Public domain | no | **removed** |
| 4 | `stanislaw-wyspianski::Self-Portrait` | Wyspiański's self-portrait | **The same Ducreux painting** | Public domain | no | **corrected** |
| 5 | `karl-bryullov::Self-Portrait` | Bryullov's self-portrait | **The same Ducreux painting** | Public domain | no | **corrected** |
| 6 | `matrakci-nasuh::View of Istanbul (Mecmu-ı Menazil)` | The Istanbul folio | **The Aleppo folio** of the same manuscript — and a duplicate of this artist's own sibling `View of Aleppo` record | Public domain | no | **corrected** |
| 7 | `bada-shanren::Two Birds` | A distinct work | **The same file as this artist's `Lotus and Birds` record.** One image cannot be both works | Public domain | no | **image removed** |
| 8 | `giambattista-tiepolo::Apollo and the Continents (Würzburg)` | The Würzburg Residenz ceiling fresco | **The Metropolitan Museum's oil *modello*, *Allegory of the Planets and Continents*** — same artist, same composition, different object | Public domain | no | **documented, not changed** |

**One file, three records.** The Ducreux *Self-Portrait, Yawning* was serving as
the self-portrait of Kahlo, Wyspiański **and** Bryullov simultaneously. It was
found by checking which image URLs appear under more than one record — a check
worth keeping permanently, since it costs nothing and caught two mismatches
outside the mandated sample.

### Dispositions and why

**Removed (no image), 4 records.** Kahlo died in 1954 and clears the build's
`died <= 1955` filter, but her *works* remain in copyright — Mexico is life+100,
so 2054. No public-domain image of a Kahlo painting exists on Commons to
substitute, which is precisely why the resolver returned garbage: it searched,
found nothing matching, and accepted the best near-miss. There is no honest
replacement, so the images are gone. `js/app.js:1765` renders a work with no
gallery entry as a plain title row — the work still appears in "Major works",
with no picture and no generative cover posing as one. That is the honest
degradation and it required no code change.

**Corrected with a verified replacement, 3 records.** Each replacement was
checked for exact-match *and* PD *before* being written, and each thumbnail was
confirmed to return HTTP 200:

| Record | Replacement file | Verified |
| --- | --- | --- |
| `matrakci-nasuh::View of Istanbul` | `File:Matrakçı Nasuh - İstanbul.jpg` | Artist "Matrakçı Nasuh"; description "Matrakçı Nasuh'un İstanbul ve Galata betimlemesi"; same manuscript (Istanbul Univ. Library T. 5964); PD (author died >100 years ago); attribution not required |
| `stanislaw-wyspianski::Self-Portrait` | `File:Stanisław Wyspiański, Autoportret.jpg` | Artist "Stanisław Wyspiański"; `ObjectName` "Self-portrait"; PD; attribution not required |
| `karl-bryullov::Self-Portrait` | `File:Karl Bryullov (Bryullo) - Автопортрет - Google Art Project.jpg` | Artist "Karl Bryullov"; `ObjectName` "Автопортрет / Self portrait"; PD; attribution not required |

**Documented but not changed, 1 record.** The Tiepolo is the weakest of the
eight and the only one I chose not to touch. The image is the artist's own oil
*modello* for the very ceiling the record names — the composition a visitor sees
is right. Under PIGMENT.md §14 it is still "a different version" shown without a
label, so it is recorded as a mismatch rather than excused. I did not swap it
because every available photograph of the actual Würzburg ceiling is a
photograph of a 3D interior, which would trade a mild accuracy defect for a live
CC BY-SA attribution obligation — the exact problem `sistine-chapel-ceiling`
already represents. **Recommendation:** label the caption as the modello. That
is editorial copy and belongs to Van Gogh (`claude-content-editor`), not to me.

---

## A separate defect found on the way: a dead Tier 1 image

`red-fuji` — Hokusai's *Fine Wind, Clear Morning*, **Tier 1 and in the daily
pool**, meaning it can surface as the homepage "Today in Pigment" — pointed at a
file that does not exist. The shipped URL spelled the transliteration `Gaifuu`;
the live Commons file uses the macron, `Gaifū`.

This was verified as a genuine negative **two independent ways**, not from a
single failed request: the CDN thumbnail returned **HTTP 404**, and the Commons
API separately reported the title as `missing`. It is not a timeout and not a
429. Corrected to the verified file (`ObjectName` "Fine Wind, Clear Morning
(Gaifū kaisei)", description "Red Fuji", PD, 5803×3918, attribution not
required).

---

## Two rights findings with correct depiction

These are the residual exposure. Neither is a mismatch; both are real
obligations.

### `sistine-chapel-ceiling` — CC BY-SA 3.0, Tier 1, shipped as `status:"pd"`

The photograph is by Antoine Taveneaux and is licensed **CC BY-SA 3.0**, which
requires attribution *and* share-alike. The record in `js/catalog-1.js:1689`
declares `status:"pd"`. The ceiling is Michelangelo's and is unquestionably out
of copyright; the *photograph of it* is not, and it is the photograph Pigment
serves.

**I did not change this**, and the reason is worth stating rather than burying:
`image.status === "pd"` is a **behavioural** filter, not a label. `js/app.js`
uses it to decide museum collage membership and deck-pool eligibility
(`tools/validate.jxa.js:201`). Flipping it would silently remove a Tier 1 work
from the onboarding deck and change what visitors see. That is a functional
change requiring Implementation Lead coordination, not a data correction I
should make unilaterally under an evidence brief. **Escalated** — it needs a
decision, and OD-5's "documented residual risk" is a legitimate landing place
for it, but only if the owner is told, which is what this section is for.

### `correggio::Assumption of the Virgin (Parma Cathedral)` — CC BY-SA 4.0

In-situ photograph of the dome fresco, credited to Commons user
Livioandronico2013, **CC BY-SA 4.0**, attribution required. Depiction correct.
Same structural issue, no `status` field on the gallery store to be wrong.

### What honouring these would take

Pigment displays "images via Wikimedia Commons" (`js/app.js:1769`) and links the
file page from the lightbox. For a PD file that is courteous; for CC BY / CC
BY-SA it is **not sufficient** — those licences require the author's name and
the licence identifier. Three options, none of which I am authorised to pick:

1. Render author + licence for the four affected records (smallest change, keeps
   the images).
2. Replace them with PD alternatives (none exists for the two in-situ frescoes).
3. Accept as documented residual risk under OD-5 (the owner's call, and it must
   be an informed one).

---

## Systemic findings

1. **The `died <= 1955` filter is not a rights test, and the corpus proves it.**
   `tools/fetch_artworks.py` uses artist death year to decide whom to resolve
   images for. Kahlo (d. 1954) and Matisse (d. 1954) both pass, yet their works
   are broadly still in copyright — Matisse's *The Snail* (1953) is PD in France
   only from 2025 and remains under US copyright until 2049. The filter is a
   reasonable heuristic for *whom to try*; it is not, and was never, a
   determination. README's overclaim on exactly this point was corrected in
   Wave D (unit 21); the code-level version of the same conflation is recorded
   here. **This is the single most important structural finding in the
   register.** Guarded now by an explicit `SUPPRESS` list with stated reasons in
   `tools/fetch_artworks.py`, shared with `tools/audit_artworks.py`.

2. **Wrong images were still being served publicly after the data was fixed.**
   Removing the Kahlo records from `js/artworks.js` did not remove them from
   `p/artist/frida-kahlo.html`, whose `og:image` and `twitter:image` still
   pointed at the CC BY-SA 4.0 sculpture photograph. The prerendered stub
   surface lags the data by design and nothing enforced the link. Stubs
   regenerated; a regression test now asserts that no corrected image survives
   in `prerender_metadata_refs`.

3. **The gallery store has no rights or status field at all.** `js/artworks.js`
   carries only `img` and `page`. Per Wave D's D-W-3 that is deliberate — rights
   metadata is a sidecar, not runtime payload — and I have not changed it. The
   consequence to record is that the gallery surface has **no in-band signal**
   distinguishing a verified PD scan from a CC BY-SA photograph, which is why
   this class of defect was invisible until a register existed.

4. **Duplicate-image detection is free and finds real defects.** Two of the
   eight mismatches were found only by checking for image URLs used by more than
   one record. Zero duplicates remain in `js/artworks.js`.

---

## Explicitly unresolved (AC12)

Under AC12, everything below is **unresolved** and must not be represented as
cleared, public-domain, licensed, or legally approved:

- **Every public asset outside this register.** The frozen inventory reports
  **797 unique public assets** post-correction. This register examined **122**.
  The remaining **~675 are unreviewed** — not "presumed fine", unreviewed. In
  particular the 103 museum photographs are photographs of buildings and
  interiors, structurally the same category as the two CC BY-SA findings above,
  and **none of them was in the mandated sample**. If one systematic risk
  deserves the next pass, it is that one.
- **The two attribution-required records still shipped**, above.
- **The Tiepolo version mismatch**, retained pending an editorial label.
- **`sistine-chapel-ceiling`'s `status:"pd"` field**, factually wrong and
  deliberately not changed.
- **Every "Public domain" assertion in this register.** Commons asserts; Commons
  is not a court. The Matisse records are the sharpest case: four works by an
  artist who died in 1954, tagged PD-Art, whose US copyright status is very
  likely still live.
- **All 92 records whose declared `page` is not the Commons file page.** The
  provenance Pigment ships does not point at the evidence, even where the
  evidence exists and I resolved it.

---

## Data changes made under this register

All on `pig-001-stabilization`. Validator green before and after; **both
pre-existing deck warnings additionally cleared** by the separate editorial-merit
review recorded in `deck-merit-review.md`.

| File | Change |
| --- | --- |
| `js/artworks.js` | 3 Kahlo records removed; `matrakci-nasuh::View of Istanbul`, `stanislaw-wyspianski::Self-Portrait`, `karl-bryullov::Self-Portrait` re-pointed at verified files; `bada-shanren::Two Birds` duplicate image removed |
| `js/catalog-1.js` | `red-fuji` image URL corrected (dead → verified) |
| `tools/fetch_artworks.py` | `SUPPRESS` list added, with a stated reason per entry, so a regeneration cannot restore the Kahlo images |
| `tools/audit_artworks.py` | Honours the same `SUPPRESS` list; corrected Matrakçı file pinned in `PINNED` per PIGMENT.md §14 |
| `p/artist/frida-kahlo.html`, `p/artist/matrakci-nasuh.html`, `p/artwork/red-fuji.html` | Regenerated so public metadata stops serving the wrong images |
| `tests/test_rights_tooling.py` | Frozen-inventory tests now assert freeze **+ recorded corrections**; new tests for stub/data consistency and suppression |
| `index.html` | `?v=` cache strings bumped for the three edited data files (see below) |

**A correction that does not reach the browser is not a correction.** Verified in
a real browser at `localhost:8421`: after editing `js/catalog-1.js` the page
still served the *old* `Gaifuu` URL, because `index.html` still requested
`catalog-1.js?v=20260713-imagefix2` and the browser served its cached copy. The
three edited data files therefore had their cache strings bumped to
`?v=20260725-pig001-rights`. Re-verified after the bump: `red-fuji` resolves to
the corrected `Gaifū` file, `window.ARTWORKS["frida-kahlo"]` is absent, and the
Matrakçı record points at the İstanbul folio.

This matters beyond my edit: **any data-only correction on this project is
invisible to returning visitors unless its `?v=` string moves in the same
commit.** The rollback procedure in the frozen specification already assumes
this, but nothing enforces it.

Rendering checked at the same time: Kahlo's artist page renders **zero images and
zero broken images** — her works remain named in the Tier 1 arc narrative, with
no placeholder and no generative cover presented as a painting. Wyspiański's
*Self-Portrait* now shows his own *Autoportret*. (External image loads are
blocked in that preview pane, so pixel confirmation of the Commons images
themselves belongs to Vermeer's evidence pass, not this one.)

The frozen inventory `asset-inventory-effa805.json` was **not** rewritten. It is
dated evidence of effa805 and stays byte-stable; the corrections are carried as
an explicit delta in the test suite, so undocumented drift still fails.

**Not committed to `main`; not deployed.** Merge and deployment require the
owner's explicit approval.

---

## Register entries (122)

Sorted mismatches first, then attribution-required, then the remainder
alphabetically. Full machine-readable detail — including usage terms, licence
URLs, credit lines and per-entry verification basis — in `rights-register.json`.

| # | Record id | Surface | Claimed title / artist | Commons file page | Licence | Attribution | PD basis | Exact-match | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bada-shanren::Two Birds` | gallery | Two Birds — Bada Shanren | `File:Bada_Shanren_(Zhu_Da)_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg` | Public domain | no | d.1705 | mismatch | `mismatch` |
| 2 | `frida-kahlo::Self-Portrait with Thorn Necklace and Hummingbird` | gallery | Self-Portrait with Thorn Necklace and Hummin — Frida Kahlo | [file page](https://commons.wikimedia.org/wiki/File:Joseph_Ducreux_(French)_-_Self-Portrait,_Yawning_-_Google_Art_Project.jpg) | Public domain | no | d.1954 | mismatch | `mismatch` |
| 3 | `frida-kahlo::The Broken Column` | gallery | The Broken Column — Frida Kahlo | [file page](https://commons.wikimedia.org/wiki/File:Broken_column_in_Syrakousai.jpg) | CC BY 2.0 | **YES** — Andrew Malone | d.1954 | mismatch | `mismatch` |
| 4 | `frida-kahlo::The Two Fridas` | gallery | The Two Fridas — Frida Kahlo | [file page](https://commons.wikimedia.org/wiki/File:Closeup_of_Frida_Kahlo_and_Diego_Rivera_Sculpture.jpg) | CC BY-SA 4.0 | **YES** — Ines Suarez R. | d.1954 | mismatch | `mismatch` |
| 5 | `giambattista-tiepolo::Apollo and the Continents (Würzburg)` | gallery | Apollo and the Continents (Würzburg) — Giovanni Battista Tiepolo | [file page](https://commons.wikimedia.org/wiki/File:Giovanni_Battista_Tiepolo_-_Allegory_of_the_Planets_and_Continents.jpg) | Public domain | no | d.1770 | mismatch | `mismatch` |
| 6 | `karl-bryullov::Self-Portrait` | gallery | Self-Portrait — Karl Bryullov | `File:Joseph_Ducreux_(French)_-_Self-Portrait,_Yawning_-_Google_Art_Project.jpg` | Public domain | no | d.1852 | mismatch | `mismatch` |
| 7 | `matrakci-nasuh::View of Istanbul (Mecmu-ı Menazil)` | gallery | View of Istanbul (Mecmu-ı Menazil) — Matrakçı Nasuh | [file page](https://commons.wikimedia.org/wiki/File:Aleppo_ca1537_by_Matrakci_Nasuh_Istanbul_University_Library_ms5964.png) | Public domain | no | d.1564 | mismatch | `mismatch` |
| 8 | `stanislaw-wyspianski::Self-Portrait` | gallery | Self-Portrait — Stanisław Wyspiański | `File:Joseph_Ducreux_(French)_-_Self-Portrait,_Yawning_-_Google_Art_Project.jpg` | Public domain | no | d.1907 | mismatch | `mismatch` |
| 9 | `correggio::Assumption of the Virgin (Parma Cathedral)` | gallery | Assumption of the Virgin (Parma Cathedral) — Correggio | [file page](https://commons.wikimedia.org/wiki/File:Cathedral_(Parma)_-_Assumption_by_Correggio.jpg) | CC BY-SA 4.0 | **YES** — Antonio da Correggio | d.1534 | confirmed | `attribution-required` |
| 10 | `sistine-chapel-ceiling` | catalog | Sistine Chapel Ceiling — Michelangelo Buonarroti | [file page](https://commons.wikimedia.org/wiki/File:Sistine_Chapel_ceiling_02_(brightened).jpg) | CC BY-SA 3.0 | **YES** — Antoine Taveneaux | d.1564 | confirmed | `attribution-required` |
| 11 | `a-bar-at-the-folies-bergere` | catalog | A Bar at the Folies-Bergère — Édouard Manet | [file page](https://commons.wikimedia.org/wiki/File:%22Un_Bar_aux_Folies-Berg%C3%A8re%22_by_%C3%89douard_Manet_(1882).jpg) | Public domain | no | d.1883 | confirmed | `documented` |
| 12 | `adele-bloch-bauer-i` | catalog | Portrait of Adele Bloch-Bauer I — Gustav Klimt | [file page](https://commons.wikimedia.org/wiki/File:Gustav_Klimt_046.jpg) | Public domain | no | d.1918 | confirmed | `documented` |
| 13 | `akseli-gallen-kallela::Lemminkäinen's Mother` | gallery | Lemminkäinen's Mother — Akseli Gallen-Kallela | [file page](https://commons.wikimedia.org/wiki/File:Gallen_Kallela_Lemminkainens_Mother.jpg) | Public domain | no | d.1931 | confirmed | `documented` |
| 14 | `angelica-kauffman::Ariadne Abandoned by Theseus` | gallery | Ariadne Abandoned by Theseus — Angelica Kauffman | [file page](https://commons.wikimedia.org/wiki/File:Angelica_Kauffmann,_Ariadne_Abandoned_by_Theseus,_1774.jpg) | Public domain | no | d.1807 | confirmed | `documented` |
| 15 | `annibale-carracci::Domine, Quo Vadis?` | gallery | Domine, Quo Vadis? — Annibale Carracci | [file page](https://commons.wikimedia.org/wiki/File:Domine,_quo_vadis.jpg) | Public domain | no | d.1609 | confirmed | `documented` |
| 16 | `barge-haulers-on-the-volga` | catalog | Barge Haulers on the Volga — Ilya Repin | [file page](https://commons.wikimedia.org/wiki/File:Ilia_Efimovich_Repin_(1844-1930)_-_Volga_Boatmen_(1870-1873).jpg) | Public domain | no | d.1930 | confirmed | `documented` |
| 17 | `bartolome-murillo::Boys Eating Grapes and Melon` | gallery | Boys Eating Grapes and Melon — Bartolomé Esteban Murillo | [file page](https://commons.wikimedia.org/wiki/File:Carl_Reiser_(1877%E2%80%931950),_copy_after_Bartolom%C3%A9_Esteban_Murillo_(1617%E2%80%931682)_-_Beggar_Boys_Eating_Grapes_and_Melon_-_BORGM_00036_-_Russell-Cotes_Art_Gallery_%5E_Museum.jpg) | Public domain | no | d.1682 | confirmed | `documented` |
| 18 | `black-square` | catalog | Black Square — Kazimir Malevich | [file page](https://commons.wikimedia.org/wiki/File:Kazimir_Malevich,_1915,_Black_Suprematic_Square,_oil_on_linen_canvas,_79.5_x_79.5_cm,_Tretyakov_Gallery,_Moscow.jpg) | Public domain | no | d.1935 | confirmed | `documented` |
| 19 | `burial-of-the-count-of-orgaz` | catalog | The Burial of the Count of Orgaz — El Greco | [file page](https://commons.wikimedia.org/wiki/File:El_Greco_-_The_Burial_of_the_Count_of_Orgaz.JPG) | Public domain | no | d.1614 | confirmed | `documented` |
| 20 | `camille-corot::Souvenir de Mortefontaine` | gallery | Souvenir de Mortefontaine — Camille Corot | [file page](https://commons.wikimedia.org/wiki/File:Souvenir_de_Mortefontaine_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_MI_692_bis_-_photo_2.jpg) | Public domain | no | d.1875 | confirmed | `documented` |
| 21 | `chaim-soutine::Carcass of Beef` | gallery | Carcass of Beef — Chaïm Soutine | [file page](https://commons.wikimedia.org/wiki/File:Carcass_of_Beef_by_Chaim_Soutine,_c._1925,_Albright-Knox_Art_Gallery.jpg) | Public domain | no | d.1943 | confirmed | `documented` |
| 22 | `composition-vii` | catalog | Composition VII — Wassily Kandinsky | [file page](https://commons.wikimedia.org/wiki/File:Composition_VII_-_Wassily_Kandinsky,_GAC.jpg) | Public domain | no | d.1944 | confirmed | `documented` |
| 23 | `composition-viii` | catalog | Composition VIII — Wassily Kandinsky | [file page](https://commons.wikimedia.org/wiki/File:Vassily_Kandinsky,_1923_-_Composition_8,_huile_sur_toile,_140_cm_x_201_cm,_Mus%C3%A9e_Guggenheim,_New_York.jpg) | Public domain | no | d.1944 | confirmed | `documented` |
| 24 | `david-with-the-head-of-goliath` | catalog | David with the Head of Goliath — Caravaggio | [file page](https://commons.wikimedia.org/wiki/File:David_with_the_Head_of_Goliath-Caravaggio_(1610).jpg) | Public domain | no | d.1610 | confirmed | `documented` |
| 25 | `duccio::Maestà` | gallery | Maestà — Duccio di Buoninsegna | [file page](https://commons.wikimedia.org/wiki/File:Duccio_di_Buoninsegna_038.jpg) | Public domain | no | d.1319 | confirmed | `documented` |
| 26 | `el-greco::The Burial of the Count of Orgaz` | gallery | The Burial of the Count of Orgaz — El Greco | [file page](https://commons.wikimedia.org/wiki/File:El_Greco_-_The_Burial_of_the_Count_of_Orgaz.JPG) | Public domain | no | d.1614 | confirmed | `documented` |
| 27 | `elisabeth-vigee-le-brun::Self-Portrait with Her Daughter Julie` | gallery | Self-Portrait with Her Daughter Julie — Élisabeth Vigée Le Brun | [file page](https://commons.wikimedia.org/wiki/File:Self-portrait_with_Her_Daughter_by_Elisabeth-Louise_Vig%C3%A9e_Le_Brun.jpg) | Public domain | no | d.1842 | confirmed | `documented` |
| 28 | `francisco-de-zurbaran::Saint Serapion` | gallery | Saint Serapion — Francisco de Zurbarán | [file page](https://commons.wikimedia.org/wiki/File:San_Serapio,_por_Francisco_de_Zurbar%C3%A1n.jpg) | Public domain | no | d.1664 | confirmed | `documented` |
| 29 | `georges-de-la-tour::The Cheat with the Ace of Diamonds` | gallery | The Cheat with the Ace of Diamonds — Georges de La Tour | [file page](https://commons.wikimedia.org/wiki/File:Georges_de_La_Tour_-_Cheater_with_the_Ace_of_Diamonds_-_WGA12334.jpg) | Public domain | no | d.1652 | confirmed | `documented` |
| 30 | `ghent-altarpiece` | catalog | The Ghent Altarpiece — Jan van Eyck | [file page](https://commons.wikimedia.org/wiki/File:Jan_van_Eyck_The_Ghent_Altarpiece_-_Adoration_of_the_Lamb.jpg) | Public domain | no | d.1441 | confirmed | `documented` |
| 31 | `girl-with-a-pearl-earring` | catalog | Girl with a Pearl Earring — Johannes Vermeer | [file page](https://commons.wikimedia.org/wiki/File:1665_Girl_with_a_Pearl_Earring.jpg) | Public domain | no | d.1675 | confirmed | `documented` |
| 32 | `grainstacks` | catalog | Stacks of Wheat (End of Summer) — Claude Monet | [file page](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Stacks_of_Wheat_(End_of_Summer)_-_1985.1103_-_Art_Institute_of_Chicago.jpg) | Public domain | no | d.1926 | confirmed | `documented` |
| 33 | `gustav-klimt::The Kiss` | gallery | The Kiss — Gustav Klimt | [file page](https://commons.wikimedia.org/wiki/File:The_Kiss_-_Gustav_Klimt_-_Google_Cultural_Institute.jpg) | Public domain | no | d.1918 | confirmed | `documented` |
| 34 | `gustave-dore::London: A Pilgrimage` | gallery | London: A Pilgrimage — Gustave Doré | [file page](https://commons.wikimedia.org/wiki/File:Gustave_Dor%C3%A9_-_Wentworth_Street_Whitechapel_-_London,_a_Pilgrimage.jpg) | Public domain | no | d.1883 | confirmed | `documented` |
| 35 | `henri-matisse::The Dance` | gallery | The Dance — Henri Matisse | [file page](https://commons.wikimedia.org/wiki/File:Matissedance.jpg) | Public domain | no | d.1954 | confirmed | `documented` |
| 36 | `henri-matisse::The Red Studio` | gallery | The Red Studio — Henri Matisse | [file page](https://commons.wikimedia.org/wiki/File:L%27Atelier_rouge,_par_Henri_Matisse.jpg) | Public domain | no | d.1954 | confirmed | `documented` |
| 37 | `henri-matisse::The Snail` | gallery | The Snail — Henri Matisse | [file page](https://commons.wikimedia.org/wiki/File:Matisse_-_Carra,_P18.jpg) | Public domain | no | d.1954 | confirmed | `documented` |
| 38 | `henri-matisse::Woman with a Hat` | gallery | Woman with a Hat — Henri Matisse | [file page](https://commons.wikimedia.org/wiki/File:Matisse-Woman-with-a-Hat.jpg) | Public domain | no | d.1954 | confirmed | `documented` |
| 39 | `hieronymus-bosch::The Garden of Earthly Delights` | gallery | The Garden of Earthly Delights — Hieronymus Bosch | [file page](https://commons.wikimedia.org/wiki/File:The_Garden_of_Earthly_Delights_by_Bosch_High_Resolution.jpg) | Public domain | no | d.1516 | confirmed | `documented` |
| 40 | `hunters-in-the-snow` | catalog | The Hunters in the Snow — Pieter Bruegel the Elder | [file page](https://commons.wikimedia.org/wiki/File:Pieter_Bruegel_the_Elder_-_Hunters_in_the_Snow_(Winter)_-_Google_Art_Project.jpg) | Public domain | no | d.1569 | confirmed | `documented` |
| 41 | `impression-sunrise` | catalog | Impression, Sunrise — Claude Monet | [file page](https://commons.wikimedia.org/wiki/File:Monet_-_Impression,_Sunrise.jpg) | Public domain | no | d.1926 | confirmed | `documented` |
| 42 | `ito-jakuchu::Birds and Animals in the Flower Garden` | gallery | Birds and Animals in the Flower Garden — Itō Jakuchū | [file page](https://commons.wikimedia.org/wiki/File:It%C5%8D_Jakuch%C5%AB_-_Animals_in_the_Flower_garden_(Left-hand_screen).jpg) | Public domain | no | d.1800 | confirmed | `documented` |
| 43 | `ivan-the-terrible-and-his-son` | catalog | Ivan the Terrible and His Son Ivan — Ilya Repin | [file page](https://commons.wikimedia.org/wiki/File:Iv%C3%A1n_el_Terrible_y_su_hijo,_por_Ili%C3%A1_Repin.jpg) | Public domain | no | d.1930 | confirmed | `documented` |
| 44 | `jacek-malczewski::Melancholia` | gallery | Melancholia — Jacek Malczewski | [file page](https://commons.wikimedia.org/wiki/File:Malczewski_melancholia.jpg) | Public domain | no | d.1929 | confirmed | `documented` |
| 45 | `jan-steen::The Feast of Saint Nicholas` | gallery | The Feast of Saint Nicholas — Jan Steen | [file page](https://commons.wikimedia.org/wiki/File:Jan_Havicksz._Steen_%E2%80%93_Het_Sint-Nicolaasfeest_%E2%80%93_Google_Art_Project.jpg) | Public domain | no | d.1679 | confirmed | `documented` |
| 46 | `jan-van-eyck::The Ghent Altarpiece (with Hubert van Eyck)` | gallery | The Ghent Altarpiece (with Hubert van Eyck) — Jan van Eyck | [file page](https://commons.wikimedia.org/wiki/File:Jan_van_Eyck_The_Ghent_Altarpiece_-_Adoration_of_the_Lamb.jpg) | Public domain | no | d.1441 | confirmed | `documented` |
| 47 | `john-constable::Cloud Studies` | gallery | Cloud Studies — John Constable | [file page](https://commons.wikimedia.org/wiki/File:John_Constable_-_Cloud_Study_-_Google_Art_Project_(2442698).jpg) | Public domain | no | d.1837 | confirmed | `documented` |
| 48 | `john-constable::Salisbury Cathedral from the Meadows` | gallery | Salisbury Cathedral from the Meadows — John Constable | [file page](https://commons.wikimedia.org/wiki/File:Constable_Salisbury_meadows.jpg) | Public domain | no | d.1837 | confirmed | `documented` |
| 49 | `juan-de-pareja` | catalog | Portrait of Juan de Pareja — Diego Velázquez | [file page](https://commons.wikimedia.org/wiki/File:Retrato_de_Juan_Pareja,_by_Diego_Vel%C3%A1zquez.jpg) | Public domain | no | d.1660 | confirmed | `documented` |
| 50 | `judith-and-her-maidservant-detroit` | catalog | Judith and Her Maidservant with the Head of  — Artemisia Gentileschi | [file page](https://commons.wikimedia.org/wiki/File:Artemisia_Gentileschi_Judith_Maidservant_DIA.jpg) | Public domain | no | d.1656 | confirmed | `documented` |
| 51 | `judith-slaying-holofernes` | catalog | Judith Slaying Holofernes — Artemisia Gentileschi | [file page](https://commons.wikimedia.org/wiki/File:Judit_decapitando_a_Holofernes,_por_Artemisia_Gentileschi.jpg) | Public domain | no | d.1656 | confirmed | `documented` |
| 52 | `katsushika-hokusai::Fine Wind, Clear Morning (Red Fuji)` | gallery | Fine Wind, Clear Morning (Red Fuji) — Katsushika Hokusai | [file page](https://commons.wikimedia.org/wiki/File:Katsushika_Hokusai_-_Fine_Wind,_Clear_Morning_(Gaif%C5%AB_kaisei)_-_Google_Art_Project.jpg) | Public domain | no | d.1849 | confirmed | `documented` |
| 53 | `kim-hong-do::Ssireum (Wrestling)` | gallery | Ssireum (Wrestling) — Kim Hong-do (Danwon) | [file page](https://commons.wikimedia.org/wiki/File:Danwon_Ssireum.jpg) | Public domain | no | d.1806 | confirmed | `documented` |
| 54 | `labsinthe` | catalog | L'Absinthe — Edgar Degas | [file page](https://commons.wikimedia.org/wiki/File:Edgar_Degas_-_In_a_Caf%C3%A9_-_Google_Art_Project_2.jpg) | Public domain | no | d.1917 | confirmed | `documented` |
| 55 | `lady-with-an-ermine` | catalog | Lady with an Ermine — Leonardo da Vinci | [file page](https://commons.wikimedia.org/wiki/File:Lady_with_an_Ermine_-_Leonardo_da_Vinci_(adjusted_levels).jpg) | Public domain | no | d.1519 | confirmed | `documented` |
| 56 | `las-meninas` | catalog | Las Meninas — Diego Velázquez | [file page](https://commons.wikimedia.org/wiki/File:Las_Meninas,_by_Diego_Vel%C3%A1zquez,_from_Prado_in_Google_Earth.jpg) | Public domain | no | d.1660 | confirmed | `documented` |
| 57 | `lucas-cranach::The Judgment of Paris` | gallery | The Judgment of Paris — Lucas Cranach the Elder | [file page](https://commons.wikimedia.org/wiki/File:Lucas_Cranach_the_Elder_-_The_Judgment_of_Paris_-_Google_Art_Project.jpg) | Public domain | no | d.1553 | confirmed | `documented` |
| 58 | `lumber-schooners-penobscot-bay` | catalog | Lumber Schooners at Evening on Penobscot Bay — Fitz Henry Lane | [file page](https://commons.wikimedia.org/wiki/File:Fitz_Henry_Lane,_Lumber_Schooners_at_Evening_on_Penobscot_Bay,_1863,_NGA_57611.jpg) | CC0 | no | d.1865 | confirmed | `documented` |
| 59 | `madonna-munch` | catalog | Madonna — Edvard Munch | [file page](https://commons.wikimedia.org/wiki/File:Edvard_Munch_-_Madonna_-_Google_Art_Project.jpg) | Public domain | no | d.1944 | confirmed | `documented` |
| 60 | `melencolia-i` | catalog | Melencolia I — Albrecht Dürer | [file page](https://commons.wikimedia.org/wiki/File:Albrecht_D%C3%BCrer_-_Melencolia_I_-_Google_Art_Project_(_AGDdr3EHmNGyA).jpg) | Public domain | no | d.1528 | confirmed | `documented` |
| 61 | `mikhail-vrubel::The Demon Seated` | gallery | The Demon Seated — Mikhail Vrubel | [file page](https://commons.wikimedia.org/wiki/File:Vrubel_Demon.jpg) | Public domain | no | d.1910 | confirmed | `documented` |
| 62 | `mona-lisa` | catalog | Mona Lisa — Leonardo da Vinci | [file page](https://commons.wikimedia.org/wiki/File:Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg) | Public domain | no | d.1519 | confirmed | `documented` |
| 63 | `mont-sainte-victoire` | catalog | Mont Sainte-Victoire Seen from Bibémus — Paul Cézanne | [file page](https://commons.wikimedia.org/wiki/File:La_Montagne_Sainte-Victoire_vue_de_la_carri%C3%A8re_Bib%C3%A9mus,_par_Paul_C%C3%A9zanne.jpg) | Public domain | no | d.1906 | confirmed | `documented` |
| 64 | `nocturne-in-black-and-gold` | catalog | Nocturne in Black and Gold — The Falling Roc — James McNeill Whistler | [file page](https://commons.wikimedia.org/wiki/File:Whistler-Nocturne_in_black_and_gold.jpg) | Public domain | no | d.1903 | confirmed | `documented` |
| 65 | `olga-boznanska::Girl with Chrysanthemums` | gallery | Girl with Chrysanthemums — Olga Boznańska | [file page](https://commons.wikimedia.org/wiki/File:Olga_Bozna%C5%84ska_-_Girl_with_Chrysanthemums_-_MNK_II-b-1032_-_National_Museum_Krak%C3%B3w.jpg) | Public domain | no | d.1940 | confirmed | `documented` |
| 66 | `olympia` | catalog | Olympia — Édouard Manet | [file page](https://commons.wikimedia.org/wiki/File:Edouard_Manet_-_Olympia_-_Google_Art_ProjectFXD.jpg) | Public domain | no | d.1883 | confirmed | `documented` |
| 67 | `paolo-veronese::The Wedding at Cana` | gallery | The Wedding at Cana — Paolo Veronese | [file page](https://commons.wikimedia.org/wiki/File:Paolo_Veronese_008.jpg) | Public domain | no | d.1588 | confirmed | `documented` |
| 68 | `peder-severin-kroyer::Summer Evening on Skagen's Southern Beach` | gallery | Summer Evening on Skagen's Southern Beach — P.S. Krøyer | [file page](https://commons.wikimedia.org/wiki/File:P.S._Kr%C3%B8yer_-_Summer_evening_on_Skagen%27s_Beach._Anna_Ancher_and_Marie_Kr%C3%B8yer_walking_together._-_Google_Art_Project.jpg) | Public domain | no | d.1909 | confirmed | `documented` |
| 69 | `peter-paul-rubens::The Garden of Love` | gallery | The Garden of Love — Peter Paul Rubens | [file page](https://commons.wikimedia.org/wiki/File:El_Jard%C3%ADn_del_Amor_(Rubens).jpg) | Public domain | no | d.1640 | confirmed | `documented` |
| 70 | `portrait-of-innocent-x` | catalog | Portrait of Innocent X — Diego Velázquez | [file page](https://commons.wikimedia.org/wiki/File:Retrato_del_Papa_Inocencio_X._Roma,_by_Diego_Vel%C3%A1zquez.jpg) | Public domain | no | d.1660 | confirmed | `documented` |
| 71 | `primavera` | catalog | Primavera — Sandro Botticelli | [file page](https://commons.wikimedia.org/wiki/File:Botticelli-primavera.jpg) | Public domain | no | d.1510 | confirmed | `documented` |
| 72 | `raja-ravi-varma::Lady in the Moonlight` | gallery | Lady in the Moonlight — Raja Ravi Varma | [file page](https://commons.wikimedia.org/wiki/File:Raja_Ravi_Varma,_Lady_in_the_Moon_Light_(1889).jpg) | Public domain | no | d.1906 | confirmed | `documented` |
| 73 | `raphael::La Fornarina` | gallery | La Fornarina — Raphael | [file page](https://commons.wikimedia.org/wiki/File:La_Fornarina_by_Raffaello.jpg) | Public domain | no | d.1520 | confirmed | `documented` |
| 74 | `red-fuji` | catalog | Fine Wind, Clear Morning (Red Fuji) — Katsushika Hokusai | [file page](https://commons.wikimedia.org/wiki/File:Katsushika_Hokusai_-_Fine_Wind,_Clear_Morning_(Gaif%C5%AB_kaisei)_-_Google_Art_Project.jpg) | Public domain | no | d.1849 | confirmed | `documented` |
| 75 | `saturn-devouring-his-son` | catalog | Saturn Devouring His Son — Francisco Goya | [file page](https://commons.wikimedia.org/wiki/File:Francisco_de_Goya,_Saturno_devorando_a_su_hijo_(1819-1823).jpg) | Public domain | no | d.1828 | confirmed | `documented` |
| 76 | `seker-ahmed-pasha::Self-Portrait` | gallery | Self-Portrait — Şeker Ahmed Paşa | [file page](https://commons.wikimedia.org/wiki/File:Seker_ahmet_pasa.jpg) | Public domain | no | d.1907 | confirmed | `documented` |
| 77 | `self-portrait-as-the-allegory-of-painting` | catalog | Self-Portrait as the Allegory of Painting — Artemisia Gentileschi | [file page](https://commons.wikimedia.org/wiki/File:Self-portrait_as_the_Allegory_of_Painting_(La_Pittura)_-_Artemisia_Gentileschi.jpg) | Public domain | no | d.1656 | confirmed | `documented` |
| 78 | `self-portrait-at-28` | catalog | Self-Portrait at Twenty-Eight — Albrecht Dürer | [file page](https://commons.wikimedia.org/wiki/File:Albrecht_D%C3%BCrer_-_1500_self-portrait_(High_resolution_and_detail).jpg) | Public domain | no | d.1528 | confirmed | `documented` |
| 79 | `sistine-madonna` | catalog | Sistine Madonna — Raphael | [file page](https://commons.wikimedia.org/wiki/File:RAFAEL_-_Madonna_Sixtina_(Gem%C3%A4ldegalerie_Alter_Meister,_Dresden,_1513-14._%C3%93leo_sobre_lienzo,_265_x_196_cm).jpg) | Public domain | no | d.1520 | confirmed | `documented` |
| 80 | `slave-ship` | catalog | The Slave Ship — J.M.W. Turner | [file page](https://commons.wikimedia.org/wiki/File:Slave-ship.jpg) | Public domain | no | d.1851 | confirmed | `documented` |
| 81 | `sofonisba-anguissola::Portrait of Philip II` | gallery | Portrait of Philip II — Sofonisba Anguissola | [file page](https://commons.wikimedia.org/wiki/File:Portrait_of_Philip_II_of_Spain_by_Sofonisba_Anguissola_-_002b.jpg) | Public domain | no | d.1625 | confirmed | `documented` |
| 82 | `sunflowers` | catalog | Sunflowers — Vincent van Gogh | [file page](https://commons.wikimedia.org/wiki/File:Vincent_Willem_van_Gogh_127.jpg) | Public domain | no | d.1890 | confirmed | `documented` |
| 83 | `swan-no-17` | catalog | The Swan, No. 17 — Hilma af Klint | [file page](https://commons.wikimedia.org/wiki/File:Hilma_af_Klint,_1915,_Svanen,_No._17.jpg) | Public domain | no | d.1944 | confirmed | `documented` |
| 84 | `the-arnolfini-portrait` | catalog | The Arnolfini Portrait — Jan van Eyck | [file page](https://commons.wikimedia.org/wiki/File:Van_Eyck_-_Arnolfini_Portrait.jpg) | Public domain | no | d.1441 | confirmed | `documented` |
| 85 | `the-art-of-painting` | catalog | The Art of Painting — Johannes Vermeer | [file page](https://commons.wikimedia.org/wiki/File:Jan_Vermeer_-_The_Art_of_Painting_-_Google_Art_Project.jpg) | Public domain | no | d.1675 | confirmed | `documented` |
| 86 | `the-basket-of-apples` | catalog | The Basket of Apples — Paul Cézanne | [file page](https://commons.wikimedia.org/wiki/File:Paul_C%C3%A9zanne_-_The_Basket_of_Apples_-_1926.252_-_Art_Institute_of_Chicago.jpg) | Public domain | no | d.1906 | confirmed | `documented` |
| 87 | `the-beheading-of-saint-john` | catalog | The Beheading of Saint John the Baptist — Caravaggio | [file page](https://commons.wikimedia.org/wiki/File:La_decapitaci%C3%B3n_de_San_Juan_Bautista,_por_Caravaggio.jpg) | Public domain | no | d.1610 | confirmed | `documented` |
| 88 | `the-birth-of-venus` | catalog | The Birth of Venus — Sandro Botticelli | [file page](https://commons.wikimedia.org/wiki/File:Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg) | Public domain | no | d.1510 | confirmed | `documented` |
| 89 | `the-calling-of-saint-matthew` | catalog | The Calling of Saint Matthew — Caravaggio | [file page](https://commons.wikimedia.org/wiki/File:Caravaggio_%E2%80%94_The_Calling_of_Saint_Matthew.jpg) | CC0 | no | d.1610 | confirmed | `documented` |
| 90 | `the-card-players` | catalog | The Card Players — Paul Cézanne | [file page](https://commons.wikimedia.org/wiki/File:Les_Joueurs_de_cartes_-_Paul_C%C3%A9zanne.jpg) | Public domain | no | d.1906 | confirmed | `documented` |
| 91 | `the-childs-bath` | catalog | The Child's Bath — Mary Cassatt | [file page](https://commons.wikimedia.org/wiki/File:Mary_Cassatt_-_The_Child%27s_Bath_-_Google_Art_Project.jpg) | Public domain | no | d.1926 | confirmed | `documented` |
| 92 | `the-creation-of-adam` | catalog | The Creation of Adam — Michelangelo Buonarroti | [file page](https://commons.wikimedia.org/wiki/File:Michelangelo_-_Creation_of_Adam_(cropped).jpg) | Public domain | no | d.1564 | confirmed | `documented` |
| 93 | `the-dance-class` | catalog | The Dance Class — Edgar Degas | [file page](https://commons.wikimedia.org/wiki/File:Edgar_Degas_-_La_Classe_de_danse.jpg) | Public domain | no | d.1917 | confirmed | `documented` |
| 94 | `the-dance-of-life` | catalog | The Dance of Life — Edvard Munch | [file page](https://commons.wikimedia.org/wiki/File:Edvard_Munch_-_The_dance_of_life_(1899-1900).jpg) | Public domain | no | d.1944 | confirmed | `documented` |
| 95 | `the-dog` | catalog | The Dog — Francisco Goya | [file page](https://commons.wikimedia.org/wiki/File:Goya.hund.jpg) | Public domain | no | d.1828 | confirmed | `documented` |
| 96 | `the-fighting-temeraire` | catalog | The Fighting Temeraire — J.M.W. Turner | [file page](https://commons.wikimedia.org/wiki/File:The_Fighting_Temeraire,_JMW_Turner,_National_Gallery.jpg) | Public domain | no | d.1851 | confirmed | `documented` |
| 97 | `the-garden-of-earthly-delights` | catalog | The Garden of Earthly Delights — Hieronymus Bosch | [file page](https://commons.wikimedia.org/wiki/File:The_Garden_of_Earthly_Delights_by_Bosch_High_Resolution.jpg) | Public domain | no | d.1516 | confirmed | `documented` |
| 98 | `the-great-wave-off-kanagawa` | catalog | The Great Wave off Kanagawa — Katsushika Hokusai | [file page](https://commons.wikimedia.org/wiki/File:Tsunami_by_hokusai_19th_century.jpg) | Public domain | no | d.1849 | confirmed | `documented` |
| 99 | `the-haywain-triptych` | catalog | The Haywain Triptych — Hieronymus Bosch | [file page](https://commons.wikimedia.org/wiki/File:Bosch_-_Haywain_Triptych.jpg) | Public domain | no | d.1516 | confirmed | `documented` |
| 100 | `the-jewish-bride` | catalog | The Jewish Bride — Rembrandt van Rijn | [file page](https://commons.wikimedia.org/wiki/File:Rembrandt_Harmensz._van_Rijn_-_Portret_van_een_paar_als_oudtestamentische_figuren,_genaamd_%27Het_Joodse_bruidje%27_-_Google_Art_Project.jpg) | Public domain | no | d.1669 | confirmed | `documented` |
| 101 | `the-kiss` | catalog | The Kiss — Gustav Klimt | [file page](https://commons.wikimedia.org/wiki/File:The_Kiss_-_Gustav_Klimt_-_Google_Cultural_Institute.jpg) | Public domain | no | d.1918 | confirmed | `documented` |
| 102 | `the-last-supper` | catalog | The Last Supper — Leonardo da Vinci | [file page](https://commons.wikimedia.org/wiki/File:The_Last_Supper_-_Leonardo_Da_Vinci_-_High_Resolution_32x16.jpg) | Public domain | no | d.1519 | confirmed | `documented` |
| 103 | `the-naked-maja` | catalog | The Naked Maja — Francisco Goya | [file page](https://commons.wikimedia.org/wiki/File:Goya_Maja_naga2.jpg) | Public domain | no | d.1828 | confirmed | `documented` |
| 104 | `the-night-watch` | catalog | The Night Watch — Rembrandt van Rijn | [file page](https://commons.wikimedia.org/wiki/File:La_ronda_de_noche,_por_Rembrandt_van_Rijn.jpg) | Public domain | no | d.1669 | confirmed | `documented` |
| 105 | `the-potato-eaters` | catalog | The Potato Eaters — Vincent van Gogh | [file page](https://commons.wikimedia.org/wiki/File:De_aardappeleters_-_s0005V1962_-_Van_Gogh_Museum.jpg) | Public domain | no | d.1890 | confirmed | `documented` |
| 106 | `the-return-of-the-prodigal-son` | catalog | The Return of the Prodigal Son — Rembrandt van Rijn | [file page](https://commons.wikimedia.org/wiki/File:Rembrandt_Harmensz_van_Rijn_-_Return_of_the_Prodigal_Son_-_Google_Art_Project.jpg) | Public domain | no | d.1669 | confirmed | `documented` |
| 107 | `the-school-of-athens` | catalog | The School of Athens — Raphael | [file page](https://commons.wikimedia.org/wiki/File:%22The_School_of_Athens%22_by_Raffaello_Sanzio_da_Urbino.jpg) | Public domain | no | d.1520 | confirmed | `documented` |
| 108 | `the-scream` | catalog | The Scream — Edvard Munch | [file page](https://commons.wikimedia.org/wiki/File:Edvard_Munch,_1893,_The_Scream,_oil,_tempera_and_pastel_on_cardboard,_91_x_73_cm,_National_Gallery_of_Norway.jpg) | Public domain | no | d.1944 | confirmed | `documented` |
| 109 | `the-sick-child` | catalog | The Sick Child — Edvard Munch | [file page](https://commons.wikimedia.org/wiki/File:Munch_Det_Syke_Barn_1885-86.jpg) | Public domain | no | d.1944 | confirmed | `documented` |
| 110 | `the-starry-night` | catalog | The Starry Night — Vincent van Gogh | [file page](https://commons.wikimedia.org/wiki/File:Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg) | Public domain | no | d.1890 | confirmed | `documented` |
| 111 | `the-ten-largest-no-7` | catalog | The Ten Largest, No. 7, Adulthood — Hilma af Klint | [file page](https://commons.wikimedia.org/wiki/File:Hilma_af_Klint_-_The_Ten_Largest_No._7_-_Adulthood_-_1907.jpg) | Public domain | no | d.1944 | confirmed | `documented` |
| 112 | `the-third-of-may-1808` | catalog | The Third of May 1808 — Francisco Goya | [file page](https://commons.wikimedia.org/wiki/File:El_Tres_de_Mayo,_by_Francisco_de_Goya,_from_Prado_thin_black_margin.jpg) | Public domain | no | d.1828 | confirmed | `documented` |
| 113 | `the-tower-of-babel` | catalog | The Tower of Babel — Pieter Bruegel the Elder | [file page](https://commons.wikimedia.org/wiki/File:Pieter_Bruegel_the_Elder_-_The_Tower_of_Babel_(Vienna)_-_Google_Art_Project_-_edited.jpg) | Public domain | no | d.1569 | confirmed | `documented` |
| 114 | `the-trinity` | catalog | The Trinity — Andrei Rublev | [file page](https://commons.wikimedia.org/wiki/File:Andrey_Rublev_-_%D0%A1%D0%B2._%D0%A2%D1%80%D0%BE%D0%B8%D1%86%D0%B0_-_Google_Art_Project.jpg) | Public domain | no | d.1428 | confirmed | `documented` |
| 115 | `thomas-gainsborough::Mr and Mrs Andrews` | gallery | Mr and Mrs Andrews — Thomas Gainsborough | [file page](https://commons.wikimedia.org/wiki/File:Thomas_Gainsborough_-_Mr_and_Mrs_Andrews.jpg) | Public domain | no | d.1788 | confirmed | `documented` |
| 116 | `utagawa-hiroshige::Sudden Shower over Shin-Ōhashi` | gallery | Sudden Shower over Shin-Ōhashi — Utagawa Hiroshige | [file page](https://commons.wikimedia.org/wiki/File:Hiroshige,_Sudden_shower_over_Shin-%C5%8Chashi_bridge_and_Atake,_1857.jpg) | Public domain | no | d.1858 | confirmed | `documented` |
| 117 | `view-of-delft` | catalog | View of Delft — Johannes Vermeer | [file page](https://commons.wikimedia.org/wiki/File:Vermeer-view-of-delft.jpg) | Public domain | no | d.1675 | confirmed | `documented` |
| 118 | `view-of-toledo` | catalog | View of Toledo — El Greco | [file page](https://commons.wikimedia.org/wiki/File:El_Greco_View_of_Toledo.jpg) | Public domain | no | d.1614 | confirmed | `documented` |
| 119 | `vision-after-the-sermon` | catalog | Vision After the Sermon — Paul Gauguin | [file page](https://commons.wikimedia.org/wiki/File:La_vision_apr%C3%A8s_le_sermon_(Paul_Gauguin).jpg) | Public domain | no | d.1903 | confirmed | `documented` |
| 120 | `water-lilies-grandes-decorations` | catalog | Water Lilies (Grandes Décorations) — Claude Monet | [file page](https://commons.wikimedia.org/wiki/File:Claude_Monet_-_The_Water_Lilies_-_Setting_Sun_-_Google_Art_Project.jpg) | Public domain | no | d.1926 | confirmed | `documented` |
| 121 | `wheatfield-with-crows` | catalog | Wheatfield with Crows — Vincent van Gogh | [file page](https://commons.wikimedia.org/wiki/File:Korenveld_met_kraaien_-_s0149V1962_-_Van_Gogh_Museum.jpg) | Public domain | no | d.1890 | confirmed | `documented` |
| 122 | `where-do-we-come-from` | catalog | Where Do We Come From? What Are We? Where Ar — Paul Gauguin | [file page](https://commons.wikimedia.org/wiki/File:Gauguin_-_Where_Do_We_Come_From%3F_What_Are_We%3F_Where_Are_We_Going%3F_(1897-98).jpg) | Public domain | no | d.1903 | confirmed | `documented` |

---

**No clearance determination has been made for any asset in this register.**
Per OD-5 and AC28 a rights clearance requires qualified legal or rights review
with its scope and residual uncertainty recorded. This document records asserted
basis, attribution obligation, depiction accuracy and residual uncertainty only.
