# Mandatory new-thread scope and continuity gate

**Date:** 2 September 2026  
**Applies to:** every new ChatGPT Chat, ChatGPT Work thread, Codex thread, or other agent thread started by Gil Marer where Por Derecho / Project Sun Rock may be in scope, or where the thread has access to this repository/workspace.

## Controlling purpose

A new thread must not silently assume either continuity or non-continuity. Its first substantive action is a scope-and-continuity gate.

This gate exists so that related work starts from the durable current project state rather than chat memory, while genuinely unrelated work remains cleanly separated from Por Derecho / Project Sun Rock material.

## Gate A — potentially related, related, or uncertain

If the user's opening request is related to, may overlap with, or cannot safely be distinguished from Por Derecho / Project Sun Rock, the thread must, before substantive analysis or implementation:

1. state that Por Derecho / Project Sun Rock continuity governance is active for the thread;
2. fetch and identify the current remote `main` SHA for `sbu001monterecco/por-derecho`;
3. confirm that current `main`, not a predecessor chat, stale workspace, handover, branch or remembered summary, is the repository source of truth;
4. read `AGENTS.md`, `CHATGPT_START_HERE.md`, this gate, the universal publication/thread-deletion protocol and the specialist controls relevant to the task;
5. preserve the existing identity, proceeding, event, evidence, communication and route registers rather than creating parallel records;
6. re-query authorised private source systems when private evidence is needed instead of reconstructing it from public Git history or chat memory; and
7. only then continue the substantive task.

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

For related work, the durable hierarchy remains:

`current remote main -> canonical repository controls/registers -> authorised connected private sources where required -> implementation -> validation -> merge -> deployment/live verification -> continuity closeout`.

Chat memory, Work context, prior-thread summaries and historical handovers may accelerate retrieval but are not preservation or completion authorities.

For unrelated work, do not contaminate the thread with Por Derecho substantive material after the user confirms separation.

## Deletion and handover consequence

A related working thread becomes deletion-safe only when every unique material decision, correction, source, limitation, open gap and recovery instruction has escaped the thread into the appropriate durable canonical state and the applicable publication/deployment gates have been satisfied.

An unrelated thread does not need a Por Derecho continuity closeout unless it later entered the Por Derecho perimeter.

## Machine-style states

- `RELATED_CONTINUITY_ACTIVE`
- `POTENTIALLY_RELATED_CONTINUITY_ACTIVE`
- `APPARENTLY_UNRELATED_AWAITING_CONFIRMATION`
- `CONFIRMED_UNRELATED`
- `SCOPE_CHANGED_TO_RELATED_CONTINUITY_ACTIVE`

These states control workflow only. They do not create or alter evidential propositions, legal positions, publication authority or third-party contact authority.
