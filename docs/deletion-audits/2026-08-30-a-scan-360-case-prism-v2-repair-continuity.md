# A-SCAN 360 / CASE PRISM V2 REPAIR — CONTINUITY CONTROL

**Date:** 30 August 2026
**State:** `PREPARED_PENDING_MERGE`
**Branch:** `audit/ascan-360-case-prism-20260830`
**Requested control baseline:** `3473d8c399d990b45ad58dd9a2aa8f8caf0d6814`
**Actual base main:** `aac741320cd9541ecaae564db89188cb941dd645`

## Why this corrective control exists

The initial Case Prism delivered through PR #1227 made convergence and fragmentation analysis visible, but the subsequent A-SCAN 360 rerun found that those ideas were still experienced as separate components. The public matrix encoded only 43 of 99 coordinates, “parallel lanes” were event cards rather than stable lanes, isolation operated on aggregate lanes rather than exact files, and only five audience lenses existed.

Governance already required `CONVERGENCE_CLUSTER` and `FRAGMENTATION_AUDIT`. The mismatch was therefore classified as an **implementation gap**, not completion.

## Corrective reader contract

The bilingual proceedings renderer now implements in source:

1. **Decision-dependency matrix** — 18 controlled propositions across 12 legally distinct lanes. All 216 coordinates are explicit and inspectable; no coordinate degrades to an unexplained dash.
2. **Parallel-proceedings swimlane** — stable columns preserve lane identity while showing how one event can be materially relevant across files.
3. **Exact-proceeding isolation test** — one canonical proceeding can be selected; outside material fades, disappearing context is identified, and the full corpus can be restored immediately.
4. **Audience lens** — nine lenses over one evidence base: court/magistrate, Audiencia Provincial, Ministerio Fiscal, CGPJ/supervision, LAJ/judicial office, regulator/public authority, journalist/researcher, owner/affected party and professional/funder.
5. **Trace-to-Prism navigation** — the canonical trace view can open the detailed decision-dependency coordinates that name the selected file.

Changing a lens changes priority questions, ordering, competence explanation and source path only. It never changes facts, relationship status, in-file treatment or evidence status.

## Controlled data model

- Canonical proceeding nodes remain `archive/PROCEEDINGS_MASTER_REGISTER.csv`.
- `scripts/build_proceedings_case_prism_v2.py` deterministically produces the public-safe Case Prism projection from the independent frozen fixture `archive/PROCEEDINGS_CASE_PRISM_V1_SEED_30AUG2026.json`; the generated target is never its own seed.
- `assets/data/proceedings-case-prism-v1.json` remains the asset path for continuity and now declares schema 2.0.0.
- `assets/data/proceedings-interconnectivity-schema-v1.json` now declares schema 1.4.0, including the bilingual evidence-status and independent generation-seed requirements.
- The denominator is 102 canonical rows, 101 public-eligible rows, 18 propositions, 12 lanes, 216 explicit coordinates and nine lenses.
- Relationship status, file-treatment status and evidence status are independent axes.

Every proposition carries a finite test: question, source needed, current source status, competent organ, related proceedings, consequence if confirmed and consequence if refuted. Every active coordinate carries a reason, source path, evidence status, attribution, strongest contrary record and decision dependency.

## Canonical corrections in this package

- `VAL-CIV-001` is physically consolidated without creating a duplicate Master ID; its former overlay is retained as provenance.
- `GC-CRI-009` records the 21 July 2026 provisional dismissal and does not present an unfiled draft challenge as a filed procedural act.
- `GC-APP-004` points to appealed judgment `GC-CAL-002`.
- The `LZ-CIV-040` / `LZ-CIV-041` parent cycle is removed.
- `GC-APP-007` is excluded from exact-proceeding Case Prism lanes. The removal objects remain RPL 3304/2025 and accumulated/linked RPL 3319/2025; RPL 421/2026 remains the remuneration appeal.

These canonical changes become the controlling main/public state only after the package merges and deploys.

## Institutional entry and accessibility

The homepage now offers an early neutral institutional-clean-room route before the allegation-led material. Reciprocal navigation connects the homepage, Proceedings Map, Master Register, clean room, Calificación, AC and Fiscalía dossiers in both languages.

The renderer adds semantic tabs and panels, arrow/Home/End keyboard operation, focus and live-region handling, visible non-colour status labels, responsive sticky columns, reduced-motion handling and a visible degraded state if Case Prism data fails.

## Validation contract

The structural audit must verify:

- the 102/101 canonical/public denominator;
- exact Valencia and DP 1956 corrections;
- an acyclic parent graph;
- 18 × 12 = 216 explicit coordinates and every controlled relationship status;
- independent treatment vocabulary;
- source resolution and public-route existence;
- exact-file isolation, full-corpus restore, stable lanes and nine lenses;
- complete finite-test/actionability fields; and
- the explicit counsel/procurador denominator gap.

The browser smoke must verify EN and ES hash activation, six semantic tabs, keyboard navigation, all 216 interactive matrix cells, 18-by-12 swimlane geometry, lens priority, rich detail and source links, exact-file isolation/fade/restore, trace integration, mobile navigation and absence of console errors.

## Non-regression boundaries

- RPL 3319/2025 is not the fees appeal and the three appellate objects are not presented as joined.
- Same event does not mean same proceeding.
- Different proceeding does not mean factual isolation.
- Context is not joinder, knowledge, coordination, wrongdoing or liability.
- `NOT LOCATED` is not `DID NOT EXIST`.
- Meeting Point / FTI remains contextual pending completion of the actual Sun Park bridge.
- Matkator remains a separate legal person.
- Counsel/procurador lineage remains denominator-incomplete; `CP-GAP-004` and `CP-GAP-005` stay visible.

## Completion boundary

This record currently proves source preparation and local non-browser validation only. It does not prove PR review, CI browser rendering, merge, Pages deployment, live HTTP readback or deletion-safe continuity.

Before closeout, update this file and `publication-manifests/ascan-360-case-prism-v2-repair-20260830.json` with the exact PR, validated head SHA, merge SHA, relevant CI runs, Pages run and independent no-cache live-byte readback. Do not inherit those states from the original map or initial Case Prism releases.
