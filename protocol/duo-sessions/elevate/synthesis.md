# Duo `elevate` — synthesis and outcome

Branch `duo/elevate-1629`, base `origin/main` at `352b276`. Three debate rounds,
Codex wrote `AGREE` in round 3. Not merged or pushed.

## Agreed plan, as built

| # | Deliverable | Owner | Commit |
|---|---|---|---|
| A | Merge the owner-decided rights branch (D-010, D-011) | Claude | `7bd28eb` |
| B | One renderability predicate, `js/renderable.js`, shared by `js/app.js` and `tools/build_seo.jxa.js` | Claude | `016d6ab`, `fa2f83f`, `2558ed1` |
| C | Behavioural tests: executed predicate, executed Python tools on fixtures, record-ID agreement, the validator actually run | Claude (shaped by Codex) | `fa2f83f`, `73d1d0f`, `c89d7e6` |
| D | Cross-registry identity evidence for IFACE-001 | Codex (verified by Claude) | `e30e953` |
| E | Owner-led loop study kit | Codex | `e30e953` |
| F | Assessments of the Lane IV and moderna branches | Codex | `e30e953` |
| G | Future steps toward the north star | Claude | `ecaa8f9` |

## Decisions the debate changed

- **Round 1, Codex:** the predicate refactor is a *prerequisite*, not IFACE-001's
  closure, because `window.ARTWORKS` has no status. A coverage report measures
  fragility, not enjoyment, and the validator already counts quadrant anchors.
- **Round 2, Claude:** "curate a second calm-abstract work" was already closed
  (`docs/BACKLOG.md:758`). Neither agent can run a usability study; build the
  kit for the owner instead.
- **Round 2, Codex — the decisive point:** *all evaluators can agree on the same
  bug.* Tests execute production code against written-down answers and compare
  by record ID, not URL.
- **Round 3, Claude:** the IFACE-001 theory brief belongs to the other pole.
  Evidence for it is the Claude pole's to produce.
- **Round 3, Codex:** Commons titles establish shared assets, not artwork
  identity. Classify matches rather than forcing them, and keep generated
  prerender output distinct from checked-in stubs.

## Tiebreaks and deviations

- **Validator coverage.** Codex wanted the validator's eligibility logic run
  directly. It is a sealed verifier, so it is run and its outputs are checked
  instead. A negative control then showed this check is blind to any regression
  that does not push a deck quadrant below two works. That limit is written into
  the test. Closing it is a verifier edit for the owner.
- **Name.** The synthesis said `renderableImage(w)`, but the build kept
  `isRenderable`. D-011, two tool docstrings (one in a sealed file) and a test
  all name it, and keeping the name keeps them true.

## Found during the build, not predicted in the debate

- The rights branch moved 13 sites to `isRenderable` and missed **five** that
  checked `src` with no status: three in `js/app.js` and two in the prerender
  (museum-stub and list-stub `og:image`). The structural guard found the
  prerender pair on its first run.
- The Snail's gallery entry is only *latently* a conflict: the artist page's
  Major works panel renders `window.ARTWORKS` ungated and is hidden only for
  artists with a Tier-1 arc (166 of 196 gallery artists have none).
- Codex's cross-review turn hit its usage limit after one fix, so the independent
  second review was partial.
