# Digital/media asset caret identity standard — 1 September 2026

**Control ID:** `PD-DMA-GOV-001`  
**Status:** active repository-wide identity and continuity control  
**Scope:** posters, infographics, screenshots, social-media cards, video stills, diagrams, promotional-looking satire, email attachments and other digital/media assets.

## 1. Logical asset versus exact file

A reusable creative/publication item receives a stable logical reference such as `PD-DMA-0001`. A terminal caret is reserved for one **exact byte object**.

Examples:

- `PD-DMA-0001` — logical Spanish publication asset;
- `PD-DMA-0001^` — exact public SVG manifestation recorded in the machine register;
- `PD-DMA-0001-PNG^` — exact full-resolution PNG outreach master of the same logical asset.

A caret is assigned only when the exact file identity is fixed by, at minimum:

- SHA-256 of the complete bytes;
- byte length;
- MIME type / format;
- dimensions or SVG viewBox where applicable; and
- a durable file reference in the canonical register.

The caret means **file identity verified**. It does not certify that every statement in the image is factually established, that the file is publishable, that an ownership implication is correct, that a depicted person endorsed it, or that any person or entity has knowledge, intent or responsibility.

This namespace is separate from CAEPR person/entity identity reconciliation.

## 2. Reference grammar

Logical asset:

`PD-DMA-NNNN`

Exact current web file:

`PD-DMA-NNNN^`

Exact alternate manifestation:

`PD-DMA-NNNN-<FORMAT_OR_PURPOSE>^`

Examples: `PD-DMA-0002-PNG^`, `PD-DMA-0003-PRINT^`.

Historical concepts that remain identified but are quarantined use `PD-DMA-LEGACY-NNNN-<FORMAT>^`.

Language, layout, source, family, channel and editorial state are machine metadata; they do not need to be encoded into every reference.

## 3. Immutability and derivatives

A crop, compression, translation, correction, redesign or re-export creates a distinct exact file identity. A hash is never silently reused. Logical creative continuity may remain, but every byte object stays independently traceable.

If an outreach master cannot be mirrored in the repository, its caret remains valid only if the canonical register records the hash-locked binary-mirror gap. A web derivative must carry its own exact reference.

## 4. Mandatory register fields

The canonical register records logical reference, family, title, language, role, exact file references, SHA-256, bytes, format, dimensions, provenance/generation method, public/repository path or binary-mirror gap, publication status, factual/evidential status, source claims, required disclaimer, parent/derivative relationships, correction state and material limitations.

## 5. Satire and caricature

Satirical assets additionally comply with `.github/governance/SATIRE_CARICATURE_SPOOF_PUBLICATION_STANDARD_ES_EN.md`, `ops/SATIRE_CARICATURE_SPOOF_GOVERNANCE_V1.json` and family-specific controls.

Mandatory short disclosures:

> **CARICATURA / REPRESENTACIÓN SATÍRICA — NO ES UN ANUNCIO REAL**

> **SATIRICAL / CARICATURE REPRESENTATION — NOT A REAL ADVERTISEMENT**

A disclaimer never cures an invented or unsupported factual assertion. Names, roles, ownership edges, figures and dates remain source-controlled.

For named people, the visual-asset identity lock and CAEPR name status are
independent. A `LOCKED_CANONICAL_REPOSITORY_ASSET` portrait does not authorise a
full-name caret, a dated professional capacity, a present affiliation or a
satirical function label. Apply the mandatory display hierarchy in section 9.1
of the satire standard and record the person in the satire compliance register.

## 6. Current hotel-platform family

`PD-DMA-FAM-AMHP-001` currently publishes:

- `PD-DMA-0001` — Spanish “12 hoteles · 2.500 habitaciones · +100 M€ / No es lo mismo”;
- `PD-DMA-0002` — English companion;
- `PD-DMA-0003` — corrected high-contrast/platform-catalogue variant inspired by the earlier first direction; and
- `PD-DMA-0004` — corrected fictional-clearance variant inspired by the earlier second direction.

The two earlier generated concepts are retained only as `PD-DMA-LEGACY-*` design references. Their inherited hotel roster, portraits and apparent ownership/agency framing are not approved factual content and must not be republished unchanged.

## 7. Publication and evidential states remain separate

An exact file can be hash-verified and still be `DO_NOT_PUBLISH_UNCHANGED`. Conversely, a public SVG can be approved for display while its factual propositions remain attributed statements or analytical questions rather than adjudicated facts.

## 8. Correction and takedown

Corrections preserve the former file identity and record what changed, why, the replacement reference, channel status and whether the public URL now serves a replacement, correction notice or withdrawn state.

## 9. Source of truth

Canonical machine register: `data/digital-media-asset-register-v1.json`  
Legacy redirect: `assets/data/digital-media-asset-registry-v1.json`  
Public registers: `/es/registro-activos-digitales/` and `/en/digital-media-asset-register/`  
Family pages: `/es/acosta-matos-plataforma-hotelera/` and `/en/acosta-matos-hotel-platform/`.
