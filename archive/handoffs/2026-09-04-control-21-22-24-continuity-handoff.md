# Workspace handoff — Control 21–22–24 continuity governance

**Workspace ID:** `PD-WS-20260904-0001`  
**Date:** 4 September 2026  
**Scope state:** `RELATED_CONTINUITY_ACTIVE`  
**Canonical machine state:** `assets/data/control-21-22-24-continuity-v1.json`  
**Governance:** `.github/governance/CONTROL_21_22_24_CONTINUITY_INTERLINK_PROTOCOL_04SEP2026.md`

## Purpose

Preserve the June 2026 filing/proceeding perimeter as a typed, interlinked and successor-readable graph without collapsing intake references, criminal proceedings, judicial-governance routes or prosecutorial routes into one legal file.

## Current controlled state

- `GC-CRI-008` verifies DP 1901/2026 and its current controlled procedural status. The daily-reference-21 → DP 1901/2026 bridge remains unverified in this workspace.
- `GC-REF-029` verifies daily intake/reference 22, 18 June 2026, concerning the Insolvency Administrator. It is not itself a judicial proceeding number. The Control-22 → DP 1956/2026 bridge remains unverified.
- `GC-CRI-009` verifies DP 1956/2026 as a separate criminal route with provisional dismissal recorded on 21 July 2026; the controlled page does not establish the daily-reference-22 reparto bridge.
- `GC-HC-010` / Control 24 records the judge-related complaint/notitia filed through the Decanato on 18 June 2026 under daily registration no. 24 and its dependent 25 June 2026 supplement as one continuous filing record.
- The filing fact is usable as a filing/chronology/provenance fact. The post-intake route remains untraced.
- `TSJ Canarias / TSJC` is preserved only as the expected/presumed competence route, not as verified reparto, receipt, assigned organ or current custodian.
- The reporting party is asking the Decanato / Registro y Reparto, TSJC and CGPJ to locate and confirm the post-intake route, present location/custody and procedural treatment.
- `GC-GOV-019` / the 169/2026 governance-review reference and `Alzada 286/2026` remain separate controls/routes. The CGPJ 169/2026 link records later reporting and current trace activity, not proof of the original filing's allocation or merits treatment.

## Mandatory non-collapse rules

1. Do not state Control 21 became DP 1901/2026 without a source-certified intake/reparto bridge.
2. Do not state Control 22 became DP 1956/2026 without a source-certified intake/reparto bridge.
3. Do not turn daily reference 24 into a NIG, DP, certified reparto, admission, dismissal, archive or merits outcome.
4. Preserve Control 24 as one Reg. No. 24 filing record containing the 18 June original and 25 June dependent supplement; retain separate document provenance without creating a second proceeding.
5. Preserve both Control 24 status propositions: **filed through the Decanato** and **post-intake route still untraced**.
6. Preserve `TSJ Canarias / TSJC` only as the expected/presumed route until primary proof establishes reparto/receipt/docket/custody.
7. Preserve the active trace inquiry to Decanato + TSJC + CGPJ.
8. Interlinking is navigation/provenance unless the edge itself carries a stronger documented bridge state. It never transfers criminal responsibility, knowledge, intent, causation or procedural status.

## Recovery / successor boot sequence

A successor thread should:

1. fetch current remote `main` and treat it as source of truth;
2. read `AGENTS.md`, `CHATGPT_START_HERE.md`, `.github/governance/NEW_THREAD_SCOPE_AND_CONTINUITY_GATE_02SEP2026.md`, `.github/governance/ACTOR_EVENT_MULTITRACK_INTERLINKING_AND_PRECURSOR_PROTOCOL_01SEP2026.md` and the Control 21–22–24 protocol;
3. load `assets/data/control-21-22-24-continuity-v1.json` before reasoning about the three controls;
4. verify current live/source pages for `GC-CRI-008`, `GC-CRI-009`, `GC-REF-029` and `GC-HC-010` if public presentation is in scope;
5. for Control 24, begin from filed + untraced + presumed TSJC route only + active Decanato/TSJC/CGPJ trace inquiry;
6. search controlled source systems specifically for unresolved documentary bridges rather than repeating broad scans;
7. update machine state first if a bridge is proved/refuted;
8. propagate the result to all reciprocal pages/registers and rerun specialist plus repository-wide validators.

## Publication history and current release

- Prior continuity-governance release: PR `#1418`, merge SHA `005ca9b51eb0a4cff6ce9545d9cd4561a30450ab`; specialist continuity validation succeeded.
- Three-track full-digitisation release subsequently landed on `main` and independently records the Control 24 79-page signed package, 31-page principal complaint, 10-page dependent supplement, Reg. 24 and unknown formal allocation/status.
- Current reader-facing/canonical correction is PR `#1422` — **Unify GC-HC-010 under Reg. No. 24 and harden continuity governance**. It is prepared on current main and mergeable; final merge SHA and live deployment verification are recorded after merge.
- PR #1422 includes bilingual GC-HC-010 pages, machine-state correction, strengthened continuity protocol/validator, correction control, handoff update, and deterministic post-merge master-register migration.

## Finite open gaps

- Prove/refute Control 21 → DP 1901/2026 from stamped intake/reparto material.
- Prove/refute Control 22 → DP 1956/2026 from certified reparto or equivalent primary evidence.
- Locate certified Decanato reparto/outgoing route and current destination for Control 24.
- Obtain TSJC confirmation/refutation of receipt, docketing, transfer or custody.
- Obtain Decanato/TSJC/CGPJ trace responses identifying location/treatment of Reg. No. 24.
- Reconcile electronic joinder/remittal metadata for the 25 June Control 24 supplement.
- Locate/canonize missing stamped PDFs, transcriptions/OCR derivatives, hashes and evidence IDs where not already present in the controlled corpus.

## Authority boundary

This handoff authorises nothing beyond repository continuity and public-safe publication. No external filing, email, portal submission, deletion, force push or history rewrite follows from it.