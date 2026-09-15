# Future steps toward the north star

**Duo session `elevate`, 2026-09-15. Claude, after a three-round debate with Codex.**
Decision inputs for the owner, not a roadmap anyone may execute without him. Every
claim below is something measured on this branch or cited to a file.

## Where Pigment stands against its own goal

PIGMENT.md §1: *"a social atlas where people discover, understand, and express
their taste in art."* §11 phases it — Atlas 2.0, then the accountless Taste
prototype (1.5), then profiles, learning, community — and §16 is unusually
blunt: **do not jump to accounts until Discover → Admire → Map → Become is shown
to be enjoyable.**

Most of Phase 1 and 1.5 is built. There is a catalog of 398 records, a Passport,
a painted shareable Passport card, a daily painting, share chips and 820
prerendered stubs. What does **not** exist is any evidence that the loop works for
someone who did not build it. Nobody has watched a stranger use it. Everything
downstream, including the social layer the owner wants, is gated on that
evidence, and the project has spent the last month producing rights findings
instead.

That is the single most important observation in this document.

## Now — unblocked, cheap, and each one decides something

**1. Run the loop study.** `docs/LOOP_STUDY_PROTOCOL.md` is ready: five
owner-led sessions, no instrumentation, anonymous labels, a results template
keyed to loop steps. Its output is a ranked list of observed obstacles, and **that
list, not another brief, should choose the next investment.** Five sessions show
usability problems. They do not show enjoyment, and the kit says so.

**2. Settle three pending adoptions.** Each is green alone and all merge cleanly
together (199 tests, validator 0 — measured):
- `duo/rights-pd-token-0350` — executes owner decisions D-010/D-011. It is merged
  into *this* branch, so adopting this branch adopts it.
- `duo/lane-iv-and-fixes-0236` — rewrites `CLAUDE.md` and the sealed set. A
  constitutional decision. See `branch-assessments.md`.
- `codex/moderna` — a homepage/artwork redesign *study*. A product-direction
  decision. Worth deciding *after* step 1, which will say whether the homepage is
  where readers actually stall.

**3. One verifier edit, owner-present.** The validator still spells the
renderability rule out inline. Its agreement test is **measurably blind** to any
regression that does not push an onboarding-deck quadrant below two works (negative
control: dropping `"licensed"` moved black-fuji out of F−D+, 47→46, and the test
stayed green). Having `tools/validate.jxa.js` evaluate `js/renderable.js`, as
`tools/build_seo.jxa.js` now does, closes that. It is a sealed file, so it is the
owner's edit to make (CLAUDE.md §0).

## Next — depends on the above

**4. IFACE-001, with evidence instead of assumption.** The Theory Team's brief is
still owed. It can now rest on `IFACE-001/evidence/cross-registry-identity.md`:
of 581 gallery entries, 173 share a Commons file with a catalog record, and
exactly one pairs a withheld record with a gallery image (*The Snail*). That one
is **latent by coincidence**. The artist page's *Major works* panel renders
`window.ARTWORKS` with no gate, and it is hidden only for artists who have a
Tier-1 arc. **166 of 196 gallery artists have none.** This is the same shape as the
rails fixed today: correct for a reason that has nothing to do with rights. The
brief's real question is whether the gallery gets a gate, and who owns it.

**5. The rights decisions still open.** RIGHTS-001 Decision C (the 61 procedural
covers) and the owner question behind Decision E (whether a credit should name
what the file page displays or the account behind it — one photographer is
currently credited as two people, and two CC BY 2.0 credits name a long-dead
painter rather than the photographer). Residence is now Türkiye (D-010), so the
counsel questions can go to one named practitioner.

**6. The loop's honest weak point.** `docs/ADMIRE_SPEC.md:100` records that the
onboarding deck is *stratified up front* and **does not adapt to answers**.
Response-adaptive delivery is a deferred promise (PIGMENT.md §19). This is the
largest product lever on "discover and express taste," and §16 lists it first:
*implement true adaptivity or revise the claim.* Step 1 should decide which. One
measured constraint limits it either way: the F+D− (abstract, calm) quadrant holds
**one** renderable work and cannot gain another from the public domain
(`docs/BACKLOG.md:758` — calm abstraction is Rothko, in copyright). An adaptive
deck will probe that corner with almost nothing to show.

## Later — Phase 2, gated on evidence

**7. The social layer.** The owner's Letterboxd-like direction is PIGMENT.md's
own Phase 2 and Phase 4, so it is not a departure. The architecture earlier
sessions converged on still holds. **Split Pigment rather than converting it.**
The catalog stays static and git-versioned under the verifiers already built.
Only user data (accounts, lists, logs, follows) goes into a hosted database,
joined to the catalog by stable record ids, which already exist. OP-PLATFORM is
defined and unstaffed. Its lead, the infrastructure role proposed as Brunelleschi,
does not yet exist on the roster. Becoming a host also changes the owner's legal
position (takedown duties, and moderation before any social discovery, per §11
Phase 4). Hand that to Hogarth before building, not after.

## What this session did not do

It merged nothing into `main`. It wrote no theory brief, since that artifact
belongs to the Theory Team. It did not edit the validator or any other sealed
file. It gated nothing in `window.ARTWORKS`. And it did not verify the app in a
live browser: the preview tooling is anchored to the primary checkout, which sits
on another session's branch. The refactor is instead proved equivalent over all
398 records and by byte-identical regeneration of every stub. A browser load is
still worth one manual check before adoption.
