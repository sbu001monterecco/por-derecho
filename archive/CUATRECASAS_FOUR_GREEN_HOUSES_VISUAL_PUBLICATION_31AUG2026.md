# Cuatrecasas / Four Green Houses visual publication — 31 August 2026

## Scope

Add the newly generated original editorial artwork for **4 Green Houses, One Red Hotel** to the existing locked book-cover path and interlink the bilingual Cuatrecasas Sun Park pages to the existing bilingual book landing pages.

## Publication design

- Replace `assets/book-covers/locked/four-green-houses-one-red-hotel.jpg` in place so the existing book pages and existing `og:image` reference inherit the new cover without route churn.
- Add `assets/cuatrecasas-four-green-houses-one-red-hotel-cover-20260831.js`, self-limited to `/en/cuatrecasas-sun-park/` and `/es/cuatrecasas-sun-park/`.
- Extend `assets/site.js` additively to load the new self-limiting insert while preserving the 31-August Cuatrecasas LinkedIn record loader and inherited site-loader chain.
- The Cuatrecasas insert links EN → `/en/books/four-green-houses-one-red-hotel/` and ES → `/es/libros/four-green-houses-one-red-hotel/`.

## Editorial and evidential boundary

The cover is an original visual metaphor. Four generic green architectural houses surround a real-world red hotel under legal/economic pressure. The artwork is not evidence, does not establish liability, and does not assert that Cuatrecasas or any other actor joined a common plan. The public insert says so expressly.

The visual gives only a conceptual nod to the generic houses-to-hotel idea associated with property games. It does **not** use the Monopoly® logo, board, mascot, cards, branded typography or branded toy-piece design. No affiliation or endorsement is represented.

## Preservation

No route, source, allegation, qualification, image or prior Cuatrecasas/LinkedIn publication is removed. The book-cover path is intentionally stable. Existing EN/ES book routes and Cuatrecasas routes are preserved.

## Publication closeout

- Publication PR: **#1268** — `Publish Four Green Houses cover and link Cuatrecasas record`.
- Merge SHA: **`840ddd837f9e6232510f5e0098f1562d4f7795ff`**.
- Exact-SHA GitHub Pages run: **33395894569 / #1331** — completed successfully.
- PR publication-integrity gate: **33395641595** — success.
- PR audience-experience gate: **33395641625** — success.
- PR visual-asset identity gate: **33395641690** — success.
- Published cover control: JPEG, **900 × 1125**, **221,210 bytes**, SHA-256 **`0476f4fab7e8fa15451d30d6badc81623781db3c3058edd09d3d788013062b34`**.

## Permanent live-verification control

The existing `scripts/validate_cuatrecasas_book_live.py` / `Validate Cuatrecasas book live publication` workflow is extended as the production-edge control for this release. From an external GitHub-hosted runner it checks, with cache-busting:

1. the established EN/ES book routes;
2. the established EN/ES Cuatrecasas critical-gap routes;
3. the EN/ES Cuatrecasas Sun Park source pages and their `assets/site.js` dependency;
4. the live `assets/site.js` loader markers;
5. the live self-limiting Cuatrecasas/book insert and both language-specific book links;
6. the exact live JPEG byte length and SHA-256.

This is stronger than relying on an indexed crawler snapshot because the Cuatrecasas cover section is inserted client-side by JavaScript.

## Validation targets

- repository preservation validator
- publication integrity validator
- audience experience validator
- visual asset identity validator
- exact-sha Pages deployment
- external production HTTP checks for Cuatrecasas EN/ES, book EN/ES, critical gaps EN/ES, loader, insert and cover bytes
