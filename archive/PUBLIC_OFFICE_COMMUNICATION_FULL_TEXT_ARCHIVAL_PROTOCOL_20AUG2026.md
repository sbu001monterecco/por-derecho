# Public-office communication full-text archival protocol

Status: mandatory repository rule
Effective date: 20 August 2026
Scope: Project Sun Rock / Por Derecho matter

## Mandatory rule

Every communication received from a public office, public authority, court, tribunal, Fiscalía/Ministerio Fiscal office, tax authority, regulator, transparency body, inspectorate, ministry, Gobierno de Canarias department, Cabildo, Ayuntamiento, police/public-security body, public commission, public ombudsman or other public-sector body that relates materially to this matter must be preserved in the repository as a **full source record**.

A summary, chronology entry, analysis, website statement or quotation is never a substitute for the complete communication.

## What must be preserved

For every relevant communication, preserve as far as available:

1. The complete email body, including an express note when the body is empty.
2. The complete text of every substantive attached letter, resolution, decree, order, notification, certificate, report or other official document.
3. The original sender/issuing office and recipient metadata.
4. Date and time of the email or notification.
5. Subject line.
6. Official reference, expediente/proceeding number, SALIDA/ENTRADA/REGAGE number, NDE or verification code where present.
7. Original attachment filename(s).
8. Signature and registration metadata appearing in the official document.
9. The connector/source provenance used to recover it, including Gmail message ID or equivalent internal retrieval identifier where useful for reproducibility.
10. The native binary or an authenticated/custody location for it when repository tooling permits; where the repository stores only a text derivative, identify the native source and do not describe the text derivative as the native binary.

## Fidelity rule

- Preserve the complete wording of the source.
- Normalisation of line wrapping and page-break hyphenation is permitted only to make a text transcription readable; it must not change substantive wording.
- If extraction is uncertain, mark the uncertainty rather than silently correcting the source.
- Do not silently omit inconvenient, adverse, exculpatory, repetitive or apparently irrelevant passages from a document being preserved as “full text”.
- If privacy, secrecy, legal privilege or publication constraints require a redacted/public derivative, preserve the distinction between the full controlled source and the redacted/public derivative. Never silently replace the former with the latter.

## Analytical separation

Each source record must distinguish:

- **primary/source text**;
- **provenance/custody metadata**; and
- any **summary, interpretation, allegation, legal analysis or evidential inference**.

Interpretive material should normally be maintained in the relevant specialist ledger or analysis file and link back to the complete source record.

## Same-pass ingestion rule

Whenever Gmail, Drive, a portal download, uploaded file or other connected source reveals a new material communication from a public office in this matter, the handling workflow should, in the same pass where practicable:

1. read the complete communication and all substantive attachments;
2. create or update its canonical full-source repository record;
3. add the source to the relevant proceeding/institutional ledger and chronology where material;
4. propagate any material correction or new fact through the existing correction/missing-evidence/storyline architecture; and
5. only then rely on a summary or excerpt in downstream analysis or publication.

## Retroactive rule

This rule applies both prospectively and to older public-office communications encountered during future searches. If a historical official communication is already summarized in the repository but its full text is not preserved, treat that as an ingestion gap and close it when the source is next handled.

## Initial implementation — Intervención General

The first two communications brought under this rule are:

- `archive/public_office_communications/intervencion_general/2026-03-06_SALIDA_184368_2026_FULL_TEXT.md`
- `archive/public_office_communications/intervencion_general/2026-06-11_SALIDA_497011_2026_FULL_TEXT.md`

Both Gmail preservation messages have empty bodies; the substantive official communications are the attached signed/registered PDFs. The repository records therefore preserve the full official text plus Gmail/source provenance rather than mischaracterising the empty forwarding/preservation email as the communication itself.
