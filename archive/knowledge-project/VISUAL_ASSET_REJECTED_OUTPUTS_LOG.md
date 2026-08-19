# Visual asset rejected-output log

## 19 August 2026 — San Telmo / RICPE / Sun Park infographic drafts

### Rejected mapping

A generated draft placed the user-supplied portrait subsequently confirmed by the user as **Eduardo Sánchez** into the slot labelled **Francisco de Borja Rodríguez-Batllori Laffitte / Administrador Concursal**.

### Status

`REJECTED — MUST NOT BE UPLOADED, PUBLISHED, EMAILED OR REUSED`

### Controlling correction

- Borja / AC must resolve to:
  - `person.francisco-de-borja-rodriguez-batllori.primary`
  - `assets/actors/francisco-de-borja-rodriguez-batllori.jpg`
- Eduardo Sánchez must resolve to:
  - `person.eduardo-sanchez-san-telmo.primary`
  - currently `USER_CONFIRMED_PENDING_REPOSITORY_IMPORT`

### Root cause

Portrait assignment was performed from conversational attachments and prompt order instead of the canonical asset registry and an explicit visual slot map.

### Preventive control

The following are now mandatory:

- `assets/visual-asset-registry.json`
- `VISUAL_ASSET_IDENTITY_GOVERNANCE_19AUG2026.md`
- composite `.asset-map.json` sidecars
- `scripts/validate_visual_asset_registry.py`
- CI visual-asset identity gate

The rejected draft is not evidence and must not be treated as a source image for either person.
