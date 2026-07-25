# BUILD LOG — PIG-001 Wave B (units 11–15)

**Author:** Dürer (`claude-implementation-lead`), Implementation Lead
**Date:** 2026-07-25
**Branch:** `pig-001-stabilization` (never `main`; **not pushed** — `origin/pig-001-stabilization`
remains at `369440e`, the Wave A log commit; the Synthesis Lead pushes at checkpoints).
**Gate 1:** re-verified before any edit — `protocol/tasks/PIG-001/specification.md` exists with
`workflow_state: approved_for_build` and `frozen-sha256:70de6a71…0166`.
**Builds on:** Wave A (`52465b4`…`de9d7f3`, log at `evidence/build-log-wave-a.md`). No Wave A
unit was re-done or reverted.
**Validator:** `osascript -l JavaScript tools/validate.jxa.js` run after **every** unit and after
the commit rebuild; green throughout — `app.js: syntax OK`, `ALL REFERENCES VALID`, snapshot
unchanged (247/75/39/8/37/27/225/115/317(75)/75/103/15/12/36). The two pre-existing deck-pool
WARNINGS (`<2 works with E<=-40`, `empty F×D quadrant 1,-1`) are untouched (unit 22 / OD-4).
**Smoke test (end of wave):** `python3 -m http.server 8421 -d .` → `/` 200 (6189 B),
`css/styles.css?v=20260724-pig001` 200, `js/app.js?v=20260724-pig001` 200,
`js/artists-1.js?v=20260724-pig001` 200, `js/influences.js` 200. Served index carries **20**
`?v=20260724-pig001` tags and **0** unversioned script/css tags; the new `role="combobox"`,
`role="listbox"`, `aria-expanded` and `aria-pressed` attributes are present in the served markup.
**`?v=` treatment:** Wave A already set `css/styles.css` and `js/app.js` to the uniform
`?v=20260724-pig001`. Wave B edits only those two files plus `index.html` (which carries no
`?v=` of its own), so the existing wave string covers this wave — **verified**, no bump needed.

> Gate 2 is **not** certified here — that is Van Eyck's. Browser/viewport/contrast/AT evidence
> (AC15/AC18/AC19/AC20 measurement, screenshots) is Vermeer's and is deliberately not attempted.

---

## Per-unit record

### U11 — canvas cover accessible names (`5eecb98`)
- **Files:** `js/app.js` (`coverLabel` + `canvasTag` at ~:728-732; **all 19 call sites**).
- **Change:** `canvasTag()` emitted `<canvas>` with no accessible name and no fallback content,
  so every generative cover across the atlas was unnamed. The helper now emits
  `role="img" aria-label="…"`, and takes the label as a **new 4th parameter**
  (`canvasTag(style, palette, seed, label, eager, salt)`). A single helper
  `coverLabel(subject)` produces the standard name:
  **"Generative cover for `<subject>`, painted in the browser"** — honest per PIGMENT.md §14
  ("never present generated imagery as the real artwork") and voice-consistent with
  `docs/STYLE_GUIDE.md:57` ("interpretations painted in the browser").
  Subjects: artist name (artist cards, mini-cards, kindred, handoff, museum-artist cards),
  `"<title> by <artist>"` (artwork cards, list entries, arc works, artwork hero, more-by, near-it),
  movement/technique/era/nation/list/museum name, and `hero()`'s `opts.title` (covers all 4 hero
  call sites from one edit).
- **Design choice (recorded):** the brief invited a *single* helper-level change if the call sites
  already passed identifying data. They do **not** — they pass `style, palette, seed`, where
  `seed` is a raw id (and sometimes a suffixed one, e.g. `w.id + "-le"`) drawn from six different
  registries. Resolving a name from an id inside the helper would require guessing which registry
  an id belongs to and would produce wrong names on collision. So the label is passed explicitly
  at each site; the *format* is still centralised in `coverLabel`.
- **Deviation (recorded, minor):** one call site does not use `coverLabel` — the homepage hero
  (`viewHome`), whose cover is the nightly "mixed after <artist>" muse rather than a cover *of*
  a subject. It gets a bespoke but equally honest name:
  "Tonight's generative cover, mixed after `<artist>`, painted in the browser."
