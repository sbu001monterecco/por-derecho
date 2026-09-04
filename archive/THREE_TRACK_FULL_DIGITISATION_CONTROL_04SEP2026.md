# Three-track full digitisation control — 4 September 2026

**Control ID:** `PD-THREE-TRACK-DIGITISATION-20260904-01`  
**Repository:** `sbu001monterecco/por-derecho`  
**Base remote main:** `b8ded173b06f17aaf91569f051dd11e621b139ae`  
**Working branch:** `chatgpt/three-track-full-digitisation-20260904`  
**Publication state at creation:** branch implementation; PR/merge/deployment/live readback pending.

## 1. Purpose

This control implements one public reader layer across three separate procedural tracks arising from the same Sun Park / Concurso Ordinario 36/2012 evidential matrix:

1. **DP 1901/2026 / Control 21 / NEXUS 36** — private-actor layer.
2. **DP 1956/2026 / Control 22** — Insolvency Administrator layer.
3. **Control 24** — judge-related complaint/notitia layer; formal criminal allocation and current judicial status remain unverified.

The three tracks are interlinked by shared events and evidence, not merged procedurally. No relationship transfers knowledge, intent, causation, guilt or liability.

## 2. What “full digitisation” means in this release

For the controlling textual sources used here, every source page has been processed through the available native text layer and indexed into a structured public-safe digest. The public site does **not** publish the raw private pleadings. Personal identifiers, signatures, private addresses, private contact details, verification codes and protected/private evidence remain outside public Git.

This release therefore distinguishes:

- source-byte preservation in the authorised private source system;
- source identity, page count and SHA-256;
- complete text-layer processing;
- structured section/module indexing;
- public-safe editorial digest;
- visual contextual narration across the three tracks.

It does not claim visual/manual verification of every source page unless separately recorded.

## 3. DP 1901/2026 source control

### Base complaint

- Literal source: `01_NEXUS_36_DENUNCIA_PENAL_ACTUALIZADA_PRESENTACION_25JUN2026.pdf`
- Pages: **69**
- SHA-256: `cb2ea7e6a206be97e30d28e92c330f3e40ece1d18d9964b38f9a5fd05a36c3f1`
- Reported filing date: **25 June 2026**
- Internal/presentation label: Control 21 / NEXUS 36
- Public raw source: **not published**

### 9 July expansion

- Literal source: `CONTROL21_Ampliacion_JDAM_LPAM_AcostaMatos_09JUL2026_FINAL_CONSOLIDADA_FILE_THIS_09JUL2026.pdf`
- Pages: **7**
- SHA-256: `436ffdddd8c9584a1e907cb25f1fbd9f27b82e7c6976c785fdcf09f535f3c9b9`
- Reported filing date: **9 July 2026**
- Boundary: filename words such as `FILE_THIS` are not filing proof; filing status remains source-controlled.

### Current procedural presentation

The existing DP 1901 public route records NIG `3501643220260016977`, position no. 6 of the Investigation Section of the Court of Instance of Las Palmas de Gran Canaria, and a located 12 July 2026 providencia giving the Ministerio Fiscal five days to report on admission in relation to DIP 2/2026. That providencia is not promoted into a later merits decision.

The full-digitisation layer must preserve the five-private-actor perimeter already controlled elsewhere and must not import the Insolvency Administrator or the insolvency judge as additional private defendants by association.

## 4. DP 1956/2026 source control

### Base complaint

- Literal source: `01_Denuncia_Penal_AC_LPB_Sun_Park_AC-FINAL_17JUN2026.pdf`
- Pages: **55**
- SHA-256: `b11f10e7410f922a8cd1796ea462ea7ea20d555b7308e4481f2cb23732b1002b`
- Document date: **17 June 2026**
- Reported filing date: **18 June 2026**
- Presentation locator: **Control / daily reference 22**
- Public raw source: **not published**

### Procedural identity/status

- Procedure: `DP 1956/2026`
- NIG: `3501643220260016826`
- IUP: `LI2026016921`
- Organ: Plaza n.º 1, Sección de Instrucción, Tribunal de Instancia de Las Palmas de Gran Canaria
- Controlled current status: **sobreseimiento provisional communicated 21 July 2026**

Control 22 and DP 1956/2026 remain separate identifiers linked by the available source chain. The provisional dismissal is not an acquittal, `sobreseimiento libre` or merits exoneration.

