# START HERE — Concurso 36/2012 court-record reconstruction

**Date:** 29 August 2026  
**Purpose:** deletion-safe, new-thread-safe autonomous continuation for court decisions, LAJ acts, LexNET notifications, party filings, appeals/quejas/revision, finality and implementation in Concurso 36/2012.

## One-sentence mission

Reconstruct the complete **located** procedural record of Concurso 36/2012 as closed document families — **filing -> verified receipt -> court/LAJ act -> service -> review/appeal -> finality -> implementation** — and use that record to support the unitary criminal-led forensic/prosecutorial analysis without converting disputed allegations, adverse rulings or missing documents into categorical criminal findings.

## Mandatory read order in a new thread

1. `CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md` — this file.
2. `assets/data/concurso36-court-record-reconstruction-v1.json` — base reconstruction registry.
3. `assets/data/concurso36-court-record-reconstruction-2022-appellate-supplement.json` — first AP/revision supplement.
4. `assets/data/concurso36-court-record-reconstruction-gapclose2-20260829.json` — **current second P0 gap-closure supplement; its `open_points_replace` is the current P0 queue.**
5. `assets/data/concurso36-complete-record-v1.json` — earlier canonical located-corpus catalogue; **not a certified docket**.
6. `assets/data/concurso36-lexnet-supplement-20260829.json` — controlled earlier 2018 LexNET supplement.
7. `assets/data/concurso36-multitrack-judicial-failure-parallel-lives-20260829.json` — filing/response/consequence crosswalk.
8. `archive/CONCURSO36_COURT_RECORD_RECONSTRUCTION_CONTINUITY_29AUG2026.md`, `archive/CONCURSO36_COURT_RECORD_GAPCLOSE2_CONTINUITY_29AUG2026.md` and any later closeout.
9. Bilingual control room: `/es/concurso-36-2012-registro-procesal/` and `/en/insolvency-36-2012-court-record/`.

## Current reconstruction milestone

The control room now combines **37 controlled/corroborated nodes** across the base family plus two versioned supplements. This is a **located reconstruction denominator**, not the certified court docket.

### What the latest pass closed or materially narrowed

#### 2022 testimonios/finality/front-end challenge

- **11-Feb-2022 DIOR** (`A05003250-3558b8e3ae715cbf92cda7771ba1644589600797`; notification LexNET `202210469865861`) records LPB/Aweswell protests and rejects the requested treatment on the basis that the 15-Oct-2021 liquidation-phase reposición Autos were non-appealable; five-day reposición route stated.
- **14-Feb-2022 DIOR** (`A05003250-353fa667a7b4171f8f5b31deaf61644846994419`; notification LexNET `202210470242640`) orders testimonios to CAM of the 18-May-2021, 15-Oct-2021 and 26-Jan-2022 Autos **with expression of finality**.
- **16-Feb-2022 Aweswell reposición** is receipt-controlled: sent `202210470528468`, ack `1202210470528468`, principal SHA-256 `b8db8d9c84e7d4d1abf44c4eb9e2528d8872a7b1dd8fe5cf00c027fa4cab4242`.
- These front-end nodes pair into the already controlled April-2022 LAJ Decretos and subsequent direct-revision route.

#### AP appeal / queja correction

- The exact **29-Mar-2022 Audiencia Provincial LexNET receipt currently controlled belongs to Aweswell**, not LPB: sent `202210481753993`, ack `1202210481753993`; AP destination controlled.
- LPB's **31-page Queja 375/2022 principal is controlled as a document**, but its exact AP LexNET presentation receipt remains open.
- LPB = AP Sección Cuarta **Queja 375/2022**. A later signed AP Auto cross-references a **4-Jul-2022 Auto in 375/2022 in the same adverse legal sense**, but the exact signed 4-Jul Auto and its service/finality remain open.
- Aweswell = AP Sección Cuarta **Queja 379/2022**; Auto 109/2022 of 24-Nov dismisses the queja, and the 30-Nov DIOR records finality/archive.

