# Canonical actor-image assets

This directory contains identity-controlled images and first-party image pointers for named people.

## Mandatory rule

Do not select a person image by appearance, filename guess, conversational order or prompt proximity.

Resolve the subject through:

`../visual-asset-registry.json`

Every active person asset must have:

- a unique asset ID;
- canonical name and role;
- exact repository path or byte-locked first-party pointer;
- identity basis;
- `LOCKED_CANONICAL_REPOSITORY_ASSET` status;
- byte lock using the Git blob SHA;
- approved alt text;
- explicit exclusions where confusion is possible.

## Current critical distinction

- `person.francisco-de-borja-rodriguez-batllori.primary` → `francisco-de-borja-rodriguez-batllori.jpg`
- `person.eduardo-sanchez-san-telmo.primary` → `eduardo-sanchez-san-telmo.url`, a byte-locked repository pointer to the corresponding first-party RSM profile image, with a first-party San Telmo fallback.

The Eduardo Sánchez asset and the Borja / Administrador Concursal asset remain reciprocal `do_not_confuse_with` locks. The live composite slot map is `../composites/san-telmo-ricpe-sun-park-stamp-v1.asset-map.json`.

## Adding a new portrait

1. Confirm identity from the user or a reliable source; do not infer identity from the face.
2. Use the canonical person slug.
3. Add the file or first-party pointer without overwriting another person's asset.
4. Add or update the registry entry.
5. Add provenance, identity basis, alt text and Git blob SHA.
6. Run `python scripts/validate_visual_asset_registry.py`.
7. For composites, create the required `.asset-map.json` sidecar.

Unregistered images are not publication-ready.
