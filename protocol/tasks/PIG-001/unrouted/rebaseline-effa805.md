# PIG-001 — Rebaseline at effa805a8a442206985dad6b14fd67993ac6b6c0

Requested by the theory pole (recovery step 4). Run 2026-07-21 on unmodified
`main` at effa805, via `osascript -l JavaScript tools/validate.jxa.js`.

## Unedited validator output

    app.js: syntax OK
    artists: 247, movements: 75, techniques: 39, eras: 8, nations: 37, painter styles: 27, influence edges: 225, venues: 115, catalog: 317 (tier1: 75), daily pool: 75, museum notes: 103, personas: 15, lists: 12 (featured: 4), tier1 artists: 36 (arcs: 36)
    WARNINGS:
      deck pool: <2 works with E<=-40
      deck pool: empty F×D quadrant 1,-1
    ALL REFERENCES VALID

## Deltas vs the July-21 intake baseline (commit 3c2e9fa)

| Count | 3c2e9fa | effa805 | Cause |
| --- | --- | --- | --- |
| artists | 246 | 247 | 2b0e18d adds Fitz Henry Lane |
| movements | 74 | 75 | 2b0e18d adds Luminism |
| catalog artworks | 315 | 317 | 2b0e18d adds two works |
| Tier 1 artworks / daily pool | 73 | 75 | same |
| all other counts | unchanged | unchanged | — |

Both deck-pool warnings persist unchanged; ALL REFERENCES VALID.

Consequences: THEORY_001 §3.1's snapshot is now dated (it matched 3c2e9fa
exactly). The theory pole's "current Theory Brief" must cite these numbers.
The rights-surface count in data-integrity-report.md (255 pd catalog images)
grows by up to 2 pending re-count at routing time. Commit 2b0e18d is Sol's
independent content lane, outside PIG-001; it edits production files under
Sol's own authority, not under this task's Gate 1.
