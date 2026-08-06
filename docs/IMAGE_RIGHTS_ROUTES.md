# Image Rights — Pool Verification and Legal Routes

*Seurat (`claude-data-steward`), 2026-08-06. Branch `main`. Two separate pieces
of work: **Part 1** verifies the unused image pool `ATLAS_COVERAGE.md` identified;
**Part 2** researches whether post-1955 painters could enter the atlas legally.*

**Nothing in this document is a rights determination, a clearance, or legal
advice.** Per OD-5 it records what a source *asserts* and what remains
uncertain. No image was added, fetched into the repo, or promoted into
`js/catalog-*.js` in this pass. I am not qualified to give legal advice and
neither is anyone else on this team; every route in Part 2 is framed as *what
would need to be established*, not as a conclusion.

**A note on one word.** The coordinator proposed `CLEARED` as a verification
label. I have used **`MATCH CONFIRMED`** instead. "Cleared" is the exact word
OD-5 forbids, and a reader skimming a table of image records would have no way
to tell "cleared of the wrong-artwork suspicion" from "cleared for use." The
distinction this document exists to protect is the one that label would blur.

---

# PART 0 — THE FINDING THAT MATTERS MOST

**Wikipedia's images of Picasso, Warhol, Dalí, Kahlo, Pollock, Rothko and
Matisse are not usable by Pigment, and the fact that they are visible on
Wikipedia is not evidence that they are.**

The owner's phrasing — that "Wikipedia and different sources may have public
domain (or usable without any rights violation) artworks" — is reasonable on its
face, and it is precisely where this would go wrong.

English Wikipedia hosts those images under a **non-free content criteria (NFCC)
fair-use rationale**. That rationale is a claim about *Wikipedia's own use*: a
low-resolution image, in an encyclopedic article, that critically discusses the
specific work, on a US-hosted non-profit encyclopedia. Every one of those
conditions is load-bearing, and **fair use does not transfer with the file.** It
is not a property of the image; it is a property of a particular use by a
particular publisher in a particular jurisdiction. Copying such a file into
Pigment does not inherit the rationale — it starts a new use that would have to
justify itself on its own facts, in Pigment's own jurisdiction, for Pigment's own
purposes.

This is the dangerous case precisely *because* it looks legitimate. The file sits
on a reputable source, next to files that genuinely are free, reachable by the
same tooling, and the page that hosts it does not shout. A harvester that treats
"it was on Wikipedia" as the test would ingest these without a single error
message. It would be a rights violation wearing the appearance of a
well-sourced pipeline.

**The operational rule that follows, and it is already half-enforced in the
codebase:** files served from `upload.wikimedia.org/wikipedia/**en**/` are
English-Wikipedia-local uploads, which is where non-free content lives.
Files under `/wikipedia/commons/` are on Wikimedia Commons, whose upload policy
requires a free or public-domain basis to be *asserted*. `ARTWORK_SCHEMA.md` §9
already requires `image.src` to contain `/wikipedia/commons/` when
`status:"pd"`, and `tools/commons_rights.py:commons_file_title()` already
returns `None` for non-Commons paths with the comment *"e.g. /wikipedia/en/ =
local fair use"*. **That is the correct instinct and it should be stated as a
rule rather than left as a comment**, because it is the single check that stands
between this project and the failure above.

Two cautions so the rule is not over-trusted in the other direction:

1. **Commons hosting is an assertion, not an adjudication.** It means an
   uploader asserted a basis and no reviewer has removed it. Commons deletes
   copyright violations continuously, which is evidence the assertion is
   sometimes wrong.
2. **"Not on Commons" is not the only failure mode.** Part 1 found 20 pool files
   that *are* on Commons and carry CC BY / CC BY-SA licences with live
   attribution obligations — free to use, but not free of conditions, and
   Pigment honours those conditions nowhere.

---

# PART 1 — VERIFICATION OF THE UNUSED IMAGE POOL

## 1.1 What the pool is, and confirmation of the curator's counts

`ATLAS_COVERAGE.md` reported the pool from a direct read of `js/`. I recomputed
it independently. **Every figure reproduces exactly.**

