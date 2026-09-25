# Thread deletion audit — DIP 80 / publication truth / GitHub hardening / Codex

**Date:** 18 August 2026  
**Repository:** `sbu001monterecco/por-derecho`  
**Audit base:** `main` at `e5def049bb980b013c1c619d1919ab2941b29fb5`  
**Status at creation:** `REMOTE_SOURCE / CONTINUITY RECORD PENDING MERGE`

## Purpose

Preserve the material state, decisions, unresolved controls and next actions from the ChatGPT thread that:

- audited whether the dedicated DIP 80/2026 living casebook was actually live;
- identified the failure mode in which a thread could overstate implementation/publication state;
- established the universal publication-truth / thread-deletion safety architecture;
- audited GitHub hardening and disaster recovery;
- investigated Codex Security installation and the `Codex Security Access` connector failure;
- scheduled a follow-up for 19 August 2026;
- requested a fresh deletion audit and repository preservation.

This record is operational/governance material. It does **not** change public evidential propositions about any person, authority or proceeding.

## 1. Controlling publication-truth rule

The repository already contains the controlling protocol at:

`archive/UNIVERSAL_PUBLICATION_AND_THREAD_DELETION_SAFETY_PROTOCOL_18AUG2026.md`

Its canonical state machine remains:

`DRAFT → REMOTE_SOURCE → PR_OPEN → CI_GREEN → MERGED → DEPLOYED → LIVE_VERIFIED → DELETION_SAFE`

with `BLOCKED_RECOVERY` as an exceptional state.

No execution thread is authoritative about its own completion. Git tree, CI, `main`, the public host and a final continuity record are separate evidential gates. Never infer a later state from an earlier one.

### Compact Project-level instruction to retain

Use the following as the Por Derecho / Project Sun Rock foundation instruction where project-level configuration permits:

> **PUBLICATION TRUTH PROTOCOL** — No chat, agent or implementation thread may call work complete, merged, deployed, live, verified or deletion-safe from its own narration, local state, branch existence, generated payload or prior conversation. Use only the canonical state machine `DRAFT → REMOTE_SOURCE → PR_OPEN → CI_GREEN → MERGED → DEPLOYED → LIVE_VERIFIED → DELETION_SAFE`, plus `BLOCKED_RECOVERY`. Perform a fresh GitHub/deployment read before answering status questions. Report the highest independently evidenced state only. Branch ≠ implementation; source ≠ PR; PR ≠ green CI; green CI ≠ merge; merge ≠ deployment; deployment ≠ live verification; live verification ≠ deletion safety. Completion claims require branch/head SHA, PR, CI, merge SHA, deployment evidence, live URL evidence and remaining gate. Builder self-certification has no evidential weight without independent corroboration.

**Configuration boundary:** this audit does not prove that the above instruction has been installed in ChatGPT Project settings. The repository copy preserves the substance even if project-level configuration remains pending.

## 2. DIP 80/2026 — current controlling implementation state

Current completion path at audit time:

- PR: `#366` — **Materialize DIP 80/2026 open-kimono living casebook**
- branch: `agent/dip80-living-casebook-final`
- head: `c66499fb4ebfe69a868e1df678f80b2b98670377`
- PR state: open, unmerged, mergeable
- remote PR currently contains 7 changed files / 235 additions, not the final ordinary 14-route source tree

The PR declares the intended case-specific architecture:

- 7 Spanish + 7 English routes;
- dominant AHORA / NOW junction;
- reverse chronology;
- evidence/provenance atlas;
- 24-node human-gated decision tree;
- urgent-protection analysis separated from culpability;
- 11 substantive modules;
- respondent/counter-evidence and “what would change my view?” controls;
- 16 model documents and 20 teaching chapters;
- structured `caseId: DIP-80-2026` data;
- DIP 79 / DIP 80 allocation lock;
- `noindex,follow,noarchive` and no homepage/main-nav/RSS/sitemap promotion.

Fresh workflow state for head `c66499f…`:

- `Diagnose DIP 80 payload inventory`: **success**;
- `Materialise DIP 80 living casebook`: **failure**;
- `Publication integrity gate`: **failure**.

Therefore the dedicated DIP 80 living casebook is **not merged, not deployed and not live-verified**. Do not circulate the planned dedicated route as a proven live publication until the ordinary source tree materialises, CI passes, the PR merges, Pages deploys and the public routes are directly verified.

For continuity, treat DIP 80 as `BLOCKED_RECOVERY` / incomplete publication until those gates close, regardless of any earlier conversational wording that suggested it was already live or substantially complete.

## 3. GitHub production-governance state

Fresh `main` branch read at this audit:

- `main` SHA: `e5def049bb980b013c1c619d1919ab2941b29fb5`;
- branch reports `protected: true`;
- legacy protection/status-check response reports enforcement `off`;
- required status-check contexts/checks are empty.

Issue `#355` remains open: **P0: Enforce main branch ruleset and required production checks**.

The repository's prior empirical governance record establishes that direct writes to `main` were blocked on the tested path, but that a PR could merge before the publication-integrity check completed. Accordingly:

- PR-only protection: evidenced on the tested path;
- required-CI-before-merge: **not yet enforced/proven**;
- force-push/deletion/conversation-resolution/CODEOWNERS/admin-bypass rules should only be claimed when directly verified from GitHub settings/ruleset evidence.

Do not close `#355` based on intention or source-level controls alone.

## 4. Disaster recovery / independent copy

Issue `#356` — **Configure independent repository mirror and test clean restore** — is closed.

The controlling governance record states that the hardening work progressed to a restore-tested full Git bundle plus an off-GitHub Google Drive copy/readback and recurring refresh. This closes the earlier same-platform-only backup gap, subject to ordinary periodic health checks.

Do not expose backup credentials, mirror URLs, secrets or detailed recovery internals on the public website.

## 5. Codex Security state

Fresh plugin-dependency inspection at this audit:

- `codex-security` is listed as enabled/available in the OpenAI-curated catalog;
- it is **not installed** for the current user;
- GitHub is installed/enabled and resolves as an optional dependency;
- the mandatory manifest dependency `codex-security-access` (`connector_openai_codex_security_access`) remains unresolved;
- resolver reason: `no_unique_canonical_plugin`.

This is consistent with the UI error **“connector not found.”**

Operational rule: do not represent Codex Security as connected or scanning Por Derecho until the mandatory access connector resolves and an actual scan can be run. Codex Security is an additional adversarial/security layer, not a substitute for branch/ruleset enforcement, CI, backup/restore, live verification or evidence-governance controls.

## 6. 19 August follow-up checklist

A ChatGPT reminder was scheduled for the morning of **19 August 2026** (Atlantic/Canary) to revisit the following finite actions:

1. retry/fix Codex Security Access and then install/re-test Codex Security if available;
2. review other useful security/monitoring integrations without weakening least-privilege controls;
3. verify whether the compact Project-level publication/deletion-safety instruction has actually been installed;
4. finish/execute the hardened whole-site protection-and-strengthening prompt;
5. close or advance GitHub issue `#355` with empirical required-CI/ruleset evidence;
6. re-check PR `#366`, its materialisation workflow, ordinary 14-route source, merge and live Pages state;
7. confirm off-GitHub backup/restore continuity remains healthy;
8. run a fresh deletion audit after those changes.

## 7. Hardened website/repository execution prompt — recoverable form

Use this as the controlling next-pass prompt if the original chat is unavailable:

> **POR DERECHO FOUNDATION HARDENING PASS** — Audit the complete GitHub account/repository and deployed Por Derecho site from a defensive and publication-capability perspective. Start from fresh external evidence, never chat assertions. Verify repository/account security, `main` ruleset enforcement, required CI before merge, force-push/deletion protection, CODEOWNERS/review gates, least-privilege Actions permissions, immutable action pins, Dependabot/dependency controls, secret exposure risk, Pages deployment integrity, production smoke tests, live-route verification, DNS/custom-domain posture if applicable, content-security constraints available to the hosting architecture, off-GitHub backup/restore health, incident/recovery runbooks, machine-readable publication manifests, evidential provenance, bilingual route parity and deletion continuity. Assess optional integrations such as Codex Security only after their connector/access dependencies are actually available. Strengthen both **defensively** (prevent corruption, compromise, accidental publication, evidential drift and unrecoverable loss) and **offensively in the legitimate publishing sense** (faster reliable publication, stronger discoverability where intended, institutional reader journeys, resilient live verification and rapid correction/rollback). Never weaken evidential/legal boundaries or publish private security configuration. Implement repository changes through a reviewable branch/PR, run the universal publication-integrity gate, do not merge around failing checks, and verify the public host after deployment. Report state using the canonical publication state machine and preserve a final continuity record.

## 8. Public website decision

**No public website change is required from this deletion-audit thread.**

Reason:

- the new information is repository security/governance, connector state and implementation status;
- the universal protocol belongs in repository governance, not public-facing case narrative;
- publishing branch-protection weaknesses, backup internals or connector configuration would disclose unnecessary operational detail;
- the dedicated DIP 80 casebook is not yet live, and no new public route should be added merely to describe that implementation failure;
- existing public ICALPA material should remain evidence-controlled and should not be modified simply to mirror internal build state.

If a public page later asserts that the dedicated DIP 80 living casebook is live before live verification exists, correct that specific claim. Otherwise preserve the security boundary and keep this record repository-internal in purpose (not linked from site navigation).

## 9. Deletion-safety conclusion at record creation

Material thread substance is now recoverable from remote Git once this record is merged, including the previously chat-only Codex dependency diagnosis, compact Project instruction, follow-up checklist, hardened execution prompt and website non-publication decision.

At the instant this file is first committed on its audit branch, the correct classification is:

**`REMOTE_SOURCE / CONTINUITY RECORD PENDING MERGE`**

Do not call the originating thread `DELETION_SAFE` until:

1. this continuity record passes applicable repository checks;
2. it is merged to `main`;
3. it is read back from `main`;
4. no unique substantive instruction remains only in the chat.

Open operational work such as DIP 80 PR `#366`, GitHub issue `#355`, Codex Security Access and tomorrow's follow-up does **not** by itself prevent deletion of the chat once the instructions/status are durably preserved; deletion safety means continuity is preserved, not that every project task is finished.
