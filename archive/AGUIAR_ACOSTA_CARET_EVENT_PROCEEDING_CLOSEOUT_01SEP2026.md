# Fernando and Laura Aguiar Acosta — `^`, event, date and proceeding-context closeout

**Control date:** 1 September 2026  
**Control:** `PD-AGUIAR-CARET-EVT-PROC-20260901-01`

## Canonical identities

- `PD-SP-P-0088` — **Fernando Aguiar Acosta^** — `CARET_CONFIRMED`.
- `PD-SP-P-0095` — **Laura Aguiar Acosta^** — `CARET_CONFIRMED`.

No new person IDs were minted. The release preserves the existing canonical identities and adds a dedicated dated event / proceeding-context layer.

## Dated event registration

### Fernando Aguiar Acosta^

1. `PD-SP-EVT-FAG-2023-GRUPO-ACOSTA-MATOS` — 2023 public-profile corporate-law internship under the label `Grupo Acosta Matos`; exact employing legal person unresolved.
2. `PD-SP-EVT-FAG-202406-07-RICPE` — June–July 2024 RIC Private Equity placement.
3. `PD-SP-EVT-FAG-202506-08-BELAGUA-ACHM` — June–August 2025 legal-advisory placement with Belagua 2013 / ACHM Hotels by Marriott.
4. `PD-SP-EVT-FAG-2026-COLLIERS-DEBT-ADVISORY` — summer 2026 Colliers Debt Advisory placement; independently corroborated on 29 July 2026 by a financial-media report naming Fernando on an unrelated EUR 43.5m hotel-financing advisory team.

### Laura Aguiar Acosta^

1. `PD-SP-EVT-LAA-20230201-0531-MAEC-PLACEMENT` — 1 February–31 May 2023 Spanish Foreign Ministry training-placement resolution identifying Laura Aguiar Acosta / IE University.
2. `PD-SP-EVT-LAA-202407-08-CANARIAN-HOSPITALITY` — July–August 2024 Canarian Hospitality hotel-management internship in Lanzarote; the public résumé identifies MYND Yaiza and Radisson Blu Lanzarote controllers, internal-expense-control work and collaboration with the legal department on hotel purchase/management processes.

## Proceeding-context registration

For each person, the control records the following as **contextual only**:

- `GC-JUD-001` — Concurso ordinario 36/2012;
- `NAT-CNMV-001` — CNMV 2024136159; and
- `NAT-CNMV-002` — CNMV 2024174266.

Every row is explicitly marked `NO_DIRECT_PROCEDURAL_ACT_LOCATED`. The context explains why the proceeding/file may matter to records-custody or chronology questions; it does **not** assert that Fernando or Laura filed, received, decided, participated in, knew of, or were parties to the proceeding/file.

## Relationship boundary

The alleged Fernando ↔ Laura sibling relationship and the wider Acosta Matos family relationship remain attributed leads and independently unverified. Matching surnames, professional placements and perimeter overlap do not establish kinship or shared knowledge.

## Machine authority

- `assets/data/aguiar-acosta-person-event-proceeding-control-v1.json`
- `assets/data/caepr-caret-irea-ricpe-colliers-continuity-v1.json`
- `scripts/validate_aguiar_acosta_caret_event_proceeding.py`

The dedicated validator fails if the canonical person IDs lose `CARET_CONFIRMED`, if any of the six event IDs disappears, if the three proceeding contexts drift from the Master register, or if a contextual proceeding link is promoted into a direct procedural act without source proof.
