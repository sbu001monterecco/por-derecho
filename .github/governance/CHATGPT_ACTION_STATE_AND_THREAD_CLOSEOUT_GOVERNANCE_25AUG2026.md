# CHATGPT ACTION-STATE AND THREAD-CLOSEOUT GOVERNANCE

**Control date:** 25 August 2026  
**Status:** repository-wide companion to the universal thread-deletion protocol  
**Applies to:** ChatGPT/Codex research, repository, website, email, calendar, filing, institutional-communication and preservation work

## Purpose

Future threads must not confuse what was considered, prepared, authorised, executed or verified.

This control prevents recurrent errors such as:

- describing an existing page that was strengthened as newly created;
- describing a branch or PR as merged;
- describing a merge as deployed;
- describing a successful deployment as independently edge-verified;
- describing a prepared email as sent;
- describing a send-tool result as a verified correct sent package;
- describing an institutional receipt as acceptance or merits action; or
- treating a deliberate hold as failed execution.

It supplements `AGENTS.md`, `archive/THREAD_DELETION_CONTINUITY_PROTOCOL_16AUG2026.md` and `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`. It grants no authority for an external action.

## 1. Universal non-collapsible action states

Every material action should be recorded using the smallest accurate state:

| State | Meaning |
| --- | --- |
| `DISCOVERED` | the object, source, route, message or issue was located |
| `ANALYSED` | its meaning, status and limits were assessed |
| `PROPOSED` | an action was recommended but not prepared or executed |
| `PREPARED` | a concrete change/package exists but has not been authorised or executed |
| `AUTHORIZED` | the user authorised the defined external action and scope, subject to any controlling hard stop |
| `EXECUTED` | the external or repository action actually occurred |
| `VERIFIED` | independent action-specific evidence confirms the executed result and package/state |
| `HOLD` | a deliberate decision not to act until a defined trigger occurs |
| `NO_ACTION_REQUIRED` | review concluded that no present action is warranted |
| `BLOCKED` | a hard stop prevents action and the reason is identified |
| `FAILED` | an attempted action did not complete or did not produce the required result |
| `SUPERSEDED` | a later controlled action or decision replaced the earlier one |

No later-sounding state may be inferred from an earlier one.

`PREPARED != AUTHORIZED != EXECUTED != VERIFIED`.

## 2. Action-specific state machines

### Repository

Use:

`CURRENT_MAIN_CHECKED -> CHANGE_PREPARED -> COMMITTED_ON_BRANCH -> PR_OPEN -> MERGED`

Optional later states are:

`MERGED -> DEPLOYMENT_SUCCEEDED -> EDGE_VERIFIED`.

Rules:

- a local or connector-created file is not automatically on `main`;
- a branch commit is not an open PR;
- an open PR is not merged;
- a merged governance-only change is not necessarily a Pages change;
- a successful Pages workflow proves deployment of its head SHA, not a separate human/browser read-back; and
- `EDGE_VERIFIED` requires a current fetch or rendered check of the affected route, content marker and essential links.

### Website/page identity

Before promising or reporting a dedicated page, inspect the canonical route and classify one of:

- `NO_CANONICAL_PAGE_LOCATED`;
- `EXISTING_PAGE_REVIEWED_NO_CHANGE`;
- `EXISTING_PAGE_STRENGTHENED`;
- `NEW_PAGE_CREATED`;
- `ROUTE_REPAIRED_OR_REDIRECTED`;
- `MERGED_NOT_DEPLOYED`;
- `DEPLOYED_NOT_EDGE_VERIFIED`; or
- `EDGE_VERIFIED`.

Never use “created” as shorthand for a rewrite. Where the user asks for a dedicated page and one already exists, say so immediately and describe the actual operation.

### Email

`EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md` controls the hard stop. Its core sequence remains:

`PREPARED -> AUTHORIZED -> SENT -> VERIFIED`.

Non-transmission terminal states are:

- `HOLD — NOT SENT`;
- `NO RESPONSE REQUIRED — NOT SENT`;
- `BLOCKED — NOT SENT`; and
- `FAILED OR UNCERTAIN — NOT VERIFIED AS SENT`.

A deliberate hold is an executed strategic decision, not a failed send.

### Institutional correspondence

Use:

`SENT -> RECEIVED -> DOCKETED -> PROCEDURAL_ACTION -> SUBSTANTIVE_DECISION`.

Each step requires its own proof.

- `RECEIVED` may be proved by a receipt acknowledgement.
- `DOCKETED` requires an institutional file/reference or equivalent traceability evidence.
- `PROCEDURAL_ACTION` requires a notice, request, hearing step, transfer, opening order or comparable act.
- `SUBSTANTIVE_DECISION` requires the institution's operative decision and reasoning.

Never collapse `RECIBIDO` into admissibility, agreement, investigation, endorsement or resolution.

### Calendar/meeting

Use:

`PROPOSED -> AVAILABILITY_CHECKED -> EVENT_CREATED -> INVITATION_SENT -> EVENT_READ_BACK_VERIFIED`.

A drafted time, a calendar entry visible only to the organiser, and a transmitted invitation are different states.

### Filing/submission

Use:

`DRAFTED -> AUTHORIZED -> SUBMITTED -> RECEIPT_VERIFIED -> DOCKETED -> DECIDED`.

A document stored in Drive, GitHub or a chat is not filed. A portal intake number may be technical; identify whether it proves the substantive procedural act intended.

## 3. User-language interpretation

### “I follow your judgment” / “do it now”

These phrases execute the latest **clearly stated recommended course within the task's authorised scope**. They do not silently reverse the recommendation and do not bypass an independent hard stop.

