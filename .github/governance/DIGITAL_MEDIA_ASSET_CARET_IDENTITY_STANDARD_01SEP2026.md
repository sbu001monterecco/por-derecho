# Digital/media asset caret identity standard — 1 September 2026

**Control ID:** `PD-DMA-GOV-001`  
**Status:** active repository-wide identity and continuity control  
**Scope:** posters, infographics, screenshots, social-media cards, video stills, diagrams, promotional-looking satire, email attachments and other digital/media assets.

## 1. What `^` means for a digital/media asset

A digital/media reference receives a terminal caret only when the exact file identity has been fixed by, at minimum:

- SHA-256 of the complete file bytes;
- byte length;
- MIME type / file format;
- pixel dimensions where applicable; and
- a durable asset reference in the machine register.

Example: `PD-DMA-20260901-0003-ES^`.

For digital/media assets, the caret means **exact byte identity verified**. It does **not** mean that:

- every statement in the image is factually established;
- the image is approved for publication;
- the file depicts ownership, guilt, intent or responsibility accurately;
- a person or entity shown has endorsed the image; or
- a visual derivative is identical to its parent.

This media caret is separate from CAEPR person/entity identity reconciliation. The two systems must not be conflated.

## 2. Family, edition and immutable file

Every asset is handled at three levels:

1. **Creative family** — the continuing concept or campaign, for example `PD-DMA-FAM-AMHP-001`.
2. **Edition** — language, layout and purpose, such as the Spanish “No es lo mismo” edition.
3. **Immutable file** — one exact byte object, carrying a caret only after hash verification.

A corrected export is a new immutable asset. It never silently replaces the old hash. A crop, compression, translation, colour correction or web derivative receives its own reference and points to its parent.

## 3. Reference grammar

Preferred immutable reference:

`PD-DMA-YYYYMMDD-NNNN-LANG^`

Optional derivative qualifier:

`PD-DMA-YYYYMMDD-NNNN-LANG-WEB^`

Where:

- `PD-DMA` = Por Derecho digital/media asset;
- date = control or creation date;
- number = unique sequence;
- language = `ES`, `EN`, `BI` or `NA`;
- caret = exact byte identity verified.

Reserved references without a completed file do not carry a caret.

## 4. Mandatory machine fields

The register must preserve:

- reference and family ID;
- title and language;
- asset type and intended channels;
- SHA-256, bytes, dimensions and MIME when caret-confirmed;
- source/provenance and generation method;
- parent/derivative relationships;
- repository/public URL or an explicit binary-mirror gap;
- publication status;
- factual/evidential status;
- required disclaimer;
- correction or supersession state; and
- any name, portrait, hotel-roster or ownership limitations.

## 5. Publication states

Controlled values include:

- `HASH_LOCKED_EXTERNAL_ARTIFACT_PENDING_REPOSITORY_MIRROR`
- `PUBLIC_WEB_DERIVATIVE`
- `DESIGN_REFERENCE_NOT_FOR_PUBLICATION`
- `PUBLICATION_AUTHORISED_SUBJECT_TO_GOVERNANCE`
- `RESERVED_PENDING_GENERATION`
- `SUPERSEDED_BUT_PRESERVED`
- `WITHDRAWN_FROM_PUBLIC_USE_BUT_PRESERVED`

Publication status and factual status are always separate.

## 6. Satire and caricature

A satirical asset must also comply with:

- `.github/governance/SATIRE_CARICATURE_SPOOF_PUBLICATION_STANDARD_ES_EN.md`;
- `ops/SATIRE_CARICATURE_SPOOF_GOVERNANCE_V1.json`; and
- any family-specific role, identity and evidence controls.

The mandatory Spanish short disclosure is:

> **CARICATURA / REPRESENTACIÓN SATÍRICA — NO ES UN ANUNCIO REAL**

The mandatory English short disclosure is:

> **SATIRICAL / CARICATURE REPRESENTATION — NOT A REAL ADVERTISEMENT**

A disclaimer does not cure an invented fact. Exact names, roles, ownership edges, figures and dates still require source control.

## 7. Current Acosta Matos hotel-platform family

`PD-DMA-FAM-AMHP-001` contains:

- concept version 1: high-contrast “spoof advertisement” grid;
- concept version 2: vintage resort-clearance composition;
- publication version 3: Spanish “12 hoteles · 2.500 habitaciones · +100 M€ / No es lo mismo”;
- a reserved English translation; and
- reserved corrected versions inspired by versions 1 and 2.

The first two files are retained as **design references only** because their inherited labels, portraits and ownership implications are not the canonical factual roster. They must not be republished as evidence sheets. The third file is the controlled current Spanish publication asset.

## 8. Binary-storage and continuity rule

Where an exact original binary cannot be committed through the available write channel, its hash-locked reference remains valid with an explicit `repository_mirror_gap`. A lower-resolution web derivative may be committed under a separate caret reference. The original must never be falsely described as present in the repository when only a derivative is present.

## 9. Corrections and takedown

A correction never destroys the prior byte record. The register must show:

- what changed;
- why;
- who authorised publication or withdrawal;
- which reference is current for each channel; and
- whether a public URL now serves a derivative, correction notice or replacement.

## 10. Current source of truth

Machine register: `assets/data/digital-media-asset-registry-v1.json`  
Public register: `/es/registro-activos-digitales/` and `/en/digital-media-asset-register/`  
Current family landing pages: `/es/acosta-matos-plataforma-hotelera/` and `/en/acosta-matos-hotel-platform/`.
