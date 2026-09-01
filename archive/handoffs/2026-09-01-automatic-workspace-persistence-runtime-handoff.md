# Workspace handoff — automatic workspace persistence runtime

**Handoff ID:** `PD-WCH-20260901-AWP-RUNTIME-001`  
**Workspace ID:** `PD-WS-20260901-0003`  
**Date:** 1 September 2026  
**Continuity status:** `DELETION_SAFE_WITH_OPEN_WORK`  
**Repository:** `sbu001monterecco/por-derecho`  
**Implementation PR:** `#1317`  
**Implementation merge:** `ca501751410bb3f0ad928c2b16d6d885551e7ea3`

## 1. Objective and completed phase

`PD-AWP-001` has moved from architecture alone to an executable, privacy-separated persistence layer that can:

- preserve a stable workspace across replacement ChatGPT threads;
- append material workspace events during the work;
- detect event-chain tampering;
- regenerate current state and a human-readable handoff;
- normalize an authorised ChatGPT account export into private storage without publishing it; and
- allow only an expressly approved public-safe derivative to cross into the public repository.

The long-term target remains a request-path Por Derecho workbench. That OpenAI API client is a separate credential-gated phase and is not represented as implemented.

## 2. Canonical identity and concurrency correction

The runtime workspace is canonically:

- `PD-WS-20260901-0003`

An earlier branch provisionally used `PD-WS-20260901-0002`. Current `main` independently registered that number first for the authority-discovery / Red SARA workspace. The collision was detected through the repository preservation gate and merge conflicts affecting the shared workspace register and root continuation pointer.

Resolution:

- current-main assignment `PD-WS-20260901-0002` remains with authority discovery;
- the unmerged persistence-runtime workspace was renumbered to `PD-WS-20260901-0003`;
- its private Drive alias and seed archive were corrected;
- superseded PR `#1316` was closed without merge;
- the runtime was reapplied to a fresh current-main branch; and
- `PD-CWR-001` now governs concurrent allocation and makes the root pointer an index rather than a mutex.

No workspace was silently overwritten.

## 3. Repository release

Architecture release:

- PR `#1314`
- merge `89e84ffd6656a37951565d769f5eee4214661e37`

Runtime release:

- PR `#1317`
- exact tested head `aeedb75f7ffaca5614e6cfb299f207915edc9a00`
- merge `ca501751410bb3f0ad928c2b16d6d885551e7ea3`
- changed files: 15
- workflow runs on the exact tested head: 13
- workflow failures: 0

The first mission-critical run on PR `#1317` correctly rejected mutable action tags. `checkout`, `setup-python` and `upload-artifact` were then pinned to exact upstream commit SHAs. The corrected head completed all workflows without failure.

## 4. Implemented runtime

### Code and commands

Runtime:

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
- SHA-256 content and event hashes;
- `previous_event_hash` chain;
- atomic state/handoff writes;
- portable exclusive lock files;
- owner-only file modes on POSIX where available;
- hard refusal to place a private vault under the public repository root;
- explicit visibility classes;
- no automatic public export based merely on a visibility label; and
- `public-summary` requires an explicit approved `public_summary` object.

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

It does not automatically treat every historical chat as a separate workspace and does not let stale chat state supersede current repository truth without review.

## 5. Schemas, tests and CI

Schemas:

- `schemas/workspace-event-v1.schema.json`
- `schemas/workspace-state-v1.schema.json`
- `schemas/chatgpt-export-import-manifest-v1.schema.json`

Tests and CI:

- `tests/test_workspace_persistence.py`
- `.github/workflows/audit-workspace-persistence.yml`

Local runtime suite:

1. initialization / append / checkpoint / validation;
2. event tampering detection;
3. explicit public-summary gate;
4. private ChatGPT-export normalization; and
5. refusal of a vault inside the public repository.

Result: **5 tests passed, 0 failed.**

Operations/documentation:

- `docs/WORKSPACE_PERSISTENCE_RUNBOOK.md`
- `examples/workspace-checkpoint.example.json`
- `ops/AUTOMATIC_WORKSPACE_PERSISTENCE_V1.json`
- `.github/governance/CONCURRENT_WORKSPACE_REGISTRATION_PROTOCOL_01SEP2026.md`
- public `.gitignore` exclusions for private vaults and ChatGPT exports

## 6. Private Google Drive vault

A real private destination structure exists in connected Google Drive under these aliases:

- root: `Por Derecho Private Workspaces`
- workspace: `PD-WS-20260901-0003 — Automatic Workspace Persistence Runtime`
- subfolders:
  - `01 State and Handoffs`
  - `02 Event Logs`
  - `03 ChatGPT Exports`
  - `04 Artifacts and Attachments`
  - `05 Publication Manifests`

Creation/readback showed the root as owned by `sbu001@monterecco.com`, `shared: false`, with owner permission only.

