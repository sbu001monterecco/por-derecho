# GOVERNANCE GAP CLOSURE — EXECUTION RECORD

**Date:** 18 August 2026
**Scope:** Issues #355 and #356 identified by the mission-critical hardening / deletion audits.
**Initial state:** two open governance gaps: (1) GitHub administrative enforcement for `main`; (2) independent off-GitHub disaster recovery plus demonstrated clean restore.

## Closure standard

Do not mark a control closed from intent. Preserve objective evidence.

### #355 — branch/ruleset enforcement

A direct content write to `main` during this execution was rejected by GitHub with `Repository rule violations found — Changes must be made through a pull request.` This is objective evidence that a repository ruleset now enforces PR-only changes on `main`.

The legacy branch-protection endpoint still reports `protected: true` with `protection.enabled: false` and empty legacy required-status contexts. This is compatible with a repository ruleset being the active enforcement mechanism, but the currently available connector cannot read the ruleset-detail endpoint to prove every desired rule (force-push/deletion/conversation-resolution/status contexts). Therefore #355 must not be closed solely from the PR-only rejection. Preserve the observed enforcement and leave only the finite unobservable ruleset details open unless independently verified in GitHub settings.

### #356 — independent recovery

This execution strengthens `.github/workflows/repository-backup-bundle.yml` so each generated full Git bundle is not merely verified with `git bundle verify`, but is also restored into a clean mirror/worktree, checked with `git fsck --full`, compared against the source ref inventory, and smoke-served as the static site. The resulting bundle, ref inventory, hashes and restore report are uploaded as the workflow artifact.

After the workflow succeeds, the artifact is to be downloaded through the GitHub connector and uploaded into connected Google Drive as an off-GitHub recovery copy. That off-primary copy plus the clean restore test is the substantive disaster-recovery control. This is an explicit compensating control for the original optional `git push --mirror` destination; it must not be described as a live mirror.

## Final state rule

- #356 may close only after the strengthened workflow passes, the artifact is downloaded, the artifact is uploaded to Google Drive, and Drive readback confirms the independent copy.
- #355 may close only to the extent objectively evidenced by GitHub. PR-only enforcement is now observed; any remaining unobservable ruleset details must stay explicit rather than being inferred.

This record exists to prevent governance-language inflation: **equivalent recovery can close disaster-recovery risk, but source code cannot impersonate GitHub administrative settings.**
