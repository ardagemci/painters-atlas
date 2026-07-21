# DATA INTEGRITY REPORT — PIG-001

**Prepared by:** Seurat (`claude-data-steward`) · Round 1 · workflow_state: `challenge`
**Date:** 2026-07-21 · Commit `3c2e9fa` (per intake-baseline.md §2)
**Scope:** Narrow brief — five questions on the provenance/rights container, its
cost, the rights verdict, taxonomy semantics, and deck-pool fix cost. Gate 1 in
force: **no edits to `js/` or `tools/` this round.** Only this report was written.

---

## VALIDATOR

Cited, not re-run (intake-baseline.md §3, `osascript -l JavaScript tools/validate.jxa.js`):

```
artists 246 · movements 74 · techniques 39 · eras 8 · nations 37 ·
painter styles 27 · influence edges 225 · venues 115 ·
catalog 315 (tier1 73) · daily pool 73 · museum notes 103 · personas 15 ·
lists 12 (featured 4) · tier1 artists 36 (arcs 36)
WARNINGS: deck pool <2 works with E<=-40 · deck pool empty F×D quadrant 1,-1
ALL REFERENCES VALID
```

Referential integrity is clean today. The only open validator items are the two
deck-pool **warnings** (not errors) — addressed in Q5. My own record-level counts
below reconcile exactly to the validator: 315 catalog = 255 `pd` + 60 `copyright`;
73 tier1 = 73 daily-pool = the full `pd` tier-1 set.

## IDS

None added or changed (analysis round). Confirmed stable-ID discipline holds:
`coordsSource:"override"` (catalog-1.js:17) is an existing per-field provenance
marker — adding fields is idiomatic to this schema and legal under §4.4 (adding ≠
renaming); it is not exercised this round.

## IMAGES (rights surface, measured)

| Store | Records | Rendered as `<img>`? | Rights metadata present |
| --- | --- | --- | --- |
| `js/catalog-*.js` `status:"pd"` | **255** | Yes, gated on `status==="pd"` (app.js:1357/1360) | none (`src`, `page`, `status` only; `page` → Wikipedia article) |
| `js/catalog-*.js` `status:"copyright"` | **60** | **No** — falls back to generative canvas cover | n/a (suppressed) |
| `js/artworks.js` gallery | **528** works / 175 artists | **Yes, UNCONDITIONALLY — no status field, no gate** (app.js:1669/1681) | none (`img`, `page` only) |

Exact-match / PD basis: the `status:"pd"` flag is an **unsubstantiated assertion**
— it carries no Commons file page, license, author, or death-year. `page` points
at an English Wikipedia article, not the Commons `File:` page, for the whole
catalog and for 289 of 528 gallery works (239 gallery works already carry a
Commons `File:` URL, so provenance is partially recoverable there for free).

## RISKS (numbered, severity-tagged)

1. **[major] `js/artworks.js` is the largest rendered image surface and is entirely
   ungated and undocumented.** 528 third-party Commons images are shown on artist
   pages with no `status` field and no rights metadata. It is *cleaner* than it
   looks on the death-year rule (Risk 3) but it is the biggest documentation hole.
2. **[major] The fetch/audit pipeline discards the exact provenance it already
   fetches.** `tools/fetch_artworks.py` calls Commons `imageinfo` with
   `iiprop=url|mime` and keeps only `{img, page}`; it never requests
   `extmetadata` (License, LicenseShortName, Artist, DateTimeOriginal) that the
   same API returns. `tools/audit_artworks.py` likewise captures no license/author.
   The rights evidence the register needs was in hand at fetch time and thrown away.
3. **[major → escalate, not alarm] Two stores disagree on the same artists' rights
   posture.** Henri Matisse (d.1954) and Frida Kahlo (d.1954) are flagged
   `status:"copyright"` in the catalog (never rendered) yet appear in
   `js/artworks.js` galleries **rendered without a gate** — Matisse: *The Dance,
   Woman with a Hat, The Red Studio, The Snail*; Kahlo: *The Two Fridas,
   Self-Portrait with Thorn Necklace and Hummingbird, The Broken Column*. See Q3.
4. **[minor] `status:"pd"` is an assertion, not evidence** across all 255 rendered
   catalog records (documentation debt; see Q1/Q2).

---

## Q1 — THE CONTAINER RECOMMENDATION

