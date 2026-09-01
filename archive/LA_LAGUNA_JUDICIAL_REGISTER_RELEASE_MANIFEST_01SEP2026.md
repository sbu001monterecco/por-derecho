# La Laguna judicial `^` register — release manifest

Date: 1 September 2026  
Branch: `fix/la-laguna-judicial-gap-publication-20260901`

## Release purpose

Publish the source-identified La Laguna judicial actor denominator created by PR #1326 as a bilingual reader-facing register; preserve exact act/date/capacity boundaries; transplant the non-duplicative DP 748/2026 counsel/procurador/procedural lineage from stale PR #1324; and convert the three unresolved identity questions into explicit finite evidence gaps with closure triggers rather than guessed identities.

## Canonical closure achieved by this release

- All judges/magistrates and LAJs identifiable from the presently recovered primary-source La Laguna corpus retain immutable CAEPR IDs.
- Each is bound to proceeding → court organ → act/date → capacity.
- Arrecife/Yaiza cooperation actors remain auxiliary and are not reclassified as La Laguna office-holders.
- Bilingual public aggregate routes are created for the judicial perimeter.
- Root identity count is reconciled to 331 after promotion of reserved DP 748 counsel ID `PD-SP-P-0146`.
- Static ES/EN identity-register denominators are reconciled to the canonical JSON.
- Two DP 748 counsel filings are promoted with public-safe opaque source references.
- Adriana Hernández Díaz's DP 748 procurador pairing is source-verified without transferring that pairing to ETJ 163/2020.
- PR #1324's unique DP 748 procedural and professional-lineage content is preserved without importing its stale duplicate institution shard.

## Evidentiary gaps intentionally left open

- `LL-JUD-GAP-001` — exact judicial signer of Auto 454/2026 dated 24-Mar-2026.
- `LL-JUD-GAP-002` — LAJ identity for PO 344/2013.
- `LL-JUD-GAP-003` — verified appellate organ/roll and any judges/LAJ for the DP 748 subsidiary appeal lane.

A completed finite search is not proof that a missing source does not exist. These gaps close only on primary evidence sufficient for the exact attribution.

## Public routes

- ES: `/es/registro-judicial-la-laguna/`
- EN: `/en/la-laguna-judicial-register/`
- ES master identity register: `/es/registro-identidad-materia/`
- EN master identity register: `/en/matter-identity-registry/`

## Validation

Path-scoped validator: `scripts/validate_la_laguna_judicial_register.py` via `.github/workflows/validate-la-laguna-judicial-register.yml`.

## Boundary

This release establishes identity, procedural capacity, source linkage and explicit evidence gaps. It does not establish wrongdoing, intent, liability, agreement with a party or merits treatment by any judicial actor, professional or institution.
