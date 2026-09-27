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
