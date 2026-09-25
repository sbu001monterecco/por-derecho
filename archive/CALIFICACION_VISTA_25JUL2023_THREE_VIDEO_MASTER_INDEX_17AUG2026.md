# VISTA DE CALIFICACIÓN — CONCURSO 36/2012 — THREE-VIDEO MASTER INDEX

**Date created:** 17 August 2026  
**Hearing date:** 25 July 2023  
**Court:** Juzgado de lo Mercantil nº 1 de Las Palmas de Gran Canaria  
**Proceeding:** Concurso ordinario 36/2012 — Sección de Calificación  
**Canonical evidential object:** **Vista de Calificación — Concurso 36/2012**  
**Status:** `ALL THREE PRIVATE SOURCE COMPONENTS LOCATED / TECHNICALLY FINGERPRINTED / VISUALLY INDEXED / VERIFIED SPEECH TRANSCRIPT PENDING`

## 0. Controlling rule

VIDEO_01 + VIDEO_02 + VIDEO_03 are one hearing record split into technical recording components. Never treat a component as a separate hearing or draw a final merits conclusion from one component where later context may qualify it.

The three source binaries remain private and are not uploaded to the public repository. This file preserves public-safe provenance and integration intelligence only.

## 1. Exact components and fingerprints

| Component | Public-safe source label | SHA-256 | Size | Duration | Visible court-clock range |
|---|---|---|---:|---:|---|
| VIDEO_01 | private component 01 (exact filename withheld) | `63a08742ae6925cb347fe25ceb2c6a78e0625a4aa7ec1df71b6b8602f4eb7d4f` | 448,937,678 bytes | 3600.614 s = 60:00.614 | approx. 09:46:53 → 10:46:53 |
| VIDEO_02 | private component 02 (exact filename withheld) | `fee31a75c78184e09c07fa4d489028a902233cc340a63faa88a1cd6b94b0f57e` | 231,434,953 bytes | 1916.9895 s = 31:56.99 | approx. 10:46:55 → 11:18:50 |
| VIDEO_03 | private component 03 (exact filename withheld) | `8bc5a27768bf61ee520ebcd97f308bdb5f5ed594175cfa032ee98fa7093cdd07` | 192,947,423 bytes | 1500.267375 s = 25:00.27 | approx. 11:58:22 → 12:23:21 |

All three containers carry H.264 video and AAC audio. VIDEO_01 was independently fingerprinted in two ChatGPT processing threads and the SHA-256, size and duration match exactly.

Working hashes are integrity fingerprints of the supplied binaries. They are not a substitute for a court-certified audiovisual source or a provider-independent custody event.

## 2. Continuity findings

### VIDEO_01 → VIDEO_02

The visible source clock at the end of VIDEO_01 is approximately **10:46:53** and the start of VIDEO_02 approximately **10:46:55**. This approximately two-second transition strongly supports direct technical continuity between these two components.

The visual state also supports continuity: the final VIDEO_01 block shows the remote label **`JONATHAN SIMO MORALES`** and the opening VIDEO_02 samples also show **`JONATHAN SIMO MORALES`**. This is a visual continuity fact only; the spoken question/answer boundary still requires audio transcription.

### VIDEO_02 → VIDEO_03

VIDEO_02 ends at approximately **11:18:50** and VIDEO_03 begins at approximately **11:58:22**, leaving an approximately **39m32s visible-clock interval**.

Do not describe that interval as missing evidence without further proof. Possible explanations include recess, recording pause, another technical component, source-clock discontinuity or another procedural interruption. The certified hearing record/minute must resolve it.

VIDEO_02 ends with a remote participant tile labelled **`Gil Marer`**; VIDEO_03 begins with a tile labelled **`Gil Marer`**. That visual recurrence is relevant to continuity but does not prove the same spoken intervention crossed the interval.

## 3. Visual participant-label map

Identity is not inferred from faces. The following are interface-text observations plus separately controlled role material.

