# Workspace handoff — automatic workspace persistence runtime

**Handoff ID:** `PD-WCH-20260901-AWP-RUNTIME-001`  
**Workspace ID:** `PD-WS-20260901-0003`  
**Date:** 1 September 2026  
**Continuity status:** `HANDOFF_READY`
**Repository:** `sbu001monterecco/por-derecho`

**Authoritative baseline checked:** `3977178d0d01a11ab349c81e0f834322f46d5da2` (`origin/main`, 1 September 2026)
**Closeout record state:** `BRANCH_ONLY` on `codex/pd-ws-20260901-0003-continue`; no push, PR or merge is represented.

## 1. Objective

Turn `PD-AWP-001` from architecture alone into an executable, privacy-separated persistence layer that can:

- preserve a stable workspace across replacement ChatGPT threads;
- append material workspace events during the work;
- detect event-chain tampering;
- regenerate current state and a human-readable handoff;
- normalize an authorised ChatGPT account export into private storage without publishing it; and
- allow only an expressly approved public-safe derivative to cross into the public repository.

The long-term target remains a request-path Por Derecho workbench. That OpenAI API client is a separate credential-gated phase and is not represented as implemented.

## 2. Identity and concurrency correction

The runtime workspace is canonically:

- `PD-WS-20260901-0003`

An earlier implementation branch provisionally used `PD-WS-20260901-0002`. Before merge, current `main` independently registered that number for the authority-discovery / Red SARA workspace. The collision was detected through merge conflicts affecting the workspace register and root continuation pointer.

Resolution:

- current-main assignment `PD-WS-20260901-0002` remains with authority discovery;
- the unmerged persistence-runtime workspace was renumbered to `PD-WS-20260901-0003`;
- its private Drive alias and seed archive were corrected;
- the stale/conflicted PR is superseded by a fresh current-main implementation branch; and
- `PD-CWR-001` now governs concurrent allocation and makes the root pointer an index rather than a mutex.

No workspace was silently overwritten.

## 3. Repository baseline and branches

Original architecture baseline:

- PR #1314 merge `89e84ffd6656a37951565d769f5eee4214661e37`

Original implementation branch/PR:

- `agent/workspace-persistence-runtime-20260901`
- PR #1316
- superseded because current `main` advanced and the branch collided on `CURRENT_WORKSPACE_HANDOFF.md` and `data/workspace-register-v1.json`

Reconciled implementation branch:

- `agent/workspace-persistence-runtime-reconciled-20260901`
- constructed from current main `1099e48a83b8f81cd652734df5e5012336985e62`
- includes the tested runtime plus current-main authority workspace state
- merged through PR #1317 at `ca501751410bb3f0ad928c2b16d6d885551e7ea3`

Reconciliation on 1 September 2026:

- fetched `origin/main`: `3977178d0d01a11ab349c81e0f834322f46d5da2`;
- PR #1317 merge is an ancestor of that current main;
- the merged runtime tests and read-only repository audit both pass; and
- this source-safe closeout correction remains branch-only until separately merged.

A successor thread must re-check current `main` and any later closeout PR before writing.

## 4. Implemented runtime

### Code

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

The local smoke suite completed successfully:

1. initialization / append / checkpoint / validation;
2. event tampering detection;
3. explicit public-summary gate;
4. private ChatGPT-export normalization; and
5. refusal of a vault inside the public repository.

Result: **5 tests passed**.

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

Creation/readback showed the root as owned by `sbu001@monterecco.com`, `shared: false`, with owner permission only. Read-only metadata verification on 1 September 2026 reconfirmed the root and canonical `0003` workspace folder as `shared: false`, with one owner permission, and located all five expected subfolders.

Exact Drive IDs and URLs are deliberately absent from the public repository. A connected successor thread should search the exact aliases and re-read permission metadata before using the vault.

### Corrected private seed

The private `01 State and Handoffs` folder contains:

- `PD-WS-20260901-0003-seed-20260901.zip`
- bytes: `14298`
- SHA-256: `84db4a21ca7fb5cfd871029380a373a6b917420af92bdf9992dded07621479e5`
- validation: `PASS`

The archive contains a private workspace marker, `workspace.json`, a five-event append-only chain, `state.json`, `handoff.md`, empty source/artifact/attachment registers and a private Drive locator. A private in-memory validation on 1 September 2026 passed workspace identity, sequence, content-hash, event-hash, previous-event-hash and state/last-event reconciliation. The exact locator file must never be committed to public `por-derecho`.

