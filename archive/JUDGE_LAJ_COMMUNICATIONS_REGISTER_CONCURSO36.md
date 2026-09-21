# Judge, LAJ and party-communication register — Concurso 36/2012

**Control date:** 23 August 2026
**Proceeding:** Concurso ordinario 36/2012 · NIG 3501647120120000351
**Canonical source:** `assets/data/concurso36-complete-record-v1.json`
**Status:** public-safe crosswalk of the located corpus; no certified docket, no official denominator and no claim that every communication or response is present

## 1. Purpose and method

This register links a party's located filing or communication to the next located Judge, Appeal Court, LAJ or court-office act that can safely be associated with it. It does not assume that chronological proximity proves a response, that joinder proves acceptance, or that a later judicial act resolved every proposition in an earlier filing.

Each row uses canonical IDs. The `Response` column means the narrow procedural or judicial response documented by the cited record. `No direct response isolated` means exactly that; it is not evidence of silence, non-service, refusal or concealment.

The current inventory contains **127 canonical records**: **40 judicial acts**, **39 LAJ/court-office acts**, **1 unresolved judicial/LAJ act type**, **34 party filings**, **2 party communications**, and **11 records of the remaining classes**. Within the exact **72-row historical corpus** there are **34 judicial acts**, **20 LAJ/court-office acts**, **1 unresolved judicial/LAJ act type** and **7 party filings**. The unresolved record is `C36-E071`, described only as “Auto or decreto”; it is not assigned to either authority class without the signed source. The specialist corpus adds **25 court/LAJ acts** and **25 party filings**. These counts describe the current corpus, not the court file.

Current result labels remain:

- `INVENTORY PARTIAL — CERTIFIED DOCKET OR RECORDS STILL MISSING`
- `PUBLICATION COMPLETE FOR THE IDENTIFIED PUBLIC-SAFE CORPUS — NOT THE WHOLE COURT FILE`

## 2. Non-merger map

| Lane | Canonical IDs | Kept separate from |
|---|---|---|
| Historical Concurso record, including liquidation/implementation | `C36-E001`–`C36-E072` | Later removal, fee, criminal, disciplinary and other external proceedings |
| AC removal, Section 2 and appeals | `C36-SPECIALIST-R01`–`R32`; RPL 3304/2025 + 3319/2025 | Fee action and RPL 421/2026 |
| AC remuneration/civil-liability action | `C36-SPECIALIST-F01`–`F18`; ORD 641/2024; RPL 421/2026 | Removal appeals |
| Supplemental evidence inputs | `C36-SUP-*` | A court act unless a signed procedural record proves joinder or reliance |
| Calificación judgment | `C36-E070` and its still-incomplete appeal/finality chain | Criminal guilt or a retrospective title/implementation ruling |
| Decanato reference 22, DP 1901/2026, DP 1956/2026 and DIP 80/2026 | Separate source families outside this canonical crosswalk | Each other and the Concurso record absent an official allocation/joinder act |

Formal pleadings are treated as party-to-court communications. Informal correspondence is separately classified; `C36-SUP-MAT-009` and `C36-SUP-ACSEC-2018-02-27` presently fall in the canonical `party_communication` class.

## 3. Historical Concurso crosswalk

