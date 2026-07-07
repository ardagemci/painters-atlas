# The Admire Spec

*v1 — July 2026. Defines Pigment's core verb, the taste-coordinate system, the onboarding test, Persona assignment, and the taste passport. This is the engine document for Phase 1.5; Phase 1 pages must be built admire-ready against this spec.*

**Decisions already made (Arda, July 2026):** the verb is **Admire**; taste dimensions are computed from *which* artworks a user admires plus the entry quiz (not from per-verb weights); Persona unlock must be fast; the passport import/export mechanism is adopted; all Persona names are placeholders.

---

## 1. Principles

1. **One verb.** Admire is to Pigment what *watched* is to Letterboxd — warm, art-native, unambiguous.
2. **Signal from choice, not from button variety.** Your taste = which artworks you admire. Every artwork carries coordinates; you are the centroid of what you love.
3. **Positive-only in v1.** No dislikes at launch. One contrast signal (`notForMe`) is *reserved in the schema* for later (candidate surface: Painting of the Day).
4. **Fast provisional, refined forever.** A Persona arrives in minutes at onboarding; depth is a progression, not a gate.
5. **Portable by design.** All taste state lives in one versioned object (the passport) whose field names are the future account schema. Phase 2 signup = import passport.

---

## 2. The verb

### 2.1 `admire`
- **Applies to artworks only** (v1). Artists, movements and museums get *favorites* in Phase 2 — a different, curatorial gesture. Keeping admire artwork-pure keeps the taste signal clean.
- Toggle; idempotent; timestamped; un-admiring removes the signal entirely.
- Surfaces: artwork page (primary button), artwork cards in lists, Painting of the Day, onboarding deck.
- Copy: button reads **Admire** / **Admired ✓**. Counts read *"Admired by 214 people"* (Phase 2+). Profile section: **Admirations**.

### 2.2 Log toggles (records, not opinions — visually separate from Admire)
- **`seen`** — *Seen in person.* Timestamped; optional `museumId` later. The strongest art-native log verb; exists from the first artwork page, accountless.
- **`wantToSee`** — *Want to see in person.* The wishlist; later powers museum wishlists and city guides.
- Both fully independent of admire (you can have seen a work that leaves you cold — that's information too, someday).

---

## 3. Taste dimensions (v1)

Five axes, each scored **−1.00 … +1.00**. The fifth is stored from day one but may stay hidden in UI at launch.

| Key | − pole | + pole | What it measures |
|---|---|---|---|
| `F` | Figurative | Abstract | recognizable world ↔ non-representational form |
| `D` | Calm | Dramatic | quiet atmosphere ↔ intensity, tension, shadow |
| `E` | Classical | Experimental | tradition, craft, order ↔ rupture, risk, rule-breaking |
| `C` | Sensual | Conceptual | material/visual pleasure ↔ idea, critique, irony |
| `M` | Intimate | Monumental | private, domestic scale ↔ grand, sublime, public |

**Primary 2D map:** `F × D` (Figurative↔Abstract × Calm↔Dramatic). Everything else surfaces as secondary signals: *"Your position: Figurative + Dramatic. Secondary signals: sensual, classical, intimate."*

## 4. Coordinate assignment — score movements, not artists

Three inheritance levels; hand-judgment concentrated where it matters.

1. **Movements (74) are hand-scored** once, each getting a full 5-vector. This is the master data.
2. **Artists inherit**: weighted mean of their movements' vectors (primary movement ×2, others ×1). **Tier 1 artists (~50) get hand overrides** where inheritance lies (a painter can be their movement's calm exception).
3. **Artworks inherit from their artist**, with **per-work overrides for Tier 1 artworks** where the arc demands it — Goya's tapestry cartoons and his Black Paintings must not share a `D` value.

Worked examples (movement level, `{F, D, E, C, M}`):

