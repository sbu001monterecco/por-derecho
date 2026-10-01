# Canonical Outbound Communication Object (COCO) — fail-closed gate

**Control ID:** PD-COMMS-COCO-20261001-01  
**Adopted:** 1 October 2026  
**Status:** mandatory fail-closed supplement to all Project Sun Rock / Por Derecho outbound-email controls

## Core rule

No material external email may be described as `READY`, `READY FOR AUTHORIZATION`, `GREEN` or equivalent unless a single canonical outbound communication object exists and every applicable gate below is PASS.

A well-researched email is not a canonical outbound package unless the object exists.

## Required object

```text
COMMUNICATION_ID =
CONTROLLING_VERSION =
MESSAGE_CLASS =
AUDIENCE_LANE =
SOURCE_CUTOFF =
RECIPIENT_SET =
CANONICAL_ENTITY_RESOLUTION =
PERSON_GMAIL_SCAN =
ORGANISATION_GMAIL_SCAN =
PAGINATION =
COLLISION_CLASSIFICATION =
ATTACHMENT_MANIFEST =
LINK_MANIFEST =
PUBLIC_MIRROR_GATE =
DRAFT_ID =
DRAFT_READBACK =
APPROVAL_STATE =
SENT_MESSAGE_REF =
SENT_READBACK =
REGISTER_BACKFILL =
```

Before authorization, `SENT_MESSAGE_REF`, `SENT_READBACK` and `REGISTER_BACKFILL` may be `PENDING_NOT_SENT`; every other applicable field must be PASS or a precisely recorded user-approved one-use exception.

## Fail-closed rule

Any missing applicable field =

`SEND STATUS: BLOCKED — CANONICAL OUTBOUND COMMUNICATION OBJECT INCOMPLETE`

Do not downgrade a mandatory field to "where practical".

## Canonical entity gate

Resolve every named controlled entity/person against `ops/CANONICAL_ENTITY_NAMES.json`.

For each resolved record persist:
- record ID;
- canonical name;
- first-reference form;
- any source-literal exception used;
- any forbidden alias scan result.

The first narrative mention must use the controlled first-reference form.

## Attachment manifest

Every attachment must record:
- exact filename;
- bytes;
- SHA-256 where accessible;
- page count where applicable;
- language;
- source class;
- primary / derivative status;
- controlling version/date;
- reason for inclusion;
- evidence limitation;
- communication-object ID.

A regenerated file with the same filename but different bytes invalidates the prior manifest and authorization.

## Link manifest

Every link must record:
- exact URL;
- category;
- language;
- recipient-specific purpose;
- live-read result and timestamp;
- correction state;
- mirror relationship where applicable.

## Former-professional public-mirror gate

For material former-counsel / former-professional communications, apply `PD-FCCOM-MIRROR-CYBER-20260926-01`.

The COCO may pass only where:
- GitHub Pages live-read = PASS;
- GitLab Pages live-read = PASS;
- material parity = PASS;

or the user expressly approves a one-use exception for the exact transmission and exact missing mirror.

A blocked/unavailable mirror must be disclosed as BLOCKED; it must not be silently omitted.

## Gmail history gate

The final package must contain the completed fields required by `archive/PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md`.

If a material body, attachment, link or recipient change occurs after the recorded scan and enough time has elapsed for new correspondence to matter, rerun the gate.

## Repository-commit rule for evidential PDFs

Where a PDF cites repository state, use explicit roles:
- `BASELINE_REPOSITORY_COMMIT`;
- `CONTROLLING_CONTENT_COMMIT`.

Never present two commits as undifferentiated "canonical" commits.

Also persist:
- PDF build timestamp;
- source cutoff;
- SHA-256;
- page count;
- Attachment Manifest ID;
- Communication ID.

## Authorization and send

Only `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md` can move a complete object from PREPARED to AUTHORIZED.

One authorization permits one send.

After send:
1. read the native sent copy;
2. compare recipients/body/links/attachments to the object;
3. register the sent event back into the canonical communications ledger;
4. mark `REGISTER_BACKFILL = PASS`.

No automatic correction, resend or supplement follows from a failed audit.

## Incident origin

This gate closes the control gap identified in `PD-CUA-COMMS-AUDIT-20261001-01`: the 30-Sep-2026 Cuatrecasas package was substantively evidence-controlled and natively read back after send, but lacked a single persisted canonical communication object and missed the mandatory dual-public-mirror rule.

The incident does not itself authorize any new communication.
