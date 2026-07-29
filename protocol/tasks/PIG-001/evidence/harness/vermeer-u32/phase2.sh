#!/bin/zsh
# Unit 32 phase 2 — everything the route walk structurally cannot reach, plus the
# two verdicts Van Eyck asked for by name. Run after phase 1 (triple.py) finishes.
# Each block writes its own log next to this script.
set -u
cd "$(dirname "$0")"
export PIG_BASE=http://localhost:8437

# ---- 2a. the pseudo-element PERIMETER, from the DOM rather than from the CSS
CDP_PORT=9461 python3 sitecensus.py scan light 1440 900 > log-scan-light-1440.txt 2>&1 &
CDP_PORT=9462 python3 sitecensus.py scan dark  390  844 > log-scan-dark-390.txt  2>&1 &
wait

# ---- 2b. the selector-driven census: pseudo ink, SVG fill: ink, state-only surfaces
CDP_PORT=9461 python3 sitecensus.py probe light 1440 900 3 light-1440 > log-site-light-1440.txt 2>&1 &
CDP_PORT=9462 python3 sitecensus.py probe dark  1440 900 3 dark-1440  > log-site-dark-1440.txt  2>&1 &
CDP_PORT=9463 python3 sitecensus.py probe light 390  844 3 light-390  > log-site-light-390.txt  2>&1 &
CDP_PORT=9464 python3 sitecensus.py probe dark  390  844 3 dark-390   > log-site-dark-390.txt   2>&1 &
wait

# ---- 2c. N-31-1: is .tl2-year's failure caused by the .tl2-grid rule behind it?
#          Measure as shipped, then with only that layer suppressed.
CDP_PORT=9461 python3 sitecensus.py probe light 1440 900 2 n311-light-1440 tl2-year,tl2-year-now > log-n311-light-1440.txt 2>&1 &
CDP_PORT=9462 python3 sitecensus.py probe dark  1440 900 2 n311-dark-1440  tl2-year,tl2-year-now > log-n311-dark-1440.txt  2>&1 &
CDP_PORT=9463 python3 sitecensus.py probe light 390  844 2 n311-light-390  tl2-year,tl2-year-now > log-n311-light-390.txt  2>&1 &
CDP_PORT=9464 python3 sitecensus.py probe dark  390  844 2 n311-dark-390   tl2-year,tl2-year-now > log-n311-dark-390.txt   2>&1 &
wait
V32_SUPPRESS='.tl2-grid' CDP_PORT=9461 python3 sitecensus.py probe light 1440 900 2 n311sup-light-1440 tl2-year,tl2-year-now > log-n311sup-light-1440.txt 2>&1 &
V32_SUPPRESS='.tl2-grid' CDP_PORT=9462 python3 sitecensus.py probe dark  1440 900 2 n311sup-dark-1440  tl2-year,tl2-year-now > log-n311sup-dark-1440.txt  2>&1 &
V32_SUPPRESS='.tl2-grid' CDP_PORT=9463 python3 sitecensus.py probe light 390  844 2 n311sup-light-390  tl2-year,tl2-year-now > log-n311sup-light-390.txt  2>&1 &
V32_SUPPRESS='.tl2-grid' CDP_PORT=9464 python3 sitecensus.py probe dark  390  844 2 n311sup-dark-390   tl2-year,tl2-year-now > log-n311sup-dark-390.txt  2>&1 &
wait

# ---- 2d. N-31-2: at 390 px, is .sr-group's 1.00 its own ink or .main-nav on top?
CDP_PORT=9461 python3 sitecensus.py probe light 390 844 2 n312-light-390 sr-group,sr-more,sr-meta,sr-name > log-n312-light-390.txt 2>&1 &
CDP_PORT=9462 python3 sitecensus.py probe dark  390 844 2 n312-dark-390  sr-group,sr-more,sr-meta,sr-name > log-n312-dark-390.txt  2>&1 &
wait
V32_SUPPRESS='.main-nav' CDP_PORT=9461 python3 sitecensus.py probe light 390 844 2 n312sup-light-390 sr-group,sr-more,sr-meta,sr-name > log-n312sup-light-390.txt 2>&1 &
V32_SUPPRESS='.main-nav' CDP_PORT=9462 python3 sitecensus.py probe dark  390 844 2 n312sup-dark-390  sr-group,sr-more,sr-meta,sr-name > log-n312sup-dark-390.txt  2>&1 &
wait

