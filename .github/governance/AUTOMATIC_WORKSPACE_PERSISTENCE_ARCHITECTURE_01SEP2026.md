# Automatic workspace persistence architecture — 1 September 2026

**Control ID:** `PD-AWP-001`  
**Status:** repository-wide continuity architecture  
**Purpose:** minimise or eliminate dependence on any individual ChatGPT thread by making workspace state persist continuously into controlled repositories/storage.

## 1. Core principle

The target state is not “save every chat transcript into the public repository.” The target state is:

> **Every substantive workspace should continuously externalise its operative state, provenance and artifacts so that any new thread can resume safely without the previous thread.**

Full conversation preservation and operative project-state preservation are separate requirements.

The operative state is the higher-priority continuity object.

## 2. What can and cannot be automatic inside ordinary ChatGPT

### Near-automatic inside a connected ChatGPT conversation

When a substantive Por Derecho thread is active and the GitHub connector is available, the assistant can apply a standing persistence protocol during the work:

- allocate or recover a workspace ID;
- read the current handoff and repository baseline;
- write material decisions, artifact IDs, source/evidence boundaries and open tasks as they arise;
- checkpoint after material repository/publication/artifact events;
- refresh the workspace handoff before declaring a thread deletion-safe.

This is **agentic persistence while the assistant is actively responding**.

### What ordinary ChatGPT cannot guarantee by itself

The current conversational environment does not expose a universal guaranteed event hook to this assistant for:

- every newly created ChatGPT thread;
- every message in every thread regardless of whether GitHub work is requested;
- a browser/app close event;
- a thread deletion event; or
- an automatic export of all historical ChatGPT conversations into GitHub.

Therefore a “zero-touch save every thread forever” guarantee cannot be truthfully implemented solely as repository instructions inside an ordinary ChatGPT conversation.

A repository rule can govern what the assistant does when it is active; it cannot itself create a ChatGPT platform webhook that does not exist in the working environment.

## 3. Three persistence modes

### Mode A — `CONNECTED_AGENTIC_CHECKPOINTING`

**Recommended immediately.**

Use ordinary ChatGPT plus the connected GitHub repository. For any substantive Por Derecho workspace:

1. **INIT** — recover/create workspace record at the first material repository-related turn.
2. **CHECKPOINT** — after any material decision, correction, artifact generation, filing draft, source-map change, PR/merge, publication-state change or major evidence finding.
3. **HEARTBEAT** — periodically refresh compact state during long-running work rather than waiting for an explicit “continuity audit”.
4. **HANDOFF** — maintain a deletion-safe Markdown/JSON handoff.
5. **RESUME** — new thread starts from `CURRENT_WORKSPACE_HANDOFF.md` or a named workspace ID.

This can make loss exposure very small because material state is written during the thread rather than only at the end.

**Limitation:** if the user starts a new unrelated chat and never invokes the repository/continuity workflow, the repository cannot know that chat exists.

### Mode B — `PRIVATE_ARCHIVE_PLUS_PUBLIC_STATE`

**Recommended architecture for this matter.**

Split persistence into two repositories/storage tiers:

#### Private workspace vault

Suggested private repository or encrypted object store:

- `por-derecho-workspaces-private`, or
- equivalent private encrypted storage.

It may contain:

- visible user/assistant conversation exports;
- private working notes supplied by the user;
- raw generated artifacts;
- uploaded attachments where authorised;
- connector-derived source references/metadata subject to source rules;
- per-workspace event logs;
- state manifests and handoffs.

#### Public `por-derecho`

Contains only publication-safe material:

- source-safe continuity controls;
- public evidence/artifacts;
- redacted/derived state summaries;
- exact hashes/references where appropriate;
- public relationship maps and pages;
- publication manifests and correction records.

**Never automatically dump raw conversations, Gmail/Drive material, private personal data or confidential documents into the public repository.**

