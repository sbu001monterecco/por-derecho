# Sun Park — 28-upload source digitisation and publication control

**Control date:** 23 August 2026  
**Status:** draft public-safe repository control; private source binaries are not committed  
**Supersedes for corpus counts:** the 18-upload count in `SUN_PARK_ACTIVE_ESTATE_2018_2021_EIGHT_SOURCE_SUPPLEMENT_23AUG2026.md`  
**Machine companion:** `assets/data/sun-park-28-upload-source-manifest-v1.json`

## 1. Controlling result

Twenty-eight supplied filenames resolve to **twenty-six unique binaries and twenty-five documentary items**:

- the two files labelled as the 1-March-2018 photographic packet are exact duplicates;
- `Juicio Desahucio por Precario 1240-2011.pdf` is byte-for-byte identical to the already controlled `Demanda Desahucio Minorias 1260-2011.pdf`; `1240-2011` is a false filename alias, not a second proceeding;
- two CAM prints are source variants of the same February-2021 opposition, not separate pleadings; and
- the two Autos dated 24 February 2021 are distinct judicial acts and must never be conflated.

The exact originals remain in the private preservation layer. The public repository receives hashes, neutral aliases, redacted text derivatives, source cards and bounded gap requests. A filename, allegation, confidential draft or later recital is not converted into a finding.

**Route-scope decision:** retain the stable `...active-estate-2018-2021/` / `...masa-activa-2018-2021/` slugs, while expressly describing the dossier as 2017–2021. The 19-Dec-2017 opening Auto is the necessary legal anchor for the 2018 plan and later preservation/extension sequence, not a silent change of evidential scope.

## 2. Ten later uploads — reconciliation

| Control | Neutral identity | SHA-256 | Pages | Source status | Public treatment |
|---|---|---|---:|---|---|
| `C36-JUD-2018-04-16-001` | Auto approving the liquidation plan, with modifications/conditions | `6a64515f3504762bc6f44747d64d61d9a7ec99e7367d6bd3ae9ade9ebe9eaacf` | 7 | Complete scan-derived copy of an already known official act | Full redacted substantive transcript; no unredacted binary |
| `C36-PTY-2019-01-16-001` | Party filing opposing operations reported in the fourth liquidation report | `fde56be1cb8d95adac76162ca210de457d95cc6c69fb449c5745ad7fc122bb0c` | 9 | Party pleading; receipt, annexes and direct outcome absent | Balanced source card/digest, paired with the later non-convalidation sequence |
| `VAL-ORD1859-2023-EX07-LA-CAJA-2008-RECEIPTS` | Exhibit of 2008 La Caja loan/interest/hedge receipts | `0ae57307cc5b73bfaac351d808e5c8801881dcd177d3c0fae5bd1e390183652d` | 10 | Exhibit only; parent filing/index absent; filename's “Liquidaciones” does not make it a Concurso liquidation act | Private/hash-only; no account numbers or tax identifiers on the website |
| `C36-EXW-DRAFT-2018-05-10-VALUATION-REASONABLENESS` | Four Mirror / Expert Witness valuation critique commissioned by Aweswell | `ccf1d76f6791ce47e0af02162df5317f786a8ad6ec08c50784a83fabf52911a4` | 26 | Marked “strictly private and confidential” and “draft subject to changes”; no visible signature or filing stamp | Metadata and limitations only; no full public text without authority/final signed version |
| `C36-JUD-2017-12-19-001` | Auto opening LPB's liquidation phase | `3f1a239121e213ee26e4abaaa7a50940107389117c7c7ba73d83e6f149cf49f1` | 3 | Complete official electronic-copy derivative of an already controlled act | Full redacted substantive transcript |
| `C36-JUD-2021-02-24-002` | Auto granting a one-year extension of liquidation | `9841c9aa91e2fa0cf49eeff249928b0ac66dc54912853e77b83d9b1b73bbd27d` | 2 | Complete scan-derived official act; distinct from `MAT-008` | Full redacted substantive transcript; stable same-date ID |
| `PROC-1260-2011-INIT-ALIAS` | Misnamed alias of the 23-Dec-2011 JV 1260/2011 initiating pleading | `407a38eb93de7bf0be44ebf4b747df2f7cf0a4ab6f49296eb7d9b42fb51d340d` | 9 | Exact duplicate of `TS-04`; page 9 duplicates the substantive final page; annexes 1–16 absent | Alias record only; do not ingest or count twice |
| `DI248-2019-02-06-NEW-EVIDENCE` | Submission of asserted new evidence to Fiscalía, signed 7-Feb-2019 | `3252a77770158c9c2d46de8ac7fcd2817360a51a874577fd8e3402aa3d0392ba` | 5 | Party submission; annexes 1–3, receipt and express prosecutorial treatment absent | Redacted digest paired with the 7-May-2019 archive decree |
| `AP89-2014-JV1260` | AP Las Palmas Sentencia 89/2014, roll 793/2012 | `1bce9ad6111645393ee2f23915b7df05a9a879181f2c19fad83f6b3e8989c1ec` | 7 | Complete official appellate judgment; finality/enforcement record absent | Full redacted substantive transcript and prominent adverse holding |
| `PO213-2015-APPEAL-2018-12-07` | Matkator appeal against the 12-Nov-2018 judgment | `d8186d84e7e2919a8e1caf130b36f6ddc39b8862a2cbfca24c407a5f178d3fd9` | 11 | Party pleading; annexes 1–6 and appellate result absent | Redacted digest; not presented as an adjudicated result |

