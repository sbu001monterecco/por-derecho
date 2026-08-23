# SUN PARK — 7 JUNE 2018 CONVERGENCE-HUB PUBLIC IMPLEMENTATION

**Date:** 17 August 2026  
**Repository:** `sbu001monterecco/por-derecho`  
**Implementation branch:** `agent/7-june-convergence-public-implementation-17aug2026`  
**Base main checked before implementation:** `6b70dc9cca8d9f33cebcb1810cd6848855877d25`  
**Status at creation:** IMPLEMENTED ON BRANCH — PR / MERGE / PAGES VERIFICATION REQUIRED

> **Supersession note — 23 August 2026:** This implementation record retains the original deployed design description. The controlling signed-source review now fixes Auto 164/2021 of 18 May 2021 as the definitive approval, keeps the two 15 October 2021 Autos separate, and identifies the two 26 January 2022 Autos as clarifications that make no new award. Deed 457 follows on 21 February 2022. Any singular “26-Jan-2022 adjudication” shorthand below is historical and superseded.

## 1. Purpose

This record implements the reader architecture already controlled by:

- `archive/SUN_PARK_7JUN2018_PARALLEL_TRACKS_CONVERGENCE_ARCHITECTURE_17AUG2026.md`;
- `archive/SUN_PARK_7JUN2018_READER_LOGIC_REFINEMENT_AND_DELETION_HANDOVER_17AUG2026.md`;
- `archive/SUN_PARK_7JUN2018_STORYLINE_WEBSITE_BRIDGE_17AUG2026.md`;
- `archive/CAM_2018_EXTRACONCURSAL_TAKEOVER_RETRIEVAL_GATE_16AUG2026.md`.

It does **not** create a second 7-June public page. It upgrades the existing bilingual routes into the central convergence hub and adds a high homepage hinge module.

## 2. Public routes preserved

Canonical routes remain unchanged:

- EN: `/en/sun-park-takeover-7-june-2018/`
- ES: `/es/toma-control-sun-park-7-junio-2018/`
- EN homepage: `/en/`
- ES homepage: `/es/`

No redirect or new event-route architecture is introduced.

## 3. Implementation files

### New route-scoped presentation module

`assets/sun-park-7june-convergence-20260817.js`

The module runs only on the two 7-June dossier routes and the two language homepages. It:

1. reframes the visible 7-June hero around the controlling thesis:
   > **7 June 2018: the day the legal, physical, operational and commercial timelines stopped matching.**
2. inserts four independent clocks:
   - legal/title;
   - physical/operational;
   - commercial/financial;
   - institutional/knowledge;
3. makes `Before → 7 June → After` the evidential heart;
4. implements the mandatory `control before title` visual using 7-Jun-2018, 26-Jan-2022 and 21-Feb-2022 thresholds;
5. makes `what 7 June did not decide` prominent;
6. preserves the mandatory adverse precision that the principal witness presently relied upon does **not** place JDAM physically at Sun Park on 7 June 2018;
7. keeps AP Judgment 89/2014 and the May-2019 DI 248 archive visible as adverse/counterweight evidence;
8. separates `parallel lives` from `converging pressure tracks`;
9. requires an explicit legal/economic bridge before asserting cross-track causation;
10. expands the object from apartments/keys to real estate, operating capacity, customer/community platform, commercial infrastructure and recovery capacity;
11. adds an audience-reconciliation matrix across Court/AC, Community/CEXP/owners, customers/staff, operators/financiers, RICPE/CNMV/investors, tourism/Yaiza/Cabildo, RIC/incentive/FEDER bodies and Fiscalía/media/public;
12. makes the dossier a navigation interchange into the pre-7-June business/platform, ownership/Community, 7-June event record, later consequences, multiple-financial-lives, Calificación and recovery routes;
13. adds a high bilingual homepage module immediately after the existing current-priority band, before the 60-second case summary.

### Loader

`assets/site.js`

Adds an independent load of:

`sun-park-7june-convergence-20260817.js?v=20260817a`

The module no-ops on every unrelated route.

## 4. Preservation strategy

The detailed static EN/ES 7-June dossier remains in the underlying HTML. This implementation is a progressive presentation layer rather than deletion/replacement of the source-rich dossier.

That choice preserves:

- existing anchors and deep links;
- the longer legal-perimeter analysis;
- ONA/rescue evidence;
- event-by-event source treatment;
- AC/Judge, project-before-title, displacement/outcome and missing-evidence sections;
- existing language routes;
- later cross-site modules that already attach to the dossier.

## 5. Evidential controls

This implementation creates **no new primary factual finding**.

It must not be read as establishing that:

- 7 June 2018 was a whole-hotel title date;
- practical/material control equalled legal title or lawful possession;
- practical control before title itself proves a crime;
- Community governance or security powers created universal property or operational authority;
- distinct financial/public-support layers prove duplicate funding or fraud merely because they coexist;
- chronological proximity proves coordination, common intent or causation;
- institutional receipt proves personal knowledge or responsibility.

For proposed cross-track consequences, the governing chain remains:

`SOURCE EVENT → ACTOR / AUTHORITY → LEGAL OR ECONOMIC BRIDGE → AFFECTED RIGHT / OPTION → CONSEQUENCE → EVIDENCE STATUS → COUNTERFACTUAL / GAP`

## 6. Reader-experience decisions

- The new architecture appears before the pre-existing detailed legal-perimeter section so first-time readers receive the causal map before the long evidential record.
- Four clocks are displayed as independent cards rather than merged into one chronology.
- Before/7-June/After uses a visually distinct central hinge.
- Control-before-title is presented as a date-gap, not a conclusion about illegality.
- Parallel lives and pressure tracks are displayed side-by-side but labelled as different analytical constructs.
- The audience matrix is horizontally scrollable on narrow viewports and remains a semantic table.
- Mobile layouts collapse clocks, threshold layers and navigation cards into readable stacks.
- The original source-rich content remains accessible below the new gateway.

## 7. Homepage role

The homepage module states, in controlled form, that:

- a functioning hotel;
- an insolvency proceeding;
- fragmented ownership;
- Community governance; and
- an emerging redevelopment project

converged around the 7-June hinge, while formal LPB title followed later.

It offers two primary routes:

- the 7-June convergence dossier;
- the same-hotel / multiple-financial-lives dossier.

This makes the 7-June event a site-level interchange rather than an isolated event page.

## 8. Non-blocking downstream work

TripAdvisor / New Horizons / Lanzarote Information / BBC provenance work remains downstream enrichment of the customer/public-narrative lane. It is not required for the core convergence architecture and has not been invented to fill any missing link.

## 9. Verification required before final close-out

Before this implementation can be treated as fully deployed and deletion-safe, complete:

1. branch-vs-main diff review;
2. PR creation and self-review;
3. merge into protected `main`;
4. exact merge-SHA source check;
5. GitHub Pages workflow verification;
6. confirm module and loader on `main`;
7. record any deployment limitation honestly;
8. update the implementation/deletion status from this branch-time state.

Until those steps are complete, do not describe the public rebuild as deployed.
