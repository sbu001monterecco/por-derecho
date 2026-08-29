# Other-thread reconciliation queue — 29 August 2026

- **Control:** `PD-C36-LINKED-CONTINUITY-20260829-01`
- **Function:** current-main triage and controlled transplant queue
- **Default:** `DO NOT WHOLESALE-MERGE A LEGACY BRANCH`
- **External action:** not authorised

## Status vocabulary

- `ACTIVE_CANONICAL_BASELINE`: use the merged current-main lineage.
- `MERGED_BASELINE__...`: preserve the merged work; add only source-controlled deltas.
- `LEGACY_OPEN_PR__COMPARE_MAIN__TRANSPLANT_ONLY`: screen against current main and move only the verified delta to a fresh branch.
- `LEGACY_DRAFT_PR__LEGAL_PRIVACY_GATE`: do not publish until the stated review gate is satisfied.
- `GOVERNANCE_GATE`: a prerequisite that controls all publication lanes.
- `REVIEW_REQUIRED`: no assumption of uniqueness, completeness or mergeability.

## Ranked queue

| Priority | Lane | Current treatment | Next controlled step |
|---|---|---|---|
| P0 | **C36-DECISIONS-AC-REPORTS** — Concurso 36/2012 decisions, LAJ acts, service/appeal/finality chains and Insolvency Administration reports. | `ACTIVE_CANONICAL_BASELINE`; PR #1141, PR #1142 | Recover and promote only primary binaries and complete procedural/accounting families against the open P0/P1 gates. |
| P0 | **FISCALIA-EG745** — E.G. 745/2026 and the 26 August 2026 Fiscalía General del Estado / Inspección Fiscal notification and Decreto. | `MERGED_BASELINE__FOLLOW_UP_IN_SEPARATE_DOSSIER`; PR #1184, PR #1185, PR #1186, PR #1187, PR #1188 | Preserve the exact filing, receipt, notification, response, review and appeal identities; do not collapse Fiscalía capacities, periods or proceedings. |
| P1 | **ACTA-MEETINGS** — Controlled ACTA and meeting lineage. | `MERGED_BASELINE__CONTINUOUS_MAINTENANCE`; PR #1182, PR #1183 | Add only newly located authenticated source families; preserve the current 23-event / 46-bilingual-page baseline. |
| P1 | **AEAT-PINK** — AEAT / Pink Canary Services evidence and the distinct operator/contract/appearance questions. | `MERGED_BASELINE__NEW_INTAKE_REQUIRES_RECONCILIATION`; PR #1167, PR #1171 | Reconcile any later email, draft or Diligencia against the primary-source register; keep private legal advice and personal contact data outside the public release. |
| P2 | **CARETAKER-IDENTITIES** — Former seven-identity gap closure. | `MERGED_BASELINE__NO_REOPEN_WITHOUT_NEW_PRIMARY`; PR #1165, PR #1169 | Use the resolved institutional identities; do not reintroduce aliases or weaker derivative identifications. |
| P1 | **FTI-MEETING-POINT-COMPARATOR** — FTI / Meeting Point / Mercantil nº3 comparator and preservation questions. | `LEGACY_OPEN_PR__COMPARE_MAIN__TRANSPLANT_ONLY`; PR #1090 | Verify every primary reference and compare current main; transplant only non-duplicative, bounded material onto a fresh branch. |
| P1 | **NON-LPB-MATKATOR-NETWORK** — Non-LPB / Matkator owner-court-party network. | `LEGACY_OPEN_PR__COMPARE_MAIN__TRANSPLANT_ONLY`; PR #1041 | Preserve capacities and ownership boundaries; transplant only source-controlled deltas. |
| P1 | **FINCA-262-EXPLORER** — 262-finca ownership and deed journey explorer. | `LEGACY_OPEN_PR__PRIMARY_DENOMINATOR_REQUIRED`; PR #771 | Do not present the inventory as complete until the title/registry denominator and source status for every row are controlled. |
| P0 | **PP1041-WITHDRAWAL-AUTHORITY** — PP1041 withdrawal attribution, authority, instruction and procedural chain. | `LEGACY_OPEN_PR__MATERIAL_CORRECTION__LEGAL_REVIEW_AND_TRANSPLANT`; PR #576 | Preserve the correction that a withdrawal was filed in LPB's name rather than asserting that LPB itself decided to withdraw; recover the pleading, signer/filer, LexNET, authority, hearing and court-authorisation chain before stronger conclusions. |
| P1 | **MONTELANZA-2008** — Montelanza 2008 Mercantile Registry digitisation and bounded governance-origin baseline. | `LEGACY_DRAFT_PR__SOURCE_AND_PRIVACY_REVIEW__TRANSPLANT_ONLY`; PR #685 | Retain the source-over-OCR rule and the explicit non-findings; compare current main and transplant only reviewed public-safe material. |
| P1 | **CONTROLS-21-22-24** — Redacted full texts and filing-version controls for Controls 21, 22 and 24. | `LEGACY_DRAFT_PR__LEGAL_PRIVACY_GATE`; PR #701 | Do not publish until page ranges, filed-version choices, redactions and public-interest basis receive the required legal/privacy review. |
| P2 | **DAVID-ESPEJO** — David Espejo traceability and evidence-access chain. | `CURRENT_ROUTE_PRESENT__LEGACY_PR_OVERLAP_REVIEW`; legacy PR #450 | Treat the current bilingual route as the starting point; compare the old PR only for a genuinely missing source-controlled delta. |
| P1 | **LENDER-MORTGAGE-NPL** — Mortgage, lender-of-record, assignment, split-credit and NPL allegations. | `MERGED_BASELINE__OPEN_EVIDENCE`; mortgage and split-credit/NPL publication lineages | Keep allegations attributed; close only with native assignment, ledger, notarial, standing, accounting and procedural evidence. |
| P0 | **TRANSPARENCY-ACTOR-MATRIX** — Historical actor census, publication status and public/private naming controls. | `GOVERNANCE_GATE`; controlled publication matrix | No new public identity or role expansion without the reviewed matrix; keep private counsel identities/advice and unrelated matters outside the public corpus. |

