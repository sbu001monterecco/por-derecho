# Agent publishing compatibility and non-interference profile

**Status:** repository operating policy

**Applies to:** ChatGPT/Codex and other repository-maintenance agents

**Purpose:** strengthen evidence, privacy, continuity and recovery without
freezing authorised maintenance or changing existing reader-facing Pages
presentation or route behaviour.

`AGENTS.md` is the concise controlling agent instruction. This document explains
how to apply its hard/advisory split.

## Compatibility promise

A governance change is compatible only when it preserves all of the following:

1. any current authenticated ChatGPT thread can prepare a safe update in a clean
   branch;
2. the user can authorise the described commit/push/PR/merge/deploy chain in that
   thread without a special incantation or a commit SHA that does not yet exist;
3. once authorised, mechanically generated IDs do not trigger repeated approval
   requests unless the substantive scope changes;
4. existing public routes, emailed links, fragments, aliases, content, assets,
   base path and Pages configuration remain available;
5. unrelated legacy debt cannot freeze an additive repair or ordinary authorised
   publication; and
6. safety and state claims remain truthful.

This promise does not grant standing authority for an external action. It makes
the repository workflow usable once the user supplies the applicable authority.

## Enforcement matrix

| Control | Ordinary additive publication | Destructive/high-blast-radius work | State claim |
| --- | --- | --- | --- |
| Current `origin/main`, clean isolated worktree, complete diff | Hard | Hard | Hard |
| User authority for push/PR/merge/deploy | Hard | Hard | Hard where an external act is claimed |
| Changed-file privacy and credential review | Hard | Hard | Hard |
| Changed/new allegation status and limiting evidence | Hard | Hard | Hard where relied upon |
| Protected emailed route continuity | Hard if route is touched | Hard | Hard for live continuity |
| Relevant local/path-specific tests | Hard | Hard | Hard where relied upon |
| Exact post-merge Pages verification | Required after a public-surface merge | Required | Hard for `LIVE_VERIFIED` |
| Current independent backup | P0 warning; queue after merge | Hard before destructive action | Hard for `DISASTER_RECOVERY_SAFE` |
| Open evidence explicitly labelled | Allowed | Review impact | Allowed only as `WITH OPEN EVIDENCE` |
| Stale operational snapshots not edited or relied upon | Warning | Review impact | Hard if used to assert current state |
| Legacy privacy debt outside changed files | P0 remediation warning | Review impact | Must be disclosed; not silently closed |
| Unrelated SEO debt, open PRs or specialist checks | Advisory | Review impact | Not evidence of the changed state |

## Public-site surface

For this repository's branch-root Pages model, treat at least the following as
public-runtime or publication-control surface:

- `index.html`, `404.html`, other HTML, and the `es/`, `en/` and `de/` route
  trees;
- browser-consumed CSS, JavaScript, JSON, images, fonts and downloads under
  `assets/` or linked evidence/publication directories;
- `robots.txt`, every sitemap, aliases, `.nojekyll`, base-path and host settings;
- public-route generation/validation scripts, publication manifests and Pages or
  live-verification workflows.

A rules-only package must not change existing reader-facing/runtime or deployment
control paths. Root repository Markdown may itself be publicly downloadable, so
every root governance file must also be public-safe even when it is not linked
from the rendered site. Detailed policy under `.github/` is excluded from Pages
by the current branch-root publication model, but it must still contain no secret
or unnecessary private material.

## Bounded CI and review

The stable universal gate should eventually cover only fresh-base/collision,
changed-file privacy, publication-manifest consistency and core route integrity.
Specialist checks should be selected by changed paths or the package manifest.

Do not require all workflows for every PR. Do not require a human/CODEOWNER
approval until a reliable reviewer exists and the owner/agent maintenance path
has been tested. Do not enable a new required check until it has passed in shadow
mode on representative:

- bilingual content changes;
- route/alias and emailed-link repairs;
- shared asset or loader changes;
- governance-only changes; and
- urgent production fixes.

Existing required checks must not be bypassed silently. If an unrelated check is
flaky or stale, isolate and report it; repair the enforcement design separately
rather than expanding the publication diff.

### Emergency main-ruleset recovery

The ordinary recovery path remains a small corrective or revert PR from current
`main`. Never force-push or delete `main`. Where GitHub supports it, keep
repository-owner/administrator bypass limited to pull requests so an emergency
does not create a routine direct-push path.

Use that bypass only for a documented P0/P1 incident or a confirmed
ruleset/required-check malfunction that prevents an urgent, otherwise-valid PR
from completing. Before use, record the current `main` SHA, the blocked
rule/check, the reason and the smallest intended change in the PR or incident
record; include no private material. Keep the emergency PR free of unrelated
changes and run the Publication integrity gate plus relevant path-specific
validators locally.

