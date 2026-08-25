# Fiscalía EG 112/2026 clarification + daily reference 24 - deployment closeout

**Control date:** 25 August 2026

**Status:** `MERGED / DEPLOYED / LIVE READBACK HASH-VERIFIED / NO EMAIL SENT`

## Source and merge

- PR: `#969`
- PR URL: `https://github.com/sbu001monterecco/por-derecho/pull/969`
- Remote source commit: `fa11ee445c756cf68ee161dee69ef3512935709a`
- Squash-merge commit on `main`: `0c21f1a2d201e7361c517d3c5216b2adf9d2e6cd`
- Merge time: 25 August 2026

The merge added the public-safe three-page EG 112/2026 clarification decree,
its complete page-accounted transcription, bilingual adjacent explanation and
the bounded CGPJ/TSJC provenance update for daily reference no. 24.

## Validation before merge

The rebased source state passed:

- `python3 scripts/validate_repository_preservation.py`;
- `python3 scripts/validate_publication_integrity.py`;
- `python3 scripts/validate_audience_experience.py`; and
- `python3 scripts/validate_fiscalia_dip2_ref24_eg112.py`.

The PDF workflow additionally verified three A4 pages, zero AcroForm fields,
zero signature widgets, no controlled private literals in extracted text and a
clean rendered review of every page.

## GitHub Actions and Pages

Pages workflow run `32830560890` used exact head SHA
`0c21f1a2d201e7361c517d3c5216b2adf9d2e6cd`.

- build job `97748062082`: `completed / success`;
- deploy job `97748148674`: `completed / success`;
- deploy completed at `2026-08-25T09:11:36Z`.

The ancillary `report-build-status` job remained queued when the independent
readback was performed. That reporting-job state is not represented as the
deployment result; the build and deploy jobs themselves succeeded and the
deployed bytes were independently recovered.

## Independent live readback

Cache-busted readback at `2026-08-25T09:16:32Z` returned HTTP 200 for all four
critical surfaces and matched the repository bytes exactly:

| Surface | Live URL | SHA-256 |
|---|---|---|
| Spanish dossier | `https://sbu001monterecco.github.io/por-derecho/es/fiscalia-dip-2-2026/` | `968a19448357aa6ca076e988f2d2382babbc91491d797e1132e7a9d36f1fd0c7` |
| English dossier | `https://sbu001monterecco.github.io/por-derecho/en/fiscalia-dip-2-2026/` | `2f895b850693860f03b7ed902dc35f5140bace01d26acb96851fcc736ac6e5e8` |
| Public EG 112 PDF | `https://sbu001monterecco.github.io/por-derecho/evidence/fiscalia/eg-112-2026/public-pdfs/decreto-aclaracion-eg-112-2026-23ago2026-public-redacted.pdf` | `fe9111aca4aa4cc82627af6c97a8408e3ed5e3db9e0382a6e302783f281b6783` |
| Public transcription | `https://sbu001monterecco.github.io/por-derecho/evidence/fiscalia/eg-112-2026/full-text/decreto-aclaracion-eg-112-2026-23ago2026-public-transcription.md` | `edcbeb9ca68ff33b0dbd8cb4bc9442c30f63d0db1ad570c0c7d72c0222bb919a` |

Both bilingual pages contained the controlled evidence marker
`EVID-2026-FISCALIA-EG112-ACLARACION-003`. The transcript readback is
byte-identical to the repository derivative. The PDF readback is byte-identical
and preserves the privacy-clean signature/contact treatment.

## Procedural boundary retained

The deployed page states:

- daily reference no. 24 is not represented as a NIG or confirmed proceeding;
- the CGPJ agreement of 10 July documents receipt and characterisation of the
  request to locate and preserve `control 24`, not its allocation;
- the TSJC agreement of 20 August documents a related but distinct
  CGPJ-to-TSJC receipt discrepancy, not the route of the 18 June complaint; and
- presentation is documented while subsequent allocation or TSJC destination
  remains unlocated.

## Communications boundary

No email, resend, forward, self-email or Gmail draft was created or sent by this
deployment step. The intended follow-up remains a recipient-specific,
source-bounded preservation and competence-screening draft subject to the
repository's exact final-authorisation gate.
