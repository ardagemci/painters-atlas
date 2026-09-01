# IFACE-001 — intake baseline

**Opened by:** owner instruction, splitting RIGHTS-001. **Parent:** RIGHTS-001.
**OP:** OP-INTERFACE. **Lead:** Mondrian. **Baseline:** `8354de3`.

## Why this is OP-INTERFACE's task and not OP-RIGHTS'

`protocol/oriented/OP-INTERFACE.md` already claims this ground: the OP owns "the
states most easily forgotten: empty, loading, error, too-long, too-many, and **the
walled record that has no image to show**." That state does not exist yet, and
its absence is now blocking rights decisions.

OP-RIGHTS may not write `js/app.js` rendering logic or `css/`. So RIGHTS-001
could discover the gap and cannot close it.

## The finding

**Pigment has no blank state.** `js/app.js:2190`:

```js
const hasImg = w.image && w.image.src && w.image.status === "pd";
```

and the else branch at 2204 renders `canvasTag(...)` unconditionally. Withholding
an image — by removing `src` or by moving the token off `"pd"` — does not produce
a page without a picture. It produces the artist-associated procedural cover.

**Consequence upstream:** RIGHTS-001's options A3, B1, C3 and C4 are not
selectable, and A1 is unsafe without a paired change. Four owner decisions are
waiting on one missing product state.

## Scope, as measured by Dürer

**Six sites substitute a cover for an artwork record:** `js/app.js` 879 (cards),
1831 (list entries), 2037 (arc strip), 2204 (detail hero), 2246 and 2248 (the two
mini-card rails).

**A latent trap at 2246 and 2248:** both gate on `o.image && o.image.src` with
**no status check**. They are correct today only because all 61
`status:"copyright"` records carry no `src`. Any change that withholds an image by
moving the token while keeping `src` leaks that image into those two rails.

**Four further sites** substitute an artist-seeded cover onto another entity when
a work is unrenderable: 1580 (museum card), 1719–1720 (actuality), 1773 (list
card), 1810–1811 (list hero). **Four pool filters** already behave metadata-only:
1485, 1609, 3363, 2476/2495.

**Prerender:** `tools/build_seo.jxa.js:103,177`. 337 of 398 artwork stubs carry
`og:image`; a withheld record needs a defined fallback or it ships stale social
metadata — the failure already seen once on `triumph-of-death`.

**Plus** new CSS box states — `.aw-hero-gen`, `.card-art`, `.arc-work-gen`,
`.le-art`, `.mc-img` all size to a canvas — and accessible-name work.

Dürer's characterisation: a medium feature. Not a one-liner, not a rewrite.

## Also in scope — the second registry

**E-007.** `image.status` exists only on `js/catalog-*.js`. `window.ARTWORKS` in
`js/artworks.js` holds **581 image entries and zero `status` fields**, and **19 of
the 23** credit-required files also live there. A record withheld in the catalog
still renders on its artist page.

This is why `PROTOCOL.md` §5 criterion 4 fails for RIGHTS-001: two image
registries with different gating is an information-architecture incoherence, not
a preference. Whether the answer is one gate over both registries, one registry,
or something else is this task's to decide.

`creditUsage()` already walks both registries, so attribution is unaffected —
only the gate is single-registry.

## Acceptance shape (not yet criteria)

A record can be marked "show no image" and no surface shows one — detail, cards,
lists, rails, museum pages, arc strip, prerendered `og:image`. The state is
legible to a reader rather than looking broken, and carries an accessible name.
Both registries honour it. Browser evidence at desktop and mobile, both themes,
per Gate 2.

## Evidence

`protocol/tasks/RIGHTS-001/evidence/durer-01-feasibility.md` §2;
`protocol/tasks/RIGHTS-001/evidence/hogarth-03-synthesis-review.md` §3;
`protocol/tasks/RIGHTS-001/decision-record.md` E-002, E-007;
`protocol/tasks/RIGHTS-001/challenge-adaptation-report.md` CH-1.
