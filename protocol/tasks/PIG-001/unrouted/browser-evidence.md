```
BROWSER EVIDENCE — PIG-001
```

**Reviewer:** Vermeer (`claude-browser-reviewer`) — Browser Evidence Reviewer
**Scope:** Deliberately narrow per Synthesis Lead instruction — two measurements
only, against the currently deployed, unmodified build. Nothing was built or
changed; no broad accessibility audit; no full evidence pack.

---

## ENVIRONMENT

- **Commit:** `3c2e9fa45645d787da3754417448bbcebfd4029a` on `main`.
  Verified via `git log -1` and `git diff HEAD -- css/ js/ index.html`
  (empty — tracked production files are unmodified; only the known
  untracked `IVO_001.md` / `MIRA_001.md` / `SOREN_001.md` / `THEORY_001.md`
  and the `protocol/tasks/PIG-001/` directory are present, matching
  `intake-baseline.md` §2).
- **Serve command:** `python3 -m http.server 8421 -d .` from
  `/Users/ardagemci/Claude/painters-atlas`.
- **Build-identity check:** confirmed the served `#main-nav` contains exactly
  the 8 links in `index.html:36-45` (Artists, Lists, Museums, Explore,
  Movements, Techniques, Eras, Nations), read live from the DOM via
  `document.querySelectorAll('.main-nav a')`.
- **Browser:** the Claude Browser pane (Chromium-based; MCP tools
  `preview_start` / `resize_window` / `navigate` / `javascript_tool` /
  `computer`). The Claude-in-Chrome extension was checked first via
  ToolSearch and found **not connected** (`tabs_context_mcp` returned
  "Claude in Chrome is not connected") — noted as a tooling constraint, not
  a blocker, since the Claude Browser pane was available and used instead.
  Three evidence screenshots were additionally captured with headless
  Google Chrome (`/Applications/Google Chrome.app`) purely to get files
  saved to disk, since the Browser-pane `computer` tool has no
  screenshot-to-disk parameter.
- All numeric measurements below are **live-measured**, not estimated:
  `document.documentElement`/`body` `scrollWidth`/`clientWidth`,
  `window.scrollTo(99999,0)` + read-back `scrollX` (does the user actually
  gain horizontal scroll), `Element.getBoundingClientRect()` walks with
  ancestor-clipping detection, and real `Tab`-keypress-driven focus
  traversal (via `computer{action:"key", text:"Tab"}`, not synthetic
  `.focus()`, for the primary 320px pass).

## VIEWPORTS & THEMES COVERED

| Viewport | Routes | Theme |
|---|---|---|
| 320×800/900 | all 8 (`#/ #/artists #/palette #/taste #/explore #/timeline #/museums #/lists`) | dark (default; not toggled) |
| 390×844/900 | all 8 | dark (default; not toggled) |
| 1280×900 | all 8 | dark (default; not toggled) |

Light theme was not tested (out of the scoped two measurements; see NOT TESTED).

## EVIDENCE INDEX

| File | What it shows |
|---|---|
| `protocol/tasks/PIG-001/evidence/home__320__dark.png` | Home route, 320px, dark. Header row wrapped to a second line; search box, theme toggle, and a truncated "ARTISTS" sharing the row; rest of nav strip clipped out of view. |
| `protocol/tasks/PIG-001/evidence/home__390__dark.png` | Home route, 390px, dark. Same layout pattern, slightly more room. |
| `protocol/tasks/PIG-001/evidence/home__1280__dark.png` | Home route, 1280px, dark. Desktop header — visual reference for the search-box/theme-toggle overflow measured via JS (browser doesn't render a scrollbar because it's clipped by `body{overflow-x:hidden}` propagating to the viewport, so the image looks "normal"; the overflow is a geometric fact captured in the FINDINGS table, not something visibly obvious in a static screenshot). |
| Inline screenshot during live keyboard-Tab test (320px, "Nations" focused) | Captured inline via the Browser pane during the session (not saved as a separate file — the in-session `computer{action:"screenshot"}` tool used for the interactive Tab-traversal pass has no disk-save option). Shows the visible nav label reading "ERAS" while the actually-focused link (confirmed via `document.activeElement`) is "Nations" — the focus ring for "Nations" is reduced to a 1–2px sliver at the viewport's right edge. This is the direct visual evidence for the keyboard-legibility finding below. |

