# START HERE — Concurso 36/2012 dual-lens / criminal-first final handoff

**Cut-off:** 29 August 2026  
**Status:** POST-MERGE CONTINUITY CLOSEOUT  
**Purpose:** deletion-safe continuation of the 29-August Concurso 36/2012 work concerning definitive texts, procedural taxonomy, the 7-June-2018 takeover/notice chain, judge/AC review, counsel conduct, convenio, lender workout and liquidation implementation.

## Immediate verified state

- PR **#1207**, `Concurso 36/2012: lock dual-lens judicial/AC governance`, is **MERGED**.
- Final repaired PR head: `fdf81d5bbc10dfee74a7dbdab271a7d57b49c77b`.
- PR #1207 merge commit: `06bc3ba415091c1d0f1f9ac5c68a5e71766ae0f1`.
- Before merge, **all 13 PR workflows were green**, including `Validate Concurso 36/2012 complete record`, `Validate primary Autos re-digest`, publication integrity, criminal-misuse, privacy, smoke, preservation and related controls.
- The complete-record blocker was repaired rather than bypassed: `.github/workflows/validate-concurso36-complete-record.yml` now compiles both legacy/current validators and executes `scripts/validate_concurso36_complete_record_v2.py`, which preserves the legacy denominator/privacy/discovery controls while replacing only the disproved date prohibition with positive primary-source date-layer assertions.
- The immediate merge-SHA Pages run #1278 was cancelled because a direct descendant commit superseded it. The descendant `main` commit `1c2fd5944ecf6d33606ce4763d4f4742e56aa33c` has parent `06bc3ba415091c1d0f1f9ac5c68a5e71766ae0f1`, therefore contains the full #1207 merge, and **Pages run #1279 (`33271810286`) completed successfully** for that descendant.
- Publication-integrity, privacy/OSINT, visual identity and calificación controls on the descendant also completed successfully.
- Do **not** reopen the former 8-February CI blocker unless a stronger primary source genuinely changes the date-layer finding.

## Governing analytical order — PR #1208 remains controlling

Read `CONCURSO36_UNITARY_CRIMINAL_FIRST_GOVERNANCE.md` before substantive continuation.

PR #1208 hardwired the repository-wide rule that every material Concurso 36/2012 task must run as a **unitary, non-fragmented, criminal-prosecutorial, investigative and forensic analysis first**, **alongside** the complete concursal, civil, mercantile/corporate, administrative/regulatory, tax, property/registry, professional-duty and other relevant legal tracks.

The “dual-lens” dry-law taxonomy delivered by #1207 is a procedural-classification component within that controlling criminal-first methodology. It is **not** a return to a civil-first, insolvency-only or fragmented analysis.

For every material event:

1. reconstruct the document/event family end-to-end;
2. test criminal/prosecutorial/investigative/forensic relevance from the outset;
3. run dry-law and other legal tracks alongside it;
4. reconcile the tracks into one evidentiary account;
5. preserve actor-specific attribution, contrary evidence and alternative explanations; and
6. preserve the distinction between allegation, inference, primary evidence, judicial fact, implementation fact and unresolved gap.

Criminal allegations must not be silently civilised into accounting, fee, community-governance or arithmetic disputes. Equally, allegations, adverse rulings, contradictions, complaints and patterns must not be published as adjudicated criminal offences without the necessary evidentiary and legal basis.

## Primary truth correction — CAM definitive texts

Primary reinspection of the controlled electronic Auto establishes four distinct date layers:

- **8 February 2018** — Auto body / controlling judicial-act date.
- **9 February 2018** — Judge Alberto López Villarrubia electronic signature.
- **14 February 2018** — LAJ Águeda Reyes Almeida electronic signature.
- **15 February 2018** — later filename / notification-custody family layer; it is **not** the date of the Auto on the present primary record.

The primary Auto also expressly accepts that assignment changes **creditor identity, not amount**. It recognises:

- €857,373.81 special privilege — loan 2801;
- €8,194,877.88 special privilege — loan 3000; and
- contingent enforcement costs without an independently quantified amount.

Quantified special privilege comparator: **€9,052,251.69**, plus separately described unquantified contingent costs.

`assets/data/concurso36-what-court-ordered-v2.json` is the corrected controlled layer for this issue. Preserve older v1 material as historical reconstruction/provenance; do not silently rewrite it as though the earlier error never existed.

## Authority before arithmetic

