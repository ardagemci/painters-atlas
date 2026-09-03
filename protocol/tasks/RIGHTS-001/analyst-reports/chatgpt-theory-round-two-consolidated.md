# RIGHTS-001 - ChatGPT Theory Team consolidated round-two report

Filed 2026-09-03 from `main` at `0daf575`.

This is a retrospective audit artifact, not a protocol message. It merges the
material findings from the five ChatGPT Theory Team reports that informed
`messages/003-revision.json`. It does not reproduce private reasoning, alter an
immutable message envelope, change workflow state, recommend legal reliance, or
authorize implementation.

## Reports consolidated

| Role | Function in the round | Codex task |
|---|---|---|
| THEMIS | rights-framework and OD-5 review | `01a058c4-fcae-7a71-9f1a-a6fe30a7e08c` |
| ARGUS | evidence, provenance, and confidence audit | `01a058c5-27ab-7b51-84ec-04ad2b78a4ae` |
| VERA | adversarial product-theory review | `01a058c5-523e-7cf3-9cf4-12efbb1cad86` |
| ELARA | experience, accessibility, terminology, and reader-trust review | `01a058c5-7a76-78d2-9dd6-2482f72b5f52` |
| MIRA | cross-role consolidation | `01a058ca-6c58-7403-b1f2-70bf1a5f756b` |

The source reports remain separate Codex task records. This file is their single
repository-level synthesis, not a claim that every sentence of every report was
adopted.

## Shared position

The five roles agreed that the round-one A/B/C/D owner-decision structure should
survive, that CH-1 through CH-5 required a revision, and that the response must
remain theory-only. They also agreed on these boundaries:

- distinguish the underlying work from every exact photograph, scan, thumbnail,
  procedural cover, or other media asset;
- record source assertions and residual uncertainty without turning them into a
  legal conclusion;
- make every jurisdiction-dependent question name its candidate jurisdiction or
  say `I don't know` and identify what would answer it;
- keep backend, database, scheduled review, private storage, and territorial
  runtime machinery outside RIGHTS-001;
- treat acceptance tests and registries as evidence for product outcomes, not as
  substitutes for those outcomes; and
- preserve the owner's authority over A, B, C, and D.

## Specialist contributions

### THEMIS - rights-framework integrity

THEMIS accepted the substance of CH-1 through CH-5 and supported three narrow
defenses: do not replace the literal-token ratchet with a permanent offender
count for every conditional-basis record; reject the challenge's shared-
contributor assertion; and do not infer a legal distinction from the 3D/flat
grouping.

THEMIS required tighter OD-5 language. It asked the revision to avoid blanket
incorporation of round-one text, keep a per-record register of underlying work
and exact media, attribute author and licence values to their sources, limit the
no-pixel finding to the observed runtime path, and keep counsel questions tied
to named jurisdictions.

### ARGUS - evidence and provenance

ARGUS classified the evidence rather than treating the challenge as a unit:

- **Observed:** the current guard filters the literal `status:"pd"` token, so a
  vocabulary migration can lower the count without changing an asset or source
  assertion.
- **Future requirement, not present fact:** successor guards and negative
  controls did not yet exist in the reviewed repository.
- **Source assertion:** the generated registry and census named Sailko / CC BY
  3.0 and Francesco Bini / CC BY-SA 4.0. Those records contradicted the claim
  that one contributor supplied both files, but did not independently establish
  authorship or authority.
- **Analytical grouping:** three photographs of three-dimensional works, two
  photographs of flat works, and one unnamed or conflicted media asset was a
  useful 3+2+1 evidence structure, not a demonstrated legal distinction.
- **Observed runtime fact:** the cover path had no artwork-image input or
  artwork-pixel sampling operation.
- **Unknown provenance:** the repository did not establish how its static
  palette and style assignments were created or researched.

ARGUS therefore scoped any A1 successor guard to the five A1-migrated records;
the sixth af Klint record remained governed separately by B.

### VERA - adversarial review

VERA found the first round-two draft not ready for synthesis for four material
reasons:

1. It conflated a record-scoped metadata-only capability needed by A3/B1 with
   global C3 policy for all 61 cover-backed records.
2. Its mechanical criteria could pass without showing that a reader understood
   whether Pigment displayed an artwork, a photograph or scan, a Pigment cover,
   or no image.
3. Its later language overstated the narrow no-runtime-pixel-sampling finding.
4. Its decision record did not yet carry the material CH-1, CH-2, CH-3, and CH-5
   adaptations.

VERA's central correction was constitutional as well as structural: A and B
must remain real record-level owner choices, while C remains a separate global
visual-policy choice. Presentation behavior belongs to a future OP-INTERFACE
dependency rather than an expanded OP-RIGHTS write scope.

### ELARA - experience, accessibility, and reader trust

ELARA defined metadata-only as a deliberate textual state, never an empty image
frame, loading failure, broken image, disabled record, or missing alternative
text. It must preserve title, artist, date where available, navigation, links,
and existing actions while creating no image role or image alternative text.

ELARA also required the selected treatment to follow the artwork record across
detail pages and compact or secondary surfaces. A genuinely independent
editorial cover may remain only when visible and accessible language identifies
it as the editorial surface's cover rather than the affected artwork.

