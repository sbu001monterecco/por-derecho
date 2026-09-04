# Multi-Thread Collaboration & Publication v2

**Control ID:** `PD-MTCP-20260904-01`  
**Effective state:** mandatory when merged to `main`  
**Applies to:** all Por Derecho / Project Sun Rock ChatGPT, ChatGPT Work, Codex and other agent threads, including already-open threads once they refresh current `main`.

## 1. Purpose

The repository remains the durable source of truth, but concurrent agent work is split into two layers:

- **parallel specialist work** may research, digitise, analyse, audit and prepare structured deltas concurrently;
- **publication/integration is serialised** through one active integration lane.

This control reduces stale branches, duplicate handovers, overlapping canonical records, superseding PR chains and post-merge repair loops without weakening any evidence, privacy, identity, preservation or external-authority safeguard.

## 2. Runtime hierarchy

Keep operational truth and collaboration truth separate:

- `ops/CURRENT_STATE.json` remains the repository/deployment/rollback operational-truth contract;
- `ops/CURRENT_COLLABORATION_STATE.json` controls concurrent-thread roles and integration routing.

For related work the runtime order is:

`current remote main -> ops/CURRENT_STATE.json + ops/CURRENT_COLLABORATION_STATE.json -> Issue #1428 Control Tower / Integration Queue -> relevant canonical registers + task issue -> specialist work -> structured delta -> one integration PR -> validation -> merge -> deploy -> live verification`.

Historical handovers and dated state files remain audit/provenance material. They are not competing current-state authorities.

## 3. Roles

### Worker thread — default

Every related thread is a **worker** unless it is expressly operating as the single active integrator.

A worker may inspect sources, use authorised connected sources, analyse, draft canonical changes, identify corrections, propose files/routes, and preserve a structured delta. A worker must not independently create a competing publication lane, merge to `main`, or manufacture a parallel whole-project continuity universe.

### Integrator / Control Tower — single active publication lane

Only one integrator may coordinate publication at a time. Before taking the role it must:

1. fetch current remote `main`;
2. read `ops/CURRENT_STATE.json`, `ops/CURRENT_COLLABORATION_STATE.json` and Issue #1428;
3. inspect open PRs for an already-active integration/publication lane;
4. if another integration lane exists, remain a worker unless the user expressly replaces/transfers the integrator role;
5. if no integration lane exists and publication is authorised, create one current-main-based integration branch/PR and reconcile worker deltas into it.

One logical release should normally produce one integration PR, regardless of how many worker threads contributed.

### Audit/research thread

An audit or research thread is a worker with a narrower output: findings, contradictions, source gaps and proposed canonical deltas. Discovery alone does not create publication authority.

## 4. Existing-thread activation

An already-open thread does not need to restart. On activation it must:

1. discard any assumption that its remembered SHA/branch is current;
2. fetch current `main`;
3. read `AGENTS.md`, `.github/governance/NEW_THREAD_SCOPE_AND_CONTINUITY_GATE_02SEP2026.md`, this control, `ops/CURRENT_STATE.json` and `ops/CURRENT_COLLABORATION_STATE.json`;
4. determine whether it is worker or the active integrator;
5. preserve unique substantive work as a canonical delta;
6. treat its old branch/PR, if any, as a delta source until reconciled against current `main`;
7. avoid independent publication unless it is the active integrator.

### Short wake command

`Por Derecho: wake up. Refresh current main, apply PD-MTCP-20260904-01, work as a worker unless you are the active integrator, preserve only your canonical delta, and do not independently publish.`

## 5. Worker delta contract

A worker completion must be concise and additive. Minimum fields:

- `task` — what was actually investigated or prepared;
- `canonical_ids` — existing IDs affected; create a new ID only through the applicable canonical rule;
- `sources` — source IDs/locators and provenance status;
- `corrections` — exact corrections to current canonical state;
- `new_propositions` — new documented facts, attributed allegations, inferences or status changes with their evidence class;
- `open_gaps` — unresolved proof or finite next-source requirements;
- `proposed_changes` — files, records, routes or edges that should change;
- `conflicts_with_current_main` — none or an explicit collision list;
- `readiness` — `READY_TO_INTEGRATE`, `BLOCKED_SOURCE_GAP`, `RESEARCH_ONLY`, or `SUPERSEDED_BY_MAIN`.

