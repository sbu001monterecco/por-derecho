# Concurso 36/2012 — Judicial Acts and Implementation Register

**Date:** 21 August 2026  
**Status:** canonical repository control for the 2018–2022 transaction/judicial implementation spine  
**Machine-readable companion:** `assets/data/concurso36-judicial-spine-v1.json`

## Governing rule

Do not treat the 2022 result as one generic “adjudication event”. Reconstruct each legal step separately:

**proposal → judicial authorization → competitive process → later order/clarification → deed → court return/communication → Registry → accounting → final economic result.**

A later recital is not a substitute for the signed original act it describes. An authorization is not proof of correct implementation. A repeated number is not necessarily the same legal/economic object each time it appears.

## Canonical money-function rule

**recognized insolvency credit ≠ mortgage liability ≠ third-bidder threshold ≠ debt stated as consideration for the dation ≠ registry value ≠ eventual surplus/remanente.**

Every transition from one function to another requires an identifiable legal and documentary bridge.

## Current spine

| Canonical ID | Date | Instrument/node | Current source status | What can presently be said | Critical unresolved bridge |
|---|---|---|---|---|---|
| C36-JA-2018-TRANSACTION | 2018 | Plan / transaction architecture | Partial | Repository reconstruction separates mortgaged-finca dation from a EUR 400,000 non-mortgaged locales/pools line. | Original complete operative instruments, bank/ledger treatment and final title of locales/pools. |
| C36-JA-2021-01-25 | 25 Jan 2021 | Auto | Primary verified | Explains arithmetic movement from EUR 3,079,104.66 toward the EUR 3,182,000 mortgage ceiling within the improvement framework. | Underlying interest certificate/calculation and the legal classification of the amount available for set-off. |
| C36-JA-2021-01-29 | 29 Jan 2021 | Edicto | Primary verified | Publishes quantified conditions including EUR 13,168,082.02, EUR 400,000 and EUR 1,145,798.29 Community amount. | These figures must not be relabelled as one purchase price or one recognized credit. |
| C36-JA-2021-02-08-THIRD-OFFER | 8 Feb 2021 | Third-party EUR 14.8m proposal | Partial | A concrete competing proposal exists. | Filing, capacity/funds, hearing treatment and exact disposition. |
| C36-JA-2021-05-18 | 18 May 2021 | Material authorization/adjudication node | Later recital / incomplete primary chain | Later 2022 materials reproduce this as a material decision concerning the plan and competition. | Original signed Auto, complete comparecencia/licitación record, service and appeals. |
| C36-JA-2021-10-15-A | 15 Oct 2021 | Auto A | Partial | Current reconstruction records one order as treating the auction/competitive event as having occurred. | Signed original, docket position, exact scope. |
| C36-JA-2021-10-15-B | 15 Oct 2021 | Auto B | Partial | Current reconstruction records another same-date order as saying bidding had not taken place. | Signed original, docket position, exact scope and contextual reconciliation. |
| C36-JA-2022-01-FAMILY | Jan 2022 | January order / clarification family | OPEN | Deed 457 recites an Auto of 22 Jan; other repository references use 26 Jan. These must be treated as a family until disaggregated. | Every signed January act, request, docket entry and service record. |
| C36-JA-2022-02-21-DEED457 | 21 Feb 2022 | Escritura n.º 457 | Primary verified | The 76-page deed transfers described mortgaged fincas and states EUR 13,168,082.02 as debt serving as consideration; it requires communication to the Mercantile Court within five days. | Legal bridge for the debt figure, court return, mandamiento, Registry and accounts. |
| C36-JA-2022-04-20-REGISTRY | 20 Apr 2022 | Registry implementation | Partial | Current reconstruction records downstream registration in CAM’s favour. | Full finca-by-finca registry history and cancellation/mandamiento chain. |
| C36-JA-ACCOUNTS-SURPLUS | — | Liquidation accounts / surplus | OPEN | No complete primary bridge presently reconciles credit, interest, EUR 400k, dation, cash, costs and surplus. | AC workbook, rendición, bank/ledger, final balance and final judicial resolution. |

## P0 retrieval order

1. Recover and read the **original signed Auto of 18 May 2021**.
2. Recover **both original signed orders of 15 October 2021**, with docket order, applications, notifications and any clarification.
3. Recover the **complete January 2022 family**, expressly resolving the 22 January / 26 January date references instrument by instrument.
4. Recover the 2021–2022 **testimonios**, underlying CAM/AC requests, service logs and downstream notarial/Registry use.
5. Recover the **post-deed court filing within/after the five-day period**, subsequent resolution/mandamiento and Registry execution.
6. Recover the **AC accounting bridge** and separately reconcile EUR 400,000, interest, dation entries, cash/costs and any remanente.

