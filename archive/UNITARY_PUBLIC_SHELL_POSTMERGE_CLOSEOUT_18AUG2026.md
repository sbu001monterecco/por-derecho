# UNITARY PUBLIC SHELL — POST-MERGE CLOSEOUT

**Date:** 18 August 2026  
**Controlling PR:** `#419`  
**Merge SHA:** `e26f6aa54331ba77dded1218eee9a062b5a094a3`  
**Status:** `MERGED / CI-GREEN / REPOSITORY-PRESERVED / PUBLIC-EDGE READBACK OPEN`

## 1. What was merged

The P0 public-site consolidation release adds, without deleting existing dossiers:

- bilingual Case Control Room;
- bilingual controlled site search;
- curated canonical route/alias registry with main-sitemap fallback;
- simplified homepage primary navigation plus direct Control Room gateway;
- compact global Case/Search shortcuts on substantive pages;
- bounded English DP 1901/2026 routing gateway preserving separation from DIP 2/2026 and DP 1956/2026;
- responsive fixes for inherited navigation, control-table and priority-link overflow;
- dedicated unitary-shell sitemap and robots discovery entry;
- Playwright desktop/mobile route-archetype regression gate.

PR #419 merged with **16 changed files, 704 additions and 0 deletions**.

## 2. Reader architecture

The Control Room exposes six distinct but interacting systems:

1. property / registered-title / 262-finca perimeter;
2. CEXP / productive-unit economics;
3. Concurso 36/2012 — AC / Court / calificación;
4. material control / 7 June 2018;
5. RICPE / RIC / HNT / later finance and support;
6. institutional answer-holders.

The reading modes are **Understand → Audit → Respond**.

The Control Room is not a new evidential source. Canonical dossier pages, primary sources, correction registers and specialist ledgers remain controlling.

## 3. Search boundary

Search is a discovery layer. Curated aliases improve retrieval of high-value names, proceedings, property numbers, figures and concepts such as CEXP, 737338, 8588, Borja, ACTÚA, Series F and DP 1901. Every main-sitemap route is also indexed as fallback.

Search ranking does not upgrade evidential status.

## 4. Validation result

Final PR-head validation:

- publication integrity run `32195830815` — success;
- supervisory-practice route run `32195830858` — success;
- unitary browser run `32195830796` — success;
- browser artifact ID `9345825532`;
- artifact SHA-256 `380b335b762a939762625ddf36b65c967e696a5a0c9ba795adeb53f736703048`.

The browser gate rendered 10 route archetypes at both desktop and mobile widths: **20 successful renders**. It checks homepage consolidation, the six-system Control Room, CEXP search, DP 1901 routing, representative existing dossiers, duplicate IDs and page-level horizontal overflow.

During implementation the gate found and drove correction of three real UX defects on the existing RICPE route:

- desktop header navigation expanding beyond the viewport;
- wide mobile control table without properly contained scrolling;
- mobile priority-link group expanding the document width.

The final strict run reports all tested routes overflow-free.

## 5. Evidence / procedural safeguards preserved

The release does not:

- establish new liability or criminal findings;
- convert documentary gaps or silence into culpability;
- merge LPB estate property with Matkator, third-party property or all CEXP assets;
- convert financing coexistence into proof of double funding or misuse;
- promote party allegations or expert work product into official outcomes;
- substitute DP 1901/2026 with DIP 2/2026 or DP 1956/2026;
- replace dossier ownership with the Control Room summary.

## 6. Loader migration boundary

`assets/site.js` was deliberately preserved unchanged. The new shell loads through the already-global sharing bridge and is itself route-aware. This creates a safe migration point for the next technical phase: incremental route bundles instead of a one-shot rewrite of the mature global loader chain.

## 7. Public-edge boundary

The source implementation is merged on `main`, and GitHub Actions rendered it successfully under the production `/por-derecho` subpath. Direct public-host readback from the current execution environment could not resolve `sbu001monterecco.github.io`.

Accordingly, this closeout records **MERGED / CI-GREEN**, not `LIVE_VERIFIED`.

A later successful public-host verification may promote the manifest without changing the substantive reader/evidence text.