Examples:

- where the recommendation is `HOLD — NO RESPONSE REQUIRED`, “do it now” means apply and record the hold; it does not mean send;
- where the recommendation is to strengthen an existing page, it means update that page, not create a duplicate route;
- where an exact compliant outbound email package has been presented and the user expressly directs transmission, apply the email authorization rule;
- where the exact outbound package was not presented, general agreement does not supply recipient-level email authority; and
- where the user authorises repository/site publication, that authority does not extend to email, filing, messaging, financial commitment or account-setting changes.

### Latest recommendation ledger

Before executing a broad assent, record internally:

1. the user's current request;
2. the assistant's latest explicit recommendation;
3. the action that requires authority;
4. any controlling hard stop;
5. the exact state that will result; and
6. what will remain deliberately undone.

If those fields conflict, fail closed on the external act and report the accurate prepared/hold/blocked state.

## 4. Five-field completion record

Every material close-out should state:

1. **Object** — page, file, PR, message, event, filing or decision;
2. **Action** — reviewed, drafted, updated, created, merged, sent, held, etc.;
3. **State** — exact controlled state from this protocol;
4. **Verification** — commit SHA, PR, workflow run, sent read-back, receipt, docket or other proof; and
5. **Open condition** — missing evidence, trigger, deployment check or next procedural event.

A completion response should also include a plain sentence beginning:

- `What was done:`
- `What was not done:`
- `What proves the state:`
- `What remains open:`

## 5. Receipt-only communication gate

Where the latest institutional message is only a receipt or administrative acknowledgement:

1. classify it narrowly;
2. preserve the receipt and timestamp privately;
3. determine whether it contains any express request or procedural opportunity;
4. if not, default to `NO RESPONSE REQUIRED / HOLD`;
5. do not send a courtesy reply merely to acknowledge an acknowledgement;
6. do not send a website link or improved analysis as unsolicited evidence merely because the public page changed; and
7. reopen the gate only for a defined procedural trigger or genuinely supervening essential fact.

This is a default of disciplined non-correspondence, not a permanent bar on future action.

## 6. Deletion-safety dimensions

Do not use one unqualified percentage or the word “complete” to cover different kinds of safety.

Assess separately:

| Dimension | Question |
| --- | --- |
| `THREAD_REASONING_CONTINUITY` | can a future thread recover the material decisions, limitations and open questions? |
| `IMPLEMENTATION_STATE_CONTINUITY` | can it determine what was prepared, merged, deployed, sent, held or failed? |
| `PRIMARY_EVIDENCE_COMPLETENESS` | are all needed primary documents actually located and readable? |
| `LIVE_PUBLICATION_VERIFICATION` | was the exact deployed route fetched/rendered and checked? |
| `COMMUNICATION_VERIFICATION` | was any send/read-back/receipt/docket verified at the correct level? |
| `CUSTODY_RESILIENCE` | are native evidence, hashes, independent storage and restoration controls sufficient? |
| `DISASTER_RECOVERY_SAFETY` | can the repository/site be restored independently? |

A thread may be `DELETION-SAFE WITH OPEN EVIDENCE` while primary-evidence completeness, edge verification or disaster-recovery safety remains qualified. State the qualification explicitly.

## 7. Expired or unavailable chat files

An expired chat upload has two different effects:

- it **does not block deletion safety** where the material conclusions, status decisions, public-safe metadata, retrieval target and implementation state are already canonicalised and the exact bytes are not needed; but
- it **does block any later task requiring those exact bytes**, exact attachment comparison, hashing, forensic examination or verbatim source review until the file is re-uploaded or lawfully re-materialised from its source system.

Do not repeatedly ask for re-upload where the current task does not require the expired file. Do not imply that an expired chat copy means the source no longer exists.

## 8. Current-status rule

For live proceedings, email, calendars, repository state and website deployment:

- re-query the connected/current source before acting;
- do not rely on a thread audit as proof of a later status;
- use `not located` rather than `nonexistent` unless nonexistence is affirmatively proved; and
- preserve the date/time of the last status check.

A close-out is a recovery map, not a perpetual current-status certificate.

## 9. Minimal future-thread bootstrap

For a continuing project thread:

1. read `CHATGPT_START_HERE.md` and `AGENTS.md`;
2. fetch current `main`;
3. read the universal thread-deletion protocol;
4. read this action-state governance;
5. read the most relevant thread-specific audit and canonical track controls;
6. re-query current primary sources; and
7. name the current action state before taking a new external action.

## 10. Prohibited completion shortcuts

Do not say:

- “done” where only a draft exists;
- “published” where only a branch or PR exists;
- “live” where only a merge exists and deployment is unverified;
- “verified live” where only a deployment workflow succeeded without route read-back;
- “sent” where no send action occurred;
- “sent correctly” without native sent-copy read-back;
- “received by the competent body” where only a mailbox acknowledgement exists;
- “accepted” where only receipt or docketing is proved;
- “new page created” where an existing route was strengthened;
- “no response” where a deliberate hold was chosen without saying so; or
- “100% complete” while open evidence, private-source retrieval, edge verification or custody limitations remain.

## 11. Standard final decision block

Use this compact structure where helpful:

```text
ACTION DECISION: SEND / UPDATE / MERGE / HOLD / NO ACTION REQUIRED / BLOCKED
OBJECT:
FINAL STATE:
VERIFICATION:
NOT DONE:
OPEN TRIGGER OR EVIDENCE:
DELETION STATUS:
```

## Governing sentence

> Report the exact state achieved, the proof for that state, and the next missing transition. Never improve the story by collapsing two states into one.
