# Operational truth protocol

**Control ID:** `PD-OPS-TRUTH-001`  
**Control date:** 26 August 2026  
**Repository:** `sbu001monterecco/por-derecho`

## Purpose

The repository previously allowed one historical release to appear to prove three different facts at once:

1. the current `main` SHA;
2. the currently deployed GitHub Pages SHA; and
3. the correct rollback anchor.

Those are different facts and must never be collapsed. Specialist case and evidence state is also separate from operational repository/deployment truth.

## Four controlled layers

### 1. Current repository truth — dynamic

Resolve `refs/heads/main` from GitHub or the checked-out repository at the time of use. `ops/CURRENT_STATE.json` is a contract plus a last observation; its checked-in SHA and PR count are not permanent current truth.

Generate a current report with:

```bash
python scripts/generate_operational_truth.py
python scripts/generate_operational_truth.py --live
```

### 2. Current deployment truth — observed

`ops/PRODUCTION_STATUS.json` records the latest Pages deployment observed when the file was updated. A successful Pages build proves deployment success for the stated SHA. It does not, without a separate content check, prove every route, marker or byte served.

A deployment can legitimately lag `main`; that difference must be reported rather than hidden.

### 3. Historical rollback truth — append-only

`ops/LAST_KNOWN_GOOD.json` is an explicitly historical, positively verified rollback anchor. It is not current merely because it was once live.

`ops/RELEASE_LEDGER.json` is append-only. Existing release entries may not be silently removed or rewritten. Corrections are appended and identify the affected `release_id`.

### 4. Specialist case and evidence truth

`ops/CURRENT_UNITARY_STATE.json` controls synchronized case, evidence, procedural and reader-routing state. `CURRENT_UNITARY_STATE.md` is its human-readable counterpart. These files do not replace repository, deployment or rollback truth, and the operational files do not replace specialist case records.

## Historical preservation

The former PR #922 v1 state files are preserved under `archive/ops-snapshots/`. Historical verification remains evidence of what was positively verified at the time. It does not mean that the historical SHA is the current repository or deployment.

Do not rewrite `main` history. Use ordinary PRs and normal reverts.

## Freshness policy

Refresh the last observation when any configured threshold is exceeded:

- `main` has advanced beyond the permitted commit distance;
- the observation is older than the permitted hours;
- the open-PR count has drifted beyond the permitted amount; or
- the deployment observation is inadequate for the operational decision being made.

The scheduled/manual workflow fails when drift exceeds policy. A normal push produces a live report but does not falsely rewrite repository state after the merge.

## Validation

```bash
python scripts/validate_operational_truth.py
```

The validator enforces:

- schema and layer separation;
- observed-main ancestry;
- identity and professional-register counts;
- consistency with the LIVE_VERIFIED unitary specialist state;
- successful observed Pages deployment without overclaiming route verification;
- rollback-anchor inclusion in the append-only ledger;
- chronological, unique release records;
- preservation of the former PR #922 snapshots; and
- append-only protection when a base ledger exists.

## Update procedure

1. Fetch current `main`.
2. Query open PR count and the latest successful Pages run for that exact SHA.
3. Run the live generator and inspect drift.
4. Update the last-observation fields and append a release record where appropriate.
5. Never delete or rewrite an existing release-ledger entry.
6. Run structural and specialist validators.
7. Open a narrow PR.
8. Recheck branch freshness immediately before merge.
9. After merge, query the new `main` and Pages run; record that later observation in a subsequent controlled update rather than claiming the pre-merge parent SHA remains current.

## Boundaries

Operational metadata does not establish any allegation, legal status, evidential proposition, professional responsibility, procedural result or private-source fact.
