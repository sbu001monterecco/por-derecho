# Cross-thread repository, website and email rescan and action register — 23 August 2026

**Status:** CONTROLLING CROSS-THREAD RESCAN REGISTER  
**Cut-off:** 23 August 2026, after the merge of PRs #830, #832, #833 and #808  
**Purpose:** preserve what was rechecked, distinguish completed publication from open work, and prevent a future thread from treating an email, receipt, workflow notice or proposed publication as more than the evidence establishes.

## 1. Completed and rechecked publication

The repository and public website now preserve the following controls:

1. Gil Marer / Aweswell's direct, actor-specific criminal attribution concerning CAM / Acosta Matos and connected private actors is not to be reduced to a concern, question, possible involvement or merely an investigative lead.
2. Attribution, evidence, contrary material, missing proof, adjudication/procedure and source literal remain separate fields.
3. The attribution is not presented as adjudicated guilt or as a judicial finding.
4. Laura Patricia Acosta Matos is the controlled narrative identity. The contemporaneous source literal “Laura Matos” remains visibly source-literal and is not silently rewritten.
5. The strongest contrary record, including the 2018 provisional dismissal position, actor-specific proof requirements, presumption of innocence and right of reply, remains visible.
6. The direct-attribution panel remains part of the public first read rather than being hidden inside collapsed specialist material.
7. The static English and Spanish homepage actor chronology now uses the locked minimum dates: Francisco Mario Matos Matas by 22 June 2011; Antonio Cogolludo Rojas by 10 April 2014; and Shaila María Cogolludo Ramos by 8 April 2014.

Publication lineage:

- PR #830 — substantive anti-dilution, source-fidelity and first-read package; merge `05cba3c9af7071f96b56eae90a67a2ceae3a783d`.
- PR #832 — read-only post-deployment verifier.
- PR #833 — verifier made observable on pull-request checks.
- Live verification run `32636419354` — PASS across the bilingual CAM dossiers, both homepages, the loader, first-read module, cross-site CAM module and machine-readable record.
- PR #808 — bilingual static homepage actor chronology correction; merge `22f10cea2cab18539c55d6283eb9ebce16d40f71`.

This closeout adds a separate public machine-readable status record and extends the live verifier to cover that record and the corrected static chronology.

## 2. Fresh email rescan — evidential classifications

### 2.1 New REGAGE receipt

A receipt dated 23 August 2026 bearing registration number `REGAGE26e00074403517` was located. The available receipt text proves the existence of that registration number. It does **not**, by itself, prove the destination, attached package, routing, acceptance, legal effect or merits treatment.

Control: keep the item in an unclassified intake state until the destination and exact submitted package are bridged by primary evidence. Do not insert it into a substantive proceedings chronology as delivery proof before that bridge exists.

### 2.2 Ruth Ugalde outreach

An outgoing message dated 23 August 2026 with the subject line “RTB: Sun Park, Gran Canaria — possession control, insolvency and state-backed disposal” was located. It contained no attachments, linked to three public Por Derecho resources and offered a five-source index. No substantive reply was located in this rescan.

Control: classify the outreach as **SENT / AWAITING RESPONSE**. It does not prove receipt by a named person, editorial review, acceptance, endorsement or publication. Do not resend or follow up without a new, exact authorization covering the final recipient list, subject, body, links and attachments.

### 2.3 Outbound-email control incident

The rescan located two transmissions that should not have been used as tests: an empty message titled “DO NOT SEND” transmitted to a real external address, and a one-character test sent to a reserved invalid address which bounced. Neither carried the substantive evidence package. They nevertheless demonstrate that a written no-send rule is insufficient without a hard technical and procedural stop.

Control implemented in this package: no external test sends; no empty, one-character, placeholder or “DO NOT SEND” messages; no test use of real or deliberately invalid recipient addresses; drafts and local rendering only until a fresh exact authorization is recorded.

### 2.4 Automated acknowledgements and out-of-office replies

