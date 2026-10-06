# Thread Deletion-Safety Sentinel

**Control ID:** PD-THREAD-SENTINEL-20260925-01  
**Status:** ACTIVE / MANDATORY / FAIL-CLOSED  
**Applies to:** Por Derecho / Project Sun Rock substantive ChatGPT chats, ChatGPT Work sessions, repository implementation threads, source-ingest threads, filing-preparation threads and material connected-source investigations.

## Purpose

Repeated bespoke “continuity and preservation audits” are replaced by one continuously maintained thread state.

Every substantive thread must carry exactly one current deletion-safety sentinel:

- **🟢 GREEN — SAFE TO DELETE**
- **🟠 ORANGE — PRESERVATION PENDING**
- **🔴 RED — DO NOT DELETE**

The sentinel is a compact reader cue. It is not the underlying evidence. Its state must be reconstructable from durable controls outside the chat.

## Required visible cue

For every substantive assistant response in scope, show one compact final line:

`🟢 THREAD — safe to delete`

or

`🟠 THREAD — preservation pending · <short reason>`

or

`🔴 THREAD — do not delete · <short blocker>`

The cue should remain visually small. Do not turn every response into a full deletion audit.

A user may ask for the detailed basis at any time. A full closeout record is normally required only when moving to GREEN or when a RED blocker needs durable incident treatment.

## State semantics

### 🟢 GREEN — SAFE TO DELETE

GREEN means deletion of the originating chat is not expected to cause loss of material project continuity or interrupt an active operation.

GREEN requires, as applicable:

1. no unique substantive source, reasoning, correction, limitation, recovery instruction, generated artifact or source locator remains only in the chat/session/worktree;
2. material developments have been propagated to the controlling chronology/registers and any required private Drive control;
3. repository work is recoverable from remote source and merged/read back where merge is part of the task;
4. publication work has the deployment/live-readback evidence required by the universal publication protocol;
5. open gaps and unfinished actions are durably recorded with their state, owner/next action and source boundary;
6. connected-source originals remain in their native systems or controlled custody;
7. no scheduled task, automation, pending action or other operational dependency is attached to the chat in a way that deletion would pause, cancel or orphan it;
8. no unresolved file-expiry/re-upload dependency means the thread contains the only usable copy;
9. the latest sentinel basis has been read back from at least one durable private/control surface independent of the chat.

GREEN does **not** mean the underlying case, investigation, filing, publication programme or evidence set is complete. Open work may remain if its state and continuation path are durably preserved.

### 🟠 ORANGE — PRESERVATION PENDING

ORANGE is the default state for a new substantive thread and for work whose deletion safety has not yet been objectively established.

Typical ORANGE conditions:

- work is still being developed;
- a repo branch/PR/MR exists but merge/readback is incomplete;
- cross-host parity is incomplete but recoverable source exists;
- a private Drive checkpoint has not yet been updated/read back;
- a material new source has been identified but propagation is incomplete;
- an external action is pending and its durable continuation record is incomplete;
- a full deletion-safety check has not yet been run after material changes.

ORANGE means: **archive if desired; do not permanently delete yet.**

ORANGE is not a danger claim. It means continuity is not yet certified.

### 🔴 RED — DO NOT DELETE

RED is mandatory where deletion would itself create a credible material loss, interruption or orphaned dependency.

RED triggers include:

- a unique material source, upload, generated artifact, correction, recovery instruction or exact package exists only in the chat/session/local worktree;
- an attached/scheduled automation or task would be paused, cancelled or lose its operating context if the chat were deleted;
- a material native source is inaccessible elsewhere and the chat contains the only usable representation;
- an external filing/send/action has occurred but its exact native receipt/readback has not been preserved anywhere else;
- an important file is expired/unavailable and has not been reacquired while the chat contains the only remaining usable content;
- deletion would remove the only known source locator, credential-free retrieval route or preservation instruction for a material record;
- a failed or uncertain deployment, transfer or write leaves recovery dependent on this chat.

RED means: **do not delete; preserve or detach the blocker first.**

## Automatic state transitions

Every substantive thread begins at ORANGE unless a controlling durable record already proves GREEN.

Reassess the sentinel whenever any of the following occurs:

- a material file/source is uploaded or located;
- an external send, filing, publication, merge, deployment or Drive write occurs;
- a scheduled task/automation is created, moved, paused or removed;
- a material correction or contradiction is accepted;
- a repository or Drive preservation/readback gate completes or fails;
- a connected-source item becomes inaccessible or expires;
- the user asks whether the thread can be deleted;
- the assistant is about to recommend closing/archive/deleting the thread.

A state may move backwards immediately when contradictory evidence or a new dependency appears.

## Relationship to existing controls

This sentinel is the front-end state of, and does not replace:

- `archive/UNIVERSAL_PUBLICATION_AND_THREAD_DELETION_SAFETY_PROTOCOL_18AUG2026.md`;
- `ops/continuity/CONTINUITY_PRESERVATION_PROPAGATION_RULE.md`;
- `.github/governance/CONSEQUENCE_RISK_COMMUNICATION_CONTROL_25SEP2026.md`;
- repository preservation, publication-integrity, source-custody and email-authorisation controls.

Where the underlying protocol requires stronger evidence than this file, the stronger requirement controls.

## ChatGPT-level behavior

The assistant cannot add a native persistent badge to the ChatGPT product UI. Therefore the project convention is the compact final-line cue above.

The cue must be computed from current evidence, not remembered optimistically from an earlier turn.

Do not claim GREEN because:
- a prior assistant said “safe”;
- a branch or PR exists;
- a file was once written;
- CI passed on an old head;
- the user says the work “should already be preserved”;
- a task appears in an automation list without checking whether deletion of this chat affects it.

When a connector or repository needed to verify the state is unavailable, use ORANGE unless a known RED trigger exists.

## GitHub / GitLab rule

Git stores the public-safe policy, schema, validators and durable public-safe closeout records.

Do not store raw private chat content merely to obtain GREEN.

A thread-level closeout record should state:
- sentinel state;
- date;
- scope;
- relevant repository heads/merge receipts where material;
- private Drive/checkpoint reference where appropriate;
- remaining open work;
- any automation/task dependency;
- reason the thread can or cannot be deleted.

Repository divergence is ORANGE unless deletion would make reconciliation materially impossible, in which case it is RED.

## Google Drive rule

Private Drive is the preferred operational continuity layer for:
- exact private source locators;
- active thread-safety dashboard;
- private alert/deadline/action state;
- automation dependencies;
- thread closeout receipts that should not be public.

The Drive dashboard must not become the sole copy of native evidence.

## Minimal decision algorithm

Evaluate in this order:

1. **Loss/interruption test:** would deletion lose unique material or pause/orphan an active operation?  
   - yes → RED.
2. **Certification test:** are all required preservation/propagation/readback gates complete?  
   - no → ORANGE.
3. **Independence test:** can a fresh thread reconstruct the material state and continue without this chat?  
   - no → ORANGE or RED depending on whether the deficit is recoverable.
4. all applicable tests passed → GREEN.

## Anti-fragmentation rule

Do not create a new bespoke deletion doctrine for each thread.

Thread-specific audits may add facts, but they must resolve to this one tri-state sentinel and preserve the existing universal protocol.

## Canonical maxim

> **RED means deletion causes harm. ORANGE means deletion safety is not yet proved. GREEN means the work can continue without the chat.**
