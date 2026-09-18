# Fiscalía de Canarias - DIP 2/2026 official-record control

This directory preserves the public-safe official-record layer for the opening,
closure and notification of **Diligencias de investigación preprocesal n.º
2/2026**, NIG `3501670220260000245`.

The native official PDFs remain the source of truth for signatures, layout and
verification. The public repository contains reproducible redacted derivatives
and page-accounted text transcriptions. No substantive or procedural text has
been removed. The public derivatives omit only direct postal/email contact data
and electronic-verification locators/codes that are unnecessary to understand or
audit the decisions.

## Evidence inventory

| Evidence ID | Source | Source status | Native SHA-256 | Public state |
|---|---|---|---|---|
| `EVID-2026-FISCALIA-DIP2-DENUNCIA-013JAN-001` | Denuncia inicial, 13 Jan 2026, 5 pages | party filing source located and fully transcribed | `d42051eea0ff28bc230ef58315333729a84454b8376b23ad7bbc5db35e3a77a4` | public-safe full text |
| `EVID-2026-FISCALIA-DIP2-AMPLIACION-08FEB-002` | Ampliación, 8 Feb 2026, 5 pages | party filing source located and fully transcribed | `07dc79179397f680f0201075618d6782af31a6432c823a1addf341a0f75bf1be` | public-safe full text |
| `EVID-2026-FISCALIA-DIP2-DECRETO-002` | Decreto de resolución y archivo, 6 Mar 2026, 10 pages, Juan Manuel González-Casanova Ruiz, Fiscal | signed official PDF located and read | `7d7be3516fd691de5da0d05081e5d4916b6e3141804891abf5742df82007a452` | public redacted PDF + full text |
| `EVID-2026-FISCALIA-DIP2-OFICIO-001` | Oficio de notificación, 9 Mar 2026, 1 page, Ernesto Vieira Morante, Fiscal | signed official PDF located and read | `dc4d6d8b5843e0f052cbfd8025466bb1a25ae2d0634c31d6186383263168f261` | public redacted PDF + full text |
| `EVID-2026-FISCALIA-DIP2-ACTUALIZACION-11MAR-005` | Comunicación de actualización/corrección, 11 Mar 2026, 4 pages | signed party source located and fully transcribed | `0c3116c35b7dea1976dd39ee043898d0aa6b5b1164c36c9b014b4c3ca70d85b9` | public-safe full text |
| `EVID-2026-FISCALIA-DIP2-REGAGE-11MAR-006` | REGAGE26e00026303869, 11 Mar 2026, 2 pages | official presentation receipt located and fully transcribed | `102d2f407cc33f0398d45239d94fe56a80246e645191e5e987e430b5c533b289` | public-safe full text |\n| `EVID-2026-FISCALIA-DIP2-REGAGE-TRAMITACION-007` | automated registry-routing notice; event 12 Mar, email 14 Mar | reports passage to Registro General Fiscalía de la Comunidad Autónoma de Canarias; email expressly says informational/no legal value | n/a | public-safe text trace |

## Public derivatives and full text

- [13 Jan initiating complaint - page-accounted public text](full-text/denuncia-inicial-13ene2026-public-transcription.md)
- [8 Feb amplification - page-accounted public text](full-text/ampliacion-08feb2026-public-transcription.md)
- [Decreto de archivo - public redacted PDF](public-pdfs/decreto-archivo-dip-2-2026-06mar2026-public-redacted.pdf)
- [Decreto de archivo - page-accounted full text](full-text/decreto-archivo-dip-2-2026-06mar2026-public-transcription.md)
- [Oficio de notificación - public redacted PDF](public-pdfs/oficio-notificacion-dip-2-2026-09mar2026-public-redacted.pdf)
- [Oficio de notificación - page-accounted full text](full-text/oficio-notificacion-dip-2-2026-09mar2026-public-transcription.md)
- [11 Mar update/correction - page-accounted public text](full-text/actualizacion-11mar2026-public-transcription.md)
- [11 Mar REGAGE receipt - page-accounted public text](full-text/registro-11mar2026-public-transcription.md)\n- [12 Mar registry-processing trace - public-safe email transcription](full-text/registro-tramitacion-12mar2026-email-public-transcription.md)

The public PDFs retain searchable text. The transcription files preserve source
line breaks and page boundaries to support repository search and accessibility.

## What the official record establishes

1. The Fiscalía de la Comunidad Autónoma de Canarias received the complaint and
   documentation on 20 January 2026.
2. The 6 March Decree records that DIP 2/2026 was opened by decree on 11 February
   2026.
3. The 6 March Decree ordered closure and stated that the decision did not have
   res judicata effect, leaving the complainant able to reiterate the complaint
   before the competent court.
4. The 9 March notice communicated the closure, enclosed the resolution and
   repeated the Article 773 LECrim judicial-route notice.
5. The 11 March communication expressly notified Fiscalía that the relevant
   separation decisions had been appealed before the Audiencia Provincial.
6. REGAGE26e00026303869 proves formal registration of that 11 March update with
   Fiscalía de la Comunidad Autónoma de Canarias.

## Limits and open evidence

- The opening is directly recorded in the 6 March Decree. The separate 11
  February opening decree is not included in this directory and remains a
  source-completion target within the complete DIP 2/2026 file.
- Opening did not validate the complaint. Closure records Fiscalía's conclusion
  within the scope and reasoning of this decree; it does not establish that every
  historical event or later/extraconcursal allegation concerning Concurso
  36/2012 was examined.
- The appeal-status contradiction and the 11 March registered correction remain
  separately documented. The contradiction does not by itself prove intent,
  partiality, collusion or external influence.
- Post-11 March incorporation, correction, reconsideration and hierarchical
  treatment remain open evidence questions.
- The 14 September 2026 DP 1901/2026 order is now fully transcribed from three
  source photographs in `evidence/judicial/dp-1901-2026/full-text/`. It records
  a Ministerio Fiscal report dated 29 July 2026 seeking archive, but the signed
  report itself remains missing.
- The separate 11 February opening decree remains missing; therefore this
  directory is a full digitisation of the **available located corpus**, not a
  claim that the entire certified DIP 2 file has been recovered.

## Reproduction

`scripts/build_dip2_public_evidence.py` verifies both native hashes, applies the
fixed public redactions, strips metadata, validates that excluded strings are not
extractable, preserves the page count and writes the two PDF derivatives and two
transcriptions. Native source paths are supplied at runtime and are never
committed.

Canonical public routes:

- Spanish: `/es/fiscalia-dip-2-2026/`
- English: `/en/fiscalia-dip-2-2026/`
