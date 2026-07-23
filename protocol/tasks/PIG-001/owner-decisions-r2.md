# PIG-001 — Owner Decisions (product owner: Arda)

Recorded 2026-07-23, at `approved_for_build`, ahead of human review. The
build must honor these; they also surface in the Human Review Package. Two
carry durable product-direction signal beyond PIG-001 (marked → DIRECTION)
and are recorded so a later task can pick them up **without** expanding this
frozen stabilization scope.

## OD-1 — Release positioning · DECIDED (a)
Pigment is an **editorial and personalized path-discovering tool** — an
Atlas-backed editorial discovery + accountless Taste experience, not a
comprehensive historical reference. Public language constrained accordingly.

## OD-2 — Artist-first hierarchy · RATIFIED (a), with reservation
"Start with an artist" is the ratified recommended first action. Owner is
not certain about its long-term future and reserves the right to revisit.
→ DIRECTION: Pigment's pull should partly come from **presenting artists as
"superheroes" people connect with and identify with — associating oneself
with an artist or a movement.** This is a north-star refinement for later
identity/onboarding work (Persona layer, artist pages), not a PIG-001 build
item. Persona/label names remain Arda's to set.

## OD-3 — Google Fonts / privacy · DECIDED (a)
**Self-host** the OFL fonts as `woff2` committed to the repo; eliminate the
third-party `fonts.googleapis.com`/`fonts.gstatic.com` runtime calls.
Zero-dependency-compatible; same typography. Build unit 20 executes this.

## OD-4 — Deck-warning / scoring disposition · DECIDED (a), elevated
Authorize honest editorial re-scores where merit supports; otherwise a dated
owner exception. Taste coordinates are never tuned merely to silence the
validator (unchanged principle).
→ DIRECTION (significant): the owner regards the **artwork-scoring system /
taste mathematics as potentially Pigment's MAIN product**, and wants it
"polished or even revolutionized." This elevates TASTE_MATH from supporting
mechanism to candidate flagship. Consequences recorded, not acted on here:
(1) PIG-001 stays a bounded stabilization — the ~2 honest re-scores fix the
current calibration gap only; (2) a dedicated future objective (a taste-math
/ scoring overhaul) is warranted and should be proposed to the theory pole
as its own task with its own deliberation; (3) that future work touches
docs/TASTE_MATH.md, docs/ADMIRE_SPEC.md, the coordinate corpus, and the
onboarding engine — none in this release's scope.

## OD-5 — Rights/legal posture · DECIDED (a)
Ship on **documented residual risk**: the register records asserted basis,
attribution, and residual uncertainty; any actual *clearance* claim requires
qualified review; unresolved items are labeled unresolved, never "cleared."
The Matisse/Kahlo cross-store inconsistency is adjudicated inside the
register (AC11 sample).
