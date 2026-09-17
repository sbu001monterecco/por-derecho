# Por Derecho — GitLab Duo orchestration protocol

**Status:** repository operating protocol for AI-assisted decongestion and maintenance.  
**Canonical authority:** protected GitLab `main`.  
**Purpose:** increase parallel throughput without creating parallel release chains, losing provenance, weakening fail-closed controls, or assigning simultaneous write ownership to ChatGPT and GitLab Duo.

This protocol changes agent coordination only. It creates no authority to publish, file, email, contact third parties, weaken CI, expose private evidence, or convert allegations into findings.

## 1. Operating topology

Use GitLab as the orchestration and evidence layer. The preferred assembly line is:

1. **CLASSIFY — Duo read-only audit lane.** Compare one bounded MR/family against exact current `main`; identify unique material, successor overlap, private/public boundaries, and blockers.
2. **INTEGRATE — one exclusive writer.** ChatGPT or Duo Developer owns exactly one branch/MR and reconciles it onto current `main`.
3. **DIAGNOSE — CI / Fix Pipeline.** Ordinary technical failures are diagnosed from exact-head CI. Fail-closed admission controls are not mechanically repinned.
4. **REVIEW — Duo Code Review.** Once scope is frozen and the MR is Ready, use independent review with `.gitlab/duo/mr-review-instructions.yaml`.
5. **MERGE — integrator.** Re-read current `main`, exact source head, complete diff, discussions, approvals, and current-head CI immediately before merge.
6. **RELEASE — GitLab CI/CD.** Public changes follow the existing reviewed build → publication → exact live-readback chain. Source-only changes do not acquire a fictional deployment requirement merely to make the dashboard green.
7. **MIRROR — bounded GitHub parity lane.** Only public-safe, canonical GitLab material is eligible, and site-facing material waits for the applicable GitLab release/live verification.

## 2. Exclusive lane lease

Every active write lane has exactly one owner:

- `CHATGPT_WRITE`
- `DUO_WRITE`
- `HUMAN_WRITE`

Read-only auditors may inspect a write lane but must not commit, rebase, push, edit MR metadata, merge, or publish it. A second writer may take ownership only after the first lease is explicitly released or the lane is formally declared abandoned/stalled and re-read against current `main`.

Recommended control-tower receipt:

```text
LANE | MR/branch | owner | mode | base-main | head | public-impact | blocker | next-action
```

A Duo result is a proposal until admitted by the integrator. An unexpected Duo-created branch/MR does not enter `main` merely because it is useful or CI-green.

## 3. Standard Duo residual-audit output

Read-only Duo audits should end with a compact matrix rather than free-form narrative only:

```text
MR: !NNN
ASSIGNMENT_MAIN: <sha>
SOURCE_HEAD: <sha>
UNIQUE_PATHS: <count>
EXACTLY_IN_MAIN: <count>
SUCCESSOR_COVERED: <count>
PUBLIC_SAFE_RESIDUALS: <count>
PRIVATE_RESTRICTED_RESIDUALS: <count>
CI_STALENESS: CURRENT | STALE | NOT_RELEVANT
RECOMMENDATION: PRESERVE | REBASE_SAFE | NARROW_SUCCESSOR | SAFE_CLOSE
SAFE_CLOSE: YES | NO
HUMAN_JUDGMENT_REQUIRED: YES | NO
NEXT_SAFE_ACTION: <one bounded action>
```

If any unique residual, private-custody obligation, unresolved source identity, or substantive factual/legal decision remains, `SAFE_CLOSE` is `NO`.

## 4. Draft → Ready → review lifecycle

Use Draft status as an actual workflow boundary.

**Draft** means at least one of the following remains open: reconciliation, source/evidence review, public/private decision, exact inventory admission, current-main freshness, technical repair, or substantive approval.

An MR may become **Ready** only when:

- scope is frozen;
- base/current-main relationship has been re-read;
- complete diff is understood;
- exact-head required CI is green or the MR is explicitly non-CI/review-only;
- no unresolved substantive admission/publication decision is being hidden by green CI;
- no second writer owns the lane.

Ready status is the preferred trigger point for independent Duo Code Review. Review feedback is advisory; deterministic repository gates remain controlling.

## 5. Failure classification and the no-repin rule

Classify a red job before editing anything:

- `IMPLEMENTATION_DEFECT` — syntax, import, API, test, path, generated output, or other ordinary code defect. Appropriate for Duo Fix Pipeline / bounded repair.
- `STALE_BASE_OR_AUTH_CHAIN` — branch/current-main drift or predecessor adapter genuinely needs reconciliation. Repair only after authenticating the correct predecessor/successor relationship.
- `ADMISSION_GATE` — public inventory, reviewed bytes, predecessor digest, expected hash, source/provenance pin, or approval mismatch caused by a new candidate state. Requires integrator review; not an automatic defect.
- `MISSING_EVIDENCE_OR_HUMAN_JUDGMENT` — source, privacy, factual, legal, or publication decision cannot be supplied by CI. Record it and move to another safe lane.

**No-repin rule:** never resolve an `ADMISSION_GATE` merely by replacing the expected value with the observed value, weakening/removing the comparison, changing `allow_failure`, or broadening an exception. First establish an authenticated successor with an explicit bounded rationale and independent proof.

## 6. CI diagnostic tail contract

Long-running validators should preserve their detailed logs but also print a concise terminal summary so humans and automated CI diagnosis can classify the failure from the end of the trace:

```text
PD_FAILURE_SUMMARY
class=<IMPLEMENTATION_DEFECT|STALE_BASE_OR_AUTH_CHAIN|ADMISSION_GATE|MISSING_EVIDENCE_OR_HUMAN_JUDGMENT>
control=<stable control/job name>
observed=<value or NONE>
expected=<value or NONE>
paths=<bounded affected paths>
next_safe_action=<bounded diagnostic or review action>
END_PD_FAILURE_SUMMARY
```

Adding this summary must not alter pass/fail semantics.

## 7. Public-impact classification

A future public-impact classifier should begin in advisory/shadow mode. It may accelerate clearly source-only/governance-only MRs, but uncertainty must fall back to the full existing public build.

`PUBLIC_IMPACT=NO` may be asserted only where the diff cannot change generated/public bytes, release inventory, runtime loaders, public data, routes, styles/assets used by Pages, deployment configuration, or publication controls.

Any generator/loader/public-data/release-manifest ambiguity is `PUBLIC_IMPACT=YES_OR_UNKNOWN` and uses the full fail-closed release checks.

No classifier may make a public change bypass the reviewed-master and live-readback chain.

## 8. GitHub parity boundary

GitLab `main` remains sole authority. GitHub is a public secondary mirror. A parity lane must:

- compare exact canonical paths/blobs/hashes against current GitLab;
- copy only public-safe material;
- exclude private/restricted/native evidence not approved for public GitHub;
- preserve unique GitHub-only material before overwrite/deletion;
- avoid competing with a healthy existing parity writer;
- require appropriate GitLab release/live proof for site-facing bytes and green GitHub checks before merge.

## 9. Metrics

Track throughput by **dispositions**, not raw commits or branches:

- `MERGED_VERIFIED`
- `SAFE_CLOSED_WITH_PRESERVATION`
- `PRESERVE_ONLY_CLASSIFIED`
- `BLOCKED_EXPLICITLY`
- `PUBLIC_RELEASE_LIVE_VERIFIED`
- `PARITY_VERIFIED`

The objective is zero ambiguous/forgotten work, not zero historical branches or zero open evidence questions.
