# Five-actor visibility and preservation thread — 24 August 2026

**Current verdict:** `PENDING_FINAL_GUARD_MERGE_AND_LIVE_VERIFICATION`

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

## 6. Final deletion condition

This audit may be changed to `DELETION_SAFE_WITH_OPEN_GOVERNANCE_ITEMS` only after:

1. the final preservation guard is merged to `main`;
2. required source and rendered checks pass;
3. GitHub Pages publishes the exact guard release;
4. all seventeen declared live URLs are read back with the exact protected markers; and
5. the publication manifest records the PR, merge SHA, workflow run and verification time.

Until then, this thread is **not yet declared safe to delete**.