The terminology recommendation was:

- `artwork` for the underlying work;
- `photograph` or `scan` for an exact media asset only when evidence supports
  that noun;
- `Pigment cover` for Pigment-made imagery; and
- `metadata-only` for a state with no image-like substitute.

Under C1 or C2, ELARA recommended the compact visible and accessible distinction
`Pigment cover - not the artwork`. Reader-comprehension testing remains separate
from qualified jurisdictional review.

### MIRA - consolidation

MIRA resolved the principal disagreement by defining one required outcome rather
than a fifth owner decision:

**Metadata-only presentation capability:** a future OP-INTERFACE capability that
can be applied either to selected records or globally. RIGHTS-001 defines the
reader outcome but authorizes no interface work.

The consolidated precedence was:

1. A3 may apply metadata-only to the five A records.
2. B1 may independently apply metadata-only to the af Klint record.
3. Either record-scoped selection takes precedence over C1/C2 for that record.
4. C otherwise remains the global policy for the 61 cover-backed records.
5. C3 applies metadata-only globally.

This preserved A, B, and C as independent owner decisions while acknowledging
the current renderer's missing capability.

## Consolidated CH-1 through CH-5 disposition

| Challenge | Consolidated disposition |
|---|---|
| CH-1 | Accept the missing metadata-only state; reject mandatory coupling of A3/B1 to global C3; record a future record-scoped OP-INTERFACE dependency. |
| CH-2 | Accept that the literal-token ratchet is gameable; require future A1-scoped successor guards and negative controls; do not count every conditional-basis record as an offender. |
| CH-3 | Accept the 3+2+1 grouping as evidence organization; reject the shared-contributor claim and any unsupported factual or legal premise about originality. |
| CH-4 | Accept only that the observed runtime path samples no artwork pixels; leave palette/style creation and research provenance unknown. |
| CH-5 | Accept fully and remove the stale task-id-conflict references from the revision. |

These dispositions were incorporated into `messages/003-revision.json` and
decision-record entries E-001 through E-005. Later Claude specialist work found
additional implementation facts recorded as E-006 through E-010. The final
synthesis therefore did not recommend convergence. This report does not replace
that later evidence or reopen the final synthesis.

## GESAM correction addendum

The Theory Team accepts Claude's correction in
`correction-to-theory-team.md`. The instruction to withdraw GESAM was based on a
failed search and was wrong. The immutable messages retain that historical error;
the correction banners and decision-record E-011 prevent it from becoming the
current project position.

### What the current evidence establishes

- The Turkish Ministry of Culture and Tourism describes collective-management
  bodies as organizations formed under FSEK Article 42 and lists **Türkiye Güzel
  Sanat Eseri Sahipleri Meslek Birliği (GESAM)** as active in the field of
  fine-art work owners, with an activity date in 1986 and an Ankara address.
  Source: [Ministry collective-management registry](https://telifhaklari.ktb.gov.tr/TR-332333/meslek-birlikleri-hakkinda.html).
- GESAM's own institutional material says it was founded in 1986, is based in
  Ankara, and follows, collects, and distributes royalties for rights its
  members authorize it to manage. These are organizational claims from GESAM,
  not proof that it represents a particular Pigment artist or intended use.
  Source: [GESAM institutional page](https://gesam.org.tr/gesam.html).
- ADAGP identifies itself as a French visual-artists' rights-management
  organization and requires applicants to check whether it manages the relevant
  artist and intended right. Source: [ADAGP licence application guidance](https://www.adagp.fr/en/online-licence-application).

### Correct theoretical consequence

GESAM is a verified organization and must not again be described as unverified,
unplaceable, or invented. Because the owner is a private individual with no
company or revenue and habitual residence remains undetermined between France
and Turkey, GESAM and ADAGP are candidate organizations for a future, separately
authorized PLATFORM investigation. Residence is a live input to that inquiry,
not proof that either organization controls a particular use.

The evidence reviewed here does **not** establish that GESAM or ADAGP represents
all or any specific one of Pigment's 61 affected artists, covers Pigment's exact
digital use, offers a blanket agreement, or is the legally required route. A
future PLATFORM task would need, for each candidate organization:

- an official repertoire check for each relevant artist or rights holder;
- the territory and exact rights managed;
- authority or reciprocal-representation evidence;
- coverage of Pigment's actual website and any future native-app presentation;
- pricing, duration, attribution, caching, sharing, promotion, and withdrawal
  terms; and
- qualified advice for each named jurisdiction where legal effect matters.

Nothing in this correction changes the four RIGHTS-001 decisions or supplies a
legal conclusion.

## Practice correction

The Theory Team adopts the evidentiary rule exposed by this incident:

> A search that returns no result is evidence about that search, not proof that
> the searched-for organization or fact does not exist.

A negative search finding must record the query, sources, territory, date, and
scope; use bounded language such as `this search did not locate`; and receive an
independent check before it removes a previously named organization or route.

## Current procedural position

RIGHTS-001 remains at `awaiting_build_approval` with
`build_authorized: false`. The final synthesis does not recommend convergence.
This consolidated report and its correction addendum request no transition,
freeze, build, merge, deployment, or owner decision.
