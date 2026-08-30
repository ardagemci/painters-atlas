# OP-INTERFACE

**Prefix:** `IFACE-` · **Lead:** Mondrian (`claude-ux-architect`)

## The question it answers

> What does the reader encounter, and does it work at real viewports?

Information architecture, flows, states, and the visual system. This OP owns
what the atlas *feels* like to move through — including the states most easily
forgotten: empty, loading, error, too-long, too-many, and the walled record that
has no image to show.

## Write scope

**May write**

| Path | Condition |
|---|---|
| `css/**` | the visual system |
| `index.html` | structure and document head |
| `js/app.js` | rendering, routing, view logic |
| `protocol/tasks/IFACE-*/` | its own task artifacts |
| `protocol/oriented/OP-INTERFACE.md` | this file |
| `docs/` | UX and visual documentation only |
| `tests/test_prerender_hygiene.py`, browser-evidence harnesses | interface guards |

**May not write**

- Any data record: `js/catalog-*.js`, `js/artists-*.js`, `js/lists-*.js`,
  `js/taxonomy.js`, `js/influences.js`. A layout that would read better with
  different words asks OP-CONTENT; a layout that needs a record retiered asks
  OP-CONTENT.
- `image:{}` blocks, `js/photo-credits.js`, or the rights census. If a design
  needs a new rights state rendered — a credit line, a licence badge, an
  "unavailable" treatment — the *token* is OP-RIGHTS's to define and the
  *presentation* is this OP's to build. Record the dependency both ways.
- The Lane III sealed set, in Lane III.

## Agents

| Agent | Role in this OP |
|---|---|
| **Mondrian** | Lead. IA, flows, states, UX requirements |
| **Matisse** | Visual system direction and review |
| **Vermeer** | Real-browser evidence at real viewports |
| **Van Eyck** | Independent QA and accessibility gatekeeper |
| **Dürer** | Implementation |
| **Caravaggio** | Opposition, on request |

## Acceptance criteria

1. Browser evidence at **desktop and mobile, both themes**, attached — not
   described. Vermeer produces it; the owner should not have to check manually.
2. Accessibility reviewed by Van Eyck, who did not implement the change:
   keyboard reachability, focus visibility, contrast, and a meaningful
   accessible name for every generated canvas and image.
3. Empty, loading, error and overflow states are specified and shown, not left
   to chance.
4. No horizontal page scroll at any tested viewport; wide content scrolls
   inside its own container.
5. `tools/validate.jxa.js` exits 0 and the suite passes.
6. Any prerendered surface affected by the change is re-emitted in the same
   commit.

## Standing notes

The atlas paints a **generative cover** in the browser for records with no
renderable image (`js/app.js`, `canvasTag`). For a record walled under
copyright it is labelled "a seeded Pigment interpretation — the original
artwork remains under copyright." That label is a rights-bearing string: this
OP may change its typography, placement and prominence, and may not change its
wording without OP-RIGHTS. It is currently the subject of an open question in
`RIGHTS-001`.
