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

**Wikipedia says this itself, in terms.** Its own reuse guidance states that
*"what is fair use for Wikipedia may not be considered a fair use for your
intended use of the content in another context"*, warns reusers that this may
apply *"if you were using a Wikipedia article for a commercial use"*, notes that
fair use is primarily a US doctrine that may not exist in other jurisdictions,
and puts the burden squarely on the reuser: *"It is the responsibility of the
reuser to determine how a license applies to the intended reuse."* We would not
be finding a loophole in Wikipedia's policy; we would be doing the specific thing
its policy tells us not to do.

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
*The Beaneater*, *Le Verrou* / *The Bolt*, *Der Turm der blauen Pferde* / *The
Tower of Blue Horses* and roughly two dozen others surfaced as candidates and are
**correct images**. It also cannot distinguish a series from its members
(Piranesi's *Vedute di Roma* represented by *The Colosseum*; Géricault's
*Portraits of the Insane* by *Portrait of a Kleptomaniac*). Those were removed by
inspection before the shortlist below. **Nothing below is asserted as a mismatch
that has not had its file page read.**

## 1.6 Confirmed mismatches — 20 of 413

Status values: `CONFIRMED MISMATCH` — file page read, depicts something other
than the claimed work · `MATCH CONFIRMED` — file page read, does depict the
claimed work · `UNRESOLVED` — checked, evidence insufficient.

**All twenty shortlisted candidates were checked against their Commons file
page, and all twenty are confirmed defects.** None turned out to be a false
alarm; one (C3) changed character on inspection. The shortlist was drawn from
~70 machine-flagged candidates after translated titles and series members were
removed by hand.

### Group A — Commons attributes the file to a *different artist*

**All nine confirmed against the Commons file page.**

| # | Record | What the file page states it is | Status |
|---|---|---|---|
| A1 | `ogata-korin` :: Irises (Kakitsubata-zu) | **Van Gogh**, *Irises*, 1889, oil on canvas, Getty Center | **CONFIRMED MISMATCH** |
| A2 | `berthe-morisot` :: Young Woman Powdering Her Face | **Georges Seurat**, *Young Woman Powdering Herself*, 1888–90, Courtauld | **CONFIRMED MISMATCH** |
| A3 | `amedeo-modigliani` :: Portrait of Chaim Soutine | **Chaïm Soutine**, *View of Céret*, 1922 — a landscape *by* the sitter | **CONFIRMED MISMATCH** |
| A4 | `claude-lorrain` :: The Enchanted Castle | **Francis Danby**, *The Enchanted Castle*, c. 1841, V&A FA.66(O) | **CONFIRMED MISMATCH** |
| A5 | `rachel-ruysch` :: Flower Still Life | **Amalie Kärcher** (1819–87), *A Flower Still Life with Grapes*, 1857 | **CONFIRMED MISMATCH** |
| A6 | `seker-ahmed-pasha` :: Forest (Woodland Scene) | **Paul Cézanne**, *Forêt*, c. 1902–04, National Gallery of Canada | **CONFIRMED MISMATCH** |
| A7 | `sesshu-toyo` :: Winter Landscape | **Christian David Gebauer**, *Winter Landscape with Brabrand Church*, 1831, ARoS | **CONFIRMED MISMATCH** |
| A8 | `reza-abbasi` :: Portrait of a Dervish | *Portrait of the artist Reza 'Abbasi* **by Mu'in Musavvir**, 1676 — a portrait *of* him, by his student | **CONFIRMED MISMATCH** |
| A9 | `xu-beihong` :: Galloping Horse | Animated GIF from **Muybridge**'s *Animal Locomotion* (1887); not a painting | **CONFIRMED MISMATCH** |

