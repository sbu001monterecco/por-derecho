# Priority-actions execution programme

**Programme version:** `por-derecho.priority-actions.v1`  
**Prepared:** 25 August 2026  
**Preparation baseline:** `7fedbbbeed6ee7f014ecbeda4565d880ecdbaf65`  
**Machine record:** `program-v1.json`

This directory turns the latest unitary repository/site redigest into work that can be resumed safely by another authorised thread. It is an execution control, not evidence of completion.

## 1. Refresh before work

At the beginning of every execution pass:

1. fetch current `main` and record its SHA;
2. compare it with `prepared_from_main` in `program-v1.json`;
3. inspect open PRs touching the intended paths;
4. read the source controls identified by the selected task;
5. create a new branch from current `main`;
6. keep unrelated work unchanged;
7. run the task-specific and repository-wide checks; and
8. record the exact output, merge SHA and remaining blockers.

Do not rewrite `LAST_KNOWN_GOOD.json` merely because `main` has advanced. A verified rollback release, current Git head and exact deployed release are different facts.

## 2. Safe parallelisation

The programme may be divided between threads only on non-overlapping paths and sources.

### Lane A — repository/public-state work

- `P0-OPS-01`
- `P0-PRIV-01` inventory stage only
- `P0-REC-01`
- `P1-ONA-01`
- `P1-PR-01`
- `P1-WEB-01`
- `P1-RUNTIME-01`

### Lane B — private read-only transaction work

- `P0-TX-01`
- `P0-FIN-01`
- `P2-TX-WS-01`

### Lane C — combined private/public-safe derivative

- public-safe updates from `P0-FIN-01` or `P0-TX-01` may occur only after the private source has been read and minimised under the transaction-development protocol.

Two threads must not edit the same file or branch. Every thread must refresh `main` before PR creation and again before merge.

## 3. Recommended order

1. **Operational truth** (`P0-OPS-01`) so later work records the correct Git/deployment state.
2. **Read-only private mailbox re-query** (`P0-TX-01`) and **financing playbook** (`P0-FIN-01`) in parallel with repository work.
3. **Public/private inventory** (`P0-PRIV-01`) before destructive remediation.
4. **Recovery denominator** (`P0-REC-01`) as the principal evidential/quantitative lane.
5. **ONA discovery** (`P1-ONA-01`) as a bounded public-site improvement.
6. **PR #1016 delta reconstruction** (`P1-PR-01`) after current identity/professional controls are locked.
7. **Reader journey** and **runtime consolidation** only after route inventory and sent-link preservation are current.
8. **Private transaction workspace** as the long-term home for named financing and co-investment work.

## 4. Task execution protocol

For a selected task:

1. Change its runtime state privately to `IN_PROGRESS`.
2. Follow only the `allowed_actions` in `program-v1.json`.
3. Treat `prohibited_actions` as hard stops.
4. Use the listed template rather than inventing a new structure.
5. Keep evidence locators in the authoritative source system; public Git receives only permitted derivatives.
6. Test every acceptance criterion.
7. Open a focused PR with a path list and evidence-boundary statement.
8. After merge, verify the exact merged tree and any affected live route.
9. Record remaining open evidence honestly.

## 5. Task summaries

### P0-OPS-01 — operational truth

Create a release-state register that records immutable observations rather than pretending a manually edited snapshot is always current. Separate:

- current Git head observed at execution;
- exact deployed SHA, or `UNKNOWN` with the reason;
- last complete whole-site verification;
- last-known-good rollback release;
- open PR/draft counts;
- outstanding deployment and remediation checks.

The old current-state files remain historical evidence until a reviewed migration is complete.

### P0-PRIV-01 — public/private remediation

Start with a non-destructive inventory. Flag provider message IDs, private locators, raw email headers/bodies, unsent correspondence, unnecessary personal data and transaction-development material in public Git. Classify each item as:

- intended public derivative;
- redact current tree;
- relocate to private custody and replace with public-safe summary;
- retain with reason;
- Git-history remediation requiring separate decision.

Never delete the only evidential copy.

### P0-TX-01 — private mailbox re-query

Read the connected corporate mailbox for the current reply state, conflicts/onboarding, NDA version, meeting status and requested next documents. This is read-only. A reply, acknowledgement or silence does not authorise a follow-up.

### P0-FIN-01 — financing playbook

Build the named, detailed financing playbook in a private workspace. Public Git may contain only opaque IDs, wave-level status and public-safe methodology. Every route must record the stage reached and why it paused, expired, was rejected or remains open. Historic terms are stale until revalidated.

### P0-REC-01 — recovery denominator

Build a reproducible ledger connecting assets, rights, liabilities, consideration, proceeds, fees, creditor payments, income/fruits, surplus, damages and remedies to the correct claimant/right-holder. Use overlap groups and explicit no-double-counting rules.

### P1-ONA-01 — ONA discovery

Register the paired funded-exit routes in the sitemap/discovery controls; preserve canonical/hreflang parity; add concise gateways from the relevant ONA, 7 June and financial-lives routes; verify direct HTTP and source/live parity. Do not add another large homepage module.

### P1-PR-01 — PR #1016 reconstruction

Do not merge the divergent branch wholesale. Inventory unique propositions and files, compare them against current canonical IDs and validators, then rebuild only validated deltas on current `main`.

### P1-WEB-01 — reader journey

Map the existing routes to six reader questions without removing evidence or protected first-read actor/institutional content. Prefer indexes and progressive disclosure.

### P1-RUNTIME-01 — runtime manifest

Create a declarative route/module manifest in shadow mode. Compare rendered output and route behaviour before replacing any layered loader. Preserve stable URLs and fragments already sent externally.

### P2-TX-WS-01 — private transaction workspace

Keep named institutions, contacts, NDAs, models, valuations, current opportunities and negotiation material outside public Git. Public Git may contain only an anonymised charter and continuity state.

## 6. Templates

- `templates/release-state-register.template.json`
- `templates/public-private-remediation-inventory.template.csv`
- `templates/private-mailbox-requery-checklist.md`
- `templates/financing-playbook-public-safe.template.csv`
- `templates/recovery-denominator.template.csv`
- `templates/pr-triage.template.csv`
- `templates/ona-discovery-work-order.md`
- `templates/reader-journey-route-map.template.csv`
- `templates/runtime-module-manifest.template.json`
- `templates/private-transaction-workspace-charter.md`

## 7. Completion evidence

A task is not complete merely because a draft or PR exists. Minimum completion evidence is:

- current-main baseline;
- branch and PR;
- exact changed paths;
- task-specific validator result;
- relevant repository-wide checks;
- merge SHA;
- live verification where public presentation changed;
- public/private boundary confirmation;
- explicit remaining blockers.

## 8. External-action boundary

Nothing in this programme authorises:

- sending, resending, correcting or following up an email;
- scheduling a meeting;
- contacting a bank, fund, law firm, journalist, authority or other third party;
- filing a legal document;
- accepting a mandate or financial term;
- publishing private transaction material.

Each such action requires its own current authority and exact package.
