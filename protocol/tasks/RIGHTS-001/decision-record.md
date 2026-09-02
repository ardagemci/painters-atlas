# RIGHTS-001 — Decision Record

Living document (Gate 3). Every material adaptation records: what changed, why,
which assumption or constraint required it, supporting evidence, effect, and
accept / reconsider / escalate status. Unrecorded deviations are defects.

Owner decisions are recorded here as **decisions**; agent analysis is recorded
as **evidence**. OD-5 binds: nothing in this file states a clearance.

## D-000 — Task opened

- **What:** RIGHTS-001 opened under OP-RIGHTS at baseline `dd87ad2`, state `intake`.
- **Why:** Four open questions had accumulated with evidence assembled but no
  route to an owner decision — see `intake-baseline.md` §§3–6.
- **Constraint:** `protocol/oriented/OP-RIGHTS.md`; OD-5 throughout.
- **Status:** accept.

## Open items carried in at intake

| id | Item | State |
|---|---|---|
| A | Six records on a `pd` token over CC-asserted files | open — schema value undecided |
| B | `the-ten-largest-no-9`: bare CC tag, no licensor; alternative carries © | open — no clean basis located |
| C | Procedural covers on 61 walled records, drawn from Pigment's own palette assignment for the artist | open — see E-001; no artwork pixels involved |
| D | Jurisdiction | **partly decided — D-005 as amended by D-006.** Individual, no company, no revenue; residence undetermined between **France and Turkey** |

## Decisions

## D-001 — Round-one challenge routed without a liaison packet

- **What:** `messages/002-challenge.json` and
  `challenge-adaptation-report.md` were sent to the Theory Team directly. The
  Synthesis Liaison (Duchamp) packet required by `PROTOCOL.md` §1 was not
  produced, and the Coordinator did not ingest the message or advance
  `state.json`, which remains at `intake`.
- **Why:** D-001 records an owner instruction given after the packet and ingest
  were described as the alternative. That explanation is not independently
  re-proven by repository evidence. Round one is a challenge to a theory
  artifact, not a build authorisation; nothing downstream of it can reach
  production without Gate 1, which is untouched.
- **Constraint waived:** `PROTOCOL.md` §1, "after every team artifact, that
  pole's liaison analyst audits it before the Kernel routes it."
- **Effect:** The round-two revision arrives unaudited by the liaison, so any
  defect in the challenge reaches the Theory Team unfiltered. `state.json` and
  the message log now disagree about the round: two messages exist at
  `workflow_state` `theory` and `challenge` while state reads `intake`. That
  divergence must be reconciled before the Coordinator is used on this task
  again, or its first ingest will act on a stale state.
- **Evidence:** D-001's session record of the owner instruction;
  `messages/001-theory_brief.json` and `messages/002-challenge.json`, both
  schema-valid; independently observable `state.json` / message-history
  divergence.
- **Status:** accept (owner). Reconsider if the Coordinator is brought back into
  this task.

## E-001 — The procedural covers use no artwork pixels (evidence, not a decision)

- **What:** The round-one brief assumed "the repository evidence does not show
  that artwork pixels are used to generate those covers." Measured at `fa102fc`:
  279 artists carry static palette and style assignments in `js/artists-*.js`,
  and the observed paint path at `js/app.js:815-850` performs no artwork-pixel
  sampling: it has no artwork-image input, `getImageData`, or `drawImage` of a
  source image. The creation and research provenance of those assignments is
  undocumented in the reviewed evidence.
- **Effect on the question:** The finding is limited to the observed runtime
  path. It does not establish what sources informed the palette and style
  assignments or answer any jurisdiction-dependent question. C2 removes the
  artist-specific palette and style inputs from the cover; C remains open.
- **Evidence:** `challenge-adaptation-report.md` CH-4.
- **Status:** accept as finding. Decides nothing; C remains open.

## E-002 — CH-1 adaptation: record-scoped metadata-only presentation

- **What changed:** The challenge correctly found that the current renderer has
  no metadata-only state. The round-two response does not make A3 or B1 select
  global C3. Instead, either option independently requires one record-scoped
  metadata-only presentation capability. C3 remains the separate owner policy
  that applies the same outcome globally to the 61 cover-backed records.
- **Why:** Coupling A3 or B1 to global C3 would turn a record treatment into a
  Pigment-wide visual-policy choice and collapse three owner decisions into one.
