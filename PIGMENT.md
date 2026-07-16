# Pigment: Product Vision and Builder Context

Last updated: 2026-07-16

This is the primary orientation document for humans and language models working on Pigment. It explains what the product is trying to become, what already exists, which decisions are durable, and which ideas are still provisional.

This document is a compass, not a frozen specification. Preserve the north star and product principles. Challenge or revise individual features when evidence, usability, content quality, copyright, or technical constraints justify it.

For implementation-level contracts, also read:

- `docs/STYLE_GUIDE.md` - editorial voice and content budgets
- `docs/ADMIRE_SPEC.md` - the core verb, onboarding, Personas, and Taste Passport
- `docs/TASTE_MATH.md` - the taste-vector and recommendation model
- `docs/ARTWORK_SCHEMA.md` - artwork, venue, and editorial-list records

## 1. The Product in One Sentence

> Pigment is a social atlas where people discover, understand, and express their taste in art.

The north star is:

> Pigment helps people discover, understand, and express their taste in art.

Useful product lines include:

- Find your place in the history of art.
- Map your taste in art.
- Discover the art that feels like you.
- An atlas for the art you love, and the art you have not met yet.

Pigment combines four kinds of value:

1. The depth and connectedness of an art-history reference.
2. The identity, diary, and list culture of products such as Letterboxd.
3. A visual atlas of artworks, artists, movements, techniques, eras, nations, and museums.
4. A future learning and community layer built on the same underlying graph.

It is not merely a database with attractive cards. The atlas is the foundation for a personal relationship with art.

## 2. What Pigment Is Not

Do not steer Pigment toward any of these simplified identities:

- A dry encyclopedia or museum wiki
- A generic social network with art-themed posts
- A shallow trivia or QuizUp clone
- A dating app
- A meme-only art account
- A monetization-first product
- A feed that exists before users have meaningful taste profiles

Social features should emerge from taste, curation, learning, and physical encounters with art. They should not be added simply because social products usually contain them.

## 3. The Core Product Loop

The concise emotional loop is:

> Discover -> Admire -> Map -> Become -> Share

- **Discover:** encounter artworks, artists, museums, movements, lists, routes, and historical connections.
- **Admire:** record which artworks genuinely speak to you.
- **Map:** Pigment locates the shape and multiple possible islands of your taste.
- **Become:** a Taste Passport, palette, and provisional Persona turn reactions into identity.
- **Share:** send a result, list, profile, museum log, or discovery outward.

The broader mature-product loop is:

> Discover -> Save -> Reflect -> Compare -> Learn -> Share

This broader loop adds notes, reviews, lists, user comparison, guided routes, quizzes, and mastery. The shorter loop is the immediate product experience; the broader loop is the long-term platform.

## 4. The Art-Native Verb

Pigment users do not simply like art. They **Admire** it.

Admire is the core taste signal and currently applies to artworks. It is warm, positive, and specific to the domain. Taste is inferred from *which artworks* a person admires, not from a collection of differently weighted reaction verbs.

Current product language:

| Generic language | Pigment language |
| --- | --- |
| Like | Admire |
| Liked artworks | Admirations |
| User taste profile | Taste Passport |
| Profile colors | Palette |
| User type | Pigment Persona |
| Recommendations | Go next / You may admire |
| Saved items | Saved for later |
| Physical encounter | Seen in person |

Important distinctions:

- **Admire** means the work belongs to the user's taste.
- **Seen in person** is a factual log, independent of admiration.
- **Save for later** means interest without committing a taste signal.
- A pass during onboarding is silence, not dislike.
- V1 is positive-only. Negative taste signals are reserved for later and must not be introduced casually.

## 5. Product Character

Pigment should feel:

- Intelligent
- Aesthetic
- Playful
- Slightly obsessive
- Poetic but usable
- Nerdy but not academic
- Social but not shallow
- Educational but not school-like

