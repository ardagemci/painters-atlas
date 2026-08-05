# Pigment — Public Asset Inventory at a1b822b

Enumerated 2026-08-05 by static analysis of the repository at a1b822b
(regenerate: `python3 tools/asset_inventory.py`; JSON detail in asset-inventory-a1b822b.json).
"Unique asset" means a unique upload.wikimedia.org URL string; distinct
thumbnail widths of the same Commons file count separately, so unique
underlying files may be slightly fewer. No network requests were made;
reachability is derived from code gating, not fetches.

## Exact counts by surface

| Surface | References | Unique assets | Reachability |
| --- | --- | --- | --- |
| Catalog artwork images (js/catalog-1..4.js, status:"pd") | 257 | 257 | rendered in app (gate: app.js status==="pd") |
| Catalog copyright records (status:"copyright") | 66 | 0 | no src field exists; nothing stored or rendered |
| Artist-page galleries (js/artworks.js) | 528 | 528 | rendered in app |
| Museum photos (js/museums-1.js photo.src) | 104 | 104 | rendered in app |
| Prerendered stub metadata (p/**, 695 files, og:/twitter:image) | 1096 | 502 | public metadata references (crawlable regardless of app gating) |
| Homepage metadata (index.html) | 2 | 1 | public metadata reference |

## Cross-surface reconciliation

- Total unique assets across all public surfaces: **798**
- Rendered-in-app unique: **797**; metadata-only (referenced but never rendered in app): **1**
- Catalog∩gallery overlap: 92 unique URLs appear on both surfaces
- Copyright-suppressed URLs leaking into public stub metadata: **0**
