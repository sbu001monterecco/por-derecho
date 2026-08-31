# Cuatrecasas book and media delta — implementation, live verification and continuity record

**Date:** 31 August 2026  
**Control ID:** `PD-4C-BOOK-DELTA-20260831-01`  
**Repository:** `sbu001monterecco/por-derecho`  
**Initial task main:** `950b64f9bd61f21bcff7bd76cfc409eebd3bca88`  
**Reconciled publication base:** `80793dbba490b44a2ad25af836f201517000f5bc`  
**Publication PR:** `#1259`  
**Publication merge:** `4938164da577b27ad63bb731d74013ee90979727`  
**Pages run:** `33374111565` — success  
**Independent live run:** `33374892490` — four of four routes verified  
**Publication state:** `LIVE_VERIFIED`

## Purpose and result

The controlled Cuatrecasas / Sun Park professional-accountability record is now connected to Gil Marer’s planned book *4 Green Houses, One Red Hotel* through a bilingual, document-led public architecture.

The central narrative is the professional inversion:

> a firm retained within the rescue, finance, insolvency and asset-protection perimeter later became claimant and executant against Matkator, an entity and property holder within the same physical hotel reality.

That transition is published as a documentary and professional-accountability question. It is not published as a finding of negligence, conflict, procedural fraud, collusion, criminal participation or intentional interference with Concurso 36/2012.

## Public implementation

The English and Spanish book pages now cover:

1. mandate and responsible professional entity;
2. knowledge of Sun Park, LPB, Matkator, control, financing, title and Concurso 36/2012;
3. affirmative acts and attributed omissions;
4. communication, silence, warning and handover;
5. the fee/debtor/promissory-note chain;
6. later Cambiario 1048/2019 and ETJ 163/2020 conduct;
7. the finite DP 748/2026 procedural-fraud hypothesis;
8. the still-unproved directional bridge from La Laguna into Las Palmas;
9. causation, loss, strongest defence and remedy;
10. five source-controlled media-release tracks.

The bilingual critical-gap pages now include:

- **CG-011 — La Laguna → Las Palmas directional bridge**;
- **CG-012 — private legal-team delta and filing-status completeness**.

The pages interlink the canonical Cuatrecasas lifecycle, DP 748 / ETJ / civil-action, critical-gap, professional-conduct, Concurso 36/2012 decision, Master Proceedings Register and book routes.

## Evidence boundaries

### Acts, omissions, silence and enablement

The project may investigate and attribute a client-side position concerning affirmative acts, omissions, silence, deficient handover and causal enablement. “Enablement” is not association. It requires a defined duty, knowledge, available protective step, act or omission, intervening decision, counterfactual and claimant-specific loss. Temporal sequence, common subject matter or later benefit is insufficient.

### Fees and execution

The book does not assume that no fee was due. The controlled chain remains:

`client → instructor → beneficiary → invoice → expected payer → actual payer → pagaré → judicial debtor → title → asset → adjudication → possible cession → final beneficiary`.

The underlying entitlement, correct debtor, instrument function, service, former-client conflict, asset identity, valuation, adjudication and possible cession must each be proved from the relevant primary record.

### Procedural-fraud hypothesis

No public finding of *estafa procesal* is made. The finite test requires:

- an exact deception or legally material omission;
- knowledge;
- fraudulent intent;
- causal judicial error;
- a prejudicial patrimonial resolution or disposition;
- loss;
- improper benefit.

Disputed billing, deficient professional performance, silence, an adverse order or later benefit does not alone establish procedural fraud.

### La Laguna → Las Palmas

Before alleging intentional instrumentalisation, the record must identify:

- the exact La Laguna act and source;
- author, signatory, instructor and approver;
- prior knowledge from the mandate;
- immediate La Laguna effect;
- the exact transmission mechanism into Concurso 36/2012;
- the Las Palmas recipient or decision-maker;
- actual reliance or procedural effect;
- patrimonial consequence;
- beneficiary and affected legal person;
- foreseeability;
- separate proof of purpose if intent is alleged;
- counterfactual and ordinary-enforcement explanation.

Until transmission and reliance are proved, the status remains:

> **OPEN DIRECTIONAL BRIDGE — EFFECT NOT YET PROVED.**

A defence-side use in 2026 of material from one proceeding to seek protection in another proves a defensive procedural connection made by current counsel. It does not prove that the original claimant created or maintained La Laguna to manipulate a separate court.

