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
- Do not merge the Control-21 object with the judge-related 25 June supplement merely because the dates coincide.

### CONTROL-22 — Insolvency Administrator filing control

- Daily reference: `22`.
- Filing date: `18 June 2026`.
- Canonical intake object: `GC-REF-029`.
- Candidate later proceeding: `DP 1956/2026` / `GC-CRI-009`.
- **Bridge status: `UNVERIFIED`.**
- Daily reference 22 is a reception/intake locator, not a NIG, DP number, certified reparto or proof of assignment to DP 1956/2026.

### CONTROL-24 — Reg. No. 24 / judge-related complaint and dependent supplement

- Daily registration/reference: `24`.
- Original filing date: `18 June 2026`.
- Canonical repository object: `GC-HC-010`.
- Dependent supplement/ampliación: `25 June 2026`.
- **Canonical identity: one Reg. No. 24 filing record, two dated filing events.**
- The 25 June supplement remains a distinct document/event object for provenance, hashing and evidential citation, but it is **not an autonomous complaint or proceeding**. Document identity must not be confused with procedural-record identity.
- **Formal criminal destination/current custodian: `UNKNOWN`.**
- Daily registration 24 is a reception locator, not a NIG, DP number, certified reparto, admission, dismissal, archive or merits outcome.
- The combined Reg. No. 24 matter was later reported to the CGPJ within the `169/2026` control identified as `GC-GOV-019`. That later reporting does not prove the original Decanato filing's allocation, acceptance, joinder, merits treatment or outcome.
- `GC-GOV-019` / 169/2026 and `Alzada 286/2026` remain distinct CGPJ controls/routes unless a primary source establishes a stronger procedural relation. They must not be silently merged.
- `DIP 2/2026` and other prosecutorial routes are related but separate unless a primary source establishes a stronger procedural relation.

## Mandatory bridge rule

Every edge that could collapse two identifiers into one procedural identity must carry an explicit bridge state:

- `PROVEN_DOCUMENTARY_BRIDGE`
- `PROVEN_SAME_RECORD_DEPENDENT_SUPPLEMENT`
- `MATERIALLY_LINKED_DISTINCT_OBJECTS`
- `RELATED_SEPARATE_ROUTE`
- `UNVERIFIED_CANDIDATE_BRIDGE`
- `NO_BRIDGE`

`PROVEN_SAME_RECORD_DEPENDENT_SUPPLEMENT` means that a later document/event is canonically treated as a dependent filing within the same reception/control record while retaining its own document-level provenance. It does not imply certified electronic joinder, judicial allocation, admission or merits treatment.

A candidate bridge may otherwise be upgraded only when the controlled record identifies the source that proves allocation, assignment, joinder, appeal lineage or other asserted procedural identity. Shared dates, subject matter, actor overlap, receiving office or narrative sequence are insufficient by themselves.

## Bidirectional interlink rule

Material supported relationships must be represented in both navigation directions or by one machine-readable edge explicitly marked `bidirectional: true`. Every successor implementation must test:

`source/evidence ↔ filing control ↔ proceeding/authority ↔ actor/capacity ↔ event ↔ Concurso 36/2012 ↔ reciprocal public route`

Interlinking never transfers knowledge, intent, causation, guilt, liability, procedural status or evidential weight between nodes.

## Two-documents-on-25-June safeguard

The 25 June date contains at least two distinct document objects in this controlled perimeter:

1. the user-reported Control-21/private-actor filing object; and
2. the judge-related **Reg. No. 24 dependent supplement**, which belongs to the same `CONTROL-24 / GC-HC-010` filing record as the 18 June complaint.

Those two 25 June document objects must not share one canonical evidence/document ID merely because they share a date. At the same time, the Control-24 supplement must never be promoted into a second judge-related proceeding: **separate document object, same Reg. No. 24 procedural record**.

## Actor/event/action interconnection rule

Control 24 must be connected to the relevant actor, capacity, event and legally distinct action layers without collapsing them. Public and machine-readable derivatives should preserve, where supported:

- the complainant's attribution to **Alberto López Villarrubia**, then Magistrate-Judge in the Concurso 36/2012 context;
- the underlying `Concurso 36/2012` judicial/insolvency record;
- Control 22 / Insolvency Administrator material and any later DP 1956/2026 bridge only at its verified evidential strength;
- DP 1901/2026 and private-actor/CAM material only as a distinct route with typed cross-evidence;
- `GC-GOV-019` / CGPJ 169/2026 as a later reporting/governance route;
- `Alzada 286/2026` as a separate review control;
- Fiscalía/DIP routes, insolvency appeals, removal/fees, active-estate and funded-exit material only through typed contextual or documentary relationships.

For allegations, the preferred chain is:

`actor → capacity → knowledge/source → act/omission → claimed effect → lawful alternative explanation → evidence needed to confirm or exclude`.

Related does not mean consolidated; shared evidence does not mean shared responsibility; and a complaint attribution is not an adjudicated finding.

## Search and discoverability rule

The canonical machine state must remain discoverable by at least these aliases and references: `Control 21`, `Control 22`, `Control 24`, `Reg. No. 24`, `Registro n.º 24`, `daily 21`, `daily 22`, `daily 24`, `DP 1901/2026`, `DP 1956/2026`, `GC-CRI-008`, `GC-CRI-009`, `GC-REF-029`, `GC-HC-010`, `DI 169/2026`, `CGPJ 169/2026`, `Alzada 286/2026`, `DIP 2/2026`, `18 June 2026`, `25 June 2026`, `18 junio 2026`, `25 junio 2026` and `Concurso 36/2012`.

Default-branch code-search failure is not proof that a public page or source object does not exist. Successor threads must use canonical files/directories and live-route verification as needed.

## Successor-thread bootstrap

For work touching this perimeter:

1. fetch current remote `main`;
2. read `AGENTS.md`, `CHATGPT_START_HERE.md`, the new-thread continuity gate and this protocol;
3. read `assets/data/control-21-22-24-continuity-v1.json`;
4. inspect the latest relevant handoff under `archive/handoffs/` and the latest dated GC-HC-010 correction control;
5. resolve `GC-HC-010` as Reg. No. 24 with both the 18 June original and 25 June dependent supplement before reasoning about later routes;
6. re-query controlled source systems for unresolved documentary bridges instead of reconstructing them from chat memory;
7. update canonical machine state before strengthening public narrative;
8. propagate corrections to all reciprocal EN/ES pages, master-register/search/graph projections and continuity controls; and
9. run `python3 scripts/validate_control_21_22_24_continuity.py` plus the repository-wide preservation/publication validators applicable to the actual changed surface.

## Publication boundary

This governance record is public-safe. It records procedural identity controls and project-side allegations/claims only at the level necessary for continuity. It does not establish criminality, guilt, collusion, capture, neutralisation, prevarication, prosecutorial acceptance, judicial allocation or liability. Any stronger proposition requires its own source-controlled evidential state and contrary/limiting record.

## Current finite gaps

1. Source-certified Control-21 → DP 1901/2026 bridge.
2. Source-certified Control-22 → DP 1956/2026 bridge.
3. Certified reparto/current destination/current custodian for Reg. No. 24 / Control 24.
4. Certified electronic metadata for the 25 June Reg. No. 24 supplement, including joinder/remittal treatment.
5. Exact CGPJ 169/2026 document nomenclature, annex reference and treatment.
6. Canonical registration of stamped source files, transcriptions/OCR derivatives and hashes wherever not already source-controlled.
