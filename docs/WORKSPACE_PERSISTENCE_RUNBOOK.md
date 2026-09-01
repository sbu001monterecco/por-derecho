# Por Derecho workspace persistence runbook

**Runtime:** `scripts/workspace_persistence.py`  
**Governance:** `PD-AWP-001` + `PD-WCH-001` + `PD-CWR-001`  
**Current implementation level:** tested private append-only runtime, public continuity controls and a provisioned private Drive seed vault. No native all-ChatGPT-thread webhook is claimed.

## 1. Operating model

A ChatGPT thread is a temporary working surface. A `PD-WS-*` workspace is the durable continuity object.

The runtime provides:

- stable workspace identities;
- append-only JSONL events;
- SHA-256 content hashes and a previous-event hash chain;
- atomic state and handoff regeneration;
- explicit visibility classes;
- refusal to place a private vault inside public `por-derecho`;
- controlled public-summary export;
- private normalization of an authorised ChatGPT data export; and
- repository/CI validation of the public continuity layer.

It does **not** claim that ordinary ChatGPT exposes a guaranteed hook for every new thread, every turn, app close or deletion. Genuine zero-touch capture requires a workbench/client that owns the request path.

## 2. Public and private layers

### Public repository

`sbu001monterecco/por-derecho` contains only source-safe controls, schemas, runtime code, public handoffs, approved derivatives and hashes/aliases that are safe to disclose.

### Private workspace vault

Raw transcripts, private events, connected-source material, attachments and exact private locators belong outside the public repository.

A private Google Drive structure now exists under the aliases:

- `Por Derecho Private Workspaces`
- `PD-WS-20260901-0003 — Automatic Workspace Persistence Runtime`

It was owner-only and not shared when created. The exact locator is intentionally absent from public Git. Its current seed is an archived snapshot, not yet a live filesystem mount.

## 3. Choose a live filesystem vault

The Python runtime needs a filesystem path outside the public checkout. Suitable choices include:

- a synchronized local Google Drive directory mapped to the private Drive vault;
- a checkout of a separate private Git repository;
- an encrypted local directory backed up privately; or
- a future Drive/object-store adapter built around the same event schema.

Do not point the runtime at `por-derecho` or any subdirectory of it.

### Linux/macOS

```bash
export PD_WORKSPACE_VAULT="$HOME/por-derecho-workspaces-private"
python3 scripts/workspace_persistence.py doctor
```

### PowerShell

```powershell
$env:PD_WORKSPACE_VAULT = "$HOME\por-derecho-workspaces-private"
python scripts/workspace_persistence.py doctor
```

`doctor` creates only the private vault marker and confirms that the destination is outside public Git. It does not read an OpenAI API key or GitHub token.

## 4. Workspace-ID allocation and concurrency

Read `PD-CWR-001` before registering a new public workspace.

The numeric ID calculated locally or on a branch is provisional. Before merge:

1. re-read current `data/workspace-register-v1.json`;
2. confirm the ID is still free;
3. preserve all existing workspace rows;
4. renumber the unmerged workspace if current `main` already owns the ID; and
5. update private aliases, seed archives, events and handoffs affected by the correction.

Current `main` wins. The root handoff is an index, not a mutex that permits one concurrent thread to erase another.

## 5. Initialise or recover a workspace

Example using the current runtime workspace:

```bash
python3 scripts/workspace_persistence.py init \
  --workspace-id PD-WS-20260901-0003 \
  --title "Automatic workspace persistence runtime" \
  --objective "Implement continuous, privacy-separated workspace capture" \
  --repository sbu001monterecco/por-derecho \
  --baseline REPLACE_WITH_CURRENT_MAIN_SHA
```

Omit `--workspace-id` to allocate the next local daily sequence. Local auto-allocation does not by itself reserve a public ID; reconcile before merge. Use `--resume` only to recover an existing private workspace. It never overwrites the event chain.

