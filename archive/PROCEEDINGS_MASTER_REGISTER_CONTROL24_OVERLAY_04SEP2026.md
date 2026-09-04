# PROCEEDINGS MASTER REGISTER — CONTROL 24 IDENTITY OVERLAY

**Overlay ID:** `PD-PMR-CONTROL24-OVERLAY-20260904`  
**Canonical graph node:** `CONTROL-24`  
**Reserved master integration ID:** `GC-DEC-024`  
**Status:** controlling identity overlay pending the next safe deterministic rebuild of `archive/PROCEEDINGS_MASTER_REGISTER.csv`  
**Effective:** 4 September 2026

## Purpose

This overlay makes **Control 24 a first-class canonical repository object** without fabricating an official judicial identity that the controlled evidence does not establish.

It must be read together with:

- `archive/PROCEEDINGS_MASTER_REGISTER.csv`;
- `archive/PROCEEDINGS_MASTER_REGISTER_PROTOCOL.md`;
- `data/control-22-24-interconnection-register.json`;
- `data/concurso36-accountability-triangle-v1.json`;
- `governance/prompts/TRIANGLE_CONTROL_21_22_24_CONTINUITY.md`; and
- the bilingual public Control 24 pages.

The Master Register protocol permits a source-control overlay to govern a material identity correction or addition until the complete canonical CSV and its public derivative can be safely regenerated. This overlay is narrowly scoped to Control 24.

## Canonical identity

| Field | Controlling value |
|---|---|
| Master integration ID | `GC-DEC-024` |
| Canonical graph ID | `CONTROL-24` |
| Record type | `INTAKE_REFERENCE` |
| Is proceeding | `FALSE` |
| Proceeding class | `RECEPTION_LOCATOR_NOT_PROCEEDING` |
| Stream | Criminal intake / judge-related complaint |
| Geography | Gran Canaria |
| Origin organ | Decanato de los Juzgados de Las Palmas de Gran Canaria |
| Current custodian | Unresolved |
| Reference | Handwritten daily intake/reference 24 |
| Secondary reference | Complaint presented 18 June 2026; dependent supplement presented 25 June 2026 |
| NIG | None established |
| Diligencias Previas | None established |
| Date or period | 18–25 June 2026 |
| Connection | Concurso Ordinario 36/2012 / judge-accountability layer |
| Object or purpose | Reception locator for a written complaint/notitia criminis concerning identified judicial acts and supervision in Concurso 36/2012 |
| Status | Physical presentation and later supplement documented; official reparto, NIG, competent destination, incoación, inadmission, referral, archive and current custodian not located in the controlled corpus |
| Source status | `VERIFIED_PRIMARY_WITH_OFFICIAL_DESTINATION_GAP` |
| Public treatment | `PUBLIC_SUMMARY_DO_NOT_PUBLISH_RAW_PERSONAL_DATA` |
| Open reference gap | Certified Decanato/TSJC intake and reparto record; complete transmitted inventory; assigned organ; NIG/procedural number; every signed decision, notice and finality/current-status record |

## Binding evidential boundary

`Control 24` is canonical for retrieval, continuity, graph traversal and cross-proceeding analysis. It is **not**:

- a NIG;
- a Diligencias Previas number;
- proof of reparto;
- proof that the TSJC or another court opened a criminal proceeding;
- a formal querella;
- proof that a querella has been filed;
- an admission or merits determination; or
- proof of judicial misconduct, prevaricación, corruption, coordination, intent or guilt.

The public-safe formulation remains:

> A complaint/notitia criminis was presented on 18 June 2026 under the daily Decanato locator recorded as Control 24, followed by a dependent supplement on 25 June 2026. Its official allocation, procedural identity, destination and outcome remain unresolved in the controlled corpus.

## Required links

The canonical node must remain bidirectionally reachable from:

1. `C36-NEXUS` — Concurso Ordinario 36/2012;
2. `CONCURSO-JUDGE` — the separate judge-accountability vertex;
3. `C24-SUPPLEMENT-25JUN2026` — the dependent 25 June supplement;
4. `GC-GOV-019` — CGPJ DI 169/2026;
5. `CGPJ-169-AMPLIACION` — later/ampliación material in the CGPJ route;
6. `GC-GOV-020` — Recurso de alzada 286/2026;
7. `GC-FIS-017` — Fiscalía DIP 2/2026, as a separate file sharing judge-related material/context;
8. the intended or later querella lane, only with the explicit status `FORMAL_FILING_NOT_VERIFIED` unless a filing receipt is controlled;
9. `GC-APP-004` — RPL 2523/2025, through the common Concurso 36/2012 nucleus rather than false joinder; and
10. the AC and private-actor vertices through typed evidential/contextual edges, never by liability transfer.

## No silent merge with existing records

Do not silently merge Control 24 into:

- `GC-HC-010`, whose exact high-court registration and procedural identity remain unverified;
- `GC-FIS-017 / DIP 2/2026`;
- `GC-GOV-019 / DI 169/2026`;
- `GC-GOV-020 / Alzada 286/2026`;
- `GC-CRI-008 / DP 1901/2026`;
- `GC-CRI-009 / DP 1956/2026`; or
- any querella, complaint or supervision route not proved by a primary identity bridge.

Common subject matter, documents or actor references create a typed interlink, not a single proceeding.

## Master CSV integration instruction

At the next safe full rebuild:

1. add one and only one Master Register row using reserved ID `GC-DEC-024` and the fields above;
2. preserve `CONTROL-24` as the stable public/graph alias;
3. regenerate `assets/data/proceedings-master-public-v1.json` through the deterministic builder;
4. add the Control 24 public routes to the controlled projection where policy permits;
5. run all Master Register, interconnectivity and triangle validators;
6. update this overlay to `INTEGRATED_IN_MASTER` with the exact commit and generated-source hash; and
7. retain the overlay as provenance rather than deleting it.

Until those steps are complete, this overlay controls the Control 24 identity and prevents its disappearance, duplication or procedural upgrade.

## Continuity rule

Any successor thread, agent or maintenance workflow that touches the judge, CGPJ, Fiscalía, calificación, AC, private-actor or Concurso 36/2012 tracks must load `data/concurso36-accountability-triangle-v1.json` and this overlay before changing Control 24. A missing Control 24 node, a non-null NIG/DP added without primary proof, or an unqualified statement that a querella/proceeding exists is a governance failure.
