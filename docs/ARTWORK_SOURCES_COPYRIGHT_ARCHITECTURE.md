## Artwork Sources & Copyright Architecture

**Audience:** ChatGPT Theory Team
**Product:** Pigment
**Status:** Proposed operating model; requires jurisdiction-specific legal review before launch

### Executive recommendation

Pigment should pursue Artify-scale aggregation, but it should not treat Artify's apparent catalogue breadth as evidence that every displayed image has been cleared. The defensible strategy is:

> **Aggregate artwork records broadly; render media narrowly.**

Pigment can build a very large discovery graph from public collection metadata, open-access museum datasets, institutional APIs, and rights-filtered aggregators. It should display an image only when a machine-readable rights record supports the exact product use. A work may therefore exist in Pigment as a searchable, linkable, listable artwork record even when no image can be shown.

The target is not merely “200,000 artwork records.” It is:

> **200,000+ normalized artwork records, with independently auditable rights provenance for every rendered media asset.**

This approach preserves catalogue scale, supports modern and contemporary artists, and makes copyright discipline part of Pigment’s product infrastructure rather than a manual afterthought.

### 1. Why a large catalogue is technically achievable

Major cultural institutions already publish collection data at machine scale. The Met, for example, makes basic data on accessioned works—including identifying data for works still under copyright—available under CC0, while its API supplies corresponding high-resolution images when those images are part of the Open Access program. The Met currently describes more than 492,000 public-domain images as available for unrestricted use. The Smithsonian similarly separates open metadata from media: restricted objects may have CC0 metadata while the API withholds the media file. Rijksmuseum publishes collection information and high-resolution images as openly as possible, but explicitly marks exceptions. The Art Institute of Chicago exposes fields such as `is_public_domain`, `is_zoomable`, `max_zoom_window_size`, and `copyright_notice`.

Together with Wikimedia Commons and Europeana, these sources make a six-figure catalogue feasible without negotiating a separate bilateral agreement for every public-domain work.

The key architectural insight is that “present in an API” is not a single permission state. An API response can contain:

- factual or descriptive metadata;
- a media URL intended for the source institution’s own interface;
- an open-licensed media asset;
- a copyrighted image exposed for reference but not reusable by a third party;
- a thumbnail whose permitted uses differ from those of the full-resolution file; or
- a rights statement that is incomplete, stale, territorial, or supplied by a third party.

Accordingly, API availability is an ingestion signal—not a rights grant.

### 2. The three-layer rights model

Pigment must model three legally and operationally distinct layers.

#### 2.1 Artwork

The intellectual and cultural object: for example, *The Starry Night*, Vincent van Gogh, 1889, Museum of Modern Art. The artwork record contains normalized identity, creator, date, medium, dimensions, movements, subjects, locations, and institutional identifiers.

The artwork’s copyright status answers whether the underlying work is protected in a relevant territory. It does **not** by itself answer whether Pigment may use a particular photograph or scan.

#### 2.2 Media asset

A specific digital file or delivery endpoint: a museum photograph, scan, crop, thumbnail, IIIF canvas, user upload, or licensed reproduction. One artwork may have multiple assets with different creators, resolutions, crops, colour profiles, source institutions, and permissions.

An underlying artwork may be in the public domain while a particular media asset carries separate contractual, neighbouring-rights, database-rights, privacy, trademark, or other restrictions. In the European Union, Article 14 of Directive (EU) 2019/790 limits new copyright or related rights in non-original reproductions of public-domain visual art, but it does not erase every contractual, database, access, moral-rights, or non-copyright obligation.

#### 2.3 Rights grant

The evidence that permits Pigment to perform specified actions with a specified asset. A rights grant may derive from public-domain status, CC0, a Creative Commons licence, a direct artist agreement, a museum or image-agency contract, a collecting-society licence, or another documented authorization.

A grant must describe allowed product behavior—not merely contain a label such as “licensed.” Thumbnail display, full-screen display, zoom, offline caching, download, feed syndication, social sharing, editorial use, advertising, and model training are separate permissions and should not be inferred from one another.

### 3. Source strategy

#### Tier A — open-access institutional sources

Start with sources that provide stable identifiers, clear machine-readable rights signals, high-quality metadata, and public-domain or permissively licensed media. Priority candidates include:

| Source | Recommended use | Rights handling |
|---|---|---|
| The Met Open Access | Artwork metadata at scale; public-domain images | Ingest all allowed metadata; ingest/render images only when the record and source policy identify them as Open Access/public domain |
| Rijksmuseum Collection Online | Metadata and high-resolution assets | Respect the per-item copyright notice; allow broad use only for PDM/CC0 or another licence compatible with the intended feature |
| Smithsonian Open Access | CC0 metadata and media | Require the asset’s CC0 designation; do not infer media permission from the existence of restricted-object metadata |
| Art Institute of Chicago API | Metadata, IIIF delivery, explicit rendering controls | Enforce `is_public_domain`, zoomability, maximum zoom, copyright notice, and source guidance at render time |
| Wikimedia Commons | Free-licensed and public-domain media | Store and validate the individual file-page licence; generate attribution and ShareAlike obligations; retain source and revision evidence |
| Europeana | Cross-institution discovery and rights-filtered ingestion | Treat `edm:rights` or equivalent as an input, not conclusive proof; render only statements compatible with Pigment’s commercial use and independently retain the contributing institution’s record |

Pigment should prefer the authoritative holding institution over an aggregator when the same object is available from both. Aggregators remain valuable for discovery, identifier reconciliation, and source expansion.

#### Tier B — metadata-first protected works

Protected modern and contemporary works can still be part of Pigment’s knowledge graph when a lawful metadata basis exists. A metadata-only record may support:

- search and artist pages;
- titles, dates, media, dimensions, movements, exhibitions, and holding institutions;
- relationships to artists, places, styles, and other works;
- following, list membership, recommendations, and outbound links; and
- an explicit “Image unavailable due to copyright” state.

Metadata-first handling prevents the recommendation engine from being limited to works for which Pigment already holds display rights. When a valid media licence is later obtained, the asset and its rights grant can be attached without rebuilding the artwork graph.

This path still requires source-level review. Descriptive text can itself be creative; databases may carry sui generis or contractual restrictions; biographies and curatorial essays must not be copied merely because factual fields are reusable. Pigment should distinguish factual fields, source-authored prose, controlled vocabularies, and third-party database content during ingestion.

#### Tier C — licensed contemporary catalogues

For protected works, Pigment should develop several complementary licensing paths:

1. **Collecting societies and rights agencies.** Explore repertoire or blanket agreements with organizations such as ADAGP, Artists Rights Society, DACS, GESAM, and relevant territorial partners. A licence request must cover the actual app experience: websites and native apps, territories, audience, duration, commercial model, thumbnails, full-screen display, zoom, caching, sharing, and promotion.
2. **Museums, galleries, estates, and image agencies.** Negotiate both the underlying artwork rights and the photographic/media rights where these are controlled by different parties. Buying or obtaining a photograph does not automatically clear the artwork reproduced in it; ADAGP explicitly warns that photographic rights and reproduction rights can be separate.
3. **Direct artist licensing.** Offer verified artists a non-exclusive digital-display agreement with clear, granular permissions. The agreement should address ownership warranties, authority to license uploaded media, permitted surfaces, resolution, cropping, moderation, revocation prospectively, attribution, reporting, takedown, and sublicensing strictly necessary to operate Pigment.
4. **Artist or estate claim flow.** Allow a rights holder to claim an existing metadata profile, correct information, submit assets, choose permissions, and sign or accept the applicable licence. Claim status must never retroactively validate assets collected from unrelated sources.

### 4. Artist claim and upload licensing

Artist onboarding can turn contemporary-art clearance into an acquisition loop rather than a compliance burden.

The recommended flow is:

1. Verify the claimant’s identity and relationship to the artist or estate.
2. Require work-level ownership and authority declarations.
3. Record whether the claimant controls the underlying work, the uploaded photograph, or both.
4. Present a plain-language, non-exclusive grant with granular feature toggles.
5. Capture the operative terms, version, acceptance timestamp, signatory identity, and evidence package.
6. Scan uploads for duplicates, conflicting claims, embedded watermarks, and source inconsistencies.
7. Place assets in review until both identity and rights checks pass.
8. Expose transparent credit and licence status on the artwork page.

An artist-facing permission interface should not promise complete deletion from backups or downstream caches where that is technically untrue. It should distinguish withdrawal of future public display from termination of already valid third-party uses, and it should preserve the audit history even when an asset is no longer rendered.

### 5. Risk tiers and rendering policy

Rights confidence must be converted into deterministic product behavior.

