# VISTA DE CALIFICACIÓN — CONCURSO 36/2012 — THREE-VIDEO MASTER INDEX

**Date created:** 17 August 2026  
**Hearing date:** 25 July 2023  
**Court:** Juzgado de lo Mercantil nº 1 de Las Palmas de Gran Canaria  
**Proceeding:** Concurso ordinario 36/2012 — Sección de Calificación  
**Canonical evidential object:** **Vista de Calificación — Concurso 36/2012**  
**Component rule:** VIDEO_01 + VIDEO_02 + VIDEO_03 are one continuous hearing record split only for technical recording purposes. Never interpret any component as a self-contained hearing.

## 0. OE-CAL-002 status control

The hearing audiovisual is no longer wholly missing. **VIDEO_01 of the continuous three-component Vista has been supplied, fingerprinted and structurally indexed; VIDEO_02/03 are being processed separately.** The complete stitched audiovisual set, verified speaker-attributed transcript, official minute, attendance/service/representation history and evidential rulings remain unresolved. Do not revert to the older shorthand that no hearing audiovisual has been recovered.

## 1. Components

| Component | Exact filename | Current ingest state | Native hash | Duration | Continuity rule |
|---|---|---|---|---:|---|
| VIDEO_01 | `J. Mercantil 1 (Palmas de Gran Canaria (Las))_0000036_2012_VIDEO_01.mkv` | LOCATED / fingerprinted / structurally indexed; verified speech transcript pending | SHA-256 `63a08742ae6925cb347fe25ceb2c6a78e0625a4aa7ec1df71b6b8602f4eb7d4f` | 3600.614 s | Opening component only. Meaning may depend on VIDEO_02/03. |
| VIDEO_02 | `J. Mercantil 1 (Palmas de Gran Canaria (Las))_0000036_2012_VIDEO_02.mkv` | being processed in separate ChatGPT thread | pending cross-thread ingest | pending | Must append to this same canonical object. |
| VIDEO_03 | `J. Mercantil 1 (Palmas de Gran Canaria (Las))_0000036_2012_VIDEO_03.mkv` | being processed in separate ChatGPT thread | pending cross-thread ingest | pending | Must append to this same canonical object. |

No source video may be modified. Any transcript, audio extraction, still, clip or other derivative must identify the component and exact local timestamp.

## 2. VIDEO_01 native technical record

Native file size: **448,937,678 bytes**.  
Container: Matroska/WebM.  
Video: H.264/AVC Main, 960×576, 25 fps, progressive, yuv420p.  
Audio: AAC-LC, mono, 44.1 kHz.  
File duration: **3600.614 seconds**.  
Visible court clock begins approximately **25/07/2023 09:46:53** and is consistent with an end around **10:46:53**.

Working-custody hash identifies the exact uploaded binary in this ChatGPT session; it is not a substitute for a court-certified source or a provider-independent custody event.

## 3. Stable transcript / evidence schema for all three videos

Every spoken intervention that is eventually verified must use the following fields:

| Field | Rule |
|---|---|
| `component` | `VIDEO_01`, `VIDEO_02`, or `VIDEO_03` |
| `local_start` / `local_end` | HH:MM:SS.mmm relative to component |
| `court_clock` | visible court timestamp where readable; otherwise blank |
| `component_seq` | `V01-T000001`, `V02-T000001`, etc. Component-local numbering never changes |
| `global_seq` | assigned only after continuous three-video stitching; do not guess across missing transcript segments |
| `speaker_id` | stable role/candidate ID; never guessed from face |
| `speaker_display_label` | exact videoconference label if visible |
| `speaker_name_status` | VERIFIED BY TEXT/RECORD / CANDIDATE / UNRESOLVED |
| `speaker_role` | sourced role, with source status |
| `text` | verbatim or near-verbatim; use `[inaudible]`, `[uncertain wording]`, `[speaker uncertain]` |
| `confidence` | HIGH / MEDIUM / LOW |
| `issue` | controlled topic label |
| `document_referred` | exact title/date if identified |
| `party_affected` | LPB / Gil / PINK / AC / Fiscalía / Comunidad/CEXP / other |
| `evidential_class` | VERIFIED FACT / EVIDENCE-BASED INFERENCE / ALLEGATION-DISPUTED / EVIDENTIAL GAP |
| `significance` | concise evidential function, not rhetoric |
| `repository_crossrefs` | controlling ledgers / primary sources |
| `judgment_crossref` | RT branch / Sentencia section if applicable |
| `appeal_crossref` | ground/issue if applicable |
| `correction_history` | audit trail if transcript wording or attribution changes |