The workspace directory contains:

```text
workspace.json
state.json
handoff.md
events.jsonl
artifacts.json
sources.json
attachments-manifest.json
publication-events.jsonl
```

## 6. Append a material event

```bash
python3 scripts/workspace_persistence.py append \
  --workspace-id PD-WS-20260901-0003 \
  --event-type BRANCH_PR_MERGE \
  --summary "Persistence runtime PR merged" \
  --visibility PRIVATE_WORKSPACE \
  --repository-ref "sbu001monterecco/por-derecho#PR" \
  --details-json '{"state":"MERGED_TO_MAIN"}'
```

Useful event types include:

- `MATERIAL_DECISION`
- `FACT_CORRECTED`
- `IDENTITY_RECONCILED`
- `SOURCE_REGISTERED`
- `ARTIFACT_REGISTERED`
- `WORKSPACE_ID_COLLISION_RESOLVED`
- `BRANCH_PR_MERGE`
- `PUBLICATION_STATE_CHANGED`
- `TOOL_FAILURE`
- `WORKSPACE_CHECKPOINT`

The runtime accepts uppercase snake-case event types rather than imposing a closed substantive taxonomy.

## 7. Checkpoint current state

```bash
python3 scripts/workspace_persistence.py checkpoint \
  --workspace-id PD-WS-20260901-0003 \
  --summary "Runtime checkpoint" \
  --status DELETION_SAFE_WITH_OPEN_WORK \
  --objective "Operate the private vault and prepare the event-sourced client" \
  --completed "Append-only runtime implemented" \
  --open-task "Connect a durable private filesystem or API adapter" \
  --next-action "Reconcile current main before the next change" \
  --do-not-infer "Public GitHub contains raw private conversations"
```

For a richer checkpoint:

```bash
python3 scripts/workspace_persistence.py checkpoint \
  --workspace-id PD-WS-20260901-0003 \
  --payload examples/workspace-checkpoint.example.json
```

A checkpoint appends an immutable event and regenerates `state.json` and `handoff.md`. The event chain—not the generated handoff—is the chronological authority.

## 8. Validate integrity

```bash
python3 scripts/workspace_persistence.py validate
```

Or one workspace:

```bash
python3 scripts/workspace_persistence.py validate \
  --workspace-id PD-WS-20260901-0003
```

Validation checks sequence numbers, workspace identity, content hashes, event hashes, previous-event hashes and state/event reconciliation. Editing an earlier event is detected.

## 9. Export an expressly approved public checkpoint

Raw private state never flows automatically into public `por-derecho`.

A public export is permitted only when private `state.json` contains an explicit `public_summary` object:

```bash
python3 scripts/workspace_persistence.py public-summary \
  --workspace-id PD-WS-20260901-0003 \
  --output /path/to/public-repo/archive/checkpoints/PD-WS-20260901-0003.json
```

The derivative contains only the approved summary, workspace ID, generation time and source event hash. It excludes the raw event stream and remains subject to normal review/merge governance.

## 10. Import existing ChatGPT history privately

An authorised ChatGPT account export may contain `conversations.json`. Keep both source and normalized output private.

```bash
python3 scripts/workspace_persistence.py import-chatgpt \
  --source /secure/path/chatgpt-export.zip \
  --batch-id PD-CGX-20260901-initial
```

Default behavior:

- normalizes visible `user` and `assistant` messages;
- preserves conversation/node/parent identifiers and hashes;
- does not print message content;
- excludes system/tool messages unless `--include-system` is deliberately used;
- creates a clustering queue instead of declaring every historical thread a separate workspace;
- marks the import `PRIVATE_ONLY_DO_NOT_PUBLISH`; and
- does not copy the original export unless `--copy-source` is supplied.

After import, cluster related conversations into stable workspaces and reconcile stale chat state against current repository truth before deriving any public checkpoint.

## 11. Visibility classes

Every private event uses one of:

- `PUBLIC_SOURCE_SAFE`
- `PUBLIC_DERIVED_SAFE`
- `PRIVATE_WORKSPACE`
- `CONFIDENTIAL_USER_SUPPLIED`
- `CONNECTED_SOURCE_RESTRICTED`
- `PUBLICATION_REVIEW_REQUIRED`

Visibility is a handling classification, not proof or a merits judgment. Even public-safe events are not bulk-exported: `public-summary` still requires explicit approval.

## 12. Recommended backup arrangements

### Private Git repository

A scheduled local job can validate and commit the vault:

```bash
python3 /path/to/por-derecho/scripts/workspace_persistence.py validate

git -C "$PD_WORKSPACE_VAULT" add --all
git -C "$PD_WORKSPACE_VAULT" commit -m "workspace checkpoint" || true
git -C "$PD_WORKSPACE_VAULT" push
```

Use an operating-system credential manager or narrowly scoped GitHub App/token. Never place credentials in public Git or event details.

### Synchronized encrypted directory

A synchronized Drive directory is viable when it provides a local filesystem and atomic rename semantics. Avoid concurrent writers to one workspace unless a stronger shared lock/transaction layer is introduced.

### Private GitHub Issue fallback

A private-repository issue can serve as a checkpoint ledger but not as the complete binary/event vault. Never use a public issue for confidential workspace material.

## 13. Continuous assistant checkpoint policy

Under `PD-AWP-001`, a persistence-capable assistant should checkpoint after:

- a material factual correction or analytical decision;
- an identity/caret reconciliation;
- a source, proceeding or artifact registration;
- a branch, PR, merge, deployment or route verification;
- a filing/publication readiness transition;
- a material attribution/privacy-boundary change;
- a workspace-ID collision or correction;
- a tool failure changing safe assumptions; or
- an instruction to preserve, interlink, publish, make deletion-safe or continue in another thread.

This narrows the loss window. It cannot make an unobserved ChatGPT thread visible to GitHub.

## 14. Genuine zero-touch phase

The target end-state is a Por Derecho workbench in which persistence sits in the request path:

```text
user-visible input
  -> private event append
  -> model request
  -> user-visible response append
  -> tool/repository event append
  -> state/handoff refresh
```

That phase requires an OpenAI API-backed application, private storage and GitHub integration. It must not be configured with a fabricated key or silently reuse credentials. The current runtime and schemas are intended to be reused by that client.

## 15. CI enforcement

`.github/workflows/audit-workspace-persistence.yml` performs:

- Python compilation;
- runtime tests;
- repository-control validation;
- duplicate workspace-ID and handoff-path checks;
- `.gitignore` privacy-marker validation; and
- upload of a public, read-only audit result.

CI never opens or validates the real private vault.

## 16. Recovery rules

- Never repair a broken event chain by editing historical hashes.
- Preserve a damaged copy, identify the last valid event and create a recovery/supersession record.
- Never replace a full-resolution binary with a derivative under the same artifact reference.
- Never equate chat text with proof of an external fact.
- Never infer that repository publication means filing, service, authority receipt or social posting.
- Never allow imported historical chat state to overwrite newer canonical repository state without explicit reconciliation.
- Never let a concurrent workspace overwrite an ID or handoff already registered on current `main`.

## 17. Current implementation boundary

Implemented:

- `PD-WS-*` registry and deletion-safe handoff framework;
- private append-only event runtime;
- integrity validation;
- private ChatGPT-export importer;
- explicit public-summary gate;
- schemas, tests and CI;
- owner-only/not-shared Google Drive vault structure; and
- a validated private seed snapshot for `PD-WS-20260901-0003`.

Still open:

- connecting the Python runtime to a durable synchronized filesystem or Drive/object-store adapter;
- scheduled private backups;
- authorised historical export import and workspace clustering; and
- the OpenAI API request-path workbench required for genuine automatic capture of every interaction made through that client.