## Private source delta

A role-based review of four private legal-team channels was run for material after 27 August 2026.

Aggregate result:

- one new private draft package located;
- no new presentation proof located;
- no new signed judicial decision located in that delta;
- no new Cuatrecasas public fact or filed-status change established.

The private draft, sender locators, message/attachment identifiers and live legal strategy remain outside the public repository. A draft is not a filing.

The private canonical manuscript was updated with the professional-inversion and two-court supplement. A separate private Google Doc stores the exact role-based mailbox queries, source locators, version lineage, deadline controls and next delta cursor. Those private locators are not reproduced here.

## Media architecture

Maximum sustainable pressure is defined as maximum documentary visibility, answerability and correction discipline—not maximum rhetorical escalation.

Five controlled public release tracks are recognised:

1. **Professional lifecycle** — mandate, billing, knowledge, advice, acts, omissions, communication and handover.
2. **Matkator inversion** — transition from adviser within the rescue perimeter to claimant and executant against a company and property inside the same hotel reality.
3. **Fee and instrument chain** — the full causal chain from client through final beneficiary.
4. **La Laguna–Las Palmas map** — documented edges, missing transmission/reliance, counterfactual and strongest non-fraud explanation.
5. **Institutional answer tracker** — finite questions, documents produced, right of reply, corrections, professional-body status and court outcomes.

Every material release must state its primary-source basis, evidential status, strongest foreseeable defence, missing proof, finite questions, response status and correction/version history. Non-response is not an admission.

## Source and workflow controls added

- `prompts/CUATRECASAS_BOOK_MEDIA_DELTA_AGENT_31AUG2026.md`
- `assets/data/cuatrecasas-book-media-delta-v1.json`
- `publication-manifests/cuatrecasas-book-media-delta-20260831.json`
- `scripts/validate_cuatrecasas_book_live.py`
- `.github/workflows/validate-cuatrecasas-book-live.yml`

The live workflow is permanent and reproducible. It performs cache-busted external HTTPS GETs against the production GitHub Pages routes and requires HTTP 200, HTML content type, exact bilingual publication markers and canonical internal links.

## Deployment and live proof

PR `#1259` merged as `4938164da577b27ad63bb731d74013ee90979727`.

Pages run `33374111565` built and deployed that exact SHA successfully to the production environment.

Independent workflow run `33374892490`, job `99434055793`, verified at `2026-08-31T08:52:10Z`:

| Route | HTTP | Bytes | SHA-256 |
|---|---:|---:|---|
| EN book | 200 | 16,110 | `d575fdb8971fda0394fc3ccbc1e49790ccadb2531a4e2d49f412da1c604f6bc7` |
| ES book | 200 | 16,974 | `3eb96d65ceb6051cae07aac76c672d8a7516e77d7f6d61b333173341a64bc2de` |
| EN critical gaps | 200 | 10,725 | `0efd41735806ae0319dc6fbe71c07e99a48c96e2674c1d2c5bcd7078b9b993d9` |
| ES critical gaps | 200 | 11,145 | `263a1edb8e853a145574dfb6e8a6a26f09761df99540aa5214ac459dead80fbf` |

All required markers and interlinks were present. The verification artifact is `9751478683`, archive digest `ae7a0dc43ddfc2c771979a914b6015536e3f77bceac623c1ce79d6b08dea7b1b`.

## Privacy and authority boundary

Not included in the public repository:

- private email addresses;
- private message or attachment IDs;
- private subjects or full emails;
- privileged legal advice;
- current-counsel strategy;
- unsent drafts;
- filing credentials;
- unnecessary personal, service or payment data.

Repository and website publication authority does not authorise email, filing, third-party contact, fee commitment, account change or publication of private legal-team sources.

## Continuity and deletion-safety assessment

The public implementation, controlling prompt, machine-readable control, publication manifest, private manuscript supplement and private delta-control document now preserve the material work independently of the originating chat.

This thread is continuity-safe for the Cuatrecasas/book/media update once the closeout PR containing this `LIVE_VERIFIED` record is merged. That statement concerns preservation of this work product. It does not claim that the complete Cambiario, ETJ, DP 748 or Concurso 36/2012 evidential corpus is complete.

CG-011 remains intentionally open until the directional transmission, reliance and any alleged purpose are proved from primary records. CG-012 remains an active maintenance control for future legal-team deltas.
