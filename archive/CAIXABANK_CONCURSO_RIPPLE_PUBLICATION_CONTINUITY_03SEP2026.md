# CaixaBank ↔ Concurso 36/2012 ripple publication continuity — 3 September 2026

Workspace: `PD-WS-20260902-0001`

## Controlling repository state

- Predecessor audit anchor: `02a09a73b9d9548e1dcd9dabae65c86c6da58f8d` — Merge PR #1401, CaixaBank ADR and settlement invitation.
- Current `main` incorporated before continuation: `64785292f8230e46bb4372de0902faadb8a75fb9` — Merge PR #1402, ONA funded-exit interference evidence chain.
- Predecessor ripple branch commits preserved rather than recreated:
  - `673d941b9aee8661a8051416a6c6b9cf384cf41d` — reusable interconnectivity overlay.
  - `064a26475b7ea505659305a045cceb8dacbbfdac` — ES unitary ripple dossier.
  - `722c21e28b5d93112f6e8651d23b664afee5d7a1` — EN unitary ripple dossier.
- Integration merge commit: `a5eb4d6cbb16af72f8f8d2b52801160cbdbf822e` has current `main` and the predecessor ripple tip as parents. No force update was used.

## Public architecture added

Canonical new routes:

- `/es/caixabank-concurso-efecto-domino/`
- `/en/caixabank-insolvency-ripple/`

Reusable public overlays:

- `assets/caixabank-concurso-ripple-interconnect-20260903.js`
- `assets/caixabank-concurso-caret-overlay-20260903.js`

The ripple overlay is applied only to an explicit ES/EN route allow-list covering:

- CaixaBank Valencia claim;
- LPB / Concurso 36/2012 insolvency hub;
- lender/creditor-of-record hub;
- sale/lender convergence / possession-credit chain;
- recovery and restitution objectives;
- administrator-removal RPL 3304/3319 dossier;
- administrator overview and removal/fees pages.

The overlays are loaded through the already universal `borja-separation-rpl3304-inbound-20260902.js` loader path. This avoids rewriting the inherited `site.js` loader contract or removing its preservation markers. Each asset exits immediately outside its explicit governed allow-list.

## Primary court notice preserved

No court-notice image was regenerated or replaced.

The existing public child route remains the primary source:

- `/es/reclamacion-caixabank-valencia/senalamiento-28-enero-2027/`

Existing public images remain:

- `assets/evidence/caixabank-valencia-1859-2023-diligencia-06nov2025-p1-publica.jpg`
- `assets/evidence/caixabank-valencia-1859-2023-diligencia-06nov2025-p2-publica.jpg`

The reusable ripple overlay adds a visible thumbnail/card on both ES and EN CaixaBank main dossiers and links to the two-page redacted public notice. The notice child page now loads the route-scoped caret layer directly so its source-locked parties, proceeding and court organ carry the same identity control.

## Canonical procedural state carried forward

- Aweswell Limited v CAIXABANK, S.A.
- Procedimiento Ordinario 1859/2023-9.
- Juzgado de Primera Instancia nº 27 de Valencia.
- NIG 46250-42-1-2023-0049579.
- Signed diligence dated 6 November 2025.
- Live hearing: 28 January 2027 at 10:00.
- Pending and contested; no merits judgment is asserted by this publication.

Administrator-removal tracks remain distinct:

- RPL 3319/2025 — Aweswell appeal.
- RPL 3304/2025 — LPB independent appeal.
- Controlled repository state: 3319 was procedurally absorbed into the live consolidated 3304 vehicle; this is not represented as a merits loss by Aweswell.

## Controlling legal/evidential warnings

Every public arrow means **potential consequential review — not automatic invalidity**.

The publication does not state that any CaixaBank result automatically:

- annuls Concurso 36/2012;
- reverses adjudications or assignments;
- transfers liability between CaixaBank, SAREB, PH122, CAM, the insolvency administrator or the court;
- proves misconduct, knowledge, intent, concert or collusion.

The pages instead require actor/date/capacity/source analysis, accounting reconciliation and any competent further judicial, insolvency, restitution, reopening or liability mechanism required by the eventual facts and result.