#### Direct revision after April-2022 LAJ Decretos

- **25-Jul CAM opposition** is LexNET-controlled under `202210511075435`, principal SHA-256 `81e65b9615269c4da8af95989d831c18ce258531747518baacfdd85424d80fc6`.
- **26-Jul DIOR** joins CAM opposition as registration `5306/2022`.
- **28-Jul DIOR** joins AC opposition as registration `5354/2022`, closes opposition and places Aweswell's two revisions **“sobre la mesa de S.S. para resolver.”**
- The subsequent judge-signed decision resolving those revisions remains an exact P0.
- Preserve **Auto 308/2022 of 13-Jul-2022** as a corrective counterweight: it annulled a mistaken deposit-based inadmission after verifying deposits had been made in time.

#### 2022 adjudication -> deed -> court notice -> Registry

The implementation bridge is now primary-controlled for a representative LPB finca, while the finca-by-finca denominator remains open:

- **25-Apr-2022 AC quarterly report** states that the 18-May-2021 adjudication Auto was treated as final and that by public deed dated **21-Feb-2022**, notary José del Cerro Peñalver, protocol **457**, the AC transferred the covered apartments/locales/pools/solaria to Construcciones Acosta Matos, S.A.; it distinguishes apartment dation from the €400,000 direct-sale mechanics for locales/pools.
- **2-May-2022 court notification / DIOR** puts that report into the procedural channel under LexNET `202210489569008`.
- **6-May-2022 Tías Registry nota simple, finca 8751**, CSV `235019286750B8FD`, records CAM S.A. as 100% full-domain owner by **DACIÓN EN PAGO**, deed dated 21-Feb-2022, protocol 457, inscription 21ª; presentation entry Diario 61/11 also dates from 21-Feb-2022. The same note still displays the mortgage/credit chain in the cargas section, including the 2017 assignment to CAM.
- This closes a representative implementation bridge, **not** the finca-by-finca title/encumbrance/accounting denominator. Obtain the complete deed, testimonios, Registry presentations/certifications and reconcile surviving mortgage/credit entries.

#### June 2018 appeal/suspension vs 7-Jun physical-control notice

- **19-Jun-2018 LPB appeal** is LexNET-controlled: sent `201810216187332`, ack `1201810216187332`.
- The full controlled principal is an interest/privilege/liquidation-plan appeal with suspension request. It contains **no located takeover/access/locks/keys/security allegation**. Do **not** use it as proof that the Mercantile Court was formally notified of the 7-Jun physical-control event.
- **26-Jun-2018 judge-signed Auto** is a genuine protective counterweight: it suspends realisation of the listed Tías fincas because the appeal could materially alter the dation conditions, while allowing other masa-activa liquidation to continue.
- That Auto protects the **realisation process**; it does not establish authority over whole-hotel possession, locks, security, operation, income or third-party property.
- The exact formal Concurso filing/receipt first notifying the physical 7-Jun event remains P0. Non-location is not nonexistence.

#### 2021 works/access/masa and RICPE/new documents

- **24-Feb-2021 judge-signed Auto** (`A05003250-354b4c6e25db6943f7e4d268be71614172280325`) expressly records allegations concerning blocked access/security, works/demolition, perceived condition/value, judicial inspection/pericial requests and a prohibition on further intervention; it records AC/CAM responses and **denies the requested protective measures** while noting that later responsibility proceedings could be the appropriate route. This is an **adverse judicial response**, not silence.
- **25-Feb-2021 LPB nullity admission** (`A05003250-35e51f31cf17cb7fa7e9aa383211614278409930`) and **Auto 356/2021 of 6-May** (`A05003250-354d12c678b2d525c7993f07b491620305800646`) are a separate **mortgage/default-interest nullity lane**. Do not conflate them with the 24-Feb works/access/masa family.
- **8-Jul-2021 DIOR** formally transfers new documentary material (reg. `4725/2021`) to parties for submissions.
- A separate **8-Jul Providencia** requires the AC to report on liquidation/conclusion status.
- **21-Jul CAM response** is LexNET-controlled under `202110427187708`, principal SHA-256 `fa790da25b3059671458564751003635714b9c4e14cf0c50e69921bd3bcacf6d`, and includes the RICPE certification material.
- The **29-Jul-2021 Aweswell RICPE paper is not a verified 2021 court filing**. A March-2022 mailbox record expressly describes it as a prior-year draft that had not yet been put into court. Keep it `UNFILED_DRAFT` unless a later actual receipt is found.

