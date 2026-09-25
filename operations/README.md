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

An item being open does **not** fail CI. The operational-integrity validator hard-fails malformed, unowned, untracked, contradictory or falsely closed records, including missing dates, next actions, closure tests or evidence. An elapsed review date is reported prominently as an advisory warning in universal CI; it does not by itself fail an unrelated additive publication.

## Blocking dimensions

Each item declares whether it blocks:

- `publication`
- `repository_hardening`
- `security_assurance`
- `deletion_safety`

This prevents a generic phrase such as “open operational items” from being mistaken for “the website is unsafe to publish” or “the originating thread cannot be deleted.”

Blocking dimensions must be applied to the action or truth claim they protect. The registry does not currently encode path-level applicability, so a generic blocking flag must not be converted into a repository-wide publication freeze without a separately scoped decision and evidence.

## Source hierarchy

The registry is a control index, not self-proving evidence. For each item, verify the linked issue, PR, publication manifest, workflow result, platform setting or repository file before advancing state.

## Review discipline

Every non-closed item must carry `last_verified_at` and `review_by`. The item is current through `review_by`; beginning the following day it is review-due. Universal CI reports review-due items prominently but does not fail an unrelated additive merge. A stale item is a hard stop only for a separately scoped action or current-state claim that actually relies on that item. Refresh status and evidence after a real review; never extend dates as a substitute for verification.

After changing the validator or this policy, run `python3 .github/governance/test_validate_operational_items.py`. The deterministic cases cover the due-day boundary, advisory future-date behaviour and the structural conditions that must remain hard failures. CI wiring for this test remains a separate shadow-mode decision; the existing universal workflow continues to execute the production validator itself.

## Public website boundary

This directory is not a public website feature. Do not expose secrets, backup destinations, branch-protection weaknesses, connector internals or administrative security configuration through GitHub Pages. Public-site changes are appropriate only when an operational item has a genuine user-facing consequence that must be corrected or disclosed.
