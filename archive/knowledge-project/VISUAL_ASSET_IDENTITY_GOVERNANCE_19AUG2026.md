# Visual asset identity governance — Por Derecho

**Control date:** 19 August 2026  
**Policy ID:** `PD-VISUAL-ID-LOCK-2026-08-19`  
**Status:** mandatory repository, website, document, email and generated-visual rule

## Why this rule exists

A generated draft incorrectly placed a user-supplied portrait of **Eduardo Sánchez** into the visual slot labelled **Francisco de Borja Rodríguez-Batllori Laffitte / Administrador Concursal**. The repository already contained a canonical Borja image at:

`assets/actors/francisco-de-borja-rodriguez-batllori.jpg`

The mistake arose because the visual was assembled from conversational attachments and inferred slot assignment instead of resolving each named subject through a canonical repository asset ID.

This policy prevents recurrence.

## Controlling principle

> **A named person is never an image guess. Every named-person image is a canonical asset with an explicit identity, source, status, path and byte lock.**

The system must never identify, substitute or assign a real person's portrait from apparent facial similarity. It must use the identity supplied by the user/source and the exact repository mapping in `assets/visual-asset-registry.json`.

## Mandatory preflight for every visual containing a named person

Before drawing, generating, compositing, publishing, emailing or inserting the visual into a document:

1. List every named person and every image slot.
2. Resolve each slot to an exact `asset_id` in `assets/visual-asset-registry.json`.
3. Confirm the asset is `LOCKED_CANONICAL_REPOSITORY_ASSET`.
4. Confirm the file or first-party pointer path and Git blob SHA match the registry.
5. Confirm the label, role, alt text and caption come from the same registry entry.
6. Confirm the `do_not_confuse_with` exclusions.
7. Create or verify a slot-map sidecar for any composite containing two or more named people.
8. Stop publication if any required portrait is pending, unregistered, ambiguous or missing.

A visual may use a neutral placeholder when an asset is pending. It may not borrow another person's portrait.

## Canonical identity locks relevant to the San Telmo / RICPE visual

### Borja / Administrador Concursal

- **Asset ID:** `person.francisco-de-borja-rodriguez-batllori.primary`
- **Canonical name:** Francisco de Borja Rodríguez-Batllori Laffitte
- **Canonical role:** Administrador Concursal · Concurso 36/2012
- **Canonical path:** `assets/actors/francisco-de-borja-rodriguez-batllori.jpg`
- **Status:** `LOCKED_CANONICAL_REPOSITORY_ASSET`

### Eduardo Sánchez / San Telmo

- **Asset ID:** `person.eduardo-sanchez-san-telmo.primary`
- **Canonical name:** Eduardo Sánchez
- **Canonical role:** Socio · San Telmo
- **Current status:** `LOCKED_CANONICAL_REPOSITORY_ASSET`
- **Canonical repository pointer:** `assets/actors/eduardo-sanchez-san-telmo.url`
- **Live image source:** the first-party RSM profile URL recorded in `assets/visual-asset-registry.json`
- **First-party fallback:** the San Telmo image URL recorded in the same pointer and registry
- **User-confirmed source file:** `Eduardo Sánchez (1)(1).webp`
- **Source SHA-256:** `a46afb994e6fa0fb309d43fff45b72923a75db39680abc01e10a0c13a52af7d6`

Eduardo’s authorised identity is locked through the byte-locked repository pointer `assets/actors/eduardo-sanchez-san-telmo.url`, which resolves to the first-party RSM professional-profile image and carries a first-party San Telmo fallback. The live San Telmo / RICPE composite must use `person.eduardo-sanchez-san-telmo.primary` in the Eduardo slot and `person.francisco-de-borja-rodriguez-batllori.primary` in the Borja / AC slot. Neither asset may substitute for the other.

### Sun Park / MYND Yaiza

- **Asset ID:** `place.sun-park-mynd-yaiza.aerial-primary`
- **Canonical path:** `assets/sun-park-mynd-yaiza.jpg`
- **Status:** `LOCKED_CANONICAL_REPOSITORY_ASSET`

## Required slot-map rule for composites

Every published composite containing named people must have a machine-readable sidecar named:

`<visual-filename>.asset-map.json`

Example:

```json
{
  "visual_id": "san-telmo-ricpe-sun-park-stamp-v1",
  "slots": {
    "left_portrait": "person.eduardo-sanchez-san-telmo.primary",
    "centre_asset": "place.sun-park-mynd-yaiza.aerial-primary",
    "right_portrait": "person.francisco-de-borja-rodriguez-batllori.primary"
  }
}
```

