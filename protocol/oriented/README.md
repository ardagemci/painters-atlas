# Oriented Protocols

An Oriented Protocol (OP) runs the deliberation cycle in `protocol/PROTOCOL.md`
against **one domain**. It does not replace that protocol, fork it, or relax it.
The cycle, the message envelope, the convergence standard and Gates 1–4 are
identical in every OP. What an OP adds is orientation.

## What makes an OP real

A name is not a protocol. An OP is worth declaring only when it binds three
things that must match each other:

1. **A write scope.** The set of paths this OP may change, and — more
   importantly — the set it may not. `CLAUDE.md` §2 gives each *agent* a
   "Writes?" column. An OP makes that column enforceable per *objective*, so
   that a rights decision cannot quietly rewrite prose and a visual pass cannot
   quietly retier a record.
2. **An agent set.** The roster members whose competence matches the scope, with
   one of them named lead. An OP that would need an agent the roster does not
   have must say so rather than improvise.
3. **Acceptance criteria that fit the domain.** "The validator passes" is not a
   sufficient bar for a rights question, and "a lawyer would accept it" is not a
   sensible bar for a hover state.

If a proposed OP cannot state all three, it is a topic, not a protocol.

## What an OP does not change

- The deliberation cycle and workflow states (`PROTOCOL.md` §§1–2).
- The message envelope (§3) and its schema.
- The convergence standard (§5).
- Gates 1–4 (§6). Gate 4 in particular: every OP works in an isolated branch or
  worktree, and `main` merges remain the owner's.
- The Lane discipline and the sealed set in `CLAUDE.md` §0. An OP's write scope
  can only ever be a **subset** of what its lane already permits. No OP grants
  Lane III access to `tools/validate*`, `tools/audit_*.py`, `tools/lane3*`,
  `CLAUDE.md`, `PIGMENT.md`, `protocol/` or `.claude/`.
- Owner decisions. OD-5 binds in every OP, not only in OP-RIGHTS.
- Ratchet direction. A counted guard may fall and never rise, whichever OP is
  running.

## Task ids

Each OP owns a prefix, and its tasks live in `protocol/tasks/<task_id>/` with
the layout in `PROTOCOL.md` §7:

| OP | prefix | example |
|---|---|---|
| OP-RIGHTS | `RIGHTS-` | `RIGHTS-001` |
| OP-INTERFACE | `IFACE-` | `IFACE-001` |
| OP-CONTENT | `CONTENT-` | `CONTENT-001` |
| OP-PLATFORM | `PLATFORM-` | `PLATFORM-001` |

`PIG-NNN` remains the prefix for objectives that are genuinely cross-cutting, or
that predate this file. An objective is cross-cutting only if it must change
more than one OP's write scope *at the same time*; wanting two OPs' opinions is
not the same thing, and is handled by consultation rather than by widening
scope.

## The index

| OP | Lead | Question it answers | File |
|---|---|---|---|
| **OP-RIGHTS** | Hogarth | On what basis may Pigment show this, and what does the owner need to decide? | [OP-RIGHTS.md](OP-RIGHTS.md) |
| **OP-INTERFACE** | Mondrian | What does the reader encounter, and does it work at real viewports? | [OP-INTERFACE.md](OP-INTERFACE.md) |
| **OP-CONTENT** | Vasari | What belongs in the atlas, and is it described honestly? | [OP-CONTENT.md](OP-CONTENT.md) |
| **OP-PLATFORM** | Brunelleschi (unfilled) | What must exist for people to keep something here? | [OP-PLATFORM.md](OP-PLATFORM.md) |

## Deliberately not an OP

**Vision.** A protocol is machinery for converging on decisions that then get
built; vision has no build step, and a Vision OP would become a place where
strategy documents accumulate without anyone implementing them. Direction
belongs in the owner-decision series (OD-N) and in each OP's intake stage, where
it constrains real work and can be argued against with evidence. This is a
recommendation and not a rule — the owner may create one.

**Growth, analytics, monetisation.** Premature. Pigment has one owner and no
users yet. An OP declared before there is work for it is a filing cabinet.

## Consultation across OPs

An OP may request an opinion from an agent outside its set. The opinion is
evidence; it is not authority, and it does not widen the write scope. Record it
in the task's `decision-record.md` like any other input. Where two OPs disagree
on something neither can decide alone, that is a §8 escalation to the owner, not
a negotiation between agent sets.
