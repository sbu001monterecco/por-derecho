# DECLARATION 004 — CURRENT-MAIN INTEGRATION RECORD

**Date:** 21 August 2026  
**Current-main base used:** `5dfb1e5f3df8f6b36625a4a19098cb17492c6482`  
**Working branch:** `continuity/declaration004-current-main-21aug2026`  
**Status:** `SOURCE-CONTROLLED ON CURRENT-MAIN-BASED FEATURE BRANCH — NOT YET MERGED / NOT CLAIMED LIVE`

## 1. Supersession rule

The earlier branch `continuity/factual-digest-reverse-engineering-20aug2026` diverged from current `main` by more than two hundred later commits and must **not** be merged wholesale or used as a source for `assets/site.js`.

Current `main` already contains:

- Declaration 004 itself;
- Declaration 004's row in `archive/declarations/INDEX.md`;
- the 21-Aug repository/website reverse-engineering state register;
- substantially newer runtime/site-loader architecture.

This branch therefore carries forward **only controls still missing from current `main`**.

## 2. Added / updated controls

1. `archive/REVERSE_ENGINEERING_360_RICPE_IDONEIDAD_DECLARATION004_ADDENDUM_21AUG2026.md`
   - defines the source-derived-declaration evidence rule;
   - places Declaration 004 in the 360° dependency graph as question/knowledge provenance, not primary proof;
   - preserves lawful reconciliation scenarios and P0 documentary closure.

2. `assets/data/case-reconstruction-declaration004-addendum-20260821.json`
   - machine-readable source class `SOURCE_DERIVED_DECLARATION`;
   - proposition `RICPE-IDON-2022-TIMING-001`;
   - evidence node `EVID-DECL-004-RICPE-IDON-20260818`;
   - dependency relation `SUPPORTS_QUESTION_PROVENANCE`;
   - explicit `doesNotProve` controls.

3. `assets/declaration004-source-provenance-20260821.js`
   - bilingual public evidential-status note;
   - limited to the ES/EN RICPE idoneidad and ES/EN 360° reverse-engineering routes;
   - preserves private-witness anonymity;
   - expressly states that primary records control the 2022 facts.

4. `assets/site.js`
   - current-main file preserved;
   - only one new current-generation loader appended;
   - no stale 20-Aug `site.js` content transplanted.

5. `archive/REPOSITORY_WEBSITE_REVERSE_ENGINEERING_STATE_REGISTER_21AUG2026.md`
   - adds P0-E for RICPE idoneidad / Series-F–G source-and-use;
   - adds Declaration 004 source-status control;
   - makes this bridge part of the current finite-evidence queue.

## 3. Evidential boundary

Controlling rule:

> **A source-derived declaration may support knowledge, recollection, notice, chronology, question provenance or a retrieval lead. It does not replace the primary legal, administrative, banking, accounting or technical record that creates or proves the underlying bridge.**

Declaration 004 therefore does not prove:

- scope/content of Decree 224/2022;
- full content of the AEAT binding report;
- absence of a second or amended authorisation;
- Series-F or Series-G use;
- prohibited double funding;
- fraud, criminal intent or liability.

## 4. Validation performed before this record

Local syntax/data checks performed on the new branch content:

- `node --check` passed for `assets/declaration004-source-provenance-20260821.js`;
- the appended `site.js` loader block passed `node --check` in isolation;
- `assets/data/case-reconstruction-declaration004-addendum-20260821.json` parsed successfully as JSON and the source-class assertion passed.

These checks are not a substitute for repository CI, rendered DOM verification or public-edge read-back after merge.

## 5. Publication state

Do not state that this new provenance control is live merely because the branch exists.

Required later states remain separate:

1. branch/source-controlled;
2. PR reviewed/mergeable;
3. merged to `main`;
4. repository checks/CI passed;
5. public Pages route read-back verified;
6. external indexing, where material.

## 6. Next authorised publishing action

The branch is now suitable for a **draft pull request** after a final current-main comparison. PR creation and any merge remain separate publishing actions requiring their own authorisation under the repository workflow.
