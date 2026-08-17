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

**A2 · RESOLVED 2026-08-12. All 20 confirmed mismatches are cleared.**

Register: `IMAGE_RIGHTS_ROUTES.md` §1.6. Thirteen were replaced with the correct
picture. The last seven could not be, because **for five of them the work the
record named has no public-domain photograph on Commons at all** — so the record
was retitled to a work that does, the remedy *Vision of Spain* needed:

| was | is now |
| --- | --- |
| Claude Lorrain, *The Enchanted Castle* | *Landscape with Narcissus and Echo*, 1644, NG London |
| Reza Abbasi, *Portrait of a Dervish* | *Young Man with a Sword*, 1622–24, Detroit |
| Poussin, *The Four Seasons* | *The Adoration of the Golden Calf*, c. 1633–34, NG London |
| Emily Carr, *Big Raven* | *Forest, British Columbia*, 1931–32 |
| Mihri Müşfik, *Self-Portrait* | *Portrait of a Woman*, undated |

**Two have no usable image in any form**, so the gallery entry was removed and
the work keeps its place in the artist's `works[]` with no picture — the honest
state rather than a gap: **Sesshū's *Winter Landscape*** (there is no
public-domain Sesshū on Commons at all) and **Xu Beihong's *Galloping Horse***.

**Two caveats carried, not smoothed:**
- The Detroit file page says the Reza Abbasi is **"possibly by"** him. The
  gallery schema has no attribution field, so it is recorded here.
- Mihri Müşfik's replacement is **untitled and undated on Commons** — described
  only as "Turkish art". The generic title is deliberate, not a guess.

**Method notes worth keeping.** A retitle that keeps the old year silently
invents a fact: all five carried the *previous* work's date until they were
checked against the file pages — Claude Lorrain would have read 1664 for a 1644
painting. And regex surgery on `artworks.js` produced malformed JSON twice; the
file round-trips exactly through `json.dumps(indent=1)`, so structural edits
should parse, modify and re-serialise rather than pattern-match.

**A3 · RESOLVED 2026-08-08 — owner: add the real ones, re-file the rest.**
`orientalism` now contains exactly three European Orientalists and nobody else:
**Gérôme**, **John Frederick Lewis** (who actually lived a decade in Cairo, and
never painted a nude) and **Ludwig Deutsch** (who painted most of his Egypt in a
Paris studio). Şeker Ahmed Paşa, Osman Hamdi Bey and Raja Ravi Varma moved to
**`academicism`** — the defensible description, since two of the three were
taught by Gérôme inside that system. The movement's own blurb and description
were rewritten: they had centred on Osman Hamdi Bey as a member, and now name who
is deliberately *not* filed there and why.

**A4 · RESOLVED 2026-08-08 — owner: follow the Curator.** Added an **additive
optional `nationNote`**, exactly as recommended: the flag chip, the nation index
and every shipped id are untouched, and the acknowledgment sits *beside* the flag
rather than replacing it. Rendered on the artist identity line, deliberately not
a link (it names a fact; it is not a second place to travel to), validator-bounded
to a non-empty string ≤90 chars — a guard proved non-vacuous by feeding it a
95-char note and a number.

**15 records annotated**, chosen on a stricter test than the arithmetic one. A
scan found **51** painters who died before their filed state existed, but "Italy"
on Leonardo is museum convention and misleads no one. The notes go where the flag
implies the wrong *people*, not merely the wrong century: five Ottoman painters
filed 🇹🇷 (Matrakçı Nasuh was Bosnian-born), six Netherlandish and Flemish painters
filed 🇧🇪 for a state founded in 1830, two filed 🇮🇳 for a republic founded in 1947,
Ludwig Deutsch (Austrian by birth, French from 1919), and El Greco, whose Greek
filing is right and whose career was entirely Spanish.


---

# B. New requests, 2026-08-07

## B1 · Navigation — reduce, group, stop overlapping  **[DONE 2026-08-08]**

**Artists · Museums · Lists · Explore ▾ · Taste** — five destinations, one line
(measured: one distinct row at 1280px, where eight items previously wrapped to
two).

All four of the owner's asks are answered:
1. **One line.** Eight top-level items became five.
2. **The Explore overlap is gone.** Movements and Nations were each listed
   twice — top level *and* inside the Explore hub. The four taxonomy indexes and
   the three whole-atlas instruments now live in one place, grouped **Browse**
   (Movements, Techniques, Eras, Nations) and **The big pictures** (Everything at
   once, Timeline, Influences).