Each of these renders on an artist page today as that artist's work. A2 shows a
Seurat under Morisot's name; A6 shows a Cézanne as an Ottoman painting; A7 shows
a Danish oil as a 15th-century Japanese ink landscape; A1 shows Van Gogh's
*Irises* as Ogata Kōrin's screen. A3 and A8 share a distinct mechanism — the
file depicts or was made by the *person named in our title*, so the sitter's name
carried the match.

### Group B — right artist, but Commons names a *different work*

**All eight confirmed against the Commons file page.**

| # | Record | What the file page states it is | Status |
|---|---|---|---|
| B1 | `hans-holbein` :: Portrait of Henry VIII | *Portrait of **Anne of Cleves***, c. 1539, Louvre — right painter, wrong sitter | **CONFIRMED MISMATCH** |
| B2 | `nicolas-poussin` :: The Four Seasons | *Self portrait of Nicolas Poussin*, 1650, Louvre INV 7302 | **CONFIRMED MISMATCH** |
| B3 | `lucas-cranach` :: Adam and Eve | *Portrait of Princess Sibylle of Cleve*, 1526, Schlossmuseum Weimar | **CONFIRMED MISMATCH** |
| B4 | `george-stubbs` :: Horse Attacked by a Lion | *Self-portrait*, 1781, **enamel on Wedgwood plaque**, NPG 4575 | **CONFIRMED MISMATCH** |
| B5 | `paula-modersohn-becker` :: Self-Portrait at Sixth Wedding Anniversary | *Old poor woman with a glass ball and poppies*, 1907 | **CONFIRMED MISMATCH** |
| B6 | `mihri-musfik` :: Self-Portrait | *Leyla Turgut Portresi*, 1911–12, pastel on paper — a named sitter, not the artist | **CONFIRMED MISMATCH** |
| B7 | `lyubov-popova` :: Textile designs, First State Factory | *Composition*, 1917, gouache on paper — a Suprematist work predating her 1923 textile work | **CONFIRMED MISMATCH** |
| B8 | `gustave-moreau` :: Oedipus and the Sphinx | *Étude pour la tête d'Œdipe*, c. 1860, **pencil and white chalk** — a preparatory drawing | **CONFIRMED MISMATCH** |

**Four of these eight are self-portrait confusions** (B2, B4, B5, and B6 in the
reverse direction — a named sitter standing in for a self-portrait). That is the
same failure the brief describes from the previous audit, and the mechanism is
plain: `self` and `portrait` appear in almost every painter's title list, so
under the line-86 rule any self-portrait file matches almost any portrait record,
and vice versa.

Note also that B4 and B8 are not paintings at all — an enamel plaque and a pencil
drawing — and would misrepresent the medium even if the work were right.

### Group C — not a reproduction of the work at all

**All three confirmed against the Commons file page.**

| # | Record | What the file page states it is | Status |
|---|---|---|---|
| C1 | `kurt-schwitters` :: Ursonate | a **photographic portrait of Schwitters** by Genja Jonas (1895–1938), published 1927 | **CONFIRMED MISMATCH** |
| C2 | `emily-carr` :: Big Raven | a **1971 Canadian postage stamp** that reproduces *Big Raven* | **CONFIRMED MISMATCH** |
| C3 | `utagawa-hiroshige` :: One Hundred Famous Views of Edo | a **side-by-side composite** of Hiroshige's *Evening Shower at Atake* and Van Gogh's 1887 oil copy | **CONFIRMED MISMATCH — partial** |

C1 is a photograph *of the artist*, by a named photographer, standing in for a
sound poem — a work that has no visual form to reproduce at all.

C2 does depict the claimed painting, but as a **postage stamp**, which
`PIGMENT.md` §14 names explicitly among the things an image must not be
("souvenir … reproduction object"). It carries a second problem the metadata
scan would not have caught: a 1971 stamp design is a separate later work with
its own rights position, layered over a painting whose own status is a separate
question.

