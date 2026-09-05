# Publication controller — PD-MTCP-20260904-01 extension

The current-main repair resumes PR1468; it never replays a historical tree. Read
`ops/RELEASE_AUTOMATION_STATUS.json`, current main, the state-only branch
`pd-publication-state` and issue1428. Historical chat reports are not live state.

## Execution and authority

Owner commands on issue1428 use exact syntax:

```
/pd-release claim PR_NUMBER CANDIDATE_40_CHARACTER_SHA
/pd-release verify PR_NUMBER CANDIDATE_40_CHARACTER_SHA
/pd-release recover PR_NUMBER CANDIDATE_40_CHARACTER_SHA
/pd-release abort PR_NUMBER CANDIDATE_40_CHARACTER_SHA
```

Claim requires an open nondraft same-repository PR, incorporation of current main,
and exact-head successful `PD release acceptance` and `publication-integrity`
checks from GitHub Actions. The controller atomically records its permit using
Contents-API compare-and-swap on a state-only branch. It **does not merge**.
The authorized connected publisher refreshes the permit, base and head, performs
the normal exact-head protected merge, then requests verify. This keeps Pages
triggering through the existing authorized publisher, not an assumed recursive
GITHUB_TOKEN workflow. No new PAT, credential or deployment provider is needed.

There is no timeout-to-free rule. A stopped transaction retains ownership and
its fencing token; recovery must inspect the actual PR, merge and Pages state.
A successful exact live result releases only its stated scope. Failed or
missing deployment/readback retains recovery-required status. A replaced owner
cannot update state with an old blob SHA. A merged release cannot be aborted as
though it never happened. Never roll main back to satisfy a historical hash.

`queue: max` serializes participating workflow commands; compare-and-swap guards
state. It does **not** prevent independent API merges with another credential.
The controller uses contents write only to persist `pd-publication-state`.
GitHub job credentials are not branch-restricted; this is reviewed code-level
confinement, not a server-enforced security boundary. The exact workflow is the
only added exception to the production-writer guard; normal prepare jobs remain
prohibited. Its source is checked out from main, never untrusted PR code.

## Administrative enforcement — not yet activated

The installed connector lacks Administration(write). After the acceptance job
has run successfully, an authorized administrator must require the exact check
`PD release acceptance` plus `publication-integrity` from GitHub Actions, retain
force-push/deletion prevention and PR requirements, and restrict alternative
publication credentials/paths. Existing protection must be read, compared and
preserved, never overwritten by a guessed ruleset. Do not announce exclusive
server enforcement until the settings and a negative merge test prove it.
No external reviewer or unavailable service is added as a publication dependency.

## What checks mean

Required check results are unique, complete, explicit PASS/exit0. Missing,
skipped, timed-out, unknown and duplicate results block acceptance. A diagnostic
workflow completing is not a candidate passing. The inherited comparison reads
explicit defects, preserves multiplicity and numerical error facts, and separates
inventory/progress from new, unchanged, improved or resolved defects. Unknown
failure formats block comparison. Unchanged inherited findings are not erased or
certified repaired. Runtime output records source SHA, scope and remaining gaps.

The generic owned-block and original-record preservation primitives are tested,
but the existing CNMV generator and specialist page contracts are deliberately
unchanged by this automation-only release. Their inherited findings remain
visible and separately owned. Source-backed page and history repairs must not be
combined with controller installation simply to obtain a green preparation run.
Existing IDs cannot be silently assigned to another entity. Source-linked
correction history permits reviewed identity correction, not automatic proof.

For first installation or a completed release lacking runtime state, an explicit
owner `recover` command can record and verify the exact current merged PR after
checking its exact-head successful acceptance. This is recovery evidence, not a
claim that an exclusive lock existed before installation.

## Evidence, privacy and completion

Public-safe code/control changes never authorize sending mail, filing, contacting
an authority, or publishing private originals. The CaixaBank privacy/image worker
remains priority; source-copy permissions and actual redacted derivatives must be
verified independently. A removed page link is not revocation of a public share.
PR1467 is a reviewed successor, not permission to rewrite historical manifests.
Uría branches must not reuse RAUDA's committed PD-SP-O-0084.

Final reports must distinguish prepared, accepted, merged, deployed and verified
for scope. Record actual Pages run, exact merge SHA, readback, browser coverage and
remaining blockers. Unreadable new tooling does not erase earlier authenticated
results. Do not repeat old-thread discovery when a verified artifact is available.