3. **Subsections exist**, as a W3C APG *disclosure navigation* menu — not a
   `menu`/`menuitem` widget. The children stay ordinary links in labelled lists,
   so a screen reader reads them the way it read the flat nav the owner's
   VoiceOver passes signed off; the button adds `aria-expanded` and nothing else.
4. **Taste has a home** outside the footer.

Artist-first entry (OD-2) is untouched: Artists is still first.

**The panel had to leave the header, and that was forced.** `.site-header`
carries `backdrop-filter`, which makes it the containing block for
`position:fixed` descendants, so a panel inside it positioned itself against the
header rather than the viewport; and on narrow screens `.main-nav` is a
horizontally scrolling row whose `overflow-x` and mask clipped what remained.
**Measured at 390px, the first build rendered the panel as a sliver under the
header** — it looked correct at 1280px and was broken on a phone. The panel now
sits at body level, where `position:fixed` means the viewport. The cost is DOM
adjacency, so Tab handling is explicit: Tab from the trigger enters the panel,
Shift+Tab from the first link returns to it, Tab off the last link continues to
Taste.

Verified in-browser, both viewports and both themes: click, Escape (focus
returns to the trigger), ArrowDown/Up/Home/End, Tab in all three directions,
outside-click, and the active state across all 13 routes. No console errors.

## B2 · Actuality  **[BUILT AND LIVE 2026-08-12 — both rules ratified]**

Spec: **`docs/ACTUALITY.md`**. Live at **`#/actuality`**, linked from Lists.

**Two products, per the owner's refinement.** Type 1 is the *comparison article*
— visual rhyme, but the writing is about the **painting**: educational, detailed,
5–8 minutes, with only one or two funny lines touching the news photo. Type 2 is
the *blockbuster list* — works joined to the story by art-historical association,
each with its own polished paragraph.

**Type 2 shipped**: *The King Goes to Philadelphia*, answering LeBron James's
move to the 76ers. Four works that already hang in the Philadelphia Museum of
Art, a second Cassatt, and Goya's king. Verified before writing — the ESPN report
was fetched and read, and the entry states only what it states.

**The rules did work on their first outing.** Goya is written straight and says
why. **Manet's *Execution of Emperor Maximilian* was considered and left out** —
a genuinely apt "imported ruler" joke, and a firing squad, so §5 excludes it.

**A property worth keeping:** an Actuality entry borrows the cover of whatever it
points at, so it can never introduce an image. Verified — the asset inventory did
not move at all (836/835/1/115).

**Still to build:** type 1 has a schema and a format and no page of its own yet;
and none of this is placed in `PIGMENT.md` §11 phasing.

## B3 · The painters the atlas already named  **[DONE 2026-08-08]**

Four records added (`js/artists-18.js`), all public domain, 15 gallery images,
each verified by rendering it and looking:

- **Giovanni Bellini** — Giorgione and Titian both came through his workshop,
  and both were already here without him.
- **Andrea del Verrocchio** — named in Leonardo's own life text. His record says
  plainly that *very few paintings are certainly his*, and that Vasari's famous
  story about Leonardo's angel ending his painting career is unevidenced.
- **Giorgio Vasari** — the curator role is named after him. His `rinascita`
  became, via Michelet, the word *Renaissance*.
- **Jean-Léon Gérôme** — taught **Osman Hamdi Bey and Mary Cassatt**, both
  already in the atlas.

**A new movement, `academicism`,** was added because Gérôme had nowhere correct
to live: the atlas carried `orientalism` but no node for the system that produced
it. **This is also a candidate answer to A3** — the Ottoman and Indian painters
currently filed as Orientalists were trained inside the academic system, which
describes them in a way `orientalism` does not. Still the owner's call.

**Six influence edges added**, all documented pupillage rather than stylistic
resemblance, with their basis written into `js/influences.js` — the schema has no
source field (**E2**), so a comment is the only place to put it. The
Michelangelo→Vasari edge is flagged in that comment as the weakest of the six.

**Still absent** and named by the atlas's prose: Orozco, Siqueiros (both in the
`muralism` blurb, which still has one artist), Mehoffer, Aliye Berger.

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
- **C6 · DONE 2026-08-08.** The Coordinator's quality gate no longer greps.
  `check_quality_review_text()` locates the operative revision (text after the
  last `# Quality Review` heading), then its last `Gate 2 verdict` section, and
  reads the verdict only from a line that *starts* with it — so prose about a
  verdict is not a verdict, and BLOCKED anywhere in that section fails even if
  CERTIFIED is also present. Six tests, each one a way the old gate was fooled.
  Non-vacuity demonstrated: a document with rev 1 CERTIFIED and rev 2 BLOCKED
  **passed** the old gate and fails the new one; so does the sentence that
  described the bug.

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
