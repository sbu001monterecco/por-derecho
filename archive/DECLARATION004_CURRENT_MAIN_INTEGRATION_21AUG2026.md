# DECLARATION 004 — CURRENT-MAIN INTEGRATION RECORD

**Date:** 21 August 2026  
**Current-main base used:** `e4b46770eaa81fa12a7c1d89293c2aa2acfb656b`  
**Working branch:** `continuity/declaration004-current-main-21aug2026-v3`  
**Status:** `SOURCE-CONTROLLED ON CURRENT-MAIN-BASED FEATURE BRANCH — PENDING PR / MERGE / READ-BACK`

## 1. Supersession rule

Do not merge the earlier 20-Aug Declaration-004 integration branches or the superseded v2 PR branch wholesale. They were based on older repository states and would risk regressing later runtime/site and handover work.

Current `main` already contains:

- Declaration 004 itself;
- Declaration 004 in `archive/declarations/INDEX.md`;
- the 21-Aug repository/website reverse-engineering state register;
- later DP1901/DP1956, evidence-provenance, CEXP/HNT and other current handovers;
- the current site/runtime control layers;
- the FTI/Meeting Point verifier that exposed a mission-critical permission defect during the superseded PR run.

This branch carries forward only the still-missing Declaration-004 evidential-classification/public-provenance controls and the read-only hardening required for the FTI live verifier to satisfy the repository's mission-critical permissions gate.

## 2. Scope

1. `archive/REVERSE_ENGINEERING_360_RICPE_IDONEIDAD_DECLARATION004_ADDENDUM_21AUG2026.md`
   - classifies Declaration 004 correctly in the 360° dependency graph;
   - preserves lawful reconciliation scenarios and P0 source-and-use requests.

2. `assets/data/case-reconstruction-declaration004-addendum-20260821.json`
   - adds `SOURCE_DERIVED_DECLARATION` source class;
   - adds open proposition `RICPE-IDON-2022-TIMING-001`;
   - records `SUPPORTS_QUESTION_PROVENANCE`, not foundational proof.

3. `assets/declaration004-source-provenance-20260821.js`
   - bilingual anonymous source-status note;
   - limited to the ES/EN RICPE idoneidad and ES/EN 360° routes.

4. `assets/site.js`
   - preserves the current-main loader intact;
   - appends only the Declaration-004 provenance loader.

5. `archive/REPOSITORY_WEBSITE_REVERSE_ENGINEERING_STATE_REGISTER_21AUG2026.md`
   - adds P0-E RICPE idoneidad / Series-F–G source-and-use;
   - adds a permanent Declaration-004 evidential-classification rule.

6. `.github/workflows/verify-fti-meeting-point-live.yml`
   - removes `statuses: write` and the status-posting step;
   - preserves route polling, evidence output and failure semantics;
   - brings the verifier back within the mission-critical read-only workflow-permission policy.

## 3. Controlling evidential boundary

> **A source-derived declaration may support knowledge, recollection, notice, chronology, question provenance or a retrieval lead. It does not replace the primary legal, administrative, banking, accounting or technical record that creates or proves the underlying bridge.**

Declaration 004 does not independently prove Decree scope, AEAT-report content, absence of a second authorisation, Series-F/G use, prohibited double funding, fraud, criminal intent or liability.

## 4. Validation history

On superseded PR #760, the relevant publication, insolvency-perimeter and operational checks passed. The only publication-integrity failure was the mission-critical permissions gate identifying `statuses: write` in the FTI/Meeting Point live verifier. This branch incorporates the least-privilege fix rather than bypassing the gate.

Previously completed local/source validation remains applicable to the unchanged Declaration-004 files:

- JavaScript syntax check passed for the provenance module;
- appended loader block syntax check passed;
- JSON addendum parsed successfully.

Repository CI on this current-main branch must pass before merge.

## 5. Publication state

Keep separate:

1. branch/source-controlled;
2. reviewed/mergeable;
3. merged to `main`;
4. CI/checks passed;
5. GitHub Pages/source read-back verified;
6. rendered/public-edge verification where required;
7. external indexing, where material.

No live/public claim is made until post-merge read-back.