For every purported `Comunidad`, fee, quota, debt, charge, vote, representation, possession, hotel-control, works, exploitation or expenditure issue, establish first:

`actual actor -> exact entity/body -> claimed capacity -> source of authority -> personación/procedural status -> act -> recipient -> procedural effect -> patrimonial effect -> criminal/prosecutorial relevance -> contrary evidence -> gap`.

An unchanged figure does not establish lawful authority, lawful representation, standing, provenance or procedural effect. The 8-February-2018 “not change the amount” point is therefore an **authority/identity/legal-effect gate**, not merely arithmetic.

`NOT LOCATED` must not be converted to `DID NOT EXIST` without the certified denominator required to support that conclusion.

## Procedural taxonomy — do not collapse categories

A materially important procedural act is not automatically an `incidente concursal`.

- **Pieza 7 and Pieza 8** are primary-located incident families and must be separately identified from their exact initiating pleading/caption, parties, object, decision, review/finality and implementation.
- The Community-fee / final-text family is an **Article 97-bis modification comparator**. Do not relabel a located order as an incident without the source-bound incidental route.
- The **4-June-2018 clarification Auto is not itself demonstrated to be an incidente concursal and is not a demonstrated amendment of the texto definitivo** merely because it refers to a different figure.
- Keep liquidation-plan approval/clarification, reposición/apelación/queja/revisión, calificación, ordinary Section filings, AC reports, offer/improvement/adjudication machinery, testimonios and later correction/clarification applications in their actual procedural classes.

## 4 June 2018 — mandatory amount / legal-gateway audit

Preserve the declared Aweswell/Gil position that the 4-June-2018 clarification Auto could not, by itself, lawfully amend the `texto definitivo` and should not be treated as if it increased the admitted CAM credit absent a proven statutory/procedural modification route.

Mandatory comparator:

`8-Feb-2018 definitive-text comparator: €9,052,251.69 + unquantified contingent costs`

vs

`4-Jun-2018 clarification / CAM balance-certificate layer: approximately €13.166m plus the stated secured-interest treatment`

vs

`2022 deed/adjudication layer: €13,168,082.02`.

Audit mortgage-by-mortgage and component-by-component: principal, ordinary/default interest, former LC Article 59, mortgage caps, costs/enforcement costs, the legal gateway for each component, AC treatment, judicial treatment, finality, deed/set-off mechanics, Registry implementation and final accounting. **Numerical continuity is not legal authority.**

## Judge / AC adversarial review — cumulative, actor-specific

Preserve the user’s allegation as a **cumulative multi-act / multi-omission theory**, not a single-act allegation. Existing CGPJ/judicial complaint history is relevant chronology/context, not automatic proof.

For each judge/LAJ/AC node test:

`notice/knowledge -> legal duty or power -> act/omission -> procedural classification -> inconsistency/departure -> beneficiary -> harm -> repetition/pattern -> objective element -> subjective element -> counter-evidence -> remedy/review -> later implementation`.

Hypotheses may include alleged non-neutrality, arbitrariness, prevaricación, institutional shielding/neutralisation and AC breach or enablement, but the repository must continue distinguishing allegation from adjudicated criminal fact.

### AC independent responsibility

Do not make AC responsibility derivative of judicial responsibility. Where actual AC knowledge is established, separately determine what the AC verified, reported, requested, protected, accounted for and included in reports concerning possession/access, security, operation, income/fruits, works/deterioration, third-party assets, funded exits, the masa activa and unidad productiva.

## 7 June 2018 / Arrecife -> Mercantil notice architecture

Do not reduce notice to one missing LexNET receipt.

- **2-May-2018:** Arrecife Juzgado de Instrucción nº2 ordered an `exhorto` to Mercantile Court nº1 concerning Concurso 36/2012 and separately routed the complaint component concerning alleged Mercantile-organ conduct toward the Las Palmas Decanato.
- **7-Jun-2018:** same-day criminal expansion alleges forced access/entry, door/lock interference, lock changes and access control and seeks urgent protection. These remain allegations/evidence, not adjudicated facts.
- **8-Jun-2018:** a communication records direct contact with AC Francisco de Borja Rodríguez-Batllori concerning the new security/CAM presence; this is an independent actual-knowledge lane requiring source-specific treatment.
- **11-Jun-2018:** the later 13-Jun Arrecife Auto establishes that Arrecife received a response from Mercantile Court nº1 to the earlier exhorto. Do not say Mercantil never responded. The actual response and annexes remain a P0 recovery target.
- **13-Jun-2018:** Daniel Irigoyen’s meeting with the Mercantile judge and AC is an additional potential actual-notice channel; exact oral content/documents shown remain to be bound.
- Cuatrecasas correspondence records a question about who would communicate the Arrecife Auto to Mercantil and an answer that it should be communicated and that an escrito had been prepared. A takeover-specific LexNET receipt remains not located.