C3 is subtler than the automated flag suggested. The image contains **both**
works side by side — Hiroshige's print *and* Van Gogh's *Bridge in the Rain,
after Hiroshige* (Van Gogh Museum). The claimed work is present, so this is a
§14 "exact artwork / full composition" failure rather than a wrong-artist one.
**It is the case that justified reading every file page rather than trusting the
metadata scan**, and the only one of the twenty whose character changed on
inspection.

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
- **Wrong-image rate: 20 confirmed in 413 (4.8%)**, plus 10 further §14
  rendering defects (Group D) — about **7% of the pool is unusable as it
  stands**. The errors concentrate exactly where the line-86 rule is weakest:
  generic titles, self-portraits, series, and titles naming a person.
- **Licence obligations: 20 entries** are CC BY / CC BY-SA, not public domain.
  These are a *different* 20 with only partial overlap.
- **Group E remains unresolvable from metadata** — serial-numbered filenames
  needing a human to look at the image. `jan-steen :: The Merry Family` is the
  most doubtful of them.
- **Therefore Direction A's "close to mechanical" Tier 2 promotions are not
  mechanical.** A 120-record promotion made on the strength of the current
  tooling would be expected to carry **roughly six wrong images and three more
  with attribution obligations** into the catalog — where, unlike the artist
  pages they sit on now, they would acquire canonical URLs, coordinates, and
  entry into lists, the deck and the daily painting.

The last point is the one I would press. These 20 wrong images are already
visible on artist pages today. Promotion does not create the defect; it
multiplies its surface area and makes it much more expensive to withdraw, since
shipped artwork slugs are permanent (`ARTWORK_SCHEMA.md` §2).

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

## 2.1 Freedom of panorama — *real, and it splits by jurisdiction rather than resolving*

I revised this section after research. My first draft said freedom of panorama
covers only buildings and sculpture and does nothing for painting. **That is
wrong for the case that matters most here**, and the correction is the most
substantive result in Part 2.

**What it permits.** Many countries allow works **permanently sited in, or
visible from, public places** to be photographed and reproduced without the
rights holder's consent. Coverage of *two-dimensional* work varies but is not
uniformly excluded:

- **Mexico** permits *"reproduction, communication and distribution by means of
  drawings, paintings, photographs and audiovisual processes of works that are
  visible from public places"* — commercial use included, with "public place"
  read broadly enough to include indoor venues open to the public. Commons
  treats this as an acceptable freedom-of-panorama regime.
- **Brazil** likewise permits reproduction of works permanently displayed in
  public places, commercial use included.
- **Switzerland** permits images of murals and graffiti, provided they cannot be
  used for the same purpose as the original.
- **France and Sweden exclude commercial use**; **Australia** covers sculpture
  and artistic craftsmanship but *not* murals or graffiti.

**This is live, not theoretical.** Commons hosts photographs of Siqueiros's
murals — including *La Marcha de la Humanidad* at the Polyforum — under a
freedom-of-panorama template that states plainly that the subject is *"a
copyrighted architecture and/or artistic work permanently located in or visible
from a public space in a country that provides Wikimedia Commons-acceptable
freedom of panorama."* Note what that template concedes: **the mural is still
copyrighted.** The file is hosted because of where the work stands, not because
the work is free.

**What it forbids, and the catch that decides the matter.** **United States
freedom of panorama, 17 U.S.C. § 120, covers *architectural works only*.** It
does not extend to murals, sculptures or monuments. So a photograph of a Mexican
mural can be lawfully free in Mexico and simultaneously an infringing
reproduction in the United States.

That is not a technicality for Pigment. It means the resulting status is
**jurisdiction-split**: true where the work stands, false in a country where a
static public website is plainly reachable. Every existing `status:"pd"` record
in this atlas rests on a claim intended to hold generally; a panorama-sourced
record would rest on a claim known not to hold in at least one major
jurisdiction. **Those are different kinds of record and should not share a
rendering token.**

