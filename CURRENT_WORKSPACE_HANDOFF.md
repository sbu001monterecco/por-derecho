# Active workspace continuity index

**Current workspace:** `PD-WS-20260901-0003`  
**Current continuation pointer:** `PD-WCH-20260901-AWP-RUNTIME-001`  
**Status:** `DELETION_SAFE_WITH_OPEN_WORK`  
**Implementation PR:** `#1317`  
**Implementation merge:** `ca501751410bb3f0ad928c2b16d6d885551e7ea3`  
**Topic:** automatic workspace persistence runtime and private-vault implementation  
**Pointer semantics:** most recently checkpointed/default workspace; **not exclusive** and not a lock over concurrent workspaces.

A ChatGPT thread is a temporary working surface. A `PD-WS-*` workspace is the durable continuity object. More than one substantive workspace may be active or preserved at the same time.

## Active and recently preserved workspaces

### `PD-WS-20260901-0003` — automatic workspace persistence runtime

Read:

1. `archive/handoffs/2026-09-01-automatic-workspace-persistence-runtime-handoff.md`
2. `archive/AUTOMATIC_WORKSPACE_PERSISTENCE_RUNTIME_CLOSEOUT_01SEP2026.md`
3. `.github/governance/AUTOMATIC_WORKSPACE_PERSISTENCE_ARCHITECTURE_01SEP2026.md`
4. `.github/governance/CONCURRENT_WORKSPACE_REGISTRATION_PROTOCOL_01SEP2026.md`
5. `docs/WORKSPACE_PERSISTENCE_RUNBOOK.md`
6. `ops/AUTOMATIC_WORKSPACE_PERSISTENCE_V1.json`

### `PD-WS-20260901-0002` — authority discovery / Red SARA / AGE

Read:

1. `archive/handoffs/2026-09-01-authority-discovery-redsara-workspace-handoff.md`
2. the canonical authority-discovery controls named there.

### `PD-WS-20260901-0001` — Acosta Matos / Canarian Hospitality hotel-platform media package

Read:

1. `archive/handoffs/2026-09-01-acosta-matos-hotel-platform-digital-media-workspace-handoff.md`
2. the canonical digital-media, satire and platform controls named there.

The machine authority for the complete list and exact state is `data/workspace-register-v1.json`.

## Workspace selection rule for a new thread

1. Where the user supplies a `PD-WS-*` ID, use that workspace.
2. Otherwise select the workspace whose title/topic matches the user's substantive instruction.
3. Use the most recently checkpointed default above only when the instruction is genuinely ambiguous.
4. Reconcile current `main` before changing anything.
5. Do not remove, rename or supersede another workspace merely by updating this index.

A branch-local sequential ID is provisional. Before merge, re-read current `data/workspace-register-v1.json`. Current `main` wins any collision; the unmerged workspace must be renumbered under `PD-CWR-001`.

## Current implementation state

The tested runtime is merged through PR `#1317`. Its exact tested head was `aeedb75f7ffaca5614e6cfb299f207915edc9a00`; 13 workflow runs completed with zero failures. The merge commit is `ca501751410bb3f0ad928c2b16d6d885551e7ea3`.

For `PD-WS-20260901-0003`, an owner-only/not-shared Google Drive vault structure exists under the aliases recorded in the handoff. Its canonical post-merge private seed is:

- `PD-WS-20260901-0003-seed-20260901.zip`
- 14,298 bytes
- SHA-256 `84db4a21ca7fb5cfd871029380a373a6b917420af92bdf9992dded07621479e5`
- last private event `PD-WS-20260901-0003-EVT-000005`
- last event hash `d4c0263c524e094ccaa56bc8287b0c4c2e7db636aeba46a549f93bd4dc346fed`

A separate private manifest records the archive hash and merge reference. Exact Drive locators remain outside public Git.

The Python runtime is **not yet connected** to that Drive folder as a continuous filesystem/API event sink, no real historical ChatGPT export has been imported, and no OpenAI API request-path workbench or credential has been configured.

## New-thread bootstrap

> Continue from repository continuity state, not prior chat memory. Read `CURRENT_WORKSPACE_HANDOFF.md`, select the correct `PD-WS-*` workspace by my explicit ID or substantive topic, then read its detailed handoff and named canonical controls. Reconcile current `main`, preserve all evidence/publication/privacy boundaries, and continue only from recorded open work plus my new instruction. Persist material state during the work under `PD-AWP-001`; reconcile concurrent IDs under `PD-CWR-001`.

Older topic-specific deletion audits and handoffs remain historical controls. Updating the most-recent/default pointer does not invalidate or hide them.