| Quantity | Curator | This audit |
|---|---|---|
| Artists in atlas | 256 | 256 |
| Artists with ≥ 1 catalogued artwork | 46 | 46 |
| Artists with **zero** catalogued artworks | 210 | 210 |
| Of those, carrying images in `js/artworks.js` | 141 | 141 |
| **Unused `ARTWORKS` entries (the pool)** | **413** | **413** |

Method: `js/artworks.js` parsed as JSON; `artistId` harvested from
`js/catalog-*.js`; artist registry dumped via JXA across all 17 `artists-*.js`
files. (The shipped `tools/dump-artists.jxa.js` reads only `artists-1..15` and
would silently miss two files — noted below as a defect, not used here.)

## 1.2 Do the URLs still resolve? — **all 413 do**

| Status | Count |
|---|---|
| **ok** — HTTP 200, `Content-Type: image/*` | **413** |
| bad — definitive 4xx (400/404/410) | 0 |
| unverified — timeout / 429 / 5xx after backoff | 0 |

Rate-limit discipline, per `PIGMENT.md` §14 and the transport rules in
`tools/commons_rights.py`: a process-wide **0.25 s minimum spacing**, up to four
attempts with **1 s / 3 s / 9 s backoff**, `Retry-After` honoured, and a
timeout / 429 / 5xx classified **`unverified` — never `bad`**. Only 400, 404 and
410 count as definitive negatives. No entry reached the `unverified` state, so
no judgement had to be suspended on transport grounds.

**This matters for scoping.** The prior incident where a similar tool falsely
killed 216 entries did not repeat, and there is no dead-link cleanup to fund:
the pool's link rot is zero. The pool's problems are entirely about *what the
images depict* and *what licence they carry*.

## 1.3 What Commons asserts about each licence

All 413 files returned `imageinfo` with `extmetadata` — 0 missing, 0 unverified.
These are **assertions recorded on the Commons file page**, not findings by this
project and not determinations by Commons.

| Licence asserted | Files | Obligation if used |
|---|---|---|
| Public domain | 385 | none stated |
| CC0 | 8 | none (waiver) |
| CC BY-SA 4.0 | 9 | **attribution + share-alike** |
| CC BY 2.0 | 6 | **attribution** |
| CC BY-SA 3.0 | 3 | **attribution + share-alike** |
| CC BY 4.0 | 1 | **attribution** |
| CC BY 3.0 | 1 | **attribution** |

`Copyrighted` extmetadata: `False` on 385, `True` on 28 — consistent with the
licence split (a CC licence, including CC0, presupposes a copyright to license).

**Finding: 20 of 413 pool entries carry a licence with a live attribution or
share-alike obligation.** The pool is not the uniformly-public-domain body the
Direction A cost estimate assumes. This is the same failure class recorded in
`tools/fetch_artworks.py`'s `SUPPRESS` comments, where wrong images arrived
"carrying attribution obligations Pigment honours nowhere." A share-alike
licence in particular is a condition on the *downstream work*, and whether it
reaches a page that merely displays the image is not a question I can answer.

Most of these 20 appear to be **photographs of public-domain paintings**, where
the photographer asserts a copyright in the photograph. Whether such an
assertion holds for a flat, faithful reproduction is a genuinely contested
question of law that turns on jurisdiction and on how three-dimensional or
interpretive the shot is — a framed painting on a gallery wall is not the same
case as a flat scan. **I am not resolving it.** It is flagged for qualified
review, and it is an argument for preferring a different file where one exists.

Two files additionally carry a `Restrictions` assertion of **`ita-mibac`** —
Italy's cultural-heritage code, which Commons flags as potentially requiring
Ministry permission for commercial reproduction:

- `paolo-veronese :: Feast in the House of Levi`
- `lavinia-fontana :: Portrait of the Gozzadini Family`

## 1.4 Death dates against the licence basis

All **141** pool artists have a recorded death year and **all are ≤ 1955**,
consistent with `tools/fetch_artworks.py`'s `CUTOFF` gate. No pool entry depends
on a post-1955 artist. Zero artists lacked a death year.