- **Verification:** `grep -c 'canvasTag('` = **19**; `grep 'canvasTag(' | grep -v 'coverLabel\|Tonight'`
  = **0 unnamed sites**.
- **Validator:** green.
- **AC:** AC20 (accessible name for every canvas visualization surface — the largest canvas
  surface in the app). Contributes to AC15/AC16's programmatic-identity half.

### U12 — constellation keyboard operability (`980e52a`)
- **Files:** `js/app.js` (`viewInfluences` node/svg markup ~:1084-1106, lede copy; `igFocus`,
  `igClear`, new `igActivate`; new `keydown` + `focusin` listeners on `app`),
  `css/styles.css` (after `.ig-node.sel`, ~:786-792).
- **Change (WCAG 2.1.1):** `.ig-node` `<g>` elements had no `tabindex`, no role and no key
  handler — the graph was click-only and entirely keyboard-inoperable. Each node now carries
  `tabindex="0" role="button"` and an accessible name built from the artist plus relationship
  context (`"<name>, <years>, <n> connections"`), stored in `data-baselabel`. A new `igActivate(g)`
  is the **single** activation path for pointer and keyboard alike, so click behaviour is matched
  exactly: first activation focuses the circle, second navigates to the artist page. `keydown`
  handles **Enter** and **Space** (`preventDefault` so Space does not scroll) and **Escape**
  (clears the selection, leaves focus put). `igFocus` rewrites the selected node's `aria-label`
  to `"… — circle shown; choose again to open their page"` and `igClear` restores every node's
  base label, so the two-step interaction is discoverable non-visually. A `focusin` listener
  scrolls a keyboard-focused node into view **inside `#ig-wrap` only** — it adjusts the wrapper's
  `scrollLeft`/`scrollTop` and never the page. The page lede was corrected from mouse-only
  ("Click a painter…") to "Choose a painter — click, or Tab to it and press Enter — … or press
  Escape to clear."
- **Focus indicator, both themes:** a dedicated `<circle class="ig-ring">` at `r + 5` sits
  *outside* the node fill, so it reads against `.ig-wrap`'s `var(--panel)` in dark **and** light
  rather than against the node's arbitrary movement colour. Styled
  `.ig-node:focus circle.ig-ring{stroke:var(--gold2)}` with
  `.ig-node:focus:not(:focus-visible) circle.ig-ring{stroke:none}` — this shows a ring in engines
  lacking `:focus-visible` and suppresses it for mouse users in engines that have it. Specificity
  checked against the three pre-existing `circle` rules (`.ig-node circle`, `.ig-node.sel circle`)
  so the ring is never repainted by them.
- **Deviation (recorded, corrects the r2 plan):** the r2 unit table specified
  `#ig-svg` gains `role="img" aria-label`. **I did not do that, and it would have been wrong.**
  `role="img"` makes an element a *leaf* in the accessibility tree, pruning its descendants —
  which would have removed the very nodes this unit makes focusable, defeating the unit. The SVG
  instead gets `role="group" aria-label="Influence graph — N painters, M relationships"`, which
  supplies the AC20 accessible name **and** keeps the children exposed. Recorded rather than
  silently diverging (Gate 3).
- **Also recorded:** `#ig-svg.focused .ig-node:not(.lit){opacity:.07}` would have made a
  keyboard-focused non-neighbour nearly invisible while a selection is active; added
  `#ig-svg.focused .ig-node:focus{opacity:1}` so tabbing stays visible mid-selection.
- **Known limitation (for Van Eyck / unit 19):** making ~200 nodes focusable adds ~200 tab stops
  to `#/influences`. That is required by 2.1.1, but AC17's "repeated navigation can be bypassed"
  half is **not** discharged here — the graph has no bypass affordance. Recommend unit 19 (route
  focus / skip-link) add a "skip the graph" target. Not silently absorbed into this unit.
- **Not attempted here:** a full readable text equivalent of the graph. The per-node accessible
  names, the `<title>` tooltips, the `#ig-info` relationship panel (already announced via `#app`'s
  `aria-live`, so no second live region was added) and the artist pages are the current readable
  path; AC20's "meaningful readable alternative" is Van Eyck's call on that evidence.
