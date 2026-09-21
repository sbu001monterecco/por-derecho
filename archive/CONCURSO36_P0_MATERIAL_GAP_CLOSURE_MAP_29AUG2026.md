# Concurso 36/2012 — P0 material-gap closure map

- **Control date:** 29 August 2026
- **Repository baseline:** `main` re-resolved at `77531a51abb2eda352def4297f0aceb3ea166e94` after PR #1194
- **Purpose:** narrow the nine existing P0 evidence families to source-level closure states without pretending that a located subnode closes the family.
- **Evidence effect:** no allegation is adjudicated; no complete docket, AC-report series, appeal family or final-stage family is claimed.
- **External-action boundary:** this control does not authorise email, filing, preservation request or authority contact.

## Status model

Use one of these states for every material family:

- `OPEN_UNLOCATED` — the controlling source required by the closure test has not been located in the controlled corpus.
- `PRIMARY_LOCATED_PENDING_PROMOTION` — a primary source has been located in a connected controlled source, but has not yet been promoted into the canonical public evidence corpus.
- `PARTIAL_FAMILY_LOCATED` — one or more primary nodes are located, but the procedural family remains incomplete.
- `DISCOVERY_DENOMINATOR_LOCATED__CERTIFIED_OPEN` — a discovery/index source exists, but the official certified denominator remains missing.
- `PARTIAL_PROCEDURAL_CHAIN_LOCATED__MERITS_OPEN` — current procedural nodes are located, but merits/service/finality remain open.
- `OPEN_UNLOCATED_POST_LIQUIDATION` — liquidation-completion indicators exist, but the final accounts/conclusion family remains unlocated.
- `CLOSED` — use only when the exact pre-existing closure test is satisfied.

The count remains **nine P0 families open**. Status refinement does not reduce the denominator.

## Material-family reconciliation

| P0 family | Reconciled status | Primary / controlled nodes now located | What still closes the family | Priority |
|---|---|---|---|---|
| `CERTIFIED-DENOMINATOR` | `DISCOVERY_DENOMINATOR_LOCATED__CERTIFIED_OPEN` | Historical chronological workbook and controlled docket discovery register provide a candidate discovery spine. | Signed/electronic court or LAJ chronological denominator for every section and incident from 1 January 2014 through conclusion; reconcile every candidate row to the source. | P0-2 |
| `ORIGINALS-2014-2016` | `OPEN_UNLOCATED` | Existing derivative references remain discovery material. | Signed 29 April 2014 act; 2015 acts; 1 April and 1 June 2016 acts; definitive-text chain and service/review where applicable. | P0-7 |
| `BARE-REFERENCES` | `OPEN_UNLOCATED` | References `204/14`, `677/14`, `2418/14`, `5599/2015` remain identifiers rather than promoted decisions. | Locate and authenticate the underlying instruments and procedural families. | P0-8 |
| `REPORTED-JUDICIAL-ACTS` | `PARTIAL_FAMILY_LOCATED` | The controlled decision register contains promoted and derivative nodes, with favourable/neutral acts preserved. | Signed originals and complete families for C36-E004, E031, E034, E045, E056, E060, E062 and E063. | P0-6 |
| `OCTOBER-2021-CHAIN` | `PARTIAL_FAMILY_LOCATED` | Primary AC report dated **25 October 2021** located; signed LAJ Diligencia de Ordenación dated **27 October 2021** records filing **7425/2021** and transfer; connected records also locate candidates for filing **7336/2021** and requests **7416/7417**. | Promote/verify 7336/2021, 7416/7417, issued testimonios, annex completeness, service, challenges, decisions and finality. | P0-3 |
| `AC-REPORT-SERIES` | `PARTIAL_FAMILY_LOCATED` | Primary/controlled material now includes the 20 September 2018 report; located 4th and 6th report copies; 25 October 2021 report / 7425/2021; primary **25 January 2022** report; primary **25 April 2022** report with a same-date liquidation-operations list/annex and LAJ/court receipt chain recording filing **3016/2022** on 28 April 2022; signed LAJ receipt of **5367/2022** on 27 July 2022; later quarterly-report families in November 2022, March/June/September 2023, January/September 2024 and November 2025. The recovered notification package for 5367/2022 records the quarterly-report filing but does **not** contain the underlying quarterly report itself. | Recover and authenticate the underlying document filed as 5367/2022 and any later supply/service copy; build the ordinal/date/registration/receipt/annex matrix; locate the **15th quarterly liquidation report** without inferring that 5367/2022 is the 15th unless the source proves it; recover every missing report/annex; reconcile ledger/bank movements; then final accounts. | **P0-1** |
| `REVIEW-2022-2023` | `PARTIAL_FAMILY_LOCATED` | Primary **Auto 74/2023 of 6 March 2023 in RQE 375/2022** located; official **Tribunal Constitucional providencia of 23 October 2023 in amparo 2811/2023** located; RQE 379/2022 finality/return-to-origin candidate located. | Signed 9 March, 16 June, 20 June and 13 July 2022 acts; complete RQE 375/379 filing/service/finality families; promote official primary copies. | P0-4 |
| `CURRENT-APPEALS` | `PARTIAL_PROCEDURAL_CHAIN_LOCATED__MERITS_OPEN` | Current procedural nodes located for RPL 2523/2025; combined RPL 3304/2025 + 3319/2025; and RPL 421/2026. A targeted 29 August 2026 sweep did not locate merits decisions in the controlled connected corpus. | Merits decision for each appeal, service, any clarification/review, finality and implementation. | P0-5 |
| `FINAL-STAGE` | `OPEN_UNLOCATED_POST_LIQUIDATION` | Primary AC reports dated 2 November 2022, 20 June 2023 and 24 November 2025 state that the debtor's assets had been liquidated in the terms of the **15th quarterly liquidation report**. The 24 November 2025 report records treasury of **€2,098** held in the court account, no pending credits against the estate, and retention only for expenses needed to finish liquidation/conclusion. | Locate the 15th report; identify any later AC report; final accounts/rendición; transfer; objections; approval/refusal; service; finality; conclusion order; implementation/accounting. | **P0-1** |