## Immediate order

1. **Certified docket and AC-report denominator.** This is the cross-cutting P0 control. Recovering isolated favourable or adverse documents must not be confused with obtaining the denominator.
2. **PP1041 correction review.** Preserve the narrower primary-source formulation; recover authority, pleading, signer/filer, LexNET and Article 51.2/court-authorisation nodes before stronger conclusions.
3. **Current appeals and final stage.** Control merits, service and finality in RPL 2523/2025, combined RPL 3304/2025 + 3319/2025 and RPL 421/2026, then final accounts/conclusion.
4. **Meeting Point/FTI, non-LPB/Matkator and 262-finca lanes.** Compare current main, keep legal-person/capacity/title boundaries, and transplant only authenticated non-duplicative material.
5. **Montelanza and Controls 21/22/24.** Preserve source-over-OCR, explicit non-findings, filed-version decisions, redactions and the legal/privacy gate.
6. **AEAT/Pink and Fiscalía/E.G. 745 follow-up.** Reconcile new communications and filings in their own procedural families. Do not publish private counsel drafts or collapse institutional capacities.
7. **Remaining legacy PRs.** Default to `REVIEW_REQUIRED`, including limitation/prescription, Laborý/CATRUDE, private communications, source-handling, outreach, older FTI, CEXP, Matkator and evidential-traceability branches.

## Old-branch decision record

For each screened PR, record:

- PR number, title, base SHA, head SHA and state;
- whether its source files are already on current `main`;
- whether current main already contains an equivalent or stronger controlled statement;
- source class for each proposed delta;
- public/privacy/privilege status;
- exact files to transplant;
- current validators;
- decision: `TRANSPLANT`, `SUPERSEDED`, `DUPLICATE`, `RETAIN_PRIVATE`, `NEEDS_PRIMARY`, or `NEEDS_LEGAL_PRIVACY_REVIEW`.

An open PR is not evidence. A closed PR is not proof that its underlying factual proposition was accepted. A merged PR controls only the repository state it actually introduced.

## Public-identity control

No new person or role is added merely because it appears in a workbook, an old branch, a social profile, an email draft or an allegation. Use the reviewed actor matrix, preserve legal-person and capacity distinctions, and keep private counsel identities/advice outside the public package.

## Completion test

This queue is complete only when each listed legacy lane has a dated decision record and every transplanted delta has:

`source → canonical record → public-safe derivative → bilingual route → manifest → validation → merged SHA → deployment run → live readback`