**It also does nothing for easel painting**, which is nearly the whole atlas. A
canvas hanging in a museum is not permanently sited in a public place in the
relevant sense. Kahlo painted easel works; so did Picasso, Rothko, Pollock,
Warhol, Matisse and Dalí in the works Pigment names.

**Evidence needed per work:** that it is permanently sited; that it sits in a
public place as that statute defines it; that the provision covers murals and
not only architecture; that it permits commercial use; a photograph the
photographer has actually freely licensed; and an explicit decision about the US
position.

**Reach: the Mexican muralists, and essentially nobody else.** Concretely that
means Rivera (d. 1957) and Siqueiros (d. 1974) — Orozco (d. 1949) is already
inside the atlas's own cutoff. `muralism` currently has exactly one artist. So
this route plausibly unlocks **images for one to two artists' public murals**,
none of them among the seven Tier 1 names, and each carrying a US position that
would need a qualified opinion.

**Residual risk: moderate-to-high, and of an unusual shape** — not "we might be
wrong" but "we would be knowingly right in one country and wrong in another."
That is an owner decision, not a data-steward decision, and I am escalating it
rather than recommending it.

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

**What it does *not* cover, and this is the common misreading — now checked.**
**Museum open-access programmes release the museum's photography, not the
artists' copyrights**, and the museums say so themselves:

- **The Met** applies CC0 to images of works *"it believes to be in the public
  domain"*. Its own FAQ states that not every image on its site is open access —
  *"works by contemporary artists or those created more recently might still be
  under copyright."* Separately it releases *catalogue data* for the whole
  collection, in-copyright works included. **Data is not an image.**
- **The Rijksmuseum** permits free commercial reuse of reproductions of public
  domain objects, but states that where a copyright holder is listed, copyright
  still applies, and that photographs of objects still under copyright are not
  freely available.
- **The Getty** released 88,000+ images under CC0 — again, its own photography
  of works it treats as public domain.

So open access is enormously valuable for pre-1955 work — it is, in effect, the
supply behind the atlas's existing 385 public-domain assertions — and close to
worthless for the seven. **Anyone scoping this should expect the museum
open-access route to return zero Picassos**, by design rather than by oversight.

**Evidence needed per work:** the specific licence, the specific work it covers,
identification of the grantor and a reason to believe they held the right, and
the grant's date and permanence.

**Reach: I searched for a major modern painter's estate that has free-licensed
its artist's work, and found none.** That is a negative result from a limited
search, not proof of absence — but it is consistent with the known posture of the
Picasso Administration, the Warhol Foundation, the Dalí and Gala-Dalí
foundations, and the Matisse, Rothko and Pollock-Krasner estates, all of which
run *active licensing* programmes. Active licensing is the commercial opposite of
free release. **My honest expectation is that this route unlocks none of the
seven.**

**It is nevertheless the route I would pursue if any**, because it is the only
one whose positive result is a **document** rather than an inference, and because
the cost of asking is an email. It may also unlock 20th-century names outside
that list — a living or recent artist with a personal reason to want their work
seen is a much better prospect than a blue-chip estate.

## 2.3 Public domain by routes other than the death date

Several genuine mechanisms, of very different value.

**(a) US formalities — the strongest of these, and genuinely substantial.**
Works published in the US before 1929 are out of copyright there. For works
published 1929–1963, US law required a **renewal** filing in the 28th year, and
the great majority never happened: of roughly 642,000 copyrights registered in
that window only about 25% were renewed, and a 1961 Copyright Office study put
renewals below 15%. Separately, **works published without a copyright notice
between 1923 and 1977 forfeited protection outright.** For an American-published
work this can produce public-domain status in the US regardless of when the
artist died. Pollock, Rothko and Warhol are American, so this is where it would
bite if anywhere.

*But three things blunt it, and they blunt it hard for paintings:*

