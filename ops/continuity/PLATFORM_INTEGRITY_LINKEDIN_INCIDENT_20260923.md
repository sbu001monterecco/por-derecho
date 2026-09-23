# Platform integrity / LinkedIn incident continuity — 23 September 2026

**Control:** PD-PLATFORM-INTEGRITY-20260923-01  
**Status:** PUBLIC-SAFE CONTINUITY RECORD  
**Scope:** LinkedIn current restriction + cross-platform preservation hub.

## Current evidence

- 22 September 2026 LinkedIn security email: profile photo changed at 13:51 GMT, Android, provider-reported approximate location Kuwait City, Kuwait.
- The alert was found in the business mailbox Trash folder during the 23 September review. Cause of that mailbox state is unknown.
- 23 September 2026: Gil Marer reports LinkedIn account access blocked again; renewed identity verification completed; restoration and provider explanation pending.
- At the time of the review, no fresh LinkedIn restriction/moderation email explaining the 23 September event was located.
- Historical cases 241020-015316 and 241028-011722 were both restored after identity verification; LinkedIn described detected suspicious activity but did not identify an external actor.

## Bounded cross-platform controls

- Google Business Profile: documented management-request and profile-state events are preserved; who caused later closure states remains open.
- GitLab: the September 2026 account-level 403 is preserved with provider support references; a temporary login-lock mechanism was considered but did not explain the full observed duration. No external actor is established.
- GitHub: the September 2026 user-facing access-path interruption is kept separate from the connected integration and Pages, which remained operational. Cause and scope remain open.

These events are grouped for preservation and continuity only. They do not establish a common actor or mechanism.

## Mandatory proof boundary

Do not attribute any LinkedIn restriction, report, profile edit, Google event, GitHub/GitLab access incident or other platform event to a named person without provider-native evidence. Possible motive or incentive is contextual evidence only. Chronology is not causation; repeated events are not proof of agreement, conspiracy or criminal liability.

## Public projection

- EN: `/en/platform-integrity-evidence/`
- ES: `/es/integridad-plataformas-evidencia/`
- Machine-readable register: `assets/data/platform-integrity-events-v1.json`

The public page requests preservation of native account-security, moderation, reporting and audit records while withholding authentication-bearing links, message IDs, private session/IP data and reporter identities.