Per OD-5 this supports the *asserted* basis and establishes nothing. A death
year is an input to a term calculation that varies by jurisdiction, by
publication history and by work; it is not itself a rights conclusion. Note that
the pool's death dates come from our own `js/artists-*.js` records, which are
themselves unaudited against an external source.

## 1.5 Exact-artwork check — method, and why the existing tool misses these

The defect named in the brief is real and still in the tree. It is at
**`tools/audit_artworks.py:86`** (the brief said `:75`; the function
`fname_valid` begins at line 82 and the accepting expression is line 86 — the
line numbers shifted when the `RIGHTS` capture block was added):

```python
return any(t in f for t in name_toks) or any(t in f for t in title_toks)
```

A file is accepted if its **filename** contains **any** artist token **or**
**any** title token. Both halves fail independently:

- The `or` means a file needs no connection to the artist at all, provided it
  shares one word with the title. This is how `ogata-korin :: Irises` acquired
  Van Gogh's *Irises*.
- Token matching is substring-based on a ≥ 4/5-character floor, so generic words
  qualify. `Portrait`, `Forest`, `Winter Landscape` and `Flower Still Life` are
  title tokens that match thousands of unrelated files.
- It reads only the **filename**, never Commons' own `ObjectName` or `Artist`
  metadata — which, in every case below, states plainly that the file is
  something else.

**My check instead uses what Commons asserts about the file**, cross-referencing
our artist and title against the file's `ObjectName`, `ImageDescription` and
`Artist` fields, with Unicode folding and a stoplist of ~120 generic art words so
that "portrait" and "landscape" cannot carry a match on their own. Candidates
are then confirmed by reading the actual Commons file page.

**A caveat I am keeping visible: the automated pass over-flags.** It cannot
recognise translated titles, so *Le Berceau* / *The Cradle*, *Der Bohnenesser* /
*The Beaneater* and *Le Verrou* / *The Bolt* all surfaced as candidates and are
correct images. It also cannot distinguish a series from its members. **This is
why nothing below is asserted as a mismatch until the file page has been read.**
The label on each row carries the uncertainty.

## 1.6 Candidate mismatches

Status values: `CONFIRMED MISMATCH` — file page read, depicts something other
than the claimed work · `MATCH CONFIRMED` — file page read, does depict the
claimed work · `UNRESOLVED` — checked, evidence insufficient ·
`UNVERIFIED` — not yet checked against the file page.

### Group A — Commons attributes the file to a *different artist*

| # | Record | What Commons asserts the file is | Status |
|---|---|---|---|
| A1 | `ogata-korin` :: Irises (Kakitsubata-zu) | *Irises* — **Artist: Vincent van Gogh** | UNVERIFIED |
| A2 | `berthe-morisot` :: Young Woman Powdering Her Face | *Young Woman Powdering Herself* — **Artist: Georges Seurat** | UNVERIFIED |
| A3 | `amedeo-modigliani` :: Portrait of Chaim Soutine | *View of Céret* — **Artist: Chaïm Soutine** (a landscape *by* the sitter) | UNVERIFIED |
| A4 | `claude-lorrain` :: The Enchanted Castle | *The Enchanted Castle* — **Artist: Francis Danby** (V&A) | UNVERIFIED |
| A5 | `rachel-ruysch` :: Flower Still Life | *A Flower Still Life with Grapes, 1857* — **Artist: Amalie Kaercher** | UNVERIFIED |
| A6 | `seker-ahmed-pasha` :: Forest (Woodland Scene) | *Forêt / Forest, c. 1902–04* — **Artist: Paul Cézanne** | UNVERIFIED |
| A7 | `sesshu-toyo` :: Winter Landscape | *Winter Landscape with Brabrand Church* — **Artist: Christian David Gebauer** | UNVERIFIED |
| A8 | `reza-abbasi` :: Portrait of a Dervish | *Portrait of the artist Reza 'Abbasi* — **by Mu'in Musavvir, 1676** (a portrait *of* him, by another hand) | UNVERIFIED |
| A9 | `xu-beihong` :: Galloping Horse | *Animated race horse* — **photographs by Eadweard Muybridge**, animation by a Commons user; not a painting | **CONFIRMED MISMATCH** |

