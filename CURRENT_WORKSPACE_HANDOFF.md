# Active workspace continuity index

**Current workspace:** `PD-WS-20260901-0003`  
**Current continuation pointer:** `PD-WCH-20260901-AWP-RUNTIME-001`  
**Status:** `DELETION_SAFE_WITH_OPEN_WORK`  
**Topic:** automatic workspace persistence runtime and private-vault implementation  
**Pointer semantics:** most recently checkpointed/default workspace; **not exclusive** and not a lock over concurrent workspaces.

A ChatGPT thread is a temporary working surface. A `PD-WS-*` workspace is the durable continuity object. More than one substantive workspace may be active or preserved at the same time.

## Active and recently preserved workspaces

### `PD-WS-20260901-0003` — automatic workspace persistence runtime

Read:

1. `archive/handoffs/2026-09-01-automatic-workspace-persistence-runtime-handoff.md`
2. `.github/governance/AUTOMATIC_WORKSPACE_PERSISTENCE_ARCHITECTURE_01SEP2026.md`
3. `.github/governance/CONCURRENT_WORKSPACE_REGISTRATION_PROTOCOL_01SEP2026.md`
4. `docs/WORKSPACE_PERSISTENCE_RUNBOOK.md`
5. `ops/AUTOMATIC_WORKSPACE_PERSISTENCE_V1.json`

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

## Current private-vault boundary

For `PD-WS-20260901-0003`, an owner-only/not-shared Google Drive vault structure and a validated private seed snapshot exist under the aliases recorded in the handoff. Exact private locators are intentionally withheld from public Git. The Python runtime is not yet connected to that Drive folder as a live filesystem/API event sink, and no real historical ChatGPT export has been imported.

## New-thread bootstrap

> Continue from repository continuity state, not prior chat memory. Read `CURRENT_WORKSPACE_HANDOFF.md`, select the correct `PD-WS-*` workspace by my explicit ID or substantive topic, then read its detailed handoff and named canonical controls. Reconcile current `main`, preserve all evidence/publication/privacy boundaries, and continue only from recorded open work plus my new instruction. Persist material state during the work under `PD-AWP-001`; reconcile concurrent IDs under `PD-CWR-001`.

Older topic-specific deletion audits and handoffs remain historical controls. Updating the most-recent/default pointer does not invalidate or hide them.
