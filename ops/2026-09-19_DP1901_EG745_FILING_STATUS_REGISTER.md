# DP1901 / E.G.745 / Fiscal Superior — filing-status register

Control date: 20 September 2026  
Control timezone for receipt timestamps: Atlantic/Canary as the working programme timezone; times below are transcribed as printed.  
Repository state: public-safe receipt reconciliation. Private originals remain outside GitHub.

## Current result

**13 of 13 direct personal-action candidates are registered, represented by fourteen registration events because A02 has a principal and supplement. A06 and A13 now have receipt-controlled registrations. Their unresolved substantive/formalisation questions remain post-filing follow-ups. Do not repeat the whole filings.**

| ID | Destination / function | Registration evidence | Controlled state |
|---|---|---|---|
| A01 | Decanato / Registro y Reparto via DGRAJ | `REGAGE26e00082034813` | REGISTERED_RECEIPT_VERIFIED |
| A02 | Plaza 6 / DP 1901/2026 | `S000000000000144968` + supplement `S000000000000144972` | REGISTERED_WITH_SUPPLEMENT |
| A03 | CGPJ — Alzada 286/2026 | `REGAGE26e00082030716` | REGISTERED_RECEIPT_VERIFIED |
| A04 | Secretaría de Gobierno del TSJC | `REGAGE26e00082039117` | REGISTERED_RECEIPT_VERIFIED |
| A05 | Coordinación Provincial de LAJ | `REGAGE26e00082040006` | REGISTERED_RECEIPT_VERIFIED |
| A06 | Secretaría General para la Innovación y Calidad del Servicio Público de Justicia | `REGAGE26e00082058165` | REGISTERED_RECEIPT_HASH_VERIFIED_HANDLING_PENDING |
| A07 | Canary Justice Administration / ATLANTE | `REGAGE26e00082038176` | REGISTERED_RECEIPT_VERIFIED |
| A08 | Fiscalía Provincial de Las Palmas | `REGAGE26e00082044751` | REGISTERED_RECEIPT_HASH_VERIFIED |
| A09 | Fiscal Superior de Canarias | `REGAGE26e00082032153` | REGISTERED_RECEIPT_VERIFIED |
| A10 | FGE / Inspección Fiscal | `REGAGE26e00082033336` | REGISTERED_RECEIPT_VERIFIED |
| A11 | Sala de Gobierno via Secretaría de Gobierno del TSJC | `REGAGE26e00082052687` | REGISTERED_RECEIPT_HASH_VERIFIED |
| A12 | Defensor del Pueblo | `REGAGE26e00082055212` | REGISTERED_RECEIPT_HASH_VERIFIED_WITH_TEXT_DISCREPANCY |
| A13 | Fiscalía Anticorrupción | `REGAGE26e00082060401` | REGISTERED_RECEIPT_HASH_VERIFIED_FORMALISATION_ADMISSION_PENDING |

## Receipt-specific controls

- **A02:** the principal receipt proves a four-page filing only. It did not list the two planned annexes. A separate supplemental registration records the named eleven-page combined annex PDF, but the receipt contains no document hash; it therefore does not prove byte identity.
- **A08:** the receipt records four attachments and matching SHA-512 values. The request is a bounded custody/allocation search and does not presume Provincial authorship of the 29 July report.
- **A09:** two private copies of the same receipt were recovered. They represent one action, not two.
- **A10:** this is limited incorporation/preservation of the DP1901 fact in E.G.745. It is not the separate substantive E.G.745 response.
- **A11:** two PDFs, fifteen pages, and both SHA-512 values match the receipt. It is a Sala de Gobierno/reparto request, separate from A04 and not an appeal.
- **A12:** four PDFs, thirty-five pages, and all SHA-512 values match the receipt. The filed-text field also contains an extraneous operational tail. Its legal effect and any need for correction are not determined; no corrective filing is evidenced.

## Proof ceiling

An official registration receipt proves the recorded presentation/registration event and, where supplied, the listed document hashes. It does **not** by itself prove onward transmission, admission, incorporation, examination, agreement, response or institutional action.

Repository publication is not filing or service. The private receipt PDFs, addresses, identity numbers, signatures, private email material and native private filenames remain outside the public repository.

## Remaining programme separation

- **A06 — registered, handling pending:** `REGAGE26e00082058165`, presented 20 September 2026 at 21:19:02 and registered at 21:19:12, as printed. Four PDFs, forty-five pages, all receipt SHA-512 values matched. The earlier rejected attempt `REGAGE26e00073341477` remains disclosed. Admission, incorporation, preservation, response and any separate prior national alzada registration remain unproved.
- **A13 — registered, formalisation/admission pending:** `REGAGE26e00082060401`, presented 20 September 2026 at 22:07:33 and registered at 22:07:42, as printed. Five PDFs, fifty pages, all receipt SHA-512 values matched. The existing Exp.Gub.352/2025 signature/formalisation/admission and channel questions remain post-filing follow-ups. No admission, incorporation, preservation or substantive outcome is inferred.
- **Counsel-dependent judicial remedy:** separate; excluded from the personal-action count.
- **Substantive E.G.745 response:** separate from A10 and still pending.
- **Provincial email follow-up:** supplementary only; sending/delivery and filing are distinct states.

Machine control: `assets/data/dp1901-direct-action-state-20260920.json`.

## Reconciliation history

PR1679 and PR1680 preserved an eleven-of-thirteen public snapshot. The later A06/A13 official receipts supersede those two unfiled states while retaining their prior rejection/formality history. The thirteen-candidate registration cycle is complete; the wider historical action universe, authority responses, substantive E.G.745 response and counsel-dependent remedies are not thereby complete.