The preferred durable transport is a task issue or Issue #1428. A worker branch may be used when code/file changes are genuinely useful, but that branch is a proposal/delta source, not a publication authority.

## 6. Where information belongs

Do not create a new thread handover merely because a thread is ending.

- proceeding status -> canonical proceedings register;
- person/entity identity -> canonical identity/entity register;
- evidence/provenance -> canonical source/evidence register;
- event/relationship -> canonical event/graph record;
- unresolved work -> GitHub Issue/task register;
- temporary CI/branch/merge state -> GitHub PR/Actions metadata;
- release publication state -> release/PR/verification record;
- exceptional continuity material that cannot fit any canonical object -> smallest justified handover.

Historical handovers remain immutable evidence of prior state; they are not deleted merely because this control reduces future handover creation.

## 7. Pre-control PRs

Every PR opened before this control becomes effective is preserved but defaults to `LEGACY_BACKLOG` for coordination purposes unless current `main` or Issue #1428 expressly reactivates it.

`LEGACY_BACKLOG` means:

- not an active integration lane;
- do not merge wholesale merely because the old PR is mergeable;
- inspect it for unique delta value;
- classify it as `REACTIVATE`, `DELTA_SOURCE`, `SUPERSEDED`, `DRAFT_BACKLOG` or `CLOSE_NO_UNIQUE_DELTA`;
- replay unique still-correct changes onto a fresh current-main integration branch when needed.

No pre-control PR is destroyed or silently treated as merged by this policy.

## 8. Publication transaction

The normal publication path is:

1. resolve current remote `main` immediately before integration;
2. collect all ready worker deltas for the logical release;
3. reconcile canonical IDs and current-main collisions once;
4. generate all deterministic derivative data/pages/indexes on the integration branch **before merge**;
5. run scoped validators plus required repository preservation/publication checks;
6. CI regenerates/checks determinism and fails on drift; CI does not repair `main`;
7. open/maintain one integration PR;
8. merge through normal protected history;
9. deploy;
10. verify the exact merged SHA / affected public surfaces;
11. close/update the contributing task issues and Issue #1428 state.

### No normal post-merge content mutation

New publication workflows must not use a `push-to-main -> generate -> commit/push repair -> second PR` pattern. Post-merge automation should deploy and verify. If deterministic output differs after merge, the release is incomplete and a normal corrective integration PR is required; CI itself does not silently write the correction to `main`.

Existing legacy workflows that still mutate content after merge are migration debt; this rule does not silently rewrite them in an unrelated change, but new work must not replicate that pattern.

## 9. Current-main and collision rule

A worker's old branch is never a truth authority. If `main` advanced, the worker reports a delta against the new state. The integrator performs one semantic reconciliation. Current-main content wins ID/path collisions unless primary evidence and the scoped correction justify a deliberate change.

No force push, broad reset, history rewrite or stale whole-branch merge is permitted to solve concurrency.

## 10. Deletion safety under v2

A specialist thread becomes deletion-safe when its unique material has entered the appropriate canonical register/task issue or has been explicitly classified as non-material/superseded. It no longer needs a bespoke whole-project handover merely to prove deletion safety.

Deletion safety does not require that every open project gap be closed. It requires that no unique material decision, source, correction, limitation or recovery instruction remain solely inside the chat.

## 11. Evidence, privacy and authority boundaries

This is an operational collaboration control only. It does not:

- convert an allegation into a finding;
- merge distinct persons, entities, proceedings, assets, capacities or estates;
- weaken source, contrary-record, privacy, privilege, `^` identity or public/private controls;
- authorise publication when the user has authorised only analysis;
- authorise email, filing, RedSARA/AGE submission, portal action, authority contact, journalist contact, social publication or any other third-party act.

All existing substantive repository governance remains controlling alongside this coordination layer.
