# CALIFICACIÓN VISTA — THREE-VIDEO CANONICAL PROCESSING PROTOCOL

**Date:** 21 August 2026  
**Matter:** Concurso 36/2012 — Juzgado de lo Mercantil nº 1 de Las Palmas  
**Status:** INTERNAL EVIDENCE-PROCESSING CONTROL — execution pending where source MKVs/audio derivatives are not yet available to the active runtime

## Purpose

Preserve the governing workflow for the complete Vista de la Sección de Calificación recorded across three MKV files. The three recordings are to be treated as **one continuous judicial hearing split into three source files for technical recording purposes**, not as three independent evidential events.

The protocol exists to prevent two failure modes:

1. silently skipping testimony because the active runtime lacks a locally installed speech-to-text model; and
2. presenting inferred, reconstructed or machine-generated wording as verified testimony.

The absence of a local STT model is a **processing dependency**, not authority to omit the hearing and not evidence that testimony does not exist.

## Source recordings

Process, in order:

1. private source component `VIDEO_01`;
2. private source component `VIDEO_02`;
3. private source component `VIDEO_03`.

Exact private source filenames are withheld from public Git; the component hashes in the source manifest are the public integrity anchors.

Canonical sequence:

`VIDEO_01 -> VIDEO_02 -> VIDEO_03`

Do not modify or overwrite the original MKVs.

## Evidential status vocabulary

Use these statuses consistently:

- **VERIFIED TRANSCRIPTION** — wording audibly checked against the source recording.
- **MACHINE TRANSCRIPTION — REVIEW REQUIRED** — STT output not yet human/aurally verified.
- **UNCERTAIN / INAUDIBLE** — passage cannot be confidently resolved.
- **ANALYTICAL PARAPHRASE** — separate interpretation layer; never present as verbatim evidence.

Never fabricate, reconstruct from expectation, regularise grammar, or infer missing testimony as though it were spoken.

## Stage 1 — source manifest and integrity

For each MKV record:

- exact filename;
- byte size;
- exact duration;
- video codec;
- audio codec;
- frame rate where available;
- audio sample rate and channel count;
- relevant creation/container metadata;
- SHA-256 hash.

Preserve the results in the source manifest. The original MKVs remain evidential masters.

## Stage 2 — controlled audio derivatives

Extract speech-preserving transcription derivatives with FFmpeg or equivalent local tooling.

Preferred derivative:

- FLAC or WAV;
- mono;
- 16 kHz;
- no destructive filtering;
- no aggressive noise suppression;
- no alteration of the MKV master.

Preferred names:

- `CALIFICACION_VIDEO_01_AUDIO_MASTER.flac`
- `CALIFICACION_VIDEO_02_AUDIO_MASTER.flac`
- `CALIFICACION_VIDEO_03_AUDIO_MASTER.flac`

Hash each derivative and record the exact extraction command/process.

## Stage 3 — segmentation

Where the transcription engine requires smaller files, divide audio into sequential chunks with no discarded material.

Preferred parameters:

- 15–25 minute chunks;
- 5–10 second overlap;
- deterministic filenames;
- preserved source offsets.

Example:

- `VIDEO_01_000000-001500.flac`
- `VIDEO_01_001450-003000.flac`

For every chunk record:

- source MKV;
- derivative source;
- chunk filename;
- local start/end;
- overlap;
- SHA-256;
- canonical Vista start/end.

The overlap is solely to prevent words being lost at cut boundaries. Deduplicate overlap during transcript assembly.

## Stage 4 — speech-to-text route

If the active runtime has no installed local STT model, **do not terminate processing**.

Complete all locally possible stages first: inspection, hashing, extraction, segmentation, manifests and timeline mapping.

Then use an available external transcription service capable of Spanish long-form speech. Prefer a route supporting:

- Spanish speech recognition;
- speaker diarisation;
- timestamps;
- long recordings;
- uncertainty preservation.

Where OpenAI transcription is available, first test a diarisation-capable model such as `gpt-4o-transcribe-diarize` on controlled derivatives. External STT output remains machine transcription until checked against the recording.

If external STT cannot be invoked from the active runtime, identify exactly which derivative/chunk files must next be submitted. Do not reduce the status to a vague statement that the substantive testimony stage is open.

## Stage 5 — speaker diarisation and identification

Diarisation and identity are separate propositions.

First assign neutral labels:

- `SPEAKER_01`
- `SPEAKER_02`
- etc.

Name a speaker only where reliable evidence supports identity, for example:

- introduction in the hearing;
- explicit address by name;
- courtroom role;
- documentary cross-reference;
- previously verified identification.

Where uncertain use a qualified label such as:

`SPEAKER_04 [possibly Jonathan Simó — identification requires verification]`

Never silently convert a diarisation label into a named witness.

## Stage 6 — canonical continuous timeline

Maintain two simultaneous timestamp systems:

### A. Continuous Vista timestamp

Runs continuously from the beginning of VIDEO_01 through VIDEO_03.

Example: `VISTA 01:42:31`.

### B. Source-file timestamp

Example: `VIDEO_02 00:17:09`.

Canonical citation form:

`[VISTA 01:42:31 | VIDEO_02 00:17:09]`

Determine precisely whether file boundaries are continuous, overlapping or contain omissions. Do not assume or guess a gap.

## Stage 7 — transcript format

For each passage preserve:

`[VISTA hh:mm:ss | VIDEO_0N hh:mm:ss]`

**SPEAKER / VERIFIED NAME WHERE SUPPORTED**

Transcript text.

`Status: MACHINE TRANSCRIPTION — REVIEW REQUIRED`

or

`Status: VERIFIED AGAINST AUDIO`

Use explicit markers where appropriate:

- `[inaudible 00:03]`
- `[uncertain: "..."?]`
- `[speaker overlap]`
- `[interruption]`
- `[courtroom noise]`

Do not improve witness grammar in the verbatim layer.

## Stage 8 — courtroom context

Capture where discernible:

- questioner and respondent;
- judicial interventions;
- objections;
- interruptions;
- witness changes;
- document references;
- dates, companies, sums and names;
- concessions;
- disagreement;
- lack of recollection;
- qualifications such as "I think", "I do not remember", "possibly" and equivalents.

These qualifiers may be evidentially material and must not be cleaned out.

## Stage 9 — testimony digest

After, and separate from, the canonical transcript, create a structured digest per witness/participant covering:

- identity and role;
- connection to LPB / Sun Park / PwC / CLS / Horizonia / Comunidad / AC / other relevant entities;
- each material proposition;
- exact Vista/source timestamp;
- direct knowledge vs hearsay/opinion/inference;
- supporting document;
- contradiction/corroboration elsewhere;
- significance to the Calificación.

## Dedicated Jonathan Simó control

Create and maintain a separate evidence profile for **Jonathan Simó**. Subject to documentary verification, reconstruct:

- professional role at the relevant time;
- connection to the relevant accounting practice / CLS accounting;
- later professional activity including Horizonia where verified;
- status as witness in the Calificación Vista;
- what he personally knew and did;
- accounting, financial or corporate information available to him;
- testimony concerning LPB, Sun Park, Gil Marer, PwC, accounting, insolvency, Comunidad, receivables or related issues;
- direct professional knowledge versus later recollection.

Do not add irrelevant family/private biographical material.

## Cross-reference — 2016 PwC / Cristo Suárez Pimentel recording

Cross-reference verified Vista testimony against the separate 2016 meeting recording/transcription involving, where evidenced:

- Cristo Suárez Pimentel;
- PwC;
- Jonathan Simó;
- Prieto Puente;
- Matos Matas;
- other identifiable attendees.

Preserve provenance cautiously. A reported fact such as who activated or supplied a recording must be stated only to the degree supported by underlying evidence.

Search for materially relevant agreement or conflict concerning:

- LPB accounting/financial position;
- debts and receivables;
- Comunidad/CEXP;
- PwC;
- insolvency causation;
- knowledge of relevant private actors;
- matters relied upon in the Calificación.

A contradiction is not established until both passages are accurately transcribed and compared in context.

## Calificación issue matrix

Tag testimony where relevant to:

- alleged non-cooperation with the Administrador Concursal;
- accounting/document-delivery allegations;
- alleged causes of insolvency;
- third-party receivables;
- Comunidad/CEXP receivables;
- alleged aggravation of insolvency;
- LPB management/control;
- actual Sun Park operation;
- third-party interference;
- Bankia/creditor enforcement context;
- pre-concurso circumstances;
- accounting/professional advisers;
- information supplied to the AC;
- allegedly missing documents;
- propositions later accepted, rejected or qualified by Sentencia 163/2023 or the pending appeal.

The first-instance Calificación judgment and pending appeal must remain procedurally distinct. Where needed use the project formulation: **“materialmente adversa y pendiente de apelación”.**

## Repository cross-reference classification

For every significant testimony proposition classify the wider evidential state as one of:

1. corroborated;
2. contradicted;
3. partially corroborated;
4. unresolved;
5. requires further evidence.

Cross-reference exact repository sources, including where relevant:

- pleadings;
- AC reports;
- Fiscalía submissions;
- opposition filings;
- Sentencia 163/2023;
- appeal materials;
- witness correspondence;
- PwC communications;
- accounting records;
- adviser correspondence;
- Comunidad/CEXP records;
- the 2016 PwC/Cristo recording;
- documents mentioned in testimony.

## Contradiction / corroboration register

Maintain fields for:

- witness;
- proposition;
- Vista timestamp;
- exact words or accurate summary;
- comparison source/passage;
- corroboration/contradiction status;
- significance;
- confidence;
- follow-up required.

Pay particular attention to changes between contemporaneous documents, the 2016 meeting, the Calificación Vista, later pleadings and later judicial findings.

## Analytical discipline

The record should permit later analysis of what the judge heard, what the AC alleged, what witnesses actually said, what documents existed and whether later evidence affects the first-instance reasoning.

Do **not** infer misconduct, bias, prevaricación, concealment or intentional omission merely because an inconsistency exists.

Maintain separate categories for:

- verified procedural event;
- evidential inconsistency;
- analytical inference;
- allegation;
- unresolved question.

## Canonical repository outputs

Create or populate, using existing naming conventions where they already provide a better canonical location:

- `archive/CALIFICACION_VISTA_SOURCE_MANIFEST.md`
- `archive/CALIFICACION_VISTA_THREE_VIDEO_PROCESSING_LOG.md`
- `archive/CALIFICACION_VISTA_CANONICAL_TRANSCRIPT.md`
- `archive/CALIFICACION_VISTA_SPEAKER_REGISTER.md`
- `archive/CALIFICACION_VISTA_TESTIMONY_DIGEST.md`
- `archive/CALIFICACION_VISTA_CONTRADICTION_CORROBORATION_REGISTER.md`
- `archive/CALIFICACION_VISTA_DOCUMENT_CROSS_REFERENCE.md`
- `archive/CALIFICACION_VISTA_PROCESSING_GAPS.md`
- `archive/JONATHAN_SIMO_WITNESS_EVIDENCE_PROFILE.md`

Do not create duplicate competing canonicals if an equivalent file already exists.

## Website publication control

Do not automatically publish raw machine transcription.

For public-facing use:

- quote only verified passages;
- retain exact timestamps/source pointers;
- identify disputed propositions accurately;
- link to supporting evidence where appropriate;
- distinguish evidence from interpretation;
- preserve Spanish/English consistency.

## Processing-gap rule

A gap is acceptable. A silent omission is not.

For unresolved material record:

- source file;
- exact timestamp range;
- why unresolved;
- whether audio exists;
- whether extraction succeeded;
- whether STT was attempted;
- model/service used;
- result/error;
- precise next action.

Example:

`VIDEO_02 00:43:20–00:47:05 — audio successfully extracted and hashed; external STT not yet executed; substantive testimony therefore remains unverified. No transcript has been inferred.`

## Execution order

1. inspect all three MKVs;
2. hash and create source manifest;
3. determine exact duration and continuity;
4. extract audio derivatives;
5. hash derivatives;
6. create chunk manifests;
7. transcribe through available STT;
8. diarise speakers;
9. reconcile overlaps;
10. construct continuous Vista transcript;
11. identify speakers cautiously;
12. aurally verify material passages;
13. build testimony digest;
14. scan repository for corroboration/contradiction;
15. build issue matrix;
16. create Jonathan Simó profile;
17. cross-reference 2016 PwC/Cristo recording;
18. update repository canonicals;
19. prepare only verified website-safe extracts;
20. run deletion/continuity audit.

## Continuity / deletion requirement

A future thread, without access to the originating chat, must be able to recover from the repository:

- that there are three source videos;
- that they form one Vista;
- source order;
- hashes/durations once processed;
- continuous-timeline offsets;
- transcription status;
- speaker register;
- Jonathan Simó evidence profile;
- unresolved gaps;
- location of derivatives/transcripts;
- relevant document cross-references.

Anything retained only in conversational memory is not preserved.

## Current status as of 21 August 2026

The project has identified the governing three-video workflow. The substantive testimony must not be represented as complete until source-derived transcription and verification are performed. The previously identified runtime limitation — no installed local STT model and inability to install one over the network — is expressly treated as a **processing gap only**. The correct remedy is controlled audio extraction/segmentation plus an available external STT route, followed by source verification.