| Stable ID | Visible label | Components / approximate visual windows | Current status |
|---|---|---|---|
| `WITNESS_DAVID_ESPEJO` | `David Espejo Navarro` | VIDEO_01 opening ~0–10m; also appears in sampled VIDEO_02 frames | interface label verified; documentary role as expert/perito supported by pre-hearing/Drive material; exact testimony boundaries await audio |
| `PARTY_GIL` | `Gil Marer` | VIDEO_01 ~10–23m display state; VIDEO_02 near end; VIDEO_03 beginning | interface label verified; exact spoken participation requires audio |
| `WITNESS_JONATHAN_SIMO` | `JONATHAN SIMO MORALES` | VIDEO_01 ~49m through end and VIDEO_02 opening | interface label verified; documentary role supported by pre-hearing and 2016 accounting/PwC material; exact testimony requires audio |
| `JUDGE` | courtroom judicial role | all components courtroom feed | role must be tied to official record and audio before words are attributed |
| `FISCAL`, `AC`, `COUNSEL_*` | courtroom participants | unresolved visually | do not identify by face |

## 4. Component visual chronology

### VIDEO_01

- `V01-B001` 00:00–~10:00 — principal remote label `David Espejo Navarro`; courtroom inset.
- `V01-B002` ~10:00–~15:00 — principal remote label `Gil Marer`.
- `V01-B003` ~15:00–~23:00 — participant/call-status state displays `Gil Marer`.
- `V01-B004` ~24:00–~49:00 — courtroom principal view.
- `V01-B005` ~49:00–60:00 — principal remote label `JONATHAN SIMO MORALES`; courtroom inset.

### VIDEO_02

Technically verified 31:56.99 component beginning approx. 10:46:55. Sampled visual states include `JONATHAN SIMO MORALES` near the opening, later `David Espejo Navarro`, and `Gil Marer` near the end. Do not infer examination order solely from sampled principal-window states.

### VIDEO_03

Technically verified 25:00.27 component beginning approx. 11:58:22. The principal remote tile at the beginning is labelled `Gil Marer`; later sampled frames show the courtroom as principal view.

## 5. Transcript schema for the stitched Vista

Every verified spoken intervention must preserve:

`component`, `local_start`, `local_end`, `court_clock`, `component_seq`, `global_seq`, `speaker_id`, `speaker_display_label`, `speaker_name_status`, `speaker_role`, `text`, `confidence`, `issue`, `document_referred`, `party_affected`, `evidential_class`, `significance`, `repository_crossrefs`, `judgment_crossref`, `appeal_crossref`, `correction_history`.

Use `[inaudible]`, `[uncertain wording]` and `[speaker uncertain]` rather than inventing words.

Component-local IDs must be permanent: `V01-T...`, `V02-T...`, `V03-T...`. Assign global spoken sequence only after all component transcripts and the VIDEO_02→03 interval are reconciled.

## 6. Current transcription status

**Verified speaker-attributed speech transcript: not yet produced in the current technical passes.**

All three files contain audio. The processing runtimes used for the technical intake did not have a trustworthy local Spanish ASR model/service and no testimony has been fabricated.

This is a tooling/evidence-processing gap, not evidence that the audio is absent or unintelligible.

## 7. OE-CAL-002 correction

The old shorthand that the 25-Jul-2023 hearing audiovisual is wholly missing is superseded.

Current position:

> Private copies of all three technical components of the 25-Jul-2023 Calificación Vista have now been supplied and technically fingerprinted. The complete stitched, speaker-attributed transcript and certified hearing/audiovisual/attendance/service/representation/rulings record remain outstanding.

This partially closes the audiovisual-location limb of `OE-CAL-002`; it does not close the effective-defence/nullity or evidence-before-actor dossiers.

## 8. Documentary cross-reference priorities

The transcript must be tested against, at minimum:

- `archive/CALIFICACION_CANONICAL_AC_FISCAL_JUDGMENT_PERSON_MATRIX_17AUG2026.md`;
- `archive/CALIFICACION_RECORDED_OPEN_EVIDENCE_INTELLIGENCE_REGISTER_17AUG2026.md`;
- 11-Feb-2019 AC report;
- 12-Mar-2019 Fiscal position;
- LPB/Gil/PINK oppositions;
- Sentencia 163/2023;
- Gil/PINK appeal materials, including the nullity/effective-defence issue concerning the 25-Jul-2023 hearing;
- `archive/JUDGE_KNOWLEDGE_MATRIX_15AUG2026.md`;
- `archive/SUN_PARK_ACTA_AUTHORITY_LEGITIMACY_VISUAL_CONTROL_17AUG2026.md` and the 2012 good-faith fees correction gate;
- David Espejo expert/economic-note source family;
- Jonathan Simó accounting/PwC source family, including the corrected 10-Jun-2016 meeting date and recovered native reports;
- CAM 2018 material-control and multiple-financial-lives specialist gates where a verified passage makes those issues relevant.

## 9. Special evidential tracks after transcription

### David Espejo

Compare actual Vista evidence against his expert reports and the CEXP/Comunidad receivable questions, including €472,500, €518,908.69 and €737,338.85. Distinguish validity/existence/collectability from the narrower surviving collaboration/document-support finding.

### Jonathan Simó

Compare actual Vista evidence against the recovered 2012/2016 accounting and PwC source family. The 2016 material is a prior professional/documentary record, not a substitute for his 2023 testimony.

### Gil Marer

Map actual testimony to the appeal/nullity record, hotel-operation evidence, attempts to preserve/recover the business, Comunidad authority disputes, control/capacity and any documentary source expressly put to him.

### Judge / AC / Fiscal

For every verified passage distinguish: what was said, what the Judge demonstrably heard, what document was identified, whether challenged, what response/ruling followed, and whether the same source was already formally in the docket. `heard` is not the same as `accepted`, `personally reviewed`, `knowingly ignored`, or criminal intent.

## 10. Allegation → Vista → judgment → appeal architecture

After transcript verification, build one row per material issue:

`ALLEGATION → EVIDENCE RELIED UPON → VISTA PASSAGE → DOCUMENTARY CORROBORATION/CONTRADICTION → SENTENCIA 163/2023 OUTCOME → APPEAL ISSUE → PRESENT STATUS`.

Priority issue tracks include collaboration, CEXP/Comunidad receivables, PINK rent/costs, accounting, late-filing allocation, alzamiento branches, hotel operation/viability, rescue/conclusion efforts, practical control/capacity, Comunidad authority, AC consistency and judicial knowledge.

## 11. Public website rule

No testimony quote, contradiction finding, non-answer inference, Judge-knowledge claim or adverse characterisation is publication-ready solely from the present visual/technical intake.

The narrow fact that all three hearing components are now located/fingerprinted may be published if useful, but merits changes to the Calificación page should wait for source-checked transcription and three-component context.

The eventual preferred reader architecture is:

`ALLEGATION → EVIDENCE → WHAT THE VISTA SHOWED → DOCUMENTARY CHECK → JUDGMENT → APPEAL`.

## 12. Remaining evidence gaps

1. Verified full transcript of VIDEO_01/02/03.
2. Exact explanation of the 11:18:50→11:58:22 interval.
3. Certified court audiovisual/index and hearing minute.
4. Attendance and representation record.
5. Service, withdrawal and substitution history relevant to nullity/effective defence.
6. Evidential admission/exclusion rulings and document/exhibit index.
7. Exact speaker allocation from official record + audio.
8. Exact recording/source provenance and certified identity of the private copies.
9. Exact audiovisual/transmitted record before the Audiencia Provincial.

## 13. Canonical linked component files

- `archive/CALIFICACION_VISTA_25JUL2023_VIDEO01_EVIDENCE_INGEST_17AUG2026.md`
- `archive/CALIFICACION_VISTA_VIDEO_02_03_INTAKE_17AUG2026.md`
- `archive/CALIFICACION_VISTA_VIDEO02_03_SOURCE_CROSSREF_17AUG2026.md`
- `archive/THREAD_DELETION_CONTINUITY_AUDIT_CALIFICACION_VISTA_VIDEO02_03_17AUG2026.md`

This master index controls cross-component continuity. Component files remain provenance/detail ledgers and must not become competing standalone narratives.
