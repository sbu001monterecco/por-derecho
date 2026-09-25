# OPEN-KIMONO SUPERVISORY PRACTICE — IMPLEMENTATION CONTROL

**Control date:** 18 August 2026  
**Implementation branch:** `open-kimono-supervisory-practice-18aug2026`  
**Status at creation:** IMPLEMENTED ON WORKING BRANCH; PR / MERGE / RENDER VERIFICATION TO FOLLOW  
**Purpose:** make Por Derecho / Project Sun Rock a textbook-easy public practitioner system for CNMV, RICPE, Regional Incentives, SNCA/FEDER/European-funds functions and connected public offices.

## 1. Governing concept

“Open kimono” is used as a transparency metaphor, not as a waiver of confidentiality or privilege. The public standard is:

`question → competence → primary source → evidential boundary → verification → contrary evidence → decision → status → correction`.

A practitioner should be able to see:

- what the issue is;
- what the office can lawfully verify;
- what belongs to another office;
- the first records to inspect;
- what changed;
- the minimum production;
- what evidence could weaken or refute the Project position;
- what good supervisory/audit practice looks like;
- and warning signs of the opposite practice.

The negative-practice panels are a falsifiable audit standard. They do **not** assert that every named institution or person engaged in every listed negative practice.

## 2. Route ownership

### CNMV

- ES: `/es/cnmv-ricpe-verificacion/`
- EN: `/en/cnmv-ricpe-verification/`

Role: bounded supervisory gateway. It starts with 13-Jan-2021 CNMV notice, the 20-Jul-2021 RICPE internal documented position, the 21-Jul-2021 CAM court use, 22-Jan-2026 CNMV traceability and the 17-Aug-2026 RICPE communication.

Central question:

> What changed between the RICPE position documented on 20 July 2021 and later re-entry, financing and MYND operation?

The route expressly separates CNMV competence from civil/registry/Community/insolvency, tax/public-aid and criminal branches.

### RICPE

- Main institutional gateway / full dossier: `/es|en/ric-private-equity-sun-park/`
- Detailed controls: `/es/ricpe-responsabilidad-documental/`; `/en/ricpe-documentary-accountability/`

The main route is no longer to be presented simultaneously as a legacy/archive-only route. Runtime control removes the older background-archive banner and restores the current 17-Aug communication identity.

### Regional Incentives

- ES: `/es/incentivos-regionales-gc836-p06/`
- EN: `/en/regional-incentives-gc836-p06/`

Unique function: practitioner workflow for the GC/836/P06 award, title/availability, viable project, self-financing, start of investment, eligible assets/costs, connected-party treatment, other finance/aid, employment, intermediate/final conditions, inventory, verification, payment, inspection, non-compliance, sanction, correction and recovery.

Public controlled figures:

- beneficiary: Hotel New Trend, S.L.;
- investment: €11,469,714.00;
- subsidy: €3,440,914.20;
- employment: 60.

These figures prove the published award data, not full payment, final eligibility, employment compliance or absence of overlap.

### SNCA / ERDF / European funds

- ES: `/es/snca-fondos-europeos-trazabilidad/`
- EN: `/en/snca-eu-funds-traceability/`

Role: separate intake/anti-fraud, operation management, accounting/certification, inspection/control and audit/recovery functions.

Audit chain:

`beneficiary → asset/right → work package → contract/supplier → invoice/payment → eligible expenditure → certification/co-financing → result/employment → verification/audit → correction/recovery`.

The permanent MYND plaque identifies ERDF/FEDER. It does not by itself prove operation identifier, programme, co-financing rate, certified expenditure, payment, verification result or absence of overlap.

### Public-authority clean room

- ES: `/es/reconstruccion-unitaria-autoridades-publicas/`
- EN: `/en/public-authority-unitary-case-reconstruction/`

A cross-authority dependency matrix is dynamically added, mapping CNMV, RICPE, Regional Incentives, ERDF, SNCA/IGAE, AEAT/RIC, Court/AC and Cadastre/Registry questions to their distinct records and limits.

## 3. P0 implementation corrections

### Recipient-specific first screen

Updated:

- `assets/same-asset-multiple-financial-lives-20260816.js`
- `assets/public-authority-case-reconstruction-20260817.js`

Controls:

- dedicated CNMV, SNCA, Regional Incentives and main RICPE routes are excluded from generic preface modules;
- hero lookup recognises `.dossier-hero`, `.cnmv-hero` and `.hero`;
- dedicated practitioner CSS also hides cached legacy generic modules before `.cnmv-hero`, `.eu-hero` or `.ir-hero`.

