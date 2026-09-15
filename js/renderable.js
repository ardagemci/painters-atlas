/* Pigment — the one renderability predicate.

   A catalog image is shown only when isRenderable(w.image) is true. Every
   surface that decides "picture or not" asks this function, and nothing else:
   js/app.js in the browser, and tools/build_seo.jxa.js when it emits og:image
   for the prerendered stubs. tests/test_renderable.py executes this file
   against a fixture matrix and forbids any other expression of the rule.

   Why it lives in its own file and checks src as well as status. Until
   2026-09-15 the rule was spelled out at each call site: sixteen sites wrote
   `w.image && w.image.src && isRenderable(w.image)`, where isRenderable checked
   status alone — and three sites (the homepage strip and the two mini-card
   rails on the artwork page) tested `w.image && w.image.src` with no status
   check at all. Those three were correct only because every
   status:"copyright" record happens to carry no src. A record withheld by
   moving its token while keeping its src would have leaked into them. That is
   the defect class recorded in IFACE-001 (REQ-P1/P2) and RIGHTS-001 E-007.

   "pd" and "licensed" render identically — the difference is the asserted
   basis (a public-domain claim vs. a named photographer's own CC licence), not
   whether the image shows. Only "licensed" makes the credit that
   tests/test_rights_tooling.py checks mandatory rather than incidental.
   RIGHTS-001 Decision A, resolved 2026-09-08 (D-011).

   Scope, stated so nobody over-reads it: this gates js/catalog-*.js records.
   window.ARTWORKS (js/artworks.js) carries no status field and is not gated
   here — that is an open design question for IFACE-001, not a solved one. */
function isRenderable(img){
  return !!(img
    && typeof img.src === "string" && img.src !== ""
    && (img.status === "pd" || img.status === "licensed"));
}

/* Publish it the way every data file here publishes its globals. In the browser
   the declaration above is already global; the JXA tools evaluate this file
   inside a loader callback, where a bare declaration would stay local — which is
   how the first wiring failed with "Can't find variable: isRenderable". */
window.isRenderable = isRenderable;
