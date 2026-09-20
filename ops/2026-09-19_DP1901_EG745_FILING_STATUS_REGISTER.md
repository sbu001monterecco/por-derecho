# DP1901 / E.G.745 / Fiscal Superior — filing-status register

Control date: 20 September 2026  
Control timezone for receipt timestamps: Atlantic/Canary as the working programme timezone; times below are transcribed as printed.  
Repository state: public-safe receipt reconciliation. Private originals remain outside GitHub.

## Current result

**11 of 13 direct personal-action candidates are registered. A06 and A13 remain held and must not be repeated without resolving their documented prerequisites.**

| ID | Destination / function | Registration evidence | Controlled state |
|---|---|---|---|
| A01 | Decanato / Registro y Reparto via DGRAJ | `REGAGE26e00082034813` | REGISTERED_RECEIPT_VERIFIED |
| A02 | Plaza 6 / DP 1901/2026 | `S000000000000144968` + supplement `S000000000000144972` | REGISTERED_WITH_SUPPLEMENT |
| A03 | CGPJ — Alzada 286/2026 | `REGAGE26e00082030716` | REGISTERED_RECEIPT_VERIFIED |
| A04 | Secretaría de Gobierno del TSJC | `REGAGE26e00082039117` | REGISTERED_RECEIPT_VERIFIED |
| A05 | Coordinación Provincial de LAJ | `REGAGE26e00082040006` | REGISTERED_RECEIPT_VERIFIED |
| A06 | National LAJ / Ministry route | rejected attempt `REGAGE26e00073341477` | HELD_NOT_FILED |
| A07 | Canary Justice Administration / ATLANTE | `REGAGE26e00082038176` | REGISTERED_RECEIPT_VERIFIED |
| A08 | Fiscalía Provincial de Las Palmas | `REGAGE26e00082044751` | REGISTERED_RECEIPT_HASH_VERIFIED |
| A09 | Fiscal Superior de Canarias | `REGAGE26e00082032153` | REGISTERED_RECEIPT_VERIFIED |
| A10 | FGE / Inspección Fiscal | `REGAGE26e00082033336` | REGISTERED_RECEIPT_VERIFIED |
| A11 | Sala de Gobierno via Secretaría de Gobierno del TSJC | `REGAGE26e00082052687` | REGISTERED_RECEIPT_HASH_VERIFIED |
| A12 | Defensor del Pueblo | `REGAGE26e00082055212` | REGISTERED_RECEIPT_HASH_VERIFIED_WITH_TEXT_DISCREPANCY |
| A13 | Fiscalía Anticorrupción | none | HELD_NOT_FILED |

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

- **A06 — held/not filed:** rejected attempt `REGAGE26e00073341477`; exact rejection reason/history and a valid national review route remain unresolved.
- **A13 — held/not filed:** signature/formalisation/admission in Exp.Gub.352/2025 and the Article 266 channel restriction remain unresolved.
- **Counsel-dependent judicial remedy:** separate; excluded from the personal-action count.
- **Substantive E.G.745 response:** separate from A10 and still pending.
- **Provincial email follow-up:** supplementary only; sending/delivery and filing are distinct states.

Machine control: `assets/data/dp1901-direct-action-state-20260920.json`.