The 12 June 2018 Stoneweg/Varia proposal is described as a **Conditional Binding Offer**, not completed or disbursed financing.

## `^` / CAEPR / CARET control

This publication uses the canonical immutable PD-SP identity layer rather than creating display-only identities.

Source-locked objects used by the ripple include:

- `PD-SP-P-0010^` — Francisco de Borja Rodríguez-Batllori Laffitte;
- `PD-SP-O-0001^` — Aweswell Limited;
- `PD-SP-O-0002^` — Luchy Playa Blanca, S.L.U.;
- `PD-SP-O-0007^` — Construcciones Acosta Matos, S.A.;
- `PD-SP-O-0021^` — Promontoria Holding 122 B.V.;
- `PD-SP-O-0029^` — Bankia, S.A.;
- `PD-SP-O-0030^` — SAREB;
- `PD-SP-O-0032^` — CaixaBank, S.A.;
- `PD-SP-R-0001^` — Concurso 36/2012;
- `PD-SP-R-0008^` — CaixaBank Valencia / ORD 1859/2023-9 canonical proceeding object;
- `PD-SP-R-0011^` — RPL 3304/2025;
- `PD-SP-R-0012^` — RPL 3319/2025;
- `PD-SP-I-0049^` — Juzgado de Primera Instancia nº 27 de Valencia, source-locked to the organ name printed on the signed 6-Nov-2025 diligence.

`PD-SP-I-0049^` has an explicit date boundary: the 6-Nov-2025 court-organ name is confirmed; no later Tribunal-de-Instancia/successor label and no individual judge or LAJ is inferred from that identity.

The combined 3304+3319 family reference is not given a competing caret. Where a public shorthand says `RPL 3304/3319`, the caret layer renders the two exact proceedings separately because the aggregate `PD-SP-R-0013` is a non-caret family reference.

No name is completed from office succession, family/company relationship or contextual proximity. Exact-entity perimeter labels whose legal person remains open are deliberately not promoted to `^`; their existing source-gap status remains controlling. Identity resolves identity only and never transfers knowledge, intent, control, merits or responsibility.

## Specific route correction made during reintegration

The predecessor overlay/EN hub used `/en/creditor-sale-convergence/`. Repository hreflang establishes the canonical EN route as `/en/sale-lender-convergence/`. Both the overlay and EN ripple hub were corrected before publication.

## Public/private settlement boundary

Public surfaces retain only the already-authorized statement that Aweswell is prepared to explore a serious, confidential and commercial pre-trial resolution with CaixaBank before January 2027, without prejudice to pending litigation.

No private settlement values, concessions, negotiation strategy, David Espejo outreach, private CaixaBank contacts, expert correspondence or unapproved intermediary strategy are published by this workstream.

## Remaining source gaps / questions not converted into fact

- Full 2011–2012 banking/account reconciliation remains a substantive reconstruction task.
- EH 90/2012 still requires document-by-document completion where sources remain missing.
- Any future CaixaBank outcome will require outcome-specific analysis of what amounts/rights are affected and which procedural mechanism is legally available.
- Consequences for transferred credit, estate accounts, possession/title economics, adjudication or administrator liability remain conditional on the actual source and competent determination.
- Historical labels such as Caja Insular/La Caja/BFA remain economic-history labels unless and until their exact legal/corporate identity object is separately source-locked; this publication does not manufacture new carets for them.

These are retained as evidential/legal gaps, not filled by inference.

## Validation / publication fields

- PR: `#1404`
- publication instruction: `PUBLISH NOW` — 3 September 2026
- mergeability: confirmed `true` before the final caret pass
- inherited validator state: current `main` at `64785292...` already carried the same bidder-anonymisation and audience-source/route failures later observed on PR #1404; those repository-wide inherited failures are not represented as newly caused by this workstream
- new identity rule: do not merge if the final caret changes introduce a new identity-specific failure; inherited unrelated failures do not erase the user's express publication instruction
- merged `main` SHA: `PENDING_FINAL_MERGE`
- GitHub Pages live verification: `PENDING_FINAL_MERGE`

A successor thread should start from the then-current remote `main`, read this record, and never restart the CaixaBank/Concurso ripple reconstruction from zero.
