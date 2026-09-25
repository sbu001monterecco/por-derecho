# Primary reinspection — CAM definitive-text Auto date correction

**Date of control:** 29 August 2026  
**Proceeding:** Concurso ordinario 36/2012, Juzgado de lo Mercantil nº 1 de Las Palmas de Gran Canaria  
**Source family:** Gmail message `163d0e6f6da5d4ed`, attachment filename `AUTO Modificación Textos Definitivos CAM+RETRACTO - 15FEB2018.pdf` (3 pages).

## Controlling primary finding

Direct reinspection of the three-page authentic electronic copy resolves the repository's prior date-layer conflict.

The judicial body states on page 1:

> `AUTO` — `En Las Palmas de Gran Canaria, a 8 de febrero de 2018.`

The electronic-authenticity footer records:

- Magistrado-Juez Alberto López Villarrubia: electronic signature **09/02/2018 08:38:20**.
- LAJ Águeda Reyes Almeida: electronic signature **14/02/2018 09:09:34**.

The custody/filename layer uses **15FEB2018**. That later date must not replace the date printed in the body of the Auto. Repository references that treated 15 February as the controlling ruling date are therefore superseded by this direct primary reinspection and must be repaired.

## Operative amount rule

Page 2 expressly accepts LPB's amount objection. In substance, the court says that a credit assignment changes **only the creditor's identity, not the amount**, for which the definitive texts control regardless of what the assignment deed states.

The dispositive part recognises CAM as holder, replacing Promontoria Holding 122 B.V., of:

- €857,373.81 special-privilege mortgage claim (loan 2801);
- €8,194,877.88 special-privilege mortgage claim (loan 3000);
- contingent special-privilege enforcement costs without their own quantified amount.

Fixed special-privilege amount: **€9,052,251.69**, plus the separately described unquantified contingent costs.

## Governance consequence

1. The controlling act date is **8 February 2018**; 9 and 14 February are signature layers; 15 February is a later custody/notification-family label unless a primary notification document establishes its exact procedural function.
2. The 8-February Auto is a formal **Article 97 bis definitive-text modification** and an essential comparator for later calculations.
3. The 4-June-2018 clarification must not be silently treated as a further definitive-text amendment merely because it records a materially larger CAM balance/threshold.
4. Any route from €9,052,251.69 to later figures must be reconstructed component-by-component and legal-gateway-by-legal-gateway, including the serious counterargument concerning post-insolvency secured interest under former LC Article 59 and applicable mortgage caps.
5. No repository intelligence may again convert a filename, service date, signature date or later recital into the date of the judicial act when the primary document itself states another date.

## Required downstream repair

The following descendants are now marked for correction before merge of the dual-lens PR:

- `assets/data/concurso36-what-court-ordered-v1.json`;
- ES/EN critical-orders readers;
- `assets/data/concurso36-continuity-governance-20260829.json`;
- runtime continuity JS where it renders the comparator;
- `scripts/validate_concurso36_primary_autos_redigest.py` and any derivative gate that encodes the superseded 15-Feb ruling-date assertion.

This correction strengthens, rather than weakens, the evidence-control model: **primary document > filename/reconstruction > later derivative**.
