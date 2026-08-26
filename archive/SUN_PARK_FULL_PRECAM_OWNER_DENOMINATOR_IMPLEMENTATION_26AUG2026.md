# Sun Park full pre-CAM owner denominator — implementation record

**Control:** `PD-SP-UNIT-OWNER-LEDGER-001`  
**Date:** 26 August 2026  
**Status:** implemented as a public-safe, source-graded denominator; title and transfer reconciliation remains open.

## Result

The derivative source schedule headed **“Datos Propietarios Hotel Sun Park May 2008–Feb 2022 / Propietarios Pre-CAM 2008–2017”** has now been transcribed into the controlled owner ledger as:

- **72 exact unit or premises rows**;
- **2 aggregate LPB rows** preserved as source expressions;
- **74 source rows in total**;
- **62 exact rows carrying the source classification `DIRECT`**;
- **10 exact rows carrying the source classification `BANCO`**;
- **5 exact rows whose source owner label also references Matkator**;
- **1 duplicated finca group in the source**: finca `8652`, reported for both units `902` and `903`.

No private email address, telephone number, postal address, passport/identity number, bank-account information, mailbox identifier or local evidence path is published.

## Non-collapse rules

1. **NON-LPB/MATKATOR OWNER ≠ MONTELANZA/MOLINA DISSIDENT.**
2. `DIRECT` and `BANCO` reproduce the source schedule’s `CONTACTO` classification only. They are not treated as seller, deed, payment, conveyance or Registry proof.
3. Every exact owner row defaults to the **other-minority / non-adverse** ownership edge unless a separate dated source establishes another relationship.
4. AP89 litigation alignment, LPB-origin provenance, representation, Matkator association and later CAM acquisition remain separate temporal edges.
5. An option to purchase is not a completed transfer.
6. The two aggregate LPB rows are not arithmetically converted into invented unit-level titles.

## Parallel sources preserved

The AP89/JV1260 source and the later pre-CAM owner schedule remain parallel. The ledger does not overwrite:

- the `403` / `453` unit-set mismatch;
- the owner-attribution differences for units `503` and `908`;
- the 2009 option over `907` and `908`;
- the 2010 owner/representation instruments for `801`, `802` and `805`;
- the duplicated source finca `8652` for `902` and `903`;
- the still-unresolved twelve-unit LPB transfer cohort;
- the unresolved Multimatrix/Multimetrics and any later Osborne endpoint.

## What is now closed

The **source denominator itself** is closed at 72 exact rows plus two aggregate rows, subject to correction if a better original schedule is produced.

## What remains open

The following require primary documents:

1. the 18 AP89 unit-to-finca mappings;
2. the 12 individual LPB disposal deeds and Registry histories;
3. option exercise/completion for `907` and `908`;
4. the transfer/enforcement chain for `801`, `802` and `805`;
5. resolution of `403`/`453`, `503`, `908`, and duplicated finca `8652`;
6. date-specific representatives for each meeting and proceeding;
7. later CAM/Acosta Matos acquisitions without rewriting earlier provenance;
8. the exact Multimatrix/Multimetrics and any Osborne chain.

## Controlled files

- `assets/data/sun-park-unit-owner-ledger-v1.json`
- `assets/data/sun-park-unit-owner-ledger-v1.precam-full-denominator.json`
- `assets/data/sun-park-unit-owner-ledger-v1.precam-full-denominator.tsv`
- `assets/data/sun-park-unit-owner-ledger-v1.reconciliation.json`
- `scripts/validate_sun_park_unit_owner_ledger.py`
- `scripts/validate_sun_park_full_owner_denominator.py`
- `es/registro-propietarios-sun-park/index.html`
- `en/sun-park-owner-register/index.html`

The existing bilingual provenance page remains the wider contextual explanation. The two new public routes render the complete public-safe source denominator with searchable, filterable rows and the semantic perimeter legend.
