# Catalogue depth — the measurement, the method, and what is left

*Session work, 2026-09-28, branch `content/catalog-depth`. Batches 10, 11 and 12.*

## The finding

The atlas's weakest area is not the number of painters. It is that most of
them have nothing to look at.

Measured at the start of this session, against `origin/main`:

| | |
|---|---|
| painters | 300 |
| catalogued works | 398 |
| **painters with no catalogued work** | **180 (60%)** |
| of those, died ≤ 1955 and so can carry a PD image | **110** |
| of those 110, already holding fetched images in `js/artworks.js` | **110** |

Of the 120 painters who did have works, 83 had exactly one. So the atlas read
as deep for about 37 painters and as a biography index for the rest.

The second finding is that the fix was already paid for. Every one of the 110
public-domain-eligible painters had images sitting in `js/artworks.js` —
fetched in an earlier pass, never promoted into `js/catalog-*.js`. The work is
not acquisition. It is verification and writing.

Secondary gaps, in order of severity:

1. **The 18th century** — 15 catalogued works against 127 for the 19th.
   (Batch 11 addressed this; it is now 24.)
2. **Nations with painters but no works** — Turkey 13 painters/3 works, Poland
   8/2, China 8/4, India 5/1, Korea 4/1. Belarus, South Africa, Australia,
   Colombia, Indonesia, Ethiopia, Cuba, Czechia and Hungary had none at all.
3. **The venue map** — 28 United States, 15 Italy, 11 United Kingdom, thin
   everywhere else.
4. **17 movements with one painter or none.**

## What shipped

| batch | theme | works | painters un-zeroed |
|---|---|---|---|
| 10 | The Italian spine, Cimabue to Veronese | 12 | 12 |
| 11 | The eighteenth century | 9 | 9 |
| 12 | The seventeenth century | 5 | 5 |

Catalogue 398 → 424. Tier 1 127 → 153. Daily pool 120 → 146. Venues 137 → 140.
PD-eligible painters with no work: 110 → 84.

## The method, and its one bottleneck

Per work: pull the pool image from `js/artworks.js`, verify it against the
Commons API, establish the venue, write 60–90 words plus three `notice`
bullets, score five coordinates, add the record.

**The bottleneck is the venue, not the image and not the prose.** Batch 12 was
half the size of batch 10 for exactly this reason: six painters were fully
researched and held back because no source consulted would say which museum
holds the work. Venue evidence, in descending order of reliability:

1. The Commons file page's own description or source URL (Peeters → the file
   is sourced from `mauritshuis.nl`).
2. The English Wikipedia article's infobox `museum=` field (Steen →
   Rijksmuseum; Zurbarán → Norton Simon).
3. The Commons category listing for the museum.

Wikidata was tried and abandoned: QIDs guessed from memory returned Lotto
works for Zurbarán and Vuillard works for Murillo. If Wikidata is used, resolve
the QID with `wbsearchentities` first and never assume one.

## Verification is not optional, with four examples from three batches

Every image was checked against Commons metadata and the doubtful ones opened
and looked at. That caught, in about forty records:

- **Uccello, *The Battle of San Romano*** — the pool file is the **Uffizi**
  panel, not the National Gallery panel. Three panels exist in three museums
  and the filename names none of them. The venue would have been wrong.
- **Piero, *The Resurrection*** — a **CC BY-SA detail crop**, not the fresco.
  Replaced with a public-domain view of the whole thing.
- **Murillo, *Boys Eating Grapes and Melon*** — a **copy by Carl Reiser
  (1877–1950)** in the Russell-Cotes. Not a Murillo.
- **Ruisdael, *The Windmill at Wijk bij Duurstede*** — an **installation
  photograph** of the Rijksmuseum's Gallery of Honour.

A fifth was mine rather than the pool's: a thumbnail path reconstructed by hand
guessed the hash directory as `3/3d` where it is `e/eb`. Always take the
thumbnail URL from the API.

Searching Commons for a museum *building* returns that museum's **paintings**,
because the museum's name is in their metadata — "National Gallery of Victoria
building" returns a von Guérard, a Tiepolo and a Sargent. Use the category
listing, and look at the photograph before using it.

## What is left

84 public-domain-eligible painters still have no catalogued work. Grouped as
they would best be batched:

- **Held back from batch 12, venue outstanding only** — Leyster, Ruysch,
  Sirani, Fontana, Reni, Kauffman. Cheapest batch available.
- **Russians (7)** — Bryullov, Shishkin, Levitan, Vrubel, Popova, Surikov,
  Serov. Venues will mostly be the Tretyakov and the Russian Museum, both
  already in the registry.
- **Germans and Northerners (10)** — Friedrich, Kollwitz, Beckmann, Schwitters,
  Modersohn-Becker, Kirchner, Hammershøi, Krøyer, Zorn, Hodler.
- **Britain (8)** — Millais, Burne-Jones, J. F. Lewis, Hilliard, Stubbs' peers.
- **France (7)** — Bonheur, Moreau, Redon, Bonnard, Valadon, Doré.
- **Asia and the wider world (12)** — Hiroshige, Utamaro, Shōen, Utamaro's
  peers, Xu Beihong, Huang Gongwang, An Gyeon, Behzād, Basawan, Ustad Mansur,
  Raden Saleh, Ravi Varma. This batch also fixes gap 2 and gap 3 together.
- **Americas and Iberia (9)** — Homer, Bierstadt, Cole, Grant Wood, Orozco,
  Cabrera, Sorolla, and the Turkish painters Mihri Müşfik, Matrakçı, Levni.

At the rate of these three batches — 26 works for 26 painters — clearing the
remaining 84 is six to eight more batches. A reasonable definition of done for
the public-domain half of the atlas is **zero PD-eligible painters without a
work**, which would put the catalogue near 510 and the daily pool near 230.

The other 70 zero-work painters died after 1955. They cannot carry an image at
all, and their records would be Tier 2 with generative covers, as the Abstract
Expressionist batch did. That is a separate decision about whether a record
with no picture earns its place.
