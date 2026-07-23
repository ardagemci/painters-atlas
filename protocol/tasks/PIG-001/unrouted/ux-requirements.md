# UX REQUIREMENTS — PIG-001

**Author:** Mondrian (`claude-ux-architect`), UX & Interaction Architect
**Round:** 1 (challenge — analysis only, Gate 1 in force, NO production edits made)
**Date:** 2026-07-21
**Build:** commit `3c2e9fa4` (per intake-baseline.md §2)
**Purpose:** Turn THEORY_001 §7's unbounded acceptance criteria into enumerations
and definitions Van Eyck can pass/fail without judgment calls. This round designs
nothing and proposes no UI. Every enumeration below is grepped from the live code
(`js/app.js`, `index.html`, `css/styles.css`) with file:line citations, not from
PIGMENT.md (§12 confirmed stale — it claims 235 artists / 314 works / 215 edges /
"NN routes"; validator says 246 / 315 / 225).

SCOPE: whole-app inventory in service of criteria 14, 15, 16, 22, 24, 25, 27, 32,
35, plus static verification of Duchamp's U5–U8 and the merge question. Surfaces in
active spec scope: onboarding/palette, taste passport, search, artwork page, artist
page, invalid route.

---

## 0. Method note & standing caveat

All counts come from grepping the files at the cited lines, or from a faithful
re-execution harness that loads the real data files and reproduces the exact `INDEX`
builder and `runSearch()` from `js/app.js:2159-2194`. Two claims are marked
**[NEEDS BROWSER]** — they require Vermeer's runtime measurement and I do not assert
them from static code. Everything else is decidable from source.

---

## 1. ROUTE INVENTORY (grounds criteria 14, 35)

Source: the single `switch(page)` router at `js/app.js:1986-2017`. The hash is parsed
`const [page, id] = hash.split("/")` (`js/app.js:1987-1988`), so every route is
`#/<page>` or `#/<page>/<id>`. There is exactly one router and one `hashchange`
listener (`js/app.js:2152`).

**Total: 23 explicit route cases + 1 `default` (→ 404) = 24 router branches.**
By shape: **9 index/standalone routes**, **12 parameterized `/{id}` routes** (one of
which, `passport`, takes an opaque base64 payload not an entity id), and the
**home** + **default/404** branches.

| # | `case` value | Route pattern | View fn (line) | `<h1>`? | `document.title` set? | Bad-id fallback |
|---|---|---|---|---|---|---|
| 1 | `""` | `#/` | `viewHome` (1423) | yes (1440) | yes (1433) | n/a |
| 2 | `artists` | `#/artists` | `viewArtists` (1565) | via `hero`/head | yes (1566) | n/a |
| 3 | `timeline` | `#/timeline` | `viewTimeline` (862) | yes (913) | yes (863) | n/a |
| 4 | `influences` | `#/influences` | `viewInfluences` (1049) | yes (1090) | yes (1050) | n/a |
| 5 | `daily` | `#/daily` | `viewDaily` (1521) | yes (1533) | yes (1527) | → `view404()` if no pool (1523) |
| 6 | `lists` | `#/lists` | `viewLists` (1370) | yes (1375) | yes (1371) | n/a |
| 7 | `list` | `#/list/{id}` | `viewList` (1381) | yes (1394) | yes (1383) | → `view404()` (1382) |
| 8 | `palette` | `#/palette` | `viewPalette` (2553) | yes (multi-step) | yes (2554) | n/a |
| 9 | `taste` | `#/taste` | `viewTaste` (2832) | yes (2850) | yes (2833) | empty-state branch (2836) |
| 10 | `passport` | `#/passport/{payload}` | `viewPassportImport` (2927) | yes (2938) | yes (2928) | invalid-payload branch (2930) |
| 11 | `museums` | `#/museums` | `viewMuseums` (1270) | head | yes (1271) | n/a |
| 12 | `museum` | `#/museum/{id}` | `viewMuseum` (1283) | yes (1300) | yes (1285) | → `view404()` incl. sentinel ids (1284) |
| 13 | `explore` | `#/explore` | `viewExplore` (1330) | yes (1335) | yes (1331) | n/a |
| 14 | `artist` | `#/artist/{id}` | `viewArtist` (1620) | via `hero` (1634) | yes (1622) | → `view404()` (1621) |
| 15 | `artwork` | `#/artwork/{id}` | `viewArtwork` (1736) | yes (1761) | yes (1739) | → `view404()` (1737-1738) |
| 16 | `movements` | `#/movements` | `taxIndexView` (1807) | yes | yes (1808) | n/a |
| 17 | `movement` | `#/movement/{id}` | `taxDetailView` via `Mx[id]` (2008) | yes | yes (1834) | → `view404()` inline (2008) |
| 18 | `techniques` | `#/techniques` | `taxIndexView` (1807) | yes | yes (1808) | n/a |
| 19 | `technique` | `#/technique/{id}` | `taxDetailView` via `Tx[id]` (2011) | yes | yes (1834) | → `view404()` inline (2011) |
| 20 | `eras` | `#/eras` | `viewEras` (1869) | yes | yes (1870) | n/a |
| 21 | `era` | `#/era/{id}` | `viewEra` (1892) | yes (1894) | yes (1894) | → `view404()` (verify branch) |
| 22 | `nations` | `#/nations` | `viewNations` (1930) | yes | yes (1931) | n/a |
| 23 | `nation` | `#/nation/{id}` | `viewNation` (1952) | yes (1954) | yes (1954) | → `view404()` (verify branch) |
| — | `default` | anything else | `view404` (1975) | yes (1978) | yes (1976) | this IS the fallback |

