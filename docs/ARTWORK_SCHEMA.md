# Artwork Page Schema

*v1 — July 2026. Artworks become first-class objects: the substrate of Admire, lists, the deck, the daily painting, and everything in Phases 1.5–4. Companion to `ADMIRE_SPEC.md` (verbs & coords), `TASTE_MATH.md` (engine), `STYLE_GUIDE.md` (§4.4 copy budgets). This document is the contract for implementation.*

---

## 1. Principles

1. **An artwork is a record, a page, and a card** — one object, three renderings. Every field below states which renderings consume it.
2. **Admire-ready from day one.** The page ships with `Admire · Seen in person · Save for later`, wired to the Taste Passport's localStorage object (`pigment.taste.v1`) immediately — the Persona arrives in 1.5, but the signals start accruing in Phase 1.
3. **Tiered honestly.** Tier 1 records power full pages; Tier 2 records exist only to make cards, list entries and links truthful. No thin "full pages."
4. **Authored where it matters, inherited where it doesn't, enriched where machines can.** Every field is marked A (authored), I (inherited), E (enriched from Wikidata/Commons), or D (derived at build/runtime).

---

## 2. Identity

- **id**: kebab-case slug of the common English title: `the-starry-night`, `las-meninas`.
- Generic titles get artist disambiguation: `self-portrait-1889-van-gogh`, `water-lilies-setting-sun-monet`. Rule: append `-{artist shortname}` (and year if still colliding). Validator enforces global uniqueness.
- Slugs are permanent once shipped (they become URLs). Renames require a redirect entry in `SLUG_ALIASES`.

## 3. The record

```js
{
  id: "the-calling-of-saint-matthew",
  tier: 1,                                  // 1 = full page · 2 = card/stub
  title: "The Calling of Saint Matthew",
  artistId: "caravaggio",                   // must exist in ARTISTS
  year: { display: "1599–1600", sort: 1599 },

  movements: ["baroque"],                   // I: artist's primary, overridable
  techniques: ["oil-painting","tenebrism"], // I: subset of artist's, overridable
  nation: "italy",                          // I: artist's, overridable (work-specific culture)

  museum: {                                 // E/A — future museumId links here
    id: null,                               // reserved: "san-luigi-dei-francesi" | museums section later
    name: "Contarelli Chapel, San Luigi dei Francesi",
    city: "Rome"
  },
  dims: "322 × 340 cm",                     // E: Wikidata P2048×P2049, optional

  image: {                                  // from the existing artworks pipeline
    src: "https://upload.wikimedia.org/...500px-...jpg",   // Commons bucket URL only
    page: "https://en.wikipedia.org/wiki/The_Calling_of_Saint_Matthew",
    status: "pd"                            // "pd" | "generative" | "none"
  },

  coords: { F: -85, D: 92, E: -30, C: -20, M: 55 },  // TASTE_MATH §1; Tier 1 = explicit
  coordsSource: "override",                 // "inherited" | "override"

  description: "…",                         // A: 50–80 words, STYLE_GUIDE §4.4
  notice: [                                 // A: exactly 3 bullets, visual, ≤ 12 words
    "Christ's hand quotes Adam's from the Sistine ceiling",
    "The light enters where no window exists",
    "Which figure is Matthew? Scholars still point at two"
  ],

  tags: ["chiaroscuro","interior","sacred","group-scene","night"],  // §5 vocabulary
  related: ["judith-beheading-holofernes","the-supper-at-emmaus"],  // A (Tier 1, 0–4) else D by distance
  deckBuckets: ["D+","F-"]                  // D: derived from coords at build (TASTE_MATH §6 pools)
}
```

**Field consumption map**

| Rendering | Uses |
|---|---|
| Page | everything |
| Card (lists, rails, deck) | id, title, artistId, year.display, image, tags |
| Engine | coords, tags, deckBuckets, tier |
| Share/OG | title, artistId, year.display, image.src |

## 4. Requirements by tier

| Field | Tier 1 | Tier 2 |
|---|---|---|
| id, title, artistId, year | required | required |
| image | required (`pd` or explicit `generative`) | required (may be `none` → generative card) |
| coords | **explicit** (validator-enforced) | inherited allowed |
| description + notice | required, on-budget | absent (card only) |
| museum, dims | required-if-known | optional |
| tags | ≥ 3 | ≥ 1 |
| related | authored 2–4 | derived |

## 5. Tag vocabulary (seed, controlled)

One flat list, grouped for humans; additions require a PR to this file — no free-typing.

