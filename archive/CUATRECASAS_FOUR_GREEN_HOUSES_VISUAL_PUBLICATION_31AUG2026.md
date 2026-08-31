# Cuatrecasas / Four Green Houses visual publication — 31 August 2026

## Scope

Publish the original editorial artwork for **4 Green Houses, One Red Hotel** and interlink the bilingual Cuatrecasas Sun Park pages to the existing bilingual book landing pages.

## Publication design

- PR #1268 first replaced the established fallback path `assets/book-covers/locked/four-green-houses-one-red-hotel.jpg` and added the self-limiting Cuatrecasas/book loader.
- The bilingual Cuatrecasas insert links EN → `/en/books/four-green-houses-one-red-hotel/` and ES → `/es/libros/four-green-houses-one-red-hotel/`.
- `assets/site.js` remains the additive global loader and preserves the pre-existing Cuatrecasas LinkedIn record loader and inherited site-loader chain.

## Editorial and evidential boundary

The cover is an original visual metaphor. Four generic green architectural houses surround a real-world red hotel under legal/economic pressure. The artwork is not evidence, does not establish liability, and does not assert that Cuatrecasas or any other actor joined a common plan. The public insert says so expressly.

The visual gives only a conceptual nod to the generic houses-to-hotel idea associated with property games. It does **not** use the Monopoly® logo, board, mascot, cards, branded typography or branded toy-piece design. No affiliation or endorsement is represented.

## First publication and exact-SHA deployment

- Publication PR: **#1268** — `Publish Four Green Houses cover and link Cuatrecasas record`.
- Merge SHA: **`840ddd837f9e6232510f5e0098f1562d4f7795ff`**.
- GitHub Pages run: **33395894569 / #1331** — completed successfully for that exact merge SHA.
- PR publication-integrity gate: **33395641595** — success.
- PR audience-experience gate: **33395641625** — success.
- PR visual-asset identity gate: **33395641690** — success.

## Production-edge cache finding

A fresh external GitHub-hosted HTTPS verification after the successful Pages deployment established that the new JavaScript loader and Cuatrecasas insert were live, but the reused stable JPEG URL still returned the previous cached cover:

- stable URL returned **7,510 bytes**;
- stable URL SHA-256: **`9a1befa4588f24d18787f97d5ab3c582d2f0f67a3c25c824ad870ebfa6e30067`**;
- approved new cover is **221,210 bytes**, **900 × 1125**;
- approved new-cover SHA-256: **`0476f4fab7e8fa15451d30d6badc81623781db3c3058edd09d3d788013062b34`**.

This was a CDN/stable-filename publication mismatch, not a failure of the book or Cuatrecasas route HTML/JS. The failed verification artifact is preserved under Actions run **33396494161**, artifact **9759519353**.

## Cache-proof corrective publication

PR #1269 converts the cover publication to a unique immutable URL:

`assets/book-covers/locked/four-green-houses-one-red-hotel-20260831.jpg`

The versioned file uses the exact approved new-cover bytes. The old stable-path file is retained as a historical/no-JavaScript fallback; it is not deleted.

The self-limiting cover module is extended so that:

1. on the EN/ES Cuatrecasas Sun Park routes it renders the new versioned cover and links to the corresponding book landing page;
2. on the EN/ES book routes it replaces the visible fallback cover with the immutable versioned asset and marks it `data-versioned-cover="20260831"`;
3. in an interactive browser it also updates the `og:image` element to the versioned asset, while preserving the static source fallback rather than rewriting the book’s evidential content.

No book text, evidential proposition, allegation, route or prior image is removed by the cache-proof fix.

## Validation sequence

After PR #1269 passes the normal repository gates and is merged, the permanent Cuatrecasas/book production-edge validator must be updated in a separate closeout PR to verify from an external GitHub runner:

- EN/ES book routes;
- EN/ES Cuatrecasas routes;
- EN/ES critical-gap routes;
- live `assets/site.js`;
- live self-limiting cover insert;
- the exact immutable JPEG URL, byte length and SHA-256.

Only that external verification closes the publication as fully live-verified.
