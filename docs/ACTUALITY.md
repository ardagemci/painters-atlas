# Actuality — the visual-rhyme ritual

*Specification, 2026-08-08. Backlog **B2**. **Both rules ratified by the owner on
2026-08-12** (§5 tone, §6 living people), and the product split into two types at
the same time. The first list is built and live.*

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

## 1a. Two products, not one

**Type 1 — the comparison article.** `kind:"article"`. A news photograph and a
painting that are *the same picture*. The connection is visual rhyme and only
visual rhyme.

- **The article is about the painting.** It is educational writing and it has to
  be detailed and correct: what is happening in it, who made it and when, what to
  look at, what most people do not know.
- **One or two lines only** touch the news photograph, at the start or at the
  end, and those are the funny ones. The joke opens or closes the door; it is not
  the room.
- **5–8 minutes of reading** — roughly 1,000–1,600 words.
- Pigment cannot show the photograph. The rhyme is described, not displayed.

**Type 2 — the blockbuster list.** `kind:"list"`. A story everybody already has
an opinion about, answered with works joined to it by art-historical association
rather than by visual rhyme: the city, the nickname, the institution, the idea.

- Worked example, and the one that shipped: LeBron James to Philadelphia →
  Philadelphia's own walls, and a king. A painting of an army marching from
  Philadelphia to Boston would be the perfect Sixers–Celtics joke; the atlas does
  not hold one, so the list says what the atlas *does* hold.
- **Each work gets its own paragraph** — polished, not long. What is being
  painted, a piece of its history, something most people would not know, and a
  fact worth repeating. That is the `essay` field; `note` stays the one-line hook.
- It is an ordinary `EDITORIAL_LISTS` entry, so it costs no new rendering.

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

## 4. Data shape — as built

`js/actuality-1.js` holds the registry; `js/lists-1.js` holds the list a type-2
entry points at.

```js
window.ACTUALITY = [
  { id:"…",                 // kebab, permanent → the archive at #/actuality
    kind:"list",            // "list" (type 2) | "article" (type 1)
    published:"2026-09-01", // the cadence date, never "today"
    headline:"…",           // what happened, flat and factual
    newsline:"…",           // only what the cited report states
    source:{ name:"…", url:"…" },   // real, checkable, and actually read
    hook:"…",               // the card line — this one may be funny
    listId:"…",             // kind:"list"    → an EDITORIAL_LISTS id
    workId:"…",             // kind:"article" → a catalog id
    sensitive:false }       // see §5; default true when unsure
];
```

An entry **never carries its own image**. The card borrows the cover of whatever
it points at, which is by definition already in the atlas — so no Actuality entry
can add an asset, and the inventory cannot move because of one.

Type-2 list items gain an optional `essay` (200–900 chars, validator-bounded)
beside the existing `note` (≤120 chars).

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

**RATIFIED by the owner, 2026-08-12.** This is now binding on every entry. The
failure mode it prevents is a Pigment-branded joke over a painting of someone's
suffering, which no later edit repairs.

*Applied in the first list:* the Goya is the one work written straight, and its
paragraph says why — a king painted without flattery is not a punchline. Manet's
*Execution of Emperor Maximilian* was **considered and left out**: it is a
genuinely apt Philadelphia-import joke and it is a firing squad, so the rule
excludes it. That is the rule doing its job on its first outing.

## 6. Living people — the second gap

The copy will name real, living people: an executive, an athlete, a designer.

- Pigment is **describing a publicly reported event and making an art-historical
  comparison**. That is commentary, not a factual claim about the person.
- The `story` field states only what was publicly reported, and reads as
  reportable fact without characterisation.
- The joke lands on **the situation**, never on the person's appearance,
  character, private life, or anything not in the public report.
- No entry about a person's legal trouble, health, family or death.

**RATIFIED by the owner, 2026-08-12.** OD-5's language rules cover images and
art-historical claims and said nothing about naming a living person; this closes
that gap and binds every entry.

*Applied in the first list:* the entry names LeBron James, states the contract
terms and the date exactly as ESPN reported them, and makes no claim about him
beyond that. The joke is on the situation — a city receiving a famous arrival —
and the paintings carry it.

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

## 8. Sourcing — resolved

The owner approved Google and Reuters as news sources on 2026-08-12, which
removes the blocker this section used to record.

**The first entry was verified before a word of it was written.** A search
returned the story; the ESPN report was then fetched and read, and the entry
states only what that report states: signed with the Philadelphia 76ers,
announced 24 July 2026, two years and $8m with a player option, his
twenty-fourth NBA season, at forty-one, alongside Joel Embiid and Tyrese Maxey.
Nothing in the entry comes from memory.

That is the standing procedure: **search, then fetch and read the report, then
write.** An entry whose source has not been read is not publishable, for the same
reason a filename is not evidence that a picture is what it says it is.

## 9. Still to build

- **Type 1, the comparison article**, has a schema and a format here and no page
  of its own yet. It needs a route and a long-form template; the list type reuses
  `EDITORIAL_LISTS` and needed neither.
- **A homepage surface.** Actuality currently lives at `#/actuality`, linked from
  Lists. `PIGMENT.md` §11 still has no phase for any of this.
