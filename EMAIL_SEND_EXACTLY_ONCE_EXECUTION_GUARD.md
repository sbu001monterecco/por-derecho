# Outbound email — atomic exactly-once execution guard

**Control date:** 25 August 2026  
**Status:** CONTROLLING ADDENDUM TO `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`  
**Scope:** every email send, reply, forward, correction, resend, follow-up, scheduled transmission or self-email performed through any connected mail tool

This guard supplements the existing exact-authorisation rule. Where wording could be read differently, the stricter non-duplication control in this file governs.

## 1. Root problem this guard closes

A prior rule correctly said that one authorization permits at most one transmission. That wording was not enough because the execution state was not locked atomically before the first mail mutation. After a successful send returned a concrete provider message identifier, a second independent send action was invoked during what should have been read-only verification.

The duplicate was therefore caused by two separate outbound tool calls. It was not a Gmail retry, bounce, delivery replay or attachment problem.

## 2. Exactly-once invariant

> **One exact user authorization permits one—and only one—outbound mail mutation call.**

The limit applies to the complete authorized package, not merely to each tool name or each assistant step.

A mail mutation includes any action that can transmit externally, including:

- send;
- reply;
- forward;
- resend;
- correction;
- follow-up;
- scheduled send;
- send-draft;
- self-email; and
- any connector action whose effect is external transmission.

No two outbound mutations may be issued in parallel, sequentially, speculatively or as verification of the same authorization.

## 3. Authorization is consumed before—not after—the tool call

Immediately before invoking the first outbound mail mutation, the execution record must atomically set:

- `authorization_consumed = true`;
- `outbound_mutation_count = 1`;
- `mutation_lock = true`; and
- `state = TRANSMISSION_ATTEMPTED`.

This must occur **before** waiting for the provider response.

The authorization remains consumed and the mutation lock remains closed whether the provider returns:

- success;
- an error;
- a timeout;
- an unknown result;
- a malformed response; or
- no usable message identifier.

A provider error or uncertain result never reopens the original authorization.

## 4. Required state machine

`PREPARED → AUTHORIZED → TRANSMISSION_ATTEMPTED → SENT / OUTCOME_UNKNOWN / NOT_SENT_CONFIRMED → VERIFIED`

### PREPARED

The package exists but transmission has not been authorized.

### AUTHORIZED

The user has given fresh, exact authorization for one package. No mutation has yet been invoked.

### TRANSMISSION_ATTEMPTED

The one permitted outbound mutation has been invoked. The authorization is consumed and all further mail mutations are locked.

### SENT

The provider returned a positive result with a concrete message or thread identifier.

### OUTCOME_UNKNOWN

The result was missing, timed out or ambiguous. Verification must proceed only through read-only mailbox operations.

### NOT_SENT_CONFIRMED

Read-only mailbox evidence confirms that no corresponding Sent message exists. A fresh user authorization is still required before another attempt.

### VERIFIED

The native Sent message was retrieved and matched to the approved package.

## 5. Read-only verification allowlist

After state `TRANSMISSION_ATTEMPTED`, only non-mutating mailbox operations may be used for verification, including:

- read the returned message identifier;
- read the returned thread;
- search the Sent mailbox;
- inspect native MIME;
- read attachment metadata or bytes; and
- search for bounces or automated responses.

The verification phase must never invoke a send, reply, forward, resend, schedule or send-draft action.

If tool names are unclear, classify by effect: **if the action can transmit externally, it is prohibited after the first attempt.**

## 6. Package fingerprint and duplicate check

Before transmission, derive a private package fingerprint from:

1. sender account;
2. normalized To, Cc and Bcc lists;
3. transmission mode;
4. exact subject;
5. normalized full body;
6. ordered attachment names, sizes and hashes where available;
7. ordered external links; and
8. source message/thread identifier for a reply or forward.

The fingerprint must remain private and must not be placed in the public repository with recipient details.

Immediately before the authorized mutation, perform a read-only Sent-mail check for the same recipient/subject/body marker or fingerprint within the preceding ten minutes. If an equivalent message already exists, block the send and report:

**SEND STATUS: BLOCKED — EQUIVALENT MESSAGE ALREADY PRESENT IN SENT.**

After the first send, search the immediate Sent window again. More than one matching native message must be classified as a duplicate incident.

## 7. Verification receipt

A successful verification receipt must include privately:

- provider message and thread identifier;
- sent timestamp;
- sender;
- To, Cc and Bcc;
- transmission mode;
- exact subject;
- body marker;
- attachment count and exact filenames;
- source message/thread where relevant;
- package fingerprint or its private record key;
- `outbound_mutation_count = 1`; and
- duplicate-window result.

No result may be described as `VERIFIED AS SENT CORRECTLY` unless the duplicate-window result also confirms exactly one matching Sent message.

## 8. Retry and correction control

A timeout, provider error, missing attachment, duplicate, malformed body or uncertain outcome does not authorize another outbound mutation.

Every retry, correction, apology, replacement, resend or explanatory follow-up requires:

1. a newly assembled exact package;
2. a fresh history and recipient check where applicable;
3. a fresh explicit user authorization; and
4. a new one-shot execution record.

The system must never attempt to “fix” a duplicate by sending another message automatically.

## 9. Tool-routing hard stop

Once any outbound mail mutation returns or throws, the next tool call for that package must be a read-only mailbox action.

Before every subsequent Gmail/mail connector call, ask:

> **Has an outbound mutation already been attempted under this authorization?**

If yes, every mutating tool is forbidden. The only valid next action is read-only verification or a report to the user.

## 10. Incident response

Where a duplicate is detected:

- report it immediately and precisely;
- preserve the two native Sent identifiers privately;
- determine whether the bodies, recipients and attachments are identical;
- search for bounces separately;
- do not infer opening or reading;
- do not send an apology or correction without fresh authorization; and
- record a public-safe incident note without names, addresses, subjects, message identifiers or private content.

## 11. Current incident record

The 25 August 2026 duplicate-send incident and its root-cause analysis are preserved in:

`archive/OUTBOUND_EMAIL_DUPLICATE_SEND_INCIDENT_25AUG2026.md`

The machine-readable version of this guard is:

`.github/governance/outbound-email-exactly-once-guard-v1.json`

The validator is:

`.github/governance/test_outbound_email_exactly_once_guard.py`
