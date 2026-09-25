# OPTIMUM OBJECTIVE-ALIGNED USER JOURNEY — IMPLEMENTATION CONTROL

**Control date:** 18 August 2026  
**Implementation PR:** `#343 — Optimise objective-aligned reader journeys`  
**Implementation merge:** `6deaba19d8db5c5c5e20f2965ae8ab7deb28d8de`  
**Status:** MERGED INTO `main`; source verified; browser-render acceptance passed on the exact PR head before merge  
**Controlling prompt:** `archive/OPTIMUM_USER_JOURNEY_EXECUTION_PROMPT_18AUG2026.md`

## 1. Objective

The implementation optimises the site for four legitimate reader intentions without weakening the Project’s substantive case:

1. **Understand quickly** — a new reader can enter through a 60-second explanation.
2. **Verify deeply** — a sceptical reader can reach the complete evidential record, classifications, contradictions and open questions.
3. **Act within competence** — RICPE, CNMV, Regional Incentives, SNCA/ERDF and other practitioners receive a finite question, production route and lawful next step.
4. **Advance recovery, correction or contribution** — asset, income, damages and platform-recovery objectives remain visible, while documented corrections and evidence can be submitted through lawful routes.

The optimisation does not neutralise or dilute:

- the one-hotel / multiple-legal-layers reconstruction;
- the 20-Jul-2021 RICPE documentary hinge and `WHAT CHANGED?` question;
- the Comunidad → authority → material control → project-availability dependency test;
- source-specific financing-number control;
- institution-specific production requests;
- right-of-reply and correction discipline;
- or recovery/restitution objectives.

## 2. Implemented reader architecture

### 2.1 Homepage — one selector, four purposes

The homepage now has one controlling reader-intent selector instead of overlapping route modules:

- understand in 60 seconds;
- review by institution or competence;
- audit the evidence;
- recovery, correction and contribution.

The homepage hero calls to action are reduced to:

- choose my route;
- case in 60 seconds.

The desktop header is reduced to the principal destinations: case, recovery, evidence, institutions, future, updates, collaboration and language.

### 2.2 Progressive depth

Major routes receive a compact reading-depth control:

- orientation;
- guided / seven-minute read;
- full record;
- current status and material changes.

The control routes the reader to existing canonical anchors or deeper dossiers. It does not hide or delete evidence.

### 2.3 Recipient-first hierarchy

The implementation ensures the dedicated recipient hero is the first visible substantive module on tested routes. Earlier generic dynamic modules are moved below the recipient-specific hero and depth control.

This applies especially to:

- RICPE;
- CNMV;
- Regional Incentives;
- SNCA/ERDF;
- Community;
- 7 June 2018;
- multiple financial lives.

### 2.4 Compact, route-specific navigation

Long static navigation menus were reduced on the most important routes:

- homepage;
- main RICPE dossier;
- Community;
- 7 June 2018.

Static practitioner pages without a mobile menu now receive an accessible menu button with:

- `aria-expanded`;
- `aria-controls`;
- close-on-link;
- Escape-key closure.

### 2.5 Journey rail repair

The unitary rail now:

- removes the duplicated `Ownership` / `Community` opening;
- uses `Origin / Community` as the first stage;
- permits no more than one `aria-current="step"`;
- centres or aligns the current step on mobile;
- preserves stable route destinations.

### 2.6 Explicit exits

Major substantive routes now end with three clear actions:

- continue the sequence;
- verify through the correct control or clean-room route;
- act/respond through a documented correction, contribution or recovery route.

Each panel also includes previous context, case map, material updates and evidence contribution.

### 2.7 Return visits and reading progress

The site uses local-only browser storage to distinguish:

- first visit;
- current release;
- a new release since an earlier visit.

No external tracking or analytics is introduced.

Long pages receive a non-intrusive reading-progress line, with reduced-motion support and no print output.

## 3. Files introduced or materially changed

### Canonical prompt

- `archive/OPTIMUM_USER_JOURNEY_EXECUTION_PROMPT_18AUG2026.md`

### Shared implementation

- `assets/optimum-reader-journey-20260818.css`
- `assets/optimum-reader-journey-20260818.js`
- `assets/optimum-reader-journey-finish-20260818.js`

### Loader / duplication control

- `assets/ricpe-filed-status-20260817.js`
- `assets/supervisory-practice-entrypoints-20260818.js`

### Acceptance infrastructure

- `scripts/render_optimum_reader_journey.mjs`
- `.github/workflows/validate-optimum-reader-journey.yml`

## 4. Browser acceptance

### Exact tested head

`91434aa31c51112bbc9c4bc44663914929b6d962`

### Workflows

- `Validate supervisory-practice routes` — run `32124996920` — **success**.
- `Validate optimum reader journey` — run `32124996811` — **success**.

### Render matrix

Nine routes were rendered at two viewport sizes:

- homepage ES;
- RICPE ES;
- CNMV ES;
- Regional Incentives ES;
- SNCA/ERDF ES;
- Community ES;
- 7 June 2018 ES;
- multiple financial lives ES;
- CNMV EN.

Viewports:

- mobile: `390 × 844`;
- desktop: `1440 × 1000`.

Total combinations: **18**.

### Assertions passed

- recipient hero visible;
- recipient hero is the first visible main module;
- no horizontal body overflow;
- no duplicate IDs;
- no more than one current journey step;
- mobile menu exists;
- unified homepage selector exists;
- depth selector exists on major routes;
- next-step panel exists on major routes;
- reading-progress control exists.

The final diagnostics recorded `errors: []`.

### Screenshot artifact

- artifact ID: `9320082359`;
- name: `optimum-reader-journey-screenshots`;
- digest: `sha256:7cb82e807e88d74fb50372590a848b61ec0b10780e35939df526a807cd490c5f`;
- retention end: 1 September 2026.

The artifact contains top-of-page, homepage-intent and next-step screenshots plus JSON diagnostics.

## 5. Visual review conclusion

The captured routes were reviewed for:

- first-screen hierarchy;
- desktop navigation density;
- mobile navigation;
- current journey-stage visibility;
- practitioner shortcuts;
- homepage intent selection;
- next-step clarity;
- visual regressions.

Accepted results include:

- recipient-specific heroes govern Community, 7 June, funding, RICPE, CNMV, Incentives and SNCA pages;
- homepage presents the four reader intentions clearly;
- RICPE retains the 7-minute institutional path;
- practitioner pages surface seven-minute read, decision tree and good-practice/warning routes;
- mobile menus and journey controls remain usable;
- no tested route produced horizontal body overflow.

A minor cosmetic sliver of the preceding journey chip may remain visible on one narrow funding screenshot. The current `Funding` step remains fully visible and usable; this is non-material and not a delivery blocker.

## 6. Evidential and objective safeguards

The implementation does not change the evidence status of any proposition. It preserves:

- verified fact;
- verified with limit;
- actor/project representation;
- Project allegation;
- evidence-based inference;
- unresolved question;
- corrected/superseded;
- official procedural status.

It also preserves:

- alert ≠ proved fraud;
- filing ≠ admission ≠ examination ≠ decision;
- grant award ≠ payment ≠ final eligibility;
- ERDF plaque ≠ complete operation/audit file;
- multiple instruments ≠ proved duplicate funding;
- separate instruments ≠ proved absence of overlap;
- control/operation ≠ title;
- later title ≠ retrospective validation;
- referral ≠ merits acceptance.

## 7. Deployment status and freeze rule

The merge source is verified on `main`. The browser acceptance was performed against the production `/por-derecho` subpath using the exact PR head later squash-merged into `main`.

The public GitHub Pages host was not independently fetched from the working runtime. Therefore:

- repository delivery: complete;
- browser-render implementation validation: complete;
- live Pages propagation verification: still a separate finite check.

Absent a material new filing, response, correction or evidence event, the architecture should now be **frozen**. Further design changes require a demonstrated reader failure or material institutional need, not preference alone.
