# Continuation prompt — 28-source Sun Park digitisation, missing-source acquisition and bilingual publication

Use this prompt in a fresh working thread. It is deliberately executable and source-constrained.

---

You are continuing the Por Derecho / Project Sun Rock evidence-publication repository. First inspect the current `main`, all open draft PRs touching the same files, the live Spanish/English routes, source manifests, the Missing Evidence Register and validators. Do not assume a draft branch is merged or live. Preserve concurrent work and never overwrite unrelated changes.

## Objective

Reconcile, preserve, digitise and publish the controlled **28-upload / 26-unique-binary / 25-documentary-item** Sun Park corpus. Extend the existing evidence architecture; do not create a parallel archive. Preserve originals privately. Public Git may contain only public-safe metadata, hashes, redacted searchable transcripts, neutral source cards and reviewed raster derivatives.

Controlling register:

`archive/SUN_PARK_28_UPLOAD_SOURCE_DIGITISATION_AND_PUBLICATION_CONTROL_23AUG2026.md`

Machine manifest:

`assets/data/sun-park-28-upload-source-manifest-v1.json`

Canonical missing-source namespace:

`ME-PDFSCAN-001`–`ME-PDFSCAN-031`

## Non-negotiable source logic

For every proposition use one of:

`verified fact | source statement | party allegation | expert opinion | inference | procedural status | adjudicated holding | open question`.

Keep these distinctions explicit:

- relationship ≠ evidential relevance ≠ knowledge ≠ responsibility;
- complaint/filing ≠ receipt ≠ investigation ≠ finding ≠ final outcome;
- authorisation ≠ implementation;
- recognised insolvency credit ≠ mortgage ceiling ≠ better-bid threshold ≠ deed consideration ≠ Registry value ≠ surplus;
- LPB estate property ≠ Matkator property ≠ CAM property ≠ other third-party units ≠ the whole mixed-ownership complex; and
- a confidential draft expert opinion ≠ a signed final report ≠ a court-adopted valuation.

Never use editorial filename labels such as `DeudaFalsa`, `Destruccion Masa`, `Entrada ilegal`, `No-Swap` or `1240-2011` as findings or canonical titles.

## Fixed corpus corrections

1. `Juicio Desahucio por Precario 1240-2011.pdf` is an exact duplicate of `Demanda Desahucio Minorias 1260-2011.pdf`, SHA-256 `407a38eb...`; `1240` is a false alias.
2. The two 1-March-2018 photo PDFs are exact duplicates.
3. The two February-2021 CAM prints are variants of one opposition.
4. There are two different Autos dated 24-February-2021:
   - `C36-JUD-2021-02-24-001` / `MAT-008`: preservation/inspection reposición; four pages; partial allowance limited to reasoning, denial maintained.
   - `C36-JUD-2021-02-24-002`: liquidation extension; two pages; one-year extension.
5. AP Sentencia 89/2014 ordered eviction of CEXP and Monterecco from the claimant side's eighteen units and applied veil-lifting on its stated facts. It did not adjudicate the whole hotel or later conduct.
6. The 16-April-2018 Auto numerically states EUR 400,000 but does not state/adopt the Actúa values EUR 9.776m / EUR 7.097m / EUR 6.608m. Do not reproduce the confidential draft's contrary overreading as a judicial holding.
7. The Valencia `DOC 7 _ Liquidaciones` file is a 2008 bank/interest/hedge receipt exhibit, not a Concurso liquidation act.

## Work modes

### `AUDIT_ONLY`

Hash every supplied file; record bytes/pages/encryption/text state; render every page; detect duplicates/variants/misnames; compare against repository custody and route manifests; report conflicts without writing.

### `ACQUIRE_AND_DIGITISE`

Run only the finite `ME-PDFSCAN-*` acquisition batches. For each native source:

1. preserve original filename and native binary outside public Git;
2. calculate SHA-256 immediately;
3. record custodian, acquisition date, MIME/type and parent/annex/variant/duplicate relation;
4. export email as RFC822/Takeout with headers, MIME and attachments—not print view alone;
5. scan paper in colour at 300–400 dpi including backs, covers, stamps, envelopes and blank separators;
6. OCR page-faithfully with page markers and explicit `[illegible]`, `[handwritten]`, `[duplicate source page]` and `[redacted]` tokens;
7. manually compare OCR to rendered pages; and
8. update the existing gap row with a bounded negative-search log when no result is found.

### `PREPARE_PUBLIC_SAFE`

Prepare, but do not merge:

- full redacted substantive transcripts for signed court/Fiscalía acts;
- balanced source cards for party filings, always paired with the counter-position and official outcome;
- metadata/limitations only for confidential drafts;
- digest only for private email;
- hash-only treatment for bank-account exhibits; and
- no public photo gallery until originals/EXIF, identity, authority and face-blur review are complete.

Redact private addresses, personal phone/email, DNI/NIE/NIF, bank/account numbers, verification codes, signatures and unrelated private identities. Keep courts, corporate parties, judicial authors and materially necessary professional roles.

### `PUBLISH_AFTER_REVIEW`

Only after explicit review approval:

1. add the Spanish and English active-estate routes with semantic parity;
2. show `decided / not decided` for every court act;
3. show party assertion, counter-position, court observation, operative holding and unresolved source in one matrix;
4. link each source card to its redacted transcript and provenance record;
5. add route registry, sitemap, discovery-page and validator entries;
6. run PII, broken-link, JSON, HTML, duplicate-ID, same-date-act and bilingual-parity checks;
7. render the pages at desktop/mobile widths and inspect them visually;
8. keep the PR draft until review; and
9. after merge, verify the exact merge SHA, Pages deployment and both live URLs before saying “live”.

## Priority acquisition batches

Run these as resumable micro-batches, not an unbounded inbox search:

- `AE-01`: 24-Oct-2019 non-convalidation anchor, 4-Nov reposición, AP 23-Jul-2019, interest/Community certificates and final amounts.
- `AE-02`: Jan/Feb-2021 Aweswell, AC and CAM filings, DIOR/Providencia, certificates, reports and missing annexes.
- `AE-03`: finca/title/licence/work/access overlay and security/key logs.
- `AE-04`: native 23-Feb/8-Mar-2021 email, photographic attachment and request→response→inspection outcome.
- `AE-05`: RPC/offer/auction/due-diligence route and post-non-convalidation responsibility/accounting.
- `AE-06`: native 1-Mar-2018 photographs/event proof and CAM pleading variants.
- `AE-07`: JV 1260, 2014 Fiscalía, DI 248, DP 1132 and May-2019 source completion.
- `AE-08`: opening/plan Autos, plan/observations, same-date clarification and all Article-152 quarterly reports.
- `AE-09`: PO 213/2015 primary judgment, intervention, annexes, appeal and result.
- `AE-10`: confidential valuation final/signed status, instructions, source reports and judicial/rebuttal treatment.
- `AE-11`: Valencia ORD 1859/2023 parent filing and transaction-level loan/hedge reconciliation.
- `AE-12`: liquidation-extension applications, later extensions, actual close-out and Bankia/nullity action/outcome.

## Required end-of-run report

State exactly:

- files reviewed, unique binaries and documentary-item count;
- duplicates, variants and false aliases;
- new adverse evidence and any corrected prior wording;
- closed/partial/open `ME-PDFSCAN-*` rows;
- files created/updated and branch/PR/SHA;
- validation commands and results;
- what is excluded from public Git and why;
- whether the work is draft, merged, deployed and independently live-verified; and
- the smallest next safe action.

Do not send email, contact institutions, merge, publish confidential material or disclose private originals unless the user separately authorises that action.

---
