# GitHub ruleset enforcement receipt — 19 September 2026

## Scope

Ruleset: `Protect main` (#20860148)

Required exact status contexts:

- `PD release acceptance`
- `publication-integrity`
- `Outage backend parity / validate`

Deletion, non-fast-forward and pull-request protections remain enabled.

## Negative enforcement proof

PR #1666, exact head `30ffe7d9e2b616e720f496e5496564dfa9291042`, deliberately made one continuity JSON control malformed on its isolated branch.

- An immediate merge attempt was rejected while all three required checks were pending.
- Outage backend parity run #35467521899 failed as designed.
- A second exact-head merge attempt was rejected because a required check was failing.
- PR #1666 was closed unmerged; its branch and history were preserved.

## Green enforcement proof

This receipt PR is the positive candidate. It is backend-only and changes no public route, evidence, allegation or validator. It may merge only after all three exact required contexts succeed on its frozen head and `main` is re-read immediately before the exact-head merge.

Server enforcement and the controller's one-head acceptance discipline are complementary controls.