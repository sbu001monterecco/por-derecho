# LPB definitive texts / liquidation baseline — activation record

**Activated for branch review:** 20 August 2026  
**Current lifecycle state:** `REMOTE_SOURCE` → branch implementation prepared; PR, CI, merge, deployment and public-edge read-back remain to be recorded  
**Scope:** Luchy Playa Blanca, S.L.U., Concurso 36/2012 — 2013 report/inventory, 2016 definitive texts and creditor list, 2018 holder modification and liquidation plan.

## Purpose

Promote the definitive-text baseline from later reconstruction/secondary references to a controlled primary-source chain and propagate that promotion through the repository, machine-readable case models and bilingual public website without publishing unredacted court PDFs.

## Primary sources controlled

- 15-Jan-2013 AC report and inventory — 37 pages — SHA-256 `a48441aafcddd63ae792f46fc88188b17a32cecba943b8db956587ecd8c8a073`.
- 28/29-Apr-2016 AC definitive-text filing — 6 pages — SHA-256 `b62970419a699f07c48777c300f9259721df2072c0f8739aa9aa9d2db9e9aa79`.
- 28/29-Apr-2016 definitive creditor list / Annex 1 — 1 page — SHA-256 `9004df2fbc361b5f6a4b7042014e025b7643520f68c863c5835f572bdd071c31`.
- 8-Feb-2018 order modifying the credit holder — 3 pages — SHA-256 `22f4149590ef80e050640c9691b7c34dc3a5306f87e2d727bc4f852990980b88`.
- Feb-2018 liquidation plan — 15 pages — SHA-256 `767b5966bc2d380a35633b3dcb884256e0067cc3e4be3b07e5cf5d2f947b1a78`.
- 16-Apr-2018 liquidation-plan order — 7 pages — SHA-256 `2de1527a738658252f81fd3e402622f677280aaed735e5ef117d44c4a06dcd05`.

The raw files remain outside the public repository because they contain signatures, identifiers and procedural data unnecessary for the public explanation.

## Findings promoted to primary-source verified

1. The 2016 filing expressly introduced modifications into the inventory, creditor list and report and elevated the prior report to definitive status except where expressly modified.
2. Its main tables record active mass **€19,486,498.94**, passive mass **€10,125,752.00** and claims against the estate **€304,779.42**.
3. The separate definitive creditor list records specially privileged claims of **€857,373.81** and **€8,194,877.88**, totalling **€9,052,251.69**.
4. The 8-Feb-2018 order changes the holder from Promontoria to CAM at those recognised amounts; assignment does not by itself enlarge the quantum.
5. The liquidation plan expressly refers to the inventory annexed to the AC report and elevated to definitive status.
6. The plan identifies LPB's perimeter as 159 apartments, 29 premises and two pool/solarium properties.
7. The definitive-text classification, mortgage responsibility, later payable debt, better-bid threshold, non-cash consideration and actual realisation/accounting outcome are distinct quantities.

## Internal consistency questions preserved

- main 2016 tables versus materially different figures in a later paragraph;
- erroneous-looking reference to an Article 75 report of 1-Feb-2011 rather than the controlled LPB report of 15-Jan-2013;
- 28-Apr filing date versus 29-Apr electronic signature;
- three-cent differences between the summary table and separate creditor list.

These are certification/traceability questions, not findings of misconduct.

## Public implementation

New canonical routes:

- `/es/textos-definitivos-lpb-base-liquidacion/`
- `/en/lpb-definitive-texts-liquidation-baseline/`

Cross-site propagation is implemented through `assets/lpb-definitive-texts-unitary-20260820.js`, including:

- a primary-source promotion panel on the 2022 adjudication pages;
- concise links from credit, AC, insolvency, valuation, notarial, Registry, judge/LAJ and corrections routes;
- an update card on the home, updates and Case Control Room routes;
- runtime protection against the superseded phrase that the definitive texts themselves remain wholly unlocated.

Search/discovery is provided by the dedicated sitemap and controlled route registry.

## Repository implementation

Canonical internal control:

- `archive/LPB_TEXTOS_DEFINITIVOS_LIQUIDATION_BASELINE_UNITARY_DIGEST_20AUG2026.md`
- `assets/data/lpb-definitive-texts-v1.json`
- updates to the AC accounting bridge, correction register, missing-evidence register, maintenance matrix, storyline, bootstrap and public reconstruction models.

## Evidence still open

1. Complete court-certified definitive-text bundle and docket index.
2. Separate detailed Annex 2 claims-against-the-estate schedule.
3. Filing receipt and decision joining/receiving the definitive texts.
4. Complete later modification chain.
5. Credit calculation and legal basis as at 21-Feb-2022.
6. Final accounts, ledger, bank trail, liquidation balance and conclusion record.
7. Property-by-property notarial and Registry implementation.

## Publication rules

- No raw private PDFs or personal identifiers are committed.
- No universal-nullity, automatic-surplus, automatic-cancellation or criminal finding is asserted.
- Apparent inconsistencies are preserved as questions requiring certified sources.
- Matkator and third-party assets remain separate from LPB's estate.
- Primary evidence and date-specific legal advice control over this digest.

## Lifecycle gate

The controlling sequence is:

`DRAFT → REMOTE_SOURCE → PR_OPEN → CI_GREEN → MERGED → DEPLOYED → LIVE_VERIFIED → DELETION_SAFE`

Use `BLOCKED_RECOVERY` if any claimed stage cannot be objectively proved. This record must be updated after merge and live verification with the PR number, merge SHA, workflow runs, public-edge markers and deletion-safety outcome.