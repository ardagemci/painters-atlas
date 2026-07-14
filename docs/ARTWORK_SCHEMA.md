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

  museum: {                                 // E/A — venue registry reference (§5b)
    id: "san-luigi-dei-francesi",           // stable slug from the venue registry, or a sentinel
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

**Decision (Arda, July 2026): Tier 2 artworks get thin canonical pages — every admirable artwork has a real URL.** A thin page renders hero, identity line, action bar, provenance and the derived rails; description/notice are replaced by a single styled empty-state line (STYLE_GUIDE §4.10). Tier 2 → Tier 1 promotion is purely additive (write description + notice + coords override); the URL never changes.

| Field | Tier 1 (full page) | Tier 2 (thin page) |
|---|---|---|
| id, title, artistId, year | required | required |
| image | required (`pd` or explicit `generative`) | required (may be `none` → generative hero) |
| coords | **explicit** (validator-enforced) | inherited allowed |
| description + notice | required, on-budget | absent → empty-state line |
| museum, dims | required-if-known | optional |
| tags | ≥ 3 | ≥ 1 |
| related | authored 2–4 | derived |

## 5. Tag vocabulary (seed, controlled)

One flat list, grouped for humans; additions require a PR to this file — no free-typing.

- **Subject:** portrait · self-portrait · interior · landscape · seascape · still-life · nude · sacred · mythological · historical · everyday-life · animal · group-scene
- **Mood:** quiet · tender · unsettling · ecstatic · lonely · theatrical · playful · mourning
- **Light & palette:** nocturne · candlelit · golden · fog · storm · blue · red · pastel · monochrome
- **Form:** pattern · geometry · gesture · miniature-scale · monumental-scale · flatness · texture
- **Use (product):** october-mood · rain-mood · would-hang · fever-dream *(list-fuel tags)*

**Decision (Arda, July 2026): list-fuel tags stay.** They power lists, onboarding, Personas and early recommendations before any user data exists — they *are* the cold-start engine. Governance: (a) the Use group is **editorial-only, permanently** — user-generated tagging (Phase 4+, if ever) may never write into this namespace; (b) every new Use tag must power a concrete list or feature at the moment it's added; (c) once real admire data exists, these tags become testable hypotheses (do `would-hang` works out-admire the rest?) and are pruned by evidence.

Tags power: list assembly, mood search (medium backlog), deck bucket seasoning, "similar artworks" tie-breaking, Wrapped stats later.

## 5b. Venue registry (museum slugs, reserved now)

**Decision (Arda, July 2026): museum slugs/IDs are reserved immediately** — artwork identity, future museum pages, seen-in-person logs and museum matching all depend on stable references. The registry is a **venue registry, not strictly museums**: our artworks live in churches, chapels and palaces too, and "seen in person" applies to the Sistine Chapel as much as to MoMA.

- Entry shape: `{ id, name, city, country, type }` where `type: "museum" | "church" | "palace" | "site"`.
- Slug convention: kebab-case common English short name — `louvre`, `musee-dorsay`, `prado`, `uffizi`, `rijksmuseum`, `met`, `moma`, `mauritshuis`, `tretyakov`, `orangerie`, `belvedere`, `neue-galerie`, `reina-sofia`, `pera-museum`, `istanbul-modern`, `sakip-sabanci`, `phillips-collection`, `art-institute-chicago`, `national-gallery-london`, `van-gogh-museum`, `hermitage`, `vatican-museums`, `munch-museum`, `nasjonalmuseet-oslo`, `alte-pinakothek`, `kunsthistorisches`, `galleria-borghese`, `centre-pompidou`, `tate-modern`, `national-gallery-dc`, `mfa-boston`, `getty` … plus non-museum venues: `sistine-chapel`, `scrovegni-chapel`, `san-luigi-dei-francesi`, `santa-maria-delle-grazie`, `st-bavo-cathedral`, `museo-civico-sansepolcro`.
- **Sentinel ids** (always valid): `private-collection`, `lost` (e.g. The Stone Breakers, destroyed 1945), `unknown`.
- Registry lives in `js/venues.js` (`window.VENUES`) from the first catalog commit; museum *pages* arrive with the Museums deliverable, but references are stable from day one. Validator: every `museum.id` must resolve to the registry or a sentinel; `null` is allowed only for Tier 2.
- Registry additions are cheap and unreviewed; **slug renames are forbidden** (same alias rule as artwork slugs).

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

## 10. Resolved decisions (Arda, July 2026)

1. **Tier 2 artworks get thin canonical pages** — every admirable artwork needs a real URL (§4).
2. **Editorial list-fuel tags stay** — they power lists, onboarding, Personas and early recommendations before user data exists (§5, with governance rules).
3. **Museum slugs/IDs reserved now** — via the venue registry (§5b), because artwork identity, museum pages, seen-in-person logs and museum matching all depend on stable references.

## 11. Editorial lists (v1 — July 2026)

Lists live in `js/lists-1.js` as `window.EDITORIAL_LISTS`. A list is `{ id, title ≤64, lede 15–60 words, cover (artwork id, must be in works), featured (homepage flag), works: [{ id: canonical artwork id, note ≤120 chars }] }`. Lists **reuse canonical artwork pages** — never duplicate artwork data. Works may appear in any number of lists; artwork pages render reverse links ("In lists"). Routes: `#/lists`, `#/list/{id}`. List ids are permanent once shipped, like artwork and venue slugs. Validator enforces all budgets.
