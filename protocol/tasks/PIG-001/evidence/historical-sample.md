# PIG-001 — Historical Evidence Sample (AC13)

**Author:** Seurat (`claude-data-steward`), Data and Copyright Steward
**Date:** 2026-07-25
**Branch:** `pig-001-stabilization`
**Scope note:** this evidence is held **out of band**, in this document. Per the
frozen specification, AC13 has *no shipped-schema prerequisite* — nothing here
was added to `js/artists-*.js` or `js/influences.js`, and no source, confidence
or dispute field was introduced into shipped data.

---

## Verdict

**The historical layer is substantially accurate and entirely uncited.**

Across 10 profiles × 5 claim classes (50 slots) plus 20 influence edges, I found
**no fabricated claim**. Dates, biography and major works hold up well against
public sources. What the sample does establish is that Pigment's history is an
*editorial* layer presented in the register of *reference*: 70 slots examined,
**zero carry a citation**, because the schema has nowhere to put one.

The failures cluster in one place — **classification**, where Pigment's
single-value `nation` and European `movements` taxonomy is applied to artists it
does not fit. That is a taxonomy design consequence, not carelessness, and it
falls hardest on exactly the non-Western artists the atlas is trying to include.

| Classification | Slots | Share |
| --- | --- | --- |
| **Supported** by a citable public source I actually checked | 47 | 67% |
| **Plausible but uncited** | 17 | 24% |
| **Questionable** | 6 | 9% |
| **Fabricated** | **0** | 0% |

Of 70 slots: 50 profile claims (31 supported / 15 plausible / 4 questionable)
and 20 influence edges (16 supported / 2 plausible / 2 questionable).

This supports OD-1's positioning (an editorial, path-discovering tool, **not** a
comprehensive historical reference) and supports AC14's prohibition on
comprehensive-historical-reference claims. It does **not** support any claim of
scholarly accuracy, and none should be made.

---

## Method

Claims were checked against English Wikipedia article text and REST summaries,
fetched live on 2026-07-25 at ≥0.25 s intervals with retry/backoff. Wikipedia is
a *citable public source* in the sense AC13 requires (it is public, stable and
itself referenced) but it is **tertiary**; "supported" below means "corroborated
by a public source I actually opened", never "verified against scholarship".

Three classifications are used, as the criterion specifies:

- **Supported** — the source states the claim, and I read the passage.
- **Plausible but uncited** — consistent with the source and with general
  knowledge, but the source does not state it, or states it more hedged than
  Pigment does.
- **Questionable** — the source contradicts it, or the claim applies a category
  the source does not support.