Notes for criterion 35 (no secondary path becomes *less* discoverable): the header
`#main-nav` exposes only **8** of these routes (`artists, lists, museums, explore,
movements, techniques, eras, nations` — `index.html:37-44`). The footer exposes those
8 **plus `#/taste`** (`index.html:62`). Routes reachable ONLY by in-content links or
direct URL (never from the persistent chrome): `#/timeline`, `#/influences` (only via
`#/explore` or `#/artist`), `#/daily` (only via `#/` home or direct), `#/palette`
(only via home entry-card / `#/taste`), `#/list/{id}`, `#/museum/{id}`,
`#/artist/{id}`, `#/artwork/{id}`, `#/passport/{payload}`. This is the frozen
baseline any redesign is measured against for criterion 35.

`setNav()` (`js/app.js:2032-2038`) highlights a nav item for **17** of the 23 page
keys via its `map`; the 6 with no highlight are `""`(home), `daily`, `palette`,
`taste`, `passport`, and the 404 default.

---

## 2. CONTROL / STATE INVENTORY (bounds criteria 15, 16; verifies U7)

Grepped ARIA usage across `index.html` + `js/app.js` + `css/styles.css` (exact
`grep -o` counts):

| Attribute | index.html | js/app.js | css | TOTAL |
|---|---|---|---|---|
| `aria-current` | 0 | 0 | 0 | **0** |
| `aria-selected` | 0 | 0 | 0 | **0** |
| `aria-expanded` | 0 | 0 | 0 | **0** |
| `aria-pressed` | 0 | 0 | 0 | **0** |
| `role=` | 0 | 2 | 0 | **2** (both `role="img"`: js/app.js:1197, 2524) |
| `aria-label` | 2 | 6 | 0 | **8** |
| `aria-labelledby` | 0 | 1 | 0 | **1** (js/app.js:1234) |
| `aria-live` | 1 | 0 | 0 | **1** (`#app`, index.html:53, `polite`) |
| `aria-hidden` | 3 | 0 | 0 | **3** (bg-canvas + 2 brand-dots) |
| skip-link | 0 | 0 | 0 | **0** (no `skip`/`skip-link` pattern anywhere) |
| `.focus()` calls | 0 | 0 | — | **0** |
| `tabindex` | 0 | 0 | 0 | **0** |

**The complete set of stateful interactive controls** (each carries selected /
active / current / expanded / focused state) and how that state is currently
expressed. This is the **frozen inventory that bounds criteria 15 and 16** — Van Eyck
tests exactly these control types, no more:

| # | Control | Where | State class | ARIA state today | Keyboard-operable element? |
|---|---|---|---|---|---|
| C1 | Header nav item (current section) | `index.html:37-44`, toggled `js/app.js:2036-2037` | `.active` (css:131-132) | **none** (no `aria-current`) | yes — real `<a>` |
| C2 | Theme toggle (dark/light) | `index.html:50`; `js/app.js:2218-2227` | glyph swap ☀/☾ | `aria-label` present; **no `aria-pressed`** | yes — real `<button>` |
| C3 | Search input + results listbox | `index.html:47-48`; `js/app.js:2157-2213` | `.sel` on active option (css:157) | **none** (no `role=listbox/option`, no `aria-activedescendant/selected/expanded`) | yes — arrow keys (2199-2211) |
| C4 | Artist filter: era + sort (`.f-btn`) | `js/app.js:1577-1582`, handler 2140-2146 | `.on` (css:694) | **none** | yes — `<button>` |
| C5 | Taxonomy view toggle Cards/Tree (`.f-btn`) | `js/app.js:1820-1821` | `.on` | **none** | yes — `<button>` |
| C6 | Timeline zoom (Compact/Standard/Detail) | `js/app.js:918-919`, handler 2105-2114 | `.on` | **none** | yes — `<button>` |
| C7 | Timeline "jump to era" | `js/app.js:922`, handler 2115-2120 | (transient scroll) | **none** | yes — `<button>` |
| C8 | Timeline movement isolate (`.tl2-leg`) | `js/app.js:905,924`, handler 2131-2139 | `.on` + bars `.dim` (css:737,762) | **none** | yes — `<button>` |
| C9 | Timeline legend expand/collapse | `js/app.js:907-908`, handler 2121-2130 | text label swap | **none** (no `aria-expanded`) | yes — `<button>` |
| C10 | Influence edge-type filter (`.tl2-leg`) | `js/app.js:1084-1085,1093`, handler 2095-2101 | `.on` + edges `.hid` (css:771) | **none** | yes — `<button>` |
| C11 | Influence node focus/select (`.ig-node`) | `js/app.js:1077-1082`, handler 2089-2094; `igFocus` 1101 | `.sel`,`.lit`,`.focused` (css:779-783) | **none** | **NO** — `<g>`/`<circle>`, no `tabindex`, click-only |
| C12 | World-map zoom World/Europe (`.map-zoom`) | `js/app.js:1193-1194`, handler 2103-2104; `setMapZoom` 1167 | `.on` | **none** | yes — `<button>` |
| C13 | Onboarding tone picker (4-of-N) | `js/app.js:2571-2574`, handler 2953-2958 | `.on` (css:923) | **none** (no `aria-pressed`) | yes — `<button>` |
| C14 | Onboarding deck Admire/Pass | `js/app.js:2593-2594`, handler 2960-2966 | (advances state) | **none** | yes — `<button>` |
| C15 | Onboarding question options | `js/app.js:2608-2609`, handler 2967-2972 | (advances state) | **none** | yes — `<button>` |
| C16 | Persona Adopt button | `js/app.js:2542`, handler 2973-2980 | `.adopted` on card (css) | **none** | yes — `<button>` |
| C17 | Passport action Admire/Seen/Saved | `js/app.js:89-94`; handler 2080-2086 | `.on` + label+glyph swap "Admire"→"Admired ✓" (js/app.js:84-88,2084) | **none** (no `aria-pressed`) | yes — `<button>` |
| C18 | List-entry inline Admire (`.le-adm`) | `js/app.js:1416`, same handler | `.on` + label swap | **none** | yes — `<button>` |

