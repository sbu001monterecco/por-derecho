# Active workspace continuity index

**Current workspace:** `PD-WS-20260901-0005`
**Current continuation pointer:** `PD-WCH-20260901-DP748-P0-001`
**Status:** `DELETION_SAFE_WITH_OPEN_WORK`

**Implementation state:** DP 748/2026 P0 appeal/reopening package reconciled against current `main` `b0958077b71130fe808acaf1cc006185b6aa43fa` (PR #1333); it inherits the PR #1326 La Laguna identities at `273bb621de7db5473b1223fdbc080f9c733dd038`. Its provisional `0004` workspace ID was renumbered to `0005` because PR #1328 canonically occupied `0004` first. Governed PR state is recorded in the detailed handoff.
**Topic:** DP 748/2026 appeal, reopening and ETJ 163/2020 source mastery
**Pointer semantics:** most recently checkpointed/default workspace; **not exclusive** and not a lock over concurrent workspaces.

A ChatGPT thread is a temporary working surface. A `PD-WS-*` workspace is the durable continuity object. More than one substantive workspace may be active or preserved at the same time.

## Active and recently preserved workspaces

### `PD-WS-20260901-0005` — DP 748/2026 appeal/reopening

Read:

1. `archive/handoffs/2026-09-01-dp748-appeal-reopening-workspace-handoff.md`
2. `archive/DP748_2026_APPEAL_REOPENING_SOURCE_CONTROL_CLOSEOUT_01SEP2026.md`
3. `assets/data/dp748-2026-appeal-reopening-control-v1.json`
4. the canonical Master/CAEPR/counsel/procurador/gap controls named there.

### `PD-WS-20260901-0004` — PwC / Carlos Saavedra ^ completeness

Read:

1. `archive/handoffs/2026-09-01-pwc-carlos-saavedra-caret-interlink-workspace-handoff.md`
2. `assets/data/caepr-caret-pwc-carlos-saavedra-first-hop-v1.json`
3. `.github/governance/CAEPR_CARET_IDENTITY_AND_ALL_IS_VERIFICATION_PROTOCOL_26AUG2026.md`
4. the PwC evidence and correction controls named by the handoff.

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

For `PD-WS-20260901-0003`, the owner-only/not-shared Google Drive vault structure and current validated private seed snapshot were re-read on 1 September 2026 under the aliases recorded in the handoff. The current seed is the canonical `0003` revision; the earlier public fingerprint is preserved as a superseded intermediate snapshot in the detailed handoff. Exact private locators are intentionally withheld from public Git. The Python runtime is not yet connected to that Drive folder as a live filesystem/API event sink, and no real historical ChatGPT export has been imported.

## New-thread bootstrap

> Continue from repository continuity state, not prior chat memory. Read `CURRENT_WORKSPACE_HANDOFF.md`, select the correct `PD-WS-*` workspace by my explicit ID or substantive topic, then read its detailed handoff and named canonical controls. Reconcile current `main`, preserve all evidence/publication/privacy boundaries, and continue only from recorded open work plus my new instruction. Persist material state during the work under `PD-AWP-001`; reconcile concurrent IDs under `PD-CWR-001`.

Older topic-specific deletion audits and handoffs remain historical controls. Updating the most-recent/default pointer does not invalidate or hide them.
