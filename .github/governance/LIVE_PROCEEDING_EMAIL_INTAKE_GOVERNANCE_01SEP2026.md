# Live proceeding email intake governance

**Control ID:** `PD-LPEI-001`  
**Control date:** 2026-09-01  
**Status:** `ACTIVE_SPECIALIST_CONTROL`  
**Workspace:** `PD-WS-20260901-0004`  
**Scope:** every newly acquired email or email attachment that may update a live or historically controlled proceeding, expediente, authority communication, filing, response, hearing, deadline, order, service event or related operational state.

## 1. Purpose

This control makes new-email processing deterministic, append-only, provenance-backed and continuity-safe. It prevents a new email from silently overwriting an existing proceeding record or creating a second shadow register.

The canonical chain is:

`native/private source -> public-safe source derivative -> canonical communication/procedural event -> assertions -> proceeding linkage -> derived current state -> actions/deadlines -> continuity handoff`

The canonical public communications graph remains `assets/data/institutional-communications-register-v1.json`. Proceedings remain linked through `archive/PROCEEDINGS_MASTER_REGISTER.csv` and its governed public projections. This control does **not** establish a separate email-event ledger.

## 2. Public/private boundary

The repository is public. Native private evidence therefore remains outside public Git in an authorised source system or private vault.

Never commit merely because an email was acquired:

- raw private email bodies;
- provider Message-IDs, thread IDs or private mailbox locators;
- unnecessary sender/recipient/CC identities or email addresses;
- signatures, phone numbers, addresses or unnecessary personal identifiers;
- privileged advice or live legal strategy;
- unredacted protected attachments;
- authentication-bearing URLs, tokens or credentials.

A public record may contain only the minimum approved derivative needed for continuity and evidence graph operation: stable opaque source reference, public-safe date, official or proceeding reference, authority/office where safely publishable, hash/provenance status where approved, public-safe attachment references, evidence status, assertions, links, actions and limitations.

Private capture may retain full native metadata and hashes. Public Git must not reconstruct private evidence from those private fields.

## 3. Mandatory intake sequence

### Gate A — acquire and preserve the source

Preserve the native message and attachments in the authorised private source system. Record enough private custody metadata to deduplicate the item, including provider/native identifier when available, content hash and attachment hashes. Do not publish those private identifiers merely to prove custody.

### Gate B — deduplicate before interpretation

An intake rerun must be idempotent. Match in this order when available:

1. native/provider identifier in private custody;
2. native message/content hash;
3. attachment hashes plus received timestamp/context;
4. existing opaque source reference or exact already-controlled official reference.

A rerun of the same source links to the existing event. It must not create another `PD-SP-EVT-*` row merely because the source was rediscovered.

### Gate C — resolve the proceeding or expediente

Resolve against canonical identifiers, not email subject alone. Permitted resolution evidence includes:

- canonical proceeding ID or controlled proceeding reference;
- NIG, expediente, EG/DI/DIP/RPL/DP/PO or equivalent official reference;
- authority plus exact official reference;
- existing correspondence relationship already proved in the graph;
- attachment text or official act that expressly identifies the proceeding.

Subject-only matching is prohibited. If attribution remains ambiguous, record `UNRESOLVED` or `DISPUTED`; do not mutate a proceeding's derived current state.

### Gate D — append one canonical event

Create or reconcile one stable canonical communication/procedural event in the existing graph. Use the next collision-safe `PD-SP-EVT-*` ID only after current-main reconciliation and duplicate checking.

The event must identify its record type, date, direction/channel, public-safe authority/office where relevant, official/matter references, proceeding links, source-integrity status, evidence state and explicit limitations.

### Gate E — extract assertions, not unsupported facts

Every material proposition from the email or attachment is initially an assertion unless independently established by a controlling source.

For each state-changing assertion record:

- field or proposition affected;
- prior controlled value where applicable;
- newly asserted value;
- effective date/time if the source states one;
- verification status: `VERIFIED`, `UNVERIFIED` or `DISPUTED`;
- public-safe source/event reference;
- whether it confirms, supplements, contradicts, corrects or supersedes prior state.

The source's statement is evidence that the statement was made. It is not automatically proof that the asserted underlying fact is true.

### Gate F — preserve supersession

Never delete the old state merely because a later communication changes the operative position.

Use explicit supersession:

- old event/state remains historical and queryable;
- new event records what changed and why;
- current derived state points to the latest controlling, provenance-backed source;
- disputed supersession stays disputed until resolved.

A changed hearing or deadline is the clearest example: preserve the original date and source; mark the later source as superseding it only when the later communication actually establishes that effect.

### Gate G — extract operational consequences

Every intake must answer whether it creates, changes or cancels:

- a filing or appeal deadline;
- a hearing or appearance;
- a response window;
- a document-production request;
- a preservation request;
- a payment/security/procedural requirement;
- a follow-up, counsel or procurador action;
- a verification task.

For each action retain description, source assertion/event, due date/time where stated, `Atlantic/Canary` timezone unless the source establishes another applicable zone, verification status, owner/workstream where controlled, status and any superseding/cancelling event.

No deadline may exist without a trigger/source. If a deadline is calculated rather than expressly stated, label the calculation and its assumptions; do not present it as an official date.

### Gate H — refresh interlinks and search

The new event must be discoverable through all applicable controlled dimensions:

- proceeding and proceeding reference;
- NIG/expediente/official reference;
- authority/court/office;
- canonical person/entity identifiers where publication is appropriate;
- antecedent/successor or related proceeding;
- filing/response/decision relationship;
- evidence/attachment derivative;
- chronology;
- public-authority communications route where relevant;
- ACTA/community or other subject graph where already controlled.

