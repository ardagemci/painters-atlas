# Batch 21 — twenty painters

*Duo session (Claude ↔ Codex), 2026-09-19. Branch `duo/artists-1223`. Nothing
here is a rights determination (OD-5): a death year decided whom to try, and a
Commons page's own licence field is an assertion by its uploader, recorded as
such.*

---

## 1. Why these twenty

The owner asked for twenty artist packages. The atlas had already said where it
was short, so the list was taken from its own measurements rather than from a
general sense of who is famous.

- **Named in the atlas's prose, with no record (9).** `docs/ATLAS_COVERAGE.md`
  Gap 4 lists painters the existing bios reach for and cannot link to. Of
  those still absent, these nine are the ones the prose leans on hardest: Cimabue
  (Giotto's story), Simone Martini and Ambrogio Lorenzetti (Siena), Filippo
  Lippi (Botticelli's teacher), Ghirlandaio (Michelangelo's), Campin (Rogier's),
  Pontormo (Bronzino's), Böcklin (de Chirico's shock), Mucha.
- **The canon around them (2).** Uccello and Antonello da Messina, from Gap 4's
  list of painters absent with no mention at all.
- **Women (3).** The first draft of this list had none, which Claude caught in
  the debate. Elisabetta Sirani, Helene Schjerfbeck and Gwen John replaced
  Guardi, De Hooch and Memling, whose ground Canaletto, Vermeer and van Eyck
  already hold.
- **Traditions with no painter here before (6).** Abbasid Baghdad (al-Wasiti),
  Potosí (Pérez de Holguín), Rinpa's founder (Sōtatsu), Joseon genre painting
  (Shin Yun-bok), Uruguay (Torres-García), Venezuela (Michelena). These closed
  items that `docs/ROSTER_E3.md` §5 and `ATLAS_COVERAGE.md` Gap 2 left open, and
  needed new taxonomy: four nations and the `baghdad-school` movement.

Every one died by 1955, so every page shows sourced images, never a generative
cover.

## 2. What a package is

| part | where |
| --- | --- |
| Record: tagline, life, career, outside, facts, four works | `js/artists-21.js` |
| Images, one per work where a usable file exists | `js/artworks.js` |
| Influence edges, only where the new prose names the link | `js/influences.js` |
| Stub page and sitemap entry | `p/artist/<id>.html`, `sitemap.xml` |
| Evidence: work identity, Commons file and metadata, a source per claim | `docs/roster-batch-21/<id>.json` |
| Guard | `tests/test_artist_batch_21.py`; ledger `ARTIST_BATCH_21` in `tests/test_rights_tooling.py` |

No catalog records. Promoting works into `js/catalog-*.js` is the catalog
batches' pipeline, and ATLAS_COVERAGE's first finding is that the atlas is
already wider than it is deep. These 78 images are now E1's pool, like E3's.

| painter | images | claims | edges | prose |
| --- | --- | --- | --- | --- |
| Cimabue | 4/4 | 16 | 2 | Claude |
| Simone Martini | 4/4 | 15 | 1 | Claude |
| Ambrogio Lorenzetti | 4/4 | 14 | 1 | Claude |
| Filippo Lippi | 4/4 | 17 | 2 | Claude |
| Paolo Uccello | 4/4 | 18 | 0 | Claude |
| Domenico Ghirlandaio | 4/4 | 15 | 1 | Claude |
| Antonello da Messina | 4/4 | 24 | 3 | Codex, edited by Claude |
| Robert Campin | 4/4 | 17 | 1 | Claude |
| Pontormo | 4/4 | 15 | 3 | Claude |
| Elisabetta Sirani | 4/4 | 26 | 2 | Codex, edited by Claude |
| Tawaraya Sōtatsu | 3/4 | 23 | 1 | Codex, edited by Claude |
| Yahya ibn Mahmud al-Wasiti | 4/4 | 20 | 0 | Codex, edited by Claude |
| Melchor Pérez de Holguín | 4/4 | 24 | 2 | Codex, edited by Claude |
| Shin Yun-bok | 4/4 | 22 | 1 | Codex, edited by Claude |
| Arnold Böcklin | 4/4 | 19 | 1 | Claude |
| Arturo Michelena | 4/4 | 24 | 0 | Codex, edited by Claude |
| Alphonse Mucha | 4/4 | 15 | 0 | Claude |
| Helene Schjerfbeck | 4/4 | 27 | 0 | Codex, edited by Claude |
| Gwen John | 4/4 | 27 | 1 | Codex, edited by Claude |
| Joaquín Torres-García | 3/4 | 28 | 0 | Codex, edited by Claude |

## 3. The research gate, and what it changed

Research came before any prose: four works with a stable identity each, and at
least two usable Commons files showing *distinct* works.

- **Armando Reverón failed** — Commons holds no image of his work. **Arturo
  Michelena** (d. 1898) took his place and kept Venezuela in the batch.
- **Campin's *Portrait of a Stout Man* was swapped** for the London *Portrait
  of a Woman*: the source's strictest account of Campin's own hand names the
  two London portraits, not the Thyssen panel.
- **Three files were refused, and two works show no image:**
  - **Tawaraya Sōtatsu, *Deer Scroll*** — The Commons file is 3814x85 px, a whole handscroll as a 45:1 strip; at the 500px thumbnail the gallery uses it would be 11px tall and show nothing.
  - **Joaquín Torres-García, *Two Figures*** — The only Commons file is a CC BY-SA 4.0 gallery photograph (uploader GualdimG); this batch admits only files whose Commons page asserts a public-domain or CC0 basis, so no attribution duty is created.
  - Uccello's Hawkwood fresco: the first file found was a CC BY 3.0 photograph;
    a Commons scan whose page asserts a public-domain basis replaced it.
- **Every image was opened**, on contact sheets of all 78, because E3 showed
  that the matcher passes signature crops and wall labels. None was a crop, a
  label or a gallery-wall photograph.
- **Dates were checked against Wikidata.** Three disagreed and were resolved to
  a cited source, recorded in the sheet as `y_source`: Uccello's San Romano
  (National Gallery: *probably about 1438–40*, against Wikidata's 1456), and
  Cimabue's Santa Croce Crucifix (sources give c. 1265 and "after 1272"; the
  documented later bound is used).

## 4. How the prose was checked

Claude wrote ten records, Codex ten, both only from source texts fetched into
the session (Wikipedia in English, plus Spanish, Korean and Japanese where the
English article was thin). Every factual clause has a claim entry whose note
quotes at most twelve words of the source, and **every quote was re-found
verbatim in the source text by a script** — Codex's as well as Claude's.

Claude then read Codex's ten against the sources and changed four things:
- *"Sōtatsu's screens carry neither inscription nor seal"* generalised a fact
  about **one** pair of screens; it now names the Wind God and Thunder God.
- A fact whose note quoted the wrong line (al-Wasiti: only 13 of 100+ Maqamat
  manuscripts are illustrated) now quotes the line that supports it.
- Four closing sentences that summarised rather than stated were cut.
- A weak fact ("the manuscript uses red and black ink") was replaced.

One of Claude's own edges was dropped: *Campin befriended van Eyck* rested on a
recorded meeting, which is not friendship.

**What this does not establish.** The sources are encyclopaedic, not the
scholarship behind them. A claim that is wrong in the source is wrong here. The
sheets make every claim checkable; they do not make it checked against
primary literature.

## 5. Left for the owner

1. **Pins.** Every image in this batch was chosen by hand, not by the resolver.
   `CLAUDE.md` §6 asks for hand-curated images to be pinned in
   `tools/audit_artworks.py`, which is in the sealed set, so this autonomous run
   did not edit it. The block below is ready to paste into `PINNED`. Until it
   is applied, **the packages are complete except for their pins.**
2. **The two no-image works** stay imageless only as long as nobody re-runs
   `tools/fetch_artworks.py` over the whole file, which would search for them
   afresh. E3's twenty hand-corrections carry the same exposure.
3. **Live browser load** — not done from this session (the preview tooling
   serves the primary checkout). One page load of a new artist is worth doing
   before merging.

```python
    # Batch 21 (docs/ROSTER_BATCH_21.md), 2026-09-19. Every file opened by eye;
    # each Commons page's metadata is recorded in docs/roster-batch-21/<id>.json.
    # No independent legal determination (OD-5).
    "cimabue::Santa Trinita Maestà": "Cimabue - Maestà di Santa Trinita - Google Art Project.jpg",
    "cimabue::Crucifix of Santa Croce": "Cimabue 025.jpg",
    "cimabue::The Mocking of Christ": "La Dérision du Christ - Cimabue - Musée du Louvre Peintures RFML.PE.2023.33.1 - après restauration.jpg",
    "cimabue::Maestà of the Louvre": "La Vierge et l'Enfant en majesté entourés de six anges - Cimabue - Musée du Louvre Peintures INV 254 ; MR 159.jpg",
    "simone-martini::Annunciation with Saints Margaret and Ansanus": "Simone Martini — Annunciation with St. Margaret and St. Ansanus.jpg",
    "simone-martini::Saint Louis of Toulouse Crowning Robert of Anjou": "Simone Martini 013.jpg",
    "simone-martini::Maestà": "Maestà di simone martini, siena palazzo pubblico 1315-1321.jpg",
    "simone-martini::Orsini Polyptych": "Orsini Polyptiek, Simone Martini, 14de eeuw, Koninklijk Museum voor Schone Kunsten Antwerpen, 257-260.jpg",
    "ambrogio-lorenzetti::Effects of Good Government in the City": "Ambrogio Lorenzetti - Effects of Good Government in the city - Google Art Project.jpg",
    "ambrogio-lorenzetti::Presentation in the Temple": "Ambrogio Lorenzetti - Presentazione di Gesù al tempio - Google Art Project.jpg",
    "ambrogio-lorenzetti::Annunciation": "Ambrogio Lorenzetti Annunciation.jpg",
    "ambrogio-lorenzetti::Maestà of Massa Marittima": "Ambrogio lorenzetti, maestà di massa marittima.jpg",
    "filippo-lippi::Madonna and Child with Two Angels": "Madonna and Child with two Angels (by Filippo Lippi) – Galleria degli Uffizi, Florence.jpg",
    "filippo-lippi::Adoration in the Forest": "Maria, das Kind verehrend, mit dem Johannesknaben und dem Heiligen Bernhard - Die Anbetung im Walde, Die Anbetung im Walde - Gemäldegalerie Berlin - 5223451.jpg",
    "filippo-lippi::Coronation of the Virgin": "Fra Filippo Lippi 007.jpg",
    "filippo-lippi::Barbadori Altarpiece": "Pala Barbadori - Fra Filippo Lippi - Musée du Louvre Peintures INV 339.jpg",
    "paolo-uccello::The Battle of San Romano": "Uccello — the Battle of San Romano.jpg",
    "paolo-uccello::Saint George and the Dragon": "Paolo Uccello Heiliger Georg und der Drachen 1 470.jpg",
    "paolo-uccello::The Hunt in the Forest": "Hunt in the forest by paolo uccello.jpg",
    "paolo-uccello::Monument to Sir John Hawkwood": "Paolo Uccello 044.jpg",
    "domenico-ghirlandaio::An Old Man and His Grandson": "Ghirlandaio, Domenico - An Old Man and His Grandson - Louvre - Google Art Project.jpg",
    "domenico-ghirlandaio::Portrait of Giovanna Tornabuoni": "Domenico Ghirlandaio, 1489-1490 - Portrait of Giovanna Tornabuoni - Google Art Project.jpg",
    "domenico-ghirlandaio::Calling of the First Apostles": "Ghirlandaio, Domenico - Calling of the Apostles - 1481.jpg",
    "domenico-ghirlandaio::Adoration of the Magi": "Adoration of the Magi Spedale degli Innocenti.jpg",
    "antonello-da-messina::Saint Jerome in His Study": "Antonello da Messina - St Jerome in his study - National Gallery London.jpg",
    "antonello-da-messina::Virgin Annunciate": "Antonello da Messina, Annunciata di Palermo, circa 1475-77 -FG2.jpg",
    "antonello-da-messina::Saint Sebastian": "Antonello da Messina - St. Sebastian - Google Art Project.jpg",
    "antonello-da-messina::Portrait of a Man": "Antonello da Messina - Portrait of a Man - National Gallery London.jpg",
    "robert-campin::Werl Triptych": "Werl-Triptychons.jpg",
    "robert-campin::Nativity": "La Nativité, par Robert Campin.jpg",
    "robert-campin::Portrait of a Woman": "Robert Campin 012.jpg",
    "robert-campin::Seilern Triptych": "Triptych-with-the-entombment-of-christ-1822.jpg",
    "pontormo::Deposition from the Cross": "Jacopo Pontormo - Kreuzabnahme Christi.jpg",
    "pontormo::Visitation": "Pontormo-visitation-after-restorationRGB.jpg",
    "pontormo::Portrait of a Halberdier": "Pontormo (Jacopo Carucci) (Italian, Florentine) - Portrait of a Halberdier (Francesco Guardi?) - Google Art Project.jpg",
    "pontormo::Joseph in Egypt": "Jacopo Pontormo - Joseph in Egypt - WGA18079.jpg",
    "elisabetta-sirani::Timoclea Kills the Captain of Alexander the Great": "Sirani, Elisabetta - Timoclea uccide il capitano di Alessandro Magno - 1659.jpg",
    "elisabetta-sirani::Portia Wounding Her Thigh": "Elisabetta Sirani - Portia wounding her thigh.jpg",
    "elisabetta-sirani::Virgin and Child": "Sirani Virgin and Child.jpg",
    "elisabetta-sirani::Portrait of Vincenzo Ferdinando Ranuzzi as Cupid": "Sirani Vincenzo Ferdinando Ranuzzi.jpg",
    "tawaraya-sotatsu::Wind God and Thunder God": "Wind God and Thunder God Screens by Tawaraya Sotatsu hi-res.png",
    "tawaraya-sotatsu::Waves at Matsushima": "俵屋宗達《松島図》17世紀、フリーア美術館.jpg",
    "tawaraya-sotatsu::Sekiya and Miotsukushi Screens": "Genji screen 1.jpg",
    "al-wasiti::Abu Zayd before the Governor of Rahba": "Yahyâ ibn Mahmûd al-Wâsitî 001.jpg",
    "al-wasiti::The Pilgrims' Caravan": "Yahyâ ibn Mahmûd al-Wâsitî 005.jpg",
    "al-wasiti::A Village": "Yahyâ ibn Mahmûd al-Wâsitî 007.jpg",
    "al-wasiti::The Eastern Island": "Yahyâ ibn Mahmûd al-Wâsitî 002.jpg",
    "melchor-perez-de-holguin::Entry of Viceroy Morcillo into Potosí": "Entrada Virrey Arzobispo Morcillo.jpg",
    "melchor-perez-de-holguin::Saint Christopher": "Melchor Pérez Holguin - Saint Christopher - 2018.652.2 - Metropolitan Museum of Art.jpg",
    "melchor-perez-de-holguin::Saint Peter of Alcántara and Saint Teresa": "Melchor Pérez Holguín - Saint Peter of Alcántara and Saint Teresa - A1837 - Hispanic Society of America.jpg",
    "melchor-perez-de-holguin::Virgin of the Rosary": "Melchor Pérez Holguín - Virgin of the Rosary - 1994.37.3 - Dallas Museum of Art.jpg",
    "shin-yun-bok::Portrait of a Beauty": "Shin Yun-bok - A Beautiful Woman - Google Art Project.jpg",
    "shin-yun-bok::Dano Day": "Hyewon-Dano.pungjeong.jpg",
    "shin-yun-bok::Lovers under the Moon": "Hyewon-Wolha.jeongin-3.jpg",
    "shin-yun-bok::Sword Dance": "Hyewon-Ssanggeomdaemu.jpg",
    "arnold-bocklin::Isle of the Dead": "Arnold Böcklin - Die Toteninsel III (Alte Nationalgalerie, Berlin).jpg",
    "arnold-bocklin::Self-Portrait with Death Playing the Fiddle": "Arnold Boecklin-fiedelnder Tod.jpg",
    "arnold-bocklin::The Plague": "Arnold Böcklin - Die Pest.jpg",
    "arnold-bocklin::War": "Arnold Böcklin - Der Krieg.jpg",
    "arturo-michelena::Miranda in La Carraca": "Miranda en la Carraca by Arturo Michelena.jpg",
    "arturo-michelena::The Young Mother": "La Joven Madre 1889 by Arturo Michelena.jpg",
    "arturo-michelena::Charlotte Corday": "Arturo Michelena 03.JPG",
    "arturo-michelena::Penthesilea": "Arturo Michelena, Penthesilea, 1891.jpg",
    "alphonse-mucha::Gismonda": "Alfons Mucha - 1894 - Gismonda.jpg",
    "alphonse-mucha::Job": "Alphonse Mucha - Advertisment for Job cigarettes, 1896.jpg",
    "alphonse-mucha::The Seasons": "Alfons Mucha - The Seasons, 1896.jpg",
    "alphonse-mucha::The Slav Epic": "Apotheosis of the Slavs history - Alfons Mucha.jpg",
    "helene-schjerfbeck::The Convalescent": "Helene Schjerfbeck (1862-1946)- The Convalescent - Toipilas - Konvalescenten (32721924996).jpg",
    "helene-schjerfbeck::Wounded Warrior in the Snow": "Helene Schjerfbeck - Wounded Warrior in the Snow.jpg",
    "helene-schjerfbeck::Self-Portrait with Black Background": "Helene Schjerfbeck, Self-Portrait, Black Background, 1915.jpg",
    "helene-schjerfbeck::Girl with Blonde Hair": "Girl with Blonde Hair (SM 2463).png",
    "gwen-john::Self-Portrait": "Gwen John - Self-portrait (1902).jpg",
    "gwen-john::A Corner of the Artist's Room in Paris": "Gwen John - A Corner of the Artist's Room in Paris, 1907–1909, VIS.2576, Museums Sheffield.jpg",
    "gwen-john::Nude Girl": "Gwen John - Nude Girl.jpg",
    "gwen-john::Girl Reading at the Window": "Gwen John - Girl Reading at a Window, 1911, 421.1971.jpg",
    "joaquin-torres-garcia::Inverted America": "Joaquín Torres García - América Invertida.jpg",
    "joaquin-torres-garcia::Constructive Clock": "'Constructive Clock' by Joaquín Torres García , 1936. oil on canvas.jpg",
    "joaquin-torres-garcia::Portrait of Josep Pijoan": "(Barcelona) Retrat de Josep Pijoan - Joaquim Torres-Garcia - Museu Nacional d'Art de Catalunya.jpg",
```
