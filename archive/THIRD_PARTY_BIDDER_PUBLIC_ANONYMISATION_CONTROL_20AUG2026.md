# THIRD-PARTY BIDDER — NAME-ONLY PUBLIC ANONYMISATION CONTROL

**Date:** 20 August 2026  
**Status:** `PUBLICATION CONTROL — USER-DIRECTED NAME-ONLY ANONYMISATION`  
**Applies to:** every public Project Sun Rock / Por Derecho page, repository path, metadata field, shared JavaScript string, caption, alt text, search-facing summary and future adjudication publication.

## Controlling rule

Only the **name** of the third-party bidder associated with the documented proposal dated 8 February 2021 is anonymised.

The bid itself is not anonymised. Its existence, date, EUR 14.8 million amount, identified property perimeter, terms, procedural role, comparison points, communications, treatment, outcome, evidential qualifications and downstream consequences must remain specific, visible and searchable.

No other information falls within the anonymisation scope merely because it may, alone or together with other lawful public facts, assist a reader in inferring who the bidder was.

Spanish controlling formulation:

> **Únicamente se anonimiza el nombre del tercer oferente. La oferta, su importe, fecha, perímetro, términos, tratamiento procesal y todos los hechos y documentos relacionados permanecen íntegramente visibles. Ningún otro dato queda dentro del alcance de la anonimización, aunque pueda contribuir indirectamente a identificar al oferente.**

English controlling formulation:

> **Only the third-party bidder’s name is anonymised. The bid, its amount, date, perimeter, terms, procedural treatment and every related fact and document remain fully visible. No other information falls within the anonymisation scope, even where it may indirectly assist in identifying the bidder.**

## Approved public labels

- Spanish default: **`tercer oferente`**;
- Spanish procedural alternatives, only where the source context requires them: **`tercer postor`** or **`tercero mejorante`**;
- English default: **`third-party bidder`**;
- English source-sensitive alternatives: **`third-party offeror`** or **`competing third party`**.

The strongest public proposition remains:

> **Un tercer oferente documentó el 8 de febrero de 2021 una propuesta de adquisición por 14,8 millones de euros para el perímetro de fincas identificado.**

> **A third-party bidder documented an acquisition proposal dated 8 February 2021 for EUR 14.8 million covering the identified property perimeter.**

## Bid-preservation invariant

The following matters must not be deleted, generalised or reduced to a content-free reference:

- proposal date: 8 February 2021 / 08/02/2021;
- amount: EUR 14.8 million / 14,8 M€;
- identified property perimeter;
- quantified comparison point: EUR 14,713,880.31 / 14.713.880,31 €;
- the distinction between the third-party proposal, the published threshold, CAM’s proposal, the adjudication and the later deed;
- court filing or receipt, authority and funds questions;
- attendance and exact treatment at the 18 May 2021 licitation;
- deed no. 457 dated 21 February 2022;
- EUR 13,168,082.02, the separate EUR 400,000 line and their distinct documentary functions;
- the five-calendar-day court-notification obligation;
- the court, mandamiento, Registry, cancellation, accounting and final-accounts trail;
- the express evidential qualification that the located proposal does not by itself prove admission, full compliance, funding, entitlement to adjudication, wrongful exclusion or wrongdoing.

## Name-token operation

The rewrite control may replace only the protected name token and genuine orthographic, case, spacing, accent or abbreviation variants. It must preserve the surrounding sentence and record, apart from the minimum grammatical adjustment required by the name substitution.

It must not replace a whole sentence, paragraph, source card, table row, chronology entry, document description, filename component or URL component where replacing only the name component is technically possible.

## Native evidence and public derivatives

The unmodified native source remains in the controlled private evidence/custody layer with its provenance, hash, date and source locator. A public derivative may mask or replace only the bidder’s name. Amounts, dates, other actors, clauses, pagination, structure and all other evidential content must remain unaltered.

A public PDF or image derivative must state that only the bidder’s name has been redacted.

## Technical enforcement

`scripts/validate_public_bidder_anonymisation.py` provides two independent controls:

1. **name-absence gate** — uses a one-way hash of the protected token and scans the current public repository tree, relevant filenames and supplied public URLs without storing the name in plaintext;
2. **bid-preservation gate** — requires the bilingual canonical pages and corrections register to retain the controlling name-only wording and the material date, amount, comparison, deed, separate-assets and procedural markers.

`scripts/rewrite_public_bidder_anonymisation.py` remains a deterministic, idempotent name-token replacement tool. It is not a content-redaction tool.

## Scope of clearance

The automated gate can establish current-tree and tested-public-URL clearance. It does not establish that the protected name is absent from historical commits, earlier blobs, commit messages, pull-request metadata, tags or releases.

Any Git-history audit must be reported separately. No destructive history rewrite, force-push, deletion of pull-request material or invalidation of historical links is authorised by this control.

## Companion controls

- `archive/CAM_2022_ADJUDICATION_TRANSACTION_IDENTITY_AND_CONSIDERATION_CONTROL_19AUG2026.md`
- `archive/MISSING_EVIDENCE_REGISTER_CAM_2022_ADJUDICATION_ADDENDUM_19AUG2026.md`
- `archive/SUN_PARK_MASTER_STORYLINE_2022_ADJUDICATION_RECONCILIATION_ADDENDUM_19AUG2026.md`
- `es/adjudicacion-2022-reconstruccion-documental/index.html`
- `en/2022-adjudication-documentary-reconstruction/index.html`
- `es/correcciones-control-versiones/index.html`
- `en/corrections-version-control/index.html`

## Publication principle

> **Anonymise only the bidder’s name; preserve the complete bid and the complete surrounding record.**
