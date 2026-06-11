# Pigment — An Atlas of Painters

An interactive, zero-dependency atlas of **200 painters from the 16th century to today**, cross-linked by movement, technique, era and nation — with every cover artwork generated in the browser, in the spirit of each painter's style. Dark gallery and light paper themes included.

**Live site:** https://ardagemci.github.io/painters-atlas/

## What's inside

- **200 artist pages** — major works, movements, techniques, and essays on each painter's life, career, life beyond the easel, and fun facts
- **60 movements** with branches and sub-branches (Renaissance → Mannerism, Abstract Expressionism → Action Painting, Dada → Neo-Dada, Ottoman Miniature, Young Poland, Op Art …)
- **36 techniques**, also branched (Gestural Abstraction → Dripping / Soak-Stain / Squeegee; Miniature Painting; Photomontage)
- **6 era pages** with clickable birth-year timelines, and **35 nation pages** from Türkiye to Australia
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
