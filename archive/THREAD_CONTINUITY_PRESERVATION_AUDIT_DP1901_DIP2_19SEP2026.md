# Thread continuity and preservation audit — DP 1901/2026 · DIP 2/2026 · 14 September Auto

**Control date:** 19 September 2026  
**Audit ID:** `PD-THREAD-CONTINUITY-DP1901-DIP2-20260919-01`  
**Repository:** `sbu001monterecco/por-derecho`  
**Scope:** June 2026 complaint lanes, DIP 2/2026, DP 1901/2026, 29 July Fiscal intervention, 14 September Auto, E.G. 745 successor inputs, CGPJ continuity and the associated GitHub publication/preservation controls.  
**Audit base main:** `1218d40864e735fee22b9c3fcae78b95018605b0`  
**Status:** **SUBSTANTIVE_CONTINUITY_PRESERVED / SOURCE-PUBLICATION LIVE_VERIFIED / THREAD_DELETION_SAFE**.

## 1. Controlling substantive state

The controlling repository formulation is:

> **PROCEDURAL_IDENTITY_COLLISION_OPEN — DIRECTION NOT CERTIFIED.**

The available record now establishes, without resolving the direction of the collision:

- a separate judge/judicial-conduct complaint was presented on **18 June 2026** under daily reference **24**;
- a separate five-private-actor complaint was presented on **25 June 2026** under daily reference **21**;
- the dependent judge supplement presented on **25 June** expressly belongs to the daily-reference-24 complaint;
- on **9 July 2026**, private-actor amplification/documentary material was physically tendered under **DP 1901/2026, Plaza 6**;
- the signed **12 July** providencia in that same DP/NIG/IUP sent the admission question to Ministerio Fiscal in relation to **DIP 2/2026**;
- the **14 September 2026 Auto** treats DP 1901 as a proceeding for alleged judicial prevaricación, records a Ministerio Fiscal report dated **29 July 2026** seeking archive, and orders `sobreseimiento libre y archivo`.

None of those facts proves which June filing originally generated DP 1901 or that a formal joinder/reassignment/segregation occurred.

## 2. Source denominators and version control

The recovered, hash-controlled complaint-source set is now fixed as follows:

### Private-actor lane

- 25 June complaint: **86 pages**;
- 26 June immediate amplification: **26 pages**;
- 9 July final signed amplification: **19 pages**.

### Judge lane

- signed presentation package: **79 pages total**;
- principal-document bundle: **31 pages**;
- internally paginated principal pleading: **27 pages**;
- presentation/manifiesto front matter: **4 pages**;
- dependent 25 June supplement: **13 pages**.

The controlling correction rules are **CR-160, CR-161 and CR-162**. Older 69/7/10-page or settled “DP 1901 = private-actor cause” shorthand is superseded.

## 3. Primary repository controls

The continuity state is recoverable through:

- `evidence/judicial/dp-1901-2026/PROCEDURAL_IDENTITY_SOURCE_CLOSURE_18SEP2026.md`;
- `archive/DP1901_EG745_FISCAL_REPORT_ROUTING_COLLISION_CONTROL_18SEP2026.md`;
- `archive/FISCALIA_DIP2_DP1901_FULL_DIGITISATION_CONTROL_18SEP2026.md`;
- `evidence/fiscalia/2026/DIP2_DP1901_FULL_DIGITISATION_STATE_18SEP2026.json`;
- `evidence/fiscalia/2026/MF_SHORTCOMINGS_DP1901_EG745_PRODUCTION_MATRIX_18SEP2026.md`;
- `drafts/judicial/2026-09-18_DP1901_AUTO14SEP_RESPONSE_ARCHITECTURE_DRAFT.md`;
- `drafts/fiscalia/2026-09-18_EG745_DP1901_SUPERVENING_EVENT_PATCH_DRAFT.md`;
- `ops/DP1901_EG745_MF_IMMEDIATE_ACTION_MATRIX_18SEP2026.md`;
- `assets/data/control-21-22-24-continuity-v1.json`;
- `data/three-track-full-digitisation-20260904.json`;
- `archive/CORRECTION_REGISTER.md`.