Automated acknowledgements, delivery receipts and out-of-office replies were present across other outreach threads. They prove only the limited event stated in the native message. They do not prove merits review, institutional adoption, forwarding to the competent destination or agreement with the allegation.

Control: no automatic rerouting, forwarding, follow-up or substitute-recipient send may be inferred from an out-of-office reply.

## 3. Other thread decisions

### 3.1 PR #804 — redacted 21 April 2016 email publication

PR #804 remains a draft, explicitly approval-gated and presently non-mergeable. It must not be merged in its current state. Before any renewed approval request it requires:

- rebase onto current `main`;
- recovery of the best available native message and headers, or an explicit source-status limitation if unavailable;
- reconciliation of the raw-export hash with the legacy PDF hash;
- refreshed bilingual render and link validation;
- a fresh privacy and source-fidelity review;
- Gil's exact final publication authorization after the final diff is available.

### 3.2 ACTA publication and preservation threads

ACTA-related threads remain outside this deletion decision where native preservation, source-line verification, full-text/image parity, privacy review or public-render checks remain open. A safe closeout in this CAM thread must not be read as closing those separate ACTA obligations.

### 3.3 Workflow-alert hygiene

The inbox contains repeated failure notices from older live-verification workflows triggered by unrelated `main` changes. The notices cannot be dismissed automatically, but neither should they be treated as proof of substantive regression without the failing marker and live route being examined.

Recommended repository maintenance:

- narrow each legacy verifier's path triggers to its controlled sources;
- version live markers and record which source commit introduced them;
- use bounded Pages-propagation retries before failure;
- separate source-validation, deployment and public-edge conclusions;
- suppress duplicate notifications only after an equivalent required check remains observable;
- maintain one current canonical verifier per publication family and retire superseded duplicates through an auditable PR.

No specific legacy verifier is declared defective by this register where its complete failing log was not recovered during the rescan.

## 4. Actions implemented by this closeout package

- merged the static bilingual chronology correction in PR #808;
- replaced the stale CAM deletion audit with the actual PR #830/#832/#833/#808 lineage;
- added a public machine-readable CAM thread-closeout record;
- extended the read-only public-edge verifier to test the closeout record and corrected static chronology;
- hardened the outbound-email authorization rule;
- created controlled records for the new REGAGE intake, Ruth Ugalde outreach and outbound-email incident;
- updated the future outbound-email handover and journalist/media register;
- added a visible publication-control link to the CAM cross-site module.

## 5. Deliberately not done

- No email, correction, resend or follow-up was sent in this closeout.
- PR #804 was not merged.
- No REGAGE destination or package was guessed.
- No automated acknowledgement or out-of-office reply was treated as a merits response.
- No separate ACTA thread was declared deletion-safe.
- No criminal allegation was converted into an adjudicated finding.

## 6. Cross-thread priority order

1. Preserve the direct criminal attribution and source-fidelity controls already live.
2. Close the native-source and hash bridge for PR #804 before seeking renewed publication approval.
3. Classify `REGAGE26e00074403517` by destination and package from primary evidence.
4. Await any substantive Ruth Ugalde response; do not send again without fresh exact authorization.
5. Complete ACTA native-preservation and source-line gaps in their own threads.
6. Consolidate legacy live verifiers without weakening any required public-edge control.

This register is a recoverable handover. It does not depend on the chat thread for its meaning.

## 7. Master email/files scan-request batch queue — active-estate and 18-PDF corpus

**Activated:** 23 August 2026  
**Controlling source register:** `archive/SUN_PARK_ACTIVE_ESTATE_2018_2021_EIGHT_SOURCE_SUPPLEMENT_23AUG2026.md`  
**Canonical gap rows:** `ME-012`, `ME-050`, `ME-074`–`ME-076`, plus the cross-referenced existing ME / ME-CAM7J rows.

The eighteen uploads have been reconciled as seventeen unique binaries and sixteen documentary items. Five later binaries already match private custody rows `MAT-005`–`MAT-009`; one CAM print is a source variant; the two 18-page photo PDFs are exact duplicates. Do not upload or count them again as independent corroboration.

