# RIGHTS-001 — Theory Brief request

Outgoing intake handoff to the ChatGPT Theory Team. Copy the block below.
Workflow state on issue: `intake` → requesting `theory`.

---

You are the ChatGPT Theory Team for **Pigment**, an art atlas. We are opening
`RIGHTS-001`, the first task under a new **Oriented Protocol** called OP-RIGHTS.
The deliberation cycle is unchanged (`protocol/PROTOCOL.md`): you produce a
Theory Brief, Claude challenges it, you revise or defend, Claude synthesises,
the owner decides. What OP-RIGHTS adds is orientation — a fixed write scope, a
matched agent set, and acceptance criteria suited to rights questions rather
than to features.

**Your deliverable: a Theory Brief for RIGHTS-001.**

## Read this before proposing anything: what Pigment actually is

Measured today, not aspirationally.

- A **static site**. Plain HTML/CSS/JS, no build step, no backend, no database,
  no server-side logic of any kind. Hosted on GitHub Pages.
- **398 catalog records**, 880 unique image assets.
- Images are **hotlinked** from `upload.wikimedia.org`. Pigment stores no image
  files. Hotlinking and hosting are legally distinct acts and the distinction
  matters throughout.
- `image.status` is a **rendering token** with two live values: `"pd"` (342
  records) and `"copyright"` (61). It is read by one line of `js/app.js`. It is
  not a rights model; the schema says so explicitly.
- Rights evidence lives in a regenerable census
  (`protocol/tasks/PIG-001/evidence/artwork-image-rights.json`, produced by
  `tools/audit_artwork_rights.py`). Attribution rendering is generated from it
  into `js/photo-credits.js`. Both already work.
- One owner. No users. No staff, no review queue, no moderation capacity.

A proposal that assumes stored files, ingestion pipelines, a runtime policy
engine, or a human review queue is describing a different product. Say so
plainly if you think Pigment should become that product — but do not assume it
has silently already.

## The prior document, and how to use it

`docs/ARTWORK_SOURCES_COPYRIGHT_ARCHITECTURE.md` (committed at `dd87ad2`) is
yours. It is genuinely strong in places — its §9 non-assumptions, its refusal to
treat API availability as a rights grant, and the ADAGP point that obtaining a
photograph does not clear the artwork within it.

**It is two documents wearing one cover, and we are splitting it:**

- §§1, 3, 6, 7 — sources, data model, ingestion — belong to a future
  OP-PLATFORM task. **Out of scope here. Do not develop them in this brief.**
- §§2, 5, 8, 9 — the three-layer model, risk tiers R0–R4, provenance display,
  non-assumptions — are the input to **this** task.

Specific weaknesses our rights analyst identified, which the brief should
address rather than restate:

1. **R1 collapses six licence regimes into one rule.** "CC BY, CC BY-SA, or a
   clear institutional licence" is one tier, but version is load-bearing: CC 2.0,
   2.5 and 3.0 terminate automatically on breach with no cure period, while 4.0
   grants thirty days to cure. Our credit-required files span 2.0, 2.5, 3.0,
   4.0, BY-SA 3.0 and BY-SA 4.0.
2. **R1 files opposite reasoning in one bucket.** A CC BY 2.5 photograph of
   Michelangelo's *Pietà* — a new work by a living photographer who chose
   viewpoint and light — sits in the same tier as a flat reproduction of a
   painting, where the question is whether the reproduction attracts any
   copyright at all. Same tier, opposite analysis.
3. **Jurisdiction is deferred and never resolved.** The document cites EU
   Art. 14 without noting that a directive binds through each member state's
   transposition, and it never names whose exposure it models.
4. **"GESAM"** appears in the Tier C list of collecting societies. ADAGP, DACS
   and ARS are real and correctly named. We could not locate GESAM. Please
   verify or withdraw it.
5. **Vocabulary.** "clearance rates", "cleared its artwork rights" — see the
   OD-5 constraint below. The concepts survive; the words cannot be imported.

## The four open questions

**A. Six records carry `status:"pd"` on files whose Commons pages assert CC BY
or CC BY-SA.** All six render an attribution credit, so the obligation is met;
the defect is that the token asserts something the project has not established.
Five carry `{{self|...}}` — a named living photographer licensing their own
photograph (*David*, *Pietà*, *Little Dancer*, and two museum photographs by
one Commons contributor). Options already on the table: add a fourth status
value meaning *renderable, licence asserted, credit required*; change nothing
and keep the contradiction documented; move them to `copyright` and stop
rendering; re-source them. A seventh record left this set by re-sourcing onto a
file asserting a PD-Art basis, so the set is falling, not growing.

