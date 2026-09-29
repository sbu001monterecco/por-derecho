# SUN ROCK / AWESWELL — New Phase Deployment Receipt
**Date:** 29 September 2026
**Control ID:** ^AW-SR-NEW-PHASE-DEPLOYMENT-20260929-02
**State:** GitHub production GREEN / GitLab source-parity GREEN + CI AMBER / ChatGPT Work mirror AMBER.

## Deployed public layer
The following public-safe architecture is deployed on GitHub Pages:
- /en/capital/
- /en/capital/media/
- /en/capital/media/how-we-work/
- /es/capital/prensa/
- /es/capital/prensa/como-trabajamos/

English and Spanish pages use language alternates/switches. Public copy preserves PRE-ADMISSION / PRE-ISSUANCE and transaction/planning/financing disclosure boundaries.

## GitHub release proof
PR #2031 passed all 15 visible validation workflows on exact head d6bf4cdc24f3bcfed7ea254238c0af8c942318a4 and merged as:
`1b3e56e4ee7a6c15e73c767305c95aa52a957de3`.

Post-deployment status `pages-propagation/mission-critical-hardening` reported success.

PR #2034 then preserved the legacy 47-route smoke invariant and added a separate bilingual Media/PR live verifier. It passed all nine visible PR workflows and merged as:
`5828b2d0c48289567e2bc27cbb5cad658aa37c1b`.

Main-branch workflow run 36550653045 executed the live verifier and reported:
- sun_rock_capital_en=OK
- sun_rock_media_en=OK
- sun_rock_how_we_work_en=OK
- sun_rock_media_es=OK
- sun_rock_how_we_work_es=OK
- SUN ROCK MEDIA/PR LIVE CHECK: PASS
- PRODUCTION SMOKE CHECK: PASS
- LOCAL CONTINUITY: PASS (68 unique sent-email URLs)
- LIVE CONTINUITY: PASS (68 unique sent-email URLs)

The hardening commit's Pages build/deployment, publication-integrity, CI-control-plane, release-acceptance, identity and private-source governance runs also completed successfully in the checked run set.

## GitLab
MR !704 remains open and unmerged. A direct comparison on 29 September 2026 found these files text-identical to GitHub main:
- en/capital/index.html
- en/capital/media/index.html
- en/capital/media/how-we-work/index.html
- es/capital/prensa/index.html
- es/capital/prensa/como-trabajamos/index.html
- ops/capital/NEW_PHASE_GREEN_CONTROL_MANIFEST_20260929.md

GitLab CI remains AMBER because jobs are rejected before execution with ci_quota_exceeded. This is not represented as a passing pipeline or as a substantive content failure.

## Preservation
Canonical private handoff remains in:
- ChatGPT Library: /Sun Rock/New Phase 2026-09-29
- Google Drive: AWESWELL LIMITED — Sun Rock — Montaña Roja Capital Programme + SRLN-2026 — CANONICAL / New Phase 2026-09-29
- Google Drive backup: Sun Rock Private Capital Backups / New Phase 2026-09-29

## Automation
Sun Rock Daily SWOT is enabled daily at 08:30 Europe/London. It scans Past / Present / Future signals, preserves private snapshots and may only perform low-risk internal actions under the standing controls.

## Remaining blockers
1. GitLab compute quota / real CI execution.
2. ChatGPT Work direct editing capacity for the standalone capital-site mirror.
3. Transaction-specific milestones that are intentionally conditional and must never be described as completed before they are.

No fee, subscription, financing commitment, authority filing or third-party communication is created by this receipt.
