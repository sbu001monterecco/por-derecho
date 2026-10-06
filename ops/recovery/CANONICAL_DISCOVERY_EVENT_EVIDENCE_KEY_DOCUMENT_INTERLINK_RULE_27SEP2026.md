# Canonical discovery → event/evidence/key-document interlink rule

**Control date:** 27 September 2026  
**Status:** controlling ingestion rule for recursive recovery and all future source discovery.  
**Purpose:** ensure that material information recovered from Gmail, Google Drive, repository history, public authorities or other source-controlled channels is not left as an orphaned note, filename, email or narrative conclusion.

## 1. Controlling rule

Every **material** discovery must pass through canonicalisation before its lane can be marked `UTILIZED` or GREEN.

A discovery is material when it changes, supports, qualifies, contradicts, dates, attributes, authenticates, narrows, or creates a finite gap concerning a canonical actor, entity, proceeding, event, claim/proposition, asset, transaction, authority communication, filing, decision, document or evidential inference.

Noise, exact duplicates and purely administrative copies may terminate as classified non-material/duplicate records, but their duplicate/provenance relationship must be recorded where it matters to custody.

## 2. Mandatory canonical objects

For every material discovery determine, append or update **all applicable** objects:

1. **Source identity** — native source/provider identity, date, custody, hash where available, source status and public/private boundary.
2. **Key document / artifact** — stable document identity for pleadings, judgments, reports, ACTAS, deeds, contracts, emails, receipts, technical records, financial records and other decisive artifacts.
3. **Canonical event** — dated or bounded occurrence supported by the source. A document and an event are not interchangeable.
4. **Evidence item / proposition support** — what the source actually proves, supports, qualifies or contradicts, with proof ceiling.
5. **Proceeding / institutional file** — reuse the master proceeding/file identity where applicable; append only when genuinely new.
6. **Actor/entity** — every material named/attributed participant, with role and identity boundary.
7. **Claim/proposition** — link the evidence to the exact proposition, allegation, inference, lawful alternative or official finding it bears on.
8. **Gap / missing evidence** — when the source reveals a finite unresolved question, add/update the canonical gap rather than leaving it in prose.
9. **Authority communication / filing state** — when relevant, update the state machine without collapsing receipt, routing, incorporation, examination and decision.
10. **Public-safe route** — if publication is appropriate, update the canonical ES/EN reader rather than creating an orphan page.

## 3. Mandatory reciprocal interlinks

Canonicalisation is incomplete unless relationships are reciprocal where the repository architecture supports them.

Minimum graph:

`SOURCE ↔ KEY DOCUMENT ↔ EVENT ↔ EVIDENCE/PROPOSITION ↔ ACTOR/ENTITY ↔ PROCEEDING/FILE ↔ CLAIM/GAP ↔ AUTHORITY COMMUNICATION`

Requirements:
- event → source/document and source/document → event;
- evidence/proposition → source and source → propositions it materially supports/qualifies/contradicts;
- proceeding → events/documents/actors and material event/document → proceeding;
- actor → material events/proceedings/evidence and those nodes → actor;
- gap → known evidence/retrieval route and recovered evidence → gap closed/narrowed;
- public page → canonical machine/source control and canonical control → public route;
- contradiction/contrary evidence must link to the proposition it limits;
- successor filing/response must link backward to predecessor and predecessor forward to successor.

No material canonical node should remain orphaned.

## 4. Evidence-state discipline

Every proposition must be typed. Use the closest controlling class:
- `PRIMARY_SOURCE_FACT`
- `OFFICIAL_SOURCE_FACT`
- `ADJUDICATED_FINDING`
- `PARTY_ALLEGATION`
- `ATTRIBUTED_RECOLLECTION`
- `ANALYTICAL_INFERENCE`
- `CONTRARY_EVIDENCE`
- `LAWFUL_ALTERNATIVE`
- `OPEN_GAP`
- `DUPLICATE_CUSTODY_ONLY`

Never promote:
- an allegation into a fact;
- an administrative receipt into examination;
- an email association into authorship;
- a later recital into proof of the original event;
- duplicate reacquisition into independent corroboration;
- absence from a search into non-existence.

## 5. Existing canonical registers to reuse, not compete with

The repository is federated. Reuse existing stable IDs/registers and add reciprocal links rather than inventing a parallel universal taxonomy. Relevant controls include, as applicable:

