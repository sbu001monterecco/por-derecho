# All-proceedings interlinkability continuity — 30 August 2026

## Current lifecycle state

`LIVE_VERIFIED_WITH_ACCEPTED_PUBLICATION_BOUNDARY_GAP` for pull request
**#1235**.

- reviewed head: `40ccc3c699bcc1147a9ac65a52e93fec240633ce`;
- reviewed tree: `c64ae7547fed024ad0e82397f09fc5f61e2f5da7`;
- normal merge: `e13652bb8b3f51dd050c431a58e2bd70b83f5676`;
- merge tree: `c64ae7547fed024ad0e82397f09fc5f61e2f5da7` — exact reviewed-tree equality;
- exact-head CI: 49 success, one intended conditional skip, zero adverse;
- corrected Chromium/browser workflow: run `33342564713`, success;
- GitHub Pages: run `33342771113` / #1314, completed successfully on the
  exact merge; and
- independent readback: 16/16 intended critical public resources matched the
  merge tree, plus one separately recorded operational-CSV boundary
  observation.

This is not `DELETION_SAFE`. The user expressly accepted the pre-existing
direct HTTP exposure of the tracked operational CSV as an unresolved
publication-boundary gap for this release. The controlling lifecycle record is
`publication-manifests/all-proceedings-interlinkability-20260830.json`.

After #1235, PRs #1243 and #1249 advanced `main` through
`43c4046a8f76fd50e26ce0db58cac6bd62ac4e7f`; Pages run `33343638194` / #1316
succeeded. Those forward deployments add the exact Rollo 1010/2018 identity
story and preserve canonical-lineage links while adding separate Order 804/2018
decision-detail links. They do not remove the interlink registry, Case Prism or
proceedings-map renderer. The current live Master projection preserves all 106
records and differs from #1235 only in the canonical-source digest following a
semantically identical CSV reserialization.

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
  direct/recorded-connection/source-controlled-corridor neighbours only where
  the neighbour coordinate is `DIRECT`.
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
tracked source private. Cache-busted readback found
`archive/PROCEEDINGS_MASTER_REGISTER.csv` directly HTTP-accessible: SHA-256
`267b37574a8cfb96af258d0dfdbd694d506a9c03572b42f3fb1c10376516d294`
on the #1235 release tree and
`74334fd2f3b4ba6a12361b87e61b31859c9693b75b2b8dbcea4a3606c94ba457`
on the current forward main. This exposure is **unresolved and expressly
accepted for this release**. It is recorded separately from intended live URLs
so continuing exposure is not made a validation invariant.

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

The browser smoke is intentionally broader than the static audit: it covers
all 85 exact proceedings in both languages, all 106 trace routes, the 85/21
exact/non-exact Master Register split, stable cold-load fragments, source
assertion multiplicity and the bounded disappearing-proposition sets. It was not
run by the local static command set, but the corrected CI Chromium workflow
`33342564713` completed successfully before merge. Independent post-deployment
browser interaction then exercised English and Spanish Case Prism, isolation,
Treasury direct/context separation, reciprocal Master links and both
institutional clean-room routes. No page-origin console errors were observed;
browser-extension metadata noise was excluded from that result.

The PR integration pass also refreshed the two controlled institutional-route
snapshots and replaced obsolete v1 date assertions in the decision-continuity
workflow with the existing v2 primary reinspection controls. The push-only
AM357 live verifier now asserts the current 31/31 specialist, 61/130 first-hop,
21/24 unitary and 230-ID registry denominators while preserving its immutable
204-ID historical deployment snapshot. The Playa Blanca PR readback now checks
the current `site-pre-treasury-154-hq-20260828.js` predecessor entry rather than
waiting for an obsolete direct `site-pre-intervencion` marker in `site.js`.

## Remaining conditions before deletion safety

The PR, CI, exact-tree merge, Pages deployment and bounded live readback gates
are complete. Deletion safety remains unavailable until the operational-CSV
publication boundary is resolved through approved private custody, provenance
preservation and a reviewed migration, followed by a negative live readback.
The user's acceptance authorises this release despite that gap; it does not turn
the gap into intended publication or close it.

The `26/85` decision-dependency content gap, `59/85` uncovered exact files,
proposition-level source limitation, actor-specific knowledge/receipt gap,
exact-ID dossier denominator gap and `0/85` disposition-level finite-test gap
also remain explicit. They do not negate structural interlinkability, and none
may be silently upgraded by visual prominence or repetition.
