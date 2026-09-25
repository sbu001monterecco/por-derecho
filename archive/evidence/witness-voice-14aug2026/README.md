# Full working transcript preservation — 14 August 2026 voice corpus

> **PRIVACY REMEDIATION NOTICE — 25 August 2026:** this directory is tracked in a public repository. BZip2/Base64 packaging is encoding, not access control, and must not be described as a private or backend vault. No new full private voice transcript may be committed in this form. The existing payload remains preserved pending an expressly authorised, history-aware privacy review; do not decode, quote, republish or use it as a public source merely because it is technically recoverable from Git. The controlling prospective rule is `archive/declarations/VOICE_TO_TEXT_STATEMENT_OF_FACT_AND_TRUTH_PROTOCOL_25AUG2026.md`.

**Repository role:** backend evidentiary preservation package  
**Public witness label:** witness within Gil Marer's personal and business perimeter — identity reserved  
**Source date:** 14 August 2026  
**Transcript status:** complete working transcript; timestamped; not forensic, certified, signed or personally ratified  
**Website status:** not reproduced as public HTML

## What is preserved

The adjacent Base64 file is a lossless BZip2 package containing the complete working transcript used for Declaration 002. It preserves every transcript line and timestamp exactly as produced, including unclear, phonetic and potentially inaccurate passages. It is an evidence-control copy, not a corrected quotation source.

- Reconstructed filename: `WITNESS_VOICE_FULL_WORKING_TRANSCRIPT_14AUG2026.md`
- Exact uncompressed size: `57,048` bytes
- Exact uncompressed line count: `457`
- Exact uncompressed SHA-256: `19e654ae03c2afeadc1a507549854a15129c20e10da29bb941fe86fb3c92ba88`
- BZip2 size: `16,404` bytes
- BZip2 SHA-256: `a8ff24854793ea00d5f37f2a18cef182463157c09e35585bd0607703bc28b4eb`
- Base64 payload size: `22,214` bytes
- Base64 payload SHA-256: `52f6486e34397024f8247002911b7e444695ff6d489e9cc22a7ea35da532cdf8`

The package covers the full transcript of sixteen unique messages attributed in the working record to the private witness. The transcript itself records:

- included message headings for `WA0005`, `WA0007`, `WA0009`–`WA0021`, with the original earlier/later-upload distinctions;
- exclusion of `WA0003`, `WA0006` and `WA0008` as different-speaker messages;
- removal of one exact duplicate: the later `WA0013` upload duplicated the earlier `WA0012` recording;
- approximate combined included duration of `1:00:13`.

## Reconstruction and verification

From this directory:

```bash
base64 --decode WITNESS_VOICE_FULL_WORKING_TRANSCRIPT_14AUG2026.md.bz2.b64 \
  | bzip2 --decompress --stdout \
  > WITNESS_VOICE_FULL_WORKING_TRANSCRIPT_14AUG2026.md

sha256sum WITNESS_VOICE_FULL_WORKING_TRANSCRIPT_14AUG2026.md
```

The resulting SHA-256 must equal:

```text
19e654ae03c2afeadc1a507549854a15129c20e10da29bb941fe86fb3c92ba88
```

A local round-trip test performed before repository upload reconstructed a file byte-identical to the retained source and reproduced that hash.

## Evidential and privacy boundaries

1. This package preserves **transcript text**, not the native Opus audio or its messaging-platform metadata.
2. Literal quotation must be checked against the relevant original audio and timestamp. The transcript contains speech-recognition errors and unresolved wording.
3. The public declaration and website retain the functional anonymisation rule. The package is not authority to identify the private witness publicly or to confuse that witness with Laura Patricia Acosta Matos (LPAM).
4. The native audio/export manifest, per-file hashes, sender/recipient metadata and formal authentication remain separate custody tasks.
5. No allegation in the transcript is converted by preservation into an adjudicated fact, professional finding or criminal conclusion.

## Connected repository control

- [`Declaration 002`](../../declarations/002_WITNESS_GIL_PERIMETER_RICPE_VOICE_20260815.md) preserves the controlled first-person synthesis, source limits and action matrix.
- The live RICPE/Sun Park dossier remains a source-led public summary. It does not reproduce this complete working transcript.

## Deletion-continuity rule

Once this payload, this manifest and the updated Declaration 002 are retained in a durable Git commit, the originating ChatGPT thread is not the sole holder of any transcript text. Deleting the thread does **not** close the open native-audio hashing and authentication workstream.