#### Funded exits

Focused Gmail/LexNET searches in this pass did **not** locate an identifiable Concurso 36/2012 LexNET receipt for an ONA/Stoneweg/Varia/Elaia funded-exit offer. Drafts, transaction correspondence and filings in another proceeding are insufficient. Keep each rescue route classified as draft/sent/filed/received/ruled/lapsed/superseded only when the matching source proves that state.

#### 2018 Registry implementation checkpoint

Cuatrecasas correspondence to the Tías Registry dated 28-Dec-2018 states counsel had learned that a deed concerning LPB free fincas 8508–8536, 8653 and 8654 had entered the Registry in Nov-2018; counsel refers to a later 12-Dec-2018 DIOR authorising sale and a reposición/cancellation/refusal route. Treat this as an **implementation checkpoint only** until the underlying deed, Registry entry, 12-Dec DIOR and LexNET receipts are controlled.

#### New orphan

- `C36-ORPHAN-20220727-AC-REPORT-5367`: a DIOR references AC quarterly-report registration `5367/2022`, but the principal report itself was not present in the controlled forwarding package located in this pass.

## Current P0 queue — authoritative

1. Exact signed **LPB AP Auto of 4-Jul-2022 in Queja 375/2022**, plus service/finality.
2. LPB's exact **Audiencia Provincial LexNET filing receipt/principal pairing** for Queja 375/2022.
3. **Judge-signed final outcomes** after the 28-Jul-2022 placement of admitted direct revisions before the judge.
4. Complete **21-Feb-2022 deed/testimonio/presentation/Registry bridge finca-by-finca**, including reconciliation of mortgage/credit entries and legal effect while review routes were pending.
5. Exact formal **Concurso 36/2012 filing/receipt first notifying the 7-Jun-2018 physical-control/takeover event**, if one exists, plus response/service/review chain.
6. Underlying **2018 free-finca deed/Registry entry, 12-Dec-2018 DIOR, reposición receipt and final result**.
7. Complete **Feb-Oct-2021 protection/new-document/RICPE** chain through every later filing, response and operative consequence; keep the 29-Jul draft unfiled unless later receipt is found.
8. Actual Concurso 36/2012 **filing/receipt and judicial treatment for ONA/Stoneweg/Varia/Elaia/other funded exits**.
9. Principal document for AC quarterly-report registration **5367/2022** and its consequence.
10. **Certified electronic chronological index / official relation of procedural acts / equivalent per-piece export** for every section/piece. Non-production is not nonexistence.

## Autonomous operating rules

### Search / ingestion

- Use connected Gmail for original LexNET/lawyer-notification families where repository custody is incomplete; use Drive/repository where they hold the stronger original.
- Search **month-by-month to pagination exhaustion**, not only one-off keywords.
- Search separately for `Escrito Enviado Lexnet`, `Escrito Recibido Lexnet`, `Mensaje LexNET - Notificación`, `AUTO`, `DECRETO`, `PROVIDENCIA`, `DILIGENCIA DE ORDENACIÓN`, `DIOR`, `TESTIMONIO`, `REPOSICIÓN`, `APELACIÓN`, `QUEJA`, `REVISIÓN`, `NULIDAD`, plus `36/2012` and known procurator/notifier senders.
- Forwarded email = custody/provenance, **not another procedural act**.
- Dedupe by LexNET ID, sent/ack ID, electronic-document ID, hash, date, party, section/piece and operative effect; never filename alone.
- Preserve same-date distinct signed decisions as distinct records.
- A later signed judicial decision may establish existence/date/docket/direction of an earlier missing decision, but label this `cross-reference`; do not invent exact wording.

