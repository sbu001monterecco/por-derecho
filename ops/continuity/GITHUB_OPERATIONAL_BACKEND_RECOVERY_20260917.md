# GitHub operational-backend recovery control — 17 Sep 2026

**Status:** ACTIVE OUTAGE CONTINUITY CONTROL  
**GitHub recovery base:** `da67c0c2731c550b0866dad1f679c437f2b612f9`  
**Last independently verified accessible GitLab main:** `7d086d098676eecc2c1647ed09b348d8dc0bdc69`  
**Designated outage write lane:** `continuity/gitlab-block-working-lane-20260917`

## Objective

Keep Por Derecho / Project Sun Rock operational on GitHub while authenticated GitLab access is unavailable, without silently converting the mirror into a new canonical authority and without fabricating GitLab-native state.

The target is **functional continuity first, exact byte parity where independently provable, explicit recovery queues everywhere else**.

## Capability map

### Recovered / operational on GitHub

- canonical matter identity registry and operational identity controls;
- Master Proceedings Register and related interlink/caret controls;
- evidence-intelligence schemas, source classes, records, scripts and monitored RPL 2523 retrieval pilot;
- Second Pair of Eyes, Case Prism and related machine-readable applications/validators;
- publication controller, publication-integrity gates and GitHub Pages deployment/readback machinery;
- repository preservation, thread/deletion continuity and private/public boundary governance;
- GitHub Actions validation estate and off-GitHub-preservation snapshot workflow;
- exact mirrored `ops/duo/DUO_ORCHESTRATION_PROTOCOL_20260917.md`;
- emergency frozen checkpoints and outage working lane;
- GitHub-side agent instructions and advisory public-impact classifier introduced by this recovery package.

### Known freshness gaps

- root identity registry control date: 5 Sep 2026; GitLab continued changing after that date;
- Master Proceedings Register latest GitHub backfill identified in current repository history: 2 Sep 2026;
- GitLab-only or not-yet-mirrored changes from 5–17 Sep must be reconciled when exact source becomes available.

### Platform-native / exact-byte recovery pending

These are not recreated as canonical files from memory:

- `.gitlab/duo/agent-config.yml`;
- `.gitlab/duo/mr-review-instructions.yaml`;
- exact `tests/test_release_bundle_20260914.py`;
- exact implementation state of GitLab MR !529 public-impact shadow classifier (last known passing branch commit `738ab3ddb7d4c7ea91da705cf19045378b8d235f`);
- remaining GitLab MR !528 backend/template/test material not already mirrored publicly;
- GitLab MR discussions, approvals, work items, Duo sessions/reviews, pipeline history/artifacts, variables, runner/environment state, project/group settings and any Orbit/index state.

See `ops/continuity/GITLAB_EXACT_RECOVERY_QUEUE_20260917.json`.

## Outage authority model

1. **Preservation authority:** Git history and frozen continuity refs.
2. **GitHub working authority during outage:** current outage branch plus current GitHub `main` as comparison baseline.
3. **Last-known canonical authority:** GitLab main at the last independently verified accessible state; later exact GitLab state controls once access is restored and reconciled.
4. **Private evidence authority:** authorised private custody systems, never reconstructed from public Git.
5. **Publication authority:** normal reviewed GitHub release/deploy/readback path only for expressly authorised public changes.

## Functional substitutions during outage

### Agent governance

`.github/copilot-instructions.md` maps the existing `AGENTS.md` + Duo orchestration rules into a GitHub-compatible repository instruction surface. It does **not** claim feature parity with GitLab Duo.

### Public-impact shadow classification

`scripts/classify_public_impact_shadow_20260917.py` is a conservative advisory substitute. It defaults to `YES_OR_UNKNOWN` and returns `NO` only for a narrowly bounded non-public-runtime file set. It never weakens CI or publication requirements.

### Release-bundle safety

`tests/test_github_outage_backend_20260917.py` validates this recovery package, the exact frozen anchors and the fail-closed classifier semantics. It is a compatibility test, not an invented copy of the unavailable GitLab `test_release_bundle_20260914.py`.

## Rules during the block

- Do not mass-merge historical GitHub PRs to manufacture apparent parity.
- Do not promote an unverified GitHub candidate merely because the corresponding GitLab state cannot be checked.
- Do not rewrite immutable registry IDs or historical release receipts.
- Do not repin admission hashes to observed values without authenticated successor evidence.
- Do not call GitHub `main` canonical GitLab parity until exact reconciliation proves it.
- Preserve both frozen checkpoint branches.
- New outage work must identify its GitHub base SHA and whether it is GitHub-originated, exact mirrored GitLab material, or functional continuity material.

## Exit condition

The outage control remains active until authenticated GitLab access succeeds and a bounded reconciliation records:

1. exact GitLab current main;
2. GitHub current main;
3. registry/proceedings deltas;
4. exact GitLab-only backend/config files;
5. active MR/work-item/pipeline residuals;
6. platform-native settings that require manual/API export; and
7. the disposition of every GitHub outage-period change.

Only then may this recovery state be downgraded from ACTIVE.
