# Cuatrecasas GitHub billing / WIP recovery — 13 September 2026

Status: **READ-ONLY SOURCE RECOVERY / CURRENT GITLAB SUBSUMPTION**

Legacy source repository: `sbu001monterecco/por-derecho`

Controlled source commit reviewed: `2adda2e901ca7c39e91ed2510146d964acb17355`

## Purpose

This note records which useful Cuatrecasas billing/WIP controls were recovered from the older GitHub corpus and how they were migrated into the current GitLab architecture. It is not a second billing ledger and does not override the current public registers.

## Material recovered and subsumed

- `archive/CUATRECASAS_INVOICE_FINANCE_OUTCOME_AUDIT_24AUG2026.md`
- `assets/data/cuatrecasas-invoice-audit-v1.json`
- `archive/CUATRECASAS_2014_ONWARD_BILLING_PACKAGE_RECONSTRUCTION_PROMPT_24AUG2026.md`
- `archive/CUATRECASAS_2014_ONWARD_BILLING_GMAIL_DRIVE_COLLECTION_PROMPT_24AUG2026.md`
- `archive/CUATRECASAS_BILLING_CLARIFICATION_EMAIL_DRAFT_24AUG2026.md`
- `scripts/validate_cuatrecasas_invoice_audit.py`
- `archive/MISSING_EVIDENCE_REGISTER.md`, especially `ME-080` and `ME-083`

The useful controls are now represented through:

- `assets/data/cuatrecasas-invoice-payment-register-v1.json`
- `assets/data/cuatrecasas-wip-reconciliation-v1.json`
- `scripts/validate_cuatrecasas_invoice_payment_register.py`
- `scripts/validate_cuatrecasas_wip_reconciliation.py`
- bilingual invoice/payment and WIP publication tracks.

## Recovered WIP controls

The 3 July 2019 Cuatrecasas table separated the 22 issued invoices from three non-invoice lines:

| Line | Amount |
|---|---:|
| 2018 works to be invoiced | EUR 61,404.95 |
| 2019 works to be invoiced | EUR 31,020.00 |
| Estimate of work until end of 2019 | EUR 60,000.00 |
| **Aggregate WIP + estimate presentation** | **EUR 152,424.95** |

The 15 June 2020 native Cuatrecasas Collections email, now located directly, states separately:

- unpaid bills: EUR 136,830.72 plus VAT;
- work carried out: EUR 161,738.75 plus VAT;
- approximate description: around EUR 400,000 pending.

The headline movement from EUR 152,424.95 to EUR 161,738.75 is EUR 9,313.80, but the categories are not fully like-for-like because the 2019 aggregate includes a EUR 60,000 forward estimate.

Invoice 1810219093 supplies a second open bridge: EUR 97,492.50 stated accrued less EUR 30,000 actually invoiced equals EUR 67,492.50, versus EUR 61,404.95 later shown as 2018 works to be invoiced. The EUR 6,087.55 difference requires the work-level ledger.

## ME-083 correction

Legacy GitHub status: native 2020 Collections source missing.

Current status: **PARTIALLY CLOSED 13-SEP-2026**. The native 15 June 2020 email has been located and read directly. The remaining gap is the itemised ledger underlying EUR 161,738.75 and the mapping from WIP into proformas, pagarés and later claims.

## Quarterly / trimestral control

Literal GitHub searches did not identify a separate `AnythingQuarterly` entity or corpus. The relevant recurring quarterly source is the 20 December 2018 `4º Informe trimestral LUCHY PLAYA BLANCA` already controlled as `CUA-SRC-002`.

Authorship rule: **ADMINISTRACIÓN CONCURSAL THIRD-PARTY SOURCE — NOT CUATRECASAS-AUTHORED.** It can inform insolvency chronology and knowledge, but it must not be counted as a Cuatrecasas invoice, WIP statement or authored report.

### Wider ME-080 chain

The legacy missing-evidence register also contains `ME-080`, described as the complete **2017–2022 liquidation-plan, quarterly-report, EUR 400,000 and extension chain**. That is a wider insolvency/accounting reconstruction problem and should be preserved as an interlinked but separate evidence gap.

**Non-merger rule:** the `ME-080` EUR 400,000 reference is not automatically the same accounting object as the approximate EUR 400,000 described by Cuatrecasas Collections on 15 June 2020. No identity between those figures is asserted unless primary documents establish the common source, date, components and accounting purpose.

Required wider recovery includes the native liquidation-plan / observations / clarification chain, Article 152 or equivalent quarterly reports, deeds or transaction documents, payment/accounting trail, the 4 February 2020 and later extension material, and the actual implementation record. This belongs to the Concurso 36/2012 accounting track and can cross-link to WIP only where a document-specific bridge exists.

## Migration decision

The legacy invoice-audit JSON and validator were not blindly copied as competing current ledgers. Their useful invariants, reissue controls, WIP distinctions and payment-evidence discipline were migrated into the current GitLab registers and validators. Later primary evidence should update the canonical current objects rather than fork parallel totals.
