# START HERE — Concurso 36/2012 court-record reconstruction

**Date:** 29 August 2026  
**Purpose:** deletion-safe, new-thread-safe autonomous continuation for court decisions, LAJ acts, LexNET notifications, party filings, appeals/quejas/revision, finality and implementation in Concurso 36/2012.

## One-sentence mission

Reconstruct the complete **located** procedural record of Concurso 36/2012 as closed document families — **filing -> verified receipt -> court/LAJ act -> service -> review/appeal -> finality -> implementation** — and use that record to support the unitary criminal-led forensic/prosecutorial analysis without converting disputed allegations, adverse rulings or missing documents into categorical criminal findings.

## Mandatory read order in a new thread

1. `CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md` — this file.
2. `assets/data/concurso36-court-record-reconstruction-v1.json` — base reconstruction registry.
3. `assets/data/concurso36-court-record-reconstruction-2022-appellate-supplement.json` — current AP/revision closure supplement; its `open_points_replace` supersedes stale 2022 open-point wording in the base registry.
4. `assets/data/concurso36-complete-record-v1.json` — earlier canonical located-corpus catalogue; **not a certified docket**.
5. `assets/data/concurso36-lexnet-supplement-20260829.json` — controlled 2018 LexNET supplement.
6. `assets/data/concurso36-multitrack-judicial-failure-parallel-lives-20260829.json` — filing/response/consequence crosswalk.
7. `archive/CONCURSO36_COURT_RECORD_RECONSTRUCTION_CONTINUITY_29AUG2026.md` and the later AP/revision closeout if present.
8. Bilingual control room: `/es/concurso-36-2012-registro-procesal/` and `/en/insolvency-36-2012-court-record/`.

## Current reconstruction milestone — 2022 family

The control room now combines **20 base + supplemental verified/corroborated procedural nodes** around the 15-Oct-2021 / 26-Jan-2022 decisions, testimonios/finality, appeals, quejas and direct revisions.

### Appeal and queja chain

- **28-Feb-2022 LPB appeal**: LexNET `202210473582179`; later registration `1477/2022`.
- **2-Mar-2022 Aweswell appeal**: sent `202210474270428`, ack `1202210474270428`; later registration `1512/2022`.
- **9-Mar-2022 Auto**: judge-signed inadmission of both appeals; ten-day queja route; document `A05003250-3507d04a1d026d8373981d6add31646823908885`; notified under LexNET `202210476786626`.
- **29-Mar-2022 Aweswell queja**: sent `202210481753993`, ack `1202210481753993`.
- **30-Mar notice to Mercantile Court**: sent `202210482293471`, ack `1202210482293471`.
- **4-Apr-2022 DIOR**: records both parties' queja notices as registrations `2275` and `2314/2022`.
- **LPB = AP Seccion Cuarta, Queja 375/2022**. Signed 18-Apr providencia set study/vote/decision. A later signed AP Auto identifies a **4-Jul-2022 Auto in 375/2022 in the same adverse legal sense**, but the signed 4-Jul LPB Auto itself is not yet controlled.
- **Aweswell = AP Seccion Cuarta, Queja 379/2022**. 11-Apr DIOR required EUR30 deposit cure; 20-Apr DIOR confirmed cure and deliberation-ready status.
- **24-Nov-2022 AP Auto 109/2022, Queja 379/2022**: dismisses Aweswell's queja, costs + loss of deposit, no further appeal; document `A05003250-35d4ff0c0b259734c5ea7dc69411669385141492`.
- **30-Nov-2022 AP DIOR**: records finality, sends testimony back to originating court and archives 379/2022; document `A05003250-3587babc6df3d2dbfc90404de381669892710841`.

**Interpretation boundary:** these AP Autos close the asserted appeal/queja route. They do **not** adjudicate the factual merits of every underlying 2019–2021 protection, access, masa, suspension, bid/adjudication or title allegation listed in the quejas.

### Direct revision against April 2022 LAJ Decretos

- **24-May-2022 DIOR** records four revision applications against the two April Decretos: LPB `3353/3354`; Aweswell `3361/3362`; requires deposit cure. Document `A05003250-35e99a49b9442d46e69baf90bea1653397333765`.
- **2-Jun-2022 DIOR** admits LPB revisions after deposit evidence and gives parties five days to oppose. Document `A05003250-35aa1421b22bb018d3d16aa1bee1654173342082`.
- A **16-Jun-2022 providencia** then inadmitted revision applications for supposed deposit failure.
- **13-Jul-2022 Auto 308/2022** corrects that state after verifying the deposits had actually been made in form and time; it annuls the 16-Jun providencia. Document `A05003250-35188b05fa34b49034efd3977fe1657718796252`.
- **14-Jul-2022 DIOR** admits Aweswell's revisions and gives parties five days to oppose. Document `A05003250-3520a62213f4ca3ac1e1ed1cecb1657801330688`.
- CAM and AC opposition/impugnation material is located in late July; final judge outcomes of these revisions remain to be paired.

**Counterweight rule:** Auto 308/2022 is a documented corrective judicial act. Keep it visible. Do not force every node into a one-direction judicial-failure theory.

## Current highest-value 2022 gaps