## 4. GitHub merge / CI continuity

Material GitHub checkpoints already completed before this audit:

- **PR #1574** — DP1901/DIP2 source closure and routing reconciliation; merge commit `3f9b73232083b2fc9fb99e49a69909dfbeaef510`;
- **PR #1587** — deterministic Fiscalía/proceedings interconnectivity projection refresh; merge commit `3511759f4d2751229dce6a6c6e293011cf549ad5`;
- PR #1587 exact head passed:
  - Release acceptance;
  - Publication integrity gate;
  - Validate Fiscalía proceedings interconnectivity;
  - Validate audience experience;
  - Off-GitHub Preservation Snapshot;
- **PR #1592** — later institutional-continuity preservation; merge commit `41a9b3aaad2410746136beeec0377ad86e43a768`; Release Acceptance, Publication Integrity and Off-GitHub Preservation Snapshot passed on its reviewed head.

The later main commit `1218d40864e735fee22b9c3fcae78b95018605b0` records the merged DP1901 implementation state and preserves the remaining legal actions as **not filed**.

## 5. Public GitHub routes that must remain mutually consistent

- `/es/dp-1901-2026/`
- `/en/dp-1901-2026/`
- `/es/dp-1901-2026-auto-14-septiembre-2026/`
- `/en/dp-1901-2026-order-14-september-2026/`
- `/es/fiscalia-dip-2-2026/`
- `/en/fiscalia-dip-2-2026/`

The dedicated verifier added by this audit is:

- `.github/workflows/verify-dp1901-dip2-live-origin.yml`
- commit-status context: `pages-propagation/dp1901-dip2`.

On every relevant push to `main`, it fails closed unless:

1. GitHub records a successful **exact-SHA** `pages build and deployment` run; and
2. the six bilingual HTML routes plus the two central public PDF sources are byte-identical to the checked-out source files at that same SHA.

This is deliberately stronger than search-engine or crawler readback.

## 5A. Exact GitHub Pages deployment attestation — 19 September 2026

The source/publication state was verified against the exact deployed main SHA:

- source/deployment SHA: `fd9baa22040218c95a887aab41032d1d74b00195`;
- GitHub Pages run: **#1588**, run ID **35411598728**, successful;
- dedicated verifier: **Verify DP1901 DIP2 live origin #9**, run ID **35411734472**, successful;
- result: **LIVE_BYTES_VERIFIED**;
- byte-identical controlled resources: **8/8**.

The eight resources were the six bilingual DP1901/DIP2 HTML routes listed above plus:

1. `evidence/judicial/dp-1901-2026/public-pdfs/auto-14sep2026-public-controlled-transcription.pdf`;
2. `evidence/fiscalia/dip-2-2026/public-pdfs/decreto-archivo-dip-2-2026-06mar2026-public-redacted.pdf`.

PR #1597 makes this exact-main deployment attestation visible during pull-request CI without granting CI write permission. It is a verification-only successor and does not modify the eight controlled source resources.

## 6. Private-source custody / Evidence Manifest

The live private Evidence Manifest was updated during the source-closure work to preserve, among other records:

- `FIS-063` / `FIS-064` — the 11 March DIP2 correction and REGAGE receipt;
- `DP1901-SRC-001` through `DP1901-SRC-006` — stamped June/July routing images and ATLANTE/tender evidence;
- `DP21-DOC-001` through `DP21-DOC-003` — operative 86/26/19-page private-actor source PDFs;
- `JUD24-DOC-001` / `JUD24-DOC-002` — 79-page judge package and 13-page dependent supplement.

Raw private originals remain outside public Git. Public Git preserves source identities, hashes, controlled transcriptions/derivatives and evidential limits rather than indiscriminately publishing private originals.

## 7. DIP 2/2026 state

