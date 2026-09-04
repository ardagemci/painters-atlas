<!-- FILED 2026-09-04 by the Synthesis Lead. Produced by Mondrian
     (claude-ux-architect), lead of OP-INTERFACE, under Gate 1 with
     build_authorized: false — no production file was touched.

     Verified before filing:
       * `.aw-hero{...cursor:zoom-in...}` is css/styles.css:857, not 858, and is
         indeed unconditional — already wrong for today's generative hero.
       * The duplicated-predicate finding behind REQ-P1 holds and is worse than
         stated: `w.image && w.image.src && w.image.status === "pd"` appears
         EIGHT times verbatim in js/app.js, plus three `cw.image` variants, two
         bare `.status === "pd"`, one `.status === "copyright"`, and the two
         mini-card rails testing `.src` with no status check at all. A predicate
         written out eight times is how 2246/2248 drifted.
     This is a requirements artifact for a Theory Brief to be written against.
     It is not a specification and authorises nothing. -->

# UX REQUIREMENTS — IFACE-001: the withheld record

**Author:** Mondrian, OP-INTERFACE lead. **Baseline:** `5e05dcc`.
**Gate 1:** `build_authorized: false`; no production file was modified and
nothing here is authorization. Wording marked ◆ is rights-bearing and needs
OP-RIGHTS ratification (`OP-INTERFACE.md`, Standing notes).

**SCOPE:** `#/artwork/:id`, every grid and rail that can surface an artwork
record, `p/artwork/*.html`. **IA CHANGES: none** — no new route, no new object
type. A fourth *presentation state* on an existing record.

## 1. What the reader encounters — the mount

Not a canvas, not a spinner, not a grey box. A **mount**: the empty passe-partout
a print is lifted out of.

`.aw-hero` (css:854) keeps its frame, radius and `--panel` ground. In place of
`.aw-hero-gen`, a new `.aw-hero-mount`:

- An inner rectangle inset ~28px, hairline `--line2`, interior `--panel2`.
  **No `<canvas>`, no palette, no artist style, no sheen, no hover scale.**
- **Drawn at the work's true proportions** from `w.dims` when it parses — capped
  at 340px tall to match today's canvas (css:861) so nothing jumps — else 16/10.
  The reader is shown the *shape and size* of the picture they are not being
  shown: real information, pure metadata, honest weight.
- Centred inside: medium and dimensions in the sans, letterspaced
  (`Oil on canvas · 92 × 73 cm`); beneath a hairline rule, the reason line (§3).
  Nothing else — title, artist and year stay where they are already
  (`js/app.js:2208-2210`); the mount must not duplicate the page.
- `.aw-hero{cursor:zoom-in}` (css:858) is unconditional today and already wrong
  for the generative hero. Here the cursor is `default` and no `data-lb-*`
  attributes are emitted (2200).

Everything below the hero is unchanged, and that is the point. A withheld record
reads as **a page whose picture is elsewhere**, not one missing its middle.

## 2. Surface inventory

`R` = the renderable predicate of §5.

| # | Site | `js/app.js` | Behaviour |
|---|---|---|---|
| 1 | Artwork hero | 2204 | **Mount**, full, reason line visible |
| 2 | Artwork card | 879 | **Mount, reduced**: frame and rule only, no text — a 16:10 card cannot carry a sentence. Meaning via `.sr-only` (§4) |
| 3 | List entry `.le-art` | 1831 | **Mount, bare**, 132×100 / 92×74 mobile (css:1561,1588) |
| 4 | Arc strip | 2037 | **Mount, bare**, 46×46 (css:802) |
| 5 | "More by" rail | 2246 | **Mount, bare**, 52×38 (css:888) |
| 6 | "Near it" rail | 2248 | **Mount, bare**, same |
| 7 | Museum card cover | 1574→1580 | **Excluded from selection.** `works.find()` applies `R`; card falls to the building photo or the next renderable work |
| 8 | Actuality card cover | 1714→1719 | **Excluded from selection** |
| 9 | List card cover | 1769→1773 | **Excluded**; fall to the next work in `l.works` satisfying `R` |
| 10 | List hero | 1803→1810 | **Excluded**, same fallback. Mount only if no work in the list qualifies — then bare, no reason line: the list is not the withheld record |

7–10 are the legitimate "show nothing" cases: a venue card is about the venue, an
actuality card about an article, and neither should carry another record's
absence. In all four the record still appears as an *entry* further down the page
(sites 2–6); only its promotion to cover is withdrawn. Nothing leaves the atlas.

**Pools** — 1485 (Painting of the Day), 1609 (museum collage), 3363 (`deckPool`),
2476/2495 (`shippedImageTitles`/`creditUsage`) all move to `R`. A withheld record
is never Painting of the Day, never in a collage or the deck, and does not appear
in `#/credits` as a shipped image.

**Prerender** — `tools/build_seo.jxa.js:177` uses the same predicate; `img` is
null and `page()` (131-133) already degrades to `twitter:card: summary` with no
`og:image`. **No site-default image may be substituted** — sharing is the one
surface where a stand-in would be read as the work. The stub is re-emitted in the
same commit (OP-INTERFACE AC 6); `triumph-of-death` shipped stale social metadata
once already.

## 3. Distinguishable from the three existing states

All three today contain a *painted colour field* (`canvasTag`, 850). The fourth
contains no canvas at all. **Colour versus paper** is the difference a reader gets
without reading — it survives a thumbnail, a squint, and a 46px rail, which no
wording does.

