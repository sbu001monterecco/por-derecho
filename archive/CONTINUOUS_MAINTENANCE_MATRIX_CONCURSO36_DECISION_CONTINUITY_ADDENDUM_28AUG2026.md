# Continuous-maintenance matrix addendum — Concurso 36/2012 decisions

- **Control:** `PD-C36-DECISION-CONTINUITY-20260828-01`
- **State:** `PREPARED_PENDING_MERGE`
- **Cut-off:** 28 August 2026

| Control surface | Canonical location | Trigger | Required maintenance |
|---|---|---|---|
| Structured chronology | `assets/data/concurso36-decision-continuity-2014-2026-v1.json` | New primary act, certified docket entry or corrected identity/date | Add or amend one family row; preserve stable IDs, chronology and evidential ceiling |
| Human review matrix | `assets/data/concurso36-decision-continuity-2014-2026-v1.xlsx` | Structured chronology changes | Regenerate all worksheets with `scripts/build_concurso36_decision_continuity_workbook.mjs`; recheck formulas, links, filters, widths and freeze panes |
| DOCX/PDF assessment | `assets/data/concurso36-decision-continuity-assessment-2014-2026.docx` and `.pdf` | Counts, key correction, AC-report control or production request changes | Rebuild from canonical JSON, scrub metadata, render every page and verify parity |
| ES public route | `es/concurso-36-2012-autos-resoluciones/#continuidad-2014-2026` | Structured chronology changes | Regenerate from the builder and preserve all specialist content below the audit |
| EN public route | `en/insolvency-36-2012-orders-decisions/#continuity-2014-2026` | Structured chronology changes | Regenerate with record-ID parity and bilingual status/gap text |
| Audit narrative | `archive/CONCURSO36_DECISION_CONTINUITY_AUDIT_2014_2026_28AUG2026.md` | Count, classification or open-family change | Record the correction and explain the changed denominator |
| AC-report continuity | `ac_report_continuity` in the structured chronology | New report text, court receipt, annex, later report or final accounts | Update the partial-series count; do not equate receipt with report text or report statement with independent accounting proof |
| Missing-evidence register | This addendum | A requested family is produced or disproved by certification | Close only the produced node; retain unresolved neighbouring nodes |
| Correction register | Companion correction addendum | Source-controlled date, identity, proceeding or legal-effect correction | Append the superseding rule; do not rewrite historical evidence silently |
| Validation gate | `scripts/validate_concurso36_decision_continuity.py` | Schema, route or counting-rule change | Update fixtures and maintain privacy/completeness-claim controls |

Maintenance rules:

1. Same-date decisions remain separate.
2. Separate proceedings remain separate from Concurso 36/2012.
3. A decision copy does not prove service, appeal outcome, finality or implementation.
4. “Not located” never becomes “nonexistent” without an official denominator.
5. Private provider locators, exact private filenames and unredacted sources stay outside public Git.
6. Repository publication, external communication and filing authority remain separate decisions.
7. The 2014–2016 discovery rows and year-only complaints row are declared aggregation exceptions until authenticated acts can be split.