| Risk tier | Typical evidence | Production policy |
|---|---|---|
| **R0 — Verified Open** | PDM/CC0 from authoritative source; compatible asset and work status | Full display, high resolution, zoom, feed, lists, and commercial use; download/offline/share only if independently enabled by policy |
| **R1 — Verified Conditional** | CC BY, CC BY-SA, or a clear institutional licence | Render only with automatic attribution and all licence obligations; enforce adaptation and ShareAlike constraints where applicable |
| **R2 — Directly Licensed** | Executed artist, estate, museum, agency, or society agreement | Enable only the uses, territories, duration, resolutions, and channels enumerated in the grant |
| **R3 — Metadata Only** | Protected work with a lawful metadata basis, but no display grant | No Pigment-hosted or embedded artwork image; show metadata, provenance, rights notice, and an outbound institutional link |
| **R4 — Rights Unknown or Conflicted** | Missing, ambiguous, contradictory, expired, or unverifiable evidence | Quarantine asset; do not render in production; route to review |

Core rule:

> **Unknown rights are not “probably acceptable.” Unknown rights mean no image.**

Feature gates should be deny-by-default. A renderer should require an active grant whose territory, channel, date range, commercial-use flag, and requested action all match the request context. If no matching grant is found, it should return the metadata-only state.

The system must also support emergency suppression. A single kill switch should prevent an asset from appearing in search, feeds, caches, thumbnails, share cards, notifications, recommendation previews, and downstream exports while preserving the underlying evidence and audit trail.

### 6. Recommended data model

#### Artwork

```text
Artwork
  id
  canonical_title
  alternate_titles[]
  creator_ids[]
  creation_date_text
  creation_date_start
  creation_date_end
  medium
  dimensions
  classification
  subjects[]
  movement_ids[]
  holding_institution_id
  accession_number
  source_identifiers[]
  canonical_source_url
  underlying_work_status
  status_basis
  status_territories[]
  status_as_of
```

#### MediaAsset

```text
MediaAsset
  id
  artwork_id
  source_id
  source_asset_id
  source_url
  delivery_url
  storage_object_key
  asset_type
  mime_type
  width
  height
  file_hash
  crop_description
  photographer_or_digitizer
  media_rights_holder
  media_rights_status
  source_last_modified_at
  ingested_at
  quarantined_at
  suppression_reason
```

#### RightsGrant

```text
RightsGrant
  id
  artwork_id
  media_asset_id
  grant_type
  licensor
  rights_holder
  licence_uri
  agreement_or_evidence_id
  evidence_url
  evidence_snapshot_hash
  attribution_text
  copyright_notice
  allowed_territories[]
  allowed_channels[]
  commercial_use_allowed
  thumbnail_allowed
  full_display_allowed
  zoom_allowed
  download_allowed
  offline_cache_allowed
  social_share_allowed
  promotional_use_allowed
  derivatives_allowed
  model_training_allowed
  max_resolution
  valid_from
  valid_until
  revocation_status
  verification_status
  verified_by
  verified_at
  risk_tier
  notes
```

The schema should also include `Source`, `Institution`, `Creator`, `EvidenceSnapshot`, `Claim`, `TakedownCase`, and immutable `RightsDecisionEvent` entities. A rights label without its evidence and decision history is not sufficient provenance.

### 7. Ingestion and decision architecture

```text
Source adapters
      ↓
Raw immutable records + evidence snapshots
      ↓
Field-level normalization and identifier reconciliation
      ↓
Artwork entity resolution / deduplication
      ↓
Media extraction (separate from artwork metadata)
      ↓
Rights parser and policy mapping
      ↓
Automated validation + conflict detection
      ↓
Risk tier assignment
      ↓
Human review queue for ambiguity or protected works
      ↓
Publish Artwork / MediaAsset / RightsGrant independently
      ↓
Runtime policy engine → allow, transform, attribute, or deny
```

Operational requirements:

- Store the raw source response and a timestamped snapshot of the rights evidence used for each decision.
- Version source adapters and policy rules so Pigment can explain why an asset was rendered at any point in time.
- Revalidate grants on a schedule and whenever the source record, licence URI, agreement, or copyright notice changes.
- Detect conflicts across sources; the most permissive label should never automatically win.
- Prefer work- and asset-specific grants over source-wide assumptions.
- Separate ingestion from publication. A successfully downloaded file remains quarantined until its grant passes policy.
- Propagate licence requirements into presentation automatically: credit line, source link, licence link, modification notice, and ShareAlike handling.
- Maintain territorial evaluation. “Life plus 70” is not a global boolean, and publication history, nationality, restoration, neighbouring rights, and local exceptions can matter.
- Treat model training, embeddings made from pixels, and other machine-learning uses as separate permissions. Display permission must not be repurposed as training permission.

