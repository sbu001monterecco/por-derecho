# DEPLOYMENT / VERIFICATION LOG — PEP + PROCEEDINGS — 20 AUGUST 2026

**Purpose:** supplement `archive/DEPLOYMENT_LOG.md` for the two closely connected publication cycles closed in this thread family.

## Repository publication

### Proceedings propagation
- PR: **#662 — Propagate verified proceedings to public-safe website records**
- Merge commit: `3c1cc2ed878bdef43ba8f62fa406dc57fa8da591`
- Current-main source read-back: **VERIFIED**
- Surfaces: Pink Canary / AEAT / Audiencia Nacional 496/2026; Cuatrecasas ICAM/CCACM proceeding boundary; institutional records incl. CGPJ Alzada 286/2026, Q26/574 and LAJ coordinated filing chain.

### Private-actor PEP / influence / aforamiento / PER audit
- PR: **#666 — Add PEP, influence, aforamiento and related-person audit**
- Merge commit: `9d49573d6f40b98549bfa8910bd7bab5454719f9`
- Current-main source read-back: **VERIFIED in EN and ES**
- Surfaces:
  - `en/private-actors-pep-influence-aforamiento-related-persons/`
  - `es/actores-privados-pep-influencia-aforamiento-personas-relacionadas/`
  - inbound links in the EN/ES actor registers.

## Rendered-site verification state

A dedicated verifier is now present on `main`:
`.github/workflows/verify-pep-proceedings-live.yml`

It checks ten production routes with cache-busting/retry and requires:
- HTTP 200;
- non-trivial response size;
- exact page-specific content markers;
- EN/ES parity markers;
- a JSON verification artifact.

**Observed state at this close-out:** the repository source is merged and read back; the external browser/search layer available to this thread did not provide a fresh direct fetch of the new routes, and the connector used here does not expose a list operation for push-triggered workflow runs. Therefore a successful live run is **not claimed** merely from the workflow’s existence.

This is a finite, explicit deployment-evidence item, not a conversation-memory dependency. A fresh thread can retrieve/observe the workflow run or repeat a lawful direct HTTP read-back and update this log.

## QA/non-regression

For PR #666:
- changed-file publication integrity: PASS;
- operational integrity: PASS;
- visual asset identity: PASS;
- public bidder preservation: PASS;
- off-GitHub preservation snapshot: PASS.

The aggregate publication-integrity workflow was red solely because the repository-wide mission-critical validator identified a pre-existing unrelated `statuses: write` permission in `.github/workflows/verify-eleconomista-live.yml`. PR #666 did not alter that workflow; the non-regression condition was recorded before merge.

## Deletion-continuity effect

The absence of an observed fresh live read-back does not leave substantive intelligence trapped in chat. Repository state, URLs, expected markers, verifier logic and the exact remaining action are all preserved. The correct thread close-out is therefore **DELETION-SAFE WITH OPEN EVIDENCE**, not an unqualified claim of live deployment.