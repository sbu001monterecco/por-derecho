# Proceedings website propagation — implementation record

Date: 20 August 2026
Status: **MERGED TO `main` via PR #662**
Merge commit: `3c1cc2ed878bdef43ba8f62fa406dc57fa8da591`
Repository read-back: **verified from current `main`**
Public live read-back: **finite verification item remains open until a successful rendered-site run/browser read-back is recorded**

## Implemented public-safe propagation

1. **Pink Canary / AEAT / Audiencia Nacional 496/2026**
   - New bilingual pages: `en/pink-canary-aeat-496-2026/` and `es/pink-canary-aeat-496-2026/`.
   - Primary source reviewed: Audiencia Nacional, Sala de lo Contencioso-Administrativo, Sección 7ª, Auto 00426/2026 of 6 July 2026, PSS 0000496/2026 0001, linked PO 0000496/2026, NIG 28079 23 3 2026 0002648.
   - Controlled proposition: interim suspension refused; no merits determination of PO 496/2026.
   - Lawyer strategy emails and predictions deliberately excluded.

2. **Cuatrecasas / ICAM / CCACM proceeding boundary**
   - Bilingual pages updated to state expressly that ICAM 434/26 and CCACM 193/2026 are linked complaint/appeal phases of one deontological chain.
   - ETJ 163/2020, DP 748/2026 and other judicial files remain separate proceedings whose facts may provide context.
   - Autonomous ICAM 1487/26 and technical registration 1566/26 remain distinct from the first 434/26 → 193/2026 chain.

3. **Institutional records reconciliation**
   - GUB 86/2026 retained as the already-published Fiscalía territorial referral; not duplicated.
   - CGPJ record updated with Recurso de alzada 286/2026 and REGAGE26e00069061338, while preserving the distinction between a party filing and independently established facts.
   - AEAT record linked to the separate Pink Canary judicial tax proceeding 496/2026.
   - Diputación del Común Q26/574 added with the 19 June 2026 non-admission and the exact limitation that it was not a merits determination.
   - LAJ / Judicial Office supervisory chain added once, with REGAGE26e00073341191 / 73341382 / 73341477 expressly treated as three registry receipts for the same coordinated corpus, not three investigations.

## Publication controls

- No public consolidated master litigation scoreboard was created.
- Registration/receipt is not described as admission or investigation.
- Interim relief is not described as a merits judgment.
- Complaints and party allegations are not converted into verified misconduct findings.
- Confidential annexes, personal contact details, verification credentials and potentially privileged communications are not reproduced.
- EN/ES parity maintained for all substantive changes.

## QA / merge note

The PR-level publication-integrity workflow had one failure caused by a pre-existing repository-wide mission-critical invariant concerning an unrelated `2022-adjudication-documentary-reconstruction` heading. The proceedings files themselves passed the publication/deletion-safety and operational checks inspected in the workflow log. The unrelated pre-existing gate issue was recorded in PR #662 before merge.

## Live-verification control added 20 August 2026

PR #666 added `.github/workflows/verify-pep-proceedings-live.yml` to `main`. The workflow is configured to check both language versions of:

- the institutional-record register;
- Pink Canary / AEAT / Audiencia Nacional 496/2026;
- Cuatrecasas ICAM 434/26 → CCACM 193/2026;
- the new private-actor PEP/influence/PER pages and their actor-register links.

It requires HTTP 200, non-trivial response length and exact content markers, uses cache-busting/retry, and preserves a JSON artifact. The existence of the verifier closes the process-design gap but does **not** itself prove a successful rendered-site response. A future thread must record the successful run/browser read-back when observable; this task is finite and no longer conversation-dependent.