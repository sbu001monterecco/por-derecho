# Sun Park Evidence & Position-Shift Atlas — worker implementation delta

**Date:** 27 October 2026  
**Type:** Public-safe website code candidate, not a public deployment or a legal finding  
**Thread role:** WORKER under PD-MTCP-20260904-01  
**Base commit:** `25b2fb14a12dad6915f20c166426472dad98f364`  
**Active unrelated integrator observed:** PR #2119, `integration/ph122-thesis-objectives-20261027`

## Task and canonical route

Implement the already controlled bilingual `PD-RICPE-SP-UNITARY-20261023-001/VIS-MULTITRACK-20261027-01` Atlas, linked to the immutable original `PD-PWC-BAND2-ECONOMIC-PERIMETER-20261018-02`. The user authorised the website work; this worker commit is a proposal, not a release permit or an override of the existing integration lane.

## Additive code change

- `en/sun-park-atlas/index.html` and `es/atlas-probatorio-sun-park/index.html`: new language-specific pages with metadata, canonical/alternate links and no-JavaScript static fallback.
- `assets/atlas/atlas-public-v1.en.json` and `atlas-public-v1.es.json`: nine Band 2 markers, eight investigation tracks, distinct value bases, positions, property-perimeter controls and money/status gates. Public-safe same-site source links only.
- `assets/atlas/sun-park-atlas-v1.js` and `.css`: accessible dated cards, track filters, expandable proof gaps, side-by-side dated positions, non-comparable valuation ribbon, historic 54/190/18 perimeter bar, separated finance stages, mobile/print styling.
- `assets/site.js`: append one scoped loader for existing EN/ES Case Control Room, ACTÚA–GESVALT, 262-finca forensic map, RICPE, PwC/Band 2, multiple financial lives, and RICPE–HNT/GC836 pages. No existing loader chain is replaced or removed.

## Evidence and interpretation gates

The underlying nine-stage Band 2 EN/ES original SVGs and filed seven-page TSJC historic annex are untouched. The code contains no private Google Docs, Drive, Gmail, privileged legal documents, native email addresses, bank identifiers, authenticated endpoints, portrait assets or source hashes. Each statement retains its dated issuer/capacity/asset denominator qualification; public chronology is not a guilt or causation inference. Whole-hotel RICS/ECO valuation opinions are not priced on the same denominator as 31 ancillary facilities, and the 54/190/18 statement is not represented as today's title record.

## Tests before integration

1. Verify JSON schema, 8/9 cardinalities and EN/ES parity; all approved same-site links return a valid destination.
2. Run JavaScript syntax, progressive enhancement and no-JS/static fallback smoke tests at mobile and desktop sizes; keyboard toggles, focus visibility and reduced-motion.
3. Run `python3 scripts/validate_repository_preservation.py`, `python3 scripts/validate_publication_integrity.py`, `python3 scripts/validate_audience_experience.py` and relevant project specialists on the exact candidate tree.
4. Compare branch against refreshed current `main`; no deletion, image replacement, existing first-read-content changes or new public claim-source authorities.
5. Privacy, presumption-of-innocence and lawyer/owner editorial review; no private source or portrait leakage; no promotion of allegations.
6. Active integrator must merge or cherry-pick this delta in one controlled release, run required CI and obtain exact-SHA GitHub Pages EN/ES readback. GitLab Pages separately held until its own CI passes.
7. Complete the Control Tower issue #1428 receipt and live route/asset checks. `READY_TO_INTEGRATE` is not `DEPLOYED` or `LIVE_VERIFIED`.

## Existing public reader sources

- `/en|es/actua-gesvalt-2018-valuation-comparison/` (Spanish `comparativa-tasaciones-actua-gesvalt-2018`).
- `/en|es/sun-park-forensic-map-262-properties/` (Spanish `mapa-forense-sun-park-262-fincas`).
- `/en|es/ric-private-equity-sun-park/`, `/en|es/pwc-canarias-carlos-saavedra-sun-park/` and same-hotel financial-life pages.
- `archive/PWC_BAND2_ECONOMIC_PERIMETER_VISUAL_CONTROL_18OCT2026.md` and `ops/PWC_BAND2_LIVE_VERIFICATION_18OCT2026.md` control the prior original figure and boundaries.

**Readiness:** `READY_TO_INTEGRATE` subject to independent validation, legal content gate, current-main rebase/reconciliation and the single-integrator publication workflow. **No autonomous release, sending, filing or public-site deployment.**
