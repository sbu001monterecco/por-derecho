# Outbound canonical-reference and package-object hard gate

**Control date:** 30 September 2026  
**Status:** CONTROLLING FAIL-CLOSED SUPPLEMENT  
**Scope:** every substantive Project Sun Rock / Por Derecho outbound email, reply, resend, correction, follow-up, preservation request, regulator/professional-body notice, law-firm/compliance escalation, investor communication and media package  
**Parent controls:** `archive/OUTBOUND_EMAIL_COMMUNICATIONS_PROTOCOL_23AUG2026.md`, `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`, `archive/PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md`

## 1. Why this hard gate exists

The 30-Sep-2026 Cuatrecasas protected-reporting escalation was substantively source-disciplined but exposed a canonical-control failure. The exact email was sent once and verified in Gmail, but the pre-send process did not instantiate the package as one canonical communication object. The sent PDF also carried two different repository commit references, some controlled entities were not given their required first-reference forms, locally invented exhibit IDs were not registered as canonical IDs, and the final person/organisation Gmail-history gate was not recorded in the required pagination-complete format after the last package changes.

The corrective rule is **not** to send another email automatically. The corrective rule is to make future packages fail closed before transmission.

## 2. One communication = one canonical object

Before an important outbound draft may be marked **READY**, assign:

`COMMUNICATION_ID → CONTROLLING_VERSION → SOURCE_CUTOFF → RECIPIENT_SET → MESSAGE_CLASS → CANONICAL_PACKAGE_MANIFEST`

No material outbound package may reach **AUTHORISED** without those fields.

For the 30-Sep-2026 Cuatrecasas send, the retrospective public-safe identifier is:

`CUA-COM-001`

A communication ID is an internal continuity/control identifier. It is not a court, regulator or third-party reference and must never be presented as one.

## 3. Mandatory canonical package manifest

Every important package must have a manifest, private where necessary and public-safe where appropriate, containing at minimum:

- `communication_id`;
- controlling version;
- source cutoff date/time;
- recipient roles and exact recipient set in the private record;
- audience lane / message class / channel status;
- exact subject;
- exact body fingerprint or approved-body reference;
- canonical entity/proceeding check result;
- material-proposition source map;
- Attachment Manifest;
- Link Manifest;
- Gmail person-history gate result;
- Gmail organisation-history gate result;
- pagination status for every query family;
- repository parity state;
- final approval state;
- sent-copy verification state;
- exact sent attachment fingerprints; and
- immutable sent-package preservation state.

If any mandatory field is missing:

**SEND STATUS: BLOCKED — CANONICAL PACKAGE OBJECT INCOMPLETE.**

## 4. Canonical entity and proceeding rule

Before final approval, every controlled entity, person and proceeding must be checked against the relevant canonical register.

For entities covered by `ops/CANONICAL_ENTITY_NAMES.json`:

- use the exact `first_reference` form on first narrative mention;
- use the controlled acronym thereafter;
- never shorten the first reference merely because the recipient probably knows the entity;
- never invent or translate the legal name; and
- source literals with a different form must be labelled as source literals.

Examples:

- `Luchy Playa Blanca, S.L.U. (LPB)` on first reference;
- `Matkator, S.L.U.` on first reference;
- `AWESWELL LIMITED` for current assertions.

A package with a controlled entity used only in an unqualified acronym or shortened noncanonical form fails the canonical-name check.

## 5. No ad hoc “canonical” source IDs

An outbound PDF, annex or email may not invent an ID and present it as canonical unless that ID resolves to a repository/private source register.

If a temporary pack-local identifier is useful, label it expressly:

`PACK_LOCAL_EXHIBIT_ID`

and separately map it to the true source locator.

Thus:

- `CUA-2020-06-03-A` may be used as a pack-local exhibit label only if the manifest maps it to the underlying mailbox/source record;
- it must not be described as a canonical source ID unless registered in the controlling evidence system.

## 6. Material-proposition source map

Every material factual proposition in an important institutional/compliance package must map internally to:

`PROPOSITION → EVIDENCE STATUS → SOURCE ID/LOCATOR → WHAT IT PROVES → WHAT IT DOES NOT PROVE → CONTRARY/LIMITING EVIDENCE`

The recipient-facing email need not be cluttered with an internal source ID after every sentence. But for **Level 2 / Level 3 evidential packages** sent to authorities, professional bodies, law firms, auditors, compliance functions or institutional custodians, either the email or the first pages of the attachment must contain a compact **Reference Control** block with:

- `COMMUNICATION_ID`;
- package version;
- source cutoff;
- principal proceeding/file references;
- attachment canonical ID / filename;
- attachment SHA-256;
- canonical public dossier links; and
- the source-register location for the material anchors.

## 7. Attachment Manifest — hard requirements

For every attachment record:

`CANONICAL_ASSET_ID → exact filename → language → version/date → source/type → primary/derivative → evidence status → reason → bytes → SHA-256 → prior-supply status → canonical-store status`

Before send:

- exact attachment bytes must be fixed;
- the manifest SHA-256 must be computed from those bytes;
- any PDF or evidence bundle must have a single controlling filename;
- duplicate suffixes and ambiguous `final-final` names are prohibited;
- all internal commit/reference statements inside the PDF must agree with the controlling manifest; and
- if a newer repository commit is inserted into an older PDF, the whole PDF must be reconciled so it does not carry two contradictory “canonical source commit” values.

If the PDF contains inconsistent controlling hashes/versions:

**SEND STATUS: BLOCKED — ATTACHMENT INTERNAL VERSION DRIFT.**

## 8. Canonical Google Drive preservation

For a substantive sent PDF or evidence bundle:

1. the exact final bytes must be preserved in the appropriate canonical Google Drive matter folder before final success is claimed, or immediately after Gmail sent-copy verification if the connector only exposes the exact sent bytes post-send;
2. the Drive copy must be read back / searched and verified;
3. the exact sent SHA-256 and byte size must be bound to the canonical communication manifest; and
4. never replace the exact sent artifact silently. A later corrected internal version receives a new version/canonical asset ID.

A package may be sent before Drive preservation only where the final exact sent bytes cannot be established until sent-copy readback. In that case success remains:

`SENT + VERIFIED / CANONICAL PRESERVATION PENDING`

until Drive verification is complete.

## 9. Link Manifest — hard requirements

Every outbound link must be listed with:

- exact URL;
- category;
- language;
- reason;
- canonical route name;
- repository commit or official-source reference where relevant;
- live verification timestamp/result; and
- correction-state result.

For GitHub Pages / repository-controlled pages, the final link check must occur **after the last material repository merge affecting the linked page**.

A pre-merge or pre-final-change link check does not carry forward automatically.

## 10. Repository parity / exception field

The manifest must record separately:

- GitHub controlling state;
- GitLab controlling state;
- live-page deployment state; and
- whether any repository is staged/unmerged/red.

A red or staged mirror does not automatically block an outbound package where another explicitly designated repository is controlling, but the manifest must say so and the email/PDF must not imply parity that does not exist.

## 11. Gmail history gate cannot remain implicit

A broad mailbox scan is not enough. Immediately before final approval — and again before send if the package materially changes — the readiness record must contain the exact fields required by `archive/PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md`.

The package fails closed unless it expressly says:

`PERSON GMAIL SCAN = COMPLETE`  
`ORGANISATION GMAIL SCAN = COMPLETE`  
`PAGINATION = EXHAUSTED`  
`HISTORY-GATE RESULT = PASS`

with query-family and collision notes in the private record.

## 12. External prior-notice references

When an email says “previously notified”, “earlier whistleblowing communication”, “existing complaint”, “same matter” or equivalent, the manifest must identify the prior communication(s) by date, subject/reference and status.

For high-stakes institutional/compliance messages, include a compact visible prior-notice chronology if it materially assists traceability.

## 13. Legal-authority references

Where a package invokes a statutory protection or legal rule as a material basis for action, the manifest must include the exact legal authority and an authoritative URL/source.

For example, an anti-retaliation package invoking Article 36.2 of Ley 2/2023 should map the proposition to the BOE text and separately map EU/German/UK protections to their authoritative sources.

## 14. Mandatory pre-send consistency audit

Immediately before presenting the exact package for approval, test:

- one and only one `COMMUNICATION_ID`;
- one controlling version;
- one source cutoff;
- no conflicting repository commit/hash claims inside attachments;
- canonical first references;
- no unregistered/ad hoc “canonical” IDs;
- proposition-source map complete;
- Attachment Manifest complete;
- Link Manifest complete and live-verified after the last change;
- Gmail dual history gate PASS;
- repository parity/exception recorded;
- exact attachment hashes fixed;
- canonical preservation plan fixed;
- exact body/subject/recipients read back from draft.

Any failure returns the package to **PREPARED / BLOCKED**.

## 15. Post-send immutable sent-package record

After an authorised send:

1. read the native sent message;
2. verify recipients/body/links/attachments;
3. hash the exact sent attachment bytes where retrievable;
4. preserve the exact sent PDF/bundle in canonical Drive;
5. create/update the public-safe communication manifest without private addresses, Gmail IDs or private message bodies;
6. preserve exact recipient/message identifiers only in private custody; and
7. classify any discrepancy.

## 16. Discrepancy classes — do not auto-resend

A post-send defect must be classified as one of:

### A. INTERNAL_CANONICAL_CONTROL_DEFECT

Examples:
- missing internal `COMMUNICATION_ID`;
- missing manifest;
- missing first-reference legal form where identity is nevertheless unambiguous;
- inconsistent repository commit labels inside an otherwise accurate pack;
- failure to preserve exact sent bytes in Drive before declaring success.

Default action:

**NO RESEND. Correct the controls, preserve the immutable sent artifact, and update future rules.**

### B. MATERIAL_RECIPIENT_CONTENT_DEFECT

Examples:
- wrong recipient;
- missing required attachment;
- materially false legal/factual proposition;
- incorrect operative proceeding/reference that could mislead the recipient;
- wrong attachment version that changes substance.

Default action:

**DO NOT AUTO-CORRECT. Assess materiality, prepare a separate correction package, and obtain fresh user authorisation.**

## 17. Hard-stop output

No important outbound package may be described as “green”, “ready”, “canonical” or “send correctly now” unless the readiness record includes:

`CANONICAL PACKAGE OBJECT = PASS`  
`CANONICAL ENTITY CHECK = PASS`  
`PROPOSITION SOURCE MAP = PASS`  
`ATTACHMENT MANIFEST = PASS`  
`LINK MANIFEST = PASS`  
`GMAIL HISTORY GATE = PASS`  
`ATTACHMENT INTERNAL VERSION = PASS`  
`CANONICAL PRESERVATION PLAN = PASS`

The final-authorisation rule remains independently controlling.
