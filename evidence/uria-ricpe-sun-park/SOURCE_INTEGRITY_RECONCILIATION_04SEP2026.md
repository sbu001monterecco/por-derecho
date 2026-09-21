# Uría / RICPE / CaixaBank source-integrity reconciliation — 4 September 2026

Status: **ACTIVE INTEGRITY CONTROL — MULTIPLE BYTE-LEVEL FINGERPRINTS MUST NOT BE CONFLATED**

## Why this record exists

During the 4 September 2026 recovery of the native connected mailbox sources, several binaries were re-read directly from the connected Gmail source and hashed from the recovered bytes. Those hashes do not match some fingerprints inherited from the earlier #1446 manifest. The repository must preserve both provenance records rather than silently replacing one with the other or claiming byte identity that has not been proved.

A different SHA-256 does **not**, by itself, prove different substantive content. PDF/DOCX/JPEG files can differ at byte level because of metadata, re-saving, export, signature, compression or other transformations. Conversely, substantive identity cannot be assumed merely because filenames match. Each binary variant must therefore be separately identified.

## Reconciliation table

| Filename | Current connected-source binary | Size | Legacy #1446 fingerprint | Existing repository cross-check | Current status |
|---|---:|---:|---:|---|---|
| `CONTESTACION.pdf` | `abbaf13c655058635fbd37395ad2e8699c1c91918b6ef75c8a07b90b9b97b73b` | 941,946 bytes | `e9cfcc7f364939bab3c796dde132ccc28e7b42e3b98470436af0e4e56eca9669` | existing `uria-ricpe-caixabank-source-register-20260904.js` already registers `abbaf13c…` for the 47-page public raw defence | **CURRENT CONNECTED ORIGINAL VERIFIED; LEGACY VARIANT NOT YET RE-LOCATED** |
| `CONTROL21_Ampliacion_JDAM_LPAM_AcostaMatos_09JUL2026_FINAL_CONSOLIDADA_PRINT_FILE_FIRMA.docx` | `d13ddbc3c55c0d7f4753b25e0444275ec5bf1b21e0b378fcfd6315550ba78f09` | 62,288 bytes | `6741dcbfb1a2201c7773141bcfad292d101041560e599aac39178ea9530623c9` | existing source-register runtime already registers `d13ddbc3…` for Control 21 | **CURRENT CONNECTED ORIGINAL VERIFIED; LEGACY VARIANT NOT YET RE-LOCATED** |
| `Ampliacion Proc.1901-2026 (CAM et al) 09JUL2026.jpeg` | `dfad6f405b7a2ec047a98a7183a9cbfd0698427d3925d02b2a50b4de76de8f71` | 295,037 bytes | `fb9f9f5b65735fe0f53318d7d122801520b0968dc34a1bac4f6505f20e2ca967` | no independent main-branch binary hash was located for the receipt during this pass | **CURRENT CONNECTED ORIGINAL VERIFIED; LEGACY VARIANT NOT YET RE-LOCATED** |

## Evidential consequence

1. The **current connected-source hashes** above control references to the binaries actually recovered and re-read in this integration pass.
2. The **legacy #1446 fingerprints are retained** as historical/alternate-fingerprint records. They must not be described as the current connected originals unless the matching binary is located and re-hashed.
3. For `CONTESTACION.pdf` and Control 21, the fact that the existing source-register runtime independently contains the current connected-source hashes supports continuity with the repository's current-main evidence architecture.
4. For the 9 July receipt, visual inspection of the current connected binary shows a Decanato stamp dated 9 July 2026 and procedure no. 1901/2026. The prior `fb9f…` binary has not been re-located in this pass, so visual or byte identity between the two receipt variants is **NOT YET ESTABLISHED**.
5. The previously preserved filing-identity limitation remains unchanged: a receipt proves reception/submission, not byte-for-byte identity between the recovered Control 21 DOCX and the exact court-filed packet.

## Required follow-up

- Locate any binary that hashes to each legacy fingerprint and identify its provenance, creation/export date and relationship to the current connected-source binary.
- If both variants are located, compare substantive text/page content as well as metadata; do not use filename equality as a substitute for comparison.
- For the filed Control 21 document, obtain a court-native/certified copy or filing-system-native version/hash to close the filed-byte identity question.
- Keep public source notes explicit about which fingerprint they cite: **current connected source** versus **legacy/alternate variant**.
