# UNIVERSAL PUBLICATION + THREAD-DELETION SAFETY PROTOCOL

**Date:** 18 August 2026  
**Scope:** all Por Derecho / Project Sun Rock implementation threads, branches, PRs, publication records and deployment claims.

## Controlling rule

No execution thread is authoritative about its own completion.

The evidence authorities are:

1. **Git tree** — source preservation;
2. **CI** — reproducible validation;
3. **`main`** — merge status;
4. **public host** — deployment/live status;
5. **post-deployment continuity record** — deletion safety.

Thread narration, a spinner, a local worktree, a local test, a partial encoded payload, a branch name, or a publication marker is never sufficient evidence of `MERGED`, `DEPLOYED`, `LIVE VERIFIED` or `DELETION SAFE`.

## Canonical state machine

`DRAFT → REMOTE_SOURCE → PR_OPEN → CI_GREEN → MERGED → DEPLOYED → LIVE_VERIFIED → DELETION_SAFE`

`BLOCKED_RECOVERY` is a permitted exceptional state where work is known to exist or be intended but the complete recoverable source is not yet safely present in remote Git.

A state may only move forward when its objective gate has passed. It may move backwards immediately when contradictory evidence appears.

## Mandatory publication manifest

Material publication work should have a JSON record under `publication-manifests/` containing at minimum:

- `publication_id`;
- `owner`;
- `current_state`;
- exact ES/EN route inventory;
- expected source files where applicable;
- validation evidence for `CI_GREEN+`;
- merge SHA for `MERGED+`;
- deployment evidence for `DEPLOYED+`;
- public URLs and independent verification evidence for `LIVE_VERIFIED+`;
- deletion record for `DELETION_SAFE`.

The manifest is an assertion that the repository can test. It is not itself proof.

## Atomic-source rule

Normal publication work must commit the **actual reviewable source files** to the remote branch before substantive review.

Do not use encoded `.b64`, tar/zip fragments, CI self-materialisation, temporary files or chat/session state as the only recoverable copy of substantive work.

An encoded bootstrap is exceptional and temporary. If used, its manifest must declare:

- exact glob;
- exact part count;
- `complete: true` only when all parts are already remote;
- a deterministic hash;
- a finite migration to ordinary source files.

An incomplete encoded bootstrap is `BLOCKED_RECOVERY`, never `REMOTE_SOURCE` or later.

## Forbidden completion shortcuts

The publication-integrity gate rejects newly changed placeholder/temp artefacts such as `.tmp`, `NOOP.tmp` and `SHOULD_NOT_EXIST.tmp`.

It also rejects partial encoded payloads unless the relevant publication manifest explicitly declares the bootstrap complete and the actual remote part count exactly matches the declared count.

## Bilingual route rule

Where a publication declares ES/EN parity, the manifest must enumerate both route sets. From `REMOTE_SOURCE` onward every declared route must exist as an actual repository file. Route counts must match unless the manifest expressly models a non-bilingual publication.

## CI gate

`.github/workflows/publication-integrity-gate.yml` runs on PRs to `main` and pushes to `main`.

It checks:

- manifest schema/state;
- expected route/source existence;
- bilingual route parity;
- forbidden temporary files;
- incomplete encoded bootstrap publication;
- evidence prerequisites for advanced states.

A publication must not claim `CI_GREEN` unless its own substantive validator and this universal integrity gate have passed.

## Live verification gate

Repository presence and merge do not establish deployment.

After Pages deployment, run `.github/workflows/verify-publication-live.yml`. A publication may move to `LIVE_VERIFIED` only when the public URL(s) return successfully and the declared live markers are observed on the host.

## Thread-deletion gate

A working thread is **not deletion-safe** merely because its branch or PR exists.

`DELETION_SAFE` requires, at minimum:

- recoverable source in remote Git;
- finite expected-file/route inventory;
- reproducible validation evidence;
- merge/deployment/live evidence where publication was part of the task;
- preserved open gaps and evidential limitations;
- no unique substantive source remaining only in the originating chat/session/worktree;
- a final continuity record written after the above gates.

If any unique payload, source file, evidential map, local validation output or recovery instruction remains only in the originating thread/environment, the correct state is `BLOCKED_RECOVERY`.

## DIP 80/2026 first migration case

PR #352 exposed the motivating failure mode. The intended 14-route DIP 80 casebook was described as complete locally, while the remote materialisation process required nine encoded parts and had only a partial payload available during repeated failed workflow runs.

Until the complete ordinary source is present and independently validated, DIP 80 must be treated as `BLOCKED_RECOVERY` irrespective of earlier prose saying `published`, `merged`, `live` or `deletion-safe`.

The preferred repair is not indefinite chunk-by-chunk CI reconstruction. Recover the complete source, commit the actual files atomically from current `main`, validate the 14 routes and interaction/data layers, merge through a reviewable PR, verify Pages, and only then close the deletion gate.

## Canonical maxim

> **Git proves preservation. CI proves reproducibility. `main` proves merge. The public host proves deployment. Only the complete chain can prove deletion safety.**
