# UNITARY PUBLIC SHELL — DISCOVERY SYNCHRONIZATION

**Date:** 19 August 2026  
**Status:** `IMPLEMENTATION BRANCH — ADDITIVE DISCOVERY SYNC`  
**Parent publication:** `UNITARY-PUBLIC-SHELL-20260818`  
**Purpose:** keep the unitary reader interface synchronized with public dossiers created after the original shell without adding new top-level systems or changing evidential status.

## 1. Trigger

The original unitary shell correctly created a curated bilingual route registry and a fallback over the main `sitemap.xml`. Subsequent publications created important public routes in specialist discovery lanes, including:

- DP / PP 1041/2017 litigious-credit / retracto reconstruction;
- Cuatrecasas professional-lifecycle reconstruction;
- Cuatrecasas ICAM / CCACM 2026 procedural map;
- PwC Canarias / Carlos Saavedra public routes already declared through a specialist sitemap.

The issue was not deletion or regression. It was **discovery drift**: a route could be public and sitemap-listed without being guaranteed to appear in the unitary search because the search fallback read only the main sitemap.

## 2. Architecture retained

The Case Control Room remains a six-system model:

1. registered property / title;
2. CEXP / productive-unit economics;
3. Concurso 36/2012 — AC / Court / calificación;
4. material control / 7 June 2018;
5. finance / public-support layers;
6. institutional / professional answer-holders.

No seventh system is created for DP1041 or Cuatrecasas. DP1041 is bridged into the insolvency / creditor / recovery chain. Cuatrecasas and ICAM/CCACM are bridged into the institutional / professional-answer system.

## 3. Search synchronization

The controlled search now combines three layers:

### A. Base curated registry

`assets/data/unitary-route-registry-v1.json` remains the original high-value canonical index.

### B. Additive synchronization registry

`assets/data/unitary-route-registry-sync-20260819.json` adds curated bilingual metadata for:

- DP1041 / Article 1535;
- Cuatrecasas Sun Park lifecycle;
- Cuatrecasas ICAM / CCACM 2026.

This improves titles, aliases and result typing without rewriting the original controlling registry.

### C. Automatic specialist-sitemap fallback

`assets/unitary-public-shell-20260818.js` now reads `robots.txt`, identifies same-project `Sitemap:` declarations and ingests the `<url><loc>` routes from every declared sitemap, in addition to the main sitemap.

Production sitemap URLs are normalized back to the current project origin so the same logic works in GitHub Actions when the static site is served under the production `/por-derecho` subpath on localhost.

The result is forward-compatible: a future public route included in a declared specialist sitemap becomes discoverable even before it receives a curated alias entry.

## 4. DP1041 bridge and safety

The Control Room now points readers from the Concurso / creditor system to the bilingual DP1041 dossier.

The bridge asks the estate-interest question without converting it into a merits conclusion:

- what did LPB obtain or lose from the deed-and-price route;
- what was the effect of the PH122→CAM assignment treatment;
- what measurable estate benefit, if any, followed;
- what primary cessation / appeal / assignment-economics evidence remains missing.

### Mandatory boundary

The synchronization does **not** state that Article 1535 certainly applied, that LPB had a guaranteed winning retracto claim, that the insolvency administration personally terminated DP1041 absent the primary act, or that the effect pattern proves collusion, corruption or improper judicial bias.

The canonical DP1041 dossier remains controlling for those evidential distinctions.

## 5. Cuatrecasas bridge and safety

The institutional / professional-answer system now links to:

- the Cuatrecasas mandate → DD → protection → handover → recovery → ETJ lifecycle; and
- the 2026 ICAM / CCACM procedural map.

### Mandatory boundary

A bar complaint is an allegation. An ICAM archive based on limitation or territorial competence is not a merits ruling that professional conduct was proper. A pending administrative appeal is not proof that the complaint will succeed.

The public shell does not reproduce privileged advice or turn the professional-lifecycle chronology into a finding of misuse of confidential information, conflict, collusion or improper motive.

## 6. Legal-advisers sitemap

A new `sitemap-legal-advisers.xml` groups the bilingual Cuatrecasas lifecycle and ICAM/CCACM routes and is declared in `robots.txt`.

This improves ordinary search-engine discovery and also makes those routes part of the unitary controlled-search fallback.

## 7. Reader-facing wording

The EN/ES search pages now state accurately that fallback discovery comes from same-project routes contained in sitemaps declared through `robots.txt`, rather than only the main sitemap.

The Control Rooms remain explicit that:

- search is discovery metadata, not evidential proof;
- stronger labels require stronger evidence;
- silence is not liability;
- primary contrary evidence and corrections can narrow or defeat the current interpretation.

## 8. Regression contract

The unitary browser suite is expanded to cover:

- EN/ES homepage;
- EN/ES Control Room;
- EN/ES search;
- DP1901 separation gateway;
- EN/ES DP1041 routes;
- Cuatrecasas lifecycle and EN/ES ICAM/CCACM routes;
- representative AC, RICPE and 262-finca routes.

At each desktop/mobile viewport, controlled search must successfully locate:

1. `CEXP` — original curated search;
2. `1041` — new curated DP1041 synchronization;
3. `Cuatrecasas` — new curated professional-lifecycle synchronization;
4. `pwc canarias carlos saavedra` — specialist-sitemap-only fallback proof.

The last query is deliberately important: it proves the generic `robots.txt` / specialist-sitemap ingestion mechanism rather than merely proving that the new addendum registry exists.

The workflow now triggers when `robots.txt`, any `sitemap*.xml`, either unitary route registry, synchronized dossier route, or shared unitary reader code changes.

## 9. Deletion / non-regression rule

This synchronization is additive in architecture. It must not:

- delete either Control Room;
- delete either search route;
- alter the six-system count;
- remove DP1901 procedural separation;
- remove original CEXP, valuation, finance or institutional pathways;
- reduce evidential-boundary language;
- replace the original `UNITARY-PUBLIC-SHELL-20260818` manifest.

The original manifest remains controlling for the initial shell. This document and its companion publication manifest govern only the discovery synchronization layer.

## 10. Completion standard

Repository completion requires:

- publication-integrity / deletion-safety PASS;
- unitary Playwright desktop/mobile PASS;
- DP1041, Cuatrecasas and specialist-sitemap fallback searches PASS;
- no page-level horizontal overflow on tested routes;
- no substantive public-route deletion.

`LIVE_VERIFIED` remains a separate state and must not be claimed solely from merge or localhost production-subpath rendering.
