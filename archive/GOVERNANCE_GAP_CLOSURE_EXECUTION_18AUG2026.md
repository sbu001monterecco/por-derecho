# GOVERNANCE GAP CLOSURE — EXECUTION RECORD

**Date:** 18 August 2026
**Scope:** Issues #355 and #356 identified by the mission-critical hardening / deletion audits.

## Executive result

- **#356 independent disaster recovery: CLOSED** by a verified equivalent off-primary recovery control.
- **#355 main-branch governance: PARTIALLY CLOSED / ADMIN ACTION STILL REQUIRED.** PR-only enforcement is verified, but a live empirical test proved required CI/status-check enforcement is not active on the tested merge path.

## #355 — main branch / ruleset enforcement

### What is objectively enforced

A direct content write to `main` was rejected by GitHub with:

`Repository rule violations found — Changes must be made through a pull request.`

Therefore PR-only changes to `main` are actively enforced.

### Empirical required-check test

PR #365 (`Preserve governance-gap closure evidence`) was created and an immediate merge was attempted before the publication-integrity gate had completed. GitHub allowed the merge and produced merge SHA:

`a6865d67130773b7e1a3ba7cf8e8bb960762a309`

That result proves that, on this tested merge path, **required CI/status-check enforcement is not active**. It is not sufficient that the workflow exists or normally passes; GitHub must prevent merge until the required production check is green.

The legacy branch endpoint additionally continues to show empty legacy required-status contexts. A repository ruleset is evidently active for PR-only enforcement, but the connected GitHub tool cannot read or modify its detailed rules and the runtime has no authenticated `gh` CLI.

### Exact remaining administrative closure

In GitHub repository Settings → Rules / Rulesets for `main`:

1. require the production integrity check before merge (at minimum `Publication integrity gate / publication-integrity`, using the exact current check name shown by GitHub);
2. require branch/current-head freshness if operationally appropriate;
3. prohibit force pushes to `main`;
4. prohibit deletion of `main`;
5. require conversation resolution;
6. preserve PR-only enforcement already observed;
7. re-test by opening a harmless PR and attempting merge before CI completes; the merge must be rejected.

Do not close #355 until that negative merge test passes and the remaining destructive-operation controls are directly observable in GitHub settings or equivalent readback.

**Controlled state: `OPEN_ADMIN_REQUIRED`.**

## #356 — independent recovery

PR #364 strengthened `.github/workflows/repository-backup-bundle.yml` so every full Git bundle is:

- created with all refs;
- verified with `git bundle verify`;
- restored into a clean mirror and worktree;
- checked with `git fsck --full`;
- compared against the source ref inventory;
- checked with `scripts/validate_mission_critical_repo.py`;
- smoke-served as the restored static website;
- uploaded with SHA-256, refs and restore report.

### Verified workflow execution

- source SHA: `a2bda8b3efc71d84241b599112a5bf64077bf3d1`
- workflow: `Repository recovery bundle`
- run: `32149002725`
- job: `95749849770`
- workflow result: `success`
- clean restore / fsck / ref / static-site step: `success`
- artifact ID: `9328943712`
- artifact size: `10,397,758` bytes
- artifact digest: `sha256:8c4a75a61dc6f982c1389328cb9380a1849380074b452c3c2b610b653a3c0c37`
- GitHub artifact expiry: `2026-11-16T14:32:55Z`

### Independent off-GitHub copy

The verified artifact was downloaded via the GitHub connector and uploaded to connected Google Drive.

- Drive file ID: `1vPeTOG5OS4lhVM-UExohcJCPqK4-O-Sm`
- title: `Por Derecho - Independent Recovery Bundle - a2bda8b3 - 2026-08-18.zip`
- MIME: `application/zip`
- Drive readback: PASS

The recovery chain is therefore:

`full-ref Git bundle → cryptographic digest → clean restore → fsck → ref equality → repository validation → restored-site smoke test → off-GitHub Drive copy → Drive readback`.

The independent copy is deliberately not described as a live Git mirror. It is an equivalent recovery control whose recovery capability was actually demonstrated.

### Ongoing control

A recurring Sunday-morning task now refreshes the off-GitHub copy from the latest successful `Repository recovery bundle` artifact and performs Drive readback. It must report the exact failed gate instead of claiming currency when any step fails.

GitHub issue #356 has been closed as completed with the above evidence preserved in its issue history.

**Controlled state: `CLOSED_EQUIVALENT_CONTROL`.**

## Final governance posture

The original two-gap position has been reduced to **one finite GitHub-admin configuration gap**:

- disaster recovery: closed and recurring;
- PR-only main protection: verified;
- required CI merge gate: not enforced and must be enabled in GitHub settings;
- force-push/deletion/conversation-resolution controls: require direct admin readback before #355 closure.

The remaining blocker is administrative, not a missing repository implementation.