| Source / canonical ID | Status | Action or communication | Located court/LAJ response | Next proof required |
|---|---|---|---|---|
| `C36-E001` | Complete primary Auto | Court declares voluntary concurso, appoints Francisco de Borja Rodríguez-Batllori Laffitte and orders updated inventory | Opening judicial act; no precursor party application is canonicalised in this dataset | Voluntary petition, service, AC acceptance, updated inventory and any appointment-continuity acts |
| `C36-E004` → `C36-E007` | Earlier providencia reported/missing; substitution act located | Court required exhibition of assignment material; current repository control treats **15 Feb 2018** as the CAM holder-substitution date | `C36-E007` recognises holder substitution without proving assignment economics or later implementation | Reinspect complete signed binary and service metadata under the 15-Feb control; obtain assignment deed, notice, challenge and finality chain |
| `C36-E005` + `C36-E006` | Complete party instruments; proposal, not authority | CAM makes a conditioned offer; AC files liquidation plan | `C36-E008` approves a conditioned plan; `C36-E009` and `C36-E012` address separate clarification questions | Filed annexes, service, opposition set, appeal/finality and final condition-performance ledger |
| `C36-E008` → `C36-E013` | Complete court/LAJ acts | Plan authority requires publicity and better-offer process | `C36-E013` directs publication and competitive period | Publication proofs, service to all parties, exact close of period and complete challenge chain |
| `C36-E014` | Complete primary Auto | Suspends realisation of listed mortgaged apartments while other liquidation continues | No broader possession, works, operation or income authority in the act | Service/finality; precise implementation and any later lifting/modification |
| `C36-E016` | Complete AC filing | AC asks for testimony of existing April/June Autos | `C36-E017` directs delivery of the testimony | Delivered testimony, receipt and proof of the use made of it; testimony cannot enlarge authority |
| `C36-E018` | Complete AC filing | AC opposes CAM reposición and says the plan Auto is not final; anticipates EUR 400,000 branch | No direct merits response isolated; `C36-E020` is a later procedural direction, not a substitute merits answer | Exact reposición decision/service and complete EUR 400,000 cash/title/accounting chain |
| `C36-E019` + `C36-E020` | Deed status uncertain; LAJ act complete | Protocol 2150 is executed; a later LAJ direction declares the better-offer period closed and directs formalisation | `C36-E029` later sets aside `C36-E020` and refuses convalidation; `C36-E032` confirms | Deed authority/notice, all consideration and title evidence, undoing/restitution steps, service and finality |
| `C36-E024` | Complete joint LPB/Aweswell filing | Requests disclosure of AC decisions/contracts and raises timing and `ob rem` issues | `C36-E025` records/routs challenges; it does not accept allegations | Court-stamped filing/annex set, all service, AC/CAM responses and exact ruling per request |
| `C36-E026` | Original missing; existence proved by later primary recital | AC seeks post-event convalidation of Protocol 2150 | `C36-E029` refuses convalidation and orders republication | Original application, annexes, filing/service receipt and any separate relief not captured in the later recital |
| `C36-E030` | Complete primary Auto | Court rejects AC request to exclude Aweswell from participation | Judicial response preserves procedural participation only | Underlying AC application, complete oppositions/service and any appeal/finality record |
| `C36-SUP-MAT-006` | Source copy located; annex absent; party allegations | Aweswell seeks estate preservation and inspection on 18 Dec 2020 | `C36-E034` is a reported missing preservation act; `C36-E040` later decides urgent works/access issues | Cited annex, court-stamped receipt, `C36-E034` signed original, service and precise operative relationship to `C36-E040` |
| `C36-SUP-MAT-007` | Source copy located; annex absent; party counter-position | CAM opposes the preservation/inspection request | `C36-E040` records competing positions and maintains refusal of requested measures without deciding title/possession/exploitation | Cited annex, proof of filing/service, complete hearing material and implementation evidence |
| `C36-SUP-MAT-009` | Rendered primary communication copy; authentication/outcome open | Expert-access request and response chronology involving party correspondence and the AC | No signed court/LAJ response or complete downstream outcome isolated | Native RFC822, headers, attachments, all replies, proof of receipt and any resulting court filing/order |
| `C36-SUP-ACSEC-2018-02-27` | Restricted source copy; public-safe PDF/transcripts; native thread absent | AC asks the Community president to convene a meeting to consider security against unauthorised access and deterioration/improper use | No judicial/LAJ act in this record; the later Community authority and implementation must be proved separately | Native RFC822/thread and attachments; receipt; summons/minutes/vote; security contract, payer, instructions, access logs and exact relationship to later acts |
| `C36-E038` | Complete proposed text; filing/authority unresolved | Third-party bidder proposes EUR 14.8m cash posture subject to conditions | `C36-E043` convenes licitation and fixes bond; `C36-E044` approves CAM after recorded nonappearance/nondeposit | Filed original, authority, proof of funds, bond demand/payment, appearance/hearing record, notices and exact treatment of every condition |
| `C36-E045` → `C36-E048` | Judicial demand reported/missing; LAJ receipt act complete | Court reportedly requires a detailed AC liquidation report and warns of possible responsibility | `C36-E048` joins and transfers report 7425/2021; report contents are not in the corpus | Signed demand, report 7425/2021, service, objections and any judicial assessment or enforcement |
| `C36-E049` | Complete AC quarterly report; actor representation | AC reports deed outstanding, treasury and mass-credit payments | No direct court merits response isolated | Underlying bank ledger, invoices, receipts, objections, resulting court act and reconciliation to later deed/final accounts |
| `C36-E054` → `C36-E055` | LAJ act and notarial deed complete; implementation unresolved | LAJ supplies testimony/finality treatment; AC/CAM execute Protocol 457 | Deed requires return/report to court within five natural days; no resulting court act is canonicalised | Five-day return receipt, AC report, court response/mandamiento, finca-by-finca registry/cancellation, final debt/cash/surplus accounting |
| `C36-E070` | Complete first-instance judgment; unresolved finality | Court issues Sentencia 163/2023 in Calificación | First-instance result only; it is not a criminal conviction | Certified hearing record, appeal, all appellate decisions, service and finality |

