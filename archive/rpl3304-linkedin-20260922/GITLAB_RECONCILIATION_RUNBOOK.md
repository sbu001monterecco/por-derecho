# R33 / RPL 3304 — GitLab reconciliation runbook

Control date: 22 September 2026

Status: `PENDING_ACCESS_RESTORATION`

## Controlling state

Until GitLab access is restored and a reviewed reconciliation completes, GitHub `main` is the controlling public source for this package. Do not infer parity from the availability of a GitLab-hosted website, and do not overwrite a newer GitLab state without comparison.

The GitHub state from which this preservation package starts is merge commit `3fb4321536fc803768b02fe05d52d8b0d74f8322`, which merged PR #1743 and records the deployed R33 visual-linkage release.

## Restore procedure

1. Restore ordinary authorised GitLab repository access. Do not bypass account, repository or provider restrictions.
2. Record the GitLab project URL, default branch, current head SHA and deployment/pipeline state before writing.
3. Fetch current GitHub `main` and the GitLab default branch into a clean working clone.
4. Identify the merge base and compare both histories. Treat each side as potentially containing unique work.
5. Reconcile the package paths listed in `release-manifest.json`; do not force-push and do not import unrelated open GitHub PRs.
6. Preserve the signed-native/private versus public-safe boundary. The private signed PDF, private forensic case JSON, private locators, certificate data and privileged material must remain outside public Git.
7. Keep PR #1696 closed and unmerged. Do not revive it or merge it wholesale. Treat PR #1734 as a stale superseded audit lane. PR #1737 is not part of this package unless separately reviewed and merged.
8. Validate every file against `SHA256SUMS.txt` before committing.
9. Run the GitLab repository's normal privacy, publication-integrity, link and deployment checks.
10. Verify the Spanish page, English page and public PDF after deployment. Record the GitLab commit, pipeline and live readback in a new immutable receipt.

## Required public routes

- Spanish reader: `https://sbu001monterecco.github.io/por-derecho/es/concurso-36-2012-oposicion-ac-apelacion-lpb-septiembre-2026/`
- English reader: `https://sbu001monterecco.github.io/por-derecho/en/insolvency-36-2012-ac-opposition-lpb-appeal-september-2026/`
- Public PDF: `https://sbu001monterecco.github.io/por-derecho/evidence/insolvency-36-2012/concurso-autos/pdfs/R33-ac-oposicion-apelacion-lpb-septiembre-2026.pdf`

## Prohibited recovery shortcuts

- no force-push over an unreviewed GitLab head;
- no public upload of the signed native source or private forensic package;
- no replacement of the canonical R33 viewer with PR #1696 or another competing implementation;
- no statement that a court found lying, intent, coordination or criminal guilt;
- no treating the parody image as evidence;
- no description of RSM as Borja's employer;
- no entity-wide allegation against Grant Thornton or PwC;
- no treatment of silence as an admission.

## Completion receipt

The later GitLab receipt must record:

- GitHub source SHA;
- GitLab target SHA before reconciliation;
- GitLab merge/deployment SHA;
- changed paths;
- package SHA-256 verification;
- privacy and publication-check results;
- live URLs and HTTP/PDF readback;
- any deliberate divergence with reasons.
