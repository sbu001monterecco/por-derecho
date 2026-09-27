# ChatGPT answer-status traffic-light rule — 27 September 2026

**Control ID:** `PD-CHATGPT-ANSWER-COLOR-20260927-01`  
**Scope:** Por Derecho / Project Sun Rock / AWESWELL-related ChatGPT, ChatGPT Work, Codex and agent responses.

## Mandatory visible status

Every substantive response that reports, assesses or changes task state must visibly show the relevant traffic-light status. Do not leave the status implicit in prose.

Allowed statuses:

- **🟢 GREEN** — complete, verified, preserved, live/read back where applicable, or no material blocker remains for the stated scope.
- **🟠 AMBER** — partial, pending, unverified, dependent on another step/system, or contained but not yet fully closed.
- **🔴 RED** — material blocker, failed control, unresolved integrity/safety problem, or a condition that prevents the claimed completion/readiness.

## Presentation rule

1. Put an explicit overall status near the start of the answer: `🟢 GREEN`, `🟠 AMBER`, or `🔴 RED`.
2. When several systems/workstreams have different states, show the relevant color beside each component.
3. Mixed-state aggregation is conservative:
   - any RED component → overall **🔴 RED**;
   - otherwise any AMBER component → overall **🟠 AMBER**;
   - all in-scope components GREEN → overall **🟢 GREEN**.
4. Never call something GREEN merely because work was attempted. GREEN requires the verification appropriate to the claim (for example commit/readback, delivery/receipt, live deployment, or durable preservation).
5. If current verification is unavailable, use AMBER unless a RED trigger is known.
6. The color is an operational/readiness status only. It must not be used to imply guilt, legal merit, evidential weight, institutional wrongdoing, or the truth of an allegation.
7. Do not omit the color because the answer is short, obvious, or positive.

## Continuity / preservation audit — mandatory colour block

A response or persisted artifact described as a **continuity audit**, **preservation audit**, **continuity and preservation audit**, **deletion-safety audit**, **readiness audit** or materially equivalent closeout must never be prose-only.

Near the start of the answer **and** near the start of any persisted audit artifact, show:

1. `Overall operational/readiness: 🟢 GREEN | 🟠 AMBER | 🔴 RED`;
2. a **Component statuses** block/table in which every material in-scope system or workstream has its own explicit colour; and
3. the conservative aggregation result.

For continuity/preservation audits, include the following components whenever they are in scope: external filings/receipts, durable file custody/Google Drive, GitHub, GitLab, deployment/live readback if claimed, and unresolved evidential/routing controls. A component with an actually failed CI/pipeline/control is **🔴 RED**, even when its source branch or draft is safely preserved. A non-blocking unresolved dependency or unverified follow-up is **🟠 AMBER**. A component is **🟢 GREEN** only when the claim being made about it has been verified.

The persisted audit artifact must carry the same colour summary as the user-visible closeout. It is not sufficient for the chat answer to have colours if the durable audit omits them, or vice versa.

Finish the substantive response with the separate thread-deletion sentinel from `PD-THREAD-SENTINEL-20260925-01`. Operational/readiness colour and deletion-safety colour may differ and must not be collapsed.

A lightweight validator may check this presentation in advisory/shadow mode. It is **not** a new repository-wide required CI gate unless separately promoted under the enforcement-change rules in `AGENTS.md`.

## Separate thread-deletion status

The existing `PD-THREAD-SENTINEL-20260925-01` remains independent. Task/readiness color and thread-deletion color answer different questions.

Example:

- **🟢 GREEN — GitHub:** merged and live-verified.
- **🟠 AMBER — GitLab:** checkpoint preserved but not merged to protected main.
- **Overall: 🟠 AMBER.**
- `🟢 THREAD — safe to delete` may still be correct if the conversation itself is fully preserved elsewhere.

Do not collapse the two controls into one status.

## Persistence

This rule must be referenced from `AGENTS.md` and `CHATGPT_START_HERE.md`, and mirrored into durable private continuity storage where available. Future threads must apply it without requiring the user to repeat the preference.
