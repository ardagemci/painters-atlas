# Pigment Taste Mathematics

*v1 — July 2026. The formal definition of the taste engine: a **Graph-Augmented Distributional Taste Model**. Companion to `ADMIRE_SPEC.md` (product behavior) and `STYLE_GUIDE.md` (how results are worded). Users never see this document's vocabulary — they see a Taste Passport. Principle: **simple surface, serious engine — and complexity follows data, not ambition.***

---

## 0. The three layers

| Layer | Object | Status |
|---|---|---|
| **Taste Space** | artworks, artists, movements, museums, users as points/clouds in a shared 5-axis space | V1 |
| **Influence Graph** | 211+ typed edges (taught/influenced/…) + memberships, embedded as geometry | V2 |
| **Confidence Layer** | how sure the engine is, per axis, at all times | V1 |

---

## 1. Taste Space

### 1.1 Axes and scale

Five axes, canonical scale **−100 … +100** (integers; human-readable for hand-scoring).

| Key | −100 pole | +100 pole |
|---|---|---|
| `F` | Figurative | Abstract |
| `D` | Calm | Dramatic |
| `E` | Classical | Experimental |
| `C` | Sensual | Conceptual |
| `M` | Intimate | Monumental |

Primary visible map: `F × D`. `M` is stored from day one, surfaced later.

A taste vector is written `v = {F, D, E, C, M}`, e.g. Caravaggio's *Calling of Saint Matthew* ≈ `{−85, +92, −30, −20, +55}`.

### 1.2 Coordinate assignment (movement-first inheritance)