**B. One file carries a conflict on its own face.** `the-ten-largest-no-9`
(Hilma af Klint, d. 1944) currently uses a 127-byte Commons page: an empty
`{{Artwork}}` template and a bare `{{cc-by-sa-4.0}}` naming **no licensor at
all**. The best-tagged alternative in the same category is tagged
`{{PD-Art|PD-old-70}}` yet carries "© Stiftelsen Hilma af Klints Verk" inside
its own description field. Two assertions by strangers, in conflict, on one
painting. Note that a bare CC tag would populate a `licence_uri` field and
satisfy R1's schema while leaving standing entirely open — we would like the
brief to address what a tier system does with evidence that is well-formed and
possibly worthless.

**C. The generative covers — and this is the one no document has addressed.**
For records with no renderable image, `js/app.js` paints a cover **in the
browser** from the artist's own assigned style and palette, seeded by the work
id. On a copyright-walled record it is labelled *"a seeded Pigment
interpretation — the original artwork remains under copyright."* This affects
all 61 walled records: Noland, Guston, Motherwell, Kline, Hofmann, Enwonwu.
Pigment generates an image derived from a protected artist's style and renders
it on that artist's artwork page. Your §9 has no entry for "we generated it
ourselves," and R3 reads "no Pigment-hosted or embedded artwork image," which
does not describe what Pigment does. This is not a reproduction question. It may
touch style imitation, moral rights, and attribution in ways the reproduction
framework does not reach.

**D. Jurisdiction, underlying all of the above.** Hosted in the United States;
owner is not in the United States; readers are anywhere. We do not know which
determines exposure, or whether the answer differs per question.

## Hard constraints

<!-- This section spells out the forbidden phrases so the recipient can avoid
     them. It therefore contains four of them verbatim. That is safe only
     because protocol/tasks/RIGHTS-001/ is outside TestProseLanguage.SCANNED —
     an outgoing message is not project prose. Anyone widening SCANNED to cover
     protocol/tasks/ must add an OD5-EXEMPT marker here and pin it. -->

**OD-5 binds absolutely.** Pigment records *asserted basis and residual
uncertainty, never clearance*. This is enforced mechanically: a language guard
in the test suite scans `docs/`, `protocol/oriented/`, `tools/`, `tests/` and
`js/app.js` and fails the build on phrases including "verified PD", "confirmed
public domain", "rights-cleared", "cleared for use", and constructions of the
form "X is public domain". Bounded alternatives that pass: *"Commons metadata
asserts a public-domain basis"*, *"this audit did not locate"*. Write the brief
in language that would survive that guard.

**Neither team states a legal conclusion.** Not you, not Claude, not our rights
analyst. The output of this task is owner decisions and, where needed, a brief a
qualified lawyer could act on. A hosting policy is not a determination. Death-year
arithmetic is a heuristic. Where you do not know, say "I don't know" in those
words rather than hedging.

**Distinguish the work from the photograph of it,** every time. Most of the
confusion in this domain collapses those two.

## What the brief should contain

Use the envelope in `protocol/PROTOCOL.md` §3 — all fields, including
`assumptions`, `disputed_points`, `risks`, and `confidence` with a one-line
basis. Then, in the body:

1. A rights model that fits a **static, hotlinking, single-owner site** — or an
   explicit argument that Pigment must stop being one, with the cost stated.
2. A concrete recommendation on the `status` token: how many values, what each
   asserts, and what the renderer does with each. Name the migration for the six.
3. A position on question C. This is the part we most need theory on, and the
   part where we have the least.
4. What you would put to counsel, phrased as questions a lawyer can bill against
   efficiently — the census is already assembled, so no one should pay for
   reading time.
5. What you do not know.

## What would make this brief fail review

Restating the architecture document. Proposing machinery that presumes a backend.
Producing a five-tier taxonomy without saying which of our 880 assets lands in
which tier. Treating "add a field" as an answer to "what is the basis." Asserting
any legal conclusion. And padding: a shorter brief that decides something beats a
longer one that surveys.
