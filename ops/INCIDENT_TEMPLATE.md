# Production Incident — TEMPLATE

- **Incident ID:** `INC-YYYY-NNN`
- **Detected at (UTC):**
- **Detected by:** human / Production smoke monitor / other
- **Severity:** P0 / P1 / P2 / P3
- **Affected routes/assets:**
- **Observed symptom:**
- **First suspected bad SHA:**
- **Last-known-good evidence/SHA:**
- **Current `main` SHA:**
- **Production verification run/artifact:**

## Containment

- Production freeze applied:
- Unsafe workflow/change disabled or reverted:
- Evidence preserved:

## Root cause

Describe the technical root cause without converting an unverified hypothesis into a finding.

## Recovery

- Revert/corrective PR:
- Restored SHA:
- CI validation:
- Public-host verification:
- Verified at:

## Prevention

- Guardrail added:
- Monitoring/test added:
- Documentation updated:
- Remaining risk:
