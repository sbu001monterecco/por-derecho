# GitHub, website and hostile-takedown protection continuity audit — 28 August 2026

**Control ID:** `PD-GITHUB-PROTECTION-CONTINUITY-20260828-01`

**Scope:** continuity and resilience of the public repository
`sbu001monterecco/por-derecho`, its GitHub Pages publication and the
repository-visible protection controls. This is not a merits finding about any
adverse party, a prediction that a complaint or attack will occur, or evidence
that any identified person has attempted to interfere with the publication.

**Current continuity verdict:** `DELETION-SAFE WITH OPEN EVIDENCE — MERGED,
DEPLOYED AND LIVE VERIFIED`.

**Whole-system verdict:** `DISASTER_RECOVERY_SAFE` is **not claimed**.

## Why this record exists

The originating conversation examined how the Por Derecho publication could
remain available and recoverable if an adverse party used lawful complaints,
platform processes, account compromise, technical interference or other means
to disrupt it. The earlier repository file
`archive/SECURITY_RESILIENCE_AUDIT.md` contained a useful general baseline but
did not preserve the current 28-August observations, the exact distinction
between implemented and proposed controls, or the resulting staged protection
programme.

This record preserves those decisions and gaps outside ChatGPT. A future thread
must re-query live GitHub and the public host; every SHA and count below is an
audit anchor, not a permanent claim about current state.

## Final audit boundary

