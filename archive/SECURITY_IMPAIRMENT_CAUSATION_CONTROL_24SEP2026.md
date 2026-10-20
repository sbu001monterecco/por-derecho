# Security · impairment · causation — controlling correction

**Control:** PD-SP-TRACK-SECURITY-IMPAIRMENT-01  
**Date:** 24 September 2026  
**Status:** PUBLIC-SAFE LEGAL/CAUSATION FRAMEWORK — NOT A FINDING

## Controlling correction

Do not use the shorthand “the mortgage survives” as though formal survival answers the economic or legal consequences of creditor-attributable impairment.

The controlling proposition is:

> Formal survival of a mortgage/security right is analytically distinct from the creditor's net enforceable position if conduct legally attributable to that creditor is proved to have caused or contributed to impairment of the collateral, operating business, repayment source, due-diligence environment, valuation or replacement-financing package.

This is not a finding that CAM, any creditor, or any named person caused such impairment.

## Two-lane separation

1. **Real security/property:** mortgaged property, real-estate value, registered security, legally applicable improvements/indemnities.
2. **Operating/financing value:** access, CEXP/operating authority, customers/bookings, revenue, contracts, reputation, DD, valuation, replacement security and closing.

Economic interdependence does not make the lanes legally identical.

## Legal anchors

- Ley Hipotecaria arts. 109–110 — https://www.boe.es/buscar/act.php?id=BOE-A-1946-2453#a109
- Ley Hipotecaria art. 117 — https://www.boe.es/buscar/act.php?id=BOE-A-1946-2453#a117
- Código Civil art. 7 — https://www.boe.es/buscar/act.php?id=BOE-A-1889-4763#art7
- Código Civil art. 1101 — https://www.boe.es/buscar/act.php?id=BOE-A-1889-4763#art1101
- Código Civil art. 1902 — https://www.boe.es/buscar/act.php?id=BOE-A-1889-4763#art1902
- Código Civil arts. 1195–1196 — https://www.boe.es/buscar/act.php?id=BOE-A-1889-4763#art1195
- TRLC art. 153 — https://www.boe.es/buscar/act.php?id=BOE-A-2020-4859#a1-65
- Código Penal art. 263 — https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444#a263

### Legal ceilings

- LH 117 concerns deterioration caused by the owner; do not present it as the rule specifically governing creditor-caused impairment.
- CC 7 requires its own abuse-of-right elements; exercise of security is not automatically abusive.
- CC 1101 and 1902 have distinct predicates; identify the applicable obligation/tort basis.
- Civil set-off is conditional and TRLC 153 imposes insolvency-specific restrictions; damages are not an automatic deduction from a secured claim.
- CP 263 is a criminal gate, not proof of damage, authorship, intent or attribution.

## Causal proof chain

formal right → specific act → legal attribution → specific impairment → financing/asset consequence → causal bridge → quantum → legal remedy/effect.

Every arrow requires a source bridge. Repetition ≠ proof; chronology ≠ causation; relationship ≠ attribution; benefit ≠ intent; damage ≠ quantum; criminal allegation ≠ criminal finding.

## Site architecture

Canonical data: `assets/data/security-impairment-track-v1.json`  
Renderer: `assets/security-impairment-track-20260924.js`  
ES hub: `es/garantia-deterioro-causacion-acreedor/`  
EN hub: `en/security-impairment-creditor-causation/`

The route-specific module highlights one part of the same five-stage track rather than duplicating legal prose across pages.


## Implementation architecture

- GitHub public loader: `assets/site.js`, advanced from GitHub's own `main` predecessor through the exact append-only successor pinned in `ops/recovery-cross-thread/SECURITY_IMPAIRMENT_SITE_LOADER_GITHUB_REVIEWED_SUCCESSOR_20260924.json`.
- GitHub predecessor: 8,185 characters, Git blob `7d48f2f4e860b24c05a9f33647fb94643d7ec380`.
- GitHub successor: 9,247 characters, Git blob `692ba6638ed7b75b7901857145afa561ce9593d0`.
- The GitHub loader lineage is intentionally distinct from private GitLab's loader lineage. No GitLab loader body is imported into the public repository.
- Renderer: `assets/security-impairment-track-20260924.js`.
- Data: `assets/data/security-impairment-track-v1.json`, currently 26 route applications.
- Deep-dive routes: `/es/garantia-deterioro-causacion-acreedor/` and `/en/security-impairment-creditor-causation/`.
- Existing protected case-page bodies are not rewritten to carry this track. The reviewed loader invokes the component only for relevant route families, while the data file decides whether a component is actually rendered.
- Private GitLab contains narrower CEXP / CAM-offer routes; public GitHub maps the same issue to real public Community / active-estate equivalents rather than inventing nonexistent mirror paths.

## Release boundary

The implementation is a reviewed candidate until the applicable merge/release gates complete. Creation of a branch, MR/PR, or successful component-level test does not by itself mean the public site is live.