The public/private boundary must be explicit per event/artifact.

### Mode C — `TRUE_EVENT_SOURCED_AUTOMATIC_CLIENT`

**Target for genuine zero-touch persistence.**

Build a small Por Derecho chat/workbench using the OpenAI API plus a GitHub App/private storage backend. Because the application owns the interaction channel, every visible event can be captured automatically before/after model execution.

The event stream can record:

- workspace ID;
- conversation/session ID;
- timestamp;
- user-visible user message;
- user-visible assistant response;
- tool/action metadata that is appropriate to preserve;
- attachment references and hashes;
- repository commit/PR/publication events;
- supersession/correction events;
- previous-event hash for append-only integrity.

The application then maintains a compact current state/handoff automatically.

This is the only architecture here that can truthfully promise **every new workspace event is persisted automatically**, because the persistence layer sits in the request path rather than depending on the assistant remembering to write GitHub state.

## 4. Do not commit every chat turn directly to the public Git repository

Git is excellent for canonical state, review, provenance and source-safe artifacts. It is not ideal as the only raw event store for high-volume conversations and binaries.

Recommended event-sourcing pattern:

- raw event stream → private database/object store/private repository;
- material checkpoint → compact JSON/Markdown state;
- publication-safe changes → public Git PR/merge;
- binary master → private/object storage with SHA-256;
- public derivative → public repository when authorised.

This avoids thousands of noisy commits while preserving exact provenance.

## 5. Workspace identity

Every substantive workspace should receive a stable ID independent of the ChatGPT title or URL.

Preferred pattern:

`PD-WS-YYYYMMDD-NNNN`

Example:

`PD-WS-20260901-0001`

The workspace register should record:

- stable ID;
- topic/title;
- created/last-checkpoint timestamps;
- status;
- public/private classification;
- current handoff path;
- related proceedings/entities/assets;
- current repository baseline;
- related branches/PRs;
- artifact/media references;
- predecessor/successor workspaces where applicable.

A ChatGPT thread URL/ID, if available through a future capture layer, is metadata—not the canonical identity.

## 6. Material-event checkpoint triggers

In Mode A, write a checkpoint when any of these occurs:

- a new factual proposition is adopted/rejected/corrected;
- a name/entity/caret is reconciled;
- a new proceeding/source/asset is registered;
- a new artifact receives a stable reference/hash;
- a draft changes filing/publication readiness;
- a branch/PR/merge/deployment occurs;
- a website route is created or verified;
- an external-publication/social package is prepared or actually published;
- a legal/evidential attribution boundary materially changes;
- a tool failure changes what can safely be assumed;
- the user says continuity, deletion-safe, preserve, publish, register, interlink or equivalent;
- the assistant is about to leave a long multi-step task with open work.

Do not wait for thread end.

## 7. Two representations per workspace

Each active workspace should maintain:

### `state.json`

Machine-readable current state:

- current objective;
- completed events;
- current baseline SHA;
- active branch/PR;
- public/live states;
- open gaps;
- artifact references;
- evidence/publication boundaries;
- next actions.

### `handoff.md`

Human-readable continuation packet under `archive/handoffs/` or a workspace-specific directory.

The existing `PD-WCH-001` handoff standard remains controlling for deletion safety.

## 8. Existing/historical ChatGPT threads — one-time backfill

Historical chats cannot be assumed to be programmatically enumerable from this repository.

Preferred migration:

1. obtain an authorised ChatGPT data export or other user-controlled export of historical conversations;
2. ingest only the visible conversation records and attachments the user wants preserved;
3. assign stable `PD-WS-*` IDs;
4. store raw transcripts privately;
5. generate compact topic/state manifests;
6. reconcile each manifest against current `por-derecho` so obsolete chat state does not overwrite newer repository truth;
7. mark duplicates/superseded threads;
8. extract only publication-safe continuity data into the public repo.

Do **not** bulk-publish raw historical conversations into `por-derecho`.