## 4. AC-removal lane crosswalk — kept within Section 2 / RPL 3304 and 3319

| Source / canonical ID | Status | Action or communication | Located court/LAJ response | Next proof required |
|---|---|---|---|---|
| `C36-SPECIALIST-R01` | Complete redacted party filing | Aweswell files the 23 Apr 2025 removal application | `R02` joins it and gives the AC five days | Court-stamped filing/annex set and complete service receipt |
| `R03` | Complete redacted AC opposition | AC opposes removal | `R04` joins the opposition and puts the matter before the judge | Filing receipt, annexes and any other party response |
| `R01` + `R03` → `R05` | Source copies located | Competing removal and opposition positions | Auto 1377/2025 dismisses for Aweswell's standing without entering the seven merits blocks | Full service and LPB's exact procedural posture; no merits inference |
| `R07` + `R08` | Complete redacted reposición filings | Aweswell and LPB challenge Auto 1377/2025 | `R09` rejects both, confirms the standing barrier and opens non-suspensive appeal | Service/finality and complete appellate record |
| `R10` + `R11` | Complete redacted appeal filings | LPB and Aweswell appeal removal outcome | `R12`–`R16` form separate rolls and direct elevation/appearance/deposit | Certified lower-court remittal, complete notices, deposits and roll contents |
| `R17`–`R25` | Located party filings and LAJ routing acts | Parties oppose, impugn and address the appellate procedural dispute | `R19`, `R21` and `R22` record narrow processing/transfer effects | Complete service receipts and exact rulings on each contested procedural point |
| `R26`–`R29` | Located Appeal Court/LAJ acts and party document | Court schedules deliberation; parties add material; LAJ promotes accumulation | `R30` accumulates RPL 3319/2025 into RPL 3304/2025 and orders missing steps | Certified combined roll, proof all ordered steps completed and subsequent merits decision |
| `R31` + `R32` | Complete redacted party allegations | LPB and Aweswell file post-accumulation allegations | No later signed merits decision located | Signed merits outcome, service and finality; do not treat filing or accumulation as adjudication |

## 5. AC-remuneration lane crosswalk — kept within ORD 641/2024 / RPL 421/2026

| Source / canonical ID | Status | Action or communication | Located court/LAJ response | Next proof required |
|---|---|---|---|---|
| `C36-SPECIALIST-F01` | Complete redacted party filing | Aweswell files EUR 110,956.97 remuneration/civil-liability claim | `F02` transfers to Mercantile Court 1; `F03` admits and summons; `F04` directs insurer service | Court-stamped source, annex set, allocation trail and complete service returns |
| `F05` + `F06` | Complete redacted defence filings | Insurer and AC oppose the claim | `F07` joins defences and calls a preliminary hearing | Filing/service receipts and complete defence annexes |
| `F08` | Complete redacted party filing | Aweswell files further allegations after the defences | `F09` later resets preliminary hearing and defers evidence to the hearing; direct causal linkage is not assumed | Exact intervening acts, service and reason for rescheduling |
| `F10` | Complete redacted clarification request | Aweswell asks to clarify the 1 Sep 2025 decree | `F11` and `F12` oppose; `F14` refuses clarification | Standalone 1 Sep 2025 decree, service and the exact record that generated the clarification incident |
| `F01`, `F05`, `F06` → `F13` | Complete redacted source copies | Competing claim and defences proceed to first-instance judgment | Judgment 4/2026 dismisses for standing, with costs, without deciding fee legality or quantum | Complete 20 Jan 2026 preliminary-hearing minutes/recording, evidence rulings and service |
| `F15` + `F16` | Complete redacted party filings | Aweswell appeals; AC asks that judgment be declared final | `F17` forms RPL 421/2026; `F18` treats appeal as filed and transfers it | Full appellate roll, oppositions/impugnations, signed merits decision, service and finality |

