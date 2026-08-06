# Font licences — Pigment

Pigment self-hosts its two webfonts so that a visiting browser makes **no
third-party request**. These files are byte-identical to the ones the site
previously fetched from `fonts.gstatic.com` at runtime; nothing was
re-generated, re-named, or modified.

Recorded by Dürer (Implementation Lead) for PIG-001 unit 20, honoring owner
decision **OD-3** (`protocol/tasks/PIG-001/owner-decisions-r2.md`). Retrieved
2026-07-25.

---

## Playfair Display

- **Licence:** SIL Open Font License, Version 1.1
- **Licence text:** `OFL-Playfair-Display.txt` in this directory
- **Copyright:** Copyright 2017 The Playfair Display Project Authors
  (https://github.com/clauseggers/Playfair-Display), with Reserved Font Name
  "Playfair Display"
- **Designer:** Claus Eggers Sørensen
- **Upstream source:** https://fonts.google.com/specimen/Playfair+Display
- **Licence source:** https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/OFL.txt
- **Google Fonts metadata:** `license: ofl` (https://fonts.google.com/metadata/fonts/Playfair%20Display), last modified 2025-09-11
- **Binary version served:** `v40` (from the `fonts.gstatic.com/s/playfairdisplay/v40/` path)
- **Reserved Font Name note:** the RFN clause restricts *modified* versions from
  using the name. These files are unmodified and keep the original name, so the
  clause is satisfied.

## Inter

- **Licence:** SIL Open Font License, Version 1.1
- **Licence text:** `OFL-Inter.txt` in this directory
- **Copyright:** Copyright 2020 The Inter Project Authors
  (https://github.com/rsms/inter)
- **Designer:** Rasmus Andersson
- **Upstream source:** https://fonts.google.com/specimen/Inter
- **Licence source:** https://raw.githubusercontent.com/google/fonts/main/ofl/inter/OFL.txt
- **Google Fonts metadata:** `license: ofl` (https://fonts.google.com/metadata/fonts/Inter), last modified 2025-09-10
- **Binary version served:** `v20` (from the `fonts.gstatic.com/s/inter/v20/` path)
- **Reserved Font Name note:** none declared in the Inter OFL header.

---

## Files committed

Both families are shipped as **variable** woff2 files — one file covers every
weight the site uses, which is why 16 `@font-face` declarations in
`css/styles.css` resolve to only 6 binaries.

| File | Bytes | SHA-256 | Retrieved from |
|---|---|---|---|

| `inter-normal-latin-ext.woff2` | 85,272 | `a28eb6d3ccb534ae0c94ca999371df024aab60b08c3c8a5720ee9e32fa0faaa2` | https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa25L7W0Q5n-wU.woff2 |
| `inter-normal-latin.woff2` | 48,432 | `c940764593d0fe5d596be327ca7558855e018039fb78509aa21921fd3644c3e4` | https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7W0Q5nw.woff2 |
| `playfair-display-italic-latin-ext.woff2` | 13,684 | `ac9c3bcc1848b07cf06fb1e1ff6159bb81404f9e0ed265ec0b7f1431cb3805f1` | https://fonts.gstatic.com/s/playfairdisplay/v40/nuFRD-vYSZviVYUb_rj3ij__anPXDTnCjmHKM4nYO7KN_qiTXt_A-X-uE0qEE5Do.woff2 |
| `playfair-display-italic-latin.woff2` | 21,952 | `ce3932af6f6a6c7321b6f27462213c432f0be6ef2e242d0adf7f8981562a961f` | https://fonts.gstatic.com/s/playfairdisplay/v40/nuFRD-vYSZviVYUb_rj3ij__anPXDTnCjmHKM4nYO7KN_qiTXtHA-X-uE0qEEw.woff2 |
| `playfair-display-normal-latin-ext.woff2` | 20,980 | `5628567856d60d714e7a35bcac9e3de08b336d63b12138f61b970990a1ee9547` | https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTLYgEM86xRbPQ.woff2 |
| `playfair-display-normal-latin.woff2` | 38,460 | `5d91eb5d522a03081946c44c8ca17c902230dfed5f0f9b5014262135d47b15b2` | https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgEM86xQ.woff2 |

Total: 228,780 bytes across 6 files.

## Subsets shipped

Only the **latin** and **latin-ext** subsets are committed. The Cyrillic,
Cyrillic-ext, Greek, Greek-ext and Vietnamese subsets offered by Google Fonts
are deliberately omitted: a character audit of `index.html`, `css/` and all of
`js/` found zero characters in those ranges. The `unicode-range` descriptors in
`css/styles.css` are copied verbatim from the Google Fonts `css2` response, so a
browser selects exactly the same file for exactly the same characters as before.

## Weight mapping (unchanged from the previous remote stylesheet)

The declarations reproduce the previous request
`Playfair Display:ital,wght@0,400;0,600;0,800;1,400` and `Inter:wght@300;400;500;600`
exactly. `font-weight:700`, used twice in `css/styles.css` (`.main-nav a.active`,
`.tone.on::after`), resolved to Inter 600 before this change and still does,
because the same discrete weights are declared. No typeface was substituted.
