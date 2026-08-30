# OP-PLATFORM

**Prefix:** `PLATFORM-` · **Lead:** Brunelleschi (`claude-systems-architect`) — **role not yet created**

## The question it answers

> What must exist for people to keep something here?

Accounts, persistence, and the social loop: profiles, follows, user lists, logs.
The direction is a Letterboxd-shaped layer over the atlas — discover, learn,
share, curate.

## Status: declared, not staffed

This OP is written down so its scope is settled before work starts, and because
declaring it surfaces a real gap: **no agent on the roster knows backend or
infrastructure.** Dürer is the implementation lead for a static site with no
build step; nothing in the roster covers schema design, authentication,
row-level security, or hosting.

Opening a `PLATFORM-` task therefore requires creating
`.claude/agents/claude-systems-architect.md` first. The proposed namesake is
Brunelleschi — architect and engineer, and the man who worked out linear
perspective, which makes him the right patron for whoever designs the structure
everything else is drawn inside.

## The architectural commitment

Recorded here because it constrains every later decision, and because the
opposite instinct is the expensive one:

> **The catalog stays static. Only user-generated data goes in a database.**

Artists, artworks, taxonomy, editorial lists, the rights census, the validators
and the guards remain files in this repository — fast, free, cacheable,
git-versioned, and protected by tooling that already exists. Users, profiles,
follows, user lists and logs are the new, dynamic half.

The join between them is the **catalog slug**: records already carry stable ids
like `triumph-of-death` and `black-fuji`. A user list stores that string. No
migration of existing data is required, and no part of the current toolchain is
discarded.

## Write scope

**May write**

| Path | Condition |
|---|---|
| new top-level paths for the platform layer | e.g. `platform/`, schema and policy definitions, `.env.example` |
| `js/app.js` | at declared integration points only, recorded in the task's decision record |
| `protocol/tasks/PLATFORM-*/` | its own task artifacts |
| `protocol/oriented/OP-PLATFORM.md` | this file |
| `docs/` | architecture and operations documentation |

**May not write**

- Any catalog record, `js/taxonomy.js`, `js/influences.js`, or the editorial
  lists. The platform layer references the catalog; it does not edit it.
- `image:{}` blocks, `js/photo-credits.js`, or the rights census.
- `css/` beyond what a new surface requires, and never the existing visual
  system — that is OP-INTERFACE.
- The Lane III sealed set, in Lane III.

**Never committed, in any lane:** secrets, API keys, service-role credentials,
or a `.env` file. Only `.env.example` with empty values.

## Hard dependency on OP-RIGHTS

Accepting user-generated content changes Pigment's legal posture from publisher
to intermediary. That is a change of kind, not of degree, and it is the owner's
to make with advice — not a side effect of shipping an upload button.

At minimum, before any surface accepts user content:

- a takedown route exists and someone answers it;
- the terms under which a user grants Pigment permission to display what they
  post are written down;
- the jurisdictions whose rules apply are named, including the host's;
- what a user's deletion actually deletes is described truthfully, including
  what survives in backups and caches.

No `PLATFORM-` task that accepts user content may reach `human_review_ready`
without an OP-RIGHTS artifact addressing these. This dependency is deliberate
and is not waivable by scheduling.

## Acceptance criteria

1. Authorization is tested **negatively**: a test proves user A cannot read or
   write user B's private rows. A guard that cannot fail is not a guard.
2. No secret is committed, and this is checked by a guard rather than by care.
3. The static catalog still builds, validates and deploys with the platform
   layer absent or unreachable. Degradation is graceful: the atlas is readable
   by a signed-out visitor with the database down.
4. Every new dependency is named with the reason it earned its place. This
   project's zero-dependency posture is an asset being spent, not a rule being
   broken, and the spend is recorded.
5. Data the platform stores about a person is enumerated, with a stated reason
   for each field.
6. `tools/validate.jxa.js` exits 0 and the suite passes.

## Standing notes

Scope discipline matters more here than anywhere else in the project, because
this is the OP with no natural ceiling. The smallest loop that is actually alive
is **log a work → put it in a list → follow someone → see their lists.** Ratings,
reviews, comments, notifications and feeds are all later, and each should have to
argue for itself.