1. Recover the exact signed **4-Jul-2022 AP Auto in LPB Queja 375/2022**, plus service/finality. Until then, use only the later AP 109/2022 cross-reference for its adverse legal direction.
2. Recover LPB's exact **AP LexNET presentation receipt/principal queja**; its AP docket/outcome are corroborated, but the exact filing receipt is not yet controlled.
3. Control the exact **11-Feb and 14-Feb 2022 DIORs and every testimonio** issued under them: addressee, purpose, finality wording and service/delivery.
4. Close the **final judge outcomes of LPB/Aweswell direct revisions** admitted 2-Jun/14-Jul, including CAM/AC oppositions and any later review/finality.
5. Reconcile the revision DIORs' repeated references to Decretos dated **22-Apr-2022** against signed Decretos controlled as **26-Apr-2022**; preserve the discrepancy until source reconciliation.
6. Bind testimonios/finality/revision/queja to **deed -> presentation -> Registry** finca-by-finca, including what implementation occurred while review routes were pending and its legal effect.

## Autonomous operating rules

### Search / ingestion

- Use connected Gmail for original LexNET/lawyer-notification families where repository custody is incomplete.
- Search **month-by-month to pagination exhaustion**, not only one-off keywords.
- Search separately for `Escrito Enviado Lexnet`, `Escrito Recibido Lexnet`, `Mensaje LexNET - Notificación`, `AUTO`, `DECRETO`, `PROVIDENCIA`, `DILIGENCIA DE ORDENACIÓN`, `DIOR`, `TESTIMONIO`, `REPOSICIÓN`, `APELACIÓN`, `QUEJA`, `REVISIÓN`, `NULIDAD`, plus `36/2012` and known procurator/notifier senders.
- Forwarded email = custody/provenance, **not another procedural act**.
- Dedupe by LexNET ID, sent/ack ID, electronic-document ID and hash; never filename alone.
- Preserve same-date distinct signed decisions as distinct records.
- A later signed judicial decision may establish existence/date/docket/direction of an earlier missing decision, but label this `cross-reference`; do not invent its exact operative wording.

### Pairing rule

For every material family:

`family_id -> party filing -> verified receipt -> annexes -> court/LAJ response -> service -> challenge -> appeal/queja/revision -> finality -> implementation -> explicit remaining gap`.

Never call a family complete because a decision exists; test challenge, finality and implementation.

### Judicial-treatment taxonomy

1. `ADVERSE_SUBSTANTIVE_RESPONSE`
2. `PROTECTIVE_RESPONSE`
3. `PROCEDURAL_ONLY_DISPOSITION`
4. `PARTIAL_RESPONSE`
5. `RESPONSE_NOT_LOCATED`
6. `CONTRADICTORY_OPERATIVE_STATE`
7. `IMPLEMENTATION_OR_ACCOUNTING_CHAIN_OPEN`

`RESPONSE_NOT_LOCATED` is never automatically “ignored”. An adverse decision is never automatically criminal judicial misconduct.

### Evidence boundaries

- Filing = proof of filing/request/allegation and, if controlled, receipt; not proof the allegation is true.
- Signed decision = proof of what was decided; not itself proof of corruption, prevaricación, collusion, malicious prosecution or capture.
- The two 15-Oct-2021 Autos contain a verified textual contradiction; criminal significance remains a separate test.
- Institutional neutralisation/shielding is first an **effect test**; criminal attribution requires actor-specific duty, knowledge, intent/purpose, causal effect, beneficiary/harm and contrary-evidence analysis.
- LPB estate, Matkator and other third-party rights remain separate. Concurso 36/2012 is not universal title to the whole hotel.

### Publication governance

- Branch -> PR -> dedicated CI validator -> merge -> `main` readback -> Pages deployment verification.
- Do not overwrite `concurso36-complete-record-v1.json`. Use versioned supplements until cross-supplement dedupe supports canonical v2.
- Public pages may show procedural metadata, operative summaries, IDs and fingerprints after privacy review; do not publish unnecessary private strategy communications/personal data.
- Preserve adverse, protective and corrective counterweights.
- No email, filing, authority contact or outreach is authorised merely by this continuity file.

## P0 autonomous queue

1. **2022 testimonios/revision/implementation** — signed LPB 4-Jul AP Auto; LPB AP receipt; exact 11/14-Feb DIOR/testimonios; direct-revision outcomes; deed/Registry bridge.
2. **7-Jun-2018 physical-control court-notice** — exact Concurso filing/receipt, if any, reporting locks/access/security/possession/operation; pair with court/LAJ response and 26-Jun protective order.
3. **Feb-Oct-2021 protection/nullity/bid/RICPE** — 24-Feb protection family, nullity/reposicion, improved bid, July RICPE production, 15-Oct Autos, 26-Jan clarification.
4. **Funded exits 2017-2018** — classify ONA, Stoneweg/Varia, Elaia, Ben Oldman and others as draft/sent/filed/received/ruled/lapsed/superseded.
5. **Certified denominator** — signed electronic chronological index / official relation / equivalent certified per-piece export and three-way reconciliation against LexNET registry and public repository.

## Canonical v2 definition of done

Do **not** publish `concurso36-complete-record-v2.json` until supplements are deduped; unique filing/decision/notification counts exist; material filings have response/orphan links; material decisions have service/challenge/finality links; title/credit/possession/testimonio acts have implementation links/gaps; and reconstructed corpus vs certified docket remains explicit.

## Expired ChatGPT uploads

Some old direct-chat uploads have expired. **Do not block reconstruction** where Gmail/repository custody supplies the family. Ask for re-upload only when a specific expired original is itself needed for a proof/provenance comparison.

## Recommended short prompt for a new thread

> **Continue the autonomous Concurso 36/2012 court-record reconstruction from `CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md`. Close the next P0 filing/decision/notification families end-to-end, update the repository and bilingual site through PR/CI/Pages, preserve all evidence boundaries and continuity governance, and leave the project deletion-safe and ready for the next short handoff.**

A new thread should recover state from the repository rather than depend on the originating chat.