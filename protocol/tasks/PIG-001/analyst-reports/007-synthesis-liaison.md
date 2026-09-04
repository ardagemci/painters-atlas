# Synthesis Liaison Report - PIG-001 response to review, pre-transmission audit

# Synthesis Liaison Report

## Current Position

The build is certified. An independent reviewer who had blocked it four times and wrote none of its code passed all twenty-nine acceptance criteria at commit `fb8ba6e`, with zero failures and nothing unsupported. The team has drafted its final reply to the theory pole. I audited that reply before it is sent, and I am asking for four small corrections first.

## Feasibility

No feasibility question remains open. Every constraint the reply claims is genuine: the contrast instrument really cannot measure a focus ring, the two evidence bases really do sit in different browser engines, and re-verifying image rights really would need network access. Each is correctly labelled a limit rather than a result.

## Adaptations Made

Three material ones. The screenshot pack was kept as captured rather than recaptured after the last code change, because the reviewer measured the visual difference at 1.32 pixels on a soft gradient. Focus-ring contrast was replaced by a stronger measurement of a different thing - a real keyboard pass proving every ring is present and unclipped. And the automated quality check the Coordinator runs was downgraded, because it can be fooled; the team wrote that code themselves and says so.

## Product Intent

Preserved. Nothing in the reply trades the intended outcome for convenience, and the two places where the team broke a rule of yours - the wording about public-domain images, including one line that was live on the credits page - are reported plainly and already fixed.

## Evidence

Strongest: 2,626 measured text samples across twelve screen-and-theme combinations with none below the readability floor; the full test suite passing, which I re-ran myself; the horizontal-overflow defect measured at zero across eight widths; and three real VoiceOver sessions you ran, which found seven problems no automated tool had found. I re-derived every load-bearing number and they hold, with one exception: the reply says 97 commits and the true figure is 98.

Gaps, all disclosed except where noted below: everything visual was measured in Chrome and everything audible was confirmed in Safari, so the two never corroborate each other; the screen-reader evidence is one person on one setup; and there is a stated list of sixteen things nobody tested, which the reply does not mention.

## Remaining Problems

The reviewer's verdict ends by naming nine leftover items. The reply carries four of them and drops five. One of those five matters: the reviewer had closed the screenshot question and then deliberately re-opened it, because the last code change came after the screenshots were taken. He left you a choice - retake 47 mobile screenshots before the review package, or note the limitation and move on - and said either was defensible. The reply does not mention it at all, and instead reports the screenshot task as finished. That choice is yours to make, and as drafted it would never reach you.

The four dropped alongside it are smaller: a version label naming the wrong unit, a note that the specification's corpus figures are out of date, an untested condition about what the deployed site will request, and a colour contrast margin that cannot be improved.

## Synthesis Assessment

The quality evidence is sufficient and the certification is sound. The problem is in the reply's account of it, not in the work. On the parts that usually go wrong this draft is unusually good: its three corrections to the theory pole are all correct and none is overstated, and its four admissions of its own failures are accurate and not softened.

## What Happens Next

I have asked the team to make four bounded corrections before sending: restore the screenshot item and your choice about it; qualify the screenshot task as partly discharged; add the four other leftover items; and fix the commit count and one softened word. None requires new work, and none costs a round of deliberation.

## Attention Required

Hold for final Human Review Package.