The voice is a well-read friend who notices details, has opinions, and wants the visitor to keep looking. It should never sound like an auction catalogue, a tourist brochure, a generic textbook, or horoscope copy.

Core writing behavior:

- Explain what the eye can actually find.
- State why a work or artist matters, not merely that they are important.
- Prefer concrete visual evidence over prestige language.
- Use humor sparingly and precisely.
- Be honest about uncertainty, disputed attribution, and legends.
- Avoid invented facts and fake certainty.
- Make every page offer a meaningful next step.

`docs/STYLE_GUIDE.md` is authoritative for tone and content budgets.

## 6. The Atlas as a Connected System

Pigment's objects should never feel like isolated records. Each object is an entrance into the wider atlas.

Core object types:

- Artist
- Artwork
- Movement
- Technique
- Era
- Nation
- Museum or physical venue
- Editorial list
- Persona
- Palette
- Taste Passport
- Later: user, route, quiz, review, title, club, and museum visit

Expected cross-links include:

- Artwork -> artist, movement, technique, nation, museum, related works, editorial lists
- Artist -> essential works, career arc, influences, movement, technique, era, nation, museums, go-next recommendations
- Museum -> works, represented artists, city/country, kindred museums, future one-hour route
- List -> canonical artworks, artists, movements, moods, related lists
- Movement -> desire, visual traits, reaction against, essential artists and works, before/after branches
- Taste Passport -> admired works, taste coordinates, Personas, discovery rings, artists, lists, and later museums/routes

Stable IDs and slugs are product infrastructure. Once shipped, artwork, artist, movement, list, and venue IDs should not be renamed without an alias or migration plan.

## 7. Content Depth Strategy

Build depth in rings rather than spreading shallow content across everything.

### Tier 1 artists

These are exhibition-like profiles. A visitor should feel they have entered the first rooms of a retrospective or opened the first chapter of a serious book.

They include:

- Why the artist matters
- Concrete visual traits
- A career/life arc with turning points
- Up to roughly ten or more critical works where appropriate
- Works linked from the narrative
- Influences and artistic neighborhood
- Go-next recommendations
- Taste coordinates

### Tier 2 and Tier 3 artists

These remain useful atlas entries with correct taxonomy and clean content, but do not pretend to have exhibition depth.

### Tier 1 artworks

These are full, Admire-ready pages with authored descriptions, three visual observations, provenance, coordinates, source data, related works, list links, and museum links.

### Tier 2 artworks

Every admirable artwork still gets a thin canonical page and stable URL. Promotion to Tier 1 is additive; the URL never changes.

### Editorial lists

Lists establish Pigment's voice before user-generated lists exist. Their titles should be emotionally legible and shareable, not taxonomic. Examples include fear, weather, rooms, fabric, loneliness, night, theft, repetition, and artworks from an artist's final year.

## 8. Taste Atlas and Taste Passport

Every eligible artwork has a coordinate vector in a shared taste space. The launch axes use the scale `-100 ... +100`:

| Key | Negative pole | Positive pole |
| --- | --- | --- |
| F | Figurative | Abstract |
| D | Calm | Dramatic |
| E | Classical | Experimental |
| C | Sensual | Conceptual |
| M | Intimate | Monumental |

The first visible map uses `F x D` because it is immediately understandable. The remaining axes appear as secondary signals.

The basic model is a shrunken centroid:

```text
user taste = (sum of admired artwork vectors + decaying quiz prior) / total signal
```

The quiz prior currently has the equivalent weight of six artworks and decays naturally as real admirations accumulate. A deterministic two-cluster test can preserve two genuine taste islands instead of flattening contradictory taste into an unhelpful midpoint.

User-facing language stays simple:

- Your admirations leave coordinates.
- Pigment finds the center of gravity of your taste.
- Your map is still forming.
- Pigment has found a second taste island.

Do not expose implementation jargon such as k-means, Mahalanobis distance, posterior variance, or graph embeddings unless writing technical documentation.

### Taste Passport

The accountless Taste Passport lives at:

```text
localStorage key: pigment.taste.v1
```

It stores versioned, migration-ready fields for:

- Admirations
- Skipped onboarding cards
- Seen-in-person works
- Saved works
- Palette
- Quiz answers and prior
- Taste vector and clusters
- Persona candidates and adopted Persona
- Confidence milestones

The Passport is portable through JSON export and encoded import/share URLs. Future account creation should import the Passport rather than reset the user.

## 9. Onboarding Principle

The rule is:

> Provisional fast, refined forever.

The first result should take under four minutes:

1. Pick four art-named tones.
2. Admire or pass through sixteen artworks.
3. Answer five philosophy questions.
4. Receive a provisional taste map and three Persona candidates.
5. Adopt one or decide later.
6. Continue into matched artists and an editorial list.

Personas are expressive summaries, not diagnoses. Users retain agency: adopt, reject, hide, retake, or change later. Adopted Personas must never silently switch.

All current Persona names are provisional. Their coordinate prototypes and rules are more durable than their labels.

Copyright creates a known onboarding bias toward older public-domain artworks. Correct this through balanced public-domain selection, movements, philosophy questions, generative style probes, and eventually licensed or otherwise displayable modern material. Never infer that a user dislikes modern art merely because modern images could not legally appear.

## 10. Museums and Physical Art

Museums connect digital taste to the physical world. They are not decorative wiki pages.

Long-term museum value includes:

- Collection and artist discovery
- A curated "If you only have one hour" route
- Museum matching from the user's taste
- Wishlists and travel planning
- Seen-in-person artwork logs
- Museum visit diaries
- City art guides
- Future museum-friend or group experiences

The venue registry also includes churches, chapels, palaces, and sites because artworks live outside museums. `private-collection`, `lost`, and `unknown` are valid sentinel locations.

## 11. Phased Product Strategy

Do not build the full social network at once.

### Phase 1: Atlas 2.0

Goal: make the atlas valuable, deep, emotionally engaging, and easy to continue exploring.

Includes:

- Repositioned homepage
- Canonical artwork pages
- Exhibition-quality Tier 1 artist profiles
- Painting of the Day
- Editorial lists
- Museum pages
- Improved movement, technique, era, and nation pages
- Better information architecture, metadata, SEO, and share surfaces

### Phase 1.5: Accountless Taste Prototype

Goal: prove that people enjoy discovering and expressing their art taste before building accounts.

Includes:

- Admire and other Passport actions in localStorage
- Fast onboarding
- Palette picker
- Taste Map
- Provisional Personas
- Discovery rings
- Passport export/import and share links

### Phase 2: Profiles and Real Identity

Goal: turn the local Passport into a persistent personal gallery.

Includes:

- Accounts and privacy settings
- Public profiles
- Favorite artworks, artists, movements, and museums
- User palettes and Personas
- User-created lists
- Ratings, reviews, and reflections
- Persistent museum logs

Do not add direct messaging, dating, heavy notifications, or generic posting at the start of Phase 2.

### Phase 3: Learning and Mastery

Goal: teach through the atlas graph without becoming shallow trivia.

Includes:

- Guided routes
- Visual recognition and comparison quizzes
- Timeline, influence, technique, museum, and geography questions
- Explanations after answers
- Artist, movement, technique, era, and museum mastery
- Daily quizzes and route completion badges

### Phase 4: Community and Social Discovery

Goal: add social behavior after users have meaningful taste profiles and activity.

Includes:

- Following
- Activity based on Admirations, lists, reviews, routes, and museum visits
- Comments on lists and reviews
- Taste comparison
- Clubs and group challenges
- Art-friend and museum-buddy discovery
- Moderation, reporting, blocking, privacy, and anti-harassment systems before deeper social discovery

Dating may never be added. It is not part of the core promise.

## 12. Current Implementation Snapshot

The numbers below are a dated snapshot, not permanent requirements. Run the validator for current counts.

As of 2026-07-16, `main` contains:

- 235 artists
- 314 canonical artworks
- 73 Tier 1 artworks
- 36 Tier 1 exhibition artist profiles, all with career arcs
- 74 movements
- 39 techniques
- 8 eras, from the 14th century to today
- 37 nations
- 115 registered venues
- 103 museum notes/pages represented in the current museum index
- 12 editorial lists
- 15 provisional Personas
- 215 influence relationships
- 73 eligible Painting-of-the-Day works

Implemented routes include:

```text
#/                         homepage
#/artists                  artist index
#/artist/{id}              artist page
#/artwork/{id}             artwork page
#/daily                    Painting of the Day
#/lists                    editorial list index
#/list/{id}                editorial list page
#/museums                  museum index
#/museum/{id}              museum page
#/explore                  timeline and influence hub
#/timeline                 grand timeline
#/influences               influence constellation
#/movements                movement index/tree
#/movement/{id}            movement page
#/techniques               technique index/tree
#/technique/{id}           technique page
#/eras and #/era/{id}      era pages
#/nations and #/nation/{id} nation pages and maps
#/palette                  taste onboarding
#/taste                    Taste Passport and discovery rings
#/passport/{payload}       Passport import
```

The live site is:

```text
https://ardagemci.github.io/painters-atlas/
```

## 13. Technical Architecture

Pigment is currently a zero-dependency static application:

- Plain HTML, CSS, and JavaScript
- Script-tag-loaded global data registries
- Hash router
- Canvas-based generative artist/movement covers
- No backend
- No account system
- localStorage Taste Passport
- GitHub Pages deployment

Important data files:

| File | Responsibility |
| --- | --- |
| `js/artists-*.js` | Artist records |
| `js/catalog-*.js` | Canonical artwork records |
| `js/artworks.js` | Public-domain image map for artist-page works |
| `js/taxonomy.js` | Movements, techniques, eras, nations |
| `js/influences.js` | Artist relationship graph |
| `js/venues.js` | Stable physical venue registry |
| `js/museums-1.js` | Museum copy and photography |
| `js/lists-1.js` | Editorial list records |
| `js/personas.js` | Tones, questions, and Persona prototypes |
| `js/tier1-artists.js` | Rich artist overlays and career arcs |
| `js/app.js` | Router, rendering, interactions, taste engine, generative covers |
| `css/styles.css` | Themes, layouts, animation, responsive behavior |
| `tools/validate.jxa.js` | Build-blocking data and content validation |

This Mac does not currently provide Node.js. Validate with:

```sh
osascript -l JavaScript tools/validate.jxa.js
```

Run locally with:

```sh
python3 -m http.server 8421 -d /Users/ardagemci/Claude/painters-atlas
```

## 14. Artwork and Copyright Rules

Artwork accuracy is a product requirement, not a cosmetic detail.

- Prefer public-domain images hosted on Wikimedia Commons.
- The image must depict the exact artwork, not a museum room, building, souvenir, detail crop, reproduction object, or different version unless explicitly labeled.
- Full compositions are preferred over detail crops.
- Wikimedia thumbnail widths known to work include 330, 500, 960, and 1280 pixels.
- Do not classify a URL as dead because of a timeout, 429, or transient server error.
- Hand-corrected images must also be pinned in `tools/audit_artworks.py` so later audits do not replace them.
- Copyrighted works may use honest generative covers or unavailable-image states. Never present generated imagery as the real artwork.
- Keep attribution and source links close to the image record.

## 15. Known Gaps and Provisional Decisions

An LLM should not silently treat these as settled:

1. **Persona names are placeholders.** The prototypes may survive; labels and copy may change.
2. **The onboarding deck is not fully adaptive yet.** The current implementation chooses the full deck upfront, while `docs/TASTE_MATH.md` describes later choices reacting to earlier responses.
3. **The onboarding pool has coverage warnings.** It currently lacks a calm-abstract quadrant anchor and has too few strongly classical works. Fix content coverage before drawing conclusions from Persona quality.
4. **Museum pages need curated one-hour routes.** The current collection grid does not yet fulfill the Style Guide's strongest museum-page promise.
5. **Editorial list word budgets conflict.** Reconcile `STYLE_GUIDE.md` and `ARTWORK_SCHEMA.md` before enforcing a final contract.
6. **Static metadata is behind the product.** The HTML description still understates the chronology and taste/museum/list direction.
7. **Instrumentation is undecided.** The product cannot yet answer how many people finish onboarding or share a result.
8. **Share graphics and real SEO pages are incomplete.** Hash routes alone are weak for search and link previews.
9. **Movement, technique, era, and nation upgrades remain uneven.** The taxonomy is broad; emotional and educational depth is not yet uniform.
10. **The visible role of the fifth axis is unresolved.** `M` is stored, while the public map currently emphasizes `F x D`.

When implementation and documentation disagree, do not quietly choose one. Surface the mismatch, decide which behavior serves the product, then update both code and docs.

## 16. Current Strategic Priorities

The most useful next work is not simply "more data." Prioritize quality and product coherence:

1. Repair onboarding coordinate coverage and either implement true adaptivity or revise the claim.
2. Test the complete onboarding flow with real users before expanding the Persona set.
3. Resolve Persona names and descriptions after observing result quality.
4. Add museum one-hour routes for the strongest museums.
5. Upgrade the top movement and technique pages into beginner-friendly explainers.
6. Reconcile docs, metadata, navigation, and product copy with the current taste-atlas direction.
7. Add share cards and a realistic SEO/prerender plan.
8. Add privacy-friendly onboarding/share instrumentation only after an explicit product decision.
9. Continue Tier 1 depth selectively where it creates meaningful discovery paths.

Do not jump to accounts or community merely because Phase 1.5 exists. First prove that Discover -> Admire -> Map -> Become is enjoyable and produces results people recognize and want to share.

## 17. Rules for LLM Contributors

Before changing the project:

1. Read this file and the relevant document in `docs/`.
2. Inspect the current code and data rather than trusting old counts or summaries.
3. Check `git status` and recent commits. Other agents may be working in the same repository.
4. Treat `main` as the shared source of truth.
5. Preserve unrelated user changes and do not revert work you did not create.

While implementing:

1. Use existing patterns and data registries before adding abstractions.
2. Keep changes scoped to one coherent product slice.
3. Preserve permanent IDs and source attribution.
4. Reuse canonical artwork records instead of duplicating artwork data.
5. Follow the content voice and word budgets.
6. Prefer exact, sourced facts over impressive-sounding prose.
7. Keep dark and light themes working.
8. Check desktop and mobile layouts; text and controls must not overlap.
9. Do not add future-phase social features without a product decision.
10. Do not overfit the product to a provisional Persona name or a temporary data count.

Before declaring completion:

1. Run `osascript -l JavaScript tools/validate.jxa.js`.
2. Run `git diff --check`.
3. Exercise the changed route in a real browser.
4. Check for missing or incorrect images and browser errors.
5. Test the adjacent behavior that should not have changed.
6. Update the relevant documentation when a contract changes.
7. Report remaining warnings or untested surfaces honestly.

## 18. Definition of a Good Pigment Change

A good change does at least one of these:

- Helps a visitor understand why an artwork, artist, movement, or museum matters.
- Gives the visitor a meaningful next place to go.
- Makes Admire and the Taste Passport feel more expressive or trustworthy.
- Strengthens the historical graph without flattening cultural complexity.
- Improves visual inspection of the actual art.
- Makes the product more shareable without making it shallow.
- Reduces a known content, copyright, accessibility, or data-integrity risk.

A change is not good merely because it adds more cards, more entities, more animation, more statistics, or more social controls.

The standard is:

> Does this help someone discover art, understand what they are seeing, and recognize something about their own taste?

If the answer is no, it probably does not belong in Pigment yet.
