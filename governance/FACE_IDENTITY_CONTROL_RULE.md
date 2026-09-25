# Named-person visual identity control — hard rule

**Control ID:** PD-VISUAL-FACE-NOGEN-20260925-01  
**Status:** ACTIVE / FAIL-CLOSED  
**Applies to:** every Por Derecho visual, poster, composite, social image, page hero or diagram depicting a named real person.

## Core rule

A named person's face **must never be created, reconstructed, approximated, beautified, age-shifted, blended or substituted by a generative image model**.

Named-person visuals must use deterministic compositing from an approved canonical source image. If an approved source is missing, unreadable, not byte-locked, or the actor-to-slot mapping is ambiguous, generation must stop.

## Mandatory preflight

Before rendering a named-person composite:

1. resolve every named person to a canonical asset ID;
2. resolve that asset to an exact repository path or approved Drive source;
3. verify provenance and identity basis;
4. verify Git blob SHA and/or SHA-256 where available;
5. create an explicit slot map: one actor → one portrait slot → one exact source;
6. verify all factual labels from a separate text manifest;
7. reject any unapproved logo, organisation, hotel, place, role, relationship, payment arrow or outcome label.

No visual may infer identity from appearance. User-supplied identity mappings remain user-supplied mappings; they are not facial-recognition results.

## Rendering mode

For named-person composites the permitted mode is:

**DETERMINISTIC_COMPOSITING_ONLY**

Permitted operations on approved portraits:
- crop;
- scale;
- mask;
- background removal;
- rotation;
- exposure/contrast correction;
- colour harmonisation that does not redraw facial structure.

Not permitted:
- text-to-image replacement of a named person;
- face generation;
- face swap;
- generative inpainting across the face;
- synthetic “lookalike” substitution;
- blending two source faces;
- generative reconstruction of missing face pixels;
- generative alteration of age, expression, hair, facial geometry or attire presented as documentary likeness.

## Text and factual-content rule

Investigative/factual posters must not ask an image model to invent or typeset substantive factual content.

All names, roles, dates, amounts, organisations, locations, arrows, relationship labels, status labels and disclaimers must be supplied from a reviewed text/data manifest. Unsupported facts must not be added for visual completeness.

## Publication gate

A named-person composite is not publication-ready unless:

- every portrait source is approved and provenance-controlled;
- the slot map is complete;
- no generative face synthesis was used;
- the factual text manifest has been reviewed;
- the output has been visually compared with each source portrait;
- the output has a provenance sidecar recording input assets and render method;
- any mismatch means **REJECT / DO NOT PUBLISH**.

## Current JTP workstream

The 25-Sep-2026 generated posters with image-generation IDs:
- `9cc79bab-298c-4fa8-a990-b956140f74f7`
- `ef310bd0-ddfe-42dc-af1b-a71a2b8bd069`

are **REJECTED / DO NOT PUBLISH**. JTP's likeness was derived acceptably from the approved JTP source, but other named actors were re-synthesised rather than preserved and substantive labels were hallucinated. These outputs are failure examples, not approved assets.

## Non-transfer rule

Juxtaposition of real portraits is an editorial/evidential navigation device. It does not prove coordination, shared knowledge, common purpose, agency, criminality or liability.