1. **It turns on "publication," a term of art that fits paintings badly.**
   Exhibiting a canvas in a gallery is not clearly publication. Whether a
   reproduction in an exhibition catalogue published the *work*, and with what
   notice, is a contested per-work factual question. The renewal statistics above
   are drawn overwhelmingly from **books**, where publication is unambiguous —
   quoting them at a painting is a category error and I flag my own use of them
   as indicative only.
2. **It yields a US-only status.** The work may remain in copyright in Europe on
   the ordinary life+70 arithmetic. Same jurisdiction-split problem as §2.1.
3. **The research is per work and archival** — a renewal-record search plus
   evidence about the first publication event.

**Evidence needed:** the publication event and its date, the presence or absence
of notice, and a renewal search. **Reach: unknown without per-work research, and
I will not estimate it.** Plausibly a handful of *specific images* — a magazine
reproduction, a poster, an exhibition catalogue plate — rather than any artist's
body of work. Note what that yields even on success: often a *reproduction* of
the painting, not a good image of it.

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

Routes ranked by what they actually unlock:

| Rank | Route | What it unlocks | Confidence |
|---|---|---|---|
| 1 | **Freedom of panorama (Mexico/Brazil-type regimes)** | public **murals** of Rivera and Siqueiros — 1–2 artists, none of the seven; images demonstrably exist on Commons today | High that files exist; **the US position is the open question** |
| 2 | **US formalities (non-renewal / no notice)** | possibly a handful of specific published reproductions; US-only | Unknown — needs per-work archival research |
| 3 | **Deliberate free licensing** | probably nothing from the seven's estates; possibly other 20th-c. names | Low for the seven; **the only route whose success is a document** |
| 4 | Corrected death dates | at most 1–2 borderline artists, no headline names | Low value, near-zero cost |
| — | Everything in §2.4 | nothing | Dead ends |

**The `died ≤ 1955` rule is not what is keeping those seven artists imageless.
Copyright is.** Loosening the rule would not produce a single image; it would
only produce images sourced on weaker grounds. Not one of the four routes above
reaches Picasso, Dalí, Kahlo, Pollock, Rothko, Warhol or Matisse — the muralist
route is the only one that clearly works, and none of the seven painted public
murals.

So the honest framing for the owner is this: **the generative-cover and
no-image states are not a stopgap being tolerated until someone finds the real
answer. For these seven artists they are the answer**, unless a rights holder
affirmatively licenses a specific work. The atlas's modern gap is a fact about
copyright law, not a gap in our research or our nerve.

One thing genuinely did change on investigation, and it is worth the owner's
attention: **the muralists are reachable in a way I did not expect**, and
`muralism` is a movement the curator already flagged as having exactly one
artist. That is a real, small, concrete opportunity — and it comes attached to a
jurisdiction split that needs a qualified human answer before anything ships.

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
4. **Decide the muralist question deliberately, or not at all (§2.1).** The
   images exist on Commons under a template that says the work is still
   copyrighted and free only where panorama applies. If the owner wants Rivera
   and Siqueiros, that needs a qualified opinion on the US position **and** a
   distinct `image.status` token, because it is not the same kind of claim as
   the atlas's existing `pd` records. If he does not want to fund that opinion,
   the right answer is to leave it, and I would not treat that as a loss.
5. **If broader modern coverage is wanted, fund the estate-licensing enquiry
   (§2.2) and nothing else.** It is the only route whose positive result is a
   document. Expect it to come back empty for the seven.
6. **Route anything ambiguous to qualified human review.** Specifically: the
   photograph-of-a-public-domain-painting question behind the 20 CC entries, the
   two `ita-mibac` files, the US position on panorama-sourced murals, and any
   fair-use reasoning of any kind.

**What I would not attempt.**

- I would not harvest any image from a Wikipedia non-free/fair-use page, under
  any framing, for any purpose.
- I would not construct a fair-use rationale for Pigment. Neither I nor anyone
  else on this team is qualified to, and an informal one is worse than none
  because it creates confidence without protection.
