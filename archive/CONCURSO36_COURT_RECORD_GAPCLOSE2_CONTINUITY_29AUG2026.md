# Concurso 36/2012 — court-record gap closure #2 continuity

**Date:** 29 August 2026  
**Branch:** `codex/concurso36-court-record-gapclose2-20260829`  
**Baseline:** current `main` after PR #1203.

## Purpose

Advance the deletion-safe autonomous court-record reconstruction by closing/narrowing high-priority 2018, 2021 and 2022 filing/decision/notification/implementation families. This is a reconstruction of the **located corpus**, not the certified court docket.

## New controlled state

- Base reconstruction + first appellate supplement: 20 nodes.
- Second supplement: 17 additional controlled/corroborated nodes.
- Expected rendered denominator after merge: **37 nodes**.
- No silent rewrite of `concurso36-complete-record-v1.json`.

## Material closures/narrowings

1. 11-Feb and 14-Feb-2022 LAJ testimony/finality front-end acts are controlled; Aweswell's 16-Feb reposición has exact LexNET receipt and principal hash.
2. CAM's 25-Jul opposition to direct revisions, the 26-Jul joining DIOR and the 28-Jul handoff of revisions to the judge are controlled. Final judge decision remains open.
3. The exact 29-Mar AP receipt currently controlled is Aweswell's, not LPB's. LPB Queja 375/2022 principal is controlled; exact AP receipt and exact signed 4-Jul Auto remain open.
4. 19-Jun-2018 LPB appeal is controlled and contains no located takeover/access/locks/keys/security allegation. It cannot prove court notice of the 7-Jun physical-control event.
5. 26-Jun-2018 Auto is controlled as a protective suspension of realisation of listed fincas, not possession/operation authority.
6. 24-Feb-2021 Auto is controlled as an adverse response to works/access/masa protective requests; it must not be described as silence.
7. LPB's 25-Feb/6-May-2021 nullity incident is separated as a mortgage/default-interest lane.
8. 8-Jul new-document service, separate AC-status Providencia and CAM's 21-Jul RICPE response are controlled.
9. The 29-Jul-2021 Aweswell RICPE paper is corrected to unfiled draft status absent a later filing receipt.
10. 2022 implementation is now primary-controlled for representative finca 8751: AC report -> 2-May court notification -> 6-May Registry note, all pointing to the 21-Feb-2022 deed/protocol 457. Finca-by-finca deed/testimonio/Registry and mortgage/credit reconciliation remain open.
11. Funded-exit drafts/correspondence remain distinct from an actual Concurso 36/2012 filing; no identifiable ONA/Stoneweg/Varia/Elaia LexNET receipt was located in this pass.
12. New orphan: AC quarterly-report registration 5367/2022 without principal report in the controlled forwarding package.

## Required boundaries

- `RESPONSE_NOT_LOCATED` is never automatically “ignored”.
- An adverse ruling is not automatically criminal judicial conduct.
- Protective/corrective counterweights stay visible.
- The four consequence tracks remain distinct: LPB masa activa; unidad productiva; Matkator/third-party extraconcursal harm; alleged overreach beyond LPB's estate.
- A Registry note/AC report proves what the instrument records; it does not by itself prove legal correctness of implementation.
- Non-production of the certified docket/index does not establish nonexistence, loss, suppression or alteration.

## Current P0 queue

See `assets/data/concurso36-court-record-reconstruction-gapclose2-20260829.json` -> `open_points_replace`. It is authoritative until superseded by a later versioned supplement.

## Fresh-thread restart

Read `CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md` first, then the base registry and both reconstruction supplements. Continue the P0 queue end-to-end and publish only through protected branch -> PR -> CI -> merge -> Pages -> manifest-state closeout.
