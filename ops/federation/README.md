# Por Derecho Federated State Exchange — v1

## Purpose

This is the recursive bridge above the existing Evidence Control Plane and the advisory dual-host topology census.

It does **not** mirror GitHub and GitLab. It exchanges bounded machine-readable state so each host can remain different for legitimate reasons while every material difference is classified, attributable and reviewable.

## Host roles

- **GitLab** remains the private canonical working/recovery authority where current repository controls assign that role.
- **GitHub** remains the public continuity/publication/integration surface where current controls assign that role.
- **ChatGPT** is the supervised orchestration and continuity layer: retrieve live state, compare, classify, coordinate one-writer lanes, preserve the handover, and never substitute memory for repository/source truth.
- **Live public hosts** are deployment/readback authorities only. Green CI is not proof of publication.

No host role silently establishes allegation merits, source truth or legal findings.

## Recursive transaction

Each federation cycle emits a `por-derecho.federation-state-envelope.v1` envelope. A non-genesis envelope must identify and hash its predecessor.

Every cycle re-resolves both current main SHAs; regenerates complete host manifests from checked-out trees rather than API-limited compare responses; revalidates the ruleset; classifies every material difference; traverses dependency/projection edges; preserves contrary, exculpatory and lawful alternatives; integrates only through a collision-checked one-writer lane; verifies exact tested heads; verifies deployment separately by exact live readback; then emits the next envelope or closes only when all terminal conditions are met.

Recursion is bounded to 32 dependency hops with a visited set. Cycles or unresolved dependencies fail closed rather than looping or being silently skipped.

## Supervised intelligence

The federation separates six functions: Retriever, Evidence Analyst, Adversarial Reviewer, Integrator, Projection Reviewer and Release Verifier. The same model or human may perform several sequentially, but receipts must identify the function. Retrieval cannot directly promote truth/legal status; integration cannot override another active writer; release verification cannot change substantive evidence.

## Truth-seeking rules

Source is not assertion; assertion is not legal finding; authentication is not truth; relationship does not transfer knowledge, intent or responsibility; chronology/correlation is not causation; contrary/exculpatory evidence and lawful alternatives remain first-class; no numeric truth score is used; no semantic escalation occurs without source plus review; event time and knowledge time remain distinct; corrections are append-only typed supersession; and an assertion/status change recursively reopens its transitive dependants.

## Frontend projection

Frontend pages are projections, not the source of evidential truth. A future projection compiler should bind EN/ES routes to the same canonical object/assertion IDs and emit route manifests, public-safe provenance panels, correction state and exact release receipts. Pixel identity across hosts is not required; semantic equivalence or explicitly explained divergence is.

## CI integration boundary

This bootstrap deliberately adds no new root GitLab CI job and does not edit the active GitHub topology workflow. GitLab's tested-build configuration is hash-authenticated and GitHub already has an active topology lane. Automatic invocation should be added only through reviewed successor mechanisms after current colliding lanes are clear.

Manual validation command: `python3 scripts/validate_federation_bridge.py`.

## What this does not authorize

No public content change, allegation escalation, merge, deployment, email, filing, social post, access change, branch protection change or canonical-host migration is authorized by this package.
