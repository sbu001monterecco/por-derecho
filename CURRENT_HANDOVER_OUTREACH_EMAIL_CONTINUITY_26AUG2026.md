# Current handover — outreach email continuity — 26 August 2026

**Purpose:** public-safe continuation record for a future ChatGPT/agent thread.  
**Private reconstruction source:** connected Gmail and other authorised private systems.  
**Public-repository rule:** do not add recipient addresses, private email bodies, provider message IDs or private-thread subjects here.

## Current state

A historical professional-reconnection batch and several institutional traceability requests were worked during 25–26 August 2026. The exact recipient-level state is intentionally not duplicated into this public repository.

The current operational posture is:

- most recently contacted historical professionals are in `AWAIT_REPLY` state;
- at least one recipient is under an explicit `NO_UNSOLICITED_FOLLOW_UP` hold because a duplicate-send incident occurred;
- a second duplicate-send incident confirmed that post-send verification must be read-only and that one authorization permits one send action only;
- the latest correctly controlled professional send included a recipient-specific Por Derecho deep link and was verified through the native Sent copy;
- the historical 2019 referral team relevant to that reconnection exercise has been exhausted; an administrative support contact from that historical chain is not a substantive outreach target merely because they were copied on old correspondence;
- no next external recipient should be invented from this handover; the next campaign/workstream must be chosen deliberately from evidence and current need;
- outstanding institutional traceability requests remain open and must be treated as waiting states, not as merits outcomes.

## Controlling email rules

Before doing any outbound-email work, read:

1. `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`;
2. `archive/PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md`;
3. `archive/OUTREACH_EMAIL_LINK_SEND_AND_INBOUND_TRIAGE_PROTOCOL_26AUG2026.md`; and
4. `archive/THREAD_DELETION_AUDIT_OUTREACH_EMAIL_CONTINUITY_26AUG2026.md`.

The controlling state machine is:

`PREPARED → AUTHORIZED → SENT → VERIFIED`

Never collapse these states.

## Universal website-link rule

Every Project Sun Rock / Por Derecho outbound email must contain at least one current Por Derecho website link deliberately selected for the recipient and purpose.

Choose the landing page first, then draft the email around that relevance. Prefer a deep specialist route over a generic homepage or collaboration page where a specialist route is materially better. Verify the route is live and contextually accurate before the package is marked ready.

A package with no Por Derecho link is blocked.

## Private Gmail reconstruction procedure

At the beginning of a future continuation thread:

1. search connected Gmail for sent and received messages from **25 August 2026 onward** relating to:
   - historical professional reconnection;
   - Canary legal/professional contacts;
   - institutional traceability work involving the Madrid Bar/its regional council and the Tenerife Bar;
2. exhaust pagination rather than relying on the first page;
3. read the full relevant threads;
4. reconstruct privately:
   - exact recipient identities and verified professional routes;
   - exact subjects and message modes;
   - sent-once versus duplicate-send state;
   - native Sent verification state;
   - replies, acknowledgements, out-of-office responses, bounces, delays and redirects;
   - any request for information, scheduling proposal, conflict/capacity decline or substantive answer; and
5. present an action queue to the user before preparing new outbound communications.

Do not infer a reply from silence. Do not infer delivery from Sent. Do not infer merits review from acknowledgement.

## Institutional open-action classes

The following public-safe issue classes remain open until current private/institutional evidence proves otherwise:

- proof of onward transmission / traceability for a Madrid professional-regulation appeal;
- reference/registration state for a second-level regional professional-regulation appeal;
- Tenerife receipt/docket state for a territorial referral;
- substantive content/status behind an earlier Tenerife professional-regulation intake matter;
- current complete file/index for the Madrid regional professional-regulation matter, including post-snapshot additions; and
- any later procedural or final decision.

A future thread must re-query Gmail and the relevant institutional sources rather than treating this list as proof that no response has arrived.

## Professional-reconnection next-action classes

When new inbound mail is found, classify and handle it under the inbound-triage protocol. In particular:

- substantive reply → summarize, identify questions, select relevant site page, prepare reply only;
- request for information → separate public links from private evidence and prepare an exact manifest;
- scheduling → check availability only as authorized and prepare a response; do not auto-create/send an invite;
- conflict/capacity decline → record accurately; normally do not persuade;
- acknowledgement/out-of-office → normally no immediate follow-up;
- bounce/delay → do not auto-retry;
- redirect → independently verify the new route and rerun the pre-send history gate;
- no-contact request → stop contact.

## Next campaign boundary

The friendly historical-reconnection sequence covered by this handover is effectively complete. A future outbound campaign should be selected deliberately from one of these separate workstreams:

- former/current advisers from whom information, file reconstruction or cooperation is needed;
- advisers or professionals where an active dispute/professional-responsibility question requires a different tone;
- specialist Canary professionals for genuinely new finite mandates; or
- institutional follow-ups triggered by actual replies or elapsed procedural needs.

Do not mix these workstreams automatically. Each requires its own recipient history, purpose, evidential boundary, landing page and exact package approval.

## Future-thread continuation prompt

Use this prompt as the minimum bootstrap for a new ChatGPT thread:

> Fetch current `main` in `sbu001monterecco/por-derecho`. Read `AGENTS.md`, `CHATGPT_START_HERE.md`, `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`, `archive/OUTREACH_EMAIL_LINK_SEND_AND_INBOUND_TRIAGE_PROTOCOL_26AUG2026.md`, `CURRENT_HANDOVER_OUTREACH_EMAIL_CONTINUITY_26AUG2026.md`, and `archive/THREAD_DELETION_AUDIT_OUTREACH_EMAIL_CONTINUITY_26AUG2026.md`. Then perform a pagination-complete read-only Gmail scan from 25 August 2026 onward for replies, acknowledgements, bounces, delays, redirects and substantive responses connected to the professional-reconnection and ICAM/CCACM/ICATF traceability threads. Reconstruct exact recipient-level state privately from Gmail; do not publish private addresses, subjects, message IDs or bodies into Git. Present the current action queue first. For every future email, choose and verify the most relevant Por Derecho landing page before drafting; require an exact approved package; one authorization permits one send only; after a successful send, latch the send path closed and verify by read-only native Sent retrieval. Never auto-reply, auto-correct, auto-resend or auto-forward.

## Automation boundary

The repository now contains an inbound-email triage **automation specification**, not an autonomous Gmail responder. A future agent with connected Gmail may execute the read/classify/prepare workflow. No repository file creates external authority to transmit mail.
