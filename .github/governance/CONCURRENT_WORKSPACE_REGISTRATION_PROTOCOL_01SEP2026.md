# Concurrent workspace registration and collision protocol — 1 September 2026

**Control ID:** `PD-CWR-001`  
**Status:** active repository-wide continuity control  
**Purpose:** prevent two simultaneous ChatGPT/agent workspaces from silently claiming the same `PD-WS-*` identity or overwriting one another's continuation pointer.

## 1. Why this control exists

On 1 September 2026, two independently active branches both allocated `PD-WS-20260901-0002` after starting from the same earlier repository state. One represented authority-discovery / Red SARA work. The other represented implementation of the automatic workspace-persistence runtime.

The collision was discovered because both branches changed:

- `data/workspace-register-v1.json`; and
- `CURRENT_WORKSPACE_HANDOFF.md`.

The repository correctly refused a clean merge. No state was silently lost. Current `main` already contained the authority-discovery workspace, so that identity remained canonical and the later unmerged persistence-runtime workspace was renumbered to `PD-WS-20260901-0003`.

This is a governance finding: **a sequential identifier allocated on a branch is provisional until reconciled with current `main`.**

## 2. Canonical rule

Current `main` is the allocation authority for public `PD-WS-*` identities.

Before opening or merging a workspace-registration PR, the branch must:

1. fetch/re-read current `data/workspace-register-v1.json`;
2. confirm that its proposed `workspace_id` is not already assigned to another substantive scope;
3. confirm that its handoff ID/path is unique;
4. preserve every pre-existing workspace row;
5. renumber the unmerged workspace if a collision exists; and
6. update any private-vault alias, event IDs, handoff, artifacts and hashes affected by renumbering.

**Current main wins.** An unmerged branch never overwrites or redefines a workspace identity already present on current `main`.

## 3. Root pointer is an index, not a mutex

`CURRENT_WORKSPACE_HANDOFF.md` must no longer be interpreted as proving that only one substantive workspace exists.

It has three functions:

- identify the most recently checkpointed/default workspace;
- list other active or recently preserved workspaces with their exact handoff paths; and
- tell a successor thread to select by explicit `PD-WS-*` ID or substantive topic.

Updating the default pointer must not delete or obscure other workspace entries. The machine authority remains `data/workspace-register-v1.json`.

Where the user's new instruction clearly identifies a topic or workspace ID, that instruction controls selection even if another workspace is listed as the most recently checkpointed default.

## 4. Allocation states

A workspace identity may have one of the following states:

- `LOCAL_PROVISIONAL` — allocated only inside a local/private vault;
- `BRANCH_PROVISIONAL` — present on an unmerged public-repository branch;
- `MAIN_REGISTERED` — unique row merged into current `main`;
- `COLLISION_RENUMBER_REQUIRED` — another substantive workspace already owns the proposed ID on current `main`;
- `SUPERSEDED_ALIAS` — a provisional identifier retained only as a cross-reference after correction.

Do not call a branch-provisional ID canonical.

## 5. Required collision response

If a collision is found:

1. stop the merge;
2. determine which identity is already registered on current `main`;
3. allocate the next free identifier from current `main` to the unmerged workspace;
4. preserve the former provisional ID only in a private or source-safe collision event;
5. rename/rebuild any private workspace directory or cloud alias;
6. regenerate hash-chained events rather than editing old event hashes in place;
7. replace any seed/archive whose internal paths still use the collided ID;
8. update Markdown/JSON handoffs, workspace register and root index;
9. rerun tests and repository gates; and
10. close or supersede the stale/conflicted PR with a fresh current-main PR.

No raw private locator needs to be published merely to explain the correction.

## 6. Future collision resistance

The immediate sequential format remains:

`PD-WS-YYYYMMDD-NNNN`

For stronger automation, a future request-path workbench should allocate both:

- a human-readable `workspace_id`; and
- a collision-resistant immutable `workspace_uid` (UUID/ULID or equivalent).

The public register may later require `workspace_uid`. Until then, merge-time reconciliation and uniqueness validation are mandatory.

A future private allocator may also reserve IDs through a single authoritative service, private GitHub repository, transactional database or append-only object-store manifest. Branch-local “next number” calculation alone is never a uniqueness guarantee.

## 7. Private-vault rule

When renumbering a workspace whose private vault already exists:

- the cloud/local folder alias must be corrected;
- a corrected seed/state snapshot must replace or expressly supersede the old one;
- the exact private locator remains private;
- the public handoff records only the alias, permission state, seed filename/hash and correction state; and
- no raw transcript or connected-source material is moved into public Git as part of the correction.

## 8. Validation requirements

The workspace-persistence repository audit must fail on:

- duplicate `workspace_id` values;
- missing handoff paths;
- a root default pointer absent from the register;
- private-vault material inside the public repository; or
- a continuation pointer that silently removes known active workspace records.

PR freshness and merge-conflict gates remain part of the safety system. A stale-branch failure is not noise to bypass; it is a prompt to reconcile.

## 9. Relationship to other controls

This protocol supplements:

- `PD-AWP-001` — continuous workspace persistence;
- `PD-WCH-001` — workspace/thread handoff and deletion safety;
- `data/workspace-register-v1.json` — canonical public workspace identities;
- `CURRENT_WORKSPACE_HANDOFF.md` — human continuation index; and
- the private event chain produced by `scripts/workspace_persistence.py`.

## 10. Current reconciliation

Canonical assignments after reconciliation:

- `PD-WS-20260901-0001` — Acosta Matos / Canarian Hospitality hotel-platform digital-media work;
- `PD-WS-20260901-0002` — authority discovery, Red SARA/AGE filings and institutional-response continuity; and
- `PD-WS-20260901-0003` — automatic workspace-persistence runtime and private-vault implementation.

The transient branch-only use of `PD-WS-20260901-0002` for the persistence runtime is not canonical and must not be used by successor threads.
