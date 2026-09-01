# Satire name/identity fail-closed implementation — 1 September 2026

**Control:** `PD-SAT-GOV-CLOSEOUT-20260901-01`

**Base inspected:** canonical `origin/main` at `a116f9823dab53c22139a66b43a9fbad60b305fe` after PR #1335 and the subsequent actors-register additions

**Scope:** repository-wide name display, dated affiliation, factual/satirical role separation and publication-risk controls for satire, caricature, spoof advertisements and equivalent public presentations.

**Authority:** Gil Marer's current instruction, after the gap audit, to use best judgement and take the actions required to hard-wire the controls. No email, filing, third-party contact, account/security change, history rewrite, public-route deletion or unpublishing is authorised.

## Gap closed

The prior state contained strong human and machine-readable guidance but no
specialist validator consumed the satire governance JSON or rejected an
unregistered surface, unresolved full name, undated current affiliation or
missing risk review. The main caret protocol correctly remained identity-only
and described its general enforcement as manual/advisory.

This package adds:

- an explicit full-name precedence: `CARET_CONFIRMED` → controlled strongly
  verified exception → source-short/neutral form → withhold;
- a non-transfer rule between portrait/file identity and CAEPR person identity;
- separate factual-role, affiliation-state and satirical-function fields;
- a seven-part opposing-counsel risk preflight;
- canonical register `data/satire-publication-compliance-v1.json`;
- fail-closed specialist validator
  `scripts/validate_satire_publication_governance.py`;
- six negative tests covering pending names, mismatched CAEPR IDs, current
  affiliations, strong exceptions and portrait-lock transfer; and
- a changed-path CI workflow that runs only for relevant public HTML/SVG,
  media-register, satire-governance, validator and test changes.

## Existing public-surface denominator

The shadow/advisory run first evaluated the complete current canonical
denominator and produced zero findings:

- four logical assets: `PD-DMA-0001`–`PD-DMA-0004`;
- four exact public SVG surfaces; and
- two bilingual landing pages.

No named individual appears in those six current public surfaces. Each surface
is now registered under `PD-SAT-AMHP-0001`, carries its exact visible
disclosure, retains factual/source boundaries and has an explicit risk review.

No satire landing-page body, SVG byte object, public URL, route, navigation or
asset hash was changed. The two existing bilingual operational identity-registry
pages are synchronised from 339/160 to **341 total / 162 people** so the new
canonical person records render and remain searchable without inventing a new
profile route.

## Three-person application boundary

The implementation does not manufacture a new identity result:

- **Francisco de Borja Rodríguez-Batllori Laffitte** is expressly promoted to
  `CARET_CONFIRMED`, `PD-SP-P-0010`; every role remains act/date/source-specific.
- **Eduardo Sánchez Iglesias** is admitted as `CARET_CONFIRMED`,
  `PD-SP-P-0161`, from the controlled 30-November-2021 source family and RSM
  first-party naming source. The portrait lock remains a separate file control.
- **Enrique Guerra Suárez** is admitted as `CARET_CONFIRMED`,
  `PD-SP-P-0162`, from the controlled RICPE certification, first-party
  professional material and 30-November-2021 source family.

The finite **three-person identity denominator is now 3/3 CARET_CONFIRMED**.
Exact San Telmo, RSM and Grant Thornton legal-person and date-specific current
affiliation questions remain open. No direct Borja–Enrique relationship is
established.

Any future graphic naming one of them must create a `named_people` compliance
entry and pass the new validator before publication.

## Staged enforcement evidence

1. Advisory/shadow run against the complete six-surface baseline: **PASS, zero
   findings**.
2. Six negative unit tests: **PASS**; every prohibited fixture was rejected.
3. Enforced validator against the same baseline: **PASS**.
4. JSON parse and Python bytecode checks: **PASS**.

The narrow repair path is additive correction or a normal corrective/revert PR.
The workflow does not require an unavailable reviewer or unrelated specialist
checks, and it does not block non-satire urgent repairs.

## Continuity result

The implementation decision, scope, identity boundaries, baseline denominator,
tests and repair path are recoverable from canonical repository files. This
thread is deletion-safe for the governance work once the branch/PR state is
recorded below and, if authorised publication completes, the merge and CI state
are appended without claiming a Pages deployment for governance-only files.

**Repository state:** prepared on isolated branch
`codex/hardwire-satire-identity-governance`; external publication state to be
recorded after the authority-compatible push/PR stage.
