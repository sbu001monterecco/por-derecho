# OPTIMUM USER JOURNEY — DEPLOYMENT / ACCEPTANCE RECORD

**Date:** 18 August 2026  
**PR:** `#343 — Optimise objective-aligned reader journeys`  
**Merged:** yes  
**Merge commit:** `6deaba19d8db5c5c5e20f2965ae8ab7deb28d8de`  
**Source on `main`:** verified  
**Browser acceptance:** passed on exact PR head before squash merge  
**Live Pages host:** propagation not independently fetched from the available runtime

## Automated acceptance

| Control | Result |
|---|---|
| Supervisory-practice source validation | PASS · run `32124996920` |
| Playwright mobile/desktop journey validation | PASS · run `32124996811` |
| Routes / viewport combinations | 18 |
| Final error list | empty |
| Screenshot artifact | `9320082359` |
| Artifact digest | `sha256:7cb82e807e88d74fb50372590a848b61ec0b10780e35939df526a807cd490c5f` |

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

## Required assertions passed

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

## Delivery classification

- **Repository implementation:** complete.
- **Objective alignment:** complete.
- **Browser-render acceptance against the production subpath:** complete.
- **Continuity preservation:** complete.
- **Independent public Pages propagation check:** open but finite.

## Maintenance / freeze

No further structural redesign is recommended before the next material institutional or evidential event. Future changes should be triggered by:

- a documented RICPE/CNMV/public-office response;
- a new primary source or correction;
- a demonstrated broken journey;
- or a materially different audience requirement.

Preference-only redesign should be deferred to avoid regression and renewed cognitive load.
