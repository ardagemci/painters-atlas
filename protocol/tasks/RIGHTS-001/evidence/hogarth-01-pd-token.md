# Hogarth — brief on the `pd` token (seven credit-required files)

**Provenance.** Produced by `claude-rights-analyst` (Hogarth) on owner
instruction during Lane II session work on 2026-08-30, **before RIGHTS-001 was
opened**. It was not routed through the Coordinator, carries no message
envelope, and had no liaison audit. Filed here unaltered because the task's
intake baseline and open questions A–D derive from it, and a record that cites
findings it does not contain cannot be checked.

**Superseded in one particular:** the brief was given evidence stating that the
af Klint file credits "Hilma af Klint" as author. That came from
`js/photo-credits.js`, not the Commons file page, which names nobody at all. The
correction is recorded in the intake baseline §4. The brief's reasoning does not
depend on it.

**Status at filing:** `triumph-of-death` has since been re-sourced onto a file
asserting a PD-Art basis, so the set of seven is now six.

---

## Brief — the `pd` token on seven credit-required files
**Hogarth (Rights Analyst). Not legal advice. No determination is made here.**

### 1. The decision
Whether `image.status` should gain a value meaning *"renderable, licence
asserted, credit required"* — and, until it does or does not, what the seven
records that currently borrow `"pd"` should carry.

### 2. The framework, plainly
A picture of an artwork is two objects with two histories: **the work** and **the
photograph of it**. They can expire at different times, or one can never have
started.

**Photographs of three-dimensional works** — `david`, `pieta`,
`little-dancer-aged-fourteen` — involve choices: viewpoint, lens, lighting,
framing. In most systems that is enough for the photograph to be an original work
in its own right, with its own term running from the photographer's life, wholly
independent of Michelangelo or Degas. That is consistent with what the Commons
pages here assert: a living photographer named as author (Bittner Unna, Traykov,
Vercruysse), offering a CC BY licence.

**Faithful reproductions of flat works** — `black-fuji`,
`the-ten-largest-no-9`, `triumph-of-death`, `vahine-no-te-tiare` — are the
contested case, and the contest is jurisdictional:

- **United States** (where Pigment is hosted): *Bridgeman Art Library v. Corel*,
  S.D.N.Y. 1999, held that a slavish photographic copy of a 2D public-domain work
  lacks the originality copyright requires. A district decision, not a Supreme
  Court one.
- **Germany**: the Bundesgerichtshof's *Reiss-Engelhorn Museen* decision (2018)
  went the other way for museum photographs of PD paintings, under a
  neighbouring-right for simple photographs.
- **European Union**: Article 14 of Directive (EU) 2019/790 says material
  resulting from an act of reproduction of a public-domain visual work is not
  protected unless it is the author's own intellectual creation — aimed squarely
  at that gap, but it lives in each member state's transposition, not in one text.
- **The owner's own country** is not the United States, and I do not know which
  rule applies there.

**Commons' PD-Art position** asserts that a faithful photographic reproduction of
a 2D public-domain work is itself public domain and may be hosted as such — a
hosting policy, applied by Commons to files worldwide. It is an assertion by the
project, and where an uploader has instead applied a CC BY tag, the uploader is
asserting the opposite about the same file. Note the tell in the evidence: two of
the four flat files name the **original painter** (af Klint, Brueghel) in the
author field, which is a description of the work, not of a photographer.

*Sourcing note: the schema, batch and test citations below I read this session.
The four case/statute references above are from general knowledge, not fetched —
treat them as pointers to check, not as findings.*

### 3. The options (unranked — the owner ranks)

**A. Change nothing.** Costs: `docs/ARTWORK_SCHEMA.md` §3 (lines 52–56) and
`docs/CATALOG_BATCH_02.md` constraint 5 (line 75) will keep saying different
things, and `"pd"` will keep reading as a rights label to anyone who does not
read the note beside it. Improves: nothing; costs nothing. Turns on: whether a
capped, documented contradiction — `TestPdTokenAccuracy` in
`tests/test_rights_tooling.py` holds it at seven — is acceptable as a standing
state.

**B. Add a fourth value** (`"licensed"`, or similar): renders, credit mandatory.
Costs: a schema change, validator rule, `js/app.js` branch, seven record edits,
and the test's expectation — Lane I or II work, Seurat and Dürer, not you or me.
Improves: the token stops implying a status the project does not claim, and the
credit obligation becomes machine-checkable rather than conventional. Turns on:
whether `status` should describe *basis of permission* at all, or stay a pure
render switch.

**C. Move the seven to `"copyright"`.** Costs: seven images stop rendering, for
no obligation anyone has asserted. Improves: literal conformance with constraint
5, zero schema work. Turns on: whether doc-conformance outranks showing the
pictures.

**D. Re-source the four flat files** to Commons files carrying a PD-Art basis,
leaving three. Costs: per-record research, image swaps, possible resolution loss.
Improves: shrinks the problem to the case where a photographer's own claim is
least doubtful. Turns on: whether equivalent files exist. No substitution helps
the three sculptures — every photograph has a photographer.

### 4. What I do not know
I do not know which country's law governs the owner's exposure. I do not know
whether the four flat files also carry a PD-Art tag alongside the CC tag — I did
not open the file pages. I do not know whether the two painter-named author
fields are metadata errors or deliberate claims. I do not know whether any of
these uploaders would ever assert anything. I do not know whether serving a
Wikimedia thumbnail counts as adaptation.

### 5. What I would put to counsel
1. For each licence version in use (CC BY 2.0, 2.5, 3.0; CC BY-SA 4.0), what
   elements must an attribution notice contain, and does the credit rendered from
   `js/photo-credits.js` contain all of them?
2. Does serving a resized Commons thumbnail of a CC BY-SA 4.0 file produce
   "Adapted Material" triggering ShareAlike, or a technical modification outside
   it?
3. For a US-hosted site with a non-US operator, whose law decides whether a
   faithful reproduction of a 2D public-domain work carries new copyright — and
   does Art. 14 of Directive (EU) 2019/790 as transposed where the photographer
   is domiciled bear on it?
4. Where Commons' PD-Art position and an uploader's CC tag conflict on one file,
   does complying with the CC tag create obligations that would not otherwise
   exist?
5. Where the named licensor is a painter dead for centuries, on what basis, if
   any, can the offered licence be relied on?
