# CONCURSO 36/2012 — DEFINITIVE-TEXT & LIQUIDATION IMPLEMENTATION HARD-CLOSURE PROMPT

Date: 21 Aug 2026
Status: CONTROLLING EXECUTION PROMPT
Scope: LPB / Concurso 36/2012 / definitive creditor texts / CAM-credit treatment / liquidation plan / Judge / LAJ / AC / appeal-finality chain

## Purpose

Run an evidence-led, end-to-end reconstruction of whether the creditor amount, classification, security treatment and interest position actually used during liquidation can be traced step-by-step back to LPB's legally operative definitive creditor texts.

This is an execution prompt. It is not satisfied by a narrative memorandum, a generic chronology, or a statement that the repository is already complete.

The controlling question is:

> Can the creditor amount/classification/security treatment actually used to implement the liquidation be traced, step by step, back to LPB's legally operative definitive creditor texts?

If YES, show the full documentary chain.
If NO, show exactly where it breaks.
If UNKNOWN because a primary document is missing, identify the exact missing instrument.
Do not bridge a missing link by inference.

## Mandatory starting controls

Before any substantive conclusion, read current `main` and the current Concurso 36/2012 judicial-act, source/hash, notification, appeal/finality, Judge, LAJ, AC, correction and missing-evidence controls.

Preserve the existing verified anti-conflation rules:

- `C36-JUD-2018-04-16-001`: seven-page liquidation-plan Auto, Alberto López Villarrubia, canonical clean Drive SHA-256 `2de1527a738658252f81fd3e402622f677280aaed735e5ef117d44c4a06dcd05`.
- `C36-JUD-2018-04-16-002`: separate two-page CAM-credit/interest clarification Auto, Alberto López Villarrubia, SHA-256 `4748ad85af54dac606104e8f93cd71299cfd5878fc32be0bf1d4f236325e59ff`.
- Do not restore the previously reported unverified seven-page hash `bf134e63cc0c4d09be7f32536460b6eed206b3e5c7e18de19b2c326c10e15964` without locating the exact binary that generates it.
- The 4-Jun-2018 clarification is controlled through a **complete three-page authentic court copy**, Gmail `194a98a11920fefd`, `20180604 Auto Aclaracion Auto Aprobacion Plan Liquidacion.pdf`. The older two-page SHA-256 `867d80f99efc029411a0baef80467a27ceacb649ea41d1ff70f57726f33551c0` is retained only as a superseded derivative/source-history object. Canonical-copy hash, service and downstream-implementation binding remain open.
- `C36-LAJ-2018-06-15-001`: 15-Jun-2018 Diligencia de Ordenación, Águeda Reyes Almeida, SHA-256 `1298d03daca48284de642299ddb86c6b8ed2900f95d5ce05edf2d491e5f8ade5`.
- `C36-JUD-2018-06-26-001`: 26-Jun-2018 suspension Auto, Alberto López Villarrubia, SHA-256 `4f23ad7e30191b1d32c8708851729f42151c3b095476255d5fe1a5fc43509099`.
- 18-May-2021 is not to be resurrected as a generic missing-original blocker merely because older work once described it that way.

## Central definitive-text test

Do not assume that LPB's official definitive creditor texts changed.
Do not assume that a later judicial order automatically changed them.
Do not assume that a liquidation-plan document, creditor demand, mortgage certificate, execution balance, AC spreadsheet, offer arithmetic or eventual adjudication amount is equivalent to the legally operative recognised concurso credit.

Construct a definitive-text mutation ledger from the earliest operative `lista definitiva de acreedores` through every later claimed or actual change affecting the mortgage/privileged credit later associated with CAM.

For every claimed mutation identify:

1. who requested it;
2. exact date;
3. statutory ground relied on;
4. request to the Administración Concursal;
5. AC written report;
6. whether that report was favourable or unfavourable;
7. whether an incidente concursal was legally required in the actual route taken;
8. whether an incidente was filed;
9. parties served / traslado;
10. opposition or allegations;
11. judicial resolution;
12. notification;
13. appeal/finality;
14. resulting amended definitive text;
15. where the amended text was formally incorporated into the concurso.

## Legal caution

Do not state that every post-definitive change necessarily required an incidente concursal.

Apply the Ley 22/2003 version actually in force at the relevant date, including the distinction between the ordinary impugnation route and later permitted modification of definitive texts, and test the procedural consequences of the AC's position. A later-change route must be reconstructed from the actual statute, request, AC report, traslado, incident if required, judicial ruling and operative amended text.

## Competing hypotheses

Test all four and attempt to falsify each:

### H1 — formal lawful modification
The definitive creditor texts were formally and lawfully modified through the applicable statutory process.

### H2 — no textual mutation, but a valid later judicial determination
The definitive text did not change, but a later ruling validly determined an issue such as interest or the secured-credit ceiling without changing the underlying recognised credit.

### H3 — de facto liquidation use without a traced procedural bridge
A materially different amount, classification, security entitlement or interest treatment began to be used in liquidation without a presently identifiable compliant documentary bridge to the operative definitive texts.

### H4 — documentary or arithmetic reconciliation
The apparent discrepancy results from conflated documents, incomplete copies, different creditor predecessors, mathematical treatment, timing, or another non-misconduct explanation.

Do not prefer H3 merely because it is adverse.

## Credit mutation ledger

Create a chronological table with at least:

- effective date;
- document date;
- creditor identity / predecessor / successor;
- principal;
- ordinary interest;
- default interest;
- other amounts;
- total admitted amount;
- privileged-special amount;
- ordinary/subordinated amount if any;
- secured properties;
- mortgage-liability ceiling;
- definitive/provisional/contingent status;
- source;
- stable source/act ID;
- SHA-256 if available;
- legal mechanism causing the change;
- AC position;
- LPB position;
- court determination;
- notice;
- appeal/finality;
- confidence/status.

Then answer numerically:

> What was the `crédito firme reconocido` that the 16-Apr-2018 liquidation Auto allowed a specially privileged creditor to offset against an adjudication price?

## Reverse-engineer the liquidation plan

Create a canonical repository dossier and a separate public page devoted to:

**Concurso 36/2012 — Plan de Liquidación: autorización, implementación y divergencias**

Do not write only a chronology. Use the engineering model:

`rule → condition → responsible actor → required input → decision → required next step → actual next step → output → discrepancy → consequence`

At minimum reconstruct:

- AC liquidation proposal;
- LPB opposition/allegations;
- CAM proposals and competing proposals;
- 15-Feb-2018;
- both distinct 16-Apr-2018 Autos;
- 4-Jun-2018;
- 15-Jun-2018;
- publications/notices;
- offers/better offers;
- LPB appeal;
- 26-Jun-2018 suspension;
- later 2018 acts;
- possession/control developments;
- direct sale of locales/pools/solarium;
- 28-Nov-2018 conveyance sequence;
- later licitation/adjudication steps;
- creditor standing and assignments;
- 2021 realisation decisions;
- 18-May-2021 definitive approval → two separate 15-Oct-2021 confirmation/challenge Autos → two 26-Jan-2022 clarification Autos / testimony-finality bridge (no new award) → 21-Feb-2022 deed;
- set-off/payment/sobrante requirements;
- later conveyance/title consequences.

## Three parallel tracks

The public-facing explanation and internal control must visualise at least three parallel tracks:

### Track A — Plan / asset realisation
Approved rule → conditions → implementation → later realisation/adjudication.

### Track B — Creditor / definitive-text chain
Definitive list → exact recognised amount/classification → later credit/interest rulings → any Article 97 / 97 bis route → any AC report → any incident → any amended text → amount actually used.

Where the bridge is missing, label it:

**MISSING PROCEDURAL BRIDGE — NOT YET PROVEN**

### Track C — Notice / appeal / finality / suspension
Signed date → notification → appeal deadline → appeal → suspension request/order → scope → later finality → implementation before/after each stage.

## Requirement-to-implementation matrix

For every operative condition, record:

| Requirement | Source | Responsible actor | Evidence of compliance | Evidence of divergence | Result |

Include valuation, dación, direct sale, publication, better-offer period, licitation trigger, locales/pools/solarium, creditor standing, recognised-credit set-off, mortgage limits, interest calculation, consignation, sobrante, charge cancellation, AC calculations, judicial approval, LAJ implementation, notices, appeals and suspension.

Use only these result classes:

- `VERIFIED COMPLIANCE`
- `VERIFIED DIVERGENCE`
- `POTENTIAL PROCEDURAL ISSUE — EVIDENCE INCOMPLETE`
- `UNABLE TO DETERMINE`

Do not label conduct illegal, fraudulent, biased, falsified or prevaricatory merely because a document is missing.

## Alberto López Villarrubia page linkage

Locate the existing canonical Judge page; do not create a duplicate person page.

Add a dedicated liquidation-chain section covering, where supported:

- his relevant 2017 acts;
- both 16-Apr-2018 Autos;
- 4-Jun-2018;
- 26-Jun-2018 suspension;
- later judicial decisions relevant to implementation;
- definitive-text / CAM-credit reconciliation;
- what he ordered;
- what happened afterwards;
- what was later brought back before him;
- how he responded or did not respond;
- any proven divergence between earlier judicial conditions and later judicial treatment.

