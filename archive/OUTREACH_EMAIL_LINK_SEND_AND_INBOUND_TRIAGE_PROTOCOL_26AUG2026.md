# Outreach email link, send-latch and inbound-triage protocol — 26 August 2026

**Status:** CONTROLLING ADDITIVE OPERATIONAL RULE FOR PROJECT SUN ROCK / POR DERECHO EMAIL WORK

This protocol supplements `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`, `archive/PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md` and the universal publication/thread-deletion controls. Where this protocol is stricter for the covered action, apply the stricter rule. It does not authorize any email, filing, calendar invite, message or other third-party contact.

## 1. Landing-page-first rule

Every outbound Project Sun Rock / Por Derecho email must contain at least one current Por Derecho website link selected deliberately for the recipient and purpose.

The purpose of the link is substantive: it should take the recipient to the part of the public record most likely to be relevant to their expertise, institutional role, prior involvement or reason for contact.

Before drafting the email, decide the preferred landing page. Draft backwards from that page:

`recipient/capacity → reason for contact → most relevant unresolved or contextual issue → best live Por Derecho route → concise explanation of why that route is relevant → requested next step`.

Do not default mechanically to the homepage or the general collaboration page. Use a deep link where a specialist page is materially more relevant. Use the collaboration page only where collaboration itself is the best first context.

## 2. Link readiness gate

Before a package can be presented as ready or sent:

1. identify every Por Derecho link in the package;
2. verify the primary route is live at the time of preparation;
3. confirm its visible content actually matches the reason stated in the email;
4. prefer one primary deep link and, only where useful, one secondary link;
5. do not overload first-contact emails with multiple unrelated links; and
6. treat a route already sent externally as a compatibility obligation under `PD-GOV-006 — SENT-LINKS` in `AGENTS.md`.

A package with no Por Derecho link is not ready.

**SEND STATUS: BLOCKED — POR DERECHO LANDING PAGE MISSING.**

## 3. Exact-package authorization remains mandatory

The website-link rule does not weaken the exact-package approval rule. The final package must still identify every recipient, message mode, exact subject, complete body, every attachment and every external link. Any post-approval change to a link invalidates the approval and requires fresh final authorization.

`PREPARED ≠ AUTHORIZED ≠ SENT ≠ VERIFIED`.

## 4. One-send latch

One authorization permits at most one transmission of the exact approved package.

After the mail connector returns a positive send result with a concrete message/thread reference:

- the authorization is consumed;
- the send path for that package is latched closed;
- no second send invocation may be used for verification, reassurance, retry or duplicate checking; and
- verification must be read-only.

A future agent must treat a successful send result as a hard transition from `AUTHORIZED` to `SENT` and immediately switch tool class from write/send to read/search.

## 5. Read-only verification

Post-send verification may use only native Sent-mail read/search operations. It must verify, against the approved package:

- sender account;
- To/Cc/Bcc;
- new/reply/forward/correction/follow-up mode;
- exact subject;
- non-empty expected body;
- every approved Por Derecho link;
- attachment count and filenames; and
- sent timestamp.

Never invoke a send action to test whether a send succeeded.

## 6. Duplicate or malformed-send incident handling

If a duplicate, malformed, incomplete or unintended transmission is discovered:

1. stop all outbound activity for that recipient/thread;
2. inventory the native Sent copies using read-only tools;
3. report the incident accurately;
4. do not send an apology, correction, resend or explanation automatically; and
5. require a new exact package and fresh explicit authorization before any corrective transmission.

Where repeated corrections would amplify a duplicate incident, prefer no further unsolicited contact unless a substantive reason exists and the user expressly approves it.

## 7. Pre-send private-history gate

Before every new external outreach package is marked ready, perform the fresh pagination-complete person-and-organisation Gmail history scan required by `archive/PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md`.

For historical professional-reconnection work, the scan must distinguish:

- prior meeting/contact;
- documents previously supplied;
- actual mandate versus exploratory contact;
- prior advice versus no located conclusion;
- current verified professional route;
- replies, bounces, redirects and fallback routes; and
- any prior recent outreach that makes another unsolicited message inappropriate.

Do not convert historical contact into an assumed retainer, opinion, endorsement or completed review.

## 8. Inbound-email triage automation specification

This section defines the behavior a future ChatGPT/agent should execute when checking connected Gmail for replies. It is a repository operating specification, not a live server-side Gmail trigger and not authority to send anything.

