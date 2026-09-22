# IFACE-001 — Cross-registry identity evidence

Inspection baseline: `016d6ab014eb7d10255b1c27aaf2b000faaf709c`. Offline census of local registries and checked-in artwork stubs. No remote source or image loading was tested.

## Method and limits

Plan: enumerate both registries; match assets before artwork keys; separate eligibility from gallery reachability; inspect route stubs; enumerate conflicts and unresolved identity cases.

`EXACT ASSET` means the gallery img and catalog image.src identify the same Commons file after decoding percent escapes, replacing underscores with spaces, and removing thumbnail sizing/path wrappers (Unicode NFC). Commons file titles establish shared assets, not artwork identity. Source page URLs are preserved as evidence, not silently substituted for the delivered image.

`CONFIRMED SAME ARTWORK` means a different file, identical artistId and exact gallery title equality with catalog title or worksKey. This is confirmation under the requested registry-key rule, not independent art-historical verification. A missing catalog src also permits this key comparison. A series-level key is insufficient to confirm a particular work and is classified AMBIGUOUS even when worksKey agrees. `AMBIGUOUS` retains same-artist partial-title candidates (or multiple title matches) without assigning identity. `UNMATCHED` means neither asset nor title evidence nor a same-artist partial-title candidate; shared artist alone is insufficient. No translation, fuzzy-title or Commons redirect inference is made.

Catalog eligibility requires a nonempty src and status pd or licensed. Tokens are recorded metadata, not legal conclusions. Missing gallery status is an unresolved policy question; it is not itself classified as an error.

Gallery behavior: viewArtist in js/app.js has an ungated ARTWORKS image path, as RIGHTS-001 E-007 established. However, that Major works panel runs only when the artist has no TIER1 arc and the title occurs in artist.works. Arc artists instead use catalog cards. “Active” below means static source reachability through that ungated path, not a browser/network success. “Latent” means the entry has an img but is currently hidden by the arc panel or absent artist key. Both are listed so registry conflicts are not mistaken for currently visible images.

**Prerender: INSPECTION OF CHECKED-IN STUBS, not execution of tools/build_seo.jxa.js.** The builder could emit different metadata if the stubs are stale. Each matched route below gives the literal decoded og:image content from git HEAD; a missing route or tag is explicit. Runtime eligibility and stub content are separate measurements.

## Summary

| Measure | Count |
| --- | ---: |
| Catalog records | 398 |
| ARTWORKS entries | 581 |
| EXACT ASSET | 173 |
| CONFIRMED SAME ARTWORK | 4 |
| AMBIGUOUS | 2 |
| UNMATCHED | 402 |
| Gallery entries reachable through ungated panel | 478 |
| Matched withheld catalog / gallery-img conflicts (entry–record pairs) | 1 |
| Of those, active ungated gallery rendering | 0 |
| Of those, latent gallery entries | 1 |
| Entries without a confirmed artwork route mapping | 404 |

## Full withheld-catalog / gallery-img conflict list

- `henri-matisse` / **The Snail** → `the-snail` (CONFIRMED SAME ARTWORK); status `copyright`, src missing; gallery **LATENT (not currently rendered by this panel)**. Full URLs and stub inspection follow in its census row.

## Complete entry census

Every heading identifies the exact ARTWORKS artistId/title key. Catalog references preserve record IDs and source files. No confirmed mapping means no identified canonical artwork route; candidate routes must not be treated as an identity link.

### 1. leonardo-da-vinci / Mona Lisa

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `leonardo-da-vinci` → `Mona Lisa`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg/500px-Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg`; page: `https://en.wikipedia.org/wiki/Mona_Lisa`.
- Normalized gallery asset: `Mona Lisa, by Leonardo da Vinci, from C2RMF retouched.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `mona-lisa`; title `Mona Lisa`; worksKey `(absent)`; artistId `leonardo-da-vinci`. Evidence: same Commons asset `Mona Lisa, by Leonardo da Vinci, from C2RMF retouched.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg/500px-Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg`; page: `https://commons.wikimedia.org/wiki/File:Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg`.
- Checked-in route `p/artwork/mona-lisa.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg/500px-Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg`.

### 2. leonardo-da-vinci / The Last Supper

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `leonardo-da-vinci` → `The Last Supper`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/The_Last_Supper_-_Leonardo_Da_Vinci_-_High_Resolution_32x16.jpg/500px-The_Last_Supper_-_Leonardo_Da_Vinci_-_High_Resolution_32x16.jpg`; page: `https://en.wikipedia.org/wiki/The_Last_Supper_(Leonardo)`.
- Normalized gallery asset: `The Last Supper - Leonardo Da Vinci - High Resolution 32x16.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-last-supper`; title `The Last Supper`; worksKey `The Last Supper`; artistId `leonardo-da-vinci`. Evidence: same Commons asset `The Last Supper - Leonardo Da Vinci - High Resolution 32x16.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/The_Last_Supper_-_Leonardo_Da_Vinci_-_High_Resolution_32x16.jpg/500px-The_Last_Supper_-_Leonardo_Da_Vinci_-_High_Resolution_32x16.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Last_Supper_-_Leonardo_Da_Vinci_-_High_Resolution_32x16.jpg`.
- Checked-in route `p/artwork/the-last-supper.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/The_Last_Supper_-_Leonardo_Da_Vinci_-_High_Resolution_32x16.jpg/500px-The_Last_Supper_-_Leonardo_Da_Vinci_-_High_Resolution_32x16.jpg`.

### 3. leonardo-da-vinci / Lady with an Ermine

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `leonardo-da-vinci` → `Lady with an Ermine`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Lady_with_an_Ermine_-_Leonardo_da_Vinci_%28adjusted_levels%29.jpg/500px-Lady_with_an_Ermine_-_Leonardo_da_Vinci_%28adjusted_levels%29.jpg`; page: `https://en.wikipedia.org/wiki/Lady_with_an_Ermine`.
- Normalized gallery asset: `Lady with an Ermine - Leonardo da Vinci (adjusted levels).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `lady-with-an-ermine`; title `Lady with an Ermine`; worksKey `Lady with an Ermine`; artistId `leonardo-da-vinci`. Evidence: same Commons asset `Lady with an Ermine - Leonardo da Vinci (adjusted levels).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Lady_with_an_Ermine_-_Leonardo_da_Vinci_%28adjusted_levels%29.jpg/500px-Lady_with_an_Ermine_-_Leonardo_da_Vinci_%28adjusted_levels%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Lady_with_an_Ermine_-_Leonardo_da_Vinci_(adjusted_levels).jpg`.
- Checked-in route `p/artwork/lady-with-an-ermine.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Lady_with_an_Ermine_-_Leonardo_da_Vinci_%28adjusted_levels%29.jpg/500px-Lady_with_an_Ermine_-_Leonardo_da_Vinci_%28adjusted_levels%29.jpg`.

### 4. leonardo-da-vinci / Salvator Mundi

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `leonardo-da-vinci` → `Salvator Mundi`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Leonardo_da_Vinci%2C_Salvator_Mundi%2C_c.1500%2C_oil_on_walnut%2C_45.4_%C3%97_65.6_cm.jpg/500px-Leonardo_da_Vinci%2C_Salvator_Mundi%2C_c.1500%2C_oil_on_walnut%2C_45.4_%C3%97_65.6_cm.jpg`; page: `https://en.wikipedia.org/wiki/Salvator_Mundi_(painting)`.
- Normalized gallery asset: `Leonardo da Vinci, Salvator Mundi, c.1500, oil on walnut, 45.4 × 65.6 cm.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/leonardo-da-vinci`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 5. michelangelo / Sistine Chapel Ceiling

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `michelangelo` → `Sistine Chapel Ceiling`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Sistine_ceiling.jpg/500px-Sistine_ceiling.jpg`; page: `https://commons.wikimedia.org/wiki/File:Sistine_ceiling.jpg`.
- Normalized gallery asset: `Sistine ceiling.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `sistine-chapel-ceiling`; title `Sistine Chapel Ceiling`; worksKey `Sistine Chapel Ceiling`; artistId `michelangelo`. Evidence: same Commons asset `Sistine ceiling.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Sistine_ceiling.jpg/500px-Sistine_ceiling.jpg`; page: `https://commons.wikimedia.org/wiki/File:Sistine_ceiling.jpg`.
- Checked-in route `p/artwork/sistine-chapel-ceiling.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Sistine_ceiling.jpg/500px-Sistine_ceiling.jpg`.

### 6. michelangelo / The Last Judgment

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `michelangelo` → `The Last Judgment`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Last_Judgement_%28Michelangelo%29.jpg/500px-Last_Judgement_%28Michelangelo%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Last_Judgement_(Michelangelo).jpg`.
- Normalized gallery asset: `Last Judgement (Michelangelo).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-last-judgment`; title `The Last Judgment`; worksKey `The Last Judgment`; artistId `michelangelo`. Evidence: same Commons asset `Last Judgement (Michelangelo).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Last_Judgement_%28Michelangelo%29.jpg/500px-Last_Judgement_%28Michelangelo%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Last_Judgement_(Michelangelo).jpg`.
- Checked-in route `p/artwork/the-last-judgment.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Last_Judgement_%28Michelangelo%29.jpg/500px-Last_Judgement_%28Michelangelo%29.jpg`.

### 7. michelangelo / Doni Tondo

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `michelangelo` → `Doni Tondo`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Tondo_Doni%2C_por_Miguel_%C3%81ngel.jpg/500px-Tondo_Doni%2C_por_Miguel_%C3%81ngel.jpg`; page: `https://commons.wikimedia.org/wiki/File:Tondo_Doni,_por_Miguel_%C3%81ngel.jpg`.
- Normalized gallery asset: `Tondo Doni, por Miguel Ángel.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `doni-tondo`; title `Doni Tondo`; worksKey `Doni Tondo`; artistId `michelangelo`. Evidence: same Commons asset `Tondo Doni, por Miguel Ángel.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Tondo_Doni%2C_por_Miguel_%C3%81ngel.jpg/500px-Tondo_Doni%2C_por_Miguel_%C3%81ngel.jpg`; page: `https://commons.wikimedia.org/wiki/File:Tondo_Doni,_por_Miguel_%C3%81ngel.jpg`.
- Checked-in route `p/artwork/doni-tondo.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Tondo_Doni%2C_por_Miguel_%C3%81ngel.jpg/500px-Tondo_Doni%2C_por_Miguel_%C3%81ngel.jpg`.

### 8. raphael / The School of Athens

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `raphael` → `The School of Athens`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/%22The_School_of_Athens%22_by_Raffaello_Sanzio_da_Urbino.jpg/500px-%22The_School_of_Athens%22_by_Raffaello_Sanzio_da_Urbino.jpg`; page: `https://en.wikipedia.org/wiki/The_School_of_Athens`.
- Normalized gallery asset: `"The School of Athens" by Raffaello Sanzio da Urbino.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `the-school-of-athens`; title `The School of Athens`; worksKey `The School of Athens`; artistId `raphael`. Evidence: same Commons asset `"The School of Athens" by Raffaello Sanzio da Urbino.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/%22The_School_of_Athens%22_by_Raffaello_Sanzio_da_Urbino.jpg/500px-%22The_School_of_Athens%22_by_Raffaello_Sanzio_da_Urbino.jpg`; page: `https://commons.wikimedia.org/wiki/File:%22The_School_of_Athens%22_by_Raffaello_Sanzio_da_Urbino.jpg`.
- Checked-in route `p/artwork/the-school-of-athens.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/%22The_School_of_Athens%22_by_Raffaello_Sanzio_da_Urbino.jpg/500px-%22The_School_of_Athens%22_by_Raffaello_Sanzio_da_Urbino.jpg`.

### 9. raphael / Sistine Madonna

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `raphael` → `Sistine Madonna`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/RAFAEL_-_Madonna_Sixtina_%28Gem%C3%A4ldegalerie_Alter_Meister%2C_Dresden%2C_1513-14._%C3%93leo_sobre_lienzo%2C_265_x_196_cm%29.jpg/500px-RAFAEL_-_Madonna_Sixtina_%28Gem%C3%A4ldegalerie_Alter_Meister%2C_Dresden%2C_1513-14._%C3%93leo_sobre_lienzo%2C_265_x_196_cm%29.jpg`; page: `https://en.wikipedia.org/wiki/Sistine_Madonna`.
- Normalized gallery asset: `RAFAEL - Madonna Sixtina (Gemäldegalerie Alter Meister, Dresden, 1513-14. Óleo sobre lienzo, 265 x 196 cm).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `sistine-madonna`; title `Sistine Madonna`; worksKey `Sistine Madonna`; artistId `raphael`. Evidence: same Commons asset `RAFAEL - Madonna Sixtina (Gemäldegalerie Alter Meister, Dresden, 1513-14. Óleo sobre lienzo, 265 x 196 cm).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/RAFAEL_-_Madonna_Sixtina_%28Gem%C3%A4ldegalerie_Alter_Meister%2C_Dresden%2C_1513-14._%C3%93leo_sobre_lienzo%2C_265_x_196_cm%29.jpg/500px-RAFAEL_-_Madonna_Sixtina_%28Gem%C3%A4ldegalerie_Alter_Meister%2C_Dresden%2C_1513-14._%C3%93leo_sobre_lienzo%2C_265_x_196_cm%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:RAFAEL_-_Madonna_Sixtina_(Gem%C3%A4ldegalerie_Alter_Meister,_Dresden,_1513-14._%C3%93leo_sobre_lienzo,_265_x_196_cm).jpg`.
- Checked-in route `p/artwork/sistine-madonna.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/RAFAEL_-_Madonna_Sixtina_%28Gem%C3%A4ldegalerie_Alter_Meister%2C_Dresden%2C_1513-14._%C3%93leo_sobre_lienzo%2C_265_x_196_cm%29.jpg/500px-RAFAEL_-_Madonna_Sixtina_%28Gem%C3%A4ldegalerie_Alter_Meister%2C_Dresden%2C_1513-14._%C3%93leo_sobre_lienzo%2C_265_x_196_cm%29.jpg`.

### 10. raphael / La Fornarina

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `raphael` → `La Fornarina`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/La_Fornarina_by_Raffaello.jpg/500px-La_Fornarina_by_Raffaello.jpg`; page: `https://commons.wikimedia.org/wiki/File:La_Fornarina_by_Raffaello.jpg`.
- Normalized gallery asset: `La Fornarina by Raffaello.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `la-fornarina`; title `La Fornarina`; worksKey `La Fornarina`; artistId `raphael`. Evidence: same Commons asset `La Fornarina by Raffaello.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/La_Fornarina_by_Raffaello.jpg/500px-La_Fornarina_by_Raffaello.jpg`; page: `https://commons.wikimedia.org/wiki/File:La_Fornarina_by_Raffaello.jpg`.
- Checked-in route `p/artwork/la-fornarina.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/La_Fornarina_by_Raffaello.jpg/500px-La_Fornarina_by_Raffaello.jpg`.

### 11. titian / Assumption of the Virgin

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `titian` → `Assumption of the Virgin`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Tizian_041.jpg/500px-Tizian_041.jpg`; page: `https://en.wikipedia.org/wiki/Assumption_of_the_Virgin_(Titian)`.
- Normalized gallery asset: `Tizian 041.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/titian`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 12. titian / Venus of Urbino

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `titian` → `Venus of Urbino`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg/500px-Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Venus_of_Urbino`.
- Normalized gallery asset: `Tiziano - Venere di Urbino - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `venus-of-urbino`; title `Venus of Urbino`; worksKey `(absent)`; artistId `titian`. Evidence: same Commons asset `Tiziano - Venere di Urbino - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg/500px-Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/venus-of-urbino.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg/500px-Tiziano_-_Venere_di_Urbino_-_Google_Art_Project.jpg`.

### 13. titian / Bacchus and Ariadne

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `titian` → `Bacchus and Ariadne`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Titian_Bacchus_and_Ariadne.jpg/500px-Titian_Bacchus_and_Ariadne.jpg`; page: `https://en.wikipedia.org/wiki/Bacchus_and_Ariadne`.
- Normalized gallery asset: `Titian Bacchus and Ariadne.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/titian`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 14. tintoretto / The Miracle of the Slave

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `tintoretto` → `The Miracle of the Slave`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Tintoretto_-_Miracle_of_the_Slave.jpg/500px-Tintoretto_-_Miracle_of_the_Slave.jpg`; page: `https://en.wikipedia.org/wiki/Miracle_of_the_Slave_(Tintoretto)`.
- Normalized gallery asset: `Tintoretto - Miracle of the Slave.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-9.js` / `the-miracle-of-the-slave`; title `The Miracle of the Slave`; worksKey `(absent)`; artistId `tintoretto`. Evidence: same Commons asset `Tintoretto - Miracle of the Slave.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Tintoretto_-_Miracle_of_the_Slave.jpg/500px-Tintoretto_-_Miracle_of_the_Slave.jpg`; page: `https://commons.wikimedia.org/wiki/File:Tintoretto_-_Miracle_of_the_Slave.jpg`.
- Checked-in route `p/artwork/the-miracle-of-the-slave.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Tintoretto_-_Miracle_of_the_Slave.jpg/500px-Tintoretto_-_Miracle_of_the_Slave.jpg`.

### 15. tintoretto / The Last Supper (San Giorgio)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `tintoretto` → `The Last Supper (San Giorgio)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Jacopo_Tintoretto_-_The_Last_Supper_-_WGA22649.jpg/500px-Jacopo_Tintoretto_-_The_Last_Supper_-_WGA22649.jpg`; page: `https://en.wikipedia.org/wiki/Last_Supper_(Tintoretto)`.
- Normalized gallery asset: `Jacopo Tintoretto - The Last Supper - WGA22649.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/tintoretto`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 16. tintoretto / Paradise

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `tintoretto` → `Paradise`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/%28Venice%29_Jacopo_Tintoretto_-_Gloria_del_Paradiso_-_Sala_del_Maggior_Consiglio.jpg/500px-%28Venice%29_Jacopo_Tintoretto_-_Gloria_del_Paradiso_-_Sala_del_Maggior_Consiglio.jpg`; page: `https://commons.wikimedia.org/wiki/File:(Venice)_Jacopo_Tintoretto_-_Gloria_del_Paradiso_-_Sala_del_Maggior_Consiglio.jpg`.
- Normalized gallery asset: `(Venice) Jacopo Tintoretto - Gloria del Paradiso - Sala del Maggior Consiglio.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/tintoretto`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 17. paolo-veronese / The Wedding at Cana

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `paolo-veronese` → `The Wedding at Cana`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Paolo_Veronese_008.jpg/500px-Paolo_Veronese_008.jpg`; page: `https://en.wikipedia.org/wiki/The_Wedding_at_Cana_(Veronese)`.
- Normalized gallery asset: `Paolo Veronese 008.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/paolo-veronese`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 18. paolo-veronese / Feast in the House of Levi

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `paolo-veronese` → `Feast in the House of Levi`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/The_Feast_in_the_House_of_Levi_by_Paolo_Veronese_%28edited_2%29.jpg/500px-The_Feast_in_the_House_of_Levi_by_Paolo_Veronese_%28edited_2%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Feast_in_the_House_of_Levi`.
- Normalized gallery asset: `The Feast in the House of Levi by Paolo Veronese (edited 2).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/paolo-veronese`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 19. paolo-veronese / The Family of Darius before Alexander

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `paolo-veronese` → `The Family of Darius before Alexander`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/The_Family_of_Darius_before_Alexander_by_Paolo_Veronese_1570.jpg/500px-The_Family_of_Darius_before_Alexander_by_Paolo_Veronese_1570.jpg`; page: `https://en.wikipedia.org/wiki/The_Family_of_Darius_Before_Alexander`.
- Normalized gallery asset: `The Family of Darius before Alexander by Paolo Veronese 1570.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/paolo-veronese`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 20. albrecht-durer / Melencolia I

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `albrecht-durer` → `Melencolia I`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Albrecht_D%C3%BCrer_-_Melencolia_I_-_Google_Art_Project_%28_AGDdr3EHmNGyA%29.jpg/500px-Albrecht_D%C3%BCrer_-_Melencolia_I_-_Google_Art_Project_%28_AGDdr3EHmNGyA%29.jpg`; page: `https://en.wikipedia.org/wiki/Melencolia_I`.
- Normalized gallery asset: `Albrecht Dürer - Melencolia I - Google Art Project ( AGDdr3EHmNGyA).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `melencolia-i`; title `Melencolia I`; worksKey `Melencolia I`; artistId `albrecht-durer`. Evidence: same Commons asset `Albrecht Dürer - Melencolia I - Google Art Project ( AGDdr3EHmNGyA).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Albrecht_D%C3%BCrer_-_Melencolia_I_-_Google_Art_Project_%28_AGDdr3EHmNGyA%29.jpg/500px-Albrecht_D%C3%BCrer_-_Melencolia_I_-_Google_Art_Project_%28_AGDdr3EHmNGyA%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Albrecht_D%C3%BCrer_-_Melencolia_I_-_Google_Art_Project_(_AGDdr3EHmNGyA).jpg`.
- Checked-in route `p/artwork/melencolia-i.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Albrecht_D%C3%BCrer_-_Melencolia_I_-_Google_Art_Project_%28_AGDdr3EHmNGyA%29.jpg/500px-Albrecht_D%C3%BCrer_-_Melencolia_I_-_Google_Art_Project_%28_AGDdr3EHmNGyA%29.jpg`.

### 21. albrecht-durer / Young Hare

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `albrecht-durer` → `Young Hare`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Albrecht_D%C3%BCrer_-_Hare%2C_1502_-_Google_Art_Project.jpg/500px-Albrecht_D%C3%BCrer_-_Hare%2C_1502_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Young_Hare`.
- Normalized gallery asset: `Albrecht Dürer - Hare, 1502 - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `young-hare`; title `Young Hare`; worksKey `Young Hare`; artistId `albrecht-durer`. Evidence: same Commons asset `Albrecht Dürer - Hare, 1502 - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Albrecht_D%C3%BCrer_-_Hare%2C_1502_-_Google_Art_Project.jpg/500px-Albrecht_D%C3%BCrer_-_Hare%2C_1502_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Albrecht_D%C3%BCrer_-_Hare,_1502_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/young-hare.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Albrecht_D%C3%BCrer_-_Hare%2C_1502_-_Google_Art_Project.jpg/500px-Albrecht_D%C3%BCrer_-_Hare%2C_1502_-_Google_Art_Project.jpg`.

### 22. albrecht-durer / Self-Portrait at 28

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `albrecht-durer` → `Self-Portrait at 28`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Albrecht_D%C3%BCrer_-_1500_self-portrait_%28High_resolution_and_detail%29.jpg/500px-Albrecht_D%C3%BCrer_-_1500_self-portrait_%28High_resolution_and_detail%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Albrecht_D%C3%BCrer_-_1500_self-portrait_(High_resolution_and_detail).jpg`.
- Normalized gallery asset: `Albrecht Dürer - 1500 self-portrait (High resolution and detail).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `self-portrait-at-28`; title `Self-Portrait at Twenty-Eight`; worksKey `Self-Portrait at 28`; artistId `albrecht-durer`. Evidence: same Commons asset `Albrecht Dürer - 1500 self-portrait (High resolution and detail).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Albrecht_D%C3%BCrer_-_1500_self-portrait_%28High_resolution_and_detail%29.jpg/500px-Albrecht_D%C3%BCrer_-_1500_self-portrait_%28High_resolution_and_detail%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Albrecht_D%C3%BCrer_-_1500_self-portrait_(High_resolution_and_detail).jpg`.
- Checked-in route `p/artwork/self-portrait-at-28.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Albrecht_D%C3%BCrer_-_1500_self-portrait_%28High_resolution_and_detail%29.jpg/500px-Albrecht_D%C3%BCrer_-_1500_self-portrait_%28High_resolution_and_detail%29.jpg`.

### 23. albrecht-durer / Knight, Death and the Devil

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `albrecht-durer` → `Knight, Death and the Devil`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Albrecht_D%C3%BCrer%2C_Knight%2C_Death_and_Devil%2C_1513%2C_NGA_6637.jpg/500px-Albrecht_D%C3%BCrer%2C_Knight%2C_Death_and_Devil%2C_1513%2C_NGA_6637.jpg`; page: `https://en.wikipedia.org/wiki/Knight%2C_Death_and_the_Devil`.
- Normalized gallery asset: `Albrecht Dürer, Knight, Death and Devil, 1513, NGA 6637.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `knight-death-and-the-devil`; title `Knight, Death and the Devil`; worksKey `Knight, Death and the Devil`; artistId `albrecht-durer`. Evidence: same Commons asset `Albrecht Dürer, Knight, Death and Devil, 1513, NGA 6637.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Albrecht_D%C3%BCrer%2C_Knight%2C_Death_and_Devil%2C_1513%2C_NGA_6637.jpg/500px-Albrecht_D%C3%BCrer%2C_Knight%2C_Death_and_Devil%2C_1513%2C_NGA_6637.jpg`; page: `https://commons.wikimedia.org/wiki/File:Albrecht_D%C3%BCrer,_Knight,_Death_and_Devil,_1513,_NGA_6637.jpg`.
- Checked-in route `p/artwork/knight-death-and-the-devil.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Albrecht_D%C3%BCrer%2C_Knight%2C_Death_and_Devil%2C_1513%2C_NGA_6637.jpg/500px-Albrecht_D%C3%BCrer%2C_Knight%2C_Death_and_Devil%2C_1513%2C_NGA_6637.jpg`.

### 24. hans-holbein / The Ambassadors

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `hans-holbein` → `The Ambassadors`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Hans_Holbein_the_Younger_-_The_Ambassadors_-_Google_Art_Project.jpg/500px-Hans_Holbein_the_Younger_-_The_Ambassadors_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Ambassadors_(Holbein)`.
- Normalized gallery asset: `Hans Holbein the Younger - The Ambassadors - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-8.js` / `the-ambassadors`; title `The Ambassadors`; worksKey `(absent)`; artistId `hans-holbein`. Evidence: same Commons asset `Hans Holbein the Younger - The Ambassadors - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Hans_Holbein_the_Younger_-_The_Ambassadors_-_Google_Art_Project.jpg/500px-Hans_Holbein_the_Younger_-_The_Ambassadors_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hans_Holbein_the_Younger_-_The_Ambassadors_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/the-ambassadors.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Hans_Holbein_the_Younger_-_The_Ambassadors_-_Google_Art_Project.jpg/500px-Hans_Holbein_the_Younger_-_The_Ambassadors_-_Google_Art_Project.jpg`.

### 25. hans-holbein / Portrait of Henry VIII

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `hans-holbein` → `Portrait of Henry VIII`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Henry_VIII_of_England%2C_by_Hans_Holbein.jpg/500px-Henry_VIII_of_England%2C_by_Hans_Holbein.jpg`; page: `https://commons.wikimedia.org/wiki/File:Henry_VIII_of_England,_by_Hans_Holbein.jpg`.
- Normalized gallery asset: `Henry VIII of England, by Hans Holbein.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/hans-holbein`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 26. hans-holbein / Portrait of Erasmus

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `hans-holbein` → `Portrait of Erasmus`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Hans_Holbein_d._J._%28Werkstatt%29_-_Bildnis_des_Erasmus_von_Rotterdam_%28ca._1530%29.jpg/960px-Hans_Holbein_d._J._%28Werkstatt%29_-_Bildnis_des_Erasmus_von_Rotterdam_%28ca._1530%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hans_Holbein_d._J._(Werkstatt)_-_Bildnis_des_Erasmus_von_Rotterdam_(ca._1530).jpg`.
- Normalized gallery asset: `Hans Holbein d. J. (Werkstatt) - Bildnis des Erasmus von Rotterdam (ca. 1530).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/hans-holbein`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 27. pieter-bruegel / Hunters in the Snow

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `pieter-bruegel` → `Hunters in the Snow`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Pieter_Bruegel_the_Elder_-_Hunters_in_the_Snow_%28Winter%29_-_Google_Art_Project.jpg/500px-Pieter_Bruegel_the_Elder_-_Hunters_in_the_Snow_%28Winter%29_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Hunters_in_the_Snow`.
- Normalized gallery asset: `Pieter Bruegel the Elder - Hunters in the Snow (Winter) - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `hunters-in-the-snow`; title `The Hunters in the Snow`; worksKey `Hunters in the Snow`; artistId `pieter-bruegel`. Evidence: same Commons asset `Pieter Bruegel the Elder - Hunters in the Snow (Winter) - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Pieter_Bruegel_the_Elder_-_Hunters_in_the_Snow_%28Winter%29_-_Google_Art_Project.jpg/500px-Pieter_Bruegel_the_Elder_-_Hunters_in_the_Snow_%28Winter%29_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Pieter_Bruegel_the_Elder_-_Hunters_in_the_Snow_(Winter)_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/hunters-in-the-snow.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Pieter_Bruegel_the_Elder_-_Hunters_in_the_Snow_%28Winter%29_-_Google_Art_Project.jpg/500px-Pieter_Bruegel_the_Elder_-_Hunters_in_the_Snow_%28Winter%29_-_Google_Art_Project.jpg`.

### 28. pieter-bruegel / Netherlandish Proverbs

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `pieter-bruegel` → `Netherlandish Proverbs`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Pieter_Brueghel_the_Elder_-_The_Dutch_Proverbs_-_Google_Art_Project.jpg/500px-Pieter_Brueghel_the_Elder_-_The_Dutch_Proverbs_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Netherlandish_Proverbs`.
- Normalized gallery asset: `Pieter Brueghel the Elder - The Dutch Proverbs - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `netherlandish-proverbs`; title `Netherlandish Proverbs`; worksKey `Netherlandish Proverbs`; artistId `pieter-bruegel`. Evidence: same Commons asset `Pieter Brueghel the Elder - The Dutch Proverbs - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Pieter_Brueghel_the_Elder_-_The_Dutch_Proverbs_-_Google_Art_Project.jpg/500px-Pieter_Brueghel_the_Elder_-_The_Dutch_Proverbs_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Pieter_Brueghel_the_Elder_-_The_Dutch_Proverbs_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/netherlandish-proverbs.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Pieter_Brueghel_the_Elder_-_The_Dutch_Proverbs_-_Google_Art_Project.jpg/500px-Pieter_Brueghel_the_Elder_-_The_Dutch_Proverbs_-_Google_Art_Project.jpg`.

### 29. pieter-bruegel / The Tower of Babel

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `pieter-bruegel` → `The Tower of Babel`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Pieter_Bruegel_the_Elder_-_The_Tower_of_Babel_%28Vienna%29_-_Google_Art_Project_-_edited.jpg/960px-Pieter_Bruegel_the_Elder_-_The_Tower_of_Babel_%28Vienna%29_-_Google_Art_Project_-_edited.jpg`; page: `https://commons.wikimedia.org/wiki/File:Pieter_Bruegel_the_Elder_-_The_Tower_of_Babel_(Vienna)_-_Google_Art_Project_-_edited.jpg`.
- Normalized gallery asset: `Pieter Bruegel the Elder - The Tower of Babel (Vienna) - Google Art Project - edited.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `the-tower-of-babel`; title `The Tower of Babel`; worksKey `The Tower of Babel`; artistId `pieter-bruegel`. Evidence: same Commons asset `Pieter Bruegel the Elder - The Tower of Babel (Vienna) - Google Art Project - edited.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Pieter_Bruegel_the_Elder_-_The_Tower_of_Babel_%28Vienna%29_-_Google_Art_Project_-_edited.jpg/960px-Pieter_Bruegel_the_Elder_-_The_Tower_of_Babel_%28Vienna%29_-_Google_Art_Project_-_edited.jpg`; page: `https://commons.wikimedia.org/wiki/File:Pieter_Bruegel_the_Elder_-_The_Tower_of_Babel_(Vienna)_-_Google_Art_Project_-_edited.jpg`.
- Checked-in route `p/artwork/the-tower-of-babel.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Pieter_Bruegel_the_Elder_-_The_Tower_of_Babel_%28Vienna%29_-_Google_Art_Project_-_edited.jpg/960px-Pieter_Bruegel_the_Elder_-_The_Tower_of_Babel_%28Vienna%29_-_Google_Art_Project_-_edited.jpg`.

### 30. hieronymus-bosch / The Garden of Earthly Delights

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `hieronymus-bosch` → `The Garden of Earthly Delights`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/The_Garden_of_Earthly_Delights_by_Bosch_High_Resolution.jpg/500px-The_Garden_of_Earthly_Delights_by_Bosch_High_Resolution.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Garden_of_Earthly_Delights_by_Bosch_High_Resolution.jpg`.
- Normalized gallery asset: `The Garden of Earthly Delights by Bosch High Resolution.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-garden-of-earthly-delights`; title `The Garden of Earthly Delights`; worksKey `(absent)`; artistId `hieronymus-bosch`. Evidence: same Commons asset `The Garden of Earthly Delights by Bosch High Resolution.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/The_Garden_of_Earthly_Delights_by_Bosch_High_Resolution.jpg/500px-The_Garden_of_Earthly_Delights_by_Bosch_High_Resolution.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Garden_of_Earthly_Delights_by_Bosch_High_Resolution.jpg`.
- Checked-in route `p/artwork/the-garden-of-earthly-delights.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/The_Garden_of_Earthly_Delights_by_Bosch_High_Resolution.jpg/500px-The_Garden_of_Earthly_Delights_by_Bosch_High_Resolution.jpg`.

### 31. hieronymus-bosch / The Haywain Triptych

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `hieronymus-bosch` → `The Haywain Triptych`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bosch_-_Haywain_Triptych.jpg/500px-Bosch_-_Haywain_Triptych.jpg`; page: `https://en.wikipedia.org/wiki/The_Haywain_Triptych`.
- Normalized gallery asset: `Bosch - Haywain Triptych.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-haywain-triptych`; title `The Haywain Triptych`; worksKey `The Haywain Triptych`; artistId `hieronymus-bosch`. Evidence: same Commons asset `Bosch - Haywain Triptych.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bosch_-_Haywain_Triptych.jpg/500px-Bosch_-_Haywain_Triptych.jpg`; page: `https://commons.wikimedia.org/wiki/File:Bosch_-_Haywain_Triptych.jpg`.
- Checked-in route `p/artwork/the-haywain-triptych.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Bosch_-_Haywain_Triptych.jpg/500px-Bosch_-_Haywain_Triptych.jpg`.

### 32. hieronymus-bosch / The Temptation of St Anthony

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `hieronymus-bosch` → `The Temptation of St Anthony`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/The_Temptation_of_St_Anthony_%28Bosch%29.jpg/500px-The_Temptation_of_St_Anthony_%28Bosch%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Temptation_of_St_Anthony_(Bosch)`.
- Normalized gallery asset: `The Temptation of St Anthony (Bosch).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `temptation-of-saint-anthony`; title `The Temptation of St Anthony`; worksKey `The Temptation of St Anthony`; artistId `hieronymus-bosch`. Evidence: same Commons asset `The Temptation of St Anthony (Bosch).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/The_Temptation_of_St_Anthony_%28Bosch%29.jpg/500px-The_Temptation_of_St_Anthony_%28Bosch%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Temptation_of_St_Anthony_(Bosch).jpg`.
- Checked-in route `p/artwork/temptation-of-saint-anthony.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/The_Temptation_of_St_Anthony_%28Bosch%29.jpg/500px-The_Temptation_of_St_Anthony_%28Bosch%29.jpg`.

### 33. el-greco / The Burial of the Count of Orgaz

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `el-greco` → `The Burial of the Count of Orgaz`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/El_Greco_-_The_Burial_of_the_Count_of_Orgaz.JPG/500px-El_Greco_-_The_Burial_of_the_Count_of_Orgaz.JPG`; page: `https://en.wikipedia.org/wiki/The_Burial_of_the_Count_of_Orgaz`.
- Normalized gallery asset: `El Greco - The Burial of the Count of Orgaz.JPG`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `burial-of-the-count-of-orgaz`; title `The Burial of the Count of Orgaz`; worksKey `The Burial of the Count of Orgaz`; artistId `el-greco`. Evidence: same Commons asset `El Greco - The Burial of the Count of Orgaz.JPG`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/El_Greco_-_The_Burial_of_the_Count_of_Orgaz.JPG/500px-El_Greco_-_The_Burial_of_the_Count_of_Orgaz.JPG`; page: `https://commons.wikimedia.org/wiki/File:El_Greco_-_The_Burial_of_the_Count_of_Orgaz.JPG`.
- Checked-in route `p/artwork/burial-of-the-count-of-orgaz.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/El_Greco_-_The_Burial_of_the_Count_of_Orgaz.JPG/500px-El_Greco_-_The_Burial_of_the_Count_of_Orgaz.JPG`.

### 34. el-greco / View of Toledo

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `el-greco` → `View of Toledo`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/El_Greco_View_of_Toledo.jpg/500px-El_Greco_View_of_Toledo.jpg`; page: `https://en.wikipedia.org/wiki/View_of_Toledo`.
- Normalized gallery asset: `El Greco View of Toledo.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `view-of-toledo`; title `View of Toledo`; worksKey `View of Toledo`; artistId `el-greco`. Evidence: same Commons asset `El Greco View of Toledo.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/El_Greco_View_of_Toledo.jpg/500px-El_Greco_View_of_Toledo.jpg`; page: `https://commons.wikimedia.org/wiki/File:El_Greco_View_of_Toledo.jpg`.
- Checked-in route `p/artwork/view-of-toledo.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/El_Greco_View_of_Toledo.jpg/500px-El_Greco_View_of_Toledo.jpg`.

### 35. el-greco / The Opening of the Fifth Seal

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `el-greco` → `The Opening of the Fifth Seal`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/El_Greco%2C_The_Vision_of_Saint_John_%281608-1614%29.jpg/500px-El_Greco%2C_The_Vision_of_Saint_John_%281608-1614%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:El_Greco,_The_Vision_of_Saint_John_(1608-1614).jpg`.
- Normalized gallery asset: `El Greco, The Vision of Saint John (1608-1614).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `the-opening-of-the-fifth-seal`; title `The Opening of the Fifth Seal`; worksKey `The Opening of the Fifth Seal`; artistId `el-greco`. Evidence: same Commons asset `El Greco, The Vision of Saint John (1608-1614).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/El_Greco%2C_The_Vision_of_Saint_John_%281608-1614%29.jpg/500px-El_Greco%2C_The_Vision_of_Saint_John_%281608-1614%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:El_Greco,_The_Vision_of_Saint_John_(1608-1614).jpg`.
- Checked-in route `p/artwork/the-opening-of-the-fifth-seal.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/El_Greco%2C_The_Vision_of_Saint_John_%281608-1614%29.jpg/500px-El_Greco%2C_The_Vision_of_Saint_John_%281608-1614%29.jpg`.

### 36. sofonisba-anguissola / The Chess Game

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `sofonisba-anguissola` → `The Chess Game`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/The_Chess_Game_%28Sofonisba_Anguissola%29_1555_%284096x3236px%29.jpg/500px-The_Chess_Game_%28Sofonisba_Anguissola%29_1555_%284096x3236px%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Chess_Game_(Sofonisba_Anguissola)_1555_(4096x3236px).jpg`.
- Normalized gallery asset: `The Chess Game (Sofonisba Anguissola) 1555 (4096x3236px).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-9.js` / `the-chess-game`; title `The Chess Game`; worksKey `(absent)`; artistId `sofonisba-anguissola`. Evidence: same Commons asset `The Chess Game (Sofonisba Anguissola) 1555 (4096x3236px).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/The_Chess_Game_%28Sofonisba_Anguissola%29_1555_%284096x3236px%29.jpg/500px-The_Chess_Game_%28Sofonisba_Anguissola%29_1555_%284096x3236px%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Chess_Game_(Sofonisba_Anguissola)_1555_(4096x3236px).jpg`.
- Checked-in route `p/artwork/the-chess-game.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/The_Chess_Game_%28Sofonisba_Anguissola%29_1555_%284096x3236px%29.jpg/500px-The_Chess_Game_%28Sofonisba_Anguissola%29_1555_%284096x3236px%29.jpg`.

### 37. sofonisba-anguissola / Self-Portrait at the Easel

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `sofonisba-anguissola` → `Self-Portrait at the Easel`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Self-Portait_at_the_Easel_%28Sofonisba_Anguissola%29-WUS09909.jpg/960px-Self-Portait_at_the_Easel_%28Sofonisba_Anguissola%29-WUS09909.jpg`; page: `https://commons.wikimedia.org/wiki/File:Self-Portait_at_the_Easel_(Sofonisba_Anguissola)-WUS09909.jpg`.
- Normalized gallery asset: `Self-Portait at the Easel (Sofonisba Anguissola)-WUS09909.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/sofonisba-anguissola`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 38. sofonisba-anguissola / Portrait of Philip II

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `sofonisba-anguissola` → `Portrait of Philip II`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Portrait_of_Philip_II_of_Spain_by_Sofonisba_Anguissola_-_002b.jpg/500px-Portrait_of_Philip_II_of_Spain_by_Sofonisba_Anguissola_-_002b.jpg`; page: `https://commons.wikimedia.org/wiki/File:Portrait_of_Philip_II_of_Spain_by_Sofonisba_Anguissola_-_002b.jpg`.
- Normalized gallery asset: `Portrait of Philip II of Spain by Sofonisba Anguissola - 002b.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/sofonisba-anguissola`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 39. giuseppe-arcimboldo / Vertumnus

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giuseppe-arcimboldo` → `Vertumnus`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Vertumnus_%C3%A5rstidernas_gud_m%C3%A5lad_av_Giuseppe_Arcimboldo_1591_-_Skoklosters_slott_-_91503.jpg/500px-Vertumnus_%C3%A5rstidernas_gud_m%C3%A5lad_av_Giuseppe_Arcimboldo_1591_-_Skoklosters_slott_-_91503.jpg`; page: `https://en.wikipedia.org/wiki/Vertumnus_(Arcimboldo)`.
- Normalized gallery asset: `Vertumnus årstidernas gud målad av Giuseppe Arcimboldo 1591 - Skoklosters slott - 91503.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giuseppe-arcimboldo`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 40. giuseppe-arcimboldo / The Four Seasons

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giuseppe-arcimboldo` → `The Four Seasons`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Arcimboldo_-_Les_saisons_-_Le_printemps_-_Sans_cadre.jpg/500px-Arcimboldo_-_Les_saisons_-_Le_printemps_-_Sans_cadre.jpg`; page: `https://en.wikipedia.org/wiki/The_Four_Seasons_(Arcimboldo)`.
- Normalized gallery asset: `Arcimboldo - Les saisons - Le printemps - Sans cadre.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giuseppe-arcimboldo`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 41. giuseppe-arcimboldo / The Librarian

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giuseppe-arcimboldo` → `The Librarian`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Bibliotekarien_konserverad_-_Skoklosters_slott_-_97136.tif/lossy-page1-330px-Bibliotekarien_konserverad_-_Skoklosters_slott_-_97136.tif.jpg`; page: `https://en.wikipedia.org/wiki/The_Librarian_(Arcimboldo)`.
- Normalized gallery asset: `Bibliotekarien konserverad - Skoklosters slott - 97136.tif`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giuseppe-arcimboldo`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 42. caravaggio / The Calling of St Matthew

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `caravaggio` → `The Calling of St Matthew`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Caravaggio_%E2%80%94_The_Calling_of_Saint_Matthew.jpg/500px-Caravaggio_%E2%80%94_The_Calling_of_Saint_Matthew.jpg`; page: `https://en.wikipedia.org/wiki/The_Calling_of_Saint_Matthew`.
- Normalized gallery asset: `Caravaggio — The Calling of Saint Matthew.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-calling-of-saint-matthew`; title `The Calling of Saint Matthew`; worksKey `The Calling of St Matthew`; artistId `caravaggio`. Evidence: same Commons asset `Caravaggio — The Calling of Saint Matthew.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Caravaggio_%E2%80%94_The_Calling_of_Saint_Matthew.jpg/500px-Caravaggio_%E2%80%94_The_Calling_of_Saint_Matthew.jpg`; page: `https://commons.wikimedia.org/wiki/File:Caravaggio_%E2%80%94_The_Calling_of_Saint_Matthew.jpg`.
- Checked-in route `p/artwork/the-calling-of-saint-matthew.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Caravaggio_%E2%80%94_The_Calling_of_Saint_Matthew.jpg/500px-Caravaggio_%E2%80%94_The_Calling_of_Saint_Matthew.jpg`.

### 43. caravaggio / Judith Beheading Holofernes

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `caravaggio` → `Judith Beheading Holofernes`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Judith_Beheading_Holofernes-Caravaggio_%28c.1598-9%29.jpg/500px-Judith_Beheading_Holofernes-Caravaggio_%28c.1598-9%29.jpg`; page: `https://en.wikipedia.org/wiki/Judith_Beheading_Holofernes_(Caravaggio)`.
- Normalized gallery asset: `Judith Beheading Holofernes-Caravaggio (c.1598-9).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `judith-beheading-holofernes`; title `Judith Beheading Holofernes`; worksKey `Judith Beheading Holofernes`; artistId `caravaggio`. Evidence: same Commons asset `Judith Beheading Holofernes-Caravaggio (c.1598-9).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Judith_Beheading_Holofernes-Caravaggio_%28c.1598-9%29.jpg/500px-Judith_Beheading_Holofernes-Caravaggio_%28c.1598-9%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Judith_Beheading_Holofernes-Caravaggio_(c.1598-9).jpg`.
- Checked-in route `p/artwork/judith-beheading-holofernes.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Judith_Beheading_Holofernes-Caravaggio_%28c.1598-9%29.jpg/500px-Judith_Beheading_Holofernes-Caravaggio_%28c.1598-9%29.jpg`.

### 44. caravaggio / David with the Head of Goliath

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `caravaggio` → `David with the Head of Goliath`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/David_with_the_Head_of_Goliath-Caravaggio_%281610%29.jpg/500px-David_with_the_Head_of_Goliath-Caravaggio_%281610%29.jpg`; page: `https://en.wikipedia.org/wiki/David_with_the_Head_of_Goliath_(Caravaggio)`.
- Normalized gallery asset: `David with the Head of Goliath-Caravaggio (1610).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `david-with-the-head-of-goliath`; title `David with the Head of Goliath`; worksKey `David with the Head of Goliath`; artistId `caravaggio`. Evidence: same Commons asset `David with the Head of Goliath-Caravaggio (1610).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/David_with_the_Head_of_Goliath-Caravaggio_%281610%29.jpg/500px-David_with_the_Head_of_Goliath-Caravaggio_%281610%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:David_with_the_Head_of_Goliath-Caravaggio_(1610).jpg`.
- Checked-in route `p/artwork/david-with-the-head-of-goliath.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/David_with_the_Head_of_Goliath-Caravaggio_%281610%29.jpg/500px-David_with_the_Head_of_Goliath-Caravaggio_%281610%29.jpg`.

### 45. artemisia-gentileschi / Judith Slaying Holofernes

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `artemisia-gentileschi` → `Judith Slaying Holofernes`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Judit_decapitando_a_Holofernes%2C_por_Artemisia_Gentileschi.jpg/500px-Judit_decapitando_a_Holofernes%2C_por_Artemisia_Gentileschi.jpg`; page: `https://en.wikipedia.org/wiki/Judith_beheading_Holofernes`.
- Normalized gallery asset: `Judit decapitando a Holofernes, por Artemisia Gentileschi.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `judith-slaying-holofernes`; title `Judith Slaying Holofernes`; worksKey `(absent)`; artistId `artemisia-gentileschi`. Evidence: same Commons asset `Judit decapitando a Holofernes, por Artemisia Gentileschi.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Judit_decapitando_a_Holofernes%2C_por_Artemisia_Gentileschi.jpg/500px-Judit_decapitando_a_Holofernes%2C_por_Artemisia_Gentileschi.jpg`; page: `https://commons.wikimedia.org/wiki/File:Judit_decapitando_a_Holofernes,_por_Artemisia_Gentileschi.jpg`.
- Checked-in route `p/artwork/judith-slaying-holofernes.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Judit_decapitando_a_Holofernes%2C_por_Artemisia_Gentileschi.jpg/500px-Judit_decapitando_a_Holofernes%2C_por_Artemisia_Gentileschi.jpg`.

### 46. artemisia-gentileschi / Self-Portrait as the Allegory of Painting

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `artemisia-gentileschi` → `Self-Portrait as the Allegory of Painting`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Self-portrait_as_the_Allegory_of_Painting_%28La_Pittura%29_-_Artemisia_Gentileschi.jpg/500px-Self-portrait_as_the_Allegory_of_Painting_%28La_Pittura%29_-_Artemisia_Gentileschi.jpg`; page: `https://en.wikipedia.org/wiki/Self-Portrait_as_the_Allegory_of_Painting`.
- Normalized gallery asset: `Self-portrait as the Allegory of Painting (La Pittura) - Artemisia Gentileschi.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `self-portrait-as-the-allegory-of-painting`; title `Self-Portrait as the Allegory of Painting`; worksKey `Self-Portrait as the Allegory of Painting`; artistId `artemisia-gentileschi`. Evidence: same Commons asset `Self-portrait as the Allegory of Painting (La Pittura) - Artemisia Gentileschi.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Self-portrait_as_the_Allegory_of_Painting_%28La_Pittura%29_-_Artemisia_Gentileschi.jpg/500px-Self-portrait_as_the_Allegory_of_Painting_%28La_Pittura%29_-_Artemisia_Gentileschi.jpg`; page: `https://commons.wikimedia.org/wiki/File:Self-portrait_as_the_Allegory_of_Painting_(La_Pittura)_-_Artemisia_Gentileschi.jpg`.
- Checked-in route `p/artwork/self-portrait-as-the-allegory-of-painting.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Self-portrait_as_the_Allegory_of_Painting_%28La_Pittura%29_-_Artemisia_Gentileschi.jpg/500px-Self-portrait_as_the_Allegory_of_Painting_%28La_Pittura%29_-_Artemisia_Gentileschi.jpg`.

### 47. artemisia-gentileschi / Judith and her Maidservant

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `artemisia-gentileschi` → `Judith and her Maidservant`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Artemisia_Gentileschi_Judith_Maidservant_DIA.jpg/960px-Artemisia_Gentileschi_Judith_Maidservant_DIA.jpg`; page: `https://commons.wikimedia.org/wiki/File:Artemisia_Gentileschi_Judith_Maidservant_DIA.jpg`.
- Normalized gallery asset: `Artemisia Gentileschi Judith Maidservant DIA.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `judith-and-her-maidservant-detroit`; title `Judith and Her Maidservant with the Head of Holofernes`; worksKey `Judith and her Maidservant`; artistId `artemisia-gentileschi`. Evidence: same Commons asset `Artemisia Gentileschi Judith Maidservant DIA.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Artemisia_Gentileschi_Judith_Maidservant_DIA.jpg/960px-Artemisia_Gentileschi_Judith_Maidservant_DIA.jpg`; page: `https://commons.wikimedia.org/wiki/File:Artemisia_Gentileschi_Judith_Maidservant_DIA.jpg`.
- Checked-in route `p/artwork/judith-and-her-maidservant-detroit.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Artemisia_Gentileschi_Judith_Maidservant_DIA.jpg/960px-Artemisia_Gentileschi_Judith_Maidservant_DIA.jpg`.

### 48. peter-paul-rubens / The Descent from the Cross

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `peter-paul-rubens` → `The Descent from the Cross`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Peter_Paul_Rubens_-_Descent_from_the_cross_%281617%29.jpg/960px-Peter_Paul_Rubens_-_Descent_from_the_cross_%281617%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Peter_Paul_Rubens_-_Descent_from_the_cross_(1617).jpg`.
- Normalized gallery asset: `Peter Paul Rubens - Descent from the cross (1617).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/peter-paul-rubens`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 49. peter-paul-rubens / The Marie de' Medici Cycle

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `peter-paul-rubens` → `The Marie de' Medici Cycle`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/The_Felicity_of_the_Regency_%28Skizze_zum_Medici-Zyklus%29_-_Peter_Paul_Rubens.jpg/960px-The_Felicity_of_the_Regency_%28Skizze_zum_Medici-Zyklus%29_-_Peter_Paul_Rubens.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Felicity_of_the_Regency_(Skizze_zum_Medici-Zyklus)_-_Peter_Paul_Rubens.jpg`.
- Normalized gallery asset: `The Felicity of the Regency (Skizze zum Medici-Zyklus) - Peter Paul Rubens.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/peter-paul-rubens`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 50. peter-paul-rubens / The Garden of Love

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `peter-paul-rubens` → `The Garden of Love`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/El_Jard%C3%ADn_del_Amor_%28Rubens%29.jpg/500px-El_Jard%C3%ADn_del_Amor_%28Rubens%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Garden_of_Love_(Rubens)`.
- Normalized gallery asset: `El Jardín del Amor (Rubens).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-6.js` / `the-garden-of-love`; title `The Garden of Love`; worksKey `(absent)`; artistId `peter-paul-rubens`. Evidence: same Commons asset `El Jardín del Amor (Rubens).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/El_Jard%C3%ADn_del_Amor_%28Rubens%29.jpg/500px-El_Jard%C3%ADn_del_Amor_%28Rubens%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:El_Jard%C3%ADn_del_Amor_(Rubens).jpg`.
- Checked-in route `p/artwork/the-garden-of-love.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/El_Jard%C3%ADn_del_Amor_%28Rubens%29.jpg/500px-El_Jard%C3%ADn_del_Amor_%28Rubens%29.jpg`.

### 51. anthony-van-dyck / Charles I at the Hunt

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `anthony-van-dyck` → `Charles I at the Hunt`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Portrait_de_Charles_1er%2C_roi_d%27Angleterre%2C_%C3%A0_la_chasse_-_Antoon_van_Dyck_-_Mus%C3%A9e_du_Louvre_Peintures_INV_1236_%3B_MR_666.jpg/500px-Portrait_de_Charles_1er%2C_roi_d%27Angleterre%2C_%C3%A0_la_chasse_-_Antoon_van_Dyck_-_Mus%C3%A9e_du_Louvre_Peintures_INV_1236_%3B_MR_666.jpg`; page: `https://en.wikipedia.org/wiki/Charles_I_at_the_Hunt`.
- Normalized gallery asset: `Portrait de Charles 1er, roi d'Angleterre, à la chasse - Antoon van Dyck - Musée du Louvre Peintures INV 1236 ; MR 666.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-6.js` / `charles-i-at-the-hunt`; title `Charles I at the Hunt`; worksKey `(absent)`; artistId `anthony-van-dyck`. Evidence: same Commons asset `Portrait de Charles 1er, roi d'Angleterre, à la chasse - Antoon van Dyck - Musée du Louvre Peintures INV 1236 ; MR 666.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Portrait_de_Charles_1er%2C_roi_d%27Angleterre%2C_%C3%A0_la_chasse_-_Antoon_van_Dyck_-_Mus%C3%A9e_du_Louvre_Peintures_INV_1236_%3B_MR_666.jpg/500px-Portrait_de_Charles_1er%2C_roi_d%27Angleterre%2C_%C3%A0_la_chasse_-_Antoon_van_Dyck_-_Mus%C3%A9e_du_Louvre_Peintures_INV_1236_%3B_MR_666.jpg`; page: `https://commons.wikimedia.org/wiki/File:Portrait_de_Charles_1er,_roi_d%27Angleterre,_%C3%A0_la_chasse_-_Antoon_van_Dyck_-_Mus%C3%A9e_du_Louvre_Peintures_INV_1236_;_MR_666.jpg`.
- Checked-in route `p/artwork/charles-i-at-the-hunt.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Portrait_de_Charles_1er%2C_roi_d%27Angleterre%2C_%C3%A0_la_chasse_-_Antoon_van_Dyck_-_Mus%C3%A9e_du_Louvre_Peintures_INV_1236_%3B_MR_666.jpg/500px-Portrait_de_Charles_1er%2C_roi_d%27Angleterre%2C_%C3%A0_la_chasse_-_Antoon_van_Dyck_-_Mus%C3%A9e_du_Louvre_Peintures_INV_1236_%3B_MR_666.jpg`.

### 52. anthony-van-dyck / Equestrian Portrait of Charles I

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `anthony-van-dyck` → `Equestrian Portrait of Charles I`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Anthonis_van_Dyck_-_Equestrian_Portrait_of_Charles_I_-_National_Gallery%2C_London.jpg/500px-Anthonis_van_Dyck_-_Equestrian_Portrait_of_Charles_I_-_National_Gallery%2C_London.jpg`; page: `https://en.wikipedia.org/wiki/Equestrian_Portrait_of_Charles_I`.
- Normalized gallery asset: `Anthonis van Dyck - Equestrian Portrait of Charles I - National Gallery, London.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/anthony-van-dyck`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 53. anthony-van-dyck / Self-Portrait with a Sunflower

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `anthony-van-dyck` → `Self-Portrait with a Sunflower`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Anthony_van_Dyck_-_Self-portrait_with_a_Sunflower.jpg/500px-Anthony_van_Dyck_-_Self-portrait_with_a_Sunflower.jpg`; page: `https://en.wikipedia.org/wiki/Self-Portrait_with_a_Sunflower`.
- Normalized gallery asset: `Anthony van Dyck - Self-portrait with a Sunflower.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/anthony-van-dyck`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 54. rembrandt / The Night Watch

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `rembrandt` → `The Night Watch`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/La_ronda_de_noche%2C_por_Rembrandt_van_Rijn.jpg/500px-La_ronda_de_noche%2C_por_Rembrandt_van_Rijn.jpg`; page: `https://en.wikipedia.org/wiki/The_Night_Watch`.
- Normalized gallery asset: `La ronda de noche, por Rembrandt van Rijn.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-night-watch`; title `The Night Watch`; worksKey `The Night Watch`; artistId `rembrandt`. Evidence: same Commons asset `La ronda de noche, por Rembrandt van Rijn.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/La_ronda_de_noche%2C_por_Rembrandt_van_Rijn.jpg/500px-La_ronda_de_noche%2C_por_Rembrandt_van_Rijn.jpg`; page: `https://commons.wikimedia.org/wiki/File:La_ronda_de_noche,_por_Rembrandt_van_Rijn.jpg`.
- Checked-in route `p/artwork/the-night-watch.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/La_ronda_de_noche%2C_por_Rembrandt_van_Rijn.jpg/500px-La_ronda_de_noche%2C_por_Rembrandt_van_Rijn.jpg`.

### 55. rembrandt / Self-Portrait with Two Circles

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `rembrandt` → `Self-Portrait with Two Circles`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Rembrandt_Self-portrait_%28Kenwood%29.jpg/500px-Rembrandt_Self-portrait_%28Kenwood%29.jpg`; page: `https://en.wikipedia.org/wiki/Self-Portrait_with_Two_Circles`.
- Normalized gallery asset: `Rembrandt Self-portrait (Kenwood).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `self-portrait-with-two-circles`; title `Self-Portrait with Two Circles`; worksKey `Self-Portrait with Two Circles`; artistId `rembrandt`. Evidence: same Commons asset `Rembrandt Self-portrait (Kenwood).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Rembrandt_Self-portrait_%28Kenwood%29.jpg/500px-Rembrandt_Self-portrait_%28Kenwood%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Rembrandt_Self-portrait_(Kenwood).jpg`.
- Checked-in route `p/artwork/self-portrait-with-two-circles.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Rembrandt_Self-portrait_%28Kenwood%29.jpg/500px-Rembrandt_Self-portrait_%28Kenwood%29.jpg`.

### 56. rembrandt / The Jewish Bride

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `rembrandt` → `The Jewish Bride`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Rembrandt_Harmensz._van_Rijn_-_Portret_van_een_paar_als_oudtestamentische_figuren%2C_genaamd_%27Het_Joodse_bruidje%27_-_Google_Art_Project.jpg/500px-Rembrandt_Harmensz._van_Rijn_-_Portret_van_een_paar_als_oudtestamentische_figuren%2C_genaamd_%27Het_Joodse_bruidje%27_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Jewish_Bride`.
- Normalized gallery asset: `Rembrandt Harmensz. van Rijn - Portret van een paar als oudtestamentische figuren, genaamd 'Het Joodse bruidje' - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-jewish-bride`; title `The Jewish Bride`; worksKey `The Jewish Bride`; artistId `rembrandt`. Evidence: same Commons asset `Rembrandt Harmensz. van Rijn - Portret van een paar als oudtestamentische figuren, genaamd 'Het Joodse bruidje' - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Rembrandt_Harmensz._van_Rijn_-_Portret_van_een_paar_als_oudtestamentische_figuren%2C_genaamd_%27Het_Joodse_bruidje%27_-_Google_Art_Project.jpg/500px-Rembrandt_Harmensz._van_Rijn_-_Portret_van_een_paar_als_oudtestamentische_figuren%2C_genaamd_%27Het_Joodse_bruidje%27_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Rembrandt_Harmensz._van_Rijn_-_Portret_van_een_paar_als_oudtestamentische_figuren,_genaamd_%27Het_Joodse_bruidje%27_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/the-jewish-bride.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Rembrandt_Harmensz._van_Rijn_-_Portret_van_een_paar_als_oudtestamentische_figuren%2C_genaamd_%27Het_Joodse_bruidje%27_-_Google_Art_Project.jpg/500px-Rembrandt_Harmensz._van_Rijn_-_Portret_van_een_paar_als_oudtestamentische_figuren%2C_genaamd_%27Het_Joodse_bruidje%27_-_Google_Art_Project.jpg`.

### 57. rembrandt / The Anatomy Lesson of Dr Tulp

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `rembrandt` → `The Anatomy Lesson of Dr Tulp`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Rembrandt_-_The_Anatomy_Lesson_of_Dr_Nicolaes_Tulp.jpg/960px-Rembrandt_-_The_Anatomy_Lesson_of_Dr_Nicolaes_Tulp.jpg`; page: `https://commons.wikimedia.org/wiki/File:Rembrandt_-_The_Anatomy_Lesson_of_Dr_Nicolaes_Tulp.jpg`.
- Normalized gallery asset: `Rembrandt - The Anatomy Lesson of Dr Nicolaes Tulp.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-anatomy-lesson`; title `The Anatomy Lesson of Dr Nicolaes Tulp`; worksKey `The Anatomy Lesson of Dr Tulp`; artistId `rembrandt`. Evidence: same Commons asset `Rembrandt - The Anatomy Lesson of Dr Nicolaes Tulp.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Rembrandt_-_The_Anatomy_Lesson_of_Dr_Nicolaes_Tulp.jpg/960px-Rembrandt_-_The_Anatomy_Lesson_of_Dr_Nicolaes_Tulp.jpg`; page: `https://commons.wikimedia.org/wiki/File:Rembrandt_-_The_Anatomy_Lesson_of_Dr_Nicolaes_Tulp.jpg`.
- Checked-in route `p/artwork/the-anatomy-lesson.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Rembrandt_-_The_Anatomy_Lesson_of_Dr_Nicolaes_Tulp.jpg/960px-Rembrandt_-_The_Anatomy_Lesson_of_Dr_Nicolaes_Tulp.jpg`.

### 58. johannes-vermeer / Girl with a Pearl Earring

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `johannes-vermeer` → `Girl with a Pearl Earring`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/1665_Girl_with_a_Pearl_Earring.jpg/500px-1665_Girl_with_a_Pearl_Earring.jpg`; page: `https://en.wikipedia.org/wiki/Girl_with_a_Pearl_Earring`.
- Normalized gallery asset: `1665 Girl with a Pearl Earring.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `girl-with-a-pearl-earring`; title `Girl with a Pearl Earring`; worksKey `(absent)`; artistId `johannes-vermeer`. Evidence: same Commons asset `1665 Girl with a Pearl Earring.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/1665_Girl_with_a_Pearl_Earring.jpg/500px-1665_Girl_with_a_Pearl_Earring.jpg`; page: `https://commons.wikimedia.org/wiki/File:1665_Girl_with_a_Pearl_Earring.jpg`.
- Checked-in route `p/artwork/girl-with-a-pearl-earring.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/1665_Girl_with_a_Pearl_Earring.jpg/500px-1665_Girl_with_a_Pearl_Earring.jpg`.

### 59. johannes-vermeer / The Milkmaid

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `johannes-vermeer` → `The Milkmaid`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Johannes_Vermeer_-_Het_melkmeisje_-_Google_Art_Project.png/500px-Johannes_Vermeer_-_Het_melkmeisje_-_Google_Art_Project.png`; page: `https://en.wikipedia.org/wiki/The_Milkmaid_(Vermeer)`.
- Normalized gallery asset: `Johannes Vermeer - Het melkmeisje - Google Art Project.png`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-milkmaid`; title `The Milkmaid`; worksKey `(absent)`; artistId `johannes-vermeer`. Evidence: same Commons asset `Johannes Vermeer - Het melkmeisje - Google Art Project.png`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Johannes_Vermeer_-_Het_melkmeisje_-_Google_Art_Project.png/500px-Johannes_Vermeer_-_Het_melkmeisje_-_Google_Art_Project.png`; page: `https://commons.wikimedia.org/wiki/File:Johannes_Vermeer_-_Het_melkmeisje_-_Google_Art_Project.png`.
- Checked-in route `p/artwork/the-milkmaid.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Johannes_Vermeer_-_Het_melkmeisje_-_Google_Art_Project.png/500px-Johannes_Vermeer_-_Het_melkmeisje_-_Google_Art_Project.png`.

### 60. johannes-vermeer / View of Delft

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `johannes-vermeer` → `View of Delft`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Vermeer-view-of-delft.jpg/500px-Vermeer-view-of-delft.jpg`; page: `https://en.wikipedia.org/wiki/View_of_Delft`.
- Normalized gallery asset: `Vermeer-view-of-delft.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `view-of-delft`; title `View of Delft`; worksKey `View of Delft`; artistId `johannes-vermeer`. Evidence: same Commons asset `Vermeer-view-of-delft.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Vermeer-view-of-delft.jpg/500px-Vermeer-view-of-delft.jpg`; page: `https://commons.wikimedia.org/wiki/File:Vermeer-view-of-delft.jpg`.
- Checked-in route `p/artwork/view-of-delft.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Vermeer-view-of-delft.jpg/500px-Vermeer-view-of-delft.jpg`.

### 61. johannes-vermeer / The Art of Painting

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `johannes-vermeer` → `The Art of Painting`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Jan_Vermeer_-_The_Art_of_Painting_-_Google_Art_Project.jpg/500px-Jan_Vermeer_-_The_Art_of_Painting_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Art_of_Painting`.
- Normalized gallery asset: `Jan Vermeer - The Art of Painting - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-art-of-painting`; title `The Art of Painting`; worksKey `The Art of Painting`; artistId `johannes-vermeer`. Evidence: same Commons asset `Jan Vermeer - The Art of Painting - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Jan_Vermeer_-_The_Art_of_Painting_-_Google_Art_Project.jpg/500px-Jan_Vermeer_-_The_Art_of_Painting_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jan_Vermeer_-_The_Art_of_Painting_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/the-art-of-painting.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Jan_Vermeer_-_The_Art_of_Painting_-_Google_Art_Project.jpg/500px-Jan_Vermeer_-_The_Art_of_Painting_-_Google_Art_Project.jpg`.

### 62. frans-hals / The Laughing Cavalier

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `frans-hals` → `The Laughing Cavalier`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Cavalier_soldier_Hals-1624x.jpg/500px-Cavalier_soldier_Hals-1624x.jpg`; page: `https://en.wikipedia.org/wiki/Laughing_Cavalier`.
- Normalized gallery asset: `Cavalier soldier Hals-1624x.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-9.js` / `the-laughing-cavalier`; title `The Laughing Cavalier`; worksKey `(absent)`; artistId `frans-hals`. Evidence: same Commons asset `Cavalier soldier Hals-1624x.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Cavalier_soldier_Hals-1624x.jpg/500px-Cavalier_soldier_Hals-1624x.jpg`; page: `https://commons.wikimedia.org/wiki/File:Cavalier_soldier_Hals-1624x.jpg`.
- Checked-in route `p/artwork/the-laughing-cavalier.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Cavalier_soldier_Hals-1624x.jpg/500px-Cavalier_soldier_Hals-1624x.jpg`.

### 63. frans-hals / Banquet of the Officers of the St George Militia

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `frans-hals` → `Banquet of the Officers of the St George Militia`; img: `https://upload.wikimedia.org/wikipedia/commons/9/95/Johan_van_Napels_-_detail_of_The_Banquet_of_the_Officers_of_the_St_George_Militia_Company_in_1616_by_Frans_Hals.jpg`; page: `https://commons.wikimedia.org/wiki/File:Johan_van_Napels_-_detail_of_The_Banquet_of_the_Officers_of_the_St_George_Militia_Company_in_1616_by_Frans_Hals.jpg`.
- Normalized gallery asset: `Johan van Napels - detail of The Banquet of the Officers of the St George Militia Company in 1616 by Frans Hals.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/frans-hals`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 64. frans-hals / Malle Babbe

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `frans-hals` → `Malle Babbe`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Frans_Hals_021.jpg/500px-Frans_Hals_021.jpg`; page: `https://en.wikipedia.org/wiki/Malle_Babbe`.
- Normalized gallery asset: `Frans Hals 021.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/frans-hals`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 65. diego-velazquez / Las Meninas

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `diego-velazquez` → `Las Meninas`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Las_Meninas%2C_by_Diego_Vel%C3%A1zquez%2C_from_Prado_in_Google_Earth.jpg/500px-Las_Meninas%2C_by_Diego_Vel%C3%A1zquez%2C_from_Prado_in_Google_Earth.jpg`; page: `https://en.wikipedia.org/wiki/Las_Meninas`.
- Normalized gallery asset: `Las Meninas, by Diego Velázquez, from Prado in Google Earth.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `las-meninas`; title `Las Meninas`; worksKey `(absent)`; artistId `diego-velazquez`. Evidence: same Commons asset `Las Meninas, by Diego Velázquez, from Prado in Google Earth.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Las_Meninas%2C_by_Diego_Vel%C3%A1zquez%2C_from_Prado_in_Google_Earth.jpg/500px-Las_Meninas%2C_by_Diego_Vel%C3%A1zquez%2C_from_Prado_in_Google_Earth.jpg`; page: `https://commons.wikimedia.org/wiki/File:Las_Meninas,_by_Diego_Vel%C3%A1zquez,_from_Prado_in_Google_Earth.jpg`.
- Checked-in route `p/artwork/las-meninas.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Las_Meninas%2C_by_Diego_Vel%C3%A1zquez%2C_from_Prado_in_Google_Earth.jpg/500px-Las_Meninas%2C_by_Diego_Vel%C3%A1zquez%2C_from_Prado_in_Google_Earth.jpg`.

### 66. diego-velazquez / Portrait of Innocent X

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `diego-velazquez` → `Portrait of Innocent X`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Retrato_del_Papa_Inocencio_X._Roma%2C_by_Diego_Vel%C3%A1zquez.jpg/500px-Retrato_del_Papa_Inocencio_X._Roma%2C_by_Diego_Vel%C3%A1zquez.jpg`; page: `https://en.wikipedia.org/wiki/Portrait_of_Innocent_X`.
- Normalized gallery asset: `Retrato del Papa Inocencio X. Roma, by Diego Velázquez.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `portrait-of-innocent-x`; title `Portrait of Innocent X`; worksKey `Portrait of Innocent X`; artistId `diego-velazquez`. Evidence: same Commons asset `Retrato del Papa Inocencio X. Roma, by Diego Velázquez.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Retrato_del_Papa_Inocencio_X._Roma%2C_by_Diego_Vel%C3%A1zquez.jpg/500px-Retrato_del_Papa_Inocencio_X._Roma%2C_by_Diego_Vel%C3%A1zquez.jpg`; page: `https://commons.wikimedia.org/wiki/File:Retrato_del_Papa_Inocencio_X._Roma,_by_Diego_Vel%C3%A1zquez.jpg`.
- Checked-in route `p/artwork/portrait-of-innocent-x.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Retrato_del_Papa_Inocencio_X._Roma%2C_by_Diego_Vel%C3%A1zquez.jpg/500px-Retrato_del_Papa_Inocencio_X._Roma%2C_by_Diego_Vel%C3%A1zquez.jpg`.

### 67. diego-velazquez / The Surrender of Breda

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `diego-velazquez` → `The Surrender of Breda`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Velazquez-The_Surrender_of_Breda.jpg/500px-Velazquez-The_Surrender_of_Breda.jpg`; page: `https://en.wikipedia.org/wiki/The_Surrender_of_Breda`.
- Normalized gallery asset: `Velazquez-The Surrender of Breda.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-surrender-of-breda`; title `The Surrender of Breda`; worksKey `The Surrender of Breda`; artistId `diego-velazquez`. Evidence: same Commons asset `Velazquez-The Surrender of Breda.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Velazquez-The_Surrender_of_Breda.jpg/500px-Velazquez-The_Surrender_of_Breda.jpg`; page: `https://commons.wikimedia.org/wiki/File:Velazquez-The_Surrender_of_Breda.jpg`.
- Checked-in route `p/artwork/the-surrender-of-breda.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Velazquez-The_Surrender_of_Breda.jpg/500px-Velazquez-The_Surrender_of_Breda.jpg`.

### 68. diego-velazquez / Rokeby Venus

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `diego-velazquez` → `Rokeby Venus`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Diego_Vel%C3%A1zquez_-_Rokeby_Venus.jpg/500px-Diego_Vel%C3%A1zquez_-_Rokeby_Venus.jpg`; page: `https://en.wikipedia.org/wiki/Rokeby_Venus`.
- Normalized gallery asset: `Diego Velázquez - Rokeby Venus.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `rokeby-venus`; title `The Rokeby Venus`; worksKey `Rokeby Venus`; artistId `diego-velazquez`. Evidence: same Commons asset `Diego Velázquez - Rokeby Venus.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Diego_Vel%C3%A1zquez_-_Rokeby_Venus.jpg/500px-Diego_Vel%C3%A1zquez_-_Rokeby_Venus.jpg`; page: `https://commons.wikimedia.org/wiki/File:Diego_Vel%C3%A1zquez_-_Rokeby_Venus.jpg`.
- Checked-in route `p/artwork/rokeby-venus.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Diego_Vel%C3%A1zquez_-_Rokeby_Venus.jpg/500px-Diego_Vel%C3%A1zquez_-_Rokeby_Venus.jpg`.

### 69. georges-de-la-tour / The Penitent Magdalene

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `georges-de-la-tour` → `The Penitent Magdalene`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/The_Penitent_Magdalen_MET_DT7252.jpg/500px-The_Penitent_Magdalen_MET_DT7252.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Penitent_Magdalen_MET_DT7252.jpg`.
- Normalized gallery asset: `The Penitent Magdalen MET DT7252.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/georges-de-la-tour`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 70. georges-de-la-tour / The Cheat with the Ace of Diamonds

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `georges-de-la-tour` → `The Cheat with the Ace of Diamonds`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Georges_de_La_Tour_-_Cheater_with_the_Ace_of_Diamonds_-_WGA12334.jpg/960px-Georges_de_La_Tour_-_Cheater_with_the_Ace_of_Diamonds_-_WGA12334.jpg`; page: `https://commons.wikimedia.org/wiki/File:Georges_de_La_Tour_-_Cheater_with_the_Ace_of_Diamonds_-_WGA12334.jpg`.
- Normalized gallery asset: `Georges de La Tour - Cheater with the Ace of Diamonds - WGA12334.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-8.js` / `the-cheat-with-the-ace-of-diamonds`; title `The Cheat with the Ace of Diamonds`; worksKey `(absent)`; artistId `georges-de-la-tour`. Evidence: same Commons asset `Georges de La Tour - Cheater with the Ace of Diamonds - WGA12334.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Georges_de_La_Tour_-_Cheater_with_the_Ace_of_Diamonds_-_WGA12334.jpg/960px-Georges_de_La_Tour_-_Cheater_with_the_Ace_of_Diamonds_-_WGA12334.jpg`; page: `https://commons.wikimedia.org/wiki/File:Georges_de_La_Tour_-_Cheater_with_the_Ace_of_Diamonds_-_WGA12334.jpg`.
- Checked-in route `p/artwork/the-cheat-with-the-ace-of-diamonds.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Georges_de_La_Tour_-_Cheater_with_the_Ace_of_Diamonds_-_WGA12334.jpg/960px-Georges_de_La_Tour_-_Cheater_with_the_Ace_of_Diamonds_-_WGA12334.jpg`.

### 71. georges-de-la-tour / Joseph the Carpenter

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `georges-de-la-tour` → `Joseph the Carpenter`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Georges_de_La_Tour._St._Joseph%2C_the_Carpenter.JPG/500px-Georges_de_La_Tour._St._Joseph%2C_the_Carpenter.JPG`; page: `https://commons.wikimedia.org/wiki/File:Georges_de_La_Tour._St._Joseph,_the_Carpenter.JPG`.
- Normalized gallery asset: `Georges de La Tour. St. Joseph, the Carpenter.JPG`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/georges-de-la-tour`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 72. nicolas-poussin / Et in Arcadia Ego

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `nicolas-poussin` → `Et in Arcadia Ego`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Nicolas_Poussin_-_Et_in_Arcadia_ego_%28deuxi%C3%A8me_version%29.jpg/960px-Nicolas_Poussin_-_Et_in_Arcadia_ego_%28deuxi%C3%A8me_version%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Nicolas_Poussin_-_Et_in_Arcadia_ego_(deuxi%C3%A8me_version).jpg`.
- Normalized gallery asset: `Nicolas Poussin - Et in Arcadia ego (deuxième version).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-6.js` / `et-in-arcadia-ego`; title `Et in Arcadia ego`; worksKey `Et in Arcadia Ego`; artistId `nicolas-poussin`. Evidence: same Commons asset `Nicolas Poussin - Et in Arcadia ego (deuxième version).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Nicolas_Poussin_-_Et_in_Arcadia_ego_%28deuxi%C3%A8me_version%29.jpg/960px-Nicolas_Poussin_-_Et_in_Arcadia_ego_%28deuxi%C3%A8me_version%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Nicolas_Poussin_-_Et_in_Arcadia_ego_(deuxi%C3%A8me_version).jpg`.
- Checked-in route `p/artwork/et-in-arcadia-ego.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Nicolas_Poussin_-_Et_in_Arcadia_ego_%28deuxi%C3%A8me_version%29.jpg/960px-Nicolas_Poussin_-_Et_in_Arcadia_ego_%28deuxi%C3%A8me_version%29.jpg`.

### 73. nicolas-poussin / The Abduction of the Sabine Women

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `nicolas-poussin` → `The Abduction of the Sabine Women`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Nicolas_Poussin_-_L%27Enl%C3%A8vement_des_Sabines_%281634-5%29.jpg/960px-Nicolas_Poussin_-_L%27Enl%C3%A8vement_des_Sabines_%281634-5%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Nicolas_Poussin_-_L%27Enl%C3%A8vement_des_Sabines_(1634-5).jpg`.
- Normalized gallery asset: `Nicolas Poussin - L'Enlèvement des Sabines (1634-5).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/nicolas-poussin`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 74. nicolas-poussin / The Adoration of the Golden Calf

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `nicolas-poussin` → `The Adoration of the Golden Calf`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/The_Adoration_of_the_Golden_Calf_%E2%80%93_Nicolas_Poussin.jpg/500px-The_Adoration_of_the_Golden_Calf_%E2%80%93_Nicolas_Poussin.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Adoration_of_the_Golden_Calf_%E2%80%93_Nicolas_Poussin.jpg`.
- Normalized gallery asset: `The Adoration of the Golden Calf – Nicolas Poussin.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/nicolas-poussin`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 75. antoine-watteau / Pilgrimage to Cythera

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `antoine-watteau` → `Pilgrimage to Cythera`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/L%27Embarquement_pour_Cyth%C3%A8re%2C_by_Antoine_Watteau%2C_from_C2RMF_retouched.jpg/500px-L%27Embarquement_pour_Cyth%C3%A8re%2C_by_Antoine_Watteau%2C_from_C2RMF_retouched.jpg`; page: `https://en.wikipedia.org/wiki/The_Embarkation_for_Cythera`.
- Normalized gallery asset: `L'Embarquement pour Cythère, by Antoine Watteau, from C2RMF retouched.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-7.js` / `the-embarkation-for-cythera`; title `The Embarkation for Cythera`; worksKey `Pilgrimage to Cythera`; artistId `antoine-watteau`. Evidence: same Commons asset `L'Embarquement pour Cythère, by Antoine Watteau, from C2RMF retouched.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/L%27Embarquement_pour_Cyth%C3%A8re%2C_by_Antoine_Watteau%2C_from_C2RMF_retouched.jpg/500px-L%27Embarquement_pour_Cyth%C3%A8re%2C_by_Antoine_Watteau%2C_from_C2RMF_retouched.jpg`; page: `https://commons.wikimedia.org/wiki/File:L%27Embarquement_pour_Cyth%C3%A8re,_by_Antoine_Watteau,_from_C2RMF_retouched.jpg`.
- Checked-in route `p/artwork/the-embarkation-for-cythera.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/L%27Embarquement_pour_Cyth%C3%A8re%2C_by_Antoine_Watteau%2C_from_C2RMF_retouched.jpg/500px-L%27Embarquement_pour_Cyth%C3%A8re%2C_by_Antoine_Watteau%2C_from_C2RMF_retouched.jpg`.

### 76. antoine-watteau / Pierrot (Gilles)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `antoine-watteau` → `Pierrot (Gilles)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Pierrot_-_Antoine_Watteau_-_Mus%C3%A9e_du_Louvre_Peintures_MI_1121_-_apr%C3%A8s_restauration_2024.jpg/500px-Pierrot_-_Antoine_Watteau_-_Mus%C3%A9e_du_Louvre_Peintures_MI_1121_-_apr%C3%A8s_restauration_2024.jpg`; page: `https://en.wikipedia.org/wiki/Pierrot_(Watteau)`.
- Normalized gallery asset: `Pierrot - Antoine Watteau - Musée du Louvre Peintures MI 1121 - après restauration 2024.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/antoine-watteau`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 77. jean-honore-fragonard / The Swing

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jean-honore-fragonard` → `The Swing`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/The_Swing_%28P430%29.jpg/500px-The_Swing_%28P430%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Swing_(Fragonard)`.
- Normalized gallery asset: `The Swing (P430).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jean-honore-fragonard`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 78. jean-honore-fragonard / The Progress of Love

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jean-honore-fragonard` → `The Progress of Love`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Jean-Honor%C3%A9_Fragonard_-_The_Progress_of_Love_-_The_Meeting_-_WGA08071.jpg/960px-Jean-Honor%C3%A9_Fragonard_-_The_Progress_of_Love_-_The_Meeting_-_WGA08071.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jean-Honor%C3%A9_Fragonard_-_The_Progress_of_Love_-_The_Meeting_-_WGA08071.jpg`.
- Normalized gallery asset: `Jean-Honoré Fragonard - The Progress of Love - The Meeting - WGA08071.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jean-honore-fragonard`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 79. jean-honore-fragonard / The Bolt

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jean-honore-fragonard` → `The Bolt`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Le_Verrou_-_Jean-Honor%C3%A9_Fragonard_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1974_2.jpg/500px-Le_Verrou_-_Jean-Honor%C3%A9_Fragonard_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1974_2.jpg`; page: `https://en.wikipedia.org/wiki/The_Bolt_(Fragonard)`.
- Normalized gallery asset: `Le Verrou - Jean-Honoré Fragonard - Musée du Louvre Peintures RF 1974 2.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-7.js` / `the-bolt`; title `The Bolt`; worksKey `(absent)`; artistId `jean-honore-fragonard`. Evidence: same Commons asset `Le Verrou - Jean-Honoré Fragonard - Musée du Louvre Peintures RF 1974 2.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Le_Verrou_-_Jean-Honor%C3%A9_Fragonard_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1974_2.jpg/500px-Le_Verrou_-_Jean-Honor%C3%A9_Fragonard_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1974_2.jpg`; page: `https://commons.wikimedia.org/wiki/File:Le_Verrou_-_Jean-Honor%C3%A9_Fragonard_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1974_2.jpg`.
- Checked-in route `p/artwork/the-bolt.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Le_Verrou_-_Jean-Honor%C3%A9_Fragonard_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1974_2.jpg/500px-Le_Verrou_-_Jean-Honor%C3%A9_Fragonard_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1974_2.jpg`.

### 80. jean-simeon-chardin / The Ray

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jean-simeon-chardin` → `The Ray`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/La_Raie_-_Jean_Baptiste_Sim%C3%A9on_Chardin_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3197.jpg/500px-La_Raie_-_Jean_Baptiste_Sim%C3%A9on_Chardin_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3197.jpg`; page: `https://en.wikipedia.org/wiki/The_Ray_(Chardin)`.
- Normalized gallery asset: `La Raie - Jean Baptiste Siméon Chardin - Musée du Louvre Peintures INV 3197.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-9.js` / `the-ray`; title `The Ray`; worksKey `(absent)`; artistId `jean-simeon-chardin`. Evidence: same Commons asset `La Raie - Jean Baptiste Siméon Chardin - Musée du Louvre Peintures INV 3197.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/La_Raie_-_Jean_Baptiste_Sim%C3%A9on_Chardin_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3197.jpg/500px-La_Raie_-_Jean_Baptiste_Sim%C3%A9on_Chardin_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3197.jpg`; page: `https://commons.wikimedia.org/wiki/File:La_Raie_-_Jean_Baptiste_Sim%C3%A9on_Chardin_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3197.jpg`.
- Checked-in route `p/artwork/the-ray.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/La_Raie_-_Jean_Baptiste_Sim%C3%A9on_Chardin_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3197.jpg/500px-La_Raie_-_Jean_Baptiste_Sim%C3%A9on_Chardin_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3197.jpg`.

### 81. jean-simeon-chardin / Saying Grace

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jean-simeon-chardin` → `Saying Grace`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Le_B%C3%A9n%C3%A9dicit%C3%A9_de_Jean_Sim%C3%A9on_Chardin_%28cropped%29.jpg/500px-Le_B%C3%A9n%C3%A9dicit%C3%A9_de_Jean_Sim%C3%A9on_Chardin_%28cropped%29.jpg`; page: `https://en.wikipedia.org/wiki/Saying_Grace_(Chardin)`.
- Normalized gallery asset: `Le Bénédicité de Jean Siméon Chardin (cropped).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jean-simeon-chardin`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 82. jean-simeon-chardin / Soap Bubbles

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jean-simeon-chardin` → `Soap Bubbles`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Soap_Bubbles_MET_DP356133.jpg/500px-Soap_Bubbles_MET_DP356133.jpg`; page: `https://en.wikipedia.org/wiki/Soap_Bubbles_(Chardin)`.
- Normalized gallery asset: `Soap Bubbles MET DP356133.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jean-simeon-chardin`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 83. canaletto / The Stonemason's Yard

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `canaletto` → `The Stonemason's Yard`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Canaletto_-_The_Stonemason%27s_Yard.jpg/500px-Canaletto_-_The_Stonemason%27s_Yard.jpg`; page: `https://en.wikipedia.org/wiki/The_Stonemason's_Yard`.
- Normalized gallery asset: `Canaletto - The Stonemason's Yard.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/canaletto`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 84. canaletto / Return of the Bucentaur

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `canaletto` → `Return of the Bucentaur`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Canaletto_-_Bucentaur%27s_return_to_the_pier_by_the_Palazzo_Ducale_-_Google_Art_Project.jpg/960px-Canaletto_-_Bucentaur%27s_return_to_the_pier_by_the_Palazzo_Ducale_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Canaletto_-_Bucentaur%27s_return_to_the_pier_by_the_Palazzo_Ducale_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Canaletto - Bucentaur's return to the pier by the Palazzo Ducale - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/canaletto`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 85. canaletto / Eton College Chapel

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `canaletto` → `Eton College Chapel`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Canaletto_-_Eton_College_Chapel_-_with_frame.jpg/960px-Canaletto_-_Eton_College_Chapel_-_with_frame.jpg`; page: `https://commons.wikimedia.org/wiki/File:Canaletto_-_Eton_College_Chapel_-_with_frame.jpg`.
- Normalized gallery asset: `Canaletto - Eton College Chapel - with frame.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/canaletto`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 86. giambattista-tiepolo / Apollo and the Continents (Würzburg)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giambattista-tiepolo` → `Apollo and the Continents (Würzburg)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Giovanni_Battista_Tiepolo_-_Allegory_of_the_Planets_and_Continents.jpg/960px-Giovanni_Battista_Tiepolo_-_Allegory_of_the_Planets_and_Continents.jpg`; page: `https://commons.wikimedia.org/wiki/File:Giovanni_Battista_Tiepolo_-_Allegory_of_the_Planets_and_Continents.jpg`.
- Normalized gallery asset: `Giovanni Battista Tiepolo - Allegory of the Planets and Continents.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giambattista-tiepolo`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 87. giambattista-tiepolo / The Banquet of Cleopatra

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giambattista-tiepolo` → `The Banquet of Cleopatra`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Giambattista_Tiepolo_-_The_Banquet_of_Cleopatra_-_Google_Art_Project.jpg/500px-Giambattista_Tiepolo_-_The_Banquet_of_Cleopatra_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Banquet_of_Cleopatra_(Tiepolo)`.
- Normalized gallery asset: `Giambattista Tiepolo - The Banquet of Cleopatra - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giambattista-tiepolo`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 88. giambattista-tiepolo / Apotheosis of the Spanish Monarchy

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giambattista-tiepolo` → `Apotheosis of the Spanish Monarchy`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/The_Apotheosis_of_the_Spanish_Monarchy_MET_DT5155.jpg/500px-The_Apotheosis_of_the_Spanish_Monarchy_MET_DT5155.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Apotheosis_of_the_Spanish_Monarchy_MET_DT5155.jpg`.
- Normalized gallery asset: `The Apotheosis of the Spanish Monarchy MET DT5155.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giambattista-tiepolo`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 89. william-hogarth / A Rake's Progress

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `william-hogarth` → `A Rake's Progress`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/William_Hogarth_-_A_Rake%27s_Progress_-_Tavern_Scene.jpg/960px-William_Hogarth_-_A_Rake%27s_Progress_-_Tavern_Scene.jpg`; page: `https://commons.wikimedia.org/wiki/File:William_Hogarth_-_A_Rake%27s_Progress_-_Tavern_Scene.jpg`.
- Normalized gallery asset: `William Hogarth - A Rake's Progress - Tavern Scene.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/william-hogarth`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 90. william-hogarth / Marriage A-la-Mode

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `william-hogarth` → `Marriage A-la-Mode`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Marriage_A-la-Mode_1%2C_The_Marriage_Settlement_-_William_Hogarth.jpg/500px-Marriage_A-la-Mode_1%2C_The_Marriage_Settlement_-_William_Hogarth.jpg`; page: `https://en.wikipedia.org/wiki/Marriage_A-la-Mode_(Hogarth)`.
- Normalized gallery asset: `Marriage A-la-Mode 1, The Marriage Settlement - William Hogarth.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/william-hogarth`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 91. william-hogarth / Gin Lane

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `william-hogarth` → `Gin Lane`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/William_Hogarth_-_Gin_Lane.jpg/500px-William_Hogarth_-_Gin_Lane.jpg`; page: `https://commons.wikimedia.org/wiki/File:William_Hogarth_-_Gin_Lane.jpg`.
- Normalized gallery asset: `William Hogarth - Gin Lane.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/william-hogarth`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 92. thomas-gainsborough / The Blue Boy

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `thomas-gainsborough` → `The Blue Boy`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Thomas_Gainsborough_-_The_Blue_Boy_%28c._1770%29.jpg/500px-Thomas_Gainsborough_-_The_Blue_Boy_%28c._1770%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Thomas_Gainsborough_-_The_Blue_Boy_(c._1770).jpg`.
- Normalized gallery asset: `Thomas Gainsborough - The Blue Boy (c. 1770).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/thomas-gainsborough`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 93. thomas-gainsborough / Mr and Mrs Andrews

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `thomas-gainsborough` → `Mr and Mrs Andrews`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Thomas_Gainsborough_-_Mr_and_Mrs_Andrews.jpg/500px-Thomas_Gainsborough_-_Mr_and_Mrs_Andrews.jpg`; page: `https://en.wikipedia.org/wiki/Mr_and_Mrs_Andrews`.
- Normalized gallery asset: `Thomas Gainsborough - Mr and Mrs Andrews.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-7.js` / `mr-and-mrs-andrews`; title `Mr and Mrs Andrews`; worksKey `(absent)`; artistId `thomas-gainsborough`. Evidence: same Commons asset `Thomas Gainsborough - Mr and Mrs Andrews.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Thomas_Gainsborough_-_Mr_and_Mrs_Andrews.jpg/500px-Thomas_Gainsborough_-_Mr_and_Mrs_Andrews.jpg`; page: `https://commons.wikimedia.org/wiki/File:Thomas_Gainsborough_-_Mr_and_Mrs_Andrews.jpg`.
- Checked-in route `p/artwork/mr-and-mrs-andrews.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Thomas_Gainsborough_-_Mr_and_Mrs_Andrews.jpg/500px-Thomas_Gainsborough_-_Mr_and_Mrs_Andrews.jpg`.

### 94. thomas-gainsborough / The Morning Walk

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `thomas-gainsborough` → `The Morning Walk`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Thomas_Gainsborough_-_Mr_and_Mrs_William_Hallett_%28%27The_Morning_Walk%27%29_-_WGA8418.jpg/500px-Thomas_Gainsborough_-_Mr_and_Mrs_William_Hallett_%28%27The_Morning_Walk%27%29_-_WGA8418.jpg`; page: `https://en.wikipedia.org/wiki/Mr_and_Mrs_William_Hallett`.
- Normalized gallery asset: `Thomas Gainsborough - Mr and Mrs William Hallett ('The Morning Walk') - WGA8418.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/thomas-gainsborough`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 95. elisabeth-vigee-le-brun / Self-Portrait in a Straw Hat

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `elisabeth-vigee-le-brun` → `Self-Portrait in a Straw Hat`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Self-portrait_in_a_Straw_Hat_by_Elisabeth-Louise_Vig%C3%A9e-Lebrun.jpg/500px-Self-portrait_in_a_Straw_Hat_by_Elisabeth-Louise_Vig%C3%A9e-Lebrun.jpg`; page: `https://en.wikipedia.org/wiki/Self-Portrait_in_a_Straw_Hat`.
- Normalized gallery asset: `Self-portrait in a Straw Hat by Elisabeth-Louise Vigée-Lebrun.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/elisabeth-vigee-le-brun`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 96. elisabeth-vigee-le-brun / Marie Antoinette and Her Children

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `elisabeth-vigee-le-brun` → `Marie Antoinette and Her Children`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Louise_Elisabeth_Vig%C3%A9e-Lebrun_-_Marie-Antoinette_de_Lorraine-Habsbourg%2C_reine_de_France_et_ses_enfants_-_Google_Art_Project.jpg/500px-Louise_Elisabeth_Vig%C3%A9e-Lebrun_-_Marie-Antoinette_de_Lorraine-Habsbourg%2C_reine_de_France_et_ses_enfants_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Marie_Antoinette_and_Her_Children`.
- Normalized gallery asset: `Louise Elisabeth Vigée-Lebrun - Marie-Antoinette de Lorraine-Habsbourg, reine de France et ses enfants - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/elisabeth-vigee-le-brun`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 97. elisabeth-vigee-le-brun / Self-Portrait with Her Daughter Julie

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `elisabeth-vigee-le-brun` → `Self-Portrait with Her Daughter Julie`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Self-portrait_with_Her_Daughter_by_Elisabeth-Louise_Vig%C3%A9e_Le_Brun.jpg/960px-Self-portrait_with_Her_Daughter_by_Elisabeth-Louise_Vig%C3%A9e_Le_Brun.jpg`; page: `https://commons.wikimedia.org/wiki/File:Self-portrait_with_Her_Daughter_by_Elisabeth-Louise_Vig%C3%A9e_Le_Brun.jpg`.
- Normalized gallery asset: `Self-portrait with Her Daughter by Elisabeth-Louise Vigée Le Brun.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/elisabeth-vigee-le-brun`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 98. jacques-louis-david / Oath of the Horatii

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jacques-louis-david` → `Oath of the Horatii`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Le_Serment_des_Horaces_-_Jacques-Louis_David_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3692_%3B_MR_1432.jpg/500px-Le_Serment_des_Horaces_-_Jacques-Louis_David_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3692_%3B_MR_1432.jpg`; page: `https://en.wikipedia.org/wiki/Oath_of_the_Horatii`.
- Normalized gallery asset: `Le Serment des Horaces - Jacques-Louis David - Musée du Louvre Peintures INV 3692 ; MR 1432.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `oath-of-the-horatii`; title `Oath of the Horatii`; worksKey `(absent)`; artistId `jacques-louis-david`. Evidence: same Commons asset `Le Serment des Horaces - Jacques-Louis David - Musée du Louvre Peintures INV 3692 ; MR 1432.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Le_Serment_des_Horaces_-_Jacques-Louis_David_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3692_%3B_MR_1432.jpg/500px-Le_Serment_des_Horaces_-_Jacques-Louis_David_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3692_%3B_MR_1432.jpg`; page: `https://commons.wikimedia.org/wiki/File:Le_Serment_des_Horaces_-_Jacques-Louis_David_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3692_;_MR_1432.jpg`.
- Checked-in route `p/artwork/oath-of-the-horatii.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Le_Serment_des_Horaces_-_Jacques-Louis_David_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3692_%3B_MR_1432.jpg/500px-Le_Serment_des_Horaces_-_Jacques-Louis_David_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3692_%3B_MR_1432.jpg`.

### 99. jacques-louis-david / The Death of Marat

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jacques-louis-david` → `The Death of Marat`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Death_of_Marat_by_David.jpg/500px-Death_of_Marat_by_David.jpg`; page: `https://en.wikipedia.org/wiki/The_Death_of_Marat`.
- Normalized gallery asset: `Death of Marat by David.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jacques-louis-david`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 100. jacques-louis-david / The Coronation of Napoleon

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jacques-louis-david` → `The Coronation of Napoleon`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Jacques-Louis_David_-_The_Coronation_of_Napoleon_%281805-1807%29.jpg/500px-Jacques-Louis_David_-_The_Coronation_of_Napoleon_%281805-1807%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Coronation_of_Napoleon`.
- Normalized gallery asset: `Jacques-Louis David - The Coronation of Napoleon (1805-1807).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jacques-louis-david`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 101. francisco-goya / The Third of May 1808

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `francisco-goya` → `The Third of May 1808`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/El_Tres_de_Mayo%2C_by_Francisco_de_Goya%2C_from_Prado_thin_black_margin.jpg/500px-El_Tres_de_Mayo%2C_by_Francisco_de_Goya%2C_from_Prado_thin_black_margin.jpg`; page: `https://en.wikipedia.org/wiki/The_Third_of_May_1808`.
- Normalized gallery asset: `El Tres de Mayo, by Francisco de Goya, from Prado thin black margin.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-third-of-may-1808`; title `The Third of May 1808`; worksKey `(absent)`; artistId `francisco-goya`. Evidence: same Commons asset `El Tres de Mayo, by Francisco de Goya, from Prado thin black margin.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/El_Tres_de_Mayo%2C_by_Francisco_de_Goya%2C_from_Prado_thin_black_margin.jpg/500px-El_Tres_de_Mayo%2C_by_Francisco_de_Goya%2C_from_Prado_thin_black_margin.jpg`; page: `https://commons.wikimedia.org/wiki/File:El_Tres_de_Mayo,_by_Francisco_de_Goya,_from_Prado_thin_black_margin.jpg`.
- Checked-in route `p/artwork/the-third-of-may-1808.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/El_Tres_de_Mayo%2C_by_Francisco_de_Goya%2C_from_Prado_thin_black_margin.jpg/500px-El_Tres_de_Mayo%2C_by_Francisco_de_Goya%2C_from_Prado_thin_black_margin.jpg`.

### 102. francisco-goya / Saturn Devouring His Son

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `francisco-goya` → `Saturn Devouring His Son`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Francisco_de_Goya%2C_Saturno_devorando_a_su_hijo_%281819-1823%29.jpg/500px-Francisco_de_Goya%2C_Saturno_devorando_a_su_hijo_%281819-1823%29.jpg`; page: `https://en.wikipedia.org/wiki/Saturn_Devouring_His_Son`.
- Normalized gallery asset: `Francisco de Goya, Saturno devorando a su hijo (1819-1823).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `saturn-devouring-his-son`; title `Saturn Devouring His Son`; worksKey `(absent)`; artistId `francisco-goya`. Evidence: same Commons asset `Francisco de Goya, Saturno devorando a su hijo (1819-1823).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Francisco_de_Goya%2C_Saturno_devorando_a_su_hijo_%281819-1823%29.jpg/500px-Francisco_de_Goya%2C_Saturno_devorando_a_su_hijo_%281819-1823%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Francisco_de_Goya,_Saturno_devorando_a_su_hijo_(1819-1823).jpg`.
- Checked-in route `p/artwork/saturn-devouring-his-son.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Francisco_de_Goya%2C_Saturno_devorando_a_su_hijo_%281819-1823%29.jpg/500px-Francisco_de_Goya%2C_Saturno_devorando_a_su_hijo_%281819-1823%29.jpg`.

### 103. francisco-goya / The Naked Maja

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `francisco-goya` → `The Naked Maja`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Goya_Maja_naga2.jpg/500px-Goya_Maja_naga2.jpg`; page: `https://en.wikipedia.org/wiki/La_maja_desnuda`.
- Normalized gallery asset: `Goya Maja naga2.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-naked-maja`; title `The Naked Maja`; worksKey `(absent)`; artistId `francisco-goya`. Evidence: same Commons asset `Goya Maja naga2.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Goya_Maja_naga2.jpg/500px-Goya_Maja_naga2.jpg`; page: `https://commons.wikimedia.org/wiki/File:Goya_Maja_naga2.jpg`.
- Checked-in route `p/artwork/the-naked-maja.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Goya_Maja_naga2.jpg/500px-Goya_Maja_naga2.jpg`.

### 104. francisco-goya / Los Caprichos

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `francisco-goya` → `Los Caprichos`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Francisco_Goya_y_Lucientes_Pintor.jpg/500px-Francisco_Goya_y_Lucientes_Pintor.jpg`; page: `https://en.wikipedia.org/wiki/Los_caprichos`.
- Normalized gallery asset: `Francisco Goya y Lucientes Pintor.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/francisco-goya`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 105. jmw-turner / The Fighting Temeraire

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jmw-turner` → `The Fighting Temeraire`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/The_Fighting_Temeraire%2C_JMW_Turner%2C_National_Gallery.jpg/500px-The_Fighting_Temeraire%2C_JMW_Turner%2C_National_Gallery.jpg`; page: `https://en.wikipedia.org/wiki/The_Fighting_Temeraire`.
- Normalized gallery asset: `The Fighting Temeraire, JMW Turner, National Gallery.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-fighting-temeraire`; title `The Fighting Temeraire`; worksKey `The Fighting Temeraire`; artistId `jmw-turner`. Evidence: same Commons asset `The Fighting Temeraire, JMW Turner, National Gallery.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/The_Fighting_Temeraire%2C_JMW_Turner%2C_National_Gallery.jpg/500px-The_Fighting_Temeraire%2C_JMW_Turner%2C_National_Gallery.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Fighting_Temeraire,_JMW_Turner,_National_Gallery.jpg`.
- Checked-in route `p/artwork/the-fighting-temeraire.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/The_Fighting_Temeraire%2C_JMW_Turner%2C_National_Gallery.jpg/500px-The_Fighting_Temeraire%2C_JMW_Turner%2C_National_Gallery.jpg`.

### 106. jmw-turner / Rain, Steam and Speed

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jmw-turner` → `Rain, Steam and Speed`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Turner_-_Rain%2C_Steam_and_Speed_-_National_Gallery_file.jpg/500px-Turner_-_Rain%2C_Steam_and_Speed_-_National_Gallery_file.jpg`; page: `https://commons.wikimedia.org/wiki/File:Turner_-_Rain,_Steam_and_Speed_-_National_Gallery_file.jpg`.
- Normalized gallery asset: `Turner - Rain, Steam and Speed - National Gallery file.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `rain-steam-and-speed`; title `Rain, Steam and Speed — The Great Western Railway`; worksKey `Rain, Steam and Speed`; artistId `jmw-turner`. Evidence: same Commons asset `Turner - Rain, Steam and Speed - National Gallery file.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Turner_-_Rain%2C_Steam_and_Speed_-_National_Gallery_file.jpg/500px-Turner_-_Rain%2C_Steam_and_Speed_-_National_Gallery_file.jpg`; page: `https://commons.wikimedia.org/wiki/File:Turner_-_Rain,_Steam_and_Speed_-_National_Gallery_file.jpg`.
- Checked-in route `p/artwork/rain-steam-and-speed.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Turner_-_Rain%2C_Steam_and_Speed_-_National_Gallery_file.jpg/500px-Turner_-_Rain%2C_Steam_and_Speed_-_National_Gallery_file.jpg`.

### 107. jmw-turner / Snow Storm — Steam-Boat off a Harbour's Mouth

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jmw-turner` → `Snow Storm — Steam-Boat off a Harbour's Mouth`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Joseph_Mallord_William_Turner_-_Snow_Storm_-_Steam-Boat_off_a_Harbour%27s_Mouth_-_WGA23178.jpg/960px-Joseph_Mallord_William_Turner_-_Snow_Storm_-_Steam-Boat_off_a_Harbour%27s_Mouth_-_WGA23178.jpg`; page: `https://commons.wikimedia.org/wiki/File:Joseph_Mallord_William_Turner_-_Snow_Storm_-_Steam-Boat_off_a_Harbour%27s_Mouth_-_WGA23178.jpg`.
- Normalized gallery asset: `Joseph Mallord William Turner - Snow Storm - Steam-Boat off a Harbour's Mouth - WGA23178.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `snow-storm-steamboat`; title `Snow Storm: Steam-Boat off a Harbour's Mouth`; worksKey `Snow Storm — Steam-Boat off a Harbour's Mouth`; artistId `jmw-turner`. Evidence: same Commons asset `Joseph Mallord William Turner - Snow Storm - Steam-Boat off a Harbour's Mouth - WGA23178.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Joseph_Mallord_William_Turner_-_Snow_Storm_-_Steam-Boat_off_a_Harbour%27s_Mouth_-_WGA23178.jpg/500px-Joseph_Mallord_William_Turner_-_Snow_Storm_-_Steam-Boat_off_a_Harbour%27s_Mouth_-_WGA23178.jpg`; page: `https://commons.wikimedia.org/wiki/File:Joseph_Mallord_William_Turner_-_Snow_Storm_-_Steam-Boat_off_a_Harbour%27s_Mouth_-_WGA23178.jpg`.
- Checked-in route `p/artwork/snow-storm-steamboat.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Joseph_Mallord_William_Turner_-_Snow_Storm_-_Steam-Boat_off_a_Harbour%27s_Mouth_-_WGA23178.jpg/500px-Joseph_Mallord_William_Turner_-_Snow_Storm_-_Steam-Boat_off_a_Harbour%27s_Mouth_-_WGA23178.jpg`.

### 108. jmw-turner / The Slave Ship

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jmw-turner` → `The Slave Ship`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Slave-ship.jpg/500px-Slave-ship.jpg`; page: `https://en.wikipedia.org/wiki/The_Slave_Ship`.
- Normalized gallery asset: `Slave-ship.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `slave-ship`; title `The Slave Ship`; worksKey `The Slave Ship`; artistId `jmw-turner`. Evidence: same Commons asset `Slave-ship.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Slave-ship.jpg/500px-Slave-ship.jpg`; page: `https://commons.wikimedia.org/wiki/File:Slave-ship.jpg`.
- Checked-in route `p/artwork/slave-ship.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Slave-ship.jpg/500px-Slave-ship.jpg`.

### 109. john-constable / The Hay Wain

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `john-constable` → `The Hay Wain`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/John_Constable_-_The_Hay_Wain_%281821%29.jpg/500px-John_Constable_-_The_Hay_Wain_%281821%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Hay_Wain`.
- Normalized gallery asset: `John Constable - The Hay Wain (1821).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-6.js` / `the-hay-wain`; title `The Hay Wain`; worksKey `(absent)`; artistId `john-constable`. Evidence: same Commons asset `John Constable - The Hay Wain (1821).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/John_Constable_-_The_Hay_Wain_%281821%29.jpg/500px-John_Constable_-_The_Hay_Wain_%281821%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:John_Constable_-_The_Hay_Wain_(1821).jpg`.
- Checked-in route `p/artwork/the-hay-wain.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/John_Constable_-_The_Hay_Wain_%281821%29.jpg/500px-John_Constable_-_The_Hay_Wain_%281821%29.jpg`.

### 110. john-constable / Salisbury Cathedral from the Meadows

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `john-constable` → `Salisbury Cathedral from the Meadows`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Constable_Salisbury_meadows.jpg/500px-Constable_Salisbury_meadows.jpg`; page: `https://en.wikipedia.org/wiki/Salisbury_Cathedral_from_the_Meadows`.
- Normalized gallery asset: `Constable Salisbury meadows.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/john-constable`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 111. john-constable / Cloud Studies

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `john-constable` → `Cloud Studies`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/John_Constable_-_Cloud_Study_-_Google_Art_Project_%282442698%29.jpg/960px-John_Constable_-_Cloud_Study_-_Google_Art_Project_%282442698%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:John_Constable_-_Cloud_Study_-_Google_Art_Project_(2442698).jpg`.
- Normalized gallery asset: `John Constable - Cloud Study - Google Art Project (2442698).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/john-constable`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 112. caspar-david-friedrich / Wanderer above the Sea of Fog

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `caspar-david-friedrich` → `Wanderer above the Sea of Fog`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Caspar_David_Friedrich_-_Wanderer_above_the_Sea_of_Fog.jpeg/500px-Caspar_David_Friedrich_-_Wanderer_above_the_Sea_of_Fog.jpeg`; page: `https://en.wikipedia.org/wiki/Wanderer_above_the_Sea_of_Fog`.
- Normalized gallery asset: `Caspar David Friedrich - Wanderer above the Sea of Fog.jpeg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/caspar-david-friedrich`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 113. caspar-david-friedrich / The Sea of Ice

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `caspar-david-friedrich` → `The Sea of Ice`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Caspar_David_Friedrich_-_Das_Eismeer_-_Hamburger_Kunsthalle_-_02.jpg/500px-Caspar_David_Friedrich_-_Das_Eismeer_-_Hamburger_Kunsthalle_-_02.jpg`; page: `https://en.wikipedia.org/wiki/The_Sea_of_Ice`.
- Normalized gallery asset: `Caspar David Friedrich - Das Eismeer - Hamburger Kunsthalle - 02.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/caspar-david-friedrich`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 114. caspar-david-friedrich / Abbey in the Oakwood

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `caspar-david-friedrich` → `Abbey in the Oakwood`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/The_Abbey_in_the_Oakwood_by_Caspar_David_Friedrich.jpg/960px-The_Abbey_in_the_Oakwood_by_Caspar_David_Friedrich.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Abbey_in_the_Oakwood_by_Caspar_David_Friedrich.jpg`.
- Normalized gallery asset: `The Abbey in the Oakwood by Caspar David Friedrich.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/caspar-david-friedrich`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 115. theodore-gericault / The Raft of the Medusa

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `theodore-gericault` → `The Raft of the Medusa`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/JEAN_LOUIS_TH%C3%89ODORE_G%C3%89RICAULT_-_La_Balsa_de_la_Medusa_%28Museo_del_Louvre%2C_1818-19%29.jpg/500px-JEAN_LOUIS_TH%C3%89ODORE_G%C3%89RICAULT_-_La_Balsa_de_la_Medusa_%28Museo_del_Louvre%2C_1818-19%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Raft_of_the_Medusa`.
- Normalized gallery asset: `JEAN LOUIS THÉODORE GÉRICAULT - La Balsa de la Medusa (Museo del Louvre, 1818-19).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `the-raft-of-the-medusa`; title `The Raft of the Medusa`; worksKey `(absent)`; artistId `theodore-gericault`. Evidence: same Commons asset `JEAN LOUIS THÉODORE GÉRICAULT - La Balsa de la Medusa (Museo del Louvre, 1818-19).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/JEAN_LOUIS_TH%C3%89ODORE_G%C3%89RICAULT_-_La_Balsa_de_la_Medusa_%28Museo_del_Louvre%2C_1818-19%29.jpg/500px-JEAN_LOUIS_TH%C3%89ODORE_G%C3%89RICAULT_-_La_Balsa_de_la_Medusa_%28Museo_del_Louvre%2C_1818-19%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:JEAN_LOUIS_TH%C3%89ODORE_G%C3%89RICAULT_-_La_Balsa_de_la_Medusa_(Museo_del_Louvre,_1818-19).jpg`.
- Checked-in route `p/artwork/the-raft-of-the-medusa.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/JEAN_LOUIS_TH%C3%89ODORE_G%C3%89RICAULT_-_La_Balsa_de_la_Medusa_%28Museo_del_Louvre%2C_1818-19%29.jpg/500px-JEAN_LOUIS_TH%C3%89ODORE_G%C3%89RICAULT_-_La_Balsa_de_la_Medusa_%28Museo_del_Louvre%2C_1818-19%29.jpg`.

### 116. theodore-gericault / The Charging Chasseur

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `theodore-gericault` → `The Charging Chasseur`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/GericaultHorseman.jpg/500px-GericaultHorseman.jpg`; page: `https://en.wikipedia.org/wiki/The_Charging_Chasseur`.
- Normalized gallery asset: `GericaultHorseman.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/theodore-gericault`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 117. theodore-gericault / Portraits of the Insane

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `theodore-gericault` → `Portraits of the Insane`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Th%C3%A9odore_G%C3%A9ricault_-_Portrait_of_a_Kleptomaniac_-_1908-F_-_Museum_of_Fine_Arts_Ghent_%28MSK%29.jpg/960px-Th%C3%A9odore_G%C3%A9ricault_-_Portrait_of_a_Kleptomaniac_-_1908-F_-_Museum_of_Fine_Arts_Ghent_%28MSK%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Th%C3%A9odore_G%C3%A9ricault_-_Portrait_of_a_Kleptomaniac_-_1908-F_-_Museum_of_Fine_Arts_Ghent_(MSK).jpg`.
- Normalized gallery asset: `Théodore Géricault - Portrait of a Kleptomaniac - 1908-F - Museum of Fine Arts Ghent (MSK).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/theodore-gericault`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 118. eugene-delacroix / Liberty Leading the People

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `eugene-delacroix` → `Liberty Leading the People`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg/500px-La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg`; page: `https://en.wikipedia.org/wiki/Liberty_Leading_the_People`.
- Normalized gallery asset: `La Liberté guidant le peuple - Eugène Delacroix - Musée du Louvre Peintures RF 129 - après restauration 2024.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-6.js` / `liberty-leading-the-people`; title `Liberty Leading the People`; worksKey `(absent)`; artistId `eugene-delacroix`. Evidence: same Commons asset `La Liberté guidant le peuple - Eugène Delacroix - Musée du Louvre Peintures RF 129 - après restauration 2024.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg/500px-La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg`; page: `https://commons.wikimedia.org/wiki/File:La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg`.
- Checked-in route `p/artwork/liberty-leading-the-people.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg/500px-La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg`.

### 119. eugene-delacroix / The Death of Sardanapalus

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `eugene-delacroix` → `The Death of Sardanapalus`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/La_Mort_de_Sardanapale_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_2346.jpg/500px-La_Mort_de_Sardanapale_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_2346.jpg`; page: `https://en.wikipedia.org/wiki/The_Death_of_Sardanapalus`.
- Normalized gallery asset: `La Mort de Sardanapale - Eugène Delacroix - Musée du Louvre Peintures RF 2346.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/eugene-delacroix`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 120. eugene-delacroix / Women of Algiers

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `eugene-delacroix` → `Women of Algiers`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Femmes_d%27Alger_dans_leur_appartement%2C_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3824.jpg/500px-Femmes_d%27Alger_dans_leur_appartement%2C_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3824.jpg`; page: `https://en.wikipedia.org/wiki/Women_of_Algiers`.
- Normalized gallery asset: `Femmes d'Alger dans leur appartement, Eugène Delacroix - Musée du Louvre Peintures INV 3824.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/eugene-delacroix`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 121. jean-auguste-dominique-ingres / La Grande Odalisque

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jean-auguste-dominique-ingres` → `La Grande Odalisque`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/La_grande_odalisque_-_Jean-Auguste_Dominique_Ingres_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1158.jpg/500px-La_grande_odalisque_-_Jean-Auguste_Dominique_Ingres_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1158.jpg`; page: `https://en.wikipedia.org/wiki/Grande_Odalisque`.
- Normalized gallery asset: `La grande odalisque - Jean-Auguste Dominique Ingres - Musée du Louvre Peintures RF 1158.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-6.js` / `grande-odalisque`; title `Grande Odalisque`; worksKey `La Grande Odalisque`; artistId `jean-auguste-dominique-ingres`. Evidence: same Commons asset `La grande odalisque - Jean-Auguste Dominique Ingres - Musée du Louvre Peintures RF 1158.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/La_grande_odalisque_-_Jean-Auguste_Dominique_Ingres_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1158.jpg/500px-La_grande_odalisque_-_Jean-Auguste_Dominique_Ingres_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1158.jpg`; page: `https://commons.wikimedia.org/wiki/File:La_grande_odalisque_-_Jean-Auguste_Dominique_Ingres_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1158.jpg`.
- Checked-in route `p/artwork/grande-odalisque.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/La_grande_odalisque_-_Jean-Auguste_Dominique_Ingres_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1158.jpg/500px-La_grande_odalisque_-_Jean-Auguste_Dominique_Ingres_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1158.jpg`.

### 122. jean-auguste-dominique-ingres / The Turkish Bath

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jean-auguste-dominique-ingres` → `The Turkish Bath`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Le_Bain_Turc%2C_by_Jean_Auguste_Dominique_Ingres%2C_from_C2RMFFXD.jpg/500px-Le_Bain_Turc%2C_by_Jean_Auguste_Dominique_Ingres%2C_from_C2RMFFXD.jpg`; page: `https://en.wikipedia.org/wiki/The_Turkish_Bath`.
- Normalized gallery asset: `Le Bain Turc, by Jean Auguste Dominique Ingres, from C2RMFFXD.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jean-auguste-dominique-ingres`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 123. jean-auguste-dominique-ingres / Portrait of Comtesse d'Haussonville

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jean-auguste-dominique-ingres` → `Portrait of Comtesse d'Haussonville`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Jean-Auguste-Dominique_Ingres_-_Comtesse_d%27Haussonville_-_Google_Art_Project.jpg/500px-Jean-Auguste-Dominique_Ingres_-_Comtesse_d%27Haussonville_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Portrait_of_Comtesse_d'Haussonville`.
- Normalized gallery asset: `Jean-Auguste-Dominique Ingres - Comtesse d'Haussonville - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jean-auguste-dominique-ingres`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 124. katsushika-hokusai / The Great Wave off Kanagawa

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `katsushika-hokusai` → `The Great Wave off Kanagawa`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Tsunami_by_hokusai_19th_century.jpg/500px-Tsunami_by_hokusai_19th_century.jpg`; page: `https://en.wikipedia.org/wiki/The_Great_Wave_off_Kanagawa`.
- Normalized gallery asset: `Tsunami by hokusai 19th century.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-great-wave-off-kanagawa`; title `The Great Wave off Kanagawa`; worksKey `(absent)`; artistId `katsushika-hokusai`. Evidence: same Commons asset `Tsunami by hokusai 19th century.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Tsunami_by_hokusai_19th_century.jpg/500px-Tsunami_by_hokusai_19th_century.jpg`; page: `https://commons.wikimedia.org/wiki/File:Tsunami_by_hokusai_19th_century.jpg`.
- Checked-in route `p/artwork/the-great-wave-off-kanagawa.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Tsunami_by_hokusai_19th_century.jpg/500px-Tsunami_by_hokusai_19th_century.jpg`.

### 125. katsushika-hokusai / Fine Wind, Clear Morning (Red Fuji)

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `katsushika-hokusai` → `Fine Wind, Clear Morning (Red Fuji)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg/500px-Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Katsushika_Hokusai_-_Fine_Wind,_Clear_Morning_(Gaif%C5%AB_kaisei)_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Katsushika Hokusai - Fine Wind, Clear Morning (Gaifū kaisei) - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `red-fuji`; title `Fine Wind, Clear Morning (Red Fuji)`; worksKey `Fine Wind, Clear Morning (Red Fuji)`; artistId `katsushika-hokusai`. Evidence: same Commons asset `Katsushika Hokusai - Fine Wind, Clear Morning (Gaifū kaisei) - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg/500px-Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Katsushika_Hokusai_-_Fine_Wind,_Clear_Morning_(Gaif%C5%AB_kaisei)_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/red-fuji.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg/500px-Katsushika_Hokusai_-_Fine_Wind%2C_Clear_Morning_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg`.

### 126. katsushika-hokusai / Hokusai Manga

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `katsushika-hokusai` → `Hokusai Manga`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Hokusai-MangaBathingPeople.jpg/500px-Hokusai-MangaBathingPeople.jpg`; page: `https://en.wikipedia.org/wiki/Hokusai_Manga`.
- Normalized gallery asset: `Hokusai-MangaBathingPeople.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `hokusai-manga`; title `Hokusai Manga`; worksKey `Hokusai Manga`; artistId `katsushika-hokusai`. Evidence: same Commons asset `Hokusai-MangaBathingPeople.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Hokusai-MangaBathingPeople.jpg/500px-Hokusai-MangaBathingPeople.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hokusai-MangaBathingPeople.jpg`.
- Checked-in route `p/artwork/hokusai-manga.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Hokusai-MangaBathingPeople.jpg/500px-Hokusai-MangaBathingPeople.jpg`.

### 127. gustave-courbet / A Burial at Ornans

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `gustave-courbet` → `A Burial at Ornans`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Gustave_Courbet_-_A_Burial_at_Ornans_-_Google_Art_Project_2.jpg/500px-Gustave_Courbet_-_A_Burial_at_Ornans_-_Google_Art_Project_2.jpg`; page: `https://en.wikipedia.org/wiki/A_Burial_at_Ornans`.
- Normalized gallery asset: `Gustave Courbet - A Burial at Ornans - Google Art Project 2.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `a-burial-at-ornans`; title `A Burial at Ornans`; worksKey `(absent)`; artistId `gustave-courbet`. Evidence: same Commons asset `Gustave Courbet - A Burial at Ornans - Google Art Project 2.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Gustave_Courbet_-_A_Burial_at_Ornans_-_Google_Art_Project_2.jpg/500px-Gustave_Courbet_-_A_Burial_at_Ornans_-_Google_Art_Project_2.jpg`; page: `https://commons.wikimedia.org/wiki/File:Gustave_Courbet_-_A_Burial_at_Ornans_-_Google_Art_Project_2.jpg`.
- Checked-in route `p/artwork/a-burial-at-ornans.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Gustave_Courbet_-_A_Burial_at_Ornans_-_Google_Art_Project_2.jpg/500px-Gustave_Courbet_-_A_Burial_at_Ornans_-_Google_Art_Project_2.jpg`.

### 128. gustave-courbet / The Stone Breakers

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `gustave-courbet` → `The Stone Breakers`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Gustave_Courbet_-_The_Stonebreakers_-_WGA05457.jpg/500px-Gustave_Courbet_-_The_Stonebreakers_-_WGA05457.jpg`; page: `https://en.wikipedia.org/wiki/The_Stone_Breakers`.
- Normalized gallery asset: `Gustave Courbet - The Stonebreakers - WGA05457.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/gustave-courbet`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 129. gustave-courbet / The Artist's Studio

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `gustave-courbet` → `The Artist's Studio`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Courbet_LAtelier_du_peintre.jpg/500px-Courbet_LAtelier_du_peintre.jpg`; page: `https://en.wikipedia.org/wiki/The_Painter's_Studio`.
- Normalized gallery asset: `Courbet LAtelier du peintre.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/gustave-courbet`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 130. jean-francois-millet / The Gleaners

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jean-francois-millet` → `The Gleaners`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Jean-Fran%C3%A7ois_Millet_-_Gleaners_-_Google_Art_Project_2.jpg/500px-Jean-Fran%C3%A7ois_Millet_-_Gleaners_-_Google_Art_Project_2.jpg`; page: `https://en.wikipedia.org/wiki/The_Gleaners`.
- Normalized gallery asset: `Jean-François Millet - Gleaners - Google Art Project 2.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-7.js` / `the-gleaners`; title `The Gleaners`; worksKey `(absent)`; artistId `jean-francois-millet`. Evidence: same Commons asset `Jean-François Millet - Gleaners - Google Art Project 2.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Jean-Fran%C3%A7ois_Millet_-_Gleaners_-_Google_Art_Project_2.jpg/500px-Jean-Fran%C3%A7ois_Millet_-_Gleaners_-_Google_Art_Project_2.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jean-Fran%C3%A7ois_Millet_-_Gleaners_-_Google_Art_Project_2.jpg`.
- Checked-in route `p/artwork/the-gleaners.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Jean-Fran%C3%A7ois_Millet_-_Gleaners_-_Google_Art_Project_2.jpg/500px-Jean-Fran%C3%A7ois_Millet_-_Gleaners_-_Google_Art_Project_2.jpg`.

### 131. jean-francois-millet / The Angelus

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jean-francois-millet` → `The Angelus`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/JEAN-FRAN%C3%87OIS_MILLET_-_El_%C3%81ngelus_%28Museo_de_Orsay%2C_1857-1859._%C3%93leo_sobre_lienzo%2C_55.5_x_66_cm%29.jpg/500px-JEAN-FRAN%C3%87OIS_MILLET_-_El_%C3%81ngelus_%28Museo_de_Orsay%2C_1857-1859._%C3%93leo_sobre_lienzo%2C_55.5_x_66_cm%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Angelus_(painting)`.
- Normalized gallery asset: `JEAN-FRANÇOIS MILLET - El Ángelus (Museo de Orsay, 1857-1859. Óleo sobre lienzo, 55.5 x 66 cm).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jean-francois-millet`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 132. jean-francois-millet / The Sower

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jean-francois-millet` → `The Sower`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Jean-Fran%C3%A7ois_Millet_-_The_Sower_-_Google_Art_Project.jpg/500px-Jean-Fran%C3%A7ois_Millet_-_The_Sower_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Sower_(Millet)`.
- Normalized gallery asset: `Jean-François Millet - The Sower - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jean-francois-millet`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 133. edouard-manet / Olympia

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `edouard-manet` → `Olympia`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Edouard_Manet_-_Olympia_-_Google_Art_ProjectFXD.jpg/500px-Edouard_Manet_-_Olympia_-_Google_Art_ProjectFXD.jpg`; page: `https://en.wikipedia.org/wiki/Olympia_(Manet)`.
- Normalized gallery asset: `Edouard Manet - Olympia - Google Art ProjectFXD.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `olympia`; title `Olympia`; worksKey `Olympia`; artistId `edouard-manet`. Evidence: same Commons asset `Edouard Manet - Olympia - Google Art ProjectFXD.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Edouard_Manet_-_Olympia_-_Google_Art_ProjectFXD.jpg/500px-Edouard_Manet_-_Olympia_-_Google_Art_ProjectFXD.jpg`; page: `https://commons.wikimedia.org/wiki/File:Edouard_Manet_-_Olympia_-_Google_Art_ProjectFXD.jpg`.
- Checked-in route `p/artwork/olympia.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Edouard_Manet_-_Olympia_-_Google_Art_ProjectFXD.jpg/500px-Edouard_Manet_-_Olympia_-_Google_Art_ProjectFXD.jpg`.

### 134. edouard-manet / Le Déjeuner sur l'herbe

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `edouard-manet` → `Le Déjeuner sur l'herbe`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Edouard_Manet_-_Luncheon_on_the_Grass_-_Google_Art_Project.jpg/500px-Edouard_Manet_-_Luncheon_on_the_Grass_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Le_D%C3%A9jeuner_sur_l'herbe`.
- Normalized gallery asset: `Edouard Manet - Luncheon on the Grass - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `le-dejeuner-sur-lherbe`; title `Le Déjeuner sur l'herbe`; worksKey `Le Déjeuner sur l'herbe`; artistId `edouard-manet`. Evidence: same Commons asset `Edouard Manet - Luncheon on the Grass - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Edouard_Manet_-_Luncheon_on_the_Grass_-_Google_Art_Project.jpg/500px-Edouard_Manet_-_Luncheon_on_the_Grass_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Edouard_Manet_-_Luncheon_on_the_Grass_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/le-dejeuner-sur-lherbe.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Edouard_Manet_-_Luncheon_on_the_Grass_-_Google_Art_Project.jpg/500px-Edouard_Manet_-_Luncheon_on_the_Grass_-_Google_Art_Project.jpg`.

### 135. edouard-manet / A Bar at the Folies-Bergère

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `edouard-manet` → `A Bar at the Folies-Bergère`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/%22Un_Bar_aux_Folies-Berg%C3%A8re%22_by_%C3%89douard_Manet_%281882%29.jpg/500px-%22Un_Bar_aux_Folies-Berg%C3%A8re%22_by_%C3%89douard_Manet_%281882%29.jpg`; page: `https://en.wikipedia.org/wiki/A_Bar_at_the_Folies-Berg%C3%A8re`.
- Normalized gallery asset: `"Un Bar aux Folies-Bergère" by Édouard Manet (1882).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `a-bar-at-the-folies-bergere`; title `A Bar at the Folies-Bergère`; worksKey `A Bar at the Folies-Bergère`; artistId `edouard-manet`. Evidence: same Commons asset `"Un Bar aux Folies-Bergère" by Édouard Manet (1882).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/%22Un_Bar_aux_Folies-Berg%C3%A8re%22_by_%C3%89douard_Manet_%281882%29.jpg/500px-%22Un_Bar_aux_Folies-Berg%C3%A8re%22_by_%C3%89douard_Manet_%281882%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:%22Un_Bar_aux_Folies-Berg%C3%A8re%22_by_%C3%89douard_Manet_(1882).jpg`.
- Checked-in route `p/artwork/a-bar-at-the-folies-bergere.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/%22Un_Bar_aux_Folies-Berg%C3%A8re%22_by_%C3%89douard_Manet_%281882%29.jpg/500px-%22Un_Bar_aux_Folies-Berg%C3%A8re%22_by_%C3%89douard_Manet_%281882%29.jpg`.

### 136. claude-monet / Impression, Sunrise

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `claude-monet` → `Impression, Sunrise`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Monet_-_Impression%2C_Sunrise.jpg/500px-Monet_-_Impression%2C_Sunrise.jpg`; page: `https://en.wikipedia.org/wiki/Impression%2C_Sunrise`.
- Normalized gallery asset: `Monet - Impression, Sunrise.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `impression-sunrise`; title `Impression, Sunrise`; worksKey `(absent)`; artistId `claude-monet`. Evidence: same Commons asset `Monet - Impression, Sunrise.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Monet_-_Impression%2C_Sunrise.jpg/500px-Monet_-_Impression%2C_Sunrise.jpg`; page: `https://commons.wikimedia.org/wiki/File:Monet_-_Impression,_Sunrise.jpg`.
- Checked-in route `p/artwork/impression-sunrise.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Monet_-_Impression%2C_Sunrise.jpg/500px-Monet_-_Impression%2C_Sunrise.jpg`.

### 137. claude-monet / Rouen Cathedral series

- Classification: **AMBIGUOUS**.
- Gallery source: `js/artworks.js` → `claude-monet` → `Rouen Cathedral series`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/RouenCathedral_Monet_1894.jpg/500px-RouenCathedral_Monet_1894.jpg`; page: `https://en.wikipedia.org/wiki/Rouen_Cathedral_(Monet_series)`.
- Normalized gallery asset: `RouenCathedral Monet 1894.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/claude-monet`. Do not invent a slug from the gallery title.
- Unconfirmed same-artist title candidates: `rouen-cathedral-full-sunlight` (js/catalog-1.js), title `Rouen Cathedral, Full Sunlight (Harmony in Blue and Gold)`, worksKey `Rouen Cathedral series`. A partial or series-level title does not establish individual artwork identity.
- Candidate asset evidence for `rouen-cathedral-full-sunlight` (not a confirmed match): src `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Claude_Monet_-_Cath%C3%A9drale_de_Rouen._Harmonie_bleue_et_or.jpg/500px-Claude_Monet_-_Cath%C3%A9drale_de_Rouen._Harmonie_bleue_et_or.jpg`; page `https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Cath%C3%A9drale_de_Rouen._Harmonie_bleue_et_or.jpg`; normalized asset `Claude Monet - Cathédrale de Rouen. Harmonie bleue et or.jpg`.
- Series ambiguity: gallery page identifies the series; its file name does not establish the catalog’s Full Sunlight (Harmony in Blue and Gold) version.

### 138. claude-monet / Water Lilies (Grandes Décorations)

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `claude-monet` → `Water Lilies (Grandes Décorations)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Claude_Monet_-_The_Water_Lilies_-_Setting_Sun_-_Google_Art_Project.jpg/500px-Claude_Monet_-_The_Water_Lilies_-_Setting_Sun_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Claude_Monet_-_The_Water_Lilies_-_Setting_Sun_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Claude Monet - The Water Lilies - Setting Sun - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `water-lilies-grandes-decorations`; title `Water Lilies (Grandes Décorations)`; worksKey `Water Lilies (Grandes Décorations)`; artistId `claude-monet`. Evidence: same Commons asset `Claude Monet - The Water Lilies - Setting Sun - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Claude_Monet_-_The_Water_Lilies_-_Setting_Sun_-_Google_Art_Project.jpg/500px-Claude_Monet_-_The_Water_Lilies_-_Setting_Sun_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Claude_Monet_-_The_Water_Lilies_-_Setting_Sun_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/water-lilies-grandes-decorations.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Claude_Monet_-_The_Water_Lilies_-_Setting_Sun_-_Google_Art_Project.jpg/500px-Claude_Monet_-_The_Water_Lilies_-_Setting_Sun_-_Google_Art_Project.jpg`.

### 139. claude-monet / Haystacks series

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `claude-monet` → `Haystacks series`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Claude_Monet_-_Stacks_of_Wheat_%28End_of_Summer%29_-_1985.1103_-_Art_Institute_of_Chicago.jpg/500px-Claude_Monet_-_Stacks_of_Wheat_%28End_of_Summer%29_-_1985.1103_-_Art_Institute_of_Chicago.jpg`; page: `https://en.wikipedia.org/wiki/Haystacks_(Monet_series)`.
- Normalized gallery asset: `Claude Monet - Stacks of Wheat (End of Summer) - 1985.1103 - Art Institute of Chicago.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `grainstacks`; title `Stacks of Wheat (End of Summer)`; worksKey `Haystacks series`; artistId `claude-monet`. Evidence: same Commons asset `Claude Monet - Stacks of Wheat (End of Summer) - 1985.1103 - Art Institute of Chicago.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Claude_Monet_-_Stacks_of_Wheat_%28End_of_Summer%29_-_1985.1103_-_Art_Institute_of_Chicago.jpg/500px-Claude_Monet_-_Stacks_of_Wheat_%28End_of_Summer%29_-_1985.1103_-_Art_Institute_of_Chicago.jpg`; page: `https://commons.wikimedia.org/wiki/File:Claude_Monet_-_Stacks_of_Wheat_(End_of_Summer)_-_1985.1103_-_Art_Institute_of_Chicago.jpg`.
- Checked-in route `p/artwork/grainstacks.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Claude_Monet_-_Stacks_of_Wheat_%28End_of_Summer%29_-_1985.1103_-_Art_Institute_of_Chicago.jpg/500px-Claude_Monet_-_Stacks_of_Wheat_%28End_of_Summer%29_-_1985.1103_-_Art_Institute_of_Chicago.jpg`.

### 140. pierre-auguste-renoir / Bal du moulin de la Galette

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `pierre-auguste-renoir` → `Bal du moulin de la Galette`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Renoir%2C_Pierre-Auguste_-_Dance_at_Le_Moulin_de_la_Galette%2C_1876.jpg/500px-Renoir%2C_Pierre-Auguste_-_Dance_at_Le_Moulin_de_la_Galette%2C_1876.jpg`; page: `https://en.wikipedia.org/wiki/Bal_du_moulin_de_la_Galette`.
- Normalized gallery asset: `Renoir, Pierre-Auguste - Dance at Le Moulin de la Galette, 1876.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-7.js` / `bal-du-moulin-de-la-galette`; title `Bal du moulin de la Galette`; worksKey `(absent)`; artistId `pierre-auguste-renoir`. Evidence: same Commons asset `Renoir, Pierre-Auguste - Dance at Le Moulin de la Galette, 1876.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Renoir%2C_Pierre-Auguste_-_Dance_at_Le_Moulin_de_la_Galette%2C_1876.jpg/500px-Renoir%2C_Pierre-Auguste_-_Dance_at_Le_Moulin_de_la_Galette%2C_1876.jpg`; page: `https://commons.wikimedia.org/wiki/File:Renoir,_Pierre-Auguste_-_Dance_at_Le_Moulin_de_la_Galette,_1876.jpg`.
- Checked-in route `p/artwork/bal-du-moulin-de-la-galette.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Renoir%2C_Pierre-Auguste_-_Dance_at_Le_Moulin_de_la_Galette%2C_1876.jpg/500px-Renoir%2C_Pierre-Auguste_-_Dance_at_Le_Moulin_de_la_Galette%2C_1876.jpg`.

### 141. pierre-auguste-renoir / Luncheon of the Boating Party

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `pierre-auguste-renoir` → `Luncheon of the Boating Party`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Pierre-Auguste_Renoir_-_Luncheon_of_the_Boating_Party_-_Google_Art_Project.jpg/500px-Pierre-Auguste_Renoir_-_Luncheon_of_the_Boating_Party_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Luncheon_of_the_Boating_Party`.
- Normalized gallery asset: `Pierre-Auguste Renoir - Luncheon of the Boating Party - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/pierre-auguste-renoir`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 142. pierre-auguste-renoir / The Umbrellas

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `pierre-auguste-renoir` → `The Umbrellas`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Pierre-Auguste_Renoir%2C_The_Umbrellas%2C_ca._1881-86.jpg/500px-Pierre-Auguste_Renoir%2C_The_Umbrellas%2C_ca._1881-86.jpg`; page: `https://en.wikipedia.org/wiki/The_Umbrellas_(Renoir)`.
- Normalized gallery asset: `Pierre-Auguste Renoir, The Umbrellas, ca. 1881-86.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/pierre-auguste-renoir`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 143. edgar-degas / The Dance Class

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `edgar-degas` → `The Dance Class`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Edgar_Degas_-_La_Classe_de_danse.jpg/500px-Edgar_Degas_-_La_Classe_de_danse.jpg`; page: `https://en.wikipedia.org/wiki/The_Ballet_Class_(Degas%2C_Mus%C3%A9e_d'Orsay)`.
- Normalized gallery asset: `Edgar Degas - La Classe de danse.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `the-dance-class`; title `The Dance Class`; worksKey `The Dance Class`; artistId `edgar-degas`. Evidence: same Commons asset `Edgar Degas - La Classe de danse.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Edgar_Degas_-_La_Classe_de_danse.jpg/500px-Edgar_Degas_-_La_Classe_de_danse.jpg`; page: `https://commons.wikimedia.org/wiki/File:Edgar_Degas_-_La_Classe_de_danse.jpg`.
- Checked-in route `p/artwork/the-dance-class.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Edgar_Degas_-_La_Classe_de_danse.jpg/500px-Edgar_Degas_-_La_Classe_de_danse.jpg`.

### 144. edgar-degas / L'Absinthe

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `edgar-degas` → `L'Absinthe`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Edgar_Degas_-_In_a_Caf%C3%A9_-_Google_Art_Project_2.jpg/500px-Edgar_Degas_-_In_a_Caf%C3%A9_-_Google_Art_Project_2.jpg`; page: `https://en.wikipedia.org/wiki/L'Absinthe`.
- Normalized gallery asset: `Edgar Degas - In a Café - Google Art Project 2.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `labsinthe`; title `L'Absinthe`; worksKey `L'Absinthe`; artistId `edgar-degas`. Evidence: same Commons asset `Edgar Degas - In a Café - Google Art Project 2.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Edgar_Degas_-_In_a_Caf%C3%A9_-_Google_Art_Project_2.jpg/500px-Edgar_Degas_-_In_a_Caf%C3%A9_-_Google_Art_Project_2.jpg`; page: `https://commons.wikimedia.org/wiki/File:Edgar_Degas_-_In_a_Caf%C3%A9_-_Google_Art_Project_2.jpg`.
- Checked-in route `p/artwork/labsinthe.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Edgar_Degas_-_In_a_Caf%C3%A9_-_Google_Art_Project_2.jpg/500px-Edgar_Degas_-_In_a_Caf%C3%A9_-_Google_Art_Project_2.jpg`.

### 145. edgar-degas / Little Dancer Aged Fourteen

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `edgar-degas` → `Little Dancer Aged Fourteen`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Degas_Little_Dancer_PMA%2805c%29_%2815675423180%29.jpg/500px-Degas_Little_Dancer_PMA%2805c%29_%2815675423180%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Degas_Little_Dancer_PMA(05c)_(15675423180).jpg`.
- Normalized gallery asset: `Degas Little Dancer PMA(05c) (15675423180).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `little-dancer-aged-fourteen`; title `Little Dancer Aged Fourteen`; worksKey `Little Dancer Aged Fourteen`; artistId `edgar-degas`. Evidence: same Commons asset `Degas Little Dancer PMA(05c) (15675423180).jpg`.
- Catalog image.status: `licensed`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Degas_Little_Dancer_PMA%2805c%29_%2815675423180%29.jpg/500px-Degas_Little_Dancer_PMA%2805c%29_%2815675423180%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Degas_Little_Dancer_PMA(05c)_(15675423180).jpg`.
- Checked-in route `p/artwork/little-dancer-aged-fourteen.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Degas_Little_Dancer_PMA%2805c%29_%2815675423180%29.jpg/500px-Degas_Little_Dancer_PMA%2805c%29_%2815675423180%29.jpg`.

### 146. edgar-degas / Woman Combing Her Hair

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `edgar-degas` → `Woman Combing Her Hair`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/%28Albi%29_Femme_nue%2C_assise_par_terre_se_peignant_-_Edgar_Degas_-_Mus%C3%A9e_d%27Orsay.jpg/960px-%28Albi%29_Femme_nue%2C_assise_par_terre_se_peignant_-_Edgar_Degas_-_Mus%C3%A9e_d%27Orsay.jpg`; page: `https://commons.wikimedia.org/wiki/File:(Albi)_Femme_nue,_assise_par_terre_se_peignant_-_Edgar_Degas_-_Mus%C3%A9e_d%27Orsay.jpg`.
- Normalized gallery asset: `(Albi) Femme nue, assise par terre se peignant - Edgar Degas - Musée d'Orsay.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `woman-combing-her-hair`; title `Woman Combing Her Hair`; worksKey `Woman Combing Her Hair`; artistId `edgar-degas`. Evidence: same Commons asset `(Albi) Femme nue, assise par terre se peignant - Edgar Degas - Musée d'Orsay.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/%28Albi%29_Femme_nue%2C_assise_par_terre_se_peignant_-_Edgar_Degas_-_Mus%C3%A9e_d%27Orsay.jpg/500px-%28Albi%29_Femme_nue%2C_assise_par_terre_se_peignant_-_Edgar_Degas_-_Mus%C3%A9e_d%27Orsay.jpg`; page: `https://commons.wikimedia.org/wiki/File:(Albi)_Femme_nue,_assise_par_terre_se_peignant_-_Edgar_Degas_-_Mus%C3%A9e_d%27Orsay.jpg`.
- Checked-in route `p/artwork/woman-combing-her-hair.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/%28Albi%29_Femme_nue%2C_assise_par_terre_se_peignant_-_Edgar_Degas_-_Mus%C3%A9e_d%27Orsay.jpg/500px-%28Albi%29_Femme_nue%2C_assise_par_terre_se_peignant_-_Edgar_Degas_-_Mus%C3%A9e_d%27Orsay.jpg`.

### 147. camille-pissarro / Boulevard Montmartre at Night

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `camille-pissarro` → `Boulevard Montmartre at Night`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Camille_Pissarro%2C_The_Boulevard_Montmartre_at_Night%2C_1897.jpg/960px-Camille_Pissarro%2C_The_Boulevard_Montmartre_at_Night%2C_1897.jpg`; page: `https://commons.wikimedia.org/wiki/File:Camille_Pissarro,_The_Boulevard_Montmartre_at_Night,_1897.jpg`.
- Normalized gallery asset: `Camille Pissarro, The Boulevard Montmartre at Night, 1897.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-6.js` / `the-boulevard-montmartre-at-night`; title `The Boulevard Montmartre at Night`; worksKey `Boulevard Montmartre at Night`; artistId `camille-pissarro`. Evidence: same Commons asset `Camille Pissarro, The Boulevard Montmartre at Night, 1897.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Camille_Pissarro%2C_The_Boulevard_Montmartre_at_Night%2C_1897.jpg/960px-Camille_Pissarro%2C_The_Boulevard_Montmartre_at_Night%2C_1897.jpg`; page: `https://commons.wikimedia.org/wiki/File:Camille_Pissarro,_The_Boulevard_Montmartre_at_Night,_1897.jpg`.
- Checked-in route `p/artwork/the-boulevard-montmartre-at-night.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Camille_Pissarro%2C_The_Boulevard_Montmartre_at_Night%2C_1897.jpg/960px-Camille_Pissarro%2C_The_Boulevard_Montmartre_at_Night%2C_1897.jpg`.

### 148. camille-pissarro / The Red Roofs

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `camille-pissarro` → `The Red Roofs`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Camille_Pissarro_-_Red_roofs%2C_corner_of_a_village%2C_winter_-_Google_Art_Project.jpg/960px-Camille_Pissarro_-_Red_roofs%2C_corner_of_a_village%2C_winter_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Camille_Pissarro_-_Red_roofs,_corner_of_a_village,_winter_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Camille Pissarro - Red roofs, corner of a village, winter - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/camille-pissarro`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 149. camille-pissarro / Hoarfrost

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `camille-pissarro` → `Hoarfrost`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Hoarfrost%2C_Peasant_Girl_Making_a_Fire_by_Camille_Pissarro.jpg/960px-Hoarfrost%2C_Peasant_Girl_Making_a_Fire_by_Camille_Pissarro.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hoarfrost,_Peasant_Girl_Making_a_Fire_by_Camille_Pissarro.jpg`.
- Normalized gallery asset: `Hoarfrost, Peasant Girl Making a Fire by Camille Pissarro.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/camille-pissarro`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 150. berthe-morisot / The Cradle

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `berthe-morisot` → `The Cradle`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Berthe_Morisot_008.jpg/500px-Berthe_Morisot_008.jpg`; page: `https://en.wikipedia.org/wiki/The_Cradle_(Morisot)`.
- Normalized gallery asset: `Berthe Morisot 008.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-8.js` / `the-cradle`; title `The Cradle`; worksKey `(absent)`; artistId `berthe-morisot`. Evidence: same Commons asset `Berthe Morisot 008.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Berthe_Morisot_008.jpg/500px-Berthe_Morisot_008.jpg`; page: `https://commons.wikimedia.org/wiki/File:Berthe_Morisot_008.jpg`.
- Checked-in route `p/artwork/the-cradle.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Berthe_Morisot_008.jpg/500px-Berthe_Morisot_008.jpg`.

### 151. berthe-morisot / Summer's Day

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `berthe-morisot` → `Summer's Day`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Berthe_Morisot_-_Jour_d%27%C3%A9t%C3%A9%2C_1879.jpg/500px-Berthe_Morisot_-_Jour_d%27%C3%A9t%C3%A9%2C_1879.jpg`; page: `https://en.wikipedia.org/wiki/Summer's_Day`.
- Normalized gallery asset: `Berthe Morisot - Jour d'été, 1879.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/berthe-morisot`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 152. berthe-morisot / Young Woman Powdering Her Face

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `berthe-morisot` → `Young Woman Powdering Her Face`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Morisot_jeune_femme_se_poudrant.jpg/500px-Morisot_jeune_femme_se_poudrant.jpg`; page: `https://commons.wikimedia.org/wiki/File:Morisot_jeune_femme_se_poudrant.jpg`.
- Normalized gallery asset: `Morisot jeune femme se poudrant.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/berthe-morisot`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 153. mary-cassatt / The Child's Bath

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `mary-cassatt` → `The Child's Bath`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Mary_Cassatt_-_The_Child%27s_Bath_-_Google_Art_Project.jpg/500px-Mary_Cassatt_-_The_Child%27s_Bath_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Child's_Bath`.
- Normalized gallery asset: `Mary Cassatt - The Child's Bath - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `the-childs-bath`; title `The Child's Bath`; worksKey `The Child's Bath`; artistId `mary-cassatt`. Evidence: same Commons asset `Mary Cassatt - The Child's Bath - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Mary_Cassatt_-_The_Child%27s_Bath_-_Google_Art_Project.jpg/500px-Mary_Cassatt_-_The_Child%27s_Bath_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Mary_Cassatt_-_The_Child%27s_Bath_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/the-childs-bath.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Mary_Cassatt_-_The_Child%27s_Bath_-_Google_Art_Project.jpg/500px-Mary_Cassatt_-_The_Child%27s_Bath_-_Google_Art_Project.jpg`.

### 154. mary-cassatt / Little Girl in a Blue Armchair

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `mary-cassatt` → `Little Girl in a Blue Armchair`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Cassatt_Mary_Little_Girl_in_a_blue_armchair_Sun_Unedited_1878.jpg/500px-Cassatt_Mary_Little_Girl_in_a_blue_armchair_Sun_Unedited_1878.jpg`; page: `https://commons.wikimedia.org/wiki/File:Cassatt_Mary_Little_Girl_in_a_blue_armchair_Sun_Unedited_1878.jpg`.
- Normalized gallery asset: `Cassatt Mary Little Girl in a blue armchair Sun Unedited 1878.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `little-girl-in-a-blue-armchair`; title `Little Girl in a Blue Armchair`; worksKey `Little Girl in a Blue Armchair`; artistId `mary-cassatt`. Evidence: same Commons asset `Cassatt Mary Little Girl in a blue armchair Sun Unedited 1878.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Cassatt_Mary_Little_Girl_in_a_blue_armchair_Sun_Unedited_1878.jpg/500px-Cassatt_Mary_Little_Girl_in_a_blue_armchair_Sun_Unedited_1878.jpg`; page: `https://commons.wikimedia.org/wiki/File:Cassatt_Mary_Little_Girl_in_a_blue_armchair_Sun_Unedited_1878.jpg`.
- Checked-in route `p/artwork/little-girl-in-a-blue-armchair.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Cassatt_Mary_Little_Girl_in_a_blue_armchair_Sun_Unedited_1878.jpg/500px-Cassatt_Mary_Little_Girl_in_a_blue_armchair_Sun_Unedited_1878.jpg`.

### 155. mary-cassatt / The Boating Party

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `mary-cassatt` → `The Boating Party`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Mary_Cassatt_-_The_Boating_Party_-_Google_Art_Project.jpg/500px-Mary_Cassatt_-_The_Boating_Party_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Boating_Party`.
- Normalized gallery asset: `Mary Cassatt - The Boating Party - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `the-boating-party`; title `The Boating Party`; worksKey `The Boating Party`; artistId `mary-cassatt`. Evidence: same Commons asset `Mary Cassatt - The Boating Party - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Mary_Cassatt_-_The_Boating_Party_-_Google_Art_Project.jpg/500px-Mary_Cassatt_-_The_Boating_Party_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Mary_Cassatt_-_The_Boating_Party_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/the-boating-party.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Mary_Cassatt_-_The_Boating_Party_-_Google_Art_Project.jpg/500px-Mary_Cassatt_-_The_Boating_Party_-_Google_Art_Project.jpg`.

### 156. james-whistler / Arrangement in Grey and Black No. 1 (Whistler's Mother)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `james-whistler` → `Arrangement in Grey and Black No. 1 (Whistler's Mother)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Whistlers_Mother_high_res.jpg/500px-Whistlers_Mother_high_res.jpg`; page: `https://en.wikipedia.org/wiki/Whistler's_Mother`.
- Normalized gallery asset: `Whistlers Mother high res.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/james-whistler`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 157. james-whistler / Nocturne in Black and Gold — The Falling Rocket

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `james-whistler` → `Nocturne in Black and Gold — The Falling Rocket`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Whistler-Nocturne_in_black_and_gold.jpg/960px-Whistler-Nocturne_in_black_and_gold.jpg`; page: `https://commons.wikimedia.org/wiki/File:Whistler-Nocturne_in_black_and_gold.jpg`.
- Normalized gallery asset: `Whistler-Nocturne in black and gold.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-4.js` / `nocturne-in-black-and-gold`; title `Nocturne in Black and Gold — The Falling Rocket`; worksKey `Nocturne in Black and Gold — The Falling Rocket`; artistId `james-whistler`. Evidence: same Commons asset `Whistler-Nocturne in black and gold.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Whistler-Nocturne_in_black_and_gold.jpg/500px-Whistler-Nocturne_in_black_and_gold.jpg`; page: `https://commons.wikimedia.org/wiki/File:Whistler-Nocturne_in_black_and_gold.jpg`.
- Checked-in route `p/artwork/nocturne-in-black-and-gold.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Whistler-Nocturne_in_black_and_gold.jpg/500px-Whistler-Nocturne_in_black_and_gold.jpg`.

### 158. james-whistler / Symphony in White, No. 1

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `james-whistler` → `Symphony in White, No. 1`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Whistler_James_Symphony_in_White_no_1_%28The_White_Girl%29_1862.jpg/500px-Whistler_James_Symphony_in_White_no_1_%28The_White_Girl%29_1862.jpg`; page: `https://en.wikipedia.org/wiki/Symphony_in_White%2C_No._1%3A_The_White_Girl`.
- Normalized gallery asset: `Whistler James Symphony in White no 1 (The White Girl) 1862.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/james-whistler`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 159. john-singer-sargent / Madame X

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `john-singer-sargent` → `Madame X`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Madame_X_%28Madame_Pierre_Gautreau%29%2C_John_Singer_Sargent%2C_1884_%28unfree_frame_crop%29.jpg/960px-Madame_X_%28Madame_Pierre_Gautreau%29%2C_John_Singer_Sargent%2C_1884_%28unfree_frame_crop%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Madame_X_(Madame_Pierre_Gautreau),_John_Singer_Sargent,_1884_(unfree_frame_crop).jpg`.
- Normalized gallery asset: `Madame X (Madame Pierre Gautreau), John Singer Sargent, 1884 (unfree frame crop).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-6.js` / `madame-x`; title `Madame X`; worksKey `(absent)`; artistId `john-singer-sargent`. Evidence: same Commons asset `Madame X (Madame Pierre Gautreau), John Singer Sargent, 1884 (unfree frame crop).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Madame_X_%28Madame_Pierre_Gautreau%29%2C_John_Singer_Sargent%2C_1884_%28unfree_frame_crop%29.jpg/960px-Madame_X_%28Madame_Pierre_Gautreau%29%2C_John_Singer_Sargent%2C_1884_%28unfree_frame_crop%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Madame_X_(Madame_Pierre_Gautreau),_John_Singer_Sargent,_1884_(unfree_frame_crop).jpg`.
- Checked-in route `p/artwork/madame-x.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Madame_X_%28Madame_Pierre_Gautreau%29%2C_John_Singer_Sargent%2C_1884_%28unfree_frame_crop%29.jpg/960px-Madame_X_%28Madame_Pierre_Gautreau%29%2C_John_Singer_Sargent%2C_1884_%28unfree_frame_crop%29.jpg`.

### 160. john-singer-sargent / Carnation, Lily, Lily, Rose

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `john-singer-sargent` → `Carnation, Lily, Lily, Rose`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/John_Singer_Sargent_-_Carnation%2C_Lily%2C_Lily%2C_Rose_-_Google_Art_Project.jpg/500px-John_Singer_Sargent_-_Carnation%2C_Lily%2C_Lily%2C_Rose_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Carnation%2C_Lily%2C_Lily%2C_Rose`.
- Normalized gallery asset: `John Singer Sargent - Carnation, Lily, Lily, Rose - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/john-singer-sargent`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 161. john-singer-sargent / The Daughters of Edward Darley Boit

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `john-singer-sargent` → `The Daughters of Edward Darley Boit`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/The_Daughters_of_Edward_Darley_Boit%2C_John_Singer_Sargent%2C_1882_%28unfree_frame_crop%29.jpg/500px-The_Daughters_of_Edward_Darley_Boit%2C_John_Singer_Sargent%2C_1882_%28unfree_frame_crop%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Daughters_of_Edward_Darley_Boit`.
- Normalized gallery asset: `The Daughters of Edward Darley Boit, John Singer Sargent, 1882 (unfree frame crop).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/john-singer-sargent`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 162. vincent-van-gogh / The Starry Night

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `vincent-van-gogh` → `The Starry Night`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/500px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Starry_Night`.
- Normalized gallery asset: `Van Gogh - Starry Night - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-starry-night`; title `The Starry Night`; worksKey `(absent)`; artistId `vincent-van-gogh`. Evidence: same Commons asset `Van Gogh - Starry Night - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/500px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/the-starry-night.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/500px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg`.

### 163. vincent-van-gogh / Sunflowers

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `vincent-van-gogh` → `Sunflowers`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Vincent_Willem_van_Gogh_127.jpg/500px-Vincent_Willem_van_Gogh_127.jpg`; page: `https://en.wikipedia.org/wiki/Sunflowers_(Van_Gogh_series)`.
- Normalized gallery asset: `Vincent Willem van Gogh 127.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `sunflowers`; title `Sunflowers`; worksKey `(absent)`; artistId `vincent-van-gogh`. Evidence: same Commons asset `Vincent Willem van Gogh 127.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Vincent_Willem_van_Gogh_127.jpg/500px-Vincent_Willem_van_Gogh_127.jpg`; page: `https://commons.wikimedia.org/wiki/File:Vincent_Willem_van_Gogh_127.jpg`.
- Checked-in route `p/artwork/sunflowers.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Vincent_Willem_van_Gogh_127.jpg/500px-Vincent_Willem_van_Gogh_127.jpg`.

### 164. vincent-van-gogh / The Potato Eaters

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `vincent-van-gogh` → `The Potato Eaters`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/De_aardappeleters_-_s0005V1962_-_Van_Gogh_Museum.jpg/500px-De_aardappeleters_-_s0005V1962_-_Van_Gogh_Museum.jpg`; page: `https://en.wikipedia.org/wiki/The_Potato_Eaters`.
- Normalized gallery asset: `De aardappeleters - s0005V1962 - Van Gogh Museum.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-potato-eaters`; title `The Potato Eaters`; worksKey `The Potato Eaters`; artistId `vincent-van-gogh`. Evidence: same Commons asset `De aardappeleters - s0005V1962 - Van Gogh Museum.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/De_aardappeleters_-_s0005V1962_-_Van_Gogh_Museum.jpg/500px-De_aardappeleters_-_s0005V1962_-_Van_Gogh_Museum.jpg`; page: `https://commons.wikimedia.org/wiki/File:De_aardappeleters_-_s0005V1962_-_Van_Gogh_Museum.jpg`.
- Checked-in route `p/artwork/the-potato-eaters.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/De_aardappeleters_-_s0005V1962_-_Van_Gogh_Museum.jpg/500px-De_aardappeleters_-_s0005V1962_-_Van_Gogh_Museum.jpg`.

### 165. vincent-van-gogh / Wheatfield with Crows

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `vincent-van-gogh` → `Wheatfield with Crows`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Korenveld_met_kraaien_-_s0149V1962_-_Van_Gogh_Museum.jpg/500px-Korenveld_met_kraaien_-_s0149V1962_-_Van_Gogh_Museum.jpg`; page: `https://en.wikipedia.org/wiki/Wheatfield_with_Crows`.
- Normalized gallery asset: `Korenveld met kraaien - s0149V1962 - Van Gogh Museum.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `wheatfield-with-crows`; title `Wheatfield with Crows`; worksKey `Wheatfield with Crows`; artistId `vincent-van-gogh`. Evidence: same Commons asset `Korenveld met kraaien - s0149V1962 - Van Gogh Museum.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Korenveld_met_kraaien_-_s0149V1962_-_Van_Gogh_Museum.jpg/500px-Korenveld_met_kraaien_-_s0149V1962_-_Van_Gogh_Museum.jpg`; page: `https://commons.wikimedia.org/wiki/File:Korenveld_met_kraaien_-_s0149V1962_-_Van_Gogh_Museum.jpg`.
- Checked-in route `p/artwork/wheatfield-with-crows.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Korenveld_met_kraaien_-_s0149V1962_-_Van_Gogh_Museum.jpg/500px-Korenveld_met_kraaien_-_s0149V1962_-_Van_Gogh_Museum.jpg`.

### 166. paul-gauguin / Vision After the Sermon

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `paul-gauguin` → `Vision After the Sermon`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/La_vision_apr%C3%A8s_le_sermon_%28Paul_Gauguin%29.jpg/500px-La_vision_apr%C3%A8s_le_sermon_%28Paul_Gauguin%29.jpg`; page: `https://en.wikipedia.org/wiki/Vision_After_the_Sermon`.
- Normalized gallery asset: `La vision après le sermon (Paul Gauguin).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `vision-after-the-sermon`; title `Vision After the Sermon`; worksKey `Vision After the Sermon`; artistId `paul-gauguin`. Evidence: same Commons asset `La vision après le sermon (Paul Gauguin).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/La_vision_apr%C3%A8s_le_sermon_%28Paul_Gauguin%29.jpg/500px-La_vision_apr%C3%A8s_le_sermon_%28Paul_Gauguin%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:La_vision_apr%C3%A8s_le_sermon_(Paul_Gauguin).jpg`.
- Checked-in route `p/artwork/vision-after-the-sermon.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/La_vision_apr%C3%A8s_le_sermon_%28Paul_Gauguin%29.jpg/500px-La_vision_apr%C3%A8s_le_sermon_%28Paul_Gauguin%29.jpg`.

### 167. paul-gauguin / Where Do We Come From? What Are We? Where Are We Going?

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `paul-gauguin` → `Where Do We Come From? What Are We? Where Are We Going?`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Gauguin_-_Where_Do_We_Come_From%3F_What_Are_We%3F_Where_Are_We_Going%3F_%281897-98%29.jpg/500px-Gauguin_-_Where_Do_We_Come_From%3F_What_Are_We%3F_Where_Are_We_Going%3F_%281897-98%29.jpg`; page: `https://en.wikipedia.org/wiki/Where_Do_We_Come_From%3F_What_Are_We%3F_Where_Are_We_Going%3F`.
- Normalized gallery asset: `Gauguin - Where Do We Come From? What Are We? Where Are We Going? (1897-98).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `where-do-we-come-from`; title `Where Do We Come From? What Are We? Where Are We Going?`; worksKey `Where Do We Come From? What Are We? Where Are We Going?`; artistId `paul-gauguin`. Evidence: same Commons asset `Gauguin - Where Do We Come From? What Are We? Where Are We Going? (1897-98).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Gauguin_-_Where_Do_We_Come_From%3F_What_Are_We%3F_Where_Are_We_Going%3F_%281897-98%29.jpg/500px-Gauguin_-_Where_Do_We_Come_From%3F_What_Are_We%3F_Where_Are_We_Going%3F_%281897-98%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Gauguin_-_Where_Do_We_Come_From%3F_What_Are_We%3F_Where_Are_We_Going%3F_(1897-98).jpg`.
- Checked-in route `p/artwork/where-do-we-come-from.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Gauguin_-_Where_Do_We_Come_From%3F_What_Are_We%3F_Where_Are_We_Going%3F_%281897-98%29.jpg/500px-Gauguin_-_Where_Do_We_Come_From%3F_What_Are_We%3F_Where_Are_We_Going%3F_%281897-98%29.jpg`.

### 168. paul-gauguin / Tahitian Women on the Beach

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `paul-gauguin` → `Tahitian Women on the Beach`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Paul_Gauguin_056.jpg/500px-Paul_Gauguin_056.jpg`; page: `https://en.wikipedia.org/wiki/Tahitian_Women_on_the_Beach`.
- Normalized gallery asset: `Paul Gauguin 056.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `tahitian-women-on-the-beach`; title `Tahitian Women on the Beach`; worksKey `Tahitian Women on the Beach`; artistId `paul-gauguin`. Evidence: same Commons asset `Paul Gauguin 056.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Paul_Gauguin_056.jpg/500px-Paul_Gauguin_056.jpg`; page: `https://commons.wikimedia.org/wiki/File:Paul_Gauguin_056.jpg`.
- Checked-in route `p/artwork/tahitian-women-on-the-beach.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Paul_Gauguin_056.jpg/500px-Paul_Gauguin_056.jpg`.

### 169. paul-cezanne / Mont Sainte-Victoire series

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `paul-cezanne` → `Mont Sainte-Victoire series`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/La_Montagne_Sainte-Victoire_vue_de_la_carri%C3%A8re_Bib%C3%A9mus%2C_par_Paul_C%C3%A9zanne.jpg/960px-La_Montagne_Sainte-Victoire_vue_de_la_carri%C3%A8re_Bib%C3%A9mus%2C_par_Paul_C%C3%A9zanne.jpg`; page: `https://commons.wikimedia.org/wiki/File:La_Montagne_Sainte-Victoire_vue_de_la_carri%C3%A8re_Bib%C3%A9mus,_par_Paul_C%C3%A9zanne.jpg`.
- Normalized gallery asset: `La Montagne Sainte-Victoire vue de la carrière Bibémus, par Paul Cézanne.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `mont-sainte-victoire`; title `Mont Sainte-Victoire Seen from Bibémus`; worksKey `Mont Sainte-Victoire series`; artistId `paul-cezanne`. Evidence: same Commons asset `La Montagne Sainte-Victoire vue de la carrière Bibémus, par Paul Cézanne.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/La_Montagne_Sainte-Victoire_vue_de_la_carri%C3%A8re_Bib%C3%A9mus%2C_par_Paul_C%C3%A9zanne.jpg/500px-La_Montagne_Sainte-Victoire_vue_de_la_carri%C3%A8re_Bib%C3%A9mus%2C_par_Paul_C%C3%A9zanne.jpg`; page: `https://commons.wikimedia.org/wiki/File:La_Montagne_Sainte-Victoire_vue_de_la_carri%C3%A8re_Bib%C3%A9mus,_par_Paul_C%C3%A9zanne.jpg`.
- Checked-in route `p/artwork/mont-sainte-victoire.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/La_Montagne_Sainte-Victoire_vue_de_la_carri%C3%A8re_Bib%C3%A9mus%2C_par_Paul_C%C3%A9zanne.jpg/500px-La_Montagne_Sainte-Victoire_vue_de_la_carri%C3%A8re_Bib%C3%A9mus%2C_par_Paul_C%C3%A9zanne.jpg`.

### 170. paul-cezanne / The Card Players

- Classification: **CONFIRMED SAME ARTWORK**.
- Gallery source: `js/artworks.js` → `paul-cezanne` → `The Card Players`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Les_Joueurs_de_cartes%2C_par_Paul_C%C3%A9zanne.jpg/500px-Les_Joueurs_de_cartes%2C_par_Paul_C%C3%A9zanne.jpg`; page: `https://en.wikipedia.org/wiki/The_Card_Players`.
- Normalized gallery asset: `Les Joueurs de cartes, par Paul Cézanne.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-card-players`; title `The Card Players`; worksKey `The Card Players`; artistId `paul-cezanne`. Evidence: identical artistId `paul-cezanne` and gallery key equals catalog title `The Card Players`; different image files.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Les_Joueurs_de_cartes_-_Paul_C%C3%A9zanne.jpg/500px-Les_Joueurs_de_cartes_-_Paul_C%C3%A9zanne.jpg`; page: `https://commons.wikimedia.org/wiki/File:Les_Joueurs_de_cartes_-_Paul_C%C3%A9zanne.jpg`.
- Checked-in route `p/artwork/the-card-players.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Les_Joueurs_de_cartes_-_Paul_C%C3%A9zanne.jpg/500px-Les_Joueurs_de_cartes_-_Paul_C%C3%A9zanne.jpg`.

### 171. paul-cezanne / The Large Bathers

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `paul-cezanne` → `The Large Bathers`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Paul_C%C3%A9zanne%2C_French_-_The_Large_Bathers_-_Google_Art_Project.jpg/960px-Paul_C%C3%A9zanne%2C_French_-_The_Large_Bathers_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Paul_C%C3%A9zanne,_French_-_The_Large_Bathers_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Paul Cézanne, French - The Large Bathers - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-large-bathers`; title `The Large Bathers`; worksKey `The Large Bathers`; artistId `paul-cezanne`. Evidence: same Commons asset `Paul Cézanne, French - The Large Bathers - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Paul_C%C3%A9zanne%2C_French_-_The_Large_Bathers_-_Google_Art_Project.jpg/500px-Paul_C%C3%A9zanne%2C_French_-_The_Large_Bathers_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Paul_C%C3%A9zanne,_French_-_The_Large_Bathers_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/the-large-bathers.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Paul_C%C3%A9zanne%2C_French_-_The_Large_Bathers_-_Google_Art_Project.jpg/500px-Paul_C%C3%A9zanne%2C_French_-_The_Large_Bathers_-_Google_Art_Project.jpg`.

### 172. georges-seurat / A Sunday Afternoon on the Island of La Grande Jatte

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `georges-seurat` → `A Sunday Afternoon on the Island of La Grande Jatte`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/A_Sunday_on_La_Grande_Jatte%2C_Georges_Seurat%2C_1884.jpg/500px-A_Sunday_on_La_Grande_Jatte%2C_Georges_Seurat%2C_1884.jpg`; page: `https://en.wikipedia.org/wiki/A_Sunday_Afternoon_on_the_Island_of_La_Grande_Jatte`.
- Normalized gallery asset: `A Sunday on La Grande Jatte, Georges Seurat, 1884.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `a-sunday-afternoon-on-the-island-of-la-grande-jatte`; title `A Sunday Afternoon on the Island of La Grande Jatte`; worksKey `(absent)`; artistId `georges-seurat`. Evidence: same Commons asset `A Sunday on La Grande Jatte, Georges Seurat, 1884.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/A_Sunday_on_La_Grande_Jatte%2C_Georges_Seurat%2C_1884.jpg/500px-A_Sunday_on_La_Grande_Jatte%2C_Georges_Seurat%2C_1884.jpg`; page: `https://commons.wikimedia.org/wiki/File:A_Sunday_on_La_Grande_Jatte,_Georges_Seurat,_1884.jpg`.
- Checked-in route `p/artwork/a-sunday-afternoon-on-the-island-of-la-grande-jatte.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/A_Sunday_on_La_Grande_Jatte%2C_Georges_Seurat%2C_1884.jpg/500px-A_Sunday_on_La_Grande_Jatte%2C_Georges_Seurat%2C_1884.jpg`.

### 173. georges-seurat / Bathers at Asnières

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `georges-seurat` → `Bathers at Asnières`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Georges_Seurat_-_Study_for_Bathers_at_Asni%C3%A8res_PC_91.jpg/500px-Georges_Seurat_-_Study_for_Bathers_at_Asni%C3%A8res_PC_91.jpg`; page: `https://commons.wikimedia.org/wiki/File:Georges_Seurat_-_Study_for_Bathers_at_Asni%C3%A8res_PC_91.jpg`.
- Normalized gallery asset: `Georges Seurat - Study for Bathers at Asnières PC 91.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/georges-seurat`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 174. georges-seurat / The Circus

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `georges-seurat` → `The Circus`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Georges_Seurat%2C_1891%2C_Le_Cirque_%28The_Circus%29%2C_oil_on_canvas%2C_185_x_152_cm%2C_Mus%C3%A9e_d%27Orsay.jpg/500px-Georges_Seurat%2C_1891%2C_Le_Cirque_%28The_Circus%29%2C_oil_on_canvas%2C_185_x_152_cm%2C_Mus%C3%A9e_d%27Orsay.jpg`; page: `https://en.wikipedia.org/wiki/The_Circus_(Seurat)`.
- Normalized gallery asset: `Georges Seurat, 1891, Le Cirque (The Circus), oil on canvas, 185 x 152 cm, Musée d'Orsay.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/georges-seurat`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 175. henri-de-toulouse-lautrec / At the Moulin Rouge

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `henri-de-toulouse-lautrec` → `At the Moulin Rouge`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Henri_de_Toulouse-Lautrec%2C_At_the_Moulin_Rouge.jpg/500px-Henri_de_Toulouse-Lautrec%2C_At_the_Moulin_Rouge.jpg`; page: `https://en.wikipedia.org/wiki/At_the_Moulin_Rouge`.
- Normalized gallery asset: `Henri de Toulouse-Lautrec, At the Moulin Rouge.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-6.js` / `at-the-moulin-rouge`; title `At the Moulin Rouge`; worksKey `(absent)`; artistId `henri-de-toulouse-lautrec`. Evidence: same Commons asset `Henri de Toulouse-Lautrec, At the Moulin Rouge.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Henri_de_Toulouse-Lautrec%2C_At_the_Moulin_Rouge.jpg/500px-Henri_de_Toulouse-Lautrec%2C_At_the_Moulin_Rouge.jpg`; page: `https://commons.wikimedia.org/wiki/File:Henri_de_Toulouse-Lautrec,_At_the_Moulin_Rouge.jpg`.
- Checked-in route `p/artwork/at-the-moulin-rouge.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Henri_de_Toulouse-Lautrec%2C_At_the_Moulin_Rouge.jpg/500px-Henri_de_Toulouse-Lautrec%2C_At_the_Moulin_Rouge.jpg`.

### 176. henri-de-toulouse-lautrec / Moulin Rouge: La Goulue (poster)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `henri-de-toulouse-lautrec` → `Moulin Rouge: La Goulue (poster)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Henri_de_Toulouse-Lautrec%2C_Moulin_Rouge_-_La_Goulue%2C_1891_-_The_Metropolitan_Museum_of_Art.jpg/500px-Henri_de_Toulouse-Lautrec%2C_Moulin_Rouge_-_La_Goulue%2C_1891_-_The_Metropolitan_Museum_of_Art.jpg`; page: `https://en.wikipedia.org/wiki/Moulin_Rouge%3A_La_Goulue`.
- Normalized gallery asset: `Henri de Toulouse-Lautrec, Moulin Rouge - La Goulue, 1891 - The Metropolitan Museum of Art.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/henri-de-toulouse-lautrec`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 177. henri-de-toulouse-lautrec / The Bed

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `henri-de-toulouse-lautrec` → `The Bed`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/%28Albi%29_Au_lit_-_Toulouse-Lautrec_-_1894_MTL.175.jpg/960px-%28Albi%29_Au_lit_-_Toulouse-Lautrec_-_1894_MTL.175.jpg`; page: `https://commons.wikimedia.org/wiki/File:(Albi)_Au_lit_-_Toulouse-Lautrec_-_1894_MTL.175.jpg`.
- Normalized gallery asset: `(Albi) Au lit - Toulouse-Lautrec - 1894 MTL.175.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/henri-de-toulouse-lautrec`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 178. henri-rousseau / The Sleeping Gypsy

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `henri-rousseau` → `The Sleeping Gypsy`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/ROUSSEAU%2C_Henri_Sleeping_Gypsy_%28detail%29_1897.jpg/500px-ROUSSEAU%2C_Henri_Sleeping_Gypsy_%28detail%29_1897.jpg`; page: `https://commons.wikimedia.org/wiki/File:ROUSSEAU,_Henri_Sleeping_Gypsy_(detail)_1897.jpg`.
- Normalized gallery asset: `ROUSSEAU, Henri Sleeping Gypsy (detail) 1897.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/henri-rousseau`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 179. henri-rousseau / Tiger in a Tropical Storm (Surprised!)

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `henri-rousseau` → `Tiger in a Tropical Storm (Surprised!)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Surprised-Rousseau.jpg/500px-Surprised-Rousseau.jpg`; page: `https://en.wikipedia.org/wiki/Tiger_in_a_Tropical_Storm`.
- Normalized gallery asset: `Surprised-Rousseau.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `tiger-in-a-tropical-storm`; title `Tiger in a Tropical Storm (Surprised!)`; worksKey `Tiger in a Tropical Storm (Surprised!)`; artistId `henri-rousseau`. Evidence: same Commons asset `Surprised-Rousseau.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Surprised-Rousseau.jpg/500px-Surprised-Rousseau.jpg`; page: `https://commons.wikimedia.org/wiki/File:Surprised-Rousseau.jpg`.
- Checked-in route `p/artwork/tiger-in-a-tropical-storm.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Surprised-Rousseau.jpg/500px-Surprised-Rousseau.jpg`.

### 180. henri-rousseau / The Dream

- Classification: **CONFIRMED SAME ARTWORK**.
- Gallery source: `js/artworks.js` → `henri-rousseau` → `The Dream`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Henri_Rousseau_-_Le_R%C3%AAve_-_Google_Art_Project.jpg/500px-Henri_Rousseau_-_Le_R%C3%AAve_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Dream_(Rousseau)`.
- Normalized gallery asset: `Henri Rousseau - Le Rêve - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `the-dream-rousseau`; title `The Dream`; worksKey `The Dream`; artistId `henri-rousseau`. Evidence: identical artistId `henri-rousseau` and gallery key equals catalog title `The Dream`; different image files.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Henri_Rousseau_005.jpg/500px-Henri_Rousseau_005.jpg`; page: `https://commons.wikimedia.org/wiki/File:Henri_Rousseau_005.jpg`.
- Checked-in route `p/artwork/the-dream-rousseau.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Henri_Rousseau_005.jpg/500px-Henri_Rousseau_005.jpg`.

### 181. gustav-klimt / The Kiss

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `gustav-klimt` → `The Kiss`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/The_Kiss_-_Gustav_Klimt_-_Google_Cultural_Institute.jpg/500px-The_Kiss_-_Gustav_Klimt_-_Google_Cultural_Institute.jpg`; page: `https://en.wikipedia.org/wiki/The_Kiss_(Klimt)`.
- Normalized gallery asset: `The Kiss - Gustav Klimt - Google Cultural Institute.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-kiss`; title `The Kiss`; worksKey `(absent)`; artistId `gustav-klimt`. Evidence: same Commons asset `The Kiss - Gustav Klimt - Google Cultural Institute.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/The_Kiss_-_Gustav_Klimt_-_Google_Cultural_Institute.jpg/500px-The_Kiss_-_Gustav_Klimt_-_Google_Cultural_Institute.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Kiss_-_Gustav_Klimt_-_Google_Cultural_Institute.jpg`.
- Checked-in route `p/artwork/the-kiss.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/The_Kiss_-_Gustav_Klimt_-_Google_Cultural_Institute.jpg/500px-The_Kiss_-_Gustav_Klimt_-_Google_Cultural_Institute.jpg`.

### 182. gustav-klimt / Portrait of Adele Bloch-Bauer I

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `gustav-klimt` → `Portrait of Adele Bloch-Bauer I`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Gustav_Klimt_046.jpg/500px-Gustav_Klimt_046.jpg`; page: `https://en.wikipedia.org/wiki/Portrait_of_Adele_Bloch-Bauer_I`.
- Normalized gallery asset: `Gustav Klimt 046.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `adele-bloch-bauer-i`; title `Portrait of Adele Bloch-Bauer I`; worksKey `Portrait of Adele Bloch-Bauer I`; artistId `gustav-klimt`. Evidence: same Commons asset `Gustav Klimt 046.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Gustav_Klimt_046.jpg/500px-Gustav_Klimt_046.jpg`; page: `https://commons.wikimedia.org/wiki/File:Gustav_Klimt_046.jpg`.
- Checked-in route `p/artwork/adele-bloch-bauer-i.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Gustav_Klimt_046.jpg/500px-Gustav_Klimt_046.jpg`.

### 183. gustav-klimt / The Tree of Life

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `gustav-klimt` → `The Tree of Life`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Klimt_-_Nine_Cartoons_for_the_Stoclet_Frieze-_Part_4%2C_Part_of_the_tree_of_life_%281910-11%29.jpg/500px-Klimt_-_Nine_Cartoons_for_the_Stoclet_Frieze-_Part_4%2C_Part_of_the_tree_of_life_%281910-11%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Tree_of_Life%2C_Stoclet_Frieze`.
- Normalized gallery asset: `Klimt - Nine Cartoons for the Stoclet Frieze- Part 4, Part of the tree of life (1910-11).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `tree-of-life-stoclet`; title `The Tree of Life (Stoclet Frieze)`; worksKey `The Tree of Life`; artistId `gustav-klimt`. Evidence: same Commons asset `Klimt - Nine Cartoons for the Stoclet Frieze- Part 4, Part of the tree of life (1910-11).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Klimt_-_Nine_Cartoons_for_the_Stoclet_Frieze-_Part_4%2C_Part_of_the_tree_of_life_%281910-11%29.jpg/500px-Klimt_-_Nine_Cartoons_for_the_Stoclet_Frieze-_Part_4%2C_Part_of_the_tree_of_life_%281910-11%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Klimt_-_Nine_Cartoons_for_the_Stoclet_Frieze-_Part_4,_Part_of_the_tree_of_life_(1910-11).jpg`.
- Checked-in route `p/artwork/tree-of-life-stoclet.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Klimt_-_Nine_Cartoons_for_the_Stoclet_Frieze-_Part_4%2C_Part_of_the_tree_of_life_%281910-11%29.jpg/500px-Klimt_-_Nine_Cartoons_for_the_Stoclet_Frieze-_Part_4%2C_Part_of_the_tree_of_life_%281910-11%29.jpg`.

### 184. edvard-munch / The Scream

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `edvard-munch` → `The Scream`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg/500px-Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg`; page: `https://en.wikipedia.org/wiki/The_Scream`.
- Normalized gallery asset: `Edvard Munch, 1893, The Scream, oil, tempera and pastel on cardboard, 91 x 73 cm, National Gallery of Norway.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-scream`; title `The Scream`; worksKey `(absent)`; artistId `edvard-munch`. Evidence: same Commons asset `Edvard Munch, 1893, The Scream, oil, tempera and pastel on cardboard, 91 x 73 cm, National Gallery of Norway.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg/500px-Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg`; page: `https://commons.wikimedia.org/wiki/File:Edvard_Munch,_1893,_The_Scream,_oil,_tempera_and_pastel_on_cardboard,_91_x_73_cm,_National_Gallery_of_Norway.jpg`.
- Checked-in route `p/artwork/the-scream.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg/500px-Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg`.

### 185. edvard-munch / Madonna

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `edvard-munch` → `Madonna`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Edvard_Munch_-_Madonna_-_Google_Art_Project.jpg/500px-Edvard_Munch_-_Madonna_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Madonna_(Munch)`.
- Normalized gallery asset: `Edvard Munch - Madonna - Google Art Project.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `madonna-munch`; title `Madonna`; worksKey `Madonna`; artistId `edvard-munch`. Evidence: same Commons asset `Edvard Munch - Madonna - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Edvard_Munch_-_Madonna_-_Google_Art_Project.jpg/500px-Edvard_Munch_-_Madonna_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Edvard_Munch_-_Madonna_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/madonna-munch.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Edvard_Munch_-_Madonna_-_Google_Art_Project.jpg/500px-Edvard_Munch_-_Madonna_-_Google_Art_Project.jpg`.

### 186. edvard-munch / The Sick Child

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `edvard-munch` → `The Sick Child`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Munch_Det_Syke_Barn_1885-86.jpg/500px-Munch_Det_Syke_Barn_1885-86.jpg`; page: `https://en.wikipedia.org/wiki/The_Sick_Child_(Munch)`.
- Normalized gallery asset: `Munch Det Syke Barn 1885-86.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-sick-child`; title `The Sick Child`; worksKey `The Sick Child`; artistId `edvard-munch`. Evidence: same Commons asset `Munch Det Syke Barn 1885-86.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Munch_Det_Syke_Barn_1885-86.jpg/500px-Munch_Det_Syke_Barn_1885-86.jpg`; page: `https://commons.wikimedia.org/wiki/File:Munch_Det_Syke_Barn_1885-86.jpg`.
- Checked-in route `p/artwork/the-sick-child.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Munch_Det_Syke_Barn_1885-86.jpg/500px-Munch_Det_Syke_Barn_1885-86.jpg`.

### 187. edvard-munch / The Dance of Life

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `edvard-munch` → `The Dance of Life`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Edvard_Munch_-_The_dance_of_life_%281899-1900%29.jpg/500px-Edvard_Munch_-_The_dance_of_life_%281899-1900%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Dance_of_Life_(Munch)`.
- Normalized gallery asset: `Edvard Munch - The dance of life (1899-1900).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-dance-of-life`; title `The Dance of Life`; worksKey `The Dance of Life`; artistId `edvard-munch`. Evidence: same Commons asset `Edvard Munch - The dance of life (1899-1900).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Edvard_Munch_-_The_dance_of_life_%281899-1900%29.jpg/500px-Edvard_Munch_-_The_dance_of_life_%281899-1900%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Edvard_Munch_-_The_dance_of_life_(1899-1900).jpg`.
- Checked-in route `p/artwork/the-dance-of-life.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Edvard_Munch_-_The_dance_of_life_%281899-1900%29.jpg/500px-Edvard_Munch_-_The_dance_of_life_%281899-1900%29.jpg`.

### 188. henri-matisse / The Dance

- Classification: **CONFIRMED SAME ARTWORK**.
- Gallery source: `js/artworks.js` → `henri-matisse` → `The Dance`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Matissedance.jpg/500px-Matissedance.jpg`; page: `https://en.wikipedia.org/wiki/Dance_(Matisse)`.
- Normalized gallery asset: `Matissedance.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-2.js` / `the-dance-matisse`; title `The Dance`; worksKey `The Dance`; artistId `henri-matisse`. Evidence: identical artistId `henri-matisse` and gallery key equals catalog title `The Dance`; different image files.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/La_Danse_II%2C_par_Henri_Matisse.jpg/500px-La_Danse_II%2C_par_Henri_Matisse.jpg`; page: `https://commons.wikimedia.org/wiki/File:La_Danse_II,_par_Henri_Matisse.jpg`.
- Checked-in route `p/artwork/the-dance-matisse.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/La_Danse_II%2C_par_Henri_Matisse.jpg/500px-La_Danse_II%2C_par_Henri_Matisse.jpg`.

### 189. henri-matisse / Woman with a Hat

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `henri-matisse` → `Woman with a Hat`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Matisse-Woman-with-a-Hat.jpg/500px-Matisse-Woman-with-a-Hat.jpg`; page: `https://en.wikipedia.org/wiki/Woman_with_a_Hat`.
- Normalized gallery asset: `Matisse-Woman-with-a-Hat.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-2.js` / `woman-with-a-hat`; title `Woman with a Hat`; worksKey `Woman with a Hat`; artistId `henri-matisse`. Evidence: same Commons asset `Matisse-Woman-with-a-Hat.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Matisse-Woman-with-a-Hat.jpg/500px-Matisse-Woman-with-a-Hat.jpg`; page: `https://commons.wikimedia.org/wiki/File:Matisse-Woman-with-a-Hat.jpg`.
- Checked-in route `p/artwork/woman-with-a-hat.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Matisse-Woman-with-a-Hat.jpg/500px-Matisse-Woman-with-a-Hat.jpg`.

### 190. henri-matisse / The Red Studio

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `henri-matisse` → `The Red Studio`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/L%27Atelier_rouge%2C_par_Henri_Matisse.jpg/500px-L%27Atelier_rouge%2C_par_Henri_Matisse.jpg`; page: `https://en.wikipedia.org/wiki/The_Red_Studio`.
- Normalized gallery asset: `L'Atelier rouge, par Henri Matisse.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-2.js` / `the-red-studio`; title `The Red Studio`; worksKey `The Red Studio`; artistId `henri-matisse`. Evidence: same Commons asset `L'Atelier rouge, par Henri Matisse.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/L%27Atelier_rouge%2C_par_Henri_Matisse.jpg/500px-L%27Atelier_rouge%2C_par_Henri_Matisse.jpg`; page: `https://commons.wikimedia.org/wiki/File:L%27Atelier_rouge,_par_Henri_Matisse.jpg`.
- Checked-in route `p/artwork/the-red-studio.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/L%27Atelier_rouge%2C_par_Henri_Matisse.jpg/500px-L%27Atelier_rouge%2C_par_Henri_Matisse.jpg`.

### 191. henri-matisse / The Snail

- Classification: **CONFIRMED SAME ARTWORK**.
- Gallery source: `js/artworks.js` → `henri-matisse` → `The Snail`; img: `https://upload.wikimedia.org/wikipedia/commons/c/c1/Matisse_-_Carra%2C_P18.jpg`; page: `https://commons.wikimedia.org/wiki/File:Matisse_-_Carra,_P18.jpg`.
- Normalized gallery asset: `Matisse - Carra, P18.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-2.js` / `the-snail`; title `The Snail`; worksKey `(absent)`; artistId `henri-matisse`. Evidence: identical artistId `henri-matisse` and gallery key equals catalog title `The Snail`; catalog src absent.
- Catalog image.status: `copyright`; eligibility: **WITHHOLD**; src: ``; page: ``.
- Checked-in route `p/artwork/the-snail.html` — og:image: **TAG ABSENT**.

### 192. wassily-kandinsky / Composition VII

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `wassily-kandinsky` → `Composition VII`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Composition_VII_-_Wassily_Kandinsky%2C_GAC.jpg/500px-Composition_VII_-_Wassily_Kandinsky%2C_GAC.jpg`; page: `https://en.wikipedia.org/wiki/Composition_VII`.
- Normalized gallery asset: `Composition VII - Wassily Kandinsky, GAC.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `composition-vii`; title `Composition VII`; worksKey `(absent)`; artistId `wassily-kandinsky`. Evidence: same Commons asset `Composition VII - Wassily Kandinsky, GAC.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Composition_VII_-_Wassily_Kandinsky%2C_GAC.jpg/500px-Composition_VII_-_Wassily_Kandinsky%2C_GAC.jpg`; page: `https://commons.wikimedia.org/wiki/File:Composition_VII_-_Wassily_Kandinsky,_GAC.jpg`.
- Checked-in route `p/artwork/composition-vii.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Composition_VII_-_Wassily_Kandinsky%2C_GAC.jpg/500px-Composition_VII_-_Wassily_Kandinsky%2C_GAC.jpg`.

### 193. wassily-kandinsky / Improvisation 28

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `wassily-kandinsky` → `Improvisation 28`; img: `https://upload.wikimedia.org/wikipedia/commons/1/18/Vasily_Kandinsky_Improvisation_28_%28second_version%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Vasily_Kandinsky_Improvisation_28_(second_version).jpg`.
- Normalized gallery asset: `Vasily Kandinsky Improvisation 28 (second version).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `improvisation-28`; title `Improvisation 28 (Second Version)`; worksKey `Improvisation 28`; artistId `wassily-kandinsky`. Evidence: same Commons asset `Vasily Kandinsky Improvisation 28 (second version).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Vasily_Kandinsky_Improvisation_28_%28second_version%29.jpg/500px-Vasily_Kandinsky_Improvisation_28_%28second_version%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Vasily_Kandinsky_Improvisation_28_(second_version).jpg`.
- Checked-in route `p/artwork/improvisation-28.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Vasily_Kandinsky_Improvisation_28_%28second_version%29.jpg/500px-Vasily_Kandinsky_Improvisation_28_%28second_version%29.jpg`.

### 194. wassily-kandinsky / Several Circles

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `wassily-kandinsky` → `Several Circles`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Vassily_Kandinsky%2C_1926_-_Several_Circles%2C_Gugg_0910_25.jpg/960px-Vassily_Kandinsky%2C_1926_-_Several_Circles%2C_Gugg_0910_25.jpg`; page: `https://commons.wikimedia.org/wiki/File:Vassily_Kandinsky,_1926_-_Several_Circles,_Gugg_0910_25.jpg`.
- Normalized gallery asset: `Vassily Kandinsky, 1926 - Several Circles, Gugg 0910 25.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `several-circles`; title `Several Circles`; worksKey `Several Circles`; artistId `wassily-kandinsky`. Evidence: same Commons asset `Vassily Kandinsky, 1926 - Several Circles, Gugg 0910 25.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Vassily_Kandinsky%2C_1926_-_Several_Circles%2C_Gugg_0910_25.jpg/960px-Vassily_Kandinsky%2C_1926_-_Several_Circles%2C_Gugg_0910_25.jpg`; page: `https://commons.wikimedia.org/wiki/File:Vassily_Kandinsky,_1926_-_Several_Circles,_Gugg_0910_25.jpg`.
- Checked-in route `p/artwork/several-circles.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Vassily_Kandinsky%2C_1926_-_Several_Circles%2C_Gugg_0910_25.jpg/960px-Vassily_Kandinsky%2C_1926_-_Several_Circles%2C_Gugg_0910_25.jpg`.

### 195. wassily-kandinsky / Yellow-Red-Blue

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `wassily-kandinsky` → `Yellow-Red-Blue`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Kandinsky_-_Jaune_Rouge_Bleu.jpg/960px-Kandinsky_-_Jaune_Rouge_Bleu.jpg`; page: `https://commons.wikimedia.org/wiki/File:Kandinsky_-_Jaune_Rouge_Bleu.jpg`.
- Normalized gallery asset: `Kandinsky - Jaune Rouge Bleu.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `yellow-red-blue`; title `Yellow-Red-Blue`; worksKey `Yellow-Red-Blue`; artistId `wassily-kandinsky`. Evidence: same Commons asset `Kandinsky - Jaune Rouge Bleu.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Kandinsky_-_Jaune_Rouge_Bleu.jpg/960px-Kandinsky_-_Jaune_Rouge_Bleu.jpg`; page: `https://commons.wikimedia.org/wiki/File:Kandinsky_-_Jaune_Rouge_Bleu.jpg`.
- Checked-in route `p/artwork/yellow-red-blue.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Kandinsky_-_Jaune_Rouge_Bleu.jpg/960px-Kandinsky_-_Jaune_Rouge_Bleu.jpg`.

### 196. piet-mondrian / Composition with Red, Blue and Yellow

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `piet-mondrian` → `Composition with Red, Blue and Yellow`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Piet_Mondriaan%2C_1930_-_Mondrian_Composition_II_in_Red%2C_Blue%2C_and_Yellow.jpg/500px-Piet_Mondriaan%2C_1930_-_Mondrian_Composition_II_in_Red%2C_Blue%2C_and_Yellow.jpg`; page: `https://en.wikipedia.org/wiki/Composition_with_Red%2C_Blue_and_Yellow`.
- Normalized gallery asset: `Piet Mondriaan, 1930 - Mondrian Composition II in Red, Blue, and Yellow.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/piet-mondrian`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 197. piet-mondrian / Broadway Boogie Woogie

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `piet-mondrian` → `Broadway Boogie Woogie`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Piet_Mondrian%2C_1942_-_Broadway_Boogie_Woogie.jpg/500px-Piet_Mondrian%2C_1942_-_Broadway_Boogie_Woogie.jpg`; page: `https://en.wikipedia.org/wiki/Broadway_Boogie_Woogie`.
- Normalized gallery asset: `Piet Mondrian, 1942 - Broadway Boogie Woogie.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/piet-mondrian`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 198. piet-mondrian / The Gray Tree

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `piet-mondrian` → `The Gray Tree`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Piet_Mondrian%2C_1911%2C_Gray_Tree_%28De_grijze_boom%29%2C_oil_on_canvas%2C_79.7_x_109.1_cm%2C_Gemeentemuseum_Den_Haag%2C_Netherlands.jpg/500px-Piet_Mondrian%2C_1911%2C_Gray_Tree_%28De_grijze_boom%29%2C_oil_on_canvas%2C_79.7_x_109.1_cm%2C_Gemeentemuseum_Den_Haag%2C_Netherlands.jpg`; page: `https://commons.wikimedia.org/wiki/File:Piet_Mondrian,_1911,_Gray_Tree_(De_grijze_boom),_oil_on_canvas,_79.7_x_109.1_cm,_Gemeentemuseum_Den_Haag,_Netherlands.jpg`.
- Normalized gallery asset: `Piet Mondrian, 1911, Gray Tree (De grijze boom), oil on canvas, 79.7 x 109.1 cm, Gemeentemuseum Den Haag, Netherlands.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-6.js` / `gray-tree`; title `Gray Tree`; worksKey `The Gray Tree`; artistId `piet-mondrian`. Evidence: same Commons asset `Piet Mondrian, 1911, Gray Tree (De grijze boom), oil on canvas, 79.7 x 109.1 cm, Gemeentemuseum Den Haag, Netherlands.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Piet_Mondrian%2C_1911%2C_Gray_Tree_%28De_grijze_boom%29%2C_oil_on_canvas%2C_79.7_x_109.1_cm%2C_Gemeentemuseum_Den_Haag%2C_Netherlands.jpg/500px-Piet_Mondrian%2C_1911%2C_Gray_Tree_%28De_grijze_boom%29%2C_oil_on_canvas%2C_79.7_x_109.1_cm%2C_Gemeentemuseum_Den_Haag%2C_Netherlands.jpg`; page: `https://commons.wikimedia.org/wiki/File:Piet_Mondrian,_1911,_Gray_Tree_(De_grijze_boom),_oil_on_canvas,_79.7_x_109.1_cm,_Gemeentemuseum_Den_Haag,_Netherlands.jpg`.
- Checked-in route `p/artwork/gray-tree.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Piet_Mondrian%2C_1911%2C_Gray_Tree_%28De_grijze_boom%29%2C_oil_on_canvas%2C_79.7_x_109.1_cm%2C_Gemeentemuseum_Den_Haag%2C_Netherlands.jpg/500px-Piet_Mondrian%2C_1911%2C_Gray_Tree_%28De_grijze_boom%29%2C_oil_on_canvas%2C_79.7_x_109.1_cm%2C_Gemeentemuseum_Den_Haag%2C_Netherlands.jpg`.

### 199. kazimir-malevich / Black Square

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `kazimir-malevich` → `Black Square`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Kazimir_Malevich%2C_1915%2C_Black_Suprematic_Square%2C_oil_on_linen_canvas%2C_79.5_x_79.5_cm%2C_Tretyakov_Gallery%2C_Moscow.jpg/500px-Kazimir_Malevich%2C_1915%2C_Black_Suprematic_Square%2C_oil_on_linen_canvas%2C_79.5_x_79.5_cm%2C_Tretyakov_Gallery%2C_Moscow.jpg`; page: `https://en.wikipedia.org/wiki/Black_Square`.
- Normalized gallery asset: `Kazimir Malevich, 1915, Black Suprematic Square, oil on linen canvas, 79.5 x 79.5 cm, Tretyakov Gallery, Moscow.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-1.js` / `black-square`; title `Black Square`; worksKey `(absent)`; artistId `kazimir-malevich`. Evidence: same Commons asset `Kazimir Malevich, 1915, Black Suprematic Square, oil on linen canvas, 79.5 x 79.5 cm, Tretyakov Gallery, Moscow.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Kazimir_Malevich%2C_1915%2C_Black_Suprematic_Square%2C_oil_on_linen_canvas%2C_79.5_x_79.5_cm%2C_Tretyakov_Gallery%2C_Moscow.jpg/500px-Kazimir_Malevich%2C_1915%2C_Black_Suprematic_Square%2C_oil_on_linen_canvas%2C_79.5_x_79.5_cm%2C_Tretyakov_Gallery%2C_Moscow.jpg`; page: `https://commons.wikimedia.org/wiki/File:Kazimir_Malevich,_1915,_Black_Suprematic_Square,_oil_on_linen_canvas,_79.5_x_79.5_cm,_Tretyakov_Gallery,_Moscow.jpg`.
- Checked-in route `p/artwork/black-square.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Kazimir_Malevich%2C_1915%2C_Black_Suprematic_Square%2C_oil_on_linen_canvas%2C_79.5_x_79.5_cm%2C_Tretyakov_Gallery%2C_Moscow.jpg/500px-Kazimir_Malevich%2C_1915%2C_Black_Suprematic_Square%2C_oil_on_linen_canvas%2C_79.5_x_79.5_cm%2C_Tretyakov_Gallery%2C_Moscow.jpg`.

### 200. kazimir-malevich / White on White

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kazimir-malevich` → `White on White`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/White_on_White_%28Malevich%2C_1918%29.png/500px-White_on_White_%28Malevich%2C_1918%29.png`; page: `https://en.wikipedia.org/wiki/White_on_White`.
- Normalized gallery asset: `White on White (Malevich, 1918).png`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kazimir-malevich`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 201. kazimir-malevich / Suprematist Composition (Blue Rectangle over Red Beam)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kazimir-malevich` → `Suprematist Composition (Blue Rectangle over Red Beam)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Suprematist_Composition_-_Kazimir_Malevich.jpg/500px-Suprematist_Composition_-_Kazimir_Malevich.jpg`; page: `https://en.wikipedia.org/wiki/Suprematist_Composition`.
- Normalized gallery asset: `Suprematist Composition - Kazimir Malevich.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kazimir-malevich`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 202. hilma-af-klint / The Ten Largest

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `hilma-af-klint` → `The Ten Largest`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Hilma_af_Klint_-_The_Ten_Largest_No._9_-_1907.jpg/500px-Hilma_af_Klint_-_The_Ten_Largest_No._9_-_1907.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hilma_af_Klint_-_The_Ten_Largest_No._9_-_1907.jpg`.
- Normalized gallery asset: `Hilma af Klint - The Ten Largest No. 9 - 1907.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `the-ten-largest-no-9`; title `The Ten Largest, No. 9, Old Age`; worksKey `(absent)`; artistId `hilma-af-klint`. Evidence: same Commons asset `Hilma af Klint - The Ten Largest No. 9 - 1907.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Hilma_af_Klint_-_The_Ten_Largest_No._9_-_1907.jpg/500px-Hilma_af_Klint_-_The_Ten_Largest_No._9_-_1907.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hilma_af_Klint_-_The_Ten_Largest_No._9_-_1907.jpg`.
- Checked-in route `p/artwork/the-ten-largest-no-9.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Hilma_af_Klint_-_The_Ten_Largest_No._9_-_1907.jpg/500px-Hilma_af_Klint_-_The_Ten_Largest_No._9_-_1907.jpg`.

### 203. hilma-af-klint / Paintings for the Temple

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `hilma-af-klint` → `Paintings for the Temple`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Hilma_af_Klint_-_Altarpiece_No._1_Group_X_%2813919%29.jpg/500px-Hilma_af_Klint_-_Altarpiece_No._1_Group_X_%2813919%29.jpg`; page: `https://en.wikipedia.org/wiki/Paintings_for_the_Temple`.
- Normalized gallery asset: `Hilma af Klint - Altarpiece No. 1 Group X (13919).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `altarpiece-group-x-no-1`; title `Group X, No. 1, Altarpiece`; worksKey `(absent)`; artistId `hilma-af-klint`. Evidence: same Commons asset `Hilma af Klint - Altarpiece No. 1 Group X (13919).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Hilma_af_Klint_-_Altarpiece_No._1_Group_X_%2813919%29.jpg/500px-Hilma_af_Klint_-_Altarpiece_No._1_Group_X_%2813919%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hilma_af_Klint_-_Altarpiece_No._1_Group_X_(13919).jpg`.
- Checked-in route `p/artwork/altarpiece-group-x-no-1.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Hilma_af_Klint_-_Altarpiece_No._1_Group_X_%2813919%29.jpg/500px-Hilma_af_Klint_-_Altarpiece_No._1_Group_X_%2813919%29.jpg`.

### 204. hilma-af-klint / The Swan series

- Classification: **AMBIGUOUS**.
- Gallery source: `js/artworks.js` → `hilma-af-klint` → `The Swan series`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/The_Swan%2C_No._22%2C_SUW_UW_series_by_Hilma_af_Klint.jpg/960px-The_Swan%2C_No._22%2C_SUW_UW_series_by_Hilma_af_Klint.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Swan,_No._22,_SUW_UW_series_by_Hilma_af_Klint.jpg`.
- Normalized gallery asset: `The Swan, No. 22, SUW UW series by Hilma af Klint.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/hilma-af-klint`. Do not invent a slug from the gallery title.
- Unconfirmed same-artist title candidates: `swan-no-17` (js/catalog-4.js), title `The Swan, No. 17`, worksKey `The Swan series`. A partial or series-level title does not establish individual artwork identity.
- Candidate asset evidence for `swan-no-17` (not a confirmed match): src `https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Hilma_af_Klint%2C_1915%2C_Svanen%2C_No._17.jpg/500px-Hilma_af_Klint%2C_1915%2C_Svanen%2C_No._17.jpg`; page `https://commons.wikimedia.org/wiki/File:Hilma_af_Klint,_1915,_Svanen,_No._17.jpg`; normalized asset `Hilma af Klint, 1915, Svanen, No. 17.jpg`.
- Specific contradiction: gallery asset names No. 22; catalog swan-no-17 names No. 17. Shared series key does not resolve that difference.

### 205. paul-klee / Twittering Machine

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `paul-klee` → `Twittering Machine`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Die_Zwitscher-Maschine_%28Twittering_Machine%29%2C_1922_-_Paul_Klee.jpg/500px-Die_Zwitscher-Maschine_%28Twittering_Machine%29%2C_1922_-_Paul_Klee.jpg`; page: `https://en.wikipedia.org/wiki/Twittering_Machine`.
- Normalized gallery asset: `Die Zwitscher-Maschine (Twittering Machine), 1922 - Paul Klee.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/paul-klee`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 206. paul-klee / Senecio

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `paul-klee` → `Senecio`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg/500px-Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg`; page: `https://en.wikipedia.org/wiki/Senecio_(Klee)`.
- Normalized gallery asset: `Paul Klee, 1922, Senecio, oil on gauze, 40.3 × 37.4 cm, Kunstmuseum Basel.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `senecio`; title `Senecio`; worksKey `(absent)`; artistId `paul-klee`. Evidence: same Commons asset `Paul Klee, 1922, Senecio, oil on gauze, 40.3 × 37.4 cm, Kunstmuseum Basel.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg/500px-Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg`; page: `https://commons.wikimedia.org/wiki/File:Paul_Klee,_1922,_Senecio,_oil_on_gauze,_40.3_%C3%97_37.4_cm,_Kunstmuseum_Basel.jpg`.
- Checked-in route `p/artwork/senecio.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg/500px-Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg`.

### 207. paul-klee / Highway and Byways

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `paul-klee` → `Highway and Byways`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Hauptweg_und_Nebenwege_-_Paul_Klee_-_Museum_Ludwig-7026_%28cropped%29.jpg/500px-Hauptweg_und_Nebenwege_-_Paul_Klee_-_Museum_Ludwig-7026_%28cropped%29.jpg`; page: `https://en.wikipedia.org/wiki/Highway_and_Byways`.
- Normalized gallery asset: `Hauptweg und Nebenwege - Paul Klee - Museum Ludwig-7026 (cropped).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/paul-klee`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 208. paul-klee / Death and Fire

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `paul-klee` → `Death and Fire`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Death_and_Fire_%281940%29_-_Paul_Klee_%28Zentrum_Paul_Klee%29.jpg/500px-Death_and_Fire_%281940%29_-_Paul_Klee_%28Zentrum_Paul_Klee%29.jpg`; page: `https://en.wikipedia.org/wiki/Death_and_Fire`.
- Normalized gallery asset: `Death and Fire (1940) - Paul Klee (Zentrum Paul Klee).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/paul-klee`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 209. amedeo-modigliani / Reclining Nude

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `amedeo-modigliani` → `Reclining Nude`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Amedeo_Modigliani_Reclining_Nude_The_Metropolitan_Museum_of_Art.jpg/500px-Amedeo_Modigliani_Reclining_Nude_The_Metropolitan_Museum_of_Art.jpg`; page: `https://en.wikipedia.org/wiki/Reclining_Nude_(Modigliani)`.
- Normalized gallery asset: `Amedeo Modigliani Reclining Nude The Metropolitan Museum of Art.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-8.js` / `reclining-nude-modigliani`; title `Reclining Nude`; worksKey `Reclining Nude`; artistId `amedeo-modigliani`. Evidence: same Commons asset `Amedeo Modigliani Reclining Nude The Metropolitan Museum of Art.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Amedeo_Modigliani_Reclining_Nude_The_Metropolitan_Museum_of_Art.jpg/500px-Amedeo_Modigliani_Reclining_Nude_The_Metropolitan_Museum_of_Art.jpg`; page: `https://commons.wikimedia.org/wiki/File:Amedeo_Modigliani_Reclining_Nude_The_Metropolitan_Museum_of_Art.jpg`.
- Checked-in route `p/artwork/reclining-nude-modigliani.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Amedeo_Modigliani_Reclining_Nude_The_Metropolitan_Museum_of_Art.jpg/500px-Amedeo_Modigliani_Reclining_Nude_The_Metropolitan_Museum_of_Art.jpg`.

### 210. amedeo-modigliani / Jeanne Hébuterne in a Yellow Sweater

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `amedeo-modigliani` → `Jeanne Hébuterne in a Yellow Sweater`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Amedeo_Modigliani_025.jpg/960px-Amedeo_Modigliani_025.jpg`; page: `https://commons.wikimedia.org/wiki/File:Amedeo_Modigliani_025.jpg`.
- Normalized gallery asset: `Amedeo Modigliani 025.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/amedeo-modigliani`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 211. amedeo-modigliani / Portrait of Chaim Soutine

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `amedeo-modigliani` → `Portrait of Chaim Soutine`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Amedeo_Modigliani_-_Chaim_Soutine_%281917%29.jpg/500px-Amedeo_Modigliani_-_Chaim_Soutine_%281917%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Amedeo_Modigliani_-_Chaim_Soutine_(1917).jpg`.
- Normalized gallery asset: `Amedeo Modigliani - Chaim Soutine (1917).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/amedeo-modigliani`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 212. egon-schiele / Self-Portrait with Physalis

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `egon-schiele` → `Self-Portrait with Physalis`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Egon_Schiele_-_Self-Portrait_with_Physalis_-_Google_Art_Project.jpg/960px-Egon_Schiele_-_Self-Portrait_with_Physalis_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Egon_Schiele_-_Self-Portrait_with_Physalis_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Egon Schiele - Self-Portrait with Physalis - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/egon-schiele`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 213. egon-schiele / Death and the Maiden

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `egon-schiele` → `Death and the Maiden`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Egon_Schiele_-_Der_Tod_und_das_M%C3%A4dchen.jpg/500px-Egon_Schiele_-_Der_Tod_und_das_M%C3%A4dchen.jpg`; page: `https://en.wikipedia.org/wiki/Death_and_the_Maiden_(Schiele)`.
- Normalized gallery asset: `Egon Schiele - Der Tod und das Mädchen.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-9.js` / `death-and-the-maiden`; title `Death and the Maiden`; worksKey `(absent)`; artistId `egon-schiele`. Evidence: same Commons asset `Egon Schiele - Der Tod und das Mädchen.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Egon_Schiele_-_Der_Tod_und_das_M%C3%A4dchen.jpg/500px-Egon_Schiele_-_Der_Tod_und_das_M%C3%A4dchen.jpg`; page: `https://commons.wikimedia.org/wiki/File:Egon_Schiele_-_Der_Tod_und_das_M%C3%A4dchen.jpg`.
- Checked-in route `p/artwork/death-and-the-maiden.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Egon_Schiele_-_Der_Tod_und_das_M%C3%A4dchen.jpg/500px-Egon_Schiele_-_Der_Tod_und_das_M%C3%A4dchen.jpg`.

### 214. egon-schiele / The Embrace

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `egon-schiele` → `The Embrace`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Egon_Schiele_-_Die_Umarmung_-_4438_-_%C3%96sterreichische_Galerie_Belvedere.jpg/500px-Egon_Schiele_-_Die_Umarmung_-_4438_-_%C3%96sterreichische_Galerie_Belvedere.jpg`; page: `https://commons.wikimedia.org/wiki/File:Egon_Schiele_-_Die_Umarmung_-_4438_-_%C3%96sterreichische_Galerie_Belvedere.jpg`.
- Normalized gallery asset: `Egon Schiele - Die Umarmung - 4438 - Österreichische Galerie Belvedere.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/egon-schiele`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 215. ernst-ludwig-kirchner / Street, Berlin

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ernst-ludwig-kirchner` → `Street, Berlin`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Kirchner_1913_Street%2C_Berlin.jpg/500px-Kirchner_1913_Street%2C_Berlin.jpg`; page: `https://en.wikipedia.org/wiki/Street%2C_Berlin_(Kirchner)`.
- Normalized gallery asset: `Kirchner 1913 Street, Berlin.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ernst-ludwig-kirchner`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 216. ernst-ludwig-kirchner / Self-Portrait as a Soldier

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ernst-ludwig-kirchner` → `Self-Portrait as a Soldier`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Kirchner_-_Self_Portrait_as_a_Soldier_%281915%29.jpg/500px-Kirchner_-_Self_Portrait_as_a_Soldier_%281915%29.jpg`; page: `https://en.wikipedia.org/wiki/Self-Portrait_as_a_Soldier`.
- Normalized gallery asset: `Kirchner - Self Portrait as a Soldier (1915).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ernst-ludwig-kirchner`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 217. ernst-ludwig-kirchner / Marzella

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ernst-ludwig-kirchner` → `Marzella`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Kirchner_1909_Marzella.jpg/960px-Kirchner_1909_Marzella.jpg`; page: `https://commons.wikimedia.org/wiki/File:Kirchner_1909_Marzella.jpg`.
- Normalized gallery asset: `Kirchner 1909 Marzella.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ernst-ludwig-kirchner`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 218. amrita-sher-gil / Young Girls

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `amrita-sher-gil` → `Young Girls`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Young_Girls.jpg/500px-Young_Girls.jpg`; page: `https://en.wikipedia.org/wiki/Young_Girls_(painting)`.
- Normalized gallery asset: `Young Girls.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/amrita-sher-gil`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 219. amrita-sher-gil / Three Girls

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `amrita-sher-gil` → `Three Girls`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Amrita_Sher-Gil_Group_of_Three_Girls.jpg/500px-Amrita_Sher-Gil_Group_of_Three_Girls.jpg`; page: `https://en.wikipedia.org/wiki/Three_Girls_(painting)`.
- Normalized gallery asset: `Amrita Sher-Gil Group of Three Girls.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `three-girls`; title `Three Girls`; worksKey `Three Girls`; artistId `amrita-sher-gil`. Evidence: same Commons asset `Amrita Sher-Gil Group of Three Girls.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Amrita_Sher-Gil_Group_of_Three_Girls.jpg/500px-Amrita_Sher-Gil_Group_of_Three_Girls.jpg`; page: `https://commons.wikimedia.org/wiki/File:Amrita_Sher-Gil_Group_of_Three_Girls.jpg`.
- Checked-in route `p/artwork/three-girls.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Amrita_Sher-Gil_Group_of_Three_Girls.jpg/500px-Amrita_Sher-Gil_Group_of_Three_Girls.jpg`.

### 220. amrita-sher-gil / Bride's Toilet

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `amrita-sher-gil` → `Bride's Toilet`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Amrita_Sger-Gil_Bride%27s_Toilet.jpg/500px-Amrita_Sger-Gil_Bride%27s_Toilet.jpg`; page: `https://en.wikipedia.org/wiki/Bride's_Toilet`.
- Normalized gallery asset: `Amrita Sger-Gil Bride's Toilet.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/amrita-sher-gil`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 221. sandro-botticelli / The Birth of Venus

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `sandro-botticelli` → `The Birth of Venus`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg/500px-Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg`; page: `https://en.wikipedia.org/wiki/The_Birth_of_Venus`.
- Normalized gallery asset: `Sandro Botticelli - La nascita di Venere - Google Art Project - edited.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `the-birth-of-venus`; title `The Birth of Venus`; worksKey `The Birth of Venus`; artistId `sandro-botticelli`. Evidence: same Commons asset `Sandro Botticelli - La nascita di Venere - Google Art Project - edited.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg/500px-Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg`; page: `https://commons.wikimedia.org/wiki/File:Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg`.
- Checked-in route `p/artwork/the-birth-of-venus.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg/500px-Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg`.

### 222. sandro-botticelli / Primavera

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `sandro-botticelli` → `Primavera`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Botticelli-primavera.jpg/500px-Botticelli-primavera.jpg`; page: `https://en.wikipedia.org/wiki/Primavera_(Botticelli)`.
- Normalized gallery asset: `Botticelli-primavera.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `primavera`; title `Primavera`; worksKey `Primavera`; artistId `sandro-botticelli`. Evidence: same Commons asset `Botticelli-primavera.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Botticelli-primavera.jpg/500px-Botticelli-primavera.jpg`; page: `https://commons.wikimedia.org/wiki/File:Botticelli-primavera.jpg`.
- Checked-in route `p/artwork/primavera.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Botticelli-primavera.jpg/500px-Botticelli-primavera.jpg`.

### 223. sandro-botticelli / The Mystical Nativity

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `sandro-botticelli` → `The Mystical Nativity`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Mystic_Nativity%2C_Sandro_Botticelli.jpg/500px-Mystic_Nativity%2C_Sandro_Botticelli.jpg`; page: `https://en.wikipedia.org/wiki/The_Mystical_Nativity`.
- Normalized gallery asset: `Mystic Nativity, Sandro Botticelli.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-3.js` / `the-mystical-nativity`; title `The Mystical Nativity`; worksKey `The Mystical Nativity`; artistId `sandro-botticelli`. Evidence: same Commons asset `Mystic Nativity, Sandro Botticelli.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Mystic_Nativity%2C_Sandro_Botticelli.jpg/500px-Mystic_Nativity%2C_Sandro_Botticelli.jpg`; page: `https://commons.wikimedia.org/wiki/File:Mystic_Nativity,_Sandro_Botticelli.jpg`.
- Checked-in route `p/artwork/the-mystical-nativity.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Mystic_Nativity%2C_Sandro_Botticelli.jpg/500px-Mystic_Nativity%2C_Sandro_Botticelli.jpg`.

### 224. giorgione / The Tempest

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `giorgione` → `The Tempest`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Giorgione_-_Das_Gewitter.jpg/500px-Giorgione_-_Das_Gewitter.jpg`; page: `https://en.wikipedia.org/wiki/The_Tempest_(Giorgione)`.
- Normalized gallery asset: `Giorgione - Das Gewitter.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `the-tempest`; title `The Tempest`; worksKey `(absent)`; artistId `giorgione`. Evidence: same Commons asset `Giorgione - Das Gewitter.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Giorgione_-_Das_Gewitter.jpg/500px-Giorgione_-_Das_Gewitter.jpg`; page: `https://commons.wikimedia.org/wiki/File:Giorgione_-_Das_Gewitter.jpg`.
- Checked-in route `p/artwork/the-tempest.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Giorgione_-_Das_Gewitter.jpg/500px-Giorgione_-_Das_Gewitter.jpg`.

### 225. giorgione / Sleeping Venus

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giorgione` → `Sleeping Venus`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Giorgione_-_Sleeping_Venus_-_Google_Art_Project_2.jpg/500px-Giorgione_-_Sleeping_Venus_-_Google_Art_Project_2.jpg`; page: `https://en.wikipedia.org/wiki/Sleeping_Venus_(Giorgione)`.
- Normalized gallery asset: `Giorgione - Sleeping Venus - Google Art Project 2.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giorgione`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 226. giorgione / The Three Philosophers

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giorgione` → `The Three Philosophers`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Giorgione_-_Three_Philosophers_-_Google_Art_Project.jpg/500px-Giorgione_-_Three_Philosophers_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Three_Philosophers`.
- Normalized gallery asset: `Giorgione - Three Philosophers - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giorgione`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 227. matthias-grunewald / The Isenheim Altarpiece

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `matthias-grunewald` → `The Isenheim Altarpiece`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Isenheimer_Altar_%28Colmar%29_jm01221_deriv.jpg/500px-Isenheimer_Altar_%28Colmar%29_jm01221_deriv.jpg`; page: `https://commons.wikimedia.org/wiki/File:Isenheimer_Altar_(Colmar)_jm01221_deriv.jpg`.
- Normalized gallery asset: `Isenheimer Altar (Colmar) jm01221 deriv.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/matthias-grunewald`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 228. matthias-grunewald / The Mocking of Christ

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `matthias-grunewald` → `The Mocking of Christ`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Mathis_Gothart_Gr%C3%BCnewald_062.jpg/500px-Mathis_Gothart_Gr%C3%BCnewald_062.jpg`; page: `https://en.wikipedia.org/wiki/The_Mocking_of_Christ_(Gr%C3%BCnewald)`.
- Normalized gallery asset: `Mathis Gothart Grünewald 062.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/matthias-grunewald`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 229. matthias-grunewald / Stuppach Madonna

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `matthias-grunewald` → `Stuppach Madonna`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Stuppacher_Madonna_-_Gr%C3%BCnewald.jpg/500px-Stuppacher_Madonna_-_Gr%C3%BCnewald.jpg`; page: `https://en.wikipedia.org/wiki/Stuppach_Madonna`.
- Normalized gallery asset: `Stuppacher Madonna - Grünewald.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/matthias-grunewald`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 230. lucas-cranach / Portrait of Martin Luther

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `lucas-cranach` → `Portrait of Martin Luther`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Lucas_Cranach_d.%C3%84._-_Martin_Luther%2C_1528_%28Veste_Coburg%29.jpg/960px-Lucas_Cranach_d.%C3%84._-_Martin_Luther%2C_1528_%28Veste_Coburg%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Lucas_Cranach_d.%C3%84._-_Martin_Luther,_1528_(Veste_Coburg).jpg`.
- Normalized gallery asset: `Lucas Cranach d.Ä. - Martin Luther, 1528 (Veste Coburg).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/lucas-cranach`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 231. lucas-cranach / Adam and Eve

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `lucas-cranach` → `Adam and Eve`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Adam_and_Eve_%28UK_CIA_P-1947-LF-77%29.jpg/500px-Adam_and_Eve_%28UK_CIA_P-1947-LF-77%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Adam_and_Eve_(UK_CIA_P-1947-LF-77).jpg`.
- Normalized gallery asset: `Adam and Eve (UK CIA P-1947-LF-77).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/lucas-cranach`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 232. lucas-cranach / The Judgment of Paris

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `lucas-cranach` → `The Judgment of Paris`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Lucas_Cranach_the_Elder_-_The_Judgment_of_Paris_-_Google_Art_Project.jpg/960px-Lucas_Cranach_the_Elder_-_The_Judgment_of_Paris_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Lucas_Cranach_the_Elder_-_The_Judgment_of_Paris_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Lucas Cranach the Elder - The Judgment of Paris - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/lucas-cranach`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 233. correggio / Assumption of the Virgin (Parma Cathedral)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `correggio` → `Assumption of the Virgin (Parma Cathedral)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Cupola_Duomo_Parma_Correggio.jpg/500px-Cupola_Duomo_Parma_Correggio.jpg`; page: `https://commons.wikimedia.org/wiki/File:Cupola_Duomo_Parma_Correggio.jpg`.
- Normalized gallery asset: `Cupola Duomo Parma Correggio.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/correggio`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 234. correggio / Jupiter and Io

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `correggio` → `Jupiter and Io`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Antonio_Allegri%2C_called_Correggio_-_Jupiter_and_Io_-_Google_Art_Project.jpg/500px-Antonio_Allegri%2C_called_Correggio_-_Jupiter_and_Io_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Jupiter_and_Io`.
- Normalized gallery asset: `Antonio Allegri, called Correggio - Jupiter and Io - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/correggio`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 235. correggio / Adoration of the Shepherds (The Night)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `correggio` → `Adoration of the Shepherds (The Night)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Correggio_-_The_Holy_Night_-_Google_Art_Project.jpg/500px-Correggio_-_The_Holy_Night_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Nativity_(Correggio)`.
- Normalized gallery asset: `Correggio - The Holy Night - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/correggio`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 236. parmigianino / Madonna with the Long Neck

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `parmigianino` → `Madonna with the Long Neck`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Parmigianino_-_Madonna_and_Child_with_Angels%2C_known_as_the_Madonna_with_the_Long_Neck.jpg/500px-Parmigianino_-_Madonna_and_Child_with_Angels%2C_known_as_the_Madonna_with_the_Long_Neck.jpg`; page: `https://en.wikipedia.org/wiki/Madonna_with_the_Long_Neck`.
- Normalized gallery asset: `Parmigianino - Madonna and Child with Angels, known as the Madonna with the Long Neck.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/parmigianino`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 237. parmigianino / Self-Portrait in a Convex Mirror

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `parmigianino` → `Self-Portrait in a Convex Mirror`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Parmigianino_Selfportrait.jpg/500px-Parmigianino_Selfportrait.jpg`; page: `https://en.wikipedia.org/wiki/Self-Portrait_in_a_Convex_Mirror_(Parmigianino)`.
- Normalized gallery asset: `Parmigianino Selfportrait.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/parmigianino`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 238. parmigianino / Cupid Making His Bow

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `parmigianino` → `Cupid Making His Bow`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Parmigianino_-_Cupid_-_WGA17032.jpg/500px-Parmigianino_-_Cupid_-_WGA17032.jpg`; page: `https://en.wikipedia.org/wiki/Cupid_Making_His_Bow`.
- Normalized gallery asset: `Parmigianino - Cupid - WGA17032.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/parmigianino`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 239. bronzino / Portrait of Eleonora di Toledo with Her Son

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `bronzino` → `Portrait of Eleonora di Toledo with Her Son`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Bronzino_-_Eleonora_di_Toledo_col_figlio_Giovanni_-_Google_Art_Project.jpg/960px-Bronzino_-_Eleonora_di_Toledo_col_figlio_Giovanni_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Bronzino_-_Eleonora_di_Toledo_col_figlio_Giovanni_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Bronzino - Eleonora di Toledo col figlio Giovanni - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/bronzino`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 240. bronzino / An Allegory with Venus and Cupid

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `bronzino` → `An Allegory with Venus and Cupid`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Angelo_Bronzino_-_Venus%2C_Cupid%2C_Folly_and_Time_-_National_Gallery%2C_London.jpg/960px-Angelo_Bronzino_-_Venus%2C_Cupid%2C_Folly_and_Time_-_National_Gallery%2C_London.jpg`; page: `https://commons.wikimedia.org/wiki/File:Angelo_Bronzino_-_Venus,_Cupid,_Folly_and_Time_-_National_Gallery,_London.jpg`.
- Normalized gallery asset: `Angelo Bronzino - Venus, Cupid, Folly and Time - National Gallery, London.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/bronzino`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 241. bronzino / Portrait of a Young Man with a Book

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `bronzino` → `Portrait of a Young Man with a Book`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Bronzino_%28Agnolo_di_Cosimo_di_Mariano%29_-_Portrait_of_a_Young_Man_-_The_Metropolitan_Museum_of_Art.jpg/500px-Bronzino_%28Agnolo_di_Cosimo_di_Mariano%29_-_Portrait_of_a_Young_Man_-_The_Metropolitan_Museum_of_Art.jpg`; page: `https://en.wikipedia.org/wiki/Portrait_of_a_Young_Man_with_a_Book_(Bronzino)`.
- Normalized gallery asset: `Bronzino (Agnolo di Cosimo di Mariano) - Portrait of a Young Man - The Metropolitan Museum of Art.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/bronzino`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 242. lavinia-fontana / Self-Portrait at the Clavichord

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `lavinia-fontana` → `Self-Portrait at the Clavichord`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Self-portrait_at_the_Clavichord_with_a_Servant_by_Lavinia_Fontana.jpg/960px-Self-portrait_at_the_Clavichord_with_a_Servant_by_Lavinia_Fontana.jpg`; page: `https://commons.wikimedia.org/wiki/File:Self-portrait_at_the_Clavichord_with_a_Servant_by_Lavinia_Fontana.jpg`.
- Normalized gallery asset: `Self-portrait at the Clavichord with a Servant by Lavinia Fontana.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/lavinia-fontana`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 243. lavinia-fontana / Portrait of the Gozzadini Family

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `lavinia-fontana` → `Portrait of the Gozzadini Family`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Lavinia_fontana%2C_famiglia_gozzadini%2C_1583%2C_01.jpg/500px-Lavinia_fontana%2C_famiglia_gozzadini%2C_1583%2C_01.jpg`; page: `https://en.wikipedia.org/wiki/Portrait_of_the_Gozzadini_Family`.
- Normalized gallery asset: `Lavinia fontana, famiglia gozzadini, 1583, 01.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/lavinia-fontana`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 244. lavinia-fontana / Minerva Dressing

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `lavinia-fontana` → `Minerva Dressing`; img: `https://upload.wikimedia.org/wikipedia/commons/f/f4/Minerva_dressing_by_Lavinia_Fontana_%281613%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Minerva_dressing_by_Lavinia_Fontana_(1613).jpg`.
- Normalized gallery asset: `Minerva dressing by Lavinia Fontana (1613).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/lavinia-fontana`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 245. nicholas-hilliard / Young Man Among Roses

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `nicholas-hilliard` → `Young Man Among Roses`; img: `https://upload.wikimedia.org/wikipedia/commons/f/fa/Nicholas_Hilliard_-_Young_Man_Among_Roses_-_V%26A_P.163-1910.jpg`; page: `https://commons.wikimedia.org/wiki/File:Nicholas_Hilliard_-_Young_Man_Among_Roses_-_V%26A_P.163-1910.jpg`.
- Normalized gallery asset: `Nicholas Hilliard - Young Man Among Roses - V&A P.163-1910.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/nicholas-hilliard`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 246. nicholas-hilliard / Portrait of Queen Elizabeth I

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `nicholas-hilliard` → `Portrait of Queen Elizabeth I`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Elizabeth_I_%281533-1603%29%2CQueen_of_England%2C_c._1586-87_%28Nicholas_Hilliard%29_-_Nationalmuseum_-_133092.tif/lossy-page1-960px-Elizabeth_I_%281533-1603%29%2CQueen_of_England%2C_c._1586-87_%28Nicholas_Hilliard%29_-_Nationalmuseum_-_133092.tif.jpg`; page: `https://commons.wikimedia.org/wiki/File:Elizabeth_I_(1533-1603),Queen_of_England,_c._1586-87_(Nicholas_Hilliard)_-_Nationalmuseum_-_133092.tif`.
- Normalized gallery asset: `Elizabeth I (1533-1603),Queen of England, c. 1586-87 (Nicholas Hilliard) - Nationalmuseum - 133092.tif`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/nicholas-hilliard`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 247. nicholas-hilliard / Self-Portrait Aged 30

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `nicholas-hilliard` → `Self-Portrait Aged 30`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Nicholas_Hilliard_021_%282%29.jpg/960px-Nicholas_Hilliard_021_%282%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Nicholas_Hilliard_021_(2).jpg`.
- Normalized gallery asset: `Nicholas Hilliard 021 (2).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/nicholas-hilliard`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 248. annibale-carracci / The Farnese Gallery ceiling

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `annibale-carracci` → `The Farnese Gallery ceiling`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Annibale_Carracci_Farnese_Ceiling_detail.png/960px-Annibale_Carracci_Farnese_Ceiling_detail.png`; page: `https://commons.wikimedia.org/wiki/File:Annibale_Carracci_Farnese_Ceiling_detail.png`.
- Normalized gallery asset: `Annibale Carracci Farnese Ceiling detail.png`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/annibale-carracci`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 249. annibale-carracci / The Beaneater

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `annibale-carracci` → `The Beaneater`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Carracci_-_Der_Bohnenesser.jpeg/500px-Carracci_-_Der_Bohnenesser.jpeg`; page: `https://en.wikipedia.org/wiki/The_Beaneater`.
- Normalized gallery asset: `Carracci - Der Bohnenesser.jpeg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-7.js` / `the-beaneater`; title `The Beaneater`; worksKey `(absent)`; artistId `annibale-carracci`. Evidence: same Commons asset `Carracci - Der Bohnenesser.jpeg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Carracci_-_Der_Bohnenesser.jpeg/500px-Carracci_-_Der_Bohnenesser.jpeg`; page: `https://commons.wikimedia.org/wiki/File:Carracci_-_Der_Bohnenesser.jpeg`.
- Checked-in route `p/artwork/the-beaneater.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Carracci_-_Der_Bohnenesser.jpeg/500px-Carracci_-_Der_Bohnenesser.jpeg`.

### 250. annibale-carracci / Domine, Quo Vadis?

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `annibale-carracci` → `Domine, Quo Vadis?`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Domine%2C_quo_vadis.jpg/500px-Domine%2C_quo_vadis.jpg`; page: `https://en.wikipedia.org/wiki/Domine%2C_quo_vadis%3F`.
- Normalized gallery asset: `Domine, quo vadis.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/annibale-carracci`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 251. guido-reni / Aurora

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `guido-reni` → `Aurora`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Guido_Reni_-_L%27Aurora_di_Guido_Reni_nelle_arti_decorative.jpg/500px-Guido_Reni_-_L%27Aurora_di_Guido_Reni_nelle_arti_decorative.jpg`; page: `https://en.wikipedia.org/wiki/Aurora_(Reni)`.
- Normalized gallery asset: `Guido Reni - L'Aurora di Guido Reni nelle arti decorative.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/guido-reni`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 252. guido-reni / Saint Michael Archangel

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `guido-reni` → `Saint Michael Archangel`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/GuidoReni_MichaelDefeatsSatan.jpg/960px-GuidoReni_MichaelDefeatsSatan.jpg`; page: `https://commons.wikimedia.org/wiki/File:GuidoReni_MichaelDefeatsSatan.jpg`.
- Normalized gallery asset: `GuidoReni MichaelDefeatsSatan.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/guido-reni`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 253. guido-reni / Atalanta and Hippomenes

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `guido-reni` → `Atalanta and Hippomenes`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Guido_Reni_-_Atalanta_and_Hippomenes_-_Google_Art_Project.jpg/500px-Guido_Reni_-_Atalanta_and_Hippomenes_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Atalanta_and_Hippomenes`.
- Normalized gallery asset: `Guido Reni - Atalanta and Hippomenes - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/guido-reni`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 254. francisco-de-zurbaran / Still Life with Lemons, Oranges and a Rose

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `francisco-de-zurbaran` → `Still Life with Lemons, Oranges and a Rose`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Francisco_de_Zurbar%C3%A1n_-_Still_Life_with_Lemons%2C_Oranges_and_a_Rose.jpg/500px-Francisco_de_Zurbar%C3%A1n_-_Still_Life_with_Lemons%2C_Oranges_and_a_Rose.jpg`; page: `https://en.wikipedia.org/wiki/Still_Life_with_Lemons%2C_Oranges_and_a_Rose`.
- Normalized gallery asset: `Francisco de Zurbarán - Still Life with Lemons, Oranges and a Rose.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/francisco-de-zurbaran`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 255. francisco-de-zurbaran / Saint Serapion

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `francisco-de-zurbaran` → `Saint Serapion`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/San_Serapio%2C_por_Francisco_de_Zurbar%C3%A1n.jpg/500px-San_Serapio%2C_por_Francisco_de_Zurbar%C3%A1n.jpg`; page: `https://en.wikipedia.org/wiki/Saint_Serapion_(Zurbar%C3%A1n)`.
- Normalized gallery asset: `San Serapio, por Francisco de Zurbarán.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/francisco-de-zurbaran`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 256. francisco-de-zurbaran / Saint Francis in Meditation

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `francisco-de-zurbaran` → `Saint Francis in Meditation`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Francisco_de_Zurbar%C3%A1n_009.jpg/960px-Francisco_de_Zurbar%C3%A1n_009.jpg`; page: `https://commons.wikimedia.org/wiki/File:Francisco_de_Zurbar%C3%A1n_009.jpg`.
- Normalized gallery asset: `Francisco de Zurbarán 009.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/francisco-de-zurbaran`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 257. bartolome-murillo / The Immaculate Conception of Los Venerables

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `bartolome-murillo` → `The Immaculate Conception of Los Venerables`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Murillo_immaculate_conception.jpg/500px-Murillo_immaculate_conception.jpg`; page: `https://en.wikipedia.org/wiki/The_Immaculate_Conception_of_Los_Venerables`.
- Normalized gallery asset: `Murillo immaculate conception.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/bartolome-murillo`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 258. bartolome-murillo / Boys Eating Grapes and Melon

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `bartolome-murillo` → `Boys Eating Grapes and Melon`; img: `https://upload.wikimedia.org/wikipedia/commons/f/f0/Carl_Reiser_%281877%E2%80%931950%29%2C_copy_after_Bartolom%C3%A9_Esteban_Murillo_%281617%E2%80%931682%29_-_Beggar_Boys_Eating_Grapes_and_Melon_-_BORGM_00036_-_Russell-Cotes_Art_Gallery_%5E_Museum.jpg`; page: `https://commons.wikimedia.org/wiki/File:Carl_Reiser_(1877%E2%80%931950),_copy_after_Bartolom%C3%A9_Esteban_Murillo_(1617%E2%80%931682)_-_Beggar_Boys_Eating_Grapes_and_Melon_-_BORGM_00036_-_Russell-Cotes_Art_Gallery_%5E_Museum.jpg`.
- Normalized gallery asset: `Carl Reiser (1877–1950), copy after Bartolomé Esteban Murillo (1617–1682) - Beggar Boys Eating Grapes and Melon - BORGM 00036 - Russell-Cotes Art Gallery ^ Museum.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/bartolome-murillo`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 259. bartolome-murillo / The Young Beggar

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `bartolome-murillo` → `The Young Beggar`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Bartolom%C3%A9_Esteban_Murillo_-_Joven_mendigo_%281645-50%29.jpg/500px-Bartolom%C3%A9_Esteban_Murillo_-_Joven_mendigo_%281645-50%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Young_Beggar`.
- Normalized gallery asset: `Bartolomé Esteban Murillo - Joven mendigo (1645-50).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/bartolome-murillo`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 260. claude-lorrain / Seaport with the Embarkation of the Queen of Sheba

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `claude-lorrain` → `Seaport with the Embarkation of the Queen of Sheba`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Claude_Lorrain_008.jpg/500px-Claude_Lorrain_008.jpg`; page: `https://en.wikipedia.org/wiki/The_Embarkation_of_the_Queen_of_Sheba`.
- Normalized gallery asset: `Claude Lorrain 008.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-9.js` / `seaport-with-the-embarkation-of-the-queen-of-sheba`; title `Seaport with the Embarkation of the Queen of Sheba`; worksKey `(absent)`; artistId `claude-lorrain`. Evidence: same Commons asset `Claude Lorrain 008.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Claude_Lorrain_008.jpg/500px-Claude_Lorrain_008.jpg`; page: `https://commons.wikimedia.org/wiki/File:Claude_Lorrain_008.jpg`.
- Checked-in route `p/artwork/seaport-with-the-embarkation-of-the-queen-of-sheba.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Claude_Lorrain_008.jpg/500px-Claude_Lorrain_008.jpg`.

### 261. claude-lorrain / Landscape with Aeneas at Delos

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `claude-lorrain` → `Landscape with Aeneas at Delos`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Claude_Lorrain_-_Landscape_with_Aeneas_at_Delos_-_WGA05015.jpg/960px-Claude_Lorrain_-_Landscape_with_Aeneas_at_Delos_-_WGA05015.jpg`; page: `https://commons.wikimedia.org/wiki/File:Claude_Lorrain_-_Landscape_with_Aeneas_at_Delos_-_WGA05015.jpg`.
- Normalized gallery asset: `Claude Lorrain - Landscape with Aeneas at Delos - WGA05015.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/claude-lorrain`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 262. claude-lorrain / Landscape with Narcissus and Echo

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `claude-lorrain` → `Landscape with Narcissus and Echo`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Landscape_with_Narcissus_and_Echo.jpg/500px-Landscape_with_Narcissus_and_Echo.jpg`; page: `https://commons.wikimedia.org/wiki/File:Landscape_with_Narcissus_and_Echo.jpg`.
- Normalized gallery asset: `Landscape with Narcissus and Echo.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/claude-lorrain`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 263. judith-leyster / Self-Portrait

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `judith-leyster` → `Self-Portrait`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Self-portrait_by_Judith_Leyster.jpg/500px-Self-portrait_by_Judith_Leyster.jpg`; page: `https://en.wikipedia.org/wiki/Self-portrait_by_Judith_Leyster`.
- Normalized gallery asset: `Self-portrait by Judith Leyster.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/judith-leyster`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 264. judith-leyster / The Proposition

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `judith-leyster` → `The Proposition`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Judith_Leyster_The_Proposition.jpg/500px-Judith_Leyster_The_Proposition.jpg`; page: `https://en.wikipedia.org/wiki/The_Proposition_(Leyster)`.
- Normalized gallery asset: `Judith Leyster The Proposition.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/judith-leyster`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 265. judith-leyster / The Concert

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `judith-leyster` → `The Concert`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Judith_Leyster_The_Concert.jpg/960px-Judith_Leyster_The_Concert.jpg`; page: `https://commons.wikimedia.org/wiki/File:Judith_Leyster_The_Concert.jpg`.
- Normalized gallery asset: `Judith Leyster The Concert.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/judith-leyster`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 266. jan-steen / The Feast of Saint Nicholas

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jan-steen` → `The Feast of Saint Nicholas`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Jan_Havicksz._Steen_%E2%80%93_Het_Sint-Nicolaasfeest_%E2%80%93_Google_Art_Project.jpg/500px-Jan_Havicksz._Steen_%E2%80%93_Het_Sint-Nicolaasfeest_%E2%80%93_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Feast_of_Saint_Nicholas`.
- Normalized gallery asset: `Jan Havicksz. Steen – Het Sint-Nicolaasfeest – Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jan-steen`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 267. jan-steen / Beware of Luxury

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jan-steen` → `Beware of Luxury`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Jan_Steen_004.jpg/500px-Jan_Steen_004.jpg`; page: `https://en.wikipedia.org/wiki/Beware_of_Luxury`.
- Normalized gallery asset: `Jan Steen 004.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jan-steen`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 268. jan-steen / The Merry Family

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jan-steen` → `The Merry Family`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Jan_Steen_005.jpg/960px-Jan_Steen_005.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jan_Steen_005.jpg`.
- Normalized gallery asset: `Jan Steen 005.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jan-steen`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 269. jacob-van-ruisdael / The Windmill at Wijk bij Duurstede

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jacob-van-ruisdael` → `The Windmill at Wijk bij Duurstede`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Amsterdam_-_Rijksmuseum_1885_-_The_Gallery_of_Honour_%281st_Floor%29_-_The_Windmill_at_Wijk_bij_Duurstede_c._1670_by_Jacob_van_Ruisdael.png/960px-Amsterdam_-_Rijksmuseum_1885_-_The_Gallery_of_Honour_%281st_Floor%29_-_The_Windmill_at_Wijk_bij_Duurstede_c._1670_by_Jacob_van_Ruisdael.png`; page: `https://commons.wikimedia.org/wiki/File:Amsterdam_-_Rijksmuseum_1885_-_The_Gallery_of_Honour_(1st_Floor)_-_The_Windmill_at_Wijk_bij_Duurstede_c._1670_by_Jacob_van_Ruisdael.png`.
- Normalized gallery asset: `Amsterdam - Rijksmuseum 1885 - The Gallery of Honour (1st Floor) - The Windmill at Wijk bij Duurstede c. 1670 by Jacob van Ruisdael.png`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jacob-van-ruisdael`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 270. jacob-van-ruisdael / The Jewish Cemetery

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jacob-van-ruisdael` → `The Jewish Cemetery`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Jacob_Isaackszoon_van_Ruisdael_-_The_Jewish_Cemetery_%281654_or_1655%29.jpg/500px-Jacob_Isaackszoon_van_Ruisdael_-_The_Jewish_Cemetery_%281654_or_1655%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Jewish_Cemetery`.
- Normalized gallery asset: `Jacob Isaackszoon van Ruisdael - The Jewish Cemetery (1654 or 1655).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jacob-van-ruisdael`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 271. jacob-van-ruisdael / View of Haarlem with Bleaching Grounds

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jacob-van-ruisdael` → `View of Haarlem with Bleaching Grounds`; img: `https://upload.wikimedia.org/wikipedia/commons/0/07/View_of_Haarlem_with_Bleaching_Grounds_c1665_Ruisdael.jpg`; page: `https://commons.wikimedia.org/wiki/File:View_of_Haarlem_with_Bleaching_Grounds_c1665_Ruisdael.jpg`.
- Normalized gallery asset: `View of Haarlem with Bleaching Grounds c1665 Ruisdael.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jacob-van-ruisdael`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 272. clara-peeters / Still Life with Cheeses, Almonds and Pretzels

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `clara-peeters` → `Still Life with Cheeses, Almonds and Pretzels`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Clara_Peeters_-_Still_Life_with_Cheeses%2C_Almonds_and_Pretzels.jpg/500px-Clara_Peeters_-_Still_Life_with_Cheeses%2C_Almonds_and_Pretzels.jpg`; page: `https://en.wikipedia.org/wiki/Still_Life_with_Cheeses%2C_Almonds_and_Pretzels`.
- Normalized gallery asset: `Clara Peeters - Still Life with Cheeses, Almonds and Pretzels.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/clara-peeters`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 273. clara-peeters / Still Life with Flowers and Goblets

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `clara-peeters` → `Still Life with Flowers and Goblets`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Still_Life_with_Flowers_and_Gold_Cups_of_Honour_-_Clara_Peeters_-_Google_Cultural_Institute.jpg/960px-Still_Life_with_Flowers_and_Gold_Cups_of_Honour_-_Clara_Peeters_-_Google_Cultural_Institute.jpg`; page: `https://commons.wikimedia.org/wiki/File:Still_Life_with_Flowers_and_Gold_Cups_of_Honour_-_Clara_Peeters_-_Google_Cultural_Institute.jpg`.
- Normalized gallery asset: `Still Life with Flowers and Gold Cups of Honour - Clara Peeters - Google Cultural Institute.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/clara-peeters`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 274. clara-peeters / Still Life with Fish

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `clara-peeters` → `Still Life with Fish`; img: `https://upload.wikimedia.org/wikipedia/commons/7/7e/Clara_Peeters_-_Still_life_with_fish_and_cat.jpg`; page: `https://commons.wikimedia.org/wiki/File:Clara_Peeters_-_Still_life_with_fish_and_cat.jpg`.
- Normalized gallery asset: `Clara Peeters - Still life with fish and cat.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/clara-peeters`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 275. rachel-ruysch / Flower Still Life

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `rachel-ruysch` → `Flower Still Life`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Rachel_Ruysch_-_Still-Life_with_Flowers_-_WGA20555.jpg/500px-Rachel_Ruysch_-_Still-Life_with_Flowers_-_WGA20555.jpg`; page: `https://commons.wikimedia.org/wiki/File:Rachel_Ruysch_-_Still-Life_with_Flowers_-_WGA20555.jpg`.
- Normalized gallery asset: `Rachel Ruysch - Still-Life with Flowers - WGA20555.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/rachel-ruysch`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 276. rachel-ruysch / Roses, Convolvulus, Poppies and Other Flowers

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `rachel-ruysch` → `Roses, Convolvulus, Poppies and Other Flowers`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Roses%2C_Convolvulus%2C_Poppies%2C_and_Other_Flowers_in_an_Urn_on_a_Stone_Ledge_-_Rachel_Ruysch_-_Google_Cultural_Institute.jpg/960px-Roses%2C_Convolvulus%2C_Poppies%2C_and_Other_Flowers_in_an_Urn_on_a_Stone_Ledge_-_Rachel_Ruysch_-_Google_Cultural_Institute.jpg`; page: `https://commons.wikimedia.org/wiki/File:Roses,_Convolvulus,_Poppies,_and_Other_Flowers_in_an_Urn_on_a_Stone_Ledge_-_Rachel_Ruysch_-_Google_Cultural_Institute.jpg`.
- Normalized gallery asset: `Roses, Convolvulus, Poppies, and Other Flowers in an Urn on a Stone Ledge - Rachel Ruysch - Google Cultural Institute.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/rachel-ruysch`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 277. rachel-ruysch / Fruit and Insects

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `rachel-ruysch` → `Fruit and Insects`; img: `https://upload.wikimedia.org/wikipedia/commons/4/4a/Rachel_Ruysch_-_Still_Life_with_Fruit%2C_a_Bird%27s_Nest_and_Insects_NTII_DMS_814164.jpg`; page: `https://commons.wikimedia.org/wiki/File:Rachel_Ruysch_-_Still_Life_with_Fruit,_a_Bird%27s_Nest_and_Insects_NTII_DMS_814164.jpg`.
- Normalized gallery asset: `Rachel Ruysch - Still Life with Fruit, a Bird's Nest and Insects NTII DMS 814164.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/rachel-ruysch`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 278. francois-boucher / The Toilette of Venus

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `francois-boucher` → `The Toilette of Venus`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/The_Toilet_of_Venus%2C_by_Fran%C3%A7ois_Boucher.jpg/960px-The_Toilet_of_Venus%2C_by_Fran%C3%A7ois_Boucher.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Toilet_of_Venus,_by_Fran%C3%A7ois_Boucher.jpg`.
- Normalized gallery asset: `The Toilet of Venus, by François Boucher.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/francois-boucher`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 279. francois-boucher / Madame de Pompadour

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `francois-boucher` → `Madame de Pompadour`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Fran%C3%A7ois_Boucher_-_Madame_de_Pompadour%2C_1759.jpg/960px-Fran%C3%A7ois_Boucher_-_Madame_de_Pompadour%2C_1759.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fran%C3%A7ois_Boucher_-_Madame_de_Pompadour,_1759.jpg`.
- Normalized gallery asset: `François Boucher - Madame de Pompadour, 1759.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-7.js` / `madame-de-pompadour`; title `Madame de Pompadour`; worksKey `(absent)`; artistId `francois-boucher`. Evidence: same Commons asset `François Boucher - Madame de Pompadour, 1759.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Fran%C3%A7ois_Boucher_-_Madame_de_Pompadour%2C_1759.jpg/960px-Fran%C3%A7ois_Boucher_-_Madame_de_Pompadour%2C_1759.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fran%C3%A7ois_Boucher_-_Madame_de_Pompadour,_1759.jpg`.
- Checked-in route `p/artwork/madame-de-pompadour.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Fran%C3%A7ois_Boucher_-_Madame_de_Pompadour%2C_1759.jpg/960px-Fran%C3%A7ois_Boucher_-_Madame_de_Pompadour%2C_1759.jpg`.

### 280. francois-boucher / The Rising of the Sun

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `francois-boucher` → `The Rising of the Sun`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Fran%C3%A7ois_Boucher_-_The_Rising_of_the_Sun_-_WGA02916.jpg/500px-Fran%C3%A7ois_Boucher_-_The_Rising_of_the_Sun_-_WGA02916.jpg`; page: `https://en.wikipedia.org/wiki/The_Rising_of_the_Sun`.
- Normalized gallery asset: `François Boucher - The Rising of the Sun - WGA02916.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/francois-boucher`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 281. rosalba-carriera / Self-Portrait Holding a Portrait of Her Sister

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `rosalba-carriera` → `Self-Portrait Holding a Portrait of Her Sister`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Rosalba_Carriera_-_Self-Portrait_Holding_a_Portrait_of_Her_Sister_-_WGA4502.jpg/960px-Rosalba_Carriera_-_Self-Portrait_Holding_a_Portrait_of_Her_Sister_-_WGA4502.jpg`; page: `https://commons.wikimedia.org/wiki/File:Rosalba_Carriera_-_Self-Portrait_Holding_a_Portrait_of_Her_Sister_-_WGA4502.jpg`.
- Normalized gallery asset: `Rosalba Carriera - Self-Portrait Holding a Portrait of Her Sister - WGA4502.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/rosalba-carriera`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 282. rosalba-carriera / Portrait of Louis XV as a Young Man

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `rosalba-carriera` → `Portrait of Louis XV as a Young Man`; img: `https://upload.wikimedia.org/wikipedia/commons/4/48/Rosalba_Carriera_003.jpg`; page: `https://commons.wikimedia.org/wiki/File:Rosalba_Carriera_003.jpg`.
- Normalized gallery asset: `Rosalba Carriera 003.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/rosalba-carriera`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 283. joshua-reynolds / Portrait of Omai

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `joshua-reynolds` → `Portrait of Omai`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Joshua_Reynolds_-_Portrait_of_Omai.jpg/500px-Joshua_Reynolds_-_Portrait_of_Omai.jpg`; page: `https://en.wikipedia.org/wiki/Portrait_of_Omai`.
- Normalized gallery asset: `Joshua Reynolds - Portrait of Omai.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-8.js` / `portrait-of-omai`; title `Portrait of Omai`; worksKey `(absent)`; artistId `joshua-reynolds`. Evidence: same Commons asset `Joshua Reynolds - Portrait of Omai.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Joshua_Reynolds_-_Portrait_of_Omai.jpg/500px-Joshua_Reynolds_-_Portrait_of_Omai.jpg`; page: `https://commons.wikimedia.org/wiki/File:Joshua_Reynolds_-_Portrait_of_Omai.jpg`.
- Checked-in route `p/artwork/portrait-of-omai.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Joshua_Reynolds_-_Portrait_of_Omai.jpg/500px-Joshua_Reynolds_-_Portrait_of_Omai.jpg`.

### 284. joshua-reynolds / Mrs Siddons as the Tragic Muse

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `joshua-reynolds` → `Mrs Siddons as the Tragic Muse`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Mrs._Siddons_as_the_Tragic_Muse_%283051182537%29.jpg/500px-Mrs._Siddons_as_the_Tragic_Muse_%283051182537%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Mrs._Siddons_as_the_Tragic_Muse_(3051182537).jpg`.
- Normalized gallery asset: `Mrs. Siddons as the Tragic Muse (3051182537).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/joshua-reynolds`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 285. joshua-reynolds / Self-Portrait as a Deaf Man

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `joshua-reynolds` → `Self-Portrait as a Deaf Man`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Sir_Joshua_Reynolds_-_Self-Portrait_as_a_Deaf_Man_-_Google_Art_Project.jpg/960px-Sir_Joshua_Reynolds_-_Self-Portrait_as_a_Deaf_Man_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Sir_Joshua_Reynolds_-_Self-Portrait_as_a_Deaf_Man_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Sir Joshua Reynolds - Self-Portrait as a Deaf Man - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/joshua-reynolds`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 286. angelica-kauffman / Self-Portrait Hesitating between Music and Painting

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `angelica-kauffman` → `Self-Portrait Hesitating between Music and Painting`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Angelica_Kauffman_Self-portrait_Hesitating_between_the_Arts_of_Music_and_Painting.jpg/960px-Angelica_Kauffman_Self-portrait_Hesitating_between_the_Arts_of_Music_and_Painting.jpg`; page: `https://commons.wikimedia.org/wiki/File:Angelica_Kauffman_Self-portrait_Hesitating_between_the_Arts_of_Music_and_Painting.jpg`.
- Normalized gallery asset: `Angelica Kauffman Self-portrait Hesitating between the Arts of Music and Painting.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/angelica-kauffman`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 287. angelica-kauffman / Ariadne Abandoned by Theseus

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `angelica-kauffman` → `Ariadne Abandoned by Theseus`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Angelica_Kauffmann%2C_Ariadne_Abandoned_by_Theseus%2C_1774.jpg/500px-Angelica_Kauffmann%2C_Ariadne_Abandoned_by_Theseus%2C_1774.jpg`; page: `https://en.wikipedia.org/wiki/Ariadne_Abandoned_by_Theseus`.
- Normalized gallery asset: `Angelica Kauffmann, Ariadne Abandoned by Theseus, 1774.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/angelica-kauffman`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 288. george-stubbs / Whistlejacket

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `george-stubbs` → `Whistlejacket`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Whistlejacket_by_George_Stubbs_edit.jpg/500px-Whistlejacket_by_George_Stubbs_edit.jpg`; page: `https://en.wikipedia.org/wiki/Whistlejacket`.
- Normalized gallery asset: `Whistlejacket by George Stubbs edit.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/george-stubbs`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 289. george-stubbs / The Anatomy of the Horse

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `george-stubbs` → `The Anatomy of the Horse`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Stubbs_Anatomy_of_the_Horse_2.JPG/960px-Stubbs_Anatomy_of_the_Horse_2.JPG`; page: `https://commons.wikimedia.org/wiki/File:Stubbs_Anatomy_of_the_Horse_2.JPG`.
- Normalized gallery asset: `Stubbs Anatomy of the Horse 2.JPG`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/george-stubbs`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 290. george-stubbs / Horse Attacked by a Lion

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `george-stubbs` → `Horse Attacked by a Lion`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/George_Stubbs_-_Horse_Devoured_by_a_Lion_-_Google_Art_Project.jpg/500px-George_Stubbs_-_Horse_Devoured_by_a_Lion_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:George_Stubbs_-_Horse_Devoured_by_a_Lion_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `George Stubbs - Horse Devoured by a Lion - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/george-stubbs`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 291. joseph-wright-of-derby / An Experiment on a Bird in the Air Pump

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `joseph-wright-of-derby` → `An Experiment on a Bird in the Air Pump`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/An_Experiment_on_a_Bird_in_an_Air_Pump_by_Joseph_Wright_of_Derby%2C_1768.jpg/500px-An_Experiment_on_a_Bird_in_an_Air_Pump_by_Joseph_Wright_of_Derby%2C_1768.jpg`; page: `https://en.wikipedia.org/wiki/An_Experiment_on_a_Bird_in_the_Air_Pump`.
- Normalized gallery asset: `An Experiment on a Bird in an Air Pump by Joseph Wright of Derby, 1768.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/joseph-wright-of-derby`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 292. joseph-wright-of-derby / A Philosopher Lecturing on the Orrery

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `joseph-wright-of-derby` → `A Philosopher Lecturing on the Orrery`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Wright_of_Derby%2C_The_Orrery.jpg/500px-Wright_of_Derby%2C_The_Orrery.jpg`; page: `https://en.wikipedia.org/wiki/A_Philosopher_Lecturing_on_the_Orrery`.
- Normalized gallery asset: `Wright of Derby, The Orrery.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/joseph-wright-of-derby`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 293. joseph-wright-of-derby / Vesuvius in Eruption

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `joseph-wright-of-derby` → `Vesuvius in Eruption`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Joseph_Wright_of_Derby_-_Vesuvius_in_Eruption%2C_with_a_View_over_the_Islands_in_the_Bay_of_Naples_-_Google_Art_Project.jpg/960px-Joseph_Wright_of_Derby_-_Vesuvius_in_Eruption%2C_with_a_View_over_the_Islands_in_the_Bay_of_Naples_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Joseph_Wright_of_Derby_-_Vesuvius_in_Eruption,_with_a_View_over_the_Islands_in_the_Bay_of_Naples_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Joseph Wright of Derby - Vesuvius in Eruption, with a View over the Islands in the Bay of Naples - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/joseph-wright-of-derby`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 294. piranesi / Carceri d'invenzione

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `piranesi` → `Carceri d'invenzione`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Giovanni_Battista_Piranesi_-_Le_Carceri_d%27Invenzione_-_Second_Edition_-_1761_-_01_-_Title_Plate.jpg/500px-Giovanni_Battista_Piranesi_-_Le_Carceri_d%27Invenzione_-_Second_Edition_-_1761_-_01_-_Title_Plate.jpg`; page: `https://en.wikipedia.org/wiki/Carceri_d'invenzione`.
- Normalized gallery asset: `Giovanni Battista Piranesi - Le Carceri d'Invenzione - Second Edition - 1761 - 01 - Title Plate.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/piranesi`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 295. piranesi / Vedute di Roma

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `piranesi` → `Vedute di Roma`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Giovanni_Battista_Piranesi%2C_The_Colosseum.png/960px-Giovanni_Battista_Piranesi%2C_The_Colosseum.png`; page: `https://commons.wikimedia.org/wiki/File:Giovanni_Battista_Piranesi,_The_Colosseum.png`.
- Normalized gallery asset: `Giovanni Battista Piranesi, The Colosseum.png`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/piranesi`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 296. piranesi / Antichità Romane

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `piranesi` → `Antichità Romane`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Giovanni_Battista_Piranesi_-_Le_Antichit%C3%A0_romane%2C_tomo_III_%28segundo_frontisp%C3%ADcio%29_1750-53.jpg/960px-Giovanni_Battista_Piranesi_-_Le_Antichit%C3%A0_romane%2C_tomo_III_%28segundo_frontisp%C3%ADcio%29_1750-53.jpg`; page: `https://commons.wikimedia.org/wiki/File:Giovanni_Battista_Piranesi_-_Le_Antichit%C3%A0_romane,_tomo_III_(segundo_frontisp%C3%ADcio)_1750-53.jpg`.
- Normalized gallery asset: `Giovanni Battista Piranesi - Le Antichità romane, tomo III (segundo frontispício) 1750-53.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/piranesi`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 297. matrakci-nasuh / View of Istanbul (Mecmu-ı Menazil)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `matrakci-nasuh` → `View of Istanbul (Mecmu-ı Menazil)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Matrak%C3%A7%C4%B1_Nasuh_-_%C4%B0stanbul.jpg/960px-Matrak%C3%A7%C4%B1_Nasuh_-_%C4%B0stanbul.jpg`; page: `https://commons.wikimedia.org/wiki/File:Matrak%C3%A7%C4%B1_Nasuh_-_%C4%B0stanbul.jpg`.
- Normalized gallery asset: `Matrakçı Nasuh - İstanbul.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/matrakci-nasuh`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 298. matrakci-nasuh / View of Aleppo

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `matrakci-nasuh` → `View of Aleppo`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Aleppo_ca1537_by_Matrakci_Nasuh_Istanbul_University_Library_ms_5964.png/960px-Aleppo_ca1537_by_Matrakci_Nasuh_Istanbul_University_Library_ms_5964.png`; page: `https://commons.wikimedia.org/wiki/File:Aleppo_ca1537_by_Matrakci_Nasuh_Istanbul_University_Library_ms_5964.png`.
- Normalized gallery asset: `Aleppo ca1537 by Matrakci Nasuh Istanbul University Library ms 5964.png`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/matrakci-nasuh`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 299. nakkas-osman / Surname-i Hümayun (Imperial Festival Book)

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `nakkas-osman` → `Surname-i Hümayun (Imperial Festival Book)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Sueleymaniye_painting_by_Osman.jpg/500px-Sueleymaniye_painting_by_Osman.jpg`; page: `https://commons.wikimedia.org/wiki/File:Sueleymaniye_painting_by_Osman.jpg`.
- Normalized gallery asset: `Sueleymaniye painting by Osman.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-8.js` / `surname-i-humayun`; title `Surname-i Hümayun`; worksKey `Surname-i Hümayun (Imperial Festival Book)`; artistId `nakkas-osman`. Evidence: same Commons asset `Sueleymaniye painting by Osman.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Sueleymaniye_painting_by_Osman.jpg/500px-Sueleymaniye_painting_by_Osman.jpg`; page: `https://commons.wikimedia.org/wiki/File:Sueleymaniye_painting_by_Osman.jpg`.
- Checked-in route `p/artwork/surname-i-humayun.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Sueleymaniye_painting_by_Osman.jpg/500px-Sueleymaniye_painting_by_Osman.jpg`.

### 300. nakkas-osman / Şemailname (Portraits of the Sultans)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `nakkas-osman` → `Şemailname (Portraits of the Sultans)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Portrait_of_Selim_II_by_Nakka%C5%9F_Osman%2C_%C5%9Eem%C3%A2%27iln%C3%A2me%2C_1579%2C_Istanbul%2C_Topkap%C4%B1_Saray%C4%B1_M%C3%BCzesi%2C_%D0%9D._1563.jpg/960px-Portrait_of_Selim_II_by_Nakka%C5%9F_Osman%2C_%C5%9Eem%C3%A2%27iln%C3%A2me%2C_1579%2C_Istanbul%2C_Topkap%C4%B1_Saray%C4%B1_M%C3%BCzesi%2C_%D0%9D._1563.jpg`; page: `https://commons.wikimedia.org/wiki/File:Portrait_of_Selim_II_by_Nakka%C5%9F_Osman,_%C5%9Eem%C3%A2%27iln%C3%A2me,_1579,_Istanbul,_Topkap%C4%B1_Saray%C4%B1_M%C3%BCzesi,_%D0%9D._1563.jpg`.
- Normalized gallery asset: `Portrait of Selim II by Nakkaş Osman, Şemâ'ilnâme, 1579, Istanbul, Topkapı Sarayı Müzesi, Н. 1563.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/nakkas-osman`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 301. nakkas-osman / Hünername

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `nakkas-osman` → `Hünername`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Osman_I_miniature_by_Nakka%C5%9F_Osman.jpg/500px-Osman_I_miniature_by_Nakka%C5%9F_Osman.jpg`; page: `https://commons.wikimedia.org/wiki/File:Osman_I_miniature_by_Nakka%C5%9F_Osman.jpg`.
- Normalized gallery asset: `Osman I miniature by Nakkaş Osman.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/nakkas-osman`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 302. levni / Surname-i Vehbi

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `levni` → `Surname-i Vehbi`; img: `https://upload.wikimedia.org/wikipedia/commons/a/aa/Koceks_-_Surname-i_Vehbi.jpg`; page: `https://commons.wikimedia.org/wiki/File:Koceks_-_Surname-i_Vehbi.jpg`.
- Normalized gallery asset: `Koceks - Surname-i Vehbi.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/levni`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 303. levni / Portrait of Sultan Ahmed III

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `levni` → `Portrait of Sultan Ahmed III`; img: `https://upload.wikimedia.org/wikipedia/commons/5/5c/Levni_002_detail.jpg`; page: `https://commons.wikimedia.org/wiki/File:Levni_002_detail.jpg`.
- Normalized gallery asset: `Levni 002 detail.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/levni`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 304. william-blake / The Ancient of Days

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `william-blake` → `The Ancient of Days`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/The_Ancient_of_Days_-_etching_with_pen_%26_ink_wc_Whitworth_Art_Gallery_The_University_of_Manchester_UK_The_Bridgeman_Art_Library.jpg/500px-The_Ancient_of_Days_-_etching_with_pen_%26_ink_wc_Whitworth_Art_Gallery_The_University_of_Manchester_UK_The_Bridgeman_Art_Library.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_Ancient_of_Days_-_etching_with_pen_%26_ink_wc_Whitworth_Art_Gallery_The_University_of_Manchester_UK_The_Bridgeman_Art_Library.jpg`.
- Normalized gallery asset: `The Ancient of Days - etching with pen & ink wc Whitworth Art Gallery The University of Manchester UK The Bridgeman Art Library.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/william-blake`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 305. william-blake / Newton

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `william-blake` → `Newton`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Newton-WilliamBlake.jpg/500px-Newton-WilliamBlake.jpg`; page: `https://en.wikipedia.org/wiki/Newton_(Blake)`.
- Normalized gallery asset: `Newton-WilliamBlake.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/william-blake`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 306. william-blake / The Great Red Dragon series

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `william-blake` → `The Great Red Dragon series`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/William_Blake%2C_The_Great_Red_Dragon_and_the_Beast_from_the_Sea%2C_c._1805%2C_NGA_11499.jpg/500px-William_Blake%2C_The_Great_Red_Dragon_and_the_Beast_from_the_Sea%2C_c._1805%2C_NGA_11499.jpg`; page: `https://commons.wikimedia.org/wiki/File:William_Blake,_The_Great_Red_Dragon_and_the_Beast_from_the_Sea,_c._1805,_NGA_11499.jpg`.
- Normalized gallery asset: `William Blake, The Great Red Dragon and the Beast from the Sea, c. 1805, NGA 11499.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/william-blake`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 307. camille-corot / The Bridge at Narni

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `camille-corot` → `The Bridge at Narni`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Le_pont_de_Narni_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1613_-_photo_2.jpg/500px-Le_pont_de_Narni_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1613_-_photo_2.jpg`; page: `https://en.wikipedia.org/wiki/The_Bridge_at_Narni`.
- Normalized gallery asset: `Le pont de Narni - Jean-Baptiste Camille Corot - Musée du Louvre Peintures RF 1613 - photo 2.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-8.js` / `the-bridge-at-narni`; title `The Bridge at Narni`; worksKey `(absent)`; artistId `camille-corot`. Evidence: same Commons asset `Le pont de Narni - Jean-Baptiste Camille Corot - Musée du Louvre Peintures RF 1613 - photo 2.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Le_pont_de_Narni_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1613_-_photo_2.jpg/500px-Le_pont_de_Narni_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1613_-_photo_2.jpg`; page: `https://commons.wikimedia.org/wiki/File:Le_pont_de_Narni_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1613_-_photo_2.jpg`.
- Checked-in route `p/artwork/the-bridge-at-narni.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Le_pont_de_Narni_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1613_-_photo_2.jpg/500px-Le_pont_de_Narni_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1613_-_photo_2.jpg`.

### 308. camille-corot / Souvenir de Mortefontaine

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `camille-corot` → `Souvenir de Mortefontaine`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Souvenir_de_Mortefontaine_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_MI_692_bis_-_photo_2.jpg/500px-Souvenir_de_Mortefontaine_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_MI_692_bis_-_photo_2.jpg`; page: `https://en.wikipedia.org/wiki/Souvenir_de_Mortefontaine`.
- Normalized gallery asset: `Souvenir de Mortefontaine - Jean-Baptiste Camille Corot - Musée du Louvre Peintures MI 692 bis - photo 2.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/camille-corot`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 309. camille-corot / Woman with a Pearl

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `camille-corot` → `Woman with a Pearl`; img: `https://upload.wikimedia.org/wikipedia/commons/3/3a/Camille_Corot_-_Woman_with_a_Pearl.jpg`; page: `https://commons.wikimedia.org/wiki/File:Camille_Corot_-_Woman_with_a_Pearl.jpg`.
- Normalized gallery asset: `Camille Corot - Woman with a Pearl.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/camille-corot`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 310. honore-daumier / Gargantua

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `honore-daumier` → `Gargantua`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Honor%C3%A9_Daumier_-_Gargantua.jpg/960px-Honor%C3%A9_Daumier_-_Gargantua.jpg`; page: `https://commons.wikimedia.org/wiki/File:Honor%C3%A9_Daumier_-_Gargantua.jpg`.
- Normalized gallery asset: `Honoré Daumier - Gargantua.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/honore-daumier`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 311. honore-daumier / Rue Transnonain, le 15 avril 1834

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `honore-daumier` → `Rue Transnonain, le 15 avril 1834`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Honor%C3%A9_Daumier%2C_Rue_Transnonain%2C_le_15_avril_1834%2C_1834%2C_NGA_6133.jpg/960px-Honor%C3%A9_Daumier%2C_Rue_Transnonain%2C_le_15_avril_1834%2C_1834%2C_NGA_6133.jpg`; page: `https://commons.wikimedia.org/wiki/File:Honor%C3%A9_Daumier,_Rue_Transnonain,_le_15_avril_1834,_1834,_NGA_6133.jpg`.
- Normalized gallery asset: `Honoré Daumier, Rue Transnonain, le 15 avril 1834, 1834, NGA 6133.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/honore-daumier`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 312. honore-daumier / The Third-Class Carriage

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `honore-daumier` → `The Third-Class Carriage`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Honor%C3%A9_Daumier%2C_The_Third-Class_Carriage_-_The_Metropolitan_Museum_of_Art.jpg/500px-Honor%C3%A9_Daumier%2C_The_Third-Class_Carriage_-_The_Metropolitan_Museum_of_Art.jpg`; page: `https://en.wikipedia.org/wiki/The_Third-Class_Carriage`.
- Normalized gallery asset: `Honoré Daumier, The Third-Class Carriage - The Metropolitan Museum of Art.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-8.js` / `the-third-class-carriage`; title `The Third-Class Carriage`; worksKey `(absent)`; artistId `honore-daumier`. Evidence: same Commons asset `Honoré Daumier, The Third-Class Carriage - The Metropolitan Museum of Art.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Honor%C3%A9_Daumier%2C_The_Third-Class_Carriage_-_The_Metropolitan_Museum_of_Art.jpg/500px-Honor%C3%A9_Daumier%2C_The_Third-Class_Carriage_-_The_Metropolitan_Museum_of_Art.jpg`; page: `https://commons.wikimedia.org/wiki/File:Honor%C3%A9_Daumier,_The_Third-Class_Carriage_-_The_Metropolitan_Museum_of_Art.jpg`.
- Checked-in route `p/artwork/the-third-class-carriage.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Honor%C3%A9_Daumier%2C_The_Third-Class_Carriage_-_The_Metropolitan_Museum_of_Art.jpg/500px-Honor%C3%A9_Daumier%2C_The_Third-Class_Carriage_-_The_Metropolitan_Museum_of_Art.jpg`.

### 313. rosa-bonheur / The Horse Fair

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `rosa-bonheur` → `The Horse Fair`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Rosa_Bonheur%2C_The_Horse_Fair%2C_1852%E2%80%9355.jpg/500px-Rosa_Bonheur%2C_The_Horse_Fair%2C_1852%E2%80%9355.jpg`; page: `https://en.wikipedia.org/wiki/The_Horse_Fair`.
- Normalized gallery asset: `Rosa Bonheur, The Horse Fair, 1852–55.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/rosa-bonheur`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 314. rosa-bonheur / Ploughing in the Nivernais

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `rosa-bonheur` → `Ploughing in the Nivernais`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Rosa_Bonheur_-_Ploughing_in_Nevers_-_Google_Art_Project.jpg/500px-Rosa_Bonheur_-_Ploughing_in_Nevers_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Ploughing_in_the_Nivernais`.
- Normalized gallery asset: `Rosa Bonheur - Ploughing in Nevers - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/rosa-bonheur`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 315. rosa-bonheur / The Lion at Home

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `rosa-bonheur` → `The Lion at Home`; img: `https://upload.wikimedia.org/wikipedia/commons/5/54/Rosa_Bonheur_%281822-1899%29_-_The_Lion_at_Home_-_KINCM-2005.4763_-_Ferens_Art_Gallery.jpg`; page: `https://commons.wikimedia.org/wiki/File:Rosa_Bonheur_(1822-1899)_-_The_Lion_at_Home_-_KINCM-2005.4763_-_Ferens_Art_Gallery.jpg`.
- Normalized gallery asset: `Rosa Bonheur (1822-1899) - The Lion at Home - KINCM-2005.4763 - Ferens Art Gallery.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/rosa-bonheur`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 316. utagawa-hiroshige / The Fifty-three Stations of the Tōkaidō

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `utagawa-hiroshige` → `The Fifty-three Stations of the Tōkaidō`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Utagawa_Hiroshige_%28the_first%29_-_Shono_from_the_Fifty-three_Stations_on_Tokaido_Highway%2C_Hoeido_version_-_Google_Art_Project.jpg/500px-Utagawa_Hiroshige_%28the_first%29_-_Shono_from_the_Fifty-three_Stations_on_Tokaido_Highway%2C_Hoeido_version_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Utagawa_Hiroshige_(the_first)_-_Shono_from_the_Fifty-three_Stations_on_Tokaido_Highway,_Hoeido_version_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Utagawa Hiroshige (the first) - Shono from the Fifty-three Stations on Tokaido Highway, Hoeido version - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/utagawa-hiroshige`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 317. utagawa-hiroshige / Sudden Shower over Shin-Ōhashi

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `utagawa-hiroshige` → `Sudden Shower over Shin-Ōhashi`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Hiroshige%2C_Sudden_shower_over_Shin-%C5%8Chashi_bridge_and_Atake%2C_1857.jpg/960px-Hiroshige%2C_Sudden_shower_over_Shin-%C5%8Chashi_bridge_and_Atake%2C_1857.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hiroshige,_Sudden_shower_over_Shin-%C5%8Chashi_bridge_and_Atake,_1857.jpg`.
- Normalized gallery asset: `Hiroshige, Sudden shower over Shin-Ōhashi bridge and Atake, 1857.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/utagawa-hiroshige`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 318. utagawa-hiroshige / One Hundred Famous Views of Edo

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `utagawa-hiroshige` → `One Hundred Famous Views of Edo`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Hiroshige_Atake_sous_une_averse_soudaine.jpg/500px-Hiroshige_Atake_sous_une_averse_soudaine.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hiroshige_Atake_sous_une_averse_soudaine.jpg`.
- Normalized gallery asset: `Hiroshige Atake sous une averse soudaine.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/utagawa-hiroshige`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 319. ivan-aivazovsky / The Ninth Wave

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `ivan-aivazovsky` → `The Ninth Wave`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Hovhannes_Aivazovsky_-_The_Ninth_Wave_-_Google_Art_Project.jpg/500px-Hovhannes_Aivazovsky_-_The_Ninth_Wave_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Ninth_Wave`.
- Normalized gallery asset: `Hovhannes Aivazovsky - The Ninth Wave - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-8.js` / `the-ninth-wave`; title `The Ninth Wave`; worksKey `(absent)`; artistId `ivan-aivazovsky`. Evidence: same Commons asset `Hovhannes Aivazovsky - The Ninth Wave - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Hovhannes_Aivazovsky_-_The_Ninth_Wave_-_Google_Art_Project.jpg/500px-Hovhannes_Aivazovsky_-_The_Ninth_Wave_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hovhannes_Aivazovsky_-_The_Ninth_Wave_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/the-ninth-wave.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Hovhannes_Aivazovsky_-_The_Ninth_Wave_-_Google_Art_Project.jpg/500px-Hovhannes_Aivazovsky_-_The_Ninth_Wave_-_Google_Art_Project.jpg`.

### 320. ivan-aivazovsky / Among the Waves

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ivan-aivazovsky` → `Among the Waves`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Ivan_Konstantinovich_Aivazovsky_-_Among_the_Waves%2C_1898.jpg/500px-Ivan_Konstantinovich_Aivazovsky_-_Among_the_Waves%2C_1898.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ivan_Konstantinovich_Aivazovsky_-_Among_the_Waves,_1898.jpg`.
- Normalized gallery asset: `Ivan Konstantinovich Aivazovsky - Among the Waves, 1898.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ivan-aivazovsky`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 321. ivan-aivazovsky / The Black Sea

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ivan-aivazovsky` → `The Black Sea`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Black_sea_by_Ivan_Aivazovsky.jpg/960px-Black_sea_by_Ivan_Aivazovsky.jpg`; page: `https://commons.wikimedia.org/wiki/File:Black_sea_by_Ivan_Aivazovsky.jpg`.
- Normalized gallery asset: `Black sea by Ivan Aivazovsky.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ivan-aivazovsky`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 322. ilya-repin / Barge Haulers on the Volga

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `ilya-repin` → `Barge Haulers on the Volga`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Ilia_Efimovich_Repin_%281844-1930%29_-_Volga_Boatmen_%281870-1873%29.jpg/500px-Ilia_Efimovich_Repin_%281844-1930%29_-_Volga_Boatmen_%281870-1873%29.jpg`; page: `https://en.wikipedia.org/wiki/Barge_Haulers_on_the_Volga`.
- Normalized gallery asset: `Ilia Efimovich Repin (1844-1930) - Volga Boatmen (1870-1873).jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `barge-haulers-on-the-volga`; title `Barge Haulers on the Volga`; worksKey `Barge Haulers on the Volga`; artistId `ilya-repin`. Evidence: same Commons asset `Ilia Efimovich Repin (1844-1930) - Volga Boatmen (1870-1873).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Ilia_Efimovich_Repin_%281844-1930%29_-_Volga_Boatmen_%281870-1873%29.jpg/500px-Ilia_Efimovich_Repin_%281844-1930%29_-_Volga_Boatmen_%281870-1873%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ilia_Efimovich_Repin_(1844-1930)_-_Volga_Boatmen_(1870-1873).jpg`.
- Checked-in route `p/artwork/barge-haulers-on-the-volga.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Ilia_Efimovich_Repin_%281844-1930%29_-_Volga_Boatmen_%281870-1873%29.jpg/500px-Ilia_Efimovich_Repin_%281844-1930%29_-_Volga_Boatmen_%281870-1873%29.jpg`.

### 323. ilya-repin / Reply of the Zaporozhian Cossacks

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `ilya-repin` → `Reply of the Zaporozhian Cossacks`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Ilja_Jefimowitsch_Repin_-_Reply_of_the_Zaporozhian_Cossacks_-_Yorck.jpg/500px-Ilja_Jefimowitsch_Repin_-_Reply_of_the_Zaporozhian_Cossacks_-_Yorck.jpg`; page: `https://en.wikipedia.org/wiki/Reply_of_the_Zaporozhian_Cossacks`.
- Normalized gallery asset: `Ilja Jefimowitsch Repin - Reply of the Zaporozhian Cossacks - Yorck.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `reply-of-the-zaporozhian-cossacks`; title `Reply of the Zaporozhian Cossacks`; worksKey `Reply of the Zaporozhian Cossacks`; artistId `ilya-repin`. Evidence: same Commons asset `Ilja Jefimowitsch Repin - Reply of the Zaporozhian Cossacks - Yorck.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Ilja_Jefimowitsch_Repin_-_Reply_of_the_Zaporozhian_Cossacks_-_Yorck.jpg/500px-Ilja_Jefimowitsch_Repin_-_Reply_of_the_Zaporozhian_Cossacks_-_Yorck.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ilja_Jefimowitsch_Repin_-_Reply_of_the_Zaporozhian_Cossacks_-_Yorck.jpg`.
- Checked-in route `p/artwork/reply-of-the-zaporozhian-cossacks.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Ilja_Jefimowitsch_Repin_-_Reply_of_the_Zaporozhian_Cossacks_-_Yorck.jpg/500px-Ilja_Jefimowitsch_Repin_-_Reply_of_the_Zaporozhian_Cossacks_-_Yorck.jpg`.

### 324. ilya-repin / Ivan the Terrible and His Son Ivan

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `ilya-repin` → `Ivan the Terrible and His Son Ivan`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Iv%C3%A1n_el_Terrible_y_su_hijo%2C_por_Ili%C3%A1_Repin.jpg/500px-Iv%C3%A1n_el_Terrible_y_su_hijo%2C_por_Ili%C3%A1_Repin.jpg`; page: `https://en.wikipedia.org/wiki/Ivan_the_Terrible_and_His_Son_Ivan`.
- Normalized gallery asset: `Iván el Terrible y su hijo, por Iliá Repin.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-4.js` / `ivan-the-terrible-and-his-son`; title `Ivan the Terrible and His Son Ivan`; worksKey `Ivan the Terrible and His Son Ivan`; artistId `ilya-repin`. Evidence: same Commons asset `Iván el Terrible y su hijo, por Iliá Repin.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Iv%C3%A1n_el_Terrible_y_su_hijo%2C_por_Ili%C3%A1_Repin.jpg/500px-Iv%C3%A1n_el_Terrible_y_su_hijo%2C_por_Ili%C3%A1_Repin.jpg`; page: `https://commons.wikimedia.org/wiki/File:Iv%C3%A1n_el_Terrible_y_su_hijo,_por_Ili%C3%A1_Repin.jpg`.
- Checked-in route `p/artwork/ivan-the-terrible-and-his-son.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Iv%C3%A1n_el_Terrible_y_su_hijo%2C_por_Ili%C3%A1_Repin.jpg/500px-Iv%C3%A1n_el_Terrible_y_su_hijo%2C_por_Ili%C3%A1_Repin.jpg`.

### 325. albert-bierstadt / The Rocky Mountains, Lander's Peak

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `albert-bierstadt` → `The Rocky Mountains, Lander's Peak`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Albert_Bierstadt_-_The_Rocky_Mountains%2C_Lander%27s_Peak.jpg/500px-Albert_Bierstadt_-_The_Rocky_Mountains%2C_Lander%27s_Peak.jpg`; page: `https://en.wikipedia.org/wiki/The_Rocky_Mountains%2C_Lander's_Peak`.
- Normalized gallery asset: `Albert Bierstadt - The Rocky Mountains, Lander's Peak.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/albert-bierstadt`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 326. albert-bierstadt / Among the Sierra Nevada, California

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `albert-bierstadt` → `Among the Sierra Nevada, California`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Bierstadt_-_Among_the_Sierra_Nevada_Mountains_-_1868.jpg/500px-Bierstadt_-_Among_the_Sierra_Nevada_Mountains_-_1868.jpg`; page: `https://en.wikipedia.org/wiki/Among_the_Sierra_Nevada%2C_California`.
- Normalized gallery asset: `Bierstadt - Among the Sierra Nevada Mountains - 1868.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/albert-bierstadt`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 327. albert-bierstadt / A Storm in the Rocky Mountains, Mt. Rosalie

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `albert-bierstadt` → `A Storm in the Rocky Mountains, Mt. Rosalie`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Albert_Bierstadt_-_A_Storm_in_the_Rocky_Mountains%2C_Mt._Rosalie_-_Google_Art_Project.jpg/500px-Albert_Bierstadt_-_A_Storm_in_the_Rocky_Mountains%2C_Mt._Rosalie_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/A_Storm_in_the_Rocky_Mountains%2C_Mt._Rosalie`.
- Normalized gallery asset: `Albert Bierstadt - A Storm in the Rocky Mountains, Mt. Rosalie - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/albert-bierstadt`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 328. winslow-homer / The Gulf Stream

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `winslow-homer` → `The Gulf Stream`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Winslow_Homer_-_The_Gulf_Stream_-_Metropolitan_Museum_of_Art.jpg/500px-Winslow_Homer_-_The_Gulf_Stream_-_Metropolitan_Museum_of_Art.jpg`; page: `https://en.wikipedia.org/wiki/The_Gulf_Stream_(painting)`.
- Normalized gallery asset: `Winslow Homer - The Gulf Stream - Metropolitan Museum of Art.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/winslow-homer`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 329. winslow-homer / Breezing Up (A Fair Wind)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `winslow-homer` → `Breezing Up (A Fair Wind)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Winslow_Homer_-_Breezing_Up_%28A_Fair_Wind%29_-_Google_Art_Project.jpg/500px-Winslow_Homer_-_Breezing_Up_%28A_Fair_Wind%29_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Breezing_Up_(A_Fair_Wind)`.
- Normalized gallery asset: `Winslow Homer - Breezing Up (A Fair Wind) - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/winslow-homer`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 330. winslow-homer / Snap the Whip

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `winslow-homer` → `Snap the Whip`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Winslow_Homer_-_Snap_the_Whip_%28Butler_Institute_of_American_Art%29.jpg/500px-Winslow_Homer_-_Snap_the_Whip_%28Butler_Institute_of_American_Art%29.jpg`; page: `https://en.wikipedia.org/wiki/Snap_the_Whip`.
- Normalized gallery asset: `Winslow Homer - Snap the Whip (Butler Institute of American Art).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/winslow-homer`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 331. john-everett-millais / Ophelia

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `john-everett-millais` → `Ophelia`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/John_Everett_Millais_-_Ophelia_-_Google_Art_Project.jpg/500px-John_Everett_Millais_-_Ophelia_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Ophelia_(Millais)`.
- Normalized gallery asset: `John Everett Millais - Ophelia - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/john-everett-millais`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 332. john-everett-millais / Christ in the House of His Parents

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `john-everett-millais` → `Christ in the House of His Parents`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/John_Everett_Millais_-_Christ_in_the_House_of_His_Parents_%28%60The_Carpenter%27s_Shop%27%29_-_Google_Art_Project.jpg/500px-John_Everett_Millais_-_Christ_in_the_House_of_His_Parents_%28%60The_Carpenter%27s_Shop%27%29_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Christ_in_the_House_of_His_Parents`.
- Normalized gallery asset: `John Everett Millais - Christ in the House of His Parents (`The Carpenter's Shop') - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/john-everett-millais`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 333. john-everett-millais / The Blind Girl

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `john-everett-millais` → `The Blind Girl`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/John_Everett_Millais_-_The_Blind_Girl%2C_1854-56.jpg/500px-John_Everett_Millais_-_The_Blind_Girl%2C_1854-56.jpg`; page: `https://en.wikipedia.org/wiki/The_Blind_Girl`.
- Normalized gallery asset: `John Everett Millais - The Blind Girl, 1854-56.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/john-everett-millais`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 334. dante-gabriel-rossetti / Beata Beatrix

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `dante-gabriel-rossetti` → `Beata Beatrix`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Dante_Gabriel_Rossetti_-_Beata_Beatrix%2C_1864-1870.jpg/500px-Dante_Gabriel_Rossetti_-_Beata_Beatrix%2C_1864-1870.jpg`; page: `https://en.wikipedia.org/wiki/Beata_Beatrix`.
- Normalized gallery asset: `Dante Gabriel Rossetti - Beata Beatrix, 1864-1870.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-8.js` / `beata-beatrix`; title `Beata Beatrix`; worksKey `(absent)`; artistId `dante-gabriel-rossetti`. Evidence: same Commons asset `Dante Gabriel Rossetti - Beata Beatrix, 1864-1870.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Dante_Gabriel_Rossetti_-_Beata_Beatrix%2C_1864-1870.jpg/500px-Dante_Gabriel_Rossetti_-_Beata_Beatrix%2C_1864-1870.jpg`; page: `https://commons.wikimedia.org/wiki/File:Dante_Gabriel_Rossetti_-_Beata_Beatrix,_1864-1870.jpg`.
- Checked-in route `p/artwork/beata-beatrix.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Dante_Gabriel_Rossetti_-_Beata_Beatrix%2C_1864-1870.jpg/500px-Dante_Gabriel_Rossetti_-_Beata_Beatrix%2C_1864-1870.jpg`.

### 335. dante-gabriel-rossetti / Proserpine

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `dante-gabriel-rossetti` → `Proserpine`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Dante_Gabriel_Rossetti_-_Proserpine_-_Google_Art_Project.jpg/500px-Dante_Gabriel_Rossetti_-_Proserpine_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Proserpine_(Rossetti)`.
- Normalized gallery asset: `Dante Gabriel Rossetti - Proserpine - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/dante-gabriel-rossetti`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 336. dante-gabriel-rossetti / The Blessed Damozel

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `dante-gabriel-rossetti` → `The Blessed Damozel`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Dante_Gabriel_Rossetti_The_Blessed_Damozel.jpg/500px-Dante_Gabriel_Rossetti_The_Blessed_Damozel.jpg`; page: `https://en.wikipedia.org/wiki/The_Blessed_Damozel`.
- Normalized gallery asset: `Dante Gabriel Rossetti The Blessed Damozel.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/dante-gabriel-rossetti`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 337. gustave-moreau / The Apparition

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `gustave-moreau` → `The Apparition`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Gustave_Moreau_A_apari%C3%A7%C3%A3o.jpg/500px-Gustave_Moreau_A_apari%C3%A7%C3%A3o.jpg`; page: `https://en.wikipedia.org/wiki/The_Apparition_(Moreau%2C_Mus%C3%A9e_national_Gustave_Moreau)`.
- Normalized gallery asset: `Gustave Moreau A aparição.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/gustave-moreau`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 338. gustave-moreau / Oedipus and the Sphinx

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `gustave-moreau` → `Oedipus and the Sphinx`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Gustave_Moreau_-_Oedipus_and_the_Sphinx_-_WGA16201.jpg/500px-Gustave_Moreau_-_Oedipus_and_the_Sphinx_-_WGA16201.jpg`; page: `https://commons.wikimedia.org/wiki/File:Gustave_Moreau_-_Oedipus_and_the_Sphinx_-_WGA16201.jpg`.
- Normalized gallery asset: `Gustave Moreau - Oedipus and the Sphinx - WGA16201.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/gustave-moreau`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 339. gustave-moreau / Jupiter and Semele

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `gustave-moreau` → `Jupiter and Semele`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Jupiter_and_Semele_by_Gustave_Moreau.jpg/500px-Jupiter_and_Semele_by_Gustave_Moreau.jpg`; page: `https://en.wikipedia.org/wiki/Jupiter_and_Semele`.
- Normalized gallery asset: `Jupiter and Semele by Gustave Moreau.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/gustave-moreau`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 340. odilon-redon / The Cyclops

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `odilon-redon` → `The Cyclops`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Odilon_Redon_-_The_Cyclops%2C_c._1914.jpg/500px-Odilon_Redon_-_The_Cyclops%2C_c._1914.jpg`; page: `https://en.wikipedia.org/wiki/The_Cyclops_(Redon)`.
- Normalized gallery asset: `Odilon Redon - The Cyclops, c. 1914.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/odilon-redon`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 341. odilon-redon / Flower Clouds

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `odilon-redon` → `Flower Clouds`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Odilon_Redon_-_Flower_Clouds_-_Google_Art_Project.jpg/960px-Odilon_Redon_-_Flower_Clouds_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Odilon_Redon_-_Flower_Clouds_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Odilon Redon - Flower Clouds - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/odilon-redon`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 342. gustave-caillebotte / Paris Street; Rainy Day

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `gustave-caillebotte` → `Paris Street; Rainy Day`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Gustave_Caillebotte_-_Paris_Street%3B_Rainy_Day_-_Google_Art_Project.jpg/500px-Gustave_Caillebotte_-_Paris_Street%3B_Rainy_Day_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Paris_Street%3B_Rainy_Day`.
- Normalized gallery asset: `Gustave Caillebotte - Paris Street; Rainy Day - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/gustave-caillebotte`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 343. gustave-caillebotte / The Floor Scrapers

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `gustave-caillebotte` → `The Floor Scrapers`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Gustave_Caillebotte_-_The_Floor_Planers_-_Google_Art_Project.jpg/500px-Gustave_Caillebotte_-_The_Floor_Planers_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Les_raboteurs_de_parquet`.
- Normalized gallery asset: `Gustave Caillebotte - The Floor Planers - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/gustave-caillebotte`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 344. gustave-caillebotte / Man at His Window

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `gustave-caillebotte` → `Man at His Window`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Gustave_Caillebotte_-_Jeune_homme_%C3%A0_sa_fen%C3%AAtre_%28B_32%29.jpg/960px-Gustave_Caillebotte_-_Jeune_homme_%C3%A0_sa_fen%C3%AAtre_%28B_32%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Gustave_Caillebotte_-_Jeune_homme_%C3%A0_sa_fen%C3%AAtre_(B_32).jpg`.
- Normalized gallery asset: `Gustave Caillebotte - Jeune homme à sa fenêtre (B 32).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `young-man-at-his-window`; title `Young Man at His Window`; worksKey `Man at His Window`; artistId `gustave-caillebotte`. Evidence: same Commons asset `Gustave Caillebotte - Jeune homme à sa fenêtre (B 32).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Gustave_Caillebotte_-_Jeune_homme_%C3%A0_sa_fen%C3%AAtre_%28B_32%29.jpg/960px-Gustave_Caillebotte_-_Jeune_homme_%C3%A0_sa_fen%C3%AAtre_%28B_32%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Gustave_Caillebotte_-_Jeune_homme_%C3%A0_sa_fen%C3%AAtre_(B_32).jpg`.
- Checked-in route `p/artwork/young-man-at-his-window.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Gustave_Caillebotte_-_Jeune_homme_%C3%A0_sa_fen%C3%AAtre_%28B_32%29.jpg/960px-Gustave_Caillebotte_-_Jeune_homme_%C3%A0_sa_fen%C3%AAtre_%28B_32%29.jpg`.

### 345. paul-signac / The Port of Saint-Tropez

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `paul-signac` → `The Port of Saint-Tropez`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Paul_Signac_-_The_Port_of_Saint-Tropez_-_Google_Art_Project.jpg/960px-Paul_Signac_-_The_Port_of_Saint-Tropez_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Paul_Signac_-_The_Port_of_Saint-Tropez_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Paul Signac - The Port of Saint-Tropez - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/paul-signac`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 346. paul-signac / In the Time of Harmony

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `paul-signac` → `In the Time of Harmony`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Paul_Signac%2C_1893-95%2C_Au_temps_d%E2%80%99harmonie%2C_oil_on_canvas%2C_310_x_410_cm.jpg/500px-Paul_Signac%2C_1893-95%2C_Au_temps_d%E2%80%99harmonie%2C_oil_on_canvas%2C_310_x_410_cm.jpg`; page: `https://en.wikipedia.org/wiki/In_the_Time_of_Harmony`.
- Normalized gallery asset: `Paul Signac, 1893-95, Au temps d’harmonie, oil on canvas, 310 x 410 cm.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/paul-signac`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 347. paul-signac / The Papal Palace, Avignon

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `paul-signac` → `The Papal Palace, Avignon`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Paul_Signac_-_Avignon._Soir_%28le_ch%C3%A2teau_des_Papes%29_-_1909.jpg/960px-Paul_Signac_-_Avignon._Soir_%28le_ch%C3%A2teau_des_Papes%29_-_1909.jpg`; page: `https://commons.wikimedia.org/wiki/File:Paul_Signac_-_Avignon._Soir_(le_ch%C3%A2teau_des_Papes)_-_1909.jpg`.
- Normalized gallery asset: `Paul Signac - Avignon. Soir (le château des Papes) - 1909.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-7.js` / `the-papal-palace-avignon`; title `The Papal Palace, Avignon`; worksKey `(absent)`; artistId `paul-signac`. Evidence: same Commons asset `Paul Signac - Avignon. Soir (le château des Papes) - 1909.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Paul_Signac_-_Avignon._Soir_%28le_ch%C3%A2teau_des_Papes%29_-_1909.jpg/960px-Paul_Signac_-_Avignon._Soir_%28le_ch%C3%A2teau_des_Papes%29_-_1909.jpg`; page: `https://commons.wikimedia.org/wiki/File:Paul_Signac_-_Avignon._Soir_(le_ch%C3%A2teau_des_Papes)_-_1909.jpg`.
- Checked-in route `p/artwork/the-papal-palace-avignon.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Paul_Signac_-_Avignon._Soir_%28le_ch%C3%A2teau_des_Papes%29_-_1909.jpg/960px-Paul_Signac_-_Avignon._Soir_%28le_ch%C3%A2teau_des_Papes%29_-_1909.jpg`.

### 348. pierre-bonnard / Nude in the Bath

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `pierre-bonnard` → `Nude in the Bath`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Pierre_Bonnard_-_Nu_dans_le_bain.jpg/960px-Pierre_Bonnard_-_Nu_dans_le_bain.jpg`; page: `https://commons.wikimedia.org/wiki/File:Pierre_Bonnard_-_Nu_dans_le_bain.jpg`.
- Normalized gallery asset: `Pierre Bonnard - Nu dans le bain.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/pierre-bonnard`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 349. pierre-bonnard / The Open Window

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `pierre-bonnard` → `The Open Window`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/The-open-window-1921.jpg%21HalfHD.jpg/500px-The-open-window-1921.jpg%21HalfHD.jpg`; page: `https://en.wikipedia.org/wiki/The_Open_Window_(Bonnard)`.
- Normalized gallery asset: `The-open-window-1921.jpg!HalfHD.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/pierre-bonnard`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 350. pierre-bonnard / Dining Room in the Country

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `pierre-bonnard` → `Dining Room in the Country`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Bonnardsala.jpg/500px-Bonnardsala.jpg`; page: `https://commons.wikimedia.org/wiki/File:Bonnardsala.jpg`.
- Normalized gallery asset: `Bonnardsala.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/pierre-bonnard`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 351. suzanne-valadon / The Blue Room

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `suzanne-valadon` → `The Blue Room`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/%28Barcelona%29_La_chambre_bleue_-_Suzanne_Valadon.jpg/500px-%28Barcelona%29_La_chambre_bleue_-_Suzanne_Valadon.jpg`; page: `https://en.wikipedia.org/wiki/The_Blue_Room_(Valadon)`.
- Normalized gallery asset: `(Barcelona) La chambre bleue - Suzanne Valadon.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/suzanne-valadon`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 352. suzanne-valadon / Adam and Eve

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `suzanne-valadon` → `Adam and Eve`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/%28Barcelona%29_L%27%C3%A9t%C3%A9_ou_Adam_et_Eve_-_Suzanne_Valadon_-_Mus%C3%A9e_national_d%27Art_moderne_Paris.jpg/500px-%28Barcelona%29_L%27%C3%A9t%C3%A9_ou_Adam_et_Eve_-_Suzanne_Valadon_-_Mus%C3%A9e_national_d%27Art_moderne_Paris.jpg`; page: `https://en.wikipedia.org/wiki/Adam_and_Eve_(Valadon)`.
- Normalized gallery asset: `(Barcelona) L'été ou Adam et Eve - Suzanne Valadon - Musée national d'Art moderne Paris.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/suzanne-valadon`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 353. suzanne-valadon / Self-Portrait

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `suzanne-valadon` → `Self-Portrait`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/%28Barcelona%29_Autoretrat_al_mirall_-_by_Suzanne_Valadon.jpg/500px-%28Barcelona%29_Autoretrat_al_mirall_-_by_Suzanne_Valadon.jpg`; page: `https://commons.wikimedia.org/wiki/File:(Barcelona)_Autoretrat_al_mirall_-_by_Suzanne_Valadon.jpg`.
- Normalized gallery asset: `(Barcelona) Autoretrat al mirall - by Suzanne Valadon.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/suzanne-valadon`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 354. joaquin-sorolla / Walk on the Beach

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `joaquin-sorolla` → `Walk on the Beach`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Joaqu%C3%ADn_Sorolla_y_Bastida_-_Strolling_along_the_Seashore_-_Google_Art_Project.jpg/500px-Joaqu%C3%ADn_Sorolla_y_Bastida_-_Strolling_along_the_Seashore_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Walk_on_the_Beach`.
- Normalized gallery asset: `Joaquín Sorolla y Bastida - Strolling along the Seashore - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/joaquin-sorolla`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 355. joaquin-sorolla / Sad Inheritance

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `joaquin-sorolla` → `Sad Inheritance`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Joaqu%C3%ADn_Sorolla_y_Bastida_-_Triste_Herencia_%281899%29.jpg/500px-Joaqu%C3%ADn_Sorolla_y_Bastida_-_Triste_Herencia_%281899%29.jpg`; page: `https://en.wikipedia.org/wiki/Sad_Inheritance!`.
- Normalized gallery asset: `Joaquín Sorolla y Bastida - Triste Herencia (1899).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/joaquin-sorolla`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 356. joaquin-sorolla / Vision of Spain: Catalonia

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `joaquin-sorolla` → `Vision of Spain: Catalonia`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Catalu%C3%B1a._El_pescado%2C_por_Joaqu%C3%ADn_Sorolla.jpg/500px-Catalu%C3%B1a._El_pescado%2C_por_Joaqu%C3%ADn_Sorolla.jpg`; page: `https://commons.wikimedia.org/wiki/File:Catalu%C3%B1a._El_pescado,_por_Joaqu%C3%ADn_Sorolla.jpg`.
- Normalized gallery asset: `Cataluña. El pescado, por Joaquín Sorolla.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/joaquin-sorolla`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 357. vilhelm-hammershoi / Dust Motes Dancing in the Sunbeams

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `vilhelm-hammershoi` → `Dust Motes Dancing in the Sunbeams`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Hammersh%C3%B8i_Dust_motes_dancing.jpg/960px-Hammersh%C3%B8i_Dust_motes_dancing.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hammersh%C3%B8i_Dust_motes_dancing.jpg`.
- Normalized gallery asset: `Hammershøi Dust motes dancing.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/vilhelm-hammershoi`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 358. vilhelm-hammershoi / Interior, Strandgade 30

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `vilhelm-hammershoi` → `Interior, Strandgade 30`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Vilhelm_Hammersh%C3%B8i%2C_Interi%C3%B8r_fra_Strandgade_30%2C_1900.jpg/960px-Vilhelm_Hammersh%C3%B8i%2C_Interi%C3%B8r_fra_Strandgade_30%2C_1900.jpg`; page: `https://commons.wikimedia.org/wiki/File:Vilhelm_Hammersh%C3%B8i,_Interi%C3%B8r_fra_Strandgade_30,_1900.jpg`.
- Normalized gallery asset: `Vilhelm Hammershøi, Interiør fra Strandgade 30, 1900.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/vilhelm-hammershoi`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 359. akseli-gallen-kallela / The Defense of the Sampo

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `akseli-gallen-kallela` → `The Defense of the Sampo`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Gallen-Kallela_The_defence_of_the_Sampo.png/500px-Gallen-Kallela_The_defence_of_the_Sampo.png`; page: `https://commons.wikimedia.org/wiki/File:Gallen-Kallela_The_defence_of_the_Sampo.png`.
- Normalized gallery asset: `Gallen-Kallela The defence of the Sampo.png`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/akseli-gallen-kallela`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 360. akseli-gallen-kallela / Lemminkäinen's Mother

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `akseli-gallen-kallela` → `Lemminkäinen's Mother`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Gallen_Kallela_Lemminkainens_Mother.jpg/500px-Gallen_Kallela_Lemminkainens_Mother.jpg`; page: `https://en.wikipedia.org/wiki/Lemmink%C3%A4inen's_Mother`.
- Normalized gallery asset: `Gallen Kallela Lemminkainens Mother.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `lemminkainens-mother`; title `Lemminkäinen's Mother`; worksKey `(absent)`; artistId `akseli-gallen-kallela`. Evidence: same Commons asset `Gallen Kallela Lemminkainens Mother.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Gallen_Kallela_Lemminkainens_Mother.jpg/500px-Gallen_Kallela_Lemminkainens_Mother.jpg`; page: `https://commons.wikimedia.org/wiki/File:Gallen_Kallela_Lemminkainens_Mother.jpg`.
- Checked-in route `p/artwork/lemminkainens-mother.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Gallen_Kallela_Lemminkainens_Mother.jpg/500px-Gallen_Kallela_Lemminkainens_Mother.jpg`.

### 361. akseli-gallen-kallela / The Aino Myth, Triptych

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `akseli-gallen-kallela` → `The Aino Myth, Triptych`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Akseli_Gallen-Kallela_-_Aino_Myth%2C_Triptych_-_Google_Art_Project.jpg/960px-Akseli_Gallen-Kallela_-_Aino_Myth%2C_Triptych_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Akseli_Gallen-Kallela_-_Aino_Myth,_Triptych_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Akseli Gallen-Kallela - Aino Myth, Triptych - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/akseli-gallen-kallela`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 362. jan-matejko / The Battle of Grunwald

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jan-matejko` → `The Battle of Grunwald`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jan_Matejko%2C_Bitwa_pod_Grunwaldem.jpg/960px-Jan_Matejko%2C_Bitwa_pod_Grunwaldem.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jan_Matejko,_Bitwa_pod_Grunwaldem.jpg`.
- Normalized gallery asset: `Jan Matejko, Bitwa pod Grunwaldem.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jan-matejko`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 363. jan-matejko / Stańczyk

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jan-matejko` → `Stańczyk`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Jan_Matejko%2C_Sta%C5%84czyk.jpg/500px-Jan_Matejko%2C_Sta%C5%84czyk.jpg`; page: `https://en.wikipedia.org/wiki/Sta%C5%84czyk_(painting)`.
- Normalized gallery asset: `Jan Matejko, Stańczyk.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `stanczyk`; title `Stańczyk`; worksKey `(absent)`; artistId `jan-matejko`. Evidence: same Commons asset `Jan Matejko, Stańczyk.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Jan_Matejko%2C_Sta%C5%84czyk.jpg/500px-Jan_Matejko%2C_Sta%C5%84czyk.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jan_Matejko,_Sta%C5%84czyk.jpg`.
- Checked-in route `p/artwork/stanczyk.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Jan_Matejko%2C_Sta%C5%84czyk.jpg/500px-Jan_Matejko%2C_Sta%C5%84czyk.jpg`.

### 364. jan-matejko / Prussian Homage

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jan-matejko` → `Prussian Homage`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Prussian_Homage.jpg/500px-Prussian_Homage.jpg`; page: `https://en.wikipedia.org/wiki/Prussian_Homage_(painting)`.
- Normalized gallery asset: `Prussian Homage.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jan-matejko`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 365. jacek-malczewski / Melancholia

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jacek-malczewski` → `Melancholia`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Malczewski_melancholia.jpg/960px-Malczewski_melancholia.jpg`; page: `https://commons.wikimedia.org/wiki/File:Malczewski_melancholia.jpg`.
- Normalized gallery asset: `Malczewski melancholia.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jacek-malczewski`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 366. jacek-malczewski / The Vicious Circle

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jacek-malczewski` → `The Vicious Circle`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Bledne_kolo.jpg/960px-Bledne_kolo.jpg`; page: `https://commons.wikimedia.org/wiki/File:Bledne_kolo.jpg`.
- Normalized gallery asset: `Bledne kolo.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jacek-malczewski`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 367. jacek-malczewski / Thanatos

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jacek-malczewski` → `Thanatos`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Jacek_Maleczewski-Thanatos_II-1899.jpg/960px-Jacek_Maleczewski-Thanatos_II-1899.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jacek_Maleczewski-Thanatos_II-1899.jpg`.
- Normalized gallery asset: `Jacek Maleczewski-Thanatos II-1899.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jacek-malczewski`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 368. olga-boznanska / Girl with Chrysanthemums

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `olga-boznanska` → `Girl with Chrysanthemums`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Olga_Bozna%C5%84ska_-_Girl_with_Chrysanthemums_-_MNK_II-b-1032_-_National_Museum_Krak%C3%B3w.jpg/500px-Olga_Bozna%C5%84ska_-_Girl_with_Chrysanthemums_-_MNK_II-b-1032_-_National_Museum_Krak%C3%B3w.jpg`; page: `https://en.wikipedia.org/wiki/Girl_with_Chrysanthemums`.
- Normalized gallery asset: `Olga Boznańska - Girl with Chrysanthemums - MNK II-b-1032 - National Museum Kraków.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/olga-boznanska`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 369. olga-boznanska / Self-Portrait

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `olga-boznanska` → `Self-Portrait`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Olga_Bozna%C5%84ska_-_Autoportret.jpg/500px-Olga_Bozna%C5%84ska_-_Autoportret.jpg`; page: `https://commons.wikimedia.org/wiki/File:Olga_Bozna%C5%84ska_-_Autoportret.jpg`.
- Normalized gallery asset: `Olga Boznańska - Autoportret.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/olga-boznanska`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 370. olga-boznanska / Portrait of Paul Nauen

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `olga-boznanska` → `Portrait of Paul Nauen`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Olga_Bozna%C5%84ska_-_Portrait_of_Paul_Nauen_-_MNK_II-b-7_-_National_Museum_Krak%C3%B3w.jpg/960px-Olga_Bozna%C5%84ska_-_Portrait_of_Paul_Nauen_-_MNK_II-b-7_-_National_Museum_Krak%C3%B3w.jpg`; page: `https://commons.wikimedia.org/wiki/File:Olga_Bozna%C5%84ska_-_Portrait_of_Paul_Nauen_-_MNK_II-b-7_-_National_Museum_Krak%C3%B3w.jpg`.
- Normalized gallery asset: `Olga Boznańska - Portrait of Paul Nauen - MNK II-b-7 - National Museum Kraków.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/olga-boznanska`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 371. stanislaw-wyspianski / God the Father — Become! (stained glass)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `stanislaw-wyspianski` → `God the Father — Become! (stained glass)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Stanis%C5%82aw_Wyspia%C5%84ski_-_God_the_Father_%E2%80%93_Design_to_the_Stained-Glass_Window_for_the_Franciscan_Church_in_Krakow_-_MNK_II-b-514_-_National_Museum_Krak%C3%B3w.jpg/960px-Stanis%C5%82aw_Wyspia%C5%84ski_-_God_the_Father_%E2%80%93_Design_to_the_Stained-Glass_Window_for_the_Franciscan_Church_in_Krakow_-_MNK_II-b-514_-_National_Museum_Krak%C3%B3w.jpg`; page: `https://commons.wikimedia.org/wiki/File:Stanis%C5%82aw_Wyspia%C5%84ski_-_God_the_Father_%E2%80%93_Design_to_the_Stained-Glass_Window_for_the_Franciscan_Church_in_Krakow_-_MNK_II-b-514_-_National_Museum_Krak%C3%B3w.jpg`.
- Normalized gallery asset: `Stanisław Wyspiański - God the Father – Design to the Stained-Glass Window for the Franciscan Church in Krakow - MNK II-b-514 - National Museum Kraków.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/stanislaw-wyspianski`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 372. stanislaw-wyspianski / Motherhood

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `stanislaw-wyspianski` → `Motherhood`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Stanis%C5%82aw_Wyspia%C5%84ski%2C_Macierzy%C5%84stwo.jpg/500px-Stanis%C5%82aw_Wyspia%C5%84ski%2C_Macierzy%C5%84stwo.jpg`; page: `https://commons.wikimedia.org/wiki/File:Stanis%C5%82aw_Wyspia%C5%84ski,_Macierzy%C5%84stwo.jpg`.
- Normalized gallery asset: `Stanisław Wyspiański, Macierzyństwo.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-9.js` / `motherhood-wyspianski`; title `Motherhood`; worksKey `Motherhood`; artistId `stanislaw-wyspianski`. Evidence: same Commons asset `Stanisław Wyspiański, Macierzyństwo.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Stanis%C5%82aw_Wyspia%C5%84ski%2C_Macierzy%C5%84stwo.jpg/500px-Stanis%C5%82aw_Wyspia%C5%84ski%2C_Macierzy%C5%84stwo.jpg`; page: `https://commons.wikimedia.org/wiki/File:Stanis%C5%82aw_Wyspia%C5%84ski,_Macierzy%C5%84stwo.jpg`.
- Checked-in route `p/artwork/motherhood-wyspianski.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Stanis%C5%82aw_Wyspia%C5%84ski%2C_Macierzy%C5%84stwo.jpg/500px-Stanis%C5%82aw_Wyspia%C5%84ski%2C_Macierzy%C5%84stwo.jpg`.

### 373. stanislaw-wyspianski / Self-Portrait

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `stanislaw-wyspianski` → `Self-Portrait`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Stanis%C5%82aw_Wyspia%C5%84ski%2C_Autoportret.jpg/500px-Stanis%C5%82aw_Wyspia%C5%84ski%2C_Autoportret.jpg`; page: `https://commons.wikimedia.org/wiki/File:Stanis%C5%82aw_Wyspia%C5%84ski,_Autoportret.jpg`.
- Normalized gallery asset: `Stanisław Wyspiański, Autoportret.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/stanislaw-wyspianski`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 374. witkacy / Composition with a Self-Portrait

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `witkacy` → `Composition with a Self-Portrait`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Witkacy_-_Autoportret_Inc._Zado%C5%9B%C4%87_uczyni_tylko_zupe%C5%82n.jpg/960px-Witkacy_-_Autoportret_Inc._Zado%C5%9B%C4%87_uczyni_tylko_zupe%C5%82n.jpg`; page: `https://commons.wikimedia.org/wiki/File:Witkacy_-_Autoportret_Inc._Zado%C5%9B%C4%87_uczyni_tylko_zupe%C5%82n.jpg`.
- Normalized gallery asset: `Witkacy - Autoportret Inc. Zadość uczyni tylko zupełn.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/witkacy`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 375. witkacy / Portrait of Nena Stachurska

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `witkacy` → `Portrait of Nena Stachurska`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Witkacy_-_Nena_Stachurska_-_1929-05_-_KDM_I_975.jpg/960px-Witkacy_-_Nena_Stachurska_-_1929-05_-_KDM_I_975.jpg`; page: `https://commons.wikimedia.org/wiki/File:Witkacy_-_Nena_Stachurska_-_1929-05_-_KDM_I_975.jpg`.
- Normalized gallery asset: `Witkacy - Nena Stachurska - 1929-05 - KDM I 975.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/witkacy`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 376. witkacy / Fantasy — Fairy Tale

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `witkacy` → `Fantasy — Fairy Tale`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Witkiewicz-Fantazja-Bajka.jpg/960px-Witkiewicz-Fantazja-Bajka.jpg`; page: `https://commons.wikimedia.org/wiki/File:Witkiewicz-Fantazja-Bajka.jpg`.
- Normalized gallery asset: `Witkiewicz-Fantazja-Bajka.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/witkacy`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 377. seker-ahmed-pasha / Self-Portrait

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `seker-ahmed-pasha` → `Self-Portrait`; img: `https://upload.wikimedia.org/wikipedia/commons/2/22/Seker_ahmet_pasa.jpg`; page: `https://commons.wikimedia.org/wiki/File:Seker_ahmet_pasa.jpg`.
- Normalized gallery asset: `Seker ahmet pasa.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/seker-ahmed-pasha`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 378. seker-ahmed-pasha / Still Life with Fruit

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `seker-ahmed-pasha` → `Still Life with Fruit`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Ahmed-Fruit.jpg/500px-Ahmed-Fruit.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ahmed-Fruit.jpg`.
- Normalized gallery asset: `Ahmed-Fruit.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/seker-ahmed-pasha`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 379. seker-ahmed-pasha / Forest (Woodland Scene)

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `seker-ahmed-pasha` → `Forest (Woodland Scene)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Ahmed-Forest.jpg/500px-Ahmed-Forest.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ahmed-Forest.jpg`.
- Normalized gallery asset: `Ahmed-Forest.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-9.js` / `the-forest-seker-ahmed`; title `The Forest`; worksKey `Forest (Woodland Scene)`; artistId `seker-ahmed-pasha`. Evidence: same Commons asset `Ahmed-Forest.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Ahmed-Forest.jpg/500px-Ahmed-Forest.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ahmed-Forest.jpg`.
- Checked-in route `p/artwork/the-forest-seker-ahmed.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Ahmed-Forest.jpg/500px-Ahmed-Forest.jpg`.

### 380. osman-hamdi-bey / The Tortoise Trainer

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `osman-hamdi-bey` → `The Tortoise Trainer`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg/500px-Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Tortoise_Trainer`.
- Normalized gallery asset: `Osman Hamdi Bey - The Tortoise Trainer - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `the-tortoise-trainer`; title `The Tortoise Trainer`; worksKey `(absent)`; artistId `osman-hamdi-bey`. Evidence: same Commons asset `Osman Hamdi Bey - The Tortoise Trainer - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg/500px-Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/the-tortoise-trainer.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg/500px-Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg`.

### 381. osman-hamdi-bey / Girl Reciting the Qur'an

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `osman-hamdi-bey` → `Girl Reciting the Qur'an`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Young_woman_reading_%281880%29%2C_by_Osman_Hamdi_Bey.jpg/960px-Young_woman_reading_%281880%29%2C_by_Osman_Hamdi_Bey.jpg`; page: `https://commons.wikimedia.org/wiki/File:Young_woman_reading_(1880),_by_Osman_Hamdi_Bey.jpg`.
- Normalized gallery asset: `Young woman reading (1880), by Osman Hamdi Bey.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/osman-hamdi-bey`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 382. osman-hamdi-bey / Two Musician Girls

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `osman-hamdi-bey` → `Two Musician Girls`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Osman_Hamdi_Bey_-_Two_Musician_Girls_-_Google_Art_Project.jpg/960px-Osman_Hamdi_Bey_-_Two_Musician_Girls_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Osman_Hamdi_Bey_-_Two_Musician_Girls_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Osman Hamdi Bey - Two Musician Girls - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/osman-hamdi-bey`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 383. mihri-musfik / Portrait of a Woman

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `mihri-musfik` → `Portrait of a Woman`; img: `https://upload.wikimedia.org/wikipedia/commons/5/5f/Painting_by_Mihri_M%C3%BC%C5%9Ffik.jpg`; page: `https://commons.wikimedia.org/wiki/File:Painting_by_Mihri_M%C3%BC%C5%9Ffik.jpg`.
- Normalized gallery asset: `Painting by Mihri Müşfik.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/mihri-musfik`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 384. mihri-musfik / Portrait of Mustafa Kemal Atatürk

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `mihri-musfik` → `Portrait of Mustafa Kemal Atatürk`; img: `https://upload.wikimedia.org/wikipedia/commons/1/1a/Atarturk_-_Mihri_M%C3%BC%C5%9Ffik_Han%C4%B1m.jpg`; page: `https://commons.wikimedia.org/wiki/File:Atarturk_-_Mihri_M%C3%BC%C5%9Ffik_Han%C4%B1m.jpg`.
- Normalized gallery asset: `Atarturk - Mihri Müşfik Hanım.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/mihri-musfik`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 385. kathe-kollwitz / The Weavers cycle

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kathe-kollwitz` → `The Weavers cycle`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Death_-_Sheet-2-from-the-cycle-A-Weavers-Revolt-by-Kathe-Kollwitz.jpg/960px-Death_-_Sheet-2-from-the-cycle-A-Weavers-Revolt-by-Kathe-Kollwitz.jpg`; page: `https://commons.wikimedia.org/wiki/File:Death_-_Sheet-2-from-the-cycle-A-Weavers-Revolt-by-Kathe-Kollwitz.jpg`.
- Normalized gallery asset: `Death - Sheet-2-from-the-cycle-A-Weavers-Revolt-by-Kathe-Kollwitz.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kathe-kollwitz`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 386. kathe-kollwitz / Woman with Dead Child

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kathe-kollwitz` → `Woman with Dead Child`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Kollwitz.jpg/500px-Kollwitz.jpg`; page: `https://en.wikipedia.org/wiki/Woman_with_Dead_Child`.
- Normalized gallery asset: `Kollwitz.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kathe-kollwitz`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 387. kathe-kollwitz / The Grieving Parents

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kathe-kollwitz` → `The Grieving Parents`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Grieving_parents_%2816127037905%29.jpg/500px-Grieving_parents_%2816127037905%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Grieving_parents_(16127037905).jpg`.
- Normalized gallery asset: `Grieving parents (16127037905).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kathe-kollwitz`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 388. franz-marc / Blue Horse I

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `franz-marc` → `Blue Horse I`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Marc%2C_Franz_-_Blue_Horse_I_-_Google_Art_Project.jpg/500px-Marc%2C_Franz_-_Blue_Horse_I_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Blue_Horse_I`.
- Normalized gallery asset: `Marc, Franz - Blue Horse I - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/franz-marc`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 389. franz-marc / The Fate of the Animals

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `franz-marc` → `The Fate of the Animals`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Franz_Marc-The_fate_of_the_animals-1913.jpg/500px-Franz_Marc-The_fate_of_the_animals-1913.jpg`; page: `https://en.wikipedia.org/wiki/Fate_of_the_Animals`.
- Normalized gallery asset: `Franz Marc-The fate of the animals-1913.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-6.js` / `the-fate-of-the-animals`; title `The Fate of the Animals`; worksKey `(absent)`; artistId `franz-marc`. Evidence: same Commons asset `Franz Marc-The fate of the animals-1913.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Franz_Marc-The_fate_of_the_animals-1913.jpg/500px-Franz_Marc-The_fate_of_the_animals-1913.jpg`; page: `https://commons.wikimedia.org/wiki/File:Franz_Marc-The_fate_of_the_animals-1913.jpg`.
- Checked-in route `p/artwork/the-fate-of-the-animals.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Franz_Marc-The_fate_of_the_animals-1913.jpg/500px-Franz_Marc-The_fate_of_the_animals-1913.jpg`.

### 390. franz-marc / The Tower of Blue Horses

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `franz-marc` → `The Tower of Blue Horses`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Franz_Marc_029a.jpg/500px-Franz_Marc_029a.jpg`; page: `https://en.wikipedia.org/wiki/The_Tower_of_Blue_Horses`.
- Normalized gallery asset: `Franz Marc 029a.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/franz-marc`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 391. fernand-leger / The City

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `fernand-leger` → `The City`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Fernand_L%C3%A9ger%2C_1919%2C_The_City_%28La_Ville%29%2C_oil_on_canvas%2C_231.1_x_298.4_cm%2C_Philadelphia_Museum_of_Art.jpg/500px-Fernand_L%C3%A9ger%2C_1919%2C_The_City_%28La_Ville%29%2C_oil_on_canvas%2C_231.1_x_298.4_cm%2C_Philadelphia_Museum_of_Art.jpg`; page: `https://en.wikipedia.org/wiki/The_City_(L%C3%A9ger)`.
- Normalized gallery asset: `Fernand Léger, 1919, The City (La Ville), oil on canvas, 231.1 x 298.4 cm, Philadelphia Museum of Art.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-8.js` / `the-city-leger`; title `The City`; worksKey `The City`; artistId `fernand-leger`. Evidence: same Commons asset `Fernand Léger, 1919, The City (La Ville), oil on canvas, 231.1 x 298.4 cm, Philadelphia Museum of Art.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Fernand_L%C3%A9ger%2C_1919%2C_The_City_%28La_Ville%29%2C_oil_on_canvas%2C_231.1_x_298.4_cm%2C_Philadelphia_Museum_of_Art.jpg/500px-Fernand_L%C3%A9ger%2C_1919%2C_The_City_%28La_Ville%29%2C_oil_on_canvas%2C_231.1_x_298.4_cm%2C_Philadelphia_Museum_of_Art.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fernand_L%C3%A9ger,_1919,_The_City_(La_Ville),_oil_on_canvas,_231.1_x_298.4_cm,_Philadelphia_Museum_of_Art.jpg`.
- Checked-in route `p/artwork/the-city-leger.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Fernand_L%C3%A9ger%2C_1919%2C_The_City_%28La_Ville%29%2C_oil_on_canvas%2C_231.1_x_298.4_cm%2C_Philadelphia_Museum_of_Art.jpg/500px-Fernand_L%C3%A9ger%2C_1919%2C_The_City_%28La_Ville%29%2C_oil_on_canvas%2C_231.1_x_298.4_cm%2C_Philadelphia_Museum_of_Art.jpg`.

### 392. fernand-leger / Three Women (Le Grand Déjeuner)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `fernand-leger` → `Three Women (Le Grand Déjeuner)`; img: `https://upload.wikimedia.org/wikipedia/commons/9/9d/Three_Women%2C_1919_-_Fernand_L%C3%A9ger.jpg`; page: `https://commons.wikimedia.org/wiki/File:Three_Women,_1919_-_Fernand_L%C3%A9ger.jpg`.
- Normalized gallery asset: `Three Women, 1919 - Fernand Léger.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/fernand-leger`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 393. fernand-leger / The Builders

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `fernand-leger` → `The Builders`; img: `https://upload.wikimedia.org/wikipedia/commons/9/9b/The_Builders_-_Fernand_L%C3%A9ger.png`; page: `https://commons.wikimedia.org/wiki/File:The_Builders_-_Fernand_L%C3%A9ger.png`.
- Normalized gallery asset: `The Builders - Fernand Léger.png`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/fernand-leger`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 394. max-beckmann / Departure

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `max-beckmann` → `Departure`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Max_Beckmann%2C_Departure.jpg/500px-Max_Beckmann%2C_Departure.jpg`; page: `https://en.wikipedia.org/wiki/Departure_(Beckmann)`.
- Normalized gallery asset: `Max Beckmann, Departure.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/max-beckmann`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 395. max-beckmann / Self-Portrait in Tuxedo

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `max-beckmann` → `Self-Portrait in Tuxedo`; img: `https://upload.wikimedia.org/wikipedia/commons/8/88/Self-Portrait_in_Tuxedo.jpg`; page: `https://commons.wikimedia.org/wiki/File:Self-Portrait_in_Tuxedo.jpg`.
- Normalized gallery asset: `Self-Portrait in Tuxedo.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/max-beckmann`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 396. max-beckmann / The Night

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `max-beckmann` → `The Night`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Max_Beckmann%2C_1918-19%2C_The_Night_%28Die_Nacht%29%2C_oil_on_canvas%2C_133_x_154_cm%2C_Kunstsammlung_Nordrhein-Westfalen%2C_D%C3%BCsseldorf.jpg/500px-Max_Beckmann%2C_1918-19%2C_The_Night_%28Die_Nacht%29%2C_oil_on_canvas%2C_133_x_154_cm%2C_Kunstsammlung_Nordrhein-Westfalen%2C_D%C3%BCsseldorf.jpg`; page: `https://en.wikipedia.org/wiki/The_Night_(Beckmann)`.
- Normalized gallery asset: `Max Beckmann, 1918-19, The Night (Die Nacht), oil on canvas, 133 x 154 cm, Kunstsammlung Nordrhein-Westfalen, Düsseldorf.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/max-beckmann`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 397. kurt-schwitters / Merzbild 1A (The Psychiatrist)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kurt-schwitters` → `Merzbild 1A (The Psychiatrist)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Merzbild_1A_%28The_Psychiatrist%29_%281919%29.jpg/500px-Merzbild_1A_%28The_Psychiatrist%29_%281919%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Merzbild_1A_(The_Psychiatrist)_(1919).jpg`.
- Normalized gallery asset: `Merzbild 1A (The Psychiatrist) (1919).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kurt-schwitters`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 398. kurt-schwitters / The Merzbau

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kurt-schwitters` → `The Merzbau`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Hanover_Merzbau.jpg/500px-Hanover_Merzbau.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hanover_Merzbau.jpg`.
- Normalized gallery asset: `Hanover Merzbau.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kurt-schwitters`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 399. kurt-schwitters / Das Undbild

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kurt-schwitters` → `Das Undbild`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/DasUndbild.jpg/500px-DasUndbild.jpg`; page: `https://commons.wikimedia.org/wiki/File:DasUndbild.jpg`.
- Normalized gallery asset: `DasUndbild.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kurt-schwitters`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 400. grant-wood / American Gothic

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `grant-wood` → `American Gothic`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Grant_Wood_-_American_Gothic_-_Google_Art_Project.jpg/500px-Grant_Wood_-_American_Gothic_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/American_Gothic`.
- Normalized gallery asset: `Grant Wood - American Gothic - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/grant-wood`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 401. grant-wood / Stone City, Iowa

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `grant-wood` → `Stone City, Iowa`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Stone_City_Iowa_1930_Grant_Wood.jpg/500px-Stone_City_Iowa_1930_Grant_Wood.jpg`; page: `https://en.wikipedia.org/wiki/Stone_City%2C_Iowa_(painting)`.
- Normalized gallery asset: `Stone City Iowa 1930 Grant Wood.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/grant-wood`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 402. grant-wood / Daughters of Revolution

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `grant-wood` → `Daughters of Revolution`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Daughters_of_Revolution.jpg/500px-Daughters_of_Revolution.jpg`; page: `https://en.wikipedia.org/wiki/Daughters_of_Revolution`.
- Normalized gallery asset: `Daughters of Revolution.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/grant-wood`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 403. emily-carr / Forest, British Columbia

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `emily-carr` → `Forest, British Columbia`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Emily_Carr_%281931%E2%80%9332%29_Forest%2C_British_Columbia.jpg/500px-Emily_Carr_%281931%E2%80%9332%29_Forest%2C_British_Columbia.jpg`; page: `https://commons.wikimedia.org/wiki/File:Emily_Carr_(1931%E2%80%9332)_Forest,_British_Columbia.jpg`.
- Normalized gallery asset: `Emily Carr (1931–32) Forest, British Columbia.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-7.js` / `forest-british-columbia`; title `Forest, British Columbia`; worksKey `(absent)`; artistId `emily-carr`. Evidence: same Commons asset `Emily Carr (1931–32) Forest, British Columbia.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Emily_Carr_%281931%E2%80%9332%29_Forest%2C_British_Columbia.jpg/500px-Emily_Carr_%281931%E2%80%9332%29_Forest%2C_British_Columbia.jpg`; page: `https://commons.wikimedia.org/wiki/File:Emily_Carr_(1931%E2%80%9332)_Forest,_British_Columbia.jpg`.
- Checked-in route `p/artwork/forest-british-columbia.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Emily_Carr_%281931%E2%80%9332%29_Forest%2C_British_Columbia.jpg/500px-Emily_Carr_%281931%E2%80%9332%29_Forest%2C_British_Columbia.jpg`.

### 404. emily-carr / Indian Church

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `emily-carr` → `Indian Church`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Emily_Carr_Indian_Church.jpg/500px-Emily_Carr_Indian_Church.jpg`; page: `https://en.wikipedia.org/wiki/The_Indian_Church_(painting)`.
- Normalized gallery asset: `Emily Carr Indian Church.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/emily-carr`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 405. emily-carr / Above the Gravel Pit

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `emily-carr` → `Above the Gravel Pit`; img: `https://upload.wikimedia.org/wikipedia/commons/1/14/Above_the_Gravel_Pit_by_Emily_Carr%2C_1937%2C_oil_on_canvas.jpg`; page: `https://commons.wikimedia.org/wiki/File:Above_the_Gravel_Pit_by_Emily_Carr,_1937,_oil_on_canvas.jpg`.
- Normalized gallery asset: `Above the Gravel Pit by Emily Carr, 1937, oil on canvas.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/emily-carr`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 406. arshile-gorky / The Artist and His Mother

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `arshile-gorky` → `The Artist and His Mother`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Arshile_Gorky%2C_The_Artist_and_His_Mother.jpg/960px-Arshile_Gorky%2C_The_Artist_and_His_Mother.jpg`; page: `https://commons.wikimedia.org/wiki/File:Arshile_Gorky,_The_Artist_and_His_Mother.jpg`.
- Normalized gallery asset: `Arshile Gorky, The Artist and His Mother.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `the-artist-and-his-mother`; title `The Artist and His Mother`; worksKey `(absent)`; artistId `arshile-gorky`. Evidence: same Commons asset `Arshile Gorky, The Artist and His Mother.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Arshile_Gorky%2C_The_Artist_and_His_Mother.jpg/960px-Arshile_Gorky%2C_The_Artist_and_His_Mother.jpg`; page: `https://commons.wikimedia.org/wiki/File:Arshile_Gorky,_The_Artist_and_His_Mother.jpg`.
- Checked-in route `p/artwork/the-artist-and-his-mother.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Arshile_Gorky%2C_The_Artist_and_His_Mother.jpg/960px-Arshile_Gorky%2C_The_Artist_and_His_Mother.jpg`.

### 407. arshile-gorky / The Liver Is the Cock's Comb

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `arshile-gorky` → `The Liver Is the Cock's Comb`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/The_Liver_is_the_Cock%27s_Comb_y_Arshile_Gorky%2C_1944.jpg/500px-The_Liver_is_the_Cock%27s_Comb_y_Arshile_Gorky%2C_1944.jpg`; page: `https://en.wikipedia.org/wiki/The_Liver_Is_the_Cock's_Comb`.
- Normalized gallery asset: `The Liver is the Cock's Comb y Arshile Gorky, 1944.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/arshile-gorky`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 408. arshile-gorky / Agony

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `arshile-gorky` → `Agony`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/%22Agony%22_by_Arshile_Gorky.jpg/960px-%22Agony%22_by_Arshile_Gorky.jpg`; page: `https://commons.wikimedia.org/wiki/File:%22Agony%22_by_Arshile_Gorky.jpg`.
- Normalized gallery asset: `"Agony" by Arshile Gorky.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/arshile-gorky`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 409. jan-van-eyck / The Ghent Altarpiece (with Hubert van Eyck)

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jan-van-eyck` → `The Ghent Altarpiece (with Hubert van Eyck)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Jan_van_Eyck_The_Ghent_Altarpiece_-_Adoration_of_the_Lamb.jpg/500px-Jan_van_Eyck_The_Ghent_Altarpiece_-_Adoration_of_the_Lamb.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jan_van_Eyck_The_Ghent_Altarpiece_-_Adoration_of_the_Lamb.jpg`.
- Normalized gallery asset: `Jan van Eyck The Ghent Altarpiece - Adoration of the Lamb.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `ghent-altarpiece`; title `The Ghent Altarpiece`; worksKey `The Ghent Altarpiece (with Hubert van Eyck)`; artistId `jan-van-eyck`. Evidence: same Commons asset `Jan van Eyck The Ghent Altarpiece - Adoration of the Lamb.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Jan_van_Eyck_The_Ghent_Altarpiece_-_Adoration_of_the_Lamb.jpg/500px-Jan_van_Eyck_The_Ghent_Altarpiece_-_Adoration_of_the_Lamb.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jan_van_Eyck_The_Ghent_Altarpiece_-_Adoration_of_the_Lamb.jpg`.
- Checked-in route `p/artwork/ghent-altarpiece.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Jan_van_Eyck_The_Ghent_Altarpiece_-_Adoration_of_the_Lamb.jpg/500px-Jan_van_Eyck_The_Ghent_Altarpiece_-_Adoration_of_the_Lamb.jpg`.

### 410. jan-van-eyck / The Arnolfini Portrait

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jan-van-eyck` → `The Arnolfini Portrait`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Van_Eyck_-_Arnolfini_Portrait.jpg/500px-Van_Eyck_-_Arnolfini_Portrait.jpg`; page: `https://commons.wikimedia.org/wiki/File:Van_Eyck_-_Arnolfini_Portrait.jpg`.
- Normalized gallery asset: `Van Eyck - Arnolfini Portrait.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-arnolfini-portrait`; title `The Arnolfini Portrait`; worksKey `(absent)`; artistId `jan-van-eyck`. Evidence: same Commons asset `Van Eyck - Arnolfini Portrait.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Van_Eyck_-_Arnolfini_Portrait.jpg/500px-Van_Eyck_-_Arnolfini_Portrait.jpg`; page: `https://commons.wikimedia.org/wiki/File:Van_Eyck_-_Arnolfini_Portrait.jpg`.
- Checked-in route `p/artwork/the-arnolfini-portrait.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Van_Eyck_-_Arnolfini_Portrait.jpg/500px-Van_Eyck_-_Arnolfini_Portrait.jpg`.

### 411. jan-van-eyck / Man in a Red Turban

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jan-van-eyck` → `Man in a Red Turban`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Jan_van_Eyck_-_Portrait_of_a_Man_%28Self_Portrait%3F%29_1433.jpg/960px-Jan_van_Eyck_-_Portrait_of_a_Man_%28Self_Portrait%3F%29_1433.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jan_van_Eyck_-_Portrait_of_a_Man_%28Self_Portrait%3F%29_1433.jpg`.
- Normalized gallery asset: `Jan van Eyck - Portrait of a Man (Self Portrait?) 1433.jpg`.
- Gallery rendering: LATENT: arc replaces panel; no gallery status field.
- Catalog: `js/catalog-1.js` / `man-in-a-red-turban`; title `Portrait of a Man (Man in a Red Turban)`; worksKey `Man in a Red Turban`; artistId `jan-van-eyck`. Evidence: same Commons asset `Jan van Eyck - Portrait of a Man (Self Portrait?) 1433.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Jan_van_Eyck_-_Portrait_of_a_Man_%28Self_Portrait%3F%29_1433.jpg/960px-Jan_van_Eyck_-_Portrait_of_a_Man_%28Self_Portrait%3F%29_1433.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jan_van_Eyck_-_Portrait_of_a_Man_%28Self_Portrait%3F%29_1433.jpg`.
- Checked-in route `p/artwork/man-in-a-red-turban.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Jan_van_Eyck_-_Portrait_of_a_Man_%28Self_Portrait%3F%29_1433.jpg/960px-Jan_van_Eyck_-_Portrait_of_a_Man_%28Self_Portrait%3F%29_1433.jpg`.

### 412. rogier-van-der-weyden / The Descent from the Cross

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `rogier-van-der-weyden` → `The Descent from the Cross`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/El_Descendimiento%2C_by_Rogier_van_der_Weyden%2C_from_Prado_in_Google_Earth.jpg/960px-El_Descendimiento%2C_by_Rogier_van_der_Weyden%2C_from_Prado_in_Google_Earth.jpg`; page: `https://commons.wikimedia.org/wiki/File:El_Descendimiento,_by_Rogier_van_der_Weyden,_from_Prado_in_Google_Earth.jpg`.
- Normalized gallery asset: `El Descendimiento, by Rogier van der Weyden, from Prado in Google Earth.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `the-descent-from-the-cross-van-der-weyden`; title `The Descent from the Cross`; worksKey `(absent)`; artistId `rogier-van-der-weyden`. Evidence: same Commons asset `El Descendimiento, by Rogier van der Weyden, from Prado in Google Earth.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/El_Descendimiento%2C_by_Rogier_van_der_Weyden%2C_from_Prado_in_Google_Earth.jpg/960px-El_Descendimiento%2C_by_Rogier_van_der_Weyden%2C_from_Prado_in_Google_Earth.jpg`; page: `https://commons.wikimedia.org/wiki/File:El_Descendimiento,_by_Rogier_van_der_Weyden,_from_Prado_in_Google_Earth.jpg`.
- Checked-in route `p/artwork/the-descent-from-the-cross-van-der-weyden.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/El_Descendimiento%2C_by_Rogier_van_der_Weyden%2C_from_Prado_in_Google_Earth.jpg/960px-El_Descendimiento%2C_by_Rogier_van_der_Weyden%2C_from_Prado_in_Google_Earth.jpg`.

### 413. rogier-van-der-weyden / The Last Judgment Polyptych (Beaune)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `rogier-van-der-weyden` → `The Last Judgment Polyptych (Beaune)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Rogier_van_der_Weyden_001.jpg/960px-Rogier_van_der_Weyden_001.jpg`; page: `https://commons.wikimedia.org/wiki/File:Rogier_van_der_Weyden_001.jpg`.
- Normalized gallery asset: `Rogier van der Weyden 001.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/rogier-van-der-weyden`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 414. rogier-van-der-weyden / Portrait of a Lady

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `rogier-van-der-weyden` → `Portrait of a Lady`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Rogier_van_der_Weyden_-_Portrait_of_a_Lady_-_Google_Art_Project.jpg/500px-Rogier_van_der_Weyden_-_Portrait_of_a_Lady_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Rogier_van_der_Weyden_-_Portrait_of_a_Lady_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Rogier van der Weyden - Portrait of a Lady - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/rogier-van-der-weyden`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 415. fra-angelico / The Annunciation (San Marco)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `fra-angelico` → `The Annunciation (San Marco)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Angelico_Annunciation_%28Cortona%29.jpg/960px-Angelico_Annunciation_%28Cortona%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Angelico_Annunciation_(Cortona).jpg`.
- Normalized gallery asset: `Angelico Annunciation (Cortona).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/fra-angelico`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 416. fra-angelico / The Deposition

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `fra-angelico` → `The Deposition`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Fra_Angelico_076.jpg/500px-Fra_Angelico_076.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fra_Angelico_076.jpg`.
- Normalized gallery asset: `Fra Angelico 076.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/fra-angelico`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 417. fra-angelico / Coronation of the Virgin

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `fra-angelico` → `Coronation of the Virgin`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Fra_Angelico_-_Coronation_of_the_Virgin_-_1944.79_-_Cleveland_Museum_of_Art.tiff/lossy-page1-500px-Fra_Angelico_-_Coronation_of_the_Virgin_-_1944.79_-_Cleveland_Museum_of_Art.tiff.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fra_Angelico_-_Coronation_of_the_Virgin_-_1944.79_-_Cleveland_Museum_of_Art.tiff`.
- Normalized gallery asset: `Fra Angelico - Coronation of the Virgin - 1944.79 - Cleveland Museum of Art.tiff`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/fra-angelico`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 418. masaccio / The Holy Trinity

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `masaccio` → `The Holy Trinity`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Masaccio%2C_trinit%C3%A0.jpg/500px-Masaccio%2C_trinit%C3%A0.jpg`; page: `https://en.wikipedia.org/wiki/Holy_Trinity_(Masaccio)`.
- Normalized gallery asset: `Masaccio, trinità.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `the-holy-trinity-masaccio`; title `The Holy Trinity`; worksKey `(absent)`; artistId `masaccio`. Evidence: same Commons asset `Masaccio, trinità.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Masaccio%2C_trinit%C3%A0.jpg/500px-Masaccio%2C_trinit%C3%A0.jpg`; page: `https://commons.wikimedia.org/wiki/File:Masaccio,_trinit%C3%A0.jpg`.
- Checked-in route `p/artwork/the-holy-trinity-masaccio.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Masaccio%2C_trinit%C3%A0.jpg/500px-Masaccio%2C_trinit%C3%A0.jpg`.

### 419. masaccio / The Tribute Money

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `masaccio` → `The Tribute Money`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/The_Tribute_Money_by_Masaccio.jpg/500px-The_Tribute_Money_by_Masaccio.jpg`; page: `https://en.wikipedia.org/wiki/The_Tribute_Money_(Masaccio)`.
- Normalized gallery asset: `The Tribute Money by Masaccio.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/masaccio`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 420. masaccio / The Expulsion from the Garden of Eden

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `masaccio` → `The Expulsion from the Garden of Eden`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Masaccio-TheExpulsionOfAdamAndEveFromEden-Restoration.jpg/500px-Masaccio-TheExpulsionOfAdamAndEveFromEden-Restoration.jpg`; page: `https://en.wikipedia.org/wiki/Expulsion_from_the_Garden_of_Eden`.
- Normalized gallery asset: `Masaccio-TheExpulsionOfAdamAndEveFromEden-Restoration.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/masaccio`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 421. piero-della-francesca / The Resurrection

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `piero-della-francesca` → `The Resurrection`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Piero_della_Francesca_The_Resurrection_detail_VlRan.jpg/960px-Piero_della_Francesca_The_Resurrection_detail_VlRan.jpg`; page: `https://commons.wikimedia.org/wiki/File:Piero_della_Francesca_The_Resurrection_detail_VlRan.jpg`.
- Normalized gallery asset: `Piero della Francesca The Resurrection detail VlRan.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/piero-della-francesca`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 422. piero-della-francesca / The Flagellation of Christ

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `piero-della-francesca` → `The Flagellation of Christ`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Piero_della_Francesca_042.jpg/960px-Piero_della_Francesca_042.jpg`; page: `https://commons.wikimedia.org/wiki/File:Piero_della_Francesca_042.jpg`.
- Normalized gallery asset: `Piero della Francesca 042.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/piero-della-francesca`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 423. piero-della-francesca / The Legend of the True Cross

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `piero-della-francesca` → `The Legend of the True Cross`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Arezzo_Piero_general_04.JPG/500px-Arezzo_Piero_general_04.JPG`; page: `https://en.wikipedia.org/wiki/The_Legend_of_the_True_Cross`.
- Normalized gallery asset: `Arezzo Piero general 04.JPG`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/piero-della-francesca`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 424. andrei-rublev / The Trinity

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `andrei-rublev` → `The Trinity`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Andrey_Rublev_-_%D0%A1%D0%B2._%D0%A2%D1%80%D0%BE%D0%B8%D1%86%D0%B0_-_Google_Art_Project.jpg/960px-Andrey_Rublev_-_%D0%A1%D0%B2._%D0%A2%D1%80%D0%BE%D0%B8%D1%86%D0%B0_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Andrey_Rublev_-_%D0%A1%D0%B2._%D0%A2%D1%80%D0%BE%D0%B8%D1%86%D0%B0_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Andrey Rublev - Св. Троица - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-1.js` / `the-trinity`; title `The Trinity`; worksKey `(absent)`; artistId `andrei-rublev`. Evidence: same Commons asset `Andrey Rublev - Св. Троица - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Andrey_Rublev_-_%D0%A1%D0%B2._%D0%A2%D1%80%D0%BE%D0%B8%D1%86%D0%B0_-_Google_Art_Project.jpg/960px-Andrey_Rublev_-_%D0%A1%D0%B2._%D0%A2%D1%80%D0%BE%D0%B8%D1%86%D0%B0_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Andrey_Rublev_-_%D0%A1%D0%B2._%D0%A2%D1%80%D0%BE%D0%B8%D1%86%D0%B0_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/the-trinity.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Andrey_Rublev_-_%D0%A1%D0%B2._%D0%A2%D1%80%D0%BE%D0%B8%D1%86%D0%B0_-_Google_Art_Project.jpg/960px-Andrey_Rublev_-_%D0%A1%D0%B2._%D0%A2%D1%80%D0%BE%D0%B8%D1%86%D0%B0_-_Google_Art_Project.jpg`.

### 425. andrei-rublev / The Saviour (Zvenigorod)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `andrei-rublev` → `The Saviour (Zvenigorod)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Andrey_Rublev_-_%D0%A5%D1%80%D0%B8%D1%81%D1%82%D0%BE%D1%81_%D0%92%D1%81%D0%B5%D0%B4%D0%B5%D1%80%D0%B6%D0%B8%D1%82%D0%B5%D0%BB%D1%8C_-_Google_Art_Project.jpg/960px-Andrey_Rublev_-_%D0%A5%D1%80%D0%B8%D1%81%D1%82%D0%BE%D1%81_%D0%92%D1%81%D0%B5%D0%B4%D0%B5%D1%80%D0%B6%D0%B8%D1%82%D0%B5%D0%BB%D1%8C_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Andrey_Rublev_-_%D0%A5%D1%80%D0%B8%D1%81%D1%82%D0%BE%D1%81_%D0%92%D1%81%D0%B5%D0%B4%D0%B5%D1%80%D0%B6%D0%B8%D1%82%D0%B5%D0%BB%D1%8C_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Andrey Rublev - Христос Вседержитель - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/andrei-rublev`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 426. karl-bryullov / The Last Day of Pompeii

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `karl-bryullov` → `The Last Day of Pompeii`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Karl_Brullov_-_The_Last_Day_of_Pompeii_-_Google_Art_Project.jpg/500px-Karl_Brullov_-_The_Last_Day_of_Pompeii_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/The_Last_Day_of_Pompeii`.
- Normalized gallery asset: `Karl Brullov - The Last Day of Pompeii - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/karl-bryullov`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 427. karl-bryullov / The Rider

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `karl-bryullov` → `The Rider`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Karl_Bryullov_%28Bryullo%29_-_%D0%92%D1%81%D0%B0%D0%B4%D0%BD%D0%B8%D1%86%D0%B0_-_Google_Art_Project.jpg/960px-Karl_Bryullov_%28Bryullo%29_-_%D0%92%D1%81%D0%B0%D0%B4%D0%BD%D0%B8%D1%86%D0%B0_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Karl_Bryullov_(Bryullo)_-_%D0%92%D1%81%D0%B0%D0%B4%D0%BD%D0%B8%D1%86%D0%B0_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Karl Bryullov (Bryullo) - Всадница - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/karl-bryullov`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 428. karl-bryullov / Self-Portrait

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `karl-bryullov` → `Self-Portrait`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Karl_Bryullov_%28Bryullo%29_-_%D0%90%D0%B2%D1%82%D0%BE%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82_-_Google_Art_Project.jpg/500px-Karl_Bryullov_%28Bryullo%29_-_%D0%90%D0%B2%D1%82%D0%BE%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Karl_Bryullov_(Bryullo)_-_%D0%90%D0%B2%D1%82%D0%BE%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Karl Bryullov (Bryullo) - Автопортрет - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/karl-bryullov`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 429. ivan-shishkin / Morning in a Pine Forest

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ivan-shishkin` → `Morning in a Pine Forest`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Shishkin%2C_Ivan_-_Morning_in_a_Pine_Forest.jpg/500px-Shishkin%2C_Ivan_-_Morning_in_a_Pine_Forest.jpg`; page: `https://commons.wikimedia.org/wiki/File:Shishkin,_Ivan_-_Morning_in_a_Pine_Forest.jpg`.
- Normalized gallery asset: `Shishkin, Ivan - Morning in a Pine Forest.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ivan-shishkin`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 430. ivan-shishkin / Rye

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ivan-shishkin` → `Rye`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Ivan_Shishkin_-_%D0%A0%D0%BE%D0%B6%D1%8C_-_Google_Art_Project.jpg/500px-Ivan_Shishkin_-_%D0%A0%D0%BE%D0%B6%D1%8C_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Rye_(Shishkin)`.
- Normalized gallery asset: `Ivan Shishkin - Рожь - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ivan-shishkin`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 431. ivan-shishkin / In the Wild North

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ivan-shishkin` → `In the Wild North`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Shishkin_na_severe_dikom1.jpg/960px-Shishkin_na_severe_dikom1.jpg`; page: `https://commons.wikimedia.org/wiki/File:Shishkin_na_severe_dikom1.jpg`.
- Normalized gallery asset: `Shishkin na severe dikom1.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ivan-shishkin`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 432. isaac-levitan / Above Eternal Peace

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `isaac-levitan` → `Above Eternal Peace`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Levitan_nad_vech_pok28.jpg/960px-Levitan_nad_vech_pok28.jpg`; page: `https://commons.wikimedia.org/wiki/File:Levitan_nad_vech_pok28.jpg`.
- Normalized gallery asset: `Levitan nad vech pok28.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/isaac-levitan`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 433. isaac-levitan / Golden Autumn

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `isaac-levitan` → `Golden Autumn`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Levitan_Zolotaya_Osen.jpg/500px-Levitan_Zolotaya_Osen.jpg`; page: `https://en.wikipedia.org/wiki/Golden_Autumn`.
- Normalized gallery asset: `Levitan Zolotaya Osen.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/isaac-levitan`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 434. isaac-levitan / The Vladimirka Road

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `isaac-levitan` → `The Vladimirka Road`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Vladimirka_without_frame.jpg/500px-Vladimirka_without_frame.jpg`; page: `https://commons.wikimedia.org/wiki/File:Vladimirka_without_frame.jpg`.
- Normalized gallery asset: `Vladimirka without frame.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/isaac-levitan`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 435. mikhail-vrubel / The Demon Seated

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `mikhail-vrubel` → `The Demon Seated`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Vrubel_Demon.jpg/500px-Vrubel_Demon.jpg`; page: `https://en.wikipedia.org/wiki/The_Demon_Seated`.
- Normalized gallery asset: `Vrubel Demon.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/mikhail-vrubel`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 436. mikhail-vrubel / The Demon Downcast

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `mikhail-vrubel` → `The Demon Downcast`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Vrubel_Fallen_Demon.jpg/500px-Vrubel_Fallen_Demon.jpg`; page: `https://en.wikipedia.org/wiki/The_Demon_Downcast`.
- Normalized gallery asset: `Vrubel Fallen Demon.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/mikhail-vrubel`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 437. mikhail-vrubel / The Swan Princess

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `mikhail-vrubel` → `The Swan Princess`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Tsarevna-Lebed_by_Mikhail_Vrubel_%28brightened%29.jpg/500px-Tsarevna-Lebed_by_Mikhail_Vrubel_%28brightened%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Swan_Princess_(painting)`.
- Normalized gallery asset: `Tsarevna-Lebed by Mikhail Vrubel (brightened).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/mikhail-vrubel`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 438. lyubov-popova / Painterly Architectonic

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `lyubov-popova` → `Painterly Architectonic`; img: `https://upload.wikimedia.org/wikipedia/commons/d/de/Lyubov_Popova_-_Painterly_Architectonic_-_GMA_2080_-_National_Galleries_of_Scotland.jpg`; page: `https://commons.wikimedia.org/wiki/File:Lyubov_Popova_-_Painterly_Architectonic_-_GMA_2080_-_National_Galleries_of_Scotland.jpg`.
- Normalized gallery asset: `Lyubov Popova - Painterly Architectonic - GMA 2080 - National Galleries of Scotland.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/lyubov-popova`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 439. lyubov-popova / Space-Force Construction

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `lyubov-popova` → `Space-Force Construction`; img: `https://upload.wikimedia.org/wikipedia/commons/1/1f/Lyubov_Popova%2C_Space-Force_Construction_%281921%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Lyubov_Popova,_Space-Force_Construction_(1921).jpg`.
- Normalized gallery asset: `Lyubov Popova, Space-Force Construction (1921).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/lyubov-popova`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 440. lyubov-popova / Textile designs, First State Factory

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `lyubov-popova` → `Textile designs, First State Factory`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Fabric_Designs_by_Popova_04.jpg/500px-Fabric_Designs_by_Popova_04.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fabric_Designs_by_Popova_04.jpg`.
- Normalized gallery asset: `Fabric Designs by Popova 04.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/lyubov-popova`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 441. shen-zhou / Lofty Mount Lu

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `shen-zhou` → `Lofty Mount Lu`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Lofty_Mt.Lu_by_Shen_Zhou.jpg/960px-Lofty_Mt.Lu_by_Shen_Zhou.jpg`; page: `https://commons.wikimedia.org/wiki/File:Lofty_Mt.Lu_by_Shen_Zhou.jpg`.
- Normalized gallery asset: `Lofty Mt.Lu by Shen Zhou.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-9.js` / `lofty-mount-lu`; title `Lofty Mount Lu`; worksKey `(absent)`; artistId `shen-zhou`. Evidence: same Commons asset `Lofty Mt.Lu by Shen Zhou.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Lofty_Mt.Lu_by_Shen_Zhou.jpg/960px-Lofty_Mt.Lu_by_Shen_Zhou.jpg`; page: `https://commons.wikimedia.org/wiki/File:Lofty_Mt.Lu_by_Shen_Zhou.jpg`.
- Checked-in route `p/artwork/lofty-mount-lu.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Lofty_Mt.Lu_by_Shen_Zhou.jpg/960px-Lofty_Mt.Lu_by_Shen_Zhou.jpg`.

### 442. shen-zhou / Poet on a Mountaintop

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `shen-zhou` → `Poet on a Mountaintop`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Poet_on_a_Mountaintop.jpg/500px-Poet_on_a_Mountaintop.jpg`; page: `https://en.wikipedia.org/wiki/Poet_on_a_Mountaintop`.
- Normalized gallery asset: `Poet on a Mountaintop.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/shen-zhou`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 443. bada-shanren / Fish and Rocks

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `bada-shanren` → `Fish and Rocks`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Bada_Shanren_-_Fish_and_Rocks_-_1953.247_-_Cleveland_Museum_of_Art.tiff/lossy-page1-960px-Bada_Shanren_-_Fish_and_Rocks_-_1953.247_-_Cleveland_Museum_of_Art.tiff.jpg`; page: `https://commons.wikimedia.org/wiki/File:Bada_Shanren_-_Fish_and_Rocks_-_1953.247_-_Cleveland_Museum_of_Art.tiff`.
- Normalized gallery asset: `Bada Shanren - Fish and Rocks - 1953.247 - Cleveland Museum of Art.tiff`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/bada-shanren`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 444. bada-shanren / Lotus and Birds

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `bada-shanren` → `Lotus and Birds`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Bada_Shanren_%28Zhu_Da%29_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg/960px-Bada_Shanren_%28Zhu_Da%29_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg`; page: `https://commons.wikimedia.org/wiki/File:Bada_Shanren_(Zhu_Da)_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg`.
- Normalized gallery asset: `Bada Shanren (Zhu Da) - Birds in a lotus pond - 1989.363.135 - Metropolitan Museum of Art.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `birds-in-a-lotus-pond`; title `Birds in a Lotus Pond`; worksKey `Lotus and Birds`; artistId `bada-shanren`. Evidence: same Commons asset `Bada Shanren (Zhu Da) - Birds in a lotus pond - 1989.363.135 - Metropolitan Museum of Art.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Bada_Shanren_%28Zhu_Da%29_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg/960px-Bada_Shanren_%28Zhu_Da%29_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg`; page: `https://commons.wikimedia.org/wiki/File:Bada_Shanren_(Zhu_Da)_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg`.
- Checked-in route `p/artwork/birds-in-a-lotus-pond.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Bada_Shanren_%28Zhu_Da%29_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg/960px-Bada_Shanren_%28Zhu_Da%29_-_Birds_in_a_lotus_pond_-_1989.363.135_-_Metropolitan_Museum_of_Art.jpg`.

### 445. xu-beihong / The Foolish Old Man Removes the Mountains

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `xu-beihong` → `The Foolish Old Man Removes the Mountains`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Xu_Beihong_yugongyishan.jpg/960px-Xu_Beihong_yugongyishan.jpg`; page: `https://commons.wikimedia.org/wiki/File:Xu_Beihong_yugongyishan.jpg`.
- Normalized gallery asset: `Xu Beihong yugongyishan.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/xu-beihong`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 446. sesshu-toyo / Haboku (Splashed Ink) Landscape

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `sesshu-toyo` → `Haboku (Splashed Ink) Landscape`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Sesshu_-_Haboku-Sansui_-_complete.jpg/960px-Sesshu_-_Haboku-Sansui_-_complete.jpg`; page: `https://commons.wikimedia.org/wiki/File:Sesshu_-_Haboku-Sansui_-_complete.jpg`.
- Normalized gallery asset: `Sesshu - Haboku-Sansui - complete.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `haboku-sansui`; title `Haboku Sansui (Splashed-Ink Landscape)`; worksKey `Haboku (Splashed Ink) Landscape`; artistId `sesshu-toyo`. Evidence: same Commons asset `Sesshu - Haboku-Sansui - complete.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Sesshu_-_Haboku-Sansui_-_complete.jpg/960px-Sesshu_-_Haboku-Sansui_-_complete.jpg`; page: `https://commons.wikimedia.org/wiki/File:Sesshu_-_Haboku-Sansui_-_complete.jpg`.
- Checked-in route `p/artwork/haboku-sansui.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Sesshu_-_Haboku-Sansui_-_complete.jpg/960px-Sesshu_-_Haboku-Sansui_-_complete.jpg`.

### 447. sesshu-toyo / Long Scroll of Landscapes (Sansui Chōkan)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `sesshu-toyo` → `Long Scroll of Landscapes (Sansui Chōkan)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Landscapes_of_the_Four_Seasons_by_Sesshu_%28Mori_Museum%29.jpg/960px-Landscapes_of_the_Four_Seasons_by_Sesshu_%28Mori_Museum%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Landscapes_of_the_Four_Seasons_by_Sesshu_(Mori_Museum).jpg`.
- Normalized gallery asset: `Landscapes of the Four Seasons by Sesshu (Mori Museum).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/sesshu-toyo`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 448. ogata-korin / Irises (Kakitsubata-zu)

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `ogata-korin` → `Irises (Kakitsubata-zu)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Irises_screen_2.jpg/500px-Irises_screen_2.jpg`; page: `https://commons.wikimedia.org/wiki/File:Irises_screen_2.jpg`.
- Normalized gallery asset: `Irises screen 2.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-1.js` / `irises`; title `Irises`; worksKey `(absent)`; artistId `vincent-van-gogh`. Evidence: same Commons asset `Irises screen 2.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Irises_screen_2.jpg/500px-Irises_screen_2.jpg`; page: `https://commons.wikimedia.org/wiki/File:Irises_screen_2.jpg`.
- Checked-in route `p/artwork/irises.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Irises_screen_2.jpg/500px-Irises_screen_2.jpg`.

### 449. ogata-korin / Red and White Plum Blossoms

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `ogata-korin` → `Red and White Plum Blossoms`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_%28National_Treasure%29_-_Google_Art_Project.jpg/500px-Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_%28National_Treasure%29_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Red_and_White_Plum_Blossoms`.
- Normalized gallery asset: `Ogata Korin - RED AND WHITE PLUM BLOSSOMS (National Treasure) - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `red-and-white-plum-blossoms`; title `Red and White Plum Blossoms`; worksKey `(absent)`; artistId `ogata-korin`. Evidence: same Commons asset `Ogata Korin - RED AND WHITE PLUM BLOSSOMS (National Treasure) - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_%28National_Treasure%29_-_Google_Art_Project.jpg/500px-Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_%28National_Treasure%29_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_(National_Treasure)_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/red-and-white-plum-blossoms.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_%28National_Treasure%29_-_Google_Art_Project.jpg/500px-Ogata_Korin_-_RED_AND_WHITE_PLUM_BLOSSOMS_%28National_Treasure%29_-_Google_Art_Project.jpg`.

### 450. ogata-korin / Wind God and Thunder God (after Sōtatsu)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ogata-korin` → `Wind God and Thunder God (after Sōtatsu)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Wind_God_and_Thunder_God_Screens_by_Ogata_Korin.png/500px-Wind_God_and_Thunder_God_Screens_by_Ogata_Korin.png`; page: `https://en.wikipedia.org/wiki/Wind_God_and_Thunder_God_(K%C5%8Drin)`.
- Normalized gallery asset: `Wind God and Thunder God Screens by Ogata Korin.png`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ogata-korin`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 451. ito-jakuchu / Colorful Realm of Living Beings

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ito-jakuchu` → `Colorful Realm of Living Beings`; img: `https://upload.wikimedia.org/wikipedia/commons/9/91/It%C5%8D_Jakuch%C5%AB_-_Fish_in_a_lotus_pond_%28Colorful_Realm_of_Living_Beings%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:It%C5%8D_Jakuch%C5%AB_-_Fish_in_a_lotus_pond_(Colorful_Realm_of_Living_Beings).jpg`.
- Normalized gallery asset: `Itō Jakuchū - Fish in a lotus pond (Colorful Realm of Living Beings).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ito-jakuchu`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 452. ito-jakuchu / Birds and Animals in the Flower Garden

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ito-jakuchu` → `Birds and Animals in the Flower Garden`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/It%C5%8D_Jakuch%C5%AB_-_Animals_in_the_Flower_garden_%28Left-hand_screen%29.jpg/960px-It%C5%8D_Jakuch%C5%AB_-_Animals_in_the_Flower_garden_%28Left-hand_screen%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:It%C5%8D_Jakuch%C5%AB_-_Animals_in_the_Flower_garden_(Left-hand_screen).jpg`.
- Normalized gallery asset: `Itō Jakuchū - Animals in the Flower garden (Left-hand screen).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ito-jakuchu`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 453. ito-jakuchu / White Phoenix

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ito-jakuchu` → `White Phoenix`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Ito_Jakuchu_001.jpg/960px-Ito_Jakuchu_001.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ito_Jakuchu_001.jpg`.
- Normalized gallery asset: `Ito Jakuchu 001.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ito-jakuchu`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 454. uemura-shoen / Jo no Mai (Dance Performed in a Noh Play)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `uemura-shoen` → `Jo no Mai (Dance Performed in a Noh Play)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Jo-no-mai_by_Uemura_Shoen.jpg/960px-Jo-no-mai_by_Uemura_Shoen.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jo-no-mai_by_Uemura_Shoen.jpg`.
- Normalized gallery asset: `Jo-no-mai by Uemura Shoen.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/uemura-shoen`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 455. uemura-shoen / Flame (Honō)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `uemura-shoen` → `Flame (Honō)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Uemura-Flame-1918.jpg/960px-Uemura-Flame-1918.jpg`; page: `https://commons.wikimedia.org/wiki/File:Uemura-Flame-1918.jpg`.
- Normalized gallery asset: `Uemura-Flame-1918.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/uemura-shoen`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 456. kim-hong-do / Ssireum (Wrestling)

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `kim-hong-do` → `Ssireum (Wrestling)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Danwon_Ssireum.jpg/960px-Danwon_Ssireum.jpg`; page: `https://commons.wikimedia.org/wiki/File:Danwon_Ssireum.jpg`.
- Normalized gallery asset: `Danwon Ssireum.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `ssireum`; title `Ssireum`; worksKey `Ssireum (Wrestling)`; artistId `kim-hong-do`. Evidence: same Commons asset `Danwon Ssireum.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Danwon_Ssireum.jpg/960px-Danwon_Ssireum.jpg`; page: `https://commons.wikimedia.org/wiki/File:Danwon_Ssireum.jpg`.
- Checked-in route `p/artwork/ssireum.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Danwon_Ssireum.jpg/960px-Danwon_Ssireum.jpg`.

### 457. raja-ravi-varma / Shakuntala

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `raja-ravi-varma` → `Shakuntala`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Raja_Ravi_Varma_-_Mahabharata_-_Shakuntala.jpg/500px-Raja_Ravi_Varma_-_Mahabharata_-_Shakuntala.jpg`; page: `https://en.wikipedia.org/wiki/Shakuntala_(Raja_Ravi_Varma)`.
- Normalized gallery asset: `Raja Ravi Varma - Mahabharata - Shakuntala.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/raja-ravi-varma`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 458. raja-ravi-varma / Lady in the Moonlight

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `raja-ravi-varma` → `Lady in the Moonlight`; img: `https://upload.wikimedia.org/wikipedia/commons/1/11/Raja_Ravi_Varma%2C_Lady_in_the_Moon_Light_%281889%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Raja_Ravi_Varma,_Lady_in_the_Moon_Light_(1889).jpg`.
- Normalized gallery asset: `Raja Ravi Varma, Lady in the Moon Light (1889).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/raja-ravi-varma`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 459. raja-ravi-varma / Galaxy of Musicians

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `raja-ravi-varma` → `Galaxy of Musicians`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Raja_Ravi_Varma%2C_Galaxy_of_Musicians.jpg/500px-Raja_Ravi_Varma%2C_Galaxy_of_Musicians.jpg`; page: `https://en.wikipedia.org/wiki/Galaxy_of_Musicians`.
- Normalized gallery asset: `Raja Ravi Varma, Galaxy of Musicians.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/raja-ravi-varma`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 460. reza-abbasi / Youth Reading

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `reza-abbasi` → `Youth Reading`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Riza-yi-Abbasi_008.jpg/960px-Riza-yi-Abbasi_008.jpg`; page: `https://commons.wikimedia.org/wiki/File:Riza-yi-Abbasi_008.jpg`.
- Normalized gallery asset: `Riza-yi-Abbasi 008.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/reza-abbasi`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 461. reza-abbasi / Two Lovers

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `reza-abbasi` → `Two Lovers`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Reza_Abbasi_-_Two_Lovers_%281630%29.jpg/500px-Reza_Abbasi_-_Two_Lovers_%281630%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Lovers_(Abbasi)`.
- Normalized gallery asset: `Reza Abbasi - Two Lovers (1630).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `the-lovers-abbasi`; title `The Lovers`; worksKey `Two Lovers`; artistId `reza-abbasi`. Evidence: same Commons asset `Reza Abbasi - Two Lovers (1630).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Reza_Abbasi_-_Two_Lovers_%281630%29.jpg/500px-Reza_Abbasi_-_Two_Lovers_%281630%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Reza_Abbasi_-_Two_Lovers_(1630).jpg`.
- Checked-in route `p/artwork/the-lovers-abbasi.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Reza_Abbasi_-_Two_Lovers_%281630%29.jpg/500px-Reza_Abbasi_-_Two_Lovers_%281630%29.jpg`.

### 462. reza-abbasi / Young Man with a Sword

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `reza-abbasi` → `Young Man with a Sword`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Riza-i_Abbasi_Young_Man_with_a_Sword_-_Detroit_Institute_of_Arts.jpg/500px-Riza-i_Abbasi_Young_Man_with_a_Sword_-_Detroit_Institute_of_Arts.jpg`; page: `https://commons.wikimedia.org/wiki/File:Riza-i_Abbasi_Young_Man_with_a_Sword_-_Detroit_Institute_of_Arts.jpg`.
- Normalized gallery asset: `Riza-i Abbasi Young Man with a Sword - Detroit Institute of Arts.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/reza-abbasi`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 463. giotto / The Scrovegni (Arena) Chapel frescoes

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giotto` → `The Scrovegni (Arena) Chapel frescoes`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Giotto_di_Bondone_-_Scenes_with_decorative_bands_-_WGA09284.jpg/500px-Giotto_di_Bondone_-_Scenes_with_decorative_bands_-_WGA09284.jpg`; page: `https://commons.wikimedia.org/wiki/File:Giotto_di_Bondone_-_Scenes_with_decorative_bands_-_WGA09284.jpg`.
- Normalized gallery asset: `Giotto di Bondone - Scenes with decorative bands - WGA09284.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giotto`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 464. giotto / Ognissanti Madonna

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `giotto` → `Ognissanti Madonna`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Giotto%2C_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg/500px-Giotto%2C_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Ognissanti_Madonna`.
- Normalized gallery asset: `Giotto, 1267 Around-1337 - Maestà - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `ognissanti-madonna`; title `Ognissanti Madonna`; worksKey `Ognissanti Madonna`; artistId `giotto`. Evidence: same Commons asset `Giotto, 1267 Around-1337 - Maestà - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Giotto%2C_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg/500px-Giotto%2C_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Giotto,_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/ognissanti-madonna.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Giotto%2C_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg/500px-Giotto%2C_1267_Around-1337_-_Maest%C3%A0_-_Google_Art_Project.jpg`.

### 465. giotto / The Lamentation

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giotto` → `The Lamentation`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Giotto_di_Bondone_-_Scenes_from_the_New_Testament_-_Lamentation_-_WGA09159.jpg/500px-Giotto_di_Bondone_-_Scenes_from_the_New_Testament_-_Lamentation_-_WGA09159.jpg`; page: `https://commons.wikimedia.org/wiki/File:Giotto_di_Bondone_-_Scenes_from_the_New_Testament_-_Lamentation_-_WGA09159.jpg`.
- Normalized gallery asset: `Giotto di Bondone - Scenes from the New Testament - Lamentation - WGA09159.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giotto`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 466. duccio / Maestà

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `duccio` → `Maestà`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Duccio_di_Buoninsegna_038.jpg/500px-Duccio_di_Buoninsegna_038.jpg`; page: `https://commons.wikimedia.org/wiki/File:Duccio_di_Buoninsegna_038.jpg`.
- Normalized gallery asset: `Duccio di Buoninsegna 038.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/duccio`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 467. duccio / Rucellai Madonna

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `duccio` → `Rucellai Madonna`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Duccio_-_Rucellai_Madonna.jpg/500px-Duccio_-_Rucellai_Madonna.jpg`; page: `https://en.wikipedia.org/wiki/Rucellai_Madonna`.
- Normalized gallery asset: `Duccio - Rucellai Madonna.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/duccio`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 468. duccio / Madonna and Child (Stoclet Madonna)

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `duccio` → `Madonna and Child (Stoclet Madonna)`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Duccio_Di_Buoninsegna_-_Madonna_col_Bambino.jpg/500px-Duccio_Di_Buoninsegna_-_Madonna_col_Bambino.jpg`; page: `https://commons.wikimedia.org/wiki/File:Duccio_Di_Buoninsegna_-_Madonna_col_Bambino.jpg`.
- Normalized gallery asset: `Duccio Di Buoninsegna - Madonna col Bambino.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/duccio`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 469. theophanes-the-greek / Frescoes of the Transfiguration Church, Novgorod

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `theophanes-the-greek` → `Frescoes of the Transfiguration Church, Novgorod`; img: `https://upload.wikimedia.org/wikipedia/commons/a/ac/Eleutherius_of_Illyria_%281378%2C_Theophanes_the_Greek%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Eleutherius_of_Illyria_(1378,_Theophanes_the_Greek).jpg`.
- Normalized gallery asset: `Eleutherius of Illyria (1378, Theophanes the Greek).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-7.js` / `frescoes-of-the-transfiguration-novgorod`; title `Frescoes of the Church of the Transfiguration, Novgorod`; worksKey `Frescoes of the Transfiguration Church, Novgorod`; artistId `theophanes-the-greek`. Evidence: same Commons asset `Eleutherius of Illyria (1378, Theophanes the Greek).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/a/ac/Eleutherius_of_Illyria_%281378%2C_Theophanes_the_Greek%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Eleutherius_of_Illyria_(1378,_Theophanes_the_Greek).jpg`.
- Checked-in route `p/artwork/frescoes-of-the-transfiguration-novgorod.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/a/ac/Eleutherius_of_Illyria_%281378%2C_Theophanes_the_Greek%29.jpg`.

### 470. gustave-dore / Dante's Divine Comedy illustrations

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `gustave-dore` → `Dante's Divine Comedy illustrations`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Gustave_Dor%C3%A9_-_Dante_Alighieri_-_Inferno_-_Plate_9_%28Canto_III_-_Charon%29.jpg/500px-Gustave_Dor%C3%A9_-_Dante_Alighieri_-_Inferno_-_Plate_9_%28Canto_III_-_Charon%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Gustave_Dor%C3%A9_-_Dante_Alighieri_-_Inferno_-_Plate_9_(Canto_III_-_Charon).jpg`.
- Normalized gallery asset: `Gustave Doré - Dante Alighieri - Inferno - Plate 9 (Canto III - Charon).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/gustave-dore`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 471. gustave-dore / Don Quixote illustrations

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `gustave-dore` → `Don Quixote illustrations`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Don_Quixote_1.jpg/500px-Don_Quixote_1.jpg`; page: `https://commons.wikimedia.org/wiki/File:Don_Quixote_1.jpg`.
- Normalized gallery asset: `Don Quixote 1.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/gustave-dore`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 472. gustave-dore / London: A Pilgrimage

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `gustave-dore` → `London: A Pilgrimage`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Gustave_Dor%C3%A9_-_Wentworth_Street_Whitechapel_-_London%2C_a_Pilgrimage.jpg/500px-Gustave_Dor%C3%A9_-_Wentworth_Street_Whitechapel_-_London%2C_a_Pilgrimage.jpg`; page: `https://commons.wikimedia.org/wiki/File:Gustave_Dor%C3%A9_-_Wentworth_Street_Whitechapel_-_London,_a_Pilgrimage.jpg`.
- Normalized gallery asset: `Gustave Doré - Wentworth Street Whitechapel - London, a Pilgrimage.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/gustave-dore`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 473. gustave-dore / The Enigma

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `gustave-dore` → `The Enigma`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Dor%C3%A9_%E2%80%94_Enigma_%281871%29.jpg/500px-Dor%C3%A9_%E2%80%94_Enigma_%281871%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Dor%C3%A9_%E2%80%94_Enigma_(1871).jpg`.
- Normalized gallery asset: `Doré — Enigma (1871).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/gustave-dore`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 474. kitagawa-utamaro / Three Beauties of the Present Day

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kitagawa-utamaro` → `Three Beauties of the Present Day`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Utamaro_%281793%29_Three_Beauties_of_the_Present_Time%2C_MFAB_21.6382.jpg/500px-Utamaro_%281793%29_Three_Beauties_of_the_Present_Time%2C_MFAB_21.6382.jpg`; page: `https://en.wikipedia.org/wiki/Three_Beauties_of_the_Present_Day`.
- Normalized gallery asset: `Utamaro (1793) Three Beauties of the Present Time, MFAB 21.6382.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kitagawa-utamaro`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 475. kitagawa-utamaro / Ten Studies in Female Physiognomy

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kitagawa-utamaro` → `Ten Studies in Female Physiognomy`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Fujin_s%C5%8Dgaku_juttai%2C_Kamisuki_by_Utamaro.jpg/500px-Fujin_s%C5%8Dgaku_juttai%2C_Kamisuki_by_Utamaro.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fujin_s%C5%8Dgaku_juttai,_Kamisuki_by_Utamaro.jpg`.
- Normalized gallery asset: `Fujin sōgaku juttai, Kamisuki by Utamaro.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kitagawa-utamaro`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 476. kitagawa-utamaro / Woman Playing a Poppin

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kitagawa-utamaro` → `Woman Playing a Poppin`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Flickr_-_%E2%80%A6trialsanderrors_-_Utamaro%2C_Young_lady_blowing_on_a_poppin%2C_1790.jpg/500px-Flickr_-_%E2%80%A6trialsanderrors_-_Utamaro%2C_Young_lady_blowing_on_a_poppin%2C_1790.jpg`; page: `https://commons.wikimedia.org/wiki/File:Flickr_-_%E2%80%A6trialsanderrors_-_Utamaro,_Young_lady_blowing_on_a_poppin,_1790.jpg`.
- Normalized gallery asset: `Flickr - …trialsanderrors - Utamaro, Young lady blowing on a poppin, 1790.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kitagawa-utamaro`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 477. james-ensor / Christ's Entry into Brussels in 1889

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `james-ensor` → `Christ's Entry into Brussels in 1889`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Christ%27s_Entry_into_Brussels_in_1889.jpg/500px-Christ%27s_Entry_into_Brussels_in_1889.jpg`; page: `https://en.wikipedia.org/wiki/Christ's_Entry_Into_Brussels_in_1889`.
- Normalized gallery asset: `Christ's Entry into Brussels in 1889.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/james-ensor`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 478. james-ensor / The Intrigue

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `james-ensor` → `The Intrigue`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/De_intrige%2C_James_Ensor%2C_1890%2C_Koninklijk_Museum_voor_Schone_Kunsten_Antwerpen%2C_1856.002.jpeg/500px-De_intrige%2C_James_Ensor%2C_1890%2C_Koninklijk_Museum_voor_Schone_Kunsten_Antwerpen%2C_1856.002.jpeg`; page: `https://commons.wikimedia.org/wiki/File:De_intrige,_James_Ensor,_1890,_Koninklijk_Museum_voor_Schone_Kunsten_Antwerpen,_1856.002.jpeg`.
- Normalized gallery asset: `De intrige, James Ensor, 1890, Koninklijk Museum voor Schone Kunsten Antwerpen, 1856.002.jpeg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/james-ensor`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 479. james-ensor / Skeletons Fighting over a Pickled Herring

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `james-ensor` → `Skeletons Fighting over a Pickled Herring`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Ensor-11156-SkeletonsFightingoveraPickled.jpg/500px-Ensor-11156-SkeletonsFightingoveraPickled.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ensor-11156-SkeletonsFightingoveraPickled.jpg`.
- Normalized gallery asset: `Ensor-11156-SkeletonsFightingoveraPickled.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/james-ensor`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 480. james-ensor / Self-Portrait with Masks

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `james-ensor` → `Self-Portrait with Masks`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Ensor_with_Masks%2C_self-portrait%2C_Ensor_aux_masques%2C_autoportrait%2C_1899%2C_oil_on_canvas%2C_117_x_82_cm%2C_Menard_Art_Museum%2C_Komaki%2C_Japan.jpg/500px-Ensor_with_Masks%2C_self-portrait%2C_Ensor_aux_masques%2C_autoportrait%2C_1899%2C_oil_on_canvas%2C_117_x_82_cm%2C_Menard_Art_Museum%2C_Komaki%2C_Japan.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ensor_with_Masks,_self-portrait,_Ensor_aux_masques,_autoportrait,_1899,_oil_on_canvas,_117_x_82_cm,_Menard_Art_Museum,_Komaki,_Japan.jpg`.
- Normalized gallery asset: `Ensor with Masks, self-portrait, Ensor aux masques, autoportrait, 1899, oil on canvas, 117 x 82 cm, Menard Art Museum, Komaki, Japan.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/james-ensor`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 481. ferdinand-hodler / Night

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ferdinand-hodler` → `Night`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Ferdinand_Hodler_-_Die_Nacht_%281889-90%29.jpg/500px-Ferdinand_Hodler_-_Die_Nacht_%281889-90%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ferdinand_Hodler_-_Die_Nacht_(1889-90).jpg`.
- Normalized gallery asset: `Ferdinand Hodler - Die Nacht (1889-90).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ferdinand-hodler`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 482. ferdinand-hodler / The Chosen One

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ferdinand-hodler` → `The Chosen One`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Ferdinand_Hodler_002.jpg/500px-Ferdinand_Hodler_002.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ferdinand_Hodler_002.jpg`.
- Normalized gallery asset: `Ferdinand Hodler 002.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ferdinand-hodler`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 483. ferdinand-hodler / The Woodcutter

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ferdinand-hodler` → `The Woodcutter`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Ferdinand_Hodler_-_Der_Holzf%C3%A4ller%2C_1910.jpg/500px-Ferdinand_Hodler_-_Der_Holzf%C3%A4ller%2C_1910.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ferdinand_Hodler_-_Der_Holzf%C3%A4ller,_1910.jpg`.
- Normalized gallery asset: `Ferdinand Hodler - Der Holzfäller, 1910.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ferdinand-hodler`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 484. frederic-edwin-church / Niagara

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `frederic-edwin-church` → `Niagara`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Frederic_Edwin_Church_-_Niagara_Falls_-_WGA04867.jpg/500px-Frederic_Edwin_Church_-_Niagara_Falls_-_WGA04867.jpg`; page: `https://en.wikipedia.org/wiki/Niagara_(Frederic_Edwin_Church)`.
- Normalized gallery asset: `Frederic Edwin Church - Niagara Falls - WGA04867.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/frederic-edwin-church`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 485. frederic-edwin-church / The Heart of the Andes

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `frederic-edwin-church` → `The Heart of the Andes`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Church_Heart_of_the_Andes.jpg/500px-Church_Heart_of_the_Andes.jpg`; page: `https://en.wikipedia.org/wiki/The_Heart_of_the_Andes`.
- Normalized gallery asset: `Church Heart of the Andes.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-7.js` / `the-heart-of-the-andes`; title `The Heart of the Andes`; worksKey `(absent)`; artistId `frederic-edwin-church`. Evidence: same Commons asset `Church Heart of the Andes.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Church_Heart_of_the_Andes.jpg/500px-Church_Heart_of_the_Andes.jpg`; page: `https://commons.wikimedia.org/wiki/File:Church_Heart_of_the_Andes.jpg`.
- Checked-in route `p/artwork/the-heart-of-the-andes.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Church_Heart_of_the_Andes.jpg/500px-Church_Heart_of_the_Andes.jpg`.

### 486. frederic-edwin-church / The Icebergs

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `frederic-edwin-church` → `The Icebergs`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/The_Icebergs_%28Frederic_Edwin_Church%29%2C_1861_%28color%29.jpg/500px-The_Icebergs_%28Frederic_Edwin_Church%29%2C_1861_%28color%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Icebergs`.
- Normalized gallery asset: `The Icebergs (Frederic Edwin Church), 1861 (color).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/frederic-edwin-church`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 487. frederic-edwin-church / Cotopaxi

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `frederic-edwin-church` → `Cotopaxi`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Cotopaxi_church.jpg/500px-Cotopaxi_church.jpg`; page: `https://en.wikipedia.org/wiki/Cotopaxi_(painting)`.
- Normalized gallery asset: `Cotopaxi church.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/frederic-edwin-church`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 488. frederic-edwin-church / Aurora Borealis

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `frederic-edwin-church` → `Aurora Borealis`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Frederic_Edwin_Church_-_Aurora_Borealis_-_Google_Art_Project.jpg/500px-Frederic_Edwin_Church_-_Aurora_Borealis_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Aurora_Borealis_(painting)`.
- Normalized gallery asset: `Frederic Edwin Church - Aurora Borealis - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/frederic-edwin-church`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 489. thomas-cole / The Oxbow

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `thomas-cole` → `The Oxbow`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Cole_Thomas_The_Oxbow_%28The_Connecticut_River_near_Northampton_1836%29.jpg/500px-Cole_Thomas_The_Oxbow_%28The_Connecticut_River_near_Northampton_1836%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Oxbow_(Cole)`.
- Normalized gallery asset: `Cole Thomas The Oxbow (The Connecticut River near Northampton 1836).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/thomas-cole`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 490. thomas-cole / The Course of Empire: Destruction

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `thomas-cole` → `The Course of Empire: Destruction`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Cole_Thomas_The_Course_of_Empire_Destruction_1836.jpg/500px-Cole_Thomas_The_Course_of_Empire_Destruction_1836.jpg`; page: `https://commons.wikimedia.org/wiki/File:Cole_Thomas_The_Course_of_Empire_Destruction_1836.jpg`.
- Normalized gallery asset: `Cole Thomas The Course of Empire Destruction 1836.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/thomas-cole`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 491. thomas-cole / The Voyage of Life: Childhood

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `thomas-cole` → `The Voyage of Life: Childhood`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Thomas_Cole_-_The_Voyage_of_Life_Childhood%2C_1842_%28National_Gallery_of_Art%29.jpg/500px-Thomas_Cole_-_The_Voyage_of_Life_Childhood%2C_1842_%28National_Gallery_of_Art%29.jpg`; page: `https://en.wikipedia.org/wiki/The_Voyage_of_Life`.
- Normalized gallery asset: `Thomas Cole - The Voyage of Life Childhood, 1842 (National Gallery of Art).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/thomas-cole`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 492. thomas-cole / Expulsion from the Garden of Eden

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `thomas-cole` → `Expulsion from the Garden of Eden`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Cole_Thomas_Expulsion_from_the_Garden_of_Eden_1828.jpg/500px-Cole_Thomas_Expulsion_from_the_Garden_of_Eden_1828.jpg`; page: `https://en.wikipedia.org/wiki/Expulsion_from_the_Garden_of_Eden_(Cole)`.
- Normalized gallery asset: `Cole Thomas Expulsion from the Garden of Eden 1828.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/thomas-cole`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 493. andrea-mantegna / Lamentation of Christ

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `andrea-mantegna` → `Lamentation of Christ`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_dead_Christ_and_three_mourners%2C_by_Andrea_Mantegna.jpg/500px-The_dead_Christ_and_three_mourners%2C_by_Andrea_Mantegna.jpg`; page: `https://en.wikipedia.org/wiki/Lamentation_of_Christ_(Mantegna)`.
- Normalized gallery asset: `The dead Christ and three mourners, by Andrea Mantegna.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `lamentation-of-christ-mantegna`; title `Lamentation of Christ`; worksKey `Lamentation of Christ`; artistId `andrea-mantegna`. Evidence: same Commons asset `The dead Christ and three mourners, by Andrea Mantegna.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_dead_Christ_and_three_mourners%2C_by_Andrea_Mantegna.jpg/500px-The_dead_Christ_and_three_mourners%2C_by_Andrea_Mantegna.jpg`; page: `https://commons.wikimedia.org/wiki/File:The_dead_Christ_and_three_mourners,_by_Andrea_Mantegna.jpg`.
- Checked-in route `p/artwork/lamentation-of-christ-mantegna.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_dead_Christ_and_three_mourners%2C_by_Andrea_Mantegna.jpg/500px-The_dead_Christ_and_three_mourners%2C_by_Andrea_Mantegna.jpg`.

### 494. andrea-mantegna / Camera degli Sposi

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `andrea-mantegna` → `Camera degli Sposi`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Mantegna_-_Camera_degli_Sposi.jpg/500px-Mantegna_-_Camera_degli_Sposi.jpg`; page: `https://en.wikipedia.org/wiki/Camera_degli_Sposi`.
- Normalized gallery asset: `Mantegna - Camera degli Sposi.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/andrea-mantegna`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 495. andrea-mantegna / Saint Sebastian

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `andrea-mantegna` → `Saint Sebastian`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Andrea_Mantegna_089.jpg/500px-Andrea_Mantegna_089.jpg`; page: `https://en.wikipedia.org/wiki/Saint_Sebastian_(Mantegna)`.
- Normalized gallery asset: `Andrea Mantegna 089.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/andrea-mantegna`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 496. edward-burne-jones / The Golden Stairs

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `edward-burne-jones` → `The Golden Stairs`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Edward_Burne-Jones_The_Golden_Stairs.jpg/500px-Edward_Burne-Jones_The_Golden_Stairs.jpg`; page: `https://en.wikipedia.org/wiki/The_Golden_Stairs`.
- Normalized gallery asset: `Edward Burne-Jones The Golden Stairs.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/edward-burne-jones`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 497. edward-burne-jones / King Cophetua and the Beggar Maid

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `edward-burne-jones` → `King Cophetua and the Beggar Maid`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Burne-Jones_Cophetua_Beggar_Maid_-_GAP_cropped_hard.jpg/500px-Burne-Jones_Cophetua_Beggar_Maid_-_GAP_cropped_hard.jpg`; page: `https://en.wikipedia.org/wiki/King_Cophetua_and_the_Beggar_Maid_(painting)`.
- Normalized gallery asset: `Burne-Jones Cophetua Beggar Maid - GAP cropped hard.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/edward-burne-jones`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 498. edward-burne-jones / The Beguiling of Merlin

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `edward-burne-jones` → `The Beguiling of Merlin`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Beguiling_of_Merlin.jpg/500px-Beguiling_of_Merlin.jpg`; page: `https://en.wikipedia.org/wiki/The_Beguiling_of_Merlin`.
- Normalized gallery asset: `Beguiling of Merlin.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/edward-burne-jones`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 499. anders-zorn / Midsummer Dance

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `anders-zorn` → `Midsummer Dance`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Anders_Zorn_-_Midsummer_Dance_-_Google_Art_Project.jpg/500px-Anders_Zorn_-_Midsummer_Dance_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Anders_Zorn_-_Midsummer_Dance_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Anders Zorn - Midsummer Dance - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/anders-zorn`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 500. anders-zorn / The Omnibus

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `anders-zorn` → `The Omnibus`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Anders_Zorn_-_The_Omnibus_-_P3e1_-_Isabella_Stewart_Gardner_Museum.jpg/500px-Anders_Zorn_-_The_Omnibus_-_P3e1_-_Isabella_Stewart_Gardner_Museum.jpg`; page: `https://commons.wikimedia.org/wiki/File:Anders_Zorn_-_The_Omnibus_-_P3e1_-_Isabella_Stewart_Gardner_Museum.jpg`.
- Normalized gallery asset: `Anders Zorn - The Omnibus - P3e1 - Isabella Stewart Gardner Museum.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/anders-zorn`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 501. anders-zorn / Self-Portrait with Model

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `anders-zorn` → `Self-Portrait with Model`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Self-_portrait_with_Model_by_Anders_Zorn_1899_-_SMB_280-1906.jpg/500px-Self-_portrait_with_Model_by_Anders_Zorn_1899_-_SMB_280-1906.jpg`; page: `https://commons.wikimedia.org/wiki/File:Self-_portrait_with_Model_by_Anders_Zorn_1899_-_SMB_280-1906.jpg`.
- Normalized gallery asset: `Self- portrait with Model by Anders Zorn 1899 - SMB 280-1906.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/anders-zorn`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 502. peder-severin-kroyer / Summer Evening on Skagen's Southern Beach

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `peder-severin-kroyer` → `Summer Evening on Skagen's Southern Beach`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/P.S._Kr%C3%B8yer_-_Summer_evening_on_Skagen%27s_Beach._Anna_Ancher_and_Marie_Kr%C3%B8yer_walking_together._-_Google_Art_Project.jpg/500px-P.S._Kr%C3%B8yer_-_Summer_evening_on_Skagen%27s_Beach._Anna_Ancher_and_Marie_Kr%C3%B8yer_walking_together._-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Summer_Evening_on_Skagen%27s_Southern_Beach`.
- Normalized gallery asset: `P.S. Krøyer - Summer evening on Skagen's Beach. Anna Ancher and Marie Krøyer walking together. - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/peder-severin-kroyer`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 503. peder-severin-kroyer / Hip, Hip, Hurrah!

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `peder-severin-kroyer` → `Hip, Hip, Hurrah!`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Hipp_hipp_hurra%21_Konstn%C3%A4rsfest_p%C3%A5_Skagen_-_Peder_Severin_Kr%C3%B8yer.jpg/500px-Hipp_hipp_hurra%21_Konstn%C3%A4rsfest_p%C3%A5_Skagen_-_Peder_Severin_Kr%C3%B8yer.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hipp_hipp_hurra!_Konstn%C3%A4rsfest_p%C3%A5_Skagen_-_Peder_Severin_Kr%C3%B8yer.jpg`.
- Normalized gallery asset: `Hipp hipp hurra! Konstnärsfest på Skagen - Peder Severin Krøyer.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/peder-severin-kroyer`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 504. peder-severin-kroyer / The Artist and His Wife on Skagen Beach

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `peder-severin-kroyer` → `The Artist and His Wife on Skagen Beach`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/P_S_Kr%C3%B8yer_1899_-_Sommeraften_ved_Skagens_strand._Kunstneren_og_hans_hustru.jpg/500px-P_S_Kr%C3%B8yer_1899_-_Sommeraften_ved_Skagens_strand._Kunstneren_og_hans_hustru.jpg`; page: `https://commons.wikimedia.org/wiki/File:P_S_Kr%C3%B8yer_1899_-_Sommeraften_ved_Skagens_strand._Kunstneren_og_hans_hustru.jpg`.
- Normalized gallery asset: `P S Krøyer 1899 - Sommeraften ved Skagens strand. Kunstneren og hans hustru.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/peder-severin-kroyer`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 505. anna-ancher / Sunlight in the Blue Room

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `anna-ancher` → `Sunlight in the Blue Room`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg/500px-Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg`; page: `https://en.wikipedia.org/wiki/Sunlight_in_the_Blue_Room`.
- Normalized gallery asset: `Anna Ancher - Sunlight in the blue room - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-5.js` / `sunlight-in-the-blue-room`; title `Sunlight in the Blue Room`; worksKey `(absent)`; artistId `anna-ancher`. Evidence: same Commons asset `Anna Ancher - Sunlight in the blue room - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg/500px-Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/sunlight-in-the-blue-room.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg/500px-Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg`.

### 506. anna-ancher / A Funeral

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `anna-ancher` → `A Funeral`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Anna_Ancher%2C_En_begravelse%2C_1891%2C_KMS1433%2C_Statens_Museum_for_Kunst.jpg/500px-Anna_Ancher%2C_En_begravelse%2C_1891%2C_KMS1433%2C_Statens_Museum_for_Kunst.jpg`; page: `https://commons.wikimedia.org/wiki/File:Anna_Ancher,_En_begravelse,_1891,_KMS1433,_Statens_Museum_for_Kunst.jpg`.
- Normalized gallery asset: `Anna Ancher, En begravelse, 1891, KMS1433, Statens Museum for Kunst.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/anna-ancher`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 507. anna-ancher / Harvesters

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `anna-ancher` → `Harvesters`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Anna_Ancher_-_Harvesters_-_Google_Art_Project.jpg/500px-Anna_Ancher_-_Harvesters_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Anna_Ancher_-_Harvesters_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Anna Ancher - Harvesters - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/anna-ancher`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 508. paula-modersohn-becker / Self-Portrait at Sixth Wedding Anniversary

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `paula-modersohn-becker` → `Self-Portrait at Sixth Wedding Anniversary`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Paula_Moderson-Becker_-_Selbstbildnis_am_6_Hochzeitstag_-_1906.jpeg/500px-Paula_Moderson-Becker_-_Selbstbildnis_am_6_Hochzeitstag_-_1906.jpeg`; page: `https://commons.wikimedia.org/wiki/File:Paula_Moderson-Becker_-_Selbstbildnis_am_6_Hochzeitstag_-_1906.jpeg`.
- Normalized gallery asset: `Paula Moderson-Becker - Selbstbildnis am 6 Hochzeitstag - 1906.jpeg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/paula-modersohn-becker`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 509. paula-modersohn-becker / Self-Portrait with Amber Necklace

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `paula-modersohn-becker` → `Self-Portrait with Amber Necklace`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Paula_Modersohn-Becker_-_Selbstbildnis_als_Halbakt_mit_Bernsteinkette_II.jpg/500px-Paula_Modersohn-Becker_-_Selbstbildnis_als_Halbakt_mit_Bernsteinkette_II.jpg`; page: `https://commons.wikimedia.org/wiki/File:Paula_Modersohn-Becker_-_Selbstbildnis_als_Halbakt_mit_Bernsteinkette_II.jpg`.
- Normalized gallery asset: `Paula Modersohn-Becker - Selbstbildnis als Halbakt mit Bernsteinkette II.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/paula-modersohn-becker`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 510. paula-modersohn-becker / Old Poorhouse Woman with Glass Ball and Poppies

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `paula-modersohn-becker` → `Old Poorhouse Woman with Glass Ball and Poppies`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Paula_Moderson-Becker_-_Alte_Armenh%C3%A4uslerin_mit_Glaskugel_und_Mohnblumen_%281907%29.jpg/500px-Paula_Moderson-Becker_-_Alte_Armenh%C3%A4uslerin_mit_Glaskugel_und_Mohnblumen_%281907%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Paula_Moderson-Becker_-_Alte_Armenh%C3%A4uslerin_mit_Glaskugel_und_Mohnblumen_(1907).jpg`.
- Normalized gallery asset: `Paula Moderson-Becker - Alte Armenhäuslerin mit Glaskugel und Mohnblumen (1907).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/paula-modersohn-becker`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 511. chaim-soutine / Carcass of Beef

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `chaim-soutine` → `Carcass of Beef`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Carcass_of_Beef_by_Chaim_Soutine%2C_c._1925%2C_Albright-Knox_Art_Gallery.jpg/500px-Carcass_of_Beef_by_Chaim_Soutine%2C_c._1925%2C_Albright-Knox_Art_Gallery.jpg`; page: `https://commons.wikimedia.org/wiki/File:Carcass_of_Beef_by_Chaim_Soutine,_c._1925,_Albright-Knox_Art_Gallery.jpg`.
- Normalized gallery asset: `Carcass of Beef by Chaim Soutine, c. 1925, Albright-Knox Art Gallery.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/chaim-soutine`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 512. chaim-soutine / Le Petit Pâtissier

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `chaim-soutine` → `Le Petit Pâtissier`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Cha%C3%AFm_soutine%2C_il_piccolo_pasticcere%2C_1922-23_ca..JPG/500px-Cha%C3%AFm_soutine%2C_il_piccolo_pasticcere%2C_1922-23_ca..JPG`; page: `https://commons.wikimedia.org/wiki/File:Cha%C3%AFm_soutine,_il_piccolo_pasticcere,_1922-23_ca..JPG`.
- Normalized gallery asset: `Chaïm soutine, il piccolo pasticcere, 1922-23 ca..JPG`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/chaim-soutine`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 513. chaim-soutine / Landscape with Figures, Céret

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `chaim-soutine` → `Landscape with Figures, Céret`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/%27Landscape_with_Figures-C%C3%A9ret%27_by_Cha%C3%AFm_Soutine%2C_1922%2C_High_Museum_of_Art.JPG/500px-%27Landscape_with_Figures-C%C3%A9ret%27_by_Cha%C3%AFm_Soutine%2C_1922%2C_High_Museum_of_Art.JPG`; page: `https://commons.wikimedia.org/wiki/File:%27Landscape_with_Figures-C%C3%A9ret%27_by_Cha%C3%AFm_Soutine,_1922,_High_Museum_of_Art.JPG`.
- Normalized gallery asset: `'Landscape with Figures-Céret' by Chaïm Soutine, 1922, High Museum of Art.JPG`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/chaim-soutine`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 514. arkhip-kuindzhi / Moonlit Night on the Dnieper

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `arkhip-kuindzhi` → `Moonlit Night on the Dnieper`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Kuindzhi_Moonlit_night_on_the_Dnieper_1880_grm_x2.jpg/500px-Kuindzhi_Moonlit_night_on_the_Dnieper_1880_grm_x2.jpg`; page: `https://en.wikipedia.org/wiki/Moonlit_Night_on_the_Dnieper`.
- Normalized gallery asset: `Kuindzhi Moonlit night on the Dnieper 1880 grm x2.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/arkhip-kuindzhi`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 515. arkhip-kuindzhi / Birch Grove

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `arkhip-kuindzhi` → `Birch Grove`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/0853Ha._%D0%9A%D1%83%D0%B8%D0%BD%D0%B4%D0%B6%D0%B8_%D0%90.%D0%98._%D0%91%D0%B5%D1%80%D1%91%D0%B7%D0%BE%D0%B2%D0%B0%D1%8F_%D1%80%D0%BE%D1%89%D0%B0.jpg/500px-0853Ha._%D0%9A%D1%83%D0%B8%D0%BD%D0%B4%D0%B6%D0%B8_%D0%90.%D0%98._%D0%91%D0%B5%D1%80%D1%91%D0%B7%D0%BE%D0%B2%D0%B0%D1%8F_%D1%80%D0%BE%D1%89%D0%B0.jpg`; page: `https://commons.wikimedia.org/wiki/File:0853Ha._%D0%9A%D1%83%D0%B8%D0%BD%D0%B4%D0%B6%D0%B8_%D0%90.%D0%98._%D0%91%D0%B5%D1%80%D1%91%D0%B7%D0%BE%D0%B2%D0%B0%D1%8F_%D1%80%D0%BE%D1%89%D0%B0.jpg`.
- Normalized gallery asset: `0853Ha. Куинджи А.И. Берёзовая роща.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/arkhip-kuindzhi`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 516. arkhip-kuindzhi / Red Sunset on the Dnieper

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `arkhip-kuindzhi` → `Red Sunset on the Dnieper`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Red_Sunset_on_the_Dnieper_MET_DT2557.jpg/500px-Red_Sunset_on_the_Dnieper_MET_DT2557.jpg`; page: `https://en.wikipedia.org/wiki/Red_Sunset_on_the_Dnipro`.
- Normalized gallery asset: `Red Sunset on the Dnieper MET DT2557.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/arkhip-kuindzhi`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 517. vasily-surikov / The Morning of the Streltsy Execution

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `vasily-surikov` → `The Morning of the Streltsy Execution`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Surikov_streltsi.jpg/500px-Surikov_streltsi.jpg`; page: `https://en.wikipedia.org/wiki/The_Morning_of_the_Streltsy_Execution`.
- Normalized gallery asset: `Surikov streltsi.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/vasily-surikov`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 518. vasily-surikov / Boyarynya Morozova

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `vasily-surikov` → `Boyarynya Morozova`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Vasily_Surikov_-_%D0%91%D0%BE%D1%8F%D1%80%D1%8B%D0%BD%D1%8F_%D0%9C%D0%BE%D1%80%D0%BE%D0%B7%D0%BE%D0%B2%D0%B0_-_Google_Art_Project_ed.jpg/500px-Vasily_Surikov_-_%D0%91%D0%BE%D1%8F%D1%80%D1%8B%D0%BD%D1%8F_%D0%9C%D0%BE%D1%80%D0%BE%D0%B7%D0%BE%D0%B2%D0%B0_-_Google_Art_Project_ed.jpg`; page: `https://commons.wikimedia.org/wiki/File:Vasily_Surikov_-_%D0%91%D0%BE%D1%8F%D1%80%D1%8B%D0%BD%D1%8F_%D0%9C%D0%BE%D1%80%D0%BE%D0%B7%D0%BE%D0%B2%D0%B0_-_Google_Art_Project_ed.jpg`.
- Normalized gallery asset: `Vasily Surikov - Боярыня Морозова - Google Art Project ed.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/vasily-surikov`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 519. vasily-surikov / Menshikov in Berezovo

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `vasily-surikov` → `Menshikov in Berezovo`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/SurikovMenshikovBerezovo.jpg/500px-SurikovMenshikovBerezovo.jpg`; page: `https://commons.wikimedia.org/wiki/File:SurikovMenshikovBerezovo.jpg`.
- Normalized gallery asset: `SurikovMenshikovBerezovo.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/vasily-surikov`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 520. valentin-serov / Girl with Peaches

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `valentin-serov` → `Girl with Peaches`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Walentin_Alexandrowitsch_Serow_Girl_with_Peaches.jpg/500px-Walentin_Alexandrowitsch_Serow_Girl_with_Peaches.jpg`; page: `https://en.wikipedia.org/wiki/Girl_with_Peaches`.
- Normalized gallery asset: `Walentin Alexandrowitsch Serow Girl with Peaches.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/valentin-serov`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 521. valentin-serov / Portrait of Ida Rubinstein

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `valentin-serov` → `Portrait of Ida Rubinstein`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Ida_Rubinstein_by_V._Serov_%28GRM%29_FRAME_by_shakko_01.jpg/500px-Ida_Rubinstein_by_V._Serov_%28GRM%29_FRAME_by_shakko_01.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ida_Rubinstein_by_V._Serov_(GRM)_FRAME_by_shakko_01.jpg`.
- Normalized gallery asset: `Ida Rubinstein by V. Serov (GRM) FRAME by shakko 01.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/valentin-serov`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 522. valentin-serov / The Abduction of Europa

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `valentin-serov` → `The Abduction of Europa`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/1910_Serow_Abduction_of_Eurpoa_anagoria.JPG/500px-1910_Serow_Abduction_of_Eurpoa_anagoria.JPG`; page: `https://commons.wikimedia.org/wiki/File:1910_Serow_Abduction_of_Eurpoa_anagoria.JPG`.
- Normalized gallery asset: `1910 Serow Abduction of Eurpoa anagoria.JPG`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/valentin-serov`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 523. fitz-henry-lane / Lumber Schooners at Evening on Penobscot Bay

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `fitz-henry-lane` → `Lumber Schooners at Evening on Penobscot Bay`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Fitz_Henry_Lane%2C_Lumber_Schooners_at_Evening_on_Penobscot_Bay%2C_1863%2C_NGA_57611.jpg/500px-Fitz_Henry_Lane%2C_Lumber_Schooners_at_Evening_on_Penobscot_Bay%2C_1863%2C_NGA_57611.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fitz_Henry_Lane,_Lumber_Schooners_at_Evening_on_Penobscot_Bay,_1863,_NGA_57611.jpg`.
- Normalized gallery asset: `Fitz Henry Lane, Lumber Schooners at Evening on Penobscot Bay, 1863, NGA 57611.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-4.js` / `lumber-schooners-penobscot-bay`; title `Lumber Schooners at Evening on Penobscot Bay`; worksKey `Lumber Schooners at Evening on Penobscot Bay`; artistId `fitz-henry-lane`. Evidence: same Commons asset `Fitz Henry Lane, Lumber Schooners at Evening on Penobscot Bay, 1863, NGA 57611.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Fitz_Henry_Lane%2C_Lumber_Schooners_at_Evening_on_Penobscot_Bay%2C_1863%2C_NGA_57611.jpg/500px-Fitz_Henry_Lane%2C_Lumber_Schooners_at_Evening_on_Penobscot_Bay%2C_1863%2C_NGA_57611.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fitz_Henry_Lane,_Lumber_Schooners_at_Evening_on_Penobscot_Bay,_1863,_NGA_57611.jpg`.
- Checked-in route `p/artwork/lumber-schooners-penobscot-bay.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Fitz_Henry_Lane%2C_Lumber_Schooners_at_Evening_on_Penobscot_Bay%2C_1863%2C_NGA_57611.jpg/500px-Fitz_Henry_Lane%2C_Lumber_Schooners_at_Evening_on_Penobscot_Bay%2C_1863%2C_NGA_57611.jpg`.

### 524. fitz-henry-lane / Boston Harbor, Sunset

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `fitz-henry-lane` → `Boston Harbor, Sunset`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Boston_Harbor%2C_Sunset_LACMA_AC1993.229.1.jpg/500px-Boston_Harbor%2C_Sunset_LACMA_AC1993.229.1.jpg`; page: `https://commons.wikimedia.org/wiki/File:Boston_Harbor,_Sunset_LACMA_AC1993.229.1.jpg`.
- Normalized gallery asset: `Boston Harbor, Sunset LACMA AC1993.229.1.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/fitz-henry-lane`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 525. fitz-henry-lane / Owl's Head, Penobscot Bay, Maine

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `fitz-henry-lane` → `Owl's Head, Penobscot Bay, Maine`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Fitz_Henry_Lane_-_Owl%27s_Head%2C_Penobscot_Bay%2C_Maine_-_Google_Art_Project.jpg/500px-Fitz_Henry_Lane_-_Owl%27s_Head%2C_Penobscot_Bay%2C_Maine_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fitz_Henry_Lane_-_Owl%27s_Head,_Penobscot_Bay,_Maine_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Fitz Henry Lane - Owl's Head, Penobscot Bay, Maine - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/fitz-henry-lane`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 526. fitz-henry-lane / Brace's Rock

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `fitz-henry-lane` → `Brace's Rock`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Brace%27s_Rock%2C_by_Fitz_Henry_Lane%2C_1864%2C_oil_on_canvas_-_Cape_Ann_Museum_-_Gloucester%2C_MA_-_DSC01239.jpg/500px-Brace%27s_Rock%2C_by_Fitz_Henry_Lane%2C_1864%2C_oil_on_canvas_-_Cape_Ann_Museum_-_Gloucester%2C_MA_-_DSC01239.jpg`; page: `https://commons.wikimedia.org/wiki/File:Brace%27s_Rock,_by_Fitz_Henry_Lane,_1864,_oil_on_canvas_-_Cape_Ann_Museum_-_Gloucester,_MA_-_DSC01239.jpg`.
- Normalized gallery asset: `Brace's Rock, by Fitz Henry Lane, 1864, oil on canvas - Cape Ann Museum - Gloucester, MA - DSC01239.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/fitz-henry-lane`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 527. giovanni-bellini / Doge Leonardo Loredan

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `giovanni-bellini` → `Doge Leonardo Loredan`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Giovanni_Bellini%2C_portrait_of_Doge_Leonardo_Loredan.jpg/500px-Giovanni_Bellini%2C_portrait_of_Doge_Leonardo_Loredan.jpg`; page: `https://commons.wikimedia.org/wiki/File:Giovanni_Bellini,_portrait_of_Doge_Leonardo_Loredan.jpg`.
- Normalized gallery asset: `Giovanni Bellini, portrait of Doge Leonardo Loredan.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-7.js` / `portrait-of-doge-leonardo-loredan`; title `Portrait of Doge Leonardo Loredan`; worksKey `Doge Leonardo Loredan`; artistId `giovanni-bellini`. Evidence: same Commons asset `Giovanni Bellini, portrait of Doge Leonardo Loredan.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Giovanni_Bellini%2C_portrait_of_Doge_Leonardo_Loredan.jpg/500px-Giovanni_Bellini%2C_portrait_of_Doge_Leonardo_Loredan.jpg`; page: `https://commons.wikimedia.org/wiki/File:Giovanni_Bellini,_portrait_of_Doge_Leonardo_Loredan.jpg`.
- Checked-in route `p/artwork/portrait-of-doge-leonardo-loredan.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Giovanni_Bellini%2C_portrait_of_Doge_Leonardo_Loredan.jpg/500px-Giovanni_Bellini%2C_portrait_of_Doge_Leonardo_Loredan.jpg`.

### 528. giovanni-bellini / St Francis in the Desert

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giovanni-bellini` → `St Francis in the Desert`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Giovanni_Bellini_St_Francis_in_Ecstasy.jpg/500px-Giovanni_Bellini_St_Francis_in_Ecstasy.jpg`; page: `https://commons.wikimedia.org/wiki/File:Giovanni_Bellini_St_Francis_in_Ecstasy.jpg`.
- Normalized gallery asset: `Giovanni Bellini St Francis in Ecstasy.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giovanni-bellini`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 529. giovanni-bellini / San Zaccaria Altarpiece

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giovanni-bellini` → `San Zaccaria Altarpiece`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Pala_di_san_zaccaria_01.jpg/500px-Pala_di_san_zaccaria_01.jpg`; page: `https://commons.wikimedia.org/wiki/File:Pala_di_san_zaccaria_01.jpg`.
- Normalized gallery asset: `Pala di san zaccaria 01.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giovanni-bellini`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 530. giovanni-bellini / The Feast of the Gods

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giovanni-bellini` → `The Feast of the Gods`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Feast_of_the_Gods_Giovanni_Bellini_1514.jpg/500px-Feast_of_the_Gods_Giovanni_Bellini_1514.jpg`; page: `https://commons.wikimedia.org/wiki/File:Feast_of_the_Gods_Giovanni_Bellini_1514.jpg`.
- Normalized gallery asset: `Feast of the Gods Giovanni Bellini 1514.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giovanni-bellini`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 531. andrea-del-verrocchio / The Baptism of Christ

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `andrea-del-verrocchio` → `The Baptism of Christ`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Andrea_del_Verrocchio%2C_Leonardo_da_Vinci_-_Baptism_of_Christ_-_Uffizi.jpg/500px-Andrea_del_Verrocchio%2C_Leonardo_da_Vinci_-_Baptism_of_Christ_-_Uffizi.jpg`; page: `https://commons.wikimedia.org/wiki/File:Andrea_del_Verrocchio,_Leonardo_da_Vinci_-_Baptism_of_Christ_-_Uffizi.jpg`.
- Normalized gallery asset: `Andrea del Verrocchio, Leonardo da Vinci - Baptism of Christ - Uffizi.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/andrea-del-verrocchio`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 532. andrea-del-verrocchio / Madonna and Child

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `andrea-del-verrocchio` → `Madonna and Child`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Madonna-with-Child-by-Verrocchio.jpg/500px-Madonna-with-Child-by-Verrocchio.jpg`; page: `https://commons.wikimedia.org/wiki/File:Madonna-with-Child-by-Verrocchio.jpg`.
- Normalized gallery asset: `Madonna-with-Child-by-Verrocchio.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/andrea-del-verrocchio`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 533. andrea-del-verrocchio / Tobias and the Angel

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `andrea-del-verrocchio` → `Tobias and the Angel`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Workshop_of_Andrea_del_Verrocchio._Tobias_and_the_Angel._33x26cm._1470-75._NG_London.jpg/500px-Workshop_of_Andrea_del_Verrocchio._Tobias_and_the_Angel._33x26cm._1470-75._NG_London.jpg`; page: `https://commons.wikimedia.org/wiki/File:Workshop_of_Andrea_del_Verrocchio._Tobias_and_the_Angel._33x26cm._1470-75._NG_London.jpg`.
- Normalized gallery asset: `Workshop of Andrea del Verrocchio. Tobias and the Angel. 33x26cm. 1470-75. NG London.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/andrea-del-verrocchio`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 534. giorgio-vasari / Six Tuscan Poets

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giorgio-vasari` → `Six Tuscan Poets`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Italien_humanists_by_Giorgio_Vasari.jpg/500px-Italien_humanists_by_Giorgio_Vasari.jpg`; page: `https://commons.wikimedia.org/wiki/File:Italien_humanists_by_Giorgio_Vasari.jpg`.
- Normalized gallery asset: `Italien humanists by Giorgio Vasari.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giorgio-vasari`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 535. giorgio-vasari / Self-Portrait

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giorgio-vasari` → `Self-Portrait`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Giorgio_Vasari_-_Self-Portrait_-_WGA24284.jpg/500px-Giorgio_Vasari_-_Self-Portrait_-_WGA24284.jpg`; page: `https://commons.wikimedia.org/wiki/File:Giorgio_Vasari_-_Self-Portrait_-_WGA24284.jpg`.
- Normalized gallery asset: `Giorgio Vasari - Self-Portrait - WGA24284.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giorgio-vasari`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 536. giorgio-vasari / Portrait of Lorenzo de' Medici

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giorgio-vasari` → `Portrait of Lorenzo de' Medici`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Vasari-Lorenzo.jpg/500px-Vasari-Lorenzo.jpg`; page: `https://commons.wikimedia.org/wiki/File:Vasari-Lorenzo.jpg`.
- Normalized gallery asset: `Vasari-Lorenzo.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giorgio-vasari`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 537. giorgio-vasari / Perseus and Andromeda

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `giorgio-vasari` → `Perseus and Andromeda`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Vasari%2C_perseo_e_andromeda%2C_studiolo.jpg/500px-Vasari%2C_perseo_e_andromeda%2C_studiolo.jpg`; page: `https://commons.wikimedia.org/wiki/File:Vasari,_perseo_e_andromeda,_studiolo.jpg`.
- Normalized gallery asset: `Vasari, perseo e andromeda, studiolo.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/giorgio-vasari`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 538. jean-leon-gerome / The Snake Charmer

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jean-leon-gerome` → `The Snake Charmer`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Jean-L%C3%A9on_G%C3%A9r%C3%B4me_-_Le_charmeur_de_serpents.jpg/500px-Jean-L%C3%A9on_G%C3%A9r%C3%B4me_-_Le_charmeur_de_serpents.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jean-L%C3%A9on_G%C3%A9r%C3%B4me_-_Le_charmeur_de_serpents.jpg`.
- Normalized gallery asset: `Jean-Léon Gérôme - Le charmeur de serpents.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jean-leon-gerome`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 539. jean-leon-gerome / Pollice Verso

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `jean-leon-gerome` → `Pollice Verso`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Jean-Leon_Gerome_Pollice_Verso.jpg/500px-Jean-Leon_Gerome_Pollice_Verso.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jean-Leon_Gerome_Pollice_Verso.jpg`.
- Normalized gallery asset: `Jean-Leon Gerome Pollice Verso.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-6.js` / `pollice-verso`; title `Pollice Verso`; worksKey `(absent)`; artistId `jean-leon-gerome`. Evidence: same Commons asset `Jean-Leon Gerome Pollice Verso.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Jean-Leon_Gerome_Pollice_Verso.jpg/500px-Jean-Leon_Gerome_Pollice_Verso.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jean-Leon_Gerome_Pollice_Verso.jpg`.
- Checked-in route `p/artwork/pollice-verso.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Jean-Leon_Gerome_Pollice_Verso.jpg/500px-Jean-Leon_Gerome_Pollice_Verso.jpg`.

### 540. jean-leon-gerome / Bonaparte Before the Sphinx

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jean-leon-gerome` → `Bonaparte Before the Sphinx`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Jean-L%C3%A9on_G%C3%A9r%C3%B4me_-_Bonaparte_Before_the_Sphinx.jpg/500px-Jean-L%C3%A9on_G%C3%A9r%C3%B4me_-_Bonaparte_Before_the_Sphinx.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jean-L%C3%A9on_G%C3%A9r%C3%B4me_-_Bonaparte_Before_the_Sphinx.jpg`.
- Normalized gallery asset: `Jean-Léon Gérôme - Bonaparte Before the Sphinx.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jean-leon-gerome`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 541. jean-leon-gerome / Cleopatra and Caesar

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jean-leon-gerome` → `Cleopatra and Caesar`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Cleopatra_and_Caesar_by_Jean-Leon-Gerome.jpg/500px-Cleopatra_and_Caesar_by_Jean-Leon-Gerome.jpg`; page: `https://commons.wikimedia.org/wiki/File:Cleopatra_and_Caesar_by_Jean-Leon-Gerome.jpg`.
- Normalized gallery asset: `Cleopatra and Caesar by Jean-Leon-Gerome.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jean-leon-gerome`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 542. jose-clemente-orozco / Zapatistas

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jose-clemente-orozco` → `Zapatistas`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jos%C3%A9_Clemente_Orozco%2C_Zapatistas%2C_1931%2C_MoMA.jpg/500px-Jos%C3%A9_Clemente_Orozco%2C_Zapatistas%2C_1931%2C_MoMA.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jos%C3%A9_Clemente_Orozco,_Zapatistas,_1931,_MoMA.jpg`.
- Normalized gallery asset: `José Clemente Orozco, Zapatistas, 1931, MoMA.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jose-clemente-orozco`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 543. jose-clemente-orozco / Prometheus

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jose-clemente-orozco` → `Prometheus`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Prometheus_%281930%29_de_Jos%C3%A9_Clemente_Orozco_en_Pomona_College.jpg/500px-Prometheus_%281930%29_de_Jos%C3%A9_Clemente_Orozco_en_Pomona_College.jpg`; page: `https://commons.wikimedia.org/wiki/File:Prometheus_(1930)_de_Jos%C3%A9_Clemente_Orozco_en_Pomona_College.jpg`.
- Normalized gallery asset: `Prometheus (1930) de José Clemente Orozco en Pomona College.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jose-clemente-orozco`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 544. jose-clemente-orozco / Barricade

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jose-clemente-orozco` → `Barricade`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Jos%C3%A9_Clemente_Orozco%2C_Barricade.jpg/500px-Jos%C3%A9_Clemente_Orozco%2C_Barricade.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jos%C3%A9_Clemente_Orozco,_Barricade.jpg`.
- Normalized gallery asset: `José Clemente Orozco, Barricade.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jose-clemente-orozco`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 545. jose-clemente-orozco / The Subway

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jose-clemente-orozco` → `The Subway`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Jos%C3%A9_Clemente_Orozco%2C_The_Subway.jpg/500px-Jos%C3%A9_Clemente_Orozco%2C_The_Subway.jpg`; page: `https://commons.wikimedia.org/wiki/File:Jos%C3%A9_Clemente_Orozco,_The_Subway.jpg`.
- Normalized gallery asset: `José Clemente Orozco, The Subway.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jose-clemente-orozco`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 546. jozef-mehoffer / Strange Garden

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jozef-mehoffer` → `Strange Garden`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/J%C3%B3zef_Mehoffer_-_Dziwny_ogr%C3%B3d.jpg/500px-J%C3%B3zef_Mehoffer_-_Dziwny_ogr%C3%B3d.jpg`; page: `https://commons.wikimedia.org/wiki/File:J%C3%B3zef_Mehoffer_-_Dziwny_ogr%C3%B3d.jpg`.
- Normalized gallery asset: `Józef Mehoffer - Dziwny ogród.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jozef-mehoffer`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 547. jozef-mehoffer / Zinnias

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jozef-mehoffer` → `Zinnias`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/J%C3%B3zef_Mehoffer_-_Zinnias_-_MP_4274_MNW_-_National_Museum_in_Warsaw.jpg/500px-J%C3%B3zef_Mehoffer_-_Zinnias_-_MP_4274_MNW_-_National_Museum_in_Warsaw.jpg`; page: `https://commons.wikimedia.org/wiki/File:J%C3%B3zef_Mehoffer_-_Zinnias_-_MP_4274_MNW_-_National_Museum_in_Warsaw.jpg`.
- Normalized gallery asset: `Józef Mehoffer - Zinnias - MP 4274 MNW - National Museum in Warsaw.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jozef-mehoffer`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 548. jozef-mehoffer / Self-Portrait

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jozef-mehoffer` → `Self-Portrait`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/J%C3%B3zef_Mehoffer_-_Self-portrait_-_MP_403_MNW_-_National_Museum_in_Warsaw.jpg/500px-J%C3%B3zef_Mehoffer_-_Self-portrait_-_MP_403_MNW_-_National_Museum_in_Warsaw.jpg`; page: `https://commons.wikimedia.org/wiki/File:J%C3%B3zef_Mehoffer_-_Self-portrait_-_MP_403_MNW_-_National_Museum_in_Warsaw.jpg`.
- Normalized gallery asset: `Józef Mehoffer - Self-portrait - MP 403 MNW - National Museum in Warsaw.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jozef-mehoffer`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 549. john-frederick-lewis / The Reception

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `john-frederick-lewis` → `The Reception`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/John_frederick_lewis-reception1873.jpg/500px-John_frederick_lewis-reception1873.jpg`; page: `https://commons.wikimedia.org/wiki/File:John_frederick_lewis-reception1873.jpg`.
- Normalized gallery asset: `John frederick lewis-reception1873.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/john-frederick-lewis`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 550. john-frederick-lewis / Indoor Gossip, Cairo

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `john-frederick-lewis` → `Indoor Gossip, Cairo`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/John_Frederick_Lewis_%281804-1876%29_-_Indoor_Gossip%2C_Cairo_-_O.1961.1_-_Whitworth_Art_Gallery.jpg/500px-John_Frederick_Lewis_%281804-1876%29_-_Indoor_Gossip%2C_Cairo_-_O.1961.1_-_Whitworth_Art_Gallery.jpg`; page: `https://commons.wikimedia.org/wiki/File:John_Frederick_Lewis_(1804-1876)_-_Indoor_Gossip,_Cairo_-_O.1961.1_-_Whitworth_Art_Gallery.jpg`.
- Normalized gallery asset: `John Frederick Lewis (1804-1876) - Indoor Gossip, Cairo - O.1961.1 - Whitworth Art Gallery.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/john-frederick-lewis`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 551. john-frederick-lewis / Hhareem Life, Constantinople

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `john-frederick-lewis` → `Hhareem Life, Constantinople`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/John_Frederick_Lewis_-_Hhareem_Life%2C_Constantinople.jpg/500px-John_Frederick_Lewis_-_Hhareem_Life%2C_Constantinople.jpg`; page: `https://commons.wikimedia.org/wiki/File:John_Frederick_Lewis_-_Hhareem_Life,_Constantinople.jpg`.
- Normalized gallery asset: `John Frederick Lewis - Hhareem Life, Constantinople.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/john-frederick-lewis`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 552. john-frederick-lewis / Sheik Hussein of Gebel Tor

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `john-frederick-lewis` → `Sheik Hussein of Gebel Tor`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/John_Frederick_Lewis_-_Sheik_Hussein_of_Gebel_Tor_and_His_Son_-_Google_Art_Project.jpg/500px-John_Frederick_Lewis_-_Sheik_Hussein_of_Gebel_Tor_and_His_Son_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:John_Frederick_Lewis_-_Sheik_Hussein_of_Gebel_Tor_and_His_Son_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `John Frederick Lewis - Sheik Hussein of Gebel Tor and His Son - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/john-frederick-lewis`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 553. ludwig-deutsch / The Palace Guard

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ludwig-deutsch` → `The Palace Guard`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Ludwig_Deutsch-_The_Palace_Guard.jpg/500px-Ludwig_Deutsch-_The_Palace_Guard.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ludwig_Deutsch-_The_Palace_Guard.jpg`.
- Normalized gallery asset: `Ludwig Deutsch- The Palace Guard.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ludwig-deutsch`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 554. ludwig-deutsch / The Girl with the Buffalo

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ludwig-deutsch` → `The Girl with the Buffalo`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Ludwig_Deutsch_-_The_Girl_with_the_Buffalo.jpg/500px-Ludwig_Deutsch_-_The_Girl_with_the_Buffalo.jpg`; page: `https://commons.wikimedia.org/wiki/File:Ludwig_Deutsch_-_The_Girl_with_the_Buffalo.jpg`.
- Normalized gallery asset: `Ludwig Deutsch - The Girl with the Buffalo.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ludwig-deutsch`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 555. fan-kuan / Travelers among Mountains and Streams

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `fan-kuan` → `Travelers among Mountains and Streams`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Fan_Kuan_-_Travelers_Among_Mountains_and_Streams_-_Google_Art_Project.jpg/500px-Fan_Kuan_-_Travelers_Among_Mountains_and_Streams_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fan_Kuan_-_Travelers_Among_Mountains_and_Streams_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Fan Kuan - Travelers Among Mountains and Streams - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-9.js` / `travelers-among-mountains-and-streams`; title `Travelers among Mountains and Streams`; worksKey `(absent)`; artistId `fan-kuan`. Evidence: same Commons asset `Fan Kuan - Travelers Among Mountains and Streams - Google Art Project.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Fan_Kuan_-_Travelers_Among_Mountains_and_Streams_-_Google_Art_Project.jpg/500px-Fan_Kuan_-_Travelers_Among_Mountains_and_Streams_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fan_Kuan_-_Travelers_Among_Mountains_and_Streams_-_Google_Art_Project.jpg`.
- Checked-in route `p/artwork/travelers-among-mountains-and-streams.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Fan_Kuan_-_Travelers_Among_Mountains_and_Streams_-_Google_Art_Project.jpg/500px-Fan_Kuan_-_Travelers_Among_Mountains_and_Streams_-_Google_Art_Project.jpg`.

### 556. fan-kuan / Sitting Alone by a Stream

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `fan-kuan` → `Sitting Alone by a Stream`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Fan_Kuan-Sitting_Alone_by_a_Stream.jpg/500px-Fan_Kuan-Sitting_Alone_by_a_Stream.jpg`; page: `https://commons.wikimedia.org/wiki/File:Fan_Kuan-Sitting_Alone_by_a_Stream.jpg`.
- Normalized gallery asset: `Fan Kuan-Sitting Alone by a Stream.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/fan-kuan`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 557. guo-xi / Early Spring

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `guo-xi` → `Early Spring`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Guo_Xi_-_Early_Spring_%28large%29.jpg/500px-Guo_Xi_-_Early_Spring_%28large%29.jpg`; page: `https://en.wikipedia.org/wiki/Early_Spring_(painting)`.
- Normalized gallery asset: `Guo Xi - Early Spring (large).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-8.js` / `early-spring`; title `Early Spring`; worksKey `(absent)`; artistId `guo-xi`. Evidence: same Commons asset `Guo Xi - Early Spring (large).jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Guo_Xi_-_Early_Spring_%28large%29.jpg/500px-Guo_Xi_-_Early_Spring_%28large%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Guo_Xi_-_Early_Spring_(large).jpg`.
- Checked-in route `p/artwork/early-spring.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Guo_Xi_-_Early_Spring_%28large%29.jpg/500px-Guo_Xi_-_Early_Spring_%28large%29.jpg`.

### 558. guo-xi / Old Trees, Level Distance

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `guo-xi` → `Old Trees, Level Distance`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/%E5%8C%97%E5%AE%8B_%E9%83%AD%E7%86%99_%E6%A8%B9%E8%89%B2%E5%B9%B3%E9%81%A0%E5%9C%96_%E5%8D%B7_-Old_Trees%2C_Level_Distance_MET_DP167812_CRD.jpg/500px-%E5%8C%97%E5%AE%8B_%E9%83%AD%E7%86%99_%E6%A8%B9%E8%89%B2%E5%B9%B3%E9%81%A0%E5%9C%96_%E5%8D%B7_-Old_Trees%2C_Level_Distance_MET_DP167812_CRD.jpg`; page: `https://en.wikipedia.org/wiki/Old_Trees%2C_Level_Distance`.
- Normalized gallery asset: `北宋 郭熙 樹色平遠圖 卷 -Old Trees, Level Distance MET DP167812 CRD.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/guo-xi`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 559. guo-xi / Deep Valley

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `guo-xi` → `Deep Valley`; img: `https://upload.wikimedia.org/wikipedia/commons/8/80/Deep_Valley.jpg`; page: `https://commons.wikimedia.org/wiki/File:Deep_Valley.jpg`.
- Normalized gallery asset: `Deep Valley.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/guo-xi`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 560. huang-gongwang / Dwelling in the Fuchun Mountains

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `huang-gongwang` → `Dwelling in the Fuchun Mountains`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Dwelling_in_the_Fuchun_Mountains_%28first_half%29.JPG/500px-Dwelling_in_the_Fuchun_Mountains_%28first_half%29.JPG`; page: `https://en.wikipedia.org/wiki/Dwelling_in_the_Fuchun_Mountains`.
- Normalized gallery asset: `Dwelling in the Fuchun Mountains (first half).JPG`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/huang-gongwang`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 561. huang-gongwang / Stone Cliff at the Pond of Heaven

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `huang-gongwang` → `Stone Cliff at the Pond of Heaven`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Huang_Gongwang._Stone_Cliff_at_the_Pond_of_Heaven.1341._139%2C4x57%2C3._Palace_Museum%2C_Beijing.jpg/500px-Huang_Gongwang._Stone_Cliff_at_the_Pond_of_Heaven.1341._139%2C4x57%2C3._Palace_Museum%2C_Beijing.jpg`; page: `https://commons.wikimedia.org/wiki/File:Huang_Gongwang._Stone_Cliff_at_the_Pond_of_Heaven.1341._139,4x57,3._Palace_Museum,_Beijing.jpg`.
- Normalized gallery asset: `Huang Gongwang. Stone Cliff at the Pond of Heaven.1341. 139,4x57,3. Palace Museum, Beijing.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/huang-gongwang`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 562. kamal-ud-din-behzad / The Seduction of Yusuf

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kamal-ud-din-behzad` → `The Seduction of Yusuf`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Yusuf_fleeing_the_Advances_of_Zulaikha.jpg/500px-Yusuf_fleeing_the_Advances_of_Zulaikha.jpg`; page: `https://commons.wikimedia.org/wiki/File:Yusuf_fleeing_the_Advances_of_Zulaikha.jpg`.
- Normalized gallery asset: `Yusuf fleeing the Advances of Zulaikha.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kamal-ud-din-behzad`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 563. kamal-ud-din-behzad / Construction of the Castle of Khawarnaq

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kamal-ud-din-behzad` → `Construction of the Castle of Khawarnaq`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Kamal-ud-din_Bihzad_-_Construction_of_the_fort_of_Kharnaq.jpg/500px-Kamal-ud-din_Bihzad_-_Construction_of_the_fort_of_Kharnaq.jpg`; page: `https://commons.wikimedia.org/wiki/File:Kamal-ud-din_Bihzad_-_Construction_of_the_fort_of_Kharnaq.jpg`.
- Normalized gallery asset: `Kamal-ud-din Bihzad - Construction of the fort of Kharnaq.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kamal-ud-din-behzad`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 564. abd-al-samad / Akbar Presents a Painting to His Father Humayun

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `abd-al-samad` → `Akbar Presents a Painting to His Father Humayun`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/%E2%80%98Abd_al-Samad._Akbar_Presents_a_Painting_to_His_Father_Humayun._Mughal%2C_probably_Kabul%2C_c._1550%E2%80%931556._Golestan_Palace_Library%2C_Tehran.jpg/500px-%E2%80%98Abd_al-Samad._Akbar_Presents_a_Painting_to_His_Father_Humayun._Mughal%2C_probably_Kabul%2C_c._1550%E2%80%931556._Golestan_Palace_Library%2C_Tehran.jpg`; page: `https://commons.wikimedia.org/wiki/File:%E2%80%98Abd_al-Samad._Akbar_Presents_a_Painting_to_His_Father_Humayun._Mughal,_probably_Kabul,_c._1550%E2%80%931556._Golestan_Palace_Library,_Tehran.jpg`.
- Normalized gallery asset: `‘Abd al-Samad. Akbar Presents a Painting to His Father Humayun. Mughal, probably Kabul, c. 1550–1556. Golestan Palace Library, Tehran.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/abd-al-samad`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 565. abd-al-samad / Princes of the House of Timur

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `abd-al-samad` → `Princes of the House of Timur`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Princes_of_the_House_of_Timur.jpg/500px-Princes_of_the_House_of_Timur.jpg`; page: `https://en.wikipedia.org/wiki/Princes_of_the_House_of_Timur`.
- Normalized gallery asset: `Princes of the House of Timur.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-9.js` / `princes-of-the-house-of-timur`; title `Princes of the House of Timur`; worksKey `(absent)`; artistId `abd-al-samad`. Evidence: same Commons asset `Princes of the House of Timur.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Princes_of_the_House_of_Timur.jpg/500px-Princes_of_the_House_of_Timur.jpg`; page: `https://commons.wikimedia.org/wiki/File:Princes_of_the_House_of_Timur.jpg`.
- Checked-in route `p/artwork/princes-of-the-house-of-timur.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Princes_of_the_House_of_Timur.jpg/500px-Princes_of_the_House_of_Timur.jpg`.

### 566. basawan / Akbarnama illustrations

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `basawan` → `Akbarnama illustrations`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Basawan._Battle_of_rival_ascetics._Akbarnama%2C_ca._1590%2C_V%26A_Museum.jpg/500px-Basawan._Battle_of_rival_ascetics._Akbarnama%2C_ca._1590%2C_V%26A_Museum.jpg`; page: `https://commons.wikimedia.org/wiki/File:Basawan._Battle_of_rival_ascetics._Akbarnama,_ca._1590,_V%26A_Museum.jpg`.
- Normalized gallery asset: `Basawan. Battle of rival ascetics. Akbarnama, ca. 1590, V&A Museum.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/basawan`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 567. ustad-mansur / Turkey Cock

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ustad-mansur` → `Turkey Cock`; img: `https://upload.wikimedia.org/wikipedia/commons/5/52/Turkey_Cock%2C_by_Mansur%2C_opaque_watercolour_and_gold_on_paper%2C_Mughal%2C_ca._1612.jpg`; page: `https://commons.wikimedia.org/wiki/File:Turkey_Cock,_by_Mansur,_opaque_watercolour_and_gold_on_paper,_Mughal,_ca._1612.jpg`.
- Normalized gallery asset: `Turkey Cock, by Mansur, opaque watercolour and gold on paper, Mughal, ca. 1612.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ustad-mansur`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 568. ustad-mansur / Chameleon

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `ustad-mansur` → `Chameleon`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/A_chameleon_by_Ustad_Mansur.jpg/500px-A_chameleon_by_Ustad_Mansur.jpg`; page: `https://commons.wikimedia.org/wiki/File:A_chameleon_by_Ustad_Mansur.jpg`.
- Normalized gallery asset: `A chameleon by Ustad Mansur.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/ustad-mansur`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 569. an-gyeon / Dream Journey to the Peach Blossom Land

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `an-gyeon` → `Dream Journey to the Peach Blossom Land`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Dream_Journey_to_the_Peach_Blossom_Land.jpg/500px-Dream_Journey_to_the_Peach_Blossom_Land.jpg`; page: `https://commons.wikimedia.org/wiki/File:Dream_Journey_to_the_Peach_Blossom_Land.jpg`.
- Normalized gallery asset: `Dream Journey to the Peach Blossom Land.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/an-gyeon`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 570. jeong-seon / Inwangjesaekdo

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jeong-seon` → `Inwangjesaekdo`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Inwangjesaekdo.jpg/500px-Inwangjesaekdo.jpg`; page: `https://en.wikipedia.org/wiki/Inwang_jesaekdo`.
- Normalized gallery asset: `Inwangjesaekdo.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jeong-seon`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 571. jeong-seon / Geumgang jeondo

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `jeong-seon` → `Geumgang jeondo`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Geumgangjeondo.jpg/500px-Geumgangjeondo.jpg`; page: `https://en.wikipedia.org/wiki/Geumgang_jeondo`.
- Normalized gallery asset: `Geumgangjeondo.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/jeong-seon`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 572. kano-eitoku / Cypress Trees

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kano-eitoku` → `Cypress Trees`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Kano_Eitoku_-_Cypress_Trees.jpg/500px-Kano_Eitoku_-_Cypress_Trees.jpg`; page: `https://en.wikipedia.org/wiki/Cypress_Trees`.
- Normalized gallery asset: `Kano Eitoku - Cypress Trees.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kano-eitoku`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 573. kano-eitoku / Chinese Lions

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `kano-eitoku` → `Chinese Lions`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Kano_Eitoku_002.jpg/500px-Kano_Eitoku_002.jpg`; page: `https://commons.wikimedia.org/wiki/File:Kano_Eitoku_002.jpg`.
- Normalized gallery asset: `Kano Eitoku 002.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/kano-eitoku`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 574. hasegawa-tohaku / Pine Trees

- Classification: **EXACT ASSET**.
- Gallery source: `js/artworks.js` → `hasegawa-tohaku` → `Pine Trees`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Hasegawa_Tohaku_-_Pine_Trees_%28Sh%C5%8Drin-zu_by%C5%8Dbu%29_-_left_hand_screen.jpg/500px-Hasegawa_Tohaku_-_Pine_Trees_%28Sh%C5%8Drin-zu_by%C5%8Dbu%29_-_left_hand_screen.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hasegawa_Tohaku_-_Pine_Trees_(Sh%C5%8Drin-zu_by%C5%8Dbu)_-_left_hand_screen.jpg`.
- Normalized gallery asset: `Hasegawa Tohaku - Pine Trees (Shōrin-zu byōbu) - left hand screen.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- Catalog: `js/catalog-9.js` / `pine-trees-tohaku`; title `Pine Trees`; worksKey `Pine Trees`; artistId `hasegawa-tohaku`. Evidence: same Commons asset `Hasegawa Tohaku - Pine Trees (Shōrin-zu byōbu) - left hand screen.jpg`.
- Catalog image.status: `pd`; eligibility: **eligible**; src: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Hasegawa_Tohaku_-_Pine_Trees_%28Sh%C5%8Drin-zu_by%C5%8Dbu%29_-_left_hand_screen.jpg/500px-Hasegawa_Tohaku_-_Pine_Trees_%28Sh%C5%8Drin-zu_by%C5%8Dbu%29_-_left_hand_screen.jpg`; page: `https://commons.wikimedia.org/wiki/File:Hasegawa_Tohaku_-_Pine_Trees_(Sh%C5%8Drin-zu_by%C5%8Dbu)_-_left_hand_screen.jpg`.
- Checked-in route `p/artwork/pine-trees-tohaku.html` — og:image: `https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Hasegawa_Tohaku_-_Pine_Trees_%28Sh%C5%8Drin-zu_by%C5%8Dbu%29_-_left_hand_screen.jpg/500px-Hasegawa_Tohaku_-_Pine_Trees_%28Sh%C5%8Drin-zu_by%C5%8Dbu%29_-_left_hand_screen.jpg`.

### 575. hasegawa-tohaku / Pine Tree and Flowering Plants

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `hasegawa-tohaku` → `Pine Tree and Flowering Plants`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Pine_tree_Flowering_plants_Chishakuin_Tohaku.JPG/500px-Pine_tree_Flowering_plants_Chishakuin_Tohaku.JPG`; page: `https://commons.wikimedia.org/wiki/File:Pine_tree_Flowering_plants_Chishakuin_Tohaku.JPG`.
- Normalized gallery asset: `Pine tree Flowering plants Chishakuin Tohaku.JPG`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/hasegawa-tohaku`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 576. raden-saleh / The Arrest of Prince Diponegoro

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `raden-saleh` → `The Arrest of Prince Diponegoro`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Raden_Saleh_-_Diponegoro_arrest.jpg/500px-Raden_Saleh_-_Diponegoro_arrest.jpg`; page: `https://en.wikipedia.org/wiki/The_Arrest_of_Pangeran_Diponegoro`.
- Normalized gallery asset: `Raden Saleh - Diponegoro arrest.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/raden-saleh`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 577. raden-saleh / Boschbrand

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `raden-saleh` → `Boschbrand`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Forest_fire%2C_by_Raden_Saleh.jpg/500px-Forest_fire%2C_by_Raden_Saleh.jpg`; page: `https://commons.wikimedia.org/wiki/File:Forest_fire,_by_Raden_Saleh.jpg`.
- Normalized gallery asset: `Forest fire, by Raden Saleh.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/raden-saleh`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 578. raden-saleh / Lion Hunt

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `raden-saleh` → `Lion Hunt`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Raden_Saleh_-_The_Lion_hunt_%281841%29.jpg/500px-Raden_Saleh_-_The_Lion_hunt_%281841%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Raden_Saleh_-_The_Lion_hunt_(1841).jpg`.
- Normalized gallery asset: `Raden Saleh - The Lion hunt (1841).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/raden-saleh`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 579. miguel-cabrera / Portrait of Sor Juana Inés de la Cruz

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `miguel-cabrera` → `Portrait of Sor Juana Inés de la Cruz`; img: `https://upload.wikimedia.org/wikipedia/commons/3/3d/Retrato_de_Sor_Juana_In%C3%A9s_de_la_Cruz_%28Miguel_Cabrera%29.jpg`; page: `https://commons.wikimedia.org/wiki/File:Retrato_de_Sor_Juana_In%C3%A9s_de_la_Cruz_(Miguel_Cabrera).jpg`.
- Normalized gallery asset: `Retrato de Sor Juana Inés de la Cruz (Miguel Cabrera).jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/miguel-cabrera`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 580. miguel-cabrera / Casta painting

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `miguel-cabrera` → `Casta painting`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/De_espa%C3%B1ol_y_negra%2C_mulata.jpg/500px-De_espa%C3%B1ol_y_negra%2C_mulata.jpg`; page: `https://commons.wikimedia.org/wiki/File:De_espa%C3%B1ol_y_negra,_mulata.jpg`.
- Normalized gallery asset: `De español y negra, mulata.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/miguel-cabrera`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

### 581. miguel-cabrera / Virgin of Guadalupe

- Classification: **UNMATCHED**.
- Gallery source: `js/artworks.js` → `miguel-cabrera` → `Virgin of Guadalupe`; img: `https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Miguel_Cabrera_-_Altarpiece_of_the_Virgin_of_Guadalupe_with_Saint_John_the_Baptist%2C_Fray_Juan_de_Zum%C3%A1rraga_and_Juan_Diego_-_Google_Art_Project.jpg/500px-Miguel_Cabrera_-_Altarpiece_of_the_Virgin_of_Guadalupe_with_Saint_John_the_Baptist%2C_Fray_Juan_de_Zum%C3%A1rraga_and_Juan_Diego_-_Google_Art_Project.jpg`; page: `https://commons.wikimedia.org/wiki/File:Miguel_Cabrera_-_Altarpiece_of_the_Virgin_of_Guadalupe_with_Saint_John_the_Baptist,_Fray_Juan_de_Zum%C3%A1rraga_and_Juan_Diego_-_Google_Art_Project.jpg`.
- Normalized gallery asset: `Miguel Cabrera - Altarpiece of the Virgin of Guadalupe with Saint John the Baptist, Fray Juan de Zumárraga and Juan Diego - Google Art Project.jpg`.
- Gallery rendering: ACTIVE ungated image path; no gallery status field.
- **NO CONFIRMED ARTWORK ROUTE** for this entry. Artist route: `#/artist/miguel-cabrera`. Do not invent a slug from the gallery title.
- Evidence: no shared delivered Commons asset, exact same-artist title/worksKey, or same-artist partial-title candidate in the catalog.

## What this means for the pending theory brief

- Cross-registry identity: should shared files and artwork identity remain separate links, and who resolves ambiguous titles, versions and unmatched gallery keys?
- Rights precedence: when a catalog token withholds an image and a gallery entry supplies one, which registry governs? Should a different file of the same artwork inherit a decision, or require its own source evidence?
- Consistent withholding: how should a decision propagate across the active gallery, latent entries, catalog cards, lightbox and prerender metadata? What fallback is appropriate when a checked-in stub contains another artwork?
- Policy completeness: what evidence and owner decision should fill the missing gallery-status contract without treating absence as an automatic finding?

## Reproduction and source fingerprints

From the repository root on macOS, run:

```sh
python3 protocol/tasks/IFACE-001/evidence/cross_registry_identity.py
git show HEAD:js/app.js
git show HEAD:p/artwork/the-starry-night.html
```

The Python script uses the standard library and osascript/JXA only to evaluate registry declarations in memory. It does not execute the app or SEO builder, fetch URLs, or change git state. It rewrites only this report. Registry files are read from the working tree; stubs are read from HEAD. SHA-256 fingerprints pin the inspected data:

- `js/catalog-1.js`: `b691cc321d69ac4701ba4d3f922093c8c0a252ac3bd7b772401b741694ec5fe5`
- `js/catalog-2.js`: `b80174ec311f893fcb2b64e2e2815eaf307a127508f5f54acf9ecbac1e13ac3f`
- `js/catalog-3.js`: `8a8907189ad86e58dede49acba5a4f29ae040c9b3e28dece94d5b0de65522b9e`
- `js/catalog-4.js`: `4cdc28f8202f091d3a4ab06aab935ae7c77fdaa99ae6bf5f0ee125bf5e896d15`
- `js/catalog-5.js`: `736bedd7c24528fee7637f533efe1f870b5a7d5a1c8bd19e7c3dbed8d00a30a3`
- `js/catalog-6.js`: `aa69d90d4d1d820d4b100836ed0ee20f11867daefa497d1d8d85053487baf53a`
- `js/catalog-7.js`: `36257ce60dc0af8c1b9abf28257d521d43dc763085812cef98e1e0f8e69de642`
- `js/catalog-8.js`: `8e0b062b28bde56f42670ba1a36e92687f1328c8e71692f29f6044bac8bb8e7e`
- `js/catalog-9.js`: `7ac90c8fdd2ea1c1a317daf27c7d9667ebb21e0bc5a563904c50ef3abd6d96c6`
- `js/artists-1.js`: `40ae1663a4da28c22c03cf511a0350afe7a20d399b8c107a29e1a2096c2cafba`
- `js/artists-10.js`: `d6cda4dad1c2e33d5c6777d762c14659aba5ad630510fc06ecab06a12da62dd4`
- `js/artists-11.js`: `523d652f946b54d1884d318097e66e3f69bb9171ada7d158a49051d8378ef78c`
- `js/artists-12.js`: `752853501b2235cdf3419f33bfacf0ab2e8ebe04bee9ddde131ece49ae0aa509`
- `js/artists-13.js`: `0c1a836f4d201e29783e30f0660298f7bcd8c9731fa4d506148f8677447e0c28`
- `js/artists-14.js`: `c61576a5c682f7dd63344ff1130a392b3cdbbbb197e5b584c4b9cae760dc96c1`
- `js/artists-15.js`: `7e9eeeaa93c5c6a74396d60401d8d51e6eb4f41abba17c01fe6b859143f9955b`
- `js/artists-16.js`: `a4b10b2fc00b6c04847646c6c4b1ea38da91e7092e3421ae603dcc483fb53054`
- `js/artists-17.js`: `63cb54c5f4d5ddbd9f61c9dca6ed9e5fbd5000bea8043535bce0053faede6998`
- `js/artists-18.js`: `190b9801504d207ce635b489cac59d1129dead57c8ddbcac8338fe73e2a7792b`
- `js/artists-19.js`: `ec4f852c539549c72fa335529040c367ea2601edb20dfcf59efced794727a7c4`
- `js/artists-2.js`: `a0451634b41236b8605114469205e400bd5983f52ca0bfd1ad65d9b503a4a98d`
- `js/artists-20.js`: `abd03a63f9c5967e91e28212ded65ae01eb8ab11dc83efb7583aa4610aadc2b5`
- `js/artists-3.js`: `04cdd95be98952841dd539150b2099201b9a866167d385b61cb762b693d28f2e`
- `js/artists-4.js`: `62894fd1e8ece190b333c649b4af4be95643cdd51ec3b96429d09e009d6c65b6`
- `js/artists-5.js`: `bd967806ac9d50bec56cd9ada6da322682a2e13447391b5d431f17c63f1133e3`
- `js/artists-6.js`: `e655425a6b5271c5bcf2194663ac6552d50e49d95dd7d60f3456f73d55acee00`
- `js/artists-7.js`: `ea88706caac085587d0cf7a4996434b5aed433719d3a46d361cfab665554fb02`
- `js/artists-8.js`: `b11bedab4fbe21a37d33f46526572e826d16e39dc90a569be01d8a15030ed882`
- `js/artists-9.js`: `abc5a909f5fb7e708f5b284cb730fafbfc5837b39e2800b8a2d3b9573bbb1b83`
- `js/artworks.js`: `7e278f218f9c7dc94bbe3fe67092cb1eb4401e0e92803683fa9f82be42694f74`
- `js/tier1-artists.js`: `644b618ce7895d42f1095787fa39d673641b78b6bdc20a943d98f243668557cf`

---

## Independent verification (Claude, 2026-09-15)

Codex produced this census. Its headline claims were re-checked by a separate
method before the file was committed, rather than adopted from the self-report.

- **581 entries, 173 EXACT ASSET — confirmed.** Recomputed with an independent
  normaliser (URL-decode, spaces→underscores, strip the `thumb/`/`NNNpx-` forms,
  compare lower-cased Commons file names). Same 173.
- **The Snail classification — confirmed, after a suspicion that proved wrong.**
  The gallery file is `Matisse_-_Carra,_P18.jpg`, a name that does not describe
  the work, so title-key matching looked like exactly the proxy this project
  keeps catching. The Commons API shows it is a plate from *Tout l'oeuvre peint de
  Matisse* (1982) filed in `Category:The Snail by Henri Matisse`. CONFIRMED SAME
  ARTWORK stands.
- **"Latent" — confirmed, and it is contingent.** `js/app.js` renders the artist
  page's *Major works* panel as `ARTWORKS[a.id][wk.t]` with no gate at all,
  wrapped in `${arc ? "" : …}`. `henri-matisse` has a Tier-1 arc in
  `js/tier1-artists.js`, so the panel is suppressed and the walled work's image is
  not shown. **That is a coincidence of the same shape as the mini-card rails were
  before 2026-09-15:** correct today for a reason unrelated to rights. Remove the
  arc, or render ARTWORKS inside the arc view, and a `status:"copyright"` work's
  image appears ungated. Of 196 artists with gallery art, **166 have no arc**, so
  the ungated panel is the live path for most of them.

The pending theory brief should treat "0 active conflicts" as true-today, not as
structurally guaranteed.
