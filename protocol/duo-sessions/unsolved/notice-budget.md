# Notice budget reconciliation

Measured 2026-09-17 in `duo/unsolved-1229`. Scope: the 30 listed over-budget bullets.

Plan: measure the validator baseline; review each complete bullet against the 12-word rule; edit only lossless candidates; rerun the validator and audit the diff. Then reconcile PIGMENT status against repository evidence.

`tools/validate.jxa.js:137` counts `String(s).trim().split(/\s+/).filter(Boolean).length`. A spaced em dash counts as a word. The governing rule is `docs/ARTWORK_SCHEMA.md` §3, per the owner decision in `docs/BACKLOG.md:15`; work-level voice follows `docs/STYLE_GUIDE.md` §4.3–4.4.

Summary: **27 rewritten; 3 unchanged. Validator A1: 30 before → 3 after.** The three retained warnings preserve meaning over budget. No within-budget bullet was edited.

| record id | before (full text) | after (full text, or "unchanged") | words before→after | what was preserved / why left unchanged |
| --- | --- | --- | --- | --- |
| the-naked-maja | Her gaze lands first — the body is the second thing you see | Her gaze lands first — the body comes second | 13→9 | Gaze before body; the same order of looking. |
| the-sick-child | The surface is scratched and scored — he attacked it with the brush's end | Surface scratched and scored — he attacked it with the brush's end | 14→12 | Both surface marks, his attack, and the brush's end as tool. |
| the-beheading-of-saint-john | The signature in the Baptist's blood — the only one of his life | His signature, in the Baptist's blood — the only one he made | 13→12 | Signature, Baptist's blood, and uniqueness across his life. **Amended in Claude's review** — see below. |
| the-night-watch | The girl in gold carries a dead chicken — the militia's claw emblem | Girl in gold carries a dead chicken — the militia's claw emblem | 13→12 | Girl, gold, carrying, dead chicken, militia and claw emblem. |
| the-night-watch | Find the three muskets: loading, firing, clearing — a manual in one frame | Three muskets: loading, firing, clearing — a manual in one frame | 13→11 | Three muskets, all three actions, and the single-frame manual. |
| the-dog | The dog looks up and to the right, at nothing we can see | The dog looks up and right, at nothing visible | 13→9 | Dog, upward and rightward gaze, and no visible object. |
| adele-bloch-bauer-i | Little eyes hide among the gold ornaments of her gown — find three | Little eyes hide among her gown's gold ornaments — three to find | 13→12 | Hidden little eyes, gold gown ornaments, and three to find. |
| adele-bloch-bauer-i | The choker reappears in Judith I — same jewels, reportedly the same sitter | Choker reappears in Judith I — same jewels, reportedly the same sitter | 13→12 | Choker, named painting, same jewels, and reportedly qualified sitter identity. |
| view-of-delft | Find the little patch of yellow wall at the right — Proust's relic | Proust's relic: the little patch of yellow wall, at the right | 13→11 | Small patch, yellow wall, rightward location, and Proust association. **Amended in Claude's review** — see below. |
| the-fighting-temeraire | The tug is small, dark and real; the ship is already a ghost | The tug: small, dark and real; the ship is already a ghost | 13→12 | Tug's size, darkness and reality; ship already ghostlike. |
| the-fighting-temeraire | The sunset is on the wrong side of the sky — moved for effect | Sunset on the sky's wrong side — moved for effect | 14→10 | Sunset, wrong side of sky, displacement and its purpose. |
| red-fuji | No human figure anywhere — rare for Hokusai, and it's louder for it | No human figure anywhere — rare for Hokusai, louder for it | 13→11 | Complete human absence, rarity for Hokusai, and resulting loudness. |
| the-haywain-triptych | On top of the load: lovers, a praying angel, a demon piping through his nose | Atop the load: lovers, a praying angel, a nose-piping demon | 15→10 | Top of load, lovers, praying angel, demon and nose-piping. **Amended in Claude's review** — see below. |
| ghent-altarpiece | The meadow is painted flower by flower — botanists have counted some 75 species | Meadow painted flower by flower — botanists counted some 75 species | 14→11 | Meadow, individual flowers, botanists, count and approximation some. |
| ghent-altarpiece | The lower-left panel is a 1945 copy; the original is art's great cold case | The lower-left panel: a 1945 copy; original remains art's great cold case | 14→12 | Lower-left location, 1945, copy, and original's great unsolved-case status. |
| the-basket-of-apples | It should all slide off — feel how the tilts cancel each other | It should all slide off — the tilts cancel each other | 13→11 | Expected sliding of everything and mutually cancelling tilts. |
| self-portrait-as-the-allegory-of-painting | One arm holds the brush high, the other the palette: a human compass | One arm holds brush high, the other the palette: a human compass | 13→12 | One high brush arm, other palette arm, and human-compass image. |
| woman-with-a-hat | The green stripe down her face — the shadow that started the scandal | Green stripe down her face — the shadow that started the scandal | 13→12 | Green stripe, down face, shadow, and initiating the scandal. |
| the-joy-of-life | The small ring of dancers at the back — the seed of The Dance | The small ring of dancers at back — seed of The Dance | 14→12 | Small ring, dancers, rear location, and named later work's seed. **Amended in Claude's review** — see below. |
| the-joy-of-life | Line does the drawing, colour does the mood, and they never quite agree | Line draws, colour sets the mood, and they never quite agree | 13→11 | Line/drawing, colour/mood, and qualified never-quite agreement. |
| the-red-studio | The furniture is drawn by absence — bare lines where the red stops | Furniture drawn by absence — bare lines where the red stops | 13→11 | Furniture defined by absence, bare lines, red stopping at them. |
| the-piano-lesson | The grey triangle across Pierre's eye — a shadow with a ruler's edge | Grey triangle across Pierre's eye — a shadow with a ruler's edge | 13→12 | Grey triangle, across named eye, shadow and ruler-edged specificity. |
| melencolia-i | The magic square's every row sums to 34 — and its bottom row dates the print: 1514 | unchanged | 17→17 | Retained: every magic-square row, sum 34, bottom-row location, print dating and 1514. No concise house-voice version found that preserves all of these and the em-dash construction. |
| hunters-in-the-snow | The inn fire at left is the only warm color on the panel | The inn fire at left is the panel's only warm color | 13→11 | Inn fire, left location, only warm color across the panel. |
| the-tower-of-babel | Upper floors rise before the lower ones are finished — there's the flaw | Upper floors rise before lower ones are finished — there's the flaw | 13→12 | Upper/lower floors, unfinished lower construction, timing and resulting flaw. |
| burial-of-the-count-of-orgaz | The boy pointing at the miracle is El Greco's son — the signature is on his handkerchief | unchanged | 17→17 | Retained: boy pointing at the miracle, identity as El Greco's son, and signature on his handkerchief. Shortening further risked losing the gesture, identity or precise signature location. |
| a-bar-at-the-folies-bergere | The reflection is displaced — hers and the customer's; it is not a mistake | Reflection displaced — hers and the customer's; it is not a mistake | 14→12 | Both reflections displaced; explicit denial of a mistake. |
| the-school-of-athens | Plato points to heaven, Aristotle to the world — the whole argument in two hands | unchanged | 15→15 | Retained: Plato pointing to heaven, Aristotle to the world, and the whole argument in two hands. Compact substitutes either changed the destination or lost the two-hand argument. |
| lumber-schooners-penobscot-bay | The masts rule the sky into intervals; the light is banded rose to amber | Masts rule the sky into intervals; light is banded rose to amber | 14→12 | Masts dividing sky into intervals, banded light and rose-to-amber range. |
| beginning-noland | Colour sits in the cloth rather than on it, so nothing casts a shadow | Colour sits within, not atop, the cloth, so nothing casts a shadow | 14→12 | Colour in rather than on cloth, and consequent absence of any shadow. |

## Review amendments (Claude)

The draft above was checked bullet by bullet against the diff, not against this table. All 27
rewrites kept every fact, including the hedges ("reportedly the same sitter", "some 75 species").
Four were changed before commit:

- **Vermeer, *View of Delft*.** The draft read "The little yellow wall patch". Proust's phrase is
  *the little patch of yellow wall* (*petit pan de mur jaune*), and the bullet exists to point at it.
  The object was kept but the allusion was lost. Now: "Proust's relic: the little patch of yellow
  wall, at the right" (11).
- **Caravaggio.** "his life's only one" → "the only one he made" (12). Same fact, readable.
- **Matisse, *The Joy of Life*.** "Small dancer ring" → "The small ring of dancers at back" (12).
- **Bosch, *The Haywain*.** The draft dropped the article before "demon" only, which broke the list's
  parallelism. Now "a nose-piping demon" (10), with every figure kept.

**The record-id column was also wrong in 25 of 30 rows.** It showed the *museum* id (`prado`, `met`,
`rijksmuseum`…) rather than the record id. That matches a search backwards from each notice to the
nearest `id:"`, which lands on `museum:{ id:"…" }` first. The column has been rebuilt by slicing
top-level records from the pre-edit catalog, the way `tools/rights_register.py` does.

