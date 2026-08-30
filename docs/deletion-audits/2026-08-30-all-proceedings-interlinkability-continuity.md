# All-proceedings interlinkability continuity — 30 August 2026

## Current lifecycle state

`PR_OPEN` in pull request **#1235** on branch
`codex/all-proceedings-interlinkability-20260830`, based on
`5939ed3badad20193a4aba05ca62047d6bc6ff89`.

This record identifies the controlled branch, source base and open pull request; the reviewed remote head/tree is pinned independently in the PR before merge. It does **not** certify green CI, merge, deployment, live HTTP
readback or deletion-safe closeout. The controlling lifecycle record is
`publication-manifests/all-proceedings-interlinkability-20260830.json`.

## What is controlled in the repository

- The browser-facing Master Register is generated as an allowlisted derivative
  in `assets/data/proceedings-master-public-v1.json`; browser code no longer
  downloads and filters the operational CSV.
- All 106 public records have stable trace destinations. All 85 public exact
  proceedings have stable isolation destinations and reciprocal Master Register
  row anchors.
- The 85 exact public proceedings have one deterministic disposition each:
  direct procedural edge, controlled contextual bridge, explicit relationship
  gap or independent track.
- Direct edges are limited to 17 exact proceeding pairs supported by 21
  preserved canonical field assertions. Sixteen pairs / 20 assertions carry a
  verified source status; one pair / one assertion remains
  `CORPUS_REPORTED_PRIMARY_PENDING`. A pair may retain more than one source
  assertion.
- Material context is limited to seven exact `Connection` groups, one specialist
  source-controlled corridor and 18 Case Prism proposition groups. Stream, geography and chronology remain browse
  taxonomy and cannot create material reconnection by themselves.
- The isolation algorithm is bounded. It does not traverse every proposition of
  every proposition co-member. It admits the selected proceeding's own
  non-`DIRECT` coordinates, its own controlled proposition clusters and one-hop
  direct/recorded-connection neighbours only where the neighbour coordinate is
  `DIRECT`.
- `GC-APP-007` / `PD-SP-R-0013` is retained as an immutable aggregate
  removal-appeal family reference, not a third exact appeal. The exact rolls
  remain `GC-APP-005` / RPL 3304/2025 and `GC-APP-006` / RPL 3319/2025.
- `NAT-TES-001` has one documented direct routing lineage, to `X-WB-005` through
  the same REGAGE filing. The separate `LZ-TRA-028` transparency challenge is a
  specialist source-controlled contextual corridor; `NAT-AID-001` remains
  programme-specific public-money context through Case Prism P18. Neither
  contextual route is promoted into a direct procedural edge.
- Every public exact proceeding has a specific English and Spanish finite-source
  request. These questions do not upgrade source status or imply joinder,
  receipt, admissibility, knowledge, wrongdoing or liability.

## Finite denominators

| Control | Current result |
|---|---:|
| Canonical records | 107 |
| Public traceable records | 106 |
| Canonical exact proceedings | 86 |
| Public exact proceedings | 85 |
| Exact private-source row excluded from public derivatives | 1 |
| Public exact dispositions | 85 / 85 |
| Direct pairs / source assertions | 17 / 21 |
| Source-verified direct pairs / pending direct pairs | 16 / 1 |
| Controlled material context clusters | 26 |
| Exact proceedings with Case Prism coordinates | 26 / 85 |
| Exact proceedings without Case Prism coordinates | 59 / 85 |
| Specific bilingual next-source requests | 85 / 85 |

Structural interlinkability is therefore complete for the present exact public
denominator. Decision-dependency and fragmentation **content** coverage is not:
it remains `GAP_26_OF_85`. The 85 specific bilingual next-source requests are
not full finite actionability tests: exact-proceeding dispositions still lack a
complete question / competent organ / related proceedings / confirmed and
refuted consequence object, so that separate coverage is `GAP_0_OF_85`.

Case Prism sources remain proposition-level. They do not prove the status,
treatment, receipt, acknowledgement or reliance represented in an individual
cell/file, so cell-treatment source coverage remains a gap. The current public
model also has no actor-specific knowledge/receipt field. `WHO KNEW` must remain
open until actor- and file-specific evidence is registered; attribution labels
must not be used as a substitute.