The sidecar controls which subject belongs in which slot. Layout software, an image-generation model or a later editor must not reinterpret the slots.

## Generated-image rule

Image generation may create:

- background;
- typography concept;
- diagram geometry;
- arrows, framing and decorative elements;
- neutral placeholders.

It must not:

- invent or approximate a named real person's face;
- replace a canonical portrait with a generated likeness;
- infer that an uploaded person is another named person;
- swap portraits because two names occur in the same prompt;
- burn a named face into a final image without a verified slot map.

The safe workflow is:

1. generate the graphic structure with empty labelled portrait frames;
2. resolve and place the exact canonical asset or first-party pointer in each frame;
3. validate the composite against its asset-map sidecar;
4. retain editable source and export a flattened derivative where needed;
5. publish only after the validator passes.

## Activated San Telmo / RICPE / Sun Park composite

The source-stamped composite is controlled as:

- **Asset ID:** `composite.san-telmo-ricpe-sun-park-stamp-v1`
- **Storage mode:** native HTML/CSS/JavaScript
- **Component path:** `assets/san-telmo-source-stamp-20260819.js`
- **Slot order:** Eduardo Sánchez → Sun Park / MYND Yaiza → Borja / Administrador Concursal
- **Source timestamp:** statement begins at **08:08** and completes at **08:12**; context **07:57–08:27**; transcript pages **29–30 of 85**.

The native website composite may be reused across website pages only without altering the portrait-slot mapping, source line or evidential boundary. A flattened export for an email or document is a derivative and must preserve the same slot map and source control.

## Repository locations

- Named people and first-party pointers: `assets/actors/`
- Canonical registry: `assets/visual-asset-registry.json`
- Composite sidecars: `assets/composites/*.asset-map.json`
- Source-stamped component: `assets/san-telmo-source-stamp-20260819.js`
- Rejected-output log: `archive/knowledge-project/VISUAL_ASSET_REJECTED_OUTPUTS_LOG.md`
- Automated validator: `scripts/validate_visual_asset_registry.py`
- CI gate: `.github/workflows/validate-visual-asset-registry.yml`

## File naming

Person assets use the canonical lowercase ASCII slug:

`assets/actors/<canonical-person-slug>.<ext>`

A first-party external source may use a byte-locked `.url` pointer under the same canonical slug. Variants must not overwrite the primary asset.

Examples:

- `francisco-de-borja-rodriguez-batllori.jpg`
- `eduardo-sanchez-san-telmo.url`
- `francisco-de-borja-rodriguez-batllori--square-profile--20260819.webp`

Each variant needs its own asset ID and registry entry.

## Replacement and correction

Never silently replace a portrait or pointer under an existing path.

A replacement requires:

1. a new file or pointer and variant ID;
2. provenance and identity basis;
3. old and new Git blob SHA values;
4. explicit `supersedes` / `superseded_by` fields;
5. reason for replacement;
6. update of every affected slot map;
7. equivalent-prominence correction if an incorrect image was publicly displayed.

## Website markup rule

Where a named-person image is rendered in HTML, use the canonical asset ID with the resolved local path or registered first-party URL:

```html
<img
  src="../../assets/actors/francisco-de-borja-rodriguez-batllori.jpg"
  data-visual-asset-id="person.francisco-de-borja-rodriguez-batllori.primary"
  alt="Francisco de Borja Rodríguez-Batllori Laffitte, Administrador Concursal en el Concurso 36/2012">
```

Dynamic components must resolve the same asset ID and must not hard-code an unrelated attachment or generated image.

## Documents and emails

For email, PDF, Word and presentation exports:

- use the canonical asset or registered first-party source, not a chat-thumbnail guess;
- retain the asset ID in the source document's alt text, notes or metadata;
- preserve the source path/pointer and registry version in the working file;
- use the slot-map sidecar when more than one named person appears;
- never treat a generated flattened image as the primary identity source.

## Evidential and privacy boundary

The registry establishes which image the project has approved for a named subject. It does not establish any allegation, liability or fact beyond identity/provenance of the asset. Public use must still follow the project's evidence-status, right-of-reply, privacy and proportionality rules.

## Mandatory failure mode

When identity is not locked, the system must say:

> **Portrait unavailable pending canonical asset verification.**

It must not guess.
