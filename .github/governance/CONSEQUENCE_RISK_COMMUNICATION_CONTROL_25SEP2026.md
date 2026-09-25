# Consequence-Risk Communications Control

**Control ID:** PD-CRC-20260925-01  
**Status:** CONTROLLING / FAIL-CLOSED / PUBLIC-SAFE GOVERNANCE  
**Scope:** incoming and outgoing email, electronic-notification platforms, court/procurador/counsel communications, institutional portals, repository/CI notifications, and materially equivalent communications.

## 1. Objective

Por Derecho / Project Sun Rock must not treat a communication as safely processed merely because it was received, opened, indexed, summarised, added to a repository, or marked read.

Every material communication must be tested for one operational question:

> **Could failure to notice, acquire, understand, route, preserve or act on this communication make the position materially worse?**

If yes, the communication creates a persistent **consequence-risk alert** until the risk is explicitly dispositioned and, where action is required, the action is verified.

This control supplements evidence governance, supersession, publication, email-authorisation and repository-preservation rules. It does not authorise an email, filing, appeal, payment, contact or other external act.

## 2. What triggers the control

A consequence-risk review is mandatory where a communication may affect any of the following:

- a deadline, limitation period, appeal/review right, filing window, cure period, hearing, meeting or appointment;
- an adverse or status-changing decision, archive, rejection, admission, referral, joinder, transfer, request for information, requirement, sanction, suspension or closure;
- preservation or loss of evidence, access, custody, service, notification or proof of receipt;
- title, asset control, exploitation, income, financing, contract, transaction, security, insurance or other material economic position;
- legal representation, procedural standing, routing, competence, jurisdiction or responsibility for the next action;
- a live publication, platform/account, data-protection, security or reputational issue;
- a dependency created by an outbound filing, request, escalation, question, undertaking or promised response;
- a delivery failure, bounce, obsolete address, missing attachment, incorrect routing or uncertain transmission;
- a failure of the monitoring system itself, including connector outage, CI incapacity, quota exhaustion, host divergence or an ingestion gap.

Sender prestige, Gmail stars, Gmail IMPORTANT/UNREAD flags, subject-line words and automated categorisation are signals only. They are never sufficient to clear or suppress a risk event.

## 3. Mandatory source acquisition

### 3.1 Notice-of-notice

An email stating that a notification or communication is available on DEHú, Notifica, LexNET, a court portal, regulator portal or similar system is itself a risk event.

Until the underlying document has been acquired and classified, the event remains:

`CONTENT_ACQUISITION_REQUIRED`

A courtesy email with no attachment may therefore be more urgent than a long email with attachments.

### 3.2 Attachment-first rule

A message is not cleared until every potentially operative attachment has been classified or expressly recorded as inaccessible.

Potentially operative attachments include, without limitation:

- Auto;
- Acuerdo;
- Decreto;
- Providencia;
- Sentencia;
- Diligencia;
- Oficio;
- requerimiento;
- notificación;
- justificante;
- registry receipt;
- appeal or filing receipt;
- ZIP or bundle containing any of the above.

`EMAIL_READ / OPERATIVE_ATTACHMENT_UNREVIEWED` is an open risk state.

### 3.3 Native source controls

The native mailbox or authenticated platform remains the primary source. A repository summary, ChatGPT summary, Drive note or screenshot never replaces the native communication or underlying operative document.

## 4. Deadline and service decomposition

Never collapse message arrival into legal notification.

Where timing may matter, record separately:

1. mailbox arrival time;
2. platform availability time;
3. provider/court receipt time;
4. date of access or download;
5. legally effective notification/service date if established;
6. rule governing computation;
7. computed deadline;
8. source proving the computation;
9. uncertainty or competing date if unresolved.

If an operative decision exists and the service/deadline basis is unresolved, classify:

`DEADLINE_OR_SERVICE_DATE_UNRESOLVED`

and keep the alert open until reconciled.

The system must not invent a legal deadline merely because a date appears in an email. Human/legal review controls the deadline conclusion.

## 5. Inbound state machine

The minimum inbound lifecycle is:

`DETECTED → CONTENT_ACQUIRED → CLASSIFIED → ALERT_OPEN → ACKNOWLEDGED → DISPOSITION_ASSIGNED → ACTION_VERIFIED → RESOLVED`

Permitted side states:

- `CONTENT_ACQUISITION_REQUIRED`
- `OPERATIVE_ATTACHMENT_UNREVIEWED`
- `DEADLINE_OR_SERVICE_DATE_UNRESOLVED`
- `ROUTING_OR_DELIVERY_FAILURE`
- `EXPECTED_RESPONSE_OVERDUE`
- `CONTROL_SYSTEM_DEGRADED`
- `NO_ACTION_REQUIRED_VERIFIED`

An item may not move directly from DETECTED to RESOLVED.

Opening a message, marking it read, summarising it, adding it to Git, or verbally saying “seen” does not resolve the alert.

## 6. Outbound dependency rule

Every material outbound act that requests, expects or legally depends upon a later event creates a dependency object.

Examples:

- request for acknowledgement;
- filing whose incorporation/registration must be confirmed;
- request for certificate, index, document or access;
- communication stating that an authority will respond later;
- referral expected to reach another competent body;
- request to counsel for a time-sensitive act;
- contractual proposal awaiting acceptance;
- platform/security escalation awaiting restoration or review.

