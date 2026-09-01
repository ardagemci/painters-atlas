# Hogarth — rights-analyst review for the final synthesis

**Provenance.** Produced by `claude-rights-analyst` (Hogarth) for RIGHTS-001
round 3, on owner authorisation, after decision record D-002 recorded that two
rounds had run with no specialist input. This is the OP's lead reviewing work
done in his absence.

**Verified before filing.** Two claims were checked independently:

- The second-registry finding (§3) **holds**, and is larger than stated.
  `js/artworks.js` contains **zero** occurrences of `status` and 581 image
  entries. Of the 23 attribution-required files, **19** — not 15 — also appear
  there, including the af Klint file Decision B concerns and the Degas
  photograph from Decision A. Recorded as E-007.
- The duplicate `E-002` numbering **held** and is corrected; the Sailko finding
  is now E-006.

---

**Hogarth — rights-analyst review for RIGHTS-001 final synthesis. Not legal
advice. Nothing here is a determination, and nothing here decides A, B, C or D.**

**The decision the owner faces in this round:** whether the option sets as
revised are complete enough to be selected from, or whether two of them describe
an outcome the current build does not produce.

**1. The three narrowings.**

*CH-3, narrowed to "an analytical 3+2+1 evidence grouping, not a demonstrated
legal distinction."* Legitimate, and the revision is more disciplined here than
the challenge was. Whether a photograph of a flat public-domain work carries
anything of its own is answered differently in different places — the United
States has *Bridgeman v. Corel* (S.D.N.Y. 1999, a district decision); Germany has
the Bundesgerichtshof's *Reiss-Engelhorn* decision (2018) going the other way;
the European Union has Article 14 of Directive (EU) 2019/790, which binds only
through each member state's transposition. Naming the 3+2 split as a legal
distinction would require knowing which of those applies, which is Decision D,
which is open. The narrowing is not evasion because the revision carries the
grouping's consequence into the counsel questions — it asks how the named
jurisdiction treats the media layer *for the 3D and flat groups separately*. That
is the grouping doing work. What it still owes the owner is one line per group
saying what evidence would move it.

*CH-4, "accepted narrowly."* Legitimate, and CH-4 overclaimed. Measuring the
runtime paint path (`js/app.js:815–850`, no `getImageData`, no `drawImage` of a
source) establishes what the browser does. It does not establish how 279
hand-authored palettes in `js/artists-*.js` were arrived at; a person chose those
hexes while looking at something. "Provenance undocumented" is the accurate
statement. Where it shades into evasion: the revision does not say what would
document it, and the answer is cheap — the person who authored the palettes is
the owner, in the room, and nobody has asked him.

*CH-2, accepted in substance, successor guard rejected.* This is the narrowing
that leaves the owner worst off, though the objection inside it is sound:
counting every conditional-basis record as a permanent offender swaps one proxy
for another. But the substitute is a promise. `TestPdTokenAccuracy` filters the
literal `status:"pd"` string; under A1 the five records leave that string and the
count falls to one, and the replacement guards "do not yet exist" (E-003) and
belong to a specification D-002 says may not be frozen. CH-2's complaint was that
A1 buys a green test and no answer; the reply is a test that does not exist yet.
A1's consequence line should say plainly that selecting it retires the only guard
now holding these six and converts it into a requirement on future work — the
same shape as CH-1's metadata-only dependency, which the revision does at least
name.

**2. E-002** *(now E-006)*. First, a bookkeeping defect: the decision record
contains two entries numbered E-002 (the CH-1 adaptation and this finding). Fix
before synthesis.

The finding is broader than recorded. `js/photo-credits.js` credits
`author:"Sailko"` on three files and `author:"Francesco Bini"` on a fourth. If
the account identity holds, one contributor's work appears at least four times in
the rendered attribution set, not twice — so A2's per-record re-sourcing cost is
understated by more than CH-3 said.

What it means: Pigment's attribution register captures a wikilink display string
rather than the account, so it cannot detect that one contributor recurs. That is
a schema and tooling fact, established from the repository and the Commons API.

What it does not mean: it is not a finding that the attribution obligation has
been missed. Each string is the one the licensor himself put in the author field
of that file page. It is not a finding about who Francesco Bini is — Commons
asserting an account-to-name mapping is an assertion by a stranger, and a hosting
policy is not a determination. And it says nothing about the underlying Hokusai
print or Gauguin painting, which are separate objects from the two photographs.

The question for counsel: under the law of the jurisdiction fixed by Decision D,
for CC BY 3.0 (`black-fuji`) and CC BY-SA 4.0 (`vahine-no-te-tiare`)
specifically, does a notice reproducing the author string exactly as the licensor
supplied it on each source page satisfy that version's attribution term, when the
same licensor supplied different strings and the site therefore names one
contributor as two people — and does substituting the account name, which the
licensor did not choose as display text, improve or worsen that position?
Versions differ on cure, so ask per version.

**3. Whether the four decisions let the owner choose.** Two do not, for a reason
neither pole has.

`image.status` gates `js/catalog-*.js` only. A second registry,
`window.ARTWORKS` in `js/artworks.js`, holds 581 image entries, contains no
`status` field anywhere, is loaded by `index.html:158`, and is rendered on artist
pages by `js/app.js:2117`. Fifteen of the 23 credit-required files render through
it — including `File:4_hilma_af_klint,_the_ten_largest,_no_9.jpg`
(`js/artworks.js:932–935`), the exact file Decision B is about, and the Degas
*Little Dancer* photograph from Decision A. So **B1 as written does not remove
the af Klint image from the site**, and A3 does not remove the Degas one; both
are scoped to one of two registries. This is a second and distinct defect from
CH-1's. To Rubens' credit, `creditUsage()` (`js/app.js:2486`) already walks both
registries, so credits render for both; only the gate is single-registry.

*(Filing note: the measured figure is 19 of 23, not 15. The finding stands and is
larger. See E-007.)*

Decision D's options are real as sequencing, but D cannot be chosen in the sense
A, B and C can, because the option set omits the input that makes any of them
commissionable: the owner's country and operating form. The revision writes
"Turkey only if confirmed as relevant." One sentence from the owner settles that,
and it is the cheapest movement available on this task. C1–C4 cover their space.

**4. The "no visual originality audit" correction.** Fair, and I would have made
it. CH-3's sentence — that for the three sculptures original photographic choices
are "not in question" — is a conclusion about three specific photographs, in the
direction of more protection rather than less, and neither pole is competent to
state it. My own brief 01 said only "in most systems that is enough," from
general knowledge, unfetched, and I flagged it there as a pointer to check. But
the revision is over-cautious in its framing: it treats a missing audit as the
gap. Pigment cannot audit originality. That characterisation happens under a
named country's rule, and the honest statement is not "we have not audited" but
"this turns on a rule not yet identified, because D is open."

**5. What I do not know.** I do not know which country's law governs the owner's
exposure, or whether it differs for owner, United States host and reader —
resolved only by the owner naming his country and form, then a bounded memo. I do
not know whether the rendered credits satisfy the attribution terms of CC BY 3.0
and CC BY-SA 4.0 — resolved by the question in §2. I do not know whether serving
a 500px Wikimedia thumbnail is Adapted Material under CC BY-SA 4.0 — counsel. I
do not know who applied either af Klint template or whether the Stiftelsen notice
claims the work, the photograph, or is boilerplate — resolved by the file's
Commons revision history plus a provenance statement (B2). I do not know how the
279 palettes were authored — resolved by the owner's own account. I do not know
whether "Sailko" and "Francesco Bini" are one person; the Commons user page would
assert it, and an assertion is all it would be.
