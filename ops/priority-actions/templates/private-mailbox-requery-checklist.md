# Private mailbox re-query checklist

**Task:** `P0-TX-01`  
**Mode:** read-only  
**Public Git rule:** do not record names, addresses, private subjects, message IDs, provider locators, native bodies, attachments or live negotiation detail.

## 1. Baseline

- [ ] Read `TXD-20260825-02` and `TXD-20260825-03`.
- [ ] Record the current date/time and connected account searched in the private work note.
- [ ] Confirm that no send/reply/forward action will be used.

## 2. Group-side legal coordinator thread

- [ ] Locate the authorised briefing/forward and its native Sent copy.
- [ ] Search for direct replies in the thread.
- [ ] Search for replies outside the thread using sender, date window and distinctive non-sensitive concepts.
- [ ] Classify the latest state:
  - no reply located;
  - automated response;
  - acknowledgement only;
  - substantive reply;
  - request for call/documents;
  - conflict/onboarding/engagement step;
  - declined or unavailable.
- [ ] Record whether the confidentiality document was acknowledged, commented on or replaced.

## 3. Prospective external relationship-partner thread

- [ ] Locate both duplicate Sent copies and treat them as one authorised package duplicated in transmission.
- [ ] Search for a response to either message or a new thread.
- [ ] Separate personal willingness from firm conflict clearance, onboarding and engagement.
- [ ] Record whether a three-way discussion, direct adviser discussion or formal proposal was suggested.
- [ ] Record whether any current institutional contact or approach was proposed.

## 4. Current confidentiality/NDA state

- [ ] Identify the latest received draft and source message.
- [ ] Identify all proposed amendments and whether they were accepted, rejected, superseded or left unanswered.
- [ ] Record the proposed signatory entity and capacity.
- [ ] Record whether the document covers one opportunity or multiple opportunities.
- [ ] Record duration, entire-agreement effect, internal disclosure perimeter and external onward-disclosure rule.
- [ ] Mark any earlier agreement as `RELEVANCE_UNRESOLVED` unless current counsel or the parties expressly reconcile it.

## 5. Meeting and action state

- [ ] Search Calendar/email for proposed or accepted meetings.
- [ ] Record attendees and capacities privately.
- [ ] Record whether the meeting occurred, was postponed or remains proposed.
- [ ] Locate any post-meeting summary or requested-document list.
- [ ] Do not infer occurrence from a calendar invitation alone.

## 6. Output classification

Create a private status note using only:

- `NOT_LOCATED`;
- `DELIVERED_NOT_READ_PROVED`;
- `AUTOMATED_RESPONSE`;
- `ACKNOWLEDGED`;
- `SUBSTANTIVE_REPLY`;
- `CONFLICT_CHECK_STARTED`;
- `ONBOARDING_STARTED`;
- `ENGAGEMENT_PROPOSED`;
- `ENGAGEMENT_CONFIRMED`;
- `MEETING_PROPOSED`;
- `MEETING_CONFIRMED`;
- `MEETING_OCCURRED`;
- `NDA_DRAFT_ACTIVE`;
- `NDA_SIGNED`;
- `DECLINED`;
- `UNRESOLVED`.

## 7. Public-safe derivative test

A repository update is justified only if the private read materially changes continuity. It must:

- use opaque role/group descriptions;
- omit names, addresses, subjects, dates that identify a live negotiation, message IDs and document content;
- distinguish personal willingness from firm mandate;
- distinguish NDA circulation from signature;
- state that no external follow-up is authorised unless separately approved.

## 8. Hard stop

This checklist authorises no outbound communication. After the read, stop and report the state. Any proposed email or meeting invitation must be prepared as a new exact package under the controlling email rules.
