# Pigment — backlog

*Working notebook of things to fix, change or decide. Started 2026-08-07 by the
Synthesis Lead at the owner's request. Not a plan and not a commitment — a place
where known work stops living in someone's head.*

**How to use it:** grep before acting on anything here; several entries below
exist because a previous proposal named something the atlas already contained.
Items marked **DECISION** cannot be resolved by an agent.

---

# A. Owner decisions outstanding

**A1 · The `notice` word budget.** `STYLE_GUIDE` §4.3 implies ≤8 words;
`ARTWORK_SCHEMA` §3 says ≤12; the validator checks neither. 21 of the 66 new
bullets sit at 9–12 and shipped at 12, because the existing corpus already does
(`catalog-1.js` opens with a 9-word bullet). **Not declared resolved.** The
Content Editor's argument is worth weighing: §4.3's rule was written for *artist
and movement* traits and was inherited into a work-specific field, so 12 may be
the correct rule rather than a competing one. His `†` markers are in
`CATALOG_BATCH_COPY.md` so either rule can be applied without re-counting.

**A2 · The 12 undetected mismatches.** `audit_artworks.py`'s `suspect` detector
flags 8 of the 20 known wrong images; the other 12 name the artist in the
filename, so nothing asks the matcher about them. The repaired `match_verdict()`
catches all 20 *on demand*. Widening `suspect` sends those 12 to re-resolution —
which **is** the decision to replace them, not a step toward it.

**A3 · `orientalism` is applied to painters the term excludes by definition.**
Two Ottoman painters and one Indian one carry it; the atlas contains **zero**
actual European Orientalists. Osman Hamdi Bey's tagline reads *"Orientalism,
corrected from the inside"* while his `movements` array files him **as** an
Orientalist. Fixing it requires deciding what those painters are instead.

**A4 · Single-valued `nation` cannot carry the truth.** `STYLE_GUIDE` §3.3/§7
already mandate "primary filing + acknowledgment"; the prose honours it; the
schema has no field for it; so the app renders one flag chip — a 🇹🇷 on a man who
died in 1564. ~12 records are visibly wrong on a surface visitors see. The
Curator recommends an **additive optional `nationNote`**, not re-typing shipped
infrastructure.

---

# B. New requests, 2026-08-07

## B1 · Navigation — reduce, group, and stop overlapping

Owner: *"elegant and essential sections at nav, should not be so crowded and
reduced to 1 line instead of 2, overlap between explore and different nav
sections, maybe nav sections should have subsections to group multiple sections
under one, taste or my profile section."*

Four distinct asks:
1. **Fit one line.** Eight top-level destinations currently wrap to two.
2. **Resolve the Explore overlap.** `#/explore` already contains the timeline,
   influence graph, movement trees and nation map, and several of those are
   *also* top-level nav items. The duplication is real.
3. **Group under subsections.** Requires a menu pattern the site does not have —
   note the accessibility cost: the current nav is a flat list of links, which is
   the most robust thing for a screen reader. Any disclosure pattern needs
   `aria-expanded` and keyboard semantics, and the owner's VoiceOver sessions are
   the standard it must meet.
4. **A Taste / My Profile destination.** Taste is currently footer-only. This is
   the *Atlas Coherence Pass* item deferred during PIG-001 (see the deferred
   register) — it is already specified there, not new work from scratch.

**Prior art in-repo:** the Curator's §4.3 conceptual tree in the original theory
brief (Discover / Browse / Explore relationships / Taste / Search) was written for
exactly this and explicitly marked "a conceptual model, not an instruction to
create routes". Start there.

**Constraint:** the shipped artist-first entry hierarchy is owner-ratified
(OD-2). A nav restructure must not quietly overturn it.

## B2 · Actuality — news-aware curated lists

Owner: *"Pigment should be sensitive to live big news from the world across all
media and have news-aware curated lists according to those"* — LeBron to the
76ers (Philadelphia-related, King-related), Nolan's *Odyssey*, a Chanel runway or
Paris Fashion Week, social-media trends, Gen-Z tendencies. *"Updated monthly
news-aware lists."*

**This is the most interesting request here and the one with the most
constraints. All four are recorded so nobody discovers them mid-build:**

1. **No backend, no feed.** Pigment is a zero-dependency static site on GitHub
   Pages. "Live news awareness" can only mean *a person or an agent curating on a
   cadence*, then a deploy. Monthly is achievable; "live" is not, and the copy
   must not imply otherwise.
2. **Rights make illustration impossible.** LeBron, Nolan, a Chanel runway — none
   has imagery Pigment can use. The `died ≤ 1955` rule and the audited routes
   (`IMAGE_RIGHTS_ROUTES.md`) close this off completely.
3. **Constraint 2 is probably the good version of the idea.** The list cannot
   *illustrate* the news, so it must **answer** it out of the atlas: LeBron to
   Philadelphia → Eakins, the Barnes, Philadelphia painting. Nolan's *Odyssey* →
   the Odyssey in painting, Waterhouse, Böcklin, the Sirens. A Chanel runway →
   Sonia Delaunay, textile and pattern, Klimt's dresses. **The news is the door;
   the atlas is the room.** That is squarely inside OD-1's "editorial and
   personalized path-discovering tool" and does not need a single new image.
