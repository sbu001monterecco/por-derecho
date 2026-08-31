# Ricardo de Mosteyrín + justice-professionals caret continuity audit

**Date:** 31 August 2026

**Base `main`:** `e313c13bf46464015a72025dcd9264e61ec33107`

**Branch:** `codex/ricardo-mosteyrin-justice-professionals-caret-20260831`

**State at creation:** `PREPARED_PENDING_MERGE`

**Control ID:** `PD-SP-JUSTICE-PROFESSIONALS-CARET-20260831-01`

## 1. User instruction preserved

Create a dedicated page for Ricardo de Mosteyrín Sampalo, interlink it with E.G. 745/2026, Calificación / RPL 2523/2025, DP 1901/2026 and related proceedings; bring named Ministerio Fiscal / Fiscalía members, judges, LAJs, notaries and named Property Registry staff into `^` identity control; and add continuity-audit and governance controls.

## 2. Implementation inventory

### Dedicated bilingual identity page

- `es/ricardo-de-mosteyrin-sampalo/index.html`
- `en/ricardo-de-mosteyrin-sampalo/index.html`
- canonical identity: `PD-SP-P-0058`

The page separates:

- signed 12-March-2019 prosecution opinion — personal act proved;
- 25-July-2023 hearing — institutional attendance proved; individual identification attributed by Gil and certification pending;
- RPL 2523/2025 — related appeal, no new personal act attributed;
- DP 1901/2026 — prosecution report/signatory and later judicial act not located in the reviewed corpus;
- E.G. 745/2026 — institutional inspection lane signed by other identified actors, with no personal E.G. act attributed to Ricardo; and
- current official capacity under BOE-A-2026-1094 — identity/capacity evidence, not file assignment or knowledge.

### Role-wide public census

- `es/registro-identidad-profesionales-justicia/index.html`
- `en/justice-professionals-identity-register/index.html`
- `assets/data/justice-professionals-caret-audit-v1.json`
- `.github/governance/NAMED_JUSTICE_PROFESSIONAL_CARET_COVERAGE_PROTOCOL_31AUG2026.md`
- `scripts/validate_justice_professionals_caret.py`

### Canonical registry

The existing Ricardo record is upgraded with bilingual routes, the BOE source and explicit non-attribution to RPL 2523/2025, DP 1901/2026 and E.G. 745/2026. Alberto López Villarrubia's existing record receives the missing explicit `CARET_CONFIRMED` source control. New stable person IDs run from `PD-SP-P-0114` through `PD-SP-P-0144`; no existing ID is changed or reused.

## 3. Finite denominator

| Role | Named | Confirmed ^ | Pending | Control note |
|---|---:|---:|---:|---|
| Ministerio Fiscal / Fiscalía | 17 | 17 | 0 | signed actors plus exact public office-holders in the unitary record |
| Judges / magistrates | 15 | 15 | 0 | dated signed acts or official panel records; formation boundaries preserved |
| LAJs | 8 | 8 | 0 | dated signed acts; court-office act kept separate from judicial merits |
| Notaries | 8 | 5 | 3 | three source literals lack the linked primary deed/official record |
| Property Registry people | 0 | 0 | 0 | institution and generic roles only; no exact individual name located |
| **Total people** | **48** | **45** | **3** | **93.75%** |

**Verdict:** `PARTIAL — NOT ALL IS^`.

## 4. Exact pending identities

1. `PD-SP-P-0138` — Carmen Martínez Socias: obtain the primary 23-May-2008 LPB incorporation deed or official notarial record.
2. `PD-SP-P-0139` — Nicolás Quintana Plasencia: obtain the primary 3-Jan-2012 deed or official notarial record.
3. `PD-SP-P-0143` — Pedro Eugenio Botella Torres: obtain primary protocol 1,377 dated 27-May-2010 or an official notarial record.

These names remain visible as source literals with `CARET_PENDING`. They do not display `^`.

## 5. Property Registry finding

The reviewed corpus names `Registro de la Propiedad de Tías`, Registry entries, presentation data, properties and alleged or documented Registry effects. It also uses generic words such as `Registrador` or `personal del Registro`. No exact individual Registry person name was located in the finite search.

Therefore:

- denominator of exact named Registry people: `0`;
- no person ID or caret is invented;
- the institution remains separately controlled; and
- the first primary source containing exact name, dated capacity and act must trigger a new CAEPR row and audit revision.

`NO EXACT NAME LOCATED` does not mean that no individual exists in the official file.

## 6. Source hierarchy and fairness controls

The execution uses signed judicial, prosecutorial and LAJ acts; official BOE and Ministerio Fiscal sources; identified deeds/protocols or signed judicial references; and the existing controlled actor registers. It preserves these non-transfer rules:

- current office ≠ personal handling of every file;
- notification ≠ substantive authorship;
- roster ≠ final deciding formation in another case;
- LAJ processing ≠ judicial merits;
- notarial authorisation ≠ truth, judicial validation, payment or Registry effect;
- institution ≠ named person; and
- identity ≠ conduct, knowledge, intention, coordination, wrongdoing or liability.

## 7. Interlink continuity

Ricardo's dedicated page is the canonical reciprocal target from the Classification, RPL, DP 1901 and E.G. 745 routes. The role census links every confirmed identity to its dedicated route or the CAEPR registry and publishes the three pending notarial exceptions without carets. The sitemap and publication manifest enumerate the four new bilingual public routes. The operational-registry validator limits its proceeding-queue comparison to exact `PROCEEDING` records so pending people cannot be misclassified as pending proceedings.

## 8. Validation and release gates

Before merge:

```text
python3 scripts/validate_justice_professionals_caret.py
python3 scripts/validate_operational_identity_registry.py
python3 scripts/validate_repository_preservation.py
python3 scripts/validate_publication_integrity.py
python3 scripts/validate_audience_experience.py
```

The publication state may progress only through objective branch, PR, CI, merge, Pages and live-readback evidence. This file does not prove its own merge or deployment.

## 9. Post-deployment closeout required

After merge and Pages success:

1. verify HTTP 200 for the four new routes;
2. verify page markers `PD-SP-P-0058` and `PD-SP-JUSTICE-PROFESSIONALS-CARET-20260831-01` or their equivalent visible control text;
3. compare live bytes or hashes with merged source;
4. update the publication manifest with merge SHA, Pages run and live evidence; and
5. write a post-deployment attestation before claiming `LIVE_VERIFIED` or `DELETION_SAFE`.

Until that chain completes, the correct state remains no higher than the objective gate actually reached.
