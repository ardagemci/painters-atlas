# BROWSER EVIDENCE — PIG-001 (closing pass)

**Reviewer:** Vermeer (`claude-browser-reviewer`), Browser Evidence Reviewer
**Date:** 2026-07-26
**Branch:** `pig-001-stabilization` — verified **not** `main`; no push, no merge, no deploy.
**Commit under test:** `64d68a0` (HEAD), working tree clean of production edits. I edited no
production file; everything I wrote lives under `protocol/tasks/PIG-001/evidence/`.

This pass exists because Van Eyck's Gate 2 review returned **PASS 26 · FAIL 0 · UNSUPPORTED 3**
(`quality-review.md`): AC4, AC8 and AC19 had no evidence, and unit 26 had never been verified by
anyone but its own implementer. My brief was to produce that evidence.

> **REPAIRED 2026-07-28 · Van Eyck N-4.** This document was committed at `73ddc27` carrying four
> literal `<!--PLACEHOLDER-*-->` markers — §1.2's two AC19 tables, all of §6, and §9 — because the
> session writing it up was cut off. Those four sections are now rendered **from the raw data that
> was already on disk** (`harness/vermeer-closing/photo-all-{dark,light}.json`, via that pass's own
> renderer `table.py`), each under a dated repair note. **No measurement was re-run and no number
> was reconstructed from memory.** Rendering the light data surfaced a defect in that run's own
> instrument, which is reported at §1.2a rather than smoothed over. **§1's AC19 FAIL is history:**
> units 27, 28 and 29 have since closed it, and the current measurements are in
> `browser-evidence-final.md`. History is cross-referenced here, not rewritten.

**Everything below is something I observed in a browser at `64d68a0`.** Where a number
disagrees with a number someone else reported, I say so and mine is the one I stand behind.
Where I could not observe something, it is in the NOT TESTED list and is not inferred.

---

## ENVIRONMENT

| | |
| --- | --- |
| Serve | `python3 -m http.server 8421 -d .` from the repo root |
| Browser | Google Chrome, headless (`--headless=new`), driven over the DevTools Protocol |
| Viewports | `Emulation.setDeviceMetricsOverride` — **never** `--window-size`, which this Mac clamps to a 500 px minimum and which silently produced round 1's defective 390 px captures |
| Cache | `Network.setCacheDisabled=true`; every route loaded as a fresh document behind a unique query string, so no CSS or data byte is reused between measurements |
| In-page assertions | every capture and measurement asserts `window.innerWidth`, `documentElement.clientWidth`, `#app` padding, `.main-nav` treatment and `documentElement.dataset.theme` **at shutter time**; a run that cannot assert them fails rather than reports |
| Harnesses | new: `harness/vermeer-closing/{photos,ac4,ac8,ac8b,gold,shot,probe}.py` · reused: `harness/cdp-r2/{cdp,png,run_a,run_eg}.py`, `harness/durer-u26/{hero,nav}.py` |

