# Canonical contradiction capture and propagation rule — 1 October 2026

**Control:** PD-CCR-20261001-01  
**Status:** evidence-governance control.  
**Boundary:** a contradiction record identifies competing propositions and the evidence needed to reconcile them. It is not a finding that anyone lied, acted in bad faith, or committed an offence.

## Trigger

Create or refresh one canonical CONTRADICTION object when a material source:

- directly conflicts with an existing proposition;
- narrows or materially qualifies it;
- uses a different denominator, date, legal entity, role, capacity or procedural stage;
- risks conflating ownership, management, operation, branding, financing, construction, possession or governance;
- presents a forecast as an actual, an award as a payment, or committed capital as disbursed capital;
- omits an intermediate chronology material to authority, provenance, knowledge, causation or recovery; or
- repeats a common press-release/source family in a way that could be mistaken for independent corroboration.

## One logical object; many projections

One contradiction receives one stable logical ID. GitLab, GitHub, Drive, proceeding maps, website pages and publication packages are projections/backlinks, not separate versions of truth.

Each material contradiction must record:

- exact propositions A and B;
- exact source references and source-family IDs;
- speaker/entity/capacity and event/knowledge times;
- contradiction type;
- denominator and scope on each side;
- supporting, contrary, neutral and missing evidence;
- what the contradiction does not establish;
- the finite record capable of resolving it;
- typed dependent objects;
- materially relevant proceeding references;
- correction/supersession history; and
- last verification time.

## Required contradiction types

Use one or more of:

- DIRECT_DOCUMENTARY_CONTRADICTION
- ROLE_OR_CAPACITY_CONFLATION
- OWNERSHIP_MANAGEMENT_BRAND_CONFLATION
- DENOMINATOR_MISMATCH
- TIME_PERIOD_MISMATCH
- FORECAST_VS_ACTUAL
- COMMITMENT_VS_DISBURSEMENT
- AWARD_VS_PAYMENT
- SOURCE_OF_FUNDS_PROVENANCE_TENSION
- CHRONOLOGY_OMISSION
- SOURCE_FAMILY_REPUBLICATION
- STALE_OR_HISTORICAL_REPRESENTATION
- ATTRIBUTION_OR_AUTHORSHIP_CONFLICT
- LEGAL_INTERPRETATION_DIFFERENCE
- PROCEDURAL_STAGE_DIFFERENCE
- RHETORICAL_OR_REPUTATIONAL_CONTRAST
- OPEN_FACTUAL_RECONCILIATION

A slogan, aspiration or value statement is not a factual contradiction merely because conduct is disputed. Record that as a rhetorical/reputational contrast unless a falsifiable factual proposition and contrary evidence are identified.

## Source-family deduplication

A press release syndicated through multiple outlets is one source family unless an outlet adds independent documents, reporting or verification.

Record:
originator -> distributor/wire -> republication -> independent additions, if any.

Repeated publication strengthens evidence of what was publicly presented. It does not independently prove the underlying proposition.

## Exact-statement and role-separation rule

Never silently convert:

- managed hotel -> owned hotel;
- brand/franchise -> owner;
- operator/manager -> registered titleholder;
- group -> one legal person;
- capital committed -> cash paid;
- investment associated with managed assets -> manager's own equity;
- award -> payment;
- forecast/target -> actual;
- later title -> authority at an earlier date.

## Contradiction is not deception

For every contradiction ask:

1. Are the two propositions actually incompatible?
2. Can a different date, denominator, legal entity, role, capacity or accounting treatment reconcile them?
3. What record would resolve the difference?
4. Who can be shown to have known each proposition, and when?
5. What correction, explanation, contrary or exculpatory evidence exists?
6. What does the contradiction not prove?

Intent, bad faith, deception, criminality and personal knowledge require separate actor-specific evidence.

## Dependency propagation

When a contradiction changes status, place every materially dependent object into re-review, including as applicable:

- chronology/event maps;
- actor/entity records;
- title/control/ownership maps;
- finance/source-and-use maps;
- recovery/causation hypotheses;
- correction and missing-evidence registers;
- proceeding records;
- institutional communications;
- website/publication pages;
- media/rectification and social-publication packages; and
- both repository projections.

Use typed RELEVANT_TO / TRIGGERS_REVIEW_OF edges. Do not propagate to a proceeding merely because it exists: materiality, jurisdiction and procedural relevance must be recorded.

## Proceeding backlink

For each materially relevant proceeding record:

contradiction_id -> proceeding_id -> issue affected -> procedural status -> already filed? -> source/filing reference -> next permissible use.

Permitted states:
NOT_RELEVANT, INTERNAL_REVIEW, READY_FOR_COUNSEL, FILED, ACKNOWLEDGED, DECIDED, SUPERSEDED.

Internal interlinking is not authority to file externally.

## Public-output gate

Public material derived from a contradiction should distinguish:

- PUBLIC/CORPORATE REPRESENTATION
- VERIFIED SOURCE FACT
- PARTY ALLEGATION
- MATERIAL TENSION / CONTRADICTION
- OPEN RECONCILIATION
- CONTRARY / EXCULPATORY EVIDENCE
- WHAT THIS DOES NOT PROVE

Prefer dates, documents, capacities and denominators over rhetorical labels.

## Relationship to existing controls

This rule supplements the Evidence Control Plane, Truth Machine v2, Correction Register, Missing Evidence Register, unitary reconstruction protocol and source-specific publication gates. Source-specific corrections continue to govern the merits of an individual proposition; this rule governs contradiction capture, deduplication, interlinking and propagation.
