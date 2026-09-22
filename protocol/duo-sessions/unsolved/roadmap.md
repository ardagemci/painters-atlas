# Roadmap — from here to the social atlas

**Duo session `unsolved`, 2026-09-17.** Supersedes
`protocol/duo-sessions/elevate/future-steps.md`, which stays as dated history. Every
gate below is a **proposed evidence requirement**, not a product promise. Promises
live in PIGMENT.md, and changing them is Lane I. The decisions each stage waits on
are numbered as in `decision-register.md`.

---

## The goal, and the distance to it

> *"Pigment is a social atlas where people discover, understand, and express their
> taste in art."* — PIGMENT.md §1

Those three verbs are the measure of what is already built.

- **Discover** is the strongest. The atlas holds 280 artists and 398 catalogued
  works, with 15 lists, a 120-work Painting of the Day, 127 museum notes, a
  timeline, an influence graph and 820 prerendered pages.
- **Express** exists but is untested. There is onboarding, a Passport, 15
  Personas, a taste map and a painted shareable card. **Nobody outside the
  project has used any of it.**
- **Understand** is the weakest. There are artwork explanations and "what to
  notice" bullets, but the learning layer (Phase 3) does not exist: no guided
  routes, no mastery, no museum one-hour routes.
- **Social** has not started, and correctly so. PIGMENT.md §16 forbids accounts
  until the core loop is shown to work.

**So the distance to the goal is not mostly code. It is evidence.** The project has
spent a month making its data and rights rigorous, and has never watched a stranger
use the product. The roadmap is ordered to fix that first.

---

## Stage 0 — Integrate and tell the truth about the present
*Now. About a day of owner review.*

**Work:** merge the stacked duo branches (decision 1) and apply the PIGMENT.md
reconciliation (decision 2). Settle Lane IV (decision 3).

**Exit — all measurable:**
- `main` passes the suite and the validator with both branches merged.
- PIGMENT.md's §12 counts match the validator on the date stamped, and no §15 or
  §19 status contradicts the repository. `pigment-reconciliation.md` is the
  checklist.
- §19 D-6's privacy rationale is restated accurately, because every catalog image
  already comes from a third-party host.

**Why first:** every later stage is planned from PIGMENT.md, and it currently
describes a product that is partly out of date.

## Stage 1 — Prove the loop (finish Phase 1.5)
*Weeks. This is the stage that matters.*

**Work:**
1. Run five observed sessions with `docs/LOOP_STUDY_PROTOCOL.md` (decision 4).
2. Rank the obstacles people actually hit, by the kit's severity scale.
3. Fix the blocker- and major-severity obstacles, then observe again.
4. With that evidence, decide D-1 (adaptive deck or an honest claim, decision 5) and
   whether confidence (D-5) and the fifth axis (D-7) become visible.

**Exit:**
- Five completed sessions with a ranked obstacle list filed in the repository.
- No blocker-severity obstacle left open after re-observation.
- **The deck's delivery and every document describing it agree.** Today they do not.

**What this stage cannot show, stated so nobody over-reads it:** five sessions
expose usability problems. They do not prove people enjoy the loop, and they do not
by themselves justify accounts. A larger, repeated study belongs at the Phase 2
gate.

**Known limit on step 4:** the calm-abstract quadrant holds one showable work and
cannot gain another from the public domain. Whatever the deck becomes, that corner
stays thin. That is a product constraint to design around, not a backlog item.

## Stage 2 — Deepen *understand*, where the loop points
*Months, run in parallel with Stage 1's later rounds.*

Choose the order from Stage 1's obstacle list, not from this document. The
candidates, each already measured:

- **Museum one-hour routes** (D-2, decision 7), starting with the museums the
  atlas holds most works from. Each route makes claims about real works, so Vasari
  and Van Gogh are in the loop.
- **Grounded influence edges.** 107 of 259 edges have no grounding in any bio or
  citation. A ratchet already holds the count, and it should fall.
- **Lists fully at Tier 1.** 23 of 107 list works are still Tier 2.
- **Movement and technique explainers** for the most-visited taxonomy pages
  (PIGMENT.md §16.5).

**Exit:** the chosen ratchets fall and never rise, and routes exist for the museums
chosen.

## Stage 3 — One policy for every image
*Before anything that multiplies traffic or user uploads.*

**Work:** IFACE-001 in full — the no-image state and a policy for the 402 unmatched
gallery entries (decision 8). RIGHTS-001 Decisions C and E (decisions 10 and 11).
The validator on the shared rule (decision 9). Counsel in Türkiye (decision 12).

**Exit:**
- Every surface that can show an artwork image, whether catalog, gallery or
  prerender, answers to one written policy, with tests that run the production
  code.
- Rendered credits name the party each licence requires. The mechanism to check
  this already exists (`TestAuthorIdentity`); the owner's choice of which name to
  show does not.

**Why before Phase 2:** a social product copies images into feeds, lists and shares.
A rights inconsistency that is harmless on 398 static pages becomes expensive once
it is multiplied by users.

## Stage 4 — Phase 2: accounts and real identity
*Gated. Do not start without Stage 1's evidence and Stage 3's policy.*

**Gate to enter** (decision 14): Stage 1 has shown the loop working for people who
did not build it, and a larger study confirms it. Stage 3 is complete.

**Architecture — split Pigment rather than converting it.** The catalog stays
static, git-versioned and verified by the tooling already built. Only user data
moves into a hosted database: accounts, Passports, favourites, user lists and
logs. It joins to the catalog through the stable record ids that already exist.
The Passport's current `localStorage` shape (`pigment.taste.v1`) is the migration
source.

**Before any code:**
- Staff OP-PLATFORM. Its lead role, proposed earlier as Brunelleschi, does not yet
  exist on the roster.
- Have Hogarth brief the legal change. Storing user data and hosting what people
  post brings privacy duties and takedown obligations, under Turkish law since
  residence is Türkiye.

**Scope, from PIGMENT.md §11:** profiles, favourites, user lists, ratings and
reflections, museum logs. Direct messages, dating, heavy notifications and generic
posting are explicitly excluded at the start.

**Exit:** defined when the gate is met, from the evidence that met it.

## Stage 5 — Phases 3 and 4: learning, then community
*After Phase 2 has real users and real activity.*

- **Learning (Phase 3).** Guided routes, comparison and recognition quizzes,
  mastery. None exists yet. Today's "quiz" is only the onboarding taste prior.
- **Community (Phase 4).** Following, activity, comments, taste comparison.
  **Moderation, reporting, blocking and anti-harassment come before any social
  discovery** (PIGMENT.md §11). Dating is never part of the promise.

---

## What would change this roadmap

- **The loop study finds a problem upstream of taste** (for example, people never
  reach onboarding). Stage 1 then becomes an information-architecture problem, and
  the moderna redesign moves up.
- **Counsel finds the attribution practice needs changing.** Stage 3 then moves
  ahead of Stage 2.
- **The loop works, but only for art-literate people.** Stage 2's "understand"
  work becomes the path to the audience PIGMENT.md describes, and should come
  before accounts.
