# E.G. 745/2026 — deletion-safe continuity handover

**Control date:** 29 August 2026  
**Repository:** `sbu001monterecco/por-derecho`  
**Controlled starting `main`:** `377eb20a0214bf269cbda5f5716e9c75bf77b593`  
**Working branch:** `eg745-continuity-action-diary-20260829`

## 1. Resume rule

A future thread must start from current `main`, then read this file and reconcile later commits. Do not rely on the chat that created this file.

Read at minimum:

- `FISCALIA_INSPECCION_EG_745_2026_DIGITISATION_APPEAL_PACKAGE_29AUG2026.md`
- `evidence/fiscalia/2026/2026-08-26_FGE_INSPECCION_EG_745_2026_NOTIFICATION_DECREE_TRANSCRIPTION.md`
- `evidence/fiscalia/2026/2026-08-26_FGE_INSPECCION_EG_745_2026_ENGLISH_TRANSLATION.md`
- `evidence/fiscalia/2026/2026-08-26_FGE_INSPECCION_EG_745_2026_METADATA.json`
- `evidence/fiscalia/2026/FGE_INSPECCION_EG_745_2026_ANNEX_EVIDENCE_GAP_MATRIX_29AUG2026.md`
- `evidence/fiscalia/2026/EG_745_2026_ACTION_DIARY_29AUG2026.md`
- `evidence/fiscalia/2026/EG_745_2026_COUNTER_ACTION_MATRIX_29AUG2026.md`
- `drafts/fiscalia/2026-08-29_RECURSO_POTESTATIVO_REPOSICION_EG_745_2026_DRAFT.md`
- `drafts/fiscalia/2026-08-29_EG_745_2026_PROTECTIVE_ACCESS_PRESERVATION_REQUEST_DRAFT.md`
- bilingual public E.G. 745/2026 pages and 29 August response-package pages
- `archive/DEPLOYMENT_LOG.md` and the latest publication/continuity controls.

## 2. Authoritative source control

### Official notification/Decree

- Email subject: `NOTIFICACIÓN OFICIO Y DECRETO EXP. GUB. 745/2026`.
- Sender located: Marta Clavero Saavedra, Fiscalía General del Estado — Inspección Fiscal.
- Email timestamp located: 26 August 2026 12:00:49 UTC.
- Attachment: `OFICIO Y DECRETO EXP. 745-26.pdf`.
- Pages: 3.
- Size: 1,111,997 bytes.
- **Native SHA-256:** `1e09c8eb3bce26e28dc5f22e5d6ebad3f458212cf8d85f5920e869fa42554abe`.
- 29 August fresh retrieval reproduced that SHA-256 exactly.
- The native PDF controls over transcription, translation, OCR or any derivative.

### Originating registration

- `REGAGE26e00070235775`.
- Presented 2 August 2026 at 23:31:55; registered at 23:31:58 according to existing controlled material.
- A 3 August 2026 Registro Electrónico General email was freshly located confirming that registration number and processing.
- Controlled receipt SHA-256 already recorded: `33f7b47418062a0bc4993f424e459af18fa2d334acc8bafc4c2e40750f171f97`.

## 3. Official outcome preserved

The controlled transcription records that the 26 August Decreto:

1. archives E.G. 745/2026;
2. characterises the submission as `confusa e incoherente` and invokes article 66.1(c) Law 39/2015;
3. states that no sufficiently concrete irregularity was attributed to a particular fiscal in a particular matter;
4. gives optional reposición within one month or, alternatively, contentious-administrative review before the Supreme Court within two months, subject to the terms stated in the Decree.

Do not silently alter those propositions. Any correction must be a dated amendment linked to its source.

## 4. Fresh filing-status audit — 29 August 2026

Mailbox search was rerun across the relevant August period and specifically across Sent after the 26 August notification.

Located:

- the official 26 August E.G. 745 notification email and attached Decree;
- the 2 August REG-AGE registration evidence and later electronic-register processing email;
- other Fiscalía/FGE communications and preservation/continuity communications.

