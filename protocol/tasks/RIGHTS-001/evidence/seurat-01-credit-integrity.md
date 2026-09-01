# Seurat — data-integrity audit of the credit-required set

**Provenance.** Produced by `claude-data-steward` (Seurat) for RIGHTS-001 round
3, on owner authorisation. His declared OP-RIGHTS remit is "verifies a claimed
basis against the file it describes"; E-006 had been found without him
(decision record D-002).

**Verified before filing.** The painter-as-author finding (§3) was checked
independently against the Commons API: `Mrs. Siddons` returns extmetadata
`Artist = Joshua Reynolds` under CC BY 2.0 while its wikitext names
`Rennett Stowe`; `Max Beckmann, Departure` returns `Artist = Max Beckmann` under
CC BY 2.0 while its wikitext names `Allie_Caulfield`. Both hold. Recorded as
E-010.

**Scope note:** all 23 files were fetched live on 2026-09-02 with no 429s and
nothing unverified. This report reaches no legal conclusion (OD-5); it records
what pages assert, what Pigment records, and whether they match.

---

## 1. Licence and author strings: no drift

For all 23 files, Pigment's recorded `license`, `licenseUrl` and `author` are
**character-identical** to the API's `LicenseShortName`, `LicenseUrl` and
`Artist` today. **Zero recorded-licence-version mismatches.** The census
(regenerated 2026-08-30) has not drifted.

Two pages assert more than Pigment records:

| File | Page asserts | Pigment records | Code |
|---|---|---|---|
| `File:Chaïm_soutine,_il_piccolo_pasticcere,_1922-23_ca..JPG` | `{{self\|GFDL\|Cc-by-sa-3.0\|author=I, [[User:Sailko\|Sailko]]}}` — two licences | `CC BY-SA 3.0` only | `commons_rights.py:52-53` reads one licence field |
| `File:Isenheimer_Altar_(Colmar)_jm01221_deriv.jpg` | `Attribution` = `© Jörgens.mi`; licence transcluded from `{{User:Joergens.mi/licence}}` | author `joergens.mi`; the `Attribution` string unused | `build_photo_credits.py:156` — `attribution` is only a fallback after `author` |

## 2. Accounts vs recorded names

Classifying each file by the identifier inside the **raw** `Artist` HTML, before
stripping:

| Identifier class | Files | Distinct identifiers |
|---|---|---|
| Commons account (`/wiki/User:…`, incl. redlinks) | 15 | **12** |
| en.wikipedia article — the *painter*, not an account | 3 | 3 |
| Flickr person URL | 2 | 2 |
| Bare text, no identifier at all | 3 | — |
| **Total** | **23** | — |

**12 distinct Commons accounts stand behind the 15 account-backed files; Pigment
records 13 distinct strings for them.**

**One account under more than one recorded name — the E-006 collision, and it is
four files:**

| Account | Recorded as | File |
|---|---|---|
| `User:Sailko` | `Sailko` | `Chaïm_soutine,_il_piccolo_pasticcere…JPG` |
| `User:Sailko` | `Sailko` | `Katsushika_Hokusai,_tempesta…jpg` (`black-fuji`) |
| `User:Sailko` | `Sailko` | `Peter_Paul_Rubens_-_Descent_from_the_cross_(1617).jpg` |
| `User:Sailko` | **`Francesco Bini`** | `Paul_gauguin,_vahine_no_te_tiare…02.jpg` |

No other account splits.

**Named licensor and uploader are different accounts** on two files:
`Descent from the Cross` was uploaded by `Odecalchi` as `{{Extracted from|…}}`
while its `photo license = {{self|cc-by-3.0}}` names `[[User:Sailko|Sailko]]`;
`Pieta_de_Michelangelo_-_Vaticano.jpg` was uploaded by `Tetraktys` with author
`original file by [[User:Glimz|Stanislav Traykov]]`.

**Two further display-text divergences of the same class**, latent because each
account currently holds one file: `User:MiguelHermoso` → `Miguel Hermoso
Cuesta`; `User:Glimz` → `original file by Stanislav Traykov` (a fragment, not a
name).

## 3. Reverse failure: recorded author is not a photographer

Three entries record the **original painter**, and the page's own markup says so
machine-readably — the anchor points at an `en.wikipedia.org` biography, not a
`User:` page:

| Record / file | Pigment records | Page's actual photographer | Painter died |
|---|---|---|---|
| `the-ten-largest-no-9` | `Hilma af Klint` | none named — bare `{{Artwork}}` + `{{cc-by-sa-4.0}}` | 1944 |
| `Max_Beckmann,_Departure.jpg` | `Max Beckmann` | wikitext `\|author=Allie_Caulfield`, `{{FlickreviewR…reviewlicense=cc-by-2.0}}` | 1950 |
| `Mrs._Siddons_as_the_Tragic_Muse_(3051182537).jpg` | `Joshua Reynolds` | wikitext `*Author: [https://www.flickr.com/people/10393601@N08 Rennett Stowe]`; `[[Category:Photographs by Rennett Stowe]]` | 1792 |

A fourth, `Osman_I_miniature_by_Nakkaş_Osman.jpg`, records `Nakkaş Osman` — but
there the *page itself* writes `|author= Nakkaş Osman` as bare text under
`{{cc-by-sa-4.0}}`. Pigment copied the page faithfully. This is the
`triumph-of-death` pattern the baseline §3 already recorded, still live in three
or four places.

## 4. The tooling defect — exact location

The identity is present in the API response and destroyed by one regex,
`tools/commons_rights.py:118`:

```python
s = re.sub(r"<[^>]+>", "", s)
```

`Artist` arrives as HTML. Two examples fetched today:

```
File:Katsushika_Hokusai,…  <a href="//commons.wikimedia.org/wiki/User:Sailko" title="User:Sailko">Sailko</a>
File:Paul_gauguin,_vahine… <a href="//commons.wikimedia.org/wiki/User:Sailko" title="User:Sailko">Francesco Bini</a>
```

The two records differ **only** in the text node. Line 118 keeps the text node
and discards the `href` — the sole account identifier — and line 203
(`rec[field] = strip_html(...)` inside `rights_from_imageinfo`) applies it to
`("Artist", "artist")` at line 56. From there the loss is permanent:
`tools/audit_artwork_rights.py:122` writes `"author": cr.strip_html(...)` into
the census, and `tools/build_photo_credits.py:156` can only re-flatten already
flat text. **`build_photo_credits.py` is not the defect — it never receives the
identifier.** The same line also discards the `en.wikipedia.org` hrefs that mark
§3's painter-authors, and the Flickr `people/` hrefs.

**Minimal fix (not implemented).** In `rights_from_imageinfo`
(`commons_rights.py:188–204`), before line 203 strips the value, capture the
first anchor's `href` from the raw `Artist` into a new record field
`author_href`, leaving the raw string otherwise untouched. Carry it through
`audit_artwork_rights.py:122` as a sibling key. Roughly four lines; changes no
existing field, no rendered credit, and no count. **The rendered author string
should not be rewritten as a side effect** — the display text is what each file
page asks for, and choosing to override it is an owner decision, not a tool's.
Once the field exists, a ratchet alongside `TestPdTokenAccuracy` can fail when
one `author_href` maps to more than one recorded string — exactly the condition
that produced E-006, caught at build time.

## 5. Not verified, and why

- Whether `User:Sailko` and "Francesco Bini" are one natural person. Commons
  asserts the link only by the wikilink target. Off-Commons identity sources were
  not consulted.
- Provenance of `Artist` on `4_hilma_af_klint,…jpg`: the wikitext is a bare
  `{{Artwork}}` with no author parameter, yet extmetadata resolves to the
  painter's en.wikipedia article with `source: commons-desc-page`. What fills it
  was not determined.
- Who applied each bare CC tag. Current revision plus first upload log entry were
  read; page histories were not walked.
- Whether the three Flickr accounts still carry the recorded names. Not queried.
- Whether any rendered credit satisfies any licence version — outside this remit
  and outside OD-5.
- The 3 "no identifier" and 2 Flickr-only files cannot be checked for account
  collision at all; the extraction discarded nothing there.

## Risks, severity-tagged

1. *Major* — one photographer credited as two people (`User:Sailko`, 4 files);
   undetectable by any current test.
2. *Major* — 3 entries name a painter dead 76–234 years as the author of a
   CC-licensed file; a 4th does so because the page does.
3. *Minor* — 2 further account/display divergences latent, non-colliding today.
4. *Minor* — `Isenheimer` requests `© Jörgens.mi`; Pigment renders `joergens.mi`.
5. *Minor* — `Chaïm soutine` asserts two licences; Pigment records one.
6. *Informational* — no licence-version drift; no unverified fetch.
