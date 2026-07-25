# PIG-001 — Build Evidence Report, Unit 24 (photo attribution surface)

**Author:** Dürer (`claude-implementation-lead`), Implementation Lead
**Date:** 2026-07-25
**Branch:** `pig-001-stabilization` (verified; never `main`; not pushed)
**Gate 1:** VERIFIED — `protocol/tasks/PIG-001/specification.md:8`
`workflow_state: "approved_for_build"`.
**Owner input honored:** the owner explicitly authorised this unit. Directive 3
of `evidence/rights-remediation.md` named the remediation as *rendering*, not
research; that is what was built, plus the census described under "the artwork
side" below, which the brief asked for and which changed the size of the problem.

## Commits

| SHA | Scope |
| --- | --- |
| `4259932` | Registry + tools + validator: `js/photo-credits.js`, `tools/build_photo_credits.py`, `tools/audit_artwork_rights.py`, `tools/audit_museum_photo_rights.py`, `tools/validate.jxa.js`, `protocol/tasks/PIG-001/evidence/artwork-image-rights.json` |
| `a4417d4` | Rendering: `js/app.js`, `css/styles.css`, `index.html`, `tools/build_seo.jxa.js`, 679 prerendered stubs under `p/` |
| `9e572b6` | Three stubs held back during a concurrent data landing (`p/artist/alma-thomas.html`, `p/museum/guggenheim-ny.html`, `p/museum/whitney.html`) |

No `git add -A`; every commit used explicit paths. `THEORY_001.md`,
`protocol/tasks/PIG-001/CHALLENGE_001` and `protocol/tasks/PIG-001/THEORY_001`
left untracked, untouched.

## How the data gets into the shipped app

The rights evidence lives under `protocol/`, which is never served, so it could
not satisfy a licence term on its own. Three tools, one generated data file:

```
protocol/…/museum-photo-rights.json            (Seurat's census, 104 entries)
protocol/…/museum-photo-rights-supplement.json (optional top-up, mine)
protocol/…/artwork-image-rights.json           (my census, 694 images)
                     │
                     ├─ tools/audit_museum_photo_rights.py  → the supplement
                     ├─ tools/audit_artwork_rights.py       → the artwork census
                     └─ tools/build_photo_credits.py        → js/photo-credits.js
                                                               (stdlib, offline,
                                                                deterministic)
```

`js/photo-credits.js` follows the existing global-registry pattern and is wired
into `index.html` with a `?v=` string like every other data file:

* `window.PHOTO_CREDITS` — museum building photographs, keyed by venue id.
  **104 entries, 88 requiring attribution, 16 obligation-free.**
* `window.IMAGE_CREDITS` — artwork images that require attribution, keyed by
  Commons `File:` title as derived from the image URL. **28 entries.**

Shipped shape is `{ author, license, licenseUrl, page, required }` — nothing
else. Usage terms, fetch status and verification metadata stay in the evidence
files. Total payload 34 KB for both registries.

Public-domain and CC0 **artwork** images are deliberately absent from
`IMAGE_CREDITS`: they carry no obligation, and the existing "image via Wikimedia
Commons" link already names their origin. The 16 obligation-free **museum**
photographs *are* shipped and credited — see the decision below.

Runtime lookup is `commonsTitle(src)` in `js/app.js`, a mirror of
`commons_file_title()` in `tools/commons_rights.py` (thumbnail form included).
`tools/build_seo.jxa.js` carries its own copy, because JXA has no `URL` global.

## Where credit renders

| Surface | What renders |
| --- | --- |
| Museum page (`#/museum/:id`) | `Photograph: <author> · <licence, linked to the deed> · file on Commons`, as `.img-credit.mu-credit` directly under the hero |
| Artwork page (`#/artwork/:id`) | the same line under `.aw-provenance`, for the 28 licensed images |
| Lightbox | credit inside the `figcaption` — the enlarged view is where a gallery thumbnail *becomes* the image |
| Museums index | one line under the grid pointing at `#/credits` |
| `#/credits` | the consolidated surface, footer-linked beside Privacy |
| `p/museum/*.html`, `p/artwork/*.html`, `p/artist/*.html` | the same credit under the same photograph — **119 stubs** now carry one |

