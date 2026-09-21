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
  - `assets/actors/eduardo-sanchez-san-telmo.url` — a byte-locked repository pointer to the first-party RSM profile image corresponding to the user-authorised portrait.

The Eduardo Sánchez and Borja / AC assets are both active and carry reciprocal `do_not_confuse_with` locks. The controlling composite slot map is `assets/composites/san-telmo-ricpe-sun-park-stamp-v1.asset-map.json`.

Run before merge:

```bash
python scripts/validate_visual_asset_registry.py
```
