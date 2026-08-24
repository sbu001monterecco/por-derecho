# Five-actor visibility and preservation thread — 24 August 2026

**Current verdict:** `DELETION_SAFE_WITH_OPEN_GOVERNANCE_ITEMS`

**Scope:** disappearance diagnosis, restoration of five private actors plus the two separate institutional roles, homepage/direct-route permanence, content-loss controls and reader-journey recommendations.

## 1. What happened

The actor material was not erased from the repository history. A later audience-order amendment moved the detailed component behind a runtime loader and treated an older static copy as duplicate/fallback material. That created an audience-collapse failure: when the nested JavaScript chain did not settle as expected, the visible detailed cards, descriptions, images and actor-specific linkages disappeared even though source fragments remained.

The repair in PR #919 restored static homepage copies and a dynamic presentation on the protected direct routes, kept the component outside closed progressive disclosure, and restored the five private actors followed by the Insolvency Administrator and Magistrate-Judge. Git history comparison from the pre-regression reference `a551e7e…` to the repaired `main` found no tracked-file deletions; the repaired tree contained 2,401 tracked files, 417 bilingual HTML pages, 536 assets, 858 archive files and 167 evidence files.

## 2. Public repair evidence

- PR #919 merged as `a4f8c461058216ed3ec0182896fca2c4bc3c8d9e`.
- Exact tree: `0f8efa58f56490c99cc85e3ea30362e547e30e92`.
- GitHub Pages run `32726738047` completed successfully.
- Exact repair release was publicly read back on both homepages and the then-declared fourteen direct surfaces.

The final re-digest found one important omission in the original lock: the canonical Spanish Judge route is `es/concurso-36-2012-magistrado-juez/`, while the smaller `es/concurso-36-2012-juzgado-mercantil-1/` route is a legacy surface. The final guard protects and tests both. It does not silently redirect or remove either route.

The first CI pass for the final guard also exposed two older composition defects rather than missing actor content. On the RICPE routes, `asset-recovery-preservation-20260821.js` did not recognise `.dossier-hero` and could prepend its gateway before the real hero; on the takeover routes, `art1535-reserve-pathway-20260819.js` had the same omission for its Article 1535 reserve card. A grouped test selector then treated the prepended generic section as `section:first-of-type`. RICPE also had an older source-of-funds observer competing with the five-actor observer for the same post-hero slot. The final guard corrects the two hero selectors, places the source-of-funds section after the locked actor component, cache-busts both repaired loader chains and resolves the hero in explicit priority order. The render check now proves 500 ms of continuous first-read adjacency and scrolls lazy evidence images into view before requiring non-zero natural dimensions; exact counts, file paths and placement requirements remain unchanged.

## 2A. Final guard, deployment and live-readback evidence

