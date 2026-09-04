# Reconciliation handoff — Control 21–22–24 canonical governance ↔ three-track reader layer

**Date:** 4 September 2026  
**Canonical governance:** `PD-C212224-001`  
**Reader-layer control:** `PD-THREE-TRACK-DIGITISATION-20260904-01`  
**Reconciliation base:** `92b254ca03caf8f5ff4a418a9bfacb92b5bdd04f`

## Why this handoff exists

A separate, concurrent publication merged the public-safe full digitisation of DP 1901/2026, DP 1956/2026 and Control 24 after the Control 21–22–24 continuity package had already been merged. The later merge was a direct descendant of the continuity closeout, so it did not overwrite the governance package, but it introduced a second machine-readable reader-layer dataset that required an explicit binding back to the canonical bridge-state controls.

## Reconciliation performed

The reader-layer dataset `data/three-track-full-digitisation-20260904.json` is now explicitly subordinate to `assets/data/control-21-22-24-continuity-v1.json` for procedural identity and documentary bridge status.

The canonical graph reciprocally registers the three-track dataset as a `BOUND_READER_LAYER`, including its public ES/EN routes.

The continuity validator now loads and cross-validates both datasets. It fails if:

- Control 21 → DP 1901/2026 is upgraded from `UNVERIFIED_CANDIDATE_BRIDGE` without the canonical state being deliberately changed from controlled primary evidence;
- Control 22 → DP 1956/2026 is upgraded from `UNVERIFIED_CANDIDATE_BRIDGE`;
- Control 24 acquires an unverified NIG, court, official case number or formal destination;
- the potentially distinct Control-21 and Control-24 documents dated 25 June 2026 are collapsed;
- public route mappings drift between the reader layer and canonical graph;
- the reader-layer control ceases to be bound to `PD-C212224-001`.

The two specialist workflows now mutually trigger across the canonical and reader-layer change surfaces.

## Evidential state unchanged by this reconciliation

This reconciliation does **not** prove any previously open procedural bridge. In particular:

1. Control 21 → DP 1901/2026 remains `UNVERIFIED_CANDIDATE_BRIDGE`.
2. Control 22 → DP 1956/2026 remains `UNVERIFIED_CANDIDATE_BRIDGE`.
3. Control 24 formal criminal allocation/current destination remains `UNKNOWN`.
4. `CONTROL-21-OBJECT-20260625` and `CONTROL-24-AMPLIACION-20260625` remain distinct with `NO_BRIDGE` until a primary source proves identity.

## Successor rule

A successor thread working on DP 1901/2026, DP 1956/2026, Control 21, Control 22, Control 24, the June 2026 complaint corpus, or the three-track public pages must read both machine datasets and run `python3 scripts/validate_control_21_22_24_continuity.py` before publication.

Interlinking remains provenance/navigation and does not transfer knowledge, intent, causation, guilt, liability or procedural status between actors or routes.
