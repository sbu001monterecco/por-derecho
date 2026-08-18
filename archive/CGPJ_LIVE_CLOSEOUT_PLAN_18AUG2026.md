# CGPJ live close-out plan — 18 August 2026

Purpose: force and independently verify a fresh GitHub Pages deployment of the existing bilingual CGPJ reader room, insolvency-estate supervision dossier and judge ledger after the unitary-supervision merge.

## Scope

Core ES/EN routes:
- `es/cgpj-comision-permanente-sala-lectura/`
- `en/cgpj-permanent-commission-reader-room/`
- `es/cgpj-supervision-masa-activa/`
- `en/cgpj-insolvency-estate-supervision/`
- `es/concurso-36-2012-magistrado-juez/`
- `en/insolvency-36-2012-mercantile-court-1/`

## Method

1. Merge a unique public deployment probe from current `main`.
2. Let the existing GitHub Pages source/deployment mechanism publish the new `main`.
3. Run the release-specific `Verify CGPJ unitary supervision live` workflow automatically on the merge push.
4. Poll the actual public Pages host with cache-busting requests until the probe and exact page markers return HTTP 200.
5. Preserve response status, final URL, byte length, SHA-256, ETag/Last-Modified and marker presence in a workflow artifact.
6. Only after a successful public-host run, advance the controlling publication manifest from `MERGED` to `LIVE_VERIFIED` and write the final thread-deletion continuity record.

## Safety

This close-out does not change substantive legal allegations or evidence classification. The deployment probe and verifier prove publication state only.