Drive revision metadata records the collision-correction sequence without requiring public locator or revision IDs: provisional `0002` snapshot (`8748` bytes), intermediate `0002` snapshot (`10803` bytes), and current canonical `0003` snapshot (`14298` bytes). The previously published `10803`-byte SHA-256 `5b38b80efef14bab05f8d54160c792b24a0cedc610129453a92655f06fd2f742` is preserved as the superseded intermediate fingerprint; successor work must use only the current canonical `0003` fingerprint above.

### Storage boundary

The Python runtime writes to a filesystem path. Google Drive presently provides the durable private cloud structure and seed archive, but is **not yet connected as a live filesystem event sink**.

To make it the live runtime vault, one of these remains necessary:

- a locally synchronized/mounted Google Drive folder passed through `PD_WORKSPACE_VAULT`; or
- a Drive/object-store adapter preserving append, locking and integrity semantics.

No real raw ChatGPT transcript, Gmail/Drive source corpus or private attachment has been uploaded by this implementation action.

## 7. Public/private state

### Public repository contains

- runtime source code;
- schemas;
- tests and CI;
- source-safe governance and runbook;
- public workspace register/index;
- source-safe handoff metadata; and
- non-secret private-vault aliases, permission state and seed hash.

### Private Drive contains

- owner-only/not-shared folder structure; and
- the corrected validated seed snapshot for `PD-WS-20260901-0003`.

### Not performed

- no real historical ChatGPT export imported;
- no raw transcript uploaded;
- no Gmail/Drive private-source corpus copied;
- no OpenAI API key created, read or reused;
- no OpenAI API request-path workbench built or configured;
- no social post, email, filing, service or authority communication.

## 8. Open work

1. Merge this source-safe closeout correction and record its exact merge SHA; the runtime implementation itself is already merged through PR #1317.
2. Connect the runtime to a durable filesystem vault or implement a Drive/object-store adapter.
3. Initialise or restore the live private `PD-WS-20260901-0003` event chain at that destination, using the seed only as a controlled starting snapshot.
4. Optionally obtain and privately import an authorised ChatGPT data export.
5. Review the clustering queue and map related historical threads to stable workspaces.
6. Build the true request-path OpenAI workbench only after an explicit credential decision.
7. Add scheduled private backup after the live destination is selected.
8. Introduce a collision-resistant `workspace_uid` in the future workbench while preserving human-readable `PD-WS-*` IDs.

## 9. Do not infer

A successor thread must not infer that:

- ordinary ChatGPT now guarantees automatic capture of every thread;
- `CURRENT_WORKSPACE_HANDOFF.md` proves only one workspace exists;
- the public repository contains raw private transcripts;
- Google Drive is already a live mounted/runtime event sink;
- historical chats have already been imported;
- an OpenAI API key exists or may be reused silently;
- the OpenAI API workbench has been built;
- repository merge equals website deployment, filing, service, authority notice or social publication; or
- a hash-chained chat event proves the underlying external fact described in that event.

## 10. New-thread startup

1. Read `CURRENT_WORKSPACE_HANDOFF.md` as an index.
2. Select `PD-WS-20260901-0003` for persistence-runtime work.
3. Read this handoff, `PD-AWP-001`, `PD-WCH-001`, `PD-CWR-001`, the runbook, operations control and workspace register.
4. Reconcile current `main` and any later PR/merge.
5. Search the private Drive vault by exact alias only when private-vault work is required.
6. Continue only from recorded open work plus the user's new instruction.

## 11. Copy-paste bootstrap

> Continue automatic workspace persistence as `PD-WS-20260901-0003`. Read `CURRENT_WORKSPACE_HANDOFF.md` as a concurrent-workspace index, then `archive/handoffs/2026-09-01-automatic-workspace-persistence-runtime-handoff.md`, `PD-AWP-001`, `PD-WCH-001`, `PD-CWR-001`, the runbook, operations control and workspace register from current main. Reconcile any later merge before writing. Preserve the public/private boundary. The owner-only/not-shared Drive vault and validated canonical 0003 seed exist, but no live filesystem/API sink, historical export import or OpenAI API workbench is complete. Continue from recorded open work plus my new instruction.

## 12. Deletion-safety test

Current result: **HANDOFF READY; IMPLEMENTATION MERGED; SOURCE-SAFE CLOSEOUT CORRECTION BRANCH-ONLY.**

The substantive design, code and canonical workspace correction are merged. The private vault holds the validated current seed. The corrected current-main baseline, implementation merge SHA, live permission readback and superseding seed fingerprint are captured on the closeout branch. Final status becomes `DELETION_SAFE_WITH_OPEN_WORK` when this source-safe closeout correction is merged and its exact merge reference is recorded.