# ---- 2e. POPULATED #/taste and #/palette — the routes every sweep including
#          phase 1 has only ever rendered in their no-passport state (A16).
V32_PASSPORT=1 CDP_PORT=9461 python3 triple.py light 1440 900 1 pop-light-1440 "#/taste,#/palette,#/daily,#/lists" > log-pop-light-1440.txt 2>&1 &
V32_PASSPORT=1 CDP_PORT=9462 python3 triple.py dark  1440 900 1 pop-dark-1440  "#/taste,#/palette,#/daily,#/lists" > log-pop-dark-1440.txt  2>&1 &
V32_PASSPORT=1 CDP_PORT=9463 python3 triple.py light 390  844 1 pop-light-390  "#/taste,#/palette,#/daily,#/lists" > log-pop-light-390.txt  2>&1 &
V32_PASSPORT=1 CDP_PORT=9464 python3 triple.py dark  390  844 1 pop-dark-390   "#/taste,#/palette,#/daily,#/lists" > log-pop-dark-390.txt   2>&1 &
wait

# ---- 2f. HOVER / FOCUS ink
CDP_PORT=9461 python3 states.py light 1440 900 light-1440 > log-state-light-1440.txt 2>&1 &
CDP_PORT=9462 python3 states.py dark  1440 900 dark-1440  > log-state-dark-1440.txt  2>&1 &
CDP_PORT=9463 python3 states.py light 390  844 light-390  > log-state-light-390.txt  2>&1 &
CDP_PORT=9464 python3 states.py dark  390  844 dark-390   > log-state-dark-390.txt   2>&1 &
wait

# ---- 2g. ATTRIBUTION for the influence-graph labels found failing in phase 1.
#          Same method Dürer used for N-31-1: measure as shipped, then suppress
#          exactly one layer and measure again. If the value recovers, the layer
#          behind the glyphs is the cause and the ink is not.
CDP_PORT=9461 python3 sitecensus.py probe light 1440 900 2 ig-light-1440 ig-node-text,map-dot-name > log-ig-light-1440.txt 2>&1 &
CDP_PORT=9462 python3 sitecensus.py probe dark  1440 900 2 ig-dark-1440  ig-node-text,map-dot-name > log-ig-dark-1440.txt  2>&1 &
CDP_PORT=9463 python3 sitecensus.py probe light 390  844 2 ig-light-390  ig-node-text,map-dot-name > log-ig-light-390.txt  2>&1 &
CDP_PORT=9464 python3 sitecensus.py probe dark  390  844 2 ig-dark-390   ig-node-text,map-dot-name > log-ig-dark-390.txt   2>&1 &
wait
V32_SUPPRESS='.ig-edge' CDP_PORT=9461 python3 sitecensus.py probe light 1440 900 2 igsup-light-1440 ig-node-text > log-igsup-light-1440.txt 2>&1 &
V32_SUPPRESS='.ig-edge' CDP_PORT=9462 python3 sitecensus.py probe dark  1440 900 2 igsup-dark-1440  ig-node-text > log-igsup-dark-1440.txt  2>&1 &
V32_SUPPRESS='.ig-edge' CDP_PORT=9463 python3 sitecensus.py probe light 390  844 2 igsup-light-390  ig-node-text > log-igsup-light-390.txt  2>&1 &
V32_SUPPRESS='.ig-edge' CDP_PORT=9464 python3 sitecensus.py probe dark  390  844 2 igsup-dark-390   ig-node-text > log-igsup-dark-390.txt   2>&1 &
wait
V32_SUPPRESS='.ig-edge,.ig-node circle' CDP_PORT=9461 python3 sitecensus.py probe dark 390 844 2 igsup2-dark-390 ig-node-text > log-igsup2-dark-390.txt 2>&1
echo "PHASE 2 COMPLETE"
