# Por Derecho workspace persistence runbook

**Runtime:** `scripts/workspace_persistence.py`  
**Governance:** `PD-AWP-001` + `PD-WCH-001`  
**Current implementation level:** private append-only runtime and public continuity controls; no native all-ChatGPT-thread webhook is claimed.

## 1. Operating model

A ChatGPT thread is a temporary working surface. A `PD-WS-*` workspace is the durable continuity object.

The runtime provides:

- stable workspace identities;
- append-only JSONL events;
- SHA-256 content hashes;
- a previous-event hash chain;
- atomic state and handoff regeneration;
- explicit visibility classes;
- refusal to place a private vault inside the public `por-derecho` checkout;
- controlled public-summary export;
- private normalization of an authorised ChatGPT data export; and
- repository/CI validation of the public continuity layer.

It does **not** claim that ordinary ChatGPT exposes a guaranteed hook for every new thread, every turn, app close or deletion. Genuine zero-touch capture requires a client/workbench that owns the request path.

## 2. Choose the private vault

The vault must be outside the public repository.

Suitable locations include:

- a checkout of a separate **private** GitHub repository;
- an encrypted local directory backed up to private storage;
- an encrypted directory synchronized through a private cloud account; or
- a private object-store/database integration built around the same event schema.

Do not point the runtime at `sbu001monterecco/por-derecho` or any subdirectory of it.

### Linux/macOS example

```bash
export PD_WORKSPACE_VAULT="$HOME/por-derecho-workspaces-private"
python3 scripts/workspace_persistence.py doctor
```

### PowerShell example

```powershell
$env:PD_WORKSPACE_VAULT = "$HOME\por-derecho-workspaces-private"
python scripts/workspace_persistence.py doctor
```

`doctor` creates only the private vault marker and confirms that the destination is outside the public repository. It does not read an OpenAI API key or GitHub token.

## 3. Initialise or recover a workspace

```bash
python3 scripts/workspace_persistence.py init \
  --workspace-id PD-WS-20260901-0002 \
  --title "Automatic workspace persistence runtime" \
  --objective "Implement continuous, privacy-separated workspace capture" \
  --repository sbu001monterecco/por-derecho \
  --baseline 89e84ffd6656a37951565d769f5eee4214661e37
```

Omit `--workspace-id` to allocate the next local daily sequence. Use `--resume` only to recover an existing workspace; it never overwrites the event chain.

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

## 4. Append a material event

```bash
python3 scripts/workspace_persistence.py append \
  --workspace-id PD-WS-20260901-0002 \
  --event-type BRANCH_PR_MERGE \
  --summary "Persistence runtime PR merged" \
  --visibility PRIVATE_WORKSPACE \
  --repository-ref "sbu001monterecco/por-derecho#PR" \
  --details-json '{"state":"MERGED_TO_MAIN"}'
```

Appropriate event types include:

- `MATERIAL_DECISION`
- `FACT_CORRECTED`
- `IDENTITY_RECONCILED`
- `SOURCE_REGISTERED`
- `ARTIFACT_REGISTERED`
- `BRANCH_PR_MERGE`
- `PUBLICATION_STATE_CHANGED`
- `TOOL_FAILURE`
- `WORKSPACE_CHECKPOINT`

Event types are uppercase snake case. The runtime remains flexible rather than imposing a closed legal taxonomy.

## 5. Checkpoint current state

For a compact checkpoint:

```bash
python3 scripts/workspace_persistence.py checkpoint \
  --workspace-id PD-WS-20260901-0002 \
  --summary "Runtime implementation checkpoint" \
  --status DELETION_SAFE_WITH_OPEN_WORK \
  --objective "Operate the private vault and prepare the event-sourced client" \
  --completed "Append-only runtime implemented" \
  --open-task "Create or select the durable private vault destination" \
  --next-action "Initialise the real private workspace vault" \
  --do-not-infer "Public GitHub contains raw private conversations"
```

For a richer checkpoint, use a JSON file:

```bash
python3 scripts/workspace_persistence.py checkpoint \
  --workspace-id PD-WS-20260901-0002 \
  --payload examples/workspace-checkpoint.example.json
```

A checkpoint appends an immutable event and regenerates `state.json` and `handoff.md`. The event chain, not the generated handoff, is the chronological authority.

## 6. Validate integrity

```bash
python3 scripts/workspace_persistence.py validate
```

To validate one workspace:

```bash
python3 scripts/workspace_persistence.py validate \
  --workspace-id PD-WS-20260901-0002
```

Validation checks sequence numbers, workspace identity, content hashes, event hashes, previous-event hashes and state/event reconciliation. Any edit to an earlier event is detected.

## 7. Export an expressly approved public checkpoint

Raw private state never flows automatically into `por-derecho`.

A public export is permitted only when `state.json` contains an explicit `public_summary` object. Then run:

```bash
python3 scripts/workspace_persistence.py public-summary \
  --workspace-id PD-WS-20260901-0002 \
  --output /path/to/public-repo/archive/checkpoints/PD-WS-20260901-0002.json
```

