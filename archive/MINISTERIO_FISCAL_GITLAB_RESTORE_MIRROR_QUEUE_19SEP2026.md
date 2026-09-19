# Ministerio Fiscal — GitLab restoration mirror queue — 19 September 2026

## Purpose

Preserve a deterministic, deletion-safe handover from the temporary GitHub working lane back to the canonical GitLab repository once account/repository access is restored.

## Controlling rule

GitLab `main` remains the canonical Por Derecho repository when it is accessible. The current GitHub repository is an active continuity/recovery lane while GitLab is blocked. **Do not blind-copy GitHub over GitLab.** On restoration:

1. fetch the then-current GitLab `main`;
2. compare it with GitHub `main` and this Ministerio Fiscal branch/change set;
3. preserve any newer GitLab work;
4. port only the net source-controlled delta;
5. run all GitLab validators/pipelines;
6. verify the public GitLab Pages routes after deployment;
7. record the GitLab commit/MR/pipeline IDs back into this control.

## Change set queued for mirror

- `assets/data/ministerio-fiscal-canonical-register-20260919.json`
- `es/ministerio-fiscal/registro-canonico/index.html`
- `en/public-prosecution-service/canonical-register/index.html`
- `scripts/validate_ministerio_fiscal_canonical_register_20260919.py`
- hub navigation updates pointing to the new register
- any subsequent corrections committed to the same GitHub lineage before GitLab restoration

## Canonical identity rules to preserve

- existing `PD-MF-OFF-####` office identities are never renumbered;
- existing proceedings Master IDs remain controlling;
- existing CAEPR person IDs `PD-SP-P-####` remain controlling where present;
- cross-register `PD-MF-PER-####`, `PD-MF-ENT-####`, `PD-MF-REG-EVT-####` and `PD-MF-EVD-####` are linkage identities, not official Fiscalía references;
- E.G. 19/2026 and E.G. 58/2026 remain explicitly marked as Master Register reconciliation gaps until an existing or newly admitted Master ID is source-controlled.

## Privacy / source rule

Provider message IDs, Gmail thread IDs and private custody locators stay outside the public register. Public pages may identify the existence, class, date and proof function of a private source without exposing the provider locator.

## Completion condition

This queue is closed only after the GitLab merge is made against the then-current canonical `main`, the pipeline passes, and the Spanish and English canonical-register routes are opened from the deployed GitLab Pages site.