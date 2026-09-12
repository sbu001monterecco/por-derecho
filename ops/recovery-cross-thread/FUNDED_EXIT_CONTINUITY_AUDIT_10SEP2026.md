# Funded-exit continuity audit — 10 September 2026

Control: `PD-FUNDED-EXIT-CONTINUITY-20260910`

Status: **continuity / governance record only — no independent public-release effect**.

This record exists so a future Por Derecho / Project Sun Rock thread can recover the current Daniel Irigoyen / ONA funded-exit state from GitLab without depending on chat history or stale merge-request descriptions.

## Authority and moving baseline

Protected GitLab `main` is the current source authority. At the moment this tracked continuity branch was created, `main` was observed at:

`fed33309061eb90da4f756ace49f1d9b9923928f`

This is a moving baseline. Every future mutation must refresh `main` before rebasing, merging, cherry-picking, generating a release inventory or publishing.

## Authoritative funded-exit deployment

The authoritative current-main funded-exit convergence is **MR !185**:

- source branch: `release/ona-funded-exit-track-design-20260909-v2`
- target: `main`
- merge SHA: `872a0256a585179125ac261fb749ffa01ee2041d`
- exact-head MR pipeline: `2834519742` — SUCCESS
- post-merge `main` pipeline: `2834530810` — SUCCESS
- `verify-publication-controls`: job `16403995644` — SUCCESS
- `verify-recovered-loader`: job `16403995645` — SUCCESS
- `verify-gitlab-public-frontend`: job `16403995646` — SUCCESS
- `verify-ricpe-static-readers`: job `16403995647` — SUCCESS
- `publish-reviewed-master`: job `16403995667` — SUCCESS
- `verify-gitlab-pages-live`: job `16403995668` — **LIVE_VERIFIED**
- reviewed public inventory SHA-256: `74e108ae58d779a66a88a66b551e5e6d3d3285d65c5f2a6f3c6da7100abdc216`

MR !185 replayed the durable reviewed Daniel/ONA/funded-exit payload onto then-current `main` while preserving newer release controls. It did not replay stale cumulative approvals or obsolete release machinery.

## Six funded-exit routes present on current `main`

The continuity audit confirmed all six intended bilingual routes exist on current protected `main`:

| Route | Current-main control observed during audit |
| --- | --- |
| `en/ona-hotels-insolvency-exit-36-2012/index.html` | content SHA-256 `bf41d9eb35a9560f25cef76220143b4ad95b656abf7dd6c06e433c255a6609fa`; blob `43d11fc497d1a46b5ae78ce28c1c81a32c999b17` |
| `es/ona-hotels-salida-concurso-36-2012/index.html` | content SHA-256 `60ba4570403564c44b4e74785b7faf21b830504866d5043d030225e9ff7ba8a4`; blob `63a3bd536c3d04c4add930be7e26cc19caced5d6` |
| `en/daniel-irigoyen-insolvency-knowledge/index.html` | blob `7d81dbdcd913dbba3b18937a3bbf03696961eed5`; exact reviewed specialist blob |
| `es/daniel-irigoyen-conocimiento-concursal/index.html` | blob `7a3ff4a046c01028238ec906e0d5a641c5a31078`; exact reviewed specialist blob |
| `en/pre-7-june-2018-funded-ona-exit/index.html` | blob `2d301e1d9bdfcc254371da83fc9f486e9a22f7c4` |
| `es/salida-financiada-ona-antes-7-junio-2018/index.html` | blob `04180652d754b24bfac959cb24e40832feb9f22e` |

The two pre-7-June cut-off readers are therefore **not missing**. Any earlier handoff saying they still need to be created and deployed is superseded by this record and the !185 deployment receipt.

## Superseded development lanes

### MR !156

`codex/daniel-owner-funded-exit-20260909` / MR !156 was the historical specialist source lane. During this audit it was 265 commits behind current `main` and retained a failed-rebase history. Its durable payload has already been converged through !185.

MR !156 has therefore been explicitly marked **superseded and closed**. Preserve it only as a historical/source reservoir. Do **not** rebase, merge or replay its stale release machinery.

### MR !186

`release/daniel-ona-funded-exit-successor-20260909` / MR !186 was an intermediate safe-successor lane. It was correctly closed after repository-state verification established that !185 had already completed the current-main convergence and LIVE_VERIFIED deployment.

Neither !156 nor !186 is current release authority.

## Substantive model that must remain stable

The funded-exit layer is part of the unitary criminal/prosecutorial-first evidence architecture, but it must remain source-qualified and falsifiable.

Preserve these distinctions:

1. **Owner-led architecture.** The owners initiated and coordinated the effort; ONA/Clubotel was the intended operating anchor within that architecture, not automatically the lender or funder.
2. **Daniel Irigoyen's capacity.** Daniel acted as lawyer/professional adviser. His former judicial background does not make him the judge, Insolvency Administrator or judicial decision-maker in this matter.
3. **Professional report versus court record.** A contemporaneous first-person/professional account of a meeting proves what the source reported. It is not automatically a judicial minute, order, filing, adoption or implementation.
4. **Transaction-status discipline.** A term sheet, LOI, binding conditional offer, reported approval, signed operating agreement, definitive facility agreement, closing and drawdown are distinct evidential states.
5. **Temporal discipline.** The controlled pre-7-June dossier ends at the close of 6 June 2018. Later June, August, September and 2019 developments must not be backdated into that cut-off state.
6. **Estate/perimeter discipline.** LPB, the insolvency estate, other unit owners, Community governance, CEXP/operating interests and the whole hotel are not interchangeable legal/economic perimeters.
7. **Causation discipline.** The allegation that adverse conduct sabotaged or materially impaired the funded exit remains an allegation to be tested condition-by-condition and actor-by-actor. Chronology, proximity, institutional receipt, later title or later economic benefit do not by themselves prove knowledge, intent or causation.

## Remaining funded-exit work

The public-page deployment is complete. Remaining work is **evidence closure and graph enrichment**, especially:

- condition-by-condition performance / readiness / prevention / waiver / expiry / causation ledger for each funding and operating route;
- certified post-13-June filing, annexes, LexNET transmission/receipt/allocation/service/treatment chain;
- Insolvency Administrator debt certificate/update, exact figure and timing;
- definitive facility, conditions precedent, closing, drawdown and implementation records for each route;
- Cuatrecasas implementation/closing workstream records, warnings, deadlines and document ownership;
- certified Clubotel personation, opposition and ruling chain;
- route-specific lender/counterparty reasons, preserving lawful alternative explanations and contrary evidence;
- mapping into canonical propositions and prosecutorial links without upgrading preparation→filing, receipt→examination/adoption, duplicate copy→independent corroboration, graph proximity→agreement/guilt, or later benefit→prior knowledge/intent.

## Continuity routing

Issue #13 remains the orchestration/continuity hub. The 10 September 2026 supersession note is GitLab note `3812631683`.

Future work should start from current protected `main`, treat !185 plus this record as the funded-exit deployment authority, and use !156/!186 only for historical provenance when needed.

A newer unrelated `main` pipeline or later site release does not invalidate the historical !185 LIVE_VERIFIED receipt; it simply means future publication claims must also be bound to the newer exact `main`/release receipt when relevant.