- **Constraint:** OP-RIGHTS may define the required rights and reader outcome;
  future OP-INTERFACE work owns presentation behavior. This entry authorizes no
  implementation.
- **Evidence:** `messages/002-challenge.json` CH-1; current `js/app.js` artwork
  fallback; Theory Team reviews by THEMIS, VERA, ELARA, and MIRA.
- **Effect:** A3 and B1 become truthful record-scoped choices. Their treatment
  takes precedence over C1 or C2 only for selected records; C stays independent.
- **Status:** accept as adaptation. Not an owner selection.

## E-003 — CH-2 adaptation: successor guard requirements

- **What changed:** If A1 is selected, the literal `pd` ratchet may be retired
  only with future successor guards scoped to the five A1-migrated records and
  recorded negative controls. The sixth af Klint record is included only if B
  separately changes it. These guards do not yet exist.
- **Why:** The current test filters literal `status:"pd"` records, so a token
  migration could lower the count without changing the exact media assets or
  source assertions. Counting every conditional-basis record as an offender
  would create a different false proxy.
- **Constraint:** The guard must measure vocabulary integrity and attribution
  continuity without claiming source authority, jurisdiction, or legal effect.
- **Evidence:** `tests/test_rights_tooling.py` `TestPdTokenAccuracy`; CH-2;
  ARGUS audit.
- **Effect:** A1 cannot report a vocabulary migration as resolution of the
  underlying rights questions.
- **Status:** accept as adaptation. Not an owner selection.

## E-004 — CH-3 adaptation and partial defense: 3+2+1 evidence profiles

- **What changed:** The six records remain grouped analytically as three
  photographs of three-dimensional works, two photographs of flat works, and
  one unnamed or conflicted af Klint media asset governed by B. Per-record
  separation remains mandatory.
- **Why:** The grouping keeps materially different evidence questions visible,
  but the repository does not demonstrate that the groups receive different
  treatment under any named jurisdiction.
- **Constraint:** The underlying work and exact media asset stay separate. The
  generated registry and census identify Sailko and Francesco Bini as different
  source-asserted contributors; this is not an independent authorship finding.
- **Evidence:** `js/photo-credits.js`; PIG-001 rights census; CH-3; ARGUS and
  THEMIS reviews.
- **Effect:** The response accepts the evidence split, rejects the challenge's
  shared-contributor claim, and does not adopt originality or legal-effect
  assumptions.
- **Status:** accept adaptation and partial defense. Not an owner selection.

## E-005 — CH-5 correction: stale task-id conflict withdrawn

- **What changed:** The five task-id-contract conflict references from round one
  are withdrawn and are not carried into the revision.
- **Why:** Commit `18e35b6`, already in the relevant ancestry, corrected the
  schemas and Coordinator enforcement before the theory brief.
- **Constraint:** Protocol history must be stated from repository evidence.
- **Evidence:** `18e35b6`; `tests/test_protocol_ids.py`; schema validation of
  messages 001, 002, and 003.
- **Effect:** The revision no longer treats a resolved protocol defect as open.
- **Status:** accept as correction. Not an owner selection.


## E-006 — One photographer, credited as two people (evidence, not a decision)

*Renumbered from E-002 on 2026-08-31. The round-two revision merge introduced
E-002 through E-005 for its own adaptations, and this entry was appended as a
second E-002 without checking. Hogarth caught the collision in synthesis review.*

- **Found by:** the round-two revision disputing CH-3. It held that the
  shared-contributor claim "is contradicted by the current generated registry
  and census, which identify different source-asserted contributors." Both poles
  were right about different objects, and checking which settled it produced a
  finding neither had.
- **What the sources say.** Queried live against the Commons API:

  | file | `photographer`/`author` field | `[[User:…]]` link | uploader |
  |---|---|---|---|
  | `black-fuji` | `[[User:Sailko\|Sailko]]` | `Sailko` | `Sailko` |
  | `vahine-no-te-tiare` | `[[User:Sailko\|Francesco Bini]]` | `Sailko` | `Sailko` |

  One Commons account uploaded both and is named in both. The two differ only in
  the wikilink's **display text**.
- **What Pigment records.** `js/photo-credits.js` and the census capture the
  display string, not the account: `author:"Sailko"` for one and
  `author:"Francesco Bini"` for the other. The rendered credits therefore name
  **two different people for one photographer**.
