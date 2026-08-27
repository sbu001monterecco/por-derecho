# RICPE channel public-identifier exposure remediation

**Date:** 27 August 2026

**Priority:** P0 privacy hotfix
**Current state:** text correction merged; binary follow-up prepared locally and not yet deployed

## Incident

A no-cache comparison of the public repository and Pages site confirmed that an exact RICPE/Ithikios communication identifier was present in three public text files. PR #1102 merged their correction at `4761cca6366a51c377f6248a2f165430324233c2`. Its Pages deployment then established that the same identifier remained embedded in the public six-page PDF and visibly reproduced in the first rendered page image. The first validator had skipped binaries and therefore produced a false-green result.

Both exposures contradict the pre-existing control that public correlation must use only a one-way SHA-256 fingerprint and that the exact communication/access code and all access credentials remain private.

The incident record deliberately does not reproduce the exact identifier or any credential.

## Current-tree remediation

The first release replaced the exact identifier in:

1. `evidence/ricpe-cnmv/2026-08-27/resolution.txt`;
2. `CURRENT_HANDOVER_RICPE_HNT_GC836_TREASURY_21AUG2026.md`; and
3. `archive/THREAD_DELETION_AUDIT_CRITICAL_STATUS_UPDATE_21AUG2026.md`.

The follow-up release:

1. removes the unredacted PDF and its six old public render paths from the current tree;
2. publishes an honestly labelled PDF derivative with the private identifier redacted;
3. regenerates all six public page images from that derivative under a new path;
4. preserves the unredacted original under private custody and records its existing source hash without reproducing the identifier;
5. corrects the public page and manifest so neither describes the derivative as the unaltered original; and
6. makes the privacy workflow unconditional and fail-closed over text, PDF extraction and the exact controlled binary hashes.

The only permitted public correlation value remains the approved SHA-256 fingerprint. `scripts/validate_ricpe_channel_identifier_privacy.py` now normalises UUID case, scans all current-tree text, rejects the known unsafe PDF/image hashes, requires the obsolete public paths to be absent, extracts and scans the redacted PDF text, and locks every public derivative to its reviewed hash.

## Limits and required closeout

- Correcting current HEAD does not remove prior bytes from Git history, mirrors, caches or previous deployments.
- The exact identifier must not be copied into a commit message, pull-request body, issue, action log or deletion audit.
- The separate channel access credential has not been published or inspected by this remediation. The platform owner should determine whether the identifier had any access function and whether the separate credential should be rotated.
- A successful merge is not enough. No-cache live readback must establish that the three text files contain the approved fingerprint label; the obsolete PDF/image URLs are absent; the new PDF and all six images match the reviewed redacted binaries; and PDF extraction and page-one visual inspection show no protected identifier.
- Historical remediation must not rewrite shared Git history without a separately reviewed necessity, recovery and coordination plan.

## Release order

Publish this binary-complete privacy correction before the larger FTI/Meeting Point/RICPE merits update so that the wider review cannot delay removal of current public exposure.

No email, filing, push, merge, deployment or credential change is authorised by this record.
