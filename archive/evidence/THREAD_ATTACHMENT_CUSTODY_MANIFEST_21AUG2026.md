# Thread attachment custody manifest

**Audit date:** 21 August 2026  
**Scope:** six PDFs supplied to the ChatGPT thread  
**Public-record rule:** filenames are source-supplied labels, not findings or
endorsement of allegations contained in them.

This manifest records recoverability without placing private evidence binaries,
email addresses, raw Gmail identifiers or signed download links in public
GitHub. Private source locators are preserved in the self-email closeout record.

## Custody result

| Supplied filename | Recovered item | Status | Bytes | SHA-256 of recovered item | Durable source position | Next finite step |
|---|---|---|---:|---|---|---|
| `MEETINGPOINT Club Sei Lanzarote SUN PARK en Tourinews 28OCT2020.pdf` | None located in the completed exact-filename Gmail and workspace pass | `MISSING-EXACT` | Unknown | Not computed | Supplied derivative is no longer present in scratch workspace; no exact Gmail attachment was located | Retrieve the original PDF from its creator/download source or a controlled backup, hash it and record the source date |
| `TOMA DE POSESION ILEGAL DEL HOTEL SUN PARK POR CAM - 7JUN2018.pdf` | Same-name PDF recovered from an existing private source email | `EXACT-NAME RECOVERED CANDIDATE` | 1,333,361 | `808e06cfd6b6c8e49e835a419699a38ce93bb0b17284505822f942706093640a` | Native attachment remains in the controlled Gmail source record | Recover the originally supplied bytes, if available, and compare SHA-256 before calling the files identical |
| `Gmail - Fwd_ FW_ ACTA JUNTA EXTRAORDINARIA SUN PARK.PDF` | Underlying acta source attachment: `ACTA JUN EXTRA FEB22-31032022110911.pdf` | `RELATED SOURCE`; supplied printed-email derivative remains `MISSING-EXACT` | 3,369,527 | `bcde60e1bc42bdc6448eb28f1258894746f717a44a342927269549c06ec0666e` | Native source attachment remains in the original private Gmail thread | Recreate or retrieve the exact printed-email PDF, hash it separately and retain its relationship to the source acta |
| `CAM - HNT Segregacion HOTEL SUN PARK (sucesion en bloque por sucesion universal) BORME 11NOV2022.pdf` | Same-name PDF recovered from an existing private source email | `EXACT-NAME RECOVERED CANDIDATE` | 331,404 | `6860dc260239c8c8815ab90b7108396a21b2cb2fc02000cbbf5f4836d34da8ea` | Native attachment remains in the controlled Gmail source record | Compare against the originally supplied bytes before upgrading to `BYTE-IDENTICAL COPY` |
| `ACTA Cdad Sun Park 4FEB2022.pdf` | Same-name PDF recovered from an existing private source email | `EXACT-NAME RECOVERED CANDIDATE` | 3,015,343 | `56355a84eadbbd2cc085d650c20bc56560b1006992fcf6f462ecc5d6875b39e0` | Native attachment remains in the controlled Gmail source record | Compare against the originally supplied bytes; also reconcile its relationship to the 3,369,527-byte acta source file |
| `Anexo I - Informe Detallado del Estado del Hotel Sun Park 2008-2022 (Acoso Inmobiliario-Estafa Inversores y Fiscal) 9ENE_2023.pdf` | Compressed private variant: `Anexo I - Informe Detallado del Estado del Hotel Sun Park 2008-2022 _comp.pdf` | `VARIANT`; supplied exact file remains `MISSING-EXACT` | 9,462,834 | `bd4ace620d9b1d46aef64b75279fe16ed7df5ce9329c0dcc354a1a53ce8b9ea4` | Variant remains in a controlled Gmail source record and is marked private/confidential | Retrieve the exact dated original; compare pagination, content and SHA-256; do not publish the variant without authority and redaction review |

## What the hashes prove

The hashes fingerprint only the five recovered source-system files listed here.
They do not prove that a recovered candidate is byte-identical to the vanished
thread upload. That requires both byte sets or a pre-existing hash of the upload.

## Repository storage decision

The repository stores this manifest, the governing prompt and the deletion
audit. It deliberately does not store the five recovered private PDF binaries.
The repository is public-facing; moving private or confidential evidence into it
would weaken custody, confidentiality and publication control. The source PDFs
remain digitally stored in their Gmail source records. Temporary scratch copies
used to compute hashes are not represented as durable custody.

## Open custody count

- Three exact-name recovered candidates, pending byte comparison.
- Two supplied derivatives/originals missing, with a related source or variant
  recovered.
- One supplied PDF with no exact or related attachment recovered in this pass.

The correct closeout status is therefore `DELETION-SAFE WITH OPEN CUSTODY`, not
full evidence-custody completion.
