# Caret public-surface gap closure — continuity handover

**Control date:** 2 September 2026  
**Control:** `PD-SP-CARET-SURFACE-20260902-01`  
**Repository:** `sbu001monterecco/por-derecho`  
**Base remote main:** `6013473e0e510948d2702fe0b4f5f6cfe45f7028`  
**Implementation branch:** `codex/caret-public-surface-gap-closure-20260902`  
**Current state:** implementation branch prepared; PR, merge, deployment and live readback not yet recorded in this handover

## 1. Why this work exists

The initiating audit used these examples:

- `AUREN REESTRUCTURACIONES SLP`; and
- `Guillermo Fernández García`, electronic signatory of Auto 97/2025.

Both identities were already present in the federated CAEPR registry and were
already `CARET_CONFIRMED`:

- Auren exact entity: `PD-SP-O-0070`;
- Guillermo Fernández García: `PD-SP-P-0087`.

The defect was on the bilingual Meeting Point 357/2024 public surface: the page
printed the names but did not visibly propagate the caret, immutable ID and
canonical identity link. The correction therefore reuses both IDs. It does not
create duplicate people or organisations.

## 2. Implemented repair

The Spanish and English Meeting Point pages now:

- print each exact identity with `<sup>^</sup>`;
- expose `data-caepr-id` and `data-caret-state="CARET_CONFIRMED"`;
- print the immutable CAEPR ID visibly;
- link to the canonical matter-identity register anchor;
- add a dedicated identity/boundary section;
- preserve the signed Auto 97/2025 chronology;
- preserve the unresolved 24 October 2024 signed-act/allocation question;
- preserve the Auren mandate, receipt, custody, disclosure and workpaper questions;
- preserve right-of-reply, lateral evidence and reciprocal AM357 links; and
- update bilingual metadata to 2 September 2026.

Affected public source paths:

- `es/cuaderno-juridico/meeting-point-357-2024-trazabilidad-judicial/index.html`
- `en/legal-notebook/meeting-point-357-2024-judicial-traceability/index.html`

## 3. New durable governance and controls

Created:

- `.github/governance/CAEPR_PUBLIC_SURFACE_PROPAGATION_AND_CONTINUITY_GATE_02SEP2026.md`
- `assets/data/caret-public-surface-coverage-v1.json`
- `scripts/validate_caret_public_surface.py`
- `.github/workflows/verify-caret-public-surface-propagation.yml`
- `publication-manifests/caret-public-surface-gap-closure-20260902.json`
- this handover

The validator has two deliberately separate modes:

1. **strict finite coverage** for the two declared bilingual surfaces and the two
   immutable identities; and
2. **advisory archive-wide exact-name discovery** to locate likely unmarked
   confirmed names without authorising mass edits or turning quotations into
   editorial identity assertions.

The workflow also runs the existing operational identity-registry validator and,
on a main-branch push, performs cache-busted readback of both public routes and
the control JSON.

## 4. Identity and inference boundaries

The caret confirms canonical identity only.

For `PD-SP-O-0070`, the signed appointment does not itself establish:

- final mandate scope;
- documents requested or received;
- work performed;
- Sun Park/Club Sei knowledge;
- preservation or disclosure; or
- responsibility.

For `PD-SP-P-0087`, the electronic signature on Auto 97/2025 does not itself
establish:

- authorship or participation in the separate 24 October 2024 act;
- allocation or substitution on that date;
- Sun Park knowledge;
- coordination, impropriety or criminality; or
- responsibility in another proceeding.

The generic Auren professional perimeter `PD-SP-O-0046` remains distinct from the
exact appointed entity `PD-SP-O-0070`.

## 5. Open identity/source gaps intentionally not closed by inference

The existing justice-professionals production queue remains controlling.

Named `CARET_PENDING` records:

- `PD-SP-P-0138` Carmen Martínez Socias — `JP-EQ-004`;
- `PD-SP-P-0139` Nicolás Quintana Plasencia — `JP-EQ-005`;
- `PD-SP-P-0143` Pedro Eugenio Botella Torres — `JP-EQ-006`.

Other source families reused rather than duplicated:

- `LL-JUD-GAP-001` — exact judicial signatory of Auto 454/2026;
- `LL-JUD-GAP-002` — LAJ identity/identities for material PO 344/2013 acts;
- `LL-JUD-GAP-003` — downstream DP 748/2026 appellate organ/roll/judge/LAJ;
- `JP-EQ-002` — signed DP 1901/2026 Fiscalía report and author;
- `JP-EQ-003` — post-report judicial/LAJ/service chain;
- `JP-EQ-007` — exact named Property Registry person in a dated act; and
- `JP-EQ-009` — E.G. 745/2026 allocation/examination/approval chain.

No name is to be guessed from office, date, neighbouring act or later signatory.

## 6. Validation contract

Run from repository root:

```bash
python3 -m py_compile scripts/validate_caret_public_surface.py
python3 scripts/validate_caret_public_surface.py \
  --report artifacts/caret-public-surface-audit/report.json
python3 scripts/validate_operational_identity_registry.py
python3 scripts/validate_repository_preservation.py
python3 scripts/validate_publication_integrity.py
python3 scripts/validate_audience_experience.py
```

The new validator must report strict `PASS`. Archive-wide candidates remain an
advisory evidence-production/backfill list unless separately reviewed and added
to the finite strict manifest.

## 7. Successor-thread bootstrap

A successor must first fetch current remote `main`; the SHA above is only the
base of this implementation branch. Then read:

1. `AGENTS.md`;
2. `CHATGPT_START_HERE.md`;
3. `.github/governance/CAEPR_CARET_IDENTITY_AND_ALL_IS_VERIFICATION_PROTOCOL_26AUG2026.md`;
4. `.github/governance/CAEPR_PUBLIC_SURFACE_PROPAGATION_AND_CONTINUITY_GATE_02SEP2026.md`;
5. `assets/data/matter-identity-registry-v1.json` and its declared parts;
6. `assets/data/caret-public-surface-coverage-v1.json`;
7. `assets/data/justice-professionals-evidence-production-queue-v1.json`;
8. `publication-manifests/caret-public-surface-gap-closure-20260902.json`; and
9. this handover plus any later PR/live closeout.

The successor must report one of these states explicitly:

- `REGISTERED_AND_CONFIRMED`;
- `REGISTERED_BUT_PUBLIC_OCCURRENCE_GAP`;
- `CARET_PENDING_SOURCE_REQUIRED`;
- `UNKNOWN_PERSON_SOURCE_REQUIRED`;
- `PR_READY_NOT_LIVE`; or
- `MERGED_LIVE_VERIFIED`.

## 8. Merge and live closeout still required

Before claiming the gap is publicly closed:

1. compare the branch against current `main` and reconcile overlap additively;
2. obtain/record the PR and passing required checks;
3. merge without force-push or history rewrite only within current authority;
4. record the exact merge SHA and Pages deployment;
5. perform cache-busted ES/EN and control-JSON readback;
6. verify the visible carets, IDs, links, identity boundaries and existing AM357
   links; and
7. update this handover or add a live closeout record.

An open PR is not live. A successful deployment without exact route/readback is
not `LIVE_VERIFIED`.

## 9. Authority and deletion-safety boundary

This package authorises no email, filing, service, source destruction, authority
contact, credential use, private-source publication or unsupported identity
promotion.

The implementation reasoning and open tasks are now durably preserved. The
thread may be continuity-safe for handoff once the PR/check state is added, but
publication/deployment deletion safety is not claimed until the merge and live
closeout are recorded.