Reproducible commands (exact scripts run, so any of this can be re-verified):
JS snippets executed via `javascript_tool` are preserved verbatim in this
session's tool-call history; the two core ones were (a) a per-route loop
measuring `documentElement`/`body` scrollWidth/clientWidth plus a
`scrollTo(99999,0)`/read-back probe plus an ancestor-clipping-aware element
walk, and (b) a per-nav-link loop using `.focus()` (390px pass) / real `Tab`
keypresses (320px pass) reading `nav.scrollLeft` and each link's
`getBoundingClientRect()` against the nav's own visible bounds.

## FINDINGS

### Measurement 1 — root horizontal overflow (tests U2)

`css/styles.css:73` sets `overflow-x:hidden` **on `body`**, not on
`html`/root — verified directly (`html{scroll-behavior:smooth}` only, at
`css/styles.css:64`; no `overflow` rule on `html` anywhere in the file). This
matters because it changes which of two distinct, both-true findings is the
accurate characterization of "root overflow."

**Raw measurements** (`documentElement.scrollWidth` vs `.clientWidth`;
`body` matched `documentElement` in every case except home/1280 where
`body.scrollWidth` was 1px larger — immaterial):

| Width | Route | scrollWidth | clientWidth | Root geometrically overflows? | User can actually scroll root horizontally? |
|---|---|---|---|---|---|
| 320 | `#/` | 346 | 320 | **YES (+26px)** | NO |
| 320 | `#/artists` | 320 | 320 | no | NO |
| 320 | `#/palette` | 320 | 320 | no | NO |
| 320 | `#/taste` | 320 | 320 | no | NO |
| 320 | `#/explore` | 320 | 320 | no | NO |
| 320 | `#/timeline` | 320 | 320 | no | NO |
| 320 | `#/museums` | 320 | 320 | no | NO |
| 320 | `#/lists` | 320 | 320 | no | NO |
| 390 | `#/` | 402 | 390 | **YES (+12px)** | NO |
| 390 | `#/artists`…`#/lists` (7 routes) | 390 | 390 | no | NO |
| 1280 | `#/` | 1407 | 1270 | **YES (+137px)** | NO |
| 1280 | `#/artists` | 1407 | 1270 | **YES (+137px)** | NO |
| 1280 | `#/palette` | 1407 | 1280 | **YES (+127px)** | NO |
| 1280 | `#/taste` | 1407 | 1280 | **YES (+127px)** | NO |
| 1280 | `#/explore` | 1407 | 1280 | **YES (+127px)** | NO |
| 1280 | `#/timeline` | 1407 | 1270 | **YES (+137px)** | NO |
| 1280 | `#/museums` | 1407 | 1270 | **YES (+137px)** | NO |
| 1280 | `#/lists` | 1407 | 1270 | **YES (+137px)** | NO |

