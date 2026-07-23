# PIG-001 — Public Asset Inventory at effa805 (criterion 10)

Enumerated 2026-07-23 by static analysis of the repository at
effa805a8a442206985dad6b14fd67993ac6b6c0 (script preserved in task record;
JSON detail in asset-inventory-effa805.json). "Unique asset" means a unique
upload.wikimedia.org URL string; distinct thumbnail widths of the same
Commons file count separately, so unique underlying files may be slightly
fewer. No network requests were made; reachability is derived from code
gating, not fetches.

## Exact counts by surface

| Surface | References | Unique assets | Reachability |
| --- | --- | --- | --- |
| Catalog artwork images (js/catalog-1..4.js, status:"pd") | 257 | 257 | rendered in app (gate: app.js status==="pd") |
| Catalog copyright records (status:"copyright") | 60 | 0 | no src field exists; nothing stored or rendered |
| Artist-page galleries (js/artworks.js) | 532 | 529 | rendered in app |
| Museum photos (js/museums-1.js photo.src) | 103 | 103 | rendered in app |
| Prerendered stub metadata (p/**, 679 files, og:/twitter:image) | 1096 | 502 | public metadata references (crawlable regardless of app gating) |
| Homepage metadata (index.html) | 1 | 1 | public metadata reference |

## Cross-surface reconciliation

- Total unique assets across all public surfaces: **799**
- Rendered-in-app unique: **798**; metadata-only (referenced but never rendered in app): **1**
- Catalog∩gallery overlap: 91 unique URLs appear on both surfaces
- Copyright-suppressed URLs leaking into public stub metadata: **0** (the 60
  copyright-walled records carry no image URL anywhere, so no suppressed
  asset can leak)
- Deltas vs the challenge's superseded figure (783 at 3c2e9fa): +2 catalog
  (Sol's 2b0e18d), +1 gallery, +103 museum photos and +1 homepage ref that
  the earlier count omitted, minus double-counting — the revision's dispute
  of 783 is CONFIRMED; 799 unique URLs at effa805 is the frozen figure.

## Rights-evidence sample basis (criterion 11)

Mandatory inclusions: Tier 1 ∪ daily pool (75 works), every Matisse and
Kahlo gallery record in js/artworks.js, stratified reachable gallery
records to reach ≥100 total. The register records per entry: asset id,
surface, source page, exact-match result, asserted rights basis,
attribution obligation, verification date, status, disposition.