**Counts, measured in the running app (not copied):** 104 museum photographs
credited (88 licence-required, 16 courtesy); 28 artwork images credited; 132
rows on `#/credits` (104 + 28).

### The 82/21 decision (stated, as the brief asked)

The museum hero shows a **collage of the works** when the venue has any
PD-imaged works, and the building photograph only otherwise — measured: **82 of
103 heroes were collages, 21 showed the photograph**. Crediting only the 21
would have left the photograph credited nowhere it is actually seen, because it
is also that venue's card cover on the museums index and in the artwork page's
"Where it hangs" panel. So the credit renders on **every** museum page with a
photograph, and the museums index carries a pointer line. Logged as D-24-2.

### Obligation-free photographs (my call, stated)

The 16 PD/CC0/no-restrictions museum photographs get the same line, minus a
licence link they do not have: `Photograph: <author> · Public domain · file on
Commons`. Naming the photographer of a building photograph is good practice even
when not compelled, the source link is useful provenance, and a credit surface
with holes in it invites the reader to wonder which images "don't count". One
photograph (`minneapolis-institute-of-art`) has no author recorded on Commons;
it renders as `Photograph · Public domain · file on Commons`.

## The artwork side — what I actually found

The brief asked me to re-check rather than trust the old table. I did not
sample; I ran a **census of every renderable shipped artwork image**
(`tools/audit_artwork_rights.py`): every `image:{src,…,status:"pd"}` in
`js/catalog-{1..4}.js` (`status:"copyright"` ships no image) plus every
`window.ARTWORKS[artist][title].img` in `js/artworks.js`. **694 URLs, 0
unverified, 0 transient failures.**

| Licence | Images |
| --- | --- |
| Public domain | 648 |
| CC0 | 17 |
| CC BY-SA 4.0 | 13 |
| CC BY 2.0 | 7 |
| CC BY-SA 3.0 | 4 |
| CC BY 3.0 | 3 |
| CC BY 2.5 | 1 |
| CC BY 4.0 | 1 |

**29 shipped artwork images (28 distinct Commons files) still carry an
attribution-requiring licence — not the 2 the 122-record sample reported.** The
sample was not wrong about what it examined; it examined 122 of 694. All 28 are
now credited.

Three specific findings the register could not have contained:

1. **The Sistine replacement was only half-applied.** `evidence/rights-remediation.md`
   Directive 1 replaced the CC BY-SA 3.0 ceiling photograph in `js/catalog-1.js`
   with a PD file. The **gallery** record in `js/artworks.js` (`michelangelo` →
   "Sistine Chapel Ceiling") still ships
   `File:Sistine_Chapel_ceiling_02_(brightened).jpg`, CC BY-SA 3.0 by Antoine
   Taveneaux — re-verified live against the Commons API during this unit. It is
   now credited. I did **not** swap it: image records are the Data Steward's,
   and the same artwork now showing two different photographs in two surfaces is
   a data-consistency question for Seurat, not a rendering decision for me.
   **Recommended follow-up:** point the gallery record at
   `File:Sistine_ceiling.jpg`, the PD file the catalog already uses.
2. **Seven catalog records carry `image.status:"pd"` while Commons asserts a CC
   licence** — `black-fuji`, `pieta`, `david` (catalog-1), `triumph-of-death`
   (catalog-3), `little-dancer-aged-fourteen`, `vahine-no-te-tiare`,
   `the-ten-largest-no-9` (catalog-4). The images are legitimately usable and
   are now credited, but `status:"pd"` is a false statement in shipped data, the
   same defect the register flagged for `sistine-chapel-ceiling`. I did not
   change the field: `status !== "pd"` **hides the image** in eleven render
   paths, so correcting it is a data decision with visible product consequences.
   Escalated here rather than silently either way.
3. **The two CC0 records are fine.** `the-calling-of-saint-matthew` and
   `lumber-schooners-penobscot-bay` re-verified as CC0 — no attribution
   obligation, no action. The two CC BY-SA frescoes the brief flagged were
   indeed replaced with PD files in the catalog; only the gallery copy above
   survived.

Commons' `Artist` field sometimes names the **painter** rather than the
photographer (e.g. "Pieter Brueghel the Elder", "Max Beckmann"). That is the
field Commons offers for attribution, so it is what is rendered, under the
neutral label "Image credit" rather than "Photograph". Known limitation, not a
defect I can fix without contradicting the source.

