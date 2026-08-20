# Public-office communication full-text archival protocol

Status: mandatory repository rule  
Effective date: 20 August 2026  
Scope: Project Sun Rock / Por Derecho matter

## Mandatory rule

Every material communication received from a public office, public authority, court, tribunal, Fiscalía/Ministerio Fiscal office, tax authority, regulator, transparency body, inspectorate, ministry, Gobierno de Canarias department, Cabildo, Ayuntamiento, police/public-security body, public commission, public ombudsman or other public-sector body relating to this matter must be preserved in the repository as a **full source record**.

A summary, chronology entry, analysis, website statement or quotation is never a substitute for the complete communication.

## What must be preserved

For every relevant communication, preserve as far as available:

1. The complete email body, including an express note when the body is empty.
2. The complete text of every substantive attached letter, resolution, decree, order, notification, certificate, report or other official document.
3. Sender/issuing-office and recipient metadata.
4. Date and time of the email or notification.
5. Subject line.
6. Official reference, expediente/proceeding number, SALIDA/ENTRADA/REGAGE number, NDE or verification code where present.
7. Original attachment filename(s).
8. Signature and registration metadata appearing in the official document.
9. Retrieval provenance, including Gmail message ID or equivalent internal retrieval identifier where useful for reproducibility.
10. The native binary or authenticated/custody location when tooling permits. Where only a text derivative is stored, identify the native source and never describe the text derivative as the native binary.

## Fidelity and source-status rule

- Preserve complete wording where a complete source is available.
- Normalisation of line wrapping and page-break hyphenation is permitted for readability only; it must not change substance.
- If extraction is uncertain, mark the uncertainty rather than silently correcting it.
- Do not silently omit adverse, exculpatory, repetitive or apparently inconvenient passages from a document represented as “full text”.
- If privacy, secrecy, privilege or publication constraints require a redacted/public derivative, keep the full controlled source and public derivative conceptually separate.
- A user-supplied pasted transcription is not the native signed binary. It may be used immediately as a controlled derivative, but native-source recovery remains a custody task.

## Analytical separation

Each record should distinguish:

- **primary/source text**;
- **provenance/custody metadata**; and
- **summary, interpretation, allegation, legal analysis or evidential inference**.

Interpretive material should link back to the complete source record.

## Same-pass ingestion rule

Whenever Gmail, Drive, a portal download, uploaded file or other connected source reveals a new material public-office communication, the workflow should, in the same pass where practicable:

1. read the complete communication and substantive attachments;
2. create/update its canonical source record;
3. update the relevant institutional/proceeding chronology;
4. propagate any material correction through the correction/missing-evidence/storyline architecture; and
5. only then rely on summaries or excerpts downstream.

## Retroactive rule

The rule is prospective and retroactive. If a historical official communication is already summarized but its full text is not preserved, treat that as an ingestion gap and close it when next handled.

## Intervención General implementation

Current canonical controlled records include:

- `archive/public_office_communications/intervencion_general/2026-03-06_SALIDA_184368_2026_FULL_TEXT.md` — native PDF recovered from Gmail in the prior ingestion pass.
- `archive/public_office_communications/intervencion_general/2026-06-11_SALIDA_497011_2026_FULL_TEXT.md` — native PDF recovered from Gmail in the prior ingestion pass.
- `archive/public_office_communications/intervencion_general/2026-08-19_SALIDA_699645_2026_ES_EN.md` — user-supplied transcription and English translation; native signed PDF still to be recovered/hashed.
