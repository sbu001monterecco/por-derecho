# MISSION-CRITICAL GITHUB HARDENING — CONTROL RECORD

**Date:** 18 August 2026  
**Repository:** `sbu001monterecco/por-derecho`

## Audit baseline

At the start of this hardening pass:

- `main` was `3ab3e55a86e1340bd574c9ee7988a592d3a90bbd`;
- GitHub Pages was enabled and the repository was public;
- GitHub reported the `main` branch as protected but protection enforcement/status-check enforcement was off;
- the repository already had a universal publication-integrity state machine and validator;
- the strongest permanent public-host record proved `6deaba19d8db5c5c5e20f2965ae8ab7deb28d8de` or a descendant live at `2026-08-18T10:37:16.807622Z`;
- that record did not prove the exact current `main` SHA was live;
- existing workflows used mutable action major-version references;
- live publication verification was primarily manual/specialist rather than a periodic general production monitor;
- there was no repository-wide operational runbook, machine-readable production status file or scheduled full Git bundle.

## Implemented in this hardening change

- immutable full-SHA action references across production workflows;
- current action runtime generations for GitHub-hosted runners;
- explicit workflow timeouts and minimal permissions;
- prohibition on `contents: write` in production workflows;
- mission-critical meta-validator;
- two-hour public production smoke monitor with route-specific markers and incident creation;
- release-specific hardening probe plus post-merge live verification/status;
- weekly verified full Git recovery bundle;
- optional independent `--mirror` backup when `POR_DERECHO_BACKUP_MIRROR_URL` is configured;
- Dependabot for GitHub Actions;
- CODEOWNERS for infrastructure/high-blast-radius paths;
- critical-path register;
- production-status record;
- incident template and recovery runbook.

## Deliberately not changed

The GitHub Pages deployment source/mechanism is not migrated in this pass. A functioning production deployment must not be disabled before a replacement architecture is proven end-to-end.

## Open administrative gates

The repository connector used for this pass does not expose a branch-protection/ruleset mutation. Therefore source hardening does **not** prove that required checks, PR-only changes, force-push protection or CODEOWNERS are enforced by GitHub settings.

An independent backup mirror also remains open until `POR_DERECHO_BACKUP_MIRROR_URL` is configured and a clean restore test is performed.

These are explicit mission-critical gaps; they must not be reported as complete merely because the repository now documents the desired policy.
