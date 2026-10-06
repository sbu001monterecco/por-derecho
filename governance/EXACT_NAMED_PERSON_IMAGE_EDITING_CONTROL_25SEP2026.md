# Exact named-person image editing control — 25 September 2026

Control ID: **PD-EXACT-NAMED-PERSON-IMAGE-20260925-01**

## Purpose
Prevent a repeat of the JTP actor-composite reliability incident in which an identity-preserving edit was sent through a generative redraw path and substitute likenesses / unrelated content were produced.

## Mandatory preflight
Before any Por Derecho composite containing named people is rendered:
1. Resolve each named subject to an already-approved source asset.
2. Record provider, repository/Drive path, Git blob SHA when applicable, and SHA-256.
3. Check GitHub, GitLab and the connected Drive before stating that an approved source is missing.
4. Distinguish **source exists** from **source bytes are materialized in the current editing runtime**.
5. If exact repository bytes are not locally available, export/materialize them through a controlled artifact path before editing. Do not substitute a generated likeness.

## Editing rule
For an approved composition where only portraits need correction:
- use deterministic pixel compositing;
- change only expressly authorised rectangles/masks;
- do not regenerate the page;
- do not synthesize, beautify or infer a named person's face;
- do not alter text, arrows, amounts, dates, logos, evidential labels or background unless separately authorised;
- preserve already-approved portraits that are not in the authorised edit mask.

Generative image output is **not** an acceptable substitute for exact named-person source compositing.

## Verification
A candidate is publication-ineligible unless:
- every input source hash matches its approved control;
- outside-mask changed pixels = 0;
- protected regions (including any already-approved JTP portrait) are pixel-identical;
- the output has a provenance sidecar;
- no rejected candidate is reused as a source;
- repository/publication controls pass normally.

## Publication
A visual is not LIVE because it rendered successfully. Publication requires normal protected merge/deploy and anonymous readback of the actual image/page on each intended host.

## Evidence boundary
Portrait inclusion identifies the project-attributed person and role only. It does not establish knowledge, intent, participation, coordination, liability or criminality. Identity attribution must come from the controlled source record / user-supplied identification, not facial-recognition inference.
