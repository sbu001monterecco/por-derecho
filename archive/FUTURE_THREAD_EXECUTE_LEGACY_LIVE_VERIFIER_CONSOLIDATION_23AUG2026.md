# FUTURE THREAD EXECUTION — legacy live-verifier consolidation — 23 August 2026

**Status:** ACTIVE MAINTENANCE / DO NOT WEAKEN CONTROLS

## Objective

Reduce duplicate/stale GitHub Actions failure noise while preserving one clear, observable and sufficiently strict verifier for each publication family. This is operational maintenance, not a reason to remove evidential or publication safeguards.

## Core principle

A workflow notification is not itself proof that the public website regressed. Inspect the failing job, expected marker, source commit and live route. Conversely, repeated false/stale failures must not be ignored indefinitely; they should be repaired or retired audibly.

## Execution sequence

### 1. Inventory live-verification workflows

Enumerate every workflow whose purpose includes:

- GitHub Pages/public-edge verification;
- production smoke testing;
- route/marker verification;
- publication-specific live checks;
- post-deployment proof.

For each record:

- workflow filename/name;
- publication family;
- triggers/path filters;
- expected markers/routes;
- retry/propagation behavior;
- permissions;
- latest meaningful pass/fail;
- whether another workflow covers the same invariant;
- whether it remains referenced by a publication manifest/deletion audit.

### 2. Group by publication family

Create families such as CAM attribution, ACTA, AC/administrator, adjudicación, RICPE/San Telmo, Fiscalía/CGPJ, books/media, etc. Do not merge unrelated semantic safeguards merely to reduce workflow count.

### 3. Identify duplicate and stale checks

A workflow is a retirement candidate only where the repository can prove that:

- its invariants are fully covered by a current canonical check; or
- its route/feature was intentionally retired and the historical evidence remains preserved.

Do not retire a check simply because it frequently fails.

### 4. Narrow triggers

Prefer path filters tied to the controlled source files, scripts, routes, datasets and assets. Avoid running a specialist live verifier on unrelated `main` changes where possible.

Where shared loaders can affect many pages, include the loader path explicitly rather than pretending the specialist page is isolated.

### 5. Version markers and source lineage

For each canonical verifier, record:

- marker version/date;
- source commit/PR that introduced the marker;
- relevant publication manifest;
- exact public routes;
- expected source/public relationship.

A future marker change must update both the source validator and public-edge verifier in the same controlled change.

### 6. Pages propagation handling

Use bounded retries with cache-busting for public-edge checks. A push should not fail immediately merely because GitHub Pages has not propagated, but retries must remain finite and failures observable.

Separate conclusions:

1. source validation passed;
2. repository/PR integrity passed;
3. deployment workflow succeeded;
4. public edge shows the expected version.

Do not call source CI success “live verified”.

### 7. Permissions and side effects

Canonical verifiers should be read-only unless a separate auditable need requires a write. They must not send email, post external messages or mutate public evidence merely to verify it.

### 8. Retirement process

Retire superseded workflows only through a PR that records:

- old workflow;
- replacement workflow;
- invariant-by-invariant coverage map;
- latest historical run evidence;
- manifests/audits updated;
- proof that notification/required-check behavior remains sufficient.

Preserve the old workflow history through Git/GitHub history; do not rewrite history.

### 9. Notification hygiene

After consolidation, configure notifications/required checks so that a meaningful failure remains visible. Do not suppress failures globally simply to reduce inbox volume.

## Special CAM rule

The current CAM publication family has a substantive validator plus observable public-edge closeout verification. Do not retire or weaken the final closeout verifier unless a replacement proves all of its current invariants: direct attribution, non-finding, identity/source-literal separation, corrected homepage chronology, closeout-record availability and no-send boundary.

## Prohibited actions

- Do not mass-delete workflow files without a coverage map.
- Do not change expected wording merely to make a failing workflow green without checking public/source correctness.
- Do not treat a stale cache as proof of permanent regression.
- Do not treat a local/source validator as equivalent to a public-edge check.
- Do not remove off-GitHub preservation or privacy/integrity gates as part of “cleanup”.

## Completion definition

This maintenance item is complete when the repository contains:

- a workflow inventory;
- a canonical-verifier map by publication family;
- a documented retirement/keep decision for each duplicate candidate;
- narrowed triggers and bounded propagation retries where appropriate;
- updated manifests/deletion audits;
- a final CI/public-edge proof; and
- its own deletion audit.