# GitHub CAEPR release thread — continuity and preservation audit — 19 September 2026

Status: **DELETION-SAFE AFTER THIS RECEIPT IS MERGED AND ISSUE #1606 IS CLOSED.**

## Scope

This receipt preserves the technical work performed in the ChatGPT thread that began with analysis of the GitHub repository and then executed the merge/publish closeout for the CAEPR Meeting Point 357/2024 public-surface defect.

It records repository state, merge provenance, deployment/readback evidence, controller recovery, residual governance gaps and the thread-retirement verdict. It introduces no new evidential allegation, legal finding, identity promotion, filing, email, external contact or GitLab reconstruction.

## Baseline and current continuity

- Thread release final main: `e9bb7104b70dd10ebd2506a8d6cecd208188cda0`.
- Current main observed for this audit before this receipt: `593acd70d39ba7f0253e7f86177a104b17bc2e90`.
- Compare result: current main is **102 commits ahead / 0 behind** the thread release; merge base is exactly `e9bb7104b70dd10ebd2506a8d6cecd208188cda0`.
- Therefore the full thread release remains ancestral to current main; no divergent history was found.

## Thread merge chain

### PR #1609 — publication-controller recovery deadlock
- Title: **Publication: release superseded RECOVERY_REQUIRED fence safely**.
- Head: `db66a9f8b90aafce46579710f24ecc5df81c5e4d`.
- Merge: `b470fd7927edc91de3346694ef76e2c8ed9225c6`.
- Purpose: repair a deterministic controller deadlock left by merged/deployed PR #1512.
- New truthful terminal state: `SUPERSEDED_WITH_OPEN_READBACK`.
- Critical invariant: a superseded historic release with unresolved byte readback is **not** relabelled `VERIFIED_FOR_SCOPE`; the open readback gap remains explicit.
- Exact merged-SHA checks included:
  - Outage backend parity: run `35418849811` — PASS.
  - Publication integrity: run `35418849899` — PASS.
  - Release acceptance: run `35418849869` — PASS.
  - CI control plane: run `35418849858` — PASS.
  - Pages: run `35418848960` — PASS.
- PR #1512 was then recovered to `SUPERSEDED_WITH_OPEN_READBACK`, preserving `readback_verified: false` and the prior successful deployment evidence.

### PR #1608 — CAEPR N07 public-surface repair
- Title: **CAEPR: restore controlled N07 public-surface propagation**.
- Final head after current-main reconciliation: `2d4e756b4020266263fe1bd0b18bbcd393b5fe80`.
- Merge: `502f818495cf46836286bc4eed6cd9d2b1b8abc4`.
- Restored the four source-bounded `CARET_CONFIRMED` declarations on:
  - `es/cuaderno-juridico/meeting-point-357-2024-trazabilidad-judicial/index.html`
  - `en/legal-notebook/meeting-point-357-2024-judicial-traceability/index.html`
- Identities:
  - `PD-SP-O-0070` — AUREN REESTRUCTURACIONES SLP.
  - `PD-SP-P-0087` — Guillermo Fernández García.
- Historical first-hop provenance remained frozen; only the separately controlled N07 successor routes were permitted current inline caret markup.
- Exact merge checks:
  - CAEPR public-surface propagation: run `35419030653` — PASS.
  - Publication integrity: run `35419030547` — PASS.
  - Release acceptance: run `35419030611` — PASS.
  - CI control plane: run `35419030636` — PASS.
  - Pages: run `35419029936` — PASS.
- Publication controller reached `VERIFIED_FOR_SCOPE` with exact byte matches for both N07 pages and EN/ES entrypoints; pending set was empty.

### PR #1610 — rendered-browser monitor contract correction
- Title: **Monitor: align Meeting Point N07 live markers with current source**.
- Head: `8210c6e25a85b737a7e8350fdc78aff3c6113927`.
- Merge / thread-release final main: `e9bb7104b70dd10ebd2506a8d6cecd208188cda0`.
- Purpose: correct the legacy rendered-browser monitor, not the public pages.
- The stale literals `tres deudores` / `three debtors` were replaced with exact current authoritative N07 wording:
  - ES: `La entidad contractual Meeting Point exacta todavía no se ha identificado.`
  - EN: `The exact Meeting Point contracting entity remains unidentified.`