### Pairing rule

For every material family:

`family_id -> party filing -> verified receipt -> annexes -> court/LAJ response -> service -> challenge -> appeal/queja/revision -> finality -> implementation -> explicit remaining gap`.

Never call a family complete merely because a filing or decision exists.

### Judicial-treatment taxonomy

1. `ADVERSE_SUBSTANTIVE_RESPONSE`
2. `PROTECTIVE_RESPONSE`
3. `PROCEDURAL_ONLY_DISPOSITION`
4. `PARTIAL_RESPONSE`
5. `RESPONSE_NOT_LOCATED`
6. `CONTRADICTORY_OPERATIVE_STATE`
7. `IMPLEMENTATION_OR_ACCOUNTING_CHAIN_OPEN`

`RESPONSE_NOT_LOCATED` is never automatically “ignored”. An adverse decision is never automatically criminal judicial misconduct.

### Four consequence tracks

Keep these analytically separate at all times:

1. LPB **masa activa**.
2. **Unidad productiva / operating capacity**, including bookings, revenue, contracts, licences, goodwill and operating capability where the holder is identified.
3. **Matkator / third-party extraconcursal harm**.
4. Alleged **overreach of Concurso 36/2012 beyond LPB's estate**.

### Evidence boundaries

- Filing = proof of filing/request/allegation and, if controlled, receipt; not proof the allegation is true.
- Signed decision = proof of what was decided; not itself proof of corruption, prevaricación, collusion, malicious prosecution or capture.
- The two 15-Oct-2021 Autos contain a verified textual contradiction; criminal significance remains a separate test.
- Institutional neutralisation/shielding is first an **effect test**; criminal attribution requires actor-specific duty, knowledge, intent/purpose, causal effect, beneficiary/harm and contrary-evidence analysis.
- LPB estate, Matkator and other third-party rights remain separate. Concurso 36/2012 is not universal title to the whole hotel.
- Registry notes and AC reports prove what those instruments record; they do not automatically establish the legal correctness of the underlying implementation.

### Publication governance

- Branch -> PR -> dedicated CI validator -> merge -> `main` readback -> Pages deployment verification -> publication-manifest state closeout.
- Repair integrity/governance failures; never bypass them.
- Do not overwrite `concurso36-complete-record-v1.json`. Use versioned supplements until cross-supplement dedupe supports canonical v2.
- Public pages may show procedural metadata, operative summaries, IDs and fingerprints after privacy review; do not publish unnecessary private strategy communications/personal data.
- Preserve adverse, protective and corrective counterweights.
- No email, court filing, authority contact or outreach is authorised merely by this continuity file.

## Canonical v2 definition of done

Do **not** publish `concurso36-complete-record-v2.json` until supplements are deduped; unique filing/decision/notification counts exist; material filings have response/orphan links; material decisions have service/challenge/finality links; title/credit/possession/testimonio acts have implementation links/gaps; and reconstructed corpus vs certified docket remains explicit.

## Expired ChatGPT uploads

Some old direct-chat uploads have expired. **Do not block reconstruction** where Gmail/repository custody supplies the family. Ask for re-upload only when a specific expired original is itself needed for a proof/provenance comparison.

## Recommended short prompt for a new thread

> **Continue the autonomous Concurso 36/2012 court-record reconstruction from `CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md`. Close the remaining P0 filing/decision/notification/implementation families end-to-end, update the repository and bilingual site through PR/CI/Pages, preserve the four consequence tracks and all evidence boundaries, and leave the project deletion-safe and ready for the next short handoff.**

A new thread must recover state from this repository file and the current supplements rather than depend on the originating chat.