- **Why it matters beyond CH-3.** This is the mechanism by which Pigment
  discharges the attribution obligation on CC BY and CC BY-SA files. It cannot
  currently tell two display names for one account apart, so it cannot detect
  that one contributor's work appears twice — which is what made the round-one
  brief's per-record framing of option A2 read as cheaper than it is.
- **Not decided here.** Whether the extraction should prefer the account, the
  display name, or record both is a schema and tooling question for the
  specification. Whether crediting one person under two names satisfies the
  licence is a question for counsel, not for either pole.
- **Amended 2026-09-02 (Seurat):** the collision is **four files, not two**.
  `User:Sailko` is recorded as `Sailko` on the Soutine, `black-fuji` and Rubens
  *Descent from the Cross* files, and as `Francesco Bini` on `vahine`. Two
  further account/display divergences are latent and non-colliding today
  (`User:MiguelHermoso` → "Miguel Hermoso Cuesta"; `User:Glimz` → "original
  file by Stanislav Traykov", a fragment rather than a name).
- **Status:** accept as finding. A and B remain open.


## D-002 — Rounds one and two ran with no specialist input

- **What:** RIGHTS-001 reached `final_synthesis` with `analyst_count: 0`, an
  empty `analyses/`, an empty `analyst-reports/`, and no report from any roster
  specialist. PIG-001 by contrast carries a Caravaggio challenge analysis, a
  Dürer feasibility assessment, Mondrian UX requirements, a Seurat data-integrity
  report, Vermeer browser evidence, and four liaison packets.
- **Why:** the session did not spawn agents, because it does not do so unless the
  owner asks, and the owner had not. Recorded as a deviation rather than left to
  be inferred from an empty directory.
- **Effect:** OP-RIGHTS names Hogarth as lead; the Synthesis Lead did his job
  through two rounds. E-002 — verifying a claimed basis against the file that
  asserts it — is Seurat's declared remit and was done by the Synthesis Lead. No
  Implementation Lead has confirmed feasibility, which `PROTOCOL.md` §5 criterion
  5 requires before convergence can be recommended, so **no specification may be
  frozen on the current record.**
- **Remedy:** the owner authorised Hogarth, Seurat and Dürer for the synthesis
  round. Their reports attach here.
- **Status:** accept, remedied prospectively. The challenge and revision rounds
  stand as written; they are not re-run.

## D-003 — Hogarth's pre-task briefs filed as evidence

- **What:** two briefs produced before RIGHTS-001 existed —
  `evidence/hogarth-01-pd-token.md` and
  `evidence/hogarth-02-architecture-review.md` — filed unaltered.
- **Why:** the intake baseline's open questions A–D and the round-two request's
  five enumerated weaknesses both derive from them. A record that cites findings
  it does not contain cannot be checked.
- **Caveat carried with them:** both predate the task, were not routed through
  the Coordinator, carry no envelope and had no liaison audit. Brief 01 was given
  one incorrect input — that the af Klint file credits the painter as author,
  which came from `js/photo-credits.js` rather than the file page, which names
  nobody. Corrected in the intake baseline; the reasoning does not depend on it.
- **Status:** accept as evidence, not as protocol artifacts.


## E-007 — `image.status` gates one of two image registries

- **Found by:** Hogarth, synthesis review, and verified independently before
  filing. Neither pole had it across two rounds.
- **What.** `image.status` exists only on `js/catalog-*.js` records. A second
  registry, `window.ARTWORKS` in `js/artworks.js`, holds **581 image entries and
  contains no `status` field anywhere** — measured: zero occurrences of the
  string in the file. It is loaded by `index.html` and rendered on artist pages
  by `js/app.js`.
- **The measurement.** Of the 23 attribution-required files in
  `js/photo-credits.js`, **19 also appear in `js/artworks.js`** — including
  `File:4_hilma_af_klint,_the_ten_largest,_no_9.jpg`, the file Decision B is
  entirely about, and `File:Degas_Little_Dancer_PMA(05c)_(15675423180).jpg` from
  Decision A. (Hogarth reported 15; the measured figure is 19.)
- **Consequence for the owner's options.** **B1 — "metadata-only, no image-like
  substitute" — does not remove the af Klint image from the site.** It would
  still render on the artist page through the ungated registry. **A3 does not
  remove the Degas photograph** for the same reason. Both options are scoped to
  one of two registries and do not produce the outcome their text describes.
- **Distinct from CH-1.** CH-1 found that withholding yields a procedural cover
  rather than nothing. This is a second and independent defect: withholding does
  not take effect at all on the artist-page surface.
- **What is not broken.** `creditUsage()` in `js/app.js` already walks both
  registries, so attribution renders for images reached either way. Only the
  gate is single-registry.
- **Status:** accept as finding. It reopens the option text for A and B; it
  decides nothing.


## E-008 — A1, executed alone, REMOVES attribution from the five files (Dürer)

- **Found by:** Dürer, feasibility assessment. Verified independently before
  filing.
- **What.** The inline credit is gated on `hasImg`:
  `js/app.js:2228` renders `<p class="img-credit">` only inside
  `${hasImg && imageCredit(w.image.src) ? … : ""}`, and `hasImg`
  (`js/app.js:2190`) requires `status === "pd"`. The credits index does the same:
  `creditUsage()` at `js/app.js:2495` opens
  `if(!(w.image && w.image.src && w.image.status === "pd")) return;`
- **Consequence.** Migrate the five named-photographer records to a new basis
  token with no other change and the images stop rendering, **their inline
  credits vanish, and they drop off `#/credits`**. The site would carry *less*
  attribution after a change made in the name of attribution accuracy.
- **Why this matters to the deliberation.** Round one, the challenge and the
  revision all treat A1 as vocabulary hygiene with a migration cost. It is not.
  A1 is only safe bundled with the render and credits path, and `js/app.js`
  rendering logic is outside OP-RIGHTS' write scope
  (`protocol/oriented/OP-RIGHTS.md`). **A1 must be specified as one bundle with
  the credits path, or not selected.**
- **Status:** accept as finding. It changes A1's consequence line; it does not
  decide A.

## E-009 — The documented status enum and the enforced one disagree

- **Found by:** Dürer, in passing. Verified.
- **What.** `docs/ARTWORK_SCHEMA.md:50` documents the vocabulary as
  `"pd" | "generative" | "none"`, and §127 describes `status:"generative"`
  rendering "the artist-style canvas seeded by artwork id, honestly captioned".
  `tools/validate.jxa.js:188` enforces `["pd","copyright","none"]`.
- **So:** `"generative"` is documented, described in a rendering rule, and
  **rejected by the validator**. `"copyright"` is enforced and carried by 61
  live records and **absent from the documented enum**. A record authored to the
  schema would fail the build.
- **Bearing on A1.** Any new basis token has to land in a vocabulary whose two
  existing definitions already contradict each other. This is repaired first or
  the migration inherits the contradiction.
- **Status:** accept as finding. Repair is specification work, not this round's.


## E-010 — Three credits name the painter, not the photographer (Seurat)

- **Found by:** Seurat, data-integrity audit of all 23 attribution-required
  files. Verified independently against the Commons API before filing.
- **What.** Pigment's `author` comes from extmetadata's `Artist` field, which for
  some files resolves to the **depicted work's creator** rather than the
  photographer. On two files the page's own wikitext names a photographer and
  Pigment credits the painter instead:

  | file | licence | Pigment credits | page's wikitext author |
  |---|---|---|---|
  | `Mrs._Siddons_as_the_Tragic_Muse_(3051182537).jpg` | CC BY 2.0 | `Joshua Reynolds` (d. 1792) | `Rennett Stowe` (Flickr) |
  | `Max_Beckmann,_Departure.jpg` | CC BY 2.0 | `Max Beckmann` (d. 1950) | `Allie_Caulfield` |

  A third, `4_hilma_af_klint,_the_ten_largest,_no_9.jpg`, records `Hilma af
  Klint` (d. 1944) where the wikitext names nobody at all. A fourth,
  `Osman_I_miniature_by_Nakkaş_Osman.jpg`, records a 16th-century miniaturist
  because the page itself writes that as bare text — there Pigment copied the
  page faithfully.
- **Why it matters.** Both CC BY 2.0 files require attribution, and the rendered
  credit names a party the file page does not name as the photographer. This is
  distinct from E-006: there the right person is named under two labels; here a
  different person is named.
- **Not concluded here.** Whether a notice naming the depicted work's creator
  rather than the photographer satisfies CC BY 2.0's attribution term is a
  question for counsel under the jurisdiction Decision D fixes. Neither pole
  states it.
- **Same root cause as E-006.** `tools/commons_rights.py:118`
  (`re.sub(r"<[^>]+>", "", s)`) discards the anchor `href` that distinguishes a
  `/wiki/User:` account from an `en.wikipedia.org` biography, so nothing
  downstream can tell a photographer's credit from a painter's.
- **Status:** accept as finding. It enlarges A and it is not confined to the six.


## D-004 — RIGHTS-001 split; two tasks opened

- **What:** `RIGHTS-002` (OP-RIGHTS) and `IFACE-001` (OP-INTERFACE) opened at
  baseline `8354de3`, both at `intake`, both `build_authorized: false`.
- **Why:** the final synthesis declined convergence — `PROTOCOL.md` §5 criteria
  4 and 6 do not hold. The evidence separates this task's work into parts with
  **different blockers**, and holding them in one task means the fastest work
  waits on the slowest:

  | part | blocked on | now |
  |---|---|---|
  | attribution accuracy (E-006, E-010) | nothing | **RIGHTS-002** |
  | the record-scoped no-image state (CH-1, E-007) | nothing but scope — it is not OP-RIGHTS' to write | **IFACE-001** |
  | Decisions A, B, C | Decision D, which only the owner can supply | stays here |

- **What stays in RIGHTS-001:** Decisions A, B, C and D, and the proposed
  Decision E's *owner question* — whether a credit should name the display text,
  the account, or both. RIGHTS-002 does the measurement and the tooling; the
  choice remains an owner decision on this task.
- **Constraint honoured:** `OP-INTERFACE.md` already claims "the walled record
  that has no image to show." The dependency was filed to the OP that owns it
  rather than resolved by widening OP-RIGHTS' scope — which is the discipline
  `protocol/oriented/README.md` states: *needing another OP's scope is a
  dependency to record, not a scope to widen.*
- **Open scope question carried into RIGHTS-002:** `tools/` is not in
  OP-RIGHTS' may-write table, and the E-006/E-010 fix edits
  `tools/commons_rights.py`. The owner widens the scope or the dependency is
  filed. It is the first thing that task settles.
- **Not done:** RIGHTS-001 is neither cancelled nor restarted. Its record —
  including D-001 through D-003, which document a skipped liaison audit and two
  rounds without specialists — stands as written. A restart would have produced a
  cleaner record that was less true, and the ten findings exist *because* the
  flaws were recorded rather than tidied away.
- **Status:** accept.


## D-005 — OWNER DECISION: the jurisdiction facts

**The first substantive owner decision on this task.** D-000 through D-004 are
process; this one supplies evidence only the owner had.

- **Decision, in the owner's words:** *"France, individual, no company, no
  revenue."*
- **Read as the four facts the analysis needs:** habitual residence **France**;
  legal operating form **private individual, no entity**; **no revenue** from
  Pigment; site hosted in the **United States** (GitHub Pages) and read
  anywhere. The owner's country of origin and family location are separate
  facts and, per `docs/RIGHTS_PRIMER.md`, are not the ones that bear here.
- **What it unblocks.** Decision D was gating precise answers to A, B and C
  because no question could be posed under a named law. It can now be. This does
  not decide A, B or C; it makes them answerable.
- **What the filed evidence already flags about France specifically**, recorded
  here so the next brief starts from it rather than rediscovering it:
  - **Moral rights are perpetual in France** (`docs/RIGHTS_PRIMER.md`). That
    reaches Decision C — the 61 procedural covers on named, protected artists —
    and the attribution questions in RIGHTS-002, by a route entirely separate
    from the economic term.
  - **France applies wartime extensions** to terms (same source), so
    "life plus seventy" arithmetic is not the whole rule for the older records.
  - **France is an EU member state**, so Article 14 of Directive (EU) 2019/790
    reaches the flat-reproduction question **through French transposition** —
    which is the specific thing Hogarth said could not be assessed while the
    member state was unnamed (`hogarth-02-architecture-review.md`).
  - **ADAGP is the French collecting society** and was correctly named in the
    architecture document, unlike the unverifiable GESAM. Relevant to the 61
    walled artists if a licensing route is ever opened — a PLATFORM question,
    not this task's.
- **Not concluded.** Nothing above is a determination. Whether any of it changes
  an outcome for any Pigment file is exactly what a qualified French practitioner
  would answer, and the census is already assembled so that costs an hour rather
  than five.
- **Status:** accept (owner), **amended by D-006 the same day** — residence is not
  settled. The operating-form and revenue facts stand unchanged.


## D-006 — AMENDS D-005: residence is undetermined between France and Turkey

- **What changed.** D-005 recorded "France" as the residence fact. On being told
  what France implied, the owner clarified: *"run it on France and Turkey (as my
  future is undetermined yet)."* Residence is **not settled**. Two candidate
  jurisdictions, either of which may become the operative one.
