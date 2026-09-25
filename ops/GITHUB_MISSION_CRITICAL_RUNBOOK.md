# Por Derecho — Mission-Critical GitHub / GitHub Pages Runbook

**Production repository:** `sbu001monterecco/por-derecho`  
**Production branch:** `main`  
**Public host:** `https://sbu001monterecco.github.io/por-derecho/`

## 1. Authorities

No chat, agent, local worktree or branch marker is authoritative about production.

1. Git tree proves source preservation.
2. CI proves reproducible validation.
3. `main` proves merge.
4. The public host proves deployment.
5. A post-deployment verification record proves `LIVE_VERIFIED`.
6. A recoverable remote record plus tested continuity gates proves deletion safety.

The publication state machine in `archive/UNIVERSAL_PUBLICATION_AND_THREAD_DELETION_SAFETY_PROTOCOL_18AUG2026.md` remains controlling.

## 2. Normal production change

1. Start from current `main`.
2. Put actual reviewable source in remote Git; do not use a chat/session or partial encoded payload as the only copy.
3. Open a PR.
4. Require the publication-integrity gate and all path-specific tests to pass.
5. Review high-blast-radius paths listed in `ops/CRITICAL_PATHS.txt`.
6. Merge without force-pushing or rewriting `main`.
7. Wait for the public-host verification workflow.
8. Treat the release as live only after the public host serves the release-specific probe/markers.

## 3. GitHub tooling fallback

Preferred control path:

`GitHub connector/API → authenticated gh CLI → ordinary git → BLOCKED_RECOVERY`

A missing optional tool must not reduce preservation or publication guarantees. If no safe remote write path exists, preserve locally, classify the work `BLOCKED_RECOVERY`, and do not claim completion.

## 4. Incident / rollback

For a suspected production regression:

1. **Detect.** Preserve the failing workflow, route, timestamp and SHA.
2. **Freeze.** Stop preference-only or unrelated production merges until the failure is understood.
3. **Identify last-known-good.** Use `ops/LAST_KNOWN_GOOD.json`, `ops/PRODUCTION_STATUS.json` and permanent deployment evidence. Do not guess an exact live SHA.
4. **Revert.** Prefer a normal `git revert`/revert PR of the first bad production change. Do not force-push `main`.
5. **Validate.** Run the universal gate plus path-specific checks.
6. **Merge and deploy.**
7. **Live verify.** Require public HTTP + content markers, not repository presence.
8. **Record.** Create/update a production incident using `ops/INCIDENT_TEMPLATE.md` and document the preventive change.

If a global loader (`assets/site.js`, shared loader/CSS, homepage or deployment workflow) is implicated, treat the incident as P0/P1 until blast radius is known.

## 5. Backup and restore

The scheduled `Repository recovery bundle` workflow (and any push that changes that workflow itself) creates a verified `git bundle` containing all fetched branches/tags and uploads it as a GitHub Actions artifact. This is useful recovery material but is **not independent disaster recovery** because it remains on GitHub.

Independent mirroring becomes active only when the repository secret `POR_DERECHO_BACKUP_MIRROR_URL` is configured.

### Restore from a bundle

On a fresh machine:

```bash
git clone por-derecho-<sha>.bundle por-derecho-restored
cd por-derecho-restored
git fsck --full
git show-ref
```

Then add a new trusted remote and push only after verifying the expected `main`, tags and evidence-bearing refs.

A disaster-recovery claim is not complete until a bundle/mirror has been restored in a clean environment and the static site has been served/validated from that restored copy.

## 6. Required `main` ruleset / protection setting

Repository source cannot itself enforce GitHub branch rules. Administratively enable, where supported:

- require a pull request before merging;
- require `Publication integrity gate / publication-integrity`;
- block force pushes;
- block deletion of `main`;
- require conversation resolution;
- require branches to be current before merge where operationally appropriate;
- use CODEOWNERS review for production infrastructure where supported;
- keep administrator bypass explicit and emergency-only;
- enable repository Actions policy requiring full-length commit-SHA pins if available.

Until GitHub reports those controls as enforced, branch-governance readiness remains amber/red regardless of passing CI.

## 7. Production observation

- `Production smoke monitor` checks ES, EN, RICPE, CNMV, the global loader and the hardening probe every two hours.
- On failure it opens or updates a GitHub issue titled `[PRODUCTION] GitHub Pages smoke check failed`.
- Evidence is retained as an Actions artifact.
- The monitor is not a substitute for external independent uptime monitoring, but it removes silent GitHub-Pages failures from the normal operating model.

## 8. Risk classification

- **P0:** production outage, recovery, credential/security, destructive Git risk.
- **P1:** shared loaders, global styles/navigation, CI/deployment infrastructure.
- **P2:** major route/publication.
- **P3:** isolated content.

P0/P1 changes require the strictest validation and a known rollback path.
