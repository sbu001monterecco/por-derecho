# CONCURSO 36/2012 — DEFINITIVE-TEXT / LIQUIDATION IMPLEMENTATION GATE

Date: 21 Aug 2026
Status: ACTIVE CONTROL
Parent prompt: `archive/prompts/CONCURSO36_DEFINITIVE_TEXT_LIQUIDATION_HARD_CLOSURE_PROMPT_21AUG2026.md`

## Why this gate exists

The current Concurso 36/2012 reconstruction has materially improved the identity, attribution and hashing of the 2017–2018 judicial/LAJ acts. The next controlling question is no longer merely whether those acts exist. It is whether the creditor figure and secured-credit treatment actually used during liquidation can be reconciled with LPB's legally operative definitive creditor texts through a traceable procedural chain.

This gate prevents future threads from silently assuming either:

- that a later liquidation document itself modified the definitive creditor list; or
- that any discrepancy proves misconduct.

## Locked source controls

### C36-JUD-2018-04-16-001 — liquidation-plan Auto

- Alberto López Villarrubia
- seven pages
- clean controlled Drive SHA-256: `2de1527a738658252f81fd3e402622f677280aaed735e5ef117d44c4a06dcd05`
- known larger Gmail scan SHA-256: `bf134e63cc022aec0e8a2c0e428e481cce65ad80a3c6be05933b15a453916b80`
- rejected/unverified older value must not be restored without its source binary: `bf134e63cc0c4d09be7f32536460b6eed206b3e5c7e18de19b2c326c10e15964`

### C36-JUD-2018-04-16-002 — CAM-credit/interest clarification Auto

- Alberto López Villarrubia
- two pages
- SHA-256: `4748ad85af54dac606104e8f93cd71299cfd5878fc32be0bf1d4f236325e59ff`

### 4-Jun-2018 Auto family

- complete three-page authentic court copy located in Gmail `194a98a11920fefd`, `20180604 Auto Aclaracion Auto Aprobacion Plan Liquidacion.pdf`
- the older two-page SHA-256 `867d80f99efc029411a0baef80467a27ceacb649ea41d1ff70f57726f33551c0` is a superseded derivative/source-history object only
- status: `COMPLETE THREE-PAGE CANONICAL COPY — HASH / SERVICE / IMPLEMENTATION BINDING OPEN`
- P1 targets: canonical-copy hash, exact notification/service and downstream implementation

### C36-LAJ-2018-06-15-001

- Diligencia de Ordenación
- Águeda Reyes Almeida, LAJ
- SHA-256: `1298d03daca48284de642299ddb86c6b8ed2900f95d5ce05edf2d491e5f8ade5`
- must be treated as an implementation act, not an Alberto Auto
- must be cross-tested against the existing LAJ complaint/dossier

### C36-JUD-2018-06-26-001

- suspension Auto
- Alberto López Villarrubia
- SHA-256: `4f23ad7e30191b1d32c8708851729f42151c3b095476255d5fe1a5fc43509099`

## Mandatory three-track model

Future work must maintain three separate but linked tracks:

1. **Plan / asset-realisation track** — what the plan and later orders authorised, conditioned, suspended and implemented.
2. **Creditor / definitive-text track** — what credit was formally recognised, what later changes were requested, what statutory route was used, and what figure/classification was actually used.
3. **Notice / appeal / finality / suspension track** — service, appeal, suspension, finality and the timing of implementation.

A line must not be drawn from one track to another unless the documentary bridge is identified.

## Central unresolved test

The repository must ultimately be able to answer:

> What exact recognised concurso credit was legally operative when the liquidation machinery referred to or used the creditor's `crédito firme reconocido`?

And then:

> Did that figure/classification later change, and if so through exactly what statutory and documentary route?

## Public-wording gate

Until the formal mutation chain is established, do not publish as fact that Alberto López Villarrubia `slipped in` a change to LPB's definitive texts.

Acceptable evidence-led formulations include:

- `The presently controlled record does not yet identify the procedural instrument by which the operative definitive creditor figure changed from X to Y.`
- `The amount used in liquidation has not yet been reconciled to an amended definitive list through the modification procedures located in the controlled record.`
- `A compliant formal modification route has now been located and is set out below.`

The wording must follow the evidence outcome, not preselect it.

## Judge page propagation requirement

The existing Alberto López Villarrubia page must eventually contain a dedicated liquidation-chain section linking:

- both distinct 16-Apr Autos;
- 4-Jun;
- 26-Jun suspension;
- later relevant decisions;
- definitive-text/CAM-credit reconciliation;
- what the Judge ordered versus what the AC/LAJ/creditor subsequently did;
- later requests for judicial intervention and the judicial response.

This is a responsibility/knowledge/decision map, not an automatic misconduct finding.

## LAJ complaint propagation requirement

The existing LAJ page/dossier must expressly bind `C36-LAJ-2018-06-15-001` to the complaint analysis.

The 15-Jun Diligencia is a primary checkpoint because it operationalises the 16-Apr/4-Jun liquidation machinery. Future complaint analysis must compare the exact complaint allegations against that act, service/publication, offer evidence, later LAJ acts, the 26-Jun suspension and downstream execution.

Required reciprocal navigation:

`LAJ page ↔ liquidation-plan page ↔ evidence register`

## Separate liquidation-plan page requirement

A dedicated bilingual public page is required when the source reconciliation is sufficiently mature:

- ES: `Plan de Liquidación: autorización, implementación y divergencias`
- EN: equivalent reader-facing page

The page must show expected versus actual implementation, not merely dates.

It must visibly distinguish:

- `VERIFIED COMPLIANCE`
- `VERIFIED DIVERGENCE`
- `POTENTIAL PROCEDURAL ISSUE — EVIDENCE INCOMPLETE`
- `UNABLE TO DETERMINE`

## Immediate recovery priorities

P1:

1. canonical hash, exact service/notification and downstream-implementation binding for the located complete three-page 4-Jun-2018 Auto;
2. actual operative definitive creditor list before the 2018 CAM-credit rulings;
3. any formally amended definitive list after those rulings;
4. request to AC for later modification, if any;
5. AC report on that request;
6. traslado / opposition;
7. incidente concursal if required by the route actually taken;
8. Auto ordering modification, if any;
9. service/finality chain;
10. source showing the exact creditor figure ultimately used in set-off/adjudication.

P1 parallel:

11. service/publication evidence for 15-Jun implementation;
12. full 15-Jun → 26-Jun interval reconstruction;
13. end-to-end €400,000 direct-sale route;
14. later 28-Nov-2018 conveyance linkage;
15. later 2021–2022 implementation and sobrante reconciliation.

## Completion rule

This track is not complete because the prompt exists.

Completion requires a source-led answer to the definitive-text mutation question plus propagation into the relevant internal registers and public pages, followed by build/link/source verification.

Thread deletion safety and docket completeness remain separate concepts.