### 8. Product-facing rights provenance

Pigment should make rights status legible without overwhelming the experience. Each rendered artwork should display a concise, expandable provenance line such as:

- **Public Domain · Rijksmuseum**
- **CC0 · The Met Open Access**
- **CC BY-SA 4.0 · Creator via Wikimedia Commons**
- **© Artist · Licensed to Pigment**
- **Image unavailable due to copyright**

The expanded view should include the source, rights holder, applicable licence, required attribution, and a correction or rights-claim route. This is both a trust feature and a partnership asset: institutions and artists can see that Pigment preserves provenance instead of stripping it away.

### 9. Explicit non-assumptions

Pigment must not base its catalogue policy on any of the following:

- “The museum API returned an image URL.”
- “The image is already on the internet.”
- “The app is educational.”
- “The source institution owns the physical painting.”
- “The artist is categorized as modern.”
- “The work is old enough in one country.”
- “The image is only a thumbnail.”
- “Another commercial app displays it.”
- “The platform can remove it if someone complains.”

None of these statements, alone, is a reusable rights grant. Notice-and-takedown is a safety process, not a licensing strategy. Likewise, Artify’s availability in an app store is not evidence that a platform or app-store reviewer cleared its artwork rights.

### 10. Implementation sequence

#### Phase 1 — rights-safe scale

- Integrate a small set of authoritative open-access sources.
- Build the Artwork / MediaAsset / RightsGrant separation.
- Publish only R0 assets.
- Implement evidence snapshots, attribution generation, suppression, and audit logs.

#### Phase 2 — conditional open licences and metadata breadth

- Add Wikimedia Commons and rights-filtered Europeana ingestion.
- Support R1 obligations and conflict review.
- Expand protected artists as metadata-only R3 records.
- Add source revalidation and territorial policy.

#### Phase 3 — contemporary licensing

- Launch verified artist and estate claims.
- Pilot direct non-exclusive licences with a small cohort.
- Negotiate agency, collecting-society, museum, gallery, and estate pathways.
- Add contract-level feature, territory, term, and resolution enforcement.

#### Phase 4 — rights intelligence as a moat

- Measure clearance rates, rights conflicts, stale grants, takedowns, review times, and attribution compliance.
- Improve entity resolution and rights-confidence scoring without allowing confidence scores to override required evidence.
- Offer institutions and artists provenance analytics and correction workflows.

### Decision

Pigment should adopt the aggregation logic that plausibly enables Artify’s scale, while declining to copy any opaque or unverifiable copyright posture. The catalogue can be broad because artwork identity and factual metadata are separable from image display. The media experience can be rich because public-domain, CC0, permissively licensed, and directly licensed assets are separable from unknown or protected ones.

The durable product principle is therefore:

> **Ingest broadly. Preserve provenance. License explicitly. Render deterministically.**

### Primary references

- [The Met — Open Access](https://www.metmuseum.org/hubs/open-access)
- [The Met Collection API](https://metmuseum.github.io/)
- [Art Institute of Chicago API documentation](https://api.artic.edu/docs/)
- [Rijksmuseum Collection Online and data services](https://data.rijksmuseum.nl/about/)
- [Rijksmuseum Information and Data Policy](https://data.rijksmuseum.nl/policy/)
- [Smithsonian Open Access FAQ](https://www.si.edu/openaccess/faq)
- [Wikimedia Commons — Reusing content](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia/licenses/en)
- [Europeana Publishing Framework](https://pro.europeana.eu/post/publishing-framework)
- [Europeana — Identifying and clearing copyright](https://pro.europeana.eu/page/identifying-copyright-in-collection-items)
- [Europeana Data Exchange Agreement](https://pro.europeana.eu/page/the-data-exchange-agreement)
- [Directive (EU) 2019/790, Article 14](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CONSIL:PE_51_2019_REV_1)
- [Creative Commons licence overview](https://creativecommons.org/share-your-work/cclicenses/)
- [ADAGP online licence application](https://www.adagp.fr/en/online-licence-application)
- [Artists Rights Society — Digital Media Licensing Guide](https://arsny.com/wp-content/uploads/2024/12/LicensingGuide_DigitalMedia.pdf)
- [DACS licensing](https://www.dacs.org.uk/licensing)
