# DIP 2/2026 official-record publication control

**Original publication date:** 25 August 2026
**Controlling update:** 18 September 2026

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


## 18 September 2026 superseding source update

The connected mailbox was re-opened and the native sources were re-controlled. The existing two official Fiscalía documents remain fully digitised and their native hashes re-confirm:

- 6-Mar Decree: `7d7be3516fd691de5da0d05081e5d4916b6e3141804891abf5742df82007a452`;
- 9-Mar notice: `dc4d6d8b5843e0f052cbfd8025466bb1a25ae2d0634c31d6186383263168f261`.

The signed 11-Mar party update is now also fully digitised under `EVID-2026-FISCALIA-DIP2-ACTUALIZACION-11MAR-005`, native SHA-256 `0c3116c35b7dea1976dd39ee043898d0aa6b5b1164c36c9b014b4c3ca70d85b9`.

The prior shorthand “appeal-status premise corrected 11 March” is refined. What is source-proved is that the complainant **communicated the correction on 11 March** and requested incorporation. A substantive institutional correction/reconsideration after receipt has not yet been located.

The 18-Sep audit now classifies:
1. the appeal/finality premise as factually contradicted by the later certified appeal record;
2. the move from ATLANTE non-display to substantive non-existence/finality as an alleged analytical overreach;
3. the tension between the Decree's own summary of the complaint and its later characterisation as unsupported disagreement;
4. the distinction between allegations being present in the record and being substantively examined;
5. the absence of a complete source-to-conclusion audit;
6. post-11-Mar treatment as an open institutional gap;
7. possible propagation into DP 1901 as an open question only.

The 14-Sep DP 1901 order is separately digitised from three source photographs in:
`evidence/judicial/dp-1901-2026/full-text/auto-14sep2026-public-transcription.md` (canonical validated path; the earlier `auto-14sep2026-photo-transcription.md` path is retained as a same-source legacy transcription).

No inference of deliberate falsehood, capture, prevaricación, coordination or criminality is created by this update.

The 12-March registry-routing notification is now separately controlled as `EVID-2026-FISCALIA-DIP2-REGAGE-TRAMITACION-007`. It reports passage to the Registro General Fiscalía de la Comunidad Autónoma de Canarias for processing; the email itself says it is informational and has no legal value, so substantive file incorporation/review remains open.
