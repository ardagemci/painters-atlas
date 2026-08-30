# RIGHTS-001 — Intake Baseline

**Oriented Protocol:** OP-RIGHTS · **State:** `intake` · **Baseline:** `dd87ad2`

This document states what is measured and what is open at the moment the task
opens. It reaches no conclusion and recommends nothing. Per OD-5 it records
asserted basis and residual uncertainty, never clearance.

## 1. What Pigment is, measured

A zero-dependency static site: plain HTML/CSS/JS, no build step, no backend, no
database, published to GitHub Pages. There is no server, so there is no runtime
policy engine — the render gate is a literal in a data file, read by `js/app.js`.

| Measure | Value |
|---|---|
| Unique image assets | 880 |
| Rendered | 879 |
| Catalog records carrying `status:"pd"` | 342 |
| Catalog records carrying `status:"copyright"` | 61 |
| Rights census entries | 752 |
| Census entries marked `credit_required` | 24 |
| Files in `IMAGE_CREDITS` (attribution rendered) | 23 |

Licences Commons asserts across the census: Public domain 709, CC0 19,
CC BY-SA 4.0 11, CC BY 2.0 6, CC BY 3.0 3, CC BY-SA 3.0 2, CC BY 2.5 1,
CC BY 4.0 1.

**Every catalog image is hotlinked** from `upload.wikimedia.org`. Pigment stores
no image bytes of its own. Hotlinking and hosting are distinct acts and the
distinction is unexamined in the project's documents to date.

## 2. The `status` token

`docs/ARTWORK_SCHEMA.md` §3 defines `image.status` as a **rendering** flag —
"this may be displayed" — and it has two live values, `pd` and `copyright`.
`docs/CATALOG_BATCH_02.md` constraint 5 states that CC BY / CC BY-SA files do
not take the `pd` token.

The token therefore does two jobs: it gates rendering, and it reads as a claim
about a file's legal status. The schema has no value for "renderable, licence
asserted, credit required."

## 3. Open question A — six records on a borrowed token

Six records carry `status:"pd"` on files whose Commons pages assert a Creative
Commons licence. This is **not a licence breach**: all six are registered in
`js/photo-credits.js` and render their credit, so the attribution obligation is
met. The defect is that the token misdescribes the basis.

Reading the file pages — rather than the census summary of them — split the set
somewhere other than where the finding originally guessed. The line is not flat
work versus three-dimensional work. It is whether a **named living photographer
asserted authorship**:

| Records | File-page assertion |
|---|---|
| `david`, `pieta`, `little-dancer-aged-fourteen`, `black-fuji`, `vahine-no-te-tiare` | `{{self\|...}}` — a named person states they made the image and licensed it |
| `the-ten-largest-no-9` | a bare `{{cc-by-sa-4.0}}` on a 127-byte page: an empty `{{Artwork}}` naming no author, no source, no photographer |

A seventh record, `triumph-of-death`, left this set on 2026-08-30 by
re-sourcing rather than by reinterpretation. Its former file carried
`author=Pieter Brueghel` — a man who died in 1569, and so not a party who could
license anything — over a file whose stated source was the Prado's own website.
The guard's ceiling fell 7 → 6.

## 4. Open question B — a conflict on the face of a file page

For `the-ten-largest-no-9`, searches of
`Category:The_Ten_Largest_(Hilma_af_Klint)` did not locate a replacement that
could be taken without raising a new question:

- the largest candidate carries `{{self}}` **with no licence parameter** beside
  a bare `{{PD-old}}`, while claiming `{{own}}` of a painting made in 1907;
- the one tagged `{{PD-Art|PD-old-70}}` carries
  `© Stiftelsen Hilma af Klints Verk` inside its own description field.

Two assertions by strangers, in conflict, on a painter who died in 1944. It is
not known who applied either tag, or whether either had standing to.

## 5. Open question C — the generative covers

For records with no renderable image, `js/app.js` paints a cover in the browser
from **the artist's own assigned style and palette**, seeded by the work id
(`canvasTag`). For a record walled under copyright it is labelled:

> "a seeded Pigment interpretation — the original artwork remains under
> copyright"

This affects the 61 `status:"copyright"` records — Noland, Guston, Motherwell,
Kline, Hofmann, Enwonwu among them. Pigment generates an image derived from a
protected artist's style and renders it on that artist's artwork page.

No document in this project addresses it. `docs/ARTWORK_SOURCES_COPYRIGHT_ARCHITECTURE.md`
§9 lists nine non-assumptions and has no entry for "we generated it ourselves";
its R3 tier reads "no Pigment-hosted or embedded artwork image," which does not
describe what Pigment does. This is not a reproduction question, and it is
plausibly the project's most novel exposure.

## 6. Open question D — jurisdiction

Unresolved and underlying all of the above. The site is hosted in the United
States (GitHub Pages); the owner is not in the United States; readers are
anywhere. It is not known which of those determines exposure, or whether the
answer differs by question.

## 7. Machinery that already exists

Anything proposed should account for what is built, rather than describe it in
new nouns:

| Concern | Existing mechanism |
|---|---|
| Rights evidence | `protocol/tasks/PIG-001/evidence/artwork-image-rights.json`, regenerated by `tools/audit_artwork_rights.py`. A 429 is recorded as `unverified`, never as a clean result |
| Attribution rendering | `js/photo-credits.js`, generated by `tools/build_photo_credits.py`; TASL credit lines rendered by `js/app.js` |
| Render gate | `image.status`, read by `js/app.js` |
| Drift detection | asset-inventory ledgers in `tests/test_rights_tooling.py`; undeclared drift fails |
| Language discipline | `TestProseLanguage` — banned assertions of legal status, pinned exemptions |
| Token accuracy | `TestPdTokenAccuracy`, a ratchet at 6 |

## 8. Questions already framed for counsel

Assembled but not asked, with the census ready so no one pays for reading time:

1. Which jurisdiction governs the owner's exposure, and does it differ for
   owner, host and reader?
2. Does serving a resized Commons thumbnail of a CC BY-SA 4.0 file produce
   "Adapted Material" and trigger ShareAlike, or is it a technical modification
   outside it?
3. For each licence version in use (CC BY 2.0, 2.5, 3.0, 4.0; CC BY-SA 3.0,
   4.0), what must an attribution notice contain, and does the rendered credit
   contain it? Versions differ on termination and cure.
4. Where Commons' PD-Art position and an uploader's CC tag conflict on one file,
   does complying with the CC tag create obligations that would not otherwise
   exist?
5. Where the named licensor is a painter dead for centuries — or a foundation
   asserting © on a file tagged PD-Art — on what basis, if any, can the offered
   licence be relied on?
6. Does generating and displaying an image derived from a living or
   in-copyright artist's style, labelled as an interpretation, raise a question
   distinct from reproduction?

## 9. What is not known

Stated plainly, because the protocol requires it rather than as a formality:

- Which country's law governs the owner's exposure.
- Whether a resized thumbnail is an adaptation under CC BY-SA.
- Who applied the af Klint tags, and whether either had standing.
- Whether the Stiftelsen notice claims the work, the photograph, or is
  boilerplate.
- Whether the style-derived covers raise any question at all — no one competent
  has been asked.
