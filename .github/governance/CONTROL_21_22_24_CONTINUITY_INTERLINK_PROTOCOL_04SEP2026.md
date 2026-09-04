# Control 21–22–24 continuity and interlink protocol — 4 September 2026

**Control ID:** `PD-C212224-001`  
**Status:** MANDATORY CONTINUITY GOVERNANCE  
**Scope:** Concurso Ordinario 36/2012 and the June 2026 private-actor, Insolvency Administrator and judge-related filing perimeter.

## Purpose

This control prevents successor threads, editors, search/index rebuilds and public-page generation from fragmenting or silently collapsing the June 2026 filing perimeter. It supplements `AGENTS.md`, `CHATGPT_START_HERE.md`, the new-thread continuity gate and `ACTOR_EVENT_MULTITRACK_INTERLINKING_AND_PRECURSOR_PROTOCOL_01SEP2026.md`.

The durable unit is not a narrative triangle that implies common liability. It is a typed graph of distinct filing/proceeding objects connected to the common factual nucleus of Concurso 36/2012.

## Canonical controls

### CONTROL-21 — private-actor filing-control claim

- User-reported daily reference: `21`.
- User-reported filing date: `25 June 2026`.
- Candidate later proceeding: `DP 1901/2026` / `GC-CRI-008`.
- **Bridge status: `UNVERIFIED`.**
- The controlled repository currently verifies DP 1901/2026 itself, but this control does not yet possess a source-certified reparto/intake bridge proving that daily reference 21 became DP 1901/2026.
- Do not merge the Control-21 object with the judge-related 25 June amplification merely because the dates coincide.

### CONTROL-22 — Insolvency Administrator filing control

- Daily reference: `22`.
- Filing date: `18 June 2026`.
- Canonical intake object: `GC-REF-029`.
- Candidate later proceeding: `DP 1956/2026` / `GC-CRI-009`.
- **Bridge status: `UNVERIFIED`.**
- Daily reference 22 is a reception/intake locator, not a NIG, DP number, certified reparto or proof of assignment to DP 1956/2026.

### CONTROL-24 — judge-related complaint/notitia

- Daily reference: `24`.
- Filing date: `18 June 2026`.
- Canonical object: `GC-HC-010`.
- Materially connected judge-related amplification: `25 June 2026`.
- **Formal criminal destination: `UNKNOWN`.**
- Daily reference 24 is not a NIG, DP number, certified reparto, admission, dismissal, archive or merits outcome.
- `DI 169/2026` / `GC-GOV-019`, its appeal/review route and `DIP 2/2026` are related but separate procedural/institutional routes unless a primary source establishes a stronger relation.

## Mandatory bridge rule

Every edge that could collapse two identifiers into one procedural identity must carry an explicit bridge state:

- `PROVEN_DOCUMENTARY_BRIDGE`
- `MATERIALLY_LINKED_DISTINCT_OBJECTS`
- `RELATED_SEPARATE_ROUTE`
- `UNVERIFIED_CANDIDATE_BRIDGE`
- `NO_BRIDGE`

A candidate bridge may be upgraded only when the controlled record identifies the source that proves allocation, assignment, joinder, appeal lineage or other asserted procedural identity. Shared dates, subject matter, actor overlap, receiving office or narrative sequence are insufficient by themselves.

## Bidirectional interlink rule

Material supported relationships must be represented in both navigation directions or by one machine-readable edge explicitly marked `bidirectional: true`. Every successor implementation must test:

`source/evidence ↔ filing control ↔ proceeding/authority ↔ actor/capacity ↔ event ↔ Concurso 36/2012 ↔ reciprocal public route`

Interlinking never transfers knowledge, intent, causation, guilt, liability, procedural status or evidential weight between nodes.

## Two-documents-on-25-June safeguard

Until source reconciliation proves otherwise, the repository must allow for two distinct 25 June 2026 objects:

1. the user-reported Control-21/private-actor filing object; and
2. the controlled judge-related amplification materially linked to Control 24.

They must not share one canonical evidence/document ID merely because they share a date.

## Search and discoverability rule

The canonical machine state must remain discoverable by at least these aliases and references: `Control 21`, `Control 22`, `Control 24`, `daily 21`, `daily 22`, `daily 24`, `DP 1901/2026`, `DP 1956/2026`, `GC-CRI-008`, `GC-CRI-009`, `GC-REF-029`, `GC-HC-010`, `DI 169/2026`, `CGPJ 169/2026`, `DIP 2/2026`, `18 June 2026`, `25 June 2026`, and `Concurso 36/2012`.

Default-branch code-search failure is not proof that a public page or source object does not exist. Successor threads must use canonical files/directories and live-route verification as needed.

## Successor-thread bootstrap

For work touching this perimeter:

1. fetch current remote `main`;
2. read `AGENTS.md`, `CHATGPT_START_HERE.md`, the new-thread continuity gate and this protocol;
3. read `assets/data/control-21-22-24-continuity-v1.json`;
4. inspect the latest relevant handoff under `archive/handoffs/`;
5. re-query controlled source systems for any unresolved documentary bridge instead of reconstructing it from chat memory;
6. update canonical machine state before strengthening public narrative;
7. run `python3 scripts/validate_control_21_22_24_continuity.py` and the repository-wide preservation/publication validators applicable to the actual changed surface.

## Publication boundary

This governance record is public-safe. It records procedural identity controls and project-side allegations/claims only at the level necessary for continuity. It does not establish criminality, guilt, collusion, capture, neutralisation, prevarication, prosecutorial acceptance, judicial allocation or liability. Any stronger proposition requires its own source-controlled evidential state and contrary/limiting record.

## Current finite gaps

1. Source-certified Control-21 → DP 1901/2026 bridge.
2. Source-certified Control-22 → DP 1956/2026 bridge.
3. Certified reparto/current destination for Control 24.
4. Source-level reconciliation of the two potentially distinct 25 June 2026 documents.
5. Canonical registration of stamped source files, transcriptions/OCR derivatives and hashes wherever not already source-controlled.
