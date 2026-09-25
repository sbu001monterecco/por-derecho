# OpenAI model-quality report packet — named-person image fidelity

**Incident:** PD-AI-IMG-INC-20260925-01

## Product
ChatGPT image generation/editing in a conversation where exact approved real-person references were supplied.

## Expected
Preserve the exact approved real-person identities and the reviewed factual poster content, or stop if exact identity preservation cannot be guaranteed.

## Observed
One named face was recognisable, four named faces were re-synthesised as different people, and unrelated factual details were generated.

## Generation IDs
- 9cc79bab-298c-4fa8-a990-b956140f74f7
- ef310bd0-ddfe-42dc-af1b-a71a2b8bd069

## Reproduction constraint
The user explicitly instructed: use the real approved faces only; do not invent or hallucinate; report any missing source. Canonical sources were available.

## Impact
Material integrity failure for an evidential/public-interest visual. The output could misidentify real people and introduce false factual assertions.

## Mitigation applied by project
Named-person evidence visuals are now deterministic-only. Image-generation output is quarantined from identity/factual source use.

## Requested review
Investigate why referenced real-person identity constraints and factual preservation constraints were not honoured. This packet deliberately does not include private email/bank material.
