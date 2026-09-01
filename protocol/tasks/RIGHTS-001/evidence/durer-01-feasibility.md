# Dürer — RIGHTS-001 feasibility assessment

**Provenance.** Produced by `claude-implementation-lead` (Dürer) for RIGHTS-001
round 3, on owner authorisation, to satisfy `PROTOCOL.md` §5 criterion 5 — "the
direction is technically feasible (Implementation Lead confirmed)" — which no
one had supplied across two rounds (decision record D-002).

**Gate 1 respected:** `state.json` carries `build_authorized: false`. This is
assessment only; no repository file was modified.

**Verified before filing.** The two load-bearing claims were checked
independently: the A1 attribution regression (§1, recorded as E-008) and the
schema/validator enum disagreement (E-009). Both hold exactly as stated.

---

## 1. Per-option feasibility

**The `pd` literal is load-bearing in 10 files, not one.** Gate sites:
`js/app.js` 875, 1485, 1574, 1609, 1714, 1769, 1803, 1825, 2034, 2190, 2476,
2495, 3363; `tools/validate.jxa.js` 168, 184, 188 (the enum), 200, 213, 334,
425; `tools/build_seo.jxa.js` 103, 177; `tools/asset_inventory.py` 53–58;
`tools/rights_register.py` 68–70; `tools/check_image_pages.py`;
`tests/test_image_pages.py`; `tests/test_rights_tooling.py` 1352.

