# RIGHTS-002 — Decision Record

Living document (Gate 3). OD-5 binds: nothing here states a clearance.

## D-000 — Opened, and executed in Lane II without deliberation

- **What:** RIGHTS-002 opened at `intake` on 2026-09-03 as a split of RIGHTS-001
  (D-004), and executed the same week **in Lane II** — no theory brief, no
  challenge, no synthesis, no specification, no liaison packet. `messages/` and
  `analyses/` are empty and correctly so.
- **Why that was legitimate:** `CLAUDE.md` §0 routes work by three questions.
  This change is a four-line carrier field in a tool, its correctness is decided
  by measurement rather than by looking at a page, and **the owner was present**
  — which is exactly Lane II's authorisation. The owner chose that route
  explicitly (RIGHTS-001 D-009), including the `tools/` scope question the OP
  boundary would otherwise have raised.
- **What it cost, recorded rather than glossed:** OP-RIGHTS' declared write scope
  excludes `tools/`, and this task wrote there anyway. No cross-OP dependency was
  filed. The second such bypass should be visible as the second.
- **Status:** accept (owner).

## D-001 — The fix, and what was deliberately not changed

- **Defect (RIGHTS-001 E-006, E-010).** `tools/commons_rights.py` `strip_html`
  discarded the anchor in every extmetadata value, keeping only the text node.
  `Artist` arrives as `<a href="…/wiki/User:Sailko">Sailko</a>` on three files
  and `<a href="…/wiki/User:Sailko">Francesco Bini</a>` on a fourth — identical
  but for the display text. The identity was fetched and thrown away, so nothing
  downstream could tell that one account supplied four files, or that an author
  field named the depicted work's painter rather than a photographer.
- **Fix.** `first_href()` captures the first anchor target; the census carries it
  as `author_href` and `credit_href`, sibling fields beside the unchanged
  strings.
- **Deliberately not changed: the rendered credit.** `js/photo-credits.js` still
  shows exactly what each file page displays. Overriding what a licensor asked to
  be called is an owner decision, not a tool's — Seurat's position, adopted. This
  task makes the discrepancy *visible and enforced*; it does not resolve it.
- **What the census now surfaces mechanically:**

  | | |
  |---|---|
  | `User:Sailko` | recorded as both `Sailko` and `Francesco Bini` |
  | `Mrs. Siddons…` (CC BY 2.0) | author anchor → `en:Joshua_Reynolds`, d. 1792 |
  | `Max Beckmann, Departure` (CC BY 2.0) | author anchor → `en:Max_Beckmann`, d. 1950 |

- **Guard.** `TestAuthorIdentity` — two ratchets and a vacuity check. Split
  accounts ceiling 1, painter-as-author ceiling 2. Both count what the *source*
  asserts, so neither can be satisfied by relabelling. The third assertion fails
  if `author_href` stops being populated, because a ratchet reading a field the
  tool no longer writes passes while measuring nothing. All three proved
  non-vacuous by recorded negative controls.
- **Not concluded.** Whether a notice naming one party rather than another
  satisfies CC BY 2.0's attribution term is for counsel, under the jurisdiction
  RIGHTS-001 D-006 leaves open between France and Turkey.
- **Status:** accept, executed and verified.
