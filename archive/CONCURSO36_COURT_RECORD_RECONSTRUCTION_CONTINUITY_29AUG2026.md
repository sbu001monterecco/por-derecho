# Concurso 36/2012 — court-record reconstruction continuity closeout

Date: 29 August 2026  
Baseline main: `4b437dbee5ee979b9e3a9868ecd7d0e37505b181`  
Branch: `codex/concurso36-court-record-reconstruction-20260829`

## Objective

Convert the remaining court-record work into an autonomous, end-to-end reconstruction system rather than a narrative or keyword audit. Every material family follows:

**party filing -> verified receipt -> court/LAJ act -> service -> review/appeal/queja/revision -> finality -> implementation -> explicit residual gap**.

## 2022 family — current controlled state

The bilingual control room now combines the base registry with `assets/data/concurso36-court-record-reconstruction-2022-appellate-supplement.json`, producing **20 verified/corroborated procedural nodes**.

### First-instance appeal / queja chain

- 28-Feb-2022 LPB appeal: LexNET `202210473582179`, later registration `1477/2022`.
- 2-Mar-2022 Aweswell appeal: sent `202210474270428`, ack `1202210474270428`, later `1512/2022`.
- 9-Mar-2022 Auto: judge-signed inadmission of both appeals and express ten-day queja route; electronic document `A05003250-3507d04a1d026d8373981d6add31646823908885`; notified under `202210476786626`.
- 29-Mar-2022 Aweswell queja: sent `202210481753993`, ack `1202210481753993`.
- 30-Mar-2022 notice to Mercantile Court: sent `202210482293471`, ack `1202210482293471`.
- 4-Apr-2022 DIOR: Mercantile Court records both queja notices as registrations `2275` and `2314/2022`.

### Audiencia Provincial

**LPB**
- Docket now controlled as **AP Las Palmas, Seccion Cuarta, Recurso de Queja 375/2022**.
- Signed 18-Apr-2022 providencia set study/vote/decision for 15-Jul-2022; electronic document `A05003250-3537998ec267692d6cc657c22ea1650359441838`, SHA256 `d0d8d6b04c8d9d6313aae7a7facc43415329590a8ca8533bf5b70486fd87c06d`.
- The later signed AP Auto 109/2022 expressly cites a **4-Jul-2022 Auto in LPB Queja 375/2022 in the same adverse legal sense** concerning non-appealability in liquidation.
- The signed 4-Jul LPB Auto itself is **not yet controlled**. Do not quote its exact dispositive wording/costs/finality until recovered.

**Aweswell**
- Docket controlled as **AP Las Palmas, Seccion Cuarta, Recurso de Queja 379/2022**.
- 11-Apr DIOR forms roll and requires EUR30 deposit cure; document `A05003250-3589ac38850aaaf0da291b3666e1649751371477`, SHA256 `40723f5a9ac3c34353cd84f2fa94a551d8c0c5adc561058234d166476d100e96`.
- 20-Apr DIOR confirms deposit cure and deliberation-ready status; document `A05003250-35a53c8ed3ac18e55462e200e5b1650531023141`, SHA256 `5f5644f8962815c9f2a79c0817dcdc4f45ffd0d086454927f9a07538d9fa0172`.
- **24-Nov-2022 Auto 109/2022** dismisses Queja 379/2022, imposes costs/loss of deposit, states no further appeal; document `A05003250-35d4ff0c0b259734c5ea7dc69411669385141492`, SHA256 `0b0f1cda0538bccf4dabedc30630b1ac7fe52f8950f32009589a3c444977b723`.
- The Auto expressly lists the underlying orders Aweswell sought to place before the AP, including the 2021 protection-of-masa, suspension, sale/adjudication and earlier decision families. Its dismissal closes that appellate route; it does **not** adjudicate the factual merits of every underlying allegation.
- 30-Nov DIOR records finality, testimony back to origin and archive; document `A05003250-3587babc6df3d2dbfc90404de381669892710841`, SHA256 `fe114e44d671ab3d8b174b66ad7e59b53c93c5a6d74bd0d15fb856e4852ae7df`.

### Direct revision against April LAJ Decretos

- 24-May DIOR records **four** revision applications against the two April Decretos: LPB registrations `3353/3354`; Aweswell `3361/3362`; requires deposit cure. Document `A05003250-35e99a49b9442d46e69baf90bea1653397333765`, SHA256 `446e14f799f452c4193504e36d7cedea4463ed4d7edac6a11917200176209152`.
- 2-Jun DIOR admits LPB revisions after deposit evidence; document `A05003250-35aa1421b22bb018d3d16aa1bee1654173342082`, SHA256 `35374e34069431be6710116e52a9e7278018ad45e6b0a3df2cfac12cccb0b0e2`.
- A 16-Jun providencia later inadmitted revision applications for supposed deposit failure.
- **13-Jul Auto 308/2022** verifies the deposits had actually been paid in form/time and annuls the 16-Jun inadmission; document `A05003250-35188b05fa34b49034efd3977fe1657718796252`, SHA256 `3d58128b693ce9ef17e331c3cb51f3ee5af88add3ced72f740ff846651860ffb`.
- 14-Jul DIOR admits Aweswell revisions; document `A05003250-3520a62213f4ca3ac1e1ed1cecb1657801330688`, SHA256 `821a5adec017a73e84eee17b00539232bc3dd609b89de7e69b841b4ded5fd83c`.
- CAM opposition and AC opposition/preclusion material is located in late July; final judge outcomes remain to be paired.

## Analytical corrections now locked

1. This family is **not judicial silence**. It contains multiple adverse procedural/finality decisions.
2. AP dismissal of queja is a **procedural appellate-access outcome**, not a merits adjudication of every underlying allegation.
3. Auto 308/2022 is a genuine **corrective/protective counterweight** and must remain visible.
4. The revision DIORs refer to Decretos dated `22/04/2022` while signed Decretos presently controlled are dated `26/04/2022`. Preserve as a traceability discrepancy until reconciled.
5. A later signed judicial decision can establish an earlier missing decision's existence/date/docket/legal direction, but does not permit invention of the missing decision's exact operative wording.

## Residual P0 — 2022 family

1. Exact signed 4-Jul-2022 AP Auto in LPB Queja 375/2022 + service/finality.
2. Exact LPB AP LexNET queja receipt/principal document.
3. Exact 11-Feb and 14-Feb 2022 DIORs and all testimonios issued under them, including addressee, purpose, finality wording and service.
4. Final judge outcomes of LPB/Aweswell direct revisions after 2-Jun/14-Jul admissions, with CAM/AC oppositions and later review/finality.
5. Reconcile 22-Apr versus 26-Apr Decreto date references.
6. Finca-by-finca bridge: operative decision/testimonios -> deed -> presentation -> Registry, including what occurred while review routes were pending.

## Autonomous governance

- `CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md` is the authoritative new-thread restart file.
- Base: `assets/data/concurso36-court-record-reconstruction-v1.json`.
- AP/revision supplement: `assets/data/concurso36-court-record-reconstruction-2022-appellate-supplement.json`.
- Renderer merges them without silently rewriting the base denominator.
- Manifest: `publication-manifests/concurso36-court-record-reconstruction-20260829.json`.
- Dedicated CI requires the 2022 AP/revision IDs, 20-node minimum, response taxonomy, corrective counterweight and handoff prompt.
- Reader routes: `/es/concurso-36-2012-registro-procesal/` and `/en/insolvency-36-2012-court-record/`.

## Evidence governance

- Filing = evidence of request/allegation and controlled receipt, not truth.
- Court/LAJ act = evidence of what was decided, not automatic proof of criminal misconduct.
- `RESPONSE_NOT_LOCATED` = production status, never proof of non-response.
- Adverse, protective, corrective and contradictory decisions stay visible together.
- LPB estate, Matkator and other third-party rights remain separate.
- No canonical v2 until cross-supplement dedupe and response/finality/implementation pairing are materially complete.

## New-thread short prompt

`Continue the autonomous Concurso 36/2012 court-record reconstruction from CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md. Close the next P0 filing/decision/notification families end-to-end, update the repository and bilingual site through PR/CI/Pages, preserve all evidence boundaries and continuity governance, and leave the project deletion-safe and ready for the next short handoff.`

## Expired-upload boundary

Some direct uploads from earlier ChatGPT threads have expired. Do not block autonomous work where Gmail/repository copies supply the same family. Request re-upload only if a specific expired original is itself necessary for a proof/provenance comparison.