## 3. Material corrections and anti-conflation rules

### 3.1 JV 1260/2011

Sentencia 89/2014 is materially adverse and must travel with the 2011/2012 pleadings. The Audiencia Provincial:

- upheld the claimant side's appeal;
- partially reversed the first-instance judgment;
- ordered eviction of both CEXP and Monterecco Sun Park, S.L. from the **eighteen claimant-owned units**;
- imposed first-instance costs on Monterecco; and
- reasoned that Monterecco possessed the relevant keys/units and that the relationship between CEXP, Monterecco and LPB justified veil lifting in that dispute.

It did **not** adjudicate possession or title over the whole mixed-ownership complex, later governance, later works, the 2018 control event or criminal responsibility. The 54 CAM / 190 LPB / 18 third-party-unit distinction used elsewhere must not be silently replaced by the eighteen-unit perimeter litigated in JV 1260/2011.

### 3.2 16-April-2018 plan Auto

The Auto approved the AC plan with judicial precisions. It authorised the proposed CAM route for the listed mortgaged apartments by dación en pago and a separate direct-sale component for listed premises/pools at **EUR 400,000**, subject to publication and the ten-day better-offer mechanism in then Article 155.4 LC. It also established fallback direct-sale/substitution rules and quarterly reporting.

The Auto did not state or adopt the Actúa figures of EUR 9.776m, EUR 7.097m or EUR 6.608m. The 10-May valuation draft's statement that the court accepted the Actúa figure as the reasonable value of the security is therefore a **party-expert interpretation that overreads the located Auto**, not a judicial finding.

### 3.3 Two separate Autos on 24-February-2021

| Stable ID | Pages / hash | Matter | Operative result |
|---|---|---|---|
| `MAT-008` / `C36-JUD-2021-02-24-001` | 4 / `3b02a944…` | Aweswell reposición concerning inspection, expert evidence and conservation | Partially allowed only to replace the sparse reasoning; denial of filing 7,299 maintained |
| `C36-JUD-2021-02-24-002` | 2 / `9841c9aa…` | AC request to extend the liquidation period | One-year extension granted from the order date |

The second Auto mentions anticipated nullity actions against Bankia as one reason delay appeared foreseeable. It does not use the word “swap”; `No-Swap` is an editorial filename label and must not become a public title or holding.

### 3.4 2008 receipt exhibit

`...DOC 7 _ Liquidaciones.PDF` is not an order, report or quarterly liquidation record in Concurso 36/2012. Its pages are 2008 La Caja receipts relating to loan interest and an interest-coverage/hedge account. The supplied filename suggests it was exhibit 7 in Valencia Ordinary Proceedings 1859/2023, but the parent filing and exhibit index are missing. No conclusion about the swap/hedge, default, debt or later insolvency figure should be drawn until each transaction is reconciled to the loan, account ledger and parent proceeding.

## 4. Publication decision

### Website — present now in the draft dossier

1. 19-Dec-2017 liquidation-opening Auto — redacted full substantive transcript.
2. 16-Apr-2018 plan-approval Auto — redacted full substantive transcript and `decided / not decided` box.
3. 12-May-2020 reposición Auto — redacted full substantive transcript; explain that the demolition/access requests were new and procedurally extemporaneous in that motion, not decided on their merits.
4. 24-Feb-2021 `MAT-008` preservation/inspection Auto — redacted full substantive transcript with opposing positions and the limited operative result.
5. 24-Feb-2021 extension Auto — separate full substantive transcript.
6. Source cards for the 16-Jan-2019 filing, the Aweswell/CAM 2020–2021 pleadings and the 8-Mar-2021 access email, always paired with the official outcome/gaps.
7. Sentencia 89/2014 on the existing JV 1260 flagship route and as contextual adverse material, not as an active-estate holding.

### Repository only / digest

- the 2018 confidential valuation draft;
- PO 213/2015 appeal pending annex/outcome recovery;
- DI 248 February-2019 party submission, paired with the later archive;
- the 2011 complaint alias/duplicate;
- email content beyond a redacted request/response chronology; and
- the photo packet pending originals, metadata, identities and neutral contextual proof.

