# E.G. 745/2026 — unitary-register deployment attestation — 31 August 2026

**Attestation ID:** `PD-SP-MF-UNITARY-DEPLOYMENT-ATTESTATION-20260831-01`

**Target release:** [PR #1272](https://github.com/sbu001monterecco/por-derecho/pull/1272), `Close Ministerio Fiscal publication controls`

**Attestation-artifact state:** `PREPARED_PENDING_MERGE`

**Target-release state:** `DEPLOYED_EXACT_BYTES_VERIFIED_CONTROL_REMEDIATION_PENDING`

**Filing status:** `PREPARED / NOT FILED` — unchanged by repository or website publication

## 1. Immutable target identity

| Control | Observed value |
|---|---|
| Pull request | [#1272](https://github.com/sbu001monterecco/por-derecho/pull/1272) |
| Base immediately before merge | `43359d4d77e895dea76b5373b09a70c844b428f2` |
| Final reviewed head | `1fe33abad4ca0f3647d33447988f40a2ef25855d` |
| Final reviewed tree | `92e55d81d3d15b89871513b22584c96253462163` |
| Merge method | squash |
| Merge SHA | `4df51da33391c41869470ed539ad31fc4157fbfd` |
| Merge tree | `92e55d81d3d15b89871513b22584c96253462163` |
| Reviewed-tree / merge-tree parity | **MATCH** |
| GitHub `merged_at` | `2026-08-31T14:33:53Z` |

The merge has one parent, the recorded base SHA. The final PR-head tree and merge tree are byte-identical. This proves that the merged target is the reviewed 28-file tree; it does not prove that this later attestation file was part of PR #1272.

## 2. Workflow census

### Final PR-head checks

The pagination-complete exact-head query for `1fe33abad4ca0f3647d33447988f40a2ef25855d` returned **43** workflow runs: **42 success**, **one intentional PR-event skip**, zero failures, zero cancellations and zero pending. The last run update was `2026-08-31T14:31:58Z`.

The skip was [`Verify unitary criminal publication live` run 33402472361 / #359](https://github.com/sbu001monterecco/por-derecho/actions/runs/33402472361). Its `live` job is expressly guarded by `if: github.event_name != 'pull_request'`; the same workflow ran successfully after the merge on the `push` event.

### First exact merge-SHA census

The pagination-complete exact-head query for merge SHA `4df51da33391c41869470ed539ad31fc4157fbfd` returned **53** workflow runs: **47 success**, **six failure**, zero skips, zero cancellations and zero pending. This comprises 52 `push` runs and the successful dynamic Pages run.

The six failures were identified as deterministic stale-verifier failures. They do not contradict the exact 24/24 byte readback below, but they mean that the first merge-SHA workflow surface was **not all green**. Each remains an explicit control-remediation item:

| Workflow | Run | First-push result | Control state |
|---|---|---|---|
| Verify AC Community de facto administration live | [33403373932 / #129](https://github.com/sbu001monterecco/por-derecho/actions/runs/33403373932) | failure | deterministic stale verifier; remediation pending |
| Verify criminal-engineering and case information architecture live | [33403374093 / #91](https://github.com/sbu001monterecco/por-derecho/actions/runs/33403374093) | failure | deterministic stale verifier; remediation pending |
| Verify PR 830 CAM non-dilution live | [33403374183 / #168](https://github.com/sbu001monterecco/por-derecho/actions/runs/33403374183) | failure | deterministic stale verifier; remediation pending |
| Verify elEconomista Acosta Matos dossier live | [33403374018 / #46](https://github.com/sbu001monterecco/por-derecho/actions/runs/33403374018) | failure | deterministic stale verifier; remediation pending |
| Verify 2022 adjudication reconstruction live | [33403373948 / #71](https://github.com/sbu001monterecco/por-derecho/actions/runs/33403373948) | failure | deterministic stale verifier; remediation pending |
| Verify public Pages propagation — Playa Blanca hotel concept | [33403374083 / #50](https://github.com/sbu001monterecco/por-derecho/actions/runs/33403374083) | failure | deterministic stale verifier; remediation pending |

No later corrective PR, rerun or all-green result is projected into this record. Those facts belong in their own exact-SHA controls when they exist.

## 3. Exact-SHA Pages deployment

- Workflow: `pages build and deployment`.
- Run: [33403372033 / #1335](https://github.com/sbu001monterecco/por-derecho/actions/runs/33403372033).
- Workflow path: `dynamic/pages/pages-build-deployment`.
- Exact `head_sha`: `4df51da33391c41869470ed539ad31fc4157fbfd`.
- Event: `dynamic`.
- Status: `completed`.
- Conclusion: `success`.
- Created: `2026-08-31T14:33:55Z`.
- Updated: `2026-08-31T14:37:34Z`.

This is exact-merge-SHA deployment proof for PR #1272.

## 4. No-cache exact-byte readback

At `2026-08-31T14:56:20Z`, every one of the **24 Pages-visible changed files** was fetched from `https://sbu001monterecco.github.io/por-derecho/` with the exact merge SHA as a cache-busting query and with `Cache-Control: no-cache` and `Pragma: no-cache`.

Result: **24/24 HTTP 200 and byte-identical; zero mismatches or errors**. The path-by-path byte counts and SHA-256 digests are fixed in the companion machine-readable manifest.

The four changed `.github/workflows/` files are not treated as website routes. Their exact Git blobs, byte counts and SHA-256 digests were checked in the reviewed and merged tree. Together, the exact tree and 24-file Pages readback cover all 28 PR #1272 paths without pretending that `.github/` is a Pages route.

## 5. Substantive closeout preserved

The exact deployed target contains the controlled corrections recorded by PR #1272, including:

- the current CAEPR scope of **20 confirmed and four pending out of 24**, with Clubotel La Dorada and the distinct ONA identity kept separate;
- truthful inherited loader-contract markers without double-loading;
- FTI's canonical **43/101** professional scope and the repository-wide **20/24** scope;
- bounded ACTA retry only for transient live HTTPS 502/503/504 responses;
- current mission-critical reader headings and byte floors;
- the institutional-communications workflow coverage correction; and
- the final 31-August Gmail overlap checkpoint.

This attestation does not close the six stale-verifier remediation items or any source/evidential gap preserved in the predecessor closeout.

## 6. Filing, privacy and attribution boundary

The final pagination-complete Gmail/REG-AGE refresh added zero in-scope institutional events and located no new filing proof. E.G. 745/2026 therefore remains **PREPARED / NOT FILED**. No email was sent and no filing was made through this repository work. A Git commit, PR, Pages deployment, public URL, email draft or email copy is not an official filing receipt.

This record publishes no mailbox-provider identifier, exact private subject, private message body, email address, private storage locator or native custody resolver. Private source custody remains outside Git.

## 7. Non-inference rule

The release does not prove coordination, obstruction, capture, favouritism, prevarication, criminality or deliberate protection. Adverse outcomes, silence, routing gaps, repeated institutional contact and functional benefit require additional actor-specific primary evidence before any such proposition can be advanced as fact.

## 8. Self-reference and continuity boundary

This successor attests the already completed PR #1272 target release. It does not claim that the later PR carrying this attestation was itself merged or deployed. Its publication lifecycle therefore remains `PREPARED_PENDING_MERGE`; the separately qualified target-release state records the evidenced PR #1272 result and the six open verifier remediations.

Future work starts from then-current `main`, this immutable successor, the predecessor closeout, the institutional-communications reconciliation runbook, the scan checkpoint and the private custody resolver. Do not rewrite this record with later filing, mailbox, corrective-PR or rerun facts; append a new dated successor supported by primary evidence.