- **Subject:** portrait · self-portrait · interior · landscape · seascape · still-life · nude · sacred · mythological · historical · everyday-life · animal · group-scene
- **Mood:** quiet · tender · unsettling · ecstatic · lonely · theatrical · playful · mourning
- **Light & palette:** nocturne · candlelit · golden · fog · storm · blue · red · pastel · monochrome
- **Form:** pattern · geometry · gesture · miniature-scale · monumental-scale · flatness · texture
- **Use (product):** october-mood · rain-mood · would-hang · fever-dream *(list-fuel tags; editorial team only)*

Tags power: list assembly, mood search (medium backlog), deck bucket seasoning, "similar artworks" tie-breaking, Wrapped stats later.

## 6. Page anatomy — route `#/artwork/{id}`

Order fixed; sections marked with their phase.

1. **Hero** *(P1)* — the image, full-bleed, click = lightbox (existing component). `status:"generative"` renders the artist-style canvas seeded by artwork id, honestly captioned.
2. **Identity line** *(P1)* — Title · artist link · year · chips: movement / technique / nation / museum-name (chip becomes a link when Museums land).
3. **Action bar** *(P1, passport-wired)* — **Admire** (primary) · Seen in person · Save for later. States read/write `pigment.taste.v1`. Graceful first-run: no passport → create skeleton on first action.
4. **Description** *(P1)* — the 50–80 words.
5. **What to notice** *(P1)* — 3 bullets.
6. **Provenance line** *(P1)* — dims · museum, city · "image via Wikimedia Commons" source link.
7. **Rails** *(P1)* — *More by {artist}* (catalog, byArtist index) · *Near it in the atlas* (top-4 by TASTE_MATH weighted distance, excluding same artist) · *Go next* (artist page, movement page).
8. **Appears in lists** *(P1 once lists exist)* — reverse index.
9. **Admired by N people** *(Phase 2+, field reserved)*.

Empty states and captions follow STYLE_GUIDE §4.10.

## 7. Storage & code plan

- **New data files:** `js/catalog-1.js` … `js/catalog-n.js` → `window.CATALOG` (array of records), mirroring the `artists-*.js` pattern; ~40 records/file.
- **Relationship to `js/artworks.js` (image map):** during migration the bake script folds `img/page` into catalog records; `window.ARTWORKS` remains the source for *non-catalog* works shown on artist pages. End state: catalog wins where a record exists; artist-page works arrays gain optional `id:` refs to link into the catalog.
- **Derived at load (app.js):** `CATALOG_BY_ID`, `CATALOG_BY_ARTIST`, `CATALOG_BY_TAG` — one pass, no build step needed.
- **Bake tools:** `tools/build_catalog.py` (merge images + Wikidata enrichment + deckBucket derivation), reusing the audit's PINNED/override pattern and its rate-limit lessons (≥0.25 s, never delete on timeout).
- **Wikidata enrichment (E fields):** by Commons file → P276/P195 (location/collection), P2048×P2049 (dims), P571 (inception). Misses stay blank — blank beats wrong.

## 8. Tier 1 selection (the one-pool rule)

An artwork enters Tier 1 iff it belongs to at least one of:
1. an editorial list (first 12 lists),
2. the *essential works* of a Tier 1 artist (~40 artists × 4),
3. the first ~90 days of the Painting-of-the-Day schedule,
4. the onboarding deck pool (deck constraints in ADMIRE_SPEC §6.2 override everything — deck works must be Tier 1 by definition).

Target: **~160 at launch, ceiling 250.** Every Tier 1 page therefore ships with ≥ 2 inbound links — no orphans, by construction.

## 9. Validator extensions (JXA, build-blocking)

- catalog ids unique, kebab-case; `artistId`/`movements`/`techniques`/`nation` resolve
- Tier 1: explicit `coords` (integers −100…+100), description present and 30–110 words, exactly 3 `notice` bullets, ≥ 3 tags from the vocabulary, image not `none`
- `related` ids resolve; no self-reference; `image.src` contains `/wikipedia/commons/` when `status:"pd"`
- warn: Tier 1 record with zero inbound links (list/essential/daily/deck)

## 10. Open questions

1. Do Tier 2 records get thin pages (identity + image + actions only) or cards-only with no route? *(Lean: thin pages — admiring from a real URL beats a dead-end card.)*
2. `would-hang` etc. as editorial tags vs deriving them later from actual admire data — keep or drop the "Use" tag group?
3. Museum `id` reservation: adopt museum slugs now (empty section) or wait for the Museums template deliverable?