Run future scans as resumable micro-batches and write results back to the canonical ME row and source supplement. A no-result search is logged; it is not proof of non-existence.

| Batch | Source-completion IDs | Exact focus | Primary search locations / query ladder | Exit condition |
|---|---|---|---|---|
| `AE-01` | `ME-PDFSCAN-001`–`004` | 24-Oct-2019 anchor; 4-Nov reposición + blocks; AP 23-Jul-2019; interest/Community certificates and final amounts | exact dates + `36/2012` + `Auto` / `reposición` / `3.079.104,66` / `3.182.000`; Drive, Gmail attachments, counsel/procurador files, court-certified index | signed acts and annex inventory located, hashed and linked, or negative-search log complete |
| `AE-02` | `ME-PDFSCAN-005`–`008` | Aweswell photographic dossier; Jan/Feb-2021 reposición/DIOR; AC opposition/certificates/reports; CAM `DOCUMENTO NÚMERO UNO` | `7299`, `654/2021`, `690/2021`, `13 enero 2021`, `4 febrero 2021`, `9 febrero 2021`, `15 enero 2019`, `estado masa activa`, `certificación Comunidad`; Gmail/Drive/LexNET/counsel/Community | each filing, receipt and expressly cited annex reconciled |
| `AE-03` | `ME-PDFSCAN-009`–`011` | CAM 54-unit title; municipal licence/plans/works; finca-photo overlay; access/key/security requests and logs | Registry/deeds, Yaiza licence/project file, CAM/contractor records, Community/security/locksmith files, expert/notary correspondence | date-specific unit/title/licence/access matrix produced or remaining custodian stated |
| `AE-04` | `ME-PDFSCAN-012`, `ME-075` | native 23-Feb/8-Mar-2021 email, photographic attachment and complete request→response→inspection outcome | Gmail exact subject `autorización para peritos - informe estado de la masa activa de Luchy Hotel Sun Park (36/2012)`; sent/all-mail/Trash; Google Takeout; recipient mailboxes; Drive attachment search | `.eml`/RFC822 + MIME/headers + attachments + later responses/outcome hashed, or bounded negative log |
| `AE-05` | `ME-PDFSCAN-013`–`014` | RPC publication, offer/auction/due diligence; later responsibility/appeal, restitution, rectification and EUR 400,000 accounting | RPC, Concurso/LexNET, AC data room/accounts, bidder correspondence, deeds/Registry, court/appeal/counsel files | full decision and implementation chain reconciled |
| `AE-06` | `ME-PDFSCAN-015`–`016`, `ME-076` | original 1-Mar-2018 images/event proof; reconcile CAM pleading variants/receipt/annex | exact annex alias `ANEXO_08D_DOCUMENTO_GRAFICO_CAM_JOAN_CRUZ_01MAR2018`; device/photo libraries, Drive/Gmail, DP 1132 exhibits; CAM/LexNET file | originals/EXIF/identity/context and filing treatment located; duplicate/variant relations fixed |
| `AE-07` | `ME-PDFSCAN-017`–`022` | prior-ten completion: JV 1260; 2014 Fiscalía annexes/outcome; DI 248; May-2019 sequence; complete 2-May order; 1-Aug mixed-bundle components | exact filenames and procedure numbers; court/Fiscalía certified files; LexNET; Gmail/Drive; counsel files; existing repository retrieval aliases | every fragment/bundle separated into source, receipt, opposition, official act and outcome |

### Cross-thread execution rule

Any other thread locating one of these items must:

1. preserve the native source before OCR/redaction;
2. calculate SHA-256 and record filename, bytes, acquisition date, custodian and parent/variant/duplicate relation;
3. update the controlling `ME-*` status instead of creating a parallel generic gap;
4. link the source to the relevant pleading/order and record what it establishes and does not establish;
5. retain personal data, privilege and private binaries outside public Git unless a separate publication gate is approved; and
6. never claim website publication until the merge SHA, Pages deployment and exact live route have been checked.
