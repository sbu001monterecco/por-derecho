# Evidence-directory instructions

These instructions apply to every file and subdirectory under `evidence/`.

## Canonical control

All work must comply with:

- `.github/governance/EVIDENCE_VISIBILITY_IMAGE_OCR_REDACTION_AND_CONTINUITY_STANDARD_04SEP2026.md`
- `.github/governance/EVIDENCE_VISIBILITY_ROLE_CONTINUITY_OVERLAY_04SEP2026.json`
- `.github/evidence-intelligence/schemas/evidence-visibility.schema.json`

## Mandatory handling

For every new or materially updated evidence-bearing source:

1. preserve or identify the native source and register its provenance and SHA-256 when available;
2. create or link searchable text/OCR and translation where material;
3. create or link source-derived page/image evidence;
4. declare redaction and sensitivity state;
5. link the item to actors, entities, proceedings, events and public pages;
6. register truthful open gaps under `data/evidence-visibility/`.

A pending native binary must be marked `SOURCE_PENDING` or `PRESERVED_EXTERNAL_CONNECTED_SOURCE`; it must not be treated as a public image merely because a hash or textual note exists.

## Visual integrity

- Never generate, reconstruct or substitute an evidential image.
- Full-page images are the default; crops and highlights are supplemental.
- Preserve page order, parent context and derivative hashes.
- Redacted public images must derive from a separately fingerprinted, technically safe public derivative.
- Searchable text and visual evidence are both required; neither replaces the other.

## Continuity

Every handoff must preserve record-level status, open gaps, next action and owner role. A prose summary alone is not a complete evidence handoff.
