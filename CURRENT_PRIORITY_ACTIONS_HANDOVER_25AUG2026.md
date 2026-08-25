# CURRENT PRIORITY ACTIONS HANDOVER — 25 AUGUST 2026

**Initial drafting baseline recorded by the programme:** `7fedbbbeed6ee7f014ecbeda4565d880ecdbaf65`  
**Current-main reconciliation baseline:** `4fac6bf1feeb4042fbc40ae22de7dec21c614250`  
**Programme merge:** `f9d0a22305431eeb6405b70f3bc30e5ff5bae514`  
**Purpose:** make the priority actions from the latest unitary repository/site redigest executable by this thread or a future authorised thread without reconstructing them from chat.  
**Controlling programme:** `ops/priority-actions/program-v1.json`  
**Human runbook:** `ops/priority-actions/README.md`  
**Future-thread prompt:** `ops/priority-actions/FUTURE_THREAD_EXECUTION_PROMPT.md`

The `prepared_from_main` value in `program-v1.json` preserves the initial drafting baseline. Before publication, the complete 17-file programme was rebuilt as one additive commit on the reconciliation baseline above, preserving concurrent repository work. Every execution pass must still fetch current `main`; none of these SHAs should be assumed current merely because they appear in this handover.

## Start here

1. Fetch current `origin/main`; never assume the preparation SHA remains current.
2. Read `AGENTS.md`, `CHATGPT_START_HERE.md` and `ops/REPOSITORY_PRESERVATION_CONTRACT.json`.
3. Read the latest unitary/deletion audits, including:
   - `docs/deletion-audits/2026-08-25-unitary-repository-website-valencia-thread-closeout.md`;
   - `docs/deletion-audits/2026-08-25-financing-counsel-email-and-unitary-redigest-closeout.md`.
4. Read `.github/governance/TRANSACTION_DEVELOPMENT_SEPARATION_AND_PUBLICATION_PROTOCOL.md` before any financing, investment, banking or adviser work.
5. Before any outbound email, read both:
   - `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`;
   - `EMAIL_SEND_EXACTLY_ONCE_EXECUTION_GUARD.md`.
6. Validate the programme with:

```bash
python3 scripts/validate_priority_actions_program.py
```

## Prepared priority lanes

### P0

- `P0-OPS-01` — rebuild operational truth through a release-state register that separates current Git head, exact live SHA, last whole-site verification and last-known-good rollback anchor.
- `P0-PRIV-01` — inventory and remediate current-tree public/private boundary defects without pretending Git history has been erased.
- `P0-TX-01` — read-only re-query of the private mailbox for adviser replies, conflicts/onboarding, current NDA and meeting status; no follow-up send is authorised.
- `P0-FIN-01` — complete the private 2016–2026 financing playbook and publish only a minimised public-safe derivative.
- `P0-REC-01` — materialise the quantitative recovery denominator with claimant/right-holder and no-double-counting controls.

### P1

- `P1-ONA-01` — add the dedicated pre-7 June 2018 funded-exit pair to discovery/sitemap controls and verify direct live parity.
- `P1-PR-01` — rebuild the unique validated delta from PR #1016 on current `main`; do not merge the divergent PR as-is.
- `P1-WEB-01` — create a six-question reader journey without adding another large homepage block or removing protected material.
- `P1-RUNTIME-01` — prepare a declarative route/module manifest and shadow-test it before any runtime-loader consolidation.

### P2

- `P2-TX-WS-01` — establish a private transaction-development workspace; public Git contains only its anonymised charter and continuity state.

## Non-negotiable boundaries

- Repository authority does not authorise email, filing, meeting invitations, financial commitments or third-party contact.
- No private transaction name, recipient, address, message ID, provider locator, unannounced asset, pricing or negotiation term belongs in public Git.
- A historic meeting, NDA, term sheet, onboarding step or proposal is not a current facility, mandate, approval or commitment.
- Do not merge a stale or divergent PR merely because GitHub reports it mergeable.
- Preserve stable routes, sent-link obligations, bilingual parity, actor separation, evidence classifications, corrections and contrary material.
- Any destructive remediation first requires preservation of the necessary private evidence and an explicit path-level review.

## Prepared execution assets

The programme includes templates for:

- release-state registration;
- public/private remediation inventory;
- private-mailbox re-query;
- public-safe financing status;
- recovery denominator;
- PR triage;
- ONA discovery acceptance;
- reader-journey route mapping;
- runtime module manifest; and
- private transaction-workspace governance.

## State rule

Each task moves only through:

`PLANNED → READY → IN_PROGRESS → REVIEW → COMPLETE`

or

`PLANNED/READY/IN_PROGRESS → BLOCKED`

A task may be marked `COMPLETE` only when every acceptance criterion in `program-v1.json` is satisfied and the evidence locator is recorded. A chat statement is not an implementation record.

## Expired chat-upload boundary

Some files previously uploaded in ChatGPT are no longer available as live chat attachments. This programme does not infer their contents or absence. Re-upload those files, or retrieve them from their authoritative connected source, before any byte-level comparison, hashing, extraction or document-specific conclusion.