| Movement | F | D | E | C | M |
|---|---|---|---|---|---|
| Impressionism | −0.5 | −0.4 | +0.1 | −0.7 | −0.3 |
| Baroque | −0.9 | +0.8 | −0.6 | −0.3 | +0.5 |
| Suprematism | +1.0 | −0.1 | +0.9 | +0.7 | −0.1 |
| Dutch Golden Age | −0.9 | −0.5 | −0.5 | −0.4 | −0.8 |
| Surrealism | −0.3 | +0.4 | +0.6 | +0.4 | −0.1 |
| Pop Art | −0.4 | +0.1 | +0.6 | +0.8 | +0.1 |

Storage: `coords` field on movement/artist/artwork objects; the JXA validator checks presence (Tier 1) and range (all).

## 5. User taste vector

**Position = shrunken centroid.**

```
userVector = ( Σ admiredArtwork.coords · w  +  k · quizPrior ) / ( Σ w + k )
```

- `w = 1.0` for real-artwork admirations; `w = 0.5` for weak-signal probes (generative style cards, movement cards — see §7).
- `quizPrior` = vector from onboarding questions (§6.3); `k = 6` (the quiz "weighs" six artworks). Bayesian shrinkage: quiz dominates at n=5, fades by n=50.
- No recency decay in v1 (`decay` field reserved).
- **Confidence tiers** (drive copy, not access): `sketch` (<12 signals) → `forming` (12–29) → `drawn` (30–74) → `varnished` (75+).
- **Dispersion matters:** record `variance` per axis. High overall variance is not noise — it's *eclecticism*, and it feeds General Personas (§8).

## 6. Onboarding — "Find your palette" (target: under 4 minutes)

Per Arda: practical, fast, provisional. No 30-minute ceremonies.

1. **Pick 4 tones** (~20 swatches with art-native names — Ultramarine, Caravaggio Black, Monet Fog, Icon Gold…). Seeds the profile palette + a whisper-weight prior (±0.1 nudges: dark/dramatic tones → +D, pastels → −D −C, golds → −E).
2. **The deck: admire-or-pass through 16 artworks**, swipe-speed UI. *Pass is not a dislike; it is silence.*
3. **5 philosophy questions**, single-tap answers.
4. **Reveal:** 2D map position + 3 Persona candidates → adopt one, or "decide later."
5. **Handoff:** 3 artists, 1 editorial list, 1 route (placeholder in 1.5) matched to the vector.

### 6.2 Deck composition rules (the copyright-skew defense)
Every deck must contain, from the Tier 1 artwork pool (great image + confident coords required):
- ≥3 works with `F > +0.3` (real abstraction exists pre-1956: Kandinsky, Malevich, Popova, Klee, af Klint)
- ≥3 pre-1700 · ≥3 19th-century · ≥3 early-modern
- ≥2 non-European (ink, miniature, ukiyo-e…)
- axis coverage: for each of the 5 axes, at least 2 works ≥ +0.4 and 2 works ≤ −0.4
- Post-1955 taste (Pop, AbEx, contemporary) is probed by §7 signals and questions — **never inferred as absent merely because it couldn't be shown.**

### 6.3 Question → prior mapping (launch five)
Each answer applies nudges of ±0.30 (±0.15 for soft options) to 1–2 axes:

| Question | Answer → nudge |
|---|---|
| Should art require visible skill? | mastery → −E · idea can matter more → +E, +C · emotional force → +D · challenges skill itself → +E |
| Does art need meaning? | depth/symbolism → +C · beauty is enough → −C · emerges later → +0.15 C · refuses meaning → +C, +E |
| Comfort or disturb? | comfort → −D · disturb → +D · both → +0.15 D · make me notice → +C |
| Explain the world or escape it? | explains → −F, +C · escapes → −C, −D · transforms → +E · destroys → +E, +D |
| Should art be beautiful? | deeply → −C · not necessarily → +0.15 C · strange/ugly beauty → +D · distrust easy beauty → +C, +E |

## 7. Weak-signal probes (modern-taste coverage)

- **Movement cards:** "Which of these worlds pulls you?" — movement palette + one-sentence description; admiring one = movement's vector at `w = 0.5`.
- **Generative style cards:** our own canvas painters as visual probes for unshowable styles; same weight, honestly labeled ("in the spirit of").
- These appear in onboarding only if deck responses show `F > 0` drift, and later ambiently ("calibrate your modern wing").

