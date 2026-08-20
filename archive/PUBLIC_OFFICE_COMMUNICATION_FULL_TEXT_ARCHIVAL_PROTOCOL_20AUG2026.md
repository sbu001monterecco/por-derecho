# Public-office communication custody and redacted-publication protocol

Status: mandatory repository rule  
Effective date: 20 August 2026  
Scope: Project Sun Rock / Por Derecho matter

## Two-layer rule

Every material public-office communication must be handled through two conceptually separate layers:

1. **Primary evidence custody:** complete source, native binary where available, full metadata and unredacted text in a private access-controlled evidence store.
2. **Public publication derivative:** source-led, institutionally complete and appropriately redacted for the public repository and website.

A summary, chronology entry, analysis, website statement or quotation is never a substitute for the complete primary source. Equally, public GitHub publication is not a justification for exposing unnecessary personal or authentication data.

## Primary evidence custody requirements

Preserve, as far as available:

1. complete email body, including a note where empty;
2. complete substantive attachments;
3. sender/issuing-office and recipient metadata;
4. date/time and subject;
5. official reference, expediente, SALIDA/ENTRADA/REGAGE number and verification code;
6. original filenames;
7. signature/registration metadata;
8. retrieval provenance, including message or portal identifiers;
9. native binary, official verification result and cryptographic hash;
10. custody location, access controls and any privilege/secrecy restriction.

## Public derivative requirements

A public derivative should retain the institutional and evidential substance needed for accountability while redacting unnecessary:

- private email and street addresses;
- telephone numbers;
- signatures and signature images;
- verification codes or credentials capable of retrieving a personal document;
- unrelated personal identifiers;
- protected, privileged or legally restricted material.

It must state whether it is a transcription, translation, digest, redacted copy or native binary. It must not describe a derivative as the native signed document.

## Fidelity and analytical separation

- Do not silently omit adverse or exculpatory substantive passages from a document represented as complete.
- Where the public layer is a digest rather than full redacted text, label it clearly and point to the private/native custody requirement.
- Keep primary/source text, provenance/custody metadata and analysis/inference distinct.
- Mark extraction or translation uncertainty rather than silently correcting it.

## Same-pass ingestion

When a new material communication is located:

1. read the complete communication and substantive attachments;
2. secure the native source and hash in the private custody layer where possible;
3. create or update the public redacted source record;
4. update the institutional/proceeding chronology;
5. propagate material corrections through correction, missing-evidence and storyline controls;
6. audit the public output for personal data before publication.

## Retroactive correction

- If a historical source is summarized but not preserved, treat that as a primary-source gap.
- If unredacted personal or verification data appear in public Git history, replace the current public version immediately with a redacted derivative.
- Because ordinary Git commits do not erase prior history, assess separately whether a repository-history rewrite, secret rotation or document-verification mitigation is necessary.

## Intervención General implementation

- `2026-03-06_SALIDA_184368_2026_FULL_TEXT.md`: native PDF was recovered in the prior ingestion pass; its public form should be reviewed against this redaction rule.
- `2026-06-11_SALIDA_497011_2026_FULL_TEXT.md`: native PDF was recovered in the prior ingestion pass; its public form should be reviewed against this redaction rule.
- `2026-08-19_SALIDA_699645_2026_ES_EN.md`: current public redacted derivative; native signed PDF still requires recovery, verification and hashing in private custody.
