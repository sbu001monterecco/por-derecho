# CALIFICACIÓN CANONICAL MATRIX — IMPLEMENTATION STATE

Date: 17 August 2026  
Initial scan baseline: `main` at `2abc0ab85c8408850e8974d535013445a6c7928b`  
Current synchronized base: `main` at `909ddfc164e5c3865f3348cf920548fdf751638b`  
Working branch: `agent/calificacion-canonical-matrix-17aug2026`  
Draft pull request: **#267**  
Status: **implemented and validated on the protected branch; not live until reviewed, merged and deployed**

## Purpose

Add a single bilingual, person-specific and branch-specific summary near the top of the calificación pages so that a reader does not have to reconstruct the difference between:

- the AC’s complete allegation package;
- the Fiscal’s five-heading two-page opinion;
- the first-instance judgment’s accepted, rejected and narrowed grounds;
- the separate consequences for LPB, Gil and PINK; and
- the current appeal status.

## Files created

1. `archive/CALIFICACION_CANONICAL_AC_FISCAL_JUDGMENT_PERSON_MATRIX_17AUG2026.md`
   - complete RT-00–RT-14 crosswalk;
   - person-specific outcomes;
   - appeal issues/status;
   - contradiction, truth-inversion, truth-diversion and beneficiary controls;
   - adverse evidence and gaps.

2. `assets/calificacion-canonical-allegations-outcomes-20260817.js`
   - route-limited bilingual public module;
   - procedural-status banner;
   - full AC/Fiscal/judgment summary;
   - accepted/rejected/narrowed table;
   - person-specific consequences and appellate boundary;
   - scoped CSS and no external dependencies.

3. `archive/CORRECTION_REGISTER_CALIFICACION_CANONICAL_ADDENDUM_17AUG2026.md`
   - ten mandatory wording controls.

4. `archive/MISSING_EVIDENCE_REGISTER_CALIFICACION_STATUS_ADDENDUM_17AUG2026.md`
   - twelve source-completion gates and retrieval priorities.

5. `archive/CALIFICACION_CANONICAL_MATRIX_IMPLEMENTATION_STATE_17AUG2026.md`
   - this implementation and validation record.

## File amended

- `assets/site.js`
  - loads `calificacion-canonical-allegations-outcomes-20260817.js?v=20260817a` after the existing calificación source-status correction layer.

## Source set actually checked

- complete 47-page AC report;
- complete 2-page Fiscal opinion;
- Gil opposition;
- Sentencia 163/2023;
- Gil and PINK appeal files;
- AP deliberation/fallo providencia;
- finite Gmail/Drive status searches;
- 30-Jan-2018 cooperation email;
- 22–23-Jan-2018 access, preservation and exit correspondence;
- repository controlling ledgers, P17, P18 and P19;
- live GitHub Pages status and current main deployment.

## Mandatory non-overstatement controls implemented

- Gil was not allocated late filing.
- PINK was accomplice only in the rent branch.
- `connivencia` is branch-specific.
- the Fiscal’s role contradiction is reported as a facial drafting defect, not proof of intent.
- no AP judgment was **located**; the module does not assert none exists.
- accounting material supplied is separated from official-book sufficiency.
- signing the lease is separated from later non-collection.
- calificación is separated from criminal conviction.

## Validation completed

- [x] `node --check assets/calificacion-canonical-allegations-outcomes-20260817.js`
- [x] `node --check assets/site.js`
- [x] ES route insertion test
- [x] EN route insertion test
- [x] non-Calificación route guard test
- [x] required person-specific corrections, dates and figures present in both languages
- [x] privacy scan: no private addresses, identity numbers, phone numbers, private email addresses or bank details in the new module/registers
- [x] branch synchronized with current `main`
- [x] branch compare reviewed: five substantive changed files before this implementation record
- [x] draft PR #267 opened to `main`

## Deployment boundary

GitHub Pages deploys from `main` at repository root. The live site was successfully built from the current main lineage before this branch was opened. This package is intentionally **not live** while PR #267 remains draft. After merge, verify the Pages workflow and both direct URLs before recording deployment.

## Direct routes for post-merge verification

- Spanish: `/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas/`
- English: `/por-derecho/en/insolvency-classification-parallel-lives/`

## Continuity rule

If an appellate judgment or terminating resolution is obtained, do not merely edit the status banner. Ingest the full primary source, rebuild every RT row, update the correction and missing-evidence registers, revise both languages, and run a new branch → PR → deployment verification cycle.
