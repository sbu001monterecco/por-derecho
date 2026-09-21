# Authority discovery and Red SARA/AGE register — live publication closeout

**Workspace:** `PD-WS-20260901-0002`  
**Publication:** PR [#1313](https://github.com/sbu001monterecco/por-derecho/pull/1313)  
**Reviewed head:** `b98f193b5beb952710387e2a9d9b9c081fa71d90`  
**Merge:** `4de5b4c739a5e982e7953723eb0f19e63151f83d`  
**Status:** `LIVE_VERIFIED_WITH_OPEN_EVIDENCE_GAPS`

## 1. Purpose and result

The public controlled search did not surface the first Intervención General response when searched by office, and a search for `184368/2026` fell through to broad year-only results. This release repairs discovery without changing the evidential status of any communication.

It adds:

- canonical-register ingestion into the public search, with exact formal-reference precedence;
- bilingual public-safe routes for Red SARA/AGE filings and incoming authority responses;
- deterministic read-only projection `PD-SP-REDSARA-AGE-FILINGS-001`; and
- regression controls for exact Intervención reference and office-name discovery, current response coverage, attachment-index boundaries and privacy.

`184368/2026` resolves to `PD-SP-EVT-0141`; office discovery returns the three controlled Intervención records `184368/2026`, `497011/2026` and `699645/2026`. The pre-existing public-authority module, `X-INT-004` crosswalk and `^` limitations remain unchanged.

## 2. Canonical scope and limits

`assets/data/institutional-communications-register-v1.json` remains the sole canonical communications register. The new Red SARA/AGE JSON is a deterministic public-safe projection, not a competing evidence ledger.

- **92** currently individualised `REGAGE` event rows are discoverable.
- **75** detailed baseline receipts carry controlled receipt metadata.
- **100** unique listed attachment filename/SHA-512 pairs are discoverable, with receipt-occurrence counts.
- **163** currently canonical incoming institutional events are searchable by stable ID, reference, office, date and controlled fields.
- The historic **97**-record RedSARA denominator remains **75 detailed receipts + one 22-record aggregate-only batch**. It is not a complete 97-row, duplicate-free receipt register.
- The 92 current event rows and the historic 97-record denominator are separate controlled representations; no unduplicated crosswalk is asserted.
- The public baseline does not establish a complete receipt-to-attachment mapping. No such mapping is inferred.

The connected-source census remains only a bounded discovery denominator. It does not convert every message/document into a reviewed response or establish universal completeness.

## 3. Evidence and privacy boundary

A Red SARA/AGE receipt proves only the stated presentation, time, registry destination and listed annex metadata. An institutional response proves only the act, routing, notice or boundary stated in its source. Neither alone proves downstream delivery, incorporation, examination, decision, reliance, payment, effect, causation, intent, offence or guilt.

The release does not publish native receipt bundles, private emails, direct contact details, provider identifiers/locators, unredacted private attachments or third-party source material. Criminal responsibility does not propagate through a filing, office, authority tier, ACTA, referral or funding track. `^` remains identity/provenance only.

## 4. Validation, deployment and exact public readback

The PR suite completed **26/26 success**. It included the exact rendered browser smoke (`Validate unitary public shell` run `33509931303`), institutional-communications continuity validation, privacy audit, publication-integrity gate, audience-experience validation and reader-journey render.

GitHub Pages deployment `6201863449` for the exact merge succeeded at `2026-09-01T13:08:22Z`; its deployment action was [run `33511479330`, job `99868148861`](https://github.com/sbu001monterecco/por-derecho/actions/runs/33511479330/job/99868148861).

Cache-busted live readback returned HTTP 200 and exact SHA-256 equality with the merged source for:

| Public object | SHA-256 |
|---|---|
| EN authority register | `09f804cfed02070ba13935586690f321af0273f97649fd5fe0dccbaa3c1a4474` |
| ES authority register | `a38da7fbff95c3f617eb357e3b9742c447df1505e6dbb927795c556c0945ab37` |
| authority-register runtime | `9b2123d4c2d698fe42b6d24f5584178414793410d8de651e0ea52c28f9ccb092` |
| authority-register CSS | `66e906ea30be7c99a2eb1b067f9d65c5d3a105ec7c2cc08eac061e00f4a55349` |
| Red SARA/AGE projection | `9e4a09a15983e3508288d6785cac1c6e3c6c0da722a72c32b82aff9065ad3c95` |
| public search runtime | `dd32cd87b601126e42e534e5bd916e6418547a84191b601ff6f7394145131e84` |
| canonical communications register | `04eda9a473d07419c1d1d0941b9123d1497f7329366998a9f4cf76221910bbed` |

## 5. Open critical work

Publication does not close `PD-GAP-UCF-001`–`016`. The immediate P0 order remains:

1. native Community call/service, title/coefficient, proxy, debt, vote, originals/variants and the 20-Nov-2018 lifecycle (`001`–`008`);
2. document-specific ACTA → RIC/RICPE/incentive/ERDF/works bridge and Yaiza/Cabildo/SAIP files (`009`–`010`);
3. property-by-property title, cancellation, use, income and benefit reconciliation (`011`);
4. actor-by-actor criminal threshold (`013`), including contrary/lawful explanations; and
5. source-by-source authority propagation plus the Intervención → Commission → Justice/programme chain (`015`–`016`).

The specific filing-register acquisition gap is source-proved individual rows/status exports for the 22-record aggregate-only batch and any permitted receipt-to-attachment mapping source. Do not manufacture rows or mappings from the aggregate denominator.

## 6. Continuity notes

The local Git remote lacked credentials and rejected a direct push before any external change. The connected repository integration then created the reviewed branch and PR. This is a tooling fact only; it did not alter sources, filings, authorities or evidence status.

No authority was contacted, no filing/email/portal action was performed, and no private source was disclosed. Continue from `archive/handoffs/2026-09-01-authority-discovery-redsara-workspace-handoff.md`, current `main` and the named canonical controls rather than this chat.