## 9. Suggested private-vault structure

```text
workspaces/
  PD-WS-20260901-0001/
    workspace.json
    events.jsonl
    state.json
    handoff.md
    artifacts.json
    sources.json
    attachments-manifest.json
    publication-events.jsonl
```

Large binaries can live in object storage with hashes in `artifacts.json`.

## 10. Event integrity

For high-value legal/evidential continuity, use an append-only event chain:

- `event_id`
- `timestamp_utc`
- `workspace_id`
- `event_type`
- `visibility_class`
- `content_hash`
- `previous_event_hash`
- `repository_refs`
- `artifact_refs`

This provides tamper-evident continuity without pretending that the chat itself is evidence of an underlying external fact.

## 11. Visibility/privacy classes

Every persisted event/artifact should carry one of:

- `PUBLIC_SOURCE_SAFE`
- `PUBLIC_DERIVED_SAFE`
- `PRIVATE_WORKSPACE`
- `CONFIDENTIAL_USER_SUPPLIED`
- `CONNECTED_SOURCE_RESTRICTED`
- `PUBLICATION_REVIEW_REQUIRED`

Automatic sync to the public repo is allowed only for the first two classes or after an explicit governed publication transition.

## 12. GitHub issue/discussion fallback

If building a private event store is deferred, a middle-ground option is one private GitHub Issue per `PD-WS-*` workspace.

The assistant/application can append checkpoint comments and keep the issue body as current state.

Advantages:

- simpler than a custom database;
- chronological event history;
- searchable;
- linkable to PRs/commits.

Limitations:

- still requires an event producer;
- poor home for large binaries;
- less structured than JSONL/database;
- must remain private for raw workspace content.

## 13. Projects/Work are supplementary, not the system of record

A persistent ChatGPT workspace/project can help group chats, files and artifacts, but repository/object-store persistence should remain the continuity authority for this project if the objective is deletion-safe, independently auditable, Git-linked state.

Do not treat “still visible in ChatGPT” as equivalent to repository preservation.

## 14. Recommended implementation sequence

### Phase 1 — now

Adopt Mode A:

- standing agentic checkpoint rule for substantive Por Derecho threads;
- stable `PD-WS-*` register;
- material-event checkpoints;
- `CURRENT_WORKSPACE_HANDOFF.md` continuation pointer;
- existing `PD-WCH-001` deletion-safe closeout.

### Phase 2 — private safety layer

Create a private workspace vault and move raw/full-workspace preservation there. Public repo receives only governed safe summaries/artifacts.

### Phase 3 — historical import

One-time authorised import of historical ChatGPT exports, reconciled against current repository truth.

### Phase 4 — true automation

Build a Por Derecho workbench/client using the OpenAI API so persistence occurs in the request path. Add GitHub App/object-store integration and append-only event logging.

## 15. Operating rule for future threads

When the assistant recognises a substantive Por Derecho workspace and has GitHub access, default to:

> **Persist material state as part of doing the work, not as a separate end-of-thread chore.**

The user should not need to say “continuity audit” repeatedly for important material changes to be externalised.

However, the assistant must remain truthful about the limit: repository governance cannot automatically discover or save a ChatGPT thread in which no persistence-capable action is ever invoked.

## 16. Relationship to existing governance

This architecture supplements, and does not replace:

- `.github/governance/WORKSPACE_THREAD_CONTINUITY_HANDOFF_STANDARD_01SEP2026.md` (`PD-WCH-001`);
- `ops/WORKSPACE_THREAD_CONTINUITY_HANDOFF_V1.json`;
- `CURRENT_WORKSPACE_HANDOFF.md`;
- topic-specific deletion audits;
- privacy/publication/source-governance controls;
- digital/media asset caret governance.

`PD-AWP-001` governs **continuous persistence**; `PD-WCH-001` governs **safe handoff/deletion**.
