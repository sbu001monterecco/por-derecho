# Por Derecho operational control plane

This directory is the canonical repository layer for **open operational work** that is important enough to survive chat/thread deletion but is not itself a public evidential proposition.

## Why this exists

Publication state is already controlled through `publication-manifests/`. Operational debt previously remained distributed across GitHub issues, PRs and archive continuity prose. `open-operational-items.json` gives future threads and maintainers one machine-readable place to answer:

1. What remains open?
2. What does it block?
3. Who owns it?
4. What evidence supports the current status?
5. What is the next finite action?
6. What exact evidence permits closure?
7. When must it be reviewed again?

## Status model

- `OPEN` — actionable work exists now.
- `BLOCKED` — work cannot advance until a stated blocker is removed.
- `WAITING_EXTERNAL` — completion depends on an external platform/provider/control outside the repository.
- `MONITORING` — the initial setup/gap is closed but a recurring health check remains necessary.
- `CLOSED` — the closure test has been met and closure evidence is recorded.

An item being open does **not** fail CI. The operational-integrity validator fails when an item is malformed, unowned, untracked, stale, missing its next action/closure test, contradictory, or falsely marked closed.

## Blocking dimensions

Each item declares whether it blocks:

- `publication`
- `repository_hardening`
- `security_assurance`
- `deletion_safety`

This prevents a generic phrase such as “open operational items” from being mistaken for “the website is unsafe to publish” or “the originating thread cannot be deleted.”

## Source hierarchy

The registry is a control index, not self-proving evidence. For each item, verify the linked issue, PR, publication manifest, workflow result, platform setting or repository file before advancing state.

## Review discipline

Every non-closed item must carry `last_verified_at` and `review_by`. Once `review_by` passes, the repository gate requires the item to be refreshed before unrelated work can merge. This deliberately turns forgotten operational debt into visible repository friction rather than silent drift.

## Public website boundary

This directory is not a public website feature. Do not expose secrets, backup destinations, branch-protection weaknesses, connector internals or administrative security configuration through GitHub Pages. Public-site changes are appropriate only when an operational item has a genuine user-facing consequence that must be corrected or disclosed.