**Not located:** a post-notification sent E.G. 745/2026 reposición, a REG-AGE receipt for that reposición, a judicial receipt, or equivalent proof that the E.G. 745 merits response was filed.

Therefore the locked status is:

> **REPOSICIÓN — PREPARED / OUTSTANDING — NOT YET VERIFIED AS FILED**

A draft, repository publication, GitHub commit, email about another expediente, or unrelated preservation filing must not be used to upgrade that status.

## 5. Controlled deadlines and ASAP targets

- Working reposición control date: **Monday 28 September 2026**, subject to final verification of the legally effective notification date and any applicable special rule.
- Direct contentious-administrative date: **COUNSEL VERIFY BEFORE FILING**; do not publish a guessed final date.
- Internal ASAP targets are in `EG_745_2026_ACTION_DIARY_29AUG2026.md` and intentionally precede the formal backstop.

Governing rule:

> **File as soon as the filing is substantively ready. Do not wait for the final permitted day merely because time remains.**

## 6. Unresolved evidential gaps

1. Exact legally effective notification date/mechanics for deadline purposes.
2. Exact byte/content identity of the PDF registered on 2 August versus the signed 31 July master; do not assume identity from filename/history.
3. Complete E.G. 745/2026 administrative file and controlled/certified index.
4. Internal routing trace explaining the Decree's reference to an email received on 3 August alongside the 2 August REG-AGE registration.
5. Native/searchable/verifiable electronic version of the Decree and associated metadata/signature-verification data.
6. Official actor-by-actor identification/routing records sufficient to separate documented identity from Gil Marer's attribution and from unresolved identity/knowledge questions.
7. Counsel election between reposición and direct contentious review.
8. Route-specific basis, standing, limitation and causation before any disciplinary, criminal, civil, patrimonial or State-liability filing is treated as mature.

## 7. Public pages at controlled starting point

- ES: `https://sbu001monterecco.github.io/por-derecho/es/fiscalia-inspeccion-exp-gub-745-2026/`
- EN: `https://sbu001monterecco.github.io/por-derecho/en/public-prosecution-inspection-exp-gub-745-2026/`
- ES response package: `https://sbu001monterecco.github.io/por-derecho/es/fiscalia-inspeccion-exp-gub-745-2026/paquete-respuesta-29-agosto-2026.html`
- EN response package: `https://sbu001monterecco.github.io/por-derecho/en/public-prosecution-inspection-exp-gub-745-2026/response-package-29-august-2026.html`

These URLs must be rechecked after the merge/deployment recorded below. A repository merge alone is not deployment proof.

## 8. Public PDF control

The native PDF has been freshly hash-verified. The current repository page deliberately keeps the unredacted native original off the public surface because page 1 contains a direct personal email address and the document contains signatures/other personal-data elements.

**Publication gap:** an appropriate privacy-controlled public PDF derivative must be published as a separate derivative while preserving the native SHA-256 and stating that the native original controls. Do not substitute the derivative for the native source or silently overwrite either one.

The present GitHub connector can create/update UTF-8 repository files but does not expose a binary-file upload action. Therefore this continuity record treats the public-PDF binary as **OPEN — TOOLING BLOCKED**, not as completed. A prepared local derivative, if created, is not publication proof until its repository path and live URL are verified.

## 9. Exact next recommended action

1. Obtain counsel route election and final substantive approval.
2. Close source-identity/effective-notification dependencies that materially affect the bundle.
3. **File as soon as ready**; preserve exact filed bytes and receipt in the repository controls.
4. In parallel, file the distinct access/native-copy/preservation requests without treating them as suspending the merits deadline.
5. Publish the privacy-controlled PDF derivative when a binary-capable repository write path is available; record derivative hash and redactions without changing the native-source hash.

## 10. Merge / deployment closeout

This file was authored on a branch from `377eb20a0214bf269cbda5f5716e9c75bf77b593`. The final PR number, merge SHA, Pages run and live-readback evidence must be appended by the closeout commit after merge. Until then, do not state that this 29 August continuity enhancement is deployed.