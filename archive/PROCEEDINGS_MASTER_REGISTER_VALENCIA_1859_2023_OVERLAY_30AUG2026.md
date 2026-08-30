# PROCEEDINGS MASTER REGISTER — VALENCIA ORD 1859/2023-9 OVERLAY

**Date:** 30 August 2026  
**Status:** controlling additive new-row overlay pending safe canonical CSV insertion  
**Gap key:** `GAP-VAL-CAIXABANK-01859-2023`

## Purpose

The canonical `archive/PROCEEDINGS_MASTER_REGISTER.csv` currently lacks the exact Aweswell Limited v CAIXABANK, S.A. Valencia proceeding identified in the source-controlled public dossier. Until a safe full-CSV rewrite allocates a permanent unused Master ID, this overlay must be read together with the master register.

This is a **missing-row overlay**, not a correction that merges the proceeding into an existing row.

## Exact proceeding identity

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
- `Connection`: `historic banking / financial-product package; Bankia enforcement; Concurso 36/2012; hotel-asset economic history`
- `Object_or_Purpose`: `Nullity/restitution and subsidiary damages concerning the mortgage/floor/swap/refinancing/pledge/account/enforcement package, as described in the controlled public dossier`
- `Status`: `Pending and contested`
- `Latest_Known_Event`: `Signed court diligence dated 6 Nov 2025 relisted hearing for 28 Jan 2027 at 10:00`
- `Source_Status`: `VERIFIED_PRIMARY_DERIVED_PUBLIC_CONTROL`
- `Repo_Canonical_Source`: `en/caixabank-valencia-claim/index.html` / `es/reclamacion-caixabank-valencia/index.html`
- `Open_Reference_Gap`: `Permanent unused Master_ID and physical canonical CSV insertion; native/certified completion remains separately tracked in the Valencia dossier`
- `Public_Treatment`: `PUBLIC_CONTROLLED`

## Master ID rule

Do **not** invent or reuse a Master ID in this overlay. Before physical insertion:

1. inspect the complete current CSV denominator;
2. identify the next valid unused identity under the controlling Proceedings Master Register protocol;
3. preserve this gap key and overlay path in the new row's provenance/notes or correction trail; and
4. confirm no collision with `ES-VAL-CIV-048` or another Valencia record.

## Non-conflation

`ORD 1859/2023-9` is **not admitted as the same proceeding as `ES-VAL-CIV-048`**. Their descriptions differ. A later primary source can establish a relationship only through a transparent correction; similarity of territory or banking subject matter is insufficient.

## Convergence links to preserve

This proceeding must remain discoverable from the wider graph through source-graded bridges to:

- the original Caja Insular / La Caja de Canarias → BFA → Bankia → CaixaBank banking/product lane;
- Arrecife Mortgage Enforcement 90/2012;
- Concurso 36/2012 and the underlying economic/asset history;
- the later mortgage-credit assignment/title lane, kept legally separate;
- the Administrador Concursal witness-origin record; and
- calificación/recovery analysis.

These are material convergence relationships, not a finding that the separate proceedings are legally joined or that the Valencia court has adopted Por Derecho's wider allegations.

## Retirement condition

This overlay remains controlling until an exact row is inserted into `archive/PROCEEDINGS_MASTER_REGISTER.csv`, the public Master Proceedings Register and Proceedings Interconnectivity Map are checked for propagation, and a provenance-preserving closeout records the overlay as retired.