## 6. Response-status rules

Use only these meanings when this register is cited:

| Status | Meaning |
|---|---|
| `Complete primary act` | The reviewed corpus contains a complete copy of the identified instrument |
| `Source copy located` | A controlled source copy exists; its effect is limited to what the document proves |
| `Reported/missing` | The instrument is identified by a docket lead or later primary recital but its complete original is not located |
| `Party allegation/counter-position` | Proves the party advanced the proposition, not its truth |
| `Procedural response` | Joinder, transfer, service, admission, routing or scheduling only; not merits acceptance |
| `Judicial response` | Limited to the decision's actual operative and reasoned scope |
| `No direct response isolated` | The reviewed corpus does not yet identify a specific response; no inference about actual court conduct is permitted |
| `Unresolved implementation` | Authority or a deed is located, but physical, registry, accounting, service or finality proof remains incomplete |

## 7. Date-layer control

The CAM holder-substitution act is controlled for current repository/publication purposes at **15 February 2018** and cross-referenced as `C36-E007`. Do not revive an older alternate date reconstruction. The complete binary, signature layer, notification/service event and metadata must be reinspected together, and any correction must propagate atomically through the JSON, registers, timelines, public pages and validators.

## 8. Public/private and connector boundary

This register intentionally omits private message locators, personal contact data, electronic verification identifiers, bank/policy data and unredacted attachments. It points to canonical IDs rather than exposing source-account details.

The repository/history and live-site surfaces were reconciled. Three restricted PDFs were hash-matched to custody controls. Gmail, Google Drive and Library connectors returned no usable corpus in this run. Those null results are coverage/access limitations, not proof of non-existence or deletion. Native email acquisition, complete attachment chains and court-stamped filing/service receipts remain production tasks.

## 9. Twelve controlled next-proof priorities

1. Certified section-by-section chronological docket and sealed court export.
2. Complete filing, service, LexNET/ATLANTE and finality chain for every material act.
3. Minutes and recording of the 20 Jan 2026 preliminary hearing.
4. Certified 25 Jul 2023 hearing minutes, AV index/evidence rulings and disposition of the 26 Jul programme.
5. Complete 18 May 2021 third-party offer, authority, funding, bond, appearance/hearing and treatment.
6. Underlying AP complaint 375/22 order and reconciliation of the conflicting July 2022 recitals.
7. Protocol 457 five-day return, court response/mandamiento and all-finca registry/cancellation proof.
8. Complete assignment and final compensable-debt/source-system accounting bridge.
9. Complete EUR 400,000 premises/pools title, cash, restitution and accounting chain.
10. AC report 5367/2022, later reports, estate ledger/bank, final accounts and conclusion order.
11. Signed merits outcomes and finality for RPL 421/2026 and combined RPL 3304/3319.
12. Native RFC822/full response chain for `MAT-009` and filing receipts for editable specialist pleadings.

## 10. Maintenance rule

Add a row only when the source is assigned a stable canonical ID. Attach alternate copies, duplicate emails and facsimiles to that ID; do not count them as new acts. A new response must identify its proceeding, decision-maker, exact effect, service and finality status. Cross-evidence may be linked across proceedings, but procedure, allegations and legal effect must remain separate unless a signed allocation, joinder or accumulation act says otherwise.

Controlling companion sources:

- `archive/CONCURSO36_COMPLETE_RECORD_EXECUTION_DIGEST_23AUG2026.md`
- `archive/CONCURSO_36_2012_DOCKET_WIDE_DISCOVERY_PROMOTION_REGISTER_17AUG2026.md`
- `archive/CONCURSO_36_2012_CANONICAL_COURT_BINARY_REGISTER_17AUG2026.md`
- `archive/CONCURSO_36_2012_NOTIFICATION_SERVICE_COMPLETE_REGISTER_17AUG2026.md`
- `archive/CONCURSO_36_2012_APPEAL_AND_FINALITY_MASTER_REGISTER_17AUG2026.md`
- `archive/CONCURSO36_AUTOS_FULLTEXT_UNITARY_RECORD_23AUG2026.md`
- `archive/AC_SEPARATION_FEES_AUTOS_DP1901_REFERENCE22_UNITARY_DIGEST_23AUG2026.md`