After merge, confirm the ruleset is Active, obtain a normal passing required
check, verify the exact merge SHA and affected public routes, and close the
incident with evidence. If the configuration itself interferes with ordinary
authorised maintenance, restore the captured pre-change ruleset state and test
the corrected configuration through a PR.

This is an authenticated repository-owner/administrator contingency, not
standing authority for an agent or future thread. It changes neither repository
visibility, collaborators, secrets nor Pages configuration, and it does not
alter the normal express-authority branch → PR → merge → deploy path.

### Main-ruleset activation continuity — 24 August 2026

This is an implementation-status record, not permission for a future thread to
change account settings. Re-query live GitHub state, current `main` and current
user authority before acting; never infer enforcement from this document.

The last verified pre-activation state was:

- `main` had advanced to `4b1c0d3f9e2ca90b0b215cfe5d9665c90b7c7c9c`;
- active ruleset `Protect main` (ruleset `20860148`) targeted the default branch
  with no exclusions;
- it restricted deletion, required a PR with zero approvals and all three merge
  methods allowed, and blocked non-fast-forward/force-push updates;
- it did not require a status check or conversation resolution; classic branch
  protection reported required-check enforcement off;
- the canonical public baseline fingerprint was
  `8c40d162cc0fac946bffcdce2a97625a5b633c46339f00193e1ff096ead87db8`;
  and
- the proven check selector was `publication-integrity`, reported by GitHub
  Actions (app/integration `15368`), including a successful run on governance PR
  `#928`.

Ruleset activation was **not completed or verified** in the originating thread
because the authenticated GitHub settings session was unavailable. Do not claim
the required check is enforced until the live ruleset and a test PR prove it.

To continue safely in a future authenticated thread:

1. obtain current user authority for the account-setting change, fetch current
   `main`, inspect the live ruleset and capture its current bypass list;
2. keep `Protect main` Active and targeted only at the default branch; retain
   PR-only changes with zero human approvals, all existing merge methods,
   deletion protection and force-push protection;
3. add required check `publication-integrity`, bind it to GitHub Actions, require
   branches to be current before merge, require conversation resolution and,
   where supported, limit repository-administrator emergency bypass to PRs;
4. change no repository visibility, collaborators, secrets or Pages setting;
5. test through a fresh or updated PR: observe the merge blocked while the
   required check is pending, permitted after it passes, and correctly blocked
   while the branch is behind; never test by force-pushing or deleting `main`;
6. if high concurrency produces a demonstrated update/rebuild livelock, relax
   only the strict-current checkbox first; retain the required PR/check and the
   deletion/force-push protections; and
7. if configuration otherwise interferes, restore the captured pre-change
   state, re-test through a PR, and record the live ruleset, PR, check run/job,
   exact merge SHA and result before describing the control as enforced.

## Backup and deletion-safety separation

After a merge, queue a credential-stripped full mirror/bundle and rendered-site
snapshot to genuinely independent storage, with exact SHA, UTC time, hashes and
a restore test. A GitHub Actions artifact alone is not an off-GitHub copy.

Backup lag is a P0 recovery issue but does not block an additive page or link
repair. It does block history rewriting, branch/tag deletion, repository
migration, evidential removal and a `DISASTER_RECOVERY_SAFE` claim.

Likewise, a thread close-out may use the prose classification
`DELETION-SAFE WITH OPEN EVIDENCE` when its decisions, implementation state and
retrieval targets are durably recoverable. This is a continuity qualifier, not
a new publication-manifest `current_state`: manifests continue to use
`DELETION_SAFE` and record open-evidence qualifications separately under their
validated schema. Neither form means the whole repository is disaster-recovery
safe.

## Prospective privacy enforcement

Apply strict allowlists to new or changed email-link continuity records. Public
records may contain route URLs, normalized paths, compatibility destinations,
aggregate occurrence counts, bounded audit timestamps and HTTP/fragment results.
They must not contain recipient identities, subjects, message bodies, provider
message identifiers, private addresses or signatures.

Legacy records require an inventory and deliberate remediation. A global
retroactive validator that fails every unrelated PR is incompatible with this
profile.

## Governance-only acceptance test

Run:

```bash
python3 .github/governance/validate_agent_governance_compatibility.py \
  --base origin/main \
  --governance-only
```

The check fails if the package includes any path outside its narrow governance
allowlist, lacks the controlling invariants, changes a protected publication
surface, or introduces a governance document through a symlink. It is manual and
advisory until the user separately authorises a shadow-mode or required-check
change.

The acceptance test proves that rendered HTML/runtime files, assets and
deployment configuration are unchanged. This package intentionally modifies the
existing Pages-readable `CHATGPT_START_HERE.md` bootstrap and adds a public-safe
root `AGENTS.md` control route; neither is added to site navigation or loaded by
the rendered site. The test does not certify the legal merits of legacy content,
close legacy privacy debt, verify an unmerged change on Pages or grant authority
to publish.
