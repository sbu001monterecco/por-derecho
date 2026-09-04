# Reconciliation handoff — Control 21–22–24 canonical governance ↔ three-track reader layer

**Date:** 4 September 2026  
**Canonical governance:** `PD-C212224-001`  
**Reader-layer control:** `PD-THREE-TRACK-DIGITISATION-20260904-01`  
**Original reconciliation base:** `92b254ca03caf8f5ff4a418a9bfacb92b5bdd04f`  
**Concurrent Control-24 correction incorporated from:** `f4fda473b3259fd7654011b64952301ec42577b3`

## Why this handoff exists

A separate, concurrent publication merged the public-safe full digitisation of DP 1901/2026, DP 1956/2026 and Control 24 after the Control 21–22–24 continuity package had already been merged. A further concurrent Control-24 correction then strengthened `GC-HC-010` as one Reg. No. 24 filing record comprising the 18 June complaint and dependent 25 June supplement, while preserving the post-intake route as untraced and TSJC only as an expected/presumed, unverified route.

This reconciliation binds those developments rather than allowing either layer to overwrite the other.

## Reconciliation performed

The reader-layer dataset `data/three-track-full-digitisation-20260904.json` is explicitly subordinate to `assets/data/control-21-22-24-continuity-v1.json` for procedural identity and documentary bridge status.

The canonical graph reciprocally registers the three-track dataset as a `BOUND_READER_LAYER`, including its public ES/EN routes.

Two fail-closed validators divide responsibility:

- `scripts/validate_control_21_22_24_continuity.py` preserves the canonical Reg. No. 24 / Control 21 / Control 22 state, including filed-but-untraced status, one Reg. No. 24 record, dependent 25 June supplement, presumed/unverified TSJC route, and active Decanato/TSJC/CGPJ tracing.
- `scripts/validate_control_21_22_24_reader_binding.py` cross-validates the canonical graph against the three-track reader dataset and fails on bridge, identity, route or reader-layer drift.

Together they fail if:

- Control 21 → DP 1901/2026 is upgraded from `UNVERIFIED_CANDIDATE_BRIDGE` without controlled primary evidence;
- Control 22 → DP 1956/2026 is upgraded from `UNVERIFIED_CANDIDATE_BRIDGE`;
- Control 24 acquires an unverified NIG, court, official case number or formal destination;
- the 25 June Control-24 supplement is split from the same Reg. No. 24 record;
- the separate Control-21 object dated 25 June 2026 is collapsed into the Control-24 supplement;
- the expected/presumed TSJC route is promoted to verified allocation, origin or custody;
- public route mappings drift between the reader layer and canonical graph; or
- the reader-layer control ceases to be bound to `PD-C212224-001`.

The two specialist workflows mutually trigger across canonical and reader-layer change surfaces and run both validators where appropriate.

## Evidential state unchanged by this reconciliation

This reconciliation proves no previously open proceeding bridge. In particular:

1. Control 21 → DP 1901/2026 remains `UNVERIFIED_CANDIDATE_BRIDGE`.
2. Control 22 → DP 1956/2026 remains `UNVERIFIED_CANDIDATE_BRIDGE`.
3. Control 24 is documented as filed through the Decanato under Reg. No. 24, but its post-intake route/current formal destination remains `UNKNOWN` and untraced.
4. TSJ Canarias / TSJC remains only the expected/presumed criminal-competence route until primary reparto/receipt/docket/custody evidence proves more.
5. The 18 June Control-24 complaint and 25 June Control-24 supplement are one Reg. No. 24 filing record, with the supplement retained as a distinct provenance/event object.
6. `CONTROL-21-OBJECT-20260625` remains distinct from `CONTROL-24-AMPLIACION-20260625` with `NO_BRIDGE`.

## Successor rule

A successor thread working on DP 1901/2026, DP 1956/2026, Control 21, Control 22, Control 24, the June 2026 complaint corpus, or the three-track public pages must read both machine datasets and run:

```text
python3 scripts/validate_control_21_22_24_continuity.py
python3 scripts/validate_control_21_22_24_reader_binding.py
```

before publication.

Interlinking remains provenance/navigation and does not transfer knowledge, intent, causation, guilt, liability, procedural status or evidential weight between actors or routes.
