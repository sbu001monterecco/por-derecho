# Thread-deletion continuity audit — banking publication backlog

**Audit date:** 16 August 2026  
**Scope:** stale PR #19 (PH122→CAM assignment / Article 1535) and stale draft PR #17 (LPB insolvency / sale-lender convergence), rebuilt and published from current controlled evidence.

## Verdict

**DELETION-SAFE WITH OPEN EVIDENCE.**

The two material publication backlogs identified in the conversation have been rebuilt from current `main`, source-controlled, merged, exact-SHA Pages deployed and the stale PRs closed as superseded. A fresh thread can recover the publication state, primary-source locators, correction boundaries, unresolved evidence and deployment trail without relying on this chat.

## 1. Replacement of stale PR #19

### Current public routes

- `/es/acreedor-de-registro/credito-litigioso-escritura/`
- `/en/lender-of-record/litigious-credit-hidden-deed/`

### Current controlling internal record

- `archive/PH122_CAM_ASSIGNMENT_ART1535_PUBLICATION_CONTROL_16AUG2026.md`
- ME-061 in `archive/MISSING_EVIDENCE_REGISTER.md`
- banking row in `archive/CONTINUOUS_MAINTENANCE_MATRIX.md`

### Freshly re-queried primary-source locators

1. **12-Jul-2016 LPB→insolvency administration quantified notice**  
   Drive title: `BUROFAX LUCHY al ADMINISTRADOR CONCURSAL.pdf`  
   Drive id: `12sMIQNV9bpruE3DVdhgQoxxatPdrGltd`  
   Classification: existence/date/quantified dispute source-supported; allegations of overstatement, duplication, nullity or misconduct remain PARTY ALLEGATION unless independently established.

2. **6-Dec-2017 assignment-information demand**  
   Drive title: `4127-9620-2767 v 2, LUCHY PLAYA - Burofax requerimiento datos sobre cesión (crédito litigioso).docx`  
   Drive id: `1-Dc2ThZkVHuRSlBb6AJR8PoDiI89RUWqIf-ZP1_nCjA`
   Classification: request for deed/price and LPB's Article 1535 legal position are source-supported; litigious-credit status was LPB's contention, not a judicial finding.

3. **19-Dec-2017 Preliminary Proceedings 1041/2017**  
   Drive title: `Auto admite Diligencia (LPB Tanteo y Retracto - Proc 1041) 19DIC17.pdf`  
   Drive id: `1_n8VvVPEFfC37fJ4c3wdbpgiVLLlPR3P`  
   Classification: final order allowed the requested production measure for complete deed, precise price, payment date and costs, subject to security; admission does not prove unlawful withholding, non-compliance or liability.

4. **15-Feb-2018 Commercial Court order**
   Drive title: `8. Modificacion Textos Definitivos PRIV ESPECIAL (SIN INTERESES) 8FEB2018.pdf`  
   Drive id: `1jwG4inqC8HFOdLbU3RdPY3PKj6SzKA7f`  
   Classification: primary adverse ruling. It rejected LPB's Article 1535 theory, while accepting that assignment changed the creditor but not the amounts recognised in the final insolvency texts; it identified €857,373.81 and €8,194,877.88 plus contingent enforcement costs. The `8FEB2018` Drive filename is retained as source metadata but is not the controlling act date.

### Publication boundary

Do not reintroduce the stale PR #19 language that treated deliberate opacity, favouritism/bias, deliberate inflation or a manufactured undisputed debt as established. Strict Article 1535 status remains open pending the exact pre-20-Oct-2017 claim/opposition/incident and responsive pleading/act credit by credit.

### Replacement implementation

- replacement PR: **#146**
- merge: `5af0de47b691c03429bce2806de955bfa717891c`
- exact-SHA Pages build: **1154939713 — built, no error**
- old PR #19: **closed, unmerged, explicitly marked superseded by #146**

## 2. Replacement of stale draft PR #17

### Current public routes

- `/es/insolvencia-lpb/`
- `/en/lpb-insolvency/`
- `/es/convergencia-venta-acreedor/`
- `/en/sale-lender-convergence/`

### Current controlling internal record

- `archive/LPB_INSOLVENCY_SALE_LENDER_CONVERGENCE_PUBLICATION_CONTROL_16AUG2026.md`
- banking row in `archive/CONTINUOUS_MAINTENANCE_MATRIX.md`
- CR-024 to CR-032 as applicable
- ME-051–059, with ME-061 for the separate assignment issue

### Controlling corrections

