# LEGAL REPRESENTATION LEDGER — SUN PARK / AWESWELL / LPB / MATKATOR

**Control date:** 19 August 2026  
**Status:** PUBLIC-SAFE BACKEND SEED — NOT A COMPLETE REPRESENTATION HISTORY  
**Machine-readable source:** `assets/data/legal-representation-v1.json`

## 1. Purpose

This ledger reconstructs who acted as lawyer, law firm, procurador, specialist adviser or expert witness for the relevant people and entities, when they acted, for which client and matter, what can be documented about the work performed, and how knowledge/files moved at changes of representation.

It is deliberately **not** a retrospective blame list. The governing questions are:

1. Who represented or advised whom?
2. In which matter and during what verified date window?
3. What did the professional demonstrably receive, prepare, file or transmit?
4. Who preceded and succeeded that professional for that specific client/matter?
5. What knowledge and pending tasks were transferred at the handover?
6. Where does the present documentary chain stop?

A lawyer's presence in a copied email is not enough to establish an engagement. A pleading being filed is not enough to prove that every report discussed by the lawyer was annexed. “No evidence located” is not the same as “did not happen.”

## 2. Architecture decision

The representation history is **multi-track**, not linear.

The same period can contain, for example:

- LPB's counsel of record in Concurso 36/2012;
- Aweswell's separate counsel in the same insolvency;
- separate criminal or property advisers;
- a procurador serving the filing channel;
- an expert witness supplying reports;
- a large firm with several lawyers doing distinct work.

The canonical objects are therefore:

`person → firm → engagement → client → matter → event → evidence-state → handover`

The public website should later read structured data from `assets/data/legal-representation-v1.json`; it should not hard-code a simplified succession narrative.

## 3. Current principal representation

### Sixto Abogados — Javier Sixto / Estefanía Sixto-Seijas

- **Current status:** current principal advisers, confirmed by the client.
- **First activity verified in this reconstruction:** July 2023.
- **Documented tracks:** review of Concurso hearing material; 2023 Audiencia Nacional complaint work; appellate/personation and Concurso document work.
- **Open:** original engagement date; exact client-by-client and Javier/Estefanía division of responsibility.

### Carlos Llamas Sanz

- **Current status:** current principal adviser, confirmed by the client.
- **First activity verified in the present scan:** May 2026; the relationship may predate the first cluster located.
- **Documented tracks:** Matkator / ETJ 163/2020; DP 748/2026 and related procedural work; filings coordinated with procuradora Adriana Hernández Díaz.
- **Open:** true engagement start and complete current mandate map.

## 4. Verified historical chronology

### Garrigues — pre-concurso / early 2012

The current scan materially moves the starting point backwards. Garrigues was already acting before Concurso 36/2012.

Verified activity includes:

- JO 1241/2011 (LPB v Comunidad de Propietarios) by 28 March 2012;
- LPB Article 5 bis / pre-insolvency work in April 2012;
- Bankia enforcement and scheduled-auction strategy in May 2012;
- preparation for LPB insolvency and financing/security work through early June 2012.

Core names located include Miguel Méndez Itarte, José María Martínez de Artola, Víctor de la Torre and Zulay Carmen Rodríguez. Further team members appear in the correspondence and remain to be individually scoped.

**Important gap:** no 2011 engagement evidence has yet been located in the current scan. The case number JO 1241/2011 does not itself prove the date Garrigues was first retained.

### Juan Tomás Parrilla — LPB / Concurso 36/2012

- Verified acting for LPB by June 2012.
- Long-running role in Concurso 36/2012.
- Worked concurrently with Cuatrecasas and other advisers in 2018 rather than being replaced at that point.
- In late 2018 he and Cuatrecasas jointly addressed liquidation/registry/ob-rem questions.
- Formal substitution/venia process is evidenced at 31 May 2020.

This track must remain attached to **LPB**, not automatically to Aweswell.

### Cuatrecasas — Aweswell / multi-lawyer firm track

