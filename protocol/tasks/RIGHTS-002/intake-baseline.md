# RIGHTS-002 — intake baseline

**Opened by:** owner instruction, splitting RIGHTS-001 after its final synthesis
declined to recommend convergence. **Parent:** RIGHTS-001 (`awaiting_build_approval`).
**OP:** OP-RIGHTS. **Lead:** Hogarth. **Baseline:** `8354de3`.

## Why this is its own task

RIGHTS-001 asks which basis token six records should carry, and every option in
it waits on Decision D — the jurisdiction facts, which only the owner can supply.
**This task waits on nothing.** The defect here is that Pigment's rendered
credits name the wrong parties, which is true today, is measurable, and does not
turn on which country's law applies.

It is also not confined to RIGHTS-001's six records: it reaches four more files
across the 23-entry credit-required set.

## The defect

`tools/commons_rights.py:118` — `re.sub(r"<[^>]+>", "", s)` — strips HTML from
the Commons `Artist` field. `Artist` arrives as an anchor:

```
File:Katsushika_Hokusai,…  <a href="//commons.wikimedia.org/wiki/User:Sailko" …>Sailko</a>
File:Paul_gauguin,_vahine… <a href="//commons.wikimedia.org/wiki/User:Sailko" …>Francesco Bini</a>
```

Those two records differ **only** in the text node. The regex keeps the text and
discards the `href`, which is the sole account identifier, before
`rights_from_imageinfo` writes `author`. From there the loss is permanent:
`tools/audit_artwork_rights.py:122` writes it into the census, and
`tools/build_photo_credits.py` never receives the identifier at all — so fixing
the credits builder alone cannot work.

The same line discards the `en.wikipedia.org` hrefs that would distinguish a
photographer's credit from the depicted painter's.

## What it produces, measured

**E-006 — one account, two names, four files.** `User:Sailko` is recorded as
`Sailko` on the Soutine, `black-fuji` and Rubens *Descent from the Cross* files
and as `Francesco Bini` on `vahine-no-te-tiare`. Two further account/display
divergences are latent and non-colliding today (`User:MiguelHermoso`,
`User:Glimz`).

**E-010 — the credit names the painter, not the photographer.** Both files below
are CC BY 2.0, where attribution is required:

| file | Pigment credits | page's own wikitext names |
|---|---|---|
| `Mrs._Siddons_as_the_Tragic_Muse_(3051182537).jpg` | `Joshua Reynolds` (d. 1792) | `Rennett Stowe` |
| `Max_Beckmann,_Departure.jpg` | `Max Beckmann` (d. 1950) | `Allie_Caulfield` |

A third records `Hilma af Klint` where the page names nobody; a fourth records a
16th-century miniaturist because the page itself does.

**Not a defect:** licence and version. All 23 recorded licences are
character-identical to what the pages assert today.

## The proposed fix, from Seurat

Capture the first anchor's `href` from the raw `Artist` into a new census field
`author_href` before stripping; carry it through `audit_artwork_rights.py` as a
sibling key; emit an optional `authorAccount` from `build_photo_credits.py`.
Roughly four lines. Changes no existing field, no rendered credit, and no count.

**Explicitly out of scope for the tooling:** rewriting the rendered author
string. The display text is what each file page asks for, and overriding it is
an owner decision, not a tool's.

Once `author_href` exists, a ratchet can fail the build when one account maps to
more than one recorded string — the condition that produced E-006, caught before
it ships.

## Blockers and dependencies

- **Scope.** `tools/` is **not** in OP-RIGHTS' may-write table
  (`protocol/oriented/OP-RIGHTS.md`), which names those tools only as the
  permitted route to other files. This task needs that scope widened by the owner
  or the dependency formally filed. **It is the first thing to settle.**
- **Ledgers.** Regenerating the census is a live Commons fetch, so the diff is
  not knowable offline. `TestAssetInventory` keys on image URLs rather than
  credit fields and should not move, but it fails on *any* undeclared surface
  drift, so a re-audit that also refreshes a `license_short` needs a declared
  ledger entry.
- **Not blocked by:** jurisdiction, Decision D, or anything in RIGHTS-001.

## The owner decision this task will reach

Whether a rendered credit should name what the file page displays, the account
behind it, or both. Seurat declined to choose. Whether either satisfies a given
licence version is a question for counsel, not for this task.

## Evidence

`protocol/tasks/RIGHTS-001/evidence/seurat-01-credit-integrity.md` (all 23 files
verified live, 2026-09-02, no unverified fetch);
`protocol/tasks/RIGHTS-001/evidence/durer-01-feasibility.md` §4;
`protocol/tasks/RIGHTS-001/decision-record.md` E-006, E-010.
