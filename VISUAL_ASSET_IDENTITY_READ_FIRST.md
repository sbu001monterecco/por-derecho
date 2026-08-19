# READ FIRST — visual asset identity

Any task that uses a named person's image on the Por Derecho website, in an infographic, email, PDF, Word document or presentation must first read:

- `archive/knowledge-project/VISUAL_ASSET_IDENTITY_GOVERNANCE_19AUG2026.md`
- `assets/visual-asset-registry.json`
- the relevant `assets/composites/*.asset-map.json` sidecar

## Non-negotiable rule

**Do not identify or assign a real person's portrait from appearance, prompt order, filename guess or conversational proximity. Resolve the exact canonical asset ID.**

## Critical current mapping

- Francisco de Borja Rodríguez-Batllori Laffitte / Administrador Concursal:
  - `person.francisco-de-borja-rodriguez-batllori.primary`
  - `assets/actors/francisco-de-borja-rodriguez-batllori.jpg`
- Eduardo Sánchez / San Telmo:
  - `person.eduardo-sanchez-san-telmo.primary`
  - currently pending repository import; do not publish a portrait until activated in the registry.

The user-confirmed Eduardo Sánchez image must never be used in the Borja / AC slot.

Run before merge:

```bash
python scripts/validate_visual_asset_registry.py
```