### RICPE route identity

`assets/practitioner-open-kimono-20260818.js` removes the legacy RICPE archive banner and restores the current formal-communication eyebrow on the main RICPE route.

### Corporate-knowledge wording

Runtime text control changes generic “what RICPE knew” wording to “what RICPE documented internally”, preserving person/function-specific production questions.

### RICPE/HNT financing correction — CR-058

The public implementation preserves two source-specific totals:

- **€6,570,713.56** — prospectus-specific sum: €1,598,849.78 works + €4,971,863.78 employment;
- **€6,573,703.10** — separate earlier accounts/repository reconstruction;
- **€2,989.54** — unreconciled difference.

Neither amount is silently selected or normalised. Runtime propagation updates older public occurrences where static source remains legacy.

## 4. New shared implementation assets

- `assets/practitioner-open-kimono-20260818.css`
- `assets/practitioner-open-kimono-20260818.js`
- `assets/supervisory-practice-entrypoints-20260818.js`

Loaded through `assets/ricpe-filed-status-20260817.js`, which is already part of the global `site.js` chain.

Functions include:

- open-kimono positive/negative practice panels;
- RICPE identity correction;
- source-specific financing number correction;
- RICPE internal-document wording correction;
- public-authority cross-office matrix;
- homepage practitioner entry point;
- ES/EN 18-Aug material-update card.

## 5. Current official-practice sources used

### CNMV

Official CNMV investor-information page states that professional matters should be directed to the department competent by subject through the electronic-office procedure “Cualquier escrito, solicitud o comunicación dirigido a la CNMV”.

### Regional Incentives

Official framework and current structure used:

- Real Decreto 899/2007, with temporal-version warning;
- Subdirección General de Incentivos Regionales — state policy execution / Governing Council support;
- Subdirección General de Inspección y Control — inspection/checks, non-compliance and sanction processing;
- the competent Autonomous Community body remains separately responsible for the condition-evidence/report stages provided by the applicable scheme.

The file-specific applicable version must be fixed by application, award, modification, execution and settlement dates.

### European funds

Current official structure used:

- ERDF Management function;
- Certification and Payments / accounting function;
- Inspection and Control;
- SNCA / Infofraud channel as distinct intake/anti-fraud function.

The public pages do not claim that a current organisational title proves which person handled the historical Sun Park file.

## 6. Evidence-state controls

Visible categories remain:

- verified fact;
- verified with limit;
- actor/project representation;
- Project allegation;
- evidence-based inference;
- unresolved question;
- corrected/superseded;
- official procedural status.

Non-negotiable distinctions:

- alert ≠ proved fraud;
- filing ≠ admission ≠ examination ≠ decision;
- award ≠ payment ≠ final eligibility;
- plaque ≠ full ERDF operation/audit record;
- separate instruments ≠ proof of no overlap;
- multiple instruments ≠ proof of duplicate funding;
- operation ≠ title;
- later title ≠ retrospective validation;
- referral ≠ merits acceptance;
- lawful secrecy ≠ proof of inaction or exoneration.

## 7. Search and discovery

Created:

- `sitemap-supervisory-practice.xml`

Updated:

- `robots.txt`

The specialist sitemap includes CNMV, RICPE, Regional Incentives, SNCA/ERDF and the public-authority clean room in ES/EN.

## 8. Acceptance tests required before final delivery claim

### Source tests

- JavaScript syntax;
- HTML parsing;
- canonical/hreflang reciprocity;
- link/anchor review;
- stale amount scan;
- stale “what RICPE knew” scan;
- private RICPE credential scan;
- route-guard verification;
- duplicate-ID review.

### Render tests

- CNMV hero is the first substantive main module;
- RICPE hero/cockpit governs the first read;
- SNCA and Regional Incentives heroes are not pre-empted by generic modules;
- mobile at 360, 390 and 768 px;
- desktop;
- horizontal tables;
- anchor behaviour;
- no body overflow;
- ES/EN parity.

Repository/source presence is not equivalent to rendered deployment verification.

## 9. Maintenance rule

Future edits should improve this architecture only where a real practitioner need exists. Do not create another general supervisory page. Preserve the three levels:

`one minute → seven minutes → full audit`.

A new institutional page requires a unique competence/workflow not adequately served by an existing canonical route.