A9 is confirmed: the file page states *"Photos made by Eadweard Muybridge.
Animation by User Waugsberg"*, describing an animated GIF from *Animal
Locomotion* (1887). It is not a work by Xu Beihong and not a painting.

### Group B — right artist, but Commons names a *different work*

| # | Record | What Commons asserts the file is | Status |
|---|---|---|---|
| B1 | `hans-holbein` :: Portrait of Henry VIII | *Portrait of **Anne of Cleves*** (Louvre) | UNVERIFIED |
| B2 | `nicolas-poussin` :: The Four Seasons | *Self portrait of Nicolas Poussin* | UNVERIFIED |
| B3 | `lucas-cranach` :: Adam and Eve | *Portrait of Princess Sibylle of Cleve* | UNVERIFIED |
| B4 | `george-stubbs` :: Horse Attacked by a Lion | *Self-portrait* | UNVERIFIED |
| B5 | `paula-modersohn-becker` :: Self-Portrait at Sixth Wedding Anniversary | *Old poor woman with a glass ball and poppies* | UNVERIFIED |
| B6 | `mihri-musfik` :: Self-Portrait | *Leyla Turgut Portresi* — a portrait of a named sitter | UNVERIFIED |
| B7 | `lyubov-popova` :: Textile designs, First State Factory | *Composition (1917)* — a painting, not textile design | UNVERIFIED |
| B8 | `gustave-moreau` :: Oedipus and the Sphinx | *Étude pour la tête d'Œdipe* — a head study, not the painting | UNVERIFIED |

**Four of these eight are self-portrait confusions** (B2, B4, B5 and B6 in the
reverse direction). That is the same failure the brief describes from the
previous audit, and it has an obvious mechanism: `self` and `portrait` are in
every painter's title list, so under the line-86 rule any self-portrait file
matches almost any portrait record.

### Group C — not a reproduction of the work at all

| # | Record | What Commons asserts the file is | Status |
|---|---|---|---|
| C1 | `kurt-schwitters` :: Ursonate | *Kurt Schwitters, 1927* — a **photograph of the artist** | UNVERIFIED |
| C2 | `emily-carr` :: Big Raven | *Emily Carr Canada stamp 1971* — a **postage stamp** | UNVERIFIED |
| C3 | `utagawa-hiroshige` :: One Hundred Famous Views of Edo | a **side-by-side composite** of Hiroshige's *Evening Shower at Atake* and Van Gogh's 1887 oil copy | **CONFIRMED — partial** |

C3 is confirmed and is subtler than the automated pass suggested. The file page
shows the image contains **both** works side by side: Hiroshige's print *and*
Van Gogh's *Bridge in the Rain, after Hiroshige* (Van Gogh Museum). So the
claimed work is present, but the file is a comparison plate rather than a
reproduction of the print — a §14 "exact artwork" failure, not a wrong-artist
failure. **This is exactly why the file page has to be read before a row is
called a mismatch**, and it is the reason the rest stay labelled UNVERIFIED.

### Group D — §14 rendering defects (correct work, unsuitable file)

Distinct from mismatches: the file plausibly depicts the right work but
violates "full compositions preferred over detail crops" or shows the work in a
room.

| Record | Defect | Licence asserted |
|---|---|---|
| `frans-hals` :: Banquet of the Officers of the St George Militia | filename says *detail of* | Public domain |
| `georges-seurat` :: Bathers at Asnières | *Study for* Bathers, not the painting | Public domain |
| `henri-rousseau` :: The Sleeping Gypsy | *(detail)* | CC BY 2.0 |
| `annibale-carracci` :: The Farnese Gallery ceiling | *detail* | Public domain |
| `piero-della-francesca` :: The Resurrection | *detail* | CC BY-SA 4.0 |
| `levni` :: Portrait of Sultan Ahmed III | *Levni 002 detail* | Public domain |
| `peter-paul-rubens` :: The Marie de' Medici Cycle | *Skizze* — an oil sketch for the cycle | CC BY 4.0 |
| `jacob-van-ruisdael` :: The Windmill at Wijk bij Duurstede | Rijksmuseum **Gallery of Honour** installation photo | CC BY-SA 4.0 |
| `jean-simeon-chardin` :: Saying Grace | *(cropped)* | Public domain |
| `kathe-kollwitz` :: The Grieving Parents | a **sculpture**, photographed in situ | CC BY 2.0 |

