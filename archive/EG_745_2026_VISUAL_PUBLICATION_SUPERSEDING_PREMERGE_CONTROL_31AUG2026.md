# E.G. 745/2026 — superseding visual-publication pre-merge control — 31 August 2026

## Status

**`PREPARED_PENDING_MERGE` — NOT YET VERIFIED LIVE.**

This control supersedes the unavailable prepared-derivative hashes recorded in
`EG_745_2026_VISUAL_PUBLICATION_CONTINUITY_AUDIT_31AUG2026.md`. None of those
seven earlier derivative files was recoverable from the current workspace. They
remain an audit record; they are not reused or represented as publication proof.

The replacement set below was rebuilt deterministically from the exact native
source on a clean branch based on current `main` at
`4df51da33391c41869470ed539ad31fc4157fbfd`.

## Native source boundary

- Official attachment: `OFICIO Y DECRETO EXP. 745-26.pdf`.
- Pages: 3.
- Native bytes: 1,111,997.
- Native SHA-256:
  `1e09c8eb3bce26e28dc5f22e5d6ebad3f458212cf8d85f5920e869fa42554abe`.
- The native, unredacted source is private and is not committed or linked from a
  public route.
- The native source controls over every public derivative, transcription and
  convenience translation.

## Deterministic privacy control

`scripts/build_eg745_public_visual.py` accepts only the controlling native
SHA-256. It extracts the three embedded 1654 × 2338 scans, replaces only the
page-1 recipient-personal-email pixels with an opaque rectangle, and creates:

- a Pillow-inclusive redaction rectangle `x=232..625, y=474..535`
  (equivalent half-open pixel box `[232, 474, 626, 536)`), verified as the
  complete changed-pixel bounding box;

- full-resolution PNG page derivatives;
- 1240-pixel-wide WebP reader previews; and
- a new three-page A4 PDF composed only from the already-redacted raster pages.

The public PDF has no OCR/text layer, form, annotation or removable redaction
overlay. The institutional headings, operative text, official names,
stamps/signatures and public institutional contact block remain visible.

## Replacement derivative hashes

| Public derivative | Bytes | SHA-256 |
|---|---:|---|
| `oficio-decreto-eg-745-2026-public-redacted.pdf` | 1,956,595 | `a59007fa5db61d2b48b587c208f9cafedabe967e88dac4df223b2ef384595088` |
| `page-1-public-redacted.png` | 2,101,003 | `049ec3fd208f3ff9955ebf8fcfd851ac88f9a62320a6cfa164268605c850b38d` |
| `page-2-public.png` | 3,631,113 | `d3f28f59c7f000d57505f747ff870636d66f307fe57ea3aa9683091bcc2a3ca2` |
| `page-3-public.png` | 1,826,249 | `36f2b0e344abfe9dd9b7c6b46b4228ab4323ded7787a0170ee6d3e9f069be11a` |
| `page-1-public-redacted.webp` | 171,420 | `ac5ccc51d85d6bfc7933a924465c5ef493206453e822fce2b367433975dee41a` |
| `page-2-public.webp` | 353,186 | `5173cd8420ed9f6b6e1b26f3ad86025d89c82cbc69d4936b0d287f17717ae06a` |
| `page-3-public.webp` | 180,032 | `ae3f518bb5732396e5d19fdcd3ee45450d2ee104e9bf7f7594af3493115bfaa8` |

Machine-readable hashes are preserved at
`evidence/fiscalia/2026/eg745-visual-assets/eg745-public-visual-sha256.json`.

## Inherited viewer/hash correction

The earlier Base64 viewer remains preserved in Git history, but its current page
3 chunks reconstruct SHA-256
`b73a712a27c737dd8e22bf462c6e1cce095d05f8d12a3b93b1d0c763f84b528b`,
not the previously displayed `62271b...` value. The new bilingual viewers do not
use any Base64 chunk and instead reference the replacement WebP/PNG files
directly. This correction concerns derivative integrity only; it does not alter
the native source or the controlled transcription.

## Routes prepared

- ES:
  `/es/fiscalia-inspeccion-exp-gub-745-2026/facsimil-visual-31-agosto-2026.html`
- EN:
  `/en/public-prosecution-inspection-exp-gub-745-2026/visual-facsimile-31-august-2026.html`
- Assets:
  `/evidence/fiscalia/2026/eg745-visual-assets/`

## Closure gate

Do not upgrade this replacement visual set to `LIVE` until all of the following
are recorded:

1. reviewed PR head and tree;
2. merge SHA on `main`;
3. successful GitHub Pages deployment for that exact merge SHA;
4. no-cache HTTP 200 retrieval of both bilingual viewers, the redacted PDF and
   all six page derivatives; and
5. byte-identical public SHA-256 readback for every derivative.

## Evidential and filing boundary

Publication of the scanned derivative does not prove that a reconsideration was
filed, does not alter any filing status, and does not establish coordination,
obstruction, prevarication, capture, criminality or personal liability. Adverse
outcomes, silence, routing gaps and repeated institutional contact require the
additional proposition-specific evidence applicable to each such conclusion.
