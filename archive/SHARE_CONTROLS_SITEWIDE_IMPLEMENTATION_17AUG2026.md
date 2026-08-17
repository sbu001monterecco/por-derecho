# SITE-WIDE SHARE CONTROLS IMPLEMENTATION — 17 AUG 2026

**Branch:** `feat/share-controls-continuity-20260817`  
**Status at creation:** implementation complete on branch; PR/merge/deployment fields to be closed after review.

## Baseline inspected

The established ES/EN flagship book pages already used a compact `.book-share` control immediately after the book thesis and before primary actions:

`LinkedIn · WhatsApp · Email · Copiar enlace / Copy link`

The legacy `assets/book-page-share-20260815.js` generated platform URLs locally and used the Clipboard API with fallback. The visual pattern was defined in `assets/book-pages-20260815.css` as compact, rounded, wrapping controls.

This implementation treats that pattern as the design ancestor rather than replacing it.

## Architecture implemented

### `assets/share-controls-20260817.js`

New canonical cross-site engine. It:

- derives the normal share URL from `<link rel="canonical">`;
- falls back to current origin/path with query/hash removed if canonical is missing;
- supports deliberate stable deep links through `data-share-anchor` or `data-share-id`;
- supports explicit share title/hook/url overrides for future evidence objects;
- generates LinkedIn, WhatsApp and Email URLs locally;
- uses Clipboard API plus a non-destructive prompt fallback;
- provides ES/EN labels and feedback;
- exposes `window.PorDerechoShare` so future components/redesigns can initialise share objects without duplicating logic;
- preserves existing `.book-share` markup;
- injects one compact page-level share module at the end of substantive pages that do not already contain a share scope;
- excludes ES/EN language roots, legal/privacy, contact and FAQ routes from automatic injection.

### `assets/share-controls-20260817.css`

A restrained extension of the existing book-page visual vocabulary. It preserves compact rounded controls, wrapping, visible keyboard focus and mobile touch targets. It also defines quieter future variants for contextual and evidence sharing.

### `assets/book-page-share-20260815.js`

Converted into a compatibility bridge. Existing book HTML is not rewritten. The bridge delegates to the canonical engine and avoids duplicate loading.

### `assets/site.js`

Loads the canonical sharing engine across site pages. On book pages it defers to the existing book-script bridge to avoid duplicate handlers.

## Representative source verification

Verified before PR close:

- `es/libro/index.html` — existing flagship placement, canonical/OG/hreflang and `.book-share` preserved;
- `en/book/index.html` — same established interaction in English;
- `es/calificacion-concurso-36-2012-vidas-paralelas/index.html` — substantive non-book route loads `assets/site.js` and declares a canonical URL;
- `en/insolvency-classification-parallel-lives/index.html` — corresponding EN route loads `assets/site.js` and declares a canonical URL.

The cross-site loader therefore reaches both representative non-book routes without page-by-page HTML duplication.

## Behavioural/editorial rules

The default is intentionally restrained: the system makes sharing easy without popups, fake urgency, fake social proof, gamification, tracking SDKs or coercive prompts.

The enduring sequence is:

**important content → comprehension → sharing opportunity → exact destination**

Copy Link is treated as a primary professional action, not an afterthought.

## Deep-link readiness

The engine is immediately capable of exact-object sharing when a component supplies stable `data-share-id` or `data-share-anchor`. This enables future ACTA, judicial-act, authority, ownership, debt, vote, transaction, funding, asset and other canonical proposition IDs without redesigning the share engine.

This pass does **not** fabricate anchors for objects that do not yet have stable IDs in page markup. Object-level rollout should attach only to canonical evidential identities.

## Future redesign continuity

Controlling contract:

`archive/SHARING_AND_DEEP_LINK_DESIGN_CONTINUITY_CONTRACT_17AUG2026.md`

Root discovery pointer:

`SHARING_DESIGN_CONTINUITY.md`

Future redesigns may replace current presentation/code, but must preserve or improve the capabilities in that contract.

## Accessibility / mobile

Implemented:

- semantic anchors for external share actions;
- semantic button for Copy Link;
- visible `:focus-visible` treatment;
- responsive wrapping;
- minimum 44px mobile targets on the cross-site component;
- local copied-state feedback;
- no icon-only controls.

## Privacy

No remote SDK, tracker or social widget was added. LinkedIn/WhatsApp are normal outbound share URLs; Email is `mailto:`; Copy Link uses native browser APIs.

## Social-preview boundary

The engine uses the page canonical/title/description for outbound payloads. Existing book Open Graph metadata remains untouched. This execution does not falsely claim that every historical page already has equally rich OG metadata; broader OG-image/content optimisation remains a progressive editorial task.

## Exclusions

Automatic injection currently excludes:

- `/es/` and `/en/` language home roots;
- legal/privacy routes;
- contact routes;
- FAQ routes;
- any page already carrying `.book-share`, `[data-share-scope]` or `.share-controls`.

These exclusions are deliberate to avoid indiscriminate social chrome.

## Readiness before merge

- canonical share engine: implemented;
- existing ES/EN book non-regression architecture: implemented;
- cross-site loader: implemented;
- representative ES/EN non-book reachability: source-verified;
- stable evidence-anchor capability: implemented, object-by-object adoption progressive;
- future redesign contract: preserved;
- root discoverability: preserved;
- dark-pattern prohibition: preserved.

## Closing fields

PR: pending at time this record was first written.  
Merge commit: pending.  
GitHub Pages build: to verify after merge.  
Rendered browser smoke test: to verify where the execution environment permits direct HTTP observation.