The output contains only the approved `public_summary`, workspace ID, generation time and source event hash. It does not include the raw event stream.

Review and merge that derivative through the normal public-repository process.

## 8. Import existing ChatGPT history privately

ChatGPT account exports may include `conversations.json`. Keep the export and normalized results private.

```bash
python3 scripts/workspace_persistence.py import-chatgpt \
  --source /secure/path/chatgpt-export.zip \
  --batch-id PD-CGX-20260901-initial
```

Default behavior:

- extracts/normalizes visible `user` and `assistant` messages;
- preserves conversation/node/parent relationships and hashes;
- does not print message content to the terminal;
- excludes system/tool messages unless `--include-system` is deliberately used;
- creates a clustering queue rather than pretending every historical thread is a separate workspace;
- marks all imported material `PRIVATE_ONLY_DO_NOT_PUBLISH`; and
- does not copy the source ZIP unless `--copy-source` is explicitly supplied.

After import, review the clustering queue and assign related conversations to stable `PD-WS-*` workspaces. Reconcile old conversation state against current repository truth before deriving any public checkpoint.

## 9. Visibility classes

Every event must use one of:

- `PUBLIC_SOURCE_SAFE`
- `PUBLIC_DERIVED_SAFE`
- `PRIVATE_WORKSPACE`
- `CONFIDENTIAL_USER_SUPPLIED`
- `CONNECTED_SOURCE_RESTRICTED`
- `PUBLICATION_REVIEW_REQUIRED`

Visibility is a handling instruction, not a merits or evidential classification.

Only `PUBLIC_SOURCE_SAFE` and `PUBLIC_DERIVED_SAFE` may be candidates for governed public synchronization. The runtime still requires an explicit `public_summary`; it does not bulk-export events based only on the label.

## 10. Recommended automation around the runtime

### Separate private Git repository

Use the vault directory as a checkout of a private repository. A local scheduled job may run:

```bash
python3 /path/to/por-derecho/scripts/workspace_persistence.py validate

git -C "$PD_WORKSPACE_VAULT" add --all
git -C "$PD_WORKSPACE_VAULT" commit -m "workspace checkpoint" || true
git -C "$PD_WORKSPACE_VAULT" push
```

Do not place credentials in the public repository or in event details. Use the operating system credential manager or a narrowly scoped GitHub App/token appropriate to the private repository.

### Encrypted synchronized directory

The runtime can write to an encrypted local directory synchronized by a private storage provider. Ensure the local filesystem provides atomic rename semantics and that concurrent writers are not operating on the same workspace without coordination.

### Private GitHub Issue fallback

A private repository issue can act as a checkpoint ledger, but it is not a replacement for the raw JSONL/binary vault. Never use a public issue for confidential workspace material.

## 11. Continuous checkpoint policy for assistant-led work

Under `PD-AWP-001`, a persistence-capable assistant should checkpoint after:

- a material factual correction or analytical decision;
- a new identity/caret reconciliation;
- a source, proceeding or artifact registration;
- a branch, PR, merge, deployment or route verification;
- a filing/publication readiness transition;
- a material attribution or privacy-boundary change;
- a tool failure that changes safe assumptions; or
- an instruction to preserve, interlink, publish, make deletion-safe or continue in another thread.

This narrows the loss window, but it cannot make an unobserved ChatGPT thread visible to GitHub.

## 12. Genuine zero-touch phase

The target end-state is a Por Derecho workbench in which persistence sits in the request path:

```text
user-visible input
  -> private event append
  -> model request
  -> user-visible response append
  -> tool/repository event append
  -> state/handoff refresh
```

That phase requires an OpenAI API-backed application, private storage and GitHub integration. It should not be scaffolded with a fake key or silently reuse credentials. When implementation begins, make a deliberate credential decision and keep secrets outside Git.

The existing runtime and schemas are intended to be reused by that client rather than replaced.

## 13. CI enforcement

`.github/workflows/audit-workspace-persistence.yml` performs:

- Python compilation;
- five runtime tests;
- repository-control validation;
- `.gitignore` privacy-marker validation; and
- upload of the public, read-only audit result.

CI never opens or validates a real private vault.

## 14. Recovery rules

- Never repair a broken event chain by editing historical hashes.
- Preserve the damaged copy, identify the last valid event, and create a recovery/supersession event in a new chain or restored trusted copy.
- Never replace a full-resolution binary with a derivative under the same artifact reference.
- Never equate chat text with proof of an external fact.
- Never infer that repository publication means filing, service, authority receipt or social-media posting.
- Never allow imported historical chat state to overwrite a newer canonical repository record without explicit reconciliation.

## 15. Current implementation boundary

Implemented now:

- governed `PD-WS-*` workspace registry;
- deletion-safe handoff framework;
- private append-only event runtime;
- integrity validation;
- private ChatGPT-export importer;
- explicit public-summary gate;
- schemas, tests and CI.

Still requiring an external/private destination decision:

- creation of the durable private vault repository/storage account;
- scheduled encrypted/private backup credentials; and
- the OpenAI API request-path workbench for truly automatic capture of every interaction made through that client.