## Sanitisation

Two passes, deliberately:

1. **Build time** — `plain()` in `tools/build_photo_credits.py` strips `<br>`,
   strips all tags, unescapes entities, removes bidi marks left by `<bdi>`, and
   collapses whitespace. Commons `Artist`/`Credit` values genuinely arrive as
   HTML (verified live during this unit: `File:Sistine_ceiling.jpg` returns
   `Credit` = `<a rel="nofollow" class="external free" href="…">…</a>`).
   Additionally, Commons' "No machine-readable author provided. *X* assumed
   (based on copyright claims)." placeholder is reduced to *X*, and freehand
   labels the renderer supplies itself ("Photo:", "Photograph by") are stripped
   so the line does not read "Photograph: Photo: Andreas Praefcke".
2. **Render time** — every field goes through the existing `esc()` helper inside
   the `js/app.js` IIFE, and through `build_seo.jxa.js`'s own `esc()` for stubs.
   No raw Commons HTML can reach a page even if a future evidence file contains
   some.

The generator also escapes `</` in emitted JS strings so no value can close the
`<script>` element.

## Validator

`osascript -l JavaScript tools/validate.jxa.js`:

```
app.js: syntax OK
artists: 256, movements: 76, techniques: 39, eras: 8, nations: 37, painter styles: 27,
influence edges: 238, venues: 116, catalog: 323 (tier1: 76), daily pool: 75,
museum notes: 104, photo credits: 104 (attribution required: 88),
artwork image credits: 28, personas: 15, lists: 12 (featured: 4),
tier1 artists: 36 (arcs: 36)
ALL REFERENCES VALID
```

**Zero warnings before, zero warnings after** — as required. New checks added
(the brief invited them):

* every museum note with a photograph must have a credit record — **error**, not
  a warning, because uncredited use of an attribution-required file is a licence
  breach, not a cosmetic gap;
* an attribution-required record must carry author, licence name, licence URL
  and Commons file page;
* a credit for a photograph no longer shown is a warning (stale registry);
* `PHOTO_CREDITS` keys must be real venue ids; `IMAGE_CREDITS` keys must be
  `File:` titles with complete credit fields;
* counts added to the summary line so drift is visible.

This check fired for real during the unit: a museum note added concurrently
(`hirshhorn`) had no credit record, and the build failed until the record
existed. That is the check working as intended.

## Smoke test and browser evidence

`python3 -m http.server 8421 -d .` + `curl`: `/`, `/index.html`,
`/js/photo-credits.js`, `/js/app.js`, `/css/styles.css`, `/p/museum/prado.html`
→ all `200`; `index.html` contains the `photo-credits.js` script tag and
`href="#/credits"`; `js/app.js` contains `case "credits"`.

Real browser at `http://localhost:8421`, both themes:

* `#/museum/prado` (dark and light) — renders
  `Photograph: Emilio J. Rodríguez Posada · CC BY-SA 2.0 · file on Commons`,
  the licence name linked to `creativecommons.org/licenses/by-sa/2.0`
  (`rel="noopener license"`) and the file page to `commons.wikimedia.org`.
* `#/museum/hirshhorn` (dark) — the museum added mid-unit picks up
  `Photograph: Quadell · CC BY-SA 3.0 · file on Commons` with no code change:
  the pipeline handles new photographs.
* `#/artwork/pieta` — provenance line unchanged, credit line beneath it reads
  `Image credit: original file by Stanislav Traykov · CC BY 2.5 · file on
  Commons`; clicking the hero opens the lightbox and the same credit appears in
  the `figcaption`.
