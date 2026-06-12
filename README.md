# Pigment — An Atlas of Painters

An interactive, zero-dependency atlas of **206 painters from the 15th century to today**, cross-linked by movement, technique, era and nation — with every cover artwork generated in the browser, in the spirit of each painter's style. Dark gallery and light paper themes included.

**Live site:** https://ardagemci.github.io/painters-atlas/

## What's inside

- **206 artist pages** — major works, movements, techniques, and essays on each painter's life, career, life beyond the easel, and fun facts
- **64 movements** with branches and sub-branches (Modernism → American Modernism / Harlem Renaissance / Art Deco; Postmodernism → Neo-Expressionism; Renaissance → Early Netherlandish / Mannerism …), plus a clickable **genealogical family-tree view**
- **36 techniques**, also branched and tree-viewable (Gestural Abstraction → Dripping / Soak-Stain / Squeegee; Miniature Painting; Photomontage)
- **7 era pages** (15th century → today) with clickable birth-year timelines, and **35 nation pages** with a clickable **world map**
- Instant grouped search, era filters, and chips everywhere — every name, card and dot is a link
- **Generative covers:** 27 canvas algorithms paint each artist's card from their palette and style — drips for Pollock, grids for Mondrian, gold mosaic for Klimt — freshly mixed on every visit

## Running locally

No build step, no dependencies. Either open `index.html` directly, or serve the folder:

```sh
python3 -m http.server 8421
# → http://localhost:8421
```

## Editing the data

Artists live in `js/artists-1.js` … `js/artists-7.js`; movements, techniques, eras and nations in `js/taxonomy.js`. Every id an artist references must exist in the taxonomy, and each `style` must match a painter function in `js/app.js`.

Check data integrity after edits:

```sh
# macOS (no Node needed)
osascript -l JavaScript tools/validate.jxa.js

# or with Node
node tools/validate.js
```
