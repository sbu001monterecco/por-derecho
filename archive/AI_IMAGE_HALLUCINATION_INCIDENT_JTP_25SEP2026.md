# AI image-generation reliability incident — JTP actor visual — 25 September 2026

**Incident:** PD-AI-IMG-INC-20260925-01  
**Disposition:** REJECTED / DO NOT PUBLISH

Two conversational image-model renders were produced after the user required exact approved real portraits. The output preserved JTP acceptably in one render but re-synthesised the other named people and invented substantive poster details.

Rejected generation IDs:
- `9cc79bab-298c-4fa8-a990-b956140f74f7`
- `ef310bd0-ddfe-42dc-af1b-a71a2b8bd069`

Confirmed failures included wrong/non-canonical faces for the AC, JDAM, LPAM and Alberto López Villarrubia; an incorrect JTP role; invented Hotel Calvià Palace / Palma de Mallorca material; invented hotel-stay/benefit language; and relationship/outcome labels not taken from the controlled JTP record.

The repository source assets were not missing. The failure mode was the use of a generative image model for an exact-identity and exact-factual-typography task.

Permanent mitigation: `governance/FACE_IDENTITY_CONTROL_RULE.md`. Named-person evidence visuals use deterministic exact-source composition only.

This incident record is a product-quality/reproducibility record. It is not evidence about any depicted person.