- **Validator:** green. **AC:** AC17 (keyboard-operable essential visualization + visible focus),
  AC20 (accessible name), AC24 (the relationship journey is now traversable without a mouse).

### U13 — Passport read/write failure UX (`e657cae`)
- **Files:** `js/app.js` (`ppState`/`ppRaw`/`getPassport`/`ppWrite` at :67-97; `passportToggle`;
  `ppNotice` + `PP_WRITE_MSG`; `ppSave`; new `ppTroubleView`; `viewTaste` guard; `[data-pp]`
  handler; `[data-tsx]` branches `export`, `notice-close`, `storage-retry`, `storage-reset`,
  `reset`, `import`; `obFinish`; `adopt`), `css/styles.css` (`.pp-notice`).
- **The three failures found and fixed:**
  1. **Corrupt read silently wiped the Passport.** `getPassport()` swallowed the parse error and
     returned `null`, which is *indistinguishable from "no passport yet"* — so the very next
     `getPassport() || newPassport()` write **overwrote the unreadable data with an empty
     passport**. Now `getPassport()` distinguishes three states — absent (`null`/`""`), readable,
     and present-but-unparseable — recording them on a module-level `ppState {read, write, corrupt}`.
  2. **No write ever surfaced its failure.** `passportToggle` and `ppSave` each swallowed the
     `setItem` exception. All storage writes now funnel through one function, `ppWrite(p)`, which
     returns a boolean and **refuses to write at all when `ppState.corrupt` or `read === "denied"`** —
     the app never writes over bytes it could not read. `passportToggle` returns `null` on a failed
     write, and the `[data-pp]` handler now leaves the button label and `aria-pressed` untouched
     and raises a notice instead of claiming "Admired ✓".
  3. **No recovery path.** Added `ppNotice(msg)` — a dismissible `role="status"` panel in the
     existing `--panel`/`--line2`/radius idiom, carrying **Back up data (.json)**, a link to the
     Taste Passport, and Dismiss. `export` now falls back to the **raw stored bytes**
     (`pigment-passport-unreadable.json`) when the JSON will not parse, so nothing is lost.
     `#/taste` renders a new `ppTroubleView()` instead of the "No map yet" empty state, naming
     which case it is (blocked storage vs. unreadable data), stating plainly that nothing has been
     deleted, and offering *Try reading it again*, *Download the stored data* and an explicitly
     confirmed *Replace it with a new Passport*. `reset` and `storage-reset` now detect a failed
     `removeItem` and say so rather than claiming an erase.
- **Copy:** every string here is literal instruction/state/persistence copy per the spec's
  language rule — "Not saved.", "Nothing already saved has changed.", "Persona not adopted." —
  no lyrical voice on any failure path.
- **Schema:** **no change.** `ppState` is in-memory only; no new stored key, no renamed or dropped
  field. `pigment.taste.v1` is byte-compatible in both directions.
- **Deviation (recorded, minor):** the r2 plan scoped this to "`getPassport()` + `ppSave()` + one
  render branch". It necessarily grew to the `passportToggle` write and the `[data-pp]` handler,
  because that is the path a user actually hits first, and leaving it would have kept the exact
  false-success claim AC8 forbids. No product intent changed.
- **Validator:** green. **AC:** AC8 (no false success, context preserved, retry/recovery/export
  offered), AC9 (failure case exposes a meaningful next action), AC6 (button state stays accurate
  when the write did not land).

### U14 — ARIA state pass across C1–C18 (`e1595e5`)
- **Files:** `js/app.js` (15 render sites + 5 handler sites), `index.html` (:47-48 search, :50 theme).
- **Baseline:** `aria-current` 0, `aria-selected` 0, `aria-expanded` 0, `aria-pressed` 0 app-wide
  (Mondrian, `unrouted/ux-requirements.md` §2). **After:** `aria-current` 2, `aria-selected` 2,
  `aria-expanded` 4, `aria-pressed` 22 across `index.html` + `js/app.js`.
