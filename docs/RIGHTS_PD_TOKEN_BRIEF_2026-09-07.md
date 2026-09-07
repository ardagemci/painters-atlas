# The `pd` token on credit-required files — refreshed and source-verified

**Written for the owner. Not legal advice. No determination is made here.**
Supersedes the sourcing (not the structure) of
`protocol/tasks/RIGHTS-001/evidence/hogarth-01-pd-token.md`. Produced via a
Lane IV dual-model session (`protocol/duo-sessions/rights-pd-token/`) — Opus 5
and Astra 6 independently verified every citation the original brief flagged
as "from general knowledge, not fetched," then cross-checked each other's
findings. OD-5 binds this document exactly as it bound the one it updates:
asserted basis and residual uncertainty, never clearance, no option ranked.

## What changed since the original brief

**The record count is five, not six or seven.** Two of the original seven
have since been re-sourced onto files that assert a PD-Art basis directly,
independent of this brief:

| Record | Current basis | How verified |
|---|---|---|
| `the-ten-largest-no-9` (af Klint) | **PD-Art (PD-old-70).** Photographer named separately and correctly: Albin Dahlström, not af Klint. | Commons file page fetched directly, 2026-09-07 |
| `triumph-of-death` (Bruegel) | **PD-Art + CC0.** | Commons file page fetched directly, 2026-09-07 |

Both match git history (`feat(rights): Decision B executed — af Klint
re-sourced onto a PD-Art file`, and a second, separate re-sourcing the
original brief's provenance note already flagged). Neither needs further
action under this brief; both are recorded here because the count they were
part of is what "six" and "seven" have meant in this task's record.

**The German legal position needs a correction, not just a citation.** The
original brief cited the 2018 Bundesgerichtshof decision (real citation,
confirmed: *Museumsfotos*, BGH, 20 December 2018, I ZR 104/17, holding under
§72 UrhG that museum photographs of PD paintings can receive
related-rights protection) as Germany's live position, diverging from the US
*Bridgeman* line. **Current §68 UrhG** — fetched directly from
[gesetze-im-internet.de](https://www.gesetze-im-internet.de/urhg/__68.html) —
now reads: *"Vervielfältigungen gemeinfreier visueller Werke werden nicht
durch verwandte Schutzrechte nach den Teilen 2 und 3 geschützt"* ("Reproductions
of public-domain visual works are not protected by the related rights
covered in Parts 2 and 3"). The legislative materials for that amendment name
the 2018 case directly. This narrows, rather than erases, the earlier
citation: §68 addresses the *related-rights* protection *Museumsfotos*
was decided under: it does not resolve every question a full copyright claim
might raise, and neither this section nor the amendment establishes anything
about the specific photographers or files below.

**The other two citations check out as originally stated:**
- *Bridgeman Art Library, Ltd. v. Corel Corp.*, 36 F. Supp. 2d 191, 197
  (S.D.N.Y. 1999) — a federal **district court** decision, not appellate or
  Supreme Court. [Opinion text](https://chnm.gmu.edu/digitalhistory/links/pdf/chapter7/7.52.pdf).
- Directive (EU) 2019/790, Article 14 — confirmed verbatim: reproductions of
  a visual-art work whose copyright term has expired are "not subject to
  copyright or related rights, unless the material resulting from that act of
  reproduction is original in the sense that it is the author's own
  intellectual creation." [Full text](https://eur-lex.europa.eu/eli/dir/2019/790/oj/eng).

## The five records, current state (fetched directly, 2026-09-07)

| Record | Licence asserted | Named photographer | PD-Art tag? |
|---|---|---|---|
| `black-fuji` | CC BY 3.0 | Sailko | No |
| `david` | CC BY 3.0 | Jörg Bittner Unna | No |
| `pieta` | GFDL 1.2+ / CC BY-SA 3.0 / CC BY 2.5 (uploader's choice among these, not cumulative obligations) | Stanislav Traykov | No |
| `little-dancer-aged-fourteen` | CC BY 2.0 | Regan Vercruysse | No |
| `vahine-no-te-tiare` | CC BY-SA 4.0 | Francesco Bini (Sailko) | No |

All five: a living, named photographer's own licence, no PD-Art assertion
alongside it, and (for the flat works — `black-fuji`, `pieta`,
`vahine-no-te-tiare`) the painter is correctly *not* named as photographer in
any of them, contrary to what the original brief's "tell in the evidence"
worried about for the two files then in this set. That specific concern no
longer applies to any of the current five.

## The options — unranked, the owner ranks

**A. Change nothing.** Costs: the schema/doc contradiction the original
brief described stays open, now against five records instead of seven.
Improves: nothing. Costs nothing today.

**B. Add a fourth `image.status` value** (e.g. `"licensed"`): renders,
credit mandatory. Unchanged from the original brief — schema, validator,
`js/app.js` and five record edits; Lane I or II work, not Hogarth's or this
session's to execute.

**C. Move the five to `"copyright"`.** Unchanged: five images stop
rendering, for an obligation nobody has asserted against Pigment
specifically.

**D. Re-source, per file, where a suitable PD-Art alternative exists —
otherwise retain the current file with the uncertainty documented.**
Revised from the original brief's "re-source the four flat files, leaving
three [sculptures] no substitution can help": whether a PD-Art-tagged
alternative exists for any of these five files has not actually been checked
file-by-file, for either the sculptures or the remaining flat works. The
claim that no substitute exists for a photographed sculpture was an
assumption in the original brief, not a finding — a photographer choosing to
license under CC does not establish that no other photographer has released
an image of the same object under a public-domain-compatible basis. This
option is therefore two things, not one: **D1** re-source where a check finds
an alternative; **D2** retain with documented uncertainty where it doesn't.
Both are real, distinct choices the owner can make per file, or as a
standing policy for this class of record.

## What we still don't know

Everything the original brief listed, unchanged: which country's law
governs the owner's exposure; whether Commons' thumbnail serving counts as
adaptation; what a valid CC BY/BY-SA attribution notice must contain
relative to what `js/photo-credits.js` renders. Added by this round: whether
a PD-Art-tagged alternative photograph exists for any of the five files
(unchecked, not "none exists"), and whether Pieta's three co-offered
licences impose different or overlapping obligations (not analyzed here).

## Provenance

Debated and verified 2026-09-07 by Opus 5 (Claude) and Astra 6 (Codex) under
Lane IV (CLAUDE.md/AGENTS.md §1b), 2 rounds. Full transcript:
`protocol/duo-sessions/rights-pd-token/transcript.md`. Every Commons file
page cited above was fetched directly during this session, not carried over
from the original brief or from training-data recall.
