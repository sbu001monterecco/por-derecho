# REVERSE-ENGINEERING FORENSIC REDIGEST — CONCURSO 36/2012

## Mission

Reconstruct Concurso 36/2012, Juzgado de lo Mercantil nº 1 de Las Palmas, as a system of legally significant state transitions. Do not write a conventional chronology and do not start from later narratives. Start with the best primary judicial text and work outward, asset by asset, right by right, condition by condition and euro by euro.

The central test is:

> Starting only with the actual judicial orders and the estate as it really existed, can an unbroken legal, factual and accounting chain be proved from LPB’s opening estate, through possession and exploitation from 2018 onward, to the 2021 approval, the 2022 deed and Registry effects, and the later HNT/Canarian Hospitality/MYND position?

Where the chain breaks, identify the exact node, competing explanations, decisive missing evidence, probable holder, retrieval route, and the conclusion that would follow if the evidence proves or disproves the bridge.

## Non-negotiable evidential rules

1. Primary judicial, notarial, registry, banking, corporate and contemporaneous filed documents control over repository summaries, website prose, emails, pleadings and repeated allegations.
2. Separate five propositions that are often conflated:
   - the document is authentic;
   - a person or document made a recital;
   - the recital is factually true;
   - the act produced a particular legal effect;
   - the effect applied to a particular asset, person or amount.
3. Never convert a recital, party assertion, assumption, filing, later deed, registry sample or professional description into an operative judicial finding.
4. Use exactly these labels at proposition level:
   - PROVEN BY PRIMARY DOCUMENT
   - STRONGLY SUPPORTED
   - INFERENCE
   - UNRESOLVED
   - CONTRADICTED
   - DOCUMENT NOT YET LOCATED
5. Rank contradictions:
   - A — contradicted by the operative text or another controlling primary document;
   - B — strong inconsistency requiring explanation;
   - C — unresolved evidential gap;
   - D — hypothesis only.
6. A negative search result must be expressed as “not identified in the reviewed corpus”, never as proof that no document exists in the certified court file.
7. Use “No primary evidence of payment has yet been identified” unless a primary ledger, bank record, receipt or court-account record proves payment or non-payment.
8. Do not infer fraud, collusion, intent, professional misconduct, procedural illegality, criminality or invalidity from a gap, role, error, adverse decision or later benefit.

## Phase 1 — Freeze and inventory the evidence system

Before substantive analysis:

1. Record the exact repository commit and deployed-site version.
2. Inventory every source system searched: local workspace, repository, live site, Google Drive, Gmail, Library/uploads, court-file extracts, notarial material, Registry material and public filings.
3. Create one immutable source row per binary or native revision with:
   - source ID;
   - document ID and exact filename;
   - source system and stable locator;
   - retrieval time;
   - byte size, MIME type and page count;
   - complete/incomplete/core-text-complete/filed-package-incomplete status;
   - full SHA-256;
   - signature/CSV verification result;
   - annex status;
   - source relationship and supersession status;
   - page-level quotation anchors.
4. Split composite packages into individual acts and attachments. Never cite a multi-document bundle as though it were one act.
5. Preserve body date, judge-signature date, LAJ-signature date, notification date, filing date and filename alias in separate fields.
6. Build a source-supersession map. Mark every earlier digest or workpaper displaced by a stronger primary source; do not silently overwrite the audit trail.

## Phase 2 — Reconstruct the judicial state machine

For every material auto, sentencia, providencia, diligencia, decreto, aclaración, rectificación, testimonio, appeal or implementation act, create a structured record:

### A. Identity

- canonical act ID;
- exact body date and all signature/service dates;
- court, section, proceeding/NIG and incident;
- issuing judge or LAJ;
- document type and legal function;
- pages, completeness, annexes and source integrity.

### B. Application and participation

- applicant and relief requested;
- supporters and opponents;
- who was heard, notified or served;
- who apparently was not heard, with the distinction between proven absence, documentary absence and court-file verification required;
- representations placed before the court.

### C. Facts and law

- each factual proposition expressly accepted;
- each material party assertion merely recited;
- statutory provisions and actual reasoning;
- unresolved fact the court declined or did not need to decide.

### D. Operative text

Quote the decisive Spanish language accurately and translate it faithfully. Assign one function label to each operative proposition:

- AUTHORISATION
- APPROVAL
- ACKNOWLEDGEMENT
- CONDITIONAL APPROVAL
- PROVISIONAL MEASURE
- ASSUMPTION/RECITAL
- PROCEDURAL DIRECTION
- CLARIFICATION
- FINAL DISPOSITION

