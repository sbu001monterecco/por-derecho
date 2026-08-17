# CALIFICACIÓN — READER EXPERIENCE IMPLEMENTATION

**Date:** 17 August 2026  
**Status:** implementation record / deletion-continuity control  
**Branch:** `agent/calificacion-ux-reader-journey-17aug2026`  
**Routes preserved:**

- `/es/calificacion-concurso-36-2012-vidas-paralelas/`
- `/en/insolvency-classification-parallel-lives/`

## Purpose

Implement the high-priority user-experience and evidential-navigation improvements identified by the unitary repository, website, Gmail and files audit without weakening, deleting or replacing the substantive accusations.

The design rule is:

> exact first-instance result → rejected/narrowed branches → appeal status → serial audits → evidence before actor → recovery/counter-record → Gil Marer’s accusation → connected context.

## Public implementation

A new bilingual runtime module is added:

- `assets/calificacion-reader-experience-20260817.js`

It is loaded from:

- `assets/site.js`

The module applies only to the two canonical Calificación landing routes.

## Reader-facing changes

1. Adds a 30-second guided gateway immediately after the existing hero.
2. Preserves and promotes the canonical AC → Fiscalía → judgment → appeal map.
3. Preserves the existing 90-second professional read.
4. Creates a compact A01–A06 serial-navigation index.
5. Converts the full A01–A04 public audits into expandable records rather than deleting them.
6. Adds the central `EVIDENCE BEFORE ACTOR` matrix using only:
   - PROVED BEFORE ACTOR;
   - STRONG TRANSMISSION INFERENCE;
   - INSTITUTIONALLY AVAILABLE ONLY;
   - NOT YET PROVED.
7. Places documentary architecture and counter-record before the strongest judicial-criminal accusation.
8. Keeps the direct accusation against Magistrate Alberto López Villarrubia complete and visible under a stable anchor.
9. Moves wider connected material—material control, LPAM/CGPJ, CaixaBank, elEconomista and same-asset/multiple-financial-lives material—into one expandable context dossier.
10. Adds `WHAT WOULD CHANGE OUR VIEW?`, corrections and right-of-reply controls.
11. Updates the visible page date to 17 August 2026 at runtime.
12. Adds mobile, keyboard-focus and print rules.

## Substantive controls

The implementation does **not**:

- rename either canonical route;
- remove the accusation of judicial prevarication;
- remove the €3,032,010.34 allegation;
- remove the AC/Fiscal accountability allegations;
- describe an appeal as successful or final;
- convert institutional possession into personal judicial knowledge;
- treat the June 2018 transaction architecture as unconditional finance or completed drawdown;
- treat a draft as filed;
- treat wider CAM/RICPE, CGPJ, media, banking or public-funds questions as already adjudicated facts.

## Current serial status surfaced

- A01–A05: deep audit complete.
- A06: next separate audit unit.
- A05 remains rejected at first instance while the actual payment route remains an open tracing question.

## Technical approach

The current site is assembled from many independent runtime modules. This implementation is a controlled P0/P1 orchestration layer, not the final P2 build-system refactor.

It:

- waits for earlier dynamic modules to settle;
- applies an idempotent deterministic order;
- observes only top-level `main` insertions for a bounded period;
- preserves every underlying module in the DOM;
- wraps, moves or groups content rather than deleting it;
- retains print visibility for expandable context.

## Validation required before merge

- JavaScript syntax check for `assets/site.js` and the new UX module;
- compare branch against current `main`;
- review changed-file patch;
- confirm ES/EN wording parity;
- confirm canonical route files are unchanged;
- confirm no source binary or private evidence was added;
- merge through PR;
- verify GitHub Pages build is `built` with no error and points to the merge commit;
- recheck both canonical URLs after deployment.

## Deletion-continuity conclusion

A fresh ChatGPT can recover the purpose, exact public files, reader-order logic, evidential grades, route-preservation decision, substantive boundaries and deployment requirements from this record and current `main` after merge. No private or privileged source is added to the public repository by this implementation.
