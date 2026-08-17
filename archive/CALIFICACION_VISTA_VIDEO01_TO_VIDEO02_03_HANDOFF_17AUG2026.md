# CALIFICACIÓN VISTA — VIDEO_01 → VIDEO_02/03 HANDOFF

**Date:** 17 August 2026  
**Canonical object:** `Vista de Calificación — Concurso 36/2012`  
**Master file:** `archive/CALIFICACION_VISTA_25JUL2023_THREE_VIDEO_MASTER_INDEX_17AUG2026.md`

## 1. Canonical files created/updated in VIDEO_01 thread

1. **Created:** `archive/CALIFICACION_VISTA_25JUL2023_THREE_VIDEO_MASTER_INDEX_17AUG2026.md`
2. **Updated/recast:** `archive/CALIFICACION_VISTA_25JUL2023_VIDEO01_EVIDENCE_INGEST_17AUG2026.md`
3. **Created:** `archive/CALIFICACION_VISTA_VIDEO01_TO_VIDEO02_03_HANDOFF_17AUG2026.md`

All are on branch `evidence/calificacion-vista-video-01-20230725` / PR #295 pending protected-main integration.

## 2. Native VIDEO_01 control

Exact filename:
`J. Mercantil 1 (Palmas de Gran Canaria (Las))_0000036_2012_VIDEO_01.mkv`

Size: **448,937,678 bytes**  
Duration: **3600.614 s**  
SHA-256: `63a08742ae6925cb347fe25ceb2c6a78e0625a4aa7ec1df71b6b8602f4eb7d4f`  
Video: H.264 960×576, 25 fps.  
Audio: AAC mono 44.1 kHz.  
Visible court clock: approximately **09:46:53 → 10:46:53, 25-Jul-2023**.

## 3. Transcript convention

Use master schema fields:
`component`, `local_start`, `local_end`, `court_clock`, `component_seq`, `global_seq`, `speaker_id`, `speaker_display_label`, `speaker_name_status`, `speaker_role`, `text`, `confidence`, `issue`, `document_referred`, `party_affected`, `evidential_class`, `significance`, `repository_crossrefs`, `judgment_crossref`, `appeal_crossref`, `correction_history`.

Mandatory uncertainty markers:
`[inaudible]`, `[uncertain wording]`, `[speaker uncertain]`.

Never silently polish testimony.

## 4. Sequence-number state

VIDEO_01 has **no trustworthy spoken-intervention count yet** because this runtime lacks Spanish ASR. Therefore:

- VIDEO_01 component-local transcript IDs will later be `V01-T000001...`;
- VIDEO_02 should use `V02-T000001...`;
- VIDEO_03 should use `V03-T000001...`;
- **global spoken sequence is currently unassigned (last global spoken sequence = 0)**;
- final stitched global numbering is to be assigned after all three local transcripts/continuity checks are available, preserving component-local IDs permanently.

Visual navigation blocks already assigned in VIDEO_01: `V01-B001` through `V01-B005`.

## 5. Speaker IDs already assigned / candidates

| Speaker ID | Current evidence |
|---|---|
| `WITNESS_DAVID_ESPEJO` | visible interface label `David Espejo Navarro` in opening segment; pre-hearing `TESTIGOS Y PREGUNTAS CALIFICACION` identifies him as perito / Expert Witness; exact testimony boundaries await audio |
| `PARTY_GIL` | visible interface label `Gil Marer` around ~10–23 min; exact speech allocation awaits audio |
| `WITNESS_JONATHAN_SIMO` | visible interface label `JONATHAN SIMO MORALES` from ~49 min onward; pre-hearing preparation file identifies him as tax adviser to LPB and PINK; exact testimony boundaries await audio |
| `JUDGE` | reserved stable role ID; do not allocate specific words without audio |
| `FISCAL` | reserved stable role ID; unresolved visually |
| `AC` | reserved stable role ID; unresolved visually |
| `COUNSEL_LPB`, `COUNSEL_GIL`, `COUNSEL_PINK` | reserved stable role IDs; unresolved visually |

Do not identify courtroom people from facial appearance.

## 6. VIDEO_01 visual chronology

- `V01-B001` 00:00–~10:00 — remote label `David Espejo Navarro`; courtroom inset.
- `V01-B002` ~10:00–~15:00 — remote label `Gil Marer`.
- `V01-B003` ~15:00–~23:00 — participant/call-status view displays `Gil Marer`.
- `V01-B004` ~24:00–~49:00 — courtroom principal view.
- `V01-B005` ~49:00–60:00 — remote label `JONATHAN SIMO MORALES`; courtroom inset.

## 7. Unresolved speaker identities

- exact identity/role of courtroom participants;
- which courtroom participant is speaking at each intervention;
- whether all visible remote labels correspond to sworn witnesses/party examination at the relevant instant;
- exact start/end of David Espejo, Gil and Jonathan Simó spoken participation;
- counsel allocation and Fiscalía/AC intervention boundaries.

## 8. Documentary sources located for immediate cross-check

