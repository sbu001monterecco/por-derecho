# SECURITY & RESILIENCE AUDIT

> **Current continuation — 28 August 2026:** read
> `docs/deletion-audits/2026-08-28-github-hostile-takedown-protection-continuity.md`.
> It preserves the later live audit, the exact implemented/open/unverified
> distinctions and the staged protection programme. The baseline below remains
> historical context and must not be treated as proof of current settings.

Scope: repository/source-control and recovery posture visible to ChatGPT. This is not a substitute for reviewing GitHub account-level settings in the UI. Do not change high-impact account controls without explicit user approval.

## Current strengths observed
- public Git repository provides distributed history rather than a single mutable website copy;
- substantive recent work generally uses branches and pull requests;
- GitHub Pages is served from repository source and can be independently checked through the Pages build API;
- repeated PR descriptions preserve evidential/publication safeguards and validation history;
- source corrections are now preserved in a canonical correction register;
- the site is static and therefore comparatively portable to another static host.

## Risks and controls
| Risk | Current control | Gap / residual risk | Recommended action | ChatGPT authority |
|---|---|---|---|---|
| Repository deletion / account loss | Git history on GitHub | one hosted account remains a concentration risk | maintain independent mirror + periodic full clone/archive | document now; external credentials/user approval may be required |
| Unauthorized write | PR-oriented workflow | account/branch rules not fully audited in this file | verify `main` protection: PR required, force-push disabled, deletion disabled, appropriate bypass rules | inspect; ask approval before changing high-impact permissions |
| Accidental overwrite | branch/PR history | direct pushes may still be possible depending settings | enforce PR-before-merge and protected `main` | approval before permission change |
| Credential compromise | GitHub platform controls | token/session/2FA state not established here | review 2FA, active sessions, PATs, OAuth/GitHub Apps, deploy keys | user approval/account interaction required |
| Secret leakage | public repository | historical/public files could accidentally include credentials/private sources | periodic secret/privacy scan; never commit private Gmail/Drive locators or privileged evidence | safe audit/removal PR; destructive history rewrite needs approval |
| Single-copy evidence loss | public-safe handovers in repo | private originals live elsewhere | maintain Drive/Library/private evidence custody plus export manifest | documentation safe |
| Pages failure | merge history + Pages API | deployment can lag/fail independently of merge | verify each public merge and log build | safe/autonomous |
| Stale or contradictory intelligence | specialist handovers | old summaries can outlive corrections | root start file + correction register + canonical matrices | safe/autonomous |
| Stale open PRs | PR #17 and #19 remain open from older base states | merging old branches could reintroduce superseded material | rebase/re-review against current `main` before any merge; do not merge merely because GitHub says mergeable | safe review; merge only after substantive validation |

## Backup / portability minimum
1. Maintain at least one independent full Git mirror or periodically refreshed clone outside the primary GitHub account.
2. Periodically export a timestamped repository archive plus a manifest containing current `main` commit and Pages configuration.
3. Keep domain/site content static-host compatible; avoid coupling critical evidence navigation to a proprietary runtime.
4. Document restoration: create new repository → push full mirror → configure Pages/static host → verify internal links → repoint any custom domain if applicable.
5. Keep private evidence outside public GitHub while preserving stable evidence IDs/metadata sufficient to locate originals lawfully.

## Security actions requiring explicit approval
- change repository visibility;
- add/remove collaborators or alter roles;
- change branch-protection/bypass rules;
- revoke/create tokens, OAuth apps, deploy keys or SSH keys;
- delete branches with unresolved unique work;
- delete repository or rewrite published Git history;
- configure external mirror credentials.

## Next security review
Verify actual `main` branch protection and account-level credential/session controls, then update this file with the observed state rather than assumptions.