- `archive/PROCEEDINGS_MASTER_REGISTER.csv`
- `archive/MASTER_PROCEEDINGS_REGISTER_INTERNAL_20AUG2026.md`
- `archive/MISSING_EVIDENCE_REGISTER.md` + controlled addenda
- `assets/data/open-evidence-disclosure-register-v1.json`
- `assets/data/ministerio-fiscal-canonical-register-20260919.json`
- `assets/data/institutional-communications-register-v1.json`
- `assets/authority-communications-register-20260901.js`
- `evidence/community/COMMUNITY_AUTHORITY_EVENTS_EMAILS_MEETINGS_ACTAS_PUBLIC_REGISTER.md`
- specialist canonical source/artifact/event registers already controlling a subject family
- actor/caret registers and canonical actor pages
- correction/contradiction registers
- current DP1901/E.G.745 action, filing, traceability and recovery controls.

If two registers overlap, add an explicit crosswalk. Do not renumber stable IDs merely to unify formats.

## 6. Recursive recovery gate

The recovery state machine is strengthened to:

`DISCOVERED → PRESERVED → DIGITIZED/READABILITY CLASSIFIED → CONTENT EXTRACTED → SUBSTANTIVELY ANALYZED → SOURCE IDENTITY RECONCILED → KEY DOCUMENT ID RECONCILED → EVENT RECONCILED → EVIDENCE/PROPOSITION LINKED → ACTOR/ENTITY LINKED → PROCEEDING/FILE LINKED → CLAIM/GAP/CONTRADICTION LINKED → RECIPROCAL BACKLINKS VERIFIED → PUBLIC-SAFE DERIVATIVE IF APPROPRIATE → GITHUB UTILIZED → GITLAB UTILIZED → DRIVE CUSTODY VERIFIED → LIVE PUBLIC READBACK IF PUBLIC`

A material discovery cannot be counted as **fully utilized** before the applicable canonical links and reciprocal backlinks are verified.

## 7. Duplicate rule

An exact duplicate does not receive a new event or evidential proposition merely because it was reacquired.

Record:
- canonical source/document ID;
- duplicate provider/custody locator privately where appropriate;
- hash/identity match;
- whether the reacquisition improves custody, provenance or transmission history.

A duplicate may create a **new transmission/custody event** if the act of transmission itself is material; the attached duplicate document remains the same key document.

## 8. New-source rule

When a recovered source reveals an event/document/proceeding not already canonical:

1. search existing IDs/aliases first;
2. allocate a new stable ID only if no existing identity fits;
3. create the minimum source/document/event/evidence nodes required;
4. link to actors, proceedings and claims;
5. add open gaps and contrary evidence at the same time;
6. add bilingual/public treatment only after public-safe review;
7. validate reciprocal graph integrity.

## 9. Green test

A recovery lane cannot be GREEN merely because its search cursor is exhausted.

For material discoveries in the lane, GREEN requires:
- classification complete;
- custody/readability state controlled;
- source and key-document identity reconciled;
- event/evidence/proposition treatment complete;
- actor/proceeding/claim/gap links complete;
- contradictions/lawful alternatives preserved;
- reciprocal backlinks verified;
- GitHub/GitLab/Drive state reconciled as applicable;
- live readback verified where public;
- authority-only residuals bounded.

## 10. Current recovery application

Apply this rule retrospectively to every material family surfaced by the 27-Sep recursive programme, including:
- 2018 Fiscalía packet;
- 2015 LPB refinance/rescue documents;
- 2017 Solos legal DD/acquisition materials;
- 2012 pericial/condition evidence;
- 2014 SAREB valuation analysis;
- Community accounts, planning, licence and title material;
- 2017 FRB/bond/structuring/service-agreement family;
- 2015 Concurso attachment bundle;
- DP1901/E.G.745/REGAGE/CGPJ successor evidence;
- every later material discovery from the explicit Gmail A/B/C/D matrix and Drive recursion.

Existing canonical representations should be strengthened/crosslinked; duplicates must not create false new events.

## 11. Maintenance rule

Every recursive/continuity thread must report:
- discoveries;
- duplicates;
- new/updated canonical source IDs;
- new/updated key-document IDs;
- new/updated event IDs;
- evidence/proposition links;
- actor/entity links;
- proceeding/file links;
- gap/contradiction changes;
- public route changes;
- orphan count.

**Target orphan count for material canonical discoveries: zero.**