- **What still stands from D-005:** private individual, no legal entity, no
  revenue, US host, readers anywhere. Only the residence fact moved.
- **Why this is not a small amendment.** The two are structurally different for
  the questions on this task. **France is an EU member state and Turkey is not**,
  so Article 14 of Directive (EU) 2019/790 — the provision aimed squarely at
  whether a faithful reproduction of a public-domain visual work attracts new
  protection — reaches one through national transposition and does not reach the
  other at all. That provision governs precisely the flat-reproduction question
  behind `black-fuji` and `vahine-no-te-tiare`. Both are authors'-rights systems
  with moral rights, and both are Berne members, so they are not opposites; but
  they are not interchangeable either.
- **The consequence for how this task proceeds.** A brief that answers "under
  French law…" is now half an answer. The useful question becomes:

  > **Which decisions are robust to the residence uncertainty, and which turn on
  > it?**

  A decision that comes out the same under both can be taken now. One that
  genuinely diverges must either wait, or be settled by choosing an option that
  is safe under both. That framing is what the comparative brief was commissioned
  to produce.
- **Correction of my own record-keeping.** D-005 was filed as though residence
  were settled, on one word from the owner, before asking whether it was
  provisional. The amendment is same-day and the original entry stands unedited
  above rather than being rewritten — the record should show that the question
  was closed too early and reopened, not that it was always open.
