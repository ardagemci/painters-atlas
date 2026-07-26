#!/bin/zsh
# Wait out the sweep chain, then the two confirmations that do not belong in it:
#   ring.py     — the focus indicator inside the veil, both themes
#   bgcanvas.py — proves the out-of-band shortfalls are the generative canvas,
#                 not a Wikimedia photograph (the .mu-collage.c4 phantom box)
cd "$(dirname "$0")"
until grep -q "ALL RUNS COMPLETE" runall2-console.txt 2>/dev/null; do sleep 15; done
echo "=== SWEEPS DONE ==="
CDP_PORT=9411 python3 ring.py light 1440 900 > log2-ring-light-1440.txt 2>&1 || echo "ring light FAILED"
CDP_PORT=9412 python3 ring.py dark  1440 900 > log2-ring-dark-1440.txt  2>&1 || echo "ring dark FAILED"
CDP_PORT=9413 python3 ring.py light  390 844 > log2-ring-light-390.txt  2>&1 || echo "ring light390 FAILED"
CDP_PORT=9414 python3 bgcanvas.py tate-britain dark  1440 900 > log2-bgcanvas-dark.txt  2>&1 || echo "bgc dark FAILED"
CDP_PORT=9415 python3 bgcanvas.py uffizi       light 1440 900 > log2-bgcanvas-light.txt 2>&1 || echo "bgc light FAILED"
echo "=== FINISH COMPLETE ==="
