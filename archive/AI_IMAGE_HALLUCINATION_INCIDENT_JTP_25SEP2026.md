# AI image hallucination incident — JTP actor composite — 25 September 2026

**Incident ID:** PD-AI-IMG-INC-20260925-01  
**Severity:** MATERIAL — identity and factual-content integrity  
**Disposition:** generated outputs rejected; do not publish.

## Summary

Two image-model renders intended to preserve a reviewed JTP poster layout did not preserve the canonical actor images or factual content.

Generation IDs:
- `9cc79bab-298c-4fa8-a990-b956140f74f7`
- `ef310bd0-ddfe-42dc-af1b-a71a2b8bd069`

The second render correctly reflected the supplied JTP image closely enough for the user to recognise it, but the other four named faces did not correspond to the canonical approved portraits. This violates the visual-asset identity rule.

## Confirmed canonical source assets

- JTP: `Juan_Tomas_Parrilla_canonical_20260923.jpg`, Google Drive ID `1BCJJ-dYoREQsEcDfyIhqHZzijKwoGs9l`.
- AC: `assets/actors/francisco-de-borja-rodriguez-batllori.jpg`, blob `f2c3bfd6628e043940f58b4f4c76ffdba735bb57`.
- JDAM: `assets/actors/jose-daniel-acosta-matos-user-supplied-07sep2026.jpg`, blob `8cb92bebcdfc67c7b7f3dd585f01482374be5fa9`.
- LPAM: `assets/actors/laura-patricia-acosta-matos-user-supplied-07sep2026.jpg`, blob `b05f094b6dd392664b7d2c94b6f079207eee4106`.
- Alberto López Villarrubia: `assets/actors/alberto-lopez-villarrubia.jpg`, blob `52487a2fb01b2df6b231938668c9f858544fecc5`.

## Identity failures

The generated output re-synthesised the AC, JDAM, LPAM and judge portraits instead of inserting the approved canonical portrait pixels. They are therefore invalid named-person representations for this evidence workspace.

## Semantic hallucinations observed

The output also introduced unsupported or wrong substantive content, including:

- JTP labelled as “Bankruptcy administrator / Administrador concursal” rather than former LPB insolvency counsel;
- the AC described as “Lawyer – Rodríguez-Batllori Abogados” with a made-up law-firm/invoice lane;
- JDAM assigned an unsupported generic “Intermediary” role and invented “introductions, coordination and benefits” language;
- LPAM described as “Owner – Hotel Calvià Palace”;
- an invented “Hotel Calvià Palace” transaction/benefits node;
- a Palma de Mallorca location/background unrelated to the canonical Sun Park / Concurso 36/2012 JTP workstream;
- “hotel stays” and associated benefit language not sourced to the approved JTP visual manifest;
- an unsourced result label “No effective investigation” presented as part of the graphic;
- generic date/record labels that were not taken from the reviewed JTP data controls.

These additions were model-generated visual content, not repository evidence.

## Root-cause classification

The failure occurred because a generative image model was used for a task requiring exact identity preservation and exact factual typography. Passing source images and verbal instructions did not guarantee pixel-level identity preservation or factual-content fidelity.

## Permanent mitigation

Effective immediately, named-person investigative visuals use `DETERMINISTIC_COMPOSITING_ONLY` under `governance/FACE_IDENTITY_CONTROL_RULE.md`.

Image generation may be used for non-evidential background illustration only when it cannot alter named-person likenesses or substantive factual labels.

## OpenAI product-quality report packet

For product feedback, attach this incident record, the two generation IDs above, the invalid generated outputs, and the five canonical source portraits. The core reproduction is: “asked to preserve exact approved real faces and existing factual layout; model preserved one face but synthesised four wrong faces and invented multiple factual details despite explicit no-hallucination instructions.”
