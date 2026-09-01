# Workspace handoff — automatic workspace persistence runtime

**Handoff ID:** `PD-WCH-20260901-AWP-RUNTIME-001`  
**Workspace ID:** `PD-WS-20260901-0002`  
**Date:** 1 September 2026  
**Status at this checkpoint:** `HANDOFF_READY_IMPLEMENTATION_PR_PENDING`  
**Repository:** `sbu001monterecco/por-derecho`

## 1. Objective

Turn `PD-AWP-001` from architecture alone into an executable, privacy-separated persistence layer that can:

- preserve a stable workspace across replacement ChatGPT threads;
- append material workspace events during the work;
- detect later event-chain tampering;
- regenerate current state and a human-readable handoff;
- import an authorised ChatGPT account export into private storage without publishing it; and
- allow only an expressly approved public-safe derivative to cross into the public repository.

The long-term target remains a request-path Por Derecho workbench. That OpenAI API client is a separate credential-gated phase and is not falsely represented as implemented here.

## 2. Repository baseline and implementation branch

Implementation began from main:

- `89e84ffd6656a37951565d769f5eee4214661e37`
- PR #1314 merge: automatic workspace persistence architecture

Current implementation branch:

- `agent/workspace-persistence-runtime-20260901`

A successor thread must reconcile the branch/PR against current `main` before writing.

## 3. Implemented files

### Runtime

- `scripts/workspace_persistence.py`

Commands:

- `doctor`
- `init`
- `append`
- `checkpoint`
- `validate`
- `import-chatgpt`
- `public-summary`
- `validate-repository`

The runtime uses only the Python standard library.

### Integrity and privacy behavior

- stable `PD-WS-YYYYMMDD-NNNN` workspace IDs;
- append-only `events.jsonl`;
- content SHA-256;
- event SHA-256;
- `previous_event_hash` chain;
- atomic writes for state and handoff outputs;
- portable exclusive lock files;
- owner-only file modes on POSIX where available;
- hard refusal to place a private vault under the public repository root;
- explicit visibility classes;
- no automatic public export based merely on a visibility label;
- `public-summary` requires an explicit `public_summary` object in private state.

### Historical ChatGPT import

`import-chatgpt` accepts an authorised export ZIP or `conversations.json` and:

- normalizes visible user/assistant messages privately;
- preserves conversation, node and parent identifiers;
- hashes normalized content;
- excludes tool/system messages by default;
- creates an unassigned clustering queue;
- does not print message content;
- does not copy the original export unless expressly requested; and
- marks the batch `PRIVATE_ONLY_DO_NOT_PUBLISH`.

It does not automatically treat every historical chat as a separate workspace and does not allow stale chat state to supersede current repository truth without review.

### Schemas

- `schemas/workspace-event-v1.schema.json`
- `schemas/workspace-state-v1.schema.json`
- `schemas/chatgpt-export-import-manifest-v1.schema.json`

### Tests and CI

- `tests/test_workspace_persistence.py`
- `.github/workflows/audit-workspace-persistence.yml`

The local smoke suite completed successfully on 1 September 2026:

- initialization/append/checkpoint/validation;
- event tampering detection;
- explicit public-summary gate;
- private ChatGPT export normalization; and
- refusal of a vault inside the public repository.

Result: **5 tests passed**.

### Operations and documentation

- `docs/WORKSPACE_PERSISTENCE_RUNBOOK.md`
- `examples/workspace-checkpoint.example.json`
- updated `ops/AUTOMATIC_WORKSPACE_PERSISTENCE_V1.json`
- updated public `.gitignore` private-vault/export exclusions

## 4. Private vault provisioned in Google Drive

A real private destination structure was created in the connected Google Drive:

- root alias: `Por Derecho Private Workspaces`
- workspace alias: `PD-WS-20260901-0002 — Automatic Workspace Persistence Runtime`
- subfolders:
  - `01 State and Handoffs`
  - `02 Event Logs`
  - `03 ChatGPT Exports`
  - `04 Artifacts and Attachments`
  - `05 Publication Manifests`

Metadata readback on creation showed the root folder as:

- owned by `sbu001@monterecco.com`;
- `shared: false`; and
- owner permission only.

The exact Drive IDs/URLs are deliberately not stored in the public repository. A future connected thread should search the exact root/workspace aliases and re-read permission metadata before using them.

### Important storage boundary

The Python runtime writes to a filesystem path. The Google Drive structure is presently a durable private cloud destination/organizational vault, not yet a direct mounted filesystem target for the runtime.

To use it as the runtime’s live vault, one of the following remains necessary:

- a local Google Drive synchronized/mounted folder passed through `PD_WORKSPACE_VAULT`; or
- a later Drive adapter that writes event/state files through the Drive API while preserving append and integrity semantics.

No raw conversation, Gmail/Drive source material or private attachment has been uploaded by this implementation action.

## 5. Public/private state

### Public repository

Contains only:

- runtime source code;
- schemas;
- tests;
- CI;
- source-safe governance and runbook;
- workspace registry and handoff metadata; and
- non-secret Drive aliases/handling state.

### Private Drive

Contains only the newly created empty folder structure at this checkpoint.

### Not performed

- no historical ChatGPT export requested or imported;
- no raw transcript uploaded;
- no Gmail/Drive private-source corpus copied;
- no API key created, read or reused;
- no OpenAI API workbench built or configured;
- no social-media post, email, filing, service or authority communication.

## 6. Open work

1. Complete PR/checks/merge for the runtime implementation and record exact merge SHA.
2. Choose how the filesystem runtime will reach durable private storage:
   - synchronized Google Drive local folder;
   - separate private Git repository checkout; or
   - a future Drive/object-store adapter.
3. Initialize `PD-WS-20260901-0002` in that real filesystem vault with the runtime.
4. Optionally request an authorised ChatGPT data export and import it privately.
5. Review the clustering queue and map related historical threads to stable workspaces.
6. Implement the true request-path OpenAI workbench only after a deliberate credential decision.
7. Add scheduled private backup after the private destination/mount is selected.

## 7. Do not infer

A successor thread must not infer that:

- ordinary ChatGPT now guarantees automatic capture of every thread;
- the public repository contains raw private transcripts;
- the Google Drive vault is already connected as a live filesystem mount;
- historical chats have already been imported;
- an OpenAI API key exists or may be reused silently;
- the OpenAI API workbench has been built;
- repository merge equals website deployment, filing, service, authority notice or social publication; or
- a hash-chained chat event proves the underlying external fact described in that event.

## 8. Next-thread bootstrap

> Continue automatic workspace persistence from `PD-WS-20260901-0002`. Read `CURRENT_WORKSPACE_HANDOFF.md`, this handoff, `PD-AWP-001`, `docs/WORKSPACE_PERSISTENCE_RUNBOOK.md`, `ops/AUTOMATIC_WORKSPACE_PERSISTENCE_V1.json` and `data/workspace-register-v1.json` from current main. Reconcile the implementation branch/PR and current main before writing. Preserve the public/private boundary. The private Google Drive vault exists by alias and was owner-only/not shared at creation, but the filesystem runtime is not yet mounted to it. Do not claim native all-thread ChatGPT capture or an implemented OpenAI API client. Continue from the recorded open work plus my new instruction.

## 9. Deletion-safety state

The substantive design and implementation state are repository-captured. Final `DELETION_SAFE_WITH_OPEN_WORK` status requires merge/readback of this implementation and an updated exact closeout reference. Until then, this handoff is sufficient for continuation but remains `HANDOFF_READY_IMPLEMENTATION_PR_PENDING`.