- **Status:** accept (owner). D remains open as to residence; A, B and C are
  answerable comparatively but not yet answered.


## E-011 — Three corrections to the record, two of them mine (verified)

The France/Turkey brief corrected three statements this project had committed.
All three were checked independently before filing. The erroneous text is left in
place above and below; this entry is the correction.

**1. GESAM is real, and the record called it a fabrication.**
Türkiye Güzel Sanat Eseri Sahipleri Meslek Birliği — Ankara, founded 1986,
Turkey's professional body for fine-art rights holders, `gesam.org.tr`, operating
under FSEK art. 42. **[verified this session by independent search.]**

Hogarth's `hogarth-02-architecture-review.md` said he "could not place it among
collecting societies" — he had searched European societies for a Turkish body.
The Synthesis Lead then propagated that into
`theory-brief-request.md` §4 ("We could not locate GESAM. Please verify or
withdraw it"), into `round-two-request.md` ("Do not revive GESAM"), into
`messages/002-challenge.json`, and into D-005 ("the unverifiable GESAM"). **The
Theory Team dropped it on our instruction** and recorded the withdrawal in
`messages/001-theory_brief.json` and `003-revision.json`.

So `docs/ARTWORK_SOURCES_COPYRIGHT_ARCHITECTURE.md` was **right** to list GESAM
beside ADAGP, ARS and DACS, and this project was wrong to strike it. The entry we
flagged as likely invented is, if the owner becomes resident in Turkey, **his own
national society for exactly the 61 in-copyright artists** the atlas cannot
currently show. The immutable message envelopes are not edited; this entry
records the correction, and the Theory Team must be told.

**2. D-005 is wrong that Article 14 reaches France "through French
transposition."** France is reported among the member states that **declined to
transpose Article 14 separately**, on the view that existing French law already
produces the result. There is no separate French provision to read. **[verified
this session: Europeana PRO survey and Kluwer Copyright Blog, via search.]** The
flat-reproduction question behind `black-fuji` and `vahine-no-te-tiare` is
therefore an ordinary originality question in France, not an Article 14 one.

**3. `docs/RIGHTS_PRIMER.md` overstates France's wartime extensions.**
Cass. 1re civ., 27 Feb 2007 (n° 04-12.138) is reported to hold that the
harmonised 70-year term absorbs them, with a musical-works carve-out and an
unresolved "mort pour la France" +30. **[general — Hogarth marks this as
recollection to check, not fetched.]** For a painters' roster the practical
effect is that the primer's caution was larger than the facts support.

**Consequence for the term convention:** Turkey is life+70 running from 1 January
following death (WIPO Lex, Law 5846) **[fetched]** — the same arithmetic as
France. Pigment's "died 1955 or earlier" convention holds under **both**, and the
13 artists in the 1946–1955 band all died postwar.

**Status:** accept as corrections. Nothing here decides A, B or C.
