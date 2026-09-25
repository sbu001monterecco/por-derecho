# READ FIRST — visual asset identity

Any task that uses a named person's image on the Por Derecho website, in an infographic, email, PDF, Word document or presentation must first read:

- `archive/knowledge-project/VISUAL_ASSET_IDENTITY_GOVERNANCE_19AUG2026.md`
- `assets/visual-asset-registry.json`
- the relevant `assets/composites/*.asset-map.json` sidecar

## Non-negotiable rule

**Do not identify or assign a real person's portrait from appearance, prompt order, filename guess or conversational proximity. Resolve the exact canonical asset ID.**

## Critical current mapping

- Gil Marer / official base portrait:
  - `person.gil-marer.official-base`
  - `assets/actors/gil-marer--official-base--20260921.webp`
  - User-supplied self-portrait, user-approved cleaned/stylised derivative; use as the official base reference for future visual work unless explicitly superseded.
- Francisco de Borja Rodríguez-Batllori Laffitte / Administrador Concursal:
  - `person.francisco-de-borja-rodriguez-batllori.primary`
  - `assets/actors/francisco-de-borja-rodriguez-batllori.jpg`
- Eduardo Sánchez / San Telmo:
  - `person.eduardo-sanchez-san-telmo.primary`
  - `assets/actors/eduardo-sanchez-san-telmo.url` — a byte-locked repository pointer to the first-party RSM profile image corresponding to the user-authorised portrait.

Gil's official base portrait is active and byte-locked for future visual derivatives. The Eduardo Sánchez and Borja / AC assets are both active and carry reciprocal `do_not_confuse_with` locks. The controlling composite slot map is `assets/composites/san-telmo-ricpe-sun-park-stamp-v1.asset-map.json`.

Run before merge:

```bash
python scripts/validate_visual_asset_registry.py
```


## Hard named-person rendering rule — 25 September 2026

> **25-Sep-2026 named-person visual integrity override — PD-VISUAL-FACE-NOGEN-20260925-01:** before creating or editing any visual containing a named real person, read `governance/FACE_IDENTITY_CONTROL_RULE.md` and `assets/data/named-person-visual-control-v1.json`. Named faces are **DETERMINISTIC_COMPOSITING_ONLY**: exact approved source pixels or exact repository `<img>` assets; no generative face reconstruction, replacement, inpainting, approximation or synthetic likeness. Substantive poster text must come from a reviewed manifest/page source. Missing source or fact = halt/report, never invent. The rejected JTP generations are quarantined in `archive/AI_IMAGE_HALLUCINATION_INCIDENT_JTP_25SEP2026.md`.

Run before merge:

```bash
python scripts/validate_named_person_visual_control.py
```
