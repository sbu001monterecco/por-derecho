# MATKATOR / DP 552/2025 / DP 711/2025 / ETJ 163/2020 — EVIDENCE CUSTODY LEDGER

**Date activated:** 16 August 2026  
**Status:** INTERNAL CUSTODY LEDGER — PUBLIC-SAFE INDEX ONLY — NO PRIVATE BINARIES IN GITHUB  
**Controlling protocol:** `archive/EVIDENCE_CUSTODY_AND_PRESERVATION_PROTOCOL_16AUG2026.md`

## 1. Purpose

This ledger records the custody work actually performed for the ten-source Matkator / DP 552/2025 / DP 711/2025 / ETJ 163/2020 / 2020–2021 masa-activa source set.

It supersedes any earlier wording that the track had only repository/deletion continuity and no implemented custody layer.

The custody architecture actually activated is:

`CURRENT-CONVERSATION UPLOAD BINARY → LOCAL PRESERVATION COPY → SHA-256 → PRIVATE DRIVE VAULT → RAW RE-DOWNLOAD VERIFICATION → LIVE EVIDENCE MANIFEST / CUSTODY EVENT LOG → PORTABLE ZIP SNAPSHOT → SECOND SAME-ACCOUNT BACKUP COPY`

This is materially stronger than repository continuity, but **provider-independent/offline redundancy remains open**. A second object in the same Google account is not treated as independent-provider resilience.

---

## 2. Private-vault location and access boundary

The ten files are preserved in the existing private Google Drive evidence vault under:

`Por Derecho — Private Evidence Vault / 02_MATKATOR_DP552_2025 / ORIGINALS_READ_ONLY`

Custody administration material is under:

`Por Derecho — Private Evidence Vault / 02_MATKATOR_DP552_2025 / ADMIN`

The Drive copies were checked as **not shared** during this custody pass. The public repository deliberately does not contain the private PDFs or direct private-vault URLs.

The project-wide live custody register is:

`Por Derecho Evidence Manifest — live custody register`

The Matkator rows are `MAT-001` through `MAT-010`; the associated custody-event rows begin at `EVT-0017`.

---

## 3. Stable evidence IDs and cryptographic identity

| Evidence ID | Preserved source | Byte size | SHA-256 | Current custody status |
|---|---|---:|---|---|
| `MAT-001` | `DENUNCIA PRESENTADA MATKATOR 20FEB2025.pdf` | 10,661,797 | `2a31f0726e8cc89e35ef33ae6308704ec9e4cd855e8e73e7763bae13de1e34c5` | PRESERVED + HASHED + RAW RE-DOWNLOAD VERIFIED |
| `MAT-002` | `20250223 Ampliacion denuncia.pdf` | 218,059 | `0680bbeeddb2073d8d1ceb9afad0265575123da25128dd2252c15cdcba860755` | PRESERVED + HASHED + RAW RE-DOWNLOAD VERIFIED |
| `MAT-003` | `20250223 Ampliacion denuncia (1).pdf` | 218,381 | `360ab767475898d2d98bce5b52804194c173cbcbb6b91edf5f07370c1f30e73e` | PRESERVED + HASHED + RAW RE-DOWNLOAD VERIFIED |
| `MAT-004` | `250313 escrito adjuntando ampliación de la denuncia fda.pdf` | 136,674 | `e83d4794c9d9c9cd02660926119db80fb2a9fefffe4c4d8566ae567efe74af98` | PRESERVED + HASHED + RAW RE-DOWNLOAD VERIFIED |
| `MAT-005` | `Auto Desestimacion LPB Recurso Auto 24OCT2019 (Art.59LC-DeudaFalsa-Destruccion Masa) 12MAY2020.pdf` | 1,268,422 | `2caa1492433a74c603efedf9662ca1057eda863cadb81474cf05a8b7a5cfbbfa` | PRESERVED + HASHED + RAW RE-DOWNLOAD VERIFIED |
| `MAT-006` | `aweswellestadomasaactiva.pdf` | 149,603 | `8ab76545ff263d4226cff7f363ddab6daea354abde932d1ed63d920bdc9037da` | PRESERVED + HASHED + RAW RE-DOWNLOAD VERIFIED |
| `MAT-007` | `Recurso CAM vs Escrito Aweswell destruccion masa activa 15FEB2021.pdf` | 320,440 | `de45a090b2ffeccb7a7308cd08e1f75c8418fde3617949b2b3774697bde9742b` | PRESERVED + HASHED + RAW RE-DOWNLOAD VERIFIED |
| `MAT-008` | `Auto Destruccion Masa Activa 24FEB2021.pdf` | 539,101 | `3b02a944ae5becb154bdc2109935d060de80bb9e862f10ab055582696e5ee40f` | PRESERVED + HASHED + RAW RE-DOWNLOAD VERIFIED |
| `MAT-009` | `Email GM a AC ref Autorizacion Peritos Informe Masa Activa 8MAR2021.pdf` | 1,821,336 | `e542e8fddcc7f0a78782012c5f07221b9c735cb81b479d6dcac7d77819d02201` | RENDERED PDF PRESERVED + HASHED + RAW RE-DOWNLOAD VERIFIED; NATIVE EMAIL OPEN |
| `MAT-010` | `AutoAcosta MatosInstruccion (2).pdf` | 4,124,982 | `33a24824126d1b358e1d7df3b7b02888f06315151fbae8cb3e0fed21c05a81d3` | PRESERVED + HASHED + RAW RE-DOWNLOAD VERIFIED |

### Hash meaning

These hashes prove binary identity of the preserved Drive copies with the exact binaries staged from the user uploads in this ChatGPT session, because each Drive item was subsequently downloaded raw and re-hashed with an exact match.

They do **not** by themselves prove:

- authorship;
- truth of the content;
- filing authenticity;
- signature validity;
- legal effect;
- provenance before upload into ChatGPT; or
- that a rendered PDF is the native source format where a better native source exists.

---

## 4. Chain-of-custody operations actually performed

For each `MAT-001`–`MAT-010` item the custody pass performed and logged:

1. acquisition from the current-conversation runtime-staged user upload;
2. byte-for-byte preservation copy into a local track vault structure;
3. SHA-256 calculation;
4. local source-versus-preservation-copy hash comparison;
5. upload to the private Drive `ORIGINALS_READ_ONLY` folder without conversion;
6. raw Drive re-download;
7. second SHA-256 calculation on the re-downloaded Drive binary;
8. exact hash and byte-size comparison;
9. entry in the live Evidence Manifest; and
10. entry in the Custody Events log.

Result: **10/10 files passed raw re-download verification.**

No OCR, redaction, translation, annotation, recompression or content transformation was used to create the controlling preservation copies.

---

## 5. Administrative custody records actually created

The private `ADMIN` folder contains track-specific copies of:

- `MATKATOR_DP552_EVIDENCE_MANIFEST_2026-08-16.csv`;
- `MATKATOR_DP552_EVIDENCE_MANIFEST_2026-08-16.json`;
- `MATKATOR_DP552_CUSTODY_EVENTS_2026-08-16.csv`;
- `SHA256SUMS.txt`;
- `ADMIN_SHA256SUMS.txt`;
- `README_CUSTODY.txt`;
- `DRIVE_RAW_REDOWNLOAD_VERIFICATION_2026-08-16.tsv`; and
- the SHA-256 sidecar for the final portable ZIP package.

These administration records describe preservation and verification. They are not substitutes for the evidence binaries themselves.

---

## 6. Portable custody package and redundancy state

A final uncompressed ZIP custody snapshot was created containing the ten preservation masters plus the track manifest/custody/admin records:

`Por_Derecho_MATKATOR_DP552_Evidence_Custody_Package_FINAL_2026-08-16.zip`

**Byte size:** `19,511,402`  
**SHA-256:** `2be120d57d439108548baa16e7978514958ac28dd4cf2da2cc757fd4e529b003`

The final ZIP was:

- uploaded to the private Matkator track folder;
- re-downloaded raw and hash-verified; and
- copied as a second Drive object into `99_INDEPENDENT_BACKUP_EXPORTS`, then raw re-downloaded and hash-verified again.

The backup object is private/not shared. However, both copies remain in the **same Google account/provider**. Therefore the current state is:

- thread-loss resilience: **YES**;
- loss of one individual Drive object: **YES**;
- corruption/change detection for the preserved binaries: **YES, through SHA-256 and re-download verification**;
- recovery from loss of the whole Google account/provider: **NOT YET**;
- independently preserved native RFC822 source for `MAT-009`: **NOT YET**.

---

## 7. Provider-independent backup attempt and boundary

A Microsoft SharePoint/OneDrive connector route was tested during the custody pass to obtain an independent-provider copy. The connected Microsoft account exposed an MSA limitation (`MicrosoftSearch` unsupported), and no reliable independent upload target could be established through the available connector.

**No Microsoft/OneDrive copy was created.**

Do not describe the same-account Drive backup as “independent”, “off-site”, “provider-independent” or sufficient against total Google-account loss.

### Remaining last-mile custody action

Copy the final ZIP to at least one genuinely independent location, preferably:

- an encrypted offline drive held separately; or
- a separate cloud provider/account with independent credentials and recovery path.

After copying, re-calculate SHA-256 and require an exact match with:

`2be120d57d439108548baa16e7978514958ac28dd4cf2da2cc757fd4e529b003`

Record that event in the live custody register. Only then may this track be described as provider-independent/account-loss resilient.

---

## 8. Native-source gap: MAT-009

`MAT-009` preserves the rendered PDF currently available for the 23-Feb / 8-Mar-2021 expert-access correspondence. Its PDF binary is fully preserved and verified under this ledger.

It is **not** a native RFC822 `.eml` export. The native-email custody task remains:

- export the original message(s) with full headers;
- preserve attachments separately where present;
- hash the native message binaries;
- link them as new evidence items rather than replacing `MAT-009`; and
- preserve the complete response/outcome chain.

This is an authentication/source-completion gap, not a defect in the integrity of the preserved PDF copy.

---

## 9. Relationship to the source digest

Read this custody ledger with:

- `archive/MATKATOR_DP552_ETJ163_MASA_ACTIVA_SOURCE_DIGEST_16AUG2026.md`;
- `archive/MATKATOR_DP552_DP711_PROCEDURAL_CONTINUITY_ADDENDUM_16AUG2026.md`;
- `archive/CORRECTION_REGISTER.md`;
- `archive/MISSING_EVIDENCE_REGISTER.md`; and
- `archive/EVIDENCE_CUSTODY_AND_PRESERVATION_PROTOCOL_16AUG2026.md`.

The source digest controls **what each document establishes and does not establish**. This ledger controls **what custody operations have actually occurred**.

Do not let a successful hash verification upgrade a PARTY ALLEGATION into a VERIFIED FACT about underlying conduct.

---

## 10. Fresh-thread custody instruction

A fresh ChatGPT thread dealing with custody, authenticity, production, disclosure, filing or long-term preservation of this Matkator source family should:

1. read this ledger first after the general custody protocol;
2. query the private Drive vault and live Evidence Manifest rather than relying on chat history;
3. use `MAT-001`–`MAT-010` as stable custody IDs;
4. verify hashes before any evidential production where practical;
5. create derivatives separately and link them to the parent evidence ID;
6. never overwrite a preservation master;
7. preserve the `MAT-009` native-email gap;
8. preserve the provider-independent backup gap until an actual second-provider/offline copy is made; and
9. log every later export, redaction, transcription, filing, disclosure or re-verification event.

## 11. Current custody conclusion

As of 16 August 2026, the ten-document Matkator set is **cryptographically manifested, privately vaulted and recoverability-tested at the individual-file and same-account snapshot level**.

It is not yet accurate to call it fully provider-independent or whole-account-loss resilient. The final outstanding resilience step is an independently controlled second-provider/offline copy of the final ZIP, verified against the recorded ZIP SHA-256, plus native RFC822 preservation for the correspondence represented by `MAT-009` when available.