The Kollwitz row deserves separate attention: the work genuinely is a sculpture,
so the photograph is of a three-dimensional object and the photographer's CC BY
2.0 claim does not meet the flat-reproduction argument at all. This is the
freedom-of-panorama case discussed in Part 2 §2.1, arriving from the other
direction.

### Group E — opaque filenames, no evidence either way

A residual class where the Commons filename is a serial number
(`Paolo Veronese 008`, `Ito Jakuchu 001`, `Riza-yi-Abbasi 008`, `Jan Steen 005`,
`Franz Marc 029a`, `Ferdinand Hodler 002`, `Paula Modersohn-Becker 001`) and
`ObjectName` merely repeats it. These cannot be confirmed or refuted from
metadata; each needs a human to look at the image. `jan-steen :: The Merry
Family` is the most doubtful — its `ObjectName` reads *Katzenfamilie* ("cat
family"), which is not an obvious alternative title for *The Merry Family*.

## 1.7 What the pool verification means for scoping Direction A

- **Link rot: zero.** No remediation cost.
- **Wrong-image rate: ~20 candidates in 413 (≈ 5%)**, pending confirmation —
  materially higher than an unaudited pool is usually assumed to be, and
  concentrated exactly where the line-86 rule is weakest (generic titles,
  self-portraits, series).
- **Licence obligations: 20 entries** are CC BY / CC BY-SA, not public domain.
- **Therefore Direction A's "close to mechanical" Tier 2 promotions are not
  mechanical.** Every promoted record needs the file page read. At ~5% wrong and
  ~5% obligation-carrying, a 120-record promotion would ship roughly a dozen
  defects if promoted on the strength of the existing tooling.

This does not argue against Direction A. It argues that the exact-work check has
to be repaired **before** the promotion, not after.

---

# PART 2 — LEGAL ROUTES FOR POST-1955 PAINTERS

The current rule is **artist died ≤ 1955**, a deliberately conservative proxy for
life + 70. Seven Tier 1 artists — Picasso, Dalí, Kahlo, Pollock, Rothko, Warhol,
Matisse — carry full exhibition arcs with no images.

**I am not recommending that the rule be loosened.** The routes below are
enumerated with what each would require. Where a route unlocks almost nothing, I
say so.

## 2.0 The trap, restated in one line

See Part 0. **Wikipedia's fair-use images do not transfer.** Any route below that
appears to be working because "the image was on Wikipedia" is this trap and not a
route.

## 2.1 Freedom of panorama — *narrow for painters, real for a handful of murals*

**What it permits.** Many countries allow photographs of works **permanently
sited in public places** to be published without the copyright holder's consent.
Where it applies, the *photograph* can be freely licensed even though the
underlying work is in copyright.

**What it forbids, and why it barely helps a painting atlas.**

- It generally attaches to **buildings and sculpture**, not to paintings. A
  painting hanging in a museum is neither permanently sited outdoors nor in a
  public place in the relevant sense. **For easel painting — which is nearly all
  of Pigment — freedom of panorama does essentially nothing.**
- Scope varies enormously by country: some jurisdictions cover buildings only;
  some cover sculpture too; some **exclude commercial use**, which is a live
  problem because Pigment cannot guarantee its use stays non-commercial forever,
  and Commons will not host a non-commercial-only file at all.
- France and Italy are among the more restrictive, which is exactly where the
  relevant modern murals are not.

**What it would unlock, honestly.** The plausible candidates are **permanently
sited public murals** — the Mexican muralists above all. Rivera, Orozco and
Siqueiros painted public walls, and Mexico is a case where the term is life+100
so the underlying works remain in copyright regardless. Orozco (d. 1949) is
already inside the atlas's own cutoff by death date. Siqueiros (d. 1974) is the
one where panorama would have to do the work.

**Evidence needed per work:** that the work is permanently sited; that it is in a
public place as that country's statute defines it; that the country's provision
covers *paintings/murals* and not only architecture; that it permits commercial
use; and a photograph whose photographer has actually licensed it freely.

**Reach: very small. Realistically a low single-digit number of works, possibly
zero after the per-country test.** Residual risk: moderate-to-high, because the
determination is per-country and per-work and the failure is silent.

**Not a strategy. Worth naming only so it is not mistaken for one later.**

## 2.2 Deliberate free licensing by artists, estates and foundations

**What it permits.** A rights holder may release work under CC BY, CC BY-SA or
CC0. Where they genuinely have, the work is usable on the licence's terms
regardless of death date. This is the **only route in this document that is
clean by construction**, because the permission is affirmative rather than
inferred.

**What it forbids.** The licence's own conditions bind: attribution for CC BY;
attribution plus share-alike for CC BY-SA — and share-alike's reach into a page
that merely displays an image is not something I can determine. A licence
granted by someone who did not hold the rights grants nothing.

**What it does *not* cover, and this is the common misreading.** **Museum
open-access programmes release the museum's photography, not the artists'
copyrights.** When the Met, the Rijksmuseum, the Art Institute of Chicago or the
Smithsonian put collections under CC0 or "open access," what they can give away
is their own rights in the reproduction. For an in-copyright painting the
underlying work is still the artist's estate's, and those programmes are
correspondingly limited to works the institution believes are out of copyright.
**Open access therefore adds enormous value for pre-1955 work and close to none
for the seven artists in question.** Anyone scoping this should expect the
museum open-access route to return zero Picassos.

**Evidence needed per work:** the specific licence, the specific work it covers,
identification of the grantor and a reason to believe they held the right, and
the grant's date and permanence.

**Reach: unknown but probably very small for these seven specifically.** The
major modern estates — the Picasso Administration, the Warhol Foundation, the
Dalí foundation, the Matisse and Rothko estates — are known for *active*
licensing programmes, which is the opposite posture from free release. **I would
expect this route to unlock none of the seven and would not promise otherwise
without checking each estate directly.** It may unlock other 20th-century names
outside that list.

**This is the route I would actually pursue**, precisely because it is the only
one where a positive answer is a document rather than an inference.

## 2.3 Public domain by routes other than the death date

Several genuine mechanisms, of very different value.

**(a) US formalities — the strongest of these.** Works published in the US
before 1929 are out of copyright there. Between 1929 and 1963, US copyright
required **renewal**, and a large fraction was never renewed; publication without
a copyright notice before 1978 could also forfeit protection. For an
American-published work this can produce a public-domain status regardless of
when the artist died. Pollock, Rothko and Warhol are US artists, so this is
where it would bite if anywhere.

*But:* it turns on **publication**, a term of art. A painting exhibited in a
gallery is not obviously "published"; whether reproduction in a catalogue counts,
and with what notice, is a per-work factual question requiring renewal-record
research. It also yields a US-only status, while Pigment's visitors are not.
**Evidence needed:** the publication event, its date, the presence or absence of
notice, and a renewal-record search. **Reach: unknown without per-work research;
plausibly a small number of specific images rather than any artist's body of
work.** This is real, and it is expensive per work.

**(b) Government works.** Works by US federal employees in the course of duty are
not under US copyright. This reaches WPA-adjacent and official art in some cases
but does not reach the studio work of the seven.

**(c) Shorter-term jurisdictions.** Some countries run shorter terms, and a few
works are public domain somewhere and not elsewhere. For a globally-reachable
static site this creates a status that is true in one place and false in another
— **which is a reason for caution rather than a route.** Note the inverse also
bites: Mexico's life+100 is *why* Kahlo is unavailable, as
`tools/fetch_artworks.py` already records.

**(d) Misremembered death dates.** Worth a check because it is nearly free and
because our own `js/artists-*.js` death years are unaudited. It will not move any
of the seven — their dates are not in doubt — but it may correct an artist
wrongly excluded near the boundary. **Reach: possibly one or two artists, and
they would be borderline cases needing care, not headline names.**

## 2.4 Routes that turn out to be dead ends — named so nobody re-opens them

- **"It's on Wikipedia."** Part 0. The most dangerous of these because it looks
  like a source.
- **Low resolution / thumbnails.** Using a small image is not a defence. It is
  one factor inside somebody else's fair-use analysis, not a licence.
- **Attribution as a substitute for permission.** Crediting an artist does not
  create a right to reproduce. Attribution discharges a licence condition where a
  licence exists; it does not create one.
- **"Educational" or "non-commercial" framing.** Not a status Pigment can rely
  on, not a licence, and not stable over the project's life.
- **Museum open-access as a copyright grant.** §2.2 — it releases the
  photography, not the artwork.
- **De minimis / incidental inclusion.** Does not fit a product whose entire
  purpose is to present the artwork as the subject.
- **Fair use / fair dealing reasoned by us.** Pigment could in principle have its
  own rationale for some uses. **Nobody on this team, including me, is qualified
  to construct one**, and doing so informally is how projects acquire risk they
  cannot see. If this is ever wanted, it needs a qualified human, not an agent.

## 2.5 What is realistically available for post-1955 work

Plainly: **very little, and nothing that changes the seven Tier 1 arcs.**

- Freedom of panorama: a small number of public murals at best, possibly none
  after per-country tests. Not Picasso, Warhol, Rothko, Pollock or Matisse.
- Deliberate free licensing: the only clean route, and the estates concerned are
  the least likely to have taken it. Expect zero of the seven; possible for
  others.
- US formalities: the most likely to yield *something*, per work, at real
  research cost, and US-only.
- Everything else: dead ends.

**The current `died ≤ 1955` rule is not what is keeping those seven artists
imageless. Copyright is.** Loosening the rule would not produce images; it would
only produce images sourced on weaker grounds. The honest framing for the owner
is that the generative-cover and no-image states are not a workaround being
applied while a better answer is found — for these artists they *are* the answer,
unless an estate has affirmatively licensed a specific work.

---

## RECOMMENDATIONS

**What I would recommend the owner decide.**

1. **Repair `tools/audit_artworks.py:86` before any promotion from the pool.**
   Require artist evidence **and** work evidence, and read Commons `ObjectName` /
   `Artist` rather than the filename alone. This is the root cause of both the
   eight previously-found mismatches and the ~20 candidates here.
2. **Treat the 20 CC-licensed pool entries as a separate decision**, not as part
   of a bulk promotion. Either replace them with public-domain alternatives or
   decide deliberately how Pigment discharges attribution and share-alike.
3. **State the `/wikipedia/commons/` versus `/wikipedia/en/` rule explicitly in
   `PIGMENT.md` §14.** It is currently enforced by a schema rule and a code
   comment; it deserves to be a stated rule because it is the check that
   prevents the Part 0 failure.
4. **If modern coverage is genuinely wanted, fund the estate-licensing enquiry
   (§2.2) and nothing else.** It is the only route whose positive result is a
   document.
5. **Route anything ambiguous to qualified human review.** Specifically: the
   photograph-of-a-public-domain-painting question behind the 20 CC entries, the
   two `ita-mibac` files, and any fair-use reasoning of any kind.

**What I would not attempt.**

- I would not harvest any image from a Wikipedia non-free/fair-use page.
- I would not construct a fair-use rationale for Pigment.
- I would not loosen or reinterpret the `died ≤ 1955` rule to admit modern work.
- I would not promote any pool entry into `js/catalog-*.js` on the strength of
  the current exact-work check.
- I would not describe any record in this atlas as cleared or verified for use.

## STATE OF VERIFICATION

Complete: pool reconstruction (413/413), URL resolution (413/413), Commons
licence assertions (413/413), death-date cross-check (141/141).

Incomplete at time of writing: **18 of 20 candidate mismatches are labelled
UNVERIFIED** — flagged by metadata, not yet confirmed against the Commons file
page. A9 (Xu Beihong / Muybridge) and C3 (Hiroshige composite) are confirmed.
Group E is unresolvable from metadata and needs human eyes. The automated pass
over-flags on translated titles and series members, so **some UNVERIFIED rows
will turn out to be correct images** — C3 already came back more nuanced than
the flag suggested.

No data file was modified. Validator not re-run because nothing was touched.