- Authorized source commit: `e02172937ce32fbda42654093b4831ab1b3dcd7d`.
- PR [#922](https://github.com/sbu001monterecco/por-derecho/pull/922) passed the required source, preservation and rendered checks at final head `850ee0909f6eb5914d2ced3a366d5576b28b6768`.
- The guard merged to `main` as `ed98b0ac634afc34f00a425e9ed67ca58fd77cb8`, exact tree `af1d15bf6e8418767fdeea80082fbdb15dc2d692`.
- [GitHub Pages run 32750603024](https://github.com/sbu001monterecco/por-derecho/actions/runs/32750603024) completed successfully at `2026-08-24T16:24:54Z` with head SHA exactly equal to the guard merge.
- [Actor live run 32750605646](https://github.com/sbu001monterecco/por-derecho/actions/runs/32750605646) reached `RENDER_VERIFIED` at `2026-08-24T16:27:17.010Z`: **757 assertions across all 17 protected surfaces**. It verified five separate actor cards, two distinct institutional cards and role labels, five complete actor-specific five-cell linkage rows, descriptions, direct allegations, contrary boundaries, stable first-read pins, actor portraits and both evidence images.
- [Source-of-funds run 32750605643](https://github.com/sbu001monterecco/por-derecho/actions/runs/32750605643) also passed on attempt 2 after the same propagation interval. The actor source verifier completed on attempt 8.
- The exact guard inventory is **2,427 tracked files / 420 bilingual HTML pages / 541 assets / 865 archive files / 167 evidence files**.

The post-merge sweep also exposed two stale **monitor assumptions**, not missing public content. The criminal-engineering and 2022-adjudication live jobs both passed their rendered-DOM and substantive route checks but their raw-source polls still expected final modules directly in an older loader. The executable architecture is now a three-hop chain: `site.js` → `site-pre-intervencion-highlight-20260820.js` → `site-pre-intervencion-highlight-before-eg95-20260823.js` → the final case/adjudication modules. This closeout control release makes both polls verify every exact loader hop and data attribute while retaining the direct-module, route, sitemap, anonymisation, bid and rendered-DOM checks.

## 3. Durable preservation controls in this package

- `AGENTS.md` makes current remote `main` the editing baseline and prohibits stale-snapshot overwrite.
- `ops/REPOSITORY_PRESERVATION_CONTRACT.json` records repository inventory floors, protected paths, exact routes, names, roles, assets, structure and evidential boundaries.
- `scripts/validate_repository_preservation.py` blocks protected deletion/rename without a newly added, exact-base authorization record; it also validates local uncommitted work against `origin/main`.
- `operations/preservation-authorizations/README.md` defines the only acceptable deletion-authorization record.
- The settled-DOM verifier covers both homepages, fourteen canonical direct routes and the preserved legacy Spanish court route. It checks five full cards, two full institutional cards, five full linkage rows, stable IDs, seven reciprocal dossier links, approved images, role separation, first-read placement and prohibited identity drift.
- The preservation gate locks the `.dossier-hero` placement selectors and their cache-busted loader versions so older gateways cannot again be prepended ahead of the protected direct-route first read.
- The scheduled live workflow runs every six hours and includes every protected route in its source trigger set.

## 4. Content boundaries preserved

The five private actors remain individually named and described:

1. Francisco Mario Matos Matas;
2. Antonio Cogolludo Rojas;
3. Shaila María Cogolludo Ramos;
4. José Daniel Acosta Matos;
5. Laura Patricia Acosta Matos.

Francisco de Borja Rodríguez-Batllori Laffitte remains a separate court-appointed, judicial-adjacent Insolvency Administrator—not a private actor and not the judge. Alberto López Villarrubia remains a separate Magistrate-Judge exercising judicial power. No relationship transfers conduct, knowledge, intention or responsibility. Allegations, acts or commissions, omissions, contrary material, unresolved proof and right-of-reply boundaries remain separate from adjudicated outcomes.

Only the verified repository portraits for Francisco Mario Matos Matas, the Insolvency Administrator and the Magistrate-Judge may be used in those named-person slots. The absence of four other verified portraits cannot be filled by generation or visual inference.

## 5. Open improvements preserved outside chat

Every material recommendation from the re-digest is assigned in:

`ops/FIVE_ACTOR_PRESERVATION_AND_READER_JOURNEY_BACKLOG.md`

The highest-value improvements are to derive static and enhanced presentations from one structured proposition record, make every direct route static-first, show attribution/non-adjudication/strongest anchor/contrary fact/decisive proof in the first read, complete the four thinner actor dossiers, reconcile route-registry/sitemap/hreflang coverage, enforce required GitHub checks and create an exact latest-release independent recovery checkpoint.

These are durable open governance items, not reasons to retain the chat after the final guard is merged and live-verified.

## 6. Final deletion-safety determination

Every objective gate is now satisfied: the source is recoverable in public Git, PR #922 passed the required controls, the exact merge SHA was published by Pages, all seventeen protected surfaces passed settled-DOM live readback, and the manifest records the exact PR, head, merge, tree, Pages run, live run and verification time.

No unique substantive source, actor description, allegation, image, institutional-role boundary, linkage record, recovery instruction or open recommendation remains only in the originating chat or worktree. The unresolved governance items—required-check enforcement in issue #355 and a fresh independent recovery checkpoint in issue #356—remain durably assigned in `ops/FIVE_ACTOR_PRESERVATION_AND_READER_JOURNEY_BACKLOG.md`; they do not require retention of this chat.

This thread is therefore **safe to delete with open governance items**. Deleting it does not authorize removal, demotion, abridgement, collapse, relabelling or unlinking of any protected material. The five private actors must remain separate; the court-appointed, judicial-adjacent Insolvency Administrator and the Magistrate-Judge must remain distinct institutional roles; and every allegation must remain separated from an adjudicated finding, contrary material and proof outstanding.
