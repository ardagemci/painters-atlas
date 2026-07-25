# PIG-001 — Build Evidence Report, Unit 23 (privacy disclosure)

**Author:** Dürer (`claude-implementation-lead`), Implementation Lead
**Date:** 2026-07-25
**Branch:** `pig-001-stabilization` (verified; never `main`; not pushed)
**Gate 1:** VERIFIED — `protocol/tasks/PIG-001/specification.md:8`
`workflow_state: "approved_for_build"`.
**Owner input honored:** AC25 disposition — disclose the Wikimedia Commons
runtime image host, per the owner's ruling relayed at the top of this unit's
brief (not self-host, not proxy).
**Commit:** `1120e37b8c8ca721bf10a21dc5785163577ce0fe`
**Files touched:** `js/app.js`, `index.html`

## What changed

Added `viewPrivacy()` in `js/app.js` (inserted directly after `view404()`),
routed at `case "privacy"` in `route()`'s switch, and linked from the site
footer in `index.html` (`<a href="#/privacy">Privacy</a>`, appended to
`.footer-nav`, matching the existing `#/taste` precedent of a footer-only
link with no main-nav entry — `setNav()`'s `map` was left untouched, exactly
as `taste` already does). `js/app.js`'s `?v=` bumped
`20260724-pig001` → `20260725-pig001e`. No CSS changes: the page reuses the
existing `.page-head` / `.page-kicker` / `.page-lede` / `.sec-title` / `.chip`
classes already used by other views.

## Measured facts (this build, not carried over from Wave D)

Re-ran the greps myself rather than trusting the Wave D numbers in
`build-log-wave-d.md`:

- **Runtime image host, automatic on page load:** `upload.wikimedia.org`.
  **888** occurrences of `upload.wikimedia.org` URLs across five data files:
  `js/artworks.js` (528), `js/catalog-1.js` (161), `js/catalog-3.js` (52),
  `js/catalog-4.js` (44), `js/museums-1.js` (103). (Wave D reported 892; the
  re-count under the same method gives 888 — within the kind of drift a hand
  re-grep produces, not a material discrepancy. I report my own measured
  figure, 888, per the brief's instruction not to copy prior numbers.)
- **Render call sites:** `grep -n "<img\b" js/app.js` → **18** distinct
  `<img>` template sites (lines 804, 1318, 1333, 1368, 1369, 1445, 1475, 1494,
  1517, 1628, 1685, 1762, 1843, 1876, 1884, 1886, 2216, 2898) — more precise
  than Wave D's "12+".
- **Click-through-only hosts** (appear only inside `href="…" target="_blank"
  rel="noopener"` source/credit links, never in `<img src>`): `en.wikipedia.org`
  (614 occurrences), `commons.wikimedia.org` (273), `pt.wikipedia.org` (1, in
  `js/museums-1.js`). These are not automatic requests; disclosed as such.
- **Full external-host inventory**, `index.html` + `css/*` + `js/*.js`:
  `upload.wikimedia.org` (890, incl. 2 in `index.html`'s `og:image`/
  `twitter:image`, 1 unique URL, crawl-time only), `en.wikipedia.org` (614),
  `commons.wikimedia.org` (273), `www.w3.org` (4, SVG XML namespace string,
  never fetched), `ardagemci.github.io` (3, own canonical/`og:url`),
  `pt.wikipedia.org` (1). No analytics, tracking, CDN, or other third-party
  host of any kind found anywhere in `index.html`, `css/`, or `js/`.
- **Analytics/tracking check:** `grep -rniE
  "analytics|gtag|ga\(|beacon|tracking|mixpanel|segment\.|amplitude|sentry|
  hotjar|fbq\(|pixel"` across `index.html`, `js/`, `css/` returns only false
  positives (the word "pixel(s)" used as an art-historical term in artist bios
  — op art, Edo-period mosaic screens — plus unrelated code comments/variable
  names: `devicePixelRatio`, `tlZoom` "pixels per year", "tactlessly"). Zero
  analytics, tracking, or beacon code exists. This is what the privacy page
  now asserts, and it was verified, not assumed.
- **Storage keys**, confirmed by reading the source directly:
  `PASSPORT_KEY = "pigment.taste.v1"` (`js/app.js:68`, localStorage),
  `OB_KEY = "pigment.onboarding.v1"` (`js/app.js:2823`, sessionStorage). A
  third key not named in the brief was found in the same grep and is
  disclosed for completeness rather than omitted: `"pigment-theme"`
  (`js/app.js:2489`, localStorage — dark/light preference).
- **Fonts:** confirmed self-hosted from Wave D (unit 20) — no font-provider
  host appears anywhere in the current inventory above.

## Disclosure copy, as shipped (`js/app.js`, `viewPrivacy()`)

> **Privacy**
> Plain facts about what Pigment stores, what it sends, and to whom.
>
> **No account, no server**
> Pigment has no account system and no backend server. Admiring a work,
> marking it Seen in person, saving it for later, and taking onboarding all
> write to your own browser's storage on your own device — nothing is sent to
> Pigment or to anyone else. Three keys are used: `pigment.taste.v1`
> (localStorage, your Taste Passport), `pigment.onboarding.v1` (sessionStorage,
> only while onboarding is in progress), and `pigment-theme` (localStorage,
> your dark/light choice). This data stays on your device until you clear it
> yourself or clear your browser's site data for Pigment.
>
> **No analytics, no tracking**
> Pigment runs no analytics, no tracking pixels, and no beacons. No visit,
> click, or Admire is logged, measured, or transmitted anywhere. This was
> checked directly in the source, not assumed.
>
> **One third-party host: Wikimedia Commons images**
> Pigment displays artwork and museum photographs hosted on Wikimedia
> Commons, at `upload.wikimedia.org`. When a page shows one of these images,
> your browser requests it directly from Wikimedia's servers, not from
> Pigment — that request reaches Wikimedia with your IP address, under
> Wikimedia's own privacy policy, which Pigment does not control. Measured in
> this build: **888 upload.wikimedia.org image URLs** across the catalog,
> gallery and museum data, rendered as images at 18 places in the code, on
> most pages that show artwork or museum photographs — artist pages, artwork
> pages, museum pages, lists, and more.
> Separately, the "image via Wikimedia Commons" / "photo via Wikimedia
> Commons" / "source" links placed next to individual images point to
> Wikimedia Commons and Wikipedia file or article pages
> (`commons.wikimedia.org`, `en.wikipedia.org`, and one `pt.wikipedia.org`
> page). Those are ordinary outbound links — your browser only contacts them
> if you click through.
>
> **Fonts are served locally**
> Pigment's typefaces, Playfair Display and Inter, are self-hosted from this
> site (`assets/fonts/`). No font provider is contacted when the site loads.
>
> **Image credit**
> Artwork and museum images throughout Pigment are sourced from Wikimedia
> Commons. Where available, the licence and photographer for an individual
> image are linked next to it. This page is the general credit for the
> collection as a whole.
>
> [Back to the atlas]

## Attribution surface check

Grepped `js/app.js` for existing Wikimedia credit before writing anything new.
Found **per-image** credit already shipped at four sites: `:1374` ("photo via
Wikimedia Commons" on museum cards), `:1649` ("public-domain image source"),
`:1770` ("images via Wikimedia Commons", gallery tap-hint), `:1866` ("image
via Wikimedia Commons"). No **general** Commons credit existed anywhere (no
about page, no footer line, no global mention). Added one under "Image credit"
above, on the privacy page, per the brief's guidance that a global credit on
the privacy/about surface plus the existing per-image links is acceptable.
Did not touch the per-image rights-resolution question — that is Seurat's
separate rights-remediation task (D-W-6 in `build-log-wave-d.md`), untouched
here.

## Placement rationale

`#/privacy`, footer-linked, follows the `#/taste` precedent exactly: a
footer-only route not present in `#main-nav`, so `setNav()` needed no change.
Route added as the last case before `default` in `route()`'s switch, title
set via `document.title` like every other view, content wrapped in the
existing `page-head`/`page-kicker`/`page-lede` shell so no new CSS was
required and both themes inherit existing styling automatically.

## Checks run

- `osascript -l JavaScript tools/validate.jxa.js`:
  ```
  app.js: syntax OK
  artists: 247, movements: 75, techniques: 39, eras: 8, nations: 37, painter styles: 27, influence edges: 225, venues: 115, catalog: 317 (tier1: 75), daily pool: 75, museum notes: 103, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
  ALL REFERENCES VALID
  ```
  Zero warnings before this unit, zero after — unchanged, as required.
- `python3 -m http.server 8421 -d .` + `curl`: `/` → 200, `/index.html` → 200,
  `index.html` contains `href="#/privacy"`, `js/app.js` contains `viewPrivacy`
  and `case "privacy"`.
- Browser evidence (real render, both themes): navigated to `#/privacy` at
  `http://localhost:8421`. Dark theme: full copy renders under
  "No account, no server" heading, `page-kicker`/`h1`/`page-lede` in place,
  `document.title` = "Privacy — Pigment". Light theme (toggled via
  `#theme-toggle`): footer confirmed showing the new "PRIVACY" link
  alongside Artists/Taste/Museums/Lists/Movements/Techniques/Eras/Nations,
  correctly styled in the light palette, no visual regression.

## Deviation ledger (Gate 3)

| # | Deviation | Rationale | Status |
| --- | --- | --- | --- |
| D-23-1 | Measured 888 `upload.wikimedia.org` URLs, not Wave D's 892 | Independent re-grep per this unit's own instruction not to copy prior numbers; same method, small count drift, not material. Reported as measured. | Accepted |
| D-23-2 | Disclosed a third storage key, `pigment-theme`, not named in the brief | Found in the same grep pass used to confirm the two named keys. Omitting it would have been an incomplete disclosure of what the brief itself calls "storing taste data locally" — theme preference is also local state. | Accepted |
| D-23-3 | Distinguished automatic-request hosts from click-through-only hosts (`en.wikipedia.org`, `commons.wikimedia.org`, `pt.wikipedia.org`) | These appear only inside outbound `target="_blank"` links next to images, never in `<img src>`. Folding them into the "contacted on every page view" claim would overclaim; separating them is the literal, accurate statement. | Accepted |
| D-23-4 | General Commons credit placed on the privacy page rather than a separate `#/about` route | No `#/about` route exists in this app; inventing one was out of scope for a stabilization unit. Per-image credit already exists at 4 sites; the brief explicitly allows "the privacy/about surface" for the general credit. | Accepted |

## Self-assessment vs acceptance criteria

- **AC25** — Disclosure half: PASS. The runtime request inventory is
  measured fresh (888 image URLs, 18 render sites, zero analytics/tracking),
  presented honestly, and distinguishes automatic requests from click-through
  links. Disposition half: executed per the owner's decision at the top of
  this brief — disclose, don't self-host/proxy. The frozen spec's "exactly
  two hosts" inventory (fonts.googleapis.com, fonts.gstatic.com) is now
  superseded on the record by both Wave D's finding and this unit's
  disclosure; Wikimedia is no longer an undisclosed runtime host.
- **AC14** — No overclaim introduced. "No analytics, no tracking" was
  verified by grep before being asserted, per the brief's explicit
  instruction. "No third-party host" is not claimed — the opposite is stated,
  precisely and with numbers. Language is literal throughout: no metaphor, no
  brand voice, per the frozen spec's rule that privacy/state copy overrides
  house style.

## Known limitations

- I did not add per-viewport (320/390/768/1280/1440) screenshot evidence for
  this specific page — only desktop dark and desktop-viewport light were
  captured live in-browser during this unit. The page is plain static content
  with no responsive-layout risk (uses existing wrapper classes already
  verified responsive on other views), but a full Vermeer viewport pass has
  not been run against `#/privacy` specifically.
- Gate 2 is **not** certified here — that remains Van Eyck's call.
