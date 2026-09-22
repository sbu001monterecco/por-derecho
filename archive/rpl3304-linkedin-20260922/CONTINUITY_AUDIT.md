# RPL 3304/2025 — R33 opposition and LinkedIn release continuity audit

Control date: 22 September 2026  
Audit state: `PUBLIC_SAFE_PACKAGE_READY_FOR_PRESERVATION`  
Package ID: `PD-RPL3304-R33-LINKEDIN-20260922`

## 1. Purpose and scope

This package preserves the complete public-safe outcome of the thread concerning:

- the 14 September 2026 opposition signed by Francisco de Borja Rodríguez-Batllori Laffitte in RPL 3304/2025;
- its receipt on 21 September 2026;
- the already-published 22-page source and bilingual forensic reader;
- the final Spanish and English editorial-satire images;
- the final Spanish and English LinkedIn posts;
- the institutional-tagging limits for RSM Spain, Grant Thornton España and PwC España;
- a deterministic reconciliation path for GitLab when ordinary access returns.

This is a continuity and preservation record, not a judicial finding or a new evidentiary conclusion.

## 2. Canonical source and custody boundary

- Source: 22-page opposition by Francisco de Borja Rodríguez-Batllori Laffitte.
- Signed-native source size: 1,687,660 bytes.
- Signed-native SHA-256: `5e0728185cf9b686abd723497d2a53a2656a5e0de4d323a734ed02880eb1d711`.
- Public-safe 22-page derivative SHA-256: `df43ba1d044c59177a85dea18c98f64b0c9c826ec7ba030c332a1e9cfb7abd14`.
- The signed-native source remains separately preserved and is not included here.
- The private v3 forensic package remains outside public Git. Its recorded scale is 206 source blocks, 276 statement-level propositions, 206 paragraph composites and 482 truth-reconstruction records.

The private analytical records are work product, not findings that any person lied, acted intentionally, coordinated unlawfully or committed an offence.

## 3. GitHub lineage and disposition

### Superseded predecessor

PR #1696 is closed and unmerged. Its history may be consulted, but it must not be revived or merged wholesale.

### Canonical publication

- PR #1725 published the source page and public-safe PDF viewer.
  - candidate: `34aec274b9bf161b404da2c0ee1dd3d8a8a28dc9`
  - merge: `fbeff4dbbabcda55152aba8e928ab54ca5faaedb`
  - Pages run: `35664473625`
  - controller fence 38: `VERIFIED_FOR_SCOPE`
- PR #1732 added the split forensic sidecar.
  - candidate: `eca867a95e0c26b718b4999b719d93ef10e9f61b`
  - merge: `96e2e9b1e020ff32779ea35a2c3c7b33cf8c58fd`
  - Pages run: `35667186111`
  - controller run `35667198114`, fence 39: `VERIFIED_FOR_SCOPE`
- PR #1741 added the reciprocal visual-linkage release.
  - merge: `0c2c8a1b6680e61e2c76ea1c96687e07c6672154`
  - Pages run: `35672778473`, successful for that exact SHA
- PR #1743 closed the deployment metadata gap.
  - head: `f36bad327e2521246b63f1a3a057b94d63ca82b9`
  - all nine observed PR workflow runs succeeded
  - merge: `3fb4321536fc803768b02fe05d52d8b0d74f8322`

### Non-controlling open lanes at audit time

- PR #1734 is a stale, conflicting continuity-audit lane based on an older `main`; it is superseded by PR #1743 plus this package.
- PR #1737 is a separate reusable-viewer proposal. It is not part of this LinkedIn release package and must receive its own review before any merge.

## 4. Live readback

At `2026-09-22T01:49:00Z`:

- Spanish reader returned HTTP 200, `text/html; charset=utf-8`, 34,010 bytes.
- English reader returned HTTP 200, `text/html; charset=utf-8`, 21,441 bytes.
- Public PDF returned HTTP 200, `application/pdf`, 1,308,157 bytes.

Canonical URLs:

- Spanish: `https://sbu001monterecco.github.io/por-derecho/es/concurso-36-2012-oposicion-ac-apelacion-lpb-septiembre-2026/`
- English: `https://sbu001monterecco.github.io/por-derecho/en/insolvency-36-2012-ac-opposition-lpb-appeal-september-2026/`
- PDF: `https://sbu001monterecco.github.io/por-derecho/evidence/insolvency-36-2012/concurso-autos/pdfs/R33-ac-oposicion-apelacion-lpb-septiembre-2026.pdf`

