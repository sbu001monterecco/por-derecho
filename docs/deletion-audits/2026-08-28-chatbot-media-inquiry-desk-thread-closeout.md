# Continuity and deletion audit — chatbot / controlled media inquiry desk

**Control date:** 28 August 2026

**Control ID:** `PD-CHATBOT-MEDIA-DESK-20260828-01`

**Initial package state:** `REMOTE_SOURCE` after remote branch preservation

**Target verdict after merge/live readback:** `DELETION-SAFE WITH OPEN IMPLEMENTATION`

## Scope preserved

The canonical control
`CHATBOT_MEDIA_INQUIRY_DESK_CONTROL_28AUG2026.md` preserves:

- the Ask the Record / Pregunta al expediente product decision;
- the controlled journalist-first release and owner-only Stage 0;
- the fixed answer contract and visible answer lenses;
- the recovery objective without litigation prediction;
- the qualified treatment of judicial-independence concerns;
- the entity, claimant, ownership/operation, proceeding and identity perimeters;
- prohibited conclusions, data sources and external actions;
- the exact journalist submission, review and three-authorisation workflow;
- the repository-compiled approved corpus architecture;
- the typed-input and microphone-to-editable-text flow;
- the protected backend and credential-isolation requirements;
- the privacy/legal release gate and initial evaluation programme; and
- the finite reconstruction sequence.

## Lost-source boundary

The exact earlier loopback prototype was stored in a transient scratch path and
was not located in current `main`, surviving worktrees or the durable project
records checked on 28 August 2026. Its code is not represented as recovered.
This is the material open implementation gap.

The requirements and decisions needed for a clean reconstruction are preserved
in the canonical control. No unique known product decision, evidential
qualification, recovery instruction, privacy boundary or restart instruction
from the originating conversation remains solely in chat after this package is
merged and independently readable.

## Credential and API boundary

No credential, token or environment value is preserved in the repository. A
future implementation must independently verify credential lifecycle, provider
access and current quota/billing before testing. Any credential with uncertain
custody must be handled through the official secure platform flow, not copied
from chat or Git history.

## Publication and communication boundary

This package preserves a control specification. It does not deploy a chatbot,
create a phone-accessible link, accept a journalist inquiry, send email, publish
an exchange, file a document or contact an authority. Those actions remain
separately gated.

Automatic Pages publication of public-safe repository control files is not a
release of the chatbot product and does not authorise any data collection.

## Initial verification commands

```bash
python3 scripts/validate_chatbot_media_inquiry_desk_continuity.py
python3 scripts/validate_repository_preservation.py
python3 scripts/validate_publication_integrity.py
python3 scripts/validate_audience_experience.py
git diff --check
```

## Gate interpretation

- A local file or commit is not deletion-safe.
- A remote branch is `REMOTE_SOURCE`, not `DELETION_SAFE`.
- The first merge establishes recoverable source on `main`.
- A final continuity update must record the merge, passing CI/validation and
  independent readback of the canonical control files.
- Because no chatbot product is released here, live verification applies to the
  continuity files, not to an application route.
- Open implementation is compatible with the prose verdict
  `DELETION-SAFE WITH OPEN IMPLEMENTATION` only when the complete requirements
  and restart path are durably recoverable. It is not a claim that the
  executable product exists or works.

## Current open items

1. Reconstruct the Stage-0 loopback prototype from the canonical control.
2. Reconfirm the approved corpus against current `main`.
3. Establish a secure provider credential and verify its lifecycle outside Git.
4. Resolve current API access/quota and test typed answers before transcription.
5. Build and pass the bilingual, adversarial and privacy evaluation.
6. Complete the chatbot-specific privacy/legal/security release review.
7. Obtain separate authority before private deployment, journalist access,
   email release or public Q&A publication.

Open items do not depend on the originating conversation for their definition.