### Global numbering rule

Until VIDEO_01 has a trustworthy spoken transcript, **global spoken-intervention numbering is intentionally unassigned**. VIDEO_02/03 processing must retain component-local sequence IDs. After all components are available, global sequence numbers will be generated from stitched court time / continuity while preserving every component-local ID. This avoids forcing VIDEO_02/03 to renumber because VIDEO_01 speech could not yet be reliably segmented/transcribed in this runtime.

## 4. Speaker-resolution register — current VIDEO_01 evidence

Identity must not be inferred from a face. The current candidates come from visible interface text and independent preparation records.

| Stable ID | Visible label / source | Current role status | Resolution status |
|---|---|---|---|
| `WITNESS_DAVID_ESPEJO` | videoconference label reads `David Espejo Navarro` during opening segment | pre-hearing witness-question document identifies David Espejo Navarro as perito / Expert Witness; Drive also contains an Espejo expert report / economic-note source family | **CANDIDATE IDENTIFICATION — textual label + documentary role; exact oath/testimony boundaries require audio** |
| `PARTY_GIL` | videoconference label reads `Gil Marer` around ~10–20 min | party/person affected in Calificación record | **TEXT-LABEL RESOLVED; whether speaking at each moment requires audio** |
| `WITNESS_JONATHAN_SIMO` | videoconference label reads `JONATHAN SIMO MORALES` from ~49 min onward | pre-hearing witness-question document identifies Jonathan Simó Morales as tax adviser to LPB and PINK; separate 2016 evidence register exists | **CANDIDATE IDENTIFICATION — textual label + documentary role; exact testimony boundaries require audio** |
| `JUDGE` | courtroom judicial figure | exact spoken interventions require audio; judicial identity controlled elsewhere | **ROLE CANDIDATE ONLY FROM SETTING; do not attribute speech until transcript** |
| `FISCAL` | courtroom participant | unresolved in VIDEO_01 visual-only pass | **UNRESOLVED** |
| `COUNSEL_*` | courtroom participants | unresolved in VIDEO_01 visual-only pass | **UNRESOLVED** |

## 5. VIDEO_01 visual chronology — mergeable opening blocks

These are visual/evidential navigation blocks, not substitutes for spoken interventions.

| Block | VIDEO_01 local time | Approx. court time | Observed state | Safe inference |
|---|---|---|---|---|
| `V01-B001` | 00:00–~10:00 | ~09:46:53–09:56:53 | principal remote window label `David Espejo Navarro`; courtroom inset | remote participation associated with that interface label during opening component |
| `V01-B002` | ~10:00–~15:00 | ~09:56:53–10:01:53 | principal remote view label `Gil Marer` | party-labelled remote window displayed |
| `V01-B003` | ~15:00–~23:00 | ~10:01:53–10:09:53 | call/participant screen displays `Gil Marer`; courtroom remains inset | connection/participant-state period; speech cannot be allocated visually |
| `V01-B004` | ~24:00–~49:00 | ~10:10:53–10:35:53 | courtroom becomes principal view | in-court questioning/discussion is visually underway; identities/speech await audio |
| `V01-B005` | ~49:00–60:00 | ~10:35:53–10:46:53 | principal remote window label `JONATHAN SIMO MORALES`; courtroom inset | remote participation associated with that interface label through end of VIDEO_01 |

## 6. Required canonical issue tracks

All three components must be coded consistently against:

- `RT-00` collaboration umbrella;
- `RT-01` receivables / CEXP-Comunidad balances;
- `RT-02` PINK rent / non-claim / termination / causation;
- `RT-03` accounting books and supplied material;
- `RT-06/07` alzamiento theories and rejected branches;
- `RT-10` late filing, preserving that Gil was not allocated late filing in Sentencia 163/2023;
- `RT-11` collaboration / missing-support narrowing;
- `RT-12` annual accounts;
- rescue/commercial-normalisation/conclusion efforts;
- hotel operation, costs, maintenance and viability;
- Comunidad/CEXP authority, ACTA, debt and receivable provenance;
- 2018 material-control/access threshold and its effect on practical capacity;
- ownership/possession/control distinctions;
- AC consistency and source support;
- judicial knowledge / evidence-before-actor;
- Sentencia 163/2023 outcome and RPL 2523/2025 appeal issue.

## 7. Documentary controls already recovered for comparison

The hearing must be read against, not instead of:

