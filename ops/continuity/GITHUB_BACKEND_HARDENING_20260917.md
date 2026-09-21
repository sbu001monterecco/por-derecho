# GitHub backend hardening — 17 Sep 2026

**Status:** REVIEW CANDIDATE  
**Base main:** `a283e22255b1e4cb18cc27fe1c6b76cda3ba8389`  
**Branch:** `continuity/github-backend-hardening-20260917`

This tranche strengthens the already-merged outage backend recovery without changing public pages, evidence, identities, proceedings, or substantive allegations.

## Changes

1. Add `scripts/audit_github_backend_capabilities_20260917.py` to verify the reconstructible GitHub backend as a coherent system rather than a loose file set.
2. Add `tests/test_github_backend_hardening_20260917.py` to require 100% presence of the defined repository-hosted capability controls while keeping GitLab-native platform gaps explicit and excluded from that denominator.
3. Update `.github/workflows/outage-backend-parity.yml` so relevant changes on `main`, the outage lane, or this hardening lane trigger the backend parity checks.

## Capability groups monitored

- canonical identity and proceedings registers;
- evidence-intelligence schemas, retrieval pilot, compatibility validation and monitoring;
- Second Pair of Eyes and Case Prism reasoning controls;
- publication controller, publication-integrity gate and off-GitHub preservation workflow;
- agent, Duo-protocol and outage-continuity governance.

## Truth boundary

A passing capability audit means the defined repository-hosted backend controls are present and internally consistent. It does **not** claim recovery of GitLab-native merge-request discussions, Duo sessions, pipeline database state, CI variables, runner/environment configuration, project/group settings or Orbit/index state.

No GitLab-specific file is fabricated from memory. Exact GitLab recovery remains governed by `ops/continuity/GITLAB_EXACT_RECOVERY_QUEUE_20260917.json`.
