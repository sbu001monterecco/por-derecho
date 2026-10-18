# PWC BAND 2 — LIVE VERIFICATION

**Control ID:** PD-PWC-BAND2-LIVE-VERIFY-20261018-03  
**Parent visual control:** PD-PWC-BAND2-ECONOMIC-PERIMETER-20261018-02  
**Parent analytical control:** PD-PWC-ECCTA-FRUITS-20261018-01  
**Verification date:** 18 October 2026  
**GitHub state:** LIVE_VERIFIED  
**GitLab state:** SOURCE_REVIEWED / NOT LIVE — REQUIRED CI BLOCKER

## GitHub production lineage

- Content publication merge: `13def3171f94924da735f54fb4d99ed3fe123f4b` (PR #2103).
- Live-asset fallback merge: `bcaff6f0345caa59a281ecbae256f444bc9a9b47` (PR #2104).
- PR #2103 and PR #2104 passed the required GitHub publication/release checks before merge.

## Public read-back

Fresh external read-back confirmed:

- EN route serves `#pwc-eccta-economic-fruits-20261018`, the Band 2 figure, evidence-bound marker table and ECCTA section 199 boundaries.
- ES route serves the same parent anchor, the `#pwc-band2-economic-perimeter-20261018` alias, localized Band 2 figure, marker table, asset-specific income gap and PwC entity-separation boundary.
- Both page figures point to public `raw.githubusercontent.com` copies of the hash-controlled EN/ES SVGs from GitHub `main`.
- The EN and ES raw SVGs were externally read back with the in-image status line: investigation scope, not established causation; PwC liability not established; section 199 post-1 September 2025 only.

Public routes:
- EN: https://sbu001monterecco.github.io/por-derecho/en/pwc-canarias-carlos-saavedra-sun-park/#pwc-eccta-economic-fruits-20261018
- ES: https://sbu001monterecco.github.io/por-derecho/es/pwc-canarias-carlos-saavedra-sun-park/#pwc-eccta-economic-fruits-20261018
- EN visual source: https://raw.githubusercontent.com/sbu001monterecco/por-derecho/main/assets/graphics/pwc-band2-connected-economic-perimeter-20261018-en.svg
- ES visual source: https://raw.githubusercontent.com/sbu001monterecco/por-derecho/main/assets/graphics/pwc-band2-connected-economic-perimeter-20261018-es.svg

## GitLab state

GitLab MR !843 contains the reciprocal EN/ES source assets, page embeddings, parent/child controls and corrected evidence boundaries. GitLab Duo completed review of the current source and reported no further substantive comments.

GitLab Pages is **not** classified live for this change. The MR remains blocked by the same three required fail-closed CI jobs already failing on GitLab `main` before this PwC update:
- `verify-ricpe-static-readers`
- `verify-gitlab-public-frontend`
- `verify-publication-controls`

The shared failure is the inherited repository-history guard `source-tail repair path/status scope changed`. No bypass was used.

## Email linkage

The active nine-recipient PwC ECCTA draft links:
- the controlling EN GitHub page;
- the reciprocal GitLab permanent page route with its current deployment caveat;
- the EN/ES live GitHub visual sources;
- the EN/ES GitLab MR source files pending Pages deployment;
- official ECCTA section 199 and Home Office guidance.

Older sent communications are not retroactively altered. The parent/visual controls govern future substantive PwC emails and require the relevant live links.
