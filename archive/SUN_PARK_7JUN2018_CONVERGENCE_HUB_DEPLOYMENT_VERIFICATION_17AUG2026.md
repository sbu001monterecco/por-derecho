# SUN PARK — 7 JUNE 2018 CONVERGENCE-HUB DEPLOYMENT VERIFICATION

**Date:** 17 August 2026  
**Repository:** `sbu001monterecco/por-derecho`  
**Public implementation PR:** #283  
**Merge commit:** `c82a69b1c09d976452c48c7b0ff1afa3d3cd0ca9`  
**GitHub Pages run:** `32031665555`  
**Status:** **DEPLOYED — EXACT-SHA PAGES SUCCESS**

## 1. Exact-main verification

After PR #283 merged, `main` resolved to:

`c82a69b1c09d976452c48c7b0ff1afa3d3cd0ca9`

This is the PR #283 merge commit and the exact SHA used by the deployment run.

## 2. Pages verification

GitHub Pages workflow run `32031665555`:

- workflow: `pages build and deployment`;
- head branch: `main`;
- head SHA: `c82a69b1c09d976452c48c7b0ff1afa3d3cd0ca9`;
- created: `2026-08-17T12:47:58Z`;
- completed: `2026-08-17T12:48:30Z`;
- final status: `completed`;
- conclusion: `success`.

The run's three jobs all completed successfully:

- `build` — success;
- `report-build-status` — success;
- `deploy` — success.

Therefore the public-site revision was built and deployed by GitHub Pages from the exact PR #283 merge SHA.

## 3. Merged-source verification

Verified on current `main` after merge:

### Loader

`assets/site.js`

Blob SHA:

`f91562e1f6d581584869142a3da70ecfa11846dc`

The final route-independent loader contains:

`load('sun-park-7june-convergence-20260817.js?v=20260817a');`

and explicitly labels the module as a presentation layer that creates no new primary finding.

### Convergence module

`assets/sun-park-7june-convergence-20260817.js`

Blob SHA:

`2c6051362d8a1eb67292280e475497b5686e84be`

The module is route-scoped to:

- `/en/sun-park-takeover-7-june-2018/`;
- `/es/toma-control-sun-park-7-junio-2018/`;
- `/en/`;
- `/es/`.

The corrected stable deep links for the dossier include:

- EN `#project-before-title`, `#events-of-7-june`, `#displacement-and-benefit`;
- ES `#proyecto-antes-del-titulo`, `#hechos-7-junio`, `#desplazamiento-y-beneficio`.

## 4. Published reader architecture

PR #283 deploys the previously controlled architecture without replacing the source-rich static dossier:

1. canonical hinge thesis;
2. four-clock model;
3. Before → 7 June → After evidential structure;
4. control-before-title visual;
5. `what 7 June did not decide` box;
6. principal-witness JDAM absence caveat;
7. AP 89/2014 and DI 248/2018 archive counterweights;
8. parallel lives separated from converging pressure tracks;
9. legal/economic bridge rule for cross-track consequences;
10. full-platform threshold model;
11. audience-reconciliation matrix;
12. central-hub navigation exits;
13. high bilingual homepage hinge module.

## 5. Evidential/publication boundary

Deployment success does not upgrade the status of any underlying proposition.

The public controls remain:

- material/practical control is distinct from title and lawful possession;
- 7 June is not treated as a whole-hotel title date;
- practical control before title does not itself establish criminality;
- Community/security authority is not treated as universal property or operating authority;
- chronology alone is not treated as causation/common intent;
- institutional receipt is not treated as personal knowledge or responsibility;
- multiple finance/support layers are not treated as proof of unlawful duplicate funding merely by coexistence;
- AP 89/2014 and the DI 248 archive remain visible adverse evidence;
- the principal witness presently relied upon does not place JDAM physically onsite on 7 June 2018.

## 6. Verification limit

This verification proves exact-SHA repository publication through the successful GitHub Pages deployment pipeline and merged-source presence. It does not claim that every browser/cache/CDN instance was independently rendered and visually inspected at the same instant.

The implementation is therefore deployment-verified at the repository/Pages level, with browser-cache propagation treated as a separate presentation-layer consideration rather than an evidential gap.
