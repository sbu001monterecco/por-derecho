# Workspace / thread continuity handoff standard — 1 September 2026

**Control ID:** `PD-WCH-001`  
**Status:** repository-wide continuity governance  
**Purpose:** make any substantive ChatGPT/workspace thread replaceable by a new thread without losing unique decisions, evidence state, publication state, tool failures, open work or execution context.

## 1. Governing principle

A chat thread is a working surface, not the system of record.

No important project state should depend on the original conversation remaining open. Before a thread is abandoned, deleted, archived or superseded, its unique state must be reduced to a durable **continuity packet** in the repository.

The continuity packet must allow a competent new thread to answer, without guessing:

1. What was this workspace doing?
2. What is already completed and where is it recorded?
3. What is live/public, merged, branch-only, draft, held or failed?
4. What are the controlling source/evidence/legal boundaries?
5. Which exact artifacts, IDs, hashes, branches, PRs and routes matter?
6. What remains open?
7. What must not be repeated, inferred or silently changed?
8. What is the safest first action in the new thread?

## 2. The four-layer continuity packet

Every substantial workspace closeout should contain four layers.

### A. Always-current pointer

Repository root:

`CURRENT_WORKSPACE_HANDOFF.md`

This is deliberately short. It points to the current detailed handoff and identifies its status. It is the preferred first read for a new thread.

### B. Detailed workspace handoff

Preferred path:

`archive/handoffs/YYYY-MM-DD-<topic>-workspace-handoff.md`

The handoff captures scope, state, decisions, exact references, open work and startup instructions.

### C. Machine-readable handoff

Preferred path:

`archive/handoffs/YYYY-MM-DD-<topic>-workspace-handoff.json`

This preserves stable keys for automation, continuity audits and later reconstruction.

### D. Existing canonical controls

The handoff never duplicates the whole repository. It links to the controlling governance, evidence registers, publication manifests, source pages, PR/merge closeouts and other canonical records.

## 3. Mandatory detailed-handoff sections

Each detailed handoff must contain:

- **handoff ID and date**;
- **workspace/topic scope**;
- **continuity status**: `IN_PROGRESS`, `HANDOFF_READY`, `DELETION_SAFE`, or `DELETION_SAFE_WITH_OPEN_WORK`;
- **authoritative repository baseline**: current main SHA when checked;
- **active branch/PR state**, if any;
- **completed work** with exact paths/IDs;
- **public/live state** separately from repository state;
- **important decisions and terminology locks**;
- **evidence/source boundaries and anti-overstatement rules**;
- **artifact register**, including exact digital/media references where relevant;
- **tool failures or incomplete operations**;
- **open work / unresolved gaps**;
- **do-not-repeat / do-not-infer rules**;
- **next-thread first actions**;
- **copy-paste new-thread bootstrap prompt**;
- **deletion-safety test**.

## 4. State must be explicit

Never say merely “done”. Use the narrowest accurate state, for example:

- `MERGED_TO_MAIN`
- `LIVE_VERIFIED`
- `MERGED_NOT_LIVE_VERIFIED`
- `BRANCH_ONLY`
- `PR_OPEN`
- `DRAFT_ONLY`
- `RESERVED_NOT_GENERATED`
- `HASH_LOCKED_BINARY_MIRROR_GAP`
- `GENERATION_FAILED_NO_FILE_CREATED`
- `PUBLICATION_HOLD`
- `OPEN_EVIDENCE_GAP`

Repository completion, web deployment, institutional filing/service, social posting and evidential proof are different states and must never be collapsed.

## 5. Tool-failure continuity rule

A failed operation is part of workspace state when it affects what the next thread may safely assume.

The handoff must record:

- what was attempted;
- what failed;
- whether a file/result was actually created;
- any tool-level instruction not to retry automatically; and
- what user action would reopen the operation.

A failed image generation, failed web verification or failed connector write must never be converted into an implied completed deliverable.

## 6. Artifacts and binary continuity

For documents, spreadsheets, media, PDFs or images, the handoff should use the canonical asset/document register rather than relying on filenames alone.

For digital/media assets, use `PD-DMA-*` references and the caret governance in `.github/governance/DIGITAL_MEDIA_ASSET_CARET_IDENTITY_STANDARD_01SEP2026.md`.

An exact full-resolution binary that is not mirrored in the repository must be recorded as such. A derivative does not silently become the original.

## 7. Thread deletion audit

A workspace may be labelled `DELETION_SAFE` only when all of the following are true:

- no material instruction is known to remain only in chat;
- all unique decisions are in repository controls/handoff;
- exact open gaps are recorded;
- current branch/PR/main status is recorded;
- volatile outputs are either registered or explicitly acknowledged as not preserved;
- failures are recorded;
- the next-thread bootstrap prompt is sufficient to resume work;
- the handoff links to canonical source/evidence/publication controls rather than restating them inaccurately.

If any material item remains chat-only, status must remain `HANDOFF_READY_EXCEPT_CHAT_ONLY_GAP` or equivalent and the gap must be named.

## 8. New-thread startup protocol

The preferred new-thread instruction is:

> Start by reading `CURRENT_WORKSPACE_HANDOFF.md`, then the detailed handoff it names, then only the canonical controls listed there. Reconcile against current `main` before changing anything. Do not assume the originating chat remains available. Preserve all explicit evidence, attribution, publication and no-contact boundaries. Continue from the recorded next actions rather than re-running broad discovery unless the handoff identifies a stale or unresolved area.

## 9. No unnecessary re-digestion

A new thread should not repeatedly scan the whole repository merely because the prior chat is gone.

Default sequence:

1. current pointer;
2. detailed handoff;
3. named canonical controls;
4. current main/PR reconciliation;
5. targeted reads/searches for the next open task.

A full repository re-digest is justified only when the handoff is stale, contradictory, explicitly requests a unitary refresh, or the next task materially changes scope.

## 10. Updating the pointer

When a new substantive workspace becomes the active continuation point:

1. create/update its detailed Markdown + JSON handoff;
2. update `CURRENT_WORKSPACE_HANDOFF.md` to point to it;
3. keep older handoffs immutable except for correction notices;
4. record supersession explicitly;
5. merge the continuity update before treating the old thread as deletion-safe, unless the handoff explicitly records a branch-only exception.

## 11. Relationship to deletion audits

Existing `THREAD_DELETION_AUDIT_*` and topic-specific deletion-safe records remain valid historical controls.

This standard adds a common operating pattern above them. A topic-specific deletion audit may serve as the detailed handoff if it contains all mandatory fields; otherwise create a short workspace handoff pointing to the existing audit plus any missing execution state.

## 12. Current source of truth

- Root pointer: `CURRENT_WORKSPACE_HANDOFF.md`
- Machine protocol: `ops/WORKSPACE_THREAD_CONTINUITY_HANDOFF_V1.json`
- Detailed handoffs: `archive/handoffs/`
- General repository orientation: `CHATGPT_START_HERE.md`

The root pointer is the **continuation entrypoint**; `CHATGPT_START_HERE.md` remains the broader project control plane.
