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

## Validation targets

- repository preservation validator
- publication integrity validator
- audience experience validator
- rendered Cuatrecasas EN/ES insert
- book EN/ES cover read-back
- exact-sha Pages deployment
- production HTTP checks for the two Cuatrecasas routes, two book routes and cover asset
