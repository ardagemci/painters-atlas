# RIGHTS-001 — Final Synthesis

Round 2 · `claude-synthesis-lead` · `final_synthesis` → `awaiting_build_approval`

**This synthesis does not recommend freezing a specification.** §3 gives the
reasons against `PROTOCOL.md` §5, criterion by criterion. It states no legal
conclusion and decides none of A, B, C or D — those are the owner's, and §2
restates them so they can be chosen from truthfully, which two of them could not
be before.

---

## 1. What changed after the poles stopped arguing

Rounds one and two ran with `analyst_count: 0` and no specialist report of any
kind (D-002). Three specialists were then brought in. **Each found something both
poles had missed**, and two of the findings change what an option *means* rather
than what it costs.

| # | Finding | Effect |
|---|---|---|
| **E-008** | The inline credit is gated on `hasImg` (`js/app.js:2228`) and `creditUsage()` filters `status === "pd"` (`js/app.js:2495`) | **A1 executed alone removes attribution from the five files.** Credits vanish; the records drop off `#/credits` |
| **E-007** | `js/artworks.js` holds 581 image entries and **zero** `status` fields; 19 of the 23 credited files also live there | **B1 does not remove the af Klint image from the site**; A3 does not remove the Degas one |
| **E-010** | `author` comes from extmetadata `Artist`, which sometimes resolves to the depicted work's creator | Two CC BY 2.0 files credit the **painter** where the page names a photographer |
| **E-006** | One Commons account recorded under two display names | Four files, not two; A2's cost was understated |
| **E-009** | Schema documents `"pd" \| "generative" \| "none"`; validator enforces `["pd","copyright","none"]` | A record authored to the schema fails the build |

The pattern is one this project has a name for. Every round argued about which
*token* a record should carry. Nobody checked what the token was wired to. The
token turned out to gate the credit, gate the credits index, and not gate the
second registry at all — so the vocabulary debate was a debate about a proxy,
and the thing itself was three functions away.

## 2. The decisions, restated truthfully

Options unchanged in substance; consequences corrected. **The owner chooses.**

### Decision A — six records carrying `pd` over CC-asserted files

| | corrected consequence |
|---|---|
| **A1** new basis token | **Not selectable alone.** Bundled with the credits path it is a real option; executed as vocabulary work it removes attribution from five files that require it (E-008). Also inherits the enum contradiction (E-009). `js/app.js` is outside OP-RIGHTS' scope |
| **A2** re-source | Cheapest of the four, inside scope, with precedent — `triumph-of-death` left this set exactly this way. Cost concentrated, not spread: one account supplies four of the 23 credited files (E-006) |
| **A3** withhold | Blocked twice: no blank state exists (CH-1), and the artist-page registry is ungated (E-007). Requires the record-scoped metadata-only capability |
| **A4** dated exception | Free. No code moves. Debt stays visible and counted |

### Decision B — `the-ten-largest-no-9`

| | corrected consequence |
|---|---|
| **B1** metadata-only | **Does not do what it says.** The file is in `js/artworks.js` and would keep rendering on the artist page (E-007) |
| **B2** seek provenance | Unchanged. The one route that could retire the conflict rather than route around it |
| **B3** bounded expert review | Unchanged |
| **B4** dated exception | Free, and the record already carries the painter as author (E-010) |

### Decision C — the 61 procedural covers

Unchanged by this round, and the narrowest of the four. E-001 established the
covers sample no artwork pixels; the palettes are authored, so **C2 removes
editorial content rather than a derivation**. Dürer scopes C2 at ~24 call sites
and C3/C4 at the same missing capability as A3/B1. C1 is free.

### Decision D — jurisdiction

Unchanged and still gating. Hogarth's point stands: **D cannot be chosen the way
A, B and C can, because its option set omits the input that makes any of them
commissionable — the owner's country and operating form.** One sentence supplies
it. It is the cheapest movement available anywhere on this task.

### Proposed Decision E — attribution accuracy beyond the six

