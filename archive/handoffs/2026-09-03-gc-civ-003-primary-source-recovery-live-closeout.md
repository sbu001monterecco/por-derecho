# GC-CIV-003 primary-source recovery live closeout — 03 Sep 2026

**Handoff ID:** `PD-WCH-20260903-GCCIV003-SRC-003`  
**Workspace:** `PD-WS-20260902-0001`  
**Repository:** `sbu001monterecco/por-derecho`  
**Historic docket state:** `OPEN_NOT_CERTIFIED_COMPLETE`

## Source-recovery release

The targeted GC-CIV-003 primary-source registration is now merged, deployed from its exact merge SHA and live-browser verified.

- PR: **#1377 — Register GC-CIV-003 recovered primary acts and refine source gaps**
- reviewed PR head: `3595abac9a1151d8bac1ae31e9721fcd0b8fa4f4`
- merge SHA: `ddebffb07f4750ab4ab19017a3aef5a195c45f70`
- merge tree: `a724378b7e0935aef691d9c941d0261ecd9c1b10`
- exact-SHA Pages run: `33708727660` / run #`1424`
- Pages head SHA: `ddebffb07f4750ab4ab19017a3aef5a195c45f70`
- Pages result: `success`

This is a post-#1373 source correction/recovery release. It does not mutate or replace the immutable historic reintegration release checkpoint at PR #1373 / `efbb1032b0c5e21ca892b3a9db17b3f7b4073e6c`.

## Hosted Chromium live verification

Disposable verifier branch:

`verify/gc-civ-003-primary-source-live-20260903`

Branch policy: `DISPOSABLE_DO_NOT_MERGE`.

- verifier head: `072cac2577e77a6eb0b3796c5707be389fb7f4f3`
- run ID: `33709044855`
- run number: `1`
- job: `chromium-live-gc-civ-003`
- result: `success`
- terminal marker: `GC_CIV_003_PRIMARY_SOURCE_LIVE_BROWSER_VERIFIED=PASS`

The verifier confirmed against the production Pages host:

1. ES GC-CIV-003 route returns HTTP 200 and contains the 03-Sep source update, locked ID/NIG/court/Judge/LAJ identifiers, 19-Dec Auto, 23-Jan LAJ order, unresolved 19-Feb result and strongly traced/pending 5-Mar decree state.
2. EN GC-CIV-003 route returns HTTP 200 with the same evidential distinctions.
3. `assets/data/gc-civ-003-primary-source-state-20260903.json` returns HTTP 200 and preserves `OPEN_NOT_CERTIFIED_COMPLETE`, the locked IDs, the 19-Feb `SOURCE_GAP`, and `STRONGLY_TRACED_PRIMARY_FILE_STILL_TO_RECOVER` for the 5-Mar decree.
4. Homepage search resolves `GC-CIV-003` and NIG `3501642120170028407` to the correct bilingual proceeding routes.
5. Homepage search resolves Juan Avello Formoso to `PD-SP-P-0124`, Fernando Pérez Polo to `PD-SP-P-0165`, and `PD-SP-I-0048` to the correct authority register.
6. Deprecated `LZ-CIV-050` returns 404 on ES and EN routes and is absent from ES/EN homepage search.
7. `LZ-CIV-050` is absent from live `sitemap.xml`, public Master JSON and public proceeding-route data.

## Closed source gaps

Closed by recovered primary source:

1. signed 19-Dec-2017 admission Auto;
2. finality of the 19-Dec-2017 Auto **only**;
3. positive CAM citation/requerimiento on 18-Jan-2018, recorded in the 23-Jan LAJ order;
4. CAM appearance/opposition through a recovered primary party filing.

## Remaining targeted source gaps

Still open and source-separated:

1. complete docket / certified index;
2. what actually happened on 19-Feb-2018;
3. standalone primary `Decreto de archivo de 05/03/2018`;
4. original archive/desistimiento/request filing and exact procedural basis;
5. service/notification of the 5-Mar decree;
6. finality of the closure sequence.

The 5-Mar decree remains `STRONGLY_TRACED_PRIMARY_FILE_STILL_TO_RECOVER`; annex trace is not primary-decree verification.

## Targeted recovery result

No broad Gmail/Drive rediscovery was performed.

The dedicated `DILIGENCIA PRELIMINAR` and sibling `TANTEO Y RETRACTO` source families were inspected. They supplied the January chain but not the missing 19-Feb result or standalone 5-Mar decree.

Exact/near-exact Gmail/Drive searches around 19-Feb and 5-Mar did not surface the missing primary acts. A broader but still date-bounded 19-Feb Gmail result was read and proved to concern **Concurso 36/2012**, not GC-CIV-003; it therefore closes no GC-CIV-003 gap and reinforces the proceeding boundary. A 5-Mar actor/counsel mailbox search returned no responsive message.

A legacy 2020 litigation spreadsheet that describes an archive but mislabels the court as Arrecife remains a recovery lead only and cannot override the primary Las Palmas/NIG chain.

## Canonical Master-row reconciliation boundary

`assets/data/gc-civ-003-primary-source-state-20260903.json` is the controlling 03-Sep source correction overlay for GC-CIV-003 gap interpretation.

The historical 02-Sep `archive/PROCEEDINGS_MASTER_REGISTER.csv` row was **not physically rewritten** in PR #1377 and can still contain the stale phrase `Preceding signed Auto`. That older wording is superseded for source interpretation by the dated overlay and live bilingual proceeding pages.

A future deterministic Master-register rebuild must ingest the overlay and replace that stale row wording without changing:

- `GC-CIV-003` identity;
- NIG/court/Judge/LAJ locks;
- release denominators;
- immutable historical release manifests.

Do not claim that the old CSV row itself was corrected in #1377.

## Separate-proceeding boundary

The 8-Feb-2018 Mercantil Auto belongs to Concurso ordinario 36/2012, NIG `3501647120120000351`. It remains contextual only. Its Judge/LAJ identities must not be transferred into GC-CIV-003 and it does not create a formal procedural edge absent a source.

## Current source-recovery state

`MERGED_DEPLOYED_LIVE_BROWSER_VERIFIED`

The broad historic docket remains `OPEN_NOT_CERTIFIED_COMPLETE`.

## Successor instruction

Continue `PD-WS-20260902-0001` from this closeout and the machine source-state overlay. Do not restart historic discovery. Re-fetch current `main` before any write. Preserve the immutable PR #1373 checkpoint, the locked GC-CIV-003 identity, and `LZ-CIV-050` as removed. Continue only the named P0 source gaps unless a new explicit `SOURCE_GAP` justifies a tightly scoped recovery search.