The `85/85` navigation claim is limited to exact ID ↔ Master Register row ↔
renderer trace/isolation state. The repository has no established denominator
for exact ID ↔ proceeding-specific dossier/source page. Known dossier links are
additive; missing links cannot be interpreted as absence of evidence or a fully
closed source path.

## Publication and privacy boundary

The allowlisted derivative is a runtime minimisation control. It does not make a
tracked source private. The repository and its Pages configuration must be
examined separately before anyone states that
`archive/PROCEEDINGS_MASTER_REGISTER.csv` is unavailable from the public
repository or deployed artifact. Current-tree unpublishing is **not verified**.
No source should be removed, rewritten or relocated without approved private
custody, provenance preservation and a reviewed publication-boundary migration.

## Reproduce the local checks

Run from the repository root:

```bash
python3 scripts/build_public_proceedings_projection.py --check
python3 scripts/build_proceedings_case_prism_v2.py --check
python3 scripts/build_proceedings_interlinkability_v1.py --check
python3 scripts/audit_master_proceedings_publication.py
python3 scripts/audit_proceedings_interconnectivity_map.py
python3 scripts/audit_counsel_procurador_governance.py
python3 scripts/validate_operational_identity_registry.py
python3 scripts/validate_repository_preservation.py
python3 scripts/validate_publication_integrity.py
python3 scripts/validate_audience_experience.py
python3 scripts/validate_private_source_statement_osint_governance.py --base 5939ed3badad20193a4aba05ca62047d6bc6ff89
python3 scripts/validate_alberto_meeting_point_first_hop_caret.py
python3 scripts/validate_concurso36_complete_record_v2.py
python3 scripts/validate_concurso36_primary_autos_redigest_v2.py
python3 scripts/validate_concurso36_decision_continuity.py
node --check assets/master-proceedings-publication-20260830.js
node --check assets/proceedings-interconnectivity-map-20260830.js
node --check assets/site.js
node --check scripts/smoke_proceedings_case_prism.mjs
git diff --check
```

The Playwright smoke is intentionally broader than the static audit: it covers
all 85 exact proceedings in both languages, all 106 trace routes, the 85/21
exact/non-exact Master Register split, stable cold-load fragments, source
assertion multiplicity and the bounded disappearing-proposition sets. It was not
run in this container because the local Playwright dependency was not installed;
browser availability was therefore not reached. The workflow installs Playwright
and Chromium and must run the smoke before merge.

The PR integration pass also refreshed the two controlled institutional-route
snapshots and replaced obsolete v1 date assertions in the decision-continuity
workflow with the existing v2 primary reinspection controls. The push-only
AM357 live verifier now asserts the current 31/31 specialist, 61/130 first-hop,
21/24 unitary and 230-ID registry denominators while preserving its immutable
204-ID historical deployment snapshot. The Playa Blanca PR readback now checks
the current `site-pre-treasury-154-hq-20260828.js` predecessor entry rather than
waiting for an obsolete direct `site-pre-intervencion` marker in `site.js`.

## Steps required before a deletion-safe closeout

1. Review the complete branch diff, with particular attention to evidentiary
   status, private-source exclusion and the aggregate appeal-family correction.
2. Open a pull request and run every required workflow, including the expanded
   Playwright smoke.
3. Do not merge if any generated-asset check, exact-denominator check,
   preservation gate, publication-integrity gate or browser assertion fails.
4. Merge only the reviewed tree, then record the PR, merge SHA and successful
   workflow run IDs in the publication manifest.
5. Verify the deployed artifact and perform no-cache live HTTP readback of both
   map routes, both Master Register routes, both new JSON assets and representative
   exact trace/isolation fragments.
6. Resolve or formally accept the operational-CSV publication-boundary gap. A
   clean renderer readback does not close that separate question.
7. Preserve the `26/85` decision-dependency content gap until additional
   proposition coordinates are source-supported and reviewed.
8. Only after those steps may the lifecycle state advance beyond `PR_OPEN` or
   deletion-safe continuity be claimed.
