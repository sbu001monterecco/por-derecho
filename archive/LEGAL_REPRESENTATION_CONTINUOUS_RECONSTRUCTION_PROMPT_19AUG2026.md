# LEGAL REPRESENTATION — CONTINUOUS RECONSTRUCTION PROMPT

**Canonical data target:** `assets/data/legal-representation-v1.json`  
**Human control:** `archive/LEGAL_REPRESENTATION_LEDGER_19AUG2026.md`

Use this prompt for the next reconstruction pass. Do not create a competing lawyer list.

---

## MASTER EXECUTION PROMPT

Reconstruct and maintain the complete legal-representation genealogy for the Sun Park / Aweswell / Luchy Playa Blanca / Matkator / Pink Canary perimeter from **2011 to the present**.

### Operating principle

This is not a directory and not a blame exercise. Reconstruct, for every material professional:

> who represented or advised whom; in which matter; during what verifiable period; what they demonstrably knew, received, prepared, filed or transmitted; which procurador/court channel was involved; who preceded and succeeded them; and what knowledge/file handover can actually be proved.

### Read first

1. `CHATGPT_START_HERE.md`
2. `archive/LEGAL_REPRESENTATION_LEDGER_19AUG2026.md`
3. `assets/data/legal-representation-v1.json`
4. `archive/CONTINUOUS_MAINTENANCE_MATRIX.md`
5. `archive/MISSING_EVIDENCE_REGISTER.md`
6. `archive/CORRECTION_REGISTER.md`
7. applicable unitary-case and publication-control protocols

### Evidence sources

Search connected Gmail and Drive first for private evidential reconstruction. Use repository files for existing public/canonical propositions.

Never copy raw private mailbox IDs, private email addresses, privileged correspondence or sensitive subjective notes into the public repository.

### Search in chronological waves

Run overlapping waves so transitions are not missed:

- 2011–2013: pre-concurso, JO 1241/2011, Bankia enforcement, 5 bis, Garrigues, entry into Concurso 36/2012, procuradores.
- 2013–2017: Juan Tomás Parrilla, incidentes, Community/CEXP, banking, appeals, any parallel advisers.
- 2018–2019: Juan Tomás + Cuatrecasas + Cristo + other specialist/local/criminal advisers; 7 June control event; liquidation; registry/ob-rem; David Espejo reports; Fiscalía.
- January–July 2020: Cuatrecasas exit, Daniel Jiménez entry/exit, Juan Tomás substitution, Luis Miguel López entry, procuradora changes, David Espejo transmissions.
- 2021–2022: Luis Miguel/Cristo, calificación, appeals, Espejo report use/filing chain, UDEF/Fiscalía and related specialist advice.
- 2023–2024: Sixto entry, Audiencia Nacional, calificación judgment/appeal, procuradora/personation chain.
- 2025–present: current Sixto roles, Carlos Llamas, Matkator, criminal/procedural work and any new counsel.

### Search concepts

Use names plus:

`abogado`, `abogada`, `despacho`, `legal`, `asesor`, `venia`, `hoja de encargo`, `honorarios`, `minuta`, `factura`, `representación`, `dirección letrada`, `poder`, `procurador`, `procuradora`, `personación`, `LexNET`, `escrito`, `demanda`, `recurso`, `querella`, `denuncia`, `oposición`, `concurso`, `incidente`, `calificación`, `apelación`, `sustitución`, `renuncia`, `resignation`, `handover`, `expediente`, `nuevo abogado`, `abogado anterior`.

### Engagement test

Do not classify a person as retained counsel solely because they:

- were copied on an email;
- attended one meeting;
- were asked for an introduction;
- received documents;
- gave informal comments.

Prefer, in order:

1. engagement letter / mandate;
2. court or procurador record of representation;
3. venia/substitution evidence;
4. invoice/time record tied to legal work;
5. repeated direct advice/work product demonstrating a mandate;
6. client statement, explicitly labelled as such.

If retention is not proved, classify as `consulted_not_proven_retained` or candidate.

### Client-specific rule

Never write a single generic succession chain when different clients had different lawyers.

In particular, preserve the verified 2020 distinction:

- Cuatrecasas → Daniel Jiménez concerns **Aweswell's** Concurso representation.
- Juan Tomás Parrilla → Luis Miguel López concerns **LPB's** legal direction in Concurso 36/2012.

Treat parallel advisers as parallel bands.

### Date rule

Store separately:

- first verified activity;
- engagement/appointment date if proved;
- substitution/venia request date;
- successor identification date;
- court-recorded direction change;
- last verified activity;
- resignation/termination date if proved.

Do not convert a transition email into a formal court date.

### Work-product rule

For each engagement build:

- documented advice;
- documents/reports received;
- documents created;
- known filings;
- filings discussed but not proved;
- court/procurador communications;
- unresolved tasks;
- knowledge state at end of engagement.

Do not infer “no work” from a short tenure. Measure the work record.

### David Espejo rule

Keep David Espejo as `expert_witness`, not lawyer.

For **each report** and **each legal professional**, determine separately:

1. `REPORT_RECEIVED`
2. `ANALYSIS_USED_OR_DISCLOSED`
3. `TRANSMITTED_TO_PROCURADOR`
4. `FORMALLY_FILED_WITH_COURT`
5. `NO_REPORT_SPECIFIC_FILING_EVIDENCE_LOCATED`
6. `UNKNOWN`

A pleading that adopts an argument does not prove the report was filed. A lawyer's receipt does not prove onward transmission.

### Procurador rule

Build the transmission chain:

`client → lawyer → procurador → court`

Each arrow needs its own evidence. Record changes of procurador independently of changes of lawyer.

### Handover audit

For every change, test:

- venia;
- complete file transfer;
- originals;
- Drive/data access;
- expert reports;
- deadline list;
- pending motions/tasks;
- procedural status summary;
- successor acknowledgement;
- billing/closeout;
- court/procurador direction change.

Status:

- `COMPLETE`
- `PARTIAL`
- `UNCLEAR`
- `DISPUTED`
- `NO_DOCUMENTARY_HANDOVER_LOCATED`

### Public-safety rule

Public repository wording must be neutral and auditable.

Do not publish personal character assessments. Translate them, if relevant, into a question tested against documents: duration, changing positions, completed acts, resignation chronology, handover completeness, fee closeout, etc.

Never say “X did not send/file” unless affirmative evidence establishes it. Prefer “no report-specific filing evidence has yet been located.”

### Update procedure

After each meaningful pass:

1. update existing objects in `assets/data/legal-representation-v1.json`;
2. update the human ledger;
3. add newly found candidates only after classification;
4. add/correct handover events;
5. update open questions;
6. preserve corrections and prior states where a proposition materially changes;
7. do not publish the frontend merely because new backend data exists.

### Front-end publication gate

Only turn on a public page when the backend can support all of these without misleading simplification:

- current principal lawyers;
- all material former principal lawyers/firms;
- separate client tracks;
- major parallel advisers;
- procurador layer;
- major handovers;
- major date gaps visibly qualified;
- Espejo report-transmission status;
- publication-safe sourcing.

When ready, render bilingual ES/EN views from the JSON:

- chronology;
- by matter;
- by professional;
- by firm;
- handover/continuity map;
- expert-report transmission matrix.

### Required result at the end of each run

Report:

1. new professionals found;
2. engagements upgraded/downgraded;
3. dates newly verified;
4. handovers newly verified;
5. Espejo report-chain changes;
6. contradictions/corrections;
7. P0 evidence gaps remaining;
8. repository files changed;
9. whether the frontend publication gate remains closed or can be opened.