Official references such as expediente numbers must be included in the public-safe searchable derivative whenever publication is lawful and authorised. This is required so exact-reference queries can surface the event rather than depending on narrative text.

### Gate I — contradictions require review

The intake system never guesses through a material conflict. Create a review item where a new communication conflicts with an existing source concerning service, hearing date, appeal period, operative order, party/capacity, filing status, official reference, amount, title or other consequential state.

The state must be explicitly `VERIFIED`, `UNVERIFIED` or `DISPUTED` until the conflict is resolved by adequate evidence.

### Gate J — checkpoint continuity

Before the workspace is treated as deletion-safe, record:

- what source arrived;
- which proceeding(s)/authority event(s) it affected;
- the new canonical event ID;
- what changed in derived current state;
- what was only asserted;
- what was superseded;
- contradictions/open verification;
- actions/deadlines;
- changed repository/publication/search artifacts;
- the exact next unresolved task.

A successor thread must be able to resume from repository state without needing the originating chat.

## 4. Public-safe intake object

The transient/public-safe intake object used to reconcile an email update into the canonical graph follows this shape. It is an interchange object, **not a second canonical register**.

```yaml
event_id: PD-SP-EVT-####
event_type: email_update
source:
  private_source_ref: PD-PSRC-...
  received_at: YYYY-MM-DDTHH:MM:SS+01:00
  content_hash_status: PRIVATE_CUSTODY_ONLY | PUBLIC_HASH_APPROVED
  public_attachment_refs: []
proceeding:
  proceeding_ids: []
  resolution_basis: []
  resolution_status: RESOLVED | UNRESOLVED | DISPUTED
search_terms:
  official_references: []
  proceeding_references: []
  authority_references: []
change_types: []
assertions:
  - field: ""
    prior_value: null
    asserted_value: null
    effective_at: null
    verification_status: UNVERIFIED
    source_ref: ""
supersedes: []
actions:
  - action_id: PD-ACT-...
    description: ""
    due_at: null
    timezone: Atlantic/Canary
    source_assertion: ""
    verification_status: UNVERIFIED
    status: OPEN
review:
  required: false
  reason: null
continuity:
  workspace_id: PD-WS-20260901-0004
  processed_at: YYYY-MM-DDTHH:MM:SS+01:00
  handoff_ref: ""
```

The machine control is `ops/LIVE_PROCEEDING_EMAIL_INTAKE_V1.json`.

## 5. Relationship to the canonical communications register

An email intake object is reconciled into `assets/data/institutional-communications-register-v1.json` only after source/proceeding resolution and privacy review.

Where the communication is from or to a public authority, preserve the existing distinction between transmission, registration, delivery, routing, incorporation, examination, verification/rejection, adoption, decision/use, effect, causation and benefit/loss. Receipt at one stage never proves later stages.

Where the communication is counsel, court, procurador, professional adviser or another actor rather than an authority, use the same evidence-status discipline and link to the relevant proceeding/actor graph without pretending that authority-specific handling states apply.

## 6. Acceptance gate

An email-update intake is complete only when all applicable statements below are true:

1. native source is preserved in authorised private custody or the source is independently public;
2. duplicate check completed;
3. proceeding resolution is `RESOLVED`, `UNRESOLVED` or `DISPUTED` with recorded basis;
4. canonical event is appended or existing event reused;
5. attachments are linked, not duplicated, and public/private boundary is respected;
6. material assertions have provenance and verification state;
7. derived current-state changes are traceable and prior state remains preserved;
8. deadlines/actions are captured, or the intake affirmatively records that none were identified;
9. contradictions receive review rather than guessed resolution;
10. exact official/proceeding references are added to controlled search fields where publishable;
11. required interlinks/builds are refreshed;
12. continuity handoff/checkpoint is updated.

## 7. Non-negotiable failure conditions

The intake must fail closed for the affected mutation when any of these occurs:

- silent overwrite of historical state;
- subject-only proceeding match;
- duplicate event on rerun;
- unsupported state mutation;
- deadline without provenance/trigger;
- assumption-based contradiction resolution;
- publication of raw/private email identifiers or protected content;
- invented linkage between an attachment and a filing/receipt/proceeding;
- a current-state field with no traceable source event;
- creation of a parallel/shadow email register.

## 8. Operational files

- governance: `.github/governance/LIVE_PROCEEDING_EMAIL_INTAKE_GOVERNANCE_01SEP2026.md`
- machine control: `ops/LIVE_PROCEEDING_EMAIL_INTAKE_V1.json`
- specialist validator: `scripts/validate_live_proceeding_email_intake.py`
- CI: `.github/workflows/audit-live-proceeding-email-intake.yml`
- canonical communications graph: `assets/data/institutional-communications-register-v1.json`
- proceedings source: `archive/PROCEEDINGS_MASTER_REGISTER.csv`
- public proceedings projection: `assets/data/proceedings-master-public-v1.json`
- authority discovery projection: `assets/data/redsara-age-filings-register-v1.json`
- workspace register: `data/workspace-register-v1.json`
- continuity index: `CURRENT_WORKSPACE_HANDOFF.md`

## 9. Enforcement mode

This is an active **specialist** control. Its workflow validates this governance package and its machine-readable contract when relevant files change. It does not become a new universal required reviewer or deployment dependency and does not authorise mailbox access, sending email, filing, service, portal action or third-party contact.

When an authorised agent receives a new email update to a live proceeding, this control is mandatory for repository processing.