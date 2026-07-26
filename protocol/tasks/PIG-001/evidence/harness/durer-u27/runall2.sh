#!/bin/zsh
# Unit 27, clean re-measurement.
#
# WHY THIS EXISTS. A chain from the previous unit-27 pass (`sh /tmp/u27-all.sh`,
# started 19:28, orphaned to PID 1 when that session ended) was still running six
# hours later, writing the SAME `mu-<tag>.json` filenames this pass writes. For a
# while two chains measured the same venues concurrently, so the 390 px results
# on disk had mixed provenance and were produced under CPU contention. Both
# chains were stopped and everything ambiguous is measured again here, serially,
# by one process at a time, against the final committed CSS.
#
# Pixel values were never at risk of cross-talk (mu.py gives each process its own
# shot paths and each browser its own CDP port); what was at risk was knowing
# WHICH css state produced WHICH file. That is what this run settles.
set -e
cd "$(dirname "$0")"

# 1-2 — the criterion gap Vermeer named (NOT TESTED #4), full 104-venue sweeps
CDP_PORT=9401 python3 mu.py all  dark  390  844 after-dark-390    > log2-after-dark-390.txt   2>&1
CDP_PORT=9402 python3 mu.py all  light 390  844 after-light-390   > log2-after-light-390.txt  2>&1
# 3-5 — the matching BEFORE state, shipped rules restored at runtime
U27_BEFORE=1 CDP_PORT=9403 python3 mu.py worst dark  390  844 before-dark-390   > log2-before-dark-390.txt   2>&1
U27_BEFORE=1 CDP_PORT=9404 python3 mu.py worst light 390  844 before-light-390  > log2-before-light-390.txt  2>&1
U27_BEFORE=1 CDP_PORT=9405 python3 mu.py worst light 1440 900 before-light-1440 > log2-before-light-1440.txt 2>&1
# 6-7 — corroboration of the RETAINED 104-venue 1440 sweeps. Those ran before two
# late edits to styles.css (a comment, and outline-color on :focus-visible in the
# light band). Neither can move a glyph pixel, but "cannot" is worth checking, so
# the 15 adversarial venues are re-measured at 1440 against the final CSS and the
# worst-per-class must reproduce.
CDP_PORT=9406 python3 mu.py worst dark  1440 900 recheck-dark-1440  > log2-recheck-dark-1440.txt  2>&1
CDP_PORT=9407 python3 mu.py worst light 1440 900 recheck-light-1440 > log2-recheck-light-1440.txt 2>&1
echo "ALL RUNS COMPLETE"
