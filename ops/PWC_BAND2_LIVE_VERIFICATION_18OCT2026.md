# PWC BAND 2 — LIVE VERIFICATION

**Control ID:** PD-PWC-BAND2-LIVE-VERIFY-20261018-03  
**Parent visual control:** PD-PWC-BAND2-ECONOMIC-PERIMETER-20261018-02  
**Parent analytical control:** PD-PWC-ECCTA-FRUITS-20261018-01  
**Verification date:** 18 October 2026  
**GitHub state:** DEPLOYED — fresh external content-marker read-back completed; strict LIVE_VERIFIED byte-equivalence capture remains pending  
**GitLab state:** SOURCE_ONLY / NOT LIVE — REQUIRED CI BLOCKER

## GitHub production lineage

- Content publication merge: `13def3171f94924da735f54fb4d99ed3fe123f4b` (PR #2103).
- Live-asset fallback merge: `bcaff6f0345caa59a281ecbae256f444bc9a9b47` (PR #2104).
- PR #2103 and PR #2104 passed the required GitHub publication/release checks before merge.
- PR #2103 gate runs (head `15404b73d498f31d79e02ca1e5c8d71f20110bcc`): Publication integrity `39149742526`; Release acceptance `39149742487`; Visual asset identity registry `39149742545`.
- PR #2104 gate runs (head `e4dad34dca70021af7a8d4b4c762cbbecfcbb146`): Publication integrity `39150335967`; Release acceptance `39150335981`; Visual asset identity registry `39150335900`.

## Public read-back

**External read-back timestamp:** 2026-10-18T17:46:43Z (18:46:43+01:00)  
**Reader:** TinyFish external public fetch, cache bypass requested (`ttl=0`)  
**Technical state rule:** the read-back below proves public content markers and route availability. It does **not** establish byte-for-byte equality of the public response with the controlled source SVGs. Accordingly the strict repository state remains `DEPLOYED`, not `LIVE_VERIFIED`, until an external byte/hash capture is preserved. This is a technical deployment state only and does not verify the merits of any allegation.

Exact URLs read:
- https://sbu001monterecco.github.io/por-derecho/en/pwc-canarias-carlos-saavedra-sun-park/
- https://sbu001monterecco.github.io/por-derecho/es/pwc-canarias-carlos-saavedra-sun-park/
- https://raw.githubusercontent.com/sbu001monterecco/por-derecho/main/assets/graphics/pwc-band2-connected-economic-perimeter-20261018-en.svg
- https://raw.githubusercontent.com/sbu001monterecco/por-derecho/main/assets/graphics/pwc-band2-connected-economic-perimeter-20261018-es.svg

Controlled source hashes:
- EN SVG SHA-256: `9525a21a6e26578368d03bebe10e2d2e246a14a5823bbf16d73909dfad417355`
- ES SVG SHA-256: `0261759568030b519926b30e9ce8f8d569fd152ace87ba72091a01cec2841994`

Fresh external read-back confirmed the following content markers:

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

GitLab MR !843 contains the reciprocal EN/ES source assets, page embeddings, parent/child controls and corrected evidence boundaries. No automated-review outcome is treated as a governance approval or publication state.

GitLab Pages is **not** classified live for this change. The MR remains blocked by the same three required fail-closed CI jobs already failing on GitLab `main` before this PwC update:
- `verify-ricpe-static-readers`
- `verify-gitlab-public-frontend`
- `verify-publication-controls`

The shared failure is the inherited repository-history guard `source-tail repair path/status scope changed`. No bypass was used.

Traceable CI references:
- Baseline GitLab `main` pipeline: `2958946167` (17 October 2026), with required failures `verify-ricpe-static-readers` job `17257949810`, `verify-gitlab-public-frontend` job `17257949809`, and `verify-publication-controls` job `17257949807`.
- Current MR !843 pipeline: `2960612848`, with the same required failures: jobs `17267111579`, `17267111578`, and `17267111576` respectively.

## Email linkage

The active nine-recipient PwC ECCTA draft links:
- the controlling EN GitHub page;
- the reciprocal GitLab permanent page route with its current deployment caveat;
- the EN/ES live GitHub visual sources;
- the EN/ES GitLab MR source files pending Pages deployment;
- official ECCTA section 199 and Home Office guidance.

Older sent communications are not retroactively altered. The parent/visual controls govern future substantive PwC emails and require the relevant live links.
