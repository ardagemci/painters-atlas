# PIG-001 — Rights Remediation (Directives 1–3)

**Status:** Directives 1 and 3 complete; Directive 2 **not needed**. Compiled by
the Synthesis Lead from Seurat's partial run (cut off by a session limit before
it wrote this record) plus independent verification. Every licence claim below
was re-verified against the Commons API by the Synthesis Lead, not inherited.

## Directive 1 — PD replacements found for BOTH frescoes ✅

The owner asked us to look for images carrying a Commons public-domain
assertion before accepting attribution obligations. Both were found, and both
replacements also fix the
`page` field to point at a real Commons **file page** instead of an English
Wikipedia article (the documentation defect affecting 92 of 122 sampled records).

| Record | Old image | New image | Verified licence |
| --- | --- | --- | --- |
| `sistine-chapel-ceiling` (js/catalog-1.js) | `Sistine_Chapel_ceiling_02_(brightened).jpg` — CC BY-SA 3.0 | `Sistine_ceiling.jpg` (Web Gallery of Art; Artist: Michelangelo) | **Public domain** (`License: pd`, `UsageTerms: Public domain`) |
| `correggio` → *Assumption of the Virgin* (js/artworks.js) | `Cathedral_(Parma)_-_Assumption_by_Correggio.jpg` — CC BY-SA 4.0 | `Cupola_Duomo_Parma_Correggio.jpg` (uploader own work, PD-dedicated) | **Public domain** (`License: pd`, `UsageTerms: Public domain`) |

Verification command (both files, ≥0.6s spacing):
`commons.wikimedia.org/w/api.php?action=query&titles=File:<name>&prop=imageinfo&iiprop=extmetadata`

**Consequence:** `status:"pd"` is now a TRUE claim for the Sistine record. No
status-vocabulary change, no attribution rendering, and no daily-pool behaviour
change is required. **Directive 2 (option b) is moot** and was not executed.

Residual note, recorded honestly per OD-5: we rely on Commons' own PD
determination for both files; we assert no independent legal clearance. The
Sistine file is a flat reproduction credited to Michelangelo (PD-Art rationale);
the Correggio file is a photographer's explicit PD dedication of their own work.

Prerendered stubs `p/artwork/sistine-chapel-ceiling.html` and
`p/artist/correggio.html` were regenerated to match.

## Directive 3 — Museum photographs: YES, a real attribution gap ⚠️

All **103** museum-note photographs (`js/museums-1.js` `photo:{src,page}`) were
resolved against Commons — 0 unverified, 0 transient failures recorded as
negatives.

| Licence | Count |
| --- | --- |
| CC BY-SA 4.0 | 39 |
| CC BY-SA 3.0 | 20 |
| CC BY 2.0 | 9 |
| CC BY 4.0 | 8 |
| Public domain | 8 |
| CC0 | 7 |
| CC BY-SA 2.0 | 6 |
| CC BY 3.0 | 4 |
| CC BY 2.5 | 1 |
| No restrictions | 1 |

**Verdict — plainly: this is an actual compliance gap, not a hypothetical one.**
**87 of 103** museum photographs (84%) carry a licence requiring attribution,
and Pigment currently provides none. **65** of those are share-alike (CC BY-SA).
Only 16 (8 PD + 7 CC0 + 1 No-restrictions) carry no obligation.

**Proportion and character.** This is a *paperwork* failure, not a
misappropriation: every file is freely licensed for exactly this use, and every
one is used as intended. Nothing here is "stolen" and no image is the wrong
subject (unlike the 8 artwork mismatches). Displaying an image is also not
creating a derivative work, so the share-alike clause does not propagate to
Pigment's own content — the operative obligation is **credit the photographer,
name the licence, link to it**. It is nonetheless a genuine licence-term breach
until credit is rendered, and 87 is not a rounding error.

**Recommended remediation (NOT built — Implementation Lead's work):** render
per-photo credit (author + licence name + licence link + Commons file-page link)
on each museum page, plus a consolidated credits surface. The data already
exists in `evidence/museum-photo-rights.json` (103 entries with author, licence,
licence URL, and Commons title), so this is a rendering unit, not a research
unit.

## Superseding exposure statement

| Category | Round 1 claim | Verified position now |
| --- | --- | --- |
| Wrong-artwork images | not checked | 8 found; 4 removed, 3 corrected, 1 documented |
| Fresco photographer copyright | not checked | **resolved** — PD replacements found for both |
| Museum-photo attribution | not sampled | **87 of 103 require credit; none rendered — real gap** |
| Artwork-image PD basis | "zero exposure" | holds for the sampled corpus; documentation still thin (92 of 122 `page` fields point at Wikipedia articles, not Commons file pages) |
| Legal clearance | never claimed | still never claimed (OD-5) |
