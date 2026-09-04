# Controls 22 / 24 publication handover — 4 September 2026

## Continuity classification

`RELATED_CONTINUITY_ACTIVE_MULTI_TRACK`

## Base

- repository: `sbu001monterecco/por-derecho`
- base branch: `main`
- base commit observed before branch creation: `56761b5fa7a06579b3db563d859d75c65fb0a0b6`
- working branch: `publish-controls-22-24-04sep2026`

## Source-control findings preserved

### Control 22

- reported presentation date: 18 June 2026;
- subject: acts/omissions of Francisco de Borja Rodríguez-Batllori Laffitte as Insolvency Administrator in Insolvency 36/2012;
- controlling candidate located: `01_Denuncia_Penal_AC_LPB_Sun_Park_AC-FINAL_17JUN2026.pdf`;
- candidate length: 55 pages;
- document states it is a complaint/notitia criminis, not a formal querella;
- repository public record identifies DP 1956/2026 as the later actor-specific criminal route;
- exact Control 22 → DP 1956/2026 linkage remains source-controlled and must not be inferred solely from numbering;
- published DP 1956 state: provisional dismissal communicated 21 July 2026, not a final merits judgment.

### Control 24

- reported presentation date: 18 June 2026;
- subject: specified judicial acts/rulings attributed to Alberto López Villarrubia in Insolvency 36/2012;
- controlling candidate located: `02_Paquete_Unificado_Para_Presentacion_JUEZ_ FINAL 17JUNE2026 (signed).pdf`;
- unified package length: 79 pages; principal complaint: 31 pages;
- package states it is a written criminal complaint/notitia criminis, not a formal querella or formal appearance;
- intended addressee printed on the package: Civil and Criminal Chamber of the High Court of Justice of the Canary Islands;
- no official NIG, DP number, allocation, opening, dismissal or TSJC remittal is published as verified at this cut;
- `Control 24` remains a presentation locator, not a judicial case number.

### 25 June 2026 supplement

- dependent supplement intended to join Control 24;
- not an autonomous complaint;
- preserve 18 June as original complaint date and 25 June as real supplement-entry date;
- reported handwritten annotations/physical joining are traceability facts/allegations to verify, not proof of falsification, backdating or obstruction.

## Interconnection rule

The release implements the following architecture:

- Control 21 / DP 1901/2026 = private-actor layer;
- Control 22 / DP 1956/2026 = Insolvency Administrator own-act/own-omission layer;
- Control 24 = judicial-act/ruling layer;
- DI 169/2026 / Alzada 286/2026 = separate CGPJ institutional/supervisory layer;
- DIP 2/2026 = separate prosecutorial antecedent;
- removal/fees/calificación appeals remain separate judicial routes.

The controls are interlinked for documents, knowledge, authority, decisions, effects, benefit/harm and preservation. They are not automatically joined and no culpability transfers between actors.

## Querella rule

Control 24 is now publicly described as an antecedent and documentary basis for a potential or prepared querella. It must **not** be described as a filed querella unless a specific querella and official filing proof are located and the documentary bridge is verified.

## New public routes

Spanish:

- `/es/controles-22-24-18-junio-2026/`
- `/es/control-24-denuncia-juez-concurso-36-2012/`

English:

- `/en/controls-22-24-18-june-2026/`
- `/en/control-24-judge-complaint-insolvency-36-2012/`

Machine-readable control:

- `assets/data/controls-22-24-18jun2026-v1.json`

## Continuity invariants

1. Control 22 is not itself DP 1956/2026; preserve the linking source.
2. Control 24 is not a proceeding number.
3. Control 24 is not a querella.
4. The 25 June supplement is not an autonomous complaint absent official proof otherwise.
5. Prepared ≠ filed; filed ≠ allocated; allocated ≠ opened; provisional dismissal ≠ final merits judgment.
6. Related ≠ joined; shared evidence ≠ shared responsibility.
7. Unknown remains unknown until a primary official source changes it.
8. Branch/PR/merge/deployment/live-readback are separate publication states.

## Open primary-source gaps

- complete official filing/reparto bridge for Control 22 → DP 1956/2026;
- official current status/court route for Control 24;
- official registration and routing record for the 25 June supplement;
- any verified querella filing based on Control 24;
- certified full dockets needed for each challenged judicial-act nucleus.

## Publication-state rule

This handover records repository work only. Do not mark the routes `LIVE_VERIFIED` until the PR is merged, the exact merge SHA is known, Pages has deployed that SHA and cache-busted HTTP/readback confirms the intended routes and text.
