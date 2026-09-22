# Open decisions for the owner

**Duo session `unsolved`, 2026-09-17.** Every open question on Pigment that is
waiting on *a person* rather than on engineering, in one place. Each entry states
the options, what each costs, what it unblocks, and which lane the decision
belongs to. Nothing here is decided. The order is the recommended sequence, with
cheapest and most unblocking first. Reorder it freely.

Why a register at all: nearly every issue still open on the site is open because it
waits on one of these. Engineering can prepare a decision. It cannot make one.

---

### 1. Merge the two stacked duo branches
**Branches:** `duo/elevate-1629` (12 commits), and `duo/unsolved-1229` stacked on it.
**Options:** merge both · merge only `elevate` · merge neither.
**Cost:** a review of two diffs. Both are green (213 tests, validator 0).
Neither was loaded in a live browser from these sessions (see the caveat below).
**Unblocks:** everything below that cites `js/renderable.js`, the gallery
withholding fix, the notice rewrites, and the reconciliation table.
**Lane:** II.
**Caveat that belongs to this decision:** the preview tooling serves the primary
checkout, so the app was never loaded live. Equivalence was proved instead, over
all 398 records and 280 artists, and every prerendered stub regenerates as
predicted. One manual page load before merging is still worth doing.

### 2. Apply the PIGMENT.md reconciliation
**Source:** `pigment-reconciliation.md` in this folder (31 items; 13 stale).
**Options:** apply the §12/§15/§16 factual corrections now and route §19 separately
· apply all at once · defer.
**Cost:** small. The one judgement is that **§19 D-6's rationale is untrue as
written.** It defers instrumentation because the product makes "zero third-party
runtime requests", but every catalog image loads from `upload.wikimedia.org`. The
honest restatement changes the privacy argument D-6 rests on.
**Unblocks:** every future contributor orients from an accurate document.
**Lane:** II for §12/§15/§16 · **I for §19** (promises).

### 3. Lane IV and `codex/moderna`
**Source:** `../elevate/branch-assessments.md`.
**Options, each branch:** adopt · reject · hold.
**Cost:** Lane IV rewrites `CLAUDE.md` and the sealed set, so it is a
constitutional change. Moderna is a homepage and artwork-page redesign study.
**Recommendation on sequence only:** decide moderna *after* decision 4's study,
which will show whether the homepage is where people actually stall.
**Lane:** I (Lane IV) · II (moderna).

### 4. Run the loop study
**Source:** `docs/LOOP_STUDY_PROTOCOL.md`, ready to use.
**Options:** run 5 sessions now · run fewer · defer.
**Cost:** about 2.5 hours of your time, plus recruiting five people. No code and no
instrumentation.
**Unblocks:** decisions 5, 6 and 7, and the Phase 2 gate. **Pigment has no evidence
yet that its core loop works for anyone who did not build it**, and PIGMENT.md §16
gates accounts on exactly that.
**Lane:** II.

### 5. D-1 — the adaptive onboarding deck
**Fact:** `buildDeck()` stratifies the deck up front and never re-reads answers
mid-deck (PIGMENT.md §19 D-1; `docs/ADMIRE_SPEC.md:100`).
**Options:** implement response-adaptive delivery · revise the claim everywhere it is
made · keep stratified delivery and say so plainly.
**Cost:** implementing it is the largest product change on this list, and it is
**bounded by a constraint no content can lift**. The calm-abstract quadrant (F+D−)
holds one showable work, because calm abstraction is Rothko and in copyright
(`docs/BACKLOG.md:758`). An adaptive deck will probe that corner with almost
nothing to show.
**Unblocks:** D-5 (visible confidence is only worth showing once the reading is
trusted).
**Lane:** I.

### 6. D-6 — instrumentation
**Options:** none · first-party, privacy-preserving counts (did onboarding finish,
was a result shared) · a third-party analytics service.
**Cost:** see decision 2. The current "zero third-party requests" framing is not
accurate, so this has to be decided from an honest description of what the page
already requests.
**Lane:** I (it is a promise about privacy).

### 7. D-2 — museum one-hour routes
**Fact:** the Style Guide calls the route the museum page's hero unit, and no museum
page has one.
**Options:** curate routes for the strongest museums first · redefine the hero unit
· defer.
**Cost:** editorial and art-historical work per museum (Vasari, Van Gogh). Each
route makes claims about real works that someone must check.
**Lane:** II.

### 8. IFACE-001 — the rest of the gallery
**Fact, as of this session:** a gallery image whose matching catalog record is
withheld is no longer shown. **402 gallery entries have no catalog match** and stay
ungated.
**Options:** gate unmatched entries (show none without a catalog basis) · add a
status field to `js/artworks.js` · leave them as they are and record why.
**Cost:** the Theory Team's brief is still owed. Evidence for it is in
`protocol/tasks/IFACE-001/evidence/cross-registry-identity.md`.
**Lane:** I.

### 9. The validator's copy of the renderability rule
**Fact:** `tools/validate.jxa.js` still spells the rule out inline. Its agreement test
is **measurably blind** to any regression that does not push a deck quadrant below
two works. A negative control showed this on 2026-09-15.
**Options:** have the validator evaluate `js/renderable.js`, as `build_seo` does ·
leave it.
**Cost:** a small edit, but to a **sealed verifier**. That is why it waits for you.
**Lane:** II, with you present.

### 10. RIGHTS-001 Decision C — the 61 procedural covers
**Options:** C1 keep · C2 artist-neutral placeholders · C3 metadata-only · C4 pause
pending review.
**Cost:** C2 removes authored editorial content rather than a derivation (no artwork
pixels are sampled). C3 and C4 need the IFACE-001 no-image state first.
**Lane:** I.

### 11. RIGHTS-001 Decision E — who a credit names
**Fact:** one Commons account is credited under two names across four files, and
two CC BY 2.0 credits name a long-dead painter rather than the photographer the
file page identifies. The census now carries the account behind every credit.
**Options:** show the display text the page gives · show the account · show both.
**Lane:** II, with the licence question going to counsel.

### 12. Counsel
**Fact:** residence is Türkiye (RIGHTS-001 D-010). The questions are drafted and
the census is assembled.
**Options:** engage one Turkish practitioner for the attribution questions ·
defer.
**Lane:** owner only.

### 13. The three notices left over budget
Melencolia I, the Burial of the Count of Orgaz and the School of Athens each hold
more facts than 12 words allow, so they were left over budget rather than cut.
**Options:** accept · rewrite and lose a fact · split into two bullets.
**Lane:** II.

### 14. When Phase 2 begins
**Options:** after decision 4's evidence, as PIGMENT.md §16 requires · earlier.
**Cost of starting:** Pigment would begin storing user data and hosting what people
post. That means takedown duties and moderation before any social discovery
(PIGMENT.md §11, Phase 4), and **OP-PLATFORM has no staff yet**. See the roadmap.
**Lane:** I.

---

**Closed since the last register:** §19 D-3, Taste in the header nav, which is
already shipped (`index.html:59`). It was listed as open in PIGMENT.md, in last
session's future steps, and in this session's own first debate turn.
