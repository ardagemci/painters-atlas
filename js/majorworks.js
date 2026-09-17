/* Pigment — the artist page's "Major works" panel, as a callable renderer.

   Extracted from js/app.js on 2026-09-17 so that tests/test_majorworks.py can
   EXECUTE the production renderer under JXA and assert on what it emits. A
   helper that decides correctly proves nothing if the template beside it still
   uses the old value or shows a hint unconditionally — the objection that
   produced this file.

   Needs js/renderable.js (galleryThumbFor) loaded first. Pure: everything it
   reads arrives as an argument, so the same function runs in the browser and
   under JXA.

   majorWorksPanel(artist, catRecords, gallery, esc) → { items, hint, thumbs }
     artist     — an ARTISTS record (uses .name and .works[{t, y}])
     catRecords — the catalog records for that artist
     gallery    — window.ARTWORKS[artist.id], or undefined
     esc        — the page's HTML escaper

   Behaviour changes from the inline version, both deliberate:
   1. A work whose matching catalog record is withheld (status "copyright") no
      longer shows its gallery image or lightbox. Its title and catalog link stay.
   2. "tap a work to enlarge" appears only when at least one thumbnail is shown.
      Inline it appeared whenever the artist had any gallery registry at all,
      including when none of the listed works matched a gallery entry.
   Everything else is emitted exactly as before. */
function majorWorksPanel(artist, catRecords, gallery, esc){
  const catFor = {};
  (catRecords || []).forEach(cw => { catFor[cw.worksKey || cw.title] = cw; });
  let thumbs = 0;
  const items = (artist.works || []).map(wk => {
    const cw = catFor[wk.t];
    const art = galleryThumbFor(cw, gallery && gallery[wk.t]);
    const titleHtml = cw ? `<a href="#/artwork/${cw.id}">${esc(wk.t)}</a>` : esc(wk.t);
    if(!art) return `<div class="work"><span class="w-year">${esc(wk.y)}</span><span class="w-title">${titleHtml}</span></div>`;
    thumbs++;
    return `<div class="work has-img" data-lb-img="${art.img}" data-lb-cap="${esc(wk.t)} (${esc(wk.y)}) — ${esc(artist.name)}" data-lb-link="${art.page}">
                   <img class="w-thumb" loading="lazy" src="${art.img}" alt="${esc(wk.t)} by ${esc(artist.name)}"
                        onerror="this.onerror=null;this.src=this.src.replace(/\\d+px-/,'330px-')">
                   <div><span class="w-year">${esc(wk.y)}</span><span class="w-title">${titleHtml}</span></div>
                 </div>`;
  }).join("");
  const hint = thumbs
    ? `<div class="chip-label" style="margin-top:12px">tap a work to enlarge · images via Wikimedia Commons</div>` : "";
  return { items: items, hint: hint, thumbs: thumbs };
}

window.majorWorksPanel = majorWorksPanel;
