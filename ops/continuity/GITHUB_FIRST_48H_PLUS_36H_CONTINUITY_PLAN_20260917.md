# GitHub-first continuity horizon — 48h hardening + 36h stabilization

**Status:** ACTIVE CONTINUITY PLAN  
**Control date:** 17 September 2026  
**Baseline GitHub main:** `240441b56818dd0659206d9b054a959d39961bce`  
**Canonical authority:** GitLab project 86151898 remains canonical, but authenticated GitLab is treated as unavailable until there is clear evidence of restoration.  
**Active continuity backend:** GitHub.

## Operating horizon

### Phase A — hours 0–48: GitHub-first hardening

Primary objective: keep GitHub independently strong enough to preserve, validate, reason over and safely release Por Derecho material without fabricating GitLab-native state.

Priority order:

1. keep identity/proceedings registries, evidence-intelligence, Second Pair of Eyes and Case Prism coherent and deterministically validated;
2. strengthen GitHub-native equivalents only where changes are additive, reversible, backend-focused and evidence-safe;
3. keep exact GitLab recovery classes explicit and never reconstruct unavailable bytes from memory, snippets or narration;
4. inspect current-main/open-PR/workflow/preservation state on each continuity run and create work only for material deltas;
5. resolve safety-review queues without weakening publication controls;
6. create or refresh a frozen continuity checkpoint only after a material `main` change;
7. trigger the existing off-GitHub preservation snapshot once per materially new `main` SHA, avoiding duplicate compute.

No merge is authorised unless the relevant exact-head continuity/backend, release-acceptance and publication-integrity gates have passed. Server-side required-check enforcement remains an administrative gap tracked by issue #1525.

### Phase B — hours 48–84: stabilization and reconciliation readiness

Primary objective: reduce churn, close or rebase current-main-safe work, verify preservation state, and prepare a deterministic GitLab reconciliation package.

During this phase:

- prefer extracting verified deltas onto current `main` over merging stale branches wholesale;
- keep unresolved publication/evidence review gates closed rather than weakening them;
- build a GitHub outage-period disposition ledger sufficient to compare every material GitHub change against restored GitLab;
- maintain the same exact-head gate requirements;
- preserve GitHub as a strong operational backend even if GitLab returns;
- switch from outage mode to authenticated reconciliation only after restoration is independently evidenced and then actually verified.

## GitLab restoration watch

Until there is a clear restoration signal, do **not** probe authenticated GitLab. Public web surfaces and already connected sources may be checked.

A restoration signal may include a trustworthy connected-source indication that account access is reinstated, a GitLab account/project response that no longer exhibits the block when accessed through an already-authorised connected source, or equivalent direct evidence. Public anonymous project/page availability alone does not prove authenticated restoration.

When a clear signal exists, perform one bounded authenticated verification. If successful:

1. capture exact current GitLab `main`;
2. export/fetch exact GitLab-native items where authorised;
3. preserve MR discussions/approvals, pipelines, variables, runners, settings and Orbit/index state as platform-native recovery items;
4. compare GitHub outage-period changes additively;
5. never reset or force-push away GitHub continuity work.

## Recovery classification

Every GitLab-related recovery must use exactly one class:

- `EXACT_GITLAB_RECOVERY` — exact bytes/object state recovered from verifiable GitLab provenance;
- `EXACT_ALREADY_MIRRORED` — exact GitLab material already present on GitHub with verifiable identity;
- `FUNCTIONAL_GITHUB_EQUIVALENT` — GitHub substitute providing the required function but not claiming byte/platform parity;
- `PENDING_GITLAB_RESTORATION` — exact GitLab material unavailable or unverifiable.

GitLab-native Duo configuration, MR discussions/approvals, pipelines/jobs, variables, runners/environments, project/group settings and Orbit/index state remain `PENDING_GITLAB_RESTORATION` until exact authenticated recovery.

## Non-negotiable safety rules

- no force-push;
- no history deletion;
- no mass-merge of stale PRs;
- no private-evidence publication;
- no weakening of publication/privacy/release gates to obtain green CI;
- no exact-byte reconstruction from memory or snippets;
- no duplicate off-GitHub preservation run for an already preserved material `main` SHA;
- no claim that GitHub functional continuity equals exact GitLab parity.

## Current blockers/review queues

- #1525 — administrator-only required-status-check enforcement gap;
- #1529 — FTI / Meeting Point discovery fingerprint review, non-inference boundary applies;
- #1530 — AC Community publication opt-in/source-edge review, gate must remain fail-closed unless evidence and publication authority support a change.

These issue references describe current state, not permanent acceptance criteria; close or update them only on material evidence.

## Reporting rule

Each continuity run should report only material state changes: new recovery, new blocker, new or merged exact-head-safe PR, changed `main` SHA, preservation checkpoint change, or a verified GitLab restoration/reconciliation event. If nothing material changes, do not create repository noise.
