# Historical operational-state snapshots

This directory preserves operational state files that were once used as current routing records but are no longer authoritative as current repository or deployment truth.

- `CURRENT_STATE_20260824.json` preserves the mixed PR #922 current/case snapshot.
- `PRODUCTION_STATUS_20260824.json` preserves the exact PR #922 production and verification snapshot.

Historical verification remains evidence of what was positively verified at that time. It does not mean the historical SHA remains the current `main` or current Pages deployment.

Current operational routing is controlled by:

- `ops/CURRENT_STATE.json` — dynamic repository-state contract plus last observation;
- `ops/PRODUCTION_STATUS.json` — bounded deployment observation;
- `ops/LAST_KNOWN_GOOD.json` — historical rollback anchor; and
- `ops/RELEASE_LEDGER.json` — append-only release history.

Specialist case/evidence state remains separately controlled by `ops/CURRENT_UNITARY_STATE.json`.