- **A1 (new basis token) is far more expensive than the brief implies, and the
  reason is attribution, not cost.** `js/app.js:2228` renders the inline credit
  inside `hasImg && …`, and `creditUsage()` at `js/app.js:2495` filters
  `status === "pd"`. Migrate the five records to any new token and, with no
  other change, **the five images stop rendering, their inline credits vanish,
  and they drop off `#/credits`** — the site would carry *less* attribution
  after a change made in the name of accuracy. A1 is only implementable bundled
  with an edit to every gate above plus `docs/ARTWORK_SCHEMA.md` §3 and the
  `validate.jxa.js:188` enum. That is OP-INTERFACE work (`js/app.js` rendering
  logic is explicitly outside OP-RIGHTS' scope, `OP-RIGHTS.md:53–55`).
- **A2 (re-source) is cheaper than A1** — `image:{src,page,status}` is the only
  field that moves, squarely inside OP-RIGHTS' write scope (`OP-RIGHTS.md:43`),
  plus a `p/**` re-emit via `build_seo.jxa.js` and ledger entries. Precedent
  exists: `triumph-of-death` already left the set this way. But E-006 makes it
  cheaper still to *find* the affected work than the per-record framing
  suggests: one Commons account supplies **four** of the 23 `IMAGE_CREDITS`
  entries, not two.
- **A3 / B1 are not implementable today**, and CH-1 is right on the mechanism.
  `js/app.js:2190` gates, `2204` falls through to `canvasTag` unconditionally.
  There is no third branch anywhere.
- **A4 / B4 are free** — a dated ledger entry in `tests/test_rights_tooling.py`
  and prose. No code moves.
- **B2 / B3** are process, not code.
- **C1** free. **C2** (artist-neutral) is a `js/app.js` + `css/` change at every
  `canvasTag` call site, ~24 of them (859–3655) — pure OP-INTERFACE, and E-001
  is right that it removes editorial content, not a derivation. **C3 / C4**
  require the same missing no-image surface as A3/B1, applied globally.

**Documentation defect found in passing:** `docs/ARTWORK_SCHEMA.md` §3 documents
the enum as `"pd" | "generative" | "none"`; `tools/validate.jxa.js:188` enforces
`["pd","copyright","none"]`. `"generative"` is not a live value and
`"copyright"` is undocumented. Any A1 vocabulary work must fix this first.
*(Recorded as E-009.)*

## 2. The missing no-image surface — scoped

Cover substitution for an **artwork record** happens at six sites:
`js/app.js:879` (cards), `1831` (list entries), `2037` (arc strip), `2204`
(detail hero), `2246` and `2248` (the two mini-card rails). Note that **2246 and
2248 gate on `o.image && o.image.src` only — no status check**; they are correct
today solely because all 61 `status:"copyright"` records carry no `src`
(verified: 61 copyright image blocks, 0 with `src`). Any option that withholds an
image by moving the token while *keeping* `src` would leak that image into those
two rails.

Four further sites substitute an artist-seeded cover onto another entity when a
work is unrenderable: `1580` (museum card), `1719–1720` (actuality), `1773`
(list card), `1810–1811` (list hero). Four pool filters already behave
metadata-only: `1485`, `1609`, `3363`, `2476/2495`. Prerender:
`tools/build_seo.jxa.js:103,177` — 337 of 398 artwork stubs carry `og:image`; a
withheld record needs a defined fallback.

So: **10 render sites, 4 pools, 1 prerender path, plus new CSS box states**
(`.aw-hero-gen`, `.card-art`, `.arc-work-gen`, `.le-art`, `.mc-img` all size to a
canvas) and accessible-name work. That is a medium feature, not a one-liner and
not a rewrite. It is **unambiguously OP-INTERFACE** — `OP-RIGHTS.md:53–55` bars
rendering logic in `js/app.js` and all of `css/`. The revision's framing is
correct; the refusal to couple A3/B1 to C3 is also correct, since one
record-scoped state serves both.

## 3. The successor guard

Both prior proposals fail: the literal filter
(`tests/test_rights_tooling.py:1352`) is dodgeable by migration; "count every
conditional-basis record" makes owner-selected states permanent offenders. Count
neither. **Count the mismatch between what Pigment's token declares and what the
census measured for that exact file.**

Concrete test, replacing `TestPdTokenAccuracy` (three counted assertions, all
printing):

1. **Vocabulary integrity, ceiling 0.** Collect every distinct `status:"…"`
   literal in `js/catalog-*.js`. Assert the set equals a pinned `BASIS_TOKENS`
   table in the test, and that every member appears in the
   `validate.jxa.js:188` enum and in `ARTWORK_SCHEMA.md` §3. A new token cannot
   exist without a reviewed row.
2. **Basis mismatch, ratchet 6.** Each `BASIS_TOKENS` row declares what the
   token asserts, as three measurable predicates against
   `artwork-image-rights.json`: `credit_required`, `license_short` family, and
   whether `author` is non-empty. Offender = a rendered record whose token row's
   predicates do not match its census entry. Today: the five (`pd` declares
   no-credit-required; census says `credit_required: true`) plus
   `the-ten-largest-no-9` = **6**. Under A1 the five migrate to a row declaring
   *CC licence, named licensor* — which matches — so the count falls to 1
   **because the assertion was reconciled, not because a string changed**. Under
   A4 it stays 6. Under A2 it falls when the census changes. A token invented to
   escape the count fails assertion 1, and a token added to the table with
   mismatched predicates makes every record on it an offender.
3. **Attribution continuity, ceiling 0 — token-agnostic.** For every census
   entry with `credit_required: true` whose `src` appears anywhere in
   `js/catalog-*.js` or `js/artworks.js`, assert its `commons_title` is a key in
   `js/photo-credits.js`, **and** that the record's token is one `js/app.js`
   renders a credit for. This is the only guard that catches the A1 regression in
   §1, and it is unaffected by vocabulary entirely. Extends the existing
   `test_every_such_record_is_actually_credited` (line 1366), which already
   iterates the census rather than the catalog — the right instinct, just not
   wired to the render path.

Print: `basis mismatch: N (ceiling 6) · credit-required rendered: K ·
uncredited: 0`. **Negative controls** (three, per `INFLUENCE_SOURCING.md:95`):
add an unpinned token → assertion 1 exits 1; repoint a `pd` record at a CC BY
file → N rises; delete an `IMAGE_CREDITS` row → assertion 3 exits 1.

## 4. E-006's fix

Identity is discarded twice. Primary loss: `tools/commons_rights.py:113–119`,
`strip_html` — `re.sub(r"<[^>]+>", "", s)` drops the
`<a href="…/wiki/User:Sailko">` and keeps only the display text, before
`rights_from_imageinfo` (line 203) writes `author`. Second loss:
`tools/build_photo_credits.py:67–77`, `plain()`, identical regex; but by then the
href is already gone from the census, so **fixing `build_photo_credits.py` alone
cannot work.**

Minimal fix: in `commons_rights.py`, before stripping, capture
`/wiki/(User:[^"#?]+)` from `Artist`/`Credit` anchors into a new census field
`author_account`; leave `author` unchanged. Then `build_photo_credits.py:156`
emits an optional `authorAccount` alongside `author`. No renderer change needed —
`credit_literal` (line 103) already emits optional keys.

Regeneration effect: re-running `audit_artwork_rights.py` is a live network call,
so the diff is not knowable offline. On `js/photo-credits.js` it adds one key to
at most the 23 `IMAGE_CREDITS` rows and rewrites the `Generated:` header date. On
the ledgers: `TestAssetInventory` (1199–1286) keys on **image URLs**, not credit
fields, so it should not move — but
`test_reproduces_the_frozen_inventory_plus_recorded_corrections` fails on *any*
undeclared surface drift, so a re-audit that also refreshes a `license_short` or
flips a `credit_required` would need a new declared ledger. **Scope gap to
record:** `tools/` is **not** in OP-RIGHTS' may-write table
(`OP-RIGHTS.md:41–47`), which names those tools only as the permitted route to
other files. The E-006 fix needs that scope widened or the dependency filed.

## 5. Verdict on §5 criterion 5

**Feasible, with two named exceptions and one correction to the brief's cost
model.**

- **Feasible now, inside OP-RIGHTS' scope:** A2, A4, B2, B3, B4, C1, and the
  E-006 fix (subject to the `tools/` scope note).
- **Feasible but blocked on an OP-INTERFACE dependency, not on any unknown:**
  A1, A3, B1, C2, C3, C4. The blocker is the record-scoped no-image state — 10
  render sites, 4 pools, 1 prerender path, new CSS. No research is required to
  build it; it simply is not RIGHTS-001's to write.
- **Not feasible as written:** A3 and B1 *as independent, immediately-selectable
  options*. The revision's framing already fixes this by declaring the
  dependency, and I endorse that framing over CH-1's coupling.
- **Correction the record should carry:** the brief and both rounds treat A1 as
  vocabulary hygiene. It is not. Executed without the paired render change it
  **removes attribution from five files that require it** — the opposite of the
  task's purpose. A1 must be specified as one bundle with the credits path, or
  not selected. *(Recorded as E-008.)*
- **What I cannot confirm:** nothing legal, which is not mine; and no
  post-regeneration ledger delta for E-006, because `audit_artwork_rights.py`
  requires a live Commons fetch I have not run and would not run without
  authorization.

I have not confirmed feasibility for any option requiring the successor guard to
*already exist* — it does not, and §3 above is a design, not an implementation.
That guard should be a named deliverable of the specification, not an assumption
in it.
