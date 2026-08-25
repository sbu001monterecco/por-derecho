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

| Evidence ID | Official act | Source status | Native SHA-256 | Public derivative SHA-256 |
|---|---|---|---|---|
| `EVID-2026-FISCALIA-DIP2-DECRETO-002` | Decreto de resolución y archivo, 6 March 2026, 10 pages, signed by Juan Manuel González-Casanova Ruiz, Fiscal | signed official PDF located and read | `7d7be3516fd691de5da0d05081e5d4916b6e3141804891abf5742df82007a452` | `8b3c01b179e3ad88b2b9782f523cfdcd4ac3d450eda756a59c26dd90cfaf1f68` |
| `EVID-2026-FISCALIA-DIP2-OFICIO-001` | Oficio de notificación al denunciante, 9 March 2026, 1 page, signed by Ernesto Vieira Morante, Fiscal | signed official PDF located and read | `dc4d6d8b5843e0f052cbfd8025466bb1a25ae2d0634c31d6186383263168f261` | `666a778d4e3b3d1e7ded6a3682d102ec85cc230f75bbb0be3d7488397da6a451` |

## Public derivatives and full text

- [Decreto de archivo - public redacted PDF](public-pdfs/decreto-archivo-dip-2-2026-06mar2026-public-redacted.pdf)
- [Decreto de archivo - page-accounted full text](full-text/decreto-archivo-dip-2-2026-06mar2026-public-transcription.md)
- [Oficio de notificación - public redacted PDF](public-pdfs/oficio-notificacion-dip-2-2026-09mar2026-public-redacted.pdf)
- [Oficio de notificación - page-accounted full text](full-text/oficio-notificacion-dip-2-2026-09mar2026-public-transcription.md)

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

## Reproduction

`scripts/build_dip2_public_evidence.py` verifies both native hashes, applies the
fixed public redactions, strips metadata, validates that excluded strings are not
extractable, preserves the page count and writes the two PDF derivatives and two
transcriptions. Native source paths are supplied at runtime and are never
committed.

Canonical public routes:

- Spanish: `/es/fiscalia-dip-2-2026/`
- English: `/en/fiscalia-dip-2-2026/`