The complaint's source literals and anomalies remain preserved. No diplomatic transcription may silently correct an internal `30/2012` reference to `36/2012` or repair source numbering without an editorial note in a separate normalised layer.

## 5. Control 24 source/status control

The existing Control 24 digitisation remains part of this release:

- signed package: **79 pages**;
- principal complaint plus selected annexes;
- reported presentation: **18 June 2026** before the Decanato;
- daily/presentation locator: **24**;
- legal nature: denuncia / `notitia criminis`, **not formal querella**;
- dependent supplement: **10 pages**, presented 25 June 2026;
- formal assigned court, NIG, DP number and present criminal-court status: **not primary-verified**.

The CGPJ 169/2026 reporting/appeal relationship is a separate institutional link. It does not fill the missing criminal allocation/status field.

## 6. Shared-event reader model

The public visual layer uses six recurring events/documents to explain why the three tracks are connected but not the same proceeding:

| Shared event/document | DP 1901 / private actors | DP 1956 / AC | Control 24 / judicial layer |
|---|---|---|---|
| Community authority / debt / voting | alleged creation/use | knowledge, verification, reliance, reporting | judicial notice/supervision/decision response |
| 7 June 2018 material control | actor-specific private conduct | knowledge, preservation, authority, restoration | notice/protective requests/later decisions |
| 2018 funded exit | knowledge, motive, interference, benefit | estate duty, payoff, facilitation, accounting | judicial knowledge, conditions, protection, decision sequence |
| 28 Nov 2018 OB REM / €400k + 24 Oct 2019 non-validation | participation/benefit/downstream use | authority, safeguarding, accounting, restoration | non-validation, implementation and later consistency |
| credit / threshold / 2021 bidding / 2022 adjudication | offer, access, information, beneficiary | calculation, reporting, equality, implementation | scope, res judicata, competition, final decisional bridge |
| HNT / MYND / RICPE / later operation | downstream control/commercialisation/benefit allegations | later evidence only where relevant to AC-specific issues | later context does not establish historical judicial knowledge |

The controlling reader chain is:

`ACTOR → CAPACITY → EVENT → SOURCE → DECISION/OMISSION → ASSET/RIGHT → CONSEQUENCE → CONTRARY/ALTERNATIVE → OPEN PROOF`

## 7. Public implementation

Machine-readable control:

- `data/three-track-full-digitisation-20260904.json`

Contextual visual layer:

- `assets/control-22-24-interlink-20260904.js`

The existing `assets/site.js` loader already loads that contextual asset. The revised asset now includes DP 1901/2026, DP 1956/2026 and Control 24 as first-class nodes and adds the full contextual matrix directly to the relevant pages while preserving their existing substantive text.

Primary routes:

- `/es/dp-1901-2026/` / `/en/dp-1901-2026/`
- `/es/dp-1956-2026/` / `/en/dp-1956-2026/`
- `/es/control-24-denuncia-juez-concurso-36-2012/` / `/en/control-24-insolvency-judge-complaint-36-2012/`

## 8. Publication/evidence boundaries

- A filed complaint proves that an allegation/request was made, not its truth.
- A later registration, operation, financing, investment or public-support event does not validate predecessor authority or title.
- An adverse/provisional procedural outcome is preserved with equal visibility.
- A source missing from the mastered corpus is not proved nonexistent.
- Related does not mean accumulated.
- Shared evidence does not mean shared responsibility.
- Public publication is not filing, service, official receipt or personal notice.

## 9. Remaining finite gaps

1. DP 1901: complete certified docket and final post-12-July status; certified incorporation inventory for the base and 9 July expansion.
2. DP 1956: official bridge/inventory connecting the 18 June Control 22 presentation to the complete DP 1956 docket; exact material incorporated before the provisional-dismissal order; filing status of any appeal must remain source-controlled.
3. Control 24: certified Decanato/reparto trail, current custodian, assigned organ, NIG/proceeding number if any, and current judicial disposition.
4. Cross-track: official source for each claimed formal incorporation of shared evidence into more than one proceeding.

## 10. State at this record

- source retrieval: completed for the controlling DP 1901 base, DP 1901 expansion and DP 1956 base used in this release;
- text-layer processing: completed for those sources;
- structured public-safe control: created;
- contextual visual layer: updated;
- PR/merge/Pages/live readback: **pending at the time of this record**.
