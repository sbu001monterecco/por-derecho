# GitLab backend recovery readiness — 19 September 2026

**Status:** public-safe continuity control. Authenticated GitLab access remains blocked/unverified.  
**GitHub role:** active continuity backend during the outage.  
**GitLab project:** `86151898` — `por-derecho/por-derecho-setup-or-gitlab-setup`.  
**Last defensible pre-block GitLab main anchor:** `7d086d098676eecc2c1647ed09b348d8dc0bdc69`.

## What is now recoverable without guessing

The off-platform recovery record is strong enough to support a controlled backend reconstruction layer on GitHub:

- a hash-verified reconstructed Git bundle exists for the 6 September recovery seed;
- the bundle verifies as Git, with candidate commit `2e7c78b47c8064cd9b02f3abde5036679e691074` and tree `81541762b01df1eaf94e7bf1293c725bd849d43a`;
- a separate rehydrated source corpus verifies 3,851 delivered objects and all 2,540 recorded path/version rows across 1,857 candidate paths;
- 575 conflicting recovered paths remain deliberately unresolved rather than being collapsed by timestamp or last-write-wins;
- GitLab-generated notifications preserved off-platform establish a detailed merge-request, work-item and pipeline event graph through the account block;
- current GitHub already contains substantial functional parity for repository-hosted evidence intelligence, Second Pair of Eyes, Case Prism, publication controls, deterministic validators and outage governance.

The reconstructed 6 September bundle is a **historical recovery seed**, not the final GitLab tree. The rehydrated corpus is **private recovery material**, not a public deployment payload.

## Pre-block chronology anchors

The machine ledger records source-controlled chronology anchors that can be corroborated from GitLab-generated notifications. Important points include:

- 13 September: main `91e47998708638da60a9fd5e012ce965e38e5c36`, pipeline `2844357698`, PASS, 45 jobs / 3 stages;
- 16 September: main `5f5259425083a3b09aa535b1e1e279efd43500e4`, pipeline `2855032173`, PASS;
- 16 September: main `345ec1e0ab0059fc82cb8d700fd7b8ff6972fd18`, pipeline `2855885198`, PASS;
- 16 September: main `a901005930fb8f289a0621ed3f1c26184bc0304f`, pipeline `2856131784`, PASS, 57 jobs / 3 stages;
- 17 September: main `2befff8968286013a27dd579fdbdbca86164e7a6`, pipeline `2856391502`, FAIL at `verify-gitlab-public-frontend`;
- later on 17 September: protected main independently recorded as `7d086d098676eecc2c1647ed09b348d8dc0bdc69`.

The final anchor is the last defensible pre-block GitLab main established by the off-platform record. It is **not** a claim that a still-later commit was impossible before the account block.

## Notification-derived event graph

A bounded mailbox scan of Por Derecho GitLab project notifications for 13–17 September found:

- 981 project notifications;
- 93 distinct observed merge requests, within the observed number span !314–!529;
- 21 distinct observed work items (#40–#63, non-contiguous);
- hundreds of pipeline success/failure events with branches, commit SHAs, pipeline IDs and, where reported, failed job names;
- Duo Developer and Duo Code Review findings that preserve material residual/supersession decisions.

This is useful reconstruction evidence, but it is **not a substitute for GitLab's native database or an official export**.

## Recovery classification

### `EXACT_ALREADY_MIRRORED`

- `ops/duo/DUO_ORCHESTRATION_PROTOCOL_20260917.md` — pre-block parity salvage recorded exact blob identity before the GitHub merge.

This classification applies to that file only. It does not establish parity for Duo sessions, service-account state or GitLab-native configuration.

### `FUNCTIONAL_GITHUB_EQUIVALENT`

- MR/work-item/pipeline event reconstruction;
- GitHub Actions continuity backend;
- evidence-intelligence controls;
- Second Pair of Eyes;
- Case Prism;
- publication/release controls;
- deterministic outage validators.

Functional parity never means byte-for-byte GitLab platform parity.

### `PENDING_GITLAB_RESTORATION`

The following remain pending exact authenticated recovery or official export:

- `.gitlab/duo/agent-config.yml`;
- `.gitlab/duo/mr-review-instructions.yaml`;
- final `.gitlab-ci.yml` and GitLab-specific CI source not independently recovered byte-for-byte;
- complete MR discussions/review threads;
- approvals and approval rules;
- complete work-item notes and metadata;
- complete pipeline/job logs and retained artifacts;
- CI/CD variables and masking/protection state;
- runner registrations and state;
- environments/deployment records;
- project/group settings, integrations and webhooks;
- GitLab Duo sessions/service-account state;
- Orbit/index state;
- all secret values, tokens and credentials.

These must never be synthesized from notifications.

## Reconciliation rule when GitLab returns

1. Fetch exact authenticated GitLab source objects and platform metadata.
2. Record source object/path, SHA or native ID, retrieval date and byte/parity result.
3. Compare against **then-current** GitHub outage-period work.
4. Reconcile additively; preserve newer GitHub corrections and controls.
5. Never force-reset GitHub to an older restored GitLab snapshot.
6. Never select one of the 575 conflicting recovery paths merely because it has the newest timestamp.
7. Keep private evidence and recovery containers outside public Git.
8. Require **Outage backend parity**, **PD release acceptance**, and **Publication integrity** on the same exact candidate head before merge.

## Public-safety boundary

This control intentionally contains no mailbox message IDs, Support ticket numbers, private storage locators, encryption material, credentials, secret values or private evidence. The private bundles/corpora remain custody material outside public Git.

Machine-readable state: `ops/continuity/GITLAB_BACKEND_RECOVERY_LEDGER_20260919.json`.