(`clientWidth` at 1280 alternates 1270/1280 across routes because some routes
have enough vertical content to trigger a real ~10px vertical scrollbar and
some don't — a normal, unrelated effect, included for transparency.)

**Root cause, identified by walking each offending element's ancestor chain
for an existing `overflow-x:auto|hidden|scroll` container** (elements inside
such a container are locally clipped and do not contribute to
`documentElement.scrollWidth`; the ones below have no such ancestor and are
exactly what explains the numbers in the table):

1. **Home route, 320/390px:** `div.strip` bleeds ~12px past the left edge
   (`css/styles.css:626`, `margin:0 -28px 12px` — a negative margin larger
   than the 16px `#app` padding active at this breakpoint,
   `css/styles.css` mobile block). At 320px only, `article.card.tax-card`
   grid cards (330px wide, `left:16px`) additionally push the right edge to
   346px against a 320px viewport — the taxonomy-card grid isn't narrow
   enough for this breakpoint.
2. **Every route, 1280px:** `.search-wrap` (`css/styles.css:134`,
   `width:min(280px,30vw)` → 280px at 1280) and `#theme-toggle` are pushed
   past the header's right edge. `.site-header`
   (`css/styles.css:94-102`) is a single flex row with no `flex-wrap` at
   this width (wrapping is only added at the `max-width:820px` breakpoint,
   `css/styles.css:836`), and brand + 8 nav links + search box + toggle do
   not fit inside 1280px. Because the header is shared chrome, this
   reproduces identically on every route.
3. On the 7 non-home routes at 320/390px, every `getBoundingClientRect()`
   overflow hit (7 to 531 elements per route) traced back to an existing
   `overflow-x:auto` ancestor — `.strip{overflow-x:auto}`
   (`css/styles.css:642`), `.main-nav{overflow-x:auto}`
   (`css/styles.css:837`), or the `#/timeline` horizontal timeline strip.
   These are intentional horizontally-scrolling widgets (carousels/timeline)
   clipped within their own box; they do **not** register as root overflow
   and were correctly excluded from the table above.

**The interpretive split the Synthesis Lead flagged is real and both halves
are independently confirmed:**
- Geometric overflow of the root/ICB (`documentElement.scrollWidth >
  clientWidth`) is **real and measured** on 10 of the 24 width×route
  combinations tested (home @ 320 & 390; all 8 routes @ 1280), with two
  distinct, non-overlapping causes identified above.
- The user can **never** actually scroll the root/viewport horizontally on
  any of the 24 combinations — confirmed directly by
  `window.scrollTo(99999,0)` followed by reading `scrollX`, which returned
  `0` every single time. No horizontal scrollbar appears, nothing is
  reachable by scroll gesture. This is because `body`'s `overflow-x:hidden`
  (line 73), despite being on the "wrong" element in strict-root terms, is
  propagated by the browser to the viewport (the standard UA rule: when
  `html`'s overflow is the default `visible`, `body`'s overflow-x/y is
  applied to the viewport instead). `scrollWidth` still reports the true
  underlying box size regardless of this propagation — `overflow:hidden`
  suppresses scrolling/scrollbars, not the reported extent — which is why
  both numbers can be true at once without contradiction.

**Verdict — U2: PARTIALLY CONFIRMED.** THEORY_001 §3.3's literal claim
("root-level horizontal overflow was directly measured on sampled desktop
and mobile routes") is TRUE under a geometric reading and FALSE under a
"the page visibly scrolls" reading — and THEORY_001 did not specify which it
meant, so neither "confirmed" nor "refuted" alone would be honest. The
"sampled desktop and mobile routes" phrasing is also asymmetric in what was
actually found: **all 8 routes** show it on desktop (1280px), but only
**1 of 8 routes** (home) shows it on either mobile width tested — the other
7 mobile routes have no root-level overflow at all under this measurement.
Two independent, previously-undocumented root causes were identified
(negative-margin bleed + oversized grid card on mobile home; non-wrapping
desktop header row on every route), which is itself new evidence beyond what
THEORY_001 asserted.

---

### Measurement 2 — mobile nav discoverability (tests U1)

8 header destinations confirmed live from the DOM (`index.html:36-45`):
Artists, Lists, Museums, Explore, Movements, Techniques, Eras, Nations —
matches the task's assumed list exactly.

**At 320px, home route:**
- `#main-nav` computed `overflow-x: auto`; `clientWidth: 64px`;
  `scrollWidth: 689px`. Confirms `css/styles.css:837`
  (`.main-nav{order:3;width:100%;overflow-x:auto;padding-bottom:2px}`) is in
  effect, but the nav does **not** actually get the full-width row its
  `width:100%` implies: the base rule `.main-nav{display:flex;gap:4px;
  flex:1}` (`css/styles.css:118`) is not overridden at this breakpoint, so
  in the wrapped flex header the nav still shares its row with
  `.search-wrap` (166px) and `#theme-toggle` (38px), leaving only 64px of
  actual visible strip out of a 320px viewport.
- **0 of 8** destinations are fully visible at rest (scrollLeft=0); only
  "Artists" is even partially visible (64 of its 78px width). All other 7
  are entirely clipped out of view.
- **8 of 8** require horizontal scrolling of the nav strip to be reached in
  full.
- Affordance: no purpose-built cue (no fade mask, no chevron/arrow, no "more"
  text). A sitewide generic `::-webkit-scrollbar` rule
  (`css/styles.css:82-85`; 10px, colored thumb) does apply to this
  `overflow-x:auto` box, and a thin sliver is visibly rendered under the nav
  in this Chromium-based browser — but it reads as decorative: it's small,
  it's positioned right where `.main-nav a::after`
  (`css/styles.css:124-132`) already draws a similar thin gold underline on
  hover/active links, and it carries no text/icon signal that more
  destinations exist off-screen. No Firefox-specific fallback
  (`scrollbar-width`) was found in the stylesheet, so cross-engine rendering
  of even this incidental affordance is unverified (see NOT TESTED).
- Keyboard: tested with **real `Tab` keypresses** (`computer{action:"key",
  text:"Tab"}`), not synthetic focus calls, walking all 8 links in DOM order.
  Confirmed reaching all 8 in sequence, ending at `href="#/nations"` as
  expected — **the nav does not trap keyboard focus**, and `nav.scrollLeft`
  does advance to track each newly focused link (0 → 79.5 → 157.5 → 247.5 →
  … → 545), confirming the browser's native focus-scroll-into-view behavior
  is active. However, because several labels ("Museums" ~90px, "Explore"
  ~82px, "Techniques" ~109px, "Nations" ~81px) are each wider than the 64px
  visible window, the native auto-scroll can only bring part of the label
  into view, not all of it: measured directly, after tabbing to Museums,
  Explore, Techniques, and Nations in turn, each remained only **partially**
  within the nav's visible bounds. A screenshot captured at the exact moment
  "Nations" held focus (confirmed via `document.activeElement`) shows the
  on-screen label reading **"ERAS"** — the previous item — while the only
  visible trace of "Nations" being focused is a 1–2px sliver of gold focus
  ring at the extreme right edge of the strip. A sighted keyboard user
  cannot reliably tell, from what's on screen, which destination is about to
  activate on Enter.

**At 390px, home route** (same method, `.focus()`-driven since the 320px
pass already established the mechanism is native, not JS-script-dependent):
- `clientWidth: 97px`, `scrollWidth: 689px` (unchanged content; more visible
  window than at 320px).
- At rest: **1 of 8** ("Artists") fully visible; **7 of 8** require scroll.
- After focus-follow: **4 of 8** ("Museums", "Explore", "Eras" — plus
  "Artists" at start) land fully visible once scrolled to; **4 of 8**
  ("Lists", "Movements", "Techniques", "Nations") remain only partially
  visible even after the browser's auto-scroll, for the same reason as at
  320px (label wider than the visible strip).

**Verdict — U1: CONFIRMED**, with an added nuance beyond THEORY_001's
wording. "Conceals most destinations behind an unannounced horizontal
gesture" is true and, at 320px, arguably an understatement: 7 of 8 (not just
"most") are fully hidden at rest, 0 of 8 are visible without scrolling, and
the only affordance present is a generic, undersized, easily-decorative-
looking scrollbar sliver — there is no purpose-built discoverability cue at
either tested width. Separately, on the keyboard axis (which THEORY_001's
sentence does not itself distinguish): the nav is **not** a keyboard trap —
all 8 destinations are Tab-reachable and operable — but the mismatch between
the visibly-displayed label and the actually-focused target during
auto-scroll is a distinct, concretely-observed defect in its own right, and
is a materially different (and in some ways more actionable) severity
category than "hard to discover by sight." These two aspects should be
tracked separately rather than folded into one "concealed nav" statement, so
that whichever gets fixed first is scoped correctly.

---

## NOT TESTED

- **Light theme**, for either measurement — out of scope for this
  deliberately narrow two-measurement pass; the theme toggle was never
  activated. Reason: explicit instruction to keep scope to exactly the two
  measurements requested.
- **390px keyboard-follow mechanism** was verified with `.focus()` calls
  rather than real `Tab` keypresses (the 320px pass used real keypresses and
  established the underlying mechanism is native browser behavior, not
  contingent on how focus was set — but this is one inferential step
  removed from a literal keypress-by-keypress replication at 390px).
- **Cross-browser/engine rendering** — only Chromium (Claude Browser pane +
  headless Google Chrome for saved screenshots) was tested. The
  Claude-in-Chrome extension was unavailable (checked via ToolSearch,
  confirmed not connected). No Firefox or Safari check was performed;
  relevant specifically because the nav's only scroll affordance
  (`::-webkit-scrollbar` styling) is Blink/WebKit-specific and its
  appearance (or absence) on other engines is unverified.
- **Real touch/swipe gesture behavior** on an actual mobile device — only
  keyboard (`Tab`) and programmatic/mouse-wheel-equivalent
  (`window.scrollTo`) interaction were tested for the nav strip and root
  scroll respectively.
- **Viewport widths or routes outside the requested set** — no other widths
  or routes were sampled; this is a targeted two-measurement pass, not a
  general responsive audit, per explicit scope instruction.
