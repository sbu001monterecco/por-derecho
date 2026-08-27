# RICPE channel public-identifier exposure remediation

**Date:** 27 August 2026

**Priority:** P0 privacy hotfix
**Current state:** prepared locally; not yet merged, deployed or live-verified

## Incident

A no-cache comparison of current `origin/main` and the public Pages site confirmed that an exact RICPE/Ithikios communication identifier was present in three public tracked files. This contradicted the repository's pre-existing control that public correlation must use only a one-way SHA-256 fingerprint and that the exact communication/access code and all access credentials remain private.

The incident record deliberately does not reproduce the exact identifier or any credential.

## Current-tree remediation

The candidate replaces the exact identifier in:

1. `evidence/ricpe-cnmv/2026-08-27/resolution.txt`;
2. `CURRENT_HANDOVER_RICPE_HNT_GC836_TREASURY_21AUG2026.md`; and
3. `archive/THREAD_DELETION_AUDIT_CRITICAL_STATUS_UPDATE_21AUG2026.md`.

The only permitted public correlation value is the approved SHA-256 fingerprint already recorded in the RICPE channel controls. `scripts/validate_ricpe_channel_identifier_privacy.py` scans the complete current tree, hashes every UUID-shaped candidate and fails if any candidate resolves to that fingerprint. It therefore detects the exposed code without storing it inside the validator.

## Limits and required closeout

- Correcting current HEAD does not remove prior bytes from Git history, mirrors, caches or previous deployments.
- The exact identifier must not be copied into a commit message, pull-request body, issue, action log or deletion audit.
- The separate channel access credential has not been published or inspected by this remediation. The platform owner should determine whether the identifier had any access function and whether the separate credential should be rotated.
- A successful merge is not enough. No-cache live readback must establish that the three current public files contain the approved fingerprint label and no exact-code label/value.
- Historical remediation must not rewrite shared Git history without a separately reviewed necessity, recovery and coordination plan.

## Release order

Publish this privacy correction before the larger FTI/Meeting Point/RICPE merits update so that the wider review cannot delay removal of current public exposure.

No email, filing, push, merge, deployment or credential change is authorised by this record.