- canonical AC → Fiscalía → judgment → person matrix;
- 11-Feb-2019 AC report;
- 12-Mar-2019 Fiscal opinion;
- LPB/Gil/PINK opposition materials;
- Sentencia 163/2023;
- Gil/PINK appeal materials;
- `JUDGE_KNOWLEDGE_MATRIX_15AUG2026.md`;
- `SUN_PARK_ACTA_AUTHORITY_LEGITIMACY_VISUAL_CONTROL_17AUG2026.md`;
- Drive `TESTIGOS Y PREGUNTAS CALIFICACION` — **preparation/question document, not hearing testimony**;
- Drive `Calificación JT - documento cinco (pericial de Espejo valor razonable LPB).pdf`;
- Drive `Pericial - Nota Económica derechos contra la CEXP 11JUN2018.pdf` and duplicate/alias source family;
- Drive Jonathan Simó/PwC 2016 LIVE evidence register/source family;
- appeal document `20231012 Apelacion calificacion GIL.docx` located in Drive.

## 9. Major findings safely established from VIDEO_01 at this stage

1. VIDEO_01 is the opening one-hour component of the 25-Jul-2023 Vista and is technically suitable for timestamp stitching.
2. The interface/court overlay supports a continuous hearing-clock window of roughly 09:46:53–10:46:53.
3. Text-visible remote labels establish candidate participation windows for David Espejo Navarro, Gil Marer and Jonathan Simó Morales.
4. Independent pre-hearing material supplies documentary role context for Espejo and Simó, but does not prove their actual 2023 words.
5. VIDEO_01 partially closes the audiovisual-location limb of OE-CAL-002; it does not close the complete hearing/effective-defence dossier.

## 10. Contradictions established from VIDEO_01

**None yet from spoken evidence.**

Do not create contradiction entries until the audio is reliably transcribed and compared with the primary source. Visual changes or a witness's posture are not contradictions.

Potential comparison targets once transcription exists:

- Espejo testimony ↔ his expert/economic-note reports ↔ AC receivable theory ↔ Sentencia treatment;
- Jonathan Simó testimony ↔ accounting/tax records ↔ 2016 PwC/Comunidad source family ↔ AC collaboration/accounting propositions;
- any AC statement ↔ 11-Feb-2019 report and earlier correspondence;
- any Comunidad assertion ↔ 2008/2011 authority chain and debt/receivable sources.

## 11. Evidence gaps

- verified Spanish transcript of VIDEO_01;
- VIDEO_02/03 hashes, duration and continuity/overlap/gap map;
- official minute / certified audiovisual index;
- attendance and representation record;
- service/withdrawal/substitution history relevant to nullity/effective defence;
- evidential admission/exclusion rulings;
- exact documents shown/referred to in the Vista;
- speaker-by-speaker role confirmation from the official record;
- whether any answer in VIDEO_01 is completed/qualified in VIDEO_02.

## 12. Matters requiring confirmation in VIDEO_02/03

- whether Jonathan Simó's examination continues across the VIDEO_01→VIDEO_02 boundary;
- whether any apparent answer/concession at the end of VIDEO_01 is later qualified;
- whether the Judge later resolves objections/questions raised during VIDEO_01;
- whether documents mentioned in VIDEO_01 are formally introduced/explained later;
- whether the hearing later addresses hotel operation, Comunidad authority, rent/receivables, accounting, collaboration, rescue/exit, 2018 control or other RT branches in a way that changes the opening frame;
- exact end of testimony for each early witness/party.

## 13. Judicial-knowledge handoff

VIDEO_02/03 must continue the eventual table:
`Proposition | component + timestamp | how placed before Judge | supporting document | disputed? | judicial response | later Sentencia relevance | appeal relevance`.

Do not fill a row merely because a document existed in the docket. The Vista can prove a proposition was orally placed before the court only after the spoken record is verified.

## 14. Publication status

- technical/source recovery: **publication-ready in narrow form**;
- speaker labels/roles: **repository-only until contextualized**;
- testimony quotations: **not publication-ready**;
- contradictions / omissions / knowledge claims: **not publication-ready pending transcript + all three components**;
- website rewriting: **defer merits changes until complete Vista context**.

## 15. Tooling limitation that must not be lost

This VIDEO_01 thread processed **100% of the visual/technical duration but 0% of spoken content as a verified transcript** because the runtime did not contain a trustworthy Spanish speech-recognition model/service. An attempted local installation could not reach an external package/model source. This is a tooling limitation only: it does not mean the source audio is absent or unintelligible. A future thread with reliable Spanish ASR should resume from the master schema rather than treating this status as final.

## 16. Handoff instruction to VIDEO_02/03 thread

Read the master index first. Preserve component-local transcript IDs. Do not restart the hearing narrative as if VIDEO_02 or VIDEO_03 were separate evidence. Record exact first visible court clock and compare against VIDEO_01's approximate end ~10:46:53 to detect overlap/gap. If the first VIDEO_02 words are a continuation of a VIDEO_01 question/answer, mark the intervention `CROSSES_COMPONENT_BOUNDARY` and preserve both component timestamps.
