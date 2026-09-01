# DP 748/2026 — Master / CAEPR / professional-lineage correction overlay

Control date: 2026-09-01  
Status: SOURCE-RECONCILED CONTROLLING OVERLAY PENDING MERGE  
Master Proceedings ID: `TF-CRI-003`  
CAEPR proceeding ID: `PD-SP-R-0003`

## Purpose

This record corrects and extends the stale `TF-CRI-003` row without changing its immutable identity. It is the controlling reconciliation for DP 748/2026 until the next full Master Proceedings Register regeneration. It must be read with `assets/data/dp748-2026-canonical-interlink-control-v1.json`, the counsel filing register, procurador master register and counsel/procurador gap register.

## Canonical proceeding identity

- Diligencias Previas: `0000748/2026`.
- NIG: `3802343220260002351`.
- Current court label: **Plaza nº 4 del Tribunal de Instancia (Sección Instrucción) de San Cristóbal de La Laguna** (`PD-SP-I-0037`).
- Historic/predecessor source label retained as an alias: **Juzgado de Instrucción nº 4 de San Cristóbal de La Laguna**.
- Complainant: Gil Marer (`PD-SP-P-0001`).
- Reported/denounced legal entity: Cuatrecasas, Gonçalves Pereira, S.L.P. (`PD-SP-O-0049`). The line-wrapped court header does not create two Cuatrecasas entities.

## Verified professional chain

`Gil Marer → Carlos Llamas Sanz → Adriana Hernández Díaz → DP 748/2026`

- Carlos Llamas Sanz: `PD-SP-P-0146`; counsel for Gil Marer in the source-verified DP 748 period.
- Adriana Hernández Díaz: `PD-SP-P-0067` / `PROC-ADRIANA-HERNANDEZ-DIAZ`; procuradora for Gil Marer in DP 748, paired with Carlos Llamas Sanz on the located primary sources. The 1-Sep-2026 LexNET communication identifies her as procuradora nº 346 of the Tenerife procuradores' college.
- Graciela Pérez-Valencia Díaz: `PD-SP-P-0147`; Magistrate-Judge signing the 16-Jul-2026 order.
- María del Pilar Luis Medina: `PD-SP-P-0148`; LAJ identified on the 1-Sep-2026 LexNET communication.

These are proceeding/period capacities only. They do not transfer to another client, proceeding, merits position or liability question.

## Procedural chronology now controlled

1. **24-Mar-2026** — Auto 454/2026 provisionally dismisses/archives DP 748/2026.
2. **17-Apr-2026 14:29:10** — primary LexNET receipt verifies a filing by Adriana Hernández Díaz for Gil Marer, under the direction of Carlos Llamas Sanz, expressly titled **recurso de reforma y subsidiario de apelación** against Auto 454/2026.
3. **26-Jun-2026 00:22:46** — primary LexNET receipt verifies a synthesis/concreción filing in the same lane.
4. **16-Jul-2026** — the court partially upholds reform as to the acknowledged lack of reasoning in the 24-Mar order, supplies reasoning, maintains the provisional dismissal/archive, expressly records the possibility of reopening with further indicia, and states that the order is not final and can be appealed within five days from the day after the last notification.
5. **1-Sep-2026** — primary LexNET material shows the 16-Jul order was sent on 1 Sep and collected by Adriana Hernández Díaz that day. Source timestamps are preserved as displayed and must not be silently converted for deadline calculation.

## P0 appeal-control point

The repository must **not** state that no appeal exists: the 17-Apr filing expressly included a subsidiary appeal. It also must **not** state that an Audiencia Provincial appeal roll is verified: no admission/transmission/roll source has yet been located in the reviewed set.

`TF-APP-004` therefore remains an **UNVERIFIED appeal/review placeholder** pending primary proof. This is recorded as `CP-GAP-012` and is deadline-critical because the 16-Jul order was only communicated through the located LexNET packet on 1-Sep-2026.

## Direct and contextual interlinks

- `TF-CIV-002` — ETJ 163/2020: **direct underlying enforcement**. Keep civil and criminal procedural identities distinct.
- `TF-CIV-001` — Juicio Cambiario 1048/2019: **predecessor to ETJ enforcement lineage**.
- `TF-FIS-008` — EG 95/2026: **source-verified related Fiscalía coordination/context**, not a merged proceeding.
- `TF-XFR-005`: evidence-transmission/context lane only.
- `TF-APP-004`: unverified appeal/review placeholder; no promotion until a court source identifies admission/transmission/appeal roll.

## Registered evidence-lineage gaps

- `CP-GAP-012` — P0 subsidiary-appeal processing / 1-Sep notification deadline reconciliation.
- `CP-GAP-013` — complete complaint/ampliaciones/property/actor/evidence deficiency matrix.
- `CP-GAP-014` — reconcile the separate 26-Jun source carrying a “recurso de reposición” filename against its actual receipt and court treatment before promotion.
- `CP-GAP-015` — locate and backlink the underlying poder/apud-acta/personación instrument; representation itself is already source-verified.

## Publication boundary

This closeout registers identities, procedural events and relationships. It does **not** turn allegations against Cuatrecasas or any professional/judicial actor into findings of criminality. Raw Gmail addresses, NIF/NIE data, signed download links and private correspondence remain outside the public surface unless independently cleared under publication governance.

## Master-row correction instruction

On the next deterministic regeneration of `archive/PROCEEDINGS_MASTER_REGISTER.csv`, `TF-CRI-003` must inherit from the machine-readable control at `assets/data/dp748-2026-canonical-interlink-control-v1.json`: NIG, current/historic court labels, party/professional linkage, the 17-Apr reform + subsidiary appeal, 16-Jul partial-reform outcome, 1-Sep notification and the P0 unresolved appeal-processing state. Do not mint a replacement Master ID.
