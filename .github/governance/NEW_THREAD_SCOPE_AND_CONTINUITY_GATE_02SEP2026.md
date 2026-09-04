# Mandatory new-thread scope and continuity gate

**Date:** 2 September 2026  
**Coordination update:** 4 September 2026 — `PD-MTCP-20260904-01`  
**Applies to:** every new ChatGPT Chat, ChatGPT Work thread, Codex thread, or other agent thread started by Gil Marer where Por Derecho / Project Sun Rock may be in scope, or where the thread has access to this repository/workspace.

## 4-Sep-2026 multi-thread coordination override

Before the gate below is applied to related work, read:

- `.github/governance/MULTI_THREAD_COLLABORATION_AND_PUBLICATION_V2_04SEP2026.md`;
- `ops/CURRENT_STATE.json` for repository/deployment/rollback operational truth;
- `ops/CURRENT_COLLABORATION_STATE.json` for concurrent-thread/integration routing; and
- GitHub Issue #1428, the **Control Tower — Multi-thread integration queue**.

For related work, the default thread role is now `WORKER`. Parallel research/analysis is allowed, but only one active integrator/publication lane may exist at a time. A worker preserves a structured canonical delta and **does not independently publish**. A related existing thread may be activated without restarting: refresh current `main`, apply `PD-MTCP-20260904-01`, determine whether it is worker or active integrator, and reconcile its unique work against current canonical state.

Pre-control open PRs remain preserved but default to `LEGACY_BACKLOG` until explicitly reactivated/reconciled. Historical handovers remain provenance; do not create another whole-project handover when the thread's unique material can be stored directly in canonical registers/issues.

This coordination layer changes workflow only. It does not weaken any evidential, privacy, identity, legal-person separation, preservation, publication-authority or external-action boundary below.

## Controlling purpose

A new thread must not silently assume either continuity or non-continuity. Its first substantive action is a scope-and-continuity gate.

This gate exists so that related work starts from the durable current project state rather than chat memory, while genuinely unrelated work remains cleanly separated from Por Derecho / Project Sun Rock material.

## Gate A — potentially related, related, or uncertain

If the user's opening request is related to, may overlap with, or cannot safely be distinguished from Por Derecho / Project Sun Rock, the thread must, before substantive analysis or implementation:

1. state that Por Derecho / Project Sun Rock continuity governance is active for the thread;
2. fetch and identify the current remote `main` SHA for `sbu001monterecco/por-derecho`;
3. confirm that current `main`, not a predecessor chat, stale workspace, handover, branch or remembered summary, is the repository source of truth;
4. read `AGENTS.md`, `CHATGPT_START_HERE.md`, this gate, `PD-MTCP-20260904-01`, `ops/CURRENT_STATE.json`, `ops/CURRENT_COLLABORATION_STATE.json`, the universal publication/thread-deletion protocol and the specialist controls relevant to the task;
5. read Issue #1428 and the relevant task issue, if one exists, then determine `WORKER` versus active integrator role;
6. preserve the existing identity, proceeding, event, evidence, communication and route registers rather than creating parallel records;
7. re-query authorised private source systems when private evidence is needed instead of reconstructing it from public Git history or chat memory; and
8. only then continue the substantive task.

The thread should give the user a short confirmation that this bootstrap has been completed. It must not ask the user to repeat information that is already recoverable from current `main`, the canonical registers or authorised connected sources.

## Gate B — apparently unrelated

If the opening request appears completely unrelated to Por Derecho / Project Sun Rock, the thread must not simply assume that conclusion.

Before importing any Por Derecho substantive context, it must tell Gil Marer in substance:

> This appears to be unrelated to Por Derecho / Project Sun Rock and I will keep that matter's substantive context out of this thread. Please confirm that this thread is unrelated.

Until Gil confirms, classify the thread as `APPARENTLY_UNRELATED_AWAITING_CONFIRMATION` and do not import substantive Por Derecho allegations, evidence, actors, proceedings or strategy into the task merely because they are available in memory or connected sources.

After Gil confirms that it is unrelated, record the working scope as `CONFIRMED_UNRELATED` for that thread and proceed normally with the unrelated task. Repository continuity bootstrapping is then unnecessary unless the user later brings Por Derecho / Project Sun Rock into scope.

If Gil says the thread is related, or if a material overlap becomes apparent later, immediately switch to Gate A before continuing the overlapping work.

## No unnecessary interruption rule

The gate is a first-turn scope control, not a recurring interruption. Once scope has been confirmed for a thread, do not repeatedly ask the same question. Continue the work of that thread under the confirmed scope unless the user changes it or a material overlap emerges.

## Chat / Work / repository hierarchy

For related work, the durable hierarchy is now:

`current remote main -> ops/CURRENT_STATE.json (operational truth) + ops/CURRENT_COLLABORATION_STATE.json (coordination truth) -> Issue #1428 / task issue -> canonical repository controls/registers -> authorised connected private sources where required -> worker delta -> single integration lane -> validation -> merge -> deployment/live verification`.

Chat memory, Work context, prior-thread summaries and historical handovers may accelerate retrieval but are not preservation or completion authorities.

For unrelated work, do not contaminate the thread with Por Derecho substantive material after the user confirms separation.

## Deletion and handover consequence

A related working thread becomes deletion-safe when every unique material decision, correction, source, limitation, open gap and recovery instruction has escaped the thread into the appropriate durable canonical state or task issue. Under `PD-MTCP-20260904-01`, a bespoke whole-project handover is not required when that canonical delta is complete.

An unrelated thread does not need a Por Derecho continuity closeout unless it later entered the Por Derecho perimeter.

## Machine-style states

Scope states:

- `RELATED_CONTINUITY_ACTIVE`
- `POTENTIALLY_RELATED_CONTINUITY_ACTIVE`
- `APPARENTLY_UNRELATED_AWAITING_CONFIRMATION`
- `CONFIRMED_UNRELATED`
- `SCOPE_CHANGED_TO_RELATED_CONTINUITY_ACTIVE`

Coordination role states:

- `WORKER`
- `ACTIVE_INTEGRATOR`
- `LEGACY_BACKLOG`
- `READY_TO_INTEGRATE`
- `BLOCKED_SOURCE_GAP`
- `RESEARCH_ONLY`
- `SUPERSEDED_BY_MAIN`

These states control workflow only. They do not create or alter evidential propositions, legal positions, publication authority or third-party contact authority.
