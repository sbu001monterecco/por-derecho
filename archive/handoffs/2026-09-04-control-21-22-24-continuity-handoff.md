# Workspace handoff — Control 21–22–24 continuity governance

**Workspace ID:** `PD-WS-20260904-0001`  
**Date:** 4 September 2026  
**Scope state:** `RELATED_CONTINUITY_ACTIVE`  
**Publication state:** `PUBLISHED_LIVE_VERIFIED_CONTINUITY_COMPLETE`  
**Canonical machine state:** `assets/data/control-21-22-24-continuity-v1.json`  
**Reader layer:** `data/three-track-full-digitisation-20260904.json`  
**Governance:** `.github/governance/CONTROL_21_22_24_CONTINUITY_INTERLINK_PROTOCOL_04SEP2026.md`

## Purpose

Preserve the June 2026 filing/proceeding perimeter as a typed, interlinked and successor-readable graph without collapsing intake references, criminal proceedings, judicial-governance routes or prosecutorial routes into one legal file.

## Current controlled state

- `GC-CRI-008` verifies DP 1901/2026 and its current controlled procedural status. The daily-reference-21 → DP 1901/2026 bridge remains unverified.
- `GC-REF-029` verifies daily intake/reference 22, 18 June 2026, concerning the Insolvency Administrator. It is not itself a judicial proceeding number. The Control-22 → DP 1956/2026 bridge remains unverified.
- `GC-CRI-009` verifies DP 1956/2026 as a separate criminal route with provisional dismissal recorded on 21 July 2026; the controlled record does not establish the daily-reference-22 reparto bridge.
- `GC-HC-010` / Control 24 records the judge-related complaint/notitia filed through the Decanato on 18 June 2026 under Reg. No. 24 and its dependent 25 June 2026 supplement as one continuous filing record.
- The filing fact is usable as a filing/chronology/provenance fact. The post-intake route remains untraced.
- `TSJ Canarias / TSJC` is preserved only as the expected/presumed competence route, not as verified reparto, receipt, assigned organ or current custodian.
- The reporting party is asking the Decanato / Registro y Reparto, TSJC and CGPJ to locate and confirm the post-intake route, present location/custody and procedural treatment.
- `GC-GOV-019` / the 169/2026 governance-review reference and `Alzada 286/2026` remain separate controls/routes. The CGPJ 169/2026 link records later reporting and current trace activity, not proof of the original filing's allocation or merits treatment.

## Canonical ↔ reader-layer binding

`PD-C212224-001` is the procedural-identity and bridge-state authority. `PD-THREE-TRACK-DIGITISATION-20260904-01` is its bound reader layer. The reader layer may add public-safe full-text digest, source identity, narrative context and reciprocal navigation, but it cannot upgrade an unverified bridge or weaken the Reg. No. 24 safeguards.

The binding is fail-closed through:

```text
python3 scripts/validate_control_21_22_24_continuity.py
python3 scripts/validate_control_21_22_24_reader_binding.py
```

Both specialist workflows trigger across canonical and reader-layer change surfaces.

## Mandatory non-collapse rules

1. Do not state Control 21 became DP 1901/2026 without a source-certified intake/reparto bridge.
2. Do not state Control 22 became DP 1956/2026 without a source-certified intake/reparto bridge.
3. Do not turn Reg. No. 24 into a NIG, DP, certified reparto, admission, dismissal, archive or merits outcome.
4. Preserve Control 24 as one Reg. No. 24 filing record containing the 18 June original and 25 June dependent supplement; retain separate document provenance without creating a second proceeding.
5. Preserve both Control 24 status propositions: **filed through the Decanato** and **post-intake route still untraced**.
6. Preserve `TSJ Canarias / TSJC` only as the expected/presumed route until primary proof establishes reparto/receipt/docket/custody.
7. Preserve the active trace inquiry to Decanato + TSJC + CGPJ.
8. Preserve `CONTROL-21-OBJECT-20260625` and `CONTROL-24-AMPLIACION-20260625` as distinct document objects with `NO_BRIDGE` unless primary evidence proves otherwise.
9. Interlinking is navigation/provenance unless an edge itself carries a stronger documented bridge state. It never transfers criminal responsibility, knowledge, intent, causation, procedural status or evidential weight.

