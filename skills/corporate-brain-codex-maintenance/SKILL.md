---
name: corporate-brain-codex-maintenance
description: Use for engineering and maintenance of the Corporate Brain repository, ingestion utilities, validators, CI, recovery tooling and private command-centre code.
---

# Corporate Brain Codex Maintenance

Codex is the engineering layer, not the evidential source of truth.

## Standard execution

1. Fetch and identify current remote main.
2. Read repository governance and the relevant specialist skill/control.
3. Work in an isolated branch/worktree.
4. Make the smallest coherent diff.
5. Do not copy private/raw source content into the repository.
6. Run relevant validators/tests.
7. Review deletions, renames, public routes and privacy effects.
8. Refresh current main before PR/merge and reconcile overlap additively.
9. Merge only within the authority granted for the repository scope.
10. Verify post-merge CI/deployment/readback where applicable and record open work.

## Preferred automation targets

- source intake normalization
- hash/revision capture
- duplicate detection
- provenance integrity
- orphan-source/edge detection
- case-graph consistency
- Truth Machine recomputation
- golden-question evaluations
- privacy leakage tests
- backup/restore verification
- private command-centre application
