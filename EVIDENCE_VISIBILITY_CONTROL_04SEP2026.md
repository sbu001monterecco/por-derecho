# Evidence visibility deployment control — 4 September 2026

**Control:** `PD-EVIS-20260904-01`  
**Scope:** repository-wide native-file preservation, searchable text/OCR, source-derived evidence images, redaction and continuity governance  
**Adoption state:** active standard; legacy visual backfill remains partial

## Canonical components

- Policy: `.github/governance/EVIDENCE_VISIBILITY_IMAGE_OCR_REDACTION_AND_CONTINUITY_STANDARD_04SEP2026.md`
- All-role overlay: `.github/governance/EVIDENCE_VISIBILITY_ROLE_CONTINUITY_OVERLAY_04SEP2026.json`
- JSON contract: `.github/evidence-intelligence/schemas/evidence-visibility.schema.json`
- Validator: `scripts/validate_evidence_visibility.py`
- CI: `.github/workflows/validate-evidence-visibility.yml`
- Registered packages: `data/evidence-visibility/`
- Public explanation: `/en/evidence-visibility/` and `/es/visibilidad-evidencia/`
- Runtime presentation: `assets/evidence-visibility-runtime-20260904.js`

## Controlling rule

Every evidence-bearing item must be:

1. preserved or custody-identified;
2. searchable;
3. visually inspectable through source-derived images;
4. redacted through a controlled derivative where necessary;
5. linked to its actors, entities, proceedings, events and pages;

or it must carry a precise, reviewable reason why a state remains pending.

## Current Uría package

`data/evidence-visibility/uria-ricpe-sun-park-20260904.json` is the initial package under this standard.

The relevant native binaries are not currently present in the Git tree. Existing connected-source fingerprints and searchable notes are retained. Visual states are therefore registered as `SOURCE_PENDING`, with no synthetic substitute. Materialisation, redaction review, source-derived page rendering and live asset verification remain controlled follow-up tasks.

## Completeness boundary

This deployment makes the rule, schema, validation and public status presentation operative. It does **not** claim that the historic repository corpus has already been fully rendered into evidence images. Legacy backfill remains an active record-level programme.
