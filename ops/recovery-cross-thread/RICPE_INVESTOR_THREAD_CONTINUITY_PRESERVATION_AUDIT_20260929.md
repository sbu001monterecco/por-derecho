# RICPE investor-identification thread — continuity and preservation audit

**Audit date:** 29 September 2026  
**Status:** PUBLIC-SAFE CONTINUITY RECORD — SOURCE-BOUNDED  
**Scope:** RIC Private Equity / investor identity / Tenerife origination / Sun Park–HNT–MYND Yaiza capital traceability  
**Canonical investor-register ID:** `PD-SP-RICPE-INVESTOR-REGISTRY-001`  
**Investor-position namespace:** `PD-SP-RICINV-####`

## 1. Purpose

Preserve the durable conclusions and controls developed in the working thread without publishing private correspondence, contact details, unverified private identities, KYC/AML material, bank data, or the identity of a short-tenure former investor-relations employee.

The objective is to reconstruct **every evidenced RICPE shareholder / subscriber / investor position over time**, not merely to produce a list of names.

Canonical flow:

`unknown investor position -> PD-SP-RICINV-#### -> primary identity evidence -> PD-SP-P-#### / PD-SP-O-#### crosswalk -> subscription/capital event -> share series/project -> transfer/status -> representation/notice/correction history`

## 2. Durable findings to preserve

1. RICPE publicly disclosed a **51-shareholder snapshot in 2022**. The 51 positions are a snapshot denominator, not a ceiling on historical or later investors.
2. Reserve `PD-SP-RICINV-0001` through `PD-SP-RICINV-0051` for that 2022 snapshot. Continue at `PD-SP-RICINV-0052` only when evidence establishes another distinct position.
3. A RICINV reference identifies an investor/shareholder **position**, not necessarily a natural person or company. Once identity is established, retain the RICINV reference and crosswalk it to the canonical person/organisation ID.
4. Do not merge positions because names, dates, addresses, networks or circumstances look similar. Merge only on primary evidence.
5. Investor/shareholder status alone creates **no inference of knowledge, wrongdoing, complicity or responsibility**.
6. The material public fact concerning staffing is that RICPE had a dedicated **Investor Relations** function during the relevant capital period. The short-tenure former employee's identity is not necessary for the public investor-register narrative.
7. Q4 2022 is a material reconstruction window. Reported NAV/patrimony movement and registered nominal capital increases must not be equated with cash raised without subscription/share-premium/payment evidence.
8. The five capital increases registered on **23 December 2022** are separate capital events whose subscriber population, share premium, payments and new-versus-existing-holder status require native records.
9. The **14 September 2022 Santa Cruz de Tenerife** collective-RIC investment event is an origination/lead-generation traceability event. Attendance is not evidence of investment. Required chain: attendee/lead -> introduction/source -> CRM/follow-up -> subscription evidence.
10. Sun Park / HNT / MYND Yaiza requires project-specific investor reconstruction. Existing controlled work records **Series F (2022): 253 shares / EUR 1,598,849.32** and **Series G (2023): 785 shares / EUR 4,974,853.78**. Share count is not unique-subscriber count.
11. The register must expand to historical shareholders, later subscribers, transfers, cancellations/redemptions where applicable, successor holders, corporate investors and lawful beneficial-owner crosswalks.
12. Representation history matters: where evidence permits, each investor position should be linked to the version of project/investor material received and to any later correction or notification.

## 3. Native evidence priority

Highest-value records remain:

- Libro Registro de Acciones Nominativas for the full relevant period;
- subscription commitments/forms and allocation records;
- capital-increase deeds, Board/shareholder resolutions and subscription terms;
- bank receipts and share-premium/payment evidence;
- transfer, cancellation/redemption and successor-holder records;
- DFI / investor-information delivery acknowledgments and risk questionnaires;
- CRM lead-source / introducer / meeting / call / follow-up history;
- investor-event attendee and registration lists, especially Tenerife;
- KYC/AML and beneficial-owner records where lawfully obtainable and necessary;
- Series F/G -> HNT/MYND funding crosswalk;
- correction/notification records showing which investors received which representations.

## 4. Evidence-state discipline

Use at least these states:

- `ANONYMOUS_POSITION`
- `CANDIDATE_IDENTITY`
- `PRIMARY_EVIDENCE_IDENTIFIED`
- `RECONCILED_ACROSS_EVENTS`

A candidate identity must never silently become an identified investor.

## 5. Event-centric extension

The identity register should also cross-reference canonical event objects:

- capital-increase events;
- subscription events;
- investor-origination events;
- share-series allocations;
- transfers/successions;
- representation/document-version delivery;
- corrections/notices.

This turns the register into a temporal capital graph rather than a flat name list.

## 6. Privacy / publication boundary

Public-safe outputs may show canonical anonymous IDs, aggregate source facts, capital-event references, evidence status and open evidence requests. Do not publish a private investor's identity merely because the person/entity invested. Do not publish private correspondence, personal contact data, KYC/AML, bank/source-of-funds data or other controlled evidence without a lawful, proportionate and evidence-led basis.

## 7. Repository continuity correction

Earlier work created an investor-register lane in GitLab MR !431. That work must not be treated as the current live-publication state. The durable substantive material was later preserved through successor repository work; stale !431 public-page machinery must not be resurrected blindly.

Current rule: **preserve the canonical methodology and source-controlled investor reconstruction; separately verify any public-page/live status before claiming deployment.**

## 8. Cross-host preservation rule

GitHub and GitLab are continuity counterparts, not permission to blind-mirror entire repositories. This audit is deliberately public-safe and may be preserved on both hosts. Native/private evidence remains in its controlled store. Reconciliation must be selective, source-aware and non-destructive.

## 9. Thread closeout status

**Continuity:** PASS — durable conclusions captured.  
**Privacy:** PASS — no private contact details, correspondence bodies, investor identities, KYC/AML or banking data introduced.  
**Identity discipline:** PASS — anonymous investor slots remain non-adverse and evidence-gated.  
**Capital traceability:** OPEN — subscriber-level reconstruction remains incomplete.  
**Tenerife origination:** OPEN — attendee/CRM/subscription conversion evidence remains to be obtained.  
**Series F/G investor identity:** OPEN — unique subscribers remain unresolved pending native evidence.  
**Public-page status:** NOT ASSERTED by this audit.  
**Preservation:** this file is the public-safe handoff for continuation of the thread.
