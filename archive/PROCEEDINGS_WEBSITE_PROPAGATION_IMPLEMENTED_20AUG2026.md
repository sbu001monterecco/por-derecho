# Proceedings website propagation — implementation record

Date: 20 August 2026
Status: **MERGED TO `main` via PR #662**
Merge commit: `3c1cc2ed878bdef43ba8f62fa406dc57fa8da591`
Public live read-back: **not independently verified at this close-out; retry required**

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

## Remaining implementation evidence

A fresh thread should verify the public GitHub Pages routes and, once confirmed, record that read-back in the appropriate deployment/verification log. Until then, repository publication is controlling and live-browser deployment remains an open verification item.