**Verdict: ENDORSE Caravaggio's out-of-band register as the immediate move, with
two AMENDMENTS, and adopt the HYBRID (option c) as the durable target.** This is
the copyright steward's recommendation.

**Why the register first (endorse).** It substantiates an *existing* `status:"pd"`
flag rather than inventing a capability; it needs no build authorization because
`protocol/tasks/PIG-001/evidence/` is not a Gate-1 production path; and it lets the
10-image pilot *price* the work before anyone commits the corpus. All correct.

**Amendment 1 — scope must include `js/artworks.js`.** Caravaggio's finding 13
says "plus `js/artworks.js`," and the numbers make that non-optional: the gallery
is 528 rendered images vs 255 rendered catalog images. A register scoped to catalog
alone would document the smaller third of the rendered surface. Register the
**783 rendered images** (255 `pd` catalog + 528 gallery), tiered by exposure
(Q2). The 60 `copyright` catalog records need only a one-line suppression
confirmation, not a register row.

**Amendment 2 — field set.** Keep Caravaggio's `{commons_file_page, license,
author, death_year, verified_at}` and add **`basis`** (the PD rationale, e.g.
"artist d.≤1955 + Commons PD tag") and **`exact_match`** (does the file depict the
claimed work — my role's required check). Key by artwork id for catalog; by
`artist_id::title` for gallery (the key `tools/audit_artworks.py` already uses).

**Why hybrid, not register-forever (amend option b).** An out-of-band register is
invisible to users and *will* drift from the data — two sources of truth for one
fact. PIGMENT.md §14 is explicit: **"Keep attribution and source links close to the
image record."** A file under `protocol/tasks/…/evidence/` is the opposite of
"close to the record." So the durable home is a minimal in-schema field —
`image.license` + `image.commons` (Commons file page) — folded in during the build
phase once authorized, with the register as the migration source. Crucially, this
is nearly free to populate: since the fetch pipeline already hits the API that
returns `extmetadata` (Risk 2), extending `iiprop` to persist license/author turns
most of the register into pipeline output, not manual labor.

**Reject option (a)-only (schema-first now):** Gate 1 blocks it, and it would
commit the schema before the pilot has priced the audit.

**Honest tradeoffs.** Register-first buys immediate, unblocked progress and a real
cost measurement, at the price of temporary invisibility and a later migration.
The hybrid pays that migration cost deliberately to satisfy §14 and collapse the
two-source-of-truth risk. Net: **register now → pilot → in-schema field in the
build phase.**

## Q2 — THE COST ARITHMETIC

**Measured rights surface (grep + parse, real counts):**

- (i) Catalog `status`: **255 `pd`**, **60 `copyright`**, 0 other = 315 total
  (matches validator). Tier-1 = 73, all `pd` (= the daily pool).
- (ii) `js/artworks.js`: **528 works across 175 artist keys**, each `{img, page}`,
  **no `status` field** — all rendered.
- (iii) Register therefore covers **N = 783 rendered images** (255 + 528), **not
  ~786.** Note the reframe: Duchamp's 786 was `246 artists + 315 catalog + 225
  edges` — mostly uncited *prose and graph edges*, which are accuracy risks, not
  image liability, and it *excluded* the 528 gallery images. The real image-rights
  surface is a different 783: the actually-rendered third-party files.

**Time ESTIMATE (reasoning shown; not measured — pilot settles it):**

- Per record, fully manual (open Commons file page → confirm license tag, author,
  death year → confirm exact-work match → stamp `verified_at`): **~5 min** careful,
  faster batched.
- **Caravaggio's 10-image pilot** (10 Tier-1 works): **~1–1.5 h.** This is the
  decisive bounded test and should gate everything after it.
- **Full Tier-1 (73, highest exposure — the deck + full artwork pages):
  ~6–10 h manual**, or **~1–2 h** if `fetch_artworks.py` is extended to persist
  `extmetadata` (a `tools/` change → build auth) since 239 gallery works already
  hold the Commons file page.
- **Full 783-image surface: ~65–100 h fully manual**, but **~80–90% automatable**
  by re-running the fetch pipeline with `extmetadata` on the Commons-sourced subset.
  Automation is the whole cost lever.

**Vs. Workstream I as written** (§6 items 5–6: aggregate coverage over the *full
corpus* incl. 246 prose bios + 225 influence edges + a fact/legend/dispute UI):
that is corpus classification against **fields that do not exist**, plus new UI —
unbounded in *scope*, not merely hours, and blocked behind a schema design and the
release-positioning decision. The rights-only register discharges the *legal* duty
(images) for a bounded, priceable cost; the aggregate/prose/edge sourcing
(criteria 9, 10) and the uncertainty UI (item 6) are a **separate later task**, as
the liaison's CRITICAL 2/3 and Caravaggio's finding 11 both conclude.

## Q3 — THE RIGHTS VERDICT

**Plainly: I found NO actual rights exposure under the project's own rule
(artist died ≤ 1955). What exists is documentation insufficiency, plus one
store-inconsistency that I escalate rather than resolve.**

- (i) **Tooling.** `fetch_artworks.py` hard-codes `CUTOFF = 1955` and only resolves
  works of painters who died ≤1955 — the PD rule is enforced *at generation time*,
  which is why the gallery has zero post-1955 artists. But it persists only
  `{img, page}`; the license/author `extmetadata` it could request is discarded
  (Risk 2). `audit_artworks.py` validates that the image depicts the actual work
  (blacklist of room/building terms; `PINNED`/`OVERRIDES` for hand-curated files,
  matching my role's pinning duty) and health-checks URLs — but captures no rights
  fields either. **The pipeline proves depiction, not licence.**
- (ii) **Copyright wall.** Exactly the 7 expected artists carry `status:"copyright"`
  (60 records): Picasso (d.1973), Dalí (1989), Kahlo (1954), Pollock (1956),
  Rothko (1970), Warhol (1987), Matisse (1954). The rendering gate
  (app.js:1357/1360, and the POOL filter at validate.jxa.js:201 requires
  `status==="pd"`) means **none is ever displayed as an image** — all fall to
  generative covers carrying no third-party rights. Confirmed.
- (iii) **PD-rule spot check (done exhaustively, not sampled).** Parsed all 246
  artist death dates and cross-checked every rendered record:
  **0 of 255 `pd` catalog records** has an artist who died >1955;
  **0 of 175 artworks.js gallery artists** died >1955. The highest-exposure
  surfaces — the 73-work daily pool and the Tier-1 set — are clean.
  Kahlo (1954) and Matisse (1954) are flagged `copyright` **despite** satisfying
  the ≤1955 rule: the catalog errs *conservative*, i.e. in the safe direction.

**The one item to escalate (Risk 3), stated with care.** The same two artists,
Matisse and Kahlo, *are* rendered in `js/artworks.js` galleries with no gate, while
their catalog works are copyright-walled. Both died ≤1955, so **neither violates the
project's stated rule** — this is not a rule breach. But the two stores assert
*opposite* rights postures for the same painters, and several of the specific
20th-century works involved (e.g. Matisse *The Snail*, 1953) can carry residual
copyright independent of death year. Per my role, **licensing ambiguity escalates
and is not resolved by assumption.** This is precisely Caravaggio's escalation
trigger ("if the register surfaces an image whose PD status does not hold"). I flag
it; I do not rule on it. It is **latent documentation debt plus a policy question
for the owner**, not a new emergency — the build has shipped for weeks and the
death-year rule holds everywhere.

## Q4 — TAXONOMY SEMANTICS (document, do not change)

Answering THEORY_001 §9.3 point by point:

- (i) **Era is century-oriented grouping — confirmed.** The 8 era ids are:
  `14th-century, 15th-century, 16th-century, 17th-century, 18th-century,
  19th-century, 20th-century, 21st-century`. Artist records carry `eras:[…]` as an
  **array** (e.g. Leonardo `["15th-century","16th-century"]`). **Document:** do not
  rename (§9.3), and note eras *are* multi-valued.
- (ii) **Nation is a SINGLE string, not multiple.** Artist records use
  `nation:"italy"` — one scalar. The data model **does not support multiple national
  affiliations.** So §9.3's "preserve multiple affiliations where the data model
  supports them" resolves to: **supported for eras and movements (arrays), NOT
  supported for nation.** Multi-national painters (El Greco, Picasso, van Gogh) can
  structurally hold only one nation; §9.3's cautions about migration, diaspora,
  Indigenous/contested identity can currently be honored only in prose
  (`life`/`career`/`facts`), never in the taxonomy. **Document this limit**; making
  nation multi-valued is a schema *addition* (legal under §4.4, needs build auth) —
  not a rename — if the team ever wants it.
- (iii) **Movements are a parent/child branch structure, framed nowhere.**
  `taxonomy.js` header says only "Movements & techniques may have a `parent` id →
  branches and sub-branches" (113 `parent:` refs). Periods overlap across the
  relation — e.g. `school-of-london` (c.1945–1990) is nested under `expressionism`
  (c.1905–1935), and `american-realism` (1900–1960) under `realism` (1840–1880) —
  so the `parent` link is plainly **genealogical/pedagogical, not strict temporal
  or exclusive containment.** §9.3 explicitly requires this be *stated*. **Document:**
  declare the movement hierarchy a pedagogical/mixed-interpretation approximation.

**Output:** nothing to change this round — three documentation items (era =
century + multi-valued; nation single-valued and its consequence for §9.3; movement
parent = pedagogical approximation).

## Q5 — DECK-POOL FIX COST (content-selection estimate only)

Rule source: `validate.jxa.js:209-214` over the Tier-1 `pd` POOL (73 works);
`ADMIRE_SPEC.md:99` states the axis-coverage rule. Both warnings clear with
**re-scoring of existing works — no new records strictly required** — because
qualifying-adjacent works already sit in the pool:

- **`<2 works with E≤−40`** (classical pole under-probed). Currently **one** work
  qualifies: Rublev *The Trinity* (E=−40). Nearest others already in the pool:
  Vermeer *Girl with a Pearl Earring* (E=−35), Rembrandt *Prodigal Son* (E=−35),
  Vermeer *View of Delft* (E=−30), Raphael *Sistine Madonna* (E=−30). **Cost: one
  work.** Either an honest 5-point re-score of a Vermeer/Rembrandt already at −35
  (both are maximally traditional, low-experimentation — defensible), or author one
  new classical-academic Tier-1 `pd` record (Ingres/David/Bouguereau territory).
- **empty F×D quadrant `1,-1`** = need F≥+25 **and** D≤−25 (abstract + calm).
  Currently **zero** qualify, but three abstractions already in the pool miss only
  on D: Malevich *Black Square* (F=100, **D=−20**), Kandinsky *Composition VIII*
  (F=90, D=−20), af Klint *The Ten Largest No.7* (F=80, D=−15). **Cost: one work.**
  A 5-point D re-score of *Black Square* (−20→−25) is entirely honest — it is the
  austere/calm pole of abstraction — and clears the quadrant.

**Candidates exist among current catalog works** for both poles (Malevich/Kandinsky/
af Klint for abstract-calm; Vermeer/Rembrandt/Rublev for E≤−40); new authored
records are optional, not required. **Total content cost: ~2 works re-scored**
(a few hours of editorial judgment), or 1–2 new Tier-1 `pd` records if the team
prefers not to touch shipped coords.

**Steward's caveats (not blockers):** (a) re-scoring `coords` is a `js/catalog-*.js`
data edit — **Gate 1 forbids it this round**; this is a costed recommendation, not
an action. (b) Re-score only where the new value is defensible on the artwork's
merits, never to satisfy the validator — the gaps reflect genuine content thinness
at the calm-abstract and classical poles (Caravaggio finding 26: the fix is
content, and every shipped deck currently ships 3 of 4 quadrant anchors, pulling
calm-abstract and strongly-classical users toward the centroid).

---

### Summary line for the Synthesis Lead

- **Q1:** Endorse the out-of-band rights register now (no Gate-1 auth), amend its
  scope to include `js/artworks.js` and add `basis`/`exact_match` fields, and adopt
  a **hybrid** — migrate to in-schema `image.license`/`image.commons` in the build
  phase (PIGMENT §14 wants attribution *close to the record*; the fetch pipeline can
  populate it near-free).
- **Q2:** Rendered rights surface = **783 images** (255 `pd` catalog + 528 gallery),
  not ~786; 60 `copyright` records are never rendered. Pilot ~1–1.5 h; Tier-1 (73)
  ~6–10 h manual / ~1–2 h automated; full surface ~65–100 h but ~80–90% automatable.
- **Q3:** **No actual exposure** under the died-≤1955 rule — 0/255 `pd` catalog and
  0/175 gallery artists died >1955; copyright works never rendered. Findings are
  documentation debt, **plus one escalation:** Matisse & Kahlo (both d.1954) are
  copyright-walled in catalog yet rendered in galleries — a store inconsistency and
  licensing-ambiguity question I escalate rather than resolve.
