# Por Derecho Foundation stage two — implementation record

**Control date:** 20 August 2026  
**Scope:** formation/governance, independent method review, San Bernardo preservation  
**Public status throughout:** initiative in formation

## Why this record exists

An earlier redesign description referred to public origin, governance, research and Palacete routes before those routes had actually been merged into `main`. This implementation corrects that gap and advances the substantive next stage in the same controlled package.

The repository, pull request, CI result and public-edge read-back—not a narrative description—control whether a route is prepared, merged or publicly live.

## Public routes added

Spanish:

- `/es/por-derecho/origen/`
- `/es/por-derecho/gobernanza-e-independencia/`
- `/es/por-derecho/investigacion-y-formacion/`
- `/es/por-derecho/palacete/`

English:

- `/en/por-derecho/origin/`
- `/en/por-derecho/governance-and-independence/`
- `/en/por-derecho/research-and-training/`
- `/en/por-derecho/palacete/`

The common runtime exposes the institutional programme on the existing Por Derecho home and inserts the corrected maturity ladder on both applications pages.

## Substantive instruments

1. `01_FORMATION_AND_GOVERNANCE_WORKING_DRAFT_20AUG2026.md`
   - public-benefit purpose;
   - legal-formation questions;
   - proposed Board, conflicts committee, scientific/method council, executive and external assurance;
   - founder-related quarantine and recusal;
   - funding, publication, data, property and first-year controls.

2. `02_INDEPENDENT_RED_TEAM_REVIEW_PROTOCOL_20AUG2026.md`
   - synthetic-first, pre-registered review;
   - reviewer independence;
   - false-positive and adversarial case battery;
   - provenance, timing, competence, perimeter, contradiction, privacy, bias, accessibility, human control and reversibility;
   - `CONTROL RECONCILED`, `REDESIGN AND RETEST` and `DO NOT DEPLOY` outcomes;
   - separate gate before any real or institutional use.

3. `03_SAN_BERNARDO_PRESERVATION_BRIEF_20AUG2026.md`
   - public biography and archive method;
   - preservation-first principles;
   - conceptual institutional room programme;
   - quiet and reversible technology;
   - professional gates from authority to operation;
   - strict separation from acquisition, finance, title, condition, planning, heritage and access diligence.

## Corrected maturity sequence

1. brief synthetic demonstrator;
2. expanded synthetic simulation — Case Prism under internal validation;
3. independent red-team review — protocol prepared, not performed;
4. controlled real-matter application — DIP 79/2026 and DIP 80/2026 are experimental founder-related research applications;
5. institutional pilot — none presently claimed;
6. adoption — only after express institutional confirmation; none presently claimed.

DIP 79/2026 and DIP 80/2026 are not independent validation, ICALPA endorsement, ICALPA adoption, an authorised institutional pilot or a disciplinary conclusion.

## Property separation

The direct family/adviser Palacete page remains transaction-sensitive and must continue to carry:

```text
noindex,nofollow,noarchive
```

It is excluded from the Foundation sitemap. The new public `/por-derecho/palacete/` routes contain preservation and institutional-use material only.

Controlling rule:

> The house is not the Foundation.

## Automated gates

`research/por-derecho/foundation-stage-2/validate.py` checks:

- route existence and bilingual reciprocity;
- public index/follow posture;
- exact initiative/draft/no-review/no-acquisition states;
- Case Prism and DIP 79/80 maturity language;
- public/private Palacete separation;
- source-instrument boundaries;
- runtime integration;
- sitemap and robots controls;
- absence of affirmative false status claims.

The pull-request workflow also compiles the validator and syntax-checks the shared JavaScript.

After merge, the public-edge workflow polls all eight public routes, the stylesheet, runtime, sitemap and robots file until the expected markers are visible or the verification fails.

## Publication truth rule

- **Prepared** means present on a feature branch.
- **Validated** means the branch checks passed.
- **Merged** means the pull request entered `main`.
- **Publicly live** means an independent HTTP read-back found the expected route-specific marker.

No earlier state may be described as a later one.
