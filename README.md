# Pigment — An Atlas of Painters

An interactive, zero-dependency atlas of **247 painters from Giotto to today**, cross-linked by movement, technique, era and nation — with every cover artwork generated in the browser, in the spirit of each painter's style. Dark gallery and light paper themes included.

Pigment is an **editorial, path-discovering tool**, not a comprehensive history of art. It is a curated selection with a point of view: what it leaves out is as deliberate as what it includes. Counts below are a dated snapshot (2026-07-25) — run `osascript -l JavaScript tools/validate.jxa.js` for current figures.

**Live site:** https://ardagemci.github.io/painters-atlas/

## What's inside

- **247 artist pages** — major works, movements, techniques, and essays on each painter's life, career, life beyond the easel, and fun facts
- **75 movements** with branches and sub-branches (Renaissance → Proto-Renaissance / Early Netherlandish …; Modernism → American Modernism / Harlem Renaissance / Art Deco; Realism → The Peredvizhniki; Icon Painting, Literati Painting, Zen Ink, Rinpa, Nihonga, Persian Miniature, Rayonism, Constructivism …), plus a clickable **genealogical family-tree view**
- **39 techniques**, also branched and tree-viewable (Ink Wash → Splashed Ink; Gestural Abstraction → Dripping / Soak-Stain / Squeegee; Painting on Silk; Miniature Painting; Photomontage)
- **8 era pages** (14th century → today) with clickable birth-year timelines, and **37 nation pages** (including Korea and Iran) with a clickable **world map** — including an animated, zoomable Europe inset
- **The influence graph** — 225 documented relationships (taught / influenced / friends / rivals / partners) drawn as a force-directed constellation: click a painter to light their circle, filter by relationship type, and every artist page shows its own "Lineage & circle" panel
- Instant grouped search, era filters, and chips everywhere — every name, card and dot is a link
- **Real artworks** for painters whose work Wikimedia Commons asserts is public domain (the build filters on died ≤ 1955): major works resolved at build time to images hosted on Commons, shown in each artist's works panel with a full-screen lightbox. Painters still under copyright keep generative covers — a legal constraint worn as a design principle. A death year and a Commons licence template are an *asserted* basis, not a rights clearance; no clearance determination has been made
- **Generative covers:** 27 canvas algorithms paint each artist's card from their palette and style — drips for Pollock, grids for Mondrian, gold mosaic for Klimt — freshly mixed on every visit

## Running locally

No build step, no dependencies. Either open `index.html` directly, or serve the folder:

```sh
python3 -m http.server 8421
# → http://localhost:8421
```

## Editing the data

Artists live in `js/artists-1.js` … `js/artists-16.js`; movements, techniques, eras and nations in `js/taxonomy.js`. Every id an artist references must exist in the taxonomy, and each `style` must match a painter function in `js/app.js`.

To refresh the public-domain artwork images (after adding painters or works):

```sh
osascript -l JavaScript tools/dump-artists.jxa.js > /tmp/pigment-artists.json
python3 tools/fetch_artworks.py     # writes js/artworks.js
```

Check data integrity after edits:

```sh
# macOS (no Node needed)
osascript -l JavaScript tools/validate.jxa.js

# or with Node
node tools/validate.js
```

## Dipolar development coordinator

Pigment's ChatGPT theory pole and Claude synthesis/build pole are joined by a
neutral, resumable Coordinator. It validates structured exchanges, freezes a
converged specification, requires observed QA/browser evidence, and stops for
human approval without merging or deploying. See
[`coordinator/README.md`](coordinator/README.md) for setup and operation.
