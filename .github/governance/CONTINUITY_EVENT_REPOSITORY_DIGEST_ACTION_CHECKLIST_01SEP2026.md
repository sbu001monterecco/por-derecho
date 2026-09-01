# Continuity event repository-digest action checklist — 1 September 2026

**Control ID:** `PD-CONT-DIGEST-001`  
**Status:** active continuity/checkpoint governance  
**Scope:** every substantive workspace checkpoint, handoff, deletion-safety event, publication closeout, identity correction or other durable continuity event.

## 1. Governing rule

A continuity event is not complete merely because a narrative summary was written. Every substantive continuity event must carry a finite **action ledger** showing what was inspected, what was changed, what remains open and what a successor must do next.

The action ledger is required so that a future thread can distinguish:

- work actually performed;
- repository/GitHub state merely inherited;
- connected-source scans actually run;
- safe repairs completed;
- publication/live checks actually performed; and
- open tasks or evidence gaps that still require action.

## 2. Mandatory action-list fields

Every substantive continuity record must include the following, either directly or through an explicitly linked machine record:

### A. `repository_digest_actions`
A finite list of repository/GitHub inspection actions actually performed, including where applicable:

1. re-fetch current `main` and record the exact SHA;
2. read the current workspace index/handoff and relevant specialist handoffs;
3. digest controlling governance and machine registers;
4. inspect materially relevant prior PRs/merges/closeouts rather than relying on chat assurances;
5. inspect canonical identity, proceedings, evidence, chronology, relationship and media registers implicated by the event;
6. inspect public routes/manifest/deployment state where publication is in scope; and
7. identify stale, superseded or contradictory repository state.

### B. `connected_source_actions`
List each authorised connected-source scan actually run — for example Gmail, Drive or another connected source — with the search scope and the source-status limit. A repository mention of an email is not a substitute for a Gmail scan when the task specifically calls for current email reconstruction and the connector is available.

### C. `registration_and_identity_actions`
For every new material person/entity/proceeding/evidence/media object:

- run the applicable `^` registration/audit;
- identify the canonical or proposed stable ID/key;
- record aliases/collisions;
- distinguish legal person from brand/perimeter/trading name;
- record exact source/provenance; and
- state `CARET_CONFIRMED`, `CARET_PENDING`, `CARET_SUSPENDED`, `CARET_NOT_APPLICABLE` or the applicable non-CAEPR media/evidence identity state.

A GitHub file or prose mention does **not** automatically receive a CAEPR caret.

### D. `relationship_interlink_actions`
List the first-hop and material wider links checked or added:

- person ↔ firm/entity;
- person/entity ↔ event/source;
- event ↔ proceeding;
- event ↔ evidence/document;
- hotel/asset ↔ owner/manager/brand/financier/adviser;
- media object ↔ source portrait/logical asset/publication; and
- page ↔ canonical evidence/identity route.

Record missing backlinks as open actions rather than silently assuming discoverability.

### E. `chronology_and_proceedings_actions`
List the chronology/proceeding checks actually performed. Preserve exact procedural capacity and date. `NOT LOCATED` remains distinct from `DID NOT EXIST`.

### F. `publication_and_live_actions`
Where publication is in scope, separately record:

- source exists in repository;
- formal register/manifest inclusion;
- build/deploy status;
- exact Pages run/merge SHA when known;
- live route readback; and
- social/email publication state.

No one layer proves another.

### G. `completed_actions`
A finite list of repairs or durable outputs completed during the checkpoint.

### H. `open_actions`
A finite, prioritised list of unresolved items. Each item should identify the missing source/action, the reason it remains open and what would close it.

### I. `do_not_infer`
A compact list of the material boundaries a successor must preserve, including association/intent, identity/conduct, manager/owner, brand/title, financing/ownership, sent/received/read, and repository/published/live distinctions where relevant.

### J. `next_thread_bootstrap`
A copyable instruction naming the workspace ID, handoff and first files/actions a new thread must read/run.

## 3. Mandatory checkpoint sequence

For a substantive event, perform in this order where applicable:

`current main → workspace continuity → controlling governance → repository/GitHub digest → connected-source scan → ^ identity/registration → evidence/chronology/proceedings → relationship/interlink audit → publication/live state → completed/open action ledger → successor bootstrap`.

This sequence is a retrieval and continuity discipline, not permission to publish, contact or file externally.

## 4. Relationship to CAEPR `^`

This control complements the broader `^` user-command protocol. The `^` command is action + verification and already requires registration, identity, provenance, relationships, chronology, publication awareness, gap audit and continuity safety. `PD-CONT-DIGEST-001` adds one operational requirement: **the actions taken and the actions still open must be enumerated at every substantive continuity checkpoint.**

A displayed `Name^` continues to mean canonical identity resolution only. It never means that every repository digest action has been performed or that the person is responsible for any event.

## 5. Connected-source evidence boundary

A connected-source result proves only what the retrieved source supports. In particular:

- an outgoing Gmail item proves a sent-message record, not recipient reading or agreement;
- a bounce proves the delivery failure described by that bounce, not failure to every other recipient;
- CC placement proves addressing, not knowledge or action;
- an attachment filename/size proves the message carried that attachment metadata, not the truth of its content; and
- repetition across institutional emails does not transform a project allegation into a finding.

## 6. Pressure/publication work

Where a public campaign or high-pressure communication is prepared, the action ledger must distinguish:

- forceful documentary questions and preservation requests;
- source-supported factual statements;
- attributed allegations or investigative hypotheses; and
- prohibited/unproved claims of guilt, collusion, corruption, fraud or intentional concealment.

`MAX PRESSURE` means maximum specificity, traceability, unanswered-document focus and accountability — not fabrication, harassment or removal of evidential qualifications.

## 7. Deletion-safety test

A continuity event may be marked deletion-safe only if a successor can reconstruct, without the originating chat:

> current repository baseline → what was searched → what was found → what was registered → what was interlinked → what was published/live → what remains open → what to do next.

If any one of those materially affects the continuing task and exists only in chat, the event is not yet deletion-safe.