- Primary 15-May-2012 Mortgage Enforcement 90/2012 auction schedule = **158 properties**, not 166.
- 159 and 166 remain separate measurements/layers pending a property-by-property reconciliation.
- Only **LPB and its estate** entered Concurso 36/2012; Sun Park as a mixed-ownership complex, CEXP, Monterecco/Pink, Matkator, Aweswell and other owners did not thereby become part of one insolvency estate.
- June-2012 asset surplus does not by itself negate insolvency under the historical regular-payment/cash-flow test.
- Enforcement/auction is the documented immediate timing trigger for the defensive filing; this is not proof that the bank caused every component of the crisis.
- The 28-Feb-2012 viability plan proves direct-market/tour-operator architecture existed before the insolvency filing.
- Mortgage-credit ownership/accounting and the contested banking-product/Valencia liability lane remain separate.
- UK Monterecco Sun Park Limited→Aweswell Limited and Spanish Monterecco Sun Park, S.L.→Pink Canary Services, S.L. are two separate same-company name-continuity chains; the UK and Spanish legal persons remain distinct.
- Later title does not retrospectively authorise earlier access/control/commercialisation; earlier disputes do not automatically invalidate later title, financing, support or operation.

### Source recovery anchors

The current lender-of-record pages and `archive/BANKING_ORIGIN_GAP_CLOSURE_LEDGER_16AUG2026.md` are the controlling synthesis. The June declaration source remains recoverable from connected Drive; one located copy is titled `4. AUTO DECLARACION CONCURSO 11JUN2012.pdf`, Drive id `1ZjGb_UW1UNhtIeB1u977zZhLcRqhRZKh`. Its connector fetch returned the PDF binary without parsed text during this close-out, so the public pages rely on already controlled repository propositions rather than inventing content from an unread scan.

### Replacement implementation

- replacement PR: **#148**
- merge: `7e3c84161545cb6ed17ebed5b2660026a4fc0586`
- exact-SHA Pages build: **1154951959 — built, no error**
- old PR #17: **closed, unmerged, explicitly marked superseded by #148**

## 3. Discovery / navigation state

`assets/banking-recovery-publication-20260816.js` provides a bilingual three-route gateway from the existing lender-of-record pages to:

1. LPB Insolvency*;
2. sale/lender convergence; and
3. PH122→CAM / Article 1535.

`sitemap-banking-recovery.xml` advertises all six ES/EN banking-recovery routes and `robots.txt` advertises that supplemental sitemap.

## 4. External route-test limitation

An immediate direct route retrieval was attempted through the available web execution environment after deployment. That environment rejected the direct GitHub Pages URLs as unsafe-to-open because they were not previously returned by search/user input. This is an execution-environment restriction, not evidence of a site failure. Exact-SHA GitHub Pages builds and source-on-`main` verification are the deployment controls.

A later route test should be repeated when external retrieval permits it.

## 5. Open evidence that must remain open

### Banking / insolvency

- ME-051 native default notice and complete ledgers;
- ME-052 complete Mortgage Enforcement 90/2012 plus 158/159/166 property reconciliation;
- ME-053 acquisition/control chain;
- ME-054 privilege-controlled advice review;
- ME-055 conclusion/exit attempts;
- ME-056 direct-market/operator dataset;
- ME-057 Valencia public-safe record;
- ME-058 act-by-act duty/knowledge/capacity/causation matrix;
- ME-059 Spanish company-name-change package.

### Assignment / Article 1535

- ME-061 complete notarial protocol 2,248 and schedules;
- total/allocated price and payment proof;
- complete Preliminary Proceedings 1041/2017 compliance/outcome;
- exact pre-20-Oct-2017 claim/opposition/incident and response credit by credit;
- appeal/finality record for the 15-Feb-2018 order;
- insolvency-administration verification file;
- complete EH90/2012 and any other proceeding actually relied upon for asserted litigiosity.

## 6. Private-source / custody rule

Native Drive/Gmail/court-source files containing personal data, signatures, addresses, privileged material or unnecessary private information are not copied into public GitHub. The repository preserves public-safe source locators and propositions. Future threads must re-query connected primary systems when originals are required. Do not claim a separate cryptographic evidence-vault/hash event unless it has actually been performed and logged under `archive/EVIDENCE_CUSTODY_AND_PRESERVATION_PROTOCOL_16AUG2026.md`.

## 7. Fresh-thread recovery order

A new ChatGPT thread should read, in order:

1. `CHATGPT_START_HERE.md`;
2. `archive/CONTINUOUS_MAINTENANCE_MATRIX.md`;
3. `archive/MISSING_EVIDENCE_REGISTER.md` and `archive/CORRECTION_REGISTER.md`;
4. `archive/BANKING_ORIGIN_GAP_CLOSURE_LEDGER_16AUG2026.md`;
5. `archive/VALENCIA_BANKING_CONCURSAL_RECONCILIATION_LEDGER_16AUG2026.md`;
6. `archive/PH122_CAM_ASSIGNMENT_ART1535_PUBLICATION_CONTROL_16AUG2026.md`;
7. `archive/LPB_INSOLVENCY_SALE_LENDER_CONVERGENCE_PUBLICATION_CONTROL_16AUG2026.md`;
8. this audit;
9. the current public source files on `main`.

## Final continuity result

If this chat is deleted, a fresh thread can recover what was meant to be published, why the stale PRs were not merged, what was actually published instead, which primary sources controlled the Article 1535 publication, the exact correction from 166 to 158, the PR/build/deployment state and the unresolved source-completion queue.

**No material publication intention from the identified #17/#19 backlog remains trapped only in this conversation.**
