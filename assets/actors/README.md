# Canonical actor-image assets

This directory contains identity-controlled images of named people.

## Mandatory rule

Do not select a person image by appearance, filename guess, conversational order or prompt proximity.

Resolve the subject through:

`../visual-asset-registry.json`

Every active person asset must have:

- a unique asset ID;
- canonical name and role;
- exact repository path;
- identity basis;
- `LOCKED_CANONICAL_REPOSITORY_ASSET` status;
- byte lock using the Git blob SHA;
- approved alt text;
- explicit exclusions where confusion is possible.

## Current critical distinction

- `person.francisco-de-borja-rodriguez-batllori.primary` → `francisco-de-borja-rodriguez-batllori.jpg`
- `person.eduardo-sanchez-san-telmo.primary` → pending repository import; do not publish a portrait until activated in the registry.

The user-confirmed Eduardo Sánchez upload must never be placed in the Borja / Administrador Concursal slot.

## Adding a new portrait

1. Confirm identity from the user or a reliable source; do not infer identity from the face.
2. Use the canonical person slug.
3. Add the file without overwriting another person's asset.
4. Add or update the registry entry.
5. Add provenance, identity basis, alt text and Git blob SHA.
6. Run `python scripts/validate_visual_asset_registry.py`.
7. For composites, create the required `.asset-map.json` sidecar.

Unregistered images are not publication-ready.