**Verified the served build is the branch under review** before capturing anything: `#/museums`
reports "104 museums", `#/artists` reports "All 256 painters" (the D-016 corpus, not the frozen
spec's 247), `.main-nav` at 390 px computes `flex-basis:100%` / `flex-wrap:nowrap` (unit 26b), and
`--hero-veil` resolves to `.8` dark / `.86` light (unit 26a). This is HEAD, not `a4898d3`.

## VIEWPORTS & THEMES COVERED

| Work | Viewports | Themes |
| --- | --- | --- |
| AC19 photograph composites | 1440×900 | dark + light, 104 venue pages each |
| AC4 journey matrix | 1440×1200 | dark |
| AC8 storage failure | 1440×900 | dark |
| Screenshot pack | 1440×900 desktop, 390×844 mobile | dark + light, 16 routes each = 64 |
| Unit-26 hero | 1440×900 and 390×844 | dark + light |
| Unit-26 nav / zoom | 390×844, 1280×800, 1270×800 | dark + light (390); dark (zoom) |
| Console / network sweep | 1440×900 | dark, 26 routes |

---

# 1 — AC19 · TEXT OVER WIKIMEDIA PHOTOGRAPHS · **FAIL**

## 1.1 How I got round the cross-origin problem

Round 2 recorded this class NOT TESTED because `canvas.getImageData()` throws on a canvas
tainted by `upload.wikimedia.org`. **This harness never calls `getImageData`.** It uses the
two-shot glyph-diff that Dürer and I already use for the hero: CDP captures the *composited*
pixels as a PNG which is then decoded locally in pure Python (`harness/cdp-r2/png.py`), so the
same-origin policy never applies. Shot A is the page as rendered; shot B is the same page with
the candidate glyphs removed; a pixel counts only where A and B differ by more than 60 (sum of
channel deltas), which confines the sample to where a glyph actually lands. Ink is the *declared*
paint; backdrop is that same pixel in shot B — i.e. the photograph as actually composited
through every scrim above it.

**Detection is deliberately an over-approximation**: any visible text-bearing element whose rect
intersects the rect of an `<img>` served from `upload.wikimedia.org`, on any route. Over-selection
is harmless (the measured backdrop is then simply the opaque panel above the photo);
under-selection would not be, so the net was cast wide and then measured honestly.

**A defect in my own instrument, found and fixed mid-pass (recorded because it produced a false
positive I nearly reported).** My first shot-B used `visibility:hidden`, which removes an
element's *own background* as well as its glyphs. On `#/daily` that deleted the pill behind
"Click to look closer" and reported the raw Rembrandt underneath as the backdrop — **2.38:1, a
failure I was about to publish.** With shot B corrected to `color:transparent` +
`-webkit-text-fill-color:transparent` (glyphs only, every painted layer kept), the same element
measures **14.82:1 — PASS**. All numbers below come from the corrected instrument. The museum
findings are unaffected by the fix: every failing element there has a transparent background, so
both methods render shot B identically — which I confirmed by re-running the full sweep.

## 1.2 What actually fails

Two hero shapes exist on museum pages (`js/app.js:1472-1484`): a **collage** of up to six PD
artwork photographs (most venues) or a single **building photograph** — both from
`upload.wikimedia.org`, both under one scrim, `.mu-shade`
(`linear-gradient(180deg, rgba(var(--bg-rgb),.18), rgba(var(--bg-rgb),.94) 80%)`,
`styles.css:1210`). All 104 museum pages measured, both themes, on real glyph pixels:

> **Repair note, 2026-07-28 (Van Eyck N-4).** This section, §6 and §9 shipped in the committed
> object at `73ddc27` as four literal `<!--PLACEHOLDER-*-->` markers: the session that produced
> this pass was cut off while writing it up, and the tables were never rendered. They are rendered
> **now, from the raw data that was on disk at the time** —
> `harness/vermeer-closing/photo-all-dark.json` and `photo-all-light.json`, via that pass's own
> renderer `harness/vermeer-closing/table.py`. Nothing here is a new measurement and nothing is
> reconstructed from memory. Where the raw data will not support a number, that is stated instead
> of a number. **§1's FAIL verdict is history, not the current state**: units 27, 28 and 29 have
> since closed it — see `browser-evidence-final.md` §3 for the measurements at HEAD `a686d98`.

**Dark theme — 104 venue pages, 1 467 measured text elements, 919 of them inside the photograph
hero.**

| element in the hero | px | floor | **worst measured** | venue | fails on |
| --- | --- | --- | --- | --- | --- |
| breadcrumb, current page (`--muted`) | 12.5 | 4.5 | **1.01** | `k20-dusseldorf` | **97 of 102 venues** |
| breadcrumb separators (`--muted`) | 12.5 | 4.5 | **1.31** | `tate-modern` | **91 of 102 venues** |
| breadcrumb links (`--body-ink`) | 12.5 | 4.5 | **1.33** | `stanley-museum-iowa` | **91 of 104 venues** |
| `h1.display` venue name (`--ink`) | 54.4 | 3.0 | **2.48** | `k20-dusseldorf` | **1 of 104 venues** |
| `.mu-sub` city · country · founded (`--muted`) | 15.2 | 4.5 | **3.23** | `museu-picasso-barcelona` | **74 of 104 venues** |
| `.mu-hook` editorial line (`--gold2`) | 18.9 | 4.5 | 8.98 | `museu-picasso-barcelona` | — (0 of 104) |
| `Share this page` chip | 12.5 | 4.5 | 13.85 | `st-peters-basilica` | — (0 of 104) |

Below the hero, on the same pages: 548 further text elements measured, **1** class fails —
`span.count` worst **4.44** on 1 of 45 venues (`neue-galerie`).

**Light theme — 104 venue pages, 1 461 measured text elements, 913 of them inside the photograph
hero.** *Read with the caveat below.*

| element in the hero | px | floor | **worst measured** | venue | fails on |
| --- | --- | --- | --- | --- | --- |
| breadcrumb links (`--body-ink`) | 12.5 | 4.5 | **1.00** | `prado` | **99 of 104 venues** |
| breadcrumb separators (`--muted`) | 12.5 | 4.5 | **1.00** | `louvre` | **97 of 98 venues** |
| breadcrumb, current page (`--muted`) | 12.5 | 4.5 | **1.00** | `louvre` | **102 of 103 venues** |
| `h1.display` venue name (`--ink`) | 54.4 | 3.0 | **1.00** | `prado` | **16 of 104 venues** |
| `Share this page` chip | 12.5 | 4.5 | **1.00** | `prado` | **15 of 104 venues** |
| `.mu-sub` city · country · founded (`--muted`) | 15.2 | 4.5 | **1.18** | `moderna-museet` | **88 of 104 venues** |
| `.mu-hook` editorial line (`--gold2`) | 18.9 | 4.5 | **2.36** | `moderna-museet` | **104 of 104 venues** |

Below the hero, on the same pages: 548 further text elements measured, 6 classes fail — `a` worst
2.15 on 17 of 78 venues, `div.lbl` 2.37 on 13 of 63, `h2.sec-title` 1.06 on 7 of 45, `p` 1.43 on
6 of 14, `p.img-credit.mu-credit` 2.14 on 18 of 78, `span.count` 3.03 on 43 of 45.

### 1.2a — A defect in the LIGHT run, found while rendering this table

Rendering the raw light data at repair time surfaced something the original pass never got to
inspect, and it is reported rather than smoothed over. **The light run carries a contamination
signature that the dark run does not:**

| signature | dark run | light run |
| --- | --- | --- |
| rows reporting a ratio of exactly **1.00** (ink pixel identical to backdrop pixel — arithmetically impossible for real glyphs on a scrim) | **0** of 1 467 | **33** of 1 461 |
| rows whose glyph-pixel count exceeds 50 000 (larger than any element's glyph area; `p` reaches **214 760**, roughly the whole viewport) | **0** | **11** |
| venues showing either signature | **0** | **16** |

Both signatures are what shot-A/shot-B divergence looks like when the two loads do not render the
*same* collage — the diff then covers the photograph instead of the glyphs. It is confined to 16
venues: `albertina`, `belvedere`, `buffalo-akg`, `gemaldegalerie-berlin`,
`isabella-stewart-gardner`, `louvre`, `mauritshuis`, `moderna-museet`, `moma`, `munch-museum`,
`national-gallery-dc`, `national-gallery-london`, `prado`, `sistine-chapel`, `tretyakov`,
`van-gogh-museum`. **Every `1.00` in the light table above comes from that set**, so the light
table's worst-case cells and its below-hero list are not trustworthy as printed.

Excluding those 16 venues outright leaves **88 clean venues, 772 band measurements**, and the
light picture is coherent with the dark one:

| element in the hero | px | floor | **worst, clean venues only** | venue | fails on |
| --- | --- | --- | --- | --- | --- |
| breadcrumb, current page (`--muted`) | 12.5 | 4.5 | **1.24** | `museo-frida-kahlo` | **87 of 88 venues** |
| breadcrumb separators (`--muted`) | 12.5 | 4.5 | **1.29** | `museo-frida-kahlo` | **82 of 83 venues** |
| breadcrumb links (`--body-ink`) | 12.5 | 4.5 | **1.57** | `palazzo-barberini` | **83 of 88 venues** |
| `h1.display` venue name (`--ink`) | 54.4 | 3.0 | **2.88** | `k20-dusseldorf` | **1 of 88 venues** |
| `.mu-hook` editorial line (`--gold2`) | 18.9 | 4.5 | **3.60** | `scottish-national-gallery` | **88 of 88 venues** |
| `.mu-sub` city · country · founded (`--muted`) | 15.2 | 4.5 | **3.84** | `palazzo-barberini` | **72 of 88 venues** |
| `Share this page` chip | 12.5 | 4.5 | 11.27 | `uffizi` | — (0 of 88) |

Below the hero, clean venues: 412 measurements, **3** classes below floor — `span.count` 3.38,
`p.img-credit.mu-credit` 4.34, `a` 4.34, all worst on `villa-farnesina`.

**This changes no verdict.** F-V1 is a failure in *both* themes on *both* readings, and the class
that fails is the same class on the same elements; the contaminated cells only exaggerate how
badly. It matters for two reasons and they are both recorded: (a) the light figures in the table
above must not be quoted as measurements of the shipped build, and (b) the true light worst cases
are `1.24 / 1.29 / 1.57 / 2.88 / 3.60 / 3.84`, not `1.00`. Dürer's unit 27 BEFORE run reproduced
this pass's **dark** figures (`a` 1.33, `span.sep` 1.31, `div.mu-sub` 3.23) to two decimals; the
dark run is the one that has cross-operator agreement, and it is the one this finding rests on.
**A hypothesis about the mechanism, offered as a hypothesis and not as a finding:** this pass's
`photos.py` writes both shots to *fixed* `/tmp` paths, so two concurrent runs read each other's
pixels. Dürer's unit-27 driver `harness/durer-u27/mu.py` documents exactly that failure and fixes
it with per-process paths. The file mtimes are consistent with a second run having overlapped the
light sweep, but I did not observe the overlap and I am not claiming it — the contamination is
observed, its cause is not.

## 1.3 Confirmed with my own eyes, not only with a script

- `ac19-museum-met__desktop-1440x900__dark.png` — "Atlas / Museums / The Metropolitan Museum of
  Art" is **invisible** where it crosses Dürer's woodcut on pale paper.
- `ac19-museum-k20__desktop-1440x900__dark.png` and `…__light.png` — "Kunstsammlung
  Nordrhein-Westfalen (K20)" runs straight across a saturated Kandinsky; the breadcrumb row
  above it has effectively vanished in both themes.
- `ac19-museum-frida-kahlo__desktop-1440x900__light.png` — the light-theme worst case.

## 1.4 Root cause (measured, not guessed)

`.mu-shade`'s alpha ramps as a percentage of **`.mu-hero`'s** height, but the text block
`.mu-hero-body` is bottom-anchored and its own height varies with the venue name (one line or
two), the presence of a hook and the presence of a founding year. So the *same* element lands at
a different scrim alpha on every venue. Measured from the shipped gradient:

| position in the hero | `.mu-shade` alpha there |
| --- | --- |
| 20 % | .37 |
| 35 % | .51 |
| 50 % | .66 |
| 65 % | .80 |
| ≥ 80 % | .94 |

The breadcrumb row sits between roughly 20 % and 45 % on a tall hero. The alpha it needs, computed
against a worst-case opaque photograph pixel (white in dark, black in light) — this is the number
that fixes the criterion:

| theme | element | ink | floor | **minimum scrim alpha required** |
| --- | --- | --- | --- | --- |
| dark | breadcrumb link | `--body-ink` `#d8d2c4` | 4.5 | **.675** |
| dark | breadcrumb current + separators, `.mu-sub` | `--muted` `#9b937f` | 4.5 | **.864** |
| dark | `h1.display` | `--ink` `#ece6d9` | 3.0 | **.506** |
| light | breadcrumb link | `--body-ink` `#433c31` | 4.5 | **.705** |
| light | breadcrumb current + separators, `.mu-sub` | `--muted` `#585244` | 4.5 | **.834** |
| light | `h1.display` | `--ink` `#2b2620` | 3.0 | **.472** |
| light | `.mu-hook` | `--gold2` `#81632b` | 4.5 | (fails at the shipped alpha — see table) |

## 1.5 What would fix it

**The smallest change that closes the criterion is one rule, not a re-design.** Put the scrim on
the text block instead of on the hero box, so it stops depending on hero height:

```css
.mu-hero-body{
  background:linear-gradient(180deg, rgba(var(--bg-rgb),.88), rgba(var(--bg-rgb),.96));
}
```

`.88` clears the worst required alpha (`.864` dark, `.834` light) for every element in the band,
in both themes, against a worst-case opaque photograph pixel — i.e. it is a **bound**, not a
sample, which is the standard Matisse set and unit 26 met for the home hero. The photograph keeps
its full presence everywhere the text is not, which is more of it than the present
`.94`-at-the-bottom ramp already leaves. `.mu-shade` itself can then be *reduced*.

Two cheaper-looking alternatives that I checked and do **not** recommend on their own:
re-pointing `.mu-sub` and the breadcrumbs from `--muted` to `--body-ink` only lowers the
requirement to `.675`, still above the `.37–.51` the band actually gets; and steepening
`.mu-shade` to reach `.94` by 30 % of the hero erases most of the photograph, which is the thing
the hero exists to show.

Whatever is chosen, **it must be re-measured with this harness across the venue set**, not on one
convenient museum: `python3 harness/vermeer-closing/photos.py museums 0 dark` and `… light`.

**FINDING F-V1 (MAJOR, criterion-failing) · AC19** — see §6.

---

# 2 — AC4 · THE FROZEN JOURNEY MATRIX · **PASS**

Never run before; `build-log-wave-c.md:362` records it under "Not claimed, deliberately."
I walked all five frozen journeys of `unrouted/ux-requirements.md` §5 **and** AC4's own
eleven-link chain, end to end, with real CDP mouse and key events on real elements — never a
JavaScript shortcut. Full transcript: `harness/vermeer-closing/ac4-journeys.json`.

**33 steps · 0 FAIL.**

### The five frozen journeys (`ux-requirements.md` §5) — 21 steps

| J | step | route reached | what I did | anchor / relationship / consequence / onward | verdict |
| --- | --- | --- | --- | --- | --- |
| **J1** | entry | `#/` | loaded the home route | h1 "Find your place in the history of art.", 590 links | OK |
| J1 | land on artist | `#/artist/leonardo-da-vinci` | typed `Leonardo` in `#search`, clicked option 1 ("Leonardo da Vinci 1452–1519"); `aria-expanded` flipped to `true` | hero `h1` = "Leonardo da Vinci" · **10 chip links** (High Renaissance, Oil Painting, Sfumato, Fresco, Tempera…) · why-card "Why da Vinci matters — Leonardo made painting a form of research…" · chip `<a>` present | **PASS** |
| J1 | traverse a relationship | `#/movement/high-renaissance` | **keyboard**: focused the first chip link, pressed **Enter** | h1 "High Renaissance" · "The painters" heading listing **7** painter links · 25 chips onward | **PASS** |
| J1 | back | `#/artist/leonardo-da-vinci` | browser Back | hero h1 still "Leonardo da Vinci" — **anchor not lost** | **PASS** |
| **J2** | land on artwork | `#/artwork/the-starry-night` | direct load | h1 "The Starry Night" + artist sub-link → `#/artist/vincent-van-gogh` · chips Post-Impressionism / Oil Painting / Impasto / Netherlands · panels **"The picture", "What to notice", "Where it hangs", "More by van Gogh", "Near it in the atlas", "Go next"** · **3** passport buttons | **PASS** |
| J2 | personal action | same | clicked **Admire** | label `Admire` → `Admired ✓`, `aria-pressed` `false` → `true`; `seen` and `saved` stayed `false` (independent); `pigment.taste.v1` gained the id | **PASS** |
| J2 | persistence | same | full reload | still `Admired ✓` / `aria-pressed="true"` | **PASS** |
| **J3** | lists → a list | `#/list/paintings-that-still-scare-us` | clicked the list card | h1 = list title · real `<ol class="list-entries">` with **10** entries · **10** per-entry `.le-note` ("Not screaming — hearing it. That's worse.") · 20 entry links | **PASS** |
| J3 | end of list | same | scrolled | **"More lists"** section, 3 sibling list links | **PASS** |
| J3 | entry → artwork | `#/artwork/the-scream` | clicked entry 1 | h1 "The Scream", 10 chips onward | **PASS** |
| **J4** | start | `#/palette` | loaded, "Begin →" present | h1 "Find your palette." | **PASS** |
| J4 | tones (step 1) | `#/palette` | clicked 4 of **20** tone buttons | progress read **"1 of 4 chosen" → "4 of 4 chosen"** at each click; CTA `disabled` **true → false** exactly at 4; `aria-pressed` count 1→4 | **PASS** |
| J4 | deck (step 2) | `#/palette` | answered **16** cards, alternating Admire / Pass | kicker "Step 2 of 3 · the deck"; text progress **"1 of 16" … "16 of 16"** at every card; bar width 0 % → 93.75 %; auto-advanced at 16 | **PASS** |
| J4 | questions (step 3) | `#/palette` | answered **5** questions | kicker "Step 3 of 3 · five questions"; **"question 1 of 5" … "question 5 of 5"**; bar 0 % → 80 %; 4 options each; auto-advanced to reveal | **PASS** |
| J4 | reveal + **Passport creation** | `#/palette` | (auto) | signal-word h1 ("figurative + dramatic."), taste-map SVG, **3** persona candidates, "Decide later", "To your taste page →", handoff of **3** matched artists + "List for you: Paint You Can Almost Touch"; `pigment.taste.v1` **written**, `milestones.onboarded=true` | **PASS** |
| J4 | adopt → Passport | `#/taste` | clicked "Adopt this Persona", then "To your taste page →" | persona `border-crosser` stored with `adoptedAt`, **preserved across the handoff**; h1 "The Border-Crosser"; chips Copy share link / Retake onboarding / Back up data / Reset everything | **PASS** |
| **J5** | explore hub | `#/explore` | loaded | h1 "Explore"; lede "Four instruments…"; **4** entry-cards → `#/timeline`, `#/influences`, `#/movements`, `#/nations` | **PASS** |
| J5 | timeline projection | `#/timeline` | clicked the timeline entry-card | h1 "The grand timeline"; controls Compact / Standard / Detail + century isolates; **256** bar links into `#/artist/*` | **PASS** |
| J5 | timeline → canonical page | `#/artist/duccio` | clicked a bar ("Duccio di Buoninsegna") | artist page renders, 8 chips onward | **PASS** |
| J5 | influence projection | `#/influences` | loaded | h1 "The influence graph"; `#ig-svg` `role="group"` `aria-label="Influence graph — 204 painters, 238 relationships"`; **204** nodes; edge-type legend taught·30 / influenced·133 / friends·57 / rivals·14 / partners·4 | **PASS** |
| J5 | focus a node → lineage | `#/influences` | focused an `.ig-node`, pressed **Enter** | `#ig-info` un-hidden: "Leonardo da Vinci 1452–1519 · influenced Raphael · rival of Michelangelo Buonarroti" + **"Open da Vinci's page →" → `#/artist/leonardo-da-vinci`** | **PASS** |

**All five frozen Pass conditions hold**, including J1's keyboard-only clause and J4's
"six-step machine completes with visible progress at each step … and reveal→`#/taste` preserves
the saved persona".

**One divergence between the frozen table and the build, in the build's favour** (recorded, not
scored as a failure): `ux-requirements.md` §5 describes `#/explore` as offering **two**
instruments and flags "promise ≠ destination inventory — CONFIRMED in code". At HEAD `#/explore`
offers **four** — timeline, influences, movements, nations — which is exactly what the home card
promises. The frozen table is stale; the asymmetry it recorded has been closed, which is what
AC22 required. See note N-V1.

### AC4's own eleven-link chain — 12 further steps

| link | observed | verdict |
| --- | --- | --- |
| 1 entry · 2 onboarding · 3 Passport creation | the J4 walk above, run on a cleared `localStorage` | **PASS** |
| 4 Admire action | Admired *Mona Lisa* on its own page → `aria-pressed="true"`, `Admired ✓` | **PASS** |
| 5 consequence explanation | `#/taste` states it in words: *"Position: figurative + dramatic · secondary signals: experimental · map is provisional · **9 admirations inform it**"*, plus "Two islands on your map — 56 % and 44 % of you" and the Discovery-rings section | **PASS** |
| 6 persistence | survived two full document loads | **PASS** |
| 7 return | navigated away and back to `#/taste`; persona, map and admirations all intact | **PASS** |
| 8 export **or** share | "Back up data (.json)" produced a **4 747-char** `pigment-passport.json` download (intercepted, not written to disk); "Copy share link" — with `navigator.clipboard` removed so the build's **own** fallback prints the URL — produced `…#/passport/<2 575-char payload>` | **PASS** |
| 9 import | opened that share URL on a device already holding a **different** passport → "A passport arrived." · *"9 admirations · 0 seen in person · persona: The Border-Crosser"* · states plainly which fields combine and which cannot | **PASS** |
| 10 conflict handling | "Choose what to keep →" → **"Which of these should Pigment keep?"** with per-field `Keep mine — ash, ash, ash, ash` / `Take theirs — Caravaggio Black, Monet Fog, Verdigris, Lamp Smoke` (`aria-pressed` on the chosen one) **plus "Cancel — change nothing"** | **PASS** |
| 10b merge applied | admirations `[the-night-watch]` → **9 entries, union, nothing removed**; persona `null` → `border-crosser` per the choices; landed on `#/taste` | **PASS** |
| 11 reset | "Reset everything" → confirm *"Erase your Taste Passport from this device? Export it first if you want a copy."* → `localStorage.getItem('pigment.taste.v1')` is **`null`**; `#/taste` shows "No map yet — let's sketch one." | **PASS** |

**No broken or unexplained transition anywhere in the chain.** **AC4 is now supported.**

---

# 3 — AC8 · STORAGE-FAILURE RECOVERY · **PASS**

Van Eyck verified only the no-false-success half and observed "no user-visible retry / recovery /
export affordance", recording F-4. **I exercised the rest and the affordances are there.** His
probe missed them because no passport existed to fail against. Raw results:
`harness/vermeer-closing/ac8-storage.json`, `ac8-notice-chip.json`.

### S1 — `localStorage.setItem` throws `QuotaExceededError`, with a real passport present

Seeded a valid 436-byte passport, then made `setItem` throw for `pigment.taste.v1` only, then
clicked **Admire** on `#/artwork/the-starry-night` with a real mouse event.

| AC8 clause | observed |
| --- | --- |
| does not claim success | **holds** — label stayed `Admire`, `aria-pressed="false"`, `.on` absent |
| preserves context | **holds** — the stored bytes are **byte-identical** afterwards (436 → 436); the artwork page is unchanged and still fully operable |
| tells the user truthfully | **holds** — `#pp-notice` appears, `role="status"`, `display:block`, 560×150 box: *"Not saved. This device would not store your Taste Passport — it may be out of room, or site data may be switched off for this browser. **Nothing already saved has changed.**"* |
| retry / recovery / **export** path | **holds** — three affordances in the notice, all of which I clicked: **"Back up data (.json)"** → a real 943-char `data:` download named `pigment-passport.json`; **"Open the Taste Passport"** → navigates to `#/taste`, focus lands on `h1.display`, the passport's contents render, the stored passport is still intact; **"Dismiss"** → `hidden=true`, `display:none` |

The notice **survives navigation** (still present and visible after moving to `#/museums`), so a
user who navigates away does not lose the message.

> Correction to my own method: in the first run I had overridden
> `HTMLAnchorElement.prototype.click` to intercept the export download, which also disabled the
> notice's "Open the Taste Passport" link — that step was measuring my harness, not the build. It
> was re-run cleanly with a real mouse click (`ac8b.py`, `ac8-notice-chip.json`) and passes.

### S2 — corrupt `pigment.taste.v1` present (`{"version":1,"admirations":[{"id":"mona-lisa","at":"2026` — truncated JSON)

| AC8 clause | observed |
| --- | --- |
| does not claim success | **holds** — `#/taste` does **not** show the "no passport yet" empty state; it shows the trouble view, h1 **"Something is stored here, and it cannot be read."** |
| preserves context | **holds** — *"The data saved under `pigment.taste.v1` on this device is not readable as a Taste Passport. Pigment has not changed it and will not write over it."* The stored bytes are **preserved exactly**, verified after every action below. **The corrupt read does not wipe the Passport.** |
| retry | **"Try reading it again"** — clicked; re-reads, data still corrupt, returns the same honest view, **bytes still preserved** |
| recovery / export | **"Download the stored data"** — clicked; the intercepted download carries **the raw stored bytes verbatim**, named `pigment-passport-unreadable.json` (not `null`, not an empty object) |
| user-controlled replacement | **"Replace it with a new Passport"** — clicked; `confirm()` reads *"Replace the unreadable data on this device with a new, empty Taste Passport? Download it first if you want a copy — this cannot be undone."*; on accept the key is removed and `#/taste` returns to "No map yet — let's sketch one." |
| **no silent overwrite** | **holds** — with the corrupt bytes present and **no storage break at all**, clicking Admire elsewhere refuses to write: `aria-pressed="false"`, the write-failure notice appears, and the corrupt bytes are still preserved. The build will not destroy data it could not read. |

### S3 — `localStorage.getItem` throws (private browsing / site data blocked)

`#/taste` renders the *other* branch of the trouble view — h1 **"This browser will not let Pigment
read its storage."**, lede *"Local storage is blocked for this site … **Nothing has been
deleted.** Admire, Seen in person and Saved for later will not stick in the meantime."* — with
"Try reading it again" and "Back to the atlas". The build distinguishes **denied** from
**corrupt** from **genuinely absent** and says which one it is. Admire under a denied read
likewise refuses and raises the notice.

### S4 — is the app still usable?

Nine routes exercised while reads were denied: `#/` (6 851 chars), `#/artists` ("All 256
painters", 40 713), `#/museums` (12 417), `#/museum/louvre`, `#/explore`, `#/timeline`, `#/daily`
("The Night Watch"), `#/lists`, `#/credits` (16 170). **Every route rendered its full content.**
Storage failure degrades only the Passport, never the atlas.

**AC8 is now supported.** Van Eyck's F-4 was a gap in the probe, not in the build — I say that
plainly because I am the one who had to click the affordances to find out.

---

# 4 — N-1 · SCREENSHOT PACK RE-CAPTURED AT HEAD · **DONE**

All 64 shots (16 routes × {1440×900 desktop, 390×844 mobile} × {dark, light}) re-captured at
`64d68a0` and **overwritten in place**, keeping the `desktop`/`mobile` and `dark`/`light`
literals. `git status` shows them as modified, not added.

`harness/cdp-r2/run_a.py` asserts at shutter time, per shot: `innerWidth == cw == the nominal
width`; `#app` padding `16px`/`22px` at 390 and `28px`/`34px` at 1440; `.main-nav` `order:3` +
`overflow-x:auto` at 390 and `order:0` + `overflow-x:visible` at 1440; all 8 nav links present and
the nav box visible; the theme actually applied. **TOTAL 64 · FAILED ASSERTIONS 0**
(`capture-assertions.json`, regenerated).

The two surfaces N-1 named are now correct in the pack — I checked by eye, not by timestamp:

| shot | at `a4898d3` (the committed pack Van Eyck read) | at `64d68a0` (now on disk) |
| --- | --- | --- |
| `home__mobile-390x844__dark.png` | nav as **8 stacked rows**, 362 px header | **one horizontally scrolling row**, 154 px header, 4 of 8 destinations visible with the fade affordance |
| `home__desktop-1440x900__dark.png` | title over **unveiled** saturated cover shapes (the 1.10:1 state) | heavily veiled cover, title clearly separated |

---

# 5 — INDEPENDENT VERIFICATION OF UNIT 26

Unit 26 had never been checked by anyone but Dürer — the same arrangement that let round 1's
500 px capture defect survive two rounds. I re-measured his four headline claims myself at HEAD.
Raw results: `harness/durer-u26/hero-vermeer-closing-1440.json`, `hero-vermeer-closing-390.json`,
`nav-vermeer-closing.json`, `harness/vermeer-closing/gold-sites.json`.

## 5.1 The dark and light home hero — **confirmed, and dark is better than he reported**

Same glyph-pixel method, my own run: 6 fresh covers per theme at 1440×900 and 4 more at 390×844,
plus the forced worst-case opaque cover (white in dark, black in light).

| theme | element | floor | Dürer (10 covers) | **my worst observed** | Dürer bound | **my bound** | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dark | `h1.home-title` | 3.0 | 4.84 | **5.14** (1440) · **5.29** (390) | 4.62 | **4.62** | **PASS** |
| dark | `div.kicker` | 4.5 | 7.11 | **8.15** | 6.80 | **6.80** | **PASS** |
| dark | `p.lede` | 4.5 | 7.53 | **7.89** | 7.20 | **7.20** | **PASS** |
| dark | `p.footer-note` (cover credit) | 4.5 | 8.38 | **8.35** | 7.20 | **7.20** | **PASS** |
| dark | `a` (painter link in the credit) | 4.5 | 7.91 | **7.88** | 6.80 | **6.80** | **PASS** |
| light | `h1.home-title` | 3.0 | 3.67 | **3.75** (1440) · **3.46** (390) | 3.42 | **3.42** | **PASS** |
| light | `div.kicker` | 4.5 | 9.87 | **10.34** | 9.18 | **9.18** | **PASS** |
| light | `p.lede` | 4.5 | 6.66 | **7.34** | 6.66 | **6.66** | **PASS** |
| light | `p.footer-note` | 4.5 | 7.17 | **7.16** | 6.66 | **6.66** | **PASS** |
| light | `a` | 4.5 | 7.17 | **7.40** | 6.66 | **6.66** | **PASS** |

**Every forced-cover bound reproduces his to the second decimal**, at both 1440×900 and 390×844 —
which is the plateau in the radial veil doing exactly what he claimed. My observed numbers differ
from his only where the random cover draw differs, and where they differ mine are equal or higher
(his 10 covers found a worse draw than my 6, which is the honest reading, not a disagreement).
**Dark ≥ 3.0 and light ≥ 3.0 both confirmed independently.** Unit 26a's V2-1 / V2-2 claims stand.

## 5.2 Mobile header and the nav row at 390 px — **confirmed exactly**

| measure | Dürer | Van Eyck | **mine** |
| --- | --- | --- | --- |
| `.site-header` height at 390×844 | 154 px | 164 px | **154 px** (dark **and** light, identical) |
| `.main-nav` box | 358 × 35 | 358 × 45 | **358 × 35** |
| rows of links | 1 | 1 | **1** |
| computed `flex-wrap` / `flex-basis` | `nowrap` / `100%` | `nowrap` / `100%` | **`nowrap` / `100%`** |
| `overflow-x` | `auto` | — | **`auto`** |
| nav `scrollWidth` / `clientWidth` | 689 / 358 | — | **689 / 358** (scrollable, all 8 links reachable) |
| links inside the box | 4 of 8 | — | **4 of 8**, with the `linear-gradient(90deg,#000 78%,transparent)` fade affordance |
| root `scrollWidth` / `clientWidth` | 390 / 390 | 390 / 390 | **390 / 390 — 0 overflow** |

**I measure 154 px, matching Dürer, not Van Eyck's 164 px** — the difference is his environment,
and it is immaterial to every criterion either way. The nav is back to one scrolling row.

## 5.3 200 % text zoom — **confirmed, 0 overflow**

Root font-size forced to `32px !important` (200 % of 16), applied twice with a repaint between so
the layout has actually settled, across the frozen 26-route list, at two widths:

| width | routes | **overflowing** |
| --- | --- | --- |
| 1280 × 800 | 26 | **0** |
| 1270 × 800 | 26 | **0** |

`documentElement.fontSize` verified as `32px` at shutter time on every route. AC18's zoom clause
holds at HEAD.

## 5.4 The six re-pointed gold-as-small-text sites — **all six compute `--gold2`, all pass**

Tokens confirmed live: dark `--gold #c9a45c` / `--gold2 #e8c98a`; light `--gold #9e7938` /
`--gold2 #81632b`.

| site (`styles.css`) | route | computed | px | dark | light | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `.branch-chip::before` (:984) | `#/movements` | **`--gold2`** | 11.2 | 11.53 | 5.18 | **PASS** |
| `.tl2-leg-more` (:1016) | `#/timeline` | **`--gold2`** | 12.2 | 12.25 | 4.75 | **PASS** |
| `.tl2-year.now` (:1031) | `#/timeline` | **`--gold2`** | 11.2 | 11.53 | 5.18 | **PASS** |
| `.list-card .lc-kicker` (:1178) | `#/lists` | **`--gold2`** | 10.2 | 11.53 | 5.18 | **PASS** |
| `.le-num` (:1189) | `#/list/{id}` | **`--gold2`** | 19.2 | 12.25 | 4.75 | **PASS** |
| `.pc-kind` (:1277) | `#/taste` (seeded passport) | **`--gold2`** | 9.9 | 11.53 | 5.18 | **PASS** |

**12 measurements, 0 failures, 0 sites still computing `--gold`.** `.list-card .lc-kicker` also
paints over Wikimedia thumbnails on `#/lists`; measured there on real glyph pixels it is
**11.53 dark** against a `[22,20,15]` backdrop — the card body is opaque, so that surface is not
part of the AC19 failure. Light's margins are thin (4.75 against 4.5) but they are margins.
Unit 26c's V2-2/V2-3 claim stands.

## 5.5 What unit 26 did **not** reach

Unit 26 is sound on everything it claimed. It is also the reason §1 exists: unit 26's own log says
*"Not claimed: text over `upload.wikimedia.org` artwork photographs is still unmeasured."* That
was accurate, and the class it names is the one that fails.

---

# 6 — FINDINGS

> **Repair note, 2026-07-28 (Van Eyck N-4).** This section shipped as a bare
> `<!--PLACEHOLDER-FINDINGS-->` marker. It is rendered here from this pass's own body and raw
> data. Each entry states which section of this document it rests on; nothing is added that this
> pass did not observe. Dispositions at HEAD `a686d98` are marked **[status 2026-07-28]** and are
> clearly separated from what was true on 2026-07-26.

## F-V1 · MAJOR · criterion-failing · AC19 — text over Wikimedia photographs in the museum band

**Observed** (§1.2, raw `harness/vermeer-closing/photo-all-{dark,light}.json`): on museum venue
pages the breadcrumb row, `h1.display`, `.mu-sub` and (light only) `.mu-hook` paint directly over
a `upload.wikimedia.org` photograph under a single scrim, `.mu-shade`, whose alpha ramps as a
percentage of `.mu-hero`'s height while the text block `.mu-hero-body` is bottom-anchored. The
same element therefore lands at a different alpha on every venue.

| theme | worst class | worst measured | floor | venues below floor |
| --- | --- | --- | --- | --- |
| dark | breadcrumb, current page (`--muted`) | **1.01** | 4.5 | 97 of 102 |
| dark | `h1.display` (`--ink`) | **2.48** | 3.0 | 1 of 104 |
| light (clean venues, §1.2a) | breadcrumb, current page (`--muted`) | **1.24** | 4.5 | 87 of 88 |
| light (clean venues, §1.2a) | `h1.display` (`--ink`) | **2.88** | 3.0 | 1 of 88 |

**Confirmed by eye, not only by script** (§1.3): `ac19-museum-met__desktop-1440x900__dark.png`,
`ac19-museum-k20__desktop-1440x900__{dark,light}.png`,
`ac19-museum-frida-kahlo__desktop-1440x900__light.png`.

**Root cause** measured, not guessed (§1.4). **Remedy** computed as a bound, not a sample (§1.5):
move the scrim onto `.mu-hero-body` at alpha ≥ `.88`, which clears the worst required alpha
(`.864` dark, `.834` light) against a worst-case fully opaque photograph pixel.

**Scope limit stated at the time:** measured at **1440×900 only**; the mobile `.mu-hero` is
shorter, so the mobile numbers were neither inherited nor assumed (NOT TESTED #4).

**[status 2026-07-28] CLOSED by unit 27** (`563f0af`), which implemented exactly the remedy above
as `--mu-veil:.88` on `.mu-hero-body`, and measured it at both viewports. Independently
re-measured at HEAD in `browser-evidence-final.md` §3.

## F-V2 · MAJOR · AC19 — small text below the band fails on the same pages *(rendered at repair time)*

**This entry did not exist in the 2026-07-26 draft.** It is stated here because the raw data of
this pass contains it and a reader of §1.2 will see it. Below the museum hero, on the same 104
pages, the sweep measured 548 further text elements and found classes below floor in both themes:
`span.count` **4.44** dark (1 of 45 venues) and, on clean light venues, `span.count` **3.38**,
`p.img-credit.mu-credit` **4.34**, `a` **4.34**.

At the time these were read as part of the photograph over-approximation. They are not: their
real backdrop is the site-wide generative `#bg-canvas`, which is why the numbers move from venue
to venue with no photograph involved. **Dürer found this independently** — unit 28's log records
that unit 27's detector flagged `span.count` and `p.img-credit`, and that an A/B with `#bg-canvas`
removed proved the surface. It became **F-27-2** (unit 28) and then **F-7** (unit 29).

**[status 2026-07-28] CLOSED by units 28 and 29** (`3e24e4a`, `4362c8a`). Independently
re-measured at HEAD in `browser-evidence-final.md` §4.

## F-V3 · MINOR · instrument, not build — the light sweep of §1.2 is partly contaminated

Found while rendering this document, not on 2026-07-26. 16 of 104 light venues carry shot-A/shot-B
divergence signatures (33 rows at a ratio of exactly 1.00; 11 rows whose glyph-pixel counts exceed
any possible glyph area). Full statement and the clean re-reading: **§1.2a**. It exaggerates F-V1
without creating it, and the dark run — the one with cross-operator agreement — is unaffected.

## Dispositions of findings this pass was sent to settle

| finding | owner | this pass's evidence | disposition |
| --- | --- | --- | --- |
| **F-3** — AC4 unsupported, the frozen journey matrix had never been run | Van Eyck | §2 — 33 steps, 0 FAIL, all five journeys plus AC4's own eleven-link chain, real CDP mouse and key events | **CLOSED.** AC4 supported |
| **F-4** — AC8: "no user-visible retry / recovery / export affordance" | Van Eyck | §3 — S1–S4; every affordance clicked, notice copy quoted, bytes verified preserved | **CLOSED — false negative, not a build defect.** His probe had no passport to fail against |
| **N-1** — the screenshot pack depicted a superseded build | Van Eyck | §4 — 64 shots re-captured at `64d68a0`, 0 failed assertions, both named surfaces verified by eye | **CLOSED at `64d68a0`.** **[status 2026-07-28] re-opened by units 27–29 and closed again** — see `browser-evidence-final.md` §2 |
| **Unit 26 unverified by anyone but its implementer** | Van Eyck | §5 — hero bounds reproduced to the second decimal at both viewports, nav 154 px / 358×35 / 1 row / 0 overflow, 26 routes at 200 % zoom with 0 overflow, all six gold sites computing `--gold2` | **CLOSED.** Unit 26a/26c claims stand |

## Notes (not findings)

- **N-V1 · the frozen UX table is stale on `#/explore`, in the build's favour.** §2:
  `ux-requirements.md` §5 describes two instruments and flags "promise ≠ destination inventory —
  CONFIRMED in code". At HEAD `#/explore` offers **four**, which is what the home card promises.
  The asymmetry AC22 was about has been closed; the frozen table has not been updated to say so.
  Recorded, not scored as a failure.
- **Method correction, disclosed rather than buried (§1.1).** This pass's first shot-B used
  `visibility:hidden`, which deletes an element's own background as well as its glyphs, and
  produced a false 2.38:1 on `#/daily` that was nearly published. Corrected to
  `color:transparent` + `-webkit-text-fill-color:transparent`; the same element then measures
  **14.82** — PASS. Every number in this document comes from the corrected instrument, and the
  full sweep was re-run to confirm the museum findings are method-independent.
- **Method correction, AC8 (§3).** One step was measuring the harness rather than the build (an
  overridden `HTMLAnchorElement.prototype.click` also disabled the link under test). Re-run
  cleanly with a real mouse click; passes.

---

# 7 — REGRESSION SWEEP AT HEAD (console / network / images)

Re-run at `64d68a0` so the regression evidence matches the shipped code, not `a018fe2`
(`harness/cdp-r2/run_eg.py`; all 26 frozen routes walked inside one document, as a real user
moves through the SPA, so observers and the Resource Timing buffer survive).

| measure | result |
| --- | --- |
| routes walked | **26 / 26** reached |
| console **errors** (`console.error`, `onerror`, `unhandledrejection`) | **0** |
| console **warnings** | **0** |
| CDP-level `Log.entryAdded` / `Runtime.exceptionThrown` at error or warning severity | **0** |
| network requests with status ≥ 400 | **0** of 112 |
| third-party hosts | **`upload.wikimedia.org` only** (74 requests) — plus `localhost:8421` (38). **0** to `fonts.googleapis.com` / `fonts.gstatic.com` |
| images checked across the 26 routes | **680** · **broken: 0** |
| route orientation (AC15 spot-check) | live regions in the document: **0**; live mutations across 5 route changes: **0**; `document.activeElement` after each = the route's `h1[tabindex="-1"]` ("Museums", "The grand timeline", "Find your palette.", "Credits", "Blank canvas") |
| image credit lines | `#/museum/louvre` → *"Photograph: Benh LIEU SONG (Flickr) · CC BY-SA 3.0 · file on Commons"*; `#/artwork/david` → *"Image credit: Jörg Bittner Unna · CC BY 3.0 · file on Commons"*; no raw-markup leakage |

**No regression found at HEAD.** This reproduces round 2's sweep on the shipped code, and is
consistent with AC25's disclosure position (OD-3): fonts are self-hosted, and
`upload.wikimedia.org` is the only third-party host, disclosed on `#/privacy`.

---

# 8 — NOT TESTED

Explicit, and not inferred from anything.

1. **Real assistive-technology output.** No VoiceOver, NVDA or JAWS session was run. I measured
   the accessibility tree (roles, names, `aria-pressed`, live-region count, focus target) — not
   what a screen reader speaks. AC15's objective clauses are verified; the spoken result is not.
2. **Real touch input and device-pixel-ratio ≠ 1.** All input was synthetic mouse and key events
   at `deviceScaleFactor: 1`. No pinch-zoom, no Retina rendering, no on-screen keyboard.
3. **Browsers other than Chrome.** Chrome headless only. No Safari, Firefox, or any WebKit/Gecko
   engine — `-webkit-mask-image` on `.main-nav` and `backdrop-filter` are the two places where
   that gap could matter.
4. **The AC19 composite class at 390 px.** All 104 venue pages were measured at **1440×900 only**.
   The mobile `.mu-hero` is shorter (`min-height:250px`, `padding:22px 18px 16px`), so the text
   block sits at a *different* fraction of the hero and therefore under a *different* scrim alpha.
   The mechanism that fails at 1440 is height-dependent, so the mobile numbers are neither
   inherited nor assumed. **Whoever fixes F-V1 must measure 390 px as part of the fix.**
5. **Museum pages other than the 104 reachable from `#/museums`.** 116 venues exist; 12 are
   sentinels or carry no catalogued work and render no page. Not measured because not reachable.
6. **`#/artwork/*`, `#/artist/*` and `#/` composites.** Measured and found to contain **no** text
   painting over a Wikimedia photograph (artwork heroes place the title *below* the image;
   artist heroes paint over a generated canvas, not a photograph; `#/` has 519 images and 0
   overlapping text elements). This is a measured negative, not an untested area — but it is
   scoped to the routes I sampled (`#/`, `#/artists`, `#/artwork/the-starry-night`,
   `#/artist/vincent-van-gogh`, `#/taste`, `#/explore`, `#/lists`, `#/museums`, `#/daily`,
   `#/list/{id}`), not to every artwork or artist in the corpus.
7. **The 821–1100 px overflow band (Van Eyck F-1).** Not re-measured by me; outside my brief and
   outside AC18's frozen viewport set. It remains open as recorded.
8. **The masked focus indicator on the last nav link (Van Eyck F-2).** Not re-measured by me. I
   confirmed the mask is still present (`linear-gradient(90deg, rgb(0,0,0) 78%, rgba(0,0,0,0))`)
   and that the nav scrolls with all 8 links reachable, but I did not re-derive his alpha figures.
9. **Concurrent multi-tab storage conflicts.** AC8 was exercised in a single tab. Two tabs writing
   the Passport simultaneously was not tested.
10. **Onboarding interruption checkpoints (AC7).** Not re-run; carried by round 1's 5/5 and
    wave-c U18. I exercised the onboarding straight through, not interrupted.
11. **Deployed identity.** Everything was measured against a local `http.server` at `64d68a0`. No
    GitHub Pages URL was fetched; nothing here proves what a deployed build serves.

---

# 9 — DOES THE EVIDENCE NOW SUPPORT CERTIFICATION?

> **Repair note, 2026-07-28 (Van Eyck N-4).** This section shipped as a bare
> `<!--PLACEHOLDER-VERDICT-->` marker. It is rendered here from this pass's own body and from the
> commit that carried it (`73ddc27`, "AC4 PASS, AC8 PASS, AC19 FAIL (F-V1)"). It states the
> position **as of 2026-07-26 at `64d68a0`**. It is history. The current position is in
> `browser-evidence-final.md`.

**Not yet — by exactly one criterion.**

| what I was sent to settle | answer on 2026-07-26 |
| --- | --- |
| **AC4** — frozen first-user journey matrix, no broken or unexplained transition | **Yes.** §2: 33 steps, 0 FAIL, five frozen journeys plus the eleven-link chain, walked with real mouse and key events. Van Eyck's F-3 closes |
| **AC8** — storage-failure recovery does not claim success, preserves context, tells the truth, offers a way out | **Yes.** §3: S1–S4; every affordance clicked, every byte checked. Van Eyck's F-4 was a gap in the probe, not in the build |
| **AC19** — text over imagery meets its contrast floor | **No.** §1: F-V1. The museum band fails in both themes across essentially the whole venue set, and I confirmed it by eye as well as by measurement |
| **N-1** — the screenshot pack matches the build | **Yes at `64d68a0`.** §4: 64 shots, 0 failed assertions |
| **Unit 26 verified by someone other than its implementer** | **Yes.** §5: bounds reproduced to the second decimal; where our numbers differ, mine are equal or better |

So: of the **three** criteria Van Eyck recorded as UNSUPPORTED, **two are now supported by
evidence that did not exist before this pass, and the third is not unsupported — it is failing.**
Certification could not be granted, and the honest statement of why is one sentence:
*the atlas puts small text over public-domain photographs under a scrim that was never sized for
the text it carries.* That is one CSS rule wide (§1.5), it is fixable as a **bound** rather than a
sample, and I said so with the number the fix needs — `.88`.

What I would not have accepted at that moment: any claim that AC19 passes at 390 px. This pass
measured 1440×900 only, and the failing mechanism is height-dependent, so the mobile band was
**NOT TESTED**, not inherited (§8 #4).

---

### [status 2026-07-28] What happened next

| | |
| --- | --- |
| **Unit 27** (`563f0af`) | Implemented §1.5's remedy as `--mu-veil:.88` on `.mu-hero-body`, at **both** viewports. F-V1 closed |
| **Units 28–29** (`3e24e4a`, `4362c8a`) | Closed F-V2/F-27-2/F-7 — the `#bg-canvas` class this pass's data contained but did not name |
| **This document's placeholders** | Repaired, from raw data, on 2026-07-28 (§1.2 note, §6 note, this note). Van Eyck's N-4 closes |
| **The screenshot pack** | Re-captured again at HEAD `a686d98`, because units 27–29 landed after `64d68a0` |
| **Independent re-measurement of units 27–29** | `browser-evidence-final.md` §3–§4 — my instrument, not their implementer's assertion |

**The verdict above is superseded, not amended.** Nothing in §1 has been rewritten to hide that
AC19 failed on 2026-07-26; it did, and this pass is the reason it was found.