Exact Drive IDs and URLs are deliberately absent from the public repository. A connected successor thread should search the exact aliases and re-read permission metadata before using the vault.

### Canonical post-merge seed

The private `01 State and Handoffs` folder contains:

- `PD-WS-20260901-0003-seed-20260901.zip`
- bytes: `14298`
- SHA-256: `84db4a21ca7fb5cfd871029380a373a6b917420af92bdf9992dded07621479e5`
- ZIP integrity: `PASS`
- workspace validation: `PASS`
- last event: `PD-WS-20260901-0003-EVT-000005`
- last event hash: `d4c0263c524e094ccaa56bc8287b0c4c2e7db636aeba46a549f93bd4dc346fed`

The archive contains the private workspace marker, workspace metadata, five-event append-only chain, post-merge state, handoff, empty source/artifact/attachment registers and a private Drive locator. The exact locator file must never be committed to public `por-derecho`.

A separate private publication manifest records the archive hash, size, last event hash, PR and repository merge. It avoids a self-referential archive hash.

The former seed state was replaced in place. Successor work must use only canonical workspace `0003` and the post-merge hash above.

### Storage boundary

Google Drive currently provides a durable private cloud folder structure and validated seed archive, but it is **not yet connected as a continuous filesystem or API event sink**.

To make it the live runtime vault, one of these remains necessary:

- a locally synchronized/mounted Google Drive folder passed through `PD_WORKSPACE_VAULT`; or
- a Drive/object-store adapter preserving append, locking and integrity semantics.

No real raw ChatGPT transcript, Gmail/Drive source corpus or private attachment was uploaded by this implementation action.

## 7. Public/private state

### Public repository contains

- runtime source code;
- schemas;
- tests and pinned-action CI;
- source-safe governance and runbook;
- concurrent-workspace register/index;
- source-safe handoff/closeout metadata; and
- non-secret private-vault aliases, permission state, seed hash and event hash.

### Private Drive contains

- owner-only/not-shared folder structure;
- the validated canonical post-merge seed; and
- its separate private verification manifest.

### Not performed

- no real historical ChatGPT export imported;
- no raw transcript uploaded;
- no Gmail/Drive private-source corpus copied;
- no OpenAI API key created, read or reused;
- no OpenAI API request-path workbench built or configured;
- no social post, email, filing, service or authority communication.

## 8. Open work

1. Connect the runtime to a durable synchronized filesystem vault or implement a Drive/object-store adapter.
2. Optionally obtain and privately import an authorised ChatGPT data export.
3. Review the clustering queue and map related historical threads to stable workspaces after reconciling them with current repository truth.
4. Build the true request-path OpenAI workbench only after an explicit credential and deployment decision.
5. Add scheduled private backup after the live event-sink destination is selected.
6. Introduce a collision-resistant immutable `workspace_uid` alongside the human-readable `PD-WS-*` ID in the future workbench.

## 9. Do not infer

A successor thread must not infer that:

- ordinary ChatGPT now guarantees automatic capture of every thread;
- `CURRENT_WORKSPACE_HANDOFF.md` proves only one workspace exists;
- the public repository contains raw private transcripts;
- Google Drive is already a continuous mounted/API runtime event sink;
- historical chats have already been imported;
- an OpenAI API key exists or may be reused silently;
- the OpenAI API workbench has been built;
- repository merge equals website deployment, filing, service, authority notice or social publication; or
- a hash-chained workspace event proves the underlying external fact described in that event.

## 10. New-thread startup

1. Read `CURRENT_WORKSPACE_HANDOFF.md` as an index.
2. Select `PD-WS-20260901-0003` for persistence-runtime work.
3. Read this handoff, `PD-AWP-001`, `PD-WCH-001`, `PD-CWR-001`, the runbook, operations control and workspace register.
4. Reconcile current `main` before changing anything.
5. Search the private Drive vault by exact alias only when private-vault work is required.
6. Continue only from recorded open work plus the user's new instruction.

## 11. Copy-paste bootstrap

> Continue automatic workspace persistence as `PD-WS-20260901-0003`. Read `CURRENT_WORKSPACE_HANDOFF.md` as a concurrent-workspace index, then `archive/handoffs/2026-09-01-automatic-workspace-persistence-runtime-handoff.md`, `PD-AWP-001`, `PD-WCH-001`, `PD-CWR-001`, the runbook, operations control and workspace register from current main. Reconcile current main before writing. Preserve the public/private boundary. The owner-only/not-shared Drive vault and validated post-merge seed exist, but no continuous filesystem/API sink, real historical export import or OpenAI API workbench is complete. Continue from recorded open work plus my new instruction.

## 12. Deletion-safety test

Result: **DELETION-SAFE WITH OPEN WORK.**

No material decision, runtime state, collision correction, private seed identity, failure, limitation or next action identified for this implementation remains dependent on the originating chat. Open work is implementation work, not a continuity gap.