A lookup that failed is recorded as **unverified**, never as a negative. One
occurred (`Kim Hong-do` under Pigment's spelling) and was resolved by redirect
to `Kim Hongdo`; it is *not* counted as a defect.

### Spread (AC13 requires ≥5 eras, ≥5 movements, ≥5 nations)

| Dimension | Distinct values in the sample | Requirement |
| --- | --- | --- |
| Eras | 8 — 15th, 16th, 17th, 18th, 19th, 20th century (+ overlaps) | ≥5 ✅ |
| Movements | 11 — high-renaissance, baroque, ukiyo-e, abstract-art, symbolism, ottoman-miniature, realism, mannerism, expressionism, der-blaue-reiter, post-impressionism, literati-painting | ≥5 ✅ |
| Nations | 9 — italy, japan, sweden, turkey, korea, russia, india, china (+ Hungary via dual identity) | ≥5 ✅ |

The sample deliberately over-weights non-Western and less-canonical figures
(Matrakçı Nasuh, Kim Hong-do, Bada Shanren, Amrita Sher-Gil), because that is
where sourcing risk is highest and where a canonical-artist sample would have
produced a falsely reassuring result.

---

## The ten profiles

Claim classes: **B** biography · **D** dates · **C** classification ·
**W** major works · **R** relationships.

### 1. Leonardo da Vinci (`leonardo-da-vinci`) — Italy, 15th–16th c., High Renaissance

| Class | Pigment claims | Verdict |
| --- | --- | --- |
| B | Born illegitimate at Vinci; apprenticed to Verrocchio; served Milan/Florence/Rome; died at Cloux aged 67 | **Supported** — all corroborated; Pigment already hedges the "died in the king's arms" legend with "reportedly", which is the correct treatment |
| D | 1452–1519 | **Supported** |
| C | italy / High Renaissance | **Supported** — "Italian polymath of the High Renaissance" |
| W | Mona Lisa, The Last Supper, Lady with an Ermine, **Salvator Mundi** | **QUESTIONABLE** — see below |
| R | rivaled Michelangelo | **Supported** |

**Questionable — *Salvator Mundi*.** Pigment lists it flatly as a major work of
Leonardo. The source: "attributed **in whole or part** to Leonardo… this
attribution **has been disputed** by some leading specialists who propose that he
only contributed certain elements; others believe that the extensive restoration
prevents a definitive attribution." This is the most contested attribution in
recent art history and Pigment presents it without qualification. It is also
already flagged in `tools/audit_artworks.py`'s `OVERRIDES`, so the codebase knows
the work is awkward — for image resolution, not for attribution.

### 2. Artemisia Gentileschi (`artemisia-gentileschi`) — Italy, 17th c., Baroque

| Class | Verdict |
| --- | --- |
| B | **Supported** — professional by 15; first woman admitted to the Accademia delle Arti del Disegno |
| D | 1593 – c. 1656 | **Supported** — the source gives a firm birth year and an uncertain death; Pigment's `c.` correctly carries the uncertainty |
| C | italy / baroque | **Supported** — "Italian Baroque painter" |
| W | Judith Slaying Holofernes; Self-Portrait as the Allegory of Painting; Judith and her Maidservant | **Supported** |
| R | influenced by Caravaggio | **Plausible but uncited** — the source says "initially working in the style of Caravaggio", which is a style claim, not a documented contact |

### 3. Katsushika Hokusai (`katsushika-hokusai`) — Japan, 18th–19th c., Ukiyo-e

| Class | Verdict |
| --- | --- |
| B | **Supported** |
| D | 1760–1849 | **Supported** |
| C | japan / ukiyo-e | **Supported** — "Japanese ukiyo-e artist of the Edo period" |
| W | The Great Wave; Red Fuji; **Hokusai Manga (1814–78)** | **Plausible but uncited** — the first two supported. The *Manga* is dated 1814–78, i.e. 29 years past the artist's death; the posthumous volumes are real, but a reader sees an artist's work dated three decades after he died with no explanation |
| R | (ukiyo-e lineage) | **Plausible but uncited** |

### 4. Hilma af Klint (`hilma-af-klint`) — Sweden, 20th c., Abstract art / Symbolism

| Class | Verdict |
| --- | --- |
| B | **Supported** — mystic; member of "The Five"; Theosophy |
| D | 1862–1944 | **Supported** |
| C | sweden / abstract-art + symbolism | **Plausible but uncited** — the source calls her work "among the first major abstract works in Western art history"; era `20th-century` alone omits a career beginning in the 1880s |
| W | The Ten Largest (1907); Paintings for the Temple (1906–15); The Swan series (1914–15) | **Supported** |
| R | predates Kandinsky/Malevich/Mondrian | **Supported** — the source states the priority claim explicitly |

### 5. Matrakçı Nasuh (`matrakci-nasuh`) — "turkey", 16th c., Ottoman miniature

| Class | Verdict |
| --- | --- |
| B | **Supported** — polymath, mathematician, historian, miniaturist; the *matrak* etymology is corroborated |
| D | c. 1480 – c. 1564 | **Supported** |
| C | **nation: `turkey`** | **QUESTIONABLE** — see below |
| W | View of Istanbul; Stations of the Iraq Campaign; View of Aleppo | **Plausible but uncited** — and note the *image* for "View of Istanbul" was the Aleppo folio until corrected this round (see `rights-register.md`) |
| R | — | **Plausible but uncited** |

**Questionable — nationality.** The source describes him as a *"16th-century
Ottoman **Bosnian** statesman"* — `el-Bosnavî`, from Visoko. Pigment assigns
`nation: "turkey"`. Two distinct errors are folded together: the Ottoman Empire
is not modern Turkey, and the man was ethnically Bosnian. This is the clearest
case in the sample of a **single-value `nation` field forcing a wrong answer**,
and it is not fixable by editing this record — the schema has one slot.

### 6. Kim Hong-do / Danwon (`kim-hong-do`) — Korea, 18th–19th c., **"Realism"**

| Class | Verdict |
| --- | --- |
| B | **Plausible but uncited** — the article is thin |
| D | 1745 – c. 1806 | **Plausible but uncited** — the source gives "1745 – c.1806 to 1814"; Pigment's value sits inside that range but presents a contested death date as settled |
| C | **movement: `realism`** | **QUESTIONABLE** — see below |
| W | Ssireum (Wrestling); A Schoolroom (Sodang); Dano Day | **Supported** — corroborated via the *Danwon pungsokdo* album |
| R | — | **Plausible but uncited** |

**Questionable — movement.** Pigment files a Joseon-dynasty court painter under
**Realism**, a 19th-century French movement. The source describes his work as
*"Genre paintings"* and names the album *Danwon pungsokdo*; the word "realism"
appears **zero times** in the article. Korean art history calls this genre
*pungsokhwa*. This is an anachronistic category applied for want of a fitting
one — the same taxonomy pressure as Matrakçı Nasuh, on the movement axis instead
of the nation axis. Also minor: Pigment's name spelling did not resolve at
Wikipedia without a redirect (`Kim Hong-do` → `Kim Hongdo`).

### 7. Sofonisba Anguissola (`sofonisba-anguissola`) — Italy, 16th–17th c., High Renaissance / Mannerism

| Class | Verdict |
| --- | --- |
| B | **Supported** — Cremona, minor noble family; her apprenticeship set a precedent for women students; met Michelangelo in Rome |
| D | c. 1532–1625 | **Supported** — matches the source's hedged `c.` |
| C | italy / high-renaissance + mannerism | **Plausible but uncited** — the source says "Italian Renaissance painter"; the Mannerism attribution is a reasonable editorial reading, not a sourced one |
| W | The Chess Game; Self-Portrait at the Easel; Portrait of Philip II | **Supported** |
| R | Michelangelo recognised her talent | **Supported** — stated in the source |

### 8. Wassily Kandinsky (`wassily-kandinsky`) — "russia", 20th c., Expressionism / Der Blaue Reiter / Abstract

| Class | Verdict |
| --- | --- |
| B | **Supported** — born Moscow; began painting studies at 30 |
| D | 1866–1944 | **Supported** |
| C | **nation: `russia`** | **Plausible but uncited** — the source: "Russian painter and art theorist **active in Germany**". He later took German and then French citizenship. Not wrong, but flattened — the same single-value `nation` limitation, in its mild form |
| W | Composition VII; Improvisation 28; Composition VIII; Several Circles; Yellow-Red-Blue | **Supported** |
| R | Der Blaue Reiter; pioneer of abstraction | **Supported** |

### 9. Amrita Sher-Gil (`amrita-sher-gil`) — "india", 20th c., Post-Impressionism

| Class | Verdict |
| --- | --- |
| B | **Supported** — formal lessons at eight; recognition at 19 for *Young Girls* |
| D | 1913–1941 | **Supported** |
| C | **nation: `india`** | **Plausible but uncited** — the source: "**Hungarian–Indian** painter". Same flattening, and here it erases a dual identity central to how she is discussed |
| W | Young Girls (1932); Three Girls (1935); Bride's Toilet (1937) | **Supported** — *Young Girls* dated 1932 in the source |
| R | — | **Plausible but uncited** |

### 10. Bada Shanren / Zhu Da (`bada-shanren`) — China, 17th–18th c., Literati painting

| Class | Verdict |
| --- | --- |
| B | **Plausible but uncited** — Ming imperial descent and the late-Ming/early-Qing rupture are corroborated only in outline |
| D | c. 1626–1705 | **Supported** |
| C | china / literati-painting | **Supported** — "late-Ming and early-Qing dynasty Chinese painter, calligrapher, and poet" |
| W | Fish and Rocks; Lotus and Birds; **Two Birds (c. 1694)** | **QUESTIONABLE** — I could not corroborate a distinct work by this title, and Pigment shipped the *Lotus and Birds* image for it (a duplicate, removed this round). Recorded as unresolved rather than deleted: the record may be right and merely unsourced |
| R | — | **Plausible but uncited** |

---

## The twenty influence edges

`js/influences.js` holds **225 edges** across the five declared relationship
types: `taught` (26), `influenced` (129), `befriended` (53), `rivaled` (14),
`partners` (3). The 20 below were selected by deterministic stride within each
type, so every declared type is represented.

**Structural finding first, because it governs every row:** an edge is a
**three-element array** — `[from, to, type]`. There is **no source field, no
confidence field, and no dispute field**, so *every one of the 225 edges is an
uncited editorial assertion*, and a contested relationship is indistinguishable
from a documented one. The "confidence" and "dispute" columns below are **mine,
produced out of band for this criterion**; they exist nowhere in the product.

| # | Type | Edge | Source checked | Confidence | Dispute state |
| --- | --- | --- | --- | --- | --- |
| 1 | taught | Theophanes the Greek → Andrei Rublev | WP *Andrei Rublev* | Medium | **Hedged in source** — "is **considered to have** trained Rublev"; documented only that they worked together on the Annunciation Cathedral (1405). Pigment states it flatly |
| 2 | taught | François Boucher → Jean-Honoré Fragonard | WP | High | Undisputed |
| 3 | taught | Camille Pissarro → Paul Gauguin | WP | High | Undisputed; "mentored" is the more usual word than "taught" |
| 4 | taught | Ilya Repin → Zinaida Serebriakova | WP *Zinaida Serebriakova* | **High — verified** | "In 1901… she entered the art school founded by Princess Maria Tenisheva, **where she studied with Ilya Repin**" |
| 5 | influenced | Giotto → Masaccio | WP | High | Standard art-historical lineage |
| 6 | influenced | Caravaggio → Francisco de Zurbarán | WP *Zurbarán* | **LOW — contradicted** | See below |
| 7 | influenced | Antoine Watteau → François Boucher | WP | High | Boucher engraved Watteau's drawings early in his career |
| 8 | influenced | Jean-François Millet → Salvador Dalí | WP | High | Dalí's *Angelus* obsession is self-documented |
| 9 | influenced | Edvard Munch → Ernst Ludwig Kirchner | WP | High | Standard Expressionism lineage |
| 10 | influenced | Piet Mondrian → Victor Vasarely | WP *Victor Vasarely* | **Low** | **Mondrian is not mentioned anywhere in the Vasarely article.** Not disproof — but uncorroborated at the obvious source |
| 11 | befriended | Giorgione ↔ Titian | WP | Medium | They collaborated on the Fondaco dei Tedeschi frescoes; "befriended" is traditional rather than documented |
| 12 | befriended | Renoir ↔ Gustave Caillebotte | WP | High | Caillebotte was patron, friend and named Renoir his executor |
| 13 | befriended | Picasso ↔ Wifredo Lam | WP | High | Picasso championed Lam in Paris |
| 14 | befriended | Lucian Freud ↔ Francis Bacon | WP | High | Documented close friendship, later estranged — the estrangement is not representable in a single-type edge |
| 15 | rivaled | Leonardo ↔ Michelangelo | WP | High | Documented (Palazzo Vecchio commissions; Vasari) |
| 16 | rivaled | Joshua Reynolds ↔ Thomas Gainsborough | WP | High | Documented Royal Academy rivalry |
| 17 | rivaled | Henri Matisse ↔ Picasso | WP | High | Documented — but they were also friends and mutual collectors; the single-type edge picks one and discards the other |
| 18 | partners | Diego Rivera ↔ Frida Kahlo | WP | High | Documented marriage |
| 19 | partners | Jackson Pollock ↔ Lee Krasner | WP | High | Documented marriage |
| 20 | partners | Max Ernst ↔ Leonora Carrington | WP | High | Documented relationship, 1937–40 |

### The one edge a source contradicts

**#6 Caravaggio → Zurbarán (`influenced`).** Wikipedia's *Francisco de Zurbarán*
states: *"It is **unknown whether Zurbarán had the opportunity to see the
paintings of Caravaggio**, only that his work features a similar use of
chiaroscuro and tenebrism."* The article separately notes he "gained the nickname
'Spanish Caravaggio'" for that resemblance.

So the source explicitly declines the transmission claim that Pigment asserts as
fact. A stylistic resemblance — likely mediated through Ribera and other Spanish
followers — has been recorded as a direct influence edge. Pigment renders these
edges as claims in "Lineage & circle" with a directional verb, so a reader is
told something the source says is unknown.

**Disposition: recorded, not changed.** Removing the edge would lose a real
stylistic relationship; keeping it as-is overstates. The honest fix is a
confidence or "attributed/contested" marker on the edge type, which is a schema
change and firmly outside PIG-001's frozen scope. **Recommended** for the
relationship-modelling work OD-2 and OD-4 both gesture at.

### Edge findings in aggregate

| Finding | Count |
| --- | --- |
| Edges carrying a source in shipped data | **0 of 225** |
| Edges carrying a confidence or dispute marker | **0 of 225** |
| Sampled edges I could corroborate at a public source | 18 of 20 |
| Sampled edges hedged by the source but flat in Pigment | 1 (Theophanes → Rublev) |
| Sampled edges uncorroborated at the obvious source | 1 (Mondrian → Vasarely) |
| Sampled edges the source contradicts | 1 (Caravaggio → Zurbarán) |
| Sampled edges that are **fabricated** | **0** |
| Reciprocal relationships flattened to one directional type | ≥2 observed (Matisse/Picasso, Freud/Bacon) |

---

## What this sample does and does not license

**Does:** it licenses saying Pigment's historical layer is *editorially sound* —
a curated, broadly accurate, human-written account, with no invented artists, no
invented works and no invented relationships in a 70-slot probe.

**Does not:** it does not license any claim of comprehensiveness, scholarly
sourcing, or historical authority. Concretely, the following must **not** be
said of Pigment on the strength of this evidence:

- that its historical claims are *sourced* — none in shipped data is;
- that its influence graph is *verified* — 225 edges, 20 sampled, 0 citable
  in-product, and 1 of the 20 contradicted by its own obvious source;
- that its classifications are *authoritative* — the `nation` and `movements`
  taxonomies demonstrably misfit non-Western artists (Matrakçı Nasuh, Kim
  Hong-do), and the misfit is structural, not clerical;
- that anything outside these 10 profiles and 20 edges has been checked. **237
  artist profiles and 205 influence edges remain unreviewed** and are explicitly
  unresolved under AC12's discipline.

This is consistent with, and supports, the release language Wave D already
corrected under AC14 and OD-1: *"an editorial, path-discovering tool, not a
comprehensive history of art."* The sample is evidence **for** that positioning
and evidence **against** any stronger one.

---

## Recommendations (out of scope here, recorded for routing)

1. **Qualify *Salvator Mundi*** in Leonardo's works list, or drop it. It is the
   one flatly-stated claim in the sample that a reader could call wrong.
2. **`nation` needs to admit more than one value**, or an `origin`/`active`
   distinction. Matrakçı Nasuh, Kandinsky and Sher-Gil all lose real information
   to a single slot, and it is the atlas's non-Western entries that lose most.
3. **Kim Hong-do should not be filed under `realism`.** A `genre-painting` or
   `pungsokhwa` movement id would be truthful; the current value is an
   anachronism.
4. **Influence edges need a confidence or dispute marker.** One sampled edge in
   twenty is contradicted by its own source, and the schema cannot express that.
5. **`bada-shanren::Two Birds`** should be sourced or removed; it is currently an
   uncorroborated work title whose image was a duplicate.

None of these was actioned. Items 1–4 are schema or editorial changes outside
PIG-001's frozen scope; item 5 is a data question I have left open rather than
resolve by deletion on thin evidence.
