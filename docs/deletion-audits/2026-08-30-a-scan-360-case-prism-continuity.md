# A-SCAN 360 / CASE PRISM — CONTINUITY AND DELETION-SAFE HANDOFF

**Date:** 30 August 2026  
**Branch:** `ascan-360-case-prism-20260830`  
**Base main:** `3473d8c399d990b45ad58dd9a2aa8f8caf0d6814`

## Scope

This handoff preserves the A-SCAN 360 rerun and the implementation of the missing convergence/fragmentation reader layer for the Proceedings Interconnectivity Map.

## Material finding

Before this pass, repository governance/schema required `CONVERGENCE_CLUSTER` and `FRAGMENTATION_AUDIT`, but the public proceedings renderer mainly exposed track map, chronology and single-proceeding trace.

That was classified as an **implementation gap** rather than treated as complete merely because the requirement existed in governance.

## Implemented public views

The bilingual proceedings renderer now adds:

1. **Case Prism / Prisma del caso** — a decision-dependency matrix: one controlled proposition across legally distinct lanes.
2. **Parallel lanes / Vías paralelas** — approximate chronological view of the same controlled propositions across lanes.
3. **Isolation test / Prueba de aislamiento** — separates what is direct inside one selected lane from expressly curated material context outside it.
4. **Reader lens / Lente del lector** — reprioritises questions for court/magistrate, Ministerio Fiscal, CGPJ/judicial supervision, regulator/public authority and journalist/researcher without changing facts or source status.

## Data and governance

- Canonical proceeding nodes remain `archive/PROCEEDINGS_MASTER_REGISTER.csv`.
- New derived public-safe relationship/proposition source: `assets/data/proceedings-case-prism-v1.json`.
- Existing schema is upgraded to 1.2.0 and maps the new renderer views explicitly.
- New additive governance: `.github/governance/A_SCAN_360_CASE_PRISM_AND_READER_LENS_PROTOCOL_30AUG2026.md`.
- Existing anti-fragmentation, institutional-reader, publication, privacy and canonical-identity controls remain in force.

## Controlled Case Prism status vocabulary

- `DIRECT`
- `CONTEXT`
- `OPEN`
- `NOT_LOCATED`
- `OUTSIDE`

No Case Prism cell may imply a stronger proposition than its source status.

## Priority lanes preserved

- Concurso 36/2012
- RPL 2523/2025 calificación
- RPL 3304/2025 + accumulated/linked RPL 3319/2025 AC removal
- RPL 421/2026 AC remuneration
- Arrecife control/mortgage/title
- Valencia / CaixaBank `VAL-CIV-001`
- Meeting Point / FTI contextual restructuring
- Tenerife / Matkator / Cuatrecasas
- Ministerio Fiscal
- CGPJ / LAJ supervision
- historical possession/exploitation

## Critical non-regression rules

- RPL 3319/2025 is not the fees appeal.
- Valencia remains one canonical identity: `VAL-CIV-001`; do not create a duplicate Valencia case.
- Meeting Point / FTI remains contextual pending source completion of the actual Sun Park transaction/operator bridge.
- Matkator remains a separate legal person.
- The isolation test is methodological and does not prove notice, admissibility, institutional knowledge, wrongdoing or duty.
- Context is not joinder.
- `NOT LOCATED` is not `DID NOT EXIST`.

## Files changed/added in this pass

- `assets/data/proceedings-case-prism-v1.json`
- `assets/proceedings-interconnectivity-map-20260830.js`
- `assets/proceedings-interconnectivity-map-20260830.css`
- `assets/data/proceedings-interconnectivity-schema-v1.json`
- `en/proceedings-map/index.html`
- `es/mapa-procedimientos/index.html`
- `.github/governance/A_SCAN_360_CASE_PRISM_AND_READER_LENS_PROTOCOL_30AUG2026.md`
- `scripts/audit_proceedings_interconnectivity_map.py`
- this continuity handoff

## Completion boundary

This file records source implementation only. Do not call the new visual layer merged, deployed, live or deletion-safe until the PR, CI, merge, Pages deployment and appropriate post-deployment verification states have been separately established.