* `#/credits` (dark and light) — 132 rows, four sections, all links resolve;
  section headings show live counts ("104 buildings · 88 under a licence
  requiring credit", "28 of 687 images in the atlas").
* Mobile 375×812 — `.credit-list` rows stack (`display:block` under the 640px
  breakpoint), `document.scrollWidth === window.innerWidth`, no horizontal
  overflow.

Credit text uses `var(--muted)` rather than `var(--faint)`: `--faint` is
`#a39a86` in light mode, which is weak on `#f2ecdf` paper. `--muted` reads in
both palettes.

## Deviation ledger (Gate 3)

| # | Deviation | Rationale | Status |
| --- | --- | --- | --- |
| D-24-1 | Built **two** registries, not the single venue-keyed `PHOTO_CREDITS` the brief specified | The census found 28 shipped artwork images that also require credit. A venue-keyed map cannot express them. Both live in one generated file, both follow the global-registry pattern. | Accepted |
| D-24-2 | Museum credit renders on all 104 museum pages, not only the 21 whose hero shows the photograph | The photograph is the venue's card cover across the atlas; crediting only the 21 would credit it nowhere most readers see it. Detail above. | Accepted |
| D-24-3 | The 16 obligation-free museum photographs are credited too | The brief left this to my call and asked me to state it. Stated above. | Accepted |
| D-24-4 | Removed the old "photo via Wikimedia Commons" link from `.mu-sub` where a credit record exists | It duplicated the new line and pointed at an *English Wikipedia article* for most venues — the documentation defect the register flagged. The credit line links the actual Commons file page. The old link still renders as a fallback if a record is missing. | Accepted |
| D-24-5 | Privacy page edited (not in the brief) | Credit lines add `creativecommons.org` (and one `flickr.com`) as click-through hosts. Unit 23's privacy copy enumerates those hosts; leaving it unchanged would have made a shipped privacy statement incomplete. AC14. | Accepted |
| D-24-6 | Prerendered stubs regenerated (679 files) | `p/museum/*.html` display the same photographs to crawlers and scrapers and owed the same credit. Generator-driven, not hand-edited; 119 stubs now carry a credit line. | Accepted |
| D-24-7 | Did **not** fix the two artwork-data defects found (gallery Sistine record, seven false `status:"pd"` values) | Image records are the Data Steward's, and `status` gates whether an image renders at all. Reported above with a recommendation instead of silently changing product behaviour. | Escalated |
| D-24-8 | `index.html` committed while a teammate's concurrent `?v=` bumps were in it | The file is shared and my script tag had to ship. Their bumps were preserved, not reverted. Three stubs carrying their in-flight data were held out of the rendering commit and committed separately once their data landed (`9e572b6`). | Accepted |

## Self-assessment vs acceptance criteria

* **AC11 (rights/attribution integrity)** — PASS, and stronger than before. The
  attribution obligation is now discharged on every surface that shows a
  licensed image: 104 museum photographs and 28 artwork images, in-app and in
  the prerendered stubs, each with author, licence, licence deed and source
  file. Coverage is enforced by the validator rather than by vigilance. Residual
  is reported, not hidden: two data defects escalated in D-24-7.
* **AC12 (provenance recorded, no clearance claimed)** — PASS. Every credit
  links the Commons file page, which is the provenance the register found
  missing from 92 of 122 `image.page` fields. Nothing in the shipped copy or in
  either evidence file claims a legal clearance; `legal_conclusion: "none"` is
  carried through both censuses, per OD-5.
* **AC14 (no overclaim)** — PASS. Counts on `#/credits` are computed from the
  registries at render time, so no number in the interface can drift from what
  ships. The privacy page was updated rather than left to overstate the host
  inventory. The credits page says plainly that most images are public domain
  and that this is not a clearance.
* **AC26 (zero-dependency architecture)** — PASS. One new static data file, no
  new runtime dependency, no build step in the serving path, no framework. Tools
  are Python stdlib and JXA. The generated registry is a plain global, loaded by
  a plain `<script>` tag with a `?v=` string.

## Known limitations

* Grid thumbnails (artwork cards, museum cards, the artist "Major works" panel)
  do not carry an inline credit — the credit is one click away, on the work's
  own page or in the lightbox. Rendering 40 credit lines into a card grid would
  make the atlas unreadable; CC's own guidance accepts a link to the credit
  where the medium makes inline attribution impractical. Called out for Van Eyck
  rather than assumed acceptable.
* Commons' `Artist` field occasionally names the painter instead of the
  photographer (above). Faithful to the source, imperfect as prose.
* The two data defects in D-24-7 are open.
* No per-viewport screenshot pack for `#/credits`; desktop dark, desktop light
  and mobile 375 were verified live in-browser during this unit. A full Vermeer
  viewport pass has not been run against the new route.
* Gate 2 is **not** certified here — that remains Van Eyck's call.
