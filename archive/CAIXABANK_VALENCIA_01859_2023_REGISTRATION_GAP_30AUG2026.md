# CAIXABANK / VALENCIA ORD 1859/2023-9 — MASTER-REGISTER RECONCILIATION CONTROL

**Date:** 30 August 2026  
**Status:** SOURCE-TREE CONSOLIDATION COMPLETE — public/main closure effective when the corrective commit merges and deploys
**Durable correction key:** `GAP-VAL-CAIXABANK-01859-2023`

## 1. Exact controlled identity — verified

The repository's source-controlled public CaixaBank/Valencia dossier records, from a signed court diligence dated 6 November 2025:

- **Parties:** Aweswell Limited v CAIXABANK, S.A.;
- **proceeding:** Ordinary Proceeding `[ORD] 1859/2023-9`;
- **court:** Juzgado de Primera Instancia nº 27 de Valencia;
- **N.I.G.:** `46250-42-1-2023-0049579`;
- **current hearing:** **28 January 2027 at 10:00**;
- **status:** pending and contested; no merits judgment or adjudicated recovery located in the controlled public record.

Canonical public sources:

- `en/caixabank-valencia-claim/index.html`
- `es/reclamacion-caixabank-valencia/index.html`

The earlier correspondence-only formulation (`01859/2023`, January 2027 day not primary-confirmed) is superseded for identity and scheduling by the signed-diligence-derived controlled record.

## 2. Rerun correction — the proceeding was already registered

A 30 August 2026 unitary rerun of the complete canonical CSV located this existing row:

`VAL-CIV-001,,JUDICIAL_PROCEEDING,TRUE,CONTEXTUAL,Civil,Valencia,JPI nº 27 Valencia,JPI nº 27 Valencia,Procedimiento 1859/2023,...`

The exact court and proceeding number establish that `VAL-CIV-001` is the already-existing master identity for this litigation. Therefore the earlier statement that the CSV contained no row for the Valencia proceeding was incorrect and is superseded.

There is **no basis to create a second Valencia master identity** for the same proceeding merely because the existing row is incomplete.

## 3. Canonical consolidation completed; source-completion gaps remain

The prior **field-completeness / canonical-consolidation defect** is closed. On 30 August 2026, the canonical `VAL-CIV-001` row was physically updated without creating a duplicate identity.

`VAL-CIV-001` now contains these controlling corrected fields:

- `Proceeding_Class`: `DIRECT`
- `Stream`: `Civil / banking / financial products`
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
- `Open_Reference_Gap`: `Native/certified file completeness, pleadings, merits disposition, service and finality remain tracked in the Valencia dossier`
- `Public_Treatment`: `PUBLIC_CONTROLLED`

Operational status:

**VERIFIED / CANONICALLY CONSOLIDATED — canonical identity is `VAL-CIV-001`; source-level identity, NIG, court and hearing are verified. Native/certified file completeness, pleadings, merits disposition, service and finality remain separate open-source questions.**

## 4. Retired correction overlay

The correction was governed during consolidation by:

`archive/PROCEEDINGS_MASTER_REGISTER_VALENCIA_1859_2023_OVERLAY_30AUG2026.md`

That file is now **retired as a controlling layer** and preserved as the provenance trail for the correction of existing row `VAL-CIV-001`. It was never a basis for a missing-row/new-ID duplicate.

## 5. Unitary convergence — verified as a material analytical bridge

The public dossier itself cross-reconciles the banking claim with:

- the 2008–2010 financing / swap / floor / second-facility / pledge package;
- Bankia enforcement;
- Arrecife Mortgage Enforcement 90/2012;
- Insolvency / Concurso 36/2012;
- the later Bankia → SAREB → PH122 → CAM mortgage-asset lane;
- the Administrador Concursal witness-origin chronology; and
- calificación/recovery analysis.

Public-safe wording:

> **Separate Valencia proceeding; directly relevant to the historic banking/financial-product package, enforcement chronology and the underlying economic history that intersects with Concurso 36/2012 and the hotel assets. Canonical identity: `VAL-CIV-001`; canonical field consolidation is complete.**

This does **not** mean the Valencia court has adopted Por Derecho's insolvency, criminal, causation or liability allegations.

## 6. Private-source boundary

Separate professional correspondence may show additional strategic recognition of the Valencia–concursal relationship. Private or privileged strategy is not needed to establish the public bridge and must not be automatically published.

## 7. Non-duplication rule

After physical CSV consolidation:

- do not create a second master row for `ORD 1859/2023-9`;
- preserve `VAL-CIV-001` as the canonical identity;
- preserve this correction key and the overlay as the provenance trail;
- use the canonical CSV fields for repository-wide proceedings analysis; and
- retain this control and the retired overlay as the durable provenance trail.

## 8. Closure condition

**Source-tree consolidation completed 30 August 2026.** The corrective branch's physical `VAL-CIV-001` CSV row contains the verified fields above; local Master Proceedings Register and Proceedings Interconnectivity Map audits pass; and the overlay records retirement without loss of provenance. Public/main closure becomes effective only when this corrective commit merges and deploys. Closure of this reconciliation control does not close the separately stated native/certified-file, pleadings, merits, service or finality gaps.
