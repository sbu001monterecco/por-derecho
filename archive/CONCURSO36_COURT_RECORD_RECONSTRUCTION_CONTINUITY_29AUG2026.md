# Concurso 36/2012 — court-record reconstruction continuity closeout

Date: 29 August 2026  
Baseline main: `4b437dbee5ee979b9e3a9868ecd7d0e37505b181`  
Branch: `codex/concurso36-court-record-reconstruction-20260829`

## Objective

Convert the remaining court-record work into an autonomous, end-to-end reconstruction system rather than a narrative or keyword audit. Every material family must follow:

**party filing -> verified receipt -> court/LAJ act -> service -> review/appeal/queja -> finality -> implementation -> explicit residual gap**.

## First family materially closed

Primary LexNET/court copies now verify the 2022 appeal/queja/testimonio-finality family through the following nodes:

- 28-Feb-2022 LPB appeal: LexNET `202210473582179`; filing time 13:54:54; principal hash `094fbdbd52840f52f76afcad5ea55fee8c9a844c16205381cf9ea3984d29a0d4`; later identified as registration `1477/2022`.
- 2-Mar-2022 Aweswell appeal: sent LexNET `202210474270428`, ack `1202210474270428`; principal hash `a6768d02d0876867b0fdf9d5c58ae6f5f0b4a7a8bc7fd76620c40024b40c11ba`; later identified as `1512/2022`.
- 7-Mar-2022 CAM opposition: LexNET `202210475416241`; principal hash `d80918e44331e17a5c94e4e013201c640d4fa1955ad0ab9da9e7283c1f751860`.
- 9-Mar-2022 Auto: signed by Magistrado-Juez Alberto López Villarrubia; inadmitted both appeals and directed a ten-day queja route; electronic document `A05003250-3507d04a1d026d8373981d6add31646823908885`; notified 11-Mar under LexNET `202210476786626`.
- 29-Mar-2022 Aweswell queja to Audiencia Provincial: sent `202210481753993`, ack `1202210481753993`; principal hash `4c1838970f379a18711bafd2d20aec1e0244af105df634a14529a5d12bc3ec57`.
- 30-Mar-2022 notice to Mercantile Court: sent `202210482293471`, ack `1202210482293471`; requested avoidance of further prejudicial steps while queja remained pending.
- 4-Apr-2022 DIOR: LAJ Águeda Reyes Almeida joined the two queja notices and recorded them as `2275` and `2314/2022`; electronic document `A05003250-357d33adfb2c55ef416dd56d02b1649076726371`.
- 26-Apr-2022 Decreto on 14-Feb DIOR/testimonios/finality: dismissed LPB/Aweswell reposicion; treated the 15-Oct/26-Jan reposicion Auto as irrecurrible/firme; electronic document `A05003250-35127ecbb3101ef0a562bb848041650980940581`.
- 26-Apr-2022 Decreto on 11-Feb DIOR/protest: dismissed LPB reposicion on the same liquidation-phase appeal reasoning; electronic document `A05003250-35c4420e8dc3a3a7a92c73487a11650980920666`.
- 26-Apr-2022 DIOR: ordered EUR25 deposit refunds; electronic document `A05003250-353850865b4edb2b073ddff6c681650980516640`.

## Important analytical correction

This family is no longer properly described as judicial silence. It contains multiple affirmative adverse procedural/finality determinations. The remaining prosecutorial question is whether the full service, queja, finality and implementation chain was legally and factually coherent, including what the Audiencia Provincial did and what occurred before/after deed and registry implementation.

## Residual P0 for this family

1. LPB's own queja receipt and principal document.
2. Audiencia Provincial docket identity, section, admission and outcome for both quejas.
3. Exact 11-Feb and 14-Feb 2022 DIORs.
4. Exact testimonios issued and wording concerning purpose/recipient/finality.
5. Any direct revision against the 26-Apr Decretos and outcomes.
6. Finca-by-finca link from operative decision/testimonios to deed, presentation and registry effect.

## Autonomous governance added

- `CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md` is now the authoritative short-thread restart file.
- `assets/data/concurso36-court-record-reconstruction-v1.json` is the living closed-family registry.
- `publication-manifests/concurso36-court-record-reconstruction-20260829.json` carries publication and handoff state.
- `.github/workflows/validate-concurso36-court-record-reconstruction.yml` prevents loss of the core 2022 family, response taxonomy, handoff prompt and bilingual routes.
- `/es/concurso-36-2012-registro-procesal/` and `/en/insolvency-36-2012-court-record/` are the reader-facing control-room routes.

## Evidence governance

- A filing is evidence of the filing/request/allegation and, where controlled, its court-channel receipt; not proof of the factual allegation.
- A court/LAJ decision is evidence of what was decided; not proof of corruption, prevaricacion, collusion or malicious prosecution.
- `RESPONSE_NOT_LOCATED` is a production status, never proof of non-response.
- Adverse, protective and contradictory decisions remain visible simultaneously.
- LPB estate rights, Matkator rights and other third-party rights remain separate.
- No canonical v2 denominator until cross-supplement dedupe and response/finality/implementation pairing are materially complete.

## New-thread short prompt

`Continue the autonomous Concurso 36/2012 court-record reconstruction from CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md. Close the next P0 filing/decision/notification families end-to-end, update the repository and bilingual site through PR/CI/Pages, preserve all evidence boundaries and continuity governance, and leave the project deletion-safe and ready for the next short handoff.`

## Expired-upload boundary

Some native files uploaded into earlier ChatGPT threads have expired from the conversation file store. Their expiry does not invalidate repository/Gmail copies. Do not block autonomous work where those copies supply the same family. Ask for re-upload only when an expired native file itself is needed for a specific comparison, provenance or proof point.