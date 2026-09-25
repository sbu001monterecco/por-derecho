# OPTIMUM USER JOURNEY — EXECUTION PROMPT

**Date:** 18 August 2026  
**Mode:** implementation, not consultancy  
**Website:** Por Derecho / Project Sun Rock  
**Primary objective:** maximise comprehension, verification, institutional action, right of reply and recovery support without weakening evidence, multiplying pages or obscuring the Project’s substantive position.

## Mission

Scan the current deployed/source website and implement the smallest high-confidence set of changes that makes every major reader journey progressive, obvious and objective-aligned.

The site must support four legitimate reader intentions:

1. **Understand quickly** — a first-time reader understands the central sequence in 60 seconds.
2. **Verify deeply** — a sceptical professional can reach sources, evidence states, contradictions and open questions without accepting the whole theory.
3. **Act within competence** — a public office, RICPE function or adviser sees its finite question, production request and next lawful step.
4. **Engage with recovery** — a reader can inspect recovery/restitution objectives, provide a documented correction or contribute relevant evidence without confusing advocacy with proof.

A valid result may be to freeze a page that is already working. Do not manufacture change.

## Non-negotiable objectives

The journey must strengthen, not dilute:

- the one-hotel / multiple-legal-layers reconstruction;
- the July-2021 RICPE hinge and `WHAT CHANGED?` question;
- the Comunidad → practical control → project-availability dependency test;
- source-specific number control;
- the distinction between allegation, inference, verified fact and official status;
- public-office competence boundaries;
- correction and right-of-reply discipline;
- asset, income, damages and platform-recovery objectives;
- and the reader’s ability to identify exactly who can produce the missing document.

Do not optimise merely for neutrality. Optimise for **credible documentary pressure**: the strongest supported proposition, stated at the correct evidential level, delivered in the clearest sequence.

## Personas to simulate

Run the journey as:

- first-time general reader;
- RICPE director / Compliance;
- CNMV supervisor;
- Regional Incentives officer;
- SNCA / ERDF auditor;
- prosecutor or judicial reader;
- forensic accountant;
- journalist;
- investor;
- affected owner / witness;
- returning reader;
- and a person willing to submit correction or evidence.

## Success metrics

A reader should be able to achieve:

### 30 seconds

- identify the physical/economic subject;
- understand why the page matters;
- choose the correct route.

### 2 minutes

- understand the central contradiction or transition;
- distinguish what is proved from what remains open.

### 7 minutes

- identify the first five decisive documents/events;
- know what that reader or institution can verify;
- know what record would resolve the main gap.

### 20 minutes

- understand the dependency chain;
- inspect evidence status and contrary material;
- reach the full dossier without being forced through irrelevant biography or duplicated allegation modules.

### Return visit

- identify the latest verified material change quickly;
- avoid rereading the entire dossier;
- see the current institutional-status ledger.

## Required UX architecture

### A. One unified reader-intent selector

On the homepage, replace overlapping route modules with one clear selector:

- Understand in 60 seconds;
- Review as an institution/professional;
- Audit the evidence;
- Recovery, correction and contribution.

Do not present more than four equal-priority choices.

### B. Reading-depth control

On major substantive routes provide a compact, accessible switcher:

- Quick orientation;
- Guided / seven-minute read;
- Full record.

Use stable anchors or canonical deeper routes. Do not hide evidence; provide progressive access to it.

### C. One current step

Repair the unitary journey rail so only one item can be `aria-current`. Remove semantic duplication and ensure labels match destinations.

### D. Explicit exits

At the end of each major route add:

- previous/context;
- next logical stage;
- full evidence or clean-room route;
- documented correction / evidence contribution / recovery route, according to audience.

A reader should never finish a long page without knowing the next best step.

### E. Returning-reader support

Display the latest controlled material update in a compact form. Use local browser storage only to distinguish a first or earlier visit; do not use tracking or external analytics.

### F. Reading progress

Use a non-intrusive progress indicator on long pages, respecting reduced-motion preferences and accessibility.

## Cognitive-load rules

- Remove or supersede duplicated homepage journey modules.
- Do not add another general dossier page.
- Do not repeat the whole multiple-funding allegation before every specialist question.
- Do not remove deep evidence merely because it is long.
- Prefer clear ordering, progressive disclosure, anchors and next-step controls.
- Preserve existing stable URLs and deep links.
- Keep mobile controls compact and non-obstructive.

## Implementation rules

1. Scan the current source and loader order first.
2. Create a controlled branch.
3. Implement shared ES/EN components with route-specific configuration.
4. Load the optimum-journey layer last so it can resolve—not multiply—earlier presentation layers.
5. Keep all modules idempotent.
6. Do not expose private channel credentials or unnecessary personal data.
7. Preserve source-specific figures and current status grammar.
8. Add automated source and browser-render tests.
9. Capture desktop and mobile screenshots as CI artifacts.
10. Inspect the screenshots before merge and correct any visible regression.
11. Merge through a PR only after checks pass.
12. Preserve a deletion-continuity and deployment record.

## Browser acceptance tests

Run the complete route suite at the representative 390×844 phone,
900×1280 Android-tablet and 1440×1000 desktop profiles. Verify at minimum:

- both homepages;
- main RICPE route;
- CNMV;
- Regional Incentives;
- SNCA / ERDF;
- Comunidad;
- 7 June 2018;
- multiple financial lives;
- English CNMV.

In addition, run the bilingual homepage accountability regression at:

- 320×568 — very small phone;
- 360×800 — small Android phone;
- 390×844 — modern phone;
- 412×915 — large Android phone;
- 844×390 — landscape phone;
- 768×1024 — tablet portrait;
- 900×1280 — Android tablet portrait;
- 1024×768 — tablet landscape;
- 1119×800, 1120×800 and 1121×800 — both sides of the compact-menu breakpoint;
- 1366×768 — laptop;
- 1440×1000 — desktop; and
- 1920×1080 — large desktop.

For each bilingual homepage profile, inspect the static navigation immediately,
inspect it again after at least 8.5 seconds so the delayed optimiser has run,
then repeat the post-optimiser check after a normal reload. Assert:

- exactly one `.main-nav .nav-accountability` link at every phase;
- exact label and destination: Spanish `AC y Juez` →
  `#institutional-accountability-12aug`; English `AC & Judge` →
  `#institutional-accountability-12aug-en`;
- the destination fragment exists;
- the link retains burgundy `#6f2423` and white text;
- at widths up to 1120 px the compact menu opens, reports
  `aria-expanded="true"`, exposes the link fully inside the viewport, provides at
  least a 24×24 CSS-pixel target and accepts a centre-point tap;
- above 1120 px the compact toggle is hidden and the link is directly visible,
  unobscured and clickable;
- the click reaches the exact language-specific fragment; and
- the link is never duplicated, clipped, covered or removed by the delayed
  optimiser or by a cached reload.

Across the complete suite also assert:

- no horizontal body overflow;
- no duplicate IDs;
- recipient-specific hero is the first visible substantive module;
- unified homepage intent selector exists;
- depth selector exists on major pages;
- next-step panel exists;
- journey rail has no more than one current step;
- compact controls do not obscure content;
- internal links resolve; and
- ES/EN equivalent propositions remain equivalent.

Capture the closed header and every opened compact menu as CI artifacts. A DOM
match alone is not a pass: the accountability route must be visibly rendered,
within the viewport and usable by tap or click.

## Final decision gate

After implementation answer:

- Did comprehension improve?
- Did institutional usefulness improve?
- Did evidential pressure remain at least as strong?
- Did right-of-reply and correction remain visible?
- Did recovery objectives remain accessible?
- Did page count and cognitive load stay controlled?
- Did rendered mobile and desktop tests pass?

If yes, merge and freeze the architecture pending a genuinely material new event.

**Final principle:**

> Guide first. Prove second. Let the reader deepen voluntarily. Keep the strongest supported allegation intact. Make every next step obvious.
