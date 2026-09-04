# Synthesis Liaison Report - PIG-001 Build Review (round 2)

## Synthesis Liaison Report

### Current Position
The build is real, large, and mostly honest. Thirty-one units landed on an isolated
branch off the frozen baseline; the repository validator passes with zero warnings; the
two Taste-layer defects that the original theory brief never contained are closed and
behaviourally verified. Independent quality review has refused to certify three times
and still refuses. The team is asking to route the build to the theory pole for review,
not to the owner and not to production.

### Feasibility
Nothing in the remaining work is technically hard. Every open contrast defect has been
measured and has a named remedy. One remedy is a layout decision rather than a colour
change and needs the interaction architect, not more measurement. No genuine
impossibility is claimed, and none is hiding.

### Adaptations Made
Three matter. A teammate's unrelated content work committed onto the build branch
mid-build, so a rollback now has to undo this build's commits one by one instead of
resetting the branch; that is recorded and the consequence is stated. A colour remedy
that two reviewers had specified was measured, found wrong, and replaced rather than
applied. And the build team changed the coordinator's own code mid-build to add a check
that stops text files being accepted as proof of a build — a good change, but it was
never written into the decision ledger, and the report leans on that very code to argue
its routing is allowed.

### Product Intent
Preserved. The frozen twenty-nine criteria governed the build unchanged, no criterion
was quietly reinterpreted, and the scope did not expand.

### Evidence
The strongest support is that the numbers reproduce. I re-derived the build
authorization fingerprint myself and it matched exactly; I re-ran the validator; the
production-file count, the credit counts, the recovery and search results, and every
contrast figure the report quotes came back the same. That is unusually good.

The gap is what the report leaves out. The most severe defect found anywhere in this
build — search-result headings at mobile width painted at essentially zero contrast,
invisible text — appears in the independent measurement record and in the build team's
own log, and does not appear in the report at all. Four smaller open items from the
quality reviewer are also missing, including one he set as a condition on the final
review package. Two surfaces that were explicitly not cleared are not mentioned. And
the quality review the report cites was written before the last two units landed.

### Remaining Problems
Six major contrast defects are open, not five. The unrecorded change to the
coordinator's code needs ledgering. The report's own promise — that nothing was
summarised away — is not true as written and has to be made true before it is sent.

### Synthesis Assessment
Feasibility is supported. Quality is not, and the report knows that and says so
plainly, which is to its credit. But a report that under-reports its worst defect
cannot be the artifact the next pole reviews against. Sending it back is a small repair,
not a rebuild.

### What Happens Next
I am recommending the report be returned to the team for correction and re-sent. The
build stays where it is; no state changes and nothing reaches production.

### Attention Required
Hold for final Human Review Package.
