# PROCEEDINGS FULL-IDENTITY AND STORYING GOVERNANCE

**Date:** 30 August 2026
**Status:** repository-wide mandatory continuity and publication control
**Applies to:** every judicial, prosecutorial, administrative, regulatory and connected proceeding/file in the Por Derecho corpus

<!-- PROCEEDINGS_FULL_IDENTITY_STORYING_GATE -->

## 1. Purpose

Every proceeding must remain reconstructable without relying on a prior ChatGPT thread. The repository must capture the fullest source-supported identity of the file and tell its procedural story: what it is, how it arose, who participated, what happened, what was decided, what was not decided, why it matters to the wider record, what supports the account and what remains missing.

This control supplements the Master Proceedings Register, CAEPR / `^`, counsel-procurador filing lineage, Proceedings Interconnectivity Map, Case Prism, correction, evidence-gap, privacy and bilingual-publication controls. It does not convert an allegation, contextual bridge or internal inference into a finding.

## 2. Mandatory available-information rule

When an item below is available in a located source, it must be captured in the canonical or linked controls. A generic label or silent blank must not replace a more exact available value. When the item is not available, record the exact gap and the source needed to close it.

The Master CSV remains the canonical inventory and holds the compact identity. Richer detail may live in a proceeding-specific control, specialist register, CAEPR record, Case Prism data or dedicated public page, but it must use the same stable Master ID and be linked back to the master. Do not add unwieldy prose to the CSV merely to satisfy this rule.

### 2.1 Identity and classification

- stable Master ID and CAEPR proceeding/institution/person IDs;
- official proceeding reference, preserving punctuation and suffixes;
- decision, order, judgment, decree or resolution number as a distinct field from the proceeding reference;
- NIG and other official identifiers;
- proceeding/file class, jurisdiction, track and `TRUE` / `FALSE` / `UNVERIFIED` status;
- source-literal variants and canonical corrections, without turning a source error into an alias; and
- privacy/public-treatment classification.

### 2.2 Organ, venue and dates

- origin organ, current custodian and exact court, chamber or section;
- place and territorial scope where relevant;
- filing, admission, hearing, decision, notification, finality, transfer and other material dates;
- deciding panel, judge, magistrate, LAJ, prosecutor or signatory where the source identifies them; and
- latest verified procedural event, distinguished from the inventory scan date.

### 2.3 Parties and professional lineage

- each party or participant, its procedural role and the act in which that role appears;
- lawyer and side/perimeter, separately attributable per client, proceeding and period;
- procurador/procuradora, authority, power, personación and substitution where established;
- initiating, responsive and appellate filings and the court/LAJ response; and
- explicit gaps where personación, authority or a professional pairing has not been recovered.

### 2.4 Procedural lineage and interlinks

- parent, child, appeal, review, incidente, pieza, accumulation, referral, inhibition, transfer and follow-up;
- both forward and reverse navigation for every source-backed direct procedural edge;
- contextual evidentiary, actor, event, asset or transaction bridges, visibly separated from direct procedural edges;
- the source and status supporting each material edge; and
- unresolved duplicate, alias, successor, assignment or substitution questions without speculative merging.

### 2.5 Events, disposition and legal effect

- the initiating act and concise chronological sequence of material filings, hearings, decisions and notifications;
- the operative result, costs, remedies, appeal/finality status and later procedural consequences;
- what the decision actually determined and what it did not determine;
- the difference between a procedural ruling and a merits adjudication;
- allegations, attributed positions, documented facts, inferences, outcomes and open hypotheses kept distinct; and
- contrary evidence, qualifications and evidential/legal-effect limits.

### 2.6 Sources, custody and public routes

- source type, date, authenticity/status and public-safe evidence anchor;
- whether the record is a native institutional original, working copy, correspondence, reconstruction or secondary reference;
- correction and missing-evidence entries needed to resolve contradictions or incomplete dockets;
- dedicated bilingual public route/section for a materially significant proceeding, with reciprocal links to the master register, timeline/storyline, Case Prism, relevant actors and connected proceedings; and
- no publication of privileged advice, private locators, personal contact data or material otherwise excluded by the publication/privacy controls.

## 3. Storying contract

A material proceeding's public narrative must let a new reader answer, in plain language:

1. What file and decision are being described?
2. Which exact organ/section handled them, and when?
3. How did the matter arrive there and where did it go next?
4. Who appeared, for whom and through which verified professional lineage?
5. What were the key procedural steps and operative result?
6. What did the decision decide, and what remained outside its scope?
7. Why is the proceeding relevant to the wider Por Derecho chronology without conflating distinct cases?
8. Which sources support the account, and which records remain missing?

The story must be concise, chronological, bilingual where public, source-led and reciprocal: storyline → proceeding → source, and proceeding → parent/child/related route → storyline. If no dedicated page is yet warranted, the master entry and linked controls must still preserve the same fields and gap discipline.

## 4. Reference implementation: Rollo 1010/2018

The minimum acceptable treatment demonstrated by the current control separates and interlinks:

- proceeding: **Rollo 1010/2018**;
- decision: **Auto 804/2018**;
- NIG: **3500443220180003508**;
- exact organ: **Audiencia Provincial de Las Palmas — Sección Segunda**;
- parent route: **DI 1103/2018-00 → DP 1132/2018 → Rollo 1010/2018 / Auto 804/2018**;
- panel, parties, party-specific professional appearances, date, disposition and costs where supported;
- the boundary that the appellate order records adverse criminal procedural treatment, not a civil/tourism title adjudication;
- the canonical identity **Laura Patricia Acosta Matos**, while preserving a different forename in the source as a source error rather than an alias; and
- the open need for the certified complete docket and missing authority/personación instruments.

The proceeding-specific control is `archive/ROLLO_1010_2018_AUTO_804_CARET_INTERLINK_CONTROL_30AUG2026.md`. Its bilingual pages and reciprocal links are an implementation example, not a reason to omit equivalent available information from any other proceeding.

## 5. Maintenance and completion gate

For every new or materially changed proceeding:

1. search available email, Drive, repository, Library and institutional sources using the reference, decision number, NIG, organ, parties and professional names;
2. open the best available native source and capture all fields in section 2;
3. update the Master CSV, CAEPR identities, professional lineage, specialist controls, interconnectivity edges, corrections and evidence gaps as applicable;
4. create or update the public story and reciprocal links when the proceeding is material and public-safe;
5. test both direct procedural lineage and contextual relevance without merging legally distinct files;
6. run the repository proceedings, identity, professional-lineage and proceeding-specific audits; and
7. verify source, rendered route, deployment and live content separately.

No proceeding refresh may be described as **complete**, **fully captured**, **fully storied** or **fully interlinked** unless every applicable field above is either populated from a cited source or carried as an explicit evidenced gap. Deletion safety requires this governance file and marker to remain linked from the Master Register and Interconnectivity protocols and enforced by CI.
