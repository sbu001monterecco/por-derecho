# OPTIMUM USER JOURNEY — DEPLOYMENT / ACCEPTANCE RECORD

**Date:** 18 August 2026  
**PR:** `#343 — Optimise objective-aligned reader journeys`  
**Merged:** yes  
**Minimum implementation commit:** `6deaba19d8db5c5c5e20f2965ae8ab7deb28d8de`  
**Source on `main`:** verified  
**Browser acceptance:** passed on exact PR head before squash merge  
**Live GitHub Pages host:** **VERIFIED — serving the minimum implementation commit or a descendant**

## Automated acceptance

| Control | Result |
|---|---|
| Supervisory-practice source validation | PASS · run `32124996920` |
| Playwright mobile/desktop journey validation | PASS · run `32124996811` |
| Routes / viewport combinations | 18 |
| Final error list | empty |
| Screenshot artifact | `9320082359` |
| Screenshot artifact digest | `sha256:7cb82e807e88d74fb50372590a848b61ec0b10780e35939df526a807cd490c5f` |
| Public Pages propagation validation | **PASS · run `32127642260`** |
| Propagation workflow commit | `9204cba913d55b1c1f2c7f2979da305d6694cc51` |
| Minimum commit ancestry | **Confirmed — workflow commit 4 commits ahead; merge base = minimum commit** |
| Propagation evidence artifact | `9320957696` |
| Propagation artifact digest | `sha256:bb4320981fd975e19184d044cd878951c7d33cd6c19b553ba3219d06da6c8b72` |
| Public verification timestamp | `2026-08-18T10:37:16.807622Z` |

## Tested routes

- homepage ES;
- RICPE ES;
- CNMV ES;
- Regional Incentives ES;
- SNCA/ERDF ES;
- Community ES;
- 7 June 2018 ES;
- multiple financial lives ES;
- CNMV EN.

Each was tested at:

- `390 × 844`;
- `1440 × 1000`.

## Required browser assertions passed

- recipient hero visible and first;
- unified homepage reader-intent selector;
- reading-depth control on major pages;
- explicit next-step panel;
- mobile navigation control;
- no horizontal body overflow;
- no duplicate IDs;
- no more than one current journey stage;
- reading progress present.

## Visual review

The screenshot artifact was reviewed after the automated pass. The implementation was accepted for:

- homepage hierarchy and four-reader-purpose selector;
- compact navigation;
- RICPE institutional first read;
- CNMV / Incentives / SNCA practitioner pathways;
- Community and 7-June recipient-first hierarchy;
- funding route stage visibility;
- mobile menus and route controls;
- final next-step panels.

## Public GitHub Pages propagation proof

The live verification workflow did not rely on repository presence alone. It:

1. used GitHub's compare API to confirm that workflow commit `9204cba913d55b1c1f2c7f2979da305d6694cc51` is a descendant of `6deaba19d8db5c5c5e20f2965ae8ab7deb28d8de`, four commits ahead with the required minimum as merge base;
2. made cache-busted requests to the actual public host `https://sbu001monterecco.github.io/por-derecho/`;
3. received HTTP `200` for the public deployment probe, the optimum journey core asset, the finish asset, the global loader and the Spanish homepage;
4. found every required marker with no missing-marker result;
5. completed successfully on the first polling attempt;
6. published commit-status context `pages-propagation/optimum-reader-journey` as `success`.

### Live objects verified

| Public object | Required proof | Result |
|---|---|---|
| `deployment-probes/optimum-reader-journey-20260818.json` | unique probe ID + minimum commit SHA | HTTP 200 · markers present |
| `assets/optimum-reader-journey-20260818.js` | release ID + reader-intent + next-step markers | HTTP 200 · markers present |
| `assets/optimum-reader-journey-finish-20260818.js` | navigation / hero-shortcut / recipient-first markers | HTTP 200 · markers present |
| `assets/ricpe-filed-status-20260817.js` | both optimum-journey loaders | HTTP 200 · markers present |
| `es/` | Project Sun Rock + 60-second-summary marker | HTTP 200 · markers present |

All five responses were served by `GitHub.com`; their recorded `Last-Modified` timestamp was `Tue, 18 Aug 2026 10:35:13 GMT`. The detailed response headers, byte sizes and SHA-256 fingerprints are preserved in the propagation evidence artifact and in `archive/PUBLIC_GITHUB_PAGES_PROPAGATION_VERIFICATION_18AUG2026.md`.

## Delivery classification

- **Repository implementation:** complete.
- **Objective alignment:** complete.
- **Browser-render acceptance against the production subpath:** complete.
- **Continuity preservation:** complete.
- **Independent public Pages propagation:** **complete and positively verified**.
- **Operational delivery readiness:** **100%**.

## Maintenance / freeze

No further structural redesign is recommended before the next material institutional or evidential event. Future changes should be triggered by:

- a documented RICPE/CNMV/public-office response;
- a new primary source or correction;
- a demonstrated broken journey;
- or a materially different audience requirement.

Preference-only redesign should be deferred to avoid regression and renewed cognitive load.
