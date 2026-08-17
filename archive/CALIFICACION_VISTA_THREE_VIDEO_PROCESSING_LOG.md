# CALIFICACIÓN VISTA — THREE-VIDEO PROCESSING LOG

**Date:** 17 August 2026  
**Canonical object:** `Vista de Calificación — Concurso 36/2012`

## Execution log

1. **Inspected all three MKVs:** COMPLETE. ffprobe and SHA-256 performed against exact uploaded binaries.
2. **Source manifest:** COMPLETE. See `CALIFICACION_VISTA_SOURCE_MANIFEST.md`.
3. **Continuity:** COMPLETE at technical/source level. VIDEO_01→02 near-seamless by visible clock; VIDEO_02→03 contains an unresolved ~39m32s wall-clock interval.
4. **Controlled audio extraction:** COMPLETE. Three mono 16 kHz FLAC masters generated without denoising or destructive filtering.
5. **Derivative hashing:** COMPLETE.
6. **STT chunking:** COMPLETE. Seven chunks with deterministic filenames and 10-second overlap; no discarded audio.
7. **Local STT capability test:** NO TRUSTWORTHY MODEL AVAILABLE. No `whisper` or `faster_whisper` package/model installed. PyTorch is present but no model weights are available.
8. **External OpenAI STT capability test:** BLOCKED IN THIS RUNTIME. Python OpenAI client is installed, but no `OPENAI_API_KEY` is present and DNS/network access to `api.openai.com` failed. No external request was fabricated or claimed.
9. **STT result:** NOT EXECUTED. Therefore no machine words are inserted into the evidential transcript.
10. **Diarisation:** NOT EXECUTED. Visual participant labels are preserved separately from speaker diarisation.
11. **Overlap reconciliation:** PENDING STT.
12. **Canonical transcript:** scaffold created; no invented testimony.
13. **Testimony digest:** scaffold/source map created; substantive propositions await transcript.
14. **Repository corroboration scan:** existing canonical Calificación, Espejo, Jonathan Simó/PwC, appeal, Community and Judge-knowledge controls identified; proposition-level comparison awaits transcript.
15. **Website-safe extracts:** NONE from spoken evidence yet. Technical recovery only is publication-ready in narrow form.
16. **Continuity audit:** updated in this processing package.

## External STT target

When a suitable authenticated/networked runtime is available, submit the chunks in `CALIFICACION_VISTA_SOURCE_MANIFEST.md` to a Spanish-capable diarisation transcription route. For OpenAI, current API documentation supports `gpt-4o-transcribe-diarize`, `response_format=diarized_json`, Spanish language hints, and requires a chunking strategy for diarisation inputs longer than 30 seconds. Preserve raw model output as `MACHINE TRANSCRIPTION — REVIEW REQUIRED`; do not publish it as verified testimony.

Recommended request metadata to preserve per chunk:

- exact chunk filename and SHA-256;
- model and snapshot if returned;
- request date/time;
- language=`es`;
- response format;
- chunking strategy;
- raw diarised JSON;
- any API error;
- subsequent human verification status.

## Source-to-transcript mapping rule

For every STT segment calculate:

`source_local = audio_chunk_local + chunk_audio_start + audio_to_source_offset`

and:

`vista_continuous = component_vista_offset + source_local`

Canonical displayed form:

`[VISTA HH:MM:SS.mmm | VIDEO_0N HH:MM:SS.mmm]`

The continuous Vista time is a concatenated supplied-media timebase. The separate visible court-clock map must be retained so the VIDEO_02→03 wall-clock interval is never silently erased.

## Non-negotiable status vocabulary

- `VERIFIED TRANSCRIPTION` / `VERIFIED AGAINST AUDIO`
- `MACHINE TRANSCRIPTION — REVIEW REQUIRED`
- `UNCERTAIN / INAUDIBLE`
- `ANALYTICAL PARAPHRASE`

No other layer may silently replace these statuses.
