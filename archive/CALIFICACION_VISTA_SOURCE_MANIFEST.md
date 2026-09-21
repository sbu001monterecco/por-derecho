# CALIFICACIÓN VISTA — SOURCE / DERIVATIVE MANIFEST

**Date:** 17 August 2026  
**Canonical object:** `Vista de Calificación — Concurso 36/2012`  
**Status:** THREE ORIGINAL MKVS VERIFIED; CONTROLLED AUDIO DERIVATIVES AND STT CHUNKS GENERATED LOCALLY; TRANSCRIPTION NOT YET EXECUTED

This manifest supplements `archive/CALIFICACION_VISTA_25JUL2023_THREE_VIDEO_MASTER_INDEX_17AUG2026.md`. The three MKVs are one hearing split for technical recording purposes. The original MKVs were not modified.

## Original source manifest

| Component | Public-safe source label | Bytes | Duration | Video | Audio | SHA-256 |
|---|---|---:|---:|---|---|---|
| VIDEO_01 | private component 01 (exact filename withheld) | 448,937,678 | 3600.614000 s | H.264 Main, 960×576, 25 fps, yuv420p | AAC-LC, mono, 44.1 kHz | `63a08742ae6925cb347fe25ceb2c6a78e0625a4aa7ec1df71b6b8602f4eb7d4f` |
| VIDEO_02 | private component 02 (exact filename withheld) | 231,434,953 | 1916.989500 s | H.264 Main, 960×576, 25 fps, yuv420p | AAC-LC, mono, 44.1 kHz | `fee31a75c78184e09c07fa4d489028a902233cc340a63faa88a1cd6b94b0f57e` |
| VIDEO_03 | private component 03 (exact filename withheld) | 192,947,423 | 1500.267375 s | H.264 Main, 960×576, 25 fps, yuv420p | AAC-LC, mono, 44.1 kHz | `8bc5a27768bf61ee520ebcd97f308bdb5f5ed594175cfa032ee98fa7093cdd07` |

Container metadata on all three reports `encoder=libmatroska 1.3.0`. No reliable creation-time tag was exposed by ffprobe.

## Continuous source-media offsets

Continuous Vista time in this processing package is the concatenated supplied-media timeline, not wall-clock time across any recess/recording interruption.

| Component | Continuous offset | Visible court clock | Transition status |
|---|---:|---|---|
| VIDEO_01 | `VISTA 00:00:00.000` | approx. 09:46:53 → 10:46:53 | opening component |
| VIDEO_02 | `VISTA 01:00:00.614` | approx. 10:46:55 → 11:18:50 | near-seamless VIDEO_01→02 boundary (~2 s visible-clock difference) |
| VIDEO_03 | `VISTA 01:31:57.604` | approx. 11:58:22 → 12:23:21 | VIDEO_02→03 wall-clock interval ~39m32s remains unexplained; do not call it missing evidence without official record |

Total concatenated supplied-media duration: **7017.870875 s = 01:56:57.871**.

## Controlled audio masters

Generation command used for each source:

```bash
ffmpeg -i SOURCE_MKV -vn -ac 1 -ar 16000 -c:a flac -compression_level 5 OUTPUT_FLAC
```

No denoising, EQ, speech enhancement, VAD deletion or destructive filtering was applied.

| Derivative | Bytes | Duration | Format | SHA-256 |
|---|---:|---:|---|---|
| `CALIFICACION_VIDEO_01_AUDIO_MASTER.flac` | 111,768,701 | 3601.531063 s | FLAC mono 16 kHz | `f694d9e82c84afd7baeb6918edd03b85512a454291f99f5a785d5216359f1aa9` |
| `CALIFICACION_VIDEO_02_AUDIO_MASTER.flac` | 61,833,798 | 1917.666375 s | FLAC mono 16 kHz | `26914b186a79e20c6062761df0ba8549a62064b5bc8f0da94adb08610017580e` |
| `CALIFICACION_VIDEO_03_AUDIO_MASTER.flac` | 46,870,661 | 1500.589563 s | FLAC mono 16 kHz | `b88cb902d3c5024d8760b09fce7c4a65342d459a525f74e493ec555e7bc2723d` |

The extracted FLAC timeline is normalised. Mapping back to source-media zero is preserved as: VIDEO_01 `+0.039 s`; VIDEO_02 `+0.000 s`; VIDEO_03 `+0.046 s`.

## STT chunk manifest

Chunks contain **10 seconds overlap** after the first chunk of each component. No audio is discarded. Overlap must be deduplicated when the canonical transcript is assembled.

| Source | Chunk | Source-local range | Continuous Vista range | Bytes | SHA-256 |
|---|---|---|---|---:|---|
| V01 | `VIDEO_01_000000p000-002007p177.flac` | 0.039–1207.216 | 0.039–1207.216 | 37,344,169 | `044b7ccf49f1269b47263c707c2318088cac26a92a8a590e854e8383c55104f9` |
| V01 | `VIDEO_01_001957p177-004004p354.flac` | 1197.216–2404.393 | 1197.216–2404.393 | 36,815,807 | `b29932b55fb279a2b974323da70cab74ba64c14607009ff819aa2bf50f7768b1` |
| V01 | `VIDEO_01_003954p354-010001p531.flac` | 2394.393–3600.614 | 2394.393–3600.614 | 38,232,546 | `ff54fc73075ee9aab4a9a818b2969df5e156ed3cf31ff90301bd8bf50c26faf8` |
| V02 | `VIDEO_02_000000p000-001603p833.flac` | 0.000–963.833 | 3600.614–4564.447 | 31,246,024 | `74ef43053cba5ad9448afbd2189cfb10491de65b6edee8b9d8f3a14aa08daa89` |
| V02 | `VIDEO_02_001553p833-003157p666.flac` | 953.833–1916.990 | 4554.447–5517.604 | 30,916,997 | `3e215e9ac6dba5e8dbf71366b42ccc34720386dba21892b21eb9808685df8237` |
| V03 | `VIDEO_03_000000p000-001235p295.flac` | 0.046–755.341 | 5517.650–6272.944 | 23,506,576 | `39711fb37f515364255d85eb323956456b7b49897ba55a54578478b8d6b46c51` |
| V03 | `VIDEO_03_001225p295-002500p590.flac` | 745.341–1500.267 | 6262.944–7017.871 | 23,678,279 | `7041900c961cc188f3a3d4ccd2414e2b0cbd6cd9aad4bb186171fcb99fc5a374` |

## Custody boundary

The original MKVs and generated audio binaries are private evidential binaries and have **not** been copied into the public GitHub repository. The repository preserves exact identity, regeneration commands, hashes, chronology and processing state. Repository continuity is not provider-independent binary custody.

A future custody step should store the native MKVs and/or these exact derivatives in an approved private evidence vault and record the vault locator plus fresh hash verification. Until then, do not claim that the derivatives are durably stored outside the active processing runtime.