E-006 and E-010 are **not** confined to the six records and belong to no existing
decision. Two CC BY 2.0 files name a painter dead 76 and 234 years as the author;
one account appears under two names across four files. The root cause is one line
(`tools/commons_rights.py:118`) discarding the anchor `href`.

Seurat's fix is ~4 lines, adds a field, changes no rendered string, and moves no
count — and he declined to rewrite the credits as a side effect, because the
display text is what each file page asks for and overriding it is an owner
decision. **That is Decision E, and it is the only new decision this round
produces.** `tools/` is outside OP-RIGHTS' write scope, so it carries a
dependency to file rather than a scope to widen.

## 3. Convergence assessment — `PROTOCOL.md` §5

| # | Criterion | Holds? |
|---|---|---|
| 1 | Intended user outcome explicit | yes |
| 2 | Material assumptions documented | yes — 10 findings in the decision record |
| 3 | Critical objections resolved or recorded | recorded |
| 4 | IA and main flows coherent | **no** — two image registries with different gating (E-007) is an incoherence, not a preference |
| 5 | Technically feasible, Implementation Lead confirmed | **qualified yes** — A2, A4, B2, B3, B4, C1, E in scope; A1, A3, B1, C2, C3, C4 blocked on an OP-INTERFACE dependency |
| 6 | Acceptance criteria testable | **no** — the round-one criterion 5 was shown satisfiable by a change that resolves nothing (CH-2); its successor exists as a design (Dürer §3), not an implementation |
| 7 | Deviations visible in the Decision Record | yes |
| 8 | No unresolved critical risk hidden | yes — recorded, not hidden |
| 9 | Remaining disagreements noncritical or genuinely require the owner | genuinely require the owner |

**Three of nine do not hold. Convergence is not recommended and no specification
should be frozen on this record.** Criteria 4 and 6 are the substantive blocks;
neither needs research, and both have named remedies.

## 4. What would close it

In cost order, cheapest first:

1. **One sentence from the owner:** country and legal operating form. Unblocks D,
   which gates precise answers to A, B and C. Costs nothing.
2. **Decision E and its ~4-line fix**, with the `tools/` scope dependency filed.
   Independent of D, and it repairs credits that are wrong today.
3. **Build Dürer's successor guard** (his §3) — three counted assertions keyed to
   token/census *mismatch* rather than to a literal string, with three negative
   controls. Satisfies criterion 6 and cannot be passed by a vocabulary change.
4. **An OP-INTERFACE task for the record-scoped no-image state** — 10 render
   sites, 4 pools, 1 prerender path, new CSS. Unblocks A3, B1, C3, C4 and makes
   A1 safe. This is the criterion-4 remedy and it is not RIGHTS-001's to write.
5. **Then re-run convergence.** A and B can be decided at (1); they cannot be
   *implemented* as written until (4).

## 5. What remains unknown

Which jurisdiction governs the owner's exposure, and whether the answer differs
for owner, United States host and reader. Whether the rendered credits satisfy
the attribution terms of the versions in use — asked per version, since 2.0, 2.5
and 3.0 terminate on breach without cure and 4.0 grants thirty days. Whether
serving a 500px Wikimedia thumbnail is Adapted Material under CC BY-SA. Who
applied either af Klint template, and whether the Stiftelsen notice claims the
work, the photograph, or is boilerplate. Whether "Sailko" and "Francesco Bini"
are one natural person — Commons asserts the link and an assertion is all it is.
How the 279 palettes were authored, which only the owner can answer.

Each is named with the evidence that would resolve it in
`evidence/hogarth-03-synthesis-review.md` §5 and
`evidence/seurat-01-credit-integrity.md` §5.

## 6. Procedural record

This synthesis was produced without a Synthesis Liaison packet, as were rounds
one and two (D-001, owner-instructed). `analyst_count` remains 0 and the
Coordinator has not ingested any message on this task; `state.json` has been
reconciled by replaying `engine.ingest`'s state writes, and
`TestTaskStateMatchesTheMessageLog` now fails the build if it drifts again.
Gate 1 is untouched: `build_authorized: false`, and nothing in this round edited
a production file.