**U7 verdict (state communicated only visually): CONFIRMED by static inspection for
selection/toggle STATE, with one nuance.** Every stateful control C1–C18 carries a
**non-color** cue in addition to color — either a text-label swap (C2 glyph, C9, C17,
C18 label text) OR a background fill change (`.on`/`.active`/`.sel` all repaint the
control body, not merely its text color — css:131,157,425-426,694,737,923). So the
"color alone" half of criterion 15 largely holds visually. **But the *programmatic*
half fails uniformly:** across all 18 control types the selected/current/expanded/
pressed state is exposed to assistive tech **zero** times — `aria-current`,
`aria-selected`, `aria-pressed`, `aria-expanded` are each 0. A screen-reader or
switch user cannot perceive which nav item is current, which filter is active, which
tone is chosen, or which artwork is Admired. **This is the substance of criteria 15
and 16 and the reason U7 is materially true even though it is imprecise about the
mechanism.** C11 additionally fails keyboard-operability outright (see §7/U-notes).

---

## 3. SEARCH QUERY FIXTURE (makes criteria 24, 25 testable; verifies U5)

Search algorithm, verbatim from `js/app.js:2172-2194`: query is `trim().toLowerCase()`;
each `INDEX` entry's `name.toLowerCase()` is tested; **`startsWith(q)` → `starts`
bucket, else `includes(q)` → `contains` bucket**; results are `[...starts,
...contains].slice(0, 9)`; **within each bucket order is INDEX insertion order**
(Artists → Artworks → Lists → Museums → Movements → Techniques → Eras → Nations,
`js/app.js:2159-2169`); empty ⇒ `.sr-empty` message (2184). No diacritic folding, no
token/word matching, no meta-field matching. **INDEX size = 834** (Artists 246,
Artworks 315, Lists 12, Museums 103, Movements 74, Techniques 39, Eras 8, Nations 37).

The fixture below was produced by re-executing that exact algorithm against the real
data. Every "expected #1" is the **actual** current top result — Van Eyck asserts the
real ranking equals this table (criteria 24/25). Queries F19–F22 are the incidental-
substring probes (Duchamp U5).

| # | Query | Expected #1 result | Expected type | Route | Covers |
|---|---|---|---|---|---|
| F1 | `vermeer` | Johannes Vermeer | Artist | `#/artist/johannes-vermeer` | Artist (substring) |
| F2 | `rembrandt` | Rembrandt van Rijn | Artist | `#/artist/rembrandt` | Artist (prefix) |
| F3 | `frida kahlo` | Frida Kahlo | Artist | `#/artist/frida-kahlo` | Artist, multiword |
| F4 | `basquiat` | Jean-Michel Basquiat | Artist | `#/artist/jean-michel-basquiat` | Artist (mid-name substring) |
| F5 | `starry night` | The Starry Night | Artwork | `#/artwork/the-starry-night` | Artwork (substring past leading "The") |
| F6 | `guernica` | Guernica | Artwork | `#/artwork/guernica` | Artwork (prefix) |
| F7 | `mona lisa` | Mona Lisa | Artwork | `#/artwork/mona-lisa` | Artwork |
| F8 | `las meninas` | Las Meninas | Artwork | `#/artwork/las-meninas` | Artwork (two share prefix; Velázquez first by INDEX order) |
| F9 | `louvre` | Musée du Louvre | Museum | `#/museum/louvre` | Museum (substring) |
| F10 | `rijksmuseum` | Rijksmuseum | Museum | `#/museum/rijksmuseum` | Museum (prefix) |
| F11 | `impressionism` | Impressionism | Movement | `#/movement/impressionism` | Movement (prefix ahead of Post-/Neo-) |
| F12 | `cubism` | Cubism | Movement | `#/movement/cubism` | Movement |
| F13 | `fresco` | Fresco | Technique | `#/technique/fresco` | Technique |
| F14 | `woodcut` | Woodcut (id `woodblock`) | Technique | `#/technique/woodblock` | Technique — name≠id, name-only match |
| F15 | `17th century` | 17th Century | Era | `#/era/17th-century` | Era (prefix) |
| F16 | `19th` | 19th Century | Era | `#/era/19th-century` | Era (numeric prefix) |
| F17 | `japan` | 🇯🇵 Japan | Nation | `#/nation/japan` | Nation |
| F18 | `türkiye` | 🇹🇷 Türkiye (id `turkey`) | Nation | `#/nation/turkey` | Nation — name≠id; diacritic literal |
| F19 | `tate` | Tate Modern | Museum | `#/museum/tate-modern` | **U5 probe** — 2 prefix hits (Tate Modern, Tate Britain) THEN incidental `sTATE Hermitage`, `puSHKIN sTATE`, `sTATE Russian`, and `United sTATES` bleed in below |
| F20 | `art` | Artemisia Gentileschi | Artist | `#/artist/artemisia-gentileschi` | **U5 probe** — 4 prefix (Artemisia, Art Nouveau, Art Deco, Art Informel) then 39 incidental `heArt/eArth/pArt…` |
| F21 | `son` | Sonia Delaunay | Artist | `#/artist/sonia-delaunay` | **U5 probe** — 1 prefix, then "…His **Son**", "Prodigal **Son**", "Madame Monet and Her **Son**" incidental |
| F22 | `min` | Minneapolis Institute of Art | Museum | `#/museum/minneapolis-institute-of-art` | **U5 probe** — 3 prefix (Minneapolis, Minimalism, Miniature) then "Er**min**e", "Hum**min**gbird" incidental |
| F23 | `zzzqx` | *(no match)* | — | `.sr-empty` shown | Nonsense → empty state (criterion 23/27) |
| F24 | `qwertyuiopasdf` | *(no match)* | — | `.sr-empty` shown | Nonsense #2 |

