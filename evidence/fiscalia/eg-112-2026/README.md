# Fiscalía Superior de Canarias - EG 112/2026 clarification decree

**Control date:** 25 August 2026

**Public status:** official three-page clarification decree digitised; complete substantive text retained; direct contact and electronic-signature/certificate data removed

**Procedural status:** EG 112/2026 closure maintained by clarification decree dated 23 August 2026 and notified on 25 August 2026

## Controlling formulation

The decree records that Fiscalía Superior de Canarias opened Government File
112/2026 after the communication of 2 August 2026, analysed the initial request
and accompanying documents, and archived the governmental file because it did
not identify criminal indicia or action for that superior office.

The clarification:

1. acknowledges that an earlier criminal investigation, DIP 2/2026, concerned
   an alleged prevaricación offence by the Magistrate and was provisionally
   archived for want of rational criminal indicia;
2. states that the 2 and 20 August communications did not allege a new or
   similar criminal irregularity by the Magistrate and therefore did not engage
   Fiscalía Superior's objective competence through an aforado person;
3. declines to open new criminal-investigation proceedings or reopen DIP
   2/2026 on that material;
4. states that the newer civil/mercantile matters would concern the territorial
   competence of Fiscalía Provincial de Las Palmas de Gran Canaria; and
5. maintains the 20 August decision and says no appeal lies against the
   clarification decree.

This is the issuing authority's official procedural position. It is not a
judicial finding that the underlying allegations are true or false, does not
determine the route or disposition of the separate complaint presented at the
Decanato on 18 June 2026, and does not establish what other competent office
has received or examined each evidentiary module.

## Evidence inventory

| Evidence ID | Native source | Public derivative | Pages | Classification |
|---|---|---|---:|---|
| `EVID-2026-FISCALIA-EG112-ACLARACION-003` | Native electronically signed decree dated 23 August 2026 | `public-pdfs/decreto-aclaracion-eg-112-2026-23ago2026-public-redacted.pdf` | 3 | official Fiscalía decision; public-safe derivative |

The accessible page-accounted transcription is:

- `full-text/decreto-aclaracion-eg-112-2026-23ago2026-public-transcription.md`

The Spanish official text controls. The English public page is an analytical
translation and does not purport to be a certified legal translation.

## Hashes and source custody

The native signed source remains outside public Git history.

| Source or derivative | SHA-256 |
|---|---|
| Native signed decree | `3dc2ce45dc02c30edf5b10d017d0d97b9c36351ee84b195d03e7033c3a16aa57` |
| Public redacted PDF | `fe9111aca4aa4cc82627af6c97a8408e3ed5e3db9e0382a6e302783f281b6783` |
| Public transcription | `edcbeb9ca68ff33b0dbd8cb4bc9442c30f63d0db1ad570c0c7d72c0222bb919a` |

## Redactions and validation

The public derivative removes only:

- the office email address, telephone number and postal address repeated in the
  footer; and
- the visible and embedded electronic-signature/certificate payload, including
  personal identifier and certificate contact data.

The issuing office, file number, decision date, party name, reasoning,
operative result and the visible attribution `Fdo. El Fiscal Superior` remain.
The public copy contains no AcroForm dictionary or signature widget. The native
source is retained separately as the signed record.

## Reproduction

Run:

```bash
python3 scripts/build_eg112_clarification_public_evidence.py --source /path/to/native-signed-decree.pdf
```

The builder pins the native SHA-256 and page count, applies fixed public
redactions, removes form/signature objects and metadata, emits the PDF and
page-accounted transcription, and fails if controlled private literals or
widgets remain.
