# Branch adoption decisions for the owner

Scope: read-only comparison on the elevate worktree after the rights merge. No branch was checked out, merged, committed or executed for this assessment. These are decision inputs, not recommendations to merge or reject.

## Evidence and current health

| Reference | Inspected commit |
| --- | --- |
| elevate HEAD, rights merged | `7bd28ebae19546fe196f9d7844bd06f0d2cf1d34` |
| duo/lane-iv-and-fixes-0236 | `efa091d5a1de6a7c33d6757b67443e99180109de` |
| codex/moderna | `f2b9b7893af9d2cce2efd53550ddd4482913c2e1` |

**Measured by Claude, as supplied in the session handoff:** both branches pass the suite and validator alone, and merge cleanly together with the rights branch. Those checks were not rerun by Codex here; this handoff does not supply their full logs, command versions or combined commit ID. Clean merging demonstrates textual compatibility, not constitutional adoption, visual acceptance or consistent image policy. Concurrent elevate edits are outside these branch snapshots.

## duo/lane-iv-and-fixes-0236 — Dual-Build constitution and harness

### What changes

The branch diff contains 14 files, 1,374 insertions and 62 deletions:

- `CLAUDE.md`: adds opt-in Lane IV and §1b, gives both build models implementation and cross-review roles, defines session-record authorization and extends the sealed set. Updates the machine-runtime note while retaining Pigment's zero-build architecture.
- `AGENTS.md`: adds the Codex-facing constitution, explicitly requiring substantive agreement with CLAUDE.md.
- `.claude/hooks/sealed-set.py`, `.codex/hooks/sealed-set.py`, `.codex/hooks.json`: extend the guarded paths and activate protection under the Lane IV flag; add Codex hook configuration.
- `tools/lane4-run.sh`: one turn for either harness, session record read from main, isolated worktree, hook checks, wall-clock limit, verifier commands, diff ceiling, resulting branch and optional push. It does not itself orchestrate the full two-model debate or merge.
- `tools/lane3-run.sh`, `tools/lane3_writ.py`: expand sealed paths and account for untracked additions in the final sealed-path check; change protocol-path exceptions in the shared record parser.
- `tests/test_lane3.py`, `tests/test_lane4.py`: guard and runner coverage.
- `protocol/duo-sessions/README.md`, `protocol/duo-sessions/lane-iv-framework/synthesis.md`, `protocol/duo-sessions/lane-iv-framework/transcript.md`, `protocol/oriented/README.md`: document the new mechanism, deliberation and its relationship to oriented protocols.

### What adoption commits the owner to

The owner would adopt a fourth authorization mechanism: a scoped session record committed on main before execution, with explicit opt-in each time. Both models may build and must review the other's changes; neither certifies its own work. The Theory Team's separate non-building role remains. Runs do not merge; the owner retains adoption and deployment decisions.

The owner also takes on maintaining two equivalent constitution files and two harness integrations. Sealed paths now include AGENTS.md, `.codex/` and Lane IV tooling. Routine sessions cannot amend their own graders or authority; those changes need owner-led handling outside a guarded run.

### Risks and open questions

- The new authority is substantive even though tests pass. Is the owner adopting the complete model, or considering the independent guard repairs separately? A split would need an explicit scope and a new validation record.
- The Codex hook command in `.codex/hooks.json` contains the absolute path `/Users/ardagemci/Claude/painters-atlas/.codex/hooks/sealed-set.py`. What installation/worktree arrangement guarantees that this resolves to the intended version on another checkout or machine?
- Hook decisions are exact for named edit tools but shell matching is a blocklist. Runner checks are a second line of defense; neither passing tests nor comments describing a guarantee establish protection against arbitrary shell programs. Review untracked/ignored paths, path quoting and report-directory exceptions as explicit boundaries.
- The shared writ parser allows both `protocol/runs` and `protocol/duo-sessions` prefixes, while each runner's final check uses a narrower report exception. Confirm that parser acceptance and actual write authority agree for each lane, including sibling session paths.
- Lane IV's runner reuses `status: granted` parsing while its comments describe that field as inert. The record's presence on main supplies authorization. Is that clear enough to avoid treating a draft record as an approved session?
- The runner executes one agent per invocation and leaves cross-review to the workflow. Who records the review, resolves disagreement and verifies it happened before owner review? This is not established by a green runner exit.
- The branch names specific model versions and depends on CLI flags, including hook-trust handling. Who maintains these assumptions? No current external CLI compatibility check was performed here.

The branch's `protocol/duo-sessions/lane-iv-framework/synthesis.md` explicitly says the runner was tested with a synthetic session in a throwaway repository, but a complete dual-build round against the project's own main remained unexercised. Claude's suite/validator handoff does not by itself close that end-to-end gap.

### Before an adoption merge

Record the owner's constitutional decision and intended scope; review CLAUDE.md/AGENTS.md agreement and report-path authority; resolve or document the hook installation assumptions; attach Claude's exact suite/validator and integration evidence. Demonstrate the intended supported harness setup and cross-review handoff with a bounded session before relying on the new mechanism. If the branch changes during review, validate the resulting diff again.