## Highest-leverage closure sequence

The most efficient sequence is not chronological. It follows document families that collapse multiple uncertainties at once:

1. **Underlying 5367/2022 quarterly report + 15th quarterly liquidation report + AC report denominator.** The 27 July 2022 LAJ act proves that a quarterly report was filed as 5367/2022, but the recovered notification package does not carry the underlying report. Later primary reports repeatedly point to the 15th report as the liquidation-completion source. First recover the exact document behind 5367/2022 and any later supply/service copy; then determine from the source itself whether it bears an ordinal. Do **not** equate 5367/2022 with the 15th report from chronology alone. This recovery lane can narrow both `AC-REPORT-SERIES` and `FINAL-STAGE`.
2. **Final accounts/conclusion chain.** Once the 15th report and later report denominator are controlled, search specifically for rendición/final accounts, transfer, objections, approval/refusal, service/finality and conclusion. Do not infer a conclusion order from liquidation completion.
3. **October 2021 family.** Promote the already located 25 October report and 27 October 7425/2021 receipt, then attach 7336/2021, 7416/7417, testimonios, annexes, service and challenges. This should turn a formerly broad P0 gap into a small missing-node list.
4. **2022–2023 review family.** Promote the primary RQE 375/2022 Auto 74/2023 and official TC 2811/2023 providencia, then complete RQE 379/2022 and the four named 2022 signed acts.
5. **Candidate denominator reconciliation.** Use the historical workbook only as a locator. Join every row to a signed primary/official source, preserve same-date acts separately, and compute the exact unresolved delta before any certified-index request.
6. **Current appeals.** Preserve the latest procedural node for each appeal and keep the merits endpoint open until an official merits decision, service and finality are located.
7. **2014–2016 originals, bare references and remaining C36-E families.** These remain necessary for docket completeness, but presently close fewer current-state uncertainties than the AC/final-stage and current-review families.
8. **P1 date ambiguities last.** Reinspect the 8/15 February 2018 layers and the 13 January 2022 candidate only after the P0 source families above are narrowed.

## AC-report matrix to build next

Minimum columns:

`ordinal_if_known | report_date | filing_registration | LAJ_receipt_date | report_primary | notification_contains_report | later_supply_or_service | annexes | challenge | decision | finality | source_hash | canonical_path | notes`

Do not back-fill an ordinal from chronology alone. An ordinal is controlled only where the source says it or the certified docket establishes it.

### Already located anchors

- 20 September 2018 quarterly report — primary Drive copy located.
- 4th quarterly report — primary/controlled Drive copy located.
- 6th quarterly report — primary/controlled Drive copy located.
- 25 October 2021 report — primary copy located; filing 7425/2021 accepted 27 October 2021.
- **25 January 2022 quarterly report — primary connected-source copy located.**
- **25 April 2022 quarterly report — primary connected-source copy located, together with a same-date liquidation-operations list/annex; court/LAJ traffic records filing 3016/2022 and a 28 April 2022 Diligencia de Ordenación.**
- **27 July 2022 — signed LAJ receipt of filing 5367/2022 located. The recovered notification package identifies the quarterly report but does not contain the underlying report. A targeted connected-source sweep has not yet located a primary copy of that underlying document.**
- 2 November 2022 report — primary copy located and already refers back to the 15th report.
- March 2023 family — report/receipt family located.
- 20 June 2023 report / 23 June receipt family — primary report located and again refers back to the 15th report.
- 28 September / 20 October 2023 family — located.
- 11 January 2024 / registration 105/2024 family — located.
- 17 September 2024 / registration 4675/2024 family — located.
- 24 November / 27 November 2025 / registration 7294/2025 family — primary report and signed LAJ receipt located.

## Public wording rule

The public continuity page may say:

> Nine P0 evidence families remain open. Primary-source recovery has materially narrowed several of them: the October 2021 chain, the AC-report series and the 2022–2023 review family now contain located primary nodes, while current appeals have located procedural nodes but no merits endpoint yet located. Within the AC-report series, the 27 July 2022 LAJ receipt for filing 5367/2022 is located, but the underlying quarterly report has not yet been located in the controlled corpus. No family is treated as closed until its pre-existing closure test is satisfied.

Do not publish private mailbox identifiers, private contact data, counsel advice, or derivative allegations as evidence. Primary court/LAJ/AC instruments may be promoted only after source verification, privacy review and canonical hashing.

## Next evidential target

**Recover and authenticate the underlying quarterly report filed as 5367/2022, then locate and authenticate the 15th quarterly liquidation report.**

The 5367/2022 receipt is now a precise missing-source pointer rather than a generic gap. The 15th report remains the strongest single substantive target because later primary AC reports repeatedly identify it as the operative description of completed asset liquidation. The two may prove to be the same document, but the control must not say so unless the underlying source establishes that identity or ordinal.