4. **This also solves an existing item.** The 12 editorial lists shipped in July
   are owner-declared **placeholders** to be remade once the catalog is deep
   enough. News-aware lists are a strong candidate for what replaces them, rather
   than a separate feature bolted alongside.

**Not in any current phase of `PIGMENT.md` §11.** Needs placing before building —
it reads as Phase 1 editorial, but it is genuinely new product surface.

## B3 · Vasari is not in the atlas

Verified 2026-08-07: **0 artist record, 0 gallery images, 0 catalog records.**
The curator role is named after a painter the collection does not contain.

Also absent and *named by the atlas's own prose* (the Curator's "holes the atlas
dug itself"): **Verrocchio** (in Leonardo's own life text), **Bellini** (taught
both Giorgione and Titian, who are both present), **Gérôme** (taught *both*
Ottoman painters), **Orozco** and **Siqueiros** (named in the `muralism` blurb,
which has one artist), **Mehoffer**, **Aliye Berger**.

## B4 · Museum cards — cover photos don't fit

Owner: *"Cover photos don't fit well into the card, there are ones that have
empty space underneath the photo (Orsay, Louvre, Uffizi, etc.)"*

A CSS aspect-ratio/object-fit defect on the museum index cards. Note the owner's
standing rule: **museum cards show the building photograph, never an artwork**;
the museum *page* hero is the artwork collage. Any fix keeps that.

## B5 · Caillebotte — *Man at His Window* artwork page

Caillebotte **is** already an artist with gallery images and **0** catalog
records. This is a catalog record, not an artist addition — exactly the
Direction A work already in flight.

## B6 · Schwitters and Sorolla

Both **already exist** as artists with gallery images and no catalog records.
Same as B5: catalog records, not artist additions.

**One complication:** Schwitters' shipped gallery image is one of the 20
confirmed mismatches — *a photograph of Schwitters*, not a work by him. It needs
replacing before a record can be built on it.

---

# C. Carried forward — small, specified, nobody blocked

- **C1** The ten museum-note hooks the Implementation Lead had to author to land
  the batch (the validator errors on a venue holding works with no note) are the
  only visitor-facing copy in that batch the Content Editor did not write. They
  should be reviewed as his.
- **C2** `catalog-5.js` is enumerated **by name in four separate places**. A
  future `catalog-6.js` will be silently missed by whichever list someone
  forgets — and the rights audit is where a miss would be least visible.
- **C3** `beginning-noland` tier demotion — proposed by the Curator, not built.
- **C4** `tarashikomi` technique — proposed, not built.
- **C5** The `abstract` tag and §5 vocabulary enforcement — would currently fail
  on ~130 shipped records; the Curator says sequence it after normalisation.
- **C6** The Coordinator's quality gate is **non-functional**: it greps an
  append-only file for verdict strings, so it now passes on the archived
  "CERTIFIED" string regardless of the current verdict. Its scan must parse a
  single operative block.

---

# D. Shipped with known residuals (PIG-001)

Documented in `protocol/tasks/PIG-001/quality-review.md` rev 5 and carried
knowingly, not forgotten:

- **D1** Decorative arrows are DOM-fixed but **unconfirmed by ear**; a bare arrow
  persists in **695 prerendered files** across four families.
- **D2** `.md-name` renders at **2.34px** at 320px width in one zoom state —
  legibility, not contrast.
- **D3** Accessibility evidence rests on **one operator, one screen reader, one
  browser**. Structurally: every pixel measurement is Chrome, every ear
  confirmation is Safari — the two evidence bases corroborate each other nowhere.
- **D4** `pigment_coordinator/` is **excluded from the certified scope**; a merge
  carrying it is not covered by that certification.

---

# E. The large threads

**E1 · The atlas is still mostly inert.** 22 catalog records exist against a pool
of ~413 audited images across 141 artists who have none. The Curator's working
ratio: `confirmed` does not mean catalogable — of 20 candidates all 20 confirmed
but only 13 resolved to a Wikidata item carrying collection, date and dimensions.
Several more batches of exactly the work that just succeeded.

**E2 · The influence graph has no sources.** 238 edges, zero citations. And **not
one edge connects two different non-Western traditions** — no China→Korea, no
Persia→Ottoman, no Persia→Mughal, despite these being among the best-documented
transmissions in world art.

**E3 · Whole traditions absent, not thin** (grep-verified): Song and Yuan China,
Mughal painting, Behzād, Joseon before Kim Hong-do, Momoyama/Edo beyond ukiyo-e
and Rinpa, historic Africa, Southeast Asia, colonial Latin America. The holding
institutions are simply not in the venue registry.

**E4 · The taste mathematics — deferred, name agreed (Kandinsky).** The owner
regards the scoring model as potentially Pigment's main product. Measured facts
as of 2026-08-06: **141 of 323** works carry coordinates; the **F and E axes
correlate at +0.60** (two of five axes measuring much the same thing); **E has
mean +44 with almost nothing negative** — which is why the deck-pool warning kept
recurring, and why "fix the content" was treating a symptom. The first job is
measurement, not revolution: audit the coordinates, test discrimination by
simulation, and only then consider new frameworks.