| State | Reader sees | Line |
|---|---|---|
| Image | The photograph | — |
| Walled | Paint + floating pill | "a seeded Pigment interpretation — the original artwork remains under copyright" (2205) |
| Unphotographed | Paint + floating pill | "an interpretation painted in the browser — the original is unphotographed" (2206) |
| **Withheld** | Empty ruled mount, no paint | ◆ **"No picture here — this work is catalogued by its facts alone."** |

Second difference: the two existing labels float *over* paint in a translucent
pill (css:862-867). The withheld line sits **in the flow, on the ground, under a
rule**. It is not a caption on an artwork, because there is no artwork.

## 4. Accessibility — an absence has no accessible name

**A deliberate absence is not an image and must not be announced as one.**
`role="img" aria-label="no image"` announces *"image, no image"* — exactly the
defect class PIG-001 spent thirty-seven units on (`docs/BACKLOG.md:467`).

- **MUST** the mount is `aria-hidden="true"` decoration; `coverLabel()` (849) is
  not called in this state.
- **MUST** meaning is carried by real text: on the hero, the reason line is
  visible text in the flow, read after the breadcrumb and before the `<h1>`; on
  sites 2–6 the link gains an `.sr-only` span (css:469) so its accessible name
  ends `"— no picture in the atlas"` ◆.
- **MUST** nothing announces "loading", "unavailable", "error" or "missing". This
  is a finished state.
- **MUST** the mount is not focusable; focus order unchanged at every site.
- **MUST** reason line and dims meet 4.5:1 in both themes.
- **N/A** loading, error and recovery — nothing loads, nothing can fail, nothing
  is recovered. Recorded rather than left implicit.

## 5. The trap at 2246/2248 — one predicate, no site-local tests

Both gate on `o.image && o.image.src` with no status check, and are correct only
by the accident that all 61 `copyright` records carry no `src`.

**REQ-P1 (must).** One helper — `renderableImage(rec)` — is the *only* expression
of renderability in `js/app.js`. All 10 sites and 4 pools call it; **no site tests
`.src` or `.status` directly.** A guard test asserts zero such expressions outside
the helper (today: 20). This makes 2246/2248 correct by construction rather than
by coincidence, and it is the requirement that closes the leak.

**REQ-P2 (must).** The predicate returns false for a withheld record **whose `src`
is still present**. Any design expressing withholding only as absence of `src`
fails — it re-creates the same accident under a new name.

**REQ-P3 (must).** The predicate spans both registries. `window.ARTWORKS`
(`js/artworks.js`, 581 entries, zero `status` — E-007) consults the same gate, or
the state is a fiction on artist pages. *How* — unification or a second gate — is
the spec's choice; honouring one gate is not.

## 6. What I will not build

1. **C3 / C4 — metadata-only applied globally to the 61 cover-backed records.**
   This state's legibility depends on its rarity. Once, an empty mount reads as a
   decision; 61 times it reads as a broken site — and the browse grids are exactly
   where cover density lives. E-001 established the covers sample no artwork
   pixels, so C3 trades a labelled, honest cover for a field of empty frames and
   buys no accuracy. If the owner selects it I will build it; the objection
   belongs in the record first.
2. **Any withholding shipped before REQ-P1 lands.** Sequence, not preference: the
   leak is live until the helper exists.
3. **A site-default `og:image` for a withheld record.**
4. **Broken-image, spinner, "coming soon" or grey-placeholder treatments.**
5. **A4/B4 rendered as a reader-facing badge.** A dated internal exception is a
   ledger entry, not furniture on the page.

## 7. Observable acceptance criteria

1. **AC-1** `#/artwork/<withheld>` renders zero `<canvas>`.
2. **AC-2** That id produces zero `<canvas>` and zero `<img>` at all 10 sites.
3. **AC-3** Its `src`, if present in data, appears nowhere in
   `document.body.innerHTML` on the artwork, artist, list, museum, arc and index
   routes — 2246/2248 included. Zero hits.
4. **AC-4** Zero renderability tests in `js/app.js` outside `renderableImage()`
   (baseline 20 → 0).
5. **AC-5** No image on the record's **artist page** — E-007's failure.
6. **AC-6** `p/artwork/<id>.html` has no `og:image`/`twitter:image`, carries
   `twitter:card: summary`, re-emitted in the same commit.
7. **AC-7** Absent from the Painting of the Day pool, `deckPool()`, museum
   collages, and `#/credits`.
8. **AC-8** Zero `role="img"` in the withheld hero; the card/rail link's computed
   accessible name ends with the ◆ phrase; zero new axe violations; tab-stop count
   equals an image-bearing record's.
9. **AC-9** Hero height within ±8px of today's 340px; no horizontal scroll at 375,
   768, 1440; a withheld card measures the same height as its neighbours.
10. **AC-10** Screenshots, desktop and mobile, **both themes**: withheld hero; a
    grid with one withheld card among image-bearing ones; a rail.
11. **AC-11** Shown the withheld hero beside the two cover heroes, a reader picks
    out the withheld one without reading the labels.
12. **AC-12** `tools/validate.jxa.js` exits 0; suite green.
13. **AC-13** Negative controls: drop `R` at 2246 → AC-3 fails; withhold a record
    while keeping `src` → AC-3 still passes; un-mark it → every surface returns to
    today's output byte-for-byte.

## Open questions

1. **OQ-1 (OP-RIGHTS)** Ratify the ◆ strings and define the record-scoped token.
2. **OQ-2 (OP-CONTENT)** `w.dims` is missing on part of the catalog; the
   proportional mount degrades to 16/10 there.
3. **OQ-3** Registry unification versus a second gate — spec-level, either way
   satisfying REQ-P3.
4. **OQ-4** Does a withheld record keep Admire and its passport entry? My
   recommendation: yes. A reader can admire a work they know.
