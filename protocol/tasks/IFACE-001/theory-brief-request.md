# IFACE-001 — Theory Brief request

Outgoing intake handoff to the ChatGPT Theory Team. Copy the block below.
Workflow state on issue: `intake` → requesting `theory`.

---

You are the ChatGPT Theory Team for **Pigment**. We are opening `IFACE-001`, the
first task under **OP-INTERFACE** (`protocol/oriented/OP-INTERFACE.md`). Same
cycle as RIGHTS-001, different domain: this one is about what a reader
encounters.

**Your deliverable: a Theory Brief for IFACE-001.**

## The problem, stated precisely

**Pigment has no blank state.** `js/app.js:2190` reads:

```js
const hasImg = w.image && w.image.src && w.image.status === "pd";
```

and the else branch at 2204 renders `canvasTag(...)` unconditionally. So
withholding an image does not produce a page without a picture — it produces the
artist-associated procedural cover. There is no third branch anywhere.

That single gap is currently blocking **four owner decisions** in RIGHTS-001:
options A3, B1, C3 and C4 cannot be selected because they describe an outcome the
build does not produce, and A1 is unsafe without it.

## What already exists, so you do not re-derive it

Two specialist artifacts are filed and you should build on them rather than
repeat them:

- **`protocol/tasks/RIGHTS-001/evidence/durer-01-feasibility.md` §2** — the
  Implementation Lead's scoping: 10 render sites, 4 pool filters, 1 prerender
  path, new CSS box states. His verdict is that this is a medium feature, not a
  one-liner and not a rewrite.
- **`protocol/tasks/IFACE-001/ux-requirements.md`** — Mondrian's requirements,
  the OP's lead. He proposes a specific answer (§1): the hero keeps its frame,
  loses the canvas, and holds an inset hairline rectangle **drawn at the work's
  true proportions from `w.dims`** — the reader is shown the shape and size of
  the picture they are not being shown. He excludes the record entirely from four
  cover-selection surfaces rather than render an absence there, and he refuses
  two things outright (§6), including C3/C4 applied globally to all 61 records,
  on the grounds that the state's legibility depends on its rarity.

**Challenge those. They are proposals, not settled.** Mondrian's §6 refusals in
particular are a UX lead's judgement about reader experience, and the Theory
Team's job is to test whether that judgement serves the product.

## What Pigment is, measured at `5e05dcc`

- Static site, no backend, no build step, GitHub Pages. 398 catalog records,
  879 unique image assets, 61 records already carrying `status:"copyright"` with
  no `src`.
- **Two image registries, gated differently.** `image.status` exists only on
  `js/catalog-*.js`. `window.ARTWORKS` in `js/artworks.js` holds 581 image
  entries and **no `status` field at all**. A record withheld in the catalog
  still renders on its artist page. This is recorded as RIGHTS-001 E-007 and is
  why `PROTOCOL.md` §5 criterion 4 failed there. Any answer must span both.
- **A predicate written eight times.** `w.image && w.image.src && w.image.status
  === "pd"` appears verbatim eight times in `js/app.js`, plus three `cw.image`
  variants and two bare status tests — and the two mini-card rails at 2246/2248
  test `.src` with **no status check at all**. They are correct today only by
  accident: every walled record happens to carry no `src`. Mondrian's REQ-P1
  makes one `renderableImage()` helper the sole renderability expression, ceiling
  zero, guarded by test. We regard that as the structural heart of the task.

## The questions we want theory on

1. **Is "show the shape you cannot see" the right idea?** It is elegant and it is
   also unusual. Does a hairline rectangle at true proportions read as
   deliberate, or as broken? Is there a better answer that keeps Pigment feeling
   like Pigment on a page with no picture?
2. **Rarity versus consistency.** Mondrian argues the state works because it is
   rare, and therefore refuses C3/C4 globally. If the owner later selects a
   global option anyway, what should happen? A design that degrades gracefully at
   61 records is worth more than one that only works at three.
3. **Four states, one reader.** There are already three: a real image; a "seeded
   Pigment interpretation" for copyright-walled records; and an "interpretation
   painted in the browser — the original is unphotographed". A fourth must be
   distinguishable by someone not reading carefully. Mondrian's answer is
   structural — colour versus paper, which survives a 46px thumbnail where
   wording cannot. Is that enough, and what should the words be?
4. **Exclusion versus absence.** He removes the record from four surfaces
   (museum card, actuality, list card, list hero) rather than showing a state
   there, on the grounds those covers represent a venue or an article rather than
   the record. Is disappearing from a surface better or worse for a reader than
   appearing as an absence?
5. **The prerender.** 337 of 398 artwork stubs carry `og:image`. A withheld
   record emits none and **no site-default substitute** — Mondrian refuses a
   default. What does a shared link to such a record look like, and is that
   acceptable?

## Constraints

Static site: no backend, no database, no build step, no runtime policy engine.
`js/app.js` and `css/` are OP-INTERFACE's to change, and nothing in `js/catalog-*.js`
image blocks or the rights census is — those belong to OP-RIGHTS, and a proposal
needing them is a dependency to record, not a scope to widen.

Gate 1 is unmet and stays unmet: `build_authorized: false`. Your brief authorises
no implementation.

Accessibility is not a later pass. PIG-001 spent thirty-seven build units partly
on this class of problem and it was certified by a reviewer who blocked it four
times. `role="img" aria-label="no image"` announces *"image, no image"* — that is
the defect class, and regressing it is not acceptable.

## What would make this brief fail review

Proposing a spinner, a broken-image affordance, or a placeholder that reads as a
loading state. Designing only the artwork detail page and leaving the other nine
surfaces to implementation. Requiring a backend. Ignoring the second registry.
And treating the eight duplicated predicates as a tidiness issue rather than the
reason this defect existed at all.
