# Concurso 36/2012 — creditor-order date primary reinspection

**Date of reinspection:** 29 August 2026  
**Primary source:** Gmail message `163d0e6f6da5d4ed`, attachment/custody filename `AUTO Modificación Textos Definitivos CAM+RETRACTO - 15FEB2018.pdf`  
**Purpose:** resolve the repository conflict between 8 February and 15 February 2018.

## Primary finding

Direct visual/text reinspection of the three-page judicial PDF resolves the date issue:

- the body of the judicial decision states: **`AUTO — En Las Palmas de Gran Canaria, a 8 de febrero de 2018`**;
- the judge's electronic signature is dated **9 February 2018 at 08:38:20**;
- the LAJ's electronic signature is dated **14 February 2018 at 09:09:34**;
- the copy carries a visible annotation **`NOTIFICADO 15/02/2018`**.

Accordingly:

> **8 February 2018 is the date of the Auto. 15 February 2018 is the notification/custody layer visible on this copy, not the date of a separate creditor-substitution Auto.**

The custody filename containing `15FEB2018` must not override the date stated by the judicial instrument itself.

## Why the correction matters

The order is the critical formal definitive-text comparator before the 4 June 2018 liquidation-plan clarification.

The 8-February order reasons that assignment of the credit changes the **holder**, but **not the amount**, for which the definitive texts control. It then orders substitution of Promontoria Holding 122 B.V. by Construcciones Acosta Matos, S.A. for:

- €857,373.81 specially secured; and
- €8,194,877.88 specially secured;
- total fixed specially secured amount: **€9,052,251.69**;
- plus contingent enforcement costs without a self-standing fixed amount in the operative section.

The 4-June clarification later used CAM's 17-May balance-fixing instruments to set an operative improvement/bid amount of:

- €11,887,314.33; and
- €1,278,518.03;
- total: **€13,165,832.36**;
- plus continuing default interest to the extent of the respective real-security limits.

This chronology does not itself decide the legal validity of the later figure. It makes the required reconciliation explicit:

1. what Article 59 lawfully allowed to accrue within each mortgage security;
2. whether that accrual was merely payment/exigibility arithmetic or also required a formal Article 97/97-bis definitive-text modification;
3. whether LEC 214 / LOPJ 267 permitted the 4-June clarification to perform the substantive function attributed to it;
4. what contradiction/review rights existed; and
5. what economic/causal effect the operative threshold produced.

## Superseded repository statement

`assets/data/concurso36-what-court-ordered-v1.json` had previously treated 15 February as the controlling order date and described 8/9/14 February as an unverified reconstruction requiring reinspection.

That narrow date conclusion is now **superseded by primary reinspection**. It is retained only as legacy provenance. Current control is:

- `assets/data/concurso36-what-court-ordered-v2.json`;
- `CHATGPT_START_HERE_CONCURSO36_DUAL_LENS_GOVERNANCE.md`;
- `assets/data/concurso36-procedural-taxonomy-judicial-ac-dual-lens-20260829.json`.

The primary-autos CI gate has also been changed so it validates the corrected layered chronology rather than perpetuating the stale 15-February-as-order-date rule.

## Evidentiary boundary

This correction proves the document's date layers and the content of the order. It does not by itself establish that the 4-June order was unlawful or criminal, nor that the later approximately €13m figure lacked every possible legal basis. Those propositions remain subject to the controlled dry-law and adversarial tests, including the serious Article 59 counterargument.

## Deletion safety

Future agents must not regress to “15 February 2018 Auto” merely because of the custody filename or notification stamp. State the layers separately: **Auto 8 February → judge signature 9 February → LAJ signature 14 February → notified 15 February**.