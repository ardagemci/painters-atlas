# Matisse — seven records that were walled by mistake

*Session build (Lane II, the owner present), 2026-08-27, branch `main`.*

**Nothing here is a rights determination, a clearance, or legal advice (OD-5).**
This records what Wikimedia Commons asserts about seven files, what the atlas's
own rule already said, and what was changed as a result. It reaches no legal
conclusion, and the two remaining walled works stay walled precisely because a
conclusion would be needed to move them.

---

## The finding

`CLAUDE.md` §6 and `PIGMENT.md` §14 state the rule as **public-domain images
(artist died ≤ 1955) from Wikimedia Commons only**.

**Henri Matisse died on 3 November 1954.** He has always been inside that rule.
All nine of his catalogue records nonetheless carried `image:{status:"copyright"}`
and generative covers, and `docs/IMAGE_RIGHTS_ROUTES.md` (Seurat, 2026-08-06)
lists him among the seven artists for whom "the generative-cover and no-image
states … are the answer."

That grouping was right when it was written and is now out of date. Matisse's
French term is life + 70, which expired on **1 January 2025** — eighteen months
before the routes document, but the seven were treated as one bloc and the death
date was not re-checked per artist. Commons has been accepting Matisse uploads
since that expiry.

## What Commons asserts, per file

Verified 2026-08-27 against the Commons API (`extmetadata`) and each file page's
own licence templates. Every one of the seven is tagged public domain; none
carries an attribution or share-alike condition.

| Record | Commons file | Templates asserted | Px |
| --- | --- | --- | --- |
| `woman-with-a-hat` | `Matisse-Woman-with-a-Hat.jpg` | PD-old-70, PD-US-expired | 1860 |
| `the-joy-of-life` | `Le Bonheur de vivre Barnes (01c) - Flickr - rverc.jpg` | PD-Art | 3622 |
| `open-window-collioure` | `Matisse-Open-Window.jpg` | PD-Art | 2012 |
| `the-dance-matisse` | `La Danse II, par Henri Matisse.jpg` | PD-art | 2000 |
| `the-red-studio` | `L'Atelier rouge, par Henri Matisse.jpg` | PD-old-70 | 1744 |
| `goldfish-matisse` | `I pesci rossi.jpg` | PD-Art | 2052 |
| `the-piano-lesson` | `La Leçon de piano, par Henri Matisse.jpg` | PD-old-70 | 2594 |

Each record's `image.page` cites the file page that carries the assertion, per
the rule that every catalogue image cites the page licensing it.

## Exact-work verification

The `§14` trap this repository keeps hitting is the plausible wrong picture, so
every file was opened and looked at, not accepted on filename:

- **Goldfish** — confirmed the 1912 Pushkin canvas (bowl on a round table amid
  greenery), *not* the 1914 *Goldfish and Palette* it is routinely confused with.
- **The Dance** — confirmed *Dance II*, the saturated Hermitage version, not the
  paler 1909 *Dance (I)* at MoMA. The file's `ObjectName` also reads "Dance II".
- **Le Bonheur de vivre** — the Flickr-sourced file is a flat reproduction of the
  full canvas, despite the provenance suggesting an installation shot.
- **Woman with a Hat**, **Open Window**, **The Red Studio**, **The Piano Lesson**
  — each confirmed against its known composition.

## What changed

The seven moved from `tier:2` / `status:"copyright"` to **Tier 1** with real
images: `worksKey` back-links, hand-scored coordinates preserved unchanged,
60–90-word descriptions (the daily-pool budget, which they now enter), three
`notice` bullets and four tags each. `js/artists-4.js` gained the four missing
`works` entries. Catalogue Tier 1 rose to 127 and the daily pool to 120.

`LIST_TIER2_CEILING` was lowered 24 → 23, the ratchet the validator asked for
once these left the below-Tier-1 population.

## What stays walled, and why

**Blue Nude II (1952) and The Snail (1953).** The life + 70 term that freed the
early work covers these too in Europe — but their **US** term does not expire
until the 2040s, and Commons requires public domain in both the source country
and the United States. Neither is on Commons, and neither should be taken from
anywhere else. They keep their generative covers.

This is the useful shape of the finding: the wall was never one wall. It runs
**per work**, by publication date, not per artist by death date. The atlas's
death-date rule is a fast approximation that was hiding a real distinction in
both directions — it wrongly excluded seven Matisses, and it would wrongly
include the two late ones if applied naively.

## Open, for the owner

- **Picasso.** Six pre-1930 records (*The Old Guitarist*, *Family of
  Saltimbanques*, *Les Demoiselles d'Avignon*, *Ma Jolie*, *Still Life with Chair
  Caning*, *Three Musicians*) have files on **en.wikipedia** tagged
  `PD-US-expired-abroad` — expiry, not fair use, and a different category from
  the NFCC files `IMAGE_RIGHTS_ROUTES.md` Part 0 correctly warns about. The claim
  would be **US-only** and would need a distinct `image.status` token and a
  qualified opinion. Not acted on.
- **Dalí.** *The Persistence of Memory* (1931) reaches US expiry on
  **1 January 2027**. Worth diarising; worth an Actuality list on the day.
- **`IMAGE_RIGHTS_ROUTES.md` §2.5** should be read with this correction beside
  it: its per-route research stands, but its bloc treatment of "the seven" cost
  the atlas seven images for eighteen months.
