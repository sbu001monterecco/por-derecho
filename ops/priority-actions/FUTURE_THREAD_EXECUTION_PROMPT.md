# Future-thread execution prompt — priority actions programme

Use the following prompt in a new authorised thread when continuing one or more prepared priority actions.

---

Fetch the current remote `main` of `sbu001monterecco/por-derecho` and do not rely on the preparation SHA as current truth.

Read, in this order:

1. `AGENTS.md`;
2. `CHATGPT_START_HERE.md`;
3. `CURRENT_PRIORITY_ACTIONS_HANDOVER_25AUG2026.md`;
4. `ops/priority-actions/README.md`;
5. `ops/priority-actions/program-v1.json`;
6. `ops/REPOSITORY_PRESERVATION_CONTRACT.json`;
7. the source controls and template listed for the selected task ID;
8. the latest relevant deletion audit and correction/missing-evidence controls.

Selected task ID(s): `[INSERT TASK ID OR IDS]`.

Before changing anything:

- record current `main` SHA;
- compare it with `prepared_from_main`;
- inspect open PRs and branches touching the intended paths;
- state the exact task state, dependencies, privacy class, authority gate, allowed actions, prohibited actions, expected outputs and acceptance criteria;
- separate public Git work from private-source work;
- do not ask me to reconstruct information already available in the repository or connected sources.

Execution requirements:

- work from a new branch based on current `main`;
- make the smallest coherent diff;
- preserve all current routes, sent-link obligations, IDs, actor separation, legal-person distinctions, evidence classifications, corrections and contrary records;
- never publish native private communications, provider locators, live transaction terms, unannounced assets or named private pipeline information;
- for any private-source task, read the authoritative connected source before producing a summary;
- for transaction-development work, apply `.github/governance/TRANSACTION_DEVELOPMENT_SEPARATION_AND_PUBLICATION_PROTOCOL.md`;
- for any outbound email, stop and read both email controls; no send is authorised by this prompt;
- never merge a stale/divergent PR wholesale merely because it is technically mergeable;
- run `python3 scripts/validate_priority_actions_program.py` and all task-specific/current repository checks;
- before PR and again before merge, refresh current `main` and reconcile any overlap;
- after a public-site merge, verify the exact deployed SHA and affected live routes;
- update the task evidence/state record and preserve an explicit remaining-blockers list.

Report:

1. baseline and selected task;
2. sources read;
3. work performed;
4. files changed;
5. checks and results;
6. PR and merge state;
7. live verification where applicable;
8. private/public boundary confirmation;
9. remaining blockers and exact next action.

Do not claim `COMPLETE` unless every acceptance criterion in `program-v1.json` is evidenced.

---

## Suggested task prompts

### Operational truth

`Selected task ID: P0-OPS-01. Build the release-state register, preserving LAST_KNOWN_GOOD as a rollback anchor and marking exact live state UNKNOWN unless supported by deployment evidence.`

### Private mailbox status

`Selected task ID: P0-TX-01. Perform read-only mailbox retrieval for current adviser, conflict/onboarding, NDA and meeting status. Do not send or prepare an external follow-up unless separately requested.`

### Financing playbook

`Selected task ID: P0-FIN-01. Build the named detailed matrix privately and commit only a minimised opaque public-safe derivative.`

### Recovery denominator

`Selected task ID: P0-REC-01. Populate the denominator only from source-supported values, with legal-person and no-double-counting controls.`

### ONA discovery

`Selected task ID: P1-ONA-01. Add the paired routes to discovery controls, preserve proof boundaries and verify exact live parity after merge.`

### PR #1016 reconstruction

`Selected task ID: P1-PR-01. Inventory the divergent PR first; rebuild only unique validated deltas on current main.`

## Expired-upload instruction

Some earlier ChatGPT uploads have expired. Do not infer their contents. Ask for a fresh upload or retrieve the file from its authoritative connected source when the selected task requires byte-level access.
