# Five-actor visibility regression and repair — 24 August 2026

## Finding

The five-actor material was not deleted from the repository. It disappeared from the first rendered view because two independent runtime layers interacted incorrectly:

1. `homepage-actor-family-pwc-note-20260819.js` mounted the detailed five-actor component beside the legacy actor block.
2. `audience-experience-order-20260823.js` moved every homepage section not listed in `coreSections` into a closed `details` element labelled as the full record.

The audience-order layer protected the compact `.ac-dfa-update-section`, but it did not protect the actual `section[data-pd-five-ac]`. The detailed component therefore remained in the DOM but inside `[data-audience-full-record] details:not([open])`. The component also hid the legacy `.actor-intro` and `.actor-grid`, so the detailed and fallback versions were both invisible on first load.

## Amendment interaction

The progressive-collapse mechanism entered the homepage in commit `aff8bb0`. PR #914, commit `d08ba78` (`Publish five-actor criminal attribution and funded-exit obstruction control`), activated and expanded the five-actor component and updated the audience-order protection for the compact controlling allegation, but did not add the detailed five-box section to the protected sequence. PRs #915–#917 changed publication/control details without closing that selector and rendering-test gap.

This is therefore an activation/order regression, not a content-deletion event.

## Why existing checks passed

The release checks asserted that the compact `.ac-dfa-update-section` was present, named all five actors and remained outside progressive disclosure. They did not assert that the detailed five-box component itself:

- existed exactly once;
- was visible while the full record remained closed;
- contained five private-actor cards;
- placed the Insolvency Administrator and Judge immediately below those cards;
- loaded their portraits;
- contained five actor-specific private → Administrator → Judge linkage rows.

The source-only checks could not detect that a later runtime layer had moved a valid node into a closed container.

## Repair

The repair uses three independent safeguards:

1. **Static-first bilingual source:** `es/index.html` and `en/index.html` now contain the complete `section[data-pd-five-ac="20260824b"]` directly after the hero. It remains present if JavaScript fails.
2. **Protected runtime ordering:** the audience-order layer deduplicates and protects `section[data-pd-five-ac]`, places it after the compact controlling panel, excludes it from the collapsed full record, records `data-audience-protected-five-actor-visual="20260824b"`, and listens for `pd:five-actor-visual-ready`.
3. **Component and cache hardening:** the shared component supplies the same structure on the controlled dossier routes, uses a dedicated responsive stylesheet, dispatches a ready event and is cache-busted through the full loader chain.

The visible hierarchy is now:

1. five private-actor boxes;
2. immediately below, separate portrait/description cards for Francisco de Borja Rodríguez-Batllori Laffitte and Alberto López Villarrubia, each with alleged affirmative acts/commissions, omissions, a direct attributed allegation and mandatory contrary record;
3. five actor-specific linkage rows connecting alleged private conduct to the alleged Administrator and judicial act/omission, with decisive proof and non-transfer boundaries;
4. source-controlled visual evidence and correction/right-of-reply language.

## Evidence boundaries preserved

The repair preserves the direct allegations without converting them into findings. It expressly keeps the following boundaries visible:

- no automatic transfer of acts, intention or responsibility among the five actors;
- no claim that José Daniel Acosta Matos was physically present on 7 June 2018;
- Laura Patricia Acosta Matos’s exact mandate, presence and instruction remain proof questions;
- no fabricated common-company bridge for FMMM, Antonio and Shaila;
- the Administrator’s denial and narrower-authority account remain mandatory contrary evidence;
- the 2018 provisional dismissal and confirmation, CAM’s valid credit/titles, the 26 June 2018 suspension, 24 October 2019 non-validation and later corrective judicial material retain their exact scope;
- an adverse decision, error or delay does not by itself prove judicial prevarication;
- finance and sale routes retain their conditions and are not described as guaranteed exits.

## Regression gates

Source and browser gates now fail unless both language homepages render, before opening the full record:

- exactly one detailed component;
- exactly five private-actor cards;
- exactly two institutional cards;
- exactly five linkage rows;
- the FMMM, Administrator and Judge portraits loaded with non-zero natural width;
- all five private identities and both institutional identities present;
- commissions and omissions present;
- the component outside closed progressive disclosure;
- no horizontal overflow at mobile and desktop viewports.