## 5. Final visual decision

The canonical images are:

- `rpl3304-editorial-satire-es-20260922.png`
- `rpl3304-editorial-satire-en-20260922.png`

Both are 1,254 × 1,254 RGB PNG files. They use the approved images of Gil Marer and Francisco de Borja Rodríguez-Batllori Laffitte in a new editorial composition. Borja appears on a separate identification card; no actor's face is replaced.

The final images do not contain or reproduce the *Liar Liar* poster, film still, child actor, Jim Carrey image or film title. Those source/reference images are excluded from this package. Earlier formulations such as “mentiroso compulsivo”, “tortuoso” or a categorical claim that a person is incapable of lying are not the canonical title or copy.

The preserved editorial question is narrower: what would remain of the filing if no statement could omit a material part of the truth? The footer expressly labels the image as editorial satire and points to the complete source.

## 6. Final LinkedIn copy and operational state

- Spanish post: `linkedin-post-es-20260922.txt` — 2,869 Unicode characters including the final newline.
- English post: `linkedin-post-en-20260922.txt` — 2,897 Unicode characters including the final newline.
- Both remain within LinkedIn's 3,000-character post field.
- No hashtags are included.
- The selected discovery mechanism is direct `@` tagging of the relevant institutional pages, subject to LinkedIn resolving the actual company pages at publication time.
- The viewer URL remains in the body. `linkedin-first-comment-links.txt` preserves all three direct links for a first comment because an uploaded poster may replace the rich-link preview even though the URL itself remains clickable.
- `image-alt-text.md` preserves bilingual accessibility text.

## 7. Mandatory allegation and attribution limits

The final copy deliberately preserves these boundaries:

1. No court is said to have found that the Insolvency Administrator lied.
2. The image is satire; it is not evidence.
3. The filing is published and should be read in full.
4. The analysis separates claim, source support, omitted context, competing explanation and outstanding proof.
5. Corrections supported by primary sources receive equivalent prominence.
6. Silence is not treated as an admission.
7. RSM is relevant through San Telmo's later integration and possible historical-record custody; RSM is not described as Borja's employer and no inherited liability is alleged.
8. Grant Thornton references must distinguish the exact entity, capacity and dates. No claim is made that Grant Thornton participated in Concurso 36/2012 merely because of a later commercial-services relationship.
9. PwC is framed as a potential historical witness and records custodian concerning 2016 work and later contacts; PwC is not accused here of participating in criminal conduct.
10. The three firms are not treated as a collective defendant or collective wrongdoer.

## 8. Analytical continuity that must survive any migration

Keep separate:

- source statement and commentary;
- allegation and proved fact;
- contradiction or narrowing and intent;
- institutional availability and personal knowledge;
- lawful or contrary explanation and adverse inference;
- native signed source and public-safe derivative;
- RPL 3319's consolidation into RPL 3304 and any merits determination.

High-value proof still open includes the 2018 accounting transmission and attachments; native SWAP correspondence and conditions; ACTÚA, banking and insolvency-ledger reconciliation; exact Grant Thornton legal-entity/capacity reconciliation; and the separate opposition-to-evidence filing.

## 9. Preservation and GitLab recovery

- This directory is the public-safe, GitLab-ready package.
- `release-manifest.json` is the machine-readable inventory.
- `SHA256SUMS.txt` is the byte-integrity control.
- `GITLAB_RECONCILIATION_RUNBOOK.md` is the restore procedure.
- Google Drive holds a second preserved copy under the existing RPL 3304 separation-visuals structure; the private Drive locator is intentionally omitted from public Git.
- GitLab remains `PENDING_ACCESS_RESTORATION`. The existence of a public GitLab website is not proof that its repository is current.

When access returns, reconcile GitHub and GitLab histories; do not force-overwrite an unreviewed GitLab head. The later GitLab receipt must record both pre-reconciliation SHAs, the resulting SHA, pipeline evidence, hashes and live readback.

## 10. Package conclusion

The thread is preserved without importing film artwork, private evidence, privileged material or private locators. The public website source is live; the Spanish and English publication assets are exact and hash-controlled; the GitHub lineage is explicit; and the GitLab recovery procedure is deterministic.
