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

## B2 · Actuality — the visual-rhyme ritual  **[owner refined 2026-08-07]**

**Not live news on the site.** A **monthly editorial ritual** that adds (a) a set
of lists drawn from the existing catalog matching global news, and (b) a homepage
card — clickable through to a full page — pairing **one artwork** with one piece
of actuality, written as a brief, funny, educational article.

**The mechanic is visual rhyme, not thematic association.** The reference is
`@artsbutmakeitsports`. The joke is not "basketball, so let us find a sporting
picture"; it is *this photograph and this painting are the same composition*, or
the same situation four centuries apart. My earlier note framed this as thematic
("LeBron to Philadelphia → Eakins") — **that is the weaker version and is
superseded.**

**A worked example that already exists in the atlas.** Owner's imagined case: a
luxury house appoints a famous name to a creative role; pair it with something
like a pope blessing Napoleon. That painting is real — David's *Coronation of
Napoleon* (Louvre) — and `js/artists-3.js` already carries David and already says
his *Coronation* **"contains a diplomatic fiction"**: Napoleon crowns himself
while Pius VII sits behind him with his hand raised, and David painted in a
mother who boycotted the ceremony. A brand hiring a celebrity to bless a decision
it had already made is *exactly* that picture. The rhyme, the history and the
joke are all already in the repository.

**Why this is strong for Pigment specifically:**
- It needs **no new imagery** — the constraint that kills illustrating the news
  is what forces the mechanic to be good.
- It gives the **12 placeholder lists** (owner-declared, awaiting replacement) a
  reason to exist and a renewable supply.
- It is the most shareable surface the product would have, and share surfaces
  were deferred in PIG-001 pending exactly this kind of content.
- Gen-Z art-history learning through recognition rather than instruction, which
  is closer to Pigment's "figures you can identify with" than a survey is.

**Constraints that still hold:**
1. No backend. Monthly cadence via curation and deploy; copy must never imply
   live awareness.
2. **Tone is a real risk.** `STYLE_GUIDE` forbids humour where warning, consent
   or factual qualification is required, and the atlas "keeps the record" on hard
   history (Degas's antisemitism, Gauguin's colonial ledger). A funny voice must
   not be allowed to reach a painting whose subject cannot carry it. The rule
   should be explicit before the first one ships.
3. **Living people are named in the copy.** A joke about a real person's
   appointment is commentary, not a factual claim, but the line between the two
   needs stating — and nothing in the current OD-5 language rules covers it.
4. Not in any phase of `PIGMENT.md` §11. Reads as Phase 1 editorial; needs
   placing.

## B3 · Vasari is not in the atlas

Verified 2026-08-07: **0 artist record, 0 gallery images, 0 catalog records.**
The curator role is named after a painter the collection does not contain.

Also absent and *named by the atlas's own prose* (the Curator's "holes the atlas
dug itself"): **Verrocchio** (in Leonardo's own life text), **Bellini** (taught
both Giorgione and Titian, who are both present), **Gérôme** (taught *both*
Ottoman painters), **Orozco** and **Siqueiros** (named in the `muralism` blurb,
which has one artist), **Mehoffer**, **Aliye Berger**.

## B4 · Museum cards — cover photos don't fit

Owner: *"Cover photos don't fit well into the card... checking whether all
museums have an acceptable photo fitting well in the card."*

**Two problems, and only the first was CSS.**

**(a) The frame defect — FIXED, commit `8aa3bba`.** The fill rule was scoped to
`.aw-card`, so museum photographs and editorial list covers fell through to bare
`img{max-width:100%}` inside a fixed 16:10 box. Wide photographs left a strip
beneath; portrait ones overflowed and clipped. Verified in-browser: 104 of 104
cards now fill exactly, and the check was confirmed non-vacuous by disabling the
rule in-page (104 of 104 mismatched, worst gap 237.9px).

**(b) The photographs themselves — OPEN, and this is the real answer to the
owner's question.** All 104 were measured; full table in
`docs/MUSEUM_PHOTO_AUDIT.md`. **Only 23 of 104 sit comfortably in a 16:10
frame.** 22 are portrait, 6 are wider than 1.90.

More important than the ratios: several are **architectural detail shots that do
not read as the building at any crop** — `kunsthistorisches` is a close-up of a
stone inscription tablet, `vatican-museums` a side doorway in a brick wall,
`kunsthalle-mannheim` a red wall at close range. Meanwhile `munch`, the most
extreme ratio in the whole set at 0.56, works perfectly because the photograph
carries the museum's name in lit signage. **Ratio does not predict whether a card
works.** The remaining review needs eyes, not arithmetic.

**Ten indexed venues have no photograph at all** and render a generative canvas
where a building should be: `ateneum`, `kunstmuseum-basel`, `moa-museum-of-art`,
`national-museum-korea`, `national-museum-warsaw`, `ngma-new-delhi`,
`pera-museum`, `santa-maria-novella`, `skagens-museum`, `tokyo-national-museum`.
Note what that list is: Finland, Korea, Poland, India, Turkey, Japan, Denmark —
**the venues holding the atlas's non-Western and smaller-nation works are the
ones missing photographs.** That is the same collecting-history skew recorded in
E3, showing up in a second surface.

The owner's standing rule holds throughout: **museum cards show the building
photograph, never an artwork**; the museum *page* hero is the artwork collage.

## B5 · Caillebotte — *Young Man at His Window*  **[DONE 2026-08-08, `f9fd9b9`]**

Shipped as his first catalog record. Two facts were corrected on the way: the
artist record dated the work **1875** (it is 1876), and I had assumed the Musée
d'Orsay held it — the **J. Paul Getty Museum** bought it at Christie's in 2021
for $53m, after France had declared it a national treasure.

**New open question it raised.** `build_seo.jxa.js` prefers a *catalogued* work
for an artist stub's `og:image`, so adding this record switched Caillebotte's
social preview from **Paris Street; Rainy Day** — his most famous painting — to
this one. That rule will fire again on every artist whose first catalog record
is not their best-known work, and it silently degrades the share image. **Owner
decision:** should the share image follow the catalog, or should an artist keep
a designated hero? Recorded in the `CATALOG_BATCHES` ledger so it is visible.

## B6 · Schwitters and Sorolla — wrong images  **[DONE 2026-08-08]**

All six were opened and looked at. Four were correct and kept — including the
Merzbau photograph, since that work was destroyed in 1943 and survives only in
photographs. Two were wrong and are replaced:

**Schwitters — *Ursonate*** was a **1927 photographic portrait of Schwitters**:
the artist standing in for a forty-minute sound poem. Commons has no page of the
published score; the only *Ursonate* images there are photographs of a 2024
performance in Rudolstadt, which would have been a different error. The slot now
holds ***Das Undbild*** (1919), a real Merz assemblage. **The Ursonate keeps its
place in his career prose**, which is where a sound poem belongs — the atlas can
say a thing exists without pretending to show it.

**Sorolla — *Vision of Spain*** was a **photograph of the room**: ceiling, floor,
orange walls, the murals small across the far side. It is a fourteen-panel cycle
and no single frame represents it, so the entry is renamed **"Vision of Spain:
Catalonia"** and shows that panel (*Cataluña. El pescado*, public domain). His
prose still says "fourteen monumental panels", so the cycle is not misread as one
picture.

**Method note.** Neither error was findable from the filename — both files were
named plausibly. This is the third time in this sequence that opening the file
changed the answer, after the museum photographs and the Caillebotte attribution.


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
