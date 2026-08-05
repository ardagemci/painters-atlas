# VoiceOver session 3 — verifying the fixes your last two sessions caused

**Operator:** Arda · **Site:** http://localhost:8422 (confirmed serving unit 33)

Your two sessions found seven defects. All seven now have fixes, and **none of
them is verified by ear** — I can prove the right words are in the page, not that
you hear them. Six behaviours below; roughly fifteen minutes.

Same four keys: **Control** to interrupt, **Tab** to move, **Control+Option+A**
to read on, **Return** to activate. Light theme. VoiceOver on with **⌘ + F5**.

Anything that is still wrong, say so bluntly. A fix that half-works is worse
than one that plainly fails, because it survives review.

---

## 1 — The skip link, on the very first Tab (was: silent)

Diagnosis from last time: the link *was* first in tab order, but it sat 120px
above the top of the window at the moment it received focus and slid in 180ms
later. It should now be present instantly.

Load the homepage fresh. Press **Tab once**.

**Tell me:** does VoiceOver say something like "skip to main content" — and does
it say it *immediately*? Press **Return** — where do you land?

---

## 2 — The onboarding deck naming each artwork (was: silent; the worst finding)

You were on Monet's *Stacks of Wheat* and it never said so. The deck should now
announce each card.

Go to **http://localhost:8422/#/palette**, begin, choose four tones, and reach
the artwork cards.

**Tell me:** for each card, does it now say **which artwork** — title and artist?
Does it tell you **where you are** ("3 of 16")? Is the amount it says about right,
or does it become a chore by the fifth card?

That last question matters as much as the first. Sixteen cards is a lot of
speech.

---

## 3 — Dismissing search (was: silent)

Tab to search, type **leonardo**, wait for results, press **Escape**.

**Tell me:** does it now say anything — that results closed, or where you are?
And does the field itself still announce as three things at once, or simply as a
combo box now?

---

## 4 — Cancelling an import (was: silent, and it moved you)

Open **http://localhost:8422/passport-test.html**, click **A**, accept it. Then
click **B** and work to the choices — then **Cancel**.

**Tell me:** does it now tell you **nothing was changed**? Do you hear that
*before* being moved, or does the move still happen silently first?

---

## 5 — What happened after a merge (was: never stated)

Do it again: click **B**, this time keep **your own** persona (Candlelight
Conspirator), and merge.

**Tell me:** does it now confirm **which choice won**? Could you tell, without
looking, that you kept yours rather than taking theirs?

---

## 6 — The arrows (was: "right arrow" read aloud)

Anywhere on the homepage, read through a few links — the entry cards, a "go
next".

**Tell me:** do you still hear "right arrow"? Anything else being read that is
plainly decoration rather than content?

---

## When you're done

Per item: **what you heard**, anything **still silent**, anything **too talkative**,
and anything that irritated you.

The talkativeness question is genuine, not politeness. Item 2 in particular: I
added announcements to sixteen consecutive cards, and there is a real risk I have
replaced "says nothing useful" with "says too much to bear". You are the only
person who can tell me which.
