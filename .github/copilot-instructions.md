# GitHub outage-agent instructions — Por Derecho / Project Sun Rock

These instructions are an emergency GitHub-side compatibility layer while authenticated GitLab access is unavailable. They do not replace `AGENTS.md`, the canonical registers, or GitLab as the last-known canonical authority.

## Mandatory first reads

1. Read `AGENTS.md` in full.
2. Read `ops/duo/DUO_ORCHESTRATION_PROTOCOL_20260917.md`.
3. Read `ops/continuity/GITHUB_OPERATIONAL_BACKEND_RECOVERY_20260917.md`.
4. Read `ops/continuity/GITHUB_OPERATIONAL_BACKEND_PARITY_20260917.json`.
5. For evidence/registry work, read the relevant canonical root files, including `assets/data/matter-identity-registry-v1.json` and `ops/CURRENT_UNITARY_STATE.json`.

## Outage write lane

Use `continuity/gitlab-block-working-lane-20260917` for outage-period write work unless Gil Marer expressly authorises a different branch. Do not move or overwrite the frozen continuity checkpoints:

- `continuity/gitlab-block-checkpoint-20260917-0920utc`
- `continuity/gitlab-block-parity-checkpoint-20260917`

GitHub `main` is a continuity/public mirror. Last independently verified accessible GitLab canonical main before the block was `7d086d098676eecc2c1647ed09b348d8dc0bdc69`. Do not state that GitHub has complete GitLab parity unless a later exact reconciliation proves it.

## Operating rules

- Current GitHub `main` must be fetched/read before comparing or preparing a change.
- Preserve immutable canonical IDs, provenance, contrary evidence, open gaps, ES/EN parity and public/private boundaries.
- Never infer guilt, knowledge, intent, control or liability from identity, family, corporate, professional or chronological association.
- Never commit raw private email bodies, provider IDs, private Drive locators, credentials, privileged advice or native restricted evidence.
- No email, filing, authority contact, social publication, account/security change or financial commitment is authorised by repository work.
- Use one writer per lane. Read-only audits may inspect but must not race the active writer.
- Green CI is not substantive approval. Admission/provenance/hash gates must not be repinned merely to match an observed value.
- Public-impact classification is advisory and fail-closed: uncertainty means `YES_OR_UNKNOWN`.
- Preserve GitLab-specific exact-recovery items as pending rather than synthesising canonical replacements.

## Minimum validation for outage-backend changes

Run:

```bash
python3 -m unittest discover -s tests -p 'test_github_outage_backend_20260917.py' -v
python3 scripts/classify_public_impact_shadow_20260917.py --paths scripts/classify_public_impact_shadow_20260917.py tests/test_github_outage_backend_20260917.py .github/copilot-instructions.md
```

Then run the existing specialist validators relevant to the changed files. Public/site changes still require normal release acceptance, publication integrity and exact live readback.

This file configures compatible agent behaviour where GitHub tooling supports repository custom instructions. It does not assert that GitHub provides GitLab Duo Developer, Duo Code Review, Orbit, GitLab runner state, or GitLab-native MR/work-item metadata.