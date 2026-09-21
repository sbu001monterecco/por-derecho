# Deletion audit — CAEPR naming, caret identity marker and `all is^` command

**Audit date:** 26 August 2026

**Repository:** `sbu001monterecco/por-derecho`

**Current-main baseline checked:** `679d4631a9c9ff2abe7ec3a73eccf5dc504d527f`

**Working branch:** `codex/canonical-actors-entities-proceedings-registry-20260826`

**Scope:** this ChatGPT thread's decision to name the federated identity system,
define `^`, include proceedings, define `confirm all is^`, strengthen its
protocol/governance and update the repository.

## Current verdict

**NOT DELETION-SAFE UNTIL THE CAEPR BRANCH IS PUBLISHED AND MERGED TO CURRENT
`main`.**

The material reasoning is now preserved in a clean local branch, but a local
worktree is not the repository's durable merge authority. Once the complete
branch is pushed, reviewed, merged to a fresh current `main` and read back, this
thread can be classified **DELETION-SAFE** for its CAEPR governance content.

This verdict does not depend on completing a repository-wide `all is^` audit.
No such universal audit was requested or performed. It depends on preserving the
rule, its limits, the action state and the recommended implementation sequence.

## Decisions preserved

1. The existing federated matter-identity system is named the **Canonical
   Actors, Entities and Proceedings Registry (`CAEPR`)**.
2. CAEPR is a federation of existing immutable-ID registers and controls; it is
   not a duplicate monolithic register.
3. `Name^` means only that the displayed person, entity, institution or
   proceeding is positively identified and reconciled to one immutable CAEPR
   record for the stated context.
4. `^` does not prove an allegation, role, relationship, participation,
   knowledge, intention, liability, current status, procedural outcome,
   finality or source authenticity.
5. Proceedings are included, but receipts, drafts, filenames, transmissions and
   unresolved candidate references cannot be upgraded into proceedings through
   punctuation.
6. The user command `confirm all is^` triggers an enumerated verification run,
   not an assumed complete conclusion.
7. A valid run requires scope, unique-reference denominator, `^` count, coverage
   percentage and an exception list with the next source needed.
8. The only complete result is `ALL IS^ — VERIFIED FOR THE STATED SCOPE` with
   zero exceptions. Otherwise the result is `PARTIAL — NOT ALL IS^`.
9. Carets are not inserted into quotations, source literals, filenames, URLs,
   search strings or formal citations. Reconciliation is displayed outside the
   source literal.
10. Identity correction has a lifecycle: `CARET_CONFIRMED`, `CARET_PENDING`,
    `CARET_SUSPENDED` and `CARET_NOT_APPLICABLE`.

## Governance added

The dedicated protocol is:

`.github/governance/CAEPR_CARET_IDENTITY_AND_ALL_IS_VERIFICATION_PROTOCOL_26AUG2026.md`

It adds:

- eligibility thresholds by object type;
- source-literal and accessibility rules;
- denominator and exception-report discipline;
- alias, former-name, homonym, legal-form and parent/child-proceeding controls;
- caret suspension and correction handling;
- non-inference protections; and
- a compatibility boundary keeping automation advisory until separately
  authorised and tested.

`AGENTS.md` section 9 and `CHATGPT_START_HERE.md` route future threads to the
protocol.

## Recommended next implementation actions

These are **PROPOSED**, not executed:

1. Add non-destructive caret-resolution fields to the existing CAEPR schemas
   after schema review.
2. Reconcile every verified Proceedings Master Register row to an immutable
   `PD-SP-R-####` ID while preserving unresolved rows.
3. Build a finite-scope advisory `all is^` report generator.
4. Run alias, `not_same_as`, former-name, quotation and parent/child-proceeding
   tests in shadow mode.
5. Under separate website authority, add an accessible bilingual `^` legend and
   machine-readable CAEPR references to selected canonical routes before any
   broad site propagation.
6. Record future caret suspensions, object splits and mistaken merges in the
   correction register.

No automated hard gate, mass historical rewrite or rendered website change is
authorised or implemented by this thread.

## Action-state ledger

| Object | Action | State | Verification | Open condition |
| --- | --- | --- | --- | --- |
| CAEPR name and basic caret rule | Added to `AGENTS.md` and bootstrap | `COMMITTED_ON_BRANCH` | first rebased commit `6320d14c` | include in final branch publication |
| Dedicated CAEPR governance protocol | Created and committed in current branch | `COMMITTED_ON_BRANCH` | commit `9c983b2f`; all seven listed local checks passed | push, PR and merge |
| Thread deletion audit | Created and committed in current branch | `COMMITTED_ON_BRANCH` | commit `9c983b2f`; this state-only closeout update follows | push, PR and merge |
| Public branch publication | Earlier push attempt did not occur | `BLOCKED` | execution environment required more explicit public-repository authority | Gil Marer's explicit push/PR/merge authorization |
| Pull request | Not opened | `NOT EXECUTED` | no PR URL exists | successful authorised branch push |
| Merge to `main` | Not performed | `NOT EXECUTED` | current `origin/main` lacks these files | PR and required checks |
| Website presentation | Not changed | `NO_ACTION_REQUIRED` for this repository-governance scope | no HTML/runtime/route diff | separate authority and implementation if later desired |
| Email, filing or calendar action | Not performed | `NO_ACTION_REQUIRED` | none requested | none |

`COMMITTED_ON_BRANCH` does not become `PR_OPEN` or `MERGED` by implication.

## Deletion-safety dimensions

| Dimension | Result |
| --- | --- |
| `THREAD_REASONING_CONTINUITY` | **Safe on the local branch; not yet durable on `main`** |
| `IMPLEMENTATION_STATE_CONTINUITY` | **Safe on the local branch** — completed, proposed, blocked and not-executed states are separate |
| `PRIMARY_EVIDENCE_COMPLETENESS` | **Not applicable to the semantic rule; open for any later object-specific identity audit** |
| `LIVE_PUBLICATION_VERIFICATION` | **Not applicable / not performed** — no rendered website change |
| `COMMUNICATION_VERIFICATION` | **Not applicable** — no communication action |
| `CUSTODY_RESILIENCE` | **Not assessed** — no native evidential object was created or moved |
| `DISASTER_RECOVERY_SAFETY` | **Not assessed and not implied** |

## Future-thread start order

1. Fetch current `origin/main`.
2. Read `AGENTS.md`, especially section 9.
3. Read `CHATGPT_START_HERE.md`.
4. Read the dedicated CAEPR caret protocol named above.
5. Load the existing matter-identity registry and operational control.
6. For entities, load `ops/CANONICAL_ENTITY_NAMES.json`.
7. For proceedings, load the Proceedings Master Register and its protocol.
8. Apply current corrections and the named-person/entity OSINT protocol.
9. Re-query current source systems before making a time-sensitive identity,
   capacity or proceeding-status claim.

## Final closeout

**What was done:** the CAEPR name, `^` semantics, proceedings inclusion,
`confirm all is^` verification command, eligibility lifecycle, governance
protocol, implementation recommendations and exact action state were preserved
on the working branch.

**What was not done:** the branch was not pushed; no PR was opened; nothing was
merged; no rendered site route was changed; no repository-wide identity audit,
email, filing or calendar action occurred.

**What proves the state:** current-main baseline `679d4631...`, rebased commit
`6320d14c`, protocol/audit commit `9c983b2f`, this state-only closeout update and
the validated branch diff.

**What remains open:** obtain explicit public-repository authority to push, open
and merge the PR. After merge, read back the exact files from current `main`
before changing the verdict to `DELETION-SAFE`.