Verified activity in the present reconstruction runs from at least September 2018 to 26 May 2020.

Materially involved names located:

- Rosa Gual Tomás;
- Iñigo de Luisa Maíz;
- Fedra Valencia;
- Adriana González García;
- Pamela Usta Yabrudy.

The present evidence shows coordinated work on debt-certification, liquidation, appeal and registry questions. In December 2018 Rosa Gual coordinated an urgent registry workstream while Juan Tomás Parrilla was simultaneously acting in LPB's insolvency track.

On **26 May 2020**, the correspondence documents Cuatrecasas granting venia for **Aweswell's representation in Concurso 36/2012** to Daniel Jiménez.

This is a separate handover from the LPB change described below.

### Cristo Ayose Suárez Pimentel — parallel multi-matter track

Verified from at least August 2018.

The evidence presently supports a broad local/cross-matter role covering legal strategy, evidential reconstruction, criminal workstreams, procedural summaries and coordination with other lawyers. He worked in parallel with Juan Tomás Parrilla and Cuatrecasas and later with other counsel.

Cristo also had a direct role in the David Espejo expert-report workstream.

His engagement should therefore not be rendered on the website as simply “the lawyer before/after X.” It is a parallel multi-matter band whose exact client-specific mandates require further reconstruction.

### Daniel Jiménez García — Aweswell / short 2020 engagement

The evidence supports three separate phases:

1. **Pre-takeover review:** by 5 April 2020 Daniel had received multiple David Espejo report/economic-note materials.
2. **Formal Aweswell takeover:** Cuatrecasas venia on 26 May 2020; direct lawyer–expert coordination with David Espejo is also documented.
3. **End of engagement:** a resignation/fee-closeout communication dated 23 June 2020.

The documentary record therefore supports describing this as a **short engagement with documented review, coordination and legal activity**. It does not support converting a private personal assessment into a public characterization.

A complete task/output/filing audit remains open.

### Luis Miguel López Gómez — LPB / Concurso 36/2012

The evidence corrects a potentially misleading single-chain narrative.

Daniel Jiménez did **not simply replace Juan Tomás for every relevant client and then hand the same representation to Luis Miguel**.

Instead:

- Daniel took over **Aweswell's** Concurso representation from Cuatrecasas.
- At the same time, Juan Tomás's **LPB** role was being replaced.
- On 1 June 2020 Daniel contemporaneously identified Luis Miguel López as the new lawyer of the debtor LPB.
- The court record reflected LPB's change of legal direction on 16 June 2020.

Luis Miguel continued in LPB/Concurso and appeal-related work through at least 2022.

### Sixto Abogados — 2023 onward

See current representation above. The backend intentionally preserves Javier and Estefanía as separate professionals under the same firm.

### Carlos Llamas Sanz — current

See current representation above. His earlier relationship history remains an open date-reconstruction task.

## 5. Handover map already established

| Handover | Client | Matter | Status |
|---|---|---|---|
| Cuatrecasas → Daniel Jiménez | Aweswell | Concurso 36/2012 | VERIFIED — venia 26 May 2020 |
| Juan Tomás Parrilla → Luis Miguel López | LPB | Concurso 36/2012 | VERIFIED — substitution 31 May/1 June; court direction change 16 June 2020 |
| Daniel Jiménez → successor | Aweswell | Concurso 36/2012 | OPEN — resignation/fee closeout 23 June 2020; complete successor/file-transfer chain still to reconstruct |

Every future handover must be scored separately for:

- venia;
- client;
- matter;
- procurador;
- court change;
- file inventory;
- expert reports;
- pending deadlines/tasks;
- successor acknowledgement.

## 6. David Espejo — expert witness cross-layer

David Espejo is not part of the lawyer succession tree. He is a separate **expert / expert-witness** object linked to lawyers by evidence-transfer events.

The data model keeps these states separate:

1. report received by lawyer;
2. analysis used or discussed;
3. report transmitted to procurador;
4. report formally filed with court;
5. no filing evidence located;
6. unknown.

Current controlled findings include:

- Cristo Suárez Pimentel: verified involvement in Espejo's expert-workstream from 2018.
- Daniel Jiménez: verified receipt of multiple Espejo materials on 5 April 2020, direct coordination on 26 May, and swap-analysis material on 30 May.
- Luis Miguel López: verified receipt of the debt-reasonableness report on 4 February 2021; later pleading filing activity is documented, but that does **not** yet prove the report itself was annexed.
- Cuatrecasas / Rosa Gual: contemporaneous parallel workstream established; direct receipt of Espejo reports not yet located in the present scan.
- Juan Tomás Parrilla: contemporaneous parallel workstream established; direct receipt of Espejo reports not yet located in the present scan.

The same report-specific audit must later be extended to the relevant procuradores and the court file.

## 7. Procurador layer

The backend treats procuradores separately from lawyers.

Current seed contains:

- Tania — Aweswell procuradora in the 2020 Daniel Jiménez transition; full identity and filing inventory to verify.
- Mónica Padrón — appellate/personation work with Sixto in 2023; exact scope and Espejo-report filing chain to verify.
- Adriana Hernández Díaz — 2026 filings linked to Carlos Llamas; complete client-by-client appointment inventory to reconstruct.

The intended transmission model is:

`client → lawyer → procurador → court`

but the evidence must prove each arrow.

## 8. Additional advisers already surfaced

The first scan has identified further professionals who should be classified rather than silently omitted:

- Manuel Gallego Águeda — 2012 legal/Bankia-related advice; retention scope to verify.
- Daniel Irigoyen — 2018 strategic legal activity; retention scope to verify.
- Juan Daniel Fajardo Expósito — 2018 local/notarial/evidential activity; retention scope to verify.
- Armando L. Betancor — late-2018 specialist legal contact; retention scope to verify.
- Henry Feltenstein Arechabala — consulted in 2018 on white-collar/criminal material; retention not yet proved.

These appear in `candidateAdvisersToClassify` until the evidence satisfies the engagement test.

## 9. Front-end contract

Do **not** yet create a public page that implies the genealogy is complete.

When the backend reaches publication threshold, the website should provide:

1. **Chronology by client and matter** — parallel bands, 2011→present.
2. **Professional profile** — lawyer/procurador/expert, firm, verified period, clients, matters, documented acts.
3. **Firm profile** — especially for multi-lawyer firms such as Garrigues, Cuatrecasas and Sixto.
4. **Matter view** — e.g. “who represented LPB in Concurso 36/2012 at each point?”
5. **Handover/continuity map** — where knowledge passed cleanly, partially or remains unverified.
6. **Expert-report transmission matrix** — report → lawyer → procurador → court.

Public fields may include names, firms, roles, verified date windows, matters, documented activities, handovers, qualifications and open questions.

Do not expose mailbox IDs, private email addresses, privileged correspondence, private subjective assessments or raw personal notes.

## 10. P0 next evidence

1. Identify the 2011 legal/procurador layer before the first currently verified Garrigues activity.
2. Obtain/locate all engagement letters, venias and court direction-change notices for Concurso 36/2012.
3. Complete the David Espejo report-by-report transmission matrix.
4. Reconstruct Daniel Jiménez's successor/file handover after 23 June 2020.
5. Determine exact start/end and individual mandates for Garrigues, Cuatrecasas, Sixto and Carlos Llamas.
6. Reconstruct procurador appointments and filing inventories.
7. For each outgoing lawyer, record `knowledge_state_at_end_of_engagement`.

## 11. Continuity rule

This ledger and `assets/data/legal-representation-v1.json` are the canonical starting point for this track. Future work should update them rather than create competing lawyer lists.

The historical narrative may change as earlier or better evidence is recovered. Corrections must preserve the previous proposition/status and explain why it changed.
