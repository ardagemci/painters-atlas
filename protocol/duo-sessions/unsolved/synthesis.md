# Duo `unsolved` — synthesis and outcome

Branch `duo/unsolved-1229`, **stacked on `duo/elevate-1629`** (both unmerged).
Merging this branch brings both. Three debate rounds. Codex never wrote `AGREE`,
but its third turn was a precise refinement, which was adopted, not a disagreement.
Lane II (owner-invoked). Nothing was pushed or merged.

One interruption: Codex's usage limit blocked round 1. The owner chose to wait for
the reset rather than proceed solo.

## Agreed plan, as built

| # | Deliverable | Owner | Commit |
|---|---|---|---|
| a | STYLE_GUIDE §4.4 records the owner's 12-word decision (A1) | Claude | `8607e46` |
| c | Gallery art respects catalog withholding; panel extracted and executed in tests | Claude (shaped by Codex) | `08761ce` |
| b | 27 of 30 over-budget notices shortened, facts kept; 22 stubs regenerated | Codex draft, Claude review | `8ba3056` |
| d1 | PIGMENT.md reconciliation table, not an edit | Codex, verified by Claude | `bb5e6a8` |
| d2 | Decision register and roadmap | Claude | `99515c8` |

## Decisions the debate changed

- **Round 1, Codex:** Taste is *already* in the header nav, so PIGMENT.md §19 D-3 is
  drift, not a pending decision. PIGMENT.md is sealed and §19 is Lane I, so do not
  edit it; reconcile it. §12 is a dated snapshot, not a "wrong" one. Fix the writing
  contract (STYLE_GUIDE §4.4 still said ≤8 words) before shortening any copy.
- **Round 2, Codex:** define "withheld" precisely. Claude checked ARTWORK_SCHEMA §3:
  only `status:"copyright"` withholds. A missing `src` is not a decision, and
  `"none"` is undefined as withholding. Using `!isRenderable` would have hidden
  gallery art wrongly.
- **Round 3, Codex:** a helper can be right while the template ignores it, so test
  the renderer's output. Claude extracted the panel so JXA could execute it. The
  negative control that proves the point (the template bypassing the helper)
  failed 7 tests.

## Found during the build

- 25 of 30 rows in Codex's notice table named the *museum* id instead of the
  record id. Rebuilt.
- One rewrite broke Proust's phrase "the little patch of yellow wall". Restored.
  Three others were re-cut for readability. No fact was lost in any of the 27.
- §19 D-6 defers instrumentation because the product makes "zero third-party
  runtime requests". That is untrue: every catalog image loads from
  upload.wikimedia.org.
- 675 of 820 stubs carry og:image. Claude had said all 820 did during the debate.
- The "tap to enlarge" hint fix changes no real artist today. It is defensive.

## Not verified

- A live browser page load: the preview tooling serves the primary checkout.
  Mitigated by the proven equivalence of 279 of 280 artists, byte-identical item
  markup (confirmed independently by Codex), all JS files parsing, and 213 passing
  tests.
