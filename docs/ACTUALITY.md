# Actuality — the visual-rhyme ritual

*Specification, 2026-08-08. Backlog **B2**. This is new product surface: it is
not in any phase of `PIGMENT.md` §11, and it needs two owner decisions before the
first entry can ship. Written so that building it is a small job once those are
made.*

---

## 1. What it is

Once a month, Pigment publishes **one artwork paired with one piece of
actuality**, and a small set of catalog lists drawn along the same theme.

The reference is `@artsbutmakeitsports`. The mechanic is **visual rhyme, not
thematic association**. The joke is not "the news is about basketball, so here is
a sporting picture." It is *this photograph and this painting are the same
composition* — or the same human situation, four centuries apart.

**No live data.** Pigment has no backend and is not going to get one. This is a
curated, hand-written entry deployed on a cadence. Copy must never imply the site
knows what happened today.

---

## 2. Why the constraint is the feature

Rights close off illustration completely: a runway show, a transfer, a film
première — none of it has imagery Pigment can legally use. So the list cannot
*illustrate* the news. It has to **answer** it out of the atlas.

That is the good version of the idea rather than a compromised one:

- it needs **no new images**, so it costs nothing per entry but writing;
- it gives the **12 placeholder editorial lists** — owner-declared, awaiting
  replacement — a reason to exist and a renewable supply;
- it is the most shareable surface the product would have, and share surfaces
  were deferred during PIG-001 pending exactly this kind of content;
- it teaches art history by **recognition** rather than instruction, which is
  much closer to Pigment's "figures you can identify with" than a survey is.

---

## 3. The worked example — already entirely in the repository

The owner's imagined case: *a luxury house appoints a famous name to a creative
role; pair it with something like a pope blessing Napoleon.*

That painting is real, and Pigment already holds it.

- **`jacques-louis-david` → "The Coronation of Napoleon"** is a gallery image on
  his artist page today.
- His prose in `js/artists-3.js` already says the *Coronation* **"contains a
  diplomatic fiction"** — David painted in Napoleon's mother, who boycotted the
  ceremony.
- And the painting's own joke is the one the pairing needs: **Napoleon crowns
  himself** while Pius VII sits behind him with a hand raised. The Pope is
  present, and blesses nothing.

A brand hiring a celebrity to bless a decision it had already made is that
picture exactly. The rhyme, the history and the punchline are all already here —
which is the proof that the format works on the atlas Pigment actually has.

---

## 4. Data shape

A new registry, `js/actuality-1.js`, following the shape of `js/lists-1.js`:

```js
window.ACTUALITY = [
  { id:"…",                  // kebab, stable, becomes #/actuality/<id>
    published:"2026-09-01",  // the cadence date, not "today"
    hook:"…",                // ≤ 64 chars, the card line
    workId:"…",              // catalog id, OR
    worksKey:{ artistId:"…", title:"…" },   // a gallery work with no catalog record
    story:"…",               // what happened, factual, no adjectives doing work
    rhyme:"…",               // the pairing, 60–120 words, this is the piece
    lists:["…"],             // ids in EDITORIAL_LISTS drawn along the same theme
    sensitive:false }        // see §5 — true suppresses the comic register
];
```

`workId` **must** resolve, and the entry must not introduce a new image: the
whole point is that the atlas already holds the picture. A validator rule should
enforce both.

---

## 5. Tone — the rule that does not exist yet

`STYLE_GUIDE` forbids humour where warning, consent or factual qualification is
required, and the atlas "keeps the record" on hard history: Degas's
antisemitism, Gauguin's colonial ledger, Gérôme and the Orientalism argument.
None of that survives a jokey caption.

**Proposed rule.** A funny register is permitted only when *both* the news item
and the painting can carry it.

- If the painting's subject is violence, slavery, colonial subjugation, religious
  persecution, illness or death, the entry is written **straight** — the rhyme
  can still be the point, but the voice is dry, not comic.
- If the news item concerns death, crime, war, disaster or an identifiable
  person's misfortune, **there is no entry that month on that story.** Pick
  another story.
- `sensitive:true` is the switch, and the default when unsure is `true`.

This is the first owner decision. **Nothing should ship until the rule is
ratified**, because the failure mode is a Pigment-branded joke over a painting of
someone's suffering, and that is not recoverable by an edit afterwards.

## 6. Living people — the second gap

The copy will name real, living people: an executive, an athlete, a designer.

- Pigment is **describing a publicly reported event and making an art-historical
  comparison**. That is commentary, not a factual claim about the person.
- The `story` field states only what was publicly reported, and reads as
  reportable fact without characterisation.
- The joke lands on **the situation**, never on the person's appearance,
  character, private life, or anything not in the public report.
- No entry about a person's legal trouble, health, family or death.

OD-5's language rules cover images and art-historical claims. They say nothing
about naming a living person, so this is the second owner decision.

---

## 7. Surfaces

1. **Homepage card** — one, current entry only, below the hero. Uses the existing
   `.card` treatment; the image is the artwork.
2. **`#/actuality/<id>`** — the full entry: artwork, the rhyme, the story, links
   to the artist, the work, and the month's lists.
3. **`#/actuality`** — the archive, newest first. Entries never expire; an old
   pairing is still a good pairing.
4. The month's **lists** are ordinary `EDITORIAL_LISTS` entries, so nothing new
   is needed to render them.

Nav: it belongs under **Lists** rather than as a sixth top-level item — the nav
was just reduced to five on purpose (**B1**) and should not grow back.

---

## 8. What blocks the first entry

**I cannot write entry #1, and this is worth stating plainly.** A real entry must
match a real, current news story. I have no verified current-news source in this
environment, and inventing a plausible-sounding news event to demonstrate the
format would be exactly the kind of fabrication the rest of this project's
standards exist to prevent — the same failure as a filename that says "Exterior"
over a photograph of an inscription tablet.

So: the mechanism, the schema, the rules and the worked example are specifiable
now. The first published pairing needs the owner to name the story, or to approve
a source Pigment reads. Everything in §§4–7 can be built and tested before that
happens, using the David *Coronation* example as the fixture.
