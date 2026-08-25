# DIP 2/2026 official-record publication control

**Date:** 25 August 2026

**Status:** primary-source gap closure, public-safe digitisation and publication control
**Scope:** Fiscalía de la Comunidad Autónoma de Canarias, DIP 2/2026, Concurso Ordinario 36/2012 judicial-conduct complaint track.

## New primary-source findings

Two signed official PDFs are now source-controlled and fully read:

1. **Decreto de resolución y archivo, 6 March 2026, 10 pages** - signed
   electronically by **Juan Manuel González-Casanova Ruiz, Fiscal**. It records
   receipt on 20 January 2026; states that the investigation proceedings were
   opened by decree on 11 February 2026; describes the object examined; orders
   closure; and states that the decree does not produce res judicata effect and
   does not prevent reiteration before the competent court.
2. **Oficio de notificación al denunciante, 9 March 2026, 1 page** - signed
   electronically by **Ernesto Vieira Morante, Fiscal**. It communicates the
   closure, encloses the resolution and repeats the Article 773 LECrim route to
   the competent court.

Controlled evidence IDs, native hashes, public-derivative hashes, full text and
redaction scope are recorded in
`evidence/fiscalia/dip-2-2026/README.md`.

## Gap correction

The older generic gap **"DIP 2/2026 exact signatory"** is superseded. The two
public acts now have separate identified signatories and must not be conflated:

- substantive closure decree: Juan Manuel González-Casanova Ruiz;
- notification oficio: Ernesto Vieira Morante.

The still-open DIP 2/2026 source-completion targets are:

- the complete certified file;
- the separate 11 February opening decree;
- the incorporation and treatment of REGAGE26e00026303869 after 11 March;
- any correction, reconsideration, hierarchical review or substantive response;
- a complete transmission bridge into later judicial proceedings where relied
  upon.

## Evidential classification

- Receipt, opening, closure and notification are `P1 PRIMARY AUTHENTIC` official
  acts.
- The decree's description of Gil Marer's allegations is not proof of those
  allegations.
- The closure is an official outcome within the object and reasoning stated in
  the decree. It is not res judicata and does not establish that the full
  historical or later extraconcursal case was examined.
- The appeal-status premise is objectively contradicted by the separately
  controlled 28 January and 18 February court acts. That contradiction does not
  prove deliberate falsehood, prosecutorial misconduct, collusion or external
  influence.

## Public implementation

The existing stable ES/EN route pair is extended rather than duplicated:

- `es/fiscalia-dip-2-2026/index.html`
- `en/fiscalia-dip-2-2026/index.html`

Each page now leads with the official opening/closure/notice sequence, identifies
the two signatories by their documented acts, links both public-safe PDFs and
their full transcriptions, retains the existing appeal-status comparison, retains
the 11 March registered correction and preserves the evidential limitations and
right-of-reply architecture.

The public PDF derivatives redact direct contact details and electronic-
verification locators/codes only. Unredacted native files and private locators
remain outside public Git history.

## Communications boundary and continuation

The next authorised work may prepare emails and a LinkedIn post centred on the
live route after deployment verification. This publication instruction does not
authorise any email send. Exact recipients, subject, body, links and attachments
remain subject to the repository email-send gate.

## Continuity state

**DELETION-SAFE WITH OPEN EVIDENCE.** PR #959 was squash-merged as
`7a4951d7d20ba35ee59109199fa36929077e67f6` (tree
`8ca9d09a55e4c7965708510cebd4abd674a443fb`). The exact merge SHA was deployed
successfully by Pages run `32821005124`, completed at
`2026-08-25T07:19:43Z`.

Cache-busted public readback passed six of six controlled surfaces with HTTP
200 and byte-for-byte SHA-256 equality: both bilingual routes, both public PDF
derivatives and both page-accounted transcriptions. Live-browser inspection
confirmed three aligned official-record cards, four working document controls,
loaded fonts and zero horizontal overflow on each language route.

The deletion-safe classification preserves the following open evidence rather
than treating absence as proof of nonexistence:

- complete certified DIP 2/2026 file;
- separate 11 February 2026 opening decree;
- post-11 March incorporation, correction, reconsideration and hierarchical
  treatment;
- any complete transmission bridge into later judicial proceedings.

No email was sent, no Gmail draft was created and no LinkedIn post was prepared
or published during this publication step.