- **Per control, with the pattern chosen and why:**

| # | Control | Treatment | Reasoning |
|---|---|---|---|
| C1 | Header nav current section | `aria-current="page"` in `setNav()`, removed from the others | The one correct attribute for "current destination in a set of links". |
| C2 | Theme toggle | `aria-label` changed to the stable **"Light mode"**, plus `aria-pressed` = light-is-active | A toggle button needs a *stable* name and a state. The old name ("Switch between dark and light mode") describes an action, so `aria-pressed` on it would have been meaningless. The ☀/☾ glyph already reads as "turn light on", which matches. |
| C3 | Search input + results | Input: `role="combobox" aria-autocomplete="list" aria-haspopup="listbox" aria-controls="search-results"`, `aria-expanded` toggled in `runSearch`/`hideSearch`, `aria-activedescendant` set on arrow-key move. Results: `role="listbox"` + `aria-label`; options `role="option" aria-selected tabindex="-1"` with ids `sr-opt-N`; type headings wrapped in `role="group" aria-label="<type>"` with the heading itself `role="presentation"`. | The full APG combobox pattern. Group wrappers keep the type headings *in* the tree as group names instead of leaving invalid non-option children inside a listbox. `tabindex="-1"` on options is correct for the pattern (arrow keys own the list); Enter/Escape/click behaviour is unchanged. CSS uses only descendant selectors, so the new wrapper is visually inert — checked. |
| C4 | Artist era + sort filters | `aria-pressed` on the existing `<button>`s | Considered `role="radiogroup"`/`radio`: rejected. Radio semantics *promise* arrow-key roving focus, which these do not implement — that would be a wrong role, worse than none. Toggle buttons in a toolbar are honest and purely additive. |
| C5 | Taxonomy Cards/Family-tree toggle | `aria-pressed` | Same reasoning as C4. |
| C6 | Timeline zoom (Compact/Standard/Detail) | `aria-pressed` | Same. |
| C7 | Timeline "jump to era" | **nothing** | A transient scroll action with no persistent state. Adding a state would be a lie. |
| C8 | Timeline movement isolate | `aria-pressed` rendered `false`, maintained in the click handler alongside `.on` | The isolation has no module-level state and is reset by any re-render, exactly like its `.on` class; the ARIA now tracks the class one-for-one. |
| C9 | Timeline legend expand/collapse | `aria-expanded="${tlLegendAll}"` | `aria-controls` deliberately omitted: the button sits *inside* the region it expands, so pointing at an ancestor would be misleading. `aria-expanded` alone is valid on a button. |
| C10 | Influence edge-type filter | `aria-pressed`, maintained in the click handler | Handler mutates classes without a re-render, so ARIA is updated in the same loop. |
| C11 | Influence node | role + accessible name from U12; **no `aria-pressed`** | Reasoned rejection: the second activation *navigates* rather than un-pressing, so `aria-pressed="true"` would promise a toggle that does not exist. The dynamic accessible name added in U12 conveys the state truthfully instead. |
| C12 | World-map zoom World/Europe | `aria-pressed`, maintained in `setMapZoom` | Same as C10. |
| C13 | Onboarding tone picker (4-of-N) | `aria-pressed` | Textbook multi-select toggle group. |
| C14 | Onboarding deck Admire/Pass | **nothing** | Each press advances the deck; no state persists on the control. |
| C15 | Onboarding question options | **nothing** | Same — selecting advances immediately. |
| C16 | Persona Adopt button | **nothing** | The button is not rendered once adopted (`personaCard` drops it and the card reads "· yours"), so there is no pressed state to expose. |
| C17 | Passport Admire / Seen / Saved | `aria-pressed` **added**, label swap kept, both maintained in the handler | The brief asked for explicit reasoning. The label swap ("Admire" → "Admired ✓") changes the accessible **name**, which is not the same thing as programmatic **state**: switch-control users, state indicators and automated checks read `aria-pressed`, not name history. The two never contradict (pressed=true always pairs with "Admired ✓"), so the cost is mild redundancy in one announcement and the gain is a machine-detectable state that AC6 and AC16 both ask for. Removing the label swap instead would have been a visible-copy change outside my authority. |
| C18 | List-entry inline Admire | `aria-pressed` | Same control, same handler as C17. |

