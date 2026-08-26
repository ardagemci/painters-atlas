# The absent traditions — a roster pass

*2026-08-24. Backlog **E3**. Thirteen painters, and the taxonomy they needed in
order to exist. Nothing here is a rights determination (OD-5).*

---

## 1. What the measurement said

Of the **27 painters in the atlas born before 1500**, fifteen were Italian and
**three** were not European. And `js/taxonomy.js` began its era vocabulary at
**1300** — so Song China, the first tradition E3 names, had no century to be
filed in at all. Fan Kuan was painting monumental landscape three hundred years
before Giotto and the atlas had nowhere to put him.

That is the useful form of the finding: not "we should add some Chinese
painters" but **the vocabulary could not hold them**. A taxonomy is a record of
where its author was looking.

## 2. What was added

**Taxonomy first, because nothing else could be filed without it.** Two eras —
`before-1200` and `13th-century`; the nation `indonesia`; and five movements:
`song-landscape`, `mughal-painting`, `joseon-painting`, `momoyama-painting`,
`viceregal-painting`. `persian-miniature` needed nothing: it already existed and
was empty of its greatest name.

**Thirteen painters** in `js/artists-19.js`:

| tradition | painters |
| --- | --- |
| Song China | Fan Kuan, Guo Xi |
| Yuan China | Huang Gongwang |
| Timurid / Safavid Persia | Kamāl ud-Dīn Behzād |
| Persia → Mughal | Abd al-Samad |
| Mughal India | Basawan, Ustad Mansur |
| Joseon Korea | An Gyeon, Jeong Seon |
| Momoyama Japan | Kanō Eitoku, Hasegawa Tōhaku |
| Java | Raden Saleh |
| New Spain | Miguel Cabrera |

Pre-1500 painters go **27 → 32**; China 1 → 4, Iran 0 → 1, Korea 0 → 1. Italy's
share of that group falls from 56% to 47%. Historic Africa and Southeast Asia
beyond Java stay open — §5.

## 3. Two of E2's three named transmissions close

Backlog **E2**, measured two days ago, found **not one edge joining two
different non-Western traditions**, and found that most of the gap could not be
drawn because the endpoints were absent. They are present now:

- **China → Korea.** `guo-xi → an-gyeon`. The scholarship on *Mongyu dowondo*
  turns on its relation to Guo Xi, and the early Joseon court painted in his
  manner for a century after.
- **Persia → Mughal.** `kamal-ud-din-behzad → abd-al-samad → basawan`. Abd
  al-Samad trained in the Safavid royal atelier Behzād had led, carried it to
  Akbar's workshop, ran that workshop from about 1572, and Basawan came up under
  him.

Cross-tradition edges: **0 → 3** (with `foujita ↔ rivera` from E2).

**Persia → Ottoman stays open, deliberately.** The influence is real and
general; no painter-to-painter link between the atlas's one Persian and its
Ottoman miniaturists survives a source, so none is drawn.

**All eight new edges are grounded in prose, not sourced strings** — the new
records name the painters they descend from, so the ungrounded count stayed at
**107** while the graph grew from 250 to 258. That is the E2 mechanism working
as intended: prose first, citations only as fallback.

**And E2's guard caught a defect in E3 on its first live use.** The grounding
matcher requires a name token longer than three characters, and **Guo Xi has
none** — so no edge of his could ever have been attested, including the one that
closes China→Korea. The validator warned by name. The matcher now drops to a
three-character threshold *only* for painters who would otherwise have no token
at all, rather than for everyone, because short East Asian names will keep
arriving.

## 4. Images — five rejected, and two of them passed the verdict check

Twenty-seven images were resolved and merged. **Five more were rejected**, and
the two interesting ones were both marked `confirmed` by
`tools/audit_artworks.py:match_verdict`:

- **Fan Kuan, *Travelers among Mountains and Streams*** — the resolver returned
  a **crop of the signature with a red annotation box drawn on it**. Commons'
  `ObjectName` is *"Travelers Among Mountains and Streams Signature"*, so the
  artist ties, the work ties, and the verdict is `confirmed`. Replaced by hand
  with the Google Art Project scan of the whole scroll — the single most
  important image in the batch.
- **Ustad Mansur, *Siberian Crane*** — a **photograph of the museum wall
  label**. The label names artist, work, medium and date, so it confirms on
  every axis the check tests. It is a picture of a caption.

**The gap this exposes is precise.** `match_verdict` asks *does this file depict
this artist's work* — and cannot ask *is this file the work, or a picture ABOUT
the work*. A signature crop, a caption card, a museum vitrine and a postage
stamp all pass an artist-and-title test. Recorded as a finding rather than
patched, because the fix is a judgement about image content that the tool has no
way to make; **looking is the control**, and every hero image here was opened.

The other three were caught by the ordinary rules: an Oxford museum display of a
dodo skeleton (Mansur), a different painter's scroll filed as An Gyeon, and a
duplicate — my own `works[]` listed one Behzād painting under two English names.
One image was **retitled rather than rejected**: Guo Xi's resolved file is 幽谷图,
*Deep Valley*, a genuine Guo Xi that is not *Snow Mountain*, so the record now
names the picture it actually shows (the A2 remedy).

**The merge did not touch the existing 183 entries.** `js/artworks.js` round-
trips exactly through `json.dumps(indent=1)`, verified before the write, and the
new entries were merged by parsing and re-serialising rather than by re-running
`tools/fetch_artworks.py` — which rewrites the whole file from every artist and
would have re-resolved the twenty images hand-corrected in A2. Diff: **134 lines
added, zero removed, no existing artist changed.**

## 5. What stays open

1. **Historic Africa.** Genuinely hard rather than overlooked: most surviving
   traditions are anonymous, and naming a painter requires an attributed name.
   Ethiopian manuscript painting has candidates (Fəre Ṣəyon) and they need real
   research, not a guess.
2. **Southeast Asia beyond Java.** Raden Saleh is one painter standing for a
   region.
3. **More of colonial Latin America.** Cabrera is New Spain; the Cusco School is
   largely anonymous, and Melchor Pérez de Holguín in Alto Perú is the obvious
   next name.
4. **These thirteen have no catalog records.** They are E1's pool now — thirteen
   painters with 27 audited images and no artwork page, which is exactly the
   shape the catalog batches consume.
