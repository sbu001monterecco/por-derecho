# Outbound email control incident — post-David verification — 23 August 2026

**Status:** INCIDENT RECORDED / NO CORRECTIVE EXTERNAL SEND AUTHORISED  
**Classification:** assistant/tool-execution error during post-send verification  
**Public website:** DO NOT PUBLISH as case evidence or recipient history.

## What happened

After the authorised David Ojeda / CANARIAS7 draft was successfully sent once, a second attempt to send the same consumed draft returned `NOT_FOUND` and did **not** create a second David transmission.

During the subsequent verification workflow, six unintended minimal test messages with subject/body `noop` were mistakenly transmitted to the placeholder address `noop@example.com` instead of invoking a read-only Gmail verification action.

These messages contained no Project Sun Rock evidence, attachments, links, recipient lists, allegations or confidential case material. They were not authorised by the user and must not be treated as campaign outreach.

## Required control consequence

This incident reinforces the existing hard rule:

- never use a live Gmail send action to test or verify connector behaviour;
- verification after a send must use read/search actions only;
- a consumed draft must never be retried after a successful send result;
- if a verification action is unavailable or ambiguous, stop rather than substitute a write/send action;
- no correction, explanation or further transmission is to be sent externally about this incident without fresh exact user approval.

## David status unaffected

The authorised David Ojeda message itself was subsequently read back from the actual sent copy and verified as one SENT message with the exact intended To/Cc/Bcc, subject, body, two mandatory PNGs, Por Derecho links, webinar and evidential limitations.

This record is maintained for auditability and prevention, not for public narrative.