The exact formal Concurso filing/receipt first notifying the physical 7-Jun event remains open unless and until a controlled source closes it. Non-location is not nonexistence.

## Counsel instruction -> draft -> filing ledger

Maintain actor-specific ledgers for relevant counsel:

`written instruction -> acknowledgement -> advice -> draft -> deadline -> filing receipt -> court treatment -> consequence -> unexplained variance`.

Preserve work actually performed. A located draft without filing receipt is not a filed pleading; absence of the receipt alone does not prove non-filing or motive.

## Convenio -> liquidation

Controlled baseline:

- 27-Apr-2017: LPB formally filed its convenio by LexNET with viability plan/annexes.
- 26-Jun-2017: judge refused to suspend the 28-Jun creditors’ meeting and made the AC evaluation available.
- 28-Jun-2017: official Junta minute/quorum record remains required; contemporaneous client evidence regarding lack of quorum remains corroborative until the official act is controlled.
- 19-Dec-2017: liquidation opened because no proposal had been accepted, **not** because LPB had failed to file a convenio.

Recover the official 28-Jun act and continue the AC/judge treatment audit of the proposal, viability/economic terms and transition into liquidation.

## Continuous lender / workout lane

Maintain the continuous but legally differentiated chain:

`Bankia/BFA -> SAREB -> Promontoria Holding 122 / Cerberus / Haya -> CAM`.

At each transition bind creditor of record, mortgage/credit ownership, servicer and negotiation authority, assignment instruments, standing/personación, settlement/refinancing communications, amount/components/security and what was actually recognised or modified inside Concurso 36/2012. Do not collapse creditor succession, servicing, workout history and admitted-credit status into one concept.

## Art.176 / later TRLC Art.465.6 conclusion route

Reconcile the June-2018 conclusion-route materials under the historically applicable former LC Article 176. Later filenames/renaming using TRLC Article 465.6 cannot retroactively change the statutory numbering applicable in June 2018.

Preserve the user declaration that the June-2018 conclusion route/intention was not further actioned because, in his position, subsequent conduct frustrated it; treat that as a declaration unless independently established. Also continue the later 2021 Article 465.6 instruction/filing-receipt audit.

## Four consequence tracks — never collapse them

Maintain and cross-link, but do not merge:

1. LPB **masa activa**.
2. **Unidad productiva / operating capacity**, including income, bookings, contracts, licences, goodwill and operating capability where holder is identified.
3. **Matkator / third-party extraconcursal harm**.
4. Alleged **overreach of Concurso 36/2012 beyond LPB’s estate**.

A conclusion about LPB estate property does not automatically establish authority over whole-hotel possession, operation, third-party property or income.

## Current authoritative P0 queue

Unless a later merged versioned supplement expressly replaces it, continue from the court-record start file and the current `open_points_replace` queue:

1. Exact signed **LPB AP Auto of 4-Jul-2022 in Queja 375/2022**, plus service/finality.
2. LPB exact **Audiencia Provincial LexNET filing receipt/principal pairing** for Queja 375/2022.
3. **Judge-signed final outcomes** after the 28-Jul-2022 placement of admitted direct revisions before the judge.
4. Complete **21-Feb-2022 deed/testimonio/presentation/Registry bridge finca-by-finca**, including mortgage/credit reconciliation and legal effect while review routes were pending.
5. Exact formal **Concurso 36/2012 filing/receipt first notifying the 7-Jun-2018 physical-control/takeover event**, if one exists, plus response/service/review chain.
6. Underlying **2018 free-finca deed/Registry entry, 12-Dec-2018 DIOR, reposición receipt and final result**.
7. Complete **Feb-Oct-2021 protection/new-document/RICPE** chain through every later filing, response and operative consequence.
8. Actual Concurso 36/2012 **filing/receipt and judicial treatment for ONA/Stoneweg/Varia/Elaia/other funded exits**.
9. Principal document for AC quarterly-report registration **5367/2022** and its consequence.
10. **Certified electronic chronological index / official relation of procedural acts / equivalent per-piece export** for every section/piece.