The available located DIP2 corpus is digitised and interlinked:

- 13 January complaint;
- 8 February amplification;
- 6 March archive decree;
- 9 March notice;
- 11 March correction/update;
- REGAGE26e00026303869 receipt;
- automated registry-routing trace reporting passage to the Fiscalía CAC General Registry for processing.

The documented appeal-status discrepancy is a **source-to-premise discrepancy**. It does not itself prove deliberate falsehood, criminal prosecutorial conduct or invalidity of every other ground.

## 8. Authority-only gaps — intentionally still open

These gaps cannot be closed from the presently connected private/repository corpus and must not be filled by inference:

1. separate **11 February 2026 DIP2 opening decree**;
2. complete certified DIP2 file/index;
3. substantive incorporation/access/treatment/reconsideration of the 11 March correction;
4. exact initiating document that generated DP1901/NIG/IUP;
5. certified daily-reference-21 / daily-reference-24 reparto and destination history;
6. 18 June–12 July scan/ingestion/document-to-NIG association history;
7. every formal joinder/reassignment/remittal/accumulation/segregation act;
8. electronic incorporation status of the 9 July private-actor amplification;
9. exact corpus/index sent to Ministerio Fiscal before 29 July;
10. signed **29 July Fiscal report**, author, assignment, reasoning and any review/visado;
11. native/certified **14 September Auto** and legally operative notification/access metadata.

## 9. Legal-work-product boundary

Repository publication is not filing.

At the time of this audit:

- the DP1901 response architecture is **not filed**;
- the intended next legal product is the actual Spanish `recurso de reforma + subsidiaria apelación`, subject to notification-date control and counsel review;
- the E.G. 745 successor patch is **not filed** merely because it exists in GitHub;
- the proposed CGPJ Alzada 286 supervening-event supplement is **not filed** merely because it is prepared;
- no authority-production request is treated as sent unless separate transmission/registration evidence exists.

## 10. Attribution and liability boundary

The record may support criticism of process, provenance, source denominator, competence questions, appeal-history treatment and the distinction between evidential insufficiency and legal non-criminality.

It does **not** by itself prove:

- judicial prevaricación;
- prosecutorial misconduct;
- capture;
- collusion or coordination;
- intentional misrouting;
- criminal liability of the private actors or office-holders.

Responsibility remains actor-specific, source-led and open to lawful contrary explanations.

## 11. GitLab parity

GitLab remains the intended canonical repository under the wider project governance model, but authenticated access is currently blocked.

Therefore:

- GitHub is the active recovery/publication layer;
- the newer GitHub state must not later be overwritten by older GitLab public content;
- when GitLab access returns, reconcile from the newer GitHub source closure through a reviewed merge and preserve both histories.

This is an operational parity gap, not a GitHub preservation gap.

## 12. Continuity / retirement verdict

### Substantive continuity

**PASS.**

The material project state is preserved outside this conversation: sources, hashes, corrections, route identity, open gaps, legal-work-product boundaries, interconnectivity refresh and CI history are all represented in GitHub and the private custody register.

### Preservation

**PASS.**

The relevant reviewed PRs include successful Off-GitHub Preservation Snapshot checks, while private originals remain held in connected/private custody rather than being replaced by public derivatives.

### Deployment

**PASS — LIVE_VERIFIED.**

GitHub Pages run #1588 / 35411598728 successfully deployed exact SHA `fd9baa22040218c95a887aab41032d1d74b00195`. Dedicated verifier run 35411734472 then confirmed **8/8 byte-identical controlled public resources**. The verifier remains fail-closed for future relevant pushes.

### Thread retirement

**THREAD_DELETION_SAFE_FOR_SUBSTANTIVE_PROJECT_CONTINUITY.**

The source/publication state is merged, preservation-controlled and exact-live verified. Deleting the chat would not remove the sole record of a material source, correction, repository action, open obligation or deployment rule. Authority-only gaps and unfiled legal work products remain explicitly recorded outside the chat.
