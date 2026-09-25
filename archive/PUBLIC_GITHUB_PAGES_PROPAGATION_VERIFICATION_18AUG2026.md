# PUBLIC GITHUB PAGES PROPAGATION — POSITIVE VERIFICATION

**Verification date:** 18 August 2026  
**Public host:** `https://sbu001monterecco.github.io/por-derecho/`  
**Required minimum implementation commit:** `6deaba19d8db5c5c5e20f2965ae8ab7deb28d8de`  
**Verification workflow commit:** `9204cba913d55b1c1f2c7f2979da305d6694cc51`  
**Workflow run:** `32127642260`  
**Workflow job:** `95681649132`  
**Commit-status context:** `pages-propagation/optimum-reader-journey`  
**Commit-status result:** `success`  
**Final conclusion:** **VERIFIED — the public GitHub Pages host is serving `6deaba19d8db5c5e20f2965ae8ab7deb28d8de` or a descendant.**

## 1. Why the proof is sufficient

The verification combines two independent propositions:

1. **Git ancestry:** GitHub's compare API confirmed that verification commit `9204cba913d55b1c1f2c7f2979da305d6694cc51` is four commits ahead of the required minimum commit and that the merge-base commit is exactly `6deaba19d8db5c5c5e20f2965ae8ab7deb28d8de`.
2. **Live-host content:** the actual public GitHub Pages host served a unique post-implementation deployment probe together with all implementation-specific optimum-reader-journey assets and the public homepage, with every required marker present.

The unique probe was committed after the required minimum implementation commit. Therefore, a public host serving that probe and those implementation-specific assets is necessarily serving the required minimum implementation or a later descendant containing it.

This is stronger than confirming that source files exist in the repository. It verifies what the public host actually returned.

## 2. Polling result

The live-host verifier completed successfully on **attempt 1 of 72**:

- `deployment_probe=OK`
- `core_asset=OK`
- `finish_asset=OK`
- `loader_asset=OK`
- `public_home=OK`

Workflow output:

> `PUBLIC GITHUB PAGES PROPAGATION VERIFIED: 6deaba19d8db5c5e20f2965ae8ab7deb28d8de OR DESCENDANT`

**Verification timestamp:** `2026-08-18T10:37:16.807622Z`

## 3. Live response manifest

All requests were cache-busted, returned HTTP `200`, were served by `GitHub.com`, and contained no missing required marker.

| Kind | Public path | Required markers | Bytes | SHA-256 |
|---|---|---|---:|---|
| Deployment probe | `deployment-probes/optimum-reader-journey-20260818.json` | `psr-pages-optimum-reader-journey-20260818-v1`; minimum commit SHA | 397 | `5447fd65e75d8588735c33bd6d386b08acd48cfb1dace0679b9ffa316c12dab0` |
| Core reader-journey asset | `assets/optimum-reader-journey-20260818.js` | release ID; `psr-reader-intent`; `psr-next-step` | 28,343 | `207d1a13425c0eb8fad04ba05cdf530e26861894cd237bcb5d4c0d3294643dbe` |
| Finish asset | `assets/optimum-reader-journey-finish-20260818.js` | `simplifyHeaderNavigation`; `psr-hero-shortcuts`; `movePrefaceModulesAfterHero` | 9,213 | `805ac7dbecf9d5cf9f16bef53e50830ff94ba128bc933e2a432a93ab2b7fb7ef` |
| Global loader | `assets/ricpe-filed-status-20260817.js` | both optimum-reader-journey loader filenames | 6,391 | `740dc5f9f29b1c909a613a66f5499e017182c733ce4f052ee3aab9239301a8df` |
| Public Spanish homepage | `es/` | `Project Sun Rock`; `resumen-60-segundos` | 198,362 | `79901f32592f272649a2e38df98de77e5c031d01f9a8caa96cdb9e49a631dccd` |

## 4. Recorded HTTP / cache metadata

The successful live responses recorded:

- `Last-Modified: Tue, 18 Aug 2026 10:35:13 GMT`
- `Cache-Control: max-age=600`
- `Age: 0`
- `Server: GitHub.com`
- `X-Cache: MISS`
- `Via: 1.1 varnish`

The deployment-probe response additionally recorded:

- `ETag: "6a843561-18d"`
- `X-GitHub-Request-Id: DC72:36355D:16C5631:18092EF:6A8435DC`

The other response-specific ETags and request IDs remain preserved in the workflow artifact.

## 5. Evidence artifact

The workflow uploaded the complete machine-readable verification record:

- **Artifact name:** `public-pages-propagation-evidence`
- **Artifact ID:** `9320957696`
- **ZIP size:** `1,562 bytes`
- **Artifact ZIP SHA-256:** `bb4320981fd975e19184d044cd878951c7d33cd6c19b553ba3219d06da6c8b72`
- **Retention:** 30 days

The JSON artifact contains:

- verification basis;
- minimum and workflow commits;
- repository and run identifiers;
- base URL;
- start and verification timestamps;
- attempt number;
- every checked URL;
- required and missing markers;
- status code;
- final URL;
- response headers;
- byte length;
- and response SHA-256.

## 6. Workflow path and permanent verification mechanism

The repository now contains:

- `deployment-probes/optimum-reader-journey-20260818.json`
- `scripts/verify_pages_propagation.py`
- `.github/workflows/verify-pages-propagation-optimum.yml`

The workflow can be manually re-run after future material deployments. It publishes a machine-queryable commit status linked to the exact Actions run.

## 7. Closed operational gate

The prior deployment record said:

> `Independent public Pages propagation check: open but finite.`

That gate is now closed.

**Current controlled status:**

- repository source: verified;
- browser-render acceptance against production subpath: verified;
- public GitHub Pages propagation: verified;
- minimum implementation commit or descendant: verified;
- operational delivery readiness: **100%**.