## 8. Persona assignment

- **Specific Persona** = prototype vector + optional signature condition (e.g., *[Dutch-interior persona]* ≈ `{−0.8, −0.5, −0.4, −0.4, −0.8}` + admired ≥2 Dutch Golden Age works).
- **General Persona** = dispersion/behavior rule, not position (variance above threshold → eclectic archetypes; wide era-range → time-traveler archetype).
- Candidates = 3 nearest prototypes by weighted distance (2D axes ×1.5, secondary ×1.0), with one General swapped in when its rule fires.
- User agency is absolute: adopt / reject all / choose manually / hide / retake. **Adopted Personas never auto-switch**; on milestone recomputes, drift produces an *offer* ("your map has drifted toward the quiet rooms — a new Persona is available").
- Launch set: 12–16. **All names placeholders pending Arda's pass.**

## 9. Palette

- 4 tones; source `chosen` (onboarding) or `generated` (mean hues of admired works' stored palettes — data already exists per artist/movement).
- Names are always art-native (pigment names + poetic names lists in the product notebook); never `#hex`, never "light blue."
- Rendered as profile gradient + four swatches; drives the share card background.

## 10. The Taste Passport (localStorage schema)

Key: `pigment.taste.v1` — one versioned JSON object. **Field names are the Phase 2 account schema.** Migration = import.

```json
{
  "version": 1,
  "createdAt": "2026-07-06T12:00:00Z",
  "updatedAt": "2026-07-06T12:00:00Z",
  "admirations": [ { "id": "the-starry-night", "at": "…" } ],
  "notForMe":   [],
  "seen":       [ { "id": "mona-lisa", "at": "…", "museumId": null } ],
  "wantToSee":  [ "las-meninas" ],
  "probes":     [ { "kind": "movement", "id": "pop-art", "at": "…" } ],
  "quiz":       { "answers": { "q1": "b" }, "prior": { "F": 0.15, "D": 0.3, "E": 0, "C": 0.3, "M": 0 }, "at": "…" },
  "palette":    { "tones": ["ultramarine", "caravaggio-black", "museum-cream", "dried-rose"], "source": "chosen" },
  "persona":    { "adopted": null, "candidates": [], "adoptedAt": null, "hidden": false },
  "tasteVector": { "F": -0.4, "D": 0.5, "E": -0.2, "C": -0.3, "M": 0.1, "n": 14, "variance": 0.18 },
  "milestones": { "onboarded": true, "confidence": "forming" }
}
```

- `tasteVector` is a cache — always recomputable from admirations + probes + quiz.
- **Export:** the object, JSON → base64url. Two forms: downloadable `pigment-passport.json` and a share/restore URL (`#/passport/<payload>`). Copy: *"Your taste passport — your eye, portable."*
- **Import:** union-merge admirations/seen/wantToSee by `(id, earliest at)`; newer scalar fields win; never silently drop.
- Size guard: 1,000 admirations ≈ 60 KB — far under localStorage limits. Warn at 80% quota anyway.

## 11. Share surfaces (contract with the SEO/share plan)

- Persona result: pre-generated PNG per Persona (≤16 files, generated once in-browser, committed) + result URL rendering name/palette/position.
- Artwork & list pages: the artwork image itself is the OG image. Artist pages: baked cover PNGs, Tier 1 first.

## 12. Instrumentation (the Phase 1.5 hypothesis needs one gauge)

Minimum: privacy-friendly counter (Plausible/GoatCounter class) or, at absolute minimum, share-button click logging. The question "do people finish onboarding and share the result?" must be answerable. **Decision owner: Arda.**

## 13. Open questions for Arda

1. Button microcopy: **Admire** vs **I admire this** vs Turkish-flavored alternative?
2. Should deck "pass" ever count as a whisper-negative (−0.1 w), or stay pure silence? (Spec says silence.)
3. Fifth axis (`M`) visible at launch or hidden calibration?
4. `notForMe` surface: Painting of the Day only, or nowhere in 1.5?
5. Persona renames — when you're ready, the prototype vectors are name-independent.
6. Instrumentation yes/no (§12).
