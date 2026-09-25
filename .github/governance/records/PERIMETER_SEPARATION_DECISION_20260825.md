# Perimeter-separation governance decision — 25 August 2026

**Decision ID:** `PD-PERIMETER-DEC-20260825-01`  
**Policy:** `PD-PERIMETER-GOV-001`  
**Source main SHA before change:** `a968c51548db1de57b077f5327fe0d279eaf00bd`  
**Status:** governance decision recorded; person-level implementation remains pending express decisions

## User decision

Gil Marer directed that **our perimeter** and the **adverse-parties perimeter** must appear on clearly separate lists.

The repository must not continue to treat every natural person as belonging to one undifferentiated public list. Professionals, institutional actors, witnesses/experts/custodians, transaction-development contacts and unresolved candidates must remain separately classified.

## Scope authorized by this decision

This decision authorizes the repository to record and validate the architecture, classification taxonomy and future-thread rule.

It does **not** by itself authorize:

- assigning every existing person to a public category;
- retaining, adding or removing a civil name from the public website;
- anonymising, partially naming or pseudonymising a particular person;
- withdrawing or deleting an existing public entry;
- publishing private identity mappings, emails, contact details or source locators;
- treating a professional, officeholder, witness or transaction contact as an adverse private actor; or
- changing any allegation, evidential grade or responsibility attribution.

Those actions require the person-specific authorization gate in the controlling protocol.

## Principal lists

1. `OUR_PERIMETER`
2. `ADVERSE_PRIVATE_PERIMETER`

## Mandatory separate lists

3. `PROFESSIONALS`
4. `INSTITUTIONS`
5. `WITNESSES`

## Private-only queues

6. `TRANSACTION_DEVELOPMENT_PRIVATE`
7. `UNRESOLVED_PRIVATE_CANDIDATE`

## Specific continuity controls

- `PD-SP-P-0065` and `PD-SP-P-0066` remain transaction-development identities for governance purposes. They are not authorized for placement in either principal public perimeter merely because of historic banking, investment-banking or transaction-development contact.
- Their immutable IDs remain non-reusable.
- This record does not implement a public withdrawal. Current-display remediation requires an express person-specific decision and a privacy-preserving implementation plan.

## Required next implementation package

Before the public registry is re-rendered:

1. refresh current `main`;
2. scan the repository, website, authorized mailbox and authorized file indexes;
3. prepare the complete private classification and authorization matrix;
4. resolve exact identity, capacity, period and source for each person;
5. obtain Gil Marer’s display decision for every natural person;
6. generate a minimized public projection;
7. render the two principal perimeters separately, followed by the three non-perimeter role lists;
8. keep transaction and unresolved identities private;
9. update ES/EN pages, exports, counts, schemas and validators together; and
10. verify the exact merge SHA on both live language routes.

## No-inference rule

- Our perimeter identifies rights, claimant interests and recovery positions; it is not a list of every ally, adviser or witness.
- Adverse private classification identifies a documented opposing or actor-specific private capacity; it is not a finding of guilt or liability.
- Professionals, officeholders, witnesses and transaction contacts do not inherit a private-party classification from proximity, representation, employment, family, chronology or interest in the asset.

## Thread-continuity instruction

Future threads handling people, actors, contacts, identity, publication, anonymisation or the matter registry must load:

- `PERSON_PERIMETER_START_HERE.md`;
- `.github/governance/PERSON_PERIMETER_SEPARATION_AND_PUBLICATION_PROTOCOL.md`;
- `.github/governance/person-perimeter-classification-policy-v1.json`; and
- `.github/governance/TRANSACTION_DEVELOPMENT_SEPARATION_AND_PUBLICATION_PROTOCOL.md`.

New names are private candidates until the authorization gate is complete.
