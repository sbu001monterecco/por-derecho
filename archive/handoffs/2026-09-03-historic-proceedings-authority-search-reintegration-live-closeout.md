# Historic proceedings / justice authority / Fiscalía / search reintegration — live closeout and successor handoff

**Handoff ID:** `PD-WCH-20260903-AUTH-SEARCH-REINT-001`  
**Workspace ID:** `PD-WS-20260902-0001`  
**Date:** 3 September 2026  
**Status:** `DELETION_SAFE_WITH_OPEN_WORK`  
**Release state:** `MERGED_DEPLOYED_LIVE_BROWSER_VERIFIED`

## Scope

This is the successor continuity object for the historic-proceedings, justice-authority, Fiscalía, search and interconnectivity reintegration completed from the existing 2 September workspace. It does **not** certify the global historic/current docket complete. It records the exact release bytes, browser verification and remaining source-defined gaps so a successor thread can continue without repeating the broad 2 September Gmail/Drive discovery.

## Exact production release

- Final production PR: **#1373 — Reintegrate historic proceedings, justice authority and search continuity**.
- Reviewed reintegration head: `687c0a32a217f1db32a3e7e3be5e8650b677570a`.
- Production merge SHA: `efbb1032b0c5e21ca892b3a9db17b3f7b4073e6c`.
- Production merge tree: `1e2295ccc94d3e020b2ef0db59924d439de2aa93`.
- The production merge tree is exactly the reviewed head tree.
- GitHub Pages run: **33697357002 / #1420**, completed `success`, head SHA exactly `efbb1032b0c5e21ca892b3a9db17b3f7b4073e6c`.
- Exact-head reintegration validation workflow: run **33696673412**; final idempotence pass produced no controlled changes at head `687c0a32a217f1db32a3e7e3be5e8650b677570a`.

Historical publication manifests remain immutable. The current reintegration manifest records the current generated successor state and byte evolution; it does not rewrite prior release bytes.

## Live Chromium verification

A disposable verification branch rooted at the production merge SHA was used only to run a network-capable Chromium smoke test; it is **not** a production branch and must not be merged.

- Verification branch: `verify/historic-proceedings-live-browser-20260903`.
- Browser workflow: `Live browser historic reintegration 20260903`.
- Browser run: **33700567926 / #1**.
- Browser-run head: `fcf03556f89c7cf6fe541efed381471f5ac360ca`.
- Result: **success**; Chromium step `Verify exact deployed production site in Chromium` completed successfully.

The browser gate exercised the actual public Pages site and proved:

1. Spanish and English homepages load.
2. `GC-CIV-003` Spanish and English proceeding pages load.
3. Las Palmas historic civil justice-authority pages load in ES/EN.
4. Master Proceedings register and proceedings map load in ES/EN.
5. The locked `GC-CIV-003` page exposes NIG `3501642120170028407`, court `PD-SP-I-0048`, Juan Avello Formoso `PD-SP-P-0124`, Fernando Pérez Polo `PD-SP-P-0165`, and the explicit open documentary gap text.
6. Homepage search click-throughs resolve the 1041/2017 reference, NIG, `GC-CIV-003`, Juan Avello Formoso, Fernando Pérez Polo, `PD-SP-P-0165`, `^P-0165`, the exact court name, `PD-SP-I-0048`, `^I-0048`, representative `PD-SP-R-0001` / `^R-0001`, and representative organisation `PD-SP-O-0003` to controlled destinations.
7. `/es/procedimientos/lz-civ-050/` and `/en/proceedings/lz-civ-050/` return 404.
8. Homepage search returns no result for `LZ-CIV-050` in ES or EN.
9. `sitemap.xml`, `proceedings-master-public-v1.json`, and `proceeding-page-routes-20260902.json` contain no `lz-civ-050` reference.

## Final proceedings / interconnectivity denominator at this release

- **131** canonical Master Proceedings rows.
- **130** public Master Proceedings rows.
- **107** canonical exact proceedings: **106 public exact + 1 private exact**.
- **24** public non-exact / `FALSE` / `UNVERIFIED` rows.
- **130** bilingual public proceeding routes.
- **54** reciprocal formal procedural edges.
- **416** reciprocal contextual-navigation pairs.
- Fiscalía perimeter: **26 public / 23 exact / 3 unresolved**.

These counts are release denominators, not a claim that all historic proceedings ever existing have been recovered.

## Final CAEPR / justice-authority denominator at this release

CAEPR total: **350** canonical objects:

- PERSON: **165**
- ORGANISATION: **83**
- STRUCTURE: **11**
- INSTITUTION: **48**
- PROCEEDING: **43**

Source-identified justice/prosecutorial/notarial people: **62** total; **59 CARET_CONFIRMED / 3 CARET_PENDING**. Role denominator: **17 Ministerio Fiscal / 20 Judges-Magistrates / 17 LAJ / 8 Notary**.

This is the recovered-source denominator. It remains explicitly different from a certified complete historic/current official docket denominator.

## Locked correction — Diligencias Preliminares 1041/2017

The controlling identity is:

- Master ID: **`GC-CIV-003`**.
- Proceeding: **Diligencias Preliminares 1041/2017**.
- Court: **Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria**.
- Court CAEPR: **`PD-SP-I-0048`**.
- NIG: **`3501642120170028407`**.
- Magistrado-Juez: **Juan Avello Formoso — `PD-SP-P-0124`**.
- LAJ: **Fernando Pérez Polo — `PD-SP-P-0165`**.
- Primary located act: **Providencia 12 January 2018**; LAJ electronic signature dated **15 January 2018**.

The erroneous duplicate **`LZ-CIV-050`** must not be resurrected in a public route, Master register, coverage denominator, sitemap, search data or successor reconstruction.

## Remaining `SOURCE_GAP` / `CARET_PENDING` state for GC-CIV-003

Do not infer any missing identity, act or relationship. The following remain open until a primary/certified source closes them:

1. preceding signed **Auto**;
2. complete docket / certified index;
3. proof of the **19 February 2018** appearance and/or production;
4. later **5 March 2018** decree/closure sequence;
5. service/notification evidence;
6. finality evidence.

No Fiscal is attributed to this proceeding from office succession or contextual proximity; the current page correctly preserves a source gap / non-applicability state rather than inventing a Fiscal.

## New source-locked historic Las Palmas authority identities in this reintegration

- **Juan Avello Formoso — `PD-SP-P-0124` — Magistrado-Juez**, source-identified for the 12-Jan-2018 Providencia in GC-CIV-003.
- **Fernando Pérez Polo — `PD-SP-P-0165` — LAJ**, source-identified from the electronic signature dated 15-Jan-2018.
- **Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria — `PD-SP-I-0048`**, source-identified institution for GC-CIV-003.

These identities resolve only the exact source-supported act/date/capacity. They do not establish handling of other files or other dates.

## Priority targeted recovery queue

1. **P0 — GC-CIV-003 closure chain:** recover the preceding signed Auto, 19-Feb appearance/production proof, 5-Mar decree/closure, service and finality; do not perform broad discovery unless a named source gap requires it.
2. **P1 — 24 public non-exact/unverified proceeding rows:** close exact identity, organ, NIG, docket/status only from primary/certified sources.
3. **P1 — Fiscalía 3 unresolved rows:** recover the specific primary records required to move them from unresolved; preserve exact office/Fiscal attribution boundaries.
4. **P1 — global historic justice-authority docket backfill:** continue source-led Judge/Magistrate, LAJ and Fiscal recovery, keeping unknown applicable identities as explicit gaps.
5. **P2 — interconnectivity maintenance:** preserve the 54 formal reciprocal edges and 416 contextual pairs while preventing contextual proximity from being promoted into a procedural relationship.

The broad historic docket remains **OPEN_NOT_CERTIFIED_COMPLETE**.

## Action-ledger / discovery boundary

The machine companion to this handoff carries the `PD-CONT-DIGEST-001` action ledger. No broad Gmail/Drive rediscovery was performed for this closeout; that would duplicate the completed 2 September discovery. Future connected-source recovery is targeted only to an explicit `SOURCE_GAP`.

## Successor bootstrap

> Continue `PD-WS-20260902-0001` from the repository state recorded in `CURRENT_WORKSPACE_HANDOFF.md` and this 3-Sep successor handoff. Treat PR #1373, merge `efbb1032b0c5e21ca892b3a9db17b3f7b4073e6c`, tree `1e2295ccc94d3e020b2ef0db59924d439de2aa93`, Pages run 33697357002 and Chromium run 33700567926 as the completed reintegration release checkpoint. Do not restart broad discovery. Preserve the `GC-CIV-003` correction and never resurrect `LZ-CIV-050`. Continue only the named source-gap recovery or the next substantive proceeding work.

## Deletion-safety verdict

`DELETION_SAFE_WITH_OPEN_WORK`. The reintegration release is merged, deployed from the exact production merge SHA and live-browser verified. The historical docket itself remains open and reconstructable from explicit gaps and denominators.
