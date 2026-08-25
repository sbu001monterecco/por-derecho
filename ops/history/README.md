# Operational-state history

This directory preserves state files that were once used operationally but are no longer
authoritative as current repository or deployment truth.

- `CURRENT_STATE_2026-08-24_PR922.json` preserves the former mixed current/case snapshot.
- `PRODUCTION_STATUS_2026-08-24_PR922.json` preserves the exact PR #922 live-deployment record.

Historical verification remains evidence of what was positively verified at the time.
It does not mean that the historical SHA is the current `main` or current Pages deployment.
Do not delete these records when refreshing `ops/CURRENT_STATE.json` or
`ops/PRODUCTION_STATUS.json`.
