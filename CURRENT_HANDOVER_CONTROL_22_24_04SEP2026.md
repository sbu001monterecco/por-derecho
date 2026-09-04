# Current handover — Control 22 / DP 1956/2026 and Control 24

**Date:** 4 September 2026  
**Repository:** `sbu001monterecco/por-derecho`  
**Publication branch:** `publish/controls-22-24-digitisation-20260904`  
**Base main at branch creation:** `56761b5fa7a06579b3db563d859d75c65fb0a0b6`  
**Publication PR:** `#1413`  
**Merge commit:** `d6c3550cc86e4b7dd642126b458cf205c4379bf6`  
**Focused validation:** run `33823156071` — **SUCCESS**  
**GitHub Pages deployment:** run `33823548923` — **SUCCESS**, deployed SHA `d6c3550cc86e4b7dd642126b458cf205c4379bf6`  
**Direct independent HTTP readback of the four new routes:** not independently confirmed at this closeout; do not upgrade to `LIVE_VERIFIED` until that check succeeds.

## 1. Scope completed

This release digitises and interconnects two separate complaint layers arising from the same Insolvency Proceeding 36/2012 factual matrix:

1. **Control 22** — the 18 June 2026 complaint concerning the alleged own acts and omissions of the Insolvency Administrator, later associated in the available record with **DP 1956/2026**.
2. **Control 24** — the 18 June 2026 complaint concerning identifiable judicial decisions and supervision in Insolvency Proceeding 36/2012, together with the dependent contribution presented on 25 June 2026.

The release also states precisely how Gil Marer treats Control 24 as the documentary basis of a formal **querella** route while preserving the presently decisive boundary: **no filing receipt proving a formal querella has been located in the finite corpus used for this release**.

## 2. Public pages

Spanish:

- `/es/control-22-denuncia-administrador-concursal/`
- `/es/control-24-denuncia-juez-concurso-36-2012/`

English:

- `/en/control-22-insolvency-administrator-complaint/`
- `/en/control-24-insolvency-judge-complaint-36-2012/`

Each page includes:

- procedural identity and legal nature;
- attributed party position rather than adjudicated fact;
- documentary modules and finite proof questions;
- current procedural status and explicit gaps;
- reciprocal language route;
- links to DP 1956, DP 1901, the Insolvency Administrator, the judge, CGPJ/Fiscalía, removal/fees and funded-exit records;
- correction, right-of-reply and non-fragmentation boundaries.

## 3. Structured and discovery layers

- `data/control-22-24-interconnection-register.json` — typed nodes, edges, issue modules, status boundaries and priority gaps.
- `assets/control-22-24-interlink-20260904.js` — contextual interconnection panel on relevant repository pages.
- `assets/control-22-24-search-extension-20260904.js` — homepage search discovery for Control 22, DP 1956 and Control 24 terms.
- `assets/site.js` — continuity-preserving loader update; legacy, Matkator 8584 and hotel-finca loaders remain intact.
- `sitemap-control-22-24.xml` — four bilingual routes.
- `robots.txt` — specialised sitemap registered.
- `.github/workflows/validate-control-22-24.yml` — focused release validation.

## 4. Non-negotiable identity rules

- **Control 22 ≠ DP 1956/2026.** Control 22 is a filing locator; DP 1956/2026 is the later court proceeding identity.
- **Control 24 ≠ NIG, DP, High Court case number or querella.** It is a filing locator attached to a complaint/notitia criminis.
- **25 June supplement ≠ autonomous complaint.** It remains dependent unless a primary source proves otherwise.
- **Prepared, reviewed or sent to counsel ≠ filed.** A filing receipt is required.
- **Related ≠ consolidated. Shared evidence ≠ shared responsibility.**
- **Adverse decision or omission ≠ criminal intent.** Actor, capacity, knowledge, duty, act/omission, effect, lawful alternative explanation and causal bridge must be proved separately.

