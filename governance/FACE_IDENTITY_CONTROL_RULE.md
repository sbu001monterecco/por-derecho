# Named-person visual identity control — fail closed

**Control:** PD-VISUAL-FACE-NOGEN-20260925-01  
**Status:** ACTIVE  
**Scope:** every Por Derecho visual that depicts or names a real person.

## Non-delegable identity rule

A named person's likeness must come from an approved canonical source asset. A generative image model must not create, reconstruct, approximate, beautify, age-shift, blend, face-swap or substitute that person's face.

If the approved source is missing, unreadable, unregistered, hash-mismatched or ambiguously mapped, the operation stops and reports the missing asset.

## Deterministic rendering rule

Named-person evidence graphics use **DETERMINISTIC_COMPOSITING_ONLY**:
- exact source pixels inserted through crop/scale/mask/background removal;
- non-structural exposure/contrast/colour correction permitted;
- no generative face inpainting or reconstruction;
- no generative alteration of facial geometry, age, expression or identity.

An HTML/CSS layout using exact repository `<img>` assets also qualifies as deterministic composition.

## Factual-text rule

Image generation has no authority to invent or typeset substantive facts. Names, roles, dates, amounts, organisations, places, relationship labels, arrows, outcomes and disclaimers must come from a reviewed text/data manifest or existing controlled page text.

Missing fact = omit or flag open. Never fill a visual gap with a plausible-looking fact.

## Publication gate

A named-person visual is not publication-ready unless:
1. every actor resolves to an exact canonical source;
2. byte/hash locks pass;
3. a slot map or exact-source HTML manifest exists;
4. factual labels come from reviewed source text;
5. the output has been compared against source portraits;
6. the provenance record states the rendering method;
7. any identity or factual mismatch causes REJECT / DO NOT PUBLISH.

## Rejected JTP image-model outputs

The following generations are rejected failure examples and must never be used as sources:
- `9cc79bab-298c-4fa8-a990-b956140f74f7`
- `ef310bd0-ddfe-42dc-af1b-a71a2b8bd069`

They re-synthesised named people and introduced unsupported factual content.

## Legacy stylisation rule

Existing assets whose representation mode explicitly says `EDITORIAL_STYLIZATION_NOT_DOCUMENTARY_PORTRAIT_EVIDENCE` may remain preserved as editorial artefacts, but must never become the identity source for a named person or be presented as documentary likeness evidence.

## Non-transfer rule

Portrait juxtaposition does not establish coordination, common purpose, knowledge, influence, liability, criminality or a money-transfer path.
