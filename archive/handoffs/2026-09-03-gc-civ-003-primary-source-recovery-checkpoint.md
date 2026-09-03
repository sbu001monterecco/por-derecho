# GC-CIV-003 primary-source recovery checkpoint — 03 Sep 2026

**Handoff ID:** `PD-WCH-20260903-GCCIV003-SRC-002`  
**Workspace:** `PD-WS-20260902-0001`  
**Repository:** `sbu001monterecco/por-derecho`  
**Baseline main verified before branch:** `231d25c12108579efdf92365cf7860bf281178f5`  
**Working branch:** `codex/gc-civ-003-primary-source-recovery-20260903`  
**Historic release state:** `MERGED_DEPLOYED_LIVE_BROWSER_VERIFIED`  
**Historic docket state:** `OPEN_NOT_CERTIFIED_COMPLETE`

## Immutable release checkpoint

PR #1373 remains the immutable historic-proceedings / justice-authority / search reintegration release checkpoint: merge `efbb1032b0c5e21ca892b3a9db17b3f7b4073e6c`, tree `1e2295ccc94d3e020b2ef0db59924d439de2aa93`, exact-SHA Pages run `33697357002` / #1420, hosted Chromium verification run `33700567926`.

Post-release correction #1376 advanced `main` to `231d25c12108579efdf92365cf7860bf281178f5` and corrected the stale GC-CIV-003 authority row in the bilingual historic Las Palmas/Arrecife authority views. This source-recovery checkpoint does not reopen or rewrite the #1373 release manifests.

## Locked proceeding identity

- `GC-CIV-003`
- Diligencias Preliminares 1041/2017
- Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria — `PD-SP-I-0048`
- NIG `3501642120170028407`
- Juan Avello Formoso — `PD-SP-P-0124`
- Fernando Pérez Polo — `PD-SP-P-0165`

`LZ-CIV-050` remains deprecated/removed and must never be recreated.

## Newly closed / narrowed source gaps

### CLOSED BY PRIMARY SOURCE

1. **19-Dec-2017 admission Auto** — recovered and read as an authentic electronically signed judicial act.
2. **Finality of the 19-Dec-2017 Auto only** — the Auto expressly states its own finality and no appeal under art. 258.2 LEC.
3. **Positive CAM citation/requerimiento on 18-Jan-2018** — recorded by Fernando Pérez Polo in the 23-Jan Diligencia de Ordenación as a positive SCNE result.
4. **CAM appearance/opposition** — primary party filing recovered; Gerardo Pérez Almeida and Carmen Ramírez de Prada expressly identified in that filing.

### STILL OPEN / TARGETED

1. Complete docket / certified index.
2. Actual result of the scheduled 19-Feb-2018 diligence.
3. Standalone primary Decreto de archivo of 05-Mar-2018.
4. Original archive/desistimiento/request filing and exact procedural basis.
5. Service/notification of the 5-Mar decree.
6. Finality of the closure sequence.

The 5-Mar decree is `STRONGLY_TRACED_PRIMARY_FILE_STILL_TO_RECOVER`, because a later 2026 filing lists it as an annex. Annex trace is not primary-decree verification.

## Targeted connected-source recovery performed

No broad Gmail/Drive rediscovery was run.

Targeted Drive inspection covered the dedicated `DILIGENCIA PRELIMINAR` source family and its sibling `TANTEO Y RETRACTO` family. Those folders contained the January primary acts/filings but did not surface a 19-Feb act/result or a standalone 5-Mar decree. One `DP 250118` PDF exposed no readable text and generated no inference.

Targeted exact/near-exact Drive searches for the case number, 19-Feb result, 05/03/2018, decree/archive/desistimiento language returned later analytical/annex-trace material, not the missing primary acts.

Targeted Gmail searches for `1041/2017` / `1041/17` around 19-Feb and 5-Mar returned no exact case-number hit. A date/actor-scoped 5-Mar search also returned no result.

A legacy 2020 litigation spreadsheet reports an archive after CAM appeared but misidentifies the court as Arrecife. It is retained solely as a recovery lead and is not used to establish court identity, authorship, archive reasoning, service or finality.

## Source-safe repository registration

Created:

- `archive/GC_CIV_003_PRIMARY_ACTS_SOURCE_REGISTER_03SEP2026.md`
- `assets/data/gc-civ-003-primary-source-state-20260903.json`

Updated bilingual public routes:

- `es/procedimientos/gc-civ-003/index.html`
- `en/proceedings/gc-civ-003/index.html`

The public pages now distinguish the Auto, Providencia, 23-Jan LAJ order and CAM opposition; expressly restrict finality to the 19-Dec Auto; preserve the 19-Feb result as unproved; and label the 5-Mar decree as strongly traced but primary-pending.

Connected-source Drive IDs and native docket binaries are intentionally not copied to public Git.

## Canonical-row reconciliation boundary

The dated machine source-state file above is the controlling **03-Sep-2026 source correction overlay** for GC-CIV-003. The older 02-Sep Master-row wording that still says `Preceding signed Auto` is superseded for source-gap interpretation by this later source-state record and the bilingual pages.

A future deterministic Master-register rebuild should ingest this overlay and replace the stale row text without changing the locked proceeding identity or denominator. Do not treat the stale 02-Sep wording as evidence that the Auto remains missing.

## Separate 8-Feb-2018 Mercantil act

The 8-Feb-2018 Mercantil Auto belongs to Concurso ordinario 36/2012, NIG `3501647120120000351`, not to GC-CIV-003. It remains context only. Its Judge/LAJ identities must not be imported into GC-CIV-003.

## Publication state at this checkpoint

`BRANCH_REGISTERED_PR_PENDING`

Before merge:

1. compare branch against freshly re-fetched `main`;
2. run governed CI through a PR;
3. merge only if the branch is still based safely on current main or has been reconciled;
4. verify exact merge-SHA Pages deployment;
5. live-read the affected ES/EN routes and machine source-state object.

## Next P0 recovery only

1. Actual 19-Feb-2018 act/result.
2. Standalone 5-Mar-2018 decree.
3. Underlying archive/desistimiento request.
4. Service and finality of closure.

Do not broaden Gmail/Drive discovery unless one of these explicit `SOURCE_GAP` items requires a tightly scoped follow-up.
