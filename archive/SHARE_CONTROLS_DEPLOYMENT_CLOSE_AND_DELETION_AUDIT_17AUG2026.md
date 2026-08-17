# SHARE CONTROLS — DEPLOYMENT CLOSE + THREAD DELETION AUDIT

**Control date:** 17 August 2026  
**Primary PR:** #325 — `Add canonical site-wide sharing and redesign continuity`  
**Squash merge commit:** `9f543a2e6e313a440938bded9336f556e0e667eb`  
**Repository state:** MERGED TO `main`  
**Pages state observed after merge:** GitHub Pages accepted the new `main` and reported `building`; source remained `main` at `/`, with HTTPS enforced.

## Supersession notice

This file closes and supersedes the `pending` values in the final section of `archive/SHARE_CONTROLS_SITEWIDE_IMPLEMENTATION_17AUG2026.md`.

## Verified on `main`

- `assets/share-controls-20260817.js` — canonical share/deep-link engine.
- `assets/share-controls-20260817.css` — restrained responsive/accessibility layer.
- `assets/book-page-share-20260815.js` — compatibility bridge preserving established book markup.
- `assets/site.js` — cross-site loader.
- `archive/SHARING_AND_DEEP_LINK_DESIGN_CONTINUITY_CONTRACT_17AUG2026.md` — future-redesign non-regression contract.
- `archive/SHARE_CONTROLS_SITEWIDE_IMPLEMENTATION_17AUG2026.md` — implementation record.
- `SHARING_DESIGN_CONTINUITY.md` — root discovery pointer.

## Functional state

The merged implementation provides LinkedIn, WhatsApp, Email and Copy Link; canonical URLs for normal page shares; query/hash stripping on fallback URLs; deliberate stable evidence/proposition anchors through `data-share-anchor` / `data-share-id`; ES/EN labels and feedback; preservation of the flagship book placement; automatic compact page sharing on substantive pages loaded through `site.js`; exclusion of language roots/legal/privacy/contact/FAQ routes; no third-party social SDK or tracking dependency; and keyboard/mobile focus and target-size support.

## Future redesign lock

Future presentation/framework changes may not silently remove or materially degrade page sharing, contextual/evidence deep links, canonical URL semantics, ES/EN parity, social-preview quality, mobile/accessibility behaviour, Copy Link as a professional action, or the privacy posture. The controlling contract is `archive/SHARING_AND_DEEP_LINK_DESIGN_CONTINUITY_CONTRACT_17AUG2026.md`.

## Hard deletion audit

> If this chat disappeared now, could another thread open `main`, discover the current sharing implementation, understand what changed, know what must survive a future redesign, and continue toward evidence/proposition-level deep links without conversational memory?

**YES for repository/design continuity.** Recoverability is provided by the root pointer, implementation record, continuity contract, runtime asset names and PR #325 history.

## Explicit remaining boundary

At the time of post-merge observation GitHub Pages reported `building`, not yet `built`. Therefore this record does not falsely claim a completed rendered-browser smoke test. That is a deployment-observation item, not an implementation gap.

Object-level deep-link rollout is intentionally progressive: the engine supports stable IDs/anchors now but does not invent anchors for evidential objects whose canonical IDs are not yet attached to page markup.

## Readiness

- repository implementation: **100% merged**;
- existing book share preservation: **100% source-verified**;
- cross-site page-share engine: **100% merged**;
- ES/EN engine parity: **100% implemented**;
- future redesign continuity: **100% preserved in repository controls**;
- stable object/evidence deep-link engine capability: **100% implemented**;
- object-by-object anchor adoption: **progressive / not claimed complete**;
- Pages deployment observation: **build accepted; completion to be independently observed**.
