# Tooling repairs following commit f445a4d

**Author:** Dürer (Implementation Lead). **Branch:** `main`. **Not pushed.**

Four bounded repairs to the image-matching tooling, plus one defect found on the
way that was not in the brief. Read `f445a4d-false-test-claim.md` first: two of
these exist because that commit shipped an earlier draft and asserted a test
result nobody had seen.

Every claim below was re-run rather than inherited. Where a verdict line matters,
it is quoted whole, because quoting the run count instead of the verdict is the
exact mistake this file follows.

## Suite verdict, before and after

```
before:  Ran 44 tests in 0.518s     after:  Ran 44 tests in 0.513s
         FAILED (failures=2)                OK
```

Validator, after:

```
ALL REFERENCES VALID
```

---

## Repair 1 — `main` was carrying an earlier draft

`f445a4d` committed a work-in-progress copy of `tools/audit_artworks.py` (522
lines). The author's final version (529 lines) was sitting in the worktree at
`.claude/worktrees/cranky-grothendieck-ad5fbf/`. That version is now on `main`.
`tools/commons_rights.py` was byte-identical in both and needed no adoption.

Three things the final version has that the draft did not, all kept intact:

1. **Two alias entries deleted, not lost.** `annibale-carracci::The Beaneater`
   and `john-constable::Cloud Studies` no longer need `TITLE_ALIASES` rows,
   because the check now folds word-spacing and English plurals itself. A
   comment above the table says so, which is what stops someone re-adding them.
2. **A sharper contract on `meta`.** Metadata that failed to load must not reach
   `match_verdict` at all. An empty dict reads as "unconfirmed", which a caller
   may accept; a request that timed out proves nothing and must produce no
   verdict of any kind. Both callers skip the candidate and set `unverified`.
3. **A refusal to read `ImageDescription`.** Prose about the right painting is
   not evidence that this file is it. The Emily Carr postage stamp's description
   reads "the stamp depicts Carr's painting Big Raven" — consulting it would
   confirm the very file §14 excludes.

**Verified directly, against live Commons metadata, not taken on report:**

| file offered as | verdict |
| --- | --- |
| `Irises-Vincent_van_Gogh.jpg` as Ogata Kōrin, *Irises (Kakitsubata-zu)* | `rejected` |
| the same file as Vincent van Gogh, *Irises* | `confirmed` |
| `Muybridge_race_horse_animated_184px.gif` as Xu Beihong, *Galloping Horse* | `rejected` |

The two deleted aliases were checked separately: *The Beaneater* against Commons'
`The Bean Eater`, and *Cloud Studies* against `Cloud Study`, both `confirmed`
with no alias row present. Removing them cost nothing.

## Repair 2 — the red suite, and what was actually causing it

Two failures, both in `TestProseLanguage`, both pre-existing, and they had **two
different causes** — the brief named only the first.

**Cause A — `test_no_artifact_of_ours_asserts_a_legal_conclusion`.**
`docs/IMAGE_RIGHTS_ROUTES.md:17` and `:551` contain phrases OD-5 bans, and both
contain them *in order to argue against them*: line 17 quotes the rejected
`CLEARED` label to show a reader could not tell one sense of it from the other,
and line 551 states the flat jurisdictional assertion in order to show it has no
single truth value. That is the case the guard's docstring reserves the marker
form for.

Applied as `<!-- OD5-EXEMPT: … -->`, an HTML comment: it satisfies the guard,
which reads the source line, and renders as nothing at all, which a bare token in
body prose would not. Blockquoting was the wrong instrument here — in this
project a blockquote preserves a superseded claim beside its correction, and
neither line is superseded.

Both markers were pinned in `EXPECTED_EXEMPTIONS` with their justification. This
file is pinned at one too, since it spells the marker out once above; it exempts
no phrase of its own, and the pin is where you can check that.
**No pattern was widened and no exemption was loosened**; confirmed by
re-running the two lines through `BANNED` with the markers stripped, where both
are still caught.

**Cause B — `test_exemption_markers_are_pinned`, not in the brief.**
The pin expected one marker each in three files under
`protocol/tasks/PIG-001/evidence/`. **Those files are not on `main`.** They exist
only on the unmerged branch `pig-001-stabilization` (commits `95e5636`,
`a71e2c5`, `fb8ba6e`); `tests/test_rights_tooling.py` reached `main` without
them. So the pin has been asserting three markers no scanned file could supply,
and this test has failed on `main` since the day the test file landed — not
because of anything about prose.

The three entries were removed from the active map and their justifications
retained verbatim in a comment beside it, so that a future merge of that branch
re-adds them as a deliberate act rather than rediscovering them. A pin has to
describe the tree it runs against, or it stops being a pin.

## Repair 3 — `dump-artists.jxa.js` could not see the whole catalog

The dump looped `for(let i = 1; i <= 15; i++)`. There are **17** `js/artists-*.js`
shards. Shards 16 and 17 hold 25 artists, of which **16 also appear in
`js/artworks.js`** — so `main()` in `tools/audit_artworks.py` looked each of them
up in a dict that had never heard of them and raised a bare `KeyError`. The tool
could not run to completion, which is very likely why nobody noticed the draft on
`main` was a draft.

Replaced with a directory listing over `js/`, filtered to `artists-<n>.js` and
sorted numerically so 10 follows 9 rather than 1. An eighteenth shard is picked
up without an edit; the ceiling that went stale is gone rather than raised.

Verified: the dump now yields **256 artists**, and every id in `js/artworks.js`
resolves — the missing-key list is empty.

## Repair 4 — Commons started attaching tracking parameters and we stored them

Commons `thumburl` responses now carry `?utm_source=…`. The tool wrote them into
the catalog verbatim, which is worse than untidy: a tracking parameter in
`js/artworks.js` is sent back to the image host by every visitor's browser on
every page view. It would have become a request *this site* makes about the
people reading it.

Pigment shipped its `#/privacy` disclosure three days ago, naming exactly one
third-party host and no analytics of any kind. Left alone, this tooling would
have quietly made that page wrong — the disclosure would still be accurate about
what we intended and inaccurate about what we send.

`cr.strip_tracking()` now removes campaign and click-id parameters (the `utm_`,
`ga_`, `mc_`, `pk_`, `stm_` families plus the known exact keys) and preserves
everything else in order, so a URL that needs its query survives untouched. It is
applied at every point a URL enters stored data:

- `tools/commons_rights.py` — `rights_from_imageinfo()`, covering
  `commons_file_page` and `file_url` in the rights sidecar
- `tools/audit_artworks.py` — the pinned-file branch, the Commons search path,
  and the Wikipedia path, for both `img` and `page`

**No shipped record carries one.** A repo-wide scan of `js/`, `p/`,
`index.html` and `tools/` for `utm_`, `fbclid` and `gclid` returns nothing;
`tools/rights-cache.json` does not exist in this tree. The catalog was caught
before the next run wrote to it, not after.

## Left alone, deliberately

**The 12 undetected mismatches.** The `suspect` pre-filter flags 8 of the 20,
because the other 12 name the artist in the filename and so nothing ever asks the
matcher about them. `match_verdict` identifies all 20 when asked. Widening
`suspect` would route those 12 to re-resolution, which is the same decision as
replacing them — the owner's call, not mine. Raised, not taken.

**`.gitignore` and untracked files.** Untouched. Every commit here was made by
explicit path.
