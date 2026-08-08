# Museum building photographs — measured audit

*Measured 2026-08-08 by fetching the intrinsic dimensions of every photograph
referenced in `js/museums-1.js`. All 104 were measured; none failed to fetch.
The card frame is `.card-art`, `aspect-ratio: 16/10` = **1.60**.*

This document is the evidence behind backlog item **B4**. The CSS half of B4 is
fixed (commit `8aa3bba`); what remains here is a **photograph sourcing**
question, which is curatorial work, not styling.

## Summary

| Band | Ratio | Count |
| --- | --- | --- |
| Portrait — taller than wide | < 1.00 | **22** |
| Mildly tall | 1.00–1.45 | 42 |
| Comfortable in a 16:10 frame | 1.45–1.75 | **23** |
| Mildly wide | 1.75–1.90 | 11 |
| Very wide | > 1.90 | **6** |

Only **23 of 104** photographs sit comfortably in the frame. With
`object-fit: cover` now applied, none of them leaves a gap — but the further a
photograph is from 1.60, the more of it the card discards.

## Portrait photographs — the card keeps roughly a third

These are cropped hardest. `object-position: center 38%` biases the visible band
toward the facade, but a photograph shot in portrait is usually framed for
height, and cropping it to a letterbox often removes the subject.

| Venue | Size | Ratio | Works held |
| --- | --- | --- | --- |
| `munch-museum` | 960×1707 | 0.56 | 3 |
| `kunsthistorisches` | 960×1607 | 0.60 | 6 |
| `vatican-museums` | 960×1533 | 0.63 | 3 |
| `k20-dusseldorf` | 960×1440 | 0.67 | 1 |
| `st-bavo-cathedral` | 960×1440 | 0.67 | 1 |
| `groeningemuseum` | 960×1440 | 0.67 | 1 |
| `kunsthalle-mannheim` | 960×1425 | 0.67 | 1 |
| `museo-frida-kahlo` | 960×1336 | 0.72 | 1 |
| `sistine-chapel` | 960×1304 | 0.74 | 3 |
| `museu-picasso-barcelona` | 960×1301 | 0.74 | 1 |
| `ny-carlsberg-glyptotek` | 960×1288 | 0.75 | 1 |
| `moma` | 960×1280 | 0.75 | 17 |
| `neue-galerie` | 960×1280 | 0.75 | 1 |
| `baltimore-museum-of-art` | 960×1280 | 0.75 | 1 |
| `minneapolis-institute-of-art` | 960×1226 | 0.78 | 1 |
| `pio-monte-della-misericordia` | 960×1205 | 0.80 | 1 |
| `toledo-cathedral` | 960×1200 | 0.80 | 1 |
| `moderna-museet` | 960×1200 | 0.80 | 5 |
| `doria-pamphilj` | 960×1144 | 0.84 | 1 |
| `isabella-stewart-gardner` | 960×1125 | 0.85 | 2 |
| `santo-tome` | 960×1046 | 0.92 | 1 |
| `san-luigi-dei-francesi` | 960×967 | 0.99 | 1 |

**Observed directly on the museums index at 1280×900**, several of these are not
weak crops but weak photographs — architectural detail shots that do not read as
the building at any aspect ratio:

- `kunsthistorisches` — a close-up of a stone inscription tablet, not the museum.
- `vatican-museums` — a side doorway in a brick wall; nothing identifies it.
- `st-bavo-cathedral` — the tower cropped mid-height against sky.
- `kunsthalle-mannheim` — a red stone wall at close range.
- `groeningemuseum` — a doorway with signage; identifiable but thin.

`munch` (0.56, the most extreme ratio in the set) is the counter-example: the
photograph carries the building's name in lit signage and reads well cropped.
**Ratio alone does not predict whether a card works** — these need eyes.

## Very wide photographs

Previously the visible defect: rendered short, leaving a blank strip beneath.
Fixed by `object-fit`, but they now lose their left and right thirds.

| Venue | Size | Ratio | Works held |
| --- | --- | --- | --- |
| `st-peters-basilica` | 960×501 | 1.92 | 1 |
| `tretyakov` | 960×494 | 1.94 | 8 |
| `national-gallery-australia` | 960×480 | 2.00 | 1 |
| `musee-dorsay` | 960×437 | 2.20 | 22 |
| `belvedere` | 960×423 | 2.27 | 2 |
| `louvre` | 960×403 | 2.38 | 13 |

`louvre`, `musee-dorsay` and `uffizi` (1.78, in the mildly-wide band) are the
three cards the owner named.

## Indexed venues with no photograph at all

These hold catalogued works, so they appear on the museums index, and fall back
to a generative canvas cover. The validator reports each one as a notice.

- `ateneum` — 1 work(s)
- `kunstmuseum-basel` — 1 work(s)
- `moa-museum-of-art` — 1 work(s)
- `national-museum-korea` — 1 work(s)
- `national-museum-warsaw` — 1 work(s)
- `ngma-new-delhi` — 1 work(s)
- `pera-museum` — 1 work(s)
- `private-collection` — 8 work(s)
- `santa-maria-novella` — 1 work(s)
- `skagens-museum` — 1 work(s)
- `tokyo-national-museum` — 1 work(s)

`private-collection` is a sentinel and is filtered out of the index; the other
ten are real venues showing a generative cover where a building should be.

## What would resolve this

1. Replace the detail-shot photographs listed above with recognisable exterior
   views, landscape where one exists.
2. Source photographs for the ten real venues that have none.
3. Neither is a styling change. Both are Commons sourcing with the same
   public-domain and attribution discipline as artwork images — each new
   photograph needs its credit line in the photo credit register.