1. **Movements (74)** are hand-scored once — the master data.
2. **Artists** inherit the weighted mean of their movements (primary ×2, others ×1); **Tier 1 artists get hand overrides**.
3. **Artworks** inherit their artist's vector; **Tier 1 artworks get per-work overrides** where the artist's arc demands it (Goya's tapestry cartoons ≠ the Black Paintings).

Validator rules: all coords integer in [−100, +100]; Tier 1 artworks must have explicit coords; overrides logged.

### 1.3 Weighted distance

Distances weight the primary 2D map higher:

```
d(a, b) = sqrt( Σ_axis  λ_axis · (a_axis − b_axis)² )
λ = { F: 1.5, D: 1.5, E: 1.0, C: 1.0, M: 1.0 }
```

Persona matching may upgrade to **Mahalanobis distance** (distance measured relative to the shape of the user's own cloud) once the mixture layer (§3) is live: a narrow-taste user and a wanderer should not be judged by the same yardstick.

---

## 2. The V1 user model — shrunken centroid with a decaying prior

### 2.1 Quiz prior

Each onboarding answer applies nudges of **±30** (soft options **±15**) to 1–2 axes (mapping table in `ADMIRE_SPEC.md` §6.3). Nudges sum per axis, capped at ±60:

```
q = clip( Σ nudges, −60, +60 )        // the quiz prior vector
```

### 2.2 The core equation

```
u = ( Σ_i  w_i · x_i  +  k · q ) / ( Σ_i w_i  +  k )
```

- `x_i` — coords of the i-th admired item; `w_i` — its weight
- `k = 6` — the quiz "weighs" six artworks
- **All admiration weights are 1.0 in V1.** Weak-signal probes (movement cards, generative style cards) get `w = 0.5`. No other weighting until real data justifies it.

**Why not a fixed 70/30 blend:** a static ratio lets five onboarding taps own 30% of a 500-admiration veteran's identity forever. With the decaying prior, quiz influence is 60% at n=4, 11% at n=50, ~1% at n=500 — provisional fast, refined forever, automatically.

### 2.3 Worked example

Quiz (Arda's sample answers): mastery matters (E −30), depth & symbolism (C +30), strange/ugly beauty (D +30), disturb me (D +30), transforms the world (E +30)
→ `q = {F: 0, D: +60, E: 0, C: +30, M: 0}`.

Admired (n = 4):

| Work | F | D | E | C | M |
|---|---:|---:|---:|---:|---:|
| Calling of St Matthew | −85 | +92 | −30 | −20 | +55 |
| Judith Slaying Holofernes | −88 | +95 | −25 | −15 | +30 |
| Woman Holding a Balance | −90 | −60 | −45 | −35 | −80 |
| The Penitent Magdalene | −80 | +40 | −35 | −25 | −45 |

```
u = ( Σx + 6q ) / (4 + 6)
  = { F: −343/10, D: (167+360)/10, E: −135/10, C: (−95+180)/10, M: −40/10 }
  = { F: −34, D: +53, E: −14, C: +9, M: −4 }
```

Reading: figurative-leaning, dramatic, faintly classical — with the quiz (rightly) dominating at n=4. The same admiration pattern at n=40 gives `D ≈ +44`: the prior fades as the evidence grows. That single property *is* the "provisional fast, refined forever" principle, expressed as arithmetic.

---

## 3. The taste cloud — a 1-or-2 component mixture (V1.5, not V2)

**The centroid-mush problem strikes on day one:** admire six quiet interiors and six Suprematist grids, and your average is beige — a wrong Persona at the exact moment the user decides whether to share it. So V1.5 ships a minimal mixture model:

### 3.1 Algorithm (k ≤ 2, deterministic)

```
1. Compute single centroid u; total spread S1 = Σ w_i · d(x_i, u)²
2. Seed two centers at the two admirations farthest apart
3. Run 5 iterations of 2-means (assign → recompute), weights respected
4. Split spread S2 = Σ w_i · d(x_i, nearest center)²
5. ACCEPT the split iff:
     S2 ≤ 0.6 · S1                    // split explains ≥ 40% of spread
     AND each cluster has ≥ 3 items
     AND centers are ≥ 50 apart in the F×D plane
   else keep the single centroid.
```

The quiz prior attaches to the *larger* component (it calibrates the dominant taste, not the island).

### 3.2 What the mixture gives the product

| Math object | Product meaning |
|---|---|
| Component mean | a taste island's center |
| Component weight | how much of you lives there |
| Component covariance / spread | broad vs narrow island |
| Two accepted components | hybrid identity: *"two islands: quiet interiors and dramatic shadows"* |
| Admiration with high distance from both centers | *"a beautiful outlier in your Passport"* (outlier: `d > 90` from nearest center) |
| Large spread, split rejected | the eclectic/general Personas |

---

## 4. Confidence

Internal confidence is **per-axis**, not a single number, and comes from spread + sample size — not from counts alone:

```
n_eff        = Σ w_i + k
sd_axis      = sqrt( Σ w_i (x_i,axis − u_axis)² / n_eff )
sem_axis     = sd_axis / sqrt(n_eff)
conf_axis    = 1 − min(1, sem_axis / 25)
coverage_axis: "informed" iff ≥ 3 signals with |x_axis| ≥ 40
```

Ten Baroque nocturnes make `D` confident and `F` ignorant; the engine must know which axes it is still guessing about (this drives the adaptive deck, §6). The user-facing tiers (provisional → forming → solid → strong → deep, by admiration count) remain **as copy**, mapped from `n`, per the product notebook — the count table is the poem, the variance is the truth.

Quiz-vs-evidence disagreement (`|q_axis − evidence mean| > 50` on any informed axis) keeps the Persona flagged `provisional: true` regardless of n.

---

## 5. Persona matching

- **Specific Persona** = prototype vector + optional signature condition, e.g. a Dutch-interior archetype ≈ `{−80, −50, −40, −40, −80}` + admired ≥ 2 Dutch Golden Age works.
- Matching is **per-component**: each taste island is matched independently against prototypes with the weighted distance of §1.3 (Mahalanobis when available). Two accepted components → primary Persona from the heavier island, secondary from the lighter: hybrid identity for free.
- **General Personas** fire on *shape*, not position: split-rejected high spread (mean `sd ≥ 45`) → eclectic archetypes; wide era range among admirations → time-traveler archetype; two accepted far-apart components with comparable weights → contradiction archetype. A wanderer is a wanderer because their cloud is wide — not because classification failed.
- Candidates = top 3 by distance (with any fired general archetype guaranteed one slot). **Adopted Personas never auto-switch**; milestone recomputes may *offer*.

---

## 6. The onboarding deck as active learning (V1.5)

Fixed decks waste taps. The deck should maximize information per reaction:

- **Stage 1 (4 anchor works, fixed):** one from each F×D quadrant, all with |F|,|D| ≥ 50 — coarse quadrant fix.
- **Stages 2–4 (adaptive, 4 works each):** pick from precomputed buckets keyed by `(current quadrant, most-uncertain axis)` — probing E, then C, then the weakest axis again. The policy is a small baked JSON lookup (quadrants × axes × candidates), not runtime search: static-site friendly.
- Hard constraints preserved from `ADMIRE_SPEC` §6.2 (the copyright-skew defense): ≥ 3 abstract-capable works (`F ≥ +30`), ≥ 2 non-European, era spread, all with confident coords and great images.
- Effect: ~12 adaptive reactions ≈ 20–25 static ones. Serves the sub-4-minute ruling.

Skips are **silence** (`w = 0`), stored in the passport (`skipped`) for future modeling — never negative signal in V1.

---

## 7. Recommendations V1 — the discovery rings

Score candidates by distance to the *nearest* user component; exclude already-admired; enforce artist diversity (max 2 per artist per batch).

| Ring | Distance `d` | Label (product) |
|---|---|---|
| Inner | ≤ 35 | Close to your taste |
| Middle | 35–65 | A little outside your map |
| Outer | 65–95 | A stretch admiration |
| Wildcard | > 95, curated | A wildcard from the atlas |

Default batch mix: 3 inner / 2 middle / 1 outer / 1 wildcard. All radii and mixes are tunable parameters (§10).

---

## 8. Upgrade path (gated by data, never by enthusiasm)

### V2 — when museums + Tier-1 artworks land
- **Graph embeddings (build-time, zero infrastructure):** random walks over the typed graph (influence/membership/technique/location edges, type-weighted) → co-occurrence PPMI matrix → truncated SVD, d ≈ 16 → baked `embeddings.js`, exactly like `worldmap.js`. Every entity then has two addresses: taste space (how it looks) and context space (where it historically lives).
  Blended score: `s = 0.5·simTaste + 0.3·simContext + 0.15·novelty − 0.05·redundancy`. This is the moat: nobody else has *Theophanes taught Rublev* as geometry.
- **Optimal transport for cloud-vs-cloud:** museum ↔ user matching as earth-mover's distance between the user's mixture and the museum's collection cloud (exact assignment for ≤ 64 points; Sinkhorn if larger). Kills the "average of the Louvre is beige" problem. Copy: *"your taste cloud fits almost entirely inside the Musée d'Orsay's."* Interim cheap version: set-overlap counts ("40 works inside your taste zone").

### V3 — when real users and a backend exist
- **Learned latent space:** implicit-feedback matrix factorization (ALS with confidence weighting) on the co-admiration matrix, d ≈ 32; then regress learned factors onto the five named axes so the poetic labels survive as an interpretable overlay on a learned engine.
- **Bandit discovery radius:** learn per-user wildcard appetite (Thompson sampling over ring mix) instead of fixed rings. Log `(ring shown → admired?)` from V1 onward so the data exists when the bandit arrives.
- **Taste drift & Wrapped:** `recentVector` (90-day window) vs lifetime vector; drift = weighted distance; monthly deltas feed *"your taste has drifted toward Symbolism"* and the yearly Wrapped aggregations (most-admired artist/movement, dominant palette hue, top island, wildest outlier = max-distance admiration).

---

## 9. Glossary — math ↔ product

| Engine | Surface |
|---|---|
| Weighted shrunken centroid | "the center of gravity of your taste" |
| Mixture component | "a taste island" |
| Component separation | "two centers: quiet interiors and dramatic shadows" |
| High variance, split rejected | the wanderer archetypes |
| Low-likelihood admiration | "a beautiful outlier in your Passport" |
| Posterior variance | "your map is still forming" |
| Prior decay | "your Persona sharpens as you admire" |
| Earth-mover's distance | "your cloud fits inside this museum's" |
| Drift vector | "your taste has moved this season" |

## 10. Tunable parameters (defaults)

| Param | Default | Notes |
|---|---:|---|
| `k` (quiz prior weight) | 6 | in artwork-equivalents |
| nudge / soft nudge | ±30 / ±15 | prior cap ±60 per axis |
| probe weight | 0.5 | movement/generative cards |
| split acceptance | S2 ≤ 0.6·S1 | + min 3 items + 50 apart in F×D |
| outlier radius | 90 | from nearest component |
| rings | 35 / 65 / 95 | weighted distance |
| batch mix | 3/2/1/1 | inner/middle/outer/wildcard |
| λ (axis weights) | 1.5/1.5/1/1/1 | F,D primary |
| confidence sem scale | 25 | conf = 1 − sem/25 |

All defaults are guesses to be beaten by data; changing them must not require schema changes — and per §8, the data decides when the engine earns its next layer of intelligence.
