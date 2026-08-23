# Project Sun Rock / Por Derecho — Mandatory Media Core Package Rule

**Control date:** 23 August 2026  
**Status:** CONTROLLING MEDIA-OUTREACH HARD GATE  
**Scope:** every Project Sun Rock / Por Derecho outbound email to a journalist, editor, newsroom, media organisation, media-routing address or journalistic contact, including first approaches, replies, resends, corrections, supplements, follow-ups and routing/permission enquiries  
**Send gate:** `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`

## 1. Mandatory rule

Every media-facing Project Sun Rock / Por Derecho email must contain the complete **Media Core Package**.

Recipient personalisation may change the subject, opening, story module, evidential emphasis, tone, finite ask, supporting documents and recipient-specific website routes. It may **not** remove any Media Core Package component.

The Media Core Package is:

1. the appropriate-language **PwC 2016 knowledge-point PNG source map** attached as a real file;
2. the appropriate-language **San Telmo / RICPE / Sun Park PNG source map** attached as a real file;
3. the direct controlled San Telmo webinar link at approximately 08:08;
4. at least one current public Por Derecho / Project Sun Rock website link in the body; and
5. a short evidential limitation explaining that the maps and webinar do not independently prove wrongdoing, coordination, causation, defective advice or responsibility.

## 2. Controlling filenames by language

### Spanish

- `pwc-five-actors-plus-ac-2016-knowledge-checkpoint-ES.png`
- `san-telmo-ricpe-sun-park-stamp-v1-ES.png`

### English

- `pwc-five-actors-plus-ac-2016-knowledge-checkpoint-EN.png`
- `san-telmo-ricpe-sun-park-stamp-v1.png`

### German

- `Anlage-2A-PwC-Kenntnispunkt-2016-DE.png`
- `Anlage-1A-RICPE-Sun-Park-Rollen-DE.png`

Do not substitute ambiguous duplicate-download filenames, `(2)`, `(3)`, `final-final` or an unverified language version where the canonical asset is available.

## 3. Controlled links

### Webinar

`https://www.youtube.com/watch?v=mHn9IJU0qI4&t=488s`

Controlled source description:

- programme: San Telmo Abogados y Economistas, 30 November 2021;
- first-look timestamp: approximately 08:08–08:12;
- current speaker attribution: Eduardo Sánchez Iglesias;
- evidential use: finite questions concerning investor introduction, professional knowledge, advisory role, due diligence, separation of functions and project controls;
- limitation: the statement does not by itself prove irregularity, improper conduct, collusion, unlawful investment or defective advice.

### Por Derecho website

At least one current public Por Derecho route must appear in the body. Use the recipient-specific route that best answers the first editorial question. The homepage may be added but does not replace a cleaner specific dossier where one exists.

## 4. No discretionary override

The following do **not** permit omission of the Media Core Package:

- “Level 0” or “link-led” classification;
- a preference for brevity;
- concern about document overload;
- the recipient having received other documents previously;
- a first approach, re-entry, correction or friendly follow-up;
- an assistant's editorial judgment that the maps or webinar are not central to the selected story module;
- the words “normally”, “where relevant”, “consider”, “smallest package” or similar discretionary language elsewhere in the repository; or
- a later general instruction to “send”.

This file overrides any earlier discretionary source-kit wording for media-facing email.

## 5. Exception rule

An omission is valid only if Gil Marer expressly approves, for the exact recipient and exact transmission, the exact component to be omitted.

A valid exception must say, in substance:

> For this exact email to [recipient], omit [named component].

General approval of the email, the instruction “send”, silence, urgency, an earlier exception, or approval of a different package is not an exception.

Any approved exception must be recorded in the readiness record and does not change the standing rule for later messages.

## 6. Mandatory pre-send hard stop

Before requesting final approval and again before sending, verify the actual Gmail draft:

```text
MEDIA RECIPIENT = YES
PWC PNG REQUIRED = YES
PWC PNG FOUND = YES
SAN TELMO PNG REQUIRED = YES
SAN TELMO PNG FOUND = YES
WEBINAR LINK REQUIRED = YES
WEBINAR LINK FOUND = YES
POR DERECHO LINK REQUIRED = YES
POR DERECHO LINK FOUND = YES
EVIDENTIAL LIMITATION FOUND = YES
EXPLICIT USER EXCEPTION = NONE / EXACTLY RECORDED
PERSON GMAIL HISTORY SCAN = COMPLETE
ORGANISATION GMAIL HISTORY SCAN = COMPLETE
PAGINATION = EXHAUSTED
COLLISION DECISION = RECORDED
```

If any required result is not `YES` and no exact exception exists:

**SEND STATUS: BLOCKED — MANDATORY MEDIA CORE PACKAGE INCOMPLETE.**

Do not present an incomplete package as ready and do not interpret a later “send” instruction as curing the missing component.

## 7. Draft and sent-copy verification

The attachment and link manifest must identify:

- exact filenames;
- language;
- version/date;
- file size and hash where available;
- source class and limitation;
- exact webinar URL; and
- every Por Derecho route.

After an authorised send, read the actual sent copy and verify the two attachment filenames, the webinar URL, at least one Por Derecho URL and the evidential limitation. A connector success response alone is insufficient.

## 8. Triggering incident and correction

On 23 August 2026, an initial media email was prepared and sent without the two PNG source maps and webinar link after the standing instruction was wrongly treated as optional. A later same-thread corrective resend supplied the complete package after fresh exact authorisation.

The lesson is controlling:

- recipient tailoring must not remove mandatory components;
- document-overload concerns do not turn two lightweight orientation maps into optional attachments;
- package verification must test requirements, not merely confirm that the draft matches an incorrectly declared zero-attachment manifest; and
- a general “send” instruction is not an implied waiver.

No private address, Gmail identifier or full private body is reproduced in this public-safe control record.

## 9. Relationship to other rules

Read this rule with:

- `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`;
- `archive/PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md`;
- `archive/OUTBOUND_WEBSITE_LINK_MANDATORY_RULE_23AUG2026.md`;
- `archive/OUTBOUND_CANONICAL_SOURCE_KIT_MANIFEST_23AUG2026.md`;
- `archive/MAXIMUM_REACH_OUTBOUND_CAMPAIGN_LAYER_23AUG2026.md`;
- `archive/OUTBOUND_EMAIL_COMMUNICATIONS_PROTOCOL_23AUG2026.md`;
- `archive/prompts/RECIPIENT_SPECIFIC_OUTBOUND_EMAIL_PREPARATION_PROMPT_23AUG2026.md`; and
- `archive/OUTBOUND_EMAIL_FUTURE_THREAD_START_HERE_23AUG2026.md`.

This rule controls media-package completeness. It does not itself authorise any email.
