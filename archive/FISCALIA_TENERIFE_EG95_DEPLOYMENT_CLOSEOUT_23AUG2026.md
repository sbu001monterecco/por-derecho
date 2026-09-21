# FISCALÍA TENERIFE EG 95/2026 — DEPLOYMENT CLOSEOUT

**Date:** 23 August 2026  
**Status:** **MERGED TO MAIN AND LIVE-VERIFIED — FULL PROPAGATION COMPLETE**  
**Repository:** `sbu001monterecco/por-derecho`

## 1. Implementation record

The current-main implementation was merged through PR `#810`, **Integrate Fiscalía Tenerife EG 95/2026 on current main**.

- Implementation merge commit: `1e1bcae6513906080a02a79f6f6d0e649158ad2f`
- Subsequent main commit inspected during verification: `5acefbd376133ed7154d21309e4682aab94266a8`
- The subsequent commit descends from the implementation merge; it does not supersede or remove the EG 95/2026 package.

The implementation replaced the stale draft architecture of PR `#736` with a reconstruction based on current `main`.

## 2. Repository package now in main

The merged package includes:

1. complete controlled text of the outgoing 21 August 2026 email;
2. complete controlled text of Fiscalía's notification email;
3. controlled Spanish transcription of the EG 95/2026 Decree;
4. full English translation of the Decree;
5. source, custody, hash and scope manifest;
6. recovered bilingual DIP 20/2026 comparator;
7. retrieval gate;
8. correction-register append;
9. missing-evidence-register append;
10. machine-readable state file;
11. current handover;
12. Spanish and English public pages;
13. source-controlled propagation to DP 748, both institutional registers and both updates pages;
14. dedicated sitemap and `robots.txt` declaration;
15. source-specific repository validation and regression controls.

## 3. Controlled substantive position

The repository and website now state consistently that:

- Fiscalía Provincial de Santa Cruz de Tenerife opened and archived **Expediente Gubernativo 95/2026** on 21 August 2026;
- the stated reason was that Fiscalía regarded the matter as judicialised in DP 748/2026 and considered that it could not open parallel prosecutorial investigation proceedings or order the requested steps outside that judicial file;
- the Decree did not reopen DP 748/2026;
- the Decree did not expressly determine that the newly supplied documents were false, irrelevant, exculpatory or insufficient on their merits;
- the complete email also requested preservation, association with earlier Fiscalía records, cross-file separation and finite ETJ 163/2020 / Cambiario 1048/2019 checks that were not individually decided in the Decree;
- this documented difference supports a respectful scope-and-traceability objection, but does not by itself prove bad faith or legal invalidity;
- EG 95/2026, DP 748/2026 and DIP 20/2026 remain separate records;
- the exact scope of DIP 7/2026 and DIP 12/2026 remains unverified;
- and judicial incorporation of the 21 August email and annexes remains unverified.

## 4. Live-verification record

Dedicated live-verification PR `#812`, **Verify Fiscalía Tenerife EG 95/2026 live publication**, ran against the public GitHub Pages edge.

- Verification branch head tested: `fdf078286d49342de36cfc1fcf5fbb8d061954fb`
- Workflow: `Verify Fiscalía Tenerife EG 95/2026 live`
- Workflow run ID: `32608724123`
- Job ID: `97118025580`
- Result: **success**
- Verification completed: 23 August 2026 at approximately 00:47 UTC

The same branch also passed:

- `Publication integrity gate` — success;
- `Off-GitHub Preservation Snapshot` — success.

## 5. Static public-edge verification

The static verifier succeeded on its first attempt.

| Public route or asset | HTTP | Bytes observed | Required markers |
|---|---:|---:|---|
| `/es/fiscalia-tenerife-eg95-2026/` | 200 | 11,424 | Present |
| `/en/fiscalia-tenerife-eg95-2026/` | 200 | 11,372 | Present |
| `/assets/fiscalia-eg95-propagation-20260823.js` | 200 | 9,287 | Present |
| `/assets/site-pre-intervencion-highlight-20260820.js` | 200 | 828 | Present |
| `/sitemap-fiscalia-tenerife.xml` | 200 | 1,410 | Present |
| `/robots.txt` | 200 | 2,918 | Present |

The verifier confirmed both bilingual routes, the propagation module, its loader hook, sitemap discovery and robots declaration.

## 6. Rendered browser verification

Playwright with the public production host verified all of the following rendered states:

| Route | Rendered element | Result |
|---|---|---|
| Spanish EG 95/2026 page | Main heading and procedural framing | Passed |
| English EG 95/2026 page | Main heading and procedural framing | Passed |
| Spanish DP 748/2026 page | Dated EG 95/2026 notice and merits boundary | Passed |
| Spanish institutional register | Distinct Santa Cruz de Tenerife EG 95/2026 record | Passed |
| English institutional register | Distinct Santa Cruz de Tenerife File 95/2026 record | Passed |
| Spanish material-updates page | 21 August Fiscalía entry | Passed |
| English material-updates page | 21 August Public Prosecutor entry | Passed |

The rendered DP 748 notice expressly states that the Decree did not declare the supplied documents false, irrelevant or insufficient and that incorporation into DP 748/2026 is not confirmed.

## 7. Native-source custody and publication boundary

The following native sources remain preserved in connected Gmail and private Google Drive, with identifiers, exact sizes and SHA-256 hashes recorded in the source manifest:

- EG 95/2026 native Decree PDF;
- two native outgoing PNG annexes;
- DIP 20/2026 native Decree PDF;
- DIP 20/2026 native official communication PDF.

They remain outside public GitHub pending a separate personal-data, confidentiality, necessity and proportionality decision. Public GitHub contains the controlled text, translation, metadata, hashes, evidential limits and retrieval instructions.

## 8. Open evidence retained

The implementation does not pretend to have resolved:

1. the judicial decision of 16 July 2026 cited by the EG 95 Decree;
2. the native decisions and exact scope of DIP 7/2026 and DIP 12/2026;
3. proof that the 21 August email and annexes were incorporated into, forwarded to or considered within DP 748/2026;
4. individual treatment of the preservation, ETJ/Cambiario, debtor/asset-selection, remate/cession and bounded local-evidence requests;
5. the certified current state and any irreversible property effect in ETJ 163/2020.

These remain source-completion targets, not negative inferences.

## 9. Supersession and continuity

- PR `#810` is the controlling implementation PR.
- PR `#812` is the controlling live-verification and deployment-closeout PR.
- Draft PR `#736` is superseded and should not be merged.
- The prior deletion audit remains historically useful for showing the earlier unmerged state, but this closeout supersedes that implementation-status description.

## 10. Final classification

**FULLY UPDATED FOR THE CURRENTLY LOCATED SOURCE SET.**

The complete controlled source record, translation, corrections, evidence gaps, bilingual pages, cross-site propagation, static discovery, privacy boundary, preservation state and live deployment have all been implemented and independently verified.

**DELETION-SAFE WITH OPEN EVIDENCE.** The remaining gaps are expressly recorded and do not depend on conversational memory.
