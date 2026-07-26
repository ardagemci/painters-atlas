# PIG-001 — Unit 25 build log (contrast, zoom, C-8 remediation)

**Note on authorship:** Dürer committed all six groups and was cut off by a
session limit before running the required verification or writing this log. The
verification below was performed by the **Synthesis Lead** and is reported as
such. Nothing here is inherited from the implementer's own claims.

## Commits

| Group | Commit | Scope |
| --- | --- | --- |
| 25a | `b7834b5` | AC19 contrast tokens (Matisse Table 1) |
| 25b | `a11daa5` | AC19 re-pointings — gold-as-text becomes gold2 |
| 25c | `e126b40` | AC19 timeline bar ink by measurement, not by luma |
| 25d | `c7b9765` | AC19 hero over the generative canvas (light theme) |
| 25e | `02b5a93` | AC18 containment at 200% text zoom |
| 25f | `2296f9d` | AC15 / C-8 — one route announcement channel |

Working tree clean; validator green with **zero warnings** after all six.

## Verification performed (Synthesis Lead)

### AC19 tokens — VERIFIED PASS against real surfaces

Every implemented value matches Matisse's specification exactly. Computed
against the three surfaces that are actually painted (`--bg`, `--panel`,
`--panel2` — Matisse established `--bg2` is never used as a background):

| token | theme | hex | bg | panel | panel2 |
| --- | --- | --- | --- | --- | --- |
| `--muted` | light | `#585244` | 6.59 | 7.19 | 6.42 |
| `--faint` | light | `#706755` | 4.74 | 5.17 | 4.62 |
| `--gold2` | light | `#81632b` | 4.75 | 5.18 | 4.63 |
| `--wine` | light | `#a05141` | 4.76 | 5.19 | 4.64 |
| `--teal` | light | `#2b7368` | 4.75 | 5.18 | 4.63 |
| `--blue` | light | `#476a98` | 4.72 | 5.14 | 4.59 |
| `--rose` | light | `#b43e56` | 4.74 | 5.17 | 4.62 |
| `--mauve` | light | `#b23a74` | 4.76 | 5.19 | 4.63 |
| `--faint` | dark | `#8b8372` | 5.20 | 4.90 | 4.62 |
| `--rose` | dark | `#ca6478` | 5.22 | 4.91 | 4.63 |

**All body-text tokens pass AA (4.5:1) on every real surface, both themes.**
`--gold` (light `#9e7938`, min 3.31) carries only UI and large text after the
25b re-pointing and clears its 3.0 floor. Dark tokens Matisse marked as passing
were left untouched and still pass.

### Groups 25c–25f — structurally confirmed, browser re-verification outstanding

| Group | Static confirmation |
| --- | --- |
| 25c | `luma(c)>0.62` removed from js/app.js (0 occurrences) |
| 25d | `.hero-shade` present in css/styles.css (3 rules) |
| 25e | `.main-nav{display:flex;flex-wrap:wrap;gap:4px;flex:1}` — wrap applied as directed; `.skip-inline` now styled (2 rules) |
| 25f | `#route-status` gone from index.html and from app.js runtime (the single remaining hit at js/app.js:2317 is a historical comment) |

## Honest limits of this verification

The contrast harness `evidence/contrast-audit.py` has two passes with different
reach, and this matters for reading its output:

- **Pass 1 parses `css/styles.css` live** — it reflects this unit's changes, and
  is the basis of the table above.
- **Pass 2 reads `contrast-pairs-measured.csv`**, a static snapshot of DOM-measured
  pairs captured by Vermeer *before* this unit. Re-running the script therefore
  still prints "43 rendered-pair failures" — **that number is stale by
  construction** and says nothing about the current build. It will only move
  when the DOM walk is re-run in a browser.
- **Pass 3 is browser-sampled** and likewise frozen at pre-fix values, including
  the light hero composite at 2.47:1.

**Still requiring browser re-verification (Vermeer):** the light-mode hero
composite over the generative canvas (Matisse's worst-case bound predicts
6.62 / 3.23 / 4.29 against a fully opaque black cover pixel, versus a 3.0 floor);
26 routes at 200% text zoom (previously 115–117px overflow on every route);
single-announcement behaviour on route change; timeline bar ink across the 14
swatches; and a re-walk of the DOM pair set to retire the stale Pass 2 number.

**Also outstanding from Matisse's adjudication:** the 390px screenshots are a
cropped wider layout rather than a true mobile render (words sheared mid-glyph,
nav absent) even though the DOM measurements were correct. They must be
re-captured before Gate 2 certification relies on them.