The dependency must record:

- outbound event;
- expected event;
- responsible owner;
- expected checkpoint or due date if known;
- consequence of non-response;
- escalation path;
- whether follow-up requires fresh authorisation.

Silence does not itself prove rejection, non-receipt or wrongdoing. It can, however, trigger `EXPECTED_RESPONSE_OVERDUE`.

This rule does **not** override `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`. An alert may recommend a follow-up but never authorises transmission.

## 7. Delivery and routing failures

A bounce, obsolete address, failed portal submission, missing attachment, wrong recipient, rejected registration, uncertain upload, or conflicting delivery state must reopen the underlying matter.

Required distinction:

`SENT ≠ DELIVERED ≠ RECEIVED ≠ ROUTED ≠ JOINED ≠ EXAMINED ≠ ACCEPTED ≠ MERITS_OUTCOME`

One successful route does not erase a separate failed route when the failed route had its own material function.

## 8. Deduplication and incident clustering

Duplicate notices for the same underlying communication identifier, filing, court act or platform event must be clustered into one canonical event with multiple source notifications.

Machine-generated cascades must also be clustered. For example, multiple CI job failures caused by one quota exhaustion should create:

1. one root infrastructure incident; and
2. dependent job failures linked to that incident.

Do not create dozens of equal-priority alerts that bury the causal event.

## 9. Severity

Severity is based on:

`potential consequence × time sensitivity × reversibility × uncertainty`

### P0 — CRITICAL
Credible risk of imminent or irreversible prejudice, including missed deadline, lost right, default, evidence loss, asset/control loss, security compromise, or an unopened official notification where a material clock may already be running.

### P1 — HIGH
Material status-changing or strategically important event requiring review, action assignment, preservation, counsel treatment, reconciliation or follow-up, without presently established imminent irreversible prejudice.

### P2 — MATERIAL WATCH
Material development affecting the evidence/status picture, but presently requiring monitoring rather than immediate action.

A classifier may temporarily escalate an unknown-content official notice. Severity must be revised after acquisition and review.

## 10. Required alert fields

Every alert must contain at least:

- stable alert ID;
- source event ID;
- detected timestamp;
- source system;
- sender/institution class;
- proceeding/project reference where known;
- short source-safe description;
- underlying document acquired: yes/no;
- operative attachment review state;
- significance;
- concrete risk if missed;
- severity;
- deadline/service state;
- deadline if verified;
- owner;
- required disposition;
- expected response/dependency where applicable;
- source locator held privately;
- related canonical records;
- superseded prior proposition(s);
- current status;
- acknowledgement evidence;
- action-verification evidence;
- resolution reason;
- control-system health state.

Private source locators, message IDs, raw bodies, personal data and protected attachments stay outside public Git.

## 11. Supersession and propagation

A material communication must not remain isolated in the newest email, conversation or Drive note.

After source verification, propagate its consequences to every materially affected:

- chronology;
- proceeding record;
- institutional-communications register;
- source/evidence state;
- correction/supersession record;
- missing-evidence/dependency register;
- current handover;
- public-safe page or route where publication is actually warranted;
- GitHub/GitLab parity record;
- private Drive continuity record.

Historical text remains preserved. Supersession is additive and visible.

## 12. Independent second-pass safeguard

The system must periodically ask:

> **Which material incoming communications, notices, attachments, outbound dependencies or failed routes remain unacknowledged, unclassified, unresolved or without verified disposition?**

This second-pass control is mandatory because first-pass classification can fail.

It must specifically detect:

- old unread official/institutional messages;
- messages marked read without disposition;
- notifications whose underlying content was never acquired;
- operative attachments never reviewed;
- outbound requests with no recorded response;
- promised later decisions that never arrived;
- bounced/failed routes not reconciled;
- alerts closed without action evidence;
- repository/Drive divergence;
- monitoring-system degradation.

## 13. Watchdog of the watchdog

Alerting must not depend exclusively on one CI host.

If Gmail/Drive/repository connector access, GitHub Actions, GitLab runners, automation quota, authentication, or cross-host synchronisation is degraded, create:

`CONTROL_SYSTEM_DEGRADED`

The degraded state must identify what can no longer be relied upon and the fallback review route.

Absence of an automation run is never evidence that no material communication arrived.

## 14. Repository/public boundary

Public Git contains:

- this governance rule;
- machine-readable policy/schema;
- validators;
- public-safe alert-state examples;
- public-safe event projections already appropriate for publication.

Private Drive/native custody contains:

- source locators;
- raw incoming/outgoing communications;
- unredacted attachments;
- exact private deadlines/strategy where publication is inappropriate;
- the live operational alert ledger.

No private source becomes public merely because it generated an alert.

## 15. Completion standard

A material communication is operationally complete only when all applicable conditions are satisfied:

- source acquired;
- operative attachments reviewed;
- timing/service checked;
- significance classified;
- alert acknowledged;
- owner/disposition assigned;
- dependency recorded;
- required action performed under separate authority;
- action verified from the native destination/source;
- supersession propagated;
- cross-host/private continuity reconciled;
- alert closed with a documented reason.

Anything less remains open or explicitly degraded.