These tasks consolidate existing `ME-005` to `ME-008`, `ME-011` and `ME-012`; they do not replace or duplicate the Missing Evidence Register.

## Asset-perimeter control

The judicial spine must be linked to an **Order → Asset** ledger. For every finca or asset class, record:

- pre-concurso owner;
- whether it entered LPB’s estate and on what source;
- mortgage/security status;
- treatment in the plan/competitive process;
- treatment in each operative order;
- inclusion/exclusion from deed 457;
- Registry result;
- later corporate transfer, if any.

**LPB estate property must never be merged by shorthand with Matkator or other third-party property.** A whole-complex operational or possession narrative is not itself a finca-level title bridge.

## Money-function control

The spine must be linked to an **Order → Money** ledger. At minimum, track:

- EUR 3,079,104.66;
- EUR 3,182,000;
- EUR 13,168,082.02;
- EUR 400,000;
- EUR 1,145,798.29;
- EUR 14,713,880.31;
- EUR 14,800,000;
- any later accounting value, costs, cash entries and remanente.

For every amount record: source, date, legal function, debtor/creditor, whether cash or non-cash, whether recognized/claimed/capped/threshold/consideration/accounting entry, and the act authorizing any change of function.

## Implementation control

The spine must be linked to an **Order → Implementation** ledger. For every judicial authorization, ask:

1. What exactly was authorized or refused?
2. What conditions applied?
3. Who had to act next?
4. What document proves that act occurred?
5. Was it timely and within scope?
6. Which deed/mandamiento/Registry/bank/accounting entry implemented it?
7. What later document relied on it?
8. What remained unresolved?

## Public wording correction

Avoid generic shorthand such as:

> “the 26 January 2022 adjudication order”

unless a specific source and function are stated.

Prefer:

> “the January 2022 order/clarification family, including a deed recital referring to 22 January and other repository references to 26 January, pending recovery and instrument-by-instrument reconciliation of the signed originals.”

This is a narrowing correction. It neither strengthens nor weakens any allegation by itself.

## Evidential limits

- A missing primary act is not evidence that it does not exist.
- An apparent contradiction between later summaries may disappear when the signed originals and procedural context are recovered.
- Registration is evidence of a Registry result, not automatic proof that every prior substantive or accounting condition was correct.
- A deed is primary evidence of what the deed states and effects within its scope; it does not by itself prove the legal correctness of every recited debt component.
- A competitive third-party offer is material evidence of a real alternative but not proof that the offer complied with every condition or had to win.
- No surplus/remanente should be asserted as established or excluded until the primary accounting chain is closed.

## Propagation rule

Any future primary source that changes one node must propagate to:

1. this register and its JSON companion;
2. `archive/CORRECTION_REGISTER.md` where prior wording becomes unsafe;
3. `archive/MISSING_EVIDENCE_REGISTER.md` by updating the existing item rather than duplicating it;
4. the Spanish and English adjudication pages;
5. homepage/timeline references that use the affected date or figure;
6. any allegation, recovery, CGPJ, Fiscalía, lender or asset-recovery module that relies on the superseded proposition.

## Current conclusion

The repository already contains enough primary material to define the decisive question with precision, but not yet to close it:

**Can the complete signed judicial record demonstrate an unbroken, legally explained chain from the transaction proposed, through competition and the 2021/January-2022 orders, into deed 457, finca-level registration and final accounts, without an unexplained change in asset perimeter, authority, or the legal function of a material money figure?**

That is the controlling reconstruction question until the P0 evidence chain is closed.

## 23-Aug-2026 judicial-omission allegation control

Gil alleges that specified resolutions, refusals and delays of Judge Alberto López Villarrubia preserved or legitimised the 2018 private-control result. This register must not convert a missing source, adverse outcome or incomplete protection into prevarication. For each alleged act, record the exact filing/request and receipt, evidence before the judge, competence and duty, resolution/refusal/delay, objective injustice or arbitrariness, knowledge or malicious purpose, causation and contrary explanation. Classify the conduct under CP Articles 446–449 rather than importing administrative-prevarication omission doctrine automatically. Apply the full matrix in `archive/CAM_2017_2018_DIRECT_INSTRUCTION_LENDER_POSSESSION_SHADOW_ADMINISTRATION_JUDICIAL_OMISSION_LEAD_23AUG2026.md`.