- No public proposition, evidence, route, identity or page content was changed.
- Exact final-main checks:
  - Rendered Meeting Point propagation: run `35419422386` — PASS.
  - Publication integrity: run `35419422513` — PASS.
  - Release acceptance: run `35419422337` — PASS.
  - CI control plane: run `35419422446` — PASS.
  - Pages: run `35419421674` — PASS.
  - Publication controller: run `35419426567` — PASS and `VERIFIED_FOR_SCOPE`.

## Preservation recheck on current main

At audit baseline current main `593acd70d39ba7f0253e7f86177a104b17bc2e90`:

- ES N07 blob remains `7cd3846c35994e6c8b7bdc6bcec8b8bdad33ec1c`.
- EN N07 blob remains `2446a79ae0ab2ced466fb7645ca0edc63c44e06a`.
- Both still contain `PD-SP-O-0070`, `PD-SP-P-0087` and `data-caret-state="CARET_CONFIRMED"`.
- The Meeting Point live workflow blob remains `ec4d87c76c3a5304b3f92808e6990ac2c46fb676`.
- The corrected current-source monitor literals remain present; the stale `tres deudores` / `three debtors` monitor pair is absent.
- `scripts/pd_release_contract.py` blob remains `8ddf9c478e3b6543815d537cf50474980b6bc7ec`.
- `scripts/pd_release_controller.py` blob remains `e11e360034dbef130ed424773527b6a6f48c2347`.
- `ops/PUBLICATION_CONTROLLER.md` blob remains `cf3507b9ed3ee9a906a4b630dae0265d49ee431b`.
- All three retain the `SUPERSEDED_WITH_OPEN_READBACK` control.
- Current-main exact runs at the audit baseline also show Publication integrity, Release acceptance and Pages as PASS, including runs `35436117091`, `35436117054` and `35436116574`.

## Thread-only information audit

No material technical outcome from this thread remains only in chat after this receipt:

- repository analysis findings that led to action are reflected in the merged control-plane and CAEPR repairs;
- the controller deadlock and its safe terminal-state treatment are persisted in source, tests, documentation and runtime state;
- the CAEPR declarations are persisted on current main;
- the monitor-drift diagnosis and correction are persisted in the workflow;
- merge/deploy/readback provenance is available through PRs, Actions and publication-controller receipts.

This thread introduced no Gmail evidence, Drive source document or private attachment requiring separate ingestion. No Gmail or Google Drive mutation is required to preserve this thread's technical work.

## Open items inherited from the wider repository

These are real but are **not unique blockers to retiring this thread**:

1. Issue #1525 — server-enforced required GitHub backend status checks on `main` remains open.
2. Issue #1572 — independent off-GitHub preservation copy remains open.
3. GitLab exact/native recovery remains governed separately; nothing in this thread inferred missing GitLab-native bytes or state.

## Stale issue closure

Issue #1606 — **Continuity: repair CAEPR declarations on bilingual Meeting Point 357 successors** — was still open at audit time even though its acceptance conditions have been met by PR #1608 and the later #1610 live-monitor closeout. It should be closed as completed with links to the merge and live verification chain.

## Retirement verdict

**DELETE/RETIRE SAFE for this ChatGPT thread once this receipt is merged and #1606 is closed.**

Rationale:
- all thread-specific code and publication changes are merged;
- the release is ancestral to current main;
- the changed blobs remain present and unchanged;
- deployment and live/readback evidence exists;
- no thread-specific private source remains only in chat;
- remaining open governance items are independently tracked elsewhere.

Do not use retirement of this chat as authority to delete repository history, PRs, Actions artifacts, publication-controller state, GitHub issues, GitLab recovery material, Gmail, Drive or other source custody.

## Integration-time current-main reconciliation

While PR #1627 checks were running, `main` advanced from the audit baseline `593acd70d39ba7f0253e7f86177a104b17bc2e90` to `4cec76c73331ff3986017f8ac2a13e02d867a2c0`. The audit branch was reconciled by a normal merge of that newer `main` before publication claim; no force update or rollback was used. The earlier baseline remains preserved above as the state first observed when the audit began.