## Publication and deployment checkpoint

The continuity and reader-layer reconciliation is fully published.

- PR `#1420` — **Bind three-track digitisation to Control 21–22–24 continuity governance** — merged.
- Merge/main SHA: `667868ee71a98105ad7766d9afb37a5bd10fe921`.
- Post-merge continuity workflow: run `33829334065` — **SUCCESS**; canonical continuity and canonical↔reader binding both passed.
- Post-merge three-track workflow: run `33829334206` — **SUCCESS**; source identity, pagination, procedural separation, canonical continuity, reader binding, visual narration and public-safety checks passed.
- GitHub Pages deployment: run `33829332514` (#1465) on the same SHA — **SUCCESS**.
- Fresh remote-main readback after deployment: `667868ee71a98105ad7766d9afb37a5bd10fe921`.
- Public Control-24/Fiscalía route was externally checked after deployment and still states the required boundary: Reg. No. 24 is a filing locator rather than a NIG/DP/reparto; the 25 June supplement is linked to the same filing reference; later reparto/TSJC destination remains unverified.

### Bound public route set

```text
/por-derecho/es/dp-1901-2026/
/por-derecho/en/dp-1901-2026/
/por-derecho/es/dp-1956-2026/
/por-derecho/en/dp-1956-2026/
/por-derecho/es/control-24-denuncia-juez-concurso-36-2012/
/por-derecho/en/control-24-insolvency-judge-complaint-36-2012/
/por-derecho/es/procedimientos/gc-hc-010/
/por-derecho/en/proceedings/gc-hc-010/
/por-derecho/es/fiscalia-dip-2-2026/
/por-derecho/en/fiscalia-dip-2-2026/
```

## Repository-wide debt outside this release

The repository is not represented as globally validator-clean. Unrelated inherited/concurrent debt remains visible, including:

- workflow-hardening policy failures in other workflows;
- the public-bidder anonymisation/preservation gate issue;
- stale DP 3205/2014 Arrecife registry metadata/validation debt.

These were not introduced by the Control 21–22–24 canonical↔reader binding and do not alter its successful specialist validation or Pages deployment. They should be repaired in separately scoped changes rather than by weakening this continuity release.

## Recovery / successor boot sequence

A successor thread should:

1. fetch current remote `main` and treat it as source of truth;
2. read `AGENTS.md`, `CHATGPT_START_HERE.md`, `.github/governance/NEW_THREAD_SCOPE_AND_CONTINUITY_GATE_02SEP2026.md`, `.github/governance/ACTOR_EVENT_MULTITRACK_INTERLINKING_AND_PRECURSOR_PROTOCOL_01SEP2026.md` and the Control 21–22–24 protocol;
3. load `assets/data/control-21-22-24-continuity-v1.json` and `data/three-track-full-digitisation-20260904.json` before reasoning about these tracks;
4. run both specialist validators before publication;
5. verify current live/source pages for `GC-CRI-008`, `GC-CRI-009`, `GC-REF-029` and `GC-HC-010` if public presentation is in scope;
6. for Control 24, begin from filed + untraced + presumed TSJC route only + active Decanato/TSJC/CGPJ trace inquiry;
7. search controlled source systems specifically for unresolved documentary bridges rather than repeating broad scans;
8. update machine state first if a bridge is proved/refuted, then propagate to all reciprocal pages/registers and rerun specialist plus relevant repository-wide validators.

## Finite open evidential gaps

- Prove/refute Control 21 → DP 1901/2026 from stamped intake/reparto material.
- Prove/refute Control 22 → DP 1956/2026 from certified reparto or equivalent primary evidence.
- Locate certified Decanato reparto/outgoing route and current destination for Control 24.
- Obtain TSJC confirmation/refutation of receipt, docketing, transfer or custody.
- Obtain Decanato/TSJC/CGPJ trace responses identifying location/treatment of Reg. No. 24.
- Reconcile electronic joinder/remittal metadata for the 25 June Control 24 supplement.
- Locate/canonize missing stamped PDFs, transcriptions/OCR derivatives, hashes and evidence IDs where not already present in the controlled corpus.

## Authority boundary

This handoff authorises nothing beyond repository continuity and public-safe publication. No external filing, email, portal submission, deletion, force push or history rewrite follows from it.
