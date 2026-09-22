/* Pigment — the one renderability predicate.

   A catalog image is shown only when isRenderable(w.image) is true. Every
   surface that decides "picture or not" asks this function, and nothing else:
   js/app.js in the browser, and tools/build_seo.jxa.js when it emits og:image
   for the prerendered stubs. tests/test_renderable.py executes this file
   against a fixture matrix and forbids any other expression of the rule.

   Why it lives in its own file and checks src as well as status. Until
   2026-09-15 the rule was spelled out at each call site: sixteen sites wrote
   `w.image && w.image.src && isRenderable(w.image)`, where isRenderable checked
   status alone — and FIVE sites checked no status at all: in js/app.js the
   homepage strip and the two mini-card rails on the artwork page, and in
   tools/build_seo.jxa.js the og:image of museum stubs (when a venue has no
   photograph) and of list stubs (the list's cover). All five were correct only
   because every status:"copyright" record happens to carry no src. A record
   withheld by moving its token while keeping its src would have leaked into
   them — two of them into public share metadata. That is the defect class
   recorded in IFACE-001 (REQ-P1/P2) and RIGHTS-001 E-007.

   "pd" and "licensed" render identically — the difference is the asserted
   basis (a public-domain claim vs. a named photographer's own CC licence), not
   whether the image shows. Only "licensed" makes the credit that
   tests/test_rights_tooling.py checks mandatory rather than incidental.
   RIGHTS-001 Decision A, resolved 2026-09-08 (D-011).

   Scope, stated so nobody over-reads it: isRenderable gates js/catalog-*.js
   records. window.ARTWORKS (js/artworks.js) carries no status field. Since
   2026-09-17 a gallery entry that MATCHES a catalog record inherits that
   record's explicit withholding (galleryThumbFor, below). A gallery entry with
   no catalog match is still ungated — that remains an open IFACE-001 design
   question, not a solved one. */
function isRenderable(img){
  return !!(img
    && typeof img.src === "string" && img.src !== ""
    && (img.status === "pd" || img.status === "licensed"));
}

/* isWithheld — the catalog has explicitly decided NOT to show this work.

   Deliberately narrower than !isRenderable. docs/ARTWORK_SCHEMA.md §3 defines
   status:"copyright" as the value that suppresses rendering; that is a rights
   decision. A "pd" record that merely lacks a src is missing data, not a
   decision, and "none" is enforced by the validator but used by no record and
   never defined as withholding. Treating either as withheld would hide gallery
   art that nothing has ruled out. */
function isWithheld(img){
  return !!(img && img.status === "copyright");
}

/* galleryThumbFor — may a gallery image stand in for this work?

   catRecord is the catalog record matching the work (or undefined), galleryEntry
   its window.ARTWORKS entry (or undefined). The gallery has no status of its
   own, so where the two describe the same work the catalog's withholding wins:
   before 2026-09-17 the artist page's Major works panel showed the gallery image
   regardless, which put a withheld work's picture on screen whenever its artist
   had no Tier-1 arc (RIGHTS-001 E-007; IFACE-001 cross-registry evidence). */
function galleryThumbFor(catRecord, galleryEntry){
  if(!galleryEntry || typeof galleryEntry.img !== "string" || galleryEntry.img === "") return null;
  if(catRecord && isWithheld(catRecord.image)) return null;
  return galleryEntry;
}

/* Publish it the way every data file here publishes its globals. In the browser
   the declaration above is already global; the JXA tools evaluate this file
   inside a loader callback, where a bare declaration would stay local — which is
   how the first wiring failed with "Can't find variable: isRenderable". */
window.isRenderable = isRenderable;
window.isWithheld = isWithheld;
window.galleryThumbFor = galleryThumbFor;
