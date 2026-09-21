# La Laguna judicial ^ register — PR #1330 reconciliation closeout

Control date: 1 September 2026  
Current-main baseline at reconciliation start: `95f4e932eba0b3c598d6b2272ae3393e3bab9ba7`  
Historical branch: PR #1330 / `fix/la-laguna-judicial-gap-publication-20260901`

## Result

PR #1330 must not be merged wholesale. It was based on an older canonical denominator and was overtaken materially by merged PR #1332 and PR #1334. This successor release preserves only the still-unique La Laguna publication, route and finite-source gap controls on top of current main.

The source-identifiable La Laguna judicial denominator remains closed for the presently recovered primary corpus. The certified-complete historical court denominator is not claimed. `LL-JUD-GAP-001`–`003` remain explicit source gaps unless a primary closure trigger is obtained.

## Material corrections inherited from later canonical work

- Current matter-identity denominator: 339 total / 160 people / 83 organisations / 11 structures / 42 institutions / 43 proceedings at reconciliation start. Never restore PR #1330's stale 331/157-era totals.
- Carlos Llamas Sanz remains canonical `PD-SP-P-0062`; do not mint or revive stale reserved `PD-SP-P-0146`.
- DP 748 current procedural control is `assets/data/dp748-2026-appeal-reopening-control-v1.json` from merged PR #1332.
- The 20-May-2026 Providencia verifies that the reform and subsidiary appeal were interposed in time and form at the origin court. The remaining appellate gap concerns downstream Article 766.4 transfer/remittal/transmission, appellate roll and appellate office-holders—not origin-court admission.
- PR #1334 is the live/deployment closeout for the DP 748 successor package.

## PR #1330 file-by-file disposition

### Transplanted / successor-recreated on current main

1. `.github/workflows/validate-la-laguna-judicial-register.yml` → recreated as a current-main-aware specialist gate.
2. `archive/LA_LAGUNA_JUDICIAL_REGISTER_GAP_CLOSURE_01SEP2026.md` → consolidated into this closeout plus the machine gap audit.
3. `archive/PR1324_SUPERSESSION_MAP_01SEP2026.md` → substantive supersession already established by PR #1332; this closeout records #1330's own supersession.
4. `assets/data/la-laguna-judicial-actors-gap-closure-audit-v1.json` → transplanted and corrected for the verified 20-May origin-court admission.
5. `assets/data/matter-identity-registry-v1.la-laguna-judicial-institutions.json` → current records retained; bilingual aggregate routes added.
6. `assets/data/matter-identity-registry-v1.la-laguna-judicial-people.json` → current records retained; bilingual aggregate routes added.
7. `en/la-laguna-judicial-register/index.html` → recreated on current main semantics.
8. `es/registro-judicial-la-laguna/index.html` → recreated on current main semantics.
9. `scripts/validate_la_laguna_judicial_register.py` → recreated against current canonical counts and current DP 748 controls.

### Superseded by later merged canonical work; do not transplant stale versions

10. `assets/data/counsel-filing-register-v1.json` → superseded/advanced by PR #1332 current filing lineage.
11. `assets/data/counsel-procurador-gap-register-v1.json` → superseded/advanced by PR #1332 current gap controls.
12. `assets/data/counsel-procurador-perimeter-register-v1.json` → superseded/advanced by PR #1332.
13. `assets/data/dp748-2026-canonical-interlink-control-v1.json` → superseded by `dp748-2026-appeal-reopening-control-v1.json`.
14. `assets/data/matter-identity-registry-v1.json` → current main is authoritative at 339/160/83/11/42/43; stale #1330 counts rejected.
15. `assets/data/matter-identity-registry-v1.professional-people.json` → stale #1330 Carlos-Llamas ID proposal rejected; current canonical `PD-SP-P-0062` retained.
16. `assets/data/procurador-master-register-v1.json` → current PR #1332 lineage is authoritative.
17. `en/matter-identity-registry/index.html` → current main already carries the later canonical denominator.
18. `es/registro-identidad-materia/index.html` → current main already carries the later canonical denominator.

### Preserved semantically by consolidation; separate micro-handover files intentionally not copied

19. `archive/LA_LAGUNA_JUDICIAL_REGISTER_BRANCH_READY_01SEP2026.md`
20. `archive/LA_LAGUNA_JUDICIAL_REGISTER_CLOSEOUT_RULE_01SEP2026.md`
21. `archive/LA_LAGUNA_JUDICIAL_REGISTER_CONTINUITY_POINTER_01SEP2026.md`
22. `archive/LA_LAGUNA_JUDICIAL_REGISTER_FINAL_BRANCH_NOTE_01SEP2026.md`
23. `archive/LA_LAGUNA_JUDICIAL_REGISTER_NO_FALSE_CLOSURE_01SEP2026.md`
24. `archive/LA_LAGUNA_JUDICIAL_REGISTER_NO_INFERENCE_RULE_01SEP2026.md`
25. `archive/LA_LAGUNA_JUDICIAL_REGISTER_ONE_SOURCE_ONE_ACT_RULE_01SEP2026.md`
26. `archive/LA_LAGUNA_JUDICIAL_REGISTER_PUBLICATION_BOUNDARY_01SEP2026.md`
27. `archive/LA_LAGUNA_JUDICIAL_REGISTER_RELEASE_MANIFEST_01SEP2026.md`
28. `archive/LA_LAGUNA_JUDICIAL_REGISTER_RESTART_SAFE_01SEP2026.md`
29. `archive/LA_LAGUNA_JUDICIAL_REGISTER_SOURCE_BOUNDARY_01SEP2026.md`
30. `archive/LA_LAGUNA_JUDICIAL_REGISTER_SOURCE_SEARCH_CLOSEOUT_01SEP2026.md`
31. `archive/LA_LAGUNA_JUDICIAL_REGISTER_VALIDATE_NOTES_01SEP2026.md`

Their substantive rules are consolidated here and in the gap-audit JSON: no false closure, no office-holder inference, one source/act/capacity boundary, public/private separation, finite-search limits, bilingual publication and restart instructions.

### Current canonical control retained

32. `assets/data/la-laguna-judicial-actors-canonical-interlink-control-v1.json` → already present on current main from PR #1326 and remains authoritative; no stale whole-file replacement is required.

## Open source gaps

- `LL-JUD-GAP-001` — exact judicial signatory of Auto 454/2026 dated 24-Mar-2026.
- `LL-JUD-GAP-002` — LAJ identity for the material PO 344/2013 acts.
- `LL-JUD-GAP-003` — downstream DP 748 appellate transfer/remittal/transmission, roll, organ and any appellate judge/panel/LAJ. Origin-court admission is verified.

## Restart rule

A successor thread must start from current `main`, then read:

1. `assets/data/matter-identity-registry-v1.json`
2. `assets/data/la-laguna-judicial-actors-canonical-interlink-control-v1.json`
3. `assets/data/la-laguna-judicial-actors-gap-closure-audit-v1.json`
4. `assets/data/dp748-2026-appeal-reopening-control-v1.json`
5. this closeout

Do not merge PR #1330 after this successor package is merged. Close #1330 as superseded with provenance. Do not close any LL-JUD gap without its primary-source closure trigger.
