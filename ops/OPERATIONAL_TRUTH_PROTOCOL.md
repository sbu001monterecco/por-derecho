# Operational truth protocol

**Control ID:** `PD-OPS-TRUTH-001`  
**Control date:** 26 August 2026  
**Repository:** `sbu001monterecco/por-derecho`

## Purpose

The repository previously used `ops/CURRENT_STATE.json`, `ops/PRODUCTION_STATUS.json` and
`ops/LAST_KNOWN_GOOD.json` as if one historical release could simultaneously prove:

1. the current `main` SHA;
2. the currently deployed GitHub Pages SHA; and
3. the correct rollback anchor.

Those are different facts and must never be collapsed.

## Three separate truth layers

### 1. Current repository truth — dynamic

Resolve `refs/heads/main` from GitHub or the checked-out Git repository at the time of use.
The checked-in `ops/CURRENT_STATE.json` is a contract plus a last observation. Its SHA and
open-PR count are not permanent current truth.

Generate the current report with:

```bash
python scripts/generate_operational_truth.py
python scripts/generate_operational_truth.py --live
```

The live command requires network access. In GitHub Actions it uses `GITHUB_TOKEN`.

### 2. Current deployment truth — observed

`ops/PRODUCTION_STATUS.json` records the latest Pages deployment observed and verified when
the file was updated. A successful Pages build proves deployment success for the stated SHA.
It does not, without a separate content check, prove every route, marker or byte served.

A deployment can legitimately lag `main`; this must be reported rather than silently hidden.

### 3. Historical rollback truth — append-only

`ops/LAST_KNOWN_GOOD.json` is an explicitly historical, positively verified rollback anchor.
It is not current merely because it was once live.

`ops/RELEASE_LEDGER.json` is append-only. Existing release entries may not be silently
removed or rewritten. A correction must be added to the `corrections` list and point to the
affected `release_id`.

## Snapshot and history rule

When a state file changes meaning or schema:

1. preserve the preceding file under `ops/history/`;
2. state why it is historical;
3. keep the original SHA, PR, deployment and verification evidence;
4. do not label the historical snapshot as current; and
5. retain ordinary Git history—never force-push or rewrite `main`.

## Freshness policy

The live generator compares the static observation to GitHub. Refresh the observation when
any configured threshold is exceeded:

- main has advanced by more than the permitted commit distance;
- the observation is older than the permitted hours;
- the open-PR count has drifted beyond the permitted amount; or
- the deployment observation is no longer adequate for the operational decision being made.

The latest successful Pages comparison is always reported. A scheduled/manual workflow may
fail when repository age, commit distance or PR-count drift exceeds policy. A main push
produces a live report but does not falsely rewrite repository state after the merge.

## Validation

```bash
python scripts/validate_operational_truth.py
```

The validator enforces:

- schema and role separation;
- observed-main ancestry;
- identity and professional-register counts;
- successful observed Pages deployment without overclaiming route verification;
- rollback-anchor inclusion in the append-only ledger;
- chronological, unique release records;
- preservation of the former PR #922 state and production snapshots; and
- append-only protection when a base revision is available.

## Update procedure

1. Fetch current `main`.
2. Query open PR count and the latest successful Pages run for that exact SHA.
3. Run the live generator and inspect drift.
4. Update the last-observation fields and append a release record where appropriate.
5. Never delete or rewrite a previous release ledger entry.
6. Run structural validation.
7. Open a narrow PR.
8. Recheck branch freshness immediately before merge.
9. After merge, query the new `main` and Pages run; append or refresh in the next controlled
   observation rather than claiming the pre-merge parent SHA is still current.

## Boundaries

Operational metadata does not establish any case allegation, legal status, evidential
proposition, professional responsibility, procedural result or private-source fact.
