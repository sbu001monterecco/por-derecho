# DEPLOYMENT LOG — PR #319 COMMUNITY / CEXP ACTA AUTHORITY PROVENANCE

**Date:** 17 August 2026  
**PR:** #319 — `Add 2008–2022 Community ACTA authority provenance`  
**Merge method:** squash  
**Merged commit:** `d93d501f1b40a69134feb031fefca947c082192d`

## Repository verification

After merge, the GitHub branch API reported protected `main` at exactly:

`d93d501f1b40a69134feb031fefca947c082192d`.

The merged tree contains the canonical ACTA provenance register, correction/evidence/maintenance supplements, deletion checkpoint, reusable prompt, bilingual frontend module and `assets/site.js` loader update.

## GitHub Pages verification

Pages configuration:

- site: `https://sbu001monterecco.github.io/por-derecho/`
- visibility: public
- build type: legacy
- source: `main` / `/`
- HTTPS enforced: yes

Commit-specific Pages build:

- build id: **1157710758**
- commit: **`d93d501f1b40a69134feb031fefca947c082192d`**
- created: `2026-08-17T20:50:34Z`
- updated/completed: `2026-08-17T20:51:14Z`
- duration: `40604` ms
- final status: **`built`**
- error message: **none**

The commit-specific build result controls over the generic Pages endpoint's transient/stale `errored` state observed while this build was still running.

## Public implementation covered by the build

The new `assets/community-actas-authority-provenance-20260817.js` module is loaded by `assets/site.js` and targets the existing stable ES/EN Community/ACTA routes plus context bridges on relevant downstream pages.

It adds:

- 2008 Alimarket transaction baseline;
- 2008 primary-source/CEXP entity correction layer;
- bounded minority / c.23% evidence status;
- 22-Jun-2011 disputed-authority four-part evidence/status module;
- 2016/2018/2019/2022 provenance annotations;
- downstream context links.

## Privacy/publication boundary

No new public link to unredacted 2016/2018 ACTA binaries was added. The public frontend exposes source-derived facts and stable evidence IDs while recording that public redacted derivatives remain open. This prevents publication of DNI/personal identifiers contained in source copies.

## Deployment conclusion

**DEPLOYED / BUILD VERIFIED for commit `d93d501f…`.**

This log proves the repository-to-Pages build event. It does not claim that every search engine has reindexed the new content or that every open primary-evidence gap has been closed.