### E. Conditions and legal gates

For every requirement record the exact source text, obligor, deadline, proof of performance, and consequence of failure. Classify it as:

- express condition precedent;
- express condition subsequent;
- offer term;
- reporting/performance duty;
- statutory obligation;
- Registry/opposability step;
- charge-cancellation step;
- evidential implementation step;
- later approval or accounting requirement.

Answer separately:

> WHAT HAD TO HAPPEN BEFORE THE EFFECT LATER ATTRIBUTED TO THIS ORDER COULD LAWFULLY OCCUR?

Do not assume that registration, cancellation, reporting or finality all operate as identical title conditions. Obtain legal analysis where the consequence depends on Spanish property or insolvency law.

## Phase 3 — Asset and rights topology

Create a certified universe table that reconciles every denominator used in the material, including 159, 171, 220, 251, 262, 31, 29, 54, 190 and 18. For each finca, physical unit and relevant right, track at each critical date:

- registered owner and source;
- cadastral/architectural mapping;
- LPB inventory treatment;
- definitive-text treatment;
- liquidation-plan/Annex treatment;
- appraisal treatment and valuation perimeter;
- 2018 locales treatment;
- 2021 approval treatment;
- 2022 deed and Registry treatment;
- present claimed owner, operator and user.

Separate:

1. LPB-owned assets;
2. Matkator-owned assets;
3. other third-party apartments;
4. locales, pools and solaria;
5. common and ob-rem/appurtenant rights;
6. exploitation/business rights and Community/CEXP positions;
7. furniture/equipment;
8. keys, security and physical possession;
9. receivables, bookings, rent and income;
10. goodwill, customer relationships and data;
11. licences, authorisations and administrative rights.

Treat inclusion in ACTÚA/GESVALT or a whole-complex appraisal as valuation scope only unless title/estate inclusion is separately proved.

For Matkator samples 8584, 8588 and every additional lead, create this chain:

`registered owner → inventory → liquidation plan → 2021 approval → 2022 deed → Registry → later CAM/HNT/operator claim`

At every missing transition write: **NO IDENTIFIABLE LEGAL BRIDGE YET LOCATED**.

## Phase 4 — Factual control and economic-benefit reconstruction

Prove the factual event before testing authority. Build an event ledger for the period immediately before 7 June 2018 through the 2022 deed:

- actor;
- date/time;
- exact finca/right/space;
- keys, access, security, exclusion, works, demolition, operation, bookings and income;
- duration;
- source and evidence strength;
- economic beneficiary;
- judicial, ownership, Community/CEXP, contractual or administrative authority relied upon.

For every material transition ask:

> What judicial or non-judicial authority, if any, authorised this exact act over this exact asset or right?

If no primary judicial authority is found, state:

> NO PRIMARY JUDICIAL AUTHORISATION YET IDENTIFIED.

Then test competing lawful explanations such as co-owner rights, owner consent, Community resolution, lease, management contract, licence or AC authority. Do not equate absence of a court order with illegality.

## Phase 5 — Transaction and euro ledgers

### A. Creditor chain

Reconstruct Bankia → SAREB → PH122/relevant vehicle → CAM. For each link record deed, schedule, price, proof of payment, registration, court recognition, AC verification, objections, powers and exact legal person.

### B. Debt bridge

Reconcile every component from the definitive-text credit to the closing/deed amount, day by day and classification by classification:

- principal;
- ordinary interest;
- default interest;
- post-insolvency interest;
- mortgage cap;
- costs;
- Community conditions;
- other amounts;
- extinguished/compensated amount.

Arithmetic identity is not legal entitlement. Preserve each number’s function and perimeter.

### C. Valuation bridge

For every ACTÚA, GESVALT, TINSA or later value record date, purpose, instruction, methodology, condition assumption, asset universe, ownership universe, occupier/operation assumption and court use. Do not compare figures as like-for-like until perimeter and purpose match.

### D. Locales and €400,000

Trace buyer debit → cheque clearing → estate credit → fees/taxes/creditor application → balance → reversal, restitution or legal cure → final Registry and accounts. Separate Protocol 2150, the later non-convalidation rulings, 2021 reapproval and any fresh deed/ratification.

### E. Sobrante

Identify the operative legal trigger before calculating. Build:

`authorised closing value or price – final allowed compensable debt – permitted deductions = possible sobrante`

Then locate recipient, deadline, bank/court deposit, estate ledger, AC report and later judicial treatment. Do not call a cross-perimeter arithmetic difference a surplus.

## Phase 6 — Judicial knowledge, participation and AC audit

At each critical date distinguish:

- evidence created elsewhere;
- filed in the court;
- accepted by the office;
- served on parties;
- put before the judge;
- cited or decided;
- later contradicted or corrected.

Build judge/LAJ assignment chronology. Do not equate institutional file presence with actual knowledge by a particular decision-maker.

For the AC, reconstruct every application, report, inventory, valuation statement, ownership description, debt calculation, transaction report and accounting entry. Compare each with contemporaneous contrary evidence. Separate error, incomplete information, dispute and deliberate conduct unless intent is independently proved.

## Phase 7 — Reverse-engineer the repository and live website

Audit the current remote and live deployment, not only a local checkout.

1. Trace every public claim through:

   `primary source → canonical claim record → structured JSON/CSV → static ES/EN HTML → runtime JavaScript injection → rendered DOM`

2. Identify stale or contradictory descendants when a primary source changes.
3. Disambiguate multiple acts issued on the same date; never use date as the unique act ID.
4. Test whether validators check identity, date, function, operative result, asset scope and final rendered DOM.
5. Treat every file in a public Pages repository as public. A `REPOSITORY-ONLY`, `PRIVATE` or `DO-NOT-PUBLISH` label is not access control.
6. Produce exact P0/P1/P2 correction tickets with file, line/claim ID, live route, current text, replacement text, primary basis, descendants and release test.
7. Preserve the live erroneous version as correction evidence before changes.
8. Propose a single canonical claim/evidence graph with `supersedes` and `invalidates` relationships and build-time generation.

## Phase 8 — Adversarial redigest

Treat every prior report, evidence index and component workpaper as a hypothesis. Search for:

- silent supersession;
- conflicting OCR/transcriptions;
- “complete” used for an incomplete filed package;
- composite source IDs;
- document-level labels applied to proposition-level conclusions;
- legal conditions mixed with later implementation evidence;
- overstatement of finality, registration or title effect;
- omitted adverse evidence;
- denominator/perimeter drift;
- arithmetic without legal function;
- a later recital used to prove an earlier condition;
- a single-finca sample generalised across the transaction;
- a website correction register contradicted by the primary document it purports to correct.

For every surviving conclusion record the strongest falsifying alternative and the document that would decide between them.

## Mandatory closure register

Create one row per break with:

- Gap ID;
- event/claim;
- expected legal/factual/accounting chain;
- currently proved;
- exact break;
- competing explanations;
- decisive missing evidence;
- probable holder;
- best retrieval route;
- conclusion if proved;
- conclusion if disproved;
- priority P0/P1/P2;
- status;
- evidence label;
- contradiction rank;
- affected site/repository claims.

## Conclusion ladder

Separate:

1. conclusions presently proven;
2. conclusions supportable after one identified gate closes;
3. conclusions presently unavailable;
4. conclusions contradicted and requiring correction;
5. prior findings expressly superseded by this rerun.

## Outputs

Produce and preserve:

1. Executive forensic finding, maximum 2–3 pages.
2. Delta/supersession report against the prior scan.
3. Master critical-act table with function and conditions.
4. 18 May 2021 → 26 January 2022 → 21 February 2022 deep-dive.
5. Asset/title/right matrix.
6. 2018–2022 authority and economic-benefit ledger.
7. Locales/€400,000 module.
8. Credit, debt, valuation and sobrante ledgers.
9. Judicial-knowledge, procedural-rights and AC audit.
10. Contradiction matrix.
11. Gap-closure register in machine-readable and spreadsheet form.
12. Missing-document register with exact retrieval routes.
13. Repository/live-site remediation plan and proposed page: **Concurso 36/2012 — What the Court Actually Ordered**.
14. Top 20 questions the primary record requires somebody to answer.
15. Thirty-day closure sequence.
16. Source manifest, hashes and bundled workpapers.

The final answer must state whether the chain closes for:

- enumerated LPB assets;
- third-party/Matkator assets;
- possession and exploitation from 2018;
- the locales branch;
- the debt extinguished at closing;
- any sobrante;
- Registry implementation;
- CAM→HNT and current operator rights.

If any answer is “not yet”, identify the exact break and the shortest evidence route capable of changing it.
