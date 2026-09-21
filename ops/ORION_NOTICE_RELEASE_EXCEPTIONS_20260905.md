# Orion notice registration — scoped acceptance and CI exceptions

Control: `PD-SP-ORION-NOTICE-20260905`  
Date: 5 September 2026  
Integration PR: #1460  
Base: `145dd4e16773989bef1ddac6ea0428a8cca4a1ff`  
Prepared dependency-reconciled head: `2c222662cd2899e3cd86dc8681afa86591f37e86`

## Scope and accepted source boundary

Twenty individual financial/institutional notice events are added to the existing canonical communications register: 313 preserved rows + 20 = 333. Source/event allocations, 24 source descriptors and six attachment descriptors are listed in `ops/ORION_NOTICE_CANONICAL_CROSSWALK_20260905.json`. The audited public projection spans 22 existing bilingual pages, 119 unique added internal links and four existing public explanatory figures. See `ops/ORION_NOTICE_PUBLICATION_AUDIT_20260905.json` for the exact source hash, page inventory and unresolved gaps.

This is not a historical universal-completeness certificate and not a merits or liability finding. Every new event preserves its source-specific limits. In particular, source-attested dates do not turn an unlocated native submission into a recovered original; future/purported internal circulation is not proved Board delivery; intended destruction is not proved destruction; the CNMV extension is not a refusal; and the exact CajaSiete facility, approximately EUR1m recollection, transactional dates and suspension/Ona linkage remain open.

## Scoped checks performed

Preparation run `33962496007` validated canonical reconstruction, the institutional schema/validator, 13 existing institutional regression tests, Red SARA discovery/projection and scoped source/event/privacy/anchor checks before committing artifacts to the integration branch. Read-only PR validation subsequently succeeded on `eec2bd2f06d4de8f9f09d0fef9cb69bc16672d93` in run `33962911110`.

A newly introduced dependency was found in the specialist Fiscalía projection: adding twenty non-Fiscalía financial notices to the canonical register caused its frozen historical view to count 316 rather than 296 events. This was corrected, not waived. The specialist builder now preserves its established cohort separately from the new source-controlled financial-notice cohort; the corresponding validator checks the exact new records against their input while preserving all historic specialist identity/count checks. The new events remain fully visible in the 333-row canonical register and bilingual notice projections. The derivative's canonical source hash was regenerated before merge.

Dependency preparation run `33962999952` passed the specialist deterministic builder, specialist validator and regression tests, the Orion notice crosswalk/anchor check, and canonical institutional reconstruction/validation, then committed only the two specialist scripts and derivative JSON.

## Broader repository checks are not all green

The read-only base comparison run `33962909151` compared the unchanged base with proposed content without changing publication gates or main. It reproduced these failures on both revisions:

- `scripts/validate_publication_integrity.py`: the pre-existing `publication-manifests/historic-proceedings-authority-reintegration-20260903.json` lacks `current_state`, `expected_routes` and `owner`.
- `scripts/validate_audience_experience.py`: fails on both revisions. This release does not manufacture new culpability language to satisfy an unrelated presentation rule.
- `scripts/validate_repository_preservation.py`: fails on both revisions; no claim of repository-wide preservation-gate success is made.

The same comparison showed the community professional-network validator, publication-integrity v2 validator and Treasury transparency validator passing on both revisions. The purported standalone first-read script name was absent on both revisions; the actual audience/presentation controls remain the source of truth. Other broad PR/live-monitor failures were observed, including Cuatrecasas, the proceedings-map audit, an older 3205/2014 identity-display check and source-of-funds live monitoring. They are not represented as passing or as fully resolved by this scoped release. In the observed base workflow results, the 3205/2014 and audience/publication workflows were already failing.

No unrelated gate, branch protection or ruleset is disabled by this release. A normal PR merge remains subject to GitHub's configured enforcement. The source-controlled additive notice release is not a certification that every existing repository defect has been repaired.

## Deployment is a separate acceptance state

At the creation of this note the PR is not yet merged. Publication requires the merge SHA, the GitHub Pages deployment result and the read-only live verifier. That verifier compares the exact canonical register/crosswalk bytes and all 22 managed page blocks, resolves added reciprocal fragments and checks all four public figure hashes. Only that evidence supports `LIVE_VERIFIED` for this scoped release. The Control Tower closeout will record the resulting SHA/run; this note is not itself a deployment certificate.
