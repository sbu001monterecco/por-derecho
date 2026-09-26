# ONA / Cuatrecasas republish gap register — 26 Sep 2026

**Control ID:** PD-ONA-CUA-REPUBLISH-GAPS-20260926-01  
**State:** ACTIVE — evidence delta prepared; publication merge blocked pending repository checks.  
**Scope:** source recovery, version control, public projection and cross-host parity for the ONA-led funded-exit / Cuatrecasas adviser-readiness track.

## A. Evidence gaps

1. **AC / convenio evaluation text** — existing controls refer to an actual Insolvency Administrator evaluation/report text; the native/complete text is not yet recovered.
2. **Daniel Irigoyen 12–13 Jun 2018 institutional chain** — recover the exact submission, annexes, docket/LexNET entry, certified court/AC record and any immediate response.
3. **Santander continuation** — recover risk/credit follow-up, committee material, later term sheet or documented closure/decline if it exists. Current evidence proves active review and parallel-refinancing intent, not commitment.
4. **Dentons lender-side review** — recover the proposal, engagement and completed review/output if any. Current evidence proves mobilisation/coordination and conditions for review, not completion.
5. **Expert-Witness final-version reconciliation** — reconcile valuation, debt-reasonableness, economic-note and CEXP-credit versions; identify final issued/signed copies.
6. **Lagune / Elaia chain** — preserve draft → Aweswell-signed preferential right → buyer LOI → lender-package use → expiry/termination/extension. Current signed right is time-limited and the LOI has its own conditions.
7. **ONA execution family** — reconcile signed 6-Jun lease/annex, works annexes, later addenda/novation and condition status.
8. **Mailbox exhaustion** — complete pagination and attachment reconciliation across all three connected Gmail accounts for variant names and route terms; maintain a negative-search ledger.
9. **PwC / KPMG 2018 closing role** — do not promote either into the April–June 2018 closing team unless a concrete mandate/deliverable/transaction communication is recovered.

## B. Cross-repository gaps closed in this delta

- restored GitLab live mirror path `research/pre-7-june-2018-funded-ona-exit-source-map.md`, which previously existed only as recovered historical material;
- added matching adviser-readiness matrix to GitHub and GitLab;
- added matching bilingual ONA redundancy-by-design public sections;
- added matching Cuatrecasas/ONA close-out control;
- co-located first-hop sources in the canonical Google Drive source package.

## C. Infrastructure / publication gap

### GitLab baseline
The latest visible `main` pipeline before this branch is pipeline **2883826278** at commit `5d90b0fd...` and is already recorded by GitLab as **failed**. Its API job listing currently returns no jobs, so that baseline state does not by itself identify the same root cause as the branch failure.

### Current MR !618
MR pipeline **2885114415** fails at required job **verify-tested-build-handoff** (job **16753103479**). The trace shows:
- release-bundle tests pass;
- tested-build CI composition tests fail because the committed CI configuration SHA-256 does not match the authenticated expected snapshot;
- the guard raises **“Unreviewed current implementation: tested-build CI configuration”**.

**Control rule:** do not weaken, bypass or rewrite historical CI-integrity controls merely to publish this evidence delta. Repair the tested-build configuration/snapshot through its own reviewed governance path, or establish a documented repository-approved successor. Until then, GitLab publication is **STAGED, NOT LIVE VERIFIED**.

## D. GitHub publication gate

PR **#1911** contains the evidence/public-page delta. Required GitHub workflows were still running at the last check. Do not merge until required checks pass on the exact current head.

## E. Completion rule

“Republished” means:
1. protected merge completed on the relevant host;
2. exact-head CI/release checks pass or a documented approved governance successor controls;
3. generated/public artifact contains the intended bilingual sections and source controls;
4. live readback confirms the markers;
5. Google Drive control manifest points to the final canonical source/version set.

Until those conditions are met, use **prepared/staged**, not **live/republished**.
