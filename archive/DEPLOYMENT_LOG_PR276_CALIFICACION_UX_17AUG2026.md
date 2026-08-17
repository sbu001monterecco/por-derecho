# DEPLOYMENT VERIFICATION — PR #276 — CALIFICACIÓN READER EXPERIENCE

**Date (UTC):** 17 August 2026  
**Public change:** bilingual Calificación reader-experience and evidential-navigation redesign  
**PR:** #276 — `Improve the Calificación reader journey without weakening the allegations`  
**Merge commit:** `f23210c4df96eac5f79d85a6c1da5601f416c7af`

## Exact-SHA verification

- `main` was verified at exact merge commit `f23210c4df96eac5f79d85a6c1da5601f416c7af`.
- GitHub Pages build **1156249135** used that exact commit.
- Build status: **built**.
- Build error: **none**.
- Created: `2026-08-17T04:47:01Z`.
- Completed: `2026-08-17T04:47:19Z`.
- Duration: 18.340 seconds.
- Pages remains public, HTTPS-enforced and sourced from `main` at `/`.

## Merged source verified

The exact merge source contains:

- `assets/calificacion-reader-experience-20260817.js`;
- `assets/calificacion-reader-experience-finish-20260817.js`;
- the loader sequence in `assets/site.js`;
- `archive/CALIFICACION_READER_EXPERIENCE_IMPLEMENTATION_17AUG2026.md`.

The loader applies the two UX modules only to the established Spanish and English Calificación routes.

## Canonical URLs preserved

- `/es/calificacion-concurso-36-2012-vidas-paralelas/`
- `/en/insolvency-classification-parallel-lives/`

The source HTML files were not renamed, deleted or replaced. Their canonical and reciprocal `hreflang` declarations remain unchanged, so existing LinkedIn links continue to resolve to the same permanent routes.

## Public effect

The deployment adds:

- a 30-second guided read;
- the exact judgment/person/appeal pathway;
- a 90-second professional pathway;
- A01–A06 serial navigation;
- expandable A01–A04 full audits;
- the evidence-before-actor matrix;
- deterministic ordering before the direct prevaricación allegation;
- progressive disclosure for wider connected dossiers;
- correction, reply and falsifiability controls;
- deep-link, mobile, keyboard and print handling.

The direct accusation against Magistrate Alberto López Villarrubia, the €3,032,010.34 allegation and the AC/Fiscal accountability allegations remain in the public DOM and are not diluted or removed.

## External rendered-route check

A post-deployment attempt to retrieve the rendered Spanish and English GitHub Pages routes through the available web-fetch/cache path returned a cache-miss failure. This is recorded as an external inspection limitation, not as a failed deployment. Exact-SHA `main`, merged-source and successful Pages-build verification confirm publication of the intended source.

## Continuity

This file is an append-only deployment-log supplement for PR #276. It records the exact merge/build relationship and prevents a future thread from describing the UX work merely as merged but not deployment-verified.