- `archive/CALIFICACION_CANONICAL_AC_FISCAL_JUDGMENT_PERSON_MATRIX_17AUG2026.md`;
- `archive/CALIFICACION_RECORDED_OPEN_EVIDENCE_INTELLIGENCE_REGISTER_17AUG2026.md` (`OE-CAL-002` in particular);
- `archive/JUDGE_KNOWLEDGE_MATRIX_15AUG2026.md`;
- `archive/SUN_PARK_ACTA_AUTHORITY_LEGITIMACY_VISUAL_CONTROL_17AUG2026.md`;
- `archive/SUN_PARK_COMMUNITY_2012_GOOD_FAITH_FEES_AND_EVICTION_CORRECTION_GATE_17AUG2026.md`;
- `archive/CAM_2018_EXTRACONCURSAL_TAKEOVER_RETRIEVAL_GATE_16AUG2026.md`;
- `archive/SUN_PARK_MASTER_STORYLINE_TIMELINE_1989_2022_16AUG2026.md`;
- `archive/SUN_PARK_MULTIPLE_FUNDING_RETRIEVAL_GATE_16AUG2026.md` where relevant;
- the primary 11-Feb-2019 AC report, 12-Mar-2019 Fiscal opinion, LPB/Gil/PINK oppositions, Sentencia 163/2023 and appeal materials;
- Drive document `TESTIGOS Y PREGUNTAS CALIFICACION`, which is a **pre-hearing preparation/question source, not testimony**;
- David Espejo expert-report/economic-note source family, including `Calificación JT - documento cinco (pericial de Espejo valor razonable LPB).pdf` and `Pericial - Nota Económica derechos contra la CEXP 11JUN2018.pdf`;
- Jonathan Simó / PwC 2016 evidence-register/source family, which must be used only to test consistency/provenance, not to substitute for 2023 testimony.

## 8. Judicial-knowledge rule for the Vista

For each verified passage eventually transcribed, record separately:

1. what the recording proves the Judge **heard**;
2. what a participant **asserted**;
3. what document, if any, was identified or shown;
4. whether the proposition was challenged;
5. any judicial question, acknowledgment or ruling;
6. whether the same proposition was already formally in the docket;
7. later relevance to Sentencia 163/2023 and appeal.

Never convert `heard / was told / document in file` into personal acceptance, intent, prevaricación or criminal knowledge without the additional actor-specific proof required by the canonical knowledge matrix.

## 9. AC-specific Vista control

Every verified AC statement must be compared proposition-by-proposition against the 11-Feb-2019 report and earlier communications. Use the labels:

`CONSISTENT` / `NARROWED` / `CHANGED POSITION` / `OMISSION` / `TENSION` / `CONTRADICTION` / `UNRESOLVED`.

A contradiction requires a materially incompatible proposition, not a difference in emphasis or memory.

## 10. Comunidad / authority control

Any Vista reference to Comunidad de Explotación, Comunidad de Propietarios, ACTAs, presidents/administrators, votes, purported debts or representation must be mapped into the 2008 baseline → 2011 disputed authority break → later reliance chain. Use `contested authority`, `disputed ACTA`, `provenance challenged`, `purported decision` unless a stronger status is proved by a primary/competent source.

## 11. Publication control

No public page should presently quote VIDEO_01 speech because no verified audio transcript has been produced in this runtime. Visual facts and source-status changes may be used internally. Website recommendations remain **repository-only pending the full three-video context** except for the narrow statement that a three-part audiovisual hearing source has been located/ingested component by component.

## 12. Current transcription status

**VIDEO_01 verified spoken transcription: 0%** in this processing pass.  
**Visual/technical duration processed: 60:00.614 (100% of VIDEO_01).**

Reason: the current runtime contains no trustworthy Spanish ASR model/service. An attempted local installation could not access an external package/model source. The source audio is present and intact; no missing speech has been invented. A later transcript pass must preserve the schema above and append an audit trail.

This is an evidential-quality limitation, not an inference that the audio is unintelligible.

## 13. Three-video completion gate

The canonical Vista object is not mature for merits conclusions until VIDEO_02 and VIDEO_03 are ingested and continuity checked for gaps/overlap. In particular, do not finally interpret:

- any answer cut off by the end of VIDEO_01;
- witness qualifications that may be corrected later;
- apparent concessions without follow-up questioning;
- judicial remarks whose later ruling/context is in VIDEO_02/03;
- document references where the document is introduced or explained later;
- opening framing that later testimony qualifies;
- any omission/non-answer unless the complete questioning opportunity is known.

## 14. Merge destination

All component-specific handoffs must point back to this file. After all three components are available, create the stitched transcript and allegation → evidence → Vista → Sentencia → appeal crosswalk as derivatives of this **single canonical Vista object**, not three separate evidential narratives.
