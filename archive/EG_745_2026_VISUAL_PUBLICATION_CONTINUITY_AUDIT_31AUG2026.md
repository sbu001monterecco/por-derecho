# E.G. 745/2026 — visual-publication continuity audit — 31 August 2026

> **Superseding pre-merge addendum:** the seven prepared derivative files whose
> hashes are preserved below were not recoverable. A new deterministic,
> raster-first replacement set has been created from the same hash-verified
> native source and is controlled by
> `EG_745_2026_VISUAL_PUBLICATION_SUPERSEDING_PREMERGE_CONTROL_31AUG2026.md`.
> Its state remains **`PREPARED_PENDING_MERGE`**, not `LIVE`.

## Purpose

This record fixes the exact state of the E.G. 745/2026 digitisation and visual-publication work so that an unfinished binary transfer cannot later be mistaken for a completed public release.

## Controlling native source

- Official attachment: `OFICIO Y DECRETO EXP. 745-26.pdf`
- Three pages.
- Native PDF SHA-256: `1e09c8eb3bce26e28dc5f22e5d6ebad3f458212cf8d85f5920e869fa42554abe`.
- The native source controls over transcription, translation, OCR and all public derivatives.

## Text digitisation — completed

The complete three-page controlled Spanish transcription and complete three-page controlled English convenience translation are preserved in the repository. PR #1193 (`Present full E.G. 745 Decree text inline bilingually`) merged as `5f53e58c28a22f5aab7280c82a31b34fb940f5d1`, making the bilingual response-package pages self-contained for reading the full document text.

This status is separate from visual publication.

## Visual derivative prepared — not yet verified live

A privacy-controlled visual derivative has been prepared from the recovered native source. The recipient email appearing on page 1 is redacted for the public copy; the institutional headings, operative text, official names, stamps/signatures and public institutional contact block remain visible.

Prepared derivative controls:

- Public redacted PDF SHA-256: `07de15f6e1f6ae65d5d42538da6b727e38dc415420b8b803f055a798e584ee23`.
- Public page 1 PNG SHA-256: `68d5236cd3df0d650c891eb9e92787dbe3503564bdd987ad520ce8028c5e45bf`.
- Public page 2 PNG SHA-256: `e3eed7baff8463d4653bcf958ad126c702a1377c5813346a7d42ff5c88d89696`.
- Public page 3 PNG SHA-256: `a47c218e3959a74000278c189c42cb7961848c6b7fc38d17c0b4706cd2557d8f`.

Web-optimised derivatives were also prepared for eventual publication:

- page 1 WebP SHA-256: `c0f484147d6112a974f08088eefdcfeb0e6aac342f673d353006a3080dce7524`.
- page 2 WebP SHA-256: `e54236973869cbb6145a118dfaca51e3ce7f99557473532bb3d3ac1a2dbacdca`.
- page 3 WebP SHA-256: `9a2d4dee2b7d5e85d8a0a9fce84b25a6d3ff1d85112d926613a6170e80e4db99`.

These hashes describe prepared derivatives only. They are not publication proof.
They are also not the hashes of the superseding deterministic replacement set.

## Abandoned transfer branch — do not treat as publication

Branch `eg745-public-visual-20260829` currently points to `75edd03dc86b78954a066923ab4fd63ccf1663db` and is an abandoned transfer attempt. At the 31 August audit it is six commits ahead of its 29 August merge base but approximately 300 commits behind current `main`. Its effective diff contains only two text/base64 transfer files:

- `evidence/fiscalia/2026/eg745-visual-assets/contact-01.b64`
- `evidence/fiscalia/2026/eg745-visual-assets/contact-02.b64`

Those files are not a usable public image/PDF release and must not be cited as proof that the scanned Fiscalía document is live.

## Current publication status

**FULL SPANISH TEXT: LIVE / CONTROLLED.**

**FULL ENGLISH TRANSLATION: LIVE / CONTROLLED.**

**ACTUAL SCANNED VISUAL/PDF: PREPARED, BUT NOT YET VERIFIED AS PUBLISHED LIVE.**

No status may be upgraded to `LIVE` merely because a local derivative exists, a transfer branch exists, or a binary/base64 object was prepared. Visual publication closes only after all of the following are true:

1. the three privacy-controlled page images and/or redacted PDF are committed to a branch based on current `main`;
2. the bilingual E.G. 745 pages link or display those exact assets;
3. the PR is merged;
4. the exact merge SHA receives a successful GitHub Pages deployment; and
5. the public asset URLs are fetched/verified and the derivative hashes are recorded against those paths.

## Current repository checkpoint at this audit

`main`: `fa62a1199bdad4b96eb0bd82516f933409bb2b1c` at the time of this audit. Later repository work must re-read current `main`; this SHA is an audit checkpoint, not a permanent head assertion.

## Resume instruction

Resume from current `main`, not from the abandoned 29 August visual-transfer branch. Preserve the native SHA-256, publish only the privacy-controlled derivative, wire the visual assets into both Spanish and English E.G. 745 pages, merge through a fresh PR, verify exact-SHA Pages success, and only then change the visual-publication status to `LIVE`.
