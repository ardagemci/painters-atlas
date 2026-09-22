# Rights action plan — all five standing questions, one place

**Written for the owner. Not legal advice. No determination is made here.**
Covers every standing question in `.claude/agents/claude-rights-analyst.md`
("Standing questions you own"), each checked against current, real data —
not carried forward from when the questions were first written
(2026-08-24–27). Produced partly via Lane IV (`protocol/duo-sessions/`),
partly by direct verification. OD-5 applies throughout: asserted basis and
residual uncertainty, no clearance claims, no option ranked where the choice
is genuinely the owner's.

**How to read this.** Three of the five needed real research and got it.
One needed one fact from you and still does. One turned out to already be
fine. They're ordered below by what unblocks the most other work first, not
by number.

---

## 1. Jurisdiction — start here, it's free

**Status: unchanged, still blocking, still the cheapest move available.**
Hogarth's original framing stands: *"D cannot be chosen the way A, B and C
can, because its option set omits the input that makes any of them
commissionable — the owner's country and operating form."* Nothing in this
round's research changes that — if anything, the pd-token brief's finding
that Germany's and the US's rules genuinely diverge (§68 UrhG vs. *Bridgeman*)
makes the answer matter more, not less, since which one applies to you
depends on facts only you have.

**What's needed, precisely:** the country (or countries) whose law governs
your exposure as the site's operator, and your operating form (individual,
company, where incorporated if applicable). The site's host (GitHub Pages,
US-based infrastructure) and a reader's country are separate questions from
this one — Hogarth's brief already flagged that the answer can differ for
all three, and this plan doesn't resolve that, only names it clearly enough
to act on.

**Action:** one sentence from you. Nothing else in this plan is blocked on
research; several items below are blocked on this.

---

## 2. The pd-token question — done, refreshed, five records open

**Status: resolved as far as research can take it. Awaiting your decision
among named options.**

Full brief: `docs/RIGHTS_PD_TOKEN_BRIEF_2026-09-07.md`. Summary: the original
seven-record count is five — two (`the-ten-largest-no-9`, `triumph-of-death`)
were already re-sourced onto genuine PD-Art files since the question was
first written, confirmed by fetching each Commons page directly. The
remaining five (`black-fuji`, `david`, `pieta`, `little-dancer-aged-fourteen`,
`vahine-no-te-tiare`) each carry a living photographer's own CC licence, no
PD-Art tag. All four legal citations in the original brief were verified
against primary sources this round; one (the German position) needed a real
correction, not just a citation — current §68 UrhG narrows the 2018 case
Hogarth cited as Germany's live position.

**Action:** read the brief, choose among B (new schema token) / C (move to
copyright status) / D1+D2 (re-source where possible, document uncertainty
where not) — per record or as a standing policy.

---

## 3. In-copyright artists — real numbers, real licensing routes, connects to an open RIGHTS-001 decision

**Status: the count changed (68 → 61) and the standing question turns out to
overlap with RIGHTS-001's own "Decision C," which already has four framed
options awaiting your choice — this section adds what neither had: who you'd
actually license from, if you chose to.**

**The current count, verified against the live data:** 61 records,
`image:{status:"copyright"}`, across exactly **15 artists** — not 68. Six
artists account for 51 of the 61 (84%): Picasso (10), Kahlo (9), Warhol (8),
Pollock (8), Rothko (8), Dalí (8). The other nine — Alma Thomas, Ben Enwonwu,
Franz Kline, Hans Hofmann, Henri Matisse (2), Kenneth Noland, Philip Guston,
Robert Motherwell, Tarsila do Amaral — carry one or two records each.

**This is not a new question — it's a fifth of RIGHTS-001's already-framed
"Decision C" (the 61 procedural covers), options C1–C4:**

- **C1** — retain the current artist-associated generative covers, pending
  review. Free, changes nothing.
- **C2** — replace with artist-neutral placeholders. In OP-INTERFACE's
  scope, ~24 `js/app.js` call sites. Narrows an "is this cover implying
  something about the artist's style" question at the cost of personalization.
- **C3** — metadata-only surfaces (title/artist/date, no generated image).
  Needs the same missing "record-scoped no-image" capability that blocks
  pd-token options A3/B1 — a real, shared, unbuilt dependency across three
  separate decisions in this task.
- **C4** — pause the 61 covers pending qualified review, using C3 as the
  interim state.

**What this section adds — genuinely new research, not previously in
RIGHTS-001:** whether showing the *real* image is ever reachable, for the six
artists that matter most by volume. Verified via web search, cross-checked
independently (I fetched the Pollock-Krasner Foundation's own licensing page
directly and confirmed the claim below myself):