- I would not loosen or reinterpret the `died ≤ 1955` rule to admit modern work.
  The research gives no reason to, and the rule is not what is causing the gap.
- I would not add panorama-sourced murals under the existing `pd` token, even
  though the files are sitting on Commons right now and it would be easy.
- I would not promote any pool entry into `js/catalog-*.js` on the strength of
  the current exact-work check.
- I would not describe any record in this atlas as cleared or verified for use.

## SOURCES

Repository, read directly this session: `js/artworks.js`, `js/catalog-1..4.js`,
`js/artists-1..17.js`, `tools/audit_artworks.py`, `tools/commons_rights.py`,
`tools/fetch_artworks.py`, `PIGMENT.md` §14, `docs/ARTWORK_SCHEMA.md`,
`docs/ATLAS_COVERAGE.md`, `protocol/tasks/PIG-001/owner-decisions-r2.md`.

Wikimedia Commons API (`action=query&prop=imageinfo&iiprop=extmetadata`), 413
files, 2026-08-06 — the licence, `ObjectName`, `Artist` and `Restrictions`
assertions in §1.3, and the file pages confirming all 20 mismatches in §1.6.

Web, per claim class:

- **Fair use does not transfer** — `en.wikipedia.org/wiki/Wikipedia:Reusing_Wikipedia_content`,
  and `Wikipedia:Non-free_content_criteria`. Basis for Part 0's quotations.
- **Freedom of panorama, scope and country variation** —
  `commons.wikimedia.org/wiki/Commons:Freedom_of_panorama/Europe` and
  `/Americas`; `Commons:Copyright_rules_by_territory/Mexico` for Mexico's
  life+100 term and its panorama provision.
- **Panorama in practice** — `commons.wikimedia.org/wiki/Category:Polyforum_Cultural_Siqueiros`,
  for the template wording conceding the murals remain copyrighted.
- **US panorama limited to architecture** — 17 U.S.C. § 120.
- **Museum open access covers only works believed public domain** — The Met's
  image-resources and open-access policy pages; the Rijksmuseum's information
  and data policy; the Getty CC0 release.
- **US renewal and notice** — `en.wikipedia.org/wiki/Copyright_renewal_in_the_United_States`
  and NYPL's 1923–1964 copyright history. **Renewal percentages there describe
  books, not paintings**, and are cited as indicative only.

**Negative result, recorded as such:** a search for a major modern painter's
estate that has released work under a free licence returned nothing usable. That
is a limited search, not proof of absence.

## STATE OF VERIFICATION

Complete: pool reconstruction (413/413), URL resolution (413/413), Commons
licence assertions (413/413), death-date cross-check (141/141), and
**file-page confirmation of all 20 shortlisted mismatches (20/20)**.

Deliberately not attempted, and left for a human:

- **Group E** — 7 records whose Commons filename is a serial number and whose
  metadata says nothing. These need someone to look at the image. No amount of
  metadata will settle them.
- **The remaining ~340 pool entries were screened, not individually eyeballed.**
  The screen tests our artist and title against Commons' own `ObjectName`,
  `Artist` and `ImageDescription`. It would not catch a file that carries the
  right title and artist in its metadata but reproduces a different version,
  a copy, or a later replica — so **4.8% is a floor on the error rate, not a
  measurement of it**.
- **The atlas's own death years were not audited against an external source.**
  They are the input to every public-domain assertion in the pool and they have
  never been checked.
- **No legal question was resolved**, by design: the photograph-of-a-flat-artwork
  question, the two `ita-mibac` files, and every route in Part 2.

No data file was modified in this pass; no image was added, replaced or
promoted. The validator was not re-run because nothing it validates was touched
— the last recorded run, in `ATLAS_COVERAGE.md`, reported `ALL REFERENCES VALID`
and that remains the state of the tree.
