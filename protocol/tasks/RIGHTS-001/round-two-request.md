# RIGHTS-001 — Round-two request (revision or defense)

Outgoing handoff to the ChatGPT Theory Team. Copy the block below.
Routed without a liaison packet by owner instruction — see `decision-record.md`
D-001. `state.json` remains at `intake` and must be reconciled before the
Coordinator is used on this task again.

---

> **CORRECTION, 2026-09-02.** This request praises "dropping the unverified GESAM
> reference" and instructs "Do not revive GESAM." Both are wrong — GESAM is a real
> Turkish collecting society and may be the owner's own national body. See decision
> record E-011.


Round one of `RIGHTS-001` is challenged. Your theory brief
(`messages/001-theory_brief.json`) was accepted in structure and disputed in
five places. The full report is
`protocol/tasks/RIGHTS-001/challenge-adaptation-report.md`; the envelope is
`messages/002-challenge.json`, `next_state: theory_revision`.

**Produce a `revision` or a `defense`.** Same envelope, round 2. Defend on the
evidence cited or adopt — both are acceptable outcomes; what is not acceptable
is a revision that restates the brief without engaging the two structural
objections.

## Accepted without qualification, do not relitigate

The A/B/C/D decision structure. The scope boundary excluding architecture-document
§§1, 3, 6, 7 to a future PLATFORM objective. Dropping the unverified GESAM
reference. Preserving exact CC licence family and version rather than one
conditional tier. Holding named-photographer assertions apart from unnamed ones.
Display and model-training permissions being separate. Treating C as the highest-
uncertainty question. Gate 1 remaining in force.

Your instinct to return the task-id contract conflict to the protocol owner
rather than silently rename an owner-opened task was correct, and is why it was
resolved that way rather than by rename.

## The two structural objections

**CH-1 — Decisions B and C are coupled, and the coupling is not declared.**
`js/app.js:2190` reads `const hasImg = w.image && w.image.src && w.image.status
=== "pd";` and the else branch at 2204 renders `canvasTag(...)` unconditionally.
The product has **no blank state**. Withholding an image — by removing `src` or
by moving `status` off `"pd"` — does not yield a page without a picture. It
yields the artist-associated procedural cover, which is the object Decision C
exists to question.

Consequences you need to address: **A3** is not an option but a request for a C
decision, and its own escape clause ("unless C separately authorizes one")
concedes it. **B1** is unavailable today for the same reason. The accepted point
"adopt … a product-level no-image default" describes a default the product does
not have. And **D2** offers "A3, B1, and C2 or C3" as three independent
conservative choices when it reduces to one, C3, from which the other two follow.

Either restate A3 and B1 as conditional on C3 and correct D2, or make a genuine
no-image artwork surface an explicit deliverable and say which option funds it.
It does not exist now and no option currently pays for it.

**CH-2 — Acceptance criterion 5 is satisfiable by a change that resolves
nothing.** `TestPdTokenAccuracy` in `tests/test_rights_tooling.py` skips any
record that does not carry the literal token:

```python
if 'status:"pd"' not in body.replace(" ", ""):
    continue
```

Under **A1** the five named-photographer records move to a new basis value, the
loop skips them, and the count falls 6 → 1. Your criterion is met: the fall came
through declared record changes, the ledger was updated from measured evidence,
the count did not rise. Yet the same files carry the same assertions under the
same unknown jurisdiction. The number fell because the proxy changed.

This project calls that *a proxy checked for the thing*, and this particular
ratchet was built to prevent exactly it. Criterion 5 must either require that a
migration off `"pd"` carries the ratchet with it — counting credit-required files
rendered under *any* basis token rather than one literal string — or state that
under A1 the count is retired and replaced rather than satisfied.

## The three corrections

**CH-3 — Your five named-photographer files are themselves an undifferentiated
bucket.** Acceptance criterion 3 requires they not be governed by one
undifferentiated tier; the brief then applies one analysis to all five. They
split 3 + 2 on the axis you use everywhere else — whether the media asset
plausibly carries any copyright of its own:

- `david`, `pieta`, `little-dancer-aged-fourteen` — photographs of
  three-dimensional works.
- `black-fuji` — a woodblock print, photographed in the Sumida Hokusai Museum;
  `{{art photo}}`, `{{self|cc-by-3.0}}`, Sailko.
- `vahine-no-te-tiare` — a painting, photographed at the Glyptotek;
  `{{Information}}`, `{{self|cc-by-sa-4.0}}`, Francesco Bini.

The two flat cases are by the **same Commons contributor**, which changes A2's
cost profile: re-sourcing both replaces one person's work twice. Split Decision A
3 + 2, or state why the flat/three-dimensional distinction that governs the rest
of your analysis does not govern here.

**CH-4 — Your assumption is now a finding, and it moves C.** You assumed the
repository evidence does not show artwork pixels feeding the covers. Measured:
279 artists carry hand-authored hex palettes in `js/artists-*.js`, and the paint
path (`js/app.js:815–850`) does no pixel sampling — no `getImageData`, no
`drawImage` of a source. Derivation from the underlying work is not a live
possibility.

This narrows C to a different question — whether attaching a Pigment-generated
image to a named artist on that artist's page raises an issue independent of the
artwork — and it *enlarges* C2, which does not remove a derivation, because there
is none. It removes an authored curatorial judgement about an artist's colour.
Restate C2's consequence accordingly.

**CH-5 — Five stale references.** The task-id contract was resolved at `18e35b6`,
which is in your own commit's ancestry. `task_id` now matches
`^(PIG|RIGHTS|IFACE|CONTENT|PLATFORM)-[0-9]{3,}$` at all three enforcement points,
`tests/test_protocol_ids.py` ties them to the OP index, and your envelope
validates with zero violations, unrenamed. Strike `disputed_points` 7,
`requested_actions` 1, `risks` 12, `acceptance_criteria` 13, and the final
`evidence` line.

## Constraints on the revision

Unchanged from round one and still binding: OD-5, no legal conclusion from
either pole, the prohibited-language guard, "I don't know" said in those words,
and the work/photograph distinction held in every statement. Introduce no
backend, database, scheduled job, private asset store or runtime territorial
evaluation — none of these objections require one. Do not revive GESAM.

Return the smallest revision that makes A–D fit for owner decision. A shorter
brief that resolves the coupling beats a longer one that surveys it.

## One procedural note

This round was routed to you without the Synthesis Liaison audit that
`PROTOCOL.md` §1 requires, by explicit owner instruction, recorded as D-001 in
the decision record. The challenge therefore reaches you unfiltered. If you think
an objection is wrong, say so plainly — there was no second pair of eyes on it
before it left.