| Artist | Who actually manages licensing today |
|---|---|
| Picasso | Picasso Administration (Succession Picasso); Artists Rights Society (ARS) in the US |
| Kahlo | Banco de México Diego Rivera–Frida Kahlo Museums Trust, via ARS in the US |
| Warhol | Andy Warhol Foundation → ARS (US/rest of world), DACS (UK), ADAGP (France) |
| Pollock | Pollock-Krasner Foundation → ARS, explicitly, for all requests — confirmed directly: *"To request permission... please contact Artists Rights Society (ARS)"* |
| Rothko | Kate Rothko Prizel and Christopher Rothko, via ARS in the US |
| Dalí | Gala-Salvador Dalí Foundation → VEGAP (Spain), via the international collecting-society network |

**What's real and what isn't, honestly:** these are live, functioning
organizations with published licensing channels — this is not a dead end.
DACS (UK) publishes that costs are generally per-artwork-and-per-use, with
blanket annual agreements available for regular users, and has a published
museum digital-collection rate (£10/work/year for 10–100 works, ex. VAT) —
the one concrete public figure either model could find. **No comparable
published tariff exists for a use like Pigment's** (a non-commercial,
editorial art atlas), and nothing found establishes that any of these
organizations would treat that use as routine the way they treat press or
scholarly requests. Whether Pigment would qualify for a favorable rate, what
territory/duration/artist-count a request would need to cover, and whether
the underlying photograph (a second, separate rights question — see the
pd-token brief) would also need clearing are all unresolved.

**Action:** this doesn't collapse into a single decision — it's an input to
Decision C above, and a separate question of whether pursuing licensing for
the six major estates is worth the cost/effort at all versus the current
generative-cover treatment. Both are yours to weigh, not to be weighed here.

---

## 4. The 1955 line — checked, the motivating case has resolved itself

**Status: no live conflict currently exists.** Fernand Léger (died 1955,
the artist named in the original question) was fetched directly: his catalog
record's Commons page asserts PD-Art on **two independent, converging
bases** — life+70 (which, as of today, has already fully run: 1955+70+1 =
2026) and separately, US publication before 1931. There is no disagreement
between Pigment's heuristic and the Commons assertion for this file, and
hasn't been since the calendar caught up.

Checked whether any other near-boundary case exists right now: the catalog
holds four artists who died *after* 1955 (Kupka 1957, Qi Baishi 1957, Pollock
1956, Rivera 1957). None create a live conflict either — their catalog
records correctly carry `status:"copyright"` (counted in §3 above), not a
PD claim resting on the heuristic. The heuristic and the per-record status
system are working together as designed: the heuristic decides who to
*attempt*; each artwork's own Commons assertion still decides its actual
status, independent of the artist's death year.

**Action:** none required today. The underlying policy question — what to
do if a future addition's heuristic and Commons assertion genuinely
disagree — is still worth writing down once, so it doesn't have to be
re-derived under time pressure when a real case eventually shows up. That's
a documentation task, not a decision, and can wait.

---

## 5. What the atlas promises — checked, holding up

**Status: no drift found.** Compared `PIGMENT.md` §14 (image rules) and the
OD-5/OD-1 release-language rule against current behavior: generative covers
are used for copyrighted works and never presented as the real artwork
(§14); public copy is required to avoid clearance language and
completeness claims (OD-1/OD-5), and the banned-phrase guard
(`tests/test_rights_tooling.py::TestProseLanguage`) that enforces this
passes clean right now, across `docs/`, `tools/`, `tests/`, `js/app.js`, and
`protocol/oriented/`. This is a clean result, not a null one — it means the
promises as written still describe what ships, which is worth confirming
rather than assuming.

**Action:** none. Worth re-checking whenever §14 or the release-language
rule is next edited, same as any other guard.

---

## Summary — what actually needs you

| # | Question | Needs from you |
|---|---|---|
| 1 | Jurisdiction | One fact: your country/operating form |
| 2 | pd-token (5 records) | A choice among B / C / D1+D2, per record or as policy |
| 3 | In-copyright artists (61 records, 15 artists) | Whether pursuing licensing is worth it at all, given real costs are still unpublished; independently, a choice among Decision C's C1–C4 |
| 4 | The 1955 line | Nothing now; optionally, a standing policy for the next boundary case |
| 5 | What the atlas promises | Nothing — confirmed current |

## Provenance

Questions 1, 4 and 5 verified directly against live data and the repository's
own guards, 2026-09-07. Question 2 verified via a two-round Lane IV session
(Opus 5 + Astra 6) with every citation fetched from a primary source; see
`docs/RIGHTS_PD_TOKEN_BRIEF_2026-09-07.md`. Question 3's licensing-route
research was produced by Astra 6 via live web search and independently
spot-verified by Opus 5 (the Pollock-Krasner citation was fetched directly,
not taken on trust) before inclusion here.
