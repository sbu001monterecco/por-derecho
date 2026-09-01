# Current workspace handoff

**Current workspace:** `PD-WS-20260901-0002`  
**Current continuation pointer:** `PD-WCH-20260901-AWP-RUNTIME-001`  
**Status:** `HANDOFF_READY_IMPLEMENTATION_PR_PENDING`  
**Topic:** automatic workspace persistence runtime and private-vault implementation

Before continuing this workspace in a new thread, read:

1. `archive/handoffs/2026-09-01-automatic-workspace-persistence-runtime-handoff.md`
2. `.github/governance/AUTOMATIC_WORKSPACE_PERSISTENCE_ARCHITECTURE_01SEP2026.md`
3. `.github/governance/WORKSPACE_THREAD_CONTINUITY_HANDOFF_STANDARD_01SEP2026.md`
4. `docs/WORKSPACE_PERSISTENCE_RUNBOOK.md`
5. `ops/AUTOMATIC_WORKSPACE_PERSISTENCE_V1.json`
6. `data/workspace-register-v1.json`
7. the canonical controls named by the detailed handoff, fetched from **current `main`**.

Do not assume the originating chat remains available or that its transient execution state is newer than the repository. Reconcile current `main` and the recorded implementation branch/PR before changing anything.

A workspace may span multiple ChatGPT threads. The stable `PD-WS-*` workspace identity is canonical; an individual chat is only a temporary working surface and may be superseded without creating a new workspace unless the substantive scope changes.

The private Google Drive vault exists under the aliases recorded in the handoff and was owner-only/not shared at creation. The exact locator is intentionally withheld from the public repository. The Python runtime is not yet connected to that Drive folder as a filesystem mount, and no raw transcript has been imported.

When GitHub is available and this is a substantive Por Derecho workspace, follow `PD-AWP-001`: persist material decisions, artifact/source/identity changes, repository/publication events, failures and open work as part of doing the work rather than waiting for a separate end-of-thread continuity audit.

## New-thread bootstrap

> Continue `PD-WS-20260901-0002` from repository continuity state, not prior chat memory. Read `CURRENT_WORKSPACE_HANDOFF.md` and the detailed handoff it names. Reconcile current `main` and any implementation PR, preserve all evidence/publication/privacy boundaries, and continue only from the recorded open work plus my new instruction. Use the tested append-only runtime where a private filesystem vault is available. Do not claim native all-thread ChatGPT capture or an implemented OpenAI API client.

Older topic-specific deletion audits and handoffs remain historical controls. `PD-WS-20260901-0001` remains preserved in its own prior handoff; this file is only the current continuation entrypoint.
