# GOVERNANCE GAP CLOSURE — EXECUTION RECORD

**Date:** 18 August 2026
**Scope:** Issues #355 and #356 identified by the mission-critical hardening / deletion audits.
**Initial state:** two open governance gaps: (1) GitHub administrative enforcement for `main`; (2) independent off-GitHub disaster recovery plus demonstrated clean restore.

## Closure standard

Do not mark a control closed from intent. Preserve objective evidence.

## #355 — branch/ruleset enforcement

A direct content write to `main` during this execution was rejected by GitHub with:

`Repository rule violations found — Changes must be made through a pull request.`

This is objective evidence that a repository ruleset now enforces PR-only changes on `main`.

The legacy branch-protection endpoint still reports `protected: true` with `protection.enabled: false` and empty legacy required-status contexts. This is compatible with a repository ruleset being the active enforcement mechanism, but the currently available connector cannot read the repository-ruleset detail endpoint to prove every desired rule such as force-push/deletion prohibition, conversation resolution or the precise required check set.

A final closure PR is also used as an empirical status-check test: an attempted merge before the publication-integrity gate finishes must be rejected if required-check enforcement is active. The exact result should be preserved before final closure.

**Controlled state:** PR-only enforcement VERIFIED; remaining ruleset sub-controls require direct GitHub-admin readback or equivalent objective evidence. Do not infer them from source code.

## #356 — independent recovery

PR #364 strengthened `.github/workflows/repository-backup-bundle.yml` so every full Git bundle is:

- created with all refs;
- verified with `git bundle verify`;
- restored into a clean mirror and worktree;
- checked with `git fsck --full`;
- compared against the source ref inventory;
- checked with `scripts/validate_mission_critical_repo.py`;
- smoke-served as the restored static website;
- uploaded together with SHA-256, refs and restore report.

### Verified workflow execution

- merge/source SHA: `a2bda8b3efc71d84241b599112a5bf64077bf3d1`
- workflow: `Repository recovery bundle`
- workflow run: `32149002725`
- job: `95749849770`
- result: `success`
- clean restore / fsck / ref / static-site step: `success`
- artifact ID: `9328943712`
- artifact name: `por-derecho-repository-recovery-bundle`
- artifact size: `10,397,758` bytes
- artifact digest: `sha256:8c4a75a61dc6f982c1389328cb9380a1849380074b452c3c2b610b653a3c0c37`
- GitHub retention expiry: `2026-11-16T14:32:55Z`

### Independent off-GitHub copy

The verified artifact was downloaded through the GitHub connector and uploaded into the connected Google Drive.

- Drive file ID: `1vPeTOG5OS4lhVM-UExohcJCPqK4-O-Sm`
- Drive title: `Por Derecho - Independent Recovery Bundle - a2bda8b3 - 2026-08-18.zip`
- MIME type: `application/zip`
- Drive readback: PASS

This is an independent off-GitHub recovery copy. It is a full-ref Git recovery bundle with demonstrated clean restoration. It is **not** described as a live `git push --mirror` endpoint.

### Recovery-control conclusion

The substantive disaster-recovery risk is closed by an equivalent control:

`full-ref Git bundle → cryptographic digest → clean restore → fsck → ref equality → site validation → off-GitHub Drive copy → Drive readback`.

The optional live-mirror secret remains unconfigured, but is no longer required to claim that an independent recoverable copy exists. A recurring off-GitHub copy task should keep this control current after future weekly bundle runs.

**Controlled state for #356: CLOSED BY VERIFIED EQUIVALENT OFF-PRIMARY RECOVERY CONTROL.**

## Final state rule

- #356 may be closed as completed.
- #355 may close only to the extent objectively evidenced by GitHub. PR-only enforcement is verified; remaining unobservable ruleset details must stay explicit rather than being inferred.

This record exists to prevent governance-language inflation: **equivalent recovery can close disaster-recovery risk, but source code cannot impersonate GitHub administrative settings.**