## 5. Control 22 status

The public digest records:

- principal candidate: 55-page complaint, internally dated 17 June and presented on 18 June 2026;
- nature: denuncia/notitia criminis, not querella;
- later identifiers associated with the court route: DP 1956/2026, NIG `3501643220260016826`, IUP `LI2026016921`, Plaza no. 1 of the Las Palmas Investigation Section;
- provisional dismissal communicated on 21 July 2026;
- drafts of reform/appeal located, but no receipt proving filing located;
- no statement that the Insolvency Administrator committed an offence or acted in concert.

The visible apparent `30/2012` reference and irregular other-request numbering at the end of the principal candidate are preserved as source anomalies. They must never be silently corrected in a diplomatic transcript.

## 6. Control 24 status

The public digest records:

- signed package: 79 pages, including a 31-page principal complaint and ten selected annexes;
- presentation: 18 June 2026 under the Dean's Office locator Control 24;
- intended recipient: Civil and Criminal Chamber of the High Court of Justice of the Canary Islands;
- nature: written complaint/notitia criminis, not formal querella or appearance;
- 25 June supplement: ten pages, physical joinder reported by the presenter, electronic joinder not certified;
- official court entry, NIG, assigned body, present location and outcome: **not confirmed**;
- handwritten-date observation: preserved as the presenter's account and not characterised as falsification, manipulation or backdating.

## 7. Formal querella interface

The authorised public statement is:

> Gil Marer treats Control 24 and its supporting dossier as the documentary and procedural basis of the formal querella route concerning the judge. The repository has not located a filing receipt allowing it to state that such a querella was formally filed.

Do not shorten this to “the querella was filed” unless a primary receipt establishes date, organ, counsel/procurador route and documentary relationship.

## 8. Shared issue modules

The two complaints and related proceedings may share evidence concerning:

- the ONA/Clubotel funded-exit route and other finance alternatives;
- material control from June 2018;
- the 28 November 2018 OB REM transaction, €400,000 and 24 October 2019 non-validation;
- Promontoria–CAM assignment and creditor substitution;
- recognised credit, interest, improvement threshold and final amount extinguished;
- 2021 competition and 2022 adjudication/deed/registry implementation;
- final accounts and asset/revenue traceability.

Every module must be tested through actor-specific arrows. No common outcome proves common knowledge, common intent or agreement.

## 9. Priority gaps

1. Obtain the primary bridge showing how Control 22 was allocated or associated with DP 1956/2026.
2. Confirm whether any reform or appeal against the DP 1956 provisional dismissal was actually filed.
3. Obtain Dean's Office and/or High Court certification for Control 24: entry, time, inventory, outgoing route, recipient, present location and result.
4. Obtain the electronic metadata and joinder record for the 25 June supplement.
5. Locate any formal querella filing receipt before changing the current public status.
6. Produce the certified Insolvency 36/2012 docket and the act–knowledge–duty–response–effect matrix for each shared issue module.

## 10. Privacy and source boundary

No unredacted pleading, signature, private address, telephone number, email address, personal identifier, provider URL, credential, privileged advice, reserved tax material or native private correspondence is published in this release. The web pages are public-safe digests. Native evidence remains in private custody and must be linked through provenance rather than copied into public Git.

## 11. Successor instruction

Start from the structured register, then descend to the exact source and actor. Do not restart from a single undifferentiated “judge and administrator” accusation. Preserve three separate layers:

- private actors — Control 21 / DP 1901;
- Insolvency Administrator — Control 22 / DP 1956;
- judicial decisions and supervision — Control 24 and its separate querella/CGPJ/Fiscalía interfaces.

The repository source is merged and Pages has deployed the exact merge SHA. Direct public-edge readback remains a separate verification state. If a successor obtains successful cache-busted HTTP readback of all four routes, update the manifest and this handover to `LIVE_VERIFIED`; otherwise do not infer live state from deployment alone.
