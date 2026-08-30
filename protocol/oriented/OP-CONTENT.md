# OP-CONTENT

**Prefix:** `CONTENT-` · **Lead:** Vasari (`claude-curator`)

## The question it answers

> What belongs in the atlas, and is it described honestly?

Roster and coverage, taxonomy coherence, influence attestation, editorial voice.
This OP decides what enters and how it is written — and, equally, what the atlas
admits it does not hold.

## Write scope

**May write**

| Path | Condition |
|---|---|
| `js/catalog-*.js` | **every field except `image:{}`** — title, year, movements, techniques, museum, dims, description, notice, tags, tier, related |
| `js/artists-*.js` | painter records and biographies |
| `js/lists-*.js` | editorial lists |
| `js/taxonomy.js` | eras, nations, movements, techniques |
| `js/influences.js` | edges and their attestations |
| `js/artworks.js` | the gallery registry |
| `docs/STYLE_GUIDE.md`, `docs/CATALOG_BATCH_*.md`, `docs/ROSTER_*.md` | editorial and curatorial documentation |
| `protocol/tasks/CONTENT-*/` | its own task artifacts |
| `protocol/oriented/OP-CONTENT.md` | this file |

**May not write**

- `image:{ src, page, status }`. A batch never authors an image URL — every URL
  is read from `js/artworks.js` or from a rights-census entry. This rule exists
  because a batch once invented eleven Commons filenames from memory and all
  eleven 404'd. Adding a work whose image needs a new source is a dependency on
  OP-RIGHTS, recorded as one.
- `js/photo-credits.js`, the rights census, or `tests/test_rights_tooling.py`.
- `css/`, `index.html`, rendering logic in `js/app.js`.
- The Lane III sealed set, in Lane III.

## Agents

| Agent | Role in this OP |
|---|---|
| **Vasari** | Lead. What belongs, taxonomic coherence, influence attestation, coverage honesty |
| **Van Gogh** | Editorial voice per `docs/STYLE_GUIDE.md` |
| **Seurat** | Data integrity across records |
| **Dürer** | Implementation |
| **Van Eyck** | Independent review |
| **Caravaggio** | Opposition, on request — particularly against a selection rule that flatters the existing roster |

## Acceptance criteria

1. Every factual claim in prose is checkable, and the checkable ones were
   checked. Dimensions are the **work**, not the frame.
2. Coverage honesty: where the atlas cannot hold something — because no image
   exists under an acceptable basis, or the tradition is absent from the
   sources — the gap is recorded as a finding, not quietly skipped.
3. Influence edges carry attestation where attestation is possible, and the
   ungrounded count is a ratchet that may fall and never rise.
4. Taxonomy additions are used by at least one record; orphan vocabulary fails.
5. Selection rules are stated before the batch, not fitted afterwards, and a
   rule that has become self-confirming is retired by name.
6. `tools/validate.jxa.js` exits 0 and the suite passes.

## Standing notes

Selection rules in this project have a habit of feeding on their own output —
**inbound gravity** was retired after Batch 06 for exactly that reason, having
begun to rank works by how much the atlas already talked about them. A rule that
cannot be argued against with evidence is a preference wearing a formula.