### P0 emphasis from this thread

Within that queue, prioritise recovery/reconciliation of:

- the Mercantil reply received by Arrecife on 11-Jun-2018 and annexes;
- the exact 7-Jun Arrecife filing receipt/stamp;
- any AC-authored post-7-Jun Mercantile filing/report and response;
- the prepared Cuatrecasas takeover/control escrito and its filed/deferred/unfiled status;
- the full true-incidente denominator, including Pieza 7/Pieza 8 and any final-text modification route;
- the complete Auto table governing definitive-text modification/mention/refusal/limits;
- €9,052,251.69 -> later ~€13m -> €13,168,082.02 reconciliation;
- the official 28-Jun-2017 convenio/Junta act; and
- the certified chronological/per-piece court denominator.

## Mandatory read order for a new thread

1. `CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md`.
2. `CONCURSO36_UNITARY_CRIMINAL_FIRST_GOVERNANCE.md`.
3. `CHATGPT_START_HERE_CONCURSO36_DUAL_LENS_THREAD_HANDOFF_29AUG2026.md` — this corrected post-merge handoff.
4. `assets/data/concurso36-court-record-reconstruction-v1.json`.
5. `assets/data/concurso36-court-record-reconstruction-2022-appellate-supplement.json`.
6. `assets/data/concurso36-court-record-reconstruction-gapclose2-20260829.json`.
7. `assets/data/concurso36-what-court-ordered-v2.json`.
8. `assets/data/concurso36-procedural-taxonomy-judicial-ac-dual-lens-20260829.json`.
9. `archive/PRIMARY_REINSPECTION_8FEB2018_DATE_CORRECTION_29AUG2026.md`.
10. The latest merged continuity/deletion-safety closeout and deployment log.

The living court-record reconstruction previously reached **37 controlled/corroborated nodes**. Do not silently alter that denominator; use versioned supplements and explicit dedupe/reconciliation before a canonical v2.

## Publication / evidence boundaries

- Primary document > filename/prior reconstruction/later derivative.
- Filing proves filing/request/allegation where receipt is controlled; it does not prove the allegation true.
- Signed decision proves what was decided; it does not itself prove corruption, prevaricación, collusion or capture.
- Draft != filed pleading.
- `Response not located` != ignored/nonexistent.
- Actual notice, formal filing, constructive notice and testimonial knowledge are separate evidence classes.
- Registry/AC instruments prove what they record, not automatically the legal correctness of the underlying act.
- Preserve adverse, protective and corrective counterweights.
- No email, court filing, authority contact, witness contact or external accusation is authorised by this handoff alone.
- Some old direct-chat uploads have expired. Continue from Gmail/Drive/repository custody where the same source family is controlled; request re-upload only if a specific P0 depends exclusively on an expired original.

## Recommended short prompt

> **Continue the autonomous Concurso 36/2012 reconstruction from `CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md`, `CONCURSO36_UNITARY_CRIMINAL_FIRST_GOVERNANCE.md` and `CHATGPT_START_HERE_CONCURSO36_DUAL_LENS_THREAD_HANDOFF_29AUG2026.md`. Treat PR #1207 and its 8-Feb-2018 primary-date/dual-lens work as merged and deployed; do not reopen the superseded CI blocker. Continue unitarily and non-fragmentedly with criminal-prosecutorial-investigative-forensic analysis first, alongside the dry-law concursal/civil/mercantile/administrative/regulatory and other tracks. Close the current P0 filing/decision/notification/implementation families end-to-end, preserve the four consequence tracks and all evidence boundaries, update repository and bilingual site through PR/CI/Pages where substantive surfaces change, and leave the project deletion-safe for the next short handoff.**

## Deletion-safety statement

The substantive #1207 publication is merged into `main`; a direct descendant containing it has a successful GitHub Pages deployment. This corrected handoff removes the obsolete “open PR / failing validator” state. Once this corrective closeout itself is merged to `main`, a fresh thread can recover the operative state, primary date correction, governing criminal-first methodology, procedural taxonomy, remaining P0 queue and publication history without relying on the originating chat.

Deletion-safety does **not** mean evidentiary completeness, certified-docket completeness, authenticity certification, adjudication of allegations or independent disaster-recovery certification.