**Every expected result above was verified to exist in the live data.** The fixture
also exposes decidable **known limitations** Van Eyck must treat as *current baseline*
(so criterion 25 is "resolves where matching data exists", not "resolves for any
spelling"):

- **No diacritic folding** (js/app.js:2173-2177): `durer`→no match (needs `dürer`);
  `velazquez`→no match (needs `velázquez`); `cezanne`→no match. Ascii-typing users
  get `.sr-empty` for accented names. **Decidable fact, not a browser claim.**
- **Meta is not searched**: `moma` →no match (name is "The Museum of Modern Art",
  id is `moma`); `woodblock` as a *query* →no match (technique **name** is "Woodcut").
  Only `name` is indexed.
- **`rose`→no match**, **`1600`→no match**, **`seventeenth`→no match**: confirm no
  fuzzy/semantic layer.

**U5 verdict: CONFIRMED (decidable).** F19–F22 demonstrate incidental substrings
ranking into the visible 9 purely by INDEX insertion order once the `starts` bucket is
exhausted. Because `contains` results are not scored (no exact-token boost, no length
penalty), a 3-letter query like `art`/`son`/`min` surfaces long unrelated names.
Criterion 24 ("exact and meaningful matches outrank incidental substrings") is
**failing today** for these probes and is now objectively testable against this
fixture: pass = for F19–F22 every `startsWith` hit ranks above every non-prefix
`includes` hit (which the current two-bucket split already guarantees) AND an exact
full-name match, if present, ranks #1. The residual defect is *within* the `contains`
bucket (incidental substrings vs. no better match), which this fixture pins down.

---

## 4. "ESSENTIAL VISUALIZATION CONTENT" DEFINITION (bounds criterion 22)

**Rendering technology — checked in code, decisive for whether an "alternative" means
a whole new render path:**

- **Timeline `#/timeline`**: **DOM, not canvas.** Bars are real `<a class="tl2-bar"
  href="#/artist/{id}" title="name · years · movement"><span>name</span></a>`
  (`js/app.js:894-897`); grid/labels are `<div>`s. Already in the a11y tree and
  keyboard-focusable.
- **Influence constellation `#/influences`**: **inline SVG, not canvas.** Nodes are
  `<g class="ig-node"><circle><text><title></g>` (`js/app.js:1077-1082`); edges are
  `<line>` (1068-1070). `role="img"`/`aria-label` are **absent** on `#ig-svg`
  (1095). Nodes have **no `tabindex`** → not keyboard-focusable.
- **World map (nations)**: **inline SVG** with `role="img" aria-label` (1197); dots
  are `<a href="#/nation/{id}">` (1155) — focusable.
- **Taste map**: **inline SVG** with `role="img" aria-label` (2524).
- The only `<canvas>` uses are the **decorative** ambient background (`bg-canvas`,
  `aria-hidden`, index.html:29) and the generative cover art (`canvasTag`,
  js/app.js:719-720) — both explicitly "an interpretation painted in the browser"
  and never information-bearing. The passport-card canvas (2711) is an export image.

**Consequence for criterion 22: no essential instrument is canvas-rendered, so an
accessible alternative does NOT require building a new rendering pipeline — it
requires exposing data already present in the DOM/SVG.** Definition of essential vs.
decorative, per instrument, frozen for Van Eyck:

**Timeline (#/timeline)**
- ESSENTIAL (must have readable + keyboard-accessible equivalent): each painter's
  **name**, **lifespan/years**, **primary movement**, and a **link to their page**.
- ALREADY-SATISFIED alternative: the bar is an `<a>` with visible name text +
  `title` + href; the artist index `#/artists` offers the same set chronologically
  (`viewArtists`, sort "chrono", js/app.js:1581). *Pass condition:* every timeline
  bar is keyboard-reachable and its accessible name includes painter + years.
- DECORATIVE (no equivalent required): pixel x/lane position, greedy lane packing,
  movement color gradient, living-painter fade.

**Influence constellation (#/influences)**
- ESSENTIAL: each **relationship** as (source artist, target artist, relationship
  type, direction) and a **link to each artist**; the relationship-type legend counts.
- ALTERNATIVE STATUS: **partially present, with a gap.** Per-artist relationships ARE
  available as real keyboard-accessible anchor links in the artist page "Lineage &
  circle" panel (`js/app.js:1699-1704`, chips with the relationship verb) and the
  `igFocus` info panel (1116-1119). **But** (a) `#ig-svg` has no `role`/`aria-label`;
  (b) nodes are not focusable (no `tabindex`); (c) there is no single readable list of
  all 225 edges — the constellation is the only surface showing the whole web. *Pass
  condition for criterion 22:* the essential relationship data reachable in the graph
  must be reachable by keyboard and readable by AT via an equivalent (e.g. the
  per-artist lineage panels collectively, or a list view) — currently **fails** at the
  graph itself (click-only), **passes** at the artist-page equivalent.
- DECORATIVE: force-directed node positions, node radius (∝ degree), colors, the
  225-edge visual layout, hub prominence.

**Edge count = 225** (validator, intake-baseline §3), rendered by `viewInfluences`.

---

## 5. FROZEN JOURNEY DEFINITIONS (makes criterion 32 testable)

For each canonical journey (theory-brief §5.1-5.5) each step gets an **observable**
anchor / relationship / consequence / onward-path definition. All routes verified to
exist in §1. "Observable" = a specific DOM element or route Van Eyck can point at.

**J1 — Known-artist discovery (§5.1)** — routes `#/` or search → `#/artist/{id}` →
related → related entity → onward. All exist (§1 rows 1,14).
| Step | Anchor (observable) | Relationship (observable) | Consequence (observable) | Onward path (observable) |
|---|---|---|---|---|
| Land on artist | `viewArtist` `<h1>` = artist name via `hero` (1634) | `chipsFor(a)` movement/technique/era/nation chips (1640) | "Why … matters" why-card (1645-1649) OR bio | any chip `<a>` |
| Traverse a relationship | a chip or "Lineage & circle" link (1701-1702) | chip carries relationship verb (`IG_WORDS`, 1702) | destination page renders | its own chips |
| Reach related entity | movement/nation/era page `<h1>` | that page's member list | list of painters/works | card `<a>` |
*Pass:* from any `#/artist/{id}` a keyboard user reaches ≥1 related entity page and
back without losing the visible artist name anchor.

**J2 — Artwork-led discovery (§5.2)** — search/list/daily/artist/museum →
`#/artwork/{id}` → artist/movement/technique/era/nation/museum → related work →
optional personal action. Routes exist (§1 row 15).
| Step | Anchor | Relationship | Consequence | Onward path |
|---|---|---|---|---|
| Land on artwork | `viewArtwork` `<h1>` = title (1761); artist sub-link (1762) | movement/technique/nation chips (1766-1768); "Where it hangs" museum panel (1784-1794) | "The picture"/"What to notice" copy (1772-1775) | "More by", "Near it", "Go next" panels (1795-1802) |
| Personal action | `passportActions(w)` 3 buttons (1764) | Admire/Seen/Saved toggle | label swap + persists (§2 C17) | proceeds to `#/taste` implicitly |
*Pass:* artwork page exposes artist link + ≥1 classification chip + ≥1 onward panel +
the 3 passport buttons.

**J3 — Editorial discovery (§5.3)** — `#/` or `#/lists` → `#/list/{id}` →
`#/artwork/{id}` → related → another list/route. Routes exist (§1 rows 6,7).
| Step | Anchor | Relationship | Consequence | Onward path |
|---|---|---|---|---|
| Land on list | `viewList` `<h1>` = title (1394) | ordered `<ol class="list-entries">` (1400) | each entry `le-note` (1414) explains the pick | entry `<a>` to artwork |
| End of list | — | "More lists" section (1420) | 3 sibling list cards | `listCard` `<a>` |
*Pass:* list renders an ordered walk with per-entry notes and ≥1 onward list link.

**J4 — Personal Taste loop (§5.4)** — `#/` → `#/palette` → 4 tones → 16 cards → 5
questions → reveal → adopt/defer → matched discovery → `#/taste` → further Admire →
updated passport. Routes exist (§1 rows 8,9).
| Step | Anchor | Relationship | Consequence | Onward path |
|---|---|---|---|---|
| Start | `viewPalette` intro `<h1>` (2558) + "Begin" (2560) | — | enters step machine `ob` (2549-2552) | step 1 |
| Tones (step1) | "Pick four tones" (2569) | `.tone` buttons, 4-cap (2955-2956) | "N of 4 chosen"; CTA disabled until 4 (2576-2577) | "To the deck →" |
| Deck (step2) | deck card image+meta (2588-2591) | Admire/Pass (2593-2594) | progress bar `di/16` (2587) | auto-advance to step3 at 16 (2964) |
| Questions (step3) | question text (2607) | 5 option buttons (2608-2609) | progress `qi/5` (2606) | auto-advance to reveal at 5 (2970) |
| Reveal (step4) | signal-word `<h1>` (2620) | taste map SVG + 3 persona candidates (2622-2633) | Adopt / Decide later (2638-2639); `obHandoff` matched artists+list (2644-2660) | "To your taste page →" (2637) |
| Passport | `viewTaste` `<h1>` (2850) | map + persona + admirations (2853-2893) | share/export/reset chips (2861-2866) | Admire anywhere feeds back |
*Pass:* the six-step machine completes with visible progress at each step and a
persistent onward link, and reveal→`#/taste` preserves the saved persona (`obFinish`
2661-2687).

**J5 — Explore loop (§5.5)** — `#/` → `#/explore` → choose projection → focus entity
→ understand relationship → open canonical page → continue. Routes exist (§1 rows
13,3,4).
| Step | Anchor | Relationship | Consequence | Onward path |
|---|---|---|---|---|
| Explore hub | `viewExplore` `<h1>` (1335) | 2 entry-cards: timeline, influences (1338-1350) | lede promises "two instruments" (1336) | entry-card `<a>` |
| Timeline projection | timeline `<h1>` (913) | bars=lifespans, legend=movements | isolate/zoom controls (C6-C9) | any bar `<a>`→artist |
| Influence projection | influences `<h1>` (1090) | force graph, edge-type legend | node focus reveals lineage panel (1116-1119) | "Open …'s page →" (1119) |
*Pass:* `#/explore` names exactly the instruments it links to (see criterion 26 —
CONFIRMED asymmetry below) and each instrument offers a link into a canonical page.

**Criterion 26 note (Explore promise vs. destination):** the **home** entry-card
(`js/app.js:1460-1465`) promises "a timeline, an influence constellation, family trees
of movements, and a world map" — **four** instruments; the **`#/explore`** page
(`js/app.js:1332-1351`) offers only **two** (timeline, influences). Family trees live
under `#/movements`/`#/techniques` and the world map under `#/nations`. **Promise ≠
destination inventory — CONFIRMED in code**, matching the theory brief's own flag.

---

## 6. STATE MATRIX (active-scope surfaces)

`—` = state occurs and is handled; **N/A(reason)** = cannot occur in a static,
no-backend app (Duchamp's caveat on criterion 27). "loading" is generally N/A because
all data is loaded synchronously via `<script>` before `route()` runs (index.html:68-97,
`route()` builds HTML from in-memory registries) — there is no async fetch on these
surfaces except image loads and the clipboard/card export.

| Surface | Empty | Loading | Success | Failure | Recovery |
|---|---|---|---|---|---|
| **Onboarding `#/palette`** | intro screen when `ob` null (2555-2563) | **N/A** (synchronous state machine; deck built in-memory, `buildDeck` 2550) | steps 1-4 render with progress bars (2565-2642) | deck images are `<img>` — a broken src has **no onerror here** (2589) → blank tile **[gap, decidable]** | "Retake onboarding" resets `ob=null` (2982); tone-cap & disabled CTA prevent invalid submit (2577) |
| **Taste Passport `#/taste`** | "No map yet — let's sketch one" + CTA when no passport/admirations (2836-2842) | preview via `requestAnimationFrame(drawCardPreview)` shows "mixing pigment…" placeholder (2834, 2877) | full map+persona+admirations (2847-2893) | card export: `toBlob` failure leaves button re-enabled (2984-2997); share: clipboard reject → falls back to printing URL in `#taste-msg` (3007-3009) | Reset confirms then rebuilds (3011-3015); export `.json` backup (2864,2999-3004) |
| **Search** | `.sr-empty` "Nothing in the atlas matches …" (2184) | **N/A** (synchronous filter over in-memory INDEX) | grouped results, ≤9, keyboard nav (2185-2211) | no error path (pure filter cannot throw on string input) → **N/A(no async, no throw)** | Esc hides + blurs (2210); click-away hides (2213); clearing input hides (2174) |
| **Artwork `#/artwork/{id}`** | copy-absent branch: "Not written about yet…" when no `w.description` (1775); held-copyright interpretation note (1756-1758) | **N/A** (sync) except hero `<img>` | full page (1751-1804) | bad id → `view404()` (1737-1738); bad artistId → `view404()` (1738); image `onerror` downgrades resolution (1755) | 404 offers home + full-collection links (1978-1979) |
| **Artist `#/artist/{id}`** | non-Tier-1 fallback bio/panels when no `TIER1` entry (1644,1663,1708-1715) | **N/A** (sync) | full profile (1630-1733) | bad id → `view404()` (1621) | 404 recovery links |
| **Invalid route** | `view404()` "Blank canvas" (1975-1981) | **N/A** | n/a (this IS the fallback) | **N/A(this is itself the failure surface)** | two links: `#/` and `#/artists` (1979) |

**Criterion 27 dispositions (Duchamp: "limit" and "failure" may not exist):**
- **"limit" state → N/A across the scope.** No surface paginates or caps user data
  with a user-visible ceiling. Search hard-slices to 9 (`slice(0,9)`, 2181) **without
  telling the user more exist** — this is a silent truncation, not a "limit" state,
  and is the one decidable place criterion 27's "limit … preserves context" could be
  asserted as a *gap* rather than N/A. Passport import shows counts but no cap.
- **"failure" state → mostly N/A(no backend/no async throw).** The only genuine
  runtime-failure branches that exist are: clipboard reject (3009), `toBlob`/canvas
  export, `localStorage` write in try/catch (81, 2308 — silently swallowed), and
  image `onerror` downgrades. Van Eyck should test criterion 27's "failure" **only**
  at these points; asserting a network-failure state elsewhere would test an absent
  condition.

---

## 7. STATIC VERIFICATION OF DUCHAMP U6, U7, U8 (code inspection only — NOT browser)

I did not open a browser; Vermeer measures separately. These verdicts are from source.

**U6 — route changes don't establish focus/orientation. CONFIRMED (structural), one
item NEEDS BROWSER.**
- `aria-current`: **0 occurrences** anywhere → the current section/page is never
  announced semantically. (grep, §2.)
- **No skip link**: 0 `skip`/skip-link patterns in index.html/css/js. Repeated nav
  (8 links + brand + search + theme = the same ~11 tab stops on every route) cannot be
  bypassed → **criterion 16 "repeated navigation can be bypassed" fails.**
- **No focus management on route change**: `route()` (js/app.js:1986-2030) sets
  `app.innerHTML`, calls `window.scrollTo(0,0)`, `setNav`, `hideSearch` — but makes
  **zero `.focus()` calls** and sets no `tabindex`. After a hash navigation, keyboard
  focus remains wherever it was (or resets to `<body>`), never moving to the new
  page's heading/entry point → **criterion 14 "moves focus to a meaningful entry
  point" fails.**
- `#app` has `aria-live="polite"` (index.html:53). Whether swapping `innerHTML`
  causes a *useful* single announcement of the new page (vs. a noisy or empty one) is
  a runtime AT behavior — **[NEEDS BROWSER: Vermeer/Van Eyck at review].** The
  static fact: there is no dedicated "you are on page X" live-region message; the
  whole main is live, which typically over- or under-announces.
- Every view does set a distinct `document.title` (23/23, §1) — so *tab-title*
  orientation is present even though *in-page focus* orientation is not.

**U7 — state communicated only visually. CONFIRMED for the programmatic layer;
see §2.** Selection state has visible non-color cues (label/fill), but is exposed to
AT **zero** times (`aria-pressed/current/selected/expanded` all 0). Materially true.

**U8 — competing nested/adjacent actions in the "Start with an artist" surface.
CONFIRMED (nested interactive element, programmatically detectable).**
- `js/app.js:1447-1453`: `<a class="entry-card" href="#/artists">` **contains**
  `<button class="ec-surprise" data-random-artist>or surprise me →</button>`
  (button at 1451). A `<button>` nested inside an `<a>` is invalid HTML and an
  ambiguous a11y target → **criterion 17 violation, and it is the *only* true
  nested-interactive-element in the app** (I scanned every `<a>…</a>` and
  `<button>…</button>` region in app.js; exactly one anchor contains an interactive
  descendant, zero buttons do). The click handler does `e.preventDefault()` on the
  button (2074-2079) to salvage behavior, but the nested-element defect remains and is
  what a programmatic checker flags.
- **Distinction Van Eyck needs:** the whole-card pattern elsewhere
  (`<article class="card" data-href>` containing `<a>` links, e.g. 732-740) is **not**
  a nested *interactive element* — `<article>` is not an interactive element; the
  click delegate yields to inner anchors (`if(e.target.closest("a")) return;`, 2147).
  Likewise the list entry (1406-1417) places `<a>`s and a `<button>` as **siblings**
  inside a non-interactive `<li>` — **adjacent, not nested.** So criterion 17's strict
  "nested interactive element" test has **exactly one** failing instance (the
  entry-card button); the whole-card and list-entry patterns are "overlapping/adjacent
  affordances" that fail the *spirit* but not the *programmatic nested-element* test —
  the requirement below separates the two so the pass/fail is unambiguous.

---

## 8. PASSPORT MERGE PATH — confirm/refute (criterion 4)

**Refuted as a distinct feature; confirmed as import semantics.** Grep finds the 4
`merge` occurrences Duchamp counted (`js/app.js`): (1) `function mergePassports(mine,
theirs)` definition (2908-2926); (2) copy "Importing merges it with what's already on
this device — nothing is dropped" (2941); (3) button label "Merge into my passport"
`data-tsx="import"` (2942); (4) the call `mergePassports(getPassport(), window._ppImport)`
inside the **`import`** action handler (3018).

**There is no separate "merge" route, action, or button distinct from import.** The
single entry point is `#/passport/{payload}` → `viewPassportImport` → one button whose
`data-tsx` is literally `"import"` (2942) → handler merges then redirects to `#/taste`
(3017-3021). `mergePassports` is field-wise union with newest-wins on timestamped
arrays (admirations/seen/wantToSee/saved/probes) and set-union on id lists
(skipped/deckSeen/notForMe), newest-wins on scalar objects (quiz/palette/persona/
milestones) (2910-2925).

**Recommendation for criterion 4:** reword the enumerated action list from
"export, share/import, **merge**, and reset" to "export, share, **import (which
merges)**, and reset" — otherwise criterion 4 tests an action that has no independent
UI. The *behavior* (import merges, drops nothing) is real and testable: pass = after
importing a payload with overlapping ids, `getPassport()` contains the union with no
lost signals.

---

## REQUIREMENTS (numbered, testable, tagged must/should)

These make THEORY_001 §7's unbounded criteria decidable. Each cites the section above
that bounds it. Phrased so Van Eyck passes/fails without judgment.

- **R1 (must, bounds crit. 14):** On every `hashchange`, `route()` MUST move keyboard
  focus to the new view's primary heading (or a designated entry point) and that
  element MUST be programmatically focusable. *Test:* after navigating to each of the
  24 routes in §1, `document.activeElement` is within `#app` and not `<body>`.
  *Current: FAILS* (§7 U6 — zero `.focus()` calls).
- **R2 (must, bounds crit. 14):** Each route MUST establish a single, correct current-
  location signal. `document.title` already satisfies the tab-title half (23/23, §1);
  the in-page half requires R1 + R6. *Test:* title matches the §1 table for each route.
- **R3 (must, bounds crit. 16):** A keyboard-operable skip mechanism MUST allow
  bypassing the ~11 repeated header tab stops. *Test:* a focusable "skip to content"
  control exists and moves focus into `#app`. *Current: FAILS* (0 skip links, §7).
- **R4 (must, bounds crit. 16):** All primary actions MUST be operable by keyboard with
  a visible focus indicator. *Test:* controls C1–C18 (§2) are reachable and
  activatable by keyboard. *Current: C1–C10, C12–C18 PASS (real `<button>`/`<a>`); C11
  (influence node) FAILS — `<g>` with no `tabindex`, click-only.*
- **R5 (must, bounds crit. 15):** The current destination and every active control
  state (the frozen set C1–C18, §2 — no others in scope) MUST be perceivable without
  relying on color or position alone, **including programmatically**. *Test:* the
  current nav item exposes `aria-current`; toggles expose `aria-pressed`/`aria-selected`;
  collapsibles expose `aria-expanded`. *Current: FAILS uniformly* (those attributes = 0,
  §2); visual non-color cues mostly present.
- **R6 (should, bounds crit. 14):** The route-change announcement MUST fire exactly
  once per navigation with the new page identity. *Test:* **[NEEDS BROWSER]** — verify
  the `#app` `aria-live` region announces the new heading once, not the entire view.
- **R7 (must, bounds crit. 17):** No interactive surface MAY contain a **nested**
  interactive element. *Test (programmatic):* no `<a>`/`<button>` contains a
  descendant `<a>/<button>/<input>/<select>/<textarea>`. *Current: exactly ONE failure
  — the `ec-surprise` button inside the "Start with an artist" entry-card anchor
  (js/app.js:1447-1451, §7 U8).*
- **R8 (should, bounds crit. 17):** No surface SHOULD present two *overlapping*
  activation targets with different destinations. *Test:* whole-card `data-href`
  patterns (§7) and the list-entry (anchors + Admire button in one row) are documented
  as adjacent-not-nested; they pass R7 but should be reviewed against R8. *This
  separates the programmatic nested-element failure (R7) from the softer overlap
  concern so R7's pass/fail stays clean.*
- **R9 (must, bounds crit. 22):** Essential timeline content (painter name, years,
  movement, artist link — §4) MUST be keyboard-reachable and readable by AT. *Test:*
  every `.tl2-bar` is a focusable `<a>` whose accessible name includes name+years.
  *Current: PASSES structurally* (bars are anchors with title+text) — but see R10.
- **R10 (must, bounds crit. 22):** Essential influence content (each relationship as
  source/target/type/direction + artist links — §4) MUST have a keyboard-accessible,
  AT-readable equivalent. *Test:* the relationship data is reachable without a mouse
  via the per-artist "Lineage & circle" panels (js/app.js:1699-1704, PASSES) OR a list
  alternative; the graph itself (`#ig-svg`) additionally SHOULD carry
  `role="img"`+`aria-label` (currently absent, 1095) and its node interaction is
  click-only (FAILS at the graph, passes at the equivalent).
- **R11 (must, bounds crit. 24):** For fixture queries F19–F22 (§3), every
  `startsWith` match MUST rank above every non-prefix `includes` match, and an exact
  full-name match (when present) MUST rank #1. *Test:* run §3 fixture; assert ordering.
  *Current: two-bucket split already guarantees prefix>substring; residual is
  incidental-substring ordering within the `contains` bucket.*
- **R12 (must, bounds crit. 25):** Fixture queries F1–F18 (§3) MUST resolve to the
  listed correctly-typed destination. Queries with no matching data (accented-name
  ascii typos, meta-only terms — documented in §3) are OUT of scope for "resolves" and
  IN scope for the empty-state requirement R13. *Test:* run fixture; assert #1 == table.
- **R13 (must, bounds crit. 23/27):** Search empty result (F23/F24 and every
  documented no-match in §3) MUST show `.sr-empty` with the query echoed. *Current:
  PASSES* (2184). *Additionally (should):* when results are truncated to 9 of more
  (§6 limit note), the UI SHOULD indicate more exist — *current: silent slice, FAILS
  the "preserves context" half of crit. 27.*
- **R14 (must, bounds crit. 26):** The home Explore promise and the `#/explore`
  destination MUST name the same instruments. *Test:* the instrument set in the home
  entry-card copy (js/app.js:1460-1465) equals the set of links on `#/explore`
  (1338-1350). *Current: FAILS* — home says 4 (timeline, constellation, family trees,
  world map), Explore offers 2 (§5).
- **R15 (must, bounds crit. 32):** Each canonical journey J1–J5 (§5) MUST, at every
  step, expose an observable anchor, relationship, consequence, and onward path per the
  §5 tables. *Test:* walk each journey; assert each cell's cited element/route exists.
- **R16 (must, bounds crit. 35):** No route currently reachable only via in-content
  links (the §1 "content-only" set) MAY become *less* discoverable without a logged,
  approved tradeoff + rollback. *Test:* diff the discoverability baseline in §1
  against any proposed change.
- **R17 (must, bounds crit. 4):** Import MUST merge without dropping signals, and the
  criterion wording SHOULD change "merge" → "import (which merges)" since no distinct
  merge action exists (§8). *Test:* import a payload with overlapping + newer ids;
  assert `getPassport()` == field-wise union with newest-wins, nothing lost.
- **R18 (must, bounds crit. 15 for passport):** Passport action buttons (C17/C18) MUST
  expose pressed state programmatically (`aria-pressed`), not only the "Admired ✓"
  label + `.on` fill. *Test:* toggled button reports pressed to AT.

---

## OPEN QUESTIONS

1. **[NEEDS BROWSER — Vermeer]** Does the `#app` `aria-live="polite"` region produce a
   single useful route announcement, or does swapping the entire `innerHTML` cause
   over/under-announcement? R6 depends on this; I only assert statically that no
   dedicated per-page live message exists.
2. **[NEEDS BROWSER — Vermeer]** U1 (mobile nav "conceals most destinations") and U2
   (root horizontal overflow): css:837 sets `.main-nav{overflow-x:auto}` at ≤820px and
   css:73 sets root `overflow-x:hidden` — the *mechanism* for a horizontally scrolling
   nav is real, but "conceals" and any actual overflow are measurements I do not make.
   Criteria 18/19 rest on Vermeer's numbers.
3. **Criterion 2 rewrite (Duchamp noncritical #4):** should the deck-warning criterion
   adopt the objective ADMIRE_SPEC rule (docs/ADMIRE_SPEC.md:99 — "for each of the 5
   axes, ≥2 works ≥+40 and ≥2 works ≤−40")? That is Seurat/data territory, not mine,
   but it would make crit. 2 testable rather than paperwork-satisfiable. Flagging only.
4. **Criterion 27 "limit" state:** confirm with the spec owner whether the silent
   `slice(0,9)` search truncation (§6) should count as a "limit" state requiring a
   "more results" affordance (R13 should-clause), or be accepted as N/A. This is the
   one place the limit-state question is decidable rather than absent.
5. **R7 fix ownership:** the single nested-element defect (entry-card button, §7 U8) is
   a Dürer fix, not mine (Gate 1). Recorded here only as the frozen pass/fail target.
