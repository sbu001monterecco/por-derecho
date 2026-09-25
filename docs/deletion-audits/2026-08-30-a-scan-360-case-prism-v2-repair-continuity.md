# A-SCAN 360 / CASE PRISM V2 REPAIR — CONTINUITY CONTROL

**Date:** 30 August 2026
**State:** `DELETION_SAFE_WITH_OPEN_EVIDENCE`
**Branch:** `audit/ascan-360-case-prism-20260830`
**Pull request:** [#1228](https://github.com/sbu001monterecco/por-derecho/pull/1228)
**Initial implementation head/tree:** `0ed308f68b39354f30ae6a9b98eb6bf0eda1c4bf` / `4d440b27f6cb689ee365c22171bd7d85baf5a790`
**Final PR head/tree:** `62154f63c8ccb319a4f11d8c325af0a7d5e3b38e` / `ac36225aeb6b8dd67ffe3f5c6a1296f37d0aae5d`
**Merge commit:** `ad4cd3a4472004602f529db58843caf36073fa8a`
**Case Prism audit:** [run 33330927083](https://github.com/sbu001monterecco/por-derecho/actions/runs/33330927083) — success
**Pages deployment:** [run 33330926551](https://github.com/sbu001monterecco/por-derecho/actions/runs/33330926551) — success
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

These canonical changes are merged and deployed as part of the controlling main/public state at `ad4cd3a4472004602f529db58843caf36073fa8a`.

## Institutional entry and accessibility

The homepage now offers an early neutral institutional-clean-room route before the allegation-led material. Reciprocal navigation connects the homepage, Proceedings Map, Master Register, clean room, Calificación, AC and Fiscalía dossiers in both languages.

The renderer adds semantic tabs and panels, arrow/Home/End keyboard operation, focus and live-region handling, visible non-colour status labels, responsive sticky columns, reduced-motion handling and a visible degraded state if Case Prism data fails.

Because the institutional-page navigation is additive visible `<main>` content, its pre-existing first-hop rendered-provenance snapshots are refreshed to the new exact normalized lengths and hashes; the underlying 130-object identity census and 61/69 status split do not change.

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

## Exact live readback

On 30 August 2026, a no-cache public HTTP readback matched merge `ad4cd3a4472004602f529db58843caf36073fa8a` byte for byte on all 20 declared paths:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `en/index.html` | 226864 | `61d6d3544c1968cf7a4cdccf57c711cf3735dcffd0276cb814e51226a6843174` |
| `en/proceedings-map/index.html` | 15402 | `56ad9dfa11e11990056472ab6aaff8c09d3c727b36a11aefbfb05d5bc1b953ed` |
| `en/master-proceedings-register/index.html` | 7899 | `66534df26d76ae2083fc6bdd6bbbba97f7f4c4dbd08d83c13fe443f7dd5ce3e1` |
| `en/public-authority-unitary-case-reconstruction/index.html` | 27688 | `adeeccfece2b2decc18b038b930c370c192b34c53299e4f76bd8c9e577c9e144` |
| `en/calificacion-rpl-2523-evidence-map/index.html` | 12632 | `eb8f6eb525afa81ae3ee4ed4ed764f6fc5a89fd2c25fa42ad00fbac7849fcf17` |
| `en/insolvency-36-2012-administrator-removal-fees/index.html` | 20912 | `75d09763f0baf99db9277c8bed2cf6632783576706c8a9b9ea71938d778dc31c` |
| `en/fiscalia-dip-2-2026/index.html` | 60211 | `08ce4f7561b23474068e0247d7d6d41ff38edeabfaa025691f1c35e547208b3e` |
| `es/index.html` | 235970 | `6828591d3b1b24d2951d2349bff183cc308b4474f117ff561456011e7aa00dab` |
| `es/mapa-procedimientos/index.html` | 16555 | `9ea6a1cb3a6ff1518733e498c9063d4376e940cdf994351d92e26f895b4eba84` |
| `es/registro-maestro-procedimientos/index.html` | 8522 | `04a8211c793a94233cb7dd5bb97cb6bd7e108f1f72db9dfcc5d95257f1f6f5bc` |
| `es/reconstruccion-unitaria-autoridades-publicas/index.html` | 28607 | `3e4c18094485bbdaefe9644d595856e734f39540b819cd36b1534293f9a16ec3` |
| `es/calificacion-rpl-2523-mapa-prueba/index.html` | 13204 | `940c5f7021a18d0e1644b3bc0acd1795451cc51e5f445826d33e0408c91746b3` |
| `es/concurso-36-2012-separacion-ac-honorarios/index.html` | 21555 | `f0d6571bdce1c7de0111419af6516bc3dadad3eb810720b3728d30490cd38cbc` |
| `es/fiscalia-dip-2-2026/index.html` | 60961 | `ded449bff08bcb2b8e241236b409700f387c204c324ee13266246fbef1126932` |
| `assets/data/proceedings-case-prism-v1.json` | 266588 | `c092f81e69aa1552f1dba0078d8d49a213fc1e0389da08fd33a5df0fcdbaaa41` |
| `assets/data/proceedings-interconnectivity-schema-v1.json` | 6879 | `9a32750198102ece00d1c82fc3a06f4c258e651b0a1117a7e947abbda58eaf31` |
| `assets/proceedings-interconnectivity-map-20260830.js` | 44248 | `b24e7accb141f34a65615bffa4d97d0fc02a905184e4f05041ebe24cc975cad5` |
| `assets/proceedings-interconnectivity-map-20260830.css` | 18568 | `9d18e8ec4692d19a36484c43afced42288d64863736df1763dacae756a7ed552` |
| `archive/PROCEEDINGS_MASTER_REGISTER.csv` | 61440 | `b46301ef2b145698de3d7e24f0be4e69370807f54e6cd8fa09b4cb4b841e0afc` |
| `archive/PROCEEDINGS_CASE_PRISM_V1_SEED_30AUG2026.json` | 28313 | `1de9bcddec0765377daa643670dacec66f6b5284ef4386310a972ef593c3dba8` |

The dedicated post-merge audit and real Chromium smoke succeeded in run 33330927083. Pages run 33330926551 deployed the exact merge SHA before the live readback.

## Completion boundary

The implementation decisions, controlled source, validation evidence, merge, deployment and exact live-readback ledger are repository-controlled. The originating execution context is therefore **deletion-safe with open evidence** and is not required to reconstruct or continue this work.

This closeout does not upgrade any proposition's evidential status. Counsel/procurador lineage remains denominator-incomplete; native/certified Valencia file completeness remains open; and the signed DP 1956 provisional-dismissal order plus current status/finality certification remain primary-source targets. Native evidence, private custody sources and backups remain subject to their own retention controls.
