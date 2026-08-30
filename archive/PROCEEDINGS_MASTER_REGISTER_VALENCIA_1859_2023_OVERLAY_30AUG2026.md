# PROCEEDINGS MASTER REGISTER — VALENCIA `VAL-CIV-001` CORRECTION OVERLAY

**Date:** 30 August 2026  
**Status:** controlling additive correction overlay pending physical CSV field consolidation  
**Correction key:** `GAP-VAL-CAIXABANK-01859-2023`

## Purpose

A unitary rerun of the canonical `archive/PROCEEDINGS_MASTER_REGISTER.csv` located the already-existing Valencia master identity:

`VAL-CIV-001` — `JPI nº 27 Valencia` — `Procedimiento 1859/2023`.

That is the same litigation now source-controlled as **Aweswell Limited v CAIXABANK, S.A., ORD 1859/2023-9, NIG 46250-42-1-2023-0049579**.

The earlier characterization of this file as a **missing-row/new-ID overlay** is superseded. No second master identity is to be created.

This overlay corrects and enriches the existing `VAL-CIV-001` row until a safe full-CSV rewrite consolidates the fields physically.

## Controlling corrected fields for `VAL-CIV-001`

- `Master_ID`: `VAL-CIV-001`
- `Is_Proceeding`: `TRUE`
- `Record_Type`: `JUDICIAL_PROCEEDING`
- `Proceeding_Class`: `DIRECT`
- `Stream`: `Civil / banking / financial products`
- `Geography`: `Valencia`
- `Origin_Organ`: `Juzgado de Primera Instancia nº 27 de Valencia`
- `Current_Custodian`: `Juzgado de Primera Instancia nº 27 de Valencia`
- `Reference`: `ORD 1859/2023-9`
- `Secondary_Reference`: `Aweswell Limited v CAIXABANK, S.A.`
- `NIG`: `46250-42-1-2023-0049579`
- `Date_or_Period`: `2023–2027`
- `Connection`: `historic banking / financial-product package; Bankia enforcement; Arrecife Mortgage Enforcement 90/2012; Concurso 36/2012; hotel-asset economic history`
- `Object_or_Purpose`: `Nullity/restitution and subsidiary damages concerning the mortgage/floor/swap/refinancing/pledge/account/enforcement package, as described in the controlled public dossier`
- `Status`: `Pending and contested`
- `Latest_Known_Event`: `Signed court diligence dated 6 Nov 2025 relisted hearing for 28 Jan 2027 at 10:00`
- `Source_Status`: `VERIFIED_PRIMARY_DERIVED_PUBLIC_CONTROL`
- `Repo_Canonical_Source`: `en/caixabank-valencia-claim/index.html` / `es/reclamacion-caixabank-valencia/index.html`
- `Open_Reference_Gap`: `Physical CSV field consolidation; native/certified completion remains separately tracked in the Valencia dossier`
- `Public_Treatment`: `PUBLIC_CONTROLLED`
- `Last_Scan_Date`: `2026-08-30`

## Why the identity match is admitted

The raw CSV already identifies `VAL-CIV-001` with the same court (`JPI nº 27 Valencia`) and the same proceeding number (`1859/2023`). The later signed-diligence-derived record supplies the complete class suffix, parties, NIG and current hearing. This is a field-completion correction to one proceeding, not a same-name inference between different proceedings.

## No-duplication rule

- Do **not** create a second Valencia row for `ORD 1859/2023-9`.
- Do **not** allocate a new Master ID.
- Preserve `VAL-CIV-001` as the canonical identity.
- Preserve the prior gap/overlay history as a correction trail showing why the earlier missing-row inference was withdrawn.

## Convergence links to preserve

`VAL-CIV-001` must remain discoverable through source-graded analytical bridges to:

- the original Caja Insular / La Caja de Canarias → BFA → Bankia → CaixaBank banking/product lane;
- Arrecife Mortgage Enforcement 90/2012;
- Concurso 36/2012 and the underlying economic/asset history;
- the later mortgage-credit assignment/title lane, kept legally separate;
- the Administrador Concursal witness-origin record; and
- calificación/recovery analysis.

These are material convergence relationships, not a finding that the separate proceedings are legally joined or that the Valencia court has adopted Por Derecho's wider allegations.

## Retirement condition

This overlay remains controlling until the physical `VAL-CIV-001` row in `archive/PROCEEDINGS_MASTER_REGISTER.csv` is consolidated, the public Master Proceedings Register and Proceedings Interconnectivity Map are checked for propagation, and a provenance-preserving closeout records this overlay as retired.
