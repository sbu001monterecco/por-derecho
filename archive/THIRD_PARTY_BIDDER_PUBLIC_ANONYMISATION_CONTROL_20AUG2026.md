# THIRD-PARTY BIDDER — PUBLIC ANONYMISATION CONTROL

**Date:** 20 August 2026  
**Status:** `PUBLICATION CONTROL — USER-DIRECTED ANONYMISATION`  
**Applies to:** all public Project Sun Rock / Por Derecho website pages, metadata, shared JavaScript copy, image captions, alt text, search-facing summaries and future public adjudication materials.

## Controlling rule

The legal/corporate identity of the third party that produced the February-2021 acquisition proposal is **not required for the public evidential proposition and must remain anonymised on the website**.

Preferred labels:

- Spanish: **`tercer oferente`**, **`tercer postor`** or **`tercero mejorante`**, according to the source/procedural context;
- English: **`third-party bidder`**, **`third-party offeror`** or **`competing third party`**.

The strongest public proposition is:

> **Un tercer oferente documentó el 8 de febrero de 2021 una propuesta de adquisición por 14,8 millones de euros para el perímetro de fincas identificado.**

English:

> **A third-party bidder documented an acquisition proposal dated 8 February 2021 for EUR 14.8 million covering the identified property perimeter.**

## Why this is sufficient

The public issue is the **existence and treatment of real competition** inside the 2021 better-posture process, not the identity or reputation of the competing party.

Anonymisation therefore does not weaken the evidential point. It sharpens it:

`PUBLICITY / THRESHOLD → CONCRETE THIRD-PARTY PROPOSAL → PROCEDURAL TREATMENT → RESULT → EFFECT FOR THE ESTATE`.

## Evidential boundary

The located proposal document supports the existence, date, stated amount and transaction perimeter of the proposal. It does **not yet establish**, without the remaining court/financial record:

- exact court filing/receipt and timestamp;
- satisfaction of every published condition;
- corporate authority;
- actual availability of funds;
- binding acceptance;
- attendance/non-attendance and treatment at the 18-May-2021 licitation;
- whether the proposal should legally have prevailed;
- any wrongdoing in the eventual result.

Those questions remain finite source-completion tasks.

## Public-source hygiene

Do not place the protected bidder identity in:

- public HTML;
- title or description metadata;
- JavaScript-rendered public copy;
- image filenames/captions/alt text;
- RSS, sitemap descriptions or structured public data;
- public-facing source-card titles;
- future public URLs or anchors.

Private/native source systems may retain the original legal identity and filename for evidential retrieval. Public repository controls should use a generic source label plus the private source locator where required.

## Technical enforcement

`scripts/validate_public_bidder_anonymisation.py` scans public website source using a one-way hash of the protected token rather than storing the identifier in plaintext. The dedicated GitHub Actions gate runs on relevant website changes and on pushes to `main`.

## Companion controls

- `archive/CAM_2022_ADJUDICATION_TRANSACTION_IDENTITY_AND_CONSIDERATION_CONTROL_19AUG2026.md`
- `archive/MISSING_EVIDENCE_REGISTER_CAM_2022_ADJUDICATION_ADDENDUM_19AUG2026.md`
- `archive/SUN_PARK_MASTER_STORYLINE_2022_ADJUDICATION_RECONCILIATION_ADDENDUM_19AUG2026.md`
- `es/adjudicacion-2022-reconstruccion-documental/index.html`
- `en/2022-adjudication-documentary-reconstruction/index.html`

## Publication principle

> **Anonymise the bidder; preserve the competitive fact.**

The website should make the existence, amount, timing and unresolved procedural treatment of the third-party proposal visible without identifying the third party.