**Lane and authority:** constitutional owner decision, conducted with the owner present under the current Lane II handling of constitution/verifier changes. It cannot authorize its own adoption as a Lane IV run or be treated as routine Lane III maintenance. Any change to Pigment's product identity or promises remains Lane I under the constitution's routing rule.

## codex/moderna — living-exhibition design study

### What changes

The diff contains six files, 365 insertions and one deletion:

- `js/app.js`: installs a new homepage renderer (retaining `viewOriginalHome`), adds a five-work exhibition, alternative entrances and editorial sections, rearranges artwork identity/actions beside the image, and disables the prior ambient background invocation.
- `css/studio.css`: adds a shared visual layer affecting more than the two opening pages, including typography, themes, controls, layout and onboarding swatches.
- `js/studio.js`: adds Wall/Index, rehang, pointer/keyboard arrangement, a procedural WebGL field and a motion control, with reduced-motion and lifecycle handling.
- `index.html`: loads those new assets and adds **`noindex,nofollow`** for the preview.
- `docs/DESIGN-STUDY-moderna.md`: records direction, research, sampled browser checks and limitations.
- `docs/app-review-moderna.patch`: preserves a review patch; determine whether it remains useful as history or could be mistaken for a patch still needing application.

The design study reports route, phone/desktop, drag, motion, onboarding and Passport samples. Its original verification section says no full suite or independent certification was performed at that stage. Claude's later passing-suite handoff above updates automated health; it does not supply the missing comprehensive accessibility or independent visual review.

### What adoption commits the owner to

The owner would choose a spatial exhibition as the homepage's main presentation and interaction, and accept a broad CSS layer across existing routes. That means maintaining both ordinary links and optional drag/motion behavior, including keyboard, touch, reduced-motion and graphics-failure states. The study retains existing data, taste logic and actions; the prominence and discoverability of the loop's entrances still need user observation.

### Risks and open questions

- The preview robots tag would discourage search indexing if shipped unchanged. Decide production metadata explicitly before deployment; a clean merge does not remove this tag.
- Both the initial wall selection in js/app.js and rehang in js/studio.js test status `pd` directly. The merged rights policy has four tokens and permits `licensed` with a src. Is this an intentional curatorial restriction or an accidental eligibility divergence? Resolve it against the shared rendering contract; it is not evidence that the branch displays withheld records.
- Shared CSS and the disabled ambient background affect routes beyond homepage/artwork. Does the result work in both themes, narrow layouts, long titles, missing images and withheld-image states?
- The study explicitly leaves comprehensive accessibility, VoiceOver, lower-end hardware, WebGL context loss and all export/import/share branches uncertified. Drag affordances, keyboard activation and native touch scrolling need independent review.
- The experimental homepage changes entrance prominence. Does the exhibition help new visitors start and finish onboarding, or distract them? Use the owner-led loop kit to gather observations; visual preference alone cannot answer this.
- Source links and fallback copy meet concurrent rights/interface work in js/app.js. Inspect the final composed behavior even if git reports no conflict. The new presentation has no accompanying regenerated p/ stubs in its branch diff.
- The study document describes an earlier copied scratch prototype and cites Node syntax checks. Those are historical claims, not instructions for Pigment's toolchain or a precise description of the current branch delivery. Reconcile its handoff language for any production package; use the project's Python/JXA validation workflow.

### Before an adoption merge

Record which visual direction and interaction scope the owner accepts; resolve the preview robots tag and status-predicate question; review the final merged interface against the rights contract. Attach independent desktop/mobile, both-theme and keyboard/accessibility evidence, including image fallback and graphics-failure behavior. Use observed loop sessions to assess discoverability. Reconcile the study's historical scratch wording, confirm affected prerender metadata, and re-emit affected surfaces where the interface contract requires it. Attach Claude's automated evidence to the resulting review package; changes made afterward need their relevant checks.

**Lane and authority:** Lane II for an owner-directed visual exploration/adoption that retains identity, promises and navigation shape; owner visual approval and independent quality review are distinct. If the proposed adoption changes those product commitments or introduces a new promised surface, route that scope through Lane I / OP-INTERFACE with a frozen specification. Lane III cannot decide whether the design is right, and the unadopted Lane IV branch supplies no automatic authority.

## Reproduce the read-only assessment

```sh
git rev-parse HEAD duo/lane-iv-and-fixes-0236 codex/moderna
git diff --stat HEAD...duo/lane-iv-and-fixes-0236
git diff HEAD...duo/lane-iv-and-fixes-0236 -- CLAUDE.md AGENTS.md .claude/hooks/sealed-set.py .codex/hooks.json tools/lane3-run.sh tools/lane3_writ.py
git show duo/lane-iv-and-fixes-0236:tools/lane4-run.sh
git diff --stat HEAD...codex/moderna
git diff HEAD...codex/moderna -- index.html js/app.js
git show codex/moderna:js/studio.js
git show codex/moderna:css/studio.css
git show codex/moderna:docs/DESIGN-STUDY-moderna.md
```

Triple-dot diffs describe each branch's changes since its merge base, not a simulated merge into current elevate. The integration-health statement above is attributed to Claude's measurements, not inferred from these commands.