Do not convert institutional responsibility automatically into personal misconduct.

Do not use the phrase `slipped it in` as a factual public conclusion unless direct evidence establishes concealment or equivalent conduct. Prefer exact procedural wording.

## Águeda Reyes Almeida / LAJ complaint linkage

`C36-LAJ-2018-06-15-001` is a mandatory primary evidential bridge into the existing LAJ complaint/dossier.

The 15-Jun-2018 Diligencia is not merely a chronology node. It is a concrete implementation act translating the 16-Apr/4-Jun judicial rulings into the dación/direct-sale/better-offer machinery.

Cross-check each complaint allegation against:

- exact 15-Jun wording;
- 16-Apr plan Auto;
- 4-Jun Auto;
- service/publication evidence;
- offers;
- later Diligencias/Decretos;
- 26-Jun suspension;
- downstream implementation.

Create a complaint allegation/evidence matrix with:

- allegation;
- date originally raised;
- complained-of conduct;
- relevant LAJ act;
- supporting evidence;
- contradicting evidence;
- missing evidence;
- present evidential status.

Add reciprocal links:

`LAJ page ↔ liquidation-plan page ↔ evidence register`.

## 15-Jun → 26-Jun interval

Reconstruct this interval particularly hard:

- exact effect of 15-Jun Diligencia;
- service date;
- publications;
- start/end of better-offer period;
- existing offers;
- LPB appeal timing;
- suspension application timing;
- 26-Jun decision;
- acts already performed by 26-Jun;
- assets covered by suspension;
- operations left running;
- anything later treated as irreversible during the interval.

Do not infer from dates alone; recover receipts and underlying acts.

## €400,000 route

Reconstruct end-to-end the authorised direct sale of locales and pools/solarium for €400,000:

- exact assets;
- ownership;
- valuation;
- purchaser;
- publication;
- better-offer mechanism;
- competing offers;
- licitation trigger;
- AC role;
- LAJ role;
- Judge role;
- LPB objections;
- appeal/suspension implications;
- 28-Nov-2018 conveyance;
- compliance with every upstream condition;
- later appearance in 2022 perimeter/transaction if proved.

## Complete 4-Jun-2018 Auto located — binding remains P1

Use the complete three-page canonical copy located in Gmail `194a98a11920fefd`. Preserve the older two-page binary and SHA-256 `867d80f99efc029411a0baef80467a27ceacb649ea41d1ff70f57726f33551c0` only as derivative source history; it is not the best copy and does not create a separate act.

The remaining P1 work is to bind the canonical three-page hash, exact service/notification record and downstream implementation. Do not reopen continuation-page recovery unless later evidence shows that the three-page copy itself is defective.

## Exact final questions

The execution report must answer:

1. Did LPB's official definitive creditor texts change?
2. If yes, identify the exact procedural act and operative amended version.
3. If no formal change can presently be established, say so.
4. Was an incidente concursal required in the actual route taken?
5. Was one filed?
6. What AC report exists?
7. What traslado/hearing exists?
8. What Auto authorised the change, if any?
9. What version became operative?
10. What was CAM's legally operative `crédito firme reconocido`?
11. What did the 16-Apr plan Auto authorise?
12. What did the separate 16-Apr CAM-credit Auto decide?
13. What can presently be proved about 4-Jun?
14. What did 15-Jun implement?
15. What did LPB appeal?
16. What did 26-Jun suspend?
17. What happened notwithstanding/after suspension?
18. Which conditions were complied with?
19. Which were demonstrably diverged from?
20. Which remain unresolved?
21. Which steps belong to the Judge?
22. Which belong to the LAJ?
23. Which belong to the AC?
24. Which belong to CAM?
25. Which were challenged by LPB?
26. What was added to the dedicated liquidation page?
27. What was added/corrected on the Judge page?
28. How was the 15-Jun Diligencia connected to the LAJ complaint?
29. What cross-links were created?
30. What allegations were deliberately not made due to insufficient evidence?
31. PR number and merge SHA;
32. files created/modified;
33. post-merge verification;
34. remaining P1 blockers;
35. deletion-safety status.

## Definition of done

Do not conflate:

- work executed within available evidence;
- evidential closure;
- publication readiness;
- deletion safety.

A thread may be deletion-safe while the docket remains incomplete.

The strongest completion test is not `done`; it is:

> **Show the actual amended texto definitivo, or show the complete lawful substitute chain, or show the exact point where the procedural bridge is missing.**
