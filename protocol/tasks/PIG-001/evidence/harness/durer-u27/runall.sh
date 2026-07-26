#!/bin/zsh
# Unit 27 — the runs F-V1 still needs, serialised.
# Serialised on purpose: two concurrent runs of photos.py fight over one headless
# Chrome's CPU and produce settle timeouts, and a shared shot path is exactly how
# a first attempt at this unit read a backdrop the veil makes impossible. Each
# run gets its own CDP port; mu.py already gives each process its own shot paths.
set -e
cd "$(dirname "$0")"

# the criterion-critical pair first: 390x844 is Vermeer's NOT TESTED #4
CDP_PORT=9361 python3 mu.py all  dark  390  844 after-dark-390    > log-after-dark-390.txt   2>&1
CDP_PORT=9362 python3 mu.py all  light 390  844 after-light-390   > log-after-light-390.txt  2>&1
# then the matching BEFORE state, same instrument, shipped rules restored
U27_BEFORE=1 CDP_PORT=9363 python3 mu.py worst dark  390  844 before-dark-390   > log-before-dark-390.txt   2>&1
U27_BEFORE=1 CDP_PORT=9364 python3 mu.py worst light 390  844 before-light-390  > log-before-light-390.txt  2>&1
U27_BEFORE=1 CDP_PORT=9365 python3 mu.py worst light 1440 900 before-light-1440 > log-before-light-1440.txt 2>&1
echo "ALL RUNS COMPLETE"
