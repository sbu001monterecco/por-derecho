# UNITARY PUBLIC SHELL — DISCOVERY SYNC CLOSEOUT

**Date:** 19 August 2026  
**Status:** `MERGED · CI GREEN · PUBLIC-EDGE LIVE READBACK NOT INDEPENDENTLY CLAIMED`  
**Controlling PR:** #438  
**Merge SHA:** `c0f581d7306e54f15abb062493fc7d312bd635c6`

## Result

The post-shell discovery synchronization is complete at repository/source level.

The unitary Case Control Room remains a six-system architecture. The release does not add a new top-level system. Instead it integrates later public work into the appropriate existing lanes:

- DP1041 / Article 1535 → Concurso / creditor / recovery chain;
- Cuatrecasas lifecycle and ICAM/CCACM → institutional / professional answer-holder chain;
- two-track Community/CEXP governance visual → Community / CEXP evidence lane.

## Search architecture now in force

Controlled search now combines:

1. the original curated route registry;
2. the 19 August additive synchronization registry;
3. every same-project sitemap declared in `robots.txt`.

This fixes the earlier discovery-drift risk in which a specialist public route could exist and be sitemap-listed without being guaranteed to appear in the unitary search fallback.

The generic fallback was tested independently of the additive registry by searching for the PwC Canarias / Carlos Saavedra route through the already-declared PwC specialist sitemap.

## Validation evidence

Final PR-head checks:

- publication-integrity run: `32212319992` — PASS;
- supervisory-practice run: `32212319979` — PASS;
- unitary browser run: `32212319981` — PASS;
- browser artifact: `9351187726`;
- artifact SHA-256: `93937d33e59fbf953790c6d09916d0a7b44373384df55a5ed4c1c2e03795f5f4`.

The browser suite used Google Chrome `151.0.7922.108` through Playwright and rendered 17 route archetypes at desktop and mobile widths: **34 successful renders**.

Required search paths passed:

- CEXP — original curated-index continuity;
- 1041 — DP1041 synchronization;
- Cuatrecasas — professional-lifecycle synchronization;
- capture hypothesis / hipótesis de captura — governance visual under controlled hypothesis framing;
- PwC Canarias / Carlos Saavedra — generic specialist-sitemap fallback.

All tested routes were page-level horizontal-overflow free.

## Defects found and corrected before merge

The expanded test surface found genuine inherited mobile issues rather than search failures:

- EN DP1041 evidence table overflow;
- ES DP1041 evidence table overflow;
- EN governance-hypothesis status-pill overflow;
- ES governance-hypothesis status-pill overflow.

The shared responsive shell now makes evidence tables horizontally scrollable within their own page width and permits long hypothesis pills to wrap. The tests were rerun after those corrections and passed.

## CI reliability improvement

The browser workflow no longer downloads a separate Playwright Chromium build and Linux dependency bundle on each run. It installs the Playwright Node package and uses the preinstalled Chrome available on GitHub's Ubuntu runner.

This change does not weaken the assertions. It removes a network-heavy and previously slow browser-install step while preserving the same browser-render, search, DOM and overflow checks.

## Evidential boundaries preserved

### DP1041 / Article 1535

The unitary shell does not state that Article 1535 certainly applied or that LPB had a guaranteed winning claim. It does not attribute termination of the DP1041 route to the insolvency administration without the exact primary cessation act and instruction. Directional effects do not establish collusion, corruption or improper judicial bias.

### Cuatrecasas / ICAM / CCACM

A professional-conduct complaint remains an allegation. An archive based on limitation or territorial competence is not a merits ruling on whether conduct was proper. A pending appeal does not imply that the complaint will succeed. No privileged advice is reproduced by the synchronization layer.

### Community / CEXP governance

“Capture” remains a hypothesis to be tested meeting by meeting against authority, notice, attendance, voting entitlement, debt calculation, documentation and legal effect. A numerical minority or disputed minute does not by itself prove invalidity or capture.

### Search

Search is discovery metadata. It does not create, strengthen or adjudicate a factual, professional, civil or criminal conclusion.

## Deletion audit

PR #438 changed 15 files with 490 additions and 37 deleted lines.

The 37 deleted lines are replacements inside synchronized navigation/search/workflow/CSS files. No canonical public dossier was deleted. No public route was deleted. No original unitary publication manifest was overwritten. DP1901 procedural separation remains intact. The six-system Control Room structure remains intact.

**Substantive public-route deletions: 0.**

## Live-state boundary

The implementation is merged and source-verified. GitHub Actions successfully rendered the production `/por-derecho` subpath locally in the workflow environment.

This closeout does not convert that fact into an independent public-edge `LIVE_VERIFIED` claim. Public-host readback is a separate verification state.