At the start of a continuation thread, and before preparing a follow-up to any tracked outreach or institutional thread, perform a read-only Gmail scan for new inbound messages since the last known audit point.

Classify each new message into exactly one primary state where possible:

- `SUBSTANTIVE_REPLY` — contains a human substantive response or asks material questions;
- `REQUEST_FOR_INFORMATION` — asks for documents, links, explanation or evidence;
- `SCHEDULING` — proposes or asks for a meeting/time;
- `CONFLICT_OR_CAPACITY_DECLINE` — conflict, incompatibility, lack of capacity or no-interest response;
- `ACKNOWLEDGEMENT_ONLY` — confirms receipt without substantive treatment;
- `OUT_OF_OFFICE` — automated absence/return-date response;
- `DELIVERY_DELAY` — temporary delivery problem;
- `BOUNCE` — permanent non-delivery or rejected address;
- `ROUTING_REDIRECT` — asks that another office/person/channel be used;
- `NO_CONTACT_REQUEST` — unsubscribe or explicit request not to contact; or
- `UNCLASSIFIED` — insufficient information; read the full thread before action.

### Mandatory response behavior

For every inbound state:

- read the full relevant thread before drafting;
- summarize what the message actually proves and what it does not prove;
- identify the most relevant current Por Derecho landing page for any possible response;
- prepare, but do not send, a reply unless the user expressly authorizes the exact package;
- never auto-forward an inbound message;
- never auto-add a new recipient because of a redirect or colleague reference;
- never auto-create a correction or resend after a bounce;
- never treat an acknowledgement as merits review or institutional acceptance; and
- never treat a meeting proposal as authorization to create/send a calendar invitation without the required calendar authority.

### Recommended next-action mapping

- `SUBSTANTIVE_REPLY` → summarize, identify questions, prepare personalized reply with the most relevant deep link, then request/send only under fresh authorization.
- `REQUEST_FOR_INFORMATION` → inventory what can safely be supplied; separate public-link material from private evidence; prepare exact attachment/link manifest.
- `SCHEDULING` → check calendar availability if requested/authorized; prepare meeting response; do not create an invite automatically.
- `CONFLICT_OR_CAPACITY_DECLINE` → record the stated reason accurately; normally no persuasion follow-up unless specifically requested.
- `ACKNOWLEDGEMENT_ONLY` → no follow-up merely because receipt was acknowledged.
- `OUT_OF_OFFICE` → record the stated return date; do not resend automatically.
- `DELIVERY_DELAY` → wait for the provider's final state; no automatic retry.
- `BOUNCE` → research a verified current professional route before preparing a new package; fresh authorization is required.
- `ROUTING_REDIRECT` → verify the new route independently and rescan Gmail history before preparing anything.
- `NO_CONTACT_REQUEST` → stop contact and preserve the instruction privately.

## 9. Public/private boundary for continuity

The repository is public. Do not commit private recipient addresses, private email bodies, message IDs, subject lines tied to private recipients, signatures, phone numbers, tracking URLs, provider metadata, private calendar details or privileged/current-counsel advice.

Public continuity records may preserve only minimized operational facts, such as:

- that a historical professional-reconnection batch exists;
- that some messages are awaiting reply;
- that a duplicate-send incident occurred and the resulting hard-stop rule;
- that institutional traceability requests remain open; and
- the retrieval instructions a future agent must use to reconstruct exact private state from connected Gmail.

Exact recipient-level state belongs in connected Gmail and other authorised private systems, not Git.

## 10. Continuation-thread procedure

A future thread continuing email/outreach work must:

1. fetch current `main`;
2. read `AGENTS.md`, `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`, this protocol and the latest relevant thread-deletion audit;
3. scan connected Gmail from the relevant audit date forward, exhausting pagination;
4. reconstruct privately the exact sent/reply/bounce state;
5. surface a concise action queue before any new outbound package;
6. choose the website landing page before drafting each email;
7. maintain one-recipient/one-package/one-authorization/one-send discipline; and
8. verify any authorized send by read-only native Sent-message retrieval.

## 11. No implied background authority

This protocol does not create an autonomous background email responder. A future automation or agent may monitor/read/classify only within the permissions actually available to it. It may not send, reply, forward, correct, resend, schedule or contact a third party without the fresh exact authorization required by the controlling email rule.