### Private/hash-only

- the 2008 bank/hedge receipts and account identifiers;
- private originals, verification codes, signatures, private addresses and unnecessary third-party identity data; and
- any confidential valuation working papers or unapproved final report.

## 5. New finite production requests

These rows continue `ME-PDFSCAN-001`–`022`; they do not create a second missing-evidence queue.

| ID | Exact request | Why it matters | Status after this batch |
|---|---|---|---|
| `ME-PDFSCAN-023` | **No parallel request created.** The AP 89/2014, false-alias and residual first-instance/finality/enforcement/annex findings are merged into canonical `ME-PDFSCAN-017`. | Prevents a second JV 1260 retrieval queue. | SUPERSEDED / MERGED INTO `ME-PDFSCAN-017` |
| `ME-PDFSCAN-024` | Native signed 19-Dec-2017 and 16-Apr-2018 Autos, service/finality/publication records; AC plan dated 18-Jan; LPB/Aweswell observations; same-date clarification; every valuation/offer annex. | Separates what the court approved from what parties/experts said the court adopted. | PARTIAL — two complete derivative Autos located |
| `ME-PDFSCAN-025` | Third and fourth Article-152 reports; filing/service proofs; deed 2,150 of 28-Nov-2018; cheque/bank trace for EUR 400,000; 12-Dec Diligencia, challenges, 24-Oct-2019 Auto and downstream title/accounting result. | Tests the 16-Jan-2019 party allegation against the complete official/implementation record. | PARTIAL — opposition located, outcome chain incomplete |
| `ME-PDFSCAN-026` | Final signed 10-May-2018 expert report and authority to distribute; engagement/instructions, working papers and source copies of Actúa 15-Jan-2018, Gesvalt Mar-2018, Tinsa 2008/2015/2017 and AC 2012 values; any rebuttal/cross-examination/judicial treatment. | The supplied expert PDF is confidential, draft and source-dependent; one conclusion overreads the 16-Apr Auto. | PARTIAL — draft only |
| `ME-PDFSCAN-027` | Certified full PO 213/2015 docket: 12-Nov-2018 judgment, 18-Sep intervention request, 10-Oct/6-Nov orders, Community allanamiento/authority, annexes 1–6, appeal receipt/oppositions and final AP disposition/finality. | The appeal proves a position was advanced, not that it succeeded. | PARTIAL — appeal pleading only |
| `ME-PDFSCAN-028` | **No parallel request created.** Receipt, annexes and treatment of the 6/7-Feb-2019 submission are merged into canonical `ME-PDFSCAN-019`. | Prevents a second DI 248 retrieval queue while preserving the new finite question. | SUPERSEDED / MERGED INTO `ME-PDFSCAN-019` |
| `ME-PDFSCAN-029` | Parent filing, exhibit index and judicial admission/treatment for Valencia Ordinary Proceedings 1859/2023 document 7; native bank statements, loan/hedge contracts, settlement formulae and transaction-level reconciliation. | Prevents old receipts from being mislabeled as Concurso liquidation records or as self-proving a debt/swap conclusion. | PARTIAL — orphan exhibit only |
| `ME-PDFSCAN-030` | 4-Feb-2020 extension Providencia; AC applications for the 2020 and 2021 extensions; party responses; service/finality; every later extension and actual close-out; filed Bankia/nullity actions and outcomes. | Tests the reason, duration and implementation of the extension rather than relying on its recital alone. | PARTIAL — 24-Feb-2021 extension Auto located |
| `ME-PDFSCAN-031` | Complete Article-152 quarterly-report run from opening to conclusion, with annexes, filing dates, asset inventory, conservation work, receipts/payments and court responses. | The opening and plan Autos imposed a recurring reporting obligation; selected reports cannot establish the whole estate history. | OPEN |

## 6. Cross-thread scan rule

Any email, Drive, device or later ChatGPT thread that locates a requested source must:

1. preserve the native file before OCR or redaction;
2. record original filename, bytes, SHA-256, acquisition date, custodian and parent/variant/duplicate relation;
3. update the controlling `ME-PDFSCAN-*` row rather than opening a generic duplicate;
4. bind annexes to the exact filing/order and record receipt, service and outcome separately;
5. retain private/confidential originals outside public Git;
6. create public derivatives only after PII, privilege, confidentiality and proposition-status review; and
7. never describe a draft PR as merged, deployed or live.

## 7. Remaining release gate

The draft bilingual dossier and text derivatives may be reviewed in the open draft PR. Public PDFs, confidential valuation text, bank receipts, unblurred photographs and private email remain excluded. Merge and deployment remain separate decisions after link, parity, redaction and rendered-page review.