- **Validator:** green. **AC:** AC16 (programmatic half — the visible half landed in Wave A U1/U4),
  AC6 (Admire/Seen/Saved expose accurate programmatic state), AC15 (`aria-current` gives each route
  a current-destination signal), AC21 partial (selection is now perceivable in the results list;
  ranking/starvation remains unit 17).

### U15 — import conflict-confirmation UI (`3614e66`) — **the critical blocker**
- **Files:** `js/app.js` (`PP_CHOICE_FIELDS`, `PP_FIELD_LABELS`, `ppFieldKey`, `ppFieldSummary`,
  `passportConflicts`, `mergePassports`, `ppImport`, `viewPassportImport`; `[data-tsx]` branches
  `import-review`, `ppc`, `import-cancel`, `import`), `css/styles.css` (`.pp-conflicts`, `.pp-choice`).
- **The defect:** arrays were unioned correctly, but `quiz`, `palette`, `persona` and `milestones`
  were **last-writer-wins on `updatedAt`** — so opening a friend's share link with a newer
  timestamp *silently replaced the recipient's adopted Persona*, violating PIGMENT.md §9
  ("Adopted Personas must never silently switch"), while the import screen claimed
  "nothing is dropped."
- **The fix:**
  - `mergePassports(mine, theirs, choices)` is now **pure**: it deep-clones `mine` and never
    mutates it, so an abandoned merge cannot leak into local state even in memory.
  - The `updatedAt` comparison is **gone**. For each of the four fields: nothing offered → skip;
    nothing of ours to lose → adopt; same decision → skip; **differing → replaced only when
    `choices[f] === "theirs"`**, i.e. only on an explicit user choice. There is no code path that
    replaces one of these fields without one.
  - `ppFieldKey(field, v)` extracts the *decision* each field carries (`persona.adopted`, the tone
    list, `quiz.answers`, `milestones.onboarded`+`confidence`). This matters: `newPassport()`
    fabricates empty shells (`persona:{adopted:null,…}`, `milestones:{onboarded:false,…}`) that a
    naive truthiness test reads as real values — that bug was caught by the harness below
    (a brand-new user importing a friend's passport would have received *no* persona) and fixed.
  - **UI**, in the existing import/passport idiom (`.ob-wrap`, `.page-kicker`, `h1.display`,
    `.page-lede`, `.panel`, `.f-btn`, `.aw-btn primary .ob-cta`) — no new route, no new visual
    language. Screen 1 states what will happen; if any field conflicts the primary button becomes
    **"Choose what to keep →"**. Screen 2 renders one `.panel` per conflicting field with two
    `.f-btn` options carrying human summaries — *"Keep mine — The Wanderer · adopted 2026-01-01"*
    vs *"Take theirs — The Ascetic · adopted 2026-02-01"* — each with `aria-pressed` (consistent
    with U14's C4/C5 reasoning). **"Keep mine" is pre-selected**, so the no-action outcome is
    always the non-destructive one. Footer: **"Merge with these choices"** and
    **"Cancel — change nothing"**.
  - **Corrected copy.** "nothing is dropped" is replaced by a truthful split:
    *"Admirations, works seen in person, saved works, probes and skipped works are **combined** —
    all N entries in this passport are added to yours and none of yours is removed. Four settings
    cannot be combined because each holds a single value, and **K of them differ** from yours: …
    You choose which to keep on the next screen. Nothing is written until then."*
    When there is no conflict it says so explicitly instead of implying a merge of everything.
    The malformed-payload branch now also states "Nothing on this device has been changed."
- **Schema:** **no change** — no field renamed, dropped or added; `ppImport` is in-memory
  (it replaces the old `window._ppImport` global).
- **Cancel-path no-op — how it was verified (two independent methods):**
  1. **Write-path audit of the whole app.** There is exactly **one**
     `localStorage.setItem(PASSPORT_KEY, …)` in `js/app.js` (:93), and it is inside `ppWrite()`.
     `ppWrite` has exactly two callers — `passportToggle` (:116) and `ppSave` (:2438) — and
     `ppSave` has exactly three callers: `obFinish`, the `adopt` action, and the `import` action.
     The three cancel-adjacent branches (`import-review`, `ppc`, `import-cancel`) contain **no**
     `ppSave`/`ppWrite`/`setItem`/`removeItem`, and neither does `viewPassportImport`, which only
     reads (`decodePayload`, `getPassport`). So the reviewed cancel path cannot write by
     construction, not merely by intention.
  2. **Executable harness against the real source.** The actual `newPassport`, `ppFieldKey`,
     `passportConflicts` and `mergePassports` text was extracted from `js/app.js` and run under
     `osascript -l JavaScript` (no Node on this Mac) over 18 assertions —
     **18/18 pass**. The load-bearing ones: with `theirs.updatedAt` **newer** and *no* choices
     supplied, `persona.adopted`, `quiz`, `palette` and `milestones` all stay local (the old code
     replaced all four); arrays still union (`admirations` 1+1→2, `seen` preserved,
     `skipped`/`deckSeen` unioned); `choices.persona="theirs"` replaces **only** persona and leaves
     quiz and palette local; the local object is **byte-identical** (`JSON.stringify` compared)
     after three merges; mutating the merge *result* cannot reach the local object; an empty or
     malformed incoming payload leaves the local passport fully intact; identical values are not
     reported as conflicts.
- **Validator:** green.
- **AC:** **AC5** (per-field identification of local vs. incoming, explicit confirmation before
  replacement, cancel/malformed preserves the complete local Passport), **AC6** (independent
  fields survive the import matrix), AC4 (the journey's import/conflict transition is no longer
  broken or untruthful), AC14 (release/UI language matches what the code does).

---

## Deviation ledger (Gate 3)

| # | Unit | Deviation | Rationale |
|---|---|---|---|
| B-1 | U11 | Label passed per call site rather than derived inside `canvasTag` | Call sites pass ids, not names, drawn from six registries (and sometimes suffixed, `w.id + "-le"`); in-helper resolution would guess wrong on collision. Format stays centralised in `coverLabel`. |
| B-2 | U11 | Homepage hero uses a bespoke label instead of `coverLabel` | It is the nightly "mixed after <artist>" cover, not a cover *of* a subject; the generic phrasing would have been inaccurate. Equally explicit about being generative. |
| B-3 | U12 | `#ig-svg` given `role="group"`, **not** the `role="img"` named in the r2 plan | `role="img"` prunes descendants from the accessibility tree, which would have deleted the focusable nodes this unit exists to create. `role="group"` + `aria-label` satisfies AC20's naming requirement and keeps the graph operable. |
| B-4 | U12 | Page lede copy changed from "Click a painter…" to click-or-keyboard wording | The old copy documented a mouse-only interaction that is no longer the whole truth; leaving it would have made the keyboard path undiscoverable. |
| B-5 | U13 | Scope grew beyond `getPassport`/`ppSave` to `passportToggle` and the `[data-pp]` handler | That is the first write a real user triggers; leaving it would have preserved the exact false-success claim AC8 forbids. |
| B-6 | U14 | Theme toggle's `aria-label` changed from "Switch between dark and light mode" to "Light mode" | A toggle button requires a stable name plus a state; an action-phrased name makes `aria-pressed` unreadable. Non-visible copy only. |
| B-7 | U14 | Filter/toggle families use `aria-pressed`, not `role="radio"` | Radio semantics promise roving arrow-key focus that these controls do not implement — a wrong role is worse than none (brief's own rule). |
| B-8 | U14 | `aria-pressed` **added** to C17/C18 despite the existing label swap | Reasoning recorded in the U14 table: a changing accessible *name* is not programmatic *state*; the two never contradict; removing the visible label swap instead would be a copy change outside my authority. |
| B-9 | U14 | C7, C14, C15, C16 deliberately left without ARIA state | None of them holds persistent state (or the control disappears once the state exists). Inventing a state would be inaccurate. |
| B-10 | U15 | `ppFieldKey` compares the *decision* a field carries rather than raw JSON | Raw truthiness/JSON treats `newPassport()`'s empty shells as real values; the harness proved this would deny a brand-new user the incoming persona, and would raise phantom conflicts on cosmetic sub-field differences. |
| B-11 | U15 | `window._ppImport` replaced by module-scoped `ppImport` | The import flow now carries step + per-field choices; a leaked global is not the right home for it. Not a stored field, not a route, not an id. |
| B-12 | wave | Wave B's five commits were **rebuilt** onto `369440e` | U11's first commit was made with `git add -A` and swept in the previously **untracked, unrelated** `THEORY_001.md` (831 lines). The five commits were replayed scoped to `js/app.js`, `css/styles.css`, `index.html` only, and `THEORY_001.md` was restored to the working tree as untracked, exactly as found. Safe: `origin/pig-001-stabilization` was — and still is — at `369440e`, so **no pushed history was rewritten**. Final tree verified identical to the pre-rebuild tree except for that one file. |

---

## Self-assessment against the named criteria

- **AC5 — PASS (code-complete, evidence attached).** Every non-unioned field (`quiz`, `palette`,
  `persona`, `milestones`) now identifies local and incoming values by name and human summary,
  requires an explicit per-field choice before replacement, and defaults to *keep mine*. Cancel,
  navigating away, and malformed input all leave the local Passport unchanged — proved by the
  single-write-path audit and by 18/18 harness assertions including a byte-identical
  local-object check.
- **AC6 — PASS for the programmatic half.** Admire / Seen in person / Saved for later remain
  independent (unchanged `passportToggle` semantics) and now expose `aria-pressed` alongside the
  existing label swap; a failed write no longer flips either. The full navigation/reload/export/
  import/reset **matrix transcript is Van Eyck's**, not claimed here.
- **AC8 — PASS.** Read failure and corrupt data are distinguished from "no passport yet"; no
  write is ever claimed that did not land; unreadable data is never overwritten; retry, recovery
  and raw export are all offered; the app stays usable throughout.
- **AC15 — PARTIAL (this wave's share only).** `aria-current="page"` now marks the current
  destination on every route. Route focus management, skip-link and `aria-live` de-noising are
  **unit 19 / Wave C** and are not claimed here.
- **AC16 — PASS for the programmatic half.** Every stateful control in the frozen C1–C18 inventory
  now carries a correct programmatic state, or is documented above as correctly stateless. The
  visible half landed in Wave A (U1, U4). Contrast of the new focus ring is **Vermeer's measurement**.
- **AC17 — PARTIAL.** The constellation is keyboard-operable end to end with a visible focus
  indicator in both themes (nested-control violation was cleared in Wave A U5). **The "repeated
  navigation can be bypassed" half is explicitly NOT met** on `#/influences` — U12 adds ~200 tab
  stops and no bypass affordance exists; flagged above for unit 19.
- **AC20 — PARTIAL.** All 19 canvas cover surfaces and the influence constellation now have
  accessible names, and the constellation is keyboard-accessible. Reduced-motion equivalence and
  the judgement on whether the existing readable path counts as a sufficient text alternative
  remain **Van Eyck's / Vermeer's**.

**Not claimed, deliberately:** AC18/AC19 measurements, AT transcripts, screenshots, search
ranking (unit 17), onboarding checkpoint persistence (unit 18), route focus/skip-link (unit 19).

---

## Wave B summary

- **Units complete:** 5/5 (U11–U15), one commit each, in the briefed order.
- **Commits:** `5eecb98` (U11) · `980e52a` (U12) · `e657cae` (U13) · `e1595e5` (U14) · `3614e66` (U15).
- **Files touched:** `js/app.js`, `css/styles.css`, `index.html` only (+409/−80 lines net across
  the wave). No route, `case`, id, slug, frozen term or `pigment.taste.v1` field was added,
  renamed or dropped. No new dependency, no build step.
- **Validator:** green after every unit and after the commit rebuild; snapshot unchanged.
- **Working tree:** clean apart from the pre-existing untracked `THEORY_001.md`.
- **Gate 2 NOT certified here** (Van Eyck's). **Not pushed** (Synthesis Lead's).