The audit began on `main` at
`123876bdae297dd4fb38be463d9c89fae4b1fe86`. During the audit, PR
[#1172](https://github.com/sbu001monterecco/por-derecho/pull/1172) repaired two
post-merge verifiers that had treated the immutable 26-August publication
snapshot as mutable current state. It merged as
`8e11f0b72717460ad3a779bafcbdc39876b4a769`.

At that final boundary:

- Pages run
  [33207611090 / #1242](https://github.com/sbu001monterecco/por-derecho/actions/runs/33207611090)
  succeeded for the exact merge SHA;
- all seven workflows associated with the merge completed successfully;
- the Spanish and English homepages returned HTTP 200 and were byte-identical
  to the corresponding files on `main`;
- the repository-preservation validator passed for 3,761 tracked files and 604
  bilingual HTML pages;
- publication integrity passed for 79 manifests;
- audience validation passed for 604 HTML pages, 8,865 internal links and 1,788
  public files;
- 108 workflow files were present, with 241 external action uses and no mutable
  action-version reference located by the audit;
- 34 pull requests remained open, including 20 drafts; and
- production incident
  [#1121](https://github.com/sbu001monterecco/por-derecho/issues/1121)
  remained administratively open even though the verifier repair had merged.

The HTTP and byte-parity findings establish publication state only. They do not
prove the repository cannot later be suspended, deleted, compromised or made
unavailable.

## Protection-control status

| Control | Observed state | Precise limit / next proof |
|---|---|---|
| Static bilingual site and distributed Git history | Implemented | Portable source exists, but the production copy is still concentrated in one GitHub account and host. |
| PR-only `main` workflow | Partially implemented | The last controlled ruleset evidence showed PR-only changes plus deletion and non-fast-forward/force-push restrictions. Live settings must be re-queried before relying on them. |
| Required CI/status check and conversation resolution | Open | `ops/GOVERNANCE_GAPS_STATUS.json`, the 27-August operational router and issue [#355](https://github.com/sbu001monterecco/por-derecho/issues/355) record that required-check enforcement was not proved active. Activate only with separate authority and a test PR that proves pending/behind/green behaviour. |
| Action dependency pinning | Implemented at the audit boundary | All located external action references used full commit SHAs. Re-run the scan after workflow changes. |
| Publication and smoke validation | Implemented inside GitHub | The monitor, Pages build, validators and incident creation are useful, but they share the platform whose loss they are intended to detect. |
| Independent monitoring | Open | Establish monitoring and alert delivery outside the GitHub account for DNS, certificate, representative routes and a signed/current content marker. |
| Independent recovery copy | Historical control exists; current-head closure open | A 19-August off-GitHub ZIP was verified by `git fsck`, test clone and readback and copied to Google Drive and ChatGPT Library. The repository recovery-bundle workflow last ran on 23 August against an older SHA. The workflow named `Off-GitHub Preservation Snapshot` uploads a 90-day artifact to GitHub Actions and is therefore not, by itself, independent disaster recovery. Create and restore-test an independent exact-current-head mirror plus rendered-site snapshot before a current `DISASTER_RECOVERY_SAFE` claim. |
| Ownership continuity | Open | The repository remained owned by the personal account `sbu001monterecco`; no second owner or organisation membership was visible through the connected GitHub account. A dedicated organisation with two trusted owners remains the recommended future control. |
| Account authentication and recovery | Private / unverified | Two-factor methods, passkeys/security keys, offline recovery codes, active sessions, SSH keys, deploy keys, PATs, installed apps and recovery email were not inspectable. Review them privately; never record secrets or recovery codes here. |
| Public/private separation | Open | The public repository still combines the deployable site with archive, evidence, handover and operational records. Filenames such as `private`, `internal` or `archive` do not confer confidentiality. Preserve a legal-hold copy before any later history remediation. |
| Custom domain | Open | No repository `CNAME` or independent custom-domain publication was observed; canonical URLs still used the GitHub Pages hostname. |
| Independent second host | Open | `netlify.toml` is configuration evidence only, not proof of an active independent deployment. A second served copy and tested domain-switch procedure remain unproved. |
| Security-reporting endpoints | Open | Neither root `SECURITY.md` nor `/.well-known/security.txt` existed or returned a live document. Add public-safe reporting instructions that distinguish security reports from legal complaints and corrections. |
| Private legal-response pack | Open | The public legal/privacy/correction architecture is strong, but the audit did not locate one private pack controlling complaint intake, challenged-page snapshots and hashes, source/status/necessity/licensing review, counsel drafts and platform-specific response routes. |
| Workflow and PR operational surface | Open reduction programme | The workflow count increased from 58 in the earlier review to 108 at the final boundary; the open-PR backlog was 34, including 20 drafts. Consolidation and stale-branch review must preserve unique work and may not merge or delete wholesale. |

## Preserved protection programme

### P0 — continuity without changing substantive case content

1. Re-query and enforce the smallest stable `main` ruleset: PR required, the
   stable `publication-integrity` check required, conversation resolution,
   deletion protection and force-push protection, with a documented emergency
   repair path. Account-setting changes require separate authority.
2. Create a genuinely independent exact-current-head mirror, rendered-site
   snapshot, SHA-256 manifest and clean restore test. GitHub Actions artifacts
   do not satisfy this control by themselves.
3. Review account recovery, sessions, credentials and installed applications
   privately. Do not publish authentication or recovery material.
4. Close or update production incident #1121 only after the repaired monitor or
   its verified successor demonstrates the incident condition is no longer
   present.
5. Add `SECURITY.md` and `/.well-known/security.txt` through an ordinary
   public-safe PR.

### P1 — remove platform and ownership concentration

1. Move repository ownership to a dedicated organisation with two trusted
   owners and least-privilege roles, without changing editorial authority by
   implication.
2. Adopt and verify a controlled custom domain with registrar lock, MFA,
   renewal controls, protected recovery contacts and DNS security where
   supported.
3. Serve one signed/static release from GitHub Pages and an independent static
   host, and test the recovery/domain-switch procedure.
4. Separate private evidence/working custody from a minimal public publication
   repository through a sanitised build. Never treat deletion from the current
   tip as deletion from public Git history.
5. Create the private legal-response pack and complaint register. Resilience
   must preserve the ability to correct, redact and comply with lawful orders;
   it must not depend on irreversible public archives of disputed personal
   material.

### P2 — reduce avoidable operational failure

1. Replace overlapping live-verification workflows with a manifest-driven
   matrix while retaining specialist checks that test materially different
   risks.
2. Review the 34 open PRs against current `main`, transplant only unique safe
   deltas, and close superseded branches only after preservation review.
3. Keep one stable required-check name and refresh operational-truth records
   without rewriting historical deployment evidence.

## Authority and public/private boundary

This continuity closeout authorises repository preservation of the public-safe
audit and its normal branch, PR, merge and verification chain. It does **not**
authorise:

- changing GitHub account settings, ownership, collaborators, rulesets,
  credentials, tokens, keys, domains or hosting;
- deleting branches, artifacts, evidence, repository history or public routes;
- publishing private evidence, privileged advice, authentication data or
  recovery codes;
- sending email, filing a complaint, issuing a counter-notice, contacting a
  platform, authority, professional, journalist or adverse party; or
- asserting that any adverse party caused or attempted a takedown.

Every later external act retains its own authority, recipient-resolution,
privacy and counsel gates.

## Deletion-safety dimensions

| Dimension | Result |
|---|---|
| `THREAD_REASONING_CONTINUITY` | **PASS after this record is merged and read back** — findings, decisions, qualifications and restart instructions no longer depend on chat. |
| `IMPLEMENTATION_STATE_CONTINUITY` | **PASS after merge/readback** — implemented, partial, open and private/unverified controls are distinguished. |
| `PRIMARY_EVIDENCE_COMPLETENESS` | **OPEN / NOT APPLICABLE AS A GLOBAL CLAIM** — private account settings and future hostile acts were not proved or presumed. |
| `LIVE_PUBLICATION_VERIFICATION` | **PASS at the `8e11f0b7…` audit anchor** — exact Pages success and homepage byte parity were observed. Future state must be re-queried. |
| `COMMUNICATION_VERIFICATION` | **NO ACTION PERFORMED OR AUTHORISED**. |
| `CUSTODY_RESILIENCE` | **PARTIAL** — a verified 19-August independent copy exists, but exact-current-head preservation was not proved. |
| `DISASTER_RECOVERY_SAFETY` | **NOT CLAIMED**. |

## Restart path

A future thread should:

1. read `CHATGPT_START_HERE.md`, `AGENTS.md`, this record,
   `archive/SECURITY_RESILIENCE_AUDIT.md`,
   `ops/GITHUB_MISSION_CRITICAL_RUNBOOK.md`,
   `ops/GOVERNANCE_GAPS_STATUS.json` and
   `.github/governance/AGENT_PUBLISHING_COMPATIBILITY.md`;
2. resolve current `origin/main`, the latest Pages deployment, open production
   incidents, open PR count and current live route parity;
3. privately inspect account/security controls only with current authority;
4. verify the newest independent backup by exact source SHA, hash, readback and
   restore test; and
5. report changes as facts with timestamps, without converting an earlier open
   recommendation into a completed safeguard.

## Publication and closeout evidence

- Source PR:
  [#1174](https://github.com/sbu001monterecco/por-derecho/pull/1174),
  reconciled head `dd2f45d16b475f4d82b5a86cb58cbd1cbcbf76ba`.
- PR validation: all nine triggered workflows completed successfully, including
  publication integrity, private-source/OSINT governance and the preservation
  snapshot workflow. The latter remains a GitHub-hosted artifact and does not
  change the independent-backup limitation stated above.
- Merge: PR #1174 merged to `main` as
  `2b2d24562a082a311601451736e50fb32d12df60`.
- Post-merge validation: all nine workflows associated with the exact merge
  completed successfully.
- Deployment: Pages run
  [33208771146 / #1244](https://github.com/sbu001monterecco/por-derecho/actions/runs/33208771146)
  completed successfully for the exact merge SHA.
- GitHub source readback: the continuity record, deletion-audit index and
  security-audit pointer were fetched at the merge ref with blob SHAs
  `02c81d39c51e47af038bacc74d392a934985a2ff`,
  `37299e4c831e20e0ef7bdb27feef272c1c2fdcad` and
  `5e4fc2817f5dd6eefa2bfc9745c1efb7fcc0956a`.
- Public-host readback at `2026-08-28T20:37:00Z`: all three Markdown files
  returned HTTP 200 as `text/markdown` and were byte-identical to the merged
  repository files. Their SHA-256 values were respectively
  `a2f1af46bfdb51d44788a36813028b957b0b2010a0eefa6d3f77b759bcc5750a`,
  `306f872abd84262fda5f6a2971b30d85808b018d0e5e0930eef59e6060818172`
  and `8923a43fa785c4a38ef67a30b892e28313a52a3cb7a2879c35e50b5d95ae9f27`.

This evidence closes the conditions that were expressed prospectively in the
first source-controlled version of this record. It proves continuity and live
publication of the closeout package; it does not close any separately listed
resilience control.

## Final continuity conclusion

The record and its deletion-audit index entry are merged to `main`, independently
read back and supported by passing repository checks. The originating
protection-review conversation is therefore **DELETION-SAFE WITH OPEN
EVIDENCE**. Its deletion will not erase a material finding, decision,
qualification, authority boundary, completion proof or restart instruction.

That conclusion is deliberately narrower than whole-system safety. The single
account, required-check, current independent-backup, public/private split,
custom-domain, second-host, external-monitoring, security-endpoint and private
legal-response controls remain open until separately implemented and verified.
