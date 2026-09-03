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

Reusable public overlay:

- `assets/caixabank-concurso-ripple-interconnect-20260903.js`

The overlay is applied only to an explicit ES/EN route allow-list covering:

- CaixaBank Valencia claim;
- LPB / Concurso 36/2012 insolvency hub;
- lender/creditor-of-record hub;
- sale/lender convergence / possession-credit chain;
- recovery and restitution objectives;
- administrator-removal RPL 3304/3319 dossier;
- administrator overview and removal/fees pages.

The overlay is loaded through the already universal `borja-separation-rpl3304-inbound-20260902.js` loader path. This avoids rewriting the inherited `site.js` loader contract or removing its preservation markers. The ripple asset itself exits immediately outside the explicit governed allow-list.

## Primary court notice preserved

No court-notice image was regenerated or replaced.

The existing public child route remains the primary source:

- `/es/reclamacion-caixabank-valencia/senalamiento-28-enero-2027/`

Existing public images remain:

- `assets/evidence/caixabank-valencia-1859-2023-diligencia-06nov2025-p1-publica.jpg`
- `assets/evidence/caixabank-valencia-1859-2023-diligencia-06nov2025-p2-publica.jpg`

The reusable overlay adds a visible thumbnail/card on both ES and EN CaixaBank main dossiers and links to the two-page redacted public notice.

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

No competing identity record is created by this workstream.

- Existing canonical `^` identities remain controlling.
- Public ripple surfaces link to the canonical justice-professionals identity register.
- No name is completed from office succession, family/company relationship or contextual proximity.
- Unknown authorities remain `SOURCE_GAP` under the existing identity system.
- No new `CARET_PENDING` identity was introduced by this patch.

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

These are retained as evidential/legal gaps, not filled by inference.

## Validation / merge fields

To be completed at PR closeout:

- PR: `PENDING`
- merged `main` SHA: `PENDING`
- checks/validators: `PENDING`
- GitHub Pages live verification: `PENDING`

A successor thread should start from the then-current remote `main`, read this record, and never restart the CaixaBank/Concurso ripple reconstruction from zero.
