# E.G. 745/2026 — PR #1280 live successor attestation — 31 August 2026

**Attested release:** PR [#1280](https://github.com/sbu001monterecco/por-derecho/pull/1280), `LIVE_VERIFIED`  
**Filing boundary:** reconsideration `PREPARED / NOT VERIFIED AS FILED`; the private principal remains unsigned and no official filing receipt has been verified  
**This successor at authoring:** `PREPARED_PENDING_MERGE`; it does not attest its own publication

## Exact release identity

- Merge SHA: `b8d3276a65cf8dbb1e92fa905fbcfd3dafbbcd63`.
- First parent: `b3c706a90ea6712ca1c487d9e725cef7b92cc447`.
- Reviewed PR head: `c7956736153f6193c463ec1e53eca111b50388fa`.
- Merge tree: `1e9d668957e8dd370c17aa28608b27fb61fca6da`.
- Scope relative to the first parent: 15 changed files, of which 14 are Pages-visible and one is the workflow source.
- Pre-merge PR census on the final head: 54 workflows — 53 successful and one skipped; zero failures or cancellations.
- The merge retained the disjoint Four Green Houses cover correction already present on `main`; none of the 15 E.G. 745 release paths overlapped that binary.

## Exact-SHA deployment

- Pages run: [33442014678 / #1342](https://github.com/sbu001monterecco/por-derecho/actions/runs/33442014678).
- Head SHA: `b8d3276a65cf8dbb1e92fa905fbcfd3dafbbcd63`.
- Created: `2026-08-31T21:34:11Z`.
- Completed successfully: `2026-08-31T21:37:41Z`.
- E.G. 745 specialist validator: [33442016203](https://github.com/sbu001monterecco/por-derecho/actions/runs/33442016203), successful on the exact merge SHA.

## Independent no-cache live readback

At `2026-08-31T21:43:02Z`, every Pages-visible path changed by PR #1280 was retrieved from the production Pages host with a cache-busting query and `Cache-Control: no-cache`, then compared byte for byte with the exact merge tree. Result: **14/14 identical; zero failures**.

| SHA-256 | Bytes | Pages-visible path |
|---|---:|---|
| `e91e40b1b32c4ed5202a130bbf67c796baca49e8a4bc5821448982a2c7938c65` | 60,704 | `archive/CONTINUOUS_MAINTENANCE_MATRIX.md` |
| `4f8d1645f1ab10d1346ede229c120426935f676dba016ddddb04467889eb27aa` | 3,160 | `archive/EG_745_2026_CURRENT_AUDIT_INTERLINK_CLOSEOUT_31AUG2026.md` |
| `664d35842a0fbae81c407fcd6b717e0f5db09b35ee6b98f7f89cc0a3bf8d8885` | 17,139 | `assets/master-proceedings-publication-20260830.js` |
| `7eeeca03a4cc72843a788ee65147e71851579818d9a8c678a1e0d757d33f24d6` | 4,699 | `assets/site.js` |
| `b5671f3dd304fd5d12664d0fb91cdece132af37364d841c319c429fee8dd5a9f` | 8,118 | `en/master-proceedings-register/index.html` |
| `6fbe5cd4f869f65f89a4cb20e1aa3141af3fb3ec40cdfddb25a5289fd76f8cf9` | 11,226 | `en/public-prosecution-inspection-exp-gub-745-2026/continuity-errors-omissions-31-august-2026.html` |
| `a1a3403bea78bd5d0227db5b38f2ca44ead4ca544221930099f19d82d735f442` | 16,526 | `en/public-prosecution-inspection-exp-gub-745-2026/index.html` |
| `423153b15e2c0ec87890dfaa3ceb4450dd83074af1edbb9653debf5a47fadad8` | 11,649 | `es/fiscalia-inspeccion-exp-gub-745-2026/continuidad-errores-omisiones-31-agosto-2026.html` |
| `6c419099ac915c8bba8c28f3036282d686f925399d66adad588b2ff0c24c428d` | 17,633 | `es/fiscalia-inspeccion-exp-gub-745-2026/index.html` |
| `994e989d15c232fad7a01b028051b09e367c33392e3ec54502d8cc60d120257a` | 8,777 | `es/registro-maestro-procedimientos/index.html` |
| `032d6479b372b6b9670e6a190d8bb64756d664a58302a9d97ea804bd404ed6d6` | 4,896 | `publication-manifests/eg-745-2026-current-audit-interlink-closeout-20260831.json` |
| `6d99b2aeedd32d294750ac302888c36a5365d32dbbf4abe19dada7f9c97678b2` | 16,772 | `scripts/audit_master_proceedings_publication.py` |
| `50cb2d8d26bdae77c0eafb6da068cc96c943953471e14fbe57d2ee7e7a02c0e5` | 10,349 | `sitemap-fiscalia-exp-gub-745.xml` |
| `bb29a1914f3dcd800388e3cb45760e5fbc7123d02da5078230cd10ef3a1f94d2` | 122,887 | `sitemap.xml` |

## Readback-workflow correction

Run [33442016902](https://github.com/sbu001monterecco/por-derecho/actions/runs/33442016902) completed successfully but is **not** relied upon as the 14-file proof above. Its then-current merge-diff command used `git diff-tree` without a merge-parent comparison, so a merge commit could be classified as having zero Pages-visible changed paths and enter the documented no-op branch.

This successor changes that command to an explicit first-parent comparison:

`git diff --name-only <target>^1 <target>`

The no-op path remains only for a commit whose first-parent diff genuinely contains no Pages-visible files. A merge push with public changes must therefore enumerate and compare those files. The independent 14/14 readback above closes PR #1280 itself without relying on the defective no-op result.

## Public and private boundaries

- `NAT-FIS-004` remains the one canonical Master-register proceeding for E.G. 745/2026.
- The reciprocal exact-row dossier links, bilingual continuity corrections, stylesheet repair and sitemap completion are live.
- Cross-linking is navigation and traceability, not joinder or proof of receipt, examination, knowledge, reliance, coordination or merits.
- No private pleading, annex package, native source, private hash, personal data, signature material, covering communication or legal strategy is published by this attestation.
- Public filing status may change only after preservation and verification of an official receipt or equivalent competent proof.

Machine-readable counterpart: `publication-manifests/eg-745-2026-pr1280-live-successor-attestation-20260